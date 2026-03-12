# html_report.py

def generate_html(results):

    html="""
    <html>
    <head>
    <title>XSS Scan Report</title>
    </head>
    <body>
    <h1>Scan Results</h1>
    """

    html+=f"<h2>Target</h2><p>{results['target']}</p>"

    html+="<h2>Pages Discovered</h2><ul>"

    for p in results["pages"]:
        html+=f"<li>{p}</li>"

    html+="</ul>"

    html+="<h2>Parameters</h2><ul>"

    for p in results["params"]:
        html+=f"<li>{p}</li>"

    html+="</ul>"

    html+="<h2>Subdomains</h2><ul>"

    for s in results["subdomains"]:
        html+=f"<li>{s}</li>"

    html+="</ul>"

    html+="</body></html>"

    with open("scan_report.html","w") as f:
        f.write(html)

    print("[*] HTML report saved: scan_report.html")
