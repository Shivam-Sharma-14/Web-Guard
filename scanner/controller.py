from .spider import run_spider
from .passive import passive_scan
from .active import active_scan
from .sqli import scan_sqli
from .xss import scan_xss
from .ajax_spider import ajax_spider
from .severity import calculate_score
from .post_sqli import scan_post_sqli


def add_severity(results):

    for r in results:

        text = str(r)

        sev = calculate_score(text)

        r["severity"] = sev["level"]
        r["score"] = sev["score"]
        r["color"] = sev["color"]

    return sorted(results, key=lambda x: x["score"], reverse=True)



def run_scan(url,scan):

    if scan=="spider":
        results = run_spider(url)

    elif scan=="passive":
        results = passive_scan(url)

    elif scan=="active":
        results = active_scan(url)

    elif scan=="sqli":
        results = scan_sqli(url) + scan_post_sqli(url)

    elif scan=="xss":
        results = scan_xss(url)

    elif scan=="ajax":
        results = ajax_spider(url)

    # elif scan=="sqli":
    #     results = scan_sqli(url) + scan_post_sqli(url)

    else:
        results=[{"issue":"Invalid Scan"}]

    return add_severity(results)