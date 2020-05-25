# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import db
class AiqiyiMovieCategoryPipeline(object):
    def open_spider(self, spider):
        # self.file = open('ten.txt', 'w', encoding="utf-8")
        # print("-----open------")

        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # line = "{}\n".format(json.dumps(dict(item)))
        # self.file.write(line)
        # return item
        sql = 'insert into aqy_movie_category (name, url, type, key_val, label) value (%s, %s, %s, %s, %s )'
        self.cursor.execute(sql,  # 纯属python操作mysql知识，不熟悉请恶补
                            (item['name'],  # item里面定义的字段和表字段对应
                             item['url'],
                             item['key'],
                             item['key_val'],
                             item['label'],
                             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self, spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()
