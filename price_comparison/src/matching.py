import pandas as pd
import json as js  # Imported as 'js' per original code
import os
from rapidfuzz import fuzz, process
import unicodedata
import sys
import re

# Get absolute path to current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct path to data files
#DATA_PATH = os.path.join(BASE_DIR, '..', 'data')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this .py file
DATA_PATH_kosik = os.path.join(BASE_DIR, '..', 'data', 'data_kosik_subcats.json')
DATA_PATH_rohlik = os.path.join(BASE_DIR, '..', 'data', 'rohlik_dairy_products_multi_cat.json')
class GroceryComparator:
    def __init__(self):
        # Load data files
        with open(DATA_PATH_kosik, 'r', encoding='utf-8') as file, \
             open(DATA_PATH_rohlik, 'r', encoding='utf-8') as file2:
            self.data_kosik_dupl = js.load(file)
            self.data_rohlik = js.load(file2)

        # Process Kosik data
        self._process_data()
        self._match_categories()
        self._process_protein_items()

    @staticmethod
    def normalize(text):
        """Normalize text for comparison: lowercase, remove accents/whitespace"""
        text = text.lower().strip()
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    @staticmethod
    def calculate_weighed_score(item1, item2):
        """Calculate weighted similarity score between two strings"""
        score1 = fuzz.token_set_ratio(item1, item2)
        score2 = fuzz.partial_ratio(item1, item2)
        score3 = fuzz.ratio(item1, item2)
        score4 = fuzz.partial_token_set_ratio(item1, item2)
        return 0.4 * score1 + 0.2 * score2 + 0.2 * score3 + 0.2 * score4

    def _process_data(self):
        """Process and clean raw data"""
        # Kosik data processing
        self.unique_kosik_dict = {}
        for item in self.data_kosik_dupl:
            self.unique_kosik_dict[item['name']] = item
        self.data_kosik = list(self.unique_kosik_dict.values())
        
        # Rohlik data processing
        self.rohlik_df = pd.DataFrame(self.data_rohlik, columns=('name', 'price', 'subcategory_name', 'subcategory_url'))

    def _match_categories(self):
        """Match product categories between stores"""
        self.kosik_subcategories = {row['subcategory'] for row in self.data_kosik}
        self.rohlik_subcategories = {item['subcategory_name'] for item in self.data_rohlik}
        
        self.normalized_kosik = {self.normalize(cat): cat for cat in self.kosik_subcategories}
        self.normalized_rohlik = {self.normalize(cat): cat for cat in self.rohlik_subcategories}
        
        self.match_rohlik_to_kosik = {}
        for rohlik_cat in self.rohlik_subcategories:
            norm_rohlik = self.normalize(rohlik_cat)
            best_match = None
            best_score = 0
            
            for norm_kosik in self.normalized_kosik.keys():
                score = self.calculate_weighed_score(norm_rohlik, norm_kosik)
                if score > best_score and self._is_valid_match(norm_rohlik, norm_kosik):
                    best_score = score
                    best_match = norm_kosik
            
            self.match_rohlik_to_kosik[norm_rohlik] = self.normalized_kosik.get(best_match, None)

    def _is_valid_match(self, rohlik_norm, kosik_norm):
        """Filter invalid category matches"""
        return not (
            (kosik_norm == 'tvarohy' and rohlik_norm != 'smetany, slehacky, tvarohy - tvarohy') or
            (kosik_norm == 'mlecne vyrobky pro deti' and rohlik_norm not in ['mlecne - pro deti', 'syry - snacky'])
        )

    def _process_protein_items(self):
        """Special handling for protein-enriched items"""
        for item in self.data_kosik:
            if "protein" in self.normalize(item['name']):
                item['subcategory'] = 'Speciální - High protein'

    def find_products(self, selected_category):
        """Find matching products between stores for a selected category"""
    # Normalize the selected category
        norm_category = self.normalize(selected_category)
    
    # Get corresponding Košík category
        kosik_category = self.match_rohlik_to_kosik.get(norm_category, None)
    
    # Get all Košík products in matched category
        kosik_products = []
        if kosik_category:
            kosik_products = [item for item in self.data_kosik 
                            if item['subcategory'] == kosik_category]
        
    # Get all Rohlik products in selected category
        rohlik_products = [item for item in self.data_rohlik 
                        if self.normalize(item['subcategory_name']) == norm_category]
        
        return {
            'rohlik': rohlik_products,
            'kosik': kosik_products
    }

    def run_cli(self):
        """Command-line interface for testing"""
        print(f"Kosik data contains {len(self.data_kosik)} items.")
        print("Available categories:", [self.normalized_rohlik[key] for key in self.normalized_rohlik])
        
        # Category selection
        while True:
            category_input = input("Enter category (or 'exit'): ")
            if category_input.lower() == 'exit':
                return
            
            norm_category = self.normalize(category_input)
            if norm_category in self.normalized_rohlik:
                self._handle_category_selection(norm_category)
                break
            print("Invalid category. Try again.")

    def _handle_category_selection(self, norm_category):
        """Handle product selection for a chosen category"""
        print(f"Selected category: {self.normalized_rohlik[norm_category]}")
    
    def parse_rohlik_unit(self, item):
        """Extract unit price and measurement unit from Rohlik's unit_price"""
        unit_price_str = item.get('unit_price', '0 Kč/unit')
        match = re.search(r"([\d,]+)\s*Kč/(\w+)", unit_price_str)
        if match:
            price = float(match.group(1).replace(',', '.'))
            unit = match.group(2).lower()
            return price, unit
        return 0.0, 'unit'

    def parse_kosik_price(self, item, rohlik_unit):
        """Parse Košík's price using Rohlik's unit"""
        price_str = item.get('price', '0')
        try:
            return float(price_str.replace(',', '.').replace(' Kč', ''))
        except ValueError:
            return 0.0

    def find_products(self, selected_category):
        """Enhanced product matching with unit awareness"""
        norm_category = self.normalize(selected_category)
        kosik_category = self.match_rohlik_to_kosik.get(norm_category, None)
        
        # Get Rohlik products with parsed units
        rohlik_products = []
        for item in self.data_rohlik:
            if self.normalize(item.get('subcategory_name', '')) == norm_category:
                unit_price, unit = self.parse_rohlik_unit(item)
                rohlik_products.append({
                    **item,
                    'unit_price_value': unit_price,
                    'unit': unit
                })
        
        # Get Košík products
        kosik_products = []
        if kosik_category:
            kosik_products = [item for item in self.data_kosik 
                            if item.get('subcategory', '') == kosik_category]
        
        # Match products with unit conversion
        matched_products = []
        for r_product in rohlik_products:
            best_match = None
            best_score = 0
            for k_product in kosik_products:
                score = self.calculate_weighed_score(
                    self.normalize(r_product['name']),
                    self.normalize(k_product['name'])
                )
                if score > best_score:
                    best_match = k_product
                    best_score = score
            
            if best_match:
                # Use Rohlik's unit for Košík price
                kosik_price = self.parse_kosik_price(best_match, r_product['unit'])
                matched_products.append({
                    'rohlik': r_product,
                    'kosik': {
                        **best_match,
                        'unit_price_value': kosik_price,
                        'unit': r_product['unit']
                    }
                })
        return matched_products

if __name__ == "__main__":
    comparator = GroceryComparator()
    comparator.run_cli()
