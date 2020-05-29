# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
class FireFoxDrive(object):
    def open_driver_by_url(self, url):
        driver = webdriver.Firefox(executable_path="E:\\baixin\\hushenmin\\PycharmProjects\\crawl-stock\\geckodriver.exe")
        driver.minimize_window()
        # driver.implicitly_wait(30)
        driver.get(url)
        return  driver