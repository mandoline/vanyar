#!/usr/bin/env python
# coding=utf-8
import sys
import urllib, urllib2, urlparse
import json
import pymongo
# from bs4 import BeautifulSoup

ApiKey = '5ea95067a6d97afe0a1d27c5042af990'
CityUrl = 'http://apis.baidu.com/baidunuomi/openapi/cities'
ShopUrl = 'http://apis.baidu.com/baidunuomi/openapi/searchshops'
ShopUrl2 = 'http://apis.baidu.com/apistore/location/near'
CatUrl = 'http://apis.baidu.com/baidunuomi/openapi/categories'
DistrictsUrl = 'http://apis.baidu.com/baidunuomi/openapi/districts'
ShopInfoUrl = 'http://apis.baidu.com/baidunuomi/openapi/shopinfo'


class BDApiServer(object):

    def _get_res(self, url):
        req = urllib2.Request(url)
        req.add_header("apikey", ApiKey)
        resp = urllib2.urlopen(req)
        content = resp.read()
        return content

    def get_city(self):
        content = self._get_res(CityUrl)
        # f = open('city.data.txt', 'wr')
        # if content:
        #     f.write(content)
        # f.close()
        url = 'http://apis.baidu.com/baidunuomi/openapi/cities'

        req = urllib2.Request(url)
        req.add_header("apikey", ApiKey)

        resp = urllib2.urlopen(req)
        content = resp.read()
        if content:
            print(content)

    def get_districts(self):
        # params = {
        #     'city_id': '100010000',
        # }
        # data = '?'
        # for k, v in params.iteritems():
        #     data += k + '=' + v + '&'
        # content = self._get_res(DistrictsUrl + data)
        # f = open('districts.data.txt', 'wr')
        # if content:
        #     f.write(content)
        # f.close()
        '''
           strict_name":"朝阳区",
          "district_id":307,
          "biz_areas":[
              {
              ┊   "biz_area_name":"酒仙桥",
              ┊   "biz_area_id":1319
              }
                :return:
        '''
        url = 'http://apis.baidu.com/baidunuomi/openapi/districts?city_id=100010000'

        req = urllib2.Request(url)
        req.add_header("apikey", ApiKey)
        resp = urllib2.urlopen(req)
        content = resp.read()
        if content:
            print(content)

    def get_category(self):
        content = self._get_res(CatUrl)
        content_json = json.loads(content, encoding="utf-8")
        categories = content_json.get('categories')
        for cat in categories:
            if cat.get('cat_id') == 326:
                # print cat
                # f = open('cat.data.txt', 'wr')
                # f.write(str(cat).encode('utf-8'))
                # f.close()
                return cat

    def get_shops(self):
        params = {
            'city_id': '100010000',
            'location': '39.972684,116.492531',
            'cat_ids': '326',
            'district_ids': '307',
            'bizarea_ids': '1319',
            'radius': '3000',
            'page': '1',
            'page_size': '300',
            'deals_per_shop': '3',
        }
        data = '?'
        for k, v in params.iteritems():
            data += k + '=' + v + '&'
        content = self._get_res(ShopUrl + data)
        f = open('shops.data.txt', 'wr')
        if content:
            f.write(content)
        f.close()

    def get_shops2(self):
        params = {
            'keyWord': '饭店',
            'location': '39.972684, 116.492531',
            'radius': '3000',
            'page': '1',
            'number': '30',
        }
        data = '?'
        for k, v in params.iteritems():
            data += k + '=' + v + '&'
        content = self._get_res(ShopUrl2 + data)
        print content

    def get_shop_info(self, url, name):
        # url = ShopInfoUrl + '?shop_id=%s' % shop_id
        # content = self._get_res(url)
        res = urllib2.urlopen(url)
        f = open('shops/%s.html' % name, 'wr')
        f.write(res.read())
        f.close()

    def load_shops(self, download_info=False):
        f = open('shops.data.txt')
        a = f.read()
        shops = json.loads(a)['data']['shops']
        f.close()
        df = open('shopInfo.data.txt', 'wr')
        for shop in shops:
            # shop_data = self.get_shop_info(shop['shop_id'])
            # df.write(shop_data+'\n')
            data = {
                'name': shop['shop_name'],
                'url': shop['shop_url'],
                'shop_id': shop['shop_id'],
            }
            if download_info:
                self.get_shop_info(shop['shop_url'], shop['shop_name'])
            print shop['shop_url']
        df.close()
        print len(shops)

    def load_shop_info(self):
        f = open('shops.data.txt')
        a = f.read()
        shops = json.loads(a)['data']['shops']
        f.close()
        df = open('shopInfo.data.txt', 'wr')
        for shop in shops:
            name = shop['shop_name']
            shop_id = shop['shop_id']
            f = open('shops/%s.html' % name)
            soup = BeautifulSoup(f, 'lxml')
            logo = soup.select('.shop-logo > img')[0]
            shop_info_list = soup.select('.shop-list > li')

            address = shop_info_list[0].select('p > span')[0]
            phone = shop_info_list[1].select('p')[0]
            print len(shop_info_list)
            if len(shop_info_list) > 2:
                tags = shop_info_list[2].select('p')
            else:
                tags = []
            print name
            print shop_id
            print logo.attrs['src']
            print address.text
            print phone.text
            print tags

    def get_connect(cls):
        conn = pymongo.Connection('mongodb://%s' % "audit:Xx5JEvCg@audit-mongo1:14001,audit-mongo2:14001,"
                                                   "audit-mongo3:14001/audit",port=27017)
        return conn['audit']

    def down_load_shop(self, cat_id=326, subcat_id=327):
        search_url = 'http://apis.baidu.com/baidunuomi/openapi/searchshops'
        params = {
            'cat_ids': cat_id,
            'subcat_ids': subcat_id,
            'district_ids': 307,
            'bizarea_ids': 1319,
             'number': '50',
            'city_id': 100010000,
            # 'keyWord': '饭店',
            # 'location': '39.972684, 116.492531',
            # 'radius': '3000',
            # 'page': '1',
        }
        search_url += '?'
        for k, v in params.iteritems():
            search_url += k + '=' + str(v) + '&'
        has_shop = True
        page = 1
        search_url += 'page='
        while has_shop:
            url = search_url + str(page)
            print 'url:', url
            req = urllib2.Request(url)
            req.add_header("apikey", ApiKey)
            resp = urllib2.urlopen(req)
            content = resp.read()
            content = json.loads(content, encoding="utf-8")
            data = content.get('data')
            if content.get('errno') == 0 and data.get('total') > 0:
            # if content.get('errno') != 1005:
                print 'right....'
                connect = self.get_connect()
                coll = connect['chiwhat']
                shop_msgs = data.get('shops')
                for shop in shop_msgs:
                    coll.insert(shop)
                page += 1
            else:
                print content.get('errno')
                print 'false....'
                break


if __name__ == '__main__':
    api = BDApiServer()
    # api.get_city()
    # api.get_category()
    # api.get_districts()
    # api.get_shops()
    # api.load_shops()
    # api.load_shops(download_info=True)
    category = api.get_category()
    cat_id = category.get('cat_id')
    subcat_ids = category.get('subcategories')
    for subcat in subcat_ids:
        # print cat_id, subcat.get('subcat_id')
        api.down_load_shop(cat_id, subcat.get('subcat_id'))
    print 'done....'
