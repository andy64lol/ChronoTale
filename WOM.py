import random
import time
import os
import pickle
import sys
from typing import List, Dict, Optional, Tuple
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Check if script is being run directly or through the launcher
if __name__ == "__main__":
    launcher_env = os.environ.get("LAUNCHER_ACTIVE")
    if not launcher_env:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
        print(f"{Fore.BLUE}Made by andy64lol{Style.RESET_ALL}")
        sys.exit(0)

# Add GOLD color for trophy/medal display
if not hasattr(Fore, 'GOLD'):
    setattr(Fore, 'GOLD', Fore.YELLOW)

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
    return os.path.join(SAVE_DIR, f"{player_name}_{save_name}.pickle")

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
                         "Brawlcub", "Aquafin", "Blazehound", "Groundmole", "Thunderwing", "Psyowl", "Vinewhip", 
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

        # Apply trainer level cap if applicable
        if player and hasattr(player, 'trainer_level'):
            if self.level >= player.trainer_level:
                # Monster is at or above trainer level, don't level up
                print(f"{Fore.YELLOW}Warning: {self.name} cannot level up beyond your trainer level ({player.trainer_level}).{Style.RESET_ALL}")
                self.exp = self.exp_to_level - 1  # Cap exp just below next level
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
        self.inventory: Dict[Item, int] = {}  # Item -> quantity
        self.money = 500
        self.location = "Hometown"
        self.trainer_level = 5  # Starting level
        self.exp = 0
        self.exp_to_level = 100  # Initial exp needed to level up

        # Initialize story progress tracking
        self.story_progress = {}

        # Initialize quest items
        self.quest_items = []

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
                           "Mudcrawl", "Sparktail", "Glowbug", "Pebblite", "Whistleaf", "Marshwiggle", "Frostbite",
                           "Magmite", "Crystalwing", "Spiritwisp", "Bonechip", "Aquadrop", "Cloudpuff", "Sandwhirl", 
                           "Icecube", "Voltbug", "Moonbeam", "Shadowmite", "Starling"]

        uncommon_monsters = ["Floracat", "Emberbear", "Coralfish", "Boltfox", "Frostbite", "Shadowpaw", "Fairybell", "Brawlcub",
                             "Aquafin", "Blazehound", "Groundmole", "Thunderwing", "Psyowl", "Vinewhip", "Glacierclaw", "Metalbeak",
                             "Lavahound", "Gemguard", "Mysticfox", "Ghosthowl", "Tidalwave", "Stormbird", "Dunestrider", 
                             "Blizzardclaw", "Technowolf", "Dreamcatcher", "Voidwalker", "Cosmicowl"]

        # Define rare monsters that appear in special locations - NOW INCLUDING ALL NEW RARES!
        rare_monsters = ["Rockbehemoth", "Psyowl", "Drakeling", "Tornadash", "Volcanix", "Abyssal", "Spectralord",
                        "Pyrothane", "Crystalking", "Templeguard", "Banshee", "Leviathor", "Skydragon", "Mirageous", 
                        "Glacialtitan", "Cybernetic", "Naturelord", "Shadowlord", "Starhawk",
                        "Infernus", "Terravore", "Dreadspirit", "Aquabyss", "Stormrage", "Netherbeast", "Crystallord",
                        "Technocore", "Forestguard", "Voidreaper"]

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
                ["Flamouse", "Buzzer", "Shadowpaw", "Vinewhip"], 
                forest_rares
            ),
            "Cave": (
                ["Rockling", "Buzzer", "Toxifrog", "Pebblite"], 
                ["Flamouse", "Boltfox", "Shadowpaw", "Groundmole"], 
                cave_rares
            ),
            "Beach": (
                ["Puddlet", "Coralfish", "Flutterwing", "Aquafin"], 
                ["Buzzer", "Rockling", "Fairybell", "Marshwiggle"], 
                beach_rares
            ),
            "Mountain": (
                ["Rockling", "Flamouse", "Frostbite", "Glowbug"], 
                ["Buzzer", "Floracat", "Brawlcub", "Metalbeak"], 
                mountain_rares
            ),
            "Snowy Peaks": (
                ["Frostbite", "Flutterwing", "Glacierclaw"], 
                ["Brawlcub", "Fairybell", "Metalbeak"], 
                snow_rares
            ),
            "Ancient Ruins": (
                ["Shadowpaw", "Toxifrog", "Psyowl"], 
                ["Psyowl", "Brawlcub", "Sparktail"], 
                ruins_rares
            ),
            "Hometown": (
                common_monsters[:4], uncommon_monsters[:4], []
            ),  # Limited selection in hometown

            # Amazing new locations with their unique monster pools!
            "Volcanic Crater": (
                ["Magmite", "Flamouse", "Rockling", "Sparktail"], 
                ["Lavahound", "Emberbear", "Blazehound", "Metalbeak"], 
                ["Pyrothane", "Volcanix", "Infernus"]  # Now includes new rare Infernus!
            ),
            "Crystal Caverns": (
                ["Crystalwing", "Glowbug", "Rockling", "Pebblite"], 
                ["Gemguard", "Metalbeak", "Boltfox", "Glacierclaw"], 
                ["Crystalking", "Terravore", "Crystallord"]  # Now includes new rares Terravore & Crystallord!
            ),
            "Mystic Temple": (
                ["Spiritwisp", "Moonbeam", "Shadowmite", "Toxifrog"], 
                ["Mysticfox", "Psyowl", "Fairybell", "Shadowpaw"], 
                ["Templeguard", "Spectralord", "Forestguard"]  # Now includes new rare Forestguard!
            ),
            "Haunted Graveyard": (
                ["Bonechip", "Spiritwisp", "Shadowmite", "Toxifrog"], 
                ["Ghosthowl", "Shadowpaw", "Psyowl", "Fairybell"], 
                ["Banshee", "Dreadspirit", "Voidreaper"]  # Now includes new rares Dreadspirit & Voidreaper!
            ),
            "Underwater City": (
                ["Aquadrop", "Puddlet", "Coralfish", "Marshwiggle"], 
                ["Tidalwave", "Aquafin", "Coralfish", "Groundmole"], 
                ["Leviathor", "Abyssal", "Aquabyss"]  # Now includes new rare Aquabyss!
            ),
            "Sky Islands": (
                ["Cloudpuff", "Flutterwing", "Starling", "Buzzer"], 
                ["Stormbird", "Thunderwing", "Metalbeak", "Boltfox"], 
                ["Skydragon", "Tornadash", "Stormrage"]  # Now includes new rare Stormrage!
            ),
            "Desert Oasis": (
                ["Sandwhirl", "Glowbug", "Rockling", "Mudcrawl"], 
                ["Dunestrider", "Blazehound", "Groundmole", "Brawlcub"], 
                ["Mirageous", "Terraquake", "Netherbeast"]  # Now includes new rare Netherbeast!
            ),
            "Frozen Wasteland": (
                ["Icecube", "Frostbite", "Crystalwing", "Cloudpuff"], 
                ["Blizzardclaw", "Glacierclaw", "Fairybell", "Metalbeak"], 
                ["Glacialtitan", "Tempestus", "Crystallord"]  # Now includes new rare Crystallord!
            ),
            "Neon City": (
                ["Voltbug", "Sparktail", "Glowbug", "Buzzer"], 
                ["Technowolf", "Boltfox", "Thunderwing", "Metalbeak"], 
                ["Cybernetic", "Technocore", "Crystallord"]  # Now includes new rare Technocore!
            ),
            "Enchanted Grove": (
                ["Moonbeam", "Leaflet", "Flutterwing", "Whistleaf"], 
                ["Dreamcatcher", "Floracat", "Vinewhip", "Fairybell"], 
                ["Naturelord", "Vitalia", "Forestguard"]  # Now includes new rare Forestguard!
            ),
            "Shadow Realm": (
                ["Shadowmite", "Spiritwisp", "Bonechip", "Toxifrog"], 
                ["Voidwalker", "Shadowpaw", "Ghosthowl", "Psyowl"], 
                ["Shadowlord", "Voidreaper", "Dreadspirit"]  # Now includes new rares Voidreaper & Dreadspirit!
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
                self.show_load_game_menu()
                # Game loop will be started directly after loading, so we can return here
                return
            elif choice == "3":
                # Quit game
                print("\nThank you for playing World of Monsters!")
                self.running = False
                return
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
                input("Press Enter to continue...")

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

        input("\nPress Enter to continue...")

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

        while True:
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

            choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}")

            if choice == "4":
                return

            if choice in ["1", "2", "3"]:
                slot_idx = int(choice) - 1
                save_name = save_slots[slot_idx]

                # Confirm overwrite if slot already has a save
                if save_name in saved_games:
                    confirm = input(f"{Fore.YELLOW}This slot already has a saved game. Overwrite? (y/n): {Style.RESET_ALL}").lower()
                    if confirm != 'y' and confirm != 'yes':
                        continue

                # Save the game
                if self.save_game(save_name):
                    print(f"{Fore.GREEN}Game saved successfully to {save_name}!{Style.RESET_ALL}")
                    input("Press Enter to continue...")
                    return
                else:
                    print(f"{Fore.RED}Failed to save game to {save_name}.{Style.RESET_ALL}")
                    input("Press Enter to continue...")
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1-4.{Style.RESET_ALL}")
                input("Press Enter to continue...")

    def show_load_game_menu(self):
        """Show load game menu with save slots"""
        # Get save slot information
        save_slots, saved_games = self.get_save_slots()

        while True:
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

            choice = input(f"\n{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}")

            if choice == "4":
                return False

            if choice in ["1", "2", "3"]:
                slot_idx = int(choice) - 1
                save_name = save_slots[slot_idx]

                if save_name in saved_games:
                    # Load the game
                    if self.load_game(save_name):
                        print(f"{Fore.GREEN}Game loaded successfully from {save_name}!{Style.RESET_ALL}")
                        input("Press Enter to continue...")
                        # Start game loop immediately after loading
                        self.game_loop()
                        return True
                    else:
                        print(f"{Fore.RED}Failed to load game from {save_name}.{Style.RESET_ALL}")
                        input("Press Enter to continue...")
                else:
                    print(f"{Fore.RED}No saved game found in {save_name}.{Style.RESET_ALL}")
                    input("Press Enter to continue...")
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1-4.{Style.RESET_ALL}")
                input("Press Enter to continue...")

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
            print(f"{Fore.CYAN}Professor Oak:{Style.RESET_ALL} Welcome to the world of monsters!")
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
                input("Press Enter to try again...")

        return choice

    def game_loop(self):
        """Main game loop"""
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

            # Get and process player command
            command = input(f"\n{Fore.CYAN}What will you do? {Style.RESET_ALL}").strip().lower()
            self.process_command(command)

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
        """Save the current game state to file with comprehensive data preservation"""
        if not self.db_available or not self.player:
            print(f"{Fore.RED}Save functionality is not available.{Style.RESET_ALL}")
            return False

        # Default save name if none provided
        if not save_name:
            player_name = self.player.name if hasattr(self.player, 'name') and self.player.name else "Player"
            save_name = f"{player_name}_save"

        try:
            # Prepare ultimate comprehensive game state for saving
            save_data = {
                # Essential player data
                "player_name": self.player.name,
                "player_location": self.player.location,
                "player_money": self.player.money,
                "player_monsters": self.player.monsters,
                "player_inventory": self.player.inventory,
                "player_active_monster_index": self.player.active_monster_index,
                
                # Enhanced player progression data
                "player_trainer_level": getattr(self.player, 'trainer_level', 5),
                "player_exp": getattr(self.player, 'exp', 0),
                "player_exp_to_level": getattr(self.player, 'exp_to_level', 100),
                "player_skill_points": getattr(self.player, 'skill_points', 0),
                "player_badges": getattr(self.player, 'badges', []),
                "player_titles": getattr(self.player, 'titles', []),
                "player_active_title": getattr(self.player, 'active_title', None),
                
                # Epic storyline progress with detailed tracking
                "story_progress": getattr(self.player, 'story_progress', {}),
                "quest_items": getattr(self.player, 'quest_items', []),
                "story_flags": getattr(self.player, 'story_flags', {}),
                "completed_quests": getattr(self.player, 'completed_quests', []),
                "active_quests": getattr(self.player, 'active_quests', []),
                "npc_relationships": getattr(self.player, 'npc_relationships', {}),
                "unlocked_areas": getattr(self.player, 'unlocked_areas', []),
                "discovered_secrets": getattr(self.player, 'discovered_secrets', []),
                
                # Game progression and world state
                "champion_battles_completed": self.champion_battles_completed,
                "champion_battles_available": getattr(self, 'champion_battles_available', True),
                "turn_count": getattr(self, 'turn_count', 0),
                "game_difficulty": getattr(self, 'game_difficulty', 'normal'),
                "tutorial_completed": getattr(self.player, 'tutorial_completed', False),
                "settings": getattr(self.player, 'settings', {}),
                
                # Monster collection with enhanced details
                "total_monsters_caught": len(self.player.monsters) if self.player.monsters else 0,
                "monsters_by_type": self._get_monster_type_stats(),
                "monsters_by_rarity": self._get_monster_rarity_stats(),
                "highest_level_monster": self._get_highest_monster_level(),
                "fusion_count": self._count_fusion_monsters(),
                "shiny_monsters": self._count_shiny_monsters(),
                "legendary_monsters": self._count_legendary_monsters(),
                "monster_breeding_pairs": getattr(self.player, 'breeding_pairs', []),
                "monster_nicknames": getattr(self.player, 'monster_nicknames', {}),
                
                # Location and exploration tracking
                "locations_visited": self._get_visited_locations(),
                "current_battle_state": None if not self.current_battle else "in_battle",
                "exploration_percentage": self._calculate_exploration_percentage(),
                "hidden_locations_found": getattr(self.player, 'hidden_locations', []),
                "weather_encountered": getattr(self.player, 'weather_types_seen', []),
                "time_of_day_preferences": getattr(self.player, 'time_preferences', {}),
                
                # Battle and competition data
                "battles_won": getattr(self.player, 'battles_won', 0),
                "battles_lost": getattr(self.player, 'battles_lost', 0),
                "monsters_defeated": getattr(self.player, 'monsters_defeated', 0),
                "perfect_victories": getattr(self.player, 'perfect_victories', 0),
                "tournament_wins": getattr(self.player, 'tournament_wins', 0),
                "longest_win_streak": getattr(self.player, 'longest_win_streak', 0),
                "battle_strategies_used": getattr(self.player, 'strategies_used', {}),
                
                # Achievement and progression tracking
                "achievements": self._get_player_achievements(),
                "achievement_progress": getattr(self.player, 'achievement_progress', {}),
                "milestones_reached": getattr(self.player, 'milestones', []),
                "records_set": getattr(self.player, 'personal_records', {}),
                
                # Advanced monster data preservation
                "monster_variants_caught": self._get_variant_stats(),
                "legendary_encounters": getattr(self.player, 'legendary_encounters', 0),
                "rare_spawns_found": getattr(self.player, 'rare_spawns', 0),
                "alpha_monsters_caught": getattr(self.player, 'alpha_monsters', 0),
                "monster_evolution_history": getattr(self.player, 'evolution_history', []),
                
                # Economic and trading data
                "trading_history": getattr(self.player, 'trades_completed', []),
                "shop_purchases": getattr(self.player, 'purchase_history', []),
                "items_sold": getattr(self.player, 'sales_history', []),
                "net_worth": getattr(self.player, 'net_worth', 0),
                "investment_portfolio": getattr(self.player, 'investments', {}),
                
                # Game settings and metadata
                "game_version": "3.0_ultimate",
                "save_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_playtime": getattr(self, 'total_playtime', 0),
                "save_count": getattr(self.player, 'save_count', 0) + 1,
                "last_login": getattr(self.player, 'last_login', time.time()),
                "creation_date": getattr(self.player, 'creation_date', time.time()),
                
                # Session and performance data
                "current_session_time": getattr(self, 'current_session', 0),
                "favorite_monsters": getattr(self.player, 'favorites', []),
                "custom_teams": getattr(self.player, 'saved_teams', []),
                "hotkeys": getattr(self.player, 'hotkey_settings', {}),
                
                # World state preservation
                "world_events_witnessed": getattr(self.player, 'world_events', []),
                "seasonal_progress": getattr(self.player, 'seasonal_data', {}),
                "daily_login_streak": getattr(self.player, 'login_streak', 0),
                "special_event_participation": getattr(self.player, 'event_history', [])
            }

            # Get file path for save
            save_path = get_save_path(self.player.name, save_name)

            # Save to file
            with open(save_path, 'wb') as f:
                pickle.dump(save_data, f)

            print(f"{Fore.GREEN}Game saved successfully as '{save_name}'!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Saved: Level {save_data['player_trainer_level']} trainer with {save_data['total_monsters_caught']} monsters{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Story progress: {len(save_data['story_progress'])} events completed{Style.RESET_ALL}")
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

    def load_game(self, save_name: Optional[str] = None) -> bool:
        """Load a saved game state from file with comprehensive data restoration"""
        if not self.db_available:
            print(f"{Fore.RED}Load functionality is not available.{Style.RESET_ALL}")
            return False

        try:
            if save_name:
                # Load specific save if name is provided
                if not self.player or not hasattr(self.player, 'name'):
                    print(f"{Fore.RED}Cannot load: Player not initialized.{Style.RESET_ALL}")
                    return False

                save_path = get_save_path(self.player.name, save_name)

                if not os.path.exists(save_path):
                    print(f"{Fore.RED}Save '{save_name}' not found.{Style.RESET_ALL}")
                    return False

                with open(save_path, 'rb') as f:
                    save_data = pickle.load(f)
            else:
                # Show available saves for selection
                saves = []
                if os.path.exists(SAVE_DIR):
                    for filename in os.listdir(SAVE_DIR):
                        if filename.endswith('.pickle') and filename != os.path.basename(CHAMPIONS_FILE):
                            try:
                                with open(os.path.join(SAVE_DIR, filename), 'rb') as f:
                                    data = pickle.load(f)
                                    player_name = data.get("player_name", "Unknown")
                                    save_time = data.get("save_time", "Unknown")
                                    saves.append((filename, player_name, save_time))
                            except Exception:
                                # Skip corrupted saves
                                continue

                if not saves:
                    print(f"{Fore.YELLOW}No saved games found.{Style.RESET_ALL}")
                    return False

                print(f"\n{Fore.CYAN}Available saved games:{Style.RESET_ALL}")
                for i, (filename, player, timestamp) in enumerate(saves, 1):
                    save_name = filename.replace('.pickle', '').split('_', 1)[1] if '_' in filename else filename.replace('.pickle', '')
                    print(f"{i}. {save_name} - {player} ({timestamp})")

                choice = input(f"\n{Fore.CYAN}Enter save number to load (or 0 to cancel): {Style.RESET_ALL}")
                try:
                    save_index = int(choice) - 1
                    if save_index < 0:
                        print("Loading cancelled.")
                        return False
                    selected_filename = saves[save_index][0]
                    with open(os.path.join(SAVE_DIR, selected_filename), 'rb') as f:
                        save_data = pickle.load(f)
                except (ValueError, IndexError, FileNotFoundError):
                    print(f"{Fore.RED}Invalid selection or file not found.{Style.RESET_ALL}")
                    return False
                except Exception as e:
                    print(f"{Fore.RED}Error loading save: {e}{Style.RESET_ALL}")
                    return False

            # Apply the comprehensive save data to the current game state
            player = Player(save_data["player_name"])
            player.location = save_data["player_location"]
            player.money = save_data["player_money"]
            player.monsters = save_data["player_monsters"]
            player.inventory = save_data["player_inventory"]
            player.active_monster_index = save_data["player_active_monster_index"]
            
            # Restore enhanced player progression data
            player.trainer_level = save_data.get("player_trainer_level", 5)
            player.exp = save_data.get("player_exp", 0)
            player.exp_to_level = save_data.get("player_exp_to_level", 100)
            
            # Restore epic storyline progress
            player.story_progress = save_data.get("story_progress", {})
            player.quest_items = save_data.get("quest_items", [])
            
            # Restore battle statistics using setattr for dynamic attributes
            setattr(player, 'battles_won', save_data.get("battles_won", 0))
            setattr(player, 'battles_lost', save_data.get("battles_lost", 0))
            setattr(player, 'monsters_defeated', save_data.get("monsters_defeated", 0))
            setattr(player, 'legendary_encounters', save_data.get("legendary_encounters", 0))
            
            # Restore game progression
            self.champion_battles_completed = save_data.get("champion_battles_completed", 0)
            self.champion_battles_available = save_data.get("champion_battles_available", True)
            self.turn_count = save_data.get("turn_count", 0)
            
            # Set the loaded player as the current player
            self.player = player
            
            # Display comprehensive load summary
            print(f"{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Welcome back, {player.name}!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Level {player.trainer_level} trainer with {len(player.monsters)} monsters{Style.RESET_ALL}")
            
            if player.story_progress:
                print(f"{Fore.MAGENTA}Story progress: {len(player.story_progress)} events completed{Style.RESET_ALL}")
            
            if player.quest_items:
                print(f"{Fore.BLUE}Quest items: {', '.join(player.quest_items)}{Style.RESET_ALL}")
            
            achievements = save_data.get("achievements", [])
            if achievements:
                print(f"{Fore.YELLOW}Achievements unlocked: {len(achievements)}{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}Current location: {player.location}{Style.RESET_ALL}")
            
            return True

        except Exception as e:
            print(f"{Fore.RED}Error processing save data: {e}{Style.RESET_ALL}")
            return False

    def fusion_menu(self):
        """Display fusion menu to combine two monsters"""
        if not self.player or len(self.player.monsters) < 2:
            print(f"{Fore.YELLOW}You need at least two monsters to perform fusion.{Style.RESET_ALL}")
            input("Press Enter to continue...")
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
                input("Press Enter to continue...")
                return

            monster1 = self.player.monsters[choice1]
            if monster1.level < FUSION_LEVEL_REQUIREMENT:
                print(f"{Fore.RED}This monster must be at least level {FUSION_LEVEL_REQUIREMENT} for fusion.{Style.RESET_ALL}")
                input("Press Enter to continue...")
                return

            # Get second monster selection
            choice2 = int(input(f"\n{Fore.CYAN}Select second monster (0 to cancel): {Style.RESET_ALL}")) - 1
            if choice2 < 0 or choice2 >= len(self.player.monsters) or choice1 == choice2:
                print("Fusion cancelled or invalid selection.")
                input("Press Enter to continue...")
                return

            monster2 = self.player.monsters[choice2]
            if monster2.level < FUSION_LEVEL_REQUIREMENT:
                print(f"{Fore.RED}This monster must be at least level {FUSION_LEVEL_REQUIREMENT} for fusion.{Style.RESET_ALL}")
                input("Press Enter to continue...")
                return

            # Confirm fusion
            print(f"\n{Fore.YELLOW}You are about to fuse {monster1.get_colored_name()} and {monster2.get_colored_name()}.{Style.RESET_ALL}")
            confirm = input(f"{Fore.RED}This cannot be undone! Proceed? (y/n): {Style.RESET_ALL}").lower()

            if confirm != 'y':
                print("Fusion cancelled.")
                input("Press Enter to continue...")
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

        input("Press Enter to continue...")

    def championship_battle(self):
        """Start a championship battle against powerful trainers"""
        if not self.player or not self.player.has_usable_monster():
            print(f"{Fore.RED}You need at least one healthy monster to challenge the championship.{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return

        # Check if player has enough monsters
        if len(self.player.monsters) < 3:
            print(f"{Fore.RED}You need at least 3 monsters to challenge the championship.{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return

        # Ensure player's monsters are strong enough
        if all(m.level < 20 for m in self.player.monsters):
            print(f"{Fore.RED}Your monsters are too weak for the championship. Train them to at least level 20.{Style.RESET_ALL}")
            input("Press Enter to continue...")
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

        input("\nYour monsters have been fully healed. Press Enter to begin the championship...")

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
                        input("Press Enter to continue...")
                    elif battle.result == "lose":
                        # Player lost the championship
                        print(f"\n{Fore.RED}You have been defeated by {trainer['name']}!{Style.RESET_ALL}")
                        print("Better luck next time...")
                        input("Press Enter to continue...")
                        self.current_battle = None
                        return
                else:
                    # Wild monster's turn
                    wild_result = battle.wild_monster_turn()
                    print("\n" + wild_result)
                    input("Press Enter to continue...")

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
                            input("Press Enter to continue...")
                        else:
                            # All player's monsters fainted
                            print(f"\n{Fore.RED}All your monsters have fainted! You lost to {trainer['name']}.{Style.RESET_ALL}")
                            input("Press Enter to continue...")
                            self.current_battle = None
                            return

            # Trainer defeated
            print(f"\n{Fore.GREEN}You defeated {trainer['name']}!{Style.RESET_ALL}")

            # Heal player's monsters between trainer battles
            for monster in self.player.monsters:
                monster.heal(monster.max_hp // 2)  # Heal 50%

            print("\nYour monsters recovered some HP for the next battle.")
            input("Press Enter to continue...")

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

        input("Press Enter to continue...")

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
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' to see available commands.")
            input("Press Enter to continue...")

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
                input("\nPress Enter to continue...")
                return

            # Check if battle is finished
            if not hasattr(battle, 'is_finished') or battle.is_finished:
                if not hasattr(battle, 'result'):
                    print("\nBattle ended unexpectedly!")
                    self.current_battle = None
                    input("\nPress Enter to continue...")
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
                input("\nPress Enter to continue...")
        else:
            print("Invalid battle command.")
            print("Available commands: fight, catch, switch, item, run")
            input("Press Enter to continue...")

    def explore(self):
        """Explore the current location"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
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
                "You run into Professor Oak who gives you a free Potion!",
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

        input("\nPress Enter to continue...")

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
            "Shadow Peak Shrine": [
                {
                    "id": "shadow_peak_1",
                    "text": f"""As you climb the treacherous paths of Shadow Peak, you notice the mountain seems unnaturally dark,
even in broad daylight. Near the summit, you discover a small shrine partially hidden by rocks.

A tall, cloaked figure stands beside it, motionless until you approach.

{Fore.MAGENTA}Keeper of Shadows:{Style.RESET_ALL} "Few find their way here. Fewer still are worthy of the peak's secrets.
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
                        input("\nPress Enter to continue...")

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

                    input("\nPress Enter to continue...")
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
            input("\nPress Enter to continue...")

    def final_battle(self):
        """The final battle at the Chamber of Sealing"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
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
            input("\nPress Enter to continue...")
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

        input("\nPress Enter to continue...")

    def travel(self):
        """Travel to a different location"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'location'):
            print("Error: Player location not set!")
            input("\nPress Enter to continue...")
            return

        print(f"\nCurrent location: {self.player.location}")
        print("Available locations:")

        if not hasattr(self, 'locations') or not self.locations:
            print("Error: No locations available!")
            input("\nPress Enter to continue...")
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
            choice = int(input("\nEnter location number (0 to cancel): "))
            if choice == 0:
                return

            if 1 <= choice <= len(self.locations):
                destination = self.locations[choice - 1]

                if destination == self.player.location:
                    print("You're already at that location!")
                    input("\nPress Enter to continue...")
                    return

                # Check level requirement
                req_level = location_requirements.get(destination, 1)
                if self.player.trainer_level < req_level:
                    print(f"{Fore.RED}You need to be at least Trainer Level {req_level} to travel to {destination}.{Style.RESET_ALL}")
                    print(f"Your current Trainer Level is {self.player.trainer_level}.")
                    print("Continue exploring and battling to increase your Trainer Level.")
                    input("\nPress Enter to continue...")
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

        input("\nPress Enter to continue...")

    def show_monsters(self, for_fusion=False):
        """Show the player's monsters"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'monsters') or not self.player.monsters:
            print("\nYou don't have any monsters yet!")
            input("\nPress Enter to continue...")
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
            choice = int(input("\nEnter choice: "))

            if choice == 1:
                try:
                    monster_idx = int(input("\nEnter monster number to make active: ")) - 1
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
                    monster_idx = int(input("\nEnter monster number to view details: ")) - 1
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

        input("\nPress Enter to continue...")

    def show_items(self):
        """Show and use the player's inventory items"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'inventory') or not self.player.inventory:
            print("\nYour inventory is empty!")
            input("\nPress Enter to continue...")
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
                choice = int(input("\nEnter choice: "))

                if choice == 1:
                    # Can't use items in battle from this menu
                    if self.current_battle:
                        print("You can't use items from the inventory during battle!")
                        print("Use the 'item' command in battle instead.")
                        input("\nPress Enter to continue...")
                        return

                    try:
                        item_idx = int(input("\nEnter item number to use: ")) - 1
                        if 0 <= item_idx < len(items):
                            item = items[item_idx]
                            if not item:
                                print("Error: Invalid item selection!")
                                input("\nPress Enter to continue...")
                                return

                            # Monster Balls can only be used in battle
                            if hasattr(item, 'effect') and item.effect == "catch":
                                print("You can only use Monster Balls during battle!")
                                input("\nPress Enter to continue...")
                                return

                            # Only healing items need a target
                            if hasattr(item, 'effect') and item.effect in ["heal", "revive"]:
                                # Show monsters
                                if not hasattr(self.player, 'monsters') or not self.player.monsters:
                                    print("You don't have any monsters to use this item on!")
                                    input("\nPress Enter to continue...")
                                    return

                                print("\nChoose a monster to use the item on:")
                                for i, monster in enumerate(self.player.monsters):
                                    if not monster:
                                        continue
                                    monster_name = monster.get_colored_name() if hasattr(monster, 'get_colored_name') else "Monster"
                                    hp_info = f"(HP: {monster.current_hp}/{monster.max_hp})" if hasattr(monster, 'current_hp') and hasattr(monster, 'max_hp') else "(HP: ?/?)"
                                    print(f"{i+1}. {monster_name} {hp_info}")

                                try:
                                    monster_idx = int(input("\nEnter monster number: ")) - 1
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

        input("\nPress Enter to continue...")

    def heal_monsters(self):
        """Heal all monsters (only in Hometown)"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
            return

        if not hasattr(self.player, 'location') or self.player.location != "Hometown":
            print("\nYou can only rest and heal your monsters in your Hometown!")
            input("\nPress Enter to continue...")
            return

        print("\nResting at the Healing Center in your Hometown...")
        time.sleep(1.5)

        # Heal all monsters
        if not hasattr(self.player, 'monsters') or not self.player.monsters:
            print("You don't have any monsters to heal!")
            input("\nPress Enter to continue...")
            return

        try:
            for monster in self.player.monsters:
                if monster and hasattr(monster, 'full_heal'):
                    monster.full_heal()

            print(f"{Fore.GREEN}All your monsters have been fully healed!{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error healing monsters: {str(e)}")

        input("\nPress Enter to continue...")

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
        input("\nPress Enter to continue...")

    def quit_game(self):
        """Quit the game with confirmation"""
        confirm = input("\nAre you sure you want to quit? (y/n): ").lower()
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
            input("\nPress Enter to continue...")
            return

        # Switch to first usable monster if active is fainted
        if self.player.active_monster is None or self.player.active_monster.is_fainted():
            idx = self.player.get_first_usable_monster_index()
            if idx >= 0:
                self.player.switch_active_monster(idx)

        # Create and start battle
        clear_screen()
        
        # Enhanced encounter messages based on monster type and level
        encounter_msg = self.generate_encounter_message(wild_monster)
        print(f"\n{encounter_msg}")
        time.sleep(1.5)
        
        # Additional context based on monster rarity and level
        context_msg = self.generate_context_message(wild_monster)
        if context_msg:
            print(f"\n{context_msg}")
            time.sleep(1)

        self.current_battle = Battle(self.player, wild_monster)

    def generate_encounter_message(self, wild_monster: Monster) -> str:
        """Generate dynamic encounter messages based on monster characteristics"""
        monster_type = wild_monster.type.lower()
        name = wild_monster.get_colored_name()
        
        # Base encounter messages by type
        type_encounters = {
            "fire": [
                f"{Fore.RED}🔥 The air shimmers with heat as {name} emerges from flickering flames!{Style.RESET_ALL}",
                f"{Fore.RED}🔥 Embers dance around {name} as it blocks your path with fiery determination!{Style.RESET_ALL}",
                f"{Fore.RED}🔥 A wave of scorching heat announces {name}'s aggressive presence!{Style.RESET_ALL}"
            ],
            "water": [
                f"{Fore.BLUE}💧 {name} rises from the depths, water cascading from its form!{Style.RESET_ALL}",
                f"{Fore.BLUE}💧 Mist swirls as {name} emerges from a nearby water source!{Style.RESET_ALL}",
                f"{Fore.BLUE}💧 The sound of rushing water precedes {name}'s graceful appearance!{Style.RESET_ALL}"
            ],
            "electric": [
                f"{Fore.YELLOW}⚡ Static electricity fills the air as {name} appears in a flash of lightning!{Style.RESET_ALL}",
                f"{Fore.YELLOW}⚡ Sparks crackle around {name} as it materializes with electric energy!{Style.RESET_ALL}",
                f"{Fore.YELLOW}⚡ The air hums with power as {name} charges into view!{Style.RESET_ALL}"
            ],
            "grass": [
                f"{Fore.GREEN}🌿 {name} rustles through the vegetation, blending with nature itself!{Style.RESET_ALL}",
                f"{Fore.GREEN}🌿 Leaves and vines part as {name} steps forward from the greenery!{Style.RESET_ALL}",
                f"{Fore.GREEN}🌿 The scent of fresh earth accompanies {name}'s natural emergence!{Style.RESET_ALL}"
            ],
            "rock": [
                f"{Fore.CYAN}🗿 The ground trembles as {name} rises from the rocky terrain!{Style.RESET_ALL}",
                f"{Fore.CYAN}🗿 Stone fragments scatter as {name} emerges with geological might!{Style.RESET_ALL}",
                f"{Fore.CYAN}🗿 {name} appears solid and unmovable, like an ancient monument!{Style.RESET_ALL}"
            ],
            "dark": [
                f"{Fore.MAGENTA}🌙 Shadows coalesce into the menacing form of {name}!{Style.RESET_ALL}",
                f"{Fore.MAGENTA}🌙 From the darkness steps {name}, eyes gleaming with mysterious intent!{Style.RESET_ALL}",
                f"{Fore.MAGENTA}🌙 The very air grows cold as {name} materializes from the void!{Style.RESET_ALL}"
            ],
            "fairy": [
                f"{Fore.LIGHTMAGENTA_EX}✨ {name} appears in a shower of glittering stardust!{Style.RESET_ALL}",
                f"{Fore.LIGHTMAGENTA_EX}✨ Magical energy swirls as {name} gracefully descends!{Style.RESET_ALL}",
                f"{Fore.LIGHTMAGENTA_EX}✨ The air sparkles with enchantment as {name} materializes!{Style.RESET_ALL}"
            ],
            "psychic": [
                f"{Fore.MAGENTA}🔮 Reality bends as {name} appears through psychic distortion!{Style.RESET_ALL}",
                f"{Fore.MAGENTA}🔮 Your thoughts feel heavy as {name} emerges with mental prowess!{Style.RESET_ALL}",
                f"{Fore.MAGENTA}🔮 {name} materializes, its presence affecting the very fabric of space!{Style.RESET_ALL}"
            ]
        }
        
        # Get appropriate message for monster type
        if monster_type in type_encounters:
            return random.choice(type_encounters[monster_type])
        else:
            # Default encounter message
            return f"{Fore.RED}A wild {name} appeared with fierce determination!{Style.RESET_ALL}"

    def generate_context_message(self, wild_monster: Monster) -> str:
        """Generate additional context messages based on monster characteristics"""
        rarity = getattr(wild_monster, 'rarity', 'common')
        is_fusion = getattr(wild_monster, 'is_fusion', False)
        variant = getattr(wild_monster, 'variant', None)
        
        context_messages = []
        
        # Level-based messages
        if wild_monster.level >= 45:
            context_messages.append(f"{Fore.RED}⚠️  This monster radiates incredible power - approach with extreme caution!{Style.RESET_ALL}")
        elif wild_monster.level >= 35:
            context_messages.append(f"{Fore.YELLOW}⚠️  You sense this is a formidable opponent that won't go down easily!{Style.RESET_ALL}")
        elif wild_monster.level >= 25:
            context_messages.append(f"{Fore.CYAN}ℹ️  This monster appears experienced and battle-hardened!{Style.RESET_ALL}")
        elif wild_monster.level <= 10:
            context_messages.append(f"{Fore.GREEN}ℹ️  This young monster seems curious rather than aggressive!{Style.RESET_ALL}")
        
        # Rarity-based messages
        if rarity == 'legendary':
            context_messages.append(f"{Fore.LIGHTYELLOW_EX}👑 Legendary aura detected! This encounter is extraordinarily rare!{Style.RESET_ALL}")
        elif rarity == 'epic':
            context_messages.append(f"{Fore.MAGENTA}💜 Epic energy emanates from this remarkable creature!{Style.RESET_ALL}")
        elif rarity == 'rare':
            context_messages.append(f"{Fore.BLUE}💎 This monster possesses an uncommon presence!{Style.RESET_ALL}")
        
        # Fusion monster messages
        if is_fusion:
            context_messages.append(f"{Fore.CYAN}🔄 This appears to be a fusion monster - a unique hybrid creation!{Style.RESET_ALL}")
        
        # Variant messages
        if variant:
            if variant == 'shiny':
                context_messages.append(f"{Fore.YELLOW}✨ This monster has an unusual, shimmering appearance!{Style.RESET_ALL}")
            elif variant == 'alpha':
                context_messages.append(f"{Fore.RED}🔺 This is an Alpha variant - larger and more aggressive than normal!{Style.RESET_ALL}")
        
        # Health status message
        if hasattr(wild_monster, 'current_hp') and hasattr(wild_monster, 'max_hp'):
            health_ratio = wild_monster.current_hp / wild_monster.max_hp
            if health_ratio < 0.3:
                context_messages.append(f"{Fore.RED}💔 The monster appears wounded and desperate!{Style.RESET_ALL}")
            elif health_ratio > 0.9:
                context_messages.append(f"{Fore.GREEN}💚 The monster looks healthy and full of energy!{Style.RESET_ALL}")
        
        # Combat prediction based on player's strongest monster
        if self.player and self.player.monsters:
            player_max_level = max(m.level for m in self.player.monsters if m and not m.is_fainted())
            level_diff = wild_monster.level - player_max_level
            
            if level_diff > 10:
                context_messages.append(f"{Fore.RED}⚠️  This monster significantly outlevels your team!{Style.RESET_ALL}")
            elif level_diff > 5:
                context_messages.append(f"{Fore.YELLOW}⚠️  This will be a challenging battle for your current team!{Style.RESET_ALL}")
            elif level_diff < -10:
                context_messages.append(f"{Fore.GREEN}ℹ️  Your experienced team should handle this encounter well!{Style.RESET_ALL}")
        
        return random.choice(context_messages) if context_messages else ""

    def start_puzzle(self):
        """Start a puzzle that can lead to legendary monster encounters"""
        if not self.player:
            print("Error: No active player!")
            input("\nPress Enter to continue...")
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
            input("\nPress Enter to continue...")
            return

        # Select the legendary for this location
        legendary_name = random.choice(location_legendaries)
        legendary_data = legendary_info[legendary_name]

        # Check if player's monsters are strong enough
        if not any(monster.level >= 30 for monster in self.player.monsters if monster):
            print(f"{Fore.RED}Your monsters aren't strong enough to attempt this challenge.{Style.RESET_ALL}")
            print("Train them to at least level 30 before approaching the temple!")
            input("\nPress Enter to continue...")
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
        choice = input("Enter 'yes' to continue or anything else to leave: ").lower()

        if choice != 'yes' and choice != 'y':
            print("\nYou decide to leave the temple for now. Perhaps you'll return when you're better prepared.")
            input("\nPress Enter to continue...")
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
            input("\nPress Enter to continue...")

            # Trigger encounter with the legendary monster
            if legendary_name in self.all_monsters:
                legendary_monster = self.all_monsters[legendary_name].clone()
                # Ensure the legendary is at a challenging level
                legendary_monster.level = max(40, legendary_monster.level)
                legendary_monster.calculate_stats()

                self.start_battle(legendary_monster)
            else:
                print(f"{Fore.RED}Error: Legendary monster not found!{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
        else:
            print(f"\n{Fore.RED}You failed to solve the puzzle.{Style.RESET_ALL}")
            print(f"The {legendary_color}{temple_name}{Style.RESET_ALL} grows quiet, as if disappointed.")
            print("You can try again later after training more with your monsters.")
            input("\nPress Enter to continue...")

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
            player_answer = int(input("\nEnter the next number in the sequence: "))
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

        answer = input("\nYour answer: ").lower().strip()
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
        pairs = input("Enter your pairs: ")

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
            move = input("Which way do you go? ").lower().strip()

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
            input("\nPress Enter to continue...")
            return

        # Check if player has strong enough monsters for a legendary encounter
        if not any(monster.level >= 35 for monster in self.player.monsters if monster):
            print(f"{Fore.RED}Your monsters aren't strong enough for legendary encounters.{Style.RESET_ALL}")
            print("Train them to at least level 35 first!")
            input("\nPress Enter to continue...")
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
            input("\nPress Enter to continue...")
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
        legendary_monster = self.all_monsters[legendary_name].clone()

        # Ensure it's a high level for challenge
        legendary_monster.level = max(40, legendary_monster.level)
        legendary_monster.calculate_stats()

        # Create a dramatic encounter
        clear_screen()
        print(f"{Fore.YELLOW}===== LEGENDARY ENCOUNTER ====={Style.RESET_ALL}\n")

        # Show environmental effect based on monster type
        env_message = "The atmosphere changes dramatically..."
        print(f"{Fore.CYAN}{env_message}{Style.RESET_ALL}")
        time.sleep(2)

        # Describe the environment
        print(f"\n{Fore.CYAN}You stand in an ancient place of power...{Style.RESET_ALL}")
        time.sleep(1.5)

        # Build tension
        print("\nA powerful presence approaches... reality itself seems to bend in its wake...")
        time.sleep(1.5)

        # Describe the legendary's appearance
        legendary_description = legendary_info_data.get("description", "A magnificent legendary monster")

        print(f"\n{legendary_color}{legendary_name}{Style.RESET_ALL} appears before you!")
        time.sleep(1)
        print(f"{Fore.CYAN}{legendary_description}{Style.RESET_ALL}")
        time.sleep(2)

        # Epic encounter message based on monster type
        encounter_messages = {
            "Dragon": f"The legendary {legendary_name} regards you with ancient eyes that have witnessed the passing of eons...",
            "Fairy": f"The very air sparkles around {legendary_name}, as if reality is being rewritten by its presence...",
            "Fire": f"Waves of intense heat roll off {legendary_name}'s body, scorching the ground where it stands...",
            "Rock": f"The earth itself seems to bow to {legendary_name}, gems and crystals forming in its footsteps...",
            "Dark": f"An aura of infinite darkness surrounds {legendary_name}, pulling at the edges of your vision...",
            "Electric": f"Bolts of lightning dance across {legendary_name}'s form, striking the ground in a display of raw power...",
            "Ground": f"The very earth rises to form a pedestal beneath {legendary_name}, acknowledging its mastery...",
            "Psychic": f"Your thoughts feel exposed as {legendary_name}'s mental power washes over you like waves..."
        }

        # Use the encounter message for this legendary type
        type_message = encounter_messages.get(legendary_type, f"The legendary {legendary_name} exudes an aura of immense power...")
        print(f"\n{legendary_color}{type_message}{Style.RESET_ALL}")
        time.sleep(2)

        print(f"\n{Fore.YELLOW}This will be your greatest challenge yet. Are you ready to face this legendary creature?{Style.RESET_ALL}")
        input("\nPress Enter to begin the battle...")

        # Start the battle
        self.start_battle(legendary_monster)


# Main entry point
if __name__ == "__main__":
    # Initialize colorama
    init(autoreset=True)

    try:
        # Then check if launched through launcher
        if os.environ.get("LAUNCHED_FROM_LAUNCHER") != "1":
            print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
            print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
            input("Press Enter to exit...")
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
