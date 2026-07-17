import pandas as pd
from pathlib import Path

# =====================================================
# FILES
# =====================================================

PART1_FILE = "part1.xlsx"
PART2_FILE = "part2.xlsx"
PART3_FILE = "part3.xlsx"

DATA_FOLDER = "DataFiles"

OUTPUT_FOLDER = "Updated_Files"

PART2_FACTOR = 0.33

TARGET_COLUMNS = [
    "energy_net_kwh",
    "energy_consumed_kwh",
    "energy_generated_kwh"
]

TARGET_INTERVALS = {
    "2026-06-27T02:00:00.0000Z",
    "2026-06-27T02:15:00.0000Z",
    "2026-06-27T02:30:00.0000Z",
    "2026-06-27T02:45:00.0000Z",
    "2026-06-27T03:00:00.0000Z",
    "2026-06-27T03:15:00.0000Z",
    "2026-06-27T03:30:00.0000Z",
    "2026-06-27T03:45:00.0000Z"
}

NEW_SITE_FILES = {
    "dsgs_new_sites_may01-15.csv",
    "dsgs_new_sites_may16-31.csv",
    "dsgs_new_sites_june01-15.csv",
    "dsgs_new_sites_june16-30.csv"
}

# =====================================================
# LOAD PART 1
# =====================================================

part1 = pd.read_excel(PART1_FILE)

part1.columns = part1.columns.str.strip()

part1["LEAP ID"] = (
    part1["LEAP ID"]
    .astype(str)
    .str.strip()
)

part1["In Which File"] = (
    part1["In Which File"]
    .astype(str)
    .str.strip()
)

part1_june = set(
    part1[
        part1["In Which File"] == "June"
    ]["LEAP ID"]
)

part1_may_june = set(
    part1[
        part1["In Which File"] == "May and June"
    ]["LEAP ID"]
)

# =====================================================
# LOAD PART 2
# =====================================================

part2 = pd.read_excel(PART2_FILE)

part2.columns = part2.columns.str.strip()

part2["LEAP ID"] = (
    part2["LEAP ID"]
    .astype(str)
    .str.strip()
)

part2["In Which File"] = (
    part2["In Which File"]
    .astype(str)
    .str.strip()
)

part2_june = set(
    part2[
        part2["In Which File"] == "June"
    ]["LEAP ID"]
)

part2_may_june = set(
    part2[
        part2["In Which File"] == "May and June"
    ]["LEAP ID"]
)

# =====================================================
# LOAD PART 3
# =====================================================

part3 = pd.read_excel(PART3_FILE)

part3.columns = part3.columns.str.strip()

part3["LEAP ID"] = (
    part3["LEAP ID"]
    .astype(str)
    .str.strip()
)

part3["In Which File"] = (
    part3["In Which File"]
    .astype(str)
    .str.strip()
)

part3_june_factor = {}

part3_may_june_factor = {}

for _, row in part3.iterrows():

    meter_id = row["LEAP ID"]

    factor = float(row["energy_net_kwh"])

    if row["In Which File"] == "June":
        part3_june_factor[meter_id] = factor
    else:
        part3_may_june_factor[meter_id] = factor

# =====================================================
# OUTPUT
# =====================================================

Path(OUTPUT_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# PROCESS
# =====================================================

def process_file(file_path):

    print(f"\nProcessing {file_path.name}")

    df = pd.read_csv(file_path)

    df["meter_id"] = (
        df["meter_id"]
        .astype(str)
        .str.strip()
    )

    for col in TARGET_COLUMNS:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    filename = file_path.name.lower()

    is_new_site_file = filename in NEW_SITE_FILES

    # ==========================================
    # PART 1
    # ==========================================

    if is_new_site_file:

        zero_ids = part1_may_june

    else:

        zero_ids = (
            part1_june |
            part1_may_june
        )

    zero_mask = df["meter_id"].isin(zero_ids)

    df.loc[
        zero_mask,
        TARGET_COLUMNS
    ] = 0

    # ==========================================
    # PART 2
    # ==========================================

    if is_new_site_file:

        factor_ids = part2_may_june

    else:

        factor_ids = (
            part2_june |
            part2_may_june
        )

    factor_mask = df["meter_id"].isin(
        factor_ids
    )

    for col in TARGET_COLUMNS:

        df.loc[
            factor_mask,
            col
        ] = (
            df.loc[
                factor_mask,
                col
            ]
            * PART2_FACTOR
        )

    # ==========================================
    # PART 3
    # ==========================================

    part3_dict = {}

    if filename == "dsgs_june27_data.csv":

        part3_dict.update(
            part3_june_factor
        )

        part3_dict.update(
            part3_may_june_factor
        )

    elif filename == "dsgs_new_sites_june16-30.csv":

        part3_dict.update(
            part3_may_june_factor
        )

    if part3_dict:

        interval_mask = (
            df["interval_start_time_utc"]
            .isin(TARGET_INTERVALS)
        )

        for meter_id, factor in part3_dict.items():

            site_mask = (
                (df["meter_id"] == meter_id)
                &
                interval_mask
            )

            for col in TARGET_COLUMNS:

                df.loc[
                    site_mask,
                    col
                ] = (
                    df.loc[
                        site_mask,
                        col
                    ]
                    * factor
                )

    output_path = (
        Path(OUTPUT_FOLDER)
        / file_path.name
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved -> {output_path.name}"
    )

# =====================================================
# RUN
# =====================================================

for file in Path(DATA_FOLDER).glob("*.csv"):

    process_file(file)

print("\nCompleted.")