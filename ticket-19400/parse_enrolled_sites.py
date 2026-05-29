"""
Extract unique site IDs from DSGS enrolled site list CSV
This creates the dynamic array for KQL validation query
"""

import csv
from pathlib import Path

# Input file
csv_file = Path(__file__).parent / "leap_meters_export_05282026.csv"

# Read CSV and extract site IDs
site_ids = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        site_id = row['Asset Registry Site ID (partner_reference)']
        if site_id:  # Ensure not empty
            site_ids.append(site_id)

# Get unique site IDs
unique_site_ids = sorted(set(site_ids))

print(f"Total rows in CSV: {len(site_ids)}")
print(f"Unique site IDs: {len(unique_site_ids)}")
print(f"Duplicates (if any): {len(site_ids) - len(unique_site_ids)}")

# Generate KQL dynamic array format
print("\n" + "="*80)
print("KQL DYNAMIC ARRAY (Copy to KQL query):")
print("="*80)

# Format as KQL dynamic array with 10 IDs per line
kql_array = "let enrolled_dsgs_sites = dynamic([\n"
for i in range(0, len(unique_site_ids), 10):
    batch = unique_site_ids[i:i+10]
    kql_array += "    "
    kql_array += ", ".join([f'"{sid}"' for sid in batch])
    if i + 10 < len(unique_site_ids):
        kql_array += ",\n"
    else:
        kql_array += "\n"
kql_array += "]);\n"

print(kql_array)

# Save to file
output_file = Path(__file__).parent / "enrolled_sites_kql_array.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(kql_array)

print(f"\n✅ KQL array saved to: {output_file.name}")

# Generate summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS:")
print("="*80)
print(f"Total enrolled sites: {len(unique_site_ids)}")

# Count by site ID prefix (400 series vs 100 series)
site_400_series = [s for s in unique_site_ids if s.startswith('400')]
site_100_series = [s for s in unique_site_ids if s.startswith('100')]
site_others = [s for s in unique_site_ids if not s.startswith('400') and not s.startswith('100')]

print(f"  - 400-series sites: {len(site_400_series)}")
print(f"  - 100-series sites: {len(site_100_series)}")
if site_others:
    print(f"  - Other series: {len(site_others)}")

print("\nFirst 10 site IDs:")
for sid in unique_site_ids[:10]:
    print(f"  - {sid}")

print("\nLast 10 site IDs:")
for sid in unique_site_ids[-10:]:
    print(f"  - {sid}")
