from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
import csv 

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
    df = pd.read_csv(filename)
    column_names = list(df)
    column_names.remove(target)
    inputs = [{"name": input} for input in column_names]
    output = os.system('tangram train --file {} --target {}'.format(filename, target))
    print(output)
    return render_template("evaluate.html", inputs=inputs, filename=filename, target=target)


def make_csv(cols, rows, test_csv_filename):
    # writing to csv file 
    with open(test_csv_filename, 'w+') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the cols 
        csvwriter.writerow(cols) 
            
        # writing the data rows
        csvwriter.writerows(rows)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    filename = request.form.get('filename')
    target = request.form.get('target')
    df = pd.read_csv(filename)
    column_names = list(df)
    column_names.remove(target)
    input_parameters = column_names
    user_inputs = []
    for input in input_parameters:
        user_inputs.append(request.form.get(input))

    user_inputs = [user_inputs]

    print(input_parameters)
    print(user_inputs)

    test_csv_filename = filename[:-4] + "_test.csv"
    print(test_csv_filename)
    csv = make_csv(input_parameters, user_inputs, test_csv_filename)
    output = os.system('tangram predict --model {}.tangram --file {} --output output.csv'.format(filename[:-4], test_csv_filename))
    print(output)

    df = pd.read_csv('output.csv')
    output_column = list(df)[0]
    solution = df.iloc[0][0]
    print("Here is the output_column:")
    print(output_column)
    print("Here is the solution (final classification):")
    print(solution)
    return render_template("output.html", output_column=output_column, solution=solution)

