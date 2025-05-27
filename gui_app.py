import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from email_reader import EmailReader
from resposta_generator import RespostaGenerator
from html_parser import HtmlParser
import pyperclip
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitura de E-mail e Cobmais")
        self.root.geometry("650x520")
        self.root.configure(bg="#f4f8fb")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=("Segoe UI", 11), padding=8, background="#14395B", foreground="white")
        style.map('TButton', background=[('active', '#1e5ba3')])
        style.configure('TLabel', font=("Segoe UI", 14, "bold"), background="#f4f8fb", foreground="#14395B")

        # Título
        ttk.Label(root, text="Automação Setor de Planejamento Estratégico - Leitura de E-mail", anchor="center").pack(pady=(18, 8))

        # Botões
        btn_frame = tk.Frame(root, bg="#f4f8fb")
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Ler E-mails", width=18, command=self.ler_emails).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text="Gerar Resposta", width=18, command=self.gerar_resposta).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text="Fechar", width=18, command=root.quit).pack(side=tk.LEFT, padx=8)

        # Campo de saída
        self.output = scrolledtext.ScrolledText(root, width=78, height=23, font=("Consolas", 11), bg="#eaf1fa", fg="#14395B", borderwidth=2, relief="groove")
        self.output.pack(padx=16, pady=12)
        self.html_content = None
        self.df = None

    def ler_emails(self):
        try:
            self.output.delete(1.0, tk.END)
            reader = EmailReader()
            SUBJECT_FILTER = "ENC: OUVIDORIA: EXCLUSÃO DE TELEFONES/ E-MAILS / SMS"
            html_content = reader.get_latest_relevant_email(SUBJECT_FILTER)
            if not html_content:
                self.output.insert(tk.END, "Nenhum e-mail relevante encontrado.\n")
                return
            self.html_content = html_content
            parser = HtmlParser()
            df = parser.extract_table(html_content)
            if df is None:
                self.output.insert(tk.END, "Não foi possível extrair a tabela do e-mail.\n")
                return
            self.df = df
            self.output.insert(tk.END, f"E-mail lido com sucesso! {len(df)} números encontrados.\n")
            self.output.insert(tk.END, f"Primeiros números extraídos:\n{df['numero'].head().to_string(index=False)}\n")
        except Exception as e:
            self.output.insert(tk.END, f"Erro ao ler e-mails: {e}\n")

    def gerar_resposta(self):
        try:
            if self.df is None:
                self.output.insert(tk.END, "Por favor, leia os e-mails primeiro.\n")
                return
            resposta = RespostaGenerator.gerar_resposta(self.df)
            pyperclip.copy(resposta)
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(resposta)
            self.output.insert(tk.END, "Resposta gerada, copiada para a área de transferência e salva em arquivo .html\n")
        except Exception as e:
            self.output.insert(tk.END, f"Erro ao gerar resposta: {e}\n")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
