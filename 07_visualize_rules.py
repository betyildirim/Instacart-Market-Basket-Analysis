import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import textwrap

# --- CONFIGURATION ---
TOP_RULES_COUNT = 15   
NODE_SIZE = 6000       
FONT_SIZE = 9          
WRAP_WIDTH = 12        

# 1. Data Preparation
print("⏳ Preparing data...")
rules = pd.read_csv('market_basket_rules.csv')

# Clean product names for better visualization
rules['antecedents'] = rules['antecedents'].astype(str).str.replace("frozenset({'", "").str.replace("'})", "").str.replace("'", "").str.replace("Organic ", "Org. ").str.replace("Bag of ", "")
rules['consequents'] = rules['consequents'].astype(str).str.replace("frozenset({'", "").str.replace("'})", "").str.replace("'", "").str.replace("Organic ", "Org. ").str.replace("Bag of ", "")

# Select top rules
top_rules = rules.sort_values('lift', ascending=False).head(TOP_RULES_COUNT)
G = nx.from_pandas_edgelist(top_rules, source='antecedents', target='consequents', edge_attr='lift')

# 2. Canvas Setup
plt.figure(figsize=(24, 13)) 
ax = plt.gca()

# 3. Layout Optimization
print("🕸️ Calculating graph layout...")
pos = nx.spring_layout(G, k=3.5, seed=42, iterations=100)

# 4. Drawing the Graph

# A. Nodes
degrees = dict(G.degree)
node_colors = [degrees[n] for n in G.nodes]

nx.draw_networkx_nodes(G, pos, 
                       node_size=NODE_SIZE, 
                       node_color=node_colors, 
                       cmap=plt.cm.coolwarm, 
                       alpha=0.95,
                       edgecolors='#333333', linewidths=2)

# B. Edges
edges = G.edges(data=True)
weights = [data['lift']**2 for u, v, data in edges]
nx.draw_networkx_edges(G, pos, width=weights, edge_color='#666666', alpha=0.5, 
                       arrows=True, arrowstyle='-|>', arrowsize=30)

# C. Labels
labels = {node: textwrap.fill(node, width=WRAP_WIDTH) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=FONT_SIZE, 
                        font_family='sans-serif', font_weight='bold', font_color='black')

# Zoom Out Adjustment (Margins)
ax.margins(0.15) 

# 5. Legends

# Legend 1: Interaction Strength
legend_lines = [
    Line2D([0], [0], color='#666666', linewidth=2, label='Moderate (Lift ≈ 2)'),
    Line2D([0], [0], color='#666666', linewidth=8, label='Strong (Lift ≈ 4)'),
    Line2D([0], [0], color='#666666', linewidth=15, label='Very Strong (Lift > 6)')
]

first_legend = plt.legend(handles=legend_lines, 
                          bbox_to_anchor=(1.02, 1), loc='upper left', 
                          title='Interaction Strength (Line Width)', fontsize=11, title_fontsize=12, 
                          frameon=True, shadow=True, facecolor='#f8f9fa', borderpad=1)
plt.gca().add_artist(first_legend)

# Legend 2: Product Importance
legend_circles = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#b40426', markersize=18, label='High Centrality (Hub Product)'), 
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#3b4cc0', markersize=18, label='Standard Product')             
]

plt.legend(handles=legend_circles, 
           bbox_to_anchor=(1.02, 0.78), loc='upper left',
           title='Product Importance (Color)', fontsize=11, title_fontsize=12, 
           frameon=True, shadow=True, facecolor='#f8f9fa', borderpad=1)

# 6. Final Adjustments and Saving
plt.subplots_adjust(left=0.10, right=0.78, top=0.90, bottom=0.10)
plt.suptitle("Market Basket Analysis: Product Association Network", fontsize=28, fontweight='bold', color='#2c3e50')
plt.axis('off')

output_file = 'market_basket_network_graph.png'
plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Visualization saved: '{output_file}'")
plt.show()