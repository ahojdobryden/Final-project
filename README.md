# Final Project: Rohlik vs Kosik

This is our final Python project, comparing two online grocery stores — **Rohlik** and **Kosik**.

## 🛒 Project Overview

The goal of this project is to create a **smart shopping list** that recommends which store to buy each product from based on the **lowest available price**.

## 📊 Data Source

- [www.rohlik.cz](https://www.rohlik.cz)
- [www.kosik.cz](https://www.kosik.cz)

## ✅ Expected Outcome

- A shopping list that:
  - Compares prices for identical products across both platforms.
  - Suggests the cheaper store for each product.

curl ^"https://www.kosik.cz/api/front/page/products/flexible?vendor=1^&slug=c898-mlecne-a-chlazene^&limit=30^&search_term=^&page_display=horizontal^&platform=web^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: cs,en;q=0.9^" ^
  -b ^"consentPreferences=^{^\^"timestamp^\^":^\^"2025-04-15T11:42:12.140Z^\^",^\^"version^\^":1,^\^"functional_storage^\^":^\^"granted^\^",^\^"analytics_storage^\^":^\^"denied^\^",^\^"personalization_storage^\^":^\^"denied^\^",^\^"ad_storage^\^":^\^"denied^\^",^\^"ad_user_data^\^":^\^"denied^\^",^\^"ad_personalization^\^":^\^"denied^\^"^}; _nss=1; lbuid=250428^%^7C572777531998; X-Ksp-Token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImtpZDEifQ.eyJzdWIiOiIxNzcyODA5MDYiLCJzY3AiOiIxIiwiY2F0IjoxNzQ1ODU1OTIzLCJpYXQiOjE3NDU4NTU5MjMsImlzcyI6InBjeiIsImV4cCI6MTc0NjQ2MDcyM30.e40lZ6mnvb8VwXwbzsSWYYpgRfsHcL0isaVJUGfaAHPRWXkyMigWiHkG2rdT_EBOzuzjlCo0wTyXlFshOhYRlT859vUVd3FtINqacp4a48mP7OPNiGS_F4qIhDqL5fEGW2Y08wyJOKGsudDQyJagTXtgQWN9dUYfsISh-I6krv43olWqJOR5jhB_XA9OFol9Pp58kviiVTgEHPLQ9EaWYF0PNDt-Gfv6Xw0E6RS3yK4QqOAae_9CUyU15-KGQWb2QSZNMwM-FRnOlBiBSX7d6ltnGodNI6DE2-ZHiKXDoLRDYyKqkOyKyhMJVIkVq-5h4WjPLKHwSJ8ExW5irM4grP7v_6SMteQozFqtiEDINBVAfHmNFrxOBO6taniU-vJW4kZ3eZUMNheFhWGhNn2BGcSkYA-mzycZY2w4YxFGwBKlRYdgl_2aeu5K0ywP9z5brD0fNmbT0ml8v2OEbq-MOYcvO0o0KtTi_MoJsh8EmQvMWHwjSq8yUUeHJUInEAxh^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"referer: https://www.kosik.cz/c898-mlecne-a-chlazene^" ^
  -H ^"sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"135^\^", ^\^"Not-A.Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"135^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-origin^" ^
  -H ^"traceparent: 00-361cd6e5063444884f47e00f86f27604-de11cf60cd96a98d-01^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36^"
