# js_param_extractor.py

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

param_pattern=r"[?&]([a-zA-Z0-9_\-]+)="

def extract_js_params(url):

    params=set()

    try:

        r=requests.get(url,timeout=8)

        soup=BeautifulSoup(r.text,"html.parser")

        scripts=soup.find_all("script",src=True)

        for s in scripts:

            js=urljoin(url,s["src"])

            try:

                code=requests.get(js,timeout=8).text

                matches=re.findall(param_pattern,code)

                params.update(matches)

            except:
                continue

    except:
        pass

    return list(params)
