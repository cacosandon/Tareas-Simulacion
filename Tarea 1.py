from random import expovariate
from collections import deque
from datetime import timedelta, datetime


class Supermercado:
    def __init__(self, cajas):
        self.hora_inicio = datetime(2018, 8, 10, 8, 0, 0)
        self.hora_cierre = datetime(2018, 8, 10, 22, 0, 0)
        self.hora_final = datetime(2018, 8, 11, 1, 0, 0)
        self.hora_actual = datetime(2018, 8, 10, 8, 0, 0)
        self.colas = [deque() for i in range(cajas)]
        # Tiempo de llegada inicial
        m = expovariate(3)
        self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int(m % 1 * 60))
        self.clientes = []
        self.llegadas_cola = [datetime(2018, 8, 11, 1, 0, 0)]
        self.proximas_atenciones = [datetime(2018,8,11,1,0,0) for x in range(cajas)]
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

        while self.hora_actual < self.hora_final:

            self.llegadas_cola = [cliente.hora_ingresocola for cliente in self.clientes]+[datetime(2018, 8, 11, 1, 0, 0)]

            self.hora_actual = min(self.proxima_llegada, min(self.proximas_atenciones), min(self.llegadas_cola))
            # Despues de trasladarnos al tiempo, vamos al primero que pase.

            if self.hora_actual == self.proxima_llegada:

                self.clientes.append(Cliente(self.hora_actual))

                # print(f"Ha llegado un cliente a las {self.hora_actual}")

                if self.hora_actual > self.hora_cierre:
                    self.proxima_llegada = datetime(2018, 8, 11, 1, 0, 0)

                else:
                    m = expovariate(3)

                    self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int(m % 1 * 60))

            elif self.hora_actual == min(self.proximas_atenciones):
                s = 0
                for caja in self.proximas_atenciones:
                    if caja == self.hora_actual:

                        # print(f"Se va un cliente a las {self.hora_actual} de la caja {s+1}")

                        self.colas[s].popleft()

                        if len(self.colas[s]) != 0:

                            #print(f"Tiempo de espera de cliente atendido en caja {s+1} recientemente: {self.hora_actual - self.colas[s][0].hora_ingresocola_estadistica}")

                            self.espera_de_clientes.append((self.hora_actual - self.colas[s][0].hora_ingresocola_estadistica))
                            h = expovariate(1/5)

                            self.proximas_atenciones[s] = self.hora_actual + timedelta(minutes=int(h), seconds=int(h % 1 * 60))
                        else:
                            self.proximas_atenciones[s] = datetime(2018, 8, 11, 1, 0, 0)
                        break
                    s += 1

            elif self.hora_actual == min(self.llegadas_cola):
                m = 0
                for llegada_cola in self.llegadas_cola:

                    if llegada_cola == self.hora_actual:

                        n = self.cola_mas_corta()[1]
                        cliente = self.clientes[m]

                        # print(f"Llega cliente {cliente.id} a la caja {n+1} que tiene {len(self.cola_mas_corta()[0])} clientes en la cola.")

                        cliente.hora_ingresocola_estadistica = cliente.hora_ingresocola
                        cliente.hora_ingresocola = datetime(2018, 8, 11, 1, 0, 0)
                        self.colas[n].append(cliente)

                        if len(self.colas[n]) == 1:
                            h = expovariate(1/5)

                            # print("Se agrega un tiempo 0 a la lista de esperas por no haber nadie en cola.")

                            self.espera_de_clientes.append(0)
                            self.proximas_atenciones[n] = \
                                self.hora_actual + \
                                timedelta(minutes=int(h), seconds=int(h % 1 * 60))

                        break
                    m += 1



    def espera_promedio(self):
        lista = []
        for tiempo in self.espera_de_clientes:
            if tiempo != 0:
                lista.append(divmod(tiempo.days * 86400 + tiempo.seconds, 60)[0])
            else:
                lista.append(0)
        return sum(lista)/len(lista)

    def __str__(self):
        self.simular()
        mins = int(self.espera_promedio())
        sec = (self.espera_promedio()) % 1 * 60
        return f"El tiempo de espera promedio fue de {mins} minutos y {sec} segundos."


class Cliente:
    ID = 0

    def __init__(self, hora):

        self.id = Cliente.ID
        Cliente.ID += 1
        self.hora_llegada = hora
        m = expovariate(1/15)
        self.hora_ingresocola = self.hora_llegada + timedelta(minutes=int(m), seconds=int(m%1 * 60))
        self.hora_ingresocola_estadistica = self.hora_ingresocola
        self.hora_salida = False


prueba = Supermercado(16)
print(prueba)
print(len(prueba.clientes))