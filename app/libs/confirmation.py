from copy import deepcopy
from app import app
import xlrd


class Confirmation:
    bank_ids: dict
    data: dict
    content: list

    def __init__(self, filepath):
        self.wb = xlrd.open_workbook(filepath)
        self.basic = self.get_basic()
        self.data = {}
        self.bank_ids = {}
        self.content = [
            {"title": ["1、银行存款"], "foot": ["除上述列示的银行存款（包括余额为零的存款账户）外，本公司并无在贵行的其他存款。"]},
            {"title": ["2、银行借款"], "foot": ["除上述列示的银行借款外，本公司并无自贵行的其他借款。"]},
            {"title": ["3、{}期间内注销的银行存款账户"], "foot": ["除上述列示的注销账户外，本公司在此期间并未在贵行注销其他账户。"]},
            {"title": ["4、本公司作为委托人的委托贷款"], "foot": ["除上述列示的委托贷款外，本公司并无通过贵行办理的其他以本公司作为委托人的委托贷款。"]},
            {"title": ["5、本公司作为借款人的委托贷款"], "foot": ["除上述列示的委托贷款外，本公司并无通过贵行办理的其他以本公司作为借款人的委托贷款。"]},
            {"title": ["6、担保", "（1）本公司为其他单位提供的、以贵行为担保受益人的担保"], "foot": ["除上述列示的担保外，本公司并无其他以贵行为担保受益人的担保。"]},
            {"title": ["（2）贵行向本公司提供的担保"], "foot": ["除上述列示的担保外，本公司并无贵行提供的其他担保。"]},
            {"title": ["7、本公司为出票人且由贵行承兑而尚未支付的银行承兑汇票"], "foot": ["除上述列示的银行承兑汇票外，本公司并无由贵行承兑而尚未支付的其他银行承兑汇票。"]},
            {"title": ["8、本公司向贵行已贴现而尚未到期的商业汇票"], "foot": ["除上述列示的商业汇票外，本公司并无向贵行已贴现而尚未到期的其他商业汇票。"]},
            {"title": ["9、本公司为持票人且由贵行托收的商业汇票"], "foot": ["除上述列示的商业汇票外，本公司并无由贵行托收的其他商业汇票。"]},
            {"title": ["10、本公司为申请人，由贵行开具的、未履行完毕的不可撤销信用证"], "foot": ["除上述列示的不可撤销信用证外，本公司并无由贵行开具的、未履行完毕的其他不可撤销信用证。"]},
            {"title": ["11、本公司与贵行之间未履行完毕的外汇买卖合约"], "foot": ["除上述列示的外汇买卖合约外，本公司并无与贵行之间未履行完毕的其他外汇买卖合约。"]},
            {"title": ["12、本公司存放于贵行托管的证券或其他产权文件"], "foot": ["除上述列示的证券或其他产权文件外，本公司并无存放于贵行托管的其他证券或其他产权文件。"]},
            {"title": ["13、本公司购买的由贵行发行的未到期银行理财产品"], "foot": ["除上述列示的银行理财产品外，本公司并未购买其他由贵行发行的理财产品。"]},
            {"title": ["14、其他"], "foot": []},
            {"title": ["附表  资金归集（资金池或其他资金管理）账户具体信息"], "foot": []},
        ]
        self.init_titles()
        self.get_data()

    def get_basic(self):
        table = self.wb.sheet_by_index(0)
        nor = table.nrows
        data_dict = {}
        for i in range(1, nor):
            title = table.cell_value(i, 0)
            value = table.cell_value(i, 1)
            if title == "函证基准日" or title == "开函日期":
                value = xlrd.xldate.xldate_as_datetime(value, 0).strftime('%Y年%m月%d日')
            data_dict[title] = value
        return data_dict

    def init_titles(self):
        for sht in self.wb.sheets():
            if sht.number >= 1:
                self.init_title(sht)
        self.content[2]["title"][0] = self.content[2]["title"][0].format(self.basic.get("销户函证期间"))

    def init_title(self, table):
        noc = table.ncols
        if table.number <= 16:
            titles = []
            self.content[table.number - 1]["titles"] = titles
            for c in range(1, noc):
                titles.append(table.cell_value(0, c))

    def get_data(self):
        n = 0
        for sht in self.wb.sheets():
            if sht.number >= 1:
                nor = sht.nrows
                noc = sht.ncols
                for r in range(1, nor):
                    if not self.data.get(sht.cell_value(r, 0)):
                        n += 1
                        self.data[sht.cell_value(r, 0)] = deepcopy(self.content)
                        self.bank_ids[sht.cell_value(r, 0)] = n
                    if not self.data[sht.cell_value(r, 0)][sht.number - 1].get("data"):
                        self.data[sht.cell_value(r, 0)][sht.number - 1]["data"] = []
                    tmp_list = self.data[sht.cell_value(r, 0)][sht.number - 1]["data"]
                    data_list = []
                    tmp_list.append(data_list)
                    for c in range(1, noc):
                        data_list.append(sht.cell_value(r, c))
                    # print(tmp_dict)


@app.template_filter("confirmation_format")
def confirmation_format(value, title):
    if type(value) is float:
        if title == "序号":
            ret = '<td style="text-align: center">{}</td>'
        else:
            ret = '<td style="text-align: right;white-space: nowrap">{}</td>'
    else:
        if title == "序号":
            ret = '<td style="text-align: center">{}</td>'
        else:
            ret = '<td>{}</td>'
    ret = ret.format(my_format(title, value))
    return ret


def my_format(title, value):
    '''

    :param title: 标题
    :param value: 值
    :return:
    '''
    if type(value) is float:
        if "额" in title or "值" in title or "量" in title:
            return "{:,.2f}".format(value)
        elif "日" in title:
            return xlrd.xldate.xldate_as_datetime(value, 0).strftime('%Y-%m-%d')
        elif "汇率" in title:
            return "{:.4f}".format(value)
        elif "率" in title:
            if "e" in str(value):
                # 1.23e-04
                # 1e-06
                list_of_float_split_e = str(value).split("e")
                decimal_n = -int(list_of_float_split_e[1])
                num_n = len(list_of_float_split_e[0].replace(".", ""))
                # 小数位数+数字个数-1为真是数字位数，百分数再减2
                return "{{:.{}%}}".format(decimal_n + num_n - 1 - 2).format(value)
            else:
                # 小数位数-2或者保留两位小数
                return "{{:.{}%}}".format(max(len(str(value).split(".")[1]) - 2, 2)).format(value)
        elif "序号" in title:
            return "{:d}".format(int(value))
    return value


# for r in range(0, nor):
#     if r > 0:
#         if not self.data.get(table.cell_value(r, 0)):
#             self.data[table.cell_value(r, 0)] = {}

#         title = table.cell_value(0, j)
#         value = table.cell_value(i, j)
#         tmp_dict[title] = value
# return data_dict


if __name__ == '__main__':
    c = Confirmation("../static/test.xlsx")
    # print(c.basic, c.bank_ids)
    # for k in c.data:
    #     print(k, c.data[k])
