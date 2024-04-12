#CITI Employee Search
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity
#Last Updated: April 12 2024

print('~'* 60)
print('CITI Employee Search Tool')
print('Center for Policing Equity OHRP')
print('v.1.0')
print('2024', '\n')
print('~'*60)

import pandas as pd
alerts = []
chart = []
#Import data
print('Reading Data...')
print('~'*60, '\n')
certs = pd.read_csv('citi.csv')
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
with open('former.txt', 'w') as file:
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

##Check for values
final_frame['hsr_val'] = final_frame['recipient_name'].apply(has_hsr)
final_frame['rcr_val'] = final_frame['recipient_name'].apply(has_rcr)


#Results output
framename= 'citi_records.csv'
final_frame.to_csv(framename, header = True, index = False)
print('Employee CITI Statuses saved to ', framename)
print('~'*60, '\n')
print('The Following Employee Entries Need Attention:')
print('*' * 60)
for index, row in final_frame.iterrows():
	#Check if current employee
	if row['rcr_val'] == False and row['hsr_val'] == True:
		print(row['recipient_name'], 'is missing their RCR documentation.')
		print('-' * 60)
		alerts.append(row['recipient_name'] + '| RCR')
	if row['rcr_val'] == False and row['hsr_val'] == False:
		print(row['recipient_name'], 'is missing their RCR & HSR documentation.')
		print('-' * 60)
		alerts.append(row['recipient_name'] + ' | HSR & RCR')
	if row['rcr_val'] == True and row['hsr_val'] == False:
		print(row['recipient_name'], 'is missing their HSR documentation')
		print('-' * 60)
		alerts.append(row['recipient_name'] + ' | HSR')
	else:
		pass

if alerts:
	with open('alerts.txt', 'w') as file:
		for alert in alerts:
			file.write('%s\n' % alert)
	print('Saved as alert.txt')
