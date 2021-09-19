from json import load

cfg = {}

# Convert default.json to a dictionary instead

with open("default.json") as f:
    cfg = load(f)