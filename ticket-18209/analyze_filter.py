import json
import pandas as pd

# Read both CSVs
df_no_filter = pd.read_csv('external_reference_id_no_filter.csv')
df_with_filter = pd.read_csv('external_reference_id_filter.csv')

# Parse JSON data
data_no_filter = json.loads(df_no_filter['data'].iloc[0])
data_with_filter = json.loads(df_with_filter['data'].iloc[0])

# Find all records containing "56" in external_reference_id
print('=== WITHOUT FILTER - External Ref IDs containing "56" ===')
refs_with_56 = []
for site in data_no_filter:
    ext_ref = str(site['external_reference_id'])
    if '56' in ext_ref:
        refs_with_56.append({
            'site_number': site['site_number'],
            'external_reference_id': ext_ref
        })
        print(f'{len(refs_with_56):2d}: Site {site["site_number"]} - {ext_ref}')

print(f'\n📊 Total records containing "56" (manual count): {len(refs_with_56)}')

# Show filter results
print('\n=== WITH FILTER - Results Returned ===')
for i, site in enumerate(data_with_filter, 1):
    print(f'{i:2d}: Site {site["site_number"]} - {site["external_reference_id"]}')

print(f'\n📊 Total returned by filter: {len(data_with_filter)}')

# Comparison
print('\n=== COMPARISON ===')
print(f'Expected (manual count): {len(refs_with_56)} records')
print(f'Actual (filter returned): {len(data_with_filter)} records')

if len(refs_with_56) == len(data_with_filter):
    print('✅ Filter is working correctly!')
else:
    print(f'❌ FILTER BUG! Missing {len(refs_with_56) - len(data_with_filter)} records!')
    
# Metadata check
metadata_no_filter = json.loads(df_no_filter['metadata'].iloc[0])
metadata_with_filter = json.loads(df_with_filter['metadata'].iloc[0])

print('\n=== METADATA COMPARISON ===')
print(f'No filter - total_records_count: {metadata_no_filter["pagination"]["total_records_count"]}')
print(f'With filter - total_count: {metadata_with_filter["pagination"]["total_count"]}')
print(f'With filter - total_records_count: {metadata_with_filter["pagination"]["total_records_count"]}')

if metadata_with_filter["pagination"]["total_count"] == len(refs_with_56):
    print('✅ total_count is correct!')
else:
    print(f'❌ total_count is WRONG! Expected {len(refs_with_56)}, got {metadata_with_filter["pagination"]["total_count"]}')
