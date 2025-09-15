import hashlib
import unicodedata

def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn').lower()

while True:
    stringInput = input("Coloque a string para mascaramento: ")

    textHash = hashlib.sha1(stringInput.encode()).hexdigest()
    print(f"String mascarada: {textHash}")

    option = normalize(input("Deseja mascarar mais caracteres? (Sim/Não): "))
    if option == "nao":
        break

