import requests
import re

def ajax_spider(url):
    r=requests.get(url, timeout=5, verify=False)
    scripts=re.findall(r'src="(.*?)"',r.text)

    return [{"type":"AJAX","script":s,"url":url} for s in scripts]