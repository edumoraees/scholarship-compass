from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, rand, when, floor
from pyspark.sql.types import IntegerType

# 1️⃣ Criar sessão Spark
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .getOrCreate()

# 2️⃣ Ler o arquivo texto (um nome por linha)
df_nomes = spark.read.text("nomes_aleatorios.txt")

# 3️⃣ Renomear a coluna
df_nomes = df_nomes.withColumnRenamed("value", "Nomes")

print("📄 Primeiros registros:")
df_nomes.show(10)

# 4️⃣ Adicionar coluna Escolaridade
df_nomes = df_nomes.withColumn(
    "Escolaridade",
    when((rand() < 0.33), lit("Fundamental"))
    .when((rand() < 0.66), lit("Medio"))
    .otherwise(lit("Superior"))
)

# 5️⃣ Adicionar coluna Pais (13 países da América do Sul)
paises = [
    "Brasil", "Argentina", "Chile", "Uruguai", "Paraguai",
    "Peru", "Colômbia", "Venezuela", "Equador", "Bolívia",
    "Guiana", "Suriname", "Guiana Francesa"
]
df_nomes = df_nomes.withColumn(
    "Pais",
    when((rand() * 13).cast(IntegerType()) == 0, lit(paises[0]))
)
for i in range(1, len(paises)):
    df_nomes = df_nomes.withColumn(
        "Pais",
        when(col("Pais").isNull() & ((rand() * 13).cast(IntegerType()) == i), lit(paises[i])).otherwise(col("Pais"))
    )
df_nomes = df_nomes.na.fill(paises[0])  # fallback

# 6️⃣ Adicionar coluna AnoNascimento (entre 1945 e 2010)
df_nomes = df_nomes.withColumn("AnoNascimento", (floor(rand() * (2010 - 1945 + 1)) + 1945))

print("✅ DataFrame com colunas adicionadas:")
df_nomes.show(10)

# 7️⃣ Selecionar pessoas nascidas neste século (>= 2000)
df_select = df_nomes.filter(col("AnoNascimento") >= 2000)
print("🧒 Pessoas nascidas neste século:")
df_select.show(10)

# 8️⃣ Registrar tabela temporária
df_nomes.createOrReplaceTempView("pessoas")

# 9️⃣ Consultas com Spark SQL
print("📊 Pessoas nascidas neste século (via SQL):")
spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000").show(10)

# 10️⃣ Contar Millennials (1980–1994)
print("📈 Contagem de Millennials:")
spark.sql("""
SELECT COUNT(*) AS Qtde_Millennials
FROM pessoas
WHERE AnoNascimento BETWEEN 1980 AND 1994
""").show()

# 🔟 Contar pessoas por país e geração
print("🌍 Pessoas por país e geração:")
spark.sql("""
SELECT
  Pais,
  CASE
    WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
    WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
    WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
    WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
  END AS Geracao,
  COUNT(*) AS Quantidade
FROM pessoas
GROUP BY Pais, Geracao
ORDER BY Pais, Geracao, Quantidade
""").show(50)

spark.stop()
