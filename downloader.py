#!/usr/bin/python
#-*- encoding: utf-8 -*- 

import gevent
from cookielib import CookieJar
import gzip
import StringIO
import cStringIO
import urllib2
import sys
import traceback
from util.gl_log import logger
import os
import time
reload(sys) 
sys.setdefaultencoding('utf8')


class Downloader():
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
      
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
    
    def getContent(self, url, proxy):
        content = ""
        try:
            request = urllib2.Request(url)
            request.add_header("Host", "weibo.cn")
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0')
            #request.add_header('User-Agent', 'android')
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            request.add_header('Connection', 'keep-alive')
            request.add_header('Accept-encoding', 'gzip, deflate')
            request.add_header('Accept-Language', 'zh-cn,zh;q=0.5')
            request.add_header('Accept-Charset', 'GB2312,utf-8;q=0.7,*;q=0.7')
            request.add_header('Referer', "http://weibo.cn/")
            
            proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy})
            opener = urllib2.build_opener(proxy_handler) 

            response = None
            with gevent.Timeout(10, False) as timeout:
                    response = opener.open(request, timeout=5)
            if response is not None:
                #print  response.info()
                if response.info().get("Content-Encoding") == 'gzip':
                    content = self.gzipData(response.read())
                else:
                    content = response.read()
        except Exception, e:
             content = ""
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