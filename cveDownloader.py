#!/usr/bin/env python
from ares import CVESearch
import cveIdList
import os
import sys
import time
import json
import platform
import glob
import pandas as pd

"""
By Henry Weckermann
A script to automatically download CVEs by CVE-ID as Json Files from Circl.lu and convert them to one excel or csv file containing important information from the
CVE entry.
Before usage it is recommended to create a cveIdList.py file containing a list of CVE-Ids you want to download. This could be done with the createCveID_List.py script.
Afterwards you can create a wordcount of mono/bi/tri grams with the freqdist_top_words.py script (you should export the summary column from the excel file first)

Usage: 
./cveDownloader.py 		-> Downloads all CVE Entries by ID (cveIdList) into a seperate Json File in the ./jsonFiles Folder
./cveDownloader.py --excel 	-> additionally creates one excel file containing only selected parts of all CVEs from the ./jsonFiles folder [access', 'capec', 'cvss', 
				   'impact', 'summary']
./cveDownloader.py --csv	-> same as "excel" but csv output
"""


# Version using the ares wrapper for Circl.lu
THRESHOLD = 20
SLEEPTIME = 30


def showProgress(counter):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    print(f"Downloaded {counter} CVEs")
    print(f"Remaining: {len(cveIdList.cves) - (counter)}")

    remaining = len(cveIdList.cves) - (counter)
    print(f"Estimated waiting time: {remaining / THRESHOLD * SLEEPTIME} seconds / {remaining / THRESHOLD * SLEEPTIME / 60} minutes")


def main():
    cveObj = CVESearch()
    counter = 0

    try:
        os.makedirs("jsonFiles")
    except FileExistsError:
        pass # already exists

    os.chdir("jsonFiles")

    print("By Henry Weckermann")
    print(f"Downloading {len(cveIdList.cves)} files to Folder: /jsonFiles")
    print("Please be patient as the program needs to wait every 20 entries to avoid an ip ban")


    for cve in cveIdList.cves:
        jsonData = cveObj.id(cve)
        filename = cve

        with open(cve + ".json", "w") as file:
            #file.write(jsonData)
            json.dump(jsonData, file)

        counter = counter + 1

        if counter%THRESHOLD == 0:
            showProgress(counter)
            time.sleep(SLEEPTIME)


def createExcel(filetype):
    temp  = pd.DataFrame()

    path = 'jsonFiles'

    json_pattern = os.path.join(path, '*.json')
    file_list = glob.glob(json_pattern)


    for file in file_list:
        data = pd.read_json(file, lines=True)
        temp = temp.append(data, ignore_index = True)

    df = temp.loc[:, ['access', 'capec', 'cvss', 'impact', 'summary']]

    if filetype == "excel":
        df.to_excel("cvesFromJson.xlsx")
    elif filetype == "csv":
        df.to_csv("cvesFromJson.csv")

if __name__ == "__main__":

    if not "--no-download" in sys.argv:
        main()

    if "--excel" in sys.argv:
        createExcel("excel")
    if "--csv" in sys.argv:
        createExcel("csv")

