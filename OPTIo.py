import numpy as np
import cvxpy as cp
from scipy.optimize import minimize
from Matrizes import MatrizSimbolica

class OptimizarGeneradores:
    """
    Clase para resolver el problema de optimización de la generación de potencia
    en función de los generadores disponibles, teniendo en cuenta las demandas
    horarias y los costos de generación.

    Atributos:
        Demand (list): Lista de demandas horarias en MW.
        Pmin (numpy.array): Potencia mínima de cada generador en MW.
        Pmax (numpy.array): Potencia máxima de cada generador en MW.
        a (numpy.array): Coeficientes del costo lineal en la función de costo de generación.
        b (numpy.array): Coeficientes del costo lineal por MW generado en la función de costo.
        c (numpy.array): Coeficientes del costo cuadrático en la función de costo de generación.
        P0 (numpy.array): Potencias iniciales en MW para los generadores (valor inicial de optimización).
        demanda_0 (float): Demanda inicial a satisfacer.
    
    Métodos:
        objetivo(P): Calcula la función objetivo, que es el costo total de generación de potencia,
                     dado un vector de potencias generadas por cada generador.
        
        optimizar(): Resuelve el problema de optimización utilizando el método `minimize` de
                     `scipy.optimize` para encontrar las potencias óptimas que minimizan el costo
                     y satisfacen la demanda.
    """
    def __init__(self, Demand, Pmin, Pmax, a, b, c, num_horas):
        # Inicialización de los parámetros
        self.Demand = Demand
        self.Pmin = np.array(Pmin)  # Convertir a array de numpy
        self.Pmax = np.array(Pmax)  # Convertir a array de numpy
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)
        self.num_horas = num_horas
        # Condiciones iniciales
        self.P0 = np.array([0, 0, 0, 0, 0])  # Potencias iniciales en MW
        self.demanda_0 = self.Demand[0]  # Demanda inicial
        
        # Variables de optimización
        self.P = cp.Variable((len(self.a), self.num_horas), nonneg=True)  # Matriz de potencias
        self.S = cp.Variable((len(self.a), self.num_horas), boolean=True)  # Matriz de partida
        self.U = cp.Variable((len(self.a), self.num_horas), boolean=True)  # Matriz de partida
        
        
    def objetivoo(self, P):
        """
        Función objetivo que calcula el costo total de generación de potencia.
        """
        return np.sum(self.a + self.b * P + self.c * (P ** 2))
    
    def optimizaro(self):
        """
        Resuelve el problema de optimización de las potencias utilizando minimizar.
        """
        # Restricciones de igualdad
        Aeq = np.ones(5)  # Coeficientes de la ecuación de igualdad
        beq = self.demanda_0  # Demanda inicial
        # Restricciones de límites (Pmin y Pmax)
        lb = self.Pmin
        ub = self.Pmax
        # Resolver el problema de optimización
        res = minimize(self.objetivoo, self.P0, constraints={'type': 'eq', 'fun': lambda P: np.dot(Aeq, P) - beq},
                       bounds=list(zip(lb, ub)), method='SLSQP')
        # Resultados
        P_optimal = res.x
        fval_optimal = res.fun

        return P_optimal, fval_optimal
    def FO(self, Cs):
        """
        Calcula la función objetivo con el costo de cada generador considerando las variables de potencia P y S.
        """
        Cs = np.array(Cs)
        # Tiling de las matrices c, b, a para que tengan el tamaño adecuado
        c_tiled = np.tile(self.c[:, np.newaxis], (1, self.num_horas))  # c será una matriz 5x24
        b_tiled = np.tile(self.b[:, np.newaxis], (1, self.num_horas))  # b será una matriz 5x24
        a_tiled = np.tile(self.a[:, np.newaxis], (1, self.num_horas))  # a será una matriz 5x24 
        Cs_tiled = np.tile(Cs[:, np.newaxis], (1, self.num_horas))  # a será una matriz 5x24 

       # Cálculo de Fc (multiplicación elemento a elemento)
        Fc = cp.multiply(c_tiled, cp.square(self.P)) + cp.multiply(b_tiled, self.P) + a_tiled
    
        # Función objetivo FO (se suma sobre todos los generadores y horas)
        FO = cp.sum(Fc + cp.multiply(Cs_tiled, self.S))  # Suma sobre todos los generadores y horas
    
        return FO
    def constraints(self):
        Pmin_tiled = np.tile(self.Pmin[:, np.newaxis], (1, self.num_horas))  # c será una matriz 5x24
        Pmax_tiled = np.tile(self.Pmax[:, np.newaxis], (1, self.num_horas))  # b será una matriz 5x24
        A_min = cp.multiply(self.U, Pmin_tiled)
        A_max = cp.multiply(self.U, Pmax_tiled)
        # Vamos a crear una lista de restricciones
        constraints = []
        # Supongamos que queremos que cada elemento de la matriz resultante sea menor que 100
        for i in range(self.U.shape[0]):  # Recorrer las filas
            for j in range(self.U.shape[1]):  # Recorrer las columnas
                constraints.append(A_min[i, j] <= self.P[i, j])  # Restricción sobre cada elemento
        for i in range(self.U.shape[0]):  # Recorrer las filas
            for j in range(self.U.shape[1]):  # Recorrer las columnas
                constraints.append(self.P[i, j] <= A_max[i, j])  # Restricción sobre cada elemento
        
        return constraints