# Emerging Technologies
# _Handwritten Image Recognition with Keras and MNIST, Hosted with Flask_

![logo](images/keras.png) ![mnist](images/mnist.png) ![flask](images/flask.png)

## Environment Setup -- Linux (Using Python 3.6 | Pip Virtual Environment)
* Download requirements.txt
* Create Virtual Environment
* `$ python3 -m venv venv`
* Populate virtual environment with pip packages
* `$ venv/bin/pip3 install -r requirements.txt`
* Activate Virtual Environment
* `$ source venv/bin/activate`

### Flask Deployment -- Linux
* Load model
* `$ python3 model.py`
* Export Flask App
* `$ export FLASK_APP=app.py`
* Run Flask App
* `$ flask run`

## Environment Setup -- Windows (Using Anaconda 3.7 | Conda Virtual Evironment)
NOTE: Please run CMDER as Administrator, or conda commands will not run correctly. (Ignore if already set up).
* Create Conda Environment
* `$ conda create --name venv`
* Activate Conda Environment
* `$ conda activate venv`
* Download nesseccary packages
* `$ conda install -c anaconda flask -y`
* `$ conda install -c conda-forge tensorflow`
* `$ conda install -c conda-forge keras -y`
* `$ conda install -c anaconda pillow`

### Flask Deployment -- Windows
* Locate clone and change directory to webapp
* `$ cd path/to/webapp`
* Load model
* `$ python model.py`
* Export Flask App
* `$ set FLASK_APP=app.py`
* Run Flask App
* `$ flask run`

## About The Model
The [Model](keras-mnist-nn.ipynb) I used is a Sequential CNN with 16 layers. It has an accuracy of 99.40% and a loss of 0.0191%.

### References -- Model
To condense this README into a more read-able format all references are with their respective code in both [Flask App](webapp) and [Jupyter Notebook](keras-mnist-nn.ipynb)

#### References -- EC2 AWS Hosting -- (Link Available on Request)
Note:To host this on AWS I needed 2 things, Nginx and Gunicorn. Nginx handles the static files and Gunuicorn3 creates unix sockets and allows flask to talk to nginx.
I added this part only to see if I could get it running on mobile. However, the site is poorly optimized and I don't have the time to fix it. 

* [Tutorial 1](https://www.youtube.com/watch?v=-Gc8CMjQZfc)
* [Tutorial 2](https://www.youtube.com/watch?v=IwcuuWCWMic)
* [Tutorial 3](https://www.youtube.com/watch?v=IwcuuWCWMic)
* [Tutorial 4](https://www.youtube.com/watch?v=tW6jtOOGVJI)
* [Tutorial 5](https://www.youtube.com/watch?v=Dx4Gb4TbCGs)
