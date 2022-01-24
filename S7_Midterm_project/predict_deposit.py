# to use the model

from flask import Flask
from flask import request
from flask import jsonify

import pickle
import numpy as np
import xgboost as xgb

# the scripts works, without importing skitlearn, but it must be installed

# Load the model

model_file = 'model_maxdepth=4.bin'

with open(model_file,'rb') as f_in: #read binary
    (dv, scaler, model) = pickle.load(f_in) 

app = Flask('deposit')
# a decorator: route is the address and we need the POST method
@app.route('/predict_deposit', methods=['POST'])

def predict_deposit():
    # to return the body of the JSON file as a python dict
    customer = request.get_json() 

    # make this customer into a feature matrix

    # replace with numbers 0 (negative or 'no') and 1 (positive or 'yes')
    for key, value in customer.items():
        if value == 'no':
            customer[key] = 0
    else:
        customer[key] = 1 

    # separate types    
    numerical = ['age','default','balance','housing','loan','day','duration','campaign','pdays','previous']
    categorical = [ 'job', 'marital', 'education', 'contact', 'month', 'poutcome']
    
    num_dict = dict()
    cat_dict = dict()
    
    for (key, value) in customer.items():
        if key in numerical:
            num_dict[key] = value
        else:
            cat_dict[key] = value

    # DictVect input must be a dict
    X_cat = dv.transform(cat_dict) # encode the categorical features
    print(X_cat)
    # Scaler input must be a np.array
    X_num = np.array(list(num_dict.values())).reshape(1, -1)
    X_num = scaler.transform(X_num) # scale the numerical features

    # Join both matrices
    X = np.column_stack([X_num, X_cat]) 

    dX = xgb.DMatrix(X, feature_names= numerical + dv.get_feature_names())
    
    # Apply the model to the customer matrix
    y_pred = model.predict(dX)    
    deposit = y_pred >= 0.5

    result = {
        'deposit_probability': float(y_pred), #float to turn the np.float64 to an usual python float
        'deposit': bool(deposit) # bool to turn the np.boolean into an usual python boolean
    }

    return jsonify(result)

# execute only if run as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
