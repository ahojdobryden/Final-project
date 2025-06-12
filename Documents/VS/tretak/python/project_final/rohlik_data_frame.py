import os
import pandas as pd
import json
# %%
# 1. Get the absolute path to the directory where the currently running script is located.
script_directory = os.path.dirname(os.path.abspath(__file__))

print(f"The script is located in: {script_directory}")
print(f"The current working directory (where Python started) is: {os.getcwd()}")

# 2. Construct the full path to your data file using the script's directory
json_filename = 'rohlik_dairy_products_multi_cat.json'
json_file_full_path = os.path.join(script_directory, json_filename) # <--- IMPORTANT CHANGE HERE

print(f"Looking for JSON file at: {json_file_full_path}") # Debug print

try:
    # Use the constructed 'json_file_full_path' to open your file
    with open(json_file_full_path, 'r', encoding='utf-8') as f: # <--- USE THE FULL PATH
        data = json.load(f)
    
    print(f"Successfully loaded '{json_filename}'!")

    if isinstance(data, list) and data:
        df = pd.DataFrame([{
            'name': item.get('name'),
            'price': item.get('price'),
            'unit price': item.get('unit_price'),
            'category': item.get('subcategory_name')
        } for item in data])
        print("\nDataFrame created successfully:")
        print(df.head())
        print(f"\nTotal products: {len(df)}")
    else:
        print("JSON data is not in the expected list format or is empty.")

except FileNotFoundError:
    print(f"ERROR: FileNotFoundError! '{json_filename}' was not found at the constructed path '{json_file_full_path}'.")
    print(f"Please ensure the file exists in the script's directory: '{script_directory}'")
    # List files in the script directory for easier debugging
    try:
        print(f"Files and folders found in script directory '{script_directory}':")
        for item_in_dir in os.listdir(script_directory):
            print(f"  - {item_in_dir}")
    except Exception as e_listdir:
        print(f"    Could not list directory contents: {e_listdir}")
except json.JSONDecodeError:
    print(f"ERROR: Could not decode JSON. The file '{json_filename}' might be corrupted or not valid JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Counting number of products in each category
category_counts = df['category'].value_counts()
print("\nNumber of products in each category:")
print(category_counts)

#Counting the number of duplicates in the 'name' column
duplicates_count = df['name'].duplicated().sum()
print(f"\nTotal number of duplicate product names: {duplicates_count}")
