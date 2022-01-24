# Heart Failure project description 
 
Goal

We want to predict the risk of suffering a heart failure on patients by knowning if they suffer hypertension, diabetes, high cholesterol levels,... and other features as age or sex considered as potential risk factors in the detection of cardiovascular diseases. The conclusions of analysis like this one might help in early detection, the design of prevention campaigns, and understanding controversial diagnosis.

Method

We will automate the task using the most popular classification models. Most of the work is related to the data preparation, the tuning of the model parameters, and the evaluation of the model performance. 

Data

We use the dataset available in the Kaggle database: Kaggle Heart Failure Prediction Dataset (citation: fedesoriano. (September 2021) Heart Failure Prediction Dataset)

Clone the repo to your computer and navigate to this project folder (see the folder content below). 

Beside the dependencies indicated in the `requirements.txt` file (we will show how to install them below), you need to have installed:
+ [Python](https://www.python.org/downloads/),
+ [Jupyter](https://jupyter.org/install), 
+ [Jupyter Nbextensions](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html) and the "Collapsible headings" enabled (under Nbextensions in the Jupyter toolbar), and
+ Docker, in Ubuntu one just run the following in a shell:

+ `sudo apt-get install docker.io`

## Folder content 

<ul>
<li> `heart.csv` -> the dataset we use to train the models</li>
<li> `Heart_Failure.ipynb` -> the Jupyter Notebook with the Exploratory Data Analysis and the Model Selection </li>
<li> `train.py` -> to train the final model and save it with pickle to the file model_RF_t=04.bin</li>
<li> `model_RF_t=04.bin` -> the final model, in case you do not want to save it yourself by running `train.py`
<li> `predict.py` -> to load the model and deploy it in a web service</li>
<li> `predict_test.py` -> to test the web service locally </li>
<li> `Pipfile` and `Pipfile.lock` -> for the virtual environment using pipenv </li>
<li> `Dockerfile` -> the info `Docker` need to create the container </li>
</ul>


## Virtual environment 

Pipenv creates an enviroment with the name of the current folder. 

Install 'pipenv' running in shell:

+ `pip install pipenv`

Activate the environment running in shell:

+ `pipenv shell`

The packages indicated in the Pipfile provided in this folder will be installed in your computer. In case you would like to add other packages, install them using 'pipenv' instead of just 'pip'. For instance, for this project the Pipfile and Pipfile.lock (with the packages checksums) were created by running in shell (but you do not have to run this command):

+ `pipenv install -r requirements.txt` 

Next time you want to active the environment, just run 'pipenv shell'. Go out of the environment with 'Crt + d' (you do not need to have it activate when using the containerization explained in the last section).

## Check the data exploration and model selection

Once the environment is activated by `pipenv shell`, run in the shell:

+ `jupyter notebook` 

and Jupyter will open in your browser, then click on the notebook `Heart_Failure.ipynb`. 

When you are finished with the notebook, press 'Quit' in the Jupyter (top right corner) or 'Ctrl + c' in the shell, and Jupyter will be closed.

## Generate the model file

With the environment activated, run in the shell:

+ `python train.py`

and a file with name `model_RF_t=04.bin` comprising the Random Forest model with decision threshold 0.4 we selected as best performer (see `Heart_Failure.ipynb`).

## Apply the model in the web service

Open a terminal in your computer, navigate to the folder where you cloned this folder, and run the web server typing:

+ `gunicorn --bind 0.0.0.0:9696 predict:app`

(use 'waitress' instead of 'gunicorn' if you are in Windows).

The data of a new patient are written in 'predict_test.py'. Test the deployment by running the script in other shell: 

+ `python predict_test.py` 

The shell output will tell you if that patient is in risk of suffering a heart failure or not.

Close the web server with 'Ctrl + c'.

## Docker container

We do not need to install packages, activate environments, train models,... everytime we want to know if a new patient is in risk of suffering a heart failure. We can skip the former sections using a Docker container. To install docker, if you have not done it yet, run in another shell (not in an environment shell):

+ `sudo apt-get install docker.io`

First, create a Docker image locally by running in shell (the enviroment does not need to be activated):

+ `docker run -it --rm --entrypoint=bash python:3.8.12-slim`

That will open a container shell (the `-it` tag is to acces the container from the terminal, the --rm is to remove the image once we use it). It will take some minutes the first time you run it (if the image is not found locally, it is pulled from the dockerhub). 

Exit the container shell with `Ctrl + d`.

The Dockerfile is this folder installs python, runs pipenv to install packages and dependencies, runs the predict.py script to open the web server and deploys it using gunicorn

Build the docker container by running in normal shell (not in the container shell): 

+ `docker build -t "docker-heart" .` 

(watch the last point, it means 'here', i.e., build the container within the environment folder). The first build takes some minutes.

Run the docker container with: 

+ `docker run -it --rm -p 9696:9696 docker-heart` 

and the model will be deployed and ready to use: send a new request by opening a new shell in the enviroment directory and directly run:

+ `python predict_test.py`

As before, the shell output will tell you if that patient is in risk of suffering a heart failure or not.

Close the container with 'Ctrl + c'.