# CITI Update Center
## Current Version: 2.1.1

This Python program scans all PDF files in a provided directory (including subdirectories), specifically for CITI Training Certifications. It can also keep an up-to-date log of all CITI certifications held by current employees and those listed as key personnel on CPE projects. 

**Scan CITI Certificates**

Compiles the following information from each CITI Certificate read, using a certain expected location on the document:
- CITI Record Number
- Name of Recipient (Full, family, and given name)
- Certification Issue Date
- Expiration Date
- Curriculum Group for Certificate (e.g. RCR)

The script then adds all the information into the CITI Status Google Sheet with the appropraite columns. If the scraper cannot find any of the given information, it will note the missing information and place an "NA" entry for that record.

In the event that the CITI Record Number cannot be found, the script records the PDF filename in its place.

*Please Note:* The scraper is designed to scrape CERTIFICATES, not full records. Trying to scrape the full record PDF will result in missing and/or distorted information.

This scraper is mainly for OHRP use to document who has what CITI certification and set up monitoring.

**Update CITI Status** 

Scans the current list of employees from BambooHR and compares it to the list of members of the Science Team, those listed as Key Personnel, and all names listed within the log of CITI certificates. It then updates a Google Sheet and sends an update email to the CPE OHRP email.

Program Icon: https://icon-icons.com/icon/news-newspaper/177008

Other requirements:

	/certificates - folder that the script searches for PDF files within.
	
	api.key - key for the Google API. (Can only be accessed via the OHRP)

	creds.json, email.json - credentials for accessing the Google API. (Can only be accessed via the OHRP)

	spreadsheet.key - spreadsheet ID. (Can only be accessed via the OHRP)
