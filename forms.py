import requests
from xss_detector import check_reflection

def test_forms(url, payloads):

    for payload in payloads:

        data = {"input": payload}

        try:

            r = requests.post(url, data=data)

            if check_reflection(payload, r.text):

                print("[FORM REFLECTION]", url)

        except:
            pass
