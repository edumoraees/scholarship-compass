select distinct autor.nome
from autor
inner join livro on livro.autor = autor.codautor
inner join editora on editora.codeditora = livro.editora
join endereco on endereco.codendereco = editora.endereco
where not(
	UPPER(endereco.pais) = 'BRASIL'
	AND UPPER(endereco.estado) IN ('PARANÁ', 'SANTA CATARINA', 'RIO GRANDE DO SUL')
)
order by autor.nome asc