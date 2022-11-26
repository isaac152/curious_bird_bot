import json

from constants import FILE_PATH


def load_file() -> dict:
    with open(FILE_PATH, "r") as json_data:
        dictionary = json_data.read()
    return json.loads(dictionary)
