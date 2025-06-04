import pandas as pd #importing packages for further data processing
import json as js
import os
from rapidfuzz import fuzz


# Load data from JSON files with items from Kosik and Rohlik
with open('data_kosik_subcats.json', 'r', encoding='utf-8') as file, open('rohlik_dairy_products_multi_cat.json', 'r', encoding='utf-8') as file2:
    data_kosik_dupl = js.load(file)
    data_rohlik = js.load(file2)

    unique_kosik_dict = {}
    for item in data_kosik_dupl:
        unique_kosik_dict[item['name']] = item  # Later item with same name will overwrite earlier one

    # Convert back to a list
    data_kosik = list(unique_kosik_dict.values())

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



from rapidfuzz import fuzz, process
import unicodedata

def normalize(text):
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

for item in data_kosik:
    if "protein" in item['name'].lower():
        print(f"Found 'protein' in item: {item['name']} - {item['subcategory']}")
        item['subcategory'] = 'Speciální - High protein'

kosik_subcategories = {item['subcategory'] for item in data_kosik} # Extracting subcategories from Kosik data
kosik_subcategories = set(kosik_subcategories)  # Convert to a set to ensure uniqueness
print("Unique categories from Kosik:", kosik_subcategories)

rohlik_subcategories = {item['subcategory_name'] for item in data_rohlik} # Extracting subcategories from Kosik data
rohlik_subcategories = set(rohlik_subcategories)  # Convert to a set to ensure uniqueness

print("\n\n\nUnique categories from Rohlik:", rohlik_subcategories)
print(len(rohlik_subcategories), "unique categories in Rohlik data.")

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
        rohlik_to_kosik_match[rohlik_cat] = (best_kosik, score)
    else:
        rohlik_to_kosik_match[rohlik_cat] = (None, score)

# Print the final mapping
for i, (rohlik_cat, (kosik_cat, score)) in enumerate(rohlik_to_kosik_match.items(), 1):
    if kosik_cat:
        print(f"{counter} : {i}. Rohlik: '{rohlik_cat}' → Kosik: '{kosik_cat}' (Score: {score})")
        counter += 1
    else:
        print(f" Rohlik: '{rohlik_cat}' → ❌ No good match (Score: {score})")


        # Add the Kosik subcategory to the mapping

# Save the mapping to a JSON file

