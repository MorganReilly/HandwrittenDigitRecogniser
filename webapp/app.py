# G00303598 -- Morgan Reilly
# Emerging Technologies -- 2019

# References
# 1 https://www.base64encoder.io/python/
# 2 https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
# 3 https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
# 4 https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
# 5 https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python

# Imports
from flask import Flask, render_template, request
from keras.models import model_from_json
import base64
import re
import numpy as np
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageOps

print(tf.__version__)
# Flask instance
app = Flask(__name__)

# Re-size image
imHeight = 28
imWidth = 28
size = imHeight, imWidth  # image size for model


# Defualt route
@app.route('/')
def app_home():
    return render_template('mnist-input.html')


# Route to canvas and to upload
@app.route('/upload', methods=['POST'])
def upload_digit():
    print("HERE!")
    ajax_string = request.values['imageString']  # Store string that's sent from Ajax call
    # print(ajax_string)  # Non regex - Debugging

    # When the image is sent we need to remove the initial part
    # of the message sent
    # Using regex to cut first part of image data sent
    image_data = re.sub('^data:image/.+;base64,', '', ajax_string)
    print(image_data)  # This is the regex-ed image data

    # Converting base64 to image (using ref 4.)
    decodedImage = base64.b64decode(image_data)
    digit_input = 'digit_input.png'
    with open(digit_input, 'wb') as f:
        f.write(decodedImage)

    # Convert the image to greyscale
    img = Image.open('digit_input.png').convert('L')
    img.save('digit_input_grey.png')  # Save the greyscale image

    # Need to match shape defined in model => 28 x 28
    # https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic
    # To do this we need to resize the image
    original_image = Image.open('digit_input_grey.png')
    size = (28, 28)
    fit_and_resized_image = ImageOps.fit(original_image, size, Image.ANTIALIAS)

    # Save resized image
    fit_and_resized_image.save('digit-28-28.png')

    # Need to store image in an array
    # MNIST reads them in this way
    digit_28_28_array = np.array(fit_and_resized_image).reshape(1, 28, 28, 1)

    model = load_saved_model()

    # Need to send and receive prediction to model
    print("Before sendPrediction")
    sendPrediction = model.predict(digit_28_28_array)
    print("After sP, before rP")
    recievePrediction = np.array(sendPrediction[0])
    print("After rP")

    # Need to store the response as a String
    prediction = str(np.argmax(recievePrediction))
    print(prediction)

    return prediction  # Return predicted digit


def load_saved_model():
    # Try to load the model
    try:
        # Load json file and create new model
        json_to_open = open('model.json', 'r')
        loaded_json_model = json_to_open.read()
        json_to_open.close()
        model = model_from_json(loaded_json_model)

        # Load weights into new model
        model.load_weights("model.h5")
        print("Loaded from disk")
    except:
        print("ERROR: Could Not Load Model")
    return model


if __name__ == '__main__':
    app.run()
