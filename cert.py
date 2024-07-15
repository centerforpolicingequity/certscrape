#CITI Certificate Scraper
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity

#Import packages
import pandas as pd
import pdfquery
import os
from glob import iglob
import tkinter as tk
from tkinter import messagebox
global new_file

def citi_cert_scan():
	"""Scans for CITI Certificates"""
	#Set up lists and directory info
	path = os.getcwd()
	glob_directory = path + '/**/*'
	directory = [f for f in iglob(glob_directory, recursive = True) if os.path.isfile(f)]
	lst = []
	lst2 = []
	lst2_a = []
	lst2_b = []
	lst3 = []
	lst4 = []
	lst5 = []
	cols = ['cert_number', 'recipient_name', 'name_last', 'name_first', 'cert_date', 'exp_date', 'group']
	num = 0
	new_file = str(new_input.get())
	if new_file == 'Y':
		header_select = True
	else:
		header_select = False

#Loop over all CITI Certificates in Directory
	for file in directory:
		if file.endswith(".pdf"):
			with open(file, 'rb') as doc:
				certificate = pdfquery.PDFQuery(doc)
				certificate.load()
				certificate
				#Doc reads as an XML file
				#Searching for Record ID
				try:
					keyword = certificate.pq('LTTextLineHorizontal:contains("{}")'.format("Record ID"))[0]
					x0 = float(keyword.get('x0', 0)) 
					y0 = float(keyword.get('y0', 0)) 
					x1 = float(keyword.get('x1',0)) + 30
					y1 = float(keyword.get('y1', 0))
					#When Record ID is found
					cert_num = certificate.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()
					cert_num = cert_num.replace('Record ID', '').strip()
					cert_info.insert(num, 'Record ID: ' + cert_num)
					num = num + 1
					lst.append(cert_num)
				except IndexError:
					cert_info.insert(num, 'No Record ID Found')
					num = num + 1
					cert_num = file
					lst.append(cert_num)

				#Searching for Recipient
				try:
					recipient = certificate.pq('LTTextLineHorizontal:contains("{}")'.format("This is to certify that:"))[0]
					r_x0 = float(recipient.get('x0', 0)) 
					r_y0 = float(recipient.get('y0', 0)) - 40
					r_x1 = float(recipient.get('x1',0))
					r_y1 = float(recipient.get('y1', 0))
					#When Recipient is found
					recipient_name = certificate.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (r_x0, r_y0, r_x1, r_y1)).text()
					recipient_name = recipient_name.replace('This is to certify that:', '').strip()
					cert_info.insert(num, 'Name: ' + recipient_name)
					num = num + 1
					name_split = recipient_name.split()
					if len(name_split) == 2:
						name_first = name_split[0].strip()
						name_last = name_split[1].strip()
					elif len(name_split) == 3:
						name_first = name_split[0].strip() + ' ' + name_split[1].strip()
						name_last = name_split[2].strip()
					lst2.append(recipient_name)
					lst2_a.append(name_first)
					lst2_b.append(name_last)
				except IndexError:
					cert_info.insert(num, 'No Recipient Found')
					num = num + 1
					recipient_name = 'NA'
					name_last = 'NA'
					name_first = 'NA'
					lst2.append(recipient_name)
					lst2_b.append(name_last)
					lst2_a.append(name_first)

				#Searching for Certificate Date
				try:
					cert_date = certificate.pq('LTTextLineHorizontal:contains("{}")'.format("Completion Date"))[0]
					c_x0 = float(cert_date.get('x0', 0))
					c_y0 = float(cert_date.get('y0', 0))
					c_x1 = float(cert_date.get('x1',0)) + 10
					c_y1 = float(cert_date.get('y1', 0))
					#When Date is Found
					cert_date = certificate.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (c_x0, c_y0, c_x1, c_y1)).text()
					cert_date = cert_date.replace('Completion Date ', '').strip()
					cert_info.insert(num, 'Completion Date: ' + cert_date)
					num = num + 1
					lst3.append(cert_date)
				except IndexError:
					cert_info.insert(num, 'No Completion Date Found')
					num = num + 1
					cert_date = 'NA'
					lst3.append(cert_date)

				#Searching for Expiration
				try:
					exp_date = certificate.pq('LTTextLineHorizontal:contains("{}")'.format("Expiration Date"))[0]
					e_x0 = float(exp_date.get('x0', 0))
					e_y0 = float(exp_date.get('y0', 0))
					e_x1 = float(exp_date.get('x1',0)) + 10
					e_y1 = float(exp_date.get('y1', 0))
					#When Expiration is Found
					exp_date = certificate.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (e_x0, e_y0, e_x1, e_y1)).text()
					exp_date = exp_date.replace('Expiration Date ', '').strip()
					cert_info.insert(num, 'Expiration Date: ' + exp_date)
					num = num + 1
					lst4.append(exp_date)
				except IndexError:
					cert_info.insert(num, 'No Expiration Date Found')
					num = num + 1
					exp_date = 'NA'
					lst4.append(exp_date)

				#Searching for Curriculum Group
				try:
					group = certificate.pq('LTTextLineHorizontal:contains("{}")'.format("Curriculum Group"))[0]
					g_x0 = float(group.get('x0', 0)) 
					g_y0 = float(group.get('y0', 0)) + 10
					g_x1 = float(group.get('x1',0))
					g_y1 = float(group.get('y1', 0)) + 10
					#When Expiration is Found
					group = certificate.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (g_x0, g_y0, g_x1, g_y1)).text()
					cert_info.insert(num, 'Course: ' + group)
					num = num + 1
					lst5.append(group)
				except IndexError:
					cert_info.insert(num, 'No Course Found')
					num = num + 1
					group = 'NA'
					lst5.append(group)



	#Compile to pandas DataFrame and Export
	cert_info.insert(num, '*' * 60)
	num = num + 2
	cert_info.insert(num, '\n Compiling Data...')
	num = num + 1
	frame = pd.DataFrame(list(zip(lst, lst2, lst2_b, lst2_a, lst3, lst4, lst5)), columns = cols )
	cert_info.insert(num, '\n Saving to File...')
	framename = "citi.csv"
	frame.to_csv(framename, mode = 'a', header = header_select, index = False)
	messagebox.showinfo(title = 'Successfully Saved', message ='Records saved under ' + framename)

#Window Geometry
def exit_command():
	cert_window.destroy()

def cert_app():
	global cert_window
	cert_window = tk.Tk()
	cert_window.configure(background = 'white')
	cert_window.geometry('700x500')
	##Info
	cert_window.title('CITI Certificate Scraper')
	cert_app_info = tk.Label(cert_window, text = 'CITI Certificate Scraper \n Center for Policing Equity OHRP \n v.1.7 \n', width = 100, height = 4, bg = 'green', fg = 'white')
	cert_app_scan_head = tk.Label(cert_window, text = 'Scanned Certificates:', width = 100, height = 4, bg = 'black', fg = 'white')
	cert_app_info.grid(row = 1, column = 1)
	cert_app_scan_head.grid(row = 3, column = 1)
	##Input Frame
	input_frame = tk.Frame(cert_window, relief = 'sunken', width = 100)
	input_frame.grid(row = 2, column = 1)
	global new_input
	new_input = tk.StringVar()
	new_input_yes = tk.Radiobutton(input_frame, text = "Yes", fg = "black", variable = new_input, value = 'Y')
	new_input_no = tk.Radiobutton(input_frame, text = "No", fg = "black", variable = new_input, value = 'N')
	confirm = tk.Button(input_frame, text = 'OK', command = citi_cert_scan)
	new_input_yes.pack()
	new_input_no.pack()
	confirm.pack(side = 'bottom')
	##Display
	global cert_info
	cert_info = tk.Listbox(cert_window, bg = "black", fg = "green", width = 100)
	cert_info.grid(row = 4, column = 1)
	exit_button = tk.Button(cert_window, text = 'Exit', width = 75, command = exit_command)
	exit_button.grid(row = 5, column = 1)
	cert_window.mainloop()


if __name__ == '__main__':
	cert_app()