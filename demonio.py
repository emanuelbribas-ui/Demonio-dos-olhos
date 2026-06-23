import requests
import threading
import json
import os
import time
import sqlite3
import sys
from colorama import Fore, Style, init

# Inicialização
init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RESET = Style.RESET_ALL

# --- BANCO DE DADOS FATAL ---
def init_db():
    conn = sqlite3.connect('demonio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (target TEXT, tipo TEXT, info TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_data(target, tipo, info):
    conn = sqlite3.connect('demonio.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (target, tipo, info) VALUES (?, ?, ?)", (target, tipo, info))
    conn.commit()
    conn.close()

# --- MÓDULO DE BUSCA SOCIAL (Multithreaded) ---
class SocialHunter:
    def __init__(self, target):
        self.target = target
        self.sites = {
            "Github": "https://github.com/{}",
            "Twitter": "https://twitter.com/{}",
            "Instagram": "https://www.instagram.com/{}",
            "TikTok": "https://tiktok.com/@{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}"
        }

    def check(self, name, url):
        full_url = url.format(self.target)
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code == 200:
                print(f"{ROXO}[+] {name} ENCONTRADO: {full_url}")
                log_data(self.target, "Social", full_url)
        except: pass

    def hunt(self):
        threads = []
        for name, url in self.sites.items():
            t = threading.Thread(target=self.check, args=(name, url))
            threads.append(t)
            t.start()
        for t in threads: t.join()

# --- MÓDULO DE EXTRAÇÃO GEO ---
def geo_track(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()
        if data['status'] == 'success':
            res = f"Pais: {data['country']} | Cidade: {data['city']} | ISP: {data['isp']}"
            print(f"{ROXO}[!] {res}")
            log_data(ip, "GEO", res)
    except: print(f"{Fore.RED}Erro no rastreio.")

# --- ENGINE PRINCIPAL ---
def banner():
    print(ROXO + "█▀▄ █▀▀ █▀▄▀█ █▀█ █▄ █ █ █▀█   █▀▄ █▀█ █▀   █▀█ █   █▀█ █   █▀▀ █▀▀")
    print(ROXO + "█ █ █▀▀ █ ▀ █ █ █ █ ▀█ █ █ █ █   █ █ █ █ █▀  █ █ █   █ █ █   █▀▀ ▀▀█")
    print(ROXO + "▀▀  ▀▀▀ ▀   ▀ ▀▀▀ ▀  ▀ ▀ ▀ ▀ ▀   ▀▀  ▀▀▀ ▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀")
    print(BRANCO + "--- MODO FATAL ATIVADO ---")

def main():
    init_db()
    while True:
        banner()
        print(f"\n{ROXO}[1] Caçar Social [2] Rastrear IP [3] Ver Histórico [0] Sair")
        opt = input(">> ")
        
        if opt == '1':
            target = input("Username: ")
            hunter = SocialHunter(target)
            hunter.hunt()
        elif opt == '2':
            ip = input("IP: ")
            geo_track(ip)
        elif opt == '3':
            conn = sqlite3.connect('demonio.db')
            for row in conn.execute("SELECT * FROM logs"):
                print(row)
            conn.close()
        elif opt == '0':
            break
        
        input("\n[!] Enter para continuar...")

if __name__ == "__main__":
    main()
