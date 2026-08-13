# AWS Data Engineering Scholarship — Compass UOL

Projeto desenvolvido durante o programa de formação em **Engenharia de Dados em Cloud da Compass UOL**, com foco na construção progressiva de soluções de dados utilizando **Python, SQL, PySpark e serviços AWS**.

O repositório está organizado em 8 sprints, abrangendo desde fundamentos de SQL e Python até a construção de um pipeline completo de dados em ambiente AWS.

---

## Projeto Final

O projeto final consiste na construção de um **Data Lake na AWS** para ingestão, processamento, transformação, modelagem e análise de dados relacionados a filmes e séries.

### Arquitetura

```text
CSV + TMDB API
      │
      ▼
 Amazon S3
   RAW Zone
      │
      ▼
AWS Glue / PySpark
      │
      ▼
 Amazon S3
 TRUSTED Zone
      │
      ▼
AWS Glue / PySpark
      │
      ▼
 Amazon S3
 REFINED Zone
      │
      ▼
Star Schema
      │
      ├── Amazon Athena
      │
      └── Amazon QuickSight
```

---

## Tecnologias utilizadas

### Linguagens e processamento

* Python
* SQL
* PySpark
* Pandas

### AWS

* Amazon S3
* AWS Glue
* AWS Lambda
* Amazon Athena
* AWS IAM
* AWS Lake Formation
* AWS Glue Data Catalog
* AWS Glue Crawlers
* Amazon QuickSight

### Outras ferramentas

* Docker
* Git
* GitHub
* Parquet
* TMDB API

---

## Principais conceitos aplicados

* ETL / ELT
* Data Lake
* Processamento distribuído
* Modelagem dimensional
* Star Schema
* Tabelas fato e dimensão
* Particionamento de dados
* Armazenamento em Parquet
* Consumo de APIs
* Catalogação de dados
* Data Visualization

---

## Pipeline desenvolvido

### 1. Ingestão

Dados provenientes de arquivos CSV e da API do TMDB são ingeridos e armazenados na camada **Raw** do Data Lake no Amazon S3.

### 2. Processamento

Os dados são processados utilizando **AWS Glue e PySpark**, realizando limpeza, transformação, padronização e enriquecimento.

### 3. Trusted Zone

Após o processamento inicial, os dados tratados são armazenados na camada **Trusted**, utilizando formato Parquet.

### 4. Refined Zone

Os dados são transformados novamente para atender às regras de negócio e preparados para consumo analítico.

Nesta etapa foi aplicado um modelo dimensional no formato **Star Schema**, com criação de tabelas fato e dimensão.

### 5. Análise

Os dados refinados são catalogados pelo **AWS Glue Data Catalog**, consultados com **Amazon Athena** e utilizados na construção de dashboards no **Amazon QuickSight**.

---

## Sprints

### Sprint 1

Fundamentos de SQL, modelagem de dados e bancos relacionais.

➡️ [Acessar Sprint 1](./Sprint%201)

### Sprint 2

Python aplicado à manipulação, tratamento e transformação de dados.

➡️ [Acessar Sprint 2](./Sprint%202)

### Sprint 3

Docker, Python, Pandas e preparação de ambientes para processamento de dados.

➡️ [Acessar Sprint 3](./Sprint%203)

### Sprint 4

Primeiros serviços AWS, utilizando S3, Lambda, Athena, boto3 e integração com Python.

➡️ [Acessar Sprint 4](./Sprint%204)

### Sprint 5

Início do projeto de Data Lake, ingestão de dados em S3, integração com a API TMDB e processamento com Spark.

➡️ [Acessar Sprint 5](./Sprint%205)

### Sprint 6

Processamento de dados utilizando AWS Glue e PySpark, Glue Crawlers, Data Catalog e Lake Formation.

➡️ [Acessar Sprint 6](./Sprint%206)

### Sprint 7

Transformação da camada Trusted para Refined, aplicação de regras de negócio, particionamento e modelagem dimensional.

➡️ [Acessar Sprint 7](./Sprint%207)

### Sprint 8

Construção do Star Schema, geração de fatos e dimensões e desenvolvimento de dashboard no Amazon QuickSight.

➡️ [Acessar Sprint 8](./Sprint%208)

---

## Estrutura do Data Lake

```text
Data Lake
│
├── Raw
│   ├── CSV
│   └── TMDB API
│
├── Trusted
│   └── Dados tratados em Parquet
│
└── Refined
    ├── Dimensões
    └── Fatos
```

---

## Autor

**Luis Eduardo Moraes**

Profissional de tecnologia direcionando sua carreira para **Engenharia de Dados e Cloud Computing**, com foco em Python, SQL, PySpark e AWS.

* LinkedIn: luismoraesss
* GitHub: @edumoraees
