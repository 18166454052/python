# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import TencentMovieListItem
from .. import db
import pypinyin
from urllib import parse

class TencentMovieItemSpider(scrapy.Spider):
    name = "tencent_movie_item"
    allowed_domains = ["qq.com"]
    start_urls = ['http://qq.com/']

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&listpage=2&pagesize=30"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from movie_category")
        data = self.cursor.fetchall()
        for category in data:
            if category['key1'] == 'sort' or category['key_val'] == '-1':
                continue
            else:
                key = category["key1"]
                key_val = category["key_val"]

                # 此处要拼接itype
                # first_res = scrapy.Request(base_url)
                # print(PyQuery(first_res.text))
                # self.key= 'itype'
                # self.key_val= '100020'
                year = category["year"]
                url = self.base_url + "&" + key + "=" + key_val + "&offset=0"
                #if key == 'charge':
                yield scrapy.Request(url=url, dont_filter=True, callback=self.page_list,
                                     meta={'key': key, 'key_val': key_val, 'year': year})

    def parse(self, response):
        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        movie_list = py(".mod_figure_list_box  .list_item")  # 前分页的所有movie列表
        meta = response.meta
        pinyin = ""
        py = ""
        for index in range(movie_list.length):
            it = PyQuery(movie_list[index])
            #  movie_url
            #  movie_score
            #  movie_image
            #  movie_title
            #  movie_desc
            pinyin = ""
            py = ""

            movie_title = it(".figure_detail > a").attr("title")
            movie_url = parse.urljoin(response.url, it(".figure").attr("href"))
            movie_score = it(".figure > .figure_score").text()
            movie_image = it(".figure > .figure_pic").attr("src")
            movie_desc = it(".figure_detail > .figure_desc").attr("title")
            if not movie_title is None:
                pinyin1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.NORMAL)
                py1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.FIRST_LETTER)  # 简拼
                for i in pinyin1:
                    pinyin += ''.join(i)
                for j in py1:
                    py += ''.join(j)
            item = TencentMovieListItem()
            item["movie_url"] = movie_url
            item["movie_score"] = movie_score
            item["movie_image"] = movie_image
            item["movie_title"] = movie_title
            item["movie_desc"] = movie_desc
            # item["offset"] = meta["offset"]
            # item["key"] = meta["key"]
            # item["key_val"] = meta["key_val"]
            if meta['key'] == 'iyear':
                item["offset"] = meta['year']
                item["order"] = int(meta['offset']) + int(index)
                print('---iyear--------------')
                print(item)
            else:
                item["offset"] = 0
                item["order"] = 0
                print('---ii--------------')
                print(item)


            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            item["pinyin"] = pinyin
            item["py"] = py
            # category
            cate = ("itype", "iarea", "characteristic", "iyear", "charge")
            for ca in cate:
                if ca == meta['key']:
                    item[ca] = meta['key_val']
                else:
                    item[ca] = ""
            yield item

    def page_list(self, response):  # 获取当前分类下的所有分页

        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        self.parse(response)
        page_list = py(".mod_pages .page_num")
        for page in page_list.items():
            offset = page.attr("data-offset")
            meta = response.meta
            meta['offset'] = offset
            if meta['key'] == 'iyear':
                page_url = self.base_url + "&" + 'year' + "=" + meta['key_val'] + "&offset=" + offset
            else:
                page_url = self.base_url + "&" + meta['key'] + "=" + meta['key_val'] + "&offset=" + offset


            # 获取当前分页的信息
            yield scrapy.Request(url=page_url, callback=self.parse, meta=meta)

    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
