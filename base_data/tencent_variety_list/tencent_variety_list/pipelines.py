# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import db

class TencentVarietyListPipeline(object):
    def open_spider(self, spider):
        # self.file = open('ten.txt', 'w', encoding="utf-8")
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        '''
        由于爬虫和插入数据库的速度不一致，在spider中判断数据是否已经存在数据库是错误的
        因为相同的数据已经爬取，但是没有存到数据库中，此时查询没有数据
        :param item:
        :param spider:
        :return:
        '''
        # 判断结束，没有爬取 插入数据库
        sql = 'insert into variety_list ( variety_url, variety_title, variety_image, parent_id, parent_title, date, create_time) ' \
              'value (%s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(sql,  # 纯属python操作mysql知识
                            (item['variety_url'],  # item里面定义的字段和表字段对应
                             item['variety_title'],
                             item['variety_image'],
                             item['parent_id'],
                             item['parent_title'],
                             item['date'],
                             datetime.datetime.now().strftime('%Y-%m-%d')

                             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self, spider):
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()
