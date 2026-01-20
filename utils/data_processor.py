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
