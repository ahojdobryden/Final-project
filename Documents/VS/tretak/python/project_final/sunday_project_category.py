from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from lxml import html
import json

# Wait for a specific element to load (e.g., the first product name)


print('THIS IS THE SUNDAY PROJECT')

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

# The URL you want to request
basic_url = "https://rohlik.cz"  # Base URL for constructing full links
url = 'https://www.rohlik.cz/api/v1/categories?type=normal&categories=300105026&categories=300105008&categories=300105001&categories=300105053&categories=300105048&categories=300105021&categories=300105058&categories=300121231'


# Define headers and cookies
headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'baggage': 'sentry-environment=production,sentry-release=2025-04-25_16-07-53-534,sentry-public_key=a04769022c7841959445930b1f8dc5df,sentry-trace_id=c24c0a74a80c4c989ca05ee10a6df88d,sentry-sample_rate=0.2,sentry-transaction=%2F,sentry-sampled=false',
    'cache-control': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.rohlik.cz/c300105000-mlecne-a-chlazene',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '7dc22b50b3e94f00be061362ead9f853-b015660e90639b5b-0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-b3-spanid': 'jiukei0h2sq0xh8e',
    'x-b3-traceid': 'jiukei0h2sq0xh8e',
    'x-origin': 'WEB'
}

cookies = {
    'PHPSESSION': '8H0S9GkiKZg3wvT1aBWDIDIPwBWMvxuo',
    '_gcl_au': '1.1.613867309.1745492984',
    '_ga': 'GA1.1.715726514.1745492953',
    'udid': '0196677d-4258-7c54-a6be-27161d3aa592@1745492984383',
    '_fbp': 'fb.1.1745492984392.359108129837460418',
    '_tt_enable_cookie': '1',
    '_ttp': '01JSKQTGVCNXJA1GQA2P4VDWYV_.tt.1',
    'sailthru_visitor': '21171ea6-1c08-4654-a1ea-9b044428baad',
    '_hjSessionUser_203416': 'eyJpZCI6ImFkMTE2NTIzLTUwYTctNTU5Ni1hYjZjLTc3M2NkZmE1ZGFiMCIsImNyZWF0ZWQiOjE3NDU0OTI5ODQ4OTMsImV4aXN0aW5nIjp0cnVlfQ==',
    '_clck': 'jrlifh%7C2%7Cfvf%7C0%7C1940',
    'tutorialDelivery': 'true',
    'language': 'cs-CZ',
    'NEXT_LOCALE': 'cs-CZ',
    '__cfruid': 'add2583a37bdf63c726b00b4f5f1c7f074254fd9-1745755147',
    '_cfuvid': 'ibD.Tgc9vLAPALPEz2fO5Bzy9b_7Ke3R7Sgi_c_ps_s-1745755147003-0.0.1.1-604800000',
    '_hjSession_203416': 'eyJpZCI6IjlmMGQ3YjQ4LTA4ZTgtNDgxZS05NGM0LWExMmNkNWRkZjQ0YSIsImMiOjE3NDU3NTUxNDc0NzgsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    '_hjHasCachedUserAttributes': 'true',
    '_hjUserAttributesHash': '2bc54f8a87b0d480d8f2d6f65146a01b',
    'cf_clearance': 'fUWoGKyVWou9cdJitPlKhVDdYk5momzAkXqpaEOZeqo-1745760404-1.2.1.1-_2Y4kthZ_bNmhSLXoEPO6FnIiY4cdPKijO4tleLWTquGXZg5..orUeCQFr9qvcgNGM.ykHxrjjqns8QaJP9Ll1Gb19OVP6LThfbLZQxC30x0pNWGj0..Vqvat6eL.g1SBGedgS5PcNV0Icg_Kivh5aDdF_G58X6mVhEX79KwZpaxdOfOFSObfSbgQ.0ueytMMGfNJQsEZ_AMfQlrcPDnLicQg0EsK9P0.O.Kg5DB3.Ox_6enpk2K.Fy2tdroOzsEPEdD947Fx49_N9alPCRheT_wMp9iXRJBk_1TRBOCLCbA81rYRN83.1RXM.qLmZOkqiA_iYqD682IZcVLJBUOg2RlqSdg0Jvp9Am2J625xMY',
    'lastVisit': '1745760413628',
    'currentVisit': '1745760418426',
    'cto_bundle': '31XbKF9NOEJuN2dleVdKRTl6SFl1bUg0dFp0dlhHJTJCa3Y4VFJWZUE2UHU2M2RkMjVGVlBnU3lrNlNublE5Y2R1a3JCU0RKdDJrZmowaExCUDlZRjgxYXlsRmYyVGtpcE1IaHlveUtmMGlLN04zU0dXVUV4UGZYMzVHREtySUk1NWpJMHlSaUMxWlhCbXclMkZBV0lwN25ZS0clMkZvS3clM0QlM0Q',
    'sailthru_content': '5fa69a28a959cc5b0a1b758dcf207aeea0aaf2cd5769a25c7598f0d872b887739e8918bfbd95f063bfec7f3fbdd0b9b91afbb25c39db122ca870bb1fce1f5fca0ccd974d7d0790066d71f4f0a1d68efb5ca320c488f1a7f90a47e487ae1116d4491f3052cc87bb8e2a0a49cef224fb657436c971226eb4aafc5d67ab612d8eb523964c5d8e835aa0180784158a5da4a1aa065291791665c0c360918ef95b3e36c680c688f2f2741262bf0ecbb7f4eb382579cd7dd3fae526c04b0467ce436ccf3cc0f0579af11e6b5bc8e9551a414d6eb0276a9b693d5e8470f10625e6f03259',
    '_clsk': 'zpefbc%7C1745760740396%7C1%7C1%7Cl.clarity.ms%2Fcollect',
    'ttcsid_CSQC173C77U9RHEHQI30': '1745755147729::gx_H1jZunU101GRYOV8L.4.1745760745544',
    'ttcsid': '1745755147729::vknF9C160mhF2onKE0nX.4.1745760745544',
    '_dd_s': 'aid=465b99dc-8779-4f82-bdf7-c132249de318&rum=0&expire=1745761645484',
    '_ga_M2GSLWRTRY': 'GS1.1.1745755147.5.1.1745760745.57.0.0',
    'sailthru_pageviews': '61',
    'JSESSIONID': 'node09zfrnudu2if2nb2511eb0hp014136033.node0'
}

response = requests.get(url, headers=headers, cookies=cookies)
#print(response.json())

categories_id = []
categories_name = []
for dict in response.json():
    for key, value in dict.items():
        if key == 'categoryId':
            #print(f"Category ID: {value}")
            categories_id.append(value)
        if key == 'name':
            #print(f"Category Name: {value}")
            value_formatted = value.lower().replace(" ", "-").replace(",","").replace("á", "a").replace("é", "e").replace("ý", "y").replace("ř", "r").replace("č", "c").replace("š", "s").replace("ž", "z").replace("í", "i").replace("ě", "e").replace("ů", "u").replace("ú", "u").replace("ó", "o")
            categories_name.append(value_formatted)
print(f'Categories id: {categories_id}')
print(f'Categories name: {categories_name}')



for v in categories_id:
    #print(f"Category ID: {v}")
    #url = f'https://www.rohlik.cz/api/v1/categories/{v}/products?sort=popularity&offset=0&limit=100&'
    link = f'{basic_url}/c{v}-{categories_name[categories_id.index(v)]}'
    print(f"Category Name: {link}")
    # Fetch the main categories page
    driver.get(link)

    
    time.sleep(3)# Wait for the page to load

    # Example: Print the page title
    print("Page title:", driver.title)

    # Example: Get the page source
    #page_source = driver.page_source
    #print("Page source length:", len(page_source))


    try:
        # Example XPath: Adjust this to match the actual item elements on the page
        item_names = driver.find_elements(By.XPATH, '//a//h3[@data-test="productCard-body-name"]')
        prices = driver.find_elements(By.XPATH, '//p[@data-test="productCard-footer-unitPrice"]')# Adjust based on actual structure

        # Print extracted data
        for name, price in zip(item_names, prices):
            #print(f"Product Name: {name.text}")
            #print(f"Price: {price.text}")
            data_rohlik[name.text] = price.text
        print(data_rohlik)
        print("NEXT PRODUCT")
        data_rohlik = {} # Clear the dictionary for the next category
        #I still get only a couple of products, so I need to scroll down the page to load more
            
        
    

        # Check if the page height has stopped increasing (no more content to load)
        #new_height = driver.execute_script("return document.body.scrollHeight")
        #if new_height == last_height:
            #time.sleep(2)
            #print("No more content to load.")
            #break
    except Exception as e:
        print(f"Error while extracting data from {link}: {e}")
        break

    #finally:
        #print(f"Collected data: {data_rohlik}")


driver.quit()

