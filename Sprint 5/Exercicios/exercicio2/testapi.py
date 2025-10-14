from IPython.display import display
import requests
import pandas as pd

api_key = "sua_chave_de_api_aqui"
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR"

response = requests.get(url)
data = response.json()

filmes = []
for movie in data['results']:
    df = {
        'Título': movie['title'],
        'Avaliação': movie['vote_average'],
        'Lançamento': movie['release_date']
    }
    filmes.append(df)

display(pd.DataFrame(filmes))
