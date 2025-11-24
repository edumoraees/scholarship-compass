#  Desafio de Filmes & Séries - Final

## 📊 Construção da Camada Refined + Dashboard no QuickSight

Este documento apresenta toda a documentação referente à **Parte 5** do Desafio de Filmes & Séries, cobrindo a modelagem dimensional da camada **Refined**, os processos de transformação de dados e a criação de um **dashboard analítico no Amazon QuickSight**.

---

## 📌 1. Objetivo da Entrega

O objetivo principal da Parte 5 é permitir o **consumo analítico** dos dados processados nas etapas anteriores, através de:

* ✔ Modelagem dimensional na camada **Refined**
* ✔ Criação das tabelas Dimensão + Fato
* ✔ Criação de um dataset final no QuickSight
* ✔ Construção de um dashboard com visualizações analíticas

Essa etapa fecha o ciclo completo do Data Lake:

> **RAW → TRUSTED → REFINED → ANALYTICS (QUICKSIGHT)**

---

## 📁 2. Arquitetura Geral da Solução

A arquitetura final da Parte 5 segue o padrão recomendado pelo desafio:

**S3 Raw → Glue ETL → Trusted → Glue ETL → Refined (Dimensões + Fato)**

**→ Athena → QuickSight → Dashboard Publicado**

---

## 🗂️ 3. Estrutura da Camada Refined (no S3)

A camada Refined foi organizada conforme orientações do desafio:
data-lake-luis/ └── Refined/ ├── DimFilmeSerie/ ├── DimGenero/ ├── DimData/ └── FatoCatalogo/
Cada pasta armazena dados em **formato Parquet**, prontos para consumo via **Athena** e **QuickSight**.

---

## 🧱 4. Modelo Dimensional (Star Schema)

O modelo dimensional criado segue um padrão **estrela (star schema)**:
    DimGenero
         (id_genero)
             │
             │
DimData ←── FatoCatalogo ──→ DimFilmeSerie (id_data) (id_titulo) (id_titulo)

### ✔ Tabelas:

#### **📌 FatoCatalogo**
Contém as métricas analíticas e as chaves estrangeiras:
* `id_titulo` (FK)
* `id_genero` (FK)
* `id_data` (FK)
* `popularity`
* `vote_average`
* `vote_count`

#### **📌 DimFilmeSerie**
Contém os atributos dos títulos:
* `id_titulo` (PK)
* `titulo`
* `titulo_principal`
* `original_language`
* `anolancamento`
* `anotermino`
* `overview`
* `poster_path`
* `backdrop_path`

#### **📌 DimGenero**
Contém os nomes dos gêneros:
* `id_genero` (PK)
* `nome_genero`

#### **📌 DimData**
Contém os atributos de tempo para análise:
* `id_data` (PK)
* `release_date`
* `ano`
* `mes`
* `dia`

---

## 🖥️ 5. Script Glue – Criação da Camada Refined

O script abaixo foi responsável por transformar os dados Trusted em tabelas dimensionais e fato:

```python
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


movies_df = spark.read.parquet("s3://data-lake-luis/Trusted/Local/PARQUET/Movies/")
series_df = spark.read.parquet("s3://data-lake-luis/Trusted/Local/PARQUET/Series/")
tmdb_df   = spark.read.parquet("s3://data-lake-luis/Trusted/TMDB/PARQUET/MoviesSeries/")


csv_df = movies_df.unionByName(series_df, allowMissingColumns=True)


filtered_tmdb = (
    tmdb_df
    .filter(array_contains(col("genre_ids"), 53) | array_contains(col("genre_ids"), 27))
    .filter(col("vote_average") > 0)
    .filter(col("vote_count") > 5)
    .filter(year(col("release_date")).between(2012, 2022))
)

joined = (
    filtered_tmdb.alias("t")
    .join(csv_df.alias("c"), col("t.id") == col("c.id"), "left")
)


dim_filme_serie = (
    joined.select(
        col("t.id").alias("id_titulo"),
        col("t.title").alias("titulo"),
        col("c.tituloprincipal").alias("titulo_principal"),
        col("t.original_language"),
        col("c.anolancamento"),
        col("c.anotermino"),
        col("t.overview"),
        col("t.poster_path"),
        col("t.backdrop_path")
    ).dropDuplicates(["id_titulo"])
)


dim_genero = (
    joined
    .select(explode(col("t.genre_ids")).alias("id_genero"))
    .dropDuplicates()
    .withColumn("nome_genero",
        when(col("id_genero") == 27, "Horror")
        .when(col("id_genero") == 53, "Thriller")
        .otherwise("Desconhecido")
    )
)


dim_data = (
    joined
    .select(col("t.release_date"))
    .dropna()
    .withColumn("id_data", date_format("release_date", "yyyyMMdd").cast("int"))
    .withColumn("ano", year("release_date"))
    .withColumn("mes", month("release_date"))
    .withColumn("dia", dayofmonth("release_date"))
    .dropDuplicates(["id_data"])
)


fato = (
    joined
    .withColumn("id_data", date_format("t.release_date", "yyyyMMdd").cast("int"))
    .select(
        col("t.id").alias("id_titulo"),
        explode(col("t.genre_ids")).alias("id_genero"),
        col("id_data"),
        col("t.popularity"),
        col("t.vote_average"),
        col("t.vote_count")
    )
)


base = "s3://data-lake-luis/Refined/"

dim_filme_serie.write.mode("overwrite").parquet(base + "DimFilmeSerie/")
dim_genero.write.mode("overwrite").parquet(base + "DimGenero/")
dim_data.write.mode("overwrite").parquet(base + "DimData/")
fato.write.mode("overwrite").parquet(base + "FatoCatalogo/")

job.commit()
```

## ⚙️ 6. Glue Crawlers

Foram criados **4 crawlers**, um para cada entidade, todos apontando para a camada Refined no S3:

* `crawler_dim_data`
* `crawler_dim_filmeserie`
* `crawler_dim_genero`
* `crawler_fato_catalogo`

Todos atualizam o banco: **`refined_data_lake`**



---

## 🔎 7. Criação do Dataset no QuickSight

O dataset analítico foi criado no QuickSight, utilizando o **Athena** como fonte de dados para acessar a camada Refined:

* **Fonte de dados:** Athena
* **Banco:** `AwsDataCatalog`
* **Esquema:** `refined_data_lake`
* **Tabelas importadas:** `DimFilmeSerie`, `DimGenero`, `DimData`, `FatoCatalogo`

### **Junções Realizadas (INNER JOIN):**

| Tabela Fato | Chave da Fato | Chave da Dimensão | Tabela Dimensão |
| :--- | :--- | :--- | :--- |
| `FatoCatalogo` | `id_titulo` | `id_titulo` | `DimFilmeSerie` |
| `FatoCatalogo` | `id_genero` | `id_genero` | `DimGenero` |
| `FatoCatalogo` | `id_data` | `id_data` | `DimData` |



---

## 📊 8. Dashboard Construído no QuickSight

Foram criadas 3 visualizações principais no dashboard:

### 📈 8.1. Gráfico de barras – Média de notas por gênero

* **Eixo X:** `nome_genero`
* **Valor:** Média de `vote_average`


### 📉 8.2. Histograma – Distribuição de vote_average

Mostra como as avaliações (`vote_average`) estão distribuídas no dataset.


### 📋 8.3. Tabela – Títulos mais populares (Popularity + Ano)

| Coluna | Descrição |
| :--- | :--- |
| `titulo` | Título principal do filme/série |
| `popularity` | Métrica de popularidade |
| `ano` | Ano de lançamento |


---

## 📝 9. Conclusões

A análise construída permitiu:

* **Identificar** gêneros mais bem avaliados.
* **Observar** a distribuição das notas no catálogo.
* **Analisar** os títulos com maior popularidade.
* **Cruzar** informações entre diferentes dimensões.
* **Validar** a eficiência da modelagem dimensional (Star Schema).

A camada **Refined** foi estruturada corretamente e está preparada para análises avançadas, machine learning e exploração de dados via Athena e QuickSight.

---

## 📦 10. Entregáveis

* ✔ Código dos Jobs Glue
* ✔ Script da camada Refined
* ✔ Imagens do Glue Data Catalog
* ✔ Dashboard publicado (PDF)
* ✔ README.md (este arquivo)

## Evidências 

![Dashboards](/Sprint%208/Evidencias/4Dash.png)  
![Grafico de Barras Verticais](/Sprint%208/Evidencias/BarrasVerticais.png)
![Gráfico Histograma](/Sprint%208/Evidencias/HistogramaQuickSight.png)
![Gráfico de tabela](/Sprint%208/Evidencias/PopularityDesc.png)
![Dimensão e Fato](/Sprint%208/Evidencias/DimeFato.png)
![Crawlers](/Sprint%208/Evidencias/Crawlers.png)
![Database](/Sprint%208/Evidencias/database.png)