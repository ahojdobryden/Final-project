import streamlit as st
import pandas as pd
from src.matching import GroceryComparator

# Enhanced session state initialization
if 'comparator' not in st.session_state:
    st.session_state.comparator = GroceryComparator()
    
if 'cart' not in st.session_state:
    st.session_state.cart = {
        'rohlik': {},
        'kosik': {},
        'categories': {}
    }

if 'results' not in st.session_state:
    st.session_state.results = {
        'total_rohlik': 0.0,
        'total_kosik': 0.0,
        'comparison_table': [],
        'unmatched_products': []
    }

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
    for idx, pair in enumerate(matched_products):
        rp = pair['rohlik']
        key = f"rohlik_{selected_category}_{rp['name']}_{idx}"
        
        if st.checkbox(f"{rp['name']} - {rp['unit_price']:.2f} Kč/{rp['unit']}", key=key):
            # Add to cart
            st.session_state.cart['rohlik'][rp['name']] = {
                'unit_price': rp['unit_price'],
                'unit': rp['unit'],
                'category': selected_category
            }
            if pair['kosik']:
                kp = pair['kosik']
                st.session_state.cart['kosik'][rp['name']] = {
                    'unit_price': kp['unit_price'],
                    'unit': kp['unit'],
                    'name': kp['name']
                }
        else:
            # Remove from cart
            if rp['name'] in st.session_state.cart['rohlik']:
                del st.session_state.cart['rohlik'][rp['name']]
            if rp['name'] in st.session_state.cart['kosik']:
                del st.session_state.cart['kosik'][rp['name']]

with kosik_col:
    st.subheader("Košík Matches")
    for pair in matched_products:
        rp = pair['rohlik']
        kp = pair['kosik']
        
        if kp:
            status = "✓" if rp['name'] in st.session_state.cart['rohlik'] else "→"
            st.write(f"{status} {kp['name']} - {kp['unit_price']:.2f} Kč/{kp['unit']}")
        else:
            st.error("✗ No match found" if rp['name'] in st.session_state.cart['rohlik'] else "→ No match available")

# Shopping cart display
if st.session_state.cart['rohlik']:
    st.subheader("Shopping Cart")
    for name, item in st.session_state.cart['rohlik'].items():
        kosik_item = st.session_state.cart['kosik'].get(name, {})
        cols = st.columns([3, 2, 2])
        cols[0].write(f"**{name}** ({item['category']})")
        cols[1].metric("Rohlik", f"{item['unit_price']:.2f} Kč/{item['unit']}")
        cols[2].metric("Košík", 
                      f"{kosik_item.get('unit_price', 0.0):.2f} Kč/{item['unit']}" if kosik_item else "N/A")

# Calculation function
def calculate_results():
    total_r = 0.0
    total_k = 0.0
    comparison = []
    unmatched_products = []
    
    for name in st.session_state.cart['rohlik']:
        r_item = st.session_state.cart['rohlik'][name]
        k_item = st.session_state.cart['kosik'].get(name)
        
        if k_item:
            total_r += r_item['unit_price']
            total_k += k_item['unit_price']
            comparison.append({
                'Rohlik Product': name,
                'Matched Košík Product': k_item['name'],
                'Rohlik Price (Kč)': round(r_item['unit_price'], 2),
                'Košík Price (Kč)': round(k_item['unit_price'], 2)
            })
        else:
            unmatched_products.append(name)
            comparison.append({
                'Rohlik Product': name,
                'Matched Košík Product': 'No match found',
                'Rohlik Price (Kč)': round(r_item['unit_price'], 2),
                'Košík Price (Kč)': None
            })
    
    st.session_state.results = {
        'total_rohlik': total_r,
        'total_kosik': total_k,
        'comparison_table': comparison,
        'unmatched_products': unmatched_products
    }

# Results section
st.divider()
if st.button("Calculate Totals") and st.session_state.cart['rohlik']:
    calculate_results()
    
    st.subheader("Comparison Results")
    cols = st.columns(2)
    cols[0].metric("Total Rohlik", f"{st.session_state.results['total_rohlik']:.2f} Kč")
    cols[1].metric("Total Košík", f"{st.session_state.results['total_kosik']:.2f} Kč")
    
    total_r = st.session_state.results['total_rohlik']
    total_k = st.session_state.results['total_kosik']
    unmatched = st.session_state.results['unmatched_products']
    
    if total_r < total_k:
        st.success("Recommended to shop at Rohlik")
    elif total_k < total_r:
        if unmatched:
            product_list = ", ".join(unmatched)
            if len(unmatched) == 1:
                msg = f"If you do not need {product_list}, shopping at Košík is cheaper. If {product_list} is essential, go with Rohlik."
            else:
                msg = f"If you do not need {product_list}, shopping at Košík is cheaper. If {product_list} are essential, go with Rohlik."
            st.warning(msg)
        else:
            st.warning("Recommended to shop at Košík")
    else:
        st.info("Prices are equal")
    
    # Create and display table
    df = pd.DataFrame(st.session_state.results['comparison_table'])
    def format_na(val):
        return 'N/A' if pd.isna(val) else f'{val:.2f}'
    st.table(df.style.format({
        'Rohlik Price (Kč)': '{:.2f}',
        'Košík Price (Kč)': format_na
    }))
