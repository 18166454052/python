# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import STestItem
import sys
print(sys.path)

class BaiduSpider(scrapy.Spider):
    name = 'movie_category'
    #allowed_domains = ['lab.scrapy.cn']
    start_urls = ['https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1']
    '''
    如果要动态拼接路哟   要接受动态传入的参数
    此时要重写 start_request函数
    tag = getattr(self, "tag", None)
    '''


    def parse(self, response):
        py = PyQuery(response.text)

        type_list = py("body > div.mod_row_box >div >div.mod_list_filter").find(".filter_line")

        for filter_line in type_list.items():
            filter_label = filter_line(".filter_label").text()

            a_tag_list = filter_line.find("a.filter_item")


            for a_tag in a_tag_list.items():
                item = STestItem()
                item["label"] = filter_label
                item["name"] = a_tag.attr("_stat").split("_")[1]
                item["url"] = a_tag.attr("href")
                item["key"] = a_tag.attr("data-key")
                item["key_val"] = a_tag.attr("data-value")

                yield item


'''
        print("-------进入解析器--------")
        #res = response.css("title").extract()
        # 直接css得到的是一个selector列表
        # extract  得到标签的列表
        #res = response.css("title::text").extract_first()
        #::text 得到标签里的数据
        res = response.css("div.quote")[0]
        text = res.css(".text::text").extract_first()
        auto = res.css(".author::text").extract_first()
        tages = res.css(".tags .tag::text").extract()
        print('----------------text-------------------')
        print(text)
        print('----------------auto-------------------')
        print(auto)
        print('----------------tages-------------------')
        print(tages)
        print("==========================xpath=================================")
        link = response.xpath("//ol[@class='page-navigator']//@href").extract()
        print(link)
        txt = response.xpath("//ol[@class='page-navigator']//a/text()").extract()
        print(txt)
        string = response.xpath("string(//div[@class='post-content'])").extract()
        print(string)
        string1 = response.xpath("//div[@class='post-content']/text()").extract()
        print(string1)
        # string string1都可以提取文字和标签混合的所有的文字
        # 但是 string 去掉了格式   成为纯文本    string1保存了原有的格式
        '''
'''
css
关于提取页面
  提取标签属性 response.css（"a[@class='name']::attr(href)"）
  提取标签内容  respose.css（"a::text"）
  其他更高级的用法来获取到某一个标签-----再使用上面的方法

'''

'''xpath
关于提取页面
  提取标签属性 response.xpath（"//a//@href"）
  提取标签内容 response.xpath（"//a/text()"）
  
  其他更高级的用法来获取到某一个标签-----再使用上面的方法

'''