# spa_route_extractor.py

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

API_PATTERN = r'/api/[a-zA-Z0-9_\-/]+'

def extract_spa_routes(url):

    routes = set()

    try:
        r = requests.get(url, timeout=8)

        soup = BeautifulSoup(r.text, "html.parser")

        scripts = soup.find_all("script", src=True)

        for s in scripts:

            js = urljoin(url, s["src"])

            try:

                code = requests.get(js, timeout=8).text

                matches = re.findall(API_PATTERN, code)

                for m in matches:
                    routes.add(urljoin(url, m))

            except:
                continue

    except:
        pass

    return list(routes)
