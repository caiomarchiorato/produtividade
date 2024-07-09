with talhao_info as(
	select f.nome as fazenda
		,fs.nome as setor
		,t.codigo as talhao
		,t.talhaoid
		,s.nome as safra
		,sp.nome as safra_periodo
		,oc.nome as cultura
		,cast(t.dataemergencia as date) as dataemergencia
		,cast(t.dataplantioinicio as date) as dataplantioinicio
		,cast(t.datacolheitainicio  as date) as datacolheitainicio
		,year(cast(t.dataemergencia  as date)) as ano
		,date_diff('day', cast(t.dataemergencia  as date), cast(t.datacolheitainicio  as date)) as emergencia_colheita
		,date_diff('day', cast(t.dataplantioinicio as date), cast(t.datacolheitainicio  as date)) as duracao_safra
		from agrosig_novo_latest.talhao as t
		left join agrosig_novo_latest.safraperiodo as sp
		on t.safraperiodoid = sp.safraperiodoid 
			left join agrosig_novo_latest.safra as s
		on sp.safraid = s.safraid 
			left join agrosig_novo_latest.ocupacao as oc
		on oc.ocupacaoid = sp.ocupacaoid
			left join agrosig_novo_latest.fazendatalhao as ft
		on t.fazendatalhaoid = ft.fazendatalhaoid
			left join agrosig_novo_latest.fazendasetor as fs
		on fs.fazendasetorid = t.fazendasetorid
			left join agrosig_novo_latest.fazenda as f
		on f.fazendaid = fs.fazendaid 
		where 1=1
			and t.dataplantioinicio is not null 
			and t.datacolheitainicio is not null
			and cast(t.dataplantioinicio as date) >= DATE('2019-01-01')
			and t.codigo <> '99999'
			and regexp_like(sp.nome, 'Safra')
			and sp.nome not like '%Experimentos%'
		
),

meteorologia_diario as (
	select *
		,cast(mtd.data as date) as data_leitura 
		from cleansed.meteorologia_talhao_diaria as mtd
),

talhao_info_meteorologia_decendios as (
	select md.fazenda
		,md.setor
		,md.talhao
		,md.talhaoid
		,md.safra
		,md.safra_periodo
		,md.cultura
		,md.chuva_soma as chuva
		,md.temperatura_media
		,md.temperatura_min
		,md.temperatura_max
		,md.radiacao_solar_media as radiacao
		,md.umidade_media as umidade
		,md.data_leitura
		,ti.dataemergencia
		,ti.dataplantioinicio
		,ti.datacolheitainicio
		,1 + FLOOR((ROW_NUMBER() OVER (PARTITION BY md.talhaoid ORDER BY md.data_leitura) - 1) / 10) AS decendios
	
		from meteorologia_diario md
			inner join talhao_info ti
				on ti.talhaoid = md.talhaoid
		where 1=1
			and (
		        ti.cultura = 'Soja' 
		        and ti.duracao_safra > 80 
		        and ti.duracao_safra < 135
		    )
		    or (
		        ti.cultura = 'Algodão' 
		        and ti.duracao_safra > 140 
		        and ti.duracao_safra < 200
		    )
		    and (ti.duracao_safra - ti.emergencia_colheita) < 10 
			and md.data_leitura>=ti.dataplantioinicio
			and md.data_leitura<=ti.datacolheitainicio
		order by md.talhaoid
			,md.data_leitura
),

tabela_grouped_by_decendios as (   	
SELECT tab_decendios.fazenda
	,tab_decendios.setor
	,tab_decendios.talhao
	,tab_decendios.talhaoid
	,tab_decendios.safra
	,tab_decendios.safra_periodo
	,tab_decendios.cultura
	,tab_decendios.decendios
	,case
		when tab_decendios.cultura = 'Soja' 
			then ((sum(tab_decendios.temperatura_max) + sum(tab_decendios.temperatura_min))/2) -14*count(tab_decendios.decendios)
		else
			((sum(tab_decendios.temperatura_max) + sum(tab_decendios.temperatura_min))/2) -15*count(tab_decendios.decendios)
	end as graus_dias
	,sum(tab_decendios.chuva - 0.20*tab_decendios.temperatura_media) as defict_hidrico
	,sum(tab_decendios.chuva) as chuva
	,sum(tab_decendios.radiacao) as radiacao
	,avg(tab_decendios.umidade) as umidade
	,count(tab_decendios.decendios) as numero_de_dias_agregados
FROM 
    talhao_info_meteorologia_decendios tab_decendios
	group by
		tab_decendios.talhaoid
		,tab_decendios.decendios
		,tab_decendios.fazenda
		,tab_decendios.setor
		,tab_decendios.talhao
		,tab_decendios.safra
		,tab_decendios.safra_periodo
		,tab_decendios.cultura
	order by tab_decendios.talhaoid
		,tab_decendios.decendios
),
tabela_grouped_by_decendios_produtividade as (
	select 
		tab_decendios.fazenda
		,tab_decendios.setor
		,tab_decendios.talhao
		,tab_decendios.talhaoid
		,tab_decendios.safra
		,tab_decendios.safra_periodo
		,tab_decendios.cultura
		,split_part(tab_decendios.safra_periodo, ' Safra', 1) as tecnologia
		,am.variedade 
		,tab_decendios.decendios
		,tab_decendios.graus_dias
		,tab_decendios.defict_hidrico
		,tab_decendios.chuva
		,tab_decendios.radiacao
		,tab_decendios.umidade
		,tab_decendios.numero_de_dias_agregados
		,am.produtividade
		,am.texturasolo
	from tabela_grouped_by_decendios tab_decendios
	inner join cleansed.ambiente_manejo am
		on am.talhaoid = tab_decendios.talhaoid
	where 1=1
		and (
			tab_decendios.cultura = 'Soja'
			and am.produtividade >=30 
			and am.produtividade<=120
		)
		or (
			tab_decendios.cultura = 'Algodão'
			and am.produtividade >=150 
			and am.produtividade<=400
		)
)

select * from talhao_info_meteorologia_decendios