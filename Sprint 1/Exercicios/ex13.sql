select
    tbvendas.cdpro,
    tbvendas.nmcanalvendas,
    tbvendas.nmpro,
    sum(tbvendas.qtd) as quantidade_vendas
from tbvendas
where lower(tbvendas.status) = 'concluído'
  and lower(tbvendas.nmcanalvendas) in ('ecommerce','matriz')
group by tbvendas.cdpro, tbvendas.nmcanalvendas, tbvendas.nmpro
order by quantidade_vendas asc, tbvendas.nmpro asc
limit 10