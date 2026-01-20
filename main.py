from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import (
    validate_and_filter,
    calculate_total_revenue,
    calculate_revenue_by_region,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend
)

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/final_summary.txt"

def main():
    # Step 1: Read and clean sales data
    cleaned_data = read_and_clean_sales_data(DATA_PATH)

    if not cleaned_data:
        print("No valid data to process.")
        return

    # Step 2: Convert cleaned list to dictionaries
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

    print(f"Valid records after parsing: {len(transactions)}\n")

    # Step 3: Validate transactions
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Invalid records removed during validation: {invalid_count}")
    print(f"Valid records after validation: {len(valid_transactions)}\n")

    # Step 4: Revenue calculations
    total_revenue = calculate_total_revenue(valid_transactions)
    revenue_by_region = calculate_revenue_by_region(valid_transactions)

    print(f"Total Transactions: {len(valid_transactions)}")
    print(f"Total Revenue: {total_revenue}\n")

    print("Revenue by Region:")
    for region, revenue in revenue_by_region.items():
        print(f"{region}: {revenue}")

    # Step 5: Region-wise sales analysis
    region_stats = region_wise_sales(valid_transactions)
    print("\nRegion-wise Sales Analysis:")
    for region, data in region_stats.items():
        print(
            f"{region}: Total Sales={data['total_sales']}, "
            f"Transactions={data['transaction_count']}, "
            f"Percentage={data['percentage']}%"
        )

    # Step 6: Top selling products
    top_products = top_selling_products(valid_transactions, n=5)
    print("\nTop Selling Products:")
    for name, qty, revenue in top_products:
        print(f"{name}: Quantity Sold={qty}, Total Revenue={revenue}")

    # Step 7: Customer purchase analysis
    customer_stats = customer_analysis(valid_transactions)
    print("\nCustomer Purchase Analysis:")
    for cust_id, stats in customer_stats.items():
        print(
            f"{cust_id}: Total Spent={stats['total_spent']}, "
            f"Purchases={stats['purchase_count']}, "
            f"Avg Order={stats['avg_order_value']}, "
            f"Products={stats['products_bought']}"
        )

    # Step 8: Daily sales trend (Date-based analysis)
    daily_trends = daily_sales_trend(valid_transactions)
    print("\nDaily Sales Trend:")
    for date, stats in daily_trends.items():
        print(
            f"{date}: Revenue={stats['revenue']}, "
            f"Transactions={stats['transaction_count']}, "
            f"Unique Customers={stats['unique_customers']}"
        )

    # Step 9: Save all results to output file
    with open(OUTPUT_PATH, "w") as f:
        f.write(f"Total Transactions: {len(valid_transactions)}\n")
        f.write(f"Total Revenue: {total_revenue}\n\n")

        f.write("Revenue by Region:\n")
        for region, revenue in revenue_by_region.items():
            f.write(f"{region}: {revenue}\n")

        f.write("\nRegion-wise Sales Analysis:\n")
        for region, data in region_stats.items():
            f.write(
                f"{region}: Total Sales={data['total_sales']}, "
                f"Transactions={data['transaction_count']}, "
                f"Percentage={data['percentage']}%\n"
            )

        f.write("\nTop Selling Products:\n")
        for name, qty, revenue in top_products:
            f.write(f"{name}: Quantity Sold={qty}, Total Revenue={revenue}\n")

        f.write("\nCustomer Purchase Analysis:\n")
        for cust_id, stats in customer_stats.items():
            f.write(
                f"{cust_id}: Total Spent={stats['total_spent']}, "
                f"Purchases={stats['purchase_count']}, "
                f"Avg Order={stats['avg_order_value']}, "
                f"Products={stats['products_bought']}\n"
            )

        f.write("\nDaily Sales Trend:\n")
        for date, stats in daily_trends.items():
            f.write(
                f"{date}: Revenue={stats['revenue']}, "
                f"Transactions={stats['transaction_count']}, "
                f"Unique Customers={stats['unique_customers']}\n"
            )

    print(f"\nSummary saved to {OUTPUT_PATH}")
    print("Sales report generated successfully.")


if __name__ == "__main__":
    main()
