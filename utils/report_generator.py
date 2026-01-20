import os
from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a detailed sales report including overall summary,
    region-wise performance, top products, top customers, daily trends,
    product performance, and API enrichment summary.
    """
    if not transactions:
        print("No transactions to generate report.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # HEADER
    report_lines = []
    report_lines.append("SALES ANALYTICS REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("\n")

    # OVERALL SUMMARY
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    report_lines.append("OVERALL SUMMARY")
    report_lines.append(f"Total Revenue: {total_revenue:,.2f}")
    report_lines.append(f"Total Transactions: {total_transactions}")
    report_lines.append(f"Average Order Value: {avg_order_value:,.2f}")
    report_lines.append(f"Date Range: {date_range}")
    report_lines.append("\n")

    # REGION-WISE PERFORMANCE
    report_lines.append("REGION-WISE PERFORMANCE")
    region_stats = defaultdict(lambda: {"revenue": 0, "count": 0})
    for t in transactions:
        region = t['Region']
        amt = t['Quantity'] * t['UnitPrice']
        region_stats[region]["revenue"] += amt
        region_stats[region]["count"] += 1

    sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]["revenue"], reverse=True)
    report_lines.append(f"{'Region':<10} {'Sales':>15} {'% of Total':>12} {'Transactions':>12}")
    for region, stats in sorted_regions:
        percent_total = (stats["revenue"] / total_revenue * 100) if total_revenue else 0
        report_lines.append(f"{region:<10} {stats['revenue']:>15,.2f} {percent_total:>11.2f}% {stats['count']:>12}")

    report_lines.append("\n")

    # TOP 5 PRODUCTS
    report_lines.append("TOP 5 PRODUCTS")
    product_stats = defaultdict(lambda: {"quantity": 0, "revenue": 0})
    for t in transactions:
        pname = t['ProductName']
        product_stats[pname]["quantity"] += t['Quantity']
        product_stats[pname]["revenue"] += t['Quantity'] * t['UnitPrice']

    top_products = sorted(product_stats.items(), key=lambda x: x[1]["quantity"], reverse=True)[:5]
    report_lines.append(f"{'Rank':<5} {'Product Name':<20} {'Quantity':>10} {'Revenue':>15}")
    for i, (pname, stats) in enumerate(top_products, 1):
        report_lines.append(f"{i:<5} {pname:<20} {stats['quantity']:>10} {stats['revenue']:>15,.2f}")

    report_lines.append("\n")

    # TOP 5 CUSTOMERS
    report_lines.append("TOP 5 CUSTOMERS")
    customer_stats = defaultdict(lambda: {"spent": 0, "orders": 0})
    for t in transactions:
        cid = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        customer_stats[cid]["spent"] += amt
        customer_stats[cid]["orders"] += 1

    top_customers = sorted(customer_stats.items(), key=lambda x: x[1]["spent"], reverse=True)[:5]
    report_lines.append(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':>15} {'Orders':>8}")
    for i, (cid, stats) in enumerate(top_customers, 1):
        report_lines.append(f"{i:<5} {cid:<15} {stats['spent']:>15,.2f} {stats['orders']:>8}")

    report_lines.append("\n")

    # DAILY SALES TREND
    report_lines.append("DAILY SALES TREND")
    daily_stats = defaultdict(lambda: {"revenue": 0, "transactions": 0, "unique_customers": set()})
    for t in transactions:
        date = t['Date']
        amt = t['Quantity'] * t['UnitPrice']
        daily_stats[date]["revenue"] += amt
        daily_stats[date]["transactions"] += 1
        daily_stats[date]["unique_customers"].add(t['CustomerID'])

    report_lines.append(f"{'Date':<12} {'Revenue':>12} {'Transactions':>12} {'Unique Customers':>18}")
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        report_lines.append(f"{date:<12} {stats['revenue']:>12,.2f} {stats['transactions']:>12} {len(stats['unique_customers']):>18}")

    report_lines.append("\n")

    # PRODUCT PERFORMANCE ANALYSIS
    report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
    best_selling = top_products[0][0] if top_products else "N/A"
    low_perf = [(p, s["quantity"], s["revenue"]) for p, s in product_stats.items() if s["quantity"] < 10]
    avg_transaction_region = {r: stats["revenue"] / stats["count"] if stats["count"] else 0 for r, stats in region_stats.items()}

    report_lines.append(f"Best Selling Product: {best_selling}")
    if low_perf:
        report_lines.append("Low Performing Products:")
        for p, q, r in low_perf:
            report_lines.append(f"{p}: Quantity={q}, Revenue={r:,.2f}")
    report_lines.append("Average Transaction Value per Region:")
    for r, avg in avg_transaction_region.items():
        report_lines.append(f"{r}: {avg:,.2f}")

    report_lines.append("\n")

    # API ENRICHMENT SUMMARY
    report_lines.append("API ENRICHMENT SUMMARY")
    total_enriched = sum(1 for t in enriched_transactions if t.get("API_Match"))
    total_products = len(enriched_transactions)
    failed_products = [t['ProductName'] for t in enriched_transactions if not t.get("API_Match")]
    success_rate = (total_enriched / total_products * 100) if total_products else 0

    report_lines.append(f"Total Products Enriched: {total_enriched}/{total_products}")
    report_lines.append(f"Success Rate: {success_rate:.2f}%")
    if failed_products:
        report_lines.append("Products Not Enriched:")
        report_lines.append(", ".join(failed_products))

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Sales report generated and saved to {output_file}")
