import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from requests.exceptions import ConnectionError
import time
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import os
import json

from speaker.speaker import speak
from mail.mail import send_email
from crawler.crawler import crawler
from sleep.sleep import random_sleep


class main_window:
	def __init__(self,master,USER,PWD):
		self.search_list=[]
		self.pre_list=[]
		self.receiver_dict={}
		self.search_box=[]

		self.user=USER
		self.pwd=PWD
		self.crawling_enable=False
		self.delete_enable=False

		self.master=master
		self.master.title('BlueHub GUI')
		self.master.geometry('520x400')

		self.frame1 = tk.LabelFrame(self.master, text="NCKU選課資料")
		self.frame1.grid(row=1, columnspan=7, \
                 padx=5, pady=5, ipadx=5, ipady=5)

		self.frame2 = tk.LabelFrame(self.master,text="查詢結果:")
		self.frame2.grid(row=2,column=0,columnspan=6, \
                 padx=5, pady=5, ipadx=5, ipady=5,sticky='WNES')

		self.menubar=tk.Menu(self.master)
		tk.Label(self.frame2,width=6,text=' 代碼: ').grid(column=1,row=1)
		tk.Label(self.frame2,width=6,text=' 系所: ').grid(column=1,row=2)
		tk.Label(self.frame2,width=6,text=' 課程: ').grid(column=1,row=3)
		tk.Label(self.frame2,width=6,text=' 教師: ').grid(column=1,row=4)
		tk.Label(self.frame2,width=6,text=' 學分: ').grid(column=1,row=5)
		tk.Label(self.frame2,width=6,text=' 屬性: ').grid(column=1,row=6)
		tk.Label(self.frame2,width=6,text=' 時間: ').grid(column=1,row=7)
		tk.Label(self.frame2,width=6,text=' 餘額: ').grid(column=1,row=8)

		self.r_var1=tk.StringVar()
		self.r_var2=tk.StringVar()
		self.r_var3=tk.StringVar()
		self.r_var4=tk.StringVar()
		self.r_var5=tk.StringVar()
		self.r_var6=tk.StringVar()
		self.r_var7=tk.StringVar()
		self.r_var8=tk.StringVar()


		self.r_var1.set('               ')
		self.r_var2.set('               ')
		self.r_var3.set('               ')
		self.r_var4.set('               ')
		self.r_var5.set('               ')
		self.r_var6.set('               ')
		self.r_var7.set('               ')
		self.r_var8.set('               ')

		tk.Label(self.frame2,width=10,textvariable=self.r_var1).grid(column=2,row=1)
		tk.Label(self.frame2,width=10,textvariable=self.r_var2).grid(column=2,row=2)
		tk.Label(self.frame2,width=10,textvariable=self.r_var3).grid(column=2,row=3)
		tk.Label(self.frame2,width=10,textvariable=self.r_var4).grid(column=2,row=4)
		tk.Label(self.frame2,width=10,textvariable=self.r_var5).grid(column=2,row=5)
		tk.Label(self.frame2,width=10,textvariable=self.r_var6).grid(column=2,row=6)
		tk.Label(self.frame2,width=10,textvariable=self.r_var7).grid(column=2,row=7)
		tk.Label(self.frame2,width=10,textvariable=self.r_var8).grid(column=2,row=8)

		self.search_lab=tk.Label(self.frame1,text='爬蟲列表:')
		self.search_lab.grid(column=1,row=4)

		self.search_var=tk.StringVar()
		self.search_var.set('(如需刪除再點選)')
		self.search_list_box=ttk.Combobox(self.frame1,width=25,value=self.search_box,state='readonly',textvariable=self.search_var)
		self.search_list_box.grid(column=2,columnspan=2,row=4)

		self.search_cancel_btn=tk.Button(self.frame1,text='刪除',command=lambda :self.thread_it(self.delete_guard))
		self.search_cancel_btn.grid(column=4,row=4)

		self.frame3 = tk.LabelFrame(self.master,text="爬蟲紀錄")
		self.frame3.grid(row=2,column=6,columnspan=7, \
                 padx=5, pady=5, ipadx=5, ipady=5)

		self.crawling_history=tk.Text(self.frame3,height=10,width=30)
		self.crawling_history.grid(column=1,row=1)

		self.file_read()

		self.course_code_lab=tk.Label(self.frame1,text='課程代碼:')
		self.course_code_lab.grid(column=1,row=1,sticky='E')

		self.course_code_var=tk.StringVar()
		self.course_code_entry=tk.Entry(self.frame1,width=7,textvariable=self.course_code_var)
		self.course_code_entry.grid(column=2,row=1,sticky='W')

		self.search_btn=tk.Button(self.frame1,text='查詢',command=lambda :self.thread_it(self.show_data))
		self.search_btn.grid(column=2,row=1)
		
		self.ip_var=tk.StringVar()
		self.ip_var.set('')
		
		#self.ip_lab=tk.Label(self.frame1,width=7,text="IP:",textvariable=self.ip_var)
		#self.ip_lab.grid(column=3,row=1)
		tk.Label(self.frame1,width=4,text='IP: ').grid(column=3,row=1,sticky='E')
		tk.Label(self.frame1,width=12,textvariable=self.ip_var).grid(column=4,columnspan=3,row=1,sticky='W')
		
		self.email_lab=tk.Label(self.frame1,width=10,text='收件人Email:')
		self.email_lab.grid(column=1,row=2,sticky='E')

		self.email_var=tk.StringVar()
		self.email_var.set('請選擇收件人')
		self.emailChosen=ttk.Combobox(self.frame1,width=31,state="readonly",value=self.dict_to_list(self.receiver_dict),textvariable=self.email_var)
		self.emailChosen.grid(column=2,columnspan=4,row=2,sticky='W')

		self.new_email_btn=tk.Button(self.frame1,text='新增',command=self.add_email)
		self.new_email_btn.grid(column=5,row=2)

		self.add_btn=tk.Button(self.frame1,text='加入列表',command=lambda :self.thread_it(self.add_node))
		self.add_btn.grid(column=5,row=4,sticky='W')

		self.crawler_var=tk.StringVar()
		self.crawler_var.set('開始爬蟲')
		self.crawler_btn=tk.Button(self.frame3,textvariable=self.crawler_var,command=lambda :self.thread_it(self.crawling))
		self.crawler_btn.grid(column=1,columnspan=2,row=7)

	def dict_to_list(self,di):
		li=[]
		for key in di.keys():
			li.append(key+'-'+di[key])
		return li

	def add_email(self):
		new_win=tk.Tk()
		new_win.geometry('400x100')


		tk.Label(new_win, text='Email: ').grid(column=1,row=1)
		tk.Label(new_win, text='使用者名稱: ').grid(column=1,row=2)

		user_account_var = tk.StringVar()
		e1=tk.Entry(new_win, width=30,textvariable=user_account_var)
		e1.grid(column=2,row=1)

		user_name_var = tk.StringVar()
		e2=tk.Entry(new_win,width=30, textvariable=user_name_var)
		e2.grid(column=2,row=2)

		def send_to_test(user,pwd):
			email=e1.get()
			data={
				"user":user,
				"pwd":pwd,
				"subject":'test',
				"name":"BlueHub",
				"to":email,
				"body":'This is BlueHub.Copy That?'
			}
			if not send_email(data):
				self.crawling_history.insert(tk.INSERT,'發信失敗\n')
				self.crawling_history.insert(tk.INSERT,'\n')
			else:
				self.crawling_history.insert(tk.INSERT,'發信成功\n')
				self.crawling_history.insert(tk.INSERT,'\n')




		def write_and_close():

			email=e1.get()
			name=e2.get()
			if(len(email)==0 or len(name)==0):
				tk.messagebox.showwarning(title='Warning', message='請填入完整資料!')

			else:
				if(email[0]==''or name[0]==''):
					tk.messagebox.showwarning(title='Warning', message='請填入完整資料!')

				else:
					self.file_write(email,name)
					print(self.receiver_dict)
					self.email_var.set('請選擇收件人')
					ttk.Combobox(self.frame1,width=31,value=self.dict_to_list(self.receiver_dict),textvariable=self.email_var).grid(column=2,columnspan=4,row=2,sticky='W')
					close_new_win()

		def close_new_win():
			new_win.destroy()

		little_frame=tk.Frame(new_win)
		little_frame.grid(column=2,row=3)
		tk.Button(little_frame,width=10,text='測試',command=lambda :self.thread_it(send_to_test(self.user,self.pwd))).grid(column=0,row=1)
		tk.Button(little_frame,width=10, text='確認', command=write_and_close).grid(column=2,row=1)
		tk.Button(little_frame,width=10,text='取消',command=close_new_win).grid(column=1,row=1)
		new_win.mainloop()

	def add_node(self):


		if(self.email_var.get()=='請選擇收件人'):
			tk.messagebox.showwarning(title='Warning', message='尚未選取收件人!')
			return(0)

		if(self.course_code_var.get()==''):
			tk.messagebox.showwarning(title='Warning', message='尚未填入課程代碼!')
			return(0)
		info={}
		for i in self.pre_list:
			if i['code']==self.course_code_var.get().upper():
				mail_and_name=self.email_var.get()
				info=i
				info['user']=mail_and_name.split('-')[0]
				info['mail']=mail_and_name.split('-')[1]
				break
		if not info:
			try:
				info=self.search_data(add=1)
			except ConnectionError:
				tk.messagebox.showerror(title='Error', message='網路連線異常!')

		if(info):
			#record all data
			for item in self.search_list:
				if(item==info):
					tk.messagebox.showwarning(title='Warning', message='列表已存有資料!')
					return(0)

			self.search_list.append(info)
			self.search_box.append(info['user']+'-'+info['name'])
			self.search_list_box=ttk.Combobox(self.frame1,width=25,value=self.search_box,state='readonly',textvariable=self.search_var)
			self.search_list_box.grid(column=2,columnspan=2,row=4)
			self.crawling_history.insert(tk.INSERT,info['name']+' 成功加入列表\n\n')
			return(1)

	def delete_guard(self):
		if(	self.search_var.get()=='(如需刪除再點選)'):
			return(0)

		else:
			if(self.crawling_enable==False):
				self.delete_node()

			else:
				self.delete_enable=True

	def delete_node(self,index=-1):
		if(index==-1):
			index=self.search_list_box.current()

		del self.search_box[index]
		del self.search_list[index]
		self.search_var.set('(如需刪除再點選)')
		self.search_list_box=ttk.Combobox(self.frame1,width=25,value=self.search_box,state='readonly',textvariable=self.search_var)
		self.search_list_box.grid(column=2,columnspan=2,row=4)
		self.delete_enable=False

	def show_data(self):
		try:
			info=self.search_data()
		except ConnectionError:
			tk.messagebox.showerror(title='Error', message='網路連線異常!')

		if(info):
			self.r_var1.set(info['code'])
			self.r_var2.set(info['department'])#course name
			self.r_var3.set(info['name'])#name of professor
			self.r_var4.set(info['professor'])#course time
			self.r_var5.set(info['credit'])#balance of course
			self.r_var6.set(info['attr'])#name of professor
			self.r_var7.set(info['time'])#course time
			self.r_var8.set(info['balance'])#balance of course

			self.pre_list.append(info)

	def search_data(self,add=0):
		course_code=self.course_code_var.get().upper()
		if not add:
			self.crawling_history.insert(tk.INSERT,'搜尋中...\n')
		else:
			self.crawling_history.insert(tk.INSERT,'加入列表中...\n\n')
		for item in self.search_list:
			if(course_code == item['code']):
				tk.messagebox.showinfo(title='Prompt', message='課程已搜尋!')


		c=crawler()
		html=c.start(course_code[0:2])
		self.ip_var.set("               ")
		self.ip_var.set(c.IP())
		if not html:
			return {}
		soup=BeautifulSoup(html,'html.parser')
		data=soup.body.find("div",{"class":"hidden-xs hidden-sm"})
		data=data.find_all("tr")
			
		if not data:
			tk.messagebox.showerror(title='Error', message='課程代碼錯誤!')

		else:
			#find the course of the code
			for index in range(1,len(data)):
				item=data[index].find_all("td")

				if(item[1].find("div").text!="" and course_code==''.join(item[1].find("div").text.split('-'))):
					for element in item[7](text=lambda it: isinstance(it, Comment)):
						element.extract()#remove html comment

					if(add):
						mail_and_name=self.email_var.get()
						u=mail_and_name.split('-')[0]
						m=mail_and_name.split('-')[1]
					else:
						u=""
						m=""

					information={
						'code':course_code,
						'index':index,
						'user':u,
						'mail':m,
						'department':item[0].text,
						'year_class':item[2].text,
						'name':item[4].find(class_="course_name").text,
						'professor':item[6].text,
						'balance':''.join(item[7].find_all(text=True,recursive=False)),
						'time':''.join(item[8].find_all(text=True,recursive=False)),
						'credit':item[5].text.split('  ')[0],
						'attr':item[5].text.split('  ')[1],
						'counter':0
					}
					if not add:
						self.crawling_history.insert(tk.INSERT,'搜尋完成\n\n')
				
					return information
		
			tk.messagebox.showwarning(title='Warning', message='查無此課程!')
			if not add:
				self.crawling_history.insert(tk.INSERT,'搜尋失敗\n\n')
			else:
				self.crawling_history.insert(tk.INSERT,'加入列表失敗\n\n')

	def thread_it(self,func,*args):
		#mutlithreading
		print('Number of threads:',end='')
		if(threading.active_count()>=10):
			print("Too much threads!")
			self.crawling_history.insert(tk.INSERT,'點擊過快，請稍後再試\n\n')
		else:
			print(threading.active_count())

		added_t1 = threading.Thread(target=func,args=args)
		added_t1.start()

	def stop_crawling(self):
		self.crawling_enable=False

	def timer(self):
		now = datetime.now()
		now_str=str(now.hour)+":"+str(now.minute)+":"+str(now.second)
		return(now_str)

	def file_write(self,email,name):
		if not self.receiver_dict:
			try:
				os.mkdir("json")
			except FileExistsError:
				pass
			finally:
				self.receiver_dict = {'我': self.user}
				with open("./json/receivers.json", 'w') as f:
					json.dump(self.receiver_dict,f)

				self.crawling_history.insert(tk.INSERT,"建檔完成!\n\n")
		else:
			new_dict={name:email}
			self.receiver_dict.update(new_dict)
			try:
				with open("./json/receivers.json", 'w') as f:
					json.dump(self.receiver_dict,f)
			except:
				print('Something wrong when write file')
				self.crawling_history.insert(tk.INSERT,"寫檔錯誤!\n\n")


	def file_read(self,json_path="./json/receivers.json"):

		try:
			with open(json_path,'r') as f:
				self.receiver_dict = json.load(f)

		except:
			print('Something wrong when read file')
			self.crawling_history.insert(tk.INSERT,"讀檔錯誤!\n")
			self.crawling_history.insert(tk.INSERT,"重建新檔中...\n\n")
			self.file_write(self.user,"我")


	def crawling(self):
		index=len(self.search_list)
		if(self.crawler_var.get()=='停止爬蟲'):
			self.stop_crawling()
			return(0)

		if(index==0):
			tk.messagebox.showwarning(title='Warning', message='列表中尚無資料!')
			return(0)

		else:
			connection_counter=0
			self.crawling_enable=True
			self.crawler_var.set('停止爬蟲')
			self.crawling_history.insert(tk.INSERT,"時間"+self.timer()+'\n')
			self.crawling_history.insert(tk.INSERT,'開始爬蟲\n\n')

			while(self.crawling_enable and len(self.search_list)!=0):

				upper=len(self.search_list)
				i=0
				flag=0
				while(i<upper):

					if(self.crawling_enable==False):break
					if(self.delete_enable==True):
						self.delete_node()
						break

					node=self.search_list[i]

					try:
						c=crawler()
						html=c.start(node['code'][0:2])
						self.ip_var.set("               ")
						self.ip_var.set(c.IP())
						if not html:
							raise ConnectionError

						soup=BeautifulSoup(html,'html.parser')
						data=soup.body.find("div",{"class":"hidden-xs hidden-sm"})
						data=data.find_all("tr")

					except ConnectionError:
						if(connection_counter>3):
							os._exit(0)
						else:
							print("Connection error!")
							self.crawling_history.insert(tk.INSERT,'網路連線異常\n\n')
							time.sleep(2)
							connection_counter+=1
							break
					except AttributeError:
						print("AttributeError !")
						time.sleep(2)
						flag+=1
						if(flag>3):
							break
						continue
						

					item=data[node['index']].find_all("td")
					for element in item[7](text=lambda it: isinstance(it, Comment)):
						element.extract()#remove html comment
					balance=item[7].find_all(text=True,recursive=False)#avoid reading children text
					#print(item[4].find(class_="course_name").text)
					if(''.join(balance).split('/')[1]!=u'額滿'):

						now_str=self.timer()
						self.crawling_history.insert(tk.INSERT,'時間'+now_str+'\n')
						self.crawling_history.insert(tk.INSERT,node['professor']+node['name']+' 有餘額'+'\n\n')
						self.thread_it(speak,(node['code']+node['professor']+node['name']+'有餘額'+'\n'))#speak the class


						number=node['counter']
						if(number<2):
							if(number==0):
								#first time send an email
								info={
									"user":self.user,
									"pwd":self.pwd,
									"subject":node['name']+" "+'('+node['professor']+')'+' 尚有餘額',
									"name":"BlueHub",
									"to":node['mail'],
									"body":'course code:'+node['code']+node['name']+'<br> at time '+now_str
								}

								if not send_email(info):
									self.crawling_history.insert(tk.INSERT,'發信失敗\n')
									self.crawling_history.insert(tk.INSERT,'\n')
								else:
									self.crawling_history.insert(tk.INSERT,'發信成功\n')
									self.crawling_history.insert(tk.INSERT,'\n')


							self.search_list[i]['counter']+=1

						#delete the node after three times
						else:
							self.delete_node(index=i)
							upper=len(self.search_list)
							i-=1
					else:
						#recounting
						self.search_list[i]['counter']=0

					i+=1
					random_sleep()

			self.crawler_var.set('開始爬蟲')
			self.crawling_history.insert(tk.INSERT,"時間"+self.timer()+'\n')
			self.crawling_history.insert(tk.INSERT,'結束爬蟲\n\n')