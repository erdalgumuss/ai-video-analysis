from flask import jsonify

def handle_404(error):
    response = jsonify({"error": "Resource not found"})
    response.status_code = 404
    return response

def handle_500(error):
    response = jsonify({"error": "Internal server error"})
    response.status_code = 500
    return response
