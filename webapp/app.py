# G00303598 -- Morgan Reilly
# Emerging Technologies -- 2019

# References
# 1 https://www.base64encoder.io/python/
# 2 https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
# 3 https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
# 4 https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
# 5 https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
# https://dev.to/petercour/enhance-image-with-python-pil-222e
# Imports
from flask import Flask, render_template, request
from keras.models import model_from_json
import base64
import re
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps, ImageEnhance

print(tf.__version__)
# Flask instance
app = Flask(__name__)

# Re-size image
WIDTH = 28
HEIGHT = 28
DIM = WIDTH, HEIGHT  # image size for model


# Defualt route
@app.route('/')
def app_home():
    return render_template('mnist-input.html')


# Route to canvas and to upload
@app.route('/upload', methods=['POST'])
def upload_digit():
    # Need to retrieve the image url string
    # Then need to cut the base64 out of it using a regex string
    # Then need to convert the base64 to an image
    # We then convert the image to greyscale
    # We then need to rescale the image to 28 * 28 to match the model
    # Store the image in an array with resized dimensions
    digit_28_28_array = image_manipulation()
    # Load the model from memory
    model = load_saved_model()
    # Need to send and receive prediction to model
    send_prediction = model.predict(digit_28_28_array)
    receive_prediction = np.array(send_prediction[0])
    # Need to store the response as a String
    prediction = str(np.argmax(receive_prediction))
    print("Model Predicted: ", prediction)

    return prediction  # Return predicted digit


def image_manipulation():
    # Need to retrieve the image url string
    # Then need to cut the base64 out of it using a regex string
    # Then need to convert the base64 to an image
    convert_b64_to_image()
    # We then convert the image to greyscale
    convert_img_to_greyscale()
    # We then need to rescale the image to 28 * 28 to match the model
    fit_img_to_model()
    # Seeing if I can enhance the image
    enhance_image()
    # Store the image in an array with resized dimensions
    digit_28_28_array = store_as_array()
    return digit_28_28_array


# Used for retrieving the url sent through Ajax
def get_image_string():
    ajax_string = request.values['imageString']  # Store string that's sent from Ajax call
    # print(ajax_string)  # Non regex - Debugging

    # When the image is sent we need to remove the initial part
    # of the message sent
    # Using regex to cut first part of image data sent
    image_data = re.sub('^data:image/.+;base64,', '', ajax_string)
    # print(image_data)  # This is the regex-ed image data
    return image_data


def convert_b64_to_image():
    # Receive regex-ed string
    image_data = get_image_string()
    # Converting base64 to image (using ref 4.)
    decoded_image = base64.b64decode(image_data)
    digit_input = 'img_manipulation/digit_input.png'
    with open(digit_input, 'wb') as f:
        f.write(decoded_image)


# Enhances an image through:
# Sharpening, Brightening and Contrasting
def enhance_image():
    sharpen_image()
    brighten_image()
    contrast_image()


# Sharpen image
def sharpen_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open('img_manipulation/digit-28-28.png')
    img = ImageEnhance.Sharpness(img)
    sharpness = 6.0
    sharp_img = img.enhance(sharpness)
    sharp_img.save('img_manipulation/sharp_img.png')  # Save the greyscale image


# Brighten image
def brighten_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open('img_manipulation/sharp_img.png')
    img = ImageEnhance.Brightness(img)
    brightness = 1.5
    brightened_img = img.enhance(brightness)
    brightened_img.save('img_manipulation/bright_img.png')


# Contrast image
def contrast_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    # Load image image to enhance
    img = Image.open('img_manipulation/bright_img.png')
    img = ImageEnhance.Contrast(img)
    contrast = 3
    contrast_img = img.enhance(contrast)
    contrast_img.save('img_manipulation/28-28.png')


def convert_img_to_greyscale():
    # Convert the image to greyscale
    img = Image.open('img_manipulation/digit_input.png').convert('L')
    img.save('img_manipulation/digit_input_grey.png')  # Save the greyscale image


def fit_img_to_model():
    # Need to match shape defined in model => 28 x 28
    # https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic
    # To do this we need to resize the image
    original_image = Image.open('img_manipulation/digit_input_grey.png')
    fit_and_resized_image = ImageOps.fit(original_image, DIM, Image.ANTIALIAS)
    # Save resized image
    fit_and_resized_image.save('img_manipulation/digit-28-28.png')


def store_as_array():
    # Need to store image in an array
    # Model reads them in this way
    img = Image.open('img_manipulation/28-28.png')
    digit_28_28_array = np.array(img).reshape(1, WIDTH, HEIGHT, 1)
    return digit_28_28_array


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
    except():
        print("Model load failed successfully!")
    finally:
        return model


if __name__ == '__main__':
    app.run()
