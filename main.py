from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import (
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day
)

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/final_summary.txt"


def main():
    # --------------------------------------------------
    # Task 1: Read & Clean Data
    # --------------------------------------------------
    cleaned_data = read_and_clean_sales_data(DATA_PATH)

    if not cleaned_data:
        print("No valid data to process.")
        return

    # --------------------------------------------------
    # Convert cleaned list to dictionaries
    # --------------------------------------------------
    transactions = []
    for parts in cleaned_data:
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

    print(f"Records after parsing: {len(transactions)}")

    # --------------------------------------------------
    # Task 1.3: Validation
    # --------------------------------------------------
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records: {len(valid_transactions)}\n")

    # --------------------------------------------------
    # Task 2.1a: Total Revenue
    # --------------------------------------------------
    total_revenue = calculate_total_revenue(valid_transactions)
    print("Total Revenue:", total_revenue)

    # --------------------------------------------------
    # Task 2.1b: Region-wise Sales
    # --------------------------------------------------
    region_sales = region_wise_sales(valid_transactions)
    print("\nRegion-wise Sales:")
    for region, stats in region_sales.items():
        print(region, stats)

    # --------------------------------------------------
    # Task 2.1c: Top Selling Products
    # --------------------------------------------------
    top_products = top_selling_products(valid_transactions, n=5)
    print("\nTop Selling Products:")
    for product in top_products:
        print(product)

    # --------------------------------------------------
    # Task 2.1d: Customer Purchase Analysis
    # --------------------------------------------------
    customers = customer_analysis(valid_transactions)
    print("\nCustomer Analysis:")
    for customer, stats in customers.items():
        print(customer, stats)

    # --------------------------------------------------
    # Task 2.2a: Daily Sales Trend
    # --------------------------------------------------
    daily_trend = daily_sales_trend(valid_transactions)
    print("\nDaily Sales Trend:")
    for date, stats in daily_trend.items():
        print(date, stats)

    # --------------------------------------------------
    # Task 2.2b: Peak Sales Day
    # --------------------------------------------------
    peak_day = find_peak_sales_day(valid_transactions)
    print("\nPeak Sales Day:", peak_day)

    # --------------------------------------------------
    # Save Output to File
    # --------------------------------------------------
    with open(OUTPUT_PATH, "w") as f:
        f.write(f"Total Revenue: {total_revenue}\n\n")
        f.write("Region-wise Sales:\n")
        for region, stats in region_sales.items():
            f.write(f"{region}: {stats}\n")

        f.write("\nTop Selling Products:\n")
        for product in top_products:
            f.write(f"{product}\n")

        f.write("\nPeak Sales Day:\n")
        f.write(str(peak_day))

    print(f"\nSummary saved to {OUTPUT_PATH}")
    print("Sales analytics system executed successfully.")


if __name__ == "__main__":
    main()
