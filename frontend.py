import os
import customtkinter as ctk
from PIL import Image
from backend import carregar_dados_csv, gerar_resposta

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ChatBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guru dos Filtros")
        self.geometry("900x700")
        self.configure(bg="#f2f2f2")

        # Ícone da janela
        icon_path = os.path.join(os.path.dirname(__file__), "img", "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                print(f"Erro ao carregar o ícone: {e}")

        self.mensagens = []
        self.documento_csv = carregar_dados_csv()

        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=15)
        header.pack(pady=15, padx=15, fill="x")

        # Logo com CTkImage (HighDPI seguro)
        logo_path = os.path.join(os.path.dirname(__file__), "img", "logo.png")
        if os.path.exists(logo_path):
            pil_img = Image.open(logo_path).resize((80, 80))
            self.logo = ctk.CTkImage(light_image=pil_img, size=(80, 80))
            logo_label = ctk.CTkLabel(header, image=self.logo, text="")
            logo_label.pack(side="left", padx=20, pady=10)

        # Título e slogan
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", padx=10)
        ctk.CTkLabel(text_frame, text="Guru dos Filtros", font=("Segoe UI", 26, "bold"), text_color="#ffffff").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="O parceiro certo na hora de escolher filtros automotivos.", font=("Segoe UI", 14), text_color="#cbd5e1").pack(anchor="w")

        # Área do chat
        chat_frame = ctk.CTkFrame(self, fg_color="#f4f4f4", corner_radius=15)
        chat_frame.pack(padx=20, pady=(10, 0), fill="both", expand=True)

        self.chat_area = ctk.CTkTextbox(chat_frame, font=("Segoe UI", 13), text_color="#000000", wrap="word", state="disabled", corner_radius=10, fg_color="white")
        self.chat_area.pack(padx=15, pady=15, fill="both", expand=True)

        # Tags para estilo das mensagens
        self.chat_area.tag_config("Bot", foreground="#2563eb")
        self.chat_area.tag_config("Usuário", foreground="#10b981")
        self.chat_area.tag_config("mensagem", spacing3=5)

        # Entrada do usuário
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(padx=20, pady=20, fill="x")

        self.entry = ctk.CTkEntry(bottom_frame, placeholder_text="Digite sua pergunta...", font=("Segoe UI", 13), fg_color="#e2e8f0", text_color="#1e293b")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.enviar_pergunta)

        self.send_button = ctk.CTkButton(bottom_frame, text="Enviar", command=self.enviar_pergunta, fg_color="#2563eb", hover_color="#1d4ed8")
        self.send_button.pack(side="right")

        self.exibir_mensagem("Bot", "Olá! Eu sou o Guru, seu especialista em filtros automotivos. Me pergunte sobre modelos de carros e quais filtros usar.\nDigite 'x' para sair.")

    def exibir_mensagem(self, remetente, texto):
        self.chat_area.configure(state="normal")
        tag = "Bot" if remetente.lower() == "Bot" else "Usuário"

        self.chat_area.insert("end", f"{remetente}: ", tag)
        self.chat_area.insert("end", f"{texto}\n\n", "mensagem")

        self.chat_area.configure(state="disabled")
        self.chat_area.yview_moveto(1.0)

    def enviar_pergunta(self, event=None):
        pergunta = self.entry.get().strip()
        if not pergunta:
            return

        self.exibir_mensagem("Usuário", pergunta)
        self.entry.delete(0, "end")

        if pergunta.lower() == 'x':
            self.destroy()
            return

        self.mensagens.append(("user", pergunta))
        resposta = gerar_resposta(self.mensagens, self.documento_csv)
        self.mensagens.append(("assistant", resposta))
        self.exibir_mensagem("Bot", resposta)


if __name__ == "__main__":
    app = ChatBotGUI()
    app.mainloop()
