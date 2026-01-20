def read_and_clean_sales_data(file_path):
    cleaned_data = []
    invalid_count = 0
    total_count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            total_count += 1
            line = line.strip()
            if not line:
                invalid_count += 1
                continue
            parts = line.split("|")
            if len(parts) != 8:
                invalid_count += 1
                continue
            trans_id, date, prod_id, prod_name, qty, price, cust_id, region = parts
            try:
                qty = int(qty.replace(",", ""))
                price = float(price.replace(",", ""))
            except:
                invalid_count += 1
                continue
            if not cust_id or not region or not trans_id.startswith("T") or qty <= 0 or price <= 0:
                invalid_count += 1
                continue
            prod_name = prod_name.replace(",", "")
            cleaned_data.append([trans_id, date, prod_id, prod_name, qty, price, cust_id, region])
    print(f"Total records parsed: {total_count}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(cleaned_data)}")
    return cleaned_data
