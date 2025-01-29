
import os
import openmc
import openmc.deplete
import openmc.model
from datetime import datetime
import numpy as np
import pandas as pd

os.system("clear")
print("#######################################################################")
print("#######################################################################")
print("####                                                               ####")
print("####              UNIVERSIDADE FEDERAL DE MINAS GERAIS             ####")
print("####               Departamento de Engenharia Nuclear              ####")
print("####                Jefferson Quintão Campos Duarte                ####")
print("####                  Thalles Oliveira Campagnani                  ####")
print("####                                                               ####")
print("#######################################################################")
print("####                                                               ####")
print("####              SEALER - Swedish Advanced Lead Reactor           ####")
print("####                    OpenMC Simulation Library                  ####")
print("####                                                               ####")
print("#######################################################################")
print("#######################################################################")


################################################
############  Controle de diretório  ###########
################################################
def dir(nome="teste_sem_nome",data=True,voltar=False):
    if (voltar==True):
        os.chdir("../")
    if (data==True):
        agora = datetime.now()
        nome = agora.strftime(nome+"_%Y%m%d_%H%M%S")
    if not os.path.exists(nome):
        os.makedirs(nome)
    os.chdir(nome)

################################################
############         Classe          ###########
################################################
class SealerArctic:

    ################################################
    ############       Construtor        ###########
    ################################################

    def __init__(
            self,
            config="UO2",
            cross="",
            altura_barra=55.3001,
            altura_shut=55.3002,
            particulas=15000,
            ciclos=400,
            inativo=40,
            atrasados=True):
        
        ## Configurações de combustível e geometria
        #Combustivel homogêneo
        if config=="UO2" or config=="UN" or config=="U3Si2" or config=="MOX":
            self.materiais(tipoCombustivel=config,cross=cross) 
            self.geometria(altura_barra=altura_barra,altura_shut=altura_shut)

        #Combustível heterogêno
        elif (config=="UO2+MOX_anel_intermediario"):
            self.materiais(tipoCombustivel="UO2MOX",cross=cross)
            self.geometria(altura_barra=altura_barra,altura_shut=altura_shut,mox_anel_intermediario=True)
            
        elif (config=="UO2+MOX_anel_externo_1"):
            self.materiais(tipoCombustivel="UO2MOX",cross=cross)
            self.geometria(altura_barra=altura_barra,altura_shut=altura_shut,mox_anel_externo_1=True)
            
        elif (config=="UO2+MOX_anel_externo_2"):
            self.materiais(tipoCombustivel="UO2MOX",cross=cross)
            self.geometria(altura_barra=altura_barra,altura_shut=altura_shut,mox_anel_externo_2=True)
            
        else:
            self.__del__(self)

        ## Definições de simulação
        self.configuracoes(particulas, ciclos, inativo, atrasados)

    ################################################
    ############        Destrutor        ###########
    ################################################

    def __del__(self):
        print(f"Objeto destruído.")
        
    ################################################
    ############ Definição dos Materiais ###########
    ################################################

    def materiais(
            self, 
            tipoCombustivel= "UO2", 
            cross="",
            tempComb=750, 
            tempSys=663.0, 
            tempRefri=684.0, 
            tempClad_15_15Ti=690.0, 
            densidadeCombUO2=10.48, 
            densidadeCombUN=13.7426,
            densidadeCombU3Si2=11.5655, 
            densidadeCombMOX=10.62, 
            densidadeRefrigerante=10.4851):

        #Cria objeto para armazenar os materiais criados
        self.materials = openmc.Materials()

        #Já definir as cores dos materiais para os 'plots'
        self.colors = {}

        #Escolhendo o material do combustível
        if tipoCombustivel=="UO2":
            print("################################################")
            print("############ Definição dos Materiais ###########")
            print("############           UO2           ###########")
            print("################################################")
            
            self.combustivel = openmc.Material(temperature = tempComb, name=tipoCombustivel)
            self.combustivel.add_nuclide('U235', 1.7405E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('U238', 7.0720E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('O16',  1.1844E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('O17',  4.7947E-05, percent_type = 'wo')
            self.combustivel.add_nuclide('O18',  2.6720E-04, percent_type = 'wo')
            self.combustivel.volume = 2.69681E+05 #cm³
            self.combustivel.set_density('g/cm3', densidadeCombUO2)
            self.materials.append(self.combustivel)
            self.colors["self.combustivel"] = "yellow"

            
        elif tipoCombustivel=="UN":
            print("################################################")
            print("############ Definição dos Materiais ###########")
            print("############           UN            ###########")
            print("################################################")
            
            self.combustivel = openmc.Material(temperature = tempComb, name=tipoCombustivel)
            self.combustivel.add_nuclide('U235', 1.5486E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('U238', 7.8943E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('N14',  5.5484E-02, percent_type = 'wo')
            self.combustivel.add_nuclide('N15',  2.1833E-04, percent_type = 'wo')
            self.combustivel.volume = 2.69681E+05 #cm³
            self.combustivel.set_density('g/cm3', densidadeCombUN)
            self.materials.append(self.combustivel)
            self.colors["self.combustivel"] = "green"
        
        elif tipoCombustivel=="U3Si2":
            print("################################################")
            print("############ Definição dos Materiais ###########")
            print("############          U3Si2          ###########")
            print("################################################")
            
            self.combustivel = openmc.Material(temperature = tempComb, name=tipoCombustivel)
            self.combustivel.add_nuclide('U235', 1.6870E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('U238', 7.5821E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('Si28', 6.7150E-02, percent_type = 'wo')
            self.combustivel.add_nuclide('Si29', 3.5216E-03, percent_type = 'wo')
            self.combustivel.add_nuclide('Si30', 2.4181E-03, percent_type = 'wo')
            self.combustivel.volume = 2.69681E+05 #cm³
            self.combustivel.set_density('g/cm3', densidadeCombU3Si2)
            self.materials.append(self.combustivel)
            self.colors["self.combustivel"] = "orange"
            
        elif tipoCombustivel=="MOX":
            print("################################################")
            print("############ Definição dos Materiais ###########")
            print("############           MOX           ###########")
            print("################################################")
            
            self.combustivel = openmc.Material(temperature = tempComb,name=tipoCombustivel)
            self.combustivel.add_nuclide('U235',  1.2862E-03, percent_type = 'wo')
            self.combustivel.add_nuclide('U238',  6.4182E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('Pu238', 4.9985E-03, percent_type = 'wo')
            self.combustivel.add_nuclide('Pu239', 1.3089E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('Pu240', 4.4745E-02, percent_type = 'wo')
            self.combustivel.add_nuclide('Pu241', 4.2073E-02, percent_type = 'wo')
            self.combustivel.add_nuclide('Pu242', 1.5900E-02, percent_type = 'wo')
            self.combustivel.add_nuclide('O16',   1.1798E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('O17',   4.7760E-05, percent_type = 'wo')
            self.combustivel.add_nuclide('O18',   2.6615E-04, percent_type = 'wo')
            self.combustivel.volume = 2.69681E+05 #cm³
            self.combustivel.set_density('g/cm3', densidadeCombMOX)
            self.materials.append(self.combustivel)
            self.colors["self.combustivel"] = "red"
            
        elif tipoCombustivel=="UO2MOX":
            print("################################################")
            print("############ Definição dos Materiais ###########")
            print("############         UO2MOX          ###########")
            print("################################################")
            
            self.combustivel = openmc.Material(temperature = tempComb, name=tipoCombustivel)
            self.combustivel.add_nuclide('U235', 1.7405E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('U238', 7.0720E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('O16',  1.1844E-01, percent_type = 'wo')
            self.combustivel.add_nuclide('O17',  4.7947E-05, percent_type = 'wo')
            self.combustivel.add_nuclide('O18',  2.6720E-04, percent_type = 'wo')
            self.combustivel.volume = 1.84518E+05 #cm³  1 célula combustível = 1.55975E+02 cm³
            self.combustivel.set_density('g/cm3', densidadeCombUO2)
            self.materials.append(self.combustivel)
            self.colors["self.combustivel"] = "yellow"

            self.MOX = openmc.Material(temperature = tempComb)
            self.MOX.add_nuclide('U235',  1.2862E-03, percent_type = 'wo')
            self.MOX.add_nuclide('U238',  6.4182E-01, percent_type = 'wo')
            self.MOX.add_nuclide('Pu238', 4.9985E-03, percent_type = 'wo')
            self.MOX.add_nuclide('Pu239', 1.3089E-01, percent_type = 'wo')
            self.MOX.add_nuclide('Pu240', 4.4745E-02, percent_type = 'wo')
            self.MOX.add_nuclide('Pu241', 4.2073E-02, percent_type = 'wo')
            self.MOX.add_nuclide('Pu242', 1.5900E-02, percent_type = 'wo')
            self.MOX.add_nuclide('O16',   1.1798E-01, percent_type = 'wo')
            self.MOX.add_nuclide('O17',   4.7760E-05, percent_type = 'wo')
            self.MOX.add_nuclide('O18',   2.6615E-04, percent_type = 'wo')
            self.MOX.volume = 8.51622E+04 #cm³
            self.MOX.set_density('g/cm3', densidadeCombMOX)
            self.materials.append(self.MOX)
            self.colors["self.MOX"] = "red"
        
        #######################################################
        ############ Definição dos Outros Materiais ###########
        #######################################################
        
        self.reflec_ins = openmc.Material(temperature = tempSys)
        self.reflec_ins.add_nuclide('Y89',  3.2000E-02, percent_type = 'ao')
        self.reflec_ins.add_nuclide('O16',  6.5976E-01, percent_type = 'ao')
        self.reflec_ins.add_nuclide('O17',  2.5131E-04, percent_type = 'ao')
        self.reflec_ins.add_nuclide('O18',  1.3227E-03, percent_type = 'ao')
        self.reflec_ins.add_nuclide('Zr90', 1.5778E-01, percent_type = 'ao')
        self.reflec_ins.add_nuclide('Zr91', 3.4408E-02, percent_type = 'ao')
        self.reflec_ins.add_nuclide('Zr92', 5.2593E-02, percent_type = 'ao')
        self.reflec_ins.add_nuclide('Zr94', 5.3299E-02, percent_type = 'ao')
        self.reflec_ins.add_nuclide('Zr96', 8.5867E-03, percent_type = 'ao')
        self.reflec_ins.set_density('g/cm3', 6.0)
        self.materials.append(self.reflec_ins)
        self.colors["self.reflec_ins"]='blue'

        self.shield = openmc.Material(temperature = tempSys)
        self.shield.add_nuclide('B10', 7.3914E-01, percent_type = 'wo')
        self.shield.add_nuclide('B11', 3.0798E-02, percent_type = 'wo')
        self.shield.add_nuclide('C12', 2.2730E-01, percent_type = 'wo')
        self.shield.add_nuclide('C13', 2.7646E-03, percent_type = 'wo')
        self.shield.set_density('g/cm3', 2.14)
        self.materials.append(self.shield)
        self.colors["self.shield"]='green'

        self.clad_SS316L = openmc.Material(temperature = tempSys)
        self.clad_SS316L.add_nuclide('C12',   2.9639E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('C13',   3.6051E-06, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('N14',   9.9608E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('N15',   3.9196E-06, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('S32',   2.8424E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('S33',   2.3137E-06, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('S34',   1.3380E-05, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('S36',   6.7303E-08, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('P31',   4.5000E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Si28',  6.8905E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Si29',  3.6136E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Si30',  2.4813E-04, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Fe54',  3.6055E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Fe56',  5.8692E-01, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Fe57',  1.3797E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Fe58',  1.8683E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mn55',  2.0000E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Cr50',  3.3926E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Cr52',  6.8034E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Cr53',  7.8631E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Cr54',  1.9942E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Ni58',  8.0637E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Ni60',  3.2131E-02, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Ni61',  1.4202E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Ni62',  4.6012E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Ni64',  1.2103E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo92',  3.5544E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo94',  2.2637E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo95',  3.9375E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo96',  4.1688E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo97',  2.4118E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo98',  6.1566E-03, percent_type = 'wo')
        self.clad_SS316L.add_nuclide('Mo100', 2.5073E-03, percent_type = 'wo')
        self.clad_SS316L.set_density('g/cm3', 8.0)
        self.materials.append(self.clad_SS316L)
        self.colors["self.clad_SS316L"]='gray'

        self.clad_15_15Ti = openmc.Material(temperature = tempClad_15_15Ti)
        self.clad_15_15Ti.add_nuclide('C12',  9.8798E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('C13',  1.2017E-05, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('S32',  9.4746E-06, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('S33',  7.7122E-08, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('S34',  4.4599E-07, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('S36',  2.2434E-09, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('P31',  1.3000E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Si28', 5.1449E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Si29', 2.6982E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Si30', 1.8527E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Fe54', 3.6067E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Fe56', 5.8711E-01, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Fe57', 1.3802E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Fe58', 1.8689E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mn55', 1.8300E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cr50', 3.0094E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cr52', 6.0351E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cr53', 6.9750E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cr54', 1.7690E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ni58', 1.0107E-01, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ni60', 4.0271E-02, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ni61', 1.7799E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ni62', 5.7668E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ni64', 1.5169E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo92', 1.7203E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo94', 1.0956E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo95', 1.9057E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo96', 2.0177E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo97', 1.1673E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo98', 2.9798E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Mo100',1.2135E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ti46', 3.8808E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ti47', 3.5759E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ti48', 3.6184E-03, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ti49', 2.7108E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ti50', 2.6484E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('N14' , 1.0957E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('N15' , 4.3115E-07, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('V50' , 8.3341E-07, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('V51' , 3.3917E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Co59', 2.0000E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('B10' , 5.1607E-06, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('B11' , 2.2839E-05, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ta181',5.9668E-09, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ta182',4.9994E-05, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cu63', 1.7810E-04, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Cu65', 8.1901E-05, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca40', 9.6662E-05, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca42', 6.7736E-07, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca43', 1.4470E-07, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca44', 2.2878E-06, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca46', 4.5864E-09, percent_type = 'wo')
        self.clad_15_15Ti.add_nuclide('Ca48', 2.2374E-07, percent_type = 'wo')
        self.clad_15_15Ti.set_density('g/cm3', 7.89)
        self.materials.append(self.clad_15_15Ti)
        self.colors["self.clad_15_15Ti"]='black'

        self.refrigerante = openmc.Material(temperature = tempRefri)
        self.refrigerante.add_nuclide('Pb204', 1.4000E-02, percent_type = 'ao')
        self.refrigerante.add_nuclide('Pb206', 2.4100E-01, percent_type = 'ao')
        self.refrigerante.add_nuclide('Pb207', 2.2100E-01, percent_type = 'ao')
        self.refrigerante.add_nuclide('Pb208', 5.2400E-01, percent_type = 'ao')
        self.refrigerante.set_density('g/cm3', densidadeRefrigerante)
        self.materials.append(self.refrigerante)
        self.colors["self.refrigerante"]='cyan'

        self.control = openmc.Material(temperature = tempSys)
        self.control.add_nuclide('B10', 1.4420E-01, percent_type = 'wo')
        self.control.add_nuclide('B11', 6.3840E-01, percent_type = 'wo')
        self.control.add_nuclide('C12', 2.1480E-01, percent_type = 'wo')
        self.control.add_nuclide('C13', 2.6120E-03, percent_type = 'wo')
        self.control.set_density('g/cm3', 2.25)
        self.materials.append(self.control)
        self.colors["self.control"]='pink'

        self.shut_down = openmc.Material(temperature = tempSys)
        self.shut_down.add_nuclide('B10',   6.4233E-01, percent_type = 'ao')
        self.shut_down.add_nuclide('B11',   2.4341E-02, percent_type = 'ao')
        self.shut_down.add_nuclide('W182',  4.2589E-02, percent_type = 'ao') #4.2397E-02
        self.shut_down.add_nuclide('W183',  2.2902E-02, percent_type = 'ao')
        self.shut_down.add_nuclide('W184',  4.9027E-02, percent_type = 'ao')
        self.shut_down.add_nuclide('W186',  4.5482E-02, percent_type = 'ao')
        self.shut_down.add_nuclide('Re185', 6.4827E-02, percent_type = 'ao')
        self.shut_down.add_nuclide('Re187', 1.0851E-01, percent_type = 'ao')
        self.shut_down.set_density('g/cm3', 11.7)
        self.materials.append(self.shut_down)
        self.colors["self.shut_down"]='purple'

        self.clad_Fe10Cr4Al = openmc.Material(temperature = tempSys)
        self.clad_Fe10Cr4Al.add_nuclide('C12',  2.9639E-04, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('C13',  3.6051E-06, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Al27', 4.0000E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Si28', 6.4311E-04, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Si29', 3.3727E-05, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Si30', 2.3159E-05, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Cr50', 1.9956E-03, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Cr52', 4.0020E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Cr53', 4.6254E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Cr54', 1.1731E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Fe54', 4.7251E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Fe56', 7.6918E-01, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Fe57', 1.8081E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.add_nuclide('Fe58', 2.4485E-02, percent_type = 'wo')
        self.clad_Fe10Cr4Al.set_density('g/cm3', 7.3)
        self.materials.append(self.clad_Fe10Cr4Al)
        self.colors["self.clad_Fe10Cr4Al"]='brown'

        self.clad_Fe10Cr4AlRE = openmc.Material(temperature = tempSys)
        self.clad_Fe10Cr4AlRE.add_nuclide('Al27', 4.0000E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Cr50', 1.9956E-03, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Cr52', 4.0020E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Cr53', 4.6254E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Cr54', 1.1731E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Fe54', 4.7169E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Fe56', 7.6784E-01, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Fe57', 1.8050E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Fe58', 2.4442E-02, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('C12',  2.9639E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('C13',  3.6051E-06, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Zr90', 4.0565E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Zr91', 8.9447E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Zr92', 1.3822E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Zr94', 1.4313E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Zr96', 2.3550E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Ti46', 5.5441E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Ti47', 5.1084E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Ti48', 5.1692E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Ti49', 3.8725E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Ti50', 3.7834E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Si28', 6.4311E-04, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Si29', 3.3727E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.add_nuclide('Si30', 2.3159E-05, percent_type = 'wo')
        self.clad_Fe10Cr4AlRE.set_density('g/cm3', 7.3)
        self.materials.append(self.clad_Fe10Cr4AlRE)
        self.colors["self.clad_Fe10Cr4AlRE"]='magenta'

        #Se o caminho "cross" não existe, será usado a variável de ambiente OPENMC_CROSS_SECTIONS
        if os.path.exists(cross):
                self.materials.cross_sections = cross

        #Gerando input XML dos materiais
        self.materials.export_to_xml()
        
    ################################################"
    ############ Definição da Geometria ############"
    ################################################"
    
    def geometria(
            self,altura_barra=55.3001,
            altura_shut=55.3002,
            mox_anel_intermediario=False,
            mox_anel_externo_1=False,
            mox_anel_externo_2=False):
        print("################################################")
        print("############ Definição da Geometria ############")
        print("################################################")

        ############ Definição de superfícies #########################################################################################

        # Superfícies da vareta combustível

        self.fuel_radius = openmc.ZCylinder(r=0.670,)
        self.fuel_inner_clad = openmc.ZCylinder(r=0.676,)
        self.fuel_outer_clad = openmc.ZCylinder(r=0.726,)

        self.upper_gas_plenum = openmc.ZPlane(z0=+91.300,)
        
        self.upper_fuel_column    = openmc.ZPlane(z0=+55.300,)
        self.upper_insulation_top = openmc.ZPlane(z0=+56.300,)
        self.lower_fuel_column = openmc.ZPlane(z0=-55.300,)
        self.lower_insulation_bot = openmc.ZPlane(z0=-56.300,)
        self.lower_shield = openmc.ZPlane(z0=-61.300,)

        # Superfícies da vareta refletora
        self.reflec_radius = openmc.ZCylinder(r=0.8875,)
        self.reflec_inner_clad = openmc.ZCylinder(r=0.9630,)
        self.reflec_outer_clad = openmc.ZCylinder(r=1.0700,)

        # Superfícies da vareta de controle e blindagem
        self.shield_radius = openmc.ZCylinder(r=1.2385,)
        self.shield_inner_clad = openmc.ZCylinder(r=1.3435,)
        self.shield_outer_clad = openmc.ZCylinder(r=1.4930,)

        # altura_barra = 55.3001
        self.control_insertion = openmc.ZPlane(z0=altura_barra,)  # Manipulação das barras de controle
        self.shut_insertion = openmc.ZPlane(z0=altura_shut,)  # Manipulação das barras de desligamento

        # Superfícies da vareta de shut-down
        self.shut_radius = openmc.ZCylinder(r=1.6900,)
        self.shut_inner_clad = openmc.ZCylinder(r=1.7000,)
        self.shut_outer_clad = openmc.ZCylinder(r=1.8700,)

        # Core
        self.core_inner_radius = openmc.ZCylinder(r=85.4,)
        self.core_outer_radius = openmc.ZCylinder(r=87.4,)
        self.vessel_inner_radius = openmc.ZCylinder(r=132.4,)
        self.vessel_outer_radius = openmc.ZCylinder(r=137.4, boundary_type='vacuum')

        self.core_top = openmc.ZPlane(z0=+113.3,)
        self.core_bot = openmc.ZPlane(z0=-76.3,)
        self.rods_top = openmc.ZPlane(z0=+93.300,)
        self.rods_bot = openmc.ZPlane(z0=-66.300,)
        self.vessel_top = openmc.ZPlane(z0=+269.3, boundary_type='vacuum')
        self.vessel_bot = openmc.ZPlane(z0=-156.3, boundary_type='vacuum')

        ############ Definição de células de varetas ################################################################################

        # Células da vareta combustível

        self.fuel = openmc.Cell(name='celula_combustivel', fill=self.combustivel, region=-self.fuel_radius & -self.upper_fuel_column & +self.lower_fuel_column)
        self.insulation = openmc.Cell(name='celula_isolante', fill=self.reflec_ins, region=-self.fuel_radius & -self.upper_insulation_top
                                                                & +self.upper_fuel_column | 
                                                                -self.fuel_radius & -self.lower_fuel_column & +self.lower_insulation_bot)
        self.shield_fuel = openmc.Cell(name='celula_shield_fuel', fill=self.shield, region=-self.fuel_radius & -self.lower_insulation_bot & +self.lower_shield)
        self.plenum_fuel = openmc.Cell(name='celula_plenum_fuel', region=-self.fuel_inner_clad & -self.upper_gas_plenum
                                                                    & +self.upper_insulation_top)
        self.plugs_fuel = openmc.Cell(name='celula_plug_fuel', fill=self.clad_SS316L, region=-self.fuel_inner_clad & -self.rods_top
                                                                & +self.upper_gas_plenum |
                                                                -self.fuel_inner_clad & -self.lower_shield & +self.rods_bot)
        self.gap_fuel = openmc.Cell(name='celula_gap_fuel', region=-self.fuel_inner_clad & +self.fuel_radius & -self.upper_insulation_top
                                                                & +self.lower_shield)
        self.clad_fuel = openmc.Cell(name='celula_clad_fuel', fill=self.clad_15_15Ti, region=-self.fuel_outer_clad & +self.fuel_inner_clad
                                                                & -self.rods_top & +self.rods_bot)
        self.coolant_fuel = openmc.Cell(name='celula_coolant_fuel', fill=self.refrigerante, region=+self.fuel_outer_clad | 
                                                                        -self.fuel_outer_clad & +self.rods_top |
                                                                        -self.fuel_outer_clad & -self.rods_bot)

        # Para o MOX
        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            self.fuel_mox = openmc.Cell(name='celula_fuel_mox', fill=self.MOX, region=-self.fuel_radius & -self.upper_fuel_column & +self.lower_fuel_column)
            self.insulation_mox = openmc.Cell(name='celula_isolante_mox', fill=self.reflec_ins, region=-self.fuel_radius & -self.upper_insulation_top
                                                                    & +self.upper_fuel_column | 
                                                                    -self.fuel_radius & -self.lower_fuel_column & +self.lower_insulation_bot)
            self.shield_mox = openmc.Cell(name='celula_shield_mox', fill=self.shield, region=-self.fuel_radius & -self.lower_insulation_bot & +self.lower_shield)
            self.plenum_mox = openmc.Cell(name='celula_plenum_mox', region=-self.fuel_inner_clad & -self.upper_gas_plenum
                                                                        & +self.upper_insulation_top)
            self.plugs_mox = openmc.Cell(name='celula_plug_fuel_mox', fill=self.clad_SS316L, region=-self.fuel_inner_clad & -self.rods_top
                                                                    & +self.upper_gas_plenum |
                                                                    -self.fuel_inner_clad & -self.lower_shield & +self.rods_bot)
            self.gap_mox = openmc.Cell(name='celula_gap_fuel_mox', region=-self.fuel_inner_clad & +self.fuel_radius & -self.upper_insulation_top
                                                                    & +self.lower_shield)
            self.clad_mox = openmc.Cell(name='celula_clad_fuel_mox', fill=self.clad_15_15Ti, region=-self.fuel_outer_clad & +self.fuel_inner_clad
                                                                    & -self.rods_top & +self.rods_bot)
            self.coolant_mox = openmc.Cell(name='celula_coolant_fuel_mox', fill=self.refrigerante, region=+self.fuel_outer_clad | 
                                                                            -self.fuel_outer_clad & +self.rods_top |
                                                                            -self.fuel_outer_clad & -self.rods_bot)

        # Células da vareta refletora

        self.refletor = openmc.Cell(name='celula_refletor', fill=self.reflec_ins, region=-self.reflec_radius & -self.upper_gas_plenum & +self.lower_shield)
        self.gap_reflec = openmc.Cell(name='celula_gap_reflec', region=-self.reflec_inner_clad & +self.reflec_radius & -self.upper_gas_plenum
                                                                & +self.lower_shield)
        self.plug_reflec = openmc.Cell(name='celula_plug_reflec', fill=self.clad_SS316L, region=-self.reflec_inner_clad & -self.rods_top
                                                                & +self.upper_gas_plenum |
                                                                -self.reflec_inner_clad & -self.lower_shield & +self.rods_bot)
        self.clad_reflec = openmc.Cell(name='celula_clad_reflec', fill=self.clad_Fe10Cr4AlRE, region=-self.reflec_outer_clad & +self.reflec_inner_clad
                                                                & -self.rods_top & +self.rods_bot)
        self.coolant_reflec = openmc.Cell(name='celula_coolant_reflec', fill=self.refrigerante, region=+self.reflec_outer_clad |
                                                                                    -self.reflec_outer_clad & +self.rods_top |
                                                                                    -self.reflec_outer_clad & -self.rods_bot)


        # Células da vareta de blindagem

        self.blindagem = openmc.Cell(name='celula_blindagem', fill=self.shield, region=-self.shield_radius & -self.upper_gas_plenum & +self.lower_shield)
        self.gap_blindagem = openmc.Cell(name='celula_gap_blindagem', region=-self.shield_inner_clad & +self.shield_radius
                                    & -self.upper_gas_plenum & +self.lower_shield)
        self.plug_blindagem = openmc.Cell(name='celula_plug_blindagem', fill=self.clad_SS316L, region=-self.shield_inner_clad & +self.upper_gas_plenum
                                    & -self.rods_top |
                                    -self.shield_inner_clad & -self.lower_shield & +self.rods_bot)
        self.clad_blindagem = openmc.Cell(name='celula_clad_blindagem', fill=self.clad_Fe10Cr4AlRE, region=-self.shield_outer_clad & +self.shield_inner_clad
                                    & -self.rods_top & +self.rods_bot)
        self.coolant_blindagem = openmc.Cell(name='celula_coolant_blindagem', fill=self.refrigerante, region=+self.shield_outer_clad|
                                        -self.shield_outer_clad & +self.rods_top|
                                        -self.shield_outer_clad & -self.rods_bot)

        # Células da vareta de controle

        self.controle = openmc.Cell(name='celula_controle', fill=self.control, region=-self.shield_radius & +self.control_insertion)
        self.gap_controle = openmc.Cell(name='celula_gap_controle', region=-self.shield_inner_clad & +self.shield_radius & +self.control_insertion)
        self.clad_controle = openmc.Cell(name='celula_clad_controle', fill=self.clad_Fe10Cr4Al, region=-self.shield_outer_clad & +self.shield_inner_clad
                                    & +self.control_insertion)
        self.coolant_controle = openmc.Cell(name='celula_coolant_controle', fill=self.refrigerante, region=+self.shield_outer_clad|
                                        -self.shield_outer_clad & -self.control_insertion)

        # Células da vareta de shut-down

        self.desliga = openmc.Cell(name='celula_desliga', fill=self.shut_down, region=-self.shut_radius & +self.shut_insertion)
        self.gap_desliga = openmc.Cell(name='celula_gap_desliga', region=-self.shut_inner_clad & +self.shut_radius & +self.shut_insertion)
        self.clad_desliga = openmc.Cell(name='celula_clad_desliga', fill=self.clad_Fe10Cr4Al, region=-self.shut_outer_clad & +self.shut_inner_clad & +self.shut_insertion)
        self.coolant_desliga = openmc.Cell(name='celula_coolant_desliga', fill=self.refrigerante, region=+self.shut_outer_clad|
                                    -self.shut_outer_clad & -self.shut_insertion)


        ############ Universos de varetas ##############################################################################################

        self.universo_vareta_combustivel = openmc.Universe(cells=(self.fuel, self.insulation, self.shield_fuel, self.plenum_fuel, self.plugs_fuel, self.gap_fuel, 
                                                                  self.clad_fuel, self.coolant_fuel))

        self.universo_vareta_refletora = openmc.Universe(cells=(self.refletor, self.gap_reflec, self.plug_reflec, self.clad_reflec, self.coolant_reflec))

        self.universo_vareta_blindagem = openmc.Universe(cells=(self.blindagem, self.gap_blindagem, self.plug_blindagem, self.clad_blindagem, self.coolant_blindagem))

        self.universo_vareta_controle = openmc.Universe(cells=(self.controle, self.gap_controle, self.clad_controle, self.coolant_controle))

        self.universo_vareta_desligamento = openmc.Universe(cells=(self.desliga, self.gap_desliga, self.clad_desliga, self.coolant_desliga))

        # Células plano de fundo para universos
        self.celula_Pb     = openmc.Cell(fill=self.refrigerante, region=-self.core_top & +self.core_bot)
        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            self.celula_Pb_mox = openmc.Cell(fill=self.refrigerante, region=-self.core_top & +self.core_bot)

            # Para o MOX
            self.universo_vareta_mox = openmc.Universe(cells=(self.fuel_mox, self.insulation_mox, self.shield_mox, self.plenum_mox, self.plugs_mox, self.gap_mox,
                                                           self.clad_mox, self.coolant_mox))

        ############ Universos de plano de fundo para lattices #########################################################################

        self.universo_Pb     = openmc.Universe(cells=(self.celula_Pb,))
        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            self.universo_Pb_mox = openmc.Universe(cells=(self.celula_Pb_mox,))

        ############ Matrizes de varetas ###############################################################################################

        # Fuel Assemblie - Matriz do elemento combustível
        self.matriz_combustivel = openmc.HexLattice()
        self.matriz_combustivel.center = (0., 0.)
        self.matriz_combustivel.pitch = (1.637,)
        self.matriz_combustivel.orientation = 'x'
        self.matriz_combustivel.outer = self.universo_Pb

        self.anel_combustivel_1 = [self.universo_vareta_combustivel]
        self.anel_combustivel_2 = [self.universo_vareta_combustivel]*6
        self.anel_combustivel_3 = [self.universo_vareta_combustivel]*12
        self.anel_combustivel_4 = [self.universo_vareta_combustivel]*18
        self.anel_combustivel_5 = [self.universo_vareta_combustivel]*24
        self.anel_combustivel_6 = [self.universo_vareta_combustivel]*30

        self.matriz_combustivel.universes = [self.anel_combustivel_6, self.anel_combustivel_5, self.anel_combustivel_4, self.anel_combustivel_3, self.anel_combustivel_2,
                                        self.anel_combustivel_1]
        print(self.matriz_combustivel)

        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            # Fuel Assemblie - Matriz do elemento combustível MOX
            self.matriz_mox = openmc.HexLattice()
            self.matriz_mox.center = (0., 0.)
            self.matriz_mox.pitch = (1.637,)
            self.matriz_mox.orientation = 'x'
            self.matriz_mox.outer = self.universo_Pb_mox

            self.anel_mox_1 = [self.universo_vareta_mox]
            self.anel_mox_2 = [self.universo_vareta_mox]*6
            self.anel_mox_3 = [self.universo_vareta_mox]*12
            self.anel_mox_4 = [self.universo_vareta_mox]*18
            self.anel_mox_5 = [self.universo_vareta_mox]*24
            self.anel_mox_6 = [self.universo_vareta_mox]*30

            self.matriz_mox.universes = [self.anel_mox_6, self.anel_mox_5, self.anel_mox_4, self.anel_mox_3, self.anel_mox_2,
                                            self.anel_mox_1]
            print(self.matriz_mox)

        # Reflector Assemblie - Matriz do elemento refletor

        self.matriz_refletor = openmc.HexLattice()
        self.matriz_refletor.center = (0., 0.)
        self.matriz_refletor.pitch = (2.507,)
        self.matriz_refletor.orientation = 'x'
        self.matriz_refletor.outer = self.universo_Pb

        self.anel_refletor_1 = [self.universo_vareta_refletora]
        self.anel_refletor_2 = [self.universo_vareta_refletora]*6
        self.anel_refletor_3 = [self.universo_vareta_refletora]*12
        self.anel_refletor_4 = [self.universo_vareta_refletora]*18

        self.matriz_refletor.universes = [self.anel_refletor_4, self.anel_refletor_3, self.anel_refletor_2, self.anel_refletor_1]
        print(self.matriz_refletor)

        # Shield Assemblie - Matriz do elemento blindagem

        self.matriz_blindagem = openmc.HexLattice()
        self.matriz_blindagem.center = (0., 0.)
        self.matriz_blindagem.pitch = (3.475,)
        self.matriz_blindagem.orientation = 'x'
        self.matriz_blindagem.outer = self.universo_Pb

        self.anel_blindagem_1 = [self.universo_vareta_blindagem]
        self.anel_blindagem_2 = [self.universo_vareta_blindagem]*6
        self.anel_blindagem_3 = [self.universo_vareta_blindagem]*12

        self.matriz_blindagem.universes = [self.anel_blindagem_3, self.anel_blindagem_2, self.anel_blindagem_1]
        print(self.matriz_blindagem)

        # Control Assemblie - Matriz do elemento controle

        self.matriz_controle = openmc.HexLattice()
        self.matriz_controle.center = (0., 0.)
        self.matriz_controle.pitch = (3.292,)
        self.matriz_controle.orientation = 'x'
        self.matriz_controle.outer = self.universo_Pb

        self.anel_controle_1 = [self.universo_vareta_controle]
        self.anel_controle_2 = [self.universo_vareta_controle]*6
        self.anel_controle_3 = [self.universo_vareta_controle]*12

        self.matriz_controle.universes = [self.anel_controle_3, self.anel_controle_2, self.anel_controle_1]
        print(self.matriz_controle)

        # Shut-down Assemblie - Matriz do elemento segurança

        self.matriz_desligamento = openmc.HexLattice()
        self.matriz_desligamento.center = (0., 0.)
        self.matriz_desligamento.pitch = (4.500,)
        self.matriz_desligamento.orientation = 'x'
        self.matriz_desligamento.outer = self.universo_Pb

        self.anel_desligamento_1 = [self.universo_vareta_desligamento]
        self.anel_desligamento_2 = [self.universo_vareta_desligamento]*6

        self.matriz_desligamento.universes = [self.anel_desligamento_2, self.anel_desligamento_1]
        print(self.matriz_desligamento)

        ##################################################################################################################################
        # Hexágono dos elementos e preenchimento do tubo guia (clad)
        self.inner_hexagono            = openmc.model.HexagonalPrism(edge_length = 9.2,orientation = 'x',)
        self.outer_hexagono            = openmc.model.HexagonalPrism(edge_length = 9.5,orientation = 'x',)
        self.celula_fuel_hex_can       = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono) 
        self.hex_refletor              = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono)
        self.hex_blindagem             = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono)
        self.hex_controle              = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono)
        self.hex_seguranca             = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono)
        self.celula_chumbo_hex_can     = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)
        self.chumbo_refletor           = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)
        self.chumbo_blindagem          = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)
        self.chumbo_controle           = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)
        self.chumbo_seguranca          = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)

        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            # Para o mox
            self.celula_mox_hex_can        = openmc.Cell(fill=self.clad_Fe10Cr4AlRE, region=+self.inner_hexagono)
            self.celula_Pb_mox_hex_can     = openmc.Cell(fill=self.refrigerante, region=+self.outer_hexagono&+self.core_bot&-self.core_top)
        ########## Elementos #############################################################################################################

        # ELEMENTO COMBUSTÍVEL
        self.celula_colocar_combustivel = openmc.Cell(fill=self.matriz_combustivel, region=-self.inner_hexagono)
        self.universo_matriz_combustivel = openmc.Universe(cells=(self.celula_fuel_hex_can, self.celula_colocar_combustivel))

        self.celula_clad_hex_can_comb = openmc.Cell(fill=self.universo_matriz_combustivel, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
        self.universo_elemento_combustivel = openmc.Universe(cells=(self.celula_clad_hex_can_comb, self.celula_chumbo_hex_can))


        if mox_anel_intermediario or mox_anel_externo_1 or mox_anel_externo_2:
            # ELEMENTO COMBUSTÍVEL MOX
            self.celula_colocar_mox = openmc.Cell(fill=self.matriz_mox, region=-self.inner_hexagono)
            self.universo_matriz_mox = openmc.Universe(cells=(self.celula_mox_hex_can, self.celula_colocar_mox))

            self.celula_clad_hex_can_mox = openmc.Cell(fill=self.universo_matriz_mox, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
            self.universo_elemento_mox = openmc.Universe(cells=(self.celula_clad_hex_can_mox, self.celula_Pb_mox_hex_can))

        # Teste
        # cilindro_teste_combustível = openmc.ZCylinder(r=10,)   # limitador do chumbo
        # celula_teste_combustivel = openmc.Cell(fill=self.universo_elemento_combustivel, region=-cilindro_teste_combustível & +self.core_bot & -self.core_top)

        # ELEMENTO REFLETOR
        self.celula_colocar_refletor = openmc.Cell(fill=self.matriz_refletor, region=-self.inner_hexagono)
        self.universo_matriz_refletor = openmc.Universe(cells=(self.hex_refletor, self.celula_colocar_refletor))

        self.celula_clad_hex_can_reflec = openmc.Cell(fill=self.universo_matriz_refletor, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
        self.universo_elemento_refletor = openmc.Universe(cells=(self.celula_clad_hex_can_reflec, self.chumbo_refletor))

        # Teste
        # cilindro_teste_combustível = openmc.ZCylinder(r=10,)   # limitador do chumbo
        # celula_teste_combustivel = openmc.Cell(fill=self.universo_elemento_refletor, region=-cilindro_teste_combustível & +self.core_bot & -self.core_top)

        # ELEMENTO BLINDAGEM
        self.celula_colocar_blindagem = openmc.Cell(fill=self.matriz_blindagem, region=-self.inner_hexagono)
        self.universo_matriz_blindagem = openmc.Universe(cells=(self.hex_blindagem, self.celula_colocar_blindagem))

        self.celula_clad_hex_can_blind = openmc.Cell(fill=self.universo_matriz_blindagem, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
        self.universo_elemento_blindagem = openmc.Universe(cells=(self.celula_clad_hex_can_blind, self.chumbo_blindagem))

        # Teste
        # cilindro_teste_combustível = openmc.ZCylinder(r=10,)   # limitador do chumbo
        # celula_teste_combustivel = openmc.Cell(fill=self.universo_elemento_blindagem, region=-cilindro_teste_combustível & +self.core_bot & -self.core_top)

        # ELEMENTO CONTROLE
        self.celula_colocar_controle = openmc.Cell(fill=self.matriz_controle, region=-self.inner_hexagono)
        self.universo_matriz_controle = openmc.Universe(cells=(self.hex_controle, self.celula_colocar_controle))

        self.celula_clad_hex_can_control = openmc.Cell(fill=self.universo_matriz_controle, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
        self.universo_elemento_controle = openmc.Universe(cells=(self.celula_clad_hex_can_control, self.chumbo_controle))

        # Teste
        # cilindro_teste_combustível = openmc.ZCylinder(r=10,)   # limitador do chumbo
        # celula_teste_combustivel = openmc.Cell(fill=self.universo_elemento_controle, region=-cilindro_teste_combustível & +self.core_bot & -self.core_top)

        # ELEMENTO SEGURANÇA
        self.celula_colocar_desligamento = openmc.Cell(fill=self.matriz_desligamento, region=-self.inner_hexagono)
        self.universo_matriz_desligamento = openmc.Universe(cells=(self.hex_seguranca, self.celula_colocar_desligamento))

        self.celula_clad_hex_can_desliga = openmc.Cell(fill=self.universo_matriz_desligamento, region=-self.outer_hexagono & +self.core_bot & -self.core_top)
        self.universo_elemento_desligamento = openmc.Universe(cells=(self.celula_clad_hex_can_desliga, self.chumbo_seguranca))

        # Teste
        # cilindro_teste_combustível = openmc.ZCylinder(r=10,)   # limitador do chumbo
        # celula_teste_combustivel = openmc.Cell(fill=self.universo_elemento_desligamento, region=-cilindro_teste_combustível & +self.core_bot & -self.core_top)


        ############ Matrizes de elementos ############################################################################################

        self.matriz_nucleo = openmc.HexLattice()
        self.matriz_nucleo.center = (0., 0.)
        self.matriz_nucleo.pitch = (16.600,)
        self.matriz_nucleo.orientation = 'y'
        self.matriz_nucleo.outer = self.universo_Pb

        self.anel_nucleo_1 = [self.universo_elemento_combustivel]

        if mox_anel_intermediario:
            self.anel_nucleo_2 = [self.universo_elemento_mox]*6
        else:
            self.anel_nucleo_2 = [self.universo_elemento_combustivel]*6
        if mox_anel_externo_1:
            self.anel_nucleo_3 = [self.universo_elemento_combustivel] + [self.universo_elemento_mox] + \
                                 [self.universo_elemento_combustivel] + [self.universo_elemento_mox] + \
                                 [self.universo_elemento_combustivel] + [self.universo_elemento_mox] + \
                                 [self.universo_elemento_combustivel] + [self.universo_elemento_mox] + \
                                 [self.universo_elemento_combustivel] + [self.universo_elemento_mox] + \
                                 [self.universo_elemento_combustivel] + [self.universo_elemento_mox]
        elif mox_anel_externo_2:
            self.anel_nucleo_3 = [self.universo_elemento_mox] + [self.universo_elemento_combustivel] + \
                                 [self.universo_elemento_mox] + [self.universo_elemento_combustivel] + \
                                 [self.universo_elemento_mox] + [self.universo_elemento_combustivel] + \
                                 [self.universo_elemento_mox] + [self.universo_elemento_combustivel] + \
                                 [self.universo_elemento_mox] + [self.universo_elemento_combustivel] + \
                                 [self.universo_elemento_mox] + [self.universo_elemento_combustivel]
        else:
            self.anel_nucleo_3 = [self.universo_elemento_combustivel]*12

        self.anel_nucleo_4 = [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2 + \
                             [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2 + \
                             [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2 + \
                             [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2 + \
                             [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2 + \
                             [self.universo_elemento_desligamento] + [self.universo_elemento_controle]*2
        self.anel_nucleo_5 = [self.universo_elemento_refletor]*24
        self.anel_nucleo_6 = [self.universo_Pb] + [self.universo_elemento_blindagem]*4 + \
                             [self.universo_Pb] + [self.universo_elemento_blindagem]*4 + \
                             [self.universo_Pb] + [self.universo_elemento_blindagem]*4 + \
                             [self.universo_Pb] + [self.universo_elemento_blindagem]*4 + \
                             [self.universo_Pb] + [self.universo_elemento_blindagem]*4 + \
                             [self.universo_Pb] + [self.universo_elemento_blindagem]*4

        # Unindo todo o reator

        self.matriz_nucleo.universes = [self.anel_nucleo_6, self.anel_nucleo_5, self.anel_nucleo_4, self.anel_nucleo_3, self.anel_nucleo_2, self.anel_nucleo_1]
        print(self.matriz_nucleo)

        self.celula_inner_core = openmc.Cell(fill=self.matriz_nucleo, region=-self.core_inner_radius & +self.core_bot & -self.core_top)
        self.celula_clad_core = openmc.Cell(fill=self.clad_SS316L, region=-self.core_outer_radius & +self.core_inner_radius & +self.core_bot & -self.core_top)
        self.celula_inner_vessel = openmc.Cell(fill=self.refrigerante, region=-self.vessel_inner_radius & +self.core_outer_radius & +self.core_bot & -self.core_top |
                                            -self.vessel_inner_radius & +self.core_top & -self.vessel_top |
                                            -self.vessel_inner_radius & +self.vessel_bot & -self.core_bot)
        self.celula_clad_vessel = openmc.Cell(fill=self.clad_SS316L, region=+self.vessel_inner_radius & +self.vessel_bot & -self.vessel_top)

        self.universo_SEALER = openmc.Universe(cells=(self.celula_inner_core, self.celula_clad_core, self.celula_inner_vessel, self.celula_clad_vessel))

        self.celula_SEALER = openmc.Cell(fill=self.universo_SEALER, region=-self.vessel_outer_radius)

        self.geometriaReator = openmc.Geometry([self.celula_SEALER])

        self.geometriaReator.export_to_xml()
        # Para plotar os gráficos com nomes diferentes
        self.mox_anel_intermediario = mox_anel_intermediario
        self.mox_anel_externo_1     = mox_anel_externo_1
        self.mox_anel_externo_2     = mox_anel_externo_2

    ################################################
    ########### Definição da Simulação  ############
    ################################################

    def configuracoes(
            self,
            particulas=15000,
            ciclos=400,
            inativo=40,
            atrasados=True):
        print("################################################")
        print("########### Definição da Simulação  ############")
        print("################################################")

        entropy_mesh = openmc.Mesh()
        lower_left = (-5.2577E+01, -5.7310E+01, -7.7348E+01)  # (x, y, z)
        upper_right = (5.2598E+01, 5.7304E+01, 7.7401E+01)    # (x, y, z)
        entropy_mesh.lower_left = lower_left
        entropy_mesh.upper_right = upper_right
        entropy_mesh.dimension = (17, 17, 17)    

        self.ciclos = ciclos
        self.settings = openmc.Settings()
        self.settings.output = {'tallies': False}
        self.settings.particles = particulas
        self.settings.batches = ciclos
        self.settings.inactive = inativo
        self.settings.create_delayed_neutrons = atrasados
        self.settings.source = openmc.IndependentSource(space=openmc.stats.Point())
        self.settings.export_to_xml()

    ################################################"
    ###########         Rodando         ############"
    ################################################"

    def run(
            self,
            mpi=0):
        print("################################################")
        print("###########         Rodando         ############")
        print("################################################")
        if(mpi>0):
            openmc.run(mpi_args=['mpiexec', '-n', str(mpi), '--bind-to', 'numa', '--map-by', 'numa'])
        else:
            openmc.run()

    ################################################
    ###########         Plotagem        ############
    ################################################

    def plotReator(
            self,
            base='xy'):
        print("################################################")
        print("###########         Plotagem        ############")
        print("################################################")
        self.secao_transversal = openmc.Plot.from_geometry(self.geometriaReator)
        self.secao_transversal.type = 'slice'
        self.secao_transversal.basis = base
        #self.secao_transversal.width = [10,200]
        self.secao_transversal.origin = (0,0,55.299)
        self.secao_transversal.filename = base + '_nucleo_' + self.combustivel.name
        if self.mox_anel_intermediario:
            self.secao_transversal.filename += '_intermediario'
        elif self.mox_anel_externo_1:
            self.secao_transversal.filename += '_externo_1'
        elif self.mox_anel_externo_2:
            self.secao_transversal.filename += '_externo_2'
        self.secao_transversal.pixels = [15000,15000]
        self.secao_transversal.color_by = 'material'
        self.secao_transversal.colors = self.colors
        self.plotagem = openmc.Plots((self.secao_transversal,))
        self.plotagem.export_to_xml()  
        openmc.plot_geometry()
    
    ################################################
    ###########         Depleção        ############
    ################################################

    def queima(
            self,
            timesteps,
            power,
            chain_file,
            timestep_units='d',
            diff=False,
            results_file=""):
        print("################################################")
        print("###########         Depleção        ############")
        print("################################################")

        # Set up depletion operator
        model = openmc.model.Model(self.geometriaReator, self.materials, self.settings)
        if diff:
            model.differentiate_depletable_mats(diff_volume_method = 'divide equally')

        if not os.path.exists(results_file): #Inicia uma queima nova
            op = openmc.deplete.CoupledOperator(model, chain_file, diff_burnable_mats=diff)
        else: #Continua uma queima de onde parou
            results = openmc.deplete.Results.from_hdf5(results_file)
            op = openmc.deplete.CoupledOperator(model, chain_file, diff_burnable_mats=diff, prev_results=results)
        
        # Deplete 
        CF4 = openmc.deplete.CF4Integrator(operator=op, timesteps=timesteps, power=power, timestep_units=timestep_units) 
        CF4.integrate()

    ################################################
    ############ Definição dos Tallies  ############
    ################################################

    def talliesReaction(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############        Reaction        ############")
        print("################################################")

        ############# TALLIES POR CÉLULAS ##############

        # Total reaction rate
        total_tally = openmc.Tally(name='Taxa de reação total no combustível')
        total_tally.filters = [openmc.CellFilter(self.fuel)]
        total_tally.scores.append('total')

        # Elastic scattering reaction rate
        elastic_tally = openmc.Tally(name='Taxa de reação de espalhamento elastica no combustível')
        elastic_tally.filters = [openmc.CellFilter(self.fuel)]
        elastic_tally.scores.append('elastic')

        # Total scattering reaction rate
        scatter_tally = openmc.Tally(name='Taxa de reação de espalhamento total no combustível')
        scatter_tally.filters = [openmc.CellFilter(self.fuel)]
        scatter_tally.scores.append('scatter')

        # Absorption rate
        absorption_tally = openmc.Tally(name='Taxa total de absorção no combustível')
        absorption_tally.filters = [openmc.CellFilter(self.fuel)]
        absorption_tally.scores.append('absorption')

        # Captura Radiativa
        gamma_tally = openmc.Tally(name='Taxa de captura radiativa no combustível')
        gamma_tally.filters = [openmc.CellFilter(self.fuel)]
        gamma_tally.scores.append('(n,gamma)')

        # Fission rate
        fission_tally = openmc.Tally(name='Taxa total de reacao de fissao no combustível')
        fission_tally.filters = [openmc.CellFilter(self.fuel)]
        fission_tally.scores.append('fission')

        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([absorption_tally, fission_tally, gamma_tally, scatter_tally, total_tally, elastic_tally])
        tallies.export_to_xml()

    def talliesInverseVelocity(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############    Inverse-Velocity    ############")
        print("################################################")

        ############# TALLIES ##############

        tally_inverse = openmc.Tally(name='Inverse-velocity')
        tally_inverse.scores.append('inverse-velocity')

        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([tally_inverse])
        tallies.export_to_xml()        

    def talliesNU(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############      Nu / Fission      ############")
        print("################################################")

        ############# TALLIES ##############

        tally_nu = openmc.Tally(name='nu')
        tally_nu.scores.append('nu-fission')
        tally_nu.nuclides = ['U235','U238','Pu239']

        tally_fission = openmc.Tally(name='reaction rate')
        tally_fission.scores.append('fission')
        tally_fission.nuclides = ['U235','U238','Pu239']

        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([tally_nu, tally_fission])
        tallies.export_to_xml()

    def talliesEspectroFuel(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############          Fuel          ############")
        print("################################################")

        ############# TALLIES POR CÉLULAS ##############

        energy_filter = openmc.EnergyFilter([1.0000E-05, 1.1220E-05, 1.2589E-05, 1.4125E-05, 1.5849E-05, 1.7783E-05, 1.9953E-05, 2.2387E-05, 2.5119E-05, 2.8184E-05, 3.1623E-05, 3.5481E-05, 3.9811E-05, 4.4668E-05, 5.0119E-05, 5.6234E-05, 6.3096E-05, 7.0795E-05, 7.9433E-05, 8.9125E-05, 1.0000E-04, 1.1220E-04, 1.2589E-04, 1.4125E-04, 1.5849E-04, 1.7783E-04, 1.9953E-04, 2.2387E-04, 2.5119E-04, 2.8184E-04, 3.1623E-04, 3.5481E-04, 3.9811E-04, 4.4668E-04, 5.0119E-04, 5.6234E-04, 6.3096E-04, 7.0795E-04, 7.9433E-04, 8.9125E-04, 1.0000E-03, 1.1220E-03, 1.2589E-03, 1.4125E-03, 1.5849E-03, 1.7783E-03, 1.9953E-03, 2.2387E-03, 2.5119E-03, 2.8184E-03, 3.1623E-03, 3.5481E-03, 3.9811E-03, 4.4668E-03, 5.0119E-03, 5.6234E-03, 6.3096E-03, 7.0795E-03, 7.9433E-03, 8.9125E-03, 1.0000E-02, 1.1220E-02, 1.2589E-02, 1.4125E-02, 1.5849E-02, 1.7783E-02, 1.9953E-02, 2.2387E-02, 2.5119E-02, 2.8184E-02, 3.1623E-02, 3.5481E-02, 3.9811E-02, 4.4668E-02, 5.0119E-02, 5.6234E-02, 6.3096E-02, 7.0795E-02, 7.9433E-02, 8.9125E-02, 1.0000E-01, 1.1220E-01, 1.2589E-01, 1.4125E-01, 1.5849E-01, 1.7783E-01, 1.9953E-01, 2.2387E-01, 2.5119E-01, 2.8184E-01, 3.1623E-01, 3.5481E-01, 3.9811E-01, 4.4668E-01, 5.0119E-01, 5.6234E-01, 6.3096E-01, 7.0795E-01, 7.9433E-01, 8.9125E-01, 1.0000E+00, 1.1220E+00, 1.2589E+00, 1.4125E+00, 1.5849E+00, 1.7783E+00, 1.9953E+00, 2.2387E+00, 2.5119E+00, 2.8184E+00, 3.1623E+00, 3.5481E+00, 3.9811E+00, 4.4668E+00, 5.0119E+00, 5.6234E+00, 6.3096E+00, 7.0795E+00, 7.9433E+00, 8.9125E+00, 1.0000E+01, 1.1220E+01, 1.2589E+01, 1.4125E+01, 1.5849E+01, 1.7783E+01, 1.9953E+01, 2.2387E+01, 2.5119E+01, 2.8184E+01, 3.1623E+01, 3.5481E+01, 3.9811E+01, 4.4668E+01, 5.0119E+01, 5.6234E+01, 6.3096E+01, 7.0795E+01, 7.9433E+01, 8.9125E+01, 1.0000E+02, 1.1220E+02, 1.2589E+02, 1.4125E+02, 1.5849E+02, 1.7783E+02, 1.9953E+02, 2.2387E+02, 2.5119E+02, 2.8184E+02, 3.1623E+02, 3.5481E+02, 3.9811E+02, 4.4668E+02, 5.0119E+02, 5.6234E+02, 6.3096E+02, 7.0795E+02, 7.9433E+02, 8.9125E+02, 1.0000E+03, 1.1220E+03, 1.2589E+03, 1.4125E+03, 1.5849E+03, 1.7783E+03, 1.9953E+03, 2.2387E+03, 2.5119E+03, 2.8184E+03, 3.1623E+03, 3.5481E+03, 3.9811E+03, 4.4668E+03, 5.0119E+03, 5.6234E+03, 6.3096E+03, 7.0795E+03, 7.9433E+03, 8.9125E+03, 1.0000E+04, 1.1220E+04, 1.2589E+04, 1.4125E+04, 1.5849E+04, 1.7783E+04, 1.9953E+04, 2.2387E+04, 2.5119E+04, 2.8184E+04, 3.1623E+04, 3.5481E+04, 3.9811E+04, 4.4668E+04, 5.0119E+04, 5.6234E+04, 6.3096E+04, 7.0795E+04, 7.9433E+04, 8.9125E+04, 1.0000E+05, 1.1220E+05, 1.2589E+05, 1.4125E+05, 1.5849E+05, 1.7783E+05, 1.9953E+05, 2.2387E+05, 2.5119E+05, 2.8184E+05, 3.1623E+05, 3.5481E+05, 3.9811E+05, 4.4668E+05, 5.0119E+05, 5.6234E+05, 6.3096E+05, 7.0795E+05, 7.9433E+05, 8.9125E+05, 1.0000E+06, 1.1220E+06, 1.2589E+06, 1.4125E+06, 1.5849E+06, 1.7783E+06, 1.9953E+06, 2.2387E+06, 2.5119E+06, 2.8184E+06, 3.1623E+06, 3.5481E+06, 3.9811E+06, 4.4668E+06, 5.0119E+06, 5.6234E+06, 6.3096E+06, 7.0795E+06, 7.9433E+06, 8.9125E+06, 1.0000E+07, 1.1220E+07, 1.2589E+07, 1.4125E+07, 1.5849E+07, 1.7783E+07, 1.9953E+07, 2.2387E+07, 2.5119E+07, 2.8184E+07, 3.1623E+07, 3.5481E+07, 3.9811E+07, 4.4668E+07, 5.0119E+07, 5.6234E+07, 6.3096E+07, 7.0795E+07, 7.9433E+07, 8.9125E+07, 1.0000E+08])
        fuel_element_tally = openmc.Tally(name='Fluxo no universo combustível') # F34
        fuel_element_tally.filters = [openmc.CellFilter(self.fuel),energy_filter]
        fuel_element_tally.scores.append('flux')

        nu_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = [-156.3, 269.3])

        fission_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = [-156.3, 269.3])

        nu_filter      = openmc.MeshFilter(nu_radial)
        fission_filter = openmc.MeshFilter(fission_radial)

        tally2 = openmc.Tally(name='nu')
        tally2.filters.append(nu_filter)
        tally2.scores.append('nu-fission')

        tally3 = openmc.Tally(name='reaction rate')
        tally3.filters.append(fission_filter)
        tally3.scores.append('fission')


        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([fuel_element_tally, tally2, tally3])
        tallies.export_to_xml()
    
    def talliesEspectroCore(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############         Core           ############")
        print("################################################")

        ############# TALLIES POR CÉLULAS ##############

        energy_filter = openmc.EnergyFilter([1.0000E-05, 1.1220E-05, 1.2589E-05, 1.4125E-05, 1.5849E-05, 1.7783E-05, 1.9953E-05, 2.2387E-05, 2.5119E-05, 2.8184E-05, 3.1623E-05, 3.5481E-05, 3.9811E-05, 4.4668E-05, 5.0119E-05, 5.6234E-05, 6.3096E-05, 7.0795E-05, 7.9433E-05, 8.9125E-05, 1.0000E-04, 1.1220E-04, 1.2589E-04, 1.4125E-04, 1.5849E-04, 1.7783E-04, 1.9953E-04, 2.2387E-04, 2.5119E-04, 2.8184E-04, 3.1623E-04, 3.5481E-04, 3.9811E-04, 4.4668E-04, 5.0119E-04, 5.6234E-04, 6.3096E-04, 7.0795E-04, 7.9433E-04, 8.9125E-04, 1.0000E-03, 1.1220E-03, 1.2589E-03, 1.4125E-03, 1.5849E-03, 1.7783E-03, 1.9953E-03, 2.2387E-03, 2.5119E-03, 2.8184E-03, 3.1623E-03, 3.5481E-03, 3.9811E-03, 4.4668E-03, 5.0119E-03, 5.6234E-03, 6.3096E-03, 7.0795E-03, 7.9433E-03, 8.9125E-03, 1.0000E-02, 1.1220E-02, 1.2589E-02, 1.4125E-02, 1.5849E-02, 1.7783E-02, 1.9953E-02, 2.2387E-02, 2.5119E-02, 2.8184E-02, 3.1623E-02, 3.5481E-02, 3.9811E-02, 4.4668E-02, 5.0119E-02, 5.6234E-02, 6.3096E-02, 7.0795E-02, 7.9433E-02, 8.9125E-02, 1.0000E-01, 1.1220E-01, 1.2589E-01, 1.4125E-01, 1.5849E-01, 1.7783E-01, 1.9953E-01, 2.2387E-01, 2.5119E-01, 2.8184E-01, 3.1623E-01, 3.5481E-01, 3.9811E-01, 4.4668E-01, 5.0119E-01, 5.6234E-01, 6.3096E-01, 7.0795E-01, 7.9433E-01, 8.9125E-01, 1.0000E+00, 1.1220E+00, 1.2589E+00, 1.4125E+00, 1.5849E+00, 1.7783E+00, 1.9953E+00, 2.2387E+00, 2.5119E+00, 2.8184E+00, 3.1623E+00, 3.5481E+00, 3.9811E+00, 4.4668E+00, 5.0119E+00, 5.6234E+00, 6.3096E+00, 7.0795E+00, 7.9433E+00, 8.9125E+00, 1.0000E+01, 1.1220E+01, 1.2589E+01, 1.4125E+01, 1.5849E+01, 1.7783E+01, 1.9953E+01, 2.2387E+01, 2.5119E+01, 2.8184E+01, 3.1623E+01, 3.5481E+01, 3.9811E+01, 4.4668E+01, 5.0119E+01, 5.6234E+01, 6.3096E+01, 7.0795E+01, 7.9433E+01, 8.9125E+01, 1.0000E+02, 1.1220E+02, 1.2589E+02, 1.4125E+02, 1.5849E+02, 1.7783E+02, 1.9953E+02, 2.2387E+02, 2.5119E+02, 2.8184E+02, 3.1623E+02, 3.5481E+02, 3.9811E+02, 4.4668E+02, 5.0119E+02, 5.6234E+02, 6.3096E+02, 7.0795E+02, 7.9433E+02, 8.9125E+02, 1.0000E+03, 1.1220E+03, 1.2589E+03, 1.4125E+03, 1.5849E+03, 1.7783E+03, 1.9953E+03, 2.2387E+03, 2.5119E+03, 2.8184E+03, 3.1623E+03, 3.5481E+03, 3.9811E+03, 4.4668E+03, 5.0119E+03, 5.6234E+03, 6.3096E+03, 7.0795E+03, 7.9433E+03, 8.9125E+03, 1.0000E+04, 1.1220E+04, 1.2589E+04, 1.4125E+04, 1.5849E+04, 1.7783E+04, 1.9953E+04, 2.2387E+04, 2.5119E+04, 2.8184E+04, 3.1623E+04, 3.5481E+04, 3.9811E+04, 4.4668E+04, 5.0119E+04, 5.6234E+04, 6.3096E+04, 7.0795E+04, 7.9433E+04, 8.9125E+04, 1.0000E+05, 1.1220E+05, 1.2589E+05, 1.4125E+05, 1.5849E+05, 1.7783E+05, 1.9953E+05, 2.2387E+05, 2.5119E+05, 2.8184E+05, 3.1623E+05, 3.5481E+05, 3.9811E+05, 4.4668E+05, 5.0119E+05, 5.6234E+05, 6.3096E+05, 7.0795E+05, 7.9433E+05, 8.9125E+05, 1.0000E+06, 1.1220E+06, 1.2589E+06, 1.4125E+06, 1.5849E+06, 1.7783E+06, 1.9953E+06, 2.2387E+06, 2.5119E+06, 2.8184E+06, 3.1623E+06, 3.5481E+06, 3.9811E+06, 4.4668E+06, 5.0119E+06, 5.6234E+06, 6.3096E+06, 7.0795E+06, 7.9433E+06, 8.9125E+06, 1.0000E+07, 1.1220E+07, 1.2589E+07, 1.4125E+07, 1.5849E+07, 1.7783E+07, 1.9953E+07, 2.2387E+07, 2.5119E+07, 2.8184E+07, 3.1623E+07, 3.5481E+07, 3.9811E+07, 4.4668E+07, 5.0119E+07, 5.6234E+07, 6.3096E+07, 7.0795E+07, 7.9433E+07, 8.9125E+07, 1.0000E+08])
        fuel_element_tally = openmc.Tally(name='Fluxo no universo combustível') # F34
        fuel_element_tally.filters = [openmc.CellFilter(self.celula_inner_core),energy_filter]
        fuel_element_tally.scores.append('flux')

        nu_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = [-156.3, 269.3])

        fission_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = [-156.3, 269.3])

        nu_filter      = openmc.MeshFilter(nu_radial)
        fission_filter = openmc.MeshFilter(fission_radial)

        tally2 = openmc.Tally(name='nu')
        tally2.filters.append(nu_filter)
        tally2.scores.append('nu-fission')

        tally3 = openmc.Tally(name='reaction rate')
        tally3.filters.append(fission_filter)
        tally3.scores.append('fission')


        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([fuel_element_tally, tally2, tally3])
        tallies.export_to_xml()

    def talliesMeshAxial(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############        MeshAxial       ############")
        print("################################################")

        ########## MESH AXIAL PERSONALIZADO ###########
        # Pontos de divisão da malha cilíndrica
        z_divisions = np.linspace(-76.3,113.3,151).tolist()   # Divide a altura em intervalos iguais e o .tolist() passa o array numpy para um array normal
        print(z_divisions)
        r_divisions = [0.0, 87.4]                            # Raio do cilindro

        # Malha cilíndrica personalizada
        mesh_axial = openmc.CylindricalMesh(r_grid = (r_divisions), z_grid = (z_divisions))

        # Filtro de malha
        mesh_filter_axial = openmc.MeshFilter(mesh_axial)

        # Tally de malha
        tally_axial = openmc.Tally(name='TMESH4_Axial_Custom_Cylindrical')
        tally_axial.filters.append(mesh_filter_axial)
        tally_axial.scores.append('flux')                         

        tally2_axial = openmc.Tally(name='nu')
        tally2_axial.scores.append('nu-fission')

        tally3_axial = openmc.Tally(name='reaction rate')
        tally3_axial.scores.append('fission')
        ############## Coleção de tallies ##############
        tallies = openmc.Tallies([tally_axial,tally2_axial,tally3_axial])
        tallies.export_to_xml()

    def talliesMeshRadial(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############       MeshRadial       ############")
        print("################################################")

        ########## MESH RADIAL PERSONALIZADO ###########
        # Pontos de divisão da malha cilíndrica 
        self.r_divisions = np.linspace(0.0,137.4,151).tolist()    # Divide o raio em intervalos iguais e o .tolist() passa o array numpy para um array normal
        self.z_divisions = [self.lower_fuel_column.z0, self.upper_fuel_column.z0]                        # Altura do cilindro

        # Malha cilíndrica personalizada
        mesh_radial = openmc.CylindricalMesh(r_grid = (self.r_divisions), z_grid = (self.z_divisions))

        nu_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = self.z_divisions)

        fission_radial = openmc.CylindricalMesh(r_grid = [0.0 , 137.4], z_grid = self.z_divisions)

        # Filtro de malha
        mesh_filter_radial = openmc.MeshFilter(mesh_radial)
        nu_filter_radial   = openmc.MeshFilter(nu_radial)
        fission_filter_radial   = openmc.MeshFilter(fission_radial)

        # Tally de malha
        tally_radial = openmc.Tally(name='TMESH4_Radial_Custom_Cylindrical')
        tally_radial.filters.append(mesh_filter_radial)
        tally_radial.scores.append('flux')

        tally2_radial = openmc.Tally(name='nu')
        tally2_radial.filters.append(nu_filter_radial)
        tally2_radial.scores.append('nu-fission')

        tally3_radial = openmc.Tally(name='reaction rate')
        tally3_radial.filters.append(fission_filter_radial)
        tally3_radial.scores.append('fission')

        ############## Coleção de tallies ##############
        tallies = openmc.Tallies([tally_radial,tally2_radial,tally3_radial])
        tallies.export_to_xml()

    def talliesPotenciaElemento(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############        Potencia        ############")
        print("################################################")

        ############# TALLIES POR CÉLULAS ##############

        # Fission rate
        tally_fiss = openmc.Tally()
        tally_fiss.filters = [openmc.DistribcellFilter(self.celula_colocar_combustivel)]
        tally_fiss.scores.append('fission')

        # Fission rate over all the system
        fission_all = openmc.Tally(name='Taxa de fissao media do sistema')
        fission_all.scores.append('fission')

        # Total heating
        heating_tally = openmc.Tally(name='Energia proveniente de fissoes') # Localmente
        heating_tally.scores.append('heating-local')

        ############## Coleção de tallies ##############
        
        tallies = openmc.Tallies([heating_tally, tally_fiss, fission_all])
        tallies.export_to_xml()

    def talliesPotenciaPin(self):
        print("################################################")
        print("############ Definição dos Tallies  ############")
        print("############        Potencia        ############")
        print("################################################")

        ############# TALLIES POR CÉLULAS ##############

        # Total heating
        heating_tally = openmc.Tally()
        heating_tally.scores.append('heating-local')

        # Fission rate over all the system
        fission_all = openmc.Tally(name='Taxa de fissao media do sistema')
        fission_all.scores.append('fission')

        # Fission rate
        tally_fission = openmc.Tally(name='Taxa de reacao de fissao')
        tally_fission.filters = [openmc.DistribcellFilter(self.fuel)]
        tally_fission.scores.append('fission')

        ############## Coleção de tallies ##############

        tallies = openmc.Tallies([tally_fission, heating_tally, fission_all])
        tallies.export_to_xml()

    ################################################
    ############   Trabalhando Dados    ############
    ################################################

    def trabalhandoDadosInverseVelocity(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############    Inverse-Velocity    ############")
        print("################################################")
    
        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados do fuel_element_tally
        prompt_lifetime = sp.get_tally(scores=['inverse-velocity'])

        lifetime_mean    = prompt_lifetime.mean
        lifetime_std_dev = prompt_lifetime.std_dev

        print('')
        print(" Prompt removal lifetime:")
        print('')
        print("\t", lifetime_mean[0][0][0], '+/-', lifetime_std_dev[0][0][0]) 

    def trabalhandoDadosNU(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############        Nu / Fiss       ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados 
        nu   = sp.get_tally(scores=['nu-fission'])
        fission = sp.get_tally(scores=['fission'])

        nu_mean      =   nu.mean
        fission_mean =   fission.mean

        # Retirando taxa de reacao de fissao 
        print('')
        print(" Neutrons per fission:")
        print('')
        print("\t", nu_mean[0][0][0]/fission_mean[0][0][0],"[neutrons/fissão]")

    def trabalhandoDadosReaction(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############        Reaction        ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados do fuel_element_tally
        absorption = sp.get_tally(scores=['absorption'])
        fission    = sp.get_tally(scores=['fission'])
        gamma      = sp.get_tally(scores=['(n,gamma)'])
        total      = sp.get_tally(scores=['total'])
        scatter    = sp.get_tally(scores=['scatter'])
        #elastic    = sp.get_tally(scores=['elastic'], name='Taxa de reação de espalhamento elastica no combustível')

        absorption_mean    =   absorption.mean
        absorption_std_dev =   absorption.std_dev
        gamma_mean         =   gamma.mean
        gamma_std_dev      =   gamma.std_dev
        total_mean         =   total.mean
        total_std_dev      =   total.std_dev
        scatter_mean       =   scatter.mean
        scatter_std_dev    =   scatter.std_dev
        #elastic_mean       =   elastic.mean
        #elastic_std_dev    =   elastic.std_dev
        fission_mean       =   fission.mean
        fission_std_dev    =   fission.std_dev

        print('Espalhamento total no combustível    :', scatter_mean[0][0], ' +/-', scatter_std_dev[0][0], ' Reactions per source particle')
        #print('Espalhamento elástico no combustível :', elastic_mean[0][0], ' +/-', elastic_std_dev[0][0], ' Reactions per source particle')
        print('Reação total no combustível          :', total_mean[0][0], ' +/-', total_std_dev[0][0], ' Reactions per source particle')
        print('Absorção no combustível              :', absorption_mean[0][0], ' +/-', absorption_std_dev[0][0], ' Reactions per source particle')
        print('Captura radiativa no combustível     :', gamma_mean[0][0], ' +/-', gamma_std_dev[0][0], ' Reactions per source particle')
        print('Fissão no combustível                :', fission_mean[0][0], ' +/-', fission_std_dev[0][0], ' Reactions per source particle')
        #print('Razão de fissão sob absorção         :', fission_mean[0][0]/absorption_mean[0][0])

    def trabalhandoDadosEspectroFuel(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############          Fuel          ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados do fuel_element_tally
        flux = sp.get_tally(scores=['flux'])
        nu   = sp.get_tally(scores=['nu-fission'])
        fission = sp.get_tally(scores=['fission'])

        flux_meanshape  =   flux.mean.shape
        flux_mean       =   flux.mean
        flux_std_dev    =   flux.std_dev

        nu_meanshape  =   nu.mean.shape
        nu_mean       =   nu.mean
        nu_std_dev    =   nu.std_dev

        fission_meanshape  =   fission.mean.shape
        fission_mean       =   fission.mean
        fission_std_dev    =   fission.std_dev

        ################## Calculando a média de fluxo para cara intervalo de energia ###################

        # Show a Pandas dataframe
        df = flux.get_pandas_dataframe()
        print(df)

        # Retirando o keff
        print('')
        keff = sp.keff
        keff_error = keff.std_dev
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff)
        print('')

        # Retirando o numero medio de fissoes por fonte
        print('')
        print("nu-fission:")
        print('')
        print("\t", nu_mean[0][0],"\t","+/- ", nu_std_dev[0][0], "[neutrons/source]")

        # Retirando taxa de reacao de fissao 
        print('')
        print("Fission reaction rate:")
        print('')
        print("\t", fission_mean[0][0],"\t","+/- ", fission_std_dev[0][0], "[fissions/source]")

        # Retirando o fluxo
        print('')
        print("Fluxo por intervalo de energia:")
        print('')

        P      = 8.0000E+06  #(W ou J/s)
        Q      = 2.0E+08  #(eV)
        v      = nu_mean[0][0][0]/fission_mean[0][0][0]     
        volume = 1.55975E+02 # cm³             

        # Fator de conversao
        f = v*P/(1.60218*10**(-19)*Q*keff.nominal_value)

        fluxo = []
        fluxo_std  = []
        for i in range(0,260):
            mean_open = f*flux_mean[i][0][0]/volume
            std_open  = f*flux_std_dev[i][0][0]/volume
            flux_cientifico = format(mean_open, '.4e')
            flux_std_cientifico = format(std_open, '.4e')
            fluxo.append(flux_cientifico)
            fluxo_std.append(flux_std_cientifico)
            #print("  Intervalo ", i,": ","\t"," Fluxo : ", flux_cientifico, "+/-", flux_std_cientifico, "[neutrons/cm².s]")
        
        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################

        # Propagação de erros no fator de conversao
        uncertainty = []
        for i in range(0,260):
            error_flux_i = flux_std_dev[i][0][0]                                                                          # Erro associado a flux_std_dev[i]
            term_flux_1 = error_flux_i * f / volume                                                                       # Derivada parcial em relação a flux_mean[i]
            term_flux_2 = flux_mean[i][0][0] * (-v*P/(1.60218*10**(-19)*Q*(keff.nominal_value)**2)) * keff_error / volume # Derivada parcial em relação a keff
            error_fluxo_i = np.sqrt(term_flux_1**2 + term_flux_2**2)                                                      # Erro total
            erro_final_i = format(error_fluxo_i, '.4e')
            uncertainty.append(erro_final_i)       

        for i in range(0,260):
            print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo[i], "+/-", uncertainty[i], "[neutron/cm².s]")

    def trabalhandoDadosEspectroCore(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############          Core          ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados do fuel_element_tally
        flux = sp.get_tally(scores=['flux'])
        nu   = sp.get_tally(scores=['nu-fission'])
        fission = sp.get_tally(scores=['fission'])

        flux_meanshape  =   flux.mean.shape
        flux_mean       =   flux.mean
        flux_std_dev    =   flux.std_dev

        nu_meanshape  =   nu.mean.shape
        nu_mean       =   nu.mean
        nu_std_dev    =   nu.std_dev

        fission_meanshape  =   fission.mean.shape
        fission_mean       =   fission.mean
        fission_std_dev    =   fission.std_dev

        ################## Calculando a média de fluxo para cara intervalo de energia ###################

        # Show a Pandas dataframe
        df = flux.get_pandas_dataframe()
        print(df)
        
        # Retirando o keff
        print('')
        keff = sp.keff
        keff_error = keff.std_dev
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff)
        print('')

        # Retirando o numero medio de fissoes por fonte
        print('')
        print("nu-fission:")
        print('')
        print("\t", nu_mean[0][0],"\t","+/- ", nu_std_dev[0][0], "[neutrons/source]")

        # Retirando taxa de reacao de fissao 
        print('')
        print("Fission reaction rate:")
        print('')
        print("\t", fission_mean[0][0],"\t","+/- ", fission_std_dev[0][0], "[fissions/source]")

        # Retirando o fluxo
        print('')
        print("Fluxo por intervalo de energia:")
        print('')

        P      = 8.0000E+06  #(W ou J/s)
        Q      = 2.0E+08  #(eV)
        v      = nu_mean[0][0][0]/fission_mean[0][0][0]     
        volume = 4344141.3416 # cm³             

        #Flux?
        f = v*P/(1.60218*10**(-19)*Q*keff.nominal_value)

        fluxo = []
        fluxo_std  = []
        for i in range(0,260):
            mean_open = f*flux_mean[i][0][0]/volume
            std_open  = f*flux_std_dev[i][0][0]/volume
            flux_cientifico = format(mean_open, '.4e')
            flux_std_cientifico = format(std_open, '.4e')
            fluxo.append(flux_cientifico)
            fluxo_std.append(flux_std_cientifico)
            #print("  Intervalo ", i,": ","\t"," Fluxo : ", flux_cientifico, "+/-", flux_std_cientifico, "[neutrons/cm².s]")
        
        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################

        # Propagação de erros no fator de conversao
        uncertainty = []
        for i in range(0,260):
            error_flux_i = flux_std_dev[i][0][0]                                                                          # Erro associado a flux_std_dev[i]
            term_flux_1 = error_flux_i * f / volume                                                                       # Derivada parcial em relação a flux_mean[i]
            term_flux_2 = flux_mean[i][0][0] * (-v*P/(1.60218*10**(-19)*Q*(keff.nominal_value)**2)) * keff_error / volume # Derivada parcial em relação a keff
            error_fluxo_i = np.sqrt(term_flux_1**2 + term_flux_2**2)                                                      # Erro total
            erro_final_i = format(error_fluxo_i, '.4e')
            uncertainty.append(erro_final_i)       

        for i in range(0,260):
            print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo[i], "+/-", uncertainty[i], "[neutron/cm².s]")

    def trabalhandoDadosMeshAxial(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############       MeshAxial        ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')
        
        # Acesse os resultados do tally radial
        flux      = sp.get_tally(scores=['flux'])
        nu        = sp.get_tally(scores=['nu-fission'])
        fission   = sp.get_tally(scores=['fission'])
        
        nu_meanshape = nu.mean.shape
        nu_mean      = nu.mean
        nu_std_dev   = nu.std_dev
        
        flux_meanshape = flux.mean.shape
        flux_mean      = flux.mean
        flux_std_dev   = flux.std_dev
        
        fission_meanshape = fission.mean.shape
        fission_mean      = fission.mean
        fission_std_dev   = fission.std_dev
        
        # Retirando o keff
        print('')
        keff = sp.keff
        keff_error = keff.std_dev
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff , "[neutrons/source]")
        print('')
        
        # Retirando o mesh radial
        print('')
        print("Mesh Axial:")
        print('')
        P = 8.0000E+06  #(W ou J/s)
        Q = 2.0E+08  #(eV)
        v = nu_mean[0][0][0]/fission_mean[0][0][0]     
        
        # Volumes das areas do mesh
        volume = 3.14159265359 * (87.4**2) * 1.264  # (pi*r^2)*altura
        
        # Fator de conversao
        f = v*P/(1.60218*10**(-19)*Q*keff.nominal_value)

        fluxo = []
        fluxo_std = []

        for i in range(0,150):
            flux=f*flux_mean[i][0][0]/volume
            fluxo_cientifico = format(flux, '.4e')
            fluxo.append(fluxo_cientifico)
            incerteza=f*flux_std_dev[i][0][0]/volume
            inc_cientifico = format(incerteza, '.4e')
            fluxo_std.append(inc_cientifico)
            #print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo_cientifico, "+/-", inc_cientifico, "[neutrons/cm².s]")
        
        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################

        # Propagação de erros no fator de conversao
        uncertainty = []
        for i in range(0,150):
            error_flux_i = flux_std_dev[i][0][0]                                                                          # Erro associado a flux_std_dev[i]
            term_flux_1 = error_flux_i * f / volume                                                                       # Derivada parcial em relação a flux_mean[i]
            term_flux_2 = flux_mean[i][0][0] * (-v*P/(1.60218*10**(-19)*Q*(keff.nominal_value)**2)) * keff_error / volume # Derivada parcial em relação a keff
            error_fluxo_i = np.sqrt(term_flux_1**2 + term_flux_2**2)                                                      # Erro total
            erro_final_i = format(error_fluxo_i, '.4e')
            uncertainty.append(erro_final_i)       

        for i in range(0,150):
            print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo[i], "+/-", uncertainty[i], "[neutron/cm².s]")

    def trabalhandoDadosMeshRadial(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############       MeshRadial       ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Acesse os resultados do tally radial
        flux      = sp.get_tally(scores=['flux'])
        nu        = sp.get_tally(scores=['nu-fission'])
        fission   = sp.get_tally(scores=['fission'])

        print(flux)
        print(nu)
        print(fission)

        nu_meanshape = nu.mean.shape
        nu_mean      = nu.mean
        nu_std_dev   = nu.std_dev

        flux_meanshape = flux.mean.shape
        flux_mean      = flux.mean
        flux_std_dev   = flux.std_dev

        fission_meanshape = fission.mean.shape
        fission_mean      = fission.mean
        fission_std_dev   = fission.std_dev

        # Retirando o keff
        print('')
        keff = sp.keff
        keff_error = keff.std_dev
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff, "[neutrons/source]")
        print('')

        # Retirando o numero medio de fissoes por fonte
        print('')
        print("nu-fission:")
        print('')
        print("\t", nu_mean[0][0],"\t","+/- ", nu_std_dev[0][0], "[Neutrons/source]")

        # Retirando taxa de reacao de fissao 
        print('')
        print("Fission reaction rate:")
        print('')
        print("\t", fission_mean[0][0],"\t","+/- ", fission_std_dev[0][0], "[Fissions/source]")

        # Retirando o mesh radial
        print('')
        print("Mesh Radial:")
        print('')

        P = 8.0000E+06  #(W ou J/s)
        Q = 2.0E+08  #(eV)
        v = nu_mean[0][0][0]/fission_mean[0][0][0] 

        self.r_divisions = np.linspace(0.0,137.4,151).tolist()
        self.z_divisions = [self.lower_fuel_column.z0, self.upper_fuel_column.z0]                    

        # Volumes das areas do mesh
        volume = []
        for i in range(0, 150):  # Use o número apropriado de intervalos
            r1 = self.r_divisions[i]
            r2 = self.r_divisions[i + 1]
            h = self.z_divisions[1] - self.z_divisions[0]
            volume.append(3.14159265359 * (r2**2 - r1**2) * h)
            #print("\t","Intervalo:  ", i,"\t", round(volume,6),"\t","cm³")

        # Fator de conversao
        f = v*P/(1.60218*10**(-19)*Q*keff.nominal_value)

        fluxo = []
        fluxo_std = []
        for i in range(0,150):
            flux=f*flux_mean[i][0][0]/volume[i]
            fluxo_cientifico = format(flux, '.4e')
            fluxo.append(fluxo_cientifico)
            incerteza=f*flux_std_dev[i][0][0]/volume[i]
            inc_cientifico = format(incerteza, '.4e')
            fluxo_std.append(inc_cientifico)
            #print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo_cientifico, "+/-", inc_cientifico, "[neutron/cm².s]")
        
        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################

        # Propagação de erros no fator de conversao
        uncertainty = []
        for i in range(0,150):
            error_flux_i = flux_std_dev[i][0][0]                                                                             # Erro associado a flux_std_dev[i]
            term_flux_1 = error_flux_i * f / volume[i]                                                                       # Derivada parcial em relação a flux_mean[i]
            term_flux_2 = flux_mean[i][0][0] * (-v*P/(1.60218*10**(-19)*Q*(keff.nominal_value)**2)) * keff_error / volume[i] # Derivada parcial em relação a keff
            error_fluxo_i = np.sqrt(term_flux_1**2 + term_flux_2**2)                                                         # Erro total
            erro_final_i = format(error_fluxo_i, '.4e')
            uncertainty.append(erro_final_i)       

        for i in range(0,150):
            print("  Intervalo ", i,": ","\t"," Fluxo : ", fluxo[i], "+/-", uncertainty[i], "[neutron/cm².s]")
        
    def trabalhandoDadosPotenciaElemento(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############        Potencia        ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Retirando o keff
        print('')
        keff = sp.keff
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff)
        print('')

        # Acesse os resultados do fuel_element_tally
        heat    = sp.get_tally(scores=['heating-local'])
        fission = sp.get_tally(scores=['fission'])
        fiss_all = sp.get_tally(scores=['fission'], name='Taxa de fissao media do sistema')

        # Get the mean value for each instance of the fuel cell as a flattened (1D) numpy array
        taxa_fissao           = fission.mean.ravel()         # [Fissions/source]
        heating               = heat.mean.ravel()            # [eV/source]
        taxa_fissao_total     = fiss_all.mean.ravel()
        taxa_fissao_dev       = fission.std_dev.ravel()        
        heating_dev           = heat.std_dev.ravel()            
        taxa_fissao_total_dev = fiss_all.std_dev.ravel()

        avogadro = 1.602176565e-19
        heating_rate = heating * avogadro   # [Joules/source] 

        # Power 
        P = 8.0E+06                                # [Joules/sec] ou [W] 8 MW dividido por 1729 células combustível
        N = 19                                     # Número de celulas

        # Normalization
        source_per_sec = P / heating_rate          # [Source/sec]

        fission_rate_sec = []
        for i in range (0, 19):
            rate = taxa_fissao[i] * source_per_sec         # [Fissions/sec]
            fission_rate_sec.append(rate)

        Q = 1.99942676e+08   # Varia conforme o combustível UN = 1.99942676e+08 / U3Si2 = 1.99966971e+08

        print("Potência em cada célula:")
        potencia = []
        for i in range (0, 19):
            pot = fission_rate_sec[i] * Q * avogadro  # [W] Taxa de energia liberada em cada célula // O Q varia e deve ser calculado
            potencia.append(pot)
            print("\t", "Célula ", i, ":", pot)
        
        soma_pot = np.sum(potencia).tolist()
        print("Potência total:")
        print(soma_pot, "[J/s]")
        print("")

        ###############################################################
        ####################### Relative power ########################
        ###############################################################
        pot_rel = []
        for i in range (0, 19):
            rel_element = (potencia[i] / soma_pot) * N          # Equação para obter a potência relativa
            pot_rel.append(rel_element) 
        
        ##### Correção de média das energias liberadas por fissão #####

        mev_per_reaction = heating / taxa_fissao_total  # O valor do Q usado anteriormente. Tem que alterar manualmente.
        print("")
        print("Média da energia liberada por fissão:")
        print(mev_per_reaction, "[eV/fission]")
        print("")

        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################
        heating_rate_dev   = heating_dev * avogadro                 # Erro heating_rate
        limite_sup_source_dev = P / (heating_rate + heating_rate_dev)
        limite_inf_source_dev = P / (heating_rate - heating_rate_dev)
        diferença = limite_inf_source_dev - limite_sup_source_dev
        erro_source_sec = diferença/2                                   # Erro source_per_sec
        # Propagação de erros em fission_rate_sec
        fission_rate_sec_dev = []
        for i in range(0,19):
            error_taxa_fissao_i = taxa_fissao_dev[i]                                          # Erro associado a taxa_fissao[i]
            term_taxa_fissao_1 = error_taxa_fissao_i * source_per_sec                         # Derivada parcial em relação a taxa_fissao[i]
            term_taxa_fissao_2 = taxa_fissao[i] * erro_source_sec                             # Derivada parcial em relação a source_per_sec
            error_fission_rate_sec_i = np.sqrt(term_taxa_fissao_1**2 + term_taxa_fissao_2**2) # Erro total
            fission_rate_sec_dev.append(error_fission_rate_sec_i)
        potencia_dev = []
        for i in range(0,19):
            pot_error = fission_rate_sec_dev[i] * Q * avogadro
            potencia_dev.append(pot_error)
        # Calculando o erro associado a soma_pot usando a propagação de erros
        soma_pot_dev = np.sqrt(np.sum(np.array(potencia_dev)**2))
        # Calculando o erro total usando a propagação de erros
        pot_rel_dev = []
        for i in range(0,19):
            error_potencia_i = potencia_dev[i]                                  # Erro associado a potencia[i]
            term_pot_rel_1 = N / soma_pot * error_potencia_i                    # Derivada parcial em relação a potencia[i]
            term_pot_rel_2 = ((-potencia[i] * N)/ (soma_pot**2)) * soma_pot_dev # Derivada parcial em relação a soma_pot
            error_rel_element = np.sqrt(term_pot_rel_1**2 + term_pot_rel_2**2)  # Erro total
            pot_rel_dev.append(error_rel_element)

        # Imprimindo os valores da potência relativa e seus erros
        print("Potência relativa:")
        print("")
        for i in range(0,19):
            rel_element = (potencia[i] / soma_pot) * N  
            rel_element_error = pot_rel_dev[i]        
            # Convertendo arrays NumPy para escalares
            rel_element_scalar = rel_element.item()
            rel_element_error_scalar = rel_element_error.item() 
            print("\tCélula {}: {:.6f} ± {:.6f}".format(i, rel_element_scalar, rel_element_error_scalar))

    def trabalhandoDadosPotenciaPin(self):
        print("################################################")
        print("############   Trabalhando Dados    ############")
        print("############        Potencia        ############")
        print("################################################")

        sp = openmc.StatePoint('statepoint.'+str(self.ciclos)+'.h5')

        # Retirando o keff
        print('')
        keff = sp.keff
        print("\t" , " keff (valor combinado de abs/col/t.length) :",keff)
        print('')

        # Acesse os resultados do fuel_element_tally
        heat    = sp.get_tally(scores=['heating-local'])
        fission = sp.get_tally(scores=['fission'], name='Taxa de reacao de fissao')
        fiss_all = sp.get_tally(scores=['fission'], name='Taxa de fissao media do sistema')

        # Get the mean value for each instance of the fuel cell as a flattened (1D) numpy array
        taxa_fissao       = fission.mean.ravel()         # [Fissions/source]
        heating           = heat.mean.ravel()            # [eV/source]
        taxa_fissao_total = fiss_all.mean.ravel()  
        taxa_fissao_dev   = fission.std_dev.ravel()        
        heating_dev       = heat.std_dev.ravel()

        avogadro = 1.602176565e-19
        heating_rate = heating * avogadro   # [Joules/source] 

        # Power for each fuel cell
        P = 8.0E+06                                # [Joules/sec] ou [W] 8 MW dividido por 1729 células combustível
        N = 1729

        # Normalization
        source_per_sec = P / heating_rate          # [Source/sec]

        fission_rate_sec = []
        for i in range (0, 1729):
            rate = taxa_fissao[i] * source_per_sec          # [Fissions/sec]
            fission_rate_sec.append(rate)

        Q = 2.0009483e+08   # Varia conforme o combustível / UN = 1.99942676e+08 / U3Si2 = 1.99966971e+08

        potencia = []
        for i in range (0, 1729):
            pot = fission_rate_sec[i] * Q * 1.602176565e-19  # [W] Taxa de energia liberada em cada célula
            potencia.append(pot)
            #print("\t", "Célula ", i, ":", pot, "[W]")

        ###############################################################
        soma_pot = np.sum(potencia).tolist()
        print("Potência total sem correção:")
        print(soma_pot, "[eV]")
        print("")

        ###############################################################
        ####################### Relative power ########################
        ###############################################################
        self.pot_rel = []
        for i in range (0, 1729):
            rel_element = (potencia[i] / soma_pot) * N          # Equação para obter a potência relativa
            self.pot_rel.append(rel_element) 
            #print("\t", "Célula ", i, ":", rel_element)

        ##### Correção de média das energias liberadas por fissão #####

        mev_per_reaction = heating / taxa_fissao_total
        print("")
        print("Média da energia liberada por fissão:")
        print(mev_per_reaction, "[eV/fission]")
        print("")

        ###############################################################
        ###################### Calculo de erros #######################
        ###############################################################
        heating_rate_dev   = heating_dev * avogadro                    # Erro heating_rate
        limite_sup_source_dev = P / (heating_rate + heating_rate_dev)
        limite_inf_source_dev = P / (heating_rate - heating_rate_dev)
        diferença = limite_inf_source_dev - limite_sup_source_dev
        erro_source_sec = diferença/2                                  # Erro source_per_sec
        # Propagação de erros em fission_rate_sec
        fission_rate_sec_dev = []
        for i in range(0,1729):
            error_taxa_fissao_i = taxa_fissao_dev[i]                                          # Erro associado a taxa_fissao[i]
            term_taxa_fissao_1 = error_taxa_fissao_i * source_per_sec                         # Derivada parcial em relação a taxa_fissao[i]
            term_taxa_fissao_2 = taxa_fissao[i] * erro_source_sec                             # Derivada parcial em relação a source_per_sec
            error_fission_rate_sec_i = np.sqrt(term_taxa_fissao_1**2 + term_taxa_fissao_2**2) # Erro total
            fission_rate_sec_dev.append(error_fission_rate_sec_i)
        potencia_dev = []
        for i in range(0,1729):
            pot_error = fission_rate_sec_dev[i] * Q * avogadro
            potencia_dev.append(pot_error)
        # Calculando o erro associado a soma_pot usando a propagação de erros
        soma_pot_dev = np.sqrt(np.sum(np.array(potencia_dev)**2))
        # Calculando o erro total usando a propagação de erros
        pot_rel_dev = []
        for i in range(0,1729):
            error_potencia_i = potencia_dev[i]                                  # Erro associado a potencia[i]
            term_pot_rel_1 = N / soma_pot * error_potencia_i                    # Derivada parcial em relação a potencia[i]
            term_pot_rel_2 = ((-potencia[i] * N)/ (soma_pot**2)) * soma_pot_dev # Derivada parcial em relação a soma_pot
            error_rel_element = np.sqrt(term_pot_rel_1**2 + term_pot_rel_2**2)  # Erro total
            pot_rel_dev.append(error_rel_element)

        ## Imprimindo os valores da potência relativa e seus erros
        #print("Potência relativa:")
        #print("")
        #for i in range(0,1729):
        #    rel_element = (potencia[i] / soma_pot) * N  
        #    rel_element_error = pot_rel_dev[i]        
        #    # Convertendo arrays NumPy para escalares
        #    rel_element_scalar = rel_element.item()
        #    rel_element_error_scalar = rel_element_error.item() 
        #    print("\tCélula {}: {:.6f} ± {:.6f}".format(i, rel_element_scalar, rel_element_error_scalar))

        # Salvando em excel com o Pandas dataframe
        df = pd.DataFrame([self.pot_rel,pot_rel_dev]).transpose()
        df = df.map(lambda x: str(x).strip("[]"))
        df.to_csv('pot_pin.csv', index=False)

    def plotPotenciaPin(self):
        print("################################################")
        print("############          Plot          ############")
        print("############        Potencia        ############")
        print("################################################")

        from matplotlib import pyplot as plt
        import openmc.lib
    
        plt.style.use('seaborn-v0_8-paper')
    
        resolution = (10000, 10000)
        img = np.full(resolution, np.nan)
        xmin, xmax = -38., 38.
        ymin, ymax = -42., 42.
    
        
        with openmc.lib.run_in_memory():
            for row, y in enumerate(np.linspace(ymin, ymax, resolution[0])):
                print(row)
                for col, x in enumerate(np.linspace(xmin, xmax, resolution[1])):
                    try:
                        # Para cada ponto (x, y, z), determine a célula e o index associado a ela 
                        cell, distribcell_index = openmc.lib.find_cell((x, y, 0.))
                    except openmc.exceptions.GeometryError:
                        # Se um ponto aparece fora da geometria, ele entrará em exceção.
                        # Essas linhas pegam a exceção e as ignoram continuando a rodar o programa
                        continue
                    #print(str(x) + "\t" + str(y) + "\t" + str(cell.id) + "\t" + str(self.fuel.id))
                    if cell.id == self.fuel.id :
                        # Quando o ID bater, é colocado o pixel correspondente na imagem com as informações do
                        # distribcell index. Note que estamos tirando vantagem do fato que o i-ésimo elemento
                        # do "score" array corresponde a i-ésima instância do distribcell.
                        img[row, col] = self.pot_rel[distribcell_index]
        
        options = {
        'origin': 'lower',
        'extent': (xmin, xmax, ymin, ymax),
        'vmin': 0.78,
        'vmax': 1.41,
        'cmap': 'RdYlBu_r',
        }
        ## Há duas maneiras de plotar o gráfico: por plt normal ou por subplots. Por subplots a vantagem é que pode ser acoplado
        ## vários gráficos juntamente como uma grade e pode ser personalizado melhor. Nesse caso eu quero colocar o fundo do grafico
        ## de uma cor escura. 

        # Definindo uma imagem mapeável
        #plt.imshow(img, **options)

        # Fontes e título
        #plt.title('Power element distribution over the core - OpenMC', fontsize=16)
        #plt.xlabel('x [cm]', fontsize=14)
        #plt.ylabel('y [cm]', fontsize=14)
        #colorbar = plt.colorbar(label='Relative power')
        #colorbar.ax.yaxis.label.set_size(14)

        # Saída
        #plt.savefig("pot", format="eps")
        #plt.tight_layout()
        #plt.show()

        # Definindo uma imagem mapeável
        fig, ax = plt.subplots()
        #grafico = fig.add_subplot()
        ax.set_facecolor('k')          # Cor de fundo para o grafico
        c       = ax.imshow(img, **options)

        # Fontes e título
        fig.colorbar = plt.colorbar(c,label='Relative power')
        fig.colorbar.ax.yaxis.label.set_size(20)
        fig.colorbar.ax.yaxis.set_tick_params(labelsize=16)
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)
        plt.title('Power element distribution over the core', fontsize=24)
        plt.xlabel('x [cm]', fontsize=20)
        plt.ylabel('y [cm]', fontsize=20)

        # Saída
        #plt.savefig("pot", format="eps")
        plt.tight_layout()
        plt.show()