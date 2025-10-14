
# 🧩 Sprint 5 – Exercícios de Big Data e API

Este repositório contém as evidências e códigos realizados durante os **exercícios práticos da Sprint 5**, envolvendo **Docker, Spark** e **API do TMDB**.

---

## 🚀 Exercício 1 – Contagem de Palavras com Spark e Docker

Neste exercício, o objetivo foi executar um container com o **Jupyter/PySpark**, copiar um arquivo de texto (`README.md`) para dentro do container e contar as palavras utilizando o **Spark Shell**.

### 🧱 Etapas Realizadas

1. Baixei a imagem do container Jupyter com Spark usando o comando:
   ```bash
   docker pull jupyter/pyspark-notebook
   ```

   ![Baixando imagem do container](/Sprint%205/Evidencias/exercicio1/pullJupyterSpark.png)
   *Baixando a imagem do container Jupyter/PySpark*

2. Fiz o download do arquivo README.md que seria usado como base para a contagem de palavras:
   ```bash
   wget https://raw.githubusercontent.com/apache/spark/main/README.md
   ```

   ![Download do README.md](/Sprint%205/Evidencias/exercicio1/wgetReadme.png)
   *Download do arquivo README.md via wget*

3. Copiei o arquivo baixado para dentro do container Spark:
   ```bash
   docker cp README.md <id_do_container>:/home/jovyan/
   ```

   ![Cópia do arquivo para o container](/Sprint%205/Evidencias/exercicio1/dockerCPexec1.png)
   *Arquivo README.md copiado com sucesso para o container*

4. Dentro do container, executei o **Spark Shell** e rodei o código do `exec1.ipynb`, que faz a contagem das palavras no arquivo README.md.  
   Esse código lê o texto, separa as palavras e mostra o total ordenado.

   ![Execução do código Spark](/Sprint%205/Evidencias/exercicio1/exec1.png)
   *Execução do código dentro do Spark Shell*

5. Por fim, obtive o resultado com as palavras ordenadas por contagem, conforme print abaixo:

   ![Resultado ordenado](/Sprint%205/Evidencias/exercicio1/exec1ordenado.png)
   *Resultado final mostrando as palavras ordenadas por contagem*

---

## 🎬 Exercício 2 – Consumo da API TMDB com Python

Neste exercício, utilizei um script Python (`testapi.py`) para fazer a requisição à API pública do **The Movie Database (TMDB)**.  
O objetivo foi buscar filmes com base em um gênero específico e listar os resultados no terminal.

### 🧩 Código Utilizado

```python
import requests

api_key = "SUA_CHAVE_AQUI"
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR&page=1"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    for movie in data["results"][:5]:
        print(movie["title"])
else:
    print("Erro na requisição:", response.status_code)
```

Esse código faz uma chamada HTTP simples para o endpoint `/movie/top_rated` da API do TMDB e exibe os cinco primeiros filmes retornados.

![Execução da API TMDB](/Sprint%205/Evidencias/exercicio2/runAPI.png)
*Evidência da execução bem-sucedida do script Python com retorno dos filmes*

---

## ✅ Resultados Finais

- O **Exercício 1** mostrou a execução do **Spark Shell** dentro de um container Docker, realizando a contagem e ordenação de palavras do arquivo `README.md`.
- O **Exercício 2** fez uma requisição com **Python** e **Requests** à API pública do TMDB, listando os filmes mais bem avaliados com sucesso.

---

📁 Estrutura de Evidências:

```
/Sprint 5/
 └── Evidencias/
      ├── exercicio1/
      │    ├── pullJupyterSpark.png
      │    ├── wgetReadme.png
      │    ├── dockerCPexec1.png
      │    ├── exec1.png
      │    └── exec1ordenado.png
      └── exercicio2/
           └── runAPI.png
```

---
