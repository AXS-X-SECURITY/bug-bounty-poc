import sys
import requests
                                                # Disable SSL warnings for testing
requests.packages.urllib3.disable_warnings()


def test_idor(base_url, param_name, start_id, end_id, cookies_str=""):                              headers = {"User-Agent": "Ammar-IDOR-Scanner/1.0"}

    # Parse cookies if provided (Format: key1=val1; key2=val2)
    cookies = {}
    if cookies_str:
        for item in cookies_str.split(";"):                 if "=" in item:
                k, v = item.strip().split("=", 1)
                cookies[k] = v

    print("\n" + "=" * 55)
    print(f"[*] Starting IDOR Scan on Parameter: {param_name}")
    print(f"[*] ID Range: {start_id} to {end_id}")
    print("=" * 55 + "\n")

    for current_id in range(start_id, end_id + 1):
        target_url = f"{base_url}?{param_name}={current_id}"

        try:
            response = requests.get(
                target_url, headers=headers, cookies=cookies, timeout=5, verify=False
            )
            status = response.status_code
            length = len(response.text)

            # Highlighting potential hits (200 OK)
            if status == 200:
                print(
                    f"[+] [200 OK] ID: {current_id} | Size: {length} bytes -> {target_url}"
                )
            elif status == 403 or status == 401:
                print(
                    f"[-] [{status}] ID: {current_id} | Access Denied (Protected)"
                )
            else:
                print(f"[?] [{status}] ID: {current_id} | Size: {length} bytes")

        except requests.RequestException as e:
            print(f"[!] ID: {current_id} Error: {e}")


def main():
    print("=== IDOR Vulnerability Scanner ===")
    base_url = input(
        "Enter Base URL (e.g. https://example.com/api/user): "
    ).strip()
    param_name = input("Enter ID Parameter Name (e.g. id or user_id): ").strip()

    try:
        start_id = int(input("Enter Start ID (e.g. 1): "))
        end_id = int(input("Enter End ID (e.g. 10): "))
    except ValueError:
        print("[!] Invalid numeric ID range.")
        return

    cookies_str = input(
        "Enter Session Cookies (Optional, press Enter to skip): "
    ).strip()

    test_idor(base_url, param_name, start_id, end_id, cookies_str)


if __name__ == "__main__":
    main()