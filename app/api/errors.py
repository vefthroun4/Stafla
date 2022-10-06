from flask import jsonify

def resource_not_found(message):
    response = jsonify({"error": "resource not found", "message": message})
    response.status_code = 404
    return response

def unauthorised(message):
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = 401 
    return response

def forbidden(message): 
    response = jsonify({"error": "forbidden", "message": message})
    response.status_code = 403
    return response