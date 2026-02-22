import customtkinter as ctk
import json
import secrets
import os
import requests # NOVO: Para conexão global
from datetime import datetime
from cryptography.fernet import Fernet

def carregar_chave():
    if not os.path.exists("secret.key"):
        chave = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(chave)
    return open("secret.key", "rb").read()

cipher_suite = Fernet(carregar_chave())

class FlyingFortressGlobal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FLYING FORTRESS - GLOBAL COMMAND")
        self.geometry("800x600")
        
        # URL DO SEU SERVIDOR (Ajustaremos quando subir para o Render)
        self.url_servidor = "https://flying-fortress-security.onrender.com"
        
        self.tabview = ctk.CTkTabview(self, width=750, height=550)
        self.tabview.pack(padx=20, pady=20)
        
        self.tab_recrutamento = self.tabview.add("CENTRO DE RECRUTAMENTO")
        self.tab_frota = self.tabview.add("MONITOR DE FROTA")
        
        self.setup_aba_recrutamento()
        self.setup_aba_frota()

    def setup_aba_recrutamento(self):
        self.lbl_title = ctk.CTkLabel(self.tab_recrutamento, text="SELECIONE A DOUTRINA", font=("Orbitron", 22, "bold"))
        self.lbl_title.pack(pady=20)

        self.doctrine_var = ctk.StringVar(value="RU")
        self.rb_ru = ctk.CTkRadioButton(self.tab_recrutamento, text="SUKHOI SU-57 (RF)", variable=self.doctrine_var, value="RU", command=self.mudar_cor, fg_color="#8B0000")
        self.rb_ru.pack(pady=5)
        
        self.rb_us = ctk.CTkRadioButton(self.tab_recrutamento, text="B-21 RAIDER (USA)", variable=self.doctrine_var, value="US", command=self.mudar_cor, fg_color="#1F538D")
        self.rb_us.pack(pady=5)

        self.name_entry = ctk.CTkEntry(self.tab_recrutamento, placeholder_text="NOME DO PILOTO", width=300)
        self.name_entry.pack(pady=30)

        self.btn_launch = ctk.CTkButton(self.tab_recrutamento, text="AUTORIZAR ACESSO GLOBAL", command=self.registrar_militar)
        self.btn_launch.pack(pady=10)
        self.mudar_cor()

    def setup_aba_frota(self):
        self.text_frota = ctk.CTkTextbox(self.tab_frota, width=650, height=400, font=("Consolas", 12))
        self.text_frota.pack(pady=10)
        self.btn_refresh = ctk.CTkButton(self.tab_frota, text="ATUALIZAR RADAR", command=self.atualizar_radar)
        self.btn_refresh.pack(pady=10)

    def mudar_cor(self):
        cor = "#8B0000" if self.doctrine_var.get() == "RU" else "#1F538D"
        self.lbl_title.configure(text_color=cor)
        self.btn_launch.configure(fg_color=cor)

    def registrar_militar(self):
        nome = self.name_entry.get()
        if not nome: return
        
        doutrina = "RU (Su-57)" if self.doctrine_var.get() == "RU" else "US (B-21)"
        id_piloto = f"FF-{self.doctrine_var.get()}-{secrets.token_hex(2).upper()}"
        dados = {"piloto": nome, "id": id_piloto, "doutrina": doutrina, "data": datetime.now().strftime("%H:%M:%S")}
        
        # 1. Registro Local (Blindado)
        cripto = cipher_suite.encrypt(json.dumps(dados).encode())
        with open("pilotos_encrypted.db", "ab") as f:
            f.write(cripto + b"\n")
        
        # 2. Transmissão Global (Tenta enviar para a Web)
        try:
            requests.post(self.url_servidor, json=dados, timeout=3)
            print(f"[TRANS] Piloto {nome} transmitido para a Torre de Comando.")
        except:
            print("[ALERTA] Servidor Offline. Registro salvo apenas em modo Stealth (Local).")

        self.name_entry.delete(0, 'end')
        self.atualizar_radar()

    def atualizar_radar(self):
        self.text_frota.delete("0.0", "end")
        if os.path.exists("pilotos_encrypted.db"):
            with open("pilotos_encrypted.db", "rb") as f:
                for linha in f:
                    if linha.strip():
                        try:
                            decrypted = cipher_suite.decrypt(linha)
                            reg = json.loads(decrypted)
                            info = f"[{reg['data']}] ID: {reg['id']} | PILOTO: {reg['piloto']} | DOUTRINA: {reg['doutrina']}\n"
                            self.text_frota.insert("end", info)
                        except: pass

if __name__ == "__main__":
    app = FlyingFortressGlobal()
    app.mainloop()

