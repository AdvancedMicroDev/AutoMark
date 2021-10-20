# import torch
# import imghdr
# import os
# from flask import Flask, render_template, request, redirect, url_for, abort, \
#     send_from_directory
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['UPLOAD_PATH'] = 'C:/Users/narus/Documents/sketch2code_new/app/uploads'
#
#
# def validate_image(stream):
#     header = stream.read(512)
#     stream.seek(0)
#     format = imghdr.what(None, header)
#     if not format:
#         return None
#     return '.' + (format if format != 'jpeg' else 'jpg')
#
#
# @app.errorhandler(413)
# def too_large(e):
#     return "File is too large", 413
#
#
# @app.route('/')
# def index():
#     files = os.listdir(app.config['UPLOAD_PATH'])
#     return render_template('index.html', files=files)
#
#
# @app.route('/', methods=['POST'])
# def upload_files():
#     uploaded_file = request.files['file']
#     filename = secure_filename(uploaded_file.filename)
#     if filename != '':
#         file_ext = os.path.splitext(filename)[1]
#         if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
#                 file_ext != validate_image(uploaded_file.stream):
#             return "Invalid image", 400
#         uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#     return '', 204
#
#
# @app.route('/app/uploads/<filename>')
# def upload(filename):
#     return send_from_directory(app.config['UPLOAD_PATH'], filename)
#
#
# def load_model():
#     encoder = torch.load('model_weights/encoder_resnet34_0.061650436371564865.pt')
#     decoder = torch.load('model_weights/decoder_resnet34_0.061650436371564865.pt')
#     return encoder, decoder
###################################################################################################################
# <!doctype html>
# <html>
#
# <head>
#     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
#     <title>Upload new File</title>
# </head>
#
# <body>
#     <h1 class="display-3">Upload new File</h1>
#     <form>
#         <div class="input-group mb-3 ">
#             <input type="file" class="form-control" id="inputGroupFile02">
#             <label class="input-group-text" for="inputGroupFile02">Upload</label>
#         </div>
#         <div class="container py-3">
#             <div class="progress">
#                 <div class="progress-bar progress-bar-striped progress-bar-animated bg-success active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" id="load" style="width:0%"> 0% </div>
#             </div>
#             <input id="predict" class="btn btn-outline-success mt-2" type="submit" value="AutoMark">
#             <!--<button type="button" id="p1" class="btn btn-primary mt-2" autocomplete="off">OK</button>-->
#         </div>
#     </form>
# </body>
#
# </html>

# JS

# $('#predict').click(function() {

#     var timerId, percent;

#     // reset progress bar
#     percent = 0;
#     $('#predict').attr('disabled', true);
#     $('#load').css('width', '0px');
#     $('#load').addClass('progress-bar-striped active');

#     timerId = setInterval(function() {

#         // increment progress bar
#         percent += 5;
#         $('#load').css('width', percent + '%');
#         $('#load').html(percent + '%');


#         if (percent >= 100) {
#             clearInterval(timerId);
#             $('#predict').attr('disabled', false);
#             $('#load').removeClass('progress-bar-striped active');
#             $('#load').html('Prediction Successful!');
#         }
#     }, 200)
# })
###################################################################################################################

import os
from flask import Flask, request, redirect, url_for, send_from_directory, flash, render_template
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename
import numpy
from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable
from utils import *
from model import *
from inference.Compiler import *

UPLOAD_FOLDER = 'C:/Users/narus/Documents/be_prjt_files/app/uploads'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.secret_key = "super secret key"

js = Bundle('script.js', output='gen/main.js')
assets = Environment(app)
assets.register('main_js', js)


@app.route('/ping')
def hello():
    return 'Hello world!'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            encoder, decoder = load_model()
            star_text = '<START>'
            hidden = decoder.init_hidden()
            image = resize_img(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))
            image = Variable(torch.FloatTensor([image]))
            predicted = '<START> '
            for di in range(9999):
                sequence = id_for_word(star_text)
                decoder_input = Variable(torch.LongTensor([sequence])).view(1, -1)
                features = encoder(image)
                outputs, hidden = decoder(features, decoder_input, hidden)
                topv, topi = outputs.data.topk(1)
                ni = topi[0][0][0]
                word = word_for_id(ni)
                if word is None:
                    continue
                predicted += word + ' '
                star_text = word
                print(predicted)
                if word == '<END>':
                    break
            compiler = Compiler('default')
            compiled_website = compiler.compile(predicted.split())

            return compiled_website
    return render_template('index_old.html')


def load_model():
    encoder = torch.load('C:/Users/narus/Documents/be_prjt_files/encoder_resnet34_tensor(0.0820).pt')
    decoder = torch.load('C:/Users/narus/Documents/be_prjt_files/decoder_resnet34_tensor(0.0820).pt')
    return encoder, decoder


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
           in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
