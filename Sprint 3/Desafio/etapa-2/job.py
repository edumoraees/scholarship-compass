import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# Caminhos (sobrescrevíveis por env no docker-compose)
INPUT = os.getenv("INPUT", "/volume/csv_limpo.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/volume")

plt.rcParams["figure.dpi"] = 140

def carregar_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # normaliza tipos numéricos
    num_cols = [
        "Actual gross",
        "Adjusted gross (in 2022 dollars)",
        "Average gross",
        "Shows",
        "Start year",
        "End year",
        "Rank",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # higieniza espaços nas chaves textuais
    for c in ["Artist", "Tour title"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df

def q1(df: pd.DataFrame):
    """
    Q1 - Qual é a artista que mais aparece nessa lista e possui a maior média de seu faturamento
    bruto (Actual gross)?
    -> Interpretação usada:
       - Primeiro, encontre a ARTISTA que MAIS APARECE (contagem).
       - Reporte a MÉDIA de Actual gross dessa artista.
       - Também registramos, para referência, qual artista tem a MAIOR média geral de Actual gross.
    """
    contagem = df.groupby("Artist").size().sort_values(ascending=False)
    top_artist = contagem.index[0]
    top_count = int(contagem.iloc[0])

    media_da_top = df.loc[df["Artist"] == top_artist, "Actual gross"].mean()

    medias_geral = df.groupby("Artist")["Actual gross"].mean().sort_values(ascending=False)
    artista_maior_media_geral = medias_geral.index[0]
    valor_maior_media_geral = float(medias_geral.iloc[0])

    return {
        "artista_mais_aparece": top_artist,
        "qtd_ocorrencias": top_count,
        "media_actual_gross_dessa_artista": float(media_da_top) if not math.isnan(media_da_top) else None,
        "artista_maior_media_geral": artista_maior_media_geral,
        "valor_maior_media_geral": valor_maior_media_geral,
    }

def q2(df: pd.DataFrame):
    """
    Q2 - Das turnês que aconteceram dentro de um ano (Start year == End year),
         qual a turnê com maior média de faturamento bruto (Average gross)?
    """
    um_ano = df[(df["Start year"].notna()) & (df["End year"].notna())]
    um_ano = um_ano[um_ano["Start year"] == um_ano["End year"]]
    if um_ano.empty:
        return None

    linha = um_ano.sort_values(by="Average gross", ascending=False).iloc[0]
    return {
        "tour": linha["Tour title"],
        "artist": linha["Artist"],
        "ano": int(linha["Start year"]) if pd.notna(linha["Start year"]) else None,
        "avg_gross": float(linha["Average gross"]) if pd.notna(linha["Average gross"]) else None,
    }

def q3(df: pd.DataFrame):
    """
    Q3 - As 3 turnês com show (unitário) mais lucrativo:
         receita_por_show = Adjusted gross (in 2022 dollars) / Shows
    """
    tmp = df.copy()
    tmp = tmp[(tmp["Adjusted gross (in 2022 dollars)"].notna()) & (tmp["Shows"].notna()) & (tmp["Shows"] > 0)]
    tmp["Revenue per show"] = tmp["Adjusted gross (in 2022 dollars)"] / tmp["Shows"]
    top3 = tmp.sort_values(by="Revenue per show", ascending=False).head(3)
    return top3[["Artist", "Tour title", "Revenue per show"]].reset_index(drop=True)

def q4(df: pd.DataFrame, output_png: str):
    """
    Q4 - Para a artista que mais aparece na lista e (em caso de empate) com maior SOMATÓRIO
         de Actual gross, gerar gráfico de linhas do faturamento por ano (Start year).
    """
    contagem = df.groupby("Artist").size()
    max_count = contagem.max()
    candidatas = contagem[contagem == max_count].index

    soma_por_candidata = df[df["Artist"].isin(candidatas)].groupby("Artist")["Actual gross"].sum()
    artista = soma_por_candidata.sort_values(ascending=False).index[0]

    serie = (
        df[df["Artist"] == artista]
        .groupby("Start year")["Actual gross"]
        .sum()
        .dropna()
        .sort_index()
    )

    # gráfico (uma figura, sem subplots, sem estilos customizados)
    plt.figure()
    plt.plot(serie.index.astype(int), serie.values, marker="o")
    plt.title(f"Faturamento bruto por ano (Start year)\nArtista: {artista}")
    plt.xlabel("Ano (Start year)")
    plt.ylabel("Actual gross (soma)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()

    return artista

def q5(df: pd.DataFrame, output_png: str):
    """
    Q5 - Gráfico de colunas dos 5 artistas com MAIOR NÚMERO TOTAL DE SHOWS (soma).
    """
    top = (
        df.groupby("Artist")["Shows"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    plt.figure()
    top.plot(kind="bar")
    plt.title("Top 5 artistas com mais shows (soma de Shows)")
    plt.xlabel("Artista")
    plt.ylabel("Total de Shows")
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()

    return top

def escrever_respostas_txt(path: str, r1: dict, r2: dict | None, r3: pd.DataFrame):
    # Formato pedido no enunciado
    linhas = []
    # Q1
    linhas.append("Q1:")
    linhas.append(
        f"--- Artista que mais aparece: {r1['artista_mais_aparece']} "
        f"({r1['qtd_ocorrencias']} ocorrências). "
        f"Média de Actual gross dessa artista: "
        f"{r1['media_actual_gross_dessa_artista']:.2f}" if r1['media_actual_gross_dessa_artista'] is not None else
        f"--- Artista que mais aparece: {r1['artista_mais_aparece']} "
        f"({r1['qtd_ocorrencias']} ocorrências)."
    )
    linhas.append(
        f"--- Maior média de Actual gross (geral): "
        f"{r1['artista_maior_media_geral']} "
        f"({r1['valor_maior_media_geral']:.2f})"
    )
    linhas.append("")  # linha em branco

    # Q2
    linhas.append("Q2:")
    if r2:
        linhas.append(
            f"--- Turnê de um ano com maior Average gross: "
            f"{r2['tour']} ({r2['artist']}, {r2['ano']}) -> {r2['avg_gross']:.2f}"
        )
    else:
        linhas.append("--- Não há turnês com Start year == End year na base.")
    linhas.append("")

    # Q3
    linhas.append("Q3:")
    linhas.append("--- Top 3 turnês por receita unitária (Adjusted/Shows):")
    for _, row in r3.iterrows():
        linhas.append(f"    - {row['Tour title']} ({row['Artist']}) -> {row['Revenue per show']:.2f}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = carregar_df(INPUT)

    r1 = q1(df)
    r2 = q2(df)
    r3 = q3(df)

    respostas_path = os.path.join(OUTPUT_DIR, "respostas.txt")
    escrever_respostas_txt(respostas_path, r1, r2, r3)

    artista_q4 = q4(df, os.path.join(OUTPUT_DIR, "Q4.png"))
    _ = q5(df, os.path.join(OUTPUT_DIR, "Q5.png"))

    print("[OK] respostas salvas em:", respostas_path)
    print("[OK] gráficos gerados: Q4.png, Q5.png")
    print("[INFO] Artista usado no Q4:", artista_q4)

if __name__ == "__main__":
    main()
