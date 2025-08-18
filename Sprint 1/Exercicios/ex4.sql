SELECT
    autor.nome,
    autor.codautor,
    autor.nascimento,
    COUNT(livro.cod) AS quantidade
FROM autor
LEFT JOIN livro ON livro.autor = autor.codautor
GROUP BY autor.nome, autor.codautor, autor.nascimento
ORDER BY
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
    LOWER(autor.nome),
'Á','a'), 'à','a'), 'â','a'), 'ã','a'), 'ä','a'),
'é','e'), 'è','e'), 'ê','e'), 'ë','e'),
'í','i'), 'ì','i'), 'î','i'), 'ï','i'),
'ó','o'), 'ò','o'), 'ô','o'), 'õ','o'), 'ö','o'),
'ú','u'), 'ù','u'), 'û','u'), 'ü','u'),
'ç','c')
