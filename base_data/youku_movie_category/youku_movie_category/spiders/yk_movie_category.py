# -*- coding: utf-8 -*-
import scrapy

from pyquery import PyQuery
from ..items import YoukuMovieCategoryItem
from urllib import parse
from .. import db
class YkMovieCategorySpider(scrapy.Spider):
    name = "yk_movie_category"
    allowed_domains = ["youku.com"]
    start_urls = ['https://list.youku.com/category/show/c_96.html?spm=a2ha1.12528442.m_4421_c_12714.d_1&scm=20140719.manual.4421.url_in_blank_https%3A%2F%2Flist.youku.com%2Fcategory%2Fshow%2Fc_96.html']

    def parse(self, response):
        self.connect_mysql()
        self.cursor.execute("select * from movie_category")
        data = self.cursor.fetchall()
        dict ={}
        for it in data:
           dict[it['name']] = ['','']
           dict[it['name']][0] = it['key']
           dict[it['name']][1] = it['key_val']
        py = PyQuery(response.text)
        #type_list = py("#app > div > div.videolist_s_body.videolist_video_list > div:nth-child(2) > div > div > dl:nth-child(1)")
        type_list = py("#filterPanel .item")
        for index in range(type_list.length):
            if index > 0:
                item = YoukuMovieCategoryItem()
                item['label'] = py(type_list[index])("label").text()
                filter_item = py(type_list[index])("ul li ").find('a')
                for filter in filter_item.items():
                    item['url'] = parse.urljoin(response.url, filter.attr('href')),
                    item['name'] = filter.text()
                    if dict.get(item['name']):
                        item['key'] = dict.get(item['name'])[0]
                        item['key_val'] = dict.get(item['name'])[1]
                    else:
                        item['key'] = ""
                        item['key_val'] = ""
                    yield item



            '''
          
            filter_label = filter_line(".filter_label").text()

            a_tag_list = filter_line.find("a.filter_item")

            for a_tag in a_tag_list.items():
                item = YoukuMovieCategoryItem()
                item["label"] = filter_label
                item["name"] = a_tag.attr("_stat").split("_")[1]
                item["url"] = a_tag.attr("href")
                if a_tag.attr("data-key") == 'year':
                    item["key"] = 'iyear'
                else:
                    item["key"] = a_tag.attr("data-key")

                item["key_val"] = a_tag.attr("data-value")

                yield item
             '''

    def connect_mysql(self):  # 连接数据库
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()