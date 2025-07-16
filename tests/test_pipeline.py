import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_preprocessing import load_and_preprocess_data
from src.train_model import train_and_save_model, load_model, evaluate_model

def test_training_and_evaluation():
    X_train, X_test, y_train, y_test, le = load_and_preprocess_data('data/house_price.csv')
    train_and_save_model(X_train, y_train, model_path='test_model.pkl')
    model = load_model('test_model.pkl')
    score = evaluate_model(model, X_test, y_test)
    print(f"Test Model R2 Score: {score:.3f}")
    assert score > 0, "Model should have R2 score > 0"

if __name__ == "__main__":
    test_training_and_evaluation()
