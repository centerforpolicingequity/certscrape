#Import packages
import pandas as pd
import pdfquery
import os

#Set up lists and directory info
directory = 'Directory where CITI certificates are stored'
lst = []
lst2 = []
lst3 = []
lst4 = []
lst5 = []
cols = ['cert_number', 'recipient_name', 'cert_date', 'exp_date', 'group']


print('Scanning CITI Certificates in', directory, '\n')

#Loop over all CITI Certificates in Directory
for file in os.listdir(directory):
	if file.endswith(".pdf"):
		print('\n' 'Scanning', file)
		with open("{}/{}".format(directory,file), 'rb') as doc:
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
				lst2.append(recipient_name)
			except IndexError:
				print('No Recipient Found')
				recipient_name = 'NA'
				lst2.append(recipient_name)

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
print('\n','Compiling Data...')
frame = pd.DataFrame(list(zip(lst, lst2, lst3, lst4, lst5)), columns = cols )
print('\n', 'Saving to File...')
framename = "certificates.csv"
frame.to_csv(framename, header = True, index = False)
print('\n', 'CITI Scan Complete!')
print('\n','Records saved under', framename)