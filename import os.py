from flask import Flask, request, jsonify, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"zpl"}  # Nur ZPL-Dateien sollten erlaubt sein
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔥 Sicherheitslücke: Kein Schutz gegen gefährliche Dateiendungen!
def is_allowed_file(filename):
    return "." in filename  # ❌ Unsicher: Akzeptiert ALLE Dateiendungen!

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Keine Datei gesendet"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Leerer Dateiname"}), 400

    # 🔴 Keine Dateiendungsprüfung!
    filename = file.filename  
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    file.save(file_path)  # Speichert die Datei ungeprüft
    
    print(f"✅ Datei gespeichert: {file_path}")
    return jsonify({"message": "Datei hochgeladen", "filename": filename}), 200

# 🔥 Sicherheitslücke: Direkte Ausführung der Datei möglich!
@app.route("/execute", methods=["POST"])
def execute_file():
    data = request.json
    filename = data.get("filename")
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "Datei nicht gefunden"}), 404
    
    # ⚠ Unsicher: Führt beliebige Dateien direkt aus!
    result = subprocess.run(file_path, shell=True, capture_output=True, text=True)  
    return jsonify({"output": result.stdout, "error": result.stderr})

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Datei nicht gefunden"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
