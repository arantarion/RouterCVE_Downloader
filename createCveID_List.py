import re
import requests
import json

# Henry Weckermann
# Because the Circl.lu API does not allow direct search by vendor and product
# I had to do it another way
# This script downloades the whole html content of the cvedetail.com websites of specified products
# and searches for the CVE IDs in them, appening them to a set.

easy_cve = [
'https://www.cvedetails.com/vulnerability-list/vendor_id-438/product_id-26769/Adtran-AOS.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-218/product_id-50201/Alcatel-A30-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-43375/Asus-Asuswrt.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-27483/Asus-Rt-ac68u-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-25596/Asus-Rt-ac66u-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-25606/Asus-Rt-n56u-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-54437/Asus-Rt-ac3200-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-37524/Asus-Rt-ac1750-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-50179/Asus-Gt-ac5300-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-30988/Asus-Rt-ac87u-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-25598/Asus-Rt-n66u-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3447/product_id-32825/Asus-Wl-330nul-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-1369/product_id-32843/Belkin-N600-Db-Wi-fi-Dual-band-N-Router-F9k1102-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-1369/product_id-45198/Belkin-N750-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-5420/product_id-40643/Broadcom-Bcm4355c0-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-899/product_id-40187/D-link-Dir-850l-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-899/product_id-34472/D-link-Dir-868l-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-899/product_id-45559/D-link-Dsl-3782-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-899/product_id-46214/D-link-Dir-816-A2-Firmware.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-9341/product_id-16564/Dd-wrt-Dd-wrt.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-3046/Extremenetworks.html',
'https://www.cvedetails.com/vulnerability-list/vendor_id-874/product_id-26642/Juniper-Screenos.html'
]

# Regex for finding CVEs in the received file
p = re.compile('(CVE-(1999|2\d{3})-(0\d{2}[1-9]|[1-9]\d{3,}))')


def step1():

    cve_list = []

    for url in easy_cve:
        try:
            r = requests.get(url)
            text = r.text
            cve_pos = p.findall(text)
            cve_list.append(list(set([i[0] for i in cve_pos])))

        except:
            print(f'Error in URL: {url}. Could not download')
            cve_list.append('Error')

    return makeFlatList(cve_list)


def step2():

    enum_cve = [
    'https://www.cvedetails.com/vulnerability-list.php?vendor_id=16&product_id=19&version_id=&page={}&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=532&sha=bd51a01b646bad788bdc715f12e17fa177698ba8',
    'https://www.cvedetails.com/vulnerability-list.php?vendor_id=18578&product_id=&version_id=&page={}&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=3&trc=4&sha=7f4a013a773f2999d7344963c7478757268308e7',
    'https://www.cvedetails.com/vulnerability-list.php?vendor_id=874&product_id=3989&version_id=&page={}&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=202&sha=b655c7938769380aa5cedb5222d7f8c7236e9245',
    'https://www.cvedetails.com/vulnerability-list.php?vendor_id=12508&product_id=23641&version_id=&page={}&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=17&sha=54982f4894183538bda0bf316e8a38e16187ea4f'
    ]

    cve_list = []

    for url in enum_cve:
        for i in range(1,12):
            page = i
            try:
                rURL = url.format(page)
                r = requests.get(rURL)
                text = r.text
                cve_pos = p.findall(text)
                cve_list.append(list(set([i[0] for i in cve_pos])))

            except:
                pass

    return makeFlatList(cve_list)


def makeFlatList(liste):
    return list(set([item for sublist in liste for item in sublist]))


if __name__ == '__main__':
    easy_list = step1()
    hard_list = step2()

    complete_list = easy_list + hard_list

    with open("cveIdList.py", "w") as file:
        file.write('cves = [')
        file.write(',\n'.join(complete_list))
        file.write(']')

