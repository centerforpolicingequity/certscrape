#CITI Certificate Scraper
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity

#Last Updated: June 7 2024

def citi_cert_scan():
	"""Scans for CITI Certificates"""
	print('~'* 60)
	print('CITI Certificate Scraper')
	print('Center for Policing Equity OHRP')
	print('v.1.6')
	print('2024', '\n')
	print('~'*60)


	#Import packages
	import pandas as pd
	import pdfquery
	import os
	from glob import iglob

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


	new_file = input('Is this for a new CITI Certificate Table? (Y/N): ')
	if new_file == 'Y':
		header_select = True
	else:
		header_select = False
	print('\n', 'Scanning CITI Certificates', '\n')

#Loop over all CITI Certificates in Directory
	for file in directory:
		if file.endswith(".pdf"):
			print('\n' 'Scanning', file)
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
					print('This is Record ID: ',cert_num)
					lst.append(cert_num)
				except IndexError:
					print('No Record ID Found')
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
					print('This record is for: ', recipient_name)
					name_split = recipient_name.split()
					if len(name_split) == 2:
						name_first = name_split[0].strip()
						name_last = name_split[1].strip()
					elif len(name_split) == 3:
						name_first = name_split[0].strip() + ' ' + name_split[1].strip()
						name_last = name_split[2].strip()
					print('First Name: ', name_first)
					print('Last Name: ', name_last)
					lst2.append(recipient_name)
					lst2_a.append(name_first)
					lst2_b.append(name_last)
				except IndexError:
					print('No Recipient Found')
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
					print('The Completion Date Is: ', cert_date)
					lst3.append(cert_date)
				except IndexError:
					print('No Completion Date Found')
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
					print('The Expiration Date Is: ', exp_date)
					lst4.append(exp_date)
				except IndexError:
					print('No Expiration Date Found')
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
					print('Course: ', group)
					lst5.append(group)
				except IndexError:
					print('No Course Found')
					group = 'NA'
					lst5.append(group)



	#Compile to pandas DataFrame and Export
	print('\n Compiling Data...')
	frame = pd.DataFrame(list(zip(lst, lst2, lst2_b, lst2_a, lst3, lst4, lst5)), columns = cols )
	print('\n', 'Saving to File...')
	framename = "citi.csv"
	frame.to_csv(framename, mode = 'a', header = header_select, index = False)
	print('\n', 'CITI Scan Complete!')
	print('\n','Records saved under', framename)


if __name__ == '__main':
	print('Running CITI Scan standalone...')
	citi_cert_scan()

else:
	print('Citi Certification Imported...')

