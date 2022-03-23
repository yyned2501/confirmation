from flask import render_template, url_for, request, redirect, flash
from pdfkit import from_url

from app.forms.admin import SetPassword, AddUser
from app.libs.navbar import Blueprint
from app.libs.permission import permission_required
from app.models.user import User

app = Blueprint("admin", __name__)


@app.route("/users")
@app.nav("管理.用户管理", 0xff)
def users():
    u = User.query.filter(User.role_id != 1).all()
    return render_template("admin/users.html", users=u)


@app.route("/setpassword/<user_id>")
@permission_required(0xff)
def setpassword(user_id):
    user = User.query.get(user_id)
    user.password = "1111"
    user.commit()
    return "用户{}密码已恢复".format(user.username)


@app.route("/delete/<user_id>")
@permission_required(0xff)
def delete(user_id):
    user = User.query.get(user_id)
    user.delete()
    return render_template("admin/user.html", user=user)


@app.route("/restore/<user_id>")
@permission_required(0xff)
def restore(user_id):
    user = User.query.get(user_id)
    user.restore()
    return render_template("admin/user.html", user=user)


@app.route("/add_user", methods=["GET", "POST"])
@permission_required(0xff)
def add_user():
    if request.method == "POST":
        form = AddUser(request.form)
        if form.validate():
            user = User()
            user.set_form(form)
            user.role_id = 2
            user.add()
            flash("新增用户{}成功".format(user.username))
            return redirect(url_for("admin.users"))
    else:
        form = {}
    return render_template("admin/add_user.html", form=form)
