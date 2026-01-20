from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import validate_and_filter

def main():
    # Step 1: Read and clean sales data
    filename = "data/sales_data.txt"
    cleaned_data = read_and_clean_sales_data(filename)

    if not cleaned_data:
        print("No valid data to process.")
        return

    # Step 2: Convert cleaned list to dictionaries
    transactions = []
    for parts in cleaned_data:  # cleaned_data is list of lists
        transaction = {
            'TransactionID': parts[0],
            'Date': parts[1],
            'ProductID': parts[2],
            'ProductName': parts[3],
            'Quantity': parts[4],
            'UnitPrice': parts[5],
            'CustomerID': parts[6],
            'Region': parts[7]
        }
        transactions.append(transaction)

    print(f"Valid records after parsing: {len(transactions)}")

    # Step 3: Validate and filter transactions
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Invalid records removed during validation: {invalid_count}")
    print(f"Valid records after validation: {len(valid_transactions)}\n")

    # Step 4: Generate summary stats
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in valid_transactions)
    print(f"Total Transactions: {len(valid_transactions)}")
    print(f"Total Revenue: {total_revenue}\n")

    # Revenue by Region
    revenue_by_region = {}
    for t in valid_transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']
        revenue_by_region[region] = revenue_by_region.get(region, 0) + revenue

    print("Revenue by Region:")
    for region, revenue in revenue_by_region.items():
        print(f"{region}: {revenue}")

    # Step 5: Save output to file
    output_file = "output/final_summary.txt"
    with open(output_file, "w") as f:
        f.write(f"Total Transactions: {len(valid_transactions)}\n")
        f.write(f"Total Revenue: {total_revenue}\n\n")
        f.write("Revenue by Region:\n")
        for region, revenue in revenue_by_region.items():
            f.write(f"{region}: {revenue}\n")

    print(f"\nSummary saved to {output_file}")
    print("Sales report generated successfully.")

if __name__ == "__main__":
    main()
