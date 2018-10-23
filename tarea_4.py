from random import expovariate, uniform
from numpy import random


class Simulacion:
    def __init__(self, s, S):
        self.s = s
        self.S = S
        self.inventario = 60
        self.pendiente = 0
        self.pedido_actual = 0
        self.costo_total = 0
        self.time = 0

        # Arreglos
        self.proxima_demanda = self.llegada_demanda()
        self.llegada_orden = 0

    @staticmethod
    def lead_time():
        return uniform(0.5, 1)

    @staticmethod
    def llegada_demanda():
        return expovariate(10)

    @staticmethod
    def demanda():
        return random.choice([1, 2, 3, 4], p=[1/6, 1/3, 1/3, 1/6])

    def run(self):
        while self.time <= 120:

            # Si self.time es entero (comienzo de mes)
            if not (self.time % 1):
                if self.inventario < self.s:
                    self.pedido_actual = self.S - self.inventario
                    self.costo_total += (32 + 3*self.pedido_actual)
                    self.llegada_orden = self.time + self.lead_time()
            # Veo los tiempos

            if self.llegada_orden > self.proxima_demanda:
                # Sumo el inventario hasta ahora por el costo asociado al tiempo
                self.costo_total += self.inventario * (self.llegada_orden -
                                                       self.time)
                """ Quizas aquí queda negativo de nuevo """
                self.inventario += (self.pedido_actual - self.pendiente)
                self.pendiente = 0
                self.time = self.llegada_orden
            else:
                demanda = self.demanda()
                # Sumo el inventario hasta ahora por el costo asociado al tiempo
                self.costo_total += self.inventario * (self.proxima_demanda -
                                                       self.time)
                if self.inventario - demanda < 0:
                    self.inventario = 0
                    self.pendiente += abs(self.inventario - demanda)
                else:
                    self.inventario -= demanda
                self.time = self.proxima_demanda
                self.proxima_demanda = self.time + self.llegada_demanda()

    def __repr__(self):
        return f"Tiempo final: {self.time}\n" \
               f"Costo total: {self.costo_total}\n" \
               f"Costo promedio: {self.costo_total/120}\n" \



simulacion1 = Simulacion(20, 40)
simulacion1.run()
print(simulacion1)




