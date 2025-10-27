# etapa3.py
import random
import names   # instale com: pip install names
import os
# Caminho onde o arquivo será salvo
pasta_destino = r"D:\PB-LUIS-EDUARDO-MORAES\Sprint 6\Exercicios\exec1"

# Caminho completo do arquivo de saída
caminho_arquivo = os.path.join(pasta_destino, "nomes_aleatorios.txt")

# Define a semente e parâmetros
random.seed(40)
qtd_nomes_unicos = 39080
qtd_nomes_aleatorios = 1_000_000

# Gera nomes únicos
print(f"Gerando {qtd_nomes_unicos} nomes únicos...")
nomes_unicos = [names.get_full_name() for _ in range(qtd_nomes_unicos)]

# Gera nomes aleatórios a partir da lista de únicos
print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios...")
dados = [random.choice(nomes_unicos) for _ in range(qtd_nomes_aleatorios)]

# Salva em arquivo
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    for nome in dados:
        f.write(nome + "\n")

print(f"\n✅ Arquivo 'nomes_aleatorios.txt' criado com sucesso em:\n{caminho_arquivo}")
