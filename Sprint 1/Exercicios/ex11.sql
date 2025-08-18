select
    tbvendas.cdcli,
    tbvendas.nmcli,
    sum(tbvendas.qtd * tbvendas.vrunt) as gasto
from tbvendas
where lower(tbvendas.status) = 'concluído'
group by tbvendas.cdcli, tbvendas.nmcli
order by gasto desc
limit 1