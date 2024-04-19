import os
# import magic
import urllib.request

from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename
import cherrypy
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


UPLOAD_FOLDER = 'C:/uploads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('test.html')


@app.route('/python-flask-files-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    s1 = ''
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    value={}
    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pages = convert_from_path(''+UPLOAD_FOLDER+ '/' + filename, dpi=200,
                                      poppler_path='C:/Program Files/poppler-0.68.0/bin')
            print(pages)
            for idx, page in enumerate(pages):
                # print(idx)
                page.save(''+UPLOAD_FOLDER+'/'+filename+ str(idx) + '.jpg', 'JPEG')
                #page.save('' + UPLOAD_FOLDER + '/' + 'sorce' + str(idx) + '.jpg', 'JPEG')
            pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ganshyam.vyas\AppData\Local\Tesseract-OCR\tesseract.exe"
            soucecontent = []
            for i in range(idx + 1):
                # print(i)
                # print("I like")
                soucecontent.append(Image.open(''+UPLOAD_FOLDER+ '/'+filename+ str(i) + '.jpg'))

            print(soucecontent)

            for s in soucecontent:
                print(s)
                s1 = s1 + pytesseract.image_to_string(s, lang='eng')
            print(s1)
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 206
            return resp
        if success:
            resp = jsonify({'message': s1})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp




if __name__ == "__main__":
    app.run(threaded=True,port=9090,host="192.168.1.71")