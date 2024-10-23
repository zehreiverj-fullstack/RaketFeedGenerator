from dotenv import load_dotenv
import os
import requests

load_dotenv()

GODATAFEED_URL = os.getenv("GODATAFEED_URL")


def sync(file_path: str) -> None:
    with open(file_path, "rb") as csv_file:
        files = {
            "file": (
                file_path,
                csv_file,
                "text/csv",
            )
        }
        requests.put(GODATAFEED_URL, files=files)
