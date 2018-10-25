from math import log

x_inicial = 302
conjunto = set()
for i in range(100):
    x = ((40*x_inicial) % 33)
    conjunto.add(x/33)
    x_inicial = x

print(conjunto)

