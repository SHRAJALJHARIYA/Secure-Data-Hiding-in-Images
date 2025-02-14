import os
from flask import Blueprint, request, jsonify
from stegano.lsb import hide
from PIL import Image

# Define blueprint
encryption_bp = Blueprint("encryption", __name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

@encryption_bp.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files or "message" not in request.form or "key" not in request.form:
        return jsonify({"error": "Missing image, message, or key"}), 400

    image = request.files["image"]
    message = request.form["message"]
    key = request.form["key"]

    # Append key to message
    encrypted_message = f"{key}:{message}"

    input_path = os.path.join(UPLOAD_FOLDER, "original.png")
    image = Image.open(image).convert("RGB")  # Ensure correct format
    image.save(input_path, format="PNG")

    # Encrypt message
    output_path = os.path.join(ENCRYPTED_FOLDER, "encrypted.png")
    hide(input_path, encrypted_message).save(output_path, format="PNG")

    return jsonify({"message": "Encryption successful!", "image_url": "/download/encrypted"})
