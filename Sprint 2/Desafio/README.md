
# 📊 Desafio – Análise Google Play Store

Este relatório documenta a resolução das 8 etapas do desafio utilizando a base de dados **googleplaystore.csv**, com as bibliotecas `pandas` e `matplotlib`.

---

## 1️⃣ Remover linhas duplicadas

```python
# Remove linhas duplicadas e informa quantas foram eliminadas
antes = len(df)
df = df.drop_duplicates()
depois = len(df)
print(f'Removidas {antes - depois} linhas duplicadas. Total atual: {depois}.')
```

---

## 2️⃣ Top 5 apps por instalações (desempate por Reviews)


```python
# Agrupa por app e pega o maior valor de Installs e de Reviews por app
top_installs = (
    df[['App', 'Installs', 'Reviews']]
    .dropna(subset=['App', 'Installs'])
    .groupby('App', as_index=False)
    .agg({'Installs': 'max', 'Reviews': 'max'})
    .sort_values(['Installs', 'Reviews'], ascending=[False, False])
    .head(5)
)

display(top_installs)

plt.figure()
plt.bar(top_installs['App'], top_installs['Installs'])
plt.title('Top 5 Apps por Instalações (desempate por Reviews)')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Instalações')
plt.tight_layout()
plt.show()
```

---

## 3️⃣ Frequência de **APLICATIVOS únicos** por categoria


```python
# Conta quantos APPS únicos existem em cada categoria
freq_cat_apps = (
    df[['App', 'Category']]
    .dropna(subset=['App', 'Category'])
    .drop_duplicates(subset=['App'])
    .groupby('Category')['App']
    .nunique()
    .sort_values(ascending=False)
)

# Exibe tabela e gráficos
display(freq_cat_apps.head(10).rename('qtd_apps'))

plt.figure()
freq_cat_apps.head(10).plot(kind='pie', autopct='%1.1f%%')
plt.title('Top 10 Categorias por Nº de APPS únicos')
plt.ylabel('')
plt.tight_layout()
plt.show()

plt.figure()
freq_cat_apps.head(10).plot(kind='bar')
plt.title('Top 10 Categorias por Nº de APPS únicos')
plt.xlabel('Categoria')
plt.ylabel('Qtd de apps')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

---

## 4️⃣ App mais caro

```python
# Filtra preços válidos, encontra o maior e lista os apps nesse valor
nonfree = df.dropna(subset=['Price'])
nonfree = nonfree[nonfree['Price'] >= 0]

preco_max = nonfree['Price'].max()
apps_mais_caros = (
    nonfree[nonfree['Price'] == preco_max][['App', 'Price', 'Category', 'Rating', 'Reviews']]
    .drop_duplicates()
)

print(f'Preço máximo encontrado: ${preco_max}')
display(apps_mais_caros)
```

---

## 5️⃣ Quantidade de apps classificados como "Mature 17+"

```python
# Conta quantos apps possuem Content Rating igual a 'Mature 17+'
total_mature = (df['Content Rating'] == 'Mature 17+').sum()
print('Total de apps Mature 17+:', int(total_mature))
```

---

## 6️⃣ Top 10 apps por número de reviews

```python
# Ordena por Reviews desc, remove duplicatas e pega os 10 primeiros
top_reviews = (
    df[['App', 'Reviews']]
    .dropna(subset=['App', 'Reviews'])
    .sort_values('Reviews', ascending=False)
    .drop_duplicates(subset=['App'])
    .head(10)
)

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

## 7️⃣ Cálculos extras

### 7.1) Top 5 categorias por média de Rating (mín. 50 apps)

```python
cat_avg = (
    df[['Category', 'Rating']]
    .dropna(subset=['Category', 'Rating'])
    .groupby('Category')
    .agg(qtd=('Rating', 'count'), media_rating=('Rating', 'mean'))
    .query('qtd >= 50')
    .sort_values('media_rating', ascending=False)
    .head(5)
)

display(cat_avg)
```

### 7.2) Porcentagem de apps gratuitos

```python
base_type = len(df.dropna(subset=['Type']))
pct_free = (df['Type'].astype(str).str.lower() == 'free').sum() / base_type * 100 if base_type else 0
print(f'Porcentagem de apps gratuitos: {pct_free:.2f}% (base: {base_type} registros válidos)')
```

---

## 8️⃣ Gráficos extras

### 8.1) Histograma da distribuição de Ratings

```python
plt.figure()
df['Rating'].dropna().plot(kind='hist', bins=20)
plt.title('Distribuição de Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()
```

### 8.2) Dispersão – Reviews vs Rating (amostra)

```python
amostra = df[['Reviews', 'Rating']].dropna()
if len(amostra) > 3000:
    amostra = amostra.sample(n=3000, random_state=42)

plt.figure()
plt.scatter(amostra['Reviews'], amostra['Rating'], s=10, alpha=0.5)
plt.title('Reviews vs Rating (amostra)')
plt.xlabel('Reviews')
plt.ylabel('Rating')
plt.tight_layout()
plt.show()
```

---

# 🐍 Código completo em `jupyter`
[desafio.ipynb](desafio.ipynb)