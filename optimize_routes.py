import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load shipment dataset
df = pd.read_csv('shipments.csv')

# 2. Vectorized Haversine Distance Function
def haversine_np(lat1, lon1, lat2, lon2):
    r = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return r * c

df['Distance_KM'] = haversine_np(
    df['Origin_Lat'], df['Origin_Lon'], 
    df['Dest_Lat'], df['Dest_Lon']
).round(2)

# 3. Freight Cost Modeling
df['Distance_Cost'] = df['Distance_KM'] * 1.20
df['Weight_Cost'] = df['Weight_KG'] * 0.05
df['Subtotal'] = df['Base_Rate_EUR'] + df['Distance_Cost'] + df['Weight_Cost']
df['Fuel_Surcharge'] = df['Subtotal'] * 0.12
df['Total_Freight_Cost'] = (df['Subtotal'] + df['Fuel_Surcharge']).round(2)

# 4. Transport Efficiency Metric (Cost per Ton-KM)
df['Ton_KM'] = (df['Weight_KG'] / 1000.0) * df['Distance_KM']
df['Cost_Per_Ton_KM'] = (df['Total_Freight_Cost'] / df['Ton_KM']).round(4)

# 5. Lane-Level Payload Consolidation Summary
lane_summary = df.groupby(['Origin', 'Destination']).agg(
    Shipment_Count=('Shipment_ID', 'count'),
    Total_Weight_KG=('Weight_KG', 'sum'),
    Total_Volume_M3=('Volume_M3', 'sum'),
    Avg_Cost_Per_Ton_KM=('Cost_Per_Ton_KM', 'mean'),
    Total_Freight_Spend=('Total_Freight_Cost', 'sum')
).reset_index()

# Estimate 24-Ton Truckload Capacity Requirements
lane_summary['Est_Full_Truckloads_Needed'] = np.ceil(lane_summary['Total_Weight_KG'] / 24000).astype(int)

# Export output to Excel
with pd.ExcelWriter('optimized_freight_routes.xlsx') as writer:
    df.to_excel(writer, sheet_name='Shipment_Details', index=False)
    lane_summary.to_excel(writer, sheet_name='Lane_Consolidation_Summary', index=False)

# 6. Generate Efficiency Distribution Visualization
plt.figure(figsize=(10, 5))
sns.histplot(df['Cost_Per_Ton_KM'], kde=True, color='teal', bins=30)
plt.title('Distribution of Freight Transport Efficiency (Cost per Ton-KM)', fontsize=12, fontweight='bold')
plt.xlabel('Cost per Ton-KM (€)', fontsize=10)
plt.ylabel('Shipment Frequency', fontsize=10)
plt.tight_layout()
plt.savefig('freight_efficiency_distribution.png')

print("Route optimization and freight cost modeling execution complete.")
print(f"Processed {len(df)} shipments across {len(lane_summary)} unique transport lanes.")