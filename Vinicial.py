import numpy as np
from scipy.optimize import minimize

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
    def __init__(self, Demand, Pmin, Pmax, a, b, c):
        # Inicialización de los parámetros
        self.Demand = Demand
        self.Pmin = np.array(Pmin)  # Convertir a array de numpy
        self.Pmax = np.array(Pmax)  # Convertir a array de numpy
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)
        
        # Condiciones iniciales
        self.P0 = np.array([0, 0, 0, 0, 0])  # Potencias iniciales en MW
        self.demanda_0 = self.Demand[0]  # Demanda inicial
        
    def objetivo(self, P):
        """
        Función objetivo que calcula el costo total de generación de potencia.
        """
        return np.sum(self.a + self.b * P + self.c * (P ** 2))
    
    def optimizar(self):
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
        res = minimize(self.objetivo, self.P0, constraints={'type': 'eq', 'fun': lambda P: np.dot(Aeq, P) - beq},
                       bounds=list(zip(lb, ub)), method='SLSQP')
        # Resultados
        P_optimal = res.x
        fval_optimal = res.fun

        return P_optimal, fval_optimal