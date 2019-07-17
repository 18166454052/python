# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import VarietyList
import pymysql
import pymysql.cursors
import json
import re

class VarietyListSpider(scrapy.Spider):
    name = "variety_list"
    allowed_domains = ["qq.com"]

    def start_requests(self):
        self.connect_mysql()
        # 从数据库获取所有的tv_item
        self.cursor.execute("select id,variety_title,variety_url from variety_item")
        data = self.cursor.fetchall()

        for items in data:
            url = items['variety_url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'variety_id': items["id"], 'variety_title': items["variety_title"]})

    def parse(self, response):

        py = PyQuery(response.text)
        variety_list = py(".mod_figure_list_sm  .figure_list  .list_item")  #前分页的所有variety_list列表
        meta = response.meta
        for it in variety_list.items():
            item = VarietyList()
            variety_title = it(".figure").attr("title")
            variety_url = it(".figure_detail").attr("href")
            variety_image = it("a.figure  img").attr("src")
            date = it(".figure .figure_count .num").text()
            item["variety_title"] = variety_title
            item["variety_url"] = variety_url
            item["variety_image"] = variety_image
            item["parent_id"] = meta["variety_id"]
            item["parent_title"] = meta["variety_title"]
            item["date"] = date
            yield item

    def connect_mysql(self):  #连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import VarietyList
import pymysql
import pymysql.cursors
import json
import re

class VarietyListSpider(scrapy.Spider):
    name = "variety_list"
    allowed_domains = ["qq.com"]

    def start_requests(self):
        self.connect_mysql()
        # 从数据库获取所有的tv_item
        self.cursor.execute("select id,variety_title,variety_url from variety_item")
        data = self.cursor.fetchall()

        for items in data:
            url = items['variety_url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'variety_id': items["id"], 'variety_title': items["variety_title"]})

    def parse(self, response):

        py = PyQuery(response.text)
        variety_list = py(".mod_figure_list_sm  .figure_list  .list_item")  #前分页的所有variety_list列表
        meta = response.meta
        for it in variety_list.items():
            item = VarietyList()
            variety_title = it(".figure").attr("title")
            print(variety_title)
            if not variety_title is None:
                variety_url = it(".figure_detail").attr("href")
                variety_image = it("a.figure  img").attr("src")
                date = it(".figure .figure_count .num").text()
                item["variety_title"] = variety_title
                item["variety_url"] = variety_url
                item["variety_image"] = variety_image
                item["parent_id"] = meta["variety_id"]
                item["parent_title"] = meta["variety_title"]
                item["date"] = date
                yield item
            else:
                pass

    def connect_mysql(self):  #连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
