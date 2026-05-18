import pandas as pd

# Read Excel file
df = pd.read_excel('Initial DSGS Site List 2026.xlsx')

# Get Site Id column
site_ids = df['Site Id'].astype(str).dropna().tolist()

# Remove any empty or invalid values
site_ids = [str(sid).strip() for sid in site_ids if str(sid).strip() and str(sid) != 'nan']

print(f'Total sites found: {len(site_ids)}')

# Configuration
sites_per_line = 10  # Number of site IDs per line

# Also create version with 20 per line
sites_per_line_v2 = 20

# Write to file with multiple sites per line (10 per line)
with open('dsgs_site_list_array_compact.kql', 'w') as f:
    f.write('// DSGS 2026 Site List - Auto-generated from Excel (Compact Format)\n')
    f.write(f'// Total sites: {len(site_ids)}\n')
    f.write(f'// Format: {sites_per_line} site IDs per line\n')
    f.write('// Source: Initial DSGS Site List 2026.xlsx\n\n')
    f.write('let dsgs_site_list = dynamic([\n')
    
    for i in range(0, len(site_ids), sites_per_line):
        chunk = site_ids[i:i+sites_per_line]
        
        # Format each chunk on one line
        formatted_chunk = ', '.join([f'"{sid}"' for sid in chunk])
        
        # Add comma at end if not last line
        if i + sites_per_line < len(site_ids):
            f.write(f'    {formatted_chunk},\n')
        else:
            f.write(f'    {formatted_chunk}\n')
    
    f.write(']);\n')

# Also create version with 20 sites per line
with open('dsgs_site_list_array_compact_20.kql', 'w') as f:
    f.write('// DSGS 2026 Site List - Auto-generated from Excel (Ultra Compact Format)\n')
    f.write(f'// Total sites: {len(site_ids)}\n')
    f.write(f'// Format: {sites_per_line_v2} site IDs per line\n')
    f.write('// Source: Initial DSGS Site List 2026.xlsx\n\n')
    f.write('let dsgs_site_list = dynamic([\n')

    for i in range(0, len(site_ids), sites_per_line_v2):
        chunk = site_ids[i:i+sites_per_line_v2]

        # Format each chunk on one line
        formatted_chunk = ', '.join([f'"{sid}"' for sid in chunk])

        # Add comma at end if not last line
        if i + sites_per_line_v2 < len(site_ids):
            f.write(f'    {formatted_chunk},\n')
        else:
            f.write(f'    {formatted_chunk}\n')

    f.write(']);\n')

print(f'Success! Created both versions:')
print(f'  - dsgs_site_list_array_compact.kql (~{len(site_ids) // sites_per_line} lines with 10 sites/line)')
print(f'  - dsgs_site_list_array_compact_20.kql (~{len(site_ids) // sites_per_line_v2} lines with 20 sites/line)')
