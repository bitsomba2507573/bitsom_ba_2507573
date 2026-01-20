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
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
import datetime

def main():
    try:
        print("SALES ANALYTICS SYSTEM\n")

        # Step 1: Read and clean sales data
        print("[1/10] Reading sales data...")
        filename = "data/sales_data.txt"
        cleaned_data = read_and_clean_sales_data(filename)
        print(f"Successfully read {len(cleaned_data)} transactions.\n")

        if not cleaned_data:
            print("No valid data to process.")
            return

        # Step 2: Convert cleaned data (list of lists) to dictionaries
        print("[2/10] Converting cleaned data to transaction dictionaries...")
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
        print(f"Successfully converted {len(transactions)} transactions.\n")

        # Step 3: Validate and filter transactions
        print("[3/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        print(f"Valid: {len(valid_transactions)} | Invalid: {invalid_count}\n")

        # Step 4: Analyze sales data
        print("[4/10] Analyzing sales data...\n")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions, n=5)
        customer_stats = customer_analysis(valid_transactions)
        daily_trends = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)

        print(f"Total Revenue: {total_revenue}")
        print(f"Region-wise Sales: {region_stats}\n")
        print("Top Selling Products:")
        for prod in top_products:
            print(prod)
        print("\nCustomer Analysis (Top 3):")
        for cid, stats in list(customer_stats.items())[:3]:
            print(cid, stats)
        print("\nDaily Sales Trend (first 3 days):")
        for date, info in list(daily_trends.items())[:3]:
            print(date, info)
        print("\nPeak Sales Day:", peak_day)
        print("\nLow Performing Products:")
        for prod in low_products:
            print(prod)
        print()

        # Step 5: Fetch product data from API
        print("[5/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"Fetched {len(api_products)} products")
        product_mapping = create_product_mapping(api_products)
        print("Product mapping created successfully.\n")

        # Step 6: Enrich sales data
        print("[6/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        save_enriched_data(enriched_transactions)
        print("Enriched sales data saved successfully.\n")

        # Step 7: Generate final report
        print("[7/10] Generating comprehensive sales report...")
        from utils.report_generator import generate_sales_report
        generate_sales_report(valid_transactions, enriched_transactions)
        print("Sales report generated and saved to output/sales_report.txt\n")

        print("[10/10] ALL TASKS COMPLETED SUCCESSFULLY ✅")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
