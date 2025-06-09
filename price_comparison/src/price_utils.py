def parse_price(price_str):
    """Convert Czech price format to float"""
    try:
        # Example input: "671.2 Kč/kg" or "83,90 Kč"
        number_part = price_str.split(' ')[0]
        return float(number_part.replace(',', '.'))
    except:
        return 0.0
