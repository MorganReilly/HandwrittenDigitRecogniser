# ===  G00303598 -- Morgan Reilly  ===
# ===  Emerging Technologies 2019  ===

# -- Imports --
from flask import Flask, render_template, request
from keras.models import model_from_json
import base64
import re
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

# -- Flask instance --
app = Flask(__name__)

# -- Image Dimensions --
IMG_WIDTH, IMG_HEIGHT = 28, 28
IMG_DIM = IMG_WIDTH, IMG_HEIGHT

# -- Image Manipulation --
# Store all image paths here
canvas_grab_img = 'img_manipulation/canvas_grab.png'
greyscale_img = 'img_manipulation/greyscale_img.png'
resized_img = 'img_manipulation/resized_img.png'
sharpened_img = 'img_manipulation/sharpened_img.png'
brightened_img = 'img_manipulation/brightened_img.png'
contrasted_img = 'img_manipulation/contrasted_img.png'


# -- App Home --
# Route: /
# Return a render of html
@app.route('/')
def app_home():
    return render_template('mnist-input.html')


# -- Upload Digit --
# Method(s): POST
# Route: /upload
# Handle canvas send with Ajax
# Call to prediction && store prediction
# Print prediction to console => Verify of response
# Return prediction
@app.route('/predict', methods=['POST'])
def predict():
    return generate_prediction()


# -- Predict Digit --
# Call image manipulation && store response as array
# Call model manipulation && store response as integer
# Return prediction
def generate_prediction():
    img_reshape = image_manipulation()
    predicted_num = model_manipulation(img_reshape)
    print("Model Predicted: ", predicted_num)
    return predicted_num


# -- Manipulate Model --
# Parameters: Re-format model, store as array [call to 'image_manipulation()']
# Load model && store model
# Send array to model && store response
# Store first element of array
# Print element of array => Prediction
# Return prediction
def model_manipulation(img_reshape):
    model = load_saved_model()
    send_prediction = model.predict(img_reshape)
    receive_prediction = np.array(send_prediction[0])
    predicted_num = str(np.argmax(receive_prediction))
    return predicted_num


# -- Model Load --
# Try load from disk
# Otherwise generate new
# Finally return model
def load_saved_model():
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


# -- Manipulate Image --
# Generate the image [Encode && Decode]
# Convert to greyscale
# Reshape greyscale image to size 28px * 28px && save
# Apply enhancements
# Store as array && return
def image_manipulation():
    generate_image()
    convert_to_greyscale(canvas_grab_img)
    resize_image(IMG_DIM, greyscale_img)
    sharpen_image(resized_img, 2)
    brighten_image(sharpened_img, 2)
    contrast_image(brightened_img, 1)
    img_array = reshape_image(contrasted_img, IMG_WIDTH, IMG_HEIGHT)
    return img_array


# -- Convert Base64 to Image [png] --
# Get encoded URL from image
# Re-generate image from base64 image URL
# Store generated image
# Write generate image
def generate_image():
    # Adapted from:
    # https://stackoverflow.com/a/41256900/8883485
    # https://stackoverflow.com/a/31410635/8883485
    # https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
    ajax_call_data = request.values['imageString']  # Store string that's sent from Ajax call
    img_encoded = re.sub('^data:image/.+;base64,', '', ajax_call_data)
    img_decoded = base64.b64decode(img_encoded)
    with open(canvas_grab_img, 'wb') as f:
        f.write(img_decoded)
    return canvas_grab_img


# -- Convert To Greyscale --
# Open image to convert
# Convert to greyscale
# Save image
def convert_to_greyscale(img):
    # Adapted from: https://stackoverflow.com/a/12201744/8883485
    img = Image.open(img).convert('L')
    img.save(greyscale_img)  # Save the greyscale image


# -- Image Fit --
# Open canvas sent image
# Re-Map image to dimensions
# Save image
def resize_image(dim, img):
    # Adapted from: https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic
    img = Image.open(img)
    img = ImageOps.fit(img, dim, Image.ANTIALIAS)
    img.save(resized_img)


# -- Sharpen Image --
# Open image to manipulate
# Apply sharpen
# Set sharpen
# Enhance with sharpen
# Save image
def sharpen_image(img, s):
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open(img)
    img = ImageEnhance.Sharpness(img)
    sharpness = s
    img = img.enhance(sharpness)
    img.save(sharpened_img)  # Save the greyscale image


# -- Brighten image --
# Open image to manipulate
# Apply brighten
# Set brighten
# Enhance with brighten
# Save image
def brighten_image(img, b):
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open(img)
    img = ImageEnhance.Brightness(img)
    brightness = b
    img = img.enhance(brightness)
    img.save(brightened_img)


# -- Contrast image --
# Open image to manipulate
# Apply contrast
# Set contrast
# Enhance with contrast
# Save image
def contrast_image(img, c):
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open(img)
    img = ImageEnhance.Contrast(img)
    contrast = c
    img = img.enhance(contrast)
    img.save(contrasted_img)


# -- Reshape Image --
# Open image to convert
# Store as Array 28 * 28
# Return array
def reshape_image(img, img_width, img_height):
    # Adapted from: https://www.w3resource.com/numpy/manipulation/reshape.php
    img = Image.open(img)
    digit_28_28_array = np.array(img).reshape(1, img_width, img_height, 1)
    return digit_28_28_array


# -- App Run --
# Call to start application
if __name__ == '__main__':
    app.run()
