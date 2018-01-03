from flask_pagedown.fields import PageDownField
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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
    email = StringField('邮箱地址', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
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

# 定义修改密码的类
class ChangePasswordForm(Form):
    old_password = PasswordField('请输入您原来的密码：', validators=[DataRequired()])
    new_password = PasswordField('请输入您新的密码：', validators=[DataRequired()])
    submit = SubmitField('修改密码')

# 定义重置密码时输入电子邮箱的类
class PasswordResetRequestForm(Form):
    email = StringField('邮箱地址', validators=[DataRequired(), Email(), Length(1, 64)])
    submit = SubmitField('提交')

# 定义重置密码的类
class ResetPasswordForm(Form):
    new_password1 = PasswordField('请输入您的新密码：', validators=[DataRequired(),\
                                  EqualTo('new_password2', message='两次输入的密码要一致！')])
    new_password2 = PasswordField('请再次输入您的密码：', validators=[DataRequired()])
    submit = SubmitField('重置密码')

# 定义修改电子邮箱地址的类
class ResetEmailForm(Form):
    email = StringField('请输入您新的电子邮箱地址：', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('请输入您的密码', validators=[DataRequired()])
    submit = SubmitField('修改电子邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('这个电子邮箱地址已经存在了。')

# 博客文章表单
class PostForm(Form):
    body = PageDownField('你想写的是什么？', validators=[DataRequired()])
    submit = SubmitField('提交')

