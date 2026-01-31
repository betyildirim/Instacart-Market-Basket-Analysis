import pandas as pd

# 1. Load Association Rules
print("⏳ Loading rules...")
rules = pd.read_csv('market_basket_rules.csv')

# 2. Define Recommendation Function
def get_recommendation(product_name):
    """
    Looks up the best product to recommend based on the input product.
    """
    print(f"\n🔍 Searching for matches for: '{product_name}'...")
    
    # Filter rules where the antecedent contains the input product
    # Note: The CSV saves sets as strings (e.g., "frozenset({'Limes'})"), so we search within that string.
    matches = rules[rules['antecedents'].astype(str).str.contains(product_name, case=False, na=False)]
    
    if not matches.empty:
        # Sort by Lift to find the strongest association
        best_match = matches.sort_values('lift', ascending=False).iloc[0]
        
        # Clean up the string format to get the clean product name
        # "frozenset({'Product Name'})" -> "Product Name"
        recommended_product = best_match['consequents'].replace("frozenset({'", "").replace("'})", "")
        lift_score = best_match['lift']
        
        print("✅ RECOMMENDATION FOUND!")
        print(f"👉 Customers who buy '{product_name}' also buy: **{recommended_product}**")
        print(f"📈 Lift Score: {lift_score:.2f}")
    else:
        print("❌ No strong recommendation found for this item in the top 100 list.")

# --- TEST SCENARIOS ---
# Testing the engine with products known to have strong associations
get_recommendation("Limes")
get_recommendation("Organic Raspberries")
get_recommendation("Organic Whole Milk")