import json
import os

from flask import url_for
from flask_login import current_user

from sqlalchemy import Column, String, ForeignKey, Integer, Text, Boolean, desc
from sqlalchemy.orm import relationship, backref

from app.libs.celery_tasks import mk_zip_and_pdf, mk_pdf
from app.models.base import DbBase
from app.libs.confirmation import Confirmation

PATH = "app/static/"


class ConfirmationLink(DbBase):
    user = relationship("User", backref=backref("confirmations", order_by=desc("update_time")))
    co = Column(String(64))
    period = Column(String(64))
    _basic = Column("basic", Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    @property
    def basic(self):
        return json.loads(self._basic)

    @basic.setter
    def basic(self, obj):
        self._basic = json.dumps(obj, ensure_ascii=False)

    def upload(self, f, cookies):
        '''
        上传文件并生成pdf打包zip

        :param f: flask.request.files
        :param cookies: flask.request.cookies
        :return: None
        '''
        os.makedirs(PATH + "pdf", exist_ok=True)
        os.makedirs(PATH + "zip", exist_ok=True)
        path = PATH + "tmp_" + f.filename
        f.save(path)
        c = Confirmation(path)
        os.remove(path)
        self.co = c.basic.get("被审计单位")
        self.period = c.basic.get("年度（或期间）")
        self.basic = c.basic
        self.user = current_user
        self.add()
        data = []
        for i in c.data:
            path = "pdf/" + "{}_{}_{}_{}.pdf".format(self.id, self.co, self.period, i)
            data.append(
                ConfirmationData(link=self, no_id=c.bank_ids[i], bank_name=i,
                                 data={"add_none": True, "display_schedule": True, "data": c.data.get(i)},
                                 pdf_path=path))
        self.add_all(data)
        self.mk(cookies)

    def delete(self):
        try:
            os.remove(PATH + "zip/{}.zip".format(self.id))
        except FileNotFoundError:
            print("zip/{}.zip删除失败".format(self.id))
        for i in self.data:
            try:
                os.remove(PATH + i.pdf_path)
            except FileNotFoundError:
                print("{}删除失败".format(i.pdf_path))
            i.deep_delete()
        self.deep_delete()
        self.commit()

    def mk(self, cookies):
        mk_pdf_args_list = []
        files = []
        for i in self.data:
            path = "pdf/" + "{}_{}_{}_{}.pdf".format(self.id, self.co, self.period, i.bank_name)
            mk_pdf_args_list.append(
                [url_for("confirmation.view", bank_id=i.no_id, co_id=self.id), cookies, PATH + path])
            files.append(PATH + path)
        mk_zip_and_pdf.delay(self.id, files, mk_pdf_args_list)

    @classmethod
    def clean(cls):
        zipfiles = os.listdir(os.path.join(PATH, "zip"))
        zipdatas = cls.query.with_entities(cls.id).all()
        zipdatas = ["{}.zip".format(cid[0]) for cid in zipdatas]
        for zfile in zipfiles:
            if zfile in zipdatas:
                pass
            else:
                print("删除", zfile)
                os.remove(PATH + "zip/" + zfile)


class ConfirmationData(DbBase):
    link = relationship("ConfirmationLink", backref="data")
    link_id = Column(Integer, ForeignKey("confirmation_link.id"))
    no_id = Column(Integer)
    bank_name = Column(String(64))
    _data = Column("data", Text)
    pdf_path = Column(String(128))

    @property
    def data(self):
        return json.loads(self._data)

    @data.setter
    def data(self, obj):
        self._data = json.dumps(obj, ensure_ascii=False)

    @classmethod
    def clean(cls):
        pdffiles = os.listdir(os.path.join(PATH, "pdf"))
        pdfdatas = cls.query.with_entities(cls.pdf_path).all()
        pdfdatas = [pdf_path[0] for pdf_path in pdfdatas]
        for pdf in pdffiles:
            if "pdf/" + pdf in pdfdatas:
                pass
            else:
                print("删除", pdf)
                os.remove(PATH + "pdf/" + pdf)
