from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    input1 = request.form['input1']
    input2 = request.form['input2']
    input3 = request.form['input3']
    # Store the inputs locally
    with open('inputs.txt', 'a') as f:
        f.write(f'{input1}, {input2}, {input3}\n')
    return 'Form submitted successfully!'


