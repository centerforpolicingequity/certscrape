import tkinter as tk
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
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
pd.options.mode.chained_assignment = None
import datetime as dt

#Set Globals
alerts_missing = []
alerts_expired = []
chart = []
sci_team = []
key_personnel = []
sci_alerts_missing = []
sci_alerts_expired = []


#Child Windows and Functions
def citi_cert_scan():

	"""Scans for CITI Certificates"""
	#Set up lists and directory info
	path = os.getcwd()
	glob_directory = path + '/**/*'
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
	global new_file
	new_file = new_input.get()
	header_select = []
	if new_file == 'Yes':
		header_select = True
	elif new_file == 'No':
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

def cert_app():
	global cert_window
	cert_window = tk.Toplevel()
	cert_window.configure(background = 'white')
	cert_window.geometry('700x500')
	def exit_command():
		cert_window.destroy()
	##Info
	cert_window.title('CITI Certificate Scraper')
	cert_app_info = tk.Label(cert_window, text = 'CITI Certificate Scraper \n Center for Policing Equity OHRP \n v.1.7 \n', width = 100, height = 4, bg = 'green', fg = 'white')
	cert_app_scan_head = tk.Label(cert_window, text = 'Scanned Certificates:', width = 100, height = 4, bg = 'black', fg = 'white')
	cert_app_info.pack()
	##Input Frame
	new_sheet_label = tk.Label(cert_window, text = 'Is this for a new CITI sheet?', width = 100, height = 4, bg = "white", fg = "black")
	new_sheet_label.pack()
	input_frame = tk.Frame(cert_window, relief = 'sunken', width = 100)
	input_frame.pack()
	global new_input
	new_input = tk.StringVar(input_frame, value = 'None')
	new_input_yes = tk.Radiobutton(input_frame, text = "Yes", fg = "black", variable = new_input, value = 'Yes')
	new_input_no = tk.Radiobutton(input_frame, text = "No", fg = "black", variable = new_input, value = 'No')
	confirm = tk.Button(input_frame, text = 'OK', command = citi_cert_scan)
	new_input_yes.pack()
	new_input_no.pack()
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
		global selection
		global certs
		selection = str(initialize.get())
		#Import data
		try:
			certs = pd.read_csv('citi.csv', encoding = 'utf-8')
			#Fix name issue
			certs['name_first'] = certs['name_first'].str.slice(0,1)+'.'
			certs['recipient_name'] = certs['name_first'].str.upper() + ' ' + certs['name_last'].str.upper()
		except FileNotFoundError:
			messagebox.showerror(title = 'Missing Certificates', message = 'Error: Cannot Find CITI certificates file (citi.csv), please check directory.')
			sys.exit(0)

		#Import Science Team Members
		try:
			with open('science_team.list', 'r') as sci:
				for line in sci:
					sci_team.append(line.strip('\n'))
		except FileNotFoundError:
			messagebox.showerror(title = 'Missing Science', message = 'Error: Science Team list not found, please check directory.')
			sys.exit(0)

		#Import Key Personnel
		try:
			with open('key_personnel.list', 'r') as list:
				for line in list:
					key_personnel.append(line.strip('\n'))
		except FileNotFoundError:
			messagebox.showerror(title = 'Missing KP', message = 'Error: Key Personnel list not found, please check directory.')
			sys.exit(0)
		## No, then run a scan of all the data:
		if selection == 'N':
			### Adjusting Names
			name_scrape = pd.read_csv('general_bamboohr_org_chart.csv')['Name'].str.upper().tolist()
			for i in name_scrape:
				name_split = i.split() 
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
				current_certs['exp_date'] = pd.to_datetime(current_certs['exp_date'], dayfirst = True, format = "%d-%b-%y")
				latest_hsr = current_certs[current_certs['group']=='HSR for Social & Behavioral Faculty, Graduate Students & Postdoctoral Scholars'].groupby('recipient_name')['exp_date'].max()
				latest_hsr = latest_hsr.reset_index()
				try:
					return val in latest_hsr[latest_hsr['exp_date'].dt.date < now]['recipient_name'].tolist()
				except ValueError:
					return False

			def rcr_expired(val):
				"""Checks if latest RCR certificates on file are expired"""
				now = dt.date.today()
				current_certs['exp_date'] = pd.to_datetime(current_certs['exp_date'], format = "%d-%b-%y")
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

			framename= 'citi_records.csv'
			final_frame.to_csv(framename, header = True, index = False)
		## Yes: Then read the up-to-date records
		else:
			final_frame = pd.read_csv('citi_records.csv', header = 0, names = ('recipient_name', 'hsr_val', 'rcr_val', 'hsr_exp', 'rcr_exp', 'sci', 'key_pers'))

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
		# Write Report
		if alerts_missing or alerts_expired:
			with open('alerts.txt', 'w') as file:
				file.write('KEY PERSONNEL ALERTS')
				file.write('\n')
				file.write('='*10)
				file.write('MISSING CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
				file.write('='*10 + '\n')
				if alerts_missing:
					for alert in alerts_missing:
						file.write('%s\n' % alert)
				else:
					file.write('No Missing Certifications \n')
				file.write('='*10)
				file.write('EXPIRED CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
				file.write('='*10 + '\n')
				if alerts_expired:
					for alert in alerts_expired:
						file.write('%s\n' % alert)
				else:
					file.write('No Expired Certifications \n')
		if sci_alerts_missing or sci_alerts_expired:
			with open('sci_alerts.txt', 'w') as file:
				file.write('SCIENCE TEAM ALERTS')
				file.write('\n')
				file.write('='*10)
				file.write('MISSING CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
				file.write('='*10 + '\n')
				if sci_alerts_missing:
					for alert in sci_alerts_missing:
						file.write('%s\n' % alert)
				else:
					file.write('No Missing Certifications \n')
				file.write('='*10)
				file.write('EXPIRED CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
				file.write('='*10 + '\n')
				if sci_alerts_expired:
					for alert in sci_alerts_expired:
						file.write('%s\n' % alert)
				else:
					file.write('No Expired Certifications \n')

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
	scan_app_info = tk.Label(scan_window, text = 'CITI Employee Search Tool \n Center for Policing Equity OHRP \n v.1.7 \n', width = 100, height = 4, bg = 'green', fg = 'white')
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
	global initialize
	initialize = tk.StringVar(scan_window, value = 'None')
	label_app = tk.Label(scan_window, text = 'Is there already an up-to-date copy of citi_records.csv?', width = 100, height = 4, bg = "white", fg = "black")
	label_app.grid(column = 1, row = 2)
	first_time_yes = tk.Radiobutton(frm_missing, text = "Yes", fg = "black", variable = initialize, value = 'Y')
	first_time_no = tk.Radiobutton(frm_missing, text = "No", fg = "black", variable = initialize, value = 'N')
	confirm = tk.Button(scan_window, text = 'OK', command = sel)
	first_time_yes.pack()
	first_time_no.pack()
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

def email_update():
    now = dt.date.today() # Current date/time
    message_header = 'For the Office of Human Research Protection:' + '\n' + '*'*60 + '\n'
    message_footer = '*'*60 + '\n' + 'Sent from CITI Email Updater' + '\n' + '*'*60
    #Check if alerts are active:
    path = os.getcwd() + '/**/*'

    if os.path.isfile('sci_alerts.txt'):
        messagebox.showinfo('Check 1/3', 'Science Alerts Detected')
    else:
        with open('sci_alerts.txt', 'w') as file:
            file.write('No Science Team Alerts')
            file.close()
    sci_alerts = open('sci_alerts.txt', 'r')

    if os.path.isfile('former.txt'):
        messagebox.showinfo('Check 2/3', 'Employee Changes Detected')
    else:
        with open('former.txt', 'w') as file:
            file.write("No Other Employee Updates")
            file.close()
    former_alerts = open('former.txt', 'r')

    if os.path.isfile('alerts.txt'):
        messagebox.showinfo('Check 3/3','Key Personnel Alerts Detected')
    else:
        with open('alerts.txt', 'w') as file:
            file.write('No Key Personnel Alerts')
            file.close()
    key_alerts = open('alerts.txt', 'r')

    SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(message_header + sci_alerts.read() + '\n' + key_alerts.read() + '\n' + former_alerts.read() + '\n' + message_footer)
    message['to'] = 'CPEIRB@policingequity.org'
    message['subject'] = 'CITI UPDATE:' + ' ' + now.strftime("%m - %d - %Y")
    create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        messagebox.showinfo('Success', 'Successfully sent message.')
    except Exception:
        messagebox.showerror('Error','An error occurred. Check logs.')
        message = None

def add_key_pers():
	x_team = []
	key_list = []
	add_list = []

	global input_file
	input_file = file_input.get()
	global keypers_file
	keypers_file = file_keypers.get()

	try:
		with open(input_file, 'r') as team:
			for line in team:
				x_team.append(line.strip('\n'))
			team.close()
	except FileNotFoundError:
		messagebox.showerror('Input File Missing', 'Please select a file of personnel to be added.')

	try:
		with open(keypers_file, 'r') as key_file:
			for line in key_file:
				key_list.append(line.strip('\n'))
			key_file.close()
	except FileNotFoundError:
		messagebox.showerror('Key Personnel File Missing', 'Please select a file for existing key personnel.')

	if x_team:
			for name in x_team:
				if key_list:
					if name not in key_list:
						key_pers_display.insert('end', '֎  ' + name + ': Added \n')
						add_list.append(name)
					else:
						key_pers_display.insert('end', '⁐  ' + name + ': Present \n')
	else:
		key_pers_display.insert('end', 'Information missing. \n')

	if add_list:
		with open(keypers_file, 'a') as output:
				for name in add_list:
					output.write('\n' + name + '\n')

def add_app():
	global add_window
	global file_input
	file_input = tk.StringVar()
	global file_keypers
	file_keypers = tk.StringVar()
	add_window= tk.Toplevel()
	add_window.configure(background = "white")
	add_window.geometry('800x500')
	add_window.title('Key Personnel Tool')

	def select_file_input():
		input_path = fd.askopenfilename(title = "Personnel to be Added", filetypes =[("List files", "*.list"), ("All files", "*")])
		if input_path:
			with open(input_path, 'r') as file:
				content = file.read()
				input_display.insert('end', content)
				file.close()
		file_input.set(input_path)

	def select_file_keypers():
		keypers_path = fd.askopenfilename(title = "Key Personnel File", filetypes =[("List files", "*.list"), ("All files", "*")])
		if keypers_path:
			with open(keypers_path, 'r') as file:
				content = file.read()
				list_display.insert('end', content)
				file.close()
		file_keypers.set(keypers_path)
	def exit_command():
		add_window.destroy()	

	file_select_input = tk.Button(add_window, text = 'Addition List', width = 25, command = select_file_input)
	file_select_input.grid(row = 1, column = 1)
	file_select_keypers = tk.Button(add_window, text = 'Key Personnel File', width = 25, command = select_file_keypers)
	file_select_keypers.grid(row = 1, column = 3)
	
	add_button = tk.Button(add_window, text = 'Add', bg = 'green', width = 25, command = add_key_pers)
	add_button.grid(row = 2, column = 2)
	
	exit_button = tk.Button(add_window, text = 'Exit', width = 25, command = exit_command)
	exit_button.grid(row = 3, column = 2)
	
	global input_display
	input_display = tk.Text(add_window, height = 10, width = 25, bg = 'purple', fg = 'white')
	input_display.grid(row = 2, column = 1)
	
	global list_display
	list_display = tk.Text(add_window, height = 10, width = 25, bg = 'yellow', fg = 'black')
	list_display.grid(row = 2, column = 3) 
	
	global key_pers_display
	key_pers_display = tk.Text(add_window, height = 10, width = 50, bg = 'black', fg = 'white')
	key_pers_display.grid(row = 4, column = 2)

	add_window.mainloop()
			

#Main Menu
menu = tk.Tk()
def option_1():
	cert_app()

def option_2():
	scan_app()

def option_3():
	messagebox.showinfo('Checks', 'Running Checks...')
	email_update()

def option_4():
	#Clean lingering files
	#If alerts are already cleared
	if os.path.isfile('former.txt') == False and os.path.isfile('alerts.txt') == False and os.path.isfile('sci_alerts.txt') == False:
		messagebox.showerror('No Alerts', 'Alerts already cleared.')
	if os.path.isfile('former.txt'):
		messagebox.showinfo('Former Cleared', 'Cleared Former Employee List')
		os.remove('former.txt')
	if os.path.isfile('alerts.txt'):
		messagebox.showinfo('KP Cleared', 'Cleared Key Personnel Alerts')
		os.remove('alerts.txt')
	if os.path.isfile('sci_alerts.txt'):
		messagebox.showinfo('Science Cleared', 'Cleared Science Alerts')
		os.remove('sci_alerts.txt')

def option_5():
	add_app()
	
def option_6():
	messagebox.showinfo(title = 'Quitting', message = 'Thank you. Goodbye.')
	sys.exit()

menu.title('CITI UPDATE CENTER')
menu_info = tk.Label(menu, text = 'CITI UPDATE CENTER \n Center for Policing Equity OHRP \n v.1.3 \n', width = 75, height = 4, bg = 'green', fg = 'white')
label_menu = tk.Label(menu, text = 'Please select one of the following options:', width = 75, height = 4, bg = "black", fg = "white")
menu.geometry('500x300')
menu.config(background = 'white')
op_1 = tk.Button(menu, text = 'Scan CITI Certificates', width = 25, command = option_1)
op_2 = tk.Button(menu, text = 'Update CITI Statuses', width = 25, command = option_2)
op_3 = tk.Button(menu, text = 'Email Updates', width = 25, command = option_3)
op_4 = tk.Button(menu, text = 'Clear Old Alerts', width = 25, bg = 'red', command = option_4)
op_5 = tk.Button(menu, text = 'Add Key Personnel', width = 25, command = option_5)
op_6 = tk.Button(menu, text = 'Exit', width = 25, command = option_6)

menu_info.grid(column = 1, row = 1)
label_menu.grid(column = 1, row = 2)
op_1.grid(column = 1, row = 3)
op_2.grid(column = 1, row = 4)
op_3.grid(column = 1, row = 5)
op_4.grid(column = 1, row = 6)
op_5.grid(column = 1, row = 7)
op_6.grid(column = 1, row = 8)

menu.mainloop()