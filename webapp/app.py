from flask import Flask, render_template, request
import io, base64
import re
from PIL import Image

# https://www.base64encoder.io/python/
# https://stackoverflow.com/questions/41256733/regex-to-extract-multiple-base64-encoded-image-from-string
# https://stackoverflow.com/questions/31410525/base64-uri-to-png-python

app = Flask(__name__)


@app.route('/')
def app_home():
    return render_template('mnist-input.html')


@app.route('/upload', methods=['POST'])
def upload_digit():
    print("HERE!")
    # Store string thats sent from Ajax call
    ajax_string = request.values[('imageString')]

    # When the image is sent we need to remove the initial part
    # of the message sent.

    # print(ajax_string)  # Non regex

    # using regex to cut first part of image data sent
    image_data = re.sub('^data:image/.+;base64,', '', ajax_string)
    print(image_data)

    # Converting base64 to image
    b64_bytes = base64.b64decode(image_data)
    image = io.BytesIO(b64_bytes)

    image.save("whatever.png")


    # save image as a png

    return "null"


if __name__ == '__main__':
    app.run()
