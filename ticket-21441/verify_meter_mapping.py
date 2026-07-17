#!/usr/bin/env python3
"""Verify Excel files against generated meterIdSiteIdTable text files."""
import pandas as pd
import re
from pathlib import Path

pairs = [
    ('Sites need both May and June interval data.xlsx', 'meterIdSiteIdTable_new.txt'),
    ('Sites need entier June interval data.xlsx', 'Sites_need_entier_June_interval_data_meterIdSiteIdTable.txt'),
]

for excel_file, txt_file in pairs:
    print('---', excel_file)
    df = pd.read_excel(excel_file)
    print('Excel rows:', len(df))
    cols = list(df.columns)
    print('Excel columns:', cols)

    site_col = None
    meter_col = None
    for c in cols:
        lc = str(c).lower().strip()
        if site_col is None and ('siteid' in lc or 'site_id' in lc or lc == 'site'):
            site_col = c
        if meter_col is None and ('meterid' in lc or 'meter_id' in lc or 'leapmeterid' in lc or 'leapmetid' in lc or 'leap meter' in lc or 'leap' in lc):
            meter_col = c
    print('Detected site col:', site_col, 'meter col:', meter_col)

    df2 = df[[site_col, meter_col]].dropna()
    df2[site_col] = df2[site_col].astype(str).str.strip()
    df2[meter_col] = df2[meter_col].astype(str).str.strip()
    print('Non-null rows:', len(df2))
    print('Unique siteIds in excel:', df2[site_col].nunique())
    print('Unique meterIds in excel:', df2[meter_col].nunique())

    txt = Path(txt_file).read_text()
    ids = re.findall(r"'([^']*)'", txt)
    if len(ids) % 2 != 0:
        print('ERROR: odd quoted value count', len(ids))
    pairs_txt = [(ids[i], ids[i+1]) for i in range(0, len(ids), 2)]
    print('Parsed pairs in txt:', len(pairs_txt))
    sites_txt = [p[0] for p in pairs_txt]
    meters_txt = [p[1] for p in pairs_txt]
    print('Unique sites in txt:', len(set(sites_txt)))
    print('Unique meters in txt:', len(set(meters_txt)))
    print('Duplicate site count in txt:', len(pairs_txt) - len(set(sites_txt)))
    print('Duplicate meter count in txt:', len(pairs_txt) - len(set(meters_txt)))
    print('Excel rows == pairs:', len(df2) == len(pairs_txt))

    excel_sites = set(df2[site_col])
    txt_sites = set(sites_txt)
    missing = excel_sites - txt_sites
    extra = txt_sites - excel_sites
    print('Missing siteIds in txt:', len(missing))
    print('Extra siteIds in txt:', len(extra))
    if missing:
        print('Sample missing:', list(missing)[:5])
    if extra:
        print('Sample extra:', list(extra)[:5])
    print()
