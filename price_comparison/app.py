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
def parse_kosik_price(price_str):
    """Parse Košík price string to float"""
    try:
        # Handle format like "386,00" or "386.00"
        clean_price = price_str.replace(',', '.').replace(' ', '').replace('Kč', '')
        return float(clean_price)
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

# Get matched products for the selected category
matched_products = st.session_state.comparator.find_products(selected_category)

# Display products
rohlik_col, kosik_col = st.columns(2)

with rohlik_col:
    st.subheader("Rohlik Products")
    
    for idx, product_pair in enumerate(matched_products):
        rohlik_product = product_pair['rohlik']
        kosik_product = product_pair['kosik']
        
        unit_price, unit = parse_rohlik_unit(rohlik_product['unit_price'])
        display_text = f"{rohlik_product['name']} - {unit_price:.2f} Kč/{unit}"
        
        # Unique key for each checkbox
        key = f"rohlik_{rohlik_product['subcategory_name']}_{rohlik_product['name']}_{idx}"
        
        if st.checkbox(display_text, key=key):
            # Add Rohlik product to cart
            st.session_state.cart['rohlik'][rohlik_product['name']] = {
                'unit_price': unit_price,
                'unit': unit
            }
            
            # Automatically add corresponding Košík product to cart
            if kosik_product and 'name' in kosik_product:
                kosik_price = parse_kosik_price(kosik_product['price'])
                st.session_state.cart['kosik'][rohlik_product['name']] = {
                    'unit_price': kosik_price,
                    'unit': unit,
                    'name': kosik_product['name']
                }
        else:
            # Remove from cart if unchecked
            if rohlik_product['name'] in st.session_state.cart['rohlik']:
                del st.session_state.cart['rohlik'][rohlik_product['name']]
            if rohlik_product['name'] in st.session_state.cart['kosik']:
                del st.session_state.cart['kosik'][rohlik_product['name']]

with kosik_col:
    st.subheader("Košík Matches")
    
    for idx, product_pair in enumerate(matched_products):
        rohlik_product = product_pair['rohlik']
        kosik_product = product_pair['kosik']
        
        if kosik_product and 'name' in kosik_product:
            kosik_price = parse_kosik_price(kosik_product['price'])
            unit = parse_rohlik_unit(rohlik_product['unit_price'])[1]
            
            # Show matched product without checkbox
            if rohlik_product['name'] in st.session_state.cart['rohlik']:
                st.success(f"✓ {kosik_product['name']} - {kosik_price:.2f} Kč/{unit}")
            else:
                st.write(f"→ {kosik_product['name']} - {kosik_price:.2f} Kč/{unit}")
        else:
            # No match found
            if rohlik_product['name'] in st.session_state.cart['rohlik']:
                st.error("✗ No match found")
            else:
                st.write("→ No match found")

# Show current cart
if st.session_state.cart['rohlik']:
    st.subheader("Shopping Cart")
    for product_name in st.session_state.cart['rohlik']:
        rohlik_item = st.session_state.cart['rohlik'][product_name]
        kosik_item = st.session_state.cart['kosik'].get(product_name, {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Rohlik: {product_name}")
        with col2:
            if kosik_item:
                st.write(f"Košík: {kosik_item.get('name', 'No match')}")

# Calculation and results
def calculate_results():
    comparison_table = []
    total_rohlik = 0.0
    total_kosik = 0.0
    
    for product_name in st.session_state.cart['rohlik']:
        rohlik_item = st.session_state.cart['rohlik'][product_name]
        kosik_item = st.session_state.cart['kosik'].get(product_name, {})
        
        rohlik_price = rohlik_item['unit_price']
        kosik_price = kosik_item.get('unit_price', 0.0)
        
        total_rohlik += rohlik_price
        total_kosik += kosik_price
        
        comparison_table.append({
            'Product': product_name,
            'Rohlik Price': f"{rohlik_price:.2f} Kč/{rohlik_item['unit']}",
            'Košík Price': f"{kosik_price:.2f} Kč/{rohlik_item['unit']}"
        })
    
    st.session_state.results = {
        'total_rohlik': total_rohlik,
        'total_kosik': total_kosik,
        'comparison_table': comparison_table
    }

# Results display
st.divider()
if st.session_state.cart['rohlik'] and st.button("Calculate Comparison"):
    calculate_results()
    
    st.subheader("Comparison Results")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rohlik", f"{st.session_state.results['total_rohlik']:.2f} Kč")
    with col2:
        st.metric("Total Košík", f"{st.session_state.results['total_kosik']:.2f} Kč")
    
    if st.session_state.results['total_rohlik'] < st.session_state.results['total_kosik']:
        st.success("Recommended to shop at Rohlik")
    elif st.session_state.results['total_kosik'] < st.session_state.results['total_rohlik']:
        st.warning("Recommended to shop at Košík")
    else:
        st.info("Both stores have the same total price")
    
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
