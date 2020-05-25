# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import AiqiyiMovieListItem
from .. import db
import pypinyin
from urllib import parse
import json

class AqyMovieItemSpider(scrapy.Spider):
    name = "aqy_movie_item"
    allowed_domains = ["iqiyi.com"]
    start_urls = ['http://iqiyi.com/']

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://list.youku.com/category/show/c_96_a__g__s_6_u__r_.html?spm=a2ha1.12701310.app.5~5!2~5!2~5~5~DL!2~DD~A"
        self.key = ""
        self.key_val = ""
        self.params = {
            'access_play_control_platform': 14,
            'channel_id': 1,
            'data_type': 1,
            'from': 'pcw_list',
            'is_album_finished': '',
            'is_purchase': '',
            'key': '',
            'market_release_date_level': '',  # 年份
            'mode': 11,
            'pageNum': 1,
            'pageSize': 48,
            'site': 'iqiyi',
            'source_type': '',
            'three_category_id': '',  # 地区 类型
            'without_qipu': 1
        }
        self.url = 'https://pcw-api.iqiyi.com/search/video/videolists?access_play_control_platform=14&channel_id=1&data_type=1&from=pcw_list&is_album_finished=&is_purchase=&key=&mode=11&&pageSize=48&site=iqiyi&source_type=&without_qipu=1&'
        # pageNum=1&three_category_id=&market_release_date_level=   # 年
        # pageNum=1&market_release_date_level=&three_category_id=1;must   # 地区 类型
        # 从数据库获取所有的分类
        self.cursor.execute("select * from aqy_movie_category where disabled =0 order by id desc")
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
                param = category['url']
                # if key == 'charge':
                if key == 'iyear':
                    url = self.url + 'pageNum=1&three_category_id=&market_release_date_level=' + str(param)
                else:
                    url = self.url + 'pageNum=1&market_release_date_level=&three_category_id=' + str(param) + ';must'

                #if key == 'iyear':
                yield scrapy.Request(url=url, dont_filter=True, callback=self.page_list,
                                    meta={'key': key, 'key_val': key_val, 'year': year, 'offset': 0, 'param': param})

    def parse(self, response):
        print('---------parse--------------')
        # 此处要拼接offset  获取当前系itype下的所有分页
        data = json.loads(response.text)["data"]
        meta = response.meta
        pinyin = ""
        py = ""
        leng = len(data['list'])
        print(data['list'])
        print(leng)
        for index in range(leng):
            it = data["list"][index]
            pinyin = ""
            py = ""

            movie_title = it['name']
            movie_url = it["playUrl"]
            #movie_score = it['score'] if it['score'] else ""
            movie_image = it["imageUrl"]
            movie_desc = it['secondInfo']
            if not movie_title is None:
                pinyin1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.NORMAL)
                py1 = pypinyin.pinyin(movie_title.split(" ")[0], style=pypinyin.FIRST_LETTER)  # 简拼
                for i in pinyin1:
                    pinyin += ''.join(i)
                for j in py1:
                    py += ''.join(j)
            item = AiqiyiMovieListItem()
            item["movie_url"] = movie_url
            item["movie_score"] =""
            item["movie_image"] = movie_image
            item["movie_title"] = movie_title
            item["movie_desc"] = movie_desc
            if meta['key'] == 'iyear':
                item["offset"] = meta['year']
                item["order"] = int(meta['offset']) + int(index)
            else:
                item["offset"] = 0
                item["order"] = 0

            item["key"] = meta["key"]
            item["key_val"] = meta["key_val"]
            item["pinyin"] = pinyin
            item["py"] = py,
            item["source"] = 'aqy'
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
        #self.parse(response)
        data = json.loads(response.text)["data"]
        page_total = data['pageTotal']
        meta = response.meta
        for page in range(1, int(page_total)):
            #if page == 1:
            key = meta['key']
            param = meta['param']
            offset = (page - 1) * 48
            meta['offset'] = offset
            if key == 'iyear':
                url = self.url + 'pageNum=' + str(page) + '&three_category_id=&market_release_date_level=' + str(param)
            else:
                url = self.url + 'pageNum=' + str(page) + '&market_release_date_level=&three_category_id=' + str(param) + ';must'

            yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
