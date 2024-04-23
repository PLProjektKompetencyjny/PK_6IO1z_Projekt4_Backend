from flask import jsonify


class Response:
    @staticmethod
    def create(status: int, data: dict):
        return jsonify({'status': status, 'data': data})
