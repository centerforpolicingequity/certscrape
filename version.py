import pyinstaller_versionfile as pv

pv.create_versionfile(
	output_file = "versionfile.txt",
	version = "2.1",
	company_name = "Center for Policing Equity",
	file_description = "OHRP CITI App",
	internal_name = "CITI Update Center",
	legal_copyright = "Center for Poling Equity. Free to reproduce with attribution.",
	original_filename = "CITI Update Center.exe",
	product_name = "CITI Update Center")