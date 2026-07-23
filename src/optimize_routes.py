import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# 1. Load raw dataset
df = pd.read_csv('data/raw/shipments.csv')

# 2. Vectorized Haversine Distance Calculation (km)
def haversine_np(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

df['Distance_KM'] = haversine_np(
    df['Origin_Lon'], df['Origin_Lat'], 
    df['Dest_Lon'], df['Dest_Lat']
).round(2)

# 3. Freight Cost Modeling
rate_per_km = 1.20
rate_per_kg = 0.05
fuel_surcharge_pct = 0.12

subtotal = df['Base_Rate_EUR'] + (df['Distance_KM'] * rate_per_km) + (df['Weight_KG'] * rate_per_kg)
df['Total_Freight_Cost'] = (subtotal * (1 + fuel_surcharge_pct)).round(2)

# 4. Ton-KM Efficiency Metric
df['Ton_KM'] = (df['Weight_KG'] / 1000.0) * df['Distance_KM']
df['Cost_Per_Ton_KM'] = (df['Total_Freight_Cost'] / df['Ton_KM']).round(3)

# 5. Lane Consolidation Analysis (FTL vs LTL)
truck_capacity_kg = 24000
lane_summary = df.groupby(['Origin', 'Destination']).agg(
    Total_Shipments=('Shipment_ID', 'count'),
    Total_Weight_KG=('Weight_KG', 'sum'),
    Total_Freight_Cost=('Total_Freight_Cost', 'sum'),
    Avg_Distance_KM=('Distance_KM', 'mean')
).reset_index()

lane_summary['Full_Truckloads_Required'] = np.ceil(lane_summary['Total_Weight_KG'] / truck_capacity_kg).astype(int)

# Save processed output
df.to_csv('data/processed/optimized_shipments.csv', index=False)
lane_summary.to_excel('data/processed/lane_consolidation_summary.xlsx', index=False)

# 6. Generate Route Cost Efficiency Visualization
plt.figure(figsize=(10, 5))
ax = sns.barplot(
    data=lane_summary, 
    x='Origin', 
    y='Total_Freight_Cost', 
    hue='Origin', 
    palette='viridis', 
    legend=False
)
plt.title('Total Freight Spend by Origin City', fontsize=14, fontweight='bold')
plt.xlabel('Origin', fontsize=12)
plt.ylabel('Total Spend (€)', fontsize=12)

for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(
            f'€{height:,.0f}',
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0, 3),
            textcoords='offset points'
        )

plt.tight_layout()
plt.savefig('reports/freight_spend_chart.png', dpi=300)
plt.close()

print("Route optimization complete. Outputs saved to data/processed/ and chart saved to reports/")