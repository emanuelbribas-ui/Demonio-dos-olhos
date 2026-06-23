import os
import sys
import time
import sqlite3
import threading
import requests
from colorama import Fore, Style, init

# --- CONFIGURAÇÃO INICIAL ---
init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RESET = Style.RESET_ALL
DB_NAME = "demonio.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (id INTEGER PRIMARY KEY, alvo TEXT, tipo TEXT, info TEXT)''')
    conn.commit()
    conn.close()

def salvar_log(alvo, tipo, info):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (alvo, tipo, info) VALUES (?, ?, ?)", (alvo, tipo, info))
    conn.commit()
    conn.close()

# --- MODULOS DE ATAQUE ---

class SocialEngine:
    def __init__(self, target):
        self.target = target
        self.sites = [
            "https://github.com/{}", "https://twitter.com/{}", 
            "https://instagram.com/{}", "https://tiktok.com/@{}",
            "https://reddit.com/user/{}", "https://twitch.tv/{}",
            "https://behance.net/{}", "https://vk.com/{}"
        ]

    def scan(self):
        print(f"{ROXO}[!] Iniciando varredura social para: {self.target}")
        for url_base in self.sites:
            url = url_base.format(self.target)
            try:
                response = requests.get(url, timeout=4)
                if response.status_code == 200:
                    print(f"{ROXO}[+] ENCONTRADO: {url}")
                    salvar_log(self.target, "SOCIAL", url)
            except: pass

class GeoEngine:
    @staticmethod
    def rastrear(ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            if data['status'] == 'success':
                info = f"{data['country']} - {data['city']} - {data['isp']}"
                print(f"{ROXO}[!] DADOS GEO: {info}")
                salvar_log(ip, "GEO", info)
        except: print(f"{ROXO}[-] Erro na conexão.")

class DorkEngine:
    """Motor que busca vestígios em documentos públicos"""
    def __init__(self, target):
        self.target = target
        self.dorks = [
            'filetype:pdf "{}"', 'filetype:xls "{}"',
            'intext:"{}" "senha"', 'site:pastebin.com "{}"'
        ]
    
    def run(self):
        print(f"{ROXO}[!] Executando motor de Dorks para: {self.target}")
        for dork in self.dorks:
            query = dork.format(self.target)
            print(f"{ROXO}[...] Consultando: {query}")
            time.sleep(1.5) # Delay para evitar bloqueio

# --- INTERFACE ---

def mostrar_banner():
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
    init_db()
    os.system('clear')
    mostrar_banner()
    
    while True:
        print(f"\n{ROXO}1. Caça Social | 2. Rastreio Geo | 3. Motor de Dorks | 4. Histórico | 0. Sair")
        escolha = input(f"{ROXO}>> ")
        
        if escolha == '1':
            target = input("Username: ")
            engine = SocialEngine(target)
            engine.scan()
        elif escolha == '2':
            ip = input("IP Alvo: ")
            GeoEngine.rastrear(ip)
        elif escolha == '3':
            target = input("Alvo para Dorks: ")
            d = DorkEngine(target)
            d.run()
        elif escolha == '4':
            conn = sqlite3.connect(DB_NAME)
            for row in conn.execute("SELECT * FROM logs"):
                print(row)
            conn.close()
        elif escolha == '0':
            print("O Demônio encerra a sessão.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
