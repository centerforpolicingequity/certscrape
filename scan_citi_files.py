#CITI Employee Search
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity
#Last Updated: July 2024

#Import Packages
import tkinter as tk
from tkinter import messagebox
import sys
import pandas as pd
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

def sel():
		"""Runs a scan of CITI Certificates after being selected by radio button"""
		global selection
		selection = str(initialize.get())
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
			if row['sci'] == True:
				## Check if certification has expired
				if row['hsr_exp'] == False and row['rcr_exp'] == True:
					sci_alerts_expired.append(row['recipient_name'] + '| Expired RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == True:
					sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == False:
					sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR')
				else:
					pass
			if row['sci'] == False and row['key_pers'] == True:
				## Check if certification has expired
				if row['hsr_exp'] == False and row['rcr_exp'] == True:
					alerts_expired.append(row['recipient_name'] + '| Expired RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == True:
					alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
				if row['hsr_exp'] == True and row['rcr_exp'] == False:
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

#Window Geometry
def exit_command():
	scan_window.destroy()

def app():
	global scan_window
	scan_window= tk.Tk()
	scan_window.configure(background = "white")
	scan_window.geometry('700x500')
	scan_window.title('CITI Employee Search Tool')
	scan_app_info = tk.Label(scan_window, text = 'CITI Employee Search Tool \n Center for Policing Equity OHRP \n v.1.7 \n', width = 100, height = 4, bg = 'green', fg = 'white')
	frm_missing = tk.Frame(scan_window, relief = 'sunken', width = 100)
	missing_head = tk.Label(frm_missing, text = 'MISSING CERTIFICATIONS', width = 100, height = 4, bg = "black", fg = "white")
	global missing_info
	missing_info = tk.Listbox(frm_missing, bg = "black", fg = 'green', width = 100)
	global initialize
	initialize = tk.StringVar()
	label_app = tk.Label(scan_window, text = 'Is there already an up-to-date copy of citi_records.csv?', width = 100, height = 4, bg = "black", fg = "white")
	label_app.grid(column = 1, row = 2)
	first_time_yes = tk.Radiobutton(frm_missing, text = "Yes", fg = "black", variable = initialize, value = 'Y', command = sel)
	first_time_no = tk.Radiobutton(frm_missing, text = "No", fg = "black", variable = initialize, value = 'N', command = sel)
	first_time_yes.pack()
	first_time_no.pack()
	missing_head.pack(side = 'top')
	missing_info.pack(side = 'bottom')
	label = tk.Label()
	frm_missing.grid(row=3, column = 1)
	scan_app_info.grid(row = 1, column = 1)
	exit_button = tk.Button(scan_window, text = 'Exit', width = 75, command = exit_command)
	exit_button.grid(row = 4, column = 1)
	scan_window.mainloop()

#Run
if __name__ == '__main__':
	app()