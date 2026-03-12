def generate_payloads(base):

    payloads=[]

    for p in base:

        payloads.append(p)

        payloads.append(p.upper())

        payloads.append(p.replace("<","%3C"))

        payloads.append(p.replace("script","ScRiPt"))

        payloads.append(p.replace("alert","confirm"))

    return list(set(payloads))
