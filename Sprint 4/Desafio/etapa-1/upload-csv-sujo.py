import boto3

# Configurações
BUCKET_NAME = "luis-sprint4"
REGION = "us-east-1"
LOCAL_FILE = r"D:\PB-LUIS-EDUARDO-MORAES\Sprint 4\Desafio\etapa-1\InternacoesHospitalares.csv"
S3_KEY = "dados/InternacoesHospitalares.csv"

s3 = boto3.client("s3", region_name=REGION)

if REGION == "us-east-1":
    s3.create_bucket(Bucket=BUCKET_NAME)
else:
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": REGION}
    )
print(f"Bucket '{BUCKET_NAME}' criado.")

s3.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
print(f"Arquivo enviado para: s3://{BUCKET_NAME}/{S3_KEY}")

