import pandas as pd

def predict_price(model, input_dict):
    X = pd.DataFrame([input_dict])
    pred = model.predict(X)
    return pred[0]
