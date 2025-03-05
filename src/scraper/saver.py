"""Saving logic"""

import os
import csv
import datetime
from supabase import create_client
from supabase.client import PostgrestAPIError
from dotenv import load_dotenv
from common.utils import debug

load_dotenv()

def save_to_csv(data: list, filename: str = "products.csv") -> None:
    """Save the data to a CSV file."""
    if not data:
        debug(f"📁 No data to save in {filename}.")
        return

    debug(f"💾 Saving {len(data)} products to {filename}...")

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        headers = ["Name", "Price", "Relative Price", "Units", "Supermarket", "Link", "Image"]
        if any("error" in product for product in data):
            headers.append("Error")

        writer.writerow(headers)

        for product in data:
            row = [
                product["name"],
                product["price"],
                product["price_relative"],
                product["units"],
                product["supermarket"],
                product["link"],
                product["img"]
            ]
            if "error" in product:
                row.append(product["error"])

            writer.writerow(row)

    debug(f"✅ Data saved successfully to {filename}.")  

def save_to_cloud(data: list) -> None:
    """Save the data to the Cloud database."""
    if not data:
        debug("📡 No data to upload.")
        return

    debug(f"📡 Uploading {len(data)} products to cloud database...")

    total = len(data)
    remaining = data.copy()
    uploaded = []
    failed = []
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        supabase = create_client(supabase_url, supabase_key)


        for index, product in enumerate(data, start=1):
            debug(f"📊 Progress - {index}/{total} ({(index/total) * 100:.2f}%)")

            try:
                product["last_edited"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                supabase.table("Products").upsert(product).execute()
                uploaded.append(product)
                remaining.pop(0)

            except PostgrestAPIError as e:
                product["error"] = str(e)
                failed.append(product)
                debug(f"⚠️ Error inserting product '{product['name']}' from {product['supermarket']} - {e}")


    except Exception as e:
        debug(f"❌ Connection with database failed: ({e.__class__}): {e}")

    finally:
        remaining.extend(failed)
        debug(f"✅ Upload completed: {len(uploaded)} successful, {len(remaining)} remaining.")

        save_to_csv(remaining, "output/temp/failed_products.csv")
        save_to_cloud(remaining)
