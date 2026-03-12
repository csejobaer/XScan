# async_scanner.py

import aiohttp
import asyncio

async def fetch(session,url):

    try:

        async with session.get(url) as r:

            return await r.text()

    except:
        return ""

async def scan_urls(urls):

    async with aiohttp.ClientSession() as session:

        tasks=[fetch(session,u) for u in urls]

        results=await asyncio.gather(*tasks)

        return results
