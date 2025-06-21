import os
from typing import Dict, List, Any, Optional, Union
import subprocess
import sys
import time
import json
import datetime
import random
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
VERSION = "2.1.0"
LAUNCHER_NAME = "ChronoTale Launcher"

# UI Enhancement constants
BORDER_CHARS = {
    'horizontal': '═',
    'vertical': '║',
    'top_left': '╔',
    'top_right': '╗',
    'bottom_left': '╚',
    'bottom_right': '╝',
    'cross': '╬',
    'top_tee': '╦',
    'bottom_tee': '╩',
    'left_tee': '╠',
    'right_tee': '╣'
}

STATUS_ICONS = {
    'available': '●',
    'purchased': '✓',
    'locked': '🔒',
    'new': '✨',
    'popular': '🔥',
    'featured': '⭐'
}

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

def create_box(content: str, width: int = 80, title: str = "") -> str:
    """Create a properly aligned bordered box for content"""
    lines = content.split('\n')
    box = []
    
    # Calculate exact content width (total width minus 2 border chars minus 2 padding spaces)
    content_width = width - 4
    
    # Top border with title
    if title:
        title_padded = f" {title} "
        # Use simple length for title positioning
        title_len = len(title_padded)
        
        if title_len >= width - 2:
            # Title too long, truncate
            title_padded = f" {title[:width-8]}... "
            title_len = len(title_padded)
        
        title_start = (width - 2 - title_len) // 2
        remaining_chars = width - 2 - title_start - title_len
        
        top_line = (BORDER_CHARS['top_left'] + 
                   BORDER_CHARS['horizontal'] * title_start +
                   title_padded +
                   BORDER_CHARS['horizontal'] * remaining_chars +
                   BORDER_CHARS['top_right'])
    else:
        top_line = (BORDER_CHARS['top_left'] + 
                   BORDER_CHARS['horizontal'] * (width - 2) + 
                   BORDER_CHARS['top_right'])
    
    box.append(top_line)
    
    # Process content lines
    for line in lines:
        if line.strip() == "":
            # Empty line
            padded_line = f"{BORDER_CHARS['vertical']}{' ' * (width-2)}{BORDER_CHARS['vertical']}"
        else:
            # Simple truncation based on character count, not display width
            if len(line) > content_width:
                line = line[:content_width-3] + "..."
            
            # Simple padding - let terminal handle Unicode display
            spaces_needed = content_width - len(line)
            if spaces_needed < 0:
                spaces_needed = 0
            
            padded_content = line + (' ' * spaces_needed)
            padded_line = f"{BORDER_CHARS['vertical']} {padded_content} {BORDER_CHARS['vertical']}"
        
        box.append(padded_line)
    
    # Bottom border
    bottom_line = (BORDER_CHARS['bottom_left'] + 
                  BORDER_CHARS['horizontal'] * (width - 2) + 
                  BORDER_CHARS['bottom_right'])
    box.append(bottom_line)
    
    return '\n'.join(box)

def animate_loading(text: str, duration: float = 1.0) -> None:
    """Enhanced loading animation with progress bar"""
    frames = ["▱▱▱▱▱", "▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰"]
    frame_time = duration / len(frames)
    
    for frame in frames:
        print(color_text(f"█ {text} {frame}", Fore.CYAN), end='\r')
        time.sleep(frame_time)
    print()

def get_time_greeting() -> str:
    """Get time-based greeting"""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 22:
        return "Good Evening"
    else:
        return "Good Night"

def get_random_tip() -> str:
    """Get a random tip for the user"""
    tips = [
        "💡 Tip: Play games longer to earn more tokens!",
        "💡 Tip: Check achievements for bonus tokens!",
        "💡 Tip: Some games have seasonal content!",
        "💡 Tip: Your playtime is tracked across all sessions!",
        "💡 Tip: Purchase games to expand your collection!",
        "💡 Tip: Settings can be customized to your preference!"
    ]
    return random.choice(tips)

def create_terminal_shortcut() -> str:
    """Create a terminal shortcut script for ChronoTale launcher"""
    script_content = '''#!/bin/bash

# ChronoTale Launcher Terminal Shortcut
# This script automatically navigates to ChronoTale directory, activates venv, and runs the launcher

# Store the current directory to return to later
ORIGINAL_DIR=$(pwd)

# Function to handle cleanup on exit
cleanup() {
    echo "Cleaning up..."
    cd "$ORIGINAL_DIR"
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        deactivate 2>/dev/null
    fi
    echo "Returned to original directory and deactivated virtual environment."
}

# Set trap to call cleanup function on script exit
trap cleanup EXIT

# Navigate to ChronoTale directory
if [[ -d "ChronoTale" ]]; then
    cd ChronoTale
    echo "Navigated to ChronoTale directory"
elif [[ -d "../ChronoTale" ]]; then
    cd ../ChronoTale
    echo "Navigated to ChronoTale directory"
else
    echo "ChronoTale directory not found. Please run this script from the project root or ChronoTale directory."
    exit 1
fi

# Check if virtual environment exists and activate it
if [[ -d "venv" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment activated"
elif [[ -d "../venv" ]]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Virtual environment not found. Running without venv."
fi

# Run the ChronoTale launcher
echo "Starting ChronoTale Launcher..."
python launch.py

# Cleanup will be handled automatically by the trap
'''
    return script_content

def auto_install_shortcut():
    """Automatically install the terminal shortcut using the installer script"""
    try:
        import subprocess
        result = subprocess.run(['python3', 'install_shortcut.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(color_text("✅ Terminal shortcut installed successfully!", Fore.GREEN))
            print(color_text(result.stdout, Fore.WHITE))
            return True
        else:
            print(color_text("❌ Installation failed:", Fore.RED))
            print(color_text(result.stderr, Fore.RED))
            return False
    except Exception as e:
        print(color_text(f"❌ Error during installation: {e}", Fore.RED))
        return False

def generate_shell_command_instructions() -> str:
    """Generate instructions for setting up the terminal shortcut"""
    instructions = """Automatic Terminal Shortcut Installation:

The installer will:
🔹 Create the 'chronotale' command script
🔹 Install it to ~/.local/bin/chronotale
🔹 Update your shell profile (bashrc/zshrc) 
🔹 Make it executable automatically
🔹 Test the installation

After installation, use:
$ chronotale

Features:
• Automatically navigates to ChronoTale directory
• Activates virtual environment if present
• Runs the launcher with full cleanup
• Returns to original directory on exit"""
    
    return instructions

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
    print(color_text("                    ⚡ NEXT-GENERATION ADVENTURE LAUNCHER ⚡", Fore.CYAN))
    print(color_text(f"                              Version {VERSION}", Fore.MAGENTA))
    
    # Enhanced status bar
    data = load_game_data()
    greeting = get_time_greeting()
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    status_bar = f"{greeting} • {current_time} • ChronoTale Universe"
    print(color_text(f"                    {status_bar}", Fore.WHITE))
    print("\n" + color_text("═" * 80, Fore.BLUE) + "\n")

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
        print(color_text(f"\n🚀 Initializing {game_name}...", Fore.GREEN))

        # Enhanced loading animation with progress
        animate_loading(f"Loading {game_name}", 1.5)

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
    """Enhanced games library with detailed information"""
    original_games = [
        ("Legacies of our Legends RPG", "Legacies.py", "⚔️", "Epic fantasy RPG adventure"),
        ("Liminal", "Liminal.py", "🌆", "Atmospheric exploration game"),
        ("Last Human: Exodus", "Exodus.py", "🚀", "Sci-fi survival epic"),
        ("Z_survival", "Z_survival.py", "🧟", "Zombie apocalypse survival"),
        ("My first day here: Campus Life", "school.py", "🎓", "School life simulator")
    ]
    
    purchased_games = []
    for game in data['purchased_games']:
        if game[0] == "Shipwrecked":
            purchased_games.append((game[0], game[1], "🏝️", "Island survival adventure"))
        elif game[0] == "Carnival":
            purchased_games.append((game[0], game[1], "🎡", "Carnival minigame collection"))
        elif game[0] == "World Of Monsters":
            purchased_games.append((game[0], game[1], "👹", "Monster collection RPG"))
        elif game[0] == "My Last Days Here: Farewell":
            purchased_games.append((game[0], game[1], "💔", "Emotional narrative journey"))
        elif game[0] == "Hacker: Digital Hijacker":
            purchased_games.append((game[0], game[1], "💻", "Cyberpunk hacking simulator"))
        elif game[0] == "4ndyBurger Tycoon":
            purchased_games.append((game[0], game[1], "🍔", "Restaurant management game"))
        elif game[0] == "Deutschland: 1936":
            purchased_games.append((game[0], game[1], "🏛️", "Historical strategy game"))
        else:
            purchased_games.append((game[0], game[1], "🎮", "Adventure game"))
    
    all_games = original_games + purchased_games

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Game library header
        library_info = f"Total Games: {len(all_games)} | Sessions Played: {data['plays']} | Tokens Available: {data['tokens']}"
        print(color_text(f"█ GAMES LIBRARY: {library_info}", Fore.CYAN))
        print("\n" + "═" * 80 + "\n")

        # Display games in enhanced format
        for idx, (name, file, icon, desc) in enumerate(all_games, 1):
            # Get game statistics if available
            game_stats = data['game_statistics'].get(os.path.splitext(os.path.basename(file))[0], {})
            launches = game_stats.get('launches', 0)
            total_time = game_stats.get('total_time', 0)
            
            status_info = ""
            if launches > 0:
                playtime = format_time(total_time)
                status_info = f"({launches} sessions, {playtime})"
            else:
                status_info = "(Never played)"
            
            print(color_text(f"█ {icon} [{idx}] {name} - {desc}", Fore.WHITE))
            print(color_text(f"     {status_info}", Fore.YELLOW))

        print(color_text(f"\n█ 🔙 [{len(all_games) + 1}] Return to Main Menu", Fore.RED))
        
        choice = input(color_text("\n🎮 Choose your adventure (1-{}): ".format(len(all_games) + 1), Fore.MAGENTA) + Style.RESET_ALL)

        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(all_games):
                selected_game = all_games[choice_int - 1]
                game_name, game_file, icon, desc = selected_game
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
            elif choice_int == len(all_games) + 1:
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
        {"name": "Deutschland: 1936", "file": "deutschland.py", "cost": 40},
        {"name": "Mexican Gangsters!", "file": "mexican_gangsters.py", "cost": 50}
    ]

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Shop header with balance
        shop_info = f"Token Balance: {data['tokens']} | Available Games: {len([g for g in purchasable_games if not any(pg[0] == g['name'] for pg in data['purchased_games'])])}"
        print(color_text(f"█ TOKEN SHOP: {shop_info}", Fore.CYAN))
        print("\n" + "═" * 80 + "\n")

        # Display purchasable games in enhanced format
        for idx, game in enumerate(purchasable_games, 1):
            purchased = any(g[0] == game["name"] and g[1] == game["file"] for g in data['purchased_games'])
            
            if purchased:
                status = "✓ OWNED"
                print(color_text(f"█ 🎮 [{idx}] {game['name']:<30} - {status}", Fore.GREEN))
            else:
                status = f"{game['cost']} Tokens"
                icon = "🛒" if data['tokens'] >= game['cost'] else "🔒"
                print(color_text(f"█ {icon} [{idx}] {game['name']:<30} - {status}", Fore.WHITE))

        print(color_text(f"\n█ 🔙 [{len(purchasable_games)+1}] Return to Main Menu", Fore.RED))
        
        choice = input(color_text("\n🛒 Enter your choice (1-{}): ".format(len(purchasable_games)+1), Fore.MAGENTA) + Style.RESET_ALL)

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
    """Display credits with enhanced UI"""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    
    print(color_text("█ CHRONOTALE CREDITS:", Fore.CYAN))
    print("\n" + "═" * 80 + "\n")
    print(color_text("█ Development Team:", Fore.MAGENTA))
    print(color_text("█ 👨‍💻 Lead Developer: andy64lol", Fore.GREEN))
    print(color_text("█ 🎨 UI Design: ChronoTale Team", Fore.GREEN))
    print(color_text("█ 🎮 Game Collection: Community Contributors", Fore.GREEN))
    print()
    print(color_text("█ Framework Information:", Fore.MAGENTA))
    print(color_text("█ 🐍 Python Runtime with Colorama", Fore.WHITE))
    print(color_text(f"█ 🎯 Version: {VERSION}", Fore.WHITE))
    print(color_text("█ 📅 Build Date: 2025", Fore.WHITE))
    print()
    print(color_text("█ Special Thanks:", Fore.MAGENTA))
    print(color_text("█ 🌟 Beta Testers and Community", Fore.WHITE))
    print(color_text("█ 🚀 Replit Platform Support", Fore.WHITE))
    input(color_text("\n🔙 Press Enter to return to main menu...", Fore.YELLOW) + Style.RESET_ALL)

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
    """Display settings with enhanced UI"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Settings header
        settings_info = f"Current Configuration | Version: {VERSION}"
        print(color_text(f"█ LAUNCHER SETTINGS: {settings_info}", Fore.CYAN))
        print("\n" + "═" * 80 + "\n")
        
        # Settings options
        color_status = "✓ ENABLED" if data['settings']['colors_enabled'] else "✗ DISABLED"
        
        print(color_text(f"█ ⚙️ [1] Color Theme: {color_status}", Fore.WHITE))
        print(color_text("     Toggle colorful text display throughout the launcher", Fore.YELLOW))
        print()
        print(color_text("█ 📜 [2] Complete Automated Setup", Fore.WHITE))
        print(color_text("     Full automation: dependencies, global command, PATH configuration", Fore.YELLOW))
        print()
        print(color_text("█ 🔙 [3] Return to Main Menu", Fore.RED))
        print(color_text("     Save settings and return to the main menu", Fore.YELLOW))

        choice = input(color_text("\n⚙️ Select setting to modify (1-3): ", Fore.MAGENTA) + Style.RESET_ALL)

        if choice == '1':
            data['settings']['colors_enabled'] = not data['settings']['colors_enabled']
            save_game_data(data)
            status = "enabled" if data['settings']['colors_enabled'] else "disabled"
            print(color_text(f"\n✓ Color theme {status} successfully!", Fore.GREEN))
            time.sleep(1.5)
        elif choice == '2':
            # Complete automated setup
            os.system('cls' if os.name == 'nt' else 'clear')
            display_banner()
            
            print(color_text("█ COMPLETE AUTOMATED SETUP:", Fore.CYAN))
            print("\n" + "═" * 80 + "\n")
            print(color_text("This will automatically:", Fore.WHITE))
            print(color_text("• Install dependencies", Fore.WHITE))
            print(color_text("• Create global chronotale command", Fore.WHITE))
            print(color_text("• Update PATH environment", Fore.WHITE))
            print(color_text("• Configure shell profiles", Fore.WHITE))
            print(color_text("• Make command immediately available", Fore.WHITE))
            
            install = input(color_text("\nRun complete automated setup? (y/n): ", Fore.YELLOW) + Style.RESET_ALL)
            
            if install.lower() in ['y', 'yes']:
                print(color_text("\nStarting complete automation...", Fore.CYAN))
                try:
                    import subprocess
                    result = subprocess.run([sys.executable, 'setup.py'], 
                                          capture_output=True, text=True, cwd=os.getcwd())
                    
                    if result.returncode == 0:
                        print(color_text("Setup completed successfully!", Fore.GREEN))
                        print(color_text(result.stdout, Fore.WHITE))
                        
                        # Update current process PATH
                        import pathlib
                        local_bin = pathlib.Path.home() / ".local" / "bin"
                        current_path = os.environ.get('PATH', '')
                        os.environ['PATH'] = f"{local_bin}:{current_path}"
                        
                        print(color_text("chronotale command is now available in this session!", Fore.GREEN))
                    else:
                        print(color_text("Setup encountered issues:", Fore.RED))
                        print(color_text(result.stderr, Fore.RED))
                except Exception as e:
                    print(color_text(f"Setup error: {e}", Fore.RED))
            else:
                print(color_text("Setup cancelled.", Fore.YELLOW))
            
            input(color_text("\nPress Enter to return to settings...", Fore.YELLOW) + Style.RESET_ALL)
        elif choice == '3':
            return
        else:
            print(color_text("\n❌ Invalid selection!", Fore.RED))
            time.sleep(1)

def main_menu() -> None:
    """Enhanced main menu controller with modern UI"""
    data = load_game_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Enhanced status display
        status_content = f"Total Sessions: {data['plays']} | Tokens Earned: {data['tokens']} | Games Owned: {len(data['purchased_games']) + 5}"
        if data['last_played']:
            status_content += f" | Last Played: {data['last_played']}"
        
        print(color_text(f"█ PLAYER STATUS: {status_content}", Fore.CYAN))
        print("\n" + "═" * 80 + "\n")
        
        # Enhanced main menu with icons and descriptions
        print(color_text("█ MAIN MENU:", Fore.MAGENTA))
        print(color_text("█ 🎮 [1] Games Library           - Browse and launch your game collection", Fore.WHITE))
        print(color_text("█ 🛒 [2] Token Shop              - Purchase new games with earned tokens", Fore.WHITE))
        print(color_text("█ 📊 [3] Statistics & Achievements - View your gaming progress and unlocks", Fore.WHITE))
        print(color_text("█ 👨‍💻 [4] Credits                 - Meet the development team", Fore.WHITE))
        print(color_text("█ ⚙️  [5] Settings               - Customize your launcher experience", Fore.WHITE))
        print(color_text("█ ❌ [6] Exit Launcher           - Close the ChronoTale launcher", Fore.WHITE))
        
        # Random tip display
        tip = get_random_tip()
        print(color_text(f"\n█ DAILY TIP: {tip}", Fore.YELLOW))
        
        choice = input(color_text("\n🎯 Enter your choice (1-6): ", Fore.MAGENTA) + Style.RESET_ALL)

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
            print(color_text("\n🔄 Shutting down ChronoTale Launcher...", Fore.YELLOW))
            time.sleep(1)
            # Clear terminal completely
            os.system('cls' if os.name == 'nt' else 'clear')
            print(color_text("Thank you for using ChronoTale Universe Launcher!", Fore.CYAN))
            print(color_text("Adventure awaits your return...", Fore.MAGENTA))
            time.sleep(1.5)
            # Final clear
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print(color_text("\n█ Invalid input!", Fore.RED))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(color_text("\n\n🔄 Force quit detected...", Fore.YELLOW))
        time.sleep(0.5)
        # Clear terminal completely
        os.system('cls' if os.name == 'nt' else 'clear')
        print(color_text("ChronoTale Launcher terminated by user.", Fore.CYAN))
        time.sleep(1)
        # Final clear
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit(0)
