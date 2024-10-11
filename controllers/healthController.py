from flask import jsonify

def health_check():
    return jsonify({"status": "API is running"}), 200
