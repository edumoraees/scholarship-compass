import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# ============================================================
# 📌 INPUT TRUSTED
# ============================================================
trusted_movies_path = "s3://data-lake-luis/Trusted/Local/PARQUET/Movies/"
trusted_series_path = "s3://data-lake-luis/Trusted/Local/PARQUET/Series/"
trusted_tmdb_path   = "s3://data-lake-luis/Trusted/TMDB/PARQUET/MoviesSeries/"

movies_df = spark.read.parquet(trusted_movies_path)
series_df = spark.read.parquet(trusted_series_path)
tmdb_df   = spark.read.parquet(trusted_tmdb_path)

# ============================================================
# 🔧 Garantir que movies tenha anotermino
# ============================================================
movies_df = movies_df.withColumn("anotermino", lit(None).cast("int"))

# ============================================================
# 🔗 Unificação de CSV
# ============================================================
csv_df = movies_df.unionByName(series_df)

# ============================================================
# 🧹 FILTRAGEM TMDB (sem budget)
# ============================================================
filtered_tmdb = (
    tmdb_df
    .filter(array_contains(col("genre_ids"), 53) | array_contains(col("genre_ids"), 27))
    .filter(col("vote_average") > 0)
    .filter(col("vote_count") > 5)
    .filter(year(col("release_date")).between(2012, 2022))
)

# ============================================================
# 🔗 JOIN
# ============================================================
refined_df = (
    filtered_tmdb.alias("tmdb")
    .join(csv_df.alias("csv"), col("tmdb.id") == col("csv.id"), "left")
)

# ============================================================
# 🧱 SELEÇÃO FINAL (somente colunas existentes)
# ============================================================
final_df = (
    refined_df.select(
        col("tmdb.id"),
        col("tmdb.title"),
        col("tmdb.release_date"),
        col("tmdb.popularity"),
        col("tmdb.vote_average"),
        col("tmdb.vote_count"),
        col("tmdb.genre_ids"),
        col("tmdb.original_language"),
        col("csv.tituloprincipal"),
        col("csv.anolancamento"),
        col("csv.anotermino")
    )
    .withColumn("ano", year(col("release_date")))
    .withColumn("mes", month(col("release_date")))
    .withColumn("dia", dayofmonth(col("release_date")))
)

# ============================================================
# 💾 OUTPUT
# ============================================================
refined_path = "s3://data-lake-luis/Refined/FilmesSeries/"

(
    final_df
    .write
    .mode("overwrite")
    .partitionBy("ano", "mes", "dia")
    .parquet(refined_path)
)

job.commit()
