from flask import jsonify


class Response:
    @staticmethod
    def create(status: int, data: [dict], message: str = ""):
        return jsonify({'code': status, 'code_message': message, 'data': data})
