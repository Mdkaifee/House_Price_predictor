import pandas as pd

def select_features(df, threshold=0.1):
    # Simple example: select features correlated with price
    corr = df.corr()
    rel_features = corr['price'][abs(corr['price']) > threshold].index.tolist()
    rel_features.remove('price')
    return rel_features
