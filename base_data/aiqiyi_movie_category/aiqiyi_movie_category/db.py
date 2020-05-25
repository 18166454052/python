# -*- coding: utf-8 -*-
from scrapy.conf import settings
import pymysql.cursors


host = settings.get("MYSQL_CONFIG_HOST")
port = settings.get("MYSQL_CONFIG_PORT")
db = settings.get("MYSQL_CONFIG_DB")
user = settings.get("MYSQL_CONFIG_USER")
password = settings.get("MYSQL_CONFIG_PASSWORD")
charset = settings.get("MYSQL_CONFIG_CHARSET")
use_unicode = settings.get("MYSQL_CONFIG_USE_UNICODE")
cursorclass = settings.get("MYSQL_CONFIG_CURSORCLASS")


mysqlConnect = pymysql.connect(
        host=host,  # 数据库地址
        port=port,  # 数据库端口
        db=db,  # 数据库名
        user=user,  # 数据库用户名
        passwd=password,  # 数据库密码
        charset=charset,  # 编码方式
        use_unicode=use_unicode,
        cursorclass=cursorclass
     )

