import pandas as pd

# Read Excel file
df = pd.read_excel('Initial DSGS Site List 2026.xlsx')

# Get Site Id column
site_ids = df['Site Id'].astype(str).dropna().tolist()

# Remove any empty or invalid values
site_ids = [str(sid).strip() for sid in site_ids if str(sid).strip() and str(sid) != 'nan']

print(f'Total sites found: {len(site_ids)}')
print(f'First 5 sites: {site_ids[:5]}')
print(f'Last 5 sites: {site_ids[-5:]}')

# Write to file
with open('dsgs_site_list_array.kql', 'w') as f:
    f.write('// DSGS 2026 Site List - Auto-generated from Excel\n')
    f.write(f'// Total sites: {len(site_ids)}\n')
    f.write('// Source: Initial DSGS Site List 2026.xlsx\n\n')
    f.write('let dsgs_site_list = dynamic([\n')
    
    for i, site_id in enumerate(site_ids):
        if i == len(site_ids) - 1:  # Last item - no comma
            f.write(f'    "{site_id}"\n')
        else:
            f.write(f'    "{site_id}",\n')
    
    f.write(']);\n')

print(f'\nSuccess! Created: dsgs_site_list_array.kql')
