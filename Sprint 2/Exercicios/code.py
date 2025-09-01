# -*- coding: utf-8 -*-
from pathlib import Path

BASE = Path(__file__).parent
CSV  = BASE / "actors.csv"
OUT  = BASE


def parse_csv_line(s: str):
    out, field, q, i = [], [], False, 0
    while i < len(s):
        c = s[i]
        if c == '"':
            # trata aspas duplas dentro de campo: "" -> "
            if q and i + 1 < len(s) and s[i+1] == '"':
                field.append('"'); i += 1
            else:
                q = not q
        elif c == ',' and not q:
            out.append(''.join(field)); field = []
        elif c not in '\r\n':
            field.append(c)
        i += 1
    out.append(''.join(field))
    return out

def to_float(x: str) -> float:
    x = x.strip().replace('$', '').replace(',', '')
    return float(x) if x else 0.0

def to_int(x: str) -> int:
    d = ''.join(ch for ch in x if ch.isdigit() or ch == '-')
    return int(d) if d else 0

# --- leitura (tenta utf-8-sig, cai p/ latin-1 se preciso) ----------
try:
    txt = CSV.read_text(encoding="utf-8-sig")
except UnicodeDecodeError:
    txt = CSV.read_text(encoding="latin-1")

lines = txt.splitlines()
if not lines:
    raise SystemExit("Arquivo vazio.")

# cabeçalho e índices esperados
hdr = parse_csv_line(lines[0])
# ['Actor','Total Gross','Number of Movies','Average per Movie','#1 Movie','Gross']
idx = {name: hdr.index(name) for name in
       ['Actor','Total Gross','Number of Movies','Average per Movie','#1 Movie','Gross']}

# --- acumuladores para as 5 etapas --------------------------------
max_movies = (-1, "")      # (qtd, ator)
sum_gross, n_gross = 0.0, 0  # média da coluna 'Gross' (Etapa 2)
max_avg    = (-1.0, "")    # (média, ator)
movie_count = {}           # {filme: contagem}
total_gross_by_actor = {}  # {ator: total_gross}

for line in lines[1:]:
    if not line.strip():
        continue
    row = parse_csv_line(line)
    # segurança: pula linhas quebradas
    if len(row) < 6: 
        continue

    actor            = row[idx['Actor']]
    total_gross      = to_float(row[idx['Total Gross']])
    number_of_movies = to_int  (row[idx['Number of Movies']])
    avg_per_movie    = to_float(row[idx['Average per Movie']])
    top_movie        = row[idx['#1 Movie']].strip()
    gross            = to_float(row[idx['Gross']])

    # Etapa 1: ator com mais filmes
    if number_of_movies > max_movies[0]:
        max_movies = (number_of_movies, actor)

    # Etapa 2: média da coluna Gross (dos “principais filmes”)
    sum_gross += gross
    n_gross   += 1

    # Etapa 3: ator com maior Average per Movie
    if avg_per_movie > max_avg[0]:
        max_avg = (avg_per_movie, actor)

    # Etapa 4: contagem do #1 Movie
    movie_count[top_movie] = movie_count.get(top_movie, 0) + 1

    # Etapa 5: ordenar atores por Total Gross
    total_gross_by_actor[actor] = total_gross

# ordenações finais
movies_sorted = sorted(movie_count.items(), key=lambda x: (-x[1], x[0]))
actors_sorted = sorted(total_gross_by_actor.items(), key=lambda x: -x[1])


OUT.joinpath("Etapa-1.txt").write_text(
    f"O ator com o maior número de filmes é {max_movies[1]} com {max_movies[0]} filmes.\n",
    encoding="utf-8"
)

OUT.joinpath("Etapa-2.txt").write_text(
    f"A média de receita de bilheteria bruta (Gross) foi de: {sum_gross/n_gross:.2f}\n",
    encoding="utf-8"
)

OUT.joinpath("Etapa-3.txt").write_text(
    f"O ator com a maior média por filme é {max_avg[1]} com uma média de {max_avg[0]:.2f}.\n",
    encoding="utf-8"
)

OUT.joinpath("Etapa-4.txt").write_text(
    "\n".join(f"{i}° - O filme {m} aparece {c} vez(es) no dataset"
              for i,(m,c) in enumerate(movies_sorted, start=1)) + "\n",
    encoding="utf-8"
)

OUT.joinpath("Etapa-5.txt").write_text(
    "\n".join(f"{a} - {g:.2f}" for a,g in actors_sorted) + "\n",
    encoding="utf-8"
)

print("Arquivos Etapa-1 a Etapa-5 gerados na mesma pasta do script.")
