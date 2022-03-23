import datetime
from shutil import move
from os import path, makedirs

from celery import group
from celery.result import allow_join_result
from pdfkit import from_url, configuration
import zipfile

from app import celery


@celery.task
def mk_pdf(url, cookies, path):
    options = {"cookie": [(c, cookies.get(c)) for c in cookies],
               "footer-center": "[page]/[topage]",
               "margin-top": "20mm",
               "margin-bottom": "20mm",
               "footer-font-size": 9,
               "footer-font-name": "STSongTi"}
    from_url("http://localhost:5002" + url, path, options=options)
    return f"{path}生成完毕"


@celery.task
def mk_zip_and_pdf(co_id, files, mk_pdf_args_list):
    r = group([mk_pdf.s(*mk_pdf_args) for mk_pdf_args in mk_pdf_args_list])()
    with allow_join_result():
        r.get()
    with zipfile.ZipFile("app/static/zip/{}.zip".format(co_id), "w") as z:
        n = 0
        for f in files:
            n += 1
            z.write(f, str(n) + "_" + f.split("/")[-1][len(str(co_id)) + 1:])
    return "zip打包完毕"


@celery.task
def cut_logs():
    print("cut_logs")
    PATH = "/root/confirmation"
    makedirs(path.join(PATH, "logs"), exist_ok=True)
    move(path.join(PATH, "server.log"),
         path.join(PATH, "logs", "uwsgi_" + datetime.datetime.now().strftime('%Y-%m-%d') + ".log"))
    move(path.join(PATH, "celery.log"),
         path.join(PATH, "logs", "celery_" + datetime.datetime.now().strftime('%Y-%m-%d') + ".log"))
    open(path.join(PATH, "touchforlogrotat"), "w").close()
    open(path.join(PATH, "celery.log"), "w").close()
