import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import split
from pyspark.sql.types import IntegerType, DoubleType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3 = boto3.client("s3")
bucket = "data-lake-luis"


# FUNÇÃO PARA BUSCAR O ÚLTIMO CSV


def get_latest_csv(prefix):
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".csv")]

    if not files:
        raise Exception(f"Nenhum CSV encontrado em: {prefix}")

    # Retorna o mais recente pela ordem alfabética (AAAA/MM/DD)
    return sorted(files)[-1]


# PROCESSAR MOVIES


latest_movies = get_latest_csv("Raw/Local/CSV/movies/")
print(f"📌 Último CSV de movies: {latest_movies}")

df_movies = spark.read.option("header", "false").text(f"s3://{bucket}/{latest_movies}")

col = split(df_movies["value"], "\|")

df_movies = df_movies.withColumn("id", col.getItem(0)) \
       .withColumn("tituloPrincipal", col.getItem(1)) \
       .withColumn("tituloOriginal", col.getItem(2)) \
       .withColumn("anoLancamento", col.getItem(3).cast(IntegerType())) \
       .withColumn("tempoMinutos", col.getItem(4).cast(IntegerType())) \
       .withColumn("genero", col.getItem(5)) \
       .withColumn("notaMedia", col.getItem(6).cast(DoubleType())) \
       .withColumn("numeroVotos", col.getItem(7).cast(IntegerType())) \
       .withColumn("generoArtista", col.getItem(8)) \
       .withColumn("personagem", col.getItem(9)) \
       .withColumn("nomeArtista", col.getItem(10)) \
       .withColumn("anoNascimento", col.getItem(11).cast(IntegerType())) \
       .withColumn("anoFalecimento", col.getItem(12).cast(IntegerType())) \
       .withColumn("profissao", col.getItem(13)) \
       .withColumn("titulosMaisConhecidos", col.getItem(14))

df_movies = df_movies.drop("value")

df_movies.write.mode("overwrite").parquet("s3://data-lake-luis/Trusted/Local/PARQUET/Movies/")

print("✅ Movies salvos na Trusted")


# PROCESSAR SERIES
# MESMO PROCEDIMENTO


latest_series = get_latest_csv("Raw/Local/CSV/series/")
print(f"📌 Último CSV de series: {latest_series}")

df_series = spark.read.option("header", "false").text(f"s3://{bucket}/{latest_series}")

col_s = split(df_series["value"], "\|")

df_series = df_series.withColumn("id", col_s.getItem(0)) \
       .withColumn("tituloPrincipal", col_s.getItem(1)) \
       .withColumn("tituloOriginal", col_s.getItem(2)) \
       .withColumn("anoLancamento", col_s.getItem(3).cast(IntegerType())) \
       .withColumn("anoTermino", col_s.getItem(4).cast(IntegerType())) \
       .withColumn("tempoMinutos", col_s.getItem(5).cast(IntegerType())) \
       .withColumn("genero", col_s.getItem(6)) \
       .withColumn("notaMedia", col_s.getItem(7).cast(DoubleType())) \
       .withColumn("numeroVotos", col_s.getItem(8).cast(IntegerType())) \
       .withColumn("generoArtista", col_s.getItem(9)) \
       .withColumn("personagem", col_s.getItem(10)) \
       .withColumn("nomeArtista", col_s.getItem(11)) \
       .withColumn("anoNascimento", col_s.getItem(12).cast(IntegerType())) \
       .withColumn("anoFalecimento", col_s.getItem(13).cast(IntegerType())) \
       .withColumn("profissao", col_s.getItem(14)) \
       .withColumn("titulosMaisConhecidos", col_s.getItem(15))

df_series = df_series.drop("value")

df_series.write.mode("overwrite").parquet("s3://data-lake-luis/Trusted/Local/PARQUET/Series/")

print("✅ Series salvos na Trusted")

job.commit()
print("🎉 Trusted CSV finalizado com sucesso!")
