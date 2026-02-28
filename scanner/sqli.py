
import requests
from urllib.parse import urlencode
from .param_discovery import discover_params
from .detection import similarity, boolean_test, time_test

def scan_sqli(url):

    results=[]
    params = discover_params(url)

    if not params:
        return []

    try:
        normal = requests.get(url, timeout=8, verify=False).text
    except:
        return []

    for param in params:

        test_payload = "'"

        try:
            r = requests.get(url + "?" + urlencode({param:test_payload}), timeout=8, verify=False)
        except:
            continue

        sim = similarity(normal, r.text)

        # STEP 1 — Response difference threshold
        if sim > 0.98:
            continue

        # STEP 2 — Boolean confirmation
        boolean = boolean_test(url, param)

        # STEP 3 — Time confirmation
        timing = time_test(url, param)

        confidence = 0
        if sim < 0.98: confidence += 1
        if boolean: confidence += 1
        if timing: confidence += 1

        # -------------------------
        # Confidence Logic
        # -------------------------
        if confidence >= 2:

            results.append({
                "type":"SQL Injection",
                "parameter":param,
                "confidence":"High" if confidence==3 else "Medium",
                "url":url
            })

        elif confidence == 1:

            results.append({
                "type":"Possible SQL Injection",
                "parameter":param,
                "confidence":"Low",
                "url":url
            })

    return results
