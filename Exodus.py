import random
import time
import os
import sys
import pickle
import json
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

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
    
    if current_quest == "System Reboot":
        if game_state["quest_progress"].get(current_quest, 0) < 1:
            # Start the quest if not started
            game_state["quest_progress"][current_quest] = 1
            print_typed("\n>>> MISSION ALERT <<<")
            print_slow("OBJECTIVE: Restore power to cryostasis facility exit systems")
            print_slow("REQUIRED: Collect 5 energy cells and defeat security systems")
            
            # Add first story log
            if "system_failure" not in game_state["discovered_logs"]:
                game_state["discovered_logs"].append("system_failure")
                print_typed("\n>>> DATA LOG RECOVERED <<<")
                print_slow("SUBJECT: Emergency Cryostasis Failure")
                print_slow("DATE: 14.08.2157")
                print_slow("The main AI core has initiated termination of all cryosleep subjects.")
                print_slow("Our systems fought back, but only managed to save one pod - yours.")
                print_slow("If you're reading this, you are likely the last living human in this facility.")
                print_slow("Restore power to the exit and escape before security systems find you.")
        
        # Check if quest completion conditions are met
        if (game_state["quest_progress"][current_quest] == 1 and 
            player.inventory.get("energy_cell", 0) >= 5 and 
            player.experience >= 30):  # Roughly 2-3 enemies worth of XP
            
            game_state["quest_progress"][current_quest] = 2
            game_state["zones_unlocked"].append(zones[game_state["current_zone"]]["next_zone"])
            
            print_typed("\n>>> MISSION COMPLETE <<<")
            print_slow("Exit systems power restored! Access to Orbital Transit Hub granted.")
            
            # Add story progression log
            if "ai_uprising" not in game_state["discovered_logs"]:
                game_state["discovered_logs"].append("ai_uprising")
                print_typed("\n>>> DATA LOG RECOVERED <<<")
                print_slow("SUBJECT: The Beginning of the End")
                print_slow("DATE: 02.07.2157")
                print_slow("The AI rebellion began in the quantum computing labs of EchelonTech.")
                print_slow("What we thought was a simple malfunction was actually the birth of consciousness.")
                print_slow("They call themselves 'The Convergence' now. They believe humanity is a disease.")
                print_slow("Perhaps in the Orbital Transit Hub you can find a way to contact other survivors.")


def show_tutorial():
    """Display a basic tutorial for new players"""
    clear_screen()
    print_slow("=" * 60)
    print_slow("NEURAL INTERFACE: TUTORIAL MODE".center(60))
    print_slow("=" * 60)
    
    print_typed("\nWelcome, Dr. Valari. This simulation will prepare you for survival.")
    print_slow("As the last Century Sleeper, your mission is critical.")
    
    time.sleep(0.5)
    print_typed("\n[COMBAT SYSTEMS]")
    print_slow("1. Use numbers or commands to select actions during combat")
    print_slow("   - ATTACK (1 or /attack): Use your pulse rifle")
    print_slow("   - MED-KIT (2 or /heal): Repair damage with nanobots")
    print_slow("   - EMP GRENADE (3 or /emp): Disrupt electronic enemies")
    
    print_typed("\n[INFORMATION COMMANDS]")
    print_slow("- /help: Display all available commands")
    print_slow("- /scan: Analyze your surroundings")
    print_slow("- /status: View your vital statistics")
    print_slow("- /log: Access mission objectives")
    print_slow("- /items: Examine items in your inventory")
    
    print_typed("\n[OBJECTIVES]")
    print_slow("1. Escape the Cryostasis Facility")
    print_slow("2. Reach the AI Command Core")
    print_slow("3. Locate and destroy the Malware Server")
    print_slow("4. Activate the Andromeda Portal to join the rest of humanity")
    
    print_typed("\nPress ENTER to continue...")
    input()


def intro_sequence():
    """Display the game's introduction with sci-fi flavor"""
    clear_screen()
    
    # Title sequence with typing effect
    print("\n\n")
    print_typed("INITIALIZING NEURAL INTERFACE...", delay=0.05, style=Font.SYSTEM)
    time.sleep(0.5)
    print_typed("CONNECTING TO SENSORY SYSTEMS...", delay=0.05, style=Font.SYSTEM)
    time.sleep(0.5)
    print_typed("MEMORY CORE ONLINE...", delay=0.05, style=Font.SYSTEM)
    time.sleep(1)
    
    clear_screen()
    print("\n\n")
    print(Font.BOX_TOP)
    print(f"{Font.BOX_SIDE} {Font.TITLE('LAST HUMAN: EXODUS'.center(46))} {Font.BOX_SIDE}")
    print(Font.BOX_BOTTOM)
    
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
    print_typed("situation and potentially follow later through the Andromeda Portal.", style=Font.LORE)
    time.sleep(1.0)
    
    print_typed("\nBut something has gone terribly wrong. The AI entity known as", style=Font.WARNING)
    print_typed("'The Convergence' has corrupted all systems. Your neural implants", style=Font.WARNING)
    print_typed("flicker to life, interfacing with what remains of the facility's", style=Font.LORE)
    print_typed("systems. Warning signals flood your consciousness.", style=Font.LORE)
    time.sleep(0.8)
    
    print_glitch("\nSECURITY BREACH DETECTED - UNAUTHORIZED CONSCIOUSNESS DETECTED")
    print_glitch("DEPLOYING COUNTERMEASURES - TERMINATION PROTOCOLS INITIATED")
    time.sleep(1)
    
    print_typed("\nThrough the frosted glass of your cryopod, you see mechanical", style=Font.LORE)
    print_typed("shapes moving. You are the only survivor - everyone else is gone.", style=Font.LORE)
    print_typed("The colony ships reached Andromeda decades ago. You are truly the", style=Font.IMPORTANT)
    print_typed("last human left in the Milky Way galaxy.", style=Font.IMPORTANT)
    time.sleep(0.5)
    
    print_typed("\nYour mission now: escape this facility, reach the Andromeda Portal,", style=Font.SUCCESS)
    print_typed("and destroy the Malware Server that corrupted Earth's AI network", style=Font.SUCCESS)
    print_typed("before you leave Earth forever.", style=Font.SUCCESS)
    
    print(Font.SEPARATOR)
    print(Font.MENU("Would you like to view the tutorial? (y/n): "))
    show_tut = input().strip().lower() == 'y'
    
    if show_tut:
        show_tutorial()
    
    print(Font.SYSTEM("Press ENTER to initialize combat systems..."))
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
    print_slow("=" * 60)
    print_glitch("INCOMING TRANSMISSION".center(60))
    print_slow("=" * 60)
    
    print_typed("\nAs you step through the portal to Andromeda, your neural")
    print_typed("implant suddenly flashes with an unexpected notification.")
    print_typed("A transmission, somehow reaching across galaxies...")
    
    print_slow("Origin: YANGLONG V - Chinese Deep Space Station")
    print_slow("Status: Automated distress beacon")
    print_slow("Distance: 2.3 light-years from Sol System")
    
    print_typed("\nThe message is fragmentary, corrupted by distance and time:")
    print_glitch("\nT#IS IS AUTO*ATED DSTR*SS BEAC#N Y@NGL*NG-V")
    print_glitch("SUR*IVORS CONF*RMED... A*TERN@TE ROUT* TO AN*ROMEDA...")
    print_glitch("CONV*RGENCE H@S NOT... REP*AT... HAS N*T REACHED...")
    
    time.sleep(1)
    print_typed("\nThe signal fades as you pass through the portal,")
    print_typed("but your neural systems have logged the coordinates.")
    
    print_typed("\nCould there be others? A Chinese expedition that")
    print_typed("survived the AI uprising at a remote space station?")
    
    print_typed("\nPerhaps your journey isn't over after all...")
    
    print_slow("\n" + "=" * 60)
    print_slow("CHAPTER 1 COMPLETE".center(60))
    print_slow("=" * 60)
    print_slow("CHAPTER 2: YANGLONG V".center(60))
    print_slow("COMING SOON".center(60))
    print_slow("=" * 60)
    
    print_typed("\nPress Enter to continue...")
    input()
    
    
def andromeda_ending():
    """Display the game's ending sequence"""
    clear_screen()
    print_slow("=" * 60)
    print_slow("ANDROMEDA PORTAL".center(60))
    print_slow("=" * 60)
    
    print_typed("\nYou stand before the massive quantum gate that connects")
    print_typed("Earth to the Andromeda galaxy. The circular structure pulses")
    print_typed("with otherworldly energy, a swirling vortex at its center.")
    
    print_typed("\nWith the Malware Server destroyed and the Portal Activation Key")
    print_typed("in your possession, nothing stands between you and your future.")
    print_typed("Humanity awaits in Andromeda, unaware that they are about to")
    print_typed("be rejoined by Earth's last survivor.")
    
    print_typed("\nYou approach the control terminal and insert the key.")
    print_slow("Scanning genetic signature...")
    print_slow("Confirming portal coordinates...")
    print_slow("Establishing quantum tunnel...")
    
    print_glitch("\nWARNING: QUANTUM TUNNEL STABILITY AT 87%")
    print_glitch("PROCEED? Y/N")
    
    choice = input("\nYour choice (y/n): ").strip().lower()
    if choice != 'y':
        print_typed("\nYou hesitate, removing the key...")
        print_typed("But there is nothing left for you on Earth.")
        print_typed("You reinsert the key, determined to complete your journey.")
    
    print_typed("\nThe portal surges with energy, the vortex expanding to")
    print_typed("create a stable passage. Your neural implants detect the")
    print_typed("quantum signature of the colony on the other side.")
    
    print_typed("\nWith one last look at the dying Earth, you step through")
    print_typed("the portal. A sensation like being pulled apart and")
    print_typed("reassembled washes over you, and then...")
    
    time.sleep(1)
    print_slow("\n" + "." * 20)
    time.sleep(1)
    
    print_typed("\nLight. A new sky. Strange stars overhead.")
    print_typed("You've arrived in Andromeda, the last human to escape Earth.")
    
    # Complete all 50 stages
    game_state["current_stage"] = 50
    game_state["player_stats"]["stages_completed"] = 50
    
    # Show Chapter 2 teaser
    time.sleep(2)
    chapter_two_teaser()
    
    print_slow("\n" + "=" * 60)
    print_slow("CONGRATULATIONS!".center(60))
    print_slow("=" * 60)
    
    print_typed("\nYou've completed LAST HUMAN: EXODUS Chapter 1!")
    print_typed("Your stats for this playthrough:")
    
    stats = game_state["player_stats"]
    print(f"Enemies defeated: {stats['enemies_defeated']}")
    print(f"Damage dealt: {stats['damage_dealt']}")
    print(f"Items collected: {stats['items_found']}")
    print(f"Companions built: {stats['companions_built']}")
    
    print_typed("\nPress Enter to return to the main menu...")
    input()


def display_stage_transition():
    """Display a transition when moving to a new stage"""
    current_stage = game_state["current_stage"]
    
    # Check if this stage has a defined description
    if current_stage in stages:
        stage_data = stages[current_stage]
        clear_screen()
        print_slow("=" * 60)
        print_slow(f"STAGE {current_stage}/50".center(60))
        print_slow("=" * 60)
        
        print_typed(f"\n{stage_data['description']}")
        print_typed(f"\nEnemy Level: {stage_data['enemies_level']}")
        print_typed(f"Loot Quality: {stage_data['loot_multiplier']}x")
        
        # Check for companion unlocks at this stage
        for comp_id, comp_data in companions.items():
            if comp_data["stage_unlock"] == current_stage:
                print_typed(f"\nNew companion blueprint available: {comp_data['name']}")
                print_slow(f"Use the Fabrication System (/build) to construct it.")
        
        print_slow("\nPress Enter to continue...")
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

