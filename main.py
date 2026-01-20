# ===================== IMPORTS =====================
from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data,
    save_enriched_data
)
from utils.api_handler import fetch_all_products, create_product_mapping


# ===================== MAIN FUNCTION =====================
def main():
    print("Starting Sales Analytics System...\n")

    # ---------- STEP 1: Read & clean sales data ----------
    filename = "data/sales_data.txt"
    cleaned_data = read_and_clean_sales_data(filename)

    if not cleaned_data:
        print("No valid data found. Exiting.")
        return

    print(f"Valid records after cleaning: {len(cleaned_data)}")

    # ---------- STEP 2: Convert cleaned data to dictionaries ----------
    transactions = []
    for parts in cleaned_data:   # parts is already a list
        transaction = {
            "TransactionID": parts[0],
            "Date": parts[1],
            "ProductID": parts[2],
            "ProductName": parts[3],
            "Quantity": int(parts[4]),
            "UnitPrice": float(parts[5]),
            "CustomerID": parts[6],
            "Region": parts[7]
        }
        transactions.append(transaction)

    print(f"Total transactions parsed: {len(transactions)}\n")

    # ---------- TASK 2.1: Sales Summary ----------
    total_revenue = calculate_total_revenue(transactions)
    region_sales = region_wise_sales(transactions)

    print("Total Revenue:", total_revenue)
    print("Region-wise Sales:", region_sales, "\n")

    # ---------- TASK 2.1: Top Products ----------
    top_products = top_selling_products(transactions)
    print("Top Selling Products:")
    for item in top_products:
        print(item)
    print()

    # ---------- TASK 2.1: Customer Analysis ----------
    customers = customer_analysis(transactions)
    print("Customer Analysis (Top 3):")
    for k in list(customers.keys())[:3]:
        print(k, customers[k])
    print()

    # ---------- TASK 2.2: Date-based Analysis ----------
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)

    print("Daily Sales Trend (first 3 days):")
    for d in list(daily_trend.keys())[:3]:
        print(d, daily_trend[d])

    print("\nPeak Sales Day:", peak_day, "\n")

    # ---------- TASK 2.3: Low Performing Products ----------
    low_products = low_performing_products(transactions)
    print("Low Performing Products:")
    for lp in low_products:
        print(lp)
    print()

    # ---------- TASK 3.1: Fetch API Products ----------
    api_products = fetch_all_products()
    if not api_products:
        print("API fetch failed. Skipping enrichment.")
        return

    product_mapping = create_product_mapping(api_products)
    print("Product mapping created successfully.\n")

    # ---------- TASK 3.2: Enrich Sales Data ----------
    enriched_transactions = enrich_sales_data(transactions, product_mapping)
    save_enriched_data(enriched_transactions)

    print("Enriched sales data saved successfully.")
    print("\nALL TASKS COMPLETED SUCCESSFULLY ✅")


# ===================== RUN =====================
if __name__ == "__main__":
    main()
