from flask import Flask, request, jsonify, send_file
import os
import subprocess
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to Video Copyright Remover API!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, f"output_{time.strftime('%Y%m%d-%H%M%S')}.mp4")
    file.save(input_path)

    # FFmpeg Command to Process Video
    command = [
        "ffmpeg", "-i", input_path,
        "-vf", "scale=in_w:in_h, eq=brightness=0.02:contrast=1.1",
        "-c:v", "libx265", "-preset", "medium", "-crf", "28",
        "-c:a", "aac", "-y", output_path
    ]
    
    subprocess.run(command)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
