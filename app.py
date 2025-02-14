import os
from flask import Flask, jsonify, render_template, send_file
from encryption import encryption_bp
from decryption import decryption_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(encryption_bp)
app.register_blueprint(decryption_bp)

ENCRYPTED_FOLDER = "encrypted"

@app.route("/")
def index():
    return render_template("index.html")

# ✅ Route to serve the encrypted image
@app.route("/download/encrypted")
def download_encrypted():
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, "encrypted.png")
    if os.path.exists(encrypted_path):
        return send_file(encrypted_path, as_attachment=True)
    return jsonify({"error": "Encrypted file not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
