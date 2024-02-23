# certscrape
CITI Certification Scraper

This Python script scans all PDF files in a provided directory (including subdirectories), specifically for CITI Training Certifications.

It compiles the following information from each CITI Certificate read, using a certain expected location on the document:
- CITI Record Number
- Name of Recipient
- Certification Issue Date
- Expiration Date
- Curriculum Group for Certificate (e.g. RCR)

The script then adds all the information into a .CSV file with the appropraite columns. If the scraper cannot find any of the given information, it will note the missing information and place an "NA" entry for that record.

In the event that the CITI Record Number cannot be found, the script records the PDF filename in its place.

*Please Note:* The scraper is designed to scrape CERTIFICATES, not full records. Trying to scrape the full record PDF will result in missing and/or distorted information.

This scraper is mainly for IRB use to document who has what CITI certification and set up monitoring.
