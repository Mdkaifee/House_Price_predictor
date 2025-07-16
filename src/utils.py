def get_user_input(feature_names):
    input_dict = {}
    for feat in feature_names:
        val = input(f"Enter value for {feat}: ")
        try:
            val = float(val)
        except:
            pass
        input_dict[feat] = val
    return input_dict
