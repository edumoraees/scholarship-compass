# 🧾 Documentação – Etapa Trusted e Refined

---

## 🎯 Objetivo

Transformar os dados das camadas **Raw** → **Trusted** → **Refined** dentro do Data Lake no S3, padronizando e preparando os datasets para análise no Amazon Athena e futura visualização no Amazon QuickSight.

---

## 🗺️ Fluxo da Pipeline

> ```text
> S3 (Raw)
> ├── Local/CSV/movies/
> └── Local/CSV/series/
>     ↓
> AWS Glue Job (glue_process_csv)
>     ↓
> S3 (Trusted)
> ├── CSV/
> └── JSON/
>     ↓
> AWS Glue Job (glue_process_refined)
>     ↓
> S3 (Refined)
> ├── Filmes/
> └── Series/
>     ↓
> AWS Glue Catalog + Athena
>     ↓
> QuickSight (Gold Layer - visualização)
> ```

---

## ⚙️ 1. Job Glue – Trusted Layer (glue_process_csv.py)

### Função

* Ler recursivamente os arquivos CSV das pastas de filmes e séries.
* Detectar o schema automaticamente (`inferSchema`).
* Adicionar metadados (colunas `origem`, `data_processamento`).
* Salvar em formato **Parquet** na camada Trusted.

### Código

```python
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

def read_csv_recursive(path, origem):
    df = (
        spark.read
        .option("header", True)
        .option("delimiter", "|")
        .option("quote", '"')
        .option("escape", '"')
        .option("inferSchema", True)
        .option("recursiveFileLookup", True)
        .csv(path)
        .withColumn("origem", F.lit(origem))
        .withColumn("data_processamento", F.current_timestamp())
    )
    return df

raw_movies_path = "s3://data-lake-luis/Raw/Local/CSV/movies/"
raw_series_path = "s3://data-lake-luis/Raw/Local/CSV/series/"
trusted_output_path = "s3://data-lake-luis/Trusted/CSV/"

movies_df = read_csv_recursive(raw_movies_path, "movies")
series_df = read_csv_recursive(raw_series_path, "series")

df_union = movies_df.unionByName(series_df, allowMissingColumns=True)

(
    df_union.write
    .mode("overwrite")
    .format("parquet")
    .save(trusted_output_path)
)

job.commit()
```

### ✅ Resultado Esperado

* Arquivos Parquet criados em `s3://data-lake-luis/Trusted/CSV/`
* Colunas padronizadas.
* Campos adicionados: `origem`, `data_processamento`.

---

## 🧩 2. Job Glue – Refined Layer (glue_process_refined.py)

### Função

* Ler dados da camada **Trusted** (provenientes de CSV e JSON).
* Padronizar colunas (remover espaços, converter para minúsculas) e corrigir formatações.
* Adicionar coluna `data_refinado`.
* Salvar dados finalizados e separados nas pastas `Filmes` e `Series`.

### Código

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
df_series = df_trusted.filter(F.col("origem") == "series")

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

### ✅ Resultado Esperado

* Dados gravados em `s3://data-lake-luis/Refined/Filmes/`
* Dados gravados em `s3://data-lake-luis/Refined/Series/`
* Colunas com nomes padronizados (ex: `tituloprincipal`, `genero`, `notamedia`, etc).
* Campos extras: `origem`, `data_refinado`.

---

## 🏛️ 3. Criação do Banco de Dados (Athena)

```sql
CREATE DATABASE datalake_refined;
```

---

## 📊 4. Resultados Obtidos

| Resultado | Descrição |
| :--- | :--- |
| ✅ **Arquivos .parquet válidos** | Nenhum erro de schema |
| ✅ **Dados completos** | Campos **titulo**, **genero**, **notamedia**, etc |
| ✅ **Athena funcionando** | Consultas e filtros executados com sucesso |
| ✅ **Preparado para QuickSight** | Estrutura limpa, pronta para camada **Gold** |