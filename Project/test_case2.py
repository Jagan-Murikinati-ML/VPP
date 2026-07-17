import pandas as pd

ORIGINAL = "DataFiles/dsgs_june01_data.csv"
UPDATED = "Updated_Files/DSGS_8121_Sites_June_data_2026_updated/dsgs_june01_data.csv"

METER_IDS = [
    "59fef6e7-d5d0-4aa8-9db1-abb734714394",
    "6938f201-1968-486c-b97b-6bc3eb5334f1",
    "2673fe36-7a95-42f2-9c59-ea48bbe16c72",
    "7d24b8bd-5594-4088-91d1-5d09ecab40e0",
    "981b7ae6-5d92-4f8a-9d89-7519f83df70f",
    "bf0de1d2-6bcb-44c3-a1d9-dafe3506acf6",
    "8c9bf4a5-8ec1-47d7-a9c3-7bcd93703f48",
    "995828da-999b-4720-a1f4-43fc9febad48",
    "5891afce-ea99-4b54-a611-fbbeb3525728",
    "e152c118-756c-489e-8290-a2316d18cf45",
    "1b50ca1d-961e-491e-8a23-e7a7802933e2",
    "d74af3f0-ac62-4ec6-bb1e-55bd5808946a",
    "994d564d-15e2-4e7f-9bec-f470f5be7762",
    "dd13e8ff-20fc-4724-a795-fa6e87de6764",
    "6d7f6e87-7efa-4511-a8c4-edb0d063215e",
    "27c7aaea-7220-471f-b161-0cc29c54ef58",
    "41a79b0c-b773-4a30-ac55-a276ad3c7304",
    "9b4b713d-9816-4c1d-a681-d68b9e9b5ab5",
    "df901190-fab2-4b5c-8c20-38b0e35038f9",
    "2d2cfb55-c076-4c8a-a3bc-bdb7190b56bb",
    "f9017690-7940-4a02-aebc-9cdd5f7e09d3",
    "787070b3-257f-42c6-980c-d1ffc63cde3f",
    "872af269-4ba9-4c22-893c-8f2372d667fd",
    "4412dab0-94a3-465d-a078-1b33bcfb6c02",
    "6bfbe39e-4877-4b1c-9ed4-621649131d91",
    "c45d7ed3-17f8-4376-b1fb-8bb54485e0c7",
    "f4e9be4a-9fda-408d-be1a-5c20496dd044",
    "d9c949ca-c589-4f7b-82f0-64d7c0520fed",
    "426bbdf7-eb47-495e-ab1c-c55f20ac328f",
    "d230cc4a-c26a-41b6-a21d-c4ec6226d71f",
    "2afc731e-b27a-464d-9856-cf9d9288012e",
    "e1a45e20-2e09-4fcb-8cd7-21089b5abe34",
    "4a6fbcaf-811b-467e-a6e4-ad6f29887bf6",
    "f1ddad56-c307-4e10-b712-81bdfef7bc60",
    "7a02da76-5cf0-4511-bf4f-14316640ffe0",
    "dafa4e12-2c3a-4f57-981e-33328fe2e785",
    "ae065574-d538-4d47-a5e3-f1327837e8c9",
    "d7959124-ca87-4694-9493-2dc4ac40fd61",
    "af1f7ecd-4de0-43ec-9d74-81a087542230",
    "f2591ddc-af85-47e3-9af7-2b2afe25a6e4",
    "cb9def06-124e-49ab-a1fa-ba5cedd9fac1",
    "d72f5d60-b63e-43dd-b33a-d894fc962d66",
    "a4ffddc9-b923-44bc-8e75-94c70a2ffb1e",
    "78580eae-8ebb-4981-a200-59edfee06a38",
    "78795b5b-52af-4db3-bf56-3c18ab454241",
    "92bdf5dd-51ea-4823-9ebd-505d6a96a1d9",
    "644cb87d-d9b7-47a0-b746-c1f83f311186",
    "17855ab3-adc5-49f2-8d2e-38e407329175",
    "fd5c4a98-c152-4512-97a8-cf75d9de6baa",
    "61772514-be3d-4dea-a7d3-0dc4c1a517ac",
    "07f6bc70-344c-490f-9e61-729478ac58b1",
    "df57d76d-ca80-4410-b0a9-f1a54f3f9ba4",
    "b4a548bf-10d1-42bc-aa1a-b142b54f8bb2",
    "bede91f9-9d30-4578-a032-48467ec60c01",
    "b83eb0ad-0664-49d3-a03b-9893e236f940",
    "bd2fb0da-145b-41a3-aa99-f6aa7e8e24e7",
    "7dc58af4-f5ca-4888-b23b-551140710449",
    "d516faf8-bd22-4ef7-90f8-619933d15f5a",
    "0187e9a3-65ae-4461-9957-b5926a9acae7",
    "3f9f191a-7450-4f06-9315-1ea3299b0c5f",
    "f2ac07a0-f93f-470d-a804-7c8cdec4b4c9",
    "4aa70a2f-11a4-417c-a8da-76bf029ad48a",
    "03baa0fd-3a18-4d9e-bc39-de06d68015be",
    "407416e1-58eb-4a4c-8bdf-987f152704a8",
    "ea8e4a5b-0fa8-4b14-bcff-7e0cc702afc5",
    "d2c408f6-30d4-4cca-9f89-4234a329ccd3",
    "04a7fe42-ec38-4d7b-956f-b6421b83c626",
    "9d221da2-73a7-4be9-b150-55e26976cdfd",
    "ecc0c429-d359-4766-ae00-766b423b52f8",

]

orig = pd.read_csv(ORIGINAL)
upd = pd.read_csv(UPDATED)

for meter in METER_IDS:

    print("\n" + "="*80)
    print(f"METER : {meter}")
    print("="*80)

    orig_rows = orig[
        orig["meter_id"] == meter
    ].head(5)

    upd_rows = upd[
        upd["meter_id"] == meter
    ].head(5)

    print("\nORIGINAL ROWS")
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

    print("\nUPDATED ROWS")
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