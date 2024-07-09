import keras
import tensorflow as tf

class NeuralNetworkRegressor:
    def __init__(self):
        self.model = None
        
    def build_model(self, input_shape):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(64, activation='relu', input_shape=input_shape))
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        optimizer = tf.keras.optimizers.RMSprop(0.001)
        
        model.compile(optimizer=optimizer, 
                            loss='mean_squared_error',
                            metrics=['mae', 'mse', tf.keras.metrics.RootMeanSquaredError(name='rmse')])
        
        return model

    def train(self, X_train, y_train, epochs=50, batch_size=32, verbose=1):
            self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)