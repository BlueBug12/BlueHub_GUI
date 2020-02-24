# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import logging
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, Comment

class crawler:
	def __init__(self):
		self.headers = {
		    'Accept': '*/*',
		    'Accept-Encoding': 'gzip,deflate,sdch',
		    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
		    'Connection': 'keep-alive',
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
		}
		
	def start(self,department,display=0):
		self.session = requests.Session()
		self.session.headers.update(self.headers)
		options = webdriver.ChromeOptions()
		driverpath = "./driver/chromedriver.exe"
		if(display==0):
			options.add_argument('--headless')
			options.add_argument('--disable-gpu')
			
		driver = webdriver.Chrome(executable_path=driverpath,chrome_options=options)
		driver.get("https://course.ncku.edu.tw/index.php?c=qry_all")
		#ee=driver.find_element_by_xpath("//*[@id=\"main_content\"]/div[1]/div[10]/div/div[2]/li[1]")
		try:
			driver.find_element_by_xpath("//*[contains(text(),'%s')]"%(department)).click()
		except NoSuchElementException:
			print("Can't find the element!")
			driver.close()
			return 0
		
		time.sleep(5)
		self.html = driver.page_source
		time.sleep(2)
		driver.close()
		return self.html
		
def main():
	c=crawler()
	c.start('F7',1)
		
if __name__ == '__main__':
	main()


#soup=BeautifulSoup(html,'html.parser')
#data=soup.body.find("div",{"class":"hidden-xs hidden-sm"})
#data=data.find_all("tr")
#for index in range(1,len(data)):
#	item=data[index].find_all("td")
#	if(item[1].find("div").text!=""):
#		print(item[1].find("div").text)#code
#		for element in item[7](text=lambda it: isinstance(it, Comment)):
#			element.extract()#remove html comment
#		temp=item[7].find_all(text=True,recursive=False)#avoid reading children text
#		
#		s=''
#		print(s.join(temp))#balance
#		print(item[0].text)#deparent
#		print(item[2].text)#year&class
#		print(item[4].find(class_="course_name").text)#name
#		print(item[5].text)#attr
#		print(item[6].text)#professor
#		print("")