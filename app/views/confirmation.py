# coding=utf-8
from time import time

from flask import render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import current_user

from app.libs.navbar import Blueprint
from app.libs.permission import permission_required, user_permission
from app.models.confirmation import ConfirmationLink, ConfirmationData
from app.models.user import Permission

app = Blueprint("confirmation", __name__)


@app.route("/view/<co_id>/<bank_id>")
@user_permission
def view(co_id, bank_id):
    c = ConfirmationLink.query.get(co_id)
    return render_template("confirmation/confirmation.html", data=c, bank_id=int(bank_id))


@app.route("/index")
@app.nav("函证系统.银行询证函", permission=Permission.CONFIRMATION)
def index():
    c = current_user.confirmations
    return render_template("confirmation/confirmation_index.html", data=c)


@app.route("/delete_co/<co_id>")
@user_permission
def delete_co(co_id):
    c = ConfirmationLink.query.get(co_id)
    c.delete()
    return redirect(url_for("confirmation.index"))


@app.route("/co/<co_id>")
@user_permission
def co(co_id):
    c = ConfirmationLink.query.get(co_id)
    for cm in c.data:
        if isinstance(cm.data, list):
            cm.data = {"add_none": False, "display_schedule": False, "data": cm.data}
    c.commit()
    return render_template("confirmation/company.html", data=c)


@app.route("/upload", methods=["POST"])
@permission_required(Permission.CONFIRMATION)
def upload():
    if request.method == "POST":
        c = ConfirmationLink()
        f = request.files.get("file")
        c.upload(f, request.cookies)
        return redirect(url_for("confirmation.index"))


@app.route("/pdf/<co_id>/<bank_id>")
@user_permission
def pdf(co_id, bank_id):
    c = ConfirmationData.query.filter_by(no_id=bank_id, link_id=co_id).first()
    return redirect(url_for("static", filename=c.pdf_path, time=int(time())))


@app.route("/download/<co_id>")
@user_permission
def download(co_id):
    c = ConfirmationLink.query.get(co_id)
    return send_from_directory(r"static/zip/", filename="{}.zip".format(co_id), as_attachment=True,
                               attachment_filename="{}_{}.zip".format(c.co, c.period))


@app.route("/re_mk/<co_id>")
@user_permission
def re_mk(co_id):
    c = ConfirmationLink.query.get(co_id)
    c.mk(request.cookies)
    return "正在重新生成"


@app.route("/templates")
@app.nav("函证系统.模板下载", Permission.CONFIRMATION)
def templates():
    return send_from_directory(r"static", path="银行询证函上传模板.xlsx", as_attachment=True,
                               attachment_filename="银行询证函上传模板.xlsx")


@app.route("/clean")
@app.nav("函证系统.清理文件", 0xff)
def clean():
    ConfirmationLink.clean()
    ConfirmationData.clean()
    return redirect(url_for("confirmation.index"))


@app.route("/change_data/<co_id>", methods=["POST"])
def change_data(co_id):
    c = ConfirmationLink.query.get(co_id)
    c.basic = request.form
    c.co = c.basic.get("被审计单位")
    c.period = c.basic.get("年度（或期间）")
    c.commit()
    return "已保存"


@app.route("/add_none/<co_id>/<bank_id>")
def add_none(co_id, bank_id):
    c = ConfirmationData.query.filter(ConfirmationData.link_id == co_id, ConfirmationData.no_id == bank_id).first()
    data = c.data
    data["add_none"] = not data["add_none"]
    c.data = data
    c.commit()
    return jsonify({"status": c.data["add_none"]})


@app.route("/display_schedule/<co_id>/<bank_id>")
def display_schedule(co_id, bank_id):
    c = ConfirmationData.query.filter(ConfirmationData.link_id == co_id, ConfirmationData.no_id == bank_id).first()
    data = c.data
    if "display_schedule" not in data:
        data["display_schedule"] = False
    data["display_schedule"] = not data["display_schedule"]
    c.data = data
    c.commit()
    return jsonify({"status": c.data["display_schedule"]})


@app.route("/pay_bank/<co_id>/<bank_id>")
def set_pay_bank(co_id, bank_id):
    c = ConfirmationData.query.filter(ConfirmationData.link_id == co_id, ConfirmationData.no_id == bank_id).first()
    pay_bank = request.args.get("select_bank")
    if pay_bank == "other":
        pay_bank = request.args.get("other_bank")
    data = c.data
    data["pay_bank"] = pay_bank
    c.data = data
    c.commit()
    return jsonify({"status": c.data["pay_bank"]})
