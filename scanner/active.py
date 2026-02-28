import requests
from .payloads import ACTIVE_PAYLOADS

def active_scan(url):

    results=[]

    for p in ACTIVE_PAYLOADS:
        try:
            r=requests.get(url+"?input="+p,timeout=5)

            if p in r.text:
                results.append({
                    "type":"Active Reflection",
                    "payload":p,
                    "url":url
                })
        except:
            pass

    return results