# async_crawler.py

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# suppress XML warning when parsing XML like sitemap.xml
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


async def fetch(session, url):
    try:
        async with session.get(url) as r:
            return await r.text()
    except:
        return ""


async def crawl(urls):

    discovered = set()

    async with aiohttp.ClientSession() as session:

        tasks = [fetch(session, u) for u in urls]

        pages = await asyncio.gather(*tasks)

        for html, base in zip(pages, urls):

            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")

            for link in soup.find_all("a", href=True):

                full_url = urljoin(base, link["href"])

                discovered.add(full_url)

    return list(discovered)
