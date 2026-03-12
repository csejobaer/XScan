# robots_parser.py

import requests
from urllib.parse import urljoin

def parse_robots(base_url):

    urls = []

    try:
        r = requests.get(urljoin(base_url,"/robots.txt"),timeout=5)

        if r.status_code == 200:

            for line in r.text.splitlines():

                if "Disallow:" in line or "Allow:" in line:

                    path = line.split(":")[1].strip()

                    if path:
                        urls.append(urljoin(base_url,path))

    except:
        pass

    return urls


def parse_sitemap(base_url):

    urls = []

    try:
        r = requests.get(urljoin(base_url,"/sitemap.xml"),timeout=5)

        if r.status_code == 200:

            for line in r.text.split():

                if "<loc>" in line:

                    url=line.replace("<loc>","").replace("</loc>","")
                    urls.append(url)

    except:
        pass

    return urls
