# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import Text_Analysis.text_mining as tm

from hushenmin.util.FireFoxDriver import FireFoxDrive


class WebCrawler:
    def __init__(self, **kwarg):
        self.dbName = kwarg['dbName']
        self.colName = kwarg['collectionName']
        self.IP = kwarg['IP']
        self.PORT = kwarg['PORT']
        self.Prob = .10
        self.realtimeNewsURL = []
        self.tm = tm.TextMining(IP="10.3.5.58", PORT=27017)

    def ConnDB(self):
        '''Connect mongodb.
        '''
        Conn = MongoClient(self.IP, self.PORT)
        db = Conn[self.dbName]
        self._collection = db.get_collection(self.colName)

    def craw_cn_sink_into_mongo(self, url, start_page_number, end_page_number):
        self.ConnDB()
        driver = FireFoxDrive().open_driver_by_url(url)
        for pageId in range(start_page_number, end_page_number + 1):
            driver.find_element_by_css_selector('#j_more_btn').click()
        resp = driver.page_source.encode('utf-8')
        # driver.close()
        bs = BeautifulSoup(resp, "lxml")
        a_list = bs.find_all('a')
        for a in a_list:

            if 'href' in a.attrs and 'target' in a.attrs and 'title' in a.attrs \
                    and a['href'].find(url) != -1:
                print(a.parent)
                date, article = self.getUrlInfo(a['href'])
                while article == '' and self.Prob >= .1:
                    self.Prob -= .1
                    date, article = self.getUrlInfo(a['href'])
                self.Prob = .5
                if article != '':
                    data = {'Date': date,
                            'Address': a['href'],
                            'Title': a['title'],
                            'Article': article
                            }
                    print(data)
    def getUrlInfo(self, url):
        '''Analyze website and extract useful information.
        '''
        respond = requests.get(url)
        respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
        bs = BeautifulSoup(respond.text, "lxml")
        span_list = bs.find_all('span')
        part = bs.find_all('p')
        article = ''
        date = ''
        for span in span_list:
            if 'class' in span.attrs and span['class'] == ['timer']:
                date = span.text
                break

        for paragraph in part:
            chnstatus = self.countchn(str(paragraph))
            possible = chnstatus[1]
            if possible > self.Prob:
                article += str(paragraph)

        while article.find('<') != -1 and article.find('>') != -1:
            string = article[article.find('<'):article.find('>') + 1]
            article = article.replace(string, '')
        while article.find('\u3000') != -1:
            article = article.replace('\u3000', '')

        article = ' '.join(re.split(' +|\n+', article)).strip()

        return date, article
    def countchn(self, string):
        '''Count Chinese numbers and calculate the frequency of Chinese occurrence.

        # Arguments:
            string: Each part of crawled website analyzed by BeautifulSoup.
        '''
        pattern = re.compile(u'[\u1100-\uFFFDh]+?')
        result = pattern.findall(string)
        chnnum = len(result)
        possible = chnnum / len(str(string))
        return (chnnum, possible)

if __name__ == '__main__':
    web_crawler = WebCrawler(IP="10.3.5.58", PORT=27017, ThreadsNum=4, dbName="Cnstock_Stock",
                             collectionName="cnstock_news_company")
    web_crawler.craw_cn_sink_into_mongo('http://company.cnstock.com/company/scp_gsxw/', 1, 2)
