from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
CSV_FILE = 'uploads.csv'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Admin login route
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect(url_for('upload'))
        else:
            flash('Invalid Credentials')
    return render_template('admin_login.html')

# Upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data = {
            'branch': request.form['branch'],
            'year': request.form['year'],
            'regulation': request.form['regulation'],
            'semester': request.form['semester'],
            'subject': request.form['subject'],
            'file_type': request.form['file_type'],
            'unit': request.form.get('unit', ''),
            'exam_type': request.form.get('exam_type', ''),
            'month': request.form.get('month', '')
        }

        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            data['filepath'] = filename

            # Write data to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'branch', 'year', 'regulation', 'semester',
                    'subject', 'file_type', 'unit',
                    'exam_type', 'month', 'filepath'
                ])
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)

            flash('File uploaded successfully!')
            return redirect(url_for('upload'))

    return render_template('upload.html')

# Student portal – always show all uploaded files
@app.route('/student', methods=['GET', 'POST'])
def student_portal():
    files = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                files.append(row)
    return render_template('student.html', files=files)



if __name__ == '__main__':
    app.run(debug=True)
