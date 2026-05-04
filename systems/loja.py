import pygame
from configuration.config import *

class ShopSystem:
    def __init__(self, tela, fontes):
        self.tela = tela
        self.fonte_titulo = fontes['titulo']
        self.fonte_menu = fontes['menu']
        self.fonte_pequena = fontes['pequena']
        
        # O banco de itens fica dentro do sistema agora
        self.itens = [
            {"nome": "DATA_CORE", "preco": 50, "desc": "Unidade de Upload"},
            {"nome": "DATA_REPAIR", "preco": 30, "desc": "Cura +40 HP do Ativo"},
            {"nome": "SYSTEM_RESTORE", "preco": 100, "desc": "Restaura HP Total do Ativo"},
            {"nome": "MEM_EXPANSION", "preco": 500, "desc": "+1 Slot no Hangar"},
            {"nome": "SIGNAL_BOOSTER", "preco": 200, "desc": "Melhora Sinal de Upload"}
        ]

    def desenhar_interface(self, creditos, m_ativo, opcao_selecionada):
        # Título
        self.tela.blit(self.fonte_titulo.render("LOJA DE SUPRIMENTOS", True, VERDE_SISTEMA), (50, 50))
        
        # Info de Créditos e Alvo
        status_txt = f"CRÉDITOS: {creditos} | ALVO: {m_ativo['nome']} (HP:{m_ativo['hp']}/{m_ativo['hp_max']})"
        self.tela.blit(self.fonte_pequena.render(status_txt, True, OURO_STATUS), (50, 110))
        
        # Lista de Itens
        for i, item in enumerate(self.itens):
            cor = AZUL_HUD if i == opcao_selecionada else (100, 100, 100)
            
            # Nome e Preço
            txt_item = f"{item['nome']} - {item['preco']} CR"
            self.tela.blit(self.fonte_menu.render(txt_item, True, cor), (50, 180 + i*65))
            
            # Descrição
            self.tela.blit(self.fonte_pequena.render(item['desc'], True, (150, 150, 150)), (50, 215 + i*65))
        
        self.tela.blit(self.fonte_pequena.render("[ENTER] COMPRAR   [M] MENU", True, VERDE_SISTEMA), (LARGURA//2 - 80, 550))

    def processar_compra(self, opcao, creditos, m_ativo, data_cores, slots_maximos, signal_boosters):
        """
        Retorna (sucesso, novos_creditos, novo_m_ativo, novas_cores, novos_slots, novos_boosters, mensagem)
        """
        item = self.itens[opcao]
        
        if creditos >= item["preco"]:
            if item["nome"] == "DATA_CORE":
                return True, creditos - item["preco"], m_ativo, data_cores + 1, slots_maximos, signal_boosters, "DATA_CORE ADQUIRIDO."
            
            elif item["nome"] == "DATA_REPAIR":
                m_ativo["hp"] = min(m_ativo["hp"] + 40, m_ativo["hp_max"])
                return True, creditos - item["preco"], m_ativo, data_cores, slots_maximos, signal_boosters, "REPARO DE DADOS CONCLUÍDO."
            
            elif item["nome"] == "SYSTEM_RESTORE":
                m_ativo["hp"] = m_ativo["hp_max"]
                return True, creditos - item["preco"], m_ativo, data_cores, slots_maximos, signal_boosters, "SISTEMA TOTALMENTE RESTAURADO."
            
            elif item["nome"] == "MEM_EXPANSION":
                return True, creditos - item["preco"], m_ativo, data_cores, slots_maximos + 1, signal_boosters, "CAPACIDADE DO HANGAR AMPLIADA."
            
            elif item["nome"] == "SIGNAL_BOOSTER":
                return True, creditos - item["preco"], m_ativo, data_cores, slots_maximos, signal_boosters + 1, "SINAL DE UPLOAD FORTALECIDO."
        
        return False, creditos, m_ativo, data_cores, slots_maximos, signal_boosters, "CRÉDITOS INSUFICIENTES!"