SEVERITY_RULES = {

    "Possible SQL Injection": 5.5,
    "SQL Injection": 9.5,

    "XSS": 8.0,
    "Active Reflection": 6.5,
    "Missing CSP": 5.0,
    "Missing X-Frame-Options": 4.0,
    "Server Disclosure": 3.5,
    "Spider": 0,
    "AJAX": 0
}


def calculate_score(issue):

    for key in SEVERITY_RULES:
        if key.lower() in str(issue).lower():
            score = SEVERITY_RULES[key]
            break
    else:
        score = 2.0


    if score >= 9:
        level = "Critical"
        color = "red"

    elif score >= 7:
        level = "High"
        color = "orange"

    elif score >= 4:
        level = "Medium"
        color = "gold"

    elif score > 0:
        level = "Low"
        color = "green"

    else:
        level = "Info"
        color = "gray"


    return {
        "score": score,
        "level": level,
        "color": color
    }