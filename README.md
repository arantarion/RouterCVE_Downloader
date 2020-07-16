# RouterCVE Downloader
Just a bunch of quick and dirty python scripts to download CVEs of common router software
as a json file

## Usage
- Use createCveID_List.py to get CVE IDs by Vendor and Product as cveIdList.py file
- Use cveDownloader.py to download the full cve as json from all specified IDs and save them as one excel or csv file
- Use nGramCount.py to calculate most frequently used words, bi/tri-grams in the summary of all CVEs
