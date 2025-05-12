import os
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from backend import carregar_dados_csv, gerar_resposta

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mecânico Inteligente")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f")

        self.mensagens = []
        self.documento_csv = carregar_dados_csv()

        # --- Cabeçalho com logo ---
        header_frame = tk.Frame(root, bg="#1e1e2f")
        header_frame.pack(pady=10, fill=tk.X)

        caminho_logo = os.path.join(os.path.dirname(__file__), "img", "logo.png")

        try:
            if os.path.exists(caminho_logo):
                imagem = Image.open(caminho_logo)
                imagem = imagem.resize((100, 100), Image.ANTIALIAS)
                self.logo = ImageTk.PhotoImage(imagem)
                tk.Label(header_frame, image=self.logo, bg="#1e1e2f").pack()
            else:
                raise FileNotFoundError("logo.png não encontrado na pasta Docs.")
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            tk.Label(header_frame, text="Buscador de Filtros", font=("Segoe UI", 20), bg="#1e1e2f", fg="white").pack()

        # --- Frame principal da interface ---
        main_frame = tk.Frame(root, bg="#1e1e2f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Área de texto (chat) com estilo mais suave ---
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            bg="#2e2e3e",
            fg="white",
            font=("Segoe UI", 12),
            height=20,
            bd=0,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_area.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.chat_area.config(state=tk.DISABLED)

        # --- Frame de entrada ---
        bottom_frame = tk.Frame(root, bg="#1e1e2f")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(10, 10))

        self.entry = tk.Entry(bottom_frame, font=("Segoe UI", 12), bg="#3e3e4e", fg="white", insertbackground="white", relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.enviar_pergunta)

        self.send_button = tk.Button(bottom_frame, text="Enviar", font=("Segoe UI", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, command=self.enviar_pergunta)
        self.send_button.pack(side=tk.RIGHT)

        self.exibir_mensagem("Bot", "  Olá! Meu nomé é Guru dos filtros, seu melhor assistente para identificar filtros. Me pergunte sobre modelos de carros e seus filtros. Digite 'x' para sair.")
        self.exibir_mensagem("Bot", "Por favor ao inserir uma pergunta tente ser claro e objetivo pois ainda estou aprendendo sobre a línguagem humana")

    def exibir_mensagem(self, remetente, texto):
        self.chat_area.config(state=tk.NORMAL)
        if remetente == "Bot":
            remetente += " 🔧"
        self.chat_area.insert(tk.END, f"{remetente}: {texto}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def enviar_pergunta(self, event=None):
        pergunta = self.entry.get().strip()
        if not pergunta:
            return

        self.exibir_mensagem("Você", pergunta)
        self.entry.delete(0, tk.END)

        if pergunta.lower() == 'x':
            self.root.quit()
            return

        self.mensagens.append(("user", pergunta))
        resposta = gerar_resposta(self.mensagens, self.documento_csv)
        self.mensagens.append(("assistant", resposta))
        self.exibir_mensagem("Bot", resposta)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()