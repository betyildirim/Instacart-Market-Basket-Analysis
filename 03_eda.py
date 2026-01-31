import pandas as pd
import plotly.express as px

# 1. Load & Merge Data (Same as before)
print("⏳ Preparing data for analysis...")
df_orders = pd.read_csv('data/orders.csv')
df_products = pd.read_csv('data/products.csv')
df_train = pd.read_csv('data/order_products__train.csv')

df_merged = pd.merge(df_train, df_products, on='product_id', how='left')
df_merged = pd.merge(df_merged, df_orders, on='order_id', how='left')

print("✅ Data ready! Generating charts...")

# --- CHART 1: TOP 10 BEST SELLING PRODUCTS ---
print("📊 Creating Product Chart...")
top_products = df_merged['product_name'].value_counts().head(10).reset_index()
top_products.columns = ['product_name', 'count']

fig1 = px.bar(top_products, 
              x='count', 
              y='product_name', 
              orientation='h',
              title='Top 10 Best Selling Products',
              labels={'count': 'Number of Sales', 'product_name': 'Product'},
              color='count',
              color_continuous_scale='Viridis')

# --- CHART 2: BUSIEST DAYS OF THE WEEK ---
print("📊 Creating Day of Week Chart...")
day_counts = df_merged['order_dow'].value_counts().sort_index().reset_index()
day_counts.columns = ['day_of_week', 'order_count']

# Map numbers to day names (0=Sunday, 1=Monday...)
days_map = {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}
day_counts['day_name'] = day_counts['day_of_week'].map(days_map)

fig2 = px.bar(day_counts, 
              x='day_name', 
              y='order_count',
              title='Total Orders by Day of Week',
              labels={'order_count': 'Total Orders', 'day_name': 'Day'},
              color='order_count')

# Show Charts
fig1.show()
fig2.show()

print("✅ Done! Check your browser for the graphs.")