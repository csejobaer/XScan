# scanner.py

import requests
from concurrent.futures import ThreadPoolExecutor
from endpoint_finder import discover_endpoints
from subdomain_enum import discover_subdomains
from sensitive_file_detector import detect_sensitive_files
from payload_library import generate_payload_set
from xss_detector import check_reflection
from async_crawler import crawl
from url_normalizer import deduplicate
from rate_limiter import RateLimiter
from urllib.parse import urlparse
import asyncio

results = {
    "reflections": [],
    "pages": [],
    "subdomains": [],
    "sensitive_files": []
}


def test_page(page, payloads, limiter):

    for payload in payloads:

        limiter.wait()

        try:
            url = f"{page}?q={payload}"

            r = requests.get(url, timeout=5)

            if check_reflection(payload, r.text):

                print(f"[XSS REFLECTION] {url}")

                results["reflections"].append(url)

        except:
            pass


def main():

    target = input("Enter target URL (e.g., https://example.com): ").strip()

    limiter = RateLimiter(0.3)

    print("\n[*] Endpoint discovery started")
    pages = set(discover_endpoints(target))

    pages.add(target)

    print("\n[*] Subdomain discovery started")
    domain = urlparse(target).netloc
    subs = discover_subdomains(domain)

    for s in subs:
        print(f"[SUBDOMAIN FOUND] {s}")

    results["subdomains"] = subs
    pages.update(subs)

    print("\n[*] Checking for sensitive files")
    sensitive = detect_sensitive_files(target)

    for s in sensitive:
        print(f"[SENSITIVE FILE FOUND] {s}")

    results["sensitive_files"] = sensitive

    print("\n[*] Crawling discovered pages")
    crawled = asyncio.run(crawl(list(pages)))

    pages.update(crawled)

    pages = set(deduplicate(list(pages)))

    results["pages"] = list(pages)

    print(f"\n[*] Total pages discovered: {len(pages)}")

    payloads = generate_payload_set()

    print(f"[*] Payloads loaded: {len(payloads)}")

    print("\n[*] Starting XSS tests\n")

    with ThreadPoolExecutor(max_workers=10) as executor:

        for i, page in enumerate(pages):

            print(f"[SCAN] {i+1}/{len(pages)} -> {page}")

            executor.submit(test_page, page, payloads, limiter)

    print("\n[*] Scan finished")

    print(f"[+] Reflections found: {len(results['reflections'])}")


if __name__ == "__main__":
    main()
