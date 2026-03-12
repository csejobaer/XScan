# param_bruteforce.py

import requests

COMMON_PARAMS = [
"id","page","q","search","query",
"file","url","redirect","next",
"user","username","email"
]

def brute_params(url):

    discovered=[]

    for param in COMMON_PARAMS:

        test=f"{url}?{param}=test"

        try:

            r=requests.get(test,timeout=5)

            if "test" in r.text:

                print("[PARAM FOUND]",param)

                discovered.append(param)

        except:
            continue

    return discovered
