# =================================================================
# V.O.I.D. SYSTEMS - GESTOR DE EVENTOS CAÓTICOS
# =================================================================
import random

def processar_efeitos_ambientais(p_ativo, inimigo_atual, evento_ativo):
    """
    Aplica bônus passivos e efeitos de status baseados no evento ativo.
    Esta função deve ser chamada no final de cada ciclo de turno.
    Retorna uma lista de strings para alimentar o log de combate.
    """
    logs = []
    # Lista de entidades para aplicar a lógica de forma justa (Player e IA)
    entidades = [p_ativo, inimigo_atual]

    for e in entidades:
        # Se a unidade estiver abatida, não processa bônus
        if e["hp"] <= 0:
            continue
            
        tribo = e.get("tribo", "Desconhecida")

        # --- 1. TEMPESTADE SOLAR (FOGO) ---
        # Bônus: Além do dano extra na engine, recupera Energia rapidamente
        if evento_ativo == "Tempestade Solar" and tribo == "Fogo":
            ganho_en = 10
            e["en"] = min(e["en_max"], e["en"] + ganho_en)
            logs.append(f"{e['nome']} absorveu calor: +{ganho_en} EN")

        # --- 2. PULSO DE BLINDAGEM (MECÂNICA) ---
        # Bônus: Nanobots reparam a carcaça (Pequena cura baseada na Defesa)
        elif evento_ativo == "Pulso de Blindagem" and tribo == "Mecânica":
            reparo = int(e["def"] * 0.2) # Repara baseado na força da defesa
            e["hp"] = min(e["hp_max"], e["hp"] + reparo)
            logs.append(f"{e['nome']} auto-reparo: +{reparo} HP")

       # --- 3. NEVASCA (GELO) ---
        # Bônus: "Criogênese" - Gelo regenera EN. Outros perdem EN e ficam sem Especial.
        elif evento_ativo == "Nevasca":
            if tribo == "Gelo":
                # Monstros de Gelo ficam revigorados no frio
                e["en"] = min(e["en_max"], e["en"] + 5)
                e["especial_travado"] = False # Garante que Gelo sempre use
            else:
                # Quem não é de Gelo sofre fadiga e CONGELA o Especial
                e["en"] = max(0, e["en"] - 8)
                e["especial_travado"] = True  # <--- A TRAVA AQUI
                logs.append(f"{e['nome']} congelou: Especial [S] BLOQUEADO!")

        # --- 4. RECUPERAÇÃO DE FLORESTA (NATURALISTAS) ---
        # Bônus: Cura passiva baseada no HP Máximo
        elif evento_ativo == "Recuperação de Floresta" and tribo == "Naturalistas":
            cura = int(e["hp_max"] * 0.10) # 10% de recuperação
            e["hp"] = min(e["hp_max"], e["hp"] + cura)
            logs.append(f"{e['nome']} fotossíntese: +{cura} HP")

        # --- 5. ECLIPSE VAZIO (SOMBRAS) ---
        # Bônus: Furtividade - Difícil de atingir (Aumenta Agilidade temporariamente)
        elif evento_ativo == "Eclipse Vazio" and tribo == "Sombras":
            # Bônus de agilidade ajuda a atacar primeiro no próximo turno
            e["agi"] = int(e.get("agi", 10) * 1.3)
            logs.append(f"{e['nome']} camuflado nas sombras!")

        # --- 6. SUSSURROS DO ABISMO (ESQUECIDOS) ---
        # Bônus: Dano Mental - Ignora parte da defesa do oponente
        elif evento_ativo == "Sussurros do Abismo" and tribo == "Esquecidos":
            # Vamos simular um buff de fúria
            e["atk"] = int(e["atk"] * 1.1)
            logs.append(f"{e['nome']} ouviu o chamado: ATK UP!")

    return logs