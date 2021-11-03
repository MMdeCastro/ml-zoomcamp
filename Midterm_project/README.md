# Project description 

GOAL 

The classification goal is to predict if the client will subscribe (yes/no) a fix term deposit (target variable 'deposit') after a marketing campaign. It might help the bank in designing promotions, new campaigns, and understanding controversial campaign results.

DATA

Original dataset: [UCI Machine learning repository](https://archive.ics.uci.edu/ml/datasets/Bank%2BMarketing)

Here we use a subset of the dataset dowloaded from [Kaggle](https://www.kaggle.com/janiobachmann/bank-marketing-dataset).

Citation: _A Data-Driven Approach to Predict the Success of Bank Telemarketing_. S. Moro, P. Cortez and P. Rita., Decision Support Systems, Elsevier, 62:22-31, June 2014


## Folder content 

<ul>
<li> bank.csv -> the dataset </li>
<li> bank_marketing.ipynb -> jupyter notebook with the Exploratory Data Analysis and Model selection </li>
<li> bank_marketing_with_outputs.ipynb -> same notebook but with cell outputs (it might take a bit to render here) </li>
<li> train_deposit.py -> final model training and saving with pickle </li>
<li> predict_deposit.py -> model loading and web service deployment</li>
<li> predict_test_deposite.py -> output testing locally </li>
<li> pipenv and pipenv.lock -> for the virtual environment using pipenv </li>
<li> Dockerfile -> of a Docker container </li>
</ul>

## Deployment of model

Open the web server by running:

+ gunicorn --bind 0.0.0.0:9696 predict_deposit:app

(use 'waitress' instead of 'gunicorn' if you are in Windows).

The data of a new customer are written in 'predict_test_deposit.py'. Test the deployment by running it in other shell: 

+ python predict_test_deposit.py. 

The output (if that client will open a deposit or not and the probability) will be written in the shell.

Close the web server with 'Ctrl + c'.

## Virtual Environment 

Pipenv creates an enviroment with the name of the current folder. 

+ Install 'pipenv' running 'pip install pipenv' in shell.
+ Activate the environment running 'pipenv shell' in shell.
+ When then environment is activated, install everything using 'pipenv' instead of 'pip', for this project:

pipenv install numpy scikit-learn==1.00 xgboost flask gunicorn

+ The Pipfile records what you have installed (thus only run the packages installation once) and in the Pipfile.lock are the packages checksums.
+ Close the environment with 'Crt + d'

To use the environment, run 'pipenv shell' and deploy the model as said in the section above.

## Docker

Create a Docker image locally instead by running in shell:

'docker run -it --rm --entrypoint=bash python:3.8.12-slim'

The Dockerfile is this folder installs python, runs pipenv and its dependencies, runs the predict_deposit.py script to open the web server and the xgboost model and deploys it using gunicorn

~~~~
FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict_deposit.py", "model_maxdepth=4.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind 0.0.0.0:9696", "predict_deposit:app"]
~~~~

+ Build the docker container by running: 

docker built -t docker-deposit . 

(the last point means 'here', i.e., run it in the environment folder).

+ Run the docker container with: 

docker run -it -rm -p 9696:9696 docker-deposit 

and the model will be deployed and ready to use.
