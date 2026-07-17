import pandas as pd

ORIGINAL = "DataFiles/dsgs_june09_data.csv"
UPDATED = "Updated_Files/DSGS_8121_Sites_June_data_2026_updated/dsgs_june09_data.csv"

METERS = [
    "ed9dc510-6289-422b-80d2-97b31dbe8a21",
    "849abe28-4870-4da1-9f03-eaf62ffa5319"
]

TARGET_COLUMNS = [
    "energy_net_kwh",
    "energy_consumed_kwh",
    "energy_generated_kwh"
]

orig = pd.read_csv(ORIGINAL)
upd = pd.read_csv(UPDATED)

passed = 0
failed = 0

for meter in METERS:

    o = orig[orig["meter_id"] == meter]
    u = upd[upd["meter_id"] == meter]

    if o.empty:
        print(f"NOT FOUND : {meter}")
        failed += 1
        continue

    ok = True

    for col in TARGET_COLUMNS:

        if not (pd.to_numeric(u[col], errors="coerce") == 0).all():
            ok = False
            print(f"FAIL : {meter} : {col}")
            break

    if ok:
        print(
            f"PASS : {meter} "
            f"(Rows={len(u)})"
        )
        passed += 1
    else:
        failed += 1

print()
print("Passed =", passed)
print("Failed =", failed)