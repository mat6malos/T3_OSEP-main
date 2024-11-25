from OPTIo import OptimizarGeneradores
from Graf import GraficarHoras
from P_viento import GeneradorPotencia
from Matrizes import MatrizSimbolica
import cvxpy as cp
import gurobipy as gp
from A import OptimizarFinal
from gurobipy import GRB


# Datos Generadores
Pmin            = [150, 20, 25, 20, 10]  # MW
Pmax            = [455, 130, 162, 130, 55]  # MW
a               = [1000, 700, 450, 680, 670]  # $
b               = [16.19, 16.6, 19.7, 16.5, 27.8]  # $/MW
c               = [0.00048, 0.002, 0.00398, 0.00211, 0.00173]  # $/MW^2
t               = [8, 5, 6, 5, 1]  # h
Cs              = [9000, 1100, 1800, 1120, 60]  # $
Ramp            = [136.5, 130, 162, 130, 55]  # MW/h
Demand          = [390, 420, 480, 530, 560, 620, 640, 670, 730, 780, 810, 840, 780, 730, 670, 590, 560, 620, 670, 780, 730, 620, 500, 450]  # MW
Vv              = [7.5, 4.5, 5, 4.5, 2.5, 3.5, 3.5, 5, 3, 5.5, 7, 9, 9, 11.5, 13, 13.5, 13.5, 13, 11.5, 10, 9.5, 8.5, 9, 10.5]  # m/s
Vp              = [[0, 0], [0.5, 0], [1, 0], [1.5, 0], [2, 0], [2.5, 0], [3, 29], [3.5, 81], [4, 146], [4.5, 226], [5, 327], [5.5, 452], [6, 600], [6.5, 775], [7, 981], [7.5, 1216], [8, 1487], [8.5, 1780], [9, 2103], [9.5, 2437], [10, 2753], [10.5, 2999], [11, 3159], [11.5, 3241], [12, 3276], [12.5, 3290], [13, 3297], [13.5, 3300]] # m/s, kW
num_horas       = 24
num_gen         = 5

# Crear un objeto de la clase GeneradorPotencia
generador = GeneradorPotencia(Vv, Vp)
PVmax           = generador.Gvmax

# Caso inicial
# Solución de la minimización
C_o             = OptimizarGeneradores(Demand, Pmin, Pmax, a, b, c, num_horas)
V_o, f_o        = C_o.optimizaro()

# Crear un solo modelo
modelo          = gp.Model("Matriz_Modelo")

# Crear matrices usando el mismo modelo
P               = MatrizSimbolica(num_gen, num_horas, "P", model=modelo)
S               = MatrizSimbolica(num_gen, num_horas, "s", model=modelo)
U               = MatrizSimbolica(num_gen, num_horas, "u", model=modelo)
PV              = MatrizSimbolica(1, num_horas, "Pv", model=modelo)
matriz_S = S.matriz
matriz_P = P.matriz

# Definir función objetivo
F              = OptimizarFinal(matriz_P, matriz_S, Cs, a, b, c)

modelo.setObjective(F.FO, GRB.MINIMIZE)

# Definir restricciones
    ## Restricción de igualdad
for hora in range(num_horas):
    Psum    = 0
    for gen in range(len(P.matriz)):
        Psum    = Psum + P.matriz[gen][hora]
    Psum        = Psum + PV.matriz[0][hora]
    modelo.addConstr(Psum == Demand[hora], "constrig_" + str(hora + 1)) 
    ## Restricción maximos
for hora in range(num_horas):
    for gen in range(len(P.matriz)):
        modelo.addConstr(P.matriz[gen][hora] <= U.matriz[gen][hora] * Pmax[gen], "constrmax_" + str(gen + 1)+ "_"+ str(hora + 1)) 
    modelo.addConstr(PV.matriz[0][hora] <= PVmax[hora], "constrmax_v_"+ str(hora + 1)) 
    ## Restricción minimos
for hora in range(num_horas):
    for gen in range(len(P.matriz)):
        modelo.addConstr(P.matriz[gen][hora] >= U.matriz[gen][hora] * Pmin[gen], "constrmin_" + str(gen + 1)+ "_"+ str(hora + 1))
    


modelo.optimize()

if modelo.status == GRB.OPTIMAL:
    # Imprimir el valor de la función objetivo
    print(f"Valor de la función objetivo (FO): {modelo.objVal}")

    # Imprimir los valores de cada variable
    for hora in range(num_horas):
        for gen in range(num_gen):
            # Acceder a cada variable P
            print(f"Valor de P_{gen+1}_{hora+1}: {P.matriz[gen][hora].x}")
        print(f"Valor de PV_{0}_{hora+1}: {PV.matriz[0][hora].x}")
else:
    print("No se encontró una solución óptima.")

for gen in range(num_gen):
    GraficarHoras(P.matriz[gen].x)

# Graficos
#? GraficarHoras(Demand)
#? GraficarHoras(Vv)
#? GraficarHoras(Gvmax)