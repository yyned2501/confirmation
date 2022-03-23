from flask import render_template, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect

from app.models.user import User, Permission
from app.forms.user import *
from app.libs.navbar import Blueprint

app = Blueprint("user", __name__)
app.add_app_template_global(current_user, 'current_user')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('user/login.html', form=form)


@app.route("/data", methods=["GET"])
@app.nav("个人中心.资料", permission=Permission.PERSONAL)
@login_required
def data():
    return render_template('user/data.html', user=current_user)


@app.route("/change_password", methods=["GET", "POST"])
@app.nav("个人中心.修改密码", permission=Permission.PERSONAL)
@login_required
def change_password():
    form = ChangeForm(request.form)
    if request.method == "POST":
        if form.validate():
            current_user.password = form.newpassword.data
            current_user.commit()
            flash("您的密码已修改")
            return redirect(url_for("user.data"))
    return render_template('user/change_password.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
