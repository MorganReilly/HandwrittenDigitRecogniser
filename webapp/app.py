from flask import Flask, render_template, request
import io, base64
import re
import cv2
from PIL import Image

app = Flask(__name__)


@app.route('/')
def app_home():
    return render_template('mnist-input.html')


@app.route('/upload', methods=['POST'])
def upload_digit():
    # Using these references
    # 1 https://www.base64encoder.io/python/
    # 2 https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
    # 3 https://stackoverflow.com/questions/31410525/base64-uri-to-png-python
    # 4 https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
    # 5 https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python

    # print("HERE!") # Debugging

    ajax_string = request.values['imageString']  # Store string that's sent from Ajax call
    # print(ajax_string)  # Non regex - Debugging

    # When the image is sent we need to remove the initial part
    # of the message sent
    # Using regex to cut first part of image data sent
    image_data = re.sub('^data:image/.+;base64,', '', ajax_string)
    print(image_data)  # This is the regex-ed image data

    # Converting base64 to image (using ref 4.)
    b64_bytes = base64.b64decode(image_data)
    digit_input = 'digit_input.png'
    with open(digit_input, 'wb') as f:
        f.write(b64_bytes)

    # Convert the image to greyscale
    img = Image.open('digit_input.png').convert('L')
    img.save('digit_input_grey.png')  # Save the greyscale image

    # need to store image in an array
    # MNIST read them in this way
    # need to match shape defined in model

    return "null"  # change this later ?


if __name__ == '__main__':
    app.run()
