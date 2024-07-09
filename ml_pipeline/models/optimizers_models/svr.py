from sklearn.svm import SVR
from skopt import BayesSearchCV
from sklearn.metrics import mean_squared_error

class SVROptimizer:
    def __init__(self, param_space=None, n_iter=50, cv=3, random_state=42):
        self.param_space = param_space
        self.n_iter = n_iter
        self.cv = cv
        self.random_state = random_state
        self.model = None
#just train a simple model
    def train(self, X_train, y_train, **kwargs):
        self.model = SVR(**kwargs)
        self.model.fit(X_train, y_train)

    def optimize(self, X_train, y_train):
        self.model = BayesSearchCV(
            SVR(),
            self.param_space,
            n_iter = self.n_iter,
            cv = self.cv,
            random_state = self.random_state,
            n_jobs= -1
        )
        
        self.model.fit(X_train, y_train)
        
    def predict(self, X_test):
        if self.model is None:
            raise ValueError("O modelo ainda não foi treinado")
        return self.model.predict(X_test)
    
    def evaluate(self, X_test, y_test):
        if self.model is None:
            raise ValueError("O modelo ainda não foi treinado")
        y_pred = self.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"MSE: {mse}")
        return mse