from random import *
from collections import deque
from datetime import *


class Supermercado:
    def __init__(self):
        self.hora_inicio = datetime(2018, 8, 10, 8, 0, 0)
        self.hora_cierre = datetime(2018, 8, 10, 22, 0, 0)
        self.hora_final = datetime(2018, 8, 11, 1, 0, 0)
        self.hora_actual = datetime(2018, 8, 10, 8, 0, 0)
        self.colas = [deque() for i in range(16)]
        #Tiempo de llegada inicial
        m = expovariate(1/3)
        self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int((m-int(m))*100))
        self.clientes = []
        self.llegadas_cola = [datetime(2018, 8, 11, 1, 0, 0)]
        self.proximas_atenciones = [datetime(2018,8,11,1,0,0) for i in range (16)]
        self.espera_de_clientes = []

    def cola_mas_corta(self):
        mas_corta = [self.colas[0], 0]
        i = 0
        for cola in self.colas:
            if len(cola) < len(mas_corta):
                mas_corta = [cola , i]
            i += 1

        return mas_corta


    def simular(self):
        while self.hora_actual < self.hora_final:

            self.llegadas_cola = [cliente.hora_ingresocola for cliente in self.clientes]+[datetime(2018, 8, 11, 1, 0, 0)]
            print(self.proxima_llegada, min(self.proximas_atenciones), min(self.llegadas_cola))


            self.hora_actual = min(self.proxima_llegada, min(self.proximas_atenciones), min(self.llegadas_cola))
            # Despues de trasladarnos al tiempo, vamos al primero que pase.

            if self.hora_actual == self.proxima_llegada:
                if self.proxima_llegada > self.hora_cierre:
                    self.proxima_llegada = datetime(2018, 8, 11, 1, 0, 0)
                else:
                    self.clientes.append(Cliente(self.hora_actual))
                    m = expovariate(1/3)
                    self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int((m-int(m))*100))

            elif self.hora_actual == min(self.proximas_atenciones):
                s = 0
                for caja in self.proximas_atenciones:
                    if caja == self.hora_actual:
                        cliente_sale = self.colas[s].popleft()
                        if len(self.colas[s]) != 0:
                            self.espera_de_clientes.append((self.hora_actual - self.colas[s][0].hora_ingresocola_estadistica))
                            h = expovariate(1 / 5)
                            self.proximas_atenciones[s] = self.hora_actual + timedelta(minutes=int(h), seconds=int((h - int(h)) * 100))
                        else:
                            self.proximas_atenciones[s] = datetime(2018,8,11,1,0,0)
                        break
                    s += 1

            elif self.hora_actual == min(self.llegadas_cola):

                m = 0
                for llegada_cola in self.llegadas_cola:
                    if llegada_cola == self.hora_actual:
                        cola = self.cola_mas_corta()[0]
                        n = self.cola_mas_corta()[1]
                        cliente = self.clientes[m]
                        cola.append(cliente)
                        cliente.hora_ingresocola_estadistica = cliente.hora_ingresocola
                        cliente.hora_ingresocola = datetime(2018,8,11,1,0,0)

                        if len(cola) == 1:
                            h = expovariate(1/5)
                            self.espera_de_clientes.append(0)
                            self.proximas_atenciones[n] = self.hora_actual + timedelta(minutes=int(h), seconds=int((h-int(h))*100))

                        break
                    m += 1
    def espera_promedio(self):
        lista = []
        for tiempo in self.espera_de_clientes:
            if tiempo != 0:
                lista.append(divmod(tiempo.days * 86400 + tiempo.seconds, 60)[0])
            else:
                lista.append(0)
        return lista



class Cliente:
    ID = 0
    def __init__(self, hora):
        self.id = Cliente.ID
        Cliente.ID += 1
        self.hora_llegada = hora
        m = expovariate(1/15)
        self.hora_ingresocola = self.hora_llegada + timedelta(minutes=int(m), seconds=int((m-int(m))*100))
        self.hora_ingresocola_estadistica = False
        self.hora_salida = False
        
        
       
prueba = Supermercado()
prueba.simular()
h = 0
for x in prueba.espera_promedio():
    h += x
print(h/(len(prueba.espera_promedio())))


        
