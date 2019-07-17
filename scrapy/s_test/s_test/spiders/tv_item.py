# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import TvItem
import pymysql
import pymysql.cursors
import string
import time
class TvItemSpider(scrapy.Spider):
    name = "tv_item"
    allowed_domains = ["qq.com"]
    #start_urls = ["https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&itype=100018&listpage=2&offset=0&pagesize=30"]

    def start_requests(self):
        self.connect_mysql()
                       # https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=tv&feature=1&listpage=2&offset=0&pagesize=30&sort=19
        self.base_url = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=tv&sort=19&listpage=2&pagesize=30"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from tv_category")
        data = self.cursor.fetchall()

        for category in data:
            if category['key'] == 'sort' or category['key_val'] == '-1':
                continue
            else:
                key = category["key"]
                key_val = category["key_val"]
                # 此处要拼接itype
                #first_res = scrapy.Request(base_url)
                #print(PyQuery(first_res.text))
                #self.key= 'itype'
                #self.key_val= '100020'
                url = self.base_url + "&" + key + "=" + key_val + "&offset=0"
                yield scrapy.Request(url=url, dont_filter=True, callback=self.page_list, meta={'key': key, 'key_val': key_val})



    def parse(self, response):
        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        tv_list = py(".mod_figure_list_box  .list_item")  #前分页的所有movie列表
        meta = response.meta
        for it in tv_list.items():
            tv_title = it(".figure_detail > a").attr("title")
            tv_url = it(".figure").attr("href")
            caption = it(".figure > .figure_caption").text()

            if not caption is None:
                tv_caption = caption
                if caption.find("更新") == -1:
                    tv_all = 1  # 已经更新完
                else:
                    tv_all = 0   # 在更新中
            else:
                tv_caption = ""
                tv_all = 1  # 已经更新完

            tv_image = it(".figure > .figure_pic").attr("src")
            tv_desc = it(".figure_detail > .figure_desc").attr("title")
            item = TvItem()
            item["tv_url"] = tv_url
            item["tv_caption"] = tv_caption
            item["tv_image"] = tv_image
            item["tv_title"] = tv_title
            item["tv_all"] = tv_all
            item["tv_desc"] = tv_desc
            item["offset"] = meta["offset"]
            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            # category
            cate = ("feature", "iarea", "year", "pay")
            for ca in cate:
                if ca == meta['key']:
                    item[ca] = meta['key_val']
                else:
                    item[ca] = ""
            yield item

    def page_list(self, response):  #获取当前分类下的所有分页

        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        page_list = py(".mod_pages .page_num")
        for page in page_list.items():
            offset = page.attr("data-offset")
            meta = response.meta
            meta['offset'] = offset
            page_url = self.base_url + "&" + meta['key'] + "=" + meta['key_val'] + "&offset=" + offset
            # 获取当前分页的信息
            yield scrapy.Request(url=page_url, callback=self.parse, meta=meta)


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
