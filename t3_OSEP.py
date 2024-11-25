from OPTIo import OptimizarGeneradores
from Graf import GraficarHoras
from P_viento import GeneradorPotencia
from Matrizes import MatrizSimbolica
import cvxpy as cp
import gurobipy as gp
from A import OptimizarFinal


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
matriz_S = S.matriz
matriz_P = P.matriz

F              = OptimizarFinal(matriz_P, matriz_S, Cs, a, b, c)
print(F.FO)

# Ahora ambas matrices compartirán el mismo modelo de optimización






## Crear un objeto de la clase GeneradorPotencia
#generador = GeneradorPotencia(Vv, Vp)
#
#FO         = C_o.FO(Cs)
#constraints = C_o.constraints()
#
#prob = cp.Problem(cp.Minimize(FO), constraints)
#
## Resolver el problema
#prob.solve(solver=cp.CBC)


# Graficos
#? GraficarHoras(Demand)
#? GraficarHoras(Vv)
#? GraficarHoras(Gvmax)