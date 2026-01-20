from utils.file_handler import read_and_clean_sales_data
from utils.data_processor import analyze_sales, generate_report

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/sales_report.txt"

def main():
    cleaned_data = read_and_clean_sales_data(DATA_PATH)
    total_revenue, region_sales = analyze_sales(cleaned_data)
    generate_report(cleaned_data, total_revenue, region_sales, OUTPUT_PATH)
    print("Sales report generated successfully.")

if __name__ == "__main__":
    main()
