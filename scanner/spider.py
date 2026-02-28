import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse

def run_spider(url):
    visited=set()
    stack=[url]
    results=[]

    while stack:
        current=stack.pop()

        if current in visited:
            continue

        visited.add(current)

        try:
            r=requests.get(current,timeout=5,verify=False)
            soup=BeautifulSoup(r.text,"html.parser")

            for link in soup.find_all("a",href=True):
                full=urljoin(url,link["href"])
                if urlparse(full).netloc==urlparse(url).netloc:
                    stack.append(full)

            results.append({"type":"Spider","url":current,"status":"Crawled"})

        except:
            results.append({"type":"Spider","url":current,"status":"Failed"})

    return results