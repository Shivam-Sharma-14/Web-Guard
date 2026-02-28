import requests

def passive_scan(url):
    r=requests.get(url, timeout=5, verify=False)
    h=r.headers
    issues=[]

    if "Content-Security-Policy" not in h:
        issues.append("Missing CSP")

    if "X-Frame-Options" not in h:
        issues.append("Missing X-Frame-Options")

    if "Server" in h:
        issues.append("Server Disclosure: "+h["Server"])

    return [{"type":"Passive","issue":i,"url":url} for i in issues]