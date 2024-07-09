import joblib
import pandas as pd
import joblib

#custom
from utils.lofo_agent import ImportanceAgent
import os
import joblib
import warnings
import pandas as pd

#custom
from utils.query_execution import create_dataframe_from_query
from utils.dataprep import prepare_data, make_directories, select_types_from_data, normalize_data, convert_date_to_dayofyear
from utils.plot_models import plot_predictio


#carregando dados
data = create_dataframe_from_query("data/queries/novo_c_solo.sql")
data = data[data['ocupacao'] == 'Soja']
data.dropna(inplace=True)

columns_to_drop = ['ocupacao','setor','safra','safra_periodo','ano','dataemergencia','duracao_safra', 'periodo', 'media_velocidade_vento', 'media_direcao_vento', 'media_velocidade_rajada', 'media_direcao_rajada']
categorical_data = ['estadio', 'fazenda', 'talhao', 'textura']
target = 'produtividade'

dates = ['dataemergencia', 'datacolheitainicio', 'dataplantioinicio']
data = convert_date_to_dayofyear(data, dates)

#preparando dados
X, Y = prepare_data(data=data,
                    target=target,
                    drop_columns=columns_to_drop, 
                    categorical_columns= categorical_data)
make_directories()
dense_data, sparse_data = select_types_from_data(X)

dados = pd.merge(X, Y, left_index=True, right_index=True)
print(dados.columns)

modelo_carregado = joblib.load('saves/rf_model.pkl')

lofo_agent = ImportanceAgent(model=modelo_carregado, dataset=dados, scoring='neg_mean_squared_error')
# lofo_agent.plot_importance()

# data_importance = lofo_agent.get_lofo_importance()
data_importance_only_p = lofo_agent.remove_negative_importance()

X_important = X[data_importance_only_p.feature]
print(f'Colunas selecionadas: {X_important.columns}')    

# x_train, x_test, y_train, y_test = split_and_normalize_data(X, Y, test_size=0.2,
#                                                             random_state=42,
#                                                             scaler='standard',
#                                                             sparse_data=sparse_data, dense_data=dense_data)
# x_train.set_index('safra', inplace=True)
# x_test.set_index('safra', inplace=True)

# optimizer = select_model(models[0])
# optimizer.optimize(x_train, y_train)
# pred_x = optimizer.model.predict(x_test)
# best_model = optimizer.model.best_estimator_
# data_atual = date.today().strftime("%d-%m-%Y")

# model_filename = f'saves/{data_atual}/rf_lofo_model.pkl'
# joblib.dump(best_model, model_filename)

# cv_r2_scores = cross_val_score(best_model, x_train, y_train, cv=5, scoring='r2')
# mean_cv_r2 = cv_r2_scores.mean()
# print(f"Mean CV R2: {mean_cv_r2}")
