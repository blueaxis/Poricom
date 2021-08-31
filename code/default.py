from json import load

cfg = {}

with open("default.json") as f:
    cfg = load(f)