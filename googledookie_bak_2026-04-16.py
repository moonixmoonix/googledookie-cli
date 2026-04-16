import sys
import termios
import tty

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

def main():
    HEADER, HIGHLIGHT, ENDC, BOLD = '\033[95m', '\033[92m', '\033[0m', '\033[1m'
    
    options = [
        "Files Containing Juicy Info",
        "Sensitive Directories / Open Directories",
        "Vulnerable Server Software",
        "Vulnerable Files",
        "Pages Containing Login Portals",
        "Publicly Exposed Documents",
        "Cloud Storage & SaaS Exposure",
        "IoT & Industrial Control Systems",
        "API & Integration Secrets",
        "Identity & Access Management (IAM)"
    ]
    
    current_selection = 0

    while True:
        print("\033[H\033[J", end="")
        print(f"{HEADER}{BOLD}=== GOOGLEDOOKIE: CATEGORIES ==={ENDC}\n")
        
        for i, option in enumerate(options):
            if i == current_selection:
                print(f"{HIGHLIGHT}  -- {option} (Selected){ENDC}")
            else:
                print(f"  -- {option}")
                
        print(f"\n{BOLD}[Arrows to Move, Enter to Select, Q to Quit]{ENDC}")

        key = get_char()
        if key == '\x1b[A': # Up Arrow
            current_selection = (current_selection - 1) % len(options)
        elif key == '\x1b[B': # Down Arrow
            current_selection = (current_selection + 1) % len(options)
        elif key == '\r':
            print(f"\n\nCategory Selected: {options[current_selection]}")
            break
        elif key.lower() == 'q':
            sys.exit()

if __name__ == "__main__":
    main()
