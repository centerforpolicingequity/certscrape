#Splash
import sys, os
path = os.getcwd()

print('~'* 60)
print('CITI UPDATE CENTER')
print('Center for Policing Equity OHRP')
print('v.1.0')
print('~' * 60)
#Menu
def main_menu():
	print('\n'*3)
	print('MAIN MENU'.center(60, '*'))
	print("1. Scan CITI Certificates")
	print('2. Update CITI Statuses')
	print("3. E-Mail Weekly Update to CPE")
	print("4. Exit")
	print('\n')


main_menu()
selection = input('Please select one of the above options: ')

if selection == '1':
	import cert
	complete = input('Are there any other tasks you wish to perform? (Y/N): ')
	if complete == 'Y':
		main_menu()
	elif complete == 'N':
		print('Thank you. Goodbye.')
		sys.exit(1)

elif selection == '2':
	import scan_citi_files
	complete = input('Are there any other tasks you wish to perform? (Y/N): ')
	if complete == 'Y':
		main_menu()
	elif complete == 'N':
		print('Thank you. Goodbye.')
		sys.exit(1)

elif selection == '3':
	import email_updates
	complete = input('Are there any other tasks you wish to perform? (Y/N): ')
	if complete == 'Y':
		main_menu()
	elif complete == 'N':
		print('Thank you. Goodbye.')
		sys.exit(1)

elif selection == '4':
	print('Thank you. Goodbye.')
	sys.exit(1)

