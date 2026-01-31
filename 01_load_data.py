import pandas as pd
import os

# Define file paths
path_orders = 'data/orders.csv'
path_products = 'data/products.csv'
path_train = 'data/order_products__train.csv'

print("⏳ Loading datasets... Please wait.")

try:
    # Load datasets
    df_orders = pd.read_csv(path_orders)
    df_products = pd.read_csv(path_products)
    df_train = pd.read_csv(path_train)

    print("✅ Success: All datasets loaded correctly.\n")

    # 1. Inspect Orders Data
    print("--- ORDERS DATA SAMPLE ---")
    print(df_orders.head())
    print("-" * 30)
    
    # 2. Inspect Products Data
    print("--- PRODUCTS DATA SAMPLE ---")
    print(df_products.head())
    print(f"Total Unique Products: {df_products['product_id'].nunique()}")
    print("-" * 30)

    # 3. Inspect Train Data (Basket Details)
    print("--- ORDER_PRODUCTS_TRAIN SAMPLE ---")
    print(df_train.head())
    print("-" * 30)

    # 4. Data Dimensions
    print("\n--- DATA DIMENSIONS ---")
    print(f"Orders Table Shape: {df_orders.shape}")
    print(f"Products Table Shape: {df_products.shape}")
    print(f"Train Table Shape: {df_train.shape}")

    # 5. Check for Missing Values
    print("\n--- MISSING VALUE CHECK ---")
    print(f"Missing in Orders: {df_orders.isnull().sum().sum()}")
    print(f"Missing in Products: {df_products.isnull().sum().sum()}")
    print(f"Missing in Train: {df_train.isnull().sum().sum()}")

except FileNotFoundError:
    print("❌ Error: File not found. Please check your 'data' folder and filenames.")