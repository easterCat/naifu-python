from flask import redirect, request, session, url_for
from . import api


@api.route("/home")
def home():
    if 'username' in session:
        username = session['username']
        return '登录用户名是:' + username + '<br>' + \
               "<b><a href = '/logout'>点击这里注销</a></b>"
    return "您暂未登录， <br><a href = '/login'></b>" + \
           "点击这里登录</b></a>"


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '''
<form action = "" method = "post">
    <p><input type="text" name="username"/></p>
    <p><input type="submit" value ="登录"/></p>
</form>
'''


@api.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
