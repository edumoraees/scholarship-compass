select tbvendedor.cdvdd, tbvendedor.nmvdd
from tbvendas
inner join tbvendedor on tbvendedor.cdvdd = tbvendas.cdvdd
where tbvendas.status = 'Concluído'
group by tbvendedor.cdvdd, tbvendedor.nmvdd 
order by count(*) desc
limit 1