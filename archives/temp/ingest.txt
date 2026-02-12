import pandas as pd

raw_data = pd.read_csv('data/raw/retail_store_sales.csv')

#Trimming Whitespace (leaading/trailing), Correct format on Capitlization
columns = ['Transaction ID', 'Customer ID', 'Category', 'Item', 'Payment Method', 'Location']
raw_data[columns] = raw_data[columns].apply(lambda s: s.str.strip().str.title())
#print(raw_data["Transaction ID"].unique())

#Checking for null values
new_columns_reject_null = ['Transaction ID', 'Customer ID', 'Category', 'Item', 'Price Per Unit', 'Quantity', 'Total Spent', 'Payment Method', 'Location', 'Transaction Date']
reject_tables_null = raw_data[new_columns_reject_null].isna().any(axis=1);

rejected_df = raw_data[reject_tables_null].copy()
valid_df = raw_data[~reject_tables_null].copy()
 
print(rejected_df.head())
