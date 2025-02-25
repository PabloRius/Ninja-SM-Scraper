"""Fetching logic"""

import random
import requests
from common.const import HEADERS, user_agents_list
from common.utils import debug

def fetch_one(url:str)->str|None:
    """Fetch the webpage content."""
    current_headers = HEADERS
    current_headers["User-Agent"] = user_agents_list[random.randint(0, len(user_agents_list) - 1)]
    response = requests.get(url, headers=HEADERS, timeout=500)
    while response.status_code == 403:
        print("403 Forbidden")
        current_headers["User-Agent"] = \
            user_agents_list[random.randint(0, len(user_agents_list) - 1)]
        response = requests.get(url, headers=HEADERS, timeout=500)
    if response.status_code == 200:
        print("200 OK")
        return response.text
    debug(f"Failed to fetch {url} (Status Code: {response.status_code}) \
          (user-agent: {current_headers['User-Agent']})")
    return None

def fetch_many(urls: list[str]) -> list[str | None]:
    """Fetch each URL and display progress."""
    pages = []
    total = len(urls)

    for i, url in enumerate(urls, start=1):
        page = fetch_one(url)
        pages.append(page)
        print(f"Fetched {i}/{total} URLs")

    return pages
