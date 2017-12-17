from flask import render_template, redirect, request, url_for, flash
from ..email import send_email
from app import db
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetEmailForm, ResetPasswordForm, PasswordResetRequestForm
from flask_login import login_user, login_required, logout_user, current_user
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


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登陆了QAQ！欢迎再来！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data,
        password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('一封确认邮件已经发送到您的注册邮箱了。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经验证了您的账户，谢谢！')
    else:
        flash('这个验证链接是错误的或者是过期的。')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '验证邮件', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的验证邮件已经发送到您的邮箱地址。')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=('GET', 'POST'))
@login_required
def change_password():
    if not current_user.confirmed:
        flash('请先验证您的邮箱。')
        return redirect(url_for('auth.unconfirmed'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            # 此处的current_user即为User类的实例，所以可以直接修改提交
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('您的密码已经修改成功了')
        else:
            flash('您输入的原来密码不正确')
    return render_template('auth/changepassword.html', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # 确认当时的一定处于未登陆的匿名状态
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置密码', 'auth/email/reset_password',
                       user=user, token=token, next=request.args.get('next'))
        flash('一封重置密码的邮件已经发送到您的邮箱了，请查收。')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    # 确定匿名状态
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.new_password1.data):
            db.session.commit()
            flash('您的密码已经更新，请重新登陆。')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)



@auth.route('/change_email_request', methods=('GET', 'POST'))
@login_required
def change_email_request():
    form = ResetEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认您的邮箱地址', 'auth/email/change_email', user=current_user, token=token)
            flash('一封确认邮件已经发送到您的邮箱了，请确认。')
            return redirect(url_for('main.index'))
        else:
            flash('您输入的邮箱地址或者密码不正确')
    return render_template('auth/changeemail.html', form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('您已经成功修改了电子邮箱地址')
    else:
        flash('无效的请求')
    return redirect(url_for('main.index'))

