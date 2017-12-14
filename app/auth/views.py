from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm
from flask_login import login_user
from ..modles import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)