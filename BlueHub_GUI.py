# -*- coding: utf-8 -*-
"""
	@author: BlueBug
"""
import threading
import tkinter as tk
from tkinter import messagebox
import pickle
from tkinter import ttk
from requests.exceptions import ConnectionError
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from gtts import gTTS
from pygame import mixer
import tempfile
import os
from fake_useragent import UserAgent
import random

def random_sleep(min=0.1,max=1.0):
	seed=random.uniform(min,max)
	time.sleep(seed)

def speak(sentence,language='zh-tw',loop=1):
	with tempfile.NamedTemporaryFile(delete=True) as tf:
		tts=gTTS(text=sentence, lang=language)
		tts.save('{}.mp3'.format(tf.name))
		mixer.init()
		mixer.music.load('{}.mp3'.format(tf.name))
		mixer.music.play(loop)
		time.sleep(1)
		
		
class log_in_window:
	def __init__(self,master,account,pwd):
		self.master=master
		self.account=account
		self.pwd=pwd
		master.title('Welcome to BlueHub')
		master.geometry('450x300')
		
		
		# welcome image
		self.canvas = tk.Canvas(master, height=200, width=500)
		self.image_file = tk.PhotoImage(file='welcome.gif')
		self.image = self.canvas.create_image(0,0, anchor='nw', image=self.image_file)
		self.canvas.pack(side='top')

		# user information
		tk.Label(master, text='Gmail Account: ').place(x=50, y= 150)
		tk.Label(master, text='Password: ').place(x=50, y= 190)
		
		#Blue12345py
		self.var_usr_name = tk.StringVar()
		self.entry_usr_name = tk.Entry(master,width=30, textvariable=self.var_usr_name)
		self.entry_usr_name.place(x=160, y=150)

		self.var_usr_pwd = tk.StringVar()
		self.entry_usr_pwd = tk.Entry(master,width=30 ,textvariable=self.var_usr_pwd, show='*')
		self.entry_usr_pwd.place(x=160, y=190)
		self.btn_enter = tk.Button(master, text='Enter', command=self.close_window)
		self.btn_enter.place(x=170, y=230)
		
		master.mainloop()

	def close_window(self):
		self.account.append(self.var_usr_name.get())
		self.pwd.append(self.var_usr_pwd.get())
		self.master.destroy()
   
            
class main_window:
	def __init__(self,master,account,pwd):
		self.search_list=[]#course_code,course_url,counter,course_year,user_email
		#self.email_list=[]
		self.test=[1,2,3]
		self.email_dict={}
		self.search_box=[]
		
		self.account=account
		self.pwd=pwd
		self.crawling_enable=False
		self.delete_enable=False
		#self.file_read()
		
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
		
		tk.Label(self.frame2,width=6,text='系所名稱: ').grid(column=1,row=1)
		tk.Label(self.frame2,width=6,text='課程名稱: ').grid(column=1,row=2)
		tk.Label(self.frame2,width=6,text='教師姓名: ').grid(column=1,row=3)
		tk.Label(self.frame2,width=6,text='上課時間: ').grid(column=1,row=4)
		tk.Label(self.frame2,width=6,text='課程餘額: ').grid(column=1,row=5)
		
		self.r_var1=tk.StringVar()
		self.r_var2=tk.StringVar()
		self.r_var3=tk.StringVar()
		self.r_var4=tk.StringVar()
		self.r_var5=tk.StringVar()
		
		self.r_var1.set('               ')
		self.r_var2.set('               ')
		self.r_var3.set('               ')
		self.r_var4.set('               ')
		self.r_var5.set('               ')
		 
		tk.Label(self.frame2,width=10,textvariable=self.r_var1).grid(column=2,row=1)
		tk.Label(self.frame2,width=10,textvariable=self.r_var2).grid(column=2,row=2)
		tk.Label(self.frame2,width=10,textvariable=self.r_var3).grid(column=2,row=3)
		tk.Label(self.frame2,width=10,textvariable=self.r_var4).grid(column=2,row=4)
		tk.Label(self.frame2,width=10,textvariable=self.r_var5).grid(column=2,row=5)
		
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
		
		self.year_lab=tk.Label(self.frame1, width=10, text='課程年級:')
		self.year_lab.grid(column=1,row=1,sticky='E')       
        
		self.file_read()
		self.year_var=tk.StringVar()
		self.year_var.set(3)
		self.yearChosen=ttk.Combobox(self.frame1,width=5,state='readonly',textvariable=self.year_var)
		self.yearChosen['value']=(0,1,2,3,4)#year of the class
		self.yearChosen.current(3)#normally year2
		self.yearChosen.grid(column=2,row=1,sticky='W')
		
		self.course_code_lab=tk.Label(self.frame1,text='課程代碼:')
		self.course_code_lab.grid(column=3,row=1,sticky='E')
		
		self.course_code_var=tk.StringVar()
		self.course_code_entry=tk.Entry(self.frame1,width=7,textvariable=self.course_code_var)
		self.course_code_entry.grid(column=4,row=1,sticky='W')
		
		self.search_btn=tk.Button(self.frame1,text='查詢',command=lambda :self.thread_it(self.show_data))
		self.search_btn.grid(column=5,row=1)
		
		self.email_lab=tk.Label(self.frame1,width=10,text='收件人Email:')
		self.email_lab.grid(column=1,row=2,sticky='E')
		
		self.email_var=tk.StringVar()
		self.email_var.set('請選擇收件人')
		self.emailChosen=ttk.Combobox(self.frame1,width=33,state="readonly",value=self.dict_to_list(self.email_dict),textvariable=self.email_var)
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
	
	def send_email(self,subject,to_address,body):
		
		try:
			smtpserver = smtplib.SMTP('smtp.gmail.com',587)  
			smtpserver.ehlo()
			smtpserver.starttls()
			smtpserver.ehlo()
			smtpserver.login(self.account[0],self.pwd[0])  # log in

			from_name = 'BlueHub'
			msg = MIMEMultipart()
			msg['Subject'] =subject  #title
			msg['From'] = from_name
			msg['To'] = to_address
			mail_body= body #HTML
			
			msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
			smtpserver.sendmail(from_name, to_address, msg.as_string())
			smtpserver.quit()  # sign out
			
		except:
			print("Something wrong when sending mail!")
			self.crawling_history.insert(tk.INSERT,'發信失敗\n')
			self.crawling_history.insert(tk.INSERT,'\n')

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

		def send_to_test():
			email=e1.get()
			self.send_email('test',email,'This is BlueHub.Copy That?')

			
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
					#self.email_list.append(name+'-'+email)
					print(self.email_dict)
					self.email_var.set('請選擇收件人')
					ttk.Combobox(self.frame1,width=33,value=self.dict_to_list(self.email_dict),textvariable=self.email_var).grid(column=2,columnspan=4,row=2,sticky='W')
					close_new_win()
			
		def close_new_win():
			new_win.destroy()
		
		little_frame=tk.Frame(new_win)
		little_frame.grid(column=2,row=3)
		tk.Button(little_frame,width=10,text='測試',command=lambda :self.thread_it(send_to_test)).grid(column=0,row=1)
		tk.Button(little_frame,width=10, text='確認', command=write_and_close).grid(column=2,row=1)
		tk.Button(little_frame,width=10,text='取消',command=close_new_win).grid(column=1,row=1)
		new_win.mainloop()
		
	
	  

	def add_node(self):
	
		node=[]
		if(self.email_var.get()=='請選擇收件人'):
			tk.messagebox.showwarning(title='Warning', message='尚未選取收件人!')
			return(0)
			
		if(self.course_code_var.get()==''):
			tk.messagebox.showwarning(title='Warning', message='尚未選取收件人!')
			return(0)
			
		else:	
			result=self.search_data(result_list=node)
			if(result==3):
				#record all data
				for item in self.search_list:
					if(item==node):
						tk.messagebox.showwarning(title='Warning', message='列表已存有資料!')
						return(0)
					
				self.search_list.append(node)
				self.search_box.append((node[0][4].split('-')[0],node[0][0]))
				self.search_list_box=ttk.Combobox(self.frame1,width=25,value=self.search_box,state='readonly',textvariable=self.search_var)
				self.search_list_box.grid(column=2,columnspan=2,row=4)
				return(0)
			
			
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
		data_result=[]
		if(self.search_data(data=data_result)==3):
		
			dep=''.join(data_result[0][0].text.split())
			self.r_var1.set(dep)#department
			self.r_var2.set(data_result[0][10].text)#course name
			self.r_var3.set(data_result[0][13].text)#name of professor
			self.r_var4.set(data_result[0][16].text)#course time
			self.r_var5.set(data_result[0][15].text)#balance of course
	
	def search_data(self,data=[],result_list=[]):
		course_code=self.course_code_var.get().upper()
		
		for item in self.search_list:
			if(course_code == item[0]):
				#The course had been searched!
				tk.messagebox.showinfo(title='Prompt', message='課程已搜尋!')
				return(0)#state0
					
		
		course_year="course_y"+self.year_var.get()
		course_url='http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no='+course_code[0:2]
		print(course_url)
		
		try:    
			ua = UserAgent()
			headers = {'User-Agent':ua.random}
			get_information=requests.get(course_url,headers=headers)
			
		except ConnectionError:
			#Connection Error
			tk.messagebox.showerror(title='Error', message='網路連線異常!')
			return(1)#state1

		get_information.encoding='utf-8'
		soup=BeautifulSoup(get_information.text,'html.parser')
		result=soup.find_all("tr",{"class":course_year})

		if(len(result)==0):
			#Wrong course code
			tk.messagebox.showerror(title='Error', message='課程代碼錯誤!')
			return(2)#state2

		else:

			#find the course of the code
			counter=0
			for item in result:
				x=item.find_all("td")
				if(x[2].text==course_code[2:5]):
					data.append(result[counter].find_all("td"))
					mail_and_name=self.email_var.get()
					print(mail_and_name)
					result_list.append([course_code,course_url,counter,course_year,mail_and_name,0])
					
					return(3)#state3 
					
				counter+=1

			if(counter==len(result)):
				#Can't find the course
				tk.messagebox.showwarning(title='Warning', message='查無此課程!')
				return(4)#state4
        
	
	def thread_it(self,func,*args):
		#mutlithreading
		print('Number of threads:',end='')
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
		new_dict={name:email}
		self.email_dict.update(new_dict)
		try:
			with open("user.pickle","wb") as file:
				pickle.dump(self.email_dict,file)
		except:
			print('Something wrong when write file')
			self.crawling_history.insert(tk.INSERT,"寫檔錯誤!\n\n")

			
	def file_read(self):
		try:
			with open("user.pickle","rb") as file:
				self.email_dict=pickle.load(file)
		except:
			print('Something wrong when read file')
			self.crawling_history.insert(tk.INSERT,"讀檔錯誤!\n\n")
			with open("user.pickle","wb") as file:
				pickle.dump({},file)
			self.crawling_history.insert(tk.INSERT,"已建立空收件人名單\n\n")
			
			
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
				
				while(i<upper):
					
					if(self.crawling_enable==False):break
					if(self.delete_enable==True):
						self.delete_node()
						break
					
					node=self.search_list[i][0]
					
					try:
						#random user agent
						ua = UserAgent()
						headers = {'User-Agent':ua.random}		
						get_information=requests.get(node[1],headers=headers)
						
						get_information.encoding='utf-8'
						soup=BeautifulSoup(get_information.text,"lxml")
						result=soup.find_all("tr",{"class":node[3]})
						data=result[node[2]].find_all("td")
					except:
						if(connection_counter>3):
							os._exit(0)
						else:
							print("Connection error!")
							self.crawling_history.insert(tk.INSERT,'網路連線異常\n\n')
							time.sleep(2)
							connection_counter+=1
							break
						
						
						
					if(data[15].text!=u'額滿'):
						
						now_str=self.timer()
						#print(now_str)
						#print(data[0].text)#department of the course
						#print(data[10].text)#name of the course
						#print(data[13].text)#professor of the course
						#print('餘額:'+data[15].text)#balance of the course
						self.crawling_history.insert(tk.INSERT,'時間'+now_str+'\n')
						self.crawling_history.insert(tk.INSERT,node[0]+data[10].text+' 有餘額'+'\n\n')
						self.thread_it(speak,(node[0]+data[13].text+data[10].text+'有餘額'+'\n'))#speak the class
						
						
						number=node[5]
						if(number<2):
							if(number==0):
								#first time send an email
								subject=data[10].text+'('+data[13].text+')'+' 尚有餘額'
								mail_address=node[4].split('-')[1]
								body='course code:'+data[1].text+data[2].text+'<br> at time '+now_str
								self.send_email(subject,mail_address,body)
							
							self.search_list[i][0][5]+=1
							
						#delete the node after three times
						else:
							self.delete_node(index=i)
							upper=len(self.search_list)
							i-=1
					else:
						#recounting
						self.search_list[i][0][5]=0	

					i+=1
					random_sleep()
				
			self.crawler_var.set('開始爬蟲')
			self.crawling_history.insert(tk.INSERT,"時間"+self.timer()+'\n')
			self.crawling_history.insert(tk.INSERT,'結束爬蟲\n\n')
			
	def function(self):
		pass
	
	def add_menu(self,name):
		item=tk.Menu(self.menubar,teatoff=0)
		self.menubar.add_cascade(label=name,menu=item)
		item.add_command(label="收件者",command=self.function)
		

#main code
user_email=[]
user_pwd=[]   

root1=tk.Tk()
log_in_window(root1,user_email,user_pwd)

root2=tk.Tk()
bluehub=main_window(root2,user_email,user_pwd)

root2.mainloop()

print('End of threads:',end='')
print(threading.active_count())