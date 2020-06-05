from ares import CVESearch
import cveIdList
import os
import time
import json

# Version using the ares wrapper for Circl.lu

def showProgress(counter):
    os.system('clear')
    print(f"Downloaded {counter} CVEs")
    print(f"Remaining: {len(cveIdList.cves) - (counter)}")

    remaining = len(cveIdList.cves) - (counter)
    print(f"Estimated waiting time: {remaining / 20 * 30} seconds / {remaining / 20 * 30 / 60} minutes")


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

        if counter%20 == 0:
            showProgress(counter)
            time.sleep(30)


if __name__ == "__main__":
    main()
