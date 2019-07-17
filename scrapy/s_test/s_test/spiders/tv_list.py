# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import TvList
import pymysql
import pymysql.cursors
import json
import re

class TvListSpider(scrapy.Spider):
    name = "tv_list"
    allowed_domains = ["qq.com"]

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://v.qq.com/detail/r/"
        # 从数据库获取所有的tv_item
        self.cursor.execute("select id,tv_title,tv_url,tv_all from tv_item")
        data = self.cursor.fetchall()

        for items in data:
            tv_url = items["tv_url"].split("/")[-1]
            url = self.base_url + tv_url
            yield scrapy.Request(url=url, callback=self.check_all, meta={'tv_id': items["id"], 'tv_title': items["tv_title"],id: tv_url, 'tv_all': items["tv_all"]})
        #url = self.base_url + 'vbb35hm6m6da1wc.html'
        #yield scrapy.Request(url=url, callback=self.check_all, meta={'tv_id': '111', 'tv_title': "陈情令", id:'vbb35hm6m6da1wc.html','tv_all': '0'})

    def parse(self, response):
        # 此处要拼接offset  获取当前系itype下的所有分页
        # py = PyQuery(response.text)
        # tv_list = py(".mod_figure_list_box  .list_item")  #前分页的所有movie列表
        # meta = response.meta
        # for it in tv_list.items():
        #     tv_title = it(".figure_detail > a").attr("title")
        #     tv_url = it(".figure").attr("href")
        #     caption = it(".figure > .figure_caption").text()
        #
        #     if not caption is None:
        #         tv_caption = caption
        #         if caption.find("更新") == -1:
        #             tv_all = 1  # 已经更新完
        #         else:
        #             tv_all = 0   # 在更新中
        #     else:
        #         tv_caption = ""
        #         tv_all = 1  # 已经更新完
        #
        #     tv_image = it(".figure > .figure_pic").attr("src")
        #     tv_desc = it(".figure_detail > .figure_desc").attr("title")
        #     item = TvItem()
        #     item["tv_url"] = tv_url
        #     item["tv_caption"] = tv_caption
        #     item["tv_image"] = tv_image
        #     item["tv_title"] = tv_title
        #     item["tv_all"] = tv_all
        #     item["tv_desc"] = tv_desc
        #     item["offset"] = meta["offset"]
        #     item["key"] = meta["key"]
        #     item["key_val"] = meta["key_val"]
        #     # category
        #     cate = ("feature", "iarea", "year", "pay")
        #     for ca in cate:
        #         if ca == meta['key']:
        #             item[ca] = meta['key_val']
        #         else:
        #             item[ca] = ""
        item = TvList()
        yield item

    def check_all(self, response):  # 判断是不是所有的列表都显示
        '''
           tv_num = scrapy.Field()
           tv_title = scrapy.Field()
           tv_url = scrapy.Field()
           parent_id = scrapy.Field()
           parent_title = scrapy.Field()
           is_trail_notice = scrapy.Field()
           create_time = scrapy.Field()

        '''
        py = PyQuery(response.text)
        tv_list = py("div._playsrc_series > span > div > div > div > span.item")
        is_all = tv_list.has_class("item_all")
        meta = response.meta

        if is_all == False:   # 可以获取所有电视剧列表
            for tv in tv_list.items():
                mark = tv(".mark_v > img").attr("alt")  # 是不是预告片
                item = TvList()
                item["tv_url"] = tv("a").attr("href")
                item["tv_num"] = tv("a > span ").text()
                item["parent_id"] = meta["tv_id"]
                item["parent_title"] = meta["tv_title"]
                item["tv_title"] = ""
                item["is_trail_notice"] = '1' if mark == '预告' else '0'
                item["tv_all"] = meta["tv_all"]
                yield item

        else:

            base_url = "https://s.video.qq.com/get_playsource?plat=2&type=4&data_type=2&video_type=2&range=0-1000&plname=qq&otype=json&num_mod_cnt=20&callback=_jsonp_1_39e8&_t=1562138280612&id="
            url = base_url + meta["id"]
            yield scrapy.Request(url=url, callback=self.jsonp, meta=meta)

    def jsonp(self, response):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            tv_list1 = str(PyQuery(response.text))
            rule = r'\((.*?)\)'
            tv_res = re.findall(rule, tv_list1)[0]
            tv_lists = json.loads(tv_res)["PlaylistItem"]["videoPlayList"]
            meta = response.meta
            for tv in tv_lists:
                item = TvList()
                item["tv_url"] = tv["playUrl"]
                item["tv_num"] = tv["episode_number"]
                item["parent_id"] = meta["tv_id"]
                item["parent_title"] = meta["tv_title"]
                item["is_trail_notice"] = '0'
                item["tv_title"] = ""
                yield item

            return

        except:
            raise ValueError('Invalid Input')



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
