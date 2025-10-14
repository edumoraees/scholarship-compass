# Etapa 1 - Dockerfile para ingestão dos arquivos CSV no S3

# 1. Imagem base
FROM python:3.10-slim

# 2. Define diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia os arquivos necessários para dentro do container
COPY ingest_csv.py .
COPY requirements.txt .
COPY data ./data

# 4. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Define o comando padrão ao rodar o container
CMD ["python", "ingest_csv.py"]
