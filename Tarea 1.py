from random import *
from collections import deque
from datetime import *


class Supermercado:
    def __init__(self):
        self.hora_inicio = datetime(2018, 8, 10, 8, 0, 0)
        self.hora_final = datetime(2018, 8, 10, 22, 0, 0)
        self.hora_actual = datetime(2018, 8, 10, 8, 0, 0)
        self.colas = [deque() for i in range(16)]
        #Tiempo de llegada inicial
        m = expovariate(1/3)
        self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int((m-int(m))*100))
        self.llegadas_cola = [cliente.hora_ingresocola for cliente in self.clientes]
        self.proximas_atenciones = [datetime(2018,8,10,23,0,0) for i in range (16)]
        self.clientes = []
        self.espera_de_clientes = []


    def simular(self):
        while self.hora_actual < self.hora_final:
            for cliente in self.clientes:
                if cliente.hora_salida == False:
                    break
                self.hora_actual = datetime(2018,8,10,23,0,0)
            self.hora_actual = min(self.proxima_llegada,min(self.proximas_atenciones),min(self.llegadas_cola))
            #Después de trasladarnos al tiempo, vamos al primero que pase.
            if self.hora_actual == self.proxima_llegada:
                self.clientes.append(Cliente(self.hora_actual))
                m = expovariate(1/3)
                self.proxima_llegada = self.hora_actual + timedelta(minutes=int(m), seconds=int((m-int(m))*100))
            elif self.hora_actual == min(self.proximas_atenciones):
                s = 0
                for caja in self.proximas_atenciones:
                    if caja == self.hora_actual:
                        cliente_sale = self.colas[s].pop()
                        self.espera_de_clientes.append((cliente_sale.hora_salida - cliente_sale.hora_ingresocola))
                        break
                    s += 1





class Cliente:
    ID = 0
    def __init__(self, hora):
        self.id = Cliente.ID
        Cliente.ID += 1
        self.hora_llegada = hora
        m = expovariate(1/15)
        self.hora_ingresocola = self.hora_llegada + timedelta(minutes=int(m), seconds=int((m-int(m))*100))
        self.hora_salida = False
        
        
       


        
