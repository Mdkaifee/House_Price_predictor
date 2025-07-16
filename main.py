#Code without Flask web app

# from src.data_preprocessing import load_and_preprocess_data
# from src.train_model import train_and_save_model, load_model, evaluate_model
# from src.predict import predict_price
# import difflib

# def get_valid_input(user_input, options):
#     """Return exact or closest match from options (case-insensitive)."""
#     user_input_clean = user_input.strip().lower()
#     options_lower = [opt.lower() for opt in options]
#     if user_input_clean in options_lower:
#         return options[options_lower.index(user_input_clean)]
#     # Suggest the closest match (minimum similarity 0.7)
#     close = difflib.get_close_matches(user_input_clean, options_lower, n=1, cutoff=0.7)
#     if close:
#         suggestion = options[options_lower.index(close[0])]
#         print(f"Did you mean: {suggestion}?")
#         return suggestion
#     return None

# def main():
#     X_train, X_test, y_train, y_test, le = load_and_preprocess_data('data/house_price.csv')
#     train_and_save_model(X_train, y_train, model_path='model.pkl')
#     model = load_model('model.pkl')
#     acc = evaluate_model(model, X_test, y_test)
#     print(f"Model R² Score on Test Set: {acc:.3f}")

#     import pandas as pd
#     df = pd.read_csv('data/house_price.csv')
#     # Get mapping of state to cities
#     state_city_map = {}
#     for s, group in df.groupby('state'):
#         state_city_map[s] = sorted(group['Location'].unique().tolist())

#     # --- State selection ---
#     all_states = sorted(list(state_city_map.keys()))
#     print("\nStates:", ', '.join(all_states))
#     while True:
#         state_input = input("Enter state (choose from above): ")
#         state = get_valid_input(state_input, all_states)
#         if not state:
#             print("Sorry, state not in dataset. Please choose from above.")
#         else:
#             break

#     # --- City selection ---
#     cities = state_city_map[state]
#     print("\nCities in", state + ":", ', '.join(cities))
#     while True:
#         city_input = input("Enter city (choose from above): ")
#         city = get_valid_input(city_input, cities)
#         if not city:
#             print("Sorry, city not in selected state. Please choose from above.")
#         else:
#             break

#     # Get the encoded value for city/region
#     regions = list(le.classes_)
#     if city not in regions:
#         print("City not in model. Please restart and choose a valid city.")
#         return
#     region_encoded = le.transform([city])[0]

#     # --- BHK input validation ---
#     while True:
#         try:
#             BHK = int(input("Enter BHK (number of bedrooms): "))
#             if BHK < 1:
#                 print("Number of bedrooms must be at least 1.")
#             else:
#                 break
#         except ValueError:
#             print("Please enter a valid integer for BHK.")

#     # --- Area input validation ---
#     while True:
#         try:
#             area = float(input("Enter area (sq ft): "))
#             if area <= 0:
#                 print("Area must be a positive number greater than zero.")
#             else:
#                 break
#         except ValueError:
#             print("Please enter a valid number for area.")

#     input_dict = {
#         'region': region_encoded,
#         'BHK': BHK,
#         'area': area
#     }

#     price = predict_price(model, input_dict)
#     if price <= 0:
#         print("\nSorry, predicted price is not valid for the given inputs (result is negative or zero).")
#     else:
#         print(f"\nPredicted Sale Price: ₹{price:,.2f}")
#         print("Kaha s layega itna paisa? 😄, Chal dafa ho,Loan le kr aa")

# if __name__ == "__main__":
#     main()


#Code for Flask web app
from flask import Flask, jsonify, render_template, request
from src.data_preprocessing import load_and_preprocess_data
from src.train_model import train_and_save_model, load_model, evaluate_model
from src.predict import predict_price
import difflib
import pandas as pd
from num2words import num2words

app = Flask(__name__)

# Load & train once at startup
X_train, X_test, y_train, y_test, le = load_and_preprocess_data('data/house_price.csv')
train_and_save_model(X_train, y_train, model_path='model.pkl')
model = load_model('model.pkl')

df = pd.read_csv('data/house_price.csv')
state_city_map = {s: sorted(g['Location'].unique().tolist()) for s, g in df.groupby('state')}
all_states = sorted(state_city_map.keys())

def get_valid_input(user_input, options):
    user_input_clean = user_input.strip().lower()
    options_lower = [opt.lower() for opt in options]
    if user_input_clean in options_lower:
        return options[options_lower.index(user_input_clean)]
    close = difflib.get_close_matches(user_input_clean, options_lower, n=1, cutoff=0.7)
    if close:
        suggestion = options[options_lower.index(close[0])]
        return suggestion
    return None

@app.route('/get_cities/<state>')
def get_cities(state):
    state_decoded = state.replace("%20", " ")  # handle URL encoded spaces
    cities = state_city_map.get(state_decoded, [])
    return jsonify(cities)

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    price = None
    selected_state = None
    selected_city = None
    cities = []
    bhk = None
    area = None

    if request.method == 'POST':
        selected_state = request.form.get('state')
        selected_city = request.form.get('city')
        bhk_input = request.form.get('bhk')
        area_input = request.form.get('area')

        state = get_valid_input(selected_state, all_states)
        if not state:
            error = "Invalid state. Please select from the list."
        else:
            cities = state_city_map[state]
            city = get_valid_input(selected_city, cities)
            if not city:
                error = "Invalid city for selected state."
            else:
                try:
                    bhk = int(bhk_input)
                    area = float(area_input)
                    if bhk < 1 or area <= 0:
                        error = "BHK must be >= 1 and area must be > 0."
                except (ValueError, TypeError):
                    error = "Please enter valid BHK and area."

                if not error:
                    if city not in le.classes_:
                        error = "City not in model."
                    else:
                        region_encoded = le.transform([city])[0]
                        input_dict = {'region': region_encoded, 'BHK': bhk, 'area': area}
                        price = predict_price(model, input_dict)
                        if price <= 0:
                            error = "Predicted price invalid."

        if error:
            return render_template('index.html',
                                   states=all_states,
                                   cities=cities,
                                   error=error,
                                   selected_state=selected_state,
                                   selected_city=selected_city,
                                   bhk=bhk,
                                   area=area)
        # Convert price to words (Indian English)
        price_in_words = num2words(price, lang='en_IN', to='currency', currency='INR')

        # Successful prediction: render result page with both numeric and word prices
        return render_template('result.html', price=price, price_in_words=price_in_words)

    # GET request: no selection yet
    return render_template('index.html',
                           states=all_states,
                           cities=cities,
                           error=error,
                           selected_state=selected_state,
                           selected_city=selected_city,
                           bhk=bhk,
                           area=area)

if __name__ == '__main__':
    app.run(debug=True)
