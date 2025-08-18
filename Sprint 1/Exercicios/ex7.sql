SELECT
    autor.nome
from autor
left join livro ON livro.autor = autor.codautor
where livro.cod is null
order by autor.nome 
