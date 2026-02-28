
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

def discover_params(url):

    found_params = set()

    try:
        r = requests.get(url, timeout=5, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")

        # GET params already in URL
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        for p in qs:
            found_params.add(p)

        # form inputs
        forms = soup.find_all("form")

        for form in forms:
            inputs = form.find_all("input")
            for inp in inputs:
                name = inp.get("name")
                if name:
                    found_params.add(name)

    except:
        pass

    return list(found_params)
