# -*- coding: utf-8 -*-
import scrapy

from pyquery import PyQuery
from ..items import YoukuMovieListItem
from .. import db
import pypinyin
from urllib import parse

class YkMovieListSpider(scrapy.Spider):
    name = "yk_movie_list"
    allowed_domains = ["youku.com"]
    start_urls = ['http://youku.com/']

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://list.youku.com/category/show/c_96_a__g__s_6_u__r_.html?spm=a2ha1.12701310.app.5~5!2~5!2~5~5~DL!2~DD~A"
        self.key = ""
        self.key_val = ""
        # 从数据库获取所有的分类
        self.cursor.execute("select * from youku_movie_category where disabled =0")
        data = self.cursor.fetchall()
        for category in data:
            if category['key'] == 'sort' or category['key_val'] == '-1':
                continue
            else:
                key = category["key"]
                key_val = category["key_val"]

                # 此处要拼接itype
                # first_res = scrapy.Request(base_url)
                # print(PyQuery(first_res.text))
                # self.key= 'itype'
                # self.key_val= '100020'
                year = category["year"]
                url = category['url']
                # if key == 'charge':
                yield scrapy.Request(url=url, dont_filter=True, callback=self.page_list,
                                     meta={'key': key, 'key_val': key_val, 'year': year, 'url': url, 'offset': 30})

    def parse(self, response):
        print('---------parse--------------')
        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        movie_list = py(".box-series  .panel .yk-col4.mr1  .yk-pack.pack-film")  # 前分页的所有movie列表
        #print('++++++++++++++++++++' + movie_list.length)
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

            movie_title = it(".p-thumb > a").attr("title")
            movie_url = parse.urljoin(response.url, it(".info-list .title a").attr("href"))
            #movie_score = it(".figure > .figure_score").text()
            movie_image = it(".p-thumb .quic").attr("_src")
            #movie_desc = it(".figure_detail > .figure_desc").attr("title")
            if not movie_title is None:
                pinyin1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.NORMAL)
                py1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.FIRST_LETTER)  # 简拼
                for i in pinyin1:
                    pinyin += ''.join(i)
                for j in py1:
                    py += ''.join(j)
            item = YoukuMovieListItem()
            item["movie_url"] = movie_url
            item["movie_score"] = ""
            item["movie_image"] = movie_image
            item["movie_title"] = movie_title
            item["movie_desc"] = ""
            # item["offset"] = meta["offset"]
            # item["key"] = meta["key"]
            # item["key_val"] = meta["key_val"]
            if meta['key'] == 'iyear':
                item["offset"] = meta['year']
                item["order"] = int(meta['offset']) + int(index)
            else:
                item["offset"] = 0
                item["order"] = 0

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
            #print(item)
            yield item

    def page_list(self, response):  # 获取当前分类下的所有分页

        # 此处要拼接offset  获取当前系itype下的所有分页
        py = PyQuery(response.text)
        #self.parse(response)

        #print(py)
        movie_list = py(".box-series  .panel .yk-col4.mr1  .yk-pack.pack-film")  # 前分页的所有movie列表
        page_list = py(".yk-pages li")
        last = py(page_list[page_list.length - 2]).text()
        for page in range(1, int(last)):
            # offset = page.attr("data-offset")
            meta = response.meta
            url = meta['url']
            url = url.replace(".html","_p_" + str(page) + '.html')
            offset = page * 30
            meta['offset'] = offset
            # if meta['key'] == 'iyear':
            #     page_url = self.base_url + "&" + 'year' + "=" + meta['key_val'] + "&offset=" + offset
            # else:
            #     page_url = self.base_url + "&" + meta['key'] + "=" + meta['key_val'] + "&offset=" + offset
            #page_url = self.base_url + "&p=" + page.text()
            # 获取当前分页的信息
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

