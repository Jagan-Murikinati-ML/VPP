# AssetMaster NULL percentage report (vppopsdb, dev)

NULL percentage for every column of every AssetMaster table in `vppopsdb` (schema `asset`). It complements [asset-data-quality-report.md](asset-data-quality-report.md), which covers the payload layer and the all-time column layer.

## Scope and method

- **Environment:** dev only.
- **Window:** rows last written between 2026-10-20 00:00 and 2026-10-23 00:00 UTC (20, 21 and 22 October). A row is in the window when its `last_event_ts` falls inside it. Rows are upserted, so a row created earlier and updated in the window counts; a row not touched in the window does not.
- **Rows counted:** live rows only (`status <> 'deleted'`).
- **NULL vs blank:** `null %` counts SQL NULLs only. Empty strings are counted separately as `blank`, and `populated %` is the share that is neither NULL nor blank.
- **Tables:** every base table in the `asset` schema except `event_ledger`, `ingestion_errors` and `onboarding_results` (operational), and the view `v_site_onboarding_latest`.
- **Query:** `vppmetadata-rds/scripts/asset-null-check.sql`. It reads the column list from `INFORMATION_SCHEMA`, so columns added later are included on the next run. Raw output: `vppmetadata-rds/scripts/asset-null-check-results.csv`.

## Summary by table

| table | rows in window | columns | all NULL | partly populated | fully populated |
| --- | --- | --- | --- | --- | --- |
| asset_status | 8087 | 9 | 0 | 3 | 6 |
| contract_details | 588 | 27 | 0 | 5 | 22 |
| customer_information | 597 | 19 | 0 | 13 | 6 |
| document_links | 589 | 8 | 0 | 0 | 8 |
| hardware_ac_combiners | 3 | 17 | 2 | 3 | 12 |
| hardware_backup_interfaces | 0 | 13 | no rows | 0 | 0 |
| hardware_batteries | 600 | 22 | 0 | 15 | 7 |
| hardware_inverters | 602 | 22 | 1 | 14 | 7 |
| hardware_panels | 2915 | 16 | 0 | 1 | 15 |
| hardware_system_sizes | 592 | 10 | 0 | 2 | 8 |
| installer_information | 645 | 21 | 0 | 15 | 6 |
| partner_information | 770 | 11 | 0 | 3 | 8 |
| site_details | 772 | 29 | 3 | 19 | 7 |
| site_monitoring_details | 657 | 8 | 0 | 0 | 8 |

## Columns that are all NULL

Every live row in the window has NULL in these columns.

| table | column | type | rows in window |
| --- | --- | --- | --- |
| hardware_ac_combiners | common_info | nvarchar | 3 |
| hardware_ac_combiners | triggered_by | nvarchar | 3 |
| hardware_inverters | triggered_by | nvarchar | 602 |
| site_details | contact_email | nvarchar | 772 |
| site_details | display_name | nvarchar | 772 |
| site_details | simulation_job_id | nvarchar | 772 |

`hardware_backup_interfaces` had no live rows in the window, so none of its 13 columns can be measured: `asset_identifier`, `common_info`, `dt_id`, `firmware_version`, `hardware_backup_interfaces_id`, `ingest_time`, `last_event_ts`, `product_code`, `product_manufacturer`, `product_name`, `product_type`, `serial_number`, `status`.

All-NULL here means all-NULL in this window, not necessarily forever. The earlier all-time report shows `site_details.contact_email` (0.5%), `site_details.simulation_job_id` (1%) and `site_details.display_name` (1.5%) as rarely populated, not never. It also lists `hardware_inverters.triggered_by` (`triggeredBy` on `inverter;1`) and `hardware_ac_combiners.common_info` (no `commonInfo` on `acCombiner;1`) among the payload fields that are unmapped or absent.

## Columns that are partly populated

Columns with at least one NULL and at least one value. Grouped by how empty they are, most empty first.

### Almost always NULL (95% or more NULL)

| table | column | rows in window | NULL rows | NULL % | blank rows | populated % |
| --- | --- | --- | --- | --- | --- | --- |
| site_details | triggered_by | 772 | 771 | 99.9% | 0 | 0.1% |
| contract_details | fund | 588 | 587 | 99.8% | 0 | 0.2% |
| contract_details | new_roof_guarantee_term_years | 588 | 586 | 99.7% | 0 | 0.3% |
| hardware_batteries | ems_serial_number | 600 | 598 | 99.7% | 0 | 0.3% |
| hardware_inverters | connected_module_manufacturer | 602 | 600 | 99.7% | 0 | 0.3% |
| hardware_inverters | connected_module_name | 602 | 600 | 99.7% | 0 | 0.3% |
| hardware_inverters | connected_module_power_class | 602 | 600 | 99.7% | 0 | 0.3% |
| hardware_inverters | connected_module_serial_number | 602 | 600 | 99.7% | 0 | 0.3% |
| hardware_inverters | warranty_date | 602 | 600 | 99.7% | 0 | 0.3% |
| site_details | configuration_type | 772 | 769 | 99.6% | 0 | 0.4% |
| site_details | installation_complete_date | 772 | 769 | 99.6% | 0 | 0.4% |
| hardware_batteries | triggered_by | 600 | 594 | 99.0% | 0 | 1.0% |
| hardware_inverters | fw_version | 602 | 594 | 98.7% | 0 | 1.3% |
| hardware_batteries | fw_version | 600 | 591 | 98.5% | 0 | 1.5% |
| hardware_batteries | warranty_date | 600 | 591 | 98.5% | 0 | 1.5% |
| contract_details | annual_degradation_rate | 588 | 576 | 98.0% | 0 | 2.0% |
| contract_details | power_plan_agreement | 588 | 576 | 98.0% | 0 | 2.0% |

### Inconsistent (5% to under 95% NULL)

| table | column | rows in window | NULL rows | NULL % | blank rows | populated % |
| --- | --- | --- | --- | --- | --- | --- |
| installer_information | account_id | 645 | 594 | 92.1% | 0 | 7.9% |
| installer_information | account_name | 645 | 594 | 92.1% | 0 | 7.9% |
| installer_information | access_notes | 645 | 590 | 91.5% | 0 | 8.5% |
| hardware_ac_combiners | communication_type | 3 | 1 | 33.3% | 0 | 66.7% |
| hardware_ac_combiners | ems_serial_number | 3 | 1 | 33.3% | 0 | 66.7% |
| hardware_ac_combiners | warranty_date | 3 | 1 | 33.3% | 0 | 66.7% |
| site_details | pto_date | 772 | 179 | 23.2% | 0 | 76.8% |
| site_details | purchase_date | 772 | 179 | 23.2% | 0 | 76.8% |
| site_details | site_name | 772 | 125 | 16.2% | 0 | 83.8% |
| site_details | asset_attributes | 772 | 123 | 15.9% | 0 | 84.1% |
| site_details | full_address | 772 | 123 | 15.9% | 0 | 84.1% |
| site_details | installation_status | 772 | 123 | 15.9% | 0 | 84.1% |
| site_details | time_zone | 772 | 123 | 15.9% | 0 | 84.1% |
| site_details | account_number | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | city | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | country | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | latitude | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | longitude | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | postal_code | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | state | 772 | 122 | 15.8% | 0 | 84.2% |
| site_details | street1 | 772 | 122 | 15.8% | 0 | 84.2% |
| installer_information | country | 645 | 57 | 8.8% | 0 | 91.2% |
| installer_information | full_address | 645 | 57 | 8.8% | 0 | 91.2% |
| installer_information | city | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | common_info | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | company | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | first_name | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | last_name | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | phone | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | postal_code | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | state | 645 | 56 | 8.7% | 0 | 91.3% |
| installer_information | street1 | 645 | 56 | 8.7% | 0 | 91.3% |
| site_details | common_info | 772 | 58 | 7.5% | 0 | 92.5% |

### Mostly populated (under 5% NULL)

| table | column | rows in window | NULL rows | NULL % | blank rows | populated % |
| --- | --- | --- | --- | --- | --- | --- |
| hardware_inverters | product_sub_type | 602 | 20 | 3.3% | 0 | 96.7% |
| hardware_inverters | common_info | 602 | 13 | 2.2% | 0 | 97.8% |
| hardware_batteries | nameplate_usable_wh_rtg | 600 | 12 | 2.0% | 0 | 98.0% |
| hardware_inverters | registration_number | 602 | 12 | 2.0% | 0 | 98.0% |
| hardware_batteries | common_info | 600 | 11 | 1.8% | 0 | 98.2% |
| hardware_batteries | nameplate_wh_rtg | 600 | 11 | 1.8% | 0 | 98.2% |
| hardware_batteries | registration_number | 600 | 11 | 1.8% | 0 | 98.2% |
| hardware_batteries | backup_type | 600 | 9 | 1.5% | 0 | 98.5% |
| hardware_batteries | coupling_type | 600 | 9 | 1.5% | 0 | 98.5% |
| customer_information | access_notes | 597 | 8 | 1.3% | 581 | 1.3% |
| customer_information | city | 597 | 7 | 1.2% | 0 | 98.8% |
| customer_information | country | 597 | 7 | 1.2% | 0 | 98.8% |
| customer_information | full_address | 597 | 7 | 1.2% | 0 | 98.8% |
| customer_information | postal_code | 597 | 7 | 1.2% | 0 | 98.8% |
| customer_information | state | 597 | 7 | 1.2% | 0 | 98.8% |
| customer_information | street1 | 597 | 7 | 1.2% | 0 | 98.8% |
| hardware_batteries | communication_type | 600 | 7 | 1.2% | 0 | 98.8% |
| customer_information | common_info | 597 | 6 | 1.0% | 0 | 99.0% |
| contract_details | guaranteed_refund_rate_schedule | 588 | 5 | 0.9% | 0 | 99.1% |
| customer_information | email | 597 | 5 | 0.8% | 0 | 99.2% |
| customer_information | first_name | 597 | 5 | 0.8% | 0 | 99.2% |
| customer_information | last_name | 597 | 5 | 0.8% | 0 | 99.2% |
| customer_information | phone | 597 | 5 | 0.8% | 0 | 99.2% |
| hardware_inverters | manufacturer | 602 | 5 | 0.8% | 0 | 99.2% |
| hardware_inverters | model | 602 | 5 | 0.8% | 0 | 99.2% |
| hardware_inverters | nameplate_w_max_rtg | 602 | 5 | 0.8% | 0 | 99.2% |
| hardware_inverters | product_code | 602 | 5 | 0.8% | 0 | 99.2% |
| hardware_inverters | product_type | 602 | 5 | 0.8% | 0 | 99.2% |
| hardware_system_sizes | common_info | 592 | 4 | 0.7% | 0 | 99.3% |
| hardware_system_sizes | system_type | 592 | 4 | 0.7% | 0 | 99.3% |
| partner_information | company_type_id | 770 | 3 | 0.4% | 0 | 99.6% |
| hardware_batteries | manufacturer | 600 | 2 | 0.3% | 0 | 99.7% |
| hardware_batteries | model | 600 | 2 | 0.3% | 0 | 99.7% |
| hardware_batteries | product_code | 600 | 2 | 0.3% | 0 | 99.7% |
| hardware_batteries | product_type | 600 | 2 | 0.3% | 0 | 99.7% |
| partner_information | company_name | 770 | 2 | 0.3% | 0 | 99.7% |
| customer_information | customer_finance_type | 597 | 1 | 0.2% | 0 | 99.8% |
| hardware_panels | serial_number | 2915 | 7 | 0.2% | 2900 | 0.3% |
| installer_information | email | 645 | 1 | 0.2% | 0 | 99.8% |
| asset_status | entity_type | 8087 | 10 | 0.1% | 0 | 99.9% |
| asset_status | last_event_type | 8087 | 10 | 0.1% | 0 | 99.9% |
| asset_status | model | 8087 | 10 | 0.1% | 0 | 99.9% |
| partner_information | company_type | 770 | 1 | 0.1% | 0 | 99.9% |

Note: `hardware_panels.serial_number` sits in the last group only because it has few NULLs; see Blank strings below.

### Blank strings

These columns are mostly empty strings rather than NULL, so they look populated to a NULL check.

| table | column | rows in window | NULL rows | blank rows | populated % |
| --- | --- | --- | --- | --- | --- |
| hardware_panels | serial_number | 2915 | 7 | 2900 | 0.3% |
| customer_information | access_notes | 597 | 8 | 581 | 1.3% |

## EventHub payload check

What the Asset Registry events carry, and how that lines up with the tables. Source: the ingester's copy of each hub event in `asset.event_ledger.raw_event`, partition 0, enqueued 2026-10-20 to 2026-10-22 UTC.

- **Events in the window:** 11,490 hub events: 10,869 processed, 600 onboarding results, 16 skipped non-asset events and 5 for a model with no table. Fields below come from the 10,874 processed and no-table events.
- **Completeness:** sequence numbers run from 11,211,043 to 11,222,532 with no gaps, and the hub explorer shows sequence 11,211,043 at the same time as the ledger. The first hub event consumed in the window is at 2026-10-20 23:47 UTC, so earlier events on 20 October are not covered.
- **Mapping compared against:** `AssetTableMap.cs` as committed on 2026-10-19 (`53bed49`). The mapping is being changed separately, so rerun the comparison after those changes.
- **Query:** `vppmetadata-rds/scripts/asset-eventhub-payload-fields.sql`; raw output `vppmetadata-rds/scripts/asset-eventhub-payload-fields-results.csv`. Paths are relative to `payload.properties`; `commonInfo.*` is excluded because it is stored as a single JSON column.

### Events per model

| model | target table | Created | Updated | Deleted |
| --- | --- | --- | --- | --- |
| acCombiner;1 | hardware_ac_combiners | 4 | 10 | 2 |
| battery;1 | hardware_batteries | 597 | 15 | 8 |
| batteryPack;1 | hardware_batteries | 12 | 0 | 8 |
| defaultSystemInfo;1 | hardware_system_sizes | 587 | 16 | 0 |
| homeowner;1 | customer_information | 598 | 631 | 4 |
| installer;1 | installer_information | 645 | 16 | 4 |
| inverter;1 | hardware_inverters | 592 | 14 | 4 |
| microInverter;1 | hardware_inverters | 15 | 0 | 11 |
| oAndMContract;1 | contract_details | 587 | 16 | 0 |
| partner;1 | partner_information | 774 | 0 | 632 |
| pvArray;1 | hardware_panels | 2978 | 0 | 73 |
| pvSystemInfo;1 | hardware_system_sizes | 6 | 0 | 5 |
| site;1 | site_details | 651 | 746 | 5 |
| siteAggregator;1 | none (no table) | 3 | 0 | 2 |

### Fields that arrive with no column

Fields on Created and Updated events that the mapping does not store, with the NULL rate a column for each would have today. Delete events are left out; they carry `triggeredBy` as audit information only.

**How the NULL rate is calculated.** A table row is one entity (a site, a battery, an inverter) in its current state, not one event, so the rate is per entity. Live entities are those whose last event in the window is not a Delete. An entity counts as populated if any of its Created or Updated events in the window carried a real value (not null, not an empty string). Would-be NULL % is 100 minus that share. This assumes an update that does not mention a field leaves an earlier value in place. Source: `vppmetadata-rds/scripts/asset-eventhub-entity-coverage.sql`.

#### No column anywhere in the database

| model | field | events carrying | live entities | entities with a value | would-be NULL % | distinct values |
| --- | --- | --- | --- | --- | --- | --- |
| battery;1 | `nameplateInfo.totalBatteryWHRtg` | 1 | 591 | 1 | 99.8% | 1 |
| battery;1 | `nameplateInfo.wMaxRtg` | 1 | 591 | 1 | 99.8% | 1 |
| battery;1 | `productInfo.prodSubType` | 1 | 591 | 1 | 99.8% | 1 |
| site;1 | `isVppRegistered` | 717 | 770 | 123 | 84.0% | 2 |

`isVppRegistered` is the one that matters. 717 update events carried it, but they come from only 123 of the 770 live sites (about 6 updates per site), so a column for it would be 84.0% NULL, not the 3.9% that counting update events suggests (717 of 746 carried it). It has two distinct values; the earlier report lists its JSON type as boolean. It is never on a Created event, so a new site has no value until its first update. The three `battery;1` fields each appear on a single battery of 591 (99.8% NULL).

#### Column already exists, but the mapping does not read the field

| model | field | existing column | events carrying | live entities | entities with a value | would-be NULL % | column NULL % today (whole table) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| acCombiner;1 | `triggeredBy` | hardware_ac_combiners.triggered_by | 3 | 4 | 1 | 75.0% | 100.0% |
| microInverter;1 | `connectedModule.powerClass` | hardware_inverters.connected_module_power_class | 12 | 7 | 4 | 42.9% | 99.7% |
| microInverter;1 | `connectedModule.productInfo.prodMfr` | hardware_inverters.connected_module_manufacturer | 15 | 7 | 7 | 0.0% | 99.7% |
| microInverter;1 | `connectedModule.productInfo.prodName` | hardware_inverters.connected_module_name | 15 | 7 | 7 | 0.0% | 99.7% |
| microInverter;1 | `connectedModule.serialNum` | hardware_inverters.connected_module_serial_number | 15 | 7 | 7 | 0.0% | 99.7% |
| microInverter;1 | `triggeredBy` | hardware_inverters.triggered_by | 6 | 7 | 2 | 71.4% | 100.0% |
| microInverter;1 | `warrantyDt` | hardware_inverters.warranty_date | 15 | 7 | 7 | 0.0% | 99.7% |

The whole-table rate is higher because `hardware_inverters` also holds about 595 rows from `inverter;1` events, which never carry these fields. Only 2 `hardware_inverters` rows hold `connected_module_*` values although 7 live `microInverter;1` entities carried them, so the stored data does not reflect these events; confirm with the mapping owner whether the deployed ingester differs from the committed code. The `acCombiner;1` figure rests on only 4 live entities.

- **`siteAggregator;1` has no table.** 3 Created and 2 Deleted events (the 5 no-table events) are recorded in `asset_status` only.
- **Fields that appeared in the earlier all-time report but not in this window:** `utilityName`, `partnerOrgId`, `utilityAccountNumber`, `couplingType` on inverters and others did not appear in any event here.


## NULL percentage per column, all tables

Every column, most NULL first. `distinct` is blank for `nvarchar(max)` columns.

### asset_status

8087 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| entity_type | nvarchar | 10 | 0.1% | 0 | 99.9% | 5 | PARTIAL |
| last_event_type | nvarchar | 10 | 0.1% | 0 | 99.9% | 8 | PARTIAL |
| model | nvarchar | 10 | 0.1% | 0 | 99.9% | 14 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 771 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 8087 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 8087 | FULL |
| is_mapped | bit | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 2213 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### contract_details

588 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fund | nvarchar | 587 | 99.8% | 0 | 0.2% | 1 | PARTIAL |
| new_roof_guarantee_term_years | int | 586 | 99.7% | 0 | 0.3% | 2 | PARTIAL |
| annual_degradation_rate | nvarchar | 576 | 98.0% | 0 | 2.0% | 1 | PARTIAL |
| power_plan_agreement | nvarchar | 576 | 98.0% | 0 | 2.0% | 1 | PARTIAL |
| guaranteed_refund_rate_schedule | nvarchar | 5 | 0.9% | 0 | 99.1% |  | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| battery_owner | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| common_info | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| contract_details_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| contract_duration_years | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| contract_type | nvarchar | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| guaranteed_system_output_kwh_schedule | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| homeowner_term_length_years | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| installation_workmanship_guarantee_years | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| legal_owner | nvarchar | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| minimum_reserve_level | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| production_guarantee_level | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| production_guarantee_term_years | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| reporting_intervals | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| roof_penetration_warranty_term_years | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| start_date | datetime2 | 0 | 0.0% | 0 | 100.0% | 11 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| year_one_expected_output_kwh | decimal | 0 | 0.0% | 0 | 100.0% | 11 | FULL |
| year_one_monthly_production | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |

### customer_information

597 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| access_notes | nvarchar | 8 | 1.3% | 581 | 1.3% |  | PARTIAL |
| city | nvarchar | 7 | 1.2% | 0 | 98.8% | 11 | PARTIAL |
| country | nvarchar | 7 | 1.2% | 0 | 98.8% | 1 | PARTIAL |
| full_address | nvarchar | 7 | 1.2% | 0 | 98.8% | 11 | PARTIAL |
| postal_code | nvarchar | 7 | 1.2% | 0 | 98.8% | 11 | PARTIAL |
| state | nvarchar | 7 | 1.2% | 0 | 98.8% | 2 | PARTIAL |
| street1 | nvarchar | 7 | 1.2% | 0 | 98.8% | 11 | PARTIAL |
| common_info | nvarchar | 6 | 1.0% | 0 | 99.0% |  | PARTIAL |
| email | nvarchar | 5 | 0.8% | 0 | 99.2% | 8 | PARTIAL |
| first_name | nvarchar | 5 | 0.8% | 0 | 99.2% | 9 | PARTIAL |
| last_name | nvarchar | 5 | 0.8% | 0 | 99.2% | 9 | PARTIAL |
| phone | nvarchar | 5 | 0.8% | 0 | 99.2% | 7 | PARTIAL |
| customer_finance_type | nvarchar | 1 | 0.2% | 0 | 99.8% | 2 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 594 | FULL |
| customer_information_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 597 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 597 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 597 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 594 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### document_links

589 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 589 | FULL |
| document_index | int | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| document_links_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 589 | FULL |
| document_url | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 589 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 589 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 589 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### hardware_ac_combiners

3 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| common_info | nvarchar | 3 | 100.0% | 0 | 0.0% |  | ALL_NULL |
| triggered_by | nvarchar | 3 | 100.0% | 0 | 0.0% | 0 | ALL_NULL |
| communication_type | nvarchar | 1 | 33.3% | 0 | 66.7% | 2 | PARTIAL |
| ems_serial_number | nvarchar | 1 | 33.3% | 0 | 66.7% | 2 | PARTIAL |
| warranty_date | datetime2 | 1 | 33.3% | 0 | 66.7% | 2 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 3 | FULL |
| firmware_version | nvarchar | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| hardware_ac_combiners_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 3 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 3 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 3 | FULL |
| product_code | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| product_manufacturer | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| product_name | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| product_type | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| serial_number | nvarchar | 0 | 0.0% | 0 | 100.0% | 3 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### hardware_backup_interfaces

0 live rows in the window.

No rows in the window; columns cannot be measured.

### hardware_batteries

600 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ems_serial_number | nvarchar | 598 | 99.7% | 0 | 0.3% | 2 | PARTIAL |
| triggered_by | nvarchar | 594 | 99.0% | 0 | 1.0% | 2 | PARTIAL |
| fw_version | nvarchar | 591 | 98.5% | 0 | 1.5% | 3 | PARTIAL |
| warranty_date | datetime2 | 591 | 98.5% | 0 | 1.5% | 4 | PARTIAL |
| nameplate_usable_wh_rtg | decimal | 12 | 2.0% | 0 | 98.0% | 3 | PARTIAL |
| common_info | nvarchar | 11 | 1.8% | 0 | 98.2% |  | PARTIAL |
| nameplate_wh_rtg | decimal | 11 | 1.8% | 0 | 98.2% | 4 | PARTIAL |
| registration_number | nvarchar | 11 | 1.8% | 0 | 98.2% | 12 | PARTIAL |
| backup_type | nvarchar | 9 | 1.5% | 0 | 98.5% | 2 | PARTIAL |
| coupling_type | nvarchar | 9 | 1.5% | 0 | 98.5% | 2 | PARTIAL |
| communication_type | nvarchar | 7 | 1.2% | 0 | 98.8% | 2 | PARTIAL |
| manufacturer | nvarchar | 2 | 0.3% | 0 | 99.7% | 3 | PARTIAL |
| model | nvarchar | 2 | 0.3% | 0 | 99.7% | 7 | PARTIAL |
| product_code | nvarchar | 2 | 0.3% | 0 | 99.7% | 7 | PARTIAL |
| product_type | nvarchar | 2 | 0.3% | 0 | 99.7% | 3 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 591 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 600 | FULL |
| hardware_batteries_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 600 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 600 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 599 | FULL |
| serial_number | nvarchar | 0 | 0.0% | 0 | 100.0% | 24 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### hardware_inverters

602 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| triggered_by | nvarchar | 602 | 100.0% | 0 | 0.0% | 0 | ALL_NULL |
| connected_module_manufacturer | nvarchar | 600 | 99.7% | 0 | 0.3% | 1 | PARTIAL |
| connected_module_name | nvarchar | 600 | 99.7% | 0 | 0.3% | 1 | PARTIAL |
| connected_module_power_class | nvarchar | 600 | 99.7% | 0 | 0.3% | 2 | PARTIAL |
| connected_module_serial_number | nvarchar | 600 | 99.7% | 0 | 0.3% | 2 | PARTIAL |
| warranty_date | datetime2 | 600 | 99.7% | 0 | 0.3% | 1 | PARTIAL |
| fw_version | nvarchar | 594 | 98.7% | 0 | 1.3% | 4 | PARTIAL |
| product_sub_type | nvarchar | 20 | 3.3% | 0 | 96.7% | 1 | PARTIAL |
| common_info | nvarchar | 13 | 2.2% | 0 | 97.8% |  | PARTIAL |
| registration_number | nvarchar | 12 | 2.0% | 0 | 98.0% | 14 | PARTIAL |
| manufacturer | nvarchar | 5 | 0.8% | 0 | 99.2% | 4 | PARTIAL |
| model | nvarchar | 5 | 0.8% | 0 | 99.2% | 10 | PARTIAL |
| nameplate_w_max_rtg | decimal | 5 | 0.8% | 0 | 99.2% | 6 | PARTIAL |
| product_code | nvarchar | 5 | 0.8% | 0 | 99.2% | 10 | PARTIAL |
| product_type | nvarchar | 5 | 0.8% | 0 | 99.2% | 2 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 594 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 602 | FULL |
| hardware_inverters_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 602 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 602 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 601 | FULL |
| serial_number | nvarchar | 0 | 0.0% | 0 | 100.0% | 25 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### hardware_panels

2915 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| serial_number | nvarchar | 7 | 0.2% | 2900 | 0.3% | 8 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| azimuth | float | 0 | 0.0% | 0 | 100.0% | 13 | FULL |
| common_info | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 2915 | FULL |
| hardware_panels_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 2915 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 2915 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 588 | FULL |
| manufacturer | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| model | nvarchar | 0 | 0.0% | 0 | 100.0% | 7 | FULL |
| monthly_solar_access | nvarchar | 0 | 0.0% | 0 | 100.0% |  | FULL |
| panel_count | int | 0 | 0.0% | 0 | 100.0% | 13 | FULL |
| product_code | nvarchar | 0 | 0.0% | 0 | 100.0% | 7 | FULL |
| product_type | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| tilt | float | 0 | 0.0% | 0 | 100.0% | 14 | FULL |

### hardware_system_sizes

592 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| common_info | nvarchar | 4 | 0.7% | 0 | 99.3% |  | PARTIAL |
| system_type | nvarchar | 4 | 0.7% | 0 | 99.3% | 1 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 592 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 592 | FULL |
| hardware_system_sizes_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 592 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 592 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 592 | FULL |
| panel_system_size_unit | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |
| panel_system_size_value | float | 0 | 0.0% | 0 | 100.0% | 15 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### installer_information

645 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| account_id | nvarchar | 594 | 92.1% | 0 | 7.9% | 5 | PARTIAL |
| account_name | nvarchar | 594 | 92.1% | 0 | 7.9% | 5 | PARTIAL |
| access_notes | nvarchar | 590 | 91.5% | 0 | 8.5% |  | PARTIAL |
| country | nvarchar | 57 | 8.8% | 0 | 91.2% | 1 | PARTIAL |
| full_address | nvarchar | 57 | 8.8% | 0 | 91.2% | 8 | PARTIAL |
| city | nvarchar | 56 | 8.7% | 0 | 91.3% | 7 | PARTIAL |
| common_info | nvarchar | 56 | 8.7% | 0 | 91.3% |  | PARTIAL |
| company | nvarchar | 56 | 8.7% | 0 | 91.3% | 3 | PARTIAL |
| first_name | nvarchar | 56 | 8.7% | 0 | 91.3% | 6 | PARTIAL |
| last_name | nvarchar | 56 | 8.7% | 0 | 91.3% | 6 | PARTIAL |
| phone | nvarchar | 56 | 8.7% | 0 | 91.3% | 6 | PARTIAL |
| postal_code | nvarchar | 56 | 8.7% | 0 | 91.3% | 7 | PARTIAL |
| state | nvarchar | 56 | 8.7% | 0 | 91.3% | 3 | PARTIAL |
| street1 | nvarchar | 56 | 8.7% | 0 | 91.3% | 8 | PARTIAL |
| email | nvarchar | 1 | 0.2% | 0 | 99.8% | 11 | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 644 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 645 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 645 | FULL |
| installer_information_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 645 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 644 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### partner_information

770 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| company_type_id | nvarchar | 3 | 0.4% | 0 | 99.6% | 10 | PARTIAL |
| company_name | nvarchar | 2 | 0.3% | 0 | 99.7% | 716 | PARTIAL |
| company_type | nvarchar | 1 | 0.1% | 0 | 99.9% | 10 | PARTIAL |
| account_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 719 | FULL |
| account_name | nvarchar | 0 | 0.0% | 0 | 100.0% | 717 | FULL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 54 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 770 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 770 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 770 | FULL |
| partner_information_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 770 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### site_details

772 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| contact_email | nvarchar | 772 | 100.0% | 0 | 0.0% | 0 | ALL_NULL |
| display_name | nvarchar | 772 | 100.0% | 0 | 0.0% | 0 | ALL_NULL |
| simulation_job_id | nvarchar | 772 | 100.0% | 0 | 0.0% | 0 | ALL_NULL |
| triggered_by | nvarchar | 771 | 99.9% | 0 | 0.1% | 1 | PARTIAL |
| configuration_type | nvarchar | 769 | 99.6% | 0 | 0.4% | 2 | PARTIAL |
| installation_complete_date | datetime2 | 769 | 99.6% | 0 | 0.4% | 3 | PARTIAL |
| pto_date | datetime2 | 179 | 23.2% | 0 | 76.8% | 15 | PARTIAL |
| purchase_date | datetime2 | 179 | 23.2% | 0 | 76.8% | 15 | PARTIAL |
| site_name | nvarchar | 125 | 16.2% | 0 | 83.8% | 645 | PARTIAL |
| asset_attributes | nvarchar | 123 | 15.9% | 0 | 84.1% |  | PARTIAL |
| full_address | nvarchar | 123 | 15.9% | 0 | 84.1% | 25 | PARTIAL |
| installation_status | nvarchar | 123 | 15.9% | 0 | 84.1% | 2 | PARTIAL |
| time_zone | nvarchar | 123 | 15.9% | 0 | 84.1% | 5 | PARTIAL |
| account_number | nvarchar | 122 | 15.8% | 0 | 84.2% | 650 | PARTIAL |
| city | nvarchar | 122 | 15.8% | 0 | 84.2% | 21 | PARTIAL |
| country | nvarchar | 122 | 15.8% | 0 | 84.2% | 2 | PARTIAL |
| latitude | float | 122 | 15.8% | 0 | 84.2% | 25 | PARTIAL |
| longitude | float | 122 | 15.8% | 0 | 84.2% | 25 | PARTIAL |
| postal_code | nvarchar | 122 | 15.8% | 0 | 84.2% | 24 | PARTIAL |
| state | nvarchar | 122 | 15.8% | 0 | 84.2% | 8 | PARTIAL |
| street1 | nvarchar | 122 | 15.8% | 0 | 84.2% | 24 | PARTIAL |
| common_info | nvarchar | 58 | 7.5% | 0 | 92.5% |  | PARTIAL |
| asset_identifier | nvarchar | 0 | 0.0% | 0 | 100.0% | 771 | FULL |
| dt_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 772 | FULL |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 772 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 771 | FULL |
| site_details_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 772 | FULL |
| site_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 771 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

### site_monitoring_details

657 live rows in the window.

| column | type | NULL rows | NULL % | blank rows | populated % | distinct | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ingest_time | datetime2 | 0 | 0.0% | 0 | 100.0% | 657 | FULL |
| last_event_ts | datetime2 | 0 | 0.0% | 0 | 100.0% | 648 | FULL |
| oem_index | int | 0 | 0.0% | 0 | 100.0% | 2 | FULL |
| oem_name | nvarchar | 0 | 0.0% | 0 | 100.0% | 4 | FULL |
| oem_site_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 81 | FULL |
| site_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 648 | FULL |
| site_monitoring_details_id | nvarchar | 0 | 0.0% | 0 | 100.0% | 657 | FULL |
| status | nvarchar | 0 | 0.0% | 0 | 100.0% | 1 | FULL |

