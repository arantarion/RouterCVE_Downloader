# RouterCVE Downloader
Just a bunch of quick and dirty python scripts to download CVEs of common router software
as a json file

## Usage
- Use get_cve_ids.py to get CVE IDs by Vendor and Product
- Use download_cve_by_id.py to download the full cve as json from all specified IDs
- Use json_to_dataframe.py to transform all json files in the folder "jsonFiles" into a single Pandas dataframe
  and output a compact version of the dataframe as an excel file.