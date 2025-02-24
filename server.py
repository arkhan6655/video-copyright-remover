import os
import subprocess
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all domains (or specify your frontend domain)
CORS(app, origins=["https://video-copyright-remover.vercel.app"])

@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Save the uploaded file
    input_file = os.path.join("uploads", file.filename)
    file.save(input_file)

    # Set the output file name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join("uploads", f"output_{timestamp}.mp4")

    # FFmpeg command to process the video
    ffmpeg_command = [
        'ffmpeg', '-i', input_file, output_file
    ]

    try:
        subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'FFmpeg processing failed', 'details': e.stderr.decode()}), 500

    return jsonify({'message': 'File processed successfully', 'output': output_file})

if __name__ == '__main__':
    app.run(debug=True)
