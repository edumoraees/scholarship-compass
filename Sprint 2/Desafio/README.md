
# 📊 Desafio – Análise Google Play Store

Este relatório documenta a resolução das 8 etapas do desafio utilizando a base de dados **googleplaystore.csv**, com as bibliotecas `pandas` e `matplotlib`.

---

## 1️⃣ Importação das bibliotecas, leitura da base de dados e tratamento da base de dados.

```python
import pandas as pd             
import matplotlib.pyplot as plt            

# 1) Ler CSV
dataset = pd.read_csv('googleplaystore.csv')  # lê o arquivo CSV e carrega no DataFrame "dataset"

# 2) Reviews -> numérico
dataset['Reviews'] = pd.to_numeric(dataset['Reviews'], errors='coerce')  
# converte a coluna "Reviews" para número; se não conseguir, coloca NaN

# 3) App em minúsculas (normaliza) e remove espaços extras
dataset['App'] = dataset['App'].astype(str).str.lower().str.strip()  
# transforma os nomes dos apps em string, deixa em minúsculo e tira espaços

# 4) Remover duplicatas mantendo o maior Reviews por app
dataset = (dataset.sort_values('Reviews', ascending=False)  
                  .drop_duplicates(subset=['App'], keep='first'))  
# ordena pelo número de reviews (maior primeiro) e remove duplicados, mantendo só 1 por app

# 5) Installs -> inteiro ANULÁVEL (aceita NA)
#    - remove tudo que não for dígito; '' vira NA; converte para Int64 (pandas nullable int)
dataset['Installs'] = (dataset['Installs'].astype(str)  
                       .str.replace(r'[^0-9]', '', regex=True)  
                       .replace('', pd.NA)  
                       .astype('Int64'))  
# limpa a coluna Installs, deixa só números, converte vazio em NA e transforma em inteiro

# 6) Price -> float (robusto)
#    - remove '$', vírgulas etc; '' vira NA; converte para float anulável
dataset['Price'] = (dataset['Price'].astype(str)  
                    .str.replace(r'[^0-9.\-]', '', regex=True)  
                    .replace('', pd.NA)  
                    .astype('Float64'))  
# limpa a coluna Price, deixa só números e ponto, converte vazio em NA e em float

if 'Type' in dataset.columns:  
    dataset.loc[(dataset['Type'].astype(str).str.lower() == 'free') &  
                (dataset['Price'].isna()), 'Price'] = 0.0  
# se o app é "free" mas não tem preço informado, define o preço como 0.0

# 7) Category: troca '_' por espaço e tira espaços extras
dataset['Category'] = (dataset['Category'].astype(str)  
                       .str.replace('_', ' ', regex=False)  
                       .str.strip())  
# ajusta a coluna Category, substituindo "_" por espaço e limpando espaços

display(dataset.head())  # mostra as primeiras linhas do DataFrame
```

---

## 2️⃣ Top 5 apps por instalações (desempate por Reviews)


```python
top_installs = dataset.sort_values(['Installs','Reviews'], ascending=False, inplace=False).head(5)
# ordena apps por número de instalações e depois reviews (desempate), pega os 5 primeiros

fig, ax = plt.subplots(figsize=(6, 8))
fig, ax = plt.subplots(figsize=(6, 8))
ax.set_facecolor("#FFFFFF")  

plt.bar(top_installs['App'], top_installs['Installs'], color="#1F22CF")
plt.xlabel('Aplicativos', fontsize=12)
plt.ylabel('Instalações (Bilhões)', fontsize=12)
plt.title('Top 5 Aplicativos Mais Instalados na Google Play Store\n Obs.: Critério de desempate adotado foi por numeros de reviews', fontsize=16)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()

plt.show()
```

---

## 3️⃣ Frequência de **APLICATIVOS únicos** por categoria


```python
frequency_apps_by_category = dataset['Category'].value_counts()
# conta quantos apps existem em cada categoria

explode = []
for count in frequency_apps_by_category:
    if count > 300:
        explode.append(0.01)
    elif count > 50:
        explode.append(0.2)
    else:
        explode.append(0.6)
# cria lista que define o afastamento (explode) das fatias no gráfico de pizza dependendo da quantidade

plt.figure(figsize=(16, 12))
plt.pie(
    frequency_apps_by_category,
    explode=explode,
    labels=frequency_apps_by_category.index,
    labeldistance= 1.07,
    autopct='%1.1f%%',
    pctdistance=0.94,
    startangle=27,
)
plt.title('Frequência de Aplicativos por Categoria',fontsize=16)
plt.axis('equal')

plt.legend( frequency_apps_by_category.index, title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.show()
```

---

## 4️⃣ App mais caro

```python
app_mais_caro = dataset.loc[dataset['Price'].idxmax()]
# pega o app com maior valor na coluna Price

texto = (
    f"App mais caro\n\n"
    f"App: {app_mais_caro['App']}\n"
    f"Categoria: {app_mais_caro['Category']}\n"
    f"Preço: ${app_mais_caro['Price']:.2f}"
)
# monta um texto descritivo com informações do app mais caro

display(app_mais_caro)
# mostra os dados completos desse app

```

---

## 5️⃣ Quantidade de apps classificados como "Mature 17+"

```python
total_mature = (dataset['Content Rating'] == 'Mature 17+').sum()
# cria série booleana para verificar se Content Rating é “Mature 17+” e soma os True

print('Total de apps Mature 17+:', int(total_mature))
# imprime o resultado
```

---

## 6️⃣ Top 10 apps por número de reviews

```python
top_reviews = (
    dataset[['App', 'Reviews']]
    .dropna(subset=['App', 'Reviews'])
    .sort_values('Reviews', ascending=False)
    .drop_duplicates(subset=['App'])
    .head(10)
)
# seleciona apps e reviews, remove valores nulos, ordena pelos reviews,
# elimina duplicados e pega os 10 primeiros (apps mais avaliados)
display(top_reviews)
plt.figure()
plt.bar(top_reviews['App'], top_reviews['Reviews'])
plt.title('Top 10 Apps por Reviews')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Reviews')
plt.tight_layout()
plt.show()
```
---
## 7️⃣  Top 5 apps pagos por reviews 

```python
paid_apps = dataset.loc[dataset['Type'] == 'Free']
# Está filtrando "Free" em vez de "Paid"

top_5_apps_paid = paid_apps.sort_values(['Reviews'], ascending=False, inplace=False).head(5)
# ordena pelos reviews em ordem decrescente e pega os 5 primeiros

top_5_apps_paid = top_5_apps_paid[['App', 'Reviews', 'Category']].reset_index(drop=True)
# seleciona apenas App, Reviews e Category, e reseta o índice

ranking = [f"{i}°" for i in range(1, 6)]
# cria lista com posições 1° a 5°

top_5_apps_paid.insert(0, 'Ranking', ranking)
# adiciona a coluna Ranking no DataFrame

display(top_5_apps_paid)
# mostra a tabela final
```
---
## 8️⃣  Melhor app pago (rating + installs)
```python
best_rated_and_viewed_apps = paid_apps.sort_values(['Rating', 'Installs'], ascending=False, inplace=False)
# ordena apps pagos pelo Rating e depois pelas Installs (ambos descrescente)

best_rated_and_viewed_apps = best_rated_and_viewed_apps[['App', 'Installs', 'Rating']].reset_index(drop=True).head(1)
# seleciona colunas App, Installs, Rating, reseta índice e pega só o melhor

texto = (
    f"App: {best_rated_and_viewed_apps['App'][0]}\n"
    f"Installs: {best_rated_and_viewed_apps['Installs'][0]}\n"
    f"Rating: {best_rated_and_viewed_apps['Rating'][0]}"
)
# monta texto com informações do melhor app pago
```python

--- 

## 9️⃣  Gráficos extras

### 8.1) Histograma da distribuição de Ratings

```python
# Pega a coluna type e faz a contagem e mostra em gráfico a distribuição de apps pagos e gratuitos
dataset['Type']  = dataset['Type'].astype(str).str.lower().str.strip()
dataset['Price'] = pd.to_numeric(dataset['Price'], errors='coerce')
paid = dataset[(dataset['Type'] == 'paid') & (dataset['Price'].notna()) & (dataset['Price'] > 0)]
plt.figure()
plt.hist(paid['Price'], bins=30)
plt.title('Distribuição de Preços — Apps Pagos')
plt.xlabel('Preço (US$)')
plt.ylabel('Quantidade de apps')
plt.tight_layout()
plt.show()
```

### 🔟 Distribuição de Apps: Gratuitos vs Pago

```python
# Pega a coluna type e faz a contagem e mostra em gráfico a distribuição de apps pagos e gratuitos
tipo_series = (dataset['Type'].astype(str)
               .str.lower()
               .map({'free': 'Gratuito', 'paid': 'Pago'}))  
dist_tipo = tipo_series.value_counts(dropna=True)
plt.figure()
dist_tipo.plot(kind='pie', autopct='%1.1f%%')

plt.title('Distribuição de Apps: Gratuito vs Pago')
plt.ylabel('')
plt.tight_layout()
plt.show()
```

---

# 🐍 Código completo em `jupyter`
[desafio.ipynb](desafio.ipynb)