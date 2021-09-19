from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file_and_render_target_prompt():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        
        # Extract column names
        df = pd.read_csv(uploaded_file.filename)
        column_names = list(df) # ['age', 'gender', 'chest_pain', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar_greater_than_120', 'resting_ecg_result', 'exercise_max_heart_rate', 'exercise_induced_angina', 'exercise_st_depression', 'exercise_st_slope', 'fluoroscopy_vessels_colored', 'thallium_stress_test', 'diagnosis']  
        data = [{"name": column} for column in column_names]
        return render_template("target_prompts.html", data=data, filename=uploaded_file.filename)
    return redirect(url_for('index'))


@app.route('/train', methods=['POST'])
def train():
    target = request.form.get('columns')
    filename = request.form.get('filename')

    print(target)
    print(filename)
    # Train the model
    output = os.system('tangram train --file {} --target {}'.format(filename, target))
    print(output)
    return redirect(url_for('index'))