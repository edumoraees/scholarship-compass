# 🚀 Laboratório – Apache Spark e Geração de Dados

## 🎯 Objetivo Geral

Aplicar na prática os fundamentos de **manipulação de dados** com Python e **Apache Spark**, desenvolvendo scripts que geram dados sintéticos e, em seguida, realizam consultas e análises com o PySpark.

---

## 🧩 **Exercício 1 – Geração de Dados**

### 🧠 Etapa 1 – Lista de Números Aleatórios

Criação de 250 números inteiros aleatórios entre 1 e 1000 e inversão da lista.

**Script:** `etapa3.1.py`

```python
import random

numeros = [random.randint(1, 1000) for _ in range(250)]
numeros.reverse()

print("Lista invertida de números aleatórios:")
print(numeros)
```

📄 **Resultado:** lista de números impressa no console, demonstrando uso de listas e funções nativas do Python.

---

### 🐾 Etapa 2 – Lista de Animais Ordenada

Criação de uma lista com 20 animais, ordenação alfabética e gravação em arquivo `.txt`.

**Script:** `etapa3.2.py`
**Saída:** `animais.txt`

Exemplo de conteúdo:

```
cachorro
cavalo
coelho
elefante
gato
...
```

---

### 👥 Etapa 3 – Geração de Nomes Aleatórios

Uso da biblioteca [`names`](https://pypi.org/project/names/) para gerar **milhões de nomes completos** aleatórios e gravar em arquivo.

**Script:** `etapa3.3.py`
**Saída:** `nomes_aleatorios.txt`

Esse arquivo será utilizado no **Exercício 2**.

---

## ⚙️ **Exercício 2 – Manipulação com PySpark**

### 🧩 Objetivo

Trabalhar com DataFrames e consultas SQL utilizando o Apache Spark para manipular o arquivo `nomes_aleatorios.txt` gerado anteriormente.

---

### 💚 Etapas Executadas

1. Criar sessão Spark.
2. Ler `nomes_aleatorios.txt` como DataFrame e renomear a coluna para `Nomes`.
3. Adicionar colunas aleatórias:

   * `Escolaridade` (Fundamental, Médio, Superior)
   * `Pais` (13 países da América do Sul)
   * `AnoNascimento` (entre 1945 e 2010)
4. Filtrar pessoas nascidas neste século (≥ 2000).
5. Contar e agrupar gerações com Spark SQL (Baby Boomers, Geração X, Millennials, Geração Z).

---

### 💻 Execução do Script

```bash
pip install pyspark names
python lab_spark.py
```

---

### 📞 Resultados Esperados

* DataFrame enriquecido com colunas `Escolaridade`, `Pais`, `AnoNascimento`.
* Consultas SQL exibindo:

  * Pessoas nascidas neste século.
  * Quantidade de Millennials (1980–1994).
  * Distribuição por país e geração.

Exemplo:

```
+---------+-------------+------------+
|Pais     |Geracao      |Quantidade  |
+---------+-------------+------------+
|Brasil   |Geração Z    |742         |
|Argentina|Millennials  |681         |
...
```

---

### 🧠 Conclusão

Com esses exercícios foi possível:

* Dominar a leitura, criação e manipulação de arquivos .txt em Python.
* Entender a integração entre **geração de dados** e **processamento distribuído** no Spark.
* Aplicar funções SQL em DataFrames, consolidando a base para análises em grandes volumes de dados.

## 🎯 **Exercício 3 - Laboratório AWS Glue**

Explorar os serviços **AWS S3**, **IAM**, **Lake Formation** e **Glue** para criar um pipeline de dados completo, desde o armazenamento inicial até a catalogação e transformação dos dados.

---

## ⚙️ Parte 1 – Criação do Bucket e Upload de Dados

### 🔹 Objetivo
Criar um bucket no **Amazon S3** e realizar o upload do arquivo `nomes.csv`, que será utilizado nas próximas etapas do laboratório.

### 🔹 Etapas
1. Acessar o console do **Amazon S3**.
2. Criar um bucket nomeado como:
   ```
   meubucket-labglue
   ```
3. Criar a estrutura de diretórios:
   ```
   lab-glue/input/
   ```
4. Fazer upload do arquivo **nomes.csv** para dentro da pasta `input`.

📂 Caminho final:
```
s3://meubucket-labglue/lab-glue/input/nomes.csv
```

📸 Evidência:
![](/Sprint%206/Evidencias/labglue-upload.png)

---

## 🧱 Parte 2 – Criação da Função IAM

### 🔹 Objetivo
Criar uma **IAM Role** que permita que o **AWS Glue** acesse o bucket S3 e demais serviços necessários.

### 🔹 Etapas
1. Acessar o serviço **IAM** → “Funções” → “Criar função”.
2. Selecionar **Serviço AWS Glue** como entidade confiável.
3. Nomear a função como:
   ```
   AWSGlueServiceRole-Lab4
   ```
4. Adicionar as seguintes políticas gerenciadas:
   - AmazonS3FullAccess
   - AWSGlueConsoleFullAccess
   - AWSLakeFormationDataAdmin
   - CloudWatchFullAccess

5. Adicionar a **Trust Policy** abaixo:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

📸 Evidência:
![](/Sprint%206/Evidencias/create-IAM.png)

---

## 🧩 Parte 3 – Laboratório AWS Glue Completo

### 🧾 Etapa 1 – Criação do Banco de Dados
- Criar um banco de dados chamado **glue-lab** no **Glue Data Catalog**.
- Descrição: “Banco de metadados para o laboratório AWS Glue.”

📸 Evidência:
![](/Sprint%206/Evidencias/database-create.png)

---

### 🧠 Etapa 2 – Configuração do Crawler
Criar um crawler com as configurações abaixo:

- **Nome:** crawler-nomes  
- **Fonte de dados:** S3  
- **Caminho:** `s3://meubucket-labglue/lab-glue/input/`  
- **Função IAM:** `AWSGlueServiceRole-Lab4`  
- **Banco de destino:** `glue-lab`  
- **Agendamento:** Sob demanda  
- **Recrawl:** All subfolders  

📸 Evidência:
![](/Sprint%206/Evidencias/crawler-create.png)

---

### 🗄️ Etapa 3 – Configuração no Lake Formation
Conceder permissões de acesso no **Lake Formation** para a função `AWSGlueServiceRole-Lab4`.

✅ Permissões concedidas:
- Create table  
- Alter  
- Drop  
- Select  
- Insert  
- Delete  
- Describe

---

### 🔍 Etapa 4 – Execução do Crawler
Após executar o crawler, uma tabela chamada **input** foi criada automaticamente no banco **glue-lab**.

**Localização dos dados:**  
`s3://meubucket-labglue/lab-glue/input/`

**Classificação:** CSV  
**Status:** Ativo  

📸 Evidência:
![](/Sprint%206/Evidencias/query-select.png)

---

### 🧮 Etapa 5 – Execução do Job ETL
Foi criado um Job ETL no Glue Studio para processar e transformar os dados.  
Durante o processo, ajustes de permissão foram aplicados à role `AWSGlueServiceRole-Lab4`.

Após correção da política de confiança, o job foi executado com sucesso.

---

### ✅ Conclusão
Com os três exercícios, o ambiente AWS foi configurado para permitir:

- Armazenamento de dados no S3  
- Configuração de permissões via IAM e Lake Formation  
- Catalogação e transformação de dados com AWS Glue  

🧠 **Resultado:** Pipeline de dados funcional e pronto para consultas no **Athena**.