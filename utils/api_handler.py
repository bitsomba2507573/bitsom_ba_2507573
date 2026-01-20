import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API (limit=100)
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Products fetched successfully")
        return data.get('products', [])
    except requests.RequestException as e:
        print(f"Failed to fetch products: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    mapping = {}
    for product in api_products:
        mapping[product['id']] = {
            'title': product.get('title', 'Unknown'),
            'category': product.get('category', 'Unknown'),
            'brand': product.get('brand', 'Unknown'),
            'price': product.get('price', 0.0),
            'rating': product.get('rating', 0.0)
        }
    print("Product mapping created successfully")
    return mapping
