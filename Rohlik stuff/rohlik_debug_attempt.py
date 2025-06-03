from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium_stealth import stealth # Uncomment and pip install selenium-stealth if CAPTCHA loop persists
import time
import json
import random

CHROMEDRIVER_PATH = r"C:\Drivers\chromedriver-win64\chromedriver.exe"

# --- Selenium Options ---
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36") 
options.set_capability("acceptInsecureCerts", True)

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# --- Apply selenium-stealth (optional) ---
# stealth(driver, ...) # Your stealth config here

# --- ROHLIK.CZ SUBATEGORY URLS (FOR DEBUG, ONLY ONE URL) ---
ROHLIK_SUBCATEGORY_URLS = [
    {"name": "Sýry - Dárková balení", "url": "https://www.rohlik.cz/c300121865-darkove-baleni-a-speciality"}
]


def human_like_scroll(scroll_attempts=3, min_pause=1.0, max_pause=2.0): # Shorter scroll for single card debug
    print("  - DEBUG: Starting human-like scroll (short for debug)...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);") # Scroll a bit
    time.sleep(random.uniform(min_pause, max_pause))
    print("  - DEBUG: Short scroll complete.")


def scrape_rohlik_products_DEBUG_ONE_CARD(): # THIS IS THE UPDATED DEBUG FUNCTION
    current_url_for_debug = driver.current_url
    print(f"  - DEBUG: Attempting to scrape ONE card from URL: {current_url_for_debug}")
    products = []
    
    try:
        card_selector_for_wait = "div[data-test^='productCard-']"
        print(f"  - DEBUG: Waiting for at least one product card ('{card_selector_for_wait}') to be VISIBLE (up to 30s)...")
        try:
            WebDriverWait(driver, 30).until( 
                EC.visibility_of_element_located((By.CSS_SELECTOR, card_selector_for_wait))
            )
            print(f"  - DEBUG: SUCCESS - At least one product card is initially visible.")
        except TimeoutException:
            # Fallback if individual cards are slow, try the grid container from your image
            grid_selector_fallback = "div[data-test='products-grid']" 
            print(f"  - DEBUG: Initial card wait timed out. Trying fallback: waiting for '{grid_selector_fallback}' (up to 15s)...")
            try:
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, grid_selector_fallback))
                )
                print(f"  - DEBUG: SUCCESS - Fallback grid container ('{grid_selector_fallback}') is visible.")
            except TimeoutException:
                print(f"  - DEBUG: TIMEOUT - Neither product cards nor '{grid_selector_fallback}' became visible on {current_url_for_debug}.")
                return []

        # No extensive scrolling for single card debug, assume it's in view or loaded by initial scroll
        # human_like_scroll() 
        print("  - DEBUG: Skipping extensive scroll for single card debug. Assuming first card is loaded.")
        time.sleep(2) # Give a moment for JS

        product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-test^='productCard-']")
        print(f"  - DEBUG: Found {len(product_cards)} potential product cards on the page.")
        
        if not product_cards:
            print(f"  - DEBUG: CRITICAL - No product cards found at all on {current_url_for_debug}.")
            return []

        # --- PROCESS ONLY THE FIRST CARD ---
        card_context = product_cards[0] # This is the div[data-test^="productCard-"]
        idx = 0
        print(f"\n  --- DEBUG: Processing ONLY THE FIRST Card (index {idx + 1}) ---")
        print(f"    Card {idx+1} outerHTML (first 700 chars): {card_context.get_attribute('outerHTML')[:700]}...")
            
        name = "Name not found"
        price_str = "Price not found" 
        unit_price_str = "Unit price not found"
        package_amount_str = "Amount not found"
            
        link_wrapper_a = None
        try:
            print(f"    DEBUG: Trying to find main link wrapper 'a.sc-e9663433-1' in card {idx+1}...")
            link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a.sc-e9663433-1") 
            print(f"    DEBUG: Found main link wrapper (specific class): {link_wrapper_a.tag_name}")
        except NoSuchElementException:
            print(f"    DEBUG: Main link wrapper (a.sc-e9663433-1) not found. Trying generic 'a[href]'.")
            try:
                link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a[href]")
                print(f"    DEBUG: Found generic 'a[href]': {link_wrapper_a.tag_name}")
            except NoSuchElementException:
                print(f"    DEBUG: CRITICAL - No suitable <a> link wrapper found in card {idx+1}.")
        
        context_for_body = link_wrapper_a if link_wrapper_a else card_context
        if link_wrapper_a: print(f"    DEBUG: Context for name/price body will be the found <a> tag.")
        else: print(f"    DEBUG: Context for name/price body will be the main card_context div (as <a> wrapper was not found).")

        try:
            name_selector = "h3[data-test='productCard-body-name']"
            print(f"    DEBUG: Trying to find name with '{name_selector}' in body context...")
            name_element = context_for_body.find_element(By.CSS_SELECTOR, name_selector)
            name = name_element.get_attribute("title").strip()
            if not name: name = name_element.text.strip()
            print(f"    DEBUG: SUCCESS - Found name: '{name}'")
        except NoSuchElementException:
            print(f"    DEBUG: FAILURE - Product name ('{name_selector}') NOT FOUND in body context for card {idx + 1}.")
        
        try:
            price_no_selector = "span[data-test='productCard-body-price-priceNo']"
            print(f"    DEBUG: Trying to find price_no_span with '{price_no_selector}' in body context...")
            price_no_span = context_for_body.find_element(By.CSS_SELECTOR, price_no_selector)
            print(f"    DEBUG: Found price_no_span. HTML: {price_no_span.get_attribute('outerHTML')}")
            
            # Corrected JS for getting text from the first child span of price_no_span
            main_price_digits_js = "var firstInnerSpan = arguments[0].querySelector('span'); if (firstInnerSpan) return firstInnerSpan.textContent.trim(); else if (arguments[0].childNodes.length > 0 && arguments[0].childNodes[0].nodeType === Node.TEXT_NODE) return arguments[0].childNodes[0].nodeValue.trim(); return '';"
            main_price_digits = driver.execute_script(main_price_digits_js, price_no_span)
            print(f"    DEBUG: main_price_digits: '{main_price_digits}'")

            decimal_digits = ""
            try:
                sup_element = price_no_span.find_element(By.XPATH, "./sup")
                decimal_digits = sup_element.text.strip()
                print(f"    DEBUG: Found decimal_digits: '{decimal_digits}'")
            except NoSuchElementException: print(f"    DEBUG: No 'sup' for decimal digits found.")
            
            currency_selector = "span[data-test='productCard-body-price-currency']"
            currency_span = context_for_body.find_element(By.CSS_SELECTOR, currency_selector) 
            currency = currency_span.text.strip()
            print(f"    DEBUG: Found currency: '{currency}'")
            
            if main_price_digits and decimal_digits: price_str = f"{main_price_digits},{decimal_digits} {currency}"
            elif main_price_digits: price_str = f"{main_price_digits} {currency}"
            else: price_str = "Price parts missing"
            print(f"    DEBUG: Constructed price_str: '{price_str}'")
                    
        except NoSuchElementException as e:
            print(f"    DEBUG: One of the Price elements NOT FOUND for product '{name}'. Detail: {e}")
            price_str = "Price data missing (elements not found)"
        except Exception as e_price_extract: 
            print(f"    DEBUG: Other error extracting price details for '{name}': {e_price_extract}")
            price_str = "Price extraction error"
        
        try:
            footer_selector = "div.sc-90654762-0.fuXXWU" # Class from your image for the footer div
            print(f"    DEBUG: Trying to find footer_div with '{footer_selector}' in card_context (main productCard div)...")
            footer_div = card_context.find_element(By.CSS_SELECTOR, footer_selector)
            print(f"    DEBUG: Found footer_div.")
            try:
                unit_price_element = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-unitPrice']")
                unit_price_str = unit_price_element.text.strip()
                print(f"    DEBUG: Found unit_price: '{unit_price_str}'")
            except NoSuchElementException: 
                print(f"    DEBUG: Unit price element not found in footer.")
                unit_price_str = None 
            try:
                amount_element = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-amount']")
                package_amount_str = amount_element.text.strip()
                print(f"    DEBUG: Found amount: '{package_amount_str}'")
            except NoSuchElementException: 
                print(f"    DEBUG: Amount element not found in footer.")
                package_amount_str = None
        except NoSuchElementException:
            print(f"    DEBUG: Footer div ('{footer_selector}') not found for '{name}'.")
            unit_price_str = None
            package_amount_str = None

        if name and name != "Name not found":
            products.append({
                "name": name, "price": price_str, 
                "unit_price": unit_price_str, "package_amount": package_amount_str
            })
            print(f"    DEBUG: Appended product: {products[-1]}")
        else:
            print(f"    DEBUG: Did not append product for card {idx+1} because name was not found or empty.")

        print(f"\n  --- DEBUG: Finished processing the first card. Extracted: {len(products)} ---")

    except TimeoutException: 
        print(f"  - DEBUG: TIMEOUT waiting for initial product cards on {current_url_for_debug}.")
    except Exception as e:
        print(f"  - DEBUG: MAJOR ERROR during product scraping function for URL {current_url_for_debug}: {e}")
    
    if not products:
        print(f"  - DEBUG: FINAL - No products scraped from {current_url_for_debug}.")
    return products


def main():
    all_products = []
    # For this debug run, ROHLIK_SUBCATEGORY_URLS is already set globally to one URL.

    if not ROHLIK_SUBCATEGORY_URLS:
        print("ERROR: ROHLIK_SUBCATEGORY_URLS list is empty.")
        if driver: driver.quit()
        return

    # This loop will run only once for the debug setup
    for i, subcat_info in enumerate(ROHLIK_SUBCATEGORY_URLS):
        subcat_name = subcat_info.get("name", f"Unknown Subcategory {i+1}")
        subcat_url = subcat_info.get("url")

        if not subcat_url:
            print(f"Skipping subcategory '{subcat_name}' due to missing URL.")
            continue

        print(f"\n--- Processing Rohlik Subcategory {i+1}/{len(ROHLIK_SUBCATEGORY_URLS)}: '{subcat_name}' ---")
        print(f"Navigating to: {subcat_url}")
        try:
            driver.get(subcat_url)
            time.sleep(random.uniform(2.5, 4.5)) 

            # Re-enable manual prompt for this focused debug
            print("ACTION REQUIRED IN BROWSER (Rohlik.cz):")
            print(f"1. For subcategory '{subcat_name}': Accept COOKIES if prompted.")
            print("2. Close any LOGIN PROMPTS or other popups.")
            print("3. Solve any CAPTCHA if it appears.")
            print("4. IMPORTANT: Scroll around the page a little bit yourself, mimic human browsing for 10-20 seconds.")
            input(f"Once the page for '{subcat_name}' is stable and THE FIRST PRODUCT is visible, press Enter here to scrape ONLY THE FIRST CARD...")

            products_on_page = scrape_rohlik_products_DEBUG_ONE_CARD() # Call the DEBUG version
            
            for p in products_on_page: 
                p['subcategory_name'] = subcat_name
                p['subcategory_url'] = subcat_url
            all_products.extend(products_on_page)
            
            print(f"  - Scraped {len(products_on_page)} products from '{subcat_name}'.")
            
        except Exception as e_main_loop: 
            print(f"  - CRITICAL ERROR processing subcategory '{subcat_name}' ({subcat_url}): {e_main_loop}")
            try:
                driver.current_url 
            except:
                print("    WebDriver session seems to be closed. Stopping script.")
                break 
        
    if driver: 
        try:
            driver.quit()
        except: pass
    
    output_filename = "rohlik_DEBUG_ONE_CARD_dairy_products.json" # Different output for debug
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"\nDEBUG Scraping complete. Scraped {len(all_products)} products.")
    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()
