import json
import pandas as pd
from pathlib import Path
from collections import Counter

#Category mapping dictionary
KOSIK_TO_ROHLIK_MAPPING = {
    'syry': 'Sýry',
    'jogurty a mlecne dezerty': 'Jogurty',
    'maslo margariny tuky': 'Máslo',
    'smetany a slehacky': 'Smetany, šlehačky, tvarohy',
    'tvarohy': 'Smetany, šlehačky, tvarohy',
    'mleko a mlecne napoje': 'Mléčné',
    'majonezy tatarky a dresingy': 'Majonézy, Dresingy a Tatarské omáčky',
    'rostlinne a bilkovinne alternativy': 'Mléčné',
    'mlecne vyrobky pro deti': 'Mléčné',
    'bez laktozy': 'Mléčné',
    'bio': 'Sýry BIO a farmářské',
    'farmarske': 'Sýry BIO a farmářské',
    # Categories to be excluded (will be filtered out)
    # 'vejce a drozdi': 'EXCLUDE',  # Will be removed
    # 'xxl baleni': 'EXCLUDE',     # Will be removed
}

# Categories to exclude from the dataset
EXCLUDED_CATEGORIES = ['vejce a drozdi', 'xxl baleni']

# Rohlik categories to merge
ROHLIK_CATEGORY_MAPPING = {
    'Majonézy': 'Majonézy, Dresingy a Tatarské omáčky',
    'Dresingy': 'Majonézy, Dresingy a Tatarské omáčky',
    'Tatarské omáčky': 'Majonézy, Dresingy a Tatarské omáčky',
    'Plátkové sýry': 'Sýry',
    'Čerstvě krájené': 'Sýry',
    'Sýry': 'Sýry'
}

# Rohlik categories to exclude
ROHLIK_EXCLUDED_CATEGORIES = ['Speciální']

def load_json_data():
    """
    Load JSON files from the same directory as this script
    """
    # Get the directory where this script is located
    script_dir = Path(__file__).resolve().parent
    
    # Files are in the same directory as the script
    kosik_file = script_dir / 'data_kosik_subcats.json'
    rohlik_file = script_dir / 'rohlik_dairy_products_multi_cat.json'
    
    print(f"Loading files from: {script_dir}")
    print(f"Kosik file: {kosik_file}")
    print(f"Rohlik file: {rohlik_file}")
    
    # Load Kosik data
    kosik_data = None
    if kosik_file.exists():
        with open(kosik_file, 'r', encoding='utf-8') as file:
            kosik_data = json.load(file)
        print(f"✓ Loaded Kosik data: {len(kosik_data)} items")
    else:
        print(f"✗ Kosik file not found")
    
    # Load Rohlik data
    rohlik_data = None
    if rohlik_file.exists():
        with open(rohlik_file, 'r', encoding='utf-8') as file:
            rohlik_data = json.load(file)
        print(f"✓ Loaded Rohlik data: {len(rohlik_data)} items")
    else:
        print(f"✗ Rohlik file not found")
    
    return kosik_data, rohlik_data

def filter_kosik_data(kosik_data):
    """
    Filter out excluded categories from Kosik data
    
    Args:
        kosik_data: List of Kosik product dictionaries
        
    Returns:
        list: Filtered Kosik data without excluded categories
    """
    if not kosik_data:
        return kosik_data
    
    if isinstance(kosik_data, dict):
        kosik_data = [kosik_data]
    
    original_count = len(kosik_data)
    
    # Filter out products with excluded categories
    filtered_data = []
    excluded_count = 0
    
    for item in kosik_data:
        category = item.get('subcategory', '')
        if category not in EXCLUDED_CATEGORIES:
            filtered_data.append(item)
        else:
            excluded_count += 1
    
    print(f"\nFiltering Kosik data:")
    print(f"Original products: {original_count}")
    print(f"Excluded products: {excluded_count}")
    print(f"Remaining products: {len(filtered_data)}")
    print(f"Excluded categories: {EXCLUDED_CATEGORIES}")
    
    return filtered_data

def filter_and_remap_rohlik_data(rohlik_data):
    """
    Filter out excluded categories and remap categories in Rohlik data
    
    Args:
        rohlik_data: List of Rohlik product dictionaries
        
    Returns:
        list: Filtered and remapped Rohlik data
    """
    if not rohlik_data:
        return rohlik_data
    
    if isinstance(rohlik_data, dict):
        rohlik_data = [rohlik_data]
    
    original_count = len(rohlik_data)
    
    # Filter out products with excluded categories and remap categories
    filtered_data = []
    excluded_count = 0
    remapped_count = 0
    
    for item in rohlik_data:
        if 'subcategory_name' in item and item['subcategory_name']:
            # Extract main category (part before the "-")
            full_category = item['subcategory_name']
            main_category = full_category.split(' - ')[0].strip()
            
            # Skip excluded categories
            if main_category in ROHLIK_EXCLUDED_CATEGORIES:
                excluded_count += 1
                continue
            
            # Remap categories if needed
            if main_category in ROHLIK_CATEGORY_MAPPING:
                new_category = ROHLIK_CATEGORY_MAPPING[main_category]
                if new_category != main_category:
                    remapped_count += 1
                    # Create a new subcategory_name with the remapped category
                    if ' - ' in full_category:
                        subcategory = full_category.split(' - ', 1)[1]
                        item['subcategory_name'] = f"{new_category} - {subcategory}"
                    else:
                        item['subcategory_name'] = new_category
                    
                    # Also store the original category for reference
                    item['original_category'] = main_category
            
            filtered_data.append(item)
    
    print(f"\nFiltering and remapping Rohlik data:")
    print(f"Original products: {original_count}")
    print(f"Excluded products: {excluded_count}")
    print(f"Remapped categories: {remapped_count}")
    print(f"Remaining products: {len(filtered_data)}")
    print(f"Excluded categories: {ROHLIK_EXCLUDED_CATEGORIES}")
    
    return filtered_data

def extract_kosik_categories(kosik_data):
    """
    Extract category names from Kosik JSON data
    
    Args:
        kosik_data: List of dictionaries with Kosik product data
    
    Returns:
        Dictionary containing extracted category information
    """
    if not kosik_data:
        return {
            'subcategories': [],
            'subcategory_counts': {},
            'total_products': 0
        }
    
    subcategories = []
    
    # Handle both single item and list of items
    if isinstance(kosik_data, dict):
        kosik_data = [kosik_data]
    
    for item in kosik_data:
        # Extract subcategory only
        if 'subcategory' in item and item['subcategory']:
            subcategories.append(item['subcategory'])
    
    # Get unique categories and counts
    unique_subcategories = sorted(list(set(subcategories)))
    subcategory_counts = dict(Counter(subcategories))
    
    return {
        'subcategories': unique_subcategories,
        'subcategory_counts': subcategory_counts,
        'total_products': len(kosik_data)
    }

def extract_rohlik_categories(rohlik_data):
    """
    Extract category names from Rohlik JSON data (only part before the "-")
    
    Args:
        rohlik_data: List of dictionaries with Rohlik product data
    
    Returns:
        Dictionary containing extracted category information
    """
    if not rohlik_data:
        return {
            'categories': [],
            'category_counts': {},
            'total_products': 0
        }
    
    categories = []
    
    # Handle both single item and list of items
    if isinstance(rohlik_data, dict):
        rohlik_data = [rohlik_data]
    
    for item in rohlik_data:
        # Extract main category (part before the "-")
        if 'subcategory_name' in item and item['subcategory_name']:
            full_category = item['subcategory_name']
            # Split by " - " and take only the first part
            main_category = full_category.split(' - ')[0].strip()
            categories.append(main_category)
    
    # Get unique categories and counts
    unique_categories = sorted(list(set(categories)))
    category_counts = dict(Counter(categories))
    
    return {
        'categories': unique_categories,
        'category_counts': category_counts,
        'total_products': len(rohlik_data)
    }

def clean_price_string(price_str):
    """
    Clean price string by removing currency symbols and converting to float
    
    Args:
        price_str (str): Price string to clean
        
    Returns:
        str: Cleaned price string with just the numeric value
    """
    if not price_str:
        return None
    
    # Remove common currency symbols and units
    cleaned = str(price_str).replace('Kč', '')
    cleaned = cleaned.replace('/kg', '').replace('/l', '').replace('/ks', '')
    cleaned = cleaned.strip()
    
    # Handle comma as decimal separator (Czech format)
    if ',' in cleaned and '.' not in cleaned:
        cleaned = cleaned.replace(',', '.')
    
    return cleaned

def create_combined_dataset(kosik_data, rohlik_data):
    """
    Create a combined dataset from Kosik and Rohlik data
    
    Args:
        kosik_data: List of Kosik product dictionaries
        rohlik_data: List of Rohlik product dictionaries
        
    Returns:
        pandas.DataFrame: Combined dataset with product, store, and price columns
    """
    combined_records = []
    
    # Process Kosik data (now filtered)
    if kosik_data:
        if isinstance(kosik_data, dict):
            kosik_data = [kosik_data]
        
        for item in kosik_data:
            # Extract required fields with error handling
            product_name = item.get('name', 'Unknown Product')
            price = item.get('price', None)
            
            # Clean the price
            cleaned_price = clean_price_string(price)
            
            combined_records.append({
                'product': product_name,
                'store': 'kosik',
                'price': cleaned_price
            })
    
    # Process Rohlik data
    if rohlik_data:
        if isinstance(rohlik_data, dict):
            rohlik_data = [rohlik_data]
        
        for item in rohlik_data:
            # Extract required fields with error handling
            product_name = item.get('name', 'Unknown Product')
            unit_price = item.get('unit_price', None)
            
            # Clean the price
            cleaned_price = clean_price_string(unit_price)
            
            combined_records.append({
                'product': product_name,
                'store': 'rohlik',
                'price': cleaned_price
            })
    
    # Create DataFrame
    df = pd.DataFrame(combined_records)
    
    return df

def inspect_dataset(df):
    """
    Display head and tail of the dataset for inspection
    
    Args:
        df: pandas.DataFrame with the combined dataset
    """
    print(f"\n{'='*60}")
    print("DATASET INSPECTION")
    print(f"{'='*60}")
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    print(f"\n{'-'*40}")
    print("HEAD (First 10 rows)")
    print(f"{'-'*40}")
    print(df.head(10).to_string(index=False))
    
    print(f"\n{'-'*40}")
    print("TAIL (Last 10 rows)")
    print(f"{'-'*40}")
    print(df.tail(10).to_string(index=False))

def calculate_price_statistics(df):
    """
    Calculate comprehensive price statistics for the dataset
    
    Args:
        df: pandas.DataFrame with the combined dataset
    """
    # Convert price column to numeric, handling errors
    df['price_numeric'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Filter out rows with invalid prices
    valid_df = df[df['price_numeric'].notna() & (df['price_numeric'] > 0)]
    
    print(f"\n{'='*60}")
    print("PRICE STATISTICS ANALYSIS")
    print(f"{'='*60}")
    
    print(f"Total products: {len(df)}")
    print(f"Products with valid prices: {len(valid_df)}")
    print(f"Products with invalid/missing prices: {len(df) - len(valid_df)}")
    
    if len(valid_df) == 0:
        print("No valid price data found for analysis!")
        return
    
    # Average unit price across all products for both stores
    print(f"\n{'-'*50}")
    print("AVERAGE UNIT PRICES")
    print(f"{'-'*50}")
    
    overall_avg = valid_df['price_numeric'].mean()
    print(f"Overall average price: {overall_avg:.2f} Kč")
    
    # Average by store
    store_averages = valid_df.groupby('store')['price_numeric'].mean()
    for store, avg_price in store_averages.items():
        print(f"Average price at {store.title()}: {avg_price:.2f} Kč")
    
    # Cheapest and most expensive products by store
    print(f"\n{'-'*50}")
    print("PRICE EXTREMES BY STORE")
    print(f"{'-'*50}")
    
    for store in ['kosik', 'rohlik']:
        store_data = valid_df[valid_df['store'] == store]
        
        if len(store_data) > 0:
            print(f"\n{store.upper()} STORE:")
            
            # Cheapest product
            cheapest = store_data.loc[store_data['price_numeric'].idxmin()]
            print(f"  Cheapest: {cheapest['product'][:50]}{'...' if len(cheapest['product']) > 50 else ''}")
            print(f"  Price: {cheapest['price_numeric']:.2f} Kč")
            
            # Most expensive product
            expensive = store_data.loc[store_data['price_numeric'].idxmax()]
            print(f"  Most expensive: {expensive['product'][:50]}{'...' if len(expensive['product']) > 50 else ''}")
            print(f"  Price: {expensive['price_numeric']:.2f} Kč")
        else:
            print(f"\nNo valid price data found for {store}")

def add_categories_to_dataset(df, kosik_data, rohlik_data):
    """
    Add category information to the combined dataset
    
    Args:
        df: Combined dataset DataFrame
        kosik_data: Original Kosik data (filtered)
        rohlik_data: Original Rohlik data (filtered and remapped)
        
    Returns:
        pandas.DataFrame: Dataset with category information added
    """
    # Create category mapping dictionaries
    kosik_categories = {}
    rohlik_categories = {}
    
    # Map Kosik products to categories (using filtered data)
    if kosik_data:
        if isinstance(kosik_data, dict):
            kosik_data = [kosik_data]
        
        for item in kosik_data:
            product_name = item.get('name', '')
            category = item.get('subcategory', '')
            # Convert to standardized category using updated mapping
            standardized_category = convert_kosik_category(category)
            kosik_categories[product_name] = standardized_category
    
    # Map Rohlik products to categories (using filtered and remapped data)
    if rohlik_data:
        if isinstance(rohlik_data, dict):
            rohlik_data = [rohlik_data]
        
        for item in rohlik_data:
            product_name = item.get('name', '')
            subcategory_name = item.get('subcategory_name', '')
            # Extract main category (part before the "-")
            if subcategory_name:
                main_category = subcategory_name.split(' - ')[0].strip()
                rohlik_categories[product_name] = main_category
    
    # Add category column to the dataset
    def get_category(row):
        if row['store'] == 'kosik':
            return kosik_categories.get(row['product'], 'Unknown')
        else:  # rohlik
            return rohlik_categories.get(row['product'], 'Unknown')
    
    df['category'] = df.apply(get_category, axis=1)
    return df

def calculate_category_statistics(df):
    """
    Calculate average prices per category for both stores
    
    Args:
        df: DataFrame with product, store, price, and category columns
    """
    # Convert price to numeric if not already done
    if 'price_numeric' not in df.columns:
        df['price_numeric'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Filter valid prices
    valid_df = df[df['price_numeric'].notna() & (df['price_numeric'] > 0)]
    
    print(f"\n{'-'*50}")
    print("AVERAGE PRICES BY CATEGORY")
    print(f"{'-'*50}")
    
    # Overall category averages
    category_averages = valid_df.groupby('category')['price_numeric'].agg(['mean', 'count']).round(2)
    category_averages = category_averages.sort_values('mean', ascending=False)
    
    print("\nOverall Category Averages:")
    print(f"{'Category':<30} {'Avg Price (Kč)':<15} {'Product Count':<15}")
    print("-" * 60)
    for category, stats in category_averages.iterrows():
        print(f"{category:<30} {stats['mean']:<15.2f} {int(stats['count']):<15}")
    
    # Category averages by store
    print(f"\nCategory Averages by Store:")
    store_category_averages = valid_df.groupby(['store', 'category'])['price_numeric'].agg(['mean', 'count']).round(2)
    
    for store in ['kosik', 'rohlik']:
        print(f"\n{store.upper()}:")
        store_data = store_category_averages.loc[store] if store in store_category_averages.index else pd.DataFrame()
        
        if not store_data.empty:
            store_data = store_data.sort_values('mean', ascending=False)
            print(f"{'Category':<30} {'Avg Price (Kč)':<15} {'Product Count':<15}")
            print("-" * 60)
            for category, stats in store_data.iterrows():
                print(f"{category:<30} {stats['mean']:<15.2f} {int(stats['count']):<15}")
        else:
            print("No data available")

def display_summary_table(df):
    """
    Display a comprehensive summary table with key statistics
    
    Args:
        df: pandas.DataFrame with the combined dataset
    """
    # Convert price to numeric if not already done
    if 'price_numeric' not in df.columns:
        df['price_numeric'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Filter valid prices
    valid_df = df[df['price_numeric'].notna() & (df['price_numeric'] > 0)]
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE SUMMARY TABLE")
    print(f"{'='*80}")
    
    if len(valid_df) == 0:
        print("No valid price data available for summary!")
        return
    
    # Calculate overall statistics
    overall_avg = valid_df['price_numeric'].mean()
    overall_median = valid_df['price_numeric'].median()
    overall_min = valid_df['price_numeric'].min()
    overall_max = valid_df['price_numeric'].max()
    
    # Find overall cheapest and most expensive products
    cheapest_overall = valid_df.loc[valid_df['price_numeric'].idxmin()]
    expensive_overall = valid_df.loc[valid_df['price_numeric'].idxmax()]
    
    print(f"\n{'-'*80}")
    print("OVERALL STATISTICS")
    print(f"{'-'*80}")
    print(f"{'Metric':<40} {'Value':<20} {'Details':<20}")
    print("-" * 80)
    print(f"{'Total Products':<40} {len(df):<20} {'All stores':<20}")
    print(f"{'Products with Valid Prices':<40} {len(valid_df):<20} {'Price data available':<20}")
    print(f"{'Average Price':<40} {overall_avg:.2f} Kč{'':<8} {'Across all products':<20}")
    print(f"{'Median Price':<40} {overall_median:.2f} Kč{'':<8} {'Middle value':<20}")
    print(f"{'Price Range':<40} {overall_min:.2f} - {overall_max:.2f} Kč{'':<1} {'Min - Max':<20}")
    
    print(f"\n{'-'*80}")
    print("STORE COMPARISON")
    print(f"{'-'*80}")
    
    # Store-by-store statistics
    store_stats = valid_df.groupby('store')['price_numeric'].agg(['count', 'mean', 'median', 'min', 'max']).round(2)
    
    print(f"{'Store':<10} {'Products':<10} {'Avg Price':<12} {'Median':<10} {'Min Price':<12} {'Max Price':<12}")
    print("-" * 80)
    for store, stats in store_stats.iterrows():
        print(f"{store.title():<10} {int(stats['count']):<10} {stats['mean']:.2f} Kč{'':<3} {stats['median']:.2f} Kč{'':<1} {stats['min']:.2f} Kč{'':<3} {stats['max']:.2f} Kč")
    
    print(f"\n{'-'*80}")
    print("EXTREME VALUES")
    print(f"{'-'*80}")
    print(f"Overall Cheapest Product:")
    print(f"  {cheapest_overall['product'][:60]}{'...' if len(cheapest_overall['product']) > 60 else ''}")
    print(f"  Store: {cheapest_overall['store'].title()}, Price: {cheapest_overall['price_numeric']:.2f} Kč")
    
    print(f"\nOverall Most Expensive Product:")
    print(f"  {expensive_overall['product'][:60]}{'...' if len(expensive_overall['product']) > 60 else ''}")
    print(f"  Store: {expensive_overall['store'].title()}, Price: {expensive_overall['price_numeric']:.2f} Kč")
    
    # Store-specific extremes
    print(f"\n{'-'*80}")
    print("STORE-SPECIFIC EXTREMES")
    print(f"{'-'*80}")
    
    for store in ['kosik', 'rohlik']:
        store_data = valid_df[valid_df['store'] == store]
        if len(store_data) > 0:
            cheapest = store_data.loc[store_data['price_numeric'].idxmin()]
            expensive = store_data.loc[store_data['price_numeric'].idxmax()]
            
            print(f"\n{store.upper()} STORE:")
            print(f"  Cheapest: {cheapest['product'][:50]}{'...' if len(cheapest['product']) > 50 else ''}")
            print(f"  Price: {cheapest['price_numeric']:.2f} Kč")
            print(f"  Most Expensive: {expensive['product'][:50]}{'...' if len(expensive['product']) > 50 else ''}")
            print(f"  Price: {expensive['price_numeric']:.2f} Kč")

def display_dataset_summary(df):
    """
    Display summary statistics for the combined dataset
    
    Args:
        df: pandas.DataFrame with the combined dataset
    """
    print(f"\n{'='*60}")
    print("COMBINED DATASET SUMMARY")
    print(f"{'='*60}")
    
    print(f"Total products: {len(df)}")
    print(f"Kosik products: {len(df[df['store'] == 'kosik'])}")
    print(f"Rohlik products: {len(df[df['store'] == 'rohlik'])}")
    
    # Count products with valid prices
    valid_prices = df[df['price'].notna() & (df['price'] != '') & (df['price'] != '0')]
    print(f"Products with valid prices: {len(valid_prices)}")
    
    print(f"\n{'-'*40}")
    print("SAMPLE DATA")
    print(f"{'-'*40}")
    print(df.head(10).to_string(index=False))
    
    # Show products with missing prices
    missing_prices = df[df['price'].isna() | (df['price'] == '') | (df['price'] == '0')]
    if len(missing_prices) > 0:
        print(f"\n{'-'*40}")
        print(f"PRODUCTS WITH MISSING PRICES: {len(missing_prices)}")
        print(f"{'-'*40}")
        print(missing_prices.head().to_string(index=False))

def save_combined_dataset(df, filename="combined_dataset.csv"):
    """
    Save the combined dataset to a CSV file
    
    Args:
        df: pandas.DataFrame with the combined dataset
        filename: Name of the output file
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n✓ Combined dataset saved to: {filename}")
    except Exception as e:
        print(f"\n✗ Error saving dataset: {e}")

def display_kosik_categories(categories_data):
    """
    Display the extracted Kosik categories in a readable format
    """
    print(f"\n{'='*60}")
    print("KOSIK CATEGORY ANALYSIS")
    print(f"{'='*60}")
    
    print(f"Total products analyzed: {categories_data['total_products']}")
    
    print(f"\n{'-'*40}")
    print("SUBCATEGORIES")
    print(f"{'-'*40}")
    for i, category in enumerate(categories_data['subcategories'], 1):
        count = categories_data['subcategory_counts'].get(category, 0)
        print(f"{i:2d}. {category} ({count} products)")
    
    print(f"\n{'-'*40}")
    print("CATEGORY FREQUENCY")
    print(f"{'-'*40}")
    sorted_subcats = sorted(categories_data['subcategory_counts'].items(), 
                           key=lambda x: x[1], reverse=True)
    for category, count in sorted_subcats:
        print(f"{count:3d} products: {category}")

def display_rohlik_categories(categories_data):
    """
    Display the extracted Rohlik categories in a readable format
    """
    print(f"\n{'='*60}")
    print("ROHLIK CATEGORY ANALYSIS")
    print(f"{'='*60}")
    
    print(f"Total products analyzed: {categories_data['total_products']}")
    
    print(f"\n{'-'*40}")
    print("MAIN CATEGORIES")
    print(f"{'-'*40}")
    for i, category in enumerate(categories_data['categories'], 1):
        count = categories_data['category_counts'].get(category, 0)
        print(f"{i:2d}. {category} ({count} products)")
    
    print(f"\n{'-'*40}")
    print("CATEGORY FREQUENCY")
    print(f"{'-'*40}")
    sorted_cats = sorted(categories_data['category_counts'].items(), 
                        key=lambda x: x[1], reverse=True)
    for category, count in sorted_cats:
        print(f"{count:3d} products: {category}")

def convert_kosik_category(kosik_category):
    """
    Convert a Kosik category to its corresponding Rohlik category
    
    Args:
        kosik_category (str): Kosik category name
        
    Returns:
        str: Corresponding Rohlik category name
    """
    return KOSIK_TO_ROHLIK_MAPPING.get(kosik_category, 'Speciální')

def convert_kosik_data_categories(kosik_data):
    """
    Convert all category names in Kosik data to Rohlik category names
    
    Args:
        kosik_data (list): List of Kosik product dictionaries
        
    Returns:
        list: Modified data with converted category names
    """
    for item in kosik_data:
        if 'subcategory' in item:
            item['standardized_category'] = convert_kosik_category(item['subcategory'])
    
    return kosik_data

# Main execution with filtering and remapping
if __name__ == "__main__":
    # Load the data
    kosik_data, rohlik_data = load_json_data()

    # Filter Kosik data to remove excluded categories
    if kosik_data:
        kosik_data = filter_kosik_data(kosik_data)
        
        print("Ready to process filtered Kosik data")
        
        # Extract and display Kosik categories (after filtering)
        kosik_categories = extract_kosik_categories(kosik_data)
        display_kosik_categories(kosik_categories)
        
        print(f"\nFiltered Kosik Summary:")
        print(f"- Found {len(kosik_categories['subcategories'])} unique subcategories")
        print(f"- Subcategory list: {kosik_categories['subcategories']}")

    # Filter and remap Rohlik data
    if rohlik_data:
        rohlik_data = filter_and_remap_rohlik_data(rohlik_data)
        
        print("Ready to process filtered and remapped Rohlik data")
        
        # Extract and display Rohlik categories
        rohlik_categories = extract_rohlik_categories(rohlik_data)
        display_rohlik_categories(rohlik_categories)
        
        print(f"\nRohlik Summary:")
        print(f"- Found {len(rohlik_categories['categories'])} unique categories")
        print(f"- Category list: {rohlik_categories['categories']}")

    # Create combined dataset with filtered data
    if kosik_data or rohlik_data:
        print("\nCreating combined dataset with filtered data...")
        combined_df = create_combined_dataset(kosik_data, rohlik_data)
        
        # Add category information to dataset
        combined_df = add_categories_to_dataset(combined_df, kosik_data, rohlik_data)
        
        # Display dataset summary
        display_dataset_summary(combined_df)
        
        # DATASET INSPECTION
        inspect_dataset(combined_df)
        
        # PRICE STATISTICS ANALYSIS
        calculate_price_statistics(combined_df)
        
        # CATEGORY ANALYSIS
        calculate_category_statistics(combined_df)
        
        # Save to CSV file
        save_combined_dataset(combined_df)
        
        print(f"\nAnalysis completed successfully!")
        print(f"Dataset shape: {combined_df.shape}")
        print(f"Columns: {list(combined_df.columns)}")
        
        # DISPLAY COMPREHENSIVE SUMMARY TABLE
        display_summary_table(combined_df)
