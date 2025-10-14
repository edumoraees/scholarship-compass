
# 🎬 Desafio Data Lake - Filmes e Séries  
### Etapas 1 e 2 — Ingestão de Dados (CSV + API TMDB)

---

## 🧩 1. Objetivo Geral

O objetivo deste desafio é aplicar, de forma prática, os conhecimentos adquiridos durante o programa, construindo um **Data Lake** com as camadas de **Ingestão, Armazenamento, Processamento e Consumo**.  
O contexto envolve dados de filmes e séries obtidos a partir de **arquivos CSV locais** e da **API pública do TMDB (The Movie Database)**.

---

## 🚀 2. Etapa 1 — Ingestão de Arquivos CSV no Amazon S3 (via Docker)

### 🎯 Objetivo
Desenvolver um container **Docker** capaz de realizar a **ingestão batch** dos arquivos CSV (`filmes.csv` e `series.csv`) para a camada **RAW** do bucket S3.  
Essa ingestão representa a primeira camada do Data Lake, sem tratamento ou filtragem dos dados.

---

### 🧱 Estrutura do Projeto

```
📁 desafio-etapa1/
│
├── ingest_csv.py
├── Dockerfile
├── requirements.txt
└── data/
    ├── movies.csv
    └── series.csv
```

---

### ⚙️ Dockerfile Utilizado

```dockerfile
# Etapa 1 - Dockerfile para ingestão dos arquivos CSV no S3

FROM python:3.10-slim
WORKDIR /app
COPY ingest_csv.py .
COPY requirements.txt .
COPY data ./data
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "ingest_csv.py"]
```

---

### 🐍 Script de Ingestão (`ingest_csv.py`)

O script lê os arquivos CSV e realiza o upload para o S3 utilizando a biblioteca `boto3`, gravando no bucket `data-lake-luis` na camada **Raw/Local/CSV**, conforme o padrão:

```
s3://data-lake-luis/Raw/Local/CSV/<categoria>/<ano>/<mês>/<dia>/<arquivo>.csv
```

```
import boto3
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Configurações
BUCKET_NAME = os.getenv("BUCKET_NAME", "data-lake-luis")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
RAW_ZONE = "Raw/Local/CSV"

# Caminhos locais dos arquivos CSV
FILES = {
    "movies": "./data/movies.csv",
    "series": "./data/series.csv"
}

def upload_to_s3(file_path, s3_client, tipo):
    """
    Faz upload de um arquivo CSV para o S3 seguindo o padrão de path definido no desafio.
    """
    now = datetime.now()
    year, month, day = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    
    file_name = os.path.basename(file_path)
    s3_key = f"{RAW_ZONE}/{tipo}/{year}/{month}/{day}/{file_name}"

    print(f"Enviando {file_name} para s3://{BUCKET_NAME}/{s3_key}")

    try:
        s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
        print(f"✅ Upload concluído: {s3_key}")
    except Exception as e:
        print(f"❌ Erro ao enviar {file_path}: {e}")

def main():
    # Cria cliente boto3
    s3 = boto3.client("s3", region_name=AWS_REGION)

    # Faz upload de cada arquivo CSV
    for tipo, path in FILES.items():
        if os.path.exists(path):
            upload_to_s3(path, s3, tipo)
        else:
            print(f"⚠️ Arquivo não encontrado: {path}")

if __name__ == "__main__":
    main()

```

---

### 📦 Estrutura de Armazenamento no S3

```
data-lake-luis/
└── Raw/
    └── Local/
        └── CSV/
            ├── movies/
            │   └── 2025/10/09/movies.csv
            └── series/
                └── 2025/10/09/series.csv
```

---

### 🖼️ Evidências Etapa 1

![Bucket criado](/Sprint%205/Evidencias/desafio-etapa1/bucket-criado.png)  
![Caminho criado](/Sprint%205/Evidencias/desafio-etapa1/caminho-criado.png)  
![CSV importado](/Sprint%205/Evidencias/desafio-etapa1/csv-importado.png)

---

## ☁️ 3. Etapa 2 — Ingestão de Dados da API TMDB com AWS Lambda

### 🎯 Objetivo

Capturar dados adicionais sobre filmes e séries diretamente da **API do TMDB**, persistindo-os no bucket S3 na camada **RAW/TMDB/JSON**.  
Essa ingestão é feita por uma função **AWS Lambda** que se comunica com a API e envia os dados agrupados em arquivos JSON com até 100 registros.

---

### ⚙️ Configuração da Função Lambda

**Nome da função:** `lambda_ingestao_tmdb`  
**Runtime:** Python 3.10  
**Permissões IAM:**  
- `AWSLambdaBasicExecutionRole`  
- `AmazonS3FullAccess`  

**Variáveis de ambiente:**  
| Chave         | Valor              |
|----------------|--------------------|
| `TMDB_API_KEY` | *(sua chave pessoal do TMDB)* |
| `BUCKET_NAME`  | data-lake-luis     |

![Variáveis de ambiente](/Sprint%205/Evidencias/desafio-etapa2/variaveis_de_ambiente.png)

---

### 🧠 Código da Função (`lambda_function.py`)

```python
import os, json, boto3, urllib.request
from datetime import datetime

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME", "data-lake-luis")
RAW_ZONE = "Raw/TMDB/JSON"
s3 = boto3.client("s3")

def fetch_movies_by_genre(genre_name, genre_id, pages=5):
    all_results = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&with_genres={genre_id}&page={page}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            all_results.extend(data.get("results", []))
    return all_results

def lambda_handler(event, context):
    genres = {"thriller": 53, "horror": 27}
    today = datetime.now().strftime("%Y/%m/%d")

    for genre_name, genre_id in genres.items():
        print(f"🎬 Coletando filmes de {genre_name.upper()}...")
        movies = fetch_movies_by_genre(genre_name, genre_id, pages=10)
        print(f"📦 Total coletado: {len(movies)} filmes de {genre_name}")

        for i in range(0, len(movies), 100):
            part = i // 100 + 1
            file_name = f"{genre_name}_{part:03d}.json"
            key = f"{RAW_ZONE}/{today}/{file_name}"

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=json.dumps(movies[i:i+100], indent=2),
                ContentType="application/json"
            )
            print(f"✅ Enviado: s3://{BUCKET_NAME}/{key}")

    return {"statusCode": 200, "body": json.dumps("Coleta concluída e arquivos enviados para o S3.")}
```

---

### 📁 Estrutura da Camada TMDB/JSON no S3

```
data-lake-luis/
└── Raw/
    └── TMDB/
        └── JSON/
            └── 2025/10/13/
                ├── horror_001.json
                ├── horror_002.json
                ├── thriller_001.json
                └── thriller_002.json
```

---

### 🧩 Evidências Etapa 2

![Arquivos JSON](/Sprint%205/Evidencias/desafio-etapa2/arquivos_json.png)  
![Função Lambda](/Sprint%205/Evidencias/desafio-etapa2/func_lambda.png)  
![Variáveis de ambiente](/Sprint%205/Evidencias/desafio-etapa2/variaveis_de_ambiente.png)

---

## 🧾 4. Conclusão Final

- A **Etapa 1** garantiu a ingestão batch dos arquivos CSV originais (filmes e séries), utilizando Docker e `boto3`.  
- A **Etapa 2** complementou o Data Lake com dados atualizados do TMDB via AWS Lambda, ampliando o conjunto de dados disponíveis.  
- Ambas as etapas seguem o padrão de organização definido pelo desafio, gravando os arquivos na camada **RAW** com hierarquia de diretórios por data.

✅ **Resultado Final:**  
O bucket `data-lake-luis` contém as camadas **Raw/Local/CSV** e **Raw/TMDB/JSON**, representando o sucesso das duas primeiras fases do Data Lake de Filmes e Séries.
