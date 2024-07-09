from datetime import date
import mlflow
import mlflow.sklearn
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from ml_pipeline.models import select_models
from ml_pipeline.model_evaluation import ModelEvaluation


class ModelTraining:
    def __init__(self, models, scalers):
        self.model = None
        self.model_name = models
        self.scaler = scalers[0]

    def split_data(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_models(self, X_train, X_test, y_train, y_test, X_valid, y_valid, n_features_select=None,R_Feature_Selection=False):
        use_optimization = True
        run_name = f"estimativa_produtividade_{date.today().strftime('%d-%m-%Y')}_{self.model_name}_{self.scaler}"
        with mlflow.start_run(run_name=run_name):
                mlflow.log_param("model", self.model_name)
                mlflow.log_param("scaler", self.scaler)

                actual_model = None
                #print(X_train.columns)
                print(f"Training {self.model_name} model!!!")
                if use_optimization:
                    optimizer = select_models.select_model(self.model_name)
                    optimizer.optimize(X_train, y_train)
                    if R_Feature_Selection == False:
                        actual_model = optimizer.model
                    else:
                        best_estimator = optimizer.model.best_estimator_
                        rfe = RFE(best_estimator, n_features_to_select=n_features_select, step=1)
                        rfe.fit(X_train, y_train)
                        rfe_columns = X_train.columns[rfe.support_]
                        actual_model = rfe.estimator_
                        #printando hiper parâmetros de actual_model
                        print(actual_model.get_params())
                        X_test = X_test[rfe_columns]
                        print(rfe_columns)
                else:
                    if R_Feature_Selection == False:
                        basic_model = select_models.select_model(self.model_name)
                        basic_model.train(X_train, y_train)                        
                        actual_model = basic_model.model
                    else:
                        #usando basic models
                        basic_model = select_models.select_model(self.model_name)
                        basic_model.train(X_train, y_train)
                        
                        #incorporando rfe
                        rfe = RFE(basic_model.model, n_features_to_select=n_features_select, step=1)
                        rfe.fit(X_train, y_train)
                        rfe_columns = X_train.columns[rfe.support_]
                        actual_model = rfe.estimator_
                        print(actual_model.get_params())

                        X_test = X_test[rfe_columns]
                        print(rfe_columns)

                evaluator = ModelEvaluation(actual_model, self.model_name)
                rmse, r2, mae = evaluator.evaluate(X_test, y_test)

                # evaluator.evaluate_on_validation(X_valid, y_valid)
                evaluator.save_model()
                # self.model = actual_model
                return optimizer, actual_model, rmse, r2, mae

    def save_model(self):
        for model_name, model in self.models.items():
            mlflow.sklearn.log_model(model, model_name)

    def log_metrics(self):
        for model_name, model in self.models.items():
            mlflow.log_metric(f'{model_name}_mse', mean_squared_error(Y_test, model.predict(X_test_normalized)))

    def evaluate(self, X_test, Y_test):
        for model_name, model in self.models.items():
            predictions = model.predict(X_test)
            mse = mean_squared_error(Y_test, predictions)
            print(f'{model_name} MSE: {mse}')

    def evaluate_on_validation(self, X_validation, Y_validation):
        for model_name, model in self.models.items():
            predictions = model.predict(X_validation)
            mse = mean_squared_error(Y_validation, predictions)
            print(f'{model_name} MSE on validation: {mse}')

    def load_model(self, model_name):
        model = mlflow.sklearn.load_model(model_name)
        return model

    def predict(self, model_name, data):
        model = self.models[model_name]
        return model.predict(data)
