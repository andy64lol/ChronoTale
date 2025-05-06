import os
import subprocess
import sys
import time
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Game data persistence
def load_game_data():
    """Load game statistics from JSON file"""
    try:
        with open('game_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'plays': 0, 'tokens': 0}

def save_game_data(data):
    """Save game statistics to JSON file"""
    with open('game_data.json', 'w') as f:
        json.dump(data, f)

# Core functions
def display_banner():
    """Display the ChronoTale banner with pixel font"""
    print(Fore.YELLOW + r"""
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░                    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░                      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░                    ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
""" + Fore.CYAN + "A Multidimensional Adventure Launcher")
    print("\n" + "═" * 50 + "\n")

def check_file(file_name):
    """Check if a game file exists"""
    if not os.path.isfile(file_name):
        print(Fore.RED + f"█ Error: {file_name} not found!")
        return False
    return True

def launch_game(file_name):
    """Launch the specified game file"""
    try:
        game_name = os.path.splitext(os.path.basename(file_name))[0]
        print(Fore.GREEN + f"\n█ Launching {game_name}..." + Style.RESET_ALL)

        # Pixel-style loading animation
        frames = ["[■□□□]", "[■■□□]", "[■■■□]", "[■■■■]"]
        for frame in frames:
            print(Fore.BLUE + f"█ Loading {frame}", end='\r')
            time.sleep(0.2)

        subprocess.run([sys.executable, file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"█ Crash: Game exited with error {e.returncode}")
    except Exception as e:
        print(Fore.RED + f"█ Crash: {e}")

# Menu system
def games_menu(data):
    """Display games submenu"""
    games = {
        '1': ("Legacies", "Legacies.py"),
        '2': ("Liminal", "Liminal.py"),
        '3': ("Exodus", "Exodus.py"),
        '4': ("Z_survival", "Z_survival.py"),
        '5': ("My first day here: Campus Life", "school.py")
    }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(Fore.CYAN + f"█ Total Plays: {data['plays']} | Tokens: {data['tokens']}")
        print("\n" + "═" * 50 + "\n")
        print(Fore.MAGENTA + "█ Available Games:\n")
        for key, (name, _) in games.items():
            print(Fore.CYAN + f"█ [{key}] {name}")
        print(Fore.RED + "█ [6] Back to Main Menu")

        choice = input(Fore.YELLOW + "\n█ Select: " + Style.RESET_ALL)

        if choice in games:
            game_file = games[choice][1]
            if check_file(game_file):
                start_time = time.time()
                launch_game(game_file)
                end_time = time.time()
                
                # Calculate playtime tokens
                elapsed = end_time - start_time
                elapsed_minutes = elapsed // 60
                time_tokens = (elapsed_minutes // 5) * 10
                
                # Update game data
                data['plays'] += 1
                data['tokens'] += 5 + time_tokens
                save_game_data(data)
                
                input(Fore.YELLOW + "\n█ Press Enter to continue..." + Style.RESET_ALL)
        elif choice == '6':
            return
        else:
            print(Fore.RED + "\n█ Invalid input!")
            time.sleep(1)

def shop_menu(data):
    """Display token shop"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(Fore.CYAN + "█ Welcome to the Token Shop!")
    print(Fore.YELLOW + "█ Shop is coming soon! You can use your tokens here.")
    print(Fore.CYAN + f"█ Your current balance: {data['tokens']} Tokens")
    input(Fore.YELLOW + "\n█ Press Enter to return to main menu..." + Style.RESET_ALL)

def credits_menu():
    """Display credits"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(Fore.CYAN + "█ Credits:")
    print(Fore.GREEN + "█ Developed by andy64lol")
    input(Fore.YELLOW + "\n█ Press Enter to return to main menu..." + Style.RESET_ALL)

def settings_menu():
    """Display settings"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(Fore.CYAN + "█ Settings:")
    print(Fore.YELLOW + "█ Settings menu is under construction")
    input(Fore.YELLOW + "\n█ Press Enter to return to main menu..." + Style.RESET_ALL)

def main_menu():
    """Main menu controller"""
    data = load_game_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(Fore.CYAN + f"█ Total Plays: {data['plays']} | Tokens: {data['tokens']}")
        print("\n" + "═" * 50 + "\n")
        print(Fore.MAGENTA + "█ Main Menu:\n")
        print(Fore.CYAN + "█ [1] Games")
        print(Fore.CYAN + "█ [2] Shop")
        print(Fore.CYAN + "█ [3] Credits")
        print(Fore.CYAN + "█ [4] Settings")
        print(Fore.RED + "█ [5] Quit")

        choice = input(Fore.YELLOW + "\n█ Select: " + Style.RESET_ALL)

        if choice == '1':
            games_menu(data)
        elif choice == '2':
            shop_menu(data)
        elif choice == '3':
            credits_menu()
        elif choice == '4':
            settings_menu()
        elif choice == '5':
            print(Fore.YELLOW + "\n█ Closing...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "\n█ Invalid input!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n█ Force quit!")
        sys.exit(0)
