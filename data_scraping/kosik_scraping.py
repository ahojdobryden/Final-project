from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# Path to your ChromeDriver binary
CHROMEDRIVER_PATH = "/Users/kucer/Downloads/chromedriver-mac-arm64/chromedriver"  # Update this to your local path


# Set Chrome options
options = Options()
options.add_argument("--headless")  # Runs Chrome in headless mode (no GUI) pak odkomentit
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Setup the Chrome service
service = Service(CHROMEDRIVER_PATH)

# Start the WebDriver
#driver = webdriver.Chrome(service=service, options=options)

# The target URL for the API request
url = "https://www.kosik.cz/api/front/page/products/flexible"
basic_url = "https://www.kosik.cz"  # Base URL for constructing full links

# Parameters for the GET request
params = {
    "vendor": "1",
    "slug": "c898-mlecne-a-chlazene",
    "limit": 30,
    "search_term": "",
    "page_display": "horizontal",
    "platform": "web"
}

# Headers that mimic the browser request
headers = {
    "accept": "*/*",
    "accept-language": "cs,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://www.kosik.cz/c898-mlecne-a-chlazene",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-361cd6e5063444884f47e00f86f27604-de11cf60cd96a98d-01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# Cookies for the request
cookies = {
    "consentPreferences": '{"timestamp":"2025-04-15T11:42:12.140Z","version":1,"functional_storage":"granted","analytics_storage":"denied","personalization_storage":"denied","ad_storage":"denied","ad_user_data":"denied","ad_personalization":"denied"}',
    "_nss": "1",
    "lbuid": "250428|572777531998",
    "X-Ksp-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImtpZDEifQ.eyJzdWIiOiIxNzcyODA5MDYiLCJzY3AiOiIxIiwiY2F0IjoxNzQ1ODU1OTIzLCJpYXQiOjE3NDU4NTU5MjMsImlzcyI6InBjeiIsImV4cCI6MTc0NjQ2MDcyM30.e40lZ6mnvb8VwXwbzsSWYYpgRfsHcL0isaVJUGfaAHPRWXkyMigWiHkG2rdT_EBOzuzjlCo0wTyXlFshOhYRlT859vUVd3FtINqacp4a48mP7OPNiGS_F4qIhDqL5fEGW2Y08wyJOKGsudDQyJagTXtgQWN9dUYfsISh-I6krv43olWqJOR5jhB_XA9OFol9Pp58kviiVTgEHPLQ9EaWYF0PNDt-Gfv6Xw0E6RS3yK4QqOAae_9CUyU15-KGQWb2QSZNMwM-FRnOlBiBSX7d6ltnGodNI6DE2-ZHiKXDoLRDYyKqkOyKyhMJVIkVq-5h4WjPLKHwSJ8ExW5irM4grP7v_6SMteQozFqtiEDINBVAfHmNFrxOBO6taniU-vJW4kZ3eZUMNheFhWGhNn2BGcSkYA-mzycZY2w4YxFGwBKlRYdgl_2aeu5K0ywP9z5brD0fNmbT0ml8v2OEbq-MOYcvO0o0KtTi_MoJsh8EmQvMWHwjSq8yUUeHJUInEAxh"
}
##################
def get_links(api_url, params, headers, base_url):
    response = requests.get(api_url, params=params, headers=headers)
    data = response.json()
    links = []
    for item in data.get("subCategories", []):
        relative_url = item.get("url")
        if relative_url:
            links.append(f"{base_url}{relative_url}")
    return links

def scrape_products_from_link(driver, link, subcat_name):
    driver.get(link)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//article[@data-cnstrc-item-name]'))
    )
    # Load all products
    while True:
        try:
            wait = WebDriverWait(driver, 5)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Načíst další')]")))
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
        except Exception:
            break
##################

# Sending the GET request with the necessary parameters, headers, and cookies
# response = requests.get(url, params=params, headers=headers, cookies=cookies)
response = requests.get(url, params=params, headers=headers)
data = response.json()  # Parse the JSON response
# Checking the status code of the response
#print(data)

links = []
data_kosik = {}
data_kosik_subcats = []

for key,value in data.items():
    if key == "subCategories":
        data_url = value
        #links.append(f'{basic_url}{key.get('link')}')

for item in data_url:
    relative_url = item.get("url")
    if relative_url:
        full_url = f"{basic_url}{relative_url}"
        links.append(full_url)
print(f'THESE ARE THE LINKS: {links}.')

start_time = time.time()
for i,link in enumerate(links):
    driver = webdriver.Chrome(service=service, options=options)
    subcategory_name_list = (link.split("/")[-1]).split("-")[1::]
    subcat_name = " ".join(str(item) for item in subcategory_name_list)  # Extract the last part of the URL as the subcategory name
    print(f"Processing link {i+1}/{len(links)}: {subcat_name}")
    driver.get(link)
    time.sleep(5)  # Wait for the page to load completely

    height = driver.execute_script("return document.body.scrollHeight")  # Get the initial page height

    while True:
        try:
            # Try to click the "Load More" button if it exists
            wait = WebDriverWait(driver, 5)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Načíst další')]")))
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)  # Wait for new products to load
        except ElementClickInterceptedException as e:
            print("ElementClickInterceptedException occurred:", e)
        except Exception as e:
            print("No more 'Load More' button or error occurred:", e)

        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load

        # Check if new content is loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == height:
            print("No more content to load.")
            break
        height = new_height


    page_title = driver.title
    print(f'This is the page title: {page_title}.')
    # Extract the page source   
    page_source = driver.page_source
    #print(f'This is the length of the page source: {page_source}.')

    try:
        # Example XPath: Adjust this to match the actual item elements on the page
        subsub_name = driver.find_element(By.XPATH, "(//nav//ul//li/a)")
        # Example XPath: Adjust this to match the actual item elements on the page
        item_elements = driver.find_elements(By.XPATH, '//article[@data-cnstrc-item-name]')
    
        item_names = [item.get_attribute("data-cnstrc-item-name") for item in item_elements]
        # prices = driver.find_elements(By.XPATH, "//*[@class='text-gray']")# Adjust based on actual structure
        prices = driver.find_elements(By.XPATH, "//div[@class='tw-flex tw-justify-between tw-pr-2 tw-text-sm tw-font-normal tw-text-ds-neutral-70']/div[2]/span[1]")# Adjust based on actual structure

        # Print extracted data
        if len(item_names) != len(prices):
            print(f"Warning: Mismatch between item names ({len(item_names)}) and prices ({len(prices)})")
        #for name, price in zip(item_names, prices): jen pro ted, 3.6.12:05
            #data_kosik[name] = price.text
        for name, price in zip(item_names, prices):
            product_dict = {
                "name": name,
                "price": price.text,
                "subcategory": subcat_name,
                "sub-subcategory_name": subsub_name.text if subsub_name else "Unknown"
            }
            data_kosik_subcats.append(product_dict)   
    
    except Exception as e:
        print(f"Error while extracting data from {link}: {e}")

    finally:

        print(data_kosik_subcats)
    driver.quit()

#driver.quit()

import json

# Save data_kosik to a JSON file
with open("data_kosik_subcats.json", "w", encoding="utf-8") as json_file:
    json.dump(data_kosik_subcats, json_file, ensure_ascii=False, indent=4)

print("Data saved to data_kosik_subcats.json")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


print('THIS IS THE END OF THE MONDAY PROJECT')
print(f'THESE ARE THE LINKS: {links}.')