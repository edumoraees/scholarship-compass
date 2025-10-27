# 🧩 Desafio – Entrega 3: Processamento da Camada Trusted

## 🎯 Objetivo
O objetivo desta entrega foi praticar a integração dos serviços da AWS estudados nas sprints anteriores, aplicando o uso do **AWS Glue** e **Amazon S3** para transformar e padronizar os dados da **camada Raw** em uma **camada Trusted**, onde os dados ficam limpos, confiáveis e prontos para análise.

---

## 🚀 Etapas Realizadas

### 1️⃣ Criação dos Jobs no AWS Glue
Foram criados **dois jobs Spark** no serviço AWS Glue:
- **`glue_process_csv`** → responsável por processar os dados em formato CSV vindos da camada *Raw/Local*.
- **`glue_process_json`** → responsável por processar os dados em formato JSON vindos da API TMDB.

Os dois jobs foram criados através do **Spark Script Editor**, conforme as boas práticas descritas no desafio.

**Configurações aplicadas nos dois jobs:**
- **Worker type:** G.1X (6 vCPU e 16 GB RAM)  
- **Requested number of workers:** 2  
- **Job timeout:** 60 minutos  

---

## 🧱 Estrutura dos dados no S3

### 🗂️ Entrada (Raw Zone)
Os dados originais estavam organizados conforme o padrão abaixo:

s3://data-lake-luis/Raw/Local/CSV/movies/2025/10/09/movies.csv
s3://data-lake-luis/Raw/Local/CSV/series/2025/10/09/series.csv


### 🗃️ Saída (Trusted Zone)
Após o processamento via AWS Glue, os dados foram transformados em **arquivos Parquet (Snappy)** e salvos na **Trusted Zone**:

s3://data-lake-luis/Trusted/CSV/
s3://data-lake-luis/Trusted/JSON/


---

## ⚙️ Detalhes Técnicos do Processamento

- O job **`glue_process_csv`** converteu os arquivos CSV para o formato **Parquet**, sem necessidade de particionamento (processamento batch).  
- O job **`glue_process_json`** leu os dados brutos do TMDB em formato JSON e gravou na camada Trusted em formato **Parquet particionado por data**, usando o padrão:
/origem_do_dado/formato_do_dado/especificacao_do_dado/data_ingestao/ano/mes/dia/


---

## 📸 Evidências de Execução

### 🔹 Estrutura final da camada Trusted
![Camada Trusted](/Sprint%206/Evidencias/camada_trusted.png)

### 🔹 Job CSV concluído com sucesso
![Job CSV Succeeded](/Sprint%206/Evidencias/glue-succeeded_csv.png)

### 🔹 Job JSON concluído com sucesso
![Job JSON Succeeded](/Sprint%206/Evidencias/glue_succeeded_json.png)

---

## ✅ Conclusão
Com esta entrega, foi concluída a **camada Trusted do Data Lake**, garantindo que:
- Todos os dados foram padronizados em formato Parquet.  
- A estrutura segue o modelo de particionamento definido no desafio.  
- Os datasets estão prontos para serem consultados via **AWS Athena** ou outras ferramentas analíticas.

🎉 **Entrega 3 concluída com sucesso!**
