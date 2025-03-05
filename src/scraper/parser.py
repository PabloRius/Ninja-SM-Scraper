"""Parsing logic"""

from typing import List, Union, Callable
from common.utils import debug

def parse_many(pages: list[Union[str, None]], parse_one: Callable[[Union[str, None]], List]) -> List:
    """Extract product details from multiple HTML pages."""

    total = len(pages)
    products = []

    for index, page in enumerate(pages, start=1):
        debug(f"📄 Parsing page {index}/{total} ({(index/total) * 100:.2f}%)")
        parsed_products = parse_one(page) if page else []
        products.extend(parsed_products)

    return products
