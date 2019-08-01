# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import MovieItem
import pymysql
import pymysql.cursors
import pypinyin
class MovieListSpider(scrapy.Spider):
    name = "movie_list"
    allowed_domains = ["qq.com"]
    #start_urls = ["https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&itype=100018&listpage=2&offset=0&pagesize=30"]

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&channel=movie&sort=18&listpage=2&pagesize=30"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from movie_category")
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
        movie_list = py(".mod_figure_list_box  .list_item")  #前分页的所有movie列表
        meta = response.meta
        pinyin = ""
        py = ""
        for it in movie_list.items():
            #  movie_url
            #  movie_score
            #  movie_image
            #  movie_title
            #  movie_desc
            pinyin = ""
            py = ""

            movie_title = it(".figure_detail > a").attr("title")
            movie_url = it(".figure").attr("href")
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
            item = MovieItem()
            item["movie_url"] = movie_url
            item["movie_score"] = movie_score
            item["movie_image"] = movie_image
            item["movie_title"] = movie_title
            item["movie_desc"] = movie_desc
            item["offset"] = meta["offset"]
            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            item["pinyin"] = pinyin
            item["py"] = py
            # category
            cate = ("itype", "iarea", "characteristic", "year", "charge")
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
