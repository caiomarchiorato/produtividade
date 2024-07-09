import warnings
import pandas as pd
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from ml_pipeline.data_preparation import DataPreprocessor
from ml_pipeline.model_training import ModelTraining
from config import Config
import joblib
from utils.query_execution import load_create_data
from collections import defaultdict
from wrappers import (
    filter_data_wrapper,
    drop_wrapper,
    convert_dates_wrapper,
    categorical_encoding_wrapper,
    normalization_wrapper,
    pivot_wrapper
)

periodos_estadios = Config.combinacoes_3
# n_variaveis = [5,6,7,8,9,10,11,12]

def main():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    # query_name = '23_05_2024'
    # data = load_create_data(query_name)
    data = pd.read_csv('data/csv/23_05_2024.csv')

#metricas para cada periodo e cada modelo
    metrics = defaultdict(lambda: defaultdict(dict))
    for periodos in periodos_estadios:
    #use config.columns to filter the data
        data = data[Config.columns]
        data_filtered = data[data['estadio'].isin(periodos)]

        data_prep = DataPreprocessor(data_filtered)

        train_set, validation_set = data_prep.SplitData()

        if not Config.pivot_switch:
            Config.categorical_data.append('estadio')

        hot_encoder, label_encoder = None, None 
        preprocessing_pipeline = Pipeline(steps=[
            ('filter_produtividade', FunctionTransformer(filter_data_wrapper,           kw_args={'data_prep': data_prep})),
            ('dropper',              FunctionTransformer(drop_wrapper,                  kw_args={'columns': Config.columns_to_drop, 'target': Config.target, 'data_prep': data_prep})),
            ('convert_dates',        FunctionTransformer(convert_dates_wrapper,         kw_args={'dates': Config.date_columns, 'data_prep': data_prep})),
            ('pivot',                FunctionTransformer(pivot_wrapper,                 kw_args={'pivot_columns': Config.pivot_columns, 'pivot_switch': Config.pivot_switch, 'data_prep': data_prep})),
            ('normalization',        FunctionTransformer(normalization_wrapper,         kw_args={'scaler': Config.scaler,'target_column': Config.target, 'data_prep': data_prep})),
            ('categorical_encoding', FunctionTransformer(categorical_encoding_wrapper,  kw_args={'target': Config.target, 'categorical_columns': Config.categorical_data, 'data_prep': data_prep })),
        ], verbose=False)

        print("Preprocessing data...")
        X_processed = preprocessing_pipeline.fit_transform(train_set)
        X, y, _, _ = X_processed[0], X_processed[1], X_processed[2], X_processed[3]

        X_valid_processed = preprocessing_pipeline.transform(validation_set)
        X_valid, y_valid, _, _ = X_valid_processed[0], X_valid_processed[1], X_valid_processed[2], X_valid_processed[3]
        for model in Config.models:
            print(f"Training model {model} features and {periodos} periods")
            mTraining = ModelTraining(model, Config.scaler)
            X_train, X_test, y_train, y_test = mTraining.split_data(X, y)

            rmse, r2, mae = mTraining.train_models(X_train, X_test, y_train, y_test, X_valid, y_valid, n_features_select=None, R_Feature_Selection=False)
            metrics[model][str(periodos)] = {'rmse': rmse, 'r2': r2, 'mae': mae}
            
            save_path = f'saves/{model}/{str(periodos)}]'
            if not os.path.exists(save_path):
                os.makedirs(f'saves/{model}/{str(periodos)}]')
            joblib.dump(mTraining.model, f'{save_path}/model.pkl')
                
    metrics_df = pd.DataFrame([{**{'model': model, 'periodos': periodos}, **metrics[model][str(periodos)]}
                                for model in metrics for periodos in metrics[model]])
    metrics_df.to_csv('saves/metrics.csv', index=False)
    
if __name__ == '__main__':
    main()
