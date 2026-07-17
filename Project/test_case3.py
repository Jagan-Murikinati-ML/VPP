import pandas as pd

# =====================================================
# CONFIG
# =====================================================

ORIGINAL = "DataFiles/dsgs_new_sites_june16-30.csv"
UPDATED = "Updated_Files/DSGS_414_NewSites_MayJun_Data_2026_updated/dsgs_new_sites_june16-30.csv"

METER_ID = "df2d3657-19dc-4c30-aec0-dd34519b539e"

FACTOR = 0.707977519889059
TARGET_TIMES = {
    "2026-06-27T02:00:00.0000Z",
    "2026-06-27T02:15:00.0000Z",
    "2026-06-27T02:30:00.0000Z",
    "2026-06-27T02:45:00.0000Z",
    "2026-06-27T03:00:00.0000Z",
    "2026-06-27T03:15:00.0000Z",
    "2026-06-27T03:30:00.0000Z",
    "2026-06-27T03:45:00.0000Z"
}

NON_TARGET_TIME = "2026-06-27T04:00:00.0000Z"

TARGET_COLUMNS = [
    "energy_net_kwh",
    "energy_consumed_kwh",
    "energy_generated_kwh"
]

# =====================================================
# LOAD FILES
# =====================================================

orig = pd.read_csv(ORIGINAL)
upd = pd.read_csv(UPDATED)

orig["meter_id"] = orig["meter_id"].astype(str).str.strip()
upd["meter_id"] = upd["meter_id"].astype(str).str.strip()

# =====================================================
# TARGET ROWS (SHOULD CHANGE)
# =====================================================

orig_rows = orig[
    (orig["meter_id"] == METER_ID)
    &
    (orig["interval_start_time_utc"].isin(TARGET_TIMES))
].copy()

upd_rows = upd[
    (upd["meter_id"] == METER_ID)
    &
    (upd["interval_start_time_utc"].isin(TARGET_TIMES))
].copy()

print("\n====================================")
print("TARGET ROW COUNT")
print("====================================")
print("Rows found:", len(orig_rows))

if len(orig_rows) != 8:
    print("ERROR : Expected exactly 8 rows")
    exit()

print("\n====================================")
print("ORIGINAL TARGET ROWS")
print("====================================")

print(
    orig_rows[
        [
            "interval_start_time_utc",
            "energy_net_kwh",
            "energy_consumed_kwh",
            "energy_generated_kwh"
        ]
    ]
)

print("\n====================================")
print("UPDATED TARGET ROWS")
print("====================================")

print(
    upd_rows[
        [
            "interval_start_time_utc",
            "energy_net_kwh",
            "energy_consumed_kwh",
            "energy_generated_kwh"
        ]
    ]
)

# =====================================================
# FACTOR VALIDATION
# =====================================================

print("\n====================================")
print("FACTOR VALIDATION")
print("====================================")

for col in TARGET_COLUMNS:

    orig_rows[col] = pd.to_numeric(
        orig_rows[col],
        errors="coerce"
    )

    upd_rows[col] = pd.to_numeric(
        upd_rows[col],
        errors="coerce"
    )

    if (orig_rows[col].fillna(0) == 0).all():

        print(
            f"WARNING : {col} contains only zeros. "
            f"Factor validation not meaningful."
        )
        continue

    expected = orig_rows[col] * FACTOR

    actual = upd_rows[col]

    comparison = (
        (expected - actual)
        .abs()
        .fillna(0)
        < 1e-9
    )

    if comparison.all():

        print(f"PASS : {col}")

    else:

        print(f"FAIL : {col}")

        bad_idx = comparison[~comparison].index[0]

        print(
            "Timestamp :",
            orig_rows.loc[
                bad_idx,
                "interval_start_time_utc"
            ]
        )

        print(
            "Original  :",
            orig_rows.loc[bad_idx, col]
        )

        print(
            "Expected  :",
            expected.loc[bad_idx]
        )

        print(
            "Actual    :",
            actual.loc[bad_idx]
        )

# =====================================================
# NON TARGET ROW
# =====================================================

orig_non_target = orig[
    (orig["meter_id"] == METER_ID)
    &
    (orig["interval_start_time_utc"] == NON_TARGET_TIME)
]

upd_non_target = upd[
    (upd["meter_id"] == METER_ID)
    &
    (upd["interval_start_time_utc"] == NON_TARGET_TIME)
]

print("\n====================================")
print("NON TARGET TIMESTAMP CHECK")
print("====================================")

print("\nOriginal:")

print(
    orig_non_target[
        [
            "interval_start_time_utc",
            "energy_net_kwh",
            "energy_consumed_kwh",
            "energy_generated_kwh"
        ]
    ]
)

print("\nUpdated:")

print(
    upd_non_target[
        [
            "interval_start_time_utc",
            "energy_net_kwh",
            "energy_consumed_kwh",
            "energy_generated_kwh"
        ]
    ]
)

print("\n====================================")
print("NON TARGET VALIDATION")
print("====================================")

for col in TARGET_COLUMNS:

    original = float(
        orig_non_target.iloc[0][col]
    )

    updated = float(
        upd_non_target.iloc[0][col]
    )

    if abs(original - updated) < 1e-9:

        print(
            f"PASS : {col} unchanged"
        )

    else:

        print(
            f"FAIL : {col} changed unexpectedly"
        )

        print(
            f"Original = {original}"
        )

        print(
            f"Updated  = {updated}"
        )