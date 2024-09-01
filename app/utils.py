from flask import jsonify


def create_response(data=None, message=None, status=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), status
