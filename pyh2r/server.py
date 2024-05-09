import os
import shutil
from collections import deque
import time
import whisper
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the directory to store uploaded files
UPLOAD_DIR = 'uploaded_files'
# Define the maximum number of files to keep as logs
MAX_LOG_FILES = 100
# Initialize a deque to keep track of uploaded files
uploaded_files = deque(maxlen=MAX_LOG_FILES)

# Show the user a loading message while the model is being loaded
print("Loading model...")
start = time.time()
model = whisper.load_model("base")
print(f"Model loaded in {time.time() - start:.2f} seconds")

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is an audio file
    if file and allowed_file(file.filename):
        # Save the file to the upload directory
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(file_path)

        # Append the file path to the deque
        uploaded_files.append(file_path)

        # Process the audio file here (you can implement your own logic)
        start = time.time()
        read = model.transcribe(file_path, language="de")
        runtime = time.time() - start

        # For demonstration purposes, let's just return some basic information about the file
        file_info = {
            'filename': file.filename,
            'content_type': file.content_type,
            'file_size': len(file.read())
        }
        return jsonify({'file_info': file_info,
                        'runtime': runtime,
                        'read': read}), 200

    return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'ogg'}  # Add more file formats if needed

if __name__ == '__main__':
    app.run(debug=False)
