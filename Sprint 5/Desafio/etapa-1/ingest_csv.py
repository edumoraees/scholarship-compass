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
