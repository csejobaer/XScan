# subdomains.py
import requests

common_subdomains = [
    "www","admin","api","dev","test","staging","portal","blog","shop","beta"
]

def discover_subdomains(domain):
    discovered = []
    print("[*] Discovering subdomains...")
    for sub in common_subdomains:
        url = f"https://{sub}.{domain}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code < 500:
                print("[SUBDOMAIN FOUND]", url)
                discovered.append(url)
        except:
            continue
    return discovered
