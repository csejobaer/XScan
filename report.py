# report.py

import json

def save_report(data):

    with open("scan_report.json","w") as f:

        json.dump(data,f,indent=4)

    print("[*] Report saved to scan_report.json")
