# to use the model

from flask import Flask
from flask import request
from flask import jsonify

import pickle
import numpy as np
#from sklearn.ensemble import RandomForestClassifier
# the scripts works, without importing skitlearn, but it must be installed

# Load the model

model_file = 'model_RF_t=04.bin'

with open(model_file,'rb') as f_in: #read binary
    (dv, scaler, model) = pickle.load(f_in) 

app = Flask('heart')
# a decorator: route is the address and we need the POST method
@app.route('/predict', methods=['POST'])

def predict():
    # to return the body of the JSON file as a python dict
    patient = request.get_json() 

    # 1. Prepare the new patient data

    # separate types    
    numerical = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
    num_dict = dict()
    cat_dict = dict()
    
    for (key, value) in patient.items():
        if key in numerical:
            num_dict[key] = value
        else:
            cat_dict[key] = value

    # DictVect input must be a dict
    X_cat = dv.transform(cat_dict) # encode the categorical features

    # Scaler input must be a np.array
    X_num = np.array(list(num_dict.values())).reshape(1, -1)
    X_num = scaler.transform(X_num) # scale the numerical features

    # Join both arrays
    X = np.column_stack([X_num, X_cat]) 
    
    # 2. Apply the model to the new patient array  
    y_pred = model.predict_proba(X)[0,1] # 2nd col is prob of heart failure "yes"

    # extract decision threshold form model name
    aux0 = model_file.split('=')
    aux0[1]
    aux1 = aux0[1].split('.')
    t = aux1[0]
    t = int(t)
    t = t/10.

    # apply the decision threshold to convert into a raw score make a boolean
    heart_failure = y_pred >= t

    result = {
        'Decision threshold': float(t),
        'Heart failure probability': float(y_pred), #float to turn the np.float64 to an usual python float
        'Risk of heart failure': bool(heart_failure), # bool to turn the np.boolean into an usual python boolean

    }

    return jsonify(result)

# execute only if run as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
