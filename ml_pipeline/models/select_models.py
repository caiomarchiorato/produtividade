from ml_pipeline.models.optimizers_models.ridge import RidgeOptimizer
from ml_pipeline.models.optimizers_models.lasso import LassoOptimizer
from ml_pipeline.models.optimizers_models.svr import SVROptimizer
from ml_pipeline.models.optimizers_models.random_forest import RandomForestOptimizer
from ml_pipeline.models.optimizers_models.gradient_boosting import GradientBoostingOptimizer 
from ml_pipeline.models.optimizers_models.xgboost import XGBoostOptimizer
from ml_pipeline.models.optimizers_models.mlpregressor import MLPRegressorOptimizer
from ml_pipeline.models.optimizers_models.knn import KNNOptimizer

@staticmethod
def select_model(model_name):
    if model_name == 'ridge':
        ridge_model = RidgeOptimizer(
            param_space = {
                'alpha': (0.1, 10.0, 'log-uniform')
            }
        )
        return ridge_model
    elif model_name == 'lasso':
        lasso_model = LassoOptimizer(
            param_space = {
                'alpha': (0.1, 10.0, 'log-uniform')
            }
        )
        return lasso_model
    elif model_name == 'svr':
        svr_model = SVROptimizer(
            param_space = {
                'C': (1e-6, 1e+6, 'log-uniform'),
                'gamma': (1e-6, 1e+1, 'log-uniform'),
                'epsilon': (1e-6, 1e+1, 'log-uniform')
            }
        )
        return svr_model
    elif model_name == 'rf':
        rf_model = RandomForestOptimizer(
            param_space = {
                'criterion': ['squared_error', 'absolute_error'],
                'n_estimators': (10, 1000),
                'max_depth': (1, 100),
                'max_leaf_nodes': (10, 1000),
                'max_features': (0.1, 1.0, 'uniform'),
                'min_samples_split': (2, 10),
                'min_samples_leaf': (1, 10),
                'bootstrap': [True, False]
            }
        )
        
        return rf_model
    elif model_name == 'gbr':
        gbr_model = GradientBoostingOptimizer(
            param_space = {
                'n_estimators': (10, 1000),
                'max_depth': (1, 10)
                }
        )
        return gbr_model
    elif model_name == 'xgboost':
        xgboost_model = XGBoostOptimizer(
            param_space = {
                'n_estimators': (10, 1000),
                'max_depth': (1, 100),
                'learning_rate': (0.01, 1.0),
                'min_child_weight': (1, 10),  
                'gamma': (0.0, 1.0),           
                'subsample': (0.1, 1.0),      
                'colsample_bytree': (0.1, 1.0),
                'reg_alpha': (0.0, 10.0),      
            }
        )
        return xgboost_model
    elif model_name == 'mlp':
        mlp_model = MLPRegressorOptimizer(
            param_space = {
                'activation': ['relu', 'tanh', 'logistic'],
                'alpha': (1e-6, 1e+1, 'log-uniform')
                }
        )
        return mlp_model
    elif model_name == 'knn':
        knn_model = KNNOptimizer(
            param_space = {
                'n_neighbors': (1, 100),
                'weights': ['uniform', 'distance']}
        )
        return knn_model
    else:
        raise ValueError(f"Modelo {model_name} não implementado")