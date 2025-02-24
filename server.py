from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

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

    # Save the uploaded file
    video_path = os.path.join("uploads", file.filename)
    file.save(video_path)

    # Now you can process the video file (using FFmpeg or any other logic you have)
    output_file = "output_" + file.filename
    ffmpeg_command = [
        'ffmpeg', '-i', video_path, output_file
    ]
    subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return jsonify({'message': 'File processed successfully', 'output': output_file})

if __name__ == '__main__':
    app.run(debug=True)
