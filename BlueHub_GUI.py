# -*- coding: utf-8 -*-
"""
	@author: BlueBug
"""
import tkinter as tk
from main_window.main_window import main_window
from log_in.log_in import log_in_window

def main():
	root1=tk.Tk()
	lw=log_in_window(root1)
	lw.login()
	user,pwd=lw.get_info()

	root2=tk.Tk()
	main_window(root2,user,pwd)
	root2.mainloop()

if __name__ == '__main__':
	main()
