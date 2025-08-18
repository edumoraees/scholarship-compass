select cdpro, nmpro
from tbvendas

where status = 'Concluído' 
	and tbvendas.deletado = '0'
	and date(tbvendas.dtven) between '2014-02-03' AND '2018-02-02'
group by cdpro, nmpro
order by sum(tbvendas.qtd) desc
limit 1;