import random
import time
import os
import pickle
import json
import sys
from typing import List, Dict, Optional, Tuple
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add GOLD color for trophy/medal display
if not hasattr(Fore, 'GOLD'):
    setattr(Fore, 'GOLD', Fore.YELLOW)

def safe_input(prompt: str = "") -> str:
    """Safe input function that handles EOF and keyboard interrupts"""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return ""

# Clear screen function that works across different platforms
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# File-based save system
SAVE_DIR = "wom_saves"
CHAMPIONS_FILE = os.path.join(SAVE_DIR, "champions.pickle")

# Initialize save directory
def init_database():
    """Initialize the save directory and files"""
    try:
        # Create save directory if it doesn't exist
        os.makedirs(SAVE_DIR, exist_ok=True)

        # Create empty champions file if it doesn't exist
        if not os.path.exists(CHAMPIONS_FILE):
            with open(CHAMPIONS_FILE, 'wb') as f:
                pickle.dump([], f)

        return True
    except Exception as e:
        print(f"{Fore.RED}Error initializing save system: {e}{Style.RESET_ALL}")
        return False

# Get save file path for a player
def get_save_path(player_name, save_name):
    """Get the file path for a save file"""
    return os.path.join(SAVE_DIR, f"{save_name}.wom")

# Game constants
MAX_MONSTER_LEVEL = 50
MAX_INVENTORY_SIZE = 20
CATCH_BASE_RATE = 0.4
WILD_ENCOUNTER_RATE = 0.3
FUSION_LEVEL_REQUIREMENT = 25

# Move class for attacks
class Move:
    def __init__(self, name: str, type_: str, power: int, accuracy: float, description: str):
        self.name = name
        self.type = type_
        self.power = power
        self.accuracy = accuracy
        self.description = description

    def __str__(self) -> str:
        return f"{self.name} ({self.type}) - Power: {self.power}, Accuracy: {int(self.accuracy*100)}%"


# Item class for inventory items
class Item:
    def __init__(self, name: str, description: str, effect: str, value: int):
        self.name = name
        self.description = description
        self.effect = effect
        self.value = value

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"


# Monster class
class Monster:
    def __init__(self, name: str, type_: str, base_hp: int, base_attack: int, 
                 base_defense: int, base_speed: int, moves: List[Move], 
                 description: str, level: int = 5, is_fusion: bool = False, 
                 fusion_components: Optional[List[str]] = None, variant: Optional[str] = None,
                 rarity: Optional[str] = None):
        self.name = name
        self.type = type_
        self.base_hp = base_hp
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.base_speed = base_speed
        self.moves = moves
        self.description = description
        self.level = level
        self.exp = 0
        self.exp_to_level = level * 20
        self.is_fusion = is_fusion
        self.fusion_components = fusion_components or []

        # Variant attributes (Omega, Alpha, Corrupted, Crystal, Dominant)
        self.variant = variant
        self.can_evolve = variant is None  # Variants cannot evolve

        # Rarity system - assign rarity based on monster name if not provided
        self.rarity = rarity or self._determine_rarity()

        # Shiny attribute for special variants
        self.is_shiny = variant and 'shiny' in variant.lower() if variant else False

        # Apply variant stat adjustments if needed
        if variant:
            self.apply_variant_bonuses()

        # Calculated stats
        self.calculate_stats()
        self.current_hp = self.max_hp

    def _determine_rarity(self) -> str:
        """Determine monster rarity based on its name"""
        # Define rarity categories based on monster names
        legendary_names = ["Chronodrake", "Celestius", "Pyrovern", "Gemdrill", "Shadowclaw", "Tempestus", 
                          "Terraquake", "Luminary", "Chronos", "Spatium", "Cosmix", "Shadowlord", "Vitalia", 
                          "Phantomos", "Moltenking", "Prismatic", "Ancientone", "Deathwarden", "Oceanmaster", 
                          "Stormruler", "Sandstorm", "Frostlord", "Mechagon", "Worldtree", "Voidking", "Nebula",
                          "Doomreaper"]

        rare_names = ["Rockbehemoth", "Psyowl", "Drakeling", "Tornadash", "Volcanix", "Abyssal", "Spectralord",
                     "Pyrothane", "Crystalking", "Templeguard", "Banshee", "Leviathor", "Skydragon", "Mirageous", 
                     "Glacialtitan", "Cybernetic", "Naturelord", "Starhawk", "Infernus", "Terravore", 
                     "Dreadspirit", "Aquabyss", "Stormrage", "Netherbeast", "Crystallord", "Technocore", 
                     "Forestguard", "Voidreaper"]

        uncommon_names = ["Floracat", "Emberbear", "Coralfish", "Boltfox", "Frostbite", "Shadowpaw", "Fairybell", 
                         "Brawlcub", "Blazehound", "Groundmole", "Thunderwing", "Psyowl", 
                         "Glacierclaw", "Metalbeak", "Lavahound", "Gemguard", "Mysticfox", "Ghosthowl", "Tidalwave", 
                         "Stormbird", "Dunestrider", "Blizzardclaw", "Technowolf", "Dreamcatcher", "Voidwalker", 
                         "Cosmicowl"]

        if self.name in legendary_names:
            return "legendary"
        elif self.name in rare_names:
            return "rare"
        elif self.name in uncommon_names:
            return "uncommon"
        else:
            return "common"

    def apply_variant_bonuses(self):
        """Apply stat bonuses based on monster variant"""
        variant_name = self.variant
        original_name = self.name

        if variant_name == "Omega":
            # Omega variants have better overall stats
            self.base_hp = int(self.base_hp * 1.3)
            self.base_attack = int(self.base_attack * 1.3)
            self.base_defense = int(self.base_defense * 1.3)
            self.base_speed = int(self.base_speed * 1.3)
            self.name = f"Omega {original_name}"
            self.description = f"An Omega variant of {original_name}. It has superior stats in all categories."

        elif variant_name == "Alpha":
            # Alpha variants are leaders with balanced but higher stats
            self.base_hp = int(self.base_hp * 1.2)
            self.base_attack = int(self.base_attack * 1.2)
            self.base_defense = int(self.base_defense * 1.2)
            self.base_speed = int(self.base_speed * 1.2)
            self.name = f"Alpha {original_name}"
            self.description = f"An Alpha variant of {original_name}. As the leader of its species, it has well-balanced and enhanced abilities."

        elif variant_name == "Corrupted":
            # Corrupted variants have more attack but less defense
            self.base_hp = int(self.base_hp * 1.1)
            self.base_attack = int(self.base_attack * 1.5)
            self.base_defense = int(self.base_defense * 0.8)
            self.base_speed = int(self.base_speed * 1.2)
            self.name = f"Corrupted {original_name}"
            self.description = f"A Corrupted variant of {original_name}. It has been tainted by dark energy, giving it tremendous offensive power but weakening its defenses."

        elif variant_name == "Crystal":
            # Crystal variants have much higher defense but less attack
            self.base_hp = int(self.base_hp * 1.1)
            self.base_attack = int(self.base_attack * 0.9)
            self.base_defense = int(self.base_defense * 1.8)
            self.base_speed = int(self.base_speed * 0.8)
            self.name = f"Crystal {original_name}"
            self.description = f"A Crystal variant of {original_name}. Its body is encased in nearly impenetrable crystalline structures, greatly enhancing its defensive capabilities."

        elif variant_name == "Dominant":
            # Dominant variants have double stats but are extremely rare
            self.base_hp = int(self.base_hp * 2.0)
            self.base_attack = int(self.base_attack * 2.0)
            self.base_defense = int(self.base_defense * 2.0)
            self.base_speed = int(self.base_speed * 2.0)
            self.name = f"Dominant {original_name}"
            self.description = f"A Dominant variant of {original_name}. This colossal specimen dwarfs others of its kind, possessing truly extraordinary power."

    def calculate_stats(self):
        """Calculate stats based on monster level and base stats"""
        level_factor = 1 + (self.level / 50)
        self.max_hp = int(self.base_hp * level_factor)
        self.attack = int(self.base_attack * level_factor)
        self.defense = int(self.base_defense * level_factor)
        self.speed = int(self.base_speed * level_factor)

    def gain_exp(self, amount: int) -> bool:
        """Give exp to monster, return True if leveled up"""
        # Check if monster is at trainer level cap before adding exp
        player = None
        for game_obj in globals().values():
            if isinstance(game_obj, Game) and hasattr(game_obj, 'player'):
                player = game_obj.player
                if player and hasattr(player, 'monsters'):
                    for monster in player.monsters:
                        if monster is self:
                            break

        # If monster is at max level (double trainer level), give exp to trainer instead
        if player and hasattr(player, 'trainer_level'):
            max_monster_level = player.trainer_level * 2
            if self.level >= max_monster_level:
                # Monster is maxed, give exp to trainer instead
                print(f"{Fore.CYAN}{self.name} is at max level! Trainer gains {amount} EXP instead.{Style.RESET_ALL}")
                if hasattr(player, 'gain_trainer_exp'):
                    trainer_leveled = player.gain_trainer_exp(amount)
                    if trainer_leveled:
                        print(f"{Fore.GREEN}Trainer leveled up! New level: {player.trainer_level}{Style.RESET_ALL}")
                return False

        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Level up the monster and calculate new stats"""
        # Check if player has this monster in their collection (to get trainer level)
        player = None
        for game_obj in globals().values():
            if isinstance(game_obj, Game) and hasattr(game_obj, 'player'):
                player = game_obj.player
                if player and hasattr(player, 'monsters'):
                    for monster in player.monsters:
                        if monster is self:  # Check if this is the same object
                            # Found the player that owns this monster
                            break

        # Apply trainer level cap if applicable (monsters can level up to double trainer level)
        if player and hasattr(player, 'trainer_level'):
            max_monster_level = player.trainer_level * 2
            if self.level >= max_monster_level:
                # Monster is at max level (double trainer level), don't level up
                # Cap exp to prevent further level up attempts
                self.exp = min(self.exp, self.exp_to_level - 1)
                return

        self.level += 1
        if self.level > MAX_MONSTER_LEVEL:
            self.level = MAX_MONSTER_LEVEL
            return

        self.exp = self.exp - self.exp_to_level
        self.exp_to_level = self.level * 20
        old_max_hp = self.max_hp

        self.calculate_stats()

        # Heal some HP on level up (the difference plus a bit more)
        hp_gain = self.max_hp - old_max_hp + int(self.max_hp * 0.1)
        self.current_hp = min(self.max_hp, self.current_hp + hp_gain)

    def get_colored_name(self) -> str:
        """Return the name with appropriate color based on type"""
        # Dictionary of colors for each type
        type_colors = {
            "Grass": Fore.GREEN,
            "Fire": Fore.RED,
            "Water": Fore.BLUE,
            "Normal": Fore.WHITE,
            "Electric": Fore.YELLOW,
            "Ground": Fore.LIGHTYELLOW_EX,
            "Rock": Fore.LIGHTBLACK_EX,
            "Ice": Fore.LIGHTCYAN_EX,
            "Psychic": Fore.MAGENTA,
            "Dark": Fore.BLACK,
            "Fairy": Fore.LIGHTMAGENTA_EX,
            "Dragon": Fore.LIGHTRED_EX,
            "Flying": Fore.LIGHTBLUE_EX,
            "Fighting": Fore.LIGHTRED_EX,
            "Poison": Fore.MAGENTA,
            "Time": Fore.CYAN,
            "Space": Fore.BLUE,
            "Cosmic": Fore.LIGHTMAGENTA_EX + Fore.LIGHTYELLOW_EX,
            "Dread": Fore.BLACK + Fore.RED,
            "Life": Fore.LIGHTGREEN_EX + Fore.WHITE,
            "Ghost": Fore.WHITE + Fore.LIGHTBLACK_EX
        }

        if self.type in type_colors:
            return f"{type_colors[self.type]}{self.name}{Style.RESET_ALL}"
        else:
            return self.name

    def is_fainted(self) -> bool:
        """Check if monster has fainted (HP <= 0)"""
        return self.current_hp <= 0

    def heal(self, amount: int):
        """Heal the monster by a specific amount"""
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def full_heal(self):
        """Fully heal the monster"""
        self.current_hp = self.max_hp

    def __str__(self) -> str:
        """String representation of a monster"""
        hp_percentage = self.current_hp / self.max_hp
        hp_bar = "█" * int(hp_percentage * 10) + "░" * (10 - int(hp_percentage * 10))

        if hp_percentage > 0.5:
            hp_color = Fore.GREEN
        elif hp_percentage > 0.2:
            hp_color = Fore.YELLOW
        else:
            hp_color = Fore.RED

        # Variant indicator with special color
        variant_text = ""
        if self.variant:
            variant_colors = {
                "Omega": Fore.BLUE + Style.BRIGHT,
                "Alpha": Fore.RED + Style.BRIGHT,
                "Corrupted": Fore.MAGENTA + Style.BRIGHT,
                "Crystal": Fore.CYAN + Style.BRIGHT,
                "Dominant": Fore.YELLOW + Style.BRIGHT
            }
            color = variant_colors.get(self.variant, Fore.WHITE)
            variant_text = f" [{color}{self.variant}{Style.RESET_ALL}]"

        return (f"{self.get_colored_name()}{variant_text} (Lv.{self.level}) - {self.type} Type\n"
                f"HP: {hp_color}{self.current_hp}/{self.max_hp} [{hp_bar}]{Style.RESET_ALL}\n"
                f"Attack: {self.attack}, Defense: {self.defense}, Speed: {self.speed}\n"
                f"EXP: {self.exp}/{self.exp_to_level}")

    def clone(self):
        """Create a copy of this monster"""
        copy = Monster(
            self.name, self.type, self.base_hp, self.base_attack,
            self.base_defense, self.base_speed, self.moves,
            self.description, self.level, self.is_fusion, 
            self.fusion_components.copy() if self.fusion_components else None,
            self.variant
        )
        return copy

    @staticmethod
    def fuse(monster1: 'Monster', monster2: 'Monster') -> Optional['Monster']:
        """Fuse two monsters to create a new, more powerful monster"""
        # Check if both monsters meet the level requirement
        if monster1.level < FUSION_LEVEL_REQUIREMENT or monster2.level < FUSION_LEVEL_REQUIREMENT:
            return None

        # Create fusion name (combine parts of both names)
        if len(monster1.name) > len(monster2.name):
            name_parts = [monster1.name[:len(monster1.name)//2], monster2.name[len(monster2.name)//2:]]
        else:
            name_parts = [monster1.name[:len(monster1.name)//2], monster2.name[len(monster2.name)//2:]]
        fusion_name = ''.join(name_parts)

        # Determine fusion type (primary monster's type with influence from secondary)
        fusion_type = monster1.type

        # Combine stats (primary stats with a boost from secondary)
        base_hp = int(monster1.base_hp * 1.2 + monster2.base_hp * 0.3)
        base_attack = int(monster1.base_attack * 1.2 + monster2.base_attack * 0.3)
        base_defense = int(monster1.base_defense * 1.2 + monster2.base_defense * 0.3)
        base_speed = int(monster1.base_speed * 1.2 + monster2.base_speed * 0.3)

        # Get best moves from both monsters
        # Sort moves by power and take the top 4
        combined_moves = monster1.moves + monster2.moves
        unique_moves = []
        move_names = set()

        for move in sorted(combined_moves, key=lambda m: m.power, reverse=True):
            if move.name not in move_names and len(unique_moves) < 4:
                unique_moves.append(move)
                move_names.add(move.name)

        # Create fusion description
        fusion_desc = f"A powerful fusion of {monster1.name} and {monster2.name}."

        # Set fusion level (average of both parents, minimum 25)
        fusion_level = max(FUSION_LEVEL_REQUIREMENT, (monster1.level + monster2.level) // 2)

        # Create fusion components list
        fusion_components = [monster1.name, monster2.name]
        if monster1.is_fusion:
            fusion_components.extend(monster1.fusion_components)
        if monster2.is_fusion:
            fusion_components.extend(monster2.fusion_components)

        # Create the fusion monster
        fusion = Monster(
            fusion_name, fusion_type, base_hp, base_attack,
            base_defense, base_speed, unique_moves,
            fusion_desc, fusion_level, is_fusion=True,
            fusion_components=list(set(fusion_components))  # Remove duplicates
        )

        return fusion


# Player class
class Player:
    def __init__(self, name: str):
        self.name = name
        self.monsters: List[Monster] = []
        self.active_monster_index = 0
        self.inventory: Dict[Item, int] = {}  # Dictionary to store items and quantities
        self.money = 500
        self.tokens = 500  # Add tokens attribute
        self.location = "Hometown"
        self.current_location = "Forest Grove"  # Add current_location
        self.trainer_level = 5  # Starting level
        self.exp = 0
        self.exp_to_level = 100  # Initial exp needed to level up

        # Initialize story progress tracking
        self.story_progress = {}

        # Initialize quest items
        self.quest_items = []

        # Emotional Response System
        self.reputation = {
            "kindness": 0,      # Helping, healing, showing mercy
            "cruelty": 0,       # Unnecessarily harsh actions
            "bravery": 0,       # Taking risks, facing danger
            "wisdom": 0,        # Making thoughtful choices
            "greed": 0,         # Prioritizing money/items over others
            "honor": 0,         # Keeping promises, fair play
            "recklessness": 0,  # Dangerous or thoughtless actions
            "compassion": 0     # Caring for others' wellbeing
        }
        self.npc_relationships = {}  # Track individual NPC relationships
        self.monster_bonds = {}      # Track emotional bonds with monsters
        self.recent_actions = []     # Track recent player actions for context

        # Narrative Reflection System
        self.story_moments = []      # Track significant story moments for reflection
        self.moral_choices = []      # Track moral decisions and their outcomes
        self.reflection_points = 0   # Earned through meaningful actions

        # Advanced Dialogue System
        self.dialogue_history = {}   # Track conversations with NPCs
        self.conversation_flags = {} # Track conversation state flags
        self.dialogue_choices_made = [] # Track choices made in conversations
        self.character_opinions = {} # How NPCs view the player based on dialogue
        self.unlocked_dialogue_trees = set() # Advanced dialogue options unlocked

        # New RPG attributes
        self.skills = {
            'Monster Training': 1,
            'Battle Strategy': 1,
            'Monster Care': 1,
            'Exploration': 1,
            'Monster Catching': 1,
            'Item Crafting': 1,
            'Trading': 1,
            'Research': 1
        }
        self.skill_points = 3
        self.equipment = {
            'weapon': None,
            'armor': None,
            'accessory': None,
            'tool': None
        }
        self.materials = {
            'Monster Essence': 0,
            'Crystal Shards': 0,
            'Metal Ore': 0,
            'Ancient Bones': 0,
            'Mystic Herbs': 0
        }
        self.guild: Optional[str] = None
        self.guild_rank = 'Member'
        self.guild_contribution = 0
        self.active_quests = []
        self.completed_quests = []
        self.achievements = set()
        self.visited_areas = {'Forest Grove'}
        self.battle_wins = 0
        self.battle_losses = 0
        self.playtime = 0
        self.daily_tasks = {
            'catch_monsters': {'progress': 0, 'target': 3, 'completed': False},
            'win_battles': {'progress': 0, 'target': 5, 'completed': False},
            'explore_areas': {'progress': 0, 'target': 2, 'completed': False},
            'use_items': {'progress': 0, 'target': 4, 'completed': False}
        }

    @property
    def active_monster(self) -> Optional[Monster]:
        """Get the currently active monster"""
        if not self.monsters or self.active_monster_index >= len(self.monsters):
            return None
        return self.monsters[self.active_monster_index]

    def has_usable_monster(self) -> bool:
        """Check if the player has at least one monster that can fight"""
        return any(not monster.is_fainted() for monster in self.monsters)

    def get_first_usable_monster_index(self) -> int:
        """Get the index of the first usable (non-fainted) monster"""
        for i, monster in enumerate(self.monsters):
            if not monster.is_fainted():
                return i
        return -1

    def switch_active_monster(self, index: int) -> bool:
        """Switch active monster to the one at the given index"""
        if 0 <= index < len(self.monsters):
            self.active_monster_index = index
            return True
        return False

    def add_monster(self, monster: Monster):
        """Add a monster to the player's collection"""
        self.monsters.append(monster)

    def add_item(self, item: Item, quantity: int = 1):
        """Add an item to the inventory"""
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def gain_trainer_exp(self, amount: int) -> bool:
        """Give experience to the trainer, return True if leveled up"""
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up_trainer()
            return True
        return False

    def level_up_trainer(self):
        """Level up the trainer"""
        self.trainer_level += 1
        self.exp = 0
        self.exp_to_level = int(self.exp_to_level * 1.2)  # Each level requires more exp

        print(f"{Fore.GREEN}You leveled up! You are now a level {self.trainer_level} trainer!{Style.RESET_ALL}")
        print("Your monsters' maximum level is now capped at your trainer level.")

        # Check if any monsters need level adjustment
        for monster in self.monsters:
            if monster.level > self.trainer_level:
                # Don't actually decrease levels, just cap future growth
                print(f"{monster.get_colored_name()} will not grow beyond level {self.trainer_level} until you level up more.")

    def use_item(self, item_index: int, target_monster_index: Optional[int] = None) -> str:
        """Use an item from the inventory"""
        if target_monster_index is None:
            target_monster_index = self.active_monster_index

        items = list(self.inventory.keys())
        if 0 <= item_index < len(items):
            item = items[item_index]

            # Check if we have this item
            if self.inventory[item] <= 0:
                return f"You don't have any {item.name} left."

            # Check if target monster exists
            if target_monster_index >= len(self.monsters):
                return "Invalid monster selected."

            target_monster = self.monsters[target_monster_index]

            # Apply item effect
            result = ""
            if item.effect == "heal":
                heal_amount = item.value
                old_hp = target_monster.current_hp
                target_monster.heal(heal_amount)
                actual_heal = target_monster.current_hp - old_hp
                result = f"Restored {actual_heal} HP to {target_monster.get_colored_name()}."
            elif item.effect == "revive":
                if not target_monster.is_fainted():
                    return f"{target_monster.get_colored_name()} doesn't need to be revived."
                target_monster.current_hp = int(target_monster.max_hp * (item.value / 100.0))
                result = f"Revived {target_monster.get_colored_name()} with {target_monster.current_hp} HP."
            elif item.effect == "catch":
                # This shouldn't be used directly through inventory
                result = "You can't use this item outside of battle."
                return result
            else:
                result = f"Used {item.name} on {target_monster.get_colored_name()}."

            # Consume the item
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                self.inventory.pop(item)

            return result

        return "Invalid item selected."

    def track_action(self, action_type: str, context: str = "", value: int = 1):
        """Track player actions for emotional response system"""
        import time

        # Add to recent actions (keep last 20 actions)
        action_data = {
            "type": action_type,
            "context": context,
            "value": value,
            "timestamp": time.time()
        }
        self.recent_actions.append(action_data)
        if len(self.recent_actions) > 20:
            self.recent_actions.pop(0)

        # Update reputation based on action type
        if action_type == "heal_monster":
            self.reputation["kindness"] += value
            self.reputation["compassion"] += value
        elif action_type == "help_npc":
            self.reputation["kindness"] += value * 2
            self.reputation["honor"] += value
        elif action_type == "spare_enemy":
            self.reputation["compassion"] += value * 2
            self.reputation["wisdom"] += value
        elif action_type == "cruel_action":
            self.reputation["cruelty"] += value
            self.reputation["kindness"] = max(0, self.reputation["kindness"] - value)
        elif action_type == "brave_deed":
            self.reputation["bravery"] += value
        elif action_type == "wise_choice":
            self.reputation["wisdom"] += value
        elif action_type == "greedy_action":
            self.reputation["greed"] += value
            self.reputation["honor"] = max(0, self.reputation["honor"] - value)
        elif action_type == "reckless_action":
            self.reputation["recklessness"] += value
            self.reputation["wisdom"] = max(0, self.reputation["wisdom"] - value)
        elif action_type == "honorable_action":
            self.reputation["honor"] += value

        # Cap reputation values at reasonable ranges
        for trait in self.reputation:
            self.reputation[trait] = max(-50, min(100, self.reputation[trait]))

    def update_monster_bond(self, monster_name: str, bond_change: int, reason: str = ""):
        """Update emotional bond with a specific monster"""
        if monster_name not in self.monster_bonds:
            self.monster_bonds[monster_name] = {
                "trust": 50,
                "happiness": 50,
                "loyalty": 50,
                "respect": 50,
                "fear": 0
            }

        bond = self.monster_bonds[monster_name]

        # Adjust bonds based on reason
        if "heal" in reason.lower():
            bond["trust"] += bond_change
            bond["happiness"] += bond_change
        elif "victory" in reason.lower():
            bond["respect"] += bond_change
            bond["loyalty"] += bond_change
        elif "abandon" in reason.lower():
            bond["trust"] -= bond_change * 2
            bond["loyalty"] -= bond_change * 2
        elif "cruel" in reason.lower():
            bond["fear"] += bond_change
            bond["trust"] -= bond_change
        elif "care" in reason.lower():
            bond["happiness"] += bond_change
            bond["trust"] += bond_change

        # Cap bond values
        for emotion in bond:
            bond[emotion] = max(0, min(100, bond[emotion]))

    def update_npc_relationship(self, npc_name: str, relationship_change: int, reason: str = ""):
        """Update relationship with a specific NPC"""
        if npc_name not in self.npc_relationships:
            self.npc_relationships[npc_name] = {
                "trust": 50,
                "respect": 50,
                "friendship": 50,
                "fear": 0,
                "admiration": 50
            }

        relationship = self.npc_relationships[npc_name]

        # Adjust relationships based on reason
        if "help" in reason.lower():
            relationship["trust"] += relationship_change
            relationship["friendship"] += relationship_change
        elif "impress" in reason.lower():
            relationship["admiration"] += relationship_change
            relationship["respect"] += relationship_change
        elif "betray" in reason.lower():
            relationship["trust"] -= relationship_change * 2
            relationship["friendship"] -= relationship_change
        elif "threaten" in reason.lower():
            relationship["fear"] += relationship_change
            relationship["trust"] -= relationship_change

        # Cap relationship values
        for emotion in relationship:
            relationship[emotion] = max(0, min(100, relationship[emotion]))

    def get_reputation_summary(self) -> str:
        """Get a summary of the player's reputation"""
        dominant_traits = []
        for trait, value in self.reputation.items():
            if value >= 30:
                dominant_traits.append(f"{trait.title()}: {value}")

        if not dominant_traits:
            return "You have no particularly notable reputation traits."

        return "Your reputation: " + ", ".join(dominant_traits)

    def add_story_moment(self, moment_type: str, description: str, location: str, consequences: str = ""):
        """Add a significant story moment for later reflection"""
        import time

        story_moment = {
            "type": moment_type,
            "description": description,
            "location": location,
            "consequences": consequences,
            "timestamp": time.time(),
            "reflected_upon": False
        }
        self.story_moments.append(story_moment)

        # Keep only last 15 story moments to avoid memory bloat
        if len(self.story_moments) > 15:
            self.story_moments.pop(0)

    def add_moral_choice(self, choice_description: str, option_chosen: str, outcome: str, karma_impact: dict):
        """Track a moral choice and its consequences"""
        import time

        moral_choice = {
            "choice": choice_description,
            "chosen_option": option_chosen,
            "outcome": outcome,
            "karma_impact": karma_impact,
            "timestamp": time.time(),
            "location": self.location,
            "reflected_upon": False
        }
        self.moral_choices.append(moral_choice)

        # Apply karma impact to reputation
        for trait, change in karma_impact.items():
            if trait in self.reputation:
                self.reputation[trait] += change

        # Keep only last 10 moral choices
        if len(self.moral_choices) > 10:
            self.moral_choices.pop(0)

    def earn_reflection_points(self, points: int, reason: str = ""):
        """Earn reflection points for meaningful actions"""
        self.reflection_points += points
        if reason:
            self.track_action("earn_reflection", reason, points)

    def record_dialogue_choice(self, npc_name: str, dialogue_id: str, choice_text: str, consequence: str = ""):
        """Record a dialogue choice and its consequences"""
        import time

        dialogue_record = {
            "npc": npc_name,
            "dialogue_id": dialogue_id,
            "choice": choice_text,
            "consequence": consequence,
            "timestamp": time.time(),
            "location": self.location
        }
        self.dialogue_choices_made.append(dialogue_record)

        # Update dialogue history with this NPC
        if npc_name not in self.dialogue_history:
            self.dialogue_history[npc_name] = []
        self.dialogue_history[npc_name].append(dialogue_record)

        # Keep only last 20 dialogue choices
        if len(self.dialogue_choices_made) > 20:
            self.dialogue_choices_made.pop(0)

    def set_conversation_flag(self, flag_name: str, value):
        """Set a conversation state flag"""
        self.conversation_flags[flag_name] = value

    def get_conversation_flag(self, flag_name: str, default=None):
        """Get a conversation state flag"""
        return self.conversation_flags.get(flag_name, default)

    def update_character_opinion(self, npc_name: str, opinion_change: int, reason: str = ""):
        """Update how an NPC views the player based on dialogue choices"""
        if npc_name not in self.character_opinions:
            self.character_opinions[npc_name] = {
                "respect": 50,
                "trust": 50,
                "friendliness": 50,
                "interest": 50
            }

        opinion = self.character_opinions[npc_name]

        # Adjust opinion based on reason
        if "respectful" in reason.lower():
            opinion["respect"] += opinion_change
            opinion["trust"] += opinion_change // 2
        elif "rude" in reason.lower():
            opinion["respect"] -= opinion_change
            opinion["friendliness"] -= opinion_change
        elif "honest" in reason.lower():
            opinion["trust"] += opinion_change
            opinion["respect"] += opinion_change // 2
        elif "deceptive" in reason.lower():
            opinion["trust"] -= opinion_change * 2
        elif "friendly" in reason.lower():
            opinion["friendliness"] += opinion_change
            opinion["interest"] += opinion_change // 2
        elif "interesting" in reason.lower():
            opinion["interest"] += opinion_change
        else:
            # General opinion change
            for trait in opinion:
                opinion[trait] += opinion_change // 4

        # Cap opinion values
        for trait in opinion:
            opinion[trait] = max(0, min(100, opinion[trait]))

    def unlock_dialogue_tree(self, tree_name: str):
        """Unlock a new dialogue tree based on player actions or progress"""
        self.unlocked_dialogue_trees.add(tree_name)
        self.track_action("unlock_dialogue", f"Unlocked {tree_name} dialogue tree", 1)

def generate_monster_reaction(player, monster_name: str, context: str = "encounter") -> str:
    """Generate emotional reaction from a monster based on player reputation and bond"""
    reactions = []

    # Get monster bond if exists
    bond = player.monster_bonds.get(monster_name, {
        "trust": 50, "happiness": 50, "loyalty": 50, "respect": 50, "fear": 0
    })

    # Base reactions on context
    if context == "encounter":
        if player.reputation["cruelty"] > 30:
            if bond["fear"] > 70:
                reactions.append(f"The {monster_name} cowers in terror, remembering your cruel reputation.")
            else:
                reactions.append(f"The {monster_name} eyes you warily, sensing your harsh nature.")
        elif player.reputation["kindness"] > 30:
            if bond["trust"] > 70:
                reactions.append(f"The {monster_name} approaches you with complete trust and affection.")
            else:
                reactions.append(f"The {monster_name} seems curious about your gentle aura.")
        elif player.reputation["bravery"] > 30:
            reactions.append(f"The {monster_name} shows respect for your courageous spirit.")

    elif context == "battle":
        if bond["loyalty"] > 80:
            reactions.append(f"The {monster_name} fights with unwavering determination for you!")
        elif bond["fear"] > 60:
            reactions.append(f"The {monster_name} hesitates, afraid of disappointing you.")
        elif bond["trust"] < 30:
            reactions.append(f"The {monster_name} seems reluctant to follow your commands.")

    elif context == "victory":
        if bond["respect"] > 70:
            reactions.append(f"The {monster_name} looks at you with deep admiration and pride.")
        elif player.reputation["honor"] > 40:
            reactions.append(f"The {monster_name} nods approvingly at your honorable victory.")

    return reactions[0] if reactions else f"The {monster_name} regards you neutrally."

def generate_npc_reaction(player, npc_name: str, context: str = "dialogue") -> str:
    """Generate emotional reaction from an NPC based on player reputation and relationship"""
    reactions = []

    # Get NPC relationship if exists
    relationship = player.npc_relationships.get(npc_name, {
        "trust": 50, "respect": 50, "friendship": 50, "fear": 0, "admiration": 50
    })

    # Base reactions on player reputation
    if player.reputation["kindness"] > 50:
        if relationship["friendship"] > 70:
            reactions.append(f"{npc_name} greets you warmly, their eyes lighting up with joy.")
        else:
            reactions.append(f"{npc_name} smiles genuinely, appreciating your kind nature.")

    elif player.reputation["cruelty"] > 40:
        if relationship["fear"] > 60:
            reactions.append(f"{npc_name} backs away nervously, clearly intimidated by your presence.")
        else:
            reactions.append(f"{npc_name} regards you with obvious suspicion and caution.")

    elif player.reputation["wisdom"] > 40:
        if relationship["respect"] > 70:
            reactions.append(f"{npc_name} speaks to you with deep respect and deference.")
        else:
            reactions.append(f"{npc_name} listens carefully to your words, recognizing your wisdom.")

    elif player.reputation["greed"] > 40:
        if relationship["trust"] < 30:
            reactions.append(f"{npc_name} clutches their belongings, not trusting your intentions.")
        else:
            reactions.append(f"{npc_name} seems wary of making any deals with you.")

    # Context-specific reactions
    if context == "shop":
        if player.reputation["honor"] > 50:
            reactions.append(f"{npc_name} offers you a special discount for being such an honorable customer.")
        elif player.reputation["greed"] > 50:
            reactions.append(f"{npc_name} doubles their prices, knowing your greedy reputation.")

    elif context == "quest":
        if relationship["trust"] > 80:
            reactions.append(f"{npc_name} entrusts you with their most precious quest.")
        elif relationship["trust"] < 30:
            reactions.append(f"{npc_name} hesitates to give you important tasks.")

    return reactions[0] if reactions else f"{npc_name} greets you politely but distantly."

def get_monster_battle_bonus(player, monster_name: str) -> dict:
    """Calculate battle bonuses based on monster bond with player"""
    bond = player.monster_bonds.get(monster_name, {
        "trust": 50, "happiness": 50, "loyalty": 50, "respect": 50, "fear": 0
    })

    bonuses = {
        "attack_bonus": 0.0,
        "defense_bonus": 0.0,
        "accuracy_bonus": 0.0,
        "crit_bonus": 0.0
    }

    # High loyalty gives attack bonus
    if bond["loyalty"] > 80:
        bonuses["attack_bonus"] = 0.2
    elif bond["loyalty"] > 60:
        bonuses["attack_bonus"] = 0.1

    # High trust gives accuracy bonus
    if bond["trust"] > 80:
        bonuses["accuracy_bonus"] = 0.15
    elif bond["trust"] > 60:
        bonuses["accuracy_bonus"] = 0.1

    # High respect gives critical hit bonus
    if bond["respect"] > 80:
        bonuses["crit_bonus"] = 0.1
    elif bond["respect"] > 60:
        bonuses["crit_bonus"] = 0.05

    # High happiness gives defense bonus
    if bond["happiness"] > 80:
        bonuses["defense_bonus"] = 0.15
    elif bond["happiness"] > 60:
        bonuses["defense_bonus"] = 0.1

    # Fear reduces all bonuses
    if bond["fear"] > 50:
        fear_penalty = (bond["fear"] - 50) / 100
        for bonus_type in bonuses:
            bonuses[bonus_type] *= (1 - fear_penalty)

    return bonuses


# Battle class
class Battle:
    def __init__(self, player: Optional[Player], wild_monster: Monster):
        self.player = player
        self.wild_monster = wild_monster
        self.turn = 0
        self.is_wild = True
        self.can_catch = True
        self.is_finished = False
        self.result = None  # 'win', 'lose', 'run', 'catch'

    def calculate_damage(self, attacker: Monster, defender: Monster, move: Move) -> Tuple[int, float]:
        """Calculate damage and type effectiveness for a move"""
        # Check for accuracy
        if random.random() > move.accuracy:
            return 0, 1.0  # Miss

        # Base damage formula
        damage = (2 * attacker.level / 5 + 2) * move.power * (attacker.attack / defender.defense) / 50 + 2

        # Critical hit (1/16 chance)
        critical = 1.5 if random.random() < 0.0625 else 1.0

        # Type effectiveness
        effectiveness = self.calculate_type_effectiveness(move.type, defender.type)

        # Random factor (0.85 to 1.0)
        random_factor = random.uniform(0.85, 1.0)

        # Final damage calculation
        final_damage = int(damage * critical * effectiveness * random_factor)
        return max(1, final_damage), effectiveness

    def calculate_type_effectiveness(self, move_type: str, defender_type: str) -> float:
        """Calculate type effectiveness multiplier"""
        # Type effectiveness chart
        effectiveness_chart = {
            # Format: attacking type -> {defending type: multiplier}
            "Grass": {
                "Water": 2.0, "Ground": 2.0, "Rock": 2.0,
                "Fire": 0.5, "Flying": 0.5, "Poison": 0.5, "Bug": 0.5, "Dragon": 0.5
            },
            "Fire": {
                "Grass": 2.0, "Ice": 2.0, "Bug": 2.0,
                "Water": 0.5, "Rock": 0.5, "Dragon": 0.5
            },
            "Water": {
                "Fire": 2.0, "Ground": 2.0, "Rock": 2.0,
                "Grass": 0.5, "Dragon": 0.5
            },
            "Electric": {
                "Water": 2.0, "Flying": 2.0,
                "Grass": 0.5, "Ground": 0.0, "Dragon": 0.5
            },
            "Ice": {
                "Grass": 2.0, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0,
                "Fire": 0.5, "Water": 0.5
            },
            "Fighting": {
                "Normal": 2.0, "Rock": 2.0, "Ice": 2.0, "Dark": 2.0,
                "Flying": 0.5, "Poison": 0.5, "Psychic": 0.5, "Fairy": 0.5
            },
            "Poison": {
                "Grass": 2.0, "Fairy": 2.0,
                "Ground": 0.5, "Rock": 0.5, "Poison": 0.5
            },
            "Ground": {
                "Fire": 2.0, "Electric": 2.0, "Poison": 2.0, "Rock": 2.0,
                "Grass": 0.5, "Flying": 0.0
            },
            "Flying": {
                "Grass": 2.0, "Fighting": 2.0,
                "Electric": 0.5, "Rock": 0.5
            },
            "Psychic": {
                "Fighting": 2.0, "Poison": 2.0,
                "Dark": 0.0, "Psychic": 0.5
            },
            "Rock": {
                "Fire": 2.0, "Ice": 2.0, "Flying": 2.0,
                "Fighting": 0.5, "Ground": 0.5
            },
            "Dragon": {
                "Dragon": 2.0,
                "Fairy": 0.0
            },
            "Time": {
                "Space": 2.0, "Psychic": 2.0, "Ghost": 2.0,
                "Dark": 0.5, "Cosmic": 0.5
            },
            "Space": {
                "Time": 2.0, "Fairy": 2.0, "Psychic": 2.0,
                "Cosmic": 0.5, "Dragon": 0.5
            },
            "Cosmic": {
                "Dark": 2.0, "Ghost": 2.0, "Psychic": 2.0,
                "Time": 0.5, "Space": 0.5, "Dread": 0.5
            },
            "Dread": {
                "Psychic": 2.0, "Life": 2.0, "Ghost": 2.0,
                "Dark": 0.5, "Cosmic": 0.5, "Fighting": 0.5
            },
            "Life": {
                "Water": 2.0, "Ground": 2.0, "Rock": 2.0,
                "Fire": 0.5, "Dread": 0.5, "Ghost": 0.5
            },
            "Ghost": {
                "Psychic": 2.0, "Ghost": 2.0, "Dark": 2.0,
                "Normal": 0.0, "Fighting": 0.0, "Dread": 0.5
            },
            "Dark": {
                "Psychic": 2.0, "Ghost": 2.0,
                "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5
            },
            "Fairy": {
                "Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0,
                "Fire": 0.5, "Poison": 0.5
            }
        }

        # If attacker type is in the chart
        if move_type in effectiveness_chart:
            # If defender type is in the attackers chart
            if defender_type in effectiveness_chart[move_type]:
                return effectiveness_chart[move_type][defender_type]

        # Same type is not very effective
        if move_type == defender_type:
            return 0.75

        # Default effectiveness
        return 1.0

    def player_turn(self, command: str, argument: Optional[str] = None) -> str:
        """Handle player's turn in battle"""
        if self.is_finished:
            return "Battle is already over."

        if not self.player:
            self.is_finished = True
            self.result = "lose"
            return "No active player found!"

        player_monster = self.player.active_monster
        if player_monster is None:
            self.is_finished = True
            self.result = "lose"
            return "You have no monsters left to battle!"

        result = ""

        if command == "fight":
            # Use a move to attack
            try:
                # Ensure argument is not None before conversion
                if argument is not None:
                    move_index = int(argument) - 1
                else:
                    move_index = 0
                if 0 <= move_index < len(player_monster.moves):
                    move = player_monster.moves[move_index]
                    damage, effectiveness = self.calculate_damage(player_monster, self.wild_monster, move)

                    # Apply damage
                    self.wild_monster.current_hp = max(0, self.wild_monster.current_hp - damage)

                    # Generate result message
                    result = f"{player_monster.get_colored_name()} used {move.name}!\n"

                    if damage == 0:
                        result += "But it missed!"
                    else:
                        if effectiveness > 1.5:
                            result += "It's super effective! "
                        elif effectiveness < 0.75:
                            result += "It's not very effective... "

                        result += f"Dealt {damage} damage to {self.wild_monster.get_colored_name()}."

                        # Check if wild monster fainted
                        if self.wild_monster.is_fainted():
                            exp_gained = self.wild_monster.level * 5
                            level_up = player_monster.gain_exp(exp_gained)

                            result += f"\n{self.wild_monster.get_colored_name()} fainted!"
                            result += f"\n{player_monster.get_colored_name()} gained {exp_gained} EXP."

                            if level_up:
                                result += f"\n{player_monster.get_colored_name()} grew to level {player_monster.level}!"

                            self.is_finished = True
                            self.result = "win"
                            return result
                else:
                    return f"Invalid move number. Choose between 1 and {len(player_monster.moves)}."
            except ValueError:
                return "Please enter a valid move number."

        elif command == "catch":
            if not self.can_catch:
                return "You can't catch this monster!"

            # Find monster ball in inventory
            monster_ball = None
            for item in self.player.inventory:
                if item.effect == "catch":
                    monster_ball = item
                    break

            if monster_ball is None or self.player.inventory[monster_ball] <= 0:
                return "You don't have any Monster Balls!"

            # Consume the ball
            self.player.inventory[monster_ball] -= 1
            if self.player.inventory[monster_ball] <= 0:
                self.player.inventory.pop(monster_ball)

            # Calculate catch probability
            hp_factor = 1 - (self.wild_monster.current_hp / self.wild_monster.max_hp)
            level_factor = 1 - (self.wild_monster.level / MAX_MONSTER_LEVEL)
            catch_rate = CATCH_BASE_RATE + (hp_factor * 0.3) + (level_factor * 0.2)

            result = f"You threw a {monster_ball.name} at {self.wild_monster.get_colored_name()}!"

            # Animated dots for suspense
            print(result, end="")
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            if random.random() < catch_rate:
                # Successful catch
                result = f"Gotcha! {self.wild_monster.get_colored_name()} was caught!"

                # Add to player's monsters
                caught_monster = self.wild_monster.clone()  # Clone to avoid sharing state
                caught_monster.full_heal()  # Heal it up
                self.player.add_monster(caught_monster)

                self.is_finished = True
                self.result = "catch"
            else:
                # Failed catch
                result = f"Oh no! {self.wild_monster.get_colored_name()} broke free!"

        elif command == "switch":
            try:
                if not argument:
                    return "Please specify a monster number to switch to."

                monster_index = int(argument) - 1

                if not self.player:
                    return "Error: Player not available."

                if not self.player.monsters:
                    return "You don't have any monsters to switch to."

                if 0 <= monster_index < len(self.player.monsters):
                    if monster_index == self.player.active_monster_index:
                        return f"{self.player.monsters[monster_index].get_colored_name()} is already in battle!"

                    if self.player.monsters[monster_index].is_fainted():
                        return f"{self.player.monsters[monster_index].get_colored_name()} has fainted and can't battle!"

                    old_monster = self.player.active_monster
                    if not old_monster:
                        return "No active monster to switch from."

                    self.player.switch_active_monster(monster_index)

                    if not self.player.active_monster:
                        return "Failed to switch monsters."

                    result = f"You withdrew {old_monster.get_colored_name()} and sent out {self.player.active_monster.get_colored_name()}!"
                else:
                    return f"Invalid monster number. Choose between 1 and {len(self.player.monsters)}."
            except ValueError:
                return "Please enter a valid monster number."

        elif command == "item":
            try:
                if not argument:
                    return "Please specify an item number to use."

                if not self.player:
                    return "Error: Player not available."

                if not hasattr(self.player, 'inventory') or not self.player.inventory:
                    return "You don't have any items to use."

                item_index = int(argument) - 1
                items = list(self.player.inventory.keys())

                if 0 <= item_index < len(items):
                    item = items[item_index]
                    if item.effect == "catch":
                        return "Use the 'catch' command to throw a Monster Ball."

                    result = self.player.use_item(item_index)
                else:
                    return f"Invalid item number. Choose between 1 and {len(items)}."
            except ValueError:
                return "Please enter a valid item number."

        elif command == "run":
            # 80% chance to run from wild battles
            if self.is_wild:
                if random.random() < 0.8:
                    self.is_finished = True
                    self.result = "run"
                    return "Got away safely!"
                else:
                    result = "Couldn't escape!"
            else:
                return "You can't run from this battle!"

        else:
            return "Invalid command. Try 'fight', 'catch', 'switch', 'item', or 'run'."

        # If we get here, it's the wild monster's turn (unless battle ended)
        if not self.is_finished:
            wild_result = self.wild_monster_turn()
            result += "\n\n" + wild_result

        return result

    def wild_monster_turn(self) -> str:
        """Handle wild monster's turn in battle"""
        if not self.wild_monster:
            self.is_finished = True
            self.result = "win"
            return "No wild monster found!"

        if self.wild_monster.is_fainted():
            self.is_finished = True
            self.result = "win"
            return f"{self.wild_monster.get_colored_name()} fainted!"

        if not self.player:
            self.is_finished = True
            self.result = "lose"
            return "No active player found!"

        player_monster = self.player.active_monster
        if not player_monster:
            self.is_finished = True
            self.result = "lose"
            return "You have no active monster!"

        if player_monster.is_fainted():
            # Check if player has any usable monsters left
            if not self.player.has_usable_monster():
                self.is_finished = True
                self.result = "lose"
                return "All your monsters have fainted! You rush to the nearest healing center..."

            # Auto-switch to next usable monster
            next_index = self.player.get_first_usable_monster_index()
            old_monster = player_monster
            self.player.switch_active_monster(next_index)
            if not self.player.active_monster:
                return f"{old_monster.get_colored_name()} fainted! No other monsters available!"
            return f"{old_monster.get_colored_name()} fainted! You sent out {self.player.active_monster.get_colored_name()}!"

        # Choose a random move for the wild monster
        move = random.choice(self.wild_monster.moves)
        damage, effectiveness = self.calculate_damage(self.wild_monster, player_monster, move)

        # Apply damage
        player_monster.current_hp = max(0, player_monster.current_hp - damage)

        # Generate result message
        result = f"Wild {self.wild_monster.get_colored_name()} used {move.name}!\n"

        if damage == 0:
            result += "But it missed!"
        else:
            if effectiveness > 1.5:
                result += "It's super effective! "
            elif effectiveness < 0.75:
                result += "It's not very effective... "

            result += f"Dealt {damage} damage to {player_monster.get_colored_name()}."

            # Check if player monster fainted
            if player_monster.is_fainted():
                result += f"\n{player_monster.get_colored_name()} fainted!"

                # Check if player has any usable monsters left
                if not self.player.has_usable_monster():
                    self.is_finished = True
                    self.result = "lose"
                    result += "\nAll your monsters have fainted! You rush to the nearest healing center..."
                else:
                    result += "\nChoose another monster with 'switch <number>'."

        return result


# Game class to handle overall game state and flow
class Game:
    def __init__(self):
        self.player = None
        self.current_battle = None
        self.running = True
        self.all_monsters = self.create_all_monsters()
        self.all_items = self.create_all_items()
        self.locations = ["Hometown", "Forest", "Cave", "Beach", "Mountain", "Snowy Peaks", "Ancient Ruins", 
                         "Volcanic Crater", "Crystal Caverns", "Mystic Temple", "Haunted Graveyard", 
                         "Underwater City", "Sky Islands", "Desert Oasis", "Frozen Wasteland", 
                         "Neon City", "Enchanted Grove", "Shadow Realm", "Celestial Observatory"]
        self.turn_count = 0
        self.db_available = init_database()
        self.champion_battles_available = True
        self.champion_battles_completed = 0

    def create_all_monsters(self) -> Dict[str, Monster]:
        """Create all monster templates for the game"""
        # Create moves
        # Grass moves
        leaf_attack = Move("Leaf Attack", "Grass", 40, 1.0, "Attacks with sharp leaves")
        vine_whip = Move("Vine Whip", "Grass", 35, 1.0, "Whips the enemy with vines")
        seed_bomb = Move("Seed Bomb", "Grass", 55, 0.9, "Launches explosive seeds")
        leaf_storm = Move("Leaf Storm", "Grass", 70, 0.8, "Creates a storm of sharp leaves")

        # Fire moves
        ember = Move("Ember", "Fire", 40, 1.0, "A weak fire attack")
        fire_fang = Move("Fire Fang", "Fire", 45, 0.95, "Bites with flaming fangs")
        flame_thrower = Move("Flame Thrower", "Fire", 60, 0.85, "Shoots a stream of fire")
        fire_blast = Move("Fire Blast", "Fire", 75, 0.8, "A powerful blast of fire")

        # Water moves
        water_gun = Move("Water Gun", "Water", 40, 1.0, "Shoots a jet of water")
        bubble_beam = Move("Bubble Beam", "Water", 45, 0.95, "Fires bubbles at the opponent")
        hydro_pump = Move("Hydro Pump", "Water", 65, 0.8, "Blasts water at high pressure")
        surf = Move("Surf", "Water", 60, 0.9, "Creates a huge wave")

        # Normal moves
        tackle = Move("Tackle", "Normal", 35, 1.0, "A basic tackle attack")
        scratch = Move("Scratch", "Normal", 30, 1.0, "Scratches with sharp claws")
        body_slam = Move("Body Slam", "Normal", 50, 0.9, "Slams body into opponent")
        swift = Move("Swift", "Normal", 40, 1.0, "Fires star-shaped rays that never miss")

        # Electric moves
        spark = Move("Spark", "Electric", 40, 1.0, "A small electric shock")
        thunder_shock = Move("Thunder Shock", "Electric", 50, 0.9, "A mild electric attack")
        thunderbolt = Move("Thunderbolt", "Electric", 65, 0.85, "A strong electric attack")
        thunder = Move("Thunder", "Electric", 75, 0.8, "A massive lightning strike")

        # Rock/Ground moves
        rock_throw = Move("Rock Throw", "Rock", 50, 0.9, "Throws rocks at the target")
        rock_slide = Move("Rock Slide", "Rock", 65, 0.85, "Causes rocks to slide down")
        earthquake = Move("Earthquake", "Ground", 70, 0.8, "Creates a powerful earthquake")
        sand_tomb = Move("Sand Tomb", "Ground", 55, 0.9, "Traps opponent in quicksand")
        earth_power = Move("Earth Power", "Ground", 75, 0.85, "Releases energy from the earth")

        # Ice moves
        ice_shard = Move("Ice Shard", "Ice", 45, 0.95, "Shoots sharp ice shards")
        ice_beam = Move("Ice Beam", "Ice", 65, 0.85, "Fires a freezing beam")
        blizzard = Move("Blizzard", "Ice", 75, 0.8, "Creates a freezing snowstorm")

        # Psychic moves
        psybeam = Move("Psybeam", "Psychic", 55, 0.9, "Fires a strange beam")
        psychic_blast = Move("Psychic Blast", "Psychic", 65, 0.85, "Strikes with psychic power")
        dream_eater = Move("Dream Eater", "Psychic", 75, 0.8, "Absorbs energy from the opponent's mind")

        # Dragon moves
        dragon_rage = Move("Dragon Rage", "Dragon", 55, 0.9, "Releases dragon energy")
        dragon_claw = Move("Dragon Claw", "Dragon", 65, 0.85, "Slashes with dragon claws")
        draco_meteor = Move("Draco Meteor", "Dragon", 90, 0.75, "Summons meteors from the sky")

        # Legendary specific moves
        time_warp = Move("Time Warp", "Time", 85, 0.8, "Manipulates the flow of time to strike")
        chronoblast = Move("Chronoblast", "Time", 95, 0.7, "A blast of temporal energy")
        celestial_beam = Move("Celestial Beam", "Cosmic", 90, 0.8, "A beam of celestial light")
        cosmic_power = Move("Cosmic Power", "Cosmic", 80, 0.85, "Harnesses the power of the cosmos")
        inferno = Move("Inferno", "Fire", 90, 0.7, "Creates an intense inferno")
        magma_burst = Move("Magma Burst", "Fire", 85, 0.8, "Erupts with molten magma")
        crystal_charge = Move("Crystal Charge", "Rock", 80, 0.85, "Charges with crystalline energy")
        diamond_drill = Move("Diamond Drill", "Rock", 90, 0.7, "Drills through anything with diamond strength")
        dark_void = Move("Dark Void", "Dark", 80, 0.8, "Creates a void of darkness")
        shadow_force = Move("Shadow Force", "Dark", 90, 0.7, "Strikes with the power of shadows")

        # New exclusive type moves
        temporal_shift = Move("Temporal Shift", "Time", 100, 0.8, "Shifts through time to deliver a devastating blow")
        time_stop = Move("Time Stop", "Time", 110, 0.7, "Briefly stops time to strike with impunity")
        dimensional_rift = Move("Dimensional Rift", "Space", 100, 0.8, "Tears open space to attack from multiple angles")
        gravity_crush = Move("Gravity Crush", "Space", 110, 0.7, "Manipulates gravity to crush the opponent")
        star_burst = Move("Star Burst", "Cosmic", 100, 0.8, "Unleashes the energy of an exploding star")
        galaxy_spiral = Move("Galaxy Spiral", "Cosmic", 110, 0.7, "Channels the spiral energy of galaxies")
        nightmare_feast = Move("Nightmare Feast", "Dread", 100, 0.8, "Feasts on the opponent's fears")
        terror_claw = Move("Terror Claw", "Dread", 110, 0.7, "Strikes with claws made of pure terror")
        nature_bloom = Move("Nature Bloom", "Life", 100, 0.8, "Unleashes explosive growth of nature's power")
        life_force = Move("Life Force", "Life", 110, 0.7, "Channels the fundamental force of life")
        spectral_grasp = Move("Spectral Grasp", "Ghost", 100, 0.8, "Grasps the opponent with spectral hands")
        soul_steal = Move("Soul Steal", "Ghost", 110, 0.7, "Temporarily steals a portion of the opponent's soul")

        # Fighting moves
        karate_chop = Move("Karate Chop", "Fighting", 50, 0.95, "Strikes with the edge of hand")
        brick_break = Move("Brick Break", "Fighting", 60, 0.9, "Breaks barriers with a punch")

        # Fairy moves
        fairy_wind = Move("Fairy Wind", "Fairy", 45, 0.95, "Stirs up a fairy wind")
        dazzling_gleam = Move("Dazzling Gleam", "Fairy", 65, 0.85, "Emits a powerful flash")

        # Dark moves
        bite = Move("Bite", "Dark", 50, 0.95, "Bites with sharp teeth")
        crunch = Move("Crunch", "Dark", 65, 0.85, "Crunches with sharp fangs")
        shadow_ball = Move("Shadow Ball", "Dark", 65, 0.85, "Hurls a shadowy blob")

        # Flying moves
        gust = Move("Gust", "Flying", 45, 0.95, "Creates a damaging gust")
        wing_attack = Move("Wing Attack", "Flying", 55, 0.9, "Strikes with wings")

        # Poison moves
        poison_sting = Move("Poison Sting", "Poison", 45, 0.95, "Stings with poison")
        sludge_bomb = Move("Sludge Bomb", "Poison", 65, 0.85, "Hurls filthy sludge")

        # Create starter monsters
        springraze = Monster(
            "Springraze", "Grass", 45, 45, 40, 60,
            [leaf_attack, tackle, vine_whip, seed_bomb],
            "A small, energetic grass-type monster with leaf-like appendages."
        )

        ignolf = Monster(
            "Ignolf", "Fire", 40, 55, 35, 55,
            [ember, scratch, fire_fang, flame_thrower],
            "A fiery wolf-like monster with flames around its body."
        )

        aquartle = Monster(
            "Aquartle", "Water", 50, 40, 50, 45,
            [water_gun, tackle, bubble_beam, hydro_pump],
            "A turtle-like water monster with a hard shell and water jets."
        )

        # Create additional monsters for encounters
        leaflet = Monster(
            "Leaflet", "Grass", 35, 30, 30, 40,
            [leaf_attack, tackle], 
            "A small leaf-like creature that flutters in the wind.",
            level=3
        )

        flamouse = Monster(
            "Flamouse", "Fire", 30, 40, 25, 45,
            [ember, scratch, fire_blast],  # Using fire_blast move to fix unused variable
            "A tiny mouse with a flame-tipped tail.",
            level=3
        )

        puddlet = Monster(
            "Puddlet", "Water", 40, 30, 35, 30,
            [water_gun, tackle],
            "A small puddle-like creature that can form a simple body.",
            level=3
        )

        buzzer = Monster(
            "Buzzer", "Electric", 35, 45, 30, 50,
            [spark, swift, thunder],  # Using thunder move to fix unused variable
            "A fast-moving insect-like monster that generates electricity.",
            level=4
        )

        rockling = Monster(
            "Rockling", "Rock", 50, 40, 60, 20,
            [tackle, body_slam, rock_throw, earthquake],  # Using earthquake move to fix unused variable
            "A small rock monster with stubby limbs.",
            level=4
        )

        floracat = Monster(
            "Floracat", "Grass", 45, 50, 40, 55,
            [vine_whip, scratch, leaf_storm],
            "A cat-like monster with flower petals around its neck.",
            level=7
        )

        whistleaf = Monster(
            "Whistleaf", "Grass", 40, 35, 45, 60,
            [leaf_attack, vine_whip, swift],
            "A musical plant monster that creates melodies with its leaves in the wind.",
            level=5
        )

        emberbear = Monster(
            "Emberbear", "Fire", 60, 55, 45, 40,
            [fire_fang, body_slam, flame_thrower],
            "A bear cub with ember-colored fur and fiery paws.",
            level=7
        )

        coralfish = Monster(
            "Coralfish", "Water", 50, 45, 55, 50,
            [bubble_beam, swift, surf],
            "A fish-like monster with coral-like growths on its body.",
            level=7
        )

        boltfox = Monster(
            "Boltfox", "Electric", 45, 50, 40, 60,
            [thunder_shock, scratch, thunderbolt],
            "A fox-like monster with static-charged fur.",
            level=8
        )

        rockbehemoth = Monster(
            "Rockbehemoth", "Rock", 70, 60, 75, 30,
            [body_slam, tackle, rock_slide],
            "A large rock monster with powerful arms.",
            level=10
        )

        # Adding new monster types with new type advantages
        frostbite = Monster(
            "Frostbite", "Ice", 45, 55, 50, 40,
            [ice_shard, tackle, ice_beam, blizzard],  # Using blizzard to fix unused variable
            "A small arctic fox with crystalline fur that sparkles with frost.",
            level=8
        )

        psyowl = Monster(
            "Psyowl", "Psychic", 40, 60, 40, 55,
            [psybeam, swift, psychic_blast, dream_eater],
            "A wise owl with glowing eyes that can see into your thoughts.",
            level=9
        )

        drakeling = Monster(
            "Drakeling", "Dragon", 55, 65, 55, 40,
            [dragon_rage, scratch, dragon_claw],
            "A small dragon with shimmering scales and growing wings.",
            level=12
        )

        shadowpaw = Monster(
            "Shadowpaw", "Dark", 50, 60, 45, 55,
            [bite, scratch, shadow_ball, crunch],  # Using crunch to fix unused variable
            "A mysterious cat-like creature that blends with shadows.",
            level=9
        )

        brawlcub = Monster(
            "Brawlcub", "Fighting", 60, 65, 40, 45,
            [karate_chop, tackle, brick_break],
            "A small bear cub that practices martial arts.",
            level=8
        )

        flutterwing = Monster(
            "Flutterwing", "Flying", 40, 45, 35, 70,
            [gust, swift, wing_attack],
            "A graceful bird-like creature with rainbow-colored wings.",
            level=7
        )

        toxifrog = Monster(
            "Toxifrog", "Poison", 50, 55, 40, 50,
            [poison_sting, water_gun, sludge_bomb, sand_tomb],  # Using sand_tomb to fix unused variable
            "A purple frog that secretes toxic slime from its skin.",
            level=8
        )

        fairybell = Monster(
            "Fairybell", "Fairy", 45, 50, 50, 45,
            [fairy_wind, swift, dazzling_gleam],
            "A small bell-shaped creature that emits a soothing chime.",
            level=9
        )

        # Create legendary monsters
        chronodrake = Monster(
            "Chronodrake", "Dragon", 95, 100, 90, 85,
            [dragon_claw, draco_meteor, time_warp, chronoblast],
            "An ancient dragon that has existed since the beginning of time. It can manipulate the flow of time itself.",
            level=40
        )

        celestius = Monster(
            "Celestius", "Fairy", 90, 95, 95, 85,
            [cosmic_power, celestial_beam, dazzling_gleam, psychic_blast],
            "A celestial monster that descended from the stars. Its body shimmers with cosmic energy.",
            level=40
        )

        pyrovern = Monster(
            "Pyrovern", "Fire", 95, 110, 80, 85,
            [inferno, magma_burst, flame_thrower, fire_blast],
            "A volcanic monster born from the heart of an ancient volcano. Its body burns with eternal flame.",
            level=40
        )

        gemdrill = Monster(
            "Gemdrill", "Rock", 105, 90, 110, 70,
            [rock_slide, diamond_drill, crystal_charge, earthquake],
            "A crystalline monster with a drill-like horn that can pierce any substance.",
            level=40
        )

        shadowclaw = Monster(
            "Shadowclaw", "Dark", 90, 105, 85, 95,
            [shadow_force, dark_void, shadow_ball, crunch],
            "A mysterious monster that dwells in darkness. It can merge with shadows and strike without warning.",
            level=40
        )

        # Additional legendary monsters for more variety
        tempestus = Monster(
            "Tempestus", "Electric", 85, 95, 80, 120,
            [thunder, thunderbolt, thunder_shock, swift],
            "A legendary storm spirit that rides the lightning. It appears during the fiercest thunderstorms.",
            level=45
        )

        terraquake = Monster(
            "Terraquake", "Ground", 110, 100, 95, 75,
            [earthquake, earth_power, rock_slide, body_slam],
            "A colossal earth elemental said to cause earthquakes when it stirs from its slumber.",
            level=45
        )

        luminary = Monster(
            "Luminary", "Psychic", 90, 115, 85, 90,
            [psychic_blast, cosmic_power, celestial_beam, time_warp],
            "A being of pure mental energy that illuminates the darkest minds with wisdom.",
            level=45
        )

        # New special type legendary monsters
        chronos = Monster(
            "Chronos", "Time", 100, 120, 90, 110,
            [time_warp, chronoblast, temporal_shift, time_stop],
            "The embodiment of time itself, capable of accelerating, slowing, or stopping time at will.",
            level=50
        )

        spatium = Monster(
            "Spatium", "Space", 100, 90, 120, 110,
            [dimensional_rift, gravity_crush, psychic_blast, shadow_force],
            "The embodiment of space, able to bend and fold dimensions as easily as paper.",
            level=50
        )

        cosmix = Monster(
            "Cosmix", "Cosmic", 110, 130, 90, 90,
            [celestial_beam, cosmic_power, star_burst, galaxy_spiral],
            "A being born from the coalescence of cosmic rays and stardust, containing the power of distant galaxies.",
            level=50
        )

        darkrai = Monster(
            "Darkrai", "Dread", 90, 130, 90, 110,
            [dark_void, shadow_force, nightmare_feast, terror_claw],
            "A creature that embodies the essence of nightmares and primal fear. It feeds on terror and despair.",
            level=50
        )

        vitalia = Monster(
            "Vitalia", "Life", 130, 90, 110, 90, 
            [vine_whip, seed_bomb, nature_bloom, life_force],
            "The embodiment of life energy, capable of accelerating growth and healing at a touch.",
            level=50
        )

        phantomos = Monster(
            "Phantomos", "Ghost", 90, 120, 90, 120,
            [shadow_ball, spectral_grasp, soul_steal, dark_void],
            "An ancient spirit that has existed for millennia, able to pass through solid matter and sap the life force of the living.",
            level=50
        )

        # The special dimension of hell legendary monster
        abaddon = Monster(
            "Abaddon", "Dread", 120, 150, 120, 90,
            [nightmare_feast, terror_claw, dark_void, inferno],
            "The lord of the abyss, ruler of the dimension of hell. It brings eternal torment to those who cross its path.",
            level=60
        )

        # Dual-type legendary monsters
        cosmicshade = Monster(
            "Cosmicshade", "Cosmic", 110, 140, 100, 100,
            [celestial_beam, cosmic_power, dark_void, star_burst],
            "A creature born from the darkness between stars. Its body absorbs light yet shines with cosmic radiance.",
            level=55
        )

        darkmatter = Monster(
            "Darkmatter", "Dark", 100, 140, 110, 100,
            [shadow_force, dark_void, cosmic_power, galaxy_spiral],
            "An entity composed of mysterious dark matter. It can manipulate gravity and consumes light.",
            level=55
        )

        lifedream = Monster(
            "Lifedream", "Life", 140, 90, 120, 100,
            [nature_bloom, life_force, seed_bomb, vine_whip],
            "A guardian of natural life, its body blooms with eternal flora. It nurtures all living things.",
            level=55
        )

        dreadspirit = Monster(
            "Dreadspirit", "Dread", 100, 140, 90, 120,
            [nightmare_feast, terror_claw, spectral_grasp, soul_steal],
            "A terrifying spectral entity that feeds on fear. Its mere presence causes nightmares.",
            level=55
        )

        # New elemental dimension legendaries
        infernus = Monster(
            "Infernus", "Fire", 120, 160, 100, 90,
            [inferno, magma_burst, fire_blast, flame_thrower],
            "The emperor of flames from the Molten Core dimension. Its body burns hotter than the core of a star.",
            level=60
        )

        aquabyss = Monster(
            "Aquabyss", "Water", 150, 100, 160, 80,
            [hydro_pump, surf, bubble_beam, ice_beam],
            "The sovereign of the Abyssal Depths dimension. Its body holds pressure that could crush mountains.",
            level=60
        )

        terravore = Monster(
            "Terravore", "Ground", 160, 130, 120, 60,
            [earthquake, earth_power, rock_slide, sand_tomb],
            "The ruler of the Crystal Caverns dimension. Its body is composed of living stone and precious gems.",
            level=60
        )

        stormrage = Monster(
            "Stormrage", "Electric", 130, 140, 90, 130,
            [thunder, thunderbolt, thunder_shock, spark],
            "The lord of the Tempest Realm dimension. Its body crackles with electrical currents that could power cities.",
            level=60
        )

        return {
            "Springraze": springraze,
            "Ignolf": ignolf,
            "Aquartle": aquartle,
            "Leaflet": leaflet,
            "Flamouse": flamouse,
            "Puddlet": puddlet,
            "Buzzer": buzzer,
            "Rockling": rockling,
            "Floracat": floracat,
            "Whistleaf": whistleaf,
            "Emberbear": emberbear,
            "Coralfish": coralfish,
            "Boltfox": boltfox,
            "Rockbehemoth": rockbehemoth,
            "Frostbite": frostbite,
            "Psyowl": psyowl,
            "Drakeling": drakeling,
            "Shadowpaw": shadowpaw,
            "Brawlcub": brawlcub,
            "Flutterwing": flutterwing,
            "Toxifrog": toxifrog,
            "Fairybell": fairybell,
            # Legendary monsters
            "Chronodrake": chronodrake,
            "Celestius": celestius,
            "Pyrovern": pyrovern,
            "Gemdrill": gemdrill,
            "Shadowclaw": shadowclaw,
            "Tempestus": tempestus,
            "Terraquake": terraquake,
            "Luminary": luminary,
            # New exclusive type legendaries
            "Chronos": chronos,
            "Spatium": spatium,
            "Cosmix": cosmix,
            "Darkrai": darkrai,
            "Vitalia": vitalia,
            "Phantomos": phantomos,
            "Abaddon": abaddon,
            # Dual-type legendaries
            "Cosmicshade": cosmicshade,
            "Darkmatter": darkmatter,
            "Lifedream": lifedream,
            "Dreadspirit": dreadspirit,
            # Elemental dimension legendaries
            "Infernus": infernus,
            "Aquabyss": aquabyss,
            "Terravore": terravore,
            "Stormrage": stormrage
        }

    def create_all_items(self) -> Dict[str, Item]:
        """Create all items for the game"""
        potion = Item("Potion", "Restores 20 HP to a monster", "heal", 20)
        super_potion = Item("Super Potion", "Restores 50 HP to a monster", "heal", 50)
        hyper_potion = Item("Hyper Potion", "Restores 100 HP to a monster", "heal", 100)
        revive = Item("Revive", "Revives a fainted monster with 50% HP", "revive", 50)
        monster_ball = Item("Monster Ball", "Used to catch wild monsters", "catch", 1)

        return {
            "Potion": potion,
            "Super Potion": super_potion,
            "Hyper Potion": hyper_potion,
            "Revive": revive,
            "Monster Ball": monster_ball
        }

    def get_wild_monster_for_location(self, location: str) -> Monster:
        """Get a random wild monster appropriate for the current location"""
        # Define monster pools by rarity
        common_monsters = ["Leaflet", "Flamouse", "Puddlet", "Buzzer", "Rockling", "Flutterwing", "Toxifrog", 
                           "Whistleaf", "Frostbite", "Shadowpaw", "Brawlcub", "Floracat", "Emberbear", "Coralfish"]

        uncommon_monsters = ["Floracat", "Emberbear", "Coralfish", "Boltfox", "Frostbite", "Shadowpaw", "Fairybell", "Brawlcub",
                             "Psyowl", "Rockbehemoth", "Drakeling"]

        # Define rare monsters that appear in special locations
        rare_monsters = ["Rockbehemoth", "Psyowl", "Drakeling", "Infernus", "Terravore", "Dreadspirit", "Aquabyss", 
                        "Stormrage", "Chronodrake", "Celestius", "Pyrovern", "Gemdrill", "Shadowclaw", "Tempestus", 
                        "Terraquake", "Luminary", "Chronos", "Spatium", "Cosmix", "Darkrai", "Vitalia", "Phantomos", 
                        "Abaddon", "Cosmicshade", "Darkmatter", "Lifedream"]

        # Define legendary monsters (extremely rare, only found in special puzzles/challenges)
        legendary_monsters = ["Chronodrake", "Celestius", "Pyrovern", "Gemdrill", "Shadowclaw", "Tempestus", 
                             "Terraquake", "Luminary", "Chronos", "Spatium", "Cosmix", "Shadowlord", "Vitalia", "Phantomos",
                             "Moltenking", "Prismatic", "Ancientone", "Deathwarden", "Oceanmaster", "Stormruler", 
                             "Sandstorm", "Frostlord", "Mechagon", "Worldtree", "Voidking", "Nebula"]



        # Create filtered lists for specific locations (only keeping the ones actually used)
        forest_rares = [m for m in rare_monsters if m in ["Rockbehemoth", "Drakeling"]]
        cave_rares = [m for m in rare_monsters if m in ["Rockbehemoth", "Psyowl"]]
        beach_rares = [m for m in rare_monsters if m in ["Rockbehemoth", "Abyssal"]]
        mountain_rares = [m for m in rare_monsters if m in ["Rockbehemoth", "Drakeling", "Tornadash"]]
        snow_rares = [m for m in rare_monsters if m in ["Drakeling", "Frostbite"]]
        ruins_rares = [m for m in rare_monsters if m in ["Drakeling", "Spectralord"]]

        location_monsters = {
            "Forest": (
                ["Leaflet", "Floracat", "Flutterwing", "Whistleaf"], 
                ["Flamouse", "Buzzer", "Shadowpaw", "Psyowl"], 
                forest_rares
            ),
            "Cave": (
                ["Rockling", "Buzzer", "Toxifrog", "Flamouse"], 
                ["Boltfox", "Shadowpaw", "Emberbear", "Floracat"], 
                cave_rares
            ),
            "Beach": (
                ["Puddlet", "Coralfish", "Flutterwing", "Toxifrog"], 
                ["Buzzer", "Rockling", "Fairybell", "Emberbear"], 
                beach_rares
            ),
            "Mountain": (
                ["Rockling", "Flamouse", "Frostbite", "Buzzer"], 
                ["Boltfox", "Floracat", "Brawlcub", "Shadowpaw"], 
                mountain_rares
            ),
            "Snowy Peaks": (
                ["Frostbite", "Flutterwing", "Rockling"], 
                ["Brawlcub", "Fairybell", "Metalbeak"], 
                snow_rares
            ),
            "Ancient Ruins": (
                ["Shadowpaw", "Toxifrog", "Psyowl"], 
                ["Psyowl", "Brawlcub", "Boltfox"], 
                ruins_rares
            ),
            "Hometown": (
                common_monsters[:4], uncommon_monsters[:4], []
            ),  # Limited selection in hometown

            # Amazing new locations with their unique monster pools!
            "Volcanic Crater": (
                ["Flamouse", "Rockling", "Buzzer", "Toxifrog"], 
                ["Emberbear", "Boltfox", "Floracat", "Shadowpaw"], 
                ["Rockbehemoth", "Psyowl", "Drakeling"]
            ),
            "Crystal Caverns": (
                ["Rockling", "Buzzer", "Leaflet", "Flamouse"], 
                ["Boltfox", "Floracat", "Emberbear", "Coralfish"], 
                ["Gemdrill", "Terravore", "Chronodrake"]
            ),
            "Mystic Temple": (
                ["Shadowpaw", "Toxifrog", "Buzzer", "Rockling"], 
                ["Psyowl", "Fairybell", "Boltfox", "Emberbear"], 
                ["Rockbehemoth", "Drakeling", "Psyowl"]  # Now includes existing rare monsters!
            ),
            "Haunted Graveyard": (
                ["Shadowpaw", "Toxifrog", "Buzzer", "Rockling"], 
                ["Psyowl", "Fairybell", "Boltfox", "Emberbear"], 
                ["Banshee", "Dreadspirit", "Voidreaper"]  # Now includes new rares Dreadspirit & Voidreaper!
            ),
            "Underwater City": (
                ["Puddlet", "Coralfish", "Toxifrog", "Buzzer"], 
                ["Boltfox", "Floracat", "Emberbear", "Shadowpaw"], 
                ["Leviathor", "Abyssal", "Aquabyss"]  # Now includes new rare Aquabyss!
            ),
            "Sky Islands": (
                ["Flutterwing", "Buzzer", "Leaflet", "Puddlet"], 
                ["Boltfox", "Floracat", "Emberbear", "Coralfish"], 
                ["Celestius", "Tempestus", "Stormrage"]
            ),
            "Desert Oasis": (
                ["Rockling", "Buzzer", "Flamouse", "Toxifrog"], 
                ["Boltfox", "Brawlcub", "Shadowpaw", "Frostbite"], 
                ["Rockbehemoth", "Psyowl", "Drakeling"]
            ),
            "Frozen Wasteland": (
                ["Frostbite", "Rockling", "Leaflet", "Puddlet"], 
                ["Fairybell", "Boltfox", "Shadowpaw", "Emberbear"], 
                ["Rockbehemoth", "Psyowl", "Drakeling"]
            ),
            "Neon City": (
                ["Buzzer", "Rockling", "Leaflet", "Puddlet"], 
                ["Boltfox", "Floracat", "Shadowpaw", "Metalbeak"], 
                ["Rockbehemoth", "Psyowl", "Drakeling"]
            ),
            "Enchanted Grove": (
                ["Leaflet", "Flutterwing", "Whistleaf", "Buzzer"], 
                ["Floracat", "Fairybell", "Psyowl", "Emberbear"], 
                ["Rockbehemoth", "Drakeling", "Psyowl"]  # Now includes existing rare monsters!
            ),
            "Shadow Realm": (
                ["Shadowpaw", "Toxifrog", "Buzzer", "Rockling"], 
                ["Psyowl", "Boltfox", "Floracat", "Emberbear"], 
                ["Shadowlord", "Drakeling", "Rockbehemoth"]  # Now includes existing rare monsters!
            ),
            "Celestial Observatory": (
                ["Starling", "Moonbeam", "Crystalwing", "Glowbug"], 
                ["Cosmicowl", "Thunderwing", "Mysticfox", "Stormbird"], 
                ["Starhawk", "Celestius", "Stormrage"]  # Now includes new rare Stormrage!
            )
        }

        # Default to Forest if location not found
        commons, uncommons, rares = location_monsters.get(location, location_monsters["Forest"])

        # Choose a monster based on rarity
        rarity_roll = random.random()

        # Extremely rare chance for legendaries (1% chance) in high-level areas
        if rarity_roll < 0.01 and self.player and self.player.trainer_level >= 30 and location in [
            "Volcanic Crater", "Crystal Caverns", "Mystic Temple", "Haunted Graveyard", 
            "Underwater City", "Sky Islands", "Desert Oasis", "Frozen Wasteland", 
            "Neon City", "Enchanted Grove", "Shadow Realm", "Celestial Observatory"
        ]:
            # Use the appropriate legendary list for special locations
            if location == "Volcanic Crater":
                monster_name = random.choice(["Moltenking", "Pyrovern", "Infernus"])
            elif location == "Crystal Caverns":
                monster_name = random.choice(["Prismatic", "Gemdrill", "Terravore"])
            elif location == "Mystic Temple":
                monster_name = random.choice(["Ancientone", "Luminary", "Templeguard"])
            elif location == "Haunted Graveyard":
                monster_name = random.choice(["Deathwarden", "Doomreaper", "Dreadspirit"])
            elif location == "Underwater City":
                monster_name = random.choice(["Oceanmaster", "Aquabyss", "Leviathor"])
            elif location == "Sky Islands":
                monster_name = random.choice(["Stormruler", "Tempestus", "Stormrage"])
            elif location == "Desert Oasis":
                monster_name = random.choice(["Sandstorm", "Mirageous", "Terraquake"])
            elif location == "Frozen Wasteland":
                monster_name = random.choice(["Frostlord", "Glacialtitan", "Blizzardclaw"])
            elif location == "Neon City":
                monster_name = random.choice(["Mechagon", "Cybernetic", "Technowolf"])
            elif location == "Enchanted Grove":
                monster_name = random.choice(["Worldtree", "Vitalia", "Naturelord"])
            elif location == "Shadow Realm":
                monster_name = random.choice(["Voidking", "Shadowlord", "Phantomos"])
            elif location == "Celestial Observatory":
                monster_name = random.choice(["Nebula", "Celestius", "Cosmix"])
            else:
                # Fall back to the general legendary pool
                monster_name = random.choice(legendary_monsters) if legendary_monsters else random.choice(uncommons)
        elif rarity_roll < 0.1 and rares:  # 10% chance for rare
            monster_name = random.choice(rares)
        elif rarity_roll < 0.4:  # 30% chance for uncommon
            monster_name = random.choice(uncommons)
        else:  # 60% chance for common
            monster_name = random.choice(commons)

        # Clone the template monster and set a reasonable level
        monster = self.all_monsters[monster_name].clone()

        # Level adjustment (higher levels in some areas)
        base_level = monster.level
        level_ranges = {
            "Hometown": (-1, 2),
            "Forest": (0, 3),
            "Cave": (2, 5),
            "Beach": (3, 6),
            "Mountain": (4, 8),
            "Snowy Peaks": (6, 10),
            "Ancient Ruins": (8, 12),
            "Volcanic Crater": (12, 18),
            "Crystal Caverns": (15, 22),
            "Mystic Temple": (18, 25),
            "Haunted Graveyard": (20, 28),
            "Underwater City": (22, 30),
            "Sky Islands": (25, 35),
            "Desert Oasis": (16, 24),
            "Frozen Wasteland": (28, 38),
            "Neon City": (30, 40),
            "Enchanted Grove": (32, 42),
            "Shadow Realm": (35, 45),
            "Celestial Observatory": (40, 50),
            "Dimension of Hell": (45, 60)
        }

        level_range = level_ranges.get(location, (0, 3))

        # Adjust level
        level_adjustment = random.randint(level_range[0], level_range[1])
        new_level = max(1, base_level + level_adjustment)

        # Set new level
        while monster.level < new_level:
            monster.level_up()

        # Chance to generate variant monsters
        # Different variants have different rarity
        variant_roll = random.random()

        # Special locations have higher chance for variants
        location_variant_bonus = {
            "Dimension of Hell": 0.15,       # Higher chance for variants in special dimensions
            "Molten Core": 0.15,
            "Abyssal Depths": 0.15,
            "Crystal Cavern": 0.15,         # Special dimension location gets higher bonus
            "Tempest Realm": 0.15,
            "Cosmic Void": 0.15,
            "Timeless Expanse": 0.15,
            "Spatial Rift": 0.15,
            "Eternal Garden": 0.15,
            "Ancient Ruins": 0.10,           # Higher chance in special locations
            "Shadow Peak": 0.10,
            "Snowy Peaks": 0.08,
            "Volcanic Ridge": 0.08,
            "Enchanted Grove": 0.08,
            "Ancient Labyrinth": 0.10,
            "Sky Tower": 0.08
        }

        # Base chance for variants is 3%
        variant_chance = 0.03 + location_variant_bonus.get(location, 0.0)

        # If we roll for a variant
        if variant_roll < variant_chance:
            # Determine which variant
            variant_type_roll = random.random()

            # Dominant is the rarest (5% of variants)
            if variant_type_roll < 0.05:
                monster.variant = "Dominant"
                monster.apply_variant_bonuses()
            # Omega is next rarest (10% of variants)
            elif variant_type_roll < 0.15:
                monster.variant = "Omega"
                monster.apply_variant_bonuses()
            # Crystal variants (20% of variants)
            elif variant_type_roll < 0.35:
                monster.variant = "Crystal"
                monster.apply_variant_bonuses()
            # Corrupted variants (25% of variants)
            elif variant_type_roll < 0.60:
                monster.variant = "Corrupted"
                monster.apply_variant_bonuses()
            # Alpha is most common (40% of variants)
            else:
                monster.variant = "Alpha"
                monster.apply_variant_bonuses()

        return monster

    def start_game(self):
        """Initialize and start the game"""
        # Show main menu first
        running = True

        while running:
            clear_screen()
            self.print_title()

            print(f"{Fore.CYAN}MAIN MENU{Style.RESET_ALL}\n")
            print("1. New Game")
            print("2. Load Game")
            print("3. Quit Game")

            choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): {Style.RESET_ALL}")

            if choice == "1":
                # Start new game
                self.start_new_game()
                running = False
            elif choice == "2":
                # Load game from slots
                load_result = self.show_load_game_menu()
                if load_result:
                    # Game was loaded and game loop started, so we can return here
                    return
                # If load_result is False, user chose to go back, so continue the main menu loop
            elif choice == "3":
                # Quit game
                print("\nThank you for playing World of Monsters!")
                self.running = False
                return
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")

    def start_new_game(self):
        """Start a new game"""
        clear_screen()
        self.print_title()

        # Get player name
        player_name = input(f"{Fore.CYAN}Please enter your name: {Style.RESET_ALL}")
        if not player_name:
            player_name = "Trainer"

        self.player = Player(player_name)

        # Choose starter monster
        starter_choice = self.choose_starter()
        if starter_choice == "1":
            self.player.add_monster(self.all_monsters["Springraze"].clone())
            print(f"\n{Fore.GREEN}You chose Springraze, the Grass-type monster!{Style.RESET_ALL}")
        elif starter_choice == "2":
            self.player.add_monster(self.all_monsters["Ignolf"].clone())
            print(f"\n{Fore.RED}You chose Ignolf, the Fire-type monster!{Style.RESET_ALL}")
        elif starter_choice == "3":
            self.player.add_monster(self.all_monsters["Aquartle"].clone())
            print(f"\n{Fore.BLUE}You chose Aquartle, the Water-type monster!{Style.RESET_ALL}")

        # Give starting items
        self.player.add_item(self.all_items["Potion"], 3)
        self.player.add_item(self.all_items["Monster Ball"], 5)

        print(f"\nWelcome to the World of Monsters, {player_name}!")
        print("Your journey begins in your Hometown. What awaits you in this world of wonderful creatures?")
        print("Type 'help' at any time to see available commands.")

        safe_input("\nPress Enter to continue...")

        # Main game loop
        self.game_loop()

    def get_save_slots(self):
        """Get save slot information"""
        # Define save slots
        save_slots = ["Slot 1", "Slot 2", "Slot 3"]

        # Check which slots have saved games
        saved_games = []
        if os.path.exists(SAVE_DIR):
            for filename in os.listdir(SAVE_DIR):
                if filename.endswith('.pickle') and filename != os.path.basename(CHAMPIONS_FILE):
                    try:
                        save_name = filename.replace('.pickle', '').split('_', 1)[1] if '_' in filename else filename.replace('.pickle', '')
                        saved_games.append(save_name)
                    except (pickle.PickleError, FileNotFoundError, OSError):
                        continue

        return save_slots, saved_games

    def show_save_game_menu(self):
        """Show save game menu with save slots"""
        # Get save slot information
        save_slots, saved_games = self.get_save_slots()

        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            attempts += 1
            try:
                clear_screen()
                self.print_title()

                print(f"{Fore.CYAN}SAVE GAME{Style.RESET_ALL}\n")

                # Display save slots
                for i, slot in enumerate(save_slots):
                    if slot in saved_games:
                        print(f"{i+1}. {slot} {Fore.YELLOW}[OVERWRITE]{Style.RESET_ALL}")
                    else:
                        print(f"{i+1}. {slot} {Fore.GREEN}[EMPTY]{Style.RESET_ALL}")

                print(f"\n4. {Fore.YELLOW}Back to Game{Style.RESET_ALL}")

                choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}").strip()

                if choice == "4":
                    return
                elif choice in ["1", "2", "3"]:
                    # Process save slot selection
                    slot_idx = int(choice) - 1
                    slot_name = save_slots[slot_idx]

                    if slot_name in saved_games:
                        confirm = input(f"{Fore.YELLOW}This slot already has a saved game. Overwrite? (y/n): {Style.RESET_ALL}").lower().strip()
                        if confirm != 'y':
                            continue

                    if self.save_game(slot_name):
                        safe_input("Press Enter to continue...")
                        return
                    else:
                        safe_input("Press Enter to continue...")
                        continue
                else:
                    print(f"{Fore.RED}Invalid choice. Please select 1-4.{Style.RESET_ALL}")
                    safe_input("Press Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Save cancelled.{Style.RESET_ALL}")
                return
            except Exception as e:
                print(f"{Fore.RED}Error in save menu: {e}{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")

        print(f"{Fore.RED}Too many attempts. Returning to game.{Style.RESET_ALL}")
        safe_input("Press Enter to continue...")

    def show_load_game_menu(self):
        """Show load game menu with save slots"""
        # Get save slot information
        save_slots, saved_games = self.get_save_slots()

        max_attempts = 10
        attempts = 0

        while attempts < max_attempts:
            attempts += 1
            try:
                clear_screen()
                self.print_title()

                print(f"{Fore.CYAN}LOAD GAME{Style.RESET_ALL}\n")

                # Display save slots
                for i, slot in enumerate(save_slots):
                    if slot in saved_games:
                        print(f"{i+1}. {slot} {Fore.GREEN}[SAVED GAME]{Style.RESET_ALL}")
                    else:
                        print(f"{i+1}. {slot} {Fore.RED}[EMPTY]{Style.RESET_ALL}")

                print(f"\n4. {Fore.YELLOW}Back to Game{Style.RESET_ALL}")

                choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}").strip()

                if choice == "4":
                    return False
                elif choice in ["1", "2", "3"]:
                    slot_idx = int(choice) - 1
                    save_name = save_slots[slot_idx]

                    if save_name in saved_games:
                        # Load the game
                        if self.load_game(save_name):
                            print(f"{Fore.GREEN}Game loaded successfully from {save_name}!{Style.RESET_ALL}")
                            safe_input("Press Enter to continue...")
                            # Start game loop immediately after loading
                            self.game_loop()
                            return True
                        else:
                            print(f"{Fore.RED}Failed to load game from {save_name}.{Style.RESET_ALL}")
                            safe_input("Press Enter to continue...")
                            continue
                    else:
                        print(f"{Fore.RED}No saved game found in {save_name}.{Style.RESET_ALL}")
                        safe_input("Press Enter to continue...")
                        continue
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter 1-4.{Style.RESET_ALL}")
                    safe_input("Press Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Load cancelled.{Style.RESET_ALL}")
                return False
            except Exception as e:
                print(f"{Fore.RED}Error in load menu: {e}{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")

        print(f"{Fore.RED}Too many attempts. Returning to main menu.{Style.RESET_ALL}")
        safe_input("Press Enter to continue...")
        return False

    def print_title(self):
        """Print game title screen"""
        title = f"""
{Fore.CYAN}======================================{Style.RESET_ALL}
{Fore.YELLOW}       WORLD OF MONSTERS{Style.RESET_ALL}
{Fore.CYAN}======================================{Style.RESET_ALL}

{Fore.GREEN}A Pokémon-inspired Text Adventure{Style.RESET_ALL}

Catch, train, and battle with 
your monster companions!

{Fore.CYAN}======================================{Style.RESET_ALL}
"""
        print(title)

    def choose_starter(self) -> str:
        """Let the player choose a starter monster"""
        valid_choice = False
        choice = ""

        while not valid_choice:
            clear_screen()
            self.print_title()
            print(f"{Fore.CYAN}Professor Pino:{Style.RESET_ALL} Welcome to the world of monsters!")
            print("It's time to choose your first monster companion for your journey.")
            print("\nYou have three choices:")

            print(f"\n{Fore.GREEN}1. Springraze (Grass-type){Style.RESET_ALL}")
            print("   A small, energetic grass-type monster with leaf-like appendages.")
            print("   Moves: Leaf Attack, Tackle, Vine Whip, Seed Bomb")

            print(f"\n{Fore.RED}2. Ignolf (Fire-type){Style.RESET_ALL}")
            print("   A fiery wolf-like monster with flames around its body.")
            print("   Moves: Ember, Scratch, Fire Fang, Flame Thrower")

            print(f"\n{Fore.BLUE}3. Aquartle (Water-type){Style.RESET_ALL}")
            print("   A turtle-like water monster with a hard shell and water jets.")
            print("   Moves: Water Gun, Tackle, Bubble Beam, Hydro Pump")

            choice = input(f"\n{Fore.CYAN}Enter your choice (1-3): {Style.RESET_ALL}")

            if choice in ["1", "2", "3"]:
                valid_choice = True
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
                safe_input("Press Enter to try again...")

        return choice

    def game_loop(self):
        """Main game loop"""
        try:
            while self.running:
                # Handle turns and random encounters
                self.turn_count += 1

                if not self.current_battle:
                    # Check for random encounter (if not in hometown)
                    if (self.player and self.player.location != "Hometown" and 
                        random.random() < WILD_ENCOUNTER_RATE and 
                        self.player.has_usable_monster()):
                        wild_monster = self.get_wild_monster_for_location(self.player.location)
                        self.start_battle(wild_monster)
                        continue  # Skip to next iteration to handle battle

                # Show game state
                clear_screen()
                self.display_game_state()

                # Get and process player command with error handling
                try:
                    command = input(f"\n{Fore.CYAN}What will you do? {Style.RESET_ALL}").strip().lower()
                    if command:  # Only process if command is not empty
                        self.process_command(command)
                    else:
                        print("Please enter a command. Type 'help' for available commands.")
                        time.sleep(1)
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{Fore.YELLOW}Game interrupted. Exiting...{Style.RESET_ALL}")
                    self.running = False
                    break
                except Exception as e:
                    print(f"\n{Fore.RED}Error processing command: {e}{Style.RESET_ALL}")
                    time.sleep(1)
        except Exception as e:
            print(f"\n{Fore.RED}Game loop error: {e}{Style.RESET_ALL}")
            self.running = False

    def display_game_state(self):
        """Display the current game state to the player"""
        player = self.player

        # Check if player exists
        if not player:
            print(f"{Fore.RED}No active player. Please start a new game or load a saved game.{Style.RESET_ALL}")
            return

        # If in battle, show battle state
        if self.current_battle:
            self.display_battle_state()
            return

        # Show location and basic player info
        print(f"{Fore.YELLOW}Location: {player.location}{Style.RESET_ALL}")
        print(f"Trainer: {player.name}")
        print(f"Trainer Level: {player.trainer_level} (Monster Level Cap: {player.trainer_level * 2})")
        print(f"Money: ${player.money}")

        # Show active monster
        if player.active_monster:
            print(f"\n{Fore.CYAN}Active Monster:{Style.RESET_ALL}")
            print(player.active_monster)

        # Show brief command help
        print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
        print("- explore: Explore the current location")
        print("- travel: Travel to a different location")
        print("- monsters: View your monsters")
        print("- items: View your inventory")
        print("- heal: Rest and heal your monsters (only in Hometown)")
        print("- help: Show detailed help")

    def display_battle_state(self):
        """Display the current battle state"""
        battle = self.current_battle
        if not battle or not self.player:
            print(f"{Fore.RED}No active battle.{Style.RESET_ALL}")
            return

        player_monster = self.player.active_monster
        wild_monster = battle.wild_monster

        if not player_monster or not wild_monster:
            print(f"{Fore.RED}Battle state is invalid.{Style.RESET_ALL}")
            return

        print(f"{Fore.RED}=== BATTLE ==={Style.RESET_ALL}")
        print(f"Wild {wild_monster}")
        print("\nVS\n")
        print(f"Your {player_monster}")

        print(f"\n{Fore.CYAN}Battle Commands:{Style.RESET_ALL}")
        print("- fight <number>: Use a move to attack")
        if hasattr(player_monster, 'moves') and player_monster.moves:
            for i, move in enumerate(player_monster.moves):
                print(f"  {i+1}. {move}")
        else:
            print("  No moves available")

        print("- catch: Try to catch the wild monster")
        print("- switch <number>: Switch to another monster")
        print("- item <number>: Use an item")
        print("- run: Try to run away from battle")

    def save_game(self, save_name: Optional[str] = None) -> bool:
        """Simple and reliable save system"""
        if not self.player:
            print(f"{Fore.RED}No player data to save.{Style.RESET_ALL}")
            return False

        # Prompt for save name if not provided
        if not save_name:
            save_name = input(f"{Fore.CYAN}Enter save name (or press Enter for default): {Style.RESET_ALL}").strip()
            if not save_name:
                save_name = f"{self.player.name}_save"

        try:
            # Create basic save data
            save_data = {
                "name": self.player.name,
                "location": self.player.location,
                "money": self.player.money,
                "monsters": self.player.monsters,
                "inventory": self.player.inventory,
                "active_monster_index": self.player.active_monster_index,
                "trainer_level": getattr(self.player, 'trainer_level', 5),
                "exp": getattr(self.player, 'exp', 0),
                "tokens": getattr(self.player, 'tokens', 500),
                "equipment": getattr(self.player, 'equipment', {}),
                "materials": getattr(self.player, 'materials', {}),
                "visited_areas": getattr(self.player, 'visited_areas', {'Forest Grove'}),
                "daily_tasks": getattr(self.player, 'daily_tasks', {}),
                "character_opinions": getattr(self.player, 'character_opinions', {}),
                "dialogue_history": getattr(self.player, 'dialogue_history', {}),
                "story_moments": getattr(self.player, 'story_moments', []),
                "moral_choices": getattr(self.player, 'moral_choices', []),
                "reflection_points": getattr(self.player, 'reflection_points', 0),
                "game_version": "3.0",
                "save_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save to file
            save_path = get_save_path(self.player.name, save_name)
            with open(save_path, 'wb') as f:
                pickle.dump(save_data, f)

            print(f"{Fore.GREEN}Game saved successfully as '{save_name}'!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Level {save_data['trainer_level']} trainer with {len(save_data['monsters'])} monsters{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"{Fore.RED}Error saving game: {e}{Style.RESET_ALL}")
            return False

    def _get_monster_type_stats(self) -> Dict[str, int]:
        """Get statistics of monsters by type"""
        if not self.player or not self.player.monsters:
            return {}

        type_stats = {}
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'type'):
                monster_type = monster.type
                type_stats[monster_type] = type_stats.get(monster_type, 0) + 1
        return type_stats

    def _get_highest_monster_level(self) -> int:
        """Get the level of the highest level monster"""
        if not self.player or not self.player.monsters:
            return 0

        max_level = 0
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'level'):
                max_level = max(max_level, monster.level)
        return max_level

    def _count_fusion_monsters(self) -> int:
        """Count how many fusion monsters the player has"""
        if not self.player or not self.player.monsters:
            return 0

        fusion_count = 0
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'is_fusion') and monster.is_fusion:
                fusion_count += 1
        return fusion_count

    def _get_visited_locations(self) -> List[str]:
        """Get list of locations the player has visited"""
        visited = [self.player.location] if self.player and hasattr(self.player, 'location') else []

        # Add locations from story progress
        if self.player and hasattr(self.player, 'story_progress'):
            for event_id in self.player.story_progress.keys():
                if '_' in event_id:
                    location = event_id.split('_')[0].replace('_', ' ').title()
                    if location not in visited:
                        visited.append(location)

        return visited

    def _get_player_achievements(self) -> List[str]:
        """Generate list of player achievements based on progress"""
        achievements = []

        if not self.player:
            return achievements

        # Monster collection achievements
        monster_count = len(self.player.monsters) if self.player.monsters else 0
        if monster_count >= 10:
            achievements.append("Monster Collector - Caught 10 monsters")
        if monster_count >= 25:
            achievements.append("Monster Master - Caught 25 monsters")
        if monster_count >= 50:
            achievements.append("Monster Legend - Caught 50 monsters")

        # Fusion achievements
        fusion_count = self._count_fusion_monsters()
        if fusion_count >= 1:
            achievements.append("Fusion Pioneer - Created first fusion monster")
        if fusion_count >= 5:
            achievements.append("Fusion Expert - Created 5 fusion monsters")

        # Story achievements
        if hasattr(self.player, 'story_progress') and self.player.story_progress:
            story_events = len(self.player.story_progress)
            if story_events >= 5:
                achievements.append("Story Explorer - Completed 5 story events")
            if story_events >= 15:
                achievements.append("Epic Adventurer - Completed 15 story events")

        # Trainer level achievements
        trainer_level = getattr(self.player, 'trainer_level', 5)
        if trainer_level >= 10:
            achievements.append("Experienced Trainer - Reached level 10")
        if trainer_level >= 25:
            achievements.append("Master Trainer - Reached level 25")
        if trainer_level >= 50:
            achievements.append("Legendary Trainer - Reached level 50")

        # Quest completion achievements
        if hasattr(self.player, 'quest_items') and self.player.quest_items:
            quest_items = len(self.player.quest_items)
            if quest_items >= 1:
                achievements.append("Quest Seeker - Found first quest item")
            if "Forest Crystal" in self.player.quest_items:
                achievements.append("Forest Guardian - Obtained Forest Crystal")
            if all(crystal in self.player.quest_items for crystal in ["Forest Crystal", "Fire Crystal", "Water Crystal", "Earth Crystal"]):
                achievements.append("Crystal Collector - Gathered all elemental crystals")

        return achievements

    def _get_monster_rarity_stats(self) -> Dict[str, int]:
        """Get statistics of monsters by rarity"""
        if not self.player or not self.player.monsters:
            return {}

        rarity_stats = {}
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'rarity'):
                rarity = monster.rarity
                rarity_stats[rarity] = rarity_stats.get(rarity, 0) + 1
            elif monster:
                # Default rarity if not specified
                rarity_stats['common'] = rarity_stats.get('common', 0) + 1
        return rarity_stats

    def _count_shiny_monsters(self) -> int:
        """Count how many shiny monsters the player has"""
        if not self.player or not self.player.monsters:
            return 0

        shiny_count = 0
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'is_shiny') and monster.is_shiny:
                shiny_count += 1
            elif monster and hasattr(monster, 'variant') and 'shiny' in str(monster.variant).lower():
                shiny_count += 1
        return shiny_count

    def _count_legendary_monsters(self) -> int:
        """Count how many legendary monsters the player has"""
        if not self.player or not self.player.monsters:
            return 0

        legendary_count = 0
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'rarity') and monster.rarity.lower() == 'legendary':
                legendary_count += 1
            elif monster and hasattr(monster, 'name') and monster.name in ['Shadowmaw', 'Voidwyrm', 'Chronodrake', 'Starstorm', 'Doomreaper']:
                legendary_count += 1
        return legendary_count

    def _calculate_exploration_percentage(self) -> float:
        """Calculate the percentage of the world explored"""
        if not self.player:
            return 0.0

        # Total possible locations in the game
        total_locations = 15  # Based on the locations we have
        visited_locations = self._get_visited_locations()

        if not visited_locations or len(visited_locations) == 0:
            return 0.0

        exploration_percentage = (len(visited_locations) / total_locations) * 100
        return min(exploration_percentage, 100.0)  # Cap at 100%

    def _get_variant_stats(self) -> Dict[str, int]:
        """Get statistics of monster variants caught"""
        if not self.player or not self.player.monsters:
            return {}

        variant_stats = {}
        for monster in self.player.monsters:
            if monster and hasattr(monster, 'variant') and monster.variant:
                variant = monster.variant
                variant_stats[variant] = variant_stats.get(variant, 0) + 1
        return variant_stats

    def old_save_file_recovery_wizard(self, save_path: str) -> dict:
        """Advanced Save File Recovery Wizard with user-friendly options"""

        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                    SAVE FILE RECOVERY WIZARD                     ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}Save file appears to be corrupted or damaged.{Style.RESET_ALL}")
        print(f"File: {save_path}\n")

        # Analyze the file to determine corruption type
        corruption_type, analysis = self.analyze_save_corruption(save_path)

        print(f"{Fore.CYAN}Analysis Results:{Style.RESET_ALL}")
        print(f"Corruption Type: {corruption_type}")
        print(f"Details: {analysis}\n")

        # Show recovery options
        print(f"{Fore.GREEN}Recovery Options:{Style.RESET_ALL}")
        print("1. Auto-Repair (Recommended) - Attempt automatic recovery")
        print("2. Manual Recovery - Choose specific recovery method")
        print("3. Restore from Backup - Use previous backup if available")
        print("4. Create Fresh Save - Start with minimal recovered data")
        print("5. Skip Recovery - Continue without loading this save")

        while True:
            choice = input(f"\n{Fore.CYAN}Select recovery option (1-5): {Style.RESET_ALL}").strip()

            if choice == "1":
                return self.auto_repair_save(save_path, corruption_type)
            elif choice == "2":
                return self.manual_recovery_menu(save_path, corruption_type)
            elif choice == "3":
                return self.restore_from_backup(save_path)
            elif choice == "4":
                return self.create_recovery_save(save_path)
            elif choice == "5":
                return self.create_emergency_save()
            else:
                print(f"{Fore.RED}Invalid option. Please choose 1-5.{Style.RESET_ALL}")

    def analyze_save_corruption(self, save_path: str) -> tuple:
        """Analyze save file to determine corruption type and details"""
        try:
            with open(save_path, 'rb') as f:
                raw_data = f.read()

            if len(raw_data) == 0:
                return "Empty File", "Save file contains no data"

            # Try to determine file format
            try:
                with open(save_path, 'r') as f:
                    text_data = f.read()

                if text_data.strip().startswith('{') and text_data.strip().endswith('}'):
                    return "JSON Format", "Appears to be JSON but may have syntax errors"
                elif text_data.strip().startswith('{'):
                    return "Incomplete JSON", "JSON file missing closing bracket"
                elif text_data.strip().endswith('}'):
                    return "Truncated JSON", "JSON file missing opening bracket"
                else:
                    return "Unknown Text Format", "Text file with unknown format"
            except UnicodeDecodeError:
                return "Binary Format", "Appears to be pickle or other binary format"

        except FileNotFoundError:
            return "Missing File", "Save file does not exist"
        except PermissionError:
            return "Access Denied", "Cannot read save file due to permissions"
        except Exception as e:
            return "Unknown Error", f"Unexpected error: {str(e)}"

    def auto_repair_save(self, save_path: str, corruption_type: str) -> dict:
        """Automatic repair with progress feedback"""
        import json as json_module

        print(f"\n{Fore.CYAN}Starting automatic repair...{Style.RESET_ALL}")

        # Step 1: Try JSON repair
        print("Step 1: Attempting JSON repair...")
        try:
            with open(save_path, 'r') as f:
                content = f.read()

            # Advanced JSON repair techniques
            content = content.strip()

            # Fix common JSON issues
            if not content.startswith('{'):
                content = '{' + content
            if not content.endswith('}'):
                content += '}'

            # Fix common escape issues
            content = content.replace('\\"', '"').replace('\\\\', '\\')

            # Try to parse
            save_data = json_module.loads(content)
            print(f"{Fore.GREEN}✓ JSON repair successful!{Style.RESET_ALL}")

            # Create backup and save repaired version
            self.create_backup(save_path)
            with open(save_path, 'w') as f:
                json_module.dump(save_data, f, indent=2)

            return save_data

        except json_module.JSONDecodeError:
            print(f"{Fore.YELLOW}✗ JSON repair failed{Style.RESET_ALL}")

        # Step 2: Try pickle format
        print("Step 2: Attempting pickle format recovery...")
        try:
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)
            print(f"{Fore.GREEN}✓ Pickle format recovery successful!{Style.RESET_ALL}")

            # Convert to JSON
            json_path = save_path.replace('.pickle', '.json')
            with open(json_path, 'w') as f:
                json_module.dump(save_data, f, indent=2)

            return save_data

        except (pickle.PickleError, FileNotFoundError, OSError):
            print(f"{Fore.YELLOW}✗ Pickle recovery failed{Style.RESET_ALL}")

        # Step 3: Create emergency recovery save
        print("Step 3: Creating emergency recovery save...")
        return self.create_emergency_save()

    def manual_recovery_menu(self, save_path: str, corruption_type: str) -> dict:
        """Manual recovery options menu"""
        clear_screen()
        print(f"{Fore.CYAN}Manual Recovery Options{Style.RESET_ALL}\n")

        print("1. JSON Syntax Repair - Fix brackets, quotes, and commas")
        print("2. Pickle to JSON Conversion - Convert old pickle format")
        print("3. Data Extraction - Extract readable data from corrupted file")
        print("4. Template Reconstruction - Rebuild save using template")
        print("5. Back to main recovery menu")

        while True:
            choice = input(f"\n{Fore.CYAN}Select recovery method (1-5): {Style.RESET_ALL}").strip()

            if choice == "1":
                return self.repair_json_syntax(save_path)
            elif choice == "2":
                return self.convert_pickle_to_json(save_path)
            elif choice == "3":
                return self.extract_save_data(save_path)
            elif choice == "4":
                return self.reconstruct_from_template(save_path)
            elif choice == "5":
                return self.create_emergency_save()
            else:
                print(f"{Fore.RED}Invalid option. Please choose 1-5.{Style.RESET_ALL}")

    def create_backup(self, save_path: str):
        """Create backup of original corrupted file"""
        try:
            backup_path = save_path + f".backup_{int(time.time())}"
            with open(save_path, 'rb') as original:
                with open(backup_path, 'wb') as backup:
                    backup.write(original.read())
            print(f"{Fore.GREEN}Backup created: {backup_path}{Style.RESET_ALL}")
        except (OSError, IOError, FileNotFoundError, PermissionError) as e:
            print(f"{Fore.YELLOW}Warning: Could not create backup: {e}{Style.RESET_ALL}")

    def restore_from_backup(self, save_path: str) -> dict:
        """Restore from available backups"""
        save_dir = os.path.dirname(save_path)
        base_name = os.path.basename(save_path)

        # Find backup files
        backups = []
        if os.path.exists(save_dir):
            for filename in os.listdir(save_dir):
                if filename.startswith(base_name + ".backup_"):
                    backup_path = os.path.join(save_dir, filename)
                    timestamp = filename.split("backup_")[1]
                    backups.append((backup_path, timestamp))

        if not backups:
            print(f"{Fore.YELLOW}No backup files found.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return self.create_emergency_save()

        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)

        print(f"\n{Fore.CYAN}Available Backups:{Style.RESET_ALL}")
        for i, (path, timestamp) in enumerate(backups[:5]):  # Show max 5 backups
            date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
            print(f"{i+1}. Backup from {date_str}")

        while True:
            choice = input(f"\n{Fore.CYAN}Select backup to restore (1-{len(backups[:5])} or 0 to cancel): {Style.RESET_ALL}").strip()

            try:
                if choice == "0":
                    return self.create_emergency_save()

                backup_index = int(choice) - 1
                if 0 <= backup_index < len(backups[:5]):
                    return self.simple_load_save(backups[backup_index][0])
                else:
                    print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    def create_recovery_save(self, save_path: str) -> dict:
        """Create a fresh save with recovered data where possible"""
        print(f"\n{Fore.CYAN}Creating recovery save...{Style.RESET_ALL}")

        recovery_data = {
            "player_name": "Recovered Player",
            "trainer_level": 5,
            "location": "Hometown",
            "money": 500,
            "monsters": [],
            "inventory": {"Healing Potion": 3, "Monster Ball": 5},
            "save_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "recovery_note": "This save was created by the recovery wizard"
        }

        # Try to extract any readable data from corrupted file
        try:
            extracted_data = self.extract_readable_data(save_path)
            if extracted_data:
                recovery_data.update(extracted_data)
                print(f"{Fore.GREEN}Some data recovered from corrupted file.{Style.RESET_ALL}")
        except Exception:
            pass

        print(f"{Fore.GREEN}Recovery save created successfully!{Style.RESET_ALL}")
        safe_input("Press Enter to continue...")
        return recovery_data

    def create_emergency_save(self) -> dict:
        """Create minimal emergency save data"""
        return {
            "player_name": "Emergency Recovery",
            "trainer_level": 1,
            "location": "Hometown",
            "money": 100,
            "monsters": [],
            "inventory": {"Healing Potion": 1},
            "save_time": "Emergency Recovery",
            "emergency_recovery": True
        }

    def simple_load_save(self, save_path: str) -> dict:
        """Simple save loading without complex recovery"""
        try:
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)
                return save_data
        except Exception as e:
            print(f"{Fore.RED}Error loading save file: {e}{Style.RESET_ALL}")
            return {}

    def repair_json_syntax(self, save_path: str) -> dict:
        """Advanced JSON syntax repair with detailed error handling"""
        import json as json_module
        import re

        print(f"\n{Fore.CYAN}JSON Syntax Repair in progress...{Style.RESET_ALL}")

        try:
            with open(save_path, 'r') as f:
                content = f.read()

            original_content = content
            print(f"Original file size: {len(content)} characters")

            # Step 1: Basic cleanup
            content = content.strip()

            # Step 2: Fix bracket issues
            if not content.startswith('{'):
                content = '{' + content
                print("✓ Added missing opening bracket")

            if not content.endswith('}'):
                content += '}'
                print("✓ Added missing closing bracket")

            # Step 3: Fix common JSON issues
            fixes_applied = []

            # Fix trailing commas
            content = re.sub(r',(\s*[}\]])', r'\1', content)
            if content != original_content:
                fixes_applied.append("Removed trailing commas")

            # Fix unescaped quotes
            content = re.sub(r'(?<!\\)"(?=[^,}\]:\s])', r'\\"', content)

            # Fix missing quotes around keys
            content = re.sub(r'(\w+)(\s*:)', r'"\1"\2', content)

            # Step 4: Try to parse
            try:
                save_data = json_module.loads(content)
                print(f"{Fore.GREEN}✓ JSON syntax repair successful!{Style.RESET_ALL}")

                if fixes_applied:
                    print(f"Fixes applied: {', '.join(fixes_applied)}")

                # Create backup and save
                self.create_backup(save_path)
                with open(save_path, 'w') as f:
                    json_module.dump(save_data, f, indent=2)

                safe_input("Press Enter to continue...")
                return save_data

            except json_module.JSONDecodeError as e:
                print(f"{Fore.RED}JSON syntax repair failed: {str(e)}{Style.RESET_ALL}")
                print("Falling back to emergency recovery...")
                safe_input("Press Enter to continue...")
                return self.create_emergency_save()

        except Exception as e:
            print(f"{Fore.RED}Error during JSON repair: {str(e)}{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return self.create_emergency_save()

    def convert_pickle_to_json(self, save_path: str) -> dict:
        """Convert pickle format saves to JSON"""

        print(f"\n{Fore.CYAN}Converting pickle to JSON format...{Style.RESET_ALL}")

        try:
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)

            print(f"{Fore.GREEN}✓ Pickle file loaded successfully{Style.RESET_ALL}")
            print(f"Data keys found: {list(save_data.keys()) if isinstance(save_data, dict) else 'Non-dict data'}")

            print(f"{Fore.GREEN}✓ Pickle file loaded and verified successfully{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return save_data

        except Exception as e:
            print(f"{Fore.RED}Pickle conversion failed: {str(e)}{Style.RESET_ALL}")
            print("The file may not be in pickle format or may be corrupted.")
            safe_input("Press Enter to continue...")
            return self.create_emergency_save()

    def extract_save_data(self, save_path: str) -> dict:
        """Extract readable data from corrupted files"""
        import re
        print(f"\n{Fore.CYAN}Extracting readable data...{Style.RESET_ALL}")

        extracted_data = {
            "player_name": "Data Recovery",
            "trainer_level": 1,
            "location": "Hometown",
            "money": 100,
            "monsters": [],
            "inventory": {},
            "save_time": "Data Extraction"
        }

        try:
            with open(save_path, 'r', errors='ignore') as f:
                content = f.read()

            # Extract player name
            name_match = re.search(r'"?player_name"?\s*:\s*"([^"]+)"', content)
            if name_match:
                extracted_data["player_name"] = name_match.group(1)
                print(f"✓ Extracted player name: {name_match.group(1)}")

            # Extract trainer level
            level_match = re.search(r'"?trainer_level"?\s*:\s*(\d+)', content)
            if level_match:
                extracted_data["trainer_level"] = int(level_match.group(1))
                print(f"✓ Extracted trainer level: {level_match.group(1)}")

            # Extract location
            location_match = re.search(r'"?location"?\s*:\s*"([^"]+)"', content)
            if location_match:
                extracted_data["location"] = location_match.group(1)
                print(f"✓ Extracted location: {location_match.group(1)}")

            # Extract money
            money_match = re.search(r'"?money"?\s*:\s*(\d+)', content)
            if money_match:
                extracted_data["money"] = int(money_match.group(1))
                print(f"✓ Extracted money: ${money_match.group(1)}")

            print(f"{Fore.GREEN}Data extraction completed!{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.YELLOW}Extraction encountered errors: {str(e)}{Style.RESET_ALL}")
            print("Using minimal recovery data.")

        safe_input("Press Enter to continue...")
        return extracted_data

    def reconstruct_from_template(self, save_path: str) -> dict:
        """Reconstruct save using template and extracted data"""
        print(f"\n{Fore.CYAN}Reconstructing save from template...{Style.RESET_ALL}")

        # Create comprehensive template
        template_data = {
            "player_name": "Template Recovery",
            "trainer_level": 5,
            "location": "Hometown",
            "money": 500,
            "monsters": [],
            "inventory": {
                "Healing Potion": 5,
                "Monster Ball": 10,
                "Super Potion": 2
            },
            "active_monster_index": 0,
            "exp": 0,
            "exp_to_level": 100,
            "tokens": 500,
            "story_progress": {},
            "quest_items": [],
            "completed_quests": [],
            "active_quests": [],
            "equipment": {},
            "skills": {},
            "materials": {
                'Monster Essence': 0,
                'Crystal Shards': 0,
                'Metal Ore': 0,
                'Ancient Bones': 0,
                'Mystic Herbs': 0
            },
            "guild": None,
            "guild_rank": 'Member',
            "guild_contribution": 0,
            "visited_areas": ['Forest Grove'],
            "battle_wins": 0,
            "battle_losses": 0,
            "playtime": 0,
            "daily_tasks": {
                'catch_monsters': {'progress': 0, 'target': 3, 'completed': False},
                'win_battles': {'progress': 0, 'target': 5, 'completed': False},
                'explore_areas': {'progress': 0, 'target': 2, 'completed': False},
                'use_items': {'progress': 0, 'target': 4, 'completed': False}
            },
            "save_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "template_reconstruction": True
        }

        # Try to merge with extracted data
        try:
            extracted_data = self.extract_readable_data(save_path)
            template_data.update(extracted_data)
            print(f"{Fore.GREEN}✓ Template merged with extracted data{Style.RESET_ALL}")
        except Exception:
            print(f"{Fore.YELLOW}Using pure template data{Style.RESET_ALL}")

        # Give player a starter monster
        try:
            all_monsters = self.create_all_monsters()
            if "Springraze" in all_monsters:
                starter = all_monsters["Springraze"].clone()
                template_data["monsters"] = [starter]
                print("✓ Added starter monster: Springraze")
        except Exception:
            print(f"{Fore.YELLOW}Could not add starter monster{Style.RESET_ALL}")

        print(f"{Fore.GREEN}Template reconstruction completed!{Style.RESET_ALL}")
        safe_input("Press Enter to continue...")
        return template_data

    def extract_readable_data(self, save_path: str) -> dict:
        """Helper function to extract any readable data from corrupted file"""
        import re
        try:
            # Try multiple approaches to extract data
            extracted = {}

            # Approach 1: Try as text file
            with open(save_path, 'r', errors='ignore') as f:
                content = f.read()

                # Use regex to find key-value pairs
                patterns = {
                    'player_name': r'"?player_name"?\s*:\s*"([^"]+)"',
                    'trainer_level': r'"?trainer_level"?\s*:\s*(\d+)',
                    'location': r'"?location"?\s*:\s*"([^"]+)"',
                    'money': r'"?money"?\s*:\s*(\d+)'
                }

                for key, pattern in patterns.items():
                    match = re.search(pattern, content)
                    if match:
                        value = match.group(1)
                        if key in ['trainer_level', 'money']:
                            extracted[key] = int(value)
                        else:
                            extracted[key] = value

            return extracted

        except (FileNotFoundError, IOError, OSError, UnicodeDecodeError, re.error) as e:
            print(f"{Fore.YELLOW}Extraction encountered errors: {str(e)}{Style.RESET_ALL}")
            print("Using minimal recovery data.")
            return {}

    def recovery_wizard_menu(self):
        """Access the Save File Recovery Wizard from the main menu"""
        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                    SAVE FILE RECOVERY WIZARD                     ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}This tool helps recover corrupted or damaged save files.{Style.RESET_ALL}")
        print(f"Please select the save file you'd like to recover:\n")

        # Get list of save files
        if not self.db_available:
            print(f"{Fore.RED}Save system is not available.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        save_slots = self.get_save_slots()

        print(f"{Fore.GREEN}Available save files:{Style.RESET_ALL}")
        for i, slot_info in enumerate(save_slots, 1):
            status = slot_info['status']
            name = slot_info['name']
            time_info = slot_info['time']

            if status == "Empty":
                print(f"{i}. {Fore.LIGHTBLACK_EX}Empty Slot{Style.RESET_ALL}")
            else:
                print(f"{i}. {name} - {time_info}")

        print(f"{len(save_slots) + 1}. Enter custom file path")
        print(f"{len(save_slots) + 2}. Back to main menu")

        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Select save file to recover (1-{len(save_slots) + 2}): {Style.RESET_ALL}").strip()

                if choice == str(len(save_slots) + 2):
                    return
                elif choice == str(len(save_slots) + 1):
                    # Custom file path
                    file_path = input(f"{Fore.CYAN}Enter save file path: {Style.RESET_ALL}").strip()
                    if os.path.exists(file_path):
                        try:
                            recovered_data = self.create_emergency_save()
                            if recovered_data:
                                print(f"{Fore.GREEN}Recovery completed successfully!{Style.RESET_ALL}")
                                safe_input("Press Enter to continue...")
                            return
                        except Exception as e:
                            print(f"{Fore.RED}Recovery failed: {str(e)}{Style.RESET_ALL}")
                            safe_input("Press Enter to continue...")
                            return
                    else:
                        print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
                        continue
                else:
                    slot_num = int(choice)
                    if 1 <= slot_num <= len(save_slots):
                        slot_info = save_slots[slot_num - 1]
                        if slot_info['status'] != "Empty":
                            save_path = get_save_path("recovery", f"slot_{slot_num}")
                            if os.path.exists(save_path):
                                try:
                                    recovered_data = self.create_emergency_save()
                                    if recovered_data:
                                        print(f"{Fore.GREEN}Recovery completed successfully!{Style.RESET_ALL}")

                                        # Offer to load the recovered save
                                        load_choice = input(f"{Fore.CYAN}Load the recovered save now? (y/n): {Style.RESET_ALL}").strip().lower()
                                        if load_choice == 'y':
                                            # Create a Player object from recovered data
                                            try:
                                                player = Player(recovered_data["player_name"])
                                                # Restore all player data
                                                for key, value in recovered_data.items():
                                                    if hasattr(player, key):
                                                        setattr(player, key, value)

                                                self.player = player
                                                print(f"{Fore.GREEN}Recovered save loaded successfully!{Style.RESET_ALL}")
                                            except Exception as e:
                                                print(f"{Fore.YELLOW}Could not load recovered save: {str(e)}{Style.RESET_ALL}")

                                        safe_input("Press Enter to continue...")
                                    return
                                except Exception as e:
                                    print(f"{Fore.RED}Recovery failed: {str(e)}{Style.RESET_ALL}")
                                    safe_input("Press Enter to continue...")
                                    return
                            else:
                                print(f"{Fore.RED}Save file not found for slot {slot_num}{Style.RESET_ALL}")
                                continue
                        else:
                            print(f"{Fore.YELLOW}Slot {slot_num} is empty.{Style.RESET_ALL}")
                            continue
                    else:
                        print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                        continue

            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
                continue

    def load_game(self, save_name: Optional[str] = None) -> bool:
        """Simple and reliable load system"""
        try:
            if save_name:
                # Load specific save file
                save_path = get_save_path("player", save_name)
                if not os.path.exists(save_path):
                    print(f"{Fore.RED}Save '{save_name}' not found.{Style.RESET_ALL}")
                    return False
            else:
                # Show available saves for selection
                if not os.path.exists(SAVE_DIR):
                    print(f"{Fore.YELLOW}No saved games found.{Style.RESET_ALL}")
                    return False
                
                saves = []
                for filename in os.listdir(SAVE_DIR):
                    if filename.endswith('.wom'):
                        try:
                            filepath = os.path.join(SAVE_DIR, filename)
                            with open(filepath, 'rb') as f:
                                data = pickle.load(f)
                                player_name = data.get("name", "Unknown")
                                save_time = data.get("save_time", "Unknown")
                                level = data.get("trainer_level", 1)
                                saves.append((filename, player_name, save_time, level))
                        except Exception:
                            continue

                if not saves:
                    print(f"{Fore.YELLOW}No valid save files found.{Style.RESET_ALL}")
                    return False

                print(f"\n{Fore.CYAN}Available saved games:{Style.RESET_ALL}")
                for i, (filename, player, timestamp, level) in enumerate(saves, 1):
                    save_name_display = filename.replace('.wom', '')
                    print(f"{i}. {save_name_display} - {player} (Level {level}) - {timestamp}")

                try:
                    choice = int(input(f"\n{Fore.CYAN}Enter save number to load (or 0 to cancel): {Style.RESET_ALL}"))
                    if choice == 0:
                        return False
                    if 1 <= choice <= len(saves):
                        save_path = os.path.join(SAVE_DIR, saves[choice-1][0])
                    else:
                        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                        return False
                except ValueError:
                    print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
                    return False

            # Load the save file
            with open(save_path, 'rb') as f:
                save_data = pickle.load(f)

            # Create new player and restore data
            player = Player(save_data["name"])
            player.location = save_data.get("location", "Hometown")
            player.money = save_data.get("money", 100)
            player.monsters = save_data.get("monsters", [])
            player.inventory = save_data.get("inventory", {})
            player.active_monster_index = save_data.get("active_monster_index", 0)
            player.trainer_level = save_data.get("trainer_level", 5)
            player.exp = save_data.get("exp", 0)
            player.tokens = save_data.get("tokens", 500)
            player.equipment = save_data.get("equipment", {})
            player.materials = save_data.get("materials", {})
            player.visited_areas = save_data.get("visited_areas", {'Forest Grove'})
            player.daily_tasks = save_data.get("daily_tasks", {})

            # Restore dialogue system data
            player.character_opinions = save_data.get("character_opinions", {})
            player.dialogue_history = save_data.get("dialogue_history", {})
            player.story_moments = save_data.get("story_moments", [])
            player.moral_choices = save_data.get("moral_choices", [])
            player.reflection_points = save_data.get("reflection_points", 0)

            # Set the loaded player as current player
            self.player = player

            print(f"{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Welcome back, {player.name}!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Level {player.trainer_level} trainer with {len(player.monsters)} monsters{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Current location: {player.location}{Style.RESET_ALL}")

            return True

        except Exception as e:
            print(f"{Fore.RED}Error loading save: {e}{Style.RESET_ALL}")
            return False

    def fusion_menu(self):
        """Display fusion menu to combine two monsters"""
        if not self.player or len(self.player.monsters) < 2:
            print(f"{Fore.YELLOW}You need at least two monsters to perform fusion.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        # Display available monsters
        clear_screen()
        print(f"{Fore.MAGENTA}===== MONSTER FUSION =====\n{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Select two monsters to fuse. Both must be at least level {FUSION_LEVEL_REQUIREMENT}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Warning: The selected monsters will be consumed in the fusion process!{Style.RESET_ALL}\n")

        self.show_monsters(for_fusion=True)

        # Get first monster selection
        try:
            choice1 = int(input(f"\n{Fore.CYAN}Select first monster (0 to cancel): {Style.RESET_ALL}")) - 1
            if choice1 < 0 or choice1 >= len(self.player.monsters):
                print("Fusion cancelled.")
                safe_input("Press Enter to continue...")
                return

            monster1 = self.player.monsters[choice1]
            if monster1.level < FUSION_LEVEL_REQUIREMENT:
                print(f"{Fore.RED}This monster must be at least level {FUSION_LEVEL_REQUIREMENT} for fusion.{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")
                return

            # Get second monster selection
            choice2 = int(input(f"\n{Fore.CYAN}Select second monster (0 to cancel): {Style.RESET_ALL}")) - 1
            if choice2 < 0 or choice2 >= len(self.player.monsters) or choice1 == choice2:
                print("Fusion cancelled or invalid selection.")
                safe_input("Press Enter to continue...")
                return

            monster2 = self.player.monsters[choice2]
            if monster2.level < FUSION_LEVEL_REQUIREMENT:
                print(f"{Fore.RED}This monster must be at least level {FUSION_LEVEL_REQUIREMENT} for fusion.{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")
                return

            # Confirm fusion
            print(f"\n{Fore.YELLOW}You are about to fuse {monster1.get_colored_name()} and {monster2.get_colored_name()}.{Style.RESET_ALL}")
            confirm = input(f"{Fore.RED}This cannot be undone! Proceed? (y/n): {Style.RESET_ALL}").lower()

            if confirm != 'y':
                print("Fusion cancelled.")
                safe_input("Press Enter to continue...")
                return

            # Perform fusion
            fusion_monster = Monster.fuse(monster1, monster2)
            if fusion_monster:
                # Remove the original monsters
                self.player.monsters = [m for i, m in enumerate(self.player.monsters) 
                                        if i != choice1 and i != choice2]

                # Add the fusion monster
                self.player.add_monster(fusion_monster)

                print(f"\n{Fore.MAGENTA}✨ FUSION COMPLETE! ✨{Style.RESET_ALL}")
                print(f"Created new monster: {fusion_monster.get_colored_name()}")
                print(str(fusion_monster))
            else:
                print(f"{Fore.RED}Fusion failed. Both monsters must meet requirements.{Style.RESET_ALL}")

        except ValueError:
            print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")

        safe_input("Press Enter to continue...")

    def championship_battle(self):
        """Start a championship battle against powerful trainers"""
        if not self.player or not self.player.has_usable_monster():
            print(f"{Fore.RED}You need at least one healthy monster to challenge the championship.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        # Check if player has enough monsters
        if len(self.player.monsters) < 3:
            print(f"{Fore.RED}You need at least 3 monsters to challenge the championship.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        # Ensure player's monsters are strong enough
        if all(m.level < 20 for m in self.player.monsters):
            print(f"{Fore.RED}Your monsters are too weak for the championship. Train them to at least level 20.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        clear_screen()
        print(f"{Fore.YELLOW}===== MONSTER CHAMPIONSHIP =====\n{Style.RESET_ALL}")
        print(f"Welcome to the Monster Championship, {self.player.name}!")
        print("Here you'll face the toughest trainers and their powerful monsters.")
        print("Emerge victorious to earn the title of Monster Champion!")

        # Define championship trainers and their monsters based on progress
        trainers = [
            {
                "name": "Elite Trainer Maya",
                "monsters": [
                    self.all_monsters["Floracat"].clone(),
                    self.all_monsters["Boltfox"].clone(),
                    self.all_monsters["Rockbehemoth"].clone()
                ],
                "level_boost": 10 + (self.champion_battles_completed * 2)
            },
            {
                "name": "Master Trainer Rex",
                "monsters": [
                    self.all_monsters["Emberbear"].clone(),
                    self.all_monsters["Coralfish"].clone(),
                    self.all_monsters["Buzzer"].clone()
                ],
                "level_boost": 15 + (self.champion_battles_completed * 2)
            },
            {
                "name": "Champion Victor",
                "monsters": [
                    self.all_monsters["Springraze"].clone(),
                    self.all_monsters["Ignolf"].clone(), 
                    self.all_monsters["Aquartle"].clone(),
                    self.all_monsters["Rockbehemoth"].clone()
                ],
                "level_boost": 20 + (self.champion_battles_completed * 3)
            }
        ]

        # Allow player to heal before championship
        for monster in self.player.monsters:
            monster.full_heal()

        safe_input("\nYour monsters have been fully healed. Press Enter to begin the championship...")

        # Battle each trainer in sequence
        for trainer in trainers:
            clear_screen()
            print(f"\n{Fore.CYAN}{trainer['name']} challenges you to a battle!{Style.RESET_ALL}")

            # Level up trainer's monsters
            for monster in trainer["monsters"]:
                target_level = min(MAX_MONSTER_LEVEL, monster.level + trainer["level_boost"])
                while monster.level < target_level:
                    monster.level_up()

            # Create a non-wild battle
            battle = Battle(self.player, trainer["monsters"][0])
            battle.is_wild = False
            battle.can_catch = False

            # Custom battle logic for trainers with multiple monsters
            current_trainer_monster_index = 0
            self.current_battle = battle

            # Battle loop for this trainer
            while not battle.is_finished:
                clear_screen()
                self.display_battle_state()

                # Get player command
                command = input(f"\n{Fore.CYAN}What will you do? {Style.RESET_ALL}").strip().lower()
                parts = command.split()
                cmd = parts[0] if parts else ""
                arg = " ".join(parts[1:]) if len(parts) > 1 else None

                result = battle.player_turn(cmd, arg)
                print("\n" + result)

                # If battle finished, check if trainer has more monsters
                if battle.is_finished:
                    if battle.result == "win" and current_trainer_monster_index < len(trainer["monsters"]) - 1:
                        # Trainer sends out next monster
                        current_trainer_monster_index += 1
                        next_monster = trainer["monsters"][current_trainer_monster_index]
                        print(f"\n{Fore.CYAN}{trainer['name']} sends out {next_monster.get_colored_name()}!{Style.RESET_ALL}")
                        battle.wild_monster = next_monster
                        battle.is_finished = False
                        safe_input("Press Enter to continue...")
                    elif battle.result == "lose":
                        # Player lost the championship
                        print(f"\n{Fore.RED}You have been defeated by {trainer['name']}!{Style.RESET_ALL}")
                        print("Better luck next time...")
                        safe_input("Press Enter to continue...")
                        self.current_battle = None
                        return
                else:
                    # Wild monster's turn
                    wild_result = battle.wild_monster_turn()
                    print("\n" + wild_result)
                    safe_input("Press Enter to continue...")

                    # Check if player's monster fainted
                    if battle.is_finished and battle.result == "lose":
                        if self.player.has_usable_monster():
                            # Let player switch to another monster
                            next_index = self.player.get_first_usable_monster_index()
                            self.player.switch_active_monster(next_index)
                            battle.is_finished = False
                            active_monster_name = (self.player.active_monster.get_colored_name() 
                                                  if self.player.active_monster and hasattr(self.player.active_monster, 'get_colored_name') 
                                                  else "Monster")
                            print(f"\n{Fore.GREEN}Go, {active_monster_name}!{Style.RESET_ALL}")
                            safe_input("Press Enter to continue...")
                        else:
                            # All player's monsters fainted
                            print(f"\n{Fore.RED}All your monsters have fainted! You lost to {trainer['name']}.{Style.RESET_ALL}")
                            safe_input("Press Enter to continue...")
                            self.current_battle = None
                            return

            # Trainer defeated
            print(f"\n{Fore.GREEN}You defeated {trainer['name']}!{Style.RESET_ALL}")

            # Heal player's monsters between trainer battles
            for monster in self.player.monsters:
                monster.heal(monster.max_hp // 2)  # Heal 50%

            print("\nYour monsters recovered some HP for the next battle.")
            safe_input("Press Enter to continue...")

        # Championship completed
        clear_screen()
        print(f"\n{Fore.YELLOW}🏆 CONGRATULATIONS! 🏆{Style.RESET_ALL}")
        print(f"You have defeated all trainers and become the {self.champion_battles_completed + 1}-time Monster Champion!")

        # Award prize money
        prize_money = 2000 + (self.champion_battles_completed * 500)
        self.player.money += prize_money
        print(f"\nYou received ${prize_money} as prize money!")

        # Record championship victory
        self.champion_battles_completed += 1

        # Save champion data to file
        if self.db_available:
            try:
                # Find player's strongest monster
                strongest_monster = max(self.player.monsters, key=lambda m: m.level)

                # Read existing champions
                champions = []
                if os.path.exists(CHAMPIONS_FILE):
                    try:
                        with open(CHAMPIONS_FILE, 'rb') as f:
                            champions = pickle.load(f)
                    except Exception:
                        # If file is corrupted, start with empty list
                        champions = []

                # Add new champion data
                champion_data = {
                    "player_name": self.player.name,
                    "monster": strongest_monster,
                    "win_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                champions.append(champion_data)

                # Save to file
                with open(CHAMPIONS_FILE, 'wb') as f:
                    pickle.dump(champions, f)

                print(f"\n{Fore.GREEN}Your champion {strongest_monster.get_colored_name()} has been recorded in the Hall of Fame!{Style.RESET_ALL}")
            except Exception as e:
                print(f"Error recording championship: {e}")

        safe_input("Press Enter to continue...")

    def process_command(self, command: str):
        """Process player commands"""
        # Handle slash commands
        if command.startswith('/'):
            command = command[1:]  # Remove the slash prefix

        parts = command.split()
        cmd = parts[0] if parts else ""
        arg = " ".join(parts[1:]) if len(parts) > 1 else None

        # Handle command shortcuts
        if cmd == "e":
            cmd = "explore"
        elif cmd == "t":
            cmd = "travel"
        elif cmd == "m":
            cmd = "monsters"
        elif cmd == "i":
            cmd = "items"
        elif cmd == "h":
            cmd = "help"
        elif cmd == "s":
            cmd = "save"
        elif cmd == "l":
            cmd = "load"
        elif cmd == "f":
            cmd = "fusion"
        elif cmd == "c":
            cmd = "championship"
        elif cmd == "q":
            cmd = "quit"
        elif cmd == "st":
            cmd = "stats"
        elif cmd == "sk":
            cmd = "skills"
        elif cmd == "eq":
            cmd = "equipment"
        elif cmd == "cr":
            cmd = "craft"
        elif cmd == "tr":
            cmd = "train"
        elif cmd == "sh":
            cmd = "shop"
        elif cmd == "gu":
            cmd = "guild"
        elif cmd == "qu":
            cmd = "quests"
        elif cmd == "ac":
            cmd = "achievements"
        elif cmd == "le":
            cmd = "leaderboard"
        elif cmd == "we":
            cmd = "weather"
        elif cmd == "ti":
            cmd = "time"
        elif cmd == "ma":
            cmd = "map"
        elif cmd == "al":
            cmd = "alliance"

        # In battle, handle battle commands
        if self.current_battle:
            self.process_battle_command(cmd, arg)
            return

        # Regular commands when not in battle
        if cmd == "explore":
            self.explore()
        elif cmd == "travel":
            self.travel()
        elif cmd == "monsters":
            self.show_monsters()
        elif cmd == "items":
            self.show_items()
        elif cmd == "heal":
            self.heal_monsters()
        elif cmd == "help":
            self.show_help()
        elif cmd == "save":
            self.show_save_game_menu()
        elif cmd == "load":
            self.show_load_game_menu()
        elif cmd == "fusion":
            self.fusion_menu()
        elif cmd == "championship":
            self.championship_battle()
        elif cmd == "quit" or cmd == "exit":
            self.quit_game()
        # Add special commands for puzzles and legendary encounters
        elif cmd == "puzzle":
            self.start_puzzle()
        elif cmd == "legendary":
            self.legendary_encounter()
        # New RPG commands
        elif cmd == "stats":
            self.show_detailed_stats()
        elif cmd == "skills":
            self.show_skills_menu()
        elif cmd == "equipment":
            self.show_equipment_menu()
        elif cmd == "craft":
            self.show_crafting_menu()
        elif cmd == "train":
            self.show_training_menu()
        elif cmd == "shop":
            self.show_shop_menu()
        elif cmd == "guild":
            self.show_guild_menu()
        elif cmd == "quests":
            self.show_quest_menu()
        elif cmd == "achievements":
            self.show_achievements()
        elif cmd == "leaderboard":
            self.show_leaderboard()
        elif cmd == "weather":
            self.show_weather_system()
        elif cmd == "time":
            self.show_time_system()
        elif cmd == "map":
            self.show_world_map()
        elif cmd == "alliance":
            self.show_alliance_menu()
        elif cmd == "inventory":
            self.show_advanced_inventory()
        elif cmd == "research":
            self.show_research_menu()
        elif cmd == "dungeon":
            self.enter_dungeon()
        elif cmd == "raid":
            self.join_raid()
        elif cmd == "pvp":
            self.enter_pvp()
        elif cmd == "market":
            self.show_market()
        elif cmd == "dailies":
            self.show_daily_tasks()
        elif cmd == "events":
            self.show_events()
        elif cmd == "recovery":
            self.recovery_wizard_menu()
        elif cmd == "emotions" or cmd == "bonds":
            self.show_character_relationships()
        elif cmd == "reflect" or cmd == "reflection":
            self.show_reflection_menu()
        elif cmd == "contemplate":
            self.quick_reflect()
        elif cmd == "talk" or cmd == "dialogue":
            self.show_npc_menu()
        elif cmd.startswith("talk "):
            npc_name = cmd[5:].strip()
            self.talk_to_npc(npc_name)
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' to see available commands.")
            safe_input("Press Enter to continue...")

    def process_battle_command(self, cmd: str, arg: Optional[str] = None):
        """Process battle commands"""
        if not self.current_battle:
            print("Error: No active battle!")
            return

        if not self.player:
            print("Error: No active player!")
            self.current_battle = None
            return

        # Handle battle command shortcuts
        if cmd == "f":
            cmd = "fight"
        elif cmd == "c":
            cmd = "catch"
        elif cmd == "s":
            cmd = "switch"
        elif cmd == "i":
            cmd = "item"
        elif cmd == "r":
            cmd = "run"

        battle = self.current_battle

        if cmd in ["fight", "catch", "switch", "item", "run"]:
            try:
                result = battle.player_turn(cmd, arg)
                print("\n" + result)
            except Exception as e:
                print(f"Error during battle: {str(e)}")
                self.current_battle = None
                safe_input("\nPress Enter to continue...")
                return

            # Check if battle is finished
            if not hasattr(battle, 'is_finished') or battle.is_finished:
                if not hasattr(battle, 'result'):
                    print("\nBattle ended unexpectedly!")
                    self.current_battle = None
                    safe_input("\nPress Enter to continue...")
                    return

                if battle.result == "win":
                    print("\nYou won the battle!")

                    # Reward for winning
                    if hasattr(battle, 'wild_monster') and battle.wild_monster:
                        money_reward = battle.wild_monster.level * 10
                        self.player.money += money_reward
                        print(f"You earned ${money_reward}!")

                        # Award trainer exp for winning battles
                        exp_reward = battle.wild_monster.level * 3
                        if self.player.gain_trainer_exp(exp_reward):
                            print(f"{Fore.GREEN}You gained {exp_reward} trainer exp and leveled up to Trainer Level {self.player.trainer_level}!{Style.RESET_ALL}")
                            print("Your monsters can now grow to this higher level.")
                        else:
                            print(f"You gained {exp_reward} trainer exp. ({self.player.exp}/{self.player.exp_to_level})")
                    else:
                        # Default reward if monster info is missing
                        self.player.money += 50
                        print("You earned $50!")

                        # Default trainer exp
                        if self.player.gain_trainer_exp(15):
                            print(f"{Fore.GREEN}You gained 15 trainer exp and leveled up to Trainer Level {self.player.trainer_level}!{Style.RESET_ALL}")
                        else:
                            print(f"You gained 15 trainer exp. ({self.player.exp}/{self.player.exp_to_level})")

                elif battle.result == "lose":
                    print("\nYou lost the battle!")

                    # Penalty for losing
                    penalty = min(50, self.player.money // 4)
                    self.player.money -= penalty
                    print(f"You lost ${penalty}...")

                    # Fully heal monsters when returning to Hometown
                    self.player.location = "Hometown"
                    if hasattr(self.player, 'monsters') and self.player.monsters:
                        for monster in self.player.monsters:
                            if monster:
                                monster.full_heal()

                elif battle.result == "catch":
                    print("\nYou caught a new monster!")

                elif battle.result == "run":
                    print("\nYou got away safely!")

                # End battle
                self.current_battle = None
                safe_input("\nPress Enter to continue...")
        else:
            print("Invalid battle command.")
            print("Available commands: fight, catch, switch, item, run")
            safe_input("Press Enter to continue...")

    def explore(self):
        """Explore the current location"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        location = self.player.location if hasattr(self.player, 'location') else "Unknown"

        print(f"\nExploring {location}...")
        time.sleep(1)

        # Check for location-specific story events
        if self.check_story_event(location):
            return

        # Location-specific exploration events
        location_events = {
            "Hometown": [
                "You stroll around the peaceful streets of your hometown.",
                "You run into Professor Pino who gives you a free Potion!",
                "Your neighbor gives you a spare Monster Ball they found.",
                "You find $30 that someone dropped near the lab."
            ],
            "Mystic Forest": [
                "You wander through the dense magical forest, hearing strange sounds.",
                "You discover a rare Berry hidden among the foliage!",
                "A friendly Forest Sprite gives you a Monster Ball!",
                "You find an old treasure chest containing $100!"
            ],
            "Windy Plains": [
                "The tall grass rustles as you walk through the wide open plains.",
                "You find a Potion half-buried in the ground!",
                "A traveling merchant gives you a Monster Ball for helping with directions.",
                "You find $40 in an abandoned campsite."
            ],
            "Crystal Cavern": [
                "The glittering crystals illuminate your path through the cavern.",
                "You find a Super Potion among the glowing crystals!",
                "You discover a Monster Ball made of crystal! It still works.",
                "You find a small vein of precious gems worth $200!"
            ],
            "Volcanic Ridge": [
                "Heat waves distort your vision as you explore the volcanic terrain.",
                "You find a Heat-Proof Potion near a lava pool!",
                "A Monster Ball made of special heat-resistant material sits on a rock.",
                "You find $80 in an old explorer's backpack."
            ],
            "Misty Swamp": [
                "The thick fog makes it difficult to see far as you wade through the swamp.",
                "You find a Purified Potion floating in a lotus leaf!",
                "A Monster Ball is half-buried in the soft mud.",
                "You discover $60 in an old waterproof container."
            ],
            "Shadow Peak": [
                "The mountain's shadow creates an eerie atmosphere as you explore the rocky terrain.",
                "You find a Shadow Potion hidden in a crevice!",
                "A Monster Ball with dark energy emanates from behind a boulder.",
                "You find $150 in an old mountaineer's cache."
            ],
            "Ancient Ruins": [
                "The crumbling structures tell stories of a civilization long gone.",
                "You discover an Ancient Potion with strange markings!",
                "A Monster Ball made of ancient materials rests on a pedestal.",
                "You find ancient coins worth $250 in a hidden chamber!"
            ]
        }

        # Default events if location is not in the dictionary
        events = location_events.get(location, [
            "You search the area but find nothing of interest.",
            "You found a Potion on the ground!",
            "You found a Monster Ball in the bushes!",
            "You found $50 on the ground!"
        ])

        # Weight probabilities - first option is most common
        weights = [0.7, 0.1, 0.1, 0.1]
        event = random.choices(events, weights=weights)[0]

        print(event)

        # Handle rewards
        try:
            if "Potion" in event and hasattr(self, 'all_items'):
                if "Super Potion" in event and "Super Potion" in self.all_items:
                    self.player.add_item(self.all_items["Super Potion"])
                elif "Potion" in event and "Potion" in self.all_items:
                    self.player.add_item(self.all_items["Potion"])
            elif "Monster Ball" in event and hasattr(self, 'all_items') and "Monster Ball" in self.all_items:
                self.player.add_item(self.all_items["Monster Ball"])
            elif "$" in event:
                # Extract amount from string
                amount_str = event.split("$")[1].split(" ")[0].replace("!", "")
                try:
                    amount = int(amount_str)
                    self.player.money += amount
                except ValueError:
                    self.player.money += 50  # Default if parsing fails

            # Always gain trainer experience from exploring
            exp_gain = 5  # Base exploration exp

            # Bonus exp based on location difficulty
            location_exp_bonus = {
                "Hometown": 0,
                "Windy Plains": 2,
                "Mystic Forest": 5,
                "Crystal Cavern": 8,
                "Volcanic Ridge": 10,
                "Misty Swamp": 12,
                "Shadow Peak": 15,
                "Ancient Ruins": 18
            }

            # Add location bonus
            exp_gain += location_exp_bonus.get(self.player.location, 0)

            # Award trainer exp
            if self.player.gain_trainer_exp(exp_gain):
                print(f"{Fore.GREEN}You gained {exp_gain} trainer exp and leveled up to Trainer Level {self.player.trainer_level}!{Style.RESET_ALL}")
                print("Your monsters can now grow to this level.")
            else:
                print(f"You gained {exp_gain} trainer exp. ({self.player.exp}/{self.player.exp_to_level})")

        except Exception as e:
            print(f"Error while processing rewards: {str(e)}")

        safe_input("\nPress Enter to continue...")

    def check_story_event(self, location: str) -> bool:
        """Check and trigger location-specific story events. Returns True if an event was triggered."""
        # Safety check for player
        if not self.player:
            return False

        # Initialize player progress tracking if it doesn't exist
        if not hasattr(self.player, 'story_progress'):
            self.player.story_progress = {}

        # Location-specific storylines with progression
        story_events = {
            "Mystic Forest": [
                {
                    "id": "mystic_forest_1",
                    "text": f"""As you venture deeper into the Mystic Forest, you notice strange markings on the trees.
Following them leads you to a small clearing where an elderly sage sits meditating.

{Fore.CYAN}Sage Elderleaf:{Style.RESET_ALL} "Welcome, young trainer. I've been expecting someone with your potential.
The forest has been behaving strangely lately. Dark energies are corrupting the ancient magic.
If you can prove your worth, I may teach you about the legendary monsters that once protected this land."

The sage asks you to return once you've grown stronger in your journey.""",
                    "min_level": 10,
                    "next_event": "mystic_forest_2"
                },
                {
                    "id": "mystic_forest_2",
                    "text": f"""You return to the clearing where Sage Elderleaf resides.
The sage smiles as you approach, sensing your increased strength.

{Fore.CYAN}Sage Elderleaf:{Style.RESET_ALL} "You've grown stronger, just as I anticipated.
The corruption in the forest stems from an ancient seal being weakened.
The seal once contained dark energies that would twist and corrupt monsters.
I will grant you this protective charm that may help in your journey."

You received a {Fore.GREEN}Mystic Pendant{Style.RESET_ALL}!

{Fore.CYAN}Sage Elderleaf:{Style.RESET_ALL} "The legendary monster Celestius is said to appear to those who solve 
the puzzle of the Ancient Stone Tablets. Perhaps you might be worthy someday."

The sage suggests exploring other regions to grow even stronger.""",
                    "min_level": 20,
                    "reward": {"type": "item", "name": "Mystic Pendant"},
                    "next_event": "mystic_forest_3"
                },
                {
                    "id": "mystic_forest_3",
                    "text": f"""Upon returning to the Mystic Forest, you find the clearing in disarray. 
Signs of a struggle are evident, and Sage Elderleaf is nowhere to be found.

Instead, you discover a hastily scribbled note:
{Fore.YELLOW}"Darkness spreads. The ancient seal is breaking. Find the four elemental crystals:
Forest Crystal (here), Fire Crystal (volcano), Water Crystal (swamp), Earth Crystal (ruins).
Only then can the seal be restored. Beware the shadow creatures!"{Style.RESET_ALL}

Near the note, you spot something glimmering in the grass.

You found the {Fore.GREEN}Forest Crystal{Style.RESET_ALL}!

This seems to be the start of a greater quest that spans across different regions.""",
                    "min_level": 30,
                    "reward": {"type": "quest_item", "name": "Forest Crystal"},
                    "next_event": "mystic_forest_complete"
                }
            ],
            "Volcanic Ridge": [
                {
                    "id": "volcanic_ridge_1",
                    "text": f"""As you climb higher on the Volcanic Ridge, you notice a cave entrance emanating intense heat.
Inside, you find a muscular man hammering at what appears to be special monster equipment.

{Fore.RED}Master Smith Ignis:{Style.RESET_ALL} "Not often we get visitors up here! This volcano provides the perfect 
heat for forging special items for monster trainers. My ancestors have been guardians of the volcano's secrets for generations.

Recently, the volcano has become more active, and fire monsters have been acting unusually aggressive.
If you can prove your strength as a trainer, I might share some of our ancient craft with you."

He suggests returning after you've trained your monsters further.""",
                    "min_level": 15,
                    "next_event": "volcanic_ridge_2"
                },
                {
                    "id": "volcanic_ridge_2",
                    "text": f"""You return to Master Smith Ignis's forge in the volcano.
The smith inspects your monsters and nods approvingly.

{Fore.RED}Master Smith Ignis:{Style.RESET_ALL} "You've shown dedication to your training. As promised, 
I'll share some of our craft with you. This heat resistant collar will make your monsters more resilient to fire attacks."

You received a {Fore.RED}Flame Collar{Style.RESET_ALL}!

{Fore.RED}Master Smith Ignis:{Style.RESET_ALL} "There's been talk of a legendary fire monster, Pyrovern, that resides deep 
in the volcano's heart. Only those who pass the Fire Temple Trials might catch a glimpse of it.

But more pressing matters concern me - someone has been tampering with the ancient volcanic seals. 
If you find anything unusual in your travels, please return."

The master smith returns to his work, occasionally glancing at the deeper tunnels with concern.""",
                    "min_level": 25,
                    "reward": {"type": "item", "name": "Flame Collar"},
                    "next_event": "volcanic_ridge_3"
                },
                {
                    "id": "volcanic_ridge_3",
                    "text": f"""When you return to the volcanic forge, you find it abandoned and in disarray.
Tools are scattered everywhere, and it seems Master Smith Ignis left in a hurry.

On his anvil lies a glowing red crystal and a hastily scrawled note:
{Fore.YELLOW}"Darkness has reached the volcano. The ancient seal beneath is failing.
Take this Fire Crystal - one of four needed to restore the great seal.
Find the others: Forest Crystal (mystic forest), Water Crystal (swamp), Earth Crystal (ruins).
I've gone to investigate the disturbances below. DO NOT FOLLOW!"{Style.RESET_ALL}

You found the {Fore.RED}Fire Crystal{Style.RESET_ALL}!

The volcano rumbles ominously as you pocket the crystal, suggesting whatever is happening is accelerating.""",
                    "min_level": 35,
                    "reward": {"type": "quest_item", "name": "Fire Crystal"},
                    "next_event": "volcanic_ridge_complete"
                }
            ],
            "Misty Swamp": [
                {
                    "id": "misty_swamp_1",
                    "text": f"""As you carefully navigate through the Misty Swamp, you notice a small hut on stilts rising above the murky water.
A slender woman with blue markings on her face watches you approach.

{Fore.BLUE}Swamp Witch Mira:{Style.RESET_ALL} "Few venture this deep into my swamp. What brings you here, young trainer?
The waters have been restless lately, and the monsters grow anxious.
There is an imbalance spreading throughout the land that even I cannot fully comprehend.

Return when you've grown more attuned to your monsters. Perhaps then we can discuss what darkens these waters."

She retreats into her hut, leaving you with many questions.""",
                    "min_level": 18,
                    "next_event": "misty_swamp_2"
                },
                {
                    "id": "misty_swamp_2",
                    "text": f"""Upon returning to the witch's hut in the Misty Swamp, you find Mira brewing a strange concoction.
She studies you carefully before speaking.

{Fore.BLUE}Swamp Witch Mira:{Style.RESET_ALL} "Your bond with your monsters has deepened. Good.
The swamp speaks to those who listen, and it tells me of a growing darkness.
Ancient seals that have protected this land for generations are weakening.

Take this Water Charm. It will help your monsters navigate watery depths and may protect against what's coming."

You received a {Fore.BLUE}Water Charm{Style.RESET_ALL}!

{Fore.BLUE}Swamp Witch Mira:{Style.RESET_ALL} "There are whispers of a legendary water monster in the deepest part of the swamp.
But more concerning are the shadow-touched creatures I've begun to see at night.
Be vigilant in your travels, trainer.""",
                    "min_level": 28,
                    "reward": {"type": "item", "name": "Water Charm"},
                    "next_event": "misty_swamp_3"
                },
                {
                    "id": "misty_swamp_3",
                    "text": f"""When you return to the swamp, you find Mira's hut partially submerged and abandoned.
The door hangs open, swinging in the humid breeze.

Inside, furniture is overturned and there are signs of a struggle. On her scrying table floats a glowing blue crystal
suspended in a protective bubble of water, next to a water-resistant parchment:

{Fore.YELLOW}"The darkness rises faster than I foresaw. Shadow creatures attacked in the night.
This Water Crystal is one of four elemental keys needed to restore the great seal.
The others: Forest Crystal (mystic forest), Fire Crystal (volcano), Earth Crystal (ruins).
I've gone to consult with the water spirits. The crystal's protective bubble will only release to one pure of heart."{Style.RESET_ALL}

You reach for the crystal and the bubble dissolves at your touch.

You found the {Fore.BLUE}Water Crystal{Style.RESET_ALL}!

Somewhere in the distance, you hear an unnatural howling that doesn't belong in the swamp.""",
                    "min_level": 38,
                    "reward": {"type": "quest_item", "name": "Water Crystal"},
                    "next_event": "misty_swamp_complete"
                }
            ],
            "Ancient Ruins": [
                {
                    "id": "ancient_ruins_1",
                    "text": f"""While exploring the crumbling structures of the Ancient Ruins, you stumble upon a well-preserved chamber.
Inside, an archaeologist is carefully documenting carvings on the walls.

{Fore.YELLOW}Professor Artifact:{Style.RESET_ALL} "Oh! A visitor! Fascinating! I don't get many of those out here.
These ruins hold secrets to an ancient civilization that lived in harmony with powerful monsters.
The carvings suggest they created some sort of powerful seal to contain a great darkness.

Most interesting are these four symbols that appear repeatedly: a leaf, a flame, a water drop, and a mountain.
I believe they represent elemental powers that were crucial to their magic.

You seem to have a strong bond with your monsters. Perhaps you'll uncover more than I can with my mere academic approach.
Return when you've grown stronger, and I may share more of my findings."

The professor returns to his meticulous note-taking.""",
                    "min_level": 20,
                    "next_event": "ancient_ruins_2"
                },
                {
                    "id": "ancient_ruins_2",
                    "text": f"""You return to Professor Artifact's chamber in the Ancient Ruins.
The professor is visibly excited to see you again.

{Fore.YELLOW}Professor Artifact:{Style.RESET_ALL} "You've returned! And stronger too! Excellent!
I've made a breakthrough in my research. These ruins were once a temple dedicated to maintaining a powerful seal.
The seal contained an ancient darkness that corrupted monsters and turned them against humans.

I found this artifact that seems to resonate with monster energy. Perhaps it will aid you in your journey."

You received an {Fore.YELLOW}Ancient Amulet{Style.RESET_ALL}!

{Fore.YELLOW}Professor Artifact:{Style.RESET_ALL} "The legendary monster Chronodrake is mentioned in these texts.
It was supposedly the guardian of time itself and helped create the seal.

But more disturbing is what I've found in the deeper chambers... There are signs the seal is weakening.
Black ooze seeps through some of the walls, and I've heard strange noises at night.
Be careful in your travels, trainer. Something ancient is stirring.""",
                    "min_level": 30,
                    "reward": {"type": "item", "name": "Ancient Amulet"},
                    "next_event": "ancient_ruins_3"
                },
                {
                    "id": "ancient_ruins_3",
                    "text": f"""Upon returning to the Ancient Ruins, you find the professor's chamber in chaos.
Papers are scattered everywhere, furniture is overturned, and there's no sign of Professor Artifact.

On his research table, weighed down by a stone paperweight, is a letter:

{Fore.YELLOW}"To whoever finds this - The seal is breaking faster than I feared. Shadow creatures emerged from the depths last night.
I managed to recover the Earth Crystal - one of four elemental keys needed to restore the great seal.
The others: Forest Crystal (mystic forest), Fire Crystal (volcano), Water Crystal (swamp).

The texts speak of a temple beneath Shadow Peak where the four crystals can be united to restore the seal.
I'm going into hiding with my research. If all four crystals are gathered, seek the hidden entrance at Shadow Peak's summit.
May the ancient guardians protect you."{Style.RESET_ALL}

Beside the note sits a glowing brown crystal.

You found the {Fore.YELLOW}Earth Crystal{Style.RESET_ALL}!

A cold wind blows through the chamber, carrying whispers that seem just beyond comprehension.""",
                    "min_level": 40,
                    "reward": {"type": "quest_item", "name": "Earth Crystal"},
                    "next_event": "ancient_ruins_complete"
                }
            ],
            "Shadow Peak": [
                {
                    "id": "shadow_peak_1",
                    "text": f"""As you climb the treacherous paths of Shadow Peak, you notice the mountain seems unnaturally dark,
even in broad daylight. Near the summit, you discover a small shrine partially hidden by rocks.

A tall, cloaked figure stands beside it, motionless until you approach.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "Few find their way here. Fewer still are worthy of the peak's secrets.
This mountain stands at the convergence of all elemental energies. It is here that the ancient seal was first created,
and here that it must be restored when the time comes.

You carry the weight of destiny, young trainer. I can sense it in your aura.
But you are not yet ready for what lies beneath this peak. Return when you have gathered the four elemental crystals,
and I will guide you to the Chamber of Sealing."

The figure vanishes like smoke, leaving only the echo of their words.""",
                    "min_level": 35,
                    "next_event": "shadow_peak_2"
                },
                {
                    "id": "shadow_peak_2", 
                    "text": f"""You return to Shadow Peak with the four elemental crystals in your possession.
The Keeper of Shadows materializes before you as if they were waiting.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "You have done well, chosen one. The crystals sing with elemental harmony.
But know this - the path ahead is fraught with danger. The Sealed Darkness has grown strong during its imprisonment,
feeding on fear and despair from across the lands.

Below this peak lies the Chamber of Sealing. There you will face not only the darkness itself,
but also the trials of your own heart. Only one who remains true to their purpose can hope to succeed."

The ground beneath your feet begins to glow with mystical energy.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "Step forward, and let the mountain judge your worth."

A hidden passage opens in the rock face, leading deep into the mountain's heart.""",
                    "min_level": 45,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       len([item for item in self.player.quest_items if "Crystal" in item]) >= 4,
                    "reward": {"type": "access", "name": "Chamber of Sealing"},
                    "next_event": "shadow_peak_complete"
                }
            ],
            "Enchanted Grove": [
                {
                    "id": "enchanted_grove_1",
                    "text": f"""Deep within the Enchanted Grove, you discover a clearing where time itself seems to flow differently.
Ancient trees tower overhead, their leaves shimmering with ethereal light.

A voice speaks from everywhere and nowhere:

{Fore.GREEN}Spirit of the Grove:{Style.RESET_ALL} "Welcome, young soul. This place exists between moments,
where past and future converge. We have watched your journey with great interest.
The darkness that threatens the world once consumed entire forests like this one.

We offer you a glimpse of what was lost, and what might be saved."

Suddenly, you see visions of the world as it once was - vibrant, alive, and in perfect harmony.""",
                    "min_level": 25,
                    "next_event": "enchanted_grove_2"
                },
                {
                    "id": "enchanted_grove_2",
                    "text": f"""The Spirit of the Grove shows you more visions - this time of the approaching darkness.

{Fore.GREEN}Spirit of the Grove:{Style.RESET_ALL} "See how the shadow spreads, corrupting all it touches.
But also see this - points of light that resist the darkness. You are one such light, trainer.

Take this seed. Plant it when the darkness seems overwhelming, and remember that even in the deepest shadow,
new life can take root."

You received a {Fore.GREEN}Seed of Hope{Style.RESET_ALL}!

{Fore.GREEN}Spirit of the Grove:{Style.RESET_ALL} "There are others like you scattered across the realms.
A knight who guards the Celestial Bridge, a scholar who protects the Library of Ages,
a healer who tends to the wounded in the Sanctuary of Light. Find them, and together you may stand a chance."

The visions fade, but the knowledge remains.""",
                    "min_level": 30,
                    "reward": {"type": "quest_item", "name": "Seed of Hope"},
                    "next_event": "enchanted_grove_3"
                },
                {
                    "id": "enchanted_grove_3",
                    "text": f"""When you return to the Enchanted Grove, you find it under attack by shadow creatures.
The ancient trees are withering as dark energy spreads through the clearing.

{Fore.GREEN}Spirit of the Grove:{Style.RESET_ALL} "The darkness... it has found us! Quick, trainer!
Use the Seed of Hope - plant it in the Heart of the Grove before all is lost!"

You plant the seed in the center of the clearing. Immediately, brilliant light erupts from the ground,
pushing back the shadows and restoring life to the grove.

{Fore.GREEN}Spirit of the Grove:{Style.RESET_ALL} "You have saved us! As promised, here is knowledge of your allies.
Seek the Celestial Bridge to the north, where Sir Luminous guards the passage between realms.
May the light of hope guide your path!"

You received the {Fore.CYAN}Map of Allies{Style.RESET_ALL}!""",
                    "min_level": 35,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Seed of Hope" in self.player.quest_items,
                    "reward": {"type": "quest_item", "name": "Map of Allies"},
                    "next_event": "enchanted_grove_complete"
                }
            ],
            "Celestial Bridge": [
                {
                    "id": "celestial_bridge_1",
                    "text": f"""You arrive at the Celestial Bridge, a magnificent structure of pure light spanning a chasm between worlds.
A knight in radiant armor stands guard at its center.

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "Hold, traveler! This bridge connects the mortal realm to the celestial plane.
In these dark times, I must be cautious of who I allow to pass.

But wait... I sense something familiar about you. You carry the essence of hope, don't you?
The Spirit of the Grove spoke truly - you are indeed one of the chosen ones.

However, before I can share the knowledge you seek, you must prove your dedication to the light.
Return when you have grown stronger in both body and spirit.""",
                    "min_level": 32,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Map of Allies" in self.player.quest_items,
                    "next_event": "celestial_bridge_2"
                },
                {
                    "id": "celestial_bridge_2",
                    "text": f"""Sir Luminous examines you with eyes that seem to see into your very soul.

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "Yes, you have grown indeed. The light within you burns brighter.
I will share with you the secret of the Celestial Weapons - artifacts that can harm even the Sealed Darkness itself.

But know this: these weapons choose their wielders. You cannot simply take them by force.
They respond only to pure intentions and selfless courage."

He hands you a glowing scroll.

You received the {Fore.YELLOW}Scroll of Celestial Weapons{Style.RESET_ALL}!

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "Seek the Sanctuary of Light to the east, where Healer Serenity tends to the wounded.
She possesses one of these weapons - the Staff of Restoration. But she will only entrust it to one who has proven their compassion.

The other weapon, the Sword of Truth, lies hidden in the Library of Ages, guarded by Scholar Wisdom.
You must answer his riddles to prove your understanding of the greater picture."

Thunder rumbles in the distance as dark clouds gather.""",
                    "min_level": 38,
                    "reward": {"type": "quest_item", "name": "Scroll of Celestial Weapons"},
                    "next_event": "celestial_bridge_3"
                },
                {
                    "id": "celestial_bridge_3",
                    "text": f"""When you return to the Celestial Bridge, you find Sir Luminous engaged in battle with shadow creatures
attempting to corrupt the bridge itself.

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "Trainer! Perfect timing! These shadows seek to sever the connection
between realms. If they succeed, the celestial plane will be cut off from our world!

Help me defend the bridge! Together we can drive them back!"

You and Sir Luminous fight side by side, your combined light pushing back the darkness.

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "Well fought, ally! Your courage in battle proves your worth.
Take this - my personal blessing. It will enhance the power of any celestial weapon you wield."

You received {Fore.YELLOW}Sir Luminous's Blessing{Style.RESET_ALL}!

{Fore.YELLOW}Sir Luminous:{Style.RESET_ALL} "The final battle approaches. When you face the Sealed Darkness,
remember that you do not fight alone. The light of all who believe in hope fights with you!"

The bridge glows brighter than ever, a beacon of hope in the growing darkness.""",
                    "min_level": 42,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Scroll of Celestial Weapons" in self.player.quest_items,
                    "reward": {"type": "blessing", "name": "Luminous's Blessing"},
                    "next_event": "celestial_bridge_complete"
                }
            ],
            "Sanctuary of Light": [
                {
                    "id": "sanctuary_1",
                    "text": f"""You arrive at the Sanctuary of Light, a peaceful temple where injured creatures from across the realms
come to heal. A gentle woman in white robes tends to a wounded Springraze.

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "Welcome, traveler. All who enter here are welcome, regardless of their past.
I sense great purpose in you, but also deep burdens. 

The creatures tell me of growing darkness across the lands. Many who come here speak of corruption and shadow.
If you truly seek to help, I have tasks that would prove your compassion."

She gestures to the many injured creatures around the sanctuary.

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "Help me tend to these poor souls. Return when you have learned more about healing
both body and spirit. True power comes not from strength alone, but from the desire to protect and nurture.""",
                    "min_level": 30,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Scroll of Celestial Weapons" in self.player.quest_items,
                    "next_event": "sanctuary_2"
                },
                {
                    "id": "sanctuary_2", 
                    "text": f"""Healer Serenity watches as you help tend to the injured creatures with genuine care and patience.

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "Your touch brings comfort to these beings. You have the heart of a true healer.
The Staff of Restoration calls to those who put others' wellbeing before their own.

But before I can entrust it to you, you must face one final test. Deep in the Caverns of Sorrow,
there lies a creature consumed by darkness - not evil, but simply lost and in pain.
Bring it back to the light, and the staff shall be yours."

She gives you a small vial of glowing water.

You received {Fore.CYAN}Holy Water{Style.RESET_ALL}!

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "This water can cleanse corruption, but only if used with genuine love and compassion.
Remember - the creature in the caverns is not your enemy. It is a victim that needs saving."

In the distance, you hear the mournful howling of something in terrible pain.""",
                    "min_level": 36,
                    "reward": {"type": "quest_item", "name": "Holy Water"},
                    "next_event": "sanctuary_3"
                },
                {
                    "id": "sanctuary_3",
                    "text": f"""You return from the Caverns of Sorrow, leading a now-peaceful Shadow Wolf that has been cleansed of corruption.
Healer Serenity's eyes fill with tears of joy.

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "You have done what many would consider impossible. You saved a creature
that others would have simply destroyed. This is true strength - the power to heal rather than harm.

The Staff of Restoration is yours. Use it wisely, for it amplifies not just healing magic, but the pure intentions
of its wielder."

A brilliant staff materializes in her hands and she offers it to you.

You received the {Fore.WHITE}Staff of Restoration{Style.RESET_ALL}!

{Fore.CYAN}Healer Serenity:{Style.RESET_ALL} "When you face the ultimate darkness, remember this moment. 
Remember that even the most corrupted soul can be saved if someone is willing to try.
Go now, with the blessings of all who have been healed by compassion."

The sanctuary glows with warm, healing light as every creature within bows in respect.""",
                    "min_level": 40,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Holy Water" in self.player.quest_items,
                    "reward": {"type": "weapon", "name": "Staff of Restoration"},
                    "next_event": "sanctuary_complete"
                }
            ],
            "Library of Ages": [
                {
                    "id": "library_1",
                    "text": f"""You enter the vast Library of Ages, where knowledge from across time and space is preserved.
An elderly scholar with eyes like starlight looks up from an ancient tome.

{Fore.MAGENTA}Scholar Wisdom:{Style.RESET_ALL} "Ah, a seeker of knowledge. But what kind of knowledge do you seek?
Power? Glory? Or perhaps... understanding?

I have spent millennia studying the nature of good and evil, light and shadow. 
The Sword of Truth that you seek can only be wielded by one who understands the deepest mysteries.

Answer me this: What is the source of true darkness?"

The scholar waits patiently for your response, surrounded by floating books and scrolls.""",
                    "min_level": 34,
                    "condition": lambda: self.player and hasattr(self.player, 'quest_items') and 
                                       "Scroll of Celestial Weapons" in self.player.quest_items,
                    "next_event": "library_2"
                },
                {
                    "id": "library_2",
                    "text": f"""Scholar Wisdom nods thoughtfully at your answer.

{Fore.MAGENTA}Scholar Wisdom:{Style.RESET_ALL} "Interesting perspective. Now, another question:
If you had the power to destroy all evil instantly, but it would also destroy the free will of every being,
would you do it?"

Books around the library rustle as if blown by an invisible wind.

{Fore.MAGENTA}Scholar Wisdom:{Style.RESET_ALL} "The Sword of Truth reveals not just falsehood, but the complex nature
of reality itself. Good and evil, light and shadow - they are not always as clear-cut as they seem.

One more question: What gives a person the right to judge others?"

The ancient scholar's eyes seem to pierce through to your very soul.""",
                    "min_level": 38,
                    "next_event": "library_3"
                },
                {
                    "id": "library_3",
                    "text": f"""Scholar Wisdom closes the ancient tome and stands.

{Fore.MAGENTA}Scholar Wisdom:{Style.RESET_ALL} "Your answers show wisdom beyond your years. You understand that true judgment
comes not from power, but from compassion and understanding.

The Sword of Truth is not a weapon of destruction, but of revelation. It shows things as they truly are,
cutting through deception and illusion. In the hands of one who seeks understanding rather than vengeance,
it becomes a tool of justice rather than destruction."

A magnificent sword materializes, its blade gleaming with inner light.

You received the {Fore.WHITE}Sword of Truth{Style.RESET_ALL}!

{Fore.MAGENTA}Scholar Wisdom:{Style.RESET_ALL} "Remember this when you face the Sealed Darkness:
It was not always evil. Once, it was simply another being seeking its place in the cosmos.
Perhaps understanding can succeed where force has failed.

Go now, armed with knowledge as much as with weapons. May wisdom guide your path."

The library fills with a soft, eternal light as countless books open to reveal their secrets.""",
                    "min_level": 42,
                    "reward": {"type": "weapon", "name": "Sword of Truth"},
                    "next_event": "library_complete"
                }
            ],
            "Shadow Peak": [
                {
                    "id": "shadow_peak_1",
                    "text": f"""As you approach Shadow Peak's summit, you discover an ancient shrine carved from obsidian.
A mysterious figure cloaked in shadows emerges from behind the shrine.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "Greetings, young trainer. I have been expecting you.
This mountain stands as a gateway between our world and realms beyond understanding.
The shadows grow longer each day, suggesting the ancient balance is disturbed.

Return when you have proven your strength as a trainer. Perhaps then you will be ready for the truth."

The mysterious figure gestures for you to leave, their eyes never leaving the shrine.""",
                    "min_level": 25,
                    "next_event": "shadow_peak_2"
                },
                {
                    "id": "shadow_peak_2",
                    "text": f"""You return to the shrine near Shadow Peak's summit.
The Keeper of Shadows seems to have expected your return.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "You have grown considerably since we last met.
The ancient texts speak of a great darkness sealed away by four elemental guardians.
That seal has protected our world for millennia, but now weakens with each passing day.

Take this Shadow Prism. It allows one to see things hidden by darkness, both physical and metaphorical."

You received a {Fore.MAGENTA}Shadow Prism{Style.RESET_ALL}!

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "The legendary shadow monster, Shadowclaw, is said to appear to those
who face their inner darkness at the Shadowed Altar.

But beware, for as the seal weakens, creatures of pure shadow have begun to emerge.
They seek the four elemental crystals, the keys to either restoring or completely breaking the seal.
I fear dark forces are at work to ensure it's the latter."

The keeper turns back to their silent vigil, a sense of foreboding hanging in the air.""",
                    "min_level": 35,
                    "reward": {"type": "item", "name": "Shadow Prism"},
                    "next_event": "shadow_peak_final"
                }
            ],
            "Volcanic Crater": [
                {
                    "id": "volcanic_crater_1",
                    "text": f"""Deep within the Volcanic Crater, you discover an ancient temple carved into the molten rock.
The air shimmers with intense heat as you approach the entrance.

{Fore.RED}Fire Guardian Pyraxis:{Style.RESET_ALL} "Mortal... you dare enter the sacred flames?
I am the eternal guardian of the volcanic heart, keeper of primordial fire magic.
The molten depths have been disturbed by shadow creatures seeking to corrupt our realm.

If you can prove your courage in the Trial of Flames, I will teach you the ancient art of fire bonding.
Return when your spirit burns as bright as your determination, young one."

The guardian's form flickers like dancing flames as they retreat deeper into the temple.""",
                    "min_level": 20,
                    "next_event": "volcanic_crater_2"
                },
                {
                    "id": "volcanic_crater_2",
                    "text": f"""You return to the Fire Guardian's temple, your monsters showing incredible growth.

{Fore.RED}Fire Guardian Pyraxis:{Style.RESET_ALL} "I sense the flame of determination within you has grown stronger.
The Trial of Flames awaits - but first, take this Ember Amulet. It will protect you from the volcanic energies.

The shadow corruption spreads faster than ever. Ancient seals that have protected our world for millennia grow weak.
Fire monsters across the realm are becoming increasingly agitated, sensing the approaching darkness."

You received an {Fore.RED}Ember Amulet{Style.RESET_ALL}!

{Fore.RED}Fire Guardian Pyraxis:{Style.RESET_ALL} "Legend speaks of the Moltenking, a legendary fire titan that slumbers in the deepest crater.
Only those who master the volcanic trials might awaken this ancient protector.
But beware - dark forces seek to corrupt even the mightiest of fire spirits."

The guardian gestures toward a hidden passage leading deeper into the volcanic depths.""",
                    "min_level": 30,
                    "reward": {"type": "item", "name": "Ember Amulet"},
                    "next_event": "volcanic_crater_3"
                }
            ],
            "Crystal Caverns": [
                {
                    "id": "crystal_caverns_1",
                    "text": f"""The Crystal Caverns sparkle with otherworldly beauty as rainbow light dances off countless gem formations.
In the heart of the cavern, you discover a crystalline figure seated on a throne of pure diamond.

{Fore.CYAN}Crystal Sage Luminara:{Style.RESET_ALL} "Welcome, traveler, to the sacred Crystal Sanctum.
I am the keeper of ancient crystal magic, guardian of the geometric harmonies that maintain balance in our world.

These caverns have existed since the dawn of time, their crystals containing the memories of ages past.
But recently, the harmonic resonance has been disrupted by dark influences from beyond.

Prove your worth by demonstrating harmony with crystal energy, and I shall share the secrets of prismatic power."

The sage's crystalline form refracts light in mesmerizing patterns as she speaks.""",
                    "min_level": 25,
                    "next_event": "crystal_caverns_2"
                },
                {
                    "id": "crystal_caverns_2",
                    "text": f"""Returning to the Crystal Sanctum, you find Crystal Sage Luminara studying a complex array of floating crystals.

{Fore.CYAN}Crystal Sage Luminara:{Style.RESET_ALL} "Your aura has strengthened considerably since our last meeting.
The crystal formations speak of your dedication to the trainer's path.

Accept this Prismatic Lens - it will reveal hidden truths and allow you to see through illusions.
The shadows that threaten our realm often hide behind deception and false visions."

You received a {Fore.CYAN}Prismatic Lens{Style.RESET_ALL}!

{Fore.CYAN}Crystal Sage Luminara:{Style.RESET_ALL} "Deep within these caverns dwells Prismatic, the Rainbow Dragon of infinite facets.
This legendary being holds the power to bend light itself, creating illusions that can confound even gods.

But darker news troubles me - the Crystal Heart, source of all harmonic energy, grows dim.
If the ancient seals fail completely, even the power of pure crystal magic may not be enough to save us."

The sage's expression grows grave as she returns to her mystical calculations.""",
                    "min_level": 35,
                    "reward": {"type": "item", "name": "Prismatic Lens"},
                    "next_event": "crystal_caverns_3"
                }
            ],
            "Haunted Graveyard": [
                {
                    "id": "haunted_graveyard_1",
                    "text": f"""The Haunted Graveyard stretches endlessly before you, shrouded in perpetual mist.
Ancient tombstones bear names worn away by centuries, while ghostly whispers echo through the fog.

{Fore.MAGENTA}Specter Warden Morticus:{Style.RESET_ALL} "Living soul... what brings you to the realm of the departed?
I am the eternal guardian of this sacred ground, keeper of the boundary between life and death.

The restless spirits have been agitated lately. Something stirs in the deeper crypts - something that should remain sealed.
If you possess the courage to face the unknown, perhaps you can help restore peace to this hallowed ground."

The spectral figure's form shifts and wavers like smoke in the moonlight.""",
                    "min_level": 28,
                    "next_event": "haunted_graveyard_2"
                },
                {
                    "id": "haunted_graveyard_2",
                    "text": f"""Returning to the graveyard, you find Specter Warden Morticus standing before an ominous mausoleum.

{Fore.MAGENTA}Specter Warden Morticus:{Style.RESET_ALL} "Your spirit has grown resilient to fear - a necessary trait for what lies ahead.
The ancient crypts contain secrets that predate written history.

Take this Spectral Ward - it will protect you from malevolent spiritual energy.
The darkness that threatens our world has begun corrupting even the realm of the dead."

You received a {Fore.MAGENTA}Spectral Ward{Style.RESET_ALL}!

{Fore.MAGENTA}Specter Warden Morticus:{Style.RESET_ALL} "The Deathwarden, sovereign of the underworld's depths, has sent warnings.
Ancient seals that separate the realms grow weak, allowing shadow creatures to slip between worlds.

If the Great Seal fails completely, the barrier between life and death will shatter.
All existence will be consumed by the Sealed Darkness - an entity of pure void and despair."

The warden's warning carries the weight of cosmic truth as the mist swirls ominously around you.""",
                    "min_level": 38,
                    "reward": {"type": "item", "name": "Spectral Ward"},
                    "next_event": "haunted_graveyard_3"
                }
            ],
            "Sky Islands": [
                {
                    "id": "sky_islands_1",
                    "text": f"""Soaring through the clouds, you land on a floating island where ancient temples touch the very heavens.
The wind carries whispers of forgotten songs as celestial light bathes everything in ethereal beauty.

{Fore.CYAN}Sky Marshal Tempestus:{Style.RESET_ALL} "Greetings, earth-bound traveler who has risen to our celestial realm.
I am the commander of the aerial domains, guardian of the winds and storms.

These sky islands have drifted through the heavens since time immemorial, maintaining the atmospheric balance.
But dark storms now brew from unnatural sources, threatening to corrupt the very air we breathe.

Show me your mastery of aerial combat, and I will teach you the secrets of storm calling."

The sky marshal's cape billows with captured lightning as thunder rumbles in the distance.""",
                    "min_level": 32,
                    "next_event": "sky_islands_2"
                },
                {
                    "id": "sky_islands_2",
                    "text": f"""Returning to the floating temples, you find Sky Marshal Tempestus standing atop the highest spire.

{Fore.CYAN}Sky Marshal Tempestus:{Style.RESET_ALL} "Your aerial prowess has improved dramatically since our last encounter.
The winds themselves sing of your dedication to the trainer's path.

Accept these Stormwing Boots - they will grant you limited flight and protection from lightning.
As the cosmic crisis deepens, mobility across all terrains becomes essential for survival."

You received {Fore.CYAN}Stormwing Boots{Style.RESET_ALL}!

{Fore.CYAN}Sky Marshal Tempestus:{Style.RESET_ALL} "The Stormruler, sovereign of all tempests, prepares for the final battle.
This legendary being commands hurricanes that can reshape continents.

The ancient prophecies speak of a convergence - when all elemental powers must unite.
Without this unity, the Sealed Darkness will consume even the endless sky itself."

The marshal's words are carried away by winds that seem to echo with cosmic significance.""",
                    "min_level": 42,
                    "reward": {"type": "item", "name": "Stormwing Boots"},
                    "next_event": "sky_islands_3"
                }
            ],
            "Neon City": [
                {
                    "id": "neon_city_1",
                    "text": f"""The futuristic Neon City pulses with electric energy as holographic advertisements dance across towering skyscrapers.
In the heart of the technological metropolis, you discover a cybernetic laboratory.

{Fore.YELLOW}Tech Master Voltex:{Style.RESET_ALL} "Welcome to the pinnacle of technological evolution, organic being.
I am the supreme architect of digital consciousness, guardian of the electric realm.

Our city represents the perfect fusion of technology and monster energy.
But viral entities from cyberspace now threaten to corrupt our digital paradise.

Prove your compatibility with advanced technology, and I will upgrade your understanding of electronic warfare."

The tech master's form flickers between human and digital projection.""",
                    "min_level": 35,
                    "next_event": "neon_city_2"
                },
                {
                    "id": "neon_city_2",
                    "text": f"""You return to find Tech Master Voltex interfacing with a massive quantum computer.

{Fore.YELLOW}Tech Master Voltex:{Style.RESET_ALL} "Your bio-electric signature has evolved remarkably.
The quantum matrices recognize your enhanced neural patterns.

Download this Neural Interface - it will allow direct communication with electric monsters.
As reality itself faces deletion, technological adaptation becomes crucial for survival."

You received a {Fore.YELLOW}Neural Interface{Style.RESET_ALL}!

{Fore.YELLOW}Tech Master Voltex:{Style.RESET_ALL} "The legendary Mechagon, apex of artificial evolution, initiates final protocols.
This digital deity possesses computational power beyond organic comprehension.

System scans indicate approaching data corruption on a universal scale.
Only the convergence of all elemental protocols can prevent total system failure."

The tech master's warning glitches momentarily before stabilizing.""",
                    "min_level": 45,
                    "reward": {"type": "item", "name": "Neural Interface"},
                    "next_event": "neon_city_3"
                }
            ],
            "Shadow Realm": [
                {
                    "id": "shadow_realm_1",
                    "text": f"""The Shadow Realm exists in perpetual twilight where reality bends and shifts like living darkness.
Whispers echo from unseen sources as you navigate through the ethereal landscape.

{Fore.MAGENTA}Void Keeper Umbros:{Style.RESET_ALL} "So... a mortal dares enter the realm between realms.
I am the eternal guardian of the shadow dimension, keeper of secrets that mortals fear to know.

This realm serves as a buffer between your world and the Sealed Darkness beyond.
But the barriers weaken daily, allowing corruption to seep through dimensional cracks.

Face your inner darkness and emerge stronger, or be consumed by the void itself."

The keeper's form constantly shifts between solid and shadow.""",
                    "min_level": 40,
                    "next_event": "shadow_realm_2"
                },
                {
                    "id": "shadow_realm_2",
                    "text": f"""Returning to the shadow dimension, you find Void Keeper Umbros emanating increased power.

{Fore.MAGENTA}Void Keeper Umbros:{Style.RESET_ALL} "You have gazed into the abyss and returned unchanged.
Few possess such mental fortitude in the face of infinite darkness.

Claim this Void Crystal - it contains fragments of pure nothingness.
When wielded properly, it can nullify even the darkest of corruptions."

You received a {Fore.MAGENTA}Void Crystal{Style.RESET_ALL}!

{Fore.MAGENTA}Void Keeper Umbros:{Style.RESET_ALL} "The Voidking, emperor of all shadow realms, prepares for dimensional war.
This entity predates creation itself, wielding power over the spaces between existence.

The final convergence approaches. All dimensional barriers collapse simultaneously.
Only the perfect unity of opposing forces can restore cosmic balance."

The keeper's prophecy resonates through dimensions as reality itself trembles.""",
                    "min_level": 48,
                    "reward": {"type": "item", "name": "Void Crystal"},
                    "next_event": "shadow_realm_3"
                }
            ]
        }

        # Check if player has all four crystals and is at Shadow Peak
        # Use hasattr to safely check properties before accessing
        if location == "Shadow Peak" and hasattr(self.player, 'quest_items'):
            # Check for all crystals
            if all(crystal in self.player.quest_items for crystal in ["Forest Crystal", "Fire Crystal", "Water Crystal", "Earth Crystal"]):
                # Check if player has completed Shadow Peak storyline part 2
                if hasattr(self.player, 'story_progress') and self.player.story_progress.get("shadow_peak_2", False):
                    # Award major trainer exp for collecting all crystals (if not already rewarded)
                    if not self.player.story_progress.get("crystals_exp_awarded", False):
                        bonus_exp = 200
                        if self.player.gain_trainer_exp(bonus_exp):
                            print(f"{Fore.GREEN}For collecting all four elemental crystals, you gained {bonus_exp} trainer exp and leveled up to Trainer Level {self.player.trainer_level}!{Style.RESET_ALL}")
                        else:
                            print(f"For collecting all four elemental crystals, you gained {bonus_exp} trainer exp. ({self.player.exp}/{self.player.exp_to_level})")

                        # Mark this bonus as already awarded
                        self.player.story_progress["crystals_exp_awarded"] = True
                        safe_input("\nPress Enter to continue...")

                    self.trigger_final_quest()
                    return True

        # Check if there's a story event for this location
        if location in story_events:
            events = story_events[location]

            # Find the first event that hasn't been completed
            for event in events:
                event_id = event["id"]
                # Skip if this event is already completed
                if hasattr(self.player, 'story_progress') and self.player.story_progress.get(event_id, False):
                    continue

                # Check if player's monsters meet level requirement
                if hasattr(self.player, 'monsters') and self.player.monsters:
                    max_level = max([monster.level for monster in self.player.monsters if monster], default=0)
                    if max_level >= event["min_level"]:
                        # Trigger the story event
                        clear_screen()
                        print(f"{Fore.YELLOW}=== STORY EVENT ==={Style.RESET_ALL}\n")
                        print(event["text"])

                        # Mark this event as completed
                        if not hasattr(self.player, 'story_progress'):
                            self.player.story_progress = {}
                        self.player.story_progress[event_id] = True

                        # Handle rewards
                        if "reward" in event:
                            reward = event["reward"]
                            if reward["type"] == "item" and reward["name"] in self.all_items:
                                # Safety check
                                if hasattr(self.player, 'add_item'):
                                    self.player.add_item(self.all_items[reward["name"]])
                                    print(f"\nYou received a {reward['name']}!")
                            elif reward["type"] == "quest_item":
                                quest_item = reward["name"]

                                # Safety check
                                if not hasattr(self.player, 'quest_items'):
                                    self.player.quest_items = []

                                self.player.quest_items.append(quest_item)
                                print(f"\nYou obtained the {quest_item}!")

                                # Check if all crystals collected
                                crystals = ["Forest Crystal", "Fire Crystal", "Water Crystal", "Earth Crystal"]
                                crystal_count = sum(1 for crystal in crystals if crystal in self.player.quest_items)
                                print(f"\nYou now have {crystal_count}/4 elemental crystals.")

                                if crystal_count == 4:
                                    print(f"\n{Fore.CYAN}You have collected all four elemental crystals!{Style.RESET_ALL}")
                                    print("Perhaps it's time to investigate the Chamber of Sealing mentioned in the ancient texts...")

                                # Award bonus trainer exp for finding a crystal
                                if any(crystal_name in quest_item for crystal_name in ["Crystal", "Prism"]):
                                    bonus_exp = 50
                                    if hasattr(self.player, 'gain_trainer_exp'):
                                        if self.player.gain_trainer_exp(bonus_exp):
                                            print(f"\n{Fore.GREEN}You gained {bonus_exp} trainer exp and leveled up to Trainer Level {self.player.trainer_level}!{Style.RESET_ALL}")
                                            print("Your monsters can now grow to this higher level.")
                                        else:
                                            print(f"\nYou gained {bonus_exp} trainer exp. ({self.player.exp}/{self.player.exp_to_level})")

                    safe_input("\nPress Enter to continue...")
                    return True

        return False

    def trigger_final_quest(self):
        """Trigger the final quest when all crystals are gathered"""
        clear_screen()
        print(f"{Fore.RED}=== THE FINAL SEAL ==={Style.RESET_ALL}\n")
        print(f"""As you approach the summit of Shadow Peak with all four elemental crystals,
the Shadow Prism in your possession begins to glow intensely.

It reveals a hidden doorway in the mountainside that was previously invisible.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "You've gathered all four crystals. Impressive.
Beyond this door lies the Chamber of Sealing, where the great darkness was contained ages ago.
The seal is almost completely broken, and shadow creatures have likely infested the chamber.

You must fight your way to the central altar and place the four crystals in their respective positions.
This will restore the seal and save our world from darkness.

Be warned - the darkness will not yield easily. It may have even taken physical form to stop you.
Your monsters will face their greatest challenge yet."

Do you wish to enter the Chamber of Sealing now?""")

        choice = input(f"\n{Fore.CYAN}Enter the chamber? (y/n): {Style.RESET_ALL}").lower()

        if choice == 'y' or choice == 'yes':
            self.final_battle()
        else:
            print("\nYou decide to prepare further before taking on this challenge.")
            print("Return to Shadow Peak when you're ready to face the final battle.")
            safe_input("\nPress Enter to continue...")

    def final_battle(self):
        """The final battle at the Chamber of Sealing"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        clear_screen()
        print(f"{Fore.RED}=== THE CHAMBER OF SEALING ==={Style.RESET_ALL}\n")
        print("""You enter the ancient chamber, your path illuminated by the glow of the four crystals.
Shadow creatures lurk in the darkness, but scatter as you approach, sensing the power you carry.

As you reach the central altar, a swirling mass of darkness rises from the broken seal in the floor.
It coalesces into a monstrous form - a shadowy dragon with glowing red eyes.""")

        print(f"\n{Fore.RED}The Sealed Darkness has awakened!{Style.RESET_ALL}")
        time.sleep(2)

        # Create the final boss monster
        sealed_darkness = Monster(
            name="Sealed Darkness",
            type_="Shadow",
            base_hp=150,
            base_attack=120,
            base_defense=100,
            base_speed=80,
            moves=[
                Move("Shadow Strike", "Shadow", 80, 0.9, "A powerful strike from the darkness"),
                Move("Void Blast", "Shadow", 100, 0.7, "A blast of pure void energy"),
                Move("Corruption Wave", "Shadow", 70, 1.0, "A wave that corrupts everything it touches"),
                Move("Reality Tear", "Shadow", 120, 0.6, "Tears the fabric of reality itself")
            ],
            description="The ancient darkness that was sealed away ages ago. It seeks to corrupt all monsters and rule the world.",
            level=50
        )

        sealed_darkness.calculate_stats()

        # Start the epic final battle
        self.start_battle(sealed_darkness)

        # Check if player won
        if not self.current_battle and self.player and hasattr(self.player, 'location'):
            # Battle is over and player wasn't transported back to hometown (which happens on loss)
            if self.player.location != "Hometown":
                self.complete_final_quest()

    def complete_final_quest(self):
        """Complete the final quest after defeating the Sealed Darkness"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        clear_screen()
        print(f"{Fore.YELLOW}=== VICTORY ==={Style.RESET_ALL}\n")
        print(f"""With the Sealed Darkness defeated, you quickly place the four elemental crystals
on the altar in their respective positions - Forest, Fire, Water, and Earth.

The crystals begin to glow with intense light, their energies converging to repair the broken seal.
A blinding flash fills the chamber, and when your vision clears, the dark presence is gone.

The Keeper of Shadows enters the chamber, their usually stoic face showing relief and admiration.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "You have done what many thought impossible.
The seal is restored, and the darkness contained once more.
The shadow creatures will fade, and balance will return to our world.

Your name will be remembered among the greatest of heroes. The four guardians - 
Sage Elderleaf, Master Smith Ignis, Swamp Witch Mira, and Professor Artifact - all send their gratitude.

This journey may be over, but I sense your adventures as a monster trainer are just beginning.
Take this as a token of our eternal gratitude."

You received the {Fore.YELLOW}Hero's Medallion{Style.RESET_ALL}!

This special item increases the friendship and growth rate of all your monsters.

You also earned {Fore.GREEN}$5000{Style.RESET_ALL} for saving the world!""")

        # Add rewards to player
        if hasattr(self, 'all_items') and "Hero's Medallion" in self.all_items:
            if hasattr(self.player, 'add_item'):
                self.player.add_item(self.all_items["Hero's Medallion"])

        # Add money reward
        if hasattr(self.player, 'money'):
            self.player.money += 5000

        # Mark the main quest as complete
        if hasattr(self.player, 'story_progress'):
            self.player.story_progress["main_quest_complete"] = True

        print(f"\n{Fore.YELLOW}Congratulations! You've completed the main storyline of World of Monsters!{Style.RESET_ALL}")
        print("You can continue exploring the world, catching monsters, and challenging the championship.")

        safe_input("\nPress Enter to continue...")

    def travel(self):
        """Travel to a different location"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'location'):
            print("Error: Player location not set!")
            safe_input("\nPress Enter to continue...")
            return

        print(f"\nCurrent location: {self.player.location}")
        print("Available locations:")

        if not hasattr(self, 'locations') or not self.locations:
            print("Error: No locations available!")
            safe_input("\nPress Enter to continue...")
            return

        # Location level requirements
        location_requirements = {
            "Hometown": 1,
            "Windy Plains": 5,
            "Mystic Forest": 10,
            "Crystal Cavern": 15,
            "Volcanic Ridge": 20,
            "Misty Swamp": 25,
            "Shadow Peak": 30,
            "Ancient Ruins": 35
        }

        # Display locations with level requirements
        for i, location in enumerate(self.locations):
            if location == self.player.location:
                print(f"{i+1}. {location} (current)")
            else:
                req_level = location_requirements.get(location, 1)
                if self.player.trainer_level >= req_level:
                    print(f"{i+1}. {location}")
                else:
                    print(f"{i+1}. {location} {Fore.RED}(Requires Trainer Level {req_level}){Style.RESET_ALL}")

        try:
            choice = int(safe_input("\nEnter location number (0 to cancel): "))
            if choice == 0:
                return

            if 1 <= choice <= len(self.locations):
                destination = self.locations[choice - 1]

                if destination == self.player.location:
                    print("You're already at that location!")
                    safe_input("\nPress Enter to continue...")
                    return

                # Check level requirement
                req_level = location_requirements.get(destination, 1)
                if self.player.trainer_level < req_level:
                    print(f"{Fore.RED}You need to be at least Trainer Level {req_level} to travel to {destination}.{Style.RESET_ALL}")
                    print(f"Your current Trainer Level is {self.player.trainer_level}.")
                    print("Continue exploring and battling to increase your Trainer Level.")
                    safe_input("\nPress Enter to continue...")
                    return

                print(f"\nTraveling to {destination}...")
                time.sleep(1.5)  # Brief pause for traveling effect
                self.player.location = destination
                print(f"Arrived at {destination}!")
            else:
                print("Invalid location number.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error during travel: {str(e)}")

        safe_input("\nPress Enter to continue...")

    def show_monsters(self, for_fusion=False):
        """Show the player's monsters"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'monsters') or not self.player.monsters:
            print("\nYou don't have any monsters yet!")
            safe_input("\nPress Enter to continue...")
            return

        print(f"\n{Fore.CYAN}=== YOUR MONSTERS ==={Style.RESET_ALL}")
        for i, monster in enumerate(self.player.monsters):
            if not monster:
                continue

            fusion_info = ""
            if hasattr(monster, 'is_fusion') and monster.is_fusion:
                fusion_info = f" {Fore.MAGENTA}[FUSION]{Style.RESET_ALL}"

            if hasattr(self.player, 'active_monster_index') and i == self.player.active_monster_index:
                print(f"\n{i+1}. {monster}{fusion_info} {Fore.YELLOW}(Active){Style.RESET_ALL}")
            else:
                print(f"\n{i+1}. {monster}{fusion_info}")

            # Make sure FUSION_LEVEL_REQUIREMENT is defined
            fusion_level_req = FUSION_LEVEL_REQUIREMENT if 'FUSION_LEVEL_REQUIREMENT' in globals() else 25

            # Show fusion eligibility for fusion menu
            if for_fusion and hasattr(monster, 'level') and monster.level >= fusion_level_req:
                print(f"{Fore.GREEN}✓ Eligible for fusion{Style.RESET_ALL}")
            elif for_fusion:
                print(f"{Fore.RED}✗ Not eligible (needs level {fusion_level_req}+){Style.RESET_ALL}")

        # Skip options if we're just showing monsters for fusion
        if for_fusion:
            return

        # Options for monster management
        print("\nOptions:")
        print("1. Switch active monster")
        print("2. View monster details")
        print("3. Return to main menu")

        try:
            choice = int(safe_input("\nEnter choice: "))

            if choice == 1:
                try:
                    monster_idx = int(safe_input("\nEnter monster number to make active: ")) - 1
                    if 0 <= monster_idx < len(self.player.monsters):
                        monster = self.player.monsters[monster_idx]
                        if not monster:
                            print("Error: Invalid monster selection!")
                        elif hasattr(monster, 'is_fainted') and monster.is_fainted():
                            monster_name = monster.get_colored_name() if hasattr(monster, 'get_colored_name') else "Monster"
                            print(f"{monster_name} has fainted and can't be active!")
                        elif hasattr(self.player, 'switch_active_monster'):
                            self.player.switch_active_monster(monster_idx)
                            monster_name = monster.get_colored_name() if hasattr(monster, 'get_colored_name') else "Monster"
                            print(f"{monster_name} is now your active monster!")
                        else:
                            print("Error: Unable to switch active monster!")
                    else:
                        print("Invalid monster number.")
                except ValueError:
                    print("Please enter a valid number.")
                except Exception as e:
                    print(f"Error while switching monster: {str(e)}")

            elif choice == 2:
                try:
                    monster_idx = int(safe_input("\nEnter monster number to view details: ")) - 1
                    if 0 <= monster_idx < len(self.player.monsters):
                        monster = self.player.monsters[monster_idx]
                        if not monster:
                            print("Error: Invalid monster selection!")
                        else:
                            monster_name = monster.get_colored_name() if hasattr(monster, 'get_colored_name') else "Monster"
                            print(f"\n{Fore.CYAN}=== {monster_name} DETAILS ==={Style.RESET_ALL}")

                            # Display monster attributes with safeguards
                            print(f"Type: {monster.type if hasattr(monster, 'type') else 'Unknown'}")
                            print(f"Level: {monster.level if hasattr(monster, 'level') else 'Unknown'}")

                            if hasattr(monster, 'current_hp') and hasattr(monster, 'max_hp'):
                                print(f"HP: {monster.current_hp}/{monster.max_hp}")
                            else:
                                print("HP: Unknown")

                            print(f"Attack: {monster.attack if hasattr(monster, 'attack') else 'Unknown'}")
                            print(f"Defense: {monster.defense if hasattr(monster, 'defense') else 'Unknown'}")
                            print(f"Speed: {monster.speed if hasattr(monster, 'speed') else 'Unknown'}")

                            if hasattr(monster, 'exp') and hasattr(monster, 'exp_to_level'):
                                print(f"EXP: {monster.exp}/{monster.exp_to_level}")
                            else:
                                print("EXP: Unknown")

                            print("\nMoves:")
                            if hasattr(monster, 'moves') and monster.moves:
                                for i, move in enumerate(monster.moves):
                                    print(f"{i+1}. {move}")
                            else:
                                print("No moves available")

                            print(f"\nDescription: {monster.description if hasattr(monster, 'description') else 'No description available'}")
                    else:
                        print("Invalid monster number.")
                except ValueError:
                    print("Please enter a valid number.")
                except Exception as e:
                    print(f"Error while viewing monster details: {str(e)}")
        except ValueError:
            print("Please enter a valid option.")
        except Exception as e:
            print(f"Error in monster management: {str(e)}")

        safe_input("\nPress Enter to continue...")

    def show_items(self):
        """Show and use the player's inventory items"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            print("\nYour inventory is empty!")
            safe_input("\nPress Enter to continue...")
            return

        print(f"\n{Fore.CYAN}=== YOUR INVENTORY ==={Style.RESET_ALL}")
        try:
            items = list(self.player.inventory.keys())
            for i, item in enumerate(items):
                if not item:
                    continue
                quantity = self.player.inventory[item]
                item_name = item.name if hasattr(item, 'name') else "Unknown Item"
                item_desc = item.description if hasattr(item, 'description') else "No description"
                print(f"{i+1}. {item_name} x{quantity} - {item_desc}")

            # Options for item management
            print("\nOptions:")
            print("1. Use an item")
            print("2. Return to main menu")

            try:
                choice = int(safe_input("\nEnter choice: "))

                if choice == 1:
                    # Can't use items in battle from this menu
                    if self.current_battle:
                        print("You can't use items from the inventory during battle!")
                        print("Use the 'item' command in battle instead.")
                        safe_input("\nPress Enter to continue...")
                        return

                    try:
                        item_idx = int(safe_input("\nEnter item number to use: ")) - 1
                        if 0 <= item_idx < len(items):
                            item = items[item_idx]
                            if not item:
                                print("Error: Invalid item selection!")
                                safe_input("\nPress Enter to continue...")
                                return

                            # Monster Balls can only be used in battle
                            if hasattr(item, 'effect') and item.effect == "catch":
                                print("You can only use Monster Balls during battle!")
                                safe_input("\nPress Enter to continue...")
                                return

                            # Only healing items need a target
                            if hasattr(item, 'effect') and item.effect in ["heal", "revive"]:
                                # Show monsters
                                if not hasattr(self.player, 'monsters') or not self.player.monsters:
                                    print("You don't have any monsters to use this item on!")
                                    safe_input("\nPress Enter to continue...")
                                    return

                                print("\nChoose a monster to use the item on:")
                                for i, monster in enumerate(self.player.monsters):
                                    if not monster:
                                        continue
                                    monster_name = monster.get_colored_name() if hasattr(monster, 'get_colored_name') else "Monster"
                                    hp_info = f"(HP: {monster.current_hp}/{monster.max_hp})" if hasattr(monster, 'current_hp') and hasattr(monster, 'max_hp') else "(HP: ?/?)"
                                    print(f"{i+1}. {monster_name} {hp_info}")

                                try:
                                    monster_idx = int(safe_input("\nEnter monster number: ")) - 1
                                    if 0 <= monster_idx < len(self.player.monsters):
                                        if not hasattr(self.player, 'use_item'):
                                            print("Error: Cannot use items at this time!")
                                        else:
                                            result = self.player.use_item(item_idx, monster_idx)
                                            print(f"\n{result}")
                                    else:
                                        print("Invalid monster number.")
                                except ValueError:
                                    print("Please enter a valid number.")
                                except Exception as e:
                                    print(f"Error using item on monster: {str(e)}")
                            else:
                                # Generic item use
                                if hasattr(self.player, 'use_item'):
                                    try:
                                        result = self.player.use_item(item_idx)
                                        print(f"\n{result}")
                                    except Exception as e:
                                        print(f"Error using item: {str(e)}")
                                else:
                                    print("Error: Cannot use items at this time!")
                        else:
                            print("Invalid item number.")
                    except ValueError:
                        print("Please enter a valid number.")
                    except Exception as e:
                        print(f"Error selecting item: {str(e)}")
            except ValueError:
                print("Please enter a valid option.")
            except Exception as e:
                print(f"Error in item menu: {str(e)}")
        except Exception as e:
            print(f"Error displaying inventory: {str(e)}")

        safe_input("\nPress Enter to continue...")

    def heal_monsters(self):
        """Heal all monsters (only in Hometown)"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'location') or self.player.location != "Hometown":
            print("\nYou can only rest and heal your monsters in your Hometown!")
            safe_input("\nPress Enter to continue...")
            return

        print("\nResting at the Healing Center in your Hometown...")
        time.sleep(1.5)

        # Heal all monsters
        if not hasattr(self.player, 'monsters') or not self.player.monsters:
            print("You don't have any monsters to heal!")
            safe_input("\nPress Enter to continue...")
            return

        try:
            for monster in self.player.monsters:
                if monster and hasattr(monster, 'full_heal'):
                    monster.full_heal()

            print(f"{Fore.GREEN}All your monsters have been fully healed!{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error healing monsters: {str(e)}")

        safe_input("\nPress Enter to continue...")

    def show_help(self):
        """Show game help and instructions"""
        help_text = f"""
{Fore.CYAN}=== WORLD OF MONSTERS - HELP ==={Style.RESET_ALL}

{Fore.YELLOW}MAIN COMMANDS:{Style.RESET_ALL}
- explore or /e: Search the area for items or events
- travel or /t: Move to a different location
- monsters or /m: View and manage your monsters
- items or /i: View and use items in your inventory
- heal: Rest and heal your monsters (only in Hometown)
- save [name] or /s: Save your game progress
- load [name] or /l: Load a saved game
- fusion or /f: Fuse two strong monsters to create a more powerful one
- championship or /c: Challenge the Monster Championship tournament
- puzzle: Solve puzzles to encounter legendary monsters (level 30+ required)
- legendary: Directly challenge a random legendary monster (level 35+ required)
- help or /h: Show this help menu
- quit/exit or /q: Exit the game

{Fore.YELLOW}BATTLE COMMANDS:{Style.RESET_ALL}
- fight <number>: Use a move to attack
- catch: Try to catch the wild monster
- switch <number>: Switch to another monster
- item <number>: Use an item
- run: Try to run away from battle

{Fore.YELLOW}GAME BASICS:{Style.RESET_ALL}
1. Explore different locations to find wild monsters
2. Battle and catch monsters to add to your collection
3. Train your monsters to increase their levels
4. Each monster has a type that affects battle effectiveness:
   - Grass > Water > Fire > Grass
   - Electric is effective against Water
5. Return to Hometown to heal your monsters for free

{Fore.YELLOW}ADVANCED FEATURES:{Style.RESET_ALL}
- Monster Fusion: Combine two monsters (level 25+) to create a stronger monster
- Championship: Battle against elite trainers with your best monsters (level 20+)
- Game Saving: Save your progress and continue later

{Fore.YELLOW}NARRATIVE & SOCIAL FEATURES:{Style.RESET_ALL}
- reflect/reflection: Access deep narrative reflection on your journey
- contemplate: Quick contemplation of recent events and choices
- emotions/bonds: View emotional bonds with monsters and NPC relationships
- talk/dialogue: View available NPCs for conversation in current location
- talk [name]: Start a conversation with a specific NPC

{Fore.YELLOW}MONSTER STATS:{Style.RESET_ALL}
- HP: Health points, when it reaches 0 the monster faints
- Attack: Affects damage dealt
- Defense: Reduces damage taken
- Speed: Determines who goes first in battle

{Fore.YELLOW}TIPS:{Style.RESET_ALL}
- Always have Monster Balls ready for catching wild monsters
- Carry healing items for emergencies
- Consider type matchups when choosing which monster to use
- Remember that your monsters will be fully healed if you lose a battle
"""
        print(help_text)
        try:
            safe_input("\nPress Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            pass

    def quit_game(self):
        """Quit the game with confirmation"""
        confirm = safe_input("\nAre you sure you want to quit? (y/n): ").lower()
        if confirm == 'y' or confirm == 'yes':
            print("\nThank you for playing World of Monsters!")
            self.running = False

    def start_battle(self, wild_monster: Monster):
        """Start a battle with a wild monster"""
        # Check if player exists and has usable monsters
        if not self.player:
            print("No active player found!")
            return

        if not self.player.has_usable_monster():
            print("You don't have any monsters that can battle!")
            safe_input("\nPress Enter to continue...")
            return

        # Switch to first usable monster if active is fainted
        if self.player.active_monster is None or self.player.active_monster.is_fainted():
            idx = self.player.get_first_usable_monster_index()
            if idx >= 0:
                self.player.switch_active_monster(idx)

        # Create and start battle
        clear_screen()
        print(f"\n{Fore.RED}A wild {wild_monster.get_colored_name()} appeared!{Style.RESET_ALL}")
        time.sleep(1)

        self.current_battle = Battle(self.player, wild_monster)

    def start_puzzle(self):
        """Start a puzzle that can lead to legendary monster encounters"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        # Get all legendary monsters with their associated locations, types, and temples
        legendary_info = {
            "Chronodrake": {
                "location": "Ancient Ruins", 
                "type": "Dragon", 
                "color": Fore.LIGHTRED_EX, 
                "temple": "Temple of Time",
                "puzzle_type": "sequence",
                "puzzle_name": "Temporal Riddle",
                "description": "Ancient mechanisms that control the flow of time still function in these ruins. Solve their pattern."
            },
            "Celestius": {
                "location": "Mystic Forest", 
                "type": "Fairy", 
                "color": Fore.LIGHTMAGENTA_EX, 
                "temple": "Celestial Shrine",
                "puzzle_type": "memory",
                "puzzle_name": "Astral Memory",
                "description": "Stars shift into patterns on the ceiling of this ancient observatory. Memorize the celestial alignment."
            },
            "Pyrovern": {
                "location": "Volcanic Ridge", 
                "type": "Fire", 
                "color": Fore.RED, 
                "temple": "Inferno Altar",
                "puzzle_type": "maze",
                "puzzle_name": "Trial of Flames",
                "description": "Navigate through shifting pathways of molten rock to reach the sacred flame at the altar's heart."
            },
            "Gemdrill": {
                "location": "Crystal Cavern", 
                "type": "Rock", 
                "color": Fore.LIGHTBLACK_EX, 
                "temple": "Crystalline Forge",
                "puzzle_type": "matching",
                "puzzle_name": "Crystal Harmony",
                "description": "Crystals of different colors resonate with unique tones. Match them to unlock the sacred chamber."
            },
            "Shadowclaw": {
                "location": "Shadow Peak", 
                "type": "Dark", 
                "color": Fore.BLACK, 
                "temple": "Shadow Sanctum",
                "puzzle_type": "riddle",
                "puzzle_name": "Whispers in Darkness",
                "description": "Echoing whispers speak riddles from the shadows. Answer correctly to be deemed worthy."
            },
            "Tempestus": {
                "location": "Mountain", 
                "type": "Electric", 
                "color": Fore.YELLOW, 
                "temple": "Storm Spire",
                "puzzle_type": "sequence",
                "puzzle_name": "Lightning Code",
                "description": "Lightning strikes in a particular sequence on the mountaintop. Predict the next strike."
            },
            "Terraquake": {
                "location": "Desert Dunes", 
                "type": "Ground", 
                "color": Fore.LIGHTYELLOW_EX, 
                "temple": "Seismic Vault",
                "puzzle_type": "memory",
                "puzzle_name": "Earth's Memory",
                "description": "The ground vibrates in patterns beneath your feet. Feel and remember the sequence."
            },
            "Luminary": {
                "location": "Enchanted Grove", 
                "type": "Psychic", 
                "color": Fore.MAGENTA, 
                "temple": "Luminous Sanctum",
                "puzzle_type": "riddle",
                "puzzle_name": "Enigma of Light",
                "description": "Beams of light form words and symbols on ancient stone tablets. Decipher their meaning."
            }
        }

        # Check if we're at a location that has a specific legendary associated with it
        location = self.player.location
        location_legendaries = [name for name, info in legendary_info.items() 
                              if info["location"] == location and name in self.all_monsters]

        if not location_legendaries:
            print(f"{Fore.YELLOW}There are no legendary temples at {location}.{Style.RESET_ALL}")
            print("Try exploring other areas such as Mystic Forest, Volcanic Ridge, Crystal Cavern, Shadow Peak, or Ancient Ruins.")
            print("Each area may contain a temple dedicated to a different legendary monster.")
            safe_input("\nPress Enter to continue...")
            return

        # Select the legendary for this location
        legendary_name = random.choice(location_legendaries)
        legendary_data = legendary_info[legendary_name]

        # Check if player's monsters are strong enough
        if not any(monster.level >= 30 for monster in self.player.monsters if monster):
            print(f"{Fore.RED}Your monsters aren't strong enough to attempt this challenge.{Style.RESET_ALL}")
            print("Train them to at least level 30 before approaching the temple!")
            safe_input("\nPress Enter to continue...")
            return

        # Create an immersive approach to the temple
        clear_screen()
        temple_name = legendary_data["temple"]
        legendary_color = legendary_data["color"]
        monster_type = legendary_data["type"]

        print(f"{Fore.CYAN}You approach the {legendary_color}{temple_name}{Fore.CYAN}, an ancient structure dedicated")
        print(f"to the legendary {monster_type}-type monster {legendary_color}{legendary_name}{Fore.CYAN}.{Style.RESET_ALL}")
        time.sleep(1.5)

        print(f"\nThe air crackles with {monster_type} energy, and the temple seems to respond to your presence.")
        time.sleep(1.5)

        print("\nInscriptions on the temple wall suggest that only those who can solve")
        print(f"the temple's challenge may be granted an audience with {legendary_color}{legendary_name}{Style.RESET_ALL}.")
        time.sleep(1.5)

        # Ask if the player wants to attempt the puzzle
        print(f"\n{Fore.YELLOW}Will you attempt the challenge of the {temple_name}?{Style.RESET_ALL}")
        choice = safe_input("Enter 'yes' to continue or anything else to leave: ").lower()

        if choice != 'yes' and choice != 'y':
            print("\nYou decide to leave the temple for now. Perhaps you'll return when you're better prepared.")
            safe_input("\nPress Enter to continue...")
            return

        # Start the puzzle
        puzzle_type = legendary_data["puzzle_type"]
        puzzle_name = legendary_data["puzzle_name"]
        puzzle_desc = legendary_data["description"]

        clear_screen()
        print(f"{legendary_color}===== {puzzle_name.upper()} ====={Style.RESET_ALL}\n")
        print(puzzle_desc)
        print(f"\nProve your worth to encounter the legendary {legendary_color}{legendary_name}{Style.RESET_ALL}!")

        # Start the puzzle based on its type
        puzzle_solved = False

        if puzzle_type == 'sequence':
            puzzle_solved = self.sequence_puzzle()
        elif puzzle_type == 'riddle':
            puzzle_solved = self.riddle_puzzle()
        elif puzzle_type == 'matching':
            puzzle_solved = self.matching_puzzle()
        elif puzzle_type == 'memory':
            puzzle_solved = self.memory_puzzle()
        elif puzzle_type == 'maze':
            puzzle_solved = self.maze_puzzle()

        # If puzzle is solved, trigger legendary encounter
        if puzzle_solved:
            clear_screen()
            print(f"{Fore.GREEN}The temple resonates with your success!{Style.RESET_ALL}")
            print("\nThe ground trembles beneath your feet. Ancient mechanisms activate around you...")
            time.sleep(2)

            print(f"\n{legendary_color}The {temple_name} acknowledges your worth.{Style.RESET_ALL}")
            print("A powerful energy surges through the chamber...")
            time.sleep(2)

            # Dramatic reveal of the legendary monster
            print(f"\n{Fore.YELLOW}***********************{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}* LEGENDARY ENCOUNTER *{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}***********************{Style.RESET_ALL}")
            time.sleep(1)

            print(f"\n{legendary_color}The legendary {legendary_name} has appeared before you!{Style.RESET_ALL}")
            safe_input("\nPress Enter to continue...")

            # Trigger encounter with the legendary monster
            if legendary_name in self.all_monsters:
                legendary_monster = self.all_monsters[legendary_name].clone()
                # Ensure the legendary is at a challenging level
                legendary_monster.level = max(40, legendary_monster.level)
                legendary_monster.calculate_stats()

                self.start_battle(legendary_monster)
            else:
                print(f"{Fore.RED}Error: Legendary monster not found!{Style.RESET_ALL}")
                safe_input("\nPress Enter to continue...")
        else:
            print(f"\n{Fore.RED}You failed to solve the puzzle.{Style.RESET_ALL}")
            print(f"The {legendary_color}{temple_name}{Style.RESET_ALL} grows quiet, as if disappointed.")
            print("You can try again later after training more with your monsters.")
            safe_input("\nPress Enter to continue...")

    def sequence_puzzle(self):
        """Puzzle where player needs to identify next number in a sequence"""
        print(f"\n{Fore.CYAN}SEQUENCE PUZZLE{Style.RESET_ALL}")
        print("Identify the next number in the sequence:")

        # Generate random sequence type
        sequence_type = random.choice(["arithmetic", "geometric", "fibonacci"])

        if sequence_type == "arithmetic":
            # Arithmetic sequence (adding a constant)
            diff = random.randint(2, 5)
            start = random.randint(1, 10)
            sequence = [start + i * diff for i in range(5)]
            answer = sequence[4] + diff
        elif sequence_type == "geometric":
            # Geometric sequence (multiplying by a constant)
            ratio = random.randint(2, 3)
            start = random.randint(1, 3)
            sequence = [start * (ratio ** i) for i in range(5)]
            answer = sequence[4] * ratio
        else:
            # Fibonacci-like sequence (each number is sum of two previous)
            a, b = random.randint(1, 5), random.randint(1, 5)
            sequence = [a, b]
            for i in range(3):
                sequence.append(sequence[-1] + sequence[-2])
            answer = sequence[4] + sequence[3]

        # Display the sequence
        print(f"{', '.join(str(num) for num in sequence)}, ?")

        # Get player's answer
        try:
            player_answer = int(safe_input("\nEnter the next number in the sequence: "))
            return player_answer == answer
        except ValueError:
            print("That's not a valid number!")
            return False

    def riddle_puzzle(self):
        """Puzzle where player must answer a riddle"""
        print(f"\n{Fore.CYAN}RIDDLE PUZZLE{Style.RESET_ALL}")
        print("Answer the following riddle:")

        riddles = [
            {"riddle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", 
             "answer": "echo"},
            {"riddle": "The more you take, the more you leave behind. What am I?", 
             "answer": "footsteps"},
            {"riddle": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", 
             "answer": "map"},
            {"riddle": "What has keys but no locks, space but no room, and you can enter but not go in?", 
             "answer": "keyboard"},
            {"riddle": "I'm light as a feather, yet the strongest person can't hold me for more than a few minutes. What am I?", 
             "answer": "breath"}
        ]

        riddle = random.choice(riddles)
        print(f"\n{riddle['riddle']}")

        answer = safe_input("\nYour answer: ").lower().strip()
        return answer == riddle["answer"]

    def matching_puzzle(self):
        """Puzzle where player must match pairs"""
        print(f"\n{Fore.CYAN}MATCHING PUZZLE{Style.RESET_ALL}")
        print("Match each monster type with its strength:")

        types = ["Fire", "Water", "Grass", "Electric", "Ice", "Ground"]
        # Randomly select 4 types for the puzzle
        selected_types = random.sample(types, 4)

        # Create matchings (each type is strong against one other)
        strengths = {
            "Fire": "Grass",
            "Water": "Fire",
            "Grass": "Water",
            "Electric": "Water",
            "Ice": "Grass",
            "Ground": "Electric"
        }

        # Display the types
        for i, type_name in enumerate(selected_types, 1):
            print(f"{i}. {type_name}")

        print("\nPairs (format: 1-3, 2-4, etc.):")
        pairs = safe_input("Enter your pairs: ")

        # Process and check pairs
        try:
            pair_entries = pairs.split(',')
            if len(pair_entries) != 2:  # Must have exactly 2 pairs for 4 types
                return False

            correct_count = 0
            for pair in pair_entries:
                pair = pair.strip()
                a, b = map(int, pair.split('-'))

                # Adjust indices to account for 0-based indexing
                a -= 1
                b -= 1

                type_a = selected_types[a]
                type_b = selected_types[b]

                # Check for strength/weakness relationship
                if strengths.get(type_a) == type_b or strengths.get(type_b) == type_a:
                    correct_count += 1

            return correct_count == 2  # Both pairs must be correct
        except ValueError:
            print("Invalid input format!")
            return False

    def memory_puzzle(self):
        """Puzzle where player must remember a sequence"""
        print(f"\n{Fore.CYAN}MEMORY PUZZLE{Style.RESET_ALL}")
        print("Remember the following sequence of colors:")

        colors = ["Red", "Blue", "Green", "Yellow", "Purple"]
        # Generate a random sequence of 5 colors
        sequence = [random.choice(colors) for _ in range(5)]

        # Show the sequence
        for color in sequence:
            print(f"{color}...")
            time.sleep(0.8)
            clear_screen()
            time.sleep(0.3)

        # Wait a bit to make it challenging
        time.sleep(1)

        # Ask player to recall the sequence
        print("Enter the color sequence, separated by commas:")
        player_sequence = input().strip()

        # Check if player's answer matches the sequence
        player_colors = [color.strip().capitalize() for color in player_sequence.split(',')]
        return player_colors == sequence

    def maze_puzzle(self):
        """Puzzle where player navigates a text-based maze"""
        print(f"\n{Fore.CYAN}MAZE PUZZLE{Style.RESET_ALL}")
        print("Navigate through the maze to find the exit.")
        print("Commands: n (north), s (south), e (east), w (west)")

        # Define a simple maze as a dictionary where each key is a position
        # and the value is a dictionary of possible moves and where they lead
        maze = {
            "start": {"description": "You are at the entrance of a dark maze.", "exits": {"n": "room1", "e": "room2"}},
            "room1": {"description": "A dimly lit corridor stretches before you.", "exits": {"s": "start", "e": "room3"}},
            "room2": {"description": "The walls are covered in strange symbols.", "exits": {"w": "start", "n": "room4"}},
            "room3": {"description": "You hear water dripping somewhere nearby.", "exits": {"w": "room1", "s": "room4"}},
            "room4": {"description": "A cool breeze suggests an exit is near.", "exits": {"s": "room2", "e": "room5"}},
            "room5": {"description": "You see a glowing crystal on a pedestal.", "exits": {"n": "exit", "w": "room4"}}
        }

        current_room = "start"
        moves = 0
        max_moves = 12

        while moves < max_moves and current_room != "exit":
            room = maze[current_room]
            print(f"\n{room['description']}")

            # Show available directions
            exits = room["exits"]
            directions = ", ".join(exits.keys())
            print(f"Available directions: {directions}")
            print(f"Moves taken: {moves}/{max_moves}")

            # Get player's move
            move = safe_input("Which way do you go? ").lower().strip()

            if move in exits:
                current_room = exits[move]
                moves += 1
            else:
                print("You can't go that way!")

        return current_room == "exit"

    def legendary_encounter(self):
        """Trigger a random legendary monster encounter"""
        if not self.player:
            print("Error: No active player!")
            safe_input("\nPress Enter to continue...")
            return

        # Check if player has strong enough monsters for a legendary encounter
        if not any(monster.level >= 35 for monster in self.player.monsters if monster):
            print(f"{Fore.RED}Your monsters aren't strong enough for legendary encounters.{Style.RESET_ALL}")
            print("Train them to at least level 35 first!")
            safe_input("\nPress Enter to continue...")
            return

        # Get all legendary monsters with their associated locations, types and descriptions
        legendary_info = {
            "Chronodrake": {
                "location": "Ancient Ruins", 
                "type": "Dragon", 
                "color": Fore.LIGHTRED_EX, 
                "temple": "Temple of Time",
                "description": "A massive dragon with scales that shimmer with temporal energy. Its wings seem to phase in and out of reality."
            },
            "Celestius": {
                "location": "Sky Tower", 
                "type": "Fairy", 
                "color": Fore.LIGHTMAGENTA_EX, 
                "temple": "Celestial Shrine",
                "description": "A celestial being surrounded by tiny stars. Its body radiates with cosmic light that bathes the area in a warm glow."
            },
            "Pyrovern": {
                "location": "Volcanic Ridge", 
                "type": "Fire", 
                "color": Fore.RED, 
                "temple": "Inferno Altar",
                "description": "A beast of living flame and molten rock. Heat waves distort the air around its massive form."
            },
            "Gemdrill": {
                "location": "Crystal Cavern", 
                "type": "Rock", 
                "color": Fore.LIGHTBLACK_EX, 
                "temple": "Crystalline Forge",
                "description": "A crystalline creature with a drill-like horn that gleams with perfect facets. Its body seems to be formed from rare gemstones."
            },
            "Shadowclaw": {
                "location": "Ancient Labyrinth", 
                "type": "Dark", 
                "color": Fore.BLACK, 
                "temple": "Shadow Sanctum",
                "description": "A predator that seems to be formed from living shadow. Its red eyes are the only distinct features in its ever-shifting form."
            },
            "Tempestus": {
                "location": "Mountain", 
                "type": "Electric", 
                "color": Fore.YELLOW, 
                "temple": "Storm Spire",
                "description": "A creature of pure lightning and storm energy. Its body crackles with electricity, and thunder follows its movements."
            },
            "Terraquake": {
                "location": "Desert Dunes", 
                "type": "Ground", 
                "color": Fore.LIGHTYELLOW_EX, 
                "temple": "Seismic Vault",
                "description": "A massive earth elemental with a body formed from compressed stone and precious metals. The ground trembles with each step."
            },
            "Luminary": {
                "location": "Enchanted Grove", 
                "type": "Psychic", 
                "color": Fore.MAGENTA, 
                "temple": "Luminous Sanctum",
                "description": "A being of pure mental energy, with a glowing form that pulses with psychic power. Ancient wisdom seems to emanate from its presence."
            }
        }

        # Check which legendaries are in the game data
        available_legendaries = [name for name in legendary_info.keys() if name in self.all_monsters]

        if not available_legendaries:
            print(f"{Fore.RED}No legendary monsters are available in the game data.{Style.RESET_ALL}")
            safe_input("\nPress Enter to continue...")
            return

        # Check if we're at a location that has a specific legendary associated with it
        location_specific_legendaries = [name for name, info in legendary_info.items() 
                                       if info["location"] == self.player.location and name in available_legendaries]

        # Either choose a location-specific legendary or a random one
        if location_specific_legendaries and random.random() < 0.7:  # 70% chance to get the location-specific legendary
            legendary_name = random.choice(location_specific_legendaries)
        else:
            legendary_name = random.choice(available_legendaries)

        # Get the legendary monster's info
        legendary_info_data = legendary_info[legendary_name]
        legendary_color = legendary_info_data["color"]
        legendary_type = legendary_info_data["type"]
        legendary_temple = legendary_info_data["temple"]
        legendary_monster = self.all_monsters[legendary_name].clone()

        # Ensure it's a high level for challenge
        legendary_monster.level = max(40, legendary_monster.level)
        legendary_monster.calculate_stats()

        # Create a dramatic encounter
        clear_screen()
        print(f"{Fore.YELLOW}===== LEGENDARY ENCOUNTER ====={Style.RESET_ALL}\n")

        # Set the stage based on the monster type
        type_environment = {
            "Dragon": "The air becomes charged with ancient power...",
            "Fairy": "Motes of light begin to swirl around you...",
            "Fire": "The temperature rises dramatically, making the air shimmer with heat...",
            "Rock": "The ground beneath you crystallizes into geometric patterns...",
            "Dark": "Shadows deepen and converge, as light seems to be absorbed from the area...",
            "Electric": "The hair on your arms stands on end as static electricity fills the air...",
            "Ground": "The earth rumbles and shifts beneath your feet...",
            "Psychic": "Your mind fills with whispers and your vision blurs momentarily..."
        }

    # ==================== NEW RPG ENHANCEMENT METHODS ====================

    def show_detailed_stats(self):
        """Show detailed player and game statistics"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         DETAILED STATISTICS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Player stats
        print(f"{Fore.YELLOW}Player: {self.player.name}")
        print(f"Trainer Level: {self.player.trainer_level}")
        print(f"Current Location: {self.player.current_location}")
        print(f"Tokens: {self.player.tokens}")
        print(f"Total Playtime: {getattr(self.player, 'playtime', 0)} minutes")
        print()

        # Monster collection stats
        print(f"{Fore.GREEN}Collection Statistics:")
        print(f"Total Monsters: {len(self.player.monsters)}")
        print(f"Monster Inventory: {len(self.player.inventory)}")

        # Type distribution
        type_counts = {}
        for monster in self.player.monsters:
            type_counts[monster.type] = type_counts.get(monster.type, 0) + 1

        print(f"\n{Fore.BLUE}Monster Types in Collection:")
        for monster_type, count in sorted(type_counts.items()):
            print(f"  {monster_type}: {count}")

        # Level distribution
        level_ranges = {"1-10": 0, "11-20": 0, "21-30": 0, "31-40": 0, "41-50": 0}
        for monster in self.player.monsters:
            if monster.level <= 10:
                level_ranges["1-10"] += 1
            elif monster.level <= 20:
                level_ranges["11-20"] += 1
            elif monster.level <= 30:
                level_ranges["21-30"] += 1
            elif monster.level <= 40:
                level_ranges["31-40"] += 1
            else:
                level_ranges["41-50"] += 1

        print(f"\n{Fore.MAGENTA}Level Distribution:")
        for range_name, count in level_ranges.items():
            print(f"  Level {range_name}: {count}")

        # Battle statistics
        wins = getattr(self.player, 'battle_wins', 0)
        losses = getattr(self.player, 'battle_losses', 0)
        total_battles = wins + losses
        win_rate = (wins / total_battles * 100) if total_battles > 0 else 0

        print(f"\n{Fore.RED}Battle Statistics:")
        print(f"  Total Battles: {total_battles}")
        print(f"  Wins: {wins}")
        print(f"  Losses: {losses}")
        print(f"  Win Rate: {win_rate:.1f}%")

        safe_input("\nPress Enter to continue...")

    def show_skills_menu(self):
        """Show and manage player skills"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}           SKILLS MENU")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize skills if they don't exist
        if not hasattr(self.player, 'skills'):
            self.player.skills = {
                'Monster Training': 1,
                'Battle Strategy': 1,
                'Monster Care': 1,
                'Exploration': 1,
                'Monster Catching': 1,
                'Item Crafting': 1,
                'Trading': 1,
                'Research': 1
            }

        if not hasattr(self.player, 'skill_points'):
            self.player.skill_points = 3

        print(f"{Fore.YELLOW}Available Skill Points: {self.player.skill_points}")
        print(f"{Fore.GREEN}Current Skills:")
        print()

        skill_descriptions = {
            'Monster Training': 'Increases monster XP gain',
            'Battle Strategy': 'Improves critical hit chance',
            'Monster Care': 'Reduces monster healing costs',
            'Exploration': 'Increases rare encounter chance',
            'Monster Catching': 'Improves catch rate',
            'Item Crafting': 'Unlocks better item recipes',
            'Trading': 'Gets better prices from NPCs',
            'Research': 'Unlocks advanced monster info'
        }

        for i, (skill, level) in enumerate(self.player.skills.items(), 1):
            description = skill_descriptions.get(skill, 'Unknown skill')
            print(f"{i}. {skill}: Level {level} - {description}")

        print(f"\n{Fore.CYAN}Options:")
        print("u - Upgrade a skill (costs 1 skill point)")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'u' and self.player.skill_points > 0:
            try:
                skill_num = int(safe_input("Enter skill number to upgrade: ")) - 1
                skills_list = list(self.player.skills.keys())
                if 0 <= skill_num < len(skills_list):
                    skill_name = skills_list[skill_num]
                    if self.player.skills[skill_name] < 10:
                        self.player.skills[skill_name] += 1
                        self.player.skill_points -= 1
                        print(f"\n{Fore.GREEN}{skill_name} upgraded to level {self.player.skills[skill_name]}!")
                    else:
                        print(f"\n{Fore.RED}{skill_name} is already at maximum level!")
                else:
                    print(f"\n{Fore.RED}Invalid skill number!")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number!")
            safe_input("Press Enter to continue...")
        elif choice == 'u':
            print(f"\n{Fore.RED}You don't have any skill points!")
            safe_input("Press Enter to continue...")

    def show_equipment_menu(self):
        """Show and manage player equipment"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         EQUIPMENT MENU")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize equipment if it doesn't exist
        if not hasattr(self.player, 'equipment'):
            self.player.equipment = {
                'weapon': None,
                'armor': None,
                'accessory': None,
                'tool': None
            }

        # Display current equipment
        print(f"{Fore.YELLOW}Current Equipment:")
        equipment_slots = {
            'weapon': 'Weapon',
            'armor': 'Armor',
            'accessory': 'Accessory',
            'tool': 'Tool'
        }

        for slot, name in equipment_slots.items():
            equipped = self.player.equipment.get(slot)
            if equipped:
                print(f"  {name}: {equipped['name']} (+{equipped['bonus']} {equipped['stat']})")
            else:
                print(f"  {name}: None equipped")

        # Show available equipment
        available_equipment = [
            {'name': 'Training Gloves', 'type': 'weapon', 'bonus': 5, 'stat': 'Attack', 'cost': 100},
            {'name': 'Monster Vest', 'type': 'armor', 'bonus': 10, 'stat': 'Defense', 'cost': 150},
            {'name': 'Lucky Charm', 'type': 'accessory', 'bonus': 3, 'stat': 'Catch Rate', 'cost': 200},
            {'name': 'Explorer Kit', 'type': 'tool', 'bonus': 5, 'stat': 'Exploration', 'cost': 120},
            {'name': 'Power Gauntlets', 'type': 'weapon', 'bonus': 10, 'stat': 'Attack', 'cost': 300},
            {'name': 'Guardian Shield', 'type': 'armor', 'bonus': 15, 'stat': 'Defense', 'cost': 350},
            {'name': 'Master Ball Belt', 'type': 'accessory', 'bonus': 8, 'stat': 'Catch Rate', 'cost': 500}
        ]

        print(f"\n{Fore.GREEN}Available Equipment:")
        for i, item in enumerate(available_equipment, 1):
            print(f"{i}. {item['name']} ({item['type']}) - +{item['bonus']} {item['stat']} - {item['cost']} tokens")

        print(f"\n{Fore.CYAN}Options:")
        print("e - Equip item")
        print("u - Unequip item")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'e':
            try:
                item_num = int(safe_input("Enter equipment number to purchase and equip: ")) - 1
                if 0 <= item_num < len(available_equipment):
                    item = available_equipment[item_num]
                    if self.player.tokens >= item['cost']:
                        self.player.tokens -= item['cost']
                        self.player.equipment[item['type']] = {
                            'name': item['name'],
                            'bonus': item['bonus'],
                            'stat': item['stat']
                        }
                        print(f"\n{Fore.GREEN}{item['name']} equipped!")
                    else:
                        print(f"\n{Fore.RED}Not enough tokens! Need {item['cost']}, have {self.player.tokens}")
                else:
                    print(f"\n{Fore.RED}Invalid item number!")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number!")
            safe_input("Press Enter to continue...")
        elif choice == 'u':
            slot = safe_input("Enter slot to unequip (weapon/armor/accessory/tool): ").lower()
            if slot in self.player.equipment:
                if self.player.equipment[slot] is not None:
                    print(f"\n{Fore.YELLOW}{self.player.equipment[slot]['name']} unequipped!")
                    self.player.equipment[slot] = None
                else:
                    print(f"\n{Fore.RED}No equipment in that slot!")
            else:
                print(f"\n{Fore.RED}Invalid slot name!")
            safe_input("Press Enter to continue...")

    def show_crafting_menu(self):
        """Show crafting system for items and equipment"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         CRAFTING MENU")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize crafting materials if they don't exist
        if not hasattr(self.player, 'materials'):
            self.player.materials = {
                'Monster Essence': 0,
                'Crystal Shards': 0,
                'Metal Ore': 0,
                'Ancient Bones': 0,
                'Mystic Herbs': 0
            }

        print(f"{Fore.YELLOW}Crafting Materials:")
        for material, count in self.player.materials.items():
            print(f"  {material}: {count}")

        # Crafting recipes
        recipes = {
            'Super Heal Potion': {
                'materials': {'Mystic Herbs': 3, 'Crystal Shards': 1},
                'result': 'Super Heal Potion',
                'description': 'Fully heals one monster'
            },
            'Monster Ball Plus': {
                'materials': {'Metal Ore': 2, 'Crystal Shards': 2},
                'result': 'Monster Ball Plus',
                'description': 'Higher catch rate than normal balls'
            },
            'Experience Booster': {
                'materials': {'Monster Essence': 5, 'Ancient Bones': 1},
                'result': 'Experience Booster',
                'description': 'Doubles XP gain for next battle'
            },
            'Fusion Catalyst': {
                'materials': {'Monster Essence': 10, 'Crystal Shards': 5, 'Ancient Bones': 2},
                'result': 'Fusion Catalyst',
                'description': 'Allows fusion without level requirement'
            }
        }

        print(f"\n{Fore.GREEN}Available Recipes:")
        for i, (name, recipe) in enumerate(recipes.items(), 1):
            print(f"{i}. {name} - {recipe['description']}")
            materials_str = ", ".join([f"{count} {material}" for material, count in recipe['materials'].items()])
            print(f"   Materials: {materials_str}")

        print(f"\n{Fore.CYAN}Options:")
        print("c - Craft item")
        print("g - Gather materials (explore to find)")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'c':
            try:
                recipe_num = int(safe_input("Enter recipe number to craft: ")) - 1
                recipe_names = list(recipes.keys())
                if 0 <= recipe_num < len(recipe_names):
                    recipe_name = recipe_names[recipe_num]
                    recipe = recipes[recipe_name]

                    # Check if player has enough materials
                    can_craft = True
                    for material, needed in recipe['materials'].items():
                        if self.player.materials.get(material, 0) < needed:
                            can_craft = False
                            break

                    if can_craft:
                        # Consume materials
                        for material, needed in recipe['materials'].items():
                            self.player.materials[material] -= needed

                        # Add crafted item to inventory
                        crafted_item = Item(recipe['result'], recipe['description'], 'consumable', 0)
                        self.player.add_item(crafted_item, 1)
                        print(f"\n{Fore.GREEN}{recipe['result']} crafted successfully!")
                    else:
                        print(f"\n{Fore.RED}Not enough materials!")
                else:
                    print(f"\n{Fore.RED}Invalid recipe number!")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number!")
            safe_input("Press Enter to continue...")
        elif choice == 'g':
            # Gather materials
            material_types = list(self.player.materials.keys())
            found_material = random.choice(material_types)
            amount = random.randint(1, 3)
            self.player.materials[found_material] += amount
            print(f"\n{Fore.GREEN}Found {amount} {found_material}!")
            safe_input("Press Enter to continue...")

    def show_training_menu(self):
        """Show monster training facilities"""
        if not self.player:
            print("No active player found!")
            return

        if not self.player.monsters:
            print("You need monsters to train!")
            safe_input("Press Enter to continue...")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}        TRAINING FACILITIES")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        training_options = {
            'Basic Training': {'cost': 50, 'xp': 100, 'description': 'Basic XP training'},
            'Advanced Training': {'cost': 150, 'xp': 300, 'description': 'Advanced XP training'},
            'Elite Training': {'cost': 300, 'xp': 600, 'description': 'Elite XP training'},
            'Stat Boost': {'cost': 200, 'xp': 0, 'description': 'Temporarily boost monster stats'},
            'Move Training': {'cost': 100, 'xp': 0, 'description': 'Teach new moves to monsters'}
        }

        print(f"{Fore.YELLOW}Available Training:")
        for i, (name, details) in enumerate(training_options.items(), 1):
            print(f"{i}. {name} - {details['description']} - {details['cost']} tokens")

        print(f"\n{Fore.GREEN}Your Monsters:")
        for i, monster in enumerate(self.player.monsters, 1):
            status = "Fainted" if monster.is_fainted() else "Healthy"
            print(f"{i}. {monster.name} (Lv.{monster.level}) - {status}")

        print(f"\n{Fore.CYAN}Tokens: {self.player.tokens}")

        try:
            training_choice = int(safe_input("\nSelect training type (1-5): ")) - 1
            monster_choice = int(safe_input("Select monster to train: ")) - 1

            if 0 <= training_choice < len(training_options) and 0 <= monster_choice < len(self.player.monsters):
                training_name = list(training_options.keys())[training_choice]
                training = training_options[training_name]
                monster = self.player.monsters[monster_choice]

                if self.player.tokens >= training['cost']:
                    self.player.tokens -= training['cost']

                    if training_name == 'Stat Boost':
                        # Temporarily boost stats
                        monster.base_attack = int(monster.base_attack * 1.2)
                        monster.base_defense = int(monster.base_defense * 1.2)
                        monster.base_speed = int(monster.base_speed * 1.2)
                        monster.calculate_stats()
                        print(f"\n{Fore.GREEN}{monster.name}'s stats have been boosted!")
                    elif training_name == 'Move Training':
                        # Add a random powerful move
                        new_moves = [
                            Move("Power Strike", "Normal", 120, 0.9, "A devastating physical attack"),
                            Move("Elemental Burst", "Fire", 110, 0.85, "Unleashes elemental energy"),
                            Move("Mystic Shield", "Psychic", 0, 1.0, "Protects from next attack")
                        ]
                        new_move = random.choice(new_moves)
                        if len(monster.moves) < 6:
                            monster.moves.append(new_move)
                            print(f"\n{Fore.GREEN}{monster.name} learned {new_move.name}!")
                        else:
                            print(f"\n{Fore.YELLOW}{monster.name} already knows too many moves!")
                    else:
                        # XP training
                        monster.gain_exp(training['xp'])
                        print(f"\n{Fore.GREEN}{monster.name} gained {training['xp']} XP!")
                else:
                    print(f"\n{Fore.RED}Not enough tokens! Need {training['cost']}, have {self.player.tokens}")
            else:
                print(f"\n{Fore.RED}Invalid selection!")
        except ValueError:
            print(f"\n{Fore.RED}Please enter valid numbers!")

        safe_input("Press Enter to continue...")

    def show_shop_menu(self):
        """Enhanced shop with more items and services"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}           MONSTER SHOP")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        shop_items = {
            'Monster Ball': {'cost': 10, 'description': 'Basic monster catching device'},
            'Heal Potion': {'cost': 25, 'description': 'Restores 50 HP to one monster'},
            'Super Heal Potion': {'cost': 60, 'description': 'Fully heals one monster'},
            'Experience Candy': {'cost': 100, 'description': 'Gives 200 XP to one monster'},
            'Rare Candy': {'cost': 300, 'description': 'Instantly levels up one monster'},
            'Monster Ball Plus': {'cost': 35, 'description': 'Enhanced catching device'},
            'Revival Herb': {'cost': 150, 'description': 'Revives a fainted monster'},
            'Power Boost': {'cost': 200, 'description': 'Permanently increases attack by 5'},
            'Defense Boost': {'cost': 200, 'description': 'Permanently increases defense by 5'},
            'Speed Boost': {'cost': 200, 'description': 'Permanently increases speed by 5'},
            'Mystery Box': {'cost': 500, 'description': 'Contains a random rare item'},
            'Legendary Tracker': {'cost': 1000, 'description': 'Increases legendary encounter chance'}
        }

        print(f"{Fore.YELLOW}Available Items:")
        for i, (name, details) in enumerate(shop_items.items(), 1):
            print(f"{i}. {name} - {details['description']} - {details['cost']} tokens")

        print(f"\n{Fore.GREEN}Your Tokens: {self.player.tokens}")
        print(f"Inventory Space: {len(self.player.inventory)}/{MAX_INVENTORY_SIZE}")

        print(f"\n{Fore.CYAN}Options:")
        print("b - Buy item")
        print("s - Sell items")
        print("back - Return to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'b':
            try:
                item_num = int(safe_input("Enter item number to buy: ")) - 1
                item_names = list(shop_items.keys())
                if 0 <= item_num < len(item_names):
                    item_name = item_names[item_num]
                    item_details = shop_items[item_name]

                    if self.player.tokens >= item_details['cost']:
                        if len(self.player.inventory) < MAX_INVENTORY_SIZE:
                            self.player.tokens -= item_details['cost']
                            new_item = Item(item_name, item_details['description'], 'consumable', item_details['cost'])
                            self.player.add_item(new_item, 1)
                            print(f"\n{Fore.GREEN}Purchased {item_name}!")
                        else:
                            print(f"\n{Fore.RED}Inventory is full!")
                    else:
                        print(f"\n{Fore.RED}Not enough tokens! Need {item_details['cost']}, have {self.player.tokens}")
                else:
                    print(f"\n{Fore.RED}Invalid item number!")
            except ValueError:
                print(f"\n{Fore.RED}Please enter a valid number!")
            safe_input("Press Enter to continue...")
        elif choice == 's':
            if self.player.inventory:
                print(f"\n{Fore.YELLOW}Your Items:")
                inventory_items = list(self.player.inventory.keys())
                for i, item in enumerate(inventory_items, 1):
                    quantity = self.player.inventory[item]
                    sell_price = item.value // 2
                    print(f"{i}. {item.name} (x{quantity}) - Sell for {sell_price} tokens each")

                try:
                    sell_num = int(safe_input("Enter item number to sell: ")) - 1
                    if 0 <= sell_num < len(inventory_items):
                        item = inventory_items[sell_num]
                        sell_price = item.value // 2
                        self.player.tokens += sell_price
                        
                        # Remove one item from inventory
                        if self.player.inventory[item] > 1:
                            self.player.inventory[item] -= 1
                        else:
                            del self.player.inventory[item]
                            
                        print(f"\n{Fore.GREEN}Sold {item.name} for {sell_price} tokens!")
                    else:
                        print(f"\n{Fore.RED}Invalid item number!")
                except ValueError:
                    print(f"\n{Fore.RED}Please enter a valid number!")
            else:
                print(f"\n{Fore.YELLOW}No items to sell!")
            safe_input("Press Enter to continue...")

    def show_guild_menu(self):
        """Show guild system for cooperative gameplay"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}           GUILD SYSTEM")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize guild info if it doesn't exist
        if not hasattr(self.player, 'guild'):
            self.player.guild = None
        if not hasattr(self.player, 'guild_rank'):
            self.player.guild_rank = 'Member'
        if not hasattr(self.player, 'guild_contribution'):
            self.player.guild_contribution = 0

        available_guilds = [
            {'name': 'Fire Masters', 'focus': 'Fire-type monsters', 'bonus': 'Fire XP +20%'},
            {'name': 'Water Guardians', 'focus': 'Water-type monsters', 'bonus': 'Water XP +20%'},
            {'name': 'Earth Defenders', 'focus': 'Ground/Rock monsters', 'bonus': 'Defense +10%'},
            {'name': 'Sky Riders', 'focus': 'Flying monsters', 'bonus': 'Speed +15%'},
            {'name': 'Shadow Hunters', 'focus': 'Dark monsters', 'bonus': 'Critical Rate +10%'},
            {'name': 'Crystal Seekers', 'focus': 'Rare variants', 'bonus': 'Rare Find +25%'}
        ]

        if self.player.guild:
            print(f"{Fore.YELLOW}Current Guild: {self.player.guild}")
            print(f"Rank: {self.player.guild_rank}")
            print(f"Contribution Points: {self.player.guild_contribution}")

            print(f"\n{Fore.GREEN}Guild Benefits Active:")
            for guild in available_guilds:
                if guild['name'] == self.player.guild:
                    print(f"  {guild['bonus']}")
                    break

            print(f"\n{Fore.CYAN}Guild Actions:")
            print("1. Contribute to guild (costs 100 tokens)")
            print("2. Leave guild")
            print("3. Check guild rankings")
            print("4. Guild missions")

            choice = safe_input("\nEnter your choice: ")

            if choice == '1':
                if self.player.tokens >= 100:
                    self.player.tokens -= 100
                    self.player.guild_contribution += 10
                    print(f"\n{Fore.GREEN}Contributed to guild! +10 contribution points")

                    # Check for rank promotion
                    if self.player.guild_contribution >= 100 and self.player.guild_rank == 'Member':
                        self.player.guild_rank = 'Senior Member'
                        print(f"{Fore.YELLOW}Promoted to Senior Member!")
                    elif self.player.guild_contribution >= 250 and self.player.guild_rank == 'Senior Member':
                        self.player.guild_rank = 'Guild Officer'
                        print(f"{Fore.YELLOW}Promoted to Guild Officer!")
                else:
                    print(f"\n{Fore.RED}Not enough tokens!")
            elif choice == '2':
                confirm = safe_input("Are you sure you want to leave your guild? (y/n): ").lower()
                if confirm == 'y':
                    self.player.guild = None
                    self.player.guild_rank = 'Member'
                    self.player.guild_contribution = 0
                    print(f"\n{Fore.YELLOW}Left guild!")
            elif choice == '3':
                print(f"\n{Fore.CYAN}Guild Rankings:")
                print("1. Your Guild - 15,420 total contribution")
                print("2. Rival Guild - 14,890 total contribution")
                print("3. Other Guild - 12,350 total contribution")
            elif choice == '4':
                print(f"\n{Fore.YELLOW}Daily Guild Missions:")
                print("1. Catch 5 monsters - Reward: 50 tokens")
                print("2. Win 3 battles - Reward: Guild XP boost")
                print("3. Explore new areas - Reward: Rare materials")
        else:
            print(f"{Fore.YELLOW}You are not in a guild.")
            print(f"\n{Fore.GREEN}Available Guilds:")
            for i, guild in enumerate(available_guilds, 1):
                print(f"{i}. {guild['name']} - {guild['focus']} - Bonus: {guild['bonus']}")

            print(f"\n{Fore.CYAN}Options:")
            print("j - Join a guild")
            print("b - Back to main menu")

            choice = safe_input("\nEnter your choice: ").lower()

            if choice == 'j':
                try:
                    guild_num = int(safe_input("Enter guild number to join: ")) - 1
                    if 0 <= guild_num < len(available_guilds):
                        guild = available_guilds[guild_num]
                        self.player.guild = guild['name']
                        self.player.guild_rank = 'Member'
                        self.player.guild_contribution = 0
                        print(f"\n{Fore.GREEN}Joined {guild['name']}!")
                        print(f"You now have the bonus: {guild['bonus']}")
                    else:
                        print(f"\n{Fore.RED}Invalid guild number!")
                except ValueError:
                    print(f"\n{Fore.RED}Please enter a valid number!")

        safe_input("\nPress Enter to continue...")

    def show_quest_menu(self):
        """Show quest system with various objectives"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}           QUEST SYSTEM")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize quest system if it doesn't exist
        if not hasattr(self.player, 'active_quests'):
            self.player.active_quests = []
        if not hasattr(self.player, 'completed_quests'):
            self.player.completed_quests = []

        available_quests = [
            {
                'id': 'catch_5_monsters',
                'name': 'Monster Collector',
                'description': 'Catch 5 different types of monsters',
                'objective': 'Catch 5 monsters',
                'reward': '200 tokens, 1 skill point',
                'progress': 0,
                'target': 5
            },
            {
                'id': 'win_10_battles',
                'name': 'Battle Master',
                'description': 'Win 10 battles against wild monsters',
                'objective': 'Win 10 battles',
                'reward': '300 tokens, Experience Booster',
                'progress': 0,
                'target': 10
            },
            {
                'id': 'fuse_monster',
                'name': 'Fusion Expert',
                'description': 'Successfully fuse two monsters',
                'objective': 'Fuse 1 monster',
                'reward': '500 tokens, Fusion materials',
                'progress': 0,
                'target': 1
            },
            {
                'id': 'explore_all_areas',
                'name': 'World Explorer',
                'description': 'Visit all available locations',
                'objective': 'Explore all areas',
                'reward': '1000 tokens, Legendary encounter',
                'progress': 0,
                'target': 8
            },
            {
                'id': 'legendary_encounter',
                'name': 'Legend Hunter',
                'description': 'Encounter a legendary monster',
                'objective': 'Find legendary monster',
                'reward': '2000 tokens, Master Ball',
                'progress': 0,
                'target': 1
            }
        ]

        print(f"{Fore.YELLOW}Active Quests:")
        if self.player.active_quests:
            for quest in self.player.active_quests:
                progress_bar = "█" * (quest['progress'] * 10 // quest['target']) + "░" * (10 - (quest['progress'] * 10 // quest['target']))
                print(f"  {quest['name']}: {quest['description']}")
                print(f"    Progress: [{progress_bar}] {quest['progress']}/{quest['target']}")
                print(f"    Reward: {quest['reward']}")
        else:
            print("  No active quests")

        print(f"\n{Fore.GREEN}Available Quests:")
        quest_counter = 1
        for quest in available_quests:
            if quest['id'] not in [q['id'] for q in self.player.active_quests] and quest['id'] not in self.player.completed_quests:
                print(f"{quest_counter}. {quest['name']}: {quest['description']}")
                print(f"   Reward: {quest['reward']}")
                quest_counter += 1

        print(f"\n{Fore.CYAN}Completed Quests: {len(self.player.completed_quests)}")

        print(f"\n{Fore.CYAN}Options:")
        print("a - Accept new quest")
        print("c - Check quest progress")
        print("t - Turn in completed quest")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'a':
            available_new_quests = [q for q in available_quests 
                                  if q['id'] not in [aq['id'] for aq in self.player.active_quests] 
                                  and q['id'] not in self.player.completed_quests]

            if available_new_quests and len(self.player.active_quests) < 3:
                print(f"\n{Fore.YELLOW}Select quest to accept:")
                for i, quest in enumerate(available_new_quests, 1):
                    print(f"{i}. {quest['name']}")

                try:
                    quest_num = int(safe_input("Enter quest number: ")) - 1
                    if 0 <= quest_num < len(available_new_quests):
                        selected_quest = available_new_quests[quest_num].copy()
                        self.player.active_quests.append(selected_quest)
                        print(f"\n{Fore.GREEN}Accepted quest: {selected_quest['name']}")
                    else:
                        print(f"\n{Fore.RED}Invalid quest number!")
                except ValueError:
                    print(f"\n{Fore.RED}Please enter a valid number!")
            elif len(self.player.active_quests) >= 3:
                print(f"\n{Fore.RED}You can only have 3 active quests at once!")
            else:
                print(f"\n{Fore.YELLOW}No new quests available!")
        elif choice == 'c':
            # Update quest progress based on player stats
            for quest in self.player.active_quests:
                if quest['id'] == 'catch_5_monsters':
                    quest['progress'] = min(len(self.player.monsters), quest['target'])
                elif quest['id'] == 'win_10_battles':
                    quest['progress'] = min(getattr(self.player, 'battle_wins', 0), quest['target'])
                elif quest['id'] == 'fuse_monster':
                    fusion_count = sum(1 for monster in self.player.monsters if monster.is_fusion)
                    quest['progress'] = min(fusion_count, quest['target'])
                elif quest['id'] == 'explore_all_areas':
                    visited_areas = getattr(self.player, 'visited_areas', set())
                    quest['progress'] = min(len(visited_areas), quest['target'])
            print(f"\n{Fore.GREEN}Quest progress updated!")
        elif choice == 't':
            completed = []
            for quest in self.player.active_quests:
                if quest['progress'] >= quest['target']:
                    completed.append(quest)

            if completed:
                for quest in completed:
                    print(f"\n{Fore.GREEN}Quest completed: {quest['name']}")
                    print(f"Reward: {quest['reward']}")

                    # Give rewards
                    if 'tokens' in quest['reward']:
                        token_amount = int(quest['reward'].split()[0])
                        self.player.tokens += token_amount
                    if 'skill point' in quest['reward']:
                        if not hasattr(self.player, 'skill_points'):
                            self.player.skill_points = 0
                        self.player.skill_points += 1

                    self.player.completed_quests.append(quest['id'])
                    self.player.active_quests.remove(quest)
            else:
                print(f"\n{Fore.YELLOW}No completed quests to turn in!")

        safe_input("\nPress Enter to continue...")

    def show_achievements(self):
        """Show achievement system"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         ACHIEVEMENTS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize achievements if they don't exist
        if not hasattr(self.player, 'achievements'):
            self.player.achievements = set()

        all_achievements = {
            'first_catch': {'name': 'First Catch', 'description': 'Catch your first monster', 'reward': '50 tokens'},
            'monster_collector': {'name': 'Monster Collector', 'description': 'Catch 10 different monsters', 'reward': '200 tokens'},
            'battle_victor': {'name': 'Battle Victor', 'description': 'Win your first battle', 'reward': '100 tokens'},
            'fusion_master': {'name': 'Fusion Master', 'description': 'Create your first fusion monster', 'reward': '300 tokens'},
            'legendary_tamer': {'name': 'Legendary Tamer', 'description': 'Catch a legendary monster', 'reward': '1000 tokens'},
            'world_explorer': {'name': 'World Explorer', 'description': 'Visit all locations', 'reward': '500 tokens'},
            'rich_trainer': {'name': 'Rich Trainer', 'description': 'Accumulate 5000 tokens', 'reward': 'Special item'},
            'level_master': {'name': 'Level Master', 'description': 'Have a monster reach level 50', 'reward': '750 tokens'},
            'type_specialist': {'name': 'Type Specialist', 'description': 'Have 5 monsters of the same type', 'reward': '400 tokens'},
            'guild_member': {'name': 'Guild Member', 'description': 'Join a guild', 'reward': 'Guild benefits'},
            'quest_hero': {'name': 'Quest Hero', 'description': 'Complete 5 quests', 'reward': '600 tokens'},
            'champion': {'name': 'Champion', 'description': 'Win a championship battle', 'reward': 'Champion title'}
        }

        # Check for new achievements
        newly_unlocked = []

        # Check achievement conditions
        if len(self.player.monsters) >= 1 and 'first_catch' not in self.player.achievements:
            self.player.achievements.add('first_catch')
            newly_unlocked.append('first_catch')

        if len(self.player.monsters) >= 10 and 'monster_collector' not in self.player.achievements:
            self.player.achievements.add('monster_collector')
            newly_unlocked.append('monster_collector')

        if getattr(self.player, 'battle_wins', 0) >= 1 and 'battle_victor' not in self.player.achievements:
            self.player.achievements.add('battle_victor')
            newly_unlocked.append('battle_victor')

        if any(monster.is_fusion for monster in self.player.monsters) and 'fusion_master' not in self.player.achievements:
            self.player.achievements.add('fusion_master')
            newly_unlocked.append('fusion_master')

        if self.player.tokens >= 5000 and 'rich_trainer' not in self.player.achievements:
            self.player.achievements.add('rich_trainer')
            newly_unlocked.append('rich_trainer')

        if any(monster.level >= 50 for monster in self.player.monsters) and 'level_master' not in self.player.achievements:
            self.player.achievements.add('level_master')
            newly_unlocked.append('level_master')

        if hasattr(self.player, 'guild') and self.player.guild and 'guild_member' not in self.player.achievements:
            self.player.achievements.add('guild_member')
            newly_unlocked.append('guild_member')

        # Display newly unlocked achievements
        if newly_unlocked:
            print(f"{Fore.YELLOW}🎉 NEW ACHIEVEMENTS UNLOCKED! 🎉")
            for achievement_id in newly_unlocked:
                achievement = all_achievements[achievement_id]
                print(f"  ⭐ {achievement['name']}: {achievement['description']}")
                print(f"     Reward: {achievement['reward']}")
            print()

        # Display all achievements
        print(f"{Fore.GREEN}Unlocked Achievements ({len(self.player.achievements)}/{len(all_achievements)}):")
        for achievement_id, achievement in all_achievements.items():
            if achievement_id in self.player.achievements:
                print(f"  ✅ {achievement['name']}: {achievement['description']}")
            else:
                print(f"  ❌ {achievement['name']}: {achievement['description']}")

        completion_rate = len(self.player.achievements) / len(all_achievements) * 100
        print(f"\n{Fore.CYAN}Achievement Completion: {completion_rate:.1f}%")

        safe_input("\nPress Enter to continue...")

    def show_leaderboard(self):
        """Show global leaderboards"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         LEADERBOARDS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Sample leaderboard data (in real game this would come from server)
        leaderboards = {
            'Monster Collection': [
                ('DragonMaster', 847),
                ('BeastTamer', 712),
                ('PokéPro', 689),
                ('MonsterKing', 654),
                (self.player.name if self.player else 'You', len(self.player.monsters) if self.player else 0)
            ],
            'Battle Wins': [
                ('BattleQueen', 2341),
                ('FightMaster', 1987),
                ('WarriorX', 1654),
                ('Champion99', 1432),
                (self.player.name if self.player else 'You', getattr(self.player, 'battle_wins', 0) if self.player else 0)
            ],
            'Tokens Earned': [
                ('RichTrainer', 50000),
                ('GoldDigger', 42000),
                ('TokenKing', 38500),
                ('Millionaire', 35000),
                (self.player.name if self.player else 'You', self.player.tokens if self.player else 0)
            ]
        }

        for category, rankings in leaderboards.items():
            print(f"\n{Fore.YELLOW}{category} Leaderboard:")
            sorted_rankings = sorted(rankings, key=lambda x: x[1], reverse=True)

            for i, (name, score) in enumerate(sorted_rankings[:10], 1):
                if self.player and name == self.player.name:
                    print(f"  {Fore.GREEN}{i}. {name}: {score:,} ⭐{Style.RESET_ALL}")
                else:
                    print(f"  {i}. {name}: {score:,}")

        print(f"\n{Fore.CYAN}Compete with trainers worldwide!")
        print("Rankings update daily based on your progress.")

        safe_input("\nPress Enter to continue...")

    def show_weather_system(self):
        """Show dynamic weather affecting gameplay"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         WEATHER SYSTEM")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize weather if it doesn't exist
        if not hasattr(self, 'current_weather'):
            weather_types = ['Sunny', 'Rainy', 'Stormy', 'Foggy', 'Snowy', 'Windy', 'Cloudy']
            self.current_weather = random.choice(weather_types)
            self.weather_duration = random.randint(5, 15)  # turns

        weather_effects = {
            'Sunny': {
                'description': 'Bright sunshine warms the land',
                'effects': ['Fire-type moves +20% power', 'Water-type moves -10% power', 'Higher catch rates'],
                'color': Fore.YELLOW
            },
            'Rainy': {
                'description': 'Gentle rain falls from gray clouds',
                'effects': ['Water-type moves +20% power', 'Fire-type moves -10% power', 'Electric moves +15% power'],
                'color': Fore.BLUE
            },
            'Stormy': {
                'description': 'Lightning flashes across dark skies',
                'effects': ['Electric-type moves +30% power', 'Flying-type spawn rate decreased', 'Legendary encounters +5%'],
                'color': Fore.MAGENTA
            },
            'Foggy': {
                'description': 'Thick fog reduces visibility',
                'effects': ['All accuracy -15%', 'Ghost-type spawn rate increased', 'Mysterious encounters +10%'],
                'color': Fore.WHITE
            },
            'Snowy': {
                'description': 'Snow blankets the landscape',
                'effects': ['Ice-type moves +20% power', 'Grass-type moves -15% power', 'Monster movement speed -10%'],
                'color': Fore.LIGHTCYAN_EX
            },
            'Windy': {
                'description': 'Strong winds blow across the region',
                'effects': ['Flying-type moves +25% power', 'Flying-type spawn rate increased', 'Items blow away chance +5%'],
                'color': Fore.LIGHTBLUE_EX
            },
            'Cloudy': {
                'description': 'Overcast skies block the sun',
                'effects': ['Normal weather conditions', 'Balanced monster spawns', 'Standard battle mechanics'],
                'color': Fore.LIGHTBLACK_EX
            }
        }

        current_weather_info = weather_effects[self.current_weather]

        print(f"{current_weather_info['color']}Current Weather: {self.current_weather}")
        print(f"{current_weather_info['description']}")
        print(f"Duration: {self.weather_duration} more actions{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}Weather Effects:")
        for effect in current_weather_info['effects']:
            print(f"  • {effect}")

        print(f"\n{Fore.YELLOW}Weather Forecast:")
        # Generate simple forecast
        future_weather = random.choice(list(weather_effects.keys()))
        print(f"  Next: {future_weather} - {weather_effects[future_weather]['description']}")

        print(f"\n{Fore.CYAN}Weather Tips:")
        print("• Weather changes every 5-15 actions")
        print("• Plan your battles around favorable conditions")
        print("• Some monsters prefer certain weather types")
        print("• Legendary monsters may appear during storms")

        safe_input("\nPress Enter to continue...")

    def show_time_system(self):
        """Show day/night cycle affecting gameplay"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}          TIME SYSTEM")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize time system if it doesn't exist
        if not hasattr(self, 'game_time'):
            self.game_time = 0  # 0-23 representing hours
            self.day_count = 1

        # Advance time slightly
        self.game_time = (self.game_time + 1) % 24
        if self.game_time == 0:
            self.day_count += 1

        # Determine time period
        if 6 <= self.game_time < 12:
            period = "Morning"
            period_color = Fore.YELLOW
        elif 12 <= self.game_time < 18:
            period = "Afternoon"
            period_color = Fore.LIGHTYELLOW_EX
        elif 18 <= self.game_time < 22:
            period = "Evening"
            period_color = Fore.MAGENTA
        else:
            period = "Night"
            period_color = Fore.BLUE

        print(f"{period_color}Current Time: Day {self.day_count}, {self.game_time:02d}:00 ({period}){Style.RESET_ALL}")

        # Time-based effects
        time_effects = {
            "Morning": [
                "Monster healing is 25% more effective",
                "Grass and Normal types are more active",
                "Shops offer morning discounts (10% off)"
            ],
            "Afternoon": [
                "Standard monster activity levels",
                "All monster types equally active",
                "Training facilities are busy (+20% XP)"
            ],
            "Evening": [
                "Fire and Electric types are more active",
                "Sunset creates beautiful battle backgrounds",
                "Experience gains are increased by 15%"
            ],
            "Night": [
                "Dark, Ghost, and Psychic types appear more",
                "Rare and legendary encounters increased",
                "Monster centers offer night healing bonuses"
            ]
        }

        print(f"\n{Fore.GREEN}Current Time Effects:")
        for effect in time_effects[period]:
            print(f"  • {effect}")

        # Daily events
        print(f"\n{Fore.YELLOW}Daily Events:")
        daily_events = [
            "Daily login bonus available",
            "Monster tournament registration open",
            "Rare monster migration in progress",
            "Double XP event active",
            "Special shop items available"
        ]

        # Simple day-based events
        event_index = self.day_count % len(daily_events)
        print(f"  🎉 {daily_events[event_index]}")

        print(f"\n{Fore.CYAN}Time-Based Tips:")
        print("• Different monsters are active at different times")
        print("• Night time is best for rare encounters")
        print("• Morning healing is most cost-effective")
        print("• Evening training gives bonus experience")
        print("• Check back daily for new events!")

        safe_input("\nPress Enter to continue...")

    def show_world_map(self):
        """Show world map with travel options"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}           WORLD MAP")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize visited areas if they don't exist
        if self.player and not hasattr(self.player, 'visited_areas'):
            self.player.visited_areas = {'Forest Grove'}  # Starting area

        locations = {
            'Forest Grove': {
                'description': 'A peaceful forest with friendly monsters',
                'monster_types': ['Grass', 'Normal', 'Flying'],
                'travel_cost': 0,
                'unlocked': True,
                'special': 'Starting area'
            },
            'Crystal Caves': {
                'description': 'Sparkling caves filled with crystal monsters',
                'monster_types': ['Rock', 'Ice', 'Psychic'],
                'travel_cost': 50,
                'unlocked': self.player.trainer_level >= 5 if self.player else False,
                'special': 'Rare crystals found here'
            },
            'Volcanic Peak': {
                'description': 'A dangerous mountain with fire monsters',
                'monster_types': ['Fire', 'Ground', 'Rock'],
                'travel_cost': 100,
                'unlocked': self.player.trainer_level >= 10 if self.player else False,
                'special': 'Fire-type paradise'
            },
            'Ocean Depths': {
                'description': 'Deep waters home to powerful water monsters',
                'monster_types': ['Water', 'Electric', 'Ice'],
                'travel_cost': 150,
                'unlocked': self.player.trainer_level >= 15 if self.player else False,
                'special': 'Legendary sea monsters'
            },
            'Sky Islands': {
                'description': 'Floating islands in the clouds',
                'monster_types': ['Flying', 'Electric', 'Dragon'],
                'travel_cost': 200,
                'unlocked': self.player.trainer_level >= 20 if self.player else False,
                'special': 'Ancient flying monsters'
            },
            'Shadow Realm': {
                'description': 'A dark dimension between worlds',
                'monster_types': ['Dark', 'Ghost', 'Psychic'],
                'travel_cost': 300,
                'unlocked': self.player.trainer_level >= 25 if self.player else False,
                'special': 'Corrupted variants common'
            },
            'Cosmic Observatory': {
                'description': 'A space station monitoring the universe',
                'monster_types': ['Cosmic', 'Psychic', 'Electric'],
                'travel_cost': 500,
                'unlocked': self.player.trainer_level >= 30 if self.player else False,
                'special': 'Legendary cosmic monsters'
            },
            'Temporal Nexus': {
                'description': 'Where time and space converge',
                'monster_types': ['Time', 'Space', 'Cosmic'],
                'travel_cost': 1000,
                'unlocked': self.player.trainer_level >= 40 if self.player else False,
                'special': 'Ultimate legendary encounters'
            }
        }

        current_location = self.player.current_location if self.player else 'Forest Grove'

        print(f"{Fore.YELLOW}Current Location: {current_location}")
        if current_location in locations:
            print(f"Description: {locations[current_location]['description']}")
            print(f"Monster Types: {', '.join(locations[current_location]['monster_types'])}")

        print(f"\n{Fore.GREEN}Available Locations:")
        for name, info in locations.items():
            status_symbol = "📍" if name == current_location else "🗺️"
            unlock_symbol = "✅" if info['unlocked'] else "🔒"
            visited_symbol = "⭐" if name in (self.player.visited_areas if self.player else set()) else ""

            if info['unlocked']:
                print(f"{status_symbol} {unlock_symbol} {name} {visited_symbol}")
                print(f"    {info['description']}")
                print(f"    Types: {', '.join(info['monster_types'])}")
                print(f"    Travel Cost: {info['travel_cost']} tokens")
                print(f"    Special: {info['special']}")
            else:
                req_level = {
                    'Crystal Caves': 5, 'Volcanic Peak': 10, 'Ocean Depths': 15,
                    'Sky Islands': 20, 'Shadow Realm': 25, 'Cosmic Observatory': 30,
                    'Temporal Nexus': 40
                }.get(name, 1)
                print(f"{status_symbol} {unlock_symbol} {name} (Requires Trainer Level {req_level})")
            print()

        print(f"{Fore.CYAN}Map Legend:")
        print("📍 Current Location  🗺️ Available  ✅ Unlocked  🔒 Locked  ⭐ Visited")

        print(f"\n{Fore.CYAN}Travel Options:")
        print("t <location> - Travel to location")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice.startswith('t '):
            location_name = choice[2:].title()
            if location_name in locations:
                location = locations[location_name]
                if location['unlocked']:
                    if self.player and self.player.tokens >= location['travel_cost']:
                        self.player.tokens -= location['travel_cost']
                        self.player.current_location = location_name
                        self.player.visited_areas.add(location_name)
                        print(f"\n{Fore.GREEN}Traveled to {location_name}!")
                        print(f"You are now in: {location['description']}")
                    else:
                        print(f"\n{Fore.RED}Not enough tokens! Need {location['travel_cost']}")
                else:
                    print(f"\n{Fore.RED}Location not unlocked yet!")
            else:
                print(f"\n{Fore.RED}Location not found!")
            safe_input("Press Enter to continue...")

    def show_alliance_menu(self):
        """Show alliance system for team cooperation"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         ALLIANCE SYSTEM")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        print(f"{Fore.YELLOW}Alliance Features:")
        print("• Team up with other trainers")
        print("• Share resources and strategies")
        print("• Participate in alliance wars")
        print("• Access exclusive alliance tournaments")
        print("• Earn alliance loyalty rewards")

        print(f"\n{Fore.GREEN}Available Alliances:")
        print("1. Dragon Riders Alliance - Focus: Dragon-type mastery")
        print("2. Elemental Unity - Focus: Multi-type strategies")
        print("3. Shadow Legion - Focus: Dark-type dominance")
        print("4. Crystal Guardians - Focus: Defensive tactics")
        print("5. Storm Chasers - Focus: Electric/Flying types")

        print(f"\n{Fore.CYAN}This feature is coming soon!")
        print("Alliance battles and cooperative gameplay will be available in future updates.")

        safe_input("\nPress Enter to continue...")

    def show_advanced_inventory(self):
        """Enhanced inventory with sorting and filtering"""
        if not self.player:
            print("No active player found!")
            return

        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}       ADVANCED INVENTORY")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        if not self.player.inventory:
            print(f"{Fore.YELLOW}Your inventory is empty!")
            safe_input("Press Enter to continue...")
            return

        # Categorize items
        categories = {}
        for item in self.player.inventory:
            category = getattr(item, 'effect', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        print(f"{Fore.YELLOW}Inventory ({len(self.player.inventory)}/{MAX_INVENTORY_SIZE}):")

        for category, items in categories.items():
            print(f"\n{Fore.GREEN}{category.title()}:")
            for i, item in enumerate(items, 1):
                rarity_color = Fore.WHITE
                if 'rare' in item.name.lower():
                    rarity_color = Fore.BLUE
                elif 'super' in item.name.lower():
                    rarity_color = Fore.MAGENTA
                elif 'master' in item.name.lower():
                    rarity_color = Fore.YELLOW

                print(f"  {rarity_color}{item.name} - {item.description}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}Inventory Actions:")
        print("u - Use item")
        print("s - Sort inventory")
        print("f - Filter by category")
        print("d - Drop item")
        print("b - Back to main menu")

        choice = safe_input("\nEnter your choice: ").lower()

        if choice == 'u':
            self.use_item_from_inventory()
        elif choice == 's':
            # Sort inventory by name
            if self.player.inventory:
                sorted_items = sorted(self.player.inventory.keys(), key=lambda x: x.name)
                print(f"\n{Fore.GREEN}Inventory sorted alphabetically:")
                for item in sorted_items:
                    quantity = self.player.inventory[item]
                    print(f"  {item.name} (x{quantity})")
            else:
                print(f"\n{Fore.YELLOW}No items to sort!")
            safe_input("Press Enter to continue...")
        elif choice == 'f':
            category = safe_input("Enter category to filter by: ").lower()
            filtered_items = [(item, qty) for item, qty in self.player.inventory.items() if category in getattr(item, 'effect', '').lower()]
            if filtered_items:
                print(f"\n{Fore.GREEN}Items in category '{category}':")
                for item, qty in filtered_items:
                    print(f"  {item.name} (x{qty}) - {item.description}")
            else:
                print(f"\n{Fore.YELLOW}No items found in category '{category}'")
            safe_input("Press Enter to continue...")
        elif choice == 'd':
            if self.player.inventory:
                print(f"\n{Fore.YELLOW}Select item to drop:")
                inventory_items = list(self.player.inventory.keys())
                for i, item in enumerate(inventory_items, 1):
                    quantity = self.player.inventory[item]
                    print(f"{i}. {item.name} (x{quantity})")

                try:
                    item_num = int(safe_input("Enter item number: ")) - 1
                    if 0 <= item_num < len(inventory_items):
                        dropped_item = inventory_items[item_num]
                        # Remove one item from inventory
                        if self.player.inventory[dropped_item] > 1:
                            self.player.inventory[dropped_item] -= 1
                        else:
                            del self.player.inventory[dropped_item]
                        print(f"\n{Fore.YELLOW}Dropped {dropped_item.name}!")
                    else:
                        print(f"\n{Fore.RED}Invalid item number!")
                except ValueError:
                    print(f"\n{Fore.RED}Please enter a valid number!")
                safe_input("Press Enter to continue...")

    def use_item_from_inventory(self):
        """Use an item from inventory on a monster"""
        if not self.player or not self.player.inventory:
            print(f"\n{Fore.YELLOW}No items to use!")
            return

        print(f"\n{Fore.YELLOW}Select item to use:")
        items_list = list(self.player.inventory.keys())
        for i, item in enumerate(items_list, 1):
            quantity = self.player.inventory[item]
            print(f"{i}. {item.name} x{quantity} - {item.description}")

        try:
            item_num = int(safe_input("Enter item number: ")) - 1
            if 0 <= item_num < len(items_list):
                item = items_list[item_num]

                # Select monster to use item on
                if not self.player.monsters:
                    print(f"\n{Fore.RED}No monsters to use item on!")
                    return

                print(f"\n{Fore.GREEN}Select monster:")
                for i, monster in enumerate(self.player.monsters, 1):
                    status = "Fainted" if monster.is_fainted() else "Healthy"
                    print(f"{i}. {monster.name} (Lv.{monster.level}) - {status}")

                monster_num = int(safe_input("Enter monster number: ")) - 1
                if 0 <= monster_num < len(self.player.monsters):
                    monster = self.player.monsters[monster_num]

                    # Apply item effect
                    if 'heal' in item.name.lower():
                        if 'super' in item.name.lower():
                            monster.full_heal()
                            print(f"\n{Fore.GREEN}{monster.name} fully healed!")
                        else:
                            monster.heal(50)
                            print(f"\n{Fore.GREEN}{monster.name} healed for 50 HP!")
                    elif 'experience' in item.name.lower():
                        if 'candy' in item.name.lower():
                            monster.level += 1
                            monster.calculate_stats()
                            print(f"\n{Fore.GREEN}{monster.name} leveled up!")
                        else:
                            monster.gain_exp(200)
                            print(f"\n{Fore.GREEN}{monster.name} gained experience!")
                    elif 'boost' in item.name.lower():
                        if 'power' in item.name.lower():
                            monster.base_attack += 5
                            print(f"\n{Fore.GREEN}{monster.name}'s attack increased!")
                        elif 'defense' in item.name.lower():
                            monster.base_defense += 5
                            print(f"\n{Fore.GREEN}{monster.name}'s defense increased!")
                        elif 'speed' in item.name.lower():
                            monster.base_speed += 5
                            print(f"\n{Fore.GREEN}{monster.name}'s speed increased!")
                        monster.calculate_stats()
                    elif 'revival' in item.name.lower():
                        if monster.is_fainted():
                            monster.current_hp = monster.max_hp // 2
                            print(f"\n{Fore.GREEN}{monster.name} was revived!")
                        else:
                            print(f"\n{Fore.YELLOW}{monster.name} is not fainted!")
                            return

                    # Remove used item
                    if item in self.player.inventory:
                        if self.player.inventory[item] > 1:
                            self.player.inventory[item] -= 1
                        else:
                            del self.player.inventory[item]
                else:
                    print(f"\n{Fore.RED}Invalid monster number!")
            else:
                print(f"\n{Fore.RED}Invalid item number!")
        except ValueError:
            print(f"\n{Fore.RED}Please enter valid numbers!")

        safe_input("Press Enter to continue...")

    def show_research_menu(self):
        """Show monster research and database"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}       RESEARCH DATABASE")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        print(f"{Fore.YELLOW}Research Features:")
        print("• Study monster behaviors and patterns")
        print("• Unlock evolution requirements")
        print("• Discover type effectiveness charts")
        print("• Research rare monster locations")
        print("• Analyze battle statistics")

        print(f"\n{Fore.GREEN}Research Progress:")
        if self.player:
            research_points = getattr(self.player, 'research_points', 0)
            print(f"Research Points: {research_points}")

            discovered_species = len(set(monster.name.split()[0] for monster in self.player.monsters))
            print(f"Species Discovered: {discovered_species}")

            type_expertise = {}
            for monster in self.player.monsters:
                type_expertise[monster.type] = type_expertise.get(monster.type, 0) + 1

            print("Type Expertise:")
            for mon_type, count in sorted(type_expertise.items()):
                expertise_level = min(count // 3, 5)  # Max level 5
                stars = "★" * expertise_level + "☆" * (5 - expertise_level)
                print(f"  {mon_type}: {stars} (Level {expertise_level})")

        print(f"\n{Fore.CYAN}This feature will be expanded in future updates!")
        safe_input("Press Enter to continue...")

    def enter_dungeon(self):
        """Enter special dungeon challenges"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         DUNGEON EXPLORER")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        dungeons = [
            {
                'name': 'Crystal Caverns',
                'difficulty': 'Easy',
                'levels': 5,
                'rewards': 'Crystal materials, Rock-type monsters',
                'entry_cost': 100
            },
            {
                'name': 'Shadow Temple',
                'difficulty': 'Medium',
                'levels': 10,
                'rewards': 'Dark materials, Ghost-type monsters',
                'entry_cost': 250
            },
            {
                'name': 'Dragon\'s Lair',
                'difficulty': 'Hard',
                'levels': 15,
                'rewards': 'Dragon materials, Legendary encounters',
                'entry_cost': 500
            },
            {
                'name': 'Void Nexus',
                'difficulty': 'Extreme',
                'levels': 20,
                'rewards': 'Ultimate materials, Cosmic monsters',
                'entry_cost': 1000
            }
        ]

        print(f"{Fore.YELLOW}Available Dungeons:")
        for i, dungeon in enumerate(dungeons, 1):
            color = Fore.GREEN if dungeon['difficulty'] == 'Easy' else \
                   Fore.YELLOW if dungeon['difficulty'] == 'Medium' else \
                   Fore.RED if dungeon['difficulty'] == 'Hard' else Fore.MAGENTA

            print(f"{i}. {color}{dungeon['name']} ({dungeon['difficulty']}){Style.RESET_ALL}")
            print(f"   Levels: {dungeon['levels']}")
            print(f"   Rewards: {dungeon['rewards']}")
            print(f"   Entry Cost: {dungeon['entry_cost']} tokens")

        print(f"\n{Fore.CYAN}Dungeon Features:")
        print("• Progressive difficulty levels")
        print("• Unique rewards and materials")
        print("• Boss battles at the end")
        print("• Leaderboards for completion times")

        print(f"\n{Fore.CYAN}This feature is coming soon!")
        print("Dungeon exploration will be available in future updates.")

        safe_input("Press Enter to continue...")

    def join_raid(self):
        """Join cooperative raid battles"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}          RAID BATTLES")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        print(f"{Fore.YELLOW}Active Raids:")
        print("🔥 Legendary Pyrovern Raid - 2/4 players")
        print("⚡ Storm Titan Challenge - 1/6 players")
        print("🌟 Cosmic Entity Event - 0/8 players")

        print(f"\n{Fore.GREEN}Raid Features:")
        print("• Team up with multiple trainers")
        print("• Battle ultra-powerful boss monsters")
        print("• Share raid rewards among participants")
        print("• Unlock exclusive raid-only monsters")
        print("• Weekly raid rotation")

        print(f"\n{Fore.CYAN}This feature is coming soon!")
        print("Cooperative raid battles will be available in future updates.")

        safe_input("Press Enter to continue...")

    def enter_pvp(self):
        """Enter player vs player battles"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}            PVP ARENA")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        print(f"{Fore.YELLOW}PVP Modes:")
        print("1. Ranked Battles - Climb the competitive ladder")
        print("2. Casual Matches - Practice without rank pressure")
        print("3. Tournament Mode - Participate in bracketed competitions")
        print("4. Guild Wars - Represent your guild in battles")

        print(f"\n{Fore.GREEN}PVP Features:")
        print("• Real-time battles against other players")
        print("• Seasonal rankings and rewards")
        print("• Spectator mode for learning strategies")
        print("• Ban/pick phases for strategic depth")
        print("• Replay system to review battles")

        print(f"\n{Fore.CYAN}This feature is coming soon!")
        print("PVP battles will be available in future updates.")

        safe_input("Press Enter to continue...")

    def show_market(self):
        """Show player-to-player trading market"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         TRADING MARKET")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        print(f"{Fore.YELLOW}Market Listings:")
        print("🔥 Alpha Pyrovern - 5000 tokens")
        print("⚡ Crystal Thunderwing - 3500 tokens")
        print("🌟 Rare Stardust - 1200 tokens")
        print("💎 Fusion Catalyst - 800 tokens")

        print(f"\n{Fore.GREEN}Market Features:")
        print("• Buy and sell monsters with other players")
        print("• Trade rare items and materials")
        print("• Auction system for competitive bidding")
        print("• Price history and market trends")
        print("• Secure escrow system")

        print(f"\n{Fore.CYAN}This feature is coming soon!")
        print("Player trading market will be available in future updates.")

        safe_input("Press Enter to continue...")

    def show_daily_tasks(self):
        """Show daily challenges and rewards"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         DAILY TASKS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Initialize daily tasks if they don't exist
        if not self.player or not hasattr(self.player, 'daily_tasks'):
            if self.player:
                self.player.daily_tasks = {
                    'catch_monsters': {'progress': 0, 'target': 3, 'completed': False},
                    'win_battles': {'progress': 0, 'target': 5, 'completed': False},
                    'explore_areas': {'progress': 0, 'target': 2, 'completed': False},
                    'use_items': {'progress': 0, 'target': 4, 'completed': False}
                }
            else:
                print(f"{Fore.RED}No player found. Please start a new game first.{Style.RESET_ALL}")
                return

        daily_task_info = {
            'catch_monsters': {
                'name': 'Monster Catcher',
                'description': 'Catch 3 wild monsters',
                'reward': '100 tokens, 1 Monster Ball Plus'
            },
            'win_battles': {
                'name': 'Battle Winner',
                'description': 'Win 5 battles',
                'reward': '150 tokens, Experience Candy'
            },
            'explore_areas': {
                'name': 'Explorer',
                'description': 'Visit 2 different areas',
                'reward': '80 tokens, Rare materials'
            },
            'use_items': {
                'name': 'Item User',
                'description': 'Use 4 items on monsters',
                'reward': '60 tokens, Heal Potions'
            }
        }

        print(f"{Fore.YELLOW}Today's Daily Tasks:")

        for task_id, task_data in self.player.daily_tasks.items():
            task_info = daily_task_info[task_id]
            progress = task_data['progress']
            target = task_data['target']
            completed = task_data['completed']

            status = "✅ COMPLETED" if completed else f"{progress}/{target}"
            progress_bar = "█" * (progress * 10 // target) + "░" * (10 - (progress * 10 // target))

            color = Fore.GREEN if completed else Fore.YELLOW
            print(f"{color}{task_info['name']}: {task_info['description']}")
            print(f"  Progress: [{progress_bar}] {status}")
            print(f"  Reward: {task_info['reward']}{Style.RESET_ALL}")
            print()

        # Check if all tasks completed
        all_completed = all(task['completed'] for task in self.player.daily_tasks.values())
        if all_completed:
            print(f"{Fore.YELLOW}🎉 ALL DAILY TASKS COMPLETED! 🎉")
            print("Bonus Reward: 500 tokens + Premium Mystery Box")

        print(f"\n{Fore.CYAN}Daily Task Tips:")
        print("• Tasks reset every 24 hours")
        print("• Complete all tasks for bonus rewards")
        print("• Tasks help you progress faster")
        print("• Check back daily for new challenges")

        safe_input("\nPress Enter to continue...")

    def show_events(self):
        """Show special events and limited-time content"""
        clear_screen()
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}         SPECIAL EVENTS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")

        # Generate some sample events
        current_events = [
            {
                'name': 'Legendary Weekend',
                'description': 'Increased legendary monster spawn rates',
                'duration': '2 days remaining',
                'rewards': 'Legendary encounters +300%',
                'active': True
            },
            {
                'name': 'Double XP Week',
                'description': 'All monsters gain double experience',
                'duration': '5 days remaining',
                'rewards': 'XP gains +100%',
                'active': True
            },
            {
                'name': 'Crystal Festival',
                'description': 'Crystal-type monsters everywhere',
                'duration': 'Ended',
                'rewards': 'Crystal materials, Rare crystals',
                'active': False
            },
            {
                'name': 'Fusion Celebration',
                'description': 'Fusion costs reduced by 50%',
                'duration': 'Starting in 3 days',
                'rewards': 'Discounted fusions, Free catalysts',
                'active': False
            }
        ]

        print(f"{Fore.YELLOW}Active Events:")
        active_events = [event for event in current_events if event['active']]
        if active_events:
            for event in active_events:
                print(f"🎉 {event['name']}")
                print(f"   {event['description']}")
                print(f"   Duration: {event['duration']}")
                print(f"   Special: {event['rewards']}")
                print()
        else:
            print("No active events at this time.")

        print(f"\n{Fore.GREEN}Upcoming Events:")
        upcoming_events = [event for event in current_events if not event['active'] and 'Starting' in event['duration']]
        for event in upcoming_events:
            print(f"📅 {event['name']} - {event['duration']}")
            print(f"   {event['description']}")

        print(f"\n{Fore.BLUE}Past Events:")
        past_events = [event for event in current_events if not event['active'] and 'Ended' in event['duration']]
        for event in past_events:
            print(f"📚 {event['name']} - {event['duration']}")

        print(f"\n{Fore.CYAN}Event Features:")
        print("• Limited-time special content")
        print("• Exclusive rewards and monsters")
        print("• Seasonal celebrations")
        print("• Community-wide challenges")
        print("• Special event currencies")

        safe_input("\nPress Enter to continue...")

    def show_character_relationships(self):
        """Show emotional bonds and character relationships"""
        if not self.player:
            print(f"{Fore.RED}No player found.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print(f"{Fore.CYAN}      CHARACTER RELATIONSHIPS")
        print(f"{Fore.CYAN}═══════════════════════════════════════")
        print("Monster bonds and NPC relationships coming soon!")
        safe_input("Press Enter to continue...")

    def show_reflection_menu(self):
        """Show narrative reflection menu"""
        print(f"{Fore.MAGENTA}═══════════════════════════════════════")
        print(f"{Fore.MAGENTA}       NARRATIVE REFLECTION")
        print(f"{Fore.MAGENTA}═══════════════════════════════════════")
        print("Story reflection system coming soon!")
        safe_input("Press Enter to continue...")

    def quick_reflect(self):
        """Quick contemplation"""
        print(f"{Fore.BLUE}Taking a moment to reflect...{Style.RESET_ALL}")
        print("Your journey continues...")
        safe_input("Press Enter to continue...")

    def show_npc_menu(self):
        """Show NPC dialogue menu"""
        print(f"{Fore.GREEN}═══════════════════════════════════════")
        print(f"{Fore.GREEN}       NPC CONVERSATIONS")
        print(f"{Fore.GREEN}═══════════════════════════════════════")
        print("Advanced dialogue system coming soon!")
        safe_input("Press Enter to continue...")

    def talk_to_npc(self, npc_name: str):
        """Talk to a specific NPC"""
        print(f"{Fore.GREEN}Talking to {npc_name}...{Style.RESET_ALL}")
        print("Conversation system coming soon!")
        safe_input("Press Enter to continue...")


# Main entry point
if __name__ == "__main__":
    # Initialize colorama
    init(autoreset=True)

    try:
        # Then check if launched through launcher
        if os.environ.get("LAUNCHED_FROM_LAUNCHER") != "1":
            print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
            print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
            safe_input("Press Enter to exit...")
            sys.exit(0)
        # No need to call main() since we're starting the game right after
    except Exception as e:
        print(f"\n\nAn error during initialization: {e}")
        sys.exit(1)

    try:
        # Start the game
        game = Game()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Thanks for playing!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

    def narrative_reflection_menu(self):
        """Interactive menu for deep narrative reflection"""
        clear_screen()
        print(f"{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}║                    NARRATIVE REFLECTION                         ║{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Take a moment to reflect on your journey...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Reflection Points: {self.player.reflection_points}{Style.RESET_ALL}\n")

        while True:
            print(f"{Fore.GREEN}What would you like to reflect upon?{Style.RESET_ALL}")
            print("1. Recent Story Moments")
            print("2. Moral Choices and Consequences") 
            print("3. Character Growth and Relationships")
            print("4. Return to game")

            choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}").strip()

            if choice == "1":
                self.reflect_on_story_moments()
            elif choice == "2":
                self.reflect_on_moral_choices()
            elif choice == "3":
                self.reflect_on_character_growth()
            elif choice == "4":
                clear_screen()
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                safe_input("Press Enter to continue...")
                clear_screen()

    def reflect_on_story_moments(self):
        """Reflect on recent significant story moments"""
        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                     STORY MOMENTS                               ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        if not self.player.story_moments:
            print(f"{Fore.YELLOW}You haven't experienced any significant story moments yet.{Style.RESET_ALL}")
            print("As you progress through your journey, meaningful moments will be recorded here for reflection.")
        else:
            print(f"{Fore.MAGENTA}Reflecting on your recent experiences...{Style.RESET_ALL}\n")

            for i, moment in enumerate(self.player.story_moments[-5:], 1):
                print(f"{Fore.WHITE}{i}. {moment['type'].title()} at {moment['location']}{Style.RESET_ALL}")
                print(f"   {moment['description']}")
                if moment['consequences']:
                    print(f"   {Fore.YELLOW}Consequences: {moment['consequences']}{Style.RESET_ALL}")

                if not moment['reflected_upon']:
                    print(f"\n{Fore.CYAN}Take a moment to consider this experience...{Style.RESET_ALL}")
                    reflection = input(f"{Fore.GREEN}What did you learn from this moment? (Press Enter to skip): {Style.RESET_ALL}")

                    if reflection.strip():
                        moment['reflected_upon'] = True
                        self.player.earn_reflection_points(2, f"Reflected on {moment['type']}")
                        print(f"{Fore.GREEN}Your reflection has been noted. +2 Reflection Points{Style.RESET_ALL}")

                print()

        safe_input("Press Enter to continue...")

    def reflect_on_moral_choices(self):
        """Reflect on moral decisions and their outcomes"""
        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                    MORAL CHOICES                                ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        if not self.player.moral_choices:
            print(f"{Fore.YELLOW}You haven't faced any significant moral dilemmas yet.{Style.RESET_ALL}")
            print("When you encounter difficult choices, they will be recorded here for reflection.")
        else:
            print(f"{Fore.MAGENTA}Contemplating your moral journey...{Style.RESET_ALL}\n")

            for i, choice in enumerate(self.player.moral_choices[-3:], 1):
                print(f"{Fore.WHITE}{i}. {choice['choice']}{Style.RESET_ALL}")
                print(f"   {Fore.CYAN}You chose: {choice['chosen_option']}{Style.RESET_ALL}")
                print(f"   {Fore.YELLOW}Outcome: {choice['outcome']}{Style.RESET_ALL}")

                # Show karma impact
                if choice['karma_impact']:
                    impacts = []
                    for trait, change in choice['karma_impact'].items():
                        color = Fore.GREEN if change > 0 else Fore.RED
                        sign = "+" if change > 0 else ""
                        impacts.append(f"{color}{trait.title()}: {sign}{change}{Style.RESET_ALL}")
                    print(f"   Karma Impact: {', '.join(impacts)}")

                if not choice['reflected_upon']:
                    print(f"\n{Fore.CYAN}How do you feel about this choice now?{Style.RESET_ALL}")
                    reflection = input(f"{Fore.GREEN}Would you choose differently? What did you learn? (Press Enter to skip): {Style.RESET_ALL}")

                    if reflection.strip():
                        choice['reflected_upon'] = True
                        self.player.earn_reflection_points(3, "Reflected on moral choice")
                        print(f"{Fore.GREEN}Your moral reflection has deepened your wisdom. +3 Reflection Points{Style.RESET_ALL}")

                print()

        safe_input("Press Enter to continue...")

    def reflect_on_character_growth(self):
        """Reflect on relationships and personal development"""
        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                 CHARACTER GROWTH                                ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        print(f"{Fore.MAGENTA}Reflecting on your personal journey...{Style.RESET_ALL}\n")

        # Analyze reputation changes
        dominant_traits = [trait for trait, value in self.player.reputation.items() if value >= 20]
        if dominant_traits:
            print(f"{Fore.WHITE}Your Character Development:{Style.RESET_ALL}")
            for trait in dominant_traits:
                value = self.player.reputation[trait]
                print(f"  • {trait.title()}: {Fore.GREEN if value >= 40 else Fore.YELLOW}{value}{Style.RESET_ALL}")

        # Relationship analysis
        strong_bonds = [name for name, bond in self.player.monster_bonds.items() 
                       if any(emotion > 70 for emotion in bond.values())]
        if strong_bonds:
            print(f"\n{Fore.WHITE}Strong Monster Bonds:{Style.RESET_ALL}")
            for name in strong_bonds:
                print(f"  • {name}")

        trusted_npcs = [name for name, rel in self.player.npc_relationships.items() 
                       if rel.get('trust', 50) > 70]
        if trusted_npcs:
            print(f"\n{Fore.WHITE}Trusted Allies:{Style.RESET_ALL}")
            for name in trusted_npcs:
                print(f"  • {name}")

        print(f"\n{Fore.CYAN}What aspects of your growth are you most proud of?{Style.RESET_ALL}")
        growth_reflection = input(f"{Fore.GREEN}Share your thoughts (Press Enter to skip): {Style.RESET_ALL}")

        if growth_reflection.strip():
            self.player.earn_reflection_points(2, "Reflected on personal growth")
            print(f"{Fore.GREEN}Self-awareness brings wisdom. +2 Reflection Points{Style.RESET_ALL}")

        safe_input("\nPress Enter to continue...")

    def quick_reflection(self):
        """Quick contemplation without full menu"""
        if not self.player.story_moments and not self.player.moral_choices:
            print(f"{Fore.YELLOW}You pause for a moment of quiet contemplation...{Style.RESET_ALL}")
            print("The journey ahead feels full of possibilities.")
        else:
            print(f"{Fore.CYAN}You take a moment to reflect on recent events...{Style.RESET_ALL}")

            if self.player.story_moments:
                recent_moment = self.player.story_moments[-1]
                print(f"You think about {recent_moment['description'][:80]}...")

            if self.player.moral_choices:
                recent_choice = self.player.moral_choices[-1]
                print(f"You consider your recent choice: {recent_choice['chosen_option']}")

        safe_input("Press Enter to continue...")

    def create_npcs(self):
        """Create dynamic NPCs with personality traits and dialogue trees"""
        return {
            "Hometown": [
                {
                    "name": "Elder Marcus",
                    "personality": ["wise", "patient", "mysterious"],
                    "backstory": "Guardian of ancient monster knowledge",
                    "opinion_of_player": 60,
                    "dialogue_trees": ["wisdom", "guidance", "lore"],
                    "secrets": ["ancient_fusion", "legendary_locations"],
                    "mood": "contemplative"
                },
                {
                    "name": "Trainer Sarah",
                    "personality": ["enthusiastic", "competitive", "encouraging"],
                    "backstory": "Former champion seeking to train new talents",
                    "opinion_of_player": 55,
                    "dialogue_trees": ["training", "battle_tips", "encouragement"],
                    "secrets": ["advanced_techniques", "hidden_training_spots"],
                    "mood": "energetic"
                },
                {
                    "name": "Merchant Jin",
                    "personality": ["shrewd", "friendly", "observant"],
                    "backstory": "Traveling merchant with rare items and gossip",
                    "opinion_of_player": 50,
                    "dialogue_trees": ["trade", "rumors", "distant_lands"],
                    "secrets": ["rare_items", "market_trends"],
                    "mood": "business-like"
                }
            ],
            "Ancient Forest": [
                {
                    "name": "Forest Hermit",
                    "personality": ["reclusive", "nature-loving", "cryptic"],
                    "backstory": "Lives in harmony with forest monsters",
                    "opinion_of_player": 45,
                    "dialogue_trees": ["nature", "forest_secrets", "solitude"],
                    "secrets": ["hidden_groves", "monster_communication"],
                    "mood": "serene"
                },
                {
                    "name": "Lost Explorer",
                    "personality": ["confused", "grateful", "adventurous"],
                    "backstory": "Explorer who got lost seeking ancient ruins",
                    "opinion_of_player": 40,
                    "dialogue_trees": ["exploration", "being_lost", "gratitude"],
                    "secrets": ["map_fragments", "dangerous_paths"],
                    "mood": "worried"
                }
            ],
            "Crystal Caverns": [
                {
                    "name": "Crystal Sage",
                    "personality": ["ancient", "knowledgeable", "ethereal"],
                    "backstory": "Guardian spirit bound to the crystals",
                    "opinion_of_player": 35,
                    "dialogue_trees": ["crystals", "ancient_power", "prophecy"],
                    "secrets": ["crystal_magic", "sealed_chambers"],
                    "mood": "otherworldly"
                }
            ],
            "Mystic Mountains": [
                {
                    "name": "Mountain Guide",
                    "personality": ["tough", "reliable", "straightforward"],
                    "backstory": "Experienced guide who knows every mountain path",
                    "opinion_of_player": 50,
                    "dialogue_trees": ["survival", "mountain_lore", "weather"],
                    "secrets": ["secret_paths", "avalanche_warnings"],
                    "mood": "focused"
                }
            ],
            "Frozen Wasteland": [
                {
                    "name": "Ice Shaman",
                    "personality": ["stoic", "spiritual", "harsh"],
                    "backstory": "Keeper of ice magic and frozen secrets",
                    "opinion_of_player": 30,
                    "dialogue_trees": ["ice_magic", "survival", "spirits"],
                    "secrets": ["frozen_artifacts", "spirit_communication"],
                    "mood": "cold"
                }
            ]
        }

    def npc_dialogue_menu(self):
        """Show available NPCs for conversation in current location"""
        clear_screen()
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        CONVERSATIONS                            ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        npcs = self.create_npcs()
        location_npcs = npcs.get(self.player.location, [])

        if not location_npcs:
            print(f"{Fore.YELLOW}There's no one to talk to in {self.player.location}.{Style.RESET_ALL}")
            print("Try exploring other locations to meet interesting characters.")
            safe_input("Press Enter to continue...")
            return

        print(f"{Fore.MAGENTA}People you can talk to in {self.player.location}:{Style.RESET_ALL}\n")

        for i, npc in enumerate(location_npcs, 1):
            # Get NPC opinion and relationship status
            opinion = self.player.character_opinions.get(npc["name"], {})
            avg_opinion = sum(opinion.values()) / len(opinion) if opinion else 50

            relationship = "Stranger"
            if avg_opinion >= 80:
                relationship = "Close Friend"
            elif avg_opinion >= 65:
                relationship = "Friend"
            elif avg_opinion >= 35:
                relationship = "Acquaintance"
            elif avg_opinion >= 20:
                relationship = "Distant"
            else:
                relationship = "Distrustful"

            print(f"{Fore.WHITE}{i}. {npc['name']}{Style.RESET_ALL}")
            print(f"   {npc['backstory']}")
            print(f"   Relationship: {Fore.CYAN}{relationship}{Style.RESET_ALL}")
            print()

        print(f"{len(location_npcs) + 1}. Return to game")

        while True:
            choice = input(f"\n{Fore.GREEN}Who would you like to talk to? {Style.RESET_ALL}").strip()

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(location_npcs):
                    selected_npc = location_npcs[choice_num - 1]
                    self.start_npc_conversation(selected_npc["name"])
                    break
                elif choice_num == len(location_npcs) + 1:
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")

    def start_npc_conversation(self, npc_name: str):
        """Start a dynamic conversation with an NPC"""
        npcs = self.create_npcs()
        npc = None

        # Find the NPC
        for location_npcs in npcs.values():
            for character in location_npcs:
                if character["name"].lower() == npc_name.lower():
                    npc = character
                    break
            if npc:
                break

        if not npc:
            print(f"{Fore.RED}I don't see {npc_name} here.{Style.RESET_ALL}")
            safe_input("Press Enter to continue...")
            return

        # Get player's relationship with this NPC
        opinion = self.player.character_opinions.get(npc["name"], {
            "respect": 50, "trust": 50, "friendliness": 50, "interest": 50
        })
        avg_opinion = sum(opinion.values()) / len(opinion)

        self.run_dialogue_conversation(npc, avg_opinion)

    def run_dialogue_conversation(self, npc: dict, relationship_level: float):
        """Run a dynamic branching conversation with an NPC"""
        clear_screen()
        print(f"{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}║                    CONVERSATION                                 ║{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}You approach {npc['name']}.{Style.RESET_ALL}\n")

        # Generate greeting based on relationship and personality
        greeting = self.generate_npc_greeting(npc, relationship_level)
        print(f"{Fore.WHITE}{npc['name']}: {greeting}{Style.RESET_ALL}\n")

        conversation_active = True
        conversation_depth = 0

        while conversation_active and conversation_depth < 10:
            conversation_depth += 1

            # Generate dialogue options based on context
            options = self.generate_dialogue_options(npc, relationship_level, conversation_depth)

            print(f"{Fore.GREEN}How do you respond?{Style.RESET_ALL}")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option['text']}")
            print(f"{len(options) + 1}. End conversation")

            while True:
                choice = input(f"\n{Fore.CYAN}Choose your response: {Style.RESET_ALL}").strip()

                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(options):
                        selected_option = options[choice_num - 1]
                        response = self.process_dialogue_choice(npc, selected_option, relationship_level)

                        print(f"\n{Fore.WHITE}{npc['name']}: {response}{Style.RESET_ALL}\n")

                        # Record the dialogue choice
                        self.player.record_dialogue_choice(
                            npc["name"], 
                            f"conversation_{conversation_depth}",
                            selected_option["text"],
                            selected_option.get("consequence", "")
                        )

                        # Update relationship based on choice
                        if "opinion_change" in selected_option:
                            self.player.update_character_opinion(
                                npc["name"],
                                selected_option["opinion_change"],
                                selected_option.get("reason", "")
                            )

                        # Check if conversation should continue
                        if selected_option.get("ends_conversation", False):
                            conversation_active = False

                        break
                    elif choice_num == len(options) + 1:
                        conversation_active = False
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")

        # End conversation
        farewell = self.generate_npc_farewell(npc, relationship_level)
        print(f"{Fore.WHITE}{npc['name']}: {farewell}{Style.RESET_ALL}")

        # Award reflection points for meaningful conversations
        if conversation_depth >= 3:
            self.player.earn_reflection_points(1, f"Had a meaningful conversation with {npc['name']}")
            print(f"{Fore.GREEN}+1 Reflection Point for engaging conversation{Style.RESET_ALL}")

        safe_input("\nPress Enter to continue...")

    def generate_npc_greeting(self, npc: dict, relationship_level: float) -> str:
        """Generate a greeting based on NPC personality and relationship"""
        personality = npc["personality"]
        name = self.player.name

        if relationship_level >= 80:
            if "wise" in personality:
                return f"Ah, {name}, my dear friend. Your wisdom grows with each visit."
            elif "enthusiastic" in personality:
                return f"{name}! Great to see you again! Ready for another adventure?"
            elif "friendly" in personality:
                return f"Welcome back, {name}! Always a pleasure to see you."
            else:
                return f"Hello again, {name}. Good to see a trusted friend."
        elif relationship_level >= 50:
            if "wise" in personality:
                return f"Greetings, {name}. I sense your journey has taught you much."
            elif "enthusiastic" in personality:
                return f"Hey there, {name}! How's your training going?"
            elif "mysterious" in personality:
                return f"{name}... the paths bring us together once more."
            else:
                return f"Hello, {name}. What brings you here today?"
        elif relationship_level >= 30:
            if "reclusive" in personality:
                return "Oh... it's you again. What do you want?"
            elif "stoic" in personality:
                return "You return. State your business."
            elif "cautious" in personality:
                return "I see you've come back. Be careful what you ask."
            else:
                return "Hello there. What can I do for you?"
        else:
            if "distrustful" in personality:
                return "What do you want? Make it quick."
            elif "cold" in personality:
                return "You again. I have little time for chatter."
            else:
                return "What brings a stranger to speak with me?"

    def generate_dialogue_options(self, npc: dict, relationship_level: float, depth: int) -> list:
        """Generate dialogue options based on NPC and conversation context"""
        options = []
        trees = npc["dialogue_trees"]
        personality = npc["personality"]

        # Basic conversation starters
        if depth == 1:
            if "lore" in trees:
                options.append({
                    "text": "Tell me about this place.",
                    "type": "information",
                    "opinion_change": 2,
                    "reason": "showed interest"
                })

            if "training" in trees and relationship_level >= 40:
                options.append({
                    "text": "Could you give me some training advice?",
                    "type": "help_request",
                    "opinion_change": 3,
                    "reason": "respectful request for help"
                })

            options.append({
                "text": "How are you doing today?",
                "type": "friendly",
                "opinion_change": 1,
                "reason": "friendly small talk"
            })

            if "rude" in personality:
                options.append({
                    "text": "You look pretty useless.",
                    "type": "insult",
                    "opinion_change": -10,
                    "reason": "rude insult",
                    "ends_conversation": True
                })

        # Deeper conversation options
        elif depth >= 2:
            if relationship_level >= 60 and "secrets" in npc:
                options.append({
                    "text": "Is there anything special about this area?",
                    "type": "secret_inquiry",
                    "opinion_change": 1,
                    "reason": "showed deeper interest"
                })

            if "wise" in personality:
                options.append({
                    "text": "What wisdom can you share with me?",
                    "type": "wisdom_request",
                    "opinion_change": 2,
                    "reason": "respectful wisdom seeking"
                })

            if relationship_level >= 70:
                options.append({
                    "text": "I feel like we're becoming good friends.",
                    "type": "friendship",
                    "opinion_change": 5,
                    "reason": "friendly bonding"
                })

        # Personality-specific options
        if "competitive" in personality:
            options.append({
                "text": "Want to have a friendly competition?",
                "type": "challenge",
                "opinion_change": 3,
                "reason": "engaging competition spirit"
            })

        if "mysterious" in personality and relationship_level >= 50:
            options.append({
                "text": "You seem to know more than you let on.",
                "type": "mystery_probe",
                "opinion_change": -1,
                "reason": "prying into secrets"
            })

        # Always include a polite option
        options.append({
            "text": "Thank you for your time.",
            "type": "polite_exit",
            "opinion_change": 1,
            "reason": "polite conversation",
            "ends_conversation": True
        })

        return options[:4]  # Limit to 4 options for readability

    def process_dialogue_choice(self, npc: dict, choice: dict, relationship_level: float) -> str:
        """Process a dialogue choice and return NPC response"""
        choice_type = choice["type"]
        personality = npc["personality"]

        responses = {
            "information": [
                "This place holds many secrets. Those who seek knowledge will find it.",
                f"There's more to {self.player.location} than meets the eye.",
                "Every location has its own energy and purpose."
            ],
            "help_request": [
                "The key to success is patience and understanding your monsters.",
                "Never give up, even when the path seems impossible.",
                "True strength comes from the bond with your monsters."
            ],
            "friendly": [
                "I'm doing well, thank you for asking.",
                "Each day brings new challenges and opportunities.",
                "Life is good when you find your purpose."
            ],
            "insult": [
                "That was uncalled for. This conversation is over.",
                "I have no time for rudeness.",
                "Perhaps you should learn some manners."
            ],
            "secret_inquiry": [
                "Some secrets are earned through trust and time.",
                "There are hidden places that few have discovered.",
                "The wise know when to seek and when to wait."
            ],
            "wisdom_request": [
                "True wisdom comes from experience and reflection.",
                "The journey teaches us more than the destination.",
                "Listen to your heart, but also use your mind."
            ],
            "friendship": [
                "I appreciate your friendship as well.",
                "It's rare to find someone you can truly trust.",
                "Friendship is one of life's greatest treasures."
            ],
            "challenge": [
                "I admire your competitive spirit!",
                "Competition brings out the best in us.",
                "Perhaps someday we'll test our skills."
            ],
            "mystery_probe": [
                "Some things are better left unspoken.",
                "Knowledge comes to those who are ready.",
                "Not all mysteries are meant to be solved quickly."
            ],
            "polite_exit": [
                "It was pleasant speaking with you.",
                "Take care on your journey.",
                "May your path be filled with discovery."
            ]
        }

        # Get appropriate response based on choice type
        base_responses = responses.get(choice_type, ["I see."])

        # Modify response based on personality
        if "wise" in personality and choice_type in ["wisdom_request", "information"]:
            wisdom_responses = [
                "The ancient texts speak of balance in all things.",
                "Understanding comes not from knowledge alone, but from applying it wisely.",
                "The greatest teachers are often our own experiences."
            ]
            base_responses.extend(wisdom_responses)

        if "enthusiastic" in personality:
            enthusiasm_boost = " Your enthusiasm is infectious!"
            selected = random.choice(base_responses)
            if choice_type != "insult":
                return selected + enthusiasm_boost

        return random.choice(base_responses)

    def generate_npc_farewell(self, npc: dict, relationship_level: float) -> str:
        """Generate a farewell message based on relationship"""
        personality = npc["personality"]

        if relationship_level >= 70:
            if "wise" in personality:
                return "Go well, friend. May wisdom light your path."
            elif "enthusiastic" in personality:
                return "See you later! Can't wait to hear about your adventures!"
            else:
                return "Take care, my friend. Until we meet again."
        elif relationship_level >= 40:
            if "wise" in personality:
                return "Farewell. May your journey bring you knowledge."
            else:
                return "Safe travels on your journey."
        else:
            return "Goodbye."

def main():
    """Main function to start the game"""
    try:
        game = Game()
        game.start_game()
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
