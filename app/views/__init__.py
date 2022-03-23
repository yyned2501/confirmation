from .user import app as user
# from .test import app as test
from .admin import app as admin
from .confirmation import app as confirmation


def register_blueprint(app):
    from .index import index
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(confirmation, url_prefix='/confirmation')
    # app.register_blueprint(test, url_prefix='/test')
