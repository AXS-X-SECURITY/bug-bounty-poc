import sys
import requests                                 
# Disable SSL warnings
requests.packages.urllib3.disable_warnings()    
IMPORTANT_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy",
]


def check_cors(url):
    headers = {                                         "User-Agent": "Ammar-CORS-Analyzer/1.0",
        "Origin": "https://evil-attacker.com",
    }

    print("\n" + "=" * 60)
    print(f"[*] Starting CORS & Security Headers Scan on: {url}")
    print("=" * 60 + "\n")

    try:
        response = requests.get(url, headers=headers, timeout=6, verify=False)
        res_headers = response.headers

        # 1. CORS Vulnerability Analysis
        print("[*] Checking CORS Configuration...")
        allow_origin = res_headers.get("Access-Control-Allow-Origin")
        allow_credentials = res_headers.get("Access-Control-Allow-Credentials")

        if allow_origin == "https://evil-attacker.com":
            if allow_credentials == "true":
                print(
                    "[🔥] CRITICAL VULNERABILITY! CORS misconfiguration allows Arbitrary Origin with Credentials!"
                )
            else:
                print(
                    "[⚡] POTENTIAL RISK: CORS reflects untrusted Origin (evil-attacker.com)."
                )
        elif allow_origin == "*":
            print(
                "[!] WARNING: Access-Control-Allow-Origin is set to wildcard (*)."
            )
        else:
            print("[+] CORS Configuration looks secure or restricted.")

        # 2. Security Headers Analysis
        print("\n[*] Checking Missing Security Headers...")
        missing_headers = []
        for h in IMPORTANT_HEADERS:
            if h in res_headers:
                print(f"[+] [FOUND] {h}: {res_headers[h][:50]}...")
            else:
                print(f"[-] [MISSING] {h}")
                missing_headers.append(h)

        if missing_headers:
            print(
                f"\n[!] Total Missing Security Headers: {len(missing_headers)}"
            )

    except requests.RequestException as e:
        print(f"[!] Connection Error: {e}")


def main():
    print("=== CORS & Security Headers Analyzer ===")
    url = input(
        "Enter Full URL (e.g. https://example.com or https://api.example.com): "
    ).strip()

    if url:
        check_cors(url)
    else:
        print("[!] URL cannot be empty.")


if __name__ == "__main__":
    main()