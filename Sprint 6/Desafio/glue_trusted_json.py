import sys
from datetime import datetime

from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import lit


# Parâmetros do JOB

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


# CONFIGURAÇÕES

bucket = "data-lake-luis"

tmdb_raw_path = f"s3://{bucket}/Raw/TMDB/JSON/"
tmdb_trusted_path = f"s3://{bucket}/Trusted/TMDB/PARQUET/MoviesSeries/"

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")


# LEITURA DOS JSONs

tmdb_dyf = glueContext.create_dynamic_frame_from_options(
    connection_type="s3",
    connection_options={"paths": [tmdb_raw_path], "recurse": True},
    format="json",
    format_options={"multiline": True}
)

# Converte para DataFrame para adicionar partições
df = tmdb_dyf.toDF()

df = (
    df
    .withColumn("year", lit(year))
    .withColumn("month", lit(month))
    .withColumn("day", lit(day))
)

tmdb_trusted_dyf = DynamicFrame.fromDF(df, glueContext, "tmdb_trusted")

# ESCRITA DOS DADOS NO FORMATO PARQUET COM PARTIÇÕES
glueContext.write_dynamic_frame.from_options(
    frame=tmdb_trusted_dyf,
    connection_type="s3",
    connection_options={
        "path": tmdb_trusted_path,
        "partitionKeys": ["year", "month", "day"]
    },
    format="parquet"
)

job.commit()
