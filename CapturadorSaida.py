import io
import sys

class CapturadorSaida:

    def __init__(self, simulador):
        self.simulador = simulador

    def capturar_inf(self):
        with io.StringIO() as buffer:
            # Redireciona a saída padrão para o buffer
            sys.stdout = buffer
            self.simulador.print_state()
            sys.stdout = sys.__stdout__  # Restaura a saída padrão
            return buffer.getvalue()  # Retorna o valor capturado