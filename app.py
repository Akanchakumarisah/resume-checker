from flask import Flask, render_template, request, jsonify
import os
from utils.file_handler import save_file, allowed_file
from utils.nlp_processor import analyze_resume

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
     
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if resume_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(resume_file.filename, ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX'}), 400
    
    try:
        # Save the uploaded file
        filename = save_file(resume_file, app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Analyze the resume
        analysis_result = analyze_resume(file_path, job_description)
        
        # Clean up - remove the uploaded file after analysis
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=10000)