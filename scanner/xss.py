import requests
from .payloads import XSS_PAYLOADS

def scan_xss(url):

    results=[]

    for payload in XSS_PAYLOADS:
        try:
            r=requests.get(url+"?q="+payload,timeout=5)

            if payload in r.text:
                results.append({
                    "type":"XSS",
                    "payload":payload,
                    "url":url
                })
        except:
            pass

    return results