import os
import subprocess
import time
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

# Enable CORS for the frontend domain
CORS(app, origins=["https://video-copyright-remover.vercel.app"])

# Setup basic logging to capture incoming requests and other logs
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request():
    logging.debug(f"Received request: {request.method} {request.url}")

@app.route('/upload', methods=['POST'])
def upload_video():
    logging.debug("Starting video upload process...")

    # Check if the request contains a file
    if 'file' not in request.files:
        logging.error("No file part in the request.")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        logging.error("No selected file.")
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        logging.debug("Created 'uploads' directory.")

    # Save the uploaded file
    input_file = os.path.join("uploads", file.filename)
    file.save(input_file)
    logging.debug(f"File saved as {input_file}")

    # Set the output file name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join("uploads", f"output_{timestamp}.mp4")
    logging.debug(f"Output file set to {output_file}")

    # FFmpeg command to process the video
    ffmpeg_command = [
        'ffmpeg', '-i', input_file, output_file
    ]
    logging.debug(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")

    try:
        subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
        logging.debug(f"FFmpeg processed the video successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg processing failed: {e.stderr.decode()}")
        return jsonify({'error': 'FFmpeg processing failed', 'details': e.stderr.decode()}), 500

    return jsonify({'message': 'File processed successfully', 'output': output_file})

if __name__ == '__main__':
    app.run(debug=True)
