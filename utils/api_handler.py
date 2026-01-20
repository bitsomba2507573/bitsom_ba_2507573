import requests

# --------------------------
# Task 3.1: Fetch Products
# --------------------------
def fetch_all_products(limit=100):
    """
    Fetch all products from DummyJSON API.
    Returns a list of product dictionaries.
    """
    url = f"https://dummyjson.com/products?limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Products fetched successfully: {len(data.get('products', []))}")
        return data.get('products', [])
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of numeric product IDs to product info.
    Returns a dictionary: {numeric_id: {title, category, brand, rating}}
    """
    mapping = {}
    for product in api_products:
        try:
            numeric_id = int(product['id'])
            mapping[numeric_id] = {
                "title": product.get('title'),
                "category": product.get('category'),
                "brand": product.get('brand'),
                "rating": product.get('rating')
            }
        except Exception as e:
            continue
    print("Product mapping created successfully.")
    return mapping

# --------------------------
# Task 3.2: Enrich Sales Data
# --------------------------
def enrich_sales_data(transactions, product_mapping):
    """
    Enrich transaction data with API product information.
    Adds fields: API_Category, API_Brand, API_Rating, API_Match
    """
    enriched = []
    for t in transactions:
        enriched_t = t.copy()
        try:
            numeric_id = int(''.join(filter(str.isdigit, t['ProductID'])))
            api_info = product_mapping.get(numeric_id)
            if api_info:
                enriched_t['API_Category'] = api_info.get('category')
                enriched_t['API_Brand'] = api_info.get('brand')
                enriched_t['API_Rating'] = api_info.get('rating')
                enriched_t['API_Match'] = True
            else:
                enriched_t['API_Category'] = None
                enriched_t['API_Brand'] = None
                enriched_t['API_Rating'] = None
                enriched_t['API_Match'] = False
        except Exception:
            enriched_t['API_Category'] = None
            enriched_t['API_Brand'] = None
            enriched_t['API_Rating'] = None
            enriched_t['API_Match'] = False
        enriched.append(enriched_t)
    print(f"Enriched {len(enriched)}/{len(transactions)} transactions.")
    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to a file (pipe-delimited).
    """
    headers = [
        "TransactionID","Date","ProductID","ProductName","Quantity","UnitPrice",
        "CustomerID","Region","API_Category","API_Brand","API_Rating","API_Match"
    ]
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("|".join(headers) + "\n")
            for t in enriched_transactions:
                row = [str(t.get(h, "")) for h in headers]
                f.write("|".join(row) + "\n")
        print(f"Enriched sales data saved to {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")
