# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import CartoonItem
import pymysql
import pymysql.cursors
import pypinyin
import string
import time
class CartoonItemSpider(scrapy.Spider):
    name = "cartoon_item"
    allowed_domains = ["qq.com"]
    #start_urls = ["https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&itype=100018&listpage=2&offset=0&pagesize=30"]

    def start_requests(self):

        self.connect_mysql()
                       # https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=cartoon&listpage=2&offset=30&pagesize=30&sort=18
        self.base_url = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&channel=cartoon&sort=18&listpage=2&pagesize=30"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from cartoon_category")
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
        cartoon_list = py(".list_item")
        meta = response.meta
        for index in range(cartoon_list.length):
            it = PyQuery(cartoon_list[index])
            cartoon_title = it(".figure_detail > a").attr("title")
            cartoon_url = it(".figure").attr("href")
            caption = it(".figure > .figure_caption").text()

            if not caption is None:
                cartoon_caption = caption
                if caption.find("更新") == -1:
                    cartoon_all = 1  # 已经更新完
                else:
                    cartoon_all = 0   # 在更新中
            else:
                cartoon_caption = ""
                cartoon_all = 1  # 已经更新完

            cartoon_image = it(".figure > .figure_pic").attr("src")
            cartoon_desc = it(".figure_detail > .figure_desc").attr("title")
            pinyin = ""
            py = ""
            if not cartoon_title is None:
                pinyin1 = pypinyin.pinyin(cartoon_title.split(" ")[0], style=pypinyin.NORMAL)
                py1 = pypinyin.pinyin(cartoon_title.split(" ")[0], style=pypinyin.FIRST_LETTER)  # 简拼
                for i in pinyin1:
                    pinyin += ''.join(i)
                for j in py1:
                    py += ''.join(j)

            item = CartoonItem()
            item["cartoon_url"] = cartoon_url
            item["cartoon_caption"] = cartoon_caption
            item["cartoon_image"] = cartoon_image
            item["cartoon_title"] = cartoon_title
            item["cartoon_all"] = cartoon_all
            item["cartoon_desc"] = cartoon_desc
            item["offset"] = meta["offset"]
            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            item["px"] = int(meta["offset"]) + int(index)
            item["pinyin"] = pinyin
            item["py"] = py
            # category
            cate = ("itype", "iarea", "iyear", "ipay", "plot_aspect", "language")
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
