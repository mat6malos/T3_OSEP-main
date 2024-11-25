import gurobipy as gp

class MatrizSimbolica:
    def __init__(self, num_generadores, num_horas, letra, model=None):
        """
        Inicializa la clase para crear una matriz de variables de decisión de Gurobi.
        
        :param num_generadores: Número de generadores (filas).
        :param num_horas: Número de horas (columnas).
        :param letra: Letra base para las variables.
        :param model: Modelo de Gurobi. Si se pasa `None`, se crea un nuevo modelo.
        """
        self.num_generadores = num_generadores
        self.num_horas = num_horas
        self.letra = letra
        self.model = model if model else gp.Model("Matriz_Modelo")  # Usa el modelo pasado o crea uno nuevo
        self.matriz = self.crear_matriz()  # Genera la matriz de variables de decisión

    def crear_matriz(self):
        """
        Crea la matriz de variables de decisión de Gurobi de tamaño (num_generadores x num_horas).
        
        :return: Matriz de variables de decisión de Gurobi.
        """
        matriz = []
        for i in range(1, self.num_generadores + 1):  # Itera sobre los generadores
            fila = []
            for t in range(1, self.num_horas + 1):  # Itera sobre las horas
                # Crea una variable de decisión de Gurobi
                var = self.model.addVar(vtype=gp.GRB.CONTINUOUS, name=f"{self.letra}_{i}_{t}")
                fila.append(var)
            matriz.append(fila)
        self.model.update()  # Actualiza el modelo con las nuevas variables
        return matriz




