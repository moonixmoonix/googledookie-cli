import sys
import termios
import tty
import time
import os

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

def handle_c1a1():
    while True:
        print("\033[H\033[J", end="")
        print(f"\033[95m\033[1m=== DORK INFO: C1A1 - Log Files (Passwords) ===\033[0m\n")
        print("EXPLANATION:")
        print("Targets log files that may contain plaintext credentials. You must")
        print("provide a filter such as a domain name, organization name, or app name.\n")
        
        print("\033[1mEXAMPLES (Using Foo's Bar / foos-bar.com):\033[0m")
        print("  1. Domain: \033[94mfiletype:log \"password\" foos-bar.com\033[0m")
        print("  2. Org Name: \033[94mfiletype:log \"password\" \"Foo's Bar\"\033[0m")
        print("  3. App Name: \033[94mfiletype:log \"password\" foosbar_mobile_app\033[0m\n")
        
        print("\033[1mPOSSIBLE RESULTS:\033[0m")
        print("  - foos-bar.com/logs/auth.log  -> 'Failed login for user admin: pass123'")
        print("  - backup.foos-bar.com/debug.log -> 'DB_CONNECT: root / foobar_pwd_2026'\n")
        
        user_input = input("Enter search terms (Domain, Org, or App) or 'q' to return: ").strip()
        
        if user_input.lower() == 'q':
            return None
        elif user_input == "":
            continue
        else:
            print(f"\n\033[92mTarget saved: {user_input}\033[0m")
            time.sleep(1)
            return user_input

def main():
    HEADER, HIGHLIGHT, SUB, ENDC, BOLD = '\033[95m', '\033[92m', '\033[94m', '\033[0m', '\033[1m'
    
    DATA = {
        "C1: Files Containing Juicy Info": ["C1A1: Log Files (Passwords)", "C1A2: Environment Files", "C1A3: AWS Credentials", "C1A4: Config Credentials", "C1A5: SQL Database Dumps", "C1A6: Mail Archives", "C1A7: Password Lists"],
        "C2: Sensitive Directories / Open Directories": ["C2A1: Basic Index Discovery", "C2A2: Backup Directories", "C2A3: Config/ETC Access", "C2A4: Admin Folders", "C2A5: DCIM / Media", "C2A6: FTP Indexing"],
        "C3: Vulnerable Server Software": ["C3A1: Apache Server Status", "C3A2: WordPress Config", "C3A3: Joomla Setup", "C3A4: Outdated PHP", "C3A5: Envoy Proxy Info"],
        "C4: Vulnerable Files": ["C4A1: SQLi Entry Point", "C4A2: Error Leakage", "C4A3: Open Redirects", "C4A4: XSS Target", "C4A5: CGI Scripts"],
        "C5: Pages Containing Login Portals": ["C5A1: Generic Admin", "C5A2: Okta/SSO Portals", "C5A3: Cpanel Access", "C5A4: Router Logins", "C5A5: Jenkins Dashboards"],
        "C6: Publicly Exposed Documents": ["C6A1: Confidential PDF", "C6A2: Excel Payroll", "C6A3: Word Doc Leaks", "C6A4: CV/Resume List", "C6A5: Gov Policy"],
        "C7: Cloud Storage & SaaS Exposure": ["C7A1: AWS S3 Buckets", "C7A2: Google Drive Leaks", "C7A3: Firebase Databases", "C7A4: Azure Blobs"],
        "C8: IoT & Industrial Control Systems": ["C8A1: IP Camera Feeds", "C8A2: Printer Interfaces", "C8A3: Smart Building Controls", "C8A4: VoIP Phone Panels"],
        "C9: API & Integration Secrets": ["C9A1: API Documentation", "C9A2: Postman Collections", "C9A3: Stripe/Payment Keys", "C9A4: GitHub Action Logs"],
        "C10: Identity & Access Management (IAM)": ["C10A1: VPN Client Configs", "C10A2: Active Directory Info", "C10A3: SSH Private Keys", "C10A4: Auth0/JWT Configs"]
    }
    
    categories = list(DATA.keys())
    expanded = {cat: False for cat in categories}
    current_selection = 0

    while True:
        display_list = []
        for cat in categories:
            display_list.append(('cat', cat))
            if expanded[cat]:
                for t in DATA[cat]:
                    display_list.append(('type', t))
        
        current_selection = max(0, min(current_selection, len(display_list) - 1))
        print("\033[H\033[J", end="")
        print(f"{HEADER}{BOLD}=== GOOGLEDOOKIE: OSINT FRAMEWORK ==={ENDC}\n")
        
        for i, (kind, name) in enumerate(display_list):
            if kind == 'cat':
                prefix = " > "
                marker = " [▼]" if expanded[name] else " [▶]"
                style = HIGHLIGHT if i == current_selection else (BOLD + ENDC)
            else:
                prefix = "   └─ "
                marker = ""
                style = HIGHLIGHT if i == current_selection else SUB
            print(f"{style}{prefix}{name}{marker}{ENDC}")

        # Re-adding the missing UI instruction block
        print(f"\n{BOLD}[Arrows to Move, Enter to Select/Expand, Q to Quit]{ENDC}")

        key = get_char()
        if key == '\x1b[A':
            current_selection = (current_selection - 1) % len(display_list)
        elif key == '\x1b[B':
            current_selection = (current_selection + 1) % len(display_list)
        elif key == '\r':
            kind, name = display_list[current_selection]
            if kind == 'cat':
                expanded[name] = not expanded[name]
                time.sleep(0.05)
            elif name == "C1A1: Log Files (Passwords)":
                target = handle_c1a1()
                if target:
                    pass
            else:
                print(f"\n\n{HIGHLIGHT}Targeting: {name}{ENDC}")
                time.sleep(1)
        elif key.lower() == 'q':
            sys.exit()

if __name__ == "__main__":
    main()
