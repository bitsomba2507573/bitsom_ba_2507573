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
