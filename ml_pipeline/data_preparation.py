import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder

#create a wrapper to print the output of each function
def print_output(func):
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        print(output)
        return output
    return wrapper

class DataPreprocessor:
    def __init__(self, data):
        self.data = data
        self.hot_encoder = None
        self.ordinal_encoder = None

    def SplitData(self):
        train = self.data
        validation = self.data
        return train, validation
    
    def Dropper(self, data, columns, target):

        data = data[data[target] > 0].dropna(subset=target)

        q1 = data[target].quantile(0.25)
        q3 = data[target].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5*iqr
        limite_superior = q3 + 1.5*iqr

        data = data[(data[target] > limite_inferior) & (data[target] < limite_superior)]

        if columns:
            return data.drop(columns, axis=1)
        else:
            return data

    
    def FilterData(self, data):
        return data[(data['produtividade'] >= 35) & (data['produtividade'] <= 85)]

    def TrainTest(self, data, target, test_size):
        X = data.drop(columns=[target], axis=1)
        Y = data[target]
        return X, Y
    
    def DateConverter(self, data, dates):
        for date in dates:
            data[date] = pd.to_datetime(data[date])
            data[date] = data[date].dt.dayofyear
        return data

    def DataTypes(self, data):
        dense_data = data.select_dtypes(include=['float64', 'int64', 'float32']).columns
        sparse_data = [col for col in data.columns if col not in dense_data]
        bool_columns = data.select_dtypes(include=bool).columns
        data[bool_columns] = data[bool_columns].astype(int)
        return dense_data, sparse_data

    def Normalizer(self, data, scaler, sparse_data, dense_data, target_column):
        X = data.drop(columns=[target_column], axis=1)
        y = data[target_column]

        X_sparse = X[sparse_data]
        X_dense = X[dense_data]

        if scaler == 'standard':
            scalers = StandardScaler()
        elif scaler == 'minmax':
            scalers = MinMaxScaler()
        elif scaler == 'robust':
            scalers = RobustScaler()
        else:
            raise ValueError(f"Scaler {scaler} not recognized. Use 'standard', 'minmax', or 'robust'.")

        X_dense_normalized = pd.DataFrame(scalers.fit_transform(X_dense), columns=X_dense.columns, index=X_dense.index)

        X_normalized = pd.concat([X_dense_normalized, X_sparse], axis=1)
        X_normalized[target_column] = y

        return X_normalized

    def Pivoter(self, data, pivot_columns, index, pivot_switch):
        if pivot_switch:
            df_pivoted = data.pivot_table(index=index, 
                                    columns='estadio', 
                                    values=pivot_columns).reset_index()

            df_pivoted.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in df_pivoted.columns.values]

            data = df_pivoted.copy()
            #dropna with subset of all columns with 'graus_dias_score' in the name
            data.dropna(subset=[col for col in data.columns if 'graus_dias_score' in col], inplace=True)
            data.drop(columns=['fazenda', 'talhao'], inplace=True)
        else:
            data = data.dropna()
        return data

    def CategoricalEncoder(self, data, target, categorical_columns):
        X = data.drop([target], axis=1)
        Y = data[target]
        encoders = {}

        to_be_one_hot_encoded = []
        to_be_label_encoded = []
        for column in categorical_columns:
            if len(data[column].unique()) <= 10:
                to_be_one_hot_encoded.append(column)
            else:
                to_be_label_encoded.append(column)

        if not self.hot_encoder:
            print('Creating a new hot encoder for this set')
            encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=bool)
            encoded_array = encoder.fit_transform(X[to_be_one_hot_encoded])
            self.hot_encoder = encoder
        else:
            print('Using existing hot encoder for this set')
            encoder = self.hot_encoder
            encoded_array = encoder.transform(X[to_be_one_hot_encoded])

        encoded_columns = []
        for col, categories in zip(to_be_one_hot_encoded, encoder.categories_):
            encoded_columns.extend([f"{col}_{category}" for category in categories])

        encoded = pd.DataFrame(encoded_array, columns=encoded_columns, index=X.index)
        numeric_X = X.drop(columns=to_be_one_hot_encoded, axis=1)
        new_X = pd.concat([numeric_X, encoded], axis=1)

        if not self.ordinal_encoder:
            print('Creating new ordinal encoder for this set')
            ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
            encoded_array = ordinal_encoder.fit_transform(new_X[to_be_label_encoded])
            self.ordinal_encoder = ordinal_encoder
        else:
            print('Using existing ordinal encoder for this set')
            ordinal_encoder = self.ordinal_encoder
            encoded_array = ordinal_encoder.transform(new_X[to_be_label_encoded])

        encoded_columns = pd.DataFrame(encoded_array, columns=to_be_label_encoded, index=new_X.index)
        
        new_X.drop(columns=to_be_label_encoded, inplace=True)
        new_X = new_X.join(encoded_columns)
        encoders['ordinal'] = ordinal_encoder

        X = new_X
        X.set_index('talhaoid', inplace=True)
        return X, Y, encoder, ordinal_encoder

    def lag_variable(self, data, columns, lag):
        data_lagged = data.copy()
        for column in columns:
            data_lagged[f'{column}_lag_{lag}'] = data_lagged.shift(lag)[column]
            data_lagged.dropna(inplace=True)
        return data_lagged

class DirectoryManager:
    @staticmethod
    def make_directories():
        for directory in ['saves', 'plots', 'results']:
            if not os.path.exists(directory):
                os.makedirs(directory)

