# js_endpoint_extractor.py

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

endpoint_pattern = r"['\"](\/[a-zA-Z0-9_\-\/]+)['\"]"

def extract_js_endpoints(url):

    endpoints = []

    try:

        r = requests.get(url,timeout=5)

        soup = BeautifulSoup(r.text,"html.parser")

        scripts = soup.find_all("script",src=True)

        for s in scripts:

            js_url = urljoin(url,s["src"])

            try:

                js = requests.get(js_url,timeout=5).text

                matches = re.findall(endpoint_pattern,js)

                for m in matches:

                    endpoints.append(urljoin(url,m))

            except:
                continue

    except:
        pass

    return list(set(endpoints))
