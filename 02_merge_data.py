import pandas as pd

# 1. Load Datasets
print("⏳ Loading data...")
df_orders = pd.read_csv('data/orders.csv')
df_products = pd.read_csv('data/products.csv')
df_train = pd.read_csv('data/order_products__train.csv')

# 2. Merge Datasets
print("🔗 Merging tables...")

# Step A: Merge Train with Products to get Product Names
# (Left join on 'product_id')
df_merged = pd.merge(df_train, df_products, on='product_id', how='left')

# Step B: Merge with Orders to get User Info
# (Left join on 'order_id')
df_merged = pd.merge(df_merged, df_orders, on='order_id', how='left')

# 3. Validation & Output
print("✅ Merge Completed Successfully!")
print(f"Final Data Shape: {df_merged.shape}\n")

print("--- MERGED DATA SAMPLE ---")
# Select key columns for display
cols_to_show = ['user_id', 'product_name', 'order_dow', 'order_hour_of_day', 'days_since_prior_order']
print(df_merged[cols_to_show].head())