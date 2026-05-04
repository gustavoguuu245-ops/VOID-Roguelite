import pygame
import pickle
import os
from configuration.config import *

class SaveSystem:
    def __init__(self, tela, fontes):
        self.tela = tela
        self.fonte_titulo = fontes['titulo']
        self.fonte_menu = fontes['menu']
        self.fonte_pequena = fontes['pequena']
        self.diretorio_saves = "saves"
        
        # Cria a pasta de saves se ela não existir
        if not os.path.exists(self.diretorio_saves):
            os.makedirs(self.diretorio_saves)

    def salvar_jogo(self, slot, dados_globais):
        """
        Grava os dados no disco. 
        Usa .get() para evitar que o jogo feche se faltar alguma informação.
        """
        nome_arquivo = os.path.join(self.diretorio_saves, f"save_slot_{slot}.dat")
        
        try:
            # Filtramos os dados para garantir que apenas texto/números sejam salvos
            dados_para_salvar = {
                "nome_operador": str(dados_globais.get('nome_operador', "Operador")),
                "creditos": int(dados_globais.get('creditos', 0)),
                "data_cores": int(dados_globais.get('data_cores', 0)),
                "slots_maximos": int(dados_globais.get('slots_maximos', 10)),
                "patente_index": int(dados_globais.get('patente_index', 0)),
                "time": self._filtrar_lista(dados_globais.get('time', [])),
                "hangar": self._filtrar_lista(dados_globais.get('hangar', []))
            }

            with open(nome_arquivo, "wb") as f:
                pickle.dump(dados_para_salvar, f)
            
            return f"SLOT {slot} ARQUIVADO!"
        except Exception as e:
            print(f"ERRO CRÍTICO AO SALVAR: {e}")
            return "FALHA NO PROTOCOLO"

    def carregar_jogo(self, slot):
        """Recupera os dados do arquivo .dat"""
        nome_arquivo = os.path.join(self.diretorio_saves, f"save_slot_{slot}.dat")
        
        if not os.path.exists(nome_arquivo):
            return None, "TERMINAL VAZIO"
        
        try:
            with open(nome_arquivo, "rb") as f:
                dados = pickle.load(f)
                return dados, "DADOS RECUPERADOS!"
        except Exception as e:
            print(f"ERRO AO CARREGAR: {e}")
            return None, "ARQUIVO CORROMPIDO"

    def _filtrar_lista(self, lista):
        """Remove superfícies do Pygame (imagens) que o pickle não aceita"""
        nova_lista = []
        for m in lista:
            # Mantém apenas o que é dicionário e filtra valores simples
            if isinstance(m, dict):
                m_limpo = {k: v for k, v in m.items() if isinstance(v, (int, float, str, bool, dict, list))}
                nova_lista.append(m_limpo)
        return nova_lista

    def desenhar_interface_slots(self, titulo_texto):
        """Interface visual de seleção de slots"""
        self.tela.fill(PRETO_ESPACO)
        
        # Título
        surf_t = self.fonte_titulo.render(titulo_texto, True, VIOLETA_SCANNER)
        self.tela.blit(surf_t, (LARGURA//2 - surf_t.get_width()//2, 50))
        
        for i in range(1, 4):
            y_pos = 150 + (i-1) * 120
            arq = os.path.join(self.diretorio_saves, f"save_slot_{i}.dat")
            existe = os.path.exists(arq)
            
            # Cores dinâmicas
            cor_box = VERDE_SISTEMA if existe else (60, 60, 60)
            
            # Caixa do Slot
            pygame.draw.rect(self.tela, (20, 20, 20), (150, y_pos, 600, 90), border_radius=10) # Fundo
            pygame.draw.rect(self.tela, cor_box, (150, y_pos, 600, 90), 2, border_radius=10) # Borda
            
            info = "--- SLOT DISPONÍVEL ---"
            if existe:
                try:
                    with open(arq, "rb") as f:
                        d = pickle.load(f)
                        info = f"OP: {d.get('nome_operador')} | CR: {d.get('creditos')} | CORES: {d.get('data_cores')}"
                except:
                    info = "ARQUIVO INCOMPATÍVEL"
            
            # Textos
            self.tela.blit(self.fonte_menu.render(f"SLOT 0{i}", True, cor_box), (180, y_pos + 15))
            self.tela.blit(self.fonte_pequena.render(info, True, (180, 180, 180)), (180, y_pos + 50))
        
        # Instrução de volta
        hint = self.fonte_pequena.render("[M] RETORNAR AO CENTRO DE COMANDO", True, AZUL_HUD)
        self.tela.blit(hint, (LARGURA//2 - hint.get_width()//2, 550))