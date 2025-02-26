import re

class RegrasAtivadas:

    def __init__(self, infoControlSystemSimulation): 
        self.infoControlSystemSimulation = infoControlSystemSimulation  # String de inf. de um ControlSystemSimulation
        self.numeros_regras = self._extrair_numeros_regras()
        self.graus_ativacao = self._extrair_graus_ativacao()

    def _extrair_numeros_regras(self):
        # Regex para encontrar os números das regras na String de saída
        return re.findall(r'RULE #(\d+):', self.infoControlSystemSimulation)

    def _extrair_graus_ativacao(self):
        # Regex para encontrar os graus de ativação na String de saída
        return re.findall(r'Activation\s*\(THEN-clause\):\s*[^:]*:\s*([0-9]*\.[0-9]+)', self.infoControlSystemSimulation)

    def obter_ativacoes(self):
        ativacoes = []
        for i, decimal in enumerate(self.graus_ativacao):
            if float(decimal) > 0.0:  # Exibe somente regras ativadas
                regra_numero = self.numeros_regras[i] if i < len(self.numeros_regras) else "N/A"
                ativacoes.append((regra_numero, decimal))
        return ativacoes

    def imprimir_ativacoes(self):
        ativacoes = self.obter_ativacoes()
        for regra_numero, decimal in ativacoes:
            print(f'Regra #{regra_numero}: Ativação = {decimal}')

    
