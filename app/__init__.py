import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import config


def make_celery(app):
    from celery import Celery
    from celery.schedules import crontab
    _celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    _celery.conf.timezone = "Asia/Shanghai"
    _celery.conf.beat_schedule = {
        'cut_log': {
            'task': 'app.libs.celery_tasks.cut_logs',
            'schedule': crontab(0, 0),
            'args': None
        },
    }

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    _celery.Task = ContextTask
    return _celery


app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
env_flask_config_name = os.getenv('FLASK_CONFIG') or "default"
print(env_flask_config_name)
app.config.from_object(config[env_flask_config_name])
login_manager.init_app(app)
login_manager.login_view = 'user.login'
login_manager.login_message = '不对游客开放，请登录'
celery = make_celery(app)


def init_db():
    from .models import db
    from app.models.user import User, Permission, Roles
    dbs = [
        Roles.query.get(1) or Roles(name="管理员", permission=0xff),
        Roles.query.get(2) or Roles(name="函证", permission=Permission.PERSONAL | Permission.CONFIRMATION),
        User.query.get(1) or User(username="admin", password="admin", role_id=1),
        User.query.get(2) or User(username="001", password="1111", role_id=2),
        User.query.get(3) or User(username="002", password="1111", role_id=2),
        User.query.get(4) or User(username="003", password="1111", role_id=2),
        User.query.get(5) or User(username="004", password="1111", role_id=2),
        User.query.get(6) or User(username="005", password="1111", role_id=2),
        User.query.get(7) or User(username="006", password="1111", role_id=2),
        User.query.get(8) or User(username="007", password="1111", role_id=2),
        User.query.get(9) or User(username="008", password="1111", role_id=2),
        User.query.get(10) or User(username="009", password="1111", role_id=2),
        User.query.get(11) or User(username="010", password="1111", role_id=2),
    ]
    db.session.add_all(dbs)
    db.session.commit()


@app.before_first_request
def init():
    from app.libs.navbar import init_nav
    from app.models import db
    app.jinja_env.auto_reload = True
    print("初始化数据库")
    db.create_all()
    init_db()
    print("初始化导航")
    init_nav()


def init_app():
    from .models import db
    db.init_app(app)
    from .views import register_blueprint
    register_blueprint(app)
    return app
