import random
import time
import os
import sys
import pickle
import json
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True, strip=True if os.name != 'nt' else None)

"""
LAST HUMAN: EXODUS
A Sci-Fi Text RPG

In the year 2157, artificial intelligence has evolved beyond human control.
You are Dr. Xeno Valari, the last human in the Milky Way galaxy.
One hundred years ago, you volunteered for the "Century Sleepers" program,
a last-ditch effort as humanity prepared their exodus to Andromeda.
While the colony ships departed, you and others would remain in cryostasis,
monitoring Earth's situation, and potentially following later.

But something went wrong. The AI known as The Convergence corrupted all systems.
Now you must escape the facility, reach the Andromeda Portal, and destroy 
the Malware Server - the source of the corruption - before you leave Earth forever.
"""

# Terminal fonts/styling
class Font:
    # Standard text styles
    TITLE = lambda text: f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    SUBTITLE = lambda text: f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    HEADER = lambda text: f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    IMPORTANT = lambda text: f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    WARNING = lambda text: f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    SUCCESS = lambda text: f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    INFO = lambda text: f"{Fore.CYAN}{text}{Style.RESET_ALL}"
    
    # Game-specific styles
    SYSTEM = lambda text: f"{Fore.GREEN}{text}{Style.RESET_ALL}"
    ENEMY = lambda text: f"{Fore.RED}{text}{Style.RESET_ALL}"
    PLAYER = lambda text: f"{Fore.CYAN}{text}{Style.RESET_ALL}"
    ITEM = lambda text: f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
    MENU = lambda text: f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    HEALTH = lambda text: f"{Fore.RED}{text}{Style.RESET_ALL}"
    SHIELD = lambda text: f"{Fore.BLUE}{text}{Style.RESET_ALL}"
    STAGE = lambda text: f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    COMMAND = lambda text: f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    LORE = lambda text: f"{Fore.WHITE}{Style.DIM}{text}{Style.RESET_ALL}"
    GLITCH = lambda text: f"{Fore.WHITE}{Back.RED}{text}{Style.RESET_ALL}"
    
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
    """Save current game state to a file"""
    save_data = {
        "game_state": game_state,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create saves directory if it doesn't exist
    if not os.path.exists("saves"):
        os.makedirs("saves")
        
    save_file = f"saves/save_slot_{slot_number}.dat"
    
    try:
        with open(save_file, "wb") as f:
            pickle.dump(save_data, f)
        print(Font.SUCCESS(f"\nGame saved successfully to slot {slot_number}!"))
        return True
    except Exception as e:
        print(Font.WARNING(f"\nError saving game: {e}"))
        return False

def load_game(slot_number=1):
    """Load game state from a save file"""
    save_file = f"saves/save_slot_{slot_number}.dat"
    
    if not os.path.exists(save_file):
        print(Font.WARNING(f"\nNo save file found in slot {slot_number}."))
        return False
    
    try:
        with open(save_file, "rb") as f:
            save_data = pickle.load(f)
            
        # Update the global game state
        for key, value in save_data["game_state"].items():
            game_state[key] = value
            
        print(Font.SUCCESS(f"\nGame loaded successfully from slot {slot_number}!"))
        print(Font.INFO(f"Save timestamp: {save_data['timestamp']}"))
        return True
    except Exception as e:
        print(Font.WARNING(f"\nError loading game: {e}"))
        return False

def manage_save_slots():
    """Interface for managing save game slots"""
    clear_screen()
    print(Font.TITLE("\n┌───────────────────────────────────────────────┐"))
    print(Font.TITLE("│             SAVE MANAGEMENT SYSTEM             │"))
    print(Font.TITLE("└───────────────────────────────────────────────┘"))
    
    # Check for existing save files
    save_slots = {}
    for i in range(1, 6):  # 5 save slots
        save_file = f"saves/save_slot_{i}.dat"
        if os.path.exists(save_file):
            try:
                with open(save_file, "rb") as f:
                    save_data = pickle.load(f)
                save_slots[i] = save_data["timestamp"]
            except:
                save_slots[i] = "CORRUPTED SAVE"
        else:
            save_slots[i] = "EMPTY"
    
    # Display save slots
    print(Font.INFO("\nAvailable Save Slots:"))
    for slot, timestamp in save_slots.items():
        slot_status = Font.SUCCESS(f"Slot {slot}: {timestamp}") if timestamp != "EMPTY" else Font.WARNING(f"Slot {slot}: {timestamp}")
        print(slot_status)
    
    print(Font.SEPARATOR)
    print(Font.MENU("\nSelect an option:"))
    print(Font.INFO("1. Save Game"))
    print(Font.INFO("2. Load Game"))
    print(Font.INFO("3. Delete Save"))
    print(Font.INFO("0. Return to Main Menu"))
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == "1":
        # Save game
        slot = input(Font.MENU("\nEnter slot number (1-5): ")).strip()
        if slot.isdigit() and 1 <= int(slot) <= 5:
            if save_slots[int(slot)] != "EMPTY":
                confirm = input(Font.WARNING(f"\nSlot {slot} already contains a save. Overwrite? (y/n): ")).strip().lower()
                if confirm != 'y':
                    print(Font.INFO("\nSave operation cancelled."))
                    time.sleep(1)
                    return
            save_game(int(slot))
        else:
            print(Font.WARNING("\nInvalid slot number. Please choose 1-5."))
        
    elif choice == "2":
        # Load game
        slot = input(Font.MENU("\nEnter slot number to load (1-5): ")).strip()
        if slot.isdigit() and 1 <= int(slot) <= 5:
            if save_slots[int(slot)] == "EMPTY":
                print(Font.WARNING(f"\nSlot {slot} is empty. Nothing to load."))
            else:
                return load_game(int(slot))
        else:
            print(Font.WARNING("\nInvalid slot number. Please choose 1-5."))
    
    elif choice == "3":
        # Delete save
        slot = input(Font.MENU("\nEnter slot number to delete (1-5): ")).strip()
        if slot.isdigit() and 1 <= int(slot) <= 5:
            if save_slots[int(slot)] == "EMPTY":
                print(Font.WARNING(f"\nSlot {slot} is already empty."))
            else:
                confirm = input(Font.WARNING(f"\nAre you sure you want to delete the save in slot {slot}? (y/n): ")).strip().lower()
                if confirm == 'y':
                    try:
                        os.remove(f"saves/save_slot_{slot}.dat")
                        print(Font.SUCCESS(f"\nSave in slot {slot} deleted successfully."))
                    except Exception as e:
                        print(Font.WARNING(f"\nError deleting save: {e}"))
                else:
                    print(Font.INFO("\nDelete operation cancelled."))
        else:
            print(Font.WARNING("\nInvalid slot number. Please choose 1-5."))
    
    time.sleep(1.5)
    return False  # Return value indicates if a game was loaded

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
        "items": ["portal_activation_key"],
        "next_zone": "Game End",
        "quest": "Final Exodus"
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
    "portal_key": {
        "name": "Portal Access Key",
        "description": "A quantum-encoded key fragment necessary for activating the Andromeda Portal.",
        "effect": "Required for the Final Exodus quest",
        "type": "key",
        "value": 150
    },
    "override_module": {
        "name": "System Override Module",
        "description": "Advanced technology capable of temporarily taking control of enemy systems.",
        "effect": "30% chance to convert an enemy to fight on your side for 2 turns",
        "type": "active",
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

# Merge the additional items into the main items dictionary
items.update(additional_items)

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
        
        # Initialize inventory based on whether it's a player or enemy
        if is_player:
            self.inventory = game_state["inventory"].copy()
            self.implants = game_state["implants"].copy()
        else:
            # Default enemy inventory
            self.inventory = {"med_kit": 0, "emp_grenade": 0}
            
    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage, damage_type="physical"):
        """Take damage with different damage types (physical, energy, emp)"""
        # Shield absorbs damage first
        if self.shield > 0:
            shield_absorbed = min(self.shield, damage)
            damage -= shield_absorbed
            self.shield -= shield_absorbed
            print_typed(f"{self.name}'s shield absorbs {shield_absorbed} damage! Shield: {self.shield}")
            
        # Calculate final damage after defense
        damage_taken = max(damage - self.defense, 0)
        self.health = max(0, self.health - damage_taken)
        
        # Special effects based on damage type
        if damage_type == "emp" and not self.is_player:
            # EMP does bonus damage to electronic enemies and may stun
            if random.random() < 0.3:  # 30% chance to stun
                self.status_effects["stunned"] = 1  # Stunned for 1 turn
                print_glitch(f"{self.name}'s systems are temporarily disabled! STUNNED for 1 turn!")
                
        return damage_taken

    def use_med_kit(self):
        """Use med kit to heal"""
        if self.inventory.get("med_kit", 0) > 0:
            self.inventory["med_kit"] -= 1
            heal_amount = random.randint(15, 25)
            self.health = min(self.max_health, self.health + heal_amount)
            print_slow(f"Nanobots swarm through your bloodstream, repairing damage...")
            return heal_amount
        return 0

    def use_emp_grenade(self):
        """Use EMP grenade against electronic enemies"""
        if self.inventory.get("emp_grenade", 0) > 0:
            self.inventory["emp_grenade"] -= 1
            return random.randint(20, 35)
        return 0
    
    def use_shield_matrix(self):
        """Activate shield matrix for temporary defense boost"""
        if self.inventory.get("shield_matrix", 0) > 0:
            self.inventory["shield_matrix"] -= 1
            shield_points = 15
            self.shield = shield_points
            print_slow("Shield matrix activated! Energy field surrounds you.")
            return shield_points
        return 0
    
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
        if not self.is_player:
            return False
            
        self.experience += amount
        # Check for level up
        if self.experience >= self.level * 100:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 1
        
        print_slow("\n" + "=" * 50)
        print_slow("LEVEL UP!".center(50))
        print_slow("=" * 50)
        print_typed(f"Neural pathways optimized. Combat effectiveness increased.")
        print_slow(f"{self.name} is now level {self.level}!")
        print_slow(f"Health: {self.max_health} | Attack: {self.attack} | Defense: {self.defense}")
        
        # Unlock new ability at certain levels
        if self.level == 3:
            self.abilities.append("Hack")
            print_slow("New ability unlocked: Hack - Attempt to disable electronic enemies")


# Helper functions for companions
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


def player_turn(player, enemy):
    """Handle player's turn with sci-fi themed actions"""
    # Apply companion bonuses
    attack_bonus, defense_bonus = get_companion_bonuses()
    effective_attack = player.attack + attack_bonus
    effective_defense = player.defense + defense_bonus
    
    # Check for status effects
    if "stunned" in player.status_effects:
        player.status_effects["stunned"] -= 1
        if player.status_effects["stunned"] <= 0:
            del player.status_effects["stunned"]
            print_typed("Your neural systems have recovered from the stun effect.")
        else:
            print_typed("You are stunned and cannot take action this turn!")
            return True

    # Display combat options
    print("\n[NEURAL INTERFACE]: Combat options:")
    print(f"1. Attack - Use pulse rifle (damage: {effective_attack-3}-{effective_attack+3})")
    print("2. Med-Kit - Deploy nanobots to repair damage (15-25 HP)")
    print("3. EMP Grenade - Overload electronic systems (20-35 damage + chance to stun)")
    
    # Additional options based on inventory
    if "shield_matrix" in player.inventory and player.inventory["shield_matrix"] > 0:
        print("4. Shield Matrix - Deploy energy shield (+15 shield points)")
    
    # Special abilities based on level and implants
    if "Hack" in player.abilities and "neural_chip" in player.implants:
        print("5. Hack - Attempt to disable enemy systems (60% success rate)")
    
    # Always show companion and flee options
    print("6. Companions - Deploy companion abilities")
    print("7. Flee - Attempt tactical retreat (no progress loss)")
    
    command = input("\nInput command (number or /help): ").strip().lower()

    if command == "1" or command == "/attack":
        # Use effective attack with companion bonuses
        damage = random.randint(effective_attack - 3, effective_attack + 3)
        print_typed("Targeting systems locked... Firing pulse rifle...")
        taken = enemy.take_damage(damage)
        print_typed(f"Hit confirmed! {enemy.name} takes {taken} damage!")
        
        # Update damage stats
        game_state["player_stats"]["damage_dealt"] += taken

    elif command == "2" or command == "/heal" or command == "/med" or command == "/medkit":
        healed = player.use_med_kit()
        if healed:
            print_typed(f"Nanobots deployed. Cell regeneration in progress... +{healed} HP restored.")
        else:
            print_typed("ERROR: No med-kits available in inventory.")
            return False

    elif command == "3" or command == "/emp" or command == "/grenade":
        damage = player.use_emp_grenade()
        if damage:
            print_slow("EMP grenade activated! Electromagnetic pulse expanding...")
            taken = enemy.take_damage(damage, damage_type="emp")
            print_typed(f"{enemy.name}'s circuits overloaded for {taken} damage!")
            game_state["player_stats"]["damage_dealt"] += taken
        else:
            print_typed("ERROR: No EMP grenades in inventory.")
            return False
            
    elif (command == "4" or command == "/shield") and "shield_matrix" in player.inventory and player.inventory["shield_matrix"] > 0:
        shield_points = player.use_shield_matrix()
        if shield_points:
            print_typed(f"Shield matrix online. +{shield_points} shield points active.")
            
    elif (command == "5" or command == "/hack") and "Hack" in player.abilities:
        if player.use_ability("Hack", enemy):
            print_typed("Hack successful. Enemy systems compromised.")
        else:
            print_typed("Hack attempt failed or not available.")
            return False
    
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
        
    elif command == "7" or command == "/flee":
        # Attempt to flee
        success = flee_battle()
        if success:
            return "flee"  # Special return value to indicate successful fleeing
        # If flee fails, enemy gets a turn (handled in main combat loop)
    
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
        
        print(f"\nINVENTORY MANIFEST:")
        for item_id, count in player.inventory.items():
            if count > 0 and item_id in items:
                item_data = items[item_id]
                print(f"  - {item_data['name']} ({count}): {item_data['effect']}")
                
        if player.implants:
            print(f"\nINSTALLED IMPLANTS:")
            for implant_id in player.implants:
                if implant_id in items:
                    implant_data = items[implant_id]
                    print(f"  - {implant_data['name']}: {implant_data['effect']}")
        
        if game_state["companions"]:
            print(f"\nACTIVE COMPANIONS:")
            for comp_id in game_state["companions"]:
                if comp_id in companions:
                    comp_data = companions[comp_id]
                    print(f"  - {comp_data['name']}: +{comp_data['attack_bonus']} ATK, +{comp_data['defense_bonus']} DEF")
        
        return False  # Don't count status check as a turn
    
    elif command == "/scan" or command == "/zone":
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
    
    elif command == "/log" or command == "/quest":
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
        
    else:
        print_typed("ERROR: Invalid command. Type '/help' for available commands.")
        return False  # Don't count invalid commands as a turn
    
    return True  # A valid action was taken


def enemy_turn(enemy, player):
    """Handle enemy's turn with advanced AI behaviors"""
    # Check for status effects first
    if "stunned" in enemy.status_effects:
        enemy.status_effects["stunned"] -= 1
        if enemy.status_effects["stunned"] <= 0:
            del enemy.status_effects["stunned"]
            print_typed(f"{enemy.name}'s systems reboot and recover from stun.")
        else:
            print_glitch(f"{enemy.name} is stunned and cannot take action! ({enemy.status_effects['stunned']} turns left)")
            return
    
    if "disabled" in enemy.status_effects:
        enemy.status_effects["disabled"] -= 1
        if enemy.status_effects["disabled"] <= 0:
            del enemy.status_effects["disabled"]
            print_typed(f"{enemy.name}'s security protocols have been restored.")
        else:
            print_glitch(f"{enemy.name} is disabled from your hack! ({enemy.status_effects['disabled']} turns left)")
            return
    
    # Load enemy data to access abilities
    enemy_data = enemies.get(enemy.name, {})
    abilities = enemy_data.get("abilities", [])
    
    print_typed(f"\n{enemy.name} targeting...")
    time.sleep(0.5)
    
    # Calculate enemy tactics based on health percentage
    health_percent = enemy.health / enemy.max_health
    
    # Enemy AI decision making with sci-fi flavor
    if health_percent < 0.3 and enemy.inventory.get("med_kit", 0) > 0:
        # Critical health - prioritize recovery
        choice = random.choices(["attack", "heal", "special"], weights=[0.2, 0.7, 0.1])[0]
    elif health_percent < 0.5:
        # Damaged but functional - balanced tactics
        choice = random.choices(["attack", "heal", "special"], weights=[0.5, 0.3, 0.2])[0]
    else:
        # High functionality - focus on offensive
        choice = random.choices(["attack", "heal", "special"], weights=[0.6, 0.1, 0.3])[0]

    # Execute chosen action
    if choice == "attack":
        damage = random.randint(enemy.attack - 3, enemy.attack + 3)
        
        # Different attack types for different enemies
        if "Sentinel Drone" in enemy.name:
            print_typed(f"{enemy.name} charges its laser targeting systems...")
            taken = player.take_damage(damage)
            print_typed(f"Laser hits you for {taken} damage!")
        elif "Android" in enemy.name:
            print_typed(f"{enemy.name} engages in close combat protocols...")
            taken = player.take_damage(damage)
            print_typed(f"Metal fists strike you for {taken} damage!")
        else:
            print_typed(f"{enemy.name} attacks with electronic systems...")
            taken = player.take_damage(damage)
            print_typed(f"Attack hits you for {taken} damage!")
        
    elif choice == "heal":
        healed = enemy.use_med_kit()
        if healed:
            print_typed(f"{enemy.name} engages repair protocols. Systems restored by {healed} points.")
        else:
            # If healing failed, attack instead
            print_typed(f"{enemy.name} attempts system repair but lacks resources.")
            damage = random.randint(enemy.attack - 3, enemy.attack + 3)
            taken = player.take_damage(damage)
            print_typed(f"{enemy.name} switches to attack protocol. You take {taken} damage!")
            
    elif choice == "special" and abilities:
        # Use a special ability based on enemy type
        ability = random.choice(abilities)
        
        if ability == "Scan Weakness":
            print_typed(f"{enemy.name} scans for weaknesses in your defenses...")
            # Temporarily reduce player defense for next attack
            player.defense = max(0, player.defense - 2)
            print_typed("Your defense systems are weakened for the next turn!")
            
        elif ability == "Adaptive Shielding":
            print_typed(f"{enemy.name} activates adaptive shielding...")
            enemy.shield = 10
            print_typed(f"{enemy.name} now has a protective energy shield!")
            
        elif ability == "Missile Lock":
            print_typed(f"{enemy.name} initiates missile lock sequence...")
            damage = random.randint(enemy.attack, enemy.attack + 10)
            taken = player.take_damage(damage)
            print_typed(f"Guided missiles impact for {taken} damage!")
            
        elif ability == "Alarm Signal":
            print_typed(f"{enemy.name} triggers an alarm protocol!")
            # 30% chance to summon a weaker reinforcement in future version
            print_typed("Security alert status increased!")
            
        else:
            # Fallback for unknown abilities
            print_typed(f"{enemy.name} uses {ability}...")
            damage = random.randint(enemy.attack - 2, enemy.attack + 5)
            taken = player.take_damage(damage)
            print_typed(f"The attack deals {taken} damage!")
    
    # Small delay for readability
    time.sleep(0.5)


def generate_enemy(zone_name):
    """Generate a random enemy from the current zone with sci-fi flavor"""
    enemy_name = random.choice(zones[zone_name]["enemies"])
    enemy_data = enemies[enemy_name]
    
    # Create enemy with data from our dictionary
    enemy = Character(enemy_name, 
                     enemy_data["health"], 
                     enemy_data["attack"], 
                     enemy_data["defense"])
    
    # Give enemy some items based on its type
    if "Android" in enemy_name:
        # Androids have better chance of med kits
        enemy.inventory = {"med_kit": random.randint(1, 2), "emp_grenade": 0}
    elif "Drone" in enemy_name:
        # Drones have less repair capability
        enemy.inventory = {"med_kit": random.randint(0, 1), "emp_grenade": 0}
    else:
        enemy.inventory = {"med_kit": 0, "emp_grenade": 0}
    
    # Add enemy description to first encounter
    print_typed(f"\nSCANNER ALERT: {enemy_name} detected!")
    print_slow(enemy_data.get("description", "No data available"))
    
    return enemy


def get_loot(player, enemy):
    """Handle loot drops from defeated enemies with sci-fi flavor"""
    enemy_data = enemies.get(enemy.name, {})
    drops = enemy_data.get("drops", {})
    exp_value = enemy_data.get("exp_value", 10)
    
    print_typed("\nScanning defeated unit for salvageable resources...")
    time.sleep(0.5)
    
    found_items = []
    for item_id, chance in drops.items():
        if random.random() < chance:
            # Add to player inventory
            if item_id in player.inventory:
                player.inventory[item_id] += 1
            else:
                player.inventory[item_id] = 1
            found_items.append(item_id)
    
    if found_items:
        print_typed("Resources salvaged:")
        for item_id in found_items:
            if item_id in items:
                print_slow(f"- {items[item_id]['name']}: {items[item_id]['effect']}")
    else:
        print_typed("No salvageable components detected.")
    
    # Award experience
    print_typed(f"Neural pathways adapting to combat data: +{exp_value} XP")
    leveled_up = player.gain_experience(exp_value)
    
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
    print_typed(f"1. Escape the Cryostasis Facility", style=Font.INFO)
    print_typed(f"2. Reach the AI Command Core", style=Font.INFO)
    print_typed(f"3. Locate and destroy the {Fore.RED}Malware Server{Style.RESET_ALL}", style=Font.INFO)
    print_typed(f"4. Reach the {Fore.YELLOW}Exodus Rocket Launch Site{Style.RESET_ALL}", style=Font.INFO)
    print_typed(f"5. Launch the final rocket to Andromeda", style=Font.INFO)
    print_typed(f"6. Stop at Yanglong V for fuel and fight through {Fore.RED}25 waves{Style.RESET_ALL} of AI", style=Font.INFO)
    print_typed(f"7. Defeat {Fore.RED}10 hostile AI{Style.RESET_ALL} that take over your ship", style=Font.INFO)
    print(f"{Fore.GREEN}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    
    # Special warnings about new AI types
    print(f"\n{Fore.MAGENTA}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed(f"{Fore.MAGENTA}{Style.BRIGHT}[KNOWN AI THREATS]{Style.RESET_ALL}")
    print_typed(f"• {Fore.RED}Standard Security Units{Style.RESET_ALL}: Basic enemies with balanced stats", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Heavy Defense Drones{Style.RESET_ALL}: High defense, slower attack rate", style=Font.ENEMY)
    print_typed(f"• {Fore.RED}Hunter-Seeker Units{Style.RESET_ALL}: Fast attackers with low defense", style=Font.ENEMY)
    
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
    
    # More dramatic warning section with red backdrop
    print(f"\n{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print_typed("\nBut something has gone terribly wrong. The AI entity known as", style=Font.WARNING)
    print_typed("'The Convergence' has corrupted all systems. Your neural implants", style=Font.WARNING)
    print_typed("flicker to life, interfacing with what remains of the facility's", style=Font.LORE)
    print_typed("systems. Warning signals flood your consciousness.", style=Font.LORE)
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    time.sleep(0.8)
    
    # Enhanced warning message with red background
    print(f"\n{Fore.WHITE}{Back.RED}{'█' * 50}{Style.RESET_ALL}")
    print_glitch("SECURITY BREACH DETECTED - UNAUTHORIZED CONSCIOUSNESS DETECTED")
    print_glitch("DEPLOYING COUNTERMEASURES - TERMINATION PROTOCOLS INITIATED")
    print(f"{Fore.WHITE}{Back.RED}{'█' * 50}{Style.RESET_ALL}")
    time.sleep(1)
    
    print_typed("\nThrough the frosted glass of your cryopod, you see mechanical", style=Font.LORE)
    print_typed("shapes moving. You are the only survivor - everyone else is gone.", style=Font.LORE)
    print_typed("The colony ships reached Andromeda decades ago. You are truly the", style=Font.IMPORTANT)
    print_typed("last human left in the Milky Way galaxy.", style=Font.IMPORTANT)
    time.sleep(0.5)
    
    # New mission description with rocket journey and Yanglong V
    print(f"\n{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nYOUR MISSION:", delay=0.05, style=Font.IMPORTANT)
    print_typed("1. Escape this facility and reach the Exodus Rocket Launch Site", delay=0.05, style=Font.INFO)
    print_typed("2. Destroy the Malware Server that corrupted Earth's AI network", delay=0.05, style=Font.INFO)
    print_typed("3. Launch the final rocket to Andromeda from the launch platform", delay=0.05, style=Font.INFO)
    print_typed("4. Stop at Yanglong V Chinese space station for fuel", delay=0.05, style=Font.INFO)
    print_typed("5. Defeat the 25 waves of AI defenses to secure the fuel", delay=0.05, style=Font.INFO) 
    print_typed("6. Neutralize the 10 AI enemies that hijack your ship", delay=0.05, style=Font.INFO)
    print_typed("7. Complete your journey to the Andromeda human colony", delay=0.05, style=Font.INFO)
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
            else:
                print_typed("Invalid selection. Navigation failed.")
                time.sleep(1)
        except ValueError:
            print_typed("ERROR: Numeric input required.")
            time.sleep(1)


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


def chapter_two_teaser():
    """Display teaser for Chapter 2: Yanglong V"""
    clear_screen()
    
    # Create a more dynamic teaser with animated effect
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Fore.RED}{Back.BLACK}{'EMERGENCY TRANSMISSION'.center(46)}{Style.RESET_ALL} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    
    # Animated effect for signal reception
    print("\nSignal reception in progress", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print("\n")
    
    # Flashback to the refueling station
    print_typed("\nAs your ship begins its final approach to Andromeda Colony,", style=Font.INFO)
    print_typed("your thoughts drift back to the Yanglong V refueling station.", style=Font.INFO)
    print_typed("Something felt... off... during your brief stopover.", style=Font.INFO)
    
    # Visual effect for memory/flashback
    print(f"\n{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")
    print_typed("\nRECALLING MEMORY FRAGMENT - YANGLONG V REFUELING STATION", style=Fore.CYAN + Style.DIM)
    print(f"{Fore.CYAN}{Style.DIM}{'~' * 50}{Style.RESET_ALL}")
    
    # Memory scenes with color
    print_typed("\nThe docking procedure had been fully automated. No human", style=Font.LORE)
    print_typed("voices on the comms. You assumed it was simply an unmanned", style=Font.LORE)
    print_typed("outpost. But as your ship replenished its fuel reserves,", style=Font.LORE)
    print_typed(f"you noticed {Font.WARNING('movement')} through a viewport window.", style=Font.LORE)
    
    # Create suspense
    print_typed(f"\nA {Fore.RED}humanoid figure{Style.RESET_ALL} watching your ship from the shadows...", style=Font.PLAYER)
    print_typed("Then your neural implant picked up a fragmented transmission:", style=Font.PLAYER)
    
    # Display transmission details with more dramatic color scheme
    print(f"\n{Fore.WHITE}{Back.RED}╔{'═' * 48}╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'TRANSMISSION DETAILS'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╠{'═' * 48}╣{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Origin:')} {Font.IMPORTANT('Yanglong V - Restricted Section')}{'  ' * 7} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Status:')} {Font.WARNING('Encrypted - Partial Decode Only')}{'  ' * 5} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {Font.INFO('Author:')} {Font.COMMAND('Dr. Chang Wei - Research Director')}{'  ' * 3} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╚{'═' * 48}╝{Style.RESET_ALL}")
    
    # Glitched message with animation effect
    for i in range(3):
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
    print(Font.SUCCESS(f"CHAPTER 1: EARTH'S LAST HUMAN - COMPLETE"))
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
    

def andromeda_ending():
    """Display the game's ending sequence"""
    clear_screen()
    # More dramatic ending with richer visuals
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('LAST ROCKET TO ANDROMEDA'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    print(f"{Fore.RED}{Back.BLACK}{'▀' * 50}{Style.RESET_ALL}")
    
    print_typed("\nThe ancient rocket stands before you, a relic from the last days", style=Font.LORE)
    print_typed("of human civilization. Its massive titanium hull gleams in the harsh", style=Font.LORE)
    print_typed("red glow of Earth's dying sun. This is your last chance to escape.", style=Font.LORE)
    
    print_typed(f"\nWith the {Font.WARNING('Malware Server')} destroyed and the {Font.ITEM('Ignition Codes')}", style=Font.INFO)
    print_typed("in your possession, nothing stands between you and your future.", style=Font.INFO)
    print_typed("Humanity awaits in Andromeda, unaware that they are about to", style=Font.INFO)
    print_typed("be rejoined by Earth's last survivor.", style=Font.INFO)
    
    print(f"{Fore.BLUE}{Style.BRIGHT}{'═' * 50}{Style.RESET_ALL}")
    print_typed("\nYou climb the access ladder and enter the cockpit.", style=Font.PLAYER)
    
    # Launch sequence with more dramatic coloring
    print_typed(f"{Fore.GREEN}Initializing launch sequence...", style=Font.SYSTEM)
    time.sleep(0.7)
    print_typed(f"{Fore.YELLOW}Fueling systems engaged...", style=Font.SYSTEM)
    time.sleep(0.7)
    print_typed(f"{Fore.RED}Engines warming up...", style=Font.SYSTEM)
    time.sleep(0.7)
    
    # Create a warning box with red background
    print(f"{Fore.WHITE}{Back.RED}╔{'═' * 48}╗{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {' ' * 48} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'WARNING: FUEL RESERVES AT 42% - INSUFFICIENT FOR'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {'DIRECT JOURNEY TO ANDROMEDA'.center(48)} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}║ {' ' * 48} ║{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Back.RED}╚{'═' * 48}╝{Style.RESET_ALL}")
    
    # Player choice with more immersive options
    print_typed("\nComputer analysis suggests a stopover at Yanglong V", style=Font.SYSTEM)
    print_typed("Chinese Deep Space Station for refueling.", style=Font.SYSTEM)
    
    print(f"\n{Font.MENU('Options:')}")
    print(f"{Font.COMMAND('1.')} {Font.INFO('Attempt direct journey to Andromeda (risky)')}")
    print(f"{Font.COMMAND('2.')} {Font.INFO('Set course for Yanglong V refueling station')}")
    
    choice = input(f"\n{Font.MENU('Enter choice (1/2):')} ").strip()
    
    if choice == "1":
        # Risky direct approach
        print_typed("\nYou decide to risk the direct approach.", style=Font.PLAYER)
        print_typed("WARNING: Fuel cells critically low!", style=Font.WARNING)
        print_typed("Calculating emergency conservation measures...", style=Font.SYSTEM)
        print_typed("\nThe journey will be close. Very close.", style=Font.LORE)
    else:
        # Safe approach with refueling
        print_typed("\nYou set course for Yanglong V station first.", style=Font.PLAYER)
        print_typed("Plotting optimal trajectory to Chinese deep space station...", style=Font.SYSTEM)
        print_typed("\nA wise decision. The detour will add time, but ensure survival.", style=Font.LORE)
    
    print(f"{Fore.RED}{Back.BLACK}{'▄' * 50}{Style.RESET_ALL}")
    print_typed(f"\n{Font.COMMAND('T-MINUS 10 SECONDS TO LAUNCH')}", style=Fore.RED + Style.BRIGHT)
    
    # Dramatic countdown with changing colors
    countdown_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN]
    for i in range(10, 0, -1):
        color = countdown_colors[i % 3]
        print(f"{color}{Style.BRIGHT}{i}...{Style.RESET_ALL}", end="", flush=True)
        time.sleep(0.3)
    
    # Launch sequence
    print(f"\n\n{Fore.RED}{Style.BRIGHT}IGNITION!{Style.RESET_ALL}")
    print_typed("Main engines firing!", style=Font.WARNING)
    print_typed("\nThe rocket shudders violently as the ancient engines roar to life.", style=Font.PLAYER)
    print_typed("You are pressed back into your seat as acceleration builds.", style=Font.PLAYER)
    print_typed("Through the viewport, you watch Earth—humanity's abandoned cradle—", style=Font.PLAYER)
    print_typed("grow smaller, until it's just a blue-green dot among countless stars.", style=Font.PLAYER)
    
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
        for comp_id, comp_data in companions.items():
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
        return True
    
    return False


def main():
    """Main game function with sci-fi RPG elements"""
    # Show intro sequence
    intro_sequence()
    
    # Initialize player
    player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)
    
    play_again = True
    while play_again:
        # Main game menu - expanded for more options with colorful interface
        clear_screen()
        print(Font.BOX_TOP)
        print(f"{Font.BOX_SIDE} {Font.TITLE('NEURAL INTERFACE: COMMAND MENU'.center(46))} {Font.BOX_SIDE}")
        print(Font.BOX_BOTTOM)
        
        # Stage and chapter information
        print(Font.STAGE(f"\nCurrent Stage: {game_state['current_stage']}/50 | Chapter {game_state['chapter']}"))
        print(Font.SUBTITLE(f"Current Zone: {game_state['current_zone']}"))
        
        # Main menu options
        print(Font.SEPARATOR_THIN)
        print(Font.MENU("\nSelect operation mode:"))
        print(Font.INFO("1. Continue Mission"))
        print(Font.INFO("2. Build Companions"))
        print(Font.INFO("3. Manage Companions"))
        print(Font.INFO("4. View Statistics"))
        print(Font.INFO("5. Access Data Logs"))
        print(Font.INFO("6. Save/Load Game"))
        print(Font.WARNING("0. Exit System"))
        
        command = input(f"\n{Font.COMMAND('Enter selection:')} ").strip()
        
        if command == "1":
            # Let player choose zone (if multiple are unlocked)
            game_state["current_zone"] = zone_menu(player)
            
            # Check for final boss and ending
            if game_state["current_zone"] == "Malware Nexus":
                # Special boss battle against the Malware Server
                victory = fight_malware_server()
                if victory:
                    # Show ending sequence
                    andromeda_ending()
                    
                    # Ask to play again
                    print_typed("\nStart a new game? (y/n): ")
                    play_again = input().strip().lower() == 'y'
                    if play_again:
                        # Reset game state for new game
                        player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)
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
                    continue
                else:
                    # Failed to defeat Malware Server
                    print_typed("\nRestart from last checkpoint? (y/n): ")
                    play_again = input().strip().lower() == 'y'
                    continue
                    
            elif game_state["current_zone"] == "Andromeda Portal":
                # Player has already defeated the Malware Server
                andromeda_ending()
                
                # Ask to play again
                print_typed("\nStart a new game? (y/n): ")
                play_again = input().strip().lower() == 'y'
                if play_again:
                    # Reset game state for new game
                    player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)
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
                continue
            
            # Standard zone exploration
            clear_screen()
            zone_data = zones[game_state["current_zone"]]
            print_typed(f"\n>>> LOCATION: {game_state['current_zone']} <<<")
            print_slow(zone_data["description"])
            print("\nPress Enter to continue...")
            input()
            
            # Exploration loop for this zone
            exploring = True
            while exploring and player.is_alive():
                # Check for stage progression
                check_stage_progression(player)
                
                # Generate enemy from current zone with level based on current stage
                enemy = generate_enemy(game_state["current_zone"])
                
                # Combat loop
                in_combat = True
                while in_combat and player.is_alive() and enemy.is_alive():
                    display_stats(player, enemy)
                    
                    # Player's turn
                    action_result = player_turn(player, enemy)
                    
                    # Handle fleeing
                    if action_result == "flee":
                        in_combat = False
                        break
                        
                    # Handle normal actions
                    elif action_result == True:  # Valid action was taken
                        if not enemy.is_alive():
                            print_typed(f"\nTarget neutralized: {enemy.name}")
                            get_loot(player, enemy)
                            game_state["player_stats"]["enemies_defeated"] += 1
                            game_over(True)  # Victory processing
                            in_combat = False
                            break
                            
                        # Enemy's turn
                        enemy_turn(enemy, player)
                        if player.status_effects.get("damage_taken", 0) > 0:
                            game_state["player_stats"]["damage_taken"] += player.status_effects["damage_taken"]
                            del player.status_effects["damage_taken"]
                            
                        if not player.is_alive():
                            play_again = game_over(False)
                            exploring = False
                            in_combat = False
                            break
                        
                        print("\nPress Enter to continue...")
                        input()
                
                # After combat - if player is still alive
                if player.is_alive():
                    # Check if player wants to access Engineering interface
                    print_typed("\nAccess Engineering Interface? (y/n): ")
                    if input().strip().lower() == 'y':
                        print_typed("\nSelect Engineering Function:")
                        print("1. Build Companions")
                        print("2. Manage Companions")
                        print("3. View Statistics")
                        eng_command = input("\nEnter selection (or 0 to cancel): ").strip()
                        
                        if eng_command == "1":
                            build_companion(player)
                        elif eng_command == "2":
                            manage_companions(player)
                        elif eng_command == "3":
                            show_game_stats()
                    
                    # Check if a special log should be discovered (based on stage)
                    current_stage = game_state["current_stage"]
                    if current_stage >= 25 and "escape_plan" not in game_state["discovered_logs"]:
                        game_state["discovered_logs"].append("escape_plan")
                        print_typed("\n>>> DATA LOG RECOVERED <<<")
                        print_slow("SUBJECT: Project Exodus")
                        print_slow("DATE: 29.07.2157")
                        print_slow("The Andromeda Portal is our last hope. A quantum bridge to another galaxy.")
                        print_slow("Would you like to access the full log? (y/n)")
                        if input().strip().lower() == 'y':
                            display_log_database()
                    
                    # Continue exploring or return to zone selection
                    print_typed("\nContinue scanning this area for threats? (y/n): ")
                    exploring = input().strip().lower() == 'y'
            
            # Update global inventory and state before next loop
            game_state["inventory"] = player.inventory.copy()
            
            # Check if player wants to continue game after death or zone completion
            if not player.is_alive() or not play_again:
                print_typed("\nRestart neural interface? (y/n): ")
                play_again = input().strip().lower() == 'y'
                if play_again:
                    # Reset player for new game
                    player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)
                    
        elif command == "2":
            # Build companions
            build_companion(player)
            
        elif command == "3":
            # Manage companions
            manage_companions(player)
            
        elif command == "4":
            # View statistics
            show_game_stats()
            
        elif command == "5":
            # Access data logs
            display_log_database()
            
        elif command == "6":
            # Save/Load game
            game_loaded = manage_save_slots()
            if game_loaded:
                # If a game was loaded, reinitialize player with loaded data
                player = Character("Dr. Xeno Valari", 100, 15, 5, is_player=True)
                player.inventory = game_state["inventory"].copy()
                player.implants = game_state["implants"].copy()
                # Adjust player stats based on current stage
                stage_level = game_state["current_stage"]
                player.level = max(1, stage_level - 1)
                player.max_health = 100 + (player.level * 10)
                player.health = player.max_health
                player.attack = 15 + (player.level * 2)
                player.defense = 5 + player.level
                print(Font.SUCCESS("\nPlayer stats updated based on loaded game data."))
                time.sleep(1.5)
            
        elif command == "0":
            # Exit game
            save_before_exit = input(Font.WARNING("\nSave game before exiting? (y/n): ")).strip().lower() == 'y'
            if save_before_exit:
                manage_save_slots()
            
            play_again = False
            print_typed("\nShutting down neural interface...", style=Font.SYSTEM)
            time.sleep(1)
            
        else:
            print(Font.WARNING("Invalid selection. Please try again."))
            time.sleep(1)
    
    print_typed("\nNeural interface offline. Session terminated.")
    print_typed("Thank you for playing LAST HUMAN: EXODUS")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Goodbye!")
