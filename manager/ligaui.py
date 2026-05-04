# liga_ui.py
# Interface Visual da Liga V.O.I.D. para Pygame

import pygame
from typing import Optional, List, Tuple
from dataclasses import dataclass

from configuration.config import *
from manager.liga import LigaManager, Divisao, LEVEL_CAPS
from manager.ligabattle import BatalhaLiga4x4


class LigaUI:
    def __init__(self, tela: pygame.Surface, fonte_titulo, fonte_menu, fonte_pequena):
        self.tela = tela
        self.fonte_titulo = fonte_titulo
        self.fonte_menu = fonte_menu
        self.fonte_pequena = fonte_pequena
        
        self.liga: Optional[LigaManager] = None
        self.batalha_atual: Optional[BatalhaLiga4x4] = None
        
        # Estados da UI da Liga
        self.estado_liga = "MENU_LIGA"  # MENU_LIGA, TABELA, ARTILHARIA, CALENDARIO, BATALHA, RESULTADO
        self.divisao_selecionada = Divisao.SERIE_D
        self.opcao_menu = 0
        self.opcoes_menu = [
            "📊 TABELA DE CLASSIFICAÇÃO",
            "⚽ PRÓXIMA PARTIDA",
            "🏆 ARTILHARIA",
            "📅 CALENDÁRIO",
            "💾 VOLTAR AO MENU"
        ]
        
        # Cores por divisão
        self.cores_divisao = {
            Divisao.SERIE_A: (255, 215, 0),      # Ouro
            Divisao.SERIE_B: (192, 192, 192),    # Prata
            Divisao.SERIE_C: (205, 127, 50),     # Bronze
            Divisao.SERIE_D: (100, 200, 255)     # Azul claro
        }
    
    def inicializar(self, time_jogador: List[dict], nome_jogador: str, 
                    divisao_inicial: Divisao = Divisao.SERIE_D):
        """Inicializa a liga com o time do jogador"""
        self.liga = LigaManager()
        self.liga.inicializar_liga(time_jogador, nome_jogador, divisao_inicial)
        self.divisao_selecionada = divisao_inicial
    
    def processar_input(self, evento: pygame.event.Event) -> Optional[str]:
        if self.estado_liga == "MENU_LIGA":
            # ... (seu código atual do menu da liga) ...
            pass
            
        # --- AQUI É A ARENA 4X4 (COMPLETAMENTE ISOLADA DO MAIN) ---
        elif self.estado_liga == "BATALHA":
            if evento.type == pygame.KEYDOWN:
                # [A] Ataque Base / [S] Ataque Especial
                if evento.key == pygame.K_a:
                    if self.batalha_atual and getattr(self.batalha_atual, 'finalizada', False) == False:
                        self.batalha_atual.executar_turno_jogador("base")
                
                elif evento.key == pygame.K_s:
                    if self.batalha_atual and getattr(self.batalha_atual, 'finalizada', False) == False:
                        self.batalha_atual.executar_turno_jogador("especial")
                
                # Checa se o seu "Deus" aniquilou a equipe inimiga após o golpe
                if self.batalha_atual and getattr(self.batalha_atual, 'finalizada', False):
                    self.estado_liga = "RESULTADO_RODADA"
        
        # --- MENU PRINCIPAL DA LIGA ---
        if self.estado_liga == "MENU_LIGA":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.opcao_menu = (self.opcao_menu - 1) % len(self.opcoes_menu)
                elif evento.key == pygame.K_DOWN:
                    self.opcao_menu = (self.opcao_menu + 1) % len(self.opcoes_menu)
                elif evento.key == pygame.K_RETURN:
                    if self.opcao_menu == 0:
                        self.estado_liga = "TABELA"
                    
                    elif self.opcao_menu == 1:
                        # O seu método prepara a batalha e muda o estado interno para "BATALHA"
                        self._preparar_partida()
                        
                        # === O SEGREDO ESTÁ AQUI ===
                        # Se a partida foi criada com sucesso, avisamos o main.py!
                        if self.estado_liga == "BATALHA":
                            return "INICIAR_PARTIDA" 
                    
                    elif self.opcao_menu == 2:
                        self.estado_liga = "ARTILHARIA"
                    elif self.opcao_menu == 3:
                        self.estado_liga = "CALENDARIO"
                    elif self.opcao_menu == 4:
                        return "MENU"  # Volta ao menu principal
                
                elif evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                    return "MENU"
        
        # --- TABELA ---
        elif self.estado_liga == "TABELA":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    # Troca divisão
                    divs = list(Divisao)
                    idx = divs.index(self.divisao_selecionada)
                    if evento.key == pygame.K_LEFT:
                        idx = (idx - 1) % len(divs)
                    else:
                        idx = (idx + 1) % len(divs)
                    self.divisao_selecionada = divs[idx]
                elif evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                    self.estado_liga = "MENU_LIGA"
        
        # --- ARTILHARIA ---
        elif self.estado_liga == "ARTILHARIA":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                    self.estado_liga = "MENU_LIGA"
        
        # --- CALENDÁRIO ---
        elif self.estado_liga == "CALENDARIO":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                    self.estado_liga = "MENU_LIGA"
        
        # --- BATALHA 4x4 ---
        elif self.estado_liga == "BATALHA":
            if evento.type == pygame.KEYDOWN:
                if self.batalha_atual and not self.batalha_atual.batalha_encerrada:
                    if evento.key == pygame.K_a:
                        self.batalha_atual.executar_turno_jogador("base")
                    elif evento.key == pygame.K_s:
                        self.batalha_atual.executar_turno_jogador("especial")
                else:
                    # Batalha encerrada, avançar
                    if evento.key == pygame.K_RETURN:
                        self._processar_resultado_batalha()
                        self.estado_liga = "RESULTADO_RODADA"
        
        # --- RESULTADO DA RODADA ---
        elif self.estado_liga == "RESULTADO_RODADA":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_m:
                    self.estado_liga = "MENU_LIGA"
        
        return 
    
    def _preparar_partida(self):
        """Prepara a próxima partida do jogador"""
        partida = self.liga.get_proxima_partida_jogador()
        if not partida:
            self.estado_liga = "MENU_LIGA"
            return
        
        time_j, time_a = partida
        
        # Cria batalha 4x4 - Argumentos ajustados para bater com o __init__ do ligabattle.py
        self.batalha_atual = BatalhaLiga4x4(
            time_jogador=time_j.monstros,
            time_adversario=time_a.monstros,
            nome_j=time_j.nome,  # Nome correto do argumento no motor
            nome_a=time_a.nome   # Nome correto do argumento no motor
        )
        
        self.estado_liga = "BATALHA"
    
    def _processar_resultado_batalha(self):
        """Processa resultado após batalha manual"""
        if not self.batalha_atual or not self.liga:
            return
        
        venceu, abates_j, abates_a = self.batalha_atual.get_resultado_final()
        
        partida = self.liga.get_proxima_partida_jogador()
        if partida:
            time_j, time_a = partida
            self.liga.processar_resultado_jogador(time_j, time_a, venceu, abates_j, abates_a)
            
            # Simula o restante da rodada
            self.liga.simular_rodada_completa()
    
    def renderizar(self):
        """Renderiza a tela atual da Liga"""
        if not self.liga:
            return
        
        self.tela.fill(PRETO_ESPACO)
        
        # Desenha grid de fundo
        for i in range(0, LARGURA, 50):
            pygame.draw.line(self.tela, (15, 25, 45), (i, 0), (i, ALTURA))
        for i in range(0, ALTURA, 50):
            pygame.draw.line(self.tela, (15, 25, 45), (0, i), (LARGURA, i))
        
        if self.estado_liga == "MENU_LIGA":
            self._render_menu_liga()
        elif self.estado_liga == "TABELA":
            self._render_tabela()
        elif self.estado_liga == "ARTILHARIA":
            self._render_artilharia()
        elif self.estado_liga == "CALENDARIO":
            self._render_calendario()
        elif self.estado_liga == "BATALHA":
            self._render_batalha()
        elif self.estado_liga == "RESULTADO_RODADA":
            self._render_resultado_rodada()
    
    def _render_menu_liga(self):
        """Renderiza menu principal da Liga"""
        # Título
        titulo = self.fonte_titulo.render("🏆 LIGA V.O.I.D.", True, VIOLETA_SCANNER)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))
        
        # Info da rodada
        info = self.fonte_pequena.render(
            f"Rodada {self.liga.rodada_atual + 1}/38 | Divisão: {self.liga.time_jogador_divisao.value}",
            True, OURO_STATUS
        )
        self.tela.blit(info, (LARGURA//2 - info.get_width()//2, 140))
        
        # Opções
        for i, opcao in enumerate(self.opcoes_menu):
            cor = VERDE_SISTEMA if i == self.opcao_menu else AZUL_HUD
            txt = self.fonte_menu.render(opcao, True, cor)
            self.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, 220 + i * 60))
        
        # Instruções
        inst = self.fonte_pequena.render("[↑↓] NAVEGAR  [ENTER] SELECIONAR  [M] VOLTAR", True, (150, 150, 150))
        self.tela.blit(inst, (LARGURA//2 - inst.get_width()//2, 550))
    
    def _render_tabela(self):
        """Renderiza tabela de classificação"""
        div = self.divisao_selecionada
        cor_div = self.cores_divisao[div]
        
        # Título
        titulo = self.fonte_titulo.render(f"📊 {div.value}", True, cor_div)
        self.tela.blit(titulo, (50, 30))
        
        # Level cap
        cap = self.fonte_pequena.render(f"Level Cap: {LEVEL_CAPS[div]}", True, CIANO_XP)
        self.tela.blit(cap, (50, 75))
        
        # Cabeçalho
        headers = ["POS", "TIME", "P", "J", "V", "D", "GF", "GS", "SALDO"]
        x_pos = [50, 100, 400, 450, 490, 530, 570, 620, 670]
        
        for h, x in zip(headers, x_pos):
            txt = self.fonte_pequena.render(h, True, AZUL_HUD)
            self.tela.blit(txt, (x, 110))
        
        # Times
        classificacao = self.liga.get_classificacao(div)
        
        for i, time in enumerate(classificacao):
            y = 135 + i * 22
            
            # Destaca time do jogador
            eh_jogador = (time.id == self.liga.time_jogador_id)
            cor = VERDE_SISTEMA if eh_jogador else (200, 200, 200)
            
            # Destaque top 4 (zona de promoção) e bottom 4 (rebaixamento)
            if not eh_jogador:
                if i < 4:
                    cor = (100, 255, 100)  # Verde claro
                elif i >= 16:
                    cor = (255, 100, 100)  # Vermelho claro
            
            dados = [
                f"{time.posicao:2d}",
                time.nome[:25],
                f"{time.pontos:2d}",
                f"{time.jogos:2d}",
                f"{time.vitorias:2d}",
                f"{time.derrotas:2d}",
                f"{time.gols_feitos:2d}",
                f"{time.gols_sofridos:2d}",
                f"{time.saldo:+3d}"
            ]
            
            for d, x in zip(dados, x_pos):
                txt = self.fonte_pequena.render(d, True, cor)
                self.tela.blit(txt, (x, y))
        
        # Instruções
        inst = self.fonte_pequena.render("[←→] TROCAR DIVISÃO  [M] VOLTAR", True, (150, 150, 150))
        self.tela.blit(inst, (LARGURA//2 - inst.get_width()//2, 570))
    
    def _render_artilharia(self):
        """Renderiza top artilheiros"""
        titulo = self.fonte_titulo.render("🏆 ARTILHARIA DA LIGA", True, OURO_STATUS)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))
        
        top = self.liga.get_top_artilheiros(10)
        
        # Cabeçalho
        headers = ["POS", "MONSTRO", "TIME", "TRIBO", "ABATES", "JOGOS", "MÉDIA"]
        x_pos = [80, 130, 350, 520, 620, 690, 760]
        
        for h, x in zip(headers, x_pos):
            txt = self.fonte_pequena.render(h, True, AZUL_HUD)
            self.tela.blit(txt, (x, 120))
        
        # Medalhas
        medalhas = ["🥇", "🥈", "🥉"]
        
        for i, art in enumerate(top):
            y = 150 + i * 35
            
            # Destaque top 3
            if i < 3:
                cor = [OURO_STATUS, (192, 192, 192), (205, 127, 50)][i]
                prefixo = medalhas[i]
            else:
                cor = (200, 200, 200)
                prefixo = f"{i+1:2d}."
            
            # Destaca se for do jogador
            if art.time_nome == f"[{self.liga.nome_operador}] SQUAD":
                cor = VERDE_SISTEMA
            
            dados = [
                prefixo,
                art.monstro_nome[:18],
                art.time_nome[:20],
                art.tribo[:10],
                f"{art.abates}",
                f"{art.jogos}",
                f"{art.media:.2f}"
            ]
            
            for d, x in zip(dados, x_pos):
                txt = self.fonte_pequena.render(str(d), True, cor)
                self.tela.blit(txt, (x, y))
        
        # Prêmio final
        if self.liga.rodada_atual >= 38:
            if top:
                campeao = top[0]
                msg = f"🏆 EXECUTOR DA TEMPORADA: {campeao.monstro_nome} ({campeao.abates} abates)!"
                txt = self.fonte_menu.render(msg, True, OURO_STATUS)
                self.tela.blit(txt, (LARGURA//2 - txt.get_width()//2, 520))
        
        inst = self.fonte_pequena.render("[M] VOLTAR", True, (150, 150, 150))
        self.tela.blit(inst, (LARGURA//2 - inst.get_width()//2, 570))
    
    def _render_calendario(self):
        """Renderiza calendário de rodadas"""
        titulo = self.fonte_titulo.render("📅 CALENDÁRIO", True, AZUL_HUD)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))
        
        # Mostra próximas 5 rodadas
        rodada_atual = self.liga.rodada_atual
        
        for offset in range(5):
            rodada = rodada_atual + offset + 1
            if rodada > 38:
                break
            
            y = 130 + offset * 80
            
            # Destaca rodada atual
            cor = VERDE_SISTEMA if offset == 0 else (200, 200, 200)
            txt_rodada = self.fonte_menu.render(f"RODADA {rodada}", True, cor)
            self.tela.blit(txt_rodada, (80, y))
            
            # Mostra confronto do jogador nesta rodada
            jogos = self.liga.calendario.get(rodada, [])
            for t1_idx, t2_idx, div in jogos:
                times = self.liga.divisoes[div]
                t1, t2 = times[t1_idx], times[t2_idx]
                
                if t1.id == self.liga.time_jogador_id or t2.id == self.liga.time_jogador_id:
                    adversario = t2 if t1.id == self.liga.time_jogador_id else t1
                    txt_adv = self.fonte_pequena.render(f"vs {adversario.nome} ({div.value})", True, cor)
                    self.tela.blit(txt_adv, (80, y + 30))
                    break
        
        inst = self.fonte_pequena.render("[M] VOLTAR", True, (150, 150, 150))
        self.tela.blit(inst, (LARGURA//2 - inst.get_width()//2, 570))
    
    def _render_batalha(self):
        """Renderiza batalha 4x4 em tempo real"""
        if not self.batalha_atual:
            return
        
        estado = self.batalha_atual.get_status()
        
        jogador = estado["jogador"]
        adversario = estado["adversario"]
        
        # Título
        titulo = self.fonte_titulo.render("⚔️ BATALHA 4x4", True, VERMELHO_ALERTA)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 20))
        
        # Info do turno
        turno_txt = self.fonte_pequena.render(
            f"Turno {estado['turno']}/{estado['max_turnos']}", True, OURO_STATUS
        )
        self.tela.blit(turno_txt, (LARGURA//2 - turno_txt.get_width()//2, 70))
        
        # --- TIME JOGADOR (ESQUERDA) ---
        self._render_time_batalha(estado['jogador'], 50, 120, True)
        
        # VS
        vs = self.fonte_titulo.render("VS", True, VERMELHO_ALERTA)
        self.tela.blit(vs, (LARGURA//2 - vs.get_width()//2, 250))
        
        # --- TIME ADVERSÁRIO (DIREITA) ---
        self._render_time_batalha(estado['adversario'], 550, 120, False)
        
        # Log de batalha
        log = estado['ultimo_log']
        if log:
            # Quebra log em linhas se for muito longo
            words = log.split()
            lines = []
            current_line = ""
            for word in words:
                test = current_line + " " + word if current_line else word
                if len(test) < 80:
                    current_line = test
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            y_log = 420
            for line in lines[:3]:  # Max 3 linhas
                txt = self.fonte_pequena.render(line, True, VERDE_SISTEMA)
                self.tela.blit(txt, (50, y_log))
                y_log += 20
        
        # Controles
        if not estado['encerrada']:
            ctrl = "[A] ATAQUE  [S] ESPECIAL  [M] DESISTIR"
        else:
            ctrl = f"🏆 {estado['vencedor'].upper()} VENCEU! [ENTER] CONTINUAR"
        
        txt_ctrl = self.fonte_pequena.render(ctrl, True, AZUL_HUD)
        self.tela.blit(txt_ctrl, (LARGURA//2 - txt_ctrl.get_width()//2, 500))
        
        # Abates
        abates_txt = self.fonte_pequena.render(
            f"Abates: {estado['jogador']['abates']} x {estado['adversario']['abates']}",
            True, CIANO_XP
        )
        self.tela.blit(abates_txt, (LARGURA//2 - abates_txt.get_width()//2, 530))
    
    def _render_time_batalha(self, dados_time: dict, x: int, y: int, eh_jogador: bool):
        """Renderiza os slots de esquadrão e o monstro ativo na arena"""
        cor_time = VERDE_SISTEMA if eh_jogador else VERMELHO_ALERTA
        
        # Identificação do Esquadrão
        nome_surf = self.fonte_menu.render(dados_time['nome_time'][:20], True, cor_time)
        self.tela.blit(nome_surf, (x, y))
        
        # Iteração pelos 4 slots do esquadrão
        y_monstro_base = y + 50
        for i in range(4):
            pos_y = y_monstro_base + i * 75  # Espaçamento otimizado para evitar sobreposição
            
            # Status Operacional
            vivo = i in dados_time['time_vivo']
            morto = i in dados_time['time_morto']
            
            if vivo:
                cor = VERDE_SISTEMA
                status = "●"
            elif morto:
                cor = (100, 100, 100)
                status = "✖"
            else:
                cor = (60, 60, 60)
                status = "○"
            
            # Verificação de Unidade Ativa em Campo
            ativo = dados_time['monstro_ativo']
            eh_ativo = ativo and ativo['posicao'] == i
            
            if eh_ativo:
                # Frame de destaque para a unidade conectada
                pygame.draw.rect(self.tela, cor, (x - 10, pos_y - 5, 320, 65), 1)
                status = "▶"
            
            # Identificador da Unidade
            txt_id = self.fonte_pequena.render(f"{status} UNIDADE {i+1}", True, cor)
            self.tela.blit(txt_id, (x, pos_y))
            
            # Interface de Telemetria (Stats) para unidade ativa
            if eh_ativo:
                hp_pct = ativo['hp'] / max(ativo['hp_max'], 1)
                en_pct = ativo['en'] / max(ativo['en_max'], 1)
                
                # Monitor de Integridade (HP)
                pygame.draw.rect(self.tela, (40, 0, 0), (x + 30, pos_y + 22, 120, 10))
                cor_hp = VERDE_SISTEMA if hp_pct > 0.3 else VERMELHO_ALERTA
                pygame.draw.rect(self.tela, cor_hp, (x + 30, pos_y + 22, int(120 * hp_pct), 10))
                
                # Monitor de Carga (Energia)
                pygame.draw.rect(self.tela, (10, 10, 40), (x + 30, pos_y + 36, 120, 6))
                pygame.draw.rect(self.tela, CIANO_XP, (x + 30, pos_y + 36, int(120 * en_pct), 6))
                
                # Nome e Dados de Vida
                txt_stats = self.fonte_pequena.render(
                    f"{ativo['nome'][:12]} ({ativo['hp']}/{ativo['hp_max']})", True, cor
                )
                self.tela.blit(txt_stats, (x + 160, pos_y + 22))

    def _render_resultado_rodada(self):
        """Renderiza os dados consolidados e a tabela após o combate"""
        self.tela.fill((5, 5, 20)) # Fundo de análise tática
        titulo = self.fonte_titulo.render("📊 RESULTADOS DA RODADA", True, VIOLETA_SCANNER)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))
        
        if self.batalha_atual:
            venceu, abates_j, abates_a = self.batalha_atual.get_resultado_final()
            res_msg = "VITÓRIA!" if venceu else "DERROTA!"
            cor_res = VERDE_SISTEMA if venceu else VERMELHO_ALERTA
            
            txt_res = self.fonte_titulo.render(res_msg, True, cor_res)
            self.tela.blit(txt_res, (LARGURA//2 - txt_res.get_width()//2, 120))
            
            placar_txt = self.fonte_menu.render(f"{abates_j} x {abates_a}", True, CIANO_XP)
            self.tela.blit(placar_txt, (LARGURA//2 - placar_txt.get_width()//2, 170))
        
        # Log de outros confrontos da liga
        if self.liga:
            y_log = 230
            self.tela.blit(self.fonte_menu.render("OUTROS JOGOS:", True, AZUL_HUD), (50, y_log))
            
            for i, res_log in enumerate(self.liga.resultados_rodada[:8]):
                txt_log = self.fonte_pequena.render(res_log, True, (180, 180, 180))
                self.tela.blit(txt_log, (50, y_log + 40 + i * 25))

            # Status de Classificação do Operador
            classificacao = self.liga.get_classificacao(self.liga.time_jogador_divisao)
            dados_op = next((t for t in classificacao if t.id == self.liga.time_jogador_id), None)
            
            if dados_op:
                txt_pos = self.fonte_pequena.render(
                    f"POSIÇÃO ATUAL: {dados_op.posicao}º | PONTOS: {dados_op.pontos}",
                    True, OURO_STATUS
                )
                self.tela.blit(txt_pos, (LARGURA//2 - txt_pos.get_width()//2, 520))
        
        inst_txt = self.fonte_pequena.render("[ENTER] CONTINUAR PROTOCOLO", True, VERDE_SISTEMA)
        self.tela.blit(inst_txt, (LARGURA//2 - inst_txt.get_width()//2, 570))