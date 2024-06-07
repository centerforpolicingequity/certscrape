#CITI Employee Search
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity
#Last Updated: June 7 2024

def update_citi_statuses():
	"""Updates CITI Statuses"""
	print('~'* 60)
	print('CITI Employee Search Tool')
	print('Center for Policing Equity OHRP')
	print('v.1.6')
	print('2024', '\n')
	print('~'*60)

	import sys
	import pandas as pd
	pd.options.mode.chained_assignment = None
	import datetime as dt
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
		print('Error: Cannot Find CITI certificates file (citi.csv), please check directory.')
		sys.exit(1)

	#Import Science Team Members
	with open('science_team.list', 'r') as sci:
		try:
			for line in sci:
				sci_team.append(line.strip('\n'))
		except FileNotFoundError:
			print('Science Team list not found, please check directory.')
			sys.exit(2)

	#Import Key Personnel
	with open('key_personnel.list', 'r') as list:
		try:
			for line in list:
				key_personnel.append(line.strip('\n'))
		except FileNotFoundError:
			print('Key Personnel list not found, please check directory.')
			sys.exit(2)


	#First time?
	initialize = input('Is there already an up-to-date copy of \' citi_records.csv \'? (Y/N): ')
	## No, then run a scan of all the data:
	if initialize == 'N':
		print('Reading Data...')
		print('~'*60, '\n')
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
		for name in missing_employees:
			print('The following employee may no longer work at CPE:', name)
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
				print('No Expired HSR')
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
				print('No Expired RCR')
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
		print('Employee CITI Statuses saved to ', framename)
		print('~'*60, '\n')
	## Yes: Then read the up-to-date records
	else:
		print('Reading Employee CITI Statuses...')
		final_frame = pd.read_csv('citi_records.csv', header = 0, names = ('recipient_name', 'hsr_val', 'rcr_val', 'hsr_exp', 'rcr_exp', 'sci', 'key_pers'))

	# Results output
	print('~' * 60)
	print('MISSING CERTIFICATIONS')
	print('Note: ** indicates that employee is in Science & Technology')
	print('*' * 60)
	for index, row in final_frame.iterrows():
		## Check if missing certification
		if row['sci'] == True:
			if row['rcr_val'] == False and row['hsr_val'] == True:
				print(row['recipient_name'], 'is missing their RCR documentation.**')
				print('-' * 60)
				sci_alerts_missing.append(row['recipient_name'] + '| RCR')
			if row['rcr_val'] == False and row['hsr_val'] == False:
				print(row['recipient_name'], 'is missing their RCR & HSR documentation.**')
				print('-' * 60)
				sci_alerts_missing.append(row['recipient_name'] + ' | HSR & RCR')
			if row['rcr_val'] == True and row['hsr_val'] == False:
				print(row['recipient_name'], 'is missing their HSR documentation.**')
				print('-' * 60)
				sci_alerts_missing.append(row['recipient_name'] + ' | HSR')
			else:
				pass
		if row['sci'] == False and row['key_pers'] == True:
			if row['rcr_val'] == False and row['hsr_val'] == True:
				print(row['recipient_name'], 'is listed as key personnel and is missing their RCR documentation.')
				print('-' * 60)
				alerts_missing.append(row['recipient_name'] + '| RCR')
			if row['rcr_val'] == False and row['hsr_val'] == False:
				print(row['recipient_name'], 'is listed as key personnel and is missing their RCR & HSR documentation.')
				print('-' * 60)
				alerts_missing.append(row['recipient_name'] + ' | HSR & RCR')
			if row['rcr_val'] == True and row['hsr_val'] == False:
				print(row['recipient_name'], 'is listed as key personnel and is missing their HSR documentation.')
				print('-' * 60)
				alerts_missing.append(row['recipient_name'] + ' | HSR')
			else:
				pass
		else:
			pass

	print('\n')
	print('EXPIRED CERTIFICATIONS')
	print('Note: ** indicates that employee is in Science & Technology')
	print('*'*60) 

	for index, row in final_frame.iterrows():
		if row['sci'] == True:
			## Check if certification has expired
			if row['hsr_exp'] == False and row['rcr_exp'] == True:
				print(row['recipient_name'], 'has an expired RCR certificate.**')
				print('-' * 60)
				sci_alerts_expired.append(row['recipient_name'] + '| Expired RCR')
			if row['hsr_exp'] == True and row['rcr_exp'] == True:
				print(row['recipient_name'], 'has expired RCR & HSR certificates.**')
				print('-' * 60)
				sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
			if row['hsr_exp'] == True and row['rcr_exp'] == False:
				print(row['recipient_name'], 'has an expired HSR certificate.**')
				print('-' * 60)
				sci_alerts_expired.append(row['recipient_name'] + ' | Expired HSR')
			else:
				pass
		if row['sci'] == False and row['key_pers'] == True:
			## Check if certification has expired
			if row['hsr_exp'] == False and row['rcr_exp'] == True:
				print(row['recipient_name'], 'has an expired RCR certificate.')
				print('-' * 60)
				alerts_expired.append(row['recipient_name'] + '| Expired RCR')
			if row['hsr_exp'] == True and row['rcr_exp'] == True:
				print(row['recipient_name'], 'has expired RCR & HSR certificates.')
				print('-' * 60)
				alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
			if row['hsr_exp'] == True and row['rcr_exp'] == False:
				print(row['recipient_name'], 'has an expired HSR certificate.')
				print('-' * 60)
				alerts_expired.append(row['recipient_name'] + ' | Expired HSR') 
			else:
				pass
		else:
			pass
	print('~'*60, '\n')
	# Write Report
	if alerts_missing or alerts_expired:
		with open('alerts.txt', 'w') as file:
			file.write('KEY PERSONNEL ALERTS')
			file.write('\n')
			file.write('='*60)
			file.write('MISSING CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
			file.write('='*60 + '\n')
			for alert in alerts_missing:
				file.write('%s\n' % alert)
			file.write('='*60)
			file.write('EXPIRED CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
			file.write('='*60 + '\n')
			for alert in alerts_expired:
				file.write('%s\n' % alert)
		print('Key Personnel Alerts Saved as alerts.txt')
	else:
		print('No Key Personnel Alerts')
	if sci_alerts_missing or sci_alerts_expired:
		with open('sci_alerts.txt', 'w') as file:
			file.write('SCIENCE TEAM ALERTS')
			file.write('\n')
			file.write('='*60)
			file.write('MISSING CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
			file.write('='*60 + '\n')
			for alert in sci_alerts_missing:
				file.write('%s\n' % alert)
			file.write('='*60)
			file.write('EXPIRED CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
			file.write('='*60 + '\n')
			for alert in sci_alerts_expired:
				file.write('%s\n' % alert)
		print('Science Team Alerts Saved as sci_alerts.txt')
	else:
		print('No Science Team Alerts')

if __name__ == '__main':
	print('Running CITI Status Update standalone...')
	update_citi_statuses()
else:
	print('CITI Status Update Imported...')