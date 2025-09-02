import pandas as pd
import numpy as np

print("--- Generating Synthetic Water Source Data for Karnataka ---")

# Data based on real-world sources and typical water quality ranges in the region.
# This makes the analysis more authentic.
data = {
    'district': [
        'Bagalkote', 'Bangalore Urban', 'Bangalore Rural', 'Belagavi', 'Bellary',
        'Bidar', 'Chamarajanagar', 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga',
        'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri',
        'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur',
        'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir'
    ],
    'source_name': [
        'Ghataprabha River', 'Arkavathi River', 'Kaveri River (near Mekedatu)', 'Krishna River', 'Tungabhadra Reservoir',
        'Manjara River', 'Kaveri River (near Shivanasamudra)', 'Palar River', 'Bhadra Reservoir', 'Vedavathi River',
        'Netravati River', 'Tunga River', 'Malaprabha River', 'Tungabhadra River', 'Hemavathi Reservoir', 'Varada River',
        'Bhima River', 'Kaveri River (Talakaveri)', 'Ponnaiyar River', 'Tungabhadra River', 'KRS Reservoir', 'Kabini Reservoir', 'Krishna River',
        'Arkavathi Reservoir', 'Tunga Reservoir', 'Jayathi River', 'Swarna River', 'Kali River', 'Krishna River', 'Krishna River'
    ],
    'source_type': [
        'River', 'River', 'River', 'River', 'Reservoir', 'River', 'River', 'River', 'Reservoir', 'River', 'River',
        'River', 'River', 'River', 'Reservoir', 'River', 'River', 'River', 'River', 'River', 'Reservoir', 'Reservoir',
        'River', 'Reservoir', 'Reservoir', 'River', 'River', 'River', 'River', 'River'
    ],
    'distance_from_center_km': [
        15, 25, 30, 20, 10, 22, 18, 28, 12, 19, 8, 14, 16, 25, 9, 17, 24, 5, 30, 26, 11, 7, 21, 13, 6, 23, 10, 15, 18, 20
    ]
}

df = pd.DataFrame(data)

# --- Generate Realistic Water Quality Metrics ---
# These ranges are typical for untreated surface water in the region.
# np.random.uniform(low, high, size)
df['total_dissolved_solids_ppm'] = np.random.uniform(150, 450, df.shape[0]).round(2)
df['ph_level'] = np.random.uniform(6.8, 8.2, df.shape[0]).round(2)
df['hardness_mg_L'] = np.random.uniform(80, 250, df.shape[0]).round(2)
df['turbidity_ntu'] = np.random.uniform(5, 40, df.shape[0]).round(2)
df['silica_mg_L'] = np.random.uniform(10, 50, df.shape[0]).round(2)

# Specific tuning for known excellent/poor sources to make it more realistic
# Dakshina Kannada (Netravati) is known for good quality water
df.loc[df['district'] == 'Dakshina Kannada', ['total_dissolved_solids_ppm', 'hardness_mg_L', 'turbidity_ntu']] = [120.5, 75.2, 4.8]
# Kalaburagi (Bhima) can have higher TDS
df.loc[df['district'] == 'Kalaburagi', ['total_dissolved_solids_ppm', 'hardness_mg_L', 'turbidity_ntu']] = [480.2, 280.6, 35.1]
# Mysuru (Kabini) is generally good quality
df.loc[df['district'] == 'Mysuru', ['total_dissolved_solids_ppm', 'hardness_mg_L', 'turbidity_ntu']] = [165.7, 90.3, 8.2]


# --- Save to CSV ---
output_path = 'data/karnataka_water_sources.csv'
df.to_csv(output_path, index=False)

print(f"Successfully generated synthetic water dataset with {len(df)} sources.")
print(f"File saved to: {output_path}")