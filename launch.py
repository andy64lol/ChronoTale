import os
from typing import Dict, List, Any, Optional, Union
import subprocess
import sys
import time
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "2.0.0"

# Game data persistence
def load_game_data() -> Any:
    """Load game statistics from JSON file"""
    try:
        with open('game_data.json', 'r') as f:
            data = json.load(f)
            if 'purchased_games' not in data:
                data['purchased_games'] = []
            if 'settings' not in data:
                data['settings'] = {'colors_enabled': True, 'auto_save': True}
            if 'game_statistics' not in data:
                data['game_statistics'] = {}
            if 'achievements' not in data:
                data['achievements'] = []
            if 'last_played' not in data:
                data['last_played'] = None
            if 'total_playtime' not in data:
                data['total_playtime'] = 0
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'plays': 0, 
            'tokens': 0, 
            'purchased_games': [], 
            'settings': {'colors_enabled': True, 'auto_save': True},
            'game_statistics': {},
            'achievements': [],
            'last_played': None,
            'total_playtime': 0
        }

def save_game_data(data: Any) -> Any:
    """Save game statistics to JSON file"""
    with open('game_data.json', 'w') as f:
        json.dump(data, f)

def color_text(text: Any, color: Any) -> Any:
    """Apply color to text if colors are enabled"""
    data = load_game_data()
    if data['settings']['colors_enabled']:
        return color + text + Style.RESET_ALL
    return text

# Core functions
def display_banner() -> None:
    """Display the enhanced ChronoTale banner with version info"""
    banner = r"""
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░                    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░                      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓██▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░                    ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 

"""
    print(color_text(banner, Fore.YELLOW))
    print(color_text("                    ⚡ MULTIDIMENSIONAL ADVENTURE LAUNCHER ⚡", Fore.CYAN))
    print(color_text(f"                              Version {VERSION}", Fore.MAGENTA))
    print("\n" + "═" * 80 + "\n")

def check_file(file_name: Any) -> bool:
    """Check if a game file exists"""
    if not os.path.isfile(file_name):
        print(color_text(f"█ Error: {file_name} not found!", Fore.RED))
        return False
    return True

def launch_game(file_name: Any, data: Any) -> Any:
    """Launch the specified game file with enhanced tracking"""
    try:
        game_name = os.path.splitext(os.path.basename(file_name))[0]
        print(color_text(f"\n█ Launching {game_name}...", Fore.GREEN) + Style.RESET_ALL)

        # Enhanced loading animation
        frames = ["[■□□□]", "[■■□□]", "[■■■□]", "[■■■■]"]
        for frame in frames:
            print(color_text(f"█ Loading {frame}", Fore.BLUE), end='\r')
            time.sleep(0.2)
        
        # Track game statistics
        if game_name not in data['game_statistics']:
            data['game_statistics'][game_name] = {'launches': 0, 'total_time': 0, 'last_played': None}
        
        data['game_statistics'][game_name]['launches'] += 1
        data['game_statistics'][game_name]['last_played'] = time.time()
        data['last_played'] = game_name
        
        # Set environment variable to indicate the game was launched from launcher
        os.environ["LAUNCHED_FROM_LAUNCHER"] = "1"
        
        # Track launch time
        start_time = time.time()
        
        # Run the game
        subprocess.run([sys.executable, file_name], check=True)
        
        # Calculate session time
        end_time = time.time()
        session_time = end_time - start_time
        data['game_statistics'][game_name]['total_time'] += session_time
        data['total_playtime'] += session_time
        
        # Award achievements for playtime
        check_playtime_achievements(data, game_name, session_time)
        
        # Clear the environment variable when game exits
        if "LAUNCHED_FROM_LAUNCHER" in os.environ:
            del os.environ["LAUNCHED_FROM_LAUNCHER"]
            
        return session_time
        
    except subprocess.CalledProcessError as e:
        print(color_text(f"█ Crash: Game exited with error {e.returncode}", Fore.RED))
        return 0
    except Exception as e:
        print(color_text(f"█ Crash: {e}", Fore.RED))
        return 0

def check_playtime_achievements(data: Any, game_name: str, session_time: float) -> None:
    """Check and award achievements based on playtime"""
    achievements = []
    
    # Session-based achievements
    if session_time >= 300:  # 5 minutes
        achievements.append("Dedicated Player")
    if session_time >= 1800:  # 30 minutes
        achievements.append("Marathon Gamer")
    if session_time >= 3600:  # 1 hour
        achievements.append("Epic Session")
    
    # Total playtime achievements
    total_time = data['total_playtime']
    if total_time >= 3600 and "Gaming Enthusiast" not in data['achievements']:
        achievements.append("Gaming Enthusiast")
    if total_time >= 18000 and "ChronoTale Master" not in data['achievements']:
        achievements.append("ChronoTale Master")
    
    # Game-specific achievements
    game_stats = data['game_statistics'].get(game_name, {})
    if game_stats.get('launches', 0) >= 5 and f"{game_name} Veteran" not in data['achievements']:
        achievements.append(f"{game_name} Veteran")
    
    # Collection achievements
    if len(data['purchased_games']) >= 3 and "Collector" not in data['achievements']:
        achievements.append("Collector")
    
    # Award new achievements
    for achievement in achievements:
        if achievement not in data['achievements']:
            data['achievements'].append(achievement)
            print(color_text(f"\n🏆 Achievement Unlocked: {achievement}!", Fore.YELLOW))
            data['tokens'] += 5  # Bonus tokens for achievements

def format_time(seconds: float) -> str:
    """Format time in a human-readable format"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

# Menu system
def games_menu(data: Any) -> Any:
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
                    session_time = launch_game(game_file, data)

                    # Calculate playtime tokens
                    elapsed_minutes = session_time // 60
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

def shop_menu(data: Any) -> Any:
    """Display token shop"""
    purchasable_games = [
        {"name": "Shipwrecked", "file": "shipwrecked.py", "cost": 30},
        {"name": "Carnival", "file": "Carnival.py", "cost": 30},
        {"name": "World Of Monsters", "file": "WOM.py", "cost": 30},
        {"name": "My Last Days Here: Farewell", "file": "My_last_days_here.py", "cost": 35},
        {"name": "Hacker: Digital Hijacker", "file": "hacker.py", "cost": 40},
        {"name": "4ndyBurger Tycoon", "file": "burger.py", "cost": 40},
        {"name": "Deutschland: 1936", "file": "deutschland.py", "cost": 40}
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

def credits_menu() -> None:
    """Display credits"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    print(color_text("█ Credits:", Fore.CYAN))
    print(color_text("█ Developed by andy64lol", Fore.GREEN))
    print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))
    input(color_text("\n█ Press Enter to return to main menu...", Fore.YELLOW) + Style.RESET_ALL)

def statistics_menu(data: Any) -> Any:
    """Display comprehensive statistics and achievements"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        print(color_text("█ CHRONOTALE STATISTICS & ACHIEVEMENTS", Fore.MAGENTA))
        print("\n" + "═" * 80 + "\n")
        
        # Overall Statistics
        print(color_text("📊 OVERALL STATISTICS", Fore.CYAN))
        print(color_text(f"Total Games Launched: {data['plays']}", Fore.WHITE))
        print(color_text(f"Total Playtime: {format_time(data['total_playtime'])}", Fore.WHITE))
        print(color_text(f"Tokens Earned: {data['tokens']}", Fore.WHITE))
        print(color_text(f"Games Owned: {len(data['purchased_games']) + 5}", Fore.WHITE))  # 5 base games
        if data['last_played']:
            print(color_text(f"Last Played: {data['last_played']}", Fore.WHITE))
        
        # Game Statistics
        print(color_text("\n🎮 GAME STATISTICS", Fore.CYAN))
        if data['game_statistics']:
            for game_name, stats in data['game_statistics'].items():
                playtime = format_time(stats['total_time'])
                launches = stats['launches']
                print(color_text(f"  {game_name}: {launches} launches, {playtime} played", Fore.WHITE))
        else:
            print(color_text("  No game statistics yet - start playing to see data!", Fore.YELLOW))
        
        # Achievements
        print(color_text("\n🏆 ACHIEVEMENTS", Fore.CYAN))
        if data['achievements']:
            for achievement in data['achievements']:
                print(color_text(f"  ✓ {achievement}", Fore.GREEN))
        else:
            print(color_text("  No achievements unlocked yet - keep playing!", Fore.YELLOW))
        
        # Achievement Progress Hints
        print(color_text("\n💡 ACHIEVEMENT HINTS", Fore.CYAN))
        hints = []
        if data['total_playtime'] < 3600:
            hints.append("Play for 1 hour total to become a Gaming Enthusiast")
        if len(data['purchased_games']) < 3:
            hints.append("Buy 3 games to become a Collector")
        if not any("Veteran" in achievement for achievement in data['achievements']):
            hints.append("Launch any game 5 times to become a Veteran")
        
        for hint in hints[:3]:  # Show max 3 hints
            print(color_text(f"  • {hint}", Fore.YELLOW))
        
        print(color_text("\n█ [1] Back to Main Menu", Fore.RED))
        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)
        
        if choice == '1':
            return
        else:
            print(color_text("█ Invalid input!", Fore.RED))
            time.sleep(1)

def settings_menu(data: Any) -> Any:
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

def main_menu() -> None:
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
        print(color_text("█ [3] Statistics & Achievements", Fore.CYAN))
        print(color_text("█ [4] Credits", Fore.CYAN))
        print(color_text("█ [5] Settings", Fore.CYAN))
        print(color_text("█ [6] Quit", Fore.RED))
        print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

        if choice == '1':
            games_menu(data)
        elif choice == '2':
            shop_menu(data)
        elif choice == '3':
            statistics_menu(data)
        elif choice == '4':
            credits_menu()
        elif choice == '5':
            settings_menu(data)
        elif choice == '6':
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
