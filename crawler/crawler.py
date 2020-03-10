from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
#from fake_useragent import UserAgent
import time
import os

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
		self.ip=""
		
	def start(self,department,display=0):
		os.system("start /b .\\tor_browser\\Tor\\tor.exe")
		time.sleep(2)
#		self.session = requests.Session()
#		self.session.headers.update(self.headers)
		opts = Options()
		opts.add_argument("--incognito")
		proxy = "socks5://localhost:9050"
		opts.add_argument('--proxy-server={}'.format(proxy))
		ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
		#ua = UserAgent()
		opts.add_argument("user-agent={}".format(ua))
		driverpath = "./driver/chromedriver.exe"
		if(display==0):
			opts.add_argument('--headless')
			opts.add_argument('--disable-gpu')

		driver = webdriver.Chrome(executable_path=driverpath,chrome_options=opts)
		driver.get("https://course.ncku.edu.tw/index.php?c=qry_all")
		try:
			driver.find_element_by_xpath("//*[contains(text(),'%s')]"%(department)).click()
		except NoSuchElementException:
			print("Can't find the element!")
			driver.close()
			os.system("TASKKILL /F /IM tor.exe")
			return 0
		
		
		time.sleep(5)
		self.html = driver.page_source
		driver.close()
		driver = webdriver.Chrome(executable_path=driverpath,chrome_options=opts)
		driver.get('https://www.whatismyip.com.tw/')
		time.sleep(5)
		try:
			self.ip=driver.find_element_by_xpath("/html/body/b/span").text
		except NoSuchElementException:
			print("Can't find your IP!")
			driver.close()
			os.system("TASKKILL /F /IM tor.exe")
			return 0
		
		#time.sleep(2)
		driver.close()
		os.system("TASKKILL /F /IM tor.exe")
		#self.session.close()
		return self.html
	
	def IP(self):
		return self.ip

if __name__ == '__main__':
	c=crawler()
	c.start('E2',1)