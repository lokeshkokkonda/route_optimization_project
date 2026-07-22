import pandas as pd
import numpy as np

np.random.seed(42)

# Coordinates for major European logistics hubs
cities = {
    'Hamburg': (53.5511, 9.9937),
    'Berlin': (52.5200, 13.4050),
    'Munich': (48.1371, 11.5761),
    'Frankfurt': (50.1109, 8.6821),
    'Cologne': (50.9375, 6.9603),
    'Kiel': (54.3233, 10.1228)
}

city_names = list(cities.keys())
data = []

for i in range(1, 501):
    origin, dest = np.random.choice(city_names, size=2, replace=False)
    origin_coords = cities[origin]
    dest_coords = cities[dest]
    
    weight_kg = int(np.random.uniform(500, 12000))
    volume_m3 = round(float(weight_kg / np.random.uniform(200, 350)), 2)
    base_rate = round(float(np.random.uniform(150, 400)), 2)

    data.append({
        'Shipment_ID': f"SHP-{i:04d}",
        'Origin': origin,
        'Origin_Lat': origin_coords[0],
        'Origin_Lon': origin_coords[1],
        'Destination': dest,
        'Dest_Lat': dest_coords[0],
        'Dest_Lon': dest_coords[1],
        'Weight_KG': weight_kg,
        'Volume_M3': volume_m3,
        'Base_Rate_EUR': base_rate
    })

df = pd.DataFrame(data)
df.to_csv('shipments.csv', index=False)
print(f"Successfully generated {len(df)} shipment records in shipments.csv")