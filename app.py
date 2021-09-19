from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        
        # Extract column names
        df = pd.read_csv(uploaded_file.filename)
        column_names = list(df) # ['age', 'gender', 'chest_pain', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar_greater_than_120', 'resting_ecg_result', 'exercise_max_heart_rate', 'exercise_induced_angina', 'exercise_st_depression', 'exercise_st_slope', 'fluoroscopy_vessels_colored', 'thallium_stress_test', 'diagnosis']  

        # Train the model
        output = os.system('tangram train --file {} --target diagnosis'.format(uploaded_file.filename))
        print(output)
        os.remove(uploaded_file.filename)
    return redirect(url_for('index'))