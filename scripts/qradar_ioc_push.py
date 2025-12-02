# scripts/qradar_ioc_push.py

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = "https://192.168.25.100"                 # Example: https://192.168.25.100
API_TOKEN = "96aed746-e9b2-43ef-8cd4-7e42434c77b7"                      # Replace with your QRadar API token
REFERENCE_SET = "phishing_iocs"                     # Reference Set in QRadar

headers = {
    "SEC": API_TOKEN,
    "Content-Type": "application/json"
}


def push_ioc(ioc):
    """Push a single IOC to QRadar Reference Set."""

    url = f"{QRADAR_HOST}/api/reference_data/sets/{REFERENCE_SET}"
    params = {"value": ioc}

    r = requests.post(url, headers=headers, params=params, verify=False)

    if r.status_code in (200, 201):
        print(f"[QRadar] Added IOC → {ioc}")
        return True
    else:
        print(f"[QRadar] Failed to add {ioc}: {r.text}")
        return False


def push_ioc_list(ioc_list):
    """Push a list of IOCs to QRadar."""

    print(f"\n[*] Sending IOCs to QRadar Reference Set → {REFERENCE_SET}")
    for ioc in ioc_list:
        push_ioc(ioc)
    print("[*] IOC upload completed.\n")
