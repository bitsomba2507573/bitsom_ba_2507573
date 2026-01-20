from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import (
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/final_summary.txt"


def main():
    # -------- Task 1.1 + 1.2: Read & Clean ----------
    cleaned_data = read_and_clean_sales_data(DATA_PATH)

    if not cleaned_data:
        print("No valid data found.")
        return

    # -------- Convert to dictionaries ----------
    transactions = []
    for parts in cleaned_data:
        transactions.append({
            'TransactionID': parts[0],
            'Date': parts[1],
            'ProductID': parts[2],
            'ProductName': parts[3],
            'Quantity': parts[4],
            'UnitPrice': parts[5],
            'CustomerID': parts[6],
            'Region': parts[7]
        })

    print(f"Valid records after parsing: {len(transactions)}")

    # -------- Task 1.3: Validation & Filtering ----------
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Invalid records removed during validation: {invalid_count}")
    print(f"Valid records after validation: {len(valid_transactions)}\n")

    # -------- Task 2.1: Sales Summary ----------
    total_revenue = calculate_total_revenue(valid_transactions)
    region_sales = region_wise_sales(valid_transactions)

    print("Total Revenue:", total_revenue)
    print("Region-wise Sales:", region_sales, "\n")

    # -------- Task 2.1(c): Top Selling Products ----------
    top_products = top_selling_products(valid_transactions)

    print("Top Selling Products:")
    for p in top_products:
        print(p)
    print()

    # -------- Task 2.1(d): Customer Analysis ----------
    customers = customer_analysis(valid_transactions)

    print("Customer Purchase Analysis:")
    for c, data in customers.items():
        print(c, data)
    print()

    # -------- Task 2.2(a): Daily Sales Trend ----------
    daily_trend = daily_sales_trend(valid_transactions)

    print("Daily Sales Trend:")
    for date, data in daily_trend.items():
        print(date, data)
    print()

    # -------- Task 2.2(b): Peak Sales Day ----------
    peak_day = find_peak_sales_day(valid_transactions)
    print("Peak Sales Day:", peak_day, "\n")

    # -------- Task 2.3(a): Low Performing Products ----------
    low_products = low_performing_products(valid_transactions)

    print("Low Performing Products:")
    for p in low_products:
        print(p)

    # -------- Save Summary ----------
    with open(OUTPUT_PATH, "w") as f:
        f.write(f"Total Transactions: {len(valid_transactions)}\n")
        f.write(f"Total Revenue: {total_revenue}\n\n")
        f.write("Region-wise Sales:\n")
        for region, data in region_sales.items():
            f.write(f"{region}: {data}\n")

    print("\nSummary saved to", OUTPUT_PATH)
    print("Sales report generated successfully.")


if __name__ == "__main__":
    main()
