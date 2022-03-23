from flask import flash, current_app
from flask_login import UserMixin, AnonymousUserMixin, logout_user
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import DbBase


class User(UserMixin, DbBase):
    __tablename__ = "users"
    username = Column(String(64), unique=True, nullable=False)
    _password = Column("password", String(256), nullable=False)
    role = relationship("Roles")
    role_id = Column(Integer, ForeignKey("roles.id"))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def can(self, permission):
        return self.role is not None and (self.role.permission & permission) == permission

    def get_id(self):
        return self._password


@login_manager.user_loader
def get_user(_password):
    if _password == "None":
        return None
    user = User.query.filter(User._password == _password).first()
    if not user or user.valid == 0:
        return None
    return user


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return permission == 0 or permission == -1


login_manager.anonymous_user = AnonymousUser


class Permission:
    PERSONAL = 0b1
    CONFIRMATION = 0b10


class Roles(DbBase):
    __tablename__ = "roles"
    name = Column(String(64), nullable=False)
    permission = Column(Integer, nullable=False)
