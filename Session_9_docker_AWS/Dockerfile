FROM agrigorev/zoomcamp-cats-dogs-lambda:v2

RUN pip install pillow
RUN pip install numpy
RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp38-cp38-linux_x86_64.whl

COPY lambda_dogs_cats.py .

CMD [ "lambda_dogs_cats.lambda_handler" ]
