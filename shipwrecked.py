import os
import time
import json
import random
import colorama
import glob
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Modding system
def load_mods():
    """Load all available mods from the mods directory"""
    mods_data = {
        "locations": {},
        "items": {},
        "recipes": {},
        "enemies": {},
        "events": {}
    }
    
    # Get all mod directories
    mod_dirs = [d for d in glob.glob("mods/*/") if os.path.isdir(d)]
    
    for mod_dir in mod_dirs:
        mod_info_path = os.path.join(mod_dir, "mod_info.json")
        
        # Skip if mod_info.json doesn't exist
        if not os.path.exists(mod_info_path):
            continue
            
        try:
            # Load mod info
            with open(mod_info_path, 'r') as f:
                mod_info = json.load(f)
                
            print(f"{Fore.GREEN}Loading mod: {mod_info.get('name', 'Unknown')}{Style.RESET_ALL}")
            
            # Load locations
            locations_path = os.path.join(mod_dir, "locations.json")
            if os.path.exists(locations_path):
                with open(locations_path, 'r') as f:
                    locations_data = json.load(f)
                    if "new_locations" in locations_data:
                        mods_data["locations"].update(locations_data["new_locations"])
            
            # Load items
            items_path = os.path.join(mod_dir, "items.json")
            if os.path.exists(items_path):
                with open(items_path, 'r') as f:
                    items_data = json.load(f)
                    if "new_items" in items_data:
                        mods_data["items"].update(items_data["new_items"])
            
            # Load recipes
            recipes_path = os.path.join(mod_dir, "recipes.json")
            if os.path.exists(recipes_path):
                with open(recipes_path, 'r') as f:
                    recipes_data = json.load(f)
                    if "new_recipes" in recipes_data:
                        mods_data["recipes"].update(recipes_data["new_recipes"])
                        
            # Load enemies
            enemies_path = os.path.join(mod_dir, "enemies.json")
            if os.path.exists(enemies_path):
                with open(enemies_path, 'r') as f:
                    enemies_data = json.load(f)
                    if "new_enemies" in enemies_data:
                        mods_data["enemies"].update(enemies_data["new_enemies"])
                        
            # Load events
            events_path = os.path.join(mod_dir, "events.json")
            if os.path.exists(events_path):
                with open(events_path, 'r') as f:
                    events_data = json.load(f)
                    if "new_events" in events_data:
                        mods_data["events"].update(events_data["new_events"])
                
        except Exception as e:
            print(f"{Fore.RED}Error loading mod from {mod_dir}: {str(e)}{Style.RESET_ALL}")
            
    return mods_data

class GameState:
    def __init__(self) -> None:
        # Player stats
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.energy = 100
        
        # Game progress
        self.days_survived = 1
        self.time_of_day = "Morning"  # Morning, Afternoon, Evening, Night
        self.current_location = "Beach"
        self.explored_locations = ["Beach"]
        self.has_shelter = False
        self.raft_type = "None"  # None, Standard Raft, Improved Raft, Advanced Raft, Ultimate Raft
        self.has_fire = False
        
        # Stronghold attributes
        self.stronghold_followers = 0
        self.available_recruits = []
        self.follower_tasks = {
            "Gathering": 0,
            "Hunting": 0,
            "Defense": 0,
            "Building": 0
        }
        self.stronghold_upgrades = {
            "walls": False,
            "watchtower": False,
            "farm": False,
            "workshop": False
        }
        self.daily_food_production = 0
        self.crafting_efficiency = 0.0
        self.fire_remaining_time = 0
        self.has_raft = False
        self.raft_progress = 0
        self.signal_fire_progress = 0
        self.has_signal_fire = False
        self.has_signal_mirror = False
        self.rescued = False
        self.game_over = False
        self.message = ""
        self.last_enemy_encounter = ""
        self.defeated_enemies = []
        self.loaded_mods = []  # Track loaded mods
        self.mods_enabled = False  # Mods disabled by default
        
        # Quest system
        self.active_quests = {}
        self.completed_quests = {}
        self.failed_quests = {}
        self.story_flags = {}
        self.story_path = "survivor"  # Default story path: survivor, explorer, or conqueror
        self.quest_log = []
        
        # Weather system
        self.weather = "Clear"  # Clear, Rainy, Stormy, Foggy, Hot
        self.weather_duration = 0  # How many time periods the weather will last
        
        # Inventory
        self.inventory = {
            # Basic resources
            "Wood": 0,
            "Stone": 0,
            "Vine": 0,
            "Leaf": 0,
            "Coconut": 0,
            "Bamboo": 0,
            "Crystal": 0,
            "Metal": 0,
            "Clay": 0,
            "Obsidian": 0,
            "Sand": 0,
            
            # Food items
            "Fruit": 0,
            "Berry": 0,
            "Fish": 0, 
            "Small Fish": 0,
            "Medium Fish": 0,
            "Large Fish": 0,
            "Exotic Fish": 0,
            "Meat": 0,
            "Small Game": 0,
            "Wild Pig Meat": 0,
            "Venison": 0,
            "Chicken": 0,
            "Exotic Bird": 0,
            "Mushroom": 0,
            "Exotic Fruit": 0,
            "Seaweed": 0,
            "Fresh Water": 0,
            
            # Tools and equipment
            "Spear": 0,
            "Fishing Rod": 0,
            "Water Container": 0,
            "Torch": 0,
            "Bandage": 0,
            "Map": 0,
            "Compass": 0,
            "Axe": 0,
            "Pickaxe": 0,
            "Bow and Arrow": 0,
            "Rope": 0,
            "Slingshot": 0,
            "Waterskin": 0,
            "Medicinal Potion": 0,
            
            # Crafting materials
            "Hide": 0,
            "Feather": 0,
            "Colorful Feather": 0,
            
            # Special items
            "Pirate Treasure": 0,
            "Ancient Artifact": 0,
            "Ship Parts": 0,
            "Signal Mirror": 0
        }
        
        # Available locations and their unlock status
        self.locations = {
            # Starting locations
            "Beach": True,
            "Forest": True,
            
            # Original locations
            "Mountain": False,
            "Cave": False,
            "Waterfall": False,
            "Abandoned Hut": False,
            "Shipwreck": False,
            "Shelter": False,
            "Jungle": False,
            "Cliff Side": False,
            "Ancient Ruins": False,
            "Swamp": False,
            "Coral Reef": False,
            "Volcanic Area": False,
            "Hidden Valley": False,
            "Lagoon": False,
            "Underground Lake": False,
            "Pirate Camp": False,
            "Bamboo Grove": False,
            "Crystal Cave": False,
            "Mangrove Shore": False,
            "Quicksand Pit": False,
            "Hidden Cove": False,
            "Island Summit": False,
            "Abandoned Mine": False,
            
            # New locations
            "Tidal Pools": False,
            "Coconut Grove": False,
            "Volcanic Hot Springs": False,
            "Ancient Temple": False,
            "Mysterious Lighthouse": False,
            "Coral Gardens": False,
            "Native Village": False,
            "Dense Rainforest": False,
            "Rocky Cliffs": False,
            "Whale Graveyard": False,
            "Lava Tubes": False,
            "Misty Peaks": False,
            "Abandoned Research Station": False,
            "Haunted Shipwreck": False,
            "Sunken Vessel": False,
            "Stronghold": False,
        }
        
        # Island map with connections (will be randomized before saving)
        self.island_map = {
            # Default starting locations
            "Beach": ["Forest", "Coral Reef", "Shipwreck", "Mangrove Shore"],
            "Forest": ["Beach", "Mountain", "Waterfall", "Jungle", "Bamboo Grove"],
            "Mountain": ["Forest", "Cave", "Cliff Side", "Volcanic Area", "Island Summit"],
            "Cave": ["Mountain", "Underground Lake", "Abandoned Mine", "Crystal Cave"],
            "Waterfall": ["Forest", "Abandoned Hut", "Lagoon"],
            "Abandoned Hut": ["Waterfall", "Pirate Camp"],
            "Shipwreck": ["Beach", "Hidden Cove"],
            "Jungle": ["Forest", "Swamp", "Ancient Ruins", "Hidden Valley", "Bamboo Grove"],
            "Cliff Side": ["Mountain", "Island Summit"],
            "Ancient Ruins": ["Jungle", "Hidden Valley", "Pirate Camp"],
            "Swamp": ["Jungle", "Quicksand Pit", "Mangrove Shore"],
            "Coral Reef": ["Beach", "Lagoon", "Hidden Cove"],
            "Volcanic Area": ["Mountain", "Island Summit"],
            "Hidden Valley": ["Jungle", "Ancient Ruins"],
            "Lagoon": ["Waterfall", "Coral Reef"],
            "Underground Lake": ["Cave", "Crystal Cave"],
            "Pirate Camp": ["Abandoned Hut", "Ancient Ruins"],
            "Bamboo Grove": ["Forest", "Jungle"],
            "Crystal Cave": ["Cave", "Underground Lake"],
            "Mangrove Shore": ["Beach", "Swamp"],
            "Quicksand Pit": ["Swamp"],
            "Hidden Cove": ["Shipwreck", "Coral Reef"],
            "Island Summit": ["Mountain", "Cliff Side", "Volcanic Area"],
            "Abandoned Mine": ["Cave"]
            # Shelter is not part of the map as it's a craftable location
        }
        
        # Enemies that can be encountered in each location
        self.location_enemies = {
            "Beach": ["Crab", "Seagull"],
            "Forest": ["Wild Boar", "Snake"],
            "Mountain": ["Wolf", "Eagle"],
            "Cave": ["Bear", "Bat Colony"],
            "Waterfall": ["Snake", "Crocodile"],
            "Abandoned Hut": ["Pirate Scout", "Rat Swarm"],
            "Shipwreck": ["Pirate", "Shark"],
            "Jungle": ["Jaguar", "Monkey Tribe", "Wild Boar"],
            "Cliff Side": ["Eagle", "Wolf"],
            "Ancient Ruins": ["Pirate Captain", "Snake"],
            "Swamp": ["Crocodile", "Poisonous Frog"],
            "Coral Reef": ["Shark", "Jellyfish"],
            "Volcanic Area": ["Wild Boar", "Fire Snake"],
            "Hidden Valley": ["Wolf Pack", "Wild Boar"],
            "Lagoon": ["Jellyfish", "Crab"],
            "Underground Lake": ["Bat Colony", "Snake"],
            "Pirate Camp": ["Pirate", "Pirate Captain", "Pirate Scout"],
            "Bamboo Grove": ["Monkey Tribe", "Wild Boar"],
            "Crystal Cave": ["Snake", "Bat Colony"],
            "Mangrove Shore": ["Crocodile", "Crab"], 
            "Quicksand Pit": ["Snake", "Poisonous Frog"],
            "Hidden Cove": ["Pirate", "Shark"],
            "Island Summit": ["Eagle", "Wolf Pack"],
            "Abandoned Mine": ["Rat Swarm", "Snake"]
        }

        # Crafting recipes
        self.crafting_recipes = {
            # Basic tools
            "Spear": {"Wood": 1, "Stone": 1, "Vine": 1},
            "Fishing Rod": {"Wood": 2, "Vine": 2},
            "Water Container": {"Coconut": 1},
            "Torch": {"Wood": 1, "Leaf": 3},
            "Bandage": {"Leaf": 3},
            "Map": {"Wood": 1, "Berry": 2},  # Use berry juice as ink
            
            # Advanced tools
            "Axe": {"Wood": 1, "Stone": 2, "Vine": 1},
            "Pickaxe": {"Wood": 1, "Stone": 3, "Vine": 1},
            "Bow and Arrow": {"Wood": 2, "Vine": 3, "Leaf": 2},
            "Slingshot": {"Wood": 1, "Vine": 2},
            "Rope": {"Vine": 4},
            "Waterskin": {"Leaf": 5, "Vine": 2},
            "Compass": {"Metal": 2, "Stone": 1, "Sand": 1},
            "Medicinal Potion": {"Leaf": 3, "Mushroom": 2, "Berry": 1},
            
            # Constructions
            "Shelter": {"Wood": 5, "Leaf": 10, "Vine": 3},
            "Fire": {"Wood": 3, "Stone": 2},
            "Raft": {"Wood": 15, "Vine": 8},
            "Signal Fire": {"Wood": 10, "Leaf": 5},
            "Bamboo Raft": {"Bamboo": 10, "Vine": 5},
            "Strong Shelter": {"Wood": 8, "Stone": 5, "Vine": 4, "Leaf": 15},
            "Stronghold": {"Wood": 30, "Stone": 20, "Metal": 10, "Vine": 15},
            
            # Special items
            "Signal Mirror": {"Metal": 1, "Sand": 2},
            "Obsidian Spear": {"Wood": 1, "Obsidian": 2, "Vine": 2},
            "Metal Tools": {"Metal": 3, "Wood": 2, "Stone": 1}
        }

        # Random events
        self.events = [
            {"name": "Storm", "description": "A violent storm hits the island. ", "effect": self.event_storm},
            {"name": "Wild Animal", "description": "A wild animal approaches your camp. ", "effect": self.event_wild_animal},
            {"name": "Food Spoilage", "description": "Some of your food has spoiled. ", "effect": self.event_food_spoilage},
            {"name": "Ship Sighting", "description": "You see a ship in the distance! ", "effect": self.event_ship_sighting},
            {"name": "Illness", "description": "You don't feel well. You might be getting sick. ", "effect": self.event_illness},
            {"name": "Good Weather", "description": "The weather is perfect today. ", "effect": self.event_good_weather},
            {"name": "Discovery", "description": "You found something interesting! ", "effect": self.event_discovery}
        ]
        
    def add_quest(self, quest_id, title, description, objectives, rewards=None, story_path=None):
        """Add a new quest to the active quests list
        
        Args:
            quest_id (str): Unique identifier for the quest
            title (str): Quest title
            description (str): Quest description and background
            objectives (dict): Dictionary of objectives with their completion status
            rewards (dict, optional): Rewards for completing the quest
            story_path (str, optional): Story path this quest belongs to
        """
        if quest_id in self.active_quests or quest_id in self.completed_quests:
            return False  # Quest already exists
            
        # Create the quest structure
        quest = {
            "id": quest_id,
            "title": title,
            "description": description,
            "objectives": objectives,
            "progress": 0,  # Percentage of completion
            "rewards": rewards or {},
            "story_path": story_path or "any",
            "date_started": self.days_survived,
            "location_started": self.current_location
        }
        
        # Add to active quests
        self.active_quests[quest_id] = quest
        
        # Add to quest log
        log_entry = f"Day {self.days_survived}: Started quest '{title}'"
        self.quest_log.append(log_entry)
        
        return True
        
    def update_quest_objective(self, quest_id, objective_id, value=True):
        """Update a quest objective status
        
        Args:
            quest_id (str): The quest identifier
            objective_id (str): The objective identifier
            value: The value to set (True for completion, or numeric progress for float objectives)
        
        Returns:
            bool: True if quest was completed as a result, False otherwise
        """
        if quest_id not in self.active_quests:
            return False
            
        quest = self.active_quests[quest_id]
        if objective_id not in quest["objectives"]:
            return False
            
        # Update the objective
        quest["objectives"][objective_id] = value
        
        # Check if all objectives are complete
        all_complete = True
        for obj_value in quest["objectives"].values():
            if isinstance(obj_value, bool) and not obj_value:
                all_complete = False
                break
            elif isinstance(obj_value, (int, float)) and obj_value < 1.0:
                all_complete = False
                break
                
        # Calculate progress percentage
        total_objectives = len(quest["objectives"])
        completed = sum(1 for v in quest["objectives"].values() if v is True or v >= 1.0)
        quest["progress"] = int((completed / total_objectives) * 100)
        
        # If all objectives are complete, complete the quest
        if all_complete:
            self.complete_quest(quest_id)
            return True
            
        return False
        
    def complete_quest(self, quest_id):
        """Mark a quest as completed and give rewards
        
        Args:
            quest_id (str): The quest identifier
        """
        if quest_id not in self.active_quests:
            return False
            
        quest = self.active_quests[quest_id]
        quest["date_completed"] = self.days_survived
        
        # Add to completed quests
        self.completed_quests[quest_id] = quest
        
        # Remove from active quests
        del self.active_quests[quest_id]
        
        # Add to quest log
        log_entry = f"Day {self.days_survived}: Completed quest '{quest['title']}'"
        self.quest_log.append(log_entry)
        
        # Apply rewards
        rewards_text = []
        for reward_type, reward_value in quest["rewards"].items():
            if reward_type == "items":
                for item, amount in reward_value.items():
                    if item in self.inventory:
                        self.inventory[item] += amount
                        rewards_text.append(f"{amount} {item}")
            elif reward_type == "story_flag":
                self.story_flags[reward_value] = True
            elif reward_type == "story_path":
                self.story_path = reward_value
            elif reward_type == "location":
                self.locations[reward_value] = True
                rewards_text.append(f"Discovered {reward_value}")
        
        # Return a message about quest completion
        if rewards_text:
            return f"Quest completed: {quest['title']}! Rewards: {', '.join(rewards_text)}"
        else:
            return f"Quest completed: {quest['title']}!"
        
    def fail_quest(self, quest_id, reason):
        """Mark a quest as failed
        
        Args:
            quest_id (str): The quest identifier
            reason (str): The reason for failure
        """
        if quest_id not in self.active_quests:
            return False
            
        quest = self.active_quests[quest_id]
        quest["date_failed"] = self.days_survived
        quest["failure_reason"] = reason
        
        # Add to failed quests
        self.failed_quests[quest_id] = quest
        
        # Remove from active quests
        del self.active_quests[quest_id]
        
        # Add to quest log
        log_entry = f"Day {self.days_survived}: Failed quest '{quest['title']}' - {reason}"
        self.quest_log.append(log_entry)
        
        return f"Quest failed: {quest['title']} - {reason}"
    
    def get_available_quests(self):
        """Check for new quests that should be triggered based on current game state"""
        # This will be implemented with specific quest triggers
        new_quests = []
        
        # Check story flags and conditions for new quests
        if self.days_survived == 3 and "started_main_quest" not in self.story_flags:
            # Start the island mystery main quest line after 3 days
            self.story_flags["started_main_quest"] = True
            self.add_quest(
                "island_mystery", 
                "The Island's Secret", 
                "While exploring, you've noticed unusual structures and artifacts. This island seems to hide ancient secrets waiting to be uncovered.",
                {"discover_ruins": False, "find_artifact": False, "translate_markings": False},
                {"items": {"Ancient Artifact": 1}, "story_flag": "ruins_discovered"}
            )
            new_quests.append("The Island's Secret")
            
        # Pirate storyline
        if "Pirate Camp" in self.explored_locations and "pirate_threat" not in self.story_flags:
            self.story_flags["pirate_threat"] = True
            self.add_quest(
                "pirate_threat",
                "Pirate Problem",
                "You've discovered pirates are active on the island. They're looking for something valuable and won't let anyone get in their way.",
                {"spy_on_pirates": False, "find_treasure_map": False, "locate_treasure": False},
                {"items": {"Pirate Treasure": 1}, "story_flag": "pirates_defeated"}
            )
            new_quests.append("Pirate Problem")
            
        # Conqueror storyline - unlocked after defeating pirates
        if "pirates_defeated" in self.story_flags and "conqueror_path" not in self.story_flags:
            self.story_flags["conqueror_path"] = True
            self.add_quest(
                "island_ruler",
                "Island Ruler",
                "With the pirates defeated, you could establish yourself as the ruler of this island. Control the resources and any who may arrive here.",
                {"build_stronghold": False, "collect_resources": False, "defeat_challengers": False},
                {"story_flag": "pirate_king", "story_path": "conqueror"}
            )
            new_quests.append("Island Ruler")
            
        # Ancient temple quest - more explorer/adventure oriented path
        if "Ancient Ruins" in self.explored_locations and "temple_discovery" not in self.story_flags:
            self.story_flags["temple_discovery"] = True
            self.add_quest(
                "temple_mystery",
                "Temple of the Ancients",
                "The ancient ruins contain references to a hidden temple deep in the island. Discovering it could reveal the island's history.",
                {"find_temple_clues": False, "locate_temple": False, "solve_temple_puzzle": False},
                {"items": {"Crystal": 3, "Obsidian": 2}, "story_flag": "temple_secrets", "location": "Ancient Temple"}
            )
            new_quests.append("Temple of the Ancients")
        
        # Rescue/escape quest line - standard survival path
        if self.days_survived >= 5 and "escape_plan" not in self.story_flags:
            self.story_flags["escape_plan"] = True
            self.add_quest(
                "island_escape",
                "Escape Plan",
                "You need to find a way off this island. Building a seaworthy raft or signaling for rescue are your best options.",
                {"build_raft": False, "create_signal": False, "prepare_supplies": False},
                {"story_flag": "ready_for_escape", "story_path": "survivor"}
            )
            new_quests.append("Escape Plan")
        
        return new_quests
        
    def check_story_progress(self):
        """Check for story progression based on completed quests and make world changes"""
        story_updates = []
        
        # Handle main storyline progression
        if "ruins_discovered" in self.story_flags and "temple_secrets" in self.story_flags and "island_mystery_resolved" not in self.story_flags:
            self.story_flags["island_mystery_resolved"] = True
            story_updates.append("You've learned the island was once home to an advanced ancient civilization.")
            
            # Add a follow-up quest
            self.add_quest(
                "ancient_technology",
                "Lost Technology",
                "The ancients left behind powerful technology. Finding it could completely change your situation.",
                {"find_power_source": False, "activate_device": False, "master_technology": False},
                {"story_flag": "ancient_tech_mastered", "story_path": "explorer"}
            )
            story_updates.append("New quest available: Lost Technology")
            
        # Handle pirate storyline
        if "pirates_defeated" in self.story_flags and "pirate_aftermath" not in self.story_flags:
            self.story_flags["pirate_aftermath"] = True
            story_updates.append("With the pirates gone, the island feels safer. You've found their hidden stash of supplies.")
            
            # Add some rewards
            self.inventory["Metal"] += 5
            self.inventory["Rope"] += 3
            self.inventory["Medicinal Potion"] += 2
            
        # Check for story path specialization
        path_changed = False
        if "ancient_tech_mastered" in self.story_flags and self.story_path != "explorer":
            self.story_path = "explorer"
            story_updates.append("You've embraced the path of an explorer, mastering the secrets of the island.")
            path_changed = True
            
        if "pirate_king" in self.story_flags and self.story_path != "conqueror":
            self.story_path = "conqueror"
            story_updates.append("You've become a leader on the island, commanding respect even from the pirates.")
            path_changed = True
            
        if "ready_for_escape" in self.story_flags and self.story_path == "survivor" and not path_changed:
            story_updates.append("You remain focused on survival and escape, taking a practical approach to island life.")
            
        return story_updates
    
    def integrate_mods(self):
        """Load and integrate all available mods"""
        # Check if mods are enabled
        if not self.mods_enabled:
            print(f"{Fore.YELLOW}Mods are currently disabled. Use '/mods enable' to enable them.{Style.RESET_ALL}")
            return
            
        # Load mods from files
        mods_data = load_mods()
        
        # If no mods found, return early
        if not any(mods_data.values()):
            return
            
        print(f"{Fore.GREEN}Integrating mods into game...{Style.RESET_ALL}")
        
        # Add new locations from mods
        for location_name, location_data in mods_data["locations"].items():
            # Add to locations dictionary if not already present
            if location_name not in self.locations:
                self.locations[location_name] = False
                print(f"{Fore.BLUE}Added new location: {location_name}{Style.RESET_ALL}")
                
            # Add location connections to island map
            if "connections" in location_data:
                connections = location_data["connections"]
                if location_name not in self.island_map:
                    self.island_map[location_name] = []
                
                # Add the connections
                for connection in connections:
                    if connection in self.locations:
                        if connection not in self.island_map[location_name]:
                            self.island_map[location_name].append(connection)
                        
                        # Add reverse connection if it exists
                        if connection in self.island_map:
                            if location_name not in self.island_map[connection]:
                                self.island_map[connection].append(location_name)
                
            # Add location enemies
            if "enemies" in location_data:
                enemies = location_data["enemies"]
                if location_name not in self.location_enemies:
                    self.location_enemies[location_name] = []
                    
                # Add enemies to location
                for enemy in enemies:
                    if enemy not in self.location_enemies[location_name]:
                        self.location_enemies[location_name].append(enemy)
        
        # Add new items to inventory
        for item_name in mods_data["items"]:
            if item_name not in self.inventory:
                self.inventory[item_name] = 0
                print(f"{Fore.BLUE}Added new item: {item_name}{Style.RESET_ALL}")
        
        # Add new recipes
        for recipe_name, recipe_ingredients in mods_data["recipes"].items():
            if recipe_name not in self.crafting_recipes:
                self.crafting_recipes[recipe_name] = recipe_ingredients
                print(f"{Fore.BLUE}Added new recipe: {recipe_name}{Style.RESET_ALL}")
                
        # Add mods to loaded mods list
        for mod_dir in glob.glob("mods/*/"):
            mod_name = os.path.basename(os.path.dirname(mod_dir))
            if mod_name not in self.loaded_mods:
                self.loaded_mods.append(mod_name)
                
        print(f"{Fore.GREEN}Mods integration complete!{Style.RESET_ALL}")
        
        # Available locations and their unlock status
        self.locations = {
            # Starting locations
            "Beach": True,
            "Forest": True,
            
            # Original locations
            "Mountain": False,
            "Cave": False,
            "Waterfall": False,
            "Abandoned Hut": False,
            "Shipwreck": False,
            "Shelter": False,
            "Jungle": False,
            "Cliff Side": False,
            "Ancient Ruins": False,
            "Swamp": False,
            "Coral Reef": False,
            "Volcanic Area": False,
            "Hidden Valley": False,
            "Lagoon": False,
            "Underground Lake": False,
            "Pirate Camp": False,
            "Bamboo Grove": False,
            "Crystal Cave": False,
            "Mangrove Shore": False,
            "Quicksand Pit": False,
            "Hidden Cove": False,
            "Island Summit": False,
            "Abandoned Mine": False,
            
            # New locations
            "Tidal Pools": False,
            "Coconut Grove": False,
            "Volcanic Hot Springs": False,
            "Ancient Temple": False,
            "Mysterious Lighthouse": False,
            "Coral Gardens": False,
            "Native Village": False,
            "Dense Rainforest": False,
            "Rocky Cliffs": False,
            "Whale Graveyard": False,
            "Lava Tubes": False,
            "Stronghold": False,
            "Misty Peaks": False,
            "Abandoned Research Station": False,
            "Haunted Shipwreck": False,
            "Sunken Vessel": False
        }
        
        # Island map with connections (will be randomized before saving)
        self.island_map = {
            # Default starting locations
            "Beach": ["Forest", "Coral Reef", "Shipwreck", "Mangrove Shore"],
            "Forest": ["Beach", "Mountain", "Waterfall", "Jungle", "Bamboo Grove"],
            "Mountain": ["Forest", "Cave", "Cliff Side", "Volcanic Area", "Island Summit"],
            "Cave": ["Mountain", "Underground Lake", "Abandoned Mine", "Crystal Cave"],
            "Waterfall": ["Forest", "Abandoned Hut", "Lagoon"],
            "Abandoned Hut": ["Waterfall", "Pirate Camp"],
            "Shipwreck": ["Beach", "Hidden Cove"],
            "Jungle": ["Forest", "Swamp", "Ancient Ruins", "Hidden Valley", "Bamboo Grove"],
            "Cliff Side": ["Mountain", "Island Summit"],
            "Ancient Ruins": ["Jungle", "Hidden Valley", "Pirate Camp"],
            "Swamp": ["Jungle", "Quicksand Pit", "Mangrove Shore"],
            "Coral Reef": ["Beach", "Lagoon", "Hidden Cove"],
            "Volcanic Area": ["Mountain", "Island Summit"],
            "Hidden Valley": ["Jungle", "Ancient Ruins"],
            "Lagoon": ["Waterfall", "Coral Reef"],
            "Underground Lake": ["Cave", "Crystal Cave"],
            "Pirate Camp": ["Abandoned Hut", "Ancient Ruins"],
            "Bamboo Grove": ["Forest", "Jungle"],
            "Crystal Cave": ["Cave", "Underground Lake"],
            "Mangrove Shore": ["Beach", "Swamp"],
            "Quicksand Pit": ["Swamp"],
            "Hidden Cove": ["Shipwreck", "Coral Reef"],
            "Island Summit": ["Mountain", "Cliff Side", "Volcanic Area"],
            "Abandoned Mine": ["Cave"]
            # Shelter is not part of the map as it's a craftable location
        }
        
        # Enemies that can be encountered in each location
        self.location_enemies = {
            "Beach": ["Crab", "Seagull"],
            "Forest": ["Wild Boar", "Snake"],
            "Mountain": ["Wolf", "Eagle"],
            "Cave": ["Bear", "Bat Colony"],
            "Waterfall": ["Snake", "Crocodile"],
            "Abandoned Hut": ["Pirate Scout", "Rat Swarm"],
            "Shipwreck": ["Pirate", "Shark"],
            "Jungle": ["Jaguar", "Monkey Tribe", "Wild Boar"],
            "Cliff Side": ["Eagle", "Wolf"],
            "Ancient Ruins": ["Pirate Captain", "Snake"],
            "Swamp": ["Crocodile", "Poisonous Frog"],
            "Coral Reef": ["Shark", "Jellyfish"],
            "Volcanic Area": ["Wild Boar", "Fire Snake"],
            "Hidden Valley": ["Wolf Pack", "Wild Boar"],
            "Lagoon": ["Jellyfish", "Crab"],
            "Underground Lake": ["Bat Colony", "Snake"],
            "Pirate Camp": ["Pirate", "Pirate Captain", "Pirate Scout"],
            "Bamboo Grove": ["Monkey Tribe", "Wild Boar"],
            "Crystal Cave": ["Snake", "Bat Colony"],
            "Mangrove Shore": ["Crocodile", "Crab"], 
            "Quicksand Pit": ["Snake", "Poisonous Frog"],
            "Hidden Cove": ["Pirate", "Shark"],
            "Island Summit": ["Eagle", "Wolf Pack"],
            "Abandoned Mine": ["Rat Swarm", "Snake"]
        }

        # Crafting recipes
        self.crafting_recipes = {
            # Basic tools
            "Spear": {"Wood": 1, "Stone": 1, "Vine": 1},
            "Fishing Rod": {"Wood": 2, "Vine": 2},
            "Water Container": {"Coconut": 1},
            "Torch": {"Wood": 1, "Leaf": 3},
            "Bandage": {"Leaf": 3},
            "Map": {"Wood": 1, "Berry": 2},  # Use berry juice as ink
            
            # Advanced tools
            "Axe": {"Wood": 1, "Stone": 2, "Vine": 1},
            "Pickaxe": {"Wood": 1, "Stone": 3, "Vine": 1},
            "Bow and Arrow": {"Wood": 2, "Vine": 3, "Leaf": 2},
            "Slingshot": {"Wood": 1, "Vine": 2},
            "Rope": {"Vine": 4},
            "Waterskin": {"Leaf": 5, "Vine": 2},
            "Compass": {"Metal": 2, "Stone": 1, "Sand": 1},
            "Medicinal Potion": {"Leaf": 3, "Mushroom": 2, "Berry": 1},
            
            # Constructions
            "Shelter": {"Wood": 5, "Leaf": 10, "Vine": 3},
            "Fire": {"Wood": 3, "Stone": 2},
            "Raft": {"Wood": 15, "Vine": 8},
            "Signal Fire": {"Wood": 10, "Leaf": 5},
            "Bamboo Raft": {"Bamboo": 10, "Vine": 5},
            "Stronghold": {"Wood": 30, "Stone": 20, "Metal": 10, "Vine": 15},
            "Strong Shelter": {"Wood": 8, "Stone": 5, "Vine": 4, "Leaf": 15},
            
            # Special items
            "Signal Mirror": {"Metal": 1, "Sand": 2},
            "Obsidian Spear": {"Wood": 1, "Obsidian": 2, "Vine": 2},
            "Metal Tools": {"Metal": 3, "Wood": 2, "Stone": 1}
        }

        # Random events
        self.events = [
            {"name": "Storm", "description": "A violent storm hits the island. ", "effect": self.event_storm},
            {"name": "Wild Animal", "description": "A wild animal approaches your camp. ", "effect": self.event_wild_animal},
            {"name": "Food Spoilage", "description": "Some of your food has spoiled. ", "effect": self.event_food_spoilage},
            {"name": "Ship Sighting", "description": "You see a ship in the distance! ", "effect": self.event_ship_sighting},
            {"name": "Illness", "description": "You don't feel well. You might be getting sick. ", "effect": self.event_illness},
            {"name": "Good Weather", "description": "The weather is perfect today. ", "effect": self.event_good_weather},
            {"name": "Discovery", "description": "You found something interesting! ", "effect": self.event_discovery}
        ]

    def event_storm(self) -> str:
        if self.has_shelter:
            result = "Your shelter protects you from the rain."
        else:
            self.health -= 10
            self.energy -= 15
            result = "Without shelter, you get soaked and feel miserable. You lose 10 health and 15 energy."
        
        if self.has_fire and not self.has_shelter:
            self.has_fire = False
            self.fire_remaining_time = 0
            result += " The rain extinguishes your fire."
        
        return result

    def event_wild_animal(self) -> str:
        if self.inventory["Spear"] > 0:
            self.inventory["Meat"] += 2
            return "You defend yourself with your spear and manage to hunt the animal. You gain 2 meat."
        else:
            self.health -= 15
            return "Without a weapon, the animal attacks you. You lose 15 health."

    def event_food_spoilage(self) -> str:
        # All food items that can spoil
        food_items = [
            # Basic items
            "Fruit", "Berry", "Mushroom", "Exotic Fruit", "Seaweed",
            # Fish items
            "Small Fish", "Medium Fish", "Large Fish", "Exotic Fish", "Fish",
            # Meat items
            "Small Game", "Wild Pig Meat", "Venison", "Chicken", "Exotic Bird", "Meat"
        ]
        spoiled = False
        
        for food in food_items:
            if self.inventory[food] > 0:
                spoiled = True
                spoiled_amount = min(self.inventory[food], random.randint(1, 2))
                self.inventory[food] -= spoiled_amount
        
        if spoiled:
            return "Some of your food has spoiled and had to be thrown away."
        else:
            return "Luckily, you had no food that could spoil."

    def event_ship_sighting(self) -> str:
        rescue_chance = 0.0
        result_message = ""
        
        # Signal fire gives a 50% base chance
        if self.has_signal_fire:
            rescue_chance = 0.5
            result_message = "You light your signal fire"
        
        # Signal mirror adds 25% additional chance
        if self.has_signal_mirror:
            if rescue_chance > 0:
                rescue_chance += 0.25
                result_message += " and use your signal mirror to reflect sunlight"
            else:
                rescue_chance = 0.3
                result_message = "You use your signal mirror to reflect sunlight toward the ship"
        
        # Check for rescue
        if rescue_chance > 0:
            if random.random() < rescue_chance:
                self.rescued = True
                return f"{result_message}. The ship has spotted you! They're coming to rescue you!"
            else:
                return f"{result_message}, but the ship passes by without noticing. Maybe next time..."
        else:
            return "Without a signal fire or signal mirror, you have no way to signal the ship. It passes by without noticing you."

    def event_illness(self) -> str:
        self.health -= 8
        self.energy -= 10
        return "You've caught a cold. You lose 8 health and 10 energy."

    def event_good_weather(self) -> str:
        self.energy += 10
        result = "The pleasant weather boosts your morale. You gain 10 energy."
        
        if self.raft_progress > 0 and self.raft_progress < 100:
            progress = random.randint(5, 10)
            self.raft_progress = min(100, self.raft_progress + progress)
            result += f" You make good progress on your raft ({progress}%)."
        
        return result

    def event_discovery(self) -> str:
        # Randomly unlock a new location
        locked_locations = [loc for loc, unlocked in self.locations.items() 
                           if not unlocked and loc not in ["Shelter"]]
        
        if locked_locations:
            new_location = random.choice(locked_locations)
            self.locations[new_location] = True
            return f"You discovered a path to a new area: {new_location}!"
        
        # If no locked locations, give some resources
        resources = [
            "Wood", "Stone", "Vine", "Fruit", "Coconut", "Bamboo", 
            "Crystal", "Metal", "Clay", "Obsidian", "Sand", 
            "Mushroom", "Exotic Fruit", "Seaweed"
        ]
        resource = random.choice(resources)
        amount = random.randint(1, 3)
        self.inventory[resource] += amount
        
        # Small chance to find a special item
        if random.random() < 0.1:
            special_items = ["Compass", "Signal Mirror", "Ship Parts", "Rope"]
            special_item = random.choice(special_items)
            self.inventory[special_item] += 1
            return f"You found {amount} {resource.lower()} and a {special_item.lower()}!"
            
        return f"You found {amount} {resource.lower()}!"
        
    def update_weather(self) -> None:
        """Update the weather conditions based on random chance and duration"""
        # If current weather hasn't expired yet, just decrease duration
        if self.weather_duration > 0:
            self.weather_duration -= 1
            return
            
        # Choose new weather condition
        weather_types = {
            "Clear": 0.5,    # 50% chance of clear weather
            "Rainy": 0.25,   # 25% chance of rain
            "Foggy": 0.1,    # 10% chance of fog
            "Hot": 0.1,      # 10% chance of hot weather
            "Stormy": 0.05   # 5% chance of storm
        }
        
        # Select weather based on weighted probabilities
        rand_val = random.random()
        cumulative_prob = 0
        new_weather = "Clear"  # Default
        
        for weather, prob in weather_types.items():
            cumulative_prob += prob
            if rand_val <= cumulative_prob:
                new_weather = weather
                break
                
        self.weather = new_weather
        
        # Set duration (1-3 days for most weather, shorter for extreme conditions)
        if new_weather == "Stormy":
            self.weather_duration = random.randint(1, 2)  # Storms are shorter
        elif new_weather == "Clear":
            self.weather_duration = random.randint(2, 4)  # Clear weather lasts longer
        else:
            self.weather_duration = random.randint(1, 3)  # Standard duration

    def trigger_random_event(self) -> str:
        # 25% chance of an event each day
        if random.random() < 0.25:
            event = random.choice(self.events)
            result = event["description"] + event["effect"]()
            return result
        return ""

    def update_status(self) -> None:
        # Update time of day
        if self.time_of_day == "Morning":
            self.time_of_day = "Afternoon"
        elif self.time_of_day == "Afternoon":
            self.time_of_day = "Evening"
        elif self.time_of_day == "Evening":
            self.time_of_day = "Night"
        else:  # Night
            self.time_of_day = "Morning"
            self.days_survived += 1
            
            # Update weather
            self.update_weather()
            
            # Stronghold resource generation (for conqueror path)
            if self.locations.get("Stronghold", False) and self.locations["Stronghold"]:
                # Initialize followers if not exists
                if not hasattr(self, 'stronghold_followers'):
                    self.stronghold_followers = 0
                
                # Generate resources at the start of each day
                # Base resources
                base_wood = 3
                base_stone = 2
                base_metal = 1
                
                # Initialize follower tasks if needed
                if not hasattr(self, 'follower_tasks'):
                    self.follower_tasks = {
                        "Gathering": 0,
                        "Hunting": 0,
                        "Defense": 0,
                        "Building": 0
                    }
                
                # Extra resources from followers based on their assigned tasks
                gathering_multiplier = 1.0 + (self.follower_tasks.get("Gathering", 0) * 0.2)
                
                # Calculate resources from followers
                follower_wood = self.stronghold_followers * random.randint(1, 2) * gathering_multiplier
                follower_stone = self.stronghold_followers * random.randint(0, 1) * gathering_multiplier
                follower_metal = int(self.stronghold_followers * 0.5 * gathering_multiplier) if self.stronghold_followers > 0 else 0
                
                # Calculate total resources (rounded to integers)
                wood_gained = int(base_wood + follower_wood + random.randint(0, 2))
                stone_gained = int(base_stone + follower_stone + random.randint(0, 1))
                metal_gained = int(base_metal + follower_metal)
                
                # Food from hunting followers
                hunters = self.follower_tasks.get("Hunting", 0)
                if hunters > 0:
                    food_gained = hunters * random.randint(1, 3)
                    self.inventory["Food"] += food_gained
                
                # Check for farm upgrade
                if hasattr(self, 'stronghold_upgrades') and self.stronghold_upgrades.get("farm", False):
                    farm_food = self.daily_food_production if hasattr(self, 'daily_food_production') else 3
                    self.inventory["Food"] += farm_food
                
                # Add to inventory
                self.inventory["Wood"] += wood_gained
                self.inventory["Stone"] += stone_gained
                self.inventory["Metal"] += metal_gained
                
                # Create message based on followers and resources gathered
                food_message = ""
                
                # Add information about food if any was produced
                hunters = self.follower_tasks.get("Hunting", 0)
                if hunters > 0:
                    food_gained = hunters * random.randint(1, 3)
                    food_message = f" and {food_gained} food from hunting"
                
                # Add information about farm food
                farm_food_message = ""
                if hasattr(self, 'stronghold_upgrades') and self.stronghold_upgrades.get("farm", False):
                    farm_food = self.daily_food_production if hasattr(self, 'daily_food_production') else 3
                    farm_food_message = f" Your farm produced {farm_food} food."
                
                # Create the full message
                if self.stronghold_followers > 0:
                    stronghold_message = f"Your stronghold workers ({self.stronghold_followers} followers) have gathered {wood_gained} wood, {stone_gained} stone, and {metal_gained} metal{food_message} overnight.{farm_food_message}"
                else:
                    stronghold_message = f"Your stronghold has generated {wood_gained} wood, {stone_gained} stone, and {metal_gained} metal overnight.{farm_food_message}"
                
                # Set the message
                if not hasattr(self, 'stronghold_message'):
                    self.stronghold_message = stronghold_message
                else:
                    self.stronghold_message = stronghold_message
                    
                # Random chance to gain a new follower if on conqueror path
                if self.story_path == "conqueror" and random.random() < 0.05:  # 5% chance per day
                    self.stronghold_followers += 1
                    self.stronghold_message += f" A new follower has joined your stronghold! (Total: {self.stronghold_followers})"
            
            # Random events happen at the start of a new day
            self.message = self.trigger_random_event()
        
        # Update stats
        self.hunger -= random.randint(2, 5)
        self.thirst -= random.randint(3, 7)
        energy_loss = random.randint(2, 4)
        
        # Weather effects
        weather_message = ""
        if self.weather == "Rainy":
            # Rain makes you more hungry and tired
            self.hunger -= random.randint(1, 2)
            energy_loss += 2
            weather_message = f" The {self.weather.lower()} weather is wearing you down."
            
            # Rain puts out fires unless sheltered
            if self.has_fire and not self.has_shelter:
                self.has_fire = False
                self.fire_remaining_time = 0
                weather_message += " Your fire has been extinguished by the rain."
        
        elif self.weather == "Stormy":
            # Storms are dangerous and drain resources faster
            self.hunger -= random.randint(2, 3)
            self.thirst -= random.randint(1, 2)
            energy_loss += 4
            weather_message = f" The {self.weather.lower()} weather is harsh and dangerous."
            
            # Storms always put out fires unless sheltered
            if self.has_fire and not self.has_shelter:
                self.has_fire = False
                self.fire_remaining_time = 0
                weather_message += " Your fire has been extinguished by the storm."
        
        elif self.weather == "Foggy":
            # Fog makes exploration more tiring
            energy_loss += 1
            weather_message = f" The {self.weather.lower()} conditions make it harder to navigate."
        
        elif self.weather == "Hot":
            # Hot weather increases thirst but can help with drying/crafting
            self.thirst -= random.randint(2, 4)
            weather_message = f" The {self.weather.lower()} weather is making you extra thirsty."
        
        elif self.weather == "Clear":
            # Clear weather is slightly beneficial
            energy_loss -= 1
            weather_message = f" The {self.weather.lower()} weather lifts your spirits."
        
        # Apply energy loss with minimum of 1
        self.energy -= max(1, energy_loss)
        
        # Add weather message if there is one
        if weather_message and self.time_of_day == "Morning":
            self.message += weather_message
        
        # Night time effects
        if self.time_of_day == "Night":
            if not self.has_shelter:
                health_loss = 5
                energy_loss = 5
                
                # Weather effects at night are more severe without shelter
                if self.weather == "Rainy":
                    health_loss += 3
                    energy_loss += 3
                elif self.weather == "Stormy":
                    health_loss += 6
                    energy_loss += 6
                
                self.health -= health_loss
                self.energy -= energy_loss
                self.message += f" You spent the night exposed to the {self.weather.lower()} elements. -{health_loss} health, -{energy_loss} energy."
            
            if not self.has_fire:
                self.health -= 3
                self.message += " Without a fire, the cold night affected your health. -3 health."
        
        # Check if fire is still burning
        if self.has_fire:
            self.fire_remaining_time -= 1
            if self.fire_remaining_time <= 0:
                self.has_fire = False
                self.message += " Your fire has gone out."
        
        # Health effects from hunger and thirst
        if self.hunger <= 0:
            self.hunger = 0
            self.health -= 10
            self.message += " You're starving! -10 health."
        
        if self.thirst <= 0:
            self.thirst = 0
            self.health -= 15
            self.message += " You're severely dehydrated! -15 health."
        
        # Energy effects
        if self.energy <= 0:
            self.energy = 0
            self.health -= 5
            self.message += " You're exhausted! -5 health."
        
        # Cap stats at max values
        self.hunger = min(100, self.hunger)
        self.thirst = min(100, self.thirst)
        self.energy = min(100, self.energy)
        self.health = min(100, self.health)
        
        # Check game over condition
        if self.health <= 0:
            self.health = 0
            self.game_over = True
            self.message = "You have died. Game Over."
        
        if self.rescued:
            self.game_over = True
            self.message = "Congratulations! You have been rescued and survived the island!"

class GameManager:
    def __init__(self) -> None:
        self.game_state = GameState()
        self.save_slots = 3  # Number of save slots available
        self.current_slot = 1  # Default slot
        self.save_file_template = "shipwrecked_save_{}.json"  # Template for save file names
        self.save_file = self.save_file_template.format(self.current_slot)  # Current save file
        self.map_file = "island_map.json"
        self.mods_loaded = False  # Track if mods have been loaded
        
        # Define the ASCII art for the game title
        self.ascii_title = """
  ███████ ██   ██ ██ ██████  ██     ██ ██████  ███████  ██████ ██   ██ ███████ ██████  
  ██      ██   ██ ██ ██   ██ ██     ██ ██   ██ ██      ██      ██  ██  ██      ██   ██ 
  ███████ ███████ ██ ██████  ██  █  ██ ██████  █████   ██      █████   █████   ██   ██ 
       ██ ██   ██ ██ ██      ██ ███ ██ ██   ██ ██      ██      ██  ██  ██      ██   ██ 
  ███████ ██   ██ ██ ██       ███ ███  ██   ██ ███████  ██████ ██   ██ ███████ ██████  
"""
        
        # Simple text descriptors for enemies instead of ASCII art
        self.ascii_enemies = {
            "Pirate": "[Pirate: Armed and dangerous]",
            "Pirate Scout": "[Pirate Scout: Quick and agile]",
            "Pirate Captain": "[Pirate Captain: Heavily armed leader]",
            "Wolf": "[Wolf: Sharp teeth and keen senses]",
            "Wolf Pack": "[Wolf Pack: Multiple wolves hunting together]",
            "Bear": "[Bear: Large and powerful]",
            "Snake": "[Snake: Slithering predator]",
            "Fire Snake": "[Fire Snake: Venomous with red markings]",
            "Wild Boar": "[Wild Boar: Aggressive with tusks]",
            "Crab": "[Crab: Hard shell with pincers]",
            "Seagull": "[Seagull: Flying coastal bird]",
            "Eagle": "[Eagle: Sharp-eyed predatory bird]",
            "Bat Colony": "[Bat Colony: Group of flying mammals]",
            "Crocodile": "[Crocodile: Powerful reptile with deadly bite]",
            "Rat Swarm": "[Rat Swarm: Many small rodents]",
            "Shark": "[Shark: Ocean predator with many teeth]",
            "Jaguar": "[Jaguar: Spotted jungle hunter]",
            "Monkey Tribe": "[Monkey Tribe: Group of primates]",
            "Poisonous Frog": "[Poisonous Frog: Small but deadly amphibian]",
            "Jellyfish": "[Jellyfish: Translucent with stinging tentacles]"
        }
        
        # Simple text representation of the island map
        self.ascii_island = """
            ~~~~~~~~~~ ISLAND MAP ~~~~~~~~~~
            
              /\\     ~         /\\
             /  \\~~~~         /  \\
            /    \\    /\\     /    \\
           /      \\  /  \\   /      \\
          /        \\/    \\ /        \\
          \\                          /
           \\   o                    /
            \\    ☼                 /
             \\        ^           /
              \\       ^          /
               \\~~~~~~~         /
                ~~~~~~~~~~~~~~~~~
                
            Legend:
            ~ : Ocean    /\\ : Mountains
            o : Beach    ☼  : Ruins
            ^ : Forest
        """
        
        self.ascii_victory = "*** VICTORY: YOU SURVIVED! ***"
        
        self.ascii_game_over = "*** GAME OVER ***"
        
        # Additional ASCII art for special events and locations
        # Ship ASCII art removed, keeping only title ASCII art

        # Island ASCII art removed

        # Shelter ASCII art removed

        # Fire ASCII art removed
        
        # Randomize the island map on first run
        self.randomize_island_map()
    
    def display_intro(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + self.ascii_title)
        print(Fore.WHITE + Style.BRIGHT + "A Survival Text Adventure\n")
        print(Fore.YELLOW + "Your ship was caught in a terrible storm and has sunk.")
        print("You wake up washed ashore on a mysterious island with nothing but")
        print("the clothes on your back. You must survive until rescue arrives,")
        print("or find a way to escape on your own.\n")
        
        # Check for mods without loading them
        if not self.mods_loaded:
            print(Fore.CYAN + "Checking for mods...")
            
            # Count available mods without integrating them
            mod_dirs = [d for d in glob.glob("mods/*/") if os.path.isdir(d) and os.path.exists(os.path.join(d, "mod_info.json"))]
            mod_count = len(mod_dirs)
            
            if mod_count > 0:
                print(Fore.YELLOW + f"Found {mod_count} mod(s). Mods are disabled by default.")
                print(Fore.GREEN + "Use '/mods enable' to enable mods and '/mods info' to see details." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "No mods found. You can add mods to the 'mods' folder.\n" + Style.RESET_ALL)
            
            self.mods_loaded = True
        
        print(Fore.GREEN + "Your journey begins now. Good luck!\n")
        input(Fore.BLUE + "Press Enter to start..." + Style.RESET_ALL)
    
    def display_stats(self) -> None:
        gs = self.game_state
        
        # Determine colors based on status
        health_color = Fore.GREEN if gs.health > 50 else (Fore.YELLOW if gs.health > 25 else Fore.RED)
        hunger_color = Fore.GREEN if gs.hunger > 50 else (Fore.YELLOW if gs.hunger > 25 else Fore.RED)
        thirst_color = Fore.GREEN if gs.thirst > 50 else (Fore.YELLOW if gs.thirst > 25 else Fore.RED)
        energy_color = Fore.GREEN if gs.energy > 50 else (Fore.YELLOW if gs.energy > 25 else Fore.RED)
        
        # Weather color based on condition
        weather_color = Fore.WHITE
        if gs.weather == "Clear":
            weather_color = Fore.GREEN
        elif gs.weather == "Rainy":
            weather_color = Fore.BLUE
        elif gs.weather == "Foggy":
            weather_color = Fore.WHITE
        elif gs.weather == "Hot":
            weather_color = Fore.YELLOW
        elif gs.weather == "Stormy":
            weather_color = Fore.RED
        
        print(f"\n{Fore.CYAN}=========== DAY {gs.days_survived} - {gs.time_of_day} ==========={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Location: {Fore.YELLOW}{gs.current_location}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Weather: {weather_color}{gs.weather}{Style.RESET_ALL}")
        
        # Display status bars
        print(f"{Fore.WHITE}Health:  {health_color}{self.create_bar(gs.health)}{Style.RESET_ALL} {gs.health}%")
        print(f"{Fore.WHITE}Hunger:  {hunger_color}{self.create_bar(gs.hunger)}{Style.RESET_ALL} {gs.hunger}%")
        print(f"{Fore.WHITE}Thirst:  {thirst_color}{self.create_bar(gs.thirst)}{Style.RESET_ALL} {gs.thirst}%")
        print(f"{Fore.WHITE}Energy:  {energy_color}{self.create_bar(gs.energy)}{Style.RESET_ALL} {gs.energy}%")
        
        # Display status indicators
        status_indicators = []
        if gs.has_shelter:
            status_indicators.append(f"{Fore.GREEN}[Shelter Built]")
        if gs.has_fire:
            status_indicators.append(f"{Fore.YELLOW}[Fire Active: {gs.fire_remaining_time} turns]")
        if gs.has_signal_fire:
            status_indicators.append(f"{Fore.RED}[Signal Fire Ready]")
        if gs.has_signal_mirror:
            status_indicators.append(f"{Fore.CYAN}[Signal Mirror Ready]")
        if gs.raft_progress > 0:
            raft_indicator = f"{Fore.BLUE}[Raft: {gs.raft_progress}%"
            if gs.raft_type:
                raft_indicator += f" - {gs.raft_type}"
            raft_indicator += "]"
            status_indicators.append(raft_indicator)
        if gs.locations.get("Stronghold", False) and gs.locations["Stronghold"]:
            status_indicators.append(f"{Fore.GREEN}[Stronghold Built]")
            
        if status_indicators:
            print(f"\nStatus: {' '.join(status_indicators)}{Style.RESET_ALL}")
        
        # Display message
        if gs.message:
            print(f"\n{Fore.MAGENTA}{gs.message}{Style.RESET_ALL}")
            gs.message = ""  # Clear the message after displaying
            
        # Display Stronghold resource generation message if it exists
        if hasattr(gs, 'stronghold_message') and gs.stronghold_message:
            print(f"\n{Fore.GREEN}{gs.stronghold_message}{Style.RESET_ALL}")
            gs.stronghold_message = ""  # Clear the message after displaying
            
    def create_bar(self, value: int) -> str:
        bar_length = 20
        filled_length = int(value / 100 * bar_length)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        return bar
        
    def display_main_menu(self) -> str:
        gs = self.game_state
        
        # Check for new available quests
        new_quests = gs.get_available_quests()
        if new_quests:
            quest_notification = ", ".join(new_quests)
            print(f"\n{Fore.GREEN}New quests available: {quest_notification}{Style.RESET_ALL}")
        
        # Check for story progress
        story_updates = gs.check_story_progress()
        if story_updates:
            for update in story_updates:
                print(f"\n{Fore.MAGENTA}{update}{Style.RESET_ALL}")
        
        # Show active quests notification if any are available
        if gs.active_quests:
            print(f"\n{Fore.CYAN}You have {len(gs.active_quests)} active quest(s). Type {Fore.YELLOW}/quests{Fore.CYAN} to view them.{Style.RESET_ALL}")
        
        # Show the current location with the menu
        print(f"\n{Fore.WHITE}Location: {Fore.YELLOW}{gs.current_location}{Style.RESET_ALL} | Weather: {Fore.CYAN}{gs.weather}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}What would you like to do? (Type a command with / prefix){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/explore {Fore.WHITE}- Explore current location")
        print(f"{Fore.YELLOW}/inventory {Fore.WHITE}- Check inventory")
        print(f"{Fore.YELLOW}/craft {Fore.WHITE}- Craft items")
        print(f"{Fore.YELLOW}/eat {Fore.WHITE}- Eat/Drink")
        print(f"{Fore.YELLOW}/rest {Fore.WHITE}- Rest")
        print(f"{Fore.YELLOW}/travel {Fore.WHITE}- Travel to another location")
        print(f"{Fore.YELLOW}/map {Fore.WHITE}- View island map (requires Map item)")
        print(f"{Fore.YELLOW}/fish {Fore.WHITE}- Go fishing (requires Fishing Rod)")
        print(f"{Fore.YELLOW}/hunt {Fore.WHITE}- Hunt for food (requires Spear)")
        print(f"{Fore.YELLOW}/signal {Fore.WHITE}- Use signal mirror (requires Signal Mirror)")
        print(f"{Fore.YELLOW}/raft {Fore.WHITE}- Build or check your rescue raft")
        print(f"{Fore.YELLOW}/weather {Fore.WHITE}- Detailed weather forecast")
        print(f"{Fore.YELLOW}/stats {Fore.WHITE}- View detailed player statistics")
        print(f"{Fore.YELLOW}/quests {Fore.WHITE}- View your quest log and current quests")
        print(f"{Fore.YELLOW}/story {Fore.WHITE}- View your story progress and path")
        
        # Show stronghold command if player has a stronghold
        if gs.locations.get("Stronghold", False):
            print(f"{Fore.YELLOW}/stronghold {Fore.WHITE}- Manage your stronghold and followers")
        
        print(f"{Fore.YELLOW}/mods {Fore.WHITE}- View information about installed mods")
        print(f"{Fore.YELLOW}/save {Fore.WHITE}- Save game")
        print(f"{Fore.YELLOW}/load {Fore.WHITE}- Load game")
        print(f"{Fore.YELLOW}/quit {Fore.WHITE}- Quit game")
        print(f"{Fore.YELLOW}/help {Fore.WHITE}- Show commands")
        
        while True:
            command = input(f"\n{Fore.GREEN}Enter command: {Style.RESET_ALL}").strip().lower()
            
            if command.startswith('/'):
                command = command[1:]  # Remove the / prefix
                
                if command == 'explore':
                    return '1'
                elif command in ('inventory', 'inv', 'i'):
                    return '2'
                elif command == 'craft':
                    return '3'
                elif command in ('eat', 'drink'):
                    return '4'
                elif command == 'rest':
                    return '5'
                elif command == 'travel':
                    return '6'
                elif command == 'save':
                    return '7'
                elif command == 'load':
                    return '9'  # New option for load
                elif command in ('quit', 'exit', 'q'):
                    return '8'
                elif command == 'map':
                    self.display_map()
                elif command == 'help':
                    self.display_help()
                elif command == 'fish':
                    self.go_fishing()
                elif command == 'hunt':
                    self.go_hunting()
                elif command == 'signal':
                    self.use_signal_mirror()
                elif command == 'raft':
                    self.raft_menu()
                elif command == 'weather':
                    self.weather_forecast()
                elif command == 'stats':
                    self.display_detailed_stats()
                elif command == 'quests':
                    self.display_quests()
                elif command == 'story':
                    self.display_story_progress()
                elif command == 'stronghold' and self.game_state.locations.get("Stronghold", False):
                    self.stronghold_menu()
                elif command.startswith('mods'):
                    parts = command.split()
                    if len(parts) == 1:
                        # Just '/mods' - show info
                        self.display_mods_info()
                    elif len(parts) > 1:
                        subcommand = parts[1].lower()
                        if subcommand == 'enable':
                            self.enable_mods()
                        elif subcommand == 'disable':
                            self.disable_mods()
                        elif subcommand == 'info':
                            self.display_mods_info()
                        else:
                            print(f"{Fore.RED}Unknown mods subcommand. Use 'enable', 'disable', or 'info'.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Unknown command. Type /help for a list of commands.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Commands start with '/'. Type /help for a list of commands.{Style.RESET_ALL}")
    
    def display_quests(self) -> None:
        """Display active quests and quest log"""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== QUEST LOG ====={Style.RESET_ALL}")
        
        # Display active quests
        if gs.active_quests:
            print(f"\n{Fore.GREEN}Active Quests: {len(gs.active_quests)}{Style.RESET_ALL}")
            
            for quest_id, quest in gs.active_quests.items():
                print(f"\n{Fore.YELLOW}{quest['title']} [{quest['progress']}%]{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{quest['description']}{Style.RESET_ALL}")
                
                print(f"\n{Fore.CYAN}Objectives:{Style.RESET_ALL}")
                for obj_id, status in quest['objectives'].items():
                    # Format the objective ID to be more readable
                    readable_obj = obj_id.replace('_', ' ').capitalize()
                    
                    if isinstance(status, bool):
                        if status:
                            print(f"{Fore.GREEN}✓ {readable_obj}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}✗ {readable_obj}{Style.RESET_ALL}")
                    elif isinstance(status, (int, float)):
                        print(f"{Fore.YELLOW}{readable_obj}: {status*100:.0f}%{Style.RESET_ALL}")
                        
                # Show rewards if any
                if quest['rewards']:
                    print(f"\n{Fore.MAGENTA}Rewards:{Style.RESET_ALL}")
                    for reward_type, reward_value in quest['rewards'].items():
                        if reward_type == "items":
                            items_list = [f"{amount} {item}" for item, amount in reward_value.items()]
                            print(f"{Fore.WHITE}• Items: {', '.join(items_list)}{Style.RESET_ALL}")
                        elif reward_type == "story_flag":
                            print(f"{Fore.WHITE}• Story Progress{Style.RESET_ALL}")
                        elif reward_type == "story_path":
                            print(f"{Fore.WHITE}• Path: {reward_value.capitalize()}{Style.RESET_ALL}")
                        elif reward_type == "location":
                            print(f"{Fore.WHITE}• Discover: {reward_value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}You don't have any active quests.{Style.RESET_ALL}")
        
        # Display completed quests
        if gs.completed_quests:
            print(f"\n{Fore.GREEN}Completed Quests: {len(gs.completed_quests)}{Style.RESET_ALL}")
            
            for quest_id, quest in gs.completed_quests.items():
                print(f"{Fore.GREEN}✓ {quest['title']} (Day {quest['date_completed']}){Style.RESET_ALL}")
        
        # Display failed quests
        if gs.failed_quests:
            print(f"\n{Fore.RED}Failed Quests: {len(gs.failed_quests)}{Style.RESET_ALL}")
            
            for quest_id, quest in gs.failed_quests.items():
                print(f"{Fore.RED}✗ {quest['title']} - {quest['failure_reason']} (Day {quest['date_failed']}){Style.RESET_ALL}")
        
        # Display recent quest log entries
        if gs.quest_log:
            print(f"\n{Fore.CYAN}Recent Quest Activity:{Style.RESET_ALL}")
            
            # Show the last 5 log entries
            recent_log = gs.quest_log[-5:] if len(gs.quest_log) > 5 else gs.quest_log
            for entry in recent_log:
                print(f"{Fore.WHITE}• {entry}{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_story_progress(self) -> None:
        """Display story progress and current path"""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== STORY PROGRESS ====={Style.RESET_ALL}")
        
        # Show current story path
        story_path_descriptions = {
            "survivor": "You are focused on survival and escape, using practical approaches to overcome the island's challenges.",
            "explorer": "You are drawn to the island's mysteries, uncovering its ancient secrets and forgotten history.",
            "conqueror": "You seek to master and control the island, building a new life and possibly ruling over those you encounter."
        }
        
        print(f"\n{Fore.YELLOW}Current Path: {gs.story_path.capitalize()}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{story_path_descriptions.get(gs.story_path, 'You are still finding your way.')}{Style.RESET_ALL}")
        
        # Show story milestones based on story flags
        print(f"\n{Fore.CYAN}Story Milestones:{Style.RESET_ALL}")
        
        story_milestones = []
        
        # Add milestones based on story flags
        if "started_main_quest" in gs.story_flags:
            story_milestones.append("You've begun to suspect there's more to this island than meets the eye.")
            
        if "ruins_discovered" in gs.story_flags:
            story_milestones.append("You've discovered ancient ruins that hint at a previous civilization on the island.")
            
        if "pirate_threat" in gs.story_flags:
            story_milestones.append("Pirates are active on the island and pose a threat to your survival.")
            
        if "pirates_defeated" in gs.story_flags:
            story_milestones.append("You've dealt with the pirate threat and secured their treasure.")
            
        if "temple_discovery" in gs.story_flags:
            story_milestones.append("You've learned of a hidden temple somewhere on the island.")
            
        if "temple_secrets" in gs.story_flags:
            story_milestones.append("You've uncovered the secrets of the ancient temple.")
            
        if "island_mystery_resolved" in gs.story_flags:
            story_milestones.append("You've learned that an advanced civilization once inhabited this island.")
            
        if "ancient_tech_mastered" in gs.story_flags:
            story_milestones.append("You've mastered ancient technology that gives you control over aspects of the island.")
            
        if "pirate_king" in gs.story_flags:
            story_milestones.append("You've established yourself as the leader of the island, even commanding respect from pirates.")
            
        if "ready_for_escape" in gs.story_flags:
            story_milestones.append("You're prepared to escape the island and return to civilization.")
            
        # Display milestones or a message if none yet
        if story_milestones:
            for milestone in story_milestones:
                print(f"{Fore.WHITE}• {milestone}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}You're just beginning your journey on the island.{Style.RESET_ALL}")
            
        # Show potential story paths/endings based on current progress
        print(f"\n{Fore.CYAN}Possible Endings:{Style.RESET_ALL}")
        possible_endings = []
        
        # Always show the basic rescue ending
        possible_endings.append("Rescue: Build a signal fire or reliable raft to escape the island.")
        
        # Show special endings based on story progress
        if "temple_discovery" in gs.story_flags or "ruins_discovered" in gs.story_flags:
            possible_endings.append("Island Secret: Uncover the full mystery of the island's ancient civilization.")
            
        if "pirate_threat" in gs.story_flags:
            possible_endings.append("Island Ruler: Defeat the pirates and establish your dominance over the island.")
            
        if "temple_secrets" in gs.story_flags:
            possible_endings.append("Ancient Power: Master the lost technology of the ancients.")
            
        for ending in possible_endings:
            print(f"{Fore.WHITE}• {ending}{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def stronghold_menu(self) -> None:
        """Display options for managing the stronghold and followers"""
        gs = self.game_state
        
        # Initialize followers attribute if it doesn't exist
        if not hasattr(gs, 'stronghold_followers'):
            gs.stronghold_followers = 0
            
        # Generate a list of available recruits if it doesn't exist
        if not hasattr(gs, 'available_recruits'):
            gs.available_recruits = []
            
            # Generate 1-3 random recruits that can be found
            num_recruits = random.randint(1, 3)
            recruit_types = ["Survivor", "Native Islander", "Ex-Pirate", "Castaway"]
            recruit_skills = ["Gathering", "Building", "Hunting", "Fishing", "Crafting", "Defense"]
            
            for _ in range(num_recruits):
                recruit_type = random.choice(recruit_types)
                skill = random.choice(recruit_skills)
                gs.available_recruits.append({
                    "type": recruit_type,
                    "skill": skill,
                    "cost": {
                        "Food": random.randint(3, 5),
                        "Water": random.randint(2, 4)
                    }
                })
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}===== STRONGHOLD MANAGEMENT ====={Style.RESET_ALL}")
            
            # Display stronghold status
            print(f"\n{Fore.WHITE}Your stronghold status:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Location: {Fore.CYAN}Stronghold{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Current followers: {Fore.GREEN}{gs.stronghold_followers}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Daily resource production:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}• Wood: {3 + gs.stronghold_followers * 1}-{8 + gs.stronghold_followers * 2}")
            print(f"{Fore.WHITE}• Stone: {2 + gs.stronghold_followers * 0}-{5 + gs.stronghold_followers * 1}")
            print(f"{Fore.WHITE}• Metal: {1 + int(gs.stronghold_followers * 0.5)}")
            
            # Show options
            print(f"\n{Fore.WHITE}Options:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}1. {Fore.WHITE}Recruit new followers")
            print(f"{Fore.YELLOW}2. {Fore.WHITE}Assign tasks to followers")
            print(f"{Fore.YELLOW}3. {Fore.WHITE}Construct upgrades")
            print(f"{Fore.YELLOW}0. {Fore.WHITE}Back to main menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == "1":
                self.recruit_followers()
            elif choice == "2":
                self.assign_follower_tasks()
            elif choice == "3":
                self.construct_stronghold_upgrades()
            elif choice == "0":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def recruit_followers(self) -> None:
        """Recruit new followers for the stronghold"""
        gs = self.game_state
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}===== RECRUIT FOLLOWERS ====={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Potential recruits who could join your stronghold:{Style.RESET_ALL}")
        
        # Display available recruits
        if gs.available_recruits:
            for i, recruit in enumerate(gs.available_recruits, 1):
                print(f"\n{Fore.YELLOW}{i}. {recruit['type']} - Skilled in {recruit['skill']}{Style.RESET_ALL}")
                cost_str = ", ".join([f"{amount} {item}" for item, amount in recruit["cost"].items()])
                print(f"{Fore.WHITE}   Cost: {cost_str}{Style.RESET_ALL}")
                
            print(f"\n{Fore.YELLOW}0. {Fore.WHITE}Back to stronghold menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (or search for more recruits): {Style.RESET_ALL}")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(gs.available_recruits):
                    # Try to recruit the selected follower
                    recruit = gs.available_recruits[choice_num - 1]
                    
                    # Check if player has required resources
                    can_recruit = True
                    for item, amount in recruit["cost"].items():
                        if gs.inventory.get(item, 0) < amount:
                            can_recruit = False
                            print(f"{Fore.RED}You don't have enough {item} to recruit this follower.{Style.RESET_ALL}")
                            break
                    
                    if can_recruit:
                        # Consume resources
                        for item, amount in recruit["cost"].items():
                            gs.inventory[item] -= amount
                        
                        # Add follower
                        gs.stronghold_followers += 1
                        print(f"\n{Fore.GREEN}The {recruit['type']} has joined your stronghold!{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}Your stronghold now has {gs.stronghold_followers} followers.{Style.RESET_ALL}")
                        
                        # Remove from available recruits
                        gs.available_recruits.pop(choice_num - 1)
                        
                        # Update quest objective if active
                        if "island_ruler" in gs.active_quests:
                            # Make sure the quest has the expected structure
                            if "objectives" in gs.active_quests["island_ruler"] and "collect_resources" in gs.active_quests["island_ruler"]["objectives"]:
                                # Check if resources are already collected
                                if not gs.active_quests["island_ruler"]["objectives"]["collect_resources"]:
                                    # Mark resources as collected (set to True since the objective is boolean)
                                    gs.update_quest_objective("island_ruler", "collect_resources", True)
                                    print(f"\n{Fore.MAGENTA}Quest updated: Island Ruler - Resources collected!{Style.RESET_ALL}")
                elif choice_num == 0:
                    return
                else:
                    print(f"{Fore.RED}Invalid choice. Please select a number between 0 and {len(gs.available_recruits)}.{Style.RESET_ALL}")
            except ValueError:
                if choice.lower() == "search":
                    # Generate new potential recruits
                    gs.available_recruits = []
                    num_recruits = random.randint(1, 3)
                    recruit_types = ["Survivor", "Native Islander", "Ex-Pirate", "Castaway"]
                    recruit_skills = ["Gathering", "Building", "Hunting", "Fishing", "Crafting", "Defense"]
                    
                    for _ in range(num_recruits):
                        recruit_type = random.choice(recruit_types)
                        skill = random.choice(recruit_skills)
                        gs.available_recruits.append({
                            "type": recruit_type,
                            "skill": skill,
                            "cost": {
                                "Food": random.randint(3, 5),
                                "Water": random.randint(2, 4)
                            }
                        })
                    print(f"{Fore.GREEN}You searched for new potential recruits!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid input. Please enter a number or 'search'.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}There are currently no available recruits. Search for more?{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}1. {Fore.WHITE}Search for recruits")
            print(f"{Fore.YELLOW}0. {Fore.WHITE}Back to stronghold menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == "1":
                # Generate new potential recruits
                gs.available_recruits = []
                num_recruits = random.randint(1, 3)
                recruit_types = ["Survivor", "Native Islander", "Ex-Pirate", "Castaway"]
                recruit_skills = ["Gathering", "Building", "Hunting", "Fishing", "Crafting", "Defense"]
                
                for _ in range(num_recruits):
                    recruit_type = random.choice(recruit_types)
                    skill = random.choice(recruit_skills)
                    gs.available_recruits.append({
                        "type": recruit_type,
                        "skill": skill,
                        "cost": {
                            "Food": random.randint(3, 5),
                            "Water": random.randint(2, 4)
                        }
                    })
                print(f"{Fore.GREEN}You searched for new potential recruits!{Style.RESET_ALL}")
            elif choice != "0":
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def assign_follower_tasks(self) -> None:
        """Assign tasks to stronghold followers"""
        gs = self.game_state
        
        if gs.stronghold_followers <= 0:
            print(f"\n{Fore.YELLOW}You don't have any followers to assign tasks to.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Initialize task assignments if they don't exist
        if not hasattr(gs, 'follower_tasks'):
            gs.follower_tasks = {
                "Gathering": 0,
                "Hunting": 0,
                "Defense": 0,
                "Building": 0
            }
            
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}===== ASSIGN TASKS ====={Style.RESET_ALL}")
        print(f"{Fore.WHITE}You have {gs.stronghold_followers} followers to assign to tasks.{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Current assignments:{Style.RESET_ALL}")
        
        for task, count in gs.follower_tasks.items():
            print(f"{Fore.YELLOW}{task}: {Fore.WHITE}{count} followers")
            
        print(f"\n{Fore.WHITE}Available tasks:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. {Fore.WHITE}Gathering - Increases resource collection")
        print(f"{Fore.YELLOW}2. {Fore.WHITE}Hunting - Collects food automatically")
        print(f"{Fore.YELLOW}3. {Fore.WHITE}Defense - Reduces chance of attacks")
        print(f"{Fore.YELLOW}4. {Fore.WHITE}Building - Helps with construction projects")
        print(f"{Fore.YELLOW}0. {Fore.WHITE}Back to stronghold menu")
        
        choice = input(f"\n{Fore.GREEN}Choose a task to assign followers to: {Style.RESET_ALL}")
        
        if choice == "1":
            task = "Gathering"
        elif choice == "2":
            task = "Hunting"
        elif choice == "3":
            task = "Defense"
        elif choice == "4":
            task = "Building"
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Get number of followers to assign
        assigned_followers = sum(gs.follower_tasks.values())
        available_followers = gs.stronghold_followers - assigned_followers
        
        print(f"\n{Fore.WHITE}You have {available_followers} unassigned followers.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current {task} assignment: {gs.follower_tasks[task]} followers{Style.RESET_ALL}")
        
        try:
            count = int(input(f"\n{Fore.GREEN}How many followers to assign to {task} (0-{gs.stronghold_followers}): {Style.RESET_ALL}"))
            
            if 0 <= count <= gs.stronghold_followers:
                # Calculate how many need to be unassigned from other tasks
                current_total = sum(gs.follower_tasks.values())
                new_total = current_total - gs.follower_tasks[task] + count
                
                if new_total > gs.stronghold_followers:
                    over_assigned = new_total - gs.stronghold_followers
                    print(f"{Fore.YELLOW}Warning: You need to unassign {over_assigned} followers from other tasks first.{Style.RESET_ALL}")
                else:
                    gs.follower_tasks[task] = count
                    print(f"\n{Fore.GREEN}Successfully assigned {count} followers to {task}.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid number. Please enter a number between 0 and {gs.stronghold_followers}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def construct_stronghold_upgrades(self) -> None:
        """Build upgrades for the stronghold"""
        gs = self.game_state
        
        # Initialize upgrades if they don't exist
        if not hasattr(gs, 'stronghold_upgrades'):
            gs.stronghold_upgrades = {
                "walls": False,
                "watchtower": False,
                "farm": False,
                "workshop": False
            }
            
        # Define upgrade costs
        upgrade_costs = {
            "walls": {"Wood": 15, "Stone": 25},
            "watchtower": {"Wood": 20, "Stone": 10},
            "farm": {"Wood": 10, "Seed": 5, "Water": 10},
            "workshop": {"Wood": 15, "Metal": 5, "Tool": 2}
        }
        
        # Define upgrade benefits
        upgrade_benefits = {
            "walls": "Improved defense against attacks and bad weather",
            "watchtower": "Early warning of dangers and better chance to spot passing ships",
            "farm": "Steady food supply that doesn't deplete",
            "workshop": "More efficient crafting and resource processing"
        }
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}===== STRONGHOLD UPGRADES ====={Style.RESET_ALL}")
        
        # Show current upgrades
        print(f"\n{Fore.WHITE}Current upgrades:{Style.RESET_ALL}")
        for upgrade, built in gs.stronghold_upgrades.items():
            status = f"{Fore.GREEN}Built" if built else f"{Fore.RED}Not Built"
            print(f"{Fore.YELLOW}{upgrade.capitalize()}: {status}{Style.RESET_ALL}")
            
        # Show available upgrades
        print(f"\n{Fore.WHITE}Available upgrades:{Style.RESET_ALL}")
        
        available_upgrades = [upgrade for upgrade, built in gs.stronghold_upgrades.items() if not built]
        
        if available_upgrades:
            for i, upgrade in enumerate(available_upgrades, 1):
                print(f"\n{Fore.YELLOW}{i}. {upgrade.capitalize()}{Style.RESET_ALL}")
                print(f"{Fore.WHITE}   Benefit: {upgrade_benefits[upgrade]}")
                
                cost_str = ", ".join([f"{amount} {item}" for item, amount in upgrade_costs[upgrade].items()])
                print(f"{Fore.WHITE}   Cost: {cost_str}{Style.RESET_ALL}")
                
            print(f"\n{Fore.YELLOW}0. {Fore.WHITE}Back to stronghold menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_upgrades):
                    # Try to build the selected upgrade
                    upgrade = available_upgrades[choice_num - 1]
                    cost = upgrade_costs[upgrade]
                    
                    # Check if player has required resources
                    can_build = True
                    for item, amount in cost.items():
                        if gs.inventory.get(item, 0) < amount:
                            can_build = False
                            print(f"{Fore.RED}You don't have enough {item} to build this upgrade.{Style.RESET_ALL}")
                            break
                    
                    if can_build:
                        # Consume resources
                        for item, amount in cost.items():
                            gs.inventory[item] -= amount
                        
                        # Build upgrade
                        gs.stronghold_upgrades[upgrade] = True
                        print(f"\n{Fore.GREEN}You've built the {upgrade.capitalize()}!{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}Benefit: {upgrade_benefits[upgrade]}{Style.RESET_ALL}")
                        
                        # Apply special effects based on the upgrade
                        if upgrade == "farm":
                            if not hasattr(gs, 'daily_food_production'):
                                gs.daily_food_production = 3
                            else:
                                gs.daily_food_production += 3
                            print(f"{Fore.GREEN}Your stronghold will now produce 3 Food daily.{Style.RESET_ALL}")
                            
                        elif upgrade == "workshop":
                            # Could reduce crafting costs by 25%
                            if not hasattr(gs, 'crafting_efficiency'):
                                gs.crafting_efficiency = 0.25
                            else:
                                gs.crafting_efficiency += 0.25
                            print(f"{Fore.GREEN}Crafting at your stronghold is now 25% more efficient.{Style.RESET_ALL}")
                        
                        # Update quest objective if active
                        if "island_ruler" in gs.active_quests:
                            # Check if all upgrades are built for quest completion
                            if all(gs.stronghold_upgrades.values()):
                                gs.update_quest_objective("island_ruler", "defeat_challengers", True)
                                print(f"\n{Fore.MAGENTA}Quest updated: Island Ruler - You've established complete control!{Style.RESET_ALL}")
                elif choice_num != 0:
                    print(f"{Fore.RED}Invalid choice. Please select a number between 0 and {len(available_upgrades)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}You've built all available upgrades for your stronghold!{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
        
    def enable_mods(self) -> None:
        """Enable mods in the game"""
        gs = self.game_state
        
        if gs.mods_enabled:
            print(f"\n{Fore.YELLOW}Mods are already enabled.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Count available mods
        mod_dirs = [d for d in glob.glob("mods/*/") if os.path.isdir(d) and os.path.exists(os.path.join(d, "mod_info.json"))]
        mod_count = len(mod_dirs)
        
        if mod_count == 0:
            print(f"\n{Fore.YELLOW}No mods found in the mods directory.{Style.RESET_ALL}")
            print(f"{Fore.WHITE}To add mods to the game:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. Create a directory in the 'mods' folder with your mod name.")
            print(f"{Fore.WHITE}2. Add a 'mod_info.json' file with metadata about your mod.")
            print(f"{Fore.WHITE}3. Add content files (locations.json, items.json, recipes.json, etc.)")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}===== ENABLE MODS ====={Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Found {mod_count} mod(s) available.{Style.RESET_ALL}")
        print(f"{Fore.RED}Warning: Enabling mods may change game mechanics and balance.{Style.RESET_ALL}")
        print(f"{Fore.RED}You will need to restart the game for mods to take full effect.{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.GREEN}Do you want to enable mods? (y/n): {Style.RESET_ALL}").lower()
        
        if confirm == 'y' or confirm == 'yes':
            gs.mods_enabled = True
            print(f"\n{Fore.GREEN}Mods enabled! Integrating mods now...{Style.RESET_ALL}")
            
            # Clear existing loaded mods list
            gs.loaded_mods = []
            
            # Integrate mods immediately
            gs.integrate_mods()
            
            # Let player know that a restart may be needed for all features
            print(f"\n{Fore.YELLOW}Some mod features may require a new game to fully integrate.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}Mods remain disabled.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def disable_mods(self) -> None:
        """Disable mods in the game"""
        gs = self.game_state
        
        if not gs.mods_enabled:
            print(f"\n{Fore.YELLOW}Mods are already disabled.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}===== DISABLE MODS ====={Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}You currently have {len(gs.loaded_mods)} mod(s) loaded.{Style.RESET_ALL}")
        print(f"{Fore.RED}Warning: Disabling mods may affect your current game.{Style.RESET_ALL}")
        print(f"{Fore.RED}You will need to restart the game for changes to take full effect.{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.GREEN}Do you want to disable mods? (y/n): {Style.RESET_ALL}").lower()
        
        if confirm == 'y' or confirm == 'yes':
            gs.mods_enabled = False
            print(f"\n{Fore.YELLOW}Mods disabled. Changes will take effect on restart.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}Mods remain enabled.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_mods_info(self) -> None:
        """Display information about loaded mods"""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== MODS INFORMATION ====={Style.RESET_ALL}")
        
        # Count available mods
        mod_dirs = [d for d in glob.glob("mods/*/") if os.path.isdir(d) and os.path.exists(os.path.join(d, "mod_info.json"))]
        mod_count = len(mod_dirs)
        
        # Display mods status
        status_color = Fore.GREEN if gs.mods_enabled else Fore.RED
        status_text = "Enabled" if gs.mods_enabled else "Disabled"
        print(f"{Fore.WHITE}Mods Status: {status_color}{status_text}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Available Mods: {Fore.YELLOW}{mod_count}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Loaded Mods: {Fore.YELLOW}{len(gs.loaded_mods)}{Style.RESET_ALL}")
        
        # Command reminder
        print(f"\n{Fore.CYAN}Commands:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}/mods enable - Enable all mods")
        print(f"{Fore.WHITE}/mods disable - Disable all mods")
        print(f"{Fore.WHITE}/mods info - Show mod information{Style.RESET_ALL}")
        
        if not gs.loaded_mods:
            if not gs.mods_enabled and mod_count > 0:
                print(f"\n{Fore.YELLOW}Mods are available but currently disabled.{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Use {Fore.GREEN}/mods enable{Fore.WHITE} to enable mods.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}No mods are currently loaded.{Style.RESET_ALL}")
                print(f"\n{Fore.WHITE}To add mods to the game:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}1. Create a directory in the 'mods' folder with your mod name.")
                print(f"{Fore.WHITE}2. Add a 'mod_info.json' file with metadata about your mod.")
                print(f"{Fore.WHITE}3. Add content files (locations.json, items.json, recipes.json, etc.)")
        else:
            print(f"\n{Fore.GREEN}Loaded mods: {len(gs.loaded_mods)}{Style.RESET_ALL}")
            
            for mod_name in gs.loaded_mods:
                mod_info_path = os.path.join("mods", mod_name, "mod_info.json")
                
                if os.path.exists(mod_info_path):
                    try:
                        with open(mod_info_path, 'r') as f:
                            mod_info = json.load(f)
                            
                        print(f"\n{Fore.YELLOW}{mod_info.get('name', mod_name)}{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}Description: {mod_info.get('description', 'No description provided')}")
                        print(f"{Fore.WHITE}Author: {mod_info.get('author', 'Unknown')}")
                        print(f"{Fore.WHITE}Version: {mod_info.get('version', '1.0.0')}")
                        
                        # Check what content files are included
                        content_types = []
                        if os.path.exists(os.path.join("mods", mod_name, "locations.json")):
                            content_types.append("Locations")
                        if os.path.exists(os.path.join("mods", mod_name, "items.json")):
                            content_types.append("Items")
                        if os.path.exists(os.path.join("mods", mod_name, "recipes.json")):
                            content_types.append("Recipes")
                        if os.path.exists(os.path.join("mods", mod_name, "enemies.json")):
                            content_types.append("Enemies")
                        if os.path.exists(os.path.join("mods", mod_name, "events.json")):
                            content_types.append("Events")
                            
                        print(f"{Fore.WHITE}Content: {', '.join(content_types) if content_types else 'None'}")
                    except Exception as e:
                        print(f"{Fore.RED}Error loading mod info for {mod_name}: {str(e)}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.YELLOW}{mod_name}{Style.RESET_ALL}")
                    print(f"{Fore.RED}No mod_info.json found!{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}===== MOD CREATION GUIDE ====={Style.RESET_ALL}")
        print(f"{Fore.WHITE}See the README.md file in the 'mods' directory for detailed instructions")
        print(f"{Fore.WHITE}on creating your own mods for Shipwrecked.{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
        
    def display_help(self) -> None:
        """Display a help screen with all available commands."""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== AVAILABLE COMMANDS ====={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}/explore {Fore.WHITE}- Search your location for resources and battle enemies")
        print(f"{Fore.YELLOW}/inventory {Fore.WHITE}- View what items you currently have (aliases: /inv, /i)")
        print(f"{Fore.YELLOW}/craft {Fore.WHITE}- Create tools, shelter, and other items from resources")
        print(f"{Fore.YELLOW}/eat {Fore.WHITE}- Consume food and water to restore hunger and thirst")
        print(f"{Fore.YELLOW}/rest {Fore.WHITE}- Recover energy by resting")
        print(f"{Fore.YELLOW}/travel {Fore.WHITE}- Move to a different location on the island")
        print(f"{Fore.YELLOW}/map {Fore.WHITE}- View the island map (requires crafting a Map item)")
        print(f"{Fore.YELLOW}/fish {Fore.WHITE}- Go fishing for food (requires Fishing Rod)")
        print(f"{Fore.YELLOW}/hunt {Fore.WHITE}- Hunt for food and hide from animals (requires Spear)")
        print(f"{Fore.YELLOW}/signal {Fore.WHITE}- Try to signal for rescue (requires Signal Mirror)")
        print(f"{Fore.YELLOW}/raft {Fore.WHITE}- Build or check your escape raft")
        print(f"{Fore.YELLOW}/weather {Fore.WHITE}- Check detailed weather forecast and predictions")
        print(f"{Fore.YELLOW}/stats {Fore.WHITE}- View detailed player statistics and achievements")
        print(f"{Fore.YELLOW}/quests {Fore.WHITE}- View your active quests and quest log")
        print(f"{Fore.YELLOW}/story {Fore.WHITE}- View your story progress and current path")
        
        # Only show stronghold command if player has a stronghold
        if gs.locations.get("Stronghold", False):
            print(f"{Fore.YELLOW}/stronghold {Fore.WHITE}- Manage your stronghold, followers, and upgrades")
            
        print(f"{Fore.YELLOW}/mods {Fore.WHITE}- View information about installed mods")
        print(f"{Fore.YELLOW}/save {Fore.WHITE}- Save your current game progress")
        print(f"{Fore.YELLOW}/load {Fore.WHITE}- Load a previously saved game")
        print(f"{Fore.YELLOW}/quit {Fore.WHITE}- Exit the game (aliases: /exit, /q)")
        print(f"{Fore.YELLOW}/help {Fore.WHITE}- Show this list of commands")
        
        print(f"\n{Fore.CYAN}===== GAME TIPS ====={Style.RESET_ALL}")
        print(f"{Fore.WHITE}- Craft a {Fore.YELLOW}spear{Fore.WHITE} to defend yourself against enemies")
        print(f"{Fore.WHITE}- Build a {Fore.YELLOW}shelter{Fore.WHITE} for better protection at night")
        print(f"{Fore.WHITE}- Craft a {Fore.YELLOW}map{Fore.WHITE} to see the island layout and plan your exploration")
        print(f"{Fore.WHITE}- Keep an eye on your {Fore.YELLOW}hunger{Fore.WHITE} and {Fore.YELLOW}thirst{Fore.WHITE} levels")
        print(f"{Fore.WHITE}- Undiscovered locations show as {Fore.RED}??????{Fore.WHITE} until you find them")
        
        # Additional tips for players with a stronghold
        if gs.locations.get("Stronghold", False):
            print(f"\n{Fore.CYAN}===== STRONGHOLD TIPS ====={Style.RESET_ALL}")
            print(f"{Fore.WHITE}- Recruit {Fore.YELLOW}followers{Fore.WHITE} to help gather resources and defend your stronghold")
            print(f"{Fore.WHITE}- Assign followers to {Fore.YELLOW}tasks{Fore.WHITE} like gathering, hunting, and defense")
            print(f"{Fore.WHITE}- Build {Fore.YELLOW}upgrades{Fore.WHITE} like walls, a farm, and a workshop")
            print(f"{Fore.WHITE}- The {Fore.YELLOW}farm upgrade{Fore.WHITE} provides a daily supply of food")
            print(f"{Fore.WHITE}- Progress on the {Fore.YELLOW}conqueror path{Fore.WHITE} by building a powerful stronghold")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def explore_location(self) -> None:
        gs = self.game_state
        location = gs.current_location
        
        print(f"\n{Fore.CYAN}Exploring {location}...{Style.RESET_ALL}")
        
        # Weather effects on exploration
        weather_effect = ""
        weather_resource_modifier = 1.0  # Default multiplier for resource gathering
        enemy_chance_modifier = 1.0      # Default multiplier for enemy encounters
        
        if gs.weather == "Rainy":
            weather_effect = f"\n{Fore.BLUE}The rain makes exploration more difficult and reduces visibility.{Style.RESET_ALL}"
            weather_resource_modifier = 0.8   # 20% fewer resources in rain
            enemy_chance_modifier = 0.7       # 30% fewer enemies in rain
        elif gs.weather == "Foggy":
            weather_effect = f"\n{Fore.WHITE}The fog severely limits visibility, making it harder to find things.{Style.RESET_ALL}"
            weather_resource_modifier = 0.6   # 40% fewer resources in fog
            enemy_chance_modifier = 0.5       # 50% fewer enemies in fog (they can't see you either)
        elif gs.weather == "Stormy":
            weather_effect = f"\n{Fore.RED}The storm makes exploration dangerous! You should seek shelter.{Style.RESET_ALL}"
            weather_resource_modifier = 0.5   # 50% fewer resources in storm
            enemy_chance_modifier = 0.3       # 70% fewer enemies in storm (they're taking shelter)
        elif gs.weather == "Hot":
            weather_effect = f"\n{Fore.YELLOW}The hot weather is draining, but good visibility helps you spot things.{Style.RESET_ALL}"
            weather_resource_modifier = 1.2   # 20% more resources in hot weather
            enemy_chance_modifier = 1.2       # 20% more enemies in hot weather (they're active)
        elif gs.weather == "Clear":
            weather_effect = f"\n{Fore.GREEN}The clear weather makes exploration easier and more productive.{Style.RESET_ALL}"
            weather_resource_modifier = 1.3   # 30% more resources in clear weather
            enemy_chance_modifier = 1.0       # Normal enemy chance in clear weather
        
        if weather_effect:
            print(weather_effect)
        
        time.sleep(1)
        
        # Check for enemy encounters with modified chance
        if random.random() < (0.3 * enemy_chance_modifier):  # Base 30% modified by weather
            self.encounter_enemy()
        
        # Energy cost for exploration, modified by weather
        base_energy_cost = random.randint(5, 10)
        if gs.weather == "Hot":
            base_energy_cost += 3      # Hot weather is more tiring
        elif gs.weather == "Stormy":
            base_energy_cost += 5      # Storms are very tiring
        elif gs.weather == "Clear":
            base_energy_cost -= 2      # Clear weather is less tiring
        
        energy_cost = max(3, base_energy_cost)  # Minimum 3 energy cost
        gs.energy -= energy_cost
        
        # Add location to explored locations list if not already there
        if location not in gs.explored_locations:
            gs.explored_locations.append(location)
        
        # Different exploration outcomes based on location
        found_items = {}
        
        if location == "Beach":
            items = {
                "Wood": (1, 3),
                "Stone": (0, 2),
                "Coconut": (0, 2),
                "Vine": (0, 1)
            }
            
            # Special chance to find the shipwreck
            if not gs.locations["Shipwreck"] and random.random() < 0.2:
                gs.locations["Shipwreck"] = True
                # Make sure there's a connection to Shipwreck in the island map
                if "Shipwreck" not in gs.island_map:
                    gs.island_map["Shipwreck"] = ["Beach"]
                if "Beach" not in gs.island_map["Shipwreck"]:
                    gs.island_map["Shipwreck"].append("Beach")
                if "Shipwreck" not in gs.island_map["Beach"]:
                    gs.island_map["Beach"].append("Shipwreck")
                print(f"{Fore.YELLOW}You spot debris in the distance. You've discovered the {Fore.CYAN}Shipwreck{Fore.YELLOW}!{Style.RESET_ALL}")
            
        elif location == "Forest":
            items = {
                "Wood": (2, 4),
                "Stone": (0, 1),
                "Fruit": (0, 2),
                "Berry": (0, 3),
                "Vine": (1, 3),
                "Leaf": (2, 5)
            }
            
            # Chance to find mountain or waterfall
            if not gs.locations["Mountain"] and random.random() < 0.15:
                gs.locations["Mountain"] = True
                # Connect Mountain to Forest in the island map
                if "Mountain" not in gs.island_map:
                    gs.island_map["Mountain"] = ["Forest"]
                if "Forest" not in gs.island_map["Mountain"]:
                    gs.island_map["Mountain"].append("Forest")
                if "Mountain" not in gs.island_map["Forest"]:
                    gs.island_map["Forest"].append("Mountain")
                print(f"{Fore.YELLOW}Through the trees, you spot a {Fore.CYAN}Mountain{Fore.YELLOW} in the distance!{Style.RESET_ALL}")
            
            if not gs.locations["Waterfall"] and random.random() < 0.15:
                gs.locations["Waterfall"] = True
                # Connect Waterfall to Forest in the island map
                if "Waterfall" not in gs.island_map:
                    gs.island_map["Waterfall"] = ["Forest"]
                if "Forest" not in gs.island_map["Waterfall"]:
                    gs.island_map["Waterfall"].append("Forest")
                if "Waterfall" not in gs.island_map["Forest"]:
                    gs.island_map["Forest"].append("Waterfall")
                print(f"{Fore.YELLOW}You hear rushing water. You've discovered a {Fore.CYAN}Waterfall{Fore.YELLOW}!{Style.RESET_ALL}")
            
        elif location == "Mountain":
            items = {
                "Stone": (2, 4),
                "Wood": (0, 1),
                "Vine": (0, 1)
            }
            
            # Chance to find cave
            if not gs.locations["Cave"] and random.random() < 0.25:
                gs.locations["Cave"] = True
                # Connect Cave to Mountain in the island map
                if "Cave" not in gs.island_map:
                    gs.island_map["Cave"] = ["Mountain"]
                if "Mountain" not in gs.island_map["Cave"]:
                    gs.island_map["Cave"].append("Mountain")
                if "Cave" not in gs.island_map["Mountain"]:
                    gs.island_map["Mountain"].append("Cave")
                print(f"{Fore.YELLOW}You notice a dark opening in the mountainside. You've found a {Fore.CYAN}Cave{Fore.YELLOW}!{Style.RESET_ALL}")
                
        elif location == "Cave":
            items = {
                "Stone": (2, 5),
            }
            
            # Very small chance to find special items
            if random.random() < 0.1:
                print(f"{Fore.YELLOW}You find some supplies that must have been left by previous castaways!{Style.RESET_ALL}")
                special_items = ["Spear", "Water Container", "Torch"]
                special_item = random.choice(special_items)
                gs.inventory[special_item] += 1
                print(f"{Fore.GREEN}You found a {Fore.CYAN}{special_item}{Fore.GREEN}!{Style.RESET_ALL}")
                
        elif location == "Waterfall":
            items = {
                "Fresh Water": (3, 6),
                "Stone": (1, 2),
                "Vine": (0, 2)
            }
            
            # Chance to find abandoned hut
            if not gs.locations["Abandoned Hut"] and random.random() < 0.2:
                gs.locations["Abandoned Hut"] = True
                # Connect Abandoned Hut to Waterfall in the island map
                if "Abandoned Hut" not in gs.island_map:
                    gs.island_map["Abandoned Hut"] = ["Waterfall"]
                if "Waterfall" not in gs.island_map["Abandoned Hut"]:
                    gs.island_map["Abandoned Hut"].append("Waterfall")
                if "Abandoned Hut" not in gs.island_map["Waterfall"]:
                    gs.island_map["Waterfall"].append("Abandoned Hut")
                print(f"{Fore.YELLOW}Beyond the waterfall, you spot an {Fore.CYAN}Abandoned Hut{Fore.YELLOW}!{Style.RESET_ALL}")
                
        elif location == "Abandoned Hut":
            items = {
                "Wood": (1, 2),
                "Leaf": (0, 2)
            }
            
            # Good chance to find special items
            if random.random() < 0.3:
                print(f"{Fore.YELLOW}You search through the old hut and find something useful!{Style.RESET_ALL}")
                special_items = ["Spear", "Fishing Rod", "Water Container", "Torch"]
                special_item = random.choice(special_items)
                gs.inventory[special_item] += 1
                print(f"{Fore.GREEN}You found a {Fore.CYAN}{special_item}{Fore.GREEN}!{Style.RESET_ALL}")
                
        elif location == "Shipwreck":
            items = {
                "Wood": (2, 4),
                "Vine": (0, 1)
            }
            
            # Good chance to find special items
            if random.random() < 0.4:
                print(f"{Fore.YELLOW}You salvage through the ship's remains and find something useful!{Style.RESET_ALL}")
                special_items = ["Spear", "Fishing Rod", "Water Container", "Torch"]
                special_item = random.choice(special_items)
                gs.inventory[special_item] += 1
                print(f"{Fore.GREEN}You found a {Fore.CYAN}{special_item}{Fore.GREEN}!{Style.RESET_ALL}")
                
        elif location == "Shelter":
            items = {}  # No items to find in shelter
            
            # Rest bonus when exploring shelter
            rest_bonus = random.randint(5, 15)
            gs.energy += rest_bonus
            print(f"{Fore.GREEN}You feel comfortable in your shelter. You regain {rest_bonus} energy.{Style.RESET_ALL}")
            
        elif location == "Jungle":
            items = {
                "Wood": (1, 3),
                "Vine": (2, 4),
                "Fruit": (1, 3),
                "Exotic Fruit": (0, 2),
                "Leaf": (2, 4)
            }
            
            # Chance to find hidden areas
            if not gs.locations["Ancient Ruins"] and random.random() < 0.15:
                gs.locations["Ancient Ruins"] = True
                # Connect Ancient Ruins to Jungle in the island map
                if "Ancient Ruins" not in gs.island_map:
                    gs.island_map["Ancient Ruins"] = ["Jungle"]
                if "Jungle" not in gs.island_map["Ancient Ruins"]:
                    gs.island_map["Ancient Ruins"].append("Jungle")
                if "Ancient Ruins" not in gs.island_map["Jungle"]:
                    gs.island_map["Jungle"].append("Ancient Ruins")
                print(f"{Fore.YELLOW}Through the dense foliage, you spot what looks like {Fore.CYAN}Ancient Ruins{Fore.YELLOW}!{Style.RESET_ALL}")
                
        elif location == "Cliff Side":
            items = {
                "Stone": (2, 4),
                "Wood": (0, 1)
            }
            
            # Good view from the cliff might reveal new locations
            if not gs.locations["Island Summit"] and random.random() < 0.25:
                gs.locations["Island Summit"] = True
                # Connect Island Summit to Cliff Side in the island map
                if "Island Summit" not in gs.island_map:
                    gs.island_map["Island Summit"] = ["Cliff Side", "Mountain"]
                if "Cliff Side" not in gs.island_map["Island Summit"]:
                    gs.island_map["Island Summit"].append("Cliff Side")
                if "Island Summit" not in gs.island_map["Cliff Side"]:
                    gs.island_map["Cliff Side"].append("Island Summit")
                print(f"{Fore.YELLOW}From this vantage point, you can see the {Fore.CYAN}Island Summit{Fore.YELLOW}!{Style.RESET_ALL}")
                
        elif location == "Ancient Ruins":
            items = {
                "Stone": (2, 3),
                "Metal": (0, 2)
            }
            
            # Chance to find special items
            if random.random() < 0.3:
                print(f"{Fore.YELLOW}Searching through the ruins, you discover something remarkable!{Style.RESET_ALL}")
                gs.inventory["Ancient Artifact"] += 1
                print(f"{Fore.GREEN}You found an {Fore.CYAN}Ancient Artifact{Fore.GREEN}!{Style.RESET_ALL}")
                
                # Update quest objective if active
                if "island_mystery" in gs.active_quests:
                    gs.update_quest_objective("island_mystery", "discover_ruins", True)
                    gs.update_quest_objective("island_mystery", "find_artifact", True)
                    print(f"{Fore.MAGENTA}Quest updated: The Island's Secret{Style.RESET_ALL}")
                    
            # Chance to find temple clues for temple quest
            if "temple_mystery" in gs.active_quests and random.random() < 0.25:
                print(f"{Fore.YELLOW}You notice strange markings on a stone tablet that seem to indicate a temple location!{Style.RESET_ALL}")
                gs.update_quest_objective("temple_mystery", "find_temple_clues", True)
                print(f"{Fore.MAGENTA}Quest updated: Temple of the Ancients{Style.RESET_ALL}")
                
        elif location == "Swamp":
            items = {
                "Wood": (1, 2),
                "Vine": (1, 3),
                "Clay": (1, 3),
                "Mushroom": (0, 2)
            }
            
            # Chance to find quicksand pit
            if not gs.locations["Quicksand Pit"] and random.random() < 0.2:
                gs.locations["Quicksand Pit"] = True
                # Connect Quicksand Pit to Swamp in the island map
                if "Quicksand Pit" not in gs.island_map:
                    gs.island_map["Quicksand Pit"] = ["Swamp"]
                if "Swamp" not in gs.island_map["Quicksand Pit"]:
                    gs.island_map["Quicksand Pit"].append("Swamp")
                if "Quicksand Pit" not in gs.island_map["Swamp"]:
                    gs.island_map["Swamp"].append("Quicksand Pit")
                print(f"{Fore.YELLOW}You almost fall into a {Fore.CYAN}Quicksand Pit{Fore.YELLOW}! At least now you know where it is.{Style.RESET_ALL}")
                
        elif location == "Coral Reef":
            items = {
                "Fish": (1, 3),
                "Seaweed": (1, 3)
            }
            
            # Special chance for fishing in coral reef
            if gs.inventory["Fishing Rod"] > 0:
                fish_bonus = random.randint(1, 2)
                gs.inventory["Fish"] += fish_bonus
                print(f"{Fore.GREEN}The reef is teeming with fish! You catch {fish_bonus} extra fish!{Style.RESET_ALL}")
                
        elif location == "Volcanic Area":
            items = {
                "Stone": (2, 4),
                "Obsidian": (1, 2)
            }
            
            # Hot environment causes more thirst
            thirst_loss = random.randint(5, 10)
            gs.thirst = max(0, gs.thirst - thirst_loss)
            print(f"{Fore.RED}The volcanic heat makes you thirsty. You lose {thirst_loss} thirst points.{Style.RESET_ALL}")
            
        elif location == "Hidden Valley":
            items = {
                "Wood": (1, 3),
                "Fruit": (2, 4),
                "Exotic Fruit": (1, 3),
                "Berry": (2, 4)
            }
            
            # Abundant food in hidden valley
            print(f"{Fore.GREEN}This secluded valley is rich with food sources!{Style.RESET_ALL}")
            
        elif location == "Lagoon":
            items = {
                "Fresh Water": (2, 4),
                "Fish": (1, 2),
                "Sand": (1, 3)
            }
            
            # Peaceful area helps recover energy
            energy_gain = random.randint(5, 10)
            gs.energy = min(100, gs.energy + energy_gain)
            print(f"{Fore.GREEN}The calm waters of the lagoon are soothing. You gain {energy_gain} energy.{Style.RESET_ALL}")
            
        elif location == "Underground Lake":
            items = {
                "Fresh Water": (3, 5),
                "Stone": (1, 3),
                "Crystal": (0, 2)
            }
            
            # Dark area is spooky and might cause stress
            if random.random() < 0.3:
                energy_loss = random.randint(3, 8)
                gs.energy = max(0, gs.energy - energy_loss)
                print(f"{Fore.RED}The darkness and echoing sounds make you uneasy. You lose {energy_loss} additional energy.{Style.RESET_ALL}")
            
        elif location == "Pirate Camp":
            items = {
                "Wood": (1, 2),
                "Metal": (0, 2)
            }
            
            # Chance to find pirate treasure
            if random.random() < 0.2:
                print(f"{Fore.YELLOW}Hidden beneath some debris, you find a small treasure chest!{Style.RESET_ALL}")
                gs.inventory["Pirate Treasure"] += 1
                print(f"{Fore.GREEN}You found {Fore.CYAN}Pirate Treasure{Fore.GREEN}!{Style.RESET_ALL}")
                
                # Update pirate quest objectives if active
                if "pirate_threat" in gs.active_quests:
                    gs.update_quest_objective("pirate_threat", "locate_treasure", True)
                    print(f"{Fore.MAGENTA}Quest updated: Pirate Problem{Style.RESET_ALL}")
            
            # Chance to spy on pirates for the quest
            if "pirate_threat" in gs.active_quests:
                if "objectives" in gs.active_quests["pirate_threat"] and "spy_on_pirates" in gs.active_quests["pirate_threat"]["objectives"]:
                    if not gs.active_quests["pirate_threat"]["objectives"]["spy_on_pirates"]:
                        print(f"{Fore.YELLOW}You overhear pirates discussing their plans. They seem to be searching for something valuable.{Style.RESET_ALL}")
                        gs.update_quest_objective("pirate_threat", "spy_on_pirates", True)
                        print(f"{Fore.MAGENTA}Quest updated: Pirate Problem{Style.RESET_ALL}")
                
            # Chance to find a treasure map
            if "pirate_threat" in gs.active_quests:
                if "objectives" in gs.active_quests["pirate_threat"] and "find_treasure_map" in gs.active_quests["pirate_threat"]["objectives"]:
                    if not gs.active_quests["pirate_threat"]["objectives"]["find_treasure_map"]:
                        if random.random() < 0.3:
                            print(f"{Fore.YELLOW}Among the pirate belongings, you discover a tattered map with markings that could lead to treasure!{Style.RESET_ALL}")
                            gs.update_quest_objective("pirate_threat", "find_treasure_map", True)
                            print(f"{Fore.MAGENTA}Quest updated: Pirate Problem{Style.RESET_ALL}")
                
        elif location == "Bamboo Grove":
            items = {
                "Bamboo": (3, 6),
                "Vine": (1, 3),
                "Leaf": (1, 3)
            }
            
            print(f"{Fore.GREEN}The bamboo here is perfect for building stronger structures!{Style.RESET_ALL}")
            
        elif location == "Crystal Cave":
            items = {
                "Crystal": (1, 3),
                "Stone": (2, 4)
            }
            
            # Beautiful environment boosts morale
            energy_gain = random.randint(5, 10)
            gs.energy = min(100, gs.energy + energy_gain)
            print(f"{Fore.GREEN}The beautiful crystal formations boost your spirits! You gain {energy_gain} energy.{Style.RESET_ALL}")
            
        elif location == "Ancient Temple":
            items = {
                "Stone": (1, 2),
                "Crystal": (1, 2),
                "Obsidian": (0, 2)
            }
            
            # Chance to find special items
            if random.random() < 0.3:
                print(f"{Fore.YELLOW}Deep within the temple, you discover an ancient device!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}This technology seems far more advanced than expected!{Style.RESET_ALL}")
                
                # Update quest objectives if active
                if "temple_mystery" in gs.active_quests:
                    gs.update_quest_objective("temple_mystery", "solve_temple_puzzle", True)
                    print(f"{Fore.MAGENTA}Quest updated: Temple of the Ancients{Style.RESET_ALL}")
                    
                if "ancient_technology" in gs.active_quests:
                    if "objectives" in gs.active_quests["ancient_technology"]:
                        # Update power source objective
                        if "find_power_source" in gs.active_quests["ancient_technology"]["objectives"] and not gs.active_quests["ancient_technology"]["objectives"]["find_power_source"]:
                            print(f"{Fore.YELLOW}You find a strange crystal that seems to power the ancient device!{Style.RESET_ALL}")
                            gs.update_quest_objective("ancient_technology", "find_power_source", True)
                            gs.inventory["Power Crystal"] = gs.inventory.get("Power Crystal", 0) + 1
                            print(f"{Fore.MAGENTA}Quest updated: Lost Technology{Style.RESET_ALL}")
                        
                        # Update activate device objective
                        elif "activate_device" in gs.active_quests["ancient_technology"]["objectives"] and not gs.active_quests["ancient_technology"]["objectives"]["activate_device"]:
                            print(f"{Fore.YELLOW}After studying the markings, you manage to activate the ancient device!{Style.RESET_ALL}")
                            gs.update_quest_objective("ancient_technology", "activate_device", True)
                            print(f"{Fore.MAGENTA}Quest updated: Lost Technology{Style.RESET_ALL}")
                            
                        # Update master technology objective
                        elif "master_technology" in gs.active_quests["ancient_technology"]["objectives"] and not gs.active_quests["ancient_technology"]["objectives"]["master_technology"]:
                            print(f"{Fore.YELLOW}With your continued study, you've finally mastered the ancient technology!{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}This knowledge could revolutionize modern science!{Style.RESET_ALL}")
                            gs.update_quest_objective("ancient_technology", "master_technology", True)
                            print(f"{Fore.MAGENTA}Quest updated: Lost Technology{Style.RESET_ALL}")
            
        elif location == "Mangrove Shore":
            items = {
                "Wood": (2, 4),
                "Vine": (1, 3),
                "Fish": (0, 2),
                "Clay": (1, 3)
            }
            
            # Good fishing spot
            if gs.inventory["Fishing Rod"] > 0 and random.random() < 0.6:
                fish_amount = random.randint(2, 4)
                gs.inventory["Fish"] += fish_amount
                print(f"{Fore.GREEN}The mangrove roots provide shelter for many fish! You catch {fish_amount} fish!{Style.RESET_ALL}")
            
        elif location == "Quicksand Pit":
            items = {
                "Sand": (3, 5),
                "Clay": (1, 3)
            }
            
            # Dangerous area drains energy
            energy_loss = random.randint(10, 15)
            gs.energy = max(0, gs.energy - energy_loss)
            print(f"{Fore.RED}Navigating around the quicksand is exhausting! You lose {energy_loss} additional energy.{Style.RESET_ALL}")
            
        elif location == "Hidden Cove":
            items = {
                "Wood": (1, 3),
                "Stone": (1, 2),
                "Fish": (1, 3),
                "Metal": (0, 1)
            }
            
            # Chance to find ship parts
            if random.random() < 0.25:
                print(f"{Fore.YELLOW}You find some usable parts that must have washed ashore from shipwrecks!{Style.RESET_ALL}")
                gs.inventory["Ship Parts"] += 1
                print(f"{Fore.GREEN}You found {Fore.CYAN}Ship Parts{Fore.GREEN}!{Style.RESET_ALL}")
            
        elif location == "Island Summit":
            items = {
                "Stone": (2, 4),
                "Crystal": (0, 1)
            }
            
            # From the summit, you can see far
            if random.random() < 0.5:
                locked_locations = [loc for loc, unlocked in gs.locations.items() 
                                  if not unlocked and loc not in ["Shelter"]]
                if locked_locations:
                    new_location = random.choice(locked_locations)
                    gs.locations[new_location] = True
                    
                    # Connect the newly discovered location to the most appropriate other location
                    if new_location not in gs.island_map:
                        # Find a logical location to connect it to
                        possible_connections = ["Beach", "Forest", "Mountain", "Cliff Side", "Jungle"]
                        available_connections = [loc for loc in possible_connections if gs.locations.get(loc, False)]
                        
                        if available_connections:
                            connect_to = random.choice(available_connections)
                            
                            # Add the connection to the island map
                            if new_location not in gs.island_map:
                                gs.island_map[new_location] = [connect_to]
                            else:
                                gs.island_map[new_location].append(connect_to)
                                
                            if new_location not in gs.island_map.get(connect_to, []):
                                if connect_to in gs.island_map:
                                    gs.island_map[connect_to].append(new_location)
                                else:
                                    gs.island_map[connect_to] = [new_location]
                    
                    print(f"{Fore.YELLOW}From this height, you spot a {Fore.CYAN}{new_location}{Fore.YELLOW} in the distance!{Style.RESET_ALL}")
            
        elif location == "Abandoned Mine":
            items = {
                "Stone": (3, 5),
                "Metal": (1, 3),
                "Crystal": (0, 1)
            }
            
            # Chance to find special metal tools
            if random.random() < 0.2:
                print(f"{Fore.YELLOW}Deep in the mine, you discover some old mining equipment!{Style.RESET_ALL}")
                special_items = ["Pickaxe", "Axe", "Metal Tools"]
                special_item = random.choice(special_items)
                gs.inventory[special_item] += 1
                print(f"{Fore.GREEN}You found {Fore.CYAN}{special_item}{Fore.GREEN}!{Style.RESET_ALL}")
                
        else:
            items = {
                "Wood": (0, 1),
                "Stone": (0, 1)
            }
        
        # Process found items, with weather modifier affecting the amount
        for item, (min_amount, max_amount) in items.items():
            # Calculate base amount
            base_amount = random.randint(min_amount, max_amount)
            
            # Modify amount based on weather
            modified_amount = int(base_amount * weather_resource_modifier)
            
            # Ensure minimum of 1 if original range would have given something
            if min_amount > 0 and base_amount > 0 and modified_amount < 1:
                modified_amount = 1
                
            if modified_amount > 0:
                gs.inventory[item] += modified_amount
                found_items[item] = modified_amount
        
        # Show what was found
        if found_items:
            print(f"\n{Fore.GREEN}You found:{Style.RESET_ALL}")
            for item, amount in found_items.items():
                print(f"{Fore.WHITE}- {amount} {Fore.CYAN}{item}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}You didn't find anything useful this time.{Style.RESET_ALL}")
        
        # Special chance for fishing if at beach or waterfall - affected by weather
        fishing_base_chance = 0.6
        fishing_weather_modifier = 1.0
        
        # Weather affects fishing success
        if gs.weather == "Rainy":
            fishing_weather_modifier = 1.2  # Rain brings fish closer to surface
        elif gs.weather == "Stormy":
            fishing_weather_modifier = 0.4  # Storm makes fishing difficult
        elif gs.weather == "Clear":
            fishing_weather_modifier = 1.1  # Clear water helps visibility
        elif gs.weather == "Foggy":
            fishing_weather_modifier = 0.8  # Fog reduces visibility
            
        if (location in ["Beach", "Waterfall"] and gs.inventory["Fishing Rod"] > 0 and 
            random.random() < (fishing_base_chance * fishing_weather_modifier)):
            fish_amount = random.randint(1, 3)
            # Adjust fish amount by weather
            fish_amount = max(1, int(fish_amount * weather_resource_modifier))
            gs.inventory["Fish"] += fish_amount
            
            if gs.weather == "Rainy":
                print(f"\n{Fore.GREEN}The rain has brought more fish near the surface. You catch {fish_amount} fish!{Style.RESET_ALL}")
            elif gs.weather == "Stormy":
                print(f"\n{Fore.GREEN}Despite the storm, you manage to catch {fish_amount} fish!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}You use your fishing rod and catch {fish_amount} fish!{Style.RESET_ALL}")
        
        # Special chance for hunting if in forest or mountain - affected by weather
        hunting_base_chance = 0.4
        hunting_weather_modifier = 1.0
        
        # Weather affects hunting success
        if gs.weather == "Foggy":
            hunting_weather_modifier = 0.6  # Fog makes it harder to spot animals
        elif gs.weather == "Rainy":
            hunting_weather_modifier = 0.8  # Rain washes away scents and tracks
        elif gs.weather == "Clear":
            hunting_weather_modifier = 1.2  # Clear weather improves visibility
        elif gs.weather == "Hot":
            hunting_weather_modifier = 1.3  # Hot weather brings animals to water sources
            
        if (location in ["Forest", "Mountain"] and gs.inventory["Spear"] > 0 and 
            random.random() < (hunting_base_chance * hunting_weather_modifier)):
            meat_amount = random.randint(1, 2)
            # Adjust meat amount by weather
            meat_amount = max(1, int(meat_amount * weather_resource_modifier))
            gs.inventory["Meat"] += meat_amount
            
            if gs.weather == "Hot":
                print(f"\n{Fore.GREEN}The hot weather has brought animals out seeking water. You hunt {meat_amount} pieces of meat!{Style.RESET_ALL}")
            elif gs.weather == "Foggy":
                print(f"\n{Fore.GREEN}Despite the fog, you manage to hunt {meat_amount} pieces of meat!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}You successfully hunt and obtain {meat_amount} pieces of meat!{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Exploring consumed {energy_cost} energy.{Style.RESET_ALL}")
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
        
    def check_inventory(self) -> None:
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== INVENTORY ====={Style.RESET_ALL}")
        
        # Group inventory by categories
        categories = {
            "Basic Resources": ["Wood", "Stone", "Vine", "Leaf", "Coconut", "Sand"],
            "Special Resources": ["Bamboo", "Crystal", "Metal", "Clay", "Obsidian"],
            "Food": ["Fruit", "Berry", "Fish", "Meat", "Mushroom", "Exotic Fruit", "Seaweed"],
            "Water": ["Fresh Water"],
            "Basic Tools": ["Spear", "Fishing Rod", "Water Container", "Torch", "Bandage", "Map", "Rope"],
            "Advanced Tools": ["Axe", "Pickaxe", "Bow and Arrow", "Slingshot", "Compass", "Waterskin", "Medicinal Potion"],
            "Special Items": ["Pirate Treasure", "Ancient Artifact", "Ship Parts", "Signal Mirror"]
        }
        
        empty_inventory = True
        
        for category, items in categories.items():
            category_items = [(item, count) for item, count in gs.inventory.items() 
                             if item in items and count > 0]
            
            if category_items:
                empty_inventory = False
                print(f"\n{Fore.YELLOW}{category}:{Style.RESET_ALL}")
                for item, count in category_items:
                    print(f"{Fore.WHITE}- {Fore.CYAN}{item}: {Fore.GREEN}{count}{Style.RESET_ALL}")
        
        if empty_inventory:
            print(f"\n{Fore.RED}Your inventory is empty.{Style.RESET_ALL}")
            
        # Check for quest resources for conqueror path
        if "island_ruler" in gs.active_quests and not gs.active_quests["island_ruler"]["objectives"]["collect_resources"]:
            if (gs.inventory.get("Wood", 0) >= 30 and 
                gs.inventory.get("Stone", 0) >= 20 and 
                gs.inventory.get("Metal", 0) >= 10):
                print(f"\n{Fore.MAGENTA}You now have enough resources to build a stronghold!{Style.RESET_ALL}")
                gs.update_quest_objective("island_ruler", "collect_resources", True)
                print(f"{Fore.MAGENTA}Quest updated: Island Ruler{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_crafting_menu(self) -> None:
        gs = self.game_state
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}===== CRAFTING ====={Style.RESET_ALL}")
            
            print(f"\n{Fore.WHITE}Available recipes:{Style.RESET_ALL}")
            
            # Display recipes with ingredient requirements
            for i, (item, ingredients) in enumerate(gs.crafting_recipes.items(), 1):
                # Skip recipes for items that are already built/active
                if (item == "Shelter" and gs.has_shelter) or \
                   (item == "Fire" and gs.has_fire) or \
                   (item == "Signal Fire" and gs.has_signal_fire) or \
                   (item == "Raft" and gs.raft_progress >= 100):
                    continue
                    
                # Check if player has ingredients
                has_ingredients = all(gs.inventory[ing] >= amount for ing, amount in ingredients.items())
                
                # Format ingredient requirements
                ingredient_list = ", ".join([f"{amount} {ing}" for ing, amount in ingredients.items()])
                
                # Display with appropriate color
                color = Fore.GREEN if has_ingredients else Fore.RED
                print(f"{Fore.YELLOW}{i}. {color}{item} - Requires: {ingredient_list}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}0. {Fore.WHITE}Back to main menu{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (0 to cancel): {Style.RESET_ALL}")
            
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return
                
                # Get the item name at the chosen index
                available_recipes = [item for item in gs.crafting_recipes.keys() 
                                   if not ((item == "Shelter" and gs.has_shelter) or 
                                          (item == "Fire" and gs.has_fire) or 
                                          (item == "Signal Fire" and gs.has_signal_fire) or 
                                          (item == "Raft" and gs.raft_progress >= 100))]
                
                if 1 <= choice_num <= len(available_recipes):
                    item_to_craft = available_recipes[choice_num-1]
                    self.craft_item(item_to_craft)
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                    input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    
            except ValueError:
                print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")
                input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def craft_item(self, item: str) -> None:
        gs = self.game_state
        ingredients = gs.crafting_recipes[item]
        
        # Check if player has required ingredients
        has_ingredients = all(gs.inventory[ing] >= amount for ing, amount in ingredients.items())
        
        if has_ingredients:
            # Consume ingredients
            for ingredient, amount in ingredients.items():
                gs.inventory[ingredient] -= amount
            
            # Apply crafting effect
            if item == "Shelter":
                gs.has_shelter = True
                gs.locations["Shelter"] = True
                print(f"\n{Fore.GREEN}You've built a shelter! It will protect you from the elements.{Style.RESET_ALL}")
                print(Fore.YELLOW + "[Shelter constructed]" + Style.RESET_ALL)
            
            elif item == "Strong Shelter":
                gs.has_shelter = True
                gs.locations["Shelter"] = True
                print(f"\n{Fore.GREEN}You've built a strong shelter! It will provide excellent protection in all weather conditions.{Style.RESET_ALL}")
                print(Fore.YELLOW + "[Strong shelter constructed]" + Style.RESET_ALL)
            
            elif item == "Stronghold":
                gs.has_shelter = True
                gs.locations["Shelter"] = True
                gs.locations["Stronghold"] = True  # Add a new location
                print(f"\n{Fore.GREEN}You've built a formidable stronghold! This will be your base of operations.{Style.RESET_ALL}")
                print(Fore.YELLOW + "[Stronghold constructed]" + Style.RESET_ALL)
                
                # Update quest objective if active
                if "island_ruler" in gs.active_quests:
                    gs.update_quest_objective("island_ruler", "build_stronghold", True)
                    print(f"{Fore.MAGENTA}Quest updated: Island Ruler{Style.RESET_ALL}")
            
            elif item == "Fire":
                gs.has_fire = True
                gs.fire_remaining_time = 6  # Lasts for 6 time periods
                print(f"\n{Fore.GREEN}You've started a fire! It will keep you warm for a while.{Style.RESET_ALL}")
                print(Fore.RED + "[Fire has been started]" + Style.RESET_ALL)
            
            elif item == "Signal Fire":
                gs.has_signal_fire = True
                print(f"\n{Fore.GREEN}You've built a signal fire! It's ready to be lit if you see a ship.{Style.RESET_ALL}")
                print(Fore.RED + "[Signal fire prepared]" + Style.RESET_ALL)
            
            elif item == "Raft":
                # Check if player has Ship Parts to enhance the raft
                if gs.inventory["Ship Parts"] > 0:
                    gs.raft_progress = 60  # Better starting progress with ship parts
                    gs.raft_type = "Ship Parts"
                    gs.inventory["Ship Parts"] -= 1
                    print(f"\n{Fore.GREEN}You've started building a raft using the ship parts you found! It's sturdier and more seaworthy.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Ship Parts used: 1{Style.RESET_ALL}")
                else:
                    gs.raft_progress = 35  # Standard progress without ship parts
                    gs.raft_type = "Standard"
                    print(f"\n{Fore.GREEN}You've started building a raft! Continue gathering materials to complete it.{Style.RESET_ALL}")
                print(Fore.BLUE + "[Building standard raft...]" + Style.RESET_ALL)
                
            elif item == "Bamboo Raft":
                # Check if player has Ship Parts to enhance the raft
                if gs.inventory["Ship Parts"] > 0:
                    gs.raft_progress = 75  # Even better progress with bamboo + ship parts
                    gs.raft_type = "Bamboo and Ship Parts"
                    gs.inventory["Ship Parts"] -= 1
                    print(f"\n{Fore.GREEN}You've started building a bamboo raft enhanced with ship parts! This will be very seaworthy.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Ship Parts used: 1{Style.RESET_ALL}")
                else:
                    gs.raft_progress = 50  # Better progress with just bamboo
                    gs.raft_type = "Bamboo"
                    print(f"\n{Fore.GREEN}You've started building a bamboo raft! The bamboo makes it easier to build and more buoyant.{Style.RESET_ALL}")
                print(Fore.BLUE + "[Building bamboo raft...]" + Style.RESET_ALL)
            
            elif item == "Signal Mirror":
                gs.inventory[item] += 1
                gs.has_signal_mirror = True
                print(f"\n{Fore.GREEN}You've crafted a signal mirror! This will improve your chances of being spotted by passing ships.{Style.RESET_ALL}")
            
            else:  # Regular items
                gs.inventory[item] += 1
                print(f"\n{Fore.GREEN}You've crafted a {item}!{Style.RESET_ALL}")
            
            # Crafting costs energy - affected by weather
            base_energy_cost = random.randint(5, 15)
            weather_energy_modifier = 1.0
            
            # Weather affects crafting
            if gs.weather == "Hot":
                weather_energy_modifier = 1.3  # Hot weather makes crafting more tiring
                weather_msg = f"{Fore.YELLOW}The hot weather makes crafting more tiring.{Style.RESET_ALL}"
            elif gs.weather == "Rainy":
                weather_energy_modifier = 1.2  # Rain makes outdoor work harder
                weather_msg = f"{Fore.BLUE}The rain makes crafting more challenging.{Style.RESET_ALL}"
            elif gs.weather == "Stormy":
                weather_energy_modifier = 1.5  # Storms make outdoor work much harder
                weather_msg = f"{Fore.RED}The storm makes crafting very difficult.{Style.RESET_ALL}"
            elif gs.weather == "Clear":
                weather_energy_modifier = 0.9  # Clear weather is good for working
                weather_msg = f"{Fore.GREEN}The clear weather makes crafting easier.{Style.RESET_ALL}"
            elif gs.weather == "Foggy":
                weather_energy_modifier = 1.1  # Fog makes it a bit harder to see what you're doing
                weather_msg = f"{Fore.WHITE}The fog makes it slightly harder to see what you're doing.{Style.RESET_ALL}"
            else:
                weather_msg = ""
                
            # Being in a shelter reduces weather effects on crafting
            if gs.has_shelter and gs.current_location == "Shelter":
                weather_energy_modifier = max(0.9, weather_energy_modifier * 0.7)  # Shelter reduces weather effects
                if weather_msg:
                    weather_msg = f"{Fore.GREEN}Your shelter protects you from the weather.{Style.RESET_ALL}"
                    
            energy_cost = int(base_energy_cost * weather_energy_modifier)
            gs.energy -= energy_cost
            
            if weather_msg:
                print(weather_msg)
                
            print(f"{Fore.YELLOW}Crafting consumed {energy_cost} energy.{Style.RESET_ALL}")
            
        else:
            print(f"\n{Fore.RED}You don't have enough materials to craft {item}.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def eat_drink_menu(self) -> None:
        gs = self.game_state
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}===== EAT/DRINK ====={Style.RESET_ALL}")
            
            # Display current hunger and thirst
            hunger_color = Fore.GREEN if gs.hunger > 50 else (Fore.YELLOW if gs.hunger > 25 else Fore.RED)
            thirst_color = Fore.GREEN if gs.thirst > 50 else (Fore.YELLOW if gs.thirst > 25 else Fore.RED)
            
            print(f"{Fore.WHITE}Hunger: {hunger_color}{self.create_bar(gs.hunger)}{Style.RESET_ALL} {gs.hunger}%")
            print(f"{Fore.WHITE}Thirst: {thirst_color}{self.create_bar(gs.thirst)}{Style.RESET_ALL} {gs.thirst}%")
            
            # Food items
            food_items = [
                # Basic items
                ("Fruit", 15), 
                ("Berry", 10), 
                ("Coconut", 20),
                ("Mushroom", 12),
                ("Exotic Fruit", 20),
                ("Seaweed", 8),
                
                # Fish from fishing activity
                ("Small Fish", 15),
                ("Medium Fish", 25),
                ("Large Fish", 40),
                ("Exotic Fish", 30),
                
                # Meat from hunting activity
                ("Small Game", 25),
                ("Wild Pig Meat", 45),
                ("Venison", 60),
                ("Chicken", 35),
                ("Exotic Bird", 30),
                
                # Legacy items for compatibility
                ("Fish", 25), 
                ("Meat", 35)
            ]
            available_food = [(item, value, gs.inventory[item]) 
                             for item, value in food_items if gs.inventory[item] > 0]
            
            # Water items
            water_items = [
                ("Fresh Water", 30), 
                ("Coconut", 15),
                ("Waterskin", 40),  # Waterskin holds more water
                ("Exotic Fish", 20)  # Exotic fish provides hydration
            ]
            available_water = [(item, value, gs.inventory[item]) 
                              for item, value in water_items if gs.inventory[item] > 0]
            
            # Display available food
            if available_food:
                print(f"\n{Fore.YELLOW}Available Food:{Style.RESET_ALL}")
                for i, (item, value, quantity) in enumerate(available_food, 1):
                    print(f"{Fore.WHITE}{i}. {Fore.CYAN}{item} {Fore.WHITE}(+{value} hunger) - {Fore.GREEN}{quantity} available{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}No food available.{Style.RESET_ALL}")
            
            # Display available water
            if available_water:
                print(f"\n{Fore.YELLOW}Available Drinks:{Style.RESET_ALL}")
                for i, (item, value, quantity) in enumerate(available_water, 1):
                    offset = len(available_food)
                    print(f"{Fore.WHITE}{i+offset}. {Fore.CYAN}{item} {Fore.WHITE}(+{value} thirst) - {Fore.GREEN}{quantity} available{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}No drinks available.{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}0. {Fore.WHITE}Back to main menu{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (0 to cancel): {Style.RESET_ALL}")
            
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return
                
                all_consumables = available_food + available_water
                
                if 1 <= choice_num <= len(all_consumables):
                    item, value, _ = all_consumables[choice_num-1]
                    
                    # Consume the item
                    gs.inventory[item] -= 1
                    
                    # Apply effects
                    if item in [food[0] for food in food_items]:
                        gs.hunger = min(100, gs.hunger + value)
                        print(f"\n{Fore.GREEN}You ate {item} and gained {value} hunger points.{Style.RESET_ALL}")
                        
                    if item in [water[0] for water in water_items]:
                        gs.thirst = min(100, gs.thirst + value)
                        print(f"{Fore.GREEN}You drank from {item} and gained {value} thirst points.{Style.RESET_ALL}")
                        
                    # Coconuts provide both food and water
                    if item == "Coconut":
                        print(f"{Fore.GREEN}Coconuts provide both food and water!{Style.RESET_ALL}")
                        
                    # Medicinal potion heals health
                    if item == "Medicinal Potion":
                        health_gain = 25
                        gs.health = min(100, gs.health + health_gain)
                        print(f"{Fore.GREEN}The medicinal potion heals your wounds. You gain {health_gain} health points!{Style.RESET_ALL}")
                    
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                    input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    
            except ValueError:
                print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")
                input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def rest(self) -> None:
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== REST ====={Style.RESET_ALL}")
        
        # Rest effects
        energy_gain = 30  # Base energy gain
        health_gain = 5   # Base health gain
        
        # Better rest in shelter
        in_shelter = (gs.current_location == "Shelter" or gs.has_shelter)
        if in_shelter:
            energy_gain += 15
            health_gain += 5
            print(f"{Fore.GREEN}You rest comfortably in your shelter.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}You rest on the ground.{Style.RESET_ALL}")
        
        # Fire provides additional benefits
        if gs.has_fire:
            energy_gain += 10
            health_gain += 3
            print(f"{Fore.YELLOW}The warmth of the fire helps you rest better.{Style.RESET_ALL}")
            
        # Weather effects on rest
        weather_msg = ""
        if gs.weather == "Rainy" and not in_shelter:
            energy_gain -= 10
            health_gain -= 2
            weather_msg = f"{Fore.BLUE}The rain makes it difficult to rest properly.{Style.RESET_ALL}"
        elif gs.weather == "Stormy" and not in_shelter:
            energy_gain -= 20
            health_gain -= 5
            weather_msg = f"{Fore.RED}The storm makes it almost impossible to rest outdoors.{Style.RESET_ALL}"
        elif gs.weather == "Hot":
            energy_gain -= 5
            weather_msg = f"{Fore.YELLOW}The heat makes you restless.{Style.RESET_ALL}"
            if in_shelter:
                weather_msg = f"{Fore.YELLOW}Even in your shelter, the heat makes you a bit restless.{Style.RESET_ALL}"
                energy_gain -= 2  # Less effect in shelter
        elif gs.weather == "Clear" and not in_shelter:
            energy_gain += 5
            health_gain += 2
            weather_msg = f"{Fore.GREEN}The pleasant weather helps you rest better outdoors.{Style.RESET_ALL}"
        elif gs.weather == "Foggy" and not in_shelter:
            energy_gain -= 5
            weather_msg = f"{Fore.WHITE}The damp fog makes outdoor rest less effective.{Style.RESET_ALL}"
            
        # Ensure minimum gains
        energy_gain = max(10, energy_gain)
        health_gain = max(0, health_gain)
        
        # Display weather effects if any
        if weather_msg:
            print(weather_msg)
        
        # Apply rest effects
        gs.energy = min(100, gs.energy + energy_gain)
        gs.health = min(100, gs.health + health_gain)
        
        print(f"\n{Fore.GREEN}You feel refreshed! +{energy_gain} energy, +{health_gain} health.{Style.RESET_ALL}")
        
        # Resting advances time
        gs.update_status()
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def travel_menu(self) -> None:
        gs = self.game_state
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}===== TRAVEL ====={Style.RESET_ALL}")
            print(f"{Fore.WHITE}Current location: {Fore.YELLOW}{gs.current_location}{Style.RESET_ALL}")
            
            # Show available connected locations based on the island map
            print(f"\n{Fore.WHITE}Available locations:{Style.RESET_ALL}")
            
            # Get locations connected to current location from island map
            connected_locations = []
            
            if gs.current_location in gs.island_map:
                connected_locations = gs.island_map[gs.current_location]
            
            # Filter out locations that are unlocked
            available_locations = []
            for i, location in enumerate(connected_locations, 1):
                if gs.locations.get(location, False):
                    available_locations.append((i, location))
            
            if available_locations:
                for i, location in available_locations:
                    print(f"{Fore.YELLOW}{i}. {Fore.CYAN}{location}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No other locations available from here.{Style.RESET_ALL}")
            
            # Special case for raft if it's complete
            if gs.raft_progress >= 100:
                print(f"{Fore.YELLOW}{len(available_locations) + 1}. {Fore.CYAN}Use Raft to Escape{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}0. {Fore.WHITE}Back to main menu{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice (0 to cancel): {Style.RESET_ALL}")
            
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return
                
                # Handle raft escape option
                if gs.raft_progress >= 100 and choice_num == len(available_locations) + 1:
                    print(f"\n{Fore.CYAN}You push your raft into the water and set sail, hoping to find rescue...{Style.RESET_ALL}")
                    time.sleep(2)
                    
                    # Base chance of successful escape starts at 60%
                    escape_chance = 0.6
                    
                    # Different raft types provide different success chances
                    if gs.raft_type == "Bamboo":
                        escape_chance += 0.1
                        print(f"{Fore.YELLOW}The bamboo raft is lighter and more buoyant, improving your chances.{Style.RESET_ALL}")
                    elif gs.raft_type == "Ship Parts":
                        escape_chance += 0.15
                        print(f"{Fore.YELLOW}The ship parts make your raft more seaworthy, improving your chances.{Style.RESET_ALL}")
                    elif gs.raft_type == "Bamboo and Ship Parts":
                        escape_chance += 0.25
                        print(f"{Fore.YELLOW}Your bamboo raft with ship parts is extremely seaworthy, significantly improving your chances.{Style.RESET_ALL}")
                    
                    # Signal Mirror helps with rescue if spotted by a ship during escape
                    if gs.has_signal_mirror:
                        escape_chance += 0.1
                        print(f"{Fore.YELLOW}You bring your signal mirror, which can help passing ships spot you.{Style.RESET_ALL}")
                    
                    # Weather conditions significantly affect escape chances
                    weather_modifier = 0.0
                    weather_msg = ""
                    
                    if gs.weather == "Clear":
                        weather_modifier = 0.15
                        weather_msg = f"{Fore.GREEN}The clear weather gives you excellent visibility and calm seas. +15% chance{Style.RESET_ALL}"
                    elif gs.weather == "Foggy":
                        weather_modifier = -0.2
                        weather_msg = f"{Fore.WHITE}The fog severely limits visibility, making navigation very difficult. -20% chance{Style.RESET_ALL}"
                    elif gs.weather == "Rainy":
                        weather_modifier = -0.1
                        weather_msg = f"{Fore.BLUE}The rain reduces visibility and makes the journey more challenging. -10% chance{Style.RESET_ALL}"
                    elif gs.weather == "Stormy":
                        weather_modifier = -0.3
                        weather_msg = f"{Fore.RED}The storm makes sailing extremely dangerous! It would be wiser to wait for better weather. -30% chance{Style.RESET_ALL}"
                    elif gs.weather == "Hot":
                        weather_modifier = 0.05
                        weather_msg = f"{Fore.YELLOW}The hot weather is exhausting but provides good visibility. +5% chance{Style.RESET_ALL}"
                        
                    escape_chance += weather_modifier
                    if weather_msg:
                        print(weather_msg)
                        
                    # Cap escape chance between 10% and 95%
                    if escape_chance < 0.1:
                        escape_chance = 0.1
                    elif escape_chance > 0.95:
                        escape_chance = 0.95
                    
                    # Show escape chance (rounded to nearest 5%)
                    displayed_chance = round(escape_chance * 100 / 5) * 5
                    print(f"\n{Fore.CYAN}Estimated survival chance: {displayed_chance}%{Style.RESET_ALL}")
                    
                    time.sleep(2)
                    print(f"\n{Fore.WHITE}You paddle out into the open sea...{Style.RESET_ALL}")
                    time.sleep(2)
                    
                    # Attempt escape
                    if random.random() < escape_chance:
                        gs.rescued = True
                        gs.message = "After days at sea, you're spotted by a passing ship. You've escaped the island!"
                        print(f"\n{Fore.GREEN}Success! {gs.message}{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.RED}A massive storm hits! Your raft is being tossed by massive waves!{Style.RESET_ALL}")
                        time.sleep(1)
                        print(f"{Fore.RED}The raft breaks apart and you're washed back to shore.{Style.RESET_ALL}")
                        
                        gs.raft_progress = 0
                        gs.health -= 20
                        gs.energy -= 30
                        
                        # More descriptive failure message
                        failure_message = "Your raft has been destroyed by a storm. "
                        
                        if gs.raft_type != "Standard":
                            failure_message += f"Despite your {gs.raft_type} raft's quality, the sea was too rough. "
                        
                        failure_message += "You'll need to build another one."
                        gs.raft_type = ""  # Reset raft type
                        gs.message = failure_message
                    
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                # Regular travel
                if 1 <= choice_num <= len(available_locations):
                    _, new_location = available_locations[choice_num-1]
                    
                    # Travel costs energy - affected by weather
                    base_energy_cost = random.randint(10, 20)
                    weather_energy_modifier = 1.0
                    weather_msg = ""
                    
                    # Weather affects travel
                    if gs.weather == "Rainy":
                        weather_energy_modifier = 1.3  # Rain makes travel more difficult
                        weather_msg = f"{Fore.BLUE}The rain makes travel more challenging.{Style.RESET_ALL}"
                    elif gs.weather == "Stormy":
                        weather_energy_modifier = 1.8  # Storms make travel very difficult
                        weather_msg = f"{Fore.RED}The storm makes travel extremely difficult and dangerous.{Style.RESET_ALL}"
                    elif gs.weather == "Foggy":
                        weather_energy_modifier = 1.5  # Fog makes navigation harder
                        weather_msg = f"{Fore.WHITE}The fog makes it hard to find your way.{Style.RESET_ALL}"
                    elif gs.weather == "Hot":
                        weather_energy_modifier = 1.2  # Hot weather is tiring
                        weather_msg = f"{Fore.YELLOW}The heat makes travel more tiring.{Style.RESET_ALL}"
                    elif gs.weather == "Clear":
                        weather_energy_modifier = 0.8  # Clear weather is good for travel
                        weather_msg = f"{Fore.GREEN}The clear weather makes travel easier.{Style.RESET_ALL}"
                    
                    # Calculate actual energy cost
                    energy_cost = int(base_energy_cost * weather_energy_modifier)
                    gs.energy -= energy_cost
                    
                    # Update location
                    gs.current_location = new_location
                    gs.update_status()  # Travel takes time
                    
                    # Display weather message if applicable
                    if weather_msg:
                        print(weather_msg)
                    
                    print(f"\n{Fore.GREEN}You travel to {new_location}. (-{energy_cost} energy){Style.RESET_ALL}")
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    return
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                    input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    
            except ValueError:
                print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")
                input(f"{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def randomize_island_map(self) -> None:
        """Randomizes the connections between locations"""
        gs = self.game_state
        
        # If map file exists, load it
        if os.path.exists(self.map_file):
            try:
                with open(self.map_file, 'r') as f:
                    map_data = json.load(f)
                    
                    # Validate the loaded map
                    for location in gs.locations.keys():
                        if location not in ["Shelter", "Stronghold"] and location not in map_data:
                            raise ValueError(f"Missing location in map: {location}")
                    
                    gs.island_map = map_data
                    return
            except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
                print(f"{Fore.RED}Error loading island map: {e}. Generating new map...{Style.RESET_ALL}")
                # If loading fails, continue with randomization
        
        # Maintain key locations connections
        key_connections = {
            "Beach": ["Forest"],
            "Forest": ["Beach", "Mountain"],
            "Mountain": ["Forest", "Cave"],
            "Cave": ["Mountain"],
            # Special locations that aren't part of the travel network
            "Shelter": [],
            "Stronghold": []
        }
        
        # Create a new randomized map
        new_map = {}
        
        # Filter out special locations that aren't part of the travel network
        non_travel_locations = ["Shelter", "Stronghold"]
        all_locations = [loc for loc in gs.locations.keys() if loc not in non_travel_locations]
        
        for location in all_locations:
            # Start with any required connections
            connections = key_connections.get(location, []).copy()
            
            # Add 1-3 random connections
            possible_connections = [loc for loc in all_locations 
                                   if loc != location and loc not in connections 
                                   and loc not in non_travel_locations]
            
            num_connections = min(len(possible_connections), random.randint(1, 3))
            
            if possible_connections and num_connections > 0:
                connections.extend(random.sample(possible_connections, num_connections))
            
            new_map[location] = connections
        
        # Ensure all locations are reachable from Beach
        reachable = set(["Beach"])
        frontier = ["Beach"]
        
        while frontier:
            current = frontier.pop(0)
            for next_loc in new_map.get(current, []):
                if next_loc not in reachable:
                    reachable.add(next_loc)
                    frontier.append(next_loc)
        
        # Add additional paths for unreachable locations
        unreachable = set(all_locations) - reachable
        for location in unreachable:
            if location not in new_map:
                new_map[location] = []
                
            connect_to = random.choice(list(reachable))
            new_map[connect_to].append(location)
            new_map[location].append(connect_to)
        
        # Make sure all regular locations are in the map
        for location in all_locations:
            if location not in new_map:
                new_map[location] = ["Beach"]  # Connect to Beach as fallback
                new_map["Beach"].append(location)
        
        # Save the map
        gs.island_map = new_map
        try:
            with open(self.map_file, 'w') as f:
                json.dump(new_map, f)
        except Exception as e:
            print(f"{Fore.RED}Error saving island map: {e}{Style.RESET_ALL}")
            # If saving fails, continue with the game
    
    def go_fishing(self) -> None:
        """Handle fishing activity - requires a fishing rod"""
        gs = self.game_state
        
        # Check if the player has a fishing rod
        if gs.inventory["Fishing Rod"] <= 0:
            print(f"{Fore.RED}You need a Fishing Rod to go fishing. Try crafting one first.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Check if player is at a suitable location
        water_locations = ["Beach", "Waterfall", "Lake", "River", "Coast"]
        if gs.current_location not in water_locations:
            print(f"{Fore.RED}You can't fish here. Try going to the Beach, Waterfall, Lake, River, or Coast.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}You cast your fishing line into the water...{Style.RESET_ALL}")
        time.sleep(1.5)
        
        # Weather effects on fishing success
        catch_chance = 0.7  # Base 70% chance
        energy_cost = random.randint(5, 10)
        
        if gs.weather == "Rainy":
            print(f"{Fore.BLUE}The rain seems to make the fish more active.{Style.RESET_ALL}")
            catch_chance += 0.1
        elif gs.weather == "Stormy":
            print(f"{Fore.RED}The choppy water makes fishing difficult.{Style.RESET_ALL}")
            catch_chance -= 0.2
            energy_cost += 3
        elif gs.weather == "Clear":
            print(f"{Fore.GREEN}Perfect fishing weather!{Style.RESET_ALL}")
            catch_chance += 0.15
            
        time.sleep(1)
        
        # Random chance to catch something
        if random.random() < catch_chance:
            # What did they catch?
            catch_types = ["Small Fish", "Medium Fish", "Large Fish", "Exotic Fish"]
            catch_weights = [0.5, 0.3, 0.15, 0.05]  # Probabilities
            catch = random.choices(catch_types, weights=catch_weights, k=1)[0]
            
            if catch == "Small Fish":
                food_value = random.randint(10, 20)
                print(f"{Fore.GREEN}You caught a small fish! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Small Fish"] += 1
            elif catch == "Medium Fish":
                food_value = random.randint(20, 35)
                print(f"{Fore.GREEN}You caught a good-sized fish! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Medium Fish"] += 1
            elif catch == "Large Fish":
                food_value = random.randint(35, 50)
                print(f"{Fore.GREEN}You caught a large fish! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Large Fish"] += 1
            elif catch == "Exotic Fish":
                food_value = random.randint(30, 40)
                water_value = random.randint(15, 25)
                print(f"{Fore.GREEN}You caught a colorful exotic fish! It will restore {food_value} hunger and {water_value} thirst.{Style.RESET_ALL}")
                gs.inventory["Exotic Fish"] += 1
                
            # Small chance fishing rod breaks
            if random.random() < 0.05:  # 5% chance
                gs.inventory["Fishing Rod"] -= 1
                print(f"{Fore.RED}Your fishing rod broke during the catch!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}You didn't catch anything this time.{Style.RESET_ALL}")
            
        # Apply energy cost
        gs.energy -= energy_cost
        print(f"{Fore.BLUE}Fishing consumed {energy_cost} energy.{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def go_hunting(self) -> None:
        """Handle hunting activity - requires a spear"""
        gs = self.game_state
        
        # Check if the player has a spear
        if gs.inventory["Spear"] <= 0:
            print(f"{Fore.RED}You need a Spear to go hunting. Try crafting one first.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Check if player is at a suitable location
        hunt_locations = ["Forest", "Jungle", "Bamboo Grove", "Meadow", "Mountain"]
        if gs.current_location not in hunt_locations:
            print(f"{Fore.RED}This area is not suitable for hunting. Try going to the Forest, Jungle, or Meadow.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}You start tracking for animals to hunt...{Style.RESET_ALL}")
        time.sleep(1.5)
        
        # Weather effects on hunting success
        success_chance = 0.65  # Base 65% chance
        energy_cost = random.randint(15, 25)  # Hunting is more tiring than fishing
        
        if gs.weather == "Rainy":
            print(f"{Fore.BLUE}The rain washes away tracks, making hunting more difficult.{Style.RESET_ALL}")
            success_chance -= 0.1
        elif gs.weather == "Foggy":
            print(f"{Fore.WHITE}The fog makes it harder to see but also masks your approach.{Style.RESET_ALL}")
            success_chance -= 0.05
        elif gs.weather == "Stormy":
            print(f"{Fore.RED}Most animals are taking shelter from the storm.{Style.RESET_ALL}")
            success_chance -= 0.2
            energy_cost += 5
        elif gs.weather == "Clear":
            print(f"{Fore.GREEN}Good visibility makes tracking easier!{Style.RESET_ALL}")
            success_chance += 0.1
            
        time.sleep(1)
        
        # Random chance to hunt successfully
        if random.random() < success_chance:
            # What did they catch?
            catch_types = ["Small Game", "Wild Pig", "Deer", "Wild Chicken", "Exotic Bird"]
            catch_weights = [0.4, 0.25, 0.2, 0.1, 0.05]  # Probabilities
            catch = random.choices(catch_types, weights=catch_weights, k=1)[0]
            
            if catch == "Small Game":
                food_value = random.randint(20, 30)
                print(f"{Fore.GREEN}You caught some small game! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Small Game"] += 1
            elif catch == "Wild Pig":
                food_value = random.randint(40, 60)
                print(f"{Fore.GREEN}You caught a wild pig! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Wild Pig Meat"] += 1
                gs.inventory["Hide"] += 1
                print(f"{Fore.GREEN}You also collected 1 Hide that can be used for crafting.{Style.RESET_ALL}")
            elif catch == "Deer":
                food_value = random.randint(50, 70)
                print(f"{Fore.GREEN}You caught a deer! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Venison"] += 1
                gs.inventory["Hide"] += 2
                print(f"{Fore.GREEN}You also collected 2 Hides that can be used for crafting.{Style.RESET_ALL}")
            elif catch == "Wild Chicken":
                food_value = random.randint(30, 45)
                print(f"{Fore.GREEN}You caught a wild chicken! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Chicken"] += 1
                gs.inventory["Feather"] += random.randint(3, 7)
                print(f"{Fore.GREEN}You also collected some Feathers that can be used for crafting.{Style.RESET_ALL}")
            elif catch == "Exotic Bird":
                food_value = random.randint(25, 35)
                print(f"{Fore.GREEN}You caught an exotic bird! It will restore {food_value} hunger.{Style.RESET_ALL}")
                gs.inventory["Exotic Bird"] += 1
                gs.inventory["Colorful Feather"] += random.randint(2, 5)
                print(f"{Fore.GREEN}You also collected some Colorful Feathers that can be used for crafting.{Style.RESET_ALL}")
                
            # Small chance spear breaks
            if random.random() < 0.08:  # 8% chance
                gs.inventory["Spear"] -= 1
                print(f"{Fore.RED}Your spear broke during the hunt!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Your hunt was unsuccessful this time.{Style.RESET_ALL}")
            
        # Apply energy cost
        gs.energy -= energy_cost
        print(f"{Fore.BLUE}Hunting consumed {energy_cost} energy.{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
        
    def use_signal_mirror(self) -> None:
        """Attempt to signal for rescue using a signal mirror"""
        gs = self.game_state
        
        # Check if the player has a signal mirror
        if gs.inventory["Signal Mirror"] <= 0:
            print(f"{Fore.RED}You need a Signal Mirror to try signaling for rescue. Try crafting one first.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Weather effects on signaling success
        success_chance = 0.1  # Base 10% chance - rescue should be rare
        
        print(f"\n{Fore.CYAN}You use your signal mirror to try and catch the attention of any passing ships or aircraft...{Style.RESET_ALL}")
        time.sleep(1.5)
        
        if gs.weather == "Rainy":
            print(f"{Fore.BLUE}The rain reduces visibility, making your signal less effective.{Style.RESET_ALL}")
            success_chance -= 0.05
        elif gs.weather == "Foggy":
            print(f"{Fore.WHITE}The fog makes it nearly impossible for anyone to see your signal.{Style.RESET_ALL}")
            success_chance -= 0.08
        elif gs.weather == "Stormy":
            print(f"{Fore.RED}The storm makes signaling futile - no one would be out in this weather.{Style.RESET_ALL}")
            success_chance -= 0.09
        elif gs.weather == "Clear":
            print(f"{Fore.GREEN}The clear sky provides perfect conditions for your signal to be seen!{Style.RESET_ALL}")
            success_chance += 0.1
            
        # Check if player is at a good location for signaling
        if gs.current_location in ["Beach", "Mountain", "Island Summit", "Cliff Side"]:
            print(f"{Fore.GREEN}This elevated position improves your chances of being seen.{Style.RESET_ALL}")
            success_chance += 0.1
            
        # Update quest objective for escape quest
        if "island_escape" in gs.active_quests:
            gs.update_quest_objective("island_escape", "create_signal", True)
            print(f"{Fore.MAGENTA}Quest updated: Escape Plan{Style.RESET_ALL}")
            
        time.sleep(1)
        
        # Random chance for successful rescue
        if random.random() < success_chance:
            print(f"\n{Fore.CYAN}Wait... you see something on the horizon!{Style.RESET_ALL}")
            time.sleep(2)
            print(f"\n{Fore.GREEN}A ship has spotted your signal and is changing course to rescue you!{Style.RESET_ALL}")
            time.sleep(2)
            
            gs.rescued = True
            
            # Set ending message based on story path
            if gs.story_path == "survivor":
                gs.message = "You were rescued after signaling a passing ship with your mirror! (Survivor Ending)"
            elif gs.story_path == "explorer" and "ancient_tech_mastered" in gs.story_flags:
                gs.message = "You escaped the island with ancient knowledge that will revolutionize modern technology! (Explorer Ending)"
            elif gs.story_path == "conqueror" and "pirate_king" in gs.story_flags:
                gs.message = "You left the island with pirate treasures and tales of conquest! (Conqueror Ending)"
            else:
                gs.message = "You were rescued after signaling a passing ship with your mirror!"
                
            # Complete the escape quest if active
            if "island_escape" in gs.active_quests:
                gs.complete_quest("island_escape")
            
            # Game will end in the next update loop
        else:
            print(f"\n{Fore.YELLOW}You spend some time signaling, but no one seems to notice.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Maybe you'll have better luck next time.{Style.RESET_ALL}")
            
        # Small energy cost
        gs.energy -= random.randint(3, 8)
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def raft_menu(self) -> None:
        """Display options for building and checking a rescue raft"""
        gs = self.game_state
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}===== RAFT BUILDING ====={Style.RESET_ALL}")
            
            # Show current raft status
            if gs.raft_type == "None":
                print(f"\n{Fore.YELLOW}You have not built a raft yet.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}Current raft: {Fore.CYAN}{gs.raft_type}{Style.RESET_ALL}")
                
                # Show estimated success chance
                base_chance = 0
                if gs.raft_type == "Standard Raft":
                    base_chance = 30
                elif gs.raft_type == "Improved Raft":
                    base_chance = 50
                elif gs.raft_type == "Advanced Raft":
                    base_chance = 70
                elif gs.raft_type == "Ultimate Raft":
                    base_chance = 90
                    
                # Weather modifications
                weather_mod = 0
                if gs.weather == "Clear":
                    weather_mod = 10
                elif gs.weather == "Stormy":
                    weather_mod = -30
                elif gs.weather == "Rainy":
                    weather_mod = -10
                elif gs.weather == "Foggy":
                    weather_mod = -15
                    
                # Ensure final chance is between 5% and 95%
                final_chance = base_chance + weather_mod
                if final_chance < 5:
                    final_chance = 5
                elif final_chance > 95:
                    final_chance = 95
                print(f"{Fore.YELLOW}Estimated escape success chance: {final_chance}%{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}(Weather conditions affect success chance){Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}1. {Fore.WHITE}Build Standard Raft (10 Wood, 5 Vine)")
            print(f"{Fore.YELLOW}2. {Fore.WHITE}Build Improved Raft (15 Wood, 10 Vine, 3 Hide)")
            print(f"{Fore.YELLOW}3. {Fore.WHITE}Build Advanced Raft (20 Wood, 15 Vine, 5 Hide)")
            print(f"{Fore.YELLOW}4. {Fore.WHITE}Build Ultimate Raft (25 Wood, 20 Vine, 10 Hide, 5 Ship Parts)")
            print(f"{Fore.YELLOW}5. {Fore.WHITE}Attempt Escape (use your current raft)")
            print(f"{Fore.YELLOW}0. {Fore.WHITE}Return to main menu")
            
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == "1":
                self.build_raft("Standard Raft", {"Wood": 10, "Vine": 5})
            elif choice == "2":
                self.build_raft("Improved Raft", {"Wood": 15, "Vine": 10, "Hide": 3})
            elif choice == "3":
                self.build_raft("Advanced Raft", {"Wood": 20, "Vine": 15, "Hide": 5})
            elif choice == "4":
                self.build_raft("Ultimate Raft", {"Wood": 25, "Vine": 20, "Hide": 10, "Ship Parts": 5})
            elif choice == "5":
                self.attempt_escape()
            elif choice == "0":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                time.sleep(1)
    
    def build_raft(self, raft_type: str, materials: dict) -> None:
        """Build a specific type of raft"""
        gs = self.game_state
        
        # Check if player has required materials
        can_build = True
        for material, amount in materials.items():
            if gs.inventory[material] < amount:
                can_build = False
                print(f"{Fore.RED}You don't have enough {material}. Need {amount}, have {gs.inventory[material]}.{Style.RESET_ALL}")
        
        # Check if player is at beach
        if gs.current_location != "Beach":
            print(f"{Fore.RED}You need to be at the Beach to build a raft.{Style.RESET_ALL}")
            can_build = False
            
        if can_build:
            # Consume materials
            for material, amount in materials.items():
                gs.inventory[material] -= amount
                
            # Set new raft type
            gs.raft_type = raft_type
            
            print(f"{Fore.GREEN}You've successfully built a {raft_type}!{Style.RESET_ALL}")
            
            # Update quest objective if the escape quest is active
            if "island_escape" in gs.active_quests:
                gs.update_quest_objective("island_escape", "build_raft", True)
                print(f"{Fore.MAGENTA}Quest updated: Escape Plan{Style.RESET_ALL}")
            
            # Energy cost
            energy_cost = random.randint(20, 30)
            gs.energy -= energy_cost
            print(f"{Fore.BLUE}Building the raft consumed {energy_cost} energy.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def attempt_escape(self) -> None:
        """Try to escape the island using the current raft"""
        gs = self.game_state
        
        if gs.raft_type == "None":
            print(f"{Fore.RED}You need to build a raft before attempting to escape.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        if gs.current_location != "Beach":
            print(f"{Fore.RED}You need to be at the Beach to launch your raft.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Calculate success chance
        base_chance = 0
        if gs.raft_type == "Standard Raft":
            base_chance = 30
        elif gs.raft_type == "Improved Raft":
            base_chance = 50
        elif gs.raft_type == "Advanced Raft":
            base_chance = 70
        elif gs.raft_type == "Ultimate Raft":
            base_chance = 90
            
        # Weather modifications
        weather_mod = 0
        if gs.weather == "Clear":
            weather_mod = 10
            print(f"{Fore.GREEN}The clear weather provides good sailing conditions.{Style.RESET_ALL}")
        elif gs.weather == "Stormy":
            weather_mod = -30
            print(f"{Fore.RED}Launching during a storm is extremely dangerous!{Style.RESET_ALL}")
        elif gs.weather == "Rainy":
            weather_mod = -10
            print(f"{Fore.BLUE}The rain makes navigation more difficult.{Style.RESET_ALL}")
        elif gs.weather == "Foggy":
            weather_mod = -15
            print(f"{Fore.WHITE}The fog will make it hard to navigate.{Style.RESET_ALL}")
            
        # Ensure final chance is between 5% and 95%
        final_chance = base_chance + weather_mod
        if final_chance < 5:
            final_chance = 5
        elif final_chance > 95:
            final_chance = 95
        
        print(f"\n{Fore.CYAN}You push your {gs.raft_type} into the water and begin rowing away from the island...{Style.RESET_ALL}")
        time.sleep(2)
        
        # Random chance for successful escape
        if random.random() * 100 < final_chance:
            print(f"\n{Fore.GREEN}After many hours of rowing, you spot a passing ship in the distance!{Style.RESET_ALL}")
            time.sleep(1)
            print(f"{Fore.GREEN}They've seen you and are coming to your rescue!{Style.RESET_ALL}")
            time.sleep(1)
            
            gs.rescued = True
            
            # Set ending message based on story path
            if gs.story_path == "survivor":
                gs.message = f"You successfully escaped the island on your {gs.raft_type} and returned to civilization. (Survivor Ending)"
            elif gs.story_path == "explorer" and "ancient_tech_mastered" in gs.story_flags:
                gs.message = "You escaped the island with ancient knowledge that will revolutionize modern technology. (Explorer Ending)"
            elif gs.story_path == "conqueror" and "pirate_king" in gs.story_flags:
                gs.message = "You left the island with pirate treasures and tales of conquest. (Conqueror Ending)"
            else:
                gs.message = f"You successfully escaped the island on your {gs.raft_type}!"
                
            # Complete the escape quest if active
            if "island_escape" in gs.active_quests:
                gs.complete_quest("island_escape")
            
            # Game will end in the next update loop
        else:
            print(f"\n{Fore.RED}After several hours at sea, your raft begins to come apart...{Style.RESET_ALL}")
            time.sleep(1)
            print(f"{Fore.RED}You have no choice but to turn back to the island.{Style.RESET_ALL}")
            time.sleep(1)
            
            # Damage or destroy the raft
            if random.random() < 0.7:  # 70% chance raft is destroyed
                print(f"{Fore.RED}Your {gs.raft_type} is destroyed in the process!{Style.RESET_ALL}")
                gs.raft_type = "None"
            else:
                print(f"{Fore.YELLOW}Your {gs.raft_type} is damaged but still usable.{Style.RESET_ALL}")
                
            # Energy and health cost from failed attempt
            energy_cost = random.randint(40, 60)
            health_cost = random.randint(10, 20)
            
            gs.energy = max(1, gs.energy - energy_cost)
            gs.health = max(1, gs.health - health_cost)
            
            print(f"{Fore.RED}The failed escape attempt has cost you {energy_cost} energy and {health_cost} health.{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def weather_forecast(self) -> None:
        """Display detailed information about current and future weather"""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== WEATHER FORECAST ====={Style.RESET_ALL}")
        
        # Current weather
        weather_color = Fore.WHITE
        if gs.weather == "Clear":
            weather_color = Fore.GREEN
        elif gs.weather == "Rainy":
            weather_color = Fore.BLUE
        elif gs.weather == "Stormy":
            weather_color = Fore.RED
        elif gs.weather == "Foggy":
            weather_color = Fore.WHITE
        elif gs.weather == "Hot":
            weather_color = Fore.YELLOW
            
        print(f"\n{Fore.WHITE}Current weather: {weather_color}{gs.weather}{Style.RESET_ALL}")
        print(f"Weather duration: {gs.weather_duration} more days")
        
        # Weather effects
        print(f"\n{Fore.CYAN}Current Effects:{Style.RESET_ALL}")
        
        if gs.weather == "Clear":
            print(f"{Fore.GREEN}+ Improved exploration success")
            print(f"{Fore.GREEN}+ Better resource gathering")
            print(f"{Fore.GREEN}+ Reduced energy consumption")
            print(f"{Fore.GREEN}+ Improved signaling success")
            print(f"{Fore.GREEN}+ Better fishing and hunting")
        elif gs.weather == "Rainy":
            print(f"{Fore.BLUE}- Reduced visibility during exploration")
            print(f"{Fore.BLUE}- Slightly fewer resources found")
            print(f"{Fore.BLUE}+ Better fishing success")
            print(f"{Fore.BLUE}- Reduced hunting success")
            print(f"{Fore.BLUE}- Lower signaling chance")
        elif gs.weather == "Stormy":
            print(f"{Fore.RED}- Dangerous exploration conditions")
            print(f"{Fore.RED}- Significantly fewer resources found")
            print(f"{Fore.RED}- Higher energy consumption")
            print(f"{Fore.RED}- Much lower fishing and hunting success")
            print(f"{Fore.RED}- Signaling almost impossible")
            print(f"{Fore.RED}- Very dangerous for raft escape")
        elif gs.weather == "Foggy":
            print(f"{Fore.WHITE}- Severely reduced visibility")
            print(f"{Fore.WHITE}- Fewer resources found")
            print(f"{Fore.WHITE}- Reduced hunting success")
            print(f"{Fore.WHITE}- Poor signaling conditions")
            print(f"{Fore.WHITE}- Navigation difficult for raft escape")
        elif gs.weather == "Hot":
            print(f"{Fore.YELLOW}+ Better visibility for exploration")
            print(f"{Fore.YELLOW}+ More resources found")
            print(f"{Fore.YELLOW}- Higher energy consumption")
            print(f"{Fore.YELLOW}+ Active wildlife (better hunting)")
            
        # Weather prediction
        print(f"\n{Fore.CYAN}Weather Prediction:{Style.RESET_ALL}")
        
        # Simple prediction model - just show most likely transitions
        if gs.weather == "Clear":
            print(f"{Fore.YELLOW}Clear weather may continue or turn Hot or Rainy soon")
        elif gs.weather == "Rainy":
            print(f"{Fore.YELLOW}Rain may intensify into a Storm or clear up in coming days")
        elif gs.weather == "Stormy":
            print(f"{Fore.YELLOW}Storm should subside into Rain or Fog within 1-2 days")
        elif gs.weather == "Foggy":
            print(f"{Fore.YELLOW}Fog will likely clear up in the next day or two")
        elif gs.weather == "Hot":
            print(f"{Fore.YELLOW}Hot weather may continue or clouds might bring rain soon")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_detailed_stats(self) -> None:
        """Show detailed player statistics and achievements"""
        gs = self.game_state
        
        print(f"\n{Fore.CYAN}===== DETAILED STATISTICS ====={Style.RESET_ALL}")
        
        # Survival stats
        print(f"\n{Fore.YELLOW}Survival Stats:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Days survived: {gs.days_survived}")
        print(f"{Fore.WHITE}Current health: {gs.health}/100")
        print(f"{Fore.WHITE}Current hunger: {gs.hunger}/100")
        print(f"{Fore.WHITE}Current thirst: {gs.thirst}/100")
        print(f"{Fore.WHITE}Current energy: {gs.energy}/100")
        
        # Exploration stats
        print(f"\n{Fore.YELLOW}Exploration Stats:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current location: {gs.current_location}")
        print(f"{Fore.WHITE}Locations discovered: {len(gs.explored_locations)}/{len(gs.locations)}")
        
        # List all discovered locations
        print(f"\n{Fore.WHITE}Discovered locations:")
        for location in sorted(gs.explored_locations):
            print(f"{Fore.CYAN}- {location}")
            
        # Resource stats
        print(f"\n{Fore.YELLOW}Resources Collected:{Style.RESET_ALL}")
        
        # Group items by type
        resources = ["Wood", "Stone", "Vine", "Leaf", "Fruit", "Berry", "Coconut", "Fresh Water", 
                    "Metal", "Hide", "Feather", "Bamboo", "Ship Parts", "Colorful Feather"]
        
        tools = ["Spear", "Fishing Rod", "Water Container", "Torch", "Signal Mirror", "Map"]
        
        food = ["Small Fish", "Medium Fish", "Large Fish", "Exotic Fish", "Small Game", 
               "Wild Pig Meat", "Venison", "Chicken", "Exotic Bird"]
        
        special = ["Ancient Artifact", "Ship Parts"]
        
        # Display resources
        print(f"\n{Fore.WHITE}Raw Materials:")
        for item in resources:
            if gs.inventory[item] > 0:
                print(f"{Fore.CYAN}- {item}: {gs.inventory[item]}")
                
        # Display tools
        print(f"\n{Fore.WHITE}Tools and Equipment:")
        for item in tools:
            if gs.inventory[item] > 0:
                print(f"{Fore.CYAN}- {item}: {gs.inventory[item]}")
                
        # Display food
        print(f"\n{Fore.WHITE}Food Items:")
        for item in food:
            if gs.inventory[item] > 0:
                print(f"{Fore.CYAN}- {item}: {gs.inventory[item]}")
                
        # Display special items
        print(f"\n{Fore.WHITE}Special Items:")
        for item in special:
            if gs.inventory[item] > 0:
                print(f"{Fore.CYAN}- {item}: {gs.inventory[item]}")
                
        # Raft info
        print(f"\n{Fore.YELLOW}Escape Progress:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current raft: {Fore.CYAN}{gs.raft_type}{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_map(self) -> None:
        """Display the island map with discovered and undiscovered locations"""
        gs = self.game_state
        
        if gs.inventory["Map"] <= 0:
            print(f"\n{Fore.RED}You don't have a map. Craft one to see the island layout.{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}===== ISLAND MAP ====={Style.RESET_ALL}")
        print(Fore.GREEN + self.ascii_island + Style.RESET_ALL)
        print(f"{Fore.WHITE}Discovered locations: {Fore.YELLOW}{len(gs.explored_locations)}/{len(gs.locations) - 1}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Current location: {Fore.CYAN}{gs.current_location}{Style.RESET_ALL}")
        
        # Show connections from current location
        print(f"\n{Fore.WHITE}Connected areas:{Style.RESET_ALL}")
        for destination in gs.island_map.get(gs.current_location, []):
            if destination in gs.explored_locations:
                print(f"- {Fore.GREEN}{destination}{Style.RESET_ALL}")
            elif gs.locations[destination]:  # Known but unexplored
                print(f"- {Fore.YELLOW}{destination}{Style.RESET_ALL}")
            else:
                print(f"- {Fore.RED}??????{Style.RESET_ALL}")
        
        # Show all discovered locations
        print(f"\n{Fore.WHITE}All discovered locations:{Style.RESET_ALL}")
        for location in sorted(gs.locations.keys()):
            if location == "Shelter":
                if gs.has_shelter:
                    status = f"{Fore.GREEN}[Built]"
                else:
                    status = f"{Fore.RED}[Not Built]"
                print(f"- {Fore.CYAN}Shelter{Style.RESET_ALL} {status}")
            elif location in gs.explored_locations:
                print(f"- {Fore.GREEN}{location}{Style.RESET_ALL}")
            elif gs.locations[location]:  # Known but unexplored
                print(f"- {Fore.YELLOW}{location}{Style.RESET_ALL}")
        
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def encounter_enemy(self) -> None:
        """Handle random enemy encounters during exploration"""
        gs = self.game_state
        location = gs.current_location
        
        # No enemies in shelter
        if location == "Shelter":
            return
        
        # 30% chance of enemy encounter
        if random.random() > 0.3:
            return
            
        # Get potential enemies for this location
        possible_enemies = gs.location_enemies.get(location, [])
        if not possible_enemies:
            return
            
        # Select a random enemy
        enemy = random.choice(possible_enemies)
        enemy_strength = random.randint(10, 30)
        
        print(f"\n{Fore.RED}You've encountered a {enemy}! It looks {enemy_strength}% aggressive.{Style.RESET_ALL}")
        
        # Display enemy ASCII art if available
        if enemy in self.ascii_enemies:
            enemy_color = Fore.RED if enemy.startswith("Pirate") else Fore.YELLOW
            print(enemy_color + self.ascii_enemies[enemy] + Style.RESET_ALL)
        
        time.sleep(1)
        
        # Check if player has a weapon
        has_weapon = gs.inventory["Spear"] > 0
        
        if has_weapon:
            print(f"{Fore.YELLOW}You ready your spear to defend yourself.{Style.RESET_ALL}")
            success_chance = 0.7  # 70% chance with weapon
        else:
            print(f"{Fore.YELLOW}You have no weapon to defend yourself!{Style.RESET_ALL}")
            success_chance = 0.3  # 30% chance without weapon
        
        time.sleep(1)
        print(f"{Fore.WHITE}You prepare to fight...{Style.RESET_ALL}")
        time.sleep(1)
        
        # Determine outcome
        if random.random() < success_chance:
            # Victory
            print(f"\n{Fore.GREEN}You successfully fought off the {enemy}!{Style.RESET_ALL}")
            
            # Chance to get meat from animal enemies
            if enemy not in ["Pirate", "Pirate Scout", "Pirate Captain"]:
                meat_gained = random.randint(1, 2)
                gs.inventory["Meat"] += meat_gained
                print(f"{Fore.GREEN}You gained {meat_gained} meat from the {enemy}.{Style.RESET_ALL}")
            else:
                # Pirates might drop special items
                if random.random() < 0.5:
                    special_items = ["Spear", "Water Container", "Torch", "Map"]
                    item = random.choice(special_items)
                    gs.inventory[item] += 1
                    print(f"{Fore.GREEN}You found a {item} on the defeated pirate!{Style.RESET_ALL}")
            
            # Add to defeated enemies list
            if enemy not in gs.defeated_enemies:
                gs.defeated_enemies.append(enemy)
                
            # Update quest objectives for conqueror path
            if "island_ruler" in gs.active_quests and enemy.startswith("Pirate"):
                if "objectives" in gs.active_quests["island_ruler"] and "defeat_challengers" in gs.active_quests["island_ruler"]["objectives"]:
                    gs.update_quest_objective("island_ruler", "defeat_challengers", True)
                    print(f"{Fore.MAGENTA}Quest updated: Island Ruler{Style.RESET_ALL}")
                
            # Update quest objectives for pirate quest
            if "pirate_threat" in gs.active_quests and enemy.startswith("Pirate"):
                # Make sure the quest has the expected structure
                if "objectives" in gs.active_quests["pirate_threat"] and "locate_treasure" in gs.active_quests["pirate_threat"]["objectives"]:
                    if not gs.active_quests["pirate_threat"]["objectives"]["locate_treasure"]:
                        # Small chance to find treasure map when defeating pirates
                        if random.random() < 0.3:
                            print(f"{Fore.YELLOW}The defeated pirate drops a crumpled treasure map!{Style.RESET_ALL}")
                            gs.update_quest_objective("pirate_threat", "find_treasure_map", True)
                            print(f"{Fore.MAGENTA}Quest updated: Pirate Problem{Style.RESET_ALL}")
        else:
            # Defeat
            damage = random.randint(5, 15)
            gs.health -= damage
            print(f"\n{Fore.RED}The {enemy} got the better of you! You lose {damage} health.{Style.RESET_ALL}")
            
            # Chance to lose an item
            if gs.inventory["Spear"] > 0 and random.random() < 0.3:
                gs.inventory["Spear"] -= 1
                print(f"{Fore.RED}Your spear broke during the fight!{Style.RESET_ALL}")
        
        gs.last_enemy_encounter = str(enemy)
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_save_slots(self) -> int:
        """Display available save slots and return the chosen slot"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}===== SAVE GAME ====={Style.RESET_ALL}")
        
        # Show available slots
        for slot in range(1, self.save_slots + 1):
            save_file = self.save_file_template.format(slot)
            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    slot_info = f"Day {save_data['days_survived']}, {save_data['time_of_day']} - {save_data['current_location']}"
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"{Fore.RED}Error loading save: {e}{Style.RESET_ALL}")
                    slot_info = "Corrupted save"
            else:
                slot_info = "Empty slot"
                
            print(f"{Fore.YELLOW}{slot}. {Fore.WHITE}Slot {slot}: {slot_info}")
        
        print(f"{Fore.YELLOW}0. {Fore.WHITE}Back")
        
        # Get player choice
        while True:
            try:
                choice = int(input(f"\n{Fore.GREEN}Choose a slot: {Style.RESET_ALL}"))
                if 0 <= choice <= self.save_slots:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 0 and {self.save_slots}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def save_game(self) -> None:
        # Display save slots
        slot = self.display_save_slots()
        
        # If player chose to go back
        if slot == 0:
            return
            
        # Set the current slot and save file
        self.current_slot = slot
        save_file = self.save_file_template.format(slot)
        
        try:
            # Convert game state to a dictionary
            save_data = {
                "health": self.game_state.health,
                "hunger": self.game_state.hunger,
                "thirst": self.game_state.thirst,
                "energy": self.game_state.energy,
                "days_survived": self.game_state.days_survived,
                "time_of_day": self.game_state.time_of_day,
                "current_location": self.game_state.current_location,
                "explored_locations": self.game_state.explored_locations,
                "has_shelter": self.game_state.has_shelter,
                "has_fire": self.game_state.has_fire,
                "fire_remaining_time": self.game_state.fire_remaining_time,
                "has_raft": self.game_state.has_raft,
                "raft_progress": self.game_state.raft_progress,
                "signal_fire_progress": self.game_state.signal_fire_progress,
                "has_signal_fire": self.game_state.has_signal_fire,
                "inventory": self.game_state.inventory,
                "locations": self.game_state.locations,
                "island_map": self.game_state.island_map,
                "defeated_enemies": self.game_state.defeated_enemies,
                "last_enemy_encounter": self.game_state.last_enemy_encounter
            }
            
            # Save to file
            with open(save_file, 'w') as f:
                json.dump(save_data, f)
                
            print(f"\n{Fore.GREEN}Game saved successfully to Slot {slot}!{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}Error saving game: {e}{Style.RESET_ALL}")
            
        input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
    
    def display_load_slots(self) -> int:
        """Display available save slots for loading and return the chosen slot"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN}===== LOAD GAME ====={Style.RESET_ALL}")
        
        # Check if any save files exist
        has_saves = False
        
        # Show available slots
        for slot in range(1, self.save_slots + 1):
            save_file = self.save_file_template.format(slot)
            if os.path.exists(save_file):
                has_saves = True
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    slot_info = f"Day {save_data['days_survived']}, {save_data['time_of_day']} - {save_data['current_location']}"
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"{Fore.RED}Error loading save: {e}{Style.RESET_ALL}")
                    slot_info = "Corrupted save"
            else:
                slot_info = "Empty slot"
                
            print(f"{Fore.YELLOW}{slot}. {Fore.WHITE}Slot {slot}: {slot_info}")
        
        print(f"{Fore.YELLOW}0. {Fore.WHITE}Back")
        
        # If no saves exist, show message
        if not has_saves:
            print(f"\n{Fore.RED}No saved games found!{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return 0
            
        # Get player choice
        while True:
            try:
                choice = int(input(f"\n{Fore.GREEN}Choose a slot: {Style.RESET_ALL}"))
                if 0 <= choice <= self.save_slots:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 0 and {self.save_slots}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def load_game(self) -> bool:
        # Display load slots
        slot = self.display_load_slots()
        
        # If player chose to go back or no saves exist
        if slot == 0:
            return False
            
        # Set the current slot and load file
        self.current_slot = slot
        save_file = self.save_file_template.format(slot)
        
        try:
            # Check if save file exists
            if not os.path.exists(save_file):
                print(f"\n{Fore.RED}Save file for Slot {slot} does not exist!{Style.RESET_ALL}")
                input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                return False
                
            # Load from file
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                
            # Apply saved data to game state
            gs = self.game_state
            gs.health = save_data["health"]
            gs.hunger = save_data["hunger"]
            gs.thirst = save_data["thirst"]
            gs.energy = save_data["energy"]
            gs.days_survived = save_data["days_survived"]
            gs.time_of_day = save_data["time_of_day"]
            gs.current_location = save_data["current_location"]
            gs.explored_locations = save_data["explored_locations"]
            gs.has_shelter = save_data["has_shelter"]
            gs.has_fire = save_data["has_fire"]
            gs.fire_remaining_time = save_data["fire_remaining_time"]
            gs.has_raft = save_data["has_raft"]
            gs.raft_progress = save_data["raft_progress"]
            gs.signal_fire_progress = save_data["signal_fire_progress"]
            gs.has_signal_fire = save_data["has_signal_fire"]
            gs.inventory = save_data["inventory"]
            gs.locations = save_data["locations"]
            
            # Load new fields if they exist (for compatibility with older saves)
            if "island_map" in save_data:
                gs.island_map = save_data["island_map"]
            if "defeated_enemies" in save_data:
                gs.defeated_enemies = save_data["defeated_enemies"]
            if "last_enemy_encounter" in save_data:
                gs.last_enemy_encounter = save_data["last_enemy_encounter"]
            
            return True
            
        except Exception as e:
            print(f"\n{Fore.RED}Error loading game: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            return False
    
    def check_any_save_exists(self) -> bool:
        """Check if any save files exist"""
        for slot in range(1, self.save_slots + 1):
            save_file = self.save_file_template.format(slot)
            if os.path.exists(save_file):
                return True
        return False
    
    def start_menu(self) -> bool:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + self.ascii_title)
        print(Fore.WHITE + Style.BRIGHT + "A Survival Text Adventure\n")
        
        print(f"{Fore.YELLOW}1. {Fore.WHITE}New Game")
        print(f"{Fore.YELLOW}2. {Fore.WHITE}Load Game")
        print(f"{Fore.YELLOW}0. {Fore.WHITE}Quit")
        
        while True:
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == "1":
                self.display_intro()
                return True
            elif choice == "2":
                # Check if any save file exists
                has_saves = self.check_any_save_exists()
                        
                if not has_saves:
                    print(f"\n{Fore.RED}No saved games found!{Style.RESET_ALL}")
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    return self.start_menu()  # Restart the menu
                elif self.load_game():
                    print(f"\n{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    return True
            elif choice == "0":
                print(f"\n{Fore.YELLOW}Thanks for playing!{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    def game_over_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if self.game_state.rescued:
            print(Fore.GREEN + Style.BRIGHT + self.ascii_victory)
            print(f"{Fore.CYAN}You survived for {self.game_state.days_survived} days on the island!{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}{self.game_state.message}{Style.RESET_ALL}")
            
        else:
            print(Fore.RED + Style.BRIGHT + self.ascii_game_over)
            print(f"{Fore.CYAN}You survived for {self.game_state.days_survived} days on the island before succumbing to the elements.{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}{self.game_state.message}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Thanks for playing Shipwrecked!{Style.RESET_ALL}")
        
        # Remove save file after game over
        save_file = self.save_file_template.format(self.current_slot)
        if os.path.exists(save_file):
            try:
                os.remove(save_file)
            except Exception:
                pass
                
        input(f"\n{Fore.BLUE}Press Enter to exit...{Style.RESET_ALL}")
    
    def run_game(self) -> None:
        # Start menu
        if not self.start_menu():
            return
            
        # Main game loop
        while not self.game_state.game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_stats()
            
            choice = self.display_main_menu()
            
            if choice == "1":
                self.explore_location()
                self.game_state.update_status()
            elif choice == "2":
                self.check_inventory()
            elif choice == "3":
                self.display_crafting_menu()
            elif choice == "4":
                self.eat_drink_menu()
            elif choice == "5":
                self.rest()
            elif choice == "6":
                self.travel_menu()
            elif choice == "7":
                self.save_game()
            elif choice == "9":
                # Load game during play
                if self.load_game():
                    print(f"\n{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "8":
                print(f"\n{Fore.YELLOW}Are you sure you want to quit? (y/n){Style.RESET_ALL}")
                confirm = input().lower()
                if confirm == "y":
                    self.save_game()
                    return
        
        # Game over screen
        self.game_over_screen()

def main() -> None:
    try:
        # Initialize and run game
        game = GameManager()
        game.run_game()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Game interrupted. Thanks for playing!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        
# Launcher verification
def is_launched_from_launcher():
    import inspect
    import os
    
    # Get the call stack
    stack = inspect.stack()
    
    # Check if any calling file is launch.py
    for frame in stack:
        calling_file = os.path.basename(frame.filename)
        if calling_file == "launch.py":
            return True
    
    return False

if __name__ == "__main__":
    # Check if game was launched from the launcher
    if is_launched_from_launcher():
        main()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
