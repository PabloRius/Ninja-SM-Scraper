"""Extract Tesco groceries."""
# pylint: disable=C0301

from typing import List
import re
from bs4 import BeautifulSoup

from common.utils import debug

from scraper.fetch import fetch_many, fetch_one
from scraper.parser import parse_many


def extract_tesco() -> list:
    """Extract Tesco groceries."""
    debug("🔄 Extracting Tesco items...")
    main_urls = [
        "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/marketplace/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/bakery/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/frozen-food/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/treats-and-snacks/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/drinks/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/baby-and-toddler/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/pets/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/household/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/home-and-ents/all?sortBy=relevance&count=40",
        "https://www.tesco.com/groceries/en-GB/shop/easter/all?sortBy=relevance&count=40"
    ]

    urls = []
    debug("🔄 Generating Tesco urls...")
    for index, url in enumerate(main_urls, start=1):
        n_pages = extract_n_pages(fetch_one(url))
        urls.extend([f"{url}&page={i}" for i in range(1, n_pages + 1)])
        debug(f"📄 Pages found: {len(urls)}, {index}/{len(main_urls)} ({(index/len(main_urls)) * 100:.2f}%) urls analysed")

    debug(f"🔄 Fetching {len(urls)} urls...")
    pages = fetch_many(urls)

    debug(f"🔄 Parsing {len(pages)} pages...")
    products = tesco_ize(parse_many(pages, parse_one))

    debug(f"✅ Extraction complete: {len(products)} products found.")
    return products

def tesco_ize(products: list) -> list:
    """Convert the products to Tesco format."""
    debug(f"🔄 Converting {len(products)} products to Tesco format...")
    standardized_products = []

    total = len(products)
    for index, product in enumerate(products, start=1):
        name = clean_name(product["name"])
        price = clean_price(product["price"])
        relative_price, units = normalise_relative_price(product["price_relative"])

        standardized_products.append({
            "name": name, "price": price, 
            "price_relative": relative_price, "units": units,
            "supermarket": "Tesco", "link": product["link"], "img": product["img"]
        }) 

    debug("✅ Conversion to Tesco format complete.")
    return standardized_products

def parse_one(html: str | None) -> List:
    """Extract product details from the Tesco HTML content"""
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    products = []

    items = soup.select("._ecrj")
    total = len(items)
    debug(f"🔄 Adding {total} products.")

    for index, product in enumerate(items, start=1):
        try:
            title = product.select_one("h3")
            name = title.get_text(strip=True).encode("latin1").decode("utf-8")
            link_tag = title.select_one("a")
            link = "https://www.tesco.com" + link_tag["href"] if link_tag else ""
            price = product.select_one(".styled__PriceText-sc-v0qv7n-1").get_text(strip=True)\
                .encode("latin1").decode("utf-8")
            price_relative = product.select_one(".ddsweb-price__subtext").get_text(strip=True)\
                .encode("latin1").decode("utf-8")
            image_tag = product.select_one("div.bixZuE img")
            image_url = image_tag["src"] if image_tag else ""

            products.append({
                "name": name, "price": price, "price_relative": price_relative,
                "link": link, "img": image_url
            })

        except AttributeError:
            continue

    return products

def extract_n_pages(html):
    """Extract the number of pages from the Tesco HTML."""
    soup = BeautifulSoup(html, "html.parser")
    pagination_div = soup.find("div", class_="ddsweb-pagination__navigation")
    if not pagination_div:
        return 1

    pages = pagination_div.find_all("li")
    if len(pages) > 1:
        try:
            page_count = int(pages[-2].text.strip())
            return page_count
        except ValueError:
            return 1

    return 1

def clean_name(name: str) -> str:
    """Cleans the product name."""
    return re.sub(r"\"", "", name.strip())

def clean_price(price: str) -> float:
    """Remove currency symbol and convert price to float."""
    price = price.replace("£", "").strip()
    try:
        return round(float(price), 2)
    except ValueError:
        return 0.0

def normalise_relative_price(relative_price: str) -> tuple[float, str]:
    """Convert price per unit to a standard format (per liter or per kilo)."""
    match = re.search(r"([\d.]+)\s*/\s*(litre|100ml|100g|kg|each)", relative_price, re.IGNORECASE)
    if not match:
        return 0.0, ""

    value, unit = float(match.group(1)), match.group(2).lower()
    conversion = {"100ml": (10, "per_litre"), "100g": (10, "per_kilo"),
                  "litre": (1, "per_litre"), "kg": (1, "per_kilo"), "each": (1, "per_unit")}
    
    factor, unit_label = conversion.get(unit, (1, ""))
    return round(value * factor, 4), unit_label
