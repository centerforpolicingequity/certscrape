#Splash
import sys, os
path = os.getcwd()

print('~'* 60)
print('CITI UPDATE CENTER')
print('Center for Policing Equity OHRP')
print('v.1.1')
print('~' * 60)

print('Importing Modules...')
import cert
import scan_citi_files
import email_updates

#Menu
def main_menu():
	"""Main Menu"""
	print('\n'*3)
	print(' MAIN MENU '.center(60, '*'))
	print("1. Scan CITI Certificates")
	print('2. Update CITI Statuses')
	print("3. E-Mail Weekly Update to CPE")
	print("4. Exit")
	print('\n')
	
	selection = input('Please select one of the above options: ')
	if selection == '1':
		cert.citi_cert_scan()
		complete = input('Are there any other tasks you wish to perform? (Y/N): ')
		if complete == 'Y':
			main_menu()
			selection = input('Please select one of the above options: ')
		elif complete == 'N':
			print('Thank you. Goodbye.')
			sys.exit(1)

	elif selection == '2':
		scan_citi_files.update_citi_statuses()
		complete = input('Are there any other tasks you wish to perform? (Y/N): ')
		if complete == 'Y':
			main_menu()
			selection = input('Please select one of the above options: ')
		elif complete == 'N':
			print('Thank you. Goodbye.')
			sys.exit(1)
	
	elif selection == '3':
		email_updates.email_update()
		complete = input('Are there any other tasks you wish to perform? (Y/N): ')
		if complete == 'Y':
			main_menu()
			selection = input('Please select one of the above options: ')
		elif complete == 'N':
			print('Thank you. Goodbye.')
			sys.exit(1)

	elif selection == '4':
		print('Thank you. Goodbye.')
		sys.exit(1)

main_menu()
