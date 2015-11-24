#!/usr/bin/python
#-*- encoding: utf-8 -*- 

# import gevent
from cookielib import CookieJar
import gzip
import StringIO
import cStringIO
import urllib2
import sys
import traceback
import os
import time
reload(sys) 
sys.setdefaultencoding('utf8')


class Downloader():
    # def __init__(self, proxy_list):
    #     self.proxy_list = proxy_list
      
    def getHtmlSource(self, url, proxy):
        #print '=========',proxy
        s = time.time()
        content = self.getContent(url, proxy)
        for i in range(2):
            if content == "":
                content = self.getContent(url, proxy)
            else:
                break
        e = time.time()
#        print 'proxy: %s content len: %s' %(proxy,len(content))
        return dict(url=url, data=content, proxy=proxy, timecost=e - s)
    
    def getContent(self, url, proxy=None):
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
        content = ""
        try:
            request = urllib2.Request(url)
            request.add_header("Host", "bj.meituan.com")
            request.add_header('User-Agent', agent)
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            request.add_header('Connection', 'keep-alive')
            request.add_header('Accept-encoding', 'gzip, deflate, sdch')
            request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            request.add_header('Accept-Charset', 'GB2312,utf-8;q=0.7,*;q=0.7')
            request.add_header('Referer', "http://bj.meituan.com/category/meishi/chaoyangqu?mtt=1.index%2Fdefault%2Fpoi.0.0.ihdis970")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))
            content = opener.open(request, timeout=30).read()
        except Exception, e:
            content = ""
        if content[:6] == '\x1f\x8b\x08\x00\x00\x00':
            content = gzip.GzipFile(fileobj=cStringIO.StringIO(content)).read()
        # content = content.decode('unicode_escape')
        if content != "":
            content = content.encode('utf-8')
        return content
    
    def gzipData(self, spiderData):
        """
            get data from gzip
        """
        if 0 == len(spiderData):
            return spiderData
        spiderDataStream = StringIO.StringIO(spiderData)
        spiderData = gzip.GzipFile(fileobj=spiderDataStream).read()
        return spiderData