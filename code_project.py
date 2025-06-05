import pandas as pd #importing packages for further data processing
import json as js
import os
from rapidfuzz import fuzz, process
import unicodedata

def normalize(text): # Function to normalize text by converting to lowercase, stripping whitespace, and removing accents
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text


# Load data from JSON files with items from Kosik and Rohlik
with open('data_kosik_subcats.json', 'r', encoding='utf-8') as file, open('rohlik_dairy_products_multi_cat.json', 'r', encoding='utf-8') as file2:
    data_kosik_dupl = js.load(file)
    data_rohlik = js.load(file2)

    unique_kosik_dict = {}
    for item in data_kosik_dupl:
        unique_kosik_dict[item['name']] = item  # Later item with same name will overwrite earlier one

    # Convert back to a list
    data_kosik = list(unique_kosik_dict.values())
    kosik_df = pd.DataFrame(data_kosik, columns= ('name', 'price', 'subcategory', 'sub-subcategory_name') )  # Convert Kosik data to DataFrame for easier manipulation

    #pd.columns(data_rohlik) = c('name', 'price', 'subcategory_name', 'subcategory_id', 'subcategory_url')
    rohlik_df = pd.DataFrame(data_rohlik, columns= ('name', 'price', 'subcategory_name', 'subcategory_url'))  # Convert Rohlik data to DataFrame for easier manipulation
    print(kosik_df.head())
    print(rohlik_df.head())  # Display first few rows of Kosik data

    #print("Kosik data:", len(data_kosik_dupl))
    #print("Rohlik data:", len(data_rohlik))

    #since the Kosik data contains duplicates, we will use a set to store unique items



    #user_input = input('What do you want to order? (type "exit" to quit): ') #customer's input for ordering items
    shopping_cart = [] #list to store items in the shopping cart
    #while user_input.lower() != 'exit':
        #shopping_cart.append(user_input) #adding the item to the shopping cart
        #user_input = input('What else do you want to order? (type "exit" to quit): ') #asking for another item
    #print("Your shopping cart:", shopping_cart) #printing the shopping cart

    



    #not needed anymore, the matching was inefficient and not accurate enough
    #kosik_rohlik_categories_str = []
    #cnt = 1
    #while cnt < 10:
        #for item in rohlik_subcategories:
            #str1= item.lower()
            #for el in kosik_subcategories:
                #list_kosik = el.lower().split(" ")
                #for word in list_kosik:
                    #str2 = word.lower()
                    #print(str2)
                # Check if the string from Rohlik is a substring of the string from Kosik
                    #if str2 in str1 and len(str2) > 2:  # Ensure the string is longer than 2 characters
                        #kosik_rohlik_categories_str.append((item, el))
                        #print(f" {cnt} : {item} in Rohlik and {el} in Kosik")
                        #cnt += 1  # Increment the counter for each match
                        #break




    #i = 0
    #while i < 7:
        #print(kosik_df.iloc[i])  # Display first few rows of Kosik data
        #i += 1

    for item in data_kosik:  # creating a new subcategory for Kosik items that contain "protein" in their name
        item_name = normalize(item['name'])
        if "protein" in item_name:
            print(f"Found 'protein' in item: {item_name} - {item['subcategory']}")
            item['subcategory'] = 'Speciální - High protein'


    kosik_subcategories = {row['subcategory'] for row in data_kosik} # Extracting subcategories from Kosik data
    kosik_subcategories = set(kosik_subcategories)  # Convert to a set to ensure uniqueness


    rohlik_subcategories = {item['subcategory_name'] for item in data_rohlik} # Extracting subcategories from Kosik data
    rohlik_subcategories = set(rohlik_subcategories)  # Convert to a set to ensure uniqueness

    #print("\n\n\nUnique categories from Rohlik:", rohlik_subcategories)
    #print(len(rohlik_subcategories), "unique categories in Rohlik data.")

    # Normalize Kosik subcategories once
    normalized_kosik = {normalize(cat): cat for cat in kosik_subcategories}
    norm_kosik_keys = list(normalized_kosik.keys())

    # Now match every Rohlik category to the BEST Kosik match
    rohlik_to_kosik_match = {}
    THRESHOLD = 40  # Consider tuning this up/down depending on your needs

    counter = 1
    for rohlik_cat in rohlik_subcategories:
        norm_rohlik = normalize(rohlik_cat)

        match, score, _ = process.extractOne(
            norm_rohlik,
            norm_kosik_keys,
            scorer=fuzz.token_set_ratio
        )

        if score >= THRESHOLD:
            best_kosik = normalized_kosik[match]
            rohlik_to_kosik_match[rohlik_cat] = best_kosik
        else:
            rohlik_to_kosik_match[rohlik_cat] = (None, score)

    print(f"\n\n\nRohlik to Kosik category matches: {rohlik_to_kosik_match} \n\n\n")
    # SHOPPING PROCESS
    shopping_cart = []
    shopping_cart_kosik = []  # List to store items in the shopping cart for Kosik
    shopping_cart_rohlik = []  # List to store items in the shopping cart for Rohlik
    print("categories:", kosik_subcategories)
    category_user = normalize(input("Please choose a category from the list above: "))
    if category_user not in kosik_subcategories:
        category_user = normalize(input("Category not found. Please try again: "))
        

    else:
        print(f"You selected the category: {category_user}")
        print("Matching items from Rohlik to Kosik...")
        item_input = input('Please type a product you are looking for. If you want to see all items in the category, type "all". If you want to exit, type "exit": ')
        if normalize(item_input) == 'exit':
            print("Exiting the program.")
        elif normalize(item_input) == 'all':
            print(f"Here are all items in the category '{category_user}':")
            #for item in data_kosik:
                #if item['subcategory'] == category_user:
                    #print(f"{item['name']} - {item['price']} CZK")
            while normalize(item_input) != 'exit':
                item_input = input('Please type the desired product: ')
                if item_input != 'exit':
                    shopping_cart.append(normalize(item_input))
                
        else:
            shopping_cart.append(normalize(item_input))
            while normalize(item_input) != 'exit':
                item_input = input('Please type the desired product: ')
                if item_input != 'exit':
                    shopping_cart.append(normalize(item_input))
                else:
                    print("Exiting the program.")
                    break
                
print(shopping_cart)

#for item in shopping_cart:



from rapidfuzz import fuzz, process

possible_items_kosik= []

# Collect normalized names from the selected Kosik category
for item in data_kosik:
    if item['subcategory'] == category_user:
        norm_item = normalize(item['name'])
        possible_items_kosik.append((norm_item, item))  # Keep original item too

# Match each shopping_cart item
for it in shopping_cart:
    normalized_it = normalize(it)
    
    # Extract just the list of normalized names
    norm_names = [name for name, _ in possible_items_kosik]

    result = process.extractOne(normalized_it, norm_names, scorer=fuzz.token_set_ratio)

    if result:
        match, score, _ = result
        if score >= 80:
            # Find the corresponding original item
            for norm_name, original_item in possible_items_kosik:
                if norm_name == match:
                    print(f"Found match: {original_item['name']} - {original_item['price']} CZK")
                    shopping_cart_kosik.append(original_item)
                    break
        else:
            print(f"No good match found for '{it}' (score was {score}) in category {category_user}.")
    else:
        print(f"No match found for '{it}' in Kosik category {category_user}.")

#Rohlik
possible_items_rohlik= []

# Collect normalized names from the selected Kosik category
for item in data_rohlik:
    if item['subcategory_name'] == category_user:
        norm_item = normalize(item['name'])
        possible_items_rohlik.append((norm_item, item))  # Keep original item too

# Match each shopping_cart item
for it in shopping_cart:
    normalized_it = normalize(it)
    
    # Extract just the list of normalized names
    norm_names = [name for name, _ in possible_items_rohlik]

    result = process.extractOne(normalized_it, norm_names, scorer=fuzz.token_set_ratio)

    if result:
        match, score, _ = result
        if score >= 20:
            # Find the corresponding original item
            for norm_name, original_item in possible_items_rohlik:
                if norm_name == match:
                    print(f"Found match: {original_item['name']} - {original_item['price']} CZK")
                    shopping_cart_rohlik.append(original_item)
                    break
        else:
            print(f"No good match found for '{it}' (score was {score}) in category {category_user}.")
    else:
        print(f"No match found for '{it}' in Rohlik category {category_user}.")


    #if item['subcategory'] == category_user and normalize(item_input) in normalize(item['name']):
        #print(f"{item['name']} - {item['price']} CZK")
        #shopping_cart_kosik.append(item)




#print(f'Shopping cart Kosik: {shopping_cart_kosik}')
#print(f'Shopping cart Rohlik: {shopping_cart_rohlik}')


