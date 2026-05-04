import random
from configuration.database import *

# =================================================================
# 1. SISTEMA DE PROGRESSÃO E CÁLCULOS
# =================================================================

def calcular_xp_proximo(lvl):
    return int(50 * (lvl ** 1.5) + (lvl * 100))

def calcular_xp_recompensa(lvl_inimigo):
    base_xp = lvl_inimigo * 25
    return base_xp + random.randint(5, 15)

def verificar_level_up(monstro):
    subiu = False
    while monstro["xp"] >= monstro["xp_max"]:
        monstro["xp"] -= monstro["xp_max"]
        monstro["lvl"] += 1
        
        # --- MODIFICAÇÃO: Ganhos Genéticos Baseados no DNA ---
        # Agora o monstro cresce conforme o bônus do Brinde do Véu
        # Se dna["hp"] for 0.15, o ganho será de 15% (1.15)
        
        monstro["hp_max"] = int(monstro["hp_max"] * (1.0 + monstro["dna"]["hp"]))
        monstro["atk"] = int(monstro["atk"] * (1.0 + monstro["dna"]["atk"]))
        monstro["def"] = int(monstro["def"] * (1.0 + monstro["dna"]["def"]))
        # Se quiser que a agilidade também cresça com DNA:
        # monstro["agi"] = int(monstro.get("agi", 10) * (1.0 + monstro["dna"].get("agi", 0.05)))
        
        # --- MANUTENÇÃO DO QUE JÁ FUNCIONAVA ---
        monstro["xp_max"] = calcular_xp_proximo(monstro["lvl"])
        
        # Cura Total no UP
        monstro["hp"] = monstro["hp_max"]
        monstro["en"] = monstro["en_max"]
        subiu = True
        
    return subiu

def calcular_dano(atacante, defensor, tipo_ataque="base", evento_ativo="Estabilidade"):
    # 0. Verificação de Vida
    if atacante["hp"] <= 0: return 0, False, "UNIDADE DESLIGADA"

    # =========================================================
    # 1. ESQUIVA (Calculada ANTES de tudo. Se desviar, anula o ataque)
    # =========================================================
    passiva_def = str(defensor.get("passiva", "")).lower()
    if passiva_def == "esquiva":
        if random.random() <= 0.15:  # 15% de chance
            # Retorna 0 de dano, False (não foi crítico), e a mensagem especial
            return 0, False, "ESQUIVA LENDÁRIA! O ataque falhou!"

    # =========================================================
    # STATUS BASE E PREPARAÇÃO
    # =========================================================
    atk = atacante.get("atk", 10)
    dfesa = defensor.get("def", 10)
    tribo_atq = atacante.get("tribo", "")
    tribo_def = defensor.get("tribo", "")
    
    # --- LÓGICA DE EVENTOS CAÓTICOS (1 POR TRIBO) ---
    chance_critico = 0.10
    msg_evento = ""

    # 1. FOGO na Tempestade Solar: Dano explode (Mais Dano)
    if evento_ativo == "Tempestade Solar" and tribo_atq == "Fogo":
        atk *= 1.4
    
    # 2. MECÂNICA no Pulso de Blindagem: Foca em DEFESA (Não dano)
    elif evento_ativo == "Pulso de Blindagem" and tribo_def == "Mecânica":
        dfesa *= 1.5
    
    # 3. ESQUECIDOS nos Sussurros: Dano Mental (Bônus de Ataque)
    elif evento_ativo == "Sussurros do Abismo" and tribo_atq == "Esquecidos":
        atk *= 1.3

    # --- TABELA DE VANTAGENS (5 TRIBOS) ---
    tabela = {
        "Fogo": {"Mecânica": 1.5, "Gelo": 0.5},
        "Mecânica": {"Naturalistas": 1.5, "Fogo": 0.5},
        "Naturalistas": {"Sombras": 1.5, "Mecânica": 0.5},
        "Sombras": {"Gelo": 1.5, "Naturalistas": 0.5},
        "Gelo": {"Fogo": 1.5, "Sombras": 1.5} 
    }
    mult_tipo = tabela.get(tribo_atq, {}).get(tribo_def, 1.0)
    
    # =========================================================
    # CÁLCULO PRINCIPAL
    # =========================================================
    mod_especial = 1.6 if tipo_ataque == "especial" else 1.0
    dano_base = (atk * mod_especial * mult_tipo) - (dfesa * 0.4)
    
    critico = random.random() < chance_critico
    if critico: dano_base *= 2
    
    dano_final = int(max(8, dano_base * random.uniform(0.9, 1.1)))
    
    msg = "!!! VANTAGEM !!!" if mult_tipo > 1.0 else ("... FRAQUEZA ..." if mult_tipo < 1.0 else "")
    if critico: msg = "CRÍTICO! " + msg

    # =========================================================
    # 2. BLINDAGEM (Calculada no FIM, reduzindo o dano que ia entrar)
    # =========================================================
    if passiva_def == "blindagem":
        reducao = int(dano_final * 0.25) # Corta 25% do dano
        dano_final -= reducao
        # Adiciona um aviso na frente da mensagem para o jogador ver na tela
        msg = f"[BLINDAGEM ativada] {msg}".strip()
    
    return dano_final, critico, msg

# =================================================================
# 2. GERAÇÃO DE INSTÂNCIAS E SCANNER
# =================================================================

def gerar_instancia_monster(nome, monstros_db):
    base = monstros_db[nome]
    dna = {
        "hp":  round(random.uniform(0.6, 1.8), 2),
        "atk": round(random.uniform(0.6, 1.8), 2),
        "def": round(random.uniform(0.6, 1.8), 2),
        "agi": round(random.uniform(0.6, 1.8), 2)
    }
    
    hp_m = int(base["hp_base"] * dna["hp"])
    lvl = 1
    return {
        "nome": nome, "dna": dna, "lvl": lvl, "xp": 0,
        "tribo": base.get("tribo", "Sombras"),
        "xp_max": calcular_xp_proximo(lvl),
        "hp_max": hp_m, "hp": hp_m,
        "atk": int(base.get("atk_base", 15) * dna["atk"]),
        "def": int(base.get("def_base", 10) * dna["def"]),
        "agi": int(base.get("agi_base", 10) * dna["agi"]),
        "en_max": 100, "en": 100,
        "esp_id": base.get("esp", "brasas"),
        "passiva": base.get("passiva", "Nenhuma")
    }

def sortear_inimigo(hangar, monstro_ativo_index, monstros_db):
    nome = random.choice(list(monstros_db.keys()))
    inimigo = gerar_instancia_monster(nome, monstros_db)
    lvl_p = hangar[monstro_ativo_index]["lvl"] if hangar else 1
    inimigo["lvl"] = max(1, random.randint(lvl_p - 1, lvl_p + 3))
    
    # Escalonamento de Status
    mult = 1 + (inimigo["lvl"] - 1) * 0.12
    inimigo["hp_max"] = int(inimigo["hp_max"] * mult)
    inimigo["hp"] = inimigo["hp_max"]
    inimigo["atk"] = int(inimigo["atk"] * mult)
    return inimigo, f"SCANNER: {nome} Lv.{inimigo['lvl']} detectado."

# =================================================================
# 3. HABILIDADES PASSIVAS 
# =================================================================

def processar_efeitos_pos_ataque(atacante, defensor, dano):
    """Processa efeitos que ocorrem após a finalização do cálculo de dano principal."""
    logs = []
    
    # Padronização para evitar erros de maiúsculas/minúsculas no banco de dados
    passiva_atk = str(atacante.get("passiva", "")).lower()
    passiva_def = str(defensor.get("passiva", "")).lower()

    # 1. VAMPIRISMO: Sombras ou passiva (Cura 20% do dano causado)
    if passiva_atk == "vampirismo" or atacante.get("tribo") == "Sombras":
        cura = dano // 5 # Equilibrado para 20%
        if cura > 0:
            atacante["hp"] = min(atacante["hp_max"], atacante["hp"] + cura)
            logs.append(f"DRENO:+{cura}")
    
    # 2. REFLEXO: Mecânicos ou passiva (Devolve 25% do dano recebido)
    if passiva_def == "reflexo" or defensor.get("tribo") == "Mecânica":
        dano_retorno = dano // 4
        if dano_retorno > 0:
            atacante["hp"] -= dano_retorno
            logs.append(f"REFLEXO:-{dano_retorno}")
        
    # 3. BURN: Fogo ou passiva (Dano de 10% do HP Máximo do alvo)
    if passiva_atk == "burn" or atacante.get("tribo") == "Fogo":
        dano_burn = max(1, defensor["hp_max"] // 10)
        defensor["hp"] -= dano_burn
        logs.append(f"BURN:-{dano_burn}")
    
    return " ".join(logs)