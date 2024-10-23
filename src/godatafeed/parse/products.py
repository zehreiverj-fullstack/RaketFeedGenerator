from dotenv import load_dotenv
import os
import re

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")


def parse(products: dict) -> list:
    parsed_products = []

    for product in products.values():

        raketeer = product["attributes"]["raketeer"]["data"]
        media = product["attributes"]["media"]["data"]
        variants = product["attributes"]["variants"]["data"]

        if not raketeer or not media or not variants:
            continue
        if len(media) == 0 or len(variants) == 0:
            continue

        slug = product["attributes"]["slug"]
        default_variant = list(
            filter(lambda variant: variant["attributes"]["isDefault"], variants)
        )[0]

        id = product["id"]
        name = product["attributes"]["name"]
        description = re.sub(r'free shipping', 'no cost delivery', product["attributes"]["description"], flags=re.IGNORECASE|re.DOTALL)
        price = default_variant["attributes"]["price"]
        merchant_category = "digital"
        url = f"{FRONTEND_URL}{raketeer['attributes']['username']}/products/{slug}"
        image_url = media[0]["attributes"]["url"]
        manufacturer = "raket.ph"
        manufacturer_part_number = id + price
        brand = "raket.ph"
        condition = "new"
        availability = "in stock"
        
        parsed_products.append(
            {
                "Unique ID": id,
                "Title": name,
                "Name": name,
                "Description": description,
                "Price": price,
                "Merchant Category": merchant_category,
                "URL": url,
                "Image URL": image_url,
                "Manufacturer": manufacturer,
                "Manufacturer Part Number": manufacturer_part_number,
                "Brand": brand,
                "Condition": condition,
                "Availability": availability
            }
        )

    return parsed_products