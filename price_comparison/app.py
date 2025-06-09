import streamlit as st
import sys
import os
from pathlib import Path
from src.matching import GroceryComparator
import re

# Initialize session state
if 'comparator' not in st.session_state:
    st.session_state.comparator = GroceryComparator()
    
if 'cart' not in st.session_state:
    st.session_state.cart = {
        'rohlik': {},
        'kosik': {}
    }

if 'results' not in st.session_state:
    st.session_state.results = {
        'total_rohlik': 0.0,
        'total_kosik': 0.0,
        'comparison_table': []
    }

# Utility functions
def parse_price(price_str):
    """Parse Czech price string to float"""
    try:
        return float(re.search(r'[\d,]+', price_str.replace(' ', '')).group().replace(',', '.'))
    except:
        return 0.0

def parse_rohlik_unit(unit_price_str):
    """Extract unit and price from Rohlik's unit_price string"""
    match = re.search(r'([\d,]+)\s*Kč/(\w+)', unit_price_str)
    if match:
        return float(match.group(1).replace(',', '.')), match.group(2).lower()
    return 0.0, 'unit'

# Main interface
st.title("Rohlik vs Košík - Unit Price Comparison")

# Category selection
categories = list({item['subcategory_name'] for item in st.session_state.comparator.data_rohlik})
selected_category = st.selectbox("Select Product Category", categories)

# Display products
rohlik_col, kosik_col = st.columns(2)

with rohlik_col:
    st.subheader("Rohlik Products")
    rohlik_products = [item for item in st.session_state.comparator.data_rohlik 
                      if item['subcategory_name'] == selected_category]
    
    for idx, product in enumerate(rohlik_products):
        unit_price, unit = parse_rohlik_unit(product['unit_price'])
        display_text = f"{product['name']} - {unit_price:.2f} Kč/{unit}"
        # Key now includes index and subcategory to ensure uniqueness
        key = f"rohlik_{product['subcategory_name']}_{product['name']}_{idx}"
        if st.checkbox(display_text, key=key):
            st.session_state.cart['rohlik'][product['name']] = {
                'unit_price': unit_price,
                'unit': unit
            }

with kosik_col:
    st.subheader("Košík Matches")
    matched_products = st.session_state.comparator.find_products(selected_category)
    
    for idx, product in enumerate(matched_products):
        rohlik_name = product['rohlik']['name']
        kosik_product = product['kosik']
        
        if kosik_product:
            kosik_price = parse_price(kosik_product['price'])
            unit = product['rohlik']['unit']
            display_text = f"{kosik_product['name']} - {kosik_price:.2f} Kč/{unit}"
            # Key now includes index and rohlik name to ensure uniqueness
            key = f"kosik_{rohlik_name}_{kosik_product['name']}_{idx}"
            if st.checkbox(display_text, key=key):
                st.session_state.cart['kosik'][rohlik_name] = {
                    'unit_price': kosik_price,
                    'unit': unit
                }

# Calculation and results
def calculate_results():
    comparison_table = []
    total_rohlik = 0.0
    total_kosik = 0.0
    
    for product_name in st.session_state.cart['rohlik']:
        rohlik_item = st.session_state.cart['rohlik'][product_name]
        kosik_item = st.session_state.cart['kosik'].get(product_name, {})
        
        total_rohlik += rohlik_item['unit_price']
        kosik_price = kosik_item.get('unit_price', 0.0)
        total_kosik += kosik_price
        
        comparison_table.append({
            'Product': product_name,
            'Rohlik Price': f"{rohlik_item['unit_price']:.2f} Kč/{rohlik_item['unit']}",
            'Košík Price': f"{kosik_price:.2f} Kč/{rohlik_item['unit']}"
        })
    
    st.session_state.results = {
        'total_rohlik': total_rohlik,
        'total_kosik': total_kosik,
        'comparison_table': comparison_table
    }

# Results display
st.divider()
if st.button("Calculate Comparison"):
    calculate_results()
    
    st.subheader("Comparison Results")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rohlik", f"{st.session_state.results['total_rohlik']:.2f} Kč")
    with col2:
        st.metric("Total Košík", f"{st.session_state.results['total_kosik']:.2f} Kč")
    
    if st.session_state.results['total_rohlik'] < st.session_state.results['total_kosik']:
        st.success("Recommended to shop at Rohlik")
    else:
        st.warning("Recommended to shop at Košík")
    
    st.write("Detailed Price Comparison:")
    st.dataframe(
        st.session_state.results['comparison_table'],
        column_config={
            "Product": "Product Name",
            "Rohlik Price": st.column_config.TextColumn("Rohlik Price"),
            "Košík Price": st.column_config.TextColumn("Košík Price")
        },
        hide_index=True,
        use_container_width=True
    )
