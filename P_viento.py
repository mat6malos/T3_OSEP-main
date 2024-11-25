import numpy as np

class GeneradorPotencia:
    def __init__(self, Vv, Vp, num_horas=24):
        """
        Inicializa el objeto con los valores de Vv, Vp y num_horas.
        Al instanciarlo, ejecuta el cálculo de potencia.
        """
        self.Vv = Vv
        self.Vp = Vp
        self.num_horas = num_horas
        
        # Ejecutar el cálculo al crear el objeto
        self.Gvmax, self.Gvmin = self.generar_potencia()

    def generar_potencia(self):
        """
        Calcula la potencia generada a partir de las velocidades del viento (Vv) 
        y las relaciones de potencia (Vp). 
        Devuelve Gvmax (potencia máxima) y Gvmin (potencia mínima).
        """
        Vgen = []

        # Recorrer todos los valores de Vv
        for viento in self.Vv:
            potencia_generada = None  # Inicializar variable para la potencia generada

            # Buscar en el arreglo Vp el valor correspondiente de potencia
            for relacion in self.Vp:
                if viento == relacion[0]:  # Si Vv coincide con la velocidad del viento en Vp
                    potencia_generada = relacion[1]
                    break
                elif viento >= 13.5 and viento <= 25:  # Si Vv está en el rango de 13.5 a 25 m/s
                    potencia_generada = 3300
                    break

            # Añadir la potencia generada a la lista Vgen
            Vgen.append(potencia_generada)

        # Convertir Vgen a un array de NumPy y calcular Gvmax
        Vgen = np.array(Vgen)
        Gvmax = (Vgen * 200 / 1000) # Convertir de kW a MW

        # Transponer Gvmax para asegurar que tenga la forma correcta
        Gvmax = Gvmax.T.tolist()

        # Inicializar Gvmin como un arreglo de ceros
        Gvmin = np.zeros(self.num_horas).tolist()

        return Gvmax, Gvmin
