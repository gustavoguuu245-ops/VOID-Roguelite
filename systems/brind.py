import pygame
import random
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from configuration.config import *
from configuration.database import tribos_info

@dataclass
class BrindResultado:
    sucesso: bool
    boost: float
    perdeu_alvo: bool
    mensagem: str


class BrindSystem:
    def __init__(self):
        self.alvo_index = -1
        self.sacrif_index = -1
        self.atributo_escolhido = None   # "hp", "atk", "def", "agi"
        self.nivel_risco = "Médio"       # Leve, Médio, Abismo

    def processar_input(self, evento, hangar):
        if evento.type != pygame.KEYDOWN:
            return None

        # Navegação de monstros
        if evento.key == pygame.K_1:      # Tecla 1 = Alvo
            self.alvo_index = (self.alvo_index + 1) % len(hangar)
        elif evento.key == pygame.K_2:    # Tecla 2 = Sacrifício
            self.sacrif_index = (self.sacrif_index + 1) % len(hangar)

        # Mudar Atributo (Z / X)
        attrs = ["hp", "atk", "def", "agi"]
        if self.atributo_escolhido is None:
            self.atributo_escolhido = "hp"
        idx = attrs.index(self.atributo_escolhido)
        if evento.key == pygame.K_z:
            self.atributo_escolhido = attrs[(idx - 1) % 4]
        elif evento.key == pygame.K_x:
            self.atributo_escolhido = attrs[(idx + 1) % 4]

        # Mudar Nível de Risco (C / V)
        niveis = ["Leve", "Médio", "Abismo"]
        idx_r = niveis.index(self.nivel_risco)
        if evento.key == pygame.K_c:
            self.nivel_risco = niveis[(idx_r - 1) % 3]
        elif evento.key == pygame.K_v:
            self.nivel_risco = niveis[(idx_r + 1) % 3]

        # Executar o Brind
        if evento.key == pygame.K_SPACE:
            if self.alvo_index == -1 or self.sacrif_index == -1:
                return BrindResultado(False, 0.0, False, "Selecione Alvo (tecla 1) e Sacrifício (tecla 2)")
            return self.executar_brind(hangar, self.alvo_index, self.sacrif_index, self.atributo_escolhido, self.nivel_risco)

        # Voltar para o Hangar
        if evento.key in (pygame.K_m, pygame.K_ESCAPE):
            self.reset()
            return "HANGAR"

        return None
    
    def pode_fazer_brind(self, hangar: list, alvo_idx: int, sacrif_idx: int, atributo: str) -> Tuple[bool, str]:
        if alvo_idx == sacrif_idx:
            return False, "Não pode sacrificar o mesmo monstro."

        alvo = hangar[alvo_idx]
        sacrif = hangar[sacrif_idx]

        # Regra: Mesma tribo
        if alvo.get("tribo") != sacrif.get("tribo"):
            return False, "O Véu só aceita sacrifícios entre monstros da mesma tribo."

        # DNA do sacrifício deve ser maior
        if sacrif["dna"][atributo] <= alvo["dna"][atributo]:
            return False, f"O DNA de {atributo.upper()} do sacrifício não é superior ao do alvo."

        return True, ""

    def calcular_brind(self, nivel: str) -> Dict:
        if nivel == "Leve":
            chance = 0.75
            boost_min, boost_max = 0.01, 0.03
            perde_alvo_chance = 0.0
        elif nivel == "Médio":
            chance = 0.48
            boost_min, boost_max = 0.04, 0.07
            perde_alvo_chance = 0.35
        else:  # Abismo
            chance = 0.22
            boost_min, boost_max = 0.08, 0.12
            perde_alvo_chance = 1.0

        sucesso = random.random() < chance
        boost = round(random.uniform(boost_min, boost_max), 2)

        return {
            "sucesso": sucesso,
            "boost": boost,
            "perde_alvo_chance": perde_alvo_chance
        }

    def executar_brind(self, hangar: list, alvo_idx: int, sacrif_idx: int, atributo: str, nivel: str) -> BrindResultado:
        pode, msg = self.pode_fazer_brind(hangar, alvo_idx, sacrif_idx, atributo)
        if not pode:
            return BrindResultado(False, 0.0, False, msg)

        resultado = self.calcular_brind(nivel)

        alvo = hangar[alvo_idx]
        sacrif = hangar[sacrif_idx]

        if resultado["sucesso"]:
            boost_final = min(1.8, alvo["dna"][atributo] + resultado["boost"])
            alvo["dna"][atributo] = round(boost_final, 2)
            
            # Remove o sacrifício
            del hangar[sacrif_idx]
            if sacrif_idx < alvo_idx:  # ajusta índice se necessário
                alvo_idx -= 1

            return BrindResultado(
                True, 
                resultado["boost"], 
                False,
                f"Sucesso! O Véu aceitou o sacrifício.\n+{resultado['boost']:.2f} em {atributo.upper()}"
            )
        else:
            # Falha
            del hangar[sacrif_idx]  # sempre perde o sacrifício
            perdeu_alvo = random.random() < resultado["perde_alvo_chance"]
            
            if perdeu_alvo and alvo_idx < len(hangar):
                del hangar[alvo_idx]
                return BrindResultado(False, 0.0, True, "O Abismo devorou ambos...")
            else:
                return BrindResultado(False, 0.0, False, "O sacrifício foi rejeitado pelo Véu.")

    def reset(self):
        self.ativo = False
        self.alvo_index = -1
        self.sacrif_index = -1
        self.atributo_escolhido = None
        self.nivel_risco = "Médio"