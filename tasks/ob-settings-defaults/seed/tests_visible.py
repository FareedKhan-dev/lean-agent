import json
import os

from settings import load_settings

with open("visible_settings.json", "w", encoding="utf-8") as f:
    json.dump({"theme": "dark"}, f)
s = load_settings("visible_settings.json")
assert s["theme"] == "dark" and s["page_size"] == 20, s
os.remove("visible_settings.json")
print("ok")
