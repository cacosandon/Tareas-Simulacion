from random import uniform, seed, randint
from collections import deque
from time import clock
from math import log


class Supermercado:
    def __init__(self, cajas):
        self.cajas = cajas
        self.hora_inicio = 0
        self.hora_cierre = 840
        self.hora_final = 3000
        self.hora_actual = 0
        self.colas = [deque() for i in range(cajas)]
        # Tiempo de llegada inicial
        m = (-1/3)*log(1 - uniform(0, 1))
        self.proxima_llegada = self.hora_actual + m
        self.clientes = []
        self.llegadas_cola = [3000]
        self.proximas_atenciones = []
        self.espera_de_clientes = []

    def cola_mas_corta(self):
        mas_corta = [self.colas[0], 0]
        i = 0
        for cola in self.colas:
            if len(cola) < len(mas_corta[0]):
                mas_corta = [cola, i]
            i += 1

        return mas_corta

    def printeo_colas(self):
        buscando_productos = sum(1 for x in self.clientes if x.hora_ingresocola_estadistica > self.hora_actual)
        cantidad_colas = " ".join([str(len(x)) for x in self.colas])
        if self.hora_actual > self.hora_cierre:
            return f'Hay {buscando_productos} persona(s) buscando sus productos.\n' \
                   f'Colas: {cantidad_colas}\n' \
                   f'Ya cerró la entrada.'
        return f'Hay {buscando_productos} persona(s) buscando sus productos.\n' \
               f'Colas: {cantidad_colas}\n'

    def simular(self):
        tiempo1 = clock()
        self.proximas_atenciones = [3000]*self.cajas
        
        while self.hora_actual < self.hora_final:
            
            self.llegadas_cola = [cliente.hora_ingresocola for
                                  cliente in self.clientes]+[3000]

            self.hora_actual = min(self.proxima_llegada,
                                   min(self.proximas_atenciones),
                                   min(self.llegadas_cola))
            # Despues de trasladarnos al tiempo, vamos al primero que pase.

            if self.hora_actual == self.proxima_llegada:

                self.clientes.append(Cliente(self.hora_actual))

                # print(f"Ha llegado un cliente a las {self.hora_actual}")

                if self.hora_actual > self.hora_cierre:
                    self.proxima_llegada = 3000

                else:
                    m = (-1 / 3) * log(1 - uniform(0, 1))
                    self.proxima_llegada = self.hora_actual + m

            elif self.hora_actual == min(self.proximas_atenciones):
                s = self.proximas_atenciones.index(min(self.proximas_atenciones))
                # print(f"Se va un cliente a las {self.hora_actual}
                # de la caja {s+1}")

                self.colas[s].popleft()
                

                if len(self.colas[s]) != 0:

                    #print(f"Tiempo de espera de cliente atendido
                    # en caja {s+1} recientemente: {self.hora_actual -
                    # self.colas[s][0].hora_ingresocola_estadistica}")
                    self.espera_de_clientes.append\
                          ((self.hora_actual -
                           self.colas[s][0].hora_ingresocola_estadistica))
                    h = (-5)*log(1 - uniform(0, 1))

                    self.proximas_atenciones[s] = self.hora_actual + h
                else:
                    self.proximas_atenciones[s] = 3000
                        
                        
                    

            elif self.hora_actual == min(self.llegadas_cola):
                m = self.llegadas_cola.index(min(self.llegadas_cola))
                n = self.cola_mas_corta()[1]
                
                cliente = self.clientes[m]

                # print(f"Llega cliente {cliente.id} a la caja {n+1}
                #  que tiene {len(self.cola_mas_corta()[0])}
                # clientes en la cola.")

                self.clientes[m].hora_ingresocola = 3000
    
                self.colas[n].append(cliente)

                if len(self.colas[n]) == 1:
                    h = (-5) * log(1 - uniform(0, 1))

                    # print("Se agrega un tiempo 0 a la lista de esperas por no haber nadie en cola.")

                    self.espera_de_clientes.append(0)
                    self.proximas_atenciones[n] = \
                        self.hora_actual + h
                    #print(f"Proxima atencion de caja {n}: {h} minutos")

        tiempo2 = clock()
        return tiempo2-tiempo1

    def espera_promedio(self):
        suma = 0
        for tiempo in self.espera_de_clientes:
            suma += tiempo
        return suma/len(self.espera_de_clientes)

    def __str__(self):
        tiempo = self.simular()
        mins = int(self.espera_promedio())
        sec = (self.espera_promedio()) % 1 * 60
        return f"El tiempo de espera promedio fue de {mins} minutos y {sec} " \
               f"segundos.\n" \
               f"Se demoró {tiempo} segundos."


class Cliente:
    ID = 0

    def __init__(self, hora):

        self.id = Cliente.ID
        Cliente.ID += 1
        self.hora_llegada = hora
        m = (-15) * log(1 - uniform(0, 1))
        self.hora_ingresocola = self.hora_llegada + m
        self.hora_ingresocola_estadistica = self.hora_ingresocola
        self.hora_salida = False

sim = Supermercado(16)
print(sim)

