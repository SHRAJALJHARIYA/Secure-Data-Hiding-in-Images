import os
from flask import Blueprint, request, jsonify
from stegano.lsb import reveal

# Define blueprint
decryption_bp = Blueprint("decryption", __name__)

UPLOAD_FOLDER = "uploads"

# Ensure directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@decryption_bp.route("/decrypt", methods=["POST"])
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
            return jsonify({"error": "Incorrect decryption key!"}), 403
        return jsonify({"error": "No hidden message found!"}), 400
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500
