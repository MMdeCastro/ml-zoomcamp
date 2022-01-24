# Heart Failure project description 
 
Goal

We want to predict the risk of suffering a heart failure on patients by knowning if they suffer hypertension, diabetes, high cholesterol levels,... and other features, as age or sex, which are considered as potential risk factors in the detection of cardiovascular diseases. The conclusions of analysis like this one might help in early detection, the design of prevention campaigns, and understanding controversial diagnosis.

Method

We will automate the task using the most popular classification models. Most of the work is related to the data preparation, the tuning of the model parameters, and the evaluation of the model performance. 

Data

We use the dataset available in the Kaggle database: Kaggle Heart Failure Prediction Dataset (citation: fedesoriano. (September 2021) Heart Failure Prediction Dataset)

Clone the repo to your computer and navigate to this project folder (see the folder content below). 

Beside the dependencies indicated in the `environment.yml` file (we will show how to install them below), you need to have installed:
+ [miniconda](https://docs.conda.io/en/latest/miniconda.html) or a bigger `conda` version, all of them already contain `Python`, the programming language we will use, and [pip](https://pip.pypa.io/en/stable/installation/), a package manager we will need, and
+ `Docker`, for the containarization, in Ubuntu one just run the following in a shell: `sudo apt-get install docker.io`

## Folder content 

<ul>
<li> environment.yml -> the file with the packages we need 
<li> heart.csv -> the dataset we use to train the models</li>
<li> Heart_Failure.ipynb -> the Jupyter Notebook with the Exploratory Data Analysis and the Model Selection </li>
<li> train.py` -> to train the final model and save it with pickle to the file model_RF_t=04.bin</li>
<li> model_RF_t=04.bin -> the final model, in case you do not want to generate it yourself by running `python train.py`
<li> predict.py -> to load the model and deploy it in a web service</li>
<li> predict_test.py -> to test the web service locally </li>
<li> Pipfile and Pipfile.lock -> for the virtual environment using pipenv </li>
<li> Dockerfile -> the info `Docker` need to create the container </li>
</ul>


## Virtual environment 

In a terminal or bash shell (if you are in Linux or Mac, or in the Anaconda prompt if you are in Windows), navigate to the folder where you cloned the Heart Failure Prediction project and run:

+ `conda env create -f environment.yml`

and the packages we need will be installed.

To activate this environment, use

+ `conda activate heart`

To deactivate an active environment, use

+ `conda deactivate`

## Have a look to the data exploration and model selection in the Jupyter Notebook

Once the 'heart' `conda` environment is activated, run in the shell:

+ `jupyter notebook` 

and Jupyter will open in your browser, enable 'Collapsible headings' in the Nbextensions menu (see the Jupyter toolbar) and then click on the Jupyter Notebook `Heart_Failure.ipynb`. It will open in your browser. Then follow the instructions in the Jyputer Notebook. 

When you are finished with the notebook, press 'Quit' in the Jupyter (top right corner) or `Ctrl + c` in the shell, and Jupyter will be closed.

## Generate the model file

Everything in the following should take place within the `conda` environment 'heart' activated, and still in the folder where you cloned the Heart Failure Prediction project, run in the shell:

+ `python train.py`

and in your project folder, a file with name `model_RF_t=04.bin` (it occupies about 277kB) comprising the Random Forest model (with decision threshold 0.4) that we selected as best performer (see `Heart_Failure.ipynb`), will be created.

## Apply the model in the web service

Run the web server typing:

+ `gunicorn --bind 0.0.0.0:9696 predict:app`

(use `waitress` instead of `gunicorn` if you are in Windows).

The data of a new patient are written in 'predict_test.py'. Test the deployment by running the script in other shell: 

+ `python predict_test.py` 

The shell output will tell you if that new patient is in risk of suffering a heart failure or not. Modify the info in `predict_test.py` to simulate different new patients.

Close the web server with 'Ctrl + c'.

## Docker container

We do not need to install packages, activate environments, train models,... everytime we want to know if a new patient is in risk of suffering a heart failure. We can skip the former sections using a Docker container. To install docker, if you have not done it yet, run in another shell (not in an environment shell):

+ `sudo apt-get install docker.io`

A `Pipfile` and a `Pipfile.lock` are already in the folder you cloned, we need them to populate the Docker container. Here we explain how we have created that files, therefore you do not have to reproduce the following 3 command lines. We have used `Pipenv` to create the `Pipfile` and the `Pipfile.lock` that record the info of the packages we need to have inside the container. We have installed [pipenv](https://pypi.org/project/pipenv/) in the conda environment 'heart' by running in the shell:

+ `pip install pipenv` (you do not have to run this because you already have the `Pipfile` and `Pipfile.lock` files)

We activated the `pipenv` environment (it takes the name of the project folder you are) by running in the folder shell (inside the `conda` environment):

+ `pipenv shell` (you do not have to run this because you already have the `Pipfile` and `Pipfile.lock` files)

and then we installed the packages we need in the container by running:

+ `pipenv install numpy scikit-learn==1.00 flask gunicorn` (you do not have to run this because you already have the `Pipfile` and `Pipfile.lock` files)

and we went out of the `pipenv` environment with 'Crt + d'.

With the `Pipfile` and `Pipfile.lock` we are ready to create a Docker image. 

Please, follow the step below:

in a new shell (neither the conda 'heart', nor the pipenv enviroments need to be activated, just be in the project folder), run:

+ `docker run -it --rm --entrypoint=bash python:3.8.12-slim`

That will open a container shell (the `-it` tag is to acces the container from the terminal, the --rm is to remove the image once we use it). It will take some minutes the first time you run it (if the image is not found locally, it is pulled from the dockerhub). 

Exit the container shell with `Ctrl + d`.

The Dockerfile is this folder installs `Python`, runs `pipenv` to install packages and dependencies, runs the `predict.py` script to open the web server and deploys it using `gunicorn` (now it does not matter anymore if you are in Windows, no need to replace `gunicorn` with `waitress` because inside the container your native OS does not matter).

Build the docker container by running in normal shell (not in the container shell): 

+ `docker build -t "docker-heart" .` 

(watch the last point, it means 'here', i.e., build the container within the environment folder). The first build takes some minutes.

Run the docker container with: 

+ `docker run -it --rm -p 9696:9696 docker-heart` 

and the model will be deployed and ready to use: send a new request by opening a new shell in the enviroment directory and directly run:

+ `python predict_test.py`

As before, the shell output will tell you if that patient is in risk of suffering a heart failure or not.

Close the container with 'Ctrl + c'.