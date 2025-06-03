import pandas as pd
import json as js
import os
print(os.getcwd())
# Load data from JSON files
with open('data_kosik_subcats.json', 'r', encoding='utf-8') as file, open('rohlik_dairy_products_multi_cat.json', 'r', encoding='utf-8') as file2:
    data_kosik = js.load(file)
    data_rohlik = js.load(file2)


    print("Kosik data:", len(data_kosik))
    print("Rohlik data:", len(data_rohlik))

    set_kosik = set()
    for item in data_kosik:
        set_kosik.add(item['name'])

    print("Unique Kosik items:", len(set_kosik))