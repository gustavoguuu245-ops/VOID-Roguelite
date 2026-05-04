import pygame
import random
import sys
import os

from configuration.config import *
from configuration.database import *
from configuration.hud import HUD
import configuration.engine as engine
import systems.eventos as eventos_sys
from systems.hangar import HangarSystem
from systems.loja import ShopSystem
from saves.save import SaveSystem
from manager.liga import LigaManager
from manager.ligaui import LigaUI
from systems.brind import BrindSystem

# Inicialização do Pygame
pygame.init()

# ==================== CONFIGURAÇÃO VISUAL ====================
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("V.O.I.D. Interface - Estação Orbital")

fontes = {
    'titulo': pygame.font.SysFont("Courier", 45, bold=True),
    'menu': pygame.font.SysFont("Courier", 26),
    'pequena': pygame.font.SysFont("Courier", 16)
}

# ==================== INICIALIZAÇÃO DE MÓDULOS ====================
interface_hud = HUD(tela, fontes)
hangar_sys = HangarSystem(tela, fontes)
loja_sys = ShopSystem(tela, fontes)
save_sys = SaveSystem(tela, fontes)

# Motor da Liga
liga_manager = LigaManager()
liga_ui = LigaUI(tela, fontes['titulo'], fontes['menu'], fontes['pequena'])
liga_ui.liga = liga_manager
# Áreas de clique para os botões do topo (conforme seu hud.py)
RECT_ARQUIVAR = pygame.Rect(LARGURA - 300, 20, 120, 30)
RECT_RECUPERAR = pygame.Rect(LARGURA - 160, 20, 120, 30)

# ==================== VARIÁVEIS GLOBAIS ====================
itens_menu = ["[ 1 ] EXPLORAR (SCAN)", "[ 2 ] HANGAR", "[ 3 ] BRIND", "[ 4 ] LOJA", "[ 5 ] SAIR"]
itens_sub_menu = ["[ 1 ] BATALHAR", "[ 2 ] MEU HANGAR", "[ VOLTAR ]"]
modo_save = "SALVAR"
slot_sel = None
sub_menu = False
opcao_selecionada = 0
estado = "LOGIN"
nome_operador = ""
creditos = 100
data_cores = 2
slots_maximos = 3
signal_boosters = 0
evento_ativo = "Estabilidade"
contador_turnos = 0
mensagem = "CONEXÃO ESTABELECIDA. AGUARDANDO OPERADOR..."
brind_sys = BrindSystem()
hangar = []
time_jogador = [] 
p_ativo = None
inimigo_atual = None
monstro_ativo_index = 0

# --- Carregamento de Imagens ---
imagens_monstros = {}
for nome, dados in monstros_db.items():
    try:
        img_load = pygame.image.load(dados["img"]).convert_alpha()
        imagens_monstros[nome] = pygame.transform.scale(img_load, (200, 200))
    except:
        imagens_monstros[nome] = None

# Função auxiliar para resetar ambiente
def preparar_nova_batalha():
    global contador_turnos, evento_ativo
    contador_turnos = 0
    evento_ativo = None # Limpa o clima para a nova luta
    eventos_possiveis = ["Tempestade Solar", "Nevasca", "Eclipse Vazio", "Recuperação de Floresta", "Pulso de Blindagem", "Sussurros do Abismo"]
    evento_ativo = random.choice(eventos_possiveis)

# ==================== LOOP PRINCIPAL ====================
rodando = True
while rodando:
    tela.fill(PRETO_ESPACO)
    mouse_pos = pygame.mouse.get_pos()
    
    # Grade de Fundo
    for i in range(0, LARGURA, 50): pygame.draw.line(tela, (15, 25, 45), (i, 0), (i, ALTURA))
    for i in range(0, ALTURA, 50): pygame.draw.line(tela, (15, 25, 45), (0, i), (LARGURA, i))

    eventos_pygame = pygame.event.get()
    for evento in eventos_pygame:
        if evento.type == pygame.QUIT:
            rodando = False

        # --- LÓGICA DE INPUT POR ESTADO ---
        if estado == "LOGIN":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nome_operador) > 2:
                    estado = "TRIBO_INICIAL"
                elif evento.key == pygame.K_BACKSPACE: nome_operador = nome_operador[:-1]
                else:
                    if len(nome_operador) < 10 and evento.unicode.isalnum():
                        nome_operador += evento.unicode.upper()

        elif estado == "TRIBO_INICIAL":
            lista_tribos = list(tribos_info.keys())
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: opcao_selecionada = (opcao_selecionada - 1) % len(lista_tribos)
                if evento.key == pygame.K_DOWN: opcao_selecionada = (opcao_selecionada + 1) % len(lista_tribos)
                if evento.key == pygame.K_RETURN:
                    tribo_esc = lista_tribos[opcao_selecionada]
                    cands = [m for m, d in monstros_db.items() if d.get("tribo") == tribo_esc]
                    if cands:
                        novo = engine.gerar_instancia_monster(random.choice(cands), monstros_db)
                        hangar.append(novo)
                        p_ativo = hangar[0]
                        estado = "MENU"

        elif estado == "MENU":
            # --- TRATAMENTO DE TECLADO ---
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: 
                    opcao_selecionada = (opcao_selecionada - 1) % len(itens_menu)
                elif evento.key == pygame.K_DOWN: 
                    opcao_selecionada = (opcao_selecionada + 1) % len(itens_menu)
                
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0: # SCAN
                        inimigo_atual, mensagem = engine.sortear_inimigo(hangar, monstro_ativo_index, monstros_db)
                        preparar_nova_batalha()
                        estado = "BATALHA"
                    elif opcao_selecionada == 1: 
                        estado = "HANGAR"
                    elif opcao_selecionada == 2: # BRINDE DO VÉU (Substituindo a Liga)
                # Estrutura pronta para o futuro sistema de fusão
                        estado = "BRIND"
                        mensagem = "ACESSO AO VÉU ESTABELECIDO. O SACRIFÍCIO REQUER DOIS GENOMAS."
                    elif opcao_selecionada == 3: 
                        estado = "LOJA"
                    elif opcao_selecionada == 4: # SAIR (ajuste o índice se necessário)
                        rodando = False

            # --- TRATAMENTO DE MOUSE (PARA OS BOTÕES DO TOPO) ---
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clique com o botão esquerdo
                    mouse_pos = evento.pos
                    
                    # Clicou em [ ARQUIVAR ]
                    if RECT_ARQUIVAR.collidepoint(mouse_pos):
                        modo_save = "SALVAR"
                        estado = "SAVE_MENU"
                        mensagem = "PROTOCOLO DE ARQUIVAMENTO ACIONADO."
                    
                    # Clicou em [ RECUPERAR ]
                    elif RECT_RECUPERAR.collidepoint(mouse_pos):
                        modo_save = "CARREGAR"
                        estado = "SAVE_MENU"
                        mensagem = "RECUPERAÇÃO DE DADOS INICIADA."

        elif estado == "HANGAR":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP: monstro_ativo_index = (monstro_ativo_index - 1) % len(hangar)
                elif evento.key == pygame.K_DOWN: monstro_ativo_index = (monstro_ativo_index + 1) % len(hangar)
                elif evento.key == pygame.K_SPACE:
                    m = hangar[monstro_ativo_index]
                    
                    # Inverte a tag de seleção (True -> False / False -> True)
                    if m.get('no_time', False):
                        m['no_time'] = False
                        mensagem = f"{m['nome'].upper()} REMOVIDO DA ESCALAÇÃO."
                    else:
                        # Conta quantos monstros já possuem a tag no hangar
                        time_atual = [mon for mon in hangar if mon.get('no_time', False)]
                        
                        if len(time_atual) < 4:
                            m['no_time'] = True
                            mensagem = f"{m['nome'].upper()} ESCALADO PARA A LIGA!"
                        else:
                            mensagem = "LIMITE DE ESCALAÇÃO ATINGIDO (4/4)!"
                    
                    # Sincroniza a lista time_jogador para manter compatibilidade com o HUD do hangar
                    time_jogador = [mon for mon in hangar if mon.get('no_time', False)]

                elif evento.key == pygame.K_RETURN:
                    m_selecionado = hangar[monstro_ativo_index]
                    if m_selecionado["hp"] > 0:
                        p_ativo = m_selecionado
                        preparar_nova_batalha()
                        estado = "BATALHA"
                        mensagem = f"UNIDADE {p_ativo['nome'].upper()} CONECTADA!"
                    else:
                        mensagem = "ERRO: UNIDADE ABATIDA! REPARE NA LOJA."
                elif evento.key == pygame.K_m: estado = "MENU"
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # 1. Antes de checar o clique, atualizamos a lista oficial baseada nas tags
                time_jogador = [mon for mon in hangar if mon.get('no_time', False)]
                
                # 2. Checamos o clique no botão "IR PARA LIGA"
                res = hangar_sys.checar_clique_preparar(evento.pos, time_jogador)
                if res and res[0]:
                    
                    # 3. CURA TOTAL DO TIME ANTES DA LIGA
                    for m in time_jogador:
                        m["hp"] = m["hp_max"]
                        m["en"] = m.get("en_max", 100) # Usa o en_max se existir no dict, senão assume 100
                    
                    # 4. Passamos os dados para o MOTOR DA LIGA primeiro
                    liga_manager.configurar_time_jogador(nome_operador, time_jogador)
                    liga_ui.liga = liga_manager 
                    p_ativo = time_jogador[0] 
                    
                    # Usa APENAS a variável 'estado' (Esqueça estado_global)
                    estado = "MENU_LIGA" 
                    mensagem = f"BEM-VINDO À SÉRIE D, {nome_operador.upper()}!"
        # --- INPUT DA LIGA ---
        elif estado in ["MENU_LIGA", "TABELA", "ARTILHARIA", "CALENDARIO", "LIGA_ARENA", "RESULTADO_RODADA"]:
            res_liga = liga_ui.processar_input(evento)
            
            # Se o jogador clicou em "Próxima Partida"
            if res_liga == "INICIAR_PARTIDA":
                estado = "LIGA_ARENA"  # <--- Aqui usamos apenas 'estado'
                liga_ui.estado_liga = "BATALHA" # Estado interno da UI
            
            # Se a partida da liga acabou
            elif res_liga == "FIM_DA_PARTIDA":
                estado = "RESULTADO_RODADA"
                            
        elif estado == "LOJA":
            if evento.type == pygame.KEYDOWN:
                # Navegação nos Itens da Loja (Cima / Baixo)
                if evento.key == pygame.K_UP: 
                    opcao_selecionada = (opcao_selecionada - 1) % len(loja_sys.itens)
                elif evento.key == pygame.K_DOWN: 
                    opcao_selecionada = (opcao_selecionada + 1) % len(loja_sys.itens)
                
                # --- NOVO: Trocar o Monstro Alvo (Esquerda / Direita) ---
                elif evento.key == pygame.K_LEFT:
                    if hangar: # Garante que o hangar não está vazio
                        monstro_ativo_index = (monstro_ativo_index - 1) % len(hangar)
                        p_ativo = hangar[monstro_ativo_index]
                elif evento.key == pygame.K_RIGHT:
                    if hangar:
                        monstro_ativo_index = (monstro_ativo_index + 1) % len(hangar)
                        p_ativo = hangar[monstro_ativo_index]
                # --------------------------------------------------------

                # Comprar Item
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    res = loja_sys.processar_compra(opcao_selecionada, creditos, p_ativo, data_cores, slots_maximos, signal_boosters)
                    sucesso, creditos, p_ativo, data_cores, slots_maximos, signal_boosters, mensagem = res
                
                # Sair da Loja
                elif evento.key == pygame.K_m or evento.key == pygame.K_ESCAPE:
                    estado = "MENU"
                    opcao_selecionada = 0
                       
        elif estado == "BRIND":
            if evento.type == pygame.KEYDOWN:
                resultado_ritual = brind_sys.processar_input(evento, hangar)

                # Se o ritual foi executado (ESPAÇO)
                if resultado_ritual:
                    mensagem = resultado_ritual.mensagem
                    
                    # Reset após sucesso ou falha grave
                    if resultado_ritual.sucesso or resultado_ritual.perdeu_alvo:
                        brind_sys.reset()

                # Voltar para o Hangar
                if evento.key in (pygame.K_m, pygame.K_ESCAPE):
                    estado = "HANGAR"
                    brind_sys.reset()
                    mensagem = "Retornando ao Hangar..."

        elif estado == "BATALHA":
            if evento.type == pygame.KEYDOWN:
                # [M] Retornar ao Menu Principal
                if evento.key == pygame.K_m: 
                    # Reset básico ao sair para não herdar lixo na próxima luta
                    contador_turnos = 0
                    estado = "MENU"
                
                # [R] Novo Scan / Reiniciar Luta
                elif evento.key == pygame.K_r:
                    inimigo_atual, mensagem = engine.sortear_inimigo(hangar, monstro_ativo_index, monstros_db)
                    # RESETS CRÍTICOS
                    contador_turnos = 0
                    p_ativo["especial_travado"] = False
                    inimigo_atual["especial_travado"] = False
                    evento_ativo = random.choice(["Tempestade Solar", "Nevasca", "Eclipse Vazio", "Recuperação de Floresta"])
                    mensagem += f" | AMBIENTE: {evento_ativo.upper()}"

                # --- LÓGICA DE ATAQUE (A) OU (S) ---
                elif evento.key in [pygame.K_a, pygame.K_s]:
                    if p_ativo["hp"] <= 0:
                        mensagem = "UNIDADE ABATIDA! TROQUE EM [T]."
                    elif inimigo_atual["hp"] <= 0:
                        mensagem = "ALVO ELIMINADO! USE [R] PARA NOVO SCAN."
                    else:
                        tipo_p = "base" if evento.key == pygame.K_a else "especial"
                        custo_en_p = 30 if tipo_p == "especial" else 0
                        
                        # --- LIMPEZA DE STATUS (Garante que a trava só exista sob Nevasca) ---
                        p_ativo["especial_travado"] = False
                        inimigo_atual["especial_travado"] = False
                        
                        # Re-aplica a trava IMEDIATAMENTE se for Nevasca e não for de Gelo
                        # Isso evita que o jogador "pule" a trava clicando rápido
                        if evento_ativo == "Nevasca":
                            if p_ativo.get("tribo") != "Gelo": p_ativo["especial_travado"] = True
                            if inimigo_atual.get("tribo") != "Gelo": inimigo_atual["especial_travado"] = True

                        if tipo_p == "especial" and p_ativo["en"] < custo_en_p:
                            mensagem = f"ENERGIA INSUFICIENTE! (Precisa de {custo_en_p})"
                        else:
                            # Ordem de ataque baseada em Agilidade
                            ordem = ["player", "enemy"]
                            if inimigo_atual.get("agi", 10) > p_ativo.get("agi", 10):
                                ordem = ["enemy", "player"]
                            
                            msg_combate = "" 
                            
                            for atacante_tipo in ordem:
                                if p_ativo["hp"] <= 0 or inimigo_atual["hp"] <= 0: break 
                                
                                if atacante_tipo == "player":
                                    # --- TURNO DO JOGADOR ---
                                    player_travado = p_ativo.get("especial_travado", False)
                                    
                                    # Bloqueio real do Especial
                                    if tipo_p == "especial" and player_travado:
                                        msg_combate += "| SISTEMA CONGELADO! "
                                    else:
                                        dano, crit, msg_v = engine.calcular_dano(p_ativo, inimigo_atual, tipo_p, evento_ativo)
                                        inimigo_atual["hp"] = max(0, inimigo_atual["hp"] - dano)
                                        if tipo_p == "especial": p_ativo["en"] -= custo_en_p
                                        else: p_ativo["en"] = min(p_ativo["en_max"], p_ativo["en"] + 15)
                                        
                                        msg_combate += f"| Você: {dano} "
                                        msg_combate += engine.processar_efeitos_pos_ataque(p_ativo, inimigo_atual, dano)
                                else:
                                    # --- TURNO DA IA ---
                                    ia_travada = inimigo_atual.get("especial_travado", False)
                                    # IA só tenta especial se tiver energia E não estiver travada
                                    tipo_ia = "especial" if (inimigo_atual["en"] >= 30 and random.random() < 0.4 and not ia_travada) else "base"
                                    
                                    dano_i, crit_i, msg_v_i = engine.calcular_dano(inimigo_atual, p_ativo, tipo_ia, evento_ativo)
                                    p_ativo["hp"] = max(0, p_ativo["hp"] - dano_i)
                                    if tipo_ia == "especial": inimigo_atual["en"] -= 30
                                    else: inimigo_atual["en"] = min(inimigo_atual["en_max"], inimigo_atual["en"] + 15)
                                    
                                    msg_combate += f"| Inimigo: {dano_i} "
                                    msg_combate += engine.processar_efeitos_pos_ataque(inimigo_atual, p_ativo, dano_i)

                                # --- ATUALIZAÇÃO DE TURNO E AMBIENTE ---
                                contador_turnos += 1
                                # Chama o sistema de eventos para processar curas e aplicar travas para o próximo turno
                                logs_eventos = eventos_sys.processar_efeitos_ambientais(p_ativo, inimigo_atual, evento_ativo)
                                if logs_eventos: msg_combate += " | " + " ".join(logs_eventos)

                                # Sorteio de novo ambiente a cada 2 ações (Turno completo)
                                if contador_turnos % 2 == 0:
                                    eventos_possiveis = ["Tempestade Solar", "Pulso de Blindagem", "Nevasca", "Recuperação de Floresta", "Eclipse Vazio", "Sussurros do Abismo"]
                                    evento_ativo = random.choice(eventos_possiveis)
                                    msg_combate += f" | AMBIENTE: {evento_ativo.upper()}!"

                            mensagem = msg_combate

                            if inimigo_atual["hp"] <= 0:
                                inimigo_atual["hp"] = 0
                                exp = engine.calcular_xp_recompensa(inimigo_atual["lvl"])
                                p_ativo["xp"] += exp
                                upou = engine.verificar_level_up(p_ativo)
                                creditos += random.randint(20, 60)
                                mensagem = f"VITÓRIA! +{exp} XP. " + ("LEVEL UP!" if upou else "[R] NOVO SCAN")
                            elif p_ativo["hp"] <= 0:
                                p_ativo["hp"] = 0
                                reservas_vivas = [m for m in hangar if m["hp"] > 0]
                                if not reservas_vivas:
                                    unidade_resgatada = random.choice(hangar)
                                    unidade_resgatada["hp"] = unidade_resgatada["hp_max"]
                                    p_ativo = unidade_resgatada
                                    mensagem = f"PROTOCOLO FÊNIX: {p_ativo['nome']} REATIVADO. RECUANDO..."
                                    estado = "MENU" 
                                else:
                                    mensagem = f"!!! {p_ativo['nome'].upper()} ABATIDO! TROQUE EM [T] !!!"

                elif evento.key == pygame.K_t:
                    if estado == "BATALHA" and inimigo_atual["hp"] > 0:
                        if random.random() < 0.50:
                            inimigo_atual, _ = engine.sortear_inimigo(hangar, monstro_ativo_index, monstros_db)
                            mensagem = "O inimigo fugiu durante a troca!"
                        else:
                            mensagem = "EFETUANDO RECUO TÁTICO..."
                    estado = "HANGAR"

                elif evento.key == pygame.K_u:
                    # TRAVA DE UPLOAD: Não permite se o inimigo estiver com 0 HP
                    if inimigo_atual["hp"] <= 0:
                        mensagem = "ALVO DESTRUÍDO! IMPOSSÍVEL REALIZAR UPLOAD."
                    elif data_cores > 0 and len(hangar) < slots_maximos:
                        chance = max(5, min(95, (1 - (inimigo_atual["hp"] / inimigo_atual["hp_max"])) * 100))
                        data_cores -= 1
                        if random.randint(0, 100) < chance:
                            novo_m = inimigo_atual.copy()
                            novo_m["hp"] = novo_m["hp_max"] // 4
                            hangar.append(novo_m)
                            inimigo_atual["hp"] = 0
                            mensagem = f"UPLOAD SUCESSO: {novo_m['nome']}!"
                        else:
                            mensagem = "FALHA NO UPLOAD! Contra-ataque!"
                            dano_i, _, _ = engine.calcular_dano(inimigo_atual, p_ativo, "base", evento_ativo)
                            p_ativo["hp"] = max(0, p_ativo["hp"] - dano_i)

         # PARTE DO SAVE #
        elif estado == "SAVE_MENU":
            # --- VOLTAR COM TECLADO ---
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m: 
                    estado = "MENU"
                
                # Detecta slot via Teclado (1, 2 ou 3)
                slot_sel = None
                if evento.key in [pygame.K_KP1, pygame.pygame.K_KP1]: slot_sel = 1
                elif evento.key in [pygame.K_KP2, pygame.K_KP2]: slot_sel = 2
                elif evento.key in [pygame.K_KP3, pygame.K_kP3]: slot_sel = 3
                
                # Se apertou teclado, processa
                if slot_sel:
                    # Lógica unificada de processamento (abaixo)
                    pass 

            # --- DETECTAR SLOT VIA CLIQUE DO MOUSE ---
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    mouse_pos = evento.pos
                    slot_sel = None
                    # Verifica colisão com as caixas dos slots (conforme definido no save.py)
                    for i in range(1, 4):
                        rect_slot = pygame.Rect(150, 150 + (i-1) * 120, 600, 90)
                        if rect_slot.collidepoint(mouse_pos):
                            slot_sel = i
            
            # --- PROCESSAMENTO FINAL (SALVAR OU CARREGAR) ---
            if slot_sel:
                if modo_save == "SALVAR":
                    # EMPACOTA DADOS ATUAIS
                    dados_atuais = {
                        "nome_operador": nome_operador,
                        "creditos": creditos,
                        "data_cores": data_cores,
                        "slots_maximos": slots_maximos,
                        "time": time_jogador,
                        "hangar": hangar
                    }
                    mensagem = save_sys.salvar_jogo(slot_sel, dados_atuais)
                
                elif modo_save == "CARREGAR":
                    # RECUPERA DADOS DO DISCO
                    dados_carregados, msg = save_sys.carregar_jogo(slot_sel)
                    
                    if dados_carregados:
                        # Atualiza as variáveis globais do seu main.py
                        nome_operador = dados_carregados.get("nome_operador", nome_operador)
                        creditos = dados_carregados.get("creditos", creditos)
                        data_cores = dados_carregados.get("data_cores", data_cores)
                        slots_maximos = dados_carregados.get("slots_maximos", slots_maximos)
                        hangar = dados_carregados.get("hangar", [])
                        time_jogador = dados_carregados.get("time", [])
                        
                        if hangar:
                            p_ativo = hangar[0] # Garante que o monstro ativo seja resetado
                        
                        mensagem = msg
                        estado = "MENU" # Volta ao menu após carregar com sucesso
                    else:
                        mensagem = msg
    # --- RENDERIZAÇÃO ---
    if estado == "LOGIN":
        interface_hud.desenhar_login(nome_operador, mouse_pos, pygame.Rect(350, 420, 200, 50))
    elif estado == "TRIBO_INICIAL":
        interface_hud.desenhar_tribo_inicial(opcao_selecionada)
    elif estado == "MENU":
        interface_hud.desenhar_menu_principal(nome_operador, creditos, data_cores, opcao_selecionada, sub_menu, itens_menu, itens_sub_menu)
    elif estado == "HANGAR":
        hangar_sys.desenhar_interface(hangar, time_jogador, monstro_ativo_index)
    elif estado == "BRIND":
        interface_hud.desenhar_tela_brind(tela, hangar, brind_sys)    
    elif estado == "LOJA":
        loja_sys.desenhar_interface(creditos, p_ativo, opcao_selecionada)
    elif estado == "BATALHA":
        interface_hud.desenhar_batalha(p_ativo, inimigo_atual, contador_turnos, evento_ativo, imagens_monstros, mensagem, False, 0, [])
    
    elif estado in ["MENU_LIGA", "TABELA", "ARTILHARIA", "CALENDARIO", "LIGA_ARENA", "RESULTADO_RODADA"]:
        
        liga_ui.renderizar()
    elif estado == "SAVE_MENU":
        save_sys.desenhar_interface_slots("SISTEMA DE ARQUIVAMENTO")
        # Desenha a mensagem de confirmação (aquela que diz "SLOT X ARQUIVADO")
        if 'mensagem' in locals():
            interface_hud.desenhar_caixa_mensagem(mensagem)    

    pygame.display.flip()

pygame.quit()