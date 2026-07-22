import pandas as pd

print("=" * 80)
print("🔋 BATTERY DISCHARGE CALCULATION FOR SITE 400000837")
print("=" * 80)

# Read the CSV file
df = pd.read_csv('ticket-12654/400000837_data.csv')

print(f"\n📊 Data Overview:")
print(f"Total telemetry readings: {len(df)}")
print(f"Time range: {df['sourceTimestamp'].min()} to {df['sourceTimestamp'].max()}")

# Extract relevant columns
df['sourceTimestamp'] = pd.to_datetime(df['sourceTimestamp'])
df['battery_200_IncWhExp'] = df['battery_200_IncWhExp'].astype(float)
df['battery_713_SoC'] = df['battery_713_SoC'].astype(float)

# Sort by timestamp
df = df.sort_values('sourceTimestamp')

print(f"\n" + "=" * 80)
print("METHOD 1: Sum of Incremental Discharge (battery_200_IncWhExp)")
print("=" * 80)

# Calculate total discharge
total_discharge_wh = df['battery_200_IncWhExp'].sum()
total_discharge_kwh = total_discharge_wh / 1000.0

print(f"\n📋 Breakdown by timestamp:")
print("-" * 80)
for idx, row in df.iterrows():
    print(f"{row['sourceTimestamp']}  |  IncWhExp: {row['battery_200_IncWhExp']:>6.0f} Wh  |  SOC: {row['battery_713_SoC']:>6.2f}%")

print(f"\n" + "-" * 80)
print(f"✅ Total Discharge (Wh):  {total_discharge_wh:,.0f} Wh")
print(f"✅ Total Discharge (kWh): {total_discharge_kwh:,.3f} kWh")
print("=" * 80)

print(f"\n" + "=" * 80)
print("METHOD 2: SOC Drop Estimation")
print("=" * 80)

soc_start = df.iloc[0]['battery_713_SoC']   # First reading (earliest time)
soc_end = df.iloc[-1]['battery_713_SoC']    # Last reading (latest time)
soc_drop = soc_start - soc_end

print(f"\nSOC at START (07:15): {soc_start:.2f}%")
print(f"SOC at END   (08:15): {soc_end:.2f}%")
print(f"SOC Drop:             {soc_drop:.2f}%")

# Typical SolarEdge battery capacity (estimate)
# You would need the actual battery capacity for this site
# Common SolarEdge battery: 10 kWh
battery_capacity_kwh = 10.0  # This is an estimate!

estimated_discharge_kwh = (soc_drop / 100) * battery_capacity_kwh

print(f"\nAssuming battery capacity: {battery_capacity_kwh} kWh")
print(f"Estimated Discharge: {estimated_discharge_kwh:.3f} kWh")
print("=" * 80)

print(f"\n" + "=" * 80)
print("METHOD 3: Cumulative Total Difference (battery_200_TotWhExp)")
print("=" * 80)

# Use cumulative totals (more accurate!)
tot_exp_start = df.iloc[0]['battery_200_TotWhExp']   # Earliest
tot_exp_end = df.iloc[-1]['battery_200_TotWhExp']    # Latest

# Convert string with comma to float
if isinstance(tot_exp_start, str):
    tot_exp_start = float(tot_exp_start.replace(',', ''))
if isinstance(tot_exp_end, str):
    tot_exp_end = float(tot_exp_end.replace(',', ''))

cumulative_discharge_wh = tot_exp_end - tot_exp_start
cumulative_discharge_kwh = cumulative_discharge_wh / 1000.0

print(f"\nTotWhExp at START (07:15): {tot_exp_start:,.0f} Wh")
print(f"TotWhExp at END   (08:15): {tot_exp_end:,.0f} Wh")
print(f"Difference:                {cumulative_discharge_wh:,.0f} Wh")
print(f"\n✅ Total Discharge (kWh):  {cumulative_discharge_kwh:.3f} kWh")
print("=" * 80)

print(f"\n" + "=" * 80)
print("🎯 FINAL ANSWER")
print("=" * 80)
print(f"\nFor site 400000837 during event ca0c0d89-614d-4358-b31f-2cb27a29cf5f:")
print(f"Time window: 07:15:00 - 08:15:00 (1 hour)")
print(f"\nBattery Discharge Calculation:")
print(f"  Method 1 (Sum of Incremental):  {total_discharge_kwh:.3f} kWh")
print(f"  Method 3 (Cumulative Delta):    {cumulative_discharge_kwh:.3f} kWh")
print(f"\n⭐ RECOMMENDED VALUE: {cumulative_discharge_kwh:.3f} kWh")
print(f"\n(Methods 1 and 3 should be very close. Method 3 is more accurate.)")
print("=" * 80)
