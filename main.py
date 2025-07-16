from src.data_preprocessing import load_and_preprocess_data
from src.train_model import train_and_save_model, load_model, evaluate_model
from src.predict import predict_price

def main():
    X_train, X_test, y_train, y_test, le = load_and_preprocess_data('data/house_price.csv')
    train_and_save_model(X_train, y_train, model_path='model.pkl')
    model = load_model('model.pkl')
    acc = evaluate_model(model, X_test, y_test)
    print(f"Model R2 Score on Test Set: {acc:.3f}")

    print("\n--- Predict House Price ---")
    regions = list(le.classes_)
    print(f"Regions: {', '.join(regions)}")

    # Robust region input handling
    while True:
        region = input("Enter region (choose from above): ")
        if region not in regions:
            print("Sorry, the region/city you entered is NOT in the dataset. Please choose exactly from the above list.")
        else:
            region_encoded = le.transform([region])[0]
            break

    BHK = int(input("Enter BHK (number of bedrooms): "))
    area = float(input("Enter area (sq ft): "))

    input_dict = {
        'region': region_encoded,
        'BHK': BHK,
        'area': area
    }

    price = predict_price(model, input_dict)
    print(f"\nPredicted Sale Price: ₹{price:,.2f}")
    print("Kaha s layega itna paisa? 😄,Chal dafa ho")

if __name__ == "__main__":
    main()
