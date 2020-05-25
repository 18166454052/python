# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import db
class TencentMovieListPipeline(object):
    def open_spider(self, spider):

        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        sel_sql = "select * from movie_item where movie_title = \'%s\' " % (item['movie_title'])
        self.cursor.execute(sel_sql)
        res = self.cursor.fetchone()  # None
        if not res is None:
            # print(res)
            new_key_val = ""
            if res[item['key']] == '':  # 分类是空的   直接添加
                new_key_val = item['key_val']

            elif res[item['key']].find(item['key_val']) == -1:  # 已经有其他分类存在  且不存在此时的分类  添加
                new_key_val = res[item['key']] + '_' + item['key_val']
            else:
                return item

            if item['key'] == 'iyear':   # iyear  还要跟新  offset  px
                update_sql = "UPDATE movie_item SET %s  =  \'%s \',%s  =  \'%s \',%s  =  \'%s \'  WHERE movie_title = \'%s\'" % (
                item['key'], new_key_val, 'year', item['offset'], 'px', item['order'], item['movie_title'])
            else:
                update_sql = "UPDATE movie_item SET %s  =  \'%s \' WHERE movie_title = \'%s\'" % (
                item['key'], new_key_val, item['movie_title'])

            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库

            if item['key'] == 'iyear':  # iyear  传递 year  px   其他分类不传递   以防覆盖已经存在的year px
                sql = 'insert into movie_item ( movie_url, movie_score, movie_image, movie_title, movie_desc, year, itype , iarea , characteristic, iyear, charge,px,create_time, pinyin, py) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['movie_url'],  # item里面定义的字段和表字段对应
                                     item['movie_score'],
                                     item['movie_image'],
                                     item['movie_title'],
                                     item['movie_desc'],
                                     item['offset'],
                                     item['itype'],
                                     item['iarea'],
                                     item['characteristic'],
                                     item['iyear'],
                                     item['charge'],
                                     item['order'],
                                     datetime.datetime.now().strftime('%Y-%m-%d'),
                                     item['pinyin'],
                                     item['py']
                                     ))
            else:
                sql = 'insert into movie_item ( movie_url, movie_score, movie_image, movie_title, movie_desc,  itype , iarea , characteristic, iyear, charge,create_time, pinyin, py) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['movie_url'],  # item里面定义的字段和表字段对应
                                     item['movie_score'],
                                     item['movie_image'],
                                     item['movie_title'],
                                     item['movie_desc'],
                                     item['itype'],
                                     item['iarea'],
                                     item['characteristic'],
                                     item['iyear'],
                                     item['charge'],
                                     datetime.datetime.now().strftime('%Y-%m-%d'),
                                     item['pinyin'],
                                     item['py']
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
