# 📋 Etapas

## 1️⃣ Arquivo `Dockerfile` para executar o código `carguru.py`

- Primeiro salvei o arquivo [carguru.py](Etapa-1/app/carguru.py) dentro de uma pasta chamada app.
- Em seguida criei o arquivo dockerfile para gerar uma imagem, e utilizei como base python3.
```
FROM python:3

WORKDIR /app

COPY . .

CMD ["python3", "app/carguru.py"]
```
- Para criar a imagem e o container usei os comandos:
```
docker build -t carguru .
```
```
docker run -it --name container-carguru carguru
```

## 2️⃣  Criação de script capaz de receber strings via input, gerar o hash da string por meio do algoritmo `SHA-1` e imprimir na tela com o método `hexdigest()`.
- Script de mascaramento:
```
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
```
- Em seguida também criei um arquivo dockerfile com base na imagem python3
  ```
  FROM python:3

  WORKDIR /app

  COPY . .

  CMD ["python3", "app/index.py"]
  ```

- E novamente na criação da imagem e do container, usei os comandos: 
  ```
  docker build -t mascarar-dados .
  ```
  ```
  docker run -it --name container-mascaramento mascarar-dados
  ```

## Evidências em execução

* Imagens que contém no meu docker.
![Docker](/Sprint%203/Evidencias/Exercicios/DockerImages.png)

* Iniciando container carguru.
![Docker](/Sprint%203/Evidencias/Exercicios/DockerRUN-Carguru.png)

* Iniciando container mascarar-dados.

  ![Docker](/Sprint%203/Evidencias/Exercicios/DockerRUN-MascararDados.png)