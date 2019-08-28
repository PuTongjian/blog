from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from app.libs.redprint import RedPrint
from app.libs.cahce import cache
from app.forms import LoginForm
from app.models import Manager

views = RedPrint('manager')


@views.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        manager = Manager.login(email=form.email.data, password=form.password.data)
        remember = form.remember_me.data
        login_user(manager, remember=remember)

        next = request.args.get('next')
        return redirect(next or url_for('views.index'))
    return render_template('login.html', form=form)


@views.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    cache.delete('article_editor')
    return redirect(url_for('views.index'))


@views.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    pass


