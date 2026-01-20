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
