from flask import Flask, request, render_template
from datetime import datetime
import extractPrereqs

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/opticourse.html', methods=['GET', 'POST'])
def opticourse():
    if request.method == 'POST':
            
        college = request.form['college']
        dept = request.form['dept']
        major = request.form['major']
        minor = request.form['minor']
        techBreadth = request.form['techbreadth']
        artsHumSubGroup = request.form['artsHumSubGroup']
        sciInqSubGroup = request.form['sciInqSubGroup']
        socCultSubGroup = request.form['socCultSubGroup']
        topicElective = request.form['topicElective']
        numberQuarters = request.form['numberQuarters']
        topicGE = request.form['topicGE']
        easy = request.form['easy']

        tabledata = [['Name', 'Age', 'Gender'],
            ['John', '25', 'Male'],
            ['Jane', '30', 'Female'],
            ['Bob', '35', 'Male'],
            ['Alice', '40', 'Female']]

        
        with open('myinputs.txt', 'a') as f:
            f.write(f"{college},{dept},{minor},{minor},{techBreadth},{artsHumSubGroup},{sciInqSubGroup},{socCultSubGroup},{topicElective},{numberQuarters},{topicGE},{easy},{current_time}\n")

        return 'Inputs saved successfully!' + " " + str(extractPrereqs.extractPrereqs("course 100 or 110", "EC ENGR")) + " " + str(extractPrereqs.fat)
    
    return render_template('opticourse.html')


    

if __name__ == '__main__':
    app.run(debug=True)
