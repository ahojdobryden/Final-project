from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth # Make sure this is installed: pip install selenium-stealth
import time
import json
import random

# --- Info pro Terku (tenhle script budu ještě upravovat)
# Jsou tam antibotikovy opatreni. Když runneš kód, tak se ti otevře okno prohlížeče a budeš muset vyřešit CAPTCHA a zavřít pop-up s adresou.
# Pak dej v terminálu Enter, aby se spustil scraping, měl by vyjet JSON s produkty, je jich jen 384 ale jenom


CHROMEDRIVER_PATH = r"C:\\Drivers\\chromedriver-win64\\chromedriver.exe"

# --- Selenium Options - Aggressive Anti-Detection ---
options = Options()
# NO --headless for manual CAPTCHA and to observe
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled") # Key anti-detection flag
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36") # Use a current, common UA
options.set_capability("acceptInsecureCerts", True)
# options.add_argument("--window-size=1920,1080") # Can sometimes help appear more human
# options.add_argument("--start-maximized")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# --- Apply selenium-stealth ---
stealth(driver,
        languages=["cs-CZ", "cs", "en-US", "en"],
        vendor="Google Inc.",
        platform="Win32", # Or your correct platform
        webgl_vendor="Intel Inc.", # Adjust if you know yours (e.g., from browserleaks.com/webgl)
        renderer="Intel Iris OpenGL Engine", # Adjust
        fix_hairline=True,
        run_on_insecure_origins=True
        )

main_dairy_url = "https://www.foodora.cz/darkstore/l1hl/foodora-market-chodovska/category/aebe6331-2bc7-4e3e-9e05-356d967c98de"

def human_like_scroll(scroll_attempts=7, min_pause=2.0, max_pause=3.5):
    """More human-like scrolling with variable pauses."""
    print("  - Starting human-like scroll_to_load_all...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(scroll_attempts):
        print(f"    - Scroll attempt {i+1}/{scroll_attempts}")
        # Scroll part of the way, not always to the absolute bottom, then a final full scroll
        if i < scroll_attempts -1:
            scroll_amount = random.uniform(0.6, 0.9) # scroll 60-90% of current view
            driver.execute_script(f"window.scrollBy(0, window.innerHeight * {scroll_amount});")
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Final full scroll

        time.sleep(random.uniform(min_pause, max_pause))
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height and i > 2 : # Give it a few scrolls to actually load more
            print("    - Reached bottom of page or no new content loaded after a few attempts.")
            break
        last_height = new_height
    print("  - Human-like scrolling complete.")


def scrape_all_products_from_single_page_load():
    print("  - Attempting to scrape all products from the current page...")
    products = []
    
    try:
        print("  - Waiting for product grid (ul.product-grid) to be visible (up to 30s)...")
        WebDriverWait(driver, 30).until( 
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.product-grid"))
        )
        time.sleep(random.uniform(1.5, 3.0)) # Extra pause after grid appears
        print("  - Product grid is visible. Proceeding with human-like scroll.")
        human_like_scroll() # Use the more human-like scroll

        # Iterate over each list item (<li>) in the product grid
        # Each <li> should represent one product card
        product_list_items = driver.find_elements(By.CSS_SELECTOR, "ul.product-grid > li")
        
        print(f"  - Found {len(product_list_items)} product list items (<li>) after scrolling.")
        
        for idx, list_item_card in enumerate(product_list_items):
            name = "Name not found"
            price_text = "Price not found" 
            unit_price_text = "Unit price not found"
            card_context = list_item_card

            try:
                # 1. Extract Name (within the card_context)
                try:
                    name_element = card_context.find_element(By.CSS_SELECTOR, "[data-testid='groceries-product-card-name']")
                    name = name_element.text.strip()
                except NoSuchElementException:
                    # This li might not be a product if name is missing
                    # print(f"    - Product name ([data-testid='groceries-product-card-name']) not found in card (index {idx}).")
                    continue # Skip this item if no name found

                # 2. Extract Price (within the card_context)
                try:
                    price_element = card_context.find_element(By.CSS_SELECTOR, "[data-testid='groceries-product-card-price']")
                    price_text = price_element.text.strip()
                except NoSuchElementException:
                    print(f"    - Price element ([data-testid='groceries-product-card-price']) NOT FOUND for product '{name}' (index {idx}). Item might be out of stock.")
                    price_text = "Price element missing" 
                
                # 3. Extract Unit Price (within the card_context)
                # Unit price is inside <p data-testid="comparison-price-content"> which is a child of the main <a> wrapper
                try:
                    main_link_wrapper = card_context.find_element(By.CSS_SELECTOR, "a.groceries-product-card-nav-wrapper")
                    unit_price_element = main_link_wrapper.find_element(By.CSS_SELECTOR, "[data-testid='comparison-price-content']")
                    unit_price_text = unit_price_element.text.strip()
                except NoSuchElementException: 
                    unit_price_text = None # Common for unit price to be missing
                
                if name and name != "Name not found": # Ensure name was actually found
                    products.append({
                        "name": name,
                        "price": price_text, 
                        "unit_price": unit_price_text 
                    })

            except Exception as e_card_parsing: 
                print(f"    - Broader error parsing one product card (index {idx}, current name: '{name}'): {e_card_parsing}")

    except TimeoutException: 
        print("  - Timed out waiting for product grid 'ul.product-grid'. Page might not have loaded them or selector is wrong.")
        print("  - Current URL when timed out:", driver.current_url)
        # print(f"Page source at timeout: {driver.page_source[:1000]}")
    except Exception as e:
        print(f"  - Error during product scraping (other exception): {e}")
    
    if not products:
        print("  - No products scraped from this page.")
    return products

def main():
    all_products = []
    
    print(f"Navigating to the main dairy section: {main_dairy_url}")
    driver.get(main_dairy_url)
    time.sleep(random.uniform(2.0, 4.0)) # Wait a bit for initial page elements to settle

    print("\n--- Initial Page Load & Manual Interaction ---")
    print("ACTION REQUIRED IN BROWSER:")
    print("1. Solve any CAPTCHA presented.")
    print("2. Close any address/delivery popups.")
    print("3. IMPORTANT: Scroll around the page a little bit yourself, maybe click a category filter then click back to 'All'. Mimic human browsing for 10-20 seconds.")
    print("   This helps build a 'human-like' interaction score before the script takes over scrolling.")
    input("Once the page is stable, and you're past initial checks, press Enter here to start automated scraping...")

    # Now that the page is "clean" from manual interaction, scrape everything
    products_on_page = scrape_all_products_from_single_page_load()
    all_products.extend(products_on_page)
    
    print(f"\n  - Scraped {len(products_on_page)} products from the page after full scroll.")

    driver.quit()
    
    output_filename = "foodora_all_dairy_products.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"\nScraping complete. Scraped {len(all_products)} products in total.")
    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()
# Note: This script is designed to be run in a local environment with a GUI.
# It will not work in headless mode without additional configuration.   