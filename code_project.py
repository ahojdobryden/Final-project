import pandas as pd #importing packages for further data processing
import json as js
import os
from rapidfuzz import fuzz, process
import unicodedata
import time  # Importing time for potential delays in processing

def normalize(text):
    """
    Normalize text by converting to lowercase, stripping whitespace, and removing accents.
    """
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def calculate_weighed_score(item1, item2):
    """
    Combine multiple scoring methods to determine the best match between two items.
    Uses token set ratio, partial ratio, and regular ratio from RapidFuzz.
    """
    score1 = fuzz.token_set_ratio(item1, item2)
    score2 = fuzz.partial_ratio(item1, item2)
    score3 = fuzz.ratio(item1, item2)
    score4 = fuzz.partial_token_set_ratio(item1, item2)
    return 0.4 * score1 + 0.2 * score2 + 0.2 * score3 + 0.2 * score4 # Adjust weights as needed

def tokenize_and_normalize(name):
    """ Tokenize and normalize a product name into a set of unique tokens.
    This helps in comparing items based on their names."""
    tokens = normalize(name).split()
    return set(tokens)


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
    #print(kosik_df.head())
    #print(rohlik_df.head())  # Display first few rows of Kosik data

print(f"Kosik data contains {len(data_kosik)} items.")
shopping_cart = [] #list to store items in the shopping cart
  


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

# Normalize Rohlik subcategories once
normalized_rohlik = {normalize(cat): cat for cat in rohlik_subcategories}
norm_rohlik_keys = list(normalized_rohlik.keys())  # Convert to list for easier iteration


        
match_rohlik_to_kosik = {}
for rohlik_cat in rohlik_subcategories:
    norm_rohlik = normalize(rohlik_cat)
    best_match = None
    best_score = 0
    for norm_kosik in norm_kosik_keys:
        score = calculate_weighed_score(norm_rohlik, norm_kosik)
        print(f"Comparing Rohlik '{norm_rohlik}' with Kosik '{norm_kosik}' - Score: {score}")
        # the matching is imperfect, so we need to filter out some categories
        if score > best_score and (norm_kosik != 'tvarohy' or norm_rohlik == 'smetany, slehacky, tvarohy - tvarohy') and (norm_kosik != 'mlecne vyrobky pro deti' or norm_rohlik == 'mlecne - pro deti' or norm_rohlik == 'syry - snacky'):
            best_score = score
            best_match = norm_kosik
        if best_match:
            best_kosik = normalized_kosik[best_match]
            match_rohlik_to_kosik[norm_rohlik] = best_kosik
        else:
            match_rohlik_to_kosik[norm_rohlik] = None

# Print the matched categories
#print(f"\nMatched categories from Rohlik to Kosik: {match_rohlik_to_kosik} , {len(match_rohlik_to_kosik)} matches found.")


shopping_cart = []
shopping_cart_kosik = []  # List to store items in the shopping cart for Kosik
shopping_cart_rohlik = []  # List to store items in the shopping cart for Rohlik

print("categories:", norm_rohlik_keys)

# Ask for valid category
while True:
    category_user = normalize(input("Please choose a category from the list above: "))
    if category_user in norm_rohlik_keys:
        break
    elif category_user == 'exit':
        print("Exiting the program.")
        exit()
    else:
        print("Category not found. Please try again.")

print(f"You selected the category: {category_user}")
print("Matching items from Rohlik to Kosik...")

# Ask for product
item_input = input('Please type a product you are looking for. If you want to see all items in the category, type "all". If you want to exit, type "exit": ')

if normalize(item_input) == 'exit':
    print("Exiting the program.")

elif normalize(item_input) == 'all':
    print(f"Here are all items in the category '{category_user}':")
    for item in data_rohlik:
        if normalize(item['subcategory_name']) == category_user:
            print(f"{item['name']} - {item['unit_price']} CZK")
    # Start asking for products
    while True:
        item_input = input('Please type the desired product (or "exit" to stop): ')
        if normalize(item_input) == 'exit':
            print("Exiting product selection.")
            break
        shopping_cart.append(normalize(item_input))

else:
    shopping_cart.append(normalize(item_input))
    while True:
        item_input = input('Please type the desired product (or "exit" to stop): ')
        if normalize(item_input) == 'exit':
            print("Exiting product selection.")
            break
        shopping_cart.append(normalize(item_input))
            
                
            
print(shopping_cart)

#for item in shopping_cart:



from rapidfuzz import fuzz, process

possible_items_kosik= []
cat_kosik = match_rohlik_to_kosik.get(category_user, None)
print(f"\n\n\nSelected Kosik category: {cat_kosik}")
# Collect normalized names from the selected Kosik category
for item in data_kosik:
    if item['subcategory'] == cat_kosik:
        norm_item = normalize(item['name'])
        possible_items_kosik.append((norm_item, item))  # Keep original item too

# Match each shopping_cart item
for it in shopping_cart:
    normalized_it = normalize(it) # Normalize the input item

    best_match = None #setting initial values for best match and score
    best_score = 0

    for norm_name, original_item in possible_items_kosik: # Extract just the list of normalized names
        score = calculate_weighed_score(normalized_it, norm_name) # calculate the score between the input and the item from Kosik
        if score > best_score and score >= 60: # score threshold passed and improved
            best_score = score #new best score
            best_match = original_item #new best match
    if best_match:
        shopping_cart_kosik.append(best_match) #at the end of the loop, append the best match to the shopping cart for Kosik
    
    
#Rohlik
possible_items_rohlik= []
for item in data_rohlik:
    if normalize(item['subcategory_name']) == category_user: #normalizing items from the desired category
        norm_item = normalize(item['name'])
        possible_items_rohlik.append((norm_item, item))  # storing normalized possible matches, keep original item too


# Match each shopping_cart item
for it in shopping_cart:
    normalized_it = normalize(it) # Normalize the input item
    best_match = None # setting initial values for best match and score
    best_score = 0
    
    # Extract just the list of normalized names
    for norm_name, original_item in possible_items_rohlik: #iterate through the possible items from Rohlik
        score = calculate_weighed_score(normalized_it, norm_name) # calculate the score between the input and the item from Rohlik
        if score > best_score and score >= 60:  # Adjust threshold as needed
            best_score = score #new best score
            best_match = original_item #new best match
    if best_match:  # Adjust threshold as needed
        shopping_cart_rohlik.append(best_match) # # at the end of the loop, append the best match to the shopping cart for Rohlik


#print(f'Shopping cart Kosik: {shopping_cart_kosik}')
#print(f'Shopping cart Rohlik: {shopping_cart_rohlik}')





# Ensure both carts are aligned
max_len = max(len(shopping_cart_kosik), len(shopping_cart_rohlik))
for i in range(max_len):
    kosik_item = shopping_cart_kosik[i] if i < len(shopping_cart_kosik) else None
    rohlik_item = shopping_cart_rohlik[i] if i < len(shopping_cart_rohlik) else None

    # Skip if either is missing
    if not kosik_item:
        print(f"\n⚠️ Kosik doesn't have a match for item index {i}.")
        continue
    elif not rohlik_item:
        print(f"\n⚠️ Rohlik doesn't have a match for item index {i}.")
        continue
    name_kosik = normalize(kosik_item['name'])
    name_rohlik = normalize(rohlik_item['name'])

    print(f"\nComparing: Kosik - '{kosik_item['name']}' vs Rohlik - '{rohlik_item['name']}'")

    try:
        kosik_price = float(kosik_item['price'].replace(',', '.').replace(' Kč', '').strip())
        rohlik_price = float(rohlik_item['unit_price'].replace(',', '.').replace(' Kč/kg', '').replace(' Kč/l', '').strip())

        if name_kosik == name_rohlik:
            print(f"🔍 Same name match.")
        else:
            print(f"🔁 Most similar match, score: ")

        if kosik_price < rohlik_price:
            print(f"✅ Kosik is cheaper: {kosik_price} CZK vs {rohlik_price} CZK")
        elif kosik_price > rohlik_price:
            print(f"✅ Rohlik is cheaper: {rohlik_price} CZK vs {kosik_price} CZK")
        else:
            print(f"💰 Same price: {kosik_price} CZK")

    except Exception as e:
        print(f"⚠️ Error comparing prices: {e}")