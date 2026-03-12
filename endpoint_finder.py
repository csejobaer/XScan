# endpoint_finder.py
import requests
import time
from urllib.parse import urljoin

# Default internal wordlist if file missing
DEFAULT_WORDLIST = [
"admin","login","logout","dashboard","panel","controlpanel",
"api","api/v1","api/v2","rest","graphql",
"user","users","profile","account","settings",
"search","query","find",
"upload","uploads","files","download",
"config","config.php",".env",".git","backup",
"test","dev","beta","staging",
"blog","news","shop","cart","checkout",
"contact","about","support"
]

HEADERS = [
{"User-Agent":"Mozilla/5.0"},
{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
{"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)"}
]

def load_wordlist():

    try:
        with open("wordlist.txt") as f:
            print("[*] Using external wordlist.txt")
            return [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print("[!] wordlist.txt not found — using built-in wordlist")
        return DEFAULT_WORDLIST


def detect_waf(response):

    waf_signatures = {
        "cloudflare":"cloudflare",
        "sucuri":"sucuri",
        "akamai":"akamai",
        "imperva":"incapsula"
    }

    for waf in waf_signatures:
        if waf in response.lower():
            return waf_signatures[waf]

    return None


def discover_endpoints(base_url):

    wordlist = load_wordlist()
    discovered = []

    print(f"[*] Testing {len(wordlist)} common paths")

    for i, word in enumerate(wordlist):

        url = urljoin(base_url, word)

        try:

            headers = HEADERS[i % len(HEADERS)]

            r = requests.get(url, headers=headers, timeout=8)

            waf = detect_waf(r.text)

            if waf:
                print(f"[!] Possible WAF detected: {waf}")

            if r.status_code in [200,301,302,403]:

                print(f"[FOUND] {url} (status {r.status_code})")

                discovered.append(url)

            else:

                print(f"[SKIP] {url}")

            time.sleep(0.5)

        except requests.exceptions.RequestException:

            print(f"[ERROR] {url}")

    return discovered
