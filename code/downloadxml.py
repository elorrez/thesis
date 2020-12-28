import wget
import os
from pymodis.downmodis import downModis
import requests
import re
import csv

with open('C:/EVA/THESIS/code/xmltodo.csv', 'r') as u:
    urls = list(csv.reader(u))
print(urls)

def get_hdf(urls):
    out_dir = "C:/EVA/THESIS/data/hdf/"
    os.chdir(out_dir)
    error = []
    for url in urls:
        #xml_url = url[0] + ".xml"
        name = re.split("/", url)[-1]
        try:
            r = requests.get(url, allow_redirects=True)
            open(name, "wb").write(r.content)
        except:
            error.append(url)

    return error

def get_xml(urls):
    out_dir = "C:/EVA/THESIS/data/xml/"
    os.chdir(out_dir)
    error = []
    for url in urls:
        xml_url = url[0] + ".xml"
        name = re.split("/", xml_url)[-1]
        try:
            r = requests.get(xml_url, allow_redirects=True)
            open(name, "wb").write(r.content)
        except:
            error.append(url)

    return error

error = get_xml(urls)

# url = 'https://e4ftl01.cr.usgs.gov//MODV6_Cmp_B/MOLT/MOD13A3.006/2013.01.01/MOD13A3.A2013001.h20v09.006.2015254151846.hdf.xml'
# r = requests.get(url, allow_redirects=True)
# open('MOD13A3.A2013001.h20v09.006.2015254151846.hdf.xml', "wb").write(r.content)
