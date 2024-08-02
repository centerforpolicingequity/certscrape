# CITI Update Center


This Python script scans all PDF files in a provided directory (including subdirectories), specifically for CITI Training Certifications. It can also keep an up-to-date log of all CITI certifications held by current employees and those listed as key personnel on CPE projects. 

*NEW* GUI Added!

Citi Update Center.py
Runs the main GUI for the CITI Update Center. From here, a user can select one of five options: Scan CITI Certificates, Update CITI Status, Email the Weekly Update to the CPE OHRP Email, Add Key Personnel, or exit.

Scan CITI Certificates
Compiles the following information from each CITI Certificate read, using a certain expected location on the document:
- CITI Record Number
- Name of Recipient (Full, family, and given name)
- Certification Issue Date
- Expiration Date
- Curriculum Group for Certificate (e.g. RCR)

The script then adds all the information into a .CSV file with the appropraite columns. If the scraper cannot find any of the given information, it will note the missing information and place an "NA" entry for that record.

In the event that the CITI Record Number cannot be found, the script records the PDF filename in its place.

*Please Note:* The scraper is designed to scrape CERTIFICATES, not full records. Trying to scrape the full record PDF will result in missing and/or distorted information.

This scraper is mainly for IRB use to document who has what CITI certification and set up monitoring. Outputs a log of CITI Certificates labeled 'citi.csv'.

Update CITI Status
Scans the current list of employees from BambooHR and compares it to the list of members of the Science Team, those listed as Key Personnel, and all names listed within the log of CITI certificates. It then generates up to four files:

	1. former.txt - a list of personnel who are listed within the CITI log but not the current employee list, indicating that the respective employees may no longer be with CPE.

	2. alerts.txt - a list of employees listed as Key Personnel on one or more projects who are either missing required CITI certificates or else have expired certificates. 

	3. sci_alerts.txt - a list of employees listed as members of the Science division who are either missing required CITI certificates or else have expired certificates.

	4. citi_records.csv - a table of employees listing their name, whether they have required certificates, if those certificates are expired, if they are listed as key personnel, and if they are listed as members of the Science division.

Email Updates
Uses the Gmail API to combine and email alert files to the CPE OHRP email. Typically run on a weekly basis for update purposes.

Add Key Personnel
Adds needed personnel (e.g. science_team.list) to file of key personnel (e.g. key_personnel.list).

Other required files:

	key_personnel.list - a plaintext file listing employees who are considered Key Personnel on one or more projects.

	science_team.list -a plaintext file listing employees who are members of the Science division.

	credentials.json - credentials for accessing the Gmail API. 

	general_bamboohr_org_chart.csv - A list of employees downloaded from the "People" directory on BambooHR.

	quickstart.py - a script for initial setup of the Gmail API.
