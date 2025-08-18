SELECT
    tbvendedor.nmvdd as vendedor,
    coalesce(sum(tbvendas.qtd * tbvendas.vrunt), 0) as valor_total_vendas,
    round(
        coalesce(sum(tbvendas.qtd * tbvendas.vrunt), 0) * (tbvendedor.perccomissao / 100.0),
        2
    ) AS comissao
from tbvendedor
left join tbvendas
  on tbvendas.cdvdd = tbvendedor.cdvdd
 and tbvendas.status = 'Concluído'
group by
    tbvendedor.cdvdd, tbvendedor.nmvdd, tbvendedor.perccomissao
order by comissao DESC;
