import pandas as pd

# 1. Load Rules
print("⏳ Loading the brain of the system...")
rules = pd.read_csv('market_basket_rules.csv')

# Clean up the product names in the rules to make them readable
# (Removing "frozenset" characters)
rules['antecedents'] = rules['antecedents'].astype(str).str.replace("frozenset({'", "").str.replace("'})", "").str.replace("'", "")
rules['consequents'] = rules['consequents'].astype(str).str.replace("frozenset({'", "").str.replace("'})", "").str.replace("'", "")

# 2. Show Capacity
print(f"\n✅ SYSTEM READY! I have {len(rules)} different rules in my memory.")
print("-" * 50)

# Get unique products that trigger a recommendation
available_products = rules['antecedents'].unique()

print("📋 PRODUCTS I CAN RECOMMEND FOR:")
print(available_products)
print("-" * 50)

# 3. Interactive Loop
while True:
    user_input = input("\n🛒 Enter a product name (or 'q' to quit): ")
    
    if user_input.lower() == 'q':
        print("👋 Bye!")
        break
    
    # Search for the product
    match = rules[rules['antecedents'].str.contains(user_input, case=False)]
    
    if not match.empty:
        # Get the best recommendation (highest lift)
        best = match.sort_values('lift', ascending=False).iloc[0]
        
        print(f"\n💡 RECOMMENDATION: If you buy '{best['antecedents']}', you should buy '{best['consequents']}'!")
        print(f"📊 Confidence (Lift): {best['lift']:.2f}")
    else:
        print("❌ I don't have a rule for that specific product yet.")