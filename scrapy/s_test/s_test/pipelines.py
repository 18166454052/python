# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
import pymysql.cursors
import datetime
import db

class STestPipeline(object):
    # def __init__(self):
    #     pass
    #
    # @classmethod
    # def from_crawler(cls,crawler):
    #         return cls()

    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
        # print("-----open------")

        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        # line = "{}\n".format(json.dumps(dict(item)))
        # self.file.write(line)
        # return item
        sql = 'insert into movie_category (name, url, key, key_val, label) value (%s, %s, %s, %s, %s )'
        self.cursor.execute(sql,   # 纯属python操作mysql知识，不熟悉请恶补
             (item['name'],  # item里面定义的字段和表字段对应
             item['url'],
             item['key'],
             item['key_val'],
             item['label'],
             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

class MovieListPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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



    def process_item(self, item, spider):
        '''
        由于爬虫和插入数据库的速度不一致，在spider中判断数据是否已经存在数据库是错误的
        因为相同的数据已经爬取，但是没有存到数据库中，此时查询没有数据
        :param item:
        :param spider:
        :return:
        '''

        # 根据电影名称 判断该电影是不是已经爬取，如果已经存在 修改分类
        sel_sql = "select * from movie_item where movie_title = \'%s\' " % (item['movie_title'])
        self.cursor.execute(sel_sql)
        res = self.cursor.fetchone()  # None
        if not res is None:
            #print(res)
            new_key_val = ""
            if res[item['key']] == '':  # 分类是空的   直接添加
                new_key_val = item['key_val']

            elif res[item['key']].find(item['key_val']) == -1:  # 已经有其他分类存在  且不存在此时的分类  添加
                new_key_val = res[item['key']] + '_' + item['key_val']
            else:
                return item

            update_sql = "UPDATE movie_item SET %s  =  \'%s \' WHERE movie_title = \'%s\'" % (item['key'], new_key_val, item['movie_title'])
            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库
            sql = 'insert into movie_item ( movie_url, movie_score, movie_image, movie_title, movie_desc,offset,  itype , iarea , characteristic, year, charge,pinyin, py) ' \
                  'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
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
                                 item['year'],
                                 item['charge'],
                                 item['pinyin'],
                                 item['py']
                                 ))
            # 提交sql语句
            self.connect.commit()
            return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

class TvCategoryPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
        # print("-----open------")

        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        # line = "{}\n".format(json.dumps(dict(item)))
        # self.file.write(line)
        # return item
        sql = 'insert into tv_category (name, url, type, type_val, label) value (%s, %s, %s, %s, %s )'
        self.cursor.execute(sql,   # 纯属python操作mysql知识
             (item['name'],  # item里面定义的字段和表字段对应
             item['url'],
             item['key'],
             item['key_val'],
             item['label'],
             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()


class TvItemPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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



    def process_item(self, item, spider):
        '''
        由于爬虫和插入数据库的速度不一致，在spider中判断数据是否已经存在数据库是错误的
        因为相同的数据已经爬取，但是没有存到数据库中，此时查询没有数据
        :param item:
        :param spider:
        :return:
        '''

        # 根据电视剧名称 判断该电影是不是已经爬取，如果已经存在 修改分类
        sel_sql = "select * from tv_item where tv_title = \'%s\' " % (item['tv_title'])
        self.cursor.execute(sel_sql)
        res = self.cursor.fetchone()  # None
        if not res is None:
            #print(res)
            new_key_val = ""

            if res[item['key']] == '':   # 分类是空的   直接添加
                new_key_val = item['key_val']

            elif res[item['key']].find(item['key_val']) == -1:  # 已经有其他分类存在  且不存在此时的分类  添加
                new_key_val = res[item['key']] + '_' + item['key_val']
            else:
                return item
                #new_key_val = item['key_val']
            update_sql = "UPDATE tv_item SET %s  =  \'%s \' WHERE tv_title = \'%s\'" % (item['key'], new_key_val, item['tv_title'])
            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库  cate = ("feature", "iarea", "year", "pay")
            sql = 'insert into tv_item ( tv_url,tv_all, tv_image, tv_title, tv_desc,tv_caption , offset,  feature , iarea , year, pay, create_time, pinyin, py) ' \
                  'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s,%s)'
            self.cursor.execute(sql,  # 纯属python操作mysql知识
                                (item['tv_url'],  # item里面定义的字段和表字段对应
                                 item['tv_all'],
                                 item['tv_image'],
                                 item['tv_title'],
                                 item['tv_desc'],
                                 item['tv_caption'],
                                 item['offset'],
                                 item['feature'],
                                 item['iarea'],
                                 item['year'],
                                 item['pay'],
                                 datetime.datetime.now().strftime('%Y-%m-%d'),
                                 item['pinyin'],
                                 item['py'],
                                 ))
            # 提交sql语句
            self.connect.commit()
            return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

class TvListPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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



    def process_item(self, item, spider):
        # 如果是没有跟新完的  会有数据重复    查看数据库 直接更新
        if item["tv_all"] == 1:  # 已经跟新完毕直接插入
            sql = 'insert into tv_list (tv_url,tv_num,tv_title, parent_id, parent_title, is_trail_notice , create_time) ' \
                  'value (%s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(sql,  # 纯属python操作mysql知识
                                (item['tv_url'],  # item里面定义的字段和表字段对应
                                 item['tv_num'],
                                 item['tv_title'],
                                 item['parent_id'],
                                 item['parent_title'],
                                 item['is_trail_notice'],
                                 datetime.datetime.now().strftime('%Y-%m-%d')
                                 ))
        else:  # 检查是否已经插入  update
            sql = "select * from  tv_list where  tv_num = \'%s\' and parent_title = \'%s\'" % (item["tv_num"], item["parent_title"])
            self.cursor.execute(sql)
            res = self.cursor.fetchone()  # None
            if not res is None:  # 已经存在  更新
                sql1 = "UPDATE tv_list set tv_url = \'%s\' , is_trail_notice =  \'%s\'  where  tv_num = \'%s\' and  parent_title = \'%s\'" % (item["tv_url"], item["is_trail_notice"], item["tv_num"], item["parent_title"])
                print(sql1)
                self.cursor.execute(sql1)
            else:    #直接插入
                sql = 'insert into tv_list (tv_url,tv_num,tv_title, parent_id, parent_title, is_trail_notice , create_time) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s)'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['tv_url'],  # item里面定义的字段和表字段对应
                                     item['tv_num'],
                                     item['tv_title'],
                                     item['parent_id'],
                                     item['parent_title'],
                                     item['is_trail_notice'],
                                     datetime.datetime.now().strftime('%Y-%m-%d')
                                     ))

        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回


    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

class VarietyCategoryPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
        # print("-----open------")

        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        # line = "{}\n".format(json.dumps(dict(item)))
        # self.file.write(line)
        # return item
        sql = 'insert into variety_category (name, url, type, type_val, label) value (%s, %s, %s, %s, %s )'
        self.cursor.execute(sql,   # 纯属python操作mysql知识
             (item['name'],  # item里面定义的字段和表字段对应
             item['url'],
             item['key'],
             item['key_val'],
             item['label'],
             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()


class VarietyItemPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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
            #print(res)
            new_key_val = ""
            if res[item['key']] == '':  # 分类是空的   直接添加
                new_key_val = item['key_val']

            elif res[item['key']].find(item['key_val']) == -1:  # 已经有其他分类存在  且不存在此时的分类  添加
                new_key_val = res[item['key']] + '_' + item['key_val']
            else:
                return item

            update_sql = "UPDATE variety_item SET %s  =  \'%s \' WHERE variety_title = \'%s\'" % (item['key'], new_key_val, item['variety_title'])
            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库
            sql = 'insert into variety_item (variety_url, variety_image, variety_title, variety_desc, offset,exclusive, itype , iarea ,iyear, ipay, px ,create_time, pinyin, py) ' \
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
            # 提交sql语句
            self.connect.commit()
            return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()


class VarietyListPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()


class CartoonCategoryPipeline(object):
    def open_spider(self,spider):



        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='movie',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        # line = "{}\n".format(json.dumps(dict(item)))
        # self.file.write(line)
        # return item
        sql = 'insert into cartoon_category (name, url, type, type_val, label) value (%s, %s, %s, %s, %s )'
        self.cursor.execute(sql,   # 纯属python操作mysql知识
             (item['name'],  # item里面定义的字段和表字段对应
             item['url'],
             item['key'],
             item['key_val'],
             item['label'],
             ))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()


class CartoonItemPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
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



    def process_item(self, item, spider):
        '''
        由于爬虫和插入数据库的速度不一致，在spider中判断数据是否已经存在数据库是错误的
        因为相同的数据已经爬取，但是没有存到数据库中，此时查询没有数据
        :param item:
        :param spider:
        :return:
        '''

        # 根据电视剧名称 判断该电影是不是已经爬取，如果已经存在 修改分类
        sel_sql = "select * from cartoon_item where cartoon_title = \'%s\' " % (item['cartoon_title'])
        self.cursor.execute(sel_sql)
        res = self.cursor.fetchone()  # None
        if not res is None:
            #print(res)
            new_key_val = ""

            if res[item['key']] == '':   # 分类是空的   直接添加
                new_key_val = item['key_val']

            elif res[item['key']].find(item['key_val']) == -1:  # 已经有其他分类存在  且不存在此时的分类  添加
                new_key_val = res[item['key']] + '_' + item['key_val']
            else:
                return item
                #new_key_val = item['key_val']
            update_sql = "UPDATE cartoon_item SET %s  =  \'%s \' WHERE cartoon_title = \'%s\'" % (item['key'], new_key_val, item['cartoon_title'])
            self.cursor.execute(update_sql)
            self.connect.commit()
            print("=============================处理重复数据============================================")
            return item

        else:
            # 判断结束，没有爬取 插入数据库  cate = ("feature", "iarea", "year", "pay")
            sql = 'insert into cartoon_item ( cartoon_url,cartoon_all, cartoon_image, cartoon_title, cartoon_desc,cartoon_caption , offset,  itype , iarea , iyear, ipay,language, plot_aspect , pinyin , py ,px , create_time) ' \
                  'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)'
            self.cursor.execute(sql,  # 纯属python操作mysql知识
                                (item['cartoon_url'],  # item里面定义的字段和表字段对应
                                 item['cartoon_all'],
                                 item['cartoon_image'],
                                 item['cartoon_title'],
                                 item['cartoon_desc'],
                                 item['cartoon_caption'],
                                 item['offset'],
                                 item['itype'],
                                 item['iarea'],
                                 item['iyear'],
                                 item['ipay'],
                                 item['language'],
                                 item['plot_aspect'],
                                 item['pinyin'],
                                 item['py'],
                                 item['px'],
                                 datetime.datetime.now().strftime('%Y-%m-%d')
                                 ))
            # 提交sql语句
            self.connect.commit()
            return item  # 必须实现返回

    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

class CartoonListPipeline(object):
    def open_spider(self,spider):

        # self.file = open('ten.txt', 'w', encoding="utf-8")
        self.connect = db.mysqlConnect
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()



    def process_item(self, item, spider):
        # 如果是没有跟新完的  会有数据重复    查看数据库 直接更新
        if item["cartoon_all"] == 1:  # 已经跟新完毕直接插入
            sql = 'insert into cartoon_list (cartoon_url, cartoon_num, cartoon_title, parent_id, parent_title, is_trail_notice , create_time) ' \
                  'value (%s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(sql,  # 纯属python操作mysql知识
                                (item['cartoon_url'],  # item里面定义的字段和表字段对应
                                 item['cartoon_num'],
                                 item['cartoon_title'],
                                 item['parent_id'],
                                 item['parent_title'],
                                 item['is_trail_notice'],
                                 datetime.datetime.now().strftime('%Y-%m-%d')
                                 ))
        else:  # 检查是否已经插入  update
            sql = "select * from  cartoon_list where  cartoon_num = \'%s\' and parent_title = \'%s\'" % (item["cartoon_num"], item["parent_title"])
            self.cursor.execute(sql)
            res = self.cursor.fetchone()  # None
            if not res is None:  # 已经存在  更新
                sql1 = "UPDATE cartoon_list set cartoon_url = \'%s\' , is_trail_notice =  \'%s\'  where  cartoon_num = \'%s\' and  parent_title = \'%s\'" % (item["cartoon_url"], item["is_trail_notice"], item["cartoon_num"], item["parent_title"])
                print(sql1)
                self.cursor.execute(sql1)
            else:    #直接插入
                sql = 'insert into cartoon_list (cartoon_url,cartoon_num,cartoon_title, parent_id, parent_title, is_trail_notice , create_time) ' \
                      'value (%s, %s, %s, %s, %s, %s, %s)'
                self.cursor.execute(sql,  # 纯属python操作mysql知识
                                    (item['cartoon_url'],  # item里面定义的字段和表字段对应
                                     item['cartoon_num'],
                                     item['cartoon_title'],
                                     item['parent_id'],
                                     item['parent_title'],
                                     item['is_trail_notice'],
                                     datetime.datetime.now().strftime('%Y-%m-%d')
                                     ))

        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回


    def close_spider(self,spider):
        # self.file.close()
        # print("--------close---------")
        self.cursor.close()
        # 关闭数据库连接
        self.connect.close()

