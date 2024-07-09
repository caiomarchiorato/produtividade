from sklearn.metrics import root_mean_squared_error, mean_squared_error, r2_score, mean_absolute_error
import mlflow

class ModelEvaluation:
    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        # Resultados dos testes
        print(20*"-")
        print("# Test Results #")
        print(f"📏 RMSE: {rmse:.2f}")
        print(f"📊 R2 Score: {r2:.2f}")
        # print(f"💡 MAE: {mae:.2f}")
        # print(f"🧮 MSE: {mse:.2f}")

        # if rmse < 2:
        #     # Smile face
        #     print("  😊 Great Job! 😊  ")
        #     print("  _________")
        #     print(" /         \\")
        #     print("|   O   O   |")
        #     print("|     >     |")
        #     print("|    '-'    |")
        #     print(" \\_________/")
        # else:
        #     # Sad face
        #     print("  😞 Keep Trying 😞  ")
        #     print("  _________")
        #     print(" /         \\")
        #     print("|   X   X   |")
        #     print("|     v     |")
        #     print("|    ---    |")
        #     print(" \\_________/")

        self.log_metrics(rmse, r2, mae)
        return rmse, r2, mae


    def evaluate_on_validation(self, X_validation, Y_validation):
        y_pred = self.model.predict(X_validation)
        mse = mean_squared_error(Y_validation, y_pred)
        rmse = root_mean_squared_error(Y_validation, y_pred)
        r2 = r2_score(Y_validation, y_pred)
        mae = mean_absolute_error(Y_validation, y_pred)
        
        # Resultados da validação
        print("✨ Validation Results ✨")
        print(f"📏 RMSE: {rmse:.2f}")
        print(f"📊 R2 Score: {r2:.2f}")
        # print(f"💡 MAE: {mae:.2f}")
        # print(f"🧮 MSE: {mse:.2f}")
        
        # if rmse < 2:
        #     # Smile face
        #     print("  😊 Excellent! 😊  ")
        #     print("  _________")
        #     print(" /         \\")
        #     print("|   O   O   |")
        #     print("|     >     |")
        #     print("|    '-'    |")
        #     print(" \\_________/")
        # else:
        #     # Sad face
        #     print("  😞 Needs Improvement 😞  ")
        #     print("  _________")
        #     print(" /         \\")
        #     print("|   X   X   |")
        #     print("|     v     |")
        #     print("|    ---    |")
        #     print(" \\_________/")

        return mse, rmse, r2, mae


    def save_model(self):
        mlflow.sklearn.log_model(self.model, self.model_name)

    def log_metrics(self, rmse, r2, mae):
        mlflow.log_metric(f'{self.model_name}_rmse', rmse)
        mlflow.log_metric(f'{self.model_name}_r2', r2)
        mlflow.log_metric(f'{self.model_name}_mae', mae)