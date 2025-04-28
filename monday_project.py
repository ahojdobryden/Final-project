from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from lxml import html
import json

# Wait for a specific element to load (e.g., the first product name)


print('THIS IS THE MONDAY PROJECT')

#print(links)
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
driver = webdriver.Chrome(service=service, options=options)
data_rohlik = {}

basic_url = 'https://www.rohlik.cz' 
url = "https://www.rohlik.cz/api/v4/navigation/components/navigation-tabs/subcategories"
params = {
    "categoryIds": "300105026,300105008,300105001,300105053,300105048,300105021,300105058,300121231"
}

headers = {
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Cache-Control": "no-cache",
    "Sec-Fetch-Mode": "cors",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15",
    "Referer": "https://www.rohlik.cz/",
    "Connection": "keep-alive",
    "Host": "www.rohlik.cz",
    "Sec-Fetch-Dest": "empty",
    "Cookie": "_ga_M2GSLWRTRY=GS1.1.1745840258.12.1.1745840524.31.0.0; _dd_s=aid=a0de0ec8-071b-4ac0-92f9-3f1d660cd49a&rum=0&expire=1745841424727; PHPSESSION=XaixLjqCc8XwzMX3pjo0oswJT6exUCna; ttcsid_CSQC173C77U9RHEHQI30=1745840338168::iX5ocE4rBPhIOljOE_rl.11.1745840523454; JSESSIONID=node0ca9rw50fv5pq17u6r3trdwk4p20619515.node0; _clsk=1g4h023%7C1745840497634%7C3%7C1%7Ca.clarity.ms%2Fcollect; _tt_enable_cookie=1; _ttp=01JRWR8Z5WZVYMR0XVHA0M8CJ8_.tt.1; ttcsid=1745840338168::T40DvpERep1TmxiaPDS7.11.1745840496351; sailthru_content=... (truncated for readability)",
    "baggage": "sentry-environment=production,sentry-release=2025-04-28_07-43-09-836,sentry-public_key=a04769022c7841959445930b1f8dc5df,sentry-trace_id=f134db90f149479fac5ccc8b84a1898b,sentry-sample_rate=0.2,sentry-transaction=%2F,sentry-sampled=false",
    "x-b3-traceid": "1x0xz7zr8wiapqqk",
    "x-b3-spanid": "1x0xz7zr8wiapqqk",
    "X-Origin": "WEB",
    "sentry-trace": "f134db90f149479fac5ccc8b84a1898b-b5fd3bb4681e9dca-0",
    "Priority": "u=3, i"
}

response = requests.get(url, headers=headers, params=params)

links = []

# Check if the request was successful
if response.ok:
    data = response.json()
    #print(f'THIS IS THE DATA: {data}.')
    # Extract links from the JSON response
    for item in data:
        links.append(f'{basic_url}{item.get('link')}')

else:
    print(f"Request failed with status code: {response.status_code}")


#print(f'THESE ARE THE LINKS: {links}.')
start_time = time.time()
for link in links:
    driver.get(link)
    time.sleep(5)  # Wait for the page to load completely


    # Keep clicking the "Load More" button until it disappears
    while True:
        try:
            # Locate the "Load More" button (adjust the XPath to match the button's structure)
            load_more_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="button" and contains(text(), "Zobrazit vše")]'))
    )
            load_more_button.click()
            time.sleep(3)  # Wait for new products to load
        except Exception as e:
            print("No more 'Load More' button or error occurred:", e)
            break

    page_title = driver.title
    print(f'This is the page title: {page_title}.')
    # Extract the page source   
    page_source = driver.page_source
    print(f'This is the length of the page source: {page_source}.')

    try:
        # Example XPath: Adjust this to match the actual item elements on the page
        item_names = driver.find_elements(By.XPATH, '//a//h3[@data-test="productCard-body-name"]')
        prices = driver.find_elements(By.XPATH, '//p[@data-test="productCard-footer-unitPrice"]')# Adjust based on actual structure

        # Print extracted data
        for name, price in zip(item_names, prices):
            #print(f"Product Name: {name.text}")
            #print(f"Price: {price.text}")
            data_rohlik[name.text] = price.text
            #print("-" * 20)
    
    except Exception as e:
        print(f"Error while extracting data from {link}: {e}")

    finally:
        print(data_rohlik)


driver.quit()

import json

# Save data_rohlik to a JSON file
with open("data_rohlik.json", "w", encoding="utf-8") as json_file:
    json.dump(data_rohlik, json_file, ensure_ascii=False, indent=4)

print("Data saved to data_rohlik.json")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


print('THIS IS THE END OF THE MONDAY PROJECT')
