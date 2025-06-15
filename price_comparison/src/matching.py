import json as js
import os
from rapidfuzz import fuzz, process
import unicodedata
import requests

# Get absolute path to current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct path to data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this .py file
DATA_PATH_kosik = os.path.join(BASE_DIR, '..', 'data', 'data_kosik_subcats.json')
DATA_PATH_rohlik = os.path.join(BASE_DIR, '..', 'data', 'rohlik_dairy_products_multi_cat.json')
class GroceryComparator:
    def __init__(self):
        # Load data files
        with open(DATA_PATH_kosik, 'r', encoding='utf-8') as file, \
             open(DATA_PATH_rohlik, 'r', encoding='utf-8') as file2:
            self.data_kosik = js.load(file)
            self.data_rohlik = js.load(file2)

        self._process_data()
        self._match_categories()
        self._process_protein_items()

    @staticmethod
    def normalize(text):
        """Normalize text by lowercasing, stripping whitespace, and removing accents"""
        text = text.lower().strip()
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    @staticmethod
    def calculate_weighed_score(item1, item2):
        """Calculate a weighted score between two items using fuzzy matching"""
        score1 = fuzz.token_set_ratio(item1, item2) #how strings overlap with each other
        score2 = fuzz.partial_ratio(item1, item2) #compares the longest common subsequence
        score3 = fuzz.ratio(item1, item2) #how similar the strings are character by character
        score4 = fuzz.partial_token_set_ratio(item1, item2) #finds the best matching subsequence of tokens
        return 0.4 * score1 + 0.2 * score2 + 0.2 * score3 + 0.2 * score4 

    def _process_data(self):
        """Process and clean data from Košík, leaving only unique items"""
        unique_kosik = {}
        for item in self.data_kosik:
            unique_kosik[item['name']] = item
        self.data_kosik = list(unique_kosik.values())

    def _match_categories(self):
        """Match Rohlik subcategories to Kosik subcategories"""
        kosik_subs = {item['subcategory'] for item in self.data_kosik} 
        rohlik_subs = {item['subcategory_name'] for item in self.data_rohlik}
        self.match_rohlik_to_kosik = {}
        for r_sub in rohlik_subs:
            norm_r = self.normalize(r_sub)
            best_score = 0
            best_match = None
            for k_sub in kosik_subs:
                norm_k = self.normalize(k_sub)
                score = self.calculate_weighed_score(norm_r, norm_k)
                if score > best_score and self._valid_match(norm_r, norm_k):
                    best_score = score
                    best_match = k_sub
            self.match_rohlik_to_kosik[r_sub] = best_match

    def _valid_match(self, norm_r, norm_k):
        """Check if the match between Rohlik and Kosik is valid based on specific rules"""
        return not (
            (norm_k == 'tvarohy' and norm_r != 'smetany, slehacky, tvarohy - tvarohy') or #this is a special case, these two categories were matched incorrectly
            (norm_k == 'mlecne vyrobky pro deti' and norm_r not in ['mlecne - pro deti', 'syry - snacky'])
        )

    def _process_protein_items(self):
        """Special handling for protein-enriched items"""
        for item in self.data_kosik:
            if "protein" in self.normalize(item['name']): #there is no "high protein" category in Kosik, so we need to create a special one by adding products that contain "protein" in their name
                item['subcategory'] = 'Speciální - High protein'

    def find_products(self, selected_category):
        """Find products in Rohlik and Kosik based on selected category"""
        kosik_category = self.match_rohlik_to_kosik.get(selected_category)
        kosik_products = [p for p in self.data_kosik if p['subcategory'] == kosik_category] if kosik_category else []
        rohlik_products = [p for p in self.data_rohlik if p['subcategory_name'] == selected_category]

        matched = []
        for rp in rohlik_products:
            r_price, r_unit = self.parse_rohlik_unit(rp)
            best_match = None
            best_score = 0
            for kp in kosik_products:
                score = self.calculate_weighed_score(
                    self.normalize(rp['name']),
                    self.normalize(kp['name'])
                )
                if score > best_score and score >= 60:
                    best_score = score
                    best_match = kp
            if best_match:
                k_price = self.parse_kosik_price(best_match, r_unit)
                matched.append({
                    'rohlik': {**rp, 'unit_price': r_price, 'unit': r_unit},
                    'kosik': {**best_match, 'unit_price': k_price, 'unit': r_unit}
                })
            else:
                matched.append({
                    'rohlik': {**rp, 'unit_price': r_price, 'unit': r_unit},
                    'kosik': None
                })
        return matched

    def parse_rohlik_unit(self, item):
        """Extract unit price from Rohlik item with decimal support"""
        unit_str = item.get('unit_price', '0 Kč/unit')
        # Match numbers with dots/commas as decimals and optional thousand separators
        match = re.search(r"(\d{1,3}(?:[.,\d]{3})*(?:[.,]\d+)?)\s*Kč/(\w+)", unit_str)
        if match:
            price_str = match.group(1)
            
            # Standardize decimal separator and remove thousand separators
            if ',' in price_str and '.' in price_str:
                # Handle both separators (e.g., 1.000,50 -> 1000.50)
                price_str = price_str.replace('.', '').replace(',', '.')
            else:
                # Replace comma decimal separator with dot
                price_str = price_str.replace(',', '.')
                
            # Remove any remaining thousand separators
            price_str = price_str.replace('.', '', price_str.count('.') - 1 if '.' in price_str else 0)
            
            try:
                price = float(price_str)
                unit = match.group(2).lower()
                return price, unit
            except ValueError:
                pass
        
        return 0.0, 'unit'


    def parse_kosik_price(self, item, target_unit):
        """Parse Košík's price directly as unit price"""
        try:
            # Extract and clean price from Košík's 'price' field
            price_str = item.get('price', '0')
            
            # Remove all non-numeric characters except comma and period
            clean_price = re.sub(r'[^\d,.]', '', price_str)
            
            # Replace comma with period for float conversion
            price = float(clean_price.replace(',', '.'))
            
            return price
            
        except Exception as e:
            print(f"Error parsing Košík price: {e}")
            return 0.0
