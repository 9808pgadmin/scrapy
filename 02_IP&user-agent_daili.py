#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
import requests
from lxml import etree


def get_random_useragent():
    ua = UserAgent()
    return ua.radom


url = 'https://www.xicidaili.com/nn/'
def get_ip_list():
    headers = {'User-Agent': get_random_useragent()}
    html = requests.get(url, headers=headers).content.decode('utf-8')
    #    解析
    parse_html = etree.HTML(html)
    # r_list: [ ]
    r_list = parse_html.xpath('//tr')
    proxy_list = []
    for r in r_list:
        ip = r.xpath('./td[2]/text()')[0]
        port = r.xpath('./td[3]/text()')[0]
        proxy_list.append(
            {
                'http':'http//{}:{}'.format(ip,port),
                'https':'https//{}:{}'.format(ip,port)
            }
        )
    return proxy_list


# 测试代理，建立代理ip池
def proxy_poll():
    headers = {'User-Agent': get_random_useragent()}
    # 可用代理ip列表
    userful_proxy = []
    proxy_list = get_ip_list()
    for proxy in proxy_list:
        try:
            res = requests.get(url='http://httpbin.org/get', headers=headers, proxies=proxy,
                           timeout=5)
            userful_proxy.append(proxy)
        except Exception as e:
            print('{}不能用'.format(proxy))
            continue


if __name__ == "__main":
    proxy_poll()



