#!/usr/bin/python
#-*- encoding: utf-8 -*-
import os
import sys
import ConfigParser
import time
from lxml.html.soupparser import fromstring
from lxml.html import tostring
reload(sys)
sys.setdefaultencoding('utf8')

url_list = ['http://bj.meituan.com/category/meishi/jiuxianqiao?mtt=1.index%2Fdefault%2Fpoi.0.0.ihdisek5']


def ParseMsg(msgdiv=None):
    msgdiv = fromstring(msgdiv)
    buss_name = msgdiv.xpath("//a[@class='link f3']")[0].text_content()
    buss_name = buss_name.decode('unicode_escape')
    buss_name = buss_name.encode('utf-8')
    # print tostring(buss_name, encoding='utf-8')
    print buss_name
    print '------------------------------------>>>>>>>>>>>'


def http_downloader(url):
    from downloader import Downloader
    downer = Downloader()
    hostpagehtml = downer.getContent(url)
    if hostpagehtml:
        root = fromstring(hostpagehtml)
        msgdivs = root.xpath("//div[@class='poi-tile__info']")
        for msg in msgdivs:
            msgdiv = tostring(msg, encoding='utf-8')
            print msgdiv
            ParseMsg(msgdiv)
        pass
    print url, '\n is over'

if __name__ == '__main__':
    for url in url_list:
        # print url
        http_downloader(url)
    print 'crawle over...'