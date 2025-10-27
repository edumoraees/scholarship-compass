# etapa2.py
import os

# Caminho onde o arquivo será salvo
pasta_destino = r"D:\PB-LUIS-EDUARDO-MORAES\Sprint 6\Exercicios\exec1"

# Caminho completo do arquivo de saída
caminho_arquivo = os.path.join(pasta_destino, "animais.txt")

# Declara e inicializa a lista de 20 animais
animais = [
    "cachorro", "gato", "elefante", "leão", "tigre", "girafa", "zebra",
    "macaco", "urso", "raposa", "lobo", "panda", "golfinho", "tartaruga",
    "águia", "cavalo", "coelho", "rato", "jacaré", "pinguim"
]

# Ordena em ordem alfabética
animais_ordenados = sorted(animais)

# Imprime um por linha
print("Lista de animais ordenada:\n")
[print(a) for a in animais_ordenados]

# Salva o arquivo no caminho definido
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    for a in animais_ordenados:
        f.write(a + "\n")

print(f"\n✅ Arquivo 'animais.txt' criado com sucesso em:\n{caminho_arquivo}")
