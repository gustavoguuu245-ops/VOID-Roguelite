import pygame
import random
from configuration.config import *
from configuration.database import tribos_info, monstros_db, ataques_especiais_db

class HUD:
    def __init__(self, tela, fontes):
        self.tela = tela
        self.fonte_titulo = fontes['titulo']
        self.fonte_menu = fontes['menu']
        self.fonte_pequena = fontes['pequena']

    def desenhar_login(self, nome_operador, mouse_pos, BOTAO_ACESSAR_RECT):
        txt_v = self.fonte_titulo.render("V.O.I.D. INTERFACE", True, VIOLETA_SCANNER)
        self.tela.blit(txt_v, (LARGURA//2 - txt_v.get_width()//2, 150))
        
        pygame.draw.rect(self.tela, AZUL_HUD, (250, 280, 400, 50), 2)
        txt_op = self.fonte_menu.render(f"OPERADOR: {nome_operador}_", True, VERDE_SISTEMA)
        self.tela.blit(txt_op, (270, 290))
        
        cor_btn = VERDE_SISTEMA if BOTAO_ACESSAR_RECT.collidepoint(mouse_pos) else AZUL_HUD
        pygame.draw.rect(self.tela, cor_btn, BOTAO_ACESSAR_RECT, 2)
        self.tela.blit(self.fonte_menu.render("ACESSAR", True, cor_btn), (405, 430))

    def desenhar_tribo_inicial(self, opcao_selecionada):
        self.tela.blit(self.fonte_titulo.render("SELECIONE SUA TRIBO", True, AZUL_HUD), (230, 80))
        for i, tribo in enumerate(list(tribos_info.keys())):
            cor = tribos_info[tribo]["cor"] if i == opcao_selecionada else (100, 100, 100)
            txt = self.fonte_menu.render(f"[ {tribo.upper()} ]", True, cor)
            self.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, 210 + i*70))

    def desenhar_menu_principal(self, nome_operador, creditos, data_cores, opcao_selecionada, sub_menu, itens_menu, itens_sub_menu):
        self.tela.blit(self.fonte_titulo.render("V.O.I.D. SCANNER", True, VIOLETA_SCANNER), (270, 100))
        self.tela.blit(self.fonte_pequena.render(f"OP: {nome_operador} | CR: {creditos} | CORES: {data_cores}", True, OURO_STATUS), (20, 20))
        
        lista_atual = itens_sub_menu if sub_menu else itens_menu
        for i, item in enumerate(lista_atual):
            cor = VERDE_SISTEMA if i == opcao_selecionada else AZUL_HUD
            txt = self.fonte_menu.render(item, True, cor)
            self.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, 265 + i*60))
        
        self.tela.blit(self.fonte_pequena.render("[ ARQUIVAR ]", True, AZUL_CLARO), (LARGURA - 300, 20))
        self.tela.blit(self.fonte_pequena.render("[ RECUPERAR ]", True, AZUL_CLARO), (LARGURA - 160, 20))

    def desenhar_loja(self, creditos, m_ativo, loja_itens, opcao_selecionada):
        self.tela.blit(self.fonte_titulo.render("LOJA DE SUPRIMENTOS", True, VERDE_SISTEMA), (50, 50))
        self.tela.blit(self.fonte_pequena.render(f"CRÉDITOS: {creditos} | ALVO: {m_ativo['nome']} (HP:{m_ativo['hp']})", True, OURO_STATUS), (50, 110))
        
        for i, item in enumerate(loja_itens):
            cor = AZUL_HUD if i == opcao_selecionada else (100, 100, 100)
            txt = self.fonte_menu.render(f"{item['nome']} - {item['preco']} CR", True, cor)
            self.tela.blit(txt, (50, 180 + i*65))
            self.tela.blit(self.fonte_pequena.render(item['desc'], True, (150,150,150)), (50, 215 + i*65))
        
        self.tela.blit(self.fonte_pequena.render("[ENTER] COMPRAR   [M] MENU", True, VERDE_SISTEMA), (LARGURA//2 - 80, 550))
    def desenhar_caixa_mensagem(self, mensagem):
        if mensagem:
            # Desenha um retângulo de fundo para a mensagem
            pygame.draw.rect(self.tela, (10, 10, 10), (LARGURA//2 - 300, 500, 600, 40))
            pygame.draw.rect(self.tela, AZUL_HUD, (LARGURA//2 - 300, 500, 600, 40), 1)
            
            # Renderiza o texto
            txt = self.fonte_pequena.render(mensagem, True, VERDE_SISTEMA)
            self.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, 510))
        # ==================== BRIND DO VÉU - VISUAL PREMIUM ====================
    def desenhar_tela_brind(self, screen, hangar, brind_sys):
        """Tela do Brind do Véu - Visual brilhoso e misterioso"""
        screen.fill(PRETO_ESPACO)

        # Overlay roxo escuro para ambiência
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((40, 0, 60, 85))
        screen.blit(overlay, (0, 0))

        # Título com efeito Glow (Utilizando fonte_titulo)
        titulo_glow = self.fonte_titulo.render("BRIND DO VÉU", True, (190, 100, 255))
        titulo = self.fonte_titulo.render("BRIND DO VÉU", True, (255, 215, 0))
        
        screen.blit(titulo_glow, (LARGURA//2 - titulo_glow.get_width()//2 + 4, 58))
        screen.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 55))

        subt = self.fonte_pequena.render("Sacrifício Genético • O Véu aceita apenas o forte", True, (170, 170, 255))
        screen.blit(subt, (LARGURA//2 - subt.get_width()//2, 120))

        # === ALVO ===
        if 0 <= brind_sys.alvo_index < len(hangar):
            # Certifique-se de que o método _desenhar_monstro_brind exista no seu HUD
            self._desenhar_monstro_brind(screen, hangar[brind_sys.alvo_index], 140, 190, "ALVO", (80, 255, 255))

        # === SACRIFÍCIO ===
        if 0 <= brind_sys.sacrif_index < len(hangar):
            self._desenhar_monstro_brind(screen, hangar[brind_sys.sacrif_index], 580, 190, "SACRIFÍCIO", (255, 90, 110))

        # Seta dourada de fluxo no meio
        pygame.draw.line(screen, (255, 215, 0), (390, 275), (510, 275), 6)
        pygame.draw.polygon(screen, (255, 215, 0), [(500, 265), (525, 275), (500, 285)])

        # Atributo selecionado (Feedback Central)
        if brind_sys.atributo_escolhido:
            attr_nome = brind_sys.atributo_escolhido.upper()
            cores_attr = {"hp": (255, 70, 70), "atk": (255, 150, 40), "def": (70, 160, 255), "agi": (80, 255, 110)}
            cor_destaque = cores_attr.get(brind_sys.atributo_escolhido, (255, 255, 255))
            
            attr_surf = self.fonte_menu.render(f"SINTONIA: {attr_nome}", True, cor_destaque)
            screen.blit(attr_surf, (LARGURA//2 - attr_surf.get_width()//2, 370))

        # Níveis de Risco (Botões Selecionáveis)
        niveis_info = [
            ("Leve", (100, 255, 130)),
            ("Médio", (255, 215, 70)),
            ("Abismo", (255, 60, 80))
        ]

        for i, (nivel, cor_base) in enumerate(niveis_info):
            # Destaque visual se for o nível selecionado
            selecionado = (nivel == brind_sys.nivel_risco)
            cor_box = (255, 255, 255) if selecionado else cor_base
            rect = pygame.Rect(170 + i*185, 460, 165, 58)
            
            pygame.draw.rect(screen, cor_box, rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 4 if selecionado else 2, border_radius=12)

            txt = self.fonte_pequena.render(nivel.upper(), True, PRETO_ESPACO)
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

        # Painel de Informação de Probabilidades
        info = ""
        if brind_sys.nivel_risco == "Leve":
            info = "75% sucesso • +0.07~0.11 • Perde só o sacrifício"
        elif brind_sys.nivel_risco == "Médio":
            info = "48% sucesso • +0.13~0.19 • 35% risco perder Alvo"
        else: # Abismo
            info = "22% sucesso • +0.24~0.32 • RISCO TOTAL: PERDE OS DOIS"

        info_surf = self.fonte_pequena.render(info, True, (210, 210, 255))
        screen.blit(info_surf, (LARGURA//2 - info_surf.get_width()//2, 545))

        # Comandos de Interface
        inst1 = self.fonte_pequena.render("ESPAÇO = Confirmar Brind   |   M = Voltar ao Hangar", True, (160, 160, 160))
        screen.blit(inst1, (LARGURA//2 - inst1.get_width()//2, ALTURA - 85))

        inst2 = self.fonte_pequena.render("C / V = Mudar Risco   |   Z / X = Mudar Atributo", True, (160, 160, 160))
        screen.blit(inst2, (LARGURA//2 - inst2.get_width()//2, ALTURA - 60))

    def _desenhar_monstro_brind(self, screen, monstro, x, y, titulo, cor):
        """Desenha monstro estilizado na tela do Brind"""
        nome = monstro.get("nome", "Desconhecido")
        tribo = monstro.get("tribo", "")

        screen.blit(self.fonte_pequena.render(titulo, True, cor), (x + 40, y - 45))
        screen.blit(self.fonte_menu.render(nome, True, (255, 255, 255)), (x + 40, y))
        screen.blit(self.fonte_pequena.render(tribo, True, (170, 190, 255)), (x + 40, y + 38))

        # DNA do atributo (se escolhido)
        if brind_sys := getattr(self, 'brind_sys', None):
            if brind_sys.atributo_escolhido:
                attr = brind_sys.atributo_escolhido
                val = monstro["dna"].get(attr, 1.0)
                screen.blit(self.fonte_pequena.render(f"{attr.upper()}: {val:.2f}", True, (255, 215, 0)), 
                          (x + 40, y + 72))        
            
    def desenhar_batalha(self, p_ativo, inimigo_atual, contador_turnos, evento_ativo, imagens_monstros, mensagem, torneio_ativo, lutas_concluidas, time_inimigo):
        cor_ini = tribos_info[inimigo_atual["tribo"]]["cor"]
        
        # --- RENDERIZAÇÃO DE STATUS AMBIENTE (TOP RIGHT) ---
        txt_evento = self.fonte_pequena.render(f"TURNO: {contador_turnos} | AMBIENTE: {evento_ativo}", True, OURO_STATUS)
        self.tela.blit(txt_evento, (LARGURA - txt_evento.get_width() - 20, 10))

        # --- DESENHO DOS MONSTROS (POSICIONAMENTO ESTRATÉGICO) ---
        # Jogador: Mantido na esquerda inferior
        img_p = imagens_monstros.get(p_ativo["nome"])
        if img_p: self.tela.blit(img_p, (80, 280))
        
        # Inimigo: Jogado para baixo para não bater no texto/barra
        nome_img_base = inimigo_atual["nome"].split(" (")[0]
        img_inimigo_bruta = imagens_monstros.get(nome_img_base)
        if img_inimigo_bruta:
            img_f = pygame.transform.flip(img_inimigo_bruta, True, False)
            self.tela.blit(img_f, (580, 150)) # Desci para 150 para liberar espaço no topo

        # --- STATUS DO JOGADOR (ESQUERDA) ---
        # Nome e Level
        txt_p = self.fonte_menu.render(f"{p_ativo['nome']} LV.{p_ativo['lvl']}", True, VERDE_SISTEMA)
        self.tela.blit(txt_p, (100, 240))
        
        # Barra de HP (Com fundo escuro para profundidade)
        pygame.draw.rect(self.tela, (40, 0, 0), (100, 275, 200, 12)) 
        largura_hp_p = (max(0, p_ativo["hp"]) / p_ativo["hp_max"]) * 200
        pygame.draw.rect(self.tela, VERDE_SISTEMA, (100, 275, min(200, largura_hp_p), 12))
        
        # XP e Energia (Mais finas embaixo do HP)
        largura_xp = (p_ativo["xp"] / p_ativo["xp_max"]) * 200
        pygame.draw.rect(self.tela, (40, 40, 40), (100, 292, 200, 4))
        pygame.draw.rect(self.tela, CIANO_XP, (100, 292, min(200, largura_xp), 4))
        
        largura_en = (p_ativo["en"] / p_ativo["en_max"]) * 200
        pygame.draw.rect(self.tela, (20, 20, 60), (100, 300, 200, 4))
        pygame.draw.rect(self.tela, AZUL_ENERGIA, (100, 300, min(200, largura_en), 4))

        # --- STATUS DO INIMIGO (DIREITA - ESPELHADO) ---
        # Nome e LV alinhados pela direita
        txt_i = self.fonte_menu.render(f"LV.{inimigo_atual['lvl']} {inimigo_atual['nome']}", True, cor_ini)
        # Calcula a posição X para o texto não sair da tela
        x_ini = LARGURA - txt_i.get_width() - 100
        self.tela.blit(txt_i, (x_ini, 50))
        
        # Barra de HP do Inimigo (Vermelha com borda da cor da tribo)
        pygame.draw.rect(self.tela, (40, 0, 0), (x_ini, 85, 200, 15))
        if inimigo_atual["hp"] > 0:
            largura_hp_e = (inimigo_atual["hp"] / inimigo_atual["hp_max"]) * 200
            pygame.draw.rect(self.tela, VERMELHO_ALERTA, (x_ini, 85, min(200, largura_hp_e), 15))
        pygame.draw.rect(self.tela, cor_ini, (x_ini, 85, 200, 15), 2) # Borda estilizada

        # --- HUD INFERIOR (CAIXA DE MENSAGENS E COMANDOS) ---
        # Desenha um fundo sólido para a caixa de comandos ficar legível
        pygame.draw.rect(self.tela, (5, 5, 20), (50, 500, 800, 85))
        pygame.draw.rect(self.tela, AZUL_HUD, (50, 500, 800, 85), 1, border_radius=10)
        
        # Mensagem do Sistema (Aparece em destaque)
        self.tela.blit(self.fonte_pequena.render(f">>> {mensagem}", True, VERDE_SISTEMA), (75, 515))
        
        # Barra de Comandos
        txt_menu = "[A] ATAQUE   [S] ESPECIAL   [T] TROCA   [U] UPLOAD   [R] SCAN   [M] NAVE"
        self.tela.blit(self.fonte_pequena.render(txt_menu, True, (255, 255, 255)), (75, 550))