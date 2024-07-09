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

analytics_index as (
SELECT
    aas.var_name,
    aas.min_value,
    aas.max_value,
    aas.avg_value,
    cast
    	(substring(fi.date, 1,10) as date) as data_img,
    f.name AS talhao,
    far.name AS farm_name
	FROM
	    analytics.anomaly_analysis_summary aas
		JOIN
		    analytics.anomaly_analisys ana ON ana.id = aas.anomaly_analysis_id
		JOIN
		    analytics.fields_images fi ON fi.id = ana.image_id
		JOIN
		    analytics.fields f ON f.id = fi.field_id
		JOIN
		    analytics.farms far ON f.farm_id = far.id
),

analytics_safra_comb_raw_ndvi AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY ti.talhaoid, CAST(ai.data_img AS date) ORDER BY ai.data_img) AS row_num
    FROM talhao_info ti
    JOIN analytics_index ai
        ON ti.talhao = ai.talhao AND ti.fazenda = ai.farm_name
    WHERE ai.var_name = 'ndvi'
      AND ai.data_img <= ti.datacolheitainicio
      AND ai.data_img >= ti.dataplantioinicio

),

analytics_safra_comb_raw_ndre AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY ti.talhaoid, CAST(ai.data_img AS date) ORDER BY ai.data_img) AS row_num
    FROM talhao_info ti
    JOIN analytics_index ai
        ON ti.talhao = ai.talhao AND ti.fazenda = ai.farm_name
    WHERE ai.var_name = 'ndre'
      AND ai.data_img <= ti.datacolheitainicio
      AND ai.data_img >= ti.dataplantioinicio

),

analytics_safra_comb_ndvi AS (
    SELECT acr.fazenda
    	,acr.setor
    	,acr.talhaoid
    	,acr.safra
    	,acr.safra_periodo
    	,acr.cultura
    	,acr.dataemergencia
    	,acr.dataplantioinicio
    	,acr.datacolheitainicio
    	,acr.ano
    	,acr.emergencia_colheita
    	,acr.duracao_safra
    	,acr.var_name
    	,acr.min_value
    	,acr.max_value
    	,acr.avg_value
    	,acr.data_img
    	,acr.farm_name
    FROM analytics_safra_comb_raw_ndvi acr
    	WHERE row_num = 1
),

analytics_safra_comb_ndre AS (
    SELECT acr.fazenda
    	,acr.setor
    	,acr.talhaoid
    	,acr.safra
    	,acr.safra_periodo
    	,acr.cultura
    	,acr.dataemergencia
    	,acr.dataplantioinicio
    	,acr.datacolheitainicio
    	,acr.ano
    	,acr.emergencia_colheita
    	,acr.duracao_safra
    	,acr.var_name
    	,acr.min_value
    	,acr.max_value
    	,acr.avg_value
    	,acr.data_img
    	,acr.farm_name
    FROM analytics_safra_comb_raw_ndre acr
    	WHERE row_num = 1
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

decendios_with_index as (
select
		tmd.fazenda
		,tmd.setor
		,tmd.talhao
		,tmd.talhaoid
	    ,tmd.safra
	    ,tmd.safra_periodo
	    ,tmd.cultura
	    ,tmd.chuva
	    ,tmd.temperatura_media
	    ,tmd.temperatura_min
	    ,tmd.temperatura_max
	    ,tmd.radiacao
	    ,tmd.umidade
	    ,tmd.data_leitura
	    ,tmd.dataemergencia
	    ,tmd.dataplantioinicio
	    ,tmd.datacolheitainicio
	    ,tmd.decendios
	    ,ndvi.avg_value as ndvi_avg
	    ,ndvi.max_value as ndvi_max
	    ,ndvi.min_value as ndvi_min
	    ,ndre.avg_value as ndre_avg
		,ndre.max_value as ndre_max
	    ,ndre.min_value as ndre_min
	    from
		talhao_info_meteorologia_decendios tmd
	full outer join
		analytics_safra_comb_ndvi ndvi on tmd.talhaoid = ndvi.talhaoid
		and tmd.data_leitura = ndvi.data_img
	full outer join
		analytics_safra_comb_ndre ndre on tmd.talhaoid = ndre.talhaoid
		and tmd.data_leitura = ndre.data_img
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
	,avg(cast(tab_decendios.ndvi_avg as DOUBLE)) as ndvi_avg
	,avg(cast(tab_decendios.ndvi_max as DOUBLE)) as ndvi_max
	,avg(cast(tab_decendios.ndvi_min as DOUBLE)) as ndvi_min
	,avg(cast(tab_decendios.ndre_avg as DOUBLE)) as ndre_avg
	,avg(cast(tab_decendios.ndre_max as DOUBLE)) as ndre_max
	,avg(cast(tab_decendios.ndre_min as DOUBLE)) as ndre_min
FROM 
    decendios_with_index tab_decendios
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
		,tab_decendios.ndvi_avg
		,tab_decendios.ndvi_max
		,tab_decendios.ndvi_min
		,tab_decendios.ndre_avg
		,tab_decendios.ndre_max
		,tab_decendios.ndre_min
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
select * from tabela_grouped_by_decendios_produtividade tgp
where cultura = 'Soja'
-- where ndvi_avg is not null