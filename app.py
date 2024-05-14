import time

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import model
import helper
import constants
import os

app = Flask(__name__)

app = Flask(__name__)
app.jinja_env.cache = {}
app.secret_key = "eqwnbadflajdfkvczvxmnoui"
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_CONTENT_LENGTH

isInit = False

if isInit is False:
    model.init_model()
    isInit = True

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def resolve_request():
    tab_type = request.args.get("tab")

    if tab_type == 'File':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        file_names = []

        for file in files:
            if file and helper.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif')
                return redirect(request.url)

        for item in file_names:
            helper.predict_image(constants.UPLOAD_FOLDER + item, name=item)

        return render_template('home.html', filenames=file_names)
    else:
        download_status = helper.read_image_from_url(request.form.get('url'))
        time.sleep(1)
        if download_status == 'SUCCESS':
            helper.predict_image(constants.SAVE_PATH)
        return render_template('home.html', download_status=download_status)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    # CUSTOM HOST IP HERE
    app.run(host="0.0.0.0", debug=True, port=5001, threaded=True)
