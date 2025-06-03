import pandas as pd
import json as js

# Load data from JSON files
with open('data_kosik.json', 'r', encoding='utf-8') as file, open('data_rohlik.json', 'r', encoding='utf-8') as file2:
    data_kosik = js.load(file)
    #data_rohlik = js.load(file2)


    #print("Rohlik data:", rohlik.shape)
    print("Kosik data:", len(data_kosik))
    #print("Rohlik data:", len(data_rohlik))