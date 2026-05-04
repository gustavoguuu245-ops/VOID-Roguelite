import pygame
from configuration.config import *
from configuration.database import ataques_especiais_db, tribos_info

class HangarSystem:
    def __init__(self, tela, fontes):
        self.tela = tela
        self.fonte_titulo = fontes['titulo']
        self.fonte_menu = fontes['menu']
        self.fonte_pequena = fontes['pequena']
        self.botao_preparar_rect = pygame.Rect(680, 500, 200, 50)
        
        # FIX: Surface do botão glow criada UMA VEZ só
        self.botao_glow = pygame.Surface((196, 46))
        self.botao_glow.set_alpha(60)
        self.botao_glow.fill(VERDE_SISTEMA)

    def desenhar_interface(self, hangar, time_jogador, monstro_ativo_index):
        # Título
        self.tela.blit(self.fonte_titulo.render("HANGAR DE DADOS", True, AZUL_HUD), (50, 50))
        
        # --- LISTA À ESQUERDA ---
        for i, m in enumerate(hangar):
            marcador = ""
            if m in time_jogador:
                posicao = time_jogador.index(m) + 1
                marcador = f" [TIME {posicao}]"
            
            # Cores Dinâmicas
            if i == monstro_ativo_index:
                cor = VERDE_SISTEMA
            elif m in time_jogador:
                cor = (255, 215, 0) # Amarelo Ouro
            else:
                cor = (100, 100, 100) # Cinza
            
            txt_completo = f"{i+1}. {m['nome']} Lv.{m['lvl']}{marcador}"
            txt = self.fonte_menu.render(txt_completo, True, cor)
            self.tela.blit(txt, (50, 150 + i*50))
        
        # --- DETALHES À DIREITA ---
        if hangar:
            m = hangar[monstro_ativo_index]
            esp = ataques_especiais_db.get(m.get("esp_id", "brasas"), {})
            cor_t = tribos_info[m["tribo"]]["cor"]
            
            self.tela.blit(self.fonte_menu.render(f"DADOS DE: {m['nome']}", True, cor_t), (450, 100))
            dna_medio = round(sum(m['dna'].values())/4, 2)
            self.tela.blit(self.fonte_pequena.render(f"TRIBO: {m['tribo']} | DNA MÉDIO: {dna_medio}", True, (200, 200, 200)), (450, 140))
            
            # Stats e DNAs
            self.tela.blit(self.fonte_pequena.render(f"HP:  {m['hp']}/{m['hp_max']}  (DNA: {m['dna']['hp']})", True, VERDE_SISTEMA), (450, 180))
            self.tela.blit(self.fonte_pequena.render(f"ATK: {m['atk']}  (DNA: {m['dna']['atk']})", True, (255, 100, 100)), (450, 210))
            self.tela.blit(self.fonte_pequena.render(f"DEF: {m['def']}  (DNA: {m['dna']['def']})", True, (100, 100, 255)), (450, 240))
            self.tela.blit(self.fonte_pequena.render(f"AGI: {m['agi']}  (DNA: {m['dna']['agi']})", True, CIANO_XP), (450, 270))
            
            # Especial e Skill
            self.tela.blit(self.fonte_pequena.render(f"ESPECIAL: {esp.get('nome','--')} (CUSTO: {esp.get('en',0)} EN)", True, VIOLETA_SCANNER), (450, 320))
            if m.get("hab"):
                self.tela.blit(self.fonte_pequena.render(f"HABILIDADE: {m['hab'].upper()}", True, OURO_STATUS), (450, 350))
            
            # XP Bar
            pygame.draw.rect(self.tela, (40, 40, 40), (450, 400, 350, 10))
            xp_progresso = (m["xp"]/m["xp_max"]) * 350
            pygame.draw.rect(self.tela, CIANO_XP, (450, 400, xp_progresso, 10))
            self.tela.blit(self.fonte_pequena.render(f"XP: {m['xp']}/{m['xp_max']}", True, CIANO_XP), (450, 415))

        # --- BOTÃO IR PARA LIGA (Antigo Preparar) ---
        # Agora calculamos o time baseado nos monstros que possuem a tag persistente
        time_escalado = [m for m in hangar if m.get('no_time', False)]
        pode_preparar = len(time_escalado) == 4 
        
        cor_botao = VERDE_SISTEMA if pode_preparar else (100, 100, 100)
        
        # Desenha a borda do botão
        pygame.draw.rect(self.tela, cor_botao, self.botao_preparar_rect, 2)
        
        # Se estiver pronto (4/4), desenha o preenchimento brilhante
        if pode_preparar:
           self.tela.blit(self.botao_glow, (682, 502))
        
        # Texto atualizado para IR PARA LIGA
        texto_prep = self.fonte_menu.render("IR PARA LIGA >", True, cor_botao)
        self.tela.blit(texto_prep, (690, 512)) 
        
        # Status de escalação dinâmico
        status_time = f"TIME: {len(time_escalado)}/4"
        self.tela.blit(self.fonte_pequena.render(status_time, True, cor_botao), (720, 475))
        self.tela.blit(self.fonte_pequena.render("[SETAS] NAVEGAR   [SPACE] ESCALAR   [M] MENU", True, VERDE_SISTEMA), (50, 550))

    def checar_clique_preparar(self, mouse_pos, time_jogador):
        """
        Verifica se o time está pronto e o botão foi clicado.
        O main.py envia a lista filtrada como 'time_jogador'.
        """
        if self.botao_preparar_rect.collidepoint(mouse_pos):
            # Validação final antes de entrar na Liga
            if len(time_jogador) == 4:
                return True, time_jogador[0], "MENU_LIGA", "SISTEMA SINCRONIZADO. LIGA ACESSÍVEL."
            else:
                return False, None, "HANGAR", "ERRO: SELECIONE 4 UNIDADES PARA A LIGA."
        return None