from flask import render_template, current_app
from flask_login import login_required
from app import app


@app.route("/")
@login_required
def index():
    return render_template("index/index.html")


@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('imgs/favicon.ico')



