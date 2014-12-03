from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user

from ..utils.decorators import render_to
from ..forms.auth import LoginForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('POST', 'GET'))
@render_to('auth/login.html')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        return redirect(url_for('dashboard.home'))
    return {'form': form}


@auth.route('/logout', methods=('GET',))
def logout():
    logout_user()
    return redirect('/login')
