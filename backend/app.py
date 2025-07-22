from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Create the Flask app
app = Flask(__name__)

# Folder for uploaded photos
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Form submission and ID generation
@app.route('/generate', methods=['POST'])
def generate_id():
    name = request.form.get('name')
    email = request.form.get('email')
    college = request.form.get('college')
    photo = request.files.get('photo')

    filename = None
    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('idcard.html', name=name, email=email, college=college, photo=filename)

# Redirect to uploaded image
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# Note: No need for `if __name__ == '__main__'` when using gunicorn
