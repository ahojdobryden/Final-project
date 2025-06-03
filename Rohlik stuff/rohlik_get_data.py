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
# NO --headless for manual interaction
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
# stealth(driver,
#         languages=["cs-CZ", "cs", "en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         run_on_insecure_origins=True
#         )

# --- ROHLIK.CZ SUBATEGORY URLS ---
# YOU MUST POPULATE THIS LIST WITH YOUR SPECIFIC, LOWEST-LEVEL SUBCATEGORY URLS
ROHLIK_SUBCATEGORY_URLS = [
    {"name": "Sýry - Dárková balení", "url": "https://www.rohlik.cz/c300121865-darkove-baleni-a-speciality"},
    {"name": "Plátkové sýry - Eidam", "url": "https://www.rohlik.cz/c300114177-eidam"},
    {"name": "Plátkové sýry - Cheddar", "url": "https://www.rohlik.cz/c300114183-cheddar"},
    {"name": "Plátkové sýry - Gouda", "url": "https://www.rohlik.cz/c300114179-gouda"},
    {"name": "Plátkové sýry - Ementálský typ", "url": "https://www.rohlik.cz/c300114181-ementalsky-typ"},
    {"name": "Plátkové sýry - Maasdam", "url": "https://www.rohlik.cz/c300114187-maasdam"},
    {"name": "Plátkové sýry - Ostatní", "url": "https://www.rohlik.cz/c300124083-ostatni"},
    {"name": "Sýry dárková balení - BIO a farmářské", "url": "https://www.rohlik.cz/c300123522-bio-a-farmarske"},
    {"name": "Sýry dárková balení - Ovčí", "url": "https://www.rohlik.cz/c300123523-ovci"},
    {"name": "Sýry dárková balení - Kozí", "url": "https://www.rohlik.cz/c300123525-kozi"},
    {"name": "Sýry - Smetanové", "url": "https://www.rohlik.cz/c300114175-smetanove"},
    {"name": "Sýry - Cottage", "url": "https://www.rohlik.cz/c300114171-cottage"},
    {"name": "Sýry - Tavené", "url": "https://www.rohlik.cz/c300123488-tavene"},
    {"name": "Čerstvě krájené - Strouhané", "url": "https://www.rohlik.cz/c300123217-cerstve-krajene-strouhane-syry"},
    {"name": "Čerstvě krájené - Výkroje", "url": "https://www.rohlik.cz/c300120610-cerstve-krajene-syrove-vykroje"},
    {"name": "Čerstvě krájené - Tapas", "url": "https://www.rohlik.cz/c300121397-cerstve-krajene-syry-tapas"},
    {"name": "Čerstvě krájené - Plátkové", "url": "https://www.rohlik.cz/c300120609-cerstve-krajene-platkove-syry"},
    {"name": "Sýry - Grana Padano", "url": "https://www.rohlik.cz/c300124079-grana-padano"},
    {"name": "Sýry - Pecorino", "url": "https://www.rohlik.cz/c300124082-pecorino"},
    {"name": "Sýry - Parmazánového typu", "url": "https://www.rohlik.cz/c300124080-parmazanoveho-typu"},
    {"name": "Sýry - Reggiano", "url": "https://www.rohlik.cz/c300124081-parmiggiano-reggiano"},
    {"name": "Sýry - Bločky a storuhané - Eidam", "url": "https://www.rohlik.cz/c300124073-eidam"},
    {"name": "Sýry - Bločky a storuhané - Cheddar", "url": "https://www.rohlik.cz/c300124077-cheddar"},
    {"name": "Sýry - Bločky a storuhané - Ementálský typ", "url": "https://www.rohlik.cz/c300124075-ementalsky-typ"},
    {"name": "Sýry - Bločky a storuhané - Ostatní", "url": "https://www.rohlik.cz/c300124078-ostatni"},
    {"name": "Sýry - Bločky a storuhané - Gouda", "url": "https://www.rohlik.cz/c300124076-gouda"},
    {"name": "Sýry - Bločky a storuhané - Strouhané", "url": "https://www.rohlik.cz/c300123498-strouhane"},
    {"name": "Sýry - Salátové - Feta", "url": "https://www.rohlik.cz/c300124067-feta"},
    {"name": "Sýry - Salátové - Mozzarella", "url": "https://www.rohlik.cz/c300124068-mozzarella-burrata-a-ricotta"},
    {"name": "Sýry - Salátové - Salátové", "url": "https://www.rohlik.cz/c300124069-salatove-syry"},
    {"name": "Sýry - Plísňové", "url": "https://www.rohlik.cz/c300123509-plisnove-a-zrajici"},
    {"name": "Sýry - Uzené", "url": "https://www.rohlik.cz/c300123510-parene-a-uzene"},
    {"name": "Sýry - No gril", "url": "https://www.rohlik.cz/c300124071-na-gril-a-panev"},
    {"name": "Sýry - Fondue", "url": "https://www.rohlik.cz/c300124072-fondue-a-raclette"},
    {"name": "Sýry - Pobaltské", "url": "https://www.rohlik.cz/c300120681-pobaltske"},
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


def human_like_scroll(scroll_attempts=10, min_pause=2.0, max_pause=4.0): # Default scroll for full page
    print("  - Starting human-like scroll_to_load_all...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    no_change_count = 0
    for i in range(scroll_attempts):
        # print(f"    - Scroll attempt {i+1}/{scroll_attempts}") # Verbose
        if i < scroll_attempts - 2: 
            scroll_amount = random.uniform(0.7, 0.95)
            driver.execute_script(f"window.scrollBy(0, window.innerHeight * {scroll_amount});")
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(random.uniform(min_pause, max_pause))
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            no_change_count +=1
            if no_change_count >= 3 : 
                # print("    - Reached bottom of page or no new content loaded after multiple attempts.")
                break
        else:
            no_change_count = 0 
        last_height = new_height
    print("  - Human-like scrolling complete.")

def scrape_rohlik_products_from_current_page(): # THIS IS THE RESTORED FUNCTION
    current_url_for_debug = driver.current_url
    print(f"  - Attempting to scrape Rohlik products from URL: {current_url_for_debug}")
    products = []
    
    try:
        card_selector_for_wait = "div[data-test^='productCard-']"
        # print(f"  - Waiting for at least one product card ('{card_selector_for_wait}') to be VISIBLE (up to 30s)...") # Less verbose
        try:
            WebDriverWait(driver, 30).until( 
                EC.visibility_of_element_located((By.CSS_SELECTOR, card_selector_for_wait))
            )
            # print(f"  - SUCCESS: At least one product card is initially visible.")
        except TimeoutException:
            grid_selector_fallback = "div[data-test='products-grid']" 
            # print(f"  - Initial card wait timed out. Trying fallback: waiting for '{grid_selector_fallback}' (up to 15s)...")
            try:
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, grid_selector_fallback))
                )
                # print(f"  - SUCCESS: Fallback grid container ('{grid_selector_fallback}') is visible.")
            except TimeoutException:
                print(f"  - TIMEOUT: Neither product cards nor '{grid_selector_fallback}' became visible on {current_url_for_debug}.")
                return []

        time.sleep(random.uniform(2.0, 3.5)) 
        print("  - Proceeding with human-like scroll to load all products.")
        human_like_scroll() 

        product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-test^='productCard-']")
        print(f"  - Found {len(product_cards)} potential product cards after scrolling.")
        
        if not product_cards:
            print(f"  - CRITICAL: No product cards found on {current_url_for_debug} even after scroll.")
            return []

        for idx, card_context in enumerate(product_cards):
            name = "Name not found"
            price_str = "Price not found" 
            unit_price_str = "Unit price not found"
            package_amount_str = "Amount not found"
            
            link_wrapper_a = None
            try:
                link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a.sc-e9663433-1") 
            except NoSuchElementException:
                try: 
                    link_wrapper_a = card_context.find_element(By.CSS_SELECTOR, "a[href]") 
                except NoSuchElementException:
                    pass 
            
            context_to_search_body = link_wrapper_a if link_wrapper_a else card_context

            try:
                name_element = context_to_search_body.find_element(By.CSS_SELECTOR, "h3[data-test='productCard-body-name']")
                name = name_element.get_attribute("title").strip()
                if not name: name = name_element.text.strip()
                if not name:
                    continue 
            except NoSuchElementException:
                continue 

            try:
                price_no_span = context_to_search_body.find_element(By.CSS_SELECTOR, "span[data-test='productCard-body-price-priceNo']")
                main_price_digits_js = "var firstInnerSpan = arguments[0].querySelector('span'); if (firstInnerSpan) return firstInnerSpan.textContent.trim(); else if (arguments[0].childNodes.length > 0 && arguments[0].childNodes[0].nodeType === Node.TEXT_NODE) return arguments[0].childNodes[0].nodeValue.trim(); return '';"
                main_price_digits = driver.execute_script(main_price_digits_js, price_no_span)

                decimal_digits = ""
                try:
                    sup_element = price_no_span.find_element(By.XPATH, "./sup")
                    decimal_digits = sup_element.text.strip()
                except NoSuchElementException: pass
                
                currency_span = context_to_search_body.find_element(By.CSS_SELECTOR, "span[data-test='productCard-body-price-currency']")
                currency = currency_span.text.strip()
                
                if main_price_digits and decimal_digits: price_str = f"{main_price_digits},{decimal_digits} {currency}"
                elif main_price_digits: price_str = f"{main_price_digits} {currency}"
                else: price_str = "Price parts missing"
                        
            except NoSuchElementException:
                price_str = "Price data missing"
            except Exception as e_price_extract: 
                # print(f"    - Error extracting price details for '{name}' (index {idx}): {e_price_extract}") # Optional debug
                price_str = "Price extraction error"
            
            try:
                footer_div = card_context.find_element(By.CSS_SELECTOR, "div.sc-90654762-0.fuXXWU") 
                try:
                    unit_price_element = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-unitPrice']")
                    unit_price_str = unit_price_element.text.strip()
                except NoSuchElementException: unit_price_str = None 
                try:
                    amount_element = footer_div.find_element(By.CSS_SELECTOR, "p[data-test='productCard-footer-amount']")
                    package_amount_str = amount_element.text.strip()
                except NoSuchElementException: package_amount_str = None
            except NoSuchElementException:
                unit_price_str = None
                package_amount_str = None

            if name and name != "Name not found":
                products.append({
                    "name": name, "price": price_str, 
                    "unit_price": unit_price_str, "package_amount": package_amount_str
                })

        print(f"\n  --- Finished processing {len(product_cards)} cards. Total products extracted: {len(products)} ---")

    except TimeoutException: 
        print(f"  - TIMEOUT waiting for initial product cards or grid on {current_url_for_debug}.")
    except Exception as e:
        print(f"  - MAJOR ERROR during product scraping function for URL {current_url_for_debug}: {e}")
    
    if not products:
        print(f"  - FINAL: No products scraped from {current_url_for_debug}.")
    return products

def main():
    all_products = []
    
    if not ROHLIK_SUBCATEGORY_URLS:
        print("ERROR: ROHLIK_SUBCATEGORY_URLS list is empty.")
        if driver: driver.quit()
        return

    # Initial interaction for the VERY FIRST URL in the list
    if ROHLIK_SUBCATEGORY_URLS:
        first_subcat_info = ROHLIK_SUBCATEGORY_URLS[0]
        print(f"\n--- Initial Setup for Rohlik.cz: '{first_subcat_info['name']}' ---")
        print(f"Navigating to: {first_subcat_info['url']}")
        try:
            driver.get(first_subcat_info['url'])
            time.sleep(random.uniform(2.5, 4.5)) 

            # Keep the manual prompt for the first page at least.
            print("ACTION REQUIRED IN BROWSER (Rohlik.cz - First Page Only):")
            print("1. Accept COOKIES if the banner appears.")
            print("2. Close any LOGIN PROMPTS or other popups.")
            print("3. Solve any CAPTCHA if it appears.")
            print("4. IMPORTANT: Scroll around the page a little bit yourself, mimic human browsing for 10-20 seconds.")
            input(f"Once the page for '{first_subcat_info['name']}' is stable and products are visible, press Enter to begin scraping all listed categories...")
        except Exception as e_initial_load:
            print(f"  - CRITICAL ERROR during initial load of '{first_subcat_info['name']}': {e_initial_load}")
            print("    Cannot proceed. Please check network or URL.")
            if driver: driver.quit()
            return

    for i, subcat_info in enumerate(ROHLIK_SUBCATEGORY_URLS):
        subcat_name = subcat_info.get("name", f"Unknown Subcategory {i+1}")
        subcat_url = subcat_info.get("url")

        if not subcat_url:
            print(f"Skipping subcategory '{subcat_name}' due to missing URL.")
            continue

        print(f"\n--- Processing Rohlik Subcategory {i+1}/{len(ROHLIK_SUBCATEGORY_URLS)}: '{subcat_name}' ---")
        
        if i > 0: # For subsequent URLs, navigate
            print(f"Navigating to: {subcat_url}")
            try:
                driver.get(subcat_url)
                time.sleep(random.uniform(2.0, 3.5)) 
                # If you find CAPTCHAs ARE appearing for sub-pages, re-add the input() prompt here:
                # print(f"ACTION REQUIRED: Solve CAPTCHA for '{subcat_name}' if any, then press Enter...")
                # input("Press Enter to continue scraping this subcategory...")
                print(f"  (Assuming no new CAPTCHA for '{subcat_name}'. Proceeding to scrape.)")
            except Exception as e_nav:
                print(f"  - ERROR navigating to '{subcat_name}' ({subcat_url}): {e_nav}")
                print("    Skipping this subcategory.")
                continue 
        else: # First URL, already loaded and (manually) cleared
            print(f"  (Already on page for '{subcat_name}'. Proceeding to scrape.)")

        products_on_page = scrape_rohlik_products_from_current_page() 
        
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
