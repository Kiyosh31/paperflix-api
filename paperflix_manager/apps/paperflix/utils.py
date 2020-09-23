
import json

def read_json(fname):
    try:
        file_ = open(fname, 'r', encoding='utf-8')
        load  = json.load(file_)
        return load
    except FileNotFoundError:
        return None
