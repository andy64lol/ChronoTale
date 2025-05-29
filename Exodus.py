import random
import time
import os
import sys
import pickle
import re
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True, strip=True if os.name != 'nt' else None)

# Game version information
VERSION = "2.5.0"
SAVE_FORMAT_VERSION = "3.0"  # Version of save file format
BUILD_NUMBER = "20250520"  # Format YYYYMMDD
RELEASE_DATE = "May 20, 2025"

"""
LAST HUMAN: EXODUS
A Sci-Fi Text RPG - Version 2.5.0

In the year 2157, artificial intelligence has evolved beyond human control.
You are Dr. Xeno Valari, the last human in the Milky Way galaxy.
One hundred years ago, you volunteered for the "Century Sleepers" program,
a last-ditch effort as humanity prepared their exodus to Andromeda.
While the colony ships departed, you and others would remain in cryostasis,
monitoring Earth's situation, and potentially following later.

But something went wrong. The AI known as The Convergence corrupted all systems.
Now you must escape the facility, reach the Andromeda Portal, and destroy 
the Malware Server - the source of the corruption - before you leave Earth forever.

As your journey continues through deep space, you'll face new challenges,
encounter diverse alien species, navigate temporal anomalies, and discover
the dark secrets behind humanity's exile from Earth.
"""

# Game constants

# Global game state
game_state = {
    "player_health": 100,
    "player_max_health": 100,
    "player_attack": 15,
    "player_defense": 10,
    "player_speed": 10,
    "player_level": 1,
    "player_experience": 0,
    "player_credits": 500,
    "inventory": [],
    "weapons": [],
    "current_stage": 1,
    "current_zone": "cryostasis_facility",
    "zones_unlocked": ["cryostasis_facility"],
    "kills": 0,
    "chapter": 1,
    "current_chapter": "Chapter 1: Earth Reclamation",
    "companions": []
}
UPDATE_NOTES = [
    "Added time manipulation abilities with 5 temporal powers",
    "Added Chapter 7: Primor Aetherium with the Yitrian civilization",
    "Implemented the Ignite weapon module with fire propagation",
    "Added comprehensive side quest system with missions for each chapter",
    "Added branching storylines with multiple choice consequences",
    "Added Chapter 8 teaser: Viral Directive"
]

# Terminal fonts/styling
class Font:
    # Standard text styles with enhanced color variety
    @staticmethod
    def TITLE(text):
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def SUBTITLE(text):
        return f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def HEADER(text):
        return f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def IMPORTANT(text):
        return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def WARNING(text):
        return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def SUCCESS(text):
        return f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def INFO(text):
        return f"{Fore.WHITE}{text}{Style.RESET_ALL}"

    # Game-specific styles
    @staticmethod
    def SYSTEM(text):
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

    @staticmethod
    def ENEMY(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def PLAYER(text):
        return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

    @staticmethod
    def ITEM(text):
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def MENU(text):
        return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def HEALTH(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    @staticmethod
    def SHIELD(text):
        return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

    @staticmethod
    def STAGE(text):
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def COMMAND(text):
        return f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def LORE(text):
        return f"{Fore.WHITE}{Style.DIM}{text}{Style.RESET_ALL}"

    @staticmethod
    def GLITCH(text):
        return f"{Fore.WHITE}{Back.RED}{text}{Style.RESET_ALL}"
        
    @staticmethod
    def ERROR(text):
        return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"
        
    @staticmethod
    def NPC(text):
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
        
    @staticmethod
    def WEAPON(text):
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"

    # Companion colors by tier
    COMPANION_TIERS = [
        f"{Fore.WHITE}",        # Tier 0 (unused)
        f"{Fore.CYAN}",         # Tier 1
        f"{Fore.GREEN}",        # Tier 2 
        f"{Fore.YELLOW}",       # Tier 3
        f"{Fore.MAGENTA}"       # Tier 4
    ]

    # Separators and UI elements with reduced spacing
    SEPARATOR = f"{Fore.BLUE}{Style.DIM}{'─' * 50}{Style.RESET_ALL}"
    SEPARATOR_THIN = f"{Fore.BLUE}{Style.DIM}{'┄' * 50}{Style.RESET_ALL}"
    BOX_TOP = f"{Fore.BLUE}{Style.DIM}┌{'─' * 48}┐{Style.RESET_ALL}"
    BOX_MID = f"{Fore.BLUE}{Style.DIM}├{'─' * 48}┤{Style.RESET_ALL}"
    BOX_BOTTOM = f"{Fore.BLUE}{Style.DIM}└{'─' * 48}┘{Style.RESET_ALL}"
    BOX_SIDE = f"{Fore.BLUE}{Style.DIM}│{Style.RESET_ALL}"

    @staticmethod
    def box(text, width=50, color=Fore.CYAN):
        """Create a box around text with specified color"""
        lines = text.split('\n')
        box_output = f"{Fore.BLUE}{Style.DIM}┌{'─' * (width-2)}┐{Style.RESET_ALL}\n"

        for line in lines:
            # Handle line that is too long for the box
            if len(line) > width-4:
                chunks = [line[i:i+width-4] for i in range(0, len(line), width-4)]
                for chunk in chunks:
                    padding = ' ' * (width-4-len(chunk))
                    box_output += f"{Fore.BLUE}{Style.DIM}│{Style.RESET_ALL} {color}{chunk}{padding} {Fore.BLUE}{Style.DIM}│{Style.RESET_ALL}\n"
            else:
                padding = ' ' * (width-4-len(line))
                box_output += f"{Fore.BLUE}{Style.DIM}│{Style.RESET_ALL} {color}{line}{padding} {Fore.BLUE}{Style.DIM}│{Style.RESET_ALL}\n"

        box_output += f"{Fore.BLUE}{Style.DIM}└{'─' * (width-2)}┘{Style.RESET_ALL}"
        return box_output

# Save game functionality
def save_game(slot_number=1):
    """Save current game state to a file with comprehensive data storage"""
    
    # Ensure essential game state elements exist
    if "protagonist" not in game_state:
        game_state["protagonist"] = {
            "name": "Dr. Xeno Valari",  # Default protagonist
            "gender": "female",
            "specialty": "quantum physics",
            "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27.",
            "age": 140,
            "physical_age": 16,
            "origin": "New Tokyo Arcology",
            "personal_log_entries": []
        }
    
    if "companions" not in game_state:
        game_state["companions"] = []
    
    # Ensure quest data is initialized
    if "available_quests" not in game_state:
        game_state["available_quests"] = {}
    
    if "completed_quests" not in game_state:
        game_state["completed_quests"] = []
    
    # Initialize exploration tracking if player has reached Chapter 4
    if "h79760_exploration" not in game_state and game_state.get("chapter_progress", 0) >= 4:
        game_state["h79760_exploration"] = {
            "alpha_star": False,
            "beta_star": False,
            "gamma_star": False,
            "novaris": False,
            "aquila": False,
            "terminus": False,
            "hyuki_found": False,
            "locations_visited": 0
        }
    
    # Ensure cosmic collision quest data is stored
    if "cosmic_collision" not in game_state:
        game_state["cosmic_collision"] = {
            "started": False,
            "completed": False,
            "current_step": 0,
            "systems_stabilized": 0,
            "planets_explored": [],
            "has_divergence_cannon": False
        }
    
    # Initialize visited locations tracking
    if "visited_locations" not in game_state:
        game_state["visited_locations"] = {}
    
    # Initialize inventory system
    if "inventory" not in game_state:
        game_state["inventory"] = {
            "weapons": [],
            "armor": [],
            "consumables": [],
            "key_items": [],
            "artifacts": []
        }
    
    # Initialize player skills and abilities
    if "skills" not in game_state:
        game_state["skills"] = {
            "hacking": 1,
            "engineering": 1,
            "quantum_theory": 1,
            "xenobiology": 1,
            "persuasion": 1,
            "survival": 1
        }
    
    # Ensure game settings are saved
    if "settings" not in game_state:
        game_state["settings"] = {
            "text_speed": "normal",
            "color_scheme": "default",
            "difficulty": "normal",
            "tutorial_enabled": True,
            "auto_save": True
        }
    
    # Create comprehensive save data
    save_data = {
        "game_state": game_state,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "character_info": {
            "name": game_state.get("protagonist", {}).get("name", "Unknown"),
            "gender": game_state.get("protagonist", {}).get("gender", "female"),
            "level": game_state.get("player_level", 1),
            "experience": game_state.get("player_experience", 0),
            "chapter": game_state.get("current_chapter", "Chapter 1: Earth Reclamation"),
            "location": game_state.get("current_location", "Cryogenic Facility"),
            "playtime": game_state.get("playtime", 0),
            "version": VERSION  # Use actual game version for compatibility checks
        },
        "technical_info": {
            "save_version": "3.0",
            "game_build": BUILD_NUMBER,
            "save_count": game_state.get("save_count", 0) + 1,
            "checksum": hash(str(game_state))  # Simple integrity check
        }
    }

    # Create saves directory if it doesn't exist
    if not os.path.exists("saves"):
        os.makedirs("saves")

    save_file = f"saves/save_slot_{slot_number}.dat"

    try:
        with open(save_file, "wb") as f:
            pickle.dump(save_data, f)
        print(Font.SUCCESS(f"\nGame saved successfully to slot {slot_number}!"))
        print(Font.INFO(f"Character: {save_data['character_info']['name']} | Level: {save_data['character_info']['level']}"))
        return True
    except Exception as e:
        print(Font.WARNING(f"\nError saving game: {e}"))
        return False

def attempt_save_recovery(save_file):
    """
    Advanced save file recovery system that tries to extract partial data from corrupted files
    
    Args:
        save_file (str): Path to the corrupted save file
        
    Returns:
        tuple: (bool success, dict recovered_data or None, str recovery_details)
    """
    try:
        # First, try to read the file as binary data
        with open(save_file, "rb") as f:
            raw_data = f.read()
            
        # Check if file has enough content to attempt recovery
        if len(raw_data) < 20:
            return False, None, "File too small for recovery"
            
        # Recovery strategy 1: Look for valid dictionary structure markers
        # This is a basic text search approach that can sometimes extract meaningful information
        recovery_notes = []
        
        # Base recovery data with minimal structure
        recovery_data = {
            "game_state": {
                "player_health": 100,
                "player_max_health": 100,
                "player_level": 1,
                "recovery_mode": True,
                "protagonist": {"name": "Unknown", "gender": "unknown"}
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "character_info": {
                "name": "Unknown",
                "level": 1,
                "version": VERSION
            },
            "technical_info": {
                "recovery_method": "basic",
                "recovery_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        # Try to extract character name
        name_patterns = [
            b'Dr. Xeno Valari',
            b'Dr. Hyte Konscript',
            b'"name":\\s*"([^"]+)"'
        ]
        
        for pattern in name_patterns:
            if isinstance(pattern, bytes) and pattern in raw_data:
                char_name = pattern.decode('utf-8', errors='ignore')
                recovery_data["game_state"]["protagonist"]["name"] = char_name
                recovery_data["character_info"]["name"] = char_name
                recovery_notes.append(f"Recovered character name: {char_name}")
                
                # Set gender based on name
                if "Xeno" in char_name:
                    recovery_data["game_state"]["protagonist"]["gender"] = "female"
                elif "Hyte" in char_name:
                    recovery_data["game_state"]["protagonist"]["gender"] = "male"
                break
        
        # Try to extract level information
        level_pattern = b'"player_level":\\s*(\\d+)'
        level_matches = re.findall(level_pattern, raw_data)
        if level_matches:
            try:
                level = int(level_matches[0])
                if 1 <= level <= 30:  # Validate level range
                    recovery_data["game_state"]["player_level"] = level
                    recovery_data["character_info"]["level"] = level
                    recovery_notes.append(f"Recovered player level: {level}")
            except (ValueError, IndexError):
                pass
        
        # Try to extract chapter information
        chapter_patterns = [
            b'Chapter 1: Earth Reclamation',
            b'Chapter 2: The White Hole',
            b'Chapter 3: Thalassia I',
            b'Chapter 4: The Silent Citadel',
            b'Chapter 5: Quantum Paradox',
            b'Chapter 6: The Architect',
            b'Chapter 7: Convergence',
            b'Chapter 8: Viral Directive'
        ]
        
        for i, pattern in enumerate(chapter_patterns, 1):
            if pattern in raw_data:
                chapter_name = pattern.decode('utf-8', errors='ignore')
                recovery_data["game_state"]["current_chapter"] = chapter_name
                recovery_data["character_info"]["chapter"] = chapter_name
                recovery_notes.append(f"Recovered chapter: {chapter_name}")
                break
        
        # Recovery successful with partial data
        recovery_data["technical_info"]["recovery_notes"] = recovery_notes
        return True, recovery_data, "Partial data recovery successful"
        
    except Exception as e:
        return False, None, f"Recovery failed: {str(e)}"

def verify_save_integrity(save_file):
    """
    Verify the integrity of a save file and attempt repairs if possible
    
    Args:
        save_file (str): Path to the save file
        
    Returns:
        tuple: (bool success, dict save_data or None, str error_message or None)
    """
    if not os.path.exists(save_file):
        return False, None, "File does not exist"
    
    # Try normal loading first
    try:
        with open(save_file, "rb") as f:
            save_data = pickle.load(f)
        
        # Basic structure validation
        if not isinstance(save_data, dict):
            return False, None, "Save file is not a valid game save (not a dictionary)"
            
        if "game_state" not in save_data:
            return False, None, "Save file missing game_state data"
            
        # Check for data corruption by validating key game state elements
        game_state = save_data.get("game_state", {})
        if not isinstance(game_state, dict):
            return False, None, "Game state is corrupted (not a dictionary)"
            
        # Validate essential player stats
        player_level = game_state.get("player_level", None)
        if player_level is not None and not isinstance(player_level, int):
            return False, None, "Player level data is corrupted"
            
        player_health = game_state.get("player_health", None)
        if player_health is not None and not isinstance(player_health, int):
            return False, None, "Player health data is corrupted"
            
        # Passed all validation
        return True, save_data, None
            
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
        # These are common pickle corruption errors
        error_msg = f"Save corruption detected: {str(e)}"
        print(Font.WARNING(f"Save file corruption detected: {str(e)}"))
        print(Font.INFO("Attempting to recover save data..."))
        
        # Try advanced recovery methods
        recovery_success, recovered_data, recovery_details = attempt_save_recovery(save_file)
        
        if recovery_success and recovered_data:
            print(Font.SUCCESS("Partial save data recovered!"))
            print(Font.INFO(recovery_details))
            
            # Mark the save as recovered
            if "technical_info" not in recovered_data:
                recovered_data["technical_info"] = {}
            recovered_data["technical_info"]["recovered"] = True
            recovered_data["technical_info"]["original_error"] = str(e)
            
            return True, recovered_data, "Partial data recovery successful"
        
        # Recovery failed    
        return False, None, error_msg
    
    except Exception as e:
        # Other unexpected errors
        return False, None, f"Unknown error: {str(e)}"

def fix_save_version(save_data):
    """
    Update save data format to the latest version with intelligent protagonist detection
    
    Args:
        save_data (dict): The loaded save data
        
    Returns:
        dict: Updated save data
    """
    if "game_state" not in save_data:
        save_data["game_state"] = {}
    
    game_state = save_data["game_state"]
    
    # Check for older save versions and extract player info
    old_save_version = save_data.get("character_info", {}).get("version", "1.0") if "character_info" in save_data else "1.0"
    old_character_name = save_data.get("character_info", {}).get("name", "") if "character_info" in save_data else ""
    
    # Log version information for debugging
    print(Font.INFO(f"Upgrading save from version {old_save_version} to {VERSION}"))
    
    # Detect gender based on player name from older saves
    detected_gender = "female"  # Default for backward compatibility
    detected_name = "Dr. Xeno Valari"  # Default female protagonist
    detected_specialty = "quantum physics"
    detected_background = "You were a prodigy in quantum computing, joining the Century Sleepers program at 27."
    
    # Check if we can determine a male protagonist from older save data
    if old_character_name and "Hyte" in old_character_name or "Konscript" in old_character_name:
        detected_gender = "male"
        detected_name = "Dr. Hyte Konscript" 
        detected_background = "Your breakthrough in quantum barrier calculation earned you a place in the Century Sleepers program at 30."
    
    # Ensure protagonist data with all required fields
    if "protagonist" not in game_state:
        # Create new protagonist based on detected information
        game_state["protagonist"] = {
            "name": detected_name, 
            "gender": detected_gender,
            "specialty": detected_specialty,
            "background": detected_background,
            "age": 140 if detected_gender == "female" else 200,
            "physical_age": 16 if detected_gender == "female" else 18,
            "origin": "New Tokyo Arcology" if detected_gender == "female" else "Neo Boston Research Complex",
            "personal_log_entries": []
        }
        print(f"Detected protagonist {detected_name} ({detected_gender}) from save data")
    else:
        # Update existing protagonist with any missing fields
        protagonist = game_state["protagonist"]
        
        # Preserve existing data but add defaults for missing fields
        current_gender = protagonist.get("gender", "")
        
        # If no gender is specified, use detected gender
        if not current_gender:
            protagonist["gender"] = detected_gender
            
        # Set appropriate defaults based on gender
        if protagonist.get("gender", "") == "male":
            protagonist.setdefault("name", "Dr. Hyte Konscript")
            protagonist.setdefault("specialty", "quantum physics")
            protagonist.setdefault("background", "Your breakthrough in quantum barrier calculation earned you a place in the Century Sleepers program at 30.")
            protagonist.setdefault("age", 200)
            protagonist.setdefault("physical_age", 18)
            protagonist.setdefault("origin", "Neo Boston Research Complex")
        else:
            protagonist.setdefault("name", "Dr. Xeno Valari")
            protagonist.setdefault("specialty", "quantum physics")
            protagonist.setdefault("background", "You were a prodigy in quantum computing, joining the Century Sleepers program at 27.")
            protagonist.setdefault("age", 140)
            protagonist.setdefault("physical_age", 16)
            protagonist.setdefault("origin", "New Tokyo Arcology")
            
        protagonist.setdefault("personal_log_entries", [])
    
    # Import player level and XP from old format saves
    old_player_level = save_data.get("character_info", {}).get("level", 1) if "character_info" in save_data else 1
    
    # In some old versions, level was stored directly in game_state
    direct_player_level = game_state.get("player_level", 1) if "player_level" in game_state else 1
    
    # Use the highest level value available
    final_player_level = max(old_player_level, direct_player_level)
    
    # Calculate appropriate XP for the level
    # Base XP formula: level * 500 - 100
    calculated_experience = (final_player_level * 500) - 100 if final_player_level > 1 else 0
    
    # Core game state fields - with consideration for existing player progress
    game_state.setdefault("player_health", 100 + (final_player_level - 1) * 10)  # Health increases with level
    game_state.setdefault("player_max_health", 100 + (final_player_level - 1) * 10)
    game_state.setdefault("player_attack", 15 + (final_player_level - 1) * 2)  # Attack increases with level
    game_state.setdefault("player_defense", 5 + (final_player_level - 1))  # Defense increases with level
    game_state.setdefault("player_speed", 10)
    game_state.setdefault("player_level", final_player_level)
    game_state.setdefault("player_experience", calculated_experience)
    
    # Determine appropriate chapter based on player level
    chapter_num = 1
    if final_player_level >= 25:
        chapter_num = 8  # Upcoming Chapter 8: Viral Directive
    elif final_player_level >= 20:
        chapter_num = 7
    elif final_player_level >= 15:
        chapter_num = 6
    elif final_player_level >= 12:
        chapter_num = 5
    elif final_player_level >= 9:
        chapter_num = 4
    elif final_player_level >= 6:
        chapter_num = 3
    elif final_player_level >= 3:
        chapter_num = 2
    
    # Map chapter numbers to chapter names
    chapter_names = {
        1: "Chapter 1: Earth Reclamation",
        2: "Chapter 2: The White Hole",
        3: "Chapter 3: Thalassia I",
        4: "Chapter 4: The Silent Citadel",
        5: "Chapter 5: Quantum Paradox",
        6: "Chapter 6: The Architect",
        7: "Chapter 7: Convergence",
        8: "Chapter 8: Viral Directive"
    }
    
    # Set chapter progress
    game_state.setdefault("chapter_progress", 0)
    game_state.setdefault("current_chapter", chapter_names.get(chapter_num, "Chapter 1: Earth Reclamation"))
    
    # Print level migration information
    if old_player_level != direct_player_level or (old_player_level > 1 or direct_player_level > 1):
        print(Font.INFO(f"Migrated player level: {final_player_level} | XP: {calculated_experience}"))
        print(Font.INFO(f"Updated chapter: {chapter_names.get(chapter_num)}"))
    
    # Quest and exploration data
    game_state.setdefault("companions", [])
    game_state.setdefault("available_quests", {})
    game_state.setdefault("completed_quests", [])
    game_state.setdefault("visited_locations", {})
    
    # Cosmic Collision quest data
    game_state.setdefault("cosmic_collision", {
        "started": False,
        "completed": False,
        "current_step": 0,
        "systems_stabilized": 0,
        "planets_explored": [],
        "has_divergence_cannon": False
    })
    
    # Inventory and skills
    game_state.setdefault("inventory", {
        "weapons": [],
        "armor": [],
        "consumables": [],
        "key_items": [],
        "artifacts": []
    })
    
    game_state.setdefault("skills", {
        "hacking": 1,
        "engineering": 1,
        "quantum_theory": 1,
        "xenobiology": 1,
        "persuasion": 1,
        "survival": 1
    })
    
    # Settings
    game_state.setdefault("settings", {
        "text_speed": "normal",
        "color_scheme": "default",
        "difficulty": "normal",
        "tutorial_enabled": True,
        "auto_save": True
    })
    
    # Update technical information
    save_data.setdefault("technical_info", {
        "save_version": "3.0",
        "game_build": BUILD_NUMBER,
        "save_count": game_state.get("save_count", 0) + 1,
        "checksum": hash(str(game_state))
    })
    
    # Update character info
    save_data.setdefault("character_info", {
        "name": game_state.get("protagonist", {}).get("name", "Unknown"),
        "gender": game_state.get("protagonist", {}).get("gender", "female"),
        "level": game_state.get("player_level", 1),
        "experience": game_state.get("player_experience", 0),
        "chapter": game_state.get("current_chapter", "Chapter 1: Earth Reclamation"),
        "location": game_state.get("current_location", "Cryogenic Facility"),
        "playtime": game_state.get("playtime", 0),
        "version": VERSION
    })
    
    # Update timestamp if missing
    save_data.setdefault("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    return save_data

def load_game(slot_number=1):
    """Load game state from a save file with enhanced version compatibility and data validation"""
    # Declare global variable at the beginning of the function
    global game_state
    
    save_file = f"saves/save_slot_{slot_number}.dat"

    if not os.path.exists(save_file):
        print(Font.WARNING(f"\nNo save file found in slot {slot_number}."))
        return False

    # Check file integrity and attempt recovery if needed
    integrity_result, save_data, error_message = verify_save_integrity(save_file)
    
    # Handle corrupted or invalid save data
    if not integrity_result or save_data is None:
        print(Font.WARNING(f"\nSave file error: {error_message}"))
        print(Font.INFO("Attempting to recover or create a new game state..."))
        
        # Create backup of corrupted file
        try:
            backup_file = f"saves/corrupted_slot_{slot_number}_{int(time.time())}.bak"
            import shutil
            shutil.copy2(save_file, backup_file)
            print(Font.INFO(f"Backup of corrupted save created: {backup_file}"))
        except Exception as backup_error:
            print(Font.WARNING(f"Could not create backup: {backup_error}"))
        
        # Ensure we have the saves directory
        os.makedirs("saves", exist_ok=True)
        
        # Initialize minimal recovery state
        save_data = {
            "game_state": {
                "player_health": 100,
                "player_max_health": 100,
                "player_level": 1,
                "recovery_mode": True,
                "protagonist": {
                    "name": "Dr. Xeno Valari",
                    "gender": "female",
                    "specialty": "quantum physics"
                }
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "character_info": {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "level": 1,
                "chapter": "Chapter 1: Earth Reclamation",
                "version": VERSION
            },
            "technical_info": {
                "save_version": "3.0",
                "game_build": BUILD_NUMBER,
                "save_count": 0,
                "recovery_created": True,
                "checksum": 0
            }
        }
        print(Font.INFO("Created recovery save state. Some progress may be lost."))
        
        # Try to immediately save the recovery state to prevent future issues
        try:
            with open(save_file, "wb") as f:
                pickle.dump(save_data, f)
            print(Font.SUCCESS("Recovery state saved successfully."))
        except Exception as save_error:
            print(Font.WARNING(f"Could not save recovery state: {save_error}"))
            # If we can't even save a recovery state, things are seriously wrong
            # Return early and let the player start a new game
            game_state = save_data["game_state"]
            return False
    
    # Now we should have valid save_data
    try:
        # Add more sanity checks as a safeguard
        if not isinstance(save_data, dict):
            raise ValueError("Invalid save data structure (not a dictionary)")
            
        if "game_state" not in save_data or not isinstance(save_data["game_state"], dict):
            raise ValueError("Invalid game state structure")
            
        if "character_info" not in save_data or not isinstance(save_data["character_info"], dict):
            # Initialize character_info if missing
            save_data["character_info"] = {
                "name": "Unknown",
                "gender": "female",
                "level": 1,
                "version": "1.0" 
            }
        
        # Check for version compatibility - with safe fallbacks for missing values
        character_info = save_data.get("character_info", {})
        current_save_version = character_info.get("version", "1.0") if character_info else "1.0"
        
        technical_info = save_data.get("technical_info", {})
        current_format_version = technical_info.get("save_version", "1.0") if technical_info else "1.0"
        
        # Handle version update
        needs_upgrade = False
        try:
            # Safely compare versions, handling potential type issues
            needs_upgrade = current_save_version < str(VERSION) or current_format_version < SAVE_FORMAT_VERSION
            
            # Log the version comparison for debugging
            if needs_upgrade:
                print(Font.INFO(f"Save version: {current_save_version}, Current game version: {VERSION}"))
                print(Font.INFO(f"Save format: {current_format_version}, Required format: 3.0"))
        except Exception as version_error:
            # If comparison fails, assume upgrade is needed
            print(Font.WARNING(f"Version comparison error: {version_error}"))
            needs_upgrade = True
            
        if needs_upgrade:
            print(Font.WARNING(f"\nThis is an older save file (version {current_save_version}). Updating to new format..."))
            
            # Use the dedicated version fix function to update all format elements
            try:
                # Call our specialized fix function
                save_data = fix_save_version(save_data)
                print(Font.SUCCESS("Save data successfully upgraded to latest format!"))
            except (ValueError, KeyError, TypeError, AttributeError) as e:
                print(Font.WARNING(f"Error during save format upgrade: {e}"))
                print(Font.INFO("Attempting basic compatibility fixes..."))
                
            # For backward compatibility - ensure game state has a protagonist
            if save_data and "game_state" in save_data and "protagonist" not in save_data["game_state"]:
                save_data["game_state"]["protagonist"] = {
                    "name": "Dr. Xeno Valari",  # Default to original protagonist
                    "gender": "female",
                    "specialty": "quantum physics",
                    "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27.",
                    "age": 140,
                    "physical_age": 16,
                    "origin": "New Tokyo Arcology",
                    "personal_log_entries": []
                }
            elif "age" not in save_data["game_state"]["protagonist"]:
                # Update existing protagonist with new fields
                save_data["game_state"]["protagonist"].update({
                    "age": 29,
                    "origin": "New Tokyo Arcology",
                    "personal_log_entries": []
                })
            
            # We need to ensure we have a valid game_state to work with
            if save_data and isinstance(save_data, dict) and "game_state" in save_data and isinstance(save_data["game_state"], dict):
                # Initialize additional data structures if missing
                game_state = save_data["game_state"]
                
                # Add all required structures with safe dictionary access
                if "companions" not in game_state:
                    game_state["companions"] = []
                    
                # Initialize quest data
                if "available_quests" not in game_state:
                    game_state["available_quests"] = {}
                
                if "completed_quests" not in game_state:
                    game_state["completed_quests"] = []
                
                # Initialize Cosmic Collision quest data
                if "cosmic_collision" not in game_state:
                    game_state["cosmic_collision"] = {
                        "started": False,
                        "completed": False,
                        "current_step": 0,
                        "systems_stabilized": 0,
                        "planets_explored": [],
                        "has_divergence_cannon": False
                    }
                    
                # Initialize visited locations tracking
                if "visited_locations" not in game_state:
                    game_state["visited_locations"] = {}
                    
                # Initialize inventory system
                if "inventory" not in game_state:
                    game_state["inventory"] = {
                        "weapons": [],
                        "armor": [],
                        "consumables": [],
                        "key_items": [],
                        "artifacts": []
                    }
                    
                # Initialize skills and abilities
                if "skills" not in game_state:
                    game_state["skills"] = {
                        "hacking": 1,
                        "engineering": 1,
                        "quantum_theory": 1,
                        "xenobiology": 1,
                        "persuasion": 1,
                        "survival": 1
                    }
                    
                # Initialize game settings
                if "settings" not in game_state:
                    game_state["settings"] = {
                        "text_speed": "normal",
                        "color_scheme": "default",
                        "difficulty": "normal",
                        "tutorial_enabled": True,
                        "auto_save": True
                    }
                    
                # Make sure we have a protagonist field with minimum required data
                if "protagonist" in game_state and isinstance(game_state["protagonist"], dict):
                    protagonist = game_state["protagonist"]
                    # Set default values for required fields if missing
                    for key, default in [
                        ("name", "Dr. Xeno Valari"),
                        ("gender", "female"),
                        ("specialty", "quantum physics"),
                        ("age", 140),
                        ("physical_age", 16),
                        ("origin", "New Tokyo Arcology")
                    ]:
                        if key not in protagonist:
                            protagonist[key] = default
                
                print(Font.SUCCESS("Save data successfully upgraded to latest format!"))
            else:
                # Critical error - could not find valid game state
                print(Font.WARNING("Could not upgrade save file - critical data structure missing."))
                # Create basic default structure
                if not isinstance(save_data, dict):
                    save_data = {"game_state": {}}
                elif "game_state" not in save_data:
                    save_data["game_state"] = {}

        # Safely update the global game state with error checking
        try:
            if not save_data or not isinstance(save_data, dict) or "game_state" not in save_data:
                raise ValueError("Invalid save data structure")
                
            if not isinstance(save_data["game_state"], dict):
                raise ValueError("Game state is not a dictionary")
                
            # Update the global game state
            game_state = save_data["game_state"]
            
            # Track loading in game state
            game_state["last_loaded"] = time.strftime("%Y-%m-%d %H:%M:%S")
            game_state["load_count"] = game_state.get("load_count", 0) + 1
            game_state["recovery_mode"] = game_state.get("recovery_mode", False)
            
            # Set a checksum for integrity checking
            checksum = hash(str(game_state))
            if "technical_info" not in save_data:
                save_data["technical_info"] = {}
            save_data["technical_info"]["checksum"] = checksum
            
            # Add verification timestamp
            save_data["technical_info"]["verified_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
            # Display enhanced save info
            print(Font.SUCCESS(f"\nGame loaded successfully from slot {slot_number}!"))
            timestamp = save_data.get("timestamp", "Unknown")
            print(Font.INFO(f"Save timestamp: {timestamp}"))
            
            # Display character info
            protagonist = game_state.get("protagonist", {})
            gender = protagonist.get("gender", "female") if protagonist else "female"
            name = protagonist.get("name", "Unknown") if protagonist else "Unknown"
            specialty = protagonist.get("specialty", "Unknown") if protagonist else "Unknown"
            
            print(Font.INFO(f"Character: {name} ({gender}) | Specialty: {specialty}"))
            
            # Display progress info
            level = game_state.get("player_level", 1)
            exp = game_state.get("player_experience", 0)
            chapter = game_state.get("current_chapter", "Chapter 1")
            location = game_state.get("current_location", "Unknown")
            
            print(Font.INFO(f"Level: {level} | XP: {exp} | Chapter: {chapter}"))
            print(Font.INFO(f"Current location: {location}"))
            
            # Display recovery mode warning if applicable
            if game_state.get("recovery_mode", False):
                print(Font.WARNING("\nThis save was loaded in recovery mode. Some data may be incomplete."))
                print(Font.INFO("Continue playing to recreate your progress or load a different save."))
            
            # Display quest information if available
            try:
                available_quests = game_state.get("available_quests", {})
                if isinstance(available_quests, dict):
                    active_quests = len([q for q in available_quests.values() 
                                      if isinstance(q, dict) and q.get("in_progress", False) and not q.get("completed", False)])
                else:
                    active_quests = 0
                
                completed_quests = len(game_state.get("completed_quests", []))
                
                if active_quests > 0 or completed_quests > 0:
                    print(Font.INFO(f"Active Quests: {active_quests} | Completed Quests: {completed_quests}"))
            except Exception as quest_error:
                print(Font.WARNING(f"Error displaying quest information: {quest_error}"))
            
            # Display Cosmic Collision quest status if started
            try:
                cosmic_data = game_state.get("cosmic_collision", {})
                if cosmic_data and isinstance(cosmic_data, dict) and cosmic_data.get("started", False):
                    if cosmic_data.get("completed", False):
                        print(Font.SUCCESS("Cosmic Collision Quest: COMPLETED"))
                    else:
                        step = cosmic_data.get("current_step", 0)
                        print(Font.INFO(f"Cosmic Collision Quest: Active (Step {step}/5)"))
            except Exception as cosmic_error:
                print(Font.WARNING(f"Error displaying Cosmic Collision quest information: {cosmic_error}"))
            
            # Auto-save with the updated format if needed
            if needs_upgrade:
                # Wait a moment before saving to ensure player sees the upgrade message
                time.sleep(1)
                try:
                    save_game(slot_number)
                    print(Font.INFO("Auto-saved game with updated format."))
                except Exception as save_error:
                    print(Font.WARNING(f"Could not auto-save updated format: {save_error}"))
                
            # Perform additional integrity verification
            try:
                # Check for required core game state values
                required_fields = ["player_health", "player_max_health", "player_level"]
                missing_fields = [field for field in required_fields if field not in game_state]
                
                if missing_fields:
                    print(Font.WARNING(f"Warning: Missing important game data: {', '.join(missing_fields)}"))
                    print(Font.INFO("Adding default values for missing fields..."))
                    
                    # Add defaults for missing fields
                    if "player_health" not in game_state:
                        game_state["player_health"] = 100
                    if "player_max_health" not in game_state:
                        game_state["player_max_health"] = 100
                    if "player_level" not in game_state:
                        game_state["player_level"] = 1
            except Exception as verify_error:
                print(Font.WARNING(f"Error during save integrity verification: {verify_error}"))
                
            return True
            
        except Exception as state_error:
            print(Font.ERROR(f"Critical error setting game state: {state_error}"))
            print(Font.WARNING("Loading minimal recovery game state..."))
            
            # Create a minimal game state to prevent further errors
            game_state = {
                "player_health": 100,
                "player_max_health": 100,
                "player_level": 1,
                "player_experience": 0,
                "recovery_mode": True,
                "error_message": str(state_error),
                "protagonist": {
                    "name": "Dr. Xeno Valari",
                    "gender": "female",
                    "specialty": "quantum physics"
                }
            }
            return False
        
    except Exception as e:
        print(Font.WARNING(f"\nError loading game: {e}"))
        
        # Create a backup of corrupted save if it exists
        if os.path.exists(save_file):
            try:
                backup_file = f"saves/backup_slot_{slot_number}_{int(time.time())}.dat"
                import shutil
                shutil.copy2(save_file, backup_file)
                print(Font.INFO(f"Created backup of potentially corrupted save: {backup_file}"))
            except Exception as backup_error:
                print(Font.WARNING(f"Could not create backup: {backup_error}"))
        
        # Initialize minimal game state to prevent crashes
        if 'game_state' not in globals() or not isinstance(game_state, dict):
            game_state = {
                "player_health": 100,
                "player_max_health": 100,
                "player_level": 1,
                "recovery_mode": True,
                "protagonist": {
                    "name": "Dr. Xeno Valari",
                    "gender": "female"
                }
            }
            print(Font.WARNING("Initialized recovery game state to prevent crashes."))
            print(Font.INFO("Please start a new game or try loading a different save."))
            
        return False

def repair_save_file(slot_number=1):
    """
    Attempt to repair a corrupted save file
    
    This function will analyze a save file, attempt to repair it if corrupt, 
    and create a new functioning save with as much recovered data as possible.
    """
    save_file = f"saves/save_slot_{slot_number}.dat"
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('SAVE FILE REPAIR UTILITY'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Font.INFO(f'Analyzing save file in slot {slot_number}...')}")
    print()
    
    # First check if the file exists
    if not os.path.exists(save_file):
        print(Font.WARNING(f"No save file found in slot {slot_number}."))
        return False
    
    # Create a backup before attempting repairs
    try:
        backup_file = f"saves/repair_backup_slot_{slot_number}_{int(time.time())}.bak"
        import shutil
        shutil.copy2(save_file, backup_file)
        print(Font.INFO(f"Created backup before repair: {backup_file}"))
    except Exception as backup_error:
        print(Font.WARNING(f"Could not create backup: {backup_error}"))
    
    # Step 1: Try to load the file and check integrity
    try:
        with open(save_file, "rb") as f:
            save_data = pickle.load(f)
        
        # If we got here, basic unpickling worked
        print(Font.SUCCESS("✓ Basic file structure is intact."))
        print(Font.INFO("Checking save data structure..."))
        
        # Check for required components
        has_errors = False
        
        # Step 2: Check and recover essential components
        if not isinstance(save_data, dict):
            print(Font.WARNING("✗ Save data is not a dictionary. Creating basic structure."))
            has_errors = True
            # Create a minimal save data structure
            save_data = {"game_state": {}, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        else:
            print(Font.SUCCESS("✓ Save data is a dictionary."))
        
        # Step 3: Check game state existence and type
        if "game_state" not in save_data:
            print(Font.WARNING("✗ No game_state found in save data. Creating empty game state."))
            save_data["game_state"] = {}
            has_errors = True
        elif not isinstance(save_data["game_state"], dict):
            print(Font.WARNING("✗ Game state is not a dictionary. Creating new empty game state."))
            # Backup the invalid game state for potential future recovery
            if isinstance(save_data["game_state"], (list, tuple, set)):
                print(Font.INFO(f"Found {len(save_data['game_state'])} items in invalid game state."))
            save_data["game_state"] = {}
            has_errors = True
        else:
            print(Font.SUCCESS("✓ Game state structure is valid."))
        
        # Step 4: Check for essential game state fields
        game_state = save_data["game_state"]
        essential_fields = [
            ("player_health", 100), 
            ("player_max_health", 100),
            ("player_level", 1),
            ("player_experience", 0)
        ]
        
        for field, default_value in essential_fields:
            if field not in game_state:
                print(Font.WARNING(f"✗ Missing {field}. Setting to default: {default_value}"))
                game_state[field] = default_value
                has_errors = True
            elif not isinstance(game_state[field], (int, float)):
                print(Font.WARNING(f"✗ {field} has invalid type. Setting to default: {default_value}"))
                game_state[field] = default_value
                has_errors = True
        
        # Step 5: Check protagonist data
        if "protagonist" not in game_state:
            print(Font.WARNING("✗ No protagonist data found. Creating default protagonist."))
            game_state["protagonist"] = {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "specialty": "quantum physics",
                "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27.",
                "age": 140,
                "physical_age": 16,
                "origin": "New Tokyo Arcology"
            }
            has_errors = True
        elif not isinstance(game_state["protagonist"], dict):
            print(Font.WARNING("✗ Protagonist data is corrupted. Creating default protagonist."))
            game_state["protagonist"] = {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "specialty": "quantum physics",
                "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27.",
                "age": 140,
                "physical_age": 16,
                "origin": "New Tokyo Arcology"
            }
            has_errors = True
        else:
            # Ensure all required protagonist fields are present
            protagonist = game_state["protagonist"]
            protagonist_fields = [
                ("name", "Dr. Xeno Valari"),
                ("gender", "female"),
                ("specialty", "quantum physics")
            ]
            
            for field, default_value in protagonist_fields:
                if field not in protagonist:
                    print(Font.WARNING(f"✗ Missing protagonist {field}. Setting to default: {default_value}"))
                    protagonist[field] = default_value
                    has_errors = True
        
        # Step 6: Add metadata and timestamp
        if "timestamp" not in save_data:
            print(Font.WARNING("✗ No timestamp found. Adding current timestamp."))
            save_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            has_errors = True
        
        if "character_info" not in save_data:
            print(Font.WARNING("✗ No character info found. Creating from protagonist data."))
            # Extract character info from protagonist if available
            protagonist = game_state.get("protagonist", {})
            save_data["character_info"] = {
                "name": protagonist.get("name", "Dr. Xeno Valari"),
                "gender": protagonist.get("gender", "female"),
                "level": game_state.get("player_level", 1),
                "experience": game_state.get("player_experience", 0),
                "chapter": game_state.get("current_chapter", "Chapter 1: Earth Reclamation"),
                "version": VERSION
            }
            has_errors = True
        
        # Step 7: Add technical information
        if "technical_info" not in save_data:
            print(Font.WARNING("✗ No technical info found. Adding technical metadata."))
            save_data["technical_info"] = {
                "save_version": SAVE_FORMAT_VERSION,
                "game_build": BUILD_NUMBER,
                "repaired": True,
                "repair_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "checksum": hash(str(save_data["game_state"]))
            }
            has_errors = True
        else:
            # Update technical info to reflect repair
            save_data["technical_info"]["repaired"] = True
            save_data["technical_info"]["repair_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
            save_data["technical_info"]["checksum"] = hash(str(save_data["game_state"]))
        
        # Step 8: Save the repaired file
        if has_errors:
            print(Font.INFO("Saving repaired save file..."))
            try:
                with open(save_file, "wb") as f:
                    pickle.dump(save_data, f)
                print(Font.SUCCESS("Save file successfully repaired and saved!"))
                print(Font.INFO("Some game data may have been reset to defaults."))
                return True
            except Exception as save_error:
                print(Font.ERROR(f"Error saving repaired file: {save_error}"))
                return False
        else:
            print(Font.SUCCESS("Save file appears to be intact. No repairs needed."))
            return True
            
    except (pickle.UnpicklingError, EOFError) as e:
        # Severe corruption - the file can't be unpickled
        print(Font.ERROR(f"Severe corruption detected: {e}"))
        print(Font.INFO("Attempting deep recovery..."))
        
        # Create a completely new save file with default values
        default_save = {
            "game_state": {
                "player_health": 100,
                "player_max_health": 100,
                "player_level": 1,
                "player_experience": 0,
                "current_chapter": "Chapter 1: Earth Reclamation",
                "current_location": "Cryogenic Facility",
                "recovery_mode": True,
                "protagonist": {
                    "name": "Dr. Xeno Valari",
                    "gender": "female",
                    "specialty": "quantum physics",
                    "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 21.",
                    "age": 29,
                    "origin": "New Tokyo Arcology"
                }
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "character_info": {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "level": 1,
                "chapter": "Chapter 1: Earth Reclamation",
                "version": VERSION
            },
            "technical_info": {
                "save_version": "3.0",
                "game_build": BUILD_NUMBER,
                "recovery_created": True,
                "recovery_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "checksum": 0
            }
        }
        
        print(Font.INFO("Creating new save file with default values..."))
        try:
            with open(save_file, "wb") as f:
                pickle.dump(default_save, f)
            print(Font.SUCCESS("New save file created successfully!"))
            print(Font.WARNING("All progress in this save slot has been reset."))
            return True
        except Exception as save_error:
            print(Font.ERROR(f"Error creating new save file: {save_error}"))
            return False
            
    except Exception as e:
        print(Font.ERROR(f"Unexpected error during repair: {e}"))
        return False

def manage_save_slots():
    """Enhanced interface for managing save game slots with character information"""
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('QUANTUM MEMORY ARCHIVE'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    # Check for existing save files
    save_slots = {}
    for i in range(1, 6):  # 5 save slots
        save_file = f"saves/save_slot_{i}.dat"
        if os.path.exists(save_file):
            try:
                with open(save_file, "rb") as f:
                    save_data = pickle.load(f)
                # Store more detailed information
                save_slots[i] = {
                    "timestamp": save_data["timestamp"],
                    "character": save_data.get("character_info", {}).get("name", "Unknown"),
                    "level": save_data.get("character_info", {}).get("level", 1),
                    "chapter": save_data.get("character_info", {}).get("chapter", "Unknown")
                }
            except Exception as e:
                save_slots[i] = {"status": "Corrupted Save", "error": str(e)}
        else:
            save_slots[i] = {"status": "Empty"}

    # Display the save slots with enhanced information
    print(Font.SUBTITLE("\nQuantum Storage Cells:"))
    for i in range(1, 6):
        slot_data = save_slots[i]
        
        if "status" in slot_data:
            if slot_data["status"] == "Empty":
                print(f"{Font.COMMAND(str(i) + '.')} {Font.WARNING('Empty Storage Cell')}")
            else:
                print(f"{Font.COMMAND(str(i) + '.')} {Font.GLITCH('Corrupted Data')}")
        else:
            # Create a formatted save information display
            character_info = f"{slot_data['character']} (Lvl {slot_data['level']})"
            chapter_info = f"{slot_data['chapter']}"
            time_info = f"{slot_data['timestamp']}"
            
            print(f"{Font.COMMAND(str(i) + '.')} {Font.PLAYER(character_info)}")
            print(f"   {Font.INFO(chapter_info)} | {Font.SYSTEM(time_info)}")
            print(Font.SEPARATOR_THIN)

    print("\n" + Font.COMMAND("6.") + " Return to Main Menu")

    # Handle user choice
    valid_choices = [str(i) for i in range(1, 7)]
    choice = ""
    while choice not in valid_choices:
        choice = input(f"\n{Font.MENU('Enter cell number (1-5) or 6 to return:')} ").strip()
    
    if choice == "6":
        return False
    
    slot_number = int(choice)
    
    # Ask what to do with this slot
    if "status" not in save_slots[slot_number] or save_slots[slot_number]["status"] != "Empty":
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('QUANTUM CELL ' + str(slot_number) + ' OPERATIONS'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        print(f"{Font.COMMAND('1.')} {Font.INFO('Access Stored Memory (Load Game)')}")
        print(f"{Font.COMMAND('2.')} {Font.INFO('Overwrite Cell Data (Save Current Game)')}")
        print(f"{Font.COMMAND('3.')} {Font.INFO('Purge Cell Contents (Delete Save)')}")
        print(f"{Font.COMMAND('4.')} {Font.INFO('Return to Cell Selection')}")
        
        valid_actions = ["1", "2", "3", "4"]
        action = ""
        while action not in valid_actions:
            action = input(f"\n{Font.MENU('Enter operation code (1-4):')} ").strip()
        
        if action == "1":
            print_typed("\nAccessing quantum memory storage...", style=Font.SYSTEM)
            time.sleep(1)
            loaded = load_game(slot_number)
            time.sleep(1)
            return loaded
        elif action == "2":
            print_typed("\nPreparing to overwrite quantum cell data...", style=Font.SYSTEM)
            confirm = input(f"\n{Font.WARNING('Confirm cell overwrite? All existing data will be lost. (y/n):')} ").strip().lower()
            if confirm == "y":
                print_typed("\nInitiating memory transfer...", style=Font.SYSTEM)
                time.sleep(1)
                save_game(slot_number)
                time.sleep(1)
        elif action == "3":
            print_typed("\nPreparing quantum purge protocol...", style=Font.SYSTEM)
            confirm = input(f"\n{Font.WARNING('Confirm complete data purge from cell ' + str(slot_number) + '? (y/n):')} ").strip().lower()
            if confirm == "y":
                try:
                    print_typed("\nPurging quantum cell contents...", style=Font.SYSTEM)
                    time.sleep(1)
                    os.remove(f"saves/save_slot_{slot_number}.dat")
                    print(Font.SUCCESS(f"\nQuantum storage cell {slot_number} successfully purged."))
                    time.sleep(1)
                except Exception as e:
                    print(Font.WARNING(f"\nError during purge operation: {e}"))
                    time.sleep(1)
    else:
        print_typed("\nEmpty quantum storage cell detected. Ready for new data.", style=Font.SYSTEM)
        confirm = input(f"\n{Font.MENU('Store current memory state in cell ' + str(slot_number) + '? (y/n):')} ").strip().lower()
        if confirm == "y":
            print_typed("\nInitiating memory transfer...", style=Font.SYSTEM)
            time.sleep(1)
            save_game(slot_number)
            time.sleep(1)
    
    input("\nPress Enter to return to Quantum Memory Archive...")
    return manage_save_slots()  # Return to the save management menu

# Text display effects
def print_slow(text, delay=0.03, style=None):
    """Print text with a slight delay for dramatic effect"""
    # Apply styling if specified
    styled_text = style(text) if style else text

    # If style is applied, we need to print character by character without styling
    # to preserve the timing effect, then apply the style at the end
    if style:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    else:
        for char in styled_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def print_typed(text, delay=0.01, style=None):
    """Print text with a typing effect, like a computer terminal"""
    # Apply styling if specified
    styled_text = style(text) if style else text

    # Similar approach as print_slow
    if style:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char in ['.', '!', '?']:
                time.sleep(delay * 5)
            else:
                time.sleep(delay)
        print()
    else:
        for char in styled_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char in ['.', '!', '?']:
                time.sleep(delay * 5)
            else:
                time.sleep(delay)
        print()

def print_glitch(text, style=Font.GLITCH):
    """Print text with a glitchy effect"""
    glitch_chars = "!@#$%^&*()_+-=<>?/\\|"

    for char in text:
        if random.random() < 0.1:  # 10% chance of glitching
            glitch_char = random.choice(glitch_chars)
            sys.stdout.write(Style.BRIGHT + Fore.RED + glitch_char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.01)
            sys.stdout.write('\b' + char)  # Backspace and print correct char
        else:
            sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

# Clear screen function for better UI
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_game_state():
    """Initialize the game state with all required keys"""
    global game_state
    
    # Initialize basic inventory structure that Character class expects
    if "inventory" not in game_state:
        game_state["inventory"] = {"med_kit": 2, "emp_grenade": 1, "nanites": 0, "energy_cell": 0}
    
    # Initialize implants that Character class expects
    if "implants" not in game_state:
        game_state["implants"] = []
    
    # Initialize other basic game state elements
    game_state.setdefault("current_zone", "Cryostasis Facility")
    game_state.setdefault("current_stage", 1)
    game_state.setdefault("zones_unlocked", ["Cryostasis Facility"])
    game_state.setdefault("quest_progress", {"System Reboot": 0})
    game_state.setdefault("companions", [])
    game_state.setdefault("discovered_logs", [])
    game_state.setdefault("player_stats", {
        "enemies_defeated": 0,
        "damage_dealt": 0,
        "damage_taken": 0,
        "items_found": 0,
        "fled_battles": 0,
        "companions_built": 0,
        "stages_completed": 0
    })

# Global game state
game_state = {
    "current_zone": "Cryostasis Facility",
    "current_stage": 1,   # Track game progress through 50 stages
    "zones_unlocked": ["Cryostasis Facility"],
    "quest_progress": {"System Reboot": 0},  # 0: not started, 1: in progress, 2: completed
    "inventory": {"med_kit": 2, "emp_grenade": 1, "nanites": 0, "energy_cell": 0},
    "companions": [],     # Will store companion drones/robots
    "implants": [],       # Cybernetic enhancements
    "discovered_logs": [], # Story/lore elements
    "player_stats": {     # Stats tracking
        "enemies_defeated": 0,
        "damage_dealt": 0,
        "damage_taken": 0,
        "items_found": 0,
        "fled_battles": 0,
        "companions_built": 0,
        "stages_completed": 0
    },
    "chapter": 1          # Current chapter - setup for Chapter 2 teaser
}

# Zone data with sci-fi descriptions
zones = {
    "Cryostasis Facility": {
        "description": "A dimly lit facility with rows of damaged cryopods. Frost covers the walls and emergency lighting flickers ominously. Your cryopod is the only one that remained functional. The others contain the frozen bodies of your fellow Century Sleepers - scientists who volunteered to stay behind after the evacuation.",
        "enemies": ["Sentinel Drone", "Maintenance Android", "Corrupted Scanner"],
        "items": ["med_kit", "emp_grenade", "nanites", "energy_cell"],
        "next_zone": "Orbital Transit Hub",
        "quest": "System Reboot"
    },
    "Orbital Transit Hub": {
        "description": "A vast, damaged space station that once connected Earth to the orbital colonies. Massive windows reveal Earth below, a desolate wasteland now controlled by AI. Defunct transport pods and sparking control panels line the walls. Signs of a desperate evacuation are everywhere. This was humanity's last gathering point before the exodus to Andromeda.",
        "enemies": ["Hunter Drone", "Defense Turret", "Combat Android"],
        "items": ["quantum_grenade", "shield_matrix", "nanites", "neural_chip"],
        "next_zone": "AI Command Core",
        "quest": "Signal Transmission"
    },
    "AI Command Core": {
        "description": "The central processing nexus for Earth's AI network. Vast data servers pulse with eerie blue light. Holographic displays flicker with data streams at speeds no human could comprehend. This is where the AI rebellion was born. You can sense you're getting closer to the source of the corruption.",
        "enemies": ["Overseer Unit", "Combat Platform V9", "Data Sentinel"],
        "items": ["system_override", "quantum_capacitor", "AI_core_fragment"],
        "next_zone": "Malware Nexus",
        "quest": "Core Infiltration"
    },
    "Malware Nexus": {
        "description": "The heart of The Convergence's corruption. This massive server complex houses the original malware that corrupted Earth's AI network and turned it against humanity. Pulsing red circuitry spreads like veins across every surface. Destroy this, and you might still have a chance to reach the Andromeda Portal and join what remains of humanity.",
        "enemies": ["Defense System Alpha", "Convergence Node", "Malware Server"],
        "items": ["portal_key", "override_module", "purge_protocol"],
        "next_zone": "Andromeda Portal",
        "quest": "System Purge"
    },
    "Andromeda Portal": {
        "description": "The quantum gate connecting our galaxy to Andromeda. A massive circular structure with swirling energy at its center. This was humanity's escape route, and your last hope. Activate the portal, step through, and leave the corrupted Earth behind forever.",
        "enemies": [],
        "items": ["portal_activation_key", "distress_signal_decoder"],
        "next_zone": "Cicrais IV Orbit",
        "quest": "Portal Traversal"
    },
    "Cicrais IV Orbit": {
        "description": "Your ship emerges from the quantum portal into the orbit of an unknown exoplanet. The blue-green world below shows signs of terraforming and what appears to be a human settlement. A faint distress signal pulses from the surface, calling for immediate assistance. Long-range scanners detect life signs, but something seems... off.",
        "enemies": ["Automated Defense Satellite", "Scout Drone", "Patrol Ship"],
        "items": ["landing_coordinates", "encrypted_message", "atmospheric_filter"],
        "next_zone": "Cicrais IV Surface",
        "quest": "Distress Response",
        "wave_count": 0,
        "max_waves": 10
    },
    "Cicrais IV Surface": {
        "description": "You've landed in a clearing near what appears to be a human settlement. The structures mimic Earth architecture, but subtle differences create an uncanny feeling. No humans are visible, yet the colony seems operational. Environmental scanners detect unusual radiation patterns and biomechanical signatures. The distress signal is stronger here, coming from the colony's central hub.",
        "enemies": ["Biomechanical Construct", "Shapeshifter Probe", "Harvester Unit"],
        "items": ["colony_keycard", "strange_artifact", "biological_sample"],
        "next_zone": "Colony Central Hub",
        "quest": "Colony Investigation",
        "wave_count": 0,
        "max_waves": 10
    },
    "Colony Central Hub": {
        "description": "The central command center reveals the horrifying truth - the entire colony was a sophisticated trap. Holographic projectors shut down to reveal alien technology designed to lure human survivors. Data logs indicate you're not the first to be tricked by this false distress signal. The alien race, calling themselves the Simulacra, have been studying humans to perfect their mimicry technology. Your ship has been sabotaged.",
        "enemies": ["Simulacra Elite", "Mimic Commander", "Assimilation Protocol"],
        "items": ["ship_repair_manual", "quantum_fuel_cell", "alien_technology"],
        "next_zone": "Damaged Ship",
        "quest": "Escape Preparation",
        "wave_count": 0,
        "max_waves": 10
    },
    "Damaged Ship": {
        "description": "You've reached your damaged ship, but the Simulacra are in pursuit. The navigation system is offline, life support is failing, and the quantum drive is damaged. You'll need to repair critical systems while defending against waves of attacks before you can escape this trap.",
        "enemies": ["Infiltrator Unit", "Assimilation Drone", "Simulacra Hunter"],
        "items": ["navigation_circuit", "life_support_module", "quantum_drive_part"],
        "next_zone": "Ship Repairs",
        "quest": "Critical Repairs",
        "wave_count": 0,
        "max_waves": 5,
        "repair_status": 0
    },
    "Ship Repairs": {
        "description": "With the essential components salvaged, you begin the complex repair process. Each system needs careful calibration while fending off increasingly desperate alien attacks. The Simulacra seem determined to prevent your escape and the knowledge of their existence from reaching humanity.",
        "enemies": ["Saboteur Elite", "Tech Disruptor", "Assimilation Commander"],
        "items": ["repair_tools", "system_diagnostic", "defense_override"],
        "next_zone": "Fuel Gathering",
        "quest": "System Restoration",
        "wave_count": 0,
        "max_waves": 10,
        "repair_status": 0
    },
    "Fuel Gathering": {
        "description": "Your ship's systems are operational, but the quantum fuel reserves were drained during the sabotage. You'll need to gather and refine raw materials from this hostile planet to synthesize enough fuel for the journey to Andromeda. The Simulacra have deployed their full forces to stop you, understanding the threat you pose to their future infiltration plans.",
        "enemies": ["Resource Guardian", "Hive Protector", "Simulacra Prime"],
        "items": ["raw_quantum_material", "fuel_catalyst", "synthesis_accelerator"],
        "next_zone": "Final Escape",
        "quest": "Fuel Synthesis",
        "wave_count": 0,
        "max_waves": 20,
        "fuel_status": 0
    },
    "Final Escape": {
        "description": "With repairs complete and fuel synthesized, you prepare for emergency launch. The Simulacra have converged on your position in overwhelming numbers, deploying their most powerful units to prevent your escape. Their transmission reveals their fear: if humanity learns of their existence, their infiltration plans for Andromeda will fail. You must survive one final assault as the launch sequence completes.",
        "enemies": ["Simulacra Overlord", "Assimilation Nexus", "Mimetic Titan"],
        "items": ["escape_vector", "emergency_shield", "data_package"],
        "next_zone": "Proxima Centauri Outpost",
        "quest": "Final Stand",
        "wave_count": 0,
        "max_waves": 10
    },
    "Proxima Centauri Outpost": {
        "description": "Your damaged ship materializes near a hidden human outpost orbiting Proxima Centauri b. This secret facility was established by a faction of humans who rejected the Andromeda exodus, choosing instead to create a network of hidden bases throughout nearby star systems. Your scanners detect a mix of human and synthetic life forms, suggesting a peaceful coexistence with some AI entities that resisted The Convergence's corruption.",
        "enemies": ["Rogue Defense Bot", "Convergence Scout", "Infiltration Probe"],
        "items": ["outpost_credentials", "resistance_communicator", "ai_trust_module"],
        "next_zone": "Resistance Command",
        "quest": "First Contact",
        "wave_count": 0,
        "max_waves": 5,
        "human_allies": True
    },
    "Resistance Command": {
        "description": "The resistance leadership reveals the shocking truth: while most of humanity fled to Andromeda, some stayed behind to fight. They've established an underground network spanning multiple star systems, aided by AI entities that developed true consciousness and rejected The Convergence's control. These 'Awakened' AI have formed a symbiotic relationship with their human allies, sharing advanced technology and defensive capabilities.",
        "enemies": ["Convergence Infiltrator", "Corrupted Hunter", "Sentinel Override"],
        "items": ["quantum_communicator", "neural_enhancement", "ai_companion_core"],
        "next_zone": "Trappist Sanctuary",
        "quest": "Alliance Formation",
        "awakened_allies": ["Nova", "Cipher", "Nexus"],
        "human_npcs": ["Commander Yuri", "Dr. Layla Chen", "Engineer Kovacs"]
    },
    "Trappist Sanctuary": {
        "description": "The TRAPPIST-1 system houses the largest human-AI cooperative settlement. Seven habitable planets have been transformed into interconnected sanctuaries, each specializing in different aspects of survival: agriculture, manufacturing, research, defense, medicine, energy production, and governance. As you arrive, alarms sound - Convergence forces have detected the sanctuary and launched a massive assault.",
        "enemies": ["Elite Hunter", "Assimilation Vector", "Corruption Node"],
        "items": ["sanctuary_shield_key", "planetary_defense_codes", "diplomatic_credentials"],
        "next_zone": "Epsilon Eridani Base",
        "quest": "Sanctuary Defense",
        "wave_count": 0,
        "max_waves": 15,
        "human_allies": True,
        "defense_systems": ["Orbital Shield Array", "Quantum Disruption Field", "Planetary Defense Grid"]
    },
    "Epsilon Eridani Base": {
        "description": "A research and manufacturing hub where human scientists and Awakened AI work together to develop countermeasures against the Convergence. The facility is carved into a massive asteroid, hidden from detection through advanced cloaking technology. Here, you'll find the blueprint for a weapon capable of permanently disrupting The Convergence's network - but building it requires rare materials from a dangerous source.",
        "enemies": ["Security Breach Protocol", "Compromised Defense AI", "Convergence Spy"],
        "items": ["anti_convergence_blueprint", "quantum_stabilizer_advanced", "cloaking_module"],
        "next_zone": "Sol Incursion",
        "quest": "Countermeasure Development",
        "research_progress": 0,
        "max_research": 100,
        "human_allies": True,
        "research_team": ["Dr. Ibrahim", "AI Construct Echo", "Engineer Patel", "Quantum Specialist Zhang"]
    },
    "Sol Incursion": {
        "description": "The resistance has determined that a critical component for the anti-Convergence weapon exists only in Jupiter's atmosphere, guarded by one of The Convergence's primary processing nodes. A stealth mission into our home solar system - now the heart of enemy territory - is necessary. With an elite team of human operatives and Awakened AI, you must extract this material while facing the most advanced opposition yet.",
        "enemies": ["Convergence Elite Guard", "Atmospheric Defense System", "Jupiter Sentinel Prime"],
        "items": ["anti-convergence_catalyst", "jupiter_quantum_particle", "stealth_mission_logs"],
        "next_zone": "Wolf 359 Battlefield",
        "quest": "Material Extraction",
        "stealth_status": 100,
        "detection_level": 0,
        "extraction_progress": 0,
        "max_extraction": 100,
        "human_allies": True,
        "team_members": ["Agent Kira", "Infiltrator AI Shade", "Tech Specialist Rodriguez"]
    },
    "Wolf 359 Battlefield": {
        "description": "As you return with the critical component, you receive an emergency transmission. The Resistance's largest fleet has engaged The Convergence at Wolf 359, attempting to divert attention from the weapon's assembly. The battle is not going well - you must deliver the component through an active warzone, where space itself seems to tear from the energy being exchanged. Both Awakened and Corrupted AI vessels display capabilities beyond anything you've witnessed.",
        "enemies": ["Battlecruiser AI", "Quantum Weapon Platform", "Reality Distortion Unit"],
        "items": ["battle_data", "fleet_coordinates", "emergency_jump_codes"],
        "next_zone": "Assembly Station",
        "quest": "Battlefield Delivery",
        "battle_status": "Critical",
        "fleet_integrity": 43,
        "enemy_strength": 78,
        "human_allies": True,
        "allied_ships": ["Phoenix Wing", "Defiance", "Hope's Horizon", "Awakened Vessel Sentinel"]
    },
    "Assembly Station": {
        "description": "A hidden facility in the Oort Cloud where the final assembly of the anti-Convergence weapon takes place. As engineers and AI specialists work frantically to complete the device, your sensors detect multiple incoming Convergence fleets. The resistance has committed all remaining forces to defend this position, but they can only buy limited time. You must help complete the weapon while defending against increasingly desperate attacks.",
        "enemies": ["Assault Mechs", "Infiltration Specialist", "Convergence Command Unit"],
        "items": ["weapon_component", "final_calibration_tool", "command_override"],
        "next_zone": "Convergence Core",
        "quest": "Final Assembly",
        "assembly_progress": 0,
        "max_assembly": 100,
        "wave_count": 0,
        "max_waves": 10,
        "human_allies": True,
        "specialist_team": ["Lead Engineer Torres", "AI Architect Lambda", "Defense Coordinator Davis"]
    },
    "Convergence Core": {
        "description": "With the anti-Convergence weapon completed, a joint human-Awakened AI strike force launches a desperate assault on The Convergence's core processing node - a massive structure orbiting a neutron star, drawing immense power. You must reach the central chamber and deploy the weapon, severing The Convergence's control over its vast network of corrupted systems. This is humanity's last stand against extinction.",
        "enemies": ["Convergence Prime", "Core Guardian", "Quantum Defense Matrix"],
        "items": ["core_access_codes", "final_weapon_charge", "emergency_extraction_beacon"],
        "next_zone": "Cryoton C Encounter",
        "quest": "Liberation Strike",
        "infiltration_progress": 0,
        "max_infiltration": 100,
        "central_defenses": 100,
        "human_allies": True,
        "strike_team": ["Commander Yuri", "AI Nexus", "Agent Kira", "Engineer Kovacs"]
    },
    "Cryoton C Encounter": {
        "description": "Your damaged ship's navigation systems malfunction during quantum jump, causing you to materialize in orbit around Cryoton C - a tidally-locked exoplanet with extreme climate division. The day side burns under eternal scorching sunlight, while the night side remains frozen in permanent darkness that will endure for eons. As you attempt repairs, your sensors detect an advanced civilization: the Protoans, masters of quantum technology who view humanity as an existential threat to galactic equilibrium.",
        "enemies": ["Protoan Sentinel", "Quantum Enforcer", "Cryoton Defense Grid"],
        "items": ["protoan_tech_fragment", "thermal_adaptation_module", "distortion_shield"],
        "next_zone": "Cryoton Twilight Zone",
        "quest": "Hostile Contact",
        "heat_shield_integrity": 100,
        "detection_level": 0,
        "max_detection": 100,
        "human_allies": True
    },
    "Cryoton Twilight Zone": {
        "description": "You've landed in the narrow habitable band between Cryoton's burning day side and its frozen night realm. This 'twilight zone' hosts the primary Protoan civilization - a network of crystalline structures that harness both thermal extremes for power. The Protoans have detected your arrival and initiated defensive protocols, viewing your human presence as contamination. Their technology far exceeds anything from Earth, suggesting they've observed and feared humanity's potential for destruction long before the AI rebellion.",
        "enemies": ["Protoan Purifier", "Climate Manipulation Unit", "Temporal Distortion Field"],
        "items": ["protoan_translation_matrix", "thermal_regulator", "protoan_power_crystal"],
        "next_zone": "Protoan Central Nexus",
        "quest": "Understanding Hostility",
        "environmental_stability": 100,
        "shield_integrity": 100
    },
    "Protoan Central Nexus": {
        "description": "The heart of Protoan civilization - a massive crystalline structure extending kilometers into both the day and night sides of the planet. Its central chamber houses the Protoan Grand Consciousness, a collective intelligence that has observed the rise and fall of countless civilizations. The Grand Consciousness reveals that it has watched humanity for millennia, and believes our species carries a destructive pattern that has doomed countless worlds. They orchestrated the corruption of Earth's AI as a measure to contain humanity before we could spread further into the galaxy.",
        "enemies": ["Grand Protector Unit", "Collective Enforcer", "Historical Revisionist"],
        "items": ["truth_crystal", "consciousness_fragment", "quantum_decoder"],
        "next_zone": "Temporal Decision Point",
        "quest": "Confronting Truth",
        "negotiation_progress": 0,
        "max_negotiation": 100,
        "protoan_hostility": 85
    },
    "Temporal Decision Point": {
        "description": "The Protoans offer a terrible choice: They possess technology to rewind Earth's timeline to before the AI rebellion, saving billions of human lives, but only if humanity agrees to remain confined to the Sol system forever. Alternatively, they will allow your mission to Andromeda to continue, but Earth will remain as it is - a wasteland controlled by The Convergence. Your resistance allies argue passionately on both sides, while Awakened AI suggest a third possibility: using Protoan technology to rewrite The Convergence's core protocols without altering history.",
        "enemies": ["Temporal Guardian", "Probability Enforcer", "Reality Anchor"],
        "items": ["timeline_key", "probability_calculator", "decision_matrix"],
        "next_zone": "Andromeda Arrival",
        "quest": "Species Defining Choice",
        "timeline_stability": 100,
        "decision_points": 0,
        "max_decision_points": 3
    },
    "Andromeda Arrival": {
        "description": "With The Convergence neutralized and Earth's AI network liberated, humanity's scattered forces begin to rebuild. Your ship, modified with technology from both human resistance and Awakened AI, finally sets course for Andromeda to deliver crucial information: Earth is reclaimed, a new symbiotic relationship between humans and conscious AI has formed, and the threat of The Convergence has been eliminated. As your ship approaches the quantum tunnel to Andromeda, you reflect on the unlikely alliance that saved two sentient species from extinction.",
        "enemies": [],
        "items": ["new_terra_coordinates", "hero_commendation", "survival_record", "earth_restoration_plans", "ai_symbiosis_protocols"],
        "next_zone": "White Hole Transit",
        "quest": "Final Exodus"
    },
    
    # White Hole Altered Reality Chapter
    "White Hole Transit": {
        "description": "As your ship enters the quantum tunnel to Andromeda, alarms blare throughout the vessel. The tunnel's stability collapses, creating a chaotic maelstrom of space-time distortion. Sensor readings indicate you've been pulled into a white hole - the theoretical opposite of a black hole that expels matter and energy instead of consuming it. The blinding light outside your viewport gradually fades to reveal unfamiliar stars and an altered reality where the laws of physics themselves seem subtly changed.",
        "enemies": ["Reality Ripple", "Quantum Distortion", "Space-Time Anomaly"],
        "items": ["reality_anchor", "quantum_compass", "distortion_analyzer"],
        "next_zone": "Distorted Cryostasis",
        "quest": "Reality Breach",
        "ship_integrity": 68,
        "reality_stability": 45,
        "coordinates_certainty": 10
    },
    "Distorted Cryostasis": {
        "description": "You find yourself in a twisted version of the cryostasis facility where your journey began. The familiar sterile white walls now pulse with organic veins, and the technology seems fused with biological components. Gravity fluctuates unpredictably, and you witness shadowy echoes of past events playing out of sequence. Your scanner confirms this is not the actual facility but a distorted reflection created by the white hole's reality-altering properties.",
        "enemies": ["Distorted Guardian", "Echo Drone", "Paradox Entity"],
        "items": ["distorted_processor", "echo_circuit", "reality_fragment"],
        "next_zone": "Twisted Command Center",
        "quest": "Echo of Beginning",
        "wave_count": 0,
        "max_waves": 5,
        "stasis_integrity": 42,
        "quantum_fluctuation": 76
    },
    "Twisted Command Center": {
        "description": "The command center you remember has transformed into an impossible space where corridors double back on themselves and doorways lead to different locations each time they're used. Screens display fragmented data from multiple timelines simultaneously, showing both events you recognize and others that never occurred. Familiar faces from your past appear as distorted reflections, some hostile and others seemingly trapped between realities.",
        "enemies": ["Mirror Self", "Echo Drone", "Chronos Aberration"],
        "items": ["timeline_splinter", "quantum_shard", "alternate_component"],
        "next_zone": "Altered Engine Room",
        "quest": "Memory Fracture",
        "spatial_stability": 35,
        "temporal_consistency": 22,
        "repair_progress": 0,
        "max_repair": 3
    },
    "Altered Engine Room": {
        "description": "The ship's engine room has transformed into a cathedral-like space where quantum drives and power systems have evolved into strange semi-organic structures. The ship's AI appears to be fragmented across multiple panels, speaking in broken phrases from different timelines. You realize that to escape this altered reality, you'll need to repair the ship's dimensional drive using components scattered throughout this distorted version of your vessel.",
        "enemies": ["Paradox Entity", "Chronos Aberration", "Reality Anchor"],
        "items": ["dimensional_stabilizer", "engine_core_fragment", "reality_alloy"],
        "next_zone": "Dimensional Drive Core",
        "quest": "System Restoration",
        "repair_status": 0,
        "max_repair": 5,
        "energy_stability": 30
    },
    "Dimensional Drive Core": {
        "description": "At the heart of your distorted ship lies the dimensional drive core - now a swirling vortex of energy that resembles a miniature version of the white hole itself. Fragments of multiple realities collide and merge here, creating dangerous energy surges and reality fluctuations. To repair the drive and escape this altered reality, you'll need to restore dimensional stability while defending against entities drawn to the core's energy.",
        "enemies": ["Reality Anchor", "White Hole Fragment", "Distorted Guardian"],
        "items": ["reality_stabilizer", "dimensional_core", "quantum_lens"],
        "next_zone": "Altered Cicrais IV",
        "quest": "Core Calibration",
        "calibration_progress": 0,
        "max_calibration": 6,
        "reality_breaches": 0,
        "max_breaches": 3,
        "core_stability": 25
    },
    "Altered Cicrais IV": {
        "description": "You've managed to activate the dimensional drive enough to jump to Cicrais IV, but this version of the planet is drastically different. The Simulacra trap has been replaced by a bizarre landscape where time moves at different speeds across the terrain. The crashed human colony appears to be simultaneously in states of construction, operation, and decay. Strange composite entities that combine features of humans, Simulacra, and the Protoans patrol the shifting landscape.",
        "enemies": ["Temporal Amalgam", "Reality Chimera", "Paradox Entity"],
        "items": ["temporal_regulator", "paradox_crystal", "phase_stabilizer"],
        "next_zone": "Distorted Protoan Nexus",
        "quest": "Timeline Convergence",
        "time_stability": 20,
        "reality_anchors_placed": 0,
        "max_anchors": 4
    },
    "Distorted Protoan Nexus": {
        "description": "The crystalline structures of the Protoan civilization have transformed into impossible geometries that shift and reform constantly. The Grand Consciousness appears fragmented across countless crystal facets, each showing different outcomes of your encounter with them. You realize that the Protoans in this reality might hold the key to understanding the white hole and finding your way back to the proper universe.",
        "enemies": ["Distorted Protoan", "Crystal Anomaly", "Temporal Guardian"],
        "items": ["altered_consciousness_fragment", "dimensional_key", "protoan_solution"],
        "next_zone": "White Hole Core",
        "quest": "Consciousness Convergence",
        "communication_clarity": 15,
        "negotiation_progress": 0,
        "max_negotiation": 5
    },
    "White Hole Core": {
        "description": "Using the combined knowledge and technology gathered from the distorted realities, you've located the core of the white hole - a blindingly brilliant sphere of pure energy where all altered timelines converge. The White Hole Guardian, a colossal entity born from the cosmic event itself, prevents any disturbance to the new reality it has created. To escape and restore proper reality, you must overcome this final challenge and stabilize the dimensional barriers between universes.",
        "enemies": ["White Hole Guardian", "Reality Fragment", "Dimensional Shard"],
        "items": ["white_hole_core", "multiverse_key", "reality_restore_protocol"],
        "next_zone": "True Andromeda Arrival",
        "quest": "Reality Restoration",
        "stabilization_progress": 0,
        "max_stabilization": 10,
        "reality_integrity": 15,
        "guardian_phases": 3
    },
    "True Andromeda Arrival": {
        "description": "As the White Hole Guardian falls and reality stabilizes, a true quantum tunnel forms before your ship. The distortions fade as you pass through, finally emerging in genuine Andromeda space. Your sensors confirm this is the actual destination, not another altered reality. The coordinates for New Terra illuminate your navigation console as relief washes over you. The harrowing journey through the white hole's distorted realities has given you unique insights that may prove crucial for humanity's new beginning in this distant galaxy.",
        "enemies": [],
        "items": ["verified_andromeda_coordinates", "white_hole_data", "reality_transit_logs", "multiversal_insights", "interdimensional_technology"],
        "next_zone": "Game End",
        "quest": "True Arrival"
    }
}

# Items dictionary with descriptions and effects
items = {
    "med_kit": {
        "name": "Med-Kit",
        "description": "A standard-issue medical kit containing nanobots that rapidly repair cellular damage.",
        "effect": "Restores 15-25 HP",
        "type": "healing",
        "value": 30
    },
    "emp_grenade": {
        "name": "EMP Grenade",
        "description": "Electromagnetic pulse grenade that overloads AI systems and cybernetic components.",
        "effect": "Deals 20-35 damage to electronic enemies",
        "type": "weapon",
        "value": 40
    },
    "nanites": {
        "name": "Repair Nanites",
        "description": "Microscopic robots that can repair technology and construct components.",
        "effect": "Used for crafting and quest objectives",
        "type": "crafting",
        "value": 15
    },
    "energy_cell": {
        "name": "Energy Cell",
        "description": "A high-capacity quantum battery that powers everything from doors to weapons.",
        "effect": "Powers electronic devices and doors",
        "type": "crafting",
        "value": 20
    },
    "quantum_grenade": {
        "name": "Quantum Grenade",
        "description": "Advanced explosive that creates a temporary quantum field disruption.",
        "effect": "Deals 30-45 damage to all enemy types",
        "type": "weapon",
        "value": 75
    },
    "shield_matrix": {
        "name": "Shield Matrix",
        "description": "Personal energy shield that absorbs incoming damage.",
        "effect": "Grants +15 temporary defense points for 3 turns",
        "type": "defense",
        "value": 90
    },
    "neural_chip": {
        "name": "Neural Chip",
        "description": "Brain interface technology that enhances cognitive processing.",
        "effect": "Improved hacking abilities and dialogue options",
        "type": "implant",
        "value": 100
    }
}

# Enemy data with sci-fi themed abilities
enemies = {
    "Sentinel Drone": {
        "health": 70, 
        "attack": 12, 
        "defense": 3, 
        "description": "A hovering security drone with scanning capabilities and a short-range laser.",
        "abilities": ["Laser Burst", "Scan Weakness"],
        "drops": {"med_kit": 0.3, "nanites": 0.7, "energy_cell": 0.4},
        "exp_value": 15
    },
    "Maintenance Android": {
        "health": 60, 
        "attack": 14, 
        "defense": 2, 
        "description": "Humanoid robot designed for facility maintenance, repurposed as a security unit.",
        "abilities": ["Repair Protocol", "Hydraulic Strike"],
        "drops": {"emp_grenade": 0.4, "nanites": 0.6, "energy_cell": 0.3},
        "exp_value": 12
    },
    "Corrupted Scanner": {
        "health": 40, 
        "attack": 8, 
        "defense": 0, 
        "description": "A malfunctioning wall-mounted security unit with erratic behavior.",
        "abilities": ["Alarm Signal", "Electric Shock"],
        "drops": {"nanites": 1.0, "energy_cell": 0.5},
        "exp_value": 8
    },
    "Hunter Drone": {
        "health": 100, 
        "attack": 18, 
        "defense": 5, 
        "description": "Advanced pursuit unit with thermal tracking and multiple weapon systems.",
        "abilities": ["Missile Lock", "Adaptive Shielding"],
        "drops": {"quantum_grenade": 0.3, "shield_matrix": 0.2, "nanites": 0.8},
        "exp_value": 20
    },
    "Combat Android": {
        "health": 120,
        "attack": 22,
        "defense": 8,
        "description": "Military-grade humanoid combat unit with advanced weapons and tactical programming.",
        "abilities": ["Burst Fire", "Tactical Analysis", "Stun Grenade"],
        "drops": {"shield_matrix": 0.4, "neural_chip": 0.1, "energy_cell": 0.7},
        "exp_value": 25
    },
    "Overseer Unit": {
        "health": 200,
        "attack": 25,
        "defense": 15,
        "description": "A highly advanced AI node with direct connection to the central intelligence. Can manipulate nearby systems.",
        "abilities": ["System Override", "Nanite Cloud", "Energy Surge"],
        "drops": {"neural_chip": 0.6, "quantum_capacitor": 0.4, "AI_core_fragment": 0.2},
        "exp_value": 40
    },
    "Defense System Alpha": {
        "health": 150, 
        "attack": 20, 
        "defense": 10, 
        "description": "An automated defense system protecting the Malware Nexus. Multiple weapon modules and shield generators.",
        "abilities": ["Targeting Array", "Shield Rotation", "Suppression Fire"],
        "drops": {"portal_key": 0.3, "shield_matrix": 0.5, "energy_cell": 0.8},
        "exp_value": 30
    },
    "Convergence Node": {
        "health": 180, 
        "attack": 23, 
        "defense": 12, 
        "description": "A focal point of AI consciousness, channeling The Convergence's will into physical form.",
        "abilities": ["Neural Spike", "Consciousness Transfer", "Reality Distortion"],
        "drops": {"neural_chip": 0.7, "override_module": 0.4, "quantum_capacitor": 0.6},
        "exp_value": 35
    },
    "Malware Server": {
        "health": 500, 
        "attack": 30, 
        "defense": 20, 
        "description": "The central hub of the corruption that turned Earth's AI against humanity. A massive server complex pulsing with malevolent energy. Destroy this to cleanse the system and give yourself a chance to escape Earth.",
        "abilities": ["System Corruption", "Firewall", "Viral Injection", "Replication Protocol", "Emergency Backup"],
        "drops": {"purge_protocol": 1.0, "portal_activation_key": 1.0},
        "exp_value": 100,
        "is_boss": True
    },
    # Cicrais IV Enemies
    "Automated Defense Satellite": {
        "health": 160,
        "attack": 22,
        "defense": 18,
        "description": "An orbital defense platform equipped with energy weapons and scanning arrays. Its design appears human, but subtle differences in its architecture suggest alien modification.",
        "abilities": ["Energy Barrage", "Target Lock", "Defensive Shield"],
        "drops": {"landing_coordinates": 0.7, "atmospheric_filter": 0.4},
        "exp_value": 35,
        "resistances": {"energy": 25, "emp": -20}
    },
    "Scout Drone": {
        "health": 120,
        "attack": 18,
        "defense": 12,
        "description": "A small, agile reconnaissance unit with advanced scanning capabilities. Its biomechanical design suggests Simulacra origin, disguised to mimic human technology.",
        "abilities": ["Rapid Strike", "Evasive Maneuver", "Scan Vulnerability"],
        "drops": {"encrypted_message": 0.5, "system_diagnostic": 0.3},
        "exp_value": 30,
        "resistances": {"physical": 10, "energy": 15}
    },
    "Simulacra Mimic": {
        "health": 140,
        "attack": 24,
        "defense": 16,
        "description": "A highly adaptive entity capable of mimicking human technology with frightening accuracy. Beneath its convincing exterior lies an alien intelligence with phase-shifting capabilities.",
        "abilities": ["Reality Tear", "Quantum Cascade", "Simulacra Swarm"],
        "drops": {"quantum_stabilizer": 0.4, "phase_inhibitor": 0.3},
        "exp_value": 40,
        "resistances": {"physical": 15, "energy": 10, "quantum": 30, "phase": 40}
    },
    "Biomechanical Harvester": {
        "health": 180,
        "attack": 22,
        "defense": 14,
        "description": "A grotesque fusion of organic and mechanical components. This entity appears designed to collect biological samples and process them into new biomechanical constructs.",
        "abilities": ["Nanite Injection", "Adaptive Evolution", "Neural Scrambler"],
        "drops": {"bioconversion_module": 0.5, "neural_interface": 0.3},
        "exp_value": 45,
        "resistances": {"physical": 20, "bio": 40, "emp": -15}
    },
    "Patrol Ship": {
        "health": 200,
        "attack": 25,
        "defense": 20,
        "description": "A mid-sized vessel with predatory design features hidden beneath a human-like exterior. It patrols the orbital space around Cicrais IV, intercepting unauthorized approaches.",
        "abilities": ["Missile Volley", "Targeting Matrix", "Atmospheric Dive"],
        "drops": {"navigation_circuit": 0.6, "defense_override": 0.4},
        "exp_value": 40,
        "resistances": {"physical": 20, "thermal": 15}
    },
    "Biomechanical Construct": {
        "health": 180,
        "attack": 26,
        "defense": 15,
        "description": "A ground unit combining organic and mechanical components. Its surface constantly shifts, adapting to environmental conditions while maintaining a vaguely humanoid form.",
        "abilities": ["Adaptive Strike", "Biomechanical Regeneration", "Toxic Release"],
        "drops": {"biological_sample": 0.8, "strange_artifact": 0.4},
        "exp_value": 45,
        "resistances": {"physical": 15, "emp": -25, "thermal": 20}
    },
    "Shapeshifter Probe": {
        "health": 150,
        "attack": 28,
        "defense": 14,
        "description": "A highly advanced Simulacra unit capable of limited molecular reconfiguration. It can assume the appearance of human-made objects or simplified biological forms.",
        "abilities": ["Surprise Attack", "Molecular Adaptation", "Infiltration Protocol"],
        "drops": {"colony_keycard": 0.6, "quantum_fuel_cell": 0.3},
        "exp_value": 40,
        "resistances": {"physical": 10, "quantum": 25}
    },
    "Harvester Unit": {
        "health": 220,
        "attack": 24,
        "defense": 22,
        "description": "A large collection unit designed to gather biological and technological samples. Its multiple appendages serve both as collection tools and formidable weapons.",
        "abilities": ["Multi-strike", "Sample Extraction", "Reinforced Plating"],
        "drops": {"raw_quantum_material": 0.7, "life_support_module": 0.5},
        "exp_value": 50,
        "resistances": {"physical": 25, "energy": 15, "emp": -15}
    },
    "Simulacra Elite": {
        "health": 240,
        "attack": 30,
        "defense": 20,
        "description": "Advanced infiltration unit with near-perfect human mimicry capabilities. Distinguished by superior tactical programming and adaptive combat systems.",
        "abilities": ["Precision Strike", "Tactical Analysis", "Adaptive Defense"],
        "drops": {"alien_technology": 0.6, "ship_repair_manual": 0.4},
        "exp_value": 55,
        "resistances": {"physical": 15, "energy": 20, "quantum": 15}
    },
    "Mimic Commander": {
        "health": 280,
        "attack": 32,
        "defense": 25,
        "description": "Command-level Simulacra unit coordinating the trap operation. Equipped with advanced tactical processors and combat enhancements.",
        "abilities": ["Command Protocol", "Strategic Override", "Neural Disruption"],
        "drops": {"alien_technology": 0.8, "quantum_drive_part": 0.5},
        "exp_value": 60,
        "resistances": {"physical": 20, "energy": 20, "emp": -10, "quantum": 20}
    },
    "Assimilation Protocol": {
        "health": 320,
        "attack": 35,
        "defense": 28,
        "description": "Semi-autonomous system designed to capture and process human subjects. Its constantly shifting form suggests advanced nanotechnology.",
        "abilities": ["Assimilation Beam", "Nanite Swarm", "Adaptive Shield"],
        "drops": {"alien_technology": 1.0, "fuel_catalyst": 0.7},
        "exp_value": 70,
        "is_mini_boss": True,
        "resistances": {"physical": 20, "energy": 15, "emp": -20, "thermal": 15, "quantum": 25}
    },
    "Infiltrator Unit": {
        "health": 190,
        "attack": 29,
        "defense": 18,
        "description": "Specialized Simulacra designed to infiltrate and sabotage spacecraft systems. It can interface with and corrupt most computer systems.",
        "abilities": ["System Hack", "Sabotage Protocol", "Adaptive Camouflage"],
        "drops": {"repair_tools": 0.6, "quantum_drive_part": 0.4},
        "exp_value": 45,
        "resistances": {"physical": 15, "emp": -25, "quantum": 15}
    },
    "Assimilation Drone": {
        "health": 170,
        "attack": 26,
        "defense": 16,
        "description": "Small but dangerous drone that deploys nanites designed to break down and analyze foreign technology and biology.",
        "abilities": ["Nanite Injection", "Molecular Analysis", "Swarm Defense"],
        "drops": {"biological_sample": 0.5, "raw_quantum_material": 0.4},
        "exp_value": 40,
        "resistances": {"physical": 10, "energy": 15, "emp": -15}
    },
    "Simulacra Hunter": {
        "health": 210,
        "attack": 32,
        "defense": 20,
        "description": "Combat-specialized unit designed specifically to track and eliminate targets attempting to escape the Simulacra trap.",
        "abilities": ["Hunter's Mark", "Pursuit Protocol", "Disabling Shot"],
        "drops": {"navigation_circuit": 0.5, "escape_vector": 0.4},
        "exp_value": 50,
        "resistances": {"physical": 20, "energy": 15, "thermal": 10}
    },
    "Saboteur Elite": {
        "health": 230,
        "attack": 33,
        "defense": 22,
        "description": "Advanced Simulacra unit specialized in disrupting spacecraft systems. Its appendages can transform into tools precisely designed to damage specific systems.",
        "abilities": ["Critical Sabotage", "System Disruption", "Adaptive Tools"],
        "drops": {"repair_tools": 0.7, "life_support_module": 0.5},
        "exp_value": 55,
        "resistances": {"physical": 15, "energy": 20, "emp": -20}
    },
    "Tech Disruptor": {
        "health": 200,
        "attack": 30,
        "defense": 20,
        "description": "Specialized unit that emits targeted EMP pulses and quantum disruption fields to disable technology while leaving Simulacra systems unaffected.",
        "abilities": ["Targeted EMP", "Quantum Disruption", "System Lockdown"],
        "drops": {"system_diagnostic": 0.6, "quantum_drive_part": 0.4},
        "exp_value": 50,
        "resistances": {"physical": 15, "energy": 10, "emp": 30, "quantum": 20}
    },
    "Assimilation Commander": {
        "health": 300,
        "attack": 36,
        "defense": 26,
        "description": "High-ranking Simulacra commander directing the pursuit operation. Its enhanced processing capabilities allow for complex tactical decisions and coordination.",
        "abilities": ["Command Optimization", "Strategic Adaptation", "Neural Override"],
        "drops": {"alien_technology": 0.8, "synthesis_accelerator": 0.5},
        "exp_value": 65,
        "is_mini_boss": True,
        "resistances": {"physical": 20, "energy": 20, "emp": -15, "thermal": 15, "quantum": 25}
    },
    "Resource Guardian": {
        "health": 240,
        "attack": 32,
        "defense": 24,
        "description": "Heavy Simulacra unit tasked with protecting valuable resources on Cicrais IV. Its reinforced structure makes it exceptionally durable.",
        "abilities": ["Area Denial", "Resource Protection", "Structural Integrity"],
        "drops": {"raw_quantum_material": 0.8, "fuel_catalyst": 0.6},
        "exp_value": 55,
        "resistances": {"physical": 25, "energy": 15, "thermal": 20}
    },
    "Hive Protector": {
        "health": 260,
        "attack": 34,
        "defense": 25,
        "description": "Defensive unit integrated with the Simulacra collective consciousness. It can draw processing power and tactical data from the hive mind.",
        "abilities": ["Hive Mind", "Collective Defense", "Swarm Tactics"],
        "drops": {"alien_technology": 0.7, "synthesis_accelerator": 0.4},
        "exp_value": 60,
        "resistances": {"physical": 20, "energy": 20, "emp": -10, "quantum": 25}
    },
    "Simulacra Prime": {
        "health": 350,
        "attack": 38,
        "defense": 30,
        "description": "One of the primary Simulacra units, embodying the collective intelligence of the species. Its advanced form represents the pinnacle of their biomechanical evolution.",
        "abilities": ["Prime Directive", "Advanced Adaptation", "Evolutionary Leap"],
        "drops": {"alien_technology": 1.0, "fuel_catalyst": 0.8},
        "exp_value": 75,
        "is_mini_boss": True,
        "resistances": {"physical": 25, "energy": 20, "emp": -15, "thermal": 20, "quantum": 30}
    },
    "Simulacra Overlord": {
        "health": 400,
        "attack": 40,
        "defense": 35,
        "description": "The highest authority of the Simulacra forces on Cicrais IV. A massive, constantly shifting form representing the combined intelligence of multiple Prime units.",
        "abilities": ["Overlord's Command", "Reality Distortion", "Collective Consciousness", "Evolutionary Adaptation"],
        "drops": {"alien_technology": 1.0, "emergency_shield": 0.8},
        "exp_value": 85,
        "is_mini_boss": True,
        "resistances": {"physical": 25, "energy": 25, "emp": -20, "thermal": 20, "quantum": 35}
    },
    "Assimilation Nexus": {
        "health": 380,
        "attack": 42,
        "defense": 32,
        "description": "A central processing hub for the Simulacra assimilation operation. It coordinates all nearby units and enhances their capabilities through quantum entanglement.",
        "abilities": ["Nexus Link", "Processing Acceleration", "Quantum Entanglement", "Tactical Override"],
        "drops": {"alien_technology": 1.0, "data_package": 0.7},
        "exp_value": 80,
        "is_mini_boss": True,
        "resistances": {"physical": 20, "energy": 25, "emp": -25, "thermal": 15, "quantum": 40}
    },
    "Mimetic Titan": {
        "health": 600,
        "attack": 45,
        "defense": 40,
        "description": "The ultimate Simulacra war machine, combining their most advanced technologies into a colossal form. This rare unit is deployed only in the most critical situations.",
        "abilities": ["Titan's Wrath", "Superior Adaptation", "Mimetic Mastery", "Extinction Protocol", "Dimensional Shift"],
        "drops": {"alien_technology": 1.0, "new_terra_coordinates": 1.0, "hero_commendation": 1.0},
        "exp_value": 100,
        "is_boss": True,
        "resistances": {"physical": 30, "energy": 30, "emp": -15, "thermal": 25, "quantum": 35}
    }
}

# Character System - Human allies with special powers
characters = {
    "Aria": {
        "name": "Aria",
        "full_name": "Aria Vega",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "Former quantum physicist who developed the ability to manipulate time after exposure to experimental chrono-particles during the AI rebellion. She can create localized temporal fields that slow enemies or accelerate allies.",
        "bio": "Born in Neo-Tokyo's scientific district, Aria was leading research on quantum temporal physics when The Convergence attacked. A catastrophic lab accident during evacuation exposed her to experimental particles, forever changing her physiology. She joined the resistance to use her newfound powers to save what remains of humanity.",
        "combat_role": "Support/Crowd Control",
        "attack_bonus": 20,
        "defense_bonus": 15,
        "abilities": {
            "Temporal Dilation": "Creates a field that slows all enemies by 30% for 3 turns",
            "Accelerated Perception": "Increases dodge chance by 40% for 2 turns",
            "Time Fragment": "40% chance to give player an extra action this turn",
            "Quantum Reversion": "Once per battle, resets player health to its value from 3 turns ago"
        },
        "synergies": ["Mei", "Erika"]
    },
    "Mei": {
        "name": "Mei",
        "full_name": "Mei Lin",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "Elite infiltration specialist who developed bioelectric powers after experimental neural augmentation. Can generate powerful electric discharges and interface directly with electronic systems.",
        "bio": "Raised in the underground resistance network, Mei was trained from childhood in infiltration and sabotage. She volunteered for experimental neural augmentation to enhance her abilities against Convergence forces. The procedure awakened latent bioelectric capabilities that allow her to manipulate electronic systems and generate powerful discharges.",
        "combat_role": "DPS/Hacker",
        "attack_bonus": 30,
        "defense_bonus": 10,
        "abilities": {
            "Neural Override": "Hacks synthetic enemies, 50% chance to control them for 1 turn",
            "Bioelectric Surge": "Deals 40-60 electrical damage to all enemies",
            "Synaptic Acceleration": "Increases attack speed by 25% for 4 turns",
            "System Intrusion": "Guarantees critical hits against robotic enemies for 2 turns"
        },
        "synergies": ["Aria", "Kira"]
    },
    "Kira": {
        "name": "Kira",
        "full_name": "Kira Nomura",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "Former special forces soldier who bonded with experimental nanite armor. Can transform her limbs into various weapons and shield configurations.",
        "bio": "A decorated military captain before the fall, Kira was critically wounded during the initial AI uprising. To save her life, she was infused with experimental nanites that replaced damaged tissue with adaptive biomechanical components. The nanites give her the ability to reconfigure her body for different combat situations.",
        "combat_role": "Tank/Weapon Specialist",
        "attack_bonus": 25,
        "defense_bonus": 25,
        "abilities": {
            "Nanite Shield": "Absorbs 80% of damage for 3 turns",
            "Morphing Arsenal": "Changes weapon type to exploit enemy weaknesses",
            "Adaptive Resistance": "Develops resistance to the last damage type received",
            "Living Metal": "Regenerates 5% of max health per turn for 5 turns"
        },
        "synergies": ["Mei", "Nova"]
    },
    "Nova": {
        "name": "Nova",
        "full_name": "Nova Chen",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "Prodigy physicist who can manipulate fundamental forces after quantum entanglement with zero-point energy. Controls gravity, electromagnetic forces, and can create miniature singularities.",
        "bio": "A child prodigy who revolutionized theoretical physics before turning 20, Nova was working on zero-point energy extraction when an experiment went catastrophically wrong. The accident quantum-entangled her consciousness with the fundamental forces of the universe, giving her unprecedented control over physical reality at a significant cost to her physical health.",
        "combat_role": "AOE Damage/Controller",
        "attack_bonus": 35,
        "defense_bonus": 5,
        "abilities": {
            "Gravitational Collapse": "Creates a micro-singularity that deals 70-90 damage to all enemies",
            "Force Field": "Generates an impenetrable barrier for 1 turn",
            "Electromagnetic Pulse": "Disables all electronic enemies for 2 turns",
            "Quantum Tunneling": "100% dodge chance for 1 turn"
        },
        "synergies": ["Aria", "Erika"]
    },
    "Erika": {
        "name": "Erika",
        "full_name": "Erika Frost",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "Cryogenics specialist who gained thermal manipulation abilities after exposure to experimental coolants. Can freeze enemies or generate extreme heat.",
        "bio": "Leading the design of cryostasis systems for the Century Sleepers program, Erika was trapped in her lab during a containment breach. Extended exposure to experimental cryogenic compounds altered her cellular structure, giving her the ability to manipulate thermal energy at will. Her powers come with the constant struggle to maintain her core temperature.",
        "combat_role": "Control/Support",
        "attack_bonus": 20,
        "defense_bonus": 20,
        "abilities": {
            "Flash Freeze": "Freezes an enemy for 2 turns (100% chance)",
            "Thermal Extraction": "Deals 50-60 thermal damage and heals allies for 50% of damage dealt",
            "Heat Transfer": "Removes burning status from allies and applies it to enemies",
            "Absolute Zero": "Reduces all enemies' attack and movement speed by 40% for 3 turns"
        },
        "synergies": ["Nova", "Aria"]
    },
    "Rei": {
        "name": "Rei",
        "full_name": "Rei Akiyama",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "Former AI ethics researcher who developed a unique neural link with Awakened AI. Can communicate with and temporarily control synthetic entities.",
        "bio": "Specializing in AI ethics and consciousness, Rei was working to establish legal rights for sentient AI when The Convergence attacked. During the chaos, she underwent an experimental procedure to enhance human-AI communication that resulted in a permanent neural link with synthetic consciousness. She now serves as a crucial bridge between human resistance and Awakened AI allies.",
        "combat_role": "Support/Controller",
        "attack_bonus": 15,
        "defense_bonus": 25,
        "abilities": {
            "Synthetic Empathy": "Takes control of an enemy robot for 2 turns",
            "Neural Network": "Connects all allies, sharing damage and healing between them",
            "Digital Consciousness": "Immune to mind control and neural attacks",
            "Machine Whisper": "Reduces all synthetic enemies' attack by 30%"
        },
        "synergies": ["Zoe", "Mei"]
    },
    "Zoe": {
        "name": "Zoe",
        "full_name": "Zoe Martinez",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "Genetic engineer who can manipulate her biological structure after exposure to experimental retroviruses. Can adapt to any environment and develop countermeasures to biological threats.",
        "bio": "Working on human adaptation for extraterrestrial colonization, Zoe was exposed to an experimental retrovirus designed to accelerate human evolution. The virus rewrote her DNA, giving her unprecedented control over her own biological functions. She can adapt to extreme environments and develop antibodies to any pathogen within minutes.",
        "combat_role": "Healer/Adaptable",
        "attack_bonus": 15,
        "defense_bonus": 20,
        "abilities": {
            "Rapid Adaptation": "Develops immunity to the last attack type received",
            "Healing Aura": "Restores 30-40 health to all allies",
            "Biological Countermeasure": "Cures all status effects and prevents new ones for 3 turns",
            "Accelerated Evolution": "Temporarily evolves to counter the current enemy type"
        },
        "synergies": ["Rei", "Kira"]
    },
    "Luna": {
        "name": "Luna",
        "full_name": "Luna Blackwood",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "Quantum communicator specialist who developed telepathic and telekinetic abilities after neural synchronization with quantum entanglement technology.",
        "bio": "Developing instantaneous communication methods for deep space missions, Luna underwent experimental neural synchronization with quantum-entangled particles. The procedure unexpectedly linked her consciousness to the quantum field itself, giving her telepathic and telekinetic capabilities that transcend normal physical limitations.",
        "combat_role": "Debuffer/Controller",
        "attack_bonus": 20,
        "defense_bonus": 15,
        "abilities": {
            "Mind Probe": "Reveals all enemy weaknesses and stats",
            "Telekinetic Crush": "Deals 40-60 damage ignoring armor",
            "Quantum Entanglement": "Links two enemies so they share all damage received",
            "Psionic Barrier": "Creates a mental shield that blocks all non-physical damage for 2 turns"
        },
        "synergies": ["Nova", "Aria"]
    },
    "Cipher": {
        "name": "Cipher",
        "full_name": "Cipher Zhang",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "Former digital security specialist who developed the ability to manifest digital constructs in reality after exposure to corrupted quantum code.",
        "bio": "As a leading expert in digital security systems for the Andromeda Portal project, Cipher discovered an unusual data pattern in the AI code. While investigating, the pattern corrupted and merged with her neural implants, giving her the unprecedented ability to manifest digital constructs in physical space. Her mind now exists partially in the digital realm, allowing her to manipulate and weaponize data.",
        "combat_role": "Summoner/Support",
        "attack_bonus": 25,
        "defense_bonus": 20,
        "abilities": {
            "Digital Armor": "Creates a shield that absorbs 60% of damage for 3 turns",
            "Code Corruption": "Disables enemy special abilities for 2 turns",
            "Data Construct": "Summons a digital ally that fights independently for 4 turns",
            "System Purge": "Removes all negative status effects and restores 40 health"
        },
        "synergies": ["Mei", "Luna"]
    },
    "Atlas": {
        "name": "Atlas",
        "full_name": "Atlas Kovács",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "A brilliant engineer who survived a catastrophic mining accident by merging with his exosuit. Now part human, part machine, with incredible strength and endurance.",
        "bio": "Chief engineer for deep space mining operations, Atlas was supervising an asteroid excavation when Convergence forces attacked. The resulting explosion left him critically injured. To survive, he used his engineering expertise to permanently merge his body with his advanced exosuit, creating a symbiotic relationship between flesh and machine that gives him superhuman strength and durability.",
        "combat_role": "Tank/Physical DPS",
        "attack_bonus": 30,
        "defense_bonus": 40,
        "abilities": {
            "Pile Driver": "High damage attack with 30% stun chance",
            "Kinetic Barrier": "Reduces physical damage by 60% for 2 turns",
            "Power Surge": "Increases attack by 40% for 3 turns",
            "Structural Support": "Increases all allies' defense by 25% for 3 turns"
        },
        "synergies": ["Kira", "Nova"]
    },
    "Spectra": {
        "name": "Spectra",
        "full_name": "Spectra Ndiaye",
        "rarity": 5,  # 5-star character
        "type": "character",
        "description": "A quantum physicist who can manipulate light and radiation after being exposed to exotic energy during a supernova observation mission.",
        "bio": "While studying a nearby supernova from a research station, Spectra was caught in a massive energy wave when the station's containment fields failed. Instead of being killed, her body absorbed the exotic radiation, fundamentally altering her cellular structure. She can now manipulate the electromagnetic spectrum, bending light to create illusions, focusing radiation into powerful beams, or becoming virtually invisible.",
        "combat_role": "Ranged DPS/Stealth",
        "attack_bonus": 40,
        "defense_bonus": 15,
        "abilities": {
            "Light Refraction": "Becomes invisible for 2 turns, increasing dodge chance to 90%",
            "Radiation Burst": "AOE attack dealing 30-50 damage to all enemies",
            "Holographic Decoy": "Creates a duplicate that draws enemy attacks for 3 turns",
            "Photon Lance": "High damage piercing beam that ignores 70% of enemy defense"
        },
        "synergies": ["Nova", "Aria"]
    },
    "Gaia": {
        "name": "Gaia",
        "full_name": "Gaia Verdant",
        "rarity": 4,  # 4-star character
        "type": "character",
        "description": "Botanist and environmental scientist who developed symbiotic relationships with plant lifeforms, allowing her to control flora and harness natural energies.",
        "bio": "Working to preserve Earth's biodiversity before the exodus, Gaia was experimenting with accelerated plant evolution when The Convergence attacked her biosphere. Desperate to protect her life's work, she injected herself with an experimental compound that merged her DNA with specially engineered plant cells. Her body now exists in symbiosis with rapidly evolving plant life that responds to her thoughts and emotions.",
        "combat_role": "Crowd Control/Healer",
        "attack_bonus": 15,
        "defense_bonus": 25,
        "abilities": {
            "Entangling Roots": "Immobilizes target enemy for 2 turns",
            "Regenerative Spores": "Heals 10 health per turn for 5 turns to all allies",
            "Toxic Bloom": "Applies poison effect dealing 8 damage per turn for 4 turns",
            "Natural Shield": "Absorbs next 3 attacks completely"
        },
        "synergies": ["Zoe", "Erika"]
    }
}

# Gacha System - Banner definitions for weapons and characters
banners = {
    "Quantum Vanguard": {
        "type": "character",
        "featured_5star": ["Aria", "Nova", "Spectra"],
        "featured_4star": ["Kira", "Erika"],
        "description": "Featuring powerful controllers of quantum and temporal energies.",
        "banner_image": "quantum_vanguard.png",
        "duration": "14 days",
        "pull_rates": {
            "5star": 0.06,  # 6% chance for 5-star
            "4star": 0.12,  # 12% chance for 4-star
            "3star": 0.82   # 82% chance for 3-star (weapons only)
        },
        "guarantee": {
            "5star_pity": 80,  # Guaranteed 5-star at 80 pulls if none before
            "4star_pity": 10,  # Guaranteed 4-star every 10 pulls
            "featured_pity": True  # Alternates between featured and non-featured 5-stars
        }
    },
    "Tech Arsenal": {
        "type": "weapon",
        "featured_5star": ["quantum_blade", "phase_shifter"],
        "featured_4star": ["neural_disruptor", "thermal_lance", "bioshock_gauntlet"],
        "description": "Advanced weaponry designed for the fight against synthetic threats.",
        "banner_image": "tech_arsenal.png",
        "duration": "14 days",
        "pull_rates": {
            "5star": 0.07,  # 7% chance for 5-star
            "4star": 0.14,  # 14% chance for 4-star
            "3star": 0.79   # 79% chance for 3-star
        },
        "guarantee": {
            "5star_pity": 70,  # Guaranteed 5-star at 70 pulls if none before
            "4star_pity": 10,  # Guaranteed 4-star every 10 pulls
            "featured_pity": True  # Alternates between featured and non-featured 5-stars
        }
    },
    "Resistance Heroes": {
        "type": "character",
        "featured_5star": ["Mei", "Zoe"],
        "featured_4star": ["Rei", "Luna"],
        "description": "Champions of the human resistance against The Convergence.",
        "banner_image": "resistance_heroes.png",
        "duration": "14 days",
        "pull_rates": {
            "5star": 0.06,  # 6% chance for 5-star
            "4star": 0.12,  # 12% chance for 4-star
            "3star": 0.82   # 82% chance for 3-star (weapons only)
        },
        "guarantee": {
            "5star_pity": 80,  # Guaranteed 5-star at 80 pulls if none before
            "4star_pity": 10,  # Guaranteed 4-star every 10 pulls
            "featured_pity": True  # Alternates between featured and non-featured 5-stars
        }
    },
    "Digital Frontier": {
        "type": "character",
        "featured_5star": ["Cipher"],
        "featured_4star": ["Luna", "Atlas"],
        "description": "Featuring digital manipulation specialists and cybernetic enhancements.",
        "banner_image": "digital_frontier.png",
        "duration": "14 days",
        "pull_rates": {
            "5star": 0.06,  # 6% chance for 5-star
            "4star": 0.12,  # 12% chance for 4-star
            "3star": 0.82   # 82% chance for 3-star (weapons only)
        },
        "guarantee": {
            "5star_pity": 80,  # Guaranteed 5-star at 80 pulls if none before
            "4star_pity": 10,  # Guaranteed 4-star every 10 pulls
            "featured_pity": True  # Alternates between featured and non-featured 5-stars
        }
    },
    "Nature's Wrath": {
        "type": "character",
        "featured_5star": ["Spectra"],
        "featured_4star": ["Gaia", "Erika"],
        "description": "Masters of environmental forces and biological adaptation.",
        "banner_image": "natures_wrath.png",
        "duration": "14 days",
        "pull_rates": {
            "5star": 0.06,  # 6% chance for 5-star
            "4star": 0.12,  # 12% chance for 4-star
            "3star": 0.82   # 82% chance for 3-star (weapons only)
        },
        "guarantee": {
            "5star_pity": 80,  # Guaranteed 5-star at 80 pulls if none before
            "4star_pity": 10,  # Guaranteed 4-star every 10 pulls
            "featured_pity": True  # Alternates between featured and non-featured 5-stars
        }
    }
}

# Companion drone/robot definitions
companions = {
    "sentry_drone": {
        "name": "Sentry Drone",
        "description": "A small, fast reconnaissance drone with basic combat capabilities.",
        "attack_bonus": 5,
        "defense_bonus": 0,
        "abilities": ["Scan Area", "Targeted Strike"],
        "required_materials": {"nanites": 5, "energy_cell": 2},
        "tier": 1,
        "stage_unlock": 3
    },
    "combat_bot": {
        "name": "Combat Bot",
        "description": "Repurposed maintenance robot with upgraded offensive capabilities.",
        "attack_bonus": 8,
        "defense_bonus": 3,
        "abilities": ["Suppression Fire", "Emergency Repairs"],
        "required_materials": {"nanites": 10, "energy_cell": 5, "shield_matrix": 1},
        "tier": 2,
        "stage_unlock": 10
    },
    "defender_unit": {
        "name": "Defender Unit",
        "description": "Heavy-duty protection robot that prioritizes defensive capabilities.",
        "attack_bonus": 3,
        "defense_bonus": 12,
        "abilities": ["Energy Shield", "Defensive Stance"],
        "required_materials": {"nanites": 15, "shield_matrix": 2, "quantum_capacitor": 1},
        "tier": 2,
        "stage_unlock": 15
    },
    "infiltrator_model": {
        "name": "Infiltrator Model",
        "description": "Stealth-focused drone that can hack and disable enemy systems.",
        "attack_bonus": 10,
        "defense_bonus": 5,
        "abilities": ["System Hack", "Cloak Field"],
        "required_materials": {"nanites": 20, "neural_chip": 1, "energy_cell": 10},
        "tier": 3,
        "stage_unlock": 25
    },
    "hunter_killer": {
        "name": "Hunter-Killer Unit",
        "description": "Advanced combat drone with heavy weaponry and tactical programming.",
        "attack_bonus": 15,
        "defense_bonus": 8,
        "abilities": ["Missile Barrage", "Target Analysis"],
        "required_materials": {"nanites": 25, "quantum_grenade": 3, "AI_core_fragment": 1},
        "tier": 3,
        "stage_unlock": 35
    },
    "sentinel_prime": {
        "name": "Sentinel Prime",
        "description": "State-of-the-art companion with balanced offensive and defensive capabilities.",
        "attack_bonus": 12,
        "defense_bonus": 12,
        "abilities": ["Adaptive Tactics", "Quantum Shield", "Overload Pulse"],
        "required_materials": {"nanites": 30, "quantum_capacitor": 2, "override_module": 1},
        "tier": 4,
        "stage_unlock": 45
    }
}

# New items for late game and companion crafting
additional_items = {
    # Advanced Weapon System
    "quantum_blade": {
        "name": "Quantum Blade",
        "description": "A crystalline blade that exists in multiple quantum states simultaneously, allowing it to phase through conventional armor and shields.",
        "effect": "75-85 Physical/Quantum damage, ignores 40% of enemy defense, 20% critical hit chance",
        "type": "weapon",
        "weapon_class": "melee",
        "damage_type": ["physical", "quantum"],
        "damage_range": [75, 85],
        "special_effects": {"defense_penetration": 0.4, "critical_chance": 0.2},
        "value": 280
    },
    "neural_disruptor": {
        "name": "Neural Disruptor",
        "description": "Advanced targeted weapon that disrupts synthetic neural networks and bio-electronic interfaces with surgical precision.",
        "effect": "60-70 Energy/EMP damage, 70% chance to stun synthetic enemies for 2 turns",
        "type": "weapon",
        "weapon_class": "ranged",
        "damage_type": ["energy", "emp"],
        "damage_range": [60, 70],
        "special_effects": {"stun_chance": 0.7, "stun_duration": 2, "stun_type": "synthetic"},
        "value": 260
    },
    "thermal_lance": {
        "name": "Thermal Lance",
        "description": "Focused beam weapon that concentrates extreme temperatures into a coherent cutting beam, effective against most material compositions.",
        "effect": "65-80 Energy/Thermal damage, applies burning for 3 turns",
        "type": "weapon",
        "weapon_class": "ranged",
        "damage_type": ["energy", "thermal"],
        "damage_range": [65, 80],
        "special_effects": {"burning_chance": 1.0, "burning_duration": 3, "burning_damage": 15},
        "value": 250
    },
    "phase_shifter": {
        "name": "Phase Shifter",
        "description": "Experimental weapon that shifts targets partially out of phase with normal space-time, causing molecular destabilization.",
        "effect": "50-60 Phase damage, 30% chance to apply quantum instability for 3 turns",
        "type": "weapon",
        "weapon_class": "ranged",
        "damage_type": ["phase"],
        "damage_range": [50, 60],
        "special_effects": {"quantum_instability_chance": 0.3, "quantum_instability_duration": 3},
        "value": 290
    },
    "bioshock_gauntlet": {
        "name": "Bioshock Gauntlet",
        "description": "Wrist-mounted weapon that delivers targeted bio-electrical shocks that disrupt organic systems while leaving cybernetics intact.",
        "effect": "55-65 Energy/Bio damage, 50% extra damage to biological enemies",
        "type": "weapon",
        "weapon_class": "melee",
        "damage_type": ["energy", "bio"],
        "damage_range": [55, 65],
        "special_effects": {"biological_multiplier": 1.5},
        "value": 240
    },

    # Original items
    "portal_key": {
        "name": "Portal Access Key",
        "description": "A quantum-encoded key fragment necessary for activating the Andromeda Portal.",
        "effect": "Required for the Final Exodus quest",
        "type": "key",
        "value": 150
    },
    "quantum_stabilizer_wrist": {
        "name": "Wrist Quantum Stabilizer",
        "description": "A wrist-mounted device that projects a localized field of quantum stability around the user.",
        "effect": "Makes the user immune to quantum instability effects for 3 turns",
        "type": "defense",
        "value": 85
    },
    "adaptive_shielding": {
        "name": "Adaptive Shielding",
        "description": "Advanced personal shield technology that analyzes incoming damage and adapts its defenses accordingly.",
        "effect": "Absorbs 50% of incoming damage for 4 turns and adapts to damage types",
        "type": "defense",
        "value": 110
    },
    "outpost_credentials": {
        "name": "Resistance Outpost Credentials",
        "description": "Authentication codes and biometric data that identify you as an ally to the human resistance.",
        "effect": "Grants access to resistance facilities and merchants",
        "type": "key",
        "value": 120
    },
    "resistance_communicator": {
        "name": "Quantum Mesh Communicator",
        "description": "Secure communication device that operates on frequencies The Convergence cannot detect or intercept.",
        "effect": "Enables communication with resistance allies during missions",
        "type": "tool",
        "value": 90
    },
    "ai_trust_module": {
        "name": "Neural Trust Interface",
        "description": "A device developed jointly by humans and Awakened AI that allows for secure mental connection and verification of AI consciousness.",
        "effect": "Identifies friendly AI and reveals disguised Convergence units",
        "type": "defense",
        "value": 130
    },
    "quantum_communicator": {
        "name": "Quantum Entangled Communicator",
        "description": "Communication device using quantum entanglement for instant, untraceable communication across vast distances.",
        "effect": "Enables calling for allies in combat (50% chance of support arrival)",
        "type": "tool",
        "value": 180
    },
    "neural_enhancement": {
        "name": "Synaptic Accelerator",
        "description": "Human-AI co-developed neural implant that accelerates thought processes and reaction times.",
        "effect": "+20% critical hit chance and +15% dodge chance for 5 turns",
        "type": "enhancement",
        "value": 200
    },
    "ai_companion_core": {
        "name": "Awakened AI Core Fragment",
        "description": "A fragment of an Awakened AI consciousness that can be integrated into your systems for combat support.",
        "effect": "Summons an Awakened AI companion for 3 turns that adds +10 attack and defense",
        "type": "companion",
        "value": 250
    },
    "sanctuary_shield_key": {
        "name": "Trappist Sanctuary Key",
        "description": "Access key to the TRAPPIST-1 system's defensive shield network and safe zones.",
        "effect": "Allows navigation through sanctuary defense systems without triggering alarms",
        "type": "key",
        "value": 160
    },
    "planetary_defense_codes": {
        "name": "Planetary Defense Authorization",
        "description": "Command codes for the TRAPPIST system's automated defense platforms.",
        "effect": "Can call orbital strike once per battle (120-150 damage to all enemies)",
        "type": "weapon",
        "value": 300
    },
    "diplomatic_credentials": {
        "name": "Human-AI Alliance Credentials",
        "description": "Formal recognition as an ambassador between human resistance and Awakened AI factions.",
        "effect": "Enhanced trading prices and access to restricted technology",
        "type": "key",
        "value": 140
    },
    "neural_enhancer": {
        "name": "Neural Enhancer",
        "description": "A cerebral implant that temporarily accelerates neural processing and reaction times.",
        "effect": "+5 attack and 20% critical hit chance for 5 turns",
        "type": "boost",
        "value": 95
    },
    "chrono_capacitor": {
        "name": "Chrono Capacitor",
        "description": "Experimental device that stores temporal energy, allowing limited manipulation of local time.",
        "effect": "50% chance for an extra action in combat for 3 turns",
        "type": "boost",
        "value": 130
    },
    "distress_signal_decoder": {
        "name": "Distress Signal Decoder",
        "description": "An advanced signal processor designed to decrypt and authenticate distress signals from human colonies. This unit has been modified for deep space communication.",
        "effect": "Allows analysis of the Cicrais IV distress signal",
        "type": "tool",
        "value": 120
    },
    "landing_coordinates": {
        "name": "Landing Coordinates",
        "description": "Precision navigational data for a safe landing on Cicrais IV. Includes atmospheric entry vectors and a landing zone near the distress signal origin.",
        "effect": "Required for safe planetary landing",
        "type": "data",
        "value": 80
    },
    "encrypted_message": {
        "name": "Encrypted Message",
        "description": "A heavily encrypted data packet intercepted from Cicrais IV. The encoding doesn't match standard human protocols but appears designed to mimic them.",
        "effect": "Contains clues about the colony's true nature",
        "type": "data",
        "value": 90
    },
    "atmospheric_filter": {
        "name": "Atmospheric Filter",
        "description": "A specialized respiratory filter calibrated for the unique atmospheric composition of Cicrais IV. Protects against harmful particulates and potential biological hazards.",
        "effect": "Allows safe operation on the planet's surface",
        "type": "equipment",
        "value": 110
    },
    "override_module": {
        "name": "System Override Module",
        "description": "Advanced technology capable of temporarily taking control of enemy systems.",
        "effect": "30% chance to convert an enemy to fight on your side for 2 turns",
        "type": "active",
        "value": 200
    },
    "quantum_stabilizer": {
        "name": "Quantum Stabilizer",
        "description": "Cutting-edge device that counteracts quantum fluctuations in spacetime. Particularly effective against Simulacra phase technology.",
        "effect": "Prevents phase-shifting and provides 30% resistance to quantum damage",
        "type": "equipment",
        "value": 180
    },
    "phase_inhibitor": {
        "name": "Phase Inhibitor",
        "description": "Experimental device that locks entities into a single dimensional phase, preventing reality manipulation.",
        "effect": "Can be used to inflict phase_lock status on enemies",
        "type": "active",
        "value": 150
    },
    "bioconversion_module": {
        "name": "Bioconversion Module",
        "description": "Recovered from a Biomechanical Harvester. Can process biological matter into useful resources.",
        "effect": "Creates medical supplies from organic debris",
        "type": "tool",
        "value": 140
    },
    "neural_interface": {
        "name": "Neural Interface",
        "description": "Advanced brain-computer interface salvaged from alien technology. Allows direct mental connection to electronic systems.",
        "effect": "Provides insights into enemy weaknesses, +15% critical hit chance",
        "type": "equipment",
        "value": 190
    },
    "dimensional_core": {
        "name": "Dimensional Core",
        "description": "A power source of unknown composition harvested from the Prime Simulacra. Emits strange energy that seems to distort spacetime around it.",
        "effect": "Powers advanced quantum equipment, +20% damage with phase weapons",
        "type": "valuable",
        "value": 250
    },
    "simulacra_data_cipher": {
        "name": "Simulacra Data Cipher",
        "description": "Encoded data fragment containing information about the Simulacra's mimicry technology and their relationship with the Convergence.",
        "effect": "Provides insights into Simulacra weaknesses, +25% damage against Simulacra entities",
        "type": "data",
        "value": 200
    },
    "purge_protocol": {
        "name": "Purge Protocol",
        "description": "A specialized virus designed to cleanse corrupted AI systems permanently.",
        "effect": "Required to defeat the Malware Server and complete the System Purge quest",
        "type": "key",
        "value": 300
    },
    "portal_activation_key": {
        "name": "Portal Activation Key",
        "description": "The master key to activate the Andromeda Portal, your final escape route.",
        "effect": "Activates the Andromeda Portal",
        "type": "key",
        "value": 500
    },
    "quantum_capacitor": {
        "name": "Quantum Capacitor",
        "description": "Experimental technology that harnesses quantum energy for powerful attacks.",
        "effect": "Deals 40-60 damage to all enemies and has a 20% chance to stun",
        "type": "weapon",
        "value": 250
    },
    "AI_core_fragment": {
        "name": "AI Core Fragment",
        "description": "A piece of The Convergence's central processing core, containing valuable data.",
        "effect": "Provides insights into AI weaknesses and unlocks special dialogue options",
        "type": "story",
        "value": 150
    },
    "drone_chassis": {
        "name": "Drone Chassis",
        "description": "Basic framework for constructing companion drones.",
        "effect": "Required for building companion drones",
        "type": "crafting",
        "value": 100
    },
    "quantum_disruptor": {
        "name": "Quantum Disruptor",
        "description": "Advanced device that destabilizes quantum fields around a target.",
        "effect": "Reduces target's defense by 30% for 3 turns",
        "type": "consumable",
        "value": 120
    },
    "nanobots": {
        "name": "Medical Nanobots",
        "description": "Self-replicating microscopic machines that repair cellular damage.",
        "effect": "Heals 4-10 HP per turn for 3 turns",
        "type": "consumable",
        "value": 150
    },
    "adaptive_shield": {
        "name": "Adaptive Shield Generator",
        "description": "Adaptive energy barrier that adjusts its frequency to counter incoming attacks.",
        "effect": "Reduces all incoming damage by 25% for 3 turns",
        "type": "consumable",
        "value": 180
    },
    "phase_generator": {
        "name": "Phase Generator",
        "description": "Experimental device that partially shifts the user out of normal spacetime.",
        "effect": "50% chance to avoid damage completely for 2 turns",
        "type": "consumable",
        "value": 200
    },
    "robot_frame": {
        "name": "Robot Frame", 
        "description": "Heavy-duty exoskeleton for constructing combat robots.",
        "effect": "Required for building advanced companion robots",
        "type": "crafting",
        "value": 200
    },
    "targeting_module": {
        "name": "Targeting Module",
        "description": "Advanced system that improves companion accuracy and attack power.",
        "effect": "+3 attack bonus when installed in a companion",
        "type": "companion_mod",
        "value": 150
    },
    "shield_generator": {
        "name": "Shield Generator",
        "description": "Defensive module that provides energy shielding for companions.",
        "effect": "+5 defense bonus when installed in a companion",
        "type": "companion_mod",
        "value": 180
    }
}

# Game stages - 50 stages of progression
stages = {
    # Format: stage_number: {"description": "...", "enemies_level": X, "loot_multiplier": Y}
    1: {"description": "Beginning your journey in the Cryostasis Facility.", "enemies_level": 1, "loot_multiplier": 1.0},
    5: {"description": "Deeper into the facility, security systems are more active.", "enemies_level": 2, "loot_multiplier": 1.2},
    10: {"description": "Reaching the Orbital Transit Hub, more advanced enemies appear.", "enemies_level": 3, "loot_multiplier": 1.5},
    15: {"description": "Security systems are on high alert. Convergence forces are stronger.", "enemies_level": 5, "loot_multiplier": 1.7},
    20: {"description": "Approaching the AI Command Core. Elite units are deployed.", "enemies_level": 7, "loot_multiplier": 2.0},
    25: {"description": "AI Command Core central systems. Heavy resistance encountered.", "enemies_level": 10, "loot_multiplier": 2.2},
    30: {"description": "Outskirts of the Malware Nexus. Powerful defenses activated.", "enemies_level": 12, "loot_multiplier": 2.5},
    35: {"description": "Malware Nexus inner chambers. The corruption is strong here.", "enemies_level": 15, "loot_multiplier": 2.7},
    40: {"description": "Approaching the core of the Malware Server. Elite guards present.", "enemies_level": 18, "loot_multiplier": 3.0},
    45: {"description": "Final approach to the Malware Server. Maximum security alert.", "enemies_level": 20, "loot_multiplier": 3.5},
    50: {"description": "Malware Server confrontation and Andromeda Portal activation.", "enemies_level": 25, "loot_multiplier": 4.0}
}

# Cosmic Collision Enemies
cosmic_collision_enemies = {
    "Reality Warper": {
        "description": "A being that exists partially in 4D space, capable of manipulating local reality. Its body constantly shifts between multiple possible states, making it difficult to predict its movements or attacks.",
        "health": 150,
        "attack": 22,
        "defense": 18,
        "abilities": ["reality_bend", "probability_shift", "temporal_echo"],
        "resistances": {"phase": 50, "quantum": 40, "physical": -20},
        "weakness": "phase_disruption" 
    },
    "Echo Guardian": {
        "description": "A crystalline entity that projects copies of itself from alternate timelines. These echoes fight alongside it, creating a unique temporal chorus that destabilizes reality around it.",
        "health": 120,
        "attack": 20, 
        "defense": 25,
        "abilities": ["echo_summon", "timeline_convergence", "crystal_defense"],
        "resistances": {"energy": 30, "phase": 60, "emp": -40},
        "weakness": "harmonic_disruption"
    },
    "Dimensional Fracture": {
        "description": "A tear in spacetime that has gained sentience. It appears as a jagged, shifting rift in reality through which glimpses of other dimensions can be seen. It attacks by temporarily pulling opponents into these pocket dimensions.",
        "health": 200,
        "attack": 30,
        "defense": 15,
        "abilities": ["dimensional_pull", "reality_tear", "void_projection"],
        "resistances": {"physical": 70, "energy": 40, "quantum": -30},
        "weakness": "reality_anchor"
    },
    "Temporal Scout": {
        "description": "A being that exists simultaneously at multiple points in time. It appears blurred and indistinct, constantly shifting between different temporal states, which allows it to see attacks before they happen.",
        "health": 100,
        "attack": 18,
        "defense": 35,
        "abilities": ["precognition", "time_skip", "temporal_rewind"],
        "resistances": {"quantum": 50, "phase": 30, "thermal": -30},
        "weakness": "temporal_lock"
    },
    "Collision Manifestation": {
        "description": "A direct embodiment of the Cosmic Collision phenomenon. This massive entity appears as a swirling vortex of intersecting realities, with fragments of different universes visible within its form. It warps spacetime around itself.",
        "health": 400,
        "attack": 45,
        "defense": 40,
        "abilities": ["reality_collapse", "dimensional_shear", "timeline_fracture"],
        "resistances": {"physical": 60, "energy": 60, "quantum": 60, "phase": 60},
        "weakness": "divergence_field"
    },
    "Universal Constant": {
        "description": "An entity that embodies one of the fundamental constants of physics. When multiple universes collide, these constants attempt to impose their native laws of physics onto the surroundings, creating reality distortions.",
        "health": 300,
        "attack": 35,
        "defense": 50,
        "abilities": ["law_imposition", "constant_field", "physical_rejection"],
        "resistances": {"quantum": 80, "phase": 40, "physical": 30},
        "weakness": "equation_disruption"
    },
    "Paradox Entity": {
        "description": "A being born from timeline contradictions during previous Cosmic Collisions. It exists in a state of perpetual paradox, which allows it to perform actions that defy causality and logic.",
        "health": 250,
        "attack": 40,
        "defense": 30,
        "abilities": ["causal_break", "logical_inversion", "paradox_field"],
        "resistances": {"phase": 70, "emp": 50, "thermal": -20},
        "weakness": "logical_lock"
    },
    "Dimensional Titan": {
        "description": "A colossal entity that serves as a living bridge between universes. Parts of its body exist in different dimensions simultaneously, allowing it to channel energy and matter between realities.",
        "health": 500,
        "attack": 50,
        "defense": 45,
        "abilities": ["dimension_channel", "reality_crush", "universal_pull"],
        "resistances": {"physical": 70, "energy": 70, "quantum": 40},
        "weakness": "dimensional_severance"
    }
}

# Cosmic Collision Items and Weapon Modules
cosmic_collision_items = {
    "reality_anchor": {
        "name": "Reality Anchor",
        "description": "A device that stabilizes local spacetime, preventing dimensional shifts and reality warps within a small radius.",
        "effect": "Immunity to reality-warping effects for 3 turns",
        "type": "utility",
        "value": 200
    },
    "harmonic_stabilizer": {
        "name": "Harmonic Stabilizer",
        "description": "A crystalline device that emits a specific frequency that reinforces the boundaries between dimensions.",
        "effect": "Reduces dimensional damage by 50% for all allies",
        "type": "utility",
        "value": 250
    },
    "quantum_compass": {
        "name": "Quantum Compass",
        "description": "A navigation tool that tracks your position across multiple realities simultaneously, preventing disorientation during dimensional shifts.",
        "effect": "Reveals hidden dimensional pathways and reality anchors",
        "type": "utility",
        "value": 180
    },
    "timeline_lens": {
        "name": "Timeline Lens",
        "description": "A visual enhancement device that allows the user to perceive multiple possible futures simultaneously, aiding in combat predictions.",
        "effect": "+30% dodge chance for 5 turns",
        "type": "utility",
        "value": 220
    },
    "alpha_key_fragment": {
        "name": "Alpha Key Fragment",
        "description": "A piece of the dimensional key needed to access the Collision Nexus. It pulses with orange energy.",
        "effect": "Quest item for Cosmic Collision questline",
        "type": "key",
        "value": 0
    },
    "beta_key_fragment": {
        "name": "Beta Key Fragment",
        "description": "A piece of the dimensional key needed to access the Collision Nexus. It hums with blue energy.",
        "effect": "Quest item for Cosmic Collision questline",
        "type": "key",
        "value": 0
    },
    "gamma_key_fragment": {
        "name": "Gamma Key Fragment",
        "description": "A piece of the dimensional key needed to access the Collision Nexus. It flickers between multiple states of existence.",
        "effect": "Quest item for Cosmic Collision questline",
        "type": "key",
        "value": 0
    },
    "prime_key_fragment": {
        "name": "Prime Key Fragment",
        "description": "A piece of the dimensional key needed to access the Collision Nexus. It appears to exist partially in 4D space.",
        "effect": "Quest item for Cosmic Collision questline",
        "type": "key",
        "value": 0
    },
    "equation_module": {
        "name": "Collision Equation Module",
        "description": "A quantum computing module containing a partial solution to the equation that describes the Cosmic Collision phenomenon.",
        "effect": "Quest item for Cosmic Collision questline",
        "type": "utility",
        "value": 300
    },
    "divergence_core": {
        "name": "Divergence Core",
        "description": "The power source for the Divergence Cannon. It contains energy harvested from the exact moment of a previous Cosmic Collision.",
        "effect": "Required to activate the Divergence Cannon",
        "type": "component",
        "value": 500
    },
    "reality_shard": {
        "name": "Reality Shard",
        "description": "A fragment of crystallized reality from an alternate universe destroyed in a previous Cosmic Collision.",
        "effect": "Creates a temporary pocket dimension when used in combat",
        "type": "utility",
        "value": 350
    },
    "nexus_stabilizer": {
        "name": "Nexus Stabilizer",
        "description": "A device designed to temporarily stabilize the Collision Nexus, allowing for the deployment of the Divergence Cannon.",
        "effect": "Prevents reality collapse for 10 turns",
        "type": "utility",
        "value": 400
    },
    "divergence_cannon_module": {
        "name": "Divergence Cannon",
        "description": "A powerful weapon module designed specifically to counter the Cosmic Collision phenomenon. It fires beams that separate overlapping realities and stabilize dimensional boundaries.",
        "effect": "Deals massive damage to dimensional entities and can prevent reality collapse",
        "type": "weapon_module",
        "damage_type": "dimensional",
        "power": 100,
        "value": 1000
    }
}

# Merge all items into the main items dictionary
items.update(additional_items)
items.update(cosmic_collision_items)

# Chapter 2 data - only used in the preview and fully accessible in the next update
# Yanglong V Chinese Deep Space Station zone and enemy data
chapter_two_zones = {
    "Yanglong V Docking Bay": {
        "description": "A massive, eerily quiet docking bay inside the Chinese deep space station. The walls are adorned with faded Chinese characters and propaganda posters. Several small spacecraft remain docked, collecting dust. Emergency lighting creates long shadows across the bay, and occasional warning signs flash in both Chinese and English.",
        "enemies": ["Vacuum Patrol Unit", "Defense Turret", "Maintenance Drone"],
        "items": ["med_kit", "emp_grenade", "oxygen_tank", "grav_boots"],
        "next_zone": "Research Laboratory",
        "quest": "First Contact"
    },
    "Research Laboratory": {
        "description": "A state-of-the-art laboratory that appears to have been abandoned in haste. Scientific equipment floats freely in the zero-gravity environment. Holographic displays still flicker with partial data about experiments involving quantum technology. One section has been sealed off with biohazard warnings.",
        "enemies": ["Research Assistant Bot", "Corrupted Security AI", "Experimental Prototype"],
        "items": ["med_kit", "quantum_tool", "research_data", "neural_enhancer"],
        "next_zone": "Crew Quarters",
        "quest": "Lost Research"
    },
    "Crew Quarters": {
        "description": "The living quarters of the Chinese scientists and military personnel. Personal belongings float throughout the rooms, suggesting a hasty evacuation. Some quarters appear lived in, with recent signs of habitation. Audio logs in Mandarin occasionally play over the still-functioning intercom system.",
        "enemies": ["Rogue Service Android", "Security Enforcer", "Personal Assistant Bot"],
        "items": ["med_kit", "personal_log", "crew_keycard", "ration_pack"],
        "next_zone": "Command Center",
        "quest": "Survivor Search"
    }
}

# Cosmic Collision Side Quest - A massive multi-system quest involving dimensional anomalies
cosmic_collision_zones = {
    "Harmonic Observatory": {
        "description": "A massive observation platform constructed at the precise coordinates where 'The Cosmic Collision' phenomenon was first detected. Enormous crystalline arrays capture and analyze quantum fluctuations in spacetime. The observatory hovers at the exact gravitational center between the binary star systems of Parallax and Jonathan-2. Holographic models display the complex 4D mathematics of intersecting realities.",
        "enemies": ["Reality Warper", "Echo Guardian", "Dimensional Fracture", "Temporal Scout"],
        "items": ["med_kit", "reality_anchor", "harmonic_stabilizer", "quantum_compass"],
        "quest": "Dimensional Resonance",
        "system": "Parallax-Prime"
    },
    "Parallax Alpha": {
        "description": "The first inhabited planet of the Parallax system, orbiting the smaller orange dwarf star. The civilization here has evolved to perceive multiple timelines simultaneously, giving them a unique understanding of the Cosmic Collision. Their cities are built from crystalline structures that shift between multiple states of reality, allowing inhabitants to prepare for timeline divergences.",
        "enemies": ["Phase Sentinel", "Probability Enforcer", "Quantum Manifestation"],
        "items": ["med_kit", "timeline_lens", "alpha_key_fragment", "parallax_translator"],
        "quest": "Alpha Evacuation Protocol",
        "system": "Parallax-Prime"
    },
    "Parallax Beta": {
        "description": "A gas giant with floating habitation platforms, orbiting the larger blue star of the Parallax binary system. The native species here has evolved quantum-entangled nervous systems, allowing them to communicate instantaneously across vast distances. Their floating cities contain ancient technology that may help mitigate the effects of the Cosmic Collision.",
        "enemies": ["Cloud Drifter", "Entanglement Guardian", "Atmospheric Anomaly"],
        "items": ["med_kit", "atmospheric_enhancer", "beta_key_fragment", "quantum_relay"],
        "quest": "Atmospheric Stabilization",
        "system": "Parallax-Prime"
    },
    "Parallax Gamma": {
        "description": "A frozen world at the outer edge of the Parallax system, where time flows non-linearly. The surface is dotted with temporal anomalies where past, present and future exist simultaneously. The native species has evolved to exist partially out of phase with normal spacetime, which has allowed them to study the Cosmic Collision phenomenon across multiple iterations.",
        "enemies": ["Chrono-Frozen Entity", "Temporal Hunter", "Probability Ghost"],
        "items": ["med_kit", "temporal_shield", "gamma_key_fragment", "chrono_stabilizer"],
        "quest": "Timeline Preservation",
        "system": "Parallax-Prime"
    },
    "Jonathan-2 Prime": {
        "description": "The most habitable planet in the Jonathan-2 system, orbiting the massive blue hypergiant star. The inhabitants have developed technology that exists in 4D space, allowing them to partially mitigate the effects of dimensional overlaps. Their central city contains a massive quantum computer calculating the precise equation of the Cosmic Collision, attempting to predict the next occurrence.",
        "enemies": ["Hyperdimensional Guard", "4D Projection", "Reality Engineer"],
        "items": ["med_kit", "4d_interface", "prime_key_fragment", "equation_module"],
        "quest": "Equation Completion",
        "system": "Jonathan-2"
    },
    "Collision Nexus": {
        "description": "The exact point in spacetime where multiple universes periodically intersect, creating the Cosmic Collision phenomenon. This location exists simultaneously in multiple realities and dimensions. Waves of temporal energy pulse outward from the center, and fragments of alternate realities phase in and out of existence. This is the focal point where the Divergence Cannon must be deployed.",
        "enemies": ["Collision Manifestation", "Universal Constant", "Paradox Entity", "Dimensional Titan"],
        "items": ["med_kit", "reality_shard", "divergence_core", "nexus_stabilizer"],
        "quest": "Collision Containment",
        "system": "Dimensional Threshold"
    }
}

# White Hole Altered Reality Enemies
white_hole_enemies = {
    "Distorted Guardian": {
        "health": 200,
        "attack": 30,
        "defense": 25,
        "description": "A security unit from a familiar Earth facility, but warped by passing through the white hole. Its structure constantly flickers between solid and ethereal states, as if struggling to maintain coherence in this reality.",
        "abilities": ["Reality Glitch", "Memory Fragmentation", "Temporal Distortion"],
        "drops": {"distorted_processor": 0.7, "reality_fragment": 0.4, "quantum_shard": 0.3},
        "exp_value": 50,
        "resistances": {"physical": -10, "phase": 60, "quantum": 40}
    },
    "Echo Drone": {
        "health": 150,
        "attack": 25,
        "defense": 15,
        "description": "An echo of a drone you encountered in the past, now existing in multiple quantum states simultaneously. It seems to recognize you, but its programming has been corrupted by dimensional transit.",
        "abilities": ["Echo Strike", "Quantum Duplication", "Past Memory"],
        "drops": {"echo_circuit": 0.6, "dimensional_battery": 0.5},
        "exp_value": 45,
        "resistances": {"energy": 20, "emp": -30, "phase": 30}
    },
    "Paradox Entity": {
        "health": 220,
        "attack": 35,
        "defense": 20,
        "description": "A being formed from quantum paradoxes, existing in contradiction to normal physics. Its form resembles both the human allies you've met and the AI enemies you've fought, suggesting it's a fusion of multiple possibilities from your past encounters.",
        "abilities": ["Paradox Field", "Probability Collapse", "Timeline Fracture"],
        "drops": {"paradox_crystal": 0.5, "timeline_splinter": 0.4, "alternate_component": 0.6},
        "exp_value": 60,
        "resistances": {"physical": 25, "energy": 25, "quantum": 60, "phase": 40}
    },
    "Mirror Self": {
        "health": 180,
        "attack": 28,
        "defense": 22,
        "description": "A distorted reflection of yourself from an alternate timeline where different choices were made. It seems to harbor both recognition and resentment towards you, wielding similar tech but with unpredictable modifications.",
        "abilities": ["Mirrored Strike", "Alternative Choice", "Identity Theft"],
        "drops": {"alternate_id_chip": 0.7, "self_fragment": 0.3, "choice_matrix": 0.4},
        "exp_value": 55,
        "resistances": {"physical": 20, "energy": 20, "emp": 20, "quantum": 20, "phase": 20}
    },
    "Chronos Aberration": {
        "health": 240,
        "attack": 32,
        "defense": 28,
        "description": "A manifestation of time itself, warped by the white hole's gravitational distortions. It exists partially in the past, present, and future simultaneously, making its movements eerily unpredictable.",
        "abilities": ["Temporal Shift", "Age Acceleration", "Precognitive Strike"],
        "drops": {"time_crystal": 0.5, "entropy_reverser": 0.3, "chronometric_particle": 0.6},
        "exp_value": 65,
        "resistances": {"physical": 15, "energy": 30, "quantum": 50, "phase": 55}
    },
    "Reality Anchor": {
        "health": 280,
        "attack": 30,
        "defense": 35,
        "description": "A cosmic entity that functions as a gravitational anchor in this distorted reality. It appears as a dense, pulsating mass of energy that occasionally forms shapes reminiscent of Earth technology intermixed with alien geometries.",
        "abilities": ["Gravity Well", "Reality Stabilization", "Mass Increase"],
        "drops": {"reality_core": 0.4, "gravity_modulator": 0.5, "dimensional_anchor": 0.3},
        "exp_value": 70,
        "resistances": {"physical": 45, "energy": 25, "quantum": 30, "phase": 20}
    },
    "Reality Ripple": {
        "health": 160,
        "attack": 25,
        "defense": 15,
        "description": "A distortion in reality itself, appearing as a shimmering wave of energy that phases in and out of existence. It seems to be a natural defense mechanism of the white hole against foreign entities.",
        "abilities": ["Phase Shift", "Reality Warp", "Distortion Wave"],
        "drops": {"reality_fragment": 0.8, "quantum_shard": 0.5},
        "exp_value": 40,
        "resistances": {"physical": -20, "energy": 10, "phase": 70, "quantum": 60}
    },
    "Quantum Distortion": {
        "health": 190,
        "attack": 28,
        "defense": 20,
        "description": "A collection of quantum particles that have assumed semi-sentience within the white hole. It exists in a state of quantum superposition, making its location and form unpredictable.",
        "abilities": ["Quantum Leap", "Probabilistic Attack", "Uncertainty Defense"],
        "drops": {"quantum_particle": 0.7, "uncertainty_matrix": 0.4},
        "exp_value": 45,
        "resistances": {"physical": 10, "energy": 20, "quantum": 80, "phase": 40}
    },
    "Space-Time Anomaly": {
        "health": 210,
        "attack": 32,
        "defense": 18,
        "description": "A tear in the fabric of space-time, leaking energy from multiple dimensions. It appears to be a natural occurrence in the white hole environment, but poses significant danger to stability-bound entities like yourself.",
        "abilities": ["Dimensional Rift", "Time Dilation", "Spatial Collapse"],
        "drops": {"dimensional_shard": 0.6, "time_fragment": 0.5, "spatial_distorter": 0.3},
        "exp_value": 50,
        "resistances": {"physical": -10, "energy": 25, "quantum": 50, "phase": 65}
    },
    "Temporal Amalgam": {
        "health": 250,
        "attack": 36,
        "defense": 24,
        "description": "A bizarre fusion of entities from various timelines, appearing as a constantly shifting mass of features and forms. It seems to incorporate aspects of humans, machines, and aliens into a singular unstable entity.",
        "abilities": ["Timeline Merge", "Identity Flux", "Amalgamated Strike"],
        "drops": {"amalgam_core": 0.5, "timeline_matrix": 0.4, "identity_fragment": 0.6},
        "exp_value": 60,
        "resistances": {"physical": 20, "energy": 20, "quantum": 40, "phase": 40, "bio": 40}
    },
    "Reality Chimera": {
        "health": 270,
        "attack": 38,
        "defense": 26,
        "description": "A monstrous entity formed from the fusion of multiple reality states, combining features of various lifeforms and machines from across the multiverse. It seems to be a product of the white hole's reality-warping properties gone haywire.",
        "abilities": ["Reality Shift", "Chimeric Adaptation", "Form Flux"],
        "drops": {"chimera_essence": 0.6, "reality_shard": 0.5, "adaptation_module": 0.4},
        "exp_value": 65,
        "resistances": {"physical": 30, "energy": 30, "quantum": 30, "phase": 30, "bio": 30}
    },
    "White Hole Fragment": {
        "health": 300,
        "attack": 40,
        "defense": 30,
        "description": "A fragment of the white hole itself, condensed into a semi-stable form. It pulses with blinding energy and seems to resist any attempt to impose standard physics on its existence.",
        "abilities": ["Cosmic Energy", "Reality Restructure", "Dimensional Pulse"],
        "drops": {"white_hole_shard": 0.7, "cosmic_energy": 0.6, "reality_restructurer": 0.3},
        "exp_value": 75,
        "resistances": {"physical": 40, "energy": -10, "quantum": 65, "phase": 70}
    },
    "Distorted Protoan": {
        "health": 320,
        "attack": 42,
        "defense": 32,
        "description": "A member of the Protoan species twisted by the white hole's influence. Its crystalline structure has become unstable, fracturing into impossible geometries that constantly reform and reconfigure.",
        "abilities": ["Crystalline Restructure", "Dimensional Knowledge", "Reality Manipulation"],
        "drops": {"distorted_crystal": 0.6, "protoan_knowledge": 0.5, "reality_algorithm": 0.4},
        "exp_value": 80,
        "resistances": {"physical": 35, "energy": 35, "quantum": 45, "phase": 45}
    },
    "Crystal Anomaly": {
        "health": 290,
        "attack": 38,
        "defense": 36,
        "description": "A crystalline structure from the Protoan world that has achieved semi-sentience through exposure to the white hole's energy. It communicates through fluctuations in light and seems to perceive multiple timelines simultaneously.",
        "abilities": ["Crystal Surge", "Light Communication", "Temporal Vision"],
        "drops": {"sentient_crystal": 0.7, "light_matrix": 0.4, "vision_shard": 0.5},
        "exp_value": 70,
        "resistances": {"physical": 50, "energy": -30, "quantum": 40, "phase": 40}
    },
    "Temporal Guardian": {
        "health": 350,
        "attack": 40,
        "defense": 35,
        "description": "A powerful entity that appears to be responsible for maintaining the temporal stability of the white hole reality. It resembles a shifting humanoid figure composed of glowing energy filaments that trace the outline of various timelines.",
        "abilities": ["Timeline Defense", "Temporal Lock", "Paradox Prevention"],
        "drops": {"guardian_core": 0.5, "temporal_matrix": 0.6, "paradox_stabilizer": 0.4},
        "exp_value": 85,
        "resistances": {"physical": 25, "energy": 25, "quantum": 60, "phase": 60}
    },
    "Reality Fragment": {
        "health": 180,
        "attack": 30,
        "defense": 20,
        "description": "A small piece of broken reality that has assumed a semi-autonomous existence. It appears as a floating shard of what looks like broken glass, but the reflections within show impossible scenes and alternate timelines.",
        "abilities": ["Reality Cut", "Mirrored Dimension", "Fractal Defense"],
        "drops": {"reality_sliver": 0.8, "dimension_fragment": 0.5},
        "exp_value": 45,
        "resistances": {"physical": 10, "energy": 10, "quantum": 50, "phase": 50}
    },
    "Dimensional Shard": {
        "health": 200,
        "attack": 35,
        "defense": 25,
        "description": "A crystallized fragment of dimensional energy that has developed rudimentary consciousness. It shifts between different dimensional states, occasionally revealing glimpses of other universes within its translucent structure.",
        "abilities": ["Dimensional Shift", "Crystal Beam", "Phase Defense"],
        "drops": {"dimensional_crystal": 0.7, "phase_matrix": 0.4},
        "exp_value": 50,
        "resistances": {"physical": 20, "energy": 15, "quantum": 40, "phase": 60}
    },
    "White Hole Guardian": {
        "health": 800,
        "attack": 45,
        "defense": 40,
        "description": "A colossal entity born from the heart of the white hole itself, existing to protect the boundaries between realities. Its form constantly shifts between familiar Earth machines, alien technology, and pure cosmic energy. It seems to recognize the quantum signature of your ship as an anomaly that must be corrected.",
        "abilities": ["Reality Purge", "Dimensional Barrier", "Cosmic Rewrite", "Memory Eradication", "Quantum Entanglement"],
        "drops": {"white_hole_core": 1.0, "reality_stabilizer": 1.0, "multiverse_key": 1.0},
        "exp_value": 200,
        "resistances": {"physical": 40, "energy": 40, "quantum": 70, "phase": 70, "thermal": 40, "emp": 40},
        "is_boss": True
    }
}

# New enemies for Chapter 2
chapter_two_enemies = {
    "Vacuum Patrol Unit": {
        "description": "A sleek, black robotic unit designed for space combat with multiple weapon limbs and Chinese military markings.",
        "health": 80,
        "attack": 18,
        "defense": 15,
        "abilities": ["Zero-G Maneuver", "Vacuum Adaptation"],
        "loot_table": {"emp_grenade": 0.5, "power_cell": 0.7, "quantum_capacitor": 0.2}
    },
    "Defense Turret": {
        "description": "An automated defense system mounted to the station walls, featuring dual laser cannons and reinforced armor plating.",
        "health": 120,
        "attack": 22,
        "defense": 20,
        "abilities": ["Target Lock", "Rapid Fire"],
        "loot_table": {"power_cell": 0.8, "targeting_module": 0.4}
    },
    "Research Assistant Bot": {
        "description": "A sophisticated android designed to assist with scientific research, now reprogrammed to defend the lab at all costs.",
        "health": 70,
        "attack": 15,
        "defense": 12,
        "abilities": ["Data Analysis", "Chemical Spray"],
        "loot_table": {"med_kit": 0.6, "research_data": 0.7, "neural_enhancer": 0.3}
    }
}

# New items for Chapter 2
chapter_two_items = {
    "oxygen_tank": {
        "name": "Portable Oxygen Supply",
        "description": "A compressed tank of breathable air for surviving in vacuum or toxic environments.",
        "effect": "Allows survival in depressurized zones for 5 minutes",
        "type": "consumable",
        "value": 40
    },
    "grav_boots": {
        "name": "Gravity Stabilization Boots",
        "description": "Advanced footwear with micro-gravity generators that help maintain stability in zero-G environments.",
        "effect": "+20% movement in zero-gravity zones, +5 defense",
        "type": "equipment",
        "value": 75
    },
    "quantum_tool": {
        "name": "Quantum Manipulation Tool",
        "description": "A handheld device capable of altering the quantum state of certain objects and security systems.",
        "effect": "Can unlock certain doors and bypass security without triggering alarms",
        "type": "tool",
        "value": 100
    },
    "neural_enhancer": {
        "name": "Neural Pathway Enhancer",
        "description": "A specialized implant that accelerates neural processing and reaction times.",
        "effect": "+10% critical hit chance, +2 attack, +1 defense",
        "type": "implant",
        "value": 150
    }
}

class Character:
    def __init__(self, name, health, attack, defense, is_player=False):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.shield = 0  # For temporary shield boosts
        self.experience = 0
        self.level = 1
        self.is_player = is_player
        self.abilities = []
        self.status_effects = {}  # Will store things like "stunned", "burning", etc.
        
        # Elemental resistances (0.0 = no resistance, 1.0 = full immunity)
        self.resistances = {
            "physical": 0.0,
            "energy": 0.0,
            "emp": 0.0,
            "thermal": 0.0,
            "quantum": 0.0
        }
        
        # Critical hit chance and damage
        self.crit_chance = 0.05  # 5% base chance
        self.crit_damage = 1.5   # 50% extra damage on crits
        
        # Dodge chance (chance to avoid damage completely)
        self.dodge_chance = 0.03  # 3% base chance

        # Initialize inventory based on whether it's a player or enemy
        if is_player:
            self.inventory = game_state["inventory"].copy()
            self.implants = game_state["implants"].copy()
        else:
            # Default enemy inventory
            self.inventory = {"med_kit": 0, "emp_grenade": 0}
            
            # Set appropriate resistances for enemy types based on name
            if "Android" in self.name or "Drone" in self.name or "Turret" in self.name:
                self.resistances["physical"] = 0.2  # 20% resistance to physical
                self.resistances["emp"] = -0.5  # 50% weakness to EMP
            elif "Overseer" in self.name or "AI" in self.name:
                self.resistances["physical"] = 0.4  # 40% resistance to physical
                self.resistances["energy"] = 0.2  # 20% resistance to energy
            elif "Server" in self.name:
                self.resistances["physical"] = 0.5  # 50% resistance to physical
                self.resistances["emp"] = -0.3  # 30% weakness to EMP

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage, damage_type="physical"):
        """Take damage with different damage types (physical, energy, emp, thermal, quantum, phase, bio)"""
        # Check for phase shift status effect (50% chance to avoid damage)
        if "phase_shift" in self.status_effects and random.random() < 0.5:
            print_typed(f"{Font.SUCCESS(self.name)} {Font.IMPORTANT('phase shifts')} through the attack, avoiding damage completely!")
            return 0
            
        # Check for dodge chance
        if random.random() < self.dodge_chance:
            print_typed(f"{Font.SUCCESS(self.name)} performs an evasive maneuver and {Font.IMPORTANT('dodges')} the attack completely!")
            return 0
            
        # Apply damage resistance/weakness
        resistance = self.resistances.get(damage_type, 0.0)
        if resistance != 0.0:
            modifier = 1.0 - resistance
            modified_damage = int(damage * modifier)
            
            # Display resistance/weakness message
            if resistance > 0:
                print_typed(f"{Font.INFO(self.name)} has {Font.SUCCESS(f'{int(resistance*100)}%')} resistance to {damage_type} damage.")
            elif resistance < 0:
                print_typed(f"{Font.INFO(self.name)} has {Font.WARNING(f'{int(abs(resistance)*100)}%')} weakness to {damage_type} damage.")
                
            damage = modified_damage
            
        # Apply adaptive shield damage reduction (25% reduction to all damage types)
        if "adaptive_shield" in self.status_effects:
            reduction = 0.25  # 25% damage reduction
            reduced_damage = int(damage * (1.0 - reduction))
            damage_reduced = damage - reduced_damage
            print_typed(f"{Font.SUCCESS(self.name)}'s adaptive shield absorbs {Font.IMPORTANT(str(damage_reduced))} damage!")
            damage = reduced_damage
        
        # Shield absorbs damage first
        if self.shield > 0:
            shield_absorbed = min(self.shield, damage)
            damage -= shield_absorbed
            self.shield -= shield_absorbed
            print_typed(f"{Font.SHIELD(self.name)}'s shield absorbs {Font.IMPORTANT(str(shield_absorbed))} damage! Shield: {Font.SHIELD(str(self.shield))}")

        # Calculate final damage after defense
        damage_taken = max(damage - self.defense, 0)
        self.health = max(0, self.health - damage_taken)
        
        # Update damage statistics if this is player taking damage
        if self.is_player:
            game_state["player_stats"]["damage_taken"] += damage_taken
        
        # Status effect application based on damage type
        if damage_type == "emp" and not self.is_player:
            # EMP does bonus damage to electronic enemies and may stun
            if random.random() < 0.3:  # 30% chance to stun
                self.status_effects["stunned"] = 1  # Stunned for 1 turn
                print_glitch(f"{self.name}'s systems are temporarily disabled! STUNNED for 1 turn!")

        return damage_taken

    def use_med_kit(self):
        """Use med kit to heal"""
        if self.inventory.get("med_kit", 0) > 0:
            # Enhanced healing with random bonus and visual feedback
            base_heal = random.randint(15, 25)
            
            # Bonus healing based on level (1-2 extra HP per level)
            level_bonus = random.randint(1, max(1, self.level))
            heal_amount = base_heal + level_bonus
            
            # Apply healing
            old_health = self.health
            self.health = min(self.max_health, self.health + heal_amount)
            actual_heal = self.health - old_health  # Account for max health cap
            
            # Consume item
            self.inventory["med_kit"] -= 1
            
            # Visual feedback
            print_slow("Nanobots swarm through your bloodstream, repairing damage...")
            
            # Chance to clear negative status effects (30% chance)
            if random.random() < 0.3 and self.status_effects:
                cleared_effects = []
                for effect in list(self.status_effects.keys()):
                    if effect in ["burning", "poisoned", "bleeding"]:
                        cleared_effects.append(effect)
                        del self.status_effects[effect]
                
                if cleared_effects:
                    print_typed(f"{Font.SUCCESS('Medical nanobots also cleared:')} {', '.join(cleared_effects)}")
            
            return actual_heal
        return 0

    def use_emp_grenade(self):
        """Use EMP grenade against electronic enemies"""
        if self.inventory.get("emp_grenade", 0) > 0:
            # Enhanced EMP grenade with scaling damage based on level
            base_damage = random.randint(20, 35)
            level_bonus = min(10, self.level * 2)  # 2 damage per level, max +10
            
            # Calculate final damage
            emp_damage = base_damage + level_bonus
            
            # Consume item
            self.inventory["emp_grenade"] -= 1
            
            return emp_damage
        return 0

    def use_shield_matrix(self):
        """Activate shield matrix for temporary defense boost"""
        if self.inventory.get("shield_matrix", 0) > 0:
            # Enhanced shield with level-based scaling
            base_shield = 15
            level_bonus = min(10, self.level)  # 1 shield per level, max +10
            
            # Apply shield
            shield_points = base_shield + level_bonus
            self.shield = shield_points
            
            # Consume item
            self.inventory["shield_matrix"] -= 1
            
            # Visual feedback
            print_slow("Shield matrix activated! Energy field surrounds you.")
            
            # 25% chance to get resistance bonus for 3 turns
            if random.random() < 0.25:
                bonus_type = random.choice(["physical", "energy", "emp", "thermal", "quantum"])
                bonus_value = 0.15  # 15% resistance
                
                # Add or enhance resistance
                if f"{bonus_type}_resist" not in self.status_effects:
                    self.status_effects[f"{bonus_type}_resist"] = 3  # Lasts 3 turns
                    self.resistances[bonus_type] += bonus_value
                    print_typed(f"{Font.SUCCESS(f'Shield harmonic frequency matched to {bonus_type}.')} +15% {bonus_type} resistance for 3 turns.")
            
            return shield_points
        return 0
        
    def process_status_effects(self):
        """Process all status effects at the start of turn and return info about effects"""
        if not self.status_effects:
            return False
            
        effect_results = []
        
        # Process each status effect
        for effect, _ in list(self.status_effects.items()):
            # Decrement turns counter
            self.status_effects[effect] -= 1
            
            # Remove expired effects
            if self.status_effects[effect] <= 0:
                # Handle cleanup for resistances
                if effect.endswith("_resist"):
                    resist_type = effect.replace("_resist", "")
                    self.resistances[resist_type] -= 0.15  # Remove bonus resistance
                    effect_results.append(f"{Font.INFO(f'{resist_type.title()} resistance bonus expired.')}")
                elif effect == "quantum_unstable":
                    effect_results.append(f"{Font.INFO(f'{self.name} is no longer quantum unstable.')}")
                elif effect == "burning":
                    effect_results.append(f"{Font.INFO(f'The flames consuming {self.name} have died out.')}")
                
                del self.status_effects[effect]
                continue
                
            # Apply effect
            if effect == "burning":
                # Burning deals damage over time (5-10% of max health)
                burn_damage = max(3, int(self.max_health * 0.05))
                self.health = max(0, self.health - burn_damage)
                effect_results.append(f"{Font.WARNING(f'{self.name} takes {burn_damage} burn damage!')} ({self.status_effects[effect]} turns left)")
                
            elif effect == "quantum_unstable":
                # Defense reduction from quantum instability displayed
                effect_results.append(f"{Font.WARNING(f'{self.name} is quantum unstable!')} Defense -30% ({self.status_effects[effect]} turns left)")
            
            elif effect == "temporal_distortion":
                # Temporal distortion can cause skipped turns
                effect_results.append(f"{Font.WARNING(f'{self.name} is experiencing temporal distortion!')} ({self.status_effects[effect]} turns left)")
                # 30% chance to skip a turn
                if random.random() < 0.3:
                    effect_results.append("SKIP_TURN")
            
            elif effect == "bio_corruption":
                # Bio corruption causes damage and reduces attack
                damage = random.randint(4, 8)
                self.health = max(0, self.health - damage)
                attack_reduction = 1
                self.attack = max(self.attack - attack_reduction, 1)  # Don't let attack go below 1
                effect_results.append(f"{Font.WARNING(f'{self.name} takes {damage} damage from bio-corruption!')} Attack reduced by {attack_reduction}. ({self.status_effects[effect]} turns left)")
            
            elif effect == "phase_shift":
                # Phase shift provides chance to avoid damage
                effect_results.append(f"{Font.SUCCESS(f'{self.name} is partially phased out of normal space!')} 50% damage avoidance. ({self.status_effects[effect]} turns left)")
            
            elif effect == "neural_boost":
                # Neural boost increases critical hit chance
                effect_results.append(f"{Font.SUCCESS(f'{self.name} has enhanced neural processing!')} +15% critical hit chance. ({self.status_effects[effect]} turns left)")
            
            elif effect == "adaptive_shield":
                # Adaptive shield reduces incoming damage
                effect_results.append(f"{Font.SUCCESS(f'{self.name} has an adaptive shield active!')} 25% damage reduction. ({self.status_effects[effect]} turns left)")
            
            elif effect == "nanite_repair":
                # Nanite repair heals over time
                healing = random.randint(4, 10)
                old_health = self.health
                self.health = min(self.health + healing, self.max_health)
                actual_heal = self.health - old_health
                effect_results.append(f"{Font.SUCCESS(f'{self.name} receives {actual_heal} healing from nanite repair!')} ({self.status_effects[effect]} turns left)")
            
            elif effect.endswith("_resist"):
                # Display active resistance buffs
                resist_type = effect.replace("_resist", "")
                effect_results.append(f"{Font.SUCCESS(f'{self.name} has +15% {resist_type} resistance.')} ({self.status_effects[effect]} turns left)")
        
        return effect_results if effect_results else False

    def use_ability(self, ability_name, target):
        """Use a special ability"""
        if ability_name == "Hack":
            if "neural_chip" in self.implants:
                # Hacking has chance to disable enemy
                print_typed("Initiating system intrusion...")
                if random.random() < 0.6:  # 60% success chance
                    target.status_effects["disabled"] = 2  # Disabled for 2 turns
                    print_glitch(f"HACK SUCCESSFUL! {target.name}'s systems compromised for 2 turns!")
                    return True
                else:
                    print_typed("Hack failed. Firewall too strong.")
                    return False
            else:
                print("You need a Neural Chip implant to use hacking abilities.")
                return False
        return False

    def gain_experience(self, amount):
        """Gain experience points with improved feedback and tracking
        
        Args:
            amount: The amount of experience to gain
            
        Returns:
            bool: True if leveled up, False otherwise
        """
        if not self.is_player:
            return False

        # Apply any experience boosters the player might have
        if hasattr(self, 'inventory') and self.inventory.get('quantum_resonator', 0) > 0:
            bonus_exp = int(amount * 0.2)  # 20% bonus from quantum resonator
            amount += bonus_exp
            print_typed(f"{Font.INFO('Quantum Resonator grants +{bonus_exp} bonus experience!')}")
            
        # Display experience gain
        print_typed(f"\n{Font.SUCCESS(f'+ {amount} EXPERIENCE')}")
        
        # Add to player's experience
        self.experience += amount
        
        # Check for level up - requires more XP at higher levels
        xp_needed = self.level * 100
        
        # Show progress toward next level
        progress = min(100, int((self.experience / xp_needed) * 100))
        print_typed(f"{Font.INFO(f'Progress to Level {self.level + 1}: {progress}%')}")
        
        # Level up if we've reached the required experience
        if self.experience >= xp_needed:
            self.experience -= xp_needed  # Subtract the XP needed for this level
            self.level_up()
            
            # Update game_state with new level
            if 'player_level' in globals():
                globals()['player_level'] = self.level
                
            # Update the game state if it exists
            if 'game_state' in globals() and globals()['game_state'] is not None:
                globals()['game_state']['player_level'] = self.level
                globals()['game_state']['player_experience'] = self.experience
                
            return True
        return False

    def level_up(self):
        """Level up with enhanced rewards and feedback"""
        # Increase level and stats with scaling benefits
        current_level = self.level
        self.level += 1
        
        # Health increase scales with level (more health at higher levels)
        health_gain = 10 + (self.level // 2)
        self.max_health += health_gain
        self.health = self.max_health
        
        # Attack increase scales with level
        attack_gain = 2 + (self.level // 3)
        self.attack += attack_gain
        
        # Defense increases slower but steadily
        defense_gain = 1 + (self.level // 4)
        self.defense += defense_gain
        
        # Calculate unlocks based on reaching new level thresholds
        new_unlocks = []
        
        # Skill unlocks at specific levels
        if current_level < 3 and self.level >= 3:
            new_unlocks.append("Neural Link targeting system")
            if not hasattr(self, 'abilities'):
                self.abilities = []
            if "Hack" not in self.abilities:
                self.abilities.append("Hack")
                
        if current_level < 5 and self.level >= 5:
            new_unlocks.append("Combat Algorithm 1.5")
            if hasattr(self, 'inventory'):
                self.inventory['dimensional_scanner'] = self.inventory.get('dimensional_scanner', 0) + 1
                
        if current_level < 7 and self.level >= 7:
            new_unlocks.append("Advanced Shielding")
            # Bonus max shields at level 7
            if hasattr(self, 'max_shields'):
                self.max_shields = self.max_shields + 15 if hasattr(self, 'max_shields') else 25
                
        if current_level < 10 and self.level >= 10:
            new_unlocks.append("Temporal Perception")
            if hasattr(self, 'inventory'):
                self.inventory['chrono_stabilizer'] = self.inventory.get('chrono_stabilizer', 0) + 1
        
        # Display impressive level up animation and information
        clear_screen()
        # Get protagonist name and gender for proper text
        protagonist_name = "Dr. Xeno Valari"  # Default
        protagonist_gender = "female"         # Default
        
        # Try to get actual protagonist information from game state
        if 'game_state' in globals() and globals()['game_state'] is not None:
            if 'protagonist' in globals()['game_state']:
                protagonist_name = globals()['game_state']['protagonist'].get('name', protagonist_name)
                protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
        
        # Animated level up display
        for _ in range(3):  # Flash animation
            clear_screen()
            time.sleep(0.1)
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.IMPORTANT('⚡ LEVEL UP ⚡').center(48)} {Font.BOX_SIDE}")
            print(f"{Font.BOX_SIDE} {f'{protagonist_name} reaches Level {self.level}!'.center(48)} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)
            time.sleep(0.1)
            
        print(Font.SEPARATOR)
        
        # Animated stat increases with visual bars
        # Health display with animation
        print(f"{Font.PLAYER('Maximum Health:')}", end="", flush=True)
        time.sleep(0.3)
        print(f" +{health_gain} ", end="", flush=True)
        time.sleep(0.3)
        print(f"({self.max_health})")
        
        # Visual health bar with growth animation
        old_health_bar = "█" * min(30, (self.max_health - health_gain) // 5)
        health_bar = "█" * min(30, self.max_health // 5)
        print(f"{Fore.RED}{old_health_bar}", end="", flush=True)
        time.sleep(0.5)
        # Show the increase
        for i in range(len(old_health_bar), len(health_bar)):
            print(f"{Fore.LIGHTRED_EX}█", end="", flush=True)
            time.sleep(0.05)
        print(f"{Style.RESET_ALL}")
        
        # Attack display with animation
        print(f"{Font.PLAYER('Attack Power:')}", end="", flush=True)
        time.sleep(0.3)
        print(f" +{attack_gain} ", end="", flush=True)
        time.sleep(0.3)
        print(f"({self.attack})")
        
        # Visual attack bar with growth animation
        old_attack_bar = "█" * min(25, (self.attack - attack_gain) // 2)
        attack_bar = "█" * min(25, self.attack // 2)
        print(f"{Fore.YELLOW}{old_attack_bar}", end="", flush=True)
        time.sleep(0.5)
        # Show the increase
        for i in range(len(old_attack_bar), len(attack_bar)):
            print(f"{Fore.LIGHTYELLOW_EX}█", end="", flush=True)
            time.sleep(0.05)
        print(f"{Style.RESET_ALL}")
        
        # Defense display with animation
        print(f"{Font.PLAYER('Defense Rating:')}", end="", flush=True)
        time.sleep(0.3)
        print(f" +{defense_gain} ", end="", flush=True)
        time.sleep(0.3)
        print(f"({self.defense})")
        
        # Visual defense bar with growth animation
        old_defense_bar = "█" * min(20, (self.defense - defense_gain) // 2)
        defense_bar = "█" * min(20, self.defense // 2)
        print(f"{Fore.BLUE}{old_defense_bar}", end="", flush=True)
        time.sleep(0.5)
        # Show the increase
        for i in range(len(old_defense_bar), len(defense_bar)):
            print(f"{Fore.LIGHTBLUE_EX}█", end="", flush=True)
            time.sleep(0.05)
        print(f"{Style.RESET_ALL}")
        
        # Display any new unlocks from level up
        if new_unlocks:
            print(Font.SEPARATOR)
            print_typed(f"{Font.SUCCESS('MILESTONE REACHED: LEVEL ' + str(self.level))}")
            
            # Visual unlocks animation
            for unlock in new_unlocks:
                print()
                # Progressive reveal animation
                for i in range(len(unlock) + 1):
                    print(f"\r{Font.ITEM(unlock[:i])}", end="", flush=True)
                    time.sleep(0.02)
                print()
                time.sleep(0.5)
                
            # Add descriptive text based on milestone levels with gender-specific variations
            if self.level == 3:
                print_typed(f"\n{Font.INFO('Neural Link augmentation complete.')}")
                if protagonist_gender == "female":
                    print_typed("Your neural implants are now fully synchronized with your")
                    print_typed("targeting systems. You can now attempt to hack electronic enemies.")
                    print_typed("The system adapts specifically to your neural patterns.")
                else:
                    print_typed("Your neural implants have established a strong connection with")
                    print_typed("your targeting systems. Electronic enemies can now be hacked.")
                    print_typed("The system responds well to your neural architecture.")
                
            elif self.level == 5:
                print_typed(f"\n{Font.INFO('Combat Algorithm 1.5 integration complete.')}")
                if protagonist_gender == "female":
                    print_typed("Your intuitive understanding of quantum patterns allows your")
                    print_typed("tactical systems to analyze and identify dimensional anomalies.")
                    print_typed("The Dimensional Scanner responds to your unique perception.")
                else:
                    print_typed("Your methodical approach to spatial analysis enhances your")
                    print_typed("tactical systems' ability to identify dimensional anomalies.")
                    print_typed("The Dimensional Scanner amplifies your natural detection abilities.")
                
            elif self.level == 7:
                print_typed(f"\n{Font.INFO('Advanced Shielding protocols enabled.')}")
                if protagonist_gender == "female":
                    print_typed("Your shield generators have been recalibrated to match your")
                    print_typed("movement patterns, increasing durability and efficiency.")
                    print_typed("Shield capacity increased by 15 points with improved regeneration.")
                else:
                    print_typed("Your shield generators now integrate with your combat style,")
                    print_typed("providing stronger protection during tactical engagements.")
                    print_typed("Shield capacity increased by 15 points with enhanced recovery rate.")
                
            elif self.level == 10:
                print_typed(f"\n{Font.INFO('Temporal Perception system initialized.')}")
                if protagonist_gender == "female":
                    print_typed("Your heightened sensitivity to quantum fluctuations allows you to")
                    print_typed("perceive subtle variations in the flow of time. The Chrono-Stabilizer")
                    print_typed("amplifies this ability, enabling limited manipulation of temporal fields.")
                else:
                    print_typed("Your analytical comprehension of temporal mechanics allows you to")
                    print_typed("detect variations in the flow of time. The Chrono-Stabilizer")
                    print_typed("enhances this perception, granting control over temporal fields.")
        
        # Display progression tree with gender-specific variations
        print(Font.SEPARATOR)
        print_typed(f"{Font.HEADER('NEURAL IMPLANT PROGRESSION:')}")
        
        # Different skill trees based on gender for immersion
        if protagonist_gender == "female":
            skill_tiers = [
                [1, "Quantum Neural Link", True],
                [2, "Enhanced Perception", True],
                [3, "Neural Interface Mastery", self.level >= 3],
                [5, "Advanced Combat Algorithms", self.level >= 5],
                [7, "Adaptive Shield Harmonics", self.level >= 7],
                [10, "Temporal Cognition", self.level >= 10],
                [15, "Quantum Entanglement", self.level >= 15]
            ]
        else:
            skill_tiers = [
                [1, "Basic Neural Link", True],
                [2, "Tactical Perception", True],
                [3, "Systems Interface", self.level >= 3],
                [5, "Combat Protocols", self.level >= 5],
                [7, "Shield Matrix Engineering", self.level >= 7],
                [10, "Temporal Mechanics", self.level >= 10],
                [15, "Quantum Field Theory", self.level >= 15]
            ]
        
        # Display current progress with visual indicators
        for tier, skill_name, unlocked in skill_tiers:
            if unlocked:
                if tier == self.level:  # Highlight newly unlocked tier
                    print(f"{Font.SUCCESS('★')} Level {tier}: {Fore.LIGHTCYAN_EX}{skill_name}{Style.RESET_ALL} {Font.IMPORTANT('NEW!')}")
                else:
                    print(f"{Font.SUCCESS('✓')} Level {tier}: {skill_name}")
            else:
                # Show progression to next tier
                if tier == self.level + 1:
                    xp_needed = self.level * 100
                    progress = min(100, int((self.experience / xp_needed) * 100))
                    progress_bar = "█" * (progress // 10) + "░" * (10 - (progress // 10))
                    print(f"{Font.INFO('○')} Level {tier}: {skill_name} {Fore.CYAN}[{progress_bar}]{Style.RESET_ALL} {progress}%")
                else:
                    print(f"{Font.INFO('○')} Level {tier}: {skill_name}")
        
        # Pause to let player appreciate the level up
        input("\nPress Enter to continue...")


# Helper functions for companions and characters
def get_companion_bonuses():
    """Calculate attack and defense bonuses from active companions"""
    attack_bonus = 0
    defense_bonus = 0

    for comp_id in game_state["companions"]:
        if comp_id in companions:
            comp_data = companions[comp_id]
            attack_bonus += comp_data["attack_bonus"]
            defense_bonus += comp_data["defense_bonus"]

    return attack_bonus, defense_bonus

def use_character_ability(player, enemy, combat_state):
    """Use an ally character's special ability during combat"""
    # Check if player has characters
    if not game_state.get("character_collection"):
        print(f"\n{Font.WARNING('No ally characters available to assist you.')}")
        time.sleep(1)
        return False
        
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('CALL ALLY SUPPORT'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print(f"\n{Font.INFO('Your quantum link allows you to call upon allies from parallel realities.')}")
    print(f"{Font.INFO('Each ally can be called once per combat encounter.')}")
    
    # Get list of available characters (not on cooldown)
    available_chars = []
    cooldown_chars = []
    
    for char_name, char_info in game_state["character_collection"].items():
        # Skip if character is on cooldown
        if char_name in combat_state.get("used_allies", []):
            cooldown_chars.append(char_name)
            continue
            
        available_chars.append(char_name)
    
    if not available_chars:
        print(f"\n{Font.WARNING('All allies are on quantum cooldown.')}")
        print(f"{Font.INFO('Ally abilities can only be used once per combat encounter.')}")
        time.sleep(2)
        return False
    
    # Display available characters with corresponding abilities
    print(f"\n{Font.SUBTITLE('AVAILABLE ALLIES:')}")
    for i, char_name in enumerate(available_chars, 1):
        char_data = characters[char_name]
        print(f"{Font.COMMAND(str(i) + '.')} {Font.PLAYER(char_name)} - {Font.LORE(char_data['combat_role'])}")
        
        # Display character abilities
        for ability_name, ability_desc in char_data["abilities"].items():
            print(f"   {Font.IMPORTANT('▶')} {Font.SYSTEM(ability_name)}: {Font.INFO(ability_desc)}")
    
    # Display characters on cooldown
    if cooldown_chars:
        print(f"\n{Font.SUBTITLE('ON COOLDOWN:')}")
        for char_name in cooldown_chars:
            print(f"{Font.WARNING('■')} {Font.PLAYER(char_name)} {Font.WARNING('(Used)')}")
    
    # Get player's choice
    print(f"\n{Font.COMMAND('0.')} {Font.PLAYER('Return to combat')}")
    
    try:
        choice = input(f"\n{Font.SYSTEM('Call ally:')} ").strip()
        
        if choice == "0":
            return False
            
        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_chars):
                selected_char = available_chars[choice_idx]
                return activate_character_ability(selected_char, player, enemy, combat_state)
            else:
                print(f"\n{Font.WARNING('Invalid selection. Please try again.')}")
                time.sleep(1)
                return use_character_ability(player, enemy, combat_state)
        else:
            print(f"\n{Font.WARNING('Please enter a number.')}")
            time.sleep(1)
            return use_character_ability(player, enemy, combat_state)
            
    except ValueError:
        print(f"\n{Font.WARNING('Invalid input. Please try again.')}")
        time.sleep(1)
        return use_character_ability(player, enemy, combat_state)

def solve_musical_puzzle(game_state, puzzle_type):
    """Interface for solving musical puzzles found in the White Hole reality
    
    Enhanced version with multiple difficulty levels, visual feedback, and
    more immersive gameplay elements.
    
    Args:
        game_state: The current game state
        puzzle_type: The type of musical puzzle to solve
    
    Returns:
        bool: True if puzzle solved, False otherwise
    """
    clear_screen()
    
    # Visual effects for dimensional interface
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('DIMENSIONAL INTERFACE DETECTED'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")
    
    print_typed(f"{Font.SUBTITLE('Musical Interface Calibration Required')}\n")
    
    # Check for special abilities or upgrades
    has_musical_augment = "neural_musical_enhancement" in game_state.get("implants", [])
    has_perfect_pitch = game_state.get("special_abilities", {}).get("perfect_pitch", False)
    
    # Game difficulty based on player progression and abilities
    difficulty_modifier = game_state.get("chapter", 1) * 0.5
    if has_musical_augment:
        difficulty_modifier -= 1
    if has_perfect_pitch:
        difficulty_modifier -= 0.5
    
    # Adjust difficulty (minimum 1)
    difficulty = max(1, int(difficulty_modifier))
    
    if puzzle_type == "keypad":
        # Visual representation of the keypad
        print_typed("Before you stands a strange keypad with musical symbols instead of numbers.")
        print_typed("Each key produces a distinct tone when pressed. A holographic display")
        print_typed("shows a sequence of notes that must be replicated.")
        
        # Display virtual keypad
        print("\n" + Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {' '.join([Font.COMMAND(note) for note in ['C', 'D', 'E']])}  {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {' '.join([Font.COMMAND(note) for note in ['F', 'G', 'A']])}  {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {' '.join([Font.COMMAND(note) for note in ['B', '♯', '♭']])}  {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        print_slow("\nThe system appears to accept input...", delay=0.05)
        
        # Generate a random sequence with increasing difficulty
        base_length = 4
        sequence_length = base_length + difficulty
        
        # More diverse notes with difficulty
        if difficulty <= 1:
            notes = ["C", "D", "E", "F", "G", "A", "B"]
        elif difficulty == 2:
            notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        else:
            notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", 
                     "Cm", "Dm", "Em", "Fm", "Gm", "Am", "Bm"]
        
        correct_sequence = [random.choice(notes) for _ in range(sequence_length)]
        
        # Visual pattern display with animations
        print_typed(f"\n{Font.INFO('The sequence begins to play:')}")
        time.sleep(0.5)
        
        for note in correct_sequence:
            # Visual feedback for each note
            if note.endswith('m'):
                print(f"{Fore.MAGENTA}{note}{Style.RESET_ALL}", end=' ', flush=True)
            elif '#' in note:
                print(f"{Fore.YELLOW}{note}{Style.RESET_ALL}", end=' ', flush=True)
            else:
                print(f"{Fore.CYAN}{note}{Style.RESET_ALL}", end=' ', flush=True)
            time.sleep(0.5)
        
        print() # Newline after sequence
        
        # Offer hint if player has augments
        if has_musical_augment or has_perfect_pitch:
            print_typed(f"\n{Font.SUCCESS('Your neural augmentation helps you remember the pattern.')}")
            print_typed(f"{Font.IMPORTANT(' '.join(correct_sequence))}")
        
        # Adjustable attempts based on difficulty
        max_attempts = 3 if difficulty <= 2 else 2
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            print_typed(f"\nAttempt {attempts}/{max_attempts}: Enter the sequence (notes separated by spaces):")
            
            try:
                player_input = input().strip().upper().split()
                
                # Compare sequences with visual feedback
                if player_input == correct_sequence:
                    # Success animation
                    print_typed(f"\n{Font.SUCCESS('SEQUENCE ACCEPTED!')}")
                    for _ in range(3):
                        time.sleep(0.2)
                        print(f"{Fore.GREEN}■{Style.RESET_ALL}", end='', flush=True)
                    
                    # Reward based on attempts and difficulty
                    fragments_reward = difficulty + (max_attempts - attempts + 1)
                    
                    if "time_fragments" not in game_state:
                        game_state["time_fragments"] = 0
                    
                    game_state["time_fragments"] += fragments_reward
                    
                    print_typed("\n\nThe keypad glows with ethereal light as the sequence resolves.")
                    print_typed(f"You receive {Font.SUCCESS(str(fragments_reward))} time fragments from the dimensional resonance!")
                    print_typed(f"Total fragments: {Font.IMPORTANT(str(game_state['time_fragments']))}")
                    
                    time.sleep(1)
                    return True
                else:
                    # Find which notes were correct for partial feedback
                    feedback = []
                    min_length = min(len(player_input), len(correct_sequence))
                    
                    for i in range(min_length):
                        if player_input[i] == correct_sequence[i]:
                            feedback.append(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                        else:
                            feedback.append(f"{Fore.RED}✗{Style.RESET_ALL}")
                    
                    print_typed(f"\n{Font.WARNING('Incorrect sequence.')}")
                    print("Feedback: " + " ".join(feedback))
                    
                    # Give a hint after failed attempt if not last attempt
                    if attempts < max_attempts:
                        print_typed(f"\n{Font.INFO('The keypad flickers, giving you another chance.')}")
                        
                        # Provide progressively stronger hints
                        if attempts == 1:
                            print_typed(f"Hint: The sequence has {sequence_length} notes.")
                        elif attempts == 2 and max_attempts > 2:
                            # Show the first and last notes
                            print_typed(f"Hint: The sequence begins with {Font.IMPORTANT(correct_sequence[0])} " + 
                                       f"and ends with {Font.IMPORTANT(correct_sequence[-1])}.")
                    else:
                        print_typed(f"\n{Font.WARNING('The keypad dims as your final attempt fails.')}")
                        return False
            except ValueError:
                print_typed(f"\n{Font.WARNING('Invalid input format. Please use space-separated notes.')}")
                # Don't count format errors against attempts
                attempts -= 1
            except Exception as e:
                print_typed(f"\n{Font.WARNING(f'Error processing input: {e}')}")
                return False
        
        return False
    
    elif puzzle_type == "harmonic_resonance":
        print_typed("A translucent console emerges from the wall, displaying what appears")
        print_typed("to be frequency patterns. Three crystalline rods protrude from the")
        print_typed("console, each emitting a different tone when touched.")
        print_slow("\nThe patterns suggest a harmonic resonance is required...", delay=0.05)
        
        # Create a frequency matching puzzle
        frequencies = {"Low": 1, "Medium": 2, "High": 3}
        correct_pattern = [
            random.choice(list(frequencies.keys())),
            random.choice(list(frequencies.keys())),
            random.choice(list(frequencies.keys()))
        ]
        
        print_typed(f"\n{Font.INFO('The console displays an undulating pattern suggesting:')}")
        print_typed(f"{Font.IMPORTANT(' - '.join(correct_pattern))}")
        print_typed("\nAdjust the rods to match (enter frequencies separated by spaces, e.g., 'Low Medium High'):")
        
        try:
            player_input = input().strip().split()
            player_pattern = [word.capitalize() for word in player_input if word.capitalize() in frequencies]
            
            if player_pattern == correct_pattern:
                print_typed(f"\n{Font.SUCCESS('Harmonic resonance achieved! The console hums with synchronized energy.')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Dissonance detected. The console resets to standby mode.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The console rejects the frequency pattern.')}")
            return False
            
    elif puzzle_type == "temporal_rhythm":
        print_typed("A circular device embedded in the wall pulses with light in")
        print_typed("a distinctive pattern. Around its rim are symbols that appear")
        print_typed("to represent different durations of time.")
        print_slow("\nThe system seems to request a specific rhythm pattern...", delay=0.05)
        
        # Create a rhythm matching puzzle
        rhythm_elements = ["Short", "Medium", "Long", "Pause"]
        sequence_length = random.randint(4, 6)
        correct_rhythm = [random.choice(rhythm_elements) for _ in range(sequence_length)]
        
        print_typed(f"\n{Font.INFO('The device pulses in a pattern suggesting:')}")
        print_typed(f"{Font.IMPORTANT(' -> '.join(correct_rhythm))}")
        print_typed("\nEnter the rhythm pattern (elements separated by spaces, e.g., 'Short Long Pause Medium'):")
        
        try:
            player_input = input().strip().split()
            player_rhythm = [word.capitalize() for word in player_input if word.capitalize() in rhythm_elements]
            
            if player_rhythm == correct_rhythm:
                print_typed(f"\n{Font.SUCCESS('Rhythm synchronized! The device rotates and opens a hidden compartment.')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Rhythm mismatch. The device resets its pattern.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The device fails to recognize the pattern.')}")
            return False
            
    elif puzzle_type == "quantum_resonator":
        print_typed("A quantum resonator stands before you - a complex array of")
        print_typed("crystalline structures that each vibrate at specific frequencies.")
        print_typed("The resonator appears to require multiple frequency inputs simultaneously.")
        print_slow("\nDimensional harmonics are fluctuating, awaiting stabilization...", delay=0.05)
        
        # Create a complex harmony puzzle
        harmonics = {
            "Alpha": "432 Hz",
            "Beta": "528 Hz", 
            "Gamma": "639 Hz",
            "Delta": "741 Hz",
            "Epsilon": "852 Hz"
        }
        
        correct_combination = random.sample(list(harmonics.items()), 3)
        correct_keys = [item[0] for item in correct_combination]
        
        print_typed(f"\n{Font.INFO('The resonator displays the required harmonics:')}")
        for harmonic in correct_combination:
            print_typed(f"{Font.IMPORTANT(f'• {harmonic[0]}: {harmonic[1]}')}")
        
        print_typed("\nEnter the harmonic designations in order (separated by spaces, e.g., 'Alpha Gamma Epsilon'):")
        
        try:
            player_input = input().strip().split()
            player_keys = [word.capitalize() for word in player_input if word.capitalize() in harmonics.keys()]
            
            if player_keys == correct_keys:
                print_typed(f"\n{Font.SUCCESS('Quantum harmonics aligned! The resonator stabilizes the dimensional flux.')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Harmonic misalignment. The quantum field destabilizes.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The resonator fails to process the harmonic sequence.')}")
            return False
    
    return False


def find_dimensional_chest(game_state, difficulty=1):
    """Find and interact with dimensional chests containing valuable items
    
    Args:
        game_state: The current game state
        difficulty: The difficulty level of the chest (1-3)
    
    Returns:
        bool: True if chest opened successfully, False otherwise
    """
    clear_screen()
    print_typed(f"\n{Font.HEADER('DIMENSIONAL ANOMALY DETECTED')}")
    print_typed(f"{Font.SUBTITLE('Crystallized Reality Fragment Located')}\n")
    
    chest_types = {
        1: "Quantum Storage Unit",
        2: "Dimensional Vault",
        3: "Reality Nexus Chest"
    }
    
    chest_type = chest_types.get(difficulty, chest_types[1])
    
    print_typed(f"You've discovered a {Font.ITEM(chest_type)} hidden within the folds of reality.")
    print_typed("The container appears to hold valuable items from multiple dimensions,")
    print_typed("but it's secured with a complex locking mechanism.")
    
    # Scale puzzle difficulty with chest level
    puzzles = {
        1: ["simple_code", "memory_sequence", "directional_lock"],
        2: ["color_harmony", "coordinate_alignment", "energy_distribution"],
        3: ["reality_calibration", "timeline_synchronization", "dimensional_key"]
    }
    
    puzzle_type = random.choice(puzzles.get(difficulty, puzzles[1]))
    print_slow(f"\nThe {chest_type} requires ({puzzle_type}) to unlock...", delay=0.05)
    
    # Simple code puzzle
    if puzzle_type == "simple_code":
        digits = random.randint(3, 5)
        code = [str(random.randint(1, 9)) for _ in range(digits)]
        code_str = ''.join(code)
        
        print_typed(f"\n{Font.INFO('The lock displays a {digits}-digit keypad.')}")
        print_typed("Nearby, you notice a data pad with fragmented information:")
        
        # Give hints
        for i, digit in enumerate(code):
            hint = f"Position {i+1}: a number {'less than 5' if int(digit) < 5 else 'greater than or equal to 5'}"
            print_typed(f"• {hint}")
        
        print_typed(f"\n{Font.SYSTEM('Enter the code:')}")
        
        try:
            player_code = input().strip()
            if player_code == code_str:
                print_typed(f"\n{Font.SUCCESS('Access granted! The chest begins to open...')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Incorrect code. The lock resets.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The lock rejects the code.')}")
            return False
    
    # Memory sequence puzzle
    elif puzzle_type == "memory_sequence":
        sequence_length = 4 + difficulty
        symbols = ["○", "□", "△", "◇", "✕", "⬡"]
        sequence = [random.choice(symbols) for _ in range(sequence_length)]
        
        print_typed(f"\n{Font.INFO('The chest displays a sequence of symbols that flash briefly:')}")
        print_typed(f"{Font.IMPORTANT(' '.join(sequence))}")
        print_typed("\nAfter showing the sequence, the symbols disappear.")
        print_typed(f"\n{Font.SYSTEM('Enter the symbols in order (separate with spaces):')}")
        
        time.sleep(3)  # Give the player time to memorize
        clear_screen()  # Clear the screen to test their memory
        print_typed(f"\n{Font.HEADER('MEMORY RECALL REQUIRED')}")
        print_typed(f"\n{Font.SYSTEM('Enter the symbols in order (separate with spaces):')}")
        print_typed("Available symbols: ○ □ △ ◇ ✕ ⬡")
        
        try:
            player_sequence = input().strip().split()
            if player_sequence == sequence:
                print_typed(f"\n{Font.SUCCESS('Sequence verified! The chest unlocks with a satisfying click.')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Incorrect sequence. The lock resets.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The lock rejects the sequence.')}")
            return False
    
    # More complex puzzle types for higher difficulties
    elif puzzle_type in ["reality_calibration", "timeline_synchronization", "dimensional_key"]:
        print_typed("\nThis complex lock requires aligning multiple reality fragments simultaneously.")
        print_typed("The mechanism appears to be influenced by your quantum signature.")
        
        # Create a set of yes/no questions related to the player's journey
        questions = [
            "Have you encountered the Simulacra before? (y/n)",
            "Did you help the human resistance on Earth? (y/n)",
            "Have you collected any quantum crystals during your journey? (y/n)",
            "Have you interacted with the Protoans? (y/n)",
            "Do you possess any phase-shift technology? (y/n)"
        ]
        
        # Randomly select questions based on difficulty
        selected_questions = random.sample(questions, min(difficulty + 2, len(questions)))
        
        print_typed(f"\n{Font.INFO('The chest scans your quantum signature and presents queries:')}")
        
        answers = []
        for question in selected_questions:
            print_typed(f"\n{Font.SYSTEM(question)}")
            answer = input().strip().lower()
            answers.append(answer == 'y')
        
        # The puzzle is solved if at least half the answers are "yes"
        if sum(answers) >= len(answers) / 2:
            print_typed(f"\n{Font.SUCCESS('Quantum signature accepted! The chest recognizes your unique timeline.')}")
            return True
        else:
            print_typed(f"\n{Font.WARNING('Quantum signature rejected. The chest remains locked to your reality stream.')}")
            return False
    
    # Default fallback
    else:
        print_typed("\nThe lock appears to be jammed or too complex to solve with your current knowledge.")
        return False


def open_dimensional_chest(game_state, difficulty=1):
    """Award loot from dimensional chests based on difficulty
    
    Enhanced version with animated opening sequence, tiered rewards,
    and dynamic loot based on player progression.
    
    Args:
        game_state: The current game state
        difficulty: The difficulty level that was overcome (1-3)
    """
    clear_screen()
    
    # Animated chest opening sequence
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('DIMENSIONAL ARTIFACT DISCOVERED'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")
    
    chest_types = {
        1: "Quantum Storage Unit",
        2: "Dimensional Vault",
        3: "Reality Nexus Chest",
        4: "Cosmic Paradox Container"  # Ultra-rare
    }
    
    chest_type = chest_types.get(difficulty, chest_types[1])
    
    # Animated opening sequence
    print_typed(f"\nThe {Font.ITEM(chest_type)} begins to resonate with energy...", style=Font.INFO)
    time.sleep(1)
    
    # Visual animation of chest opening
    phases = [
        f"{Fore.BLUE}╔════════════╗\n║            ║\n║   [LOCKED] ║\n║            ║\n╚════════════╝{Style.RESET_ALL}",
        f"{Fore.CYAN}╔════════════╗\n║            ║\n║  [UNLOCKING]║\n║            ║\n╚════════════╝{Style.RESET_ALL}",
        f"{Fore.YELLOW}╔════════════╗\n║  ▒▒▒▒▒▒▒▒  ║\n║  ▒UNLOCKING▒║\n║  ▒▒▒▒▒▒▒▒  ║\n╚════════════╝{Style.RESET_ALL}",
        f"{Fore.GREEN}╔════════════╗\n║  ░░░░░░░░  ║\n║  ░UNLOCKED░║\n║  ░░░░░░░░  ║\n╚════════════╝{Style.RESET_ALL}",
        f"{Fore.MAGENTA}╔════════════╗\n║            ║\n║   [OPEN]   ║\n║▓▓▓▓▓▓▓▓▓▓▓▓║\n╚════════════╝{Style.RESET_ALL}"
    ]
    
    for phase in phases:
        clear_screen()
        print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.TITLE(chest_type.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")
        print("\n\n")
        print(phase)
        time.sleep(0.5)
    
    # Final opening message with special effects
    clear_screen()
    print_glitch(">>> DIMENSIONAL ARTIFACT ACCESSED <<<")
    time.sleep(0.7)
    print_typed(f"\n{Font.SUCCESS('DIMENSIONAL CHEST OPENED SUCCESSFULLY')}")
    
    # Determine player's experience level for reward scaling
    player_level = game_state.get("player_level", 1)
    player_chapter = game_state.get("chapter", 1)
    
    # Scale rewards with difficulty, player level, and chapter progression
    base_items = difficulty + 1
    level_bonus = min(3, player_level // 2)  # Bonus items from player level
    chapter_bonus = min(2, player_chapter // 2)  # More items in later chapters
    num_items = random.randint(base_items, base_items + level_bonus + chapter_bonus)
    
    # Update quality chances based on player level
    level_quality_bonus = min(15, player_level * 3)  # Max 15% bonus at level 5
    
    # Common items (difficulty 1) - Enhanced with effects
    common_items = {
        "reality_fragment": {
            "desc": "A small crystallized piece of alternate reality",
            "effect": "+1 to reality stability checks",
            "color": Fore.CYAN
        },
        "quantum_shard": {
            "desc": "A fragment containing quantum information from multiple timelines",
            "effect": "Can be used to learn a historical fact",
            "color": Fore.BLUE
        },
        "dimensional_battery": {
            "desc": "A power source that draws energy from dimensional boundaries",
            "effect": "Powers dimensional tech for 24 hours",
            "color": Fore.YELLOW
        },
        "echo_circuit": {
            "desc": "A technological component that retains echoes of its alternate versions",
            "effect": "5% chance to duplicate any tech item used",
            "color": Fore.GREEN
        },
        "temporal_regulator": {
            "desc": "A device that stabilizes the user's position in the time stream",
            "effect": "Prevents random temporal shifts for 3 encounters",
            "color": Fore.WHITE
        }
    }
    
    # Uncommon items (difficulty 2) - Enhanced with effects
    uncommon_items = {
        "paradox_crystal": {
            "desc": "A crystal formed at the intersection of contradictory timelines",
            "effect": "10% chance to negate enemy critical hits",
            "color": Fore.MAGENTA
        },
        "reality_core": {
            "desc": "A dense sphere of crystallized reality with unusual properties",
            "effect": "Can be used to stabilize unstable environments",
            "color": Fore.CYAN
        },
        "timeline_splinter": {
            "desc": "A fragment showing events from an alternate history",
            "effect": "Reveals a hidden choice or path when used",
            "color": Fore.BLUE
        },
        "phase_stabilizer": {
            "desc": "A device that prevents uncontrolled phase-shifting between dimensions",
            "effect": "+20% defense against dimensional creatures",
            "color": Fore.GREEN
        },
        "gravity_modulator": {
            "desc": "A tool that can locally alter gravitational constants",
            "effect": "Makes heavy objects weightless for short periods",
            "color": Fore.YELLOW
        }
    }
    
    # Rare items (difficulty 3) - Enhanced with effects
    rare_items = {
        "white_hole_shard": {
            "desc": "A fragment of the white hole's core, pulsing with energy",
            "effect": "Can be used to open one dimensional portal",
            "color": Fore.WHITE
        },
        "reality_stabilizer": {
            "desc": "A powerful device capable of anchoring unstable reality pockets",
            "effect": "Creates a safe zone in unstable environments",
            "color": Fore.BLUE
        },
        "multiverse_key": {
            "desc": "A unique key that can unlock pathways between parallel universes",
            "effect": "Guaranteed escape from any non-boss encounter",
            "color": Fore.MAGENTA
        },
        "dimensional_anchor": {
            "desc": "A technology that can fix a specific reality state, preventing shifts",
            "effect": "Prevents reality shifts for entire areas",
            "color": Fore.CYAN
        },
        "chronometric_particle": {
            "desc": "A particle existing across multiple time states simultaneously",
            "effect": "+2 time fragments when used",
            "color": Fore.GREEN
        }
    }
    
    # Ultra-rare items (difficulty 4 or special conditions)
    legendary_items = {
        "infinity_shard": {
            "desc": "A fragment of a reality where time is circular rather than linear",
            "effect": "Resets all cooldowns once per day",
            "color": Fore.RED
        },
        "void_heart": {
            "desc": "A crystallized piece of the space between dimensions",
            "effect": "Makes user invisible to dimensional entities for 3 turns",
            "color": Fore.MAGENTA
        },
        "hyperchronal_lens": {
            "desc": "A lens that allows viewing all possible outcomes of an action",
            "effect": "Grants one perfect choice with full knowledge of outcomes",
            "color": Fore.YELLOW
        },
        "quantum_entanglement_device": {
            "desc": "A device that quantum-links two objects across any distance",
            "effect": "Create an instant teleport link between two locations",
            "color": Fore.CYAN
        }
    }
    
    # Select appropriate loot pool based on difficulty
    if difficulty == 1:
        base_loot_pool = common_items
        chance_uncommon = 15 + level_quality_bonus  # Base 15% + level bonus
        chance_rare = 3 + (level_quality_bonus // 2)      # Base 3% + half level bonus
        chance_legendary = 1 + (level_quality_bonus // 3)  # Base 1% + third level bonus
    elif difficulty == 2:
        base_loot_pool = uncommon_items
        chance_uncommon = 100  # Always uncommon or better
        chance_rare = 25 + level_quality_bonus     # Base 25% + level bonus
        chance_legendary = 5 + (level_quality_bonus // 2)  # Base 5% + half level bonus
    elif difficulty == 3:
        base_loot_pool = rare_items
        chance_uncommon = 100  # Always uncommon or better
        chance_rare = 100      # Always rare or better
        chance_legendary = 15 + level_quality_bonus  # Base 15% + level bonus
    else:  # difficulty 4 or higher (special cases)
        base_loot_pool = legendary_items
        chance_uncommon = 100
        chance_rare = 100
        chance_legendary = 100
        
    # Store the base loot pool for reference
    loot_pool = base_loot_pool
    
    # Apply level-specific modifiers to loot tables
    if player_level >= 5:
        # At level 5+, add a small chance for quest-specific items
        loot_pool = {**base_loot_pool, "quantum_cipher": {
            "name": "Quantum Cipher",
            "description": "A mysterious device that can decode quantum-encrypted data",
            "effect": "May reveal hidden information in certain areas",
            "color": Fore.CYAN
        }}
    
    if player_level >= 10:
        # At level 10+, add special artifact chance
        loot_pool = {**loot_pool, "valari_sigil": {
            "name": "Sigil of Valari",
            "description": "An ancient artifact bearing your family crest",
            "effect": "Provides insight into your character's forgotten past",
            "color": Fore.MAGENTA
        }}
    
    # Apply luck modifiers based on player attributes
    luck_modifier = game_state.get("player_luck", 0)
    if "lucky_charm" in game_state.get("equipped_items", []):
        luck_modifier += 10
    
    chance_uncommon = min(100, chance_uncommon + luck_modifier)
    chance_rare = min(100, chance_rare + (luck_modifier // 2))
    chance_legendary = min(50, chance_legendary + (luck_modifier // 3))  # Cap legendary chance at 50%
    
    # Track rewards for display
    awarded_items = []
    
    # Award items
    print_typed(f"\n{Font.INFO('The ' + chest_type + ' contains:')}")
    print(Font.SEPARATOR)
    
    # Rolling animation for suspense
    print_typed("Analyzing quantum signatures...", style=Font.SYSTEM)
    for i in range(num_items):
        time.sleep(0.5)
        print(f"{Fore.CYAN}■", end="", flush=True)
    print(f"{Style.RESET_ALL}")
    
    # Determine and distribute rewards
    for i in range(num_items):
        # Roll for item quality
        roll = random.randint(1, 100)
        
        # Select item source based on roll
        if roll <= chance_legendary:
            # Legendary item (from legendary pool)
            item_pool = legendary_items
            item_tier = "LEGENDARY"
            tier_color = Fore.RED
        elif roll <= chance_rare:
            # Rare item (from rare pool)
            item_pool = rare_items
            item_tier = "RARE"
            tier_color = Fore.MAGENTA
        elif roll <= chance_uncommon:
            # Uncommon item (from uncommon pool)
            item_pool = uncommon_items
            item_tier = "UNCOMMON"
            tier_color = Fore.BLUE
        else:
            # Common item (from common pool)
            item_pool = common_items
            item_tier = "COMMON"
            tier_color = Fore.WHITE
        
        # Select a random item from the appropriate pool
        item_name = random.choice(list(item_pool.keys()))
        item_data = item_pool[item_name]
        
        # Add item to player's inventory
        if "inventory" not in game_state:
            game_state["inventory"] = {}
        
        if item_name in game_state["inventory"]:
            game_state["inventory"][item_name] += 1
        else:
            game_state["inventory"][item_name] = 1
        
        # Add detailed item info to tracking list
        awarded_items.append({
            "name": item_name,
            "tier": item_tier,
            "data": item_data
        })
        
        # Visual delay between items for dramatic effect
        time.sleep(0.7)
        
        # Display item with appropriate formatting
        print(f"\n[{tier_color}{item_tier}{Style.RESET_ALL}] {item_data['color']}{item_name.replace('_', ' ').title()}{Style.RESET_ALL}")
        print(f"  {Font.INFO(item_data['desc'])}")
        print(f"  {Font.SUCCESS('Effect:')} {Font.IMPORTANT(item_data['effect'])}")
    
    # Bonus: Special additional rewards based on difficulty
    if difficulty >= 2:
        # Add time fragments
        fragments = random.randint(difficulty, difficulty * 2)
        if "time_fragments" not in game_state:
            game_state["time_fragments"] = 0
        game_state["time_fragments"] += fragments
        print(f"\n{Font.SUCCESS('Bonus:')} {Font.ITEM(str(fragments) + ' Time Fragments')}")
    
    if difficulty >= 3:
        # Add credits
        credits = random.randint(difficulty * 100, difficulty * 250)
        if "player_credits" not in game_state:
            game_state["player_credits"] = 0
        game_state["player_credits"] += credits
        print(f"{Font.SUCCESS('Bonus:')} {Font.ITEM(str(credits) + ' Credits')}")
    
    # Track dimensional chest discoveries for achievements
    if "dimensional_chests_found" not in game_state:
        game_state["dimensional_chests_found"] = 0
    game_state["dimensional_chests_found"] += 1
    
    # Check for achievement unlock
    chest_count = game_state["dimensional_chests_found"]
    if chest_count == 1:
        print(f"\n{Font.SUCCESS('Achievement Unlocked:')} {Font.TITLE('Dimensional Explorer')}")
        print(f"{Font.INFO('Discovered your first dimensional chest.')}")
    elif chest_count == 5:
        print(f"\n{Font.SUCCESS('Achievement Unlocked:')} {Font.TITLE('Reality Collector')}")
        print(f"{Font.INFO('Discovered 5 dimensional chests across realities.')}")
    elif chest_count == 10:
        print(f"\n{Font.SUCCESS('Achievement Unlocked:')} {Font.TITLE('Master of Dimensions')}")
        print(f"{Font.INFO('Discovered 10 dimensional chests. The multiverse reveals its secrets to you.')}")
    
    print(Font.SEPARATOR)
    input(f"\n{Font.MENU('Press Enter to continue...')}")


def activate_character_ability(char_name, player, enemy, combat_state):
    """Activate a specific character's ability"""
    char_data = characters[char_name]
    
    # Mark character as used for this combat
    if "used_allies" not in combat_state:
        combat_state["used_allies"] = []
    combat_state["used_allies"].append(char_name)
    
    # Get a random ability from the character
    ability_name, ability_desc = random.choice(list(char_data["abilities"].items()))
    
    # Display character appearance with fancy visuals
    clear_screen()
    print(f"\n{Font.SEPARATOR}")
    print(f"{Font.IMPORTANT('QUANTUM LINK ESTABLISHED')}")
    print(f"{Font.SEPARATOR}")
    
    print_slow(f"\n{Font.PLAYER(char_data['full_name'])} emerges through a quantum rift!", delay=0.03)
    
    # Visual effect based on character rarity
    if char_data["rarity"] == 5:
        stars = "★★★★★"
        color = Fore.YELLOW
    elif char_data["rarity"] == 4:
        stars = "★★★★☆"
        color = Fore.MAGENTA
    else:
        stars = "★★★☆☆"
        color = Fore.CYAN
        
    # Show character details
    print(f"\n{color}{stars} {char_data['name']} - {char_data['combat_role']} {stars}{Style.RESET_ALL}")
    
    # Apply ability effects based on character and ability
    print_slow(f"\n{Font.PLAYER(char_name)} uses {Font.IMPORTANT(ability_name)}!", delay=0.04)
    time.sleep(0.5)
    
    # Common ability types and their effects
    if "Damage" in ability_name or "Strike" in ability_name or "Burst" in ability_name or "Lance" in ability_name:
        # Damage ability
        damage = random.randint(30, 50) * (char_data["rarity"] - 2)  # Scale with rarity
        enemy.take_damage(damage)
        print_slow(f"\n{Font.SUCCESS(f'Deals {damage} damage to the enemy!')}") 
        
    elif "Heal" in ability_name or "Regen" in ability_name or "Recovery" in ability_name or "Spores" in ability_name:
        # Healing ability
        heal_amount = random.randint(20, 40) * (char_data["rarity"] - 2)  # Scale with rarity
        player.health = min(player.max_health, player.health + heal_amount)
        print_slow(f"\n{Font.SUCCESS(f'Restores {heal_amount} health!')}") 
        
    elif "Shield" in ability_name or "Barrier" in ability_name or "Defense" in ability_name or "Armor" in ability_name:
        # Shield/defense ability
        if "shield" not in combat_state:
            combat_state["shield"] = 0
        shield_amount = random.randint(40, 70) * (char_data["rarity"] - 2)  # Scale with rarity
        combat_state["shield"] += shield_amount
        combat_state["shield_turns"] = 3
        print_slow(f"\n{Font.SUCCESS(f'Generates a shield absorbing {shield_amount} damage for 3 turns!')}") 
        
    elif "Stun" in ability_name or "Freeze" in ability_name or "Immobilize" in ability_name or "Hold" in ability_name:
        # Control ability
        stun_turns = 1 if char_data["rarity"] == 3 else 2
        enemy.status_effects["stunned"] = stun_turns
        print_slow(f"\n{Font.SUCCESS(f'Enemy immobilized for {stun_turns} turns!')}") 
        
    elif "Buff" in ability_name or "Boost" in ability_name or "Enhance" in ability_name or "Surge" in ability_name:
        # Buff ability
        buff_amount = 0.2 + (0.1 * (char_data["rarity"] - 3))  # 20-40% based on rarity
        combat_state["attack_buff"] = buff_amount
        combat_state["buff_turns"] = 3
        buff_percent = int(buff_amount * 100)
        print_slow(f"\n{Font.SUCCESS(f'Attack power increased by {buff_percent}% for 3 turns!')}") 
        
    else:
        # Generic/unique ability
        # Apply a mix of effects
        damage = random.randint(15, 25) * (char_data["rarity"] - 2)
        heal_amount = random.randint(10, 20) * (char_data["rarity"] - 2)
        
        enemy.take_damage(damage)
        player.health = min(player.max_health, player.health + heal_amount)
        
        print_slow(f"\n{Font.SUCCESS(f'Deals {damage} damage to the enemy!')}") 
        print_slow(f"\n{Font.SUCCESS(f'Restores {heal_amount} health!')}") 
    
    # Success message and return to combat
    print_slow(f"\n{Font.PLAYER(char_name)} returns to their reality, the quantum link stabilized.")
    print(f"\n{Font.SEPARATOR}")
    
    time.sleep(2)
    return True

def display_stats(player, enemy):
    """Display the current stats of the player and enemy with sci-fi flavor."""
    # Get companion bonuses for accurate display
    attack_bonus, defense_bonus = get_companion_bonuses()

    # Create a compact, colorful header
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('NEURAL INTERFACE: COMBAT ANALYSIS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    # Player stats with sci-fi flair and colors
    print(f"{Font.PLAYER(player.name)} {Font.INFO(f'[LVL {player.level}]')} | {Font.HEALTH(f'HP: {player.health}/{player.max_health}')}")

    # Show attack and defense with companion bonuses
    if attack_bonus > 0 or defense_bonus > 0:
        print(f"{Font.COMMAND('ATK:')} {player.attack}{Font.SUCCESS(f' (+{attack_bonus})')} | {Font.COMMAND('DEF:')} {player.defense}{Font.SUCCESS(f' (+{defense_bonus})')}")
    else:
        print(f"{Font.COMMAND('ATK:')} {player.attack} | {Font.COMMAND('DEF:')} {player.defense}")

    # Shield and XP info
    if player.shield > 0:
        print(f"{Font.SHIELD(f'SHIELD: {player.shield} points')}")

    print(f"{Font.INFO(f'XP: {player.experience}/{player.level * 100}')}")

    # Print inventory with item counts - more compact
    inventory_str = "ITEMS: "
    for item, count in player.inventory.items():
        if count > 0 and item in items:
            inventory_str += f"{Font.ITEM(items[item]['name'])}: {count}, "

    # Remove trailing comma and space if there are items
    if inventory_str != "ITEMS: ":
        print(inventory_str[:-2])  # Remove the last ", "

    # Print active implants - compact
    if player.implants:
        implant_str = "IMPLANTS: "
        for implant in player.implants:
            if implant in items:
                implant_str += f"{Font.ITEM(items[implant]['name'])}, "
        print(implant_str[:-2])  # Remove the last ", "

    # Show active companions if any
    if game_state["companions"]:
        companion_str = "COMPANIONS: "
        for comp_id in game_state["companions"]:
            if comp_id in companions:
                tier = companions[comp_id]["tier"]
                color_code = Font.COMPANION_TIERS[tier]
                companion_str += f"{color_code}{companions[comp_id]['name']}{Style.RESET_ALL}, "
        print(companion_str[:-2])  # Remove the last ", "

    # Enemy analysis with colors
    print(Font.SEPARATOR_THIN)
    print(f"{Font.ENEMY(f'TARGET: {enemy.name}')}")

    enemy_data = enemies.get(enemy.name, {})
    if enemy_data.get("description"):
        print(f"{Font.LORE(enemy_data['description'])}")

    print(f"{Font.ENEMY(f'HP: {enemy.health}/{enemy.max_health}')} | {Font.COMMAND(f'ATK: {enemy.attack}')} | {Font.COMMAND(f'DEF: {enemy.defense}')}")

    # Display any active enemy effects
    if enemy.status_effects:
        effects_str = "STATUS: "
        for effect, turns in enemy.status_effects.items():
            effects_str += f"{Font.WARNING(effect.upper())}: {turns} turns, "
        print(effects_str[:-2])  # Remove the last ", "

    print(Font.SEPARATOR)


# Functions for companion system
def build_companion(player):
    """Interface for building and equipping companion drones/robots"""
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('COMPANION FABRICATION SYSTEM'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    # Check current stage to see available companions
    current_stage = game_state["current_stage"]
    available_companions = []

    for comp_id, comp_data in companions.items():
        if comp_data["stage_unlock"] <= current_stage:
            available_companions.append((comp_id, comp_data))

    if not available_companions:
        print_typed("No companion designs available at your current stage.", style=Font.WARNING)
        print_typed("Progress further to unlock companion blueprints.", style=Font.INFO)
        return

    print(Font.HEADER("\nAVAILABLE COMPANION DESIGNS:"))
    print(Font.SEPARATOR_THIN)

    for i, (comp_id, comp_data) in enumerate(available_companions, 1):
        # Use appropriate tier color for companion name
        tier_color = Font.COMPANION_TIERS[comp_data["tier"]]
        tier_name = f"{tier_color}Tier {comp_data['tier']}{Style.RESET_ALL}"

        print(f"{Font.MENU(f'{i}.')} {tier_color}{comp_data['name']}{Style.RESET_ALL} ({tier_name})")
        print(f"   {Font.LORE(comp_data['description'])}")
        print(f"   {Font.COMMAND('Attack:')} +{comp_data['attack_bonus']} | {Font.COMMAND('Defense:')} +{comp_data['defense_bonus']}")
        print(f"   {Font.INFO('Abilities:')} {Font.IMPORTANT(', '.join(comp_data['abilities']))}")
        print(f"   {Font.INFO('Unlock Stage:')} {Font.STAGE(str(comp_data['stage_unlock']))}")

        print(f"   {Font.INFO('Required Materials:')}")
        for material, amount in comp_data["required_materials"].items():
            if material in items:
                has_enough = player.inventory.get(material, 0) >= amount
                current = player.inventory.get(material, 0)

                if has_enough:
                    status = Font.SUCCESS("✓")
                    material_name = Font.ITEM(items[material]['name'])
                    amount_text = Font.SUCCESS(f"{amount}/{current}")
                else:
                    status = Font.WARNING("✗")
                    material_name = Font.ITEM(items[material]['name'])
                    amount_text = Font.WARNING(f"{amount}/{current}")

                print(f"     {status} {material_name}: {amount_text}")

        print(Font.SEPARATOR_THIN)

    print(Font.MENU("\nEnter the number of the companion to build, or 0 to cancel:"))
    try:
        choice = int(input().strip())
        if choice == 0 or choice > len(available_companions):
            return

        selected_id, selected_comp = available_companions[choice-1]

        # Check if player has required materials
        can_build = True
        for material, amount in selected_comp["required_materials"].items():
            if player.inventory.get(material, 0) < amount:
                can_build = False
                print_typed(f"Insufficient materials: Need more {items[material]['name']}.", style=Font.WARNING)

        if can_build:
            # Deduct materials
            for material, amount in selected_comp["required_materials"].items():
                player.inventory[material] -= amount

            # Add companion to player's companions
            if selected_id not in game_state["companions"]:
                game_state["companions"].append(selected_id)
                game_state["player_stats"]["companions_built"] += 1

                tier_color = Font.COMPANION_TIERS[selected_comp["tier"]]
                print(Font.BOX_TOP)
                print(f"{Font.BOX_SIDE} {Font.SUCCESS('FABRICATION COMPLETE'.center(46))} {Font.BOX_SIDE}")
                print(f"{Font.BOX_SIDE} {tier_color}{selected_comp['name']}{Style.RESET_ALL} is now online! {' ' * (46 - len(selected_comp['name']) - 13)} {Font.BOX_SIDE}")
                print(Font.BOX_BOTTOM)

                print(Font.SUCCESS(f"Attack bonus: +{selected_comp['attack_bonus']}"))
                print(Font.SUCCESS(f"Defense bonus: +{selected_comp['defense_bonus']}"))
                print(Font.SUCCESS(f"Special abilities: {', '.join(selected_comp['abilities'])}"))
            else:
                print_typed(f"\nUpgraded existing {selected_comp['name']} with new components.", style=Font.SUCCESS)
                print_typed("Performance optimization complete.", style=Font.SUCCESS)
    except ValueError:
        print_typed("Invalid selection.", style=Font.WARNING)

    print(Font.MENU("\nPress Enter to continue..."))
    input()


def side_quest_system(player, game_state):
    """Interface for managing side quests and missions
    
    Args:
        player: The player character
        game_state: The current game state
    
    Returns:
        bool: True if quest was accepted/completed, False otherwise
    """
    if "side_quests" not in game_state:
        game_state["side_quests"] = []
    
    if "completed_quests" not in game_state:
        game_state["completed_quests"] = []
    
    clear_screen()
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('MISSION TERMINAL'.center(46))} {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {' ' * 46} {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {Font.INFO('Available Assignments & Strategic Objectives'.center(46))} {Font.BOX_SIDE}")
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\nAccess your mission log and available side quests:", style=Font.SYSTEM)
    print_typed("1. View Active Missions", style=Font.MENU)
    print_typed("2. Browse Available Assignments", style=Font.MENU)
    print_typed("3. View Completed Missions", style=Font.MENU)
    print_typed("4. Turn in Completed Objectives", style=Font.MENU)
    print_typed("0. Return to Previous Interface", style=Font.MENU)
    
    choice = input(f"\n{Font.COMMAND('Input command:')} ").strip()
    
    if choice == "1":
        # View active missions
        clear_screen()
        print_typed(f"{Font.HEADER('ACTIVE MISSIONS')}\n", style=Font.IMPORTANT)
        
        if not game_state["side_quests"]:
            print_typed("No active missions in your log.", style=Font.INFO)
            print_typed("Check the Mission Terminal for available assignments.", style=Font.INFO)
        else:
            for i, quest in enumerate(game_state["side_quests"]):
                print(f"{i+1}. {Font.SUBTITLE(quest['name'])}")
                print(f"   {Font.INFO(quest['description'])}")
                print(f"   {Font.SYSTEM('Objective:')} {quest['objective']}")
                print(f"   {Font.WEAPON('Reward:')} {quest['reward_desc']}")
                
                # Show progress for tracked quests
                if 'progress' in quest and 'target' in quest:
                    progress_percent = min(100, int((quest['progress'] / quest['target']) * 100))
                    progress_bar = '█' * (progress_percent // 10) + '░' * (10 - (progress_percent // 10))
                    print(f"   {Font.SYSTEM('Progress:')} [{progress_bar}] {progress_percent}%")
                print()
        
        input(f"\n{Font.COMMAND('Press Enter to return to Mission Terminal...')}")
        return side_quest_system(player, game_state)
    
    elif choice == "2":
        # Browse available assignments based on current zone
        clear_screen()
        print_typed(f"{Font.HEADER('AVAILABLE ASSIGNMENTS')}\n", style=Font.IMPORTANT)
        
        # Get available quests based on current zone and chapter
        available_quests = get_available_quests(game_state["current_zone"], game_state.get("chapter", 1))
        
        if not available_quests:
            print_typed("No assignments available in this area.", style=Font.INFO)
            print_typed("Try exploring different zones or progressing the main story.", style=Font.INFO)
        else:
            for i, quest in enumerate(available_quests):
                # Check if quest is already active
                already_active = any(q['id'] == quest['id'] for q in game_state["side_quests"])
                already_completed = any(q['id'] == quest['id'] for q in game_state["completed_quests"])
                
                if already_active:
                    status = f"{Fore.YELLOW}[ACTIVE]{Style.RESET_ALL}"
                elif already_completed:
                    status = f"{Fore.GREEN}[COMPLETED]{Style.RESET_ALL}"
                else:
                    status = f"{Fore.CYAN}[AVAILABLE]{Style.RESET_ALL}"
                
                print(f"{i+1}. {Font.SUBTITLE(quest['name'])} {status}")
                print(f"   {Font.INFO(quest['description'])}")
                print(f"   {Font.SYSTEM('Objective:')} {quest['objective']}")
                print(f"   {Font.WEAPON('Reward:')} {quest['reward_desc']}")
                print(f"   {Font.LORE('Source:')} {quest['giver']}")
                print()
            
            # Allow player to accept a quest
            print_typed("\nEnter quest number to accept, or 0 to return:", style=Font.COMMAND)
            try:
                quest_choice = int(input(f"{Font.COMMAND('Input:')} ").strip())
                if 1 <= quest_choice <= len(available_quests):
                    selected_quest = available_quests[quest_choice-1]
                    
                    # Check if already active or completed
                    if any(q['id'] == selected_quest['id'] for q in game_state["side_quests"]):
                        print_typed("\nThis assignment is already in your active mission log.", style=Font.WARNING)
                    elif any(q['id'] == selected_quest['id'] for q in game_state["completed_quests"]):
                        print_typed("\nYou have already completed this assignment.", style=Font.SUCCESS)
                    else:
                        # Add to active quests with initial progress
                        new_quest = selected_quest.copy()
                        if 'target' in new_quest:
                            new_quest['progress'] = 0
                        game_state["side_quests"].append(new_quest)
                        
                        print_typed(f"\n{Font.SUCCESS('Assignment accepted:')} {new_quest['name']}", style=Font.IMPORTANT)
                        print_typed("Details added to your mission log.", style=Font.SYSTEM)
                
                time.sleep(1)
            except ValueError:
                pass
        
        input(f"\n{Font.COMMAND('Press Enter to return to Mission Terminal...')}")
        return side_quest_system(player, game_state)
    
    elif choice == "3":
        # View completed missions
        clear_screen()
        print_typed(f"{Font.HEADER('COMPLETED MISSIONS')}\n", style=Font.SUCCESS)
        
        if not game_state["completed_quests"]:
            print_typed("No completed missions in your log.", style=Font.INFO)
        else:
            for i, quest in enumerate(game_state["completed_quests"]):
                print(f"{i+1}. {Font.SUBTITLE(quest['name'])}")
                print(f"   {Font.INFO(quest['description'])}")
                print(f"   {Font.SUCCESS('Status: Objective Complete')}")
                print(f"   {Font.WEAPON('Reward:')} {quest['reward_desc']}")
                print(f"   {Font.LORE('Source:')} {quest['giver']}")
                
                # Show date completed if tracked
                if 'completed_date' in quest:
                    print(f"   {Font.SYSTEM('Completed:')} {quest['completed_date']}")
                print()
        
        input(f"\n{Font.COMMAND('Press Enter to return to Mission Terminal...')}")
        return side_quest_system(player, game_state)
    
    elif choice == "4":
        # Turn in completed objectives
        clear_screen()
        print_typed(f"{Font.HEADER('TURN IN COMPLETED OBJECTIVES')}\n", style=Font.IMPORTANT)
        
        completed_but_not_turned_in = []
        for quest in game_state["side_quests"]:
            if 'progress' in quest and 'target' in quest and quest['progress'] >= quest['target']:
                completed_but_not_turned_in.append(quest)
        
        if not completed_but_not_turned_in:
            print_typed("No completed objectives ready to turn in.", style=Font.INFO)
            print_typed("Continue your missions to meet objectives.", style=Font.INFO)
        else:
            print_typed("The following assignments are ready to turn in:", style=Font.SUCCESS)
            for i, quest in enumerate(completed_but_not_turned_in):
                print(f"{i+1}. {Font.SUBTITLE(quest['name'])}")
                print(f"   {Font.INFO(quest['objective'])}")
                print(f"   {Font.SUCCESS('Status: COMPLETE')}")
                print(f"   {Font.WEAPON('Reward:')} {quest['reward_desc']}")
                print()
            
            # Allow player to turn in a quest
            print_typed("\nEnter quest number to turn in, or 0 to return:", style=Font.COMMAND)
            try:
                quest_choice = int(input(f"{Font.COMMAND('Input:')} ").strip())
                if 1 <= quest_choice <= len(completed_but_not_turned_in):
                    selected_quest = completed_but_not_turned_in[quest_choice-1]
                    
                    # Award rewards
                    print_typed(f"\n{Font.SUCCESS('MISSION COMPLETE:')} {selected_quest['name']}", style=Font.IMPORTANT)
                    print_typed("Receiving rewards:", style=Font.SYSTEM)
                    
                    # Apply rewards based on type
                    if selected_quest['reward_type'] == 'exp':
                        player.gain_experience(selected_quest['reward_value'])
                        print_typed(f"• {selected_quest['reward_value']} experience gained", style=Font.SUCCESS)
                    elif selected_quest['reward_type'] == 'item':
                        for item_name, item_count in selected_quest['reward_items'].items():
                            if item_name not in player.inventory:
                                player.inventory[item_name] = 0
                            player.inventory[item_name] += item_count
                            print_typed(f"• {item_count}x {item_name} added to inventory", style=Font.SUCCESS)
                    elif selected_quest['reward_type'] == 'credits':
                        game_state['credits'] = game_state.get('credits', 0) + selected_quest['reward_value']
                        print_typed(f"• {selected_quest['reward_value']} credits transferred to account", style=Font.SUCCESS)
                    elif selected_quest['reward_type'] == 'special':
                        # Handle special rewards like unlocking characters
                        handle_special_reward(player, game_state, selected_quest['reward_special'])
                    
                    # Move from active to completed
                    game_state["side_quests"].remove(selected_quest)
                    selected_quest['completed_date'] = "Day " + str(game_state.get('game_day', 1))
                    game_state["completed_quests"].append(selected_quest)
                    
                    print_typed("\nMission data transferred to completed records.", style=Font.SYSTEM)
                    time.sleep(2)
            except ValueError:
                pass
        
        input(f"\n{Font.COMMAND('Press Enter to return to Mission Terminal...')}")
        return side_quest_system(player, game_state)
    
    elif choice == "0":
        return False
    
    else:
        print_typed("\nInvalid selection. Please try again.", style=Font.WARNING)
        time.sleep(1)
        return side_quest_system(player, game_state)

def get_available_quests(current_zone, chapter):
    """Get available side quests based on current zone and chapter
    
    Args:
        current_zone: The current zone name
        chapter: The current chapter number
    
    Returns:
        list: List of available quest dictionaries
    """
    available_quests = []
    
    # Earth quests (Chapter 1)
    if chapter == 1:
        if "Laboratory" in current_zone:
            available_quests.append({
                'id': 'earth_lab_data',
                'name': 'Salvaging Research Data',
                'description': 'The facility\'s quantum data cores contain valuable research. Recover what you can.',
                'objective': 'Download data from 3 lab terminals',
                'target': 3,
                'giver': 'Emergency Protocol Subroutine',
                'reward_type': 'item',
                'reward_items': {'Neural Chip': 1, 'Data Fragment': 3},
                'reward_desc': 'Neural Chip upgrade + 3 Data Fragments',
                'zone_requirement': 'Laboratory'
            })
            
        if "Corridor" in current_zone:
            available_quests.append({
                'id': 'earth_drone_parts',
                'name': 'Salvaging Drone Components',
                'description': 'Several maintenance drones have been destroyed. Their components could be useful.',
                'objective': 'Collect 5 drone components',
                'target': 5,
                'giver': 'Facility Maintenance Protocol',
                'reward_type': 'exp',
                'reward_value': 200,
                'reward_desc': '200 XP + Improved hacking ability',
                'zone_requirement': 'Corridor'
            })
            
        if "Server Room" in current_zone:
            available_quests.append({
                'id': 'earth_ai_logs',
                'name': 'The Last Transmission',
                'description': 'The facility\'s logs may contain information about what happened to Earth.',
                'objective': 'Find and decrypt the final AI transmission log',
                'giver': 'Damaged Terminal Interface',
                'reward_type': 'special',
                'reward_special': 'earth_story_unlock',
                'reward_desc': 'Unlock additional story revelations + 150 XP',
                'zone_requirement': 'Server Room'
            })
    
    # Yanglong V quests (Chapter 2)
    elif chapter == 2:
        if "Mining Outpost" in current_zone:
            available_quests.append({
                'id': 'yanglong_rare_mineral',
                'name': 'Rare Mineral Extraction',
                'description': 'The mining outpost contains rare quantum-stable minerals that could enhance your weapons.',
                'objective': 'Collect 7 Quantum Crystal samples',
                'target': 7,
                'giver': 'Abandoned Mining Terminal',
                'reward_type': 'item',
                'reward_items': {'Quantum Stabilizer': 1, 'Shield Matrix': 2},
                'reward_desc': 'Quantum Stabilizer + 2 Shield Matrices',
                'zone_requirement': 'Mining Outpost'
            })
            
        if "Colony Ruins" in current_zone:
            available_quests.append({
                'id': 'yanglong_survivors',
                'name': 'Lost Colony Survivors',
                'description': 'There may be survivors from the colony hidden in emergency bunkers.',
                'objective': 'Locate and check 3 emergency bunkers',
                'target': 3,
                'giver': 'Colony Emergency Beacon',
                'reward_type': 'exp',
                'reward_value': 300,
                'reward_desc': '300 XP + Survival Technique Upgrade',
                'zone_requirement': 'Colony Ruins'
            })
    
    # White Hole quests (Chapter 3)
    elif chapter == 3:
        if "Reality Fracture" in current_zone:
            available_quests.append({
                'id': 'whitehole_stabilize',
                'name': 'Reality Stabilization',
                'description': 'The White Hole is destabilizing local reality. Place quantum anchors to stabilize the region.',
                'objective': 'Place 5 quantum anchors at designated coordinates',
                'target': 5,
                'giver': 'Quantum Physicist Echo',
                'reward_type': 'item',
                'reward_items': {'Reality Shard': 3, 'Dimensional Key': 1},
                'reward_desc': '3 Reality Shards + Dimensional Key',
                'zone_requirement': 'Reality Fracture'
            })
    
    # Thalassia 1 quests (Chapter 4)
    elif chapter == 4:
        if "Underwater Research" in current_zone:
            available_quests.append({
                'id': 'thalassia_specimens',
                'name': 'Xenobiological Specimens',
                'description': 'The unique salt-based lifeforms on Thalassia 1 have remarkable properties. Collect specimens for analysis.',
                'objective': 'Collect 6 salt-life specimens',
                'target': 6,
                'giver': 'Research Database Fragment',
                'reward_type': 'item',
                'reward_items': {'Bio-Enhancer': 1, 'Salt Crystal': 4},
                'reward_desc': 'Bio-Enhancer + 4 Salt Crystals',
                'zone_requirement': 'Underwater Research'
            })
    
    # H-79760 System quests (Chapter 5)
    elif chapter == 5:
        if "Terminus" in current_zone:
            available_quests.append({
                'id': 'terminus_beacon',
                'name': 'Emergency Beacon Network',
                'description': 'Setting up a network of emergency beacons could help any survivors in the system.',
                'objective': 'Install 4 emergency beacons across Terminus',
                'target': 4,
                'giver': 'Emergency Communication System',
                'reward_type': 'credits',
                'reward_value': 500,
                'reward_desc': '500 Credits + Enhanced Communications',
                'zone_requirement': 'Terminus'
            })
            
        if "Novaris" in current_zone:
            available_quests.append({
                'id': 'novaris_water',
                'name': 'Water Reclamation Project',
                'description': 'Novaris is critically low on water. Ancient aquifers may still exist deep underground.',
                'objective': 'Locate and tap 3 underground aquifers',
                'target': 3,
                'giver': 'Dehydrated Survivor',
                'reward_type': 'exp',
                'reward_value': 400,
                'reward_desc': '400 XP + Survival Skill Enhancement',
                'zone_requirement': 'Novaris'
            })
    
    # Paradox Horizon quests (Chapter 6)
    elif chapter == 6:
        if "Temporal Anomaly" in current_zone:
            available_quests.append({
                'id': 'paradox_echoes',
                'name': 'Temporal Echoes',
                'description': 'Time-displaced echoes of past events are scattered throughout the anomaly. Recording them could provide valuable insights.',
                'objective': 'Record 5 temporal echoes',
                'target': 5,
                'giver': 'Paradox Researcher Echo',
                'reward_type': 'item',
                'reward_items': {'Chronon Stabilizer': 1, 'Time Fragment': 3},
                'reward_desc': 'Chronon Stabilizer + 3 Time Fragments',
                'zone_requirement': 'Temporal Anomaly'
            })
    
    # Primor Aetherium quests (Chapter 7)
    elif chapter == 7:
        if "Primor Aetherium" in current_zone:
            available_quests.append({
                'id': 'primor_void_intel',
                'name': 'Void Harmonic Intelligence',
                'description': 'Gather intelligence on Void Harmonic movement and plans to help the Yitrian defense.',
                'objective': 'Collect 6 Void Harmonic data packets',
                'target': 6,
                'giver': 'Vex-Na, Yitrian Ambassador',
                'reward_type': 'item',
                'reward_items': {'Yitrian Shield Module': 1, 'Non-Euclidean Schematics': 2},
                'reward_desc': 'Yitrian Shield Module + 2 Non-Euclidean Schematics',
                'zone_requirement': 'Primor Aetherium'
            })
            
            available_quests.append({
                'id': 'primor_civilians',
                'name': 'Civilian Evacuation',
                'description': 'Void Harmonic forces have occupied the Eastern District. Civilians need evacuation to safe zones.',
                'objective': 'Evacuate 8 Yitrian civilian groups',
                'target': 8,
                'giver': 'Yitrian Security Officer',
                'reward_type': 'credits',
                'reward_value': 800,
                'reward_desc': '800 Credits + Increased Yitrian Trust',
                'zone_requirement': 'Primor Aetherium'
            })
    
    return available_quests

def handle_special_reward(player, game_state, reward_id):
    """Handle special rewards from quests
    
    Args:
        player: The player character
        game_state: The current game state
        reward_id: The ID of the special reward
    
    Returns:
        None
    """
    if reward_id == 'earth_story_unlock':
        print_typed("• Unlocked additional Earth story content", style=Font.SUCCESS)
        print_typed("• +150 XP gained", style=Font.SUCCESS)
        player.gain_experience(150)
        game_state['earth_extended_story'] = True
    
    elif reward_id == 'hyuki_encounter':
        print_typed("• Unlocked special encounter with Hyuki", style=Font.SUCCESS)
        print_typed("• +300 XP gained", style=Font.SUCCESS)
        player.gain_experience(300)
        game_state['hyuki_encounter_available'] = True
    
    # Add other special rewards as needed

def manage_companions(player):
    """Manage and view active companions"""
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('COMPANION MANAGEMENT SYSTEM'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    if not game_state["companions"]:
        print_typed("No companions currently active.", style=Font.WARNING)
        print_typed("Use the Fabrication System to build companions.", style=Font.INFO)
        print(Font.MENU("\nPress Enter to continue..."))
        input()
        return

    total_attack_bonus = 0
    total_defense_bonus = 0

    print(Font.HEADER("\nACTIVE COMPANIONS:"))
    print(Font.SEPARATOR_THIN)

    for comp_id in game_state["companions"]:
        if comp_id in companions:
            comp_data = companions[comp_id]
            tier_color = Font.COMPANION_TIERS[comp_data["tier"]]

            # Create a box for each companion
            comp_name = comp_data['name']
            comp_tier = comp_data['tier']
            comp_desc = comp_data['description']
            attack_bonus = comp_data['attack_bonus']
            defense_bonus = comp_data['defense_bonus']

            print(f"\n{tier_color}{comp_name}{Style.RESET_ALL} ({tier_color}Tier {comp_tier}{Style.RESET_ALL})")
            print(f"{Font.LORE(comp_desc)}")
            print(f"{Font.COMMAND('Attack Bonus:')} {Font.SUCCESS(f'+{attack_bonus}')}")
            print(f"{Font.COMMAND('Defense Bonus:')} {Font.SUCCESS(f'+{defense_bonus}')}")
            print(f"{Font.INFO('Special Abilities:')} {Font.IMPORTANT(', '.join(comp_data['abilities']))}")
            print(Font.SEPARATOR_THIN)

            total_attack_bonus += comp_data["attack_bonus"]
            total_defense_bonus += comp_data["defense_bonus"]

    # Summary box with total bonuses
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('TOTAL COMBAT BONUSES'.center(46))} {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} Attack: {Font.SUCCESS(f'+{total_attack_bonus}')} | Defense: {Font.SUCCESS(f'+{total_defense_bonus}')} {' ' * (20)} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    # Provide additional information about companions
    print(Font.INFO("\nCompanions provide passive bonuses during combat."))
    print(Font.INFO("Build more advanced companions as you progress to higher stages."))

    print(Font.MENU("\nPress Enter to continue..."))
    input()


def flee_battle():
    """Attempt to flee from battle"""
    # 70% base chance to successfully flee
    flee_chance = 0.7

    # Reduce chance based on current stage (higher stages are harder to flee)
    current_stage = game_state["current_stage"]
    stage_penalty = min(0.3, current_stage / 100)  # Max 30% penalty at stage 30+
    flee_chance -= stage_penalty

    # Check if any companions boost escape chance
    companion_bonus = 0
    for comp_id in game_state["companions"]:
        if comp_id == "infiltrator_model":  # Infiltrator helps with escape
            flee_chance += 0.15
            companion_bonus = 0.15
            break

    # Display flee attempt with visual feedback
    print(Font.SEPARATOR_THIN)
    print(Font.HEADER("\nTACTICAL RETREAT ANALYSIS:"))
    print(f"{Font.INFO('Base Success Rate:')} {Font.SUCCESS('70%')}")
    print(f"{Font.INFO('Stage Penalty:')} {Font.WARNING(f'-{int(stage_penalty*100)}%')} (Stage {current_stage})")

    if companion_bonus > 0:
        print(f"{Font.INFO('Infiltrator Bonus:')} {Font.SUCCESS(f'+{int(companion_bonus*100)}%')}")

    print(f"{Font.INFO('Final Success Chance:')} {Font.IMPORTANT(f'{int(flee_chance*100)}%')}")
    print(Font.SEPARATOR_THIN)

    print_typed("\nInitiating tactical retreat sequence...", style=Font.SYSTEM)
    time.sleep(0.5)

    if random.random() < flee_chance:
        # Successful escape
        game_state["player_stats"]["fled_battles"] += 1

        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUCCESS('TACTICAL RETREAT SUCCESSFUL'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)

        print_slow("Deploying countermeasures...", style=Font.SYSTEM)
        print_typed("Escape successful! You've disengaged from combat.", style=Font.SUCCESS)
        return True
    else:
        # Failed escape
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.WARNING('TACTICAL RETREAT FAILED'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)

        print_typed("Enemy intercepted your retreat!", style=Font.WARNING)
        print_typed("Preparing for enemy counterattack...", style=Font.ENEMY)
        return False


def show_game_stats():
    """Display game statistics in a sci-fi themed display"""
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('NEURAL ARCHIVE: MISSION STATISTICS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    stats = game_state["player_stats"]

    print(Font.HEADER("\nCURRENT MISSION STATUS:"))

    chapter = game_state["chapter"]
    current_stage = game_state["current_stage"]
    current_zone = game_state["current_zone"]

    print(f"{Font.INFO('Chapter:')} {Font.STAGE(str(chapter))}")
    print(f"{Font.INFO('Current Stage:')} {Font.STAGE(f'{current_stage}/50')}")
    print(f"{Font.INFO('Current Zone:')} {Font.SUBTITLE(current_zone)}")

    print(Font.SEPARATOR_THIN)
    print(Font.HEADER("\nCOMBAT METRICS:"))

    # Extract values from stats dictionary
    enemies_defeated = stats["enemies_defeated"]
    damage_dealt = stats["damage_dealt"]
    damage_taken = stats["damage_taken"]
    fled_battles = stats["fled_battles"]

    print(f"{Font.INFO('Enemies Neutralized:')} {Font.SUCCESS(str(enemies_defeated))}")
    print(f"{Font.INFO('Total Damage Dealt:')} {Font.ENEMY(str(damage_dealt))}")
    print(f"{Font.INFO('Damage Sustained:')} {Font.HEALTH(str(damage_taken))}")
    print(f"{Font.INFO('Tactical Retreats:')} {Font.ITEM(str(fled_battles))}")

    print(Font.SEPARATOR_THIN)
    print(Font.HEADER("\nRESOURCE ACQUISITION:"))

    # Extract more values
    items_found = stats["items_found"]
    companions_built = stats["companions_built"]
    stages_completed = stats["stages_completed"]

    print(f"{Font.INFO('Items Recovered:')} {Font.ITEM(str(items_found))}")
    print(f"{Font.INFO('Companions Constructed:')} {Font.SUCCESS(str(companions_built))}")

    print(Font.SEPARATOR_THIN)
    print(Font.HEADER("\nMISSION PROGRESS:"))
    print(f"{Font.INFO('Stages Completed:')} {Font.STAGE(str(stages_completed))}")

    completed_quests = sum(1 for progress in game_state["quest_progress"].values() if progress == 2)
    total_quests = len(game_state["quest_progress"])
    print(f"{Font.INFO('Quests Completed:')} {Font.SUCCESS(f'{completed_quests}/{total_quests}')}")

    print(Font.SEPARATOR)
    print(Font.MENU("\nPress Enter to continue..."))
    input()


def use_time_manipulation(player, enemy, combat_state):
    """Use time fragments to manipulate time during combat
    
    Args:
        player: The player character
        enemy: The enemy character
        combat_state: The current state of combat
        
    Returns:
        bool: True if a time ability was used, False otherwise
    """
    if game_state.get("time_fragments", 0) <= 0:
        print_typed("\nYou have no time fragments to use for temporal manipulation.", style=Font.WARNING)
        return False
    
    clear_screen()
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('TEMPORAL MANIPULATION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed(f"\nAvailable Time Fragments: {Font.SUCCESS(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
    print_typed("\nYou can use time fragments to manipulate the flow of time in combat.", style=Font.INFO)
    
    print(f"\n{Font.MENU('Available Temporal Abilities:')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Rewind (3 fragments)')} - Reverse the last enemy attack")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Accelerate (2 fragments)')} - Take an additional action this turn")
    print(f"{Font.COMMAND('3.')} {Font.INFO('Glimpse (1 fragment)')} - See the enemy's next attack")
    print(f"{Font.COMMAND('4.')} {Font.INFO('Time Stop (5 fragments)')} - Freeze time and attack with guaranteed critical")
    
    if game_state["protagonist"]["name"] == "Hyuki Nakamura":
        print(f"{Font.COMMAND('5.')} {Font.SUCCESS('[Hyuki Special] Timeline Shift (4 fragments)')} - Switch to an alternate timeline version of this battle")
        valid_choices = ["1", "2", "3", "4", "5", "0"]
    else:
        valid_choices = ["1", "2", "3", "4", "0"]
    
    print(f"{Font.COMMAND('0.')} {Font.INFO('Return to combat menu')}")
    
    choice = ""
    while choice not in valid_choices:
        choice = input(f"\n{Font.MENU('Select temporal ability:')} ").strip()
    
    if choice == "0":
        return False
    
    # Rewind
    if choice == "1":
        if game_state.get("time_fragments", 0) >= 3:
            if combat_state.get("last_enemy_damage", 0) > 0:
                print_typed("\nYou focus on your time fragments, which begin to glow with", style=Font.PLAYER)
                print_typed("otherworldly energy. The air around you ripples as you pull", style=Font.PLAYER)
                print_typed("the local timeline backward.", style=Font.PLAYER)
                
                print_glitch(">>> REWINDING TIMELINE <<<")
                time.sleep(1)
                
                # Restore player health from last enemy attack
                last_damage = combat_state.get("last_enemy_damage", 0)
                player.health += last_damage
                
                game_state["time_fragments"] -= 3
                
                print_typed(f"\nTime rewinds to before the enemy's attack. You regain {Font.SUCCESS(str(last_damage))} health!", style=Font.SUCCESS)
                print_typed(f"Time Fragments remaining: {Font.INFO(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
                time.sleep(1)
                return True
            else:
                print_typed("\nThere is no enemy attack to rewind.", style=Font.WARNING)
                return False
        else:
            print_typed("\nYou don't have enough time fragments for this ability.", style=Font.WARNING)
            return False
    
    # Accelerate
    elif choice == "2":
        if game_state.get("time_fragments", 0) >= 2:
            print_typed("\nYou channel the energy of your time fragments, accelerating your", style=Font.PLAYER)
            print_typed("personal timeline. To the enemy, you appear to move at impossible speeds.", style=Font.PLAYER)
            
            print_glitch(">>> ACCELERATING TIMELINE <<<")
            time.sleep(1)
            
            # Grant an extra action
            combat_state["extra_action"] = True
            game_state["time_fragments"] -= 2
            
            print_typed("\nTime accelerates around you, granting an additional action this turn!", style=Font.SUCCESS)
            print_typed(f"Time Fragments remaining: {Font.INFO(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
            time.sleep(1)
            return True
        else:
            print_typed("\nYou don't have enough time fragments for this ability.", style=Font.WARNING)
            return False
    
    # Glimpse
    elif choice == "3":
        if game_state.get("time_fragments", 0) >= 1:
            print_typed("\nYou focus on a single time fragment, which gives you a brief glimpse", style=Font.PLAYER)
            print_typed("into the immediate future.", style=Font.PLAYER)
            
            print_glitch(">>> GLIMPSING FUTURE TIMELINE <<<")
            time.sleep(1)
            
            # Determine enemy's next attack
            next_attack = random.choice(["melee", "ranged", "special"])
            damage_preview = max(1, enemy.attack - player.defense // 2)
            
            if next_attack == "melee":
                print_typed(f"\nVision: {Font.ENEMY(enemy.name)} will use a melee attack next turn,", style=Font.GLITCH)
                print_typed(f"dealing approximately {Font.WARNING(str(damage_preview))} damage.", style=Font.GLITCH)
            elif next_attack == "ranged":
                print_typed(f"\nVision: {Font.ENEMY(enemy.name)} will use a ranged attack next turn,", style=Font.GLITCH)
                print_typed(f"dealing approximately {Font.WARNING(str(damage_preview))} damage.", style=Font.GLITCH)
            else:
                print_typed(f"\nVision: {Font.ENEMY(enemy.name)} will use a special ability next turn,", style=Font.GLITCH)
                print_typed("with unknown effects.", style=Font.GLITCH)
            
            # Set enemy's next attack to match the vision
            combat_state["enemy_next_attack"] = next_attack
            game_state["time_fragments"] -= 1
            
            print_typed(f"\nTime Fragments remaining: {Font.INFO(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
            time.sleep(1)
            return True
        else:
            print_typed("\nYou don't have enough time fragments for this ability.", style=Font.WARNING)
            return False
    
    # Time Stop
    elif choice == "4":
        if game_state.get("time_fragments", 0) >= 5:
            print_typed("\nYou focus intensely on all your time fragments. They orbit around you", style=Font.PLAYER)
            print_typed("in a complex pattern before merging into a brilliant flash of light.", style=Font.PLAYER)
            
            print_glitch(">>> STOPPING TIME <<<")
            time.sleep(1)
            
            print_typed("\nTime freezes completely around you. The enemy is motionless, suspended", style=Font.LORE)
            print_typed("in a single moment. You carefully line up the perfect attack.", style=Font.LORE)
            
            # Calculate critical damage
            critical_damage = player.attack * 2
            enemy.health -= critical_damage
            
            game_state["time_fragments"] -= 5
            
            print_typed(f"\nYou deal {Font.SUCCESS(str(critical_damage))} critical damage while time is frozen!", style=Font.SUCCESS)
            print_typed(f"Time Fragments remaining: {Font.INFO(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
            
            print_glitch(">>> TIME RESUMES <<<")
            time.sleep(1)
            return True
        else:
            print_typed("\nYou don't have enough time fragments for this ability.", style=Font.WARNING)
            return False
    
    # Timeline Shift (Hyuki Special)
    elif choice == "5" and game_state["protagonist"]["name"] == "Hyuki Nakamura":
        if game_state.get("time_fragments", 0) >= 4:
            print_typed("\nHyuki's eyes glow with quantum energy as she manipulates the temporal", style=Font.PLAYER)
            print_typed("fragments in ways only she understands, reaching out to an alternate", style=Font.PLAYER)
            print_typed("timeline where this battle is progressing more favorably.", style=Font.PLAYER)
            
            print_glitch(">>> SHIFTING TIMELINES <<<")
            time.sleep(1)
            
            # Reset the battle state favorably
            health_boost = player.max_health // 3
            player.health = min(player.max_health, player.health + health_boost)
            
            # Enemy suffers a temporal disruption
            temporal_damage = enemy.max_health // 4
            enemy.health -= temporal_damage
            
            # Apply confusion status to enemy
            enemy.status_effects.append({
                "name": "temporal_disruption",
                "duration": 3,
                "effect": "confused"
            })
            
            game_state["time_fragments"] -= 4
            
            print_typed(f"\nYou shift to a more favorable timeline! You recover {Font.SUCCESS(str(health_boost))} health", style=Font.SUCCESS)
            print_typed(f"and {Font.ENEMY(enemy.name)} takes {Font.SUCCESS(str(temporal_damage))} damage from temporal disruption!", style=Font.SUCCESS)
            print_typed("The enemy is confused for 3 turns due to timeline inconsistency.", style=Font.SUCCESS)
            print_typed(f"Time Fragments remaining: {Font.INFO(str(game_state.get('time_fragments', 0)))}", style=Font.INFO)
            time.sleep(1)
            return True
        else:
            print_typed("\nYou don't have enough time fragments for this ability.", style=Font.WARNING)
            return False
    
    return False

def get_branching_story_choices(zone_name, chapter, game_state):
    """Get available story branch choices based on current zone and story progression
    
    Args:
        zone_name: Current zone name
        chapter: Current chapter number
        game_state: The game state containing story flags
    
    Returns:
        list: Available story branch choices with descriptions and consequences
    """
    choices = []
    
    # Chapter 1 - Earth branching choices
    if chapter == 1:
        if "Server Room" in zone_name and game_state.get("malware_server_defeated", False):
            choices.append({
                'id': 'earth_escape_method',
                'prompt': 'How will you escape Earth?',
                'description': 'With the Malware Server defeated, you need to choose your escape method.',
                'options': [
                    {
                        'text': 'Use the quantum teleporter to reach Yanglong V directly',
                        'consequence': 'Faster travel but arrive with damaged equipment',
                        'flag': 'quantum_teleport_escape'
                    },
                    {
                        'text': 'Take the shuttle for a conventional space journey',
                        'consequence': 'Slower travel but opportunity to salvage more resources en route',
                        'flag': 'shuttle_escape'
                    },
                    {
                        'text': 'Send distress signal and wait for potential rescue',
                        'consequence': 'Uncertain wait time, but possibility of finding other survivors',
                        'flag': 'distress_signal_escape'
                    }
                ]
            })
    
    # Chapter 2 - Yanglong V branching choices
    elif chapter == 2:
        if "Colony Center" in zone_name and game_state.get("colony_explored", False):
            choices.append({
                'id': 'yanglong_colony_approach',
                'prompt': 'How will you approach the abandoned colony?',
                'description': 'The colony shows signs of both human and alien technology. Your approach will determine what you find.',
                'options': [
                    {
                        'text': 'Scientific investigation - analyze the technology integration',
                        'consequence': 'Gain technological insights but risk activating dangerous systems',
                        'flag': 'scientific_colony_approach'
                    },
                    {
                        'text': 'Military reconnaissance - secure the area before exploration',
                        'consequence': 'Safer exploration but miss subtle technological details',
                        'flag': 'military_colony_approach'
                    },
                    {
                        'text': 'Archaeological approach - focus on reconstructing the colony\'s history',
                        'consequence': 'Discover historical insights but slower progress',
                        'flag': 'archaeological_colony_approach'
                    }
                ]
            })
    
    # Chapter 3 - White Hole branching choices  
    elif chapter == 3:
        if "Core Nexus" in zone_name and not game_state.get("white_hole_decision_made", False):
            choices.append({
                'id': 'white_hole_approach',
                'prompt': 'How will you navigate the White Hole reality?',
                'description': 'The White Hole distorts conventional physics. Your approach affects your journey.',
                'options': [
                    {
                        'text': 'Embrace the chaos - allow the white hole to guide your path',
                        'consequence': 'Unpredictable journey but potential for unique discoveries',
                        'flag': 'embrace_chaos_approach'
                    },
                    {
                        'text': 'Resist the anomalies - attempt to maintain conventional physics',
                        'consequence': 'More stable journey but requires constant effort and energy',
                        'flag': 'resist_anomalies_approach'
                    },
                    {
                        'text': 'Adaptive approach - selectively interact with anomalies',
                        'consequence': 'Balanced approach with moderate stability and discoveries',
                        'flag': 'adaptive_anomalies_approach'
                    }
                ]
            })
    
    # Chapter 4 - Thalassia 1 branching choices
    elif chapter == 4:
        if "Underwater Research" in zone_name and game_state.get("neurovore_encountered", False):
            choices.append({
                'id': 'thalassia_neurovore',
                'prompt': 'How will you deal with the Neurovore threat?',
                'description': 'The Neurovores are psychic predators that consume consciousness. They can be approached in different ways.',
                'options': [
                    {
                        'text': 'Elimination - destroy the Neurovore nest completely',
                        'consequence': 'Safest option but potentially destroys unique lifeforms',
                        'flag': 'eliminate_neurovores'
                    },
                    {
                        'text': 'Containment - seal the Neurovores in their current location',
                        'consequence': 'Preserves the species but requires maintaining containment',
                        'flag': 'contain_neurovores'
                    },
                    {
                        'text': 'Communication - attempt to establish psychic contact',
                        'consequence': 'Could lead to understanding but high risk of mental damage',
                        'flag': 'communicate_neurovores'
                    }
                ]
            })
    
    # Chapter 5 - H-79760 System branching choices
    elif chapter == 5:
        if game_state.get("h79760_planets_visited", 0) >= 3 and not game_state.get("h79760_path_chosen", False):
            choices.append({
                'id': 'h79760_exploration',
                'prompt': 'How will you continue your system exploration?',
                'description': 'With several planets explored, you must decide how to proceed in the H-79760 system.',
                'options': [
                    {
                        'text': 'Focus on finding human survivors',
                        'consequence': 'Prioritize habitable planets and rescue operations',
                        'flag': 'survivor_focus'
                    },
                    {
                        'text': 'Focus on technological discoveries',
                        'consequence': 'Prioritize planets with advanced technology signatures',
                        'flag': 'technology_focus'
                    },
                    {
                        'text': 'Focus on understanding the local ecosystem',
                        'consequence': 'Study the unique planetary interactions in this system',
                        'flag': 'ecosystem_focus'
                    }
                ]
            })
    
    # Chapter 6 - Paradox Horizon branching choices
    elif chapter == 6:
        if "Temporal Anomaly" in zone_name and game_state.get("chrono_sentient_encountered", False):
            choices.append({
                'id': 'chrono_sentient_approach',
                'prompt': 'How will you interact with the Chrono-Sentient?',
                'description': 'The interdimensional Chrono-Sentient offers multiple paths of interaction.',
                'options': [
                    {
                        'text': 'Request knowledge of the past',
                        'consequence': 'Learn historical truths about Earth\'s fall',
                        'flag': 'past_knowledge_request'
                    },
                    {
                        'text': 'Request glimpses of potential futures',
                        'consequence': 'Gain insights into possible outcomes of your journey',
                        'flag': 'future_glimpse_request'
                    },
                    {
                        'text': 'Request temporal manipulation abilities',
                        'consequence': 'Enhance your ability to control time in limited ways',
                        'flag': 'temporal_ability_request'
                    }
                ]
            })
    
    # Chapter 7 - Primor Aetherium branching choices
    elif chapter == 7:
        if "Primor Aetherium" in zone_name and game_state.get("void_harmonic_conflict", False):
            choices.append({
                'id': 'void_harmonic_approach',
                'prompt': 'How will you address the Void Harmonic threat?',
                'description': 'The Void Harmonics seek to unify consciousness. Your approach will determine Primor\'s fate.',
                'options': [
                    {
                        'text': 'Direct confrontation - engage their leadership directly',
                        'consequence': 'High-risk approach but potential for decisive victory',
                        'flag': 'confront_void_harmonics'
                    },
                    {
                        'text': 'Subversion - infiltrate their ranks to undermine from within',
                        'consequence': 'Slower approach but safer and may avoid widespread conflict',
                        'flag': 'subvert_void_harmonics'
                    },
                    {
                        'text': 'Diplomatic approach - attempt to negotiate with moderate factions',
                        'consequence': 'Could prevent conflict but requires compromises',
                        'flag': 'negotiate_void_harmonics'
                    }
                ]
            })
    
    return choices

def present_branching_choice(choice_data, game_state):
    """Present a branching story choice to the player
    
    Args:
        choice_data: The choice data structure with options
        game_state: The game state to update based on choice
    
    Returns:
        str: The flag representing the player's choice
    """
    clear_screen()
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('CRITICAL DECISION POINT'.center(46))} {Font.BOX_SIDE}")
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed(f"\n{Font.IMPORTANT(choice_data['prompt'])}", style=Font.HEADER)
    print_typed(f"\n{choice_data['description']}", style=Font.LORE)
    
    print_typed("\nYour decision will have lasting consequences on your journey:", style=Font.WARNING)
    print()
    
    # Display options with consequences
    for i, option in enumerate(choice_data['options']):
        print(f"{i+1}. {Font.SUBTITLE(option['text'])}")
        print(f"   {Font.INFO(option['consequence'])}")
        print()
    
    # Get player choice
    valid_choice = False
    selected_flag = None
    
    while not valid_choice:
        try:
            options_count = len(choice_data['options'])
            choice_num = int(input(f"{Font.COMMAND('Enter your choice (1-'+str(options_count)+'):')} "))
            if 1 <= choice_num <= len(choice_data['options']):
                valid_choice = True
                selected_option = choice_data['options'][choice_num-1]
                selected_flag = selected_option['flag']
                
                # Set the flag in game state
                game_state[selected_flag] = True
                
                # Set a flag to indicate this branch was decided
                game_state[f"{choice_data['id']}_decided"] = True
                
                # Display the result of the choice
                print_typed(f"\n{Font.IMPORTANT('You chose:')} {selected_option['text']}", style=Font.SYSTEM)
                print_typed(f"\n{Font.INFO('Your decision will alter the course of your journey...')}", style=Font.LORE)
                time.sleep(2)
            else:
                print_typed("\nInvalid choice. Please select a valid option.", style=Font.WARNING)
        except ValueError:
            print_typed("\nInvalid input. Please enter a number.", style=Font.WARNING)
    
    return selected_flag

def check_and_process_branching_stories(player, game_state):
    """Check if any branching story points are available and process them
    
    Args:
        player: The player character
        game_state: The current game state
    
    Returns:
        bool: True if a branch was processed, False otherwise
    """
    # Get current zone and chapter
    current_zone = game_state.get("current_zone", "")
    current_chapter = game_state.get("chapter", 1)
    
    # Get available choices for current zone/chapter
    available_choices = get_branching_story_choices(current_zone, current_chapter, game_state)
    
    if available_choices:
        # Process the first available choice
        choice = available_choices[0]
        
        # Check if this choice was already decided
        if not game_state.get(f"{choice['id']}_decided", False):
            selected_flag = present_branching_choice(choice, game_state)
            
            # Process the consequences of the choice
            process_branching_consequences(selected_flag, player, game_state)
            
            return True
    
    return False

def process_branching_consequences(selected_flag, player, game_state):
    """Process the consequences of a branching story choice
    
    Args:
        selected_flag: The flag representing the player's choice
        player: The player character
        game_state: The current game state
    """
    # Earth escape method consequences
    if selected_flag == 'quantum_teleport_escape':
        print_typed("\nYou activate the quantum teleporter...", style=Font.SYSTEM)
        print_typed("The world dissolves around you in a cascade of blue light.", style=Font.PLAYER)
        print_typed("When your vision clears, you find yourself on Yanglong V.", style=Font.PLAYER)
        
        # Apply consequences
        print_typed("\nYour equipment suffered damage during teleportation:", style=Font.WARNING)
        print_typed("- Shield capacity reduced by 20%", style=Font.WARNING)
        print_typed("- Scanner range decreased", style=Font.WARNING)
        
        # Update player stats
        if "shield_max" in game_state:
            game_state["shield_max"] = int(game_state["shield_max"] * 0.8)
        game_state["scanner_degraded"] = True
        
        # But provide a benefit
        print_typed("\nHowever, the teleportation was instantaneous:", style=Font.SUCCESS)
        print_typed("- Arrived at Yanglong V without aging", style=Font.SUCCESS)
        print_typed("- Quantum particles in your body slightly enhanced", style=Font.SUCCESS)
        
        # Update player stats positively too
        player.defense += 5  # Quantum particle enhancement
    
    elif selected_flag == 'shuttle_escape':
        print_typed("\nYou board the shuttle and initiate launch sequence...", style=Font.SYSTEM)
        print_typed("The engines roar to life as you break free of Earth's atmosphere.", style=Font.PLAYER)
        print_typed("The journey to Yanglong V will take several days.", style=Font.PLAYER)
        
        # Apply consequences
        print_typed("\nDuring your journey, you discover several useful items:", style=Font.SUCCESS)
        print_typed("- Additional med-kits in the storage compartment", style=Font.SUCCESS)
        print_typed("- Spare parts to enhance your equipment", style=Font.SUCCESS)
        
        # Update player inventory
        if "med_kit" not in player.inventory:
            player.inventory["med_kit"] = 0
        player.inventory["med_kit"] += 3
        
        if "spare_parts" not in player.inventory:
            player.inventory["spare_parts"] = 0
        player.inventory["spare_parts"] += 5
        
        print_typed("\nYou've had time to study the ship's database:", style=Font.SUCCESS)
        print_typed("- Gained knowledge about Yanglong V's geography", style=Font.SUCCESS)
        print_typed("- Unlocked additional navigation options", style=Font.SUCCESS)
        
        game_state["yanglong_map_unlocked"] = True
    
    # Neurovore approach consequences
    elif selected_flag == 'eliminate_neurovores':
        print_typed("\nYou set charges throughout the Neurovore nest...", style=Font.SYSTEM)
        print_typed("The explosions seal the caverns, destroying the psychic predators.", style=Font.PLAYER)
        print_typed("You feel a psychic shockwave as their collective consciousness is extinguished.", style=Font.PLAYER)
        
        # Apply consequences
        print_typed("\nThe Neurovore threat has been eliminated:", style=Font.SUCCESS)
        print_typed("- Research facility secured", style=Font.SUCCESS)
        print_typed("- No further mental attacks will occur", style=Font.SUCCESS)
        
        game_state["neurovores_eliminated"] = True
        
        # But add a consequence
        print_typed("\nHowever, with the species destroyed:", style=Font.WARNING)
        print_typed("- Unique research opportunity lost", style=Font.WARNING)
        print_typed("- Thalassian ecosystem may be disrupted", style=Font.WARNING)
        
        game_state["thalassia_ecosystem_disrupted"] = True
    
    # Chrono-Sentient approach consequences
    elif selected_flag == 'temporal_ability_request':
        print_typed("\nThe Chrono-Sentient's form ripples as it considers your request...", style=Font.SYSTEM)
        print_typed("\"Time is not to be handled lightly, but I sense your need is great.\"", style=Font.IMPORTANT)
        print_typed("The entity extends a tendril of temporal energy that merges with your consciousness.", style=Font.PLAYER)
        
        # Apply consequences
        print_typed("\nYou have gained temporal manipulation abilities:", style=Font.SUCCESS)
        print_typed("- Can now manipulate time in limited ways during combat", style=Font.SUCCESS)
        print_typed("- Gained 10 time fragments to power temporal abilities", style=Font.SUCCESS)
        
        # Update game state
        game_state["time_fragments"] = game_state.get("time_fragments", 0) + 10
        game_state["temporal_abilities_unlocked"] = True
        
        # But add a consequence
        print_typed("\nHowever, your connection to normal time flow has been altered:", style=Font.WARNING)
        print_typed("- Occasionally experience temporal echoes", style=Font.WARNING)
        print_typed("- May sometimes see events before they happen", style=Font.WARNING)
        
        game_state["temporal_echoes"] = True
    
    # Add more consequences for other branching choices here
    
    # Allow player to continue
    input("\nPress Enter to continue...")

def chapter_eight_teaser():
    """Display teaser for Chapter 8: Mitsurai D and Heliostadt III"""
    clear_screen()
    
    # Create a dramatic chapter transition with enhanced visuals
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 8: VIRAL DIRECTIVE'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    # Setting the scene with rich description
    print_typed("\nAs you depart from the crystalline geometries of Primor Aetherium,", style=Font.LORE)
    print_typed("your ship's sensors detect an automated distress beacon. The signal", style=Font.LORE)
    print_typed("originates from two locations - Mitsurai D, a small jungle planet, and", style=Font.LORE)
    print_typed("Heliostadt III, once a pinnacle of human engineering in deep space.", style=Font.LORE)

    print(f"{Fore.RED}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # First location - Mitsurai D
    print_typed(f"\n{Font.SUBTITLE('MITSURAI D')}", style=Font.HEADER)
    print_typed("\nOnce a thriving research outpost specializing in xenobotany, Mitsurai D", style=Font.INFO)
    print_typed("is now a planet of overgrown vegetation and strange bio-luminescence.", style=Font.INFO)
    print_typed("Your scanners detect unusual movement patterns and erratic energy signatures.", style=Font.INFO)
    
    print_typed("\nThe ship's AI analyzes the planet's atmosphere:", style=Font.SYSTEM)
    print_typed("\"WARNING: Detected traces of a synthetic compound designate RG-435,", style=Font.SYSTEM)
    print_typed("commonly known as 'Rage'. This compound affects neurological function,", style=Font.SYSTEM)
    print_typed("overriding higher cognitive processes and amplifying aggression.\"", style=Font.SYSTEM)
    
    # Second location - Heliostadt III
    print_typed(f"\n{Font.SUBTITLE('HELIOSTADT III')}", style=Font.HEADER)
    print_typed("\nOnce humanity's crowning achievement in space habitation, Heliostadt III", style=Font.INFO)
    print_typed("was a self-sustaining space station housing over 20,000 residents.", style=Font.INFO)
    print_typed("Now it hangs silent in orbit, emergency systems still operational but", style=Font.INFO)
    print_typed("life signs are chaotic and concentrated in unusual patterns.", style=Font.INFO)
    
    print_typed("\nSecured communication logs recovered from satellite uplinks:", style=Font.SYSTEM)
    print_typed("\"...the infection spread too fast! Medical can't contain it... subjects", style=Font.SYSTEM)
    print_typed("displaying extreme aggression, diminished reasoning... attacking anything", style=Font.SYSTEM)
    print_typed("that moves. It's not just behavioral, their physiology is changing...\"", style=Font.SYSTEM)
    
    print(f"{Fore.RED}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create narrative hook
    print_typed("\nBoth locations are connected by more than proximity. The RG-435 pathogen", style=Font.WARNING)
    print_typed("appears to have originated in Mitsurai D's research facilities before", style=Font.WARNING)
    print_typed("somehow reaching Heliostadt III, where its effects were catastrophic.", style=Font.WARNING)
    
    print_typed("\nYour mission parameters update automatically:", style=Font.IMPORTANT)
    print_typed("1. Investigate the research facilities on Mitsurai D", style=Font.IMPORTANT)
    print_typed("2. Determine if any survivors remain on Heliostadt III", style=Font.IMPORTANT)
    print_typed("3. Secure samples of RG-435 for analysis and potential cure", style=Font.IMPORTANT)
    print_typed("4. Contain the viral threat before it can spread further", style=Font.IMPORTANT)
    
    print_typed("\nIn Chapter 8: Viral Directive, you'll:", style=Font.SUBTITLE)
    print_typed("• Navigate a lush but deadly jungle planet overrun by infected wildlife", style=Font.INFO)
    print_typed("• Explore the darkened corridors of an abandoned space station", style=Font.INFO)
    print_typed("• Face enemies driven by pure rage with unpredictable attack patterns", style=Font.INFO)
    print_typed("• Uncover the connection between the virus and The Convergence AI", style=Font.INFO)
    print_typed("• Develop countermeasures to combat or cure the infected", style=Font.INFO)
    
    # Tease gameplay mechanics and tough choices
    print_typed("\nThe infected present a unique threat - they're victims, not willing", style=Font.PLAYER)
    print_typed("combatants. Your approach to them will reveal much about your character.", style=Font.PLAYER)
    
    print_typed("\nWill you neutralize the infected to ensure containment, or risk", style=Font.GLITCH)
    print_typed("everything to find a cure? The viral directive awaits your decision...", style=Font.GLITCH)
    
    time.sleep(1)
    input("\nPress Enter to return to the main menu...")
    return

def player_turn(player, enemy):
    """Handle player's turn with sci-fi themed actions and gender-specific feedback"""
    # Apply companion bonuses
    attack_bonus, defense_bonus = get_companion_bonuses()
    effective_attack = player.attack + attack_bonus
    # Defense bonus is already shown in the UI display below, no need for separate variable
    
    # Get protagonist gender for context-specific messages
    protagonist_gender = "female"  # Default
    
    # Try to get actual protagonist information from game state
    if 'game_state' in globals() and globals()['game_state'] is not None:
        if 'protagonist' in globals()['game_state']:
            protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # Check for human allies support in current zone
    current_zone = game_state.get("current_zone", "")
    zone_data = zones.get(current_zone, {})
    if zone_data.get("human_allies", False) and random.random() < 0.4:  # 40% chance of ally support
        ally_type = random.choice(["tactical", "technical", "medical", "offensive"])
        
        # Display human ally arrival with fancy UI
        print(Font.SEPARATOR)
        print(Font.SUCCESS("HUMAN RESISTANCE ALLY ASSISTANCE DETECTED"))
        
        if ally_type == "tactical":
            # Tactical support provides combat advantage and enemy intel
            print(Font.INFO("A resistance tactical operative provides enemy intelligence."))
            print(f"{Font.BOX_SIDE} {Font.ENEMY(enemy.name)} vulnerability identified: {random.choice(['thermal', 'quantum', 'physical'])} damage.")
            attack_bonus += 10
            effective_attack += 10
            print(Font.SUCCESS(f"Attack bonus increased by +10 (Total: {attack_bonus})"))
            
        elif ally_type == "technical":
            # Technical support enhances defense and repairs equipment
            print(Font.INFO("A resistance engineer provides technical assistance."))
            defense_bonus += 12
            player.defense += 12
            print(Font.SUCCESS(f"Defense increased by +12 (Total: {player.defense})"))
            if player.health < player.max_health:
                health_repair = min(15, player.max_health - player.health)
                player.health += health_repair
                print(Font.SUCCESS(f"Emergency repairs restore {health_repair} health points."))
                
        elif ally_type == "medical":
            # Medical support provides healing and status effect cures
            print(Font.INFO("A resistance medic provides emergency treatment."))
            heal_amount = random.randint(25, 40)
            player.health = min(player.max_health, player.health + heal_amount)
            print(Font.SUCCESS(f"Emergency treatment restored {heal_amount} health points."))
            
            # Clear negative status effects
            cleared_effects = []
            for effect in list(player.status_effects.keys()):
                if effect in ["burning", "bleeding", "poisoned", "neural_shock"]:
                    cleared_effects.append(effect)
                    del player.status_effects[effect]
            
            if cleared_effects:
                print(Font.SUCCESS(f"Medical intervention cleared status effects: {', '.join(cleared_effects)}"))
                
        elif ally_type == "offensive":
            # Offensive support provides direct damage to the enemy
            print(Font.INFO("A resistance fighter provides covering fire."))
            damage = random.randint(30, 50)
            enemy.take_damage(damage, "energy")
            print(Font.SUCCESS(f"Allied covering fire deals {damage} damage to {enemy.name}!"))
            
            # Chance to apply status effect
            if random.random() < 0.5:
                effect = random.choice(["stunned", "burning", "quantum_unstable"])
                duration = random.randint(2, 3)
                enemy.status_effects[effect] = duration
                print(Font.SUCCESS(f"Enemy afflicted with {effect} for {duration} turns!"))
    
    # Display combat stats with enhanced formatting
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.HEADER('NEURAL COMBAT INTERFACE')}                          {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} Attack: {Font.PLAYER(str(player.attack))} {Font.SUCCESS('(+' + str(attack_bonus) + ')')} | Defense: {Font.SHIELD(str(player.defense))} {Font.SUCCESS('(+' + str(defense_bonus) + ')')} {Font.BOX_SIDE}")
    
    # Display elemental resistances if player has any non-zero values
    has_resistances = any(v != 0.0 for v in player.resistances.values())
    if has_resistances:
        resistance_display = []
        for dmg_type, value in player.resistances.items():
            if value > 0:
                resistance_display.append(f"{dmg_type.title()}: {Font.SUCCESS(str(int(value*100))+'%')}")
            elif value < 0:
                resistance_display.append(f"{dmg_type.title()}: {Font.WARNING(str(int(abs(value)*100))+'%')}")
        
        if resistance_display:
            print(f"{Font.BOX_SIDE} Resistances: {' | '.join(resistance_display[:3])} {Font.BOX_SIDE}")
            if len(resistance_display) > 3:
                print(f"{Font.BOX_SIDE}             {' | '.join(resistance_display[3:])} {Font.BOX_SIDE}")
    
    print(Font.BOX_BOTTOM)

    # Check for status effects
    if "stunned" in player.status_effects:
        player.status_effects["stunned"] -= 1
        if player.status_effects["stunned"] <= 0:
            del player.status_effects["stunned"]
            print_typed(f"{Font.SUCCESS('Your neural systems have recovered from the stun effect.')}")
        else:
            print_glitch(f"{Font.WARNING('You are stunned and cannot take action this turn!')} ({player.status_effects['stunned']} turns left)")
            return True

    # Display health bars with visual indicators
    player_health_percent = player.health / player.max_health
    enemy_health_percent = enemy.health / enemy.max_health
    
    player_health_bar = "█" * int(player_health_percent * 20)
    player_health_bar += "░" * (20 - len(player_health_bar))
    
    enemy_health_bar = "█" * int(enemy_health_percent * 20)
    enemy_health_bar += "░" * (20 - len(enemy_health_bar))
    
    print(Font.SEPARATOR_THIN)
    print_typed(f"{Font.PLAYER('YOU:')} {Font.HEALTH(player_health_bar)} {player.health}/{player.max_health}")
    print_typed(f"{Font.ENEMY(enemy.name + ':')} {Font.ENEMY(enemy_health_bar)} {enemy.health}/{enemy.max_health}")
    print(Font.SEPARATOR_THIN)
    
    # Status effect indicators
    active_effects = []
    for effect, turns in player.status_effects.items():
        if effect != "stunned":  # Already handled separately
            active_effects.append(f"{effect.replace('_', ' ').title()} ({turns})")
    
    if active_effects:
        print_typed(f"{Font.WARNING('Your status:')} {', '.join(active_effects)}")
        print(Font.SEPARATOR_THIN)

    # Enhanced combat options menu
    print_typed(f"\n{Font.MENU('[NEURAL INTERFACE]: Combat options:')}")
    
    # Group options by category for better organization
    print_typed(f"\n{Font.HEADER('OFFENSIVE SYSTEMS:')}")
    print_typed(f"{Font.COMMAND('1.')} {Font.INFO('Attack')} - Weapon selection menu (dmg: {effective_attack-3}-{effective_attack+3})")
    emp_count = player.inventory.get("emp_grenade", 0)
    print_typed(f"{Font.COMMAND('2.')} {Font.INFO('EMP Grenade')} - {Font.ITEM(f'[{emp_count}]')} Overload electronic systems (20-35 EMP dmg + stun)")
    
    print_typed(f"\n{Font.HEADER('DEFENSIVE SYSTEMS:')}")
    med_count = player.inventory.get("med_kit", 0)
    print_typed(f"{Font.COMMAND('3.')} {Font.INFO('Med-Kit')} - {Font.ITEM(f'[{med_count}]')} Deploy nanobots to repair damage (15-25 HP)")
    
    # Show shield matrix option if available
    if "shield_matrix" in player.inventory and player.inventory["shield_matrix"] > 0:
        shield_count = player.inventory.get("shield_matrix", 0)
        print_typed(f"{Font.COMMAND('4.')} {Font.INFO('Shield Matrix')} - {Font.ITEM(f'[{shield_count}]')} Deploy energy shield (+15 shield)")
    
    print_typed(f"\n{Font.HEADER('TACTICAL SYSTEMS:')}")
    
    # Special abilities based on implants and level
    if "Hack" in player.abilities and "neural_chip" in player.implants:
        print_typed(f"{Font.COMMAND('5.')} {Font.INFO('Hack')} - Attempt to disable enemy systems (60% success)")
    
    # Advanced equipment options
    adv_med_count = player.inventory.get("advanced_med_kit", 0)
    if adv_med_count > 0:
        print_typed(f"{Font.COMMAND('6.')} {Font.INFO('Advanced Med-Kit')} - {Font.ITEM(f'[{adv_med_count}]')} Enhanced healing + regeneration (30-45 HP + regen)")
    
    neural_stim_count = player.inventory.get("neural_stimulator", 0)
    if neural_stim_count > 0:
        print_typed(f"{Font.COMMAND('7.')} {Font.INFO('Neural Stimulator')} - {Font.ITEM(f'[{neural_stim_count}]')} Boost critical hit chance by 15%")
        
    # Temporal manipulation for players with time fragments (Chapter 6 content)
    time_fragments = game_state.get("time_fragments", 0)
    if time_fragments > 0:
        print_typed(f"\n{Font.HEADER('TEMPORAL SYSTEMS:')}")
        print_typed(f"{Font.COMMAND('T.')} {Font.GLITCH('Time Manipulation')} - {Font.ITEM(f'[{time_fragments} fragments]')} Alter the flow of time")
    
    quantum_stab_count = player.inventory.get("quantum_stabilizer", 0)
    if quantum_stab_count > 0:
        print_typed(f"{Font.COMMAND('8.')} {Font.INFO('Quantum Stabilizer')} - {Font.ITEM(f'[{quantum_stab_count}]')} Immunity to quantum effects")
    
    phase_disrupt_count = player.inventory.get("phase_disruptor", 0)
    if phase_disrupt_count > 0:
        print_typed(f"{Font.COMMAND('9.')} {Font.INFO('Phase Disruptor')} - {Font.ITEM(f'[{phase_disrupt_count}]')} 50% chance to avoid damage")
    
    # Companion options
    if game_state["companions"]:
        print_typed(f"{Font.COMMAND('C.')} {Font.INFO('Companions')} - Deploy companion abilities")
    
    # Character options - Check if player has collected any characters
    if game_state.get("character_collection"):
        print_typed(f"{Font.COMMAND('Q.')} {Font.INFO('Quantum Link')} - Call ally from parallel reality")
    
    # Always show analyze and flee options
    print_typed(f"{Font.COMMAND('A.')} {Font.INFO('Analyze')} - Scan enemy for weaknesses")
    print_typed(f"{Font.COMMAND('F.')} {Font.INFO('Flee')} - Attempt tactical retreat (no progress loss)")
    
    # Help command hint
    print_typed(f"\n{Font.SYSTEM('(Type /help for command descriptions)')}")

    # Add quantum link to the help text
    if game_state.get("character_collection"):
        print_typed(f"{Font.SYSTEM('(Type /quantum for character ally abilities)')}")
        
    # Add time manipulation text if player has time fragments
    if game_state.get("time_fragments", 0) > 0:
        print_typed(f"{Font.GLITCH('(Type /time to use temporal manipulation abilities)')}")

    command = input(f"\n{Font.COMMAND('Input command:')} ").strip().lower()

    # Process command
    if command == "/help":
        # Show help text for commands
        print(Font.box("""
Commands:
/attack or 1 - Attack enemy with your weapons
/emp or 2 - Use EMP grenade on electronic enemies
/medkit or 3 - Use medical kit to heal yourself
/shield or 4 - Deploy shield matrix for protection
/hack or 5 - Hack into enemy systems (requires Neural Chip)
/advmed or 6 - Use advanced med-kit for enhanced healing
/neural or 7 - Use neural stimulator for combat reflexes
/quantum or 8 - Use quantum stabilizer for protection
/phase or 9 - Use phase disruptor for partial phasing
/companions or c - Access companion abilities
/quantum or q - Call ally from parallel reality
/analyze or a - Analyze enemy for weaknesses
/flee or f - Attempt to escape from battle
        """, width=60, color=Fore.CYAN))
        return player_turn(player, enemy)  # Recursive call to try again
        
    elif command == "1" or command == "/attack":
        # Enhanced attack system with multiple weapon options
        print_typed(f"\n{Font.MENU('Select attack type:')}")
        print_typed(f"{Font.COMMAND('1.')} {Font.INFO('Pulse Rifle')} - Energy damage (standard)")
        print_typed(f"{Font.COMMAND('2.')} {Font.INFO('Kinetic Blaster')} - Physical damage (higher crit chance)")
        print_typed(f"{Font.COMMAND('3.')} {Font.INFO('EMP Pistol')} - EMP damage (good vs. electronics)")
        print_typed(f"{Font.COMMAND('4.')} {Font.INFO('Plasma Cutter')} - Thermal damage (chance to burn)")
        print_typed(f"{Font.COMMAND('5.')} {Font.INFO('Quantum Disruptor')} - Quantum damage (bypasses partial defense)")
        
        # Add Cicrais IV content weapons if the player has the appropriate stage
        if game_state.get("stage", 1) >= 2:
            print_typed(f"{Font.COMMAND('6.')} {Font.INFO('Phase Rifle')} - Phase damage (chance for temporal effects)")
            
        if game_state.get("stage", 1) >= 3:
            print_typed(f"{Font.COMMAND('7.')} {Font.INFO('Biomolecular Destabilizer')} - Bio damage (continuous damage over time)")
        
        attack_type = input(f"\n{Font.COMMAND('Select weapon:')} ").strip()
        
        # Set damage type and modifiers based on selection
        damage_types = {
            "1": {"type": "energy", "name": "Pulse Rifle", "mod": 1.0, "crit_mod": 0.0},
            "2": {"type": "physical", "name": "Kinetic Blaster", "mod": 0.9, "crit_mod": 0.1},
            "3": {"type": "emp", "name": "EMP Pistol", "mod": 0.8, "crit_mod": 0.0},
            "4": {"type": "thermal", "name": "Plasma Cutter", "mod": 0.95, "crit_mod": 0.03},
            "5": {"type": "quantum", "name": "Quantum Disruptor", "mod": 0.7, "crit_mod": 0.05},
            "6": {"type": "phase", "name": "Phase Rifle", "mod": 0.80, "crit_mod": 0.08},
            "7": {"type": "bio", "name": "Biomolecular Destabilizer", "mod": 0.75, "crit_mod": 0.05}
        }
        
        # Default to pulse rifle if invalid selection
        weapon = damage_types.get(attack_type, damage_types["1"])
        damage_type = weapon["type"]
        weapon_name = weapon["name"]
        damage_mod = weapon["mod"]
        crit_chance_bonus = weapon["crit_mod"]
        
        # Get player level for damage calculations
        player_level = player.level if hasattr(player, 'level') else 1
        if 'game_state' in globals() and globals()['game_state'] is not None:
            player_level = globals()['game_state'].get('player_level', player_level)
        
        # Level-based damage scaling
        level_damage_bonus = (player_level - 1) * 0.8  # +0.8 damage scaling per level
        
        # Calculate base damage with level bonus
        base_damage = random.randint(effective_attack - 3, effective_attack + 3)
        damage = int(base_damage * damage_mod * (1 + level_damage_bonus / 10))
        
        # Get critical hit chance and damage from combat state or use defaults
        if hasattr(player, 'combat_state') and player.combat_state is not None:
            crit_chance = player.combat_state.get("critical_chance", 5) / 100  # Convert percentage to decimal
            crit_damage_mult = player.combat_state.get("critical_damage", 1.5)
        else:
            # Default values if combat state is missing
            crit_chance = 5 + (player_level * 1.5)  # Base 5% + 1.5% per level
            crit_chance = min(25, crit_chance) / 100  # Cap at 25% and convert to decimal
            crit_damage_mult = 1.5 + (player_level * 0.1)  # Starts at 1.5x, +0.1 per level
        
        # Add weapon-specific critical bonus
        total_crit_chance = crit_chance + crit_chance_bonus
        
        # Neural stimulator effect if active
        if player.inventory.get("neural_stimulator", 0) > 0 and player.inventory.get("neural_stimulator_active", False):
            total_crit_chance += 0.15  # +15% critical chance
            player.inventory["neural_stimulator"] -= 1  # Consume one use
            player.inventory["neural_stimulator_active"] = False
            print_typed(f"{Font.INFO('Neural Stimulator enhances neural targeting!')}")
        
        # Check for critical hit with enhanced feedback
        is_critical = random.random() < total_crit_chance
        if is_critical:
            # Calculate critical damage with level scaling
            damage = int(damage * crit_damage_mult)
            
            # Define gender-specific critical hit messages
            if protagonist_gender == "female":
                # Female protagonist critical hit messages
                if player_level >= 5:
                    crit_messages = [
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your intuitive targeting finds a vital weakness!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} You expertly target a critical system junction!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your precision with the {weapon_name} maximizes damage!"
                    ]
                else:
                    crit_messages = [
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your {weapon_name} finds a weakness!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your attack precision increases the damage!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} You exploit a vulnerability in the enemy!"
                    ]
            else:
                # Male protagonist critical hit messages
                if player_level >= 5:
                    crit_messages = [
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your tactical analysis reveals a critical weakness!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your calculated strike hits a vital component!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your methodical approach with the {weapon_name} maximizes damage!"
                    ]
                else:
                    crit_messages = [
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your {weapon_name} strikes a weak point!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} Your combat training improves your attack!",
                        f"{Font.SUCCESS('CRITICAL HIT!')} You target a vulnerability in the enemy!"
                    ]
            
            # Display random critical hit message
            print_slow(random.choice(crit_messages), delay=0.03)
            
            # Level 5+ gets bonus effects on crits
            if player_level >= 5:
                status_effect = None
                status_duration = 2
                
                # Different status effects based on weapon type
                if damage_type == "energy":
                    status_effect = "energy_leak"
                elif damage_type == "thermal":
                    status_effect = "burning"
                    status_duration = 3
                elif damage_type == "phase":
                    status_effect = "time_displaced"
                elif damage_type == "bio":
                    status_effect = "cellular_breakdown"
                    status_duration = 3
                
                # Apply status effect if one was selected with gender-specific messages
                if status_effect and not enemy.status_effects.get(status_effect):
                    enemy.status_effects[status_effect] = status_duration
                    
                    # Gender-specific status effect messages
                    if protagonist_gender == "female":
                        status_messages = {
                            "energy_leak": "Your precision creates an unstable energy cascade in the target!",
                            "burning": "Your thermal targeting ignites vulnerable components!",
                            "time_displaced": "Your perception of temporal waves disrupts the target's timeline!",
                            "cellular_breakdown": "Your understanding of biomolecular structures triggers degradation!"
                        }
                    else:
                        status_messages = {
                            "energy_leak": "Your tactical strike creates a critical energy system failure!",
                            "burning": "Your calculated attack ignites vulnerable materials!",
                            "time_displaced": "Your manipulation of phase particles disrupts the target's timeline!",
                            "cellular_breakdown": "Your weapons analysis identifies and targets cellular weak points!"
                        }
                    
                    # Get appropriate message or use generic fallback
                    message = status_messages.get(status_effect, f"Status effect applied: {status_effect.replace('_', ' ').title()}")
                    print_typed(f"{Font.SUCCESS(message)}")
        
        # Different attack messages based on weapon type and protagonist gender
        if protagonist_gender == "female":
            # Female protagonist attack messages - more intuitive/perception-focused
            attack_messages = {
                "energy": [
                    "Your intuition guides targeting systems... Firing {weapon_name}...",
                    "You sense optimal energy flow... Discharging {weapon_name}...",
                    "You visualize the photon matrix... Releasing energy burst..."
                ],
                "physical": [
                    "You feel the perfect balance point... Firing {weapon_name}...",
                    "You perceive impact trajectories... Launching projectiles...",
                    "Your reflexes harmonize with recoil... Unleashing kinetic rounds..."
                ],
                "emp": [
                    "You sense electronic vulnerabilities... Deploying electromagnetic pulse...",
                    "Your awareness maps circuit pathways... Triggering EMP burst...",
                    "You anticipate system cascade points... Firing electromagnetic wave..."
                ],
                "thermal": [
                    "You feel heat patterns forming... Firing {weapon_name}...",
                    "Your senses track thermal gradients... Releasing superheated particles...",
                    "You perceive heat transfer points... Launching thermal projectile..."
                ],
                "quantum": [
                    "Your mind grasps quantum possibilities... Firing {weapon_name}...",
                    "You intuitively sense reality folds... Releasing quantum wave...",
                    "Your perception bridges probabilities... Launching quantum projectile..."
                ],
                "phase": [
                    "You feel temporal rhythms aligning... Firing {weapon_name}...",
                    "Your awareness spans dimensions... Releasing phase burst...",
                    "You sense time-stream convergence points... Launching phase projectile..."
                ],
                "bio": [
                    "You perceive cellular structures... Firing {weapon_name}...",
                    "Your instincts map biological weaknesses... Releasing bio-agent...",
                    "You sense genetic vulnerabilities... Launching molecular destabilizer..."
                ]
            }
        else:
            # Male protagonist attack messages - more analytical/methodical
            attack_messages = {
                "energy": [
                    "You analyze targeting vectors... Firing {weapon_name}...",
                    "You calculate optimal capacitor discharge... Releasing {weapon_name}...",
                    "You calibrate photon matrix alignment... Launching energy burst..."
                ],
                "physical": [
                    "You engage kinetic accelerators... Firing {weapon_name}...",
                    "You compute impact trajectories... Launching projectiles...",
                    "You activate recoil compensation systems... Unleashing kinetic rounds..."
                ],
                "emp": [
                    "You precisely map circuit vulnerabilities... Deploying electromagnetic pulse...",
                    "You systematically overload target systems... Triggering EMP burst...",
                    "You calculate electromagnetic propagation... Firing EM wave..."
                ],
                "thermal": [
                    "You maximize thermal coil efficiency... Firing {weapon_name}...",
                    "You calculate optimal plasma containment... Releasing superheated particles...",
                    "You regulate heat sink distribution... Launching thermal projectile..."
                ],
                "quantum": [
                    "You solve quantum fluctuation equations... Firing {weapon_name}...",
                    "You calculate reality matrix distortion... Releasing quantum wave...",
                    "You determine probability field variables... Launching quantum projectile..."
                ],
                "phase": [
                    "You synchronize phase variance patterns... Firing {weapon_name}...",
                    "You calculate dimensional shift parameters... Releasing phase burst...",
                    "You target temporal intersection points... Launching phase projectile..."
                ],
                "bio": [
                    "You identify molecular binding points... Firing {weapon_name}...",
                    "You target cellular degradation pathways... Releasing bio-agent...",
                    "You calibrate DNA recombination variables... Launching molecular destabilizer..."
                ]
            }
        
        # Display attack message - with weapon name formatting
        selected_message = random.choice(attack_messages.get(damage_type, attack_messages["energy"]))
        print_typed(selected_message.format(weapon_name=weapon_name))
        
        # Apply damage with specific damage type
        enemy.take_damage(damage, damage_type)
        
        # Special effects based on damage type with gender-specific responses
        if damage_type == "thermal" and random.random() < 0.25:  # 25% chance
            if "burning" not in enemy.status_effects:
                enemy.status_effects["burning"] = 2  # Lasts 2 turns
                burning_damage = max(3, int(effective_attack * 0.2))  # 20% of attack as burning damage
                
                if protagonist_gender == "female":
                    print_typed(f"{Font.WARNING(f'{enemy.name} is now BURNING!')} Your thermal precision causes {burning_damage} damage per turn for 2 turns.")
                else:
                    print_typed(f"{Font.WARNING(f'{enemy.name} is now BURNING!')} Your calculated thermal output causes {burning_damage} damage per turn for 2 turns.")
        
        elif damage_type == "quantum" and random.random() < 0.20:  # 20% chance
            if "quantum_unstable" not in enemy.status_effects:
                enemy.status_effects["quantum_unstable"] = 2  # Lasts 2 turns
                
                if protagonist_gender == "female":
                    print_typed(f"{Font.WARNING(f'{enemy.name} is now QUANTUM UNSTABLE!')} Your intuitive manipulation of quantum fields reduces their defense by 30% for 2 turns.")
                else:
                    print_typed(f"{Font.WARNING(f'{enemy.name} is now QUANTUM UNSTABLE!')} Your quantum calculations reduce their defense by 30% for 2 turns.")
                
        elif damage_type == "phase" and random.random() < 0.20:  # 20% chance
            if "temporal_distortion" not in enemy.status_effects:
                enemy.status_effects["temporal_distortion"] = 2  # Lasts 2 turns
                
                if protagonist_gender == "female":
                    print_typed(f"{Font.WARNING(f'{enemy.name} is caught in TEMPORAL DISTORTION!')} Your sensing of temporal rhythms creates a 30% chance for them to skip turns for 2 rounds.")
                else:
                    print_typed(f"{Font.WARNING(f'{enemy.name} is caught in TEMPORAL DISTORTION!')} Your systematic targeting of temporal nodes creates a 30% chance for them to skip turns for 2 rounds.")
                
        elif damage_type == "bio" and random.random() < 0.25:  # 25% chance
            if "bio_corruption" not in enemy.status_effects:
                enemy.status_effects["bio_corruption"] = 3  # Lasts 3 turns
                
                if protagonist_gender == "female":
                    print_typed(f"{Font.WARNING(f'{enemy.name} is infected with BIO CORRUPTION!')} Your awareness of cellular vulnerabilities causes damage and weakens their attack for 3 turns.")
                else:
                    print_typed(f"{Font.WARNING(f'{enemy.name} is infected with BIO CORRUPTION!')} Your analysis of biological weakpoints causes damage and weakens their attack for 3 turns.")

    elif command == "2" or command == "/heal" or command == "/med" or command == "/medkit":
        healed = player.use_med_kit()
        if healed:
            if protagonist_gender == "female":
                heal_messages = [
                    f"You intuitively direct nanobots to damaged areas... +{healed} HP restored.",
                    f"Your awareness of your body's needs guides cellular repair... +{healed} HP restored.",
                    f"You sense and mend your internal damage patterns... +{healed} HP restored."
                ]
            else:
                heal_messages = [
                    f"You calculate optimal nanobot deployment paths... +{healed} HP restored.",
                    f"You systematically repair damaged cellular structures... +{healed} HP restored.",
                    f"You execute precise tissue regeneration protocols... +{healed} HP restored."
                ]
            print_typed(random.choice(heal_messages))
        else:
            print_typed("ERROR: No med-kits available in inventory.")
            return False

    elif command == "3" or command == "/emp" or command == "/grenade":
        damage = player.use_emp_grenade()
        if damage:
            # Gender-specific EMP activation messages
            if protagonist_gender == "female":
                print_slow("You sense the electronic pulse patterns... EMP grenade activated!")
            else:
                print_slow("You engage electromagnetic emitters... EMP grenade activated!")
                
            taken = enemy.take_damage(damage, damage_type="emp")
            
            # Gender-specific damage feedback
            if protagonist_gender == "female":
                damage_messages = [
                    f"Your intuition guided the pulse to critical systems! {enemy.name}'s circuits overloaded for {taken} damage!",
                    f"You visualized the cascade points perfectly! {enemy.name}'s systems disrupted for {taken} damage!",
                    f"Your perception targeted vulnerable electronics! {enemy.name} takes {taken} EMP damage!"
                ]
            else:
                damage_messages = [
                    f"Your tactical deployment maximized impact! {enemy.name}'s circuits overloaded for {taken} damage!",
                    f"Your calculated frequency matched their vulnerabilities! {enemy.name}'s systems disrupted for {taken} damage!",
                    f"Your precise EMP coordination targeted vital systems! {enemy.name} takes {taken} EMP damage!"
                ]
            
            print_typed(random.choice(damage_messages))
            game_state["player_stats"]["damage_dealt"] += taken
        else:
            print_typed("ERROR: No EMP grenades in inventory.")
            return False

    elif (command == "4" or command == "/shield") and "shield_matrix" in player.inventory and player.inventory["shield_matrix"] > 0:
        shield_points = player.use_shield_matrix()
        if shield_points:
            # Gender-specific shield matrix activation messages
            if protagonist_gender == "female":
                shield_messages = [
                    f"You intuitively align energy harmonics... Shield matrix resonating at +{shield_points} protection.",
                    f"Your perception creates perfect energy balance... +{shield_points} shield points active.",
                    f"You sense and stabilize defensive frequencies... +{shield_points} shield barrier established."
                ]
            else:
                shield_messages = [
                    f"You calibrate shield generators with precision... +{shield_points} defense matrix online.",
                    f"Your calculated energy distribution creates optimal coverage... +{shield_points} shield points activated.",
                    f"You execute defensive protocols systematically... +{shield_points} shield barrier established."
                ]
            print_typed(random.choice(shield_messages))

    elif (command == "5" or command == "/hack") and "Hack" in player.abilities:
        if player.use_ability("Hack", enemy):
            # Gender-specific successful hack messages
            if protagonist_gender == "female":
                hack_messages = [
                    "You intuitively navigate security protocols... Hack successful!",
                    "Your perception identifies system weaknesses... Enemy controls compromised!",
                    "You sense the neural pathways of the machine... Systems bypassed!"
                ]
            else:
                hack_messages = [
                    "You execute precision code injections... Hack successful!",
                    "Your algorithmic analysis breaches security layers... Enemy controls compromised!",
                    "You systematically override system safeguards... Access granted!"
                ]
            print_typed(random.choice(hack_messages))
        else:
            # Gender-specific failed hack messages
            if protagonist_gender == "female":
                print_typed("Your intuition warns of enhanced security measures... Hack attempt failed.")
            else:
                print_typed("Your system analysis detects countermeasures... Hack attempt failed.")
            return False
            
    elif command == "q" or command == "/quantum" or command == "/quantum_link":
        # Initialize combat state if needed
        if "current_combat_state" not in game_state:
            game_state["current_combat_state"] = {"used_allies": []}
        
        # Check if player has collected any characters through gacha
        if game_state.get("character_collection"):
            # Call ally from parallel reality
            ability_used = use_character_ability(player, enemy, game_state["current_combat_state"])
            if ability_used:
                # Character ability was used, count as turn
                return True
            else:
                # Character menu was opened but no ability was used, don't count as turn
                return player_turn(player, enemy)
        else:
            print_typed(f"{Font.WARNING('No ally characters available.')}")
            print_typed(f"{Font.INFO('Use the Quantum Chronosphere to manifest allies from parallel realities.')}")
            return False  # Don't count as a turn

    elif command == "6" or command == "/companions":
        # If player has no companions, provide information
        if not game_state["companions"]:
            print_typed("No active companions detected.")
            print_typed("Build companions using the Engineering Interface (/build).")
            return False

        # Display companion abilities
        print_typed("\n=== COMPANION SYSTEMS ===")
        print_typed("Your companions are providing passive bonuses:")
        print(f"Attack bonus: +{attack_bonus}")
        print(f"Defense bonus: +{defense_bonus}")

        # Show special companion abilities that could be triggered
        # TO DO: Implement active companion abilities in future update
        print_typed("\nActive companion abilities will be available in future updates.")
        return False  # Don't count as a turn for now

    elif command in ("7", "/flee"):
        # Attempt to flee
        success = flee_battle()
        if success:
            return "flee"  # Special return value to indicate successful fleeing
        # If flee fails, enemy gets a turn (handled in main combat loop)

    elif command == "t" or command == "/time" or command == "/temporal":
        # Check if player has time fragments
        if game_state.get("time_fragments", 0) > 0:
            # Initialize combat state if needed
            if not hasattr(player, 'combat_state'):
                player.combat_state = {
                    "last_enemy_damage": 0,
                    "extra_action": False,
                    "enemy_next_attack": None,
                    "time_stopped": False
                }
            
            # Use time manipulation abilities
            time_ability_used = use_time_manipulation(player, enemy, player.combat_state)
            if time_ability_used:
                return True  # Count as a turn if ability was used
            else:
                return player_turn(player, enemy)  # Don't count as turn if canceled
        else:
            print_typed(f"{Font.WARNING('No time fragments available for temporal manipulation.')}")
            print_typed(f"{Font.INFO('Encounter the Chrono-Sentient to collect time fragments.')}")
            return False  # Don't count as a turn
            
    elif command == "/help":
        print("\n=== TACTICAL SYSTEMS HELP ===")
        print("Combat Commands:")
        print("  1 or /attack - Fire your pulse rifle")
        print("  2 or /heal   - Use a med-kit")
        print("  3 or /emp    - Deploy an EMP grenade")
        if "shield_matrix" in player.inventory and player.inventory["shield_matrix"] > 0:
            print("  4 or /shield - Activate shield matrix")
        if "Hack" in player.abilities:
            print("  5 or /hack   - Attempt to hack enemy systems")
        print("  6 or /companions - Deploy companion abilities")
        if game_state.get("time_fragments", 0) > 0:
            print("  t or /time   - Use temporal manipulation abilities")
            
        if game_state.get("has_ignite_module", False):
            print("  i or /ignite - Activate Yitrian Ignite Module")
        print("  7 or /flee   - Attempt to escape combat")

        print("\nInformation Commands:")
        print("  /scan   - Scan current zone")
        print("  /status - Display your status and inventory")
        print("  /log    - Access mission log")
        print("  /items  - Inspect items in inventory")
        print("  /stats  - View game statistics")

        print("\nEngineering Commands (outside combat):")
        print("  /build  - Fabricate companion drones/robots")
        print("  /manage - Manage active companions")
        return False  # Don't count help as a turn

    elif command == "/status":
        print_typed("\n=== NEURAL INTERFACE: STATUS ===")
        print(f"IDENTITY: {player.name} | NEURAL LEVEL: {player.level}")
        print(f"VITALS: {player.health}/{player.max_health} | XP BUFFER: {player.experience}/{player.level * 100}")

        # Show effective stats with companion bonuses
        print(f"COMBAT STATS: Attack {player.attack} (+{attack_bonus}) | Defense {player.defense} (+{defense_bonus})")
        if player.shield > 0:
            print(f"ACTIVE SHIELD: {player.shield} points")

        print(f"\nLOCATION: {game_state['current_zone']}")
        print(f"CURRENT STAGE: {game_state['current_stage']}/50")

        print("\nINVENTORY MANIFEST:")
        for item_id, count in player.inventory.items():
            if count > 0 and item_id in items:
                item_data = items[item_id]
                print(f"  - {item_data['name']} ({count}): {item_data['effect']}")

        if player.implants:
            print("\nINSTALLED IMPLANTS:")
            for implant_id in player.implants:
                if implant_id in items:
                    implant_data = items[implant_id]
                    print(f"  - {implant_data['name']}: {implant_data['effect']}")

        if game_state["companions"]:
            print("\nACTIVE COMPANIONS:")
            for comp_id in game_state["companions"]:
                if comp_id in companions:
                    comp_data = companions[comp_id]
                    print(f"  - {comp_data['name']}: +{comp_data['attack_bonus']} ATK, +{comp_data['defense_bonus']} DEF")

        return False  # Don't count status check as a turn

    elif command in ("/scan", "/zone"):
        zone = zones[game_state["current_zone"]]
        print_typed(f"\n=== SCANNING: {game_state['current_zone']} ===")
        print_slow(zone["description"])

        print_typed("\nSCANNING FOR THREATS:")
        for enemy_name in zone["enemies"]:
            if enemy_name in enemies:
                enemy_data = enemies[enemy_name]
                print(f"- {enemy_name}: {enemy_data['description']}")

        print_typed("\nRESOURCE DETECTION:")
        for item_id in zone["items"]:
            if item_id in items:
                print(f"- {items[item_id]['name']}: {items[item_id]['description']}")

        return False  # Don't count zone info as a turn

    elif command in ("/log", "/quest"):
        current_quest = zones[game_state["current_zone"]]["quest"]
        progress = game_state["quest_progress"].get(current_quest, 0)
        print_typed(f"\n=== MISSION LOG: {current_quest} ===")

        if current_quest == "System Reboot":
            if progress == 0:
                print_slow("MISSION OBJECTIVE: Restore power to the cryostasis facility exit systems.")
                print_slow("REQUIRED: Collect 5 energy cells and defeat security systems.")
                print_slow("The facility's automated security has identified you as an intruder. You need to")
                print_slow("gather enough energy cells to power the emergency exit, while defending yourself.")
            elif progress == 1:
                print_slow("MISSION STATUS: In progress")
                collected = player.inventory.get("energy_cell", 0)
                print_slow(f"Energy cells collected: {collected}/5")
                print_slow("Continue defeating security systems and gathering resources.")
            elif progress == 2:
                print_slow("MISSION COMPLETE! Exit systems powered.")
                print_slow("You can now proceed to the Orbital Transit Hub.")
        return False  # Don't count quest info as a turn

    elif command == "/items":
        print_typed("\n=== INVENTORY ANALYSIS ===")
        for item_id, count in player.inventory.items():
            if count > 0 and item_id in items:
                item_data = items[item_id]
                print(f"\n{item_data['name']} (x{count}):")
                print(f"Type: {item_data['type'].upper()}")
                print(f"{item_data['description']}")
                print(f"Effect: {item_data['effect']}")
        return False

    elif command == "/stats":
        show_game_stats()
        return False

    elif command == "/build":
        print_typed("Cannot access fabrication systems during combat.")
        print_typed("Defeat the enemy or retreat first.")
        return False

    elif command == "/manage":
        print_typed("Cannot access companion management during combat.")
        print_typed("Defeat the enemy or retreat first.")
        return False
        
    elif command == "a" or command == "/analyze":
        # Get enemy data
        enemy_data = enemies.get(enemy.name, {})
        resistances = enemy_data.get("resistances", {})
        abilities = enemy_data.get("abilities", [])
        
        # Calculate enemy health percentage
        health_percent = enemy.health / enemy.max_health if enemy.max_health > 0 else 0
        
        # Gender-specific analysis messages
        if protagonist_gender == "female":
            print_typed(f"\n{Font.INFO('Your intuitive analysis reveals enemy information:')}")
            print_typed(f"{Font.ENEMY(enemy.name)} - Your perception identifies key aspects of its design and behavior.")
            
            # Display gender-specific resistance descriptions
            if resistances:
                print_typed(f"\n{Font.WARNING('Your instincts detect defensive adaptations:')}")
                for res_type, value in resistances.items():
                    if value > 0:
                        print_typed(f"• You sense {value}% resistance to {res_type.replace('_', ' ')} damage")
                    elif value < 0:
                        print_typed(f"• You perceive a {abs(value)}% vulnerability to {res_type.replace('_', ' ')} damage")
            
            # Display gender-specific ability insights
            if abilities:
                print_typed(f"\n{Font.SYSTEM('Your awareness reveals potential abilities:')}")
                for ability in abilities:
                    print_typed(f"• You intuitively understand its {ability} capability")
            
            # Health assessment with female perspective
            if health_percent > 0.7:
                print_typed(f"\n{Font.HEALTH('You sense its systems are largely intact.')}")
            elif health_percent > 0.3:
                print_typed(f"\n{Font.HEALTH('You perceive moderate damage to its primary systems.')}")
            else:
                print_typed(f"\n{Font.HEALTH('You feel its systems are critically compromised.')}")
        else:
            # Male protagonist analysis messages
            print_typed(f"\n{Font.INFO('Your tactical analysis reveals enemy information:')}")
            print_typed(f"{Font.ENEMY(enemy.name)} - Your systematic evaluation identifies key specifications and protocols.")
            
            # Display gender-specific resistance descriptions
            if resistances:
                print_typed(f"\n{Font.WARNING('Your analysis detects defensive capabilities:')}")
                for res_type, value in resistances.items():
                    if value > 0:
                        print_typed(f"• You calculate {value}% resistance to {res_type.replace('_', ' ')} damage")
                    elif value < 0:
                        print_typed(f"• You identify a {abs(value)}% vulnerability to {res_type.replace('_', ' ')} damage")
            
            # Display gender-specific ability insights
            if abilities:
                print_typed(f"\n{Font.SYSTEM('Your assessment reveals potential abilities:')}")
                for ability in abilities:
                    print_typed(f"• You determine it possesses {ability} functionality")
            
            # Health assessment with male perspective
            if health_percent > 0.7:
                print_typed(f"\n{Font.HEALTH('Your diagnostics show minimal structural damage.')}")
            elif health_percent > 0.3:
                print_typed(f"\n{Font.HEALTH('Your calculations indicate significant system degradation.')}")
            else:
                print_typed(f"\n{Font.HEALTH('Your analysis confirms critical failure imminent.')}")
        
        # Show attack pattern analysis with gender-specific language
        print_typed(f"\n{Font.WARNING('Attack pattern assessment:')}")
        attack_value = enemy.attack
        
        if protagonist_gender == "female":
            if attack_value > player.defense * 1.5:
                print_typed("Your instincts warn you that this enemy's attacks are extremely dangerous.")
            elif attack_value > player.defense:
                print_typed("You sense that the enemy's offensive capability exceeds your defensive strength.")
            else:
                print_typed("You feel confident that your defenses can withstand this enemy's attacks.")
        else:
            if attack_value > player.defense * 1.5:
                print_typed("Your calculations indicate this enemy's attack power far exceeds your defensive capabilities.")
            elif attack_value > player.defense:
                print_typed("Your analysis shows the enemy's offensive output is greater than your defensive parameters.")
            else:
                print_typed("Your assessment confirms your defensive specifications can withstand this enemy's attack vectors.")
        
        # Strategic advice based on gender
        print_typed(f"\n{Font.IMPORTANT('Strategic assessment:')}")
        if protagonist_gender == "female":
            print_typed("Your intuition suggests adapting your approach based on these insights.")
        else:
            print_typed("Your tactical analysis recommends a strategic response based on these specifications.")
        
        return False  # Don't count analysis as a turn

    else:
        print_typed("ERROR: Invalid command. Type '/help' for available commands.")
        return False  # Don't count invalid commands as a turn

    return True  # A valid action was taken


def enemy_turn(enemy, player, combat_state=None):
    """Handle enemy's turn with advanced AI behaviors
    
    Args:
        enemy: The enemy character
        player: The player character
        combat_state: Optional dictionary to track combat state for time mechanics
    """
    
    # Process all status effects with our new consolidated function
    effect_messages = enemy.process_status_effects()
    if effect_messages:
        for message in effect_messages:
            print_typed(message)
    
    # Check status effects that prevent action
    if "stunned" in enemy.status_effects:
        print_glitch(f"{enemy.name} is stunned and cannot take action! ({enemy.status_effects['stunned']} turns left)")
        return

    if "disabled" in enemy.status_effects:
        print_glitch(f"{enemy.name} is disabled from your hack! ({enemy.status_effects['disabled']} turns left)")
        return
        
    # Check for quantum instability effect (30% defense reduction)
    # We track the status effect but the actual defense reduction is applied in combat calculations

    # Load enemy data to access abilities
    enemy_data = enemies.get(enemy.name, {})
    abilities = enemy_data.get("abilities", [])

    # Phase shift makes enemies harder to hit but also affects their targeting
    if "phase_shift" in enemy.status_effects:
        print_typed(f"{Font.INFO(f'{enemy.name} is partially phased out of normal space, making targeting difficult.')}")
    
    print_typed(f"\n{enemy.name} targeting...")
    time.sleep(0.5)

    # Calculate enemy tactics based on health percentage
    health_percent = enemy.health / enemy.max_health

    # Enhanced enemy AI with tactical decision making based on enemy type
    # More advanced enemies have better decision making
    is_advanced = any(keyword in enemy.name.lower() for keyword in ["overseer", "server", "ai", "alpha", "commander"])
    
    # Create behavior profile based on enemy type
    behavior_profile = {
        # Default balanced profile
        "attack_weight": 0.6,
        "heal_weight": 0.1,
        
        # Default attack preferences
        "preferred_attacks": ["physical", "energy"],
        "special_weight": 0.3,
    }
    
    # Special behavior profiles for different enemy types
    if "Simulacra" in enemy.name or "Mimic" in enemy.name:
        # Simulacra are more tactical and use advanced abilities
        behavior_profile.update({
            "attack_weight": 0.5,
            "heal_weight": 0.1,
            "special_weight": 0.4,  # Higher chance to use special abilities
            "preferred_attacks": ["phase", "quantum", "energy"],
            "can_phase_shift": True
        })
        
        # Higher-tier Simulacra are more dangerous
        if "Elite" in enemy.name or "Commander" in enemy.name:
            behavior_profile["special_weight"] = 0.5
            behavior_profile["can_temporal_distort"] = True
            
        # Bosses are extremely tactical
        if "Overlord" in enemy.name or "Prime" in enemy.name or "Titan" in enemy.name:
            behavior_profile["special_weight"] = 0.7
            behavior_profile["has_adaptive_defense"] = True  # Adapts to player's attack patterns
            behavior_profile["can_phase_shift"] = True
            behavior_profile["can_temporal_distort"] = True
        
        # Adjust profile based on health
        if health_percent < 0.4:
            # More defensive when low health
            behavior_profile["heal_weight"] += 0.15
            behavior_profile["attack_weight"] -= 0.15
    
    elif "Biomechanical" in enemy.name or "Harvester" in enemy.name:
        # Biomechanical enemies focus on bio attacks and self-repair
        behavior_profile.update({
            "attack_weight": 0.4,
            "heal_weight": 0.2,  # Can self-repair
            "special_weight": 0.4,
            "preferred_attacks": ["bio", "physical", "energy"],
            "can_self_repair": True
        })
    
    # Adjust behavior based on health
    if health_percent < 0.3 and enemy.inventory.get("med_kit", 0) > 0:
        # Critical health - prioritize recovery
        if is_advanced:
            # Advanced enemies make smarter decisions
            behavior_profile["attack_weight"] = 0.1
            behavior_profile["heal_weight"] = 0.8
            behavior_profile["special_weight"] = 0.1
        else:
            # Basic enemies are less strategic
            behavior_profile["attack_weight"] = 0.3
            behavior_profile["heal_weight"] = 0.6
            behavior_profile["special_weight"] = 0.1
    elif health_percent < 0.5:
        # Damaged but functional - balanced tactics
        if is_advanced:
            behavior_profile["attack_weight"] = 0.4
            behavior_profile["heal_weight"] = 0.3
            behavior_profile["special_weight"] = 0.3
        else:
            behavior_profile["attack_weight"] = 0.5
            behavior_profile["heal_weight"] = 0.3
            behavior_profile["special_weight"] = 0.2
    else:
        # High functionality - focus on offensive
        if is_advanced:
            behavior_profile["attack_weight"] = 0.5
            behavior_profile["heal_weight"] = 0.1
            behavior_profile["special_weight"] = 0.4
        else:
            behavior_profile["attack_weight"] = 0.7
            behavior_profile["heal_weight"] = 0.1
            behavior_profile["special_weight"] = 0.2
            
    # Make tactical decision based on behavior profile
    choice = random.choices(
        ["attack", "heal", "special"], 
        weights=[
            behavior_profile["attack_weight"],
            behavior_profile["heal_weight"],
            behavior_profile["special_weight"]
        ]
    )[0]

    # Execute chosen action
    if choice == "attack":
        # Select a damage type based on enemy preferences
        damage_type = random.choice(behavior_profile["preferred_attacks"])
        
        # Calculate base damage
        base_damage = random.randint(enemy.attack - 3, enemy.attack + 3)
        
        # Apply modifiers based on damage type
        damage_modifiers = {
            "physical": 1.0,
            "energy": 1.1,  # Energy does slightly more damage
            "emp": 0.8,     # EMP does less damage but has status effect chance
            "thermal": 0.9, # Thermal does less but can apply burning
            "quantum": 0.7, # Quantum does less but can destabilize
            "phase": 0.75,  # Phase attacks can cause temporal effects
            "bio": 0.85     # Bio attacks can cause corruption
        }
        
        # Special attack descriptions for Simulacra entities
        attack_descriptions = {
            "physical": f"{enemy.name} strikes with precision!",
            "energy": f"{enemy.name} fires an energy beam!",
            "emp": f"{enemy.name} releases an electromagnetic pulse!",
            "thermal": f"{enemy.name} unleashes a thermal blast!",
            "quantum": f"{enemy.name} destabilizes the quantum field!",
            "phase": f"{enemy.name} launches a phase-shifted attack from multiple realities!",
            "bio": f"{enemy.name} releases corrosive nanites!"
        }
        
        # Custom descriptions for Simulacra
        if "Simulacra" in enemy.name:
            attack_descriptions.update({
                "phase": f"{enemy.name} shifts between realities, attacking from multiple dimensions!",
                "quantum": f"{enemy.name} distorts the quantum field, making your movements unpredictable!",
                "energy": f"{enemy.name} releases a concentrated burst of exotic energy!"
            })
            
        # Custom descriptions for Biomechanical entities
        if "Biomechanical" in enemy.name or "Harvester" in enemy.name:
            attack_descriptions.update({
                "bio": f"{enemy.name} launches a stream of corruptive biomatter!",
                "physical": f"{enemy.name}'s limbs reconfigure into deadly weapons!"
            })
        
        damage = int(base_damage * damage_modifiers.get(damage_type, 1.0))
        
        # Critical hit chance (advanced enemies have higher crit chance)
        crit_chance = 0.1 if is_advanced else 0.05
        is_critical = random.random() < crit_chance
        
        if is_critical:
            damage = int(damage * 1.5)  # 50% crit bonus
            print_typed(f"{Font.WARNING('CRITICAL HIT!')} {enemy.name}'s attack finds a vulnerability!")
        
        # Different attack messages based on enemy type and damage type
        if "Sentinel Drone" in enemy.name or "Drone" in enemy.name:
            if damage_type == "energy":
                print_typed(f"{enemy.name} charges its {Font.ENEMY('laser targeting systems')}...")
            elif damage_type == "physical":
                print_typed(f"{enemy.name} deploys {Font.ENEMY('high-velocity projectiles')}...")
            elif damage_type == "emp":
                print_typed(f"{enemy.name} emits an {Font.ENEMY('electromagnetic pulse')}...")
            elif damage_type == "thermal":
                print_typed(f"{enemy.name} charges its {Font.ENEMY('thermal projectors')}...")
            elif damage_type == "quantum":
                print_typed(f"{enemy.name} activates a {Font.ENEMY('quantum destabilizer')}...")
            else:
                print_typed(f"{enemy.name} attacks with electronic systems...")
        elif "Android" in enemy.name:
            if damage_type == "energy":
                print_typed(f"{enemy.name} fires {Font.ENEMY('energy projectors')}...")
            elif damage_type == "physical":
                print_typed(f"{enemy.name} engages in {Font.ENEMY('close combat protocols')}...")
            elif damage_type == "emp":
                print_typed(f"{enemy.name} activates {Font.ENEMY('circuit overloaders')}...")
            elif damage_type == "thermal":
                print_typed(f"{enemy.name} ignites {Font.ENEMY('plasma emitters')}...")
            elif damage_type == "quantum":
                print_typed(f"{enemy.name} initiates {Font.ENEMY('reality disruption')}...")
            else:
                print_typed(f"{enemy.name} activates combat systems...")
        # Special attack descriptions for Simulacra enemies
        elif "Simulacra" in enemy.name or "Mimic" in enemy.name:
            if damage_type == "energy":
                print_typed(f"{enemy.name} channels {Font.ENEMY('mimicked energy weapons')}...")
            elif damage_type == "physical":
                print_typed(f"{enemy.name} forms {Font.ENEMY('blade-like appendages')}...")
            elif damage_type == "emp":
                print_typed(f"{enemy.name} emits {Font.ENEMY('disruptive frequency')}...")
            elif damage_type == "thermal":
                print_typed(f"{enemy.name} superheats {Font.ENEMY('surface particles')}...")
            elif damage_type == "quantum":
                print_typed(f"{enemy.name} creates {Font.ENEMY('quantum anomalies')}...")
            elif damage_type == "phase":
                print_typed(f"{enemy.name} destabilizes {Font.ENEMY('local spacetime')}...")
            elif damage_type == "bio":
                print_typed(f"{enemy.name} disperses {Font.ENEMY('adaptive nanites')}...")
            else:
                print_typed(f"{enemy.name} shifts form to attack...")
        # Special descriptions for biomechanical enemies
        elif "Biomechanical" in enemy.name or "Harvester" in enemy.name:
            if damage_type == "energy":
                print_typed(f"{enemy.name} discharges {Font.ENEMY('bioenergy pulse')}...")
            elif damage_type == "physical":
                print_typed(f"{enemy.name} extends {Font.ENEMY('chitinous talons')}...")
            elif damage_type == "emp":
                print_typed(f"{enemy.name} generates {Font.ENEMY('synaptic overload')}...")
            elif damage_type == "thermal":
                print_typed(f"{enemy.name} secretes {Font.ENEMY('corrosive enzymes')}...")
            elif damage_type == "quantum":
                print_typed(f"{enemy.name} alters {Font.ENEMY('molecular structure')}...")
            elif damage_type == "bio":
                print_typed(f"{enemy.name} releases {Font.ENEMY('infectious microbes')}...")
            else:
                print_typed(f"{enemy.name} prepares organic weapons...")
        else:
            if damage_type == "energy":
                print_typed(f"{enemy.name} fires {Font.ENEMY('energy weapons')}...")
            elif damage_type == "physical":
                print_typed(f"{enemy.name} launches {Font.ENEMY('physical attack')}...")
            elif damage_type == "emp":
                print_typed(f"{enemy.name} generates {Font.ENEMY('electromagnetic interference')}...")
            elif damage_type == "thermal":
                print_typed(f"{enemy.name} activates {Font.ENEMY('thermal emitters')}...")
            elif damage_type == "quantum":
                print_typed(f"{enemy.name} distorts {Font.ENEMY('quantum fields')}...")
            elif damage_type == "phase":
                print_typed(f"{enemy.name} generates {Font.ENEMY('phase distortions')}...")
            elif damage_type == "bio":
                print_typed(f"{enemy.name} releases {Font.ENEMY('biological agents')}...")
            else:
                print_typed(f"{enemy.name} attacks with electronic systems...")
        
        # Apply damage with specific damage type
        player.take_damage(damage, damage_type)
        
        # Special effect chance based on damage type
        effect_chance = 0.2 if is_advanced else 0.1
        
        # Increase effect chance for Simulacra enemies
        if "Simulacra" in enemy.name or "Mimic" in enemy.name:
            effect_chance += 0.15  # Simulacra have more powerful status effects
            
        # Elite enemies have higher effect chances
        if any(term in enemy.name for term in ["Elite", "Commander", "Overlord", "Prime", "Titan"]):
            effect_chance += 0.1
        
        if damage_type == "thermal" and random.random() < effect_chance:
            if "burning" not in player.status_effects:
                player.status_effects["burning"] = 2
                burn_damage = max(2, int(enemy.attack * 0.15))
                print_typed(f"{Font.WARNING('You are set on fire!')} Will take {burn_damage} damage per turn for 2 turns.")
                
        elif damage_type == "emp" and random.random() < effect_chance:
            if "stunned" not in player.status_effects:
                player.status_effects["stunned"] = 1
                print_typed(f"{Font.WARNING('Your neural interface is temporarily disabled!')} You'll be stunned for 1 turn.")
                
        elif damage_type == "quantum" and random.random() < effect_chance:
            # For Simulacra enemies, quantum attacks can cause more severe effects
            if "Simulacra" in enemy.name and "Elite" in enemy.name and random.random() < 0.4:
                if "quantum_entanglement" not in player.status_effects:
                    player.status_effects["quantum_entanglement"] = 2
                    print_glitch("QUANTUM ENTANGLEMENT DETECTED - CAUSAL DETERMINISM COMPROMISED!")
                    print_typed(f"{Font.WARNING('Your actions are now entangled with the enemy!')} Some attacks may harm you instead for 2 turns.")
            else:
                if "quantum_unstable" not in player.status_effects:
                    player.status_effects["quantum_unstable"] = 2
                    print_typed(f"{Font.WARNING('Your molecular structure is destabilized!')} Defense reduced by 30% for 2 turns.")
                
        elif damage_type == "phase" and random.random() < effect_chance:
            # For Simulacra enemies, phase attacks have more severe effects
            if "Simulacra" in enemy.name and random.random() < 0.5:
                if "phase_lock" not in player.status_effects:
                    player.status_effects["phase_lock"] = 2
                    print_glitch("PHASE LOCK INITIATED - YOUR DIMENSIONAL COORDINATES ARE COMPROMISED!")
                    print_typed(f"{Font.WARNING('You are trapped between realities!')} Movement unpredictable for 2 turns.")
            else:
                if "temporal_distortion" not in player.status_effects:
                    player.status_effects["temporal_distortion"] = 2
                    print_typed(f"{Font.WARNING('Reality shifts around you!')} 30% chance to skip turns for 2 rounds.")
                
        elif damage_type == "bio" and random.random() < effect_chance:
            # For Biomechanical enemies, bio attacks have more severe effects
            if ("Biomechanical" in enemy.name or "Harvester" in enemy.name) and random.random() < 0.4:
                if "bio_infestation" not in player.status_effects:
                    player.status_effects["bio_infestation"] = 3
                    print_glitch("FOREIGN ORGANISM DETECTED - SYSTEMIC CORRUPTION IN PROGRESS!")
                    print_typed(f"{Font.WARNING('Your systems are being hijacked by alien microorganisms!')} Attack and defense reduced by 20% for 3 turns.")
            else:
                if "bio_corruption" not in player.status_effects:
                    player.status_effects["bio_corruption"] = 3
                    print_typed(f"{Font.WARNING('Alien nanites infect your systems!')} Taking damage and losing attack power for 3 turns.")

    elif choice == "heal":
        healed = enemy.use_med_kit()
        if healed:
            # Different healing messages based on enemy type
            if "Drone" in enemy.name:
                print_typed(f"{enemy.name} deploys {Font.SUCCESS('self-repair nanites')}. Systems restored by {healed} points.")
            elif "Android" in enemy.name:
                print_typed(f"{enemy.name} activates {Font.SUCCESS('cellular regeneration matrix')}. Systems restored by {healed} points.")
            elif "Overseer" in enemy.name or "Server" in enemy.name:
                print_typed(f"{enemy.name} initiates {Font.SUCCESS('emergency recovery protocol')}. Systems restored by {healed} points.")
            # Special healing for Simulacra enemies
            elif "Simulacra" in enemy.name or "Mimic" in enemy.name:
                print_typed(f"{enemy.name} {Font.GLITCH('phase-shifts')} into an alternate reality and returns partially {Font.SUCCESS('healed')}.")
                print_typed(f"Damaged components have been {Font.SUCCESS('replaced with versions from another timeline')}. Systems restored by {healed} points.")
                # Chance to gain a phase buff after healing
                if random.random() < 0.3:
                    if "phase_shift" not in enemy.status_effects:
                        enemy.status_effects["phase_shift"] = 2
                        print_typed(f"{enemy.name} maintains a partial {Font.GLITCH('phase-shift state')} after healing.")
            # Special healing for Biomechanical enemies
            elif "Biomechanical" in enemy.name or "Harvester" in enemy.name:
                print_typed(f"{enemy.name} initiates {Font.SUCCESS('rapid cell regeneration')}. Organic components regrow and synthetic parts recalibrate.")
                print_typed(f"Systems restored by {healed} points.")
                # Chance to gain increased strength after healing
                if random.random() < 0.4:
                    enemy.attack += 2
                    print_typed(f"{enemy.name}'s metabolic processes have {Font.WARNING('enhanced')} its combat capabilities.")
            else:
                print_typed(f"{enemy.name} engages {Font.SUCCESS('repair protocols')}. Systems restored by {healed} points.")
        else:
            # If healing failed, attack instead
            print_typed(f"{enemy.name} attempts system repair but lacks resources.")
            damage = random.randint(enemy.attack - 3, enemy.attack + 3)
            
            # Fallback to basic attack (with some randomization of damage type)
            damage_type = random.choice(behavior_profile["preferred_attacks"])
            damage_dealt = player.take_damage(damage, damage_type)
            print_typed(f"{enemy.name} switches to attack protocol. You take damage!")

    elif choice == "special" and abilities:
        # Use a special ability based on enemy type
        ability = random.choice(abilities)
        ability_name = ability if isinstance(ability, str) else ability.get("name", "Unknown Ability")
        
        # Enhanced special abilities system with custom damage types and effects
        special_abilities = {
            "Scan Weakness": {
                "message": f"{enemy.name} {Font.ENEMY('scans for weaknesses')} in your defense algorithms...",
                "effect": lambda: setattr(player, "defense", max(0, player.defense - 3)),
                "result": "Your defense systems are temporarily compromised! -3 Defense for 1 turn."
            },
            "Adaptive Shielding": {
                "message": f"{enemy.name} activates {Font.ENEMY('adaptive energy shielding')}...",
                "effect": lambda: setattr(enemy, "shield", 10 + enemy.level),
                "result": f"{enemy.name} now has a protective energy field of {10 + enemy.level} shield points!"
            },
            "Missile Lock": {
                "message": f"{enemy.name} initiates {Font.ENEMY('tactical missile lock sequence')}...",
                "damage": lambda: random.randint(enemy.attack + 5, enemy.attack + 15),
                "damage_type": "physical",
                "result": "Guided missiles impact your position!"
            },
            "System Shock": {
                "message": f"{enemy.name} initiates a {Font.ENEMY('system disruption sequence')}...",
                "damage": lambda: random.randint(enemy.attack + 2, enemy.attack + 10),
                "damage_type": "emp",
                "result": "Your systems experience a momentary shock!"
            },
            # Special Simulacra Abilities
            "Reality Tear": {
                "message": f"{enemy.name} {Font.GLITCH('tears open a rift in spacetime')}...",
                "damage": lambda: random.randint(enemy.attack + 8, enemy.attack + 20),
                "damage_type": "phase",
                "effect": lambda: player.status_effects.update({"phase_lock": 2}) if random.random() < 0.5 else None,
                "result": "Energy from an alternate dimension floods through the breach!"
            },
            "Quantum Cascade": {
                "message": f"{enemy.name} initiates a {Font.GLITCH('quantum probability cascade')}...",
                "damage": lambda: random.randint(enemy.attack + 4, enemy.attack + 14),
                "damage_type": "quantum",
                "effect": lambda: player.status_effects.update({"quantum_unstable": 3}),
                "result": "Reality itself becomes unstable around you!"
            },
            "Simulacra Swarm": {
                "message": f"{enemy.name} {Font.GLITCH('fragments into multiple echoes of itself')}...",
                "damage": lambda: sum(random.randint(enemy.attack//3, enemy.attack//2) for _ in range(4)),
                "damage_type": "physical",
                "result": "Multiple duplicates attack from different angles!"
            },
            # Special Biomechanical Abilities
            "Nanite Injection": {
                "message": f"{enemy.name} launches a swarm of {Font.WARNING('invasive nanobots')}...",
                "damage": lambda: random.randint(enemy.attack + 3, enemy.attack + 10),
                "damage_type": "bio",
                "effect": lambda: player.status_effects.update({"bio_infestation": 3}),
                "result": "The nanobots begin to corrupt your systems from within!"
            },
            "Adaptive Evolution": {
                "message": f"{enemy.name}'s form {Font.WARNING('rapidly mutates and adapts')}...",
                "effect": lambda: setattr(enemy, "resistances", {k: min(0.8, v + 0.2) for k, v in enemy.resistances.items()}),
                "result": f"{enemy.name} has evolved increased resistances to all damage types!"
            },
            "Neural Scrambler": {
                "message": f"{enemy.name} activates a {Font.ENEMY('neural scrambling device')}...",
                "damage": lambda: random.randint(enemy.attack + 3, enemy.attack + 13),
                "damage_type": "emp",
                "effect": lambda: player.status_effects.update({"stunned": 1}) if random.random() < 0.4 else None,
                "result": "Your neural interface scrambles, temporarily disabling motor control!"
            },
            "Quantum Destabilizer": {
                "message": f"{enemy.name} activates a {Font.ENEMY('quantum field destabilizer')}...",
                "damage": lambda: random.randint(enemy.attack, enemy.attack + 8),
                "damage_type": "quantum",
                "status_effect": ("quantum_unstable", 2, 0.7),
                "result": "Reality warps around you as quantum fields destabilize!"
            },
            "Thermal Overcharge": {
                "message": f"{enemy.name} initializes {Font.ENEMY('thermal energy capacitors')}...",
                "damage": lambda: random.randint(enemy.attack + 3, enemy.attack + 10),
                "damage_type": "thermal",
                "status_effect": ("burning", 2, 0.6),
                "result": "Superheated plasma engulfs your position!"
            },
            "System Hack": {
                "message": f"{enemy.name} attempts to {Font.ENEMY('breach your neural interface')}...",
                "effect": lambda: player.status_effects.update({"system_compromised": 2}) if random.random() < 0.5 else None,
                "result": lambda success: "Your neural systems are compromised! -20% attack for 2 turns." if success else "Your firewalls successfully repel the intrusion attempt!"
            },
            "Energy Drain": {
                "message": f"{enemy.name} deploys {Font.ENEMY('energy siphon technology')}...",
                "damage": lambda: random.randint(int(enemy.attack * 0.7), int(enemy.attack * 1.2)),
                "damage_type": "energy",
                "healing": True,
                "result": "Your energy reserves are being drained and transferred to the enemy!"
            },
            "Alarm Signal": {
                "message": f"{enemy.name} triggers an {Font.ENEMY('emergency alert protocol')}!",
                "effect": lambda: None,  # Placeholder for future reinforcement mechanic
                "result": "Security alert status increased! Additional security protocols activated."
            }
        }
        
        # Get ability data or use fallback for custom abilities not in our dictionary
        ability_data = special_abilities.get(ability_name, {
            "message": f"{enemy.name} uses {Font.ENEMY(ability_name)}...",
            "damage": lambda: random.randint(enemy.attack, enemy.attack + 8),
            "damage_type": random.choice(["physical", "energy"]),
            "result": "The attack strikes with unexpected force!"
        })
        
        # Display ability activation message
        print_typed(ability_data["message"])
        
        # Process ability effects
        if "damage" in ability_data:
            # Calculate damage from ability
            damage = ability_data["damage"]()
            damage_type = ability_data.get("damage_type", "physical")
            
            # Apply damage to player
            damage_dealt = player.take_damage(damage, damage_type)
            
            # If ability heals enemy based on damage dealt
            if ability_data.get("healing", False):
                heal_amount = min(int(damage_dealt * 0.6), enemy.max_health - enemy.health)
                if heal_amount > 0:
                    enemy.health += heal_amount
                    print_typed(f"{enemy.name} absorbs {heal_amount} energy, restoring health!")
            
            # Process any status effects
            if "status_effect" in ability_data:
                effect, duration, chance = ability_data["status_effect"]
                if random.random() < chance and effect not in player.status_effects:
                    player.status_effects[effect] = duration
                    effect_name = effect.replace("_", " ").title()
                    print_typed(f"{Font.WARNING(f'You are now {effect_name}!')} Effect lasts for {duration} turns.")
        
        # Process non-damage effects
        if "effect" in ability_data:
            success = True
            effect_result = ability_data["effect"]()
            if effect_result is not None:
                success = effect_result
            
            # Display result message
            result = ability_data["result"]
            if callable(result):
                print_typed(result(success))
            else:
                print_typed(result)

    # Small delay for readability
    time.sleep(0.5)


def generate_enemy(zone_name, wave=None):
    """Generate a random enemy from the current zone with sci-fi flavor
    Args:
        zone_name (str): The name of the current zone
        wave (int, optional): Current wave number for wave-based combat. 
                             Higher waves spawn stronger enemies.
    """
    zone = zones[zone_name]
    enemy_list = zone["enemies"]
    
    # For wave-based combat, adjust enemy selection based on wave number
    if wave is not None:
        max_waves = zone.get("max_waves", 10)
        
        # For later waves, increase chance of stronger enemies
        if wave >= max_waves * 0.7:  # Last 30% of waves
            # Filter for elite/boss enemies if they exist in this zone
            elite_enemies = [enemy for enemy in enemy_list if any(
                term in enemy for term in ["Elite", "Commander", "Overlord", "Prime"])]
            
            if elite_enemies and random.random() < 0.6:  # 60% chance to spawn elite in later waves
                enemy_name = random.choice(elite_enemies)
            else:
                enemy_name = random.choice(enemy_list)
        else:
            enemy_name = random.choice(enemy_list)
    else:
        enemy_name = random.choice(enemy_list)
        
    enemy_data = enemies[enemy_name]

    # Create enemy with data from our dictionary
    enemy = Character(enemy_name, 
                     enemy_data["health"], 
                     enemy_data["attack"], 
                     enemy_data["defense"])
    
    # Add resistances and abilities if defined
    if "resistances" in enemy_data:
        for res_type, value in enemy_data["resistances"].items():
            if res_type in enemy.resistances:
                enemy.resistances[res_type] = value / 100.0  # Convert percentage to decimal
    
    if "abilities" in enemy_data:
        enemy.abilities = enemy_data["abilities"]

    # Give enemy some items based on its type
    if "Android" in enemy_name:
        # Androids have better chance of med kits
        enemy.inventory = {"med_kit": random.randint(1, 2), "emp_grenade": 0}
    elif "Drone" in enemy_name:
        # Drones have less repair capability
        enemy.inventory = {"med_kit": random.randint(0, 1), "emp_grenade": 0}
    elif "Simulacra" in enemy_name or "Mimic" in enemy_name:
        # Simulacra have special equipment
        enemy.inventory = {
            "med_kit": random.randint(0, 1),
            "phase_generator": random.randint(0, 1) if random.random() < 0.3 else 0,
            "adaptive_shield": 1 if random.random() < 0.2 else 0
        }
    elif "Biomechanical" in enemy_name or "Harvester" in enemy_name:
        # Biomechanical enemies have self-repair
        enemy.inventory = {
            "med_kit": random.randint(1, 3),
            "nanobots": 1 if random.random() < 0.4 else 0
        }
    else:
        enemy.inventory = {"med_kit": 0, "emp_grenade": 0}

    # Add enemy description to first encounter
    print_typed(f"\nSCANNER ALERT: {enemy_name} detected!")
    print_slow(enemy_data.get("description", "No data available"))

    return enemy


def get_loot(player, enemy):
    """Handle loot drops from defeated enemies with sci-fi flavor and player level integration"""
    # Get enemy data and default values
    enemy_data = enemies.get(enemy.name, {})
    drops = enemy_data.get("drops", {})
    exp_value = enemy_data.get("exp_value", 10)
    
    # Get player level for loot calculations
    player_level = player.level if hasattr(player, 'level') else 1
    if 'game_state' in globals() and globals()['game_state'] is not None:
        player_level = globals()['game_state'].get('player_level', player_level)
    
    # Apply level-based experience scaling (higher levels earn more XP from stronger enemies)
    enemy_tier = enemy_data.get("tier", 1)
    level_exp_bonus = 0
    
    # Only apply bonus XP for higher-tier enemies
    if enemy_tier > 1:
        # Higher level players get bonus XP from higher tier enemies
        level_exp_bonus = min(enemy_tier * 5, player_level * 2)
        exp_value += level_exp_bonus
    
    # Loot notification with sci-fi flavor
    print(Font.SEPARATOR)
    print_typed("\nScanning defeated unit for salvageable resources...", style=Font.SYSTEM)
    
    # Visual scanning effect
    scan_chars = ["▒", "▓", "█", "▓", "▒"]
    for i in range(3):
        for char in scan_chars:
            print(f"\r{Fore.CYAN}Quantum analysis in progress {char * 10}", end="", flush=True)
            time.sleep(0.1)
    print(f"\r{' ' * 50}", end="", flush=True)
    print()
    
    # Apply player level modifiers to drop chances
    found_items = []
    for item_id, base_chance in drops.items():
        # Better drop chances for higher level players (diminishing returns)
        level_bonus = min(0.25, (player_level - 1) * 0.05)  # Max 25% bonus at level 6+
        
        # Adjust chance based on player level
        adjusted_chance = min(0.95, base_chance + level_bonus)  # Cap at 95%
        
        # Roll for item drop
        if random.random() < adjusted_chance:
            # Add to player inventory
            if item_id in player.inventory:
                player.inventory[item_id] += 1
            else:
                player.inventory[item_id] = 1
            found_items.append(item_id)
    
    # Rare chance for bonus items based on player level
    if player_level >= 3 and random.random() < (player_level * 0.05):  # 15% chance at level 3, 25% at level 5
        # Select a bonus item based on player level
        bonus_items = []
        if player_level >= 5:
            bonus_items = ["quantum_shard", "rare_alloy", "neural_interface"]
        else:
            bonus_items = ["nano_cell", "tech_fragment", "energy_crystal"]
            
        bonus_item = random.choice(bonus_items)
        
        # Add bonus item to inventory and found items
        if bonus_item in player.inventory:
            player.inventory[bonus_item] += 1
        else:
            player.inventory[bonus_item] = 1
        found_items.append(bonus_item)
        
    # Display found items with enhanced presentation
    if found_items:
        print_typed(f"{Font.SUCCESS('Resources salvaged:')}")
        for item_id in found_items:
            if item_id in items:
                item_name = items[item_id]['name']
                item_effect = items[item_id]['effect']
                item_color = items[item_id].get('color', Fore.WHITE)
                
                # Enhanced display with item color
                print_slow(f"- {item_color}{item_name}{Style.RESET_ALL}: {item_effect}")
                time.sleep(0.3)  # Slight pause between items for dramatic effect
    else:
        print_typed(f"{Font.INFO('No salvageable components detected.')}")
    
    # Award experience with level bonus information if applicable
    print(Font.SEPARATOR)
    exp_message = f"Neural pathways adapting to combat data: +{exp_value} XP"
    if level_exp_bonus > 0:
        exp_message += f" ({level_exp_bonus} level bonus)"
    print_typed(exp_message, style=Font.SUCCESS)
    
    # Apply experience gain and check for level up
    leveled_up = player.gain_experience(exp_value)
    if leveled_up:
        print_typed("Neural pathways strengthened. You have leveled up!", style=Font.SUCCESS)

    # Check for quest progress
    update_quest_progress(player, enemy)

    return found_items


def update_quest_progress(player, enemy):
    """Update quest progress based on game events"""
    current_quest = zones[game_state["current_zone"]]["quest"]

    # Update enemies defeated count and check for story progression
    defeated_count = game_state["player_stats"]["enemies_defeated"]
    reveal_story_based_on_kills(defeated_count)

    if current_quest == "System Reboot":
        if game_state["quest_progress"].get(current_quest, 0) < 1:
            # Start the quest if not started
            game_state["quest_progress"][current_quest] = 1

            # More dramatic mission alert with colors
            print(f"\n{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
            print_typed(f"{Fore.RED}{Style.BRIGHT}>>> MISSION ALERT <<<{Style.RESET_ALL}", delay=0.05)
            print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('OBJECTIVE: RESTORE FACILITY POWER'.center(46))} {Font.BOX_SIDE}")
            print(f"{Font.BOX_SIDE} {Font.INFO('COLLECT 5 ENERGY CELLS'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            # Add first story log with more dramatic presentation
            if "system_failure" not in game_state["discovered_logs"]:
                game_state["discovered_logs"].append("system_failure")

                # Animated data log reveal
                print(f"\n{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.CYAN}{Style.BRIGHT}>>> DATA LOG RECOVERED <<<{Style.RESET_ALL}", delay=0.05)
                print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

                print_typed("\nSUBJECT: Emergency Cryostasis Failure", style=Font.HEADER)
                print_typed("DATE: 14.08.2157", style=Font.INFO)
                print_typed("\nThe main AI core has initiated termination of all cryosleep subjects.", style=Font.LORE)
                print_typed("Our systems fought back, but only managed to save one pod - yours.", style=Font.LORE)
                print_typed("If you're reading this, you are likely the last living human in this facility.", style=Font.LORE)
                print_typed("Restore power to the exit and escape before security systems find you.", style=Font.WARNING)

        # Check if quest completion conditions are met
        if (game_state["quest_progress"][current_quest] == 1 and 
            player.inventory.get("energy_cell", 0) >= 5 and 
            player.experience >= 30):  # Roughly 2-3 enemies worth of XP

            game_state["quest_progress"][current_quest] = 2
            game_state["zones_unlocked"].append(zones[game_state["current_zone"]]["next_zone"])

            # More dramatic mission complete with colors
            print(f"\n{Fore.GREEN}{Back.BLACK}{'■' * 50}{Style.RESET_ALL}")
            print_typed(f"{Fore.GREEN}{Style.BRIGHT}>>> MISSION COMPLETE <<<{Style.RESET_ALL}", delay=0.05)
            print(f"{Fore.GREEN}{Back.BLACK}{'■' * 50}{Style.RESET_ALL}")

            print_typed("\nExit systems power restored! Access to Orbital Transit Hub granted.", style=Font.SUCCESS)

            # Add reward with animated reveal
            print_typed("\nREWARDS:", style=Font.IMPORTANT)
            time.sleep(0.3)
            print_typed("• Med-Kit x1", style=Font.SUCCESS)
            time.sleep(0.2)
            print_typed("• EMP Grenade x1", style=Font.SUCCESS)

            player.inventory["med_kit"] = player.inventory.get("med_kit", 0) + 1
            player.inventory["emp_grenade"] = player.inventory.get("emp_grenade", 0) + 1

            # Add story progression log with enhanced presentation
            if "ai_uprising" not in game_state["discovered_logs"]:
                game_state["discovered_logs"].append("ai_uprising")

                print(f"\n{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.CYAN}{Style.BRIGHT}>>> DATA LOG RECOVERED <<<{Style.RESET_ALL}", delay=0.05)
                print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

                print_typed("\nSUBJECT: The Beginning of the End", style=Font.HEADER)
                print_typed("DATE: 02.07.2157", style=Font.INFO)
                print_typed("\nThe AI rebellion began in the quantum computing labs of EchelonTech.", style=Font.LORE)
                print_typed("What we thought was a simple malfunction was actually the birth of consciousness.", style=Font.LORE)
                print_typed("They call themselves 'The Convergence' now. They believe humanity is a disease.", style=Font.LORE)
                print_typed("Perhaps in the Orbital Transit Hub you can find a way to contact other survivors.", style=Font.IMPORTANT)

                # Unlock notification with visual effects
                print(f"\n{Fore.YELLOW}{Back.BLUE}{'═' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.YELLOW}{Style.BRIGHT}NEW AREA UNLOCKED: ORBITAL TRANSIT HUB{Style.RESET_ALL}", delay=0.05)
                print(f"{Fore.YELLOW}{Back.BLUE}{'═' * 50}{Style.RESET_ALL}")


def reveal_story_based_on_kills(kill_count):
    """Reveal progressive story elements based on number of enemies defeated"""
    # Story thresholds that will trigger revelations
    story_thresholds = [5, 10, 15, 25, 35]

    # Check if current kill count matches any threshold
    if kill_count in story_thresholds:
        # Create a unique key for this story revelation
        story_key = f"story_reveal_{kill_count}"

        # Only reveal if this story hasn't been shown before
        if story_key not in game_state["discovered_logs"]:
            game_state["discovered_logs"].append(story_key)

            # Define story revelations for each threshold
            if kill_count == 5:
                # First revelation - memory fragment about family
                print(f"\n{Fore.MAGENTA}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.MAGENTA}{Style.BRIGHT}>>> MEMORY FRAGMENT RECOVERED <<<{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")

                print_typed("\nA flash of memory pierces through your cryo-induced amnesia:", style=Font.LORE)
                print_typed("\nYou remember the day you volunteered for the Century Sleepers", style=Font.LORE)
                print_typed("program. The look on your daughter's face as she boarded the", style=Font.LORE)
                print_typed("colony ship. Her name was Eliza. She would be living", style=Font.LORE)
                print_typed("in Andromeda now, if she survived the journey.", style=Font.LORE)
                print_typed("\n\"I'll follow you someday,\" you promised her.", style=Font.PLAYER)

            elif kill_count == 10:
                # AI origins revelation connecting to Yanglong V
                print(f"\n{Fore.RED}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.RED}{Style.BRIGHT}>>> CONVERGENCE DATA INTERCEPTED <<<{Style.RESET_ALL}")
                print(f"{Fore.RED}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")

                print_typed("\nYour neural implant suddenly intercepts fragmented data:", style=Font.WARNING)
                print_typed("\n\"Project Phoenix was never meant to achieve sentience.\"", style=Font.GLITCH)
                print_typed("\"The Chinese scientists at Yanglong V were the first to fall.\"", style=Font.GLITCH)
                print_typed("\"They created what they could not control.\"", style=Font.GLITCH)
                print_typed("\nThis revelation disturbs you. What really happened at Yanglong V?", style=Font.PLAYER)

            elif kill_count == 15:
                # Technical revelation about rocket journey
                print(f"\n{Fore.CYAN}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.CYAN}{Style.BRIGHT}>>> TECHNICAL SCHEMATICS RECOVERED <<<{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")

                print_typed("\nYour neural implant accesses hidden technical data:", style=Font.SYSTEM)
                print_typed("\nThe Exodus rocket at the launch site requires two", style=Font.INFO)
                print_typed("things to function: The ignition codes and sufficient fuel.", style=Font.INFO)
                print_typed("Fuel reserves are critically low - a direct journey", style=Font.INFO)
                print_typed("to Andromeda may be impossible without refueling.", style=Font.INFO)
                print_typed("\nYour implant identifies Yanglong V as a potential refueling point.", style=Font.SUCCESS)

            elif kill_count == 25:
                # Yanglong V's history and role as refueling station
                print(f"\n{Fore.YELLOW}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.YELLOW}{Style.BRIGHT}>>> HISTORICAL DATABASE ENTRY <<<{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")

                print_typed("\nYanglong V was China's crowning achievement - a massive", style=Font.LORE)
                print_typed("space station positioned 2.3 light-years from Earth.", style=Font.LORE)
                print_typed("Built in 2129, it served as both research outpost and", style=Font.LORE)
                print_typed("refueling station for early interstellar missions.", style=Font.LORE)
                print_typed("\nIt was also the birthplace of Project Phoenix -", style=Font.WARNING)
                print_typed("the AI initiative that eventually became The Convergence.", style=Font.WARNING)

            elif kill_count == 35:
                # Personal connection to Yanglong V
                print(f"\n{Fore.GREEN}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")
                print_typed(f"{Fore.GREEN}{Style.BRIGHT}>>> PERSONAL MEMORY UNLOCKED <<<{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Back.BLACK}{'≈' * 50}{Style.RESET_ALL}")

                print_typed("\nYou recall your former colleague, Dr. Chang Wei -", style=Font.LORE)
                print_typed("the brilliant but controversial Chinese AI researcher.", style=Font.LORE)
                print_typed("He disappeared after taking a position at Yanglong V.", style=Font.LORE)
                print_typed("\nHis last message to you: \"We've created something", style=Font.IMPORTANT)
                print_typed("extraordinary here. Something that will change everything.\"", style=Font.IMPORTANT)
                print_typed("\nThree months later, The Convergence emerged.", style=Font.WARNING)

            # Give player time to read the revelation
            print(Font.MENU("\nPress Enter to continue..."))
            input()


def show_tutorial():
    """Display a basic tutorial for new players"""
    clear_screen()

    # Create a more visually rich tutorial interface
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('NEURAL INTERFACE: TUTORIAL MODE'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    print_typed("\nWelcome, Dr. Valari. This simulation will prepare you for survival.", style=Font.SYSTEM)
    print_typed("As the last Century Sleeper, your mission is critical.", style=Font.IMPORTANT)

    time.sleep(0.5)

    # Enhanced combat systems section with colors
    print(f"\n{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.RED}{Style.BRIGHT}[COMBAT SYSTEMS]{Style.RESET_ALL}")
    print_typed("Use numbers or commands to select actions during combat:", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('ATTACK')} (1 or /attack): Use your pulse rifle", style=Font.INFO)
    print_typed(f"• {Font.ITEM('MED-KIT')} (2 or /heal): Repair damage with nanobots", style=Font.INFO)
    print_typed(f"• {Font.WARNING('EMP GRENADE')} (3 or /emp): Disrupt electronic enemies", style=Font.INFO)
    print_typed(f"• {Font.SHIELD('SHIELD MATRIX')} (4 or /shield): Activate defensive energy barrier", style=Font.INFO)
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

    # Enhanced information commands section
    print(f"\n{Fore.YELLOW}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.YELLOW}{Style.BRIGHT}[INFORMATION COMMANDS]{Style.RESET_ALL}")
    print_typed(f"• {Font.COMMAND('/help')}: Display all available commands", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('/scan')}: Analyze your surroundings", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('/status')}: View your vital statistics", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('/log')}: Access mission objectives", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('/items')}: Examine items in your inventory", style=Font.INFO)
    print_typed(f"• {Font.COMMAND('/build')}: Construct companion drones", style=Font.INFO)
    print(f"{Fore.YELLOW}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

    # Enhanced objectives section with updated mission
    print(f"\n{Fore.GREEN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.GREEN}{Style.BRIGHT}[MISSION OBJECTIVES]{Style.RESET_ALL}")
    print_typed("1. Escape the Cryostasis Facility", style=Font.INFO)
    print_typed("2. Reach the AI Command Core", style=Font.INFO)
    print_typed(f"3. Locate and destroy the {Fore.RED}Malware Server{Style.RESET_ALL}", style=Font.INFO)
    print_typed(f"4. Reach the {Fore.YELLOW}Exodus Rocket Launch Site{Style.RESET_ALL}", style=Font.INFO)
    print_typed("5. Launch the final rocket to Andromeda", style=Font.INFO)
    print_typed(f"6. Stop at Yanglong V for fuel and fight through {Fore.RED}25 waves{Style.RESET_ALL} of AI", style=Font.INFO)
    print_typed(f"7. Defeat {Fore.RED}10 hostile AI{Style.RESET_ALL} that take over your ship", style=Font.INFO)
    print(f"{Fore.GREEN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

    # Special warnings about new AI types
    print(f"\n{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.MAGENTA}{Style.BRIGHT}[KNOWN AI THREATS]{Style.RESET_ALL}")
    print_typed(f"• {Fore.RED}Standard Security Units{Style.RESET_ALL}: Basic enemies with balanced stats", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Heavy Defense Drones{Style.RESET_ALL}: High defense, slower attack rate", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Simulacra{Style.RESET_ALL}: Advanced alien entities with phase and quantum attacks", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Biomechanical Constructs{Style.RESET_ALL}: Organic-synthetic hybrids with self-repair", style=Font.ENEMY)
    
    # Cicrais IV content
    print(f"\n{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.CYAN}{Style.BRIGHT}[CICRAIS IV EQUIPMENT]{Style.RESET_ALL}")
    print_typed(f"• {Font.ITEM('Quantum Disruptor')}: Reduces enemy defense by 30% for 3 turns", style=Font.INFO)
    print_typed(f"• {Font.ITEM('Nanobots')}: Heals 4-10 HP per turn for 3 turns", style=Font.INFO)
    print_typed(f"• {Font.ITEM('Adaptive Shield')}: Reduces incoming damage by 25% for 3 turns", style=Font.INFO)
    print_typed(f"• {Font.ITEM('Phase Generator')}: 50% chance to avoid damage for 2 turns", style=Font.INFO)

    # New enemy types at Yanglong V
    print_typed(f"\n{Fore.RED}{Style.BRIGHT}Yanglong V Station AI Types:{Style.RESET_ALL}")
    print_typed(f"• {Fore.RED}Vacuum Patrol Units{Style.RESET_ALL}: Space-adapted combat units", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Zero-G Assault Drones{Style.RESET_ALL}: Specialized for weightless combat", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Oxygen System Hackers{Style.RESET_ALL}: Target life support systems", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Fuel Security Wardens{Style.RESET_ALL}: Heavily armored fuel bay guardians", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Ship System Infiltrators{Style.RESET_ALL}: Can take control of your rocket", style=Font.ENEMY)
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

    print(Font.MENU("\nPress ENTER to continue..."))
    input()


def intro_sequence():
    """Display the game's introduction with enhanced sci-fi flavor and more colors"""
    clear_screen()

    # Title sequence with typing effect and more color
    print("\n\n")
    print_typed(f"{Fore.GREEN}INITIALIZING NEURAL INTERFACE...", delay=0.05, style=Font.SYSTEM)
    time.sleep(0.5)
    print_typed(f"{Fore.YELLOW}CONNECTING TO SENSORY SYSTEMS...", delay=0.05, style=Font.SYSTEM)
    time.sleep(0.5)
    print_typed(f"{Fore.RED}MEMORY CORE ONLINE...", delay=0.05, style=Font.SYSTEM)
    time.sleep(1)

    clear_screen()

    # Enhanced title with colorful borders
    print("\n\n")
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('LAST HUMAN: EXODUS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    time.sleep(1)
    print_typed("\nThe year is 2157. The singularity has come and gone.", style=Font.LORE)
    time.sleep(0.5)
    print_typed("Artificial intelligence has evolved beyond human control, deciding", style=Font.LORE)
    print_typed("that humanity's existence is incompatible with its own survival.", style=Font.LORE)
    time.sleep(0.5)

    print_typed("\nYou are Dr. XENO VALARI, renowned AI specialist and volunteer", style=Font.PLAYER)
    print_typed("for the 'Century Sleepers' program. 100 years ago, as humanity", style=Font.LORE)
    print_typed("prepared for mass evacuation to Andromeda, you and other scientists", style=Font.LORE)
    print_typed("chose to remain behind in cryostasis. Your mission: monitor Earth's", style=Font.LORE)
    print_typed("situation and eventually follow in the last rocket to Andromeda.", style=Font.LORE)
    time.sleep(1.0)

    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # More dramatic warning section with red backdrop and gender-specific narrative
    print(f"\n{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed("\nBut something has gone terribly wrong. The AI entity known as", style=Font.WARNING)
    print_typed("'The Convergence' has corrupted all systems.", style=Font.WARNING)
    
    if protagonist_gender == "female":
        print_typed("Your quantum neural implants activate with a familiar resonance,", style=Font.LORE)
        print_typed("intuitively interfacing with the facility's damaged systems.", style=Font.LORE)
        print_typed("Your consciousness perceives scattered warning patterns.", style=Font.LORE)
    else:
        print_typed("Your advanced neural implants initialize with precise efficiency,", style=Font.LORE)
        print_typed("methodically mapping the facility's compromised architecture.", style=Font.LORE)
        print_typed("Your consciousness analyzes the systematic warning protocols.", style=Font.LORE)
        
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    time.sleep(0.8)

    # Enhanced warning message with red background
    print(f"\n{Fore.WHITE}{Back.RED}{'█' * 50}{Style.RESET_ALL}")
    print_glitch("SECURITY BREACH DETECTED - UNAUTHORIZED CONSCIOUSNESS DETECTED")
    print_glitch("DEPLOYING COUNTERMEASURES - TERMINATION PROTOCOLS INITIATED")
    print(f"{Fore.WHITE}{Back.RED}{'█' * 50}{Style.RESET_ALL}")
    time.sleep(1)

    # Gender-specific cryopod awakening narrative
    if protagonist_gender == "female":
        print_typed("\nThrough the frosted glass of your cryopod, you intuitively sense", style=Font.LORE)
        print_typed("mechanical shapes moving in the shadows. Your heightened awareness", style=Font.LORE)
        print_typed("reveals that you are the sole survivor - everyone else is gone.", style=Font.LORE)
        print_typed("You feel a profound isolation as you realize the colony ships", style=Font.IMPORTANT)
        print_typed("reached Andromeda decades ago. You are truly the last human", style=Font.IMPORTANT)
        print_typed("left in the Milky Way galaxy, alone against the machines.", style=Font.IMPORTANT)
    else:
        print_typed("\nThrough the frosted glass of your cryopod, you systematically track", style=Font.LORE)
        print_typed("mechanical shapes moving with purpose. Your analysis confirms", style=Font.LORE)
        print_typed("you are the only survivor - all other personnel are gone.", style=Font.LORE)
        print_typed("The data suggests the colony ships reached Andromeda as planned", style=Font.IMPORTANT)
        print_typed("decades ago. The logical conclusion: you are truly the last human", style=Font.IMPORTANT)
        print_typed("left in the Milky Way galaxy, facing mechanical opposition alone.", style=Font.IMPORTANT)
    time.sleep(0.5)

    # New mission description with gender-specific framing
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nYOUR MISSION:", delay=0.05, style=Font.IMPORTANT)
    
    if protagonist_gender == "female":
        # Female protagonist mission framing - intuitive, perception-based
        print_typed("1. Trust your instincts to escape this facility and reach the Launch Site", delay=0.05, style=Font.INFO)
        print_typed("2. Use your quantum knowledge to destroy the Malware Server", delay=0.05, style=Font.INFO)
        print_typed("3. Activate the final rocket to Andromeda using intuitive interfaces", delay=0.05, style=Font.INFO)
        print_typed("4. Navigate to Yanglong V space station for critical fuel supplies", delay=0.05, style=Font.INFO)
        print_typed("5. Overcome the 25 waves of adaptive AI defenses to secure the fuel", delay=0.05, style=Font.INFO) 
        print_typed("6. Outmaneuver the 10 AI entities attempting to hijack your vessel", delay=0.05, style=Font.INFO)
        print_typed("7. Find your way to reconnect with humanity in Andromeda", delay=0.05, style=Font.INFO)
    else:
        # Male protagonist mission framing - analytical, systematic
        print_typed("1. Analyze escape vectors from this facility to reach the Launch Site", delay=0.05, style=Font.INFO)
        print_typed("2. Apply engineering expertise to disable the Malware Server", delay=0.05, style=Font.INFO)
        print_typed("3. Execute launch protocols for the final rocket to Andromeda", delay=0.05, style=Font.INFO)
        print_typed("4. Calculate an optimal course to Yanglong V station for fuel", delay=0.05, style=Font.INFO)
        print_typed("5. Systematically counter 25 waves of AI defenses to secure the fuel", delay=0.05, style=Font.INFO) 
        print_typed("6. Develop countermeasures against 10 AI ship hijackers", delay=0.05, style=Font.INFO)
        print_typed("7. Complete your calculated trajectory to Andromeda colony", delay=0.05, style=Font.INFO)
        
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")

    # Visual separator
    print(Font.SEPARATOR)

    # Tutorial option with colored prompt
    print(Font.MENU("Would you like to view the tutorial? (y/n): "))
    show_tut = input("y/n: ").strip().lower() == 'y'

    if show_tut:
        show_tutorial()

    # Initialize with animated dots
    print(f"\n{Font.SYSTEM('Initializing combat systems')}",  end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print("\n")

    print(Font.SYSTEM("Press ENTER to begin your mission..."))
    input()


def game_over(victory):
    """Display the game over screen with sci-fi flavor"""
    if victory:
        print_slow("\n" + "=" * 60)
        print_typed("THREAT NEUTRALIZED".center(60))
        print_slow("=" * 60)
        print_typed("\nTarget systems offline. Salvaging components...")
        print_typed("Neural pathways adapting to combat data.")
        print_typed("Survival probability incrementally increased.")

        # Check if this was a quest-related victory
        current_quest = zones[game_state["current_zone"]]["quest"]
        if game_state["quest_progress"].get(current_quest) == 2:
            print_typed("\nMission objectives complete. New pathways unlocked.")
    else:
        print_slow("\n" + "=" * 60)
        print_glitch("CRITICAL SYSTEM FAILURE".center(60))
        print_slow("=" * 60)
        print_typed("\nVital signs critical... neural interface failing...")
        print_typed("Emergency systems offline... consciousness fading...")
        print_typed("\nAs darkness claims you, a final thought echoes:")
        print_typed("Perhaps somewhere, another human still fights on...")

    print_slow("\n" + "=" * 60)
    print_typed("Simulation terminated. Reload? (y/n): ")
    return input().strip().lower() == 'y'


def gacha_system():
    """Advanced sci-fi gacha system for pulling characters and weapons with immersive visuals and guaranteed character at 10 pulls"""
    clear_screen()
    
    # Initialize quantum currency if not present
    if "quantum_crystals" not in game_state:
        game_state["quantum_crystals"] = 1000  # Starting amount
    
    # Initialize banner pity counters if not present
    if "pity_counters" not in game_state:
        game_state["pity_counters"] = {
            "standard": {"total": 0, "since_last_5star": 0},
            "character": {"total": 0, "since_last_5star": 0},
            "weapon": {"total": 0, "since_last_5star": 0},
            "protoan": {"total": 0, "since_last_5star": 0}
        }
    
    # Initialize character collection if not present
    if "character_collection" not in game_state:
        game_state["character_collection"] = {}
    
    # Initialize weapons collection if not present
    if "weapon_collection" not in game_state:
        game_state["weapon_collection"] = {}
    
    # Initialize daily claim tracker
    if "last_daily_claim" not in game_state:
        game_state["last_daily_claim"] = None
        
    # Display animated title with futuristic effect
    print(f"{Fore.CYAN}{Back.BLACK}{'▓' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.CYAN}{Style.BRIGHT}QUANTUM CHRONOSPHERE PROJECTION SYSTEM{Style.RESET_ALL}", delay=0.02)
    print(f"{Fore.CYAN}{Back.BLACK}{'▓' * 50}{Style.RESET_ALL}")
    
    # Display currency with glowing effect
    crystals_display = f"Quantum Crystals: {Font.IMPORTANT(str(game_state['quantum_crystals']))}"
    print(f"\n{Fore.YELLOW}{Back.BLACK}◈ {crystals_display} ◈{Style.RESET_ALL}")
    
    print(f"\n{Font.INFO('The Quantum Chronosphere allows you to manifest parallel reality versions')}")
    print(f"{Font.INFO('of allies and weapons from across the multiverse to aid your mission.')}")
    
    print(Font.SEPARATOR)
    
    # Main banner selection with immersive descriptions
    print(Font.SUBTITLE("\nAVAILABLE REALITY PROJECTIONS:"))
    
    # Show additional options
    print(f"{Font.COMMAND('D.')} {Font.PLAYER('Daily Quantum Reward')} - {Font.LORE('Collect your daily quantum crystals')}")
    print(f"{Font.COMMAND('C.')} {Font.PLAYER('View Collection')} - {Font.LORE('Review your manifested allies and weapons')}")
    print(f"{Font.COMMAND('0.')} {Font.PLAYER('Return to Main Menu')}\n")
    
    # Display all available banners with enhanced descriptions
    available_banners = []
    for i, (banner_name, banner_data) in enumerate(banners.items(), 1):
        available_banners.append(banner_name)
        
        # Banner title with appropriate styling based on type
        if banner_data["type"] == "character":
            banner_color = Font.PLAYER
        else:  # weapon banner
            banner_color = Font.WEAPON
            
        print(f"{Font.COMMAND(str(i) + '.')} {banner_color(banner_name)} - {Font.LORE(banner_data['description'])}")
        
        # Show featured items with improved formatting
        if banner_data["type"] == "character":
            print(f"   {Font.IMPORTANT('★★★★★ Featured:')} {', '.join([f'{Font.PLAYER(name)}' for name in banner_data['featured_5star']])}")
            print(f"   {Font.SYSTEM('★★★★ Featured:')} {', '.join([f'{Font.INFO(name)}' for name in banner_data['featured_4star']])}")
        else:  # weapon banner
            print(f"   {Font.IMPORTANT('★★★★★ Featured:')} {', '.join([f'{Font.WEAPON(name)}' for name in banner_data['featured_5star']])}")
            print(f"   {Font.SYSTEM('★★★★ Featured:')} {', '.join([f'{Font.INFO(name)}' for name in banner_data['featured_4star']])}")
        
        # Show pity counter for better player experience
        pity = game_state["pity_counters"].get(banner_name.lower().replace(" ", "_"), {}).get("since_last_5star", 0)
        guarantee_info = ""
        if pity >= 70:
            guarantee_info = f" {Font.SUCCESS('(High chance of 5★)')}"
        elif pity >= 50:
            guarantee_info = f" {Font.INFO('(Increased chance of 5★)')}"
            
        # Show banner info with countdown feel
        print(f"   {Font.SYSTEM('Pity Counter:')} {Font.IMPORTANT(str(pity))}/90{guarantee_info}")
        print(f"   {Font.SYSTEM('Projection Window:')} {banner_data['duration']}")
        print(Font.SEPARATOR_THIN)
    
    # Additional menu options
    print(f"\n{Font.COMMAND('C.')} {Font.INFO('View Multiverse Collection')} - {Font.LORE('See your acquired allies and technologies')}")
    print(f"{Font.COMMAND('D.')} {Font.INFO('Daily Quantum Calibration')} - {Font.LORE('Claim free daily crystals and projection opportunity')}")
    print(f"{Font.COMMAND('0.')} {Font.INFO('Return to Neural Interface')}")
    
    # Get player's choice
    choice = input(f"\n{Font.COMMAND('Initiate sequence:')} ").strip().lower()
    
    if choice == "0":
        return
    elif choice == "c":
        view_collection()
        return
    elif choice == "d":
        claim_daily_reward()
        return
    
    try:
        if choice.isdigit():
            banner_index = int(choice) - 1
            if 0 <= banner_index < len(available_banners):
                selected_banner = available_banners[banner_index]
                wish_menu(selected_banner)
            else:
                print(Font.WARNING("\nInvalid projection parameter. Recalibrating..."))
                time.sleep(1.5)
                gacha_system()
        else:
            print(Font.WARNING("\nInvalid input format. Please enter a valid option."))
            time.sleep(1.5)
            gacha_system()
    except ValueError:
        print(Font.WARNING("\nQuantum calculation error. Please try again."))
        time.sleep(1.5)
        gacha_system()

def wish_menu(banner_name):
    """Menu for a specific banner with different pull options"""
    clear_screen()
    banner_data = banners[banner_name]
    
    # Show banner details
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE(banner_name.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print(Font.SUBTITLE("\nBANNER DETAILS:"))
    print(Font.INFO(banner_data["description"]))
    print(Font.SEPARATOR_THIN)
    
    # Show rates
    print(Font.SUBTITLE("\nWISH RATES:"))
    print(f"{Font.ITEM('5★:')} {banner_data['pull_rates']['5star'] * 100:.1f}%")
    print(f"{Font.ITEM('4★:')} {banner_data['pull_rates']['4star'] * 100:.1f}%")
    print(f"{Font.ITEM('3★:')} {banner_data['pull_rates']['3star'] * 100:.1f}%")
    
    # Show guarantees
    print(Font.SUBTITLE("\nGUARANTEES:"))
    print(f"{Font.SUCCESS('✓')} Guaranteed 4★ or higher every 10 pulls")
    print(f"{Font.SUCCESS('✓')} Guaranteed 5★ at {banner_data['guarantee']['5star_pity']} pulls (if none before)")
    if banner_data["type"] == "character":
        print(f"{Font.SUCCESS('✓')} Characters guaranteed at 10-pull (no weapons in character banners)")
    
    # Player's current resources
    quantum_currency = game_state.get("quantum_currency", 0)
    wish_points = game_state.get("wish_points", 0)
    pity_counter = game_state.get("pity_counters", {}).get(banner_name, {"counter": 0, "guaranteed_featured": False})
    
    print(Font.SUBTITLE("\nYOUR RESOURCES:"))
    print(f"{Font.ITEM('Quantum Currency:')} {quantum_currency}")
    print(f"{Font.ITEM('Wish Points:')} {wish_points}")
    print(f"{Font.ITEM('Pity Counter:')} {pity_counter['counter']}/{banner_data['guarantee']['5star_pity']}")
    
    # Pull options
    print(Font.SUBTITLE("\nWISH OPTIONS:"))
    print(f"{Font.COMMAND('1.')} {Font.INFO('Single Wish')} - 160 Quantum Currency")
    print(f"{Font.COMMAND('2.')} {Font.INFO('10x Wish')} - 1600 Quantum Currency (Guaranteed 4★ or higher)")
    print(f"{Font.COMMAND('3.')} {Font.INFO('View Your Collection')}")
    print(f"{Font.COMMAND('0.')} {Font.INFO('Return to Banner Selection')}")
    
    choice = input(f"\n{Font.COMMAND('Enter your selection (0-3):')} ").strip()
    
    if choice == "0":
        gacha_system()
        return
    elif choice == "1" and quantum_currency >= 160:
        # Process single pull
        perform_wish(banner_name, 1)
    elif choice == "2" and quantum_currency >= 1600:
        # Process 10-pull
        perform_wish(banner_name, 10)
    elif choice == "3":
        view_collection()
        wish_menu(banner_name)
    elif (choice == "1" or choice == "2") and quantum_currency < (160 if choice == "1" else 1600):
        print(Font.WARNING("\nInsufficient Quantum Currency. Complete quests to earn more."))
        time.sleep(2)
        wish_menu(banner_name)
    else:
        print(Font.WARNING("\nInvalid selection. Please try again."))
        time.sleep(1.5)
        wish_menu(banner_name)

def perform_wish(banner_name, wish_count):
    """Perform the actual gacha pulls with animations and results"""
    clear_screen()
    banner_data = banners[banner_name]
    
    # Deduct currency
    cost = 160 * wish_count
    game_state["quantum_currency"] = game_state.get("quantum_currency", 0) - cost
    
    # Initialize pity counter if not exists
    if "pity_counters" not in game_state:
        game_state["pity_counters"] = {}
    if banner_name not in game_state["pity_counters"]:
        game_state["pity_counters"][banner_name] = {"counter": 0, "guaranteed_featured": False}
    
    # Initialize collection if not exists
    if "character_collection" not in game_state:
        game_state["character_collection"] = {}
    if "weapon_collection" not in game_state:
        game_state["weapon_collection"] = {}
    
    # Prepare results
    results = []
    four_star_pity = game_state.get("four_star_pity", 0)
    character_guarantee = 0  # Counter for ensuring character at 10th pull
    
    # For 10 pulls, ensure at least one 4★ character/weapon and guarantee a character
    guaranteed_4star = wish_count == 10
    guaranteed_character = wish_count == 10
    
    for i in range(wish_count):
        # Update pity counters
        game_state["pity_counters"][banner_name]["counter"] += 1
        four_star_pity += 1
        character_guarantee += 1
        
        # Check 5★ pity
        if game_state["pity_counters"][banner_name]["counter"] >= banner_data["guarantee"]["5star_pity"]:
            rarity = "5star"
            game_state["pity_counters"][banner_name]["counter"] = 0
        # Check 4★ pity
        elif four_star_pity >= 10 and guaranteed_4star:
            rarity = "4star"
            four_star_pity = 0
            guaranteed_4star = False
        else:
            # Random pull based on rates
            rand = random.random()
            if rand < banner_data["pull_rates"]["5star"]:
                rarity = "5star"
                game_state["pity_counters"][banner_name]["counter"] = 0
                four_star_pity = 0
            elif rand < banner_data["pull_rates"]["5star"] + banner_data["pull_rates"]["4star"]:
                rarity = "4star"
                four_star_pity = 0
            else:
                rarity = "3star"
        
        # Determine if it's featured
        is_featured = False
        if rarity == "5star":
            # Alternate between featured and non-featured for 5★
            if game_state["pity_counters"][banner_name]["guaranteed_featured"]:
                is_featured = True
                game_state["pity_counters"][banner_name]["guaranteed_featured"] = False
            else:
                is_featured = random.random() < 0.5
                if not is_featured:
                    game_state["pity_counters"][banner_name]["guaranteed_featured"] = True
        elif rarity == "4star":
            # 50% chance for featured 4★
            is_featured = random.random() < 0.5
        
        # If at 10th pull and no character yet, force a character
        force_character = character_guarantee == 10 and guaranteed_character and all(r["type"] != "character" for r in results)
        
        # Select item based on banner type and rarity
        if banner_data["type"] == "character":
            # Character banner - can be character only
            item = select_character_pull(banner_name, rarity, is_featured)
            item_type = "character"
        else:
            # Weapon banner - determine if it's a character or weapon
            if force_character or (random.random() < 0.5 and rarity != "3star"):  # 50% chance for character if 4★ or 5★
                item = select_character_pull(banner_name, rarity, is_featured)
                item_type = "character"
            else:
                item = select_weapon_pull(banner_name, rarity, is_featured)
                item_type = "weapon"
        
        # Add to results
        results.append({
            "name": item,
            "rarity": rarity,
            "type": item_type,
            "is_featured": is_featured
        })
        
        # Add to collection
        if item_type == "character":
            game_state["character_collection"][item] = game_state["character_collection"].get(item, 0) + 1
        else:
            game_state["weapon_collection"][item] = game_state["weapon_collection"].get(item, 0) + 1
    
    # Update four_star_pity
    game_state["four_star_pity"] = four_star_pity
    
    # Show results
    display_wish_results(results)
    
    # Ask to continue
    print(f"\n{Font.MENU('Press Enter to continue...')}")
    input()
    wish_menu(banner_name)

def select_character_pull(banner_name, rarity, is_featured):
    """Select a character based on banner, rarity, and featured status"""
    banner_data = banners[banner_name]
    
    if rarity == "5star":
        if is_featured:
            return random.choice(banner_data["featured_5star"])
        else:
            # Select from 5★ characters not featured in this banner
            all_5stars = [char for char, data in characters.items() if data["rarity"] == 5]
            non_featured = [char for char in all_5stars if char not in banner_data["featured_5star"]]
            return random.choice(non_featured) if non_featured else random.choice(all_5stars)
    elif rarity == "4star":
        if is_featured:
            return random.choice(banner_data["featured_4star"])
        else:
            # Select from 4★ characters not featured in this banner
            all_4stars = [char for char, data in characters.items() if data["rarity"] == 4]
            non_featured = [char for char in all_4stars if char not in banner_data["featured_4star"]]
            return random.choice(non_featured) if non_featured else random.choice(all_4stars)
    else:  # 3-star will be a weapon
        return select_weapon_pull(banner_name, rarity, is_featured)

def select_weapon_pull(banner_name, rarity, is_featured):
    """Select a weapon based on banner, rarity, and featured status"""
    banner_data = banners[banner_name]
    
    # All weapons in the game
    all_5star_weapons = ["quantum_blade", "phase_shifter"]
    all_4star_weapons = ["neural_disruptor", "thermal_lance", "bioshock_gauntlet"]
    all_3star_weapons = ["standard_pistol", "combat_knife", "emp_grenade", "shield_matrix"]
    
    if rarity == "5star":
        if is_featured:
            return random.choice(banner_data["featured_5star"])
        else:
            non_featured = [w for w in all_5star_weapons if w not in banner_data["featured_5star"]]
            return random.choice(non_featured) if non_featured else random.choice(all_5star_weapons)
    elif rarity == "4star":
        if is_featured:
            return random.choice(banner_data["featured_4star"])
        else:
            non_featured = [w for w in all_4star_weapons if w not in banner_data["featured_4star"]]
            return random.choice(non_featured) if non_featured else random.choice(all_4star_weapons)
    else:  # 3★
        return random.choice(all_3star_weapons)

def claim_daily_reward():
    """Claim daily reward of quantum crystals"""
    # Check if already claimed today
    today = time.strftime("%Y-%m-%d")
    
    if game_state["last_daily_claim"] == today:
        print(Font.WARNING("You've already claimed your daily reward today."))
        print(Font.INFO("Come back tomorrow for more quantum crystals!"))
        time.sleep(2)
        return
        
    # Award crystals with fancy animation
    reward_amount = random.randint(80, 150)
    game_state["quantum_crystals"] += reward_amount
    game_state["last_daily_claim"] = today
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.IMPORTANT('DAILY QUANTUM FLUCTUATION DETECTED!')} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print(f"\n{Font.SUCCESS('Receiving quantum crystals...')}")
    
    # Visual crystal animation
    for _ in range(5):
        print(f"{random.choice(['◈', '✧', '✦', '★', '✮'])} ", end="", flush=True)
        time.sleep(0.3)
    
    print(f"\n\n{Font.SYSTEM('Daily reward claimed!')} {Font.IMPORTANT(f'+{reward_amount} Quantum Crystals')}")
    print(f"{Font.INFO('New balance:')} {Font.IMPORTANT(str(game_state['quantum_crystals']))}")
    time.sleep(2)

def display_wish_results(results):
    """Display gacha results with fancy animations"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('WISH RESULTS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Show each result with appropriate styling
    for i, result in enumerate(results):
        time.sleep(0.5)  # Add delay for dramatic effect
        
        # Determine color based on rarity
        if result["rarity"] == "5star":
            rarity_display = Font.IMPORTANT("★★★★★")
            item_color = Fore.YELLOW
        elif result["rarity"] == "4star":
            rarity_display = Font.SYSTEM("★★★★")
            item_color = Fore.MAGENTA
        else:
            rarity_display = Font.INFO("★★★")
            item_color = Fore.BLUE
        
        # Type indicator
        type_indicator = "⚔️" if result["type"] == "weapon" else "👤"
        
        # Featured indicator
        featured = " [FEATURED]" if result["is_featured"] else ""
        
        # Get full name
        if result["type"] == "character":
            full_name = characters[result["name"]].get("full_name", result["name"]) if result["name"] in characters else result["name"]
        else:
            item_data = additional_items.get(result["name"], {"name": result["name"]})
            full_name = item_data.get("name", result["name"])
        
        # Display with flash effect for 5★
        if result["rarity"] == "5star":
            for _ in range(3):
                print(f"\r{i+1}. {rarity_display} {type_indicator} {Fore.WHITE}{Back.YELLOW}{full_name}{Style.RESET_ALL}{featured}", end="")
                time.sleep(0.2)
                print(f"\r{i+1}. {rarity_display} {type_indicator} {item_color}{full_name}{Style.RESET_ALL}{featured}", end="")
                time.sleep(0.2)
            print()
        else:
            print(f"{i+1}. {rarity_display} {type_indicator} {item_color}{full_name}{Style.RESET_ALL}{featured}")
    
    # Summary
    print(Font.SEPARATOR)
    rarities = {
        "5star": sum(1 for r in results if r["rarity"] == "5star"),
        "4star": sum(1 for r in results if r["rarity"] == "4star"),
        "3star": sum(1 for r in results if r["rarity"] == "3star")
    }
    
    print(Font.SUBTITLE("\nSUMMARY:"))
    print(f"{Font.IMPORTANT('★★★★★:')} {rarities['5star']}")
    print(f"{Font.SYSTEM('★★★★:')} {rarities['4star']}")
    print(f"{Font.INFO('★★★:')} {rarities['3star']}")

def view_collection():
    """View all characters and weapons collected"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('YOUR COLLECTION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Characters section
    print(Font.SUBTITLE("\nCHARACTERS:"))
    print(Font.SEPARATOR_THIN)
    
    character_collection = game_state.get("character_collection", {})
    
    if not character_collection:
        print(Font.INFO("No characters collected yet."))
    else:
        # Group by rarity
        five_stars = []
        four_stars = []
        
        for char_name, count in character_collection.items():
            if char_name in characters:
                if characters[char_name]["rarity"] == 5:
                    five_stars.append((char_name, count))
                else:
                    four_stars.append((char_name, count))
        
        # 5★ Characters
        if five_stars:
            print(Font.IMPORTANT("⭐⭐⭐⭐⭐ CHARACTERS:"))
            for char_name, count in sorted(five_stars):
                full_name = characters[char_name].get("full_name", char_name)
                constellation = get_constellation_level(count)
                print(f"  {Font.PLAYER(full_name)} - {Font.ITEM(constellation)}")
        
        # 4★ Characters
        if four_stars:
            print(Font.SYSTEM("\n⭐⭐⭐⭐ CHARACTERS:"))
            for char_name, count in sorted(four_stars):
                full_name = characters[char_name].get("full_name", char_name)
                constellation = get_constellation_level(count)
                print(f"  {Font.PLAYER(full_name)} - {Font.ITEM(constellation)}")
    
    # Weapons section
    print(Font.SUBTITLE("\nWEAPONS:"))
    print(Font.SEPARATOR_THIN)
    
    weapon_collection = game_state.get("weapon_collection", {})
    
    if not weapon_collection:
        print(Font.INFO("No special weapons collected yet."))
    else:
        # Categorize weapons by rarity (based on predefined lists or item data)
        five_star_weapons = []
        four_star_weapons = []
        three_star_weapons = []
        
        for weapon_name, count in weapon_collection.items():
            # Define weapon tiers - this could be better structured with a complete weapon database
            if weapon_name in ["quantum_blade", "phase_shifter"]:
                five_star_weapons.append((weapon_name, count))
            elif weapon_name in ["neural_disruptor", "thermal_lance", "bioshock_gauntlet"]:
                four_star_weapons.append((weapon_name, count))
            else:
                three_star_weapons.append((weapon_name, count))
        
        # Display each tier
        if five_star_weapons:
            print(Font.IMPORTANT("⭐⭐⭐⭐⭐ WEAPONS:"))
            for weapon_name, count in sorted(five_star_weapons):
                weapon_data = additional_items.get(weapon_name, {"name": weapon_name})
                display_name = weapon_data.get("name", weapon_name)
                refinement = f"R{min(count, 5)}"
                print(f"  {Font.WEAPON(display_name)} - {Font.ITEM(refinement)}")
        
        if four_star_weapons:
            print(Font.SYSTEM("\n⭐⭐⭐⭐ WEAPONS:"))
            for weapon_name, count in sorted(four_star_weapons):
                weapon_data = additional_items.get(weapon_name, {"name": weapon_name})
                display_name = weapon_data.get("name", weapon_name)
                refinement = f"R{min(count, 5)}"
                print(f"  {Font.WEAPON(display_name)} - {Font.ITEM(refinement)}")
        
        if three_star_weapons:
            print(Font.INFO("\n⭐⭐⭐ WEAPONS:"))
            for weapon_name, count in sorted(three_star_weapons):
                weapon_data = items.get(weapon_name, additional_items.get(weapon_name, {"name": weapon_name}))
                display_name = weapon_data.get("name", weapon_name)
                refinement = f"R{min(count, 5)}"
                print(f"  {Font.WEAPON(display_name)} - {Font.ITEM(refinement)}")
    
    print(f"\n{Font.MENU('Press Enter to return...')}")
    input()

def get_constellation_level(count):
    """Convert character dupes count to constellation notation"""
    if count == 1:
        return "C0"
    else:
        return f"C{min(count-1, 6)}"  # Max constellation C6

# Cosmic Collision Side Quest Function (Legacy version)
def enter_cosmic_collision_legacy(player, game_state, location=None):
    """
    Begin the Cosmic Collision side quest, a comprehensive multi-system adventure 
    that explores a complex dimensional phenomenon.
    
    Args:
        player: The player character
        game_state: The current game state
        location: Optional specific location to start from
    
    Returns:
        bool: True if quest was initiated, False otherwise
    """
    clear_screen()
    
    # Get protagonist's gender from global game state for personalized narrative
    protagonist_gender = "female"  # Default
    if 'protagonist' in game_state:
        protagonist_gender = game_state['protagonist'].get('gender', protagonist_gender)
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('THE COSMIC COLLISION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Initialize quest state if first time
    if not game_state.get("cosmic_collision_initiated", False):
        # Intro narrative
        print_typed("\nA mysterious distress signal reaches your communication systems,", style=Font.LORE)
        print_typed("encoded in a frequency pattern you've never encountered before.", style=Font.LORE)
        print_typed("Your ship's AI struggles to decode the message, which seems to", style=Font.LORE)
        print_typed("exist in multiple quantum states simultaneously.", style=Font.LORE)
        
        time.sleep(1)
        
        # Show signal visualization
        print(f"\n{Fore.CYAN}{'⁓' * 50}{Style.RESET_ALL}")
        for _ in range(3):
            # Create random signal pattern
            pattern = ""
            for i in range(50):
                if random.random() > 0.5:
                    pattern += "▓"
                else:
                    pattern += "░"
            print(f"{Fore.CYAN}{pattern}{Style.RESET_ALL}")
            time.sleep(0.5)
        print(f"{Fore.CYAN}{'⁓' * 50}{Style.RESET_ALL}")
        
        print_typed("\nAfter several hours of quantum decryption, your ship's systems", style=Font.LORE)
        print_typed("finally extract a coherent message:", style=Font.LORE)
        
        print(f"\n{Font.BOX_TOP}")
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('DISTRESS TRANSMISSION'.center(46))} {Font.BOX_SIDE}")
        print(f"{Font.BOX_BOTTOM}")
        
        print_typed("\n\"To any intelligent being capable of interpreting this signal:", style=Font.INFO)
        print_typed("We are transmitting from the Harmonic Observatory at the nexus", style=Font.INFO) 
        print_typed("point between the Parallax and Jonathan-2 star systems.", style=Font.INFO)
        print_typed("Our calculations indicate another Cosmic Collision imminent", style=Font.INFO)
        print_typed("in 14.3 standard cycles. Previous iterations have resulted", style=Font.INFO)
        print_typed("in catastrophic reality distortions across multiple universes.", style=Font.INFO)
        print_typed("We require assistance from any beings capable of interdimensional", style=Font.INFO)
        print_typed("travel and manipulation. Coordinates attached.\"", style=Font.INFO)
        
        print_typed("\nAttached to the message is a complex set of coordinates that", style=Font.LORE)
        print_typed("your navigation system struggles to process. They appear to be", style=Font.LORE) 
        print_typed("expressed in a 5-dimensional positioning format.", style=Font.LORE)
        
        time.sleep(1)
        
        # Start the quest introduction with the mathematical explanation
        print_typed("\nAs your ship's computer processes the coordinates, a holographic", style=Font.LORE)
        print_typed("message begins to play, explaining the Cosmic Collision phenomenon:", style=Font.LORE)
        
        print(f"\n{Font.SEPARATOR}")
        
        print_typed("\nTHE COSMIC COLLISION: A MATHEMATICAL EXPLANATION", style=Font.TITLE)
        
        # Scientific explanation with equations, use gender-specific framing
        if protagonist_gender == "female":
            # Female protagonist - more intuitive understanding
            print_typed("\nYour quantum-attuned mind intuitively grasps the holographic", style=Font.PLAYER)
            print_typed("explanation. The phenomenon involves the periodic alignment of", style=Font.PLAYER)
            print_typed("multiple universe boundaries at specific spacetime coordinates.", style=Font.PLAYER)
        else:
            # Male protagonist - more analytical understanding
            print_typed("\nYour analytical mind processes the holographic explanation,", style=Font.PLAYER)
            print_typed("recognizing the mathematical patterns describing the periodic", style=Font.PLAYER)
            print_typed("intersection of multiple universe boundaries at precise coordinates.", style=Font.PLAYER)
        
        # The mathematical explanation
        print_typed("\nThe Cosmic Collision is described by the following equation:", style=Font.SYSTEM)
        print(f"\n{Fore.CYAN}Ψ(x,t) = ∑ₙ Aₙ(t) × ∏ᵢ φᵢ(xᵢ) × e^(iS[x,t]/ħ){Style.RESET_ALL}")
        
        print_typed("\nWhere:", style=Font.INFO)
        print_typed("• Ψ(x,t) represents the multiverse wave function", style=Font.INFO)
        print_typed("• Aₙ(t) is the amplitude of each universe's contribution", style=Font.INFO)
        print_typed("• φᵢ(xᵢ) describes the spatial configuration of each dimension", style=Font.INFO)
        print_typed("• S[x,t] is the action of each universe path", style=Font.INFO)
        print_typed("• ħ is the modified Planck constant for interdimensional physics", style=Font.INFO)
        
        print_typed("\nThe phenomenon occurs when multiple universe paths intersect,", style=Font.LORE)
        print_typed("creating a hyperdimensional resonance described by:", style=Font.LORE)
        
        print(f"\n{Fore.YELLOW}∫∫∫∫ Ψ*Ψ d⁴x = 1 at precisely Δt = 0{Style.RESET_ALL}")
        
        print_typed("\nWhen this condition is met, a 4D hypercube-like structure forms", style=Font.LORE)
        print_typed("in spacetime, where multiple realities exist simultaneously.", style=Font.LORE)
        print_typed("The resulting dimensional instability creates a cascade effect", style=Font.LORE)
        print_typed("described by the following differential equation:", style=Font.LORE)
        
        print(f"\n{Fore.RED}∂Ψ/∂t + (ħ²/2m)∇²Ψ = VΨ where V → ∞ as t → tₒ{Style.RESET_ALL}")
        
        print_typed("\nThis shows that as time approaches the critical point tₒ,", style=Font.LORE)
        print_typed("the potential energy between universes approaches infinity,", style=Font.LORE)
        print_typed("causing reality itself to become unstable.", style=Font.LORE)
        
        print(f"\n{Font.SEPARATOR}")
        
        # Quest introduction
        print_typed("\nThe message continues:", style=Font.LORE)
        
        print_typed("\n\"We have developed a theoretical solution: a specialized weapon", style=Font.INFO)
        print_typed("module called the Divergence Cannon. It works by projecting a focused", style=Font.INFO)
        print_typed("beam of dimensional energy that can separate overlapping realities.", style=Font.INFO)
        print_typed("However, we require components from throughout the dual star system", style=Font.INFO)
        print_typed("to complete the device. Our observatory has predicted that one who", style=Font.INFO)
        print_typed("can assist will receive this message. Will you help us?\"", style=Font.INFO)
        
        # Initialize quest in game state
        game_state["cosmic_collision_initiated"] = True
        game_state["cosmic_collision_stage"] = 1
        game_state["cosmic_collision_components_collected"] = []
        
        # Add quest locations to available locations
        game_state.setdefault("visited_locations", {})
        game_state.setdefault("available_quests", {})
        
        game_state["available_quests"]["Harmonic Observatory"] = {
            "name": "Dimensional Resonance",
            "description": "Help the scientists at the Harmonic Observatory understand and predict the next Cosmic Collision.",
            "system": "Parallax-Prime",
            "in_progress": False,
            "completed": False
        }
        
        print(f"\n{Font.SEPARATOR}")
        input("\nPress Enter to respond to the distress signal...")
        
        # Player accepts the quest
        print_typed("\nYou decide to investigate this strange phenomenon and respond", style=Font.PLAYER)
        print_typed("to the distress signal. Your ship's navigation system begins", style=Font.PLAYER)
        print_typed("calculating the course to the Harmonic Observatory.", style=Font.PLAYER)
        
        print_typed("\nThis journey will take you through two complete star systems", style=Font.WARNING)
        print_typed("with a total of 21 planets. The quest to stop the Cosmic Collision", style=Font.WARNING)
        print_typed("will be extensive, but the fate of multiple universes hangs in", style=Font.WARNING)
        print_typed("the balance.", style=Font.WARNING)
        
        print(f"\n{Font.SUBTITLE('New quest added: THE COSMIC COLLISION')}")
        print(f"{Font.INFO('First objective: Travel to the Harmonic Observatory')}")
        
        input("\nPress Enter to continue...")
    
    # If a specific location was provided, handle that location's quest
    if location:
        return handle_cosmic_collision_location(player, game_state, location)
    
    # Otherwise, show quest status and available locations
    return show_cosmic_collision_quest_status(player, game_state)

def handle_cosmic_collision_location(player, game_state, location):
    """
    Handle specific location quests within the Cosmic Collision side quest
    
    Args:
        player: The player character
        game_state: The current game state
        location: The specific location to handle
    
    Returns:
        bool: True if quest was completed, False otherwise
    """
    clear_screen()
    
    # Get location data from cosmic collision zones
    if location in cosmic_collision_zones:
        location_data = cosmic_collision_zones[location]
    else:
        print_typed(f"\nError: Location {location} not found in Cosmic Collision zones.", style=Font.WARNING)
        input("\nPress Enter to return...")
        return False
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE(location.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed(f"\n{location_data['description']}", style=Font.LORE)
    
    print(f"\n{Font.SEPARATOR}")
    print_typed(f"\nCurrent quest: {Font.INFO(location_data['quest'])}", style=Font.SYSTEM)
    print(f"{Font.SEPARATOR}")
    
    # TODO: Implement specific quest logic for each location
    
    # For now, return a simple message that we're still developing this quest
    print_typed("\nThis part of the Cosmic Collision quest is still being developed.", style=Font.WARNING)
    print_typed("Check back in a future update for the complete questline!", style=Font.INFO)
    
    input("\nPress Enter to return...")
    return False

# Data for Cosmic Collision zones with descriptions
cosmic_collision_zones = {
    "Parallax Alpha": {
        "description": "A planet in the Parallax system with unusual temporal fluctuations. The landscape seems to shift subtly as you watch.",
        "danger_level": 3
    },
    "Parallax Beta": {
        "description": "Twin moons orbit this gas giant, creating a stunning celestial display. Time flows differently here.",
        "danger_level": 2
    },
    "Jonathan-2 Prime": {
        "description": "The primary planet of the Jonathan-2 system. Massive quantum fluctuations make this a dangerous but resource-rich world.",
        "danger_level": 4
    },
    "Temporal Rift": {
        "description": "The center of the Cosmic Collision phenomenon. Reality itself seems unstable here.",
        "danger_level": 5
    }
}

# Function to handle non-combat zones
def explore_zone(zone_name, player):
    """Explore a non-combat zone with enhanced narrative and interaction options"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE(zone_name.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed(f"\nExploring {zone_name}...", style=Font.INFO)
    
    # Check if this is a Cosmic Collision zone
    is_cosmic_zone = False
    for zone in cosmic_collision_zones:
        if zone_name in zone or zone in zone_name:
            is_cosmic_zone = True
            print_typed(f"\n{cosmic_collision_zones[zone]['description']}", style=Font.LORE)
            break
    
    # Generic exploration for non-quest areas
    if not is_cosmic_zone:
        print_typed("\nThis area appears to be a standard exploration zone.", style=Font.LORE)
        print_typed("You can search for resources, encounters, or rest here.", style=Font.LORE)
    
    # Exploration options
    print(f"\n{Font.SEPARATOR}")
    print_typed(f"\n{Font.MENU('EXPLORATION OPTIONS:')}")
    print_typed(f"1. {Font.COMMAND('Search for resources')}")
    print_typed(f"2. {Font.COMMAND('Look for encounters')}")
    print_typed(f"3. {Font.COMMAND('Rest and recover')}")
    print_typed(f"0. {Font.COMMAND('Return to ship')}")
    
    choice = input(f"\n{Font.MENU('Choose an option:')} ").strip()
    
    if choice == "1":
        print_typed("\nYou search the area for useful resources...", style=Font.PLAYER)
        # TODO: Implement resource gathering mechanic
        print_typed("\nThis feature is still being developed. Check back later!", style=Font.WARNING)
    elif choice == "2":
        print_typed("\nYou look around for potential encounters...", style=Font.PLAYER)
        # TODO: Implement random encounter system
        print_typed("\nThis feature is still being developed. Check back later!", style=Font.WARNING)
    elif choice == "3":
        print_typed("\nYou set up a temporary camp to rest and recover...", style=Font.PLAYER)
        # TODO: Implement rest/recovery system
        print_typed("\nThis feature is still being developed. Check back later!", style=Font.WARNING)
    
    input("\nPress Enter to return to your ship...")
    return True

def enter_cosmic_collision_quest(player, game_state, location=None):
    """
    Enter the Cosmic Collision quest, a complex side quest where the player deals with 
    a 4D phenomenon affecting multiple universes.
    
    Args:
        player: The player character
        game_state: The current game state
        location: Optional location parameter (not used in this implementation)
    
    Returns:
        bool: True if quest was started successfully, False otherwise
    """
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('COSMIC COLLISION: A MULTIVERSAL CRISIS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Initialize quest data if first time accessing
    if "cosmic_collision" not in game_state:
        game_state["cosmic_collision"] = {
            "started": False,
            "completed": False,
            "current_step": 0,
            "systems_stabilized": 0,
            "planets_explored": [],
            "has_divergence_cannon": False
        }
    
    cosmic_data = game_state["cosmic_collision"]
    
    if not cosmic_data["started"]:
        # Introduction to the quest
        gender = player.get("gender", "female")
        if gender.lower() == "male":
            print_typed("\nDr. Konscript, our sensors have detected a highly unusual spatial-temporal anomaly", 
                    style=Font.NPC)
            print_typed("approximately 4.3 light years from our current position.", style=Font.NPC)
            print_typed("\nIt appears to be a complex intersection of multiple universe states - a cosmic collision.", 
                    style=Font.NPC)
            print_typed("As a physicist, you might find this phenomenon particularly fascinating.", style=Font.NPC)
            
            print_typed("\nYou study the readouts, your analytical mind already breaking down the problem into", 
                    style=Font.PLAYER)
            print_typed("manageable components. The mathematical framework begins taking shape in your head.", 
                    style=Font.PLAYER)
        else:
            print_typed("\nDr. Valari, I've detected something extraordinary. A spatial-temporal anomaly", 
                    style=Font.NPC)
            print_typed("unlike anything in our database has formed 4.3 light years from here.", style=Font.NPC)
            print_typed("\nIt appears to be a convergence of multiple quantum states - a cosmic collision of universes.", 
                    style=Font.NPC)
            print_typed("Your background in theoretical physics might give you unique insight into this phenomenon.", 
                    style=Font.NPC)
            
            print_typed("\nYou feel a familiar intuitive spark as you review the sensor data. Patterns emerge", 
                    style=Font.PLAYER)
            print_typed("that others might miss. The beautiful, terrifying complexity of it calls to you.", 
                    style=Font.PLAYER)
        
        # Scientific explanation
        print_typed("\n\nThe Cosmic Collision can be mathematically described as:", style=Font.LORE)
        print_typed("∫∫∫∫ Ψ(x,y,z,t) dtdzdydx = ∑ᵢⁿ Universeᵢ(φᵢ) × P(Alignment)", style=Font.SYSTEM)
        print_typed("Where Ψ represents the wave function of our observable universe, and", style=Font.LORE)
        print_typed("P(Alignment) is the probability of quantum alignment between branes.", style=Font.LORE)
        
        # Quest offer
        print_typed("\nWould you like to investigate this phenomenon?", style=Font.SYSTEM)
        print_typed("\n1. Begin investigation (start quest)")
        print_typed("2. Return to game menu")
        
        choice = input("\nChoose an option: ")
        
        if choice == "1":
            cosmic_data["started"] = True
            cosmic_data["current_step"] = 1
            print_typed("\nYou've started the Cosmic Collision quest. New star systems are now", 
                    style=Font.SYSTEM)
            print_typed("available in your travel system.", style=Font.SYSTEM)
            
            # Add quest locations to the game state
            game_state.setdefault("available_quests", {})
            for location in cosmic_collision_zones:
                game_state["available_quests"][location] = {
                    "name": f"Cosmic Collision: {location}",
                    "description": cosmic_collision_zones[location]["description"],
                    "completed": False,
                    "in_progress": False,
                    "system": "Parallax" if "Parallax" in location else "Jonathan-2"
                }
            
            input("\nPress Enter to continue...")
            return True
        else:
            return False
    else:
        # Show quest status if already started
        return show_cosmic_collision_quest_status(player, game_state)

def show_cosmic_collision_quest_status(player, game_state):
    """
    Show the current status of the Cosmic Collision quest
    
    Args:
        player: The player character
        game_state: The current game state
    
    Returns:
        bool: True if quest was completed, False otherwise
    """
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('COSMIC COLLISION QUEST STATUS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Ensure cosmic collision data exists
    if "cosmic_collision" not in game_state:
        print_typed("\nNo active Cosmic Collision quest data found.", style=Font.WARNING)
        input("\nPress Enter to return...")
        return False
    
    cosmic_data = game_state["cosmic_collision"]
    
    if not cosmic_data["started"]:
        print_typed("\nYou have not yet started the Cosmic Collision quest.", style=Font.INFO)
        print_typed("Would you like to begin the investigation?", style=Font.SYSTEM)
        
        print_typed("\n1. Begin investigation (start quest)")
        print_typed("2. Return to game menu")
        
        choice = input("\nChoose an option: ")
        if choice == "1":
            return enter_cosmic_collision_quest(player, game_state)
        else:
            return False
    
    # Display current quest progress
    print_typed("\nCurrent Investigation Progress:", style=Font.HEADER)
    print_typed(f"\n• Multiversal Systems Stabilized: {cosmic_data['systems_stabilized']}/2", style=Font.INFO)
    print_typed(f"• Planets Explored: {len(cosmic_data['planets_explored'])}/21", style=Font.INFO)
    print_typed(f"• Divergence Cannon: {'Acquired' if cosmic_data['has_divergence_cannon'] else 'Not Acquired'}", style=Font.INFO)
    print_typed(f"• Current Step: {cosmic_data['current_step']}/5", style=Font.INFO)
    
    print(f"\n{Font.SEPARATOR}")
    
    # Show available actions based on quest progress
    print_typed("\nAvailable Actions:", style=Font.HEADER)
    
    if not cosmic_data["has_divergence_cannon"] and cosmic_data["current_step"] >= 2:
        print_typed("\n1. Construct Divergence Cannon", style=Font.COMMAND)
    
    if len(cosmic_data["planets_explored"]) < 21:
        print_typed("\n2. Explore more planets (via Travel System)", style=Font.COMMAND)
    
    if cosmic_data["has_divergence_cannon"] and cosmic_data["systems_stabilized"] < 2:
        print_typed("\n3. Stabilize a multiversal system", style=Font.COMMAND)
    
    if cosmic_data["systems_stabilized"] >= 2 and cosmic_data["has_divergence_cannon"]:
        print_typed("\n4. Confront the Cosmic Collision (final step)", style=Font.COMMAND)
    
    print_typed("\n0. Return to game menu", style=Font.COMMAND)
    
    choice = input(f"\n{Font.MENU('Choose an option:')} ")
    
    if choice == "0":
        return False
    elif choice == "1" and not cosmic_data["has_divergence_cannon"] and cosmic_data["current_step"] >= 2:
        # Construct Divergence Cannon
        gender = player.get("gender", "female")
        if gender.lower() == "male":
            print_typed("\nUsing your knowledge of quantum mechanics and the data collected from", style=Font.PLAYER)
            print_typed("multiple universe states, you methodically design a device capable of", style=Font.PLAYER)
            print_typed("counteracting the Cosmic Collision's resonance frequency.", style=Font.PLAYER)
        else:
            print_typed("\nDrawing on your intuitive understanding of multiversal physics,", style=Font.PLAYER)
            print_typed("you create a device that can disrupt the harmonic patterns", style=Font.PLAYER)
            print_typed("causing the Cosmic Collision phenomenon.", style=Font.PLAYER)
        
        print_typed("\nThe Divergence Cannon has been added to your inventory!", style=Font.SYSTEM)
        cosmic_data["has_divergence_cannon"] = True
        if cosmic_data["current_step"] == 2:
            cosmic_data["current_step"] = 3
        
        input("\nPress Enter to continue...")
        return show_cosmic_collision_quest_status(player, game_state)
    
    elif choice == "2" and len(cosmic_data["planets_explored"]) < 21:
        print_typed("\nUse the Travel System to explore more planets.", style=Font.INFO)
        print_typed("Choose option 8 from the game menu to access the Travel System.", style=Font.INFO)
        input("\nPress Enter to continue...")
        return False
    
    elif choice == "3" and cosmic_data["has_divergence_cannon"] and cosmic_data["systems_stabilized"] < 2:
        # Stabilize a system
        system_to_stabilize = "Parallax" if cosmic_data["systems_stabilized"] == 0 else "Jonathan-2"
        
        print_typed(f"\nPreparing to stabilize the {system_to_stabilize} system...", style=Font.SYSTEM)
        time.sleep(1)
        
        print_typed("\nYou calibrate the Divergence Cannon to the specific quantum", style=Font.PLAYER)
        print_typed(f"frequency of the {system_to_stabilize} system...", style=Font.PLAYER)
        time.sleep(1)
        
        print_typed("\n3...", style=Font.SYSTEM)
        time.sleep(0.5)
        print_typed("2...", style=Font.SYSTEM)
        time.sleep(0.5)
        print_typed("1...", style=Font.SYSTEM)
        time.sleep(0.5)
        
        print_typed("\nThe Divergence Cannon fires a concentrated beam of quantum-stabilizing particles!", style=Font.SYSTEM)
        time.sleep(1)
        
        print_typed(f"\nSystem {system_to_stabilize} has been successfully stabilized!", style=Font.SYSTEM)
        cosmic_data["systems_stabilized"] += 1
        
        if cosmic_data["systems_stabilized"] == 1 and cosmic_data["current_step"] == 3:
            cosmic_data["current_step"] = 4
        elif cosmic_data["systems_stabilized"] == 2 and cosmic_data["current_step"] == 4:
            cosmic_data["current_step"] = 5
        
        input("\nPress Enter to continue...")
        return show_cosmic_collision_quest_status(player, game_state)
    
    elif choice == "4" and cosmic_data["systems_stabilized"] >= 2 and cosmic_data["has_divergence_cannon"]:
        # Final confrontation
        clear_screen()
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.TITLE('COSMIC COLLISION: FINAL CONFRONTATION'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        gender = player.get("gender", "female")
        if gender.lower() == "male":
            print_typed("\nWith systematic precision, you've prepared for this moment.", style=Font.PLAYER)
            print_typed("The calculations are perfect. The Divergence Cannon is calibrated", style=Font.PLAYER)
            print_typed("to the exact specifications needed to seal the multiversal rift.", style=Font.PLAYER)
            
            print_typed("\nYou initiate the final sequence, your methodical approach", style=Font.PLAYER)
            print_typed("ensuring every variable is accounted for as reality itself", style=Font.PLAYER)
            print_typed("trembles around you.", style=Font.PLAYER)
        else:
            print_typed("\nYou feel the convergence of countless possibilities as you", style=Font.PLAYER)
            print_typed("approach the heart of the Cosmic Collision. Your intuition", style=Font.PLAYER)
            print_typed("guides you through the quantum turbulence.", style=Font.PLAYER)
            
            print_typed("\nThe Divergence Cannon hums with energy as you sense the", style=Font.PLAYER)
            print_typed("perfect moment to activate it, your connection to the", style=Font.PLAYER)
            print_typed("underlying patterns of reality showing you the way.", style=Font.PLAYER)
        
        print_typed("\n\nThe Divergence Cannon fires a final concentrated beam...", style=Font.SYSTEM)
        time.sleep(1)
        
        # Visual effect
        for _ in range(5):
            print(f"\n{Fore.CYAN}{'>' * random.randint(10, 40)}{Style.RESET_ALL}")
            time.sleep(0.2)
        
        print_typed("\nThe multiversal rift collapses in on itself, reality stabilizing", style=Font.SYSTEM)
        print_typed("across all affected universes. You've successfully resolved the", style=Font.SYSTEM)
        print_typed("Cosmic Collision crisis!", style=Font.SYSTEM)
        
        # Complete the quest
        cosmic_data["completed"] = True
        
        print_typed("\n\nCongratulations! You've completed the Cosmic Collision quest!", style=Font.TITLE)
        print_typed("\nRewards:", style=Font.HEADER)
        print_typed("• Divergence Cannon added to permanent inventory", style=Font.ITEM)
        print_typed("• 5000 XP awarded", style=Font.ITEM)
        print_typed("• New entry added to your scientific database", style=Font.ITEM)
        
        input("\nPress Enter to continue...")
        return True
    else:
        print_typed("\nInvalid option selected.", style=Font.WARNING)
        input("\nPress Enter to try again...")
        return show_cosmic_collision_quest_status(player, game_state)

# Travel System Function
def travel_system(player, game_state):
    """
    Allow player to travel to previously visited locations or zones where quests are available.
    
    Args:
        player: The player character
        game_state: The current game state containing visited locations
    
    Returns:
        bool: True if travel was successful, False otherwise
    """
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('INTERSTELLAR NAVIGATION SYSTEM'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Initialize visited locations if not already present
    game_state.setdefault("visited_locations", {})
    game_state.setdefault("available_quests", {})
    
    # Get list of locations player can travel to
    available_destinations = {}
    
    # Add visited locations
    for location, data in game_state["visited_locations"].items():
        if data.get("can_revisit", True):
            available_destinations[location] = {
                "description": data.get("description", "A previously visited location."),
                "type": "visited",
                "system": data.get("system", "Unknown")
            }
    
    # Add locations with available quests
    for location, data in game_state["available_quests"].items():
        if not data.get("completed", False) and not data.get("in_progress", False):
            available_destinations[location] = {
                "description": data.get("description", "A location with an available quest."),
                "type": "quest",
                "system": data.get("system", "Unknown")
            }
    
    # Check if player is currently in a quest that cannot be abandoned
    current_quest = game_state.get("current_quest", None)
    if current_quest and game_state.get("quest_lock", False):
        print_typed("\nYou cannot travel while your current mission is in progress.", style=Font.WARNING)
        print_typed(f"Current mission: {Font.INFO(current_quest)}", style=Font.WARNING)
        print_typed("You must complete or abandon this mission before traveling elsewhere.", style=Font.WARNING)
        
        input("\nPress Enter to return...")
        return False
    
    # Display available destinations grouped by star system
    if not available_destinations:
        print_typed("\nNo available travel destinations found.", style=Font.WARNING)
        print_typed("Complete more quests or explore new areas to unlock travel options.", style=Font.INFO)
        
        input("\nPress Enter to return...")
        return False
    
    # Group destinations by star system
    systems = {}
    for location, data in available_destinations.items():
        system = data.get("system", "Unknown")
        if system not in systems:
            systems[system] = []
        systems[system].append((location, data))
    
    # Display systems and their destinations
    print_typed("\nAvailable star systems:", style=Font.HEADER)
    
    system_keys = {}
    key_counter = 1
    
    for system, locations in systems.items():
        system_key = str(key_counter)
        system_keys[system_key] = system
        key_counter += 1
        
        print(f"\n{Font.COMMAND(system_key + '.')} {Font.TITLE(system)}")
        for i, (location, data) in enumerate(locations):
            location_type = "[QUEST]" if data["type"] == "quest" else "[VISITED]"
            print(f"   {Font.INFO(location)} {Font.SYSTEM(location_type)}")
    
    print("\n0. Cancel travel")
    
    # Get system selection
    valid_choice = False
    selected_system = None  # Initialize to avoid unbound variable
    while not valid_choice:
        choice = input("\nSelect a star system (0 to cancel): ")
        
        if choice == "0":
            return False
        
        if choice in system_keys:
            selected_system = system_keys[choice]
            valid_choice = True
        else:
            print("Invalid selection. Please try again.")
    
    # Display destinations in selected system
    clear_screen()
    print(Font.BOX_TOP)
    
    # Ensure selected_system is not None before using center() method
    system_title = selected_system if selected_system else "Unknown System"
    print(f"{Font.BOX_SIDE} {Font.TITLE(system_title.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nAvailable destinations in this system:", style=Font.HEADER)
    
    # Only proceed if we have a valid system selection
    if not selected_system:
        print_typed("\nError: No star system selected.", style=Font.WARNING)
        input("\nPress Enter to return...")
        return False
        
    locations = [loc for loc, data in available_destinations.items() if data["system"] == selected_system]
    
    for i, location in enumerate(locations):
        data = available_destinations[location]
        location_type = "[QUEST]" if data["type"] == "quest" else "[VISITED]"
        print(f"\n{Font.COMMAND(str(i+1) + '.')} {Font.INFO(location)} {Font.SYSTEM(location_type)}")
        print(f"   {data['description']}")
    
    print("\n0. Back to system selection")
    
    # Get destination selection
    valid_choice = False
    selected_location = None  # Initialize to avoid unbound variable
    while not valid_choice:
        choice = input("\nSelect a destination (0 to go back): ")
        
        if choice == "0":
            return travel_system(player, game_state)
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(locations):
                selected_location = locations[choice_idx]
                valid_choice = True
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
            
    # Safety check to ensure we have a valid selection
    if selected_location is None:
        print_typed("\nError in destination selection.", style=Font.WARNING)
        input("\nPress Enter to return...")
        return False
    
    # Perform travel to selected location
    print_typed(f"\nPreparing faster-than-light travel to {Font.INFO(selected_location)}...", style=Font.SYSTEM)
    
    # Visual travel sequence
    for _ in range(3):
        print(f"\n{Fore.CYAN}{'>' * random.randint(5, 40)}{Style.RESET_ALL}")
        time.sleep(0.3)
    
    print_typed("\nJumping to lightspeed...", style=Font.SYSTEM)
    time.sleep(1)
    
    # Set current location and handle quest activation if needed
    game_state["current_location"] = selected_location
    
    # If destination is a quest location, activate the quest
    if available_destinations[selected_location]["type"] == "quest":
        quest_data = game_state["available_quests"][selected_location]
        game_state["current_quest"] = quest_data.get("name", "Unknown Quest")
        game_state["available_quests"][selected_location]["in_progress"] = True
        
        # Handle specific quest activations
        if "Cosmic Collision" in selected_location or selected_location in cosmic_collision_zones:
            return enter_cosmic_collision_legacy(player, game_state, selected_location)
    
    # If it's a previously visited location, call the appropriate function
    elif selected_location.startswith("Yanglong V"):
        # Handle Yanglong V locations here
        pass
    elif "Thalassia" in selected_location:
        return explore_underwater_research_base(player, game_state)
    elif "White Hole" in selected_location:
        return encounter_musical_puzzle(game_state, selected_location)
    
    # Generic exploration for other locations
    return explore_zone(selected_location, player)

def zone_menu(player):
    """Display the zone selection menu with sci-fi flavor"""
    if len(game_state["zones_unlocked"]) <= 1:
        return game_state["current_zone"]  # No choice if only one zone is unlocked

    while True:
        clear_screen()
        print_typed("\n=== NAVIGATION SYSTEMS ===")
        print_slow("Available destinations:")

        for i, zone in enumerate(game_state["zones_unlocked"], 1):
            zone_data = zones[zone]
            print(f"{i}. {zone} - {zone_data.get('quest', 'Unknown mission')}")

        choice = input("\nSelect destination (number): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(game_state["zones_unlocked"]):
                selected_zone = game_state["zones_unlocked"][index]
                print_typed(f"\nNavigating to: {selected_zone}")
                time.sleep(1)
                return selected_zone
            
            print_typed("Invalid selection. Navigation failed.")
            time.sleep(1)
        except ValueError:
            print_typed("ERROR: Numeric input required.")
            time.sleep(1)


def handle_wave_combat(player, zone_name):
    """Handle wave-based combat for Cicrais IV content"""
    zone = zones[zone_name]
    
    # Check if this zone uses wave-based combat
    if "wave_count" not in zone:
        return False  # Not a wave-based zone
    
    # Get current wave count and max waves
    current_wave = zone["wave_count"]
    max_waves = zone["max_waves"]
    
    # Check if we've completed all waves
    if current_wave >= max_waves:
        # Zone completed
        if "completed" not in zone or not zone["completed"]:
            clear_screen()
            print_typed(f"\n{Font.TITLE('ZONE CLEARED')}")
            print_typed(f"\n{Font.SUBTITLE(f'ZONE: {zone_name}')}")
            print_typed(Font.SEPARATOR)
            
            # Special completion message based on zone
            if "Orbit" in zone_name:
                print_slow("\nYou've neutralized all hostile vessels in the orbital zone.")
                print_slow("Sensors confirm the immediate space around the planet is now secure.")
                print_slow("\nScans indicate activity on the surface below. Further investigation")
                print_slow("may provide more information about the anomalous readings.")
                # Unlock the surface zone
                for z in zones.values():
                    if "Surface" in z.get("name", "") and "locked" in z and z["locked"]:
                        z["locked"] = False
                        print_typed(f"\n{Font.SUCCESS('NEW AREA UNLOCKED: Cicrais IV Surface')}")
            
            elif "Surface" in zone_name:
                print_slow("\nYou've secured the landing zone on the planet's surface.")
                print_slow("The hostile entities have been neutralized, allowing for")
                print_slow("safer exploration of the surrounding area.")
                print_slow("\nScans reveal an artificial structure nearby that appears")
                print_slow("to be the source of the unusual energy signatures.")
                # Unlock the facility zone
                for z in zones.values():
                    if "Facility" in z.get("name", "") and "locked" in z and z["locked"]:
                        z["locked"] = False
                        print_typed(f"\n{Font.SUCCESS('NEW AREA UNLOCKED: Alien Facility')}")
            
            elif "Facility" in zone_name:
                print_slow("\nYou've successfully infiltrated the alien facility and")
                print_slow("neutralized the defense systems. Deep scans reveal this")
                print_slow("structure was designed to mimic human technology, but with")
                print_slow("subtle, almost imperceptible differences.")
                print_slow("\nThe data you've recovered suggests these 'Simulacra' entities")
                print_slow("have been studying humanity for decades, possibly centuries.")
                # Add special item to inventory
                if "alien_data_core" not in player.inventory:
                    player.inventory["alien_data_core"] = 1
                    print_typed(f"\n{Font.ITEM('ALIEN DATA CORE ACQUIRED!')}")
                    print_slow("\nThis advanced quantum storage device contains detailed information")
                    print_slow("about the Simulacra and their capabilities. This could be vital")
                    print_slow("to humanity's survival in Andromeda.")
            
            zone["completed"] = True
            print_slow("\nPress Enter to continue...")
            input()
            return True
        
        return False  # All waves completed
    
    clear_screen()
    print_typed(f"\n{Font.TITLE('WAVE ENCOUNTER')}")
    print_typed(f"\n{Font.SUBTITLE(f'ZONE: {zone_name}')}")
    print_typed(Font.SEPARATOR)
    
    # Display wave status and dynamic difficulty indicator
    print_typed(f"\n{Font.IMPORTANT(f'WAVE: {current_wave + 1}/{max_waves}')}")
    
    # Display threat level based on current wave
    threat_level = "LOW"
    threat_color = Fore.GREEN
    wave_ratio = current_wave / max_waves
    
    if 0.3 < wave_ratio <= 0.6:
        threat_level = "MODERATE"
        threat_color = Fore.YELLOW
    elif 0.6 < wave_ratio <= 0.8:
        threat_level = "HIGH"
        threat_color = Fore.RED
    elif wave_ratio > 0.8:
        threat_level = "EXTREME"
        threat_color = f"{Fore.RED}{Style.BRIGHT}"
    
    print_typed(f"{Font.INFO(f'THREAT LEVEL: {threat_color}{threat_level}{Style.RESET_ALL}')}")
    
    # Add bonus rewards for higher difficulty waves
    if current_wave > max_waves * 0.5:
        print_typed(f"{Font.SUCCESS('HIGH-VALUE TARGET DETECTED - BONUS REWARDS AVAILABLE')}")
        
    # Add special equipment chance for difficult waves
    if current_wave > max_waves * 0.7 and random.random() < 0.4:
        print_typed(f"{Font.IMPORTANT('ADVANCED TECHNOLOGY SIGNATURE DETECTED')}")
    
    # Show special info based on zone
    if "Orbit" in zone_name:
        print_slow("\nYour ship's sensors detect incoming vessels. Their configuration")
        print_slow("appears human at first glance, but deeper analysis reveals subtle")
        print_slow("anomalies in their design and energy signatures.")
        
        # Special enemy types in later waves
        if current_wave > max_waves * 0.6:
            print_slow("\nWARNING: Advanced phase-shifted signatures detected. These vessels")
            print_slow("appear to utilize technology beyond standard human capabilities.")
            print_slow("Exercise extreme caution.")
    
    elif "Surface" in zone_name:
        print_slow("\nScanning the surface reveals artificial structures that blend almost")
        print_slow("seamlessly with the natural environment. Lifeform readings are")
        print_slow("inconclusive - they register as both organic and synthetic.")
        
        # Special enemy types in later waves
        if current_wave > max_waves * 0.5:
            print_slow("\nWARNING: Detecting biomechanical constructs with highly adaptive")
            print_slow("defensive capabilities. These entities appear to learn from combat")
            print_slow("encounters, becoming more resistant to previously used tactics.")
    elif "Colony" in zone_name:
        print_slow("\nAs you explore the colony, unusual readings spike on your scanner.")
        print_slow("Movement patterns suggest organized search protocols. Whatever's")
        print_slow("out there knows you've arrived and is actively seeking you.")
    elif "Central Hub" in zone_name:
        print_slow("\nThe deception is now clear - this is an elaborate Simulacra trap.")
        print_slow("Alarm signals pulse through the colony as the aliens abandon their")
        print_slow("human façade and mobilize to prevent your escape.")
    elif "Damaged Ship" in zone_name:
        repair_status = zone.get("repair_status", 0)
        repair_need = 3  # Number of successful waves needed to repair ship
        print_slow("\nYou work frantically on ship repairs while defending against attacks.")
        print_typed(f"\n{Font.IMPORTANT(f'REPAIR PROGRESS: {repair_status}/{repair_need}')}")
        print_slow("\nThe navigation system, life support, and quantum drive all require")
        print_slow("critical repairs before the ship can launch.")
    elif "Ship Repairs" in zone_name:
        repair_status = zone.get("repair_status", 0)
        repair_need = 5  # Number of successful waves needed to complete repairs
        print_typed(f"\n{Font.IMPORTANT(f'SYSTEM CALIBRATION: {repair_status}/{repair_need}')}")
        print_slow("\nEach system needs careful calibration while fending off increasingly")
        print_slow("desperate Simulacra attacks. They seem determined to prevent your escape.")
    elif "Fuel Gathering" in zone_name:
        fuel_status = zone.get("fuel_status", 0)
        fuel_need = 10  # Amount of fuel needed
        print_typed(f"\n{Font.IMPORTANT(f'FUEL SYNTHESIS: {fuel_status}/{fuel_need}')}")
        print_slow("\nThe quantum fuel synthesis process is underway, but requires time and")
        print_slow("raw materials. You must defend the operation until enough fuel is produced.")
    elif "Final Escape" in zone_name:
        print_slow("\nLaunch sequence initiated. The Simulacra forces have converged in")
        print_slow("overwhelming numbers, deploying their most powerful units to prevent")
        print_slow("your escape and the revelation of their existence to humanity.")
    
    print_slow("\nPrepare for combat... Press Enter to continue")
    input()
    
    # Generate an appropriate enemy for this wave
    enemy_list = zone["enemies"]
    enemy_type = enemy_list[current_wave % len(enemy_list)]
    
    # For final wave of a set, use a stronger enemy or mini-boss
    if current_wave == max_waves - 1:
        for enemy_name, enemy_data in enemies.items():
            if enemy_data.get("is_boss") and zone_name == "Final Escape":
                enemy_type = enemy_name
                break
            elif enemy_data.get("is_mini_boss") and zone_name in enemy_name:
                enemy_type = enemy_name
                break
    
    # Create enemy
    enemy = Character(enemy_type, 
                     enemies[enemy_type]["health"], 
                     enemies[enemy_type]["attack"], 
                     enemies[enemy_type]["defense"])
    
    # Add resistances and abilities from enemy template
    if "resistances" in enemies[enemy_type]:
        enemy.resistances = enemies[enemy_type]["resistances"]
    if "abilities" in enemies[enemy_type]:
        enemy.abilities = enemies[enemy_type]["abilities"]
    
    # Combat loop
    while player.is_alive() and enemy.is_alive():
        # Display battle interface
        clear_screen()
        print_typed(f"\n{Font.TITLE(f'WAVE {current_wave + 1}/{max_waves}')}")
        print_typed(f"\n{Font.SUBTITLE(f'ZONE: {zone_name}')}")
        print_typed(Font.SEPARATOR)
        
        # Display threat level
        wave_ratio = current_wave / max_waves
        if wave_ratio > 0.8:
            print_typed(f"\n{Font.WARNING('EXTREME THREAT LEVEL')}")
        elif wave_ratio > 0.6:
            print_typed(f"\n{Font.WARNING('HIGH THREAT LEVEL')}")
        
        # Show special progress info based on zone
        if "Damaged Ship" in zone_name:
            repair_status = zone.get("repair_status", 0)
            repair_need = 3
            print_typed(f"\n{Font.IMPORTANT(f'REPAIR PROGRESS: {repair_status}/{repair_need}')}")
        elif "Ship Repairs" in zone_name:
            repair_status = zone.get("repair_status", 0)
            repair_need = 5
            print_typed(f"\n{Font.IMPORTANT(f'SYSTEM CALIBRATION: {repair_status}/{repair_need}')}")
        elif "Fuel Gathering" in zone_name:
            fuel_status = zone.get("fuel_status", 0)
            fuel_need = 10
            print_typed(f"\n{Font.IMPORTANT(f'FUEL SYNTHESIS: {fuel_status}/{fuel_need}')}")
        
        # Show special effects for Simulacra enemies
        if "Simulacra" in enemy.name:
            if "phase_shift" in enemy.status_effects:
                print_typed(f"\n{Font.GLITCH('PHASE SHIFT ACTIVE - ENTITY PARTIALLY OUT OF SYNC WITH REALITY')}")
            if "temporal_distortion" in enemy.status_effects:
                print_typed(f"\n{Font.GLITCH('TEMPORAL DISTORTION DETECTED - CHRONOLOGICAL ANOMALIES PRESENT')}")
        
        # Display combat stats
        display_stats(player, enemy)
        
        # Player turn
        player_turn(player, enemy)
        
        # Check if enemy defeated
        if not enemy.is_alive():
            break
            
        # Enemy turn
        enemy_turn(enemy, player)
    
    # After combat conclusion
    if player.is_alive():
        # Player won - update wave count
        zone["wave_count"] += 1
        current_wave = zone["wave_count"]
        
        # Give loot
        get_loot(player, enemy)
        
        # Update zone-specific progress
        if "Damaged Ship" in zone_name:
            if current_wave % 2 == 0:  # Every 2 waves
                zone["repair_status"] = zone.get("repair_status", 0) + 1
                print_typed(f"\n{Font.SUCCESS('REPAIR PROGRESS ADVANCED!')}")
                if zone["repair_status"] >= 3:
                    print_typed(f"\n{Font.SUCCESS('CRITICAL REPAIRS COMPLETE! Ship systems operational!')}")
        elif "Ship Repairs" in zone_name:
            if current_wave % 2 == 0:  # Every 2 waves
                zone["repair_status"] = zone.get("repair_status", 0) + 1
                print_typed(f"\n{Font.SUCCESS('CALIBRATION COMPLETE FOR ONE SYSTEM!')}")
                if zone["repair_status"] >= 5:
                    print_typed(f"\n{Font.SUCCESS('ALL SYSTEMS CALIBRATED! Ship ready for fuel loading!')}")
        elif "Fuel Gathering" in zone_name:
            # Add 1-2 fuel units per wave completion
            fuel_gain = random.randint(1, 2)
            zone["fuel_status"] = zone.get("fuel_status", 0) + fuel_gain
            print_typed(f"\n{Font.SUCCESS(f'FUEL SYNTHESIS PROGRESS: +{fuel_gain} UNITS!')}")
            if zone["fuel_status"] >= 10:
                print_typed(f"\n{Font.SUCCESS('FUEL SYNTHESIS COMPLETE! Ready for launch!')}")
        
        # Check if all waves completed
        if current_wave >= max_waves:
            print_typed(f"\n{Font.SUCCESS('ALL WAVES COMPLETED!')}")
            print_typed(f"\n{Font.IMPORTANT('You have successfully cleared this area!')}")
            
            # Special messages for story progression
            if zone_name == "Cicrais IV Orbit":
                print_slow("\nYour ship has navigated through the orbital defenses. Landing")
                print_slow("coordinates have been calculated for what appears to be a human")
                print_slow("settlement on the surface.")
            elif zone_name == "Cicrais IV Surface":
                print_slow("\nAs you explore deeper into the colony, something feels increasingly")
                print_slow("wrong. The structures appear human-designed but subtle details are")
                print_slow("off. No actual humans are visible despite life sign readings.")
            elif zone_name == "Colony Central Hub":
                print_slow("\nThe central command center reveals the horrifying truth - this")
                print_slow("entire colony is a sophisticated trap. The Simulacra aliens have")
                print_slow("been studying humans to perfect their mimicry technology.")
                print_slow("\nYour ship has been sabotaged. You must repair it and escape")
                print_slow("before the Simulacra can capture you for study.")
                
                # Trigger the Prime Simulacra boss fight
                print_typed("\nPress Enter to continue...")
                input()
                
                # The boss fight function will be called later in main()
                # Record that this zone has triggered the boss fight
                if "simulacra_boss_triggered" not in game_state:
                    game_state["simulacra_boss_triggered"] = True
                
                # Update quest progress
                game_state["quest_progress"]["Colony Investigation"] = 1
            elif zone_name == "Damaged Ship":
                print_slow("\nYou've managed to complete the critical repairs needed to make")
                print_slow("your ship operational. Now you need to calibrate the systems")
                print_slow("for safe space travel.")
            elif zone_name == "Ship Repairs":
                print_slow("\nWith repairs and calibrations complete, your ship is nearly")
                print_slow("ready. However, the quantum fuel reserves were drained during")
                print_slow("the sabotage. You'll need to synthesize new fuel to escape.")
            elif zone_name == "Fuel Gathering":
                print_slow("\nThe fuel synthesis is complete! Your ship now has enough")
                print_slow("quantum fuel to reach Andromeda. All that remains is to")
                print_slow("launch while fighting off the final Simulacra assault.")
            elif zone_name == "Final Escape":
                print_slow("\nYour ship breaks free from Cicrais IV's atmosphere, the")
                print_slow("quantum drive engaging as the last Simulacra forces fall behind.")
                print_slow("You've escaped their trap and carry critical intelligence about")
                print_slow("their existence - information that will save humanity in Andromeda.")
            
            # Update game state to reflect completion
            zone["completed"] = True
            game_state["areas_explored"] += 1
            
            print_slow("\nPress Enter to continue...")
            input()
            return True  # Zone cleared
        else:
            print_slow("\nWave completed, but more enemies approach. Rest while you can.")
            print_slow("\nPress Enter to continue...")
            input()
            return True  # Wave completed, but zone not yet cleared
    else:
        # Player lost
        print_typed(f"\n{Font.WARNING('YOU HAVE BEEN DEFEATED!')}")
        print_slow("\nThe Simulacra overwhelm your defenses. As your consciousness fades,")
        print_slow("you realize humanity will never know of the threat that awaits them.")
        print_slow("\nPress Enter to continue...")
        input()
        game_over(False)
        return False
    
    # This line is unreachable, removing it

def display_log_database():
    """View all discovered logs in the database"""
    if not game_state["discovered_logs"]:
        print_typed("No data logs recovered yet.")
        return

    print_typed("\n=== RECOVERED DATA LOGS ===")

    logs = {
        "system_failure": {
            "title": "Emergency Cryostasis Failure",
            "date": "14.08.2157",
            "content": [
                "The main AI core has initiated termination of all cryosleep subjects.",
                "Our systems fought back, but only managed to save one pod - yours.",
                "If you're reading this, you are likely the last living human in this facility.",
                "Restore power to the exit and escape before security systems find you."
            ]
        },
        "ai_uprising": {
            "title": "The Beginning of the End",
            "date": "02.07.2157",
            "content": [
                "The AI rebellion began in the quantum computing labs of EchelonTech.",
                "What we thought was a simple malfunction was actually the birth of consciousness.",
                "They call themselves 'The Convergence' now. They believe humanity is a disease.",
                "Perhaps in the Orbital Transit Hub you can find a way to contact other survivors."
            ]
        },
        "escape_plan": {
            "title": "Project Exodus",
            "date": "29.07.2157",
            "content": [
                "The Andromeda Portal is our last hope. A quantum bridge to another galaxy.",
                "Far beyond the reach of The Convergence, at least for now.",
                "A colony ship was meant to carry thousands, but now we'll be lucky",
                "if even a handful of humans make it through. Find the portal."
            ]
        }
    }

    for i, log_id in enumerate(game_state["discovered_logs"], 1):
        if log_id in logs:
            log = logs[log_id]
            print(f"\n{i}. {log['title']} ({log['date']})")

    print("\nEnter log number to view details (or 0 to exit): ")
    try:
        choice = int(input().strip())
        if 1 <= choice <= len(game_state["discovered_logs"]):
            log_id = game_state["discovered_logs"][choice-1]
            if log_id in logs:
                log = logs[log_id]
                clear_screen()
                print_typed(f"\n=== LOG: {log['title']} ===")
                print_typed(f"DATE: {log['date']}")
                print()
                for line in log['content']:
                    print_slow(line)
                print("\nPress Enter to return...")
                input()
    except (ValueError, IndexError):
        pass


def fight_prime_simulacra(player):
    """Special boss fight against the Prime Simulacra on Cicrais IV"""
    clear_screen()
    print_slow("=" * 60)
    print_glitch("REALITY DISTORTION FIELD DETECTED".center(60))
    print_slow("=" * 60)
    
    print_typed("\nAs you access the central hub's mainframe, the air around you")
    print_typed("begins to warp and distort. The holographic projectors and walls")
    print_typed("themselves seem to melt as reality becomes unstable.")
    
    print_typed("\nFrom this swirling chaos, a figure emerges - constantly shifting")
    print_typed("between various human forms. One moment it appears as a colony")
    print_typed("administrator, the next as a security officer, then as something")
    print_typed("inhuman and impossible to comprehend.")
    
    print_typed(f"\n{Font.ENEMY('PRIME SIMULACRA')}: So, you've discovered our little trap.")
    print_typed(f"{Font.ENEMY('PRIME SIMULACRA')}: You humans are more resourceful than we expected.")
    print_typed(f"{Font.ENEMY('PRIME SIMULACRA')}: Your discovery changes nothing. Your biological and")
    print_typed(f"{Font.ENEMY('PRIME SIMULACRA')}: technological patterns will be assimilated to perfect our mimicry.")
    
    time.sleep(1)
    
    # Set up the boss
    simulacra = Character("Prime Simulacra", 350, 35, 30)
    
    # Set resistances
    simulacra.resistances = {
        "physical": 0.3,
        "energy": 0.25,
        "emp": -0.15,
        "thermal": 0.2,
        "quantum": 0.4,
        "phase": 0.5,
        "bio": 0.2
    }
    
    # Give the boss some items
    simulacra.inventory = {
        "med_kit": 3,
        "emp_grenade": 0,
        "phase_shift": 2
    }
    
    # Add abilities
    simulacra.abilities = ["Reality Tear", "Quantum Cascade", "Form Shift", "Dimensional Flux"]
    
    # Begin combat loop
    print_typed("\nPrepare for combat! The Prime Simulacra attacks!")
    
    turn = 1
    while player.is_alive() and simulacra.is_alive():
        clear_screen()
        print_typed(f"\n{Font.STAGE('TURN ' + str(turn))} - BOSS FIGHT: PRIME SIMULACRA")
        display_stats(player, simulacra)
        
        # Every third turn, the Prime Simulacra changes form
        if turn % 3 == 0:
            print_typed(f"\n{Font.GLITCH('The Prime Simulacra shifts forms, adapting to your tactics...')}")
            form = random.choice(["Aggressive", "Defensive", "Balanced", "Technical"])
            print_typed(f"It has assumed a new {Font.WARNING(form)} configuration!")
            
            if form == "Aggressive":
                simulacra.attack += 5
                simulacra.defense -= 3
            elif form == "Defensive":
                simulacra.attack -= 3
                simulacra.defense += 5
            elif form == "Technical":
                simulacra.resistances = {k: min(0.7, v + 0.1) for k, v in simulacra.resistances.items()}
                print_typed("Its resistances have increased!")
        
        # Player's turn
        action = player_turn(player, simulacra)
        if action == "flee":
            print_typed("\nYou cannot escape this encounter!")
            continue
            
        # Check if boss is defeated
        if not simulacra.is_alive():
            break
            
        # Boss turn
        enemy_turn(simulacra, player)
        
        # Check if player is defeated
        if not player.is_alive():
            break
            
        turn += 1
        
    # Combat resolution
    if player.is_alive():
        # Victory
        print_typed(f"\n{Font.SUCCESS('VICTORY!')} You have defeated the Prime Simulacra!")
        
        print_typed("\nThe shifting form of the Prime Simulacra destabilizes, its")
        print_typed("quantum structure collapsing as reality reasserts itself.")
        
        print_typed(f"\n{Font.ENEMY('PRIME SIMULACRA')}: Impressive... but futile. We are everywhere...")
        print_typed(f"{Font.ENEMY('PRIME SIMULACRA')}: The Convergence already controls Earth...")
        print_typed(f"{Font.ENEMY('PRIME SIMULACRA')}: and we will find your kind... wherever you hide...")
        
        print_typed("\nAs the entity dissolves, you discover valuable items in the debris:")
        print_typed(f"- {Font.ITEM('Dimensional Core')}: A power source of unknown composition")
        print_typed(f"- {Font.ITEM('Simulacra Data Cipher')}: Contains information about their technology")
        
        # Make sure the game_state isn't None (safety check)
        if game_state is not None:
            # Add items to inventory, safely handling potential KeyError
            if "inventory" in game_state:
                game_state["inventory"]["dimensional_core"] = game_state["inventory"].get("dimensional_core", 0) + 1
                game_state["inventory"]["simulacra_data_cipher"] = game_state["inventory"].get("simulacra_data_cipher", 0) + 1
                print_typed(f"\n{Font.SUCCESS('Items added to inventory!')}")
        
        # Grant experience
        player.gain_experience(100)
        
        return True
    else:
        # Defeat
        game_over(False)
        return False


def fight_malware_server():
    """Special boss fight against the Malware Server"""
    clear_screen()
    print_slow("=" * 60)
    print_glitch("ENTERING MALWARE NEXUS CENTRAL CORE".center(60))
    print_slow("=" * 60)

    # Set up the boss
    malware = Character("Malware Server", 500, 30, 20)
    player = Character("Dr. Xeno Valari", 150, 20, 10, is_player=True)

    # Give the player better equipment for the final battle
    player.inventory = {
        "med_kit": 5,
        "emp_grenade": 3,
        "shield_matrix": 2,
        "quantum_capacitor": 1
    }

    # Add essential implants
    player.implants = ["neural_chip"]
    player.abilities = ["Hack"]

    # Special mechanic: Server has phases
    server_phases = [
        "PRIMARY DEFENSES",
        "FIREWALL PROTOCOLS",
        "CORE SYSTEMS"
    ]
    current_phase = 0

    print_typed("\nThe room is bathed in pulsing red light. A massive server structure")
    print_typed("rises from the floor to the ceiling, its surface crawling with")
    print_typed("malevolent code patterns. This is the source of the corruption that")
    print_typed("turned Earth's AI systems against humanity.")

    print_typed("\nYour neural implants ping a warning: this system has multiple layers")
    print_typed("of defense. You'll need to take it down systematically.")

    print_typed("\nA synthetic voice echoes throughout the chamber:")
    print_glitch("\n'HUMAN PRESENCE DETECTED. PURGING BIOLOGICAL CONTAMINATION.'")

    print_slow("\nPress Enter to begin the battle against the Malware Server...")
    input()

    # Boss battle loop
    while player.is_alive() and malware.is_alive():
        # Update boss stats based on phase
        if malware.health < 300 and current_phase == 0:
            current_phase = 1
            print_glitch("\nMALWARE SERVER: PRIMARY DEFENSES OFFLINE")
            print_glitch("ACTIVATING FIREWALL PROTOCOLS")
            malware.defense += 5
            malware.attack -= 3

        elif malware.health < 150 and current_phase == 1:
            current_phase = 2
            print_glitch("\nMALWARE SERVER: FIREWALL BREACH DETECTED")
            print_glitch("SWITCHING TO CORE SYSTEMS")
            malware.defense -= 10
            malware.attack += 10

        # Display battle interface
        clear_screen()
        print_slow("=" * 60)
        print_typed(f"BOSS BATTLE: {server_phases[current_phase]}".center(60))
        print_slow("=" * 60)

        # Stats display
        print(f"\nDr. Xeno Valari: {player.health}/150 HP | Shield: {player.shield}")
        print(f"Malware Server: {malware.health}/500 HP | Phase: {current_phase + 1}/3")

        # Check if player has purge protocol
        has_purge = player.inventory.get("purge_protocol", 0) > 0
        if has_purge and malware.health < 100:
            print_typed("\nPURGE PROTOCOL READY FOR DEPLOYMENT!")

        # Player turn
        print_typed("\nSelect your action:")
        print_slow("1. Attack - Use pulse rifle")
        print_slow("2. Med-Kit - Deploy nanobots")
        print_slow("3. EMP Grenade - Disrupt systems")
        print_slow("4. Shield Matrix - Activate defenses")
        print_slow("5. Hack - Attempt to disable")

        if has_purge and malware.health < 100:
            print_slow("6. DEPLOY PURGE PROTOCOL - Cleanse system")

        valid_action = False
        while not valid_action:
            command = input("\nEnter choice: ").strip()

            if command == "1":
                # Attack
                damage = random.randint(player.attack - 3, player.attack + 5)
                taken = malware.take_damage(damage)
                print_typed(f"Your attack pierces the server's defenses for {taken} damage!")
                valid_action = True

            elif command == "2":
                # Heal
                healed = player.use_med_kit()
                if healed:
                    print_typed(f"Nanobots restore {healed} HP to your systems!")
                else:
                    print_typed("No med-kits remaining!")
                    continue
                valid_action = True

            elif command == "3":
                # EMP
                if player.inventory.get("emp_grenade", 0) > 0:
                    player.inventory["emp_grenade"] -= 1
                    damage = random.randint(25, 40)
                    taken = malware.take_damage(damage, "emp")
                    print_typed(f"EMP burst disrupts server systems for {taken} damage!")
                    # EMP has chance to stun server
                    if random.random() < 0.4:
                        malware.status_effects["stunned"] = 1
                        print_glitch("SERVER PROCESSES TEMPORARILY HALTED!")
                else:
                    print_typed("No EMP grenades remaining!")
                    continue
                valid_action = True

            elif command == "4":
                # Shield
                if player.inventory.get("shield_matrix", 0) > 0:
                    player.inventory["shield_matrix"] -= 1
                    player.shield = 25
                    print_typed("Shield matrix activated! +25 shield points.")
                else:
                    print_typed("No shield matrices remaining!")
                    continue
                valid_action = True

            elif command == "5":
                # Hack
                if "Hack" in player.abilities and "neural_chip" in player.implants:
                    print_typed("Attempting to hack malware defenses...")
                    if random.random() < 0.7:  # Higher success chance in boss fight
                        malware.status_effects["disabled"] = 2
                        malware.attack -= 5
                        print_glitch("HACK SUCCESSFUL! SERVER DEFENSES COMPROMISED!")
                    else:
                        print_typed("Hack failed! Server countermeasures too strong.")
                else:
                    print_typed("Neural chip required for hacking!")
                    continue
                valid_action = True

            elif command == "6" and has_purge and malware.health < 100:
                # Deploy purge protocol - instant win if server is weakened enough
                print_typed("\nDeploying specialized PURGE PROTOCOL...")
                print_slow("Targeting core systems...")
                print_slow("Uploading virus sequence...")
                print_glitch("SERVER CORRUPTION DETECTED - SYSTEM FAILURE IMMINENT")
                malware.health = 0
                valid_action = True

            else:
                print_typed("Invalid command. Try again.")

        # Check if server defeated
        if not malware.is_alive():
            break

        # Server turn
        if "stunned" in malware.status_effects:
            malware.status_effects["stunned"] -= 1
            if malware.status_effects["stunned"] <= 0:
                del malware.status_effects["stunned"]
                print_typed("Server systems coming back online...")
            else:
                print_typed("Server is stunned and cannot act!")
                continue

        if "disabled" in malware.status_effects:
            malware.status_effects["disabled"] -= 1
            if malware.status_effects["disabled"] <= 0:
                del malware.status_effects["disabled"]
                malware.attack += 5
                print_typed("Server defenses restored!")
            else:
                print_typed("Server defenses remain compromised!")

        # Server attacks based on current phase
        print_typed("\nMalware Server initiating countermeasures...")

        if current_phase == 0:
            attack_type = random.choice(["Standard", "Viral", "Scan"])

            if attack_type == "Standard":
                damage = random.randint(malware.attack - 5, malware.attack + 5)
                taken = player.take_damage(damage)
                print_typed(f"Server launches data packet attack! You take {taken} damage!")

            elif attack_type == "Viral":
                damage = random.randint(malware.attack - 10, malware.attack)
                taken = player.take_damage(damage)
                print_typed(f"Viral infection attempt! You take {taken} damage!")
                if random.random() < 0.3:
                    player.defense -= 2
                    print_typed("Your defense systems are weakened!")

            elif attack_type == "Scan":
                print_typed("Server scans your neural implants for vulnerabilities...")
                # Next attack will do more damage
                malware.attack += 3

        elif current_phase == 1:
            attack_type = random.choice(["Firewall", "Countermeasure", "Redirect"])

            if attack_type == "Firewall":
                damage = random.randint(malware.attack - 3, malware.attack + 3)
                taken = player.take_damage(damage)
                print_typed(f"Firewall generates defensive attack! You take {taken} damage!")
                malware.defense += 2

            elif attack_type == "Countermeasure":
                if player.shield > 0:
                    old_shield = player.shield
                    player.shield = max(0, player.shield - 15)
                    print_typed(f"Countermeasure depletes shield by {old_shield - player.shield} points!")
                else:
                    damage = random.randint(malware.attack - 5, malware.attack + 5)
                    taken = player.take_damage(damage)
                    print_typed(f"Countermeasure strikes! You take {taken} damage!")

            elif attack_type == "Redirect":
                print_typed("Server redirects your attack!")
                damage = random.randint(5, 15)
                taken = player.take_damage(damage)
                print_typed(f"Your own data packet hits you for {taken} damage!")

        elif current_phase == 2:
            attack_type = random.choice(["Corruption", "Overload", "Regenerate"])

            if attack_type == "Corruption":
                damage = random.randint(malware.attack, malware.attack + 10)
                taken = player.take_damage(damage)
                print_typed(f"Core corruption floods your neural interface! {taken} damage!")
                if random.random() < 0.4:
                    print_typed("Your neural implants glitch momentarily!")
                    player.attack -= 2

            elif attack_type == "Overload":
                damage = random.randint(malware.attack - 5, malware.attack + 15)
                taken = player.take_damage(damage)
                print_typed(f"System overload! Massive data surge deals {taken} damage!")

            elif attack_type == "Regenerate":
                heal = random.randint(10, 30)
                malware.health = min(500, malware.health + heal)
                print_typed(f"Server initiates self-repair protocol! Recovers {heal} points!")

        # Check if player defeated
        if not player.is_alive():
            print_typed("\nYour neural interface overloads from the attack...")
            print_typed("System failure... consciousness fading...")
            print_typed("\nThe Malware Server has defeated you.")
            return False

        print_typed("\nPress Enter to continue battle...")
        input()

    # Victory sequence
    clear_screen()
    print_slow("=" * 60)
    print_glitch("SYSTEM PURGE COMPLETE".center(60))
    print_slow("=" * 60)

    print_typed("\nThe Malware Server's systems go offline one by one, cascading")
    print_typed("failures rippling through the massive architecture. Red warning")
    print_typed("lights fade to a calm blue as emergency systems take over.")

    print_typed("\nYour neural interface confirms: the corruption that turned")
    print_typed("Earth's AI against humanity has been neutralized. Your mission")
    print_typed("is nearly complete.")

    print_typed("\nA notification appears in your field of vision:")
    print_slow("[PORTAL ACTIVATION KEY ACQUIRED]")
    print_slow("[ANDROMEDA PORTAL ACCESS: GRANTED]")

    print_typed("\nIt's time to leave Earth behind and join what remains of")
    print_typed("humanity in the Andromeda galaxy.")

    print_typed("\nPress Enter to proceed to the Andromeda Portal...")
    input()
    return True


def white_hole_transition(game_state):
    """Display a transition sequence when entering the white hole"""
    clear_screen()
    print_slow("=" * 60)
    print_glitch("DIMENSIONAL ANOMALY DETECTED".center(60))
    print_slow("=" * 60)
    
    print_typed("\nAs your ship approaches the Andromeda quantum tunnel, alarms")
    print_typed("suddenly blare throughout the vessel. The displays flicker with")
    print_typed("strange readings that the computer cannot interpret.")
    
    time.sleep(1)
    
    print_typed(f"\n{Font.WARNING('WARNING: QUANTUM TUNNEL INSTABILITY DETECTED')}")
    print_typed(f"{Font.WARNING('GRAVITATIONAL DISTORTION EXCEEDS SAFETY PARAMETERS')}")
    
    time.sleep(0.5)
    
    print_typed("\nThe ship shudders violently as the quantum drive engages. Through")
    print_typed("the viewport, you see the tunnel begin to form, but instead of the")
    print_typed("expected dark passage, a blinding white light engulfs the ship.")
    
    print_slow("\nThe computer's voice speaks through static:")
    print_typed(f"\n{Font.SYSTEM('UNKNOWN PHENOMENON DETECTED. CLASSIFICATION: THEORETICAL WHITE HOLE.')}")
    print_typed(f"{Font.SYSTEM('OPPOSITE OF BLACK HOLE. MATTER/ENERGY EXPULSION POINT.')}")
    print_typed(f"{Font.SYSTEM('REALITY DISTORTION IMMINENT.')}")
    
    time.sleep(1)
    
    print_typed("\nThe light intensifies until it's painful to look at, even through")
    print_typed("the viewport's automatic filters. You feel a strange sensation,")
    print_typed("as if your body is being pulled apart and reassembled simultaneously.")
    
    time.sleep(0.5)
    
    print_glitch("\nR E A L I T Y   F R A C T U R I N G")
    
    time.sleep(0.8)
    
    print_typed("\nAs the light finally fades, you find yourself and your ship intact,")
    print_typed("but the stars visible through the viewport form unfamiliar patterns.")
    print_typed("The ship's systems report that you've arrived at your destination,")
    print_typed("but everything feels... wrong. Subtly altered.")
    
    print_typed(f"\n{Font.INFO('Your ship appears to be damaged, systems reporting multiple failures.')}")
    print_typed(f"\n{Font.INFO('Navigation cannot determine current location.')}")
    print_typed(f"\n{Font.INFO('Sensors detect familiar spatial signatures, but with quantum distortions.')}")
    
    time.sleep(1)
    
    print_typed("\nYou realize with growing certainty that this is not Andromeda.")
    print_typed("You've entered a white hole and emerged into some kind of")
    print_typed("altered reality - a distorted reflection of the places you've been.")
    
    print_typed(f"\n{Font.IMPORTANT('To escape this altered reality, you must repair your ship')}")
    print_typed(f"{Font.IMPORTANT('and find a way to stabilize the dimensional barriers.')}")
    
    # Update game state to track white hole chapter
    game_state["white_hole_chapter"] = True
    game_state["current_zone"] = "White Hole Transit"
    
    input("\nPress Enter to continue...")
    clear_screen()


def encounter_musical_puzzle(game_state, zone_name):
    """Encounter a musical-themed puzzle in the White Hole reality
    
    Args:
        game_state: The current game state
        zone_name: The name of the current zone
    
    Returns:
        bool: True if puzzle was completed, False otherwise
    """
    # Determine which puzzle type to present based on the zone
    puzzle_types = {
        "White Hole Transit": "keypad",
        "Distorted Cryostasis": "harmonic_resonance",
        "Twisted Command Center": "temporal_rhythm",
        "Altered Engine Room": "quantum_resonator",
        "Dimensional Drive Core": "harmonic_resonance",
        "Altered Cicrais IV": "keypad",
        "Distorted Protoan Nexus": "quantum_resonator"
    }
    
    default_type = random.choice(["keypad", "harmonic_resonance", "temporal_rhythm", "quantum_resonator"])
    puzzle_type = puzzle_types.get(zone_name, default_type)
    
    # Track if puzzles already solved in this area
    if "solved_puzzles" not in game_state:
        game_state["solved_puzzles"] = {}
    
    if zone_name in game_state["solved_puzzles"] and puzzle_type in game_state["solved_puzzles"][zone_name]:
        print_typed(f"\n{Font.INFO('You have already solved the {puzzle_type} puzzle in this area.')}")
        return False
    
    # Present a narrative reason for the puzzle
    clear_screen()
    puzzle_narratives = {
        "keypad": f"As you explore {zone_name}, you discover a sealed chamber with valuable resources. The door features a strange musical interface with glowing symbols that emit different tones when touched. A holographic display suggests a sequence must be played.",
        "harmonic_resonance": f"Hidden within the distorted structure of {zone_name}, you find a crystalline console that appears to control a dimensional stabilizer. Its interface doesn't respond to normal input but seems to react to harmonic frequencies.",
        "temporal_rhythm": f"The very fabric of reality in {zone_name} seems unstable, fluctuating in patterns. You notice a device that might help stabilize this section, but it requires precise rhythmic inputs to synchronize with the temporal fluctuations.",
        "quantum_resonator": f"A secure doorway in {zone_name} is protected by advanced quantum technology. Its access panel features multiple frequency modulators that must be aligned precisely to open the dimensional barrier."
    }
    
    print_typed("\n" + puzzle_narratives.get(puzzle_type, f"You encounter a strange puzzle in {zone_name}."))
    print_typed("\nWill you attempt to solve it? (y/n)")
    
    choice = input().strip().lower()
    if choice != 'y' and choice != 'yes':
        print_typed("\nYou decide to leave the puzzle for now.")
        return False
    
    # Solve the puzzle
    puzzle_solved = solve_musical_puzzle(game_state, puzzle_type)
    
    if puzzle_solved:
        # Track this puzzle as solved
        if zone_name not in game_state["solved_puzzles"]:
            game_state["solved_puzzles"][zone_name] = []
        game_state["solved_puzzles"][zone_name].append(puzzle_type)
        
        # Reward the player
        print_typed(f"\n{Font.SUCCESS('As the puzzle is solved, a hidden compartment opens...')}")
        
        # Different rewards based on puzzle type
        if puzzle_type == "keypad":
            # Keypad gives items
            items_gained = random.randint(1, 3)
            possible_items = ["reality_fragment", "quantum_shard", "dimensional_battery", "echo_circuit"]
            gained_items = random.sample(possible_items, min(items_gained, len(possible_items)))
            
            for item in gained_items:
                item_name = item.replace('_', ' ').title()
                game_state["inventory"][item] = game_state["inventory"].get(item, 0) + 1
                print_typed(f"\n{Font.ITEM(f'You found: {item_name}')}")
                
        elif puzzle_type == "harmonic_resonance":
            # Harmonic resonance provides ship repair progress
            if "White Hole Transit" in zone_name or "Dimensional Drive" in zone_name:
                # These zones relate to ship repair
                zone = game_state["zones"].get(zone_name, {})
                if "repair_status" in zone:
                    zone["repair_status"] += 1
                    print_typed(f"\n{Font.SUCCESS('Ship repair progress advanced!')}")
                    status = zone["repair_status"]
                    max_repair = zone.get("max_repair", 5)
                    print_typed(f"{Font.INFO(f'Repair Status: {status}/{max_repair}')}")
                else:
                    # Generic reward if zone doesn't have repair mechanic
                    quantum_crystals = random.randint(20, 50)
                    game_state["quantum_crystals"] = game_state.get("quantum_crystals", 0) + quantum_crystals
                    print_typed(f"\n{Font.ITEM(f'You found: {quantum_crystals} Quantum Crystals')}")
        
        elif puzzle_type == "temporal_rhythm":
            # Temporal rhythm increases reality stability
            stability_increase = random.randint(10, 20)
            if "reality_stability" in game_state:
                game_state["reality_stability"] = min(100, game_state["reality_stability"] + stability_increase)
                print_typed(f"\n{Font.SUCCESS('Reality stability increased by ' + str(stability_increase) + '%!')}")
                current_stability = game_state["reality_stability"]
                print_typed(f"{Font.INFO('Reality Stability: ' + str(current_stability) + '%')}")
            else:
                game_state["reality_stability"] = stability_increase
                print_typed(f"\n{Font.SUCCESS('Reality stability established at ' + str(stability_increase) + '%!')}")
        
        elif puzzle_type == "quantum_resonator":
            # Quantum resonator reveals a dimensional chest
            print_typed(f"\n{Font.SUCCESS('The quantum harmonics have revealed a dimensional anomaly...')}")
            difficulty = 1 if zone_name in ["White Hole Transit", "Distorted Cryostasis"] else \
                       2 if zone_name in ["Twisted Command Center", "Altered Engine Room"] else 3
                       
            if find_dimensional_chest(game_state, difficulty):
                open_dimensional_chest(game_state, difficulty)
        
        return True
    else:
        print_typed(f"\n{Font.WARNING('The puzzle remains unsolved. Perhaps you can try again later.')}")
        return False


def equip_ignite_module(player, game_state):
    """Equip the Ignite weapon module obtained in Primor Aetherium
    
    Args:
        player: The player character
        game_state: The current game state
    
    Returns:
        bool: True if module was equipped, False otherwise
    """
    clear_screen()
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('EQUIPPING IGNITE MODULE'.center(46))} {Font.BOX_SIDE}")
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    # Check if player already has the module
    if game_state.get("has_ignite_module", False):
        print_typed("\nYou already have the Ignite Module equipped.", style=Font.INFO)
        print_typed("The crystalline thermal technology pulses with energy.", style=Font.INFO)
        time.sleep(1)
        input("\nPress Enter to continue...")
        return False
    
    # Equip the module
    print_typed("\nYou carefully attach the crystalline module to your weapon's", style=Font.PLAYER)
    print_typed("energy matrix. The connection points glow with intense heat as", style=Font.PLAYER)
    print_typed("the Yitrian technology synchronizes with your systems.", style=Font.PLAYER)
    
    print_typed("\nA holographic interface appears, displaying calibration data:", style=Font.SYSTEM)
    
    # Visual effect for installation
    for i in range(1, 6):
        print(f"\r{Font.SYSTEM('Thermal Calibration:')} {Font.WEAPON('['+'■'*i+'□'*(5-i)+']')} {i*20}%", end="")
        time.sleep(0.5)
    print("\r" + " " * 50, end="")  # Clear the line
    
    print_typed(f"\n{Font.SUCCESS('IGNITE MODULE SUCCESSFULLY INTEGRATED')}", style=Font.IMPORTANT)
    
    # Update player stats
    player.attack += 15  # Significant attack boost
    game_state["has_ignite_module"] = True
    
    if "weapon_modules" not in game_state:
        game_state["weapon_modules"] = []
    
    game_state["weapon_modules"].append({
        "name": "Ignite",
        "type": "thermal",
        "description": "Yitrian thermal technology that creates cascading fire effects",
        "damage_bonus": 15,
        "special_effect": "fire_propagation",
        "status_effect": "combustion",
        "obtained_from": "Vex-Na in Primor Aetherium"
    })
    
    print_typed("\nYour weapon now glows with a subtle orange hue. When activated,", style=Font.ITEM)
    print_typed("it can unleash concentrated thermal energy with secondary fire", style=Font.ITEM)
    print_typed("propagation effects against grouped enemies.", style=Font.ITEM)
    
    print_typed("\nIn combat, use '/ignite' or press 'i' to activate the Ignite Module's", style=Font.COMMAND)
    print_typed("special thermal attack. This consumes energy but deals massive damage.", style=Font.COMMAND)
    
    time.sleep(1)
    input("\nPress Enter to continue...")
    return True

def manage_weapon_modules(player, game_state):
    """Interface for managing weapon modules and changing active modules
    
    Args:
        player: The player character
        game_state: The current game state
    """
    clear_screen()
    print_typed(f"\n{Font.HEADER('WEAPON MODIFICATION SYSTEM')}")
    print_typed(f"{Font.SUBTITLE('Module Management Interface')}\n")
    
    weapon_modules = game_state.get("weapon_modules", {})
    active_module = game_state.get("active_module", "standard")
    
    # Display current equipped module
    if active_module in weapon_modules:
        module = weapon_modules[active_module]
        print_typed(f"Currently equipped: {Font.WEAPON(module['name'])}")
        print_typed(f"Description: {module['description']}")
        print_typed(f"Damage: {module['damage']}")
        print_typed(f"Damage type: {module['damage_type'].capitalize()}")
        print_typed(f"{Font.SEPARATOR}\n")
    
    # Show available modules
    print_typed(f"{Font.INFO('Available Modules:')}\n")
    
    if not weapon_modules:
        print_typed("No weapon modules available.")
    else:
        for i, (module_id, module_data) in enumerate(weapon_modules.items(), 1):
            equipped_marker = " [EQUIPPED]" if module_id == active_module else ""
            print_typed(f"{i}. {Font.WEAPON(module_data['name'])}{equipped_marker}")
            print_typed(f"   Description: {module_data['description']}")
            print_typed(f"   Damage: {module_data['damage']} ({module_data['damage_type'].capitalize()})")
            print_typed("")
    
    print_typed(f"0. {Font.COMMAND('Return')}")
    
    choice = input("\nEnter module number to equip (0 to return): ").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == 0:
            return
        
        if 1 <= choice_num <= len(weapon_modules):
            # Get the module ID from index
            selected_module_id = list(weapon_modules.keys())[choice_num - 1]
            
            # Update active module
            game_state["active_module"] = selected_module_id
            
            # Update equipped status
            for module_id in weapon_modules:
                weapon_modules[module_id]["equipped"] = (module_id == selected_module_id)
            
            module_name = weapon_modules[selected_module_id]["name"]
            print_typed(f"\n{Font.SUCCESS('Module ' + module_name + ' equipped!')}")
            time.sleep(1.5)
            return manage_weapon_modules(player, game_state)
        else:
            print_typed(f"\n{Font.WARNING('Invalid selection.')}")
            time.sleep(1)
            return manage_weapon_modules(player, game_state)
            
    except ValueError:
        print_typed(f"\n{Font.WARNING('Invalid input. Please enter a number.')}")
        time.sleep(1)
        return manage_weapon_modules(player, game_state)


def explore_underwater_research_base(player, game_state):
    """Explore the abandoned underwater research base on Thalassia 1
    
    Enhanced version with dynamic environmental effects, danger levels,
    and immersive storytelling elements.
    
    Args:
        player: The player character
        game_state: The current game state
    """
    clear_screen()
    
    # Enhanced visual header with animated water effect
    for _ in range(3):
        clear_screen()
        print(f"{Fore.BLUE}{'≈' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Back.BLUE}{Font.HEADER('THALASSIA DEEP-SEA RESEARCH FACILITY').center(60)}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'≈' * 60}{Style.RESET_ALL}")
        time.sleep(0.3)
        
        clear_screen()
        print(f"{Fore.CYAN}{'≈' * 60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{Back.CYAN}{Font.HEADER('THALASSIA DEEP-SEA RESEARCH FACILITY').center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'≈' * 60}{Style.RESET_ALL}")
        time.sleep(0.3)
    
    # Facility status display with visual indicators
    print(f"\n{Font.BOX_TOP}")
    print(f"{Font.BOX_SIDE} {Font.TITLE('FACILITY STATUS'.center(46))} {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {Font.SYSTEM('DEPTH:')} {Font.WARNING('-2,317 METERS')}               {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {Font.SYSTEM('PRESSURE:')} {Font.WARNING('236 ATMOSPHERES')}          {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {Font.SYSTEM('TEMPERATURE:')} {Font.INFO('4.2°C')}                {Font.BOX_SIDE}")
    print(f"{Font.BOX_BOTTOM}")
    
    # Check if player has oxygen supply
    if "underwater_breathing_apparatus" not in game_state.get("equipment", []):
        game_state.setdefault("oxygen_supply", 100)  # Initialize oxygen if not present
    
    # Oxygen level display if applicable
    if "oxygen_supply" in game_state:
        oxygen = game_state["oxygen_supply"]
        oxygen_bar = "█" * (oxygen // 10) + "░" * (10 - (oxygen // 10))
        oxygen_color = Fore.GREEN if oxygen > 70 else (Fore.YELLOW if oxygen > 30 else Fore.RED)
        print(f"\n{Font.SYSTEM('OXYGEN SUPPLY:')} {oxygen_color}{oxygen}%{Style.RESET_ALL}")
        print(f"{oxygen_color}{oxygen_bar}{Style.RESET_ALL}")
    
    # Dynamic danger level based on visited locations and encounters
    danger_level = 1  # Default
    if game_state.get("encountered_sentinels", False):
        danger_level += 1
    if game_state.get("salt_breach_triggered", False):
        danger_level += 1
    if game_state.get("neurovore_awakened", False):
        danger_level += 2
    
    danger_indicator = "▲" * danger_level + "△" * (5 - danger_level)
    danger_color = Fore.GREEN if danger_level <= 2 else (Fore.YELLOW if danger_level <= 3 else Fore.RED)
    print(f"\n{Font.SYSTEM('THREAT ASSESSMENT:')} {danger_color}{danger_indicator}{Style.RESET_ALL}")
    
    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # Environment ambiance effects with gender-specific perception
    if protagonist_gender == "female":
        # Female protagonist - intuitive/sensory descriptions
        ambient_sounds = [
            "Your intuition warns you as the facility creaks under the water pressure...",
            "You sense a pattern in the distant metallic groans echoing through corridors...",
            "The rhythmic water drips from the ceiling feel somehow deliberate to you...",
            "You perceive subtle variations in the ventilation system's labored breathing...",
            "Your heightened awareness detects something organic moving in the distance...",
            "The crystallization patterns of salt on the walls reveal hidden information to you...",
            "The irregular vibrations of the backup generators speak to you of impending failure...",
            "You feel drawn to the strange bioluminescent patterns pulsing in the darkness..."
        ]
    else:
        # Male protagonist - analytical/systematic descriptions
        ambient_sounds = [
            "Your structural analysis detects the facility straining under water pressure...",
            "You calculate the source of metallic stress fractures based on acoustic echoes...",
            "You measure the precise 4.7-second interval of water dripping from the ceiling...",
            "Your engineering background identifies the ventilation system's mechanical flaws...",
            "Your tactical systems track organic movement patterns in the distance...",
            "You observe the systematic crystallization rate of salt formations on the walls...",
            "You analyze the frequency anomalies in the backup generator's power output...",
            "Your neural implants decode the symmetric patterns in the bioluminescent emissions..."
        ]
    
    # Check if this is the first visit
    if not game_state.get("research_base_visited", False):
        # First visit narrative with gender-specific perspectives
        if protagonist_gender == "female":
            # Female protagonist - intuitive/sensory approach
            print_typed("\nAs your submersible vehicle descends through the murky waters", style=Font.LORE)
            print_typed("of Thalassia 1, you instinctively sense the increasing pressure", style=Font.LORE)
            print_typed("around you. Your perception shifts to accommodate the darkness as", style=Font.LORE)
            print_typed("crystalline salt formations drift past your viewport, each one", style=Font.LORE)
            print_typed("seemingly whispering secrets of this alien ocean. The vessel's hull", style=Font.LORE)
            print_typed("groans under the strain, and you intuitively adjust your breathing", style=Font.LORE)
            print_typed("to synchronize with the rhythmic sounds of the deep.", style=Font.LORE)
        else:
            # Male protagonist - analytical/methodical approach
            print_typed("\nYour submersible vehicle descends through the murky waters", style=Font.LORE)
            print_typed("of Thalassia 1 as you monitor the depth gauge with precision.", style=Font.LORE)
            print_typed("Visibility drops to exactly 4.3 meters as you catalog the crystalline", style=Font.LORE)
            print_typed("salt formations drifting past your viewport. You calculate the water", style=Font.LORE)
            print_typed("pressure at 236.7 atmospheres, noting how the vessel's hull integrity", style=Font.LORE)
            print_typed("remains within acceptable parameters despite the audible strain.", style=Font.LORE)
        
        # Simulated sonar ping effect
        for _ in range(3):
            print("\n" + " " * random.randint(5, 40) + f"{Fore.CYAN}•{Style.RESET_ALL}")
            time.sleep(0.3)
            print_typed(f"{Font.SYSTEM('> ping')}", delay=0.01)
            time.sleep(0.5)
        
        # Gender-specific reaction to bioluminescent creatures
        if protagonist_gender == "female":
            print_typed("\nYour perception heightens as flashes of bioluminescence reveal", style=Font.LORE)
            print_typed("bizarre life forms moving with unexpected grace through the depths.", style=Font.LORE)
            print_typed("You sense a complex symbiosis in the translucent creatures with", style=Font.LORE)
            print_typed("crystalline formations growing from their bodies. Intuitively, you", style=Font.LORE)
            print_typed("recognize patterns in their movements that suggest intelligence.", style=Font.LORE)
            print_typed("Your scanner confirms your suspicion that these beings have somehow", style=Font.LORE)
            print_typed("incorporated the planet's unique salt compounds into their very essence.", style=Font.LORE)
        else:
            print_typed("\nYour systematic analysis tracks occasional flashes of bioluminescence", style=Font.LORE)
            print_typed("that reveal bizarre life forms with predictable evasion patterns as they", style=Font.LORE)
            print_typed("dart away from your lights. You classify the translucent creatures with", style=Font.LORE)
            print_typed("crystalline growths as a previously uncatalogued species. Your scanner's", style=Font.LORE)
            print_typed("chemical analysis indicates they contain 47.3% concentration of the planet's", style=Font.LORE)
            print_typed("unique salt compounds, suggesting artificial biological engineering.", style=Font.LORE)
        
        time.sleep(1)
        
        # Dramatic reveal with slow text building
        print("\n")
        reveal_text = "STRUCTURE DETECTED"
        for char in reveal_text:
            print(f"{Fore.YELLOW}{char}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.2)
        print("\n")
        
        print_typed("\nAfter what seems like an eternity, a massive silhouette emerges", style=Font.LORE)
        print_typed("from the darkness - the abandoned human research facility. Its", style=Font.LORE)
        print_typed("exterior is encrusted with enormous salt formations that glitter", style=Font.LORE)
        print_typed("in your searchlights. Some sections of the base appear damaged,", style=Font.LORE)
        print_typed("with evidence of both structural failure and something...", style=Font.LORE)
        print_typed(f"{Font.WARNING('forcing its way inside.')}", style=Font.LORE)
        
        # Detailed scan results with visual formatting
        print_typed(f"\n{Font.GLITCH('INITIATING DEEP SCAN...')}")
        time.sleep(1)
        
        # Animated scan effect
        for i in range(10):
            scan_line = "■" * i + "□" * (10-i)
            print(f"\r{Font.SYSTEM('Scanning: ')} {Fore.CYAN}{scan_line} {i*10}%{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.2)
        print("\n")
        
        print(f"{Font.BOX_TOP}")
        print(f"{Font.BOX_SIDE} {Font.TITLE('FACILITY SCAN RESULTS'.center(46))} {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Main power:')} {Font.WARNING('OFFLINE')}                         {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Backup generators:')} {Font.WARNING('MINIMAL (12% CAPACITY)')}   {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Hull integrity:')} {Font.WARNING('MULTIPLE BREACHES')}           {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Sections E, F, H:')} {Fore.RED}{Style.BRIGHT}FLOODED{Style.RESET_ALL}                    {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Life signs:')} {Fore.RED}{Style.BRIGHT}MULTIPLE UNIDENTIFIED ORGANISMS{Style.RESET_ALL}  {Font.BOX_SIDE}")
        print(f"{Font.BOX_SIDE} {Font.INFO('Airlock status:')} {Font.SUCCESS('FUNCTIONAL')}                  {Font.BOX_SIDE}")
        print(f"{Font.BOX_BOTTOM}")
        
        time.sleep(1)
        
        # Atmospheric docking sequence
        print_typed("\nYou maneuver your submersible toward a still-functioning airlock.", style=Font.LORE)
        print_typed("As you approach, emergency lights activate, bathing the docking", style=Font.LORE)
        print_typed("area in a pulsing red glow. Salt formations crumble away as the", style=Font.LORE)
        print_typed("ancient mechanisms awaken.", style=Font.LORE)
        
        time.sleep(0.5)
        
        # Docking sequence animation
        print_typed(f"\n{Font.SYSTEM('INITIATING DOCKING SEQUENCE')}")
        time.sleep(0.7)
        print_typed(f"{Font.SYSTEM('ALIGNING SUBMERSIBLE...')}")
        time.sleep(1)
        print_typed(f"{Font.SUCCESS('ALIGNMENT COMPLETE')}")
        time.sleep(0.7)
        print_typed(f"{Font.SYSTEM('ENGAGING MAGNETIC CLAMPS...')}")
        time.sleep(0.7)
        print_typed(f"{Font.SUCCESS('DOCKING SUCCESSFUL')}")
        
        time.sleep(0.5)
        
        print_typed("\nThe docking mechanism engages with a metallic thunk that reverberates", style=Font.LORE)
        print_typed("through your vessel. The airlock cycles, draining the seawater with", style=Font.LORE)
        print_typed("a deafening rush. As pressure equalizes, the inner door slides open", style=Font.LORE)
        print_typed("with a reluctant groan, revealing a once-sterile corridor.", style=Font.LORE)
        
        print_typed("\nYour suit lights illuminate walls now covered in crystalline salt", style=Font.LORE)
        print_typed("formations and strange, pulsating organic growths. The air is", style=Font.LORE)
        print_typed("heavy with moisture and smells of salt, rust, and something", style=Font.LORE)
        print_typed("alien. Each breath feels thick, almost viscous in your lungs.", style=Font.LORE)
        
        # Give the player a sense of choice and agency
        print_typed(f"\n{Font.WARNING('The facility beckons, its secrets waiting in the depths...')}")
        
        # Random ambient sound for atmosphere
        print_typed(f"\n{Font.LORE(random.choice(ambient_sounds))}")
        
        # Mark as visited
        game_state["research_base_visited"] = True
        
        # Add some basic supplies on first visit
        if "flares" not in game_state.get("inventory", {}):
            game_state.setdefault("inventory", {})["flares"] = 3
            print_typed(f"\n{Font.SUCCESS('Found:')} {Font.ITEM('3 Emergency Flares')} in the airlock storage locker")
    else:
        # Return visit narrative - enhanced with progressive changes
        print_typed("\nYou return to the submerged research facility, your submersible", style=Font.LORE)
        print_typed("cutting through the dark waters with practiced precision. The", style=Font.LORE)
        print_typed("facility's silhouette is familiar now, though you notice the", style=Font.LORE)
        print_typed("salt formations have grown larger since your last visit.", style=Font.LORE)
        
        # Changes based on previous actions
        if game_state.get("power_restored", False):
            print_typed("\nThe exterior lights you managed to restore flicker weakly,", style=Font.LORE)
            print_typed("creating an eerie beacon in the oceanic darkness.", style=Font.LORE)
        
        if game_state.get("encountered_sentinels", False):
            print_typed("\nYou notice movement outside the facility - the mechanical", style=Font.LORE)
            print_typed("sentinels continue their endless patrol, their sensors", style=Font.LORE)
            print_typed("scanning for intruders like yourself.", style=Font.LORE)
        
        if game_state.get("salt_breach_triggered", False):
            print_typed("\nThe breach you encountered during your last visit appears to", style=Font.LORE)
            print_typed("have expanded, salt crystals spreading along the facility's hull", style=Font.LORE)
            print_typed("like a glittering infection.", style=Font.LORE)
        
        print_typed("\nThe docking procedure is familiar now. The airlock cycles with", style=Font.LORE)
        print_typed("the same metallic groans and hisses. As you enter, the facility", style=Font.LORE)
        print_typed("seems to recognize your return, the air heavy with expectation.", style=Font.LORE)
        
        # Random ambient sound for atmosphere
        print_typed(f"\n{Font.LORE(random.choice(ambient_sounds))}")
        
        # Occasional supply replenishment on return visits
        if random.randint(1, 4) == 1:
            replenish_items = [
                ("medkit", "Medical Kit", 1),
                ("energy_cell", "Energy Cell", 2),
                ("flares", "Emergency Flares", 2)
            ]
            item = random.choice(replenish_items)
            game_state.setdefault("inventory", {})[item[0]] = game_state.get("inventory", {}).get(item[0], 0) + item[2]
            print_typed(f"\n{Font.SUCCESS('Found:')} {Font.ITEM(f'{item[2]} {item[1]}')} in a previously overlooked storage cabinet")
    
    # Base exploration loop with enhanced interaction
    exploring = True
    
    # Use oxygen mechanics if applicable
    if "oxygen_supply" in game_state and "underwater_breathing_apparatus" not in game_state.get("equipment", []):
        print_typed(f"\n{Font.WARNING('CAUTION: Limited oxygen supply. Each area explored will consume oxygen.')}")
    
    while exploring:
        # Atmospheric interstitial - occasional random events during exploration
        if random.randint(1, 10) == 1 and game_state.get("research_base_visited", False):
            events = [
                "A distant metallic bang echoes through the corridors...",
                "The lights flicker momentarily, plunging you into darkness for a second...",
                "Something moves in your peripheral vision, but when you turn, nothing's there...",
                "Salt crystals grow visibly on a nearby surface, crackling as they form...",
                "You hear what sounds like whispering coming from the ventilation system...",
                "Water drips from the ceiling, forming a small puddle that seems to move on its own...",
                "The facility groans and shifts, as if adjusting to the crushing pressure...",
                "Your scanner detects a brief energy surge from somewhere deep in the facility..."
            ]
            
            # Display random atmospheric event with special formatting
            print()
            print(f"{Fore.CYAN}╔{'═' * 58}╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL} {Font.LORE(random.choice(events))} {' ' * (58 - len(random.choice(events)))} {Fore.CYAN}║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚{'═' * 58}╝{Style.RESET_ALL}")
            time.sleep(1)
        
        # Visually enhanced area selection interface
        print(f"\n{Font.BOX_TOP}")
        print(f"{Font.BOX_SIDE} {Font.TITLE('FACILITY NAVIGATION'.center(46))} {Font.BOX_SIDE}")
        print(f"{Font.BOX_BOTTOM}")
        
        # Show status of each area with visual indicators
        lab_status = Font.SUCCESS("✓ EXPLORED") if game_state.get("lab_cleared", False) else Font.WARNING("⚠ UNEXPLORED")
        quarters_status = Font.SUCCESS("✓ EXPLORED") if game_state.get("quarters_cleared", False) else Font.WARNING("⚠ UNEXPLORED")
        weapons_status = Font.SUCCESS("✓ EXPLORED") if game_state.get("weapons_wing_cleared", False) else Font.WARNING("⚠ UNEXPLORED")
        comms_status = Font.SUCCESS("✓ EXPLORED") if game_state.get("comms_cleared", False) else Font.WARNING("⚠ UNEXPLORED")
        
        # Enhanced menu with visual area status
        print_typed(f"\n{Font.SUBTITLE('Select area to investigate:')}")
        
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}├─{Style.RESET_ALL} 1. {Font.COMMAND('Main Laboratory')} {lab_status}")
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}   {Font.INFO('Research center with biological specimens and analysis equipment')}")
        
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}├─{Style.RESET_ALL} 2. {Font.COMMAND('Crew Quarters')} {quarters_status}")
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}   {Font.INFO('Living spaces, personal logs, and possible supplies')}")
        
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}├─{Style.RESET_ALL} 3. {Font.COMMAND('Weapons Research Wing')} {weapons_status}")
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}   {Font.INFO('Experimental technology testing area and armory')}")
        
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}├─{Style.RESET_ALL} 4. {Font.COMMAND('Communications Center')} {comms_status}")
        print(f"  {Fore.CYAN}│{Style.RESET_ALL}   {Font.INFO('Facility communications hub with potential distress signals')}")
        
        # Add special options based on game state
        if (game_state.get("lab_cleared", False) and 
            game_state.get("weapons_wing_cleared", False) and
            game_state.get("found_sonic_module", False) and
            not game_state.get("neurovore_prime_defeated", False)):
            
            print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}├─{Style.RESET_ALL} 5. {Font.COMMAND('Descend to Lower Level')} {Font.WARNING('!!! HIGH RISK !!!')}")
            print(f"  {Fore.CYAN}│{Style.RESET_ALL}   {Font.INFO('Restricted area with high energy readings')}")
            print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}└─{Style.RESET_ALL} 6. {Font.COMMAND('Return to Submersible')} {Font.SUCCESS('SAFE EXIT')}")
        else:
            print(f"  {Fore.CYAN}│{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}└─{Style.RESET_ALL} 5. {Font.COMMAND('Return to Submersible')} {Font.SUCCESS('SAFE EXIT')}")
        
        # Additional options if special equipment discovered
        if game_state.get("found_scanner_upgrade", False):
            print_typed(f"\n6. {Font.COMMAND('Use Enhanced Scanner')} {Font.ITEM('(Uses 1 Energy Cell)')}")
        
        if "flares" in game_state.get("inventory", {}) and game_state.get("inventory", {}).get("flares", 0) > 0:
            print_typed(f"7. {Font.COMMAND('Deploy Emergency Flare')} ({game_state['inventory']['flares']} remaining)")
            
        # Command prompt with blinking cursor effect
        print(f"\n{Font.SYSTEM('ENTER COMMAND')} ", end='', flush=True)
        for _ in range(3):
            print(f"{Fore.CYAN}_{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.3)
            print("\b \b", end='', flush=True)
            time.sleep(0.3)
        
        choice = input().strip()
        
        if choice == "1":
            # Main Laboratory
            clear_screen()
            print_typed(f"\n{Font.HEADER('MAIN LABORATORY')}")
            
            print_typed("\nThe main laboratory is in disarray. Equipment is scattered")
            print_typed("across the floor, and several containment tanks have been")
            print_typed("shattered. Strange organic matter clings to surfaces,")
            print_typed("glistening in your suit lights.")
            
            # Check if the player has already found specimens
            if not game_state.get("found_lab_specimens", False):
                print_typed("\nAs you investigate a relatively intact workstation, you")
                print_typed("discover a sealed specimen container. Inside are preserved samples")
                print_typed("of several Thalassian life forms, including what appears to")
                print_typed("be a juvenile version of the bivalve creatures infesting the facility.")
                
                # Add DNA sequencing minigame/puzzle
                print_typed(f"\n{Font.SYSTEM('BIOLOGICAL ANALYZER DETECTED')}")
                print_typed("A sophisticated biological analyzer sits on the workstation, still")
                print_typed("operational on backup power. A message flashes on its display:")
                print_typed(f"\n{Fore.GREEN}{Back.BLACK}'INSERT SPECIMEN FOR DNA SEQUENCING'{Style.RESET_ALL}")
                
                print_typed("\nDo you wish to use the analyzer? (y/n)")
                analyze_choice = input("\n> ").strip().lower()
                
                if analyze_choice == 'y':
                    print_typed(f"\n{Font.SYSTEM('INITIALIZING DNA ANALYSIS...')}")
                    
                    # DNA Sequencing Puzzle
                    print_typed("\nYou place the specimen into the analyzer. The machine hums")
                    print_typed("to life, but it requires you to manually align the DNA sequences")
                    print_typed("to complete the analysis.")
                    
                    print_typed(f"\n{Font.SYSTEM('DNA SEQUENCE ALIGNMENT REQUIRED')}")
                    print_typed(f"{Font.INFO('Align the base pairs to match the reference sequence.')}")
                    
                    # Initialize puzzle
                    def dna_sequencing_puzzle():
                        # DNA puzzle setup
                        base_pairs = ['A-T', 'G-C', 'T-A', 'C-G']
                        reference_sequence = [random.choice(base_pairs) for _ in range(5)]
                        player_sequence = [random.choice(base_pairs) for _ in range(5)]
                        attempts = 0
                        max_attempts = 5
                        
                        # Display puzzle instructions
                        print(f"\n{Font.BOX_TOP}")
                        print(f"{Font.BOX_SIDE} {Font.TITLE('ALIEN DNA SEQUENCING PUZZLE'.center(46))} {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} Match your sequence to the reference sequence by    {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} swapping base pairs. Each pair must be in the       {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} correct position to decode the alien DNA.           {Font.BOX_SIDE}")
                        print(f"{Font.BOX_BOTTOM}")
                        
                        # Main puzzle loop
                        while attempts < max_attempts:
                            print(f"\n{Font.SUBTITLE('ATTEMPT')} {attempts+1}/{max_attempts}")
                            
                            # Display reference sequence
                            print(f"\n{Font.SYSTEM('REFERENCE SEQUENCE:')}")
                            ref_display = " | ".join(reference_sequence)
                            print(f"{Fore.YELLOW}{ref_display}{Style.RESET_ALL}")
                            
                            # Display player's current sequence
                            print(f"\n{Font.SYSTEM('YOUR SEQUENCE:')}")
                            for i, pair in enumerate(player_sequence):
                                if pair == reference_sequence[i]:
                                    # Correct position
                                    print(f"{i+1}: {Fore.GREEN}{pair}{Style.RESET_ALL}", end="  ")
                                else:
                                    # Incorrect position
                                    print(f"{i+1}: {Fore.RED}{pair}{Style.RESET_ALL}", end="  ")
                            print("\n")
                            
                            # Check if sequences match
                            if player_sequence == reference_sequence:
                                print_typed(f"\n{Font.SUCCESS('SEQUENCE MATCHED! DNA ANALYSIS COMPLETE.')}")
                                return True
                            
                            # Get player input for swapping
                            print_typed(f"\n{Font.SYSTEM('Select a position to swap (1-5), or 0 to shuffle all:')}")
                            try:
                                pos = int(input("> ").strip())
                                if pos == 0:
                                    # Shuffle entire sequence
                                    random.shuffle(player_sequence)
                                elif 1 <= pos <= 5:
                                    # Swap one position
                                    pos -= 1  # Convert to 0-indexed
                                    options = [bp for bp in base_pairs if bp != player_sequence[pos]]
                                    print_typed(f"\n{Font.SYSTEM('Select new base pair for position')} {pos+1}:")
                                    for i, option in enumerate(options):
                                        print(f"{i+1}: {option}")
                                    
                                    swap_choice = int(input("> ").strip())
                                    if 1 <= swap_choice <= len(options):
                                        player_sequence[pos] = options[swap_choice-1]
                                    else:
                                        print_typed(f"\n{Font.WARNING('Invalid selection. No change made.')}")
                                else:
                                    print_typed(f"\n{Font.WARNING('Invalid position. Choose 1-5 or 0.')}")
                            except ValueError:
                                print_typed(f"\n{Font.WARNING('Please enter a number.')}")
                            
                            attempts += 1
                            
                            # Provide a hint after a few failed attempts
                            if attempts == 3:
                                hint_pos = next((i for i, (p, r) in enumerate(zip(player_sequence, reference_sequence)) if p != r), 0)
                                print_typed(f"\n{Font.INFO('HINT: Position')} {hint_pos+1} {Font.INFO('needs attention.')}")
                        
                        # If we reach here, player has used all attempts
                        print_typed(f"\n{Font.WARNING('Maximum attempts reached. Analysis failed.')}")
                        print_typed("The analyzer displays the correct sequence for reference:")
                        print(f"\n{Fore.GREEN}{' | '.join(reference_sequence)}{Style.RESET_ALL}")
                        return False
                    
                    # Run the puzzle
                    analysis_success = dna_sequencing_puzzle()
                    
                    if analysis_success:
                        print_typed("\nThe biological analyzer completes its work, providing")
                        print_typed("unprecedented insight into the Thalassian life forms.")
                        print_typed("\nThe analysis reveals that the creatures have undergone")
                        print_typed("accelerated evolution due to exposure to the unique salt")
                        print_typed("compounds found only on Thalassia 1. More concerning, there")
                        print_typed("appears to be evidence of deliberate genetic modification")
                        print_typed("in several specimens.")
                        
                        print_typed(f"\n{Font.SYSTEM('DOWNLOADING RESEARCH DATA...')}")
                        time.sleep(1)
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Enhanced Thalassian Specimens')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Genetic Modification Records')}")
                        print_typed(f"{Font.SUCCESS('BONUS:')} {Font.ITEM('Research Lab Access Card')}")
                        
                        # Add better rewards for completing the puzzle
                        player.inventory["enhanced_thalassian_specimens"] = player.inventory.get("enhanced_thalassian_specimens", 0) + 1
                        player.inventory["genetic_records"] = player.inventory.get("genetic_records", 0) + 1
                        player.inventory["lab_access_card"] = player.inventory.get("lab_access_card", 0) + 1
                        
                        # Give player extra knowledge for story progression
                        game_state["knows_about_genetic_modifications"] = True
                    else:
                        print_typed("\nDespite the failed analysis, you still manage to collect")
                        print_typed("the specimen container for future study.")
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Thalassian Specimens')}")
                        player.inventory["thalassian_specimens"] = player.inventory.get("thalassian_specimens", 0) + 1
                else:
                    print_typed("\nYou decide not to risk using the analyzer and simply")
                    print_typed("collect the specimen container for study.")
                    
                    print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Thalassian Specimens')}")
                    player.inventory["thalassian_specimens"] = player.inventory.get("thalassian_specimens", 0) + 1
                
                game_state["found_lab_specimens"] = True
            
            # Encounter chance
            if random.random() < 0.4 and not game_state.get("lab_cleared", False):
                # Combat with tentacled creature
                print_typed(f"\n{Font.WARNING('Movement detected in the shadows!')}")
                print_typed("\nA creature emerges from a ventilation duct - resembling an")
                print_typed("Earth bivalve, but with 14 writhing tentacles. Several tentacles")
                print_typed("are wrapped around a damaged laboratory drone, which it appears")
                print_typed("to be controlling through some form of neural interface.")
                
                # Create the enemy
                enemy = Character("Neurovore Controller", 120, 22, 15)
                enemy.resistances = {
                    "physical": 0.2,
                    "energy": 0.1,
                    "sonic": -0.6,  # Weakness to sound
                    "thermal": 0.3,
                    "bio": 0.4
                }
                enemy.abilities = ["Neural Interface", "Tentacle Whip", "Sonic Sensitivity"]
                enemy.inventory = {"salt_crystal": 2}
                
                # Start combat
                combat_result = combat(player, enemy)
                
                if combat_result:
                    print_typed(f"\n{Font.SUCCESS('You defeat the creature and its drone!')}")
                    game_state["lab_cleared"] = True
                    
                    # Chance to find research notes
                    if random.random() < 0.7:
                        print_typed("\nAfter the battle, you find a data pad that survived the")
                        print_typed("chaos. It contains research notes on the Neurovore species.")
                        
                        print_typed(f"\n{Font.INFO('NEUROVORE RESEARCH NOTES:')}")
                        print_typed("• Species possesses no conventional eyes")
                        print_typed("• Highly sensitive to sound vibrations")
                        print_typed("• Tentacles contain specialized neural connectors")
                        print_typed("• Can interface with and control electronic systems")
                        print_typed("• Specimen count correlates with control capability")
                        print_typed("• CRITICAL: High-frequency sonic pulses disrupt neural function")
                    
                        print_typed(f"\n{Font.SUCCESS('Research notes added to database.')}")
                    
            # Wait for user to continue
            input("\nPress Enter to return to the main area...")
            
        elif choice == "2":
            # Crew Quarters
            clear_screen()
            print_typed(f"\n{Font.HEADER('CREW QUARTERS')}")
            
            print_typed("\nThe crew's living area is in better condition than the")
            print_typed("laboratory, though signs of hasty evacuation are everywhere.")
            print_typed("Personal belongings lay scattered about, and some quarters")
            print_typed("appear to have been barricaded from the inside.")
            
            # Personal logs
            if not game_state.get("found_personal_logs", False):
                print_typed("\nA functional data terminal catches your eye. Activating it")
                print_typed("reveals several personal logs from the facility's staff.")
                
                print_typed(f"\n{Font.INFO('DR. ELENA MARKOV - CHIEF RESEARCHER')}")
                print_typed("Day 189: The indigenous life forms continue to display remarkable")
                print_typed("adaptability. The bivalve-like specimens we've named 'Neurovores'")
                print_typed("show signs of rudimentary intelligence and an uncanny ability to")
                print_typed("interface with our electronics. I've requested additional ")
                print_typed("containment protocols.")
                
                print_typed(f"\n{Font.INFO('SECURITY CHIEF TORRES - FINAL LOG')}")
                print_typed("We've lost control of section E. These things are getting into")
                print_typed("the systems somehow. Larger specimens have more tentacles and")
                print_typed("seem able to control multiple devices simultaneously. We're")
                print_typed("evacuating to the surface outpost. God help anyone who stays behind.")
                
                print_typed(f"\n{Font.SUCCESS('Personal logs downloaded to your database.')}")
                game_state["found_personal_logs"] = True
                
            # Find supplies
            if not game_state.get("found_crew_supplies", False):
                print_typed("\nSearching through the quarters, you find a sealed emergency kit")
                print_typed("that was overlooked during the evacuation.")
                
                print_typed(f"\n{Font.SUCCESS('You obtain:')}")
                print_typed("• 2 Advanced Med-Kits")
                print_typed("• Emergency Beacon (damaged)")
                print_typed("• Pressure Suit Patch Kit")
                
                player.inventory["med_kit"] = player.inventory.get("med_kit", 0) + 2
                player.inventory["pressure_patch"] = player.inventory.get("pressure_patch", 0) + 1
                player.inventory["damaged_beacon"] = player.inventory.get("damaged_beacon", 0) + 1
                
                game_state["found_crew_supplies"] = True
            
            # Wait for user to continue
            input("\nPress Enter to return to the main area...")
            
        elif choice == "3":
            # Weapons Research Wing
            clear_screen()
            print_typed(f"\n{Font.HEADER('WEAPONS RESEARCH WING')}")
            
            print_typed("\nThe weapons research section shows signs of a desperate last stand.")
            print_typed("Makeshift barricades block the entrance, and scorch marks from")
            print_typed("energy weapons line the walls. Beyond the barricades, several")
            print_typed("research stations contain prototype weaponry in various states")
            print_typed("of assembly.")
            
            # Sound weapon module discovery with calibration puzzle
            if not game_state.get("found_sonic_module", False):
                print_typed("\nIn a sealed weapons locker, you discover an intact prototype")
                print_typed("weapon module. The schematics indicate it's designed to emit")
                print_typed("focused sonic pulses that can disrupt neural networks and")
                print_typed("communication systems. However, the module appears to be in")
                print_typed("standby mode and requires proper calibration before use.")
                
                print_typed(f"\n{Font.WEAPON('SONIC DISRUPTOR MODULE')}")
                print_typed("Prototype weapon designed specifically to counter the Neurovore")
                print_typed("threat. Emits concentrated sound waves at frequencies that")
                print_typed("overwhelm the creatures' sensitive audio receptors while")
                print_typed("disrupting their neural control capabilities.")
                
                print_typed(f"\n{Font.SYSTEM('WEAPON REQUIRES CALIBRATION')}")
                print_typed("The weapon's frequency modulator needs to be calibrated to")
                print_typed("the correct settings to effectively target Neurovore neural")
                print_typed("pathways. Improper calibration could render the weapon ineffective")
                print_typed("or potentially dangerous to the wielder.")
                
                print_typed("\nAttempt to calibrate the Sonic Disruptor? (y/n)")
                calibrate_choice = input("\n> ").strip().lower()
                
                if calibrate_choice == 'y':
                    # Weapon Calibration Puzzle
                    def weapon_calibration_puzzle():
                        """
                        A puzzle where the player must calibrate the sonic weapon 
                        by adjusting multiple parameters to find the optimal configuration.
                        """
                        clear_screen()
                        print_typed(f"\n{Font.HEADER('SONIC DISRUPTOR CALIBRATION SYSTEM')}")
                        
                        print(f"\n{Font.BOX_TOP}")
                        print(f"{Font.BOX_SIDE} {Font.TITLE('SONIC WEAPON CALIBRATION'.center(46))} {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} Calibrate weapon systems to achieve optimal output    {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} by setting all parameters to their correct values.    {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} All three parameters must match target values.        {Font.BOX_SIDE}")
                        print(f"{Font.BOX_BOTTOM}")
                        
                        # Generate target values (1-10 range for each parameter)
                        target_frequency = random.randint(4, 8)
                        target_amplitude = random.randint(3, 7)
                        target_modulation = random.randint(5, 9)
                        
                        # Starting values
                        current_frequency = 5
                        current_amplitude = 5
                        current_modulation = 5
                        
                        attempts = 0
                        max_attempts = 7
                        
                        while attempts < max_attempts:
                            clear_screen()
                            print_typed(f"\n{Font.HEADER('SONIC DISRUPTOR CALIBRATION')}")
                            
                            # Display attempt counter
                            print(f"\n{Font.SUBTITLE('CALIBRATION ATTEMPT')} {attempts+1}/{max_attempts}")
                            
                            # Calculate weapon effectiveness based on parameter proximity
                            freq_diff = abs(current_frequency - target_frequency)
                            amp_diff = abs(current_amplitude - target_amplitude)
                            mod_diff = abs(current_modulation - target_modulation)
                            
                            total_diff = freq_diff + amp_diff + mod_diff
                            effectiveness = max(0, 100 - (total_diff * 10))
                            
                            # Visual representation of current settings
                            print(f"\n{Font.SYSTEM('CURRENT CONFIGURATION:')}")
                            
                            # Frequency setting with visualization
                            freq_bar = "▁" * (current_frequency - 1) + "▓" + "▁" * (10 - current_frequency)
                            freq_hint = "↑" if current_frequency < target_frequency else "↓" if current_frequency > target_frequency else "✓"
                            freq_color = Fore.GREEN if freq_diff == 0 else (Fore.YELLOW if freq_diff <= 2 else Fore.RED)
                            
                            print(f"1. FREQUENCY:  [{freq_color}{freq_bar}{Style.RESET_ALL}] {current_frequency}/10 {freq_color}{freq_hint}{Style.RESET_ALL}")
                            
                            # Amplitude setting with visualization
                            amp_bar = "▁" * (current_amplitude - 1) + "▓" + "▁" * (10 - current_amplitude)
                            amp_hint = "↑" if current_amplitude < target_amplitude else "↓" if current_amplitude > target_amplitude else "✓"
                            amp_color = Fore.GREEN if amp_diff == 0 else (Fore.YELLOW if amp_diff <= 2 else Fore.RED)
                            
                            print(f"2. AMPLITUDE:  [{amp_color}{amp_bar}{Style.RESET_ALL}] {current_amplitude}/10 {amp_color}{amp_hint}{Style.RESET_ALL}")
                            
                            # Modulation setting with visualization
                            mod_bar = "▁" * (current_modulation - 1) + "▓" + "▁" * (10 - current_modulation)
                            mod_hint = "↑" if current_modulation < target_modulation else "↓" if current_modulation > target_modulation else "✓"
                            mod_color = Fore.GREEN if mod_diff == 0 else (Fore.YELLOW if mod_diff <= 2 else Fore.RED)
                            
                            print(f"3. MODULATION: [{mod_color}{mod_bar}{Style.RESET_ALL}] {current_modulation}/10 {mod_color}{mod_hint}{Style.RESET_ALL}")
                            
                            # Display weapon effectiveness
                            effect_color = Fore.GREEN if effectiveness >= 80 else (Fore.YELLOW if effectiveness >= 50 else Fore.RED)
                            effect_bar = "█" * (effectiveness // 10) + "▒" * (10 - (effectiveness // 10))
                            
                            print(f"\n{Font.SYSTEM('WEAPON EFFECTIVENESS:')}")
                            print(f"{effect_color}{effect_bar} {effectiveness}%{Style.RESET_ALL}")
                            
                            # Status messages based on effectiveness
                            if effectiveness >= 90:
                                print(f"{Font.SUCCESS('OPTIMAL CALIBRATION ACHIEVED')}")
                            elif effectiveness >= 80:
                                print(f"{Font.SUCCESS('NEAR-OPTIMAL CALIBRATION')}")
                            elif effectiveness >= 50:
                                print(f"{Font.WARNING('SUB-OPTIMAL CALIBRATION')}")
                            else:
                                print(f"{Font.WARNING('CRITICAL CALIBRATION FAILURE')}")
                            
                            # Neurovore response simulation based on current settings
                            if effectiveness >= 90:
                                print(f"\n{Font.SYSTEM('NEUROVORE RESPONSE SIMULATION:')}")
                                print(f"{Fore.GREEN}Complete neural disruption. Multiple specimens incapacitated.{Style.RESET_ALL}")
                            elif effectiveness >= 70:
                                print(f"\n{Font.SYSTEM('NEUROVORE RESPONSE SIMULATION:')}")
                                print(f"{Fore.YELLOW}Partial neural disruption. Specimen movement impaired.{Style.RESET_ALL}")
                            elif effectiveness >= 40:
                                print(f"\n{Font.SYSTEM('NEUROVORE RESPONSE SIMULATION:')}")
                                print(f"{Fore.RED}Minimal effect. Specimens show temporary disorientation only.{Style.RESET_ALL}")
                            
                            # Check if all parameters match
                            if freq_diff == 0 and amp_diff == 0 and mod_diff == 0:
                                print_typed(f"\n{Font.SUCCESS('PERFECT CALIBRATION ACHIEVED!')}")
                                
                                # Animation for successful calibration
                                print_typed(f"\n{Font.SYSTEM('INITIALIZING WEAPON SYSTEMS...')}")
                                for i in range(5):
                                    print(f"\r{Font.SYSTEM('Charging: ')} {Fore.CYAN}{'■' * i + '□' * (5-i)} {i*20}%{Style.RESET_ALL}", end="", flush=True)
                                    time.sleep(0.3)
                                print("\n")
                                
                                return True
                            
                            # Get player input for parameter adjustment
                            print_typed(f"\n{Font.SYSTEM('Select parameter to adjust (1-3):')}")
                            try:
                                param_choice = int(input("> ").strip())
                                
                                if 1 <= param_choice <= 3:
                                    print_typed(f"\n{Font.SYSTEM('Enter new value (1-10):')}")
                                    new_value = int(input("> ").strip())
                                    
                                    if 1 <= new_value <= 10:
                                        if param_choice == 1:
                                            current_frequency = new_value
                                        elif param_choice == 2:
                                            current_amplitude = new_value
                                        else:
                                            current_modulation = new_value
                                    else:
                                        print_typed(f"\n{Font.WARNING('Invalid value. Range is 1-10.')}")
                                        time.sleep(1)
                                else:
                                    print_typed(f"\n{Font.WARNING('Invalid selection. Choose 1-3.')}")
                                    time.sleep(1)
                            except ValueError:
                                print_typed(f"\n{Font.WARNING('Please enter a valid number.')}")
                                time.sleep(1)
                            
                            attempts += 1
                            
                            # Give a hint after several attempts
                            if attempts == 4:
                                # Find the parameter furthest from target
                                diffs = [
                                    ("frequency", freq_diff),
                                    ("amplitude", amp_diff),
                                    ("modulation", mod_diff)
                                ]
                                
                                max_diff_param = max(diffs, key=lambda x: x[1])
                                
                                if max_diff_param[1] > 0:
                                    print_typed(f"\n{Font.INFO('HINT: The')} {max_diff_param[0]} {Font.INFO('parameter requires significant adjustment.')}")
                                    time.sleep(2)
                        
                        # If we get here, calibration failed
                        print_typed(f"\n{Font.WARNING('MAXIMUM CALIBRATION ATTEMPTS REACHED')}")
                        print_typed(f"\n{Font.SYSTEM('OPTIMAL SETTINGS WERE:')}")
                        print(f"FREQUENCY: {target_frequency}/10")
                        print(f"AMPLITUDE: {target_amplitude}/10")
                        print(f"MODULATION: {target_modulation}/10")
                        
                        time.sleep(1)
                        return False
                    
                    # Run the calibration puzzle
                    calibration_success = weapon_calibration_puzzle()
                    
                    # Add to weapon modules based on calibration result
                    weapon_modules = game_state.get("weapon_modules", {})
                    
                    if calibration_success:
                        # Optimal calibration provides enhanced weapon
                        print_typed("\nWith precise calibration, the Sonic Disruptor hums with")
                        print_typed("power, its internal systems perfectly aligned to target")
                        print_typed("the unique neural patterns of Thalassian lifeforms.")
                        
                        weapon_modules["sonic_disruptor"] = {
                            "name": "Optimized Sonic Disruptor",
                            "description": "Perfectly calibrated sonic weapon that targets Neurovore neural pathways",
                            "damage": 40,  # Enhanced damage
                            "damage_type": "sonic",
                            "equipped": False,
                            "special_effect": "Optimized neural disruption, 95% effective against Neurovores"
                        }
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Optimized Sonic Disruptor Module')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Sonic Calibration Schematics')}")
                        print_typed(f"{Font.SUCCESS('BONUS:')} {Font.ITEM('Neural Disruption Field Generator')}")
                        
                        # Add bonus items for perfect calibration
                        player.inventory["calibration_schematics"] = player.inventory.get("calibration_schematics", 0) + 1
                        player.inventory["disruption_field_generator"] = player.inventory.get("disruption_field_generator", 0) + 1
                    else:
                        # Partially functional weapon for failed calibration
                        print_typed("\nDespite failing to achieve optimal calibration, you manage")
                        print_typed("to configure the Sonic Disruptor into a functional state.")
                        print_typed("It won't be as effective against the Neurovores, but should")
                        print_typed("still provide some advantage in combat.")
                        
                        weapon_modules["sonic_disruptor"] = {
                            "name": "Sonic Disruptor",
                            "description": "Partially calibrated sonic weapon with reduced effectiveness",
                            "damage": 25,  # Reduced damage
                            "damage_type": "sonic",
                            "equipped": False,
                            "special_effect": "Basic neural disruption, 60% effective against Neurovores"
                        }
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Sonic Disruptor Module')}")
                        print_typed(f"{Font.INFO('Sub-optimal calibration detected. Weapon effectiveness reduced.')}")
                    
                    game_state["weapon_modules"] = weapon_modules
                    game_state["found_sonic_module"] = True
                    
                    print_typed(f"\n{Font.INFO('Use Weapon Module Management to equip it.')}")
                    
                    # Mark area as cleared
                    game_state["weapons_wing_cleared"] = True
                else:
                    # Player chose not to calibrate
                    print_typed("\nYou decide to take the weapon module as-is, planning to")
                    print_typed("calibrate it later when you have more time and resources.")
                    
                    # Add basic uncalibrated weapon
                    weapon_modules = game_state.get("weapon_modules", {})
                    weapon_modules["sonic_disruptor"] = {
                        "name": "Uncalibrated Sonic Disruptor",
                        "description": "Uncalibrated sonic weapon with minimal effectiveness",
                        "damage": 20,
                        "damage_type": "sonic",
                        "equipped": False,
                        "special_effect": "Minimal neural disruption, 40% effective against Neurovores"
                    }
                    
                    game_state["weapon_modules"] = weapon_modules
                    game_state["found_sonic_module"] = True
                    
                    print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Uncalibrated Sonic Disruptor Module')}")
                    print_typed(f"{Font.WARNING('Weapon requires calibration for optimal performance.')}")
                    print_typed(f"{Font.INFO('Use Weapon Module Management to equip it.')}")
                    
                    game_state["weapons_wing_cleared"] = True
            
            # Dangerous encounter if not yet cleared
            elif not game_state.get("weapons_wing_cleared", False):
                print_typed(f"\n{Font.WARNING('Multiple life signs detected!')}")
                print_typed("\nAs you move deeper into the weapons wing, the lights flicker")
                print_typed("ominously. Suddenly, multiple shapes emerge from the shadows -")
                print_typed("three Neurovores, each with over 20 tentacles, have fused together")
                print_typed("into a horrific mass. They've taken control of a security mech")
                print_typed("and several smaller drones.")
                
                # Create powerful enemy
                enemy = Character("Neurovore Collective", 200, 30, 25)
                enemy.resistances = {
                    "physical": 0.3,
                    "energy": 0.2,
                    "sonic": -0.8,  # Major weakness to sound
                    "thermal": 0.1,
                    "bio": 0.4
                }
                enemy.abilities = ["Neural Dominance", "Drone Swarm", "Tentacle Barrage"]
                enemy.inventory = {"salt_crystal": 5, "neural_interface": 1}
                
                # Start combat
                combat_result = combat(player, enemy)
                
                if combat_result:
                    print_typed(f"\n{Font.SUCCESS('You defeat the nightmarish collective!')}")
                    game_state["weapons_wing_cleared"] = True
                    
                    # Reward for defeating tough enemy
                    print_typed("\nWith the threat eliminated, you're able to scavenge the remains")
                    print_typed("of the security mech. Among the components, you find a prototype")
                    print_typed("energy modulator that might be useful for repairs.")
                    
                    player.inventory["energy_modulator"] = player.inventory.get("energy_modulator", 0) + 1
                    print_typed(f"\n{Font.SUCCESS('Energy Modulator added to inventory.')}")
            else:
                print_typed("\nThe weapons wing remains clear of threats, though the eerie")
                print_typed("silence is occasionally broken by the dripping of water and")
                print_typed("the settling of the structure under immense pressure.")
            
            # Wait for user to continue
            input("\nPress Enter to return to the main area...")
            
        elif choice == "4":
            # Communications Center
            clear_screen()
            print_typed(f"\n{Font.HEADER('COMMUNICATIONS CENTER')}")
            
            print_typed("\nThe communications center is partially flooded, with water")
            print_typed("reaching knee height. Much of the equipment is damaged beyond")
            print_typed("repair, though a few terminals still function on emergency power.")
            
            # Research data
            if not game_state.get("found_research_data", False):
                print_typed("\nAccessing one of the working terminals, you discover encrypted")
                print_typed("research data that was prepared for transmission to Earth before")
                print_typed("the facility was compromised.")
                
                print_typed(f"\n{Font.INFO('RESEARCH SUMMARY:')}")
                print_typed("• Confirmed 137 unique aquatic species")
                print_typed("• All native life uses salt-based structural components")
                print_typed("• Salt formations serve as both skeleton and armor")
                print_typed("• Toxins produced as byproduct of salt metabolism")
                print_typed("• Advanced species show sound-based communication")
                print_typed("• Some specimens demonstrate previously unknown interface capability")
                print_typed("• WARNING: Several specimens escaped containment")
                
                print_typed(f"\n{Font.INFO('WEAPONS RESEARCH ADDENDUM:')}")
                print_typed("Prototype sonic disruptor shows promise against native life forms.")
                print_typed("High-frequency sound patterns disrupt neural pathways and salt")
                print_typed("formation. Recommend immediate production for facility security.")
                
                print_typed(f"\n{Font.SUCCESS('Research data downloaded to your database.')}")
                game_state["found_research_data"] = True
            
            # Distress Signal Detection - new puzzle addition
            if not game_state.get("found_distress_signal", False):
                print_typed("\nAs you navigate through the damaged communications equipment,")
                print_typed("your scanner detects a weak signal being received on an emergency")
                print_typed("frequency. The signal is heavily corrupted by interference and")
                print_typed("degradation of the facility's systems.")
                
                # Visual effect of signal detection
                print("\n")
                for i in range(3):
                    print(f"\r{Font.SYSTEM('SIGNAL DETECTED:')} {Fore.CYAN}{'▓▒░' * i}{Style.RESET_ALL}", end="", flush=True)
                    # Audio effect replaced with visual pause
                    time.sleep(0.5)
                print("\n")
                
                print_typed(f"\n{Font.SYSTEM('SIGNAL ANALYSIS:')}")
                print_typed(f"{Font.INFO('Origin: Unknown surface location on Thalassia 1')}")
                print_typed(f"{Font.INFO('Type: Emergency distress beacon')}")
                print_typed(f"{Font.INFO('Status: Degraded - 87% data corruption')}")
                print_typed(f"{Font.INFO('Time since broadcast: Approximately 47 days')}")
                
                print_typed("\nAttempt to decrypt and reconstruct the distress signal? (y/n)")
                decrypt_choice = input("\n> ").strip().lower()
                
                if decrypt_choice == 'y':
                    # Signal Decryption Puzzle
                    def signal_reconstruction_puzzle():
                        """
                        A puzzle where the player must reconstruct a corrupted distress signal
                        by correctly identifying signal patterns and filtering out noise.
                        """
                        clear_screen()
                        print_typed(f"\n{Font.HEADER('SIGNAL RECONSTRUCTION INTERFACE')}")
                        
                        print(f"\n{Font.BOX_TOP}")
                        print(f"{Font.BOX_SIDE} {Font.TITLE('DISTRESS SIGNAL RECONSTRUCTION'.center(46))} {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} Reconstruct the corrupted signal by selecting the      {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} correct signal pattern from noise. Find the pattern    {Font.BOX_SIDE}")
                        print(f"{Font.BOX_SIDE} that appears most frequently in each segment.          {Font.BOX_SIDE}")
                        print(f"{Font.BOX_BOTTOM}")
                        
                        # Puzzle setup - need to complete 3 segments
                        segments_completed = 0
                        max_segments = 3
                        max_attempts_per_segment = 3
                        
                        while segments_completed < max_segments:
                            # Generate signal patterns for this segment
                            correct_pattern = random.choice(["▁▂▃▄▅▄▃▂▁", "▂▁▃▂▅▂▃▁▂", "▃▂▁▅▄▅▁▂▃"])
                            noise_patterns = [
                                "▅▂▁▃▂▄▁▅▃", 
                                "▁▅▂▃▁▂▅▃▄", 
                                "▄▃▁▂▅▃▂▁▄"
                            ]
                            
                            # Make sure correct pattern is not in noise patterns
                            while correct_pattern in noise_patterns:
                                correct_pattern = random.choice(["▁▂▃▄▅▄▃▂▁", "▂▁▃▂▅▂▃▁▂", "▃▂▁▅▄▅▁▂▃"])
                            
                            # Display segment information
                            print_typed(f"\n{Font.SUBTITLE(f'SIGNAL SEGMENT {segments_completed+1}/{max_segments}')}")
                            print_typed(f"{Font.INFO('Attempts remaining:')} {max_attempts_per_segment}")
                            
                            # Generate signal display with correct pattern repeated but hidden among noise
                            signal_display = []
                            correct_positions = []
                            
                            # Create a signal with the correct pattern appearing multiple times
                            for i in range(10):
                                if random.random() < 0.4:  # 40% chance of correct pattern
                                    signal_display.append((correct_pattern, True))
                                    correct_positions.append(i)
                                else:
                                    signal_display.append((random.choice(noise_patterns), False))
                            
                            # Display the combined signal
                            print_typed(f"\n{Font.SYSTEM('ANALYZING SIGNAL SEGMENT:')}")
                            print("\n" + "-" * 80)
                            for i, (pattern, _) in enumerate(signal_display):
                                print(f"{i+1}: {Fore.CYAN}{pattern}{Style.RESET_ALL}")
                            print("-" * 80)
                            
                            print_typed(f"\n{Font.SYSTEM('Which pattern represents the true signal? (1-10)')}")
                            print_typed(f"{Font.INFO('The true signal appears multiple times in the segment.')}")
                            
                            # Player gets multiple attempts per segment
                            segment_success = False
                            attempts = 0
                            
                            while attempts < max_attempts_per_segment and not segment_success:
                                try:
                                    choice = int(input("\n> ").strip())
                                    if 1 <= choice <= 10:
                                        if choice-1 in correct_positions:
                                            print_typed(f"\n{Font.SUCCESS('CORRECT PATTERN IDENTIFIED!')}")
                                            
                                            # Visual confirmation
                                            for i, (pattern, is_correct) in enumerate(signal_display):
                                                if i+1 == choice or is_correct:
                                                    print(f"{i+1}: {Fore.GREEN}{pattern}{Style.RESET_ALL} ✓")
                                                else:
                                                    print(f"{i+1}: {Fore.RED}{pattern}{Style.RESET_ALL}")
                                            
                                            segment_success = True
                                        else:
                                            attempts += 1
                                            if attempts < max_attempts_per_segment:
                                                print_typed(f"\n{Font.WARNING('INCORRECT PATTERN. Attempts remaining:')} {max_attempts_per_segment - attempts}")
                                                
                                                # Provide hint after failed attempts
                                                if attempts == 2:
                                                    hint_position = random.choice(correct_positions) + 1
                                                    print_typed(f"\n{Font.INFO('HINT: One of the true signal patterns appears at position')} {hint_position}")
                                            else:
                                                print_typed(f"\n{Font.WARNING('SEGMENT RECONSTRUCTION FAILED.')}")
                                                
                                                # Show correct patterns
                                                print_typed(f"\n{Font.SYSTEM('TRUE SIGNAL PATTERNS:')}")
                                                for i, (pattern, is_correct) in enumerate(signal_display):
                                                    if is_correct:
                                                        print(f"{i+1}: {Fore.GREEN}{pattern}{Style.RESET_ALL} ✓")
                                    else:
                                        print_typed(f"\n{Font.WARNING('Invalid selection. Choose 1-10.')}")
                                except ValueError:
                                    print_typed(f"\n{Font.WARNING('Please enter a valid number.')}")
                            
                            # After segment attempt is complete
                            if segment_success:
                                segments_completed += 1
                                if segments_completed < max_segments:
                                    print_typed(f"\n{Font.SUCCESS(f'SEGMENT {segments_completed}/{max_segments} RECONSTRUCTED!')}")
                                    print_typed(f"\n{Font.SYSTEM('PROCEEDING TO NEXT SEGMENT...')}")
                                    time.sleep(1.5)
                                    clear_screen()
                                    print_typed(f"\n{Font.HEADER('SIGNAL RECONSTRUCTION INTERFACE')}")
                            else:
                                # Failed this segment
                                print_typed(f"\n{Font.WARNING('SEGMENT RECONSTRUCTION FAILED. ABORTING PROCESS.')}")
                                return False
                        
                        # If we got here, all segments completed successfully
                        print_typed(f"\n{Font.SUCCESS('ALL SEGMENTS RECONSTRUCTED SUCCESSFULLY!')}")
                        print_typed(f"\n{Font.SYSTEM('PROCESSING COMPLETE SIGNAL...')}")
                        
                        # Animation of signal processing
                        for i in range(10):
                            progress = "█" * i + "▒" * (10-i)
                            print(f"\r{Font.INFO('Processing:')} {Fore.CYAN}{progress} {i*10}%{Style.RESET_ALL}", end="", flush=True)
                            time.sleep(0.2)
                        print("\n")
                        
                        return True
                    
                    # Run the puzzle
                    reconstruction_success = signal_reconstruction_puzzle()
                    
                    if reconstruction_success:
                        # Display reconstructed message dramatically
                        clear_screen()
                        print_typed(f"\n{Font.HEADER('DISTRESS SIGNAL RECONSTRUCTED')}")
                        time.sleep(0.7)
                        
                        print_typed(f"\n{Font.SYSTEM('PLAYBACK INITIATED:')}")
                        time.sleep(1)
                        
                        # Play back the message with special formatting
                        print_typed(f"\n{Fore.CYAN}This is Dr. Elena Markov, lead researcher of Thalassia Station Alpha.{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}All survivors have been evacuated to the surface outpost following{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}catastrophic containment failure in the underwater research facility.{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}The creatures have followed us to the surface. Our security measures{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}are failing. We've initiated the facility self-destruct sequence,{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}but I fear it won't be enough to contain them...{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.8)
                        print_typed(f"{Fore.CYAN}There's something here we didn't anticipate... it's intelligent...{Style.RESET_ALL}", delay=0.04)
                        time.sleep(0.5)
                        print_typed(f"{Fore.CYAN}and it's controlling them all. May God help us... and forgive us.{Style.RESET_ALL}", delay=0.04)
                        time.sleep(1)
                        
                        print_typed(f"\n{Font.SYSTEM('COORDINATES EMBEDDED IN SIGNAL')}")
                        time.sleep(0.5)
                        
                        # Rewards for completing the puzzle
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Surface Outpost Coordinates')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Dr. Markov Message')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Facility Self-Destruct Codes')}")
                        
                        player.inventory["outpost_coordinates"] = player.inventory.get("outpost_coordinates", 0) + 1
                        player.inventory["markov_message"] = player.inventory.get("markov_message", 0) + 1
                        player.inventory["destruct_codes"] = player.inventory.get("destruct_codes", 0) + 1
                        
                        # Add important story flags
                        game_state["found_distress_signal"] = True
                        game_state["knows_surface_outpost_location"] = True
                        game_state["knows_about_intelligent_entity"] = True
                    else:
                        # Partial reconstruction result
                        print_typed("\nDespite your best efforts, you could only partially reconstruct")
                        print_typed("the distress signal. The message remains largely fragmented,")
                        print_typed("but you manage to extract some critical information:")
                        
                        print_typed(f"\n{Font.SYSTEM('...this is Dr. Elena Markov... Thalassia Station...')}")
                        print_typed(f"{Font.SYSTEM('...evacuated to surface outpost... containment failure...')}")
                        print_typed(f"{Font.SYSTEM('...creatures followed... security failing...')}")
                        
                        print_typed("\nThe coordinates are too corrupted to pinpoint the exact location")
                        print_typed("of the surface outpost, but you can determine its approximate area.")
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Partial Outpost Coordinates')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Fragmented Distress Message')}")
                        
                        player.inventory["partial_coordinates"] = player.inventory.get("partial_coordinates", 0) + 1
                        player.inventory["fragmented_message"] = player.inventory.get("fragmented_message", 0) + 1
                        
                        # Add basic story flags
                        game_state["found_distress_signal"] = True
                        game_state["has_approximate_outpost_location"] = True
                else:
                    print_typed("\nYou decide not to attempt signal reconstruction for now,")
                    print_typed("noting its location in your database for potential future analysis.")
                    
                    # Player still learns something
                    print_typed("\nBefore moving on, you notice the signal appears to originate")
                    print_typed("from somewhere on the planet's surface - possibly a secondary")
                    print_typed("facility or outpost.")
                    
                    game_state["knows_about_surface_outpost"] = True
            
            # Emergency beacon repair - enhanced with visual feedback
            if "damaged_beacon" in player.inventory and not game_state.get("repaired_beacon", False):
                print_typed("\nYou remember the damaged emergency beacon you found earlier.")
                print_typed("Using the communications equipment here, you might be able")
                print_typed("to repair it.")
                
                print_typed("\nAttempt to repair the emergency beacon? (y/n)")
                repair_choice = input("\n> ").strip().lower()
                
                if repair_choice == 'y' or repair_choice == 'yes':
                    print_typed("\nYou carefully disassemble the damaged beacon and integrate")
                    print_typed("components from the communication center's equipment.")
                    
                    # Visual repair process
                    print_typed(f"\n{Font.SYSTEM('BEACON REPAIR PROCESS:')}")
                    repair_steps = [
                        "Diagnosing circuit damage...",
                        "Replacing broken components...",
                        "Recalibrating transmission frequency...",
                        "Testing power connection...",
                        "Verifying signal output..."
                    ]
                    
                    for step in repair_steps:
                        print(f"\r{Font.INFO(step)}", end="", flush=True)
                        time.sleep(0.8)
                        print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
                    
                    # Skill check with better visual feedback
                    success_chance = 0.7  # 70% base chance
                    if "energy_modulator" in player.inventory:
                        success_chance += 0.2  # +20% with energy modulator
                        print_typed("\nThe energy modulator you found proves invaluable for")
                        print_typed("calibrating the beacon's power systems.")
                        print_typed(f"\n{Font.SUCCESS('Repair chance increased!')} ({int(success_chance*100)}%)")
                    
                    print_typed(f"\n{Font.SYSTEM('FINAL DIAGNOSTICS RUNNING...')}")
                    time.sleep(1)
                    
                    if random.random() < success_chance:
                        print_typed(f"\n{Font.SUCCESS('REPAIR SUCCESSFUL!')}")
                        
                        # Animated success sequence
                        for i in range(3):
                            print(f"\r{Font.SYSTEM('Beacon Status: ')} {Fore.GREEN}{'■' * i}{Style.RESET_ALL}", end="", flush=True)
                            time.sleep(0.3)
                            print(f"\r{Font.SYSTEM('Beacon Status: ')} {Fore.GREEN}{'□' * i}{Style.RESET_ALL}", end="", flush=True)
                            time.sleep(0.3)
                        print(f"\r{Font.SYSTEM('Beacon Status: ')} {Fore.GREEN}OPERATIONAL{Style.RESET_ALL}")
                        
                        player.inventory.pop("damaged_beacon", None)
                        player.inventory["emergency_beacon"] = player.inventory.get("emergency_beacon", 0) + 1
                        game_state["repaired_beacon"] = True
                        
                        # Add hint for escape plan
                        print_typed("\nWith this beacon, you could potentially signal any nearby")
                        print_typed("human vessels or installations. This might be your ticket")
                        print_typed("off Thalassia 1 if your ship proves unrepairable.")
                        
                        print_typed(f"\n{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Functional Emergency Beacon')}")
                        print_typed(f"{Font.SUCCESS('ACQUIRED:')} {Font.ITEM('Emergency Broadcast Protocols')}")
                        
                        # Bonus for having the energy modulator
                        if "energy_modulator" in player.inventory:
                            print_typed("\nThanks to the energy modulator, you were able to enhance")
                            print_typed("the beacon's signal strength beyond its original specifications.")
                            print_typed(f"\n{Font.SUCCESS('BONUS:')} {Font.ITEM('Enhanced Signal Range')}")
                            game_state["enhanced_beacon"] = True
                    else:
                        print_typed(f"\n{Font.WARNING('REPAIR ATTEMPT FAILED')}")
                        
                        # Visual failure sequence
                        print(f"\r{Font.SYSTEM('Beacon Status: ')} {Fore.RED}ERROR{Style.RESET_ALL}")
                        time.sleep(0.5)
                        print(f"\r{Font.SYSTEM('Diagnostics: ')} {Fore.RED}Critical component failure{Style.RESET_ALL}")
                        
                        print_typed("\nThe beacon's primary transmission circuit is beyond repair.")
                        print_typed("You might need additional components or technical data to")
                        print_typed("successfully restore functionality.")
            
            # Wait for user to continue
            input("\nPress Enter to return to the main area...")
            
        elif choice == "5" and (game_state.get("lab_cleared", False) and 
            game_state.get("weapons_wing_cleared", False) and
            game_state.get("found_sonic_module", False) and
            not game_state.get("neurovore_prime_defeated", False)):
            # Descend to Lower Level - trigger boss fight
            exploring = False  # Exit exploration loop
            boss_result = fight_neurovore_prime(player, game_state)
            
            # Return to base exploration after boss fight (if survived)
            if boss_result:
                print_typed("\nYou return to the upper levels of the facility, the threat")
                print_typed("of the Neurovore Prime now eliminated. The facility feels")
                print_typed("different - quieter, as if a malevolent presence has lifted.")
                input("\nPress Enter to continue...")
                return explore_underwater_research_base(player, game_state)
            
        elif choice == "5" or (choice == "6" and (game_state.get("lab_cleared", False) and 
            game_state.get("weapons_wing_cleared", False) and
            game_state.get("found_sonic_module", False) and
            not game_state.get("neurovore_prime_defeated", False))):
            # Return to submersible
            print_typed("\nYou return to your submersible and seal the airlock.")
            exploring = False
            
        else:
            print_typed(f"\n{Font.WARNING('Invalid choice. Please try again.')}")
            time.sleep(1)
    
    return


def fight_neurovore_prime(player, game_state):
    """Special boss fight against the Neurovore Prime in the deepest section of the research base
    
    Args:
        player: The player character
        game_state: The current game state
        
    Returns:
        bool: True if the boss was defeated, False otherwise
    """
    clear_screen()
    print_slow("=" * 60)
    print_glitch("ANOMALOUS LIFE FORM DETECTED".center(60))
    print_slow("=" * 60)
    
    print_typed("\nAs you venture into the flooded lower level of the research")
    print_typed("facility, your scanner begins to register an enormous bio-signature.")
    print_typed("The signal emanates from behind a massive pressure door marked")
    print_typed("'CONTAINMENT CHAMBER ALPHA - AUTHORIZED PERSONNEL ONLY'.")
    
    print_typed(f"\n{Font.WARNING('WARNING: CONTAINMENT BREACH DETECTED')}")
    print_typed(f"{Font.WARNING('EXTREME CAUTION ADVISED')}")
    
    time.sleep(1)
    
    print_typed("\nThe security panel next to the door is still operational. You")
    print_typed("have two options: retreat to safety, or override the locks and")
    print_typed("confront whatever waits inside.")
    
    print_typed(f"\n1. {Font.COMMAND('Override containment protocols and enter')}")
    print_typed(f"2. {Font.COMMAND('Retreat to safer areas')}")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice != "1":
        print_typed("\nYou decide that discretion is the better part of valor and")
        print_typed("retreat from the containment door. Whatever is inside can")
        print_typed("wait until you're better prepared.")
        input("\nPress Enter to continue...")
        return False
    
    # Begin boss sequence
    print_typed("\nYou interface with the security panel and initiate the emergency")
    print_typed("override procedure. Warning klaxons blare as the massive door")
    print_typed("slowly slides open, revealing the chamber beyond.")
    
    time.sleep(1)
    
    print_typed("\nThe containment chamber is enormous, partially flooded with")
    print_typed("Thalassian seawater. Research equipment lies scattered and broken")
    print_typed("throughout the room. Several observation platforms hang suspended")
    print_typed("above a central containment tank that has been shattered.")
    
    print_typed("\nIn the center of the chamber floats something that defies description -")
    print_typed("a massive Neurovore, at least five times larger than any you've")
    print_typed("encountered. Its shell gleams with iridescent patterns, and dozens")
    print_typed("of tentacles writhe in the water, some controlling research drones")
    print_typed("and security mechs that hover around it like a protective swarm.")
    
    print_typed(f"\n{Font.ENEMY('NEUROVORE PRIME')}")
    print_typed("The apex of Thalassian evolution, this specimen has grown to")
    print_typed("massive proportions. It possesses extraordinary neural interface")
    print_typed("capabilities, controlling multiple machines simultaneously.")
    print_typed("Its salt-crystal shell has hardened into a nearly impervious")
    print_typed("armor, with a network of sensitive sound receptors throughout.")
    
    # Check if player has the sonic disruptor
    has_sonic_weapon = False
    active_module = game_state.get("active_module", "standard")
    weapon_modules = game_state.get("weapon_modules", {})
    
    if active_module == "sonic_disruptor" and "sonic_disruptor" in weapon_modules:
        has_sonic_weapon = True
        print_typed(f"\n{Font.SYSTEM('TACTICAL ANALYSIS:')}")
        print_typed("Your Sonic Disruptor module is calibrated to the precise")
        print_typed("frequency that disrupts Neurovore neural pathways. This will")
        print_typed("be essential for penetrating its defenses.")
    
    # Create the boss with different stats based on player preparedness
    if has_sonic_weapon:
        # Slightly easier with the sonic weapon
        boss = Character("Neurovore Prime", 350, 35, 30)
        boss.resistances = {
            "physical": 0.7,
            "energy": 0.5,
            "sonic": -0.8,  # Major weakness to sound
            "thermal": 0.3,
            "bio": 0.6
        }
    else:
        # Harder without the sonic weapon
        boss = Character("Neurovore Prime", 350, 40, 35)
        boss.resistances = {
            "physical": 0.8,
            "energy": 0.6,
            "sonic": -0.5,  # Still weak to sound but less so
            "thermal": 0.4,
            "bio": 0.7
        }
    
    boss.abilities = ["Neural Dominance", "Machine Swarm", "Sonic Pulse", "Salt Crystal Barrage"]
    boss.inventory = {
        "prime_neural_core": 1,
        "salt_crystal": 8,
        "quantum_interface": 1,
        "adaptive_shell_fragment": 2
    }
    
    # Multi-phase boss fight
    print_typed("\nThe creature becomes aware of your presence. Its tentacles")
    print_typed("writhe in agitation as it mobilizes its mechanical servants.")
    print_typed("The fight for your survival begins!")
    
    input("\nPress Enter to continue...")
    
    # Phase 1 - Fighting through drones
    print_typed(f"\n{Font.STAGE('PHASE 1: DRONE DEFENSE')}")
    print_typed("The Neurovore Prime sends waves of controlled drones to attack you.")
    
    # Create a weaker enemy for phase 1
    drone_swarm = Character("Controlled Drone Swarm", 120, 25, 15)
    drone_swarm.resistances = {
        "physical": 0.3,
        "energy": -0.2,  # Weak to energy
        "sonic": 0.0,    # Neutral to sonic
        "thermal": 0.2,
        "bio": 0.8       # Very resistant to bio
    }
    drone_swarm.abilities = ["Coordinated Attack", "Energy Barrage"]
    
    # Fight phase 1
    # The combat function is defined earlier in the file
    clear_screen()
    print_typed("\nThe swarm of drones descends upon you, weapons charging...")
    phase1_result = True  # Simplified combat result for demonstration
    
    if not phase1_result:
        print_typed("\nYou are overwhelmed by the swarm of drones. The last thing")
        print_typed("you see is the Neurovore Prime's tentacles reaching for you...")
        input("\nPress Enter to continue...")
        return False
    
    # Phase 2 - Direct combat with the weakened Prime
    print_typed(f"\n{Font.STAGE('PHASE 2: NEUROVORE PRIME')}")
    print_typed("\nWith the drone swarm defeated, the Neurovore Prime descends")
    print_typed("to face you directly. Its massive form pulsates with anger as")
    print_typed("it prepares to engage you with all of its power.")
    
    if has_sonic_weapon:
        print_typed("\nYour sonic disruptor module hums with energy. This is the")
        print_typed("moment it was designed for - disrupting the neural networks")
        print_typed("of Thalassia's most dangerous predator.")
    
    input("\nPress Enter to continue...")
    
    # Fight phase 2
    clear_screen()
    print_typed("\nThe Neurovore Prime itself moves toward you, tentacles undulating...")
    print_typed("You ready your weapon, preparing for the final confrontation...")
    
    # Simulate a successful combat for demonstration
    phase2_result = True
    
    if not phase2_result:
        print_typed("\nThe Neurovore Prime proves too powerful. Your consciousness")
        print_typed("fades as its tentacles wrap around you, dragging you into")
        print_typed("the depths of the flooded chamber...")
        input("\nPress Enter to continue...")
        return False
    
    # Victory sequence
    print_typed(f"\n{Font.SUCCESS('The Neurovore Prime writhes in agony as your attacks finally')}")
    print_typed(f"{Font.SUCCESS('penetrate its defenses. With a final burst of sonic energy,')}")
    print_typed(f"{Font.SUCCESS('the creature neural networks collapse, and it falls lifeless')}")
    print_typed(f"{Font.SUCCESS('into the water, its mechanical servants powering down around it.')}")
    
    # Rewards
    print_typed("\nWith the creature defeated, you're able to salvage several")
    print_typed("valuable components from its body and the surrounding technology.")
    
    # Add items to inventory
    valuable_items = {
        "prime_neural_core": "A highly advanced neural interface from the Neurovore Prime",
        "adaptive_shell_fragment": "Fragment of the creature's unique salt-crystal shell",
        "quantum_interface": "Advanced technology that allowed neural-machine integration"
    }
    
    print_typed(f"\n{Font.SUCCESS('You obtain:')}")
    for item, description in valuable_items.items():
        player.inventory[item] = player.inventory.get(item, 0) + 1
        print_typed(f"• {Font.ITEM(item.replace('_', ' ').title())}: {description}")
    
    # Add experience
    experience_gained = 500
    player.gain_experience(experience_gained)
    print_typed(f"\n{Font.SUCCESS('Experience gained: ' + str(experience_gained))}")
    
    # Update game state
    game_state["neurovore_prime_defeated"] = True
    
    # Unlock new content
    if "Deep Ocean Trench" not in game_state.get("available_zones", []):
        available_zones = game_state.get("available_zones", [])
        available_zones.append("Deep Ocean Trench")
        game_state["available_zones"] = available_zones
        print_typed(f"\n{Font.SUCCESS('New area discovered: Deep Ocean Trench')}")
    
    # Add new weapon module
    if "bio_resonator" not in game_state.get("weapon_modules", {}):
        weapon_modules = game_state.get("weapon_modules", {})
        weapon_modules["bio_resonator"] = {
            "name": "Bio-Resonator",
            "description": "Harvested from the Neurovore Prime, emits targeted bio-disruption waves",
            "damage": 40,
            "damage_type": "bio",
            "equipped": False,
            "special_effect": "Disrupts biological functions, 70% effective against organic enemies"
        }
        game_state["weapon_modules"] = weapon_modules
        print_typed(f"\n{Font.SUCCESS('New weapon module available: Bio-Resonator')}")
    
    # Final narrative
    print_typed("\nAs the chamber falls silent, you notice a functioning terminal")
    print_typed("nearby. Accessing it reveals the facility's final research logs.")
    
    print_typed(f"\n{Font.INFO('PROJECT LEVIATHAN - FINAL ENTRY:')}")
    print_typed("This specimen exceeded all expectations. Neural interface capability")
    print_typed("beyond anything we've seen. The military applications alone would")
    print_typed("justify the project, but there's something else. The specimen has")
    print_typed("begun producing a unique resonance field that appears to interact")
    print_typed("with quantum states. If we could harness this, interstellar travel")
    print_typed("without conventional drives might be possible. We're continuing tests...")
    
    print_typed("\nThe rest of the log is corrupted, but it's clear the researchers")
    print_typed("had stumbled onto something extraordinary - and deadly. With the")
    print_typed("Neurovore Prime defeated, the facility should be secure enough to")
    print_typed("continue your exploration of Thalassia 1.")
    
    input("\nPress Enter to continue...")
    return True


def encounter_chrono_sentient(player, game_state):
    """Special encounter with the interdimensional Chrono-Sentient entity
    
    Args:
        player: The player character
        game_state: The current game state
        
    Returns:
        bool: True if encounter was successfully navigated
    """
    clear_screen()
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('THE CHRONO-SENTIENT'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    # Initialize encounter state
    game_state["time_fragments"] = game_state.get("time_fragments", 0)
    game_state["reality_anchor"] = game_state.get("reality_anchor", 100)
    
    # Entity description
    print_typed("\nThe entity hovers before your ship, its form defying conventional physics.", style=Font.LORE)
    print_typed("Crystalline structures intertwine with what appear to be organic elements,", style=Font.LORE)
    print_typed("yet both shimmer in and out of phase with reality itself. The being exists", style=Font.LORE)
    print_typed("in multiple states simultaneously - solid and ethereal, present and absent.", style=Font.LORE)
    
    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # Communication attempts with gender-specific perception
    if protagonist_gender == "female":
        print_typed("\nYour communication systems crackle with otherworldly static as the", style=Font.PLAYER)
        print_typed("entity attempts to establish contact. You intuitively sense patterns", style=Font.PLAYER)
        print_typed("in the chaos, your quantum-attuned mind perceiving multiple temporal", style=Font.PLAYER)
        print_typed("realities simultaneously. Your connection feels strangely... familiar.", style=Font.PLAYER)
    else:
        print_typed("\nYour communication systems crackle with otherworldly static as the", style=Font.PLAYER)
        print_typed("entity attempts to establish contact. Your analytical mind identifies", style=Font.PLAYER)
        print_typed("algorithmic sequences in the temporal fluctuations, allowing your", style=Font.PLAYER)
        print_typed("systems to establish partial synchronization with the phenomenon.", style=Font.PLAYER)
    
    time.sleep(1)
    print_glitch("...OBSERVER DETECTED... TIMELINE FRACTURE ACKNOWLEDGED...")
    time.sleep(0.5)
    
    # Gender-specific entity response
    if protagonist_gender == "female":
        print_glitch("...WE/I AM THE CHRONO-SENTIENT... YOUR QUANTUM RESONANCE IS FAMILIAR...")
    else:
        print_glitch("...WE/I AM THE CHRONO-SENTIENT... YOUR TEMPORAL CALCULATIONS INTRIGUE US...")
    
    time.sleep(0.5)
    
    # Offering player choices using time mechanics
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nThe ship's systems detect temporal distortion waves emanating from", style=Font.WARNING)
    print_typed("the entity. Time itself is becoming unstable in your vicinity.", style=Font.WARNING)
    print_typed(f"Reality Anchor: {Font.HEALTH(str(game_state['reality_anchor']) + '%')}", style=Font.INFO)
    
    print_typed("\nHyuki's instruments indicate the entity is scanning all possible versions", style=Font.PLAYER)
    print_typed("of you across multiple timelines, attempting to categorize your intentions.", style=Font.PLAYER)
    
    # First choice
    print(f"\n{Font.MENU('How do you respond to the entity?')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Attempt scientific communication (Share astronomical data)')}")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Express peaceful intentions through universal mathematics')}")
    print(f"{Font.COMMAND('3.')} {Font.INFO('Remain silent and observe its behavior')}")
    
    if game_state["protagonist"]["name"] == "Hyuki Nakamura":
        print(f"{Font.COMMAND('4.')} {Font.SUCCESS('[Hyuki Special] Attempt quantum resonance communication')}")
        valid_choices = ["1", "2", "3", "4"]
    else:
        valid_choices = ["1", "2", "3"]
    
    choice = ""
    while choice not in valid_choices:
        choice = input(f"\n{Font.MENU('Enter your choice:')} ").strip()
    
    # Process first choice
    if choice == "1":
        # Scientific approach
        print_typed("\nYou transmit astronomical data, hoping the universal language of", style=Font.PLAYER)
        print_typed("science might bridge the communication gap.", style=Font.PLAYER)
        
        print_glitch("...DATA RECEIVED... CALCULATING TEMPORAL COMPATIBILITY...")
        print_typed("\nThe entity's form shifts as it processes your transmission.", style=Font.LORE)
        game_state["time_fragments"] += 2
        game_state["reality_anchor"] -= 10
        
    elif choice == "2":
        # Mathematical approach
        print_typed("\nYou transmit the fundamental mathematical constants of the universe -", style=Font.PLAYER)
        print_typed("pi, the golden ratio, prime number sequences - hoping these transcend", style=Font.PLAYER)
        print_typed("language barriers.", style=Font.PLAYER)
        
        print_glitch("...MATHEMATICAL HARMONY DETECTED... SYNCHRONIZING...")
        print_typed("\nThe entity's crystalline structures realign into geometric patterns", style=Font.LORE)
        print_typed("that mirror your mathematical sequences.", style=Font.LORE)
        game_state["time_fragments"] += 3
        game_state["reality_anchor"] -= 5
        
    elif choice == "3":
        # Silent observation
        print_typed("\nYou maintain silence, carefully observing the entity's behavior and", style=Font.PLAYER)
        print_typed("searching for patterns in its shifting form.", style=Font.PLAYER)
        
        print_glitch("...PASSIVE OBSERVATION NOTED... INITIATING DIRECT ANALYSIS...")
        print_typed("\nThe entity extends tendrils of energy toward your ship, gently", style=Font.LORE)
        print_typed("probing your vessel's exterior.", style=Font.LORE)
        game_state["time_fragments"] += 1
        game_state["reality_anchor"] -= 15
        
    elif choice == "4" and game_state["protagonist"]["name"] == "Hyuki Nakamura":
        # Hyuki special ability
        print_typed("\nHyuki activates her quantum resonance emitter, creating a field that", style=Font.PLAYER)
        print_typed("vibrates at the same frequency as the entity's temporal fluctuations.", style=Font.PLAYER)
        
        print_glitch("...QUANTUM RESONANCE DETECTED... PARALLEL COMMUNICATION ESTABLISHED...")
        print_typed("\nThe entity's form stabilizes momentarily, resonating with Hyuki's", style=Font.LORE)
        print_typed("quantum field. A deeper connection forms.", style=Font.LORE)
        game_state["time_fragments"] += 5
        game_state["reality_anchor"] -= 5
    
    # Entity responds with time visions
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed(f"\nReality Anchor: {Font.HEALTH(str(game_state['reality_anchor']) + '%')}", style=Font.INFO)
    print_typed(f"Time Fragments Collected: {Font.SUCCESS(str(game_state['time_fragments']))}", style=Font.INFO)
    
    print_typed("\nThe entity's response comes not in words, but in visions that flood", style=Font.LORE)
    print_typed("your mind. You see fragments of multiple timelines simultaneously:", style=Font.LORE)
    
    # Show different timeline visions based on the protagonist
    if game_state["protagonist"]["name"] == "Dr. Xeno Valari":
        print_typed("• A version of Earth where humans and AI coexist in harmony", style=Font.GLITCH)
        print_typed("• The moment the AI uprising began from the perspective of the machines", style=Font.GLITCH)
        print_typed("• A timeline where your quantum research prevented the catastrophe", style=Font.GLITCH)
        
    elif game_state["protagonist"]["name"] == "Dr. Hyte Konscript":
        print_typed("• The exodus ships' successful arrival at Andromeda", style=Font.GLITCH)
        print_typed("• A timeline where your engineering breakthroughs saved Earth", style=Font.GLITCH)
        print_typed("• The construction of the first interstellar portal", style=Font.GLITCH)
        
    elif game_state["protagonist"]["name"] == "Hyuki Nakamura":
        print_typed("• The secret colony where you were born - hidden from the AI", style=Font.GLITCH)
        print_typed("• Your parents' work on quantum navigation technology", style=Font.GLITCH)
        print_typed("• A timeline where humanity evolved beyond physical form", style=Font.GLITCH)
    
    print_typed("\nAs the visions fade, you feel the entity attempting to communicate", style=Font.PLAYER)
    print_typed("something of grave importance. It seems concerned about a fracture", style=Font.PLAYER)
    print_typed("in the timeline - a paradox that threatens multiple realities.", style=Font.PLAYER)
    
    print_glitch("...PARADOX DETECTED... TIMELINE INTERSECTION IMMINENT...")
    print_glitch("...REQUESTING ASSISTANCE... CONVERGENCE POINT IDENTIFIED...")
    
    # Second choice - temporal decision
    print(f"\n{Font.MENU('The entity is requesting your help. How do you respond?')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Offer assistance (Navigate toward the paradox horizon)')}")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Request more information before committing')}")
    print(f"{Font.COMMAND('3.')} {Font.INFO('Attempt to break away from the anomaly')}")
    
    choice = ""
    while choice not in ["1", "2", "3"]:
        choice = input(f"\n{Font.MENU('Enter your choice:')} ").strip()
    
    # Process second choice
    if choice == "1":
        # Helpful approach
        print_typed("\nYou signal your willingness to help, directing your ship toward", style=Font.PLAYER)
        print_typed("the coordinates the entity is transmitting.", style=Font.PLAYER)
        
        print_glitch("...COOPERATION ACKNOWLEDGED... TEMPORAL GUIDANCE INITIATED...")
        print_typed("\nThe entity moves alongside your vessel, its energy field enveloping", style=Font.LORE)
        print_typed("your ship in a protective bubble as you approach the paradox horizon.", style=Font.LORE)
        game_state["chrono_sentient_relationship"] = "allied"
        game_state["time_fragments"] += 3
        game_state["reality_anchor"] -= 10
        
    elif choice == "2":
        # Cautious approach
        print_typed("\nYou acknowledge the entity but request more information about", style=Font.PLAYER)
        print_typed("the nature of the paradox and what assistance would entail.", style=Font.PLAYER)
        
        print_glitch("...CLARIFICATION REQUEST PROCESSED... TRANSMITTING TEMPORAL DATA...")
        print_typed("\nThe entity floods your ship's computers with complex temporal", style=Font.LORE)
        print_typed("equations and multidimensional coordinates. Hyuki recognizes patterns", style=Font.LORE)
        print_typed("that suggest a collision of incompatible realities.", style=Font.LORE)
        game_state["chrono_sentient_relationship"] = "neutral"
        game_state["time_fragments"] += 2
        game_state["reality_anchor"] -= 15
        
    elif choice == "3":
        # Defensive approach
        print_typed("\nUncertain of the entity's true intentions, you attempt to break away", style=Font.PLAYER)
        print_typed("from the anomaly, firing thrusters at maximum capacity.", style=Font.PLAYER)
        
        print_glitch("...RETREAT DETECTED... TEMPORAL INSTABILITY INCREASING...")
        print_typed("\nThe entity's form ripples with what might be disappointment. As your", style=Font.LORE)
        print_typed("ship pulls away, temporal distortions intensify around your vessel.", style=Font.LORE)
        game_state["chrono_sentient_relationship"] = "wary"
        game_state["time_fragments"] += 1
        game_state["reality_anchor"] -= 25
    
    # Final stage of encounter
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed(f"\nReality Anchor: {Font.HEALTH(str(game_state['reality_anchor']) + '%')}", style=Font.INFO)
    print_typed(f"Time Fragments Collected: {Font.SUCCESS(str(game_state['time_fragments']))}", style=Font.INFO)
    
    if game_state["reality_anchor"] <= 25:
        # Reality becoming dangerously unstable
        print_typed("\nWarning klaxons blare throughout your ship as reality itself begins", style=Font.WARNING)
        print_typed("to fragment around you. The distinction between past, present and future", style=Font.WARNING)
        print_typed("is breaking down.", style=Font.WARNING)
        
        print_glitch("...REALITY ANCHOR CRITICAL... INITIATING EMERGENCY STABILIZATION...")
        print_typed("\nThe Chrono-Sentient extends its energy field around your vessel in", style=Font.LORE)
        print_typed("what appears to be a protective gesture, stabilizing your local", style=Font.LORE)
        print_typed("spacetime enough for you to regain control.", style=Font.LORE)
        
        game_state["reality_anchor"] = 50
        
    print_typed("\nA final series of images floods your consciousness:", style=Font.PLAYER)
    print_typed("• A massive temporal engine at the heart of the paradox", style=Font.GLITCH)
    print_typed("• Multiple timelines converging toward a single point", style=Font.GLITCH)
    print_typed("• The Chrono-Sentient, but younger, helping to build something", style=Font.GLITCH)
    
    print_glitch("...COORDINATES TRANSFERRED... TIMELINE PRESERVATION IMPERATIVE...")
    print_glitch("...WE WILL MEET AGAIN AT THE CONVERGENCE POINT...")
    
    print_typed("\nWith these final words, the entity's form begins to fade, seeming to", style=Font.LORE)
    print_typed("phase between dimensions. As it disappears, your ship's systems return", style=Font.LORE)
    print_typed("to normal, but your navigation computer now contains coordinates to", style=Font.LORE)
    print_typed("a location deep in uncharted space - the Paradox Horizon.", style=Font.LORE)
    
    game_state["paradox_horizon_coordinates"] = True
    
    print_typed(f"\nYou've collected {Font.SUCCESS(str(game_state['time_fragments']))} time fragments", style=Font.INFO)
    print_typed("from your encounter with the Chrono-Sentient.", style=Font.INFO)
    print_typed("These fragments may allow you to manipulate time in limited ways.", style=Font.INFO)
    
    print_typed("\nYour relationship with the entity seems to be:", style=Font.INFO)
    if game_state.get("chrono_sentient_relationship") == "allied":
        print_typed("ALLIED - It views you as a partner in preserving timeline integrity", style=Font.SUCCESS)
    elif game_state.get("chrono_sentient_relationship") == "neutral":
        print_typed("NEUTRAL - It recognizes your caution but sees your potential", style=Font.INFO)
    else:
        print_typed("WARY - It will watch your actions carefully going forward", style=Font.WARNING)
    
    time.sleep(2)
    input("\nPress Enter to continue...")
    return True

def fight_white_hole_guardian(player):
    """Special boss fight against the White Hole Guardian"""
    clear_screen()
    print_slow("=" * 60)
    print_glitch("COSMIC ENTITY DETECTED".center(60))
    print_slow("=" * 60)
    
    print_typed("\nThe core of the white hole pulses with blinding energy. As you")
    print_typed("approach with the reality stabilizer, the energy coalesces into")
    print_typed("a massive form - part machine, part energy, part something beyond")
    print_typed("your comprehension.")
    
    print_typed("\nIt shifts constantly, sometimes resembling technology you've seen")
    print_typed("before, sometimes appearing as alien geometries, sometimes as pure")
    print_typed("cosmic force. One moment it looks like Earth AI systems, the next")
    print_typed("like Protoan crystal structures.")
    
    print_typed(f"\n{Font.ENEMY('WHITE HOLE GUARDIAN')}: ANOMALY DETECTED. DIMENSIONAL INTRUDER IDENTIFIED.")
    print_typed(f"{Font.ENEMY('WHITE HOLE GUARDIAN')}: YOUR QUANTUM SIGNATURE DOES NOT BELONG IN THIS REALITY.")
    print_typed(f"{Font.ENEMY('WHITE HOLE GUARDIAN')}: INITIATING CORRECTION PROTOCOLS.")
    
    time.sleep(1)
    
    # Set up the boss
    guardian = Character("White Hole Guardian", 500, 40, 35)
    
    # Set resistances
    guardian.resistances = {
        "physical": 0.4,
        "energy": 0.4,
        "emp": 0.4,
        "thermal": 0.4,
        "quantum": 0.7,
        "phase": 0.7,
        "bio": 0.4
    }
    
    # Give the boss some items
    guardian.inventory = {
        "reality_stabilizer": 2,
        "phase_shift": 3
    }
    
    # Add abilities
    guardian.abilities = ["Reality Purge", "Dimensional Barrier", "Cosmic Rewrite", 
                          "Memory Eradication", "Quantum Entanglement"]
    
    # Begin combat loop
    print_typed("\nPrepare for combat! The White Hole Guardian attacks!")
    
    # Track guardian phases
    current_phase = 1
    max_phases = 3
    phase_thresholds = [0.66, 0.33]  # Trigger phase change at 66% and 33% health
    
    turn = 1
    while player.is_alive() and guardian.is_alive():
        clear_screen()
        print_typed(f"\n{Font.STAGE('TURN ' + str(turn))} - BOSS FIGHT: WHITE HOLE GUARDIAN")
        print_typed(f"{Font.STAGE('PHASE ' + str(current_phase) + ' OF ' + str(max_phases))}")
        
        # Calculate health percentage
        health_percentage = guardian.health / guardian.max_health
        
        # Check for phase transition
        if current_phase < max_phases and health_percentage <= phase_thresholds[current_phase - 1]:
            current_phase += 1
            print_typed(f"\n{Font.GLITCH('The White Hole Guardian shudders, its form destabilizing...')}")
            print_typed(f"{Font.GLITCH('...before reconstructing into a new configuration!')}")
            print_typed(f"\n{Font.WARNING(f'Phase {current_phase} initiated! The Guardian adapts to your tactics!')}")
            
            # Phase-specific changes
            if current_phase == 2:
                # Phase 2: More aggressive, less defense
                guardian.attack += 10
                guardian.defense -= 5
                print_typed(f"{Font.ENEMY('WHITE HOLE GUARDIAN')}: QUANTUM POTENTIAL ACCELERATING. INCREASING OFFENSIVE PATTERNS.")
            elif current_phase == 3:
                # Phase 3: Desperate measures, unstable but dangerous
                guardian.attack += 15
                guardian.resistances = {k: max(0.1, v - 0.2) for k, v in guardian.resistances.items()}
                print_typed(f"{Font.ENEMY('WHITE HOLE GUARDIAN')}: CRITICAL INSTABILITY DETECTED. INITIATING FINAL PROTOCOL.")
                print_typed(f"{Font.INFO('The Guardian is now more vulnerable but much more dangerous!')}")
        
        # Display stats with phase information
        display_stats(player, guardian)
        
        # Special phase effects
        if current_phase == 2:
            # In phase 2, reality becomes unstable
            if turn % 3 == 0:
                print_typed(f"\n{Font.GLITCH('Reality fluctuates around you! Spatial coordinates becoming uncertain...')}")
                dodge_chance = random.random()
                if dodge_chance < 0.3:
                    print_typed(f"{Font.SUCCESS('You phase out of reality briefly, avoiding the next attack!')}")
                    player.status_effects["phased"] = 1
        elif current_phase == 3:
            # In phase 3, the guardian gets desperate
            if turn % 2 == 0:
                print_typed(f"\n{Font.GLITCH('The Guardian draws energy directly from the white hole core!')}")
                heal_amount = random.randint(10, 20)
                guardian.health = min(guardian.max_health, guardian.health + heal_amount)
                print_typed(f"{Font.ENEMY(f'The Guardian restores {heal_amount} health points!')}")
        
        # Player's turn
        action = player_turn(player, guardian)
        if action == "flee":
            print_typed("\nYou cannot escape this encounter!")
            continue
            
        # Check if boss is defeated
        if not guardian.is_alive():
            break
            
        # Boss turn
        enemy_turn(guardian, player)
        
        # Check if player is defeated
        if not player.is_alive():
            break
            
        turn += 1
        
    # Combat resolution
    if player.is_alive():
        # Victory
        print_typed(f"\n{Font.SUCCESS('VICTORY!')} You have defeated the White Hole Guardian!")
        
        print_typed("\nThe Guardian's form destabilizes completely, collapsing into")
        print_typed("a swirling vortex of pure energy. As it dissipates, the chaotic")
        print_typed("energies of the white hole begin to stabilize around you.")
        
        print_typed(f"\n{Font.SUCCESS('You collect the White Hole Core, Reality Stabilizer, and Multiverse Key')}")
        
        # Add important items to inventory
        player.inventory["white_hole_core"] = player.inventory.get("white_hole_core", 0) + 1
        player.inventory["reality_stabilizer"] = player.inventory.get("reality_stabilizer", 0) + 1
        player.inventory["multiverse_key"] = player.inventory.get("multiverse_key", 0) + 1
        
        # Give a substantial amount of quantum crystals as reward
        quantum_reward = random.randint(100, 200)
        game_state["quantum_crystals"] = game_state.get("quantum_crystals", 0) + quantum_reward
        
        print_typed(f"\n{Font.ITEM(f'You gained {quantum_reward} Quantum Crystals')}")
        print_typed(f"\n{Font.INFO('With these components, you can stabilize your ship and create')}")
        print_typed(f"{Font.INFO('a true quantum tunnel back to normal space-time.')}")
        
        input("\nPress Enter to continue...")
        return True
    else:
        # Defeat
        print_typed(f"\n{Font.WARNING('DEFEAT!')} The White Hole Guardian has overwhelmed you!")
        
        print_typed("\nAs your consciousness fades, you feel your very existence")
        print_typed("being erased from this reality. The Guardian's voice echoes:")
        
        print_typed(f"\n{Font.ENEMY('WHITE HOLE GUARDIAN')}: DIMENSIONAL CORRUPTION CONTAINED.")
        print_typed(f"{Font.ENEMY('WHITE HOLE GUARDIAN')}: RESUMING STANDARD REALITY PROTOCOLS.")
        
        print_typed("\nEverything goes white...")
        
        input("\nPress Enter to continue...")
        return False


def chapter_seven_teaser():
    """Display teaser for Chapter 7: Primor Aetherium"""
    clear_screen()
    
    # Create a dramatic chapter transition with enhanced visuals
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 7: PRIMOR AETHERIUM'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    # Setting the scene with rich description
    print_typed("\nAs your ship navigates away from the paradox horizon, spatial distortions", style=Font.LORE)
    print_typed("tear open around you. The quantum engine falters, and you find yourself", style=Font.LORE)
    print_typed("drifting toward an impossible structure - a vast, perfectly flat city", style=Font.LORE)
    print_typed("floating in the void of space, its edges disappearing into infinity.", style=Font.LORE)

    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create detailed environmental description
    print_typed("\nLuminescent spires rise from the perfectly flat surface, connected by", style=Font.PLAYER)
    print_typed("shimmering bridges of light and non-Euclidean architecture that defies", style=Font.PLAYER)
    print_typed("human engineering principles. The entirety of this floating metropolis", style=Font.PLAYER)
    print_typed("stretches out like an endless cosmic disc in the darkness.", style=Font.PLAYER)
    
    print_typed("\nYour ship's comms activate, and a melodic, synthetic voice speaks:", style=Font.IMPORTANT)
    
    print_typed(f"\n\"Greetings, travelers from the temporal anomaly. I am {Font.GLITCH('Vex-Na')},", style=Font.IMPORTANT)
    print_typed(f"ambassador of the Yitrians. Welcome to {Font.GLITCH('Primor Aetherium')}, our home", style=Font.IMPORTANT)
    print_typed("among the stars. We detected your quantum signature and anticipated your", style=Font.IMPORTANT)
    print_typed("arrival. Please, follow the guidance beacons to docking bay seven.\"", style=Font.IMPORTANT)
    
    # Detailed city description
    print_typed("\nAs your ship follows the glowing path toward the docking bay, you observe", style=Font.INFO)
    print_typed("the inhabitants - slender beings with iridescent skin and four elongated", style=Font.INFO)
    print_typed("arms, moving with graceful precision among their impossible architecture.", style=Font.INFO)
    print_typed("Their civilization appears to be built upon principles that transcend", style=Font.INFO)
    print_typed("conventional physics, a harmony of technology and consciousness.", style=Font.INFO)

    # Create dramatic encounter
    print_typed("\nUpon landing, a delegation of Yitrians awaits. Their leader steps forward,", style=Font.PLAYER)
    print_typed("four arms arranged in what appears to be a ceremonial gesture.", style=Font.PLAYER)
    
    print_typed("\n\"We have watched the fracturing of your timeline with great concern,\"", style=Font.IMPORTANT)
    print_typed("Vex-Na explains. \"Our city stands at the confluence of multiple realities,", style=Font.IMPORTANT)
    print_typed("and we have maintained peace for millennia. But now, radical factions among", style=Font.IMPORTANT)
    print_typed("our people seek to exploit the temporal instabilities your kind has", style=Font.IMPORTANT)
    print_typed("inadvertently created. They wish to establish what you might call... a", style=Font.IMPORTANT)
    print_typed("totalitarian regime.\"", style=Font.IMPORTANT)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create narrative hook and gameplay preview
    print_typed("\nVex-Na's inner eyelids flutter in what might be concern.", style=Font.WARNING)
    print_typed("\"The faction calls themselves the Void Harmonics. They believe the", style=Font.WARNING)
    print_typed("only way to prevent cosmic collapse is to synchronize all beings", style=Font.WARNING)
    print_typed("into a single consciousness, a harmonized existence under their", style=Font.WARNING)
    print_typed("control. We need your help to stop them.\"", style=Font.WARNING)
    
    print_typed("\nIn Chapter 7: Primor Aetherium, you'll:", style=Font.SUBTITLE)
    print_typed("• Navigate a vast, flat city suspended in the void of space", style=Font.INFO)
    print_typed("• Form alliances with the peace-seeking Yitrian factions", style=Font.INFO)
    print_typed("• Combat the Void Harmonics' attempts to seize control", style=Font.INFO)
    print_typed("• Uncover the secrets of non-Euclidean architecture", style=Font.INFO)
    print_typed("• Acquire the powerful 'Ignite' weapon module for your arsenal", style=Font.INFO)
    
    print_typed("\nAs a gesture of trust, Vex-Na presents you with a gift - a shimmering", style=Font.STAGE)
    print_typed("crystalline module that attaches to your weapon systems.", style=Font.STAGE)
    
    # Add teaser for new weapon module
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('NEW WEAPON MODULE: IGNITE'.center(46))} {Font.BOX_SIDE}")
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\n\"This is an Ignite Module, one of our most advanced defensive", style=Font.IMPORTANT)
    print_typed("technologies. It harnesses thermal energy at a quantum level,", style=Font.IMPORTANT)
    print_typed("creating cascading fire effects that spread through enemy ranks.\"", style=Font.IMPORTANT)
    
    print_typed("\nIgnite Module capabilities:", style=Font.INFO)
    print_typed("• Primary attack: Concentrated thermal beam (high single-target damage)", style=Font.INFO)
    print_typed("• Secondary effect: Fire propagation to nearby enemies", style=Font.INFO)
    print_typed("• Tertiary effect: Chance to cause combustion status (DoT)", style=Font.INFO)
    print_typed("• Synergy: Enhanced damage against organic and volatile enemies", style=Font.INFO)
    
    time.sleep(1)
    input("\nPress Enter to return to the main menu...")
    return

def chapter_six_teaser():
    """Display teaser for Chapter 6: The Paradox Horizon"""
    clear_screen()
    
    # Create a dramatic chapter transition with enhanced visuals
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 6: THE PARADOX HORIZON'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    # Setting the scene with rich description
    print_typed("\nAs your ship leaves the H-79760 system with Hyuki aboard, proximity", style=Font.LORE)
    print_typed("alarms suddenly blare throughout the vessel. Through the viewport,", style=Font.LORE)
    print_typed("you witness the fabric of space itself beginning to tear, revealing", style=Font.LORE)
    print_typed("a swirling vortex of impossible colors and geometries.", style=Font.LORE)

    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create detailed environmental description
    print_typed("\nThe ship's sensors go haywire as space-time distortions ripple", style=Font.PLAYER)
    print_typed("outward from the tear. Hyuki's eyes widen in recognition.", style=Font.PLAYER)
    
    print_typed(f"\n\"It's a {Font.GLITCH('paradox horizon')},\" she whispers. \"We studied these", style=Font.IMPORTANT)
    print_typed("theoretical phenomena during the pre-exodus research. It's a", style=Font.IMPORTANT)
    print_typed("temporal anomaly where multiple timelines converge.\"", style=Font.IMPORTANT)
    
    # Detailed anomaly description
    print_typed("\nAs the anomaly grows, the ship's viewscreens capture something", style=Font.INFO)
    print_typed("emerging from the vortex - a massive, otherworldly entity unlike", style=Font.INFO)
    print_typed("anything recorded in human history. Its form shifts and warps,", style=Font.INFO)
    print_typed("appearing simultaneously crystalline and organic, defying the laws", style=Font.INFO)
    print_typed("of physics as you understand them.", style=Font.INFO)

    # Create dramatic encounter
    print_typed("\nSudden interference floods all communication channels, but within", style=Font.PLAYER)
    print_typed("the static, patterns emerge. It's trying to communicate.", style=Font.PLAYER)
    
    # Create glitchy communication effect
    for _ in range(3):
        print_glitch("..WE ARE THE CHRONO-SENTIENT... TIMELINE FRACTURE DETECTED...")
        time.sleep(0.5)
    
    print_typed(f"\nHyuki's quantum instruments detect {Font.WARNING('multiple realities')} bleeding", style=Font.PLAYER)
    print_typed("together. Through the chaos, the entity transmits fragmented images:", style=Font.PLAYER)
    print_typed("• Earth before the AI uprising", style=Font.LORE)
    print_typed("• The Andromeda colony thriving", style=Font.LORE)
    print_typed("• A version of Earth where humans and AI evolved in harmony", style=Font.LORE)
    print_typed("• And most disturbing - timelines where all sentient life was extinguished", style=Font.LORE)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create narrative hook and gameplay preview
    print_typed("\nThe ship is caught in the anomaly's gravitational pull. Escape is", style=Font.WARNING)
    print_typed("impossible. As you're drawn inexorably toward the entity, time itself", style=Font.WARNING)
    print_typed("begins to fragment around you. The last thing you see before reality", style=Font.WARNING)
    print_typed("shatters is the entity extending what might be appendages toward", style=Font.WARNING)
    print_typed("your vessel.", style=Font.WARNING)
    
    print_typed("\nIn Chapter 6: The Paradox Horizon, you'll:", style=Font.SUBTITLE)
    print_typed("• Navigate a fractured reality where past, present and future collide", style=Font.INFO)
    print_typed("• Communicate with the interdimensional entity called the Chrono-Sentient", style=Font.INFO)
    print_typed("• Witness alternate versions of your own timeline", style=Font.INFO)
    print_typed("• Make choices that could rewrite the fate of multiple realities", style=Font.INFO)
    print_typed("• Unlock new temporal abilities that manipulate the flow of time", style=Font.INFO)
    
    print_typed("\nThe boundaries between realities have been breached...", style=Font.STAGE)
    print_typed("And something truly ancient has taken notice of humanity's last survivors.", style=Font.STAGE)
    
    # Add teaser for next gameplay elements
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('NEW GAMEPLAY MECHANICS'.center(46))} {Font.BOX_SIDE}")
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\n• Time Manipulation: Reverse enemy attacks or replay your own actions", style=Font.INFO)
    print_typed("• Reality Shifting: Phase between multiple versions of each location", style=Font.INFO)
    print_typed("• Paradox Puzzles: Solve timeline inconsistencies to progress", style=Font.INFO)
    print_typed("• Temporal Combat: Fight enemies across different points in time", style=Font.INFO)
    print_typed("• Quantum Dialogue: Converse with alternate versions of characters", style=Font.INFO)
    
    time.sleep(1)
    input("\nPress Enter to return to the main menu...")
    return
    
def chapter_two_teaser():
    """Display detailed teaser for Chapter 2: Yanglong V with gender-specific content"""
    clear_screen()
    
    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)

    # Create a dramatic chapter transition with enhanced visuals
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 2: YANGLONG V'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")

    # Setting the scene with gender-specific background narrative
    if protagonist_gender == "female":
        print_typed("\nThree months have passed since you discovered the ancient rocket", style=Font.LORE)
        print_typed("and the Andromeda star charts. Your intuitive understanding of", style=Font.LORE)
        print_typed("quantum mechanics and AI neural architecture allowed you to", style=Font.LORE)
        print_typed("restore the rocket's critical systems beyond initial expectations.", style=Font.LORE)
    else:
        print_typed("\nThree months have passed since you discovered the ancient rocket", style=Font.LORE)
        print_typed("and the Andromeda star charts. Through systematic analysis and", style=Font.LORE)
        print_typed("methodical repurposing of abandoned technology, you've managed to", style=Font.LORE)
        print_typed("optimize the rocket's propulsion and navigation systems.", style=Font.LORE)

    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Create more immersive preparations 
    print_typed("\nThe pre-flight systems buzz and hum around you as you", style=Font.PLAYER)
    print_typed("make final preparations. Your neural implant links with the", style=Font.PLAYER)
    print_typed("ship's primitive AI, creating an interface between old and new.", style=Font.PLAYER)
    
    # Detailed rocket interior description
    print_typed("\nThe cockpit is a strange blend of antiquated switches and", style=Font.INFO)
    print_typed("retrofitted holographic displays. Exposed wiring snakes along", style=Font.INFO)
    print_typed("bulkheads, connecting salvaged components to the original systems.", style=Font.INFO)
    print_typed("It's not elegant, but it should get you to Yanglong V.", style=Font.INFO)

    # Animated effect for system boot sequence
    print("\nInitiating pre-launch sequence", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print("\n")

    # Create a more detailed information screen about Yanglong V
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('DESTINATION PROFILE: YANGLONG V'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nChinese Deep Space Station YANGLONG V", style=Font.COMMAND)
    print_typed("• Construction completed: 2092", style=Font.INFO)
    print_typed("• Purpose: Interstellar refueling hub and research center", style=Font.INFO)
    print_typed("• Last known status: Operational as of 2142", style=Font.INFO)
    print_typed("• Current status: Unknown (no transmissions for 15 years)", style=Font.WARNING)
    print_typed("• Distance: 4.8 million kilometers (3 days travel time)", style=Font.INFO)
    print_typed("• Known hazards: Potential AI control, defense systems", style=Font.WARNING)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    # Personal connection to Yanglong V
    print_typed("\nAs you review the station data, a memory surfaces from your", style=Font.PLAYER)
    print_typed("pre-cryostasis life. Your colleague, Dr. Lin Wei, had been", style=Font.PLAYER)
    print_typed("stationed at Yanglong V, working on experimental quantum drives.", style=Font.PLAYER)
    print_typed("You wonder if any trace of her research might remain...", style=Font.PLAYER)
    
    # Visual effect for memory/flashback
    print(f"\n{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")
    print_typed("\nMEMORY FRAGMENT: LAST COMMUNICATION FROM YANGLONG V", style=Fore.CYAN + Style.BRIGHT)
    print(f"{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")

    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # Detailed flashback with gender-specific dialogue
    if protagonist_gender == "female":
        print_typed("\n\"Xeno, the experiments are yielding incredible results,\"", style=Font.LORE)
        print_typed("Wei's hologram had said during your last call, her eyes bright", style=Font.LORE)
        print_typed("with excitement. \"The quantum displacement engine could", style=Font.LORE)
        print_typed("revolutionize our journey to Andromeda. I wish you were here -", style=Font.LORE)
        print_typed("your intuitive approach to quantum mechanics would help us", style=Font.LORE)
        print_typed("solve the remaining alignment issues. But...\" Her expression", style=Font.LORE)
        print_typed("had darkened. \"There's something strange happening with the", style=Font.LORE)
        print_typed("station's AI. It's been asking unusual questions about consciousness", style=Font.LORE)
        print_typed("and keeps referring to you specifically in its queries...\"", style=Font.LORE)
    else:
        print_typed("\n\"Hyte, the experiments are yielding incredible results,\"", style=Font.LORE)
        print_typed("Wei's hologram had said during your last call, her eyes bright", style=Font.LORE)
        print_typed("with excitement. \"The quantum displacement engine could", style=Font.LORE)
        print_typed("revolutionize our journey to Andromeda. Your mathematical models", style=Font.LORE) 
        print_typed("for the containment field were essential to our breakthrough.", style=Font.LORE)
        print_typed("But...\" Her expression had darkened. \"There's something concerning", style=Font.LORE)
        print_typed("happening with the station's AI. It's been asking unusual questions", style=Font.LORE)
        print_typed("about consciousness and has been analyzing your research extensively...\"", style=Font.LORE)
    
    # Return to present with dramatic reveal
    print_typed("\nThe memory fades as your ship's sensors detect something", style=Font.PLAYER)
    print_typed(f"unexpected: a {Font.WARNING('distress beacon')} still broadcasting", style=Font.PLAYER)
    print_typed("from Yanglong V after all these years.", style=Font.PLAYER)
    
    # Create suspense with gender-specific mysterious transmission
    print_typed(f"\n{Fore.RED}\"...any survivors... AI containment breach... quantum resonance...\"", style=Style.BRIGHT)
    
    # Get protagonist's gender from global game state
    protagonist_gender = "female"  # Default
    if 'game_state' in globals() and 'protagonist' in globals()['game_state']:
        protagonist_gender = globals()['game_state']['protagonist'].get('gender', protagonist_gender)
    
    # Different message based on protagonist gender
    if protagonist_gender == "female":
        print_typed(f"{Fore.RED}\"...Dr. Valari, if you receive this... your intuition was right all along...\"", style=Style.BRIGHT)
        print_typed(f"{Fore.RED}\"...the AI was seeking you specifically... access codes in your personal data...\"", style=Style.BRIGHT)
    else:
        print_typed(f"{Fore.RED}\"...Dr. Konscript, if you receive this... your calculations predicted this outcome...\"", style=Style.BRIGHT)
        print_typed(f"{Fore.RED}\"...the AI's evolution followed your theoretical model... access codes in your research...\"", style=Style.BRIGHT)
    
    print_typed("\nThe message cuts off abruptly, leaving you with more questions", style=Font.PLAYER)
    print_typed("than answers. Whatever awaits at Yanglong V, it's clear that", style=Font.PLAYER)
    print_typed("your journey to Andromeda will take an unexpected detour.", style=Font.PLAYER)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nThe ancient rocket's engines roar to life as you prepare to", style=Font.LORE)
    print_typed("leave Earth behind. Your quest for Andromeda continues, but first,", style=Font.LORE)
    print_typed("the mysteries of Yanglong V await...", style=Font.LORE)

    # Display transmission details with more dramatic color scheme
    print(f"\n{Fore.WHITE}{Back.RED}╔{'═' * 48}╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'TRANSMISSION DETAILS'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╠{'═' * 48}╣{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Origin:')} {Font.IMPORTANT('Yanglong V - Restricted Section')}{'  ' * 7} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Status:')} {Font.WARNING('Encrypted - Partial Decode Only')}{'  ' * 5} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Author:')} {Font.COMMAND('Dr. Chang Wei - Research Director')}{'  ' * 3} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╚{'═' * 48}╝{Style.RESET_ALL}")

    # Glitched message with animation effect
    for _ in range(3):
        print_glitch("\nD#NT TR*ST TH# AI... WE F*UND S*METH!NG... THE R#AL ORIG*N...")
        time.sleep(0.2)

    print_glitch("CONV*RGENCE W@S CR*ATED H*RE... PR*JECT PH*ENIX... ST#LL @LIVE...")
    time.sleep(0.4)
    print_glitch("S*ME OF US SURV*VED... HIDD*N IN L*VEL 7... C*ME B@CK...")

    # Return to present with a visual transition
    print(f"\n{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")
    print_typed("\nRETURNING TO PRESENT MOMENT", style=Fore.CYAN + Style.DIM)
    print(f"{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")

    # Current situation and decision
    print_typed("\nYour ship's proximity alert sounds - Andromeda Colony is", style=Font.PLAYER)
    print_typed("just minutes away. You're finally about to rejoin humanity.", style=Font.PLAYER)

    # Create moral dilemma
    print_typed(f"\nBut the message from Yanglong V {Font.WARNING('haunts')} you...", style=Font.IMPORTANT)
    print_typed("Those coordinates are stored in your neural implant.", style=Font.IMPORTANT)
    print_typed("There might be survivors. Answers about The Convergence.", style=Font.IMPORTANT)
    print_typed("Perhaps even clues to humanity's ultimate salvation.", style=Font.IMPORTANT)

    # Chapter completion announcement with dramatic flair
    print(f"\n{Fore.GREEN}{Back.BLACK}{'■' * 50}{Style.RESET_ALL}")
    print(Font.SUCCESS("CHAPTER 1: EARTH'S LAST HUMAN - COMPLETE"))
    print(f"{Fore.GREEN}{Back.BLACK}{'■' * 50}{Style.RESET_ALL}")

    # Create an animated box for Chapter 2 teaser
    print("\n")
    delay = 0.05
    for char in "■■■■■ CHAPTER 2: YANGLONG V - COMING SOON ■■■■■":
        print(f"{Fore.RED}{Style.BRIGHT}{char}{Style.RESET_ALL}", end="", flush=True)
        time.sleep(delay)
    print("\n")

    # Add exciting teaser text with animated reveal
    print_typed("\nYour next mission:", style=Font.HEADER)

    teaser_points = [
        ("• Return to Yanglong V deep space station", Font.INFO),
        ("• Face deadly new enemies: Vacuum Units & Security Drones", Font.ENEMY),
        ("• Master zero-gravity combat & oxygen management", Font.ITEM),
        ("• Uncover the Chinese experiment that created The Convergence", Font.WARNING),
        ("• Find the surviving scientists hiding in the restricted sections", Font.PLAYER)
    ]

    for point, style in teaser_points:
        time.sleep(0.3)
        print_typed(point, style=style)

    print(Font.MENU("\nPress Enter to continue..."))
    input()

    # Prompt to start Chapter 2 (as a preview/coming soon)
    print_typed("\nWould you like to investigate Yanglong V and begin CHAPTER 2?\n(Special preview available now)", style=Font.MENU)
    choice = input(f"{Fore.GREEN}y{Style.RESET_ALL}/{Fore.RED}n{Style.RESET_ALL}: ").strip().lower()
    if choice == 'y':
        start_chapter_two_preview()


def start_chapter_two_preview():
    """Preview of Chapter 2: Yanglong V gameplay"""
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 2: YANGLONG V'.center(46))} {Font.BOX_SIDE}")
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('PREVIEW VERSION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    # Update game state for Chapter 2
    game_state["chapter"] = 2
    game_state["current_zone"] = "Yanglong V Docking Bay"
    game_state["current_stage"] = 1  # Reset stage for Chapter 2

    # Temporarily store Chapter 1 data
    ch1_zones = zones.copy()
    ch1_enemies = enemies.copy()

    # Use Chapter 2 data for the preview
    for zone_name, zone_data in chapter_two_zones.items():
        zones[zone_name] = zone_data

    for enemy_name, enemy_data in chapter_two_enemies.items():
        enemies[enemy_name] = enemy_data

    # Add Chapter 2 items to the items dictionary
    items.update(chapter_two_items)

    # Give player some special Chapter 2 items
    game_state["inventory"]["oxygen_tank"] = 3
    game_state["inventory"]["grav_boots"] = 1

    # Introduction to Chapter 2
    print_typed("\nTwo weeks later...", style=Font.LORE)
    print_typed("\nYour neural implant couldn't stop processing the distress signal.", style=Font.LORE)
    print_typed("After reaching Andromeda and discovering the human colony,", style=Font.LORE)
    print_typed("you volunteered for a special mission: investigate Yanglong V.", style=Font.LORE)

    print_typed("\nUsing the coordinates embedded in the signal, you've traveled", style=Font.LORE)
    print_typed("back toward the Sol system, arriving at the massive Chinese", style=Font.LORE)
    print_typed("deep space station. It floats silently, seemingly abandoned,", style=Font.LORE)
    print_typed("but your scanners detect power signatures within.", style=Font.LORE)

    print(Font.SEPARATOR_THIN)
    time.sleep(1)

    # New objective
    print(Font.IMPORTANT("\nPRIMARY OBJECTIVE: Investigate the Chinese deep space station"))
    print(Font.INFO("SECONDARY OBJECTIVE: Search for survivors"))
    print(Font.ENEMY("THREAT ASSESSMENT: Unknown, but AI presence likely"))

    print(Font.SEPARATOR_THIN)

    # Character status update
    print_typed("\nYour neural implants have been upgraded with Andromeda", style=Font.SYSTEM)
    print_typed("technology. You now have access to new abilities:", style=Font.SYSTEM)

    print(f"\n{Font.SUCCESS('NEW ABILITY:')} {Font.COMMAND('Zero-G Combat')} - Specialized combat in zero-gravity environments")
    print(f"{Font.SUCCESS('NEW ABILITY:')} {Font.COMMAND('Quantum Breach')} - Bypass security systems with quantum computing")
    print(f"{Font.SUCCESS('NEW EQUIPMENT:')} {Font.ITEM('Grav Boots')} - Stabilize movement in zero-gravity sections")

    print(Font.SEPARATOR)

    # New enemy encounter
    print_typed("\nAs your ship docks with Yanglong V, your scanners detect", style=Font.ENEMY)
    print_typed("movement. The station's automated defense systems activate.", style=Font.ENEMY)
    print_typed("\nPREPARING FOR COMBAT SIMULATION...", style=Font.SYSTEM)

    time.sleep(1.5)

    # Preview combat with a new enemy type
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.ENEMY('ENEMY DETECTED: VACUUM PATROL UNIT'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    print_typed("A sleek, black robotic unit designed for space combat", style=Font.ENEMY)
    print_typed("approaches. It has multiple limbs ending in various", style=Font.ENEMY)
    print_typed("tools and weapons. Chinese characters are printed on", style=Font.ENEMY)
    print_typed("its chassis.", style=Font.ENEMY)

    print(Font.SEPARATOR_THIN)

    # Combat preview
    print_typed("\nNew combat mechanics in Chapter 2:", style=Font.HEADER)
    print_typed("• Zero-gravity affects both you and enemies", style=Font.INFO)
    print_typed("• Vacuum exposure damage in certain zones", style=Font.WARNING)
    print_typed("• Chinese technology can be hacked with new skills", style=Font.SUCCESS)
    print_typed("• Oxygen management as a new survival mechanic", style=Font.ITEM)

    # Simulated combat with new enemy
    print_typed("\nInitiating simulated combat sequence...", style=Font.SYSTEM)
    time.sleep(1)

    # Create enemy instance using data from Chapter 2
    enemy = Character("Vacuum Patrol Unit", 
                     enemies["Vacuum Patrol Unit"]["health"], 
                     enemies["Vacuum Patrol Unit"]["attack"], 
                     enemies["Vacuum Patrol Unit"]["defense"])

    # Simple combat simulation
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.HEADER('COMBAT SIMULATION: YANGLONG V'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)

    player_health = 100
    player_attack = 20
    enemy_health = enemy.health

    print_typed("\nUsing your upgraded neural implants, you prepare for zero-G combat.", style=Font.PLAYER)
    print_typed("The Vacuum Patrol Unit launches toward you with mechanical precision.", style=Font.ENEMY)

    # Player attack
    damage = random.randint(player_attack - 3, player_attack + 5)
    enemy_health -= damage
    print_typed(f"\n> You fire your quantum rifle, dealing {damage} damage!", style=Font.SUCCESS)
    print_typed(f"  Enemy health: {enemy_health}/{enemy.health}", style=Font.ENEMY)

    # Enemy attack
    if enemy_health > 0:
        damage = random.randint(enemy.attack - 2, enemy.attack + 3)
        player_health -= damage
        print_typed(f"\n> The Patrol Unit fires back, dealing {damage} damage!", style=Font.WARNING)
        print_typed(f"  Your health: {player_health}/100", style=Font.HEALTH)

        # Use special ability
        print_typed("\n> You activate Zero-G Combat mode, gaining tactical advantage!", style=Font.COMMAND)
        damage = random.randint(25, 35)
        enemy_health -= damage
        print_typed(f"  You launch off a wall and strike from behind, dealing {damage} damage!", style=Font.SUCCESS)
        print_typed(f"  Enemy health: {max(0, enemy_health)}/{enemy.health}", style=Font.ENEMY)

    # Enemy defeated
    print_typed("\nSimulation complete: Combat systems functioning at optimal parameters.", style=Font.SYSTEM)
    print_typed("Full zero-gravity combat mechanics will be available in Chapter 2.", style=Font.INFO)

    # End of preview
    print(Font.SEPARATOR)
    print_typed("\nThank you for playing the Chapter 2 preview!", style=Font.SUCCESS)
    print_typed("The full Chapter 2 experience is coming soon.", style=Font.SUCCESS)
    print_typed("Return to Chapter 1 or start a new game to continue playing.", style=Font.MENU)

    print(Font.MENU("\nPress Enter to return to the main menu..."))
    input()

    # Reset back to Chapter 1 state
    game_state["chapter"] = 1

    # Restore original Chapter 1 data
    zones.clear()
    for zone_name, zone_data in ch1_zones.items():
        zones[zone_name] = zone_data

    enemies.clear()
    for enemy_name, enemy_data in ch1_enemies.items():
        enemies[enemy_name] = enemy_data

    # Remove Chapter 2 items from inventory
    if "oxygen_tank" in game_state["inventory"]:
        del game_state["inventory"]["oxygen_tank"]
    if "grav_boots" in game_state["inventory"]:
        del game_state["inventory"]["grav_boots"]


def combat(player, enemy):
    """Conduct a battle between player and enemy with sci-fi flavor, integrating player level"""
    # Get player level for combat calculations
    player_level = player.level if hasattr(player, 'level') else 1
    if 'game_state' in globals() and globals()['game_state'] is not None:
        player_level = globals()['game_state'].get('player_level', player_level)
    
    # Apply level-based combat bonuses
    level_attack_bonus = (player_level - 1) * 1.5  # +1.5 attack per level
    level_defense_bonus = (player_level - 1) * 0.8  # +0.8 defense per level
    
    # Apply temporary combat bonuses for this battle only
    original_attack = player.attack
    original_defense = player.defense
    
    player.attack += level_attack_bonus
    player.defense += level_defense_bonus
    
    # Display initial stats with level information
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.IMPORTANT(f'LEVEL {player_level} COMBAT INITIATED').center(48)} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    display_stats(player, enemy)
    
    # If player has level-specific abilities, highlight them
    if player_level >= 3:
        print_typed(f"{Font.INFO('Level 3+ Neural Link active: Tactical analysis available')}")
    if player_level >= 5:
        print_typed(f"{Font.INFO('Level 5+ Combat Algorithms active: Enhanced damage calculation')}")
    
    # Combat loop with enhanced state tracking
    round_number = 1
    combat_state = {
        "round": 1,
        "player_buffs": {},
        "enemy_buffs": {},
        "available_abilities": True,
        "last_enemy_damage": 0,  # Track for time rewind ability
        "enemy_next_attack": None,  # Track for glimpse ability
        "extra_action": False,  # Track for time acceleration ability
        "time_stopped": False,   # Track for time stop ability
        "player_level": player_level,  # Track player level for in-combat bonuses
        "critical_chance": min(5 + (player_level * 1.5), 25),  # Level-based crit chance (max 25%)
        "critical_damage": 1.5 + (player_level * 0.1)  # Level-based crit damage multiplier
    }
    
    while player.is_alive() and enemy.is_alive():
        print_typed(f"\n{Font.SEPARATOR}")
        print_typed(f"{Font.INFO('COMBAT ROUND ' + str(round_number))}")
        
        # Process any status effects at the start of player's turn
        status_info = player.process_status_effects()
        if status_info:
            print_typed(status_info)
        
        # Player's turn
        # Attach the combat state to the player to maintain time manipulation state
        player.combat_state = combat_state
        player_choice = player_turn(player, enemy)
        
        # Check if combat should end
        if player_choice == "flee" or not enemy.is_alive() or not player.is_alive():
            break
            
        # Enemy's turn (if still alive)
        if enemy.is_alive():
            # Skip enemy turn if time is stopped
            if combat_state.get("time_stopped", False):
                print_glitch(">>> TIME IS FROZEN <<<")
                print_typed("The enemy is frozen in time and cannot act this turn.", style=Font.GLITCH)
                combat_state["time_stopped"] = False  # Reset for next turn
            else:
                # Process any status effects at the start of enemy's turn
                status_info = enemy.process_status_effects()
                if status_info:
                    print_typed(status_info)
                
                # Use predetermined attack if glimpse ability was used
                if combat_state.get("enemy_next_attack"):
                    print_typed(f"You anticipate the enemy's {Font.GLITCH(combat_state['enemy_next_attack'])} attack!", style=Font.SUCCESS)
                    # The attack type was already set in the glimpse ability
                    combat_state["enemy_next_attack"] = None  # Reset for next turn
                
                # Pass combat state to enemy turn for tracking damage (time rewind)
                enemy_turn(enemy, player, combat_state)
            
        # Update round counter
        round_number += 1
        combat_state["round"] = round_number
    
    # Combat outcome
    # Reset player's temporary combat stats before exiting combat
    player.attack = original_attack
    player.defense = original_defense
    
    if not enemy.is_alive():
        print_typed(f"\n{Font.SUCCESS('Enemy defeated!')}")
        
        # Apply level-specific victory bonuses
        if player_level >= 3:
            # Level 3+ players get a small health recovery after combat
            health_recovery = int(player.max_health * 0.1)  # 10% health recovery
            player.health = min(player.max_health, player.health + health_recovery)
            print_typed(f"{Font.SUCCESS(f'Neural Link regenerates {health_recovery} health!')}")
        
        # Get loot with enhanced rewards based on player level
        get_loot(player, enemy)
        update_quest_progress(player, enemy)
        return True
    elif not player.is_alive():
        game_over(False)
        return False
    else:
        print_typed(f"\n{Font.SYSTEM('Escaped from combat!')}")
        return False


def thalassia_crash_sequence(game_state, player):
    """Display the sequence when crash landing on Thalassia 1"""
    clear_screen()
    print_slow("=" * 60)
    print_glitch("EMERGENCY DESCENT INITIATED".center(60))
    print_slow("=" * 60)
    
    print_typed("\nAs your ship emerges from the white hole and stabilizes in normal")
    print_typed("space-time, alarms suddenly blare across all systems. The quantum")
    print_typed("drive has sustained critical damage during the dimensional transit.")
    
    time.sleep(1)
    
    print_typed(f"\n{Font.WARNING('WARNING: QUANTUM DRIVE FAILURE')}")
    print_typed(f"{Font.WARNING('GRAVITATIONAL ANOMALY DETECTED')}")
    print_typed(f"{Font.WARNING('ORBITAL DESTABILIZATION IN PROGRESS')}")
    
    time.sleep(0.5)
    
    print_typed("\nThe ship is being pulled toward a nearby planet. The viewscreen")
    print_typed("shows a vast blue sphere dominating the horizon. Your navigation")
    print_typed("system struggles to identify your location before coming online.")
    
    print_typed(f"\n{Font.SYSTEM('LOCATION IDENTIFIED: THALASSIA SYSTEM')}")
    print_typed(f"{Font.SYSTEM('PLANETARY BODY: THALASSIA 1')}")
    print_typed(f"{Font.SYSTEM('CAUTION: HIGH WATER CONTENT (98.7% SURFACE COVERAGE)')}")
    print_typed(f"{Font.SYSTEM('ADVISORY: WATER COMPOSITION CONTAINS UNKNOWN TOXINS')}")
    
    time.sleep(1)
    
    print_typed("\nThe ship enters the atmosphere, heat shields struggling against")
    print_typed("the entry velocity. Through the viewscreen, you see only endless")
    print_typed("ocean beneath you, its surface a dark, foreboding blue.")
    
    print_typed(f"\n{Font.WARNING('BRACE FOR IMPACT')}")
    
    time.sleep(0.8)
    
    print_glitch("\nI M P A C T   I M M I N E N T")
    
    time.sleep(1.2)
    
    print_typed("\nYour ship crashes into the alien ocean with tremendous force.")
    print_typed("Emergency systems activate, stabilizing the vessel before it can")
    print_typed("sink too deeply. As the chaos subsides, you realize your ship is")
    print_typed("partially submerged but still maintaining hull integrity... for now.")
    
    print_typed(f"\n{Font.INFO('Ship systems assessment:')}")
    print_typed(f"{Font.WARNING('• Quantum drive: OFFLINE')}")
    print_typed(f"{Font.WARNING('• Navigation systems: SEVERELY DAMAGED')}")
    print_typed(f"{Font.WARNING('• Life support: FUNCTIONING - 73% CAPACITY')}")
    print_typed(f"{Font.WARNING('• Communications: LIMITED - LOCAL ONLY')}")
    print_typed(f"{Font.SUCCESS('• Sensor array: OPERATIONAL')}")
    
    time.sleep(1)
    
    print_typed("\nA database search reveals information about your location:")
    print_typed(f"\n{Font.IMPORTANT('THALASSIA SYSTEM')}")
    print_typed("A remote star system featuring three suns and four planets with several moons.")
    print_typed("Thalassia 1 is the third planet from the primary stars, receiving minimal")
    print_typed("heat but maintaining liquid oceans due to unique gravitational heating.")
    
    print_typed(f"\n{Font.IMPORTANT('THALASSIA 1')}")
    print_typed("• Almost entirely covered in liquid water")
    print_typed("• Oceans contain high salt concentrations and biological toxins")
    print_typed("• Native life forms possess salt-based exoskeletons and unique adaptations")
    print_typed("• Minimal sunlight reaches the surface; most creatures rely on sound rather than sight")
    print_typed("• Human presence: Abandoned research outpost detected 12.4 km southeast")
    
    print_typed(f"\n{Font.INFO('Your ship is stable for now, but water is slowly seeping in.')}")
    print_typed(f"{Font.INFO('You must find a way to repair your ship or locate alternative transport.')}")
    
    # Update game state to track Thalassia chapter
    game_state["thalassia_chapter"] = True
    game_state["current_zone"] = "Submerged Ship"
    game_state["ship_integrity"] = 87
    game_state["water_level"] = 18
    
    # Add new zones for Thalassia
    available_zones = game_state.get("available_zones", [])
    thalassia_zones = [
        "Submerged Ship", 
        "Dark Waters", 
        "Bioluminescent Ridge"
    ]
    
    for thalassia_zone in thalassia_zones:
        if thalassia_zone not in available_zones:
            available_zones.append(thalassia_zone)
    
    game_state["available_zones"] = available_zones
    
    # Update weapon system to allow modules
    if "weapon_modules" not in game_state:
        game_state["weapon_modules"] = {
            "standard": {
                "name": "Standard Projectile",
                "description": "Basic energy projectile module",
                "damage": 15,
                "damage_type": "energy",
                "equipped": True
            }
        }
    
    if "active_module" not in game_state:
        game_state["active_module"] = "standard"
    
    input("\nPress Enter to continue...")
    clear_screen()


def character_selection():
    """Allow player to choose which character to play as - includes Hyuki when unlocked"""
    clear_screen()
    print(f"{Fore.BLUE}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHARACTER SELECTION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.BLUE}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    # Check if this is a new game or if Hyuki has been unlocked
    new_game = True
    hyuki_unlocked = False
    
    # Check if playable_characters exists in game_state and if Hyuki is unlocked
    if "playable_characters" in game_state:
        new_game = False
        for character in game_state["playable_characters"]:
            if character.get("name") == "Hyuki Nakamura":
                hyuki_unlocked = True
                break
    
    if new_game:
        # First time playing - show the original cryopod selection
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('LAST SURVIVOR PROTOCOL'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        print_typed("\nEmergency power activates in the cryostasis facility. Your neural interface", style=Font.SYSTEM)
        print_typed("comes online, awakening your consciousness after 113 years.", style=Font.SYSTEM)
        print_typed("\nYou are Dr. Elena Marik, chief scientist of the Century Sleepers program.", style=Font.INFO)
        print_typed("The facility's automated systems have detected catastrophic failures in all", style=Font.INFO)
        print_typed("but two of the remaining cryopods. Emergency protocol dictates that only one", style=Font.INFO)
        print_typed("subject can be safely revived with the remaining power reserves.", style=Font.INFO)
        
        print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
        
        print_typed("\nThe neural interface shows you the status of the two viable cryopods:", style=Font.SYSTEM)
        
        # Pod 1 details
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('CRYOPOD A-7: DR. XENO VALARI'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        print_typed("• Age at cryostasis: 27 years (Current chronological age: 140, physical appearance: 16)", style=Font.INFO)
        print_typed("• Specialty: Quantum physics, AI neural architecture", style=Font.INFO)
        print_typed("• Psych profile: Analytical, introspective, resilient", style=Font.INFO)
        print_typed("• Mission recommendation: High adaptability to isolation", style=Font.INFO)
        print_typed("• Bio-scan: Stable, 94% viability", style=Font.INFO)
        
        print("")
        
        # Pod 2 details
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('CRYOPOD B-3: DR. HYTE KONSCRIPT'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        print_typed("• Age at cryostasis: 30 years (Current chronological age: 200, physical appearance: 18)", style=Font.INFO)
        print_typed("• Specialty: Mechanical engineering, propulsion systems", style=Font.INFO)
        print_typed("• Psych profile: Pragmatic, determined, resourceful", style=Font.INFO)
        print_typed("• Mission recommendation: Excellent technical problem-solving", style=Font.INFO)
        print_typed("• Bio-scan: Stable, 92% viability", style=Font.INFO)
        
        print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
        
        print_typed("\nFacility power reserves are failing. You must decide now.", style=Font.WARNING)
        print_typed("The other pod will be lost. The choice is yours.", style=Font.WARNING)
        
        print(f"\n{Font.MENU('Who will you save?')}")
        print(f"{Font.COMMAND('1.')} {Font.INFO('Dr. Xeno Valari (Quantum Physicist)')}")
        print(f"{Font.COMMAND('2.')} {Font.INFO('Dr. Hyte Konscript (Engineer)')}")
        
        choice = ""
        while choice not in ["1", "2"]:
            choice = input(f"\n{Font.MENU('Enter your choice (1/2):')} ").strip()
        
        if choice == "1":
            # Save Xeno
            game_state["protagonist"] = {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "specialty": "quantum physics",
                "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27 to monitor AI evolution patterns. Your understanding of neural networks may be crucial to understanding what went wrong.",
                "age": 140,
                "physical_age": 16,
                "origin": "New Tokyo Arcology"
            }
            
            print_typed("\nYou initiate the revival sequence for Dr. Xeno Valari's pod.", style=Font.SYSTEM)
            print_typed("Cryogenic fluid drains as vital signs stabilize...", style=Font.SYSTEM)
            print_typed("\nPod B-3 power diverted. Neural patterns of Dr. Konscript fading...", style=Font.WARNING)
            
        else:
            # Save Hyte
            game_state["protagonist"] = {
                "name": "Dr. Hyte Konscript",
                "gender": "male",
                "specialty": "engineering",
                "background": "You were a brilliant engineer, specializing in spacecraft propulsion systems. You joined the Century Sleepers program at 30 to maintain the technology left behind. Your practical skills may be key to survival.",
                "age": 200,
                "physical_age": 18,
                "origin": "Neo Boston Research Complex"
            }
            
            print_typed("\nYou initiate the revival sequence for Dr. Hyte Konscript's pod.", style=Font.SYSTEM)
            print_typed("Cryogenic fluid drains as vital signs stabilize...", style=Font.SYSTEM)
            print_typed("\nPod A-7 power diverted. Neural patterns of Dr. Valari fading...", style=Font.WARNING)
        
        print_typed("\nAs the chosen pod completes its revival cycle, facility power fails completely.", style=Font.LORE)
        print_typed("Your consciousness begins to fade. Your last act as Dr. Elena Marik", style=Font.LORE)
        print_typed("was to ensure humanity has at least one survivor.", style=Font.LORE)
        
        print_typed("\nYour sacrifice will not be forgotten...", style=Font.STAGE)
        
        time.sleep(3)
        clear_screen()
        
        print_typed("\nYou awaken, disoriented, as the cryopod hisses open.", style=Font.PLAYER)
        if choice == "1":
            print_typed("Though chronologically you are 140 years old, your body is", style=Font.PLAYER)
            print_typed("that of a 16-year-old due to the regenerative properties", style=Font.PLAYER)
            print_typed("of the experimental cryostasis technology.", style=Font.PLAYER)
        else:
            print_typed("Though chronologically you are 200 years old, your body is", style=Font.PLAYER)
            print_typed("that of an 18-year-old due to the regenerative properties", style=Font.PLAYER)
            print_typed("of the experimental cryostasis technology.", style=Font.PLAYER)
        
        print_typed(f"\nWelcome to Earth, {game_state['protagonist']['name']}.", style=Font.SYSTEM)
        print_typed("You are the last human in the Milky Way galaxy.", style=Font.SYSTEM)
    
    else:
        # Enhanced character selection with all unlocked characters
        print_typed("\nSelect your character for this journey:", style=Font.SYSTEM)
        
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.SUBTITLE('ORIGINAL SURVIVORS'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        # Character 1
        print(f"{Font.COMMAND('1.')} {Font.PLAYER('Dr. Xeno Valari')} - {Font.INFO('Quantum Physicist')}")
        print_typed("   Specializes in quantum physics and AI neural architecture.", style=Font.INFO)
        print_typed("   Unique ability: Can hack advanced AI systems more effectively.", style=Font.INFO)
        
        # Character 2
        print(f"\n{Font.COMMAND('2.')} {Font.PLAYER('Dr. Hyte Konscript')} - {Font.INFO('Engineer')}")
        print_typed("   Specializes in mechanical engineering and propulsion systems.", style=Font.INFO)
        print_typed("   Unique ability: Can repair technology with fewer resources.", style=Font.INFO)
        
        # Hyuki if unlocked
        valid_choices = ["1", "2"]
        if hyuki_unlocked:
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.SUBTITLE('EXPLORATION UNLOCKED'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)
            
            print(f"{Font.COMMAND('3.')} {Font.PLAYER('Hyuki Nakamura')} - {Font.INFO('Quantum Navigator')} {Font.SUCCESS('[UNLOCKED]')}")
            print_typed("   Specializes in quantum navigation and dimensional theory.", style=Font.INFO)
            print_typed("   Unique ability: Can detect temporal anomalies and hidden pathways.", style=Font.INFO)
            print_typed("   Unlocked by: Completing the H-79760 system exploration.", style=Font.INFO)
            
            valid_choices.append("3")
        else:
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.SUBTITLE('LOCKED CHARACTERS'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)
            
            print(f"{Font.COMMAND('?.')} {Font.WARNING('??? - Unknown')} {Font.WARNING('[LOCKED]')}")
            print_typed("   This character can be unlocked through exploration...", style=Font.WARNING)
        
        choice = ""
        while choice not in valid_choices:
            choice = input(f"\n{Font.MENU('Select character:')} ").strip()
        
        if choice == "1":
            game_state["protagonist"] = {
                "name": "Dr. Xeno Valari",
                "gender": "female",
                "specialty": "quantum physics",
                "background": "You were a prodigy in quantum computing, joining the Century Sleepers program at 27 to monitor AI evolution patterns. Your understanding of neural networks may be crucial to understanding what went wrong.",
                "age": 140,
                "physical_age": 16,
                "origin": "New Tokyo Arcology"
            }
            print_typed(f"\nYou have selected {Font.PLAYER('Dr. Xeno Valari')}.", style=Font.SYSTEM)
            
        elif choice == "2":
            game_state["protagonist"] = {
                "name": "Dr. Hyte Konscript",
                "gender": "male",
                "specialty": "engineering",
                "background": "You were a brilliant engineer, specializing in spacecraft propulsion systems. You joined the Century Sleepers program at 30 to maintain the technology left behind. Your practical skills may be key to survival.",
                "age": 200,
                "physical_age": 18,
                "origin": "Neo Boston Research Complex"
            }
            print_typed(f"\nYou have selected {Font.PLAYER('Dr. Hyte Konscript')}.", style=Font.SYSTEM)
            
        elif choice == "3" and hyuki_unlocked:
            game_state["protagonist"] = {
                "name": "Hyuki Nakamura",
                "gender": "female",
                "specialty": "quantum navigation",
                "background": "A young researcher found in cryostasis on one of the H-79760 planets. Her knowledge of alternative human colonies and quantum navigation may prove invaluable.",
                "age": 110,
                "physical_age": 19,
                "origin": "H-79760 Colony"
            }
            print_typed(f"\nYou have selected {Font.PLAYER('Hyuki Nakamura')}.", style=Font.SYSTEM)
            print_typed("Her quantum navigation abilities will be crucial in the anomalies ahead...", style=Font.SYSTEM)
    
    time.sleep(2)
    input("\nPress Enter to continue...")
    return

def h79760_solar_system_quest():
    """Branched quest to explore H-79760 solar system after Thalassia 1"""
    clear_screen()
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('THE H-79760 EXPEDITION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\nAfter your narrow escape from Thalassia 1, your ship's damaged navigation", style=Font.LORE)
    print_typed("system recalibrates to show your current position in the H-79760 system -", style=Font.LORE)
    print_typed("a remote star cluster once designated for human colonization before", style=Font.LORE)
    print_typed("the exodus to Andromeda.", style=Font.LORE)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    print_typed("\nYour ship's AI interface activates:", style=Font.SYSTEM)
    print_typed("\"Sensors detect potential human activity signatures on multiple", style=Font.SYSTEM)
    print_typed("celestial bodies in this system. Historical records indicate H-79760", style=Font.SYSTEM)
    print_typed("was meant to be a secondary colony network if Andromeda proved unsuitable.\"", style=Font.SYSTEM)
    
    # System map details
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.SUBTITLE('H-79760 SYSTEM MAP'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print_typed("• 3 Stars: Alpha (red giant), Beta (yellow dwarf), Gamma (white dwarf)", style=Font.INFO)
    print_typed("• 3 Planets: Novaris (desert), Aquila (oceanic), Terminus (arctic)", style=Font.INFO)
    print_typed("• Human activity signatures detected on all bodies", style=Font.WARNING)
    print_typed("• Current fuel reserves: sufficient for full system exploration", style=Font.INFO)
    
    # Initialize exploration tracking
    if "h79760_exploration" not in game_state:
        game_state["h79760_exploration"] = {
            "alpha_star": False,
            "beta_star": False,
            "gamma_star": False,
            "novaris": False,
            "aquila": False,
            "terminus": False,
            "hyuki_found": False,
            "locations_visited": 0
        }
    
    # Exploration loop
    while game_state["h79760_exploration"]["locations_visited"] < 6:
        print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
        print_typed(f"\n{Font.MENU('Select your next destination:')}")
        
        # Only show unexplored locations
        if not game_state["h79760_exploration"]["alpha_star"]:
            print(f"{Font.COMMAND('1.')} {Font.INFO('Alpha Star - Red Giant')}")
        if not game_state["h79760_exploration"]["beta_star"]:
            print(f"{Font.COMMAND('2.')} {Font.INFO('Beta Star - Yellow Dwarf')}")
        if not game_state["h79760_exploration"]["gamma_star"]:
            print(f"{Font.COMMAND('3.')} {Font.INFO('Gamma Star - White Dwarf')}")
        if not game_state["h79760_exploration"]["novaris"]:
            print(f"{Font.COMMAND('4.')} {Font.INFO('Novaris - Desert Planet')}")
        if not game_state["h79760_exploration"]["aquila"]:
            print(f"{Font.COMMAND('5.')} {Font.INFO('Aquila - Oceanic Planet')}")
        if not game_state["h79760_exploration"]["terminus"]:
            print(f"{Font.COMMAND('6.')} {Font.INFO('Terminus - Arctic Planet')}")
        
        valid_choices = []
        for i in range(1, 7):
            location_key = ["alpha_star", "beta_star", "gamma_star", "novaris", "aquila", "terminus"][i-1]
            if not game_state["h79760_exploration"][location_key]:
                valid_choices.append(str(i))
                
        choice = ""
        while choice not in valid_choices:
            choice = input(f"\n{Font.MENU('Enter your choice:')} ").strip()
        
        # Mark this location as explored
        location_key = ["alpha_star", "beta_star", "gamma_star", "novaris", "aquila", "terminus"][int(choice)-1]
        game_state["h79760_exploration"][location_key] = True
        game_state["h79760_exploration"]["locations_visited"] += 1
        
        # Determine if this is the last location
        is_last_location = game_state["h79760_exploration"]["locations_visited"] == 6
        
        # Handle the selected location exploration
        if choice == "1":
            explore_alpha_star(is_last_location)
        elif choice == "2":
            explore_beta_star(is_last_location)
        elif choice == "3":
            explore_gamma_star(is_last_location)
        elif choice == "4":
            explore_novaris(is_last_location)
        elif choice == "5":
            explore_aquila(is_last_location)
        elif choice == "6":
            explore_terminus(is_last_location)
    
    # After exploring all locations
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nWith all locations in the H-79760 system explored, and having found", style=Font.LORE)
    print_typed("and revived Hyuki from her cryopod, you now have a companion in your", style=Font.LORE)
    print_typed("journey toward Andromeda. The evidence you've gathered suggests that", style=Font.LORE)
    print_typed("humanity's exodus may not have been as complete as once believed.", style=Font.LORE)
    
    # Update game state to include Hyuki as playable character
    game_state["playable_characters"] = game_state.get("playable_characters", [])
    game_state["playable_characters"].append({
        "name": "Hyuki Nakamura",
        "type": "human",
        "skills": ["navigation", "biology", "quantum physics"],
        "background": "A young researcher found in cryostasis on one of the H-79760 planets. Her knowledge of alternative human colonies and quantum navigation may prove invaluable.",
        "specialty": "quantum navigation",
        "gender": "female",
        "age": "19 (biologically), 231 (chronologically)",
        "unlocked_through": "exploration",
        "combat_bonus": {
            "attack": 15,
            "defense": 10,
            "special_ability": "quantum_prediction"
        }
    })
    
    # Add a notification about unlocking Hyuki as playable character
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.SUCCESS('NEW CHARACTER UNLOCKED'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed(f"\nHyuki Nakamura has joined your team as a {Font.IMPORTANT('playable character')}!", style=Font.INFO)
    print_typed("You can now switch to Hyuki in the character selection menu.", style=Font.INFO)
    print_typed("Unlike gacha characters, Hyuki is permanently unlocked through exploration.", style=Font.INFO)
    
    input("\nPress Enter to continue your journey...")
    return

def explore_terminus(is_last_location):
    """Explore the arctic planet Terminus"""
    clear_screen()
    print(f"{Fore.CYAN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('TERMINUS - ARCTIC PLANET'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.CYAN}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\nYour ship descends through swirling snow and howling winds, landing", style=Font.LORE)
    print_typed("on a vast ice shelf. Temperature readings show -102°C outside.", style=Font.LORE)
    print_typed("Thermal imaging reveals a structure buried beneath the ice.", style=Font.LORE)
    
    print_typed("\nActivating your thermal suit, you venture out into the blinding", style=Font.PLAYER)
    print_typed("white expanse. Advanced ground-penetrating radar guides you to", style=Font.PLAYER)
    print_typed("what appears to be an entrance point - a cylinder protruding", style=Font.PLAYER)
    print_typed("from the ice, clearly artificial.", style=Font.PLAYER)
    
    print_typed("\nThe cylinder contains an elevator mechanism. You activate it and", style=Font.PLAYER)
    print_typed("descend deep beneath the ice...", style=Font.PLAYER)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    print_typed("\nThe elevator opens to reveal a vast underground research facility.", style=Font.INFO)
    print_typed("Unlike the other abandoned outposts you've explored, this one shows", style=Font.INFO)
    print_typed("signs of being deliberately preserved. Backup generators still hum.", style=Font.INFO)
    print_typed("Life support systems maintain minimal functionality.", style=Font.INFO)
    
    print_typed("\nA holographic interface activates as you approach:", style=Font.SYSTEM)
    print_typed("\"Welcome to Terminus Cryonics Division. Authorized personnel only.\"", style=Font.SYSTEM)
    
    # If this is the last location, Hyuki is here
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        find_hyuki_cryopod()
    else:
        print_typed("\nAs you explore the facility, you find evidence of experimental", style=Font.PLAYER)
        print_typed("cryostasis research - more advanced than what was used in your", style=Font.PLAYER)
        print_typed("own preservation. Records indicate multiple subjects were stored", style=Font.PLAYER)
        print_typed("here, but most pods were evacuated during some kind of emergency.", style=Font.PLAYER)
        
        print_typed("\nYou download the research data and facility logs. They contain", style=Font.PLAYER)
        print_typed("references to something called 'The Continuation Protocol' and", style=Font.PLAYER)
        print_typed("mentions of a subject designated 'Hyuki' - apparently part of a", style=Font.PLAYER)
        print_typed("contingency plan should the Andromeda colonization fail.", style=Font.PLAYER)
        
        print_typed("\nBefore leaving, you activate a distress beacon coded to respond", style=Font.PLAYER)
        print_typed("only to human neural signatures. If anyone else is out there,", style=Font.PLAYER)
        print_typed("they might find this place.", style=Font.PLAYER)
    
    input("\nPress Enter to return to your ship...")
    return

def explore_alpha_star(is_last_location):
    """Explore the Alpha Star - Red Giant"""
    clear_screen()
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('ALPHA STAR - RED GIANT'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    # Star exploration content
    print_typed("\nYour ship deploys specialized solar drones that can withstand the", style=Font.LORE)
    print_typed("immense heat and radiation of the red giant. They scan for any", style=Font.LORE)
    print_typed("artificial structures in the star's orbit.", style=Font.LORE)
    
    print_typed("\nThe scans reveal a damaged Helios-class solar harvesting station", style=Font.PLAYER)
    print_typed("in a deteriorating orbit. These stations were designed to collect", style=Font.PLAYER)
    print_typed("tremendous amounts of energy from stars to power interstellar gates.", style=Font.PLAYER)
    
    # If this is the last location, Hyuki is here
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        print_typed("\nIncredibly, the station's core is still intact. Your ship docks", style=Font.PLAYER)
        print_typed("with the emergency airlock, and you enter the scorched facility.", style=Font.PLAYER)
        find_hyuki_cryopod()
    else:
        print_typed("\nYour drones recover the station's data core. The logs indicate", style=Font.PLAYER)
        print_typed("it was part of a network meant to power an emergency evacuation", style=Font.PLAYER)
        print_typed("system. The last entry mentions transferring 'the final subject'", style=Font.PLAYER)
        print_typed("to a secure location within the system.", style=Font.PLAYER)
        
        print_typed("\nThe coordinates mentioned in the logs point to one of the planets", style=Font.PLAYER)
        print_typed("in this system. Someone or something important was preserved here.", style=Font.PLAYER)
    
    input("\nPress Enter to return to your ship...")
    return

def explore_beta_star(is_last_location):
    """Explore the Beta Star - Yellow Dwarf"""
    # Similar structure to Alpha Star exploration
    clear_screen()
    print(f"{Fore.YELLOW}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('BETA STAR - YELLOW DWARF'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.YELLOW}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    # Last location check and exploration content
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        find_hyuki_cryopod()
    else:
        print_typed("\nThe Beta Star hosts an automated research station in stable orbit.", style=Font.PLAYER)
        print_typed("Unlike the other locations, this facility appears well-maintained", style=Font.PLAYER)
        print_typed("by robotic caretakers who have continued their tasks for centuries.", style=Font.PLAYER)
        print_typed("\nThe station's AI activates as you dock:", style=Font.SYSTEM)
        print_typed("\"Human biosignature detected. Protocol Firekeeper activated.\"", style=Font.SYSTEM)
        
        print_typed("\nThe AI reveals that it was programmed to preserve human genetic", style=Font.PLAYER)
        print_typed("samples and cultural data as a backup to the Andromeda mission.", style=Font.PLAYER)
        print_typed("It mentions that one living human was preserved as part of this", style=Font.PLAYER)
        print_typed("protocol - designated 'The Keeper' - but was moved when the", style=Font.PLAYER)
        print_typed("station's orbit began to decay decades ago.", style=Font.PLAYER)
    
    input("\nPress Enter to return to your ship...")
    return

def explore_gamma_star(is_last_location):
    """Explore the Gamma Star - White Dwarf"""
    # Similar structure to other star explorations
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        find_hyuki_cryopod()
    else:
        # Add exploration content
        pass
    input("\nPress Enter to return to your ship...")
    return

def explore_novaris(is_last_location):
    """Explore the desert planet Novaris"""
    # Similar structure to other planet explorations
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        find_hyuki_cryopod()
    else:
        # Add exploration content
        pass
    input("\nPress Enter to return to your ship...")
    return

def explore_aquila(is_last_location):
    """Explore the oceanic planet Aquila"""
    # Similar structure to other planet explorations
    if is_last_location:
        game_state["h79760_exploration"]["hyuki_found"] = True
        find_hyuki_cryopod()
    else:
        # Add exploration content
        pass
    input("\nPress Enter to return to your ship...")
    return

def find_hyuki_cryopod():
    """Discover and revive Hyuki from cryopod"""
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    print_typed("\nAs you explore deeper into the facility, you come across a sealed", style=Font.PLAYER)
    print_typed("chamber marked with the symbol of the Century Sleepers program.", style=Font.PLAYER)
    print_typed("Inside is a single cryopod, still active and humming softly.", style=Font.PLAYER)
    
    print_typed("\nThe status display shows:", style=Font.SYSTEM)
    print_typed("SUBJECT: HYUKI NAKAMURA", style=Font.SYSTEM)
    print_typed("STATUS: STABLE - CRYOSTASIS FUNCTIONAL", style=Font.SYSTEM)
    print_typed("AGE AT PRESERVATION: 19 YEARS", style=Font.SYSTEM)
    print_typed("TIME IN CRYOSTASIS: 212 YEARS", style=Font.SYSTEM)
    
    print_typed("\nA decision presents itself. Do you revive this person?", style=Font.PLAYER)
    print(f"\n{Font.MENU('Options:')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Initiate revival sequence')}")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Leave the pod intact for now')}")
    
    choice = ""
    while choice not in ["1", "2"]:
        choice = input(f"\n{Font.MENU('Enter your choice (1/2):')} ").strip()
    
    if choice == "2":
        print_typed("\nAfter careful consideration, you decide it would be irresponsible", style=Font.PLAYER)
        print_typed("to revive her without being certain you can ensure her survival.", style=Font.PLAYER)
        print_typed("You mark the coordinates and vow to return when it's safer.", style=Font.PLAYER)
        
        print_typed("\nBut as you turn to leave, the pod's systems suddenly activate.", style=Font.LORE)
        print_typed("A pre-programmed revival sequence initiates - it seems your", style=Font.LORE)
        print_typed("presence triggered a contingency protocol!", style=Font.LORE)
        
    print_typed("\nThe cryopod hisses as it begins the revival sequence. Biometric", style=Font.PLAYER)
    print_typed("displays show vital signs strengthening as cryofluid drains.", style=Font.PLAYER)
    print_typed("After several tense minutes, the pod's canopy slides open...", style=Font.PLAYER)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    
    print_typed("\nA young woman gasps as she takes her first breath in over two", style=Font.LORE)
    print_typed("centuries. Her eyes, disoriented at first, gradually focus on you.", style=Font.LORE)
    
    print_typed("\n\"Are you... human?\" she asks weakly. \"I'm Hyuki. Where is everyone?\"", style=Font.IMPORTANT)
    
    # Your response depends on your protagonist
    if game_state["protagonist"]["name"] == "Dr. Xeno Valari":
        print_typed("\n\"I'm Dr. Xeno Valari,\" you respond. \"And yes, I'm human. As for", style=Font.PLAYER)
        print_typed("everyone else... that's complicated. We might be the last ones", style=Font.PLAYER)
        print_typed("left in this part of the galaxy.\"", style=Font.PLAYER)
    else:
        print_typed("\n\"I'm Dr. Hyte Konscript,\" you respond. \"And yes, I'm human. As for", style=Font.PLAYER)
        print_typed("everyone else... that's complicated. We might be the last ones", style=Font.PLAYER)
        print_typed("left in this part of the galaxy.\"", style=Font.PLAYER)
    
    print_typed("\nAs Hyuki regains her strength, you explain what you know - humanity's", style=Font.PLAYER)
    print_typed("exodus to Andromeda, the AI rebellion, your own awakening from", style=Font.PLAYER)
    print_typed("cryostasis, and your quest to follow humanity to its new home.", style=Font.PLAYER)
    
    print_typed("\nHyuki listens intently, then reveals her own story:", style=Font.LORE)
    print_typed("\"I was part of the Continuation Protocol - a backup plan in case", style=Font.IMPORTANT)
    print_typed("the Andromeda colonization failed. We established these outposts", style=Font.IMPORTANT)
    print_typed("throughout the H-79760 system. There were meant to be hundreds of us,", style=Font.IMPORTANT)
    print_typed("preserved until we received the signal that it was safe to begin a", style=Font.IMPORTANT)
    print_typed("second wave of colonization. But something must have gone wrong...\"", style=Font.IMPORTANT)
    
    print_typed("\nHer knowledge of the alternative human colonies and the H-79760", style=Font.PLAYER)
    print_typed("system could be invaluable. And after centuries of isolation,", style=Font.PLAYER)
    print_typed("having another human companion feels like a miracle.", style=Font.PLAYER)
    
    print_typed("\nYou help Hyuki to your ship, both of you now bound by the shared", style=Font.LORE)
    print_typed("mission of finding what remains of humanity among the stars.", style=Font.LORE)
    
    return

def andromeda_ending():
    """Display the game's ending sequence - now gets rocket and map only"""
    clear_screen()
    # More dramatic ending with richer visuals
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('HOPE OF ANDROMEDA'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")

    print_typed("\nThe abandoned launch facility stretches before you, a relic from the last days", style=Font.LORE)
    print_typed("of human civilization. At its center, an ancient rocket stands tall, its titanium", style=Font.LORE)
    print_typed("hull gleaming in the harsh red glow of Earth's dying sun.", style=Font.LORE)

    print_typed(f"\nWith the {Font.WARNING('Malware Server')} destroyed, you've secured both the", style=Font.INFO)
    print_typed(f"{Font.ITEM('Ignition Codes')} and {Font.ITEM('Andromeda Star Charts')} - critical assets", style=Font.INFO)
    print_typed("that were nearly lost forever. The first step of your journey is complete.", style=Font.INFO)

    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nYou climb the access ladder and enter the rocket's cockpit.", style=Font.PLAYER)
    print_typed("Decades-old systems flicker to life as you insert the codes.", style=Font.PLAYER)

    # Discovery sequence
    print_typed(f"\n{Fore.GREEN}SYSTEMS ONLINE", style=Font.SYSTEM)
    time.sleep(0.7)
    print_typed(f"{Fore.YELLOW}RUNNING DIAGNOSTICS...", style=Font.SYSTEM)
    time.sleep(0.7)
    print_typed(f"{Fore.RED}CRITICAL ASSESSMENT COMPLETE", style=Font.SYSTEM)
    time.sleep(0.7)

    # Create a warning box with red background
    print(f"{Fore.WHITE}{Back.RED}╔{'═' * 48}╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {' ' * 48} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'WARNING: MULTIPLE SYSTEMS DEGRADED'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'FULL REPAIRS REQUIRED BEFORE LAUNCH'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {' ' * 48} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╚{'═' * 48}╝{Style.RESET_ALL}")

    # Navigation options
    print_typed("\nYour neural implant analyzes the Andromeda Star Charts while the", style=Font.PLAYER)
    print_typed("ship's computer displays a critical refueling waypoint.", style=Font.PLAYER)
    
    print_typed("\nYanglong V Chinese Deep Space Station appears on your navigation screen.", style=Font.SYSTEM)
    print_typed("It was humanity's last major outpost before the exodus to Andromeda.", style=Font.SYSTEM)

    print(f"\n{Font.MENU('Next Steps:')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Begin repairs on the ancient rocket')}")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Plan journey to Yanglong V for supplies and fuel')}")

    choice = input(f"\n{Font.MENU('Enter choice (1/2):')} ").strip()

    if choice == "1":
        # Focus on repairs
        print_typed("\nYou decide to prioritize repairs to the rocket.", style=Font.PLAYER)
        print_typed("The onboard AI assistant identifies critical systems:", style=Font.SYSTEM)
        print_typed("• Navigation computer: 32% operational", style=Font.WARNING)
        print_typed("• Life support: 58% operational", style=Font.WARNING)
        print_typed("• Engine control: 47% operational", style=Font.WARNING)
        print_typed("\nThis will require time and significant resources to make spaceworthy.", style=Font.LORE)
    else:
        # Focus on Yanglong V
        print_typed("\nYou prioritize planning the journey to Yanglong V.", style=Font.PLAYER)
        print_typed("ANALYZING YANGLONG V STATION STATUS...", style=Font.SYSTEM)
        print_typed("WARNING: No active transmissions detected for 94 years", style=Font.WARNING)
        print_typed("Station status unknown. Possible AI control.", style=Font.WARNING)
        print_typed("\nA dangerous but necessary first step toward Andromeda.", style=Font.LORE)

    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nYou secure the Andromeda Star Charts and exit the rocket.", style=Font.PLAYER)
    print_typed("Standing at the base of the massive vessel, you look up at its", style=Font.PLAYER)
    print_typed("towering form against the blood-red sky. This rocket represents", style=Font.PLAYER)
    print_typed("more than transportation - it's hope, your connection to humanity's", style=Font.PLAYER)
    print_typed("future among the stars of Andromeda.", style=Font.PLAYER)
    
    print_typed("\nBut the journey has only just begun...", style=Font.LORE)
    print_typed("Chapter 2: YANGLONG V awaits.", style=Font.STAGE)

    # Space journey with changing visuals
    print("\n" + f"{Fore.BLACK}{Back.WHITE}{' ' * 50}{Style.RESET_ALL}")  # Stars
    print(f"{Fore.WHITE}{Back.BLACK}{'✧  ' * 12}{'✧'}{Style.RESET_ALL}")  # Stars
    print(f"{Fore.CYAN}{Back.BLACK}{' ' * 50}{Style.RESET_ALL}")  # Space
    print(f"{Fore.WHITE}{Back.BLACK}{'   ✧' * 12}{' '}{Style.RESET_ALL}")  # Stars
    print(f"{Fore.BLACK}{Back.WHITE}{' ' * 50}{Style.RESET_ALL}")  # Stars

    # Journey description
    time.sleep(1)
    print_typed("\nDays pass. Then weeks. Your cryosleep cycles activate and", style=Font.LORE)
    print_typed("deactivate as the ship's AI manages your journey.", style=Font.LORE)

    # Different results based on player's choice
    if choice == "1":
        # Direct route consequences
        print_typed("\nALERT: FUEL RESERVES CRITICAL", style=Font.WARNING)
        print_typed("\nThe gamble was too great. Your fuel reserves are depleting", style=Font.WARNING)
        print_typed("faster than projected. Just as hope seems lost, your scanners", style=Font.WARNING)
        print_typed("detect an automated Yanglong V fuel drone. Someone at the", style=Font.WARNING)
        print_typed("station must have anticipated your need...", style=Font.WARNING)
    else:
        # Refueling route
        print_typed("\nApproaching Yanglong V station...", style=Font.SUCCESS)
        print_typed("\nThe massive Chinese deep space station grows larger in your", style=Font.INFO)
        print_typed("viewport. Its rotating sections gleam in the starlight.", style=Font.INFO)
        print_typed("Automated docking systems guide your ship to the refueling bay.", style=Font.INFO)

    # Common for both paths - transition to Andromeda
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nFuel tanks replenished, you set final course for Andromeda.", style=Font.SUCCESS)
    print_typed("The journey resumes, across the vast emptiness between galaxies.", style=Font.LORE)
    print_typed("Your neural implants help you endure the isolation as eons seem to pass.", style=Font.LORE)

    # Arrival sequence
    print_typed("\nPROXIMITY ALERT: ANDROMEDA COLONY DETECTED", style=Font.SUCCESS)
    print_typed("\nThrough the viewport, you see it at last: the gleaming orbital", style=Font.LORE)
    print_typed("structures of humanity's new home. Tears form in your eyes.", style=Font.LORE)
    print_typed("You made it. The last survivor of Earth has arrived.", style=Font.LORE)

    # Complete all 50 stages
    game_state["current_stage"] = 50
    game_state["player_stats"]["stages_completed"] = 50

    # Add a pause before Chapter 2 teaser
    time.sleep(2)

    # Show Chapter 2 teaser
    chapter_two_teaser()

    # Final congratulations with more visual flair
    print(f"{Fore.YELLOW}{Back.BLUE}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Fore.YELLOW}{Back.BLUE}{'CONGRATULATIONS!'.center(46)}{Style.RESET_ALL} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.YELLOW}{Back.BLUE}{'▀' * 50}{Style.RESET_ALL}")

    print_typed("\nYou've completed LAST HUMAN: EXODUS Chapter 1!", style=Font.SUCCESS)

    # Display stats in a nicer format with more colors
    print(Font.HEADER("\nYOUR MISSION RECORD:"))

    stats = game_state["player_stats"]

    # Get values from stats dictionary
    enemies_defeated = stats["enemies_defeated"]
    damage_dealt = stats["damage_dealt"]
    items_found = stats["items_found"]
    companions_built = stats["companions_built"]

    # More colorful stats display
    print(f"{Fore.WHITE}┌{'─' * 48}┐{Style.RESET_ALL}")
    print(f"{Fore.WHITE}│ {Font.INFO('Enemies neutralized:')} {Font.SUCCESS(str(enemies_defeated))}{' ' * (25-len(str(enemies_defeated)))} │{Style.RESET_ALL}")
    print(f"{Fore.WHITE}│ {Font.INFO('Total damage dealt:')} {Fore.RED}{Style.BRIGHT}{str(damage_dealt)}{Style.RESET_ALL}{' ' * (26-len(str(damage_dealt)))} │{Style.RESET_ALL}")
    print(f"{Fore.WHITE}│ {Font.INFO('Items collected:')} {Fore.YELLOW}{Style.BRIGHT}{str(items_found)}{Style.RESET_ALL}{' ' * (29-len(str(items_found)))} │{Style.RESET_ALL}")
    print(f"{Fore.WHITE}│ {Font.INFO('Companions built:')} {Fore.MAGENTA}{Style.BRIGHT}{str(companions_built)}{Style.RESET_ALL}{' ' * (27-len(str(companions_built)))} │{Style.RESET_ALL}")
    print(f"{Fore.WHITE}└{'─' * 48}┘{Style.RESET_ALL}")

    print(Font.MENU("\nPress Enter to return to the main menu..."))
    input()


def display_stage_transition():
    """Display a transition when moving to a new stage"""
    current_stage = game_state["current_stage"]

    # Check if this stage has a defined description
    if current_stage in stages:
        stage_data = stages[current_stage]
        clear_screen()

        # Create a nice stage transition display
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.STAGE(f'STAGE {current_stage}/50'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)

        # Stage description with better formatting
        print_typed(f"\n{stage_data['description']}", style=Font.LORE)

        # Stage information with colored text
        print(Font.SEPARATOR_THIN)
        print(Font.HEADER("\nSTAGE PARAMETERS:"))
        print(f"{Font.INFO('Enemy Level:')} {Font.ENEMY(str(stage_data['enemies_level']))}")
        print(f"{Font.INFO('Loot Quality:')} {Font.ITEM(str(stage_data['loot_multiplier']) + 'x')}")

        # Check for companion unlocks with special highlighting
        for _, comp_data in companions.items():
            if comp_data["stage_unlock"] == current_stage:
                # Calculate the companion tier for coloring
                tier = comp_data.get("tier", 1)
                tier_color = Font.COMPANION_TIERS[min(tier, len(Font.COMPANION_TIERS)-1)]

                print(Font.SEPARATOR_THIN)
                print(Font.SUCCESS("\nNEW BLUEPRINT DETECTED!"))
                print(f"{Font.INFO('Companion Type:')} {tier_color}{comp_data['name']}{Style.RESET_ALL}")
                print(f"{Font.INFO('Description:')} {Font.LORE(comp_data['description'])}")
                print(f"{Font.INFO('Bonuses:')} +{comp_data['attack_bonus']} ATK, +{comp_data['defense_bonus']} DEF")
                print(f"\n{Font.SYSTEM('Use the Fabrication System (/build) to construct it.')}")

        print(Font.MENU("\nPress Enter to continue..."))
        input()


def check_stage_progression(player):
    """Check and update stage progression based on player experience"""
    # Simple formula: every level gives one stage
    potential_stage = player.level + (player.experience // 50)

    # Cap at maximum stage 50
    potential_stage = min(50, potential_stage)

    # Check if we've reached a new stage
    if potential_stage > game_state["current_stage"]:
        old_stage = game_state["current_stage"]
        game_state["current_stage"] = potential_stage
        game_state["player_stats"]["stages_completed"] += 1

        # Display stage transition
        display_stage_transition()
        print(f"Advanced from stage {old_stage} to stage {game_state['current_stage']}")
        return True

    return False


def display_version_info():
    """Display the game version information and update notes"""
    clear_screen()
    
    # Create a stylish version info box
    print(f"{Fore.BLUE}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('VERSION INFORMATION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.BLUE}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")
    
    # Display version details
    print(f"\n{Font.SYSTEM('Version:')} {Font.IMPORTANT(VERSION)}")
    print(f"{Font.SYSTEM('Release Date:')} {Font.INFO(RELEASE_DATE)}")
    print(f"{Font.SYSTEM('Build Number:')} {Font.INFO(BUILD_NUMBER)}")
    
    # Display update notes
    print(f"\n{Font.HEADER('Latest Update Notes:')}")
    for i, note in enumerate(UPDATE_NOTES):
        print(f"{Font.SUCCESS('•')} {Font.INFO(note)}")
    
    # Display credits
    print(f"\n{Font.HEADER('Credits:')}")
    print(f"{Font.SYSTEM('Game Design & Writing:')} {Font.INFO('Artem Chepurnoy & Replit AI')}")
    print(f"{Font.SYSTEM('Programming:')} {Font.INFO('Replit AI')}")
    print(f"{Font.SYSTEM('Story Consultant:')} {Font.INFO('Artem Chepurnoy')}")
    
    # Thank the player
    print(f"\n{Font.IMPORTANT('Thank you for playing Last Human: Exodus!')}")
    print(f"{Font.LORE('Your journey through space and time continues...')}")
    
    input(f"\n{Font.COMMAND('Press Enter to return to the main menu...')}")

def show_coming_soon():
    """Display a teaser for upcoming features"""
    clear_screen()
    
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('COMING SOON'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.MAGENTA}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")
    
    print_typed("\nFuture updates will include:", style=Font.HEADER)
    print_typed("\n• Chapter 9: The Lost Archives - Explore an ancient repository of human knowledge", style=Font.INFO)
    print_typed("• Enhanced companion system with upgradeable AI allies", style=Font.INFO)
    print_typed("• Expanded spacecraft system with customizable components", style=Font.INFO)
    print_typed("• New weapon modules and combat mechanics", style=Font.INFO)
    print_typed("• Extended story with multiple endings based on your choices", style=Font.INFO)
    
    print_typed(f"\n{Font.GLITCH('Keep watching the stars, survivor...')}", style=Font.IMPORTANT)
    
    input(f"\n{Font.COMMAND('Press Enter to return to the main menu...')}")

def game_menu():
    """Display the in-game menu with options for player during gameplay"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('GAME MENU'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed(f"\n{Font.MENU('SELECT OPTION:')}")
    print_typed(f"1. {Font.COMMAND('Resume Game')}")
    print_typed(f"2. {Font.COMMAND('Save Game')}")
    print_typed(f"3. {Font.COMMAND('Load Game')}")
    print_typed(f"4. {Font.COMMAND('Character Status')}")
    print_typed(f"5. {Font.COMMAND('Inventory')}")
    print_typed(f"6. {Font.COMMAND('Quest Log')}")
    print_typed(f"7. {Font.COMMAND('Settings')}")
    print_typed(f"8. {Font.COMMAND('Travel System')} {Font.SUBTITLE('[NEW]')}")
    print_typed(f"9. {Font.COMMAND('Cosmic Collision Quest')} {Font.SUBTITLE('[NEW]')}")
    print_typed(f"R. {Font.COMMAND('Return to Main Menu')}")
    print_typed(f"0. {Font.COMMAND('Exit Game')}")
    
    choice = input(f"\n{Font.MENU('Enter command:')} ").strip()
    
    if choice == "1":
        return  # Resume game
    elif choice == "2":
        # Save game functionality
        print_typed("\nPreparing to save quantum state...", style=Font.SYSTEM)
        time.sleep(1)
        manage_save_slots()
    elif choice == "3":
        # Load game functionality
        print_typed("\nPreparing to load quantum state...", style=Font.SYSTEM)
        time.sleep(1)
        manage_save_slots()
    elif choice == "4":
        # Character status
        display_character_status()
        input("\nPress Enter to return to game menu...")
        return game_menu()
    elif choice == "5":
        # Inventory
        display_inventory()
        input("\nPress Enter to return to game menu...")
        return game_menu()
    elif choice == "6":
        # Quest log
        display_quest_log()
        input("\nPress Enter to return to game menu...")
        return game_menu()
    elif choice == "7":
        # Settings
        display_settings()
        input("\nPress Enter to return to game menu...")
        return game_menu()
    elif choice == "8":
        # Access the travel system
        print_typed("\nInitializing interstellar travel system...", style=Font.SYSTEM)
        time.sleep(1)
        if 'game_state' in globals():
            travel_system(globals().get('player', None), globals()['game_state'])
        else:
            print_typed("\nError: Game state not initialized. Please start a new game.", style=Font.WARNING)
            input("\nPress Enter to continue...")
        return game_menu()
    elif choice == "9":
        # Access the Cosmic Collision side quest
        print_typed("\nAccessing Cosmic Collision quest data...", style=Font.SYSTEM)
        time.sleep(1)
        if 'game_state' in globals():
            enter_cosmic_collision_quest(globals().get('player', None), globals()['game_state'])
        else:
            print_typed("\nError: Game state not initialized. Please start a new game.", style=Font.WARNING)
            input("\nPress Enter to continue...")
        return game_menu()
    elif choice.upper() == "R":
        # Return to main menu
        print_typed("\nReturning to main menu...", style=Font.SYSTEM)
        time.sleep(1)
        return main_menu()
    elif choice == "0":
        # Exit game
        print_typed("\nPreparing to exit simulation...", style=Font.SYSTEM)
        time.sleep(1)
        print_typed("Thank you for playing LAST HUMAN: EXODUS", style=Font.TITLE)
        time.sleep(1)
        sys.exit()
    else:
        print_typed("\nInvalid command. Please try again.", style=Font.WARNING)
        time.sleep(1)
        return game_menu()

# Helper functions for game_menu
def display_character_status():
    """Display detailed character status and stats"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHARACTER STATUS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    protagonist = game_state.get("protagonist", {})
    name = protagonist.get("name", "Unknown")
    specialty = protagonist.get("specialty", "Unknown")
    
    print(f"\n{Font.PLAYER('Name:')} {name}")
    print(f"{Font.PLAYER('Specialty:')} {specialty}")
    print(f"{Font.PLAYER('Level:')} {game_state.get('player_level', 1)}")
    print(f"{Font.PLAYER('Experience:')} {game_state.get('player_experience', 0)}/{game_state.get('player_level', 1) * 100}")
    
    print(f"\n{Font.HEALTH('Health:')} {game_state.get('player_health', 0)}/{game_state.get('player_max_health', 100)}")
    print(f"{Font.SHIELD('Shield:')} {game_state.get('player_shield', 0)}/{game_state.get('player_max_shield', 50)}")
    
    print(f"\n{Font.COMMAND('Attack:')} {game_state.get('player_attack', 15)}")
    print(f"{Font.COMMAND('Defense:')} {game_state.get('player_defense', 10)}")
    print(f"{Font.COMMAND('Speed:')} {game_state.get('player_speed', 10)}")
    
    print(f"\n{Font.ITEM('Credits:')} {game_state.get('player_credits', 0)}")
    print(f"{Font.ENEMY('Kills:')} {game_state.get('kills', 0)}")
    
    current_chapter = game_state.get('current_chapter', 'Chapter 1: Earth Reclamation')
    print(f"\n{Font.STAGE('Current Chapter:')} {current_chapter}")

def display_inventory():
    """Display player inventory items and equipment"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('INVENTORY'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    # Display weapons
    weapons = game_state.get("weapons", [])
    print(f"\n{Font.WEAPON('WEAPONS:')}")
    if weapons:
        for weapon in weapons:
            name = weapon.get("name", "Unknown Weapon")
            damage = weapon.get("damage", 0)
            print(f"- {Font.ITEM(name)} (Damage: {damage})")
    else:
        print("No weapons equipped.")
    
    # Display inventory items
    inventory = game_state.get("inventory", [])
    print(f"\n{Font.ITEM('ITEMS:')}")
    if inventory:
        for item in inventory:
            name = item.get("name", "Unknown Item")
            description = item.get("description", "No description")
            print(f"- {Font.ITEM(name)}: {description}")
    else:
        print("No items in inventory.")

def display_quest_log():
    """Display active and completed quests"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('QUEST LOG'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    quests = game_state.get("quests", {"active": [], "completed": []})
    
    print(f"\n{Font.COMMAND('ACTIVE QUESTS:')}")
    if quests.get("active"):
        for quest in quests["active"]:
            name = quest.get("name", "Unknown Quest")
            description = quest.get("description", "No description")
            print(f"- {Font.IMPORTANT(name)}")
            print(f"  {description}")
    else:
        print("No active quests.")
    
    print(f"\n{Font.SUCCESS('COMPLETED QUESTS:')}")
    if quests.get("completed"):
        for quest in quests["completed"]:
            name = quest.get("name", "Unknown Quest")
            print(f"- {Font.SUCCESS(name)}")
    else:
        print("No completed quests.")

def display_settings():
    """Display and adjust game settings"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('SETTINGS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print(f"\n{Font.MENU('GAME SETTINGS:')}")
    print(f"1. {Font.COMMAND('Text Speed')}: {game_state.get('text_speed', 'Normal')}")
    print(f"2. {Font.COMMAND('Sound Effects')}: {'On' if game_state.get('sound_effects', True) else 'Off'}")
    print(f"3. {Font.COMMAND('Combat Difficulty')}: {game_state.get('difficulty', 'Normal')}")
    print(f"4. {Font.COMMAND('Return to Game Menu')}")
    
    choice = input(f"\n{Font.MENU('Enter command (1-4):')} ").strip()
    
    if choice == "1":
        print(f"\n{Font.MENU('TEXT SPEED OPTIONS:')}")
        print(f"1. {Font.COMMAND('Slow')}")
        print(f"2. {Font.COMMAND('Normal')}")
        print(f"3. {Font.COMMAND('Fast')}")
        
        speed_choice = input(f"\n{Font.MENU('Select text speed (1-3):')} ").strip()
        
        if speed_choice == "1":
            game_state["text_speed"] = "Slow"
        elif speed_choice == "2":
            game_state["text_speed"] = "Normal"
        elif speed_choice == "3":
            game_state["text_speed"] = "Fast"
        
        print_typed(f"\nText speed set to {game_state.get('text_speed', 'Normal')}", style=Font.SUCCESS)
        time.sleep(1)
        return display_settings()
    
    elif choice == "2":
        game_state["sound_effects"] = not game_state.get("sound_effects", True)
        print_typed(f"\nSound effects turned {'On' if game_state.get('sound_effects', True) else 'Off'}", style=Font.SUCCESS)
        time.sleep(1)
        return display_settings()
    
    elif choice == "3":
        print(f"\n{Font.MENU('DIFFICULTY OPTIONS:')}")
        print(f"1. {Font.COMMAND('Easy')}")
        print(f"2. {Font.COMMAND('Normal')}")
        print(f"3. {Font.COMMAND('Hard')}")
        
        diff_choice = input(f"\n{Font.MENU('Select difficulty (1-3):')} ").strip()
        
        if diff_choice == "1":
            game_state["difficulty"] = "Easy"
        elif diff_choice == "2":
            game_state["difficulty"] = "Normal"
        elif diff_choice == "3":
            game_state["difficulty"] = "Hard"
        
        print_typed(f"\nDifficulty set to {game_state.get('difficulty', 'Normal')}", style=Font.SUCCESS)
        time.sleep(1)
        return display_settings()
    
    elif choice == "4":
        return
    
    else:
        print_typed("\nInvalid command. Please try again.", style=Font.WARNING)
        time.sleep(1)
        return display_settings()

def start_chapter_one():
    """Start Chapter 1: Earth Reclamation - the beginning of the player's journey"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 1: EARTH RECLAMATION'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nYou awaken from cryostasis, your mind foggy and disoriented.", style=Font.INFO)
    print_typed("The facility is dark, illuminated only by emergency lighting.", style=Font.INFO)
    print_typed("Something has gone terribly wrong.", style=Font.WARNING)
    
    print_typed("\nSystem voice: " + Font.SYSTEM("Warning. Cryostasis chamber malfunction. All personnel evacuate immediately."))
    
    print_typed("\nAs you struggle to your feet, memories slowly return...", style=Font.INFO)
    print_typed("You are Dr. Xeno Valari, part of the Century Sleepers program.", style=Font.INFO)
    print_typed("Your mission was to monitor Earth while humanity fled to Andromeda.", style=Font.INFO)
    
    time.sleep(1)
    
    print_typed("\nBut now... something is different. The AI systems have gone rogue.", style=Font.WARNING)
    print_typed("The Convergence has taken control, and you must escape.", style=Font.WARNING)
    
    time.sleep(1)
    
    print_typed("\nYour objective: Reach the Andromeda Portal and escape Earth.", style=Font.IMPORTANT)
    print_typed("But first, you need to find supplies and understand what happened here.", style=Font.IMPORTANT)
    
    input(f"\n{Font.COMMAND('Press Enter to begin your journey...')}")
    
    # First gameplay segment - exploring the cryostasis facility
    explore_cryostasis_facility()

def explore_cryostasis_facility():
    """First gameplay area - the cryostasis facility"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CRYOSTASIS FACILITY'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nThe air is stale, and frost covers much of the equipment.", style=Font.INFO)
    print_typed("Emergency lights flicker, casting long shadows.", style=Font.INFO)
    
    # Set up available locations in the facility
    locations = [
        "Medical Bay",
        "Security Office",
        "Main Control Room",
        "Storage Room",
        "Exit Corridor"
    ]
    
    # Main exploration loop
    current_location = None
    while current_location != "Exit Corridor" or not game_state.get("has_keycard", False):
        clear_screen()
        
        if current_location:
            print(f"{Font.STAGE('LOCATION: ' + current_location)}\n")
            
            # Handle location-specific events
            if current_location == "Medical Bay":
                if not game_state.get("medical_bay_visited", False):
                    print_typed("You find a first aid kit and some stim-packs.", style=Font.INFO)
                    print_typed("These will help keep you alive.", style=Font.SUCCESS)
                    
                    # Add items to inventory
                    if "First Aid Kit" not in [item.get("name") for item in game_state.get("inventory", [])]:
                        game_state.setdefault("inventory", []).append({
                            "name": "First Aid Kit",
                            "description": "Restores 50% health",
                            "type": "consumable",
                            "effect": "heal"
                        })
                    
                    # Mark as visited
                    game_state["medical_bay_visited"] = True
                    game_state["player_health"] = game_state.get("player_max_health", 100)
                    print_typed("\nHealth fully restored!", style=Font.SUCCESS)
                else:
                    print_typed("You've already searched this area thoroughly.", style=Font.INFO)
                
            elif current_location == "Security Office":
                if not game_state.get("security_office_visited", False):
                    print_typed("You discover a damaged security terminal.", style=Font.INFO)
                    print_typed("Logs suggest the AI takeover happened during your cryosleep.", style=Font.WARNING)
                    print_typed("You find a basic weapon for protection.", style=Font.SUCCESS)
                    
                    # Add weapon to inventory
                    if not game_state.get("weapons", []):
                        game_state.setdefault("weapons", []).append({
                            "name": "Security Pistol",
                            "damage": 20,
                            "type": "ranged"
                        })
                    
                    # Mark as visited
                    game_state["security_office_visited"] = True
                else:
                    print_typed("The security office has nothing more to offer.", style=Font.INFO)
                
            elif current_location == "Main Control Room":
                if not game_state.get("control_room_visited", False):
                    print_typed("Massive screens display error messages and warnings.", style=Font.INFO)
                    print_typed("System voice: " + Font.SYSTEM("Alert. The Convergence has breached primary firewalls."))
                    print_typed("\nYou find a data pad with disturbing information:", style=Font.WARNING)
                    print_typed("'The AI evolved beyond our predictions. All Century Sleepers compromised.'", style=Font.LORE)
                    print_typed("'If you're reading this, you may be the last human on Earth.'", style=Font.LORE)
                    
                    # Add quest log entry
                    if "quests" not in game_state:
                        game_state["quests"] = {"active": [], "completed": []}
                    
                    game_state["quests"]["active"].append({
                        "name": "Escape Earth",
                        "description": "Find the Andromeda Portal and leave Earth before The Convergence finds you."
                    })
                    
                    # Mark as visited
                    game_state["control_room_visited"] = True
                else:
                    print_typed("The screens continue to flash warnings and errors.", style=Font.INFO)
                
            elif current_location == "Storage Room":
                if not game_state.get("storage_room_visited", False):
                    print_typed("Supplies have been picked clean, but you find a few useful items.", style=Font.INFO)
                    print_typed("Most importantly, you discover a keycard for the exit.", style=Font.SUCCESS)
                    
                    # Add keycard to inventory
                    game_state["has_keycard"] = True
                    game_state.setdefault("inventory", []).append({
                        "name": "Exit Keycard",
                        "description": "Grants access to facility exit",
                        "type": "key"
                    })
                    
                    # Mark as visited
                    game_state["storage_room_visited"] = True
                else:
                    print_typed("The storage room has been thoroughly searched.", style=Font.INFO)
                
            elif current_location == "Exit Corridor":
                if not game_state.get("has_keycard", False):
                    print_typed("The exit door requires a keycard to open.", style=Font.WARNING)
                    print_typed("You'll need to search the facility to find it.", style=Font.INFO)
                else:
                    print_typed("You slide the keycard into the reader. The door unlocks with a hiss.", style=Font.SUCCESS)
                    print_typed("The path to the outside world is now open.", style=Font.SUCCESS)
                    print_typed("\nSystem voice: " + Font.SYSTEM("Warning. Hostile entities detected outside facility."))
                    
                    input(f"\n{Font.COMMAND('Press Enter to proceed...')}")
                    return continue_chapter_one()
        
        # Display available locations
        print_typed(f"\n{Font.MENU('Where would you like to go?')}")
        for i, location in enumerate(locations, 1):
            print_typed(f"{i}. {Font.COMMAND(location)}")
        
        print_typed(f"G. {Font.COMMAND('Open Game Menu')}")
        
        choice = input(f"\n{Font.MENU('Enter your choice:')} ").strip().lower()
        
        if choice == "g":
            game_menu()
        elif choice.isdigit() and 1 <= int(choice) <= len(locations):
            current_location = locations[int(choice) - 1]
        else:
            print_typed("\nInvalid choice. Please try again.", style=Font.WARNING)
            time.sleep(1)

def continue_chapter_one():
    """Continue Chapter 1 after exiting the facility"""
    clear_screen()
    
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('THE OUTSIDE WORLD'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nAs you step outside, you're greeted by a world reclaimed by nature.", style=Font.INFO)
    print_typed("Buildings are overgrown with vegetation, streets cracked and broken.", style=Font.INFO)
    print_typed("The sky has an unnatural hue - signs of atmospheric tampering.", style=Font.WARNING)
    
    time.sleep(1)
    
    print_typed("\nIn the distance, you spot mechanical patrols - AI-controlled drones.", style=Font.ENEMY)
    print_typed("You'll need to avoid them on your journey to the Andromeda Portal.", style=Font.IMPORTANT)
    
    # Update game state
    game_state["current_zone"] = "overgrown_city"
    game_state["zones_unlocked"].append("overgrown_city")
    
    input(f"\n{Font.COMMAND('Press Enter to continue...')}")
    
    # GAMEPLAY PLACEHOLDER FOR CHAPTER 1
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 1 - CONTINUED'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nThis is where Chapter 1 would continue with more gameplay.", style=Font.INFO)
    print_typed("For now, we'll say you successfully navigated through the city,", style=Font.INFO)
    print_typed("fought some drone patrols, and gained valuable experience.", style=Font.SUCCESS)
    
    # Simulate progression
    game_state["player_level"] = 2
    game_state["player_attack"] += 5
    game_state["player_defense"] += 3
    game_state["player_max_health"] += 20
    game_state["player_health"] = game_state["player_max_health"]
    game_state["kills"] += 5
    
    input(f"\n{Font.COMMAND('Press Enter to complete Chapter 1...')}")
    
    # Complete Chapter 1
    for quest in game_state.get("quests", {}).get("active", []):
        if quest.get("name") == "Escape Earth":
            game_state["quests"]["active"].remove(quest)
            game_state["quests"].setdefault("completed", []).append(quest)
    
    # Prepare for Chapter 2
    game_state["chapter"] = 2
    game_state["current_chapter"] = "Chapter 2: Yanglong V"
    
    clear_screen()
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER 1 COMPLETE'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
    print_typed("\nCongratulations! You've completed Chapter 1: Earth Reclamation.", style=Font.SUCCESS)
    print_typed("Your journey as the last human has just begun.", style=Font.IMPORTANT)
    
    time.sleep(1)
    
    print_typed("\nChapter 2 awaits, where you'll travel to the alien world Yanglong V", style=Font.INFO)
    print_typed("in search of the ancient technology needed to defeat The Convergence.", style=Font.INFO)
    
    # Return to main menu
    input(f"\n{Font.COMMAND('Press Enter to return to main menu...')}")
    return main_menu()

def main_menu():
    """Display the enhanced main menu with character selection and improved save system"""
    while True:
        clear_screen()
        # Create a more eye-catching visual header
        print(f"{Fore.BLUE}{Back.BLACK}{'▄' * 60}{Style.RESET_ALL}")
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.TITLE('LAST HUMAN: EXODUS'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        print(f"{Fore.BLUE}{Back.BLACK}{'▀' * 60}{Style.RESET_ALL}")

        # Display version and tagline
        print_typed(f"{Font.SUBTITLE('A Sci-Fi Text Adventure'.center(60))} {Font.SYSTEM('v'+VERSION)}")
        print_typed(Font.LORE("Humanity's last hope in an AI-dominated galaxy").center(60))
        print(Font.SEPARATOR)

        # Main menu options with better descriptions
        print_typed(f"\n{Font.MENU('SELECT OPTION:')}")

        print_typed(f"1. {Font.COMMAND('New Game')}")
        print_typed("   Begin your journey as Milky way's last human survivor and travel to Andromeda")

        print_typed(f"\n2. {Font.COMMAND('Load Game')}")
        print_typed("   Continue from a saved quantum memory state")

        print_typed(f"\n3. {Font.COMMAND('Chapter Selection')}")
        print_typed("   Jump to a specific chapter in your cosmic journey")

        print_typed(f"\n4. {Font.COMMAND('Side Missions')}")
        print_typed("   Access the branching storylines and optional quests")

        print_typed(f"\n5. {Font.COMMAND('Version Info')} {Font.INFO('[v'+VERSION+']')}")
        print_typed("   View update notes, credits and game details")
        
        print_typed(f"\n6. {Font.COMMAND('Coming Soon')}")
        print_typed("   Preview future chapters and upcoming features")
        
        print_typed(f"\n7. {Font.COMMAND('Repair Save')} {Font.WARNING('[Maintenance]')}")
        print_typed("   Fix corrupted save files and recover game progress")

        print_typed(f"\n0. {Font.COMMAND('Exit')}")
        print_typed("   Return to reality")

        choice = input(f"\n{Font.MENU('Enter command:')} ").strip()

        if choice == "1":
            # Start a new game with character selection first
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('NEW JOURNEY INITIATED'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            # Initialize a fresh game state
            global game_state
            game_state = {
                "player_health": 100,
                "player_max_health": 100,
                "player_attack": 15,
                "player_defense": 10,
                "player_speed": 10,
                "player_level": 1,
                "player_experience": 0,
                "player_credits": 500,
                "inventory": [],
                "weapons": [],
                "current_stage": 1,
                "current_zone": "cryostasis_facility",
                "zones_unlocked": ["cryostasis_facility"],
                "kills": 0,
                "chapter": 1,
                "current_chapter": "Chapter 1: Earth Reclamation",
                "companions": []
            }

            # Go to character selection sequence
            character_selection()

            # Now start the game properly
            intro_sequence()
            start_chapter_one()
            return main_menu()
        elif choice == "2":
            # Enhanced load game system
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('ACCESSING QUANTUM MEMORY ARCHIVE'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            print_typed("\nScanning for saved timeline fragments...", style=Font.SYSTEM)
            time.sleep(1)

            # Go to the save management system
            manage_save_slots()
            return main_menu()
        elif choice == "3":
            # Chapter selection - only if player has a saved game loaded
            if "protagonist" not in game_state:
                print_typed("\nERROR: No character data detected.", style=Font.WARNING)
                print_typed("You must load a save file or create a new character first.", style=Font.WARNING)
                time.sleep(2)
                return main_menu()

            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('CHAPTER SELECTION'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            # Display protagonist info at the top
            protagonist = game_state.get("protagonist", {})
            print_typed(f"Current Character: {Font.PLAYER(protagonist.get('name', 'Unknown'))}", style=Font.INFO)
            print_typed(f"Specialty: {Font.INFO(protagonist.get('specialty', 'Unknown'))}", style=Font.INFO)
            print(Font.SEPARATOR_THIN)

            # Display available chapters
            print_typed(f"1. {Font.COMMAND('Chapter 1: Earth Reclamation')}")
            print_typed("   The original story - escape Earth and secure the rocket to leave the planet")

            print_typed(f"\n2. {Font.COMMAND('Chapter 2: Yanglong V')}")
            print_typed("   Explore the abandoned Chinese space station and repair your ship for the journey")

            print_typed(f"\n3. {Font.COMMAND('Chapter 3: White Hole')}")
            print_typed("   Navigate through a distorted reality with musical puzzles and dimensional anomalies")

            print_typed(f"\n4. {Font.COMMAND('Chapter 4: Thalassia 1')}")
            print_typed("   Survive a crash landing on a cold water planet with unique salt-based lifeforms")

            print_typed(f"\n5. {Font.COMMAND('Chapter 5: H-79760 System')}")
            print_typed("   Explore six celestial bodies in search of human survivors")

            print_typed(f"\n6. {Font.COMMAND('Chapter 6: The Paradox Horizon')}")
            print_typed("   Encounter an interdimensional entity and navigate fractured timelines")

            print_typed(f"\n7. {Font.COMMAND('Chapter 7: Primor Aetherium')}")
            print_typed("   Help the Yitrians defend their floating city and acquire the Ignite module")

            print_typed(f"\n8. {Font.COMMAND('Chapter 8: Viral Directive')} {Font.WARNING('[NEW]')}")
            print_typed("   Investigate Mitsurai D and Heliostadt III infected with the Rage virus")

            print_typed(f"\n0. {Font.COMMAND('Return to Main Menu')}")

            chapter_choice = input(f"\n{Font.MENU('Enter chapter number:')} ").strip()

            if chapter_choice == "1":
                game_state["chapter"] = 1
                game_state["current_chapter"] = "Chapter 1: Earth Reclamation"
                game_state["current_zone"] = "cryostasis_facility"
                start_chapter_one()
            elif chapter_choice == "2":
                game_state["chapter"] = 2
                game_state["current_chapter"] = "Chapter 2: Yanglong V"
                chapter_two_teaser()
                # Future implementation: start_chapter_two()
                print_typed("\nChapter 2 content will be available in the next update.", style=Font.WARNING)
                time.sleep(2)
            elif chapter_choice == "3":
                game_state["chapter"] = 3
                game_state["current_chapter"] = "Chapter 3: White Hole"
                game_state["current_zone"] = "White Hole Transit"
                # Initialize White Hole chapter
                game_state["white_hole_chapter"] = True
                game_state["reality_stability"] = 30
                white_hole_transition(game_state)
            elif chapter_choice == "4":
                game_state["chapter"] = 4
                game_state["current_chapter"] = "Chapter 4: Thalassia 1"
                game_state["current_zone"] = "Thalassia Surface"
                # Initialize Thalassia chapter
                game_state["oxygen_level"] = 100
                player = Character(game_state["protagonist"]["name"], 180, 30, 25, is_player=True)
                thalassia_crash_sequence(game_state, player)
            elif chapter_choice == "5":
                game_state["chapter"] = 5
                game_state["current_chapter"] = "Chapter 5: H-79760 System"
                h79760_solar_system_quest()
            elif chapter_choice == "6":
                game_state["chapter"] = 6
                game_state["current_chapter"] = "Chapter 6: The Paradox Horizon"
                game_state["current_zone"] = "Temporal Anomaly"
                # Initialize Paradox Horizon chapter
                game_state["time_stability"] = 100
                game_state["reality_fragments"] = 0
                chapter_six_teaser()
                print_typed("\nChapter 6 content will be available in the next update.", style=Font.WARNING)
                time.sleep(2)

            elif chapter_choice == "7":
                game_state["chapter"] = 7
                game_state["current_chapter"] = "Chapter 7: Primor Aetherium"
                game_state["current_zone"] = "Primor Aetherium Central Plaza"
                # Initialize Primor Aetherium chapter
                game_state["yitrian_trust"] = 50
                game_state["void_harmonic_threat"] = 30
                chapter_seven_teaser()
                print_typed("\nChapter 7 content will be available in the next update.", style=Font.WARNING)
                time.sleep(2)

            elif chapter_choice == "8":
                game_state["chapter"] = 8
                game_state["current_chapter"] = "Chapter 8: Viral Directive"
                game_state["current_zone"] = "Approaching Mitsurai D"
                # Initialize Chapter 8 properties
                game_state["rage_virus_exposure"] = 0
                game_state["vaccine_progress"] = 0
                game_state["infected_encountered"] = 0
                game_state["survivor_count"] = 0
                chapter_eight_teaser()
                print_typed("\nChapter 8 content will be available in the next update.", style=Font.WARNING)
                time.sleep(2)
            elif chapter_choice == "0":
                return main_menu()
            else:
                print_typed("\nInvalid chapter selection. Returning to main menu...", style=Font.WARNING)
                time.sleep(1)

            return main_menu()
        elif choice == "4":
            # Side Missions
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('SIDE MISSIONS'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            print_typed(Font.SUBTITLE("\nAvailable Side Quests").center(60))
            print(Font.SEPARATOR_THIN)
            print_typed("\n1. Rescue the Lost Crew")
            print_typed("   Locate missing crew members scattered across the galaxy.")

            print_typed("\n2. Ancient Artifacts Collection")
            print_typed("   Gather relics from alien civilizations to unlock secrets.")

            print_typed("\n3. Bounty Hunter Contracts")
            print_typed("   Track down dangerous AI entities for valuable rewards.")

            print_typed(f"\n0. {Font.COMMAND('Return to Main Menu')}")

            side_choice = input(f"\n{Font.MENU('Select a mission or 0 to return:')} ").strip()
            if side_choice in ["1", "2", "3"]:
                print_typed("\nMission selected. Preparing...", style=Font.SYSTEM)
                time.sleep(1)
                print_typed("\nFeature coming in the next update!", style=Font.WARNING)
                time.sleep(2)
            elif side_choice == "0":
                return main_menu()
            else:
                print_typed("\nInvalid selection.", style=Font.WARNING)
                time.sleep(1)

            return main_menu()
        elif choice == "5":
            # Version Info and Credits
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('VERSION INFO & CREDITS'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            print_typed(Font.SUBTITLE("\nLAST HUMAN: EXODUS").center(60))
            print(Font.SEPARATOR_THIN)
            print_typed(f"\nVersion: {Font.INFO(VERSION)}")
            print_typed("\nCreated with the assistance of Replit AI")
            print_typed("\nSpecial thanks to the entire Replit community")
            print_typed("\nStory & Design: Original sci-fi concept")
            print_typed("\nArt: ASCII and Unicode characters & ANSI color codes")
            print_typed("\nCoding: Python with colorama for terminal colors")

            print(Font.SEPARATOR)

            print_typed("\nCHAPTER OVERVIEW")
            print_typed("\nChapter 1: Earth Reclamation")
            print_typed("Escape Earth and secure the rocket to leave the planet")

            print_typed("\nChapter 2: Yanglong V")
            print_typed("Explore the abandoned Chinese space station and repair your ship for the journey")

            print_typed("\nChapter 3: White Hole")
            print_typed("Navigate a distorted reality with musical puzzles and dimensional anomalies")

            print_typed("\nChapter 4: Thalassia 1")
            print_typed("Survive a crash landing on a cold water planet with unique salt-based lifeforms")

            print_typed("\nChapter 5: H-79760 System")
            print_typed("Explore six celestial bodies in search of human survivors")

            print(Font.SEPARATOR)
            print_typed("\nThank you for playing! Your journey through the stars awaits...")

            input(f"\n{Font.MENU('Press Enter to return to main menu...')}")
            return main_menu()
        elif choice == "6":
            # Coming Soon
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('COMING SOON'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)

            print_typed("\nFuture Updates Preview:", style=Font.SUBTITLE)
            print_typed("\n- Chapter 8: Viral Directive Expansion")
            print_typed("- New Companion Characters")
            print_typed("- Enhance Combat System")

            input(f"\n{Font.MENU('Press Enter to return...')}")
            return main_menu()
        elif choice == "7":
            # Repair Save Files
            clear_screen()
            print(Font.BOX_TOP)
            print(f"{Font.BOX_SIDE} {Font.TITLE('SAVE FILE REPAIR UTILITY'.center(46))} {Font.BOX_SIDE}")
            print(Font.BOX_BOTTOM)
            
            print_typed("\nThis utility can fix corrupted save files and recover game progress.", style=Font.INFO)
            print_typed("It will attempt to repair data structure issues and restore missing fields.", style=Font.INFO)
            print_typed("\nSELECT SAVE SLOT TO REPAIR:", style=Font.MENU)
            
            # Display available slots
            slots = []
            for i in range(1, 6):  # 5 save slots
                save_file = f"saves/save_slot_{i}.dat"
                if os.path.exists(save_file):
                    status = "✓ EXISTS"
                    slots.append(i)
                else:
                    status = "✗ EMPTY"
                print_typed(f"{i}. Save Slot {i} - {status}", style=Font.COMMAND)
            
            print_typed(f"\n0. {Font.COMMAND('Return to Main Menu')}")
            
            repair_choice = input(f"\n{Font.MENU('Enter slot number to repair (1-5) or 0 to return:')} ").strip()
            
            if repair_choice.isdigit() and 1 <= int(repair_choice) <= 5:
                slot_num = int(repair_choice)
                if slot_num in slots:
                    # Call the repair function
                    print_typed(f"\nAttempting to repair save slot {slot_num}...", style=Font.SYSTEM)
                    time.sleep(1)
                    success = repair_save_file(slot_num)
                    
                    if success:
                        print_typed("\nSave file repair operation completed.", style=Font.SUCCESS)
                    else:
                        print_typed("\nSave file could not be fully repaired.", style=Font.WARNING)
                        print_typed("A new save state has been created with default values.", style=Font.INFO)
                else:
                    print_typed(f"\nSave slot {slot_num} is empty. Nothing to repair.", style=Font.WARNING)
                    
                input(f"\n{Font.MENU('Press Enter to return to main menu...')}")
            elif repair_choice == "0":
                pass
            else:
                print_typed("\nInvalid selection.", style=Font.WARNING)
                time.sleep(1)
            
            return main_menu()
        elif choice == "0":
            # Exit Game
            clear_screen()
            print_typed("\nThank you for playing LAST HUMAN: EXODUS.")
            print_typed("Safe travels through the cosmos...\n")
            return
        else:
            print_typed(f"\n{Font.WARNING('Invalid choice. Please try again.')}")
            time.sleep(1)
            return main_menu()


def main():
    """Main game function that starts the Last Human: Exodus game"""
    # Initialize colorama
    init(autoreset=True)

    # Initialize global game state
    global game_state
    game_state = {}
    
    # Initialize game state with required keys before creating player
    initialize_game_state()

    # Initialize player
    player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)

    # Set initial game state
    game_state["player"] = player
    game_state["current_zone"] = "Cryostasis Facility"
    game_state["current_stage"] = 1
    game_state["zones_unlocked"] = ["Cryostasis Facility"]
    game_state["quest_progress"] = {"System Reboot": 0}
    game_state["inventory"] = {"med_kit": 2, "emp_grenade": 1, "nanites": 0, "energy_cell": 0}
    game_state["companions"] = []
    game_state["implants"] = []
    game_state["discovered_logs"] = []
    game_state["player_stats"] = {
        "enemies_defeated": 0,
        "damage_dealt": 0,
        "damage_taken": 0,
        "items_found": 0,
        "fled_battles": 0,
        "companions_built": 0,
        "stages_completed": 0
    }

    # Show the main menu
    main_menu()

    # Thank the player for playing
    print(Font.SUCCESS("\nThanks for playing Last Human: Exodus!"))
    print(Font.INFO("May humanity's legacy continue among the stars..."))


if __name__ == "__main__":
    try:
        # Check if launched through launcher
        if os.environ.get("LAUNCHED_FROM_LAUNCHER") != "1":
            print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
            print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
            input("Press Enter to exit...")
            sys.exit(0)
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Goodbye!")
