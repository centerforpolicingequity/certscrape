#Libraries
import tkinter as tk
import io
from tkinter import messagebox
from tkinter import filedialog as fd
import sys, os
global path
path = os.getcwd()
import pandas as pd
import pdfquery
import os
from glob import iglob
import base64
import os.path
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygsheets
from requests import HTTPError
pd.options.mode.chained_assignment = None
import datetime as dt
import requests
from itertools import chain

#Set Globals
alerts_missing = []
alerts_expired = []
chart = []
sci_team = []
key_personnel = []
sci_alerts_missing = []
sci_alerts_expired = []

#Splash
messagebox.showinfo(title = 'Starting...', message = 'Pulling CITI Sheet Data')
# configurations
spreadsheet_id = '1XaSGwol8WqkezhNDhruM8P_EA64tTQawHaw1mzeSgcU'
with open('api.key', 'r') as file:
	api_key = file.read().rstrip()
sheet_name = "Certificate Record"

scopes = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('creds.json', scopes = scopes)
gc = gspread.service_account(filename = 'creds.json')
gs = gc.open_by_key(spreadsheet_id)

if gs:
	messagebox.showinfo(title = 'Initializing...', message = 'Certificate Record Found. \nFetching Data...')
	try:
   		gc = gspread.service_account(filename = 'creds.json')
   		gs = gc.open_by_key(spreadsheet_id)
   		messagebox.showinfo(title = 'Success', message = 'Connection Established with Certificate Record. \nStarting CITI Update Center...')
	except Exception as e:
		messagebox.showerror(title = 'Failure', message = f"Error: {e}")
else:
    messagebox.showerror(title = 'Failure', message = "Failed to start CITI Update Center.\n Please check your Internet connection.")

#Child Windows and Functions
def citi_cert_scan():
	"""Scans for CITI Certificates"""
	#Set up lists and directory info
	cert_sheet = gs.get_worksheet(0)
	path = os.getcwd()
	glob_directory = path + '/certificates/*'
	directory = [f for f in iglob(glob_directory, recursive = True) if os.path.isfile(f)]
	global lst, lst2, lst2_a, lst2_b, lst3, lst4, lst5, cols
	lst = []
	lst2 = []
	lst2_a = []
	lst2_b = []
	lst3 = []
	lst4 = []
	lst5 = []
	cols = ['cert_number', 'recipient_name', 'name_last', 'name_first', 'cert_date', 'exp_date', 'group']
	num = 0

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


	#Compile and Append to Google Sheet
	cert_info.insert(num, '*' * 60)
	num = num + 2
	cert_info.insert(num, '\n Compiling Data...')
	num = num + 1
	frame = pd.DataFrame(list(zip(lst, lst2, lst2_b, lst2_a, lst3, lst4, lst5)), columns = cols )
	cert_info.insert(num, '\n Appending to Google Sheet...')
	frame_values = frame.values.tolist()
	cert_sheet.append_rows(frame_values, value_input_option = 'USER_ENTERED')
	messagebox.showinfo(title = 'Success', message =f'{len(frame_values)} rows added to CITI Certifaction Record')

def cert_app():
	global cert_window
	cert_window = tk.Toplevel()
	cert_window.configure(background = 'white')
	cert_window.geometry('700x500')
	def exit_command():
		cert_window.destroy()
	##Info
	cert_window.title('CITI Certificate Scraper')
	cert_app_info = tk.Label(cert_window, text = 'CITI Certificate Scraper \n Center for Policing Equity OHRP \n v.2.0 \n', width = 100, height = 4, bg = 'green', fg = 'white')
	cert_app_scan_head = tk.Label(cert_window, text = 'Scanned Certificates:', width = 100, height = 4, bg = 'black', fg = 'white')
	cert_app_info.pack()
	##Input Frame
	input_frame = tk.Frame(cert_window, relief = 'sunken', width = 100)
	input_frame.pack()
	confirm = tk.Button(input_frame, text = 'Scan', command = citi_cert_scan)
	confirm.pack()
	##Display
	cert_app_scan_head.pack()
	global cert_info
	cert_info = tk.Listbox(cert_window, bg = "black", fg = "green", width = 100)
	cert_info.pack()
	exit_button = tk.Button(cert_window, text = 'Exit', width = 75, command = exit_command)
	exit_button.pack()
	cert_window.mainloop()

def sel():
		"""Runs a scan of CITI Certificates after being selected by radio button"""
		#global selection
		global certs
		#selection = str(initialize.get())
		#Import data
		try:
			cert_sheet = gs.get_worksheet(0)
			certs_data = cert_sheet.get_all_values()
			certs_head = certs_data.pop(0)
			certs = pd.DataFrame(certs_data, columns = certs_head)
			#Fix name issue
			certs['name_first'] = certs['name_first'].str.slice(0,1)+'.'
			certs['recipient_name'] = certs['name_first'].str.upper() + ' ' + certs['name_last'].str.upper()
		except Exception as e:
			messagebox.showerror(title = 'Missing Certificates', message = f'Error: {e}.')
			sys.exit(0)

		#Import Science Team Members
		try:
			sci_sheet = gs.get_worksheet(2)
			science_team = sci_sheet.get_all_values()
			sci_team = list(chain.from_iterable(science_team))
		except Exception as e:
			messagebox.showerror(title = 'Science Team Error', message = f'Error: {e}')
			sys.exit(0)
		#Import Key Personnel
		try:
			key_pers_sheet = gs.get_worksheet(3)
			key_pers = key_pers_sheet.get_all_values()
			key_personnel = list(chain.from_iterable(key_pers))
		except Exception as e:
			messagebox.showerror(title = 'Key Personnel Error', message = f'Error: {e}')
			sys.exit(0)

		### Adjusting Names
		employee_sheet = gs.get_worksheet(4)
		employee_data = employee_sheet.get_all_values()
		name_scrape = list(chain.from_iterable(employee_data))
		for i in name_scrape:
			u = i.upper()
			name_split = u.split() 
			if len(name_split) == 2:
				name_first = name_split[0][:1]+'.'
				name_last = (name_split[1].strip())
				chart.append(name_first + ' ' + name_last) 
			elif len(name_split) == 3:
				name_first = name_split[0][:1]+'.'
				name_last = name_split[2].strip()
				chart.append(name_first + ' ' + name_last)

			### Filter out former employees
		current_employees = set(chart)
		all_recipients = set(certs['recipient_name'])
		missing_employees = all_recipients - current_employees
		if missing_employees:
			with open('former.txt', 'w') as file:
				file.write('GENERAL ALERTS')
				file.write('\n')
				file.write('The following employees may no longer work at CPE as of ' + dt.date.today().strftime("%Y-%m-%d") + '\n')
				file.write('='*60 + '\n')
				for name in missing_employees:
					file.write('%s\n' % name)

		current_certs = certs[certs['recipient_name'].isin(current_employees)]
		final_frame= pd.DataFrame(current_employees, columns = ['recipient_name'])

		### Search
		#### Define Functions
		def has_hsr(name):
			"""Checks if employee currently has HSR Certificate"""
			return name in current_certs[current_certs['group'] == 'HSR for Social & Behavioral Faculty, Graduate Students & Postdoctoral Scholars']['recipient_name'].tolist()

		def has_rcr(name):
			"""Checks if employee currently has RCR Certificate"""
			return name in current_certs[current_certs['group'] == 'Responsible Conduct of Research (RCR)']['recipient_name'].tolist()

		def hsr_expired(val):
			"""Checks if latest HSR certificates on file are expired"""
			now = dt.date.today()
			current_certs['exp_date'] = pd.to_datetime(current_certs['exp_date'], dayfirst = False, format = "%m/%d/%Y")
			latest_hsr = current_certs[current_certs['group']=='HSR for Social & Behavioral Faculty, Graduate Students & Postdoctoral Scholars'].groupby('recipient_name')['exp_date'].max()
			latest_hsr = latest_hsr.reset_index()
			try:
				return val in latest_hsr[latest_hsr['exp_date'].dt.date < now]['recipient_name'].tolist()
			except ValueError:
				return False

		def rcr_expired(val):
			"""Checks if latest RCR certificates on file are expired"""
			now = dt.date.today()
			current_certs['exp_date'] = pd.to_datetime(current_certs['exp_date'], format = "%m/%d/%Y")
			latest_rcr = current_certs[current_certs['group']=='Responsible Conduct of Research (RCR)'].groupby('recipient_name')['exp_date'].max()
			latest_rcr = latest_rcr.reset_index()
			try:
				return val in latest_rcr[latest_rcr['exp_date'].dt.date < now]['recipient_name'].tolist()
			except ValueError:
				return False


		### Check for values
		final_frame['hsr_val'] = final_frame['recipient_name'].apply(has_hsr)
		final_frame['rcr_val'] = final_frame['recipient_name'].apply(has_rcr)
		final_frame['hsr_exp'] = final_frame['recipient_name'].apply(hsr_expired)
		final_frame['rcr_exp'] = final_frame['recipient_name'].apply(rcr_expired)

		#Apply science team label:
		final_frame['sci'] = final_frame['recipient_name'].isin(sci_team)

		#Apply key personnel label:
		final_frame['key_pers'] = final_frame['recipient_name'].isin(key_personnel)

		

		# Results output
		for index, row in final_frame.iterrows():
			num = 0
			## Check if missing certification
			if row['sci'] == True:
				if row['rcr_val'] == False and row['hsr_val'] == True:
					sci_alerts_missing.append(row['recipient_name'] + '| RCR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR documentation. (Science)')
					num = num + 1
				if row['rcr_val'] == False and row['hsr_val'] == False:
					sci_alerts_missing.append(row['recipient_name'] + ' | HSR & RCR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR & HSR documentation. (Science)')
					num = num + 1
				if row['rcr_val'] == True and row['hsr_val'] == False:
					sci_alerts_missing.append(row['recipient_name'] + ' | HSR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR & HSR documentation. (Science)')
					num = num + 1
				else:
					pass
			if row['sci'] == False and row['key_pers'] == True:
				if row['rcr_val'] == False and row['hsr_val'] == True:
					alerts_missing.append(row['recipient_name'] + '| RCR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR documentation. (Key Personnel)')
					num = num + 1
				if row['rcr_val'] == False and row['hsr_val'] == False:
					alerts_missing.append(row['recipient_name'] + ' | HSR & RCR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR & HSR documentation. (Key Personnel)')
					num = num + 1
				if row['rcr_val'] == True and row['hsr_val'] == False:
					alerts_missing.append(row['recipient_name'] + ' | HSR')
					missing_info.insert(num, row['recipient_name'] + ' is missing their RCR & HSR documentation. (Key Personnel)')
					num = num + 1

				else:
					pass
			else:
				pass


		for index, row in final_frame.iterrows():
			exp_num = 0
			if row['sci'] == True:
				## Check if certification has expired
				if row['hsr_exp'] == False and row['rcr_exp'] == True:
					sci_alerts_expired.append(row['recipient_name'] + '| Expired RCR')
					expired_info.insert(exp_num, row['recipient_name'] + ' has an expired RCR certificate. (Science)')
					exp_num = exp_num + 1
				if row['hsr_exp'] == True and row['rcr_exp'] == True:
					sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
					expired_info.insert(exp_num, row['recipient_name'] + ' has expired RCR & HSR certificates. (Science)')
					exp_num = exp_num + 1
				if row['hsr_exp'] == True and row['rcr_exp'] == False:
					expired_info.insert(exp_num, row['recipient_name'] + ' has an expired HSR certificate. (Science)')
					exp_num = exp_num + 1
					sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR')
				else:
					pass
			if row['sci'] == False and row['key_pers'] == True:
				## Check if certification has expired
				if row['hsr_exp'] == False and row['rcr_exp'] == True:
					expired_info.insert(exp_num, row['recipient_name'] + ' has an expired RCR certificate. (Key Personnel)')
					exp_num = exp_num + 1
					alerts_expired.append(row['recipient_name'] + '| Expired RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == True:
					expired_info.insert(exp_num, row['recipient_name'] + ' has expired RCR & HSR certificates. (Key Personnel)')
					exp_num = exp_num + 1
					alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == False:
					expired_info.insert(exp_num, row['recipient_name'] + ' has an expired HSR certificate. (Key Personnel)')
					exp_num = exp_num + 1
					alerts_expired.append(row['recipient_name'] + ' | Expired HSR') 
				else:
					pass
			else:
				pass
		# Write Reports
		try: 
			missing_sheet = gs.worksheet('Missing')
			missing_sheet.clear()
		except:
			gs.add_worksheet('Missing', 3, 3)
			missing_sheet = gs.worksheet('Missing')
			missing_sheet.clear()
		try:
			expired_sheet = gs.worksheet('Expired')
			expired_sheet.clear()
		except:
			gs.add_worksheet('Expired', 3, 3)
			expired_sheet = gs.worksheet('Expired')
			expired_sheet.clear()

		
		if alerts_missing:
				missing_sheet.batch_update([{'range' :'A2', 'values': [alerts_missing], 'majorDimension': 'COLUMNS',}])
		else:
			alerts_missing.append('No Missing Certifications (Key Personnel)')
			missing_sheet.batch_update([{'range' : 'A2', 'values': [alerts_missing], 'majorDimension': 'COLUMNS',}])
			missing_info.insert(0, 'No Missing Certifications (Key Personnel)')

		if alerts_expired:
			expired_sheet.batch_update([{'range': 'A2', 'values': [alerts_expired], 'majorDimension': 'COLUMNS',}])
		else:
			alerts_expired.append('No Expired Certifications (Key Personnel)')
			expired_sheet.batch_update([{'range' : 'A2', 'values': [alerts_expired], 'majorDimension': 'COLUMNS',}])
			expired_info.insert(0, 'No Expired Certifications (Key Personnel)')



		if sci_alerts_missing:
			missing_sheet.batch_update([{'range' :'C2', 'values': [sci_alerts_missing], 'majorDimension': 'COLUMNS',}])
		else:
			sci_alerts_missing.append('No Missing Certifications (Science)')
			missing_sheet.batch_update([{'range' : 'C2', 'values': [sci_alerts_missing], 'majorDimension': 'COLUMNS',}])
			missing_info.insert(0, 'No Missing Certifications (Science)')

		if sci_alerts_expired:
			expired_sheet.batch_update([{'range': 'C2', 'values': [sci_alerts_expired], 'majorDimension': 'COLUMNS',}])
		else:
			sci_alerts_expired.append('No Expired Certifications (Science)')
			expired_sheet.batch_update([{'range' : 'C2', 'values': [sci_alerts_expired], 'majorDimension': 'COLUMNS',}])
			expired_info.insert(0, 'No Missing Certifications (Science)')

		## Label Sheet Columns
		missing_sheet.update_cell(1,1, 'Key Personnel')
		missing_sheet.update_cell(1,3, 'Science')
		expired_sheet.update_cell(1,1, 'Key Personnel')
		expired_sheet.update_cell(1,3, 'Science')

		#Finish	
		messagebox.showinfo(title = 'Success', message = 'Records Updated')

def scan_app():
	#Main window
	global scan_window
	scan_window= tk.Toplevel()
	scan_window.configure(background = "white")
	scan_window.geometry('1000x1000')
	scan_window.title('CITI Employee Search Tool')
	def exit_command():
		scan_window.destroy()
	#Missing Info
	scan_app_info = tk.Label(scan_window, text = 'CITI Employee Search Tool \n Center for Policing Equity OHRP \n v.2.0 \n', width = 100, height = 4, bg = 'green', fg = 'white')
	frm_missing = tk.Frame(scan_window, relief = 'sunken', width = 100)
	missing_head = tk.Label(frm_missing, text = 'MISSING CERTIFICATIONS', width = 100, height = 4, bg = "black", fg = "white")
	global missing_info
	missing_info = tk.Listbox(frm_missing, bg = "navy", fg = 'white', width = 100)
	#Expired Info
	frm_expired = tk.Frame(scan_window, relief = 'sunken', width = 100)
	expired_head = tk.Label(frm_expired, text = 'EXPIRED CERTIFICATIONS', width = 100, height = 4, bg = "white", fg = "red")
	global expired_info
	expired_info = tk.Listbox(frm_expired, bg = "yellow", fg = "black", width = 100)
	#Main Window display
	confirm = tk.Button(scan_window, text = 'Scan', command = sel)
	#Missing Window Display
	missing_head.pack(side = 'top')
	missing_info.pack(side = 'bottom')
	label = tk.Label()
	frm_missing.grid(row=4, column = 1)
	#Expired Window Display
	expired_head.pack(side = 'top')
	expired_info.pack(side = 'bottom')
	frm_expired.grid(row = 5, column = 1)
	#Splash and Exit
	scan_app_info.grid(row = 1, column = 1)
	confirm.grid(row = 3, column = 1)
	exit_button = tk.Button(scan_window, text = 'Exit', width = 75, command = exit_command)
	exit_button.grid(row = 6, column = 1)
	scan_window.mainloop()
		
#Main Menu
menu = tk.Tk()
def option_1():
	cert_app()

def option_2():
	scan_app()
	
def option_3():
	messagebox.showinfo(title = 'Quitting', message = 'Thank you. Goodbye.')
	sys.exit()

menu.title('CITI UPDATE CENTER')
menu_info = tk.Label(menu, text = 'CITI UPDATE CENTER \n Center for Policing Equity OHRP \n v.2.0 \n', width = 75, height = 4, bg = 'green', fg = 'white')
label_menu = tk.Label(menu, text = 'Please select one of the following options:', width = 75, height = 4, bg = "black", fg = "white")
menu.geometry('500x300')
menu.config(background = 'white')
op_1 = tk.Button(menu, text = 'Scan CITI Certificates', width = 25, command = option_1)
op_2 = tk.Button(menu, text = 'Update CITI Statuses', width = 25, command = option_2)
op_3 = tk.Button(menu, text = 'Exit', width = 25, command = option_3)

menu_info.grid(column = 1, row = 1)
label_menu.grid(column = 1, row = 2)
op_1.grid(column = 1, row = 3)
op_2.grid(column = 1, row = 4)
op_3.grid(column = 1, row = 5)


menu.mainloop()