from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        face_id = request.form['face_id']
        face_name = request.form['face_name']
        subprocess.run(['python', 'create_and_train.py'], input=f'{face_id}\n{face_name}\n'.encode())
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/attendance')
def attendance():
    subprocess.run(['python', 'recognize.py'])
    return redirect(url_for('index'))

@app.route('/show_attendance')
def show_attendance():
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f'firebase/attendance_files/attendance{current_date}.xls'
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        data = df.to_html(classes='table table-striped', index=False)
        return render_template('attendance.html', tables=[data], current_date=current_date)
    else:
        return render_template('attendance.html', tables=["<p>No attendance file found for today.</p>"], current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)
