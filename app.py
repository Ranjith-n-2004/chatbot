import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

app = Flask(__name__)

# File Upload Config
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"}

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg", "")
    response = get_chat_response(msg)
    return response

def get_chat_response(text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(text)
        return response.text.strip()
    except Exception as e:
        return "Sorry, I couldn't process your request."

# Function to check file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Image Upload Route
@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        return jsonify({"image_url": file_path}), 200
    return jsonify({"error": "Invalid file type"}), 400

# Document Upload Route
@app.route("/upload_doc", methods=["POST"])
def upload_doc():
    if "document" not in request.files:
        return jsonify({"error": "No document provided"}), 400

    file = request.files["document"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Read text from document (if .txt)
        if filename.endswith(".txt"):
            with open(file_path, "r") as f:
                text = f.read()
            return jsonify({"text": text}), 200
        return jsonify({"document_url": file_path}), 200
    return jsonify({"error": "Invalid file type"}), 400

# Camera Capture Route
@app.route("/camera_search", methods=["POST"])
def camera_search():
    image_data = request.form.get("image")
    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # Here, you can integrate a Vision API for image processing
    return jsonify({"result": "Image received successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)