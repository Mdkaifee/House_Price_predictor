import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(csv_path):
    df = pd.read_csv(csv_path)
    print(df.columns.tolist())  # Add this line to debug columns!
    df = df.rename(columns={
        'Location': 'region',
        'BHK': 'BHK',
        'Area(in sqft)': 'area',
        'SalePrice(in Crores)': 'price'
    })
    features = ['region', 'BHK', 'area']
    target = 'price'
    df = df[features + [target]].dropna()
    df['BHK'] = pd.to_numeric(df['BHK'], errors='coerce')
    df['area'] = pd.to_numeric(df['area'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna()
    df['price'] = df['price'] * 1e7
    le = LabelEncoder()
    df['region'] = le.fit_transform(df['region'])
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, le
