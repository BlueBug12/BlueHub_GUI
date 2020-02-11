# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from bs4 import BeautifulSoup, Comment

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'leetcode.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

HOME = Path.cwd()
COOKIE_PATH = Path.joinpath(HOME, 'cookies.json')
session = requests.Session()
session.headers.update(HEADERS)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
	
#	driver = webdriver.Chrome(
#		executable_path=executable_path
#	)
driver = webdriver.Chrome()
#driver = webdriver.Chrome(chrome_options=options)
driver.get("https://course.ncku.edu.tw/index.php?c=qry_all")
ee=driver.find_element_by_xpath("//*[@id=\"main_content\"]/div[1]/div[10]/div/div[2]/li[1]")
ActionChains(driver).click(ee).perform()
time.sleep(5)
html = driver.page_source
print(html)
soup=BeautifulSoup(html,'html.parser')
data=soup.body.find("div",{"class":"hidden-xs hidden-sm"})
data=data.find_all("tr")
for index in range(1,len(data)):
	item=data[index].find_all("td")
	if(item[1].find("div").text!=""):
		print(item[1].find("div").text)#code
		for element in item[7](text=lambda it: isinstance(it, Comment)):
			element.extract()#remove html comment
		temp=item[7].find_all(text=True,recursive=False)#avoid reading children text
		
		s=''
		print(s.join(temp))#balance
		print(item[0].text)#deparent
		print(item[2].text)#year&class
		print(item[4].find(class_="course_name").text)#name
		print(item[5].text)#attr
		print(item[6].text)#professor
		print("")