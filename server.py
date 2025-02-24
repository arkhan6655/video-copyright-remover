import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return 'Welcome to the Video Copyright Remover App!'

# Favicon route to avoid 404 error
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content to suppress the error

# Upload route to handle POST request for video upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Add your video processing logic here using FFmpeg
        # For now, it's just a placeholder.
        print(f"File saved at {file_path}")
        
        # You can run FFmpeg commands to process the file here.
        
        return jsonify({'message': 'File uploaded and processed successfully!'}), 200
    else:
        return 'Invalid file type. Please upload an MP4 file.', 400

if __name__ == '__main__':
    # Ensure that the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Run Flask app
    app.run(debug=True)
