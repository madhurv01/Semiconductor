import pandas as pd

print("--- Generating Synthetic Logistics & Coordinate Data for Karnataka ---")

# --- DATA: Realistic coordinates for major districts and hubs ---

district_data = {
    'district': ['Bagalkote', 'Bangalore Urban', 'Bangalore Rural', 'Belagavi', 'Bellary', 'Bidar', 'Chamarajanagar',
                 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad',
                 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru',
                 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir'],
    'latitude': [16.18, 12.97, 13.15, 15.85, 15.14, 17.91, 11.92, 13.43, 13.31, 14.22, 12.91, 14.46, 15.46,
                 15.42, 13.06, 14.79, 17.33, 12.42, 13.13, 15.35, 12.52, 12.30, 16.20, 12.75, 13.93, 13.34,
                 13.34, 14.82, 16.83, 16.75],
    'longitude': [75.70, 77.59, 77.48, 74.50, 76.92, 77.52, 76.94, 77.72, 75.77, 76.40, 74.85, 75.92, 75.00,
                  75.62, 76.09, 75.40, 76.83, 75.72, 78.13, 76.15, 76.89, 76.65, 77.34, 77.20, 75.57, 77.11,
                  74.74, 74.52, 75.83, 77.14]
}

# Real-world major logistics hubs relevant to Karnataka
hubs_data = {
    'hub_type': ['Seaport', 'Airport', 'Chemical Hub'],
    'hub_name': ['New Mangalore Port', 'Kempegowda International Airport (BLR)', 'Mangalore Chemical Zone'],
    'latitude': [12.92, 13.19, 12.96],
    'longitude': [74.83, 77.70, 74.87]
}

# --- Create and Save DataFrames ---
df_districts = pd.DataFrame(district_data)
df_hubs = pd.DataFrame(hubs_data)

district_output_path = 'data/karnataka_district_coords.csv'
hubs_output_path = 'data/logistics_hubs.csv'

df_districts.to_csv(district_output_path, index=False)
print(f"Successfully generated district coordinates file: {district_output_path}")

df_hubs.to_csv(hubs_output_path, index=False)
print(f"Successfully generated logistics hubs file: {hubs_output_path}")

print("--- Data Generation Complete ---")