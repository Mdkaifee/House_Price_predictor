from src.data_preprocessing import load_and_preprocess_data
from src.train_model import train_and_save_model, load_model, evaluate_model
from src.predict import predict_price
import difflib

def get_valid_input(user_input, options):
    """Return exact or closest match from options (case-insensitive)."""
    user_input_clean = user_input.strip().lower()
    options_lower = [opt.lower() for opt in options]
    if user_input_clean in options_lower:
        return options[options_lower.index(user_input_clean)]
    # Suggest the closest match (minimum similarity 0.7)
    close = difflib.get_close_matches(user_input_clean, options_lower, n=1, cutoff=0.7)
    if close:
        suggestion = options[options_lower.index(close[0])]
        print(f"Did you mean: {suggestion}?")
        return suggestion
    return None

def main():
    X_train, X_test, y_train, y_test, le = load_and_preprocess_data('data/house_price.csv')
    train_and_save_model(X_train, y_train, model_path='model.pkl')
    model = load_model('model.pkl')
    acc = evaluate_model(model, X_test, y_test)
    print(f"Model R2 Score on Test Set: {acc:.3f}")

    import pandas as pd
    df = pd.read_csv('data/house_price.csv')
    # Get mapping of state to cities
    state_city_map = {}
    for s, group in df.groupby('state'):
        state_city_map[s] = sorted(group['Location'].unique().tolist())

    # --- State selection ---
    all_states = sorted(list(state_city_map.keys()))
    print("\nStates:", ', '.join(all_states))
    while True:
        state_input = input("Enter state (choose from above): ")
        state = get_valid_input(state_input, all_states)
        if not state:
            print("Sorry, state not in dataset. Please choose from above.")
        else:
            break

    # --- City selection ---
    cities = state_city_map[state]
    print("\nCities in", state + ":", ', '.join(cities))
    while True:
        city_input = input("Enter city (choose from above): ")
        city = get_valid_input(city_input, cities)
        if not city:
            print("Sorry, city not in selected state. Please choose from above.")
        else:
            break

    # Get the encoded value for city/region
    regions = list(le.classes_)
    if city not in regions:
        print("City not in model. Please restart and choose a valid city.")
        return
    region_encoded = le.transform([city])[0]

    # Rest of the input
    BHK = int(input("Enter BHK (number of bedrooms): "))
    area = float(input("Enter area (sq ft): "))

    input_dict = {
        'region': region_encoded,
        'BHK': BHK,
        'area': area
    }

    price = predict_price(model, input_dict)
    print(f"\nPredicted Sale Price: ₹{price:,.2f}")
    print("Kaha s layega itna paisa? 😄, Chal dafa ho")

if __name__ == "__main__":
    main()
