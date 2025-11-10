# 🚀 Desafio 4: Pipeline de Dados AWS (Trusted → Refined)

## 1. Objetivo do Desafio

Este desafio corresponde à **Entrega 4** do "Desafio de Filmes e Séries".

O objetivo principal é processar os dados já limpos e estruturados da camada **Trusted**, aplicar os princípios de modelagem multidimensional e armazená-los na camada **Refined**. Esta camada final deve estar pronta para análise e extração de insights, servindo como fonte de dados para ferramentas de visualização como o Amazon QuickSight (a ser usado na próxima Sprint).

O processamento foi realizado com **Apache Spark** através de um job **AWS Glue Script**, lendo da Trusted Zone e persistindo os dados na Refined Zone em formato PARQUET.

## 2. Escopo da Solução

A arquitetura abaixo demonstra o escopo desta etapa (Parte 4), focando na transformação da camada Trusted para a Refined, utilizando um Job Glue para processamento e o Amazon Athena para validação.

## 3. Configuração do Job (Requisitos)

Conforme solicitado nas instruções do desafio, o job Glue foi configurado sem o uso de Notebooks, diretamente via **Spark script editor**, e com as seguintes especificações de performance e custo:

* **Worker type:** G.1X (Opção de menor configuração)
* **Requested number of workers:** 2 (Quantidade mínima)
* **Job timeout (minutes):** 60

## 4. Evidências da Implementação

Abaixo estão as evidências que comprovam a criação, configuração e execução bem-sucedida da pipeline.

### 4.1. Jobs ETL no AWS Glue

A imagem comprova a criação dos jobs de script no AWS Glue, com destaque para o `glue_process_refined`, responsável por executar a lógica de transformação desta etapa.

![Evidência dos Jobs no AWS Glue](/Sprint%207/Evidencias/PROCESS_REFINED.png)

### 4.2. Configuração do Job (Evidência)

Esta imagem comprova que as configurações de `Worker type`, `Requested number of workers` e `Job timeout` foram aplicadas no job `glue_process_refined` de acordo com os requisitos do desafio.

### 4.3. Resultado no S3 (Camada Refined)

Após a execução do job, os dados processados e modelados foram salvos em formato Parquet no bucket S3, devidamente separados nas pastas `Filmes/` e `Series/`, prontos para serem catalogados.

![Evidência da camada Refined no S3](/Sprint%207/Evidencias/BucketS3.png)

### 4.4. Validação no Amazon Athena

Finalmente, os dados refinados foram catalogados pelo AWS Glue Data Catalog e disponibilizados no banco `datalake_refined`. A consulta `SELECT * ...` executada com sucesso no Amazon Athena demonstra que os dados estão acessíveis, íntegros e prontos para análise.

![Evidência da consulta no Athena](/Sprint%207/Evidencias/AthenaQuery.png)

## 5. Código da Camada Refined (glue_process_refined.py)

Abaixo está o código Python/PySpark utilizado no job `glue_process_refined` para realizar a transformação.

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

trusted_csv_path = "s3://data-lake-luis/Trusted/CSV/"
trusted_json_path = "s3://data-lake-luis/Trusted/JSON/"

# 🔹 Leitura unificada da camada Trusted
df_trusted = (
    glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [trusted_csv_path, trusted_json_path]},
        format="parquet"
    ).toDF()
)

# 🔹 Padronização de nomes e limpeza
df_trusted = df_trusted.dropDuplicates()
for col in df_trusted.columns:
    df_trusted = df_trusted.withColumnRenamed(col, col.strip().lower())

df_trusted = df_trusted.withColumn("data_refinado", F.current_date())

# 🔹 Separação em filmes e séries
df_filmes = df_trusted.filter(F.col("origem") == "movies")
df_series = df_trusted.filter(F.col("origMagem") == "series")

# 🔹 Escrita no S3 Refined
def salvar(df, caminho):
    dynamic = DynamicFrame.fromDF(df, glueContext, "dynamic")
    glueContext.write_dynamic_frame.from_options(
        frame=dynamic,
        connection_type="s3",
        connection_options={"path": caminho},
        format="parquet"
    )

salvar(df_filmes, "s3://data-lake-luis/Refined/Filmes/")
salvar(df_series, "s3://data-lake-luis/Refined/Series/")

job.commit()
```