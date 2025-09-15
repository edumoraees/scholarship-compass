import os, re, unicodedata
import pandas as pd

INPUT = os.getenv("INPUT", "/volume/concert_tours_by_women.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/volume")
OUTPUT = os.path.join(OUTPUT_DIR, "csv_limpo.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ordem final das colunas
FINAL_COLS = [
    "Rank",
    "Actual gross",
    "Adjusted gross (in 2022 dollars)",
    "Artist",
    "Tour title",
    "Shows",
    "Average gross",
    "Start year",
    "End year",
]

# ------------------ Funções utilitárias ------------------

def read_csv_any(path: str) -> pd.DataFrame:
    for sep in [",", ";", "\t", "|"]:
        try:
            df = pd.read_csv(path, sep=sep, engine="python")
            if df.shape[1] >= 5:
                return df
        except Exception:
            pass
    return pd.read_csv(path)

def money_to_float(s):
    if pd.isna(s): return None
    s = str(s).strip()
    if s == "" or s.lower() in {"nan","null","none"}: return None
    s = re.sub(r"[^\d,.\-]", "", s)
    if s.count(",") == 1 and s.count(".") > 1:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(",") > 1 and s.count(".") == 0:
        s = s.replace(",", "")
    elif s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    else:
        if s.count(".") > 1: s = s.replace(".", "")
        if s.count(",") > 1: s = s.replace(",", "")
    try:
        return float(s)
    except Exception:
        return None

def split_years(series: pd.Series):
    starts, ends = [], []
    for v in series.astype(str):
        s = v.strip()
        if s == "" or s.lower() in {"nan","null","none"}:
            starts.append(None); ends.append(None); continue
        nums = re.findall(r"(\d{2,4})", s)
        if not nums:
            starts.append(None); ends.append(None); continue
        if len(nums) == 1:
            y1 = int(nums[0][-4:])
            starts.append(y1); ends.append(y1)
        else:
            y1 = int(nums[0][-4:])
            y2raw = nums[1]
            if len(y2raw) == 2:  # 2014-15 -> 2015
                y2 = int(str(y1)[:2] + y2raw)
            else:
                y2 = int(y2raw[-4:])
            starts.append(y1); ends.append(y2)
    return pd.Series(starts), pd.Series(ends)

# ------------------ Limpeza de texto ------------------

def remove_control(s: str) -> str:
    return re.sub(r"[\x00-\x1F\x7F]", "", s)

def clean_footnotes(s: str) -> str:
    s = re.sub(r"\[[^\]]*\]", "", s)  # [a], [1], etc.
    s = re.sub(r"\([^)]*nota[^)]*\)", "", s, flags=re.I)
    s = re.sub(r"[†‡※＊✝✞✟✠✚✛✜✝️+]+", "", s)  # símbolos comuns
    s = re.sub(r"[\u00B9\u00B2\u00B3\u2070-\u209F]", "", s)  # super/subscripts
    return s

def clean_symbols(s: str) -> str:
    return re.sub(r"[^0-9A-Za-zÀ-ÖØ-öø-ÿ ,\.\'&\(\)\-:!/\/]", "", s)

def clean_text(s) -> str:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    s = str(s)
    s = remove_control(s)
    s = clean_footnotes(s)
    s = clean_symbols(s)
    s = re.sub(r"\s{2,}", " ", s).strip(" ,")
    return s

# ------------------ Pipeline principal ------------------

def main():
    df = read_csv_any(INPUT)

    # renomeia 'Adjustedgross (in 2022 dollars)' -> alvo correto
    for c in df.columns:
        if c.strip().lower() == "adjustedgross (in 2022 dollars)":
            df = df.rename(columns={c: "Adjusted gross (in 2022 dollars)"})
            break

    # quebra Year(s) -> Start/End
    if "Year(s)" in df.columns and ("Start year" not in df.columns or "End year" not in df.columns):
        start_s, end_s = split_years(df["Year(s)"])
        df["Start year"] = start_s
        df["End year"] = end_s

    # mantém apenas as colunas necessárias
    keep = {c: c for c in FINAL_COLS if c in df.columns}
    df = df.rename(columns=keep)

    missing = [c for c in FINAL_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes após normalização: {missing}\nCabeçalhos: {list(df.columns)}")

    df = df[FINAL_COLS].copy()

    # tipos
    for c in ["Actual gross", "Adjusted gross (in 2022 dollars)", "Average gross"]:
        df[c] = df[c].apply(money_to_float)

    for c in ["Rank", "Shows", "Start year", "End year"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    for c in ["Artist", "Tour title"]:
        df[c] = df[c].apply(clean_text)

    # ordena por Rank
    df = df.sort_values(by=["Rank"])

    # saída: garante .1f nos valores monetários
    money_cols = ["Actual gross", "Adjusted gross (in 2022 dollars)", "Average gross"]
    df_out = df.copy()
    for c in money_cols:
        df_out[c] = df_out[c].map(lambda x: f"{x:.1f}" if pd.notna(x) else "")

    for c in ["Rank", "Shows", "Start year", "End year"]:
        df_out[c] = df_out[c].astype("Int64")

    df_out.to_csv(OUTPUT, index=False)
    print(f"[OK] csv_limpo salvo em: {OUTPUT}")

if __name__ == "__main__":
    main()
