
import requests

url = 'http://localhost:9696/predict'

patient_id = 'xyz-123'
patient = {
    "Age": 56,
    "Sex": "F",
    "ChestPainType": "ATA", 
    "RestingBP": 130,  
    "Cholesterol": 150, 
    "FastingBS": "L",
    "RestingECG": "ST",
    "MaxHR": 115,
    "ExerciseAngina": "N",
    "Oldpeak": 1.,
    "ST_Slope": "Flat",
 }

# send this customer as a post request
response = requests.post(url,json=patient).json() # turn the response to a python dict
print(response)

if response['Risk of heart failure'] == True:
    print("Patient %s is in risk of suffering a heart failure" % patient_id)
else:
    print("Patient %s is not in risk of suffering a heart failure" % patient_id)
