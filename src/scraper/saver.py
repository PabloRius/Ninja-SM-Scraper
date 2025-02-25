"""Saving logic"""
import csv
from common.utils import debug

def save_to_csv(data:list, filename:str="products.csv")->None:
    """Save the data to a CSV file."""
    if not data:
        debug("No data to save.")
        return
    debug("Saving data to CSV")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price", "Relative Price", "Units", \
                         "Supermarket", "Link", "Image"])
        writer.writerows([product["name"], product["price"], \
                          product["price_relative"], product["units"], \
                            product["supermarket"], product["link"], product["img"]]
                         for product in data)

    debug(f"✅ Data saved to {filename}")
