from doctest import master
import logging
import tkinter as tk
from tkinter import Label, PhotoImage, ttk
from tkinter import messagebox
import ttkbootstrap as ttkb 
from LogicaFuzzy import LogicaFuzzy

# Configuração do log
logging.basicConfig(
    filename='logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

class App:

    def __init__(self, master, theme="flatly"):
        self.style = ttkb.Style(theme=theme)
        self.master = master
        self.regras_ativadas = None
        self.logica_fuzzy = LogicaFuzzy()
        self.cria_widgets()

    def cria_widgets(self):
        self.master.title("Diagnóstico de Transtornos Mentais")
        self.master.geometry('700x650')

        # Imagem de fundo ----------------------------------------
        logo_image = PhotoImage(file="./img/img_.png")
        logo_image = logo_image.subsample(3, 3) # Tamanho

        # Label para fundo
        logo_label = Label(self.master, image=logo_image)
        logo_label.image = logo_image  
        logo_label.place(x=10, y=10) 
        # Imagem de fundo [End] ----------------------------------------

        # Configuração das colunas 
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.cria_campos()
        self.cria_campos_resultados()

    def cria_campos(self):

        def atualiza_valor(valor, var_label):
            var_label.set(f"{float(valor):.1f}")

       # Anedonia - Cria um frame para sintoma 
        anedonia_frame = ttk.Frame(self.master)
        anedonia_frame.grid(row=0, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.anedonia_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Anedonia").grid(row=0, column=0, sticky="e")

        self.anedonia_slider = ttkb.Scale(
            anedonia_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.anedonia_valor)
        )
        self.anedonia_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(anedonia_frame, textvariable=self.anedonia_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5)) # Valor slider
        # --------------------

        # Humor deprimido
        humor_deprimido_frame = ttk.Frame(self.master)
        humor_deprimido_frame.grid(row=1, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.humor_deprimido_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Humor deprimido").grid(row=1, column=0, sticky="e")

        self.humor_deprimido_slider = ttkb.Scale(
            humor_deprimido_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.humor_deprimido_valor)
        )
        self.humor_deprimido_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(humor_deprimido_frame, textvariable=self.humor_deprimido_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Alteração no padrão do sono
        alteracao_sono_frame = ttk.Frame(self.master)
        alteracao_sono_frame.grid(row=2, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.alteracao_sono_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Alteração no padrão do sono").grid(row=2, column=0, sticky="e")

        self.alteracao_sono_slider = ttkb.Scale(
            alteracao_sono_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.alteracao_sono_valor)
        )
        self.alteracao_sono_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(alteracao_sono_frame, textvariable=self.alteracao_sono_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Pensamentos de morte
        morte_frame = ttk.Frame(self.master)
        morte_frame.grid(row=3, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.morte_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Pensamentos de morte").grid(row=3, column=0, sticky="e")

        self.morte_slider = ttkb.Scale(
            morte_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.morte_valor)
        )
        self.morte_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(morte_frame, textvariable=self.morte_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Rigidez cognitiva
        rigidez_cog_frame = ttk.Frame(self.master)
        rigidez_cog_frame.grid(row=4, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.rigidez_cog_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Rigidez cognitiva").grid(row=4, column=0, sticky="e")

        self.rigidez_cog_slider = ttkb.Scale(
            rigidez_cog_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.rigidez_cog_valor)
        )
        self.rigidez_cog_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(rigidez_cog_frame, textvariable=self.rigidez_cog_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Medo    
        medo_frame = ttk.Frame(self.master)
        medo_frame.grid(row=5, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.medo_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Medo").grid(row=5, column=0, sticky="e")

        self.medo_slider = ttkb.Scale(
            medo_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.medo_valor)
        )
        self.medo_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(medo_frame, textvariable=self.medo_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Preocupação excessiva
        preoc_exc_frame = ttk.Frame(self.master)
        preoc_exc_frame.grid(row=6, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.preoc_exc_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Preocupação excessiva").grid(row=6, column=0, sticky="e")

        self.preoc_exc_slider = ttkb.Scale(
            preoc_exc_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.preoc_exc_valor)
        )
        self.preoc_exc_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(preoc_exc_frame, textvariable=self.preoc_exc_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Comportamentos estereotipados
        comport_est_frame = ttk.Frame(self.master)
        comport_est_frame.grid(row=7, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.comport_est_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Comportamentos estereotipados").grid(row=7, column=0, sticky="e")

        self.comport_est_slider = ttkb.Scale(
            comport_est_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.comport_est_valor)
        )
        self.comport_est_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(comport_est_frame, textvariable=self.comport_est_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Dificuldade de interação social
        dif_inte_soc_frame = ttk.Frame(self.master)
        dif_inte_soc_frame.grid(row=8, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.dif_inte_soc_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Dificuldade de interação social").grid(row=8, column=0, sticky="e")

        self.dif_inte_soc_slider = ttkb.Scale(
            dif_inte_soc_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.dif_inte_soc_valor)
        )
        self.dif_inte_soc_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(dif_inte_soc_frame, textvariable=self.dif_inte_soc_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Doença(s) pré-existente(s)
        doenca_pre_existente_frame = ttk.Frame(self.master)
        doenca_pre_existente_frame.grid(row=9, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.doenca_pre_existente_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Possui doença(s) pré-existente(s)?").grid(row=9, column=0, sticky="e")

        self.doenca_pre_existente_slider = ttkb.Scale(
            doenca_pre_existente_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.doenca_pre_existente_valor)
        )
        self.doenca_pre_existente_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(doenca_pre_existente_frame, textvariable=self.doenca_pre_existente_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Sintomas presentes na maior parte do tempo
        sint_present_frame = ttk.Frame(self.master)
        sint_present_frame.grid(row=10, column=1, sticky="w", padx=(15, 5), pady=(2, 2))

        self.sint_present_valor = tk.StringVar(value="0.0")
        ttk.Label(self.master, text="Sintomas presentes na maior parte do tempo").grid(row=10, column=0, sticky="e")

        self.sint_present_slider = ttkb.Scale(
            sint_present_frame, from_=0, to=5, orient="horizontal", bootstyle="info",
            command=lambda valor: atualiza_valor(valor, self.sint_present_valor)
        )
        self.sint_present_slider.grid(row=0, column=0, sticky="w")
        ttk.Label(sint_present_frame, textvariable=self.sint_present_valor).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        # --------------------

        # Combo para tempo dos sintomass
        ttk.Label(self.master, text="Período com sintomas presentes").grid(row=11, column=0, sticky="e")
        self.seman_combobox = ttk.Combobox(self.master, bootstyle="info", values=["2 semanas ou mais", "6 meses ou mais", "Desde a infância"], state="readonly", width=15)
        self.seman_combobox.grid(row=11, column=1, sticky="w", padx=(15, 10), pady=(10, 10))
        self.seman_combobox.current(0)

        # Botões:
        ttk.Button(self.master, text="Consultar Diagnóstico", command=self.consultar_diagnostico, bootstyle="warning").grid(row=12, column=0, sticky="e", padx=(15, 5), pady=(15, 20))

        # Estilo personalizado para o botão abaixo
        self.style.configure("BluePastel.TButton", 
                            background="#0D9AC2",  # Fundo azul pastel
                            foreground="white",
                            bordercolor="#0D9AC2",  # Borda azul pastel
                            relief="solid")  # Estilo da borda mais discreto

        ttk.Button(self.master, text="Exibir Regras Ativadas", command=self.exibir_regras_ativadas, style="BluePastel.TButton").grid(row=12, column=1, sticky="w", padx=(5, 15), pady=(15, 20))

        ttk.Button(self.master, text="Limpar", command=self.limpar_campos, bootstyle="danger").place(x=680, y=10, anchor=tk.NE)

    def cria_campos_resultados(self):
        # Cria um Frame
        self.result_frame = ttk.Frame(self.master, padding=10, relief="solid", borderwidth=1)
        self.result_frame.grid(row=14, column=0, columnspan=2, padx=15, pady=10, sticky="nsew")

        self.result_depressao = tk.StringVar()
        self.result_ansiedade = tk.StringVar()
        self.result_tea = tk.StringVar()

        ttk.Label(self.result_frame, text="Resultado do diagnóstico:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(self.result_frame, textvariable=self.result_depressao).grid(row=1, column=0, sticky="w")
        ttk.Label(self.result_frame, textvariable=self.result_ansiedade).grid(row=2, column=0, sticky="w")
        ttk.Label(self.result_frame, textvariable=self.result_tea).grid(row=3, column=0, sticky="w")


    def consultar_diagnostico(self):
        entradas = {
            'anedonia': self.anedonia_slider.get(),
            'humor_deprimido': self.humor_deprimido_slider.get(),
            'alteracao_sono': self.alteracao_sono_slider.get(),
            'morte': self.morte_slider.get(),
            'rigidez_cog': self.rigidez_cog_slider.get(),
            'medo': self.medo_slider.get(),
            'preoc_exc': self.preoc_exc_slider.get(),
            'comport_est': self.comport_est_slider.get(),
            'dif_inte_soc': self.dif_inte_soc_slider.get(),
            'doenca_pre_existente': self.doenca_pre_existente_slider.get(),
            'sint_present_maior': self.sint_present_slider.get(),
            'seman_sint_present': self.direciona_valor(),
        }

        try:
            diagnosis = self.logica_fuzzy.calcula_diagnostico(entradas)
            self.regras_ativadas = self.logica_fuzzy.ativacoes()

            # Atualiza valores resultados
            self.result_depressao.set(f"Depressão: {diagnosis['depressao']:.2f}/10")
            self.result_ansiedade.set(f"Ansiedade: {diagnosis['ansiedade']:.2f}/10")
            self.result_tea.set(f"TEA: {diagnosis['tea']:.2f}/10")

            print("\nVALORES DE ENTRADA:")
            for chave, valor in entradas.items():
                print(f"{chave}: {valor}")

        except KeyError as e:
            self.grava_log_erro(entradas)
            messagebox.showwarning(
                title="Atenção",
                message=f"Não existem regras cadastradas para as entradas fornecidas."
            )


    def direciona_valor(self):
        valores = ["2 semanas ou mais", "6 meses ou mais", "Desde a infância"]
        opc = valores.index(self.seman_combobox.get()) + 1
        if opc == 1: 
            return opc # 1 eq. a 2 semanas - BAIXO
        if opc == 2: 
            return 3 # 6 meses - MÉDIO
        if opc == 3:
            return 5 # Desde a infância - ALTO
        return opc 
    
    def exibir_regras_ativadas(self):
        # Verifica se tem regras ativadas
        if not self.regras_ativadas:
            messagebox.showinfo(
                title="Atenção",
                message="Para exibir as regras ativadas, é necessário realizar um diagnóstico primeiro.\n\n"
                        "Por favor, consulte o diagnóstico e tente novamente."
            )
            return

        # Exibe as regras em grid
        regras_window = tk.Toplevel(self.master)
        regras_window.title("Regras Ativadas")
        regras_window.geometry('400x300')
        
        tree = ttk.Treeview(regras_window, columns=("regra", "grau"), show="headings")
        tree.heading("regra", text="Número da Regra")
        tree.heading("grau", text="Grau de Ativação")
        tree.column("regra", anchor="center", width=150)
        tree.column("grau", anchor="center", width=100)
        
        # Insere as regras no Treeview formatadas
        for regra, grau in self.regras_ativadas:
            grau_formatado = self.formata_grau_at(grau)
            tree.insert("", "end", values=(regra, grau_formatado))
        
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        regras_window.grab_set() 

    # Formata grau de ativação para duas duas casas decimais
    def formata_grau_at(self, valor):
        try:
            if isinstance(valor, (int, float)):
                return f"{float(valor):.2f}"
            elif isinstance(valor, str):
                try:
                    return f"{float(valor):.2f}"
                except ValueError:
                    return valor
            else:
                return str(valor)
        except Exception as e:
            print(f"Erro ao formatar o grau de ativação: {str(e)}")
            return "Erro"

    def grava_log_erro(self, entradas):
        entradas_formatadas = []
        linha = f"TESTES | "
        linha += "[Entradas => "
        for chave, valor in entradas.items():
            entradas_formatadas.append(f"{chave}: {round(valor, 2):.2f}, ")
        
        # Remove a última vírgula e espaço
        entradas_formatadas[-1] = entradas_formatadas[-1].rstrip(', ')
        
        linha += ''.join(entradas_formatadas) + "] [Saída => REGRAS NÃO COMPUTADAS PARA AS ENTRADAS]"
        logging.info(linha)

    def limpar_campos(self):
        # Limpa sliders
        self.anedonia_slider.set(0)
        self.humor_deprimido_slider.set(0)
        self.alteracao_sono_slider.set(0)
        self.morte_slider.set(0)
        self.rigidez_cog_slider.set(0)
        self.medo_slider.set(0)
        self.preoc_exc_slider.set(0)
        self.comport_est_slider.set(0)
        self.dif_inte_soc_slider.set(0)
        self.doenca_pre_existente_slider.set(0)
        self.sint_present_slider.set(0)

        # Limpa resultados
        self.seman_combobox.current(0)
        self.result_depressao.set("")
        self.result_ansiedade.set("")
        self.result_tea.set("")

  