from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/compute', methods=['POST'])
def compute():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print("File saved at:", file_path)

    file_url = f"/images/{file.filename}"

    return jsonify({'file_url': file_url})

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
