# url_normalizer.py

from urllib.parse import urlparse, parse_qs, urlunparse

def normalize(url):

    parsed = urlparse(url)

    params = parse_qs(parsed.query)

    # normalize parameters
    clean_query = "&".join([f"{p}=" for p in params])

    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",
        clean_query,
        ""
    ))

    return normalized


def deduplicate(urls):

    normalized = set()

    for u in urls:
        normalized.add(normalize(u))

    return list(normalized)
