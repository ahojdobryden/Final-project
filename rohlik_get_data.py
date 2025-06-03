from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException 
# from selenium_stealth import stealth # Uncomment and pip install selenium-stealth if CAPTCHA loop persists
import time
import json
import random

CHROMEDRIVER_PATH = r"C:\\Drivers\\chromedriver-win64\\chromedriver.exe" # Your chromedriver path

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

# --- ROHLIK.CZ SUBATEGORY URLS ---
ROHLIK_SUBCATEGORY_URLS = [
    {"name": "Sýry - Dárková balení", "url": "https://www.rohlik.cz/c300121865-darkove-baleni-a-speciality"},
    {"name": "Plátkové sýry", "url": "https://www.rohlik.cz/c300105028-platkove"},
    {"name": "Sýry BIO a farmářské", "url": "https://www.rohlik.cz/c300123521-bio-farmarske-ovci-a-kozi"},
    {"name": "Sýry - Smetanové", "url": "https://www.rohlik.cz/c300105031-smetanove-cottage-a-tavene"},
    {"name": "Čerstvě krájené", "url": "https://www.rohlik.cz/c300120608-cerstve-krajene-syry"},
    {"name": "Sýry - Parmazán, Grana Padano, Pecorino", "url": "https://www.rohlik.cz/c300105040-parmazan-grana-padano-a-pecorino"},
    {"name": "Sýry - Bločky a storuhané", "url": "https://www.rohlik.cz/c300105027-blocky-a-strouhane"},
    {"name": "Sýry - Salátové", "url": "https://www.rohlik.cz/c300124066-mozzarella-ricotta-a-salatove-syry"},
    {"name": "Sýry - Plísňové", "url": "https://www.rohlik.cz/c300123507-plisnove-zrajici-parene-a-uzene"},
    {"name": "Sýry - Na gril a Fondue", "url": "https://www.rohlik.cz/c300124070-na-gril-fondue-a-raclette"},
    {"name": "Sýry - Zahraniční", "url": "https://www.rohlik.cz/c300114329-zahranicni"},
    {"name": "Sýry - K vínu", "url": "https://www.rohlik.cz/c300122648-syry-k-vinu"},
    {"name": "Sýry - Snacky", "url": "https://www.rohlik.cz/c300124065-syrove-snacky-a-pro-deti"},
    {"name": "Majonézy", "url": "https://www.rohlik.cz/c300105060-majonezy"},
    {"name": "Dresingy", "url": "https://www.rohlik.cz/c300105061-salatove-dresingy"},
    {"name": "Tatarské omáčky", "url": "https://www.rohlik.cz/c300105061-salatove-dresingy"},
    {"name": "Jogurty - Ochucené", "url": "https://www.rohlik.cz/c300105010-ochucene"},
    {"name": "Jogurty - Dětské dezerty", "url": "https://www.rohlik.cz/c300123542-detske-dezerty-tycinky-a-rezy"},
    {"name": "Jogurty - Tvarohov dezerty", "url": "https://www.rohlik.cz/c300123535-tvarohove-dezerty-a-termixy"},
    {"name": "Jogurty - Bílé", "url": "https://www.rohlik.cz/c300105009-bile"},
    {"name": "Jogurty - BIO a farmářské", "url": "https://www.rohlik.cz/c300105070-bio-a-farmarske"},
    {"name": "Jogurty - Mléčné", "url": "https://www.rohlik.cz/c300123555-mlecne-ryze-krupice-pudingy-a-dezerty"},
    {"name": "Jogurty - Rodinná balení", "url": "https://www.rohlik.cz/c300123550-rodinna-baleni-a-jogurty-ve-skle"},
    {"name": "Jogurty - Řecké", "url": "https://www.rohlik.cz/c300123532-recke-reckeho-typu-a-skyry"},
    {"name": "Máslo - Máslo", "url": "https://www.rohlik.cz/c300105049-maslo"},
    {"name": "Máslo - Ghee", "url": "https://www.rohlik.cz/c300105049-maslo"},
    {"name": "Máslo - Pomazánkové", "url": "https://www.rohlik.cz/c300105050-pomazankove"},
    {"name": "Máslo - Kitchin", "url": "https://www.rohlik.cz/c300122004-kitchin"},
    {"name": "Máslo - Margaríny", "url": "https://www.rohlik.cz/c300122004-kitchin"},
    {"name": "Speciální - A2 Mléko", "url": "https://www.rohlik.cz/c300122516-vyrobky-z-a2-mleka"},
    {"name": "Speciální - Bez Laktózy", "url": "https://www.rohlik.cz/c300121233-jogurty-a-mlecne-dezerty-bez-laktozy"},
    {"name": "Speciální - Tvarohy bez alktózy", "url": "https://www.rohlik.cz/c300121237-tvarohy-bez-laktozy"},
    {"name": "Speciální - High protein", "url": "https://www.rohlik.cz/c300123064-high-protein"},
    {"name": "Speciální - Máslo bez laktózy", "url": "https://www.rohlik.cz/c300121235-maslo-a-tuky-bez-laktozy"},
    {"name": "Speciální - Mléčné nápoje bez laktózy", "url": "https://www.rohlik.cz/c300121234-mleko-a-mlecne-napoje-bez-laktozy"},
    {"name": "Speciální - Sýry bez laktózy", "url": "https://www.rohlik.cz/c300121232-syry-bez-laktozy"},
    {"name": "Speciální - Smetany bez laktózy", "url": "https://www.rohlik.cz/c300121236-smetany-a-slehacky-bez-laktozy"},
    {"name": "Mléčné - Čerstvé", "url": "https://www.rohlik.cz/c300105002-cerstve"},
    {"name": "Mléčné - Kefíry", "url": "https://www.rohlik.cz/c300105007-kefiry-a-zakys"},
    {"name": "Mléčné - Pro děti", "url": "https://www.rohlik.cz/c300114403-pro-deti"},
    {"name": "Mléčné - Trvanlivé", "url": "https://www.rohlik.cz/c300105003-trvanlive"},
    {"name": "Mléčné - Jogurtové nápoje", "url": "https://www.rohlik.cz/c300105005-mlecne-a-jogurtove-napoje"},
    {"name": "Mléčné - Rostlinné nápoje", "url": "https://www.rohlik.cz/c300105006-rostlinne-napoje"},
    {"name": "Mléčné - Farmářské mléko", "url": "https://www.rohlik.cz/c300105069-bio-a-farmarske-mleko-a-mlecne-napoje"},
    {"name": "Mléčné - Kondenzované", "url": "https://www.rohlik.cz/c300105004-kondenzovane"},
    {"name": "Smetany, šlehačky, tvarohy - Tvarohy", "url": "https://www.rohlik.cz/c300123065-tvarohy"},
    {"name": "Smetany, šlehačky, tvarohy - Zakysané smetany", "url": "https://www.rohlik.cz/c300105022-zakysane-smetany"},
    {"name": "Smetany, šlehačky, tvarohy - Našlehané krémy", "url": "https://www.rohlik.cz/c300122373-naslehane-kremy"},
    {"name": "Smetany, šlehačky, tvarohy - Šlehačky", "url": "https://www.rohlik.cz/c300105024-smetany-ke-slehani-a-slehacky"},
    {"name": "Smetany, šlehačky, tvarohy - Do kávy", "url": "https://www.rohlik.cz/c300105025-smetany-do-kavy"},
    {"name": "Smetany, šlehačky, tvarohy - Rostlinné", "url": "https://www.rohlik.cz/c300114405-rostlinne-alternativy-smetany"},
    {"name": "Smetany, šlehačky, tvarohy - Na vaření", "url": "https://www.rohlik.cz/c300105023-smetany-na-vareni"},
    {"name": "Smetany, šlehačky, tvarohy - BIO", "url": "https://www.rohlik.cz/c300105072-bio-a-farmarske-smetany-a-slehacky"}
]

# --- TARGET PRODUCT NAME FOR DEBUGGING (Set to None or "" when not debugging a specific card) ---
DEBUG_TARGET_PRODUCT_NAME_CONTAINS = None 

def gentle_scroll_and_wait(num_gentle_scrolls=1, pause_duration=1.5):
    try:
        for i in range(num_gentle_scrolls):
            driver.execute_script(f"window.scrollBy(0, {random.randint(100, 200)});") 
            time.sleep(pause_duration)
    except Exception as e_gs:
        print(f"    - Error during gentle_scroll_and_wait: {e_gs}")


def scrape_rohlik_products_from_current_page(expected_products_on_page=None): # THIS IS THE UPDATED FUNCTION
    current_url_for_debug = driver.current_url
    print(f"  - Attempting to scrape Rohlik products (chunked) from URL: {current_url_for_debug}")
    
    all_products_on_page = []
    processed_card_data_tests = set() 

    # print("  - Performing initial gentle scroll to settle page...") # Less verbose
    gentle_scroll_and_wait()

    scroll_attempts = 0
    max_scroll_attempts = 25 
    no_new_products_strikes = 0
    max_no_new_products_strikes = 2 # Stop after 2 consecutive scrolls yield no new products

    while scroll_attempts < max_scroll_attempts:
        scroll_attempts += 1
        
        current_live_cards = []
        try:
            time.sleep(0.25) 
            current_live_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-test^='productCard-']")
        except Exception as e_find_live: 
            print(f"    ERROR finding live cards in chunk {scroll_attempts}: {e_find_live}. Stopping.")
            break
            
        new_products_this_chunk = 0
        if not current_live_cards and scroll_attempts > max_no_new_products_strikes: 
            # print(f"    No live cards found for {max_no_new_products_strikes} consecutive checks in chunk {scroll_attempts}. Assuming end of page.") # Verbose
            no_new_products_strikes +=1
        
        for card_idx, card_context in enumerate(current_live_cards):
            try:
                card_data_test_id = card_context.get_attribute("data-test")
                if not card_data_test_id or card_data_test_id in processed_card_data_tests:
                    continue 

                # --- Condensed Parsing Logic (same as your working version for one card) ---
                name, price_str, unit_price_str, package_amount_str = "Name not found", "Price not found", "Unit not found", "Amount not found"
                link_wrapper_a = None
                try: link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a.sc-e9663433-1")
                except: 
                    try: link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a[href]")
                    except: pass
                context_to_search_body = link_wrapper_a if link_wrapper_a else card_context
                try:
                    name_element = context_to_search_body.find_element(By.CSS_SELECTOR, "h3[data-test='productCard-body-name']")
                    name = name_element.get_attribute("title").strip() or name_element.text.strip()
                    if not name: continue
                except: continue
                try:
                    price_no_span = context_to_search_body.find_element(By.CSS_SELECTOR, "span[data-test='productCard-body-price-priceNo']")
                    js_price = "var s=arguments[0].querySelector('span'); return s?s.textContent.trim():(arguments[0].childNodes.length>0&&arguments[0].childNodes[0].nodeType===Node.TEXT_NODE?arguments[0].childNodes[0].nodeValue.trim():'');"
                    main_price_digits = driver.execute_script(js_price, price_no_span)
                    decimal_digits = ""
                    try: decimal_digits = price_no_span.find_element(By.XPATH, "./sup").text.strip()
                    except: pass
                    currency = context_to_search_body.find_element(By.CSS_SELECTOR, "span[data-test='productCard-body-price-currency']").text.strip()
                    if main_price_digits and decimal_digits: price_str = f"{main_price_digits},{decimal_digits} {currency}"
                    elif main_price_digits: price_str = f"{main_price_digits} {currency}"
                    else: price_str = "Price parts missing"
                except: price_str = "Price data missing"
                try:
                    footer_div = card_context.find_element(By.CSS_SELECTOR, "div.sc-90654762-0.fuXXWU")
                    try: unit_price_str = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-unitPrice']").text.strip()
                    except: unit_price_str = None
                    try: package_amount_str = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-amount']").text.strip()
                    except: package_amount_str = None
                except: unit_price_str, package_amount_str = None, None
                
                if name and name != "Name not found":
                    all_products_on_page.append({
                        "name": name, "price": price_str,
                        "unit_price": unit_price_str, "package_amount": package_amount_str,
                        "data_test_id": card_data_test_id 
                    })
                    processed_card_data_tests.add(card_data_test_id)
                    new_products_this_chunk += 1
            except StaleElementReferenceException: continue 
            except Exception as e_card_parse_final:
                print(f"    Unexpected error parsing card {card_data_test_id if 'card_data_test_id' in locals() else 'unknown ID'} in chunk {scroll_attempts}: {e_card_parse_final}")

        print(f"    Chunk {scroll_attempts}: Processed {new_products_this_chunk} new products. Total unique products so far: {len(all_products_on_page)}")
        
        if new_products_this_chunk == 0: 
            no_new_products_strikes += 1
            # print(f"    No new products found in this chunk. Strike {no_new_products_strikes}/{max_no_new_products_strikes}.") # Verbose
        else: 
            no_new_products_strikes = 0 

        if no_new_products_strikes >= max_no_new_products_strikes:
            print(f"    Reached max strikes ({max_no_new_products_strikes}) for no new products. Assuming end of page content.")
            break
        
        if expected_products_on_page and len(all_products_on_page) >= expected_products_on_page:
            # print(f"    Reached/exceeded expected product count ({len(all_products_on_page)}/{expected_products_on_page}). Stopping scroll.") # Verbose
            break

        try:
            driver.execute_script("window.scrollBy(0, window.innerHeight * 0.80);") 
            time.sleep(random.uniform(1.8, 2.8)) 
        except Exception as e_scroll_final:
            print(f"    Error during scroll in chunk {scroll_attempts}: {e_scroll_final}. Stopping.")
            break

    final_products_dict = {p['data_test_id']: p for p in all_products_on_page}
    final_product_list = list(final_products_dict.values())
    for p in final_product_list: p.pop('data_test_id', None) 

    print(f"\n  --- Finished chunked scraping. Total unique products extracted: {len(final_product_list)} ---")
    return final_product_list


def main():
    all_products = []
    
    if not ROHLIK_SUBCATEGORY_URLS:
        print("ERROR: ROHLIK_SUBCATEGORY_URLS list is empty.")
        if driver: driver.quit()
        return

    if ROHLIK_SUBCATEGORY_URLS:
        first_subcat_info = ROHLIK_SUBCATEGORY_URLS[0]
        print(f"\n--- Initial Setup for Rohlik.cz: '{first_subcat_info['name']}' ---")
        print(f"Navigating to: {first_subcat_info['url']}")
        try:
            driver.get(first_subcat_info['url'])
            time.sleep(random.uniform(2.5, 4.5)) 
            print("ACTION REQUIRED IN BROWSER (Rohlik.cz - First Page Only):")
            print("1. Accept COOKIES if the banner appears.")
            print("2. Close any LOGIN PROMPTS or other popups.")
            print("3. Solve any CAPTCHA if it appears.")
            print("4. IMPORTANT: MANUALLY SCROLL TO THE BOTTOM of this first page to ensure all initial products are loaded for Selenium.")
            input(f"Once the page for '{first_subcat_info['name']}' is stable AND YOU HAVE MANUALLY SCROLLED, press Enter to begin scraping...")
        except Exception as e_initial_load:
            print(f"  - CRITICAL ERROR during initial load of '{first_subcat_info['name']}': {e_initial_load}")
            print("    Cannot proceed. Please check network or URL.")
            if driver: driver.quit()
            return

    for i, subcat_info in enumerate(ROHLIK_SUBCATEGORY_URLS):
        subcat_name = subcat_info.get("name", f"Unknown Subcategory {i+1}")
        subcat_url = subcat_info.get("url")
        # expected_count is no longer strictly needed by scrape_rohlik_products_from_current_page for stopping
        # but can be used if you want to pass it for an optional early exit.
        expected_count = subcat_info.get("expected_count") 

        if not subcat_url:
            print(f"Skipping subcategory '{subcat_name}' due to missing URL.")
            continue
        print(f"\n--- Processing Rohlik Subcategory {i+1}/{len(ROHLIK_SUBCATEGORY_URLS)}: '{subcat_name}' ---")
        
        if i > 0: 
            print(f"Navigating to: {subcat_url}")
            try:
                driver.get(subcat_url)
                time.sleep(random.uniform(2.0, 3.5)) 
                print(f"  (MANUALLY SCROLL THIS PAGE '{subcat_name}' FULLY IF NEEDED, then implicitly continuing to scrape.)")
            except Exception as e_nav:
                print(f"  - ERROR navigating to '{subcat_name}' ({subcat_url}): {e_nav}")
                print("    Skipping this subcategory.")
                continue 
        else: 
            print(f"  (Already on page for '{subcat_name}'. Proceeding to scrape.)")

        # Pass expected_count if you have it and want the optional early exit
        products_on_page = scrape_rohlik_products_from_current_page(expected_products_on_page=expected_count) 
        
        for p in products_on_page: 
            p['subcategory_name'] = subcat_name
            p['subcategory_url'] = subcat_url
        all_products.extend(products_on_page)
        
        print(f"  - Scraped {len(products_on_page)} products from '{subcat_name}'.")
        
        if i < len(ROHLIK_SUBCATEGORY_URLS) - 1:
            time.sleep(random.uniform(3.0, 5.5)) 

    if driver: 
        try:
            driver.quit()
        except: pass
    
    output_filename = "rohlik_dairy_products_multi_cat.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"\nScraping complete. Scraped {len(all_products)} products in total from Rohlik.cz.")
    print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()