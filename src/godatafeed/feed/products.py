from src.godatafeed.fetch.products import fetch
from src.godatafeed.parse.products import parse
from src.godatafeed.sync import sync
from src.generate import generate
from src.backup import backup
from datetime import date
import json
import os

def feed() -> None:
    name = "products"
    now = date.today()

    directory = "data"
    file_name = f"{name}-{now}"
    csv_file_path = f"{directory}/gdf-{file_name}.csv"

    backup_directory = f"{directory}/backups"
    backup_file_path = f"{backup_directory}/{file_name}.json"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(backup_directory)

    if os.path.exists(csv_file_path):
        print("CSV exists!")
        print("Syncing to GoDataFeed...")
        sync(csv_file_path)
        return
    
    products = {}
    if os.path.exists(backup_file_path): 
        print("Backup exists!")
        print("Reading backup...")
        with open(backup_file_path) as json_file:
            products:dict = json.load(json_file)
    else:
        print("Fetching products...")
        products = fetch()

        print("Writing backup...")
        backup(products, backup_file_path)

    print("Parsing...")
    products = parse(products)

    print("Generating CSV...")
    generate(products, csv_file_path)

    print("Syncing to GoDataFeed...")
    sync(csv_file_path)

    print("Done!")
