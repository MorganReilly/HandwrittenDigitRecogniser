# Emerging Technologies
# _Handwritten Image Recognition with Keras and MNIST_

## Environment Setup => Linux
* Download Requirements.txt
* $ cd webapp
* Create Virtual Environment
* $ python3 -m venv venv
* Populate virtual environment with pip packages
* $ sudo venv/bin/pip3 install -r requirements.txt
* Activate Virtual Environment
* $ source venv/bin/activate
* Load model
* $ python3 model.py
* Export Flask App
* $ export FLASK_APP=app.py
* Run Flask App
* $ flask run

## Environment Setup => Windows
* TBD

### References -- Model
* [Google Codelab tutorial](https://codelabs.developers.google.com/codelabs/cloud-tensorflow-mnist/index.html?index=..%2F..index#0)
* http://neuralnetworksanddeeplearning.com/chap1.html
* https://keras.io/
* https://keras.io/examples/mnist_cnn/
* https://www.ics.uci.edu/~mohamadt/keras_mnist.html
* [3 Brown 1 Blue - What is a neural network](https://www.youtube.com/watch?v=aircAruvnKk)
* https://www.kaggle.com/cdeotte/how-to-choose-cnn-architecture-mnist

### References -- Webapp
* Human Activity Recognition Comparitive - Jamie O' Halloran (Thesis - Unpublished but can show on request)
* https://www.base64encoder.io/python/
* https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
* https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
* https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
* https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
* https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic

#### References -- EC2 AWS Hosting -- http://34.245.207.140:8080/
Note: The code for this part of the project is hosted on the AWS instance. It contains a slightly modified base to allow for touch and a redesign of the home page to avoid scrolling issues. It also contains nginx and gunicorn3. Nginx handles the static files and Gunuicorn3 creates unix sockets and allows flask to talk to nginx. 

* https://www.youtube.com/watch?v=-Gc8CMjQZfc
* https://www.youtube.com/watch?v=IwcuuWCWMic
* https://www.youtube.com/watch?v=IwcuuWCWMic
* https://www.youtube.com/watch?v=tW6jtOOGVJI
* https://www.youtube.com/watch?v=Dx4Gb4TbCGs
* http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
