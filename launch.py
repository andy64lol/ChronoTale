import os
import subprocess
import sys
import time
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "1.2.0"

# Game data persistence
def load_game_data():
    """Load game statistics from JSON file"""
    try:
        with open('game_data.json', 'r') as f:
            data = json.load(f)
            if 'purchased_games' not in data:
                data['purchased_games'] = []
            if 'settings' not in data:
                data['settings'] = {'colors_enabled': True}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {'plays': 0, 'tokens': 0, 'purchased_games': [], 'settings': {'colors_enabled': True}}

def save_game_data(data):
    """Save game statistics to JSON file"""
    with open('game_data.json', 'w') as f:
        json.dump(data, f)

def color_text(text, color):
    """Apply color to text if colors are enabled"""
    data = load_game_data()
    if data['settings']['colors_enabled']:
        return color + text + Style.RESET_ALL
    return text

# Core functions
def display_banner():
    """Display the ChronoTale banner with pixel font"""
    banner = r"""
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░                    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░                      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░                    ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
"""
    print(color_text(banner, Fore.YELLOW) + color_text("A Multidimensional Adventure Launcher", Fore.CYAN))
    print("\n" + "═" * 50 + "\n")

def check_file(file_name):
    """Check if a game file exists"""
    if not os.path.isfile(file_name):
        print(color_text(f"█ Error: {file_name} not found!", Fore.RED))
        return False
    return True

def launch_game(file_name):
    """Launch the specified game file"""
    try:
        game_name = os.path.splitext(os.path.basename(file_name))[0]
        print(color_text(f"\n█ Launching {game_name}...", Fore.GREEN) + Style.RESET_ALL)

        # Pixel-style loading animation
        frames = ["[■□□□]", "[■■□□]", "[■■■□]", "[■■■■]"]
        for frame in frames:
            print(color_text(f"█ Loading {frame}", Fore.BLUE), end='\r')
            time.sleep(0.2)
        
        # Set environment variable to indicate the game was launched from launcher
        os.environ["LAUNCHED_FROM_LAUNCHER"] = "1"
        
        # Run the game
        subprocess.run([sys.executable, file_name], check=True)
        
        # Clear the environment variable when game exits
        if "LAUNCHED_FROM_LAUNCHER" in os.environ:
            del os.environ["LAUNCHED_FROM_LAUNCHER"]
    except subprocess.CalledProcessError as e:
        print(color_text(f"█ Crash: Game exited with error {e.returncode}", Fore.RED))
    except Exception as e:
        print(color_text(f"█ Crash: {e}", Fore.RED))

# Menu system
def games_menu(data):
    """Display games submenu"""
    original_games = [
        ("Legacies of our Legends RPG", "Legacies.py"),
        ("Liminal", "Liminal.py"),
        ("Last Human: Exodus", "Exodus.py"),
        ("Z_survival", "Z_survival.py"),
        ("My first day here: Campus Life", "school.py")
    ]
    purchased_games = [tuple(game) for game in data['purchased_games']]
    all_games = original_games + purchased_games

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(color_text(f"█ Total Plays: {data['plays']} | Tokens: {data['tokens']}", Fore.CYAN))
        print("\n" + "═" * 50 + "\n")
        print(color_text("█ Available Games:\n", Fore.MAGENTA))

        # Display games with numbering
        for idx, (name, file) in enumerate(all_games, 1):
            print(color_text(f"█ [{idx}] {name}", Fore.CYAN))

        back_number = len(all_games) + 1
        print(color_text(f"█ [{back_number}] Back to Main Menu", Fore.RED))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

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

                    input(color_text("\n█ Press Enter to continue...", Fore.YELLOW) + Style.RESET_ALL)
            elif choice_int == back_number:
                return
            else:
                print(color_text("\n█ Invalid input!", Fore.RED))
                time.sleep(1)
        except ValueError:
            print(color_text("\n█ Invalid input!", Fore.RED))
            time.sleep(1)

def shop_menu(data):
    """Display token shop"""
    purchasable_games = [
        {"name": "Shipwrecked", "file": "shipwrecked.py", "cost": 30},
        {"name": "Carnival", "file": "Carnival.py", "cost": 30},
        {"name": "World Of Monsters", "file": "WOM.py", "cost": 30},
        {"name": "Hacker: Digital Hijacker", "file": "hacker.py", "cost": 40}
    ]

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(color_text("█ Welcome to the Token Shop!", Fore.CYAN))
        print(color_text("█ Available Items:\n", Fore.YELLOW))

        # Display purchasable games
        for idx, game in enumerate(purchasable_games, 1):
            purchased = any(g[0] == game["name"] and g[1] == game["file"] for g in data['purchased_games'])
            status = color_text("Purchased", Fore.GREEN) if purchased else color_text(f"Cost: {game['cost']} Tokens", Fore.YELLOW)
            print(color_text(f"█ [{idx}] {game['name']} - {status}", Fore.CYAN))

        print(color_text(f"█ [{len(purchasable_games)+1}] Back to Main Menu", Fore.RED))
        print(color_text(f"\n█ Your current balance: {data['tokens']} Tokens", Fore.CYAN))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(purchasable_games):
                selected_game = purchasable_games[choice_int - 1]
                # Check if already purchased
                if any(g[0] == selected_game["name"] and g[1] == selected_game["file"] for g in data['purchased_games']):
                    print(color_text("█ You already own this game!", Fore.RED))
                    time.sleep(1)
                    continue
                # Check tokens
                if data['tokens'] >= selected_game["cost"]:
                    data['tokens'] -= selected_game["cost"]
                    data['purchased_games'].append([selected_game["name"], selected_game["file"]])
                    save_game_data(data)
                    print(color_text(f"█ Purchased {selected_game['name']}!", Fore.GREEN))
                    time.sleep(1)
                else:
                    print(color_text("█ Insufficient tokens!", Fore.RED))
                    time.sleep(1)
            elif choice_int == len(purchasable_games) + 1:
                return
            else:
                print(color_text("█ Invalid input!", Fore.RED))
                time.sleep(1)
        except ValueError:
            print(color_text("█ Invalid input!", Fore.RED))
            time.sleep(1)

def credits_menu():
    """Display credits"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(color_text("█ Credits:", Fore.CYAN))
    print(color_text("█ Developed by andy64lol", Fore.GREEN))
    print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))
    input(color_text("\n█ Press Enter to return to main menu...", Fore.YELLOW) + Style.RESET_ALL)

def settings_menu(data):
    """Display settings"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(color_text("█ Settings:", Fore.CYAN))
        print(color_text(f"█ [1] Toggle Colors: {'ON' if data['settings']['colors_enabled'] else 'OFF'}", Fore.CYAN))
        print(color_text("█ [2] Back to Main Menu", Fore.RED))
        print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

        if choice == '1':
            data['settings']['colors_enabled'] = not data['settings']['colors_enabled']
            save_game_data(data)
            print(color_text(f"█ Colors {'enabled' if data['settings']['colors_enabled'] else 'disabled'}!", Fore.GREEN))
            time.sleep(1)
        elif choice == '2':
            return
        else:
            print(color_text("█ Invalid input!", Fore.RED))
            time.sleep(1)

def main_menu():
    """Main menu controller"""
    data = load_game_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(color_text(f"█ Total Plays: {data['plays']} | Tokens: {data['tokens']}", Fore.CYAN))
        print("\n" + "═" * 50 + "\n")
        print(color_text("█ Main Menu:\n", Fore.MAGENTA))
        print(color_text("█ [1] Games", Fore.CYAN))
        print(color_text("█ [2] Shop", Fore.CYAN))
        print(color_text("█ [3] Credits", Fore.CYAN))
        print(color_text("█ [4] Settings", Fore.CYAN))
        print(color_text("█ [5] Quit", Fore.RED))
        print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

        if choice == '1':
            games_menu(data)
        elif choice == '2':
            shop_menu(data)
        elif choice == '3':
            credits_menu()
        elif choice == '4':
            settings_menu(data)
        elif choice == '5':
            print(color_text("\n█ Closing...", Fore.YELLOW))
            time.sleep(1)
            break
        else:
            print(color_text("\n█ Invalid input!", Fore.RED))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(color_text("\n█ Force quit!", Fore.YELLOW))
        sys.exit(0)
