
#######################################################################
####                                                               ####
####              UNIVERSIDADE FEDERAL DE MINAS GERAIS             ####
####               Departamento de Engenharia Nuclear              ####
####                Jefferson Quintão Campos Duarte                ####
####                  Thalles Oliveira Campagnani                  ####
####                                                               ####
#######################################################################

import libOpenSealer
import time

libOpenSealer.dir("casos")

### UN
## keff
#libOpenSealer.dir("UN_keff",False,False)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.run()
#
### Beff (Neutrons atrasados = Falso)
#libOpenSealer.dir("UN_Beff",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, False)
#sealer.run()
#
## Barras inseridas
#libOpenSealer.dir("UN_shutdown",False,True)
#sealer = libOpenSealer.SealerArctic('UN', -66.300, -66.300, 15000, 400, 40, True)
#sealer.run()

###################################################################################################
### U3Si2
###keff
#libOpenSealer.dir("U3Si2_keff",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2',  55.3001, 55.3002, 15000, 400, 40, True)
#sealer.run()
#
### Beff (Neutrons atrasados = Falso)
#libOpenSealer.dir("U3Si2_Beff",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2',  55.3001, 55.3002, 15000, 400, 40, False)
#sealer.run()
#
## Barras inseridas
#libOpenSealer.dir("U3Si2_shutdown",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2', -66.300, -66.300, 15000, 400, 40, True)
#sealer.run()

##########################################################################
#######                        TALLIES UN                         ########
##########################################################################

#libOpenSealer.dir("UN_Inverse_velocity",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesInverseVelocity()
#sealer.run()
#sealer.trabalhandoDadosInverseVelocity()
#
#libOpenSealer.dir("UN_Espectro_Fuel",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesEspectroFuel()
#sealer.run()
#sealer.trabalhandoDadosEspectroFuel()

libOpenSealer.dir("UN_MeshAxial",False,True)
sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
sealer.talliesMeshAxial()
sealer.run()
sealer.trabalhandoDadosMeshAxial()
#
#libOpenSealer.dir("UN_MeshRadial",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesMeshRadial()
#sealer.run()
#sealer.trabalhandoDadosMeshRadial()

#libOpenSealer.dir("UN_Pot_Elemento",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesPotenciaElemento()
#sealer.run()
#sealer.trabalhandoDadosPotenciaElemento()

#libOpenSealer.dir("UN_Pot_Pin",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesPotenciaPin()
#sealer.run()
#sealer.trabalhandoDadosPotenciaPin()
#sealer.plotPotenciaPin()

##########################################################################
#######                      TALLIES U3Si2                        ########
##########################################################################

#libOpenSealer.dir("U3Si2_Inverse_velocity",False,True)
#sealer = libOpenSealer.SealerArctic('UN', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesInverseVelocity()
#sealer.run()
#sealer.trabalhandoDadosInverseVelocity()
#
#libOpenSealer.dir("U3Si2_Espectro_Fuel",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesEspectroFuel()
#sealer.run()
#sealer.trabalhandoDadosEspectroFuel()
#
libOpenSealer.dir("U3Si2_MeshAxial",False,True)
sealer = libOpenSealer.SealerArctic('U3Si2', 55.3001, 55.3002, 15000, 400, 40, True)
sealer.talliesMeshAxial()
sealer.run()
sealer.trabalhandoDadosMeshAxial()
#
#libOpenSealer.dir("U3Si2_MeshRadial",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesMeshRadial()
#sealer.run()
#sealer.trabalhandoDadosMeshRadial()

#libOpenSealer.dir("U3Si2_Pot_Elemento",False,False)
#sealer = libOpenSealer.SealerArctic('U3Si2', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesPotenciaElemento()
#sealer.run()
#sealer.trabalhandoDadosPotenciaElemento()

#libOpenSealer.dir("U3Si2_Pot_Pin",False,True)
#sealer = libOpenSealer.SealerArctic('U3Si2', 55.3001, 55.3002, 15000, 400, 40, True)
#sealer.talliesPotenciaPin()
#sealer.run()
#sealer.trabalhandoDadosPotenciaPin()
#sealer.plotPotenciaPin()


###########################################################################
########                          QUEIMA                           ########
###########################################################################

# Registrando o tempo de inicialização
start_time = time.time()

libOpenSealer.dir("Nu_UO2_final",voltar=False)
sealer = libOpenSealer.SealerArctic(config='UO2', particulas=10000, ciclos=250, inativo=50, atrasados=True)
sealer.geometria()
sealer.talliesNU()
sealer.queima(timestep_units='d',timesteps=[15]*1, power=8.0E+06, 
              chain_file='/home/jefferson/git/SealerArctic/OpenMC/chains/chain_casl_sfr.xml', diff=False)
sealer.trabalhandoDadosNU()

# Registrando o tempo de finalização
end_time = time.time()

# Exibindo o tempo de execução em horas
execution_time_hours = (end_time - start_time) / 3600
print("Tempo de execução: ", execution_time_hours, "horas")
# Exibindo o tempo de execução em dias
execution_time_days = (end_time - start_time) / 86400
print("Tempo de execução: ", execution_time_days, "dias")
