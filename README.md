# certscrape
CITI Certification Scraper

This Python script scans all PDF files in a provided directory (including subdirectories), specifically for CITI Training Certifications.

It compiles the following information from each CITI Certificate read:
- CITI Record Number
- Name of Recipient (Full, family, and given name)
- Certification Issue Date
- Expiration Date
- Curriculum Group for Certificate (e.g. RCR)

The script then adds all the information into a .CSV file with the appropraite columns. If the scraper cannot find any of the given information, it will note the missing information and place an "NA" entry for that record.
In the event that the CITI Record Number cannot be found, the script records the PDF filename in its place.

This scraper is mainly for IRB use to document who has what CITI certification and set up monitoring.
