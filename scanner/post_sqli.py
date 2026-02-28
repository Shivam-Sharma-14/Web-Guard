
import requests
from bs4 import BeautifulSoup
from .payloads import SQLI_PAYLOADS

def scan_post_sqli(url):

    results=[]

    try:
        r=requests.get(url,timeout=6,verify=False)
        soup=BeautifulSoup(r.text,"html.parser")
        forms=soup.find_all("form")

        for form in forms:

            action=form.get("action")
            method=form.get("method","get").lower()

            if method!="post":
                continue

            target = url if not action else action

            inputs=form.find_all("input")

            for payload in SQLI_PAYLOADS:

                data={}

                for inp in inputs:
                    name=inp.get("name")
                    if name:
                        data[name]=payload

                res=requests.post(target,data=data,timeout=6,verify=False)

                if "sql" in res.text.lower():
                    results.append({
                        "type":"POST SQL Injection",
                        "url":target,
                        "payload":payload
                    })

    except:
        pass

    return results
