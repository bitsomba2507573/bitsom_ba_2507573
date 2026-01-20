# Placeholder for API functions
def fetch_product_info(product_id):
    return {"name": "Example Product", "price": 100}

import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            products = []

            for p in data.get("products", []):
                product = {
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "category": p.get("category"),
                    "brand": p.get("brand"),
                    "price": p.get("price"),
                    "rating": p.get("rating")
                }
                products.append(product)

            print(f"Successfully fetched {len(products)} products from API")
            return products

        else:
            print("Failed to fetch products. Status code:", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("API connection error:", e)
        return []
