from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def sqlalchemy_error_to_dict(e):
    error_info = {
        "type": type(e).__name__,
        "message": str(e),
        "code": getattr(e, 'code', 'Unknown')
    }

    return jsonify({"error": error_info})
