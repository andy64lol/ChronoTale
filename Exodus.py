import random
import time
import os
import sys
import pickle
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
            except pickle.UnpicklingError:
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
        print_typed("Neural pathways optimized. Combat effectiveness increased.")
        print_slow(f"{self.name} is now level {self.level}!")
        print_slow(f"Health: {self.max_health} | Attack: {self.attack} | Defense: {self.defense}")

        # Unlock new ability at certain levels
        if self.level == 3:
            self.abilities.append("Hack")
            print_slow("New ability unlocked: Hack - Attempt to disable electronic enemies")


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
    
    Args:
        game_state: The current game state
        puzzle_type: The type of musical puzzle to solve
    
    Returns:
        bool: True if puzzle solved, False otherwise
    """
    clear_screen()
    print_typed(f"\n{Font.HEADER('DIMENSIONAL INTERFACE DETECTED')}")
    print_typed(f"{Font.SUBTITLE('Musical Interface Calibration Required')}\n")
    
    if puzzle_type == "keypad":
        print_typed("Before you stands a strange keypad with musical symbols instead of numbers.")
        print_typed("Each key produces a distinct tone when pressed. A holographic display")
        print_typed("shows a sequence of notes that must be replicated.")
        print_slow("\nThe system appears to accept input...", delay=0.05)
        
        # Generate a random sequence
        sequence_length = random.randint(4, 8)
        notes = ["C", "D", "E", "F", "G", "A", "B"]
        correct_sequence = [random.choice(notes) for _ in range(sequence_length)]
        
        print_typed(f"\n{Font.INFO('The sequence appears to be:')}")
        print_typed(f"{Font.IMPORTANT(' '.join(correct_sequence))}")
        print_typed("\nEnter the sequence (notes separated by spaces, e.g., 'C E G B'):")
        
        try:
            player_input = input().strip().upper().split()
            if player_input == correct_sequence:
                print_typed(f"\n{Font.SUCCESS('Sequence accepted! The keypad glows with ethereal light.')}")
                return True
            else:
                print_typed(f"\n{Font.WARNING('Incorrect sequence. The keypad resets itself.')}")
                return False
        except ValueError:
            print_typed(f"\n{Font.WARNING('Invalid input. The keypad resets itself.')}")
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
    
    Args:
        game_state: The current game state
        difficulty: The difficulty level that was overcome (1-3)
    """
    clear_screen()
    print_typed(f"\n{Font.SUCCESS('DIMENSIONAL CHEST OPENED')}")
    
    # Scale rewards with difficulty
    num_items = random.randint(difficulty, difficulty + 2)
    
    # Common items (difficulty 1)
    common_items = {
        "reality_fragment": "A small crystallized piece of alternate reality",
        "quantum_shard": "A fragment containing quantum information from multiple timelines",
        "dimensional_battery": "A power source that draws energy from dimensional boundaries",
        "echo_circuit": "A technological component that retains echoes of its alternate versions",
        "temporal_regulator": "A device that stabilizes the user's position in the time stream"
    }
    
    # Uncommon items (difficulty 2)
    uncommon_items = {
        "paradox_crystal": "A crystal formed at the intersection of contradictory timelines",
        "reality_core": "A dense sphere of crystallized reality with unusual properties",
        "timeline_splinter": "A fragment showing events from an alternate history",
        "phase_stabilizer": "A device that prevents uncontrolled phase-shifting between dimensions",
        "gravity_modulator": "A tool that can locally alter gravitational constants"
    }
    
    # Rare items (difficulty 3)
    rare_items = {
        "white_hole_shard": "A fragment of the white hole's core, pulsing with energy",
        "reality_stabilizer": "A powerful device capable of anchoring unstable reality pockets",
        "multiverse_key": "A unique key that can unlock pathways between parallel universes",
        "dimensional_anchor": "A technology that can fix a specific reality state, preventing shifts",
        "chronometric_particle": "A particle existing across multiple time states simultaneously"
    }
    
    # Select appropriate loot pool based on difficulty
    if difficulty == 1:
        loot_pool = common_items
    elif difficulty == 2:
        loot_pool = {**common_items, **uncommon_items}  # Combine dictionaries
    else:  # difficulty 3
        loot_pool = {**common_items, **uncommon_items, **rare_items}
    
    # Always include a chance for quantum crystals (gacha currency)
    quantum_crystals = random.randint(difficulty * 10, difficulty * 25)
    
    # Select random items
    selected_items = random.sample(list(loot_pool.items()), min(num_items, len(loot_pool)))
    
    # Display loot
    print_typed(f"\n{Font.ITEM('The chest contains:')}")
    
    for item_name, item_desc in selected_items:
        # Add item to inventory
        game_state["inventory"][item_name] = game_state["inventory"].get(item_name, 0) + 1
        print_typed(f"\n• {Font.ITEM(item_name.replace('_', ' ').title())}: {item_desc}")
    
    # Add quantum crystals if any
    if quantum_crystals > 0:
        game_state["quantum_crystals"] = game_state.get("quantum_crystals", 0) + quantum_crystals
        print_typed(f"\n• {Font.ITEM(f'{quantum_crystals} Quantum Crystals')}: Currency for the Quantum Chronosphere")
    
    print_typed(f"\n{Font.SUCCESS('Items added to your inventory.')}")
    input("\nPress Enter to continue...")


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
    # Defense bonus is already shown in the UI display below, no need for separate variable
    
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
        
        # Calculate damage
        base_damage = random.randint(effective_attack - 3, effective_attack + 3)
        damage = int(base_damage * damage_mod)
        
        # Check for critical hit
        is_critical = random.random() < (player.crit_chance + crit_chance_bonus)
        if is_critical:
            damage = int(damage * player.crit_damage)
            print_slow(f"{Font.SUCCESS('CRITICAL HIT!')} Your {weapon_name} finds a weakness!", delay=0.03)
        
        # Different attack messages based on weapon type
        attack_messages = {
            "energy": [
                "Targeting systems locked... Firing {weapon_name}...",
                "Energy capacitors charged... Discharging {weapon_name}...",
                "Photon matrix aligned... Releasing energy burst..."
            ],
            "physical": [
                "Kinetic accelerators online... Firing {weapon_name}...",
                "Impact calculators engaged... Launching projectiles...",
                "Recoil compensators active... Unleashing kinetic rounds..."
            ],
            "emp": [
                "EM disruptors charged... Deploying electromagnetic pulse...",
                "Circuit overloaders ready... Triggering EMP burst...",
                "System scramblers online... Firing electromagnetic wave..."
            ],
            "thermal": [
                "Thermal capacitors charged... Igniting plasma stream...",
                "Heat sinks engaged... Releasing thermal energy...",
                "Fusion core active... Unleashing controlled plasma burst..."
            ],
            "quantum": [
                "Reality distortion field active... Firing quantum particles...",
                "Dimensional anchor established... Releasing quantum wave...",
                "Probability matrix engaged... Unleashing quantum disruption..."
            ]
        }
        
        # Display attack message
        print_typed(random.choice(attack_messages.get(damage_type, attack_messages["energy"])))
        
        # Apply damage with specific damage type
        enemy.take_damage(damage, damage_type)
        
        # Special effects based on damage type
        if damage_type == "thermal" and random.random() < 0.25:  # 25% chance
            if "burning" not in enemy.status_effects:
                enemy.status_effects["burning"] = 2  # Lasts 2 turns
                burning_damage = max(3, int(effective_attack * 0.2))  # 20% of attack as burning damage
                print_typed(f"{Font.WARNING(f'{enemy.name} is now BURNING!')} Will take {burning_damage} damage per turn for 2 turns.")
        
        elif damage_type == "quantum" and random.random() < 0.20:  # 20% chance
            if "quantum_unstable" not in enemy.status_effects:
                enemy.status_effects["quantum_unstable"] = 2  # Lasts 2 turns
                print_typed(f"{Font.WARNING(f'{enemy.name} is now QUANTUM UNSTABLE!')} Defense reduced by 30% for 2 turns.")
                
        elif damage_type == "phase" and random.random() < 0.20:  # 20% chance
            if "temporal_distortion" not in enemy.status_effects:
                enemy.status_effects["temporal_distortion"] = 2  # Lasts 2 turns
                print_typed(f"{Font.WARNING(f'{enemy.name} is caught in TEMPORAL DISTORTION!')} 30% chance to skip turns for 2 rounds.")
                
        elif damage_type == "bio" and random.random() < 0.25:  # 25% chance
            if "bio_corruption" not in enemy.status_effects:
                enemy.status_effects["bio_corruption"] = 3  # Lasts 3 turns
                print_typed(f"{Font.WARNING(f'{enemy.name} is infected with BIO CORRUPTION!')} Will take damage and lose attack power for 3 turns.")

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

    else:
        print_typed("ERROR: Invalid command. Type '/help' for available commands.")
        return False  # Don't count invalid commands as a turn

    return True  # A valid action was taken


def enemy_turn(enemy, player):
    """Handle enemy's turn with advanced AI behaviors"""
    
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
    
    Args:
        player: The player character
        game_state: The current game state
    """
    clear_screen()
    print_slow("=" * 60)
    print_typed(Font.HEADER("ABANDONED RESEARCH FACILITY").center(60))
    print_slow("=" * 60)
    
    # Check if this is the first visit
    if not game_state.get("research_base_visited", False):
        # First visit narrative
        print_typed("\nYour submersible vehicle descends through the murky waters")
        print_typed("of Thalassia 1. Visibility is limited, with only the vehicle's")
        print_typed("lights penetrating the darkness. The water pressure outside")
        print_typed("is immense, and occasional flashes of bioluminescence reveal")
        print_typed("strange creatures darting away from your lights.")
        
        time.sleep(1)
        
        print_typed("\nAfter what seems like an eternity, a structure looms out of")
        print_typed("the darkness - the abandoned human research facility. Its")
        print_typed("exterior is encrusted with salt formations and strange organic")
        print_typed("growths. Some sections appear damaged, with evidence of both")
        print_typed("structural failure and something... forcing its way inside.")
        
        print_typed(f"\n{Font.SYSTEM('SCANNING FACILITY...')}")
        print_typed(f"{Font.INFO('Main power: OFFLINE')}")
        print_typed(f"{Font.INFO('Backup generators: MINIMAL FUNCTION (12% CAPACITY)')}")
        print_typed(f"{Font.INFO('Hull integrity: COMPROMISED - SECTIONS E, F, H FLOODED')}")
        print_typed(f"{Font.INFO('Life signs: MULTIPLE UNIDENTIFIED ORGANISMS DETECTED')}")
        
        time.sleep(1)
        
        print_typed("\nYou dock your submersible at a still-functioning airlock.")
        print_typed("The docking mechanism engages with a metallic thunk, and the")
        print_typed("airlock cycles, draining the water. As the inner door opens,")
        print_typed("your suit lights illuminate a once-sterile corridor, now")
        print_typed("covered in salt deposits and strange, organic growth.")
        
        # Mark as visited
        game_state["research_base_visited"] = True
    else:
        # Return visit narrative
        print_typed("\nYou return to the submerged research facility. The docking")
        print_typed("procedure is familiar now, and the airlock cycles to admit you.")
        print_typed("The eerie silence of the abandoned facility greets you once more.")
    
    # Base exploration loop
    exploring = True
    while exploring:
        print_typed(f"\n{Font.SUBTITLE('What would you like to investigate?')}")
        
        print_typed(f"1. {Font.COMMAND('Main Laboratory')}")
        print_typed(f"2. {Font.COMMAND('Crew Quarters')}")
        print_typed(f"3. {Font.COMMAND('Weapons Research Wing')}")
        print_typed(f"4. {Font.COMMAND('Communications Center')}")
        
        # Add option for the lower level once preconditions are met
        if (game_state.get("lab_cleared", False) and 
            game_state.get("weapons_wing_cleared", False) and
            game_state.get("found_sonic_module", False) and
            not game_state.get("neurovore_prime_defeated", False)):
            print_typed(f"5. {Font.COMMAND('Descend to Lower Level')} {Font.WARNING('(DANGER)')}")
            print_typed(f"6. {Font.COMMAND('Return to submersible')}")
        else:
            print_typed(f"5. {Font.COMMAND('Return to submersible')}")
        
        choice = input("\nEnter your choice: ").strip()
        
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
                print_typed("find a sealed specimen container. Inside are preserved samples")
                print_typed("of several Thalassian life forms, including what appears to")
                print_typed("be a juvenile version of the bivalve creatures infesting the facility.")
                
                print_typed(f"\n{Font.SUCCESS('You collect the specimen container for study.')}")
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
            
            # Sound weapon module discovery
            if not game_state.get("found_sonic_module", False):
                print_typed("\nIn a sealed weapons locker, you discover an intact prototype")
                print_typed("weapon module. The schematics indicate it's designed to emit")
                print_typed("focused sonic pulses that can disrupt neural networks and")
                print_typed("communication systems.")
                
                print_typed(f"\n{Font.WEAPON('SONIC DISRUPTOR MODULE')}")
                print_typed("Prototype weapon designed specifically to counter the Neurovore")
                print_typed("threat. Emits concentrated sound waves at frequencies that")
                print_typed("overwhelm the creatures' sensitive audio receptors while")
                print_typed("disrupting their neural control capabilities.")
                
                # Add to weapon modules
                weapon_modules = game_state.get("weapon_modules", {})
                weapon_modules["sonic_disruptor"] = {
                    "name": "Sonic Disruptor",
                    "description": "Emits concentrated sound waves that disrupt neural networks",
                    "damage": 30,
                    "damage_type": "sonic",
                    "equipped": False,
                    "special_effect": "Disrupts neural interfaces, 80% effective against Neurovores"
                }
                
                game_state["weapon_modules"] = weapon_modules
                game_state["found_sonic_module"] = True
                
                print_typed(f"\n{Font.SUCCESS('Sonic Disruptor Module added to your arsenal!')}")
                print_typed(f"{Font.INFO('Use Weapon Module Management to equip it.')}")
                
                # Mark area as cleared from initial encounter
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
            
            # Emergency beacon
            if "damaged_beacon" in player.inventory and not game_state.get("repaired_beacon", False):
                print_typed("\nYou remember the damaged emergency beacon you found earlier.")
                print_typed("Using the communications equipment here, you might be able")
                print_typed("to repair it.")
                
                print_typed("\nAttempt to repair the emergency beacon? (y/n)")
                repair_choice = input().strip().lower()
                
                if repair_choice == 'y' or repair_choice == 'yes':
                    print_typed("\nYou carefully disassemble the damaged beacon and integrate")
                    print_typed("components from the communication center's equipment.")
                    
                    # Skill check
                    success_chance = 0.7  # 70% base chance
                    if "energy_modulator" in player.inventory:
                        success_chance += 0.2  # +20% with energy modulator
                        print_typed("\nThe energy modulator you found proves invaluable for")
                        print_typed("calibrating the beacon's power systems.")
                    
                    if random.random() < success_chance:
                        print_typed(f"\n{Font.SUCCESS('Repair successful! The emergency beacon is now functional.')}")
                        player.inventory.pop("damaged_beacon", None)
                        player.inventory["emergency_beacon"] = player.inventory.get("emergency_beacon", 0) + 1
                        game_state["repaired_beacon"] = True
                        
                        # Add hint for escape plan
                        print_typed("\nWith this beacon, you could potentially signal any nearby")
                        print_typed("human vessels or installations. This might be your ticket")
                        print_typed("off Thalassia 1 if your ship proves unrepairable.")
                    else:
                        print_typed(f"\n{Font.WARNING('Repair attempt failed. The beacon is too damaged.')}")
                        print_typed("\nYou might need additional components or technical data.")
            
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
    """Conduct a battle between player and enemy with sci-fi flavor"""
    # Display initial stats
    display_stats(player, enemy)
    
    # Combat loop
    round_number = 1
    combat_state = {
        "round": 1,
        "player_buffs": {},
        "enemy_buffs": {},
        "available_abilities": True
    }
    
    while player.is_alive() and enemy.is_alive():
        print_typed(f"\n{Font.SEPARATOR}")
        print_typed(f"{Font.INFO('COMBAT ROUND ' + str(round_number))}")
        
        # Process any status effects at the start of player's turn
        status_info = player.process_status_effects()
        if status_info:
            print_typed(status_info)
        
        # Player's turn
        player_choice = player_turn(player, enemy)
        
        # Check if combat should end
        if player_choice == "flee" or not enemy.is_alive() or not player.is_alive():
            break
            
        # Enemy's turn (if still alive)
        if enemy.is_alive():
            # Process any status effects at the start of enemy's turn
            status_info = enemy.process_status_effects()
            if status_info:
                print_typed(status_info)
                
            enemy_turn(enemy, player)
            
        # Update round counter
        round_number += 1
        combat_state["round"] = round_number
    
    # Combat outcome
    if not enemy.is_alive():
        print_typed(f"\n{Font.SUCCESS('Enemy defeated!')}")
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


def main_menu():
    """Display the main menu with access to all game chapters"""
    clear_screen()
    print_slow("=" * 60)
    print_typed(Font.TITLE("LAST HUMAN: EXODUS").center(60))
    print_slow("=" * 60)
    print_typed(Font.SUBTITLE("A Sci-Fi Text RPG").center(60))
    print_slow("-" * 60)
    
    # Display chapter selection
    print_typed("\nSelect Your Chapter:")
    print_typed(f"1. {Font.COMMAND('Chapter 1: Earth Reclamation')}")
    print_typed("   The original story - escape Earth and defeat the Malware Server")
    
    print_typed(f"\n2. {Font.COMMAND('Chapter 2: White Hole')}")
    print_typed("   Navigate through a distorted reality with musical puzzles and dimensional chests")
    
    print_typed(f"\n3. {Font.COMMAND('Chapter 3: Thalassia 1')}")
    print_typed("   Explore a cold water planet with unique salt-based life and an underwater research base")
    
    print_typed(f"\n4. {Font.COMMAND('Load Game')}")
    print_typed(f"5. {Font.COMMAND('Credits')}")
    print_typed(f"0. {Font.COMMAND('Exit Game')}")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == "1":
        # Start Chapter 1
        intro_sequence()
        chapter_one()
        return main_menu()
    elif choice == "2":
        # Start Chapter 2
        clear_screen()
        print_typed(f"\n{Font.INFO('Starting Chapter 2: White Hole')}")
        print_typed("You'll enter an alternate reality where familiar locations")
        print_typed("are distorted and more dangerous. You must repair your ship")
        print_typed("and defeat the White Hole Guardian to escape.")
        input("\nPress Enter to begin...")
        
        # Initialize with White Hole chapter
        game_state["white_hole_chapter"] = True
        game_state["reality_stability"] = 30
        game_state["current_zone"] = "White Hole Transit"
        
        # Add white hole zones
        white_hole_zones = [
            "White Hole Transit", 
            "Distorted Cryostasis", 
            "Twisted Command Center",
            "Altered Engine Room"
        ]
        
        game_state["available_zones"] = white_hole_zones
        
        # Start with a new player but at higher level
        player = Character("Dr. Xeno Valari", 150, 25, 20, is_player=True)
        player.level = 10
        player.inventory = {
            "med_kit": 3,
            "energy_cell": 5,
            "repair_tool": 1
        }
        
        # Begin chapter
        zone_menu(player)
        return main_menu()
    elif choice == "3":
        # Start Chapter 3
        clear_screen()
        print_typed(f"\n{Font.INFO('Starting Chapter 3: Thalassia 1')}")
        print_typed("Your ship will crash on Thalassia 1, a cold water planet")
        print_typed("with unique salt-based life forms. You'll explore an abandoned")
        print_typed("underwater research facility and face the Neurovore Prime.")
        input("\nPress Enter to begin...")
        
        # Initialize with Thalassia chapter
        game_state["thalassia_chapter"] = True
        game_state["white_hole_chapter"] = False
        
        # Create new player
        player = Character("Dr. Xeno Valari", 180, 30, 25, is_player=True)
        player.level = 15
        player.inventory = {
            "med_kit": 5,
            "pressure_suit": 1,
            "advanced_scanner": 1
        }
        
        # Begin crash sequence
        thalassia_crash_sequence(game_state, player)
        
        # Add research base to available zones
        available_zones = game_state.get("available_zones", [])
        if "Underwater Research Base" not in available_zones:
            available_zones.append("Underwater Research Base")
            game_state["available_zones"] = available_zones
        
        # Start exploring
        game_state["current_zone"] = "Submerged Ship"
        zone_menu(player)
        return main_menu()
    elif choice == "4":
        # Load Game
        load_game()
        return main_menu()
    elif choice == "5":
        # Credits
        clear_screen()
        print_slow("=" * 60)
        print_typed(Font.TITLE("CREDITS").center(60))
        print_slow("=" * 60)
        
        print_typed("\nLAST HUMAN: EXODUS")
        print_typed("A Sci-Fi Text RPG with Multiple Chapters")
        
        print_typed("\nChapter 1: Earth Reclamation")
        print_typed("The original story of escaping Earth")
        
        print_typed("\nChapter 2: White Hole")
        print_typed("A reality-bending adventure with musical puzzles")
        
        print_typed("\nChapter 3: Thalassia 1")
        print_typed("Underwater exploration and the Neurovore threat")
        
        print_typed("\nThanks for playing!")
        
        input("\nPress Enter to return to the main menu...")
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


def chapter_one():
    """The original Earth Reclamation chapter"""
    # Initialize game state
    global game_state
    game_state = {
        "current_zone": "Cryostasis Bay",
        "available_zones": ["Cryostasis Bay"],
        "visited_zones": [],
        "active_quests": [],
        "completed_quests": [],
        "white_hole_chapter": False,
        "thalassia_chapter": False
    }
    
    # Create player character
    player = Character("Dr. Xeno Valari", 100, 20, 15, is_player=True)
    player.inventory = {
        "med_kit": 2,
        "energy_cell": 3
    }
    
    # Start the game
    zone_menu(player)


def main():
    """Main game function with sci-fi RPG elements"""
    # Initialize colorama
    init(autoreset=True)

    # Initialize global game state
    global game_state
    game_state = {}

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

    # Main game loop
    play_again = True
    while play_again:
        # Show the main menu
        clear_screen()
        print("Thanks for playing Last Human: Exodus!")
        print(Font.INFO("1. Continue Mission"))
        print(Font.INFO("2. Build Companions"))
        print(Font.INFO("3. Manage Companions"))
        print(Font.INFO("4. View Statistics"))
        print(Font.INFO("5. Access Data Logs"))
        print(Font.INFO("6. Save/Load Game"))
        print(Font.INFO("7. Gacha System"))
        print(Font.WARNING("0. Exit System"))

        command = input(f"\n{Font.COMMAND('Enter selection:')} ").strip()

        if command == "1":
            # Let player choose zone (if multiple are unlocked)
            game_state["current_zone"] = zone_menu(game_state["player"])

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

            # Check if Prime Simulacra boss fight has been triggered
            if "simulacra_boss_triggered" in game_state and game_state["simulacra_boss_triggered"] and game_state["current_zone"] == "Colony Central Hub":
                # Reset the flag to prevent retriggers
                game_state["simulacra_boss_triggered"] = False

                # Update player's inventory to ensure they have proper equipment for the boss fight
                if "med_kit" not in player.inventory or player.inventory["med_kit"] < 2:
                    player.inventory["med_kit"] = 2
                    print_typed(f"\n{Font.ITEM('Medical supplies found!')} You now have 2 med kits.")

                if "shield_matrix" not in player.inventory:
                    player.inventory["shield_matrix"] = 1
                    print_typed(f"\n{Font.ITEM('Shield Matrix discovered!')} This will help protect you.")

                # Start the boss fight
                print_typed("\nPreparing Prime Simulacra boss fight...")
                boss_result = fight_prime_simulacra(player)

                if not boss_result:
                    # Player was defeated
                    continue

                # Player defeated the Prime Simulacra - give additional rewards
                print_typed("\nThe defeat of the Prime Simulacra has earned you valuable combat experience.")
                player.gain_experience(50)
                print_typed(f"\n{Font.SUCCESS('+ 50 XP')}")

            # Check if this is a Cicrais IV zone with wave-based combat
            elif "Cicrais" in game_state["current_zone"] and "wave_count" in zone_data:
                # Handle wave-based combat
                combat_result = handle_wave_combat(player, game_state["current_zone"])
                if not combat_result:
                    # Player was defeated
                    continue

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
                    elif action_result:  # Valid action was taken
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

        elif command == "7":
            # Access Gacha System
            gacha_system()

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
        # Then check if launched through launcher
        if os.environ.get("LAUNCHED_FROM_LAUNCHER") != "1":
            print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
            print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
            input("Press Enter to exit...")
            sys.exit(0)
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Goodbye!")
