import wget
import os
from pymodis.downmodis import downModis
import requests
import re
import csv

with open('C:/EVA/THESIS/code/downloadxmllinks.csv', 'r') as u:
    urls = list(csv.reader(u))
#print(urls)
out_dir = "C:/EVA/THESIS/data/xml/"
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

print(error)
