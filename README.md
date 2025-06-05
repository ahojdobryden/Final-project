# Final Project: Rohlik vs Kosik

This is our final Python project, designed to let users compare two online grocery stores — **Rohlik** and **Kosik** — by matching user-provided product names with available items on each platform and then comparing the prices of the closest matches.

## 🛒 Project Overview

The goal of this project is to create a **smart shopping list** that recommends which store to buy each product from based on the **lowest available price**.

## 📊 Data Source

- [www.rohlik.cz](https://www.rohlik.cz)
- [www.kosik.cz](https://www.kosik.cz)
- 
📄 Input Files
from web scraping of [www.kosik.cz](https://www.kosik.cz)
	•	data_kosik_subcats.json: List of Kosik products with at least name, price, subcategory, sub-subcategory_name.
from web scraping of [www.rohlik.cz](https://www.rohlik.cz)
	•	rohlik_dairy_products_multi_cat.json: List of Rohlik products with at least name, unit_price, subcategory_name, subcategory_url.

## ✅ Expected Outcome

- A shopping list that:
  - Compares prices for identical products across both platforms.
  - Suggests the cheaper store for each product.

## 📦 Features
-	Dynamic category and product matching
-	Intelligent normalization and token comparison
-	Real-time fuzzy matching with scoring
- Graceful handling of missing matches or prices

## ⚠️ Known Limitations
- Matching relies heavily on subcategory labels. If a product is miscategorized,   it may not match.
-	Only supports products from Kosik and Rohlik using the given JSON files.
- Threshold tuning may be needed depending on the input quality.
