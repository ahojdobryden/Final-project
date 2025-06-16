import streamlit as st
import pandas as pd
from src.matching import GroceryComparator

# Initialize session state for GroceryComparator instance
if 'comparator' not in st.session_state:
    st.session_state.comparator = GroceryComparator()

# Initialize empty shopping cart in session state
if 'cart' not in st.session_state:
    st.session_state.cart = {
        'rohlik': {},
        'kosik': {},
        'categories': {}
    }

# Initialize result storage in session state
if 'results' not in st.session_state:
    st.session_state.results = {
        'total_rohlik': 0.0,
        'total_kosik': 0.0,
        'comparison_table': [],
        'unmatched_products': []
    }

# --- Main Interface ---
st.title("Rohlik vs Košík - Unit Price Comparison")

# Category selection from unique subcategory names in Rohlik data
categories = list({item['subcategory_name'] for item in st.session_state.comparator.data_rohlik})
selected_category = st.selectbox("Select Product Category", categories)

# Get matched product pairs for the selected category
matched_products = st.session_state.comparator.find_products(selected_category)

# Display matched products from both retailers side by side
rohlik_col, kosik_col = st.columns(2)

with rohlik_col:
    st.subheader("Rohlik Products")
    for idx, pair in enumerate(matched_products):
        rp = pair['rohlik']
        key = f"rohlik_{selected_category}_{rp['name']}_{idx}"
        
        if st.checkbox(f"{rp['name']} - {rp['unit_price']:.2f} Kč/{rp['unit']}", key=key):
            # Add selected Rohlik product (and match if exists) to cart
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
            # Remove product from cart if deselected
            st.session_state.cart['rohlik'].pop(rp['name'], None)
            st.session_state.cart['kosik'].pop(rp['name'], None)

with kosik_col:
    st.subheader("Košík Matches")
    for pair in matched_products:
        rp = pair['rohlik']
        kp = pair['kosik']
        
        if kp:
            status = "✓" if rp['name'] in st.session_state.cart['rohlik'] else "→"
            st.write(f"{status} {kp['name']} - {kp['unit_price']:.2f} Kč/{kp['unit']}")
        else:
            msg = "✗ No match found" if rp['name'] in st.session_state.cart['rohlik'] else "→ No match available"
            st.error(msg)

# Display shopping cart if it has items
if st.session_state.cart['rohlik']:
    st.subheader("Shopping Cart")
    for name, item in st.session_state.cart['rohlik'].items():
        kosik_item = st.session_state.cart['kosik'].get(name, {})
        cols = st.columns([3, 2, 2])
        cols[0].write(f"**{name}** ({item['category']})")
        cols[1].metric("Rohlik", f"{item['unit_price']:.2f} Kč/{item['unit']}")
        cols[2].metric("Košík", 
                      f"{kosik_item.get('unit_price', 0.0):.2f} Kč/{item['unit']}" if kosik_item else "N/A")

def calculate_results():
    """
    Calculate the total prices (per unit) for selected products in both Rohlik and Košík carts.
    Also prepare a comparison table and identify unmatched products.

    Updates the session state with:
    - st.session_state.cart: Dictionary containing selected products from Rohlik and Košík
    - st.session_state.results: Dictionary containing:
            - total_rohlik: Sum of prices from Rohlik
            - total_kosik: Sum of prices from Košík (where matched)
            - comparison_table: List of product-wise comparison dicts
            - unmatched_products: List of products without a match in Košík
    """
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

# --- Results Section ---
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

    # Interpret total price comparison
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

    # Display comparison table
    df = pd.DataFrame(st.session_state.results['comparison_table'])

    def format_na(val):
        """Format missing values as 'N/A'."""
        return 'N/A' if pd.isna(val) else f'{val:.2f}'

    st.table(df.style.format({
        'Rohlik Price (Kč)': '{:.2f}',
        'Košík Price (Kč)': format_na
    }))
