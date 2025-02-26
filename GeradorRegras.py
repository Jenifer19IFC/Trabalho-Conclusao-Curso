import itertools

# Variáveis de entrada
variaveis = [
    'ansiedade', 'depressao', 'tea'
]

# Níveis
valores = ['leve', 'moderado', 'grave']

# Gera todas as combinações possíveis
combinacoes = itertools.product(valores, repeat=len(variaveis))

cont = 0
# Salva todas as combinações em um arquivo
with open('combinacoes_fuzzy.txt', 'w') as arquivo:
    for combinacao in combinacoes:
        # Cria a linha formatada 
        condicoes = " & ".join(f"{variavel}['{valor}']" for variavel, valor in zip(variaveis, combinacao))
        linha = f"self.regras.append(ctrl.Rule({condicoes}, self.ansiedade['leve']))"

        cont += 1
        arquivo.write(linha + "\n")

print("Todas as", cont, "combinações foram salvas no arquivo 'combinacoes_fuzzy.txt'.")


# Qtd. de níveis ELEVADO à qtd. de variáveis

