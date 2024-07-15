import tkinter as tk
from tkinter import messagebox
import sys, os
global path
path = os.getcwd()
import cert
import scan_citi_files
import email_updates


menu = tk.Tk()

def option_1():
	cert.cert_app()

def option_2():
	scan_citi_files.scan_app()

def option_3():
	messagebox.showinfo('Running Checks...')
	email_updates.email_update()

def option_4():
	messagebox.showinfo(title = 'Quitting', message = 'Thank you. Goodbye.')
	exit()

menu.title('CITI UPDATE CENTER')
menu_info = tk.Label(menu, text = 'CITI UPDATE CENTER \n Center for Policing Equity OHRP \n v.1.2 \n', width = 75, height = 4, bg = 'green', fg = 'white')
label_menu = tk.Label(menu, text = 'Please select one of the following options:', width = 75, height = 4, bg = "black", fg = "white")
menu.geometry('500x250')
menu.config(background = 'white')
op_1 = tk.Button(menu, text = 'Scan CITI Certificates', width = 25, command = option_1)
op_2 = tk.Button(menu, text = 'Update CITI Statuses', width = 25, command = option_2)
op_3 = tk.Button(menu, text = 'Email Updates', width = 25, command = option_3)
op_4 = tk.Button(menu, text = 'Exit', width = 25, command = option_4)

menu_info.grid(column = 1, row = 1)
label_menu.grid(column = 1, row = 2)
op_1.grid(column = 1, row = 3)
op_2.grid(column = 1, row = 4)
op_3.grid(column = 1, row = 5)
op_4.grid(column = 1, row = 6)

menu.mainloop()