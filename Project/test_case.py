import pandas as pd

ORIGINAL = "DataFiles/dsgs_new_sites_may16-31.csv"
UPDATED = "Updated_Files/dsgs_new_sites_may16-31.csv"

TEST_METERS = [
    "b640ad68-8991-4c14-be7b-ac018eff942e",
    "44e68802-a292-4b1d-b3fa-4152ca8e1a58",
    "e99b5df6-90ea-4aa1-b80b-51f7b8b8755d"
]

FACTOR = 0.33

TARGET_COLUMNS = [
    "energy_net_kwh",
    "energy_consumed_kwh",
    "energy_generated_kwh"
]

orig = pd.read_csv(ORIGINAL)
updated = pd.read_csv(UPDATED)

orig["meter_id"] = orig["meter_id"].astype(str).str.strip()
updated["meter_id"] = updated["meter_id"].astype(str).str.strip()

passed = 0
failed = 0
total_rows_validated = 0

for meter in TEST_METERS:

    o = orig[orig["meter_id"] == meter].copy()
    u = updated[updated["meter_id"] == meter].copy()

    # Meter not found
    if o.empty:
        print(f"NOT FOUND : {meter}")
        failed += 1
        continue

    if len(o) != len(u):
        print(
            f"ROW COUNT MISMATCH : {meter} "
            f"(orig={len(o)}, updated={len(u)})"
        )
        failed += 1
        continue

    total_rows_validated += len(o)

    row_ok = True

    for col in TARGET_COLUMNS:

        expected = (
            pd.to_numeric(
                o[col],
                errors="coerce"
            ) * FACTOR
        )

        actual = pd.to_numeric(
            u[col],
            errors="coerce"
        )

        comparison = (
            (expected - actual)
            .abs()
            .fillna(0)
            < 1e-9
        )

        if not comparison.all():

            first_bad = comparison[~comparison].index[0]

            print(f"\nFAIL : {meter}")
            print(f"Column : {col}")

            print(
                "Original :",
                o.loc[first_bad, col]
            )

            print(
                "Expected :",
                expected.loc[first_bad]
            )

            print(
                "Actual   :",
                actual.loc[first_bad]
            )

            row_ok = False
            break

    if row_ok:
        print(
            f"PASS : {meter} "
            f"(Rows={len(o)})"
        )
        passed += 1
    else:
        failed += 1

print("\n==========================")
print("VALIDATION SUMMARY")
print("==========================")
print(f"Passed Meters       : {passed}")
print(f"Failed Meters       : {failed}")
print(f"Rows Validated      : {total_rows_validated}")
print("==========================")