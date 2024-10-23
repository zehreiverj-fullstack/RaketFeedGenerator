from dotenv import load_dotenv
import os
import requests

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
STRAPI_FEED_TOKEN = os.getenv("STRAPI_FEED_TOKEN")
LIMIT = int(os.getenv("LIMIT"))


def fetch() -> dict:
    accumulated = {}
    page = 1
    pageSize= 100

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
            print('No more products')
            break
        
        for product in products:
            accumulated[product["id"]] = product
        
        if len(accumulated) + pageSize >= LIMIT:
            pageSize = LIMIT - len(accumulated)
            
        if len(accumulated) == LIMIT:
            print(f"Limit reached, only {LIMIT} products found")
            break
        

        print(f"Total products found: {len(accumulated)}")

        page += 1

    return accumulated
