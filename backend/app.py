from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            photo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# API to upload form data and image
@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    department = request.form['department']
    photo = request.files['photo']

    # Save image securely
    filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(photo_path)

    # Save data to SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, department, photo) VALUES (?, ?, ?)",
              (name, department, filename))
    conn.commit()
    conn.close()

    return jsonify({
        'name': name,
        'department': department,
        'photo_url': f'/uploads/{filename}'
    })

# Serve uploaded image files
@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Homepage test route
@app.route('/')
def home():
    return "✅ Flask backend is running!"

# Run the server
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
