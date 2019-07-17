# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import CartoonList
import pymysql
import pymysql.cursors
import json
import re
from scrapy.conf import settings
import db


class CartoonListSpider(scrapy.Spider):
    name = "cartoon_list"
    allowed_domains = ["qq.com"]

    def start_requests(self):
        self.connect_mysql()
        self.base_url = "https://v.qq.com/detail/m/"
        # 从数据库获取所有的cartoon_item
        self.cursor.execute("select id,cartoon_title,cartoon_url,cartoon_all from cartoon_item")
        data = self.cursor.fetchall()

        for items in data:
            cartoon_url = items["cartoon_url"].split("/")[-1]
            url = self.base_url + cartoon_url
            yield scrapy.Request(url=url, callback=self.check_all, meta={'cartoon_id': items["id"], 'cartoon_title': items["cartoon_title"],id: cartoon_url, 'cartoon_all': items["cartoon_all"]})
        #url = self.base_url + 'vbb35hm6m6da1wc.html'
        #yield scrapy.Request(url=url, callback=self.check_all, meta={'cartoon_id': '111', 'cartoon_title': "陈情令", id:'vbb35hm6m6da1wc.html','cartoon_all': '0'})

    def parse(self, response):
        # 此处要拼接offset  获取当前系itype下的所有分页
        # py = PyQuery(response.text)
        # cartoon_list = py(".mod_figure_list_box  .list_item")  #前分页的所有movie列表
        # meta = response.meta
        # for it in cartoon_list.items():
        #     cartoon_title = it(".figure_detail > a").attr("title")
        #     cartoon_url = it(".figure").attr("href")
        #     caption = it(".figure > .figure_caption").text()
        #
        #     if not caption is None:
        #         cartoon_caption = caption
        #         if caption.find("更新") == -1:
        #             cartoon_all = 1  # 已经更新完
        #         else:
        #             cartoon_all = 0   # 在更新中
        #     else:
        #         cartoon_caption = ""
        #         cartoon_all = 1  # 已经更新完
        #
        #     cartoon_image = it(".figure > .figure_pic").attr("src")
        #     cartoon_desc = it(".figure_detail > .figure_desc").attr("title")
        #     item = cartoonItem()
        #     item["cartoon_url"] = cartoon_url
        #     item["cartoon_caption"] = cartoon_caption
        #     item["cartoon_image"] = cartoon_image
        #     item["cartoon_title"] = cartoon_title
        #     item["cartoon_all"] = cartoon_all
        #     item["cartoon_desc"] = cartoon_desc
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
        item = CartoonList()
        yield item

    def check_all(self, response):  # 判断是不是所有的列表都显示
        '''
           cartoon_num = scrapy.Field()
           cartoon_title = scrapy.Field()
           cartoon_url = scrapy.Field()
           parent_id = scrapy.Field()
           parent_title = scrapy.Field()
           is_trail_notice = scrapy.Field()
           create_time = scrapy.Field()

        '''
        py = PyQuery(response.text)
        cartoon_list = py("div._playsrc_series > span > div > div > div > span.item")
        is_all = cartoon_list.has_class("item_all")
        meta = response.meta

        if is_all == False:   # 可以获取所有电视剧列表
            for cartoon in cartoon_list.items():
                mark = cartoon(".mark_v > img").attr("alt")  # 是不是预告片
                item = CartoonList()
                item["cartoon_url"] = cartoon("a").attr("href")
                item["cartoon_num"] = cartoon("a > span ").text()
                item["parent_id"] = meta["cartoon_id"]
                item["parent_title"] = meta["cartoon_title"]
                item["cartoon_title"] = ""
                item["is_trail_notice"] = '1' if mark == '预告' else '0'
                item["cartoon_all"] = meta["cartoon_all"]
                yield item

        else:

            base_url = "https://s.video.qq.com/get_playsource?plat=2&type=4&data_type=2&video_type=3&range=1-28&plname=qq&otype=json&num_mod_cnt=20&callback=_jsonp_1_9bba&_t=1563000215347&id="
            url = base_url + meta["id"]
            yield scrapy.Request(url=url, callback=self.jsonp, meta=meta)

    def jsonp(self, response):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            cartoon_list1 = str(PyQuery(response.text))
            rule = r'\((.*?)\)'
            cartoon_res = re.findall(rule, cartoon_list1)[0]
            cartoon_lists = json.loads(cartoon_res)["PlaylistItem"]["videoPlayList"]
            meta = response.meta
            for cartoon in cartoon_lists:
                item = CartoonList()
                item["cartoon_url"] = cartoon["playUrl"]
                item["cartoon_num"] = cartoon["episode_number"]
                item["parent_id"] = meta["cartoon_id"]
                item["parent_title"] = meta["cartoon_title"]
                item["is_trail_notice"] = '0'
                item["cartoon_title"] = ""
                yield item

            return

        except:
            raise ValueError('Invalid Input')



    def connect_mysql(self):  #连接数据库

        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
