# -*- coding: utf-8 -*-
import scrapy

import scrapy
from pyquery import PyQuery
from ..items import TencentVarietyItem
from .. import db
import pypinyin
from urllib import parse

class TencentVarietyListSpider(scrapy.Spider):
    name = "tencent_variety_item_update"
    allowed_domains = ["v.qq.com"]
    # start_urls = ["https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&itype=100018&listpage=2&offset=0&pagesize=30"]

    def start_requests(self):
        self.connect_mysql()
        self.count = 0

        # https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=variety&listpage=2&offset=30&pagesize=30&sort=4
        self.base_url = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=2&channel=variety&sort=5&listpage=1&pagesize=30"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from variety_category where disabled = 0")
        data = self.cursor.fetchall()
        for category in data:
            if category['key1'] == 'sort' or category['key_val'] == '-1':
                continue
            else:
                key = category["key1"]
                key_val = category["key_val"]
                year = category["year"]
                url = self.base_url + "&" + key + "=" + key_val + "&offset=0"
                yield scrapy.Request(url=url, dont_filter=True, callback=self.parse,
                                     meta={'key': key, 'key_val': key_val, 'year': year})

    def parse(self, response):
        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        variety_list = py(".list_item")  # 前分页的所有variety列表
        meta = response.meta
        for index in range(variety_list.length):
            it = PyQuery(variety_list[index])
            # variety_url = scrapy.Field()
            # variety_image = scrapy.Field()
            # variety_title = scrapy.Field()
            # variety_desc = scrapy.Field()
            # offset = scrapy.Field()
            # exclusive = scrapy.Field()
            # itype = scrapy.Field()
            # iarea = scrapy.Field()
            # iyear = scrapy.Field()
            # ipay = scrapy.Field()
            # order = scrapy.Field()
            # key = scrapy.Field()
            # key_val = scrapy.Field()
            # type = scrapy.Field()
            # create_time = scrapy.Field()
            pinyin = ""
            py = ""

            variety_title = it(".figure_detail > a").attr("title")
            variety_url = parse.urljoin(response.url, it(".figure").attr("href"))
            variety_image = it(".figure > .figure_pic").attr("src")
            variety_desc = it(".figure_detail > .figure_desc").attr("title")
            if not variety_title is None:
                pinyin1 = pypinyin.pinyin(variety_title.split(" ")[0], style=pypinyin.NORMAL)
                py1 = pypinyin.pinyin(variety_title.split(" ")[0], style=pypinyin.FIRST_LETTER)  # 简拼
                for i in pinyin1:
                    pinyin += ''.join(i)
                for j in py1:
                    py += ''.join(j)
            item = TencentVarietyItem()
            item["variety_url"] = variety_url
            item["variety_image"] = variety_image
            item["variety_title"] = variety_title
            item["variety_desc"] = variety_desc
            if meta['key'] == 'iyear':
                item["offset"] = meta['year']
                item["order"] = int(meta['offset']) + int(index)
            else:
                item["offset"] = 0
                item["order"] = 0
            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            #item["order"] = self.count
            #self.count = self.count+1

            item["pinyin"] = pinyin
            item["py"] = py
            # category
            cate = ("itype", "iarea", "exclusive", "iyear", "ipay")
            for ca in cate:
                if ca == meta['key']:
                    item[ca] = meta['key_val']
                else:
                    item[ca] = ""
            # return
            yield item


    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
