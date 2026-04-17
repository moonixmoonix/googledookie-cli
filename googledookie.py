import sys
import termios
import tty
import time
import os
from googlesearch import search

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

def execute_search(query):
    while True:
        print("\033[H\033[J", end="")
        print(f"\033[95m\033[1m=== EXECUTING SEARCH ===\033[0m")
        print(f"QUERY: \033[94m{query}\033[0m\n")
        
        results = []
        try:
            for url in search(query, num_results=10):
                results.append(url)
        except Exception as e:
            print(f"Error fetching results: {e}")
            time.sleep(2)
            return

        if not results:
            print("No results found.")
            time.sleep(2)
            return

        for i, url in enumerate(results):
            print(f" [{i+1}] {url}")
        
        print(f"\n\033[1m[S] Save to File | [E] Edit Query | [Q] Main Menu\033[0m")
        choice = input("\nAction: ").lower()
        
        if choice == 's':
            filename = "dork_results.txt"
            with open(filename, "a") as f:
                f.write(f"\n--- QUERY: {query} ---\n")
                for r in results:
                    f.write(f"{r}\n")
            print(f"\033[92mSaved to {filename}!\033[0m")
            time.sleep(1.5)
        elif choice == 'e':
            query = input("\nEdit Query: ").strip()
            continue
        elif choice == 'q':
            break
        else:
            print("Invalid selection.")
            time.sleep(1)

def handle_c1a1():
    while True:
        print("\033[H\033[J", end="")
        print(f"\033[95m\033[1m=== DORK INFO: C1A1 - Log Files (Passwords) ===\033[0m\n")
        print("EXPLANATION: Targets log files that may contain plaintext credentials.\n")
        user_input = input("Enter search terms (Domain, Org, or App) or 'q' to return: ").strip()
        if user_input.lower() == 'q': return
        elif user_input == "": continue
        
        final_dork = f'filetype:log "password" {user_input}'
        execute_search(final_dork)
        break

def search_ghdb_keyword():
    print("\033[H\033[J", end="")
    print(f"\033[95m\033[1m=== GHDB EXPANDED LIBRARY SEARCH ===\033[0m\n")
    query = input("Enter search keyword (e.g., 'camera', 'password'): ").strip().lower()
    if not query: return
    
    library = [
        {"title": "Exposed Webcam / IP Camera", "dork": "inurl:\"view/index.shtml\""},
        {"title": "Live View Camera Feed", "dork": "inurl:\"/view/view.shtml\""},
        {"title": "Axis Network Camera Feed", "dork": "intitle:\"live view - axis\""},
        {"title": "Toshiba Network Camera", "dork": "intitle:\"toshiba network camera\" user"},
        {"title": "Sony Network Camera (SNC)", "dork": "intitle:\"snc-rz30\""},
        {"title": "Panasonic IP Camera", "dork": "intitle:\"network camera\" inurl:\"viewerframe\""},
        {"title": "Mobotix Camera Portal", "dork": "intitle:\"control center\" mobotix"},
        {"title": "D-Link IP Camera", "dork": "intitle:\"d-link web configuration\""},
        {"title": "Hikvision Device Login", "dork": "intitle:\"hikvision\" inurl:\"login\""},
        {"title": "Exposed MySQL Config", "dork": "filename:config.php db_password"},
        {"title": "WordPress Backup Archive", "dork": "index of /wp-content/backups/"},
        {"title": "Vulnerable PHPinfo Leak", "dork": "ext:php intitle:phpinfo \"published by the PHP Group\""},
        {"title": "Publicly Shared .env File", "dork": "filename:.env \"DB_PASSWORD\""},
        {"title": "Open FTP Root Directory", "dork": "intitle:\"index of\" \"ftp\""},
        {"title": "Apache Server Status Info", "dork": "server-status \"Apache Server Status\""}
    ]
    
    results = [res for res in library if query in res['title'].lower() or query in res['dork'].lower()]
    
    if not results:
        print(f"\nNo results found for '{query}'.")
        time.sleep(1.5)
        return

    current_res = 0
    while True:
        print("\033[H\033[J", end="")
        print(f"\033[95m\033[1m=== GHDB RESULTS FOR: {query} ===\033[0m\n")
        for i, res in enumerate(results):
            style = '\033[92m' if i == current_res else ''
            prefix = " * " if i == current_res else "   "
            print(f"{style}{prefix}{res['title']} (Dork: {res['dork']})\033[0m")
        
        print(f"\n\033[1m[Arrows to Move, Enter to Select, Q to Cancel]\033[0m")
        key = get_char()
        if key == '\x1b[A': current_res = (current_res - 1) % len(results)
        elif key == '\x1b[B': current_res = (current_res + 1) % len(results)
        elif key == '\r':
            selected_dork = results[current_res]['dork']
            target = input("\nEnter Target (Domain/Org) or leave blank: ").strip()
            final = f"{selected_dork} {target}".strip()
            execute_search(final)
            return
        elif key.lower() == 'q': return

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
        "C10: Identity & Access Management (IAM)": ["C10A1: VPN Client Configs", "C10A2: Active Directory Info", "C10A3: SSH Private Keys", "C10A4: Auth0/JWT Configs"],
        "GHDB: External Database": ["Search GHDB by Keyword"]
    }
    categories = list(DATA.keys())
    expanded = {cat: False for cat in categories}
    current_selection = 0
    while True:
        display_list = []
        for cat in categories:
            display_list.append(('cat', cat))
            if expanded[cat]:
                for t in DATA[cat]: display_list.append(('type', t))
        current_selection = max(0, min(current_selection, len(display_list) - 1))
        print("\033[H\033[J", end="")
        print(f"{HEADER}{BOLD}=== GOOGLEDOOKIE: OSINT FRAMEWORK ==={ENDC}\n")
        for i, (kind, name) in enumerate(display_list):
            prefix = " > " if kind == 'cat' else "   └─ "
            marker = (" [▼]" if expanded[name] else " [▶]") if kind == 'cat' else ""
            style = HIGHLIGHT if i == current_selection else (BOLD + ENDC if kind == 'cat' else SUB)
            print(f"{style}{prefix}{name}{marker}{ENDC}")
        print(f"\n{BOLD}[Arrows to Move, Enter to Select, Q to Quit]{ENDC}")
        key = get_char()
        if key == '\x1b[A': current_selection = (current_selection - 1) % len(display_list)
        elif key == '\x1b[B': current_selection = (current_selection + 1) % len(display_list)
        elif key == '\r':
            kind, name = display_list[current_selection]
            if kind == 'cat': expanded[name] = not expanded[name]
            elif name == "C1A1: Log Files (Passwords)": handle_c1a1()
            elif name == "Search GHDB by Keyword": search_ghdb_keyword()
            else:
                print(f"\n\n{HIGHLIGHT}Targeting: {name}{ENDC}")
                time.sleep(1)
        elif key.lower() == 'q': sys.exit()

if __name__ == "__main__": main()
