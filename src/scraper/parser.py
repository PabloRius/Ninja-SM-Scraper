"""Parsing logic"""
from typing import List, Union, Callable

def parse_many(pages:list[str|None], parse_one:Callable[[Union[str, None]], List])->List:
    """Extract product details from multiple HTML pages"""
    products = []
    for page in pages:
        products.extend(parse_one(page))
    return products
