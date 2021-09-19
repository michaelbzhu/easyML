from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        output = os.system('tangram train --file {} --target diagnosis'.format(uploaded_file.filename))
        print(output)
        os.remove(uploaded_file.filename)
    return redirect(url_for('index'))