import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RESET = Style.RESET_ALL

def banner():
    # Limpa a tela uma única vez aqui
    os.system('clear')
    print(ROXO + """
    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗ 
    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
    ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
    ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║   ██║
    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ 
    """)
    print(BRANCO + "Quem gostaria que eu conceda a visão, mestre CM_FX?\n")

def main():
    # Chama o banner logo de cara
    banner()
    
    while True:
        # Mostra as opções
        print(f"{ROXO}[1] Caçar Social [2] Rastrear IP [3] Ver Histórico [0] Sair")
        opt = input(f"{ROXO}>> ")
        
        if opt == '1':
            target = input(f"{ROXO}Username: ")
            # ... resto do código ...
            input("\n[!] Pressione Enter para voltar ao menu...")
            banner() # Limpa e redesenha o banner após a ação
            
        elif opt == '0':
            print(f"{ROXO}O Demônio fecha os olhos.")
            sys.exit()
