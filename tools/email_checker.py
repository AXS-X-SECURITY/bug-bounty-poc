import urllib.request
import json

print("=== 1. Email Breach Check ===")
email = input("Enter email address: ").strip()
url = f"https://api.xposedornot.com/v1/check-email/{email}"
req = urllib.request.Request(url, headers={'User-Agent': 'Termux-Checker'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        if "Error" in result:
            print("[+] SAFE: Email not found in any breach database.")
        else:
            breaches = result.get("breaches", [[]])[0]
            print(f"[!] WARNING: Email found in {len(breaches)} breaches:")
            for site in breaches:
                print(f" - {site}")
except Exception:
    print("[+] SAFE or unable to connect to server.")

print("\n=== 2. Local Password Guessing Test ===")
pwd = input("Enter password to test its strength: ").strip()

# Load common passwords list if not exists
try:
    with open("10k-most-common.txt", "r", encoding="utf-8", errors="ignore") as f:
        common_passwords = [line.strip() for line in f]
except FileNotFoundError:
    print("[*] Downloading common passwords list...")
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
        "10k-most-common.txt"
    )
    with open("10k-most-common.txt", "r", encoding="utf-8", errors="ignore") as f:
        common_passwords = [line.strip() for line in f]

# Simulate guessing
if pwd in common_passwords:
    attempts = common_passwords.index(pwd) + 1
    print(f"[!] CRACKED: Password guessed on attempt #{attempts}!")
    print("[!] This password is VERY WEAK and exists in common wordlists.")
else:
    print("[+] STRONG: Password not in top 10,000 common passwords.")