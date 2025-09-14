from flask import Flask, render_template, request, jsonify, send_file
import os
import threading
from werkzeug.utils import secure_filename
import json

from ingest import process_pdf
from query import get_answer, get_key_points

app = Flask(__name__)
app.config['SECRET_KEY'] = 'researchpal-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process PDF in background thread
        def process_pdf_thread():
            try:
                process_pdf(filepath)
                # Clean up uploaded file
                os.remove(filepath)
            except Exception as e:
                print(f"Processing error: {e}")
        
        thread = threading.Thread(target=process_pdf_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'File uploaded and processing started'}), 200
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF'}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        answer = get_answer(question)
        return jsonify({'answer': answer}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/keypoints', methods=['GET'])
def get_keypoints():
    try:
        key_points = get_key_points()
        return jsonify({'key_points': key_points}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def check_status():
    # Check if database exists
    db_exists = os.path.exists('./chromadb')
    return jsonify({'db_ready': db_exists}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)