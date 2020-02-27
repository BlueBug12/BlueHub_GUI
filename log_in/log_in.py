import tkinter as tk
import configparser

class log_in_window:
	def __init__(self,master):
		self.master=master
		self.master.title('Welcome to BlueHub')
		self.master.geometry('410x280')

		# welcome image
		self.canvas = tk.Canvas(master, height=200, width=500)
		self.image_file = tk.PhotoImage(file='./image/cover.png')
		self.image = self.canvas.create_image(0,0, anchor='nw', image=self.image_file)
		self.canvas.pack(side='top')

		# user information
		tk.Label(master, text='Gmail Account: ').place(x=50, y= 150)
		tk.Label(master, text='Password: ').place(x=50, y= 190)

		self.var_usr_name = tk.StringVar()
		self.entry_usr_name = tk.Entry(master,width=30, textvariable=self.var_usr_name)
		self.entry_usr_name.place(x=160, y=150)

		self.var_usr_pwd = tk.StringVar()
		self.entry_usr_pwd = tk.Entry(master,width=30 ,textvariable=self.var_usr_pwd, show='*')
		self.entry_usr_pwd.place(x=160, y=190)
		self.btn_enter = tk.Button(master, text='Enter', command=self.close_window)
		self.btn_enter.place(x=170, y=230)

	def read_user_data(self,cfg_path,section):
		config = configparser.ConfigParser()
		config.read(cfg_path)
		self.var_usr_name.set(config.get(section,'username'))
		self.var_usr_pwd.set(config.get(section,'password'))

	def close_window(self):

		self.user=self.var_usr_name.get()
		self.pwd=self.var_usr_pwd.get()
		self.master.destroy()

	def login(self,cfg_path="./config/user.cfg",section="login"):
		self.master.after(500,lambda:self.read_user_data(cfg_path,section))
		self.master.mainloop()

	def get_info(self):
		return self.user,self.pwd