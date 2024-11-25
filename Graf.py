import matplotlib.pyplot as plt

class GraficarHoras:
    def __init__(self, Vv):
        """
        Inicializa el objeto con los valores de Vv.
        Al instanciarlo, ejecuta el gráfico de las horas.
        """
        self.Vv = Vv
        self.graficar_horas()  # Llamada al método de graficado al instanciar el objeto
        
    def graficar_horas(self):
        """
        Método que genera el gráfico de las horas con la entrada.
        """
        horas = list(range(1, 25))  # Horas de 1 a 24
        plt.figure()
        plt.plot(horas, self.Vv, '-o', linewidth=2, markersize=6, markerfacecolor='r')
        plt.grid(True)
        plt.xticks(range(1, 25))  # Marcar todas las horas
        plt.xlim([0, 25])  # Ajustar límites del eje x
        plt.ylim([0, max(self.Vv) + 2])  # Ajustar límites del eje y
        plt.xlabel('Hora del día (h)')
        plt.show()
