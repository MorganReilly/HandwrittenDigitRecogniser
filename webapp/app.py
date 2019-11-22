# G00303598 -- Morgan Reilly
# Emerging Technologies -- 2019

# References
# https://www.base64encoder.io/python/
# https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
# https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
# https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
# https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
# https://machinelearningmastery.com/save-load-keras-deep-learning-models/#
# https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic

# Imports 
from flask import Flask, render_template, request
import io, base64
import re
import cv2
from keras.models import model_from_json
from PIL import Image, ImageOps

# Flask instance
app = Flask(__name__) 

 # Previously trained model
loaded_model.load_weights("model.h5")
print("Model loaded from disk")

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
    digit_28_28_array = np.array(fit_and_resized_image).reshape(1,28,28,1)

    return "null"  # Return predicted digit


if __name__ == '__main__':
    app.run()
