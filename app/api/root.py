from flask import redirect, render_template, request, url_for
from . import api


@api.route("/")
def index():
    return render_template('index.html')


@api.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name


@api.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number %d' % postID


@api.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number %f' % revNo


@api.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest


@api.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))
