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

if response.ok:
    data = response.json()
    for item in data:
        print(f'{basic_url}{item.get('link')}')

else:
    print(f"Request failed with status code: {response.status_code}")
