# to use the model

import pickle
# the scripts works, without importing skitlearn, but it must be instaled

# Load the model  and dictvect

model_file = 'model1.bin'
dictvec_file = 'dv.bin'

with open(model_file,'rb') as f_in: #read binary
    model = pickle.load(f_in) 

with open(dictvec_file,'rb') as f_in: #read binary
    dv = pickle.load(f_in)

# customer Q3: {"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}

customer = {
#    'gender': 'female', 
#    'seniorcitizen': 0,
#    'partner': 'yes', 
#    'dependents': 'no',
#    'phoneservice': 'no', 
#    'multiplelines': 'no_phone_service', 
#    'internetservice': 'dsl',
#    'onlinesecurity': 'no', 
#    'onlinebackup': 'yes', 
#    'deviceprotection': 'no', 
#    'techsupport': 'no',
#    'streamingtv': 'no', 
#    'streamingmovies': 'no', 
    'contract': 'two_year', #'month-to-month', 
#    'paperlessbilling': 'yes',
#    'paymentmethod': 'electronic_check',
    'tenure': 12, 
    'monthlycharges': 19.7, 
#    'totalcharges': 29.85      
}

# make this customer into a feature matrix
X = dv.transform([customer])

# apply the model to the customer matrix
y_pred = model.predict_proba(X)[0,1] # 2nd col is prob of churning

print('input', customer)
print('churn probability', y_pred)


