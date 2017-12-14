from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..modles import User

# 定义登陆与注册表单类

class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登陆状态')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0, '用户名必须是字幕，数字，下划线，点，*和$')])
    password = PasswordField('请输入您的密码', validators=[
        DataRequired(), EqualTo('password2', message='两次输入的密码必须相同QAQ！')
    ])
    password2 = PasswordField('请再一次输入您的密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    """
    下面两个是自定义函数，用来验证输入的用户名和邮箱是否重复。
    在表单类中定义的以validate_ + 字段名的方法，这些方法就和常规的验证函数一起调用。
    即为自动在validators中运行"""

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('您输入的电子邮箱地址已经存在了。。。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('您输入的用户名已经存在了。。。')