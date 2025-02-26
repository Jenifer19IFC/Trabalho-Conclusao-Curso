import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from CapturadorSaida import CapturadorSaida
from RegrasAtivadas import RegrasAtivadas
import logging

# Configuração do log
logging.basicConfig(
    filename='logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

class LogicaFuzzy:
    
    def __init__(self):
        self.define_variaveis()
        self.define_funcoes_pertinencia()
        self.define_regras()
        self.diagnostico_ctrl = ctrl.ControlSystem(self.regras)
        self.diagnostico_simulador = ctrl.ControlSystemSimulation(self.diagnostico_ctrl)

    def define_variaveis(self):
         # Variáveis de entrada
        self.anedonia = ctrl.Antecedent(np.arange(0, 6, 1), 'anedonia') # Anedonia (perda de interesses)
        self.seman_sint_present = ctrl.Antecedent(np.arange(0, 6, 1), 'seman_sint_present') # Período com sintomas presentes
        self.sint_present_maior = ctrl.Antecedent(np.arange(0, 6, 1), 'sint_present_maior') # Sintomas presentes na maior parte do tempo
        self.humor_deprimido = ctrl.Antecedent(np.arange(0, 6, 1), 'humor_deprimido') # Humor deprimido
        self.alteracao_sono = ctrl.Antecedent(np.arange(0, 6, 1), 'alteracao_sono') # Alteração no padrão do sono
        self.morte = ctrl.Antecedent(np.arange(0, 6, 1), 'morte') # Pensamentos de morte
        self.rigidez_cog = ctrl.Antecedent(np.arange(0, 6, 1), 'rigidez_cog') # Rigidez cognitiva
        self.medo = ctrl.Antecedent(np.arange(0, 6, 1), 'medo') # Medo
        self.preoc_exc = ctrl.Antecedent(np.arange(0, 6, 1), 'preoc_exc') # Preocupação excessiva
        self.comport_est = ctrl.Antecedent(np.arange(0, 6, 1), 'comport_est') # Comportamentos estereotipados
        self.dif_inte_soc = ctrl.Antecedent(np.arange(0, 6, 1), 'dif_inte_soc') # Dificuldade na interação social
        self.doenca_pre_existente = ctrl.Antecedent(np.arange(0, 6, 1), 'doenca_pre_existente') # Possui doença(a) pré-existente(s)?

        # Variáveis de saída
        self.depressao = ctrl.Consequent(np.arange(0, 11, 1), 'depressao')
        self.ansiedade = ctrl.Consequent(np.arange(0, 11, 1), 'ansiedade')
        self.tea = ctrl.Consequent(np.arange(0, 11, 1), 'tea')

    def define_funcoes_pertinencia(self):
        # Entrada
        self.seman_sint_present['baixo'] = fuzz.trapmf(self.seman_sint_present.universe, [0, 0, 1, 2])
        self.seman_sint_present['medio'] = fuzz.trapmf(self.seman_sint_present.universe, [1, 2, 3, 4])
        self.seman_sint_present['alto'] = fuzz.trapmf(self.seman_sint_present.universe, [3, 4, 6, 6])

        self.sint_present_maior['baixo'] = fuzz.trapmf(self.sint_present_maior.universe, [0, 0, 1, 2])
        self.sint_present_maior['medio'] = fuzz.trapmf(self.sint_present_maior.universe, [1, 2, 3, 4])
        self.sint_present_maior['alto'] = fuzz.trapmf(self.sint_present_maior.universe, [3, 4, 6, 6])

        self.anedonia['baixo'] = fuzz.trapmf(self.anedonia.universe, [0, 0, 1, 2])
        self.anedonia['medio'] = fuzz.trapmf(self.anedonia.universe, [1, 2, 3, 4])
        self.anedonia['alto'] = fuzz.trapmf(self.anedonia.universe, [3, 4, 6, 6])

        self.humor_deprimido['baixo'] = fuzz.trapmf(self.humor_deprimido.universe, [0, 0, 1, 2])
        self.humor_deprimido['medio'] = fuzz.trapmf(self.humor_deprimido.universe, [1, 2, 3, 4])  
        self.humor_deprimido['alto'] = fuzz.trapmf(self.humor_deprimido.universe, [3, 4, 6, 6])

        self.alteracao_sono['baixo'] = fuzz.trapmf(self.alteracao_sono.universe, [0, 0, 1, 2])
        self.alteracao_sono['medio'] = fuzz.trapmf(self.alteracao_sono.universe, [1, 2, 3, 4])
        self.alteracao_sono['alto'] = fuzz.trapmf(self.alteracao_sono.universe, [3, 4, 6, 6])

        self.medo['baixo'] = fuzz.trapmf(self.medo.universe, [0, 0, 1, 2])
        self.medo['medio'] = fuzz.trapmf(self.medo.universe, [1, 2, 3, 4])
        self.medo['alto'] = fuzz.trapmf(self.medo.universe, [3, 4, 6, 6])

        self.preoc_exc['baixo'] = fuzz.trapmf(self.preoc_exc.universe, [0, 0, 1, 2])
        self.preoc_exc['medio'] = fuzz.trapmf(self.preoc_exc.universe, [1, 2, 3, 4])
        self.preoc_exc['alto'] = fuzz.trapmf(self.preoc_exc.universe, [3, 4, 6, 6])

        self.comport_est['baixo'] = fuzz.trapmf(self.comport_est.universe, [0, 0, 1, 2])
        self.comport_est['medio'] = fuzz.trapmf(self.comport_est.universe, [1, 2, 3, 4])
        self.comport_est['alto'] = fuzz.trapmf(self.comport_est.universe, [3, 4, 6, 6])

        self.dif_inte_soc['baixo'] = fuzz.trapmf(self.dif_inte_soc.universe, [0, 0, 1, 2])
        self.dif_inte_soc['medio'] = fuzz.trapmf(self.dif_inte_soc.universe, [1, 2, 3, 4])
        self.dif_inte_soc['alto'] = fuzz.trapmf(self.dif_inte_soc.universe, [3, 4, 6, 6])

        self.morte['baixo'] = fuzz.trapmf(self.morte.universe, [0, 0, 1, 2])
        self.morte['medio'] = fuzz.trapmf(self.morte.universe, [1, 2, 3, 4])
        self.morte['alto'] = fuzz.trapmf(self.morte.universe, [3, 4, 6, 6])

        self.rigidez_cog['baixo'] = fuzz.trapmf(self.rigidez_cog.universe, [0, 0, 1, 2])
        self.rigidez_cog['medio'] = fuzz.trapmf(self.rigidez_cog.universe, [1, 2, 3, 4])
        self.rigidez_cog['alto'] = fuzz.trapmf(self.rigidez_cog.universe, [3, 4, 6, 6])

        self.doenca_pre_existente['baixo'] = fuzz.trapmf(self.doenca_pre_existente.universe, [0, 0, 1, 2])
        self.doenca_pre_existente['medio'] = fuzz.trapmf(self.doenca_pre_existente.universe, [1, 2, 3, 4])
        self.doenca_pre_existente['alto'] = fuzz.trapmf(self.doenca_pre_existente.universe, [3, 4, 6, 6])

        # Saída
        self.depressao['leve'] = fuzz.trapmf(self.depressao.universe, [0, 0, 2, 4])
        self.depressao['moderado'] = fuzz.trapmf(self.depressao.universe, [2, 4, 6, 8])
        self.depressao['grave'] = fuzz.trapmf(self.depressao.universe,  [6, 8, 10, 10])

        self.ansiedade['leve'] = fuzz.trapmf(self.ansiedade.universe, [0, 0, 2, 4])
        self.ansiedade['moderado'] = fuzz.trapmf(self.ansiedade.universe, [2, 4, 6, 8])
        self.ansiedade['grave'] = fuzz.trapmf(self.ansiedade.universe,   [6, 8, 10, 10])

        self.tea['leve'] = fuzz.trapmf(self.tea.universe, [0, 0, 2, 4])
        self.tea['moderado'] = fuzz.trapmf(self.tea.universe, [2, 4, 6, 8])
        self.tea['grave'] = fuzz.trapmf(self.tea.universe,   [6, 8, 10, 10])

    def define_regras(self): # 231 REGRAS DEFINIDAS
        self.regras = []
        
        # PRIMEIRO PACK - CASOS ISOLADOS -----------------------------------------------------------------------------------------------------

        '''Depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule((self.anedonia['baixo'] | self.anedonia['medio']) & self.humor_deprimido['medio'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) 
                                     & self.morte['baixo'] & self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     self.dif_inte_soc['baixo'] & self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['leve']))
       
        '''Depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & (self.morte['baixo']  | self.morte['medio']) & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     (self.dif_inte_soc['baixo'] | self.dif_inte_soc['medio']) & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['baixo'] | self.sint_present_maior['medio']) & self.seman_sint_present['baixo'] ,
                                     self.depressao['moderado']))
        
        '''Depressão GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & 
                                    self.alteracao_sono['alto'] & self.morte['alto'] & 
                                    self.rigidez_cog['alto'] & self.medo['baixo'] & 
                                    self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                    self.dif_inte_soc['alto'] & 
                                    (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) & 
                                    self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                    self.depressao['grave']))
        
        '''Ansidade LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & 
                                     (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['leve']))
        '''Ansidade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['medio'] & 
                                     self.comport_est['baixo'] & self.dif_inte_soc['medio'] & (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))
                                     
        '''Ansidade GRAVE''' # Quadro 8
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & 
                                    (self.alteracao_sono['medio'] | self.alteracao_sono['alto']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & 
                                     self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & 
                                     (self.dif_inte_soc['medio'] | self.dif_inte_soc['alto']) & 
                                     (self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) &
                                     self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))
        
        '''TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & (self.rigidez_cog['baixo'] | self.rigidez_cog['medio']) & self.medo['baixo'] & self.preoc_exc['baixo'] & 
                                     self.comport_est['medio'] & self.dif_inte_soc['medio'] & self.doenca_pre_existente['baixo'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        '''TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & (self.morte['baixo'] | self.morte['medio']) & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        '''TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        # DEMAIS SAÍDAS ---------------------------------------------------------------------------------------------------------------------------

        ''''Quando depressão saída para ANSIEDADE'''
        # Depressão LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule((self.anedonia['baixo'] | self.anedonia['medio']) & self.humor_deprimido['medio'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) 
                                     & self.morte['baixo'] & self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     self.dif_inte_soc['baixo'] & self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
       
        # Depressão MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & (self.morte['baixo']  | self.morte['medio']) & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     (self.dif_inte_soc['baixo'] | self.dif_inte_soc['medio']) & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['baixo'] | self.sint_present_maior['medio']) & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
        
        # Depressão GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
        
        ''''Quando depressão saída para TEA'''

        # Depressão LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule((self.anedonia['baixo'] | self.anedonia['medio']) & self.humor_deprimido['medio'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) 
                                     & self.morte['baixo'] & self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     self.dif_inte_soc['baixo'] & self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
       
        # Depressão MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & (self.morte['baixo']  | self.morte['medio']) & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & 
                                     (self.dif_inte_soc['baixo'] | self.dif_inte_soc['medio']) & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['baixo'] | self.sint_present_maior['medio']) & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
        # Depressão GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
        # ----------------------------------

        ''''Quando ansiedade saída para DEPRESSÃO'''
        # Ansidade LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & 
                                     (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))
        # Ansidade MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['medio'] & 
                                     self.comport_est['baixo'] & self.dif_inte_soc['medio'] & (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))
        # Ansidade GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['medio'] | self.alteracao_sono['alto']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & 
                                     (self.dif_inte_soc['medio'] | self.dif_inte_soc['alto']) & (self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) &
                                     self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))
        
        ''''Quando ansiedade saída para TEA'''

        # Ansidade LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & 
                                     (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        # Ansidade MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['medio'] & 
                                     self.comport_est['baixo'] & self.dif_inte_soc['medio'] & (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        # Ansidade GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & 
                                    (self.alteracao_sono['medio'] | self.alteracao_sono['alto']) & 
                                    self.morte['baixo'] & self.rigidez_cog['baixo'] & self.medo['alto'] & 
                                    self.preoc_exc['alto'] & self.comport_est['baixo'] & 
                                    (self.dif_inte_soc['medio'] | self.dif_inte_soc['alto']) & 
                                    (self.doenca_pre_existente['medio'] | self.doenca_pre_existente['alto']) &
                                    self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                    self.tea['leve']))
        
        ''''Quando TEA saída para ANSIEDADE'''

         # TEA LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & (self.rigidez_cog['baixo'] | self.rigidez_cog['medio']) & self.medo['baixo'] & self.preoc_exc['baixo'] & 
                                     self.comport_est['medio'] & self.dif_inte_soc['medio'] & self.doenca_pre_existente['baixo'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        # TEA MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & (self.morte['baixo'] | self.morte['medio']) & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        # TEA GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        ''''Quando TEA saída para DEPRESSÃO'''

          # TEA LEVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & (self.alteracao_sono['baixo'] | self.alteracao_sono['medio']) & 
                                     self.morte['baixo'] & (self.rigidez_cog['baixo'] | self.rigidez_cog['medio']) & self.medo['baixo'] & self.preoc_exc['baixo'] & 
                                     self.comport_est['medio'] & self.dif_inte_soc['medio'] & self.doenca_pre_existente['baixo'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        # TEA MODERADO
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & (self.morte['baixo'] | self.morte['medio']) & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        # TEA GRAVE
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
                
        # SEGUNDO PACK - DEPRESSÃO E ANSIEDADE ---------------------------------------------------

        '''Depressão LEVE e ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Depressão MODERADO e ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                self.tea['leve']))
                                
        '''Depressão GRAVE e ansiedade GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.tea['leve']))

        '''Ansiedade LEVE e depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Ansiedade LEVE e depressão GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Ansiedade GRAVE e depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade MODERADO e depressão GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['medio'] ,
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade GRAVE e depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['alto'] | self.sint_present_maior['medio']) & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['alto'] | self.sint_present_maior['medio']) & self.seman_sint_present['medio'] ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['alto'] | self.sint_present_maior['medio']) & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        
        # ----- Acima estão 54 regras [18 regras distintas x 3]

        '''Ansiedade LEVE e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'],
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'],
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'],
                                     self.depressao['leve']))

        '''Ansiedade MODERADO e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['medio'] & 
                                     self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['medio'] & 
                                     self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['medio'] & 
                                     self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        '''Ansiedade GRAVE e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & (self.morte['alto'] | self.morte['medio']) & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['alto'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & (self.morte['alto'] | self.morte['medio']) & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['alto'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & (self.morte['alto'] | self.morte['medio']) & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['alto'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        '''Ansiedade LEVE e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        '''Ansiedade LEVE e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        '''Ansiedade MODERADO e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        '''Ansiedade GRAVE e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        '''Ansiedade GRAVE e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & 
                                     (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & 
                                     (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & 
                                     (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        '''Ansiedade MODERADO e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & 
                                     self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & 
                                     self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & 
                                     self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        '''Depressão LEVE e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão MODERADO e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))

        '''Depressão GRAVE e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão LEVE e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão LEVE e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão MODERADO e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))

        '''Depressão GRAVE e TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão GRAVE e TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        '''Depressão MODERADO e TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & (self.sint_present_maior['medio'] | self.sint_present_maior['alto']) & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        # ----- Acima estão 54 regras [18 regras distintas x 3] => 54 do começo + 54 do último intervalo = 108 regras 

        '''Depressão MODERADO, Ansiedade LEVE, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']),
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']),
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']),
                                     self.tea['leve']))
        
        '''Depressão GRAVE, Ansiedade MODERADO, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['moderado']))
        
        '''Depressão LEVE, Ansiedade GRAVE, TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     (self.doenca_pre_existente['baixo'] | self.doenca_pre_existente['medio']) & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.tea['grave']))

        '''Depressão LEVE, Ansiedade LEVE, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        '''Depressão MODERADO, Ansiedade LEVE, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['moderado']))

        '''Depressão MODERADO, Ansiedade LEVE, TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['grave']))

        '''Depressão GRAVE, Ansiedade LEVE, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['leve']))

        '''Depressão GRAVE, Ansiedade LEVE, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['moderado']))
        
        '''Depressão GRAVE, Ansiedade LEVE, TEA GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['alto']) ,
                                     self.tea['grave']))

        '''Depressão MODERADO, Ansiedade GRAVE, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.tea['leve']))
        
        '''Depressão LEVE, Ansiedade GRAVE, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & (self.seman_sint_present['medio'] | self.seman_sint_present['alto']) ,
                                     self.tea['moderado']))
        
        '''Depressão GRAVE, Ansiedade GRAVE, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio'] | self.seman_sint_present['alto']),
                                     self.tea['moderado']))
        
        # CASOS DE TESTES (REFINAMENTO) ------------------------------------

        '''Depressão GRAVE, Ansiedade LEVE, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))

        '''Depressão GRAVE, Ansiedade MODERADO''' #
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        
        '''Depressão LEVE, Ansiedade GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        
        '''Depressão GRAVE, Ansiedade GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['medio'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['medio'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['medio'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
        '''Depressão GRAVE, Ansiedade GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Depressão GRAVE, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['alto'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
        '''Depressão GRAVE, Ansiedade GRAVE'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']) ,
                                     self.depressao['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']) ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['alto'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & 
                                     (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']) ,
                                     self.tea['leve']))

        '''Depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Ansiedade LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        
        # VISUAL -----------------------------
        '''Depressão GRAVE, Ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Depressão LEVE, Ansiedade LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

        '''Depressão LEVE, Ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
                                     
        '''Ansiedade GRAVE, Depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['alto'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade GRAVE, Depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade MODERADO, Depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.depressao['moderado'])) 

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.ansiedade['moderado']))   

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & (self.medo['baixo'] | self.medo['medio']) & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & (self.seman_sint_present['baixo'] | self.seman_sint_present['medio']),
                                     self.tea['leve']))         

        '''Ansiedade LEVE, Depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Depressão MODERADO, Ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['medio'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Depressão MODERADO, Ansiedade MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''Ansiedade GRAVE, Depressão MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))
        
        '''Ansiedade MODERADO, Depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['alto'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        '''TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        '''TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['medio'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & (self.preoc_exc['baixo'] | self.preoc_exc['medio']) & 
                                     self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        '''Depressão MODERADO, Ansiedade MODERADO, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['alto'] & self.morte['medio'] & 
                                     self.rigidez_cog['alto'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        '''Depressão MODERADO, TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['medio'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        '''Ansiedade MODERADO, TEA MODERADO'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['alto'] & self.morte['baixo'] & 
                                     self.rigidez_cog['alto'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))
        
        '''TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))

        '''Ansiedade MODERADO, TEA LEVE''' 
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['medio'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['medio'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))
        
        '''TEA LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['medio'] & self.morte['baixo'] & 
                                     self.rigidez_cog['medio'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['medio'] & self.dif_inte_soc['alto'] & 
                                     self.doenca_pre_existente['baixo'] & self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['leve']))

        '''Ansiedade MODERADO, Depressão LEVE'''
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                    self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                    self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                    self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                    self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                    self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                    self.ansiedade['moderado']))
        
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
                                    self.rigidez_cog['baixo'] & self.medo['alto'] & self.preoc_exc['medio'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
                                    self.doenca_pre_existente['baixo'] & self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                    self.tea['leve']))


        # Quando há pensamento de morte --------------------------------------------------------------------------------------------
        # Moderado
        # self.regras.append(ctrl.Rule(self.morte['medio'] | self.morte['alto'],
        #                      self.depressao['moderado']))
        
        # self.regras.append(ctrl.Rule(self.morte['medio'] | self.morte['alto'],
        #                      self.ansiedade['leve']))
        
        # self.regras.append(ctrl.Rule(self.morte['medio'] | self.morte['alto'],
        #                      self.tea['moderado']))

        # Depressão - Anedonia e humor deprimido
        # self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'],
        #                             self.depressao['moderado']))

        # self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'],
        #                             self.ansiedade['leve']))

        # self.regras.append(ctrl.Rule(self.anedonia['medio'] & self.humor_deprimido['medio'],
        #                             self.tea['leve']))

        # Algumas variáveis [ÚLTIMAS REGRAS]------------------------------------------------------------------------------------------

        # DEPRESSÃO

            # Moderado
        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.morte['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['moderado']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.morte['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['medio'] & self.morte['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))

            # Grave
        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.morte['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.depressao['grave']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.morte['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.anedonia['alto'] & self.humor_deprimido['alto'] & self.morte['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['baixo'] ,
                                     self.tea['leve']))
        
         # ANSIEDADE

            # Moderado
        self.regras.append(ctrl.Rule(self.alteracao_sono['medio'] & self.medo['medio'] & self.preoc_exc['medio'] &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.alteracao_sono['medio'] & self.medo['medio'] & self.preoc_exc['medio'] &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['moderado']))

        self.regras.append(ctrl.Rule(self.alteracao_sono['medio'] & self.medo['medio'] & self.preoc_exc['medio'] &
                                     self.sint_present_maior['medio'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

            # Grave
        self.regras.append(ctrl.Rule(self.alteracao_sono['alto'] & self.medo['alto'] & self.preoc_exc['alto'] &
                                     self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.alteracao_sono['alto'] & self.medo['alto'] & self.preoc_exc['alto'] &
                                     self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.ansiedade['grave']))

        self.regras.append(ctrl.Rule(self.alteracao_sono['alto'] & self.medo['alto'] & self.preoc_exc['alto'] &
                                     self.sint_present_maior['alto'] & self.seman_sint_present['medio'] ,
                                     self.tea['leve']))

        # TEA

            # Moderado
        self.regras.append(ctrl.Rule(self.rigidez_cog['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.rigidez_cog['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.rigidez_cog['medio'] & self.comport_est['medio'] & self.dif_inte_soc['medio'] & 
                                     self.sint_present_maior['medio'] & self.seman_sint_present['alto'] ,
                                     self.tea['moderado']))

            # Grave
        self.regras.append(ctrl.Rule(self.rigidez_cog['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.depressao['leve']))

        self.regras.append(ctrl.Rule(self.rigidez_cog['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.ansiedade['leve']))

        self.regras.append(ctrl.Rule(self.rigidez_cog['alto'] & self.comport_est['alto'] & self.dif_inte_soc['alto'] & 
                                     self.sint_present_maior['alto'] & self.seman_sint_present['alto'] ,
                                     self.tea['grave']))

        

        # Para copiar apenas abaixo

        # self.regras.append(ctrl.Rule(self.anedonia['baixo'] & self.humor_deprimido['baixo'] & self.alteracao_sono['baixo'] & self.morte['baixo'] & 
        #                              self.rigidez_cog['baixo'] & self.medo['baixo'] & self.preoc_exc['baixo'] & self.comport_est['baixo'] & self.dif_inte_soc['baixo'] & 
        #                              self.doenca_pre_existente['baixo'] & self.sint_present_maior['baixo'] & self.seman_sint_present['baixo'] ,
        #                              self.depressao['leve']))

    def calcula_diagnostico(self, entradas):

        for chave, valor in entradas.items():
            self.diagnostico_simulador.input[chave] = valor
        self.diagnostico_simulador.compute()

        self.depressao.view(sim=self.diagnostico_simulador)
        self.ansiedade.view(sim=self.diagnostico_simulador)
        self.tea.view(sim=self.diagnostico_simulador)

        self.grava_log(entradas)
       
        return {
            'depressao': self.diagnostico_simulador.output['depressao'],
            'ansiedade': self.diagnostico_simulador.output['ansiedade'],
            'tea': self.diagnostico_simulador.output['tea']
        }

    def ativacoes(self):
        # Armazena saída do terminal em um buffer e guarda em uma variável 
        capturador = CapturadorSaida(self.diagnostico_simulador)
        stringInf = capturador.capturar_inf() 
        # print(stringInf)  # Imprime inf. sobre o funcionamento interno de um ControlSystemSimulation

        regrasAtivadas = RegrasAtivadas(stringInf) # Obtém somente regra e grau de ativação das regras
        regrasAtivadas.imprimir_ativacoes()
        
        return regrasAtivadas.obter_ativacoes()

        # diagnostico_simulador.print_state()

    def grava_log(self, entradas):
        entradas_formatadas = []
        linha = f"TESTES | "
        linha += "[Entradas => "
        for chave, valor in entradas.items():
            entradas_formatadas.append(f"{chave}: {round(valor, 2):.2f}, ")
        
        # Remove a última vírgula e espaço
        entradas_formatadas[-1] = entradas_formatadas[-1].rstrip(', ')
        
        linha += ''.join(entradas_formatadas) + "] [Saída => "
        linha += f"Dep.: {round(self.diagnostico_simulador.output['depressao'], 2):.2f}, "
        linha += f"Ans.: {round(self.diagnostico_simulador.output['ansiedade'], 2):.2f}, "
        linha += f"TEA: {round(self.diagnostico_simulador.output['tea'], 2):.2f}]"
        
        regras_ativadas = self.ativacoes()
        regras_formatadas = [(regra[0], f"{float(regra[1]):.2f}") for regra in regras_ativadas]
        
        linha += f"[Regras Ativadas: {regras_formatadas}"
        linha += ']'
        logging.info(linha)