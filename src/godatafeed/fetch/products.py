from dotenv import load_dotenv
import os
import requests

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    raise Exception("BACKEND_URL not set")

STRAPI_FEED_TOKEN = os.getenv("STRAPI_FEED_TOKEN")
if not STRAPI_FEED_TOKEN:
    raise Exception("STRAPI_FEED_TOKEN not set")

LIMIT = int(os.getenv("LIMIT") or 5000)


def fetch() -> dict:
    accumulated = {}
    page = 1
    pageSize = 100

    while True:
        print(f"Fetching page {page}...")

        url = f"{BACKEND_URL}/api/products?sort[0]=sold:desc&filters[$and][0][type][$eq]=digital&filters[$and][1][sold][$gt]=0&populate[raketeer]=true&populate[media]=true&populate[variants]=true&pagination[pageSize]={pageSize}&pagination[page]={page}&locale[0]=en&status=published"

        response = requests.get(
            url, headers={"Authorization": f"Bearer {STRAPI_FEED_TOKEN}"}
        )
        data = response.json()
        products = data["data"]

        print(f"Products found: {len(products)}")

        if len(products) == 0:
            print("No more products")
            break

        for product in products:
            if len(accumulated) >= LIMIT:
                break

            raketeer = product["attributes"]["raketeer"]["data"]
            media = product["attributes"]["media"]["data"]
            variants = product["attributes"]["variants"]["data"]

            if not raketeer or not media or not variants:
                continue
            if len(media) == 0 or len(variants) == 0:
                continue

            accumulated[product["id"]] = product

        if len(accumulated) + pageSize >= LIMIT:
            pageLimit = LIMIT - len(accumulated)
            pageSize = 10 if pageLimit < 10 else pageLimit

        if len(accumulated) == LIMIT:
            print(f"Limit reached, only {LIMIT} products accumulated")
            break

        print(f"Total products accumulated: {len(accumulated)}")

        page += 1

    return accumulated
