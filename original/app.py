import os
from flask import Flask, render_template, request, send_file, jsonify
from stegano.lsb import hide, reveal
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"

# Ensure directories exist
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files or "message" not in request.form or "key" not in request.form:
        return jsonify({"error": "Missing image, message, or key"}), 400

    image = request.files["image"]
    message = request.form["message"]
    key = request.form["key"]

    # Append key to message
    encrypted_message = f"{key}:{message}"

    input_path = os.path.join(UPLOAD_FOLDER, "original.png")
    image = Image.open(image)
    image = image.convert("RGB")  # Ensure correct format
    image.save(input_path, format="PNG")

    # Encrypt the message with the key
    output_path = os.path.join(ENCRYPTED_FOLDER, "encrypted.png")
    encrypted_image = hide(input_path, encrypted_message)
    encrypted_image.save(output_path, format="PNG")

    return jsonify({"message": "Encryption successful!", "image_url": "/download/encrypted"})

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files or "key" not in request.form:
        return jsonify({"error": "No image or key provided"}), 400

    image = request.files["image"]
    key = request.form["key"]
    
    image_path = os.path.join(UPLOAD_FOLDER, "uploaded.png")
    image.save(image_path)   

    try:
        hidden_message = reveal(image_path)
        if hidden_message and ":" in hidden_message:
            stored_key, message = hidden_message.split(":", 1)
            if stored_key == key:
                return jsonify({"message": message})
            else:
                return jsonify({"error": "Incorrect decryption key!"}), 403
        else:
            return jsonify({"error": "No hidden message found!"}), 400
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

# ✅ Added a route to serve the encrypted image
@app.route("/download/encrypted")
def download_encrypted():
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, "encrypted.png")
    if os.path.exists(encrypted_path):
        return send_file(encrypted_path, as_attachment=True)
    else:
        return jsonify({"error": "Encrypted file not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
