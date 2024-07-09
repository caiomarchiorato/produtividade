import warnings
import pandas as pd
import os
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from ml_pipeline.data_preparation import DataPreprocessor
from ml_pipeline.model_training import ModelTraining
from config import Config
from utils.query_execution import load_create_data
from wrappers import (
    filter_data_wrapper,
    drop_wrapper,
    convert_dates_wrapper,
    categorical_encoding_wrapper,
    normalization_wrapper,
    pivot_wrapper
)

def main():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    st.title("ML Pipeline Application")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your data CSV file", type=["csv"])
    
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # Display the uploaded data
        st.write("Uploaded Data")
        st.write(data.head())

        # Select columns from the uploaded data
        selected_columns = st.multiselect("Select columns to use", options=data.columns, default=Config.columns)
        
        if selected_columns:
            data = data[selected_columns]

            data_prep = DataPreprocessor(data)
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

            X_processed = preprocessing_pipeline.fit_transform(train_set)
            X, y, hot_encoder, label_encoder = X_processed[0], X_processed[1], X_processed[2], X_processed[3]

            #X_valid_processed = preprocessing_pipeline.transform(validation_set)
            #X_valid, y_valid, encoder_valid, label_encoder_valid = X_valid_processed[0], X_valid_processed[1], X_valid_processed[2], X_valid_processed[3]
            
            st.write("Processed Training Data")
            st.write(X.sample(5))
            st.write("Processed Validation Data")
            #st.write(X_valid.sample(5))

            mTraining = ModelTraining(Config.models, Config.scaler)

            X_train, X_test, y_train, y_test = mTraining.split_data(X, y)

            mTraining.train_models(X_train, X_test, y_train, y_test, X_valid, y_valid)

            st.success("Model training completed")

if __name__ == '__main__':
    main()
