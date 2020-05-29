# -*- coding: utf-8 -*-
from selenium import webdriver
class FireFoxDrive:
    def open_driver_by_url(self, url):
        driver = webdriver.Firefox(executable_path="geckodriver.exe")
        driver.minimize_window()
        # driver.implicitly_wait(30)
        driver.get(url)
        return  driver