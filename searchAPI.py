#!/usr/bin/python
# Search the CVE service offered by CircLU (https://www.circl.lu/services/cve-search/)

import requests
import argparse
import sys
import json


def search_cve(_cve):
    """Simple CVE search"""
    print "Searching: " + _cve
    SEARCHURL = "http://cve.circl.lu/api/cve/" + _cve
    r = requests.get(SEARCHURL)
    if r.status_code != 200:
        sys.exit("Something has gone horribly wrong.")
    else:
        data = json.loads(r.text)
        print "Summary: " + data['summary']
        print "CVSS Score: " + str(data['cvss'])


def show_vendor_product(_vendor, _product):
    """Show a specific product for a vendor"""
    print "Searching: " + _product + " from " + _vendor
    SEARCHURL =  "http://cve.circl.lu/api/search/" + _vendor + "/" + _product
    r = requests.get(SEARCHURL)
    if r.status_code != 200:
        sys.exit("Something has gone horribly wrong.")
    else:
        jdata = json.loads(r.text)
        for item in jdata:
            print "\nSummary: " + item['summary']
            print "CVE: " + item['id']
            print "CVSS: " + str(item['cvss'])


def list_vendor_products(_vendor):
    """Search for a vendor"""
    print "Vendor Search: " + _vendor,
    SEARCHURL = "http://cve.circl.lu/api/browse/" + _vendor
    r = requests.get(SEARCHURL)
    if r.status_code != 200:
        sys.exit("Something has gone horribly wrong.")
    else:
        print " ... " + str(r.status_code)
        try:
            data = json.loads(r.text)['product']
            print "Available products from " + _vendor
            for item in data:
                print item
        except:
            sys.exit("[!!] Vendor not in list")


def list_vendors():
    """List all the available vendors in the API"""
    print "Listing Vendors",
    SEARCHURL = "http://cve.circl.lu/api/browse"
    r = requests.get(SEARCHURL)
    if r.status_code != 200:
        sys.exit("Something has gone horribly wrong.")
    else:
        print " ... " + str(r.status_code)
        data = json.loads(r.text)['vendor']
        print "Available Vendors: "
        for item in data:
            print item


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='CIRCL CVE API Search')
    parser.add_argument('--list-vendors', '-l', dest='listvendors', action='store_true', help='List the available vendors')
    parser.add_argument('--product', '-p', dest='product', help='Search for a product')
    parser.add_argument('--vendors', '-v', dest='vendor', help='Search for a vendor')
    parser.add_argument('--cve', '-c', dest='cve', help='Search for this CVE')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    _cve = args.cve
    _product = args.product
    _vendor = args.vendor
    _listvendors = args.listvendors

    # TODO: This needs to be improved
    if (args.vendor and args.product):
        show_vendor_product(_vendor, _product)
    else:
        if args.cve:
            search_cve(_cve)
        elif (args.vendor and not args.product):
            list_vendor_products(_vendor)
        elif args.listvendors:
            list_vendors()

if __name__ == '__main__':
    __main__()
