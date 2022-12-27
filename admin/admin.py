from datetime import timedelta

from flask import Blueprint, render_template, request, url_for, redirect, flash, session, app

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
app.permanent_session_lifetime = timedelta(seconds=10)


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    return 'admin'


@admin.route('/login', methods=['POST', 'GET'])
def login():
    from main import get_db
    db = get_db()
    from dbpri import FDataBase
    dbase = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('addCommand'))
    elif request.method == 'POST':
        print(dbase.getUser())
        for item in dbase.getUser():
            if item['login'] == request.form['login'] and item['psw'] == request.form['psw']:
                session['userlogged'] = request.form['login']
                username = session['userlogged']
                print(username)
                return redirect(url_for('index'))
        else:
            print('Ошибка')
    return render_template('login.html', title='Авторизация', data=dbase.getUser())


@admin.route('/comands', methods=["POST", "GET"])
def addCommand():
    from main import get_db
    db = get_db()
    from dbpri import FDataBase
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name_of_comand']) > 1 and len(request.form['achivements']) > 2 and len(request.form['sostav']) > 2 and len(request.form['identif']) > 2:
            res = dbase.addCommand(request.form['name_of_comand'], request.form['achivements'], request.form['sostav'], request.form['identif'])
            if not res:
                flash('Ошибка добавления', category='error')
            else:
                flash('', category='success')
        else:
            flash('Ошибка добавления', category='error')
    return render_template('comands.html', menu=dbase.getMenu())

@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    # from main import get_db
    # db = get_db()
    # from dbpri import FDataBase
    # dbase = FDataBase(db)
    # dbase.addUser('admin', '123456')
    return redirect(url_for('.login'))