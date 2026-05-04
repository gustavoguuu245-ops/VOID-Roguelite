import random
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field

from configuration.engine import calcular_dano, processar_efeitos_pos_ataque
from systems.battle import determinar_ordem_turno
import systems.eventos as eventos_sys
from configuration.database import ataques_especiais_db

@dataclass
class MonstroBatalha:
    """Wrapper para monstros em batalha de liga (Garante sincronia com engine)"""
    dados: dict
    hp_atual: int = 0
    en_atual: int = 0
    posicao: int = 0 
    vivo: bool = True
    
    def __post_init__(self):
        # Sincroniza os dados do dict com as variáveis de controle da batalha
        self.hp_atual = self.dados.get("hp", self.dados.get("hp_max", 100))
        self.en_atual = self.dados.get("en", self.dados.get("en_max", 100))
        self.dados["hp"] = self.hp_atual
        self.dados["en"] = self.en_atual

    @property
    def nome(self) -> str: return self.dados.get("nome", "Desconhecido")
    
    @property
    def hp_max(self) -> int: return self.dados.get("hp_max", 100)

    def esta_vivo(self) -> bool:
        return self.hp_atual > 0

    def atualizar_dict(self):
        """Mantém o dicionário interno atualizado para as funções externas (engine/eventos)"""
        self.dados["hp"] = self.hp_atual
        self.dados["en"] = self.en_atual

    def receber_dano(self, dano: int):
        self.hp_atual = max(0, self.hp_atual - dano)
        self.atualizar_dict()
        if self.hp_atual <= 0: self.vivo = False

class BatalhaLiga4x4:
    def __init__(self, time_jogador: List[dict], time_adversario: List[dict], 
                 evento_ativo: Optional[str] = None, 
                 nome_j: str = "Jogador", nome_a: str = "IA"):
        
        self.time_j = [MonstroBatalha(m.copy(), posicao=i) for i, m in enumerate(time_jogador[:4])]
        self.time_a = [MonstroBatalha(m.copy(), posicao=i) for i, m in enumerate(time_adversario[:4])]
        
        self.nome_time_j = nome_j
        self.nome_time_a = nome_a
        self.evento_ativo = evento_ativo
        
        self.ativo_j = 0
        self.ativo_a = 0
        self.turno_atual = 0
        self.abates_j = 0
        self.abates_a = 0
        
        self.log: List[str] = []
        self.finalizada = False
        self.vencedor = None

    def processar_turno_jogador(self, tipo_ataque: str):
        """Executa a rodada completa: Player -> IA -> Eventos (Igual ao main.py)"""
        if self.finalizada: return

        self.turno_atual += 1
        m_j = self.time_j[self.ativo_j]
        m_a = self.time_a[self.ativo_a]

        # 1. Determinar Ordem (Engine)
        ordem = determinar_ordem_turno(m_j.dados, m_a.dados)
        
        for atacante_tipo in ordem:
            # Revalida vivos a cada sub-turno
            if not m_j.esta_vivo() or not m_a.esta_vivo(): break

            if atacante_tipo == "player":
                self._executar_ataque(m_j, m_a, tipo_ataque)
            else:
                # IA decide: 30% chance de especial se tiver EN (Igual ao main)
                acao_ia = "especial" if m_a.en_atual >= 35 and random.random() < 0.3 else "base"
                self._executar_ataque(m_a, m_j, acao_ia)

        # 2. Processar Efeitos Ambientais (Eventos.py)
        # Passamos os dicts para a função original que você já usa no main
        logs_clima = eventos_sys.processar_efeitos_ambientais(m_j.dados, m_a.dados, self.evento_ativo)
        
        # Sincroniza HP/EN após o clima
        m_j.hp_atual, m_j.en_atual = m_j.dados["hp"], m_j.dados["en"]
        m_a.hp_atual, m_a.en_atual = m_a.dados["hp"], m_a.dados["en"]

        if logs_clima: self.log.extend(logs_clima)

        # 3. Verificações de Morte e Substituição
        self._checar_substituicoes()
        self._verificar_vitoria()

    def _executar_ataque(self, atacante: MonstroBatalha, defensor: MonstroBatalha, tipo: str):
        """Lógica de Dano + Passivas (Vampirismo/Reflexo)"""
        dano, crit, msg = calcular_dano(atacante.dados, defensor.dados, tipo)
        defensor.receber_dano(dano)

        # Processa Vampirismo/Reflexo (Engine)
        logs_pos = processar_efeitos_pos_ataque(atacante.dados, defensor.dados, dano)
        
        # Sincroniza Wrappers
        atacante.hp_atual, atacante.en_atual = atacante.dados["hp"], atacante.dados["en"]
        defensor.hp_atual, defensor.en_atual = defensor.dados["hp"], defensor.dados["en"]

        prefixo = "[CRIT!] " if crit else ""
        self.log.append(f"{atacante.nome} -> {tipo.upper()}: {prefixo}{dano} DMG")
        if logs_pos: self.log.extend(logs_pos)

    def _checar_substituicoes(self):
        """Puxa o próximo monstro vivo da lista (Troca Automática)"""
        # Jogador
        if not self.time_j[self.ativo_j].esta_vivo():
            self.abates_a += 1
            for i in range(len(self.time_j)):
                if self.time_j[i].esta_vivo():
                    self.ativo_j = i
                    self.log.append(f"REFORÇO: {self.time_j[i].nome} ENTROU NA ARENA!")
                    break
        
        # IA
        if not self.time_a[self.ativo_a].esta_vivo():
            self.abates_j += 1
            for i in range(len(self.time_a)):
                if self.time_a[i].esta_vivo():
                    self.ativo_a = i
                    self.log.append(f"IA: {self.time_a[i].nome} CONECTADO!")
                    break

    def _verificar_vitoria(self):
        vivo_j = any(m.esta_vivo() for m in self.time_j)
        vivo_a = any(m.esta_vivo() for m in self.time_a)

        if not vivo_a:
            self.finalizada = True
            self.vencedor = "jogador"
        elif not vivo_j:
            self.finalizada = True
            self.vencedor = "adversario"

    def get_status(self) -> Dict:
        """Retorna os dados para a UI (ligaui.py) desenhar"""
        m_j = self.time_j[self.ativo_j]
        m_a = self.time_a[self.ativo_a]
        return {
            "jogador": {
                "nome_time": self.nome_time_j,
                "monstro_ativo": {"nome": m_j.nome, "hp": m_j.hp_atual, "hp_max": m_j.hp_max, "en": m_j.en_atual, "posicao": self.ativo_j},
                "abates": self.abates_j
            },
            "adversario": {
                "nome_time": self.nome_time_a,
                "monstro_ativo": {"nome": m_a.nome, "hp": m_a.hp_atual, "hp_max": m_a.hp_max, "en": m_a.en_atual, "posicao": self.ativo_a},
                "abates": self.abates_a
            },
            "log": self.log[-3:] if self.log else [] # Últimas 3 mensagens
        }

    def get_resultado_final(self) -> Tuple[bool, int, int]:
        return (self.vencedor == "jogador"), self.abates_j, self.abates_a