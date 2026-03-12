# params.py

import requests
from xss_detector import check_reflection

def test_url_params(url, payloads):

    for payload in payloads:

        test_url = f"{url}?q={payload}"

        try:

            r = requests.get(test_url, timeout=6)

            if check_reflection(payload, r.text):

                print("[REFLECTION FOUND]", test_url)

        except:
            continue
