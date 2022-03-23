from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


class DbBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    valid = Column(Integer, default=1)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def date(self):
        return self.update_time.strftime("%Y年%m月%d日")

    def delete(self):
        self.valid = 0
        db.session.commit()

    def restore(self):
        self.valid = 1
        db.session.commit()

    def deep_delete(self):
        db.session.delete(self)

    def set_attr(self, attrs):
        for k, v in attrs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def set_form(self, form):
        for k, v in vars(form).items():
            if hasattr(self, k):
                setattr(self, k, v.data)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            pass

    @staticmethod
    def commit():
        db.session.commit()

    @classmethod
    def add_all(cls, list_self):
        db.session.add_all(list_self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def add_no_commit(self):
        try:
            db.session.add(self)
        except IntegrityError:
            pass

    def __repr__(self):
        ret_pr = str(self.to_dict())
        return ret_pr
