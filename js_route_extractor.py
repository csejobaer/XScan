# js_route_extractor.py

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

endpoint_regex = r'["\'](\/[a-zA-Z0-9_\-\/]{3,})["\']'

def extract_routes(url):

    routes = []

    try:

        r = requests.get(url,timeout=8)

        soup = BeautifulSoup(r.text,"html.parser")

        scripts = soup.find_all("script",src=True)

        for script in scripts:

            js_url = urljoin(url,script["src"])

            try:

                js = requests.get(js_url,timeout=8).text

                matches = re.findall(endpoint_regex,js)

                for m in matches:
                    routes.append(urljoin(url,m))

            except:
                continue

    except:
        pass

    return list(set(routes))
