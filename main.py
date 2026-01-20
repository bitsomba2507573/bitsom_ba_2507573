# main.py

from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import (
    validate_and_filter,
    calculate_total_revenue,
    calculate_revenue_by_region,
    region_wise_sales,
    top_selling_products,
    low_performing_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day
)
from utils.api_handler import fetch_all_products, create_product_mapping

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/final_summary.txt"

def main():
    # -------- Task 1: Read & Clean Data --------
    raw_data = read_and_clean_sales_data(DATA_PATH)
    if not raw_data:
        print("No valid data to process.")
        return

    # Convert cleaned list of lists to dictionaries
    transactions = [
        {
            'TransactionID': parts[0],
            'Date': parts[1],
            'ProductID': parts[2],
            'ProductName': parts[3],
            'Quantity': parts[4],
            'UnitPrice': parts[5],
            'CustomerID': parts[6],
            'Region': parts[7]
        }
        for parts in raw_data
    ]
    print(f"Valid records after parsing: {len(transactions)}")

    # -------- Task 1.3: Validate & Filter --------
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)
    print(f"Invalid records removed during validation: {invalid_count}")
    print(f"Valid records after validation: {len(valid_transactions)}\n")

    # -------- Task 2.1 & 2.2: Sales Analysis --------
    total_revenue = calculate_total_revenue(valid_transactions)
    region_sales = calculate_revenue_by_region(valid_transactions)
    region_stats = region_wise_sales(valid_transactions)
    top_products = top_selling_products(valid_transactions)
    low_products = low_performing_products(valid_transactions)
    customer_stats = customer_analysis(valid_transactions)
    daily_trend = daily_sales_trend(valid_transactions)
    peak_day = find_peak_sales_day(valid_transactions)

    print(f"Total Transactions: {len(valid_transactions)}")
    print(f"Total Revenue: {total_revenue}\n")
    print("Revenue by Region:", region_sales)
    print("Region-wise Stats:", region_stats)
    print("Top Products:", top_products)
    print("Low Performing Products:", low_products)
    print("Customer Analysis:", customer_stats)
    print("Daily Sales Trend:", daily_trend)
    print("Peak Sales Day:", peak_day)

    # -------- Task 3: API Product Info --------
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)
    print(f"Total API Products Fetched: {len(product_mapping)}")

    # -------- Save Summary to File --------
    with open(OUTPUT_PATH, "w") as f:
        f.write(f"Total Transactions: {len(valid_transactions)}\n")
        f.write(f"Total Revenue: {total_revenue}\n\n")
        f.write("Revenue by Region:\n")
        for region, revenue in region_sales.items():
            f.write(f"{region}: {revenue}\n")
        f.write("\nRegion-wise Stats:\n")
        for region, stats in region_stats.items():
            f.write(f"{region}: {stats}\n")
        f.write("\nTop Products:\n")
        for p in top_products:
            f.write(f"{p}\n")
        f.write("\nLow Performing Products:\n")
        for p in low_products:
            f.write(f"{p}\n")
        f.write("\nCustomer Analysis:\n")
        for c, stats in customer_stats.items():
            f.write(f"{c}: {stats}\n")
        f.write("\nDaily Sales Trend:\n")
        for date, stats in daily_trend.items():
            f.write(f"{date}: {stats}\n")
        f.write(f"\nPeak Sales Day: {peak_day}\n")
        f.write(f"\nTotal API Products Fetched: {len(product_mapping)}\n")

    print(f"\nSummary saved to {OUTPUT_PATH}")
    print("Sales report generated successfully.")

if __name__ == "__main__":
    main()
