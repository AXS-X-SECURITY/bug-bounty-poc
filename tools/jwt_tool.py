#!/usr/bin/env python3
import base64                                   import json

GREEN, CYAN, NC = "\033[1;32m", "\033[1;36m", "\033[0m"

def decode_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            print("[!] Invalid JWT Token format!")
            return

        # Base64 Decode Header and Payload
        header = base64.b64decode(parts[0] + '==').decode('utf-8')
        payload = base64.b64decode(parts[1] + '==').decode('utf-8')

        print(f"\n{CYAN}[+] Header:{NC}\n{json.dumps(json.loads(header), indent=2)}")
        print(f"\n{GREEN}[+] Payload:{NC}\n{json.dumps(json.loads(payload), indent=2)}")
    except Exception as e:
        print(f"[!] Error decoding JWT: {e}")

if __name__ == "__main__":
    print(f"\n{CYAN}=== JWT Token Analyzer ==={NC}\n")
    jwt = input("Enter JWT Token: ").strip()
    if jwt:
        decode_jwt(jwt)