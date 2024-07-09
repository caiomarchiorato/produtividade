import matplotlib.pyplot as plt


def plot_prediction(model, y_test, pred_x, scaler):
    plt.scatter(y_test, pred_x, s=5, color='blue', alpha=0.3)
    # plt.title(f'Prediction Plot')  
    # plt.title(f'{scaler}_{model} Prediction Plot')
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='orange', linewidth=1)
    plt.savefig(f'plots/{scaler}_{model}_prediction_plot.png')

def plot_learning_curves(history):
    # Plotar curvas de aprendizado
    plt.figure(figsize=(12, 4))

    # Plotar perda
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='validation')
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plotar métricas (por exemplo, MSE)
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mse'], label='train')
    plt.plot(history.history['val_mse'], label='validation')
    plt.title('MSE')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()

    plt.tight_layout()
    plt.show()