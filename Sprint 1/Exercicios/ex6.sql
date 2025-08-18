SELECT
    autor.codautor,
    autor.nome,
    count(livro.cod) as quantidade_publicacoes
from autor
inner join livro ON livro.autor = autor.codautor
group by autor.codautor, autor.nome
order by quantidade_publicacoes DESC
limit 1