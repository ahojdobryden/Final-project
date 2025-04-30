from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from lxml import html
import json

url = 'https://www.rohlik.cz/api/v4/navigation/components/navigation-tabs/subcategories'
basic_url = "https://rohlik.cz" 
params = {
    'categoryIds': '300121865,300120608,300105027,300105028,300105031,300124066,300123521,300105040,300123507,300124070,300114329,300122648,300124065'
}

headers = {
    'x-b3-spanid': 'jy2yig7bh0knsjn1',
    'sec-ch-ua-platform': '"macOS"',
    'Cache-Control': 'no-cache',
    'Referer': 'https://www.rohlik.cz/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'baggage': 'sentry-environment=production,sentry-release=2025-04-25_16-07-53-534,sentry-public_key=a04769022c7841959445930b1f8dc5df,sentry-trace_id=b6953cc98b5c4799aa17a6debc735f24,sentry-sample_rate=0.2,sentry-transaction=%2F,sentry-sampled=false',
    'sentry-trace': 'b6953cc98b5c4799aa17a6debc735f24-852f3947e5e2cf7d-0',
    'X-Origin': 'WEB',
    'x-b3-traceid': 'jy2yig7bh0knsjn1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers, params=params)
links = []

# Check if the request was successful
if response.ok:
    data = response.json()
    print(f'THIS IS THE DATA: {data}.')
    # Extract links from the JSON response
    for item in data:
        links.append(f'{basic_url}{item.get('link')}')

else:
    print(f"Request failed with status code: {response.status_code}")


print(f'THESE ARE THE LINKS: {links}.')
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

for link in links:
    # Fetch the page
    driver.get(link)
    print(f'This is the link: {link}.')

    # Wait for the page to load (you can use WebDriverWait for smarter waits)
    time.sleep(3)

    # Example: Print the page title
    print("Page title:", driver.title)

    # Example: Get the page source
    page_source = driver.page_source
    print("Page source length:", len(page_source))

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

# Print the collected data
#print(f"Finished category: {link}")
#print(f"Collected data: {data_rohlik}")
driver.quit()

print(len(data_rohlik))
