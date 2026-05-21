import json
import pandas as pd

# Read the CSV
df = pd.read_csv('site_name_sorting.csv')

# Parse the JSON data
data_json = json.loads(df['data'].iloc[0])

# Extract site names
sites = []
for i, site in enumerate(data_json):
    sites.append({
        'row': i + 1,
        'site_number': site['site_number'],
        'site_name': site['site_name']
    })

# Display actual order
print('=== ACTUAL ORDER (as returned by function) ===')
for s in sites:
    print(f'{s["row"]:2d}: "{s["site_name"]}" (Site: {s["site_number"]})')

# Check if it's in descending order
print('\n=== CHECKING IF DESCENDING ORDER ===')
site_names = [s['site_name'] for s in sites]
sorted_desc = sorted(site_names, reverse=True)

print('\nExpected DESC order (first 20):')
for i, name in enumerate(sorted_desc[:20], 1):
    print(f'{i:2d}: "{name}"')

# Comparison
print('\n=== COMPARISON ===')
matches = all(site_names[i] == sorted_desc[i] for i in range(len(site_names)))
print(f'Does actual match expected DESC order? {matches}')

if not matches:
    print('\n❌ SORTING IS BROKEN! Mismatches found:')
    for i in range(len(site_names)):
        if site_names[i] != sorted_desc[i]:
            print(f'Position {i+1:2d}: Got "{site_names[i]}", Expected "{sorted_desc[i]}"')
else:
    print('\n✅ Sorting is correct!')
