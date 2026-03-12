# 🔎 XSS & Web Security Scanner

A modular Python-based web application scanner designed to help identify potential **XSS vulnerabilities**, discover hidden endpoints, and analyze web applications through automated reconnaissance.

⚠️ **Disclaimer:** This tool is intended for **educational purposes and authorized security testing only**. Do not use it on systems without permission.

---

# ✨ Features

## 🧭 Reconnaissance & Discovery

* **Directory / Endpoint Discovery**
  Brute-force common directories and hidden endpoints.

* **Subdomain Enumeration**
  Detect common subdomains such as `api`, `dev`, `beta`, `admin`, etc.

* **robots.txt & sitemap.xml Parsing**
  Automatically extract hidden or restricted paths.

* **JavaScript Route Extraction**
  Finds API endpoints embedded inside JavaScript files.

* **SPA Route Extraction**
  Detects API routes used by **React / Vue / Angular** applications.

* **Asynchronous Crawling**
  Multi-page crawling for faster discovery of application endpoints.

* **URL Normalization & Deduplication**
  Prevents duplicate URLs from being scanned multiple times.

---

## 🧪 Input & Parameter Testing

* **Parameter Brute-Forcing**
  Detect common GET parameters such as:

  * `id`
  * `q`
  * `search`
  * `page`

* **JavaScript Parameter Extraction**
  Extracts parameters found in client-side JavaScript code.

* **Automated Form Testing**
  Automatically submits payloads to discovered forms.

---

## 💥 XSS Payload Engine

* **Multiple Payload Contexts**

  * HTML context
  * Attribute context
  * JavaScript context
  * URL context

* **Encoded Payload Variants**

  * HTML encoded (`&lt;script&gt;`)
  * URL encoded (`%3Cscript%3E`)
  * Double encoded payloads

* **Mutation Techniques**

  * Case mutation (`ScRiPt`)
  * Event mutation (`alert → confirm / prompt`)

* **Reflection Detection**
  Detects when payloads are reflected in HTTP responses.

---

## 🔐 Security Checks

* **Sensitive File Detection**

Checks for common exposed files such as:

.env
.git/config
backup.zip
config.php
error.log

* **Rate Limiting**

Prevents sending requests too quickly to avoid blocking or triggering WAF protections.

---

## 📊 Reporting

* **JSON Report**
  Structured scan results for automation and analysis.

* **HTML Report**
  Human-readable report summarizing findings.

---

# ⚡ Performance & Stability

* Request timeouts and error handling
* Random request delays (anti-blocking)
* Asynchronous crawling for speed
* URL normalization for clean scanning

---

# 🛠 Technologies Used

* Python 3
* requests
* aiohttp
* BeautifulSoup
* asyncio

---

# 🚀 Example Usage

```bash
python scanner.py
```

Then enter a target URL:

```
Enter target URL: https://example.com
```

Example output:

```
[*] Total pages discovered: 42
[*] Payloads loaded: 24
[REFLECTION FOUND] https://example.com/search?q=<payload>
```

Reports will be generated:

```
scan_report.json
scan_report.html
```

---

# 📁 Project Structure

```
scanner/
│
├── scanner.py
├── endpoint_finder.py
├── async_crawler.py
├── spa_route_extractor.py
├── js_route_extractor.py
├── js_param_extractor.py
├── param_bruteforce.py
├── payload_library.py
├── xss_detector.py
├── subdomain_enum.py
├── sensitive_file_detector.py
├── robots_sitemap_harvester.py
├── rate_limiter.py
├── url_normalizer.py
├── report.py
└── html_report.py
```

---

# 📌 Future Improvements

* DOM-based XSS detection
* Headless browser analysis
* Stored XSS detection
* Authentication/session scanning
* Advanced payload mutation engine

---

# 📜 License

This project is for **educational and authorized security testing purposes only**.
