# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import db
class TencentVarietyItemPipeline(object):
    def open_spider(self, spider):

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

        # 根据电影名称 判断该电影是不是已经爬取，如果已经存在 修改分类
        sel_sql = "select * from variety_item where variety_title = \'%s\' " % (item['variety_title'])
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

            if item['key'] == 'iyear':  # iyear  还要跟新  offset  px
                update_sql = "UPDATE variety_item SET %s  =  \'%s \',%s  =  \'%s \',%s  =  \'%s \' WHERE variety_title = \'%s\'" % (
                    item['key'], new_key_val, 'year', item['offset'], 'px', item['order'], item['variety_title'])
            else:
                update_sql = "UPDATE variety_item SET %s  =  \'%s \'  WHERE variety_title = \'%s\'" % (
                    item['key'], new_key_val, item['variety_title'])

            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库
            if item['key'] == 'iyear':
                sql = 'insert into variety_item (variety_url, variety_image, variety_title, variety_desc, year,exclusive, itype , iarea ,iyear, ipay, px ,create_time, pinyin, py) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['variety_url'],  # item里面定义的字段和表字段对应
                                     item['variety_image'],
                                     item['variety_title'],
                                     item['variety_desc'],
                                     item['offset'],
                                     item['exclusive'],
                                     item['itype'],
                                     item['iarea'],
                                     item['iyear'],
                                     item['ipay'],
                                     item['order'],
                                     datetime.datetime.now().strftime('%Y-%m-%d'),
                                     item['pinyin'],
                                     item['py']

                                     ))
            else:
                sql = 'insert into variety_item (variety_url, variety_image, variety_title, variety_desc,exclusive, itype , iarea ,iyear, ipay,create_time, pinyin, py) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['variety_url'],  # item里面定义的字段和表字段对应
                                     item['variety_image'],
                                     item['variety_title'],
                                     item['variety_desc'],
                                     item['exclusive'],
                                     item['itype'],
                                     item['iarea'],
                                     item['iyear'],
                                     item['ipay'],
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
