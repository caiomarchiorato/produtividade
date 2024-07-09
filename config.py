class Config:
    pivot_switch = True

    columns = [
    'fazenda',
    'talhao',
    'talhaoid',
    'safra',
    # 'textura',
    'dataplantioinicio',
    'semana_plantio',
    'datacolheitainicio',
    'estadio',
    #'emergencia_colheita',
    'produtividade',
    #'numero_estadio',
    'graus_dias',
    'soma_graus_dias_acumulado',
    'graus_dias_score',
    'soma_chuva',
    'score_semanal',
    #'dias_para_soma',
    'media_temperatura',
    'media_radiacao_solar',
    'media_umidade',
    # 'herbicidas',
    # 'inseticidas',
    # 'fungicidas'
    ]

    combinacoes_3 = [['r1-r2', 'r2-r3', 'r3', 'r3-r4', 'r3-r4-2', 'r4', 'r4-r5', 'r5',
        'r5-r6', 'r6', 'r6-2', 'r6-r7', 'v0', 'v1', 'v2-v3', 'v4-v5'],
    # ['r1-r2', 'r3-r4', 'r4-r5'],
    # ['r1-r2', 'r3-r4', 'r5'],
    # ['r1-r2', 'r3-r4', 'r5-r6'],
    # ['r1-r2', 'r3-r4-2', 'r4-r5'],
    # ['r1-r2', 'r3-r4-2', 'r5'],
    # ['r1-r2', 'r3-r4-2', 'r5-r6'],
    # ['r1-r2', 'r4', 'r4-r5'],
    # ['r1-r2', 'r4', 'r5'],
    # ['r1-r2', 'r4', 'r5-r6'],
    # ['r2-r3', 'r3-r4', 'r4-r5'],
    # ['r2-r3', 'r3-r4', 'r5'],
    # ['r2-r3', 'r3-r4', 'r5-r6'],
    # ['r2-r3', 'r3-r4-2', 'r4-r5'],
    # ['r2-r3', 'r3-r4-2', 'r5'],
    # ['r2-r3', 'r3-r4-2', 'r5-r6'],
    # ['r2-r3', 'r4', 'r4-r5'],
    # ['r2-r3', 'r4', 'r5'],
    # ['r2-r3', 'r4', 'r5-r6'],
    # ['r3', 'r3-r4', 'r4-r5'],
    # ['r3', 'r3-r4', 'r5'],
    # ['r3', 'r3-r4', 'r5-r6'],
    # ['r3', 'r3-r4-2', 'r4-r5'],
    # ['r3', 'r3-r4-2', 'r5'],
    # ['r3', 'r3-r4-2', 'r5-r6'],
    # ['r3', 'r4', 'r4-r5'],
    # ['r3', 'r4', 'r5'],
    # ['r3', 'r4', 'r5-r6']
    ]
    
    from itertools import combinations
    lista = ['r1-r2', 'r2-r3', 'r3', 'r3-r4', 'r3-r4-2', 'r4', 'r4-r5', 'r5', 'r5-r6', 'r6', 'r6-2', 'r6-r7']
    combinacoes_4 = list(combinations(lista, 4))
    combinacoes_4 = [list(comb) for comb in combinacoes_4]
    
    categorical_data = ['safra']
    date_columns = ['datacolheitainicio', 'dataplantioinicio']
    pivot_columns = ['graus_dias_score', 'media_umidade']
    target = 'produtividade'
    columns_to_drop = []
    #columns_to_drop = ['soma_chuva_score','chuva_esperada','graus_dias_esperado','ocupacao','setor', 'safra_periodo','ano','dataemergencia','duracao_safra', 'periodo']
    models = ['rf'
            #   ,'xgboost', 'gbr'
            ]
    scaler = 'standard'

    index = ['fazenda', 'talhao', 'talhaoid', 'safra', 
                                'dataplantioinicio', 'semana_plantio', 'datacolheitainicio', 'produtividade']