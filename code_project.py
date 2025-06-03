import pandas as pd #importing packages for further data processing
import json as js
import os

# Load data from JSON files with items from Kosik and Rohlik
with open('data_kosik_subcats.json', 'r', encoding='utf-8') as file, open('rohlik_dairy_products_multi_cat.json', 'r', encoding='utf-8') as file2:
    data_kosik_dupl = js.load(file)
    data_rohlik = js.load(file2)


    #print("Kosik data:", len(data_kosik_dupl))
    #print("Rohlik data:", len(data_rohlik))

    data_kosik = {} #since the Kosik data contains duplicates, we will use a set to store unique items
    #for item in data_kosik_dupl:
        #data_kosik.add(item['name'])
    # Remove duplicates based on 'name'
    data_kosik = {}
    for item in data_kosik_dupl:
        data_kosik[item['name']] = item  # If name is the same, later item overwrites earlier

    user_input = input('What do you want to order? (type "exit" to quit): ') #customer's input for ordering items
    shopping_cart = [] #list to store items in the shopping cart
    while user_input.lower() != 'exit':
        shopping_cart.append(user_input) #adding the item to the shopping cart
        user_input = input('What else do you want to order? (type "exit" to quit): ') #asking for another item
    print("Your shopping cart:", shopping_cart) #printing the shopping cart

    
    kosik_subcategories = {item['subcategory'] for item in data_kosik.values()} # Extracting subcategories from Kosik data
    #kosik_subcategories = set(kosik_subcategories)  # Convert to a set to ensure uniqueness
    print("Unique categories from Kosik:", kosik_subcategories)

    rohlik_subcategories = {item['subcategory_name'] for item in data_rohlik} # Extracting subcategories from Kosik data
    #kosik_subcategories = set(kosik_subcategories)  # Convert to a set to ensure uniqueness
    print("Unique categories from Rohlik:", rohlik_subcategories)


    print("Unique Kosik items:", len(data_kosik))