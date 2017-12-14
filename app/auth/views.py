from flask import render_template, redirect, request, url_for, flash

from app import db
from . import auth
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user
from ..modles import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的用户名或者密码，请重新登录QAQ。')
    return render_template('auth/login.html', form=form)

@auth.route('/layout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登陆了QAQ！欢迎再来！')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data,
        email=register_form.email.data,
        password=register_form.password.data)
        db.session.add(user)
        flash('现在你可以登陆啦😘')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=register_form)