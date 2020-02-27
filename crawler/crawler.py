from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
import time

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
		try:
			driver.find_element_by_xpath("//*[contains(text(),'%s')]"%(department)).click()
		except NoSuchElementException:
			print("Can't find the element!")
			driver.close()
			return 0

		time.sleep(5)
		self.html = driver.page_source
		#time.sleep(2)
		driver.close()
		return self.html