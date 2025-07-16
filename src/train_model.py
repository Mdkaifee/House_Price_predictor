from sklearn.linear_model import LinearRegression
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
def train_and_save_model(X_train, y_train, model_path='model.pkl'):
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def load_model(model_path='model.pkl'):
    return joblib.load(model_path)

def evaluate_model(model, X_test, y_test):
    score = model.score(X_test, y_test)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"R2 Score: {score:.3f}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    return score
