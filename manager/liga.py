# liga_manager.py
# Motor da Liga V.O.I.D. - Sistema de Campeonato por Pontos

import random
import json
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

from configuration.database import monstros_db, tribos_info, TIERS
from configuration.engine import gerar_instancia_monster, calcular_dano


class Divisao(Enum):
    SERIE_A = "Série A"
    SERIE_B = "Série B"  
    SERIE_C = "Série C"
    SERIE_D = "Série D"

# Level Cap por divisão
LEVEL_CAPS = {
    Divisao.SERIE_D: 15,
    Divisao.SERIE_C: 35,
    Divisao.SERIE_B: 60,
    Divisao.SERIE_A: 100
}

# Número de times por divisão
TIMES_POR_DIVISAO = 20
RODADAS_TOTAIS = 38  # Turno + Returno
FORMATO_LIGA = 4  # 4x4 monstros

# Bônus de sinergia por tribo
BONUS_SINERGIA = 0.15  # +15% se 2+ da mesma tribo
BONUS_VANTAGEM_TIPO = 0.20  # +20% vantagem elemental

# Mapeamento de vantagens tribais (quem ganha de quem)
# Fogo > Gelo > Naturalistas > Mecânica > Esquecidos > Sombras > Fogo
VANTAGENS_TRIBO = {
    "Fogo": ["Gelo", "Naturalistas"],
    "Gelo": ["Naturalistas", "Mecânica"],
    "Naturalistas": ["Mecânica", "Esquecidos"],
    "Mecânica": ["Esquecidos", "Sombras"],
    "Esquecidos": ["Sombras", "Fogo"],
    "Sombras": ["Fogo", "Gelo"]
}


@dataclass
class TimeLiga:
    id: int
    nome: str
    divisao: Divisao
    monstros: List[dict] = field(default_factory=list)
    vitorias: int = 0
    derrotas: int = 0
    empates: int = 0  # Teoricamente 0, mas mantemos por segurança
    gols_feitos: int = 0  # Abates totais
    gols_sofridos: int = 0  # Abates sofridos
    pontos: int = 0
    posicao: int = 0
    historico: List[str] = field(default_factory=list)
    
    @property
    def jogos(self) -> int:
        return self.vitorias + self.derrotas + self.empates
    
    @property
    def saldo(self) -> int:
        return self.gols_feitos - self.gols_sofridos
    
    def calcular_pc(self) -> float:
        """Poder de Combate - soma dos status reais do time"""
        pc_total = 0
        tribos_count = {}
        
        for m in self.monstros:
            if not m:
                continue
            pc = m.get("atk", 0) + m.get("def", 0) + m.get("hp_max", 0) + m.get("agi", 0)
            pc_total += pc
            
            tribo = m.get("tribo", "Desconhecido")
            tribos_count[tribo] = tribos_count.get(tribo, 0) + 1
        
        # Bônus de sinergia
        sinergia = 1.0
        for tribo, count in tribos_count.items():
            if count >= 2:
                sinergia += BONUS_SINERGIA
        
        return pc_total * sinergia
    
    def obter_tribos_majoritarias(self) -> List[str]:
        """Retorna as tribos que aparecem 2+ vezes no time"""
        tribos_count = {}
        for m in self.monstros:
            tribo = m.get("tribo", "Desconhecido")
            tribos_count[tribo] = tribos_count.get(tribo, 0) + 1
        
        return [t for t, c in tribos_count.items() if c >= 2]


@dataclass
class EstatisticaArtilharia:
    monstro_nome: str
    time_nome: str
    tribo: str
    abates: int = 0
    jogos: int = 0
    divisao: str = ""
    
    @property
    def media(self) -> float:
        return self.abates / max(self.jogos, 1)


class LigaManager:
    def __init__(self):
        self.divisoes: Dict[Divisao, List[TimeLiga]] = {d: [] for d in Divisao}
        self.calendario: Dict[int, List[Tuple[int, int, Divisao]]] = {}  # rodada -> [(time1, time2, div)]
        self.rodada_atual: int = 0
        self.artilharia: Dict[str, EstatisticaArtilharia] = {}  # nome -> stats
        self.time_jogador_id: Optional[str] = "PLAYER_OPERADOR"
        
        # FIX: Inicializamos como Série D para evitar erro de None no ligaui.py
        self.time_jogador_divisao: Divisao = Divisao.SERIE_D 
        self.nome_operador: str = "Operador"
        self.time_jogador_atual: List[dict] = []
        
        # Controle de partida atual
        self.partida_atual: Optional[Tuple[TimeLiga, TimeLiga]] = None
        self.resultados_rodada: List[str] = []

    def configurar_time_jogador(self, nome_op: str, time: List[dict]):
        """
        Sincroniza os monstros escolhidos no Hangar com o motor da Liga.
        """
        self.nome_operador = nome_op
        self.time_jogador_atual = time
        self.time_jogador_id = "PLAYER_OPERADOR"
        
        # Garante que a divisão esteja setada ao configurar o time
        if not self.time_jogador_divisao:
            self.time_jogador_divisao = Divisao.SERIE_D

        # VERIFICAÇÃO CHAVE: Se a Série D estiver vazia, inicializa a liga inteira
        if not self.divisoes[Divisao.SERIE_D]:
            print("🚀 Gerando nova temporada da Liga V.O.I.D...")
            self.inicializar_liga(time, nome_op, self.time_jogador_divisao)


    def inicializar_liga(self, time_jogador_monstros: List[dict], nome_jogador: str, 
                         divisao_inicial: Divisao = Divisao.SERIE_D):
        """
        Cria todas as divisões com 20 times cada.
        O time do jogador substitui um time aleatório na divisão inicial.
        """
        self.nome_operador = nome_jogador
        self.time_jogador_divisao = divisao_inicial
        lvl_cap = LEVEL_CAPS[divisao_inicial]
        
        # Gera times para cada divisão
        for div in Divisao:
            cap = LEVEL_CAPS[div]
            for i in range(TIMES_POR_DIVISAO):
                time_id = div.value + f"_{i:02d}"
                
                # Nome temático baseado na divisão
                nomes_prefixos = {
                    Divisao.SERIE_A: ["Alpha", "Omega", "Nexus", "Apex", "Prime"],
                    Divisao.SERIE_B: ["Cyber", "Neon", "Steel", "Iron", "Chrome"],
                    Divisao.SERIE_C: ["Rogue", "Shadow", "Ghost", "Phantom", "Void"],
                    Divisao.SERIE_D: ["Nova", "Spark", "Bit", "Pixel", "Data"]
                }
                prefixo = random.choice(nomes_prefixos[div])
                sufixo = random.choice(["Squad", "Unit", "Cell", "Core", "Node"])
                nome_time = f"{prefixo}-{sufixo}-{random.randint(10,99)}"
                
                # Gera 4 monstros para o time
                monstros_time = self._gerar_time_npc(cap, div)
                
                time = TimeLiga(
                    id=time_id,
                    nome=nome_time,
                    divisao=div,
                    monstros=monstros_time
                )
                self.divisoes[div].append(time)
        
        # Substitui um time pelo do jogador na divisão inicial
        idx_substituir = random.randint(0, TIMES_POR_DIVISAO - 1)
        time_jogador = TimeLiga(
            id="PLAYER_OPERADOR", # ID Harmonizado para não dar erro na Tabela
            nome=f"[{nome_jogador.upper()}] SQUAD",
            divisao=divisao_inicial,
            monstros=time_jogador_monstros
        )
        self.divisoes[divisao_inicial][idx_substituir] = time_jogador
        self.time_jogador_id = time_jogador.id
        
        # Gera calendário de rodadas (turno + returno)
        self._gerar_calendario()
        
        print(f"🏆 Liga V.O.I.D. Inicializada!")
        print(f"   Divisão do Jogador: {divisao_inicial.value} (Cap Lvl {lvl_cap})")
        print(f"   Times: {TIMES_POR_DIVISAO} por divisão | Rodadas: {RODADAS_TOTAIS}")
    
    def _gerar_time_npc(self, level_cap: int, divisao: Divisao) -> List[dict]:
        """Gera um time de 4 monstros NPC balanceado para a divisão"""
        time = []
        nomes_usados = set()
        
        # Sorteia 4 monstros do banco
        for _ in range(FORMATO_LIGA):
            nome_base = random.choice(list(monstros_db.keys()))
            # Evita duplicatas no mesmo time
            while nome_base in nomes_usados and len(nomes_usados) < len(monstros_db):
                nome_base = random.choice(list(monstros_db.keys()))
            nomes_usados.add(nome_base)
            
            # Gera instância com level no cap
            monstro = gerar_instancia_monster(nome_base, monstros_db)
            monstro["lvl"] = level_cap
            
            # Aplica buff de nível conforme a engine faz
            mult_hp = 1 + (level_cap - 1) * 0.12
            mult_atk = 1 + (level_cap - 1) * 0.10
            
            monstro["hp_max"] = int(monstro["hp_max"] * mult_hp)
            monstro["hp"] = monstro["hp_max"]
            monstro["atk"] = int(monstro["atk"] * mult_atk)
            monstro["en"] = monstro["en_max"]
            monstro["time_nome"] = None  # Será preenchido depois
            
            time.append(monstro)
        
        return time
    
    def _gerar_calendario(self):
        """Gera o calendário de 38 rodadas (turno + returno) para cada divisão"""
        for div in Divisao:
            times = self.divisoes[div]
            n = len(times)
            
            # Algoritmo round-robin para gerar confrontos
            # Fixa o primeiro time e rotaciona os outros
            rodadas_turno = n - 1
            rodadas_returno = n - 1
            total_rodadas = rodadas_turno + rodadas_returno  # = 38 para n=20
            
            # Cria lista de índices
            indices = list(range(n))
            
            for rodada in range(1, total_rodadas + 1):
                if rodada not in self.calendario:
                    self.calendario[rodada] = []
                
                # Determina se é turno ou returno
                if rodada <= rodadas_turno:
                    # Turno: i vs j normal
                    for i in range(n // 2):
                        t1 = indices[i]
                        t2 = indices[n - 1 - i]
                        self.calendario[rodada].append((t1, t2, div))
                else:
                    # Returno: inverte mandante
                    for i in range(n // 2):
                        t1 = indices[n - 1 - i]
                        t2 = indices[i]
                        self.calendario[rodada].append((t1, t2, div))
                
                # Rotaciona (exceto o primeiro)
                indices = [indices[0]] + [indices[-1]] + indices[1:-1]
    
    def simular_rodada_completa(self) -> List[str]:
        """
        Simula todos os jogos da rodada atual (exceto o do jogador).
        Retorna lista de resultados em formato string.
        """
        if self.rodada_atual >= RODADAS_TOTAIS:
            return ["🏆 TEMPORADA ENCERRADA!"]
        
        self.resultados_rodada = []
        jogos_hoje = self.calendario.get(self.rodada_atual + 1, [])
        
        partida_jogador = None
        
        for t1_idx, t2_idx, div in jogos_hoje:
            times = self.divisoes[div]
            time1 = times[t1_idx]
            time2 = times[t2_idx]
            
            # Verifica se é partida do jogador
            if time1.id == self.time_jogador_id or time2.id == self.time_jogador_id:
                # Guarda para batalha manual
                self.partida_atual = (time1, time2)
                continue
            
            # Simula IA x IA
            vencedor, abates_t1, abates_t2 = self._simular_partida_ia(time1, time2)
            
            # Atualiza estatísticas
            self._atualizar_estatisticas(time1, time2, vencedor, abates_t1, abates_t2)
            
            # Registra resultado
            resultado = f"{time1.nome} {abates_t1} x {abates_t2} {time2.nome}"
            if vencedor == time1:
                resultado += " ✓"
            elif vencedor == time2:
                resultado += " ✓"
            self.resultados_rodada.append(resultado)
        
        return self.resultados_rodada
    
    def _simular_partida_ia(self, time1: TimeLiga, time2: TimeLiga) -> Tuple[TimeLiga, int, int]:
        """
        Simula uma partida 4x4 entre dois times NPC.
        Retorna: (vencedor, abates_t1, abates_t2)
        """
        pc1 = time1.calcular_pc()
        pc2 = time2.calcular_pc()
        
        # Vantagem de tipo
        tribos_t1 = set(m.get("tribo", "") for m in time1.monstros)
        tribos_t2 = set(m.get("tribo", "") for m in time2.monstros)
        
        vantagem_t1 = 0
        vantagem_t2 = 0
        
        for t1 in tribos_t1:
            if t1 in VANTAGENS_TRIBO:
                for t2 in tribos_t2:
                    if t2 in VANTAGENS_TRIBO[t1]:
                        vantagem_t1 += 1
        
        for t2 in tribos_t2:
            if t2 in VANTAGENS_TRIBO:
                for t1 in tribos_t1:
                    if t1 in VANTAGENS_TRIBO[t2]:
                        vantagem_t2 += 1
        
        # Aplica bônus de vantagem
        if vantagem_t1 > vantagem_t2:
            pc1 *= (1 + BONUS_VANTAGEM_TIPO)
        elif vantagem_t2 > vantagem_t1:
            pc2 *= (1 + BONUS_VANTAGEM_TIPO)
        
        # Bônus de sinergia já está no calcular_pc()
        
        # Determina vencedor com variação aleatória (upset possível)
        diferenca = abs(pc1 - pc2)
        max_pc = max(pc1, pc2)
        
        # Chance base do mais forte vencer
        if pc1 > pc2:
            chance_t1 = 0.5 + (diferenca / max_pc) * 0.4  # Entre 50% e 90%
        elif pc2 > pc1:
            chance_t1 = 0.5 - (diferenca / max_pc) * 0.4  # Entre 10% e 50%
        else:
            chance_t1 = 0.5
        
        # Limita entre 10% e 90%
        chance_t1 = max(0.1, min(0.9, chance_t1))
        
        # Sorteia vencedor
        if random.random() < chance_t1:
            vencedor = time1
            # Abates baseados na força relativa
            abates_t1 = random.randint(2, 4)
            abates_t2 = random.randint(0, abates_t1 - 1)
        else:
            vencedor = time2
            abates_t2 = random.randint(2, 4)
            abates_t1 = random.randint(0, abates_t2 - 1)
        
        # Atualiza artilharia dos monstros vencedores
        self._registrar_abates(vencedor, max(abates_t1, abates_t2))
        
        return vencedor, abates_t1, abates_t2
    
    def _registrar_abates(self, time: TimeLiga, quantidade: int):
        """Registra abates para monstros do time vencedor"""
        monstros_vivos = [m for m in time.monstros if m]
        if not monstros_vivos:
            return
        
        for _ in range(quantidade):
            # Sorteia um monstro do time para receber o abate
            m = random.choice(monstros_vivos)
            nome = m.get("nome", "Desconhecido")
            chave = f"{nome}_{time.nome}"
            
            if chave not in self.artilharia:
                self.artilharia[chave] = EstatisticaArtilharia(
                    monstro_nome=nome,
                    time_nome=time.nome,
                    tribo=m.get("tribo", "Desconhecido"),
                    divisao=time.divisao.value
                )
            
            self.artilharia[chave].abates += 1
            self.artilharia[chave].jogos += 1
    
    def _atualizar_estatisticas(self, time1: TimeLiga, time2: TimeLiga, 
                                vencedor: TimeLiga, abates_t1: int, abates_t2: int):
        """Atualiza tabela de classificação após uma partida"""
        time1.gols_feitos += abates_t1
        time1.gols_sofridos += abates_t2
        time2.gols_feitos += abates_t2
        time2.gols_sofridos += abates_t1
        
        if vencedor == time1:
            time1.vitorias += 1
            time1.pontos += 3
            time2.derrotas += 1
        elif vencedor == time2:
            time2.vitorias += 1
            time2.pontos += 3
            time1.derrotas += 1
        else:
            # Empate teórico (não deve acontecer, mas por segurança)
            time1.empates += 1
            time2.empates += 1
            time1.pontos += 1
            time2.pontos += 1
        
        # Atualiza jogos dos monstros
        for m in time1.monstros:
            if m:
                nome = m.get("nome", "Desconhecido")
                chave = f"{nome}_{time1.nome}"
                if chave in self.artilharia:
                    self.artilharia[chave].jogos += 1
        
        for m in time2.monstros:
            if m:
                nome = m.get("nome", "Desconhecido")
                chave = f"{nome}_{time2.nome}"
                if chave in self.artilharia:
                    self.artilharia[chave].jogos += 1
    
    def processar_resultado_jogador(self, time_jogador: TimeLiga, time_adversario: TimeLiga,
                                    venceu: bool, abates_jogador: int, abates_adversario: int):
        """Processa o resultado após o jogador jogar sua partida manualmente"""
        time_jogador.gols_feitos += abates_jogador
        time_jogador.gols_sofridos += abates_adversario
        time_adversario.gols_feitos += abates_adversario
        time_adversario.gols_sofridos += abates_jogador
        
        if venceu:
            time_jogador.vitorias += 1
            time_jogador.pontos += 3
            time_adversario.derrotas += 1
            self._registrar_abates(time_jogador, abates_jogador)
        else:
            time_adversario.vitorias += 1
            time_adversario.pontos += 3
            time_jogador.derrotas += 1
            self._registrar_abates(time_adversario, abates_adversario)
        
        self.partida_atual = None
        self.rodada_atual += 1
        
        # Atualiza classificação
        self._ordenar_classificacao()
    
    def _ordenar_classificacao(self):
        """Ordena times por pontos, saldo, gols feitos"""
        for div in Divisao:
            times = self.divisoes[div]
            # Sort: pontos DESC, saldo DESC, gols_feitos DESC, vitorias DESC
            times.sort(key=lambda t: (t.pontos, t.saldo, t.gols_feitos, t.vitorias), reverse=True)
            for i, t in enumerate(times):
                t.posicao = i + 1
    
    def get_classificacao(self, divisao: Divisao) -> List[TimeLiga]:
        """Retorna classificação de uma divisão ordenada"""
        self._ordenar_classificacao()
        return self.divisoes[divisao]
    
    def get_top_artilheiros(self, top_n: int = 10) -> List[EstatisticaArtilharia]:
        """Retorna top artilheiros da liga"""
        todos = sorted(self.artilharia.values(), key=lambda x: x.abates, reverse=True)
        return todos[:top_n]
    
    def get_proxima_partida_jogador(self) -> Optional[Tuple[TimeLiga, TimeLiga]]:
        """Retorna a próxima partida do jogador na rodada atual"""
        if self.rodada_atual >= RODADAS_TOTAIS:
            return None
        
        jogos_hoje = self.calendario.get(self.rodada_atual + 1, [])
        
        for t1_idx, t2_idx, div in jogos_hoje:
            times = self.divisoes[div]
            time1 = times[t1_idx]
            time2 = times[t2_idx]
            
            if time1.id == self.time_jogador_id:
                return (time1, time2)
            if time2.id == self.time_jogador_id:
                return (time2, time1)
        
        return None
    
    def verificar_fim_temporada(self) -> bool:
        """Verifica se a temporada acabou e processa promoções/rebaixamentos"""
        if self.rodada_atual < RODADAS_TOTAIS:
            return False
        
        # TODO: Implementar subida/descida de divisão
        # Série A: Campeão ganha título especial
        # Séries B, C, D: Top 4 sobem, Bottom 4 descem
        
        return True
    
    def get_resumo_rodada(self) -> str:
        """Retorna resumo da rodada atual"""
        if not self.resultados_rodada:
            return "Nenhum jogo simulado ainda."
        
        return "\n".join(self.resultados_rodada[:5])  # Top 5 resultados
    
    def salvar(self, filepath: str = "saves/liga_void.json"):
        """Salva estado da liga"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        dados = {
            "rodada_atual": self.rodada_atual,
            "time_jogador_id": self.time_jogador_id,
            "time_jogador_divisao": self.time_jogador_divisao.value if self.time_jogador_divisao else None,
            "nome_operador": self.nome_operador,
            "artilharia": {
                k: {
                    "monstro_nome": v.monstro_nome,
                    "time_nome": v.time_nome,
                    "tribo": v.tribo,
                    "abates": v.abates,
                    "jogos": v.jogos,
                    "divisao": v.divisao
                }
                for k, v in self.artilharia.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Liga salva em {filepath}")
    
    def carregar(self, filepath: str = "saves/liga_void.json") -> bool:
        """Carrega estado da liga"""
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.rodada_atual = dados.get("rodada_atual", 0)
        self.time_jogador_id = dados.get("time_jogador_id")
        div_str = dados.get("time_jogador_divisao")
        if div_str:
            self.time_jogador_divisao = Divisao(div_str)
        self.nome_operador = dados.get("nome_operador", "Operador")
        
        # Reconstrói artilharia
        for k, v in dados.get("artilharia", {}).items():
            self.artilharia[k] = EstatisticaArtilharia(**v)
        
        print(f"📂 Liga carregada. Rodada: {self.rodada_atual}")
        return True