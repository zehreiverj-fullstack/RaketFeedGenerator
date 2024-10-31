from dotenv import load_dotenv
from unidecode import unidecode
import os
import re

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    raise Exception("FRONTEND_URL not set")


def parse(products: dict) -> list:
    parsed_products = []

    for product in products.values():

        raketeer = product["attributes"]["raketeer"]["data"]
        media = product["attributes"]["media"]["data"]
        variants = product["attributes"]["variants"]["data"]

        slug = product["attributes"]["slug"]
        default_variant = list(
            filter(lambda variant: variant["attributes"]["isDefault"], variants)
        )[0]

        id = product["id"]
        name = unidecode(product["attributes"]["name"])
        description = re.sub(
            r"free shipping",
            "no cost delivery",
            product["attributes"]["description"],
            flags=re.IGNORECASE | re.DOTALL,
        )
        price = default_variant["attributes"]["price"]
        url = f"{FRONTEND_URL}{raketeer['attributes']['username']}/products/{slug}"
        image_url = media[0]["attributes"]["url"]
        manufacturer_part_number = id + price

        parsed_products.append(
            {
                "Unique ID": id,
                "Title": name,
                "ProductName": name,
                "Name": name,
                "Description": description,
                "Price": price,
                "Merchant Category": "digital",
                "URL": url,
                "Image URL": image_url,
                "Manufacturer": "raket.ph",
                "Manufacturer Part Number": manufacturer_part_number,
                "Brand": "raket.ph",
                "Condition": "new",
                "Quantity": 1,
                "WarehouseId1": manufacturer_part_number,
                "AvailableStock1": 1,
            }
        )

    return parsed_products
