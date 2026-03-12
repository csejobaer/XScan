# scanner.py

import requests
import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from endpoint_finder import discover_endpoints
from async_crawler import crawl
from payload_library import generate_payload_set
from xss_detector import check_reflection
from sensitive_file_detector import detect_sensitive_files
from subdomain_enum import discover_subdomains
from url_normalizer import deduplicate
from rate_limiter import RateLimiter

results = {
    "target": "",
    "pages": [],
    "reflections": [],
    "dom_xss": [],
    "subdomains": [],
    "sensitive_files": [],
    "waf": None
}


# -----------------------------
# WAF Detection
# -----------------------------
def detect_waf(target):

    print("[*] Detecting WAF")

    try:

        r = requests.get(target, timeout=5)

        headers = str(r.headers).lower()

        waf_signatures = {
            "cloudflare": "cloudflare",
            "akamai": "akamai",
            "sucuri": "sucuri",
            "imperva": "incapsula",
            "f5": "bigip"
        }

        for name, sig in waf_signatures.items():

            if sig in headers:
                print(f"[WAF DETECTED] {name}")
                return name

    except:
        pass

    print("[WAF] None detected")
    return None


# -----------------------------
# DOM XSS detection
# -----------------------------
def detect_dom_xss(page):

    try:

        r = requests.get(page, timeout=5)

        dangerous = [
            "document.write",
            "innerHTML",
            "outerHTML",
            "eval(",
            "setTimeout(",
            "setInterval("
        ]

        for d in dangerous:

            if d in r.text:

                print(f"[DOM XSS SINK] {page} -> {d}")

                results["dom_xss"].append({
                    "page": page,
                    "sink": d
                })

    except:
        pass


# -----------------------------
# XSS testing
# -----------------------------
def test_page(page, payloads, limiter):

    for payload in payloads:

        limiter.wait()

        try:

            url = f"{page}?q={payload}"

            r = requests.get(url, timeout=5)

            if check_reflection(payload, r.text):

                print(f"[REFLECTION] {url}")

                results["reflections"].append(url)

        except:
            pass


# -----------------------------
# Progress display
# -----------------------------
def progress(current, total):

    percent = (current / total) * 100

    print(f"[SCAN] {current}/{total} ({percent:.1f}%)")


# -----------------------------
# Report generator
# -----------------------------
def save_report():

    filename = "scan_report.json"

    with open(filename, "w") as f:

        json.dump(results, f, indent=4)

    print(f"\n[REPORT SAVED] {filename}")


# -----------------------------
# Main scanner
# -----------------------------
def main():

    target = input("Enter target URL: ").strip()

    results["target"] = target

    limiter = RateLimiter(0.2)

    print("\n[*] Starting reconnaissance")

    # Endpoint discovery
    pages = set(discover_endpoints(target))
    pages.add(target)

    # Subdomain discovery
    print("\n[*] Subdomain discovery")

    domain = urlparse(target).netloc
    subs = discover_subdomains(domain)

    results["subdomains"] = subs
    pages.update(subs)

    # Sensitive files
    print("\n[*] Checking sensitive files")

    sensitive = detect_sensitive_files(target)

    results["sensitive_files"] = sensitive

    # Crawl
    print("\n[*] Crawling pages")

    crawled = asyncio.run(crawl(list(pages)))

    pages.update(crawled)

    pages = set(deduplicate(list(pages)))

    results["pages"] = list(pages)

    print(f"\n[*] Pages discovered: {len(pages)}")

    # WAF detection
    results["waf"] = detect_waf(target)

    # DOM XSS scan
    print("\n[*] DOM XSS analysis")

    for page in pages:

        detect_dom_xss(page)

    # Payload generation
    payloads = generate_payload_set()

    print(f"\n[*] Payloads loaded: {len(payloads)}")

    print("\n[*] Starting XSS scan\n")

    start = time.time()

    with ThreadPoolExecutor(max_workers=15) as executor:

        for i, page in enumerate(pages):

            progress(i + 1, len(pages))

            executor.submit(test_page, page, payloads, limiter)

    end = time.time()

    print("\n[*] Scan complete")

    print(f"[+] Reflections found: {len(results['reflections'])}")
    print(f"[+] DOM sinks found: {len(results['dom_xss'])}")

    print(f"[+] Scan time: {round(end-start,2)} seconds")

    save_report()


if __name__ == "__main__":
    main()
