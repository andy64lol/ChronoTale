import os
from typing import Dict, List, Any, Optional, Union
import subprocess
import sys
import time
import json
import shutil
import platform
from pathlib import Path
from colorama import init, Fore, Style
import locale

# Set UTF-8 encoding for better compatibility
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LC_ALL'] = 'C.UTF-8'
os.environ['LANG'] = 'C.UTF-8'

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

def detect_virtual_env() -> Optional[str]:
    """Detect if running in a virtual environment and return the activation command"""
    if os.environ.get('VIRTUAL_ENV'):
        venv_path = os.environ.get('VIRTUAL_ENV')
        return venv_path
    
    # Check for common venv directories
    possible_venvs = ['.venv', 'venv', 'env', '.env']
    current_dir = os.getcwd()
    
    for venv_name in possible_venvs:
        venv_path = os.path.join(current_dir, venv_name)
        if os.path.exists(venv_path) and os.path.exists(os.path.join(venv_path, 'bin', 'activate')):
            return venv_path
    
    return None

def detect_desktop_environment() -> str:
    """Detect the desktop environment and return appropriate terminal command"""
    # Check environment variables for desktop environment
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    session_desktop = os.environ.get('DESKTOP_SESSION', '').lower()
    
    # Detect Crostini (Chrome OS Linux container)
    if os.path.exists('/opt/google/cros-containers'):
        return 'crostini'
    
    # Common desktop environments
    if 'gnome' in desktop_env or 'gnome' in session_desktop:
        return 'gnome'
    elif 'kde' in desktop_env or 'plasma' in desktop_env:
        return 'kde'
    elif 'xfce' in desktop_env:
        return 'xfce'
    elif 'lxde' in desktop_env or 'lxqt' in desktop_env:
        return 'lxde'
    elif 'mate' in desktop_env:
        return 'mate'
    elif 'cinnamon' in desktop_env:
        return 'cinnamon'
    
    return 'generic'

def get_terminal_command(desktop_env: str) -> str:
    """Get the appropriate terminal command for the desktop environment"""
    terminal_commands = {
        'crostini': 'x-terminal-emulator',
        'gnome': 'gnome-terminal',
        'kde': 'konsole',
        'xfce': 'xfce4-terminal',
        'lxde': 'lxterminal',
        'mate': 'mate-terminal',
        'cinnamon': 'gnome-terminal',
        'generic': 'x-terminal-emulator'
    }
    
    terminal_cmd = terminal_commands.get(desktop_env, 'x-terminal-emulator')
    
    # Check if the terminal exists, fallback to alternatives
    fallback_terminals = [
        'x-terminal-emulator',
        'gnome-terminal',
        'konsole',
        'xfce4-terminal',
        'lxterminal',
        'mate-terminal',
        'xterm',
        'terminator',
        'tilix'
    ]
    
    for term in [terminal_cmd] + fallback_terminals:
        if shutil.which(term):
            return term
    
    return 'xterm'  # Last resort

def create_desktop_shortcut() -> bool:
    """Create a desktop shortcut for ChronoTale launcher with improved Linux compatibility"""
    try:
        # Get the directory where launch.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        launcher_path = os.path.join(script_dir, 'launch.py')
        
        if not os.path.exists(launcher_path):
            print(color_text("█ Error: launch.py not found!", Fore.RED))
            return False
        
        # Get user's desktop directory
        home_dir = Path.home()
        
        # Try multiple common desktop directory names (including Crostini variations)
        possible_desktop_dirs = [
            home_dir / "Desktop",
            home_dir / "desktop", 
            home_dir / "Bureau",  # French
            home_dir / "Escritorio",  # Spanish
            home_dir / "デスクトップ",  # Japanese
            home_dir / "桌面",  # Chinese
            home_dir / ".local" / "share" / "applications"  # Applications directory
        ]
        
        desktop_dir = None
        shortcut_name = "ChronoTale.desktop"
        
        for dir_path in possible_desktop_dirs:
            if dir_path.exists():
                desktop_dir = dir_path
                break
        
        # If no desktop directory found, create applications directory or use home
        if desktop_dir is None:
            # Try to create applications directory
            apps_dir = home_dir / ".local" / "share" / "applications"
            try:
                apps_dir.mkdir(parents=True, exist_ok=True)
                desktop_dir = apps_dir
                print(color_text("█ Creating shortcut in applications directory...", Fore.CYAN))
            except:
                # Fall back to home directory
                desktop_dir = home_dir
                shortcut_name = "ChronoTale_Launcher.desktop"
                print(color_text("█ Creating shortcut in home directory...", Fore.YELLOW))
        
        # Detect desktop environment and get appropriate terminal
        desktop_env = detect_desktop_environment()
        terminal_cmd = get_terminal_command(desktop_env)
        
        # Detect virtual environment
        venv_path = detect_virtual_env()
        
        # Create .desktop file for Linux
        if platform.system() == "Linux":
            desktop_file_path = desktop_dir / shortcut_name
            
            # Build command based on environment
            if venv_path:
                base_command = f'source {venv_path}/bin/activate && cd "{script_dir}" && python launch.py'
            else:
                base_command = f'cd "{script_dir}" && python3 launch.py'
            
            # Create a simple wrapper script that keeps terminal open
            wrapper_script = os.path.join(script_dir, 'launch_wrapper.sh')
            wrapper_content = f'''#!/bin/bash
set -e
cd "{script_dir}"
clear
echo "==============================================="
echo "    ChronoTale Launcher - Starting..."
echo "==============================================="
echo ""
python3 launch.py
echo ""
echo "==============================================="
echo "Game session ended. Press Enter to close..."
echo "==============================================="
read -p ""
'''
            
            with open(wrapper_script, 'w') as f:
                f.write(wrapper_content)
            os.chmod(wrapper_script, 0o755)
            
            # Simplified terminal command that should work universally
            exec_command = f'{terminal_cmd} -e {wrapper_script}'
            
            # Create icon path (try to find or create a simple icon)
            icon_path = os.path.join(script_dir, 'icon.png')
            if not os.path.exists(icon_path):
                # Use system game icon as fallback
                icon_path = 'applications-games'
            
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=ChronoTale Launcher
Comment=Multidimensional Adventure Game Collection for {desktop_env.title()}
Exec={exec_command}
Icon={icon_path}
Terminal=true
Categories=Game;Adventure;
StartupNotify=false
Keywords=game;adventure;story;interactive;
Path={script_dir}
"""
            
            with open(desktop_file_path, 'w') as f:
                f.write(desktop_content)
            
            # Make executable
            os.chmod(desktop_file_path, 0o755)
            
            # Also create a simple backup launcher
            simple_launcher = os.path.join(script_dir, 'chronotale_start.sh')
            simple_content = f'''#!/bin/bash
cd "{script_dir}"
python3 launch.py
echo "Press Enter to exit..."
read
'''
            with open(simple_launcher, 'w') as f:
                f.write(simple_content)
            os.chmod(simple_launcher, 0o755)
            
            print(color_text(f"█ Desktop shortcut created for {desktop_env.title()} at: {desktop_file_path}", Fore.GREEN))
            print(color_text(f"█ Using terminal: {terminal_cmd}", Fore.CYAN))
            print(color_text(f"█ Wrapper script created at: {wrapper_script}", Fore.CYAN))
            print(color_text(f"█ Simple launcher created at: {simple_launcher}", Fore.CYAN))
            
            # For Crostini, provide additional instructions
            if desktop_env == 'crostini':
                print(color_text("█ Crostini detected - shortcut optimized for Chrome OS", Fore.CYAN))
            
            print(color_text("█ Alternative launch methods:", Fore.YELLOW))
            print(color_text(f"█ 1. Double-click the desktop shortcut", Fore.CYAN))
            print(color_text(f"█ 2. Run in terminal: ./chronotale_start.sh", Fore.CYAN))
            print(color_text(f"█ 3. Direct launch: python3 launch.py", Fore.CYAN))
            
            return True
            
        else:
            print(color_text("█ Desktop shortcuts currently supported on Linux only!", Fore.YELLOW))
            # For non-Linux systems, create a simple launcher script
            try:
                launcher_script = desktop_dir / "start_chronotale.bat" if platform.system() == "Windows" else desktop_dir / "start_chronotale.sh"
                if platform.system() == "Windows":
                    script_content = f'@echo off\ncd /d "{script_dir}"\npython launch.py\npause'
                else:
                    script_content = f'#!/bin/bash\ncd "{script_dir}"\npython3 launch.py'
                
                with open(launcher_script, 'w') as f:
                    f.write(script_content)
                
                if platform.system() != "Windows":
                    os.chmod(launcher_script, 0o755)
                
                print(color_text(f"█ Launcher script created at: {launcher_script}", Fore.GREEN))
                return True
            except Exception as script_error:
                print(color_text(f"█ Could not create launcher script: {str(script_error)}", Fore.YELLOW))
                return False
            
    except Exception as e:
        print(color_text(f"█ Error creating desktop shortcut: {str(e)}", Fore.RED))
        print(color_text("█ You can still launch ChronoTale by running 'python launch.py' in the ChronoTale directory", Fore.CYAN))
        return False

def create_command_alias() -> bool:
    """Create a command alias for ChronoTale launcher"""
    try:
        # Get the directory where launch.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        launcher_path = os.path.join(script_dir, 'launch.py')
        
        if not os.path.exists(launcher_path):
            print(color_text("█ Error: launch.py not found!", Fore.RED))
            return False
        
        # Detect virtual environment
        venv_path = detect_virtual_env()
        home_dir = Path.home()
        
        # Create bash script in user's bin directory
        user_bin = home_dir / ".local" / "bin"
        user_bin.mkdir(parents=True, exist_ok=True)
        
        script_path = user_bin / "chronotale"
        
        if venv_path:
            # Script with virtual environment activation
            script_content = f"""#!/bin/bash
source {venv_path}/bin/activate
cd {script_dir}
python launch.py
deactivate
"""
        else:
            # Direct execution script
            script_content = f"""#!/bin/bash
cd {script_dir}
python launch.py
"""
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        # Check if ~/.local/bin is in PATH
        path_env = os.environ.get('PATH', '')
        if str(user_bin) not in path_env:
            # Add to bashrc if not in PATH
            bashrc_path = home_dir / ".bashrc"
            with open(bashrc_path, 'a') as f:
                f.write(f'\n# ChronoTale launcher command\nexport PATH="$HOME/.local/bin:$PATH"\n')
            
            print(color_text("█ Command alias 'chronotale' created!", Fore.GREEN))
            print(color_text("█ Run 'source ~/.bashrc' or restart terminal to use it", Fore.YELLOW))
        else:
            print(color_text("█ Command alias 'chronotale' created and ready to use!", Fore.GREEN))
        
        return True
        
    except Exception as e:
        print(color_text(f"█ Error creating command alias: {str(e)}", Fore.RED))
        return False

def install_system_integration() -> bool:
    """Install ChronoTale system integration"""
    try:
        success_count = 0
        
        print(color_text("█ Creating desktop shortcut...", Fore.CYAN))
        if create_desktop_shortcut():
            success_count += 1
        
        print(color_text("█ Creating command alias...", Fore.CYAN))
        if create_command_alias():
            success_count += 1
        
        if success_count > 0:
            print(color_text(f"█ System integration completed! ({success_count}/2 features installed)", Fore.GREEN))
            return True
        else:
            print(color_text("█ System integration failed!", Fore.RED))
            return False
            
    except Exception as e:
        print(color_text(f"█ Error during system integration: {str(e)}", Fore.RED))
        return False

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
    """Display enhanced settings with system integration features"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_banner()
        
        # Detect current environment status
        venv_detected = detect_virtual_env()
        venv_status = color_text("Detected", Fore.GREEN) if venv_detected else color_text("Not Detected", Fore.YELLOW)
        
        print(color_text("█ Settings & System Integration:", Fore.CYAN))
        print(color_text("█" + "="*50, Fore.CYAN))
        
        # Display settings
        print(color_text(f"█ [1] Toggle Colors: {'ON' if data['settings']['colors_enabled'] else 'OFF'}", Fore.CYAN))
        print(color_text(f"█ [2] Toggle Auto-Save: {'ON' if data['settings'].get('auto_save', True) else 'OFF'}", Fore.CYAN))
        
        # System Integration section
        print(color_text("\n█ System Integration:", Fore.MAGENTA))
        print(color_text("█ [3] Create Desktop Shortcut", Fore.GREEN))
        print(color_text("█ [4] Install Command Alias (chronotale)", Fore.GREEN))
        print(color_text("█ [5] Full System Integration", Fore.YELLOW))
        
        # Environment info
        print(color_text("\n█ Environment Status:", Fore.BLUE))
        print(color_text(f"█     Virtual Environment: {venv_status}", Fore.WHITE))
        if venv_detected:
            print(color_text(f"█     VEnv Path: {venv_detected}", Fore.WHITE))
        print(color_text(f"█     Platform: {platform.system()}", Fore.WHITE))
        print(color_text(f"█     Python: {sys.version.split()[0]}", Fore.WHITE))
        
        # Additional settings
        print(color_text("\n█ Advanced:", Fore.MAGENTA))
        print(color_text("█ [6] Reset All Settings", Fore.RED))
        print(color_text("█ [7] Export Game Data", Fore.BLUE))
        print(color_text("█ [8] Back to Main Menu", Fore.RED))
        
        print(color_text(f"\n█ Version: {VERSION}", Fore.YELLOW))

        choice = input(color_text("\n█ Select: ", Fore.YELLOW) + Style.RESET_ALL)

        if choice == '1':
            data['settings']['colors_enabled'] = not data['settings']['colors_enabled']
            save_game_data(data)
            print(color_text(f"█ Colors {'enabled' if data['settings']['colors_enabled'] else 'disabled'}!", Fore.GREEN))
            time.sleep(2)
            
        elif choice == '2':
            data['settings']['auto_save'] = not data['settings'].get('auto_save', True)
            save_game_data(data)
            print(color_text(f"█ Auto-save {'enabled' if data['settings']['auto_save'] else 'disabled'}!", Fore.GREEN))
            time.sleep(2)
            
        elif choice == '3':
            print(color_text("█ Creating desktop shortcut...", Fore.CYAN))
            if create_desktop_shortcut():
                print(color_text("█ Desktop shortcut created successfully!", Fore.GREEN))
                if venv_detected:
                    print(color_text("█ Shortcut configured with virtual environment support!", Fore.GREEN))
            else:
                print(color_text("█ Failed to create desktop shortcut!", Fore.RED))
            input(color_text("\n█ Press Enter to continue...", Fore.YELLOW))
            
        elif choice == '4':
            print(color_text("█ Installing command alias...", Fore.CYAN))
            if create_command_alias():
                print(color_text("█ Command alias 'chronotale' installed!", Fore.GREEN))
                if venv_detected:
                    print(color_text("█ Alias configured with virtual environment support!", Fore.GREEN))
                print(color_text("█ You can now run 'chronotale' from anywhere!", Fore.CYAN))
            else:
                print(color_text("█ Failed to create command alias!", Fore.RED))
            input(color_text("\n█ Press Enter to continue...", Fore.YELLOW))
            
        elif choice == '5':
            print(color_text("█ Installing full system integration...", Fore.MAGENTA))
            print(color_text("█ This will create both desktop shortcut and command alias", Fore.CYAN))
            confirm = input(color_text("█ Continue? (y/N): ", Fore.YELLOW))
            if confirm.lower() == 'y':
                if install_system_integration():
                    print(color_text("█ Full system integration completed successfully!", Fore.GREEN))
                    if venv_detected:
                        print(color_text("█ All features configured with virtual environment support!", Fore.GREEN))
                    print(color_text("█ ChronoTale is now fully integrated with your system!", Fore.CYAN))
                else:
                    print(color_text("█ System integration failed!", Fore.RED))
            input(color_text("\n█ Press Enter to continue...", Fore.YELLOW))
            
        elif choice == '6':
            print(color_text("█ This will reset all settings to default values!", Fore.RED))
            confirm = input(color_text("█ Are you sure? (y/N): ", Fore.YELLOW))
            if confirm.lower() == 'y':
                data['settings'] = {'colors_enabled': True, 'auto_save': True}
                save_game_data(data)
                print(color_text("█ All settings reset to defaults!", Fore.GREEN))
            time.sleep(2)
            
        elif choice == '7':
            try:
                export_path = f"chronotale_export_{int(time.time())}.json"
                with open(export_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(color_text(f"█ Game data exported to: {export_path}", Fore.GREEN))
            except Exception as e:
                print(color_text(f"█ Export failed: {str(e)}", Fore.RED))
            input(color_text("\n█ Press Enter to continue...", Fore.YELLOW))
            
        elif choice == '8':
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
    except UnicodeDecodeError as e:
        print("\n█ Input encoding error detected. Restarting with safe mode...")
        print("█ If this persists, try running with: PYTHONIOENCODING=utf-8 python launch.py")
        # Restart with simpler encoding
        os.environ['LC_ALL'] = 'C.UTF-8'
        os.environ['LANG'] = 'C.UTF-8'
        try:
            main_menu()
        except:
            print("█ Please restart the launcher or contact support.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(color_text("\n█ Force quit!", Fore.YELLOW))
        sys.exit(0)
    except Exception as e:
        print(f"█ Unexpected error: {e}")
        print("█ Please restart the launcher.")
        sys.exit(1)
