import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# 1. Load Data
print("⏳ Loading datasets...")
df_orders = pd.read_csv('data/orders.csv')
df_products = pd.read_csv('data/products.csv')
df_train = pd.read_csv('data/order_products__train.csv')

# Merge to get Product Names
df_merged = pd.merge(df_train, df_products, on='product_id', how='left')

# 2. Optimize Data (Focus on Top 100 Best Sellers)
print("🧹 Filtering for Top 100 popular products...")
top_products = df_merged['product_name'].value_counts().head(100).index
df_filtered = df_merged[df_merged['product_name'].isin(top_products)]

print(f"✅ Data filtered. Analysis will be performed on {df_filtered.shape[0]} transactions.")

# 3. Create Basket Matrix
print("📦 Creating Basket Matrix... (This might take a moment)")
basket = df_filtered.groupby(['order_id', 'product_name'])['product_id'].count().unstack().reset_index().fillna(0).set_index('order_id')

# --- OPTIMIZATION FIX ---
# We convert values to Boolean (True/False) to fix the warning and speed up calculation
basket = (basket > 0).astype(bool)
print("✅ Basket Matrix Ready (Boolean Type)!")

# 4. Apply Apriori Algorithm
print("🧠 Running Apriori Algorithm...")
# min_support=0.01: Itemsets must appear in at least 1% of transactions
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)

# 5. Generate Association Rules
print("🔗 Generating Rules...")
# Metric="lift": Looking for strong associations
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# Sort rules by "Lift"
rules = rules.sort_values(['lift'], ascending=False)

# 6. Output Results
print("\n🎉 TOP 10 PRODUCT ASSOCIATION RULES 🎉")
# Formatting the output for better readability
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

# Save results
rules.to_csv('market_basket_rules.csv', index=False)
print("\n💾 Rules saved to 'market_basket_rules.csv'")