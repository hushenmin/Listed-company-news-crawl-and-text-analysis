import time, re, requests
from concurrent import futures
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium.webdriver import ActionChains

import Text_Analysis.text_mining as tm
from selenium import webdriver


def get_content_from_request(param):
    pass


# if __name__ == '__main__':
    # print('==============================================================')
    # urls = []
    # urls.append('http://company.cnstock.com/company/scp_gsxw/')
    # # for pageId in range(1, 611 + 1):
    # #     urls.append('http://company.cnstock.com/company/scp_gsxw/' + str(pageId))
    # for url in urls:
    #     print(url)
    #     print('---------------------------------------------------------------')
    #     resp = requests.get(url)
    #     resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding
    #     bs = BeautifulSoup(resp.text, "lxml")
    #     a_list = bs.find_all('a')
    #     print(len(a_list))
    #     for a in a_list:
    #         if 'href' in a.attrs and 'target' in a.attrs and 'title' in a.attrs \
    #                 and a['href'].find('http://company.cnstock.com/company/') != -1:
    #             print(a)
def get_content_from_request(url):
        resp = requests.get(url)
        resp.encoding = BeautifulSoup(resp.content,'lxml')
        bs = BeautifulSoup(resp.text,'lxml')
        a_list = bs.find_all('a')
        print(len(a_list))
        for a in a_list:
            if 'href' in a.attrs and 'target' in a.attrs and 'title' in a.attrs \
                and a['href'].find(url) != -1:
                print(a.parent)
def get_content_from_driver(url):
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        driver.minimize_window()
        driver.implicitly_wait(3)
        driver.get('http://company.cnstock.com/company/scp_gsxw/')
        for i in range(0, 100):
            driver.find_element_by_css_selector('#j_more_btn').click()
        html = driver.page_source
        print(html)
        bs = BeautifulSoup(html, "lxml")
        a_list = bs.find_all('a')
        print(len(a_list))
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for a in a_list:
            if 'href' in a.attrs and 'target' in a.attrs and 'title' in a.attrs \
                    and a['href'].find('http://company.cnstock.com/company/') != -1:
                print(a)
if __name__ == '__main__':
    get_content_from_request('http://company.cnstock.com/company/scp_gsxw/')