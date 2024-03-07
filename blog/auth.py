from flask import Blueprint, request, redirect, session, url_for, flash, render_template, get_flashed_messages
from utils.db_utils import get_session
from werkzeug.security import check_password_hash
from functools import wraps
from models import Users

login_bp = Blueprint('login_endpoints', __name__, template_folder='templates/auth')


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for('login_endpoints.login'))

    return wrapped_view


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('auth.html', messages=messages)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_session()

        user_data = conn.query(Users).filter(Users.username == username).first()

        if user_data:
            hashed_password = user_data.password

            if check_password_hash(hashed_password, password):
                session['user_id'] = user_data.id
                session['username'] = user_data.username
                return redirect(url_for('admin'))

        flash('błędna nazwa użytkownika lub hasło')
        return redirect(url_for('login_endpoints.login'))


@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Wylogowano!')
    return redirect(url_for('index'))
