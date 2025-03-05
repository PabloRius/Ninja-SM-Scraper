"""Fetching logic"""

import random
import requests
from common.const import HEADERS, user_agents_list
from common.utils import debug

def fetch_one(url: str) -> str | None:
    """Fetch the webpage content."""

    current_headers = HEADERS.copy()
    current_headers["User-Agent"] = random.choice(user_agents_list)

    try:
        response = requests.get(url, headers=current_headers, timeout=10)

        while response.status_code == 403:
            current_headers["User-Agent"] = random.choice(user_agents_list)
            response = requests.get(url, headers=current_headers, timeout=10)

        if response.status_code == 200:
            return response.text

        debug(f"❌ Failed: {url} (Status {response.status_code})")
        return None

    except requests.RequestException as e:
        debug(f"❗ Request error fetching {url}: {e}")
        return None

def fetch_many(urls: list[str]) -> list[str | None]:
    """Fetch multiple URLs."""
    pages = []
    total = len(urls)

    for index, url in enumerate(urls, start=1):
        page = fetch_one(url)
        pages.append(page)

        debug(f"📊 Progress - {index}/{total} ({(index/total) * 100:.2f}%)")

    return pages
