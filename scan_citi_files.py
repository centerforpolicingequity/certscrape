#CITI Employee Search
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity
#Last Updated: April 12 2024

print('~'* 60)
print('CITI Employee Search Tool')
print('Center for Policing Equity OHRP')
print('v.1.2')
print('2024', '\n')
print('~'*60)

import pandas as pd
pd.options.mode.chained_assignment = None
import datetime as dt
alerts_missing = []
alerts_expired = []
chart = []
#Import data
print('Reading Data...')
print('~'*60, '\n')
certs = pd.read_csv('citi.csv', encoding = 'utf-8')
#Fix name issue
certs['name_first'] = certs['name_first'].str.slice(0,1)+'.'
certs['recipient_name'] = certs['name_first'].str.upper() + ' ' + certs['name_last'].str.upper()

# Adjusting Names
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

#Filter out former employees
current_employees = set(chart)
all_recipients = set(certs['recipient_name'])
missing_employees = all_recipients - current_employees

print('The following employees may no longer work at CPE:')
for name in missing_employees:
	print(name)
if missing_employees:
	with open('former.txt', 'w') as file:
		file.write('The following employees may no longer work at CPE as of ' + dt.date.today().strftime("%Y-%m-%d") + '\n')
		file.write('='*30 + '\n')
		for name in missing_employees:
			file.write('%s\n' % name)

current_certs = certs[certs['recipient_name'].isin(current_employees)]
current_employees = list(current_employees)
final_frame= pd.DataFrame(current_employees, columns = ['recipient_name'])

#Search
##Define Functions
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
	return val in latest_hsr[latest_hsr['exp_date'].dt.date < now]['recipient_name'].tolist()

def rcr_expired(val):
	"""Checks if latest RCR certificates on file are expired"""
	now = dt.date.today()
	current_certs['exp_date'] = pd.to_datetime(current_certs['exp_date'], format = "%d-%b-%y")
	latest_rcr = current_certs[current_certs['group']=='Responsible Conduct of Research (RCR)'].groupby('recipient_name')['exp_date'].max()
	latest_rcr = latest_rcr.reset_index()
	return val in latest_rcr[latest_rcr['exp_date'].dt.date < now]['recipient_name'].tolist()

##Check for values
final_frame['hsr_val'] = final_frame['recipient_name'].apply(has_hsr)
final_frame['rcr_val'] = final_frame['recipient_name'].apply(has_rcr)
final_frame['hsr_exp'] = final_frame['recipient_name'].apply(hsr_expired)
final_frame['rcr_exp'] = final_frame['recipient_name'].apply(rcr_expired)

#Results output
framename= 'citi_records.csv'
final_frame.to_csv(framename, header = True, index = False)
print('Employee CITI Statuses saved to ', framename)
print('~'*60, '\n')
print('The Following Employee Entries Need Attention:')
print('*' * 60)
print('MISSING CERTIFICATIONS')
print('*' * 60)
for index, row in final_frame.iterrows():
	#Check if missing certification
	if row['rcr_val'] == False and row['hsr_val'] == True:
		print(row['recipient_name'], 'is missing their RCR documentation.')
		print('-' * 60)
		alerts_missing.append(row['recipient_name'] + '| RCR')
	if row['rcr_val'] == False and row['hsr_val'] == False:
		print(row['recipient_name'], 'is missing their RCR & HSR documentation.')
		print('-' * 60)
		alerts_missing.append(row['recipient_name'] + ' | HSR & RCR')
	if row['rcr_val'] == True and row['hsr_val'] == False:
		print(row['recipient_name'], 'is missing their HSR documentation')
		print('-' * 60)
		alerts_missing.append(row['recipient_name'] + ' | HSR')
	else:
		pass
print('\n')
print('EXPIRED CERTIFICATIONS')
print('*'*60) 

for index, row in final_frame.iterrows():
	#Check if certification has expired
	if row['hsr_exp'] == False and row['rcr_exp'] == True:
		print(row['recipient_name'], 'has an expired RCR certificate.')
		print('-' * 60)
		alerts_expired.append(row['recipient_name'] + '| Expired RCR')
	if row['hsr_exp'] == True and row['rcr_exp'] == True:
		print(row['recipient_name'], 'has expired RCR & HSR certificates.')
		print('-' * 60)
		alerts_expired.append(row['recipient_name'] + ' | Expired HSR & RCR')
	if row['hsr_exp'] == True and row['rcr_exp'] == False:
		print(row['recipient_name'], 'has an expired HSR certificate')
		print('-' * 60)
		alerts_expired.append(row['recipient_name'] + ' | Expired HSR')
	else:
		pass
print('~'*60, '\n')
if alerts_missing or alerts_expired:
	with open('alerts.txt', 'w') as file:
		file.write('='*30)
		file.write('MISSING CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
		file.write('='*30 + '\n')
		for alert in alerts_missing:
			file.write('%s\n' % alert)
		file.write('='*30)
		file.write('EXPIRED CERTIFICATIONS AS OF ' + dt.date.today().strftime("%Y-%m-%d"))
		file.write('='*30 + '\n')
		for alert in alerts_expired:
			file.write('%s\n' % alert)
	print('Saved as alerts.txt')
