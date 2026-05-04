import random
from configuration.engine import calcular_xp_proximo

def verificar_troca_unidade(p_ativo, time_jogador, hangar, torneio_ativo):
    """
    Decide se o jogador pode trocar de monstro ou se o primeiro 
    deve ser definido caso esteja vazio.
    """
    # Se não tem ninguém ativo mas tem gente no time, ativa o primeiro
    if p_ativo is None and len(time_jogador) > 0:
        return time_jogador[0], "Unidade inicial pronta!"

    # Lógica que você tinha no IF do K_T
    if torneio_ativo:
        return None, "TORNEIO EM CURSO: DESERÇÃO BLOQUEADA!"
    
    if len(hangar) > 1:
        # Retornamos um sinal para o main mudar o estado
        return "MUDAR_PARA_HANGAR", "ESCOLHA O REFORÇO!"
    
    return None, "VOCÊ NÃO TEM OUTRAS UNIDADES!"
def determinar_ordem_turno(p_ativo, inimigo_atual):
    """Define quem ataca primeiro com base na agilidade."""
    p_agi = p_ativo.get("agi", p_ativo.get("agi_base", 10))
    e_agi = inimigo_atual.get("agi", inimigo_atual.get("agi_base", 10))
    return ["player", "enemy"] if p_agi >= e_agi else ["enemy", "player"]

def verificar_derrota_player(p_ativo, hangar, torneio_ativo, torneio_db, patentes_lista, patente_atual_index):
    """
    Verifica se o player perdeu e se pode trocar de monstro.
    Retorna (pode_continuar, nova_mensagem, novo_estado)
    """
    if p_ativo["hp"] <= 0:
        p_ativo["hp"] = 0
        # Filtra quem ainda pode lutar
        reservas_vivas = [m for m in hangar if m["hp"] > 0 and m.get("no_time")]
        
        pode_trocar = False
        if not torneio_ativo:
            pode_trocar = len(reservas_vivas) > 0
        else:
            nome_da_patente = patentes_lista[patente_atual_index]
            # Verifica regra do torneio (Formato 1x1, 3x3, etc)
            pode_trocar = torneio_db[nome_da_patente]["formato"] > 1 and len(reservas_vivas) > 0

        if pode_trocar:
            return True, f"{p_ativo['nome']} ABATIDO! CHAME REFORÇOS NA TECLA [T]!", "BATALHA"
        else:
            return False, "EQUIPE TOTALMENTE ABATIDA! RETORNANDO À BASE...", "MENU"
            
    return True, "", "BATALHA"
def aplicar_vampirismo(atacante, dano):
    cura = int(dano * 0.15)
    atacante["hp"] = min(atacante["hp_max"], atacante["hp"] + cura)
    return f" | VAMPIRISMO: +{cura} HP"

def aplicar_reflexo(alvo, dano_recebido):
    reflexo = int(dano_recebido * 0.20)
    alvo["hp"] -= reflexo
    if alvo["hp"] < 0: alvo["hp"] = 0
    return f" | REFLEXO: {reflexo} de dano!"