import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap import ttk

class RegrasAtivadasWindow:

    def __init__(self, master, regras_ativadas, theme="flatly"):
        self.style = Style(theme=theme) 
        self.regras_ativadas = regras_ativadas
        self.window = tk.Toplevel(master)
        self.window.title("Regras Ativadas")
        self.window.geometry('400x300')
        self.cria_treeview()

    def cria_treeview(self):
        # Exibe regras em formato de grid
        tree = ttk.Treeview(self.window, columns=("regra", "grau"), show="headings")
        tree.heading("regra", text="Número da Regra")
        tree.heading("grau", text="Grau de Ativação")
        tree.column("regra", anchor="center", width=150)
        tree.column("grau", anchor="center", width=150)
        
        # Insere as regras no Treeview, formatando o grau em duas casas decimais
        for regra, grau in self.regras_ativadas:
            tree.insert("", "end", values=(regra, f"{grau:.2f}"))
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)
