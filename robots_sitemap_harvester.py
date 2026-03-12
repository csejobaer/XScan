# robots_sitemap_harvester.py

import requests
from urllib.parse import urljoin
import re

def harvest_robots(base_url):

    urls=[]

    try:
        r=requests.get(urljoin(base_url,"/robots.txt"),timeout=8)

        if r.status_code==200:

            for line in r.text.splitlines():

                if "Allow:" in line or "Disallow:" in line:

                    path=line.split(":")[1].strip()

                    if path:
                        urls.append(urljoin(base_url,path))

    except:
        pass

    return urls


def harvest_sitemap(base_url):

    urls=[]

    try:
        r=requests.get(urljoin(base_url,"/sitemap.xml"),timeout=8)

        if r.status_code==200:

            matches=re.findall(r"<loc>(.*?)</loc>",r.text)

            urls.extend(matches)

    except:
        pass

    return urls
