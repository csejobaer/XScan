# scanner.py

import asyncio
from urllib.parse import urlparse
from endpoint_finder import discover_endpoints
from js_route_extractor import extract_routes
from spa_route_extractor import extract_spa_routes
from js_param_extractor import extract_js_params
from param_bruteforce import brute_params
from subdomain_enum import discover_subdomains
from sensitive_file_detector import detect_sensitive_files
from async_crawler import crawl
from payload_library import generate_payload_set
from xss_detector import check_reflection
from report import save_report
from html_report import generate_html
from url_normalizer import deduplicate
from rate_limiter import RateLimiter
from robots_sitemap_harvester import harvest_robots, harvest_sitemap
from url_normalizer import deduplicate

# Global results dictionary
results = {
    "target": "",
    "pages": [],
    "params": [],
    "subdomains": [],
    "sensitive_files": [],
    "reflections": []
}

def main():
    target = input("Enter target URL (e.g., https://example.com): ")
    results["target"] = target
    domain = urlparse(target).netloc

    limiter = RateLimiter(1)

    # Start with a set of pages
    pages = set()
    pages.add(target)

    # Directory discovery
    pages.update(discover_endpoints(target))

    # Robots.txt + sitemap
    pages.update(harvest_robots(target))
    pages.update(harvest_sitemap(target))

    # JS route extraction
    pages.update(extract_routes(target))
    pages.update(extract_spa_routes(target))

    # Subdomain discovery
    subs = discover_subdomains(domain)
    results["subdomains"] = subs
    pages.update(subs)

    # Sensitive file detection
    sensitive = detect_sensitive_files(target)
    results["sensitive_files"] = sensitive

    # Async crawl for more pages
    discovered = asyncio.run(crawl(list(pages)))
    pages.update(discovered)

    # Deduplicate / normalize URLs
    pages = set(deduplicate(list(pages)))
    results["pages"] = list(pages)
    print(f"[*] Total pages discovered: {len(pages)}")

    # Load payloads
    payloads = generate_payload_set()
    print(f"[*] Payloads loaded: {len(payloads)}")

    # Test URL parameters
    for page in pages:
        limiter.wait()  # respect rate limiting
        params = brute_params(page)
        if params:
            results["params"].extend(params)
        for payload in payloads:
            test_url = f"{page}?q={payload}"
            try:
                import requests
                r = requests.get(test_url, timeout=6)
                if check_reflection(payload, r.text):
                    print(f"[REFLECTION FOUND] {test_url}")
                    results["reflections"].append(test_url)
            except:
                continue

    # Test forms (basic POST injection)
    from forms import test_forms
    for page in pages:
        limiter.wait()
        test_forms(page, payloads)

    # Extract JS parameters
    for page in list(pages):
        params = extract_js_params(page)
        if params:
            results["params"].extend(params)

    # Save reports
    save_report(results)
    generate_html(results)
    print("[*] Scan complete!")

if __name__ == "__main__":
    main()
