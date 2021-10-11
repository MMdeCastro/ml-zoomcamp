
import requests

url = 'http://localhost:9696/predict'

# customer Q4: {"contract": "two_year", "tenure": 1, "monthlycharges": 10}
# customer Q6: {"contract": "two_year", "tenure": 12, "monthlycharges": 10}

customer_id = 'customer in Q6' # 'xyz-123'
customer = {
 #   "gender": "female", 
 #   "seniorcitizen": 0,
 #   "partner": "yes", 
 #   "dependents": "no",
 #   "phoneservice": "no", 
 #   "multiplelines": "no_phone_service", 
 #   "internetservice": "dsl",
 #   "onlinesecurity": "no", 
 #   "onlinebackup": "yes", 
 #   "deviceprotection": "no", 
 #   "techsupport": "no",
 #   "streamingtv": "no", 
 #   "streamingmovies": "no", 
    "contract": "two_year", 
 #   "paperlessbilling": "yes",
 #   "paymentmethod": "electronic_check",
    "tenure": 12, 
    "monthlycharges": 10.0, 
 #   "totalcharges": 29.85      
}

# send this customer as a post request
response = requests.post(url,json=customer).json() # turn the response to a python dict
print(response)

if response['churn'] == True:
    print('sending promo email to %s' % customer_id)
else:
    print('not sending promo email to %s' % customer_id)