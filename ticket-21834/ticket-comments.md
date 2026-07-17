Juan Culebro
commented 8h ago


@Sanjeev Lakkaraju @Young Lee
are we expecting EACH INDIVIDUAL TIMESTAMP to have all this information?
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
KQL can't guarrantee an ordered array when creating one, but one other option could be 
                        {
                            "pointId": "01919c2e-f780-7000-9abc-def018595078",
                            "pointKey": "active_power",
                            "metricName": "active_power",
                            "readings": 
                                   [
                                         {"timestamp": "2026-05-29T05:59:22.3500002Z", "value": 412.7},
                                         {"timestamp": "2026-05-29T06:30:27.3500002Z", "value": 412.8}
                                   ]
                            "metricUnit": "KiloW",
                            "metricScope": "helios.telemetry.pipeline",
                            "derivedFrom": ""
                        },