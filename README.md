# VOID-Roguelite
V.O.I.D. é um jogo tático de sobrevivência e gerenciamento em estilo roguelite desenvolvido do zero em Python. O jogador assume o controle de uma Estação Orbital, gerenciando recursos, recrutando unidades e participando de uma liga competitiva com mecânicas de combate por turnos.

Nota sobre os Assets:
Por questões de performance e tamanho do repositório (mais de 100MB de artes), os arquivos de imagem e som originais não foram incluídos neste upload. O objetivo deste repositório é demonstrar a arquitetura do motor de jogo, o sistema de combate por turnos e a lógica de gerenciamento de ligas desenvolvida em Python.

Arquitetura Modular: Código estruturado em múltiplos sistemas independentes (Lojas, Hangar, Motor de Batalha, Interface, liga de monstro com tabelas, artilharia, calendário e sistema de descida e subida de divisão), facilitando a manutenção e expansão.

Motor de Combate Customizado: Sistema de batalha por turnos (engine.py) com cálculo de danos, vantagens de tribos, ataques especiais e eventos climáticos dinâmicos.

Sistema de Ligas e Torneios: Gerenciamento de campeonato em divisões, com tabelas de classificação, artilharia e simulação de batalhas em background (liga.py).

Gerenciamento de Progressão: Sistema de Save/Load estruturado e manipulação de DNA (sistema Brind) para fortalecimento contínuo das unidades.


Python: Lógica principal, Orientação a Objetos e manipulação de dicionários/dados.

Pygame: Renderização gráfica, controle de FPS e captura de eventos do teclado/mouse.
