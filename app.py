from flask import (Flask, jsonify, render_template,
                   request, send_from_directory, redirect, url_for)
import os

app = Flask(__name__, static_folder='templates/react/build', static_url_path='/')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/play')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat')
def chat():
    return redirect(url_for('/'))


@app.route('/upload', methods=['POST'])
def upload_endpoint():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"message": "File successfully uploaded"}), 200
    else:
        return jsonify({"message": "Invalid file type"}), 400


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)# Set use_reloader to False to prevent multiple initializations
