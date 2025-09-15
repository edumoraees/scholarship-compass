# 📊 Desafio – ETL + Análise de Turnês Musicais

Este relatório documenta a resolução do desafio em **5 etapas**, utilizando a base de dados `concert_tours_by_women.csv` e as bibliotecas `pandas` e `matplotlib`.  
A orquestração foi feita com **Docker** e **docker-compose**.

---

## 1️⃣ ETL – Leitura, limpeza e normalização da base de dados

O script [`etl.py`](etapa-1/etl.py) executa:

```python
import pandas as pd
import re

# leitura robusta do CSV (qualquer separador)
df = pd.read_csv("concert_tours_by_women.csv")

# renomeia "Adjustedgross" -> "Adjusted gross (in 2022 dollars)"
df = df.rename(columns={"Adjustedgross (in 2022 dollars)": "Adjusted gross (in 2022 dollars)"})

# divide "Year(s)" em "Start year" e "End year"
def split_years(s):
    nums = re.findall(r"\d{2,4}", str(s))
    if len(nums) == 1: return int(nums[0]), int(nums[0])
    if len(nums) >= 2: return int(nums[0][-4:]), int(nums[1][-4:])
    return None, None

df[["Start year", "End year"]] = df["Year(s)"].apply(lambda x: pd.Series(split_years(x)))

# limpeza de texto em Artist e Tour title (remove †, [a], emojis etc.)
# conversão de dinheiro para float e anos/shows para int

df.to_csv("csv_limpo.csv", index=False)
```

📂 **Saída**: `csv_limpo.csv` dentro da pasta `Volume/`, já com colunas finais padronizadas:  
`Rank, Actual gross, Adjusted gross (in 2022 dollars), Artist, Tour title, Shows, Average gross, Start year, End year`

---

## 2️⃣ JOB – Análises estatísticas e gráficos

O script [`job.py`](etapa-2/job.py) lê o `csv_limpo.csv` e responde às questões:

### Q1️⃣ Artista que mais aparece + maiores médias
- Identifica a artista com mais ocorrências e calcula sua **média de Actual gross**.  
- Também registra qual artista tem a **maior média geral**.

### Q2️⃣ Turnês em um único ano
- Filtra as turnês com `Start year == End year` e retorna a turnê com maior **Average gross**.

### Q3️⃣ Receita unitária por show
- Calcula **Adjusted gross / Shows** e mostra as **3 turnês mais lucrativas por show**.

### Q4️⃣ Evolução de faturamento
- Para a artista que mais aparece, plota um **gráfico de linhas** com a soma de **Actual gross** por ano (`Start year`).

### Q5️⃣ Artistas com mais shows
- Gera um **gráfico de barras** com os 5 artistas com maior número total de shows.

📂 **Saídas**:
- [csv_limpo.csv](Volume/csv_limpo.csv)  
- [respostas.txt](Volume/respostas.txt)  
- [Q4.png](Volume/Q4.png)  
- [Q5.png](Volume/Q5.png)  

---

## 3️⃣ Orquestração com Docker Compose

O `docker-compose.yml` define dois serviços:  
- **etl** → roda primeiro, gera o `csv_limpo.csv`  
- **job** → roda depois que o `etl` termina com sucesso, produzindo as análises

```yaml
services:
  etl:
    build: ./etapa-1
    volumes:
      - ./Volume:/volume
    environment:
      - INPUT=/volume/concert_tours_by_women.csv
      - OUTPUT_DIR=/volume

  job:
    build: ./etapa-2
    depends_on:
      etl:
        condition: service_completed_successfully
    volumes:
      - ./Volume:/volume
    environment:
      - INPUT=/volume/csv_limpo.csv
      - OUTPUT_DIR=/volume
      - MPLBACKEND=Agg
```

---

## 4️⃣ Passo a passo de execução

1. Clonar/baixar o repositório e entrar na pasta `Desafio`.
2. Colocar o CSV bruto em `Volume/concert_tours_by_women.csv`.
3. Rodar os comandos:

```bash
docker-compose build 
docker-compose up --abort-on-container-exit
```

4. Conferir as saídas na pasta `Volume/`.

---

## 5️⃣ Estrutura final do projeto

```
Desafio/
├─ etapa-1/
│  ├─ Dockerfile
│  ├─ etl.py
├─ etapa-2/
│  ├─ Dockerfile
│  ├─ job.py
├─ Volume/
│  ├─ concert_tours_by_women.csv
│  ├─ csv_limpo.csv
│  ├─ respostas.txt
│  ├─ Q4.png
│  ├─ Q5.png
├─ docker-compose.yml
└─ README.md
```

---

## 6️⃣ Evidências em execução
CSV_limpo após a execução do código ETL.PY
![Docker](/Sprint%203/Evidencias/Desafio/CSVlimpo.png)
Respostas.txt após a execução do código JOB.PY
![Docker](/Sprint%203/Evidencias/Desafio/respostas.txt.png)
Q4png após a execução do código JOB.PY
![Docker](/Sprint%203/Evidencias/Desafio/Q4png.png)
Q5png após a execução do código JOB.PY
![Docker](/Sprint%203/Evidencias/Desafio/Q5png.png)
Arquivo Dockerfile da etapa-1
![Docker](/Sprint%203/Evidencias/Desafio/DockerfileETAPA1.png)
Arquivo Dockerfile da etapa-2
![Docker](/Sprint%203/Evidencias/Desafio/DockerfileETAPA2.png)
Execução do comando para build das etapas1 e 2
![Docker](/Sprint%203/Evidencias/Desafio/DOCKERcomposeBUILD.png)
Execução do comando para rodar o script etl.py e em seguida rodar o script job.py e gerar os arquivos na pasta /Volume
![Docker](/Sprint%203/Evidencias/Desafio/DOCKERcomposeUP.png)

# ✅ Conclusão

Este desafio demonstrou a construção de um pipeline **ETL + análise** totalmente automatizado com Python, Pandas, Matplotlib e Docker, garantindo reprodutibilidade, isolamento e portabilidade dos resultados.
