from random import expovariate, uniform
from numpy import random
from math import sqrt


class Simulacion:
    def __init__(self, s, S):
        self.s = s
        self.S = S
        self.inventario = 60
        self.pendiente = 0
        self.pedido_actual = 0
        self.costo_total = 0
        self.time = 0
        self.mes = 0

        # Arreglos
        self.proxima_demanda = self.llegada_demanda()
        self.llegada_orden = 500

    @staticmethod
    def lead_time():
        return uniform(0.5, 1)

    @staticmethod
    def llegada_demanda():
        return expovariate(10)

    @staticmethod
    def demanda():
        return random.choice([1, 2, 3, 4], p=[1 / 6, 1 / 3, 1 / 3, 1 / 6])

    def run(self):
        while self.time <= 120:
            # print(self.time, self.proxima_demanda, self.llegada_orden)
            # Si self.time es entero (comienzo de mes)
            if self.time // 1 >= self.mes:
                self.mes += 1
                if self.inventario < self.s:
                    self.pedido_actual = self.S - self.inventario
                    self.costo_total += (32 + 3 * self.pedido_actual)
                    self.llegada_orden = self.time + self.lead_time()
            # Veo los tiempos

            if self.llegada_orden < self.proxima_demanda:
                # Sumo el inventario hasta ahora por el costo asociado al tiempo
                self.costo_total += (self.inventario + self.pendiente * 5) \
                                    * (self.llegada_orden - self.time)

                """ Veo si con el pedido quedo en positivo, o sigo debiendo"""
                if self.inventario + self.pedido_actual - self.pendiente < 0:
                    self.inventario = 0
                    self.pendiente = abs(self.inventario + self.pedido_actual
                                         - self.pendiente)
                else:
                    self.inventario += (self.pedido_actual - self.pendiente)
                self.pendiente = 0
                self.time = self.llegada_orden
                self.llegada_orden = 500
            else:
                demanda = self.demanda()
                # Sumo el inventario hasta ahora por el costo asociado al tiempo
                self.costo_total += (self.inventario + self.pendiente * 5) \
                                    * (self.proxima_demanda - self.time)
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
               f"Costo promedio: {self.costo_total/120}\n"


# Primera técnica: comparación de a pares

def replica_conjunta(conjunto):
    zetas = []
    politica_base = conjunto[1]
    simulacion_base = Simulacion(*politica_base)
    simulacion_base.run()
    prom_base = simulacion_base.costo_total/120

    for politica in [conjunto[0]]+conjunto[2:]:
        simulacion_politica = Simulacion(*politica)
        simulacion_politica.run()
        prom_politica = simulacion_politica.costo_total/120

        zetas.append(prom_politica - prom_base)
    return zetas


def replicas_iniciales(conjunto, replicas):
    resultados = [replica_conjunta(conjunto) for _ in range(replicas)]
    por_politica = list(zip(*resultados))
    promedios = [sum(x)/len(x) for x in por_politica]
    restas = []
    for i in range(replicas):
        restas.append([((por_politica[j][i] - promedios[j])**2)/(replicas-1)
                       for j in range(6)])
    varianzas = [sum(x) for x in zip(*restas)]
    return promedios, varianzas


def intervalos(conjunto, replicas):
    promedios, varianzas = replicas_iniciales(conjunto, replicas)
    for prom, s2 in zip(promedios, varianzas):
        print([prom - 2.97 * sqrt(s2/replicas), prom + 2.97 * sqrt(s2/replicas)])


politicas = [(20, 40), (20, 50), (20, 60), (20, 70),
             (20, 80), (25, 60), (25, 70)]

intervalos(politicas, 100)