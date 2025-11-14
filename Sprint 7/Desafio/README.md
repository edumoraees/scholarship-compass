# 📘 Parte 3 – Construção da Camada REFINED (Trusted → Refined)

Este documento descreve todo o processo realizado na Parte 3 do projeto de Data Lake, responsável pela modelagem e criação da camada **Refined** no S3, utilizando AWS Glue e Spark.

---

## 🏗️ Arquitetura da Parte 3

O fluxo desta etapa foca em consumir os dados da camada **Trusted** e transformá-los para a camada **Refined**.

> ```text
> RAW (CSV + JSON)
>     ↓
> TRUSTED (Parquet padronizado)
>     ↓
> REFINED (Modelo analítico)
> ```

Nesta etapa, utilizamos como fonte os dados já padronizados na camada Trusted:

* **Movies:** `s3://data-lake-luis/Trusted/Local/PARQUET/Movies/`
* **Series:** `s3://data-lake-luis/Trusted/Local/PARQUET/Series/`
* **TMDB:** `s3://data-lake-luis/Trusted/TMDB/PARQUET/MoviesSeries/`

---

## 🎯 Objetivo da Parte 3

Transformar os dados da Trusted em uma única tabela refinada, aplicando as seguintes regras de negócio e estruturais:

✔ **Unificação:** Filmes + Séries unificados em um único dataset.
✔ **Enriquecimento:** Dados do CSV local enriquecidos com as informações da API do TMDB.
✔ **Limpeza e Filtragens Obrigatórias:**
* Apenas gêneros **Thriller (53)** ou **Horror (27)**.
* Nota média (`vote_average`) > 0.
* Quantidade de votos (`vote_count`) > 5.
* Data de lançamento (`release_date`) entre 2012 e 2022.
✔ **Modelo Dimensional:** Geração de um modelo dimensional único.
✔ **Formato:** Escrita no S3 em formato **Parquet**.
✔ **Particionamento:** Tabela particionada por `ano`, `mes` e `dia` para otimizar queries.

---

## 🗂️ Estrutura Final do S3

A estrutura de armazenamento final na camada Refined segue o padrão Hive para o particionamento:

```text
data-lake-luis/
└── Refined/
    └── FilmesSeries/
        ├── ano=YYYY/
        │   ├── mes=MM/
        │   │   ├── dia=DD/
        │   │   │   └── part-XXXXX.snappy.parquet
        ...
```

---

## 🧠 Modelagem Refined (Resultado Final)

A tabela final `FilmesSeries` é composta pelas seguintes colunas:

| Campo | Descrição |
| :--- | :--- |
| **id** | ID do título (TMDB) |
| **title** | Título (TMDB) |
| **release_date** | Data de lançamento (TMDB) |
| **popularity** | Popularidade (TMDB) |
| **vote_average** | Nota média (TMDB) |
| **vote_count** | Quantidade de votos (TMDB) |
| **genre_ids** | Lista de gêneros (TMDB) |
| **original_language** | Idioma original (TMDB) |
| **tituloprincipal** | Título principal (CSV) |
| **anolancamento** | Ano inicial (CSV) |
| **anotermino** | Ano final (CSV - séries) |
| **ano** | Ano (Partição) |
| **mes** | Mês (Partição) |
| **dia** | Dia (Partição) |

---

## 🛠️ Job Spark Criado no AWS Glue

* **Nome do job:** `glue_refined_data_lake`
* **Versão do Glue utilizada:** `Glue 3.0 – Spark ETL`

---

## 🧾 Script Utilizado no Job (definitivo)

```python
import sys
from awsglue.transforms import *
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


# 📌 INPUT TRUSTED

trusted_movies_path = "s3://data-lake-luis/Trusted/Local/PARQUET/Movies/"
trusted_series_path = "s3://data-lake-luis/Trusted/Local/PARQUET/Series/"
trusted_tmdb_path   = "s3://data-lake-luis/Trusted/TMDB/PARQUET/MoviesSeries/"

movies_df = spark.read.parquet(trusted_movies_path)
series_df = spark.read.parquet(trusted_series_path)
tmdb_df   = spark.read.parquet(trusted_tmdb_path)

# Unifica movies + series (CSV refinado)
csv_df = movies_df.unionByName(series_df, allowMissingColumns=True)


# 🧹 FILTROS DO TMDB

filtered_tmdb = (
    tmdb_df
    .filter(array_contains(col("genre_ids"), 53) | array_contains(col("genre_ids"), 27))
    .filter(col("vote_average") > 0)
    .filter(col("vote_count") > 5)
    .filter(year(col("release_date")).between(2012, 2022))
)


# 🔗 JOIN CSV + TMDB

# Faz o LEFT JOIN mantendo o TMDB como base (pois já está filtrado)
refined_df = (
    filtered_tmdb.alias("tmdb")
    .join(csv_df.alias("csv"), col("tmdb.id") == col("csv.id"), "left")
)


# 🧱 AJUSTE FINAL DAS COLUNAS

final_df = (
    refined_df.select(
        col("tmdb.id").alias("id"),
        col("tmdb.title").alias("title"),
        col("tmdb.release_date"),
        col("tmdb.popularity"),
        col("tmdb.vote_average"),
        col("tmdb.vote_count"),
        col("tmdb.genre_ids"),
        col("tmdb.original_language"),
        col("csv.tituloprincipal"),
        col("csv.anolancamento"),
        col("csv.anotermino"),
    )
    .withColumn("ano", year(col("release_date")))
    .withColumn("mes", month(col("release_date")))
    .withColumn("dia", dayofmonth(col("release_date")))
)


# 💾 SALVA A CAMADA REFINED

refined_path = "s3://data-lake-luis/Refined/FilmesSeries/"

(
    final_df
    .write
    .mode("overwrite")
    .partitionBy("ano", "mes", "dia")
    .parquet(refined_path)
)

job.commit()
```

---

## 🔍 Crawler da Refined

Para expor os dados ao Athena, um crawler foi criado com as seguintes especificações:

* **Caminho S3:** `s3://data-lake-luis/Refined/FilmesSeries/`
* **Database:** `refined_data_lake`
* **Tabela Gerada:** `filmesseries`