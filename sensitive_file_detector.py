# sensitive_file_detector.py

import requests
from urllib.parse import urljoin

COMMON_FILES=[
".env",
".git/config",
".git/HEAD",
"backup.zip",
"backup.tar",
"database.sql",
"config.php",
"config.json",
"debug.log",
"error.log"
]

def detect_sensitive_files(base_url):

    found=[]

    print("[*] Checking for sensitive files")

    for file in COMMON_FILES:

        url=urljoin(base_url,file)

        try:

            r=requests.get(url,timeout=6)

            if r.status_code==200:

                print("[SENSITIVE FILE FOUND]",url)

                found.append(url)

        except:
            continue

    return found
