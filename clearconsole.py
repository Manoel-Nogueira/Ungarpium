import os
import sys

# Função para limpar a tela
def ClearConsole():

    if sys.platform.startswith('win'):

        os.system('cls')

    else:

        os.system('clear')
        
        