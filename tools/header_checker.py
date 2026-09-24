import requests


def check_security_headers(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print("\n" + "=" * 55)
    print(f"[*] Analyzing Headers for: {url}")
    print("=" * 55)

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        print(f"[+] Status Code : {response.status_code}")
        print(f"[+] Server      : {headers.get('Server', 'Not Specified')}\n")

        # Key security headers to inspect
        security_headers = [
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Content-Security-Policy",
        ]

        print("--- Security Headers Analysis ---")
        for header in security_headers:
            if header in headers:
                print(f"[✅ PRESENT] {header:<27}: {headers[header]}")
            else:
                print(f"[❌ MISSING] {header}")

        print("=" * 55 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"[!] Connection Error: {e}\n")


def main():
    target_site = input("Enter website domain (e.g., example.com): ").strip()
    if target_site:
        check_security_headers(target_site)


if __name__ == "__main__":
    main()