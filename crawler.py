# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def discover_links(url, visited):
    if url in visited:
        return []

    visited.add(url)
    links = []

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if urlparse(url).netloc in urlparse(link).netloc:
                links.append(link)
    except:
        pass

    return links
