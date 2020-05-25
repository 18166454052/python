# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import TencentVarietyListItem
from .. import db
from urllib import parse


class TencentVarietyListsSpider(scrapy.Spider):
    name = "tencent_variety_lists"
    allowed_domains = ["qq.com"]

    def start_requests(self):
        self.connect_mysql()
        # 从数据库获取所有的tv_item
        self.cursor.execute("select id,variety_title,variety_url from variety_item")
        data = self.cursor.fetchall()

        for items in data:
            url = items['variety_url']
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'variety_id': items["id"], 'variety_title': items["variety_title"]})

    def parse(self, response):

        py = PyQuery(response.text)
        variety_lists = py(".mod_figure_list_sm  .figure_list")[0]  # 前分页的所有variety_list列表
        variety_list = PyQuery(variety_lists)(".list_item")
        meta = response.meta
        for it in variety_list.items():
            item = TencentVarietyListItem()
            variety_title = it(".figure").attr("title")
            variety_url = parse.urljoin(response.url, it(".figure_detail").attr("href"))
            variety_image = it("a.figure  img").attr("r-lazyload")  # 懒加载的图片真实地址  不是 src
            date = it(".figure .figure_count .num").text()
            item["variety_title"] = variety_title
            item["variety_url"] = variety_url
            item["variety_image"] = variety_image
            item["parent_id"] = meta["variety_id"]
            item["parent_title"] = meta["variety_title"]
            item["date"] = date
            yield item

    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
