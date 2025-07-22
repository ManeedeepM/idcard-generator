from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Create Flask app instance
app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/generate', methods=['POST'])
def generate_id():
    name = request.form.get('name')
    college = request.form.get('college')
    email = request.form.get('email')
    photo = request.files.get('photo')

    filename = None
    if photo:
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

    return render_template('idcard.html', name=name, college=college, email=email, photo=filename)

# Serve uploaded images
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# Run locally
if __name__ == '__main__':
    app.run(debug=True)
