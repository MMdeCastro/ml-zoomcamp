
import requests

url = 'http://localhost:9696/predict_deposit'

customer_id = 'xyz-123'
customer = {
    "age": 56,
    "job": "admin.",
    "marital": "married",
    "education": "secondary",
    "default": "no",
    "balance": 45,
    "housing": "no",
    "loan": "no",
    "contact": "unknown",
    "day": 5,
    "month": "may",
    "duration": 1467,
    "campaign": 1,
    "pdays": -1,
    "previous": 0,
    "poutcome": "unknown"
 }

# send this customer as a post request
response = requests.post(url,json=customer).json() # turn the response to a python dict
print(response)

if response["deposit"] == True:
    print("Customer %s will probably open a fix term deposit" % customer_id)
else:
    print("Customer %s will probably not open a fix term deposit" % customer_id)
