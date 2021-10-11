# to use the model

from flask import Flask
from flask import request
from flask import jsonify

import pickle
# the scripts works, without importing skitlearn, but it must be installed

# Load the model and dictvect

model_file = 'model1.bin'
dictvec_file = 'dv.bin'

with open(model_file,'rb') as f_in: #read binary
    model = pickle.load(f_in) 

with open(dictvec_file,'rb') as f_in: #read binary
    dv = pickle.load(f_in)

app = Flask('churn')
# a decorator: route is the address and we need the POST method
@app.route('/predict', methods=['POST'])

def predict():
    # to return the body of the JSON file as a python dict
    customer = request.get_json() 
    # make this customer into a feature matrix
    X = dv.transform([customer])
    # apply the model to the customer matrix
    y_pred = model.predict_proba(X)[0,1] # 2nd col is prob of churning
    churn = y_pred >= 0.5

    result = {
        'churn_probability': float(y_pred), #float to turn the np.float64 to an usual python float
        'churn': bool(churn) # bool to turn the np.boolean into an usual python boolean
    }

    return jsonify(result)

# execute only if run as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
