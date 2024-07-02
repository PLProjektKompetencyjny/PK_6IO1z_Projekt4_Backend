from flask import jsonify


class Response:
    @staticmethod
    def create(status: int, data: [dict], message: str = "") -> str:
        return jsonify({'code': status, 'code_message': message, 'data': data})
      
    @staticmethod
    def create_to_dict(status: int, data: [dict], message: str = "") -> str:
        return jsonify({'code': status, 'code_message': message, 'data': [d.to_dict() for d in data]})