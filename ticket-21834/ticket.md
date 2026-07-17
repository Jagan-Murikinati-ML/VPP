Create Historical Telemetry Function with the below requirements, this function is not a rollup, so we should get the time window based on the Iginition Ingestion Rate
 
//Inputs
orgId    - 01919c2e-f780-7000-8abc-def012345678 - Not Required
orgKey   - PRIME-GROUP - Not Required
siteId   - 019e8469-25fe-7a59-93c3-afb2a7c00000 - Required
siteKey  - GA-10 -- optional
equipId  - 019e8560-01d0-7307-952d-152d50e40112 - Required
equipKey - RPP-3-G1 -- optional
pointId  - 019eb3cb-6a05-7739-beac-c9d1492d9561 -- optional
pointKey - active_power -- optional
startDateTime - Required
endDateTime - Required


//Outputs
"result": {
    "orgId": "01919c2e-f780-7000-8abc-def012345678",
    "orgKey": "PRIME-GROUP",
    "sites": [
        {
            "siteId": "01919c2e-f781-7000-8def-d3501378dd50",
            "siteKey": "GA-10",
            "devices": [
                {
                    "equipId": "01919c2e-f782-7000-8abc-f8c41b622a90",
                    "equipKey": "UPS-3-F",
                    "equipType": "wattsch:UPSType",
                    "equipMake": "Toshiba",
                    "equipModel": "G9400",
                    "points": [
                        {
                            "pointId": "01919c2e-f780-7000-9abc-def018595078",
                            "pointKey": "active_power",
                            "metricName": "active_power",
                            "metricTimeStamp": "2026-05-29T05:59:22.3500002Z",
                            "metricUnit": "KiloW",
                            "metricValue": 412.7,
                            "metricScope": "helios.telemetry.pipeline",
                            "derivedFrom": ""
                        },
                        {
                            "pointId": "08769c2e-f780-7000-9abc-def018588888",
                            "pointKey": "loading_percentage",
                            "metricName": "loading_percentage",
                            "metricTimeStamp": "2026-05-29T05:59:22.3500002Z",
                            "metricUnit": "%",
                            "metricValue": 41.3,
                            "metricScope": "helios.kg.enrichment",
                            "derivedFrom": "active_power / equipment.nameplate_kva"
                        }
                    ]
                }
            ]
        }
    ],
    "notFound": { //
        "sites": [
            "aa"
        ],
        "equipment": [],
        "points": []
    }
}
