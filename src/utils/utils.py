from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def sqlalchemy_error_to_dict(e):
    error_info = {
        "type": type(e).__name__,
        "message": str(e),
        "code": getattr(e, 'code', 'Unknown')
    }

    return jsonify({"error": error_info})
