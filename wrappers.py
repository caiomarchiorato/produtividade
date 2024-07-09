# wrappers.py
from ml_pipeline.data_preparation import DataPreprocessor
from config import Config

def filter_data_wrapper(data, data_prep):
    return data_prep.FilterData(data)

def drop_wrapper(data, columns, target, data_prep):
    return data_prep.Dropper(data, columns, target)

def convert_dates_wrapper(data, dates, data_prep):
    return data_prep.DateConverter(data,dates)

def categorical_encoding_wrapper(data, target, categorical_columns, data_prep):
    return data_prep.CategoricalEncoder(data, target, categorical_columns)

def normalization_wrapper(data, scaler, target_column, data_prep):
    #data without the target column
    dense_data, sparse_data = data_prep.DataTypes(data.drop(columns=[target_column]))
    return data_prep.Normalizer(data, scaler, sparse_data, dense_data, target_column)

def pivot_wrapper(data, pivot_columns, pivot_switch, data_prep):
    return data_prep.Pivoter(data, pivot_columns, Config.index, pivot_switch)
