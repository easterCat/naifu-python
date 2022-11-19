from flask import render_template, request
from . import api


@api.route('/student')
def student():
    return render_template('student.html')


@api.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)
