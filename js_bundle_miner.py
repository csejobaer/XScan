# js_bundle_miner.py

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

pattern=r"https?:\/\/[a-zA-Z0-9\/\.\-\_\?\=\&]+"

def mine_js(url):

    endpoints=[]

    try:

        r=requests.get(url,timeout=8)

        soup=BeautifulSoup(r.text,"html.parser")

        scripts=soup.find_all("script",src=True)

        for s in scripts:

            js=urljoin(url,s["src"])

            try:

                code=requests.get(js,timeout=8).text

                matches=re.findall(pattern,code)

                endpoints.extend(matches)

            except:
                continue

    except:
        pass

    return list(set(endpoints))
