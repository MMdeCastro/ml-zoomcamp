#!/usr/bin/env python
# coding: utf-8

# # Serverless Deep Learning
# 
# We'll deploy the dogs vs cats model we trained in Session 8
# It is already converted to tflite 
# It is tf- and keras-independent

import numpy as np

import tflite_runtime.interpreter as tflite

from io import BytesIO
from urllib import request

from PIL import Image


interpreter = tflite.Interpreter(model_path='cats-dogs-v2.tflite') # my model name dogs-cats.tflite (/= Alexey model's name)
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

#url = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Pug_600.jpg'
target_size = 150 # we check the target size in the code for Session 8

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((target_size,target_size), Image.NEAREST) # nearest is the interpolation method
    return img

def preprocess_input(x):
    x /= 255.
    return x

def predict(url):

    img = download_image(url)
    img = prepare_image(img,target_size)

    x = np.array(img, dtype='float32') # image to np.arry
    X = np.array([x]) # image to batch of 1 image

    X = preprocess_input(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    float_predictions = preds[0].tolist() # convert np.array to usual python floats which are serializable

    return float_predictions 

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result




