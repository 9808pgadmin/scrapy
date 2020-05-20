#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import random
import re
import time
from urllib import request


class MaoyanSpider:
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        # 用于记录页数
        self.page = 1

    # 获取
    def get_page(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 '}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        # 直接调用解析函数
        self.parse_page(html)

    # 解析
    def parse_page(self, html):
        p = re.compile(
            '<div class="movie-item-info">.*?title="(.*?)".*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>', re.S)
        r_list = p.findall(html)
        print(r_list)
        self.write_page(r_list)

    # 保存
    def write_page(self, r_list):
        one_film_dict = {}
        for rt in r_list:
            one_film_dict['name'] = rt[0].strip()
            one_film_dict['star'] = rt[1].strip()
            one_film_dict['time'] = rt[2].strip()[5:15]
            print(one_film_dict)

    # 保存
    # def write_page(self, r_list):
    #     # print(r_list)
    #     with open('./maoyan.csv', 'a', newline='') as f:
    #         for rt in r_list:
    #             writer = csv.writer(f)
    #             writer.writerow([rt[0], rt[1].strip(),
    #                               rt[2].strip()[5:15]])

    def main(self):
        for offset in range(0, 11, 10):
            url = self.url.format(offset)
            self.get_page(url)
            time.sleep(random.randint(1, 3))
            print('第%d页爬取完成' % self.page)
            self.page += 1


if __name__ == '__main__':
    start = time.time()
    spider = MaoyanSpider()
    spider.main()
    end = time.time()
    print('执行时间: %.2f' % (end-start))


import pymysql
"""插入数据库"""
# 数据库对象
db = pymysql.connect('localhost','root','123456','maoyandb',
                     charset='utf8')
# 游标对象
cursor = db.cursor()
# execute()方法第二个参数为列表传参补位
cursor.execute('insert into film values(%s,%s,%s)',
               ['霸王别姬','张国荣','1993'])
# 提交到数据库执行
db.commit()
# 关闭
cursor.close()
db.close()