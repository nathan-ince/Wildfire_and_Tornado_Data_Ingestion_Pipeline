import json
import re

with open('data/raw/raw_data.json') as f:
    my_list = json.load(f)

accept_list = []
reject_list = []

for row in my_list:
    valid = True

    if row["transaction_id"]:
        transaction_id = row["transaction_id"]
        if not re.match(r'^TXN_\d{7}$', transaction_id):
            valid = False 
            row["error"] = "Invalid transaction value"
    else:
        valid = False
        row["error"] = "Empty transaction value"


    if row["customer_id"]:
        customer_id = row["customer_id"]
        if not re.match(r'^CUST_\d{1,}$', customer_id):
            valid = False 
            row["error"] = "Invalid customer value"
    else:
        valid = False
        row["error"] = "Empty customer value"


    if not row["category"]:
        valid = False 
        row["error"] = "Empty category value"
    

    if row["item"]:
        item = row["item"]
        if not re.match(r'^Item_\d{1,}_[A-Z]+$', item):
            valid = False 
            row["error"] = "Invalid item value"
    else:
        valid = False
        row["error"] = "Empty item value"

    
    if row["price_per_unit"]:
        try:
            price_per_unit = float(row["price_per_unit"])
        except (TypeError, ValueError):
            valid = False
            row["error"] = "Invalid price_per_unit value"

        if price_per_unit <= 0:
            valid = False
            row["error"] = "Invalid price_per_unit value"
    else:
        valid = False
        row["error"] = "Empty price_per_unit value"


    if row["quantity"]:
        try:
            quantity = float(row["quantity"])
        except (TypeError, ValueError):
            valid = False
            row["error"] = "Invalid quantity value"

        if quantity <= 0:
            valid = False
            row["error"] = "Invalid quantity value"
    else:
        valid = False
        row["error"] = "Empty quantity value"


    if row["total_spent"]:
        try:
            total_spent = float(row["total_spent"])
        except (TypeError, ValueError):
            valid = False
            row["error"] = "Invalid total_spent value"

        if total_spent <= 0:
            valid = False
            row["error"] = "Invalid total_spent value"
        if valid:
            if total_spent != price_per_unit * quantity:
                valid = False
                row["error"] = "Invalid total_spent value"
    else:
        valid = False
        row["error"] = "Empty total_spent value"
    

    if row["payment_method"]:
        payment_method = row["payment_method"]
        if not re.match(r'^(Cash|Credit Card|Digital Wallet)$', payment_method):
            valid = False 
            row["error"] = "Invalid payment_method value"
    else:
        valid = False
        row["error"] = "Empty payment_method value"
    

    if row["location"]:
        location = row["location"]
        if not re.match(r'^(In-store|Online)$', location):
            valid = False 
            row["error"] = "Invalid location value"
        if location == "Online" and payment_method == "Cash":
            valid = False
            row["error"] = "Invalid location value"
    else:
        valid = False
        row["error"] = "Empty location value"
    

    if row["transaction_date"]:
        transaction_date = row["transaction_date"]
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', transaction_date):
            valid = False 
            row["error"] = "Invalid transaction_date value"
    else:
        valid = False
        row["error"] = "Empty transaction_date value"

    
    if row["discount_applied"] is None:
        row["discount_applied"] = False

    if valid:
        accept_list.append(row)
    else:
        reject_list.append(row)

with open("data/processed/accepted.json", "w") as f:
    json.dump(accept_list, f, indent=2)

with open("data/processed/rejected.json", "w") as f:
    json.dump(reject_list, f, indent=2)