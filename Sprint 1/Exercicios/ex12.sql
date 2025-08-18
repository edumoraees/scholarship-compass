with vendedor_min as (
  select
    tbvendas.cdvdd,
    sum(tbvendas.qtd * tbvendas.vrunt) as valor_total_vendas
  from tbvendas
  where tbvendas.status = 'Concluído'
  group by tbvendas.cdvdd
  having sum(tbvendas.qtd * tbvendas.vrunt) > 0
  order by valor_total_vendas asc
  limit 1
)
select
  tbdependente.cddep,
  tbdependente.nmdep,
  tbdependente.dtnasc,
  vendedor_min.valor_total_vendas
from tbdependente
join vendedor_min on vendedor_min.cdvdd = tbdependente.cdvdd
order by tbdependente.nmdep 