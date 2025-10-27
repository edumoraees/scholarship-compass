# etapa1.py
import random


# Gera 250 números inteiros aleatórios entre 1 e 1000
numeros = [random.randint(1, 1000) for _ in range(250)]

# Inverte a lista
numeros.reverse()

# Imprime o resultado
print("Lista invertida de números aleatórios:")
print(numeros)
