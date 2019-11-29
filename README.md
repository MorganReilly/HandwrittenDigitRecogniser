# Emerging Technologies
# _Handwritten Image Recognition with Keras and MNIST_

## Environment Setup -- Linux (Using Python 3.6 | Pip Virtual Environment)
* Download requirements.txt
* Create Virtual Environment
* $ python3 -m venv venv
* Populate virtual environment with pip packages
* $ venv/bin/pip3 install -r requirements.txt
* Activate Virtual Environment
* $ source venv/bin/activate

### Flask Deployment -- Linux
* Load model
* $ python3 model.py
* Export Flask App
* $ export FLASK_APP=app.py
* Run Flask App
* $ flask run

## Environment Setup -- Windows (Using Anaconda 3.7 | Conda Virtual Evironment)
NOTE: Please run CMDER as Administrator, or conda commands will not run correctly. (Ignore if already set up).
* Create Conda Environment
* $ conda create --name venv
* Activate Conda Environment
* $ conda activate venv
* Download nesseccary packages
* $ conda install -c anaconda flask -y
* $ conda install -c conda-forge tensorflow
* $ conda install -c conda-forge keras -y
* $ conda install -c anaconda pillow

### Flask Deployment -- Windows
* Locate clone and change directory to webapp
* $ cd path/to/webapp
* Load model
* $ python model.py
* Export Flask App
* $ set FLASK_APP=app.py
* Run Flask App
* $ flask run

### References -- Model
* [Google Codelab tutorial](https://codelabs.developers.google.com/codelabs/cloud-tensorflow-mnist/index.html?index=..%2F..index#0)
* http://neuralnetworksanddeeplearning.com/chap1.html
* https://keras.io/
* https://keras.io/examples/mnist_cnn/
* https://www.ics.uci.edu/~mohamadt/keras_mnist.html
* [3 Brown 1 Blue - What is a neural network](https://www.youtube.com/watch?v=aircAruvnKk)
* https://www.kaggle.com/cdeotte/how-to-choose-cnn-architecture-mnist

### References -- Webapp
* https://www.base64encoder.io/python/
* https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
* https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
* https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
* https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
* https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic

#### References -- EC2 AWS Hosting -- Link To Be Updated (Currently under maintenence)
Note:To host this on AWS I needed 2 things, Nginx and Gunicorn. Nginx handles the static files and Gunuicorn3 creates unix sockets and allows flask to talk to nginx. 

* https://www.youtube.com/watch?v=-Gc8CMjQZfc
* https://www.youtube.com/watch?v=IwcuuWCWMic
* https://www.youtube.com/watch?v=IwcuuWCWMic
* https://www.youtube.com/watch?v=tW6jtOOGVJI
* https://www.youtube.com/watch?v=Dx4Gb4TbCGs
* http://bencentra.com/code/2014/12/05/html5-canvas-touch-events.html
