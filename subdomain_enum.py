# subdomain_enum.py

import requests

COMMON_SUBDOMAINS = [
"www","api","dev","test","staging","beta",
"admin","portal","blog","shop","cdn","static",
"img","media","files","dashboard"
]

def discover_subdomains(domain):

    found=[]

    print("[*] Subdomain discovery started")

    for sub in COMMON_SUBDOMAINS:

        url=f"https://{sub}.{domain}"

        try:

            r=requests.get(url,timeout=5)

            if r.status_code < 500:

                print("[SUBDOMAIN FOUND]",url)

                found.append(url)

        except:
            continue

    return found
