def analyze_sales(data):
    total_revenue = sum(row[4]*row[5] for row in data)
    region_sales = {}
    for row in data:
        region = row[7]
        region_sales[region] = region_sales.get(region, 0) + row[4]*row[5]
    return total_revenue, region_sales

def generate_report(data, total_revenue, region_sales, output_path):
    with open(output_path, "w") as f:
        f.write(f"Total Transactions: {len(data)}\n")
        f.write(f"Total Revenue: {total_revenue}\n\n")
        f.write("Revenue by Region:\n")
        for region, revenue in region_sales.items():
            f.write(f"{region}: {revenue}\n")
    





def parse_transactions(raw_lines):
    """
    Parses raw lines into a clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', '').strip(),
                'Quantity': int(parts[4].replace(',', '').strip()),
                'UnitPrice': float(parts[5].replace(',', '').strip()),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    Returns: tuple(valid_transactions, invalid_count, filter_summary)
    """
    valid_transactions = []
    invalid_count = 0

    # Validation
    for t in transactions:
        if (
            t.get('TransactionID', '').startswith('T') and
            t.get('ProductID', '').startswith('P') and
            t.get('CustomerID', '').startswith('C') and
            t.get('Quantity', 0) > 0 and
            t.get('UnitPrice', 0) > 0 and
            all(field in t for field in ['TransactionID', 'Date', 'ProductID', 'ProductName',
                                         'Quantity', 'UnitPrice', 'CustomerID', 'Region'])
        ):
            valid_transactions.append(t)
        else:
            invalid_count += 1

    total_input = len(transactions)

    # Display available regions
    regions_available = set(t['Region'] for t in valid_transactions)
    print(f"Available regions: {regions_available}")

    # Display transaction amount range
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
    if amounts:
        print(f"Transaction amount range: min={min(amounts)}, max={max(amounts)}")
    else:
        print("No valid transactions for amount range.")

    # Apply optional filters
    filtered_transactions = valid_transactions.copy()
    filtered_by_region_count = 0
    filtered_by_amount_count = 0

    if region:
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        filtered_by_region_count = len(valid_transactions) - len(filtered_transactions)
        print(f"After filtering by region '{region}': {len(filtered_transactions)} records")

    if min_amount is not None:
        filtered_transactions = [t for t in filtered_transactions if t['Quantity']*t['UnitPrice'] >= min_amount]
        filtered_by_amount_count = len(valid_transactions) - len(filtered_transactions)
        print(f"After applying min_amount {min_amount}: {len(filtered_transactions)} records")

    if max_amount is not None:
        filtered_transactions = [t for t in filtered_transactions if t['Quantity']*t['UnitPrice'] <= max_amount]
        filtered_by_amount_count += len(valid_transactions) - len(filtered_transactions)
        print(f"After applying max_amount {max_amount}: {len(filtered_transactions)} records")

    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region_count,
        'filtered_by_amount': filtered_by_amount_count,
        'final_count': len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, summary

# Task 2.1: Total Revenue
def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t['Quantity'] * t['UnitPrice']
    return total


# Task 2.2: Revenue by Region
def calculate_revenue_by_region(transactions):
    revenue_by_region = {}
    for t in transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']
        revenue_by_region[region] = revenue_by_region.get(region, 0) + revenue
    return revenue_by_region


# Task 2.b: Region-wise Sales Analysis
def region_wise_sales(transactions):
    stats = {}
    total_sales_all = 0.0

    # Calculate total sales and transaction count per region
    for t in transactions:
        region = t['Region']
        sale_amount = t['Quantity'] * t['UnitPrice']
        if region not in stats:
            stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        stats[region]['total_sales'] += sale_amount
        stats[region]['transaction_count'] += 1
        total_sales_all += sale_amount

    # Calculate percentage contribution
    for region in stats:
        stats[region]['percentage'] = round((stats[region]['total_sales'] / total_sales_all) * 100, 2)

    return stats

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}

    # Aggregate totals per product
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if name not in product_stats:
            product_stats[name] = {'total_qty': 0, 'total_revenue': 0.0}
        product_stats[name]['total_qty'] += qty
        product_stats[name]['total_revenue'] += revenue

    # Convert to list of tuples
    product_list = [
        (name, data['total_qty'], data['total_revenue'])
        for name, data in product_stats.items()
    ]

    # Sort by total quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Return top n
    return product_list[:n]
