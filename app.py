import io
import json
import base64
from flask import Flask, request
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator


app = Flask(__name__,)
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'


def translate(text, target_language):

    translated = GoogleTranslator(
        source='auto', target=target_language).translate(text)

    return translated


@app.route('/all_languages', methods=['POST', "GET"])
def get_languages():

    return json.dumps(GoogleTranslator().get_supported_languages())


@app.route('/image', methods=['POST', "GET"])
def predict_with_image():

    if request.method == "POST":

        encodedImg = request.form.get('file')
        target_language = request.form.get('target_lan')

        imgdata = base64.b64decode(encodedImg)

        imageStream = io.BytesIO(imgdata)

        imageFile = Image.open(imageStream)

        imageFile = imageFile.resize((600, 360))

        text = pytesseract.image_to_string(
            imageFile, config=tessdata_dir_config)

        if text == "":
            return json.dumps(None)

        translated = translate(text, target_language)

        return json.dumps(translated)

    return 'Ok'


@app.route('/text', methods=['POST', "GET"])
def predict_with_text():

    if request.method == "POST":

        text = request.form.get('text')

        target_language = request.form.get('target_lan')

        translated = translate(text, target_language)

        return json.dumps(translated)

    return 'Ok'


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
