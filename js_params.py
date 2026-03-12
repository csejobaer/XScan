# js_params.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

param_pattern = r"[?&]([a-zA-Z0-9_]+)="

def extract_js_params(url):
    params = set()
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text,"html.parser")
        scripts = soup.find_all("script", src=True)
        for s in scripts:
            js_url = urljoin(url, s["src"])
            try:
                js = requests.get(js_url, timeout=5).text
                matches = re.findall(param_pattern, js)
                for m in matches:
                    params.add(m)
            except:
                continue
    except:
        pass
    return list(params)
