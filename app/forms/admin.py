from wtforms import Form, PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from app.models.user import User


class SetPassword(Form):
    newpassword = PasswordField(validators=[DataRequired("密码不能为空"), Length(1, 36, "密码应小于36位")])
    renewpassword = PasswordField(validators=[EqualTo("newpassword", "两次输入的密码不一致"), Length(1, 36, "密码应小于36位")])


class AddUser(Form):
    username = StringField(validators=[DataRequired("用户名不能为空"), Length(1, 36, "用户名应小于36位")])
    password = PasswordField(validators=[DataRequired("密码不能为空"), Length(1, 36, "密码应小于36位")])
    repassword = PasswordField(validators=[EqualTo("password", "两次输入的密码不一致"), Length(1, 36, "密码应小于36位")])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已存在")
