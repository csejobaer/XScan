# dom.py
import requests

def dom_sinks(url):
    sinks = ["document.write","innerHTML","eval(","setTimeout(","setInterval("]
    try:
        r = requests.get(url)
        for sink in sinks:
            if sink in r.text:
                print(f"[DOM SINK FOUND] {url} sink: {sink}")
    except:
        pass
