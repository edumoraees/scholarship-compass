select count(cod) as quantidade, nome, estado, cidade
from livro
inner join editora on editora.codeditora = livro.editora
inner join endereco on endereco.codendereco = editora.endereco
group by nome, estado, cidade
order by quantidade desc
LIMIT 5