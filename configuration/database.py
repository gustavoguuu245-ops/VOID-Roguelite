
# ==================== NOVO: BANCO DE ATAQUES ESPECIAIS ====================
ataques_especiais_db = {
    "brasas": {"nome": "BRASAS VIVAS", "en": 35, "mult": 1.7},
    "pulso": {"nome": "PULSO SOMBRIO", "en": 45, "mult": 2.1},
    "overclock": {"nome": "OVERCLOCK", "en": 50, "mult": 1.9},
    "vazio": {"nome": "VAZIO ABSOLUTO", "en": 60, "mult": 2.5},
    "picada": {"nome": "PICADA VAMPÍRICA", "en": 40, "mult": 1.5},
    "impacto": {"nome": "IMPACTO SÍSMICO", "en": 55, "mult": 2.0},
    "chicote": {"nome": "CHICOTE DE CLOROFILA", "en": 45, "mult": 1.6},
    "veneno": {"nome": "NUVEM TÓXICA", "en": 35, "mult": 1.4},
}

# ==================== BANCO DE DADOS ATUALIZADO ====================
tribos_info = {
    "Sombras":     {"recurso": "Água Potável", "cor": (40, 40, 180)},
    "Fogo":         {"recurso": "Energia Caótica", "cor": (220, 60, 20)},
    "Mecânica":     {"recurso": "Metais Raros", "cor": (140, 140, 150)},
    "Esquecidos": {"recurso": "Espaço Vital", "cor": (180, 50, 255)},
    "Naturalistas": {"recurso": "Concervação Vital", "cor": (34, 139, 34)},
    "Gelo": {"recurso": "Combustivel", "cor": (180, 230, 255)},
}

# ==================== BANCO DE HABILIDADES PASSIVAS ====================\
habilidades_passivas_db = {
    "vampirismo": {"nome": "Vampirismo", "desc": "Drena a energia do inimigo, curando 20% do dano causado."},
    "reflexo": {"nome": "Reflexo", "desc": "O Reflexo está devolvendo exatamente 25% (um quarto) do dano recebido.."},
    "burn": {"nome": "Queimadura", "desc": "Causa dano residual de 10% do HP max do alvo."},
    "blindagem": {"nome": "Blindagem", "desc": "Reduz o dano final recebido em 25%."},
    "esquiva": {"nome": "Esquiva", "desc": "Tem 15% de chance de anular o ataque completamente."}
}

monstros_db = {
    "Shadowfang":      {"tribo": "Sombras",    "hp_base": 95,  "atk": 22, "def": 10, "agi_base": 60, "en_max": 100, "img": "assets/SHADOWFANG.png", "esp": "pulso", "raridade": "Raro"},
    "Flamehowl":       {"tribo": "Fogo",       "hp_base": 88,  "atk": 28, "def": 8,  "agi_base": 30, "en_max": 100, "img": "assets/FLAMEHOWL.png", "esp": "brasas", "raridade": "Raro"},
    "Ironclad":        {"tribo": "Mecânica",   "hp_base": 115, "atk": 16, "def": 20, "agi_base": 10, "en_max": 120, "img": "assets/iron.png", "esp": "impacto", "raridade": "Raro"},
    "Voidwisp":        {"tribo": "Esquecidos", "hp_base": 82,  "atk": 20, "def": 12, "agi_base": 30, "en_max": 150, "img": "assets/VOID.png", "esp": "vazio", "raridade": "Raro"},
    "Bolt-Drone":      {"tribo": "Mecânica",   "hp_base": 85,  "atk": 30, "def": 10, "agi_base": 45, "en_max": 80,  "img": "assets/BOLT-DRONE.png", "esp": "overclock", "raridade": "Raro"},
    "Nightshade":      {"tribo": "Sombras",    "hp_base": 90,  "atk": 18, "def": 12, "agi_base": 50, "en_max": 100, "img": "assets/NIGHTSHADE.png", "esp": "pulso", "raridade": "Raro"},
    "Magma-Core":      {"tribo": "Fogo",       "hp_base": 105, "atk": 24, "def": 18, "agi_base": 10, "en_max": 100, "img": "assets/MAGMA-CORE.png", "esp": "brasas", "raridade": "Raro"},
    "Abyss-Walker":    {"tribo": "Esquecidos", "hp_base": 85,  "atk": 25, "def": 14, "agi_base": 35, "en_max": 110, "img": "assets/ABYSS-WALKER.png", "esp": "vazio", "raridade": "Raro"},
    "Vampiric":        {"tribo": "Sombras",    "hp_base": 80,  "atk": 25, "def": 8,  "agi_base": 55, "en_max": 120, "img": "assets/vampiric.png", "hab": "vampirismo", "esp": "picada", "raridade": "Raro"},
    "Reflector-Shell": {"tribo": "Mecânica",   "hp_base": 130, "atk": 15, "def": 25, "agi_base": 10, "en_max": 90,  "img": "assets/REFLECTOR.png", "hab": "reflexo", "esp": "impacto", "raridade": "Raro"},
    "Ignis-Reptile":   {"tribo": "Fogo",       "hp_base": 82,  "atk": 34, "def": 7,  "agi_base": 45, "en_max": 90,  "img": "assets/IGNIS.png", "esp": "brasas", "raridade": "Raro"},
    "Skrull":          {"tribo": "Esquecidos", "hp_base": 90,  "atk": 25, "def": 12, "agi_base": 35, "en_max": 130, "img": "assets/Skrull.png", "hab": "vampirismo", "esp": "vazio", "raridade": "Raro"},
    "Infernal-TriGuardian": {"tribo": "Fogo",  "hp_base": 92,  "atk": 30, "def": 12, "agi_base": 45, "en_max": 110, "hab": "burn",  "img": "assets/TRI_GUARDIAN.png", "esp": "brasas", "raridade": "Elite"},
    "Anjo-Deletado":   {"tribo": "Esquecidos", "hp_base": 150, "atk": 25, "def": 30, "agi_base": 5,  "en_max": 100, "hab": "vampirismo", "img": "assets/ANJO_DELETADO.png", "esp": "vazio", "raridade": "Lendário"},
    "Mainframe-Overlord": {"tribo": "Mecânica", "hp_base": 130, "atk": 35, "def": 40, "agi_base": 10, "en_max": 90,  "hab": "blindagem", "img": "assets/OVERLORD.png", "esp": "pulso", "raridade": "Lendário"},
    "Zero-Day-Entity": {"tribo": "Sombras",    "hp_base": 88,  "atk": 42, "def": 8,  "agi_base": 85, "en_max": 130, "hab": "esquiva", "img": "assets/ZERO_DAY_QUEEN.png", "esp": "pulso", "raridade": "Lendário"},
    "Copper-Drone":    {"tribo": "Mecânica",   "hp_base": 55,  "atk": 14, "def": 12, "agi_base": 30, "en_max": 80,  "hab": None, "img": "assets/COPPER_DRONE.png", "esp": "pulso", "raridade": "Comum"},
    "Idolo-Fornalha":  {"tribo": "Fogo",       "hp_base": 115, "atk": 36, "def": 25, "agi_base": 18, "en_max": 105, "hab": "burn","img": "assets/IDOLO_FORNALHA.png","esp": "brasas", "raridade": "Elite"},
    "Carniça-de-Osso": {"tribo": "Esquecidos", "hp_base": 58,  "atk": 16, "def": 20, "agi_base": 12, "en_max": 75,  "hab": None,"img": "assets/CARNICA_OSSO.png", "esp": "vazio", "raridade": "Comum"},
    "Acólito-do-Pavio": {"tribo": "Fogo",      "hp_base": 45,  "atk": 22, "def": 8,  "agi_base": 35, "en_max": 85,  "hab": "burn", "img": "assets/ACOLITO_PAVIO.png","esp": "brasas", "raridade": "Comum"},
    "Rastreador-Sombrio": {"tribo": "Sombras", "hp_base": 40,  "atk": 18, "def": 5,  "agi_base": 55, "en_max": 90,  "hab": "esquiva","img": "assets/RASTREADOR.png", "esp": "pulso", "raridade": "Comum"},
    "Cavalheiro-Caos": {"tribo": "Sombras",    "hp_base": 92,  "atk": 38, "def": 12, "agi_base": 72, "en_max": 130, "hab": "esquiva", "img": "assets/CAVALHEIRO_CAOS.png","esp": "pulso", "raridade": "Elite"},
    "Coelho Rosa":     {"tribo": "Mecânica",   "hp_base": 110, "atk": 30, "def": 22, "agi_base": 55, "en_max": 105, "hab": "reflexo", "img": "assets/COELHO_ROSA.png", "esp": "impacto", "raridade": "Elite"},
    "Bit-Mite":        {"tribo": "Mecânica",   "hp_base": 42,  "atk": 12, "def": 8,  "agi_base": 25, "en_max": 70,  "hab": None, "img": "assets/BIT_MITE.png", "esp": "pulso", "raridade": "Comum"},
    "Fagulha":   {"tribo": "Fogo",       "hp_base": 38,  "atk": 15, "def": 5,  "agi_base": 30, "en_max": 70,  "hab": None, "img": "assets/FAGULHA.png", "esp": "brasas", "raridade": "Comum"},
    "Sombra-Pálida":   {"tribo": "Sombras",    "hp_base": 35,  "atk": 13, "def": 4,  "agi_base": 40, "en_max": 75,  "hab": None, "img": "assets/SOMBRA_PALI.png","esp": "pulso", "raridade": "Comum"},
    "Fragmento-Lixo":  {"tribo": "Esquecidos", "hp_base": 40,  "atk": 11, "def": 10, "agi_base": 20, "en_max": 80,  "hab": None, "img": "assets/LIXO_DIGITAL.png", "esp": "vazio", "raridade": "Comum"},
    "Atirador-de-Falhas": {"tribo": "Esquecidos", "hp_base": 98,  "atk": 36, "def": 10, "agi_base": 65, "en_max": 120, "hab": "vampirismo", "img": "assets/ATIRADOR_FALHAS.png", "esp": "vazio", "raridade": "Elite"},
    "Sentinela-Curumim": {"tribo": "Naturalistas", "hp_base": 110, "atk": 18, "def": 12, "agi_base": 16, "en_max": 100, "hab": "vampirismo", "img": "assets/CURUMIM.png", "esp": "chicote", "raridade": "Comum"},
    "Guardião-Mata": {"tribo": "Naturalistas", "hp_base": 145, "atk": 30, "def": 22, "agi_base": 8, "en_max": 130, "hab": "blindagem", "img": "assets/GUARDIAO_MATA.png", "esp": "impacto", "raridade": "Elite"},
    "Espreitadora-Igapó": {"tribo": "Naturalistas", "hp_base": 85, "atk": 25, "def": 10, "agi_base": 48, "en_max": 95, "hab": "esquiva", "img": "assets/IGAPO.png", "esp": "chicote", "raridade": "Raro"},
    "Paje": {"tribo": "Naturalistas", "hp_base": 180, "atk": 40, "def": 30, "agi_base": 12, "en_max": 200, "hab": "vampirismo", "img": "assets/PAJE.png", "esp": "chicote", "raridade": "Lendário"},
    "Matriarca-dos-Ventos": {"tribo": "Naturalistas", "hp_base": 95, "atk": 32, "def": 12, "agi_base": 80, "en_max": 120, "hab": "esquiva", "img": "assets/MATRIARCA.png", "esp": "pulso", "raridade": "Elite"},
    "Caçador-Ancestral": {"tribo": "Naturalistas", "hp_base": 110, "atk": 45, "def": 15, "agi_base": 70, "en_max": 120, "hab": "vampirismo", "img": "assets/CACADOR.png", "esp": "impacto", "raridade": "Elite"},
    "Coral": {"tribo": "Naturalistas", "hp_base": 80, "atk": 25, "def": 12, "agi_base": 60, "en_max": 100, "hab": "esquiva", "img": "assets/CORAL.png", "esp": "veneno", "raridade": "Raro"},
    "Aratama": {"tribo": "Naturalistas", "hp_base": 120, "atk": 18, "def": 30, "agi_base": 22, "en_max": 95, "hab": "blindagem", "img": "assets/ARATAMA.png", "esp": "impacto", "raridade": "Raro"},
    "Sapo-de-Vidro": {"tribo": "Naturalistas", "hp_base": 55, "atk": 14, "def": 12, "agi_base": 30, "en_max": 80, "hab": None, "img": "assets/SAPO.png", "esp": "chicote", "raridade": "Comum"},
    "Smoke": {"tribo": "Sombras", "hp_base": 70, "atk": 15, "def": 5, "agi_base": 100, "en_max": 140, "hab": "esquiva", "img": "assets/SMOKE.png", "esp": "pulso", "raridade": "Lendário"},
    "Flameant":  {"tribo": "Fogo", "hp_base": 45, "atk": 20, "def": 8, "agi_base": 35, "en_max": 80, "img": "assets/FLAMEANT.png", "esp": "brasas", "raridade": "Comum"},
    "Magmapillar": {"tribo": "Fogo", "hp_base": 88, "atk": 28, "def": 12, "agi_base": 20, "en_max": 90, "img": "assets/MAGMAPILLAR.png", "esp": "brasas", "raridade": "Raro"},
    "Soldado de Pilha": {"tribo": "Mecânica", "hp_base": 60, "atk": 15, "def": 15, "agi_base": 20, "en_max": 100, "img": "assets/SOLDADO_PILHA.png", "esp": "impacto", "raridade": "Comum"},
    "Pixie": {"tribo": "Esquecidos", "hp_base": 78, "atk": 24, "def": 12, "agi_base": 65, "en_max": 140, "hab": "esquiva", "img": "assets/fada.png", "esp": "vazio", "raridade": "Raro"},
    "Joker":  {"tribo": "Esquecidos", "hp_base": 110, "atk": 35, "def": 20, "agi_base": 30, "en_max": 110, "hab": "burn", "img": "assets/joker.png", "esp": "vazio", "raridade": "Elite"},
    "Gato-Binário": {"tribo": "Sombras", "hp_base": 45, "atk": 18, "def": 8, "agi_base": 50, "en_max": 90, "img": "assets/GATO.png", "esp": "pulso", "raridade": "Comum"},
    "Caminhão-Bit": {"tribo": "Mecânica", "hp_base": 120, "atk": 12, "def": 25, "agi_base": 10, "en_max": 200, "img": "assets/CAMINHAO.png", "esp": "impacto", "raridade": "Raro"},
    "Koleóptero-Gelo": {"tribo": "Gelo", "hp_base": 62, "atk": 14, "def": 22, "agi_base": 15, "en_max": 80, "hab": "blindagem", "img": "assets/KOLEOPTERO.png", "esp": "impacto", "raridade": "Comum"},
    "Presa-Fóssil": {"tribo": "Gelo", "hp_base": 55, "atk": 24, "def": 10, "agi_base": 45, "en_max": 85, "hab": None, "img": "assets/PRESA_FOSSIL.png", "esp": "picada", "raridade": "Comum"},
    "Lamento-de-Crio": {"tribo": "Gelo", "hp_base": 125, "atk": 48, "def": 20, "agi_base": 65, "en_max": 140, "hab": "esquiva", "img": "assets/Crio.png", "esp": "vazio", "raridade": "Elite"},
    "Caminhante-Nival": {"tribo": "Gelo", "hp_base": 88, "atk": 28, "def": 20, "agi_base": 25, "en_max": 100, "hab": "esquiva", "img": "assets/NIVAL.png", "esp": "impacto", "raridade": "Raro"},
    "Núcleo-da-Desolação": {"tribo": "Gelo", "hp_base": 150, "atk": 60, "def": 30, "agi_base": 75, "en_max": 200, "hab": "vampirismo", "img": "assets/DESOLATION.png", "esp": "vazio", "raridade": "Lendário"},
    "Leviatã-Degelo": {"tribo": "Gelo", "hp_base": 105, "atk": 22, "def": 25, "agi_base": 18, "en_max": 95, "hab": "blindagem", "img": "assets/LEVIATA.png", "esp": "picada", "raridade": "Raro"},
    "Eterna": {"tribo": "Gelo", "hp_base": 100, "atk": 42, "def": 25, "agi_base": 30, "en_max": 150, "hab": "vampirismo", "img": "assets/ETERNA.png", "esp": "vazio", "raridade": "Elite"},
    "Pachydermus-Rex": {"tribo": "Gelo", "hp_base": 145, "atk": 34, "def": 40, "agi_base": 8, "en_max": 100, "hab": "blindagem", "img": "assets/PACHYDERMUS.png", "esp": "impacto", "raridade": "Elite"},
    "Ancestral": {"tribo": "Gelo", "hp_base": 115, "atk": 38, "def": 18, "agi_base": 55, "en_max": 110, "hab": "esquiva", "img": "assets/ANC.png", "esp": "pulso", "raridade": "Elite"},
}

TIERS = {
    "Comum":    {"chance": 60, "cor": "#FFFFFF"}, # Branco
    "Raro":     {"chance": 30, "cor": "#00AAFF"}, # Azul
    "Elite":    {"chance": 8,  "cor": "#AA00FF"}, # Roxo
    "Lendário": {"chance": 2,  "cor": "#FFD700"}  # Dourado
}

# --- CHANCES DE UPLOAD (0.0 a 1.0) ---
CHANCES_UPLOAD = {
    "Comum": 0.70,    # 70%
    "Raro": 0.40,     # 40%
    "Elite": 0.15,    # 15%
    "Lendário": 0.04  # 4%
}

TABELA_TIPOS = {
    "Fogo":         {"Mecânica": 1.5, "Gelo": 0.5},
    "Mecânica":     {"Naturalistas": 1.5, "Fogo": 0.5},
    "Naturalistas": {"Sombras": 1.5, "Mecânica": 0.5},
    "Sombras":      {"Gelo": 1.5, "Naturalistas": 0.5},
    "Gelo":         {"Fogo": 1.5, "Sombras": 1.5} # Gelo é forte contra Fogo (apaga) e Sombras (congela o vazio)
}