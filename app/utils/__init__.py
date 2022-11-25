from flask import jsonify, request


class JsonRep:
    def __init__(self, data):
        self.data = data

    @classmethod
    def success(cls, data):
        return jsonify({
            'msg': 'success',
            'code': 200,
            'data': data
        })

    @classmethod
    def error(cls, data):
        return jsonify({
            'msg': 'error',
            'code': 500,
            'data': data
        })
