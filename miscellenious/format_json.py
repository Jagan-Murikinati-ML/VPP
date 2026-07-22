import json

print("Reading CSV file...")
# Read the CSV file
with open('ticket-12654/getVPPSiteLevelPerformance_results.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"File has {len(lines)} lines")

# The JSON is on line 2 (index 1), but it's escaped
json_str = lines[1].strip()

print("Cleaning JSON string...")
# Remove the outer quotes if present
if json_str.startswith('"') and json_str.endswith('"'):
    json_str = json_str[1:-1]

# Unescape the double quotes
json_str = json_str.replace('""', '"')

print("Parsing JSON...")
# Parse and pretty-print the JSON
data = json.loads(json_str)

print(f"Total sites: {len(data)}")

# Write formatted JSON to a new file
print("Writing formatted JSON...")
with open('ticket-12654/getVPPSiteLevelPerformance_results_formatted.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('✅ Done! Created: ticket-12654/getVPPSiteLevelPerformance_results_formatted.json')
print(f'\nSample (first site):')
print(json.dumps(data[0], indent=2))

# Count NaN values
nan_count = sum(1 for site in data if site.get('battery_power') == 'NaN')
print(f'\n🔍 Sites with battery_power = "NaN": {nan_count} out of {len(data)}')
