import json
import os
from pprint import pprint as pp


def write_json(file_name, data):
    with open(file_name + ".json", "w") as f:
        json.dump(data, f, indent=4)


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def create_json(word_length):
    write_json(str(word_length), get_all_files("img", str(word_length)))


def get_all_files(dir, word_length):
    file_names = []
    for _, _, files in os.walk(os.path.join(dir, word_length)):
        for f in files:
            file_names.append(f.rsplit(".", 1)[0])
    return file_names


create_json(3)
