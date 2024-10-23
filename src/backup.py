import json


def backup(data, filePath: str) -> None:

    with open(filePath, "w") as json_file:
        json.dump(data, json_file)

    print(f"Backup done!: {filePath}")
