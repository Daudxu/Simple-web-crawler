import time
import smtplib
import pymysql
import smtplib,os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
class taskJobModel():
    def __init__(self, url, username, money, goods_name):
        self.url = url
        self.username = username
        self.money = money
        self.goods_name = goods_name
        self.db = pymysql.connect("localhost", "root", "root", "monitor")
        self.cursor = self.db.cursor()

    def savedate(self):
        self.cursor.execute(
            """select * from mtr_spider_data where create_time >=(NOW() - interval 24 hour) AND  resourcese_url = %s AND author = %s  AND source_type = 1""",
            (self.url, self.username))
        # 是否有重复数据
        repetition = self.cursor.fetchone()
        # 重复
        if repetition:
            pass
        else:
            self.cursor.execute(
                """select * from mtr_spider_data where is_lock = 2 AND  resourcese_url = %s   AND source_type = 1""",
                (self.url))
            # 是否有重复数据
            repetition1 = self.cursor.fetchone()
            if re.match(r'^https?:/{2}\w.+$', self.url):
                regular_1 = re.findall(r"/\/(.+)\/", self.url)
                urltype = re.findall(r"\/(.+)", regular_1[0])
                print(urltype[0])
            else:
                urltype = ""
                print("This looks invalid.")

            if repetition1:
                self.cursor.execute(
                    """insert into mtr_spider_data(title, author, resourcese_url, amount, module_type, is_lock)
                    value (%s, %s, %s, %s, %s, %s)""",
                    (self.goods_name,
                     self.username,
                     self.url,
                     self.money,
                     urltype,
                     '2'))
            else:
                self.cursor.execute(
                    """insert into mtr_spider_data(title, author, resourcese_url, amount, module_type)
                    value (%s, %s, %s, %s, %s)""",
                    (self.goods_name,
                     self.username,
                     self.url,
                     self.money,
                     urltype))


