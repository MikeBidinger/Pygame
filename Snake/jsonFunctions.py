import json


def write_json(file_path: str, data):
    f = open(file_path, 'w')
    js_str = json.dumps(data, indent=4)
    f.write(js_str)
    f.close()


def read_json(file_path: str):
    f = open(file_path, 'r')
    js_str = f.read()
    data = json.loads(js_str)
    f.close()
    return data
