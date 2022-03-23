from flask_login import current_user
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError

__all__ = ["LoginForm", "ChangeForm"]

from app.models.user import User


class LoginForm(Form):
    username = StringField(validators=[DataRequired("用户名不能为空"), Length(1, 36, "用户名应小于36位")])
    password = PasswordField(validators=[DataRequired("密码不能为空"), Length(1, 36, "密码应小于36位")])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first().valid == 0:
            raise ValidationError("很抱歉，您已被管理员禁用，请联系管理员")


class ChangeForm(Form):
    password = PasswordField(validators=[DataRequired("密码不能为空"), Length(1, 36, "密码应小于36位")])
    newpassword = PasswordField(validators=[DataRequired("密码不能为空"), Length(1, 36, "密码应小于36位")])
    renewpassword = PasswordField(validators=[EqualTo("newpassword", "两次输入的密码不一致"), Length(1, 36, "密码应小于36位")])

    def validate_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError("密码错误")
