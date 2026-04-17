import sys
import termios
import tty
import time
import os
import requests
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)"
]

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def fetch_results(query):
    results = []

    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        time.sleep(random.uniform(1.5, 3.0))

        response = requests.post(
            url,
            data={"q": query},
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.select("a.result__a"):
            link = a.get("href")
            if link and link.startswith("http"):
                if link not in results:
                    results.append(link)

    except Exception as e:
        print(f"Error: {e}")
        input("\nPress Enter...")
        return []

    return results


def execute_search(query):
    while True:
        print("\033[H\033[J", end="")
        print(f"\033[95m\033[1m=== EXECUTING SEARCH ===\033[0m")
        print(f"QUERY: \033[94m{query}\033[0m\n")

        results = fetch_results(query)

        if not results:
            print("\033[91mNo results found.\033[0m")
            input("\nPress Enter...")
            return

        for i, url in enumerate(results[:15]):
            print(f" [{i+1}] {url}")

        print(f"\n\033[1m[S] Save to File | [E] Edit Query | [Enter] Main Menu\033[0m")
        choice = input("\nAction: ").lower()

        if choice == 's':
            with open("dork_results.txt", "a") as f:
                f.write(f"\n--- {query} ---\n")
                for r in results[:15]:
                    f.write(f"{r}\n")
            print("Saved!")
            time.sleep(1)

        elif choice == 'e':
            query = input("\nEdit Query: ").strip()
            continue
        else:
            break


def handle_c1a1():
    while True:
        print("\033[H\033[J", end="")
        print("\033[95m\033[1m=== DORK INFO: C1A1 - Log Files (Passwords) ===\033[0m\n")

        print("\033[1mEXPLANATION:\033[0m")
        print("Targets .log files that may contain sensitive data like plaintext passwords,\n"
              "session tokens, or server activity logs accidentally exposed.\n")

        print("\033[1mEXAMPLE TARGETS:\033[0m")
        print(" * domain.com")
        print(" * \"admin\"")
        print(" * \"error\"\n")

        print("\033[94mDORK:\033[0m filetype:log \"password\"\n")

        user_input = input("Enter search terms or [Enter] for general (Q to quit): ").strip()

        if user_input.lower() == 'q':
            return

        query = f'filetype:log "password" {user_input}'.strip()
        execute_search(query)
        break


def main():
    H, HI, SUB, END, B = '\033[95m', '\033[92m', '\033[94m', '\033[0m', '\033[1m'

    DATA = {
        "C1: Files Containing Juicy Info": [
            "C1A1: Log Files (Passwords)", "C1A2: Environment Files",
            "C1A3: AWS Credentials", "C1A4: Config Credentials",
            "C1A5: SQL Database Dumps", "C1A6: Mail Archives",
            "C1A7: Password Lists"
        ],
        "C2: Sensitive Directories": [
            "C2A1: Basic Index Discovery", "C2A2: Backup Directories",
            "C2A3: Config Access", "C2A4: Admin Folders",
            "C2A5: DCIM / Media", "C2A6: FTP Indexing"
        ],
        "C3: Vulnerable Server Software": [
            "C3A1: Apache Server Status", "C3A2: WordPress Config",
            "C3A3: Joomla Setup", "C3A4: Outdated PHP",
            "C3A5: Envoy Proxy Info"
        ],
        "C4: Vulnerable Files": [
            "C4A1: SQLi Entry Point", "C4A2: Error Leakage",
            "C4A3: Open Redirects", "C4A4: XSS Target",
            "C4A5: CGI Scripts"
        ],
        "C5: Pages Containing Login Portals": [
            "C5A1: Generic Admin", "C5A2: Okta/SSO Portals",
            "C5A3: Cpanel Access", "C5A4: Router Logins",
            "C5A5: Jenkins Dashboards"
        ],
        "C6: Publicly Exposed Documents": [
            "C6A1: Confidential PDF", "C6A2: Excel Payroll",
            "C6A3: Word Doc Leaks", "C6A4: CV/Resume List",
            "C6A5: Gov Policy"
        ],
        "C7: Cloud Storage & SaaS Exposure": [
            "C7A1: AWS S3 Buckets", "C7A2: Google Drive Leaks",
            "C7A3: Firebase Databases", "C7A4: Azure Blobs"
        ],
        "C8: IoT & Industrial Control Systems": [
            "C8A1: IP Camera Feeds", "C8A2: Printer Interfaces",
            "C8A3: Smart Building Controls", "C8A4: VoIP Phone Panels"
        ],
        "C9: API & Integration Secrets": [
            "C9A1: API Documentation", "C9A2: Postman Collections",
            "C9A3: Stripe/Payment Keys", "C9A4: GitHub Action Logs"
        ],
        "C10: Identity & Access Management (IAM)": [
            "C10A1: VPN Client Configs", "C10A2: Active Directory Info",
            "C10A3: SSH Private Keys", "C10A4: Auth0/JWT Configs"
        ],
        "GHDB: External Database": ["Search GHDB by Keyword"]
    }

    cats = list(DATA.keys())
    exp = {cat: False for cat in cats}
    sel = 0

    while True:
        disp = []

        for c in cats:
            disp.append(('cat', c))
            if exp[c]:
                for t in DATA[c]:
                    disp.append(('type', t))

        print("\033[H\033[J", end="")
        print(f"{H}{B}=== GOOGLEDOOKIE: OSINT FRAMEWORK ==={END}\n")

        for i, (k, n) in enumerate(disp):
            p = " > " if k == 'cat' else "   └─ "
            m = (" [▼]" if exp[n] else " [▶]") if k == 'cat' else ""
            s = HI if i == sel else (B + END if k == 'cat' else SUB)
            print(f"{s}{p}{n}{m}{END}")

        print(f"\n{B}[Arrows to Move, Enter to Select, Q to Quit]{END}")

        key = get_char()

        if key == '\x1b[A':
            sel = (sel - 1) % len(disp)

        elif key == '\x1b[B':
            sel = (sel + 1) % len(disp)

        elif key == '\r':
            k, n = disp[sel]

            if k == 'cat':
                exp[n] = not exp[n]

            elif n == "C1A1: Log Files (Passwords)":
                handle_c1a1()

            elif n == "Search GHDB by Keyword":
                pass  # placeholder

        elif key.lower() == 'q':
            sys.exit()


if __name__ == "__main__":
    main()
