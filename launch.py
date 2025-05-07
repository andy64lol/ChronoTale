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
            data = json.load(f)
            if 'purchased_games' not in data:
                data['purchased_games'] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {'plays': 0, 'tokens': 0, 'purchased_games': []}

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
    original_games = [
        ("Legacies", "Legacies.py"),
        ("Liminal", "Liminal.py"),
        ("Exodus", "Exodus.py"),
        ("Z_survival", "Z_survival.py"),
        ("My first day here: Campus Life", "school.py")
    ]
    purchased_games = [tuple(game) for game in data['purchased_games']]
    all_games = original_games + purchased_games

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(Fore.CYAN + f"█ Total Plays: {data['plays']} | Tokens: {data['tokens']}")
        print("\n" + "═" * 50 + "\n")
        print(Fore.MAGENTA + "█ Available Games:\n")
        
        # Display games with numbering
        for idx, (name, file) in enumerate(all_games, 1):
            print(Fore.CYAN + f"█ [{idx}] {name}")
        
        back_number = len(all_games) + 1
        print(Fore.RED + f"█ [{back_number}] Back to Main Menu")

        choice = input(Fore.YELLOW + "\n█ Select: " + Style.RESET_ALL)

        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(all_games):
                selected_game = all_games[choice_int - 1]
                game_name, game_file = selected_game
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
                    data['tokens'] += 5 + int(time_tokens)
                    save_game_data(data)
                    
                    input(Fore.YELLOW + "\n█ Press Enter to continue..." + Style.RESET_ALL)
            elif choice_int == back_number:
                return
            else:
                print(Fore.RED + "\n█ Invalid input!")
                time.sleep(1)
        except ValueError:
            print(Fore.RED + "\n█ Invalid input!")
            time.sleep(1)

def shop_menu(data):
    """Display token shop"""
    purchasable_games = [
        {"name": "Shipwrecked", "file": "shipwrecked.py", "cost": 30}
    ]
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(Fore.CYAN + "█ Welcome to the Token Shop!")
        print(Fore.YELLOW + "█ Available Items:\n")
        
        # Display purchasable games
        for idx, game in enumerate(purchasable_games, 1):
            purchased = any(g[0] == game["name"] and g[1] == game["file"] for g in data['purchased_games'])
            status = Fore.GREEN + "Purchased" if purchased else Fore.YELLOW + f"Cost: {game['cost']} Tokens"
            print(Fore.CYAN + f"█ [{idx}] {game['name']} - {status}")
        
        print(Fore.RED + f"█ [{len(purchasable_games)+1}] Back to Main Menu")
        print(Fore.CYAN + f"\n█ Your current balance: {data['tokens']} Tokens")
        
        choice = input(Fore.YELLOW + "\n█ Select: " + Style.RESET_ALL)
        
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(purchasable_games):
                selected_game = purchasable_games[choice_int - 1]
                # Check if already purchased
                if any(g[0] == selected_game["name"] and g[1] == selected_game["file"] for g in data['purchased_games']):
                    print(Fore.RED + "█ You already own this game!")
                    time.sleep(1)
                    continue
                # Check tokens
                if data['tokens'] >= selected_game["cost"]:
                    data['tokens'] -= selected_game["cost"]
                    data['purchased_games'].append([selected_game["name"], selected_game["file"]])
                    save_game_data(data)
                    print(Fore.GREEN + f"█ Purchased {selected_game['name']}!")
                    time.sleep(1)
                else:
                    print(Fore.RED + "█ Insufficient tokens!")
                    time.sleep(1)
            elif choice_int == len(purchasable_games) + 1:
                return
            else:
                print(Fore.RED + "█ Invalid input!")
                time.sleep(1)
        except ValueError:
            print(Fore.RED + "█ Invalid input!")
            time.sleep(1)

def credits_menu():
    """Display credits"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(Fore.CYAN + "█ Credits:")
    print(Fore.GREEN + "█ Developed by ChronoTale Studios")
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
