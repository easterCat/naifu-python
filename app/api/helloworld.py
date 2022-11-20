from flask import render_template
from . import api


@api.route('/')
def root():
    return 'hello world!'


@api.route('/index')
def index():
    return render_template('login.html')


@api.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@api.route("/hello")
def hello_world():
    my_str = 'Hello Word'
    my_int = 10
    my_array = [3, 4, 2, 1, 7, 9]
    my_dict = {'name': 'xiaoming', 'age': 18}
    return render_template('hello.html',
                           my_str=my_str,
                           my_int=my_int,
                           my_array=my_array,
                           my_dict=my_dict)


@api.route("/world")
def world():
    my_int = 18
    my_str = 'curry'
    my_list = [1, 5, 4, 3, 2]
    my_dict = {'name': 'durant', 'age': 28}

    return render_template('hello.html',
                           my_str=my_str,
                           my_int=my_int,
                           my_list=my_list,
                           my_dict=my_dict)


@api.route('/flask')
def hello_flask():
    return 'Hello Flask'


@api.route('/python/')
def hello_python():
    return 'Hello Python'


@api.route('/admin')
def hello_admin():
    return 'Hello Admin'
