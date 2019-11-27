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
WIDTH = 28
HEIGHT = 28
DIM = WIDTH, HEIGHT


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
# Call to set decoded image
# Call to decode image
# Return base64 value
# Reconstruct image and convert to greyscale
# Reshape greyscale image to size 28px * 28px && save
# Enhance image && save
# Store as array && return
def image_manipulation():
    decode_image()
    enhance_image()
    return reshape_image()


# -- Convert Base64 to Image [png] --
# Get encoded URL from image
# Re-generate image from base64 image URL
# Store generated image
# Write generate image
def decode_image():
    img_encoded = encode_image()
    img_decoded = base64.b64decode(img_encoded)
    digit_input = 'img_manipulation/digit_input.png'
    with open(digit_input, 'wb') as f:
        f.write(img_decoded)


# -- Encode Image to Base64 --
# Store POST value from Ajax call
# Cut base64 from String with Regex
# Return encoded image data
def encode_image():
    # Adapted from:
    # https://stackoverflow.com/a/41256900/8883485
    # https://stackoverflow.com/a/31410635/8883485
    # https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image
    ajax_call_data = request.values['imageString']  # Store string that's sent from Ajax call
    img_encoded = re.sub('^data:image/.+;base64,', '', ajax_call_data)
    return img_encoded


# -- Enhances Image --
# Sharpen Image
# Brighten Image
# Contrast Image
def enhance_image():
    convert_to_greyscale()
    resize_image()
    sharpen_image()
    brighten_image()
    contrast_image()


# -- Convert To Greyscale --
# Open image to convert
# Convert to greyscale
# Save image
def convert_to_greyscale():
    # Want to make transparent
    # Adapted from: https://stackoverflow.com/a/12201744/8883485
    img = Image.open('img_manipulation/digit_input.png').convert('L')
    img.save('img_manipulation/digit_input_grey.png')  # Save the greyscale image


# -- Make Transparent --
def make_transparent():
    img = Image.open('img.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("img2.png", "PNG")


# -- Image Fit --
# Open canvas sent image
# Re-Map image to dimensions 28 * 28
# Save image
def resize_image():
    # Adapted from: https://dev.to/preslavrachev/python-resizing-and-fitting-an-image-to-an-exact-size-13ic
    original_image = Image.open('img_manipulation/digit_input_grey.png')
    fit_and_resized_image = ImageOps.fit(original_image, DIM, Image.ANTIALIAS)
    fit_and_resized_image.save('img_manipulation/digit-28-28.png')


# -- Sharpen Image --
# Open image to manipulate
# Apply sharpen
# Set sharpen
# Enhance with sharpen
# Save image
def sharpen_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open('img_manipulation/digit-28-28.png')
    img = ImageEnhance.Sharpness(img)
    sharpness = 2
    sharp_img = img.enhance(sharpness)
    sharp_img.save('img_manipulation/sharp_img.png')  # Save the greyscale image


# -- Brighten image --
# Open image to manipulate
# Apply brighten
# Set brighten
# Enhance with brighten
# Save image
def brighten_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open('img_manipulation/sharp_img.png')
    img = ImageEnhance.Brightness(img)
    brightness = 1.0
    brightened_img = img.enhance(brightness)
    brightened_img.save('img_manipulation/bright_img.png')


# -- Contrast image --
# Open image to manipulate
# Apply contrast
# Set contrast
# Enhance with contrast
# Save image
def contrast_image():
    # Adapted from: https://dev.to/petercour/enhance-image-with-python-pil-222e
    img = Image.open('img_manipulation/bright_img.png')
    img = ImageEnhance.Contrast(img)
    contrast = 1.0
    contrast_img = img.enhance(contrast)
    contrast_img.save('img_manipulation/28-28.png')


# -- Reshape Image --
# Open image to convert
# Store as Array 28 * 28
# Return array
def reshape_image():
    # Adapted from: https://www.w3resource.com/numpy/manipulation/reshape.php
    img = Image.open('img_manipulation/28-28.png')
    digit_28_28_array = np.array(img).reshape(1, WIDTH, HEIGHT, 1)
    return digit_28_28_array


# -- App Run --
# Call to start application
if __name__ == '__main__':
    app.run()
