import sys
import random
import json
import os
import time
import math
from typing import List, Dict, Optional, Tuple, Any, Union, Mapping
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Check if called with python3 command
def check_python_command():
    """Check if script was called with 'python3' command and exit if it was"""
    program_name = os.path.basename(sys.executable)
    command = sys.argv[0]
    
    if program_name == "python3" or "python3" in command:
        print(f"{Fore.RED}Please use 'python' command instead of 'python3'")
        print(f"{Fore.YELLOW}Run: python launch.py")
        sys.exit(0)

# Color constants - using colorama named colors for cross-platform compatibility
OKBLUE = Fore.BLUE
OKGREEN = Fore.GREEN
WARNING = Fore.YELLOW
FAIL = Fore.RED
ENDC = Style.RESET_ALL
BOLD = Style.BRIGHT
LIGHTGRAY = Fore.LIGHTWHITE_EX
LIGHTCYAN = Fore.LIGHTCYAN_EX
MAGENTA = Fore.MAGENTA
UNDERLINE = Style.BRIGHT  # Closest alternative in colorama (original was '\033[4m')
SUCCESS = Fore.LIGHTGREEN_EX  # Added for success messages
HEADER = Fore.MAGENTA + Style.BRIGHT  # Header formatting
CYAN = Fore.CYAN  # For cyan text
YELLOW = Fore.YELLOW  # For yellow text
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
WHITE = Fore.WHITE
BLACK = Fore.BLACK
GREY = Fore.BLACK + Style.DIM
DARKGRAY = Fore.BLACK + Style.BRIGHT  # Using bright black for dark gray
PURPLE = Fore.MAGENTA  # Using MAGENTA for purple
LIGHTCYAN = Fore.CYAN + Style.BRIGHT
LIGHTYELLOW = Fore.YELLOW + Style.BRIGHT
LIGHTRED = Fore.RED + Style.BRIGHT
LIGHTGREEN = Fore.GREEN + Style.BRIGHT
LIGHTBLUE = Fore.BLUE + Style.BRIGHT
LIGHTMAGENTA = Fore.MAGENTA + Style.BRIGHT
BG_BLACK = Back.BLACK
BG_RED = Back.RED
BG_GREEN = Back.GREEN
BG_YELLOW = Back.YELLOW
BG_BLUE = Back.BLUE
BG_MAGENTA = Back.MAGENTA
BG_CYAN = Back.CYAN
BG_WHITE = Back.WHITE
BG_GREY = Back.BLACK + Style.DIM
BG_LIGHTRED = Back.RED + Style.BRIGHT
BG_LIGHTGREEN = Back.GREEN + Style.BRIGHT
BG_LIGHTYELLOW = Back.YELLOW + Style.BRIGHT
BG_LIGHTBLUE = Back.BLUE + Style.BRIGHT
BG_LIGHTMAGENTA = Back.MAGENTA + Style.BRIGHT
BG_LIGHTCYAN = Back.CYAN + Style.BRIGHT
BG_BRIGHTWHITE = Back.WHITE + Style.BRIGHT

# Special effects (some not available in colorama but included for compatibility)
DIM = Style.DIM  # Dim/faint text
ITALIC = ""  # Not available in colorama
REVERSE = Style.RESET_ALL  # Not directly available
BLINK = ""  # Not available in colorama 
HIDDEN = ""  # Not available in colorama
STRIKETHROUGH = ""  # Not available in colorama

# Constants
INITIAL_GOLD = 100
INITIAL_HEALTH = 100
EXP_TO_LEVEL = 100
CRITICAL_CHANCE = 0.15
DODGE_CHANCE = 0.1
TICKS_PER_DAY = 50
# Only action commands take time (ticks)
TICK_COMMANDS = {
    '/gather': (3, 5),
    '/farm': (2, 4),
    '/fight': (4, 8), 
    '/craft': (3, 6),
    '/dungeon': (8, 15),
    '/travel': (5, 10),
    '/search': (2, 4),
    '/find_key': (3, 6)
}

# Commands that don't take time
NO_TICK_COMMANDS = {'/help', '/stats', '/h', '/s_t', '/inventory', '/i', '/materials', 
                   '/m', '/quests', '/q', '/save', '/load', '/prefix', '/settings',
                   '/bestiary', '/weapon_info', '/location', '/location_check',
                   '/professions', '/dungeon_list', '/mobs', '/tip', '/codes',
                   '/support', '/exit', '/x', '/dimensions', '/dim', '/camp',
                   '/camp_build', '/camp_repair', '/camp_use', '/camp_demolish', '/camp_info',
                   '/return_home', '/weather', '/season'}

# Game time tracking
# Weather system
WEATHERS = {
    "clear": {
        "name": "Clear",
        "description": "Clear skies and pleasant temperatures.",
        "crop_growth_modifier": 1.0,
        "color": BLUE,
        "rarity": 0.30
    },
    "sunny": {
        "name": "Sunny",
        "description": "Bright sunshine warms the land.",
        "crop_growth_modifier": 1.2,  # Crops grow faster in sun
        "color": OKGREEN,
        "rarity": 0.20
    },
    "cloudy": {
        "name": "Cloudy",
        "description": "Gray clouds hang overhead, blocking the sun.",
        "crop_growth_modifier": 0.9,  # Slight slowdown
        "color": LIGHTGRAY, 
        "rarity": 0.15
    },
    "rainy": {
        "name": "Rainy",
        "description": "Rain falls steadily from the sky.",
        "crop_growth_modifier": 1.5,  # Rain helps most crops
        "color": CYAN,
        "rarity": 0.15
    },
    "stormy": {
        "name": "Stormy",
        "description": "Lightning flashes as a storm rages.",
        "crop_growth_modifier": 0.7,  # Storms damage some crops
        "color": PURPLE,
        "rarity": 0.07
    },
    "windy": {
        "name": "Windy",
        "description": "Strong winds blow across the land.",
        "crop_growth_modifier": 0.8,  # Wind can damage delicate crops
        "color": YELLOW,
        "rarity": 0.08
    },
    "foggy": {
        "name": "Foggy",
        "description": "A thick fog obscures visibility.",
        "crop_growth_modifier": 0.9,  # Slight slowdown
        "color": WHITE,
        "rarity": 0.05
    }
}

# Special weathers for dimensions
DIMENSION_WEATHERS = {
    "Celestial Realm": [
        {"name": "Cosmic Rain", "description": "Glowing stardust falls from the heavens.", "crop_growth_modifier": 2.0, "color": PURPLE},
        {"name": "Celestial Harmony", "description": "The stars align in perfect harmony.", "crop_growth_modifier": 1.8, "color": CYAN}
    ],
    "Shadow Realm": [
        {"name": "Darkness Storm", "description": "Swirling shadows block all light.", "crop_growth_modifier": 0.4, "color": DARKGRAY},
        {"name": "Void Mist", "description": "A mist that seems to absorb all life energy.", "crop_growth_modifier": 0.5, "color": PURPLE}
    ],
    "Elemental Plane": [
        {"name": "Elemental Surge", "description": "Raw elemental energies fill the air.", "crop_growth_modifier": 1.7, "color": RED},
        {"name": "Primal Storm", "description": "A chaotic storm of all elements.", "crop_growth_modifier": 0.6, "color": YELLOW}
    ],
    "Ancient Ruins": [
        {"name": "Time Flux", "description": "Reality shifts as time flows erratically.", "crop_growth_modifier": 1.3, "color": BLUE},
        {"name": "Arcane Winds", "description": "Magical winds carry remnants of ancient spells.", "crop_growth_modifier": 1.4, "color": MAGENTA}
    ]
}

game_state = {
    "current_tick": 0,
    "current_day": 0,
    "last_command_tick": 0,
    "current_weather": "clear",
    "weather_duration": 5,  # Weather changes every 5 game days by default
    "last_weather_change": 0
}

# NPCs and their dialogues
NPCS = {
    "Old Sage": {
        "location": "Greenwood Village",
        "dialogues": {
            "greeting": "Welcome, young adventurer. The world needs heroes now more than ever.",
            "quest": "Dark forces gather in the east. Will you help us?",
            "story": {
                "intro": "Long ago, our lands were peaceful...",
                "chapter1": "But then the Legion Of Darkness, once sealed underground, came back...",
                "chapter2": "Now we need a hero to unite everyone against the Legion Of Darkness like how the legendary heroes did to seal it..."
            },
            "additional": [
                "Legends speak of an ancient power hidden deep within the mountains.",
                "Remember, courage and wisdom will guide you through the darkest times."
            ]
        },
        "quests": ["Dragon Hunter", "Skeleton Cleanup"]
    },
    "Blacksmith": {
        "location": "Stormhaven",
        "dialogues": {
            "greeting": "Need weapons? I've got the finest steel in all the realms.",
            "quest": "If you bring me some iron ore, I can forge you special weapons.",
            "trade": "Take a look at my wares."
        },
        "quests": ["Iron Gatherer"],
        "shop": ["Iron Sword", "Steel Sword", "Iron Armor"]
    },
    "Mysterious Stranger": {
        "location": "Shadowmere",
        "dialogues": {
            "greeting": "Psst... seeking rare artifacts?",
            "quest": "The shadows hold many secrets... and treasures.",
            "warning": "Beware the Crimson Abyss... death awaits the unprepared.",
            "additional": [
                "There are secrets buried beneath the ruins, waiting to be uncovered.",
                "Trust no one, for the enemy may be closer than you think."
            ]
        },
        "quests": ["Shadow Walker"]
    },
    "Village Elder": {
        "location": "Greenwood Village",
        "dialogues": {
            "greeting": "Greetings, traveler. Our village has seen better days.",
            "quest": "We need help gathering herbs to heal the sick.",
            "story": "The forest holds many secrets, some better left undisturbed."
        },
        "quests": ["Herbal Remedy"]
    },
    "Merchant": {
        "location": "Stormhaven",
        "dialogues": {
            "greeting": "Looking for rare goods? You've come to the right place.",
            "trade": "I have wares from distant lands, take a look."
        },
        "shop": ["Exotic Spices", "Rare Gems", "Magic Potions"]
    },
    # New NPCs for Weather Mysteries questline
    "Weather Sage": {
        "location": "Mountain Peaks",
        "dialogues": {
            "greeting": "The winds speak to those who listen. I hear you've come seeking knowledge.",
            "quest": "The weather patterns have been disturbed lately. Something unnatural is at work.",
            "story": {
                "intro": "For generations, my family has studied the weather and its connection to the world's magic.",
                "chapter1": "Recently, the patterns have become erratic. I fear a malevolent force is manipulating nature itself.",
                "chapter2": "If we collect samples from different weather conditions, I might be able to trace the source of this disturbance."
            },
            "weather_lore": "Each type of weather carries its own magic. Thunderstorms hold the power of transformation, while snow preserves ancient energies."
        },
        "quests": ["The Weather Sage", "Collecting Weather Samples", "The Weather Anomaly", "Confronting the Storm Entity"]
    },
    "Storm Entity": {
        "location": "Ancient Forest",
        "dialogues": {
            "greeting": "You dare interrupt my work? The weather bends to MY will now!",
            "battle": "Your pathetic resistance ends here. The elements answer to me alone!",
            "defeat": "Impossible... how could a mere mortal harness such power? Perhaps... I was wrong..."
        },
        "monster": True,
        "boss": True,
        "element": "Storm",
        "quests": ["Confronting the Storm Entity"]
    },
    # New NPCs for Void Walker questline
    "Dimensional Scholar": {
        "location": "Grand Library",
        "dialogues": {
            "greeting": "Ah, an adventurer! Have you noticed the strange rifts appearing throughout the land?",
            "quest": "I've been documenting these dimensional anomalies. Would you help me collect data?",
            "story": {
                "intro": "The boundaries between dimensions have always been thin in certain places.",
                "chapter1": "But lately, something or someone has been purposely tearing holes between worlds.",
                "chapter2": "These aren't natural occurrences - they're deliberate incursions. We must find who's responsible."
            }
        },
        "quests": ["Strange Disturbances", "The Void Walker's Trail"]
    },
    "Dimension Guardian": {
        "location": "Dimensional Nexus",
        "dialogues": {
            "greeting": "HALT! None may pass beyond this point without proving their worth.",
            "battle": "The spaces between worlds are not meant for mortal travel. Turn back or face judgment!",
            "defeat": "You possess... unusual strength for one of your kind. Perhaps you are... the one prophesied."
        },
        "monster": True,
        "element": "Void",
        "quests": ["Dimensional Guardians"]
    },
    "Void Walker": {
        "location": "Dimensional Nexus Core",
        "dialogues": {
            "greeting": "So, you've found me at last. Few have the determination to follow my path.",
            "reveal": "I am not your enemy. I am trying to seal the dimensional wounds before HE returns.",
            "story": {
                "intro": "I was once a guardian like those you've defeated.",
                "chapter1": "But I discovered a terrible threat - an entity that consumes entire dimensions.",
                "chapter2": "It was sealed away millennia ago, but the seal weakens. I've been strengthening the barriers.",
                "chapter3": "Now that you know the truth, will you help me complete my work? Or will you stand against me?"
            }
        },
        "quests": ["The Void Walker's Identity"],
        "choices": {
            "ally": "I understand now. I'll help you protect the dimensions.",
            "oppose": "How can I trust you? Your methods have caused chaos across the realms."
        },
        "outcomes": {
            "ally": {"item": "Void Walker's Staff", "dimension_key": "Void Plane"},
            "oppose": {"item": "Dimensional Seal Fragment", "dimension_key": "Guardian Realm"}
        }
    },
    "Wandering Bard": {
        "location": "Dragon's Peak",
        "dialogues": {
            "greeting": "Songs of heroes and legends, care to listen?",
            "story": "They say the mountains echo with the voices of ancient dragons.",
            "quest": "Help me collect tales from the nearby villages."
        },
        "quests": ["Tales of the Mountain"]
    },
    "Resistant Underground Leader": {
        "location": "Iron Caliphate of Al-Khilafah Al-Hadidiyah",
        "dialogues": {
            "greeting": "We must act carefully. The Caliphate's spies are everywhere."
        },
        "quests": ["Sabotage Supply Lines", "Rescue Imprisoned Dissidents"],
        "reward": "Rare blueprints for crafting resistance gear"
    },
    "Sympathetic Guard": {
        "location": "Iron Caliphate of Al-Khilafah Al-Hadidiyah",
        "dialogues": {
            "greeting": "The lockdown... it wasn't always like this. Something changed the Caliph."
        },
        "quests": ["Infiltrate the Palace", "Recover Stolen Artifacts"],
        "reward": "Access to guarded areas, special weapons"
    },
    "Black Market Supplier": {
        "location": "Iron Caliphate of Al-Khilafah Al-Hadidiyah",
        "dialogues": {
            "greeting": "Need food? Medical supplies? The price is high, but so are the risks."
        },
        "shop": ["Rare food items", "Medicinal herbs", "Lock-picking tools"],
        "quests": ["Distract the Patrols", "Smuggle Supplies"]
    },
    "Ronin Mercenary": {
        "location": "Shogunate of Shirui",
        "dialogues": {
            "greeting": "Honor is a luxury I can no longer afford."
        },
        "quests": ["Assassinate a Corrupt Official", "Protect a Whistleblower"],
        "reward": "Unique samurai weapons, ronin armor"
    },
    "Imperial Spy": {
        "location": "Shogunate of Shirui",
        "dialogues": {
            "greeting": "The Shogun knows everything... or so he believes."
        },
        "quests": ["Infiltrate the Dojo", "Decode Intercepted Messages"],
        "reward": "Spy tools, intelligence network access"
    },
    "Shadow Broker": {
        "location": "Shadowmere",
        "dialogues": {
            "greeting": "Information costs more than gold here."
        },
        "quests": ["Retrieve Stolen Secrets", "Eliminate a Rival"],
        "reward": "Rare magic items, forbidden scrolls"
    },
    "Fallen Noble": {
        "location": "Shadowmere",
        "dialogues": {
            "greeting": "The darkness consumes everyone eventually."
        },
        "quests": ["Reclaim Family Heirlooms", "Exposing Corruption"],
        "reward": "Ancient family weapons, noble artifacts"
    },
    "Exiled Mage": {
        "location": "Frostvale",
        "dialogues": {
            "greeting": "Cold preserves... and destroys."
        },
        "quests": ["Contain the Ice Wraith", "Retrieve Magical Research"],
        "reward": "Ice-elemental weapons, frost-resistant gear"
    },
    "Survival Guide": {
        "location": "Frostvale",
        "dialogues": {
            "greeting": "In Frostvale, respect the elements or perish."
        },
        "quests": ["Hunt Polar Creatures", "Establish a Safe House"],
        "reward": "Survival kits, cold-weather armor"
    },
    "Dragon Egg Collector": {
        "location": "Dragon's Peak",
        "dialogues": {
            "greeting": "A dragon's power begins with its egg."
        },
        "quests": ["Retrieve a Specific Egg", "Protect a Nest"],
        "reward": "Dragon egg fragments (crafting materials), rare mounts"
    },
    "Mountain Guide": {
        "location": "Dragon's Peak",
        "dialogues": {
            "greeting": "Without a guide, the mountains will bury you."
        },
        "quests": ["Map New Routes", "Rescue Lost Climbers"],
        "reward": "Mountaineering gear, map fragments"
    },
    "Dragon Lore Scholar": {
        "location": "Long Shui Zhen",
        "dialogues": {
            "greeting": "Dragons are not just beasts—they are history."
        },
        "quests": ["Decode Ancient Dragon Texts", "Find a Legendary Dragon"],
        "reward": "Knowledge-based items, dragon lore books"
    },
    "Martial Arts Rival": {
        "location": "Long Shui Zhen",
        "dialogues": {
            "greeting": "Your form is weak. Let me correct you."
        },
        "quests": ["Win the Tournament", "Retrieve Training Weapons"],
        "reward": "Unique martial arts weapons, prestige items"
    },
    "Deserted Researcher": {
        "location": "Crimson Abyss",
        "dialogues": {
            "greeting": "What we unleashed... I fear it's too late to stop."
        },
        "quests": ["Contain the Corruption", "Destroy Experimental Devices"],
        "reward": "Resistance gear, purified abyssal materials"
    },
    "Corrupted Survivor": {
        "location": "Crimson Abyss",
        "dialogues": {
            "greeting": "The Abyss... it whispers. It promises power."
        },
        "quests": ["Find the Cure", "Destroy the Corruption Source"],
        "reward": "Anti-corruption items, purification rituals"
    },
    "Village Historian": {
        "location": "Greenwood Village",
        "dialogues": {
            "greeting": "The forest holds many secrets older than the village itself."
        },
        "quests": ["Research Ancient Trees", "Translate Old Scrolls"],
        "reward": "Historical artifacts, knowledge points"
    },
    "Local Farmer": {
        "location": "Greenwood Village",
        "dialogues": {
            "greeting": "The soil here is rich, but it requires respect."
        },
        "quests": ["Harvest Rare Crops", "Scare Off Pests"],
        "reward": "Farming tools, rare seeds"
    },
    "Fisherman": {
        "location": "Stormhaven",
        "dialogues": {
            "greeting": "The sea gives generously to those who understand her."
        },
        "quests": ["Catch Legendary Fish", "Repair the Harbor"],
        "reward": "Fishing gear, rare fish"
    },
    "Shipwright": {
        "location": "Stormhaven",
        "dialogues": {
            "greeting": "A good ship is built with patience, not haste."
        },
        "quests": ["Find Ship Materials", "Solve Shipyard Sabotage"],
        "reward": "Boat blueprints, navigation tools"
    },
    "Dragon Tamer": {
        "location": "Dragon's Reach",
        "dialogues": {
            "greeting": "Dragons respect strength, but they follow wisdom."
        },
        "quests": ["Tame a Specific Dragon", "Retrieve Dragon Eggs", "Dragon Tamer Initiate"],
        "reward": "Dragon companions, taming gear"
    },
    "Mercenary Captain": {
        "location": "Dragon's Reach",
        "dialogues": {
            "greeting": "The mountains are dangerous, but the pay is good."
        },
        "quests": ["Escort the Convoy", "Eliminate Bandit Camps"],
        "reward": "Mercenary gear, gold"
    },
    "Garden Master": {
        "location": "Jade Lotus Village",
        "dialogues": {
            "greeting": "A garden reflects the grower's soul."
        },
        "quests": ["Cultivate Rare Herbs", "Design a Zen Garden"],
        "reward": "Special seeds, gardening tools"
    },
    "Tea House Owner": {
        "location": "Jade Lotus Village",
        "dialogues": {
            "greeting": "A good cup of tea can change your day."
        },
        "shop": ["Temporary stat-boosting teas"],
        "quests": ["Collect Rare Tea Leaves", "Host a Tea Ceremony"],
        "reward": "Special tea blends, social reputation"
    },
    "Lava Prospector": {
        "location": "Ember Hollow",
        "dialogues": {
            "greeting": "The earth gives treasure to those who endure its heat."
        },
        "quests": ["Extract Magma Crystals", "Repair the Cooling System"],
        "reward": "Volcanic gear, rare minerals"
    },
    "Fire Mage": {
        "location": "Ember Hollow",
        "dialogues": {
            "greeting": "Fire is both creator and destroyer."
        },
        "quests": ["Contain Lava Elemental", "Retrieve Ancient Tome"],
        "reward": "Fire-elemental weapons, spellbooks"
    },
    "Lunar Cultist": {
        "location": "Moonveil Harbor",
        "dialogues": {
            "greeting": "The moon guides us through the darkest nights."
        },
        "quests": ["Harvest Moonlit Herbs", "Restore the Lunar Altar"],
        "reward": "Moon-based magic items, night vision gear"
    },
    "Sea Captain": {
        "location": "Moonveil Harbor",
        "dialogues": {
            "greeting": "The sea is a harsh mistress, but rewarding."
        },
        "quests": ["Escort the Trade Ship", "Map New Trade Routes"],
        "reward": "Nautical gear, rare trade goods"
    },
    "Swamp Hermit": {
        "location": "Blightmoor",
        "dialogues": {
            "greeting": "The swamp gives and takes in equal measure."
        },
        "quests": ["Develop an Antidote", "Destroy the Toxic Source"],
        "reward": "Antidote recipes, poison-resistant gear"
    },
    "Mutated Creature Tamer": {
        "location": "Blightmoor",
        "dialogues": {
            "greeting": "Even mutation has its uses."
        },
        "quests": ["Capture a Mutated Beast", "Retrieve Experimental Data"],
        "reward": "Mutated pet companions, toxic weapons"
    },
    "Elven Archdruid": {
        "location": "Verdant Spire",
        "dialogues": {
            "greeting": "Nature's balance must be preserved at all costs."
        },
        "quests": ["Purge the Corruption", "Retrieve the Druidic Staff"],
        "reward": "Nature magic items, elven armor"
    },
    "Sky Gardener": {
        "location": "Verdant Spire",
        "dialogues": {
            "greeting": "The sky holds plants that ground dwellers can't imagine."
        },
        "quests": ["Pollinate Rare Flowers", "Save the Floating Garden"],
        "reward": "Flying mounts, cloudwalking boots"
    },
    "Frost Witch": {
        "location": "Silverpine",
        "dialogues": {
            "greeting": "Winter tests us, but also blesses us."
        },
        "quests": ["Summon a Snow Spirit", "Protect the Winter Festival"],
        "reward": "Frost magic items, winter-themed gear"
    },
    "Yeti Guide": {
        "location": "Silverpine",
        "dialogues": {
            "greeting": "The mountains are my home. Let me show you their ways."
        },
        "quests": ["Escort Through the Pass", "Retrieve Stolen Idol"],
        "reward": "Yeti companions, cold-resistant gear"
    },
    "Imperial Inquisitor": {
        "location": "Tlācahcāyōtl Tletl Tecpanēcatl",
        "dialogues": {
            "greeting": "Heretics will burn for the purification of the realm."
        },
        "quests": ["Expose the Heretic Cell", "Retrieve the Sacred Flame"],
        "reward": "Inquisitor gear, fire magic items"
    },
    "Rebel Healer": {
        "location": "Tlācahcāyōtl Tletl Tecpanēcatl",
        "dialogues": {
            "greeting": "We heal the wounds the Empire inflicts."
        },
        "quests": ["Gather Medicine", "Save Imprisoned Dissidents"],
        "reward": "Healing potions, medical supplies"
    },
    "Wandering Spirit": {
        "location": "Cursed Katana",
        "dialogues": {
            "greeting": "This blade... it consumes souls."
        },
        "quests": ["Purify the Katana", "Find the Spirit's Rest"],
        "reward": "Purified weapon, spirit companion"
    },
}

# Main storyline chapters
STORYLINE = {
    "Chapter 1: The Awakening": {
        "title": "The Awakening",
        "description": "As darkness spreads across the land, a hero rises to face the looming threat. The fate of the realm hangs in the balance.",
        "required_level": 1,
        "quest_line": ["The Beginning", "First Steps", "The Dark Warning"],
        "reward": {"gold": 200, "exp": 300, "item": "Novice Ring"}
    },
    "Chapter 2: The Dragon's Call": {
        "title": "The Dragon's Call",
        "description": "Ancient dragons stir from their slumber, their power echoing through the mountains. The hero must prove their worth to tame these mighty beasts.",
        "required_level": 5,
        "quest_line": ["Dragon's Peak Journey", "Dragon Trials", "The First Flight"],
        "reward": {"gold": 500, "exp": 700, "item": "Dragon Scale Armor"}
    },
    "Chapter 3: The Gathering Storm": {
        "title": "The Gathering Storm",
        "description": "Dark forces gather in the distant lands, forming alliances that threaten the peace of all realms. You must unite the fractured kingdoms before it's too late.",
        "required_level": 10,
        "quest_line": ["Alliance of Kingdoms", "The Council Meeting", "The Diplomat's Journey"],
        "reward": {"gold": 800, "exp": 1200, "item": "Diplomat's Signet"}
    },
    "Chapter 4: The Shadow Legion": {
        "title": "The Shadow Legion",
        "description": "A mysterious legion of shadow warriors has emerged from the forbidden lands. Their dark magic corrupts everything they touch.",
        "required_level": 15,
        "quest_line": ["Scouts of Darkness", "The Corrupted Forest", "The Shadow General"],
        "reward": {"gold": 1200, "exp": 1800, "item": "Shadowbane Amulet"}
    },
    "Chapter 5: The Ancient Ones": {
        "title": "The Ancient Ones",
        "description": "Beings of immense power, forgotten by time, have awakened. Their return heralds an era of chaos unless their motives can be understood.",
        "required_level": 20,
        "quest_line": ["Whispers of the Past", "The Forbidden Library", "The Gateway"],
        "reward": {"gold": 1500, "exp": 2500, "item": "Tome of the Ancients"}
    },
    "Chapter 6: The Final Confrontation": {
        "title": "The Final Confrontation",
        "description": "All paths have led to this moment. The fate of the world rests on your final battle against the ultimate darkness.",
        "required_level": 25,
        "quest_line": ["The Path Opens", "Allies United", "Darkness Falls"],
        "reward": {"gold": 2000, "exp": 3000, "item": "Hero's Legacy"}
    },
    # Post-game storylines
    "Epilogue: The New Beginning": {
        "title": "The New Beginning",
        "description": "Though the great darkness has been defeated, new challenges arise in a world forever changed by your actions.",
        "required_level": 30,
        "post_game": True,
        "quest_line": ["Rebuilding the Realms", "New Threats Emerge", "The Hero's Journey Continues"],
        "reward": {"gold": 3000, "exp": 4000, "item": "Crown of New Dawn"}
    },
    "Dimensional Rifts": {
        "title": "Dimensional Rifts",
        "description": "Strange portals have appeared throughout the land, leading to alternate realities and timelines. What dangers—and opportunities—might they hold?",
        "required_level": 35,
        "post_game": True,
        "quest_line": ["The First Portal", "Mirror Worlds", "The Time Paradox"],
        "reward": {"gold": 3500, "exp": 4500, "item": "Dimensional Compass"}
    },
    "Legacy of the Gods": {
        "title": "Legacy of the Gods",
        "description": "Ancient deities have taken notice of your heroic deeds. Now they challenge you to trials that will test the limits of your abilities.",
        "required_level": 40,
        "post_game": True,
        "quest_line": ["Divine Challenge", "The Celestial Forge", "Ascension"],
        "reward": {"gold": 4000, "exp": 5000, "item": "Godforged Artifact"}
    },
    "Chapter 3: Shadows of the Past": {
        "title": "Shadows of the Past",
        "description": "Dark secrets emerge from the shadows of Shadowmere, threatening to unravel the peace. The hero must confront the darkness within.",
        "required_level": 10,
        "quest_line": ["The Shadow's Call", "Ancient Secrets", "The Final Shadow"],
        "reward": {"gold": 1000, "exp": 1500, "item": "Shadow Blade"}
    },
    "Chapter 4: The Dark Sun's Rise": {
        "title": "The Dark Sun's Rise",
        "description": "The Dark Sun Order, the Empire's ruthless secret police, is expanding its power. You must uncover their plans before it's too late.",
        "required_level": 15,
        "quest_line": ["Shadow Infiltration", "The Informant", "Dark Sun Archives"],
        "reward": {"gold": 1500, "exp": 2000, "item": "Shadow Cloak"}
    },
    "Chapter 5: Imperial Machinations": {
        "title": "Imperial Machinations",
        "description": "The Empire of Eternal Flame strengthens its grip on the lands while the Dark Sun Order enforces their will. You discover a resistance movement.",
        "required_level": 20,
        "quest_line": ["Resistance Contact", "Imperial Fortress", "Escape from the Capital"],
        "reward": {"gold": 2000, "exp": 2500, "item": "Resistance Insignia"}
    },
    "Chapter 6: Revolution's Dawn": {
        "title": "Revolution's Dawn",
        "description": "The time has come to strike against the Empire and the Dark Sun Order. You must unite the rebel factions and lead the final assault.",
        "required_level": 25,
        "quest_line": ["Uniting the Factions", "Battle for Freedom", "Emperor's Downfall"],
        "reward": {"gold": 2500, "exp": 3000, "item": "Freedom's Banner"}
    },
    "Chapter 7: The Crimson Abyss": {
        "title": "The Crimson Abyss",
        "description": "A dark and foreboding realm where ancient evils stir. The hero's journey continues beyond this point...",
        "required_level": 30,
        "quest_line": ["Crimson Abyss Awakening", "Demon's Heart", "Abyssal Leviathan"],
        "reward": {"gold": 3000, "exp": 3500, "item": "Demon's Heart"}
    }
}

# Weapon types and their properties
WEAPONS = {
    "Wooden Sword": {"damage": 5, "speed": 1.0, "price": 30},
    "Bone Sword": {"damage": 7, "speed": 1.0, "price": 50},
    "Iron Sword": {"damage": 10, "speed": 1.0, "price": 80},
    "Steel Sword": {"damage": 15, "speed": 0.9, "price": 150},
    "Flame Sword": {"damage": 20, "speed": 1.1, "price": 300, "effect": "burn"},
    "Ice Sword": {"damage": 18, "speed": 0.8, "price": 300, "effect": "freeze"},
    "Magic Staff": {"damage": 12, "speed": 1.2, "price": 200, "effect": "magic"},
    "Battle Axe": {"damage": 25, "speed": 0.7, "price": 250},
    "Longbow": {"damage": 20, "speed": 1.5, "price": 180},
    "Shortbow": {"damage": 18, "speed": 1.3, "price": 150},
    "Dagger": {"damage": 8, "speed": 1.5, "price": 100},
    "Spear": {"damage": 12, "speed": 1.2, "price": 120},
    "Crossbow": {"damage": 15, "speed": 0.6, "price": 200},
    "Katana": {"damage": 22, "speed": 1.0, "price": 350},
    "Elder Wand": {"damage": 30, "speed": 1.0, "price": 500, "effect": "ultimate"},
    "Assassin's Dagger": {"damage": 14, "speed": 1.7, "price": 220},
    "Miner's Pickaxe": {"damage": 18, "speed": 0.8, "price": 180},
    "Storm Staff": {"damage": 20, "speed": 1.0, "price": 300, "effect": "storm"},
    "Cursed Katana": {"damage": 40, "speed": 0.9, "price": 1500, "effect": "self_damage"},
    "Ninja Star": {"damage": 16, "speed": 1.8, "price": 250},
    "Cutlass": {"damage": 20, "speed": 1.1, "price": 300},
    "Shadow Blade": {"damage": 32, "speed": 1.2, "price": 950, "effect": "critical_hit"},
    "Dragonfire Sword": {"damage": 35, "speed": 1.0, "price": 1200, "effect": "fire_damage"},
    "Lightning Sword": {"damage": 30, "speed": 1.1, "price": 1100, "effect": "lightning_damage"},
    "Wind Sword": {"damage": 28, "speed": 1.3, "price": 1000, "effect": "wind_damage"},
    "Earth Sword": {"damage": 27, "speed": 1.0, "price": 950, "effect": "earth_damage"},
    "Nature Sword": {"damage": 25, "speed": 1.2, "price": 900, "effect": "nature_damage"},
    "Jade Sword": {"damage": 24, "speed": 1.1, "price": 850},
    "Shogun's Blade": {"damage": 38, "speed": 1.0, "price": 1400},
    "Crimson Cutlass": {"damage": 28, "speed": 1.0, "price": 750, "effect": "bleed"},
    "Thunder Staff": {"damage": 30, "speed": 1.0, "price": 1000, "effect": "thunder_damage"},
    "Obsidian Blade": {"damage": 100, "speed": 0.5, "price": 1000000}
}

# Towns and locations
LOCATIONS= {
    "Greenwood Village": {
        "type": "town",
        "shops": ["Blacksmith", "General Store", "Magic Shop"],
        "monsters": ["Goblin", "Wolf"],
        "description": "A peaceful village surrounded by dense forest"
    },
    "Stormhaven": {
        "type": "town",
        "shops": ["Weaponsmith", "Armory", "Alchemist"],
        "monsters": ["Skeleton", "Ghost"],
        "description": "A coastal town known for its skilled craftsmen"
    },
    "Dragon's Peak": {
        "type": "dangerous",
        "monsters": ["Fire Dragon", "Ice Dragon"],
        "description": "A treacherous mountain where dragons dwell"
    },
    "Crystal Cave": {
        "type": "dungeon",
        "monsters": ["Crystal Golem", "Cave Troll"],
        "description": "A cave system filled with valuable crystals"
    },
    "Shadowmere": {
        "type": "town",
        "shops": ["Dark Market", "Mystic Shop"],
        "monsters": ["Shadow Beast", "Dark Knight"],
        "description": "A mysterious town shrouded in darkness and secrets."
    },
    "Sunken Depths": {
        "type": "dungeon",
        "monsters": ["Abyssal Serpent", "Sunken Ghost", "Coral Golem"],
        "description": "Sunken cities and forgotten structures beneath the ocean, filled with ancient artifacts and dangers."
    },
    "Blightmoor": {
        "type": "dangerous",
        "monsters": ["Blight Beast", "Toxic Sludge", "Mutated Scorpion"],
        "description": "A dark and twisted environment where the very soil is tainted, giving rise to dangerous, mutated creatures and toxic flora."
    },
    "Silverpine": {
        "type": "town",
        "shops": ["Silver Smith", "Herbalist", "Hunter's Lodge"],
        "monsters": ["Silver Wolf", "Forest Spirit"],
        "description": "A cold and dense forest filled with evergreens and snow, inhabited by resilient wildlife adapted to the harsh conditions."
    },
    "Frostvale": {
        "type": "town",
        "shops": ["Ice Forge", "Potion Shop"],
        "monsters": ["Ice Troll", "Frost Giant"],
        "description": "A snowy town known for its ice magic"
    },
    "Long Shui Zhen (Dragonwater Town)": {
        "type": "city",
        "shops": ["Dragon Market", "Dragon Temple"],
        "monsters": ["Dragon Knight", "Water Elemental"],
        "description": "A bustling city with a rich history of dragon taming and martial arts"
    },
    "Jade Lotus Village": {
        "type": "town",
        "shops": ["Herbalist", "Tea House", "Charm Shop"],
        "monsters": ["Lotus Spirit", "Pond Serpent"],
        "description": "A tranquil village known for its serene gardens and sacred lotus ponds"
    },
    "Thundercliff Hold": {
        "type": "dangerous",
        "monsters": ["Storm Elemental", "Rock Wyvern"],
        "description": "A high cliff fortress battered by storms and haunted by sky beasts"
    },
    "Ember Hollow": {
        "type": "dungeon",
        "monsters": ["Lava Hound", "Molten Wraith"],
        "description": "A volcanic cavern where fire magic pulses through the earth"
    },
    "Moonveil Harbor": {
        "type": "town",
        "shops": ["Navigator's Guild", "Seafood Market", "Lunar Shrine"],
        "monsters": ["Moonshade Specter", "Sea Serpent"],
        "description": "A mystical harbor town bathed in moonlight and tied to ancient sea legends"
    },
    "Verdant Spire": {
        "type": "city",
        "shops": ["Elven Boutique", "Sky Garden", "Mystic Archives"],
        "monsters": ["Treant", "Forest Guardian"],
        "description": "A soaring city built into a sacred tree, home to ancient knowledge and nature spirits"
    },
    "Silent Ashes": {
        "type": "dungeon",
        "monsters": ["Ash Revenant", "Cursed Wanderer"],
        "description": "The ruins of a once-great city buried in ash and echoing with whispers of the past"
    },
    "Suirai": {
        "type": "city",
        "shops": ["Shogun's Armory", "Suirai Market", "Mystic Dojo"],
        "monsters": ["Shogun's Guard", "Jade Samurai", "Kitsune Warrior", "Tengu Warrior", "Oni Berserker", "Shadow Samurai"],
        "description": "A bustling city known for its fierce warriors and ancient traditions, and the capital of the Shogunate of Shirui."
    },
    "Dragon's Reach": {
        "type": "dangerous",
        "monsters": ["Dragon Whelp", "Dragon Spirit", "Dragon Knight"],
        "description": "A perilous mountain range where dragons and their knights roam."
    },
    "Sunken Abyss": {
        "type": "dungeon",
        "monsters": ["Abyssal Kraken", "Sunken Ghost", "Coral Golem"],
        "description": "An underwater trench filled with ancient ruins and dangerous sea creatures."
    },
    "Frostfang Keep": {
        "type": "dungeon",
        "monsters": ["Frost Giant", "Ice Revenant", "Frost Wraith"],
        "description": "A frozen fortress haunted by icy spirits and giants."
    },
    "Glimmering Grotto": {
        "type": "dungeon",
        "monsters": ["Crystal Golem", "Glimmering Sprite"],
        "description": "A cave filled with shimmering crystals and magical creatures."
    },
    "Imperial City": {
        "type": "city",
        "shops": ["Imperial Armory", "Grand Bazaar", "Royal Jeweler", "Alchemist's Guild"],
        "monsters": ["Imperial Guard", "Dark Sun Agent", "Royal Knight"],
        "description": "The sprawling capital of the Empire of Eternal Flame, with grand architecture and oppressive security provided by the Dark Sun Order."
    },
    "Dark Sun Headquarters": {
        "type": "dungeon",
        "monsters": ["Dark Sun Enforcer", "Shadow Mage", "Dark Sun Commander", "Sun Lord Eclipsius"],
        "description": "The hidden base of operations for the Dark Sun Order, the Empire's ruthless secret police. Few who enter ever leave."
    },
    "Resistance Hideout": {
        "type": "town",
        "shops": ["Blackmarket Trader", "Resistance Armorer", "Safe House"],
        "monsters": ["Imperial Spy", "Mercenary"],
        "description": "A secret network of caves and tunnels where rebels plan their resistance against the Empire and the Dark Sun Order."
    },
}

# Character classes
CHARACTER_CLASSES = {
    "Warrior": {"health_bonus": 20, "attack_bonus": 10, "defense_bonus": 15, "speed_bonus": 5},
    "Mage": {"health_bonus": -10, "attack_bonus": 25, "defense_bonus": 0, "speed_bonus": 7},
    "Rogue": {"health_bonus": 0, "attack_bonus": 15, "defense_bonus": 5, "speed_bonus": 10},
    "Paladin": {"health_bonus": 30, "attack_bonus": 15, "defense_bonus": 20, "speed_bonus": 4},
    "Archer": {"health_bonus": -10, "attack_bonus": 20, "defense_bonus": 5, "speed_bonus": 8},
    "Berserker": {"health_bonus": 20, "attack_bonus": 30, "defense_bonus": -10, "speed_bonus": 6},
    "Priest": {"health_bonus": 10, "attack_bonus": 5, "defense_bonus": 10, "speed_bonus": 5},
    "Assassin": {"health_bonus": -15, "attack_bonus": 35, "defense_bonus": -5, "speed_bonus": 12},
    "Druid": {"health_bonus": 15, "attack_bonus": 10, "defense_bonus": 15, "speed_bonus": 6},
    "Samurai": {"health_bonus": 0, "attack_bonus": 20, "defense_bonus": 10, "speed_bonus": 9},
    "Ninja": {"health_bonus": -5, "attack_bonus": 25, "defense_bonus": 5, "speed_bonus": 11},
    "Knight": {"health_bonus": 40, "attack_bonus": 10, "defense_bonus": 20, "speed_bonus": 4},
    "Hunter": {"health_bonus": 0, "attack_bonus": 15, "defense_bonus": 10, "speed_bonus": 7},
    "Tamer": {"health_bonus": 35, "attack_bonus": 50, "defense_bonus": -25, "speed_bonus": 5},
}

# Item rarity
RARITY_MULTIPLIERS = {
    "Common": 1.0,
    "Uncommon": 1.2,
    "Rare": 1.5,
    "Epic": 2.0,
    "Legendary": 3.0
}

# Basic skills
SKILLS = {
    "Warrior": ["Slam", "Shield Block", "Berserk"],
    "Mage": ["Fireball", "Ice Shield", "Lightning Bolt"],
    "Rogue": ["Backstab", "Stealth", "Poison Strike"],
    "Paladin": ["Holy Strike", "Divine Shield", "Healing Light"],
    "Archer": ["Quick Shot", "Rain of Arrows", "Eagle Eye"],
    "Berserker": ["Rage", "Whirlwind", "Blood Thirst"],
    "Priest": ["Holy Nova", "Divine Heal", "Smite"],
    "Assassin": ["Shadow Strike", "Vanish", "Death Mark"],
    "Druid": ["Entangle", "Nature's Touch", "Beast Form"],
    "Samurai": ["Iaijutsu Slash", "Bushido Focus", "Wind Cutter"],
    "Ninja": ["Shuriken Toss", "Shadow Clone", "Silent Step"],
    "Knight": ["Shield Bash", "Taunt", "Valor Strike"],
    "Hunter": ["Trap Set", "Beast Call", "Piercing Arrow"],
    "Tamer": ["Summon Beast", "Beast Fury", "Bonded Strike"]

}

# Enhanced crafting system
CRAFTING_RECIPES = {
    "Iron Sword": {
        "materials": {"Iron Ingot": 2, "Wood": 1},
        "level_required": 2,
        "type": "weapon",
        "effect": 10
    },
    "Steel Sword": {
        "materials": {"Steel Ingot": 2, "Leather": 1},
        "level_required": 5,
        "type": "weapon",
        "effect": 15
    },
    "Health Potion": {
        "materials": {"Red Herb": 2, "Water Flask": 1},
        "level_required": 1,
        "type": "consumable",
        "effect": 30
    },
    "Iron Armor": {
        "materials": {"Iron Ingot": 4, "Leather": 2},
        "level_required": 3,
        "type": "armor",
        "effect": 10
    }
}

# Materials that can be gathered
MATERIALS = {
    "Wood": {"areas": ["Forest"], "tool_required": "Axe"},
    "Iron Ore": {"areas": ["Cave", "Mountain"], "tool_required": "Pickaxe"},
    "Red Herb": {"areas": ["Forest", "Plains"], "tool_required": None},
    "Blue Herb": {"areas": ["Mountain", "Cave"], "tool_required": None},
    "Green Herb": {"areas": ["Forest", "Swamp"], "tool_required": None},
    "Water Flask": {"areas": ["River", "Lake"], "tool_required": "Flask"},
    "Leather": {"areas": ["Plains"], "tool_required": "Hunting Knife"},
    "Steel Ingot": {"areas": ["Mines","Mountains"], "tool_required": "Furnace"},
    "Gold Ore": {"areas": ["Mountain", "Deep Cave"], "tool_required": "Pickaxe"},
    "Magic Crystal": {"areas": ["Crystal Cave", "Ancient Ruins"], "tool_required": "Magic Chisel"},
    "Fish": {"areas": ["River", "Lake", "Coast"], "tool_required": "Fishing Rod"},
    "Silk Thread": {"areas": ["Forest", "Spider Nest"], "tool_required": "Silk Spinner"},
    "Clay": {"areas": ["Riverbank", "Swamp"], "tool_required": "Shovel"},
    "Coal": {"areas": ["Mines", "Mountain"], "tool_required": "Pickaxe"},
    "Ancient Relic": {"areas": ["Ancient Ruins", "Temple"], "tool_required": "Archaeology Kit"},
    "Salt": {"areas": ["Cave", "Desert Spring"], "tool_required": "Pickaxe"},
    "Venom Sac": {"areas": ["Swamp", "Spider Nest"], "tool_required": "Hunting Knife"},
    "Paper": {"areas": ["Forest", "Village"], "tool_required": "Wood Press"},
    "Magic Ink": {"areas": ["Ancient Ruins", "Wizard Tower"], "tool_required": "Magic Vial"},
    "Fire Essence": {"areas": ["Volcano", "Forge"], "tool_required": "Essence Collector"},
    "Stone": {"areas": ["Mountain", "River", "Plains"], "tool_required": "Pickaxe"},
    "Glass": {"areas": ["Desert", "Beach"], "tool_required": "Furnace"},
    "Sand": {"areas": ["Desert", "Beach"], "tool_required": "Shovel"},
    "Straw": {"areas": ["Plains", "Farm"], "tool_required": None},
    "Cloth": {"areas": ["Village", "City"], "tool_required": "Loom"},
    "Gears": {"areas": ["Workshop", "City"], "tool_required": "Metalworking Kit"},
    "Weather Sample": {"areas": ["Mountain Top", "Storm Plains", "Weather Sage's Hut"], "tool_required": "Weather Collection Kit"},
    "Feathers": {"areas": ["Plains", "Cliffside"], "tool_required": None},
    "Magma Stone": {"areas": ["Volcano", "Lava River"], "tool_required": "Pickaxe"},
    "Dragon Scale": {"areas": ["Dragon's Peak", "Dragon's Reach"], "tool_required": None},
    "Wheat seeds": {"areas": ["Plains", "Abundant Field"], "tool_required": None},
    "Rice seeds": {"areas": ["Plains", "Abundant Field"], "tool_required": None},
    "Lotus Seeds": {"areas": ["Lotus Pond", "Swamp"], "tool_required": None},
}

# Story quests are marked with story=True
QUESTS = [
    # Chapter 1: The Awakening Story Quests
    {
        "id": 101,
        "name": "The Beginning",
        "description": "Meet the Old Sage in Greenwood Village",
        "target": {"npc": "Old Sage", "count": 1},
        "reward": {"gold": 100, "exp": 200},
        "story": True,
        "chapter": 1,
        "travel_locations": ["Greenwood Village", "Stormhaven", "Crystal Cave"]
    },
    {
        "id": 102,
        "name": "First Steps",
        "description": "Defeat 10 monsters across Greenwood Village and Stormhaven",
        "target": {"monster": "any", "count": 10},
        "reward": {"gold": 150, "exp": 250},
        "story": True,
        "chapter": 1,
        "travel_locations": ["Greenwood Village", "Stormhaven"]
    },
    {
        "id": 103,
        "name": "The Dark Warning",
        "description": "Investigate the disturbance in Crystal Cave and Shadowmere",
        "target": {"location": "Crystal Cave", "count": 1},
        "reward": {"gold": 200, "exp": 300},
        "story": True,
        "chapter": 1,
        "travel_locations": ["Crystal Cave", "Shadowmere"]
    },

    # Chapter 2: The Dragon's Call Story Quests
    {
        "id": 201,
        "name": "Dragon's Peak Journey",
        "description": "Travel to Dragon's Peak, Stormhaven, and Greenwood Village to meet the Dragon Tamer",
        "target": {"npc": "Dragon Tamer", "count": 1},
        "reward": {"gold": 300, "exp": 400},
        "story": True,
        "chapter": 2,
        "travel_locations": ["Dragon's Peak", "Stormhaven", "Greenwood Village"]
    },
    {
        "id": 202,
        "name": "Dragon Trials",
        "description": "Complete the three trials of the Dragon Tamer across Dragon's Peak",
        "target": {"trials": "Dragon Trials", "count": 3},
        "reward": {"gold": 400, "exp": 500},
        "story": True,
        "chapter": 2,
        "travel_locations": ["Dragon's Peak"]
    },
    {
        "id": 203,
        "name": "The First Flight",
        "description": "Tame your first dragon after traveling through Dragon's Peak and Crystal Cave",
        "target": {"monster": "Dragon Whelp", "count": 1},
        "reward": {"gold": 500, "exp": 600, "item": "Dragon Whistle"},
        "story": True,
        "chapter": 2,
        "travel_locations": ["Dragon's Peak", "Crystal Cave"]
    },

    # Chapter 3: Shadows of the Past Story Quests
    {
        "id": 301,
        "name": "The Shadow's Call",
        "description": "Investigate the mysterious events in Shadowmere and Frostvale",
        "target": {"location": "Shadowmere", "count": 1},
        "reward": {"gold": 600, "exp": 700},
        "story": True,
        "chapter": 3,
        "travel_locations": ["Shadowmere", "Frostvale"]
    },
    {
        "id": 302,
        "name": "Ancient Secrets",
        "description": "Recover the lost artifacts from the Silent Ashes and Crystal Cave",
        "target": {"item": "Ancient Artifact", "count": 3},
        "reward": {"gold": 700, "exp": 800},
        "story": True,
        "chapter": 3,
        "travel_locations": ["Silent Ashes", "Crystal Cave"]
    },
    {
        "id": 303,
        "name": "The Shadow's Return",
        "description": "Confront the Shadow Master in his lair after traveling through Shadowmere and the Sunken Depths",
        "target": {"monster": "Shadow Master", "count": 1},
        "reward": {"gold": 1000, "exp": 1200, "item": "Shadow Master's Cloak"},
        "story": True,
        "chapter": 3,
        "travel_locations": ["Shadowmere", "Sunken Depths"]
    },
    {
        "id": 401,
        "name": "Shadow Infiltration",
        "description": "Infiltrate the Dark Sun Order's outer circle to gather intelligence on their operations.",
        "target": {"monster": "Dark Sun Agent", "count": 3},
        "reward": {"gold": 1200, "exp": 1600, "item": "Agent's Mask"},
        "story": True,
        "chapter": 4,
        "travel_locations": ["Imperial City", "Shadowmere"]
    },
    {
        "id": 402,
        "name": "The Informant",
        "description": "Make contact with a secret informant who can provide intel on the Dark Sun Order.",
        "target": {"npc": "Mysterious Informant", "count": 1},
        "reward": {"gold": 1300, "exp": 1700, "item": "Encrypted Documents"},
        "story": True,
        "chapter": 4,
        "travel_locations": ["Stormhaven", "Shadowmere"]
    },
    {
        "id": 403,
        "name": "Dark Sun Archives",
        "description": "Break into the Dark Sun archives to uncover evidence of their crimes.",
        "target": {"location": "Imperial City", "count": 1},
        "reward": {"gold": 1400, "exp": 1800, "item": "Dark Sun Cipher"},
        "story": True,
        "chapter": 4,
        "travel_locations": ["Imperial City", "Dark Sun Headquarters"]
    },
    {
        "id": 501,
        "name": "Resistance Contact",
        "description": "Establish contact with the resistance fighting against the Empire and the Dark Sun Order.",
        "target": {"npc": "Resistance Leader", "count": 1},
        "reward": {"gold": 1600, "exp": 2000, "item": "Resistance Badge"},
        "story": True,
        "chapter": 5,
        "travel_locations": ["Resistance Hideout", "Greenwood Village"]
    },
    {
        "id": 502,
        "name": "Imperial Fortress",
        "description": "Infiltrate one of the Empire's fortresses to sabotage their weapons supply.",
        "target": {"location": "Imperial Fortress", "count": 1},
        "reward": {"gold": 1800, "exp": 2200, "item": "Imperial Officer's Key"},
        "story": True,
        "chapter": 5,
        "travel_locations": ["Imperial City", "Thundercliff Hold"]
    },
    {
        "id": 503,
        "name": "Escape from the Capital",
        "description": "Help resistance fighters escape from the Imperial City while evading Dark Sun agents.",
        "target": {"npc": "Captured Resistance Member", "count": 3},
        "reward": {"gold": 2000, "exp": 2400, "item": "Shadow Cloak"},
        "story": True,
        "chapter": 5,
        "travel_locations": ["Imperial City", "Resistance Hideout"]
    },
    {
        "id": 601,
        "name": "Uniting the Factions",
        "description": "Travel across the land to unite the various resistance factions against the Empire.",
        "target": {"npc": "Faction Leader", "count": 4},
        "reward": {"gold": 2200, "exp": 2700, "item": "Unity Banner"},
        "story": True,
        "chapter": 6,
        "travel_locations": ["Stormhaven", "Verdant Spire", "Moonveil Harbor", "Resistance Hideout"]
    },
    {
        "id": 602,
        "name": "Battle for Freedom",
        "description": "Lead an assault on the Dark Sun Headquarters to dismantle their power structure.",
        "target": {"monster": "Dark Sun Commander", "count": 1},
        "reward": {"gold": 2300, "exp": 2800, "item": "Sorcerer's Tome"},
        "story": True,
        "chapter": 6,
        "travel_locations": ["Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains"]
    },
    {
        "id": 603,
        "name": "Sacred Fire",
        "description": "Ignite the sacred fire to rally the people against the empire.",
        "target": {"location": "Tlācahcāyōtl Tletl Tecpanēcatl Palace", "count": 1},
        "reward": {"gold": 2400, "exp": 2900, "item": "Sacred Flame"},
        "story": True,
        "chapter": 6,
        "travel_locations": ["Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains"]
    },
    {
        "id": 701,
        "name": "Crimson Abyss Awakening",
        "description": "Investigate the awakening of dark forces in the Crimson Abyss.",
        "target": {"monster": "Crimson Abyss Demon", "count": 1},
        "reward": {"gold": 3000, "exp": 3500, "item": "Demon's Heart"},
        "story": True,
        "chapter": 7,
        "travel_locations": ["Crimson Abyss"]
    },
    {
        "id": 702,
        "name": "Demon's Heart",
        "description": "Retrieve the Demon's Heart from the depths of the Crimson Abyss.",
        "target": {"monster": "Crimson Abyss Demon", "count": 1},
        "reward": {"gold": 3200, "exp": 3700, "item": "Demon's Heart"},
        "story": True,
        "chapter": 7,
        "travel_locations": ["Crimson Abyss"]
    },
    {
        "id": 703,
        "name": "Abyssal Leviathan",
        "description": "Defeat the Abyssal Leviathan terrorizing the Crimson Abyss.",
        "target": {"monster": "Abyssal Leviathan", "count": 1},
        "reward": {"gold": 3500, "exp": 4000, "item": "Leviathan Scale"},
        "story": True,
        "chapter": 7,
        "travel_locations": ["Crimson Abyss"]
    },
    {
        "id": 704,
        "name": "The Final Shadow",
        "description": "Confront the Shadow Master in the depths of the Crimson Abyss.",
        "target": {"monster": "Shadow Master", "count": 1},
        "reward": {"gold": 4000, "exp": 4500, "item": "Shadow Master's Cloak"},
        "story": True,
        "chapter": 7,
        "travel_locations": ["Crimson Abyss"]
    },
    {
        "id": 801,
        "name": "The Final War to end the Shadow order",
        "description": "Confront the Fallen Eternal,Noctis",
        "target": {"monster": "Dark Legionary Supreme Lord:Noctis", "count": 1},
        "reward": {"gold": 5000, "exp": 5500, "item": "Noctis's Shadow Crystal"},
        "story": True,
        "chapter": 8,
        "travel_locations": ["Dark Legion's Fortress"]
    },
    {
        "id": 1,
        "name": "Goblin Slayer",
        "description": "Kill 3 goblins",
        "target": {"monster": "Goblin", "count": 3},
        "reward": {"gold": 50, "exp": 100}
    },
    {
        "id": 2,
        "name": "Dragon Hunter",
        "description": "Defeat any dragon",
        "target": {"monster": "Dragon", "count": 1},
        "reward": {"gold": 200, "exp": 300}
    },
    {
        "id": 3,
        "name": "Howling Threat",
        "description": "Hunt down 5 wolves in the forest",
        "target": {"monster": "Wolf", "count": 5},
        "reward": {"gold": 40, "exp": 90}
    },
    {
        "id": 4,
        "name": "Skeleton Cleanup",
        "description": "Destroy 4 skeletons near the cemetery",
        "target": {"monster": "Skeleton", "count": 4},
        "reward": {"gold": 60, "exp": 110}
    },
    {
        "id": 5,
        "name": "Ghostly Presence",
        "description": "Banish 3 ghosts from Stormhaven",
        "target": {"monster": "Ghost", "count": 3},
        "reward": {"gold": 70, "exp": 150}
    },
    {
        "id": 6,
        "name": "Troll Trouble",
        "description": "Defeat 2 Cave Trolls",
        "target": {"monster": "Cave Troll", "count": 2},
        "reward": {"gold": 90, "exp": 180}
    },
    {
        "id": 7,
        "name": "Dark Knight Duel",
        "description": "Take down 1 Dark Knight in Shadowmere",
        "target": {"monster": "Dark Knight", "count": 1},
        "reward": {"gold": 120, "exp": 250}
    },
    {
        "id": 8,
        "name": "Fire Dragon Challenge",
        "description": "Defeat the Fire Dragon atop Dragon's Peak",
        "target": {"monster": "Fire Dragon", "count": 1},
        "reward": {"gold": 250, "exp": 400}
    },
    {
        "id": 9,
        "name": "Crystal Golem Rampage",
        "description": "Stop 2 Crystal Golems in Crystal Cave",
        "target": {"monster": "Crystal Golem", "count": 2},
        "reward": {"gold": 100, "exp": 200}
    },
    {
        "id": 10,
        "name": "Ice Troll Hunt",
        "description": "Eliminate 3 Ice Trolls in Frostvale",
        "target": {"monster": "Ice Troll", "count": 3},
        "reward": {"gold": 80, "exp": 170}
    },
    {
        "id": 11,
        "name": "Phoenix Feather",
        "description": "Collect 1 Phoenix Feather from the Silent Ashes",
        "target": {"monster": "Phoenix", "count": 1},
        "reward": {"gold": 300, "exp": 500}
    },
    {
        "id": 12,
        "name": "Water Elemental",
        "description": "Defeat 2 Water Elementals in Long Shui Zhen",
        "target": {"monster": "Water Elemental", "count": 2},
        "reward": {"gold": 110, "exp": 220}
    },
    {
        "id": 13,
        "name": "Sunken Depths",
        "description": "Explore the Sunken Depths and gather 3 Coral Golem parts",
        "target": {"monster": "Coral Golem", "count": 3},
        "reward": {"gold": 130, "exp": 250}
    },
    {
        "id": 14,
        "name": "Free the people",
        "description": "Free the Shogunate from the Shogun's Tyrany",
        "target": {"monster": "The Shogun", "count": 1},
        "reward": {"gold": 500, "exp": 1000}
    },
    {
        "id": 15,
        "name": "Dragon's Reach",
        "description": "Defeat the Dragon Knight in Dragon's Reach",
        "target": {"monster": "Dragon Knight", "count": 1},
        "reward": {"gold": 400, "exp": 600}
    },
    {
        "id": 16,
        "name": "Blightmoor Cleanup",
        "description": "Eliminate 5 Blight Beasts in Blightmoor",
        "target": {"monster": "Blight Beast", "count": 5},
        "reward": {"gold": 150, "exp": 300}
    },
    # New quests for Iron Caliphate of Al-Khilafah Al-Hadidiyah
    {
        "id": 553,
        "name": "Sabotage Supply Lines",
        "description": "Disrupt the Iron Caliphate's supply routes to weaken their forces.",
        "target": {"location": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah", "count": 1},
        "reward": {"gold": 2000, "exp": 2500, "item": "Blueprints for Resistance Gear"},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 554,
        "name": "Rescue Imprisoned Dissidents",
        "description": "Free the dissidents imprisoned by the Iron Caliphate.",
        "target": {"npc": "Imprisoned Dissidents", "count": 1},
        "reward": {"gold": 2100, "exp": 2600, "item": "Resistance Gear"},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 505,
        "name": "Infiltrate the Palace",
        "description": "Sneak into the Iron Caliphate's palace to gather intelligence.",
        "target": {"location": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah Palace", "count": 1},
        "reward": {"gold": 2200, "exp": 2700, "item": "Special Weapons"},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 506,
        "name": "Recover Stolen Artifacts",
        "description": "Retrieve artifacts stolen by the Iron Caliphate's forces.",
        "target": {"item": "Stolen Artifact", "count": 3},
        "reward": {"gold": 2300, "exp": 2800, "item": "Access to Guarded Areas"},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 507,
        "name": "Distract the Patrols",
        "description": "Create diversions to help resistance members move freely.",
        "target": {"location": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah", "count": 1},
        "reward": {"gold": 1900, "exp": 2300},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 508,
        "name": "Smuggle Supplies",
        "description": "Help smuggle food and medical supplies to the resistance.",
        "target": {"location": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah", "count": 1},
        "reward": {"gold": 2000, "exp": 2400},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    # New quests for Shogunate of Shirui
    {
        "id": 433,
        "name": "Assassinate a Corrupt Official",
        "description": "Eliminate a corrupt official threatening the Shogunate's peace.",
        "target": {"npc": "Corrupt Official", "count": 1},
        "reward": {"gold": 1400, "exp": 1800, "item": "Unique Samurai Weapons"},
        "story": False,
        "chapter": 4,
        "travel_locations": ["Shogunate of Shirui"]
    },
    {
        "id": 434,
        "name": "Protect a Whistleblower",
        "description": "Escort a whistleblower safely out of the Shogunate.",
        "target": {"npc": "Whistleblower", "count": 1},
        "reward": {"gold": 1500, "exp": 1900, "item": "Ronin Armor"},
        "story": False,
        "chapter": 4,
        "travel_locations": ["Shogunate of Shirui"]
    },
    # New quests for Shadowmere
    {
        "id": 304,
        "name": "Retrieve Stolen Secrets",
        "description": "Recover secrets stolen by rival factions in Shadowmere.",
        "target": {"item": "Stolen Secrets", "count": 3},
        "reward": {"gold": 1100, "exp": 1300, "item": "Rare Magic Items"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Shadowmere"]
    },
    {
        "id": 305,
        "name": "Eliminate a Rival",
        "description": "Take out a rival threatening the Shadow Broker's operations.",
        "target": {"npc": "Rival", "count": 1},
        "reward": {"gold": 1200, "exp": 1400, "item": "Forbidden Scrolls"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Shadowmere"]
    },
    # New quests for Frostvale
    {
        "id": 306,
        "name": "Contain the Ice Wraith",
        "description": "Stop the Ice Wraith from terrorizing Frostvale.",
        "target": {"monster": "Ice Wraith", "count": 1},
        "reward": {"gold": 1300, "exp": 1500, "item": "Ice-elemental Weapons"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Frostvale"]
    },
    {
        "id": 307,
        "name": "Retrieve Magical Research",
        "description": "Find lost magical research in Frostvale.",
        "target": {"item": "Magical Research", "count": 1},
        "reward": {"gold": 1400, "exp": 1600, "item": "Frost-resistant Gear"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Frostvale"]
    },
    # New quests for Dragon's Peak
    {
        "id": 204,
        "name": "Retrieve a Specific Egg",
        "description": "Find and retrieve a rare dragon egg.",
        "target": {"item": "Dragon Egg", "count": 1},
        "reward": {"gold": 600, "exp": 700, "item": "Dragon Egg Fragments"},
        "story": False,
        "chapter": 2,
        "travel_locations": ["Dragon's Peak"]
    },
    {
        "id": 205,
        "name": "Protect a Nest",
        "description": "Defend a dragon's nest from poachers.",
        "target": {"location": "Dragon's Peak", "count": 1},
        "reward": {"gold": 650, "exp": 750, "item": "Rare Mounts"},
        "story": False,
        "chapter": 2,
        "travel_locations": ["Dragon's Peak"]
    },
    # New quests for Long Shui Zhen
    {
        "id": 308,
        "name": "Decode Ancient Dragon Texts",
        "description": "Translate ancient texts about dragons.",
        "target": {"item": "Ancient Dragon Texts", "count": 1},
        "reward": {"gold": 900, "exp": 1100, "item": "Dragon Lore Books"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Long Shui Zhen"]
    },
    {
        "id": 309,
        "name": "Find a Legendary Dragon",
        "description": "Locate a legendary dragon hidden in the mountains.",
        "target": {"monster": "Legendary Dragon", "count": 1},
        "reward": {"gold": 1000, "exp": 1200, "item": "Knowledge-based Items"},
        "story": False,
        "chapter": 3,
        "travel_locations": ["Long Shui Zhen's well"]
    },
    
    # Seasonal Farming Quests
    {
        "id": 451,
        "name": "Winter's Harvest",
        "description": "Grow and harvest 5 Winter Mint plants during the winter season.",
        "target": {"item": "Winter Mint", "count": 5},
        "reward": {"gold": 600, "exp": 500, "item": "Rare Winter Seeds"},
        "story": False,
        "chapter": 4,
        "requirements": {"season": "Winter"}
    },
    {
        "id": 452,
        "name": "Spring Bloom",
        "description": "Grow and harvest 5 Spring Tulips during the spring season.",
        "target": {"item": "Spring Tulips", "count": 5},
        "reward": {"gold": 550, "exp": 450, "item": "Rare Spring Seeds"},
        "story": False,
        "chapter": 4,
        "requirements": {"season": "Spring"}
    },
    {
        "id": 453,
        "name": "Summer's Bounty",
        "description": "Grow and harvest 5 Summer Melons during the summer season.",
        "target": {"item": "Summer Melon", "count": 5},
        "reward": {"gold": 700, "exp": 550, "item": "Rare Summer Seeds"},
        "story": False,
        "chapter": 4,
        "requirements": {"season": "Summer"}
    },
    {
        "id": 454,
        "name": "Autumn's Yield",
        "description": "Grow and harvest 5 Autumn Squash during the fall season.",
        "target": {"item": "Autumn Squash", "count": 5},
        "reward": {"gold": 650, "exp": 500, "item": "Rare Fall Seeds"},
        "story": False,
        "chapter": 4,
        "requirements": {"season": "Fall"}
    },
    
    # Weather-Dependent Quests
    {
        "id": 405,
        "name": "Storm Harvester",
        "description": "Grow and harvest 3 Thunderroots during stormy weather.",
        "target": {"item": "Thunderroot", "count": 3},
        "reward": {"gold": 800, "exp": 700, "item": "Lightning Essence"},
        "story": False,
        "chapter": 4,
        "requirements": {"weather": "stormy"}
    },
    {
        "id": 406,
        "name": "Frost Gardener",
        "description": "Grow and harvest 3 Frost Lotus plants during snowy weather.",
        "target": {"item": "Frost Lotus", "count": 3},
        "reward": {"gold": 850, "exp": 750, "item": "Frost Essence"},
        "story": False,
        "chapter": 4,
        "requirements": {"weather": "snowy"}
    },
    {
        "id": 407,
        "name": "Desert Bloom",
        "description": "Grow and harvest 3 Ghost Peppers during hot, sunny weather.",
        "target": {"item": "Ghost Pepper", "count": 3},
        "reward": {"gold": 900, "exp": 800, "item": "Fire Essence"},
        "story": False,
        "chapter": 4,
        "requirements": {"weather": "sunny"}
    },
    
    # Secondary Story Quests - The Weather Sage's Tale
    {
        "id": 851,
        "name": "The Weather Sage",
        "description": "Meet with the Weather Sage who lives in the mountains.",
        "target": {"npc": "Weather Sage", "count": 1},
        "reward": {"gold": 400, "exp": 350, "item": "Weather Map"},
        "story": True,
        "story_arc": "Weather Mysteries",
        "chapter": 8
    },
    {
        "id": 852,
        "name": "Collecting Weather Samples",
        "description": "Collect samples from different weather conditions for the Weather Sage.",
        "target": {"item": "Weather Sample", "count": 4},
        "reward": {"gold": 500, "exp": 450, "item": "Weather Vane"},
        "story": True,
        "story_arc": "Weather Mysteries",
        "chapter": 8,
        "prerequisite": 851
    },
    {
        "id": 853,
        "name": "The Weather Anomaly",
        "description": "Investigate the mysterious weather anomaly in the Ancient Forest.",
        "target": {"location": "Ancient Forest", "count": 1},
        "reward": {"gold": 600, "exp": 550, "item": "Weathered Pendant"},
        "story": True,
        "story_arc": "Weather Mysteries",
        "chapter": 8,
        "prerequisite": 852
    },
    {
        "id": 854,
        "name": "Confronting the Storm Entity",
        "description": "Defeat the entity causing the weather disturbances.",
        "target": {"monster": "Storm Entity", "count": 1},
        "reward": {"gold": 1000, "exp": 900, "item": "Weather Control Rod"},
        "story": True,
        "story_arc": "Weather Mysteries",
        "chapter": 8,
        "prerequisite": 853
    },
    
    # Dimension-Specific Secondary Stories - The Void Walker
    {
        "id": 901,
        "name": "Strange Disturbances",
        "description": "Investigate dimensional rifts appearing in various locations.",
        "target": {"item": "Dimensional Fragment", "count": 5},
        "reward": {"gold": 700, "exp": 650, "item": "Dimensional Compass"},
        "story": True,
        "story_arc": "Void Walker",
        "chapter": 9
    },
    {
        "id": 902,
        "name": "The Void Walker's Trail",
        "description": "Follow the mysterious entity that's been crossing between dimensions.",
        "target": {"location": "Dimensional Nexus", "count": 1},
        "reward": {"gold": 800, "exp": 750, "item": "Void Shard"},
        "story": True,
        "story_arc": "Void Walker",
        "chapter": 9,
        "prerequisite": 901
    },
    {
        "id": 903,
        "name": "Dimensional Guardians",
        "description": "Defeat the guardians protecting the dimensional gates.",
        "target": {"monster": "Dimension Guardian", "count": 3},
        "reward": {"gold": 900, "exp": 850, "item": "Guardian's Essence"},
        "story": True,
        "story_arc": "Void Walker",
        "chapter": 9,
        "prerequisite": 902
    },
    {
        "id": 904,
        "name": "The Void Walker's Identity",
        "description": "Discover the true identity of the Void Walker and their intentions.",
        "target": {"npc": "Void Walker", "count": 1},
        "reward": {"gold": 1200, "exp": 1100, "item": "Dimensional Key"},
        "story": True,
        "story_arc": "Void Walker",
        "chapter": 9,
        "prerequisite": 903
    }
]

# Available professions with their bonuses
PROFESSIONS = {
    # Traditional professions
    "Miner": {
        "gather_bonus": ["Iron Ore", "Gold Ore", "Silver Ore", "Mythril Ore", "Ancient Fossil"],
        "craft_bonus": ["weapons", "mining tools"],
        "special_ability": "Deep Mining",
        "ability_description": "Chance to find rare ores and gems",
        "passive_bonus": {"defense": 5},
        "level_bonuses": {
            5: "Ore Identification - Can identify rare ores without tools",
            10: "Double Mining - Chance to get double resources",
            15: "Gem Expert - Can find gems in normal mining nodes"
        }
    },
    "Herbalist": {
        "gather_bonus": ["Red Herb", "Blue Herb", "Green Herb", "Purple Herb", "Rainbow Herb"],
        "craft_bonus": ["potions", "herbal remedies"],
        "special_ability": "Herbal Knowledge",
        "ability_description": "Can identify useful herbs in any biome",
        "passive_bonus": {"health_regen": 2},
        "level_bonuses": {
            5: "Herb Preservation - Herbs stay fresh longer",
            10: "Double Harvest - Chance to gather twice as many herbs",
            15: "Rare Herb Finder - Can locate rare herbs in any biome"
        }
    },
    "Blacksmith": {
        "gather_bonus": ["Iron Ore", "Steel Ingot", "Metal Scraps"],
        "craft_bonus": ["armor", "weapons", "tools"],
        "special_ability": "Master Forging",
        "ability_description": "Chance to create superior quality equipment",
        "passive_bonus": {"attack": 3},
        "level_bonuses": {
            5: "Metal Conservation - Uses fewer materials when crafting",
            10: "Quality Crafting - Higher durability on crafted items",
            15: "Masterwork - Chance to create exceptional quality gear"
        }
    },
    "Alchemist": {
        "gather_bonus": ["Red Herb", "Magic Crystal", "Alchemical Base"],
        "craft_bonus": ["potions", "elixirs", "transmutations"],
        "special_ability": "Potion Mastery",
        "ability_description": "Potions have stronger effects",
        "passive_bonus": {"magic_defense": 5},
        "level_bonuses": {
            5: "Conservation - Chance to not consume ingredients",
            10: "Extended Effect - Potions last longer",
            15: "Alchemical Breakthrough - Can create unique potions"
        }
    },
    "Hunter": {
        "gather_bonus": ["Leather", "Monster Part", "Hunter's Trophy", "Rare Pelt"],
        "craft_bonus": ["bows", "hunting gear", "traps"],
        "special_ability": "Keen Eye",
        "ability_description": "Can track rare monsters more easily",
        "passive_bonus": {"critical_chance": 3},
        "level_bonuses": {
            5: "Clean Kill - Better quality materials from monsters",
            10: "Monster Knowledge - Increased damage against known monsters",
            15: "Rare Trophy - Chance to obtain unique monster parts"
        }
    },
    "Woodcutter": {
        "gather_bonus": ["Wood", "Rare Wood", "Ancient Bark", "Living Wood"],
        "craft_bonus": ["staves", "wooden weapons", "wooden structures"],
        "special_ability": "Lumber Expert",
        "ability_description": "Can harvest special types of wood",
        "passive_bonus": {"max_health": 10},
        "level_bonuses": {
            5: "Efficient Chopping - More wood from each tree",
            10: "Wood Whisperer - Can find magical wood types",
            15: "Ancient Forestry - Can harvest from ancient trees"
        }
    },
    "Fisher": {
        "gather_bonus": ["Fish", "Rare Fish", "Coral", "Deep Sea Treasure"],
        "craft_bonus": ["fishing gear", "water-based potions"],
        "special_ability": "Deep Fishing",
        "ability_description": "Can catch rare aquatic creatures",
        "passive_bonus": {"water_resistance": 10},
        "level_bonuses": {
            5: "Patient Angler - Better quality fish",
            10: "Treasure Hunter - Chance to find sunken treasures",
            15: "Master Baiter - Can catch legendary fish"
        }
    },
    "Archaeologist": {
        "gather_bonus": ["Ancient Relic", "Historical Artifact", "Lost Knowledge"],
        "craft_bonus": ["artifacts", "ancient weapons"],
        "special_ability": "Historian",
        "ability_description": "Can identify and restore ancient items",
        "passive_bonus": {"intelligence": 5},
        "level_bonuses": {
            5: "Careful Excavation - Better condition artifacts",
            10: "Lost Knowledge - Can read ancient texts",
            15: "Treasure Maps - Can locate hidden ruins and treasures"
        }
    },
    "Enchanter": {
        "gather_bonus": ["Magic Crystal", "Enchanted Fragment", "Arcane Dust"],
        "craft_bonus": ["enchanted items", "magical weapons"],
        "special_ability": "Mana Infusion",
        "ability_description": "Can create more powerful enchantments",
        "passive_bonus": {"magic_power": 8},
        "level_bonuses": {
            5: "Magical Insight - Can see magical properties of items",
            10: "Enchantment Mastery - Stronger enchantments",
            15: "Artifact Creation - Can create custom magical items"
        }
    },
    
    # New professions
    "Farmer": {
        "gather_bonus": ["Seeds", "Crop", "Fertilizer", "Exotic Seeds"],
        "craft_bonus": ["farming tools", "food", "crop-based items"],
        "special_ability": "Green Thumb",
        "ability_description": "Crops grow faster and yield more",
        "passive_bonus": {"stamina_regen": 3},
        "level_bonuses": {
            5: "Crop Rotation - Better yields from farming",
            10: "Weather Prediction - Can forecast weather changes",
            15: "Magical Agriculture - Can grow special magical crops"
        },
        "weather_bonuses": {
            "Sunny": "Solar Growth - Crops grow faster in sunny weather",
            "Rainy": "Water Conservation - Less watering needed during rain",
            "Stormy": "Lightning Infusion - Chance for crops to gain special properties"
        },
        "season_bonuses": {
            "Spring": "Spring Bloom - Better yields in spring",
            "Summer": "Summer Heat - Faster growth in summer",
            "Fall": "Harvest Bounty - More crops in fall",
            "Winter": "Cold Resilience - Can grow special winter crops"
        }
    },
    "Weather Mage": {
        "gather_bonus": ["Storm Crystal", "Weather Essence", "Elemental Core"],
        "craft_bonus": ["weather charms", "elemental weapons"],
        "special_ability": "Weather Sense",
        "ability_description": "Can predict and slightly influence weather",
        "passive_bonus": {"elemental_resistance": 10},
        "level_bonuses": {
            5: "Weather Reading - Can predict weather changes accurately",
            10: "Weather Shift - Can change weather for a short time",
            15: "Elemental Mastery - Weather effects boost elemental damage"
        },
        "weather_bonuses": {
            "Sunny": "Solar Power - Increased fire damage during sunny weather",
            "Rainy": "Hydration - Increased water damage during rainy weather",
            "Stormy": "Storm Caller - Increased lightning damage during storms",
            "Snowy": "Frost Bite - Increased ice damage during snow",
            "Windy": "Wind Rider - Increased movement speed during windy weather",
            "Foggy": "Mistsight - Can see clearly through fog"
        }
    },
    "Artifact Hunter": {
        "gather_bonus": ["Ancient Relic", "Artifact Fragment", "Lost Technology"],
        "craft_bonus": ["artifacts", "ancient weapons", "artifact restoration"],
        "special_ability": "Relic Sense",
        "ability_description": "Can sense nearby artifacts and relics",
        "passive_bonus": {"artifact_power": 15},
        "level_bonuses": {
            5: "Artifact Lore - Can identify artifact properties",
            10: "Restoration Expert - Can restore damaged artifacts",
            15: "Set Completion - Bonus when wearing complete artifact sets"
        }
    },
    "Monster Tamer": {
        "gather_bonus": ["Monster Essence", "Taming Crystal", "Beast Hide"],
        "craft_bonus": ["taming gear", "monster equipment"],
        "special_ability": "Beast Speech",
        "ability_description": "Can communicate with certain monsters",
        "passive_bonus": {"monster_relation": 50},
        "level_bonuses": {
            5: "Monster Empathy - Some monsters won't attack first",
            10: "Taming Mastery - Can tame certain monsters as companions",
            15: "Monster Bond - Tamed monsters are more powerful"
        }
    }
}

# Initialize user data with proper typing
user_data = {
    "name": None,
    "class": None,
    "profession": None,
    "has_chosen_profession": False,
    "level": 1,
    "inventory": [],
    "equipped": {"weapon": None, "armor": None},
    "gold": INITIAL_GOLD,
    "coolness": 0,
    "guild": None,
    "pets": [],
    "progress": "starter",
    "exp": 0,
    "health": INITIAL_HEALTH,
    "max_health": INITIAL_HEALTH,
    "attack": 10,
    "defense": 0,
    "speed": 5,
    "skills": [],
    "active_quests": [],
    "completed_quests": [],
    "materials": {},
    "tools": ["Axe", "Pickaxe", "Flask", "Hunting Knife"],
    "current_area": "Greenwood Village",
    "monsters_killed": 0,
    "dungeons_completed": [],
    # Dimension system data
    "current_dimension": "Overworld",
    "dimensions_discovered": ["Overworld"],
    "dimension_keys": [],
    # Home/camp system data
    "home_structures": {"Tent": {"built": True, "position": [0, 0], "health": 100}},
    "home_location": "Camp"
}

def ensure_user_data_keys(data: Dict) -> None:
    defaults = {
        "class": None,
        "profession": None,
        "has_chosen_profession": False,
        "level": 1,
        "inventory": [],
        "equipped": {"weapon": None, "armor": None},
        "gold": INITIAL_GOLD,
        "coolness": 0,
        "guild": None,
        "pets": [],
        "progress": "starter",
        "exp": 0,
        "health": INITIAL_HEALTH,
        "max_health": INITIAL_HEALTH,
        "attack": 10,
        "defense": 0,
        "speed": 5,
        "skills": [],
        "active_quests": [],
        "completed_quests": [],
        "materials": {},
        "tools": ["Axe", "Pickaxe", "Flask", "Hunting Knife"],
        "current_area": "Greenwood Village",
        "monsters_killed": 0,
        "dungeons_completed": [],
        # Dimension system data
        "current_dimension": "Overworld",
        "dimensions_discovered": ["Overworld"],
        "dimension_keys": [],
        # Home/camp system data
        "home_structures": {"Tent": {"built": True, "position": [0, 0], "health": 100}},
        "home_location": "Camp",
        "achievements": {
            "completed": set(),
            "stats": {
                "monsters_killed": 0,
                "items_crafted": 0,
                "bosses_defeated": 0,
                "quests_completed": 0,
                "areas_visited": set(),
                "crops_harvested": 0,
                "max_damage_dealt": 0,
                "total_gold_earned": 0,
                "rare_items_found": 0
            }
        }
    }
    for key, default_value in defaults.items():
        if key not in data:
            data[key] = default_value
        else:
            # For nested dicts, ensure keys exist recursively
            if isinstance(default_value, dict) and isinstance(data[key], dict):
                for subkey, subdefault in default_value.items():
                    if subkey not in data[key]:
                        data[key][subkey] = subdefault
                        
                    # Handle nested dictionaries one level deeper
                    if isinstance(subdefault, dict) and isinstance(data[key][subkey], dict):
                        for sub_subkey, sub_subdefault in subdefault.items():
                            if sub_subkey not in data[key][subkey]:
                                data[key][subkey][sub_subkey] = sub_subdefault


# Market prices for items and materials
MARKET_PRICES = {
    # Basic Materials
    "Wood": 5,
    "Iron Ore": 8,
    "Gold Ore": 15,
    "Red Herb": 3,
    "Water Flask": 2,
    "Leather": 4,
    "Steel Ingot": 12,
    "Magic Crystal": 20,

    # Crops and Seeds
    "Wheat": 8,
    "Corn": 12,
    "Tomato": 15,
    "Potato": 18,
    "Rice": 20,
    "Carrot": 12,
    "Lettuce": 8,
    "Strawberry": 18,

    # Monster Drops
    "Dragon Scale": 100,
    "Phoenix Feather": 200,
    "Wolf Pelt": 15,
    "Spider Silk": 10,
    "Spirit Essence": 25,
    "Soul Gem": 50,
    "Demon's Heart": 500,
    "Leviathan Scale": 400,

    # Common Equipment
    "Wooden Sword": 15,
    "Iron Sword": 40,
    "Steel Sword": 75,
    "Bone Armor": 20,
    "Iron Armor": 50,
    "Steel Armor": 90,

    # Rare Equipment
    "Flame Sword": 150,
    "Ice Sword": 150,
    "Shadow Blade": 475,
    "Dragon Armor": 425,
    "Samurai Armor": 650,
    "Cursed Katana": 750,

    # Legendary Equipment
    "Elder Wand": 400,
    "Vorpal Blade": 250,
    "Phoenix Plate": 300,
    "Mjolnir": 500,
    "Dragon Scale Armor": 425,
    "Iron Caliph's Crown": 1000,
}

def sell_item(item_name: str) -> None:
    if not item_name:
        print("Please specify an item to sell.")
        return

    # Case-insensitive search in inventory
    item = next((i for i in user_data["inventory"] if i.lower() == item_name.lower()), None)
    if not item:
        print(f"You don't have {item_name} in your inventory.")
        return

    # Check if item has a market price
    if item not in MARKET_PRICES:
        print("This item cannot be sold.")
        return

    # Remove from inventory and add gold
    user_data["inventory"].remove(item)
    price = MARKET_PRICES[item]
    user_data["gold"] += price
    print(f"Sold {item} for {price} gold.")

# Shop items
shop_items = [
    # === Basic Equipment ===
    {"name": "Wooden Sword", "type": "weapon", "effect": 5, "price": 30},
    {"name": "Iron Sword", "type": "weapon", "effect": 10, "price": 80},
    {"name": "Steel Sword", "type": "weapon", "effect": 15, "price": 150},
    {"name": "Bone Armor", "type": "armor", "effect": 5, "price": 40},
    {"name": "Iron Armor", "type": "armor", "effect": 10, "price": 100},
    {"name": "Steel Armor", "type": "armor", "effect": 15, "price": 180},
    {"name": "Bronze Dagger", "type": "weapon", "effect": 7, "price": 50},
    {"name": "Chainmail", "type": "armor", "effect": 8, "price": 75},

    # === Consumables ===
    {"name": "Healing Potion", "type": "consumable", "effect": 30, "price": 20},
    {"name": "Greater Healing Potion", "type": "consumable", "effect": 60, "price": 50},
    {"name": "Antidote", "type": "consumable", "effect": "cure_poison", "price": 25},
    {"name": "Mega Healing Potion", "type": "consumable", "effect": 60, "price": 50},
    {"name": "Mana Potion", "type": "consumable", "effect": 40, "price": 35},
    {"name": "Stamina Elixir", "type": "consumable", "effect": "restore_stamina", "price": 30},
    {"name": "Revival Herb", "type": "consumable", "effect": "revive", "price": 100},
    {"name": "Energy Drink", "type": "consumable", "effect": 25, "price": 15},

    # === Special Equipment ===
    {"name": "Magic Staff", "type": "weapon", "effect": 12, "price": 200},
    {"name": "Shadow Cloak", "type": "armor", "effect": 8, "price": 90},
    {"name": "Flame Dagger", "type": "weapon", "effect": 12, "price": 130},
    {"name": "Leather Armor", "type": "armor", "effect": 7, "price": 70},
    {"name": "Bow of the Eagle", "type": "weapon", "effect": 14, "price": 160},
    {"name": "Throwing Knife", "type": "weapon", "effect": 6, "price": 45},
    {"name": "Obsidian Greatsword", "type": "weapon", "effect": 18, "price": 220},
    {"name": "Dragonhide Vest", "type": "armor", "effect": 12, "price": 150},
    {"name": "Silver Rapier", "type": "weapon", "effect": 16, "price": 190},
    {"name": "Enchanted Robes", "type": "armor", "effect": 10, "price": 120},
    {"name": "Crossbow", "type": "weapon", "effect": 13, "price": 140},
    {"name": "Tower Shield", "type": "armor", "effect": 14, "price": 170},

    # === Exotic Equipment ===
    {"name": "Vorpal Blade", "type": "weapon", "effect": 25, "price": 500, "special": "Ignores armor"},
    {"name": "Phoenix Plate", "type": "armor", "effect": 20, "price": 600, "special": "Self-repair over time"},
    {"name": "Elder Wand", "type": "weapon", "effect": 30, "price": 800, "special": "Chance to cast spells for free"},
    {"name": "Cloak of Invisibility", "type": "armor", "effect": 15, "price": 700, "special": "Temporary stealth on use"},
    {"name": "Mjolnir", "type": "weapon", "effect": 35, "price": 1000, "special": "Lightning strikes on critical hits"},
    {"name": "Aegis of the Gods", "type": "armor", "effect": 25, "price": 900, "special": "Blocks all critical hits"},

    # === More Exotic Items from Monster Drops ===
    {"name": "Crimson Cutlass", "type": "weapon", "effect": 28, "price": 750, "special": "Bleeds enemies over time", "source": "Dreadlord Varkhull"},
    {"name": "Dragon Armor", "type": "armor", "effect": 22, "price": 850, "special": "Resistant to fire/ice/lightning", "source": "Dragon Knight"},
    {"name": "Undead Blade", "type": "weapon", "effect": 30, "price": 900, "special": "Life steal (10% of damage)", "source": "Undead Knight"},
    {"name": "Jade Crown", "type": "armor", "effect": 25, "price": 1200, "special": "+20% max HP", "source": "Jade Emperor"},
    {"name": "Shadow Blade", "type": "weapon", "effect": 32, "price": 950, "special": "Critical hits deal 3x damage", "source": "Shadow Samurai"},
    {"name": "Phoenix Feather", "type": "consumable", "effect": "full_revive", "price": 800, "special": "Revives with full HP", "source": "Phoenix"},
    {"name": "Cursed Katana", "type": "weapon", "effect": 40, "price": 1500, "special": "Deals self-damage (5% per hit)", "source": "Possessed Katana"},
    {"name": "Samurai Armor", "type": "armor", "effect": 30, "price": 1300, "special": "Counterattacks when hit", "source": "The Shogun"},
    {"name": "Kitsune Mask", "type": "armor", "effect": 18, "price": 700, "special": "Illusionary clones confuse enemies", "source": "Kitsune Warrior"},
    {"name": "Storm Eye", "type": "consumable", "effect": "summon_storm", "price": 600, "special": "Calls lightning on enemies (3 uses)", "source": "Vision of the Thunder"},
    {"name": "Frozen Soul", "type": "consumable", "effect": "freeze_enemies", "price": 500, "special": "Freezes all enemies for 1 turn", "source": "Hatred frozen soul"},
    
    # === Elemental Lord Equipment ===
    {"name": "Blazing Warhammer", "type": "weapon", "effect": 55, "price": 3500, "special": "Ignites enemies", "source": "Ignis, Lord of Flames", "element": "Ignis"},
    {"name": "Frost Giant's Axe", "type": "weapon", "effect": 52, "price": 3200, "special": "Slows enemies", "source": "Glacies, Frost Sovereign", "element": "Glacies"},
    {"name": "Storm Caller Staff", "type": "weapon", "effect": 48, "price": 3400, "special": "Chain lightning effect", "source": "Fulmen, Storm Emperor", "element": "Fulmen"},
    {"name": "Earthshaker Maul", "type": "weapon", "effect": 58, "price": 3600, "special": "Stuns enemies", "source": "Terra, Earth Colossus", "element": "Gē"},
    {"name": "Tidecaller Trident", "type": "weapon", "effect": 50, "price": 3300, "special": "Drowns enemies", "source": "Aquarius, Tide Master", "element": "Aqua"},
    
    {"name": "Inferno Plate", "type": "armor", "effect": 45, "price": 3800, "special": "Fire resistance", "source": "Ignis, Lord of Flames", "element": "Ignis"},
    {"name": "Glacier Mail", "type": "armor", "effect": 42, "price": 3500, "special": "Ice resistance", "source": "Glacies, Frost Sovereign", "element": "Glacies"},
    {"name": "Thunderstorm Garb", "type": "armor", "effect": 40, "price": 3600, "special": "Lightning resistance", "source": "Fulmen, Storm Emperor", "element": "Fulmen"},
    {"name": "Mountain's Heart Plate", "type": "armor", "effect": 48, "price": 3900, "special": "Earth resistance", "source": "Terra, Earth Colossus", "element": "Gē"},
    {"name": "Deep Sea Armor", "type": "armor", "effect": 43, "price": 3700, "special": "Water resistance", "source": "Aquarius, Tide Master", "element": "Aqua"},
    
    # === Four Horsemen Equipment ===
    {"name": "Victor's Bow", "type": "weapon", "effect": 65, "price": 8000, "special": "Always strikes first", "source": "Conquest, The White Rider", "element": "Lux"},
    {"name": "Warlord's Greatsword", "type": "weapon", "effect": 75, "price": 8500, "special": "Causes bleeding", "source": "War, The Red Rider", "element": "Ignis"},
    {"name": "Famine's Scythe", "type": "weapon", "effect": 70, "price": 8200, "special": "Drains life", "source": "Famine, The Black Rider", "element": "Gē"},
    {"name": "Death's Reaper", "type": "weapon", "effect": 85, "price": 9000, "special": "Instant death chance", "source": "Death, The Pale Rider", "element": "Nullum"},
    
    {"name": "Armor of Conquest", "type": "armor", "effect": 60, "price": 8200, "special": "Victory aura", "source": "Conquest, The White Rider", "element": "Lux"},
    {"name": "Blood-Soaked Plate", "type": "armor", "effect": 65, "price": 8500, "special": "Returns damage", "source": "War, The Red Rider", "element": "Ignis"},
    {"name": "Withering Mail", "type": "armor", "effect": 62, "price": 8300, "special": "Weakens attackers", "source": "Famine, The Black Rider", "element": "Gē"},
    {"name": "Shroud of the Reaper", "type": "armor", "effect": 70, "price": 9000, "special": "Fear aura", "source": "Death, The Pale Rider", "element": "Nullum"}
]

monsters = [
    # Greenwood Village Monsters (Level 1-2)
    {"name": "Goblin", "level": 1, "health": 50, "attack": 10, "drops": ["Gold Coin", "Wooden Sword"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Wolf", "level": 2, "health": 60, "attack": 12, "drops": ["Wolf Pelt", "Gold Coin"], "element": "Aer", "immunities": ["Aer"]},
    {"name": "Forest Spider", "level": 1, "health": 45, "attack": 8, "drops": ["Spider Silk", "Gold Coin"], "element": "Venēnum", "immunities": ["Venēnum"]},
    {"name": "Bandit", "level": 2, "health": 65, "attack": 14, "drops": ["Leather Armor", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Dire Wolf", "level": 2, "health": 70, "attack": 15, "drops": ["Wolf Fang", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Goblin Shaman", "level": 2, "health": 55, "attack": 13, "drops": ["Goblin Staff", "Gold Coin"], "boss": True, "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Goblin King", "level": 3, "health": 80, "attack": 20, "drops": ["Goblin Crown", "Gold Coin"], "boss": True, "element": "Gē", "immunities": ["Gē"]},

    # Added missing monsters
    {"name": "Dragon Whelp", "level": 4, "health": 100, "attack": 25, "drops": ["Dragon Scale", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Shadow Master", "level": 10, "health": 300, "attack": 60, "drops": ["Shadow Master's Cloak", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Blight Beast", "level": 7, "health": 180, "attack": 40, "drops": ["Blight Beast Claw", "Gold Coin"], "element": "Venēnum", "immunities": ["Venēnum"]},

    # Stormhaven Monsters (Level 2-3)
    {"name": "Skeleton", "level": 2, "health": 75, "attack": 15, "drops": ["Gold Coin", "Bone Armor"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Ghost", "level": 3, "health": 70, "attack": 18, "drops": ["Spirit Essence", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Storm Elemental", "level": 3, "health": 85, "attack": 20, "drops": ["Storm Crystal", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Pirate Scout", "level": 2, "health": 70, "attack": 16, "drops": ["Cutlass", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Haunted Armor", "level": 3, "health": 80, "attack": 22, "drops": ["Cursed Shield", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Sea Serpent", "level": 3, "health": 90, "attack": 25, "drops": ["Serpent Scale", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Dreadlord Varkhull, the Crimson Abyss Pirate Captain", "level": 5, "health": 150, "attack": 30, "drops": ["Crimson Cutlass", "Gold Coin"], "boss": True, "element": "Ferrum", "immunities": ["Ferrum"]},

    # Dragon's Peak Monsters (Level 5-6)
    {"name": "Fire Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Flame Sword"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Ice Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Ice Sword"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Electrical Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Lightning Sword"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Plant Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Nature Sword"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Earth Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Earth Sword"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Wind Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Wind Sword"], "element": "Aer", "immunities": ["Aer"]},
    {"name": "Water Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Water Sword"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Fire Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Ice Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Thunder Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Earth Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Dragon Knight", "level": 5, "health": 150, "attack": 28, "drops": ["Dragon Armor", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Water Wyvern", "level": 5, "health": 160, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Dragon Overlord", "level": 12, "health": 600, "attack": 90, "drops": ["Dragon Scale", "Dragonfire Sword", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis"]},

    # Crystal Cave Monsters (Level 3-4)
    {"name": "Crystal Golem", "level": 4, "health": 120, "attack": 25, "drops": ["Crystal Shard", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Cave Troll", "level": 4, "health": 130, "attack": 28, "drops": ["Troll Hide", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Crystal Spider", "level": 3, "health": 90, "attack": 22, "drops": ["Crystal Web", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Rock Elemental", "level": 4, "health": 140, "attack": 26, "drops": ["Earth Stone", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Cave Bat", "level": 3, "health": 80, "attack": 20, "drops": ["Bat Wing", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Crystal Tarantula", "level": 4, "health": 110, "attack": 24, "drops": ["Crystal Fang", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Crystal Giant Tarantula", "level": 7, "health": 200, "attack": 40, "drops": ["Crystal Eye", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Crystal Serpent", "level": 4, "health": 110, "attack": 24, "drops": ["Serpent Scale", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Corrupted Miner", "level": 4, "health": 115, "attack": 25, "drops": ["Miner's Pickaxe", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},

    # Shadowmere Monsters (Level 4-5)
    {"name": "Shadow Beast", "level": 4, "health": 110, "attack": 24, "drops": ["Shadow Essence", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Dark Knight", "level": 5, "health": 140, "attack": 28, "drops": ["Dark Armor", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Wraith", "level": 5, "health": 120, "attack": 30, "drops": ["Soul Gem", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Night Stalker", "level": 4, "health": 100, "attack": 26, "drops": ["Night Blade", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Shadow Assassin", "level": 5, "health": 130, "attack": 32, "drops": ["Assassin's Dagger", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Vampire", "level": 5, "health": 150, "attack": 35, "drops": ["Vampire Fang", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Undead Knight", "level": 5, "health": 160, "attack": 38, "drops": ["Undead Blade", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Undead Army General","level": 7, "health": 200, "attack": 40, "drops": ["Undead Armor", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Undead Army Commander","level": 8, "health": 250, "attack": 50, "drops": ["Undead's Blade", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},

    # Frostvale Monsters (Level 3-4)
    {"name": "Ice Troll", "level": 4, "health": 125, "attack": 26, "drops": ["Frozen Heart", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Frost Giant", "level": 4, "health": 140, "attack": 28, "drops": ["Giant's Club", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Snow Wolf", "level": 3, "health": 95, "attack": 20, "drops": ["Frost Pelt", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Ice Elemental", "level": 4, "health": 115, "attack": 24, "drops": ["Ice Crystal", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Frost Wraith", "level": 4, "health": 130, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Hatred frozen soul", "level": 5, "health": 150, "attack": 35, "drops": ["Frozen Soul", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Ice Revenant", "level": 5, "health": 160, "attack": 32, "drops": ["Frozen Heart", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Frost vengeful eye of the snow", "level": 7, "health": 200, "attack": 40, "drops": ["Frost Eye", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},

    # Long Shui Zhen Monsters (Level 4-8)
    {"name": "Dragon Spirit", "level": 5, "health": 130, "attack": 28, "drops": ["Spirit Pearl", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Water Elemental", "level": 4, "health": 110, "attack": 24, "drops": ["Water Essence", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Jade Warrior", "level": 5, "health": 140, "attack": 26, "drops": ["Jade Sword", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Jade General", "level": 5, "health": 150, "attack": 30, "drops": ["Jade Armor", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Jade soldier", "level": 4, "health": 120, "attack": 22, "drops": ["Jade Shield", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Jade Emperor's Guard", "level": 6, "health": 160, "attack": 32, "drops": ["Jade Shield", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    {"name": "Jade Emperor", "level": 8, "health": 390, "attack": 65, "drops": ["Jade Crown", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    {"name": "Legendary Dragon", "level": 8, "health": 400, "attack": 70, "drops": ["Dragon Scale", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},

    # Jade Lotus Village Monsters (Level 2-3)
    {"name": "Lotus Spirit", "level": 3, "health": 85, "attack": 18, "drops": ["Lotus Petal", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Pond Serpent", "level": 2, "health": 70, "attack": 16, "drops": ["Serpent Scale", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Garden Guardian", "level": 3, "health": 90, "attack": 20, "drops": ["Sacred Charm", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Lotus Guardian", "level": 3, "health": 95, "attack": 22, "drops": ["Lotus Shield", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Koi Empress", "level": 3, "health": 100, "attack": 24, "drops": ["Koi Scale", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},

    # Silent Ashes Monsters (Level 5-6)
    {"name": "Ash Revenant", "level": 6, "health": 160, "attack": 32, "drops": ["Revenant Ash", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Cursed Wanderer", "level": 5, "health": 140, "attack": 28, "drops": ["Cursed Relic", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Phoenix", "level": 6, "health": 180, "attack": 34, "drops": ["Phoenix Feather", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Ash Wraith", "level": 5, "health": 150, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Burnt Guardian", "level": 5, "health": 145, "attack": 29, "drops": ["Guardian's Ash", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Magmatic Knight,The fallen knight of the ashes", "level": 6, "health": 200, "attack": 40, "drops": ["Knight's Ash", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},

    # Thundercliff Hold Monsters (Level 4-5)
    {"name": "Thunder Elemental", "level": 5, "health": 130, "attack": 28, "drops": ["Storm Crystal", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Rock Wyvern", "level": 4, "health": 120, "attack": 26, "drops": ["Wyvern Scale", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Storm Hawk", "level": 4, "health": 110, "attack": 24, "drops": ["Hawk Feather", "Gold Coin"], "element": "Aer", "immunities": ["Aer"]},
    {"name": "Storm Wyvern", "level": 5, "health": 140, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Thunder Mage", "level": 5, "health": 150, "attack": 32, "drops": ["Thunder Staff", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Storm Guardian", "level": 5, "health": 160, "attack": 34, "drops": ["Guardian's Storm", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Vision of the Thunder,the core of the storm", "level": 5, "health": 150, "attack": 32, "drops": ["Storm Eye", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},

    # Shogunate Of Shirui Monsters (Level 5-12)
    {"name": "The Shogun", "level": 12, "health": 400, "attack": 70, "drops": ["Samurai Armor", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Shogun's Guard", "level": 8, "health": 350, "attack": 60, "drops": ["Shogun's Blade", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Jade Samurai", "level": 7, "health": 300, "attack": 50, "drops": ["Jade Armor", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Kitsune Warrior", "level": 6, "health": 250, "attack": 40, "drops": ["Kitsune Mask", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Tengu Warrior", "level": 6, "health": 240, "attack": 38, "drops": ["Tengu Feather", "Gold Coin"], "element": "Aer", "immunities": ["Aer"]},
    {"name": "Kappa Guardian", "level": 5, "health": 220, "attack": 35, "drops": ["Kappa Shell", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Oni Berserker", "level": 7, "health": 280, "attack": 45, "drops": ["Oni Mask", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Corrupted Ninja", "level": 5, "health": 200, "attack": 30, "drops": ["Ninja Star", "Gold Coin"], "element": "Venēnum", "immunities": ["Venēnum"]},
    {"name": "Shadow Samurai", "level": 6, "health": 260, "attack": 42, "drops": ["Shadow Blade", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Possessed Katana", "level": 5, "health": 210, "attack": 36, "drops": ["Cursed Katana", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},

    # The Iron Caliphate of Al-Khilafah Al-Hadidiyah Monsters (Level 7-12)
    {"name": "Az-Zālim al-Muqaddas,The Caliph of Al-Khilafah Al-Hadidiyah", "level": 12, "health": 500, "attack": 80, "drops": ["Iron Caliph's Crown", "Gold Coin"], "boss": True, "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Al-Hadidiyah Guardian", "level": 11, "health": 450, "attack": 75, "drops": ["Guardian's Blade", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Al-Hadidiyah Knight", "level": 10, "health": 400, "attack": 70, "drops": ["Knight's Shield", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Mercenary of the caliphate", "level": 9, "health": 350, "attack": 65, "drops": ["Mercenary's Dagger", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Loyalist of the caliphate", "level": 8, "health": 300, "attack": 60, "drops": ["Loyalist's Blade", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "High Priest of the caliphate", "level": 7, "health": 250, "attack": 55, "drops": ["High Priest's Staff", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    {"name": "Al-Hadidiyah Sorcerer", "level": 7, "health": 240, "attack": 50, "drops": ["Sorcerer's Tome", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Steel Golem", "level": 8, "health": 280, "attack": 60, "drops": ["Steel Core", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Royal Janissary", "level": 9, "health": 320, "attack": 65, "drops": ["Janissary's Blade", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Iron Caliphate General", "level": 10, "health": 370, "attack": 70, "drops": ["General's Armor", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},


    #  Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains Monsters (Level 7-12)
    {"name": "Tēcpatl Tlamacazqui,The Emperor of the Sacred Fire and Chains", "level": 12, "health": 550, "attack": 85, "drops": ["Emperor's Crown", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Secret Police from The Order of the Black Sun (Yohualli Tōnatiuh)", "level": 10, "health": 400, "attack": 70, "drops": ["Black Sun Dagger", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Knight", "level": 11, "health": 450, "attack": 75, "drops": ["Knight's Shield", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Guardian", "level": 9, "health": 350, "attack": 65, "drops": ["Guardian's Blade", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Sorcerer", "level": 8, "health": 300, "attack": 60, "drops": ["Sorcerer's Tome", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl High Priest", "level": 7, "health": 250, "attack": 55, "drops": ["High Priest's Staff", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Mercenary", "level": 9, "health": 320, "attack": 65, "drops": ["Mercenary's Dagger", "Gold Coin"], "element": "Ferrum", "immunities": ["Ferrum"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Loyalist", "level": 8, "health": 280, "attack": 60, "drops": ["Loyalist's Blade", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Royal Guard", "level": 10, "health": 370, "attack": 70, "drops": ["Royal Guard's Sword", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},

     # Crimson Abyss Monsters (Level 9-16)
    {"name": "Crimson Abyss Demon", "level": 15, "health": 600, "attack": 100, "drops": ["Demon's Heart", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Crimson Abyss Knight", "level": 14, "health": 550, "attack": 90, "drops": ["Knight's Blade", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Crimson Abyss Sorcerer", "level": 13, "health": 500, "attack": 80, "drops": ["Sorcerer's Staff", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Crimson Abyss Guardian", "level": 12, "health": 450, "attack": 75, "drops": ["Guardian's Shield", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Abyssal Leviathan", "level": 16, "health": 700, "attack": 120, "drops": ["Leviathan Scale", "Gold Coin"], "boss": True, "element": "Aqua", "immunities": ["Aqua"]},

    # The Dark Legion (Level 17-20)
    {"name": "Dark Legion Elite", "level": 17, "health": 800, "attack": 130, "drops": ["Dark Legion Armor", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Dark Legion Warlock", "level": 18, "health": 750, "attack": 140, "drops": ["Warlock Staff", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Dark Legion Commander", "level": 19, "health": 900, "attack": 150, "drops": ["Commander's Blade", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Dark Legion's Shadow Assassin", "level": 17, "health": 700, "attack": 160, "drops": ["Shadow Dagger", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Dark Legion Archpriest", "level": 18, "health": 850, "attack": 145, "drops": ["Dark Tome", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Dark Legionary Supreme Lord:Noctis, the Obsidian Fallen Eternal", 
 "level": 20, 
 "health": 2000, 
 "attack": 250, 
 "drops": ["Eternal Crown", "Obsidian Blade", "Dark Legion's Heart", "Gold Coin", "Noctis's Soul"], 
 "boss": True,
 "special_abilities": {
     "Dark Oblivion": {"damage": 400, "effect": "health_drain"},
     "Shadow Legion": {"effect": "summon_minions", "minions": ["Dark Legion Elite", "Dark Legion Warlock"]},
     "Eternal Darkness": {"effect": "damage_reduction", "duration": 3},
     "Obsidian Shield": {"effect": "reflect_damage", "duration": 2}
 },
 "phases": 3,
 "phase_triggers": [0.7, 0.3],  # Triggers at 70% and 30% health
 "unique_mechanics": True,
 "description": "The supreme ruler of the Dark Legion, wielding powers of eternal darkness and commanding legions of the fallen. Each phase unleashes new devastating abilities."
},
    {"name": "Dark Legion's Shadow Knight", "level": 19, "health": 950, "attack": 170, "drops": ["Shadow Knight's Blade", "Gold Coin"]},
    {"name": "Dark Legion's Shadow Sorcerer", "level": 18, "health": 800, "attack": 160, "drops": ["Shadow Sorcerer's Staff", "Gold Coin"]},
    {"name": "Dark Legion's Shadow Guardian", "level": 17, "health": 750, "attack": 150, "drops": ["Shadow Guardian's Shield", "Gold Coin"]},

    # Post-game dungeon monsters
    {"name": "Void Reaper", "level": 25, "health": 2500, "attack": 300, "drops": ["Void Scythe", "Void Crystal", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Ancient Dragon God", "level": 30, "health": 3000, "attack": 400, "drops": ["Divine Dragon Scale", "Dragon God's Crown", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Eternal Phoenix", "level": 28, "health": 2800, "attack": 350, "drops": ["Eternal Flame", "Phoenix Crown", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Aqua"]},
    {"name": "Chaos Incarnate", "level": 35, "health": 3500, "attack": 450, "drops": ["Chaos Blade", "Chaos Crystal", "Gold Coin"], "boss": True, "element": "Nullum", "immunities": []},
    {"name": "Abyssal Overlord", "level": 40, "health": 4000, "attack": 500, "drops": ["Abyssal Crown", "Infinity Stone", "Gold Coin"], "boss": True, "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Dragon Elite Guard", "level": 32, "health": 3200, "attack": 420, "drops": ["Elite Dragon Scale", "Dragon Guard Armor", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Phoenix Guardian", "level": 30, "health": 3000, "attack": 380, "drops": ["Phoenix Feather", "Guardian's Flame", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Chaos Spawn", "level": 33, "health": 3300, "attack": 430, "drops": ["Chaos Shard", "Spawn Crystal", "Gold Coin"], "element": "Nullum", "immunities": []},
    {"name": "Abyss Dweller", "level": 38, "health": 3800, "attack": 480, "drops": ["Dweller's Heart", "Abyssal Fragment", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Void Dragon", "level": 45, "health": 5000, "attack": 600, "drops": ["Void Dragon Scale", "Void Crown", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae", "Lux"]},
    
    # New Mid-Level Bosses (15-25)
    {"name": "Archmage Zephyrius", "level": 15, "health": 800, "attack": 120, "drops": ["Zephyr Staff", "Wind Crystal", "Gold Coin"], "boss": True, "element": "Pneuma", "immunities": ["Pneuma"], "special_ability": "Summons tornadoes that deal area damage"},
    {"name": "Warlord Magmar", "level": 18, "health": 950, "attack": 140, "drops": ["Magma Battleaxe", "Molten Core", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis"], "special_ability": "Enrages at low health, increasing attack by 50%"},
    {"name": "Lady Crystallia", "level": 20, "health": 1100, "attack": 150, "drops": ["Crystal Scepter", "Diamond Heart", "Gold Coin"], "boss": True, "element": "Gē", "immunities": ["Gē"], "special_ability": "Creates crystal shields that must be broken first"},
    {"name": "Admiral Hydros", "level": 22, "health": 1250, "attack": 160, "drops": ["Trident of the Deep", "Abyssal Pearl", "Gold Coin"], "boss": True, "element": "Aqua", "immunities": ["Aqua"], "special_ability": "Summons tidal waves that push players back"},
    {"name": "Necrolord Morbius", "level": 25, "health": 1400, "attack": 175, "drops": ["Death's Embrace", "Soul Gem", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae"], "special_ability": "Resurrects fallen minions to fight alongside him"},
    
    # New High-Level Bosses (35-50)
    {"name": "The Celestial Arbiter", "level": 35, "health": 3500, "attack": 300, "drops": ["Astral Judgment", "Star Fragment", "Gold Coin"], "boss": True, "element": "Lux", "immunities": ["Lux"], "special_ability": "Can banish players temporarily from battle"},
    {"name": "Queen Titania of the Fae", "level": 38, "health": 3800, "attack": 320, "drops": ["Titania's Blessing", "Fae Crown", "Gold Coin"], "boss": True, "element": "Vita", "immunities": ["Vita"], "special_ability": "Charms players to fight for her temporarily"},
    {"name": "Overlord Infernus", "level": 40, "health": 4200, "attack": 350, "drops": ["Infernal Mantle", "Demon's Heart", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis", "Aqua"], "special_ability": "Sets the battlefield ablaze, causing damage over time"},
    {"name": "The World Serpent", "level": 45, "health": 4800, "attack": 380, "drops": ["Serpent Scale Mail", "Primordial Fang", "Gold Coin"], "boss": True, "element": "Venēnum", "immunities": ["Venēnum", "Gē"], "special_ability": "Coils around players, reducing their movement and attack speed"},
    {"name": "Chronos, Master of Time", "level": 48, "health": 5200, "attack": 400, "drops": ["Timekeeper's Watch", "Crystallized Time", "Gold Coin"], "boss": True, "element": "Nullum", "immunities": ["Nullum"], "special_ability": "Can rewind time to heal himself or reset player abilities"},
    
    # Ultimate Bosses (50+)
    {"name": "The Void Empress", "level": 50, "health": 6000, "attack": 500, "drops": ["Void Empress Crown", "Black Hole Core", "Void-Touched Weapon", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae", "Lux", "Pneuma"], "special_ability": "Creates zones of emptiness that nullify all abilities"},
    {"name": "Primal Elemental Titan", "level": 55, "health": 7000, "attack": 550, "drops": ["Primal Essence", "Elemental Heart", "Titan's Greatsword", "Gold Coin"], "boss": True, "element": "Nullum", "immunities": [], "special_ability": "Changes elemental affinity throughout battle"},
    {"name": "Xal'gathoth, The Unknowable", "level": 60, "health": 8000, "attack": 600, "drops": ["Maddening Whisper", "Tentacle of the Deep", "Xal'gathoth's Eye", "Gold Coin"], "boss": True, "element": "Nullum", "immunities": ["Tenebrae", "Lux"], "special_ability": "Induces insanity in players, causing them to attack allies"},
    {"name": "The Worldbreaker", "level": 70, "health": 10000, "attack": 700, "drops": ["Worldbreaker Fragment", "Cosmic Shard", "Reality-Warping Gauntlet", "Gold Coin"], "boss": True, "element": "Nullum", "immunities": ["Ignis", "Aqua", "Pneuma", "Gē", "Lux", "Tenebrae"], "special_ability": "Can destroy parts of reality, removing player abilities temporarily"},
    {"name": "Time Keeper", "level": 42, "health": 4500, "attack": 550, "drops": ["Chronos Crystal", "Time Keeper's Staff", "Gold Coin"], "boss": True, "element": "Aer", "immunities": ["Aer"]},
    {"name": "Celestial Titan", "level": 48, "health": 5500, "attack": 650, "drops": ["Celestial Heart", "Titan's Crown", "Gold Coin"], "boss": True, "element": "Lux", "immunities": ["Lux"]},
    {"name": "Dimensional Horror", "level": 50, "health": 6000, "attack": 700, "drops": ["Horror Essence", "Dimensional Shard", "Gold Coin"], "boss": True, "element": "Tenebrae", "immunities": ["Tenebrae", "Lux"]},
    
    # New Elemental Lords bosses
    {"name": "Ignis, Lord of Flames", "level": 38, "health": 3800, "attack": 480, "drops": ["Heart of Fire", "Blazing Crown", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Glacies, Frost Sovereign", "level": 38, "health": 3800, "attack": 460, "drops": ["Core of Ice", "Frozen Crown", "Gold Coin"], "boss": True, "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Fulmen, Storm Emperor", "level": 38, "health": 3700, "attack": 490, "drops": ["Lightning Heart", "Storm Crown", "Gold Coin"], "boss": True, "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Terra, Earth Colossus", "level": 38, "health": 4000, "attack": 450, "drops": ["Earth Core", "Mountain Crown", "Gold Coin"], "boss": True, "element": "Gē", "immunities": ["Gē"]},
    {"name": "Aquarius, Tide Master", "level": 38, "health": 3800, "attack": 470, "drops": ["Ocean Heart", "Coral Crown", "Gold Coin"], "boss": True, "element": "Aqua", "immunities": ["Aqua"]},
    
    # Four Horsemen boss series
    {"name": "Conquest, The White Rider", "level": 52, "health": 5500, "attack": 700, "drops": ["White Bow", "Victor's Crown", "Gold Coin"], "boss": True, "element": "Lux", "immunities": ["Lux", "Tenebrae"]},
    {"name": "War, The Red Rider", "level": 54, "health": 5800, "attack": 750, "drops": ["Bloodthirsty Blade", "Warlord's Crown", "Gold Coin"], "boss": True, "element": "Ignis", "immunities": ["Ignis", "Aqua"]},
    {"name": "Famine, The Black Rider", "level": 56, "health": 6000, "attack": 720, "drops": ["Scales of Balance", "Crown of Hunger", "Gold Coin"], "boss": True, "element": "Gē", "immunities": ["Gē", "Viridia"]},
    {"name": "Death, The Pale Rider", "level": 60, "health": 7000, "attack": 800, "drops": ["Soul Scythe", "Pale Crown", "Gold Coin", "Final Judgment"], "boss": True, "element": "Nullum", "immunities": ["Tenebrae", "Lux"]},
    
    # New minions for elemental lords and horsemen
    {"name": "Winter Wolf", "level": 34, "health": 3400, "attack": 400, "drops": ["Wolf Fang", "Frost Crystal", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"]},
    {"name": "Lightning Elemental", "level": 34, "health": 3300, "attack": 420, "drops": ["Charged Crystal", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Stone Golem", "level": 34, "health": 3600, "attack": 380, "drops": ["Ancient Fossil", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Celestial Warrior", "level": 48, "health": 4800, "attack": 580, "drops": ["Celestial Armor", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    {"name": "Blood Knight", "level": 50, "health": 5000, "attack": 620, "drops": ["Blood-Stained Armor", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Withered Guardian", "level": 52, "health": 5200, "attack": 630, "drops": ["Life Essence", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Reaper's Assistant", "level": 56, "health": 5600, "attack": 680, "drops": ["Soul Fragment", "Gold Coin"], "element": "Tenebrae", "immunities": ["Tenebrae"]},
    {"name": "Temporal Guardian", "level": 40, "health": 4000, "attack": 500, "drops": ["Paradox Shard", "Gold Coin"], "element": "Aer", "immunities": ["Aer"]},
    {"name": "Astral Entity", "level": 44, "health": 4400, "attack": 550, "drops": ["Star Fragment", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]},
    
    # Weather-dependent monsters
    {"name": "Lightning Wyvern", "level": 20, "health": 1200, "attack": 180, "drops": ["Storm Scale", "Lightning Crystal", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"], "weather": "Stormy"},
    {"name": "Mist Wraith", "level": 18, "health": 900, "attack": 150, "drops": ["Ethereal Essence", "Ghost Cloth", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"], "weather": "Foggy"},
    {"name": "Blizzard Beast", "level": 22, "health": 1300, "attack": 190, "drops": ["Frozen Heart", "Ice Crystal", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"], "weather": "Snowy"},
    {"name": "Sunlight Elemental", "level": 21, "health": 1100, "attack": 170, "drops": ["Radiant Core", "Bright Crystal", "Gold Coin"], "element": "Lux", "immunities": ["Lux"], "weather": "Sunny"},
    {"name": "Gale Harpy", "level": 19, "health": 950, "attack": 160, "drops": ["Razor Feather", "Wind Crystal", "Gold Coin"], "element": "Aer", "immunities": ["Aer"], "weather": "Windy"},
    {"name": "Mud Golem", "level": 20, "health": 1250, "attack": 165, "drops": ["Clay Core", "Mud Stone", "Gold Coin"], "element": "Gē", "immunities": ["Gē"], "weather": "Rainy"},
    {"name": "Cloud Skimmer", "level": 19, "health": 980, "attack": 155, "drops": ["Cloud Fragment", "Sky Essence", "Gold Coin"], "element": "Aer", "immunities": ["Aer"], "weather": "Cloudy"},
    
    # Seasonal monsters
    {"name": "Winter Frost Monarch", "level": 25, "health": 1500, "attack": 200, "drops": ["Frost Crown", "Winter Essence", "Gold Coin"], "element": "Glacies", "immunities": ["Glacies"], "season": "Winter"},
    {"name": "Spring Bloom Guardian", "level": 24, "health": 1400, "attack": 190, "drops": ["Petal Crown", "Spring Essence", "Gold Coin"], "element": "Viridia", "immunities": ["Viridia"], "season": "Spring"},
    {"name": "Summer Flame Salamander", "level": 26, "health": 1550, "attack": 210, "drops": ["Burning Scale", "Summer Essence", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"], "season": "Summer"},
    {"name": "Autumn Harvest Keeper", "level": 25, "health": 1450, "attack": 195, "drops": ["Harvest Crown", "Autumn Essence", "Gold Coin"], "element": "Gē", "immunities": ["Gē"], "season": "Autumn"},
    
    # Farming quest monsters
    {"name": "Gargantuan Turnip", "level": 15, "health": 500, "attack": 80, "drops": ["Giant Turnip Seeds", "Vegetable Essence", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Crop Devourer", "level": 18, "health": 800, "attack": 120, "drops": ["Fertilizer", "Pest Control", "Gold Coin"], "element": "Venēnum", "immunities": ["Venēnum"]},
    {"name": "Soil Defiler", "level": 20, "health": 900, "attack": 150, "drops": ["Purified Soil", "Earth Crystal", "Gold Coin"], "element": "Gē", "immunities": ["Gē"]},
    {"name": "Phantom Scarecrow", "level": 22, "health": 1000, "attack": 170, "drops": ["Enchanted Straw", "Fear Essence", "Gold Coin"], "element": "Pneuma", "immunities": ["Pneuma"]},
    {"name": "Berry Behemoth", "level": 16, "health": 600, "attack": 100, "drops": ["Giant Berry Seeds", "Fruit Essence", "Gold Coin"], "element": "Viridia", "immunities": ["Viridia"]},
    
    # Elemental infusion monsters
    {"name": "Thunderstruck Wolf", "level": 28, "health": 1700, "attack": 230, "drops": ["Charged Pelt", "Shock Fang", "Gold Coin"], "element": "Fulmen", "immunities": ["Fulmen"]},
    {"name": "Molten Spider", "level": 27, "health": 1600, "attack": 220, "drops": ["Heat-resistant Silk", "Lava Venom", "Gold Coin"], "element": "Ignis", "immunities": ["Ignis"]},
    {"name": "Abyssal Crab", "level": 29, "health": 1800, "attack": 240, "drops": ["Deep Sea Shell", "Pressure Crystal", "Gold Coin"], "element": "Aqua", "immunities": ["Aqua"]},
    {"name": "Crystal Serpent", "level": 30, "health": 1900, "attack": 250, "drops": ["Crystal Scale", "Prismatic Essence", "Gold Coin"], "element": "Lux", "immunities": ["Lux"]}
]

# Post-game dungeons will be added to the dungeons list after its definition



ACHIEVEMENTS = {
    "First Steps": {"desc": "Create your character", "reward": {"gold": 100}},
    "Monster Hunter": {"desc": "Kill 100 monsters", "reward": {"gold": 500}},
    "Dragon Slayer": {"desc": "Kill any dragon", "reward": {"exp": 1000}},
    "Master Crafter": {"desc": "Craft 50 items", "reward": {"gold": 1000}},
    "Dungeon Master": {"desc": "Complete all dungeons", "reward": {"gold": 5000}},
    "Legendary Hero": {"desc": "Reach level 50", "reward": {"gold": 10000}},
    "Material Master": {"desc": "Collect all materials", "reward": {"gold": 2000}},
    "Rich Merchant": {"desc": "Accumulate 100000 gold", "reward": {"exp": 5000}},
    "Pet Collector": {"desc": "Adopt 5 pets", "reward": {"gold": 1500}},
    "Master Farmer": {"desc": "Harvest 1000 crops", "reward": {"gold": 3000}}
}

# Track achievement progress
def check_achievements():
    """
    Enhanced achievement system with tiers, categories, and visual feedback
    """
    # Initialize achievements structure if not exists
    if "achievements" not in user_data:
        user_data["achievements"] = {
            "unlocked": [],
            "progress": {
                "monsters_killed": 0,
                "items_crafted": 0,
                "dungeons_completed": 0,
                "crops_harvested": 0,
                "bosses_defeated": 0,
                "quests_completed": 0,
                "areas_visited": set(),
                "max_damage_dealt": 0,
                "total_gold_earned": 0,
                "rare_items_found": 0,
                "critical_hits": 0,
                "combo_finishers": 0,
                "skills_used": 0,
                "items_collected": 0,
                "potions_used": 0,
                "deaths": 0,
                "enemies_dodged": 0,
                "gold_spent": 0,
                "distance_traveled": 0,
                "treasure_chests_opened": 0
            }
        }

    # Update current achievement progress based on user_data
    update_achievement_progress()

    # Define all achievements with requirements, rewards, and categories
    ACHIEVEMENTS = [
        # Combat Achievements - Tier 1
        {
            "id": "first_blood",
            "name": "First Blood",
            "description": "Defeat your first monster",
            "category": "Combat",
            "tier": 1,
            "requirement": {"monsters_killed": 1},
            "reward": {"gold": 50, "exp": 100},
            "icon": "🗡️"
        },
        {
            "id": "monster_hunter",
            "name": "Monster Hunter",
            "description": "Defeat 100 monsters",
            "category": "Combat",
            "tier": 2,
            "requirement": {"monsters_killed": 100},
            "reward": {"gold": 500, "exp": 500, "stat_bonus": {"attack": 2}},
            "icon": "⚔️"
        },
        {
            "id": "monster_slayer",
            "name": "Monster Slayer",
            "description": "Defeat 500 monsters",
            "category": "Combat",
            "tier": 3,
            "requirement": {"monsters_killed": 500},
            "reward": {"gold": 2000, "exp": 2000, "stat_bonus": {"attack": 5}},
            "icon": "🛡️"
        },
        {
            "id": "legendary_hunter",
            "name": "Legendary Hunter",
            "description": "Defeat 1000 monsters",
            "category": "Combat",
            "tier": 4,
            "requirement": {"monsters_killed": 1000},
            "reward": {"gold": 5000, "exp": 5000, "stat_bonus": {"attack": 10, "defense": 5}, "item": "Hunter's Trophy"},
            "icon": "🏆"
        },
        
        # Boss Achievements
        {
            "id": "boss_challenge",
            "name": "Boss Challenger",
            "description": "Defeat your first boss",
            "category": "Combat",
            "tier": 1,
            "requirement": {"bosses_defeated": 1},
            "reward": {"gold": 200, "exp": 300},
            "icon": "👺"
        },
        {
            "id": "boss_slayer",
            "name": "Boss Slayer",
            "description": "Defeat 5 different bosses",
            "category": "Combat",
            "tier": 2,
            "requirement": {"bosses_defeated": 5},
            "reward": {"gold": 1000, "exp": 1500, "stat_bonus": {"attack": 3, "defense": 3}},
            "icon": "👹"
        },
        {
            "id": "boss_master",
            "name": "Boss Master",
            "description": "Defeat 15 different bosses",
            "category": "Combat",
            "tier": 3,
            "requirement": {"bosses_defeated": 15},
            "reward": {"gold": 3000, "exp": 4000, "stat_bonus": {"attack": 7, "defense": 7}, "item": "Boss Master's Crown"},
            "icon": "👑"
        },
        
        # Skill Achievements
        {
            "id": "skill_novice",
            "name": "Skill Novice",
            "description": "Use skills 50 times",
            "category": "Combat",
            "tier": 1,
            "requirement": {"skills_used": 50},
            "reward": {"exp": 200, "stat_bonus": {"intellect": 2}},
            "icon": "✨"
        },
        {
            "id": "skill_adept",
            "name": "Skill Adept",
            "description": "Use skills 200 times",
            "category": "Combat",
            "tier": 2,
            "requirement": {"skills_used": 200},
            "reward": {"exp": 800, "stat_bonus": {"intellect": 5}},
            "icon": "💫"
        },
        {
            "id": "skill_master",
            "name": "Skill Master",
            "description": "Use skills 500 times",
            "category": "Combat",
            "tier": 3,
            "requirement": {"skills_used": 500},
            "reward": {"exp": 2000, "stat_bonus": {"intellect": 10}, "item": "Spellbinder's Tome"},
            "icon": "🌟"
        },
        
        # Combo Achievements
        {
            "id": "combo_striker",
            "name": "Combo Striker",
            "description": "Perform 10 combo finishers",
            "category": "Combat",
            "tier": 1,
            "requirement": {"combo_finishers": 10},
            "reward": {"exp": 300, "stat_bonus": {"speed": 2}},
            "icon": "🔄"
        },
        {
            "id": "combo_artist",
            "name": "Combo Artist",
            "description": "Perform 50 combo finishers",
            "category": "Combat",
            "tier": 2,
            "requirement": {"combo_finishers": 50},
            "reward": {"exp": 1000, "stat_bonus": {"speed": 5, "attack": 3}},
            "icon": "⚡"
        },
        {
            "id": "combo_master",
            "name": "Combo Master",
            "description": "Perform 150 combo finishers",
            "category": "Combat",
            "tier": 3,
            "requirement": {"combo_finishers": 150},
            "reward": {"exp": 3000, "stat_bonus": {"speed": 10, "attack": 7}, "item": "Combo Master's Gloves"},
            "icon": "🌪️"
        },
        
        # Critical Hit Achievements
        {
            "id": "critical_striker",
            "name": "Critical Striker",
            "description": "Land 25 critical hits",
            "category": "Combat",
            "tier": 1,
            "requirement": {"critical_hits": 25},
            "reward": {"exp": 200, "stat_bonus": {"critical_chance": 0.02}},
            "icon": "❗"
        },
        {
            "id": "critical_expert",
            "name": "Critical Expert",
            "description": "Land 100 critical hits",
            "category": "Combat",
            "tier": 2,
            "requirement": {"critical_hits": 100},
            "reward": {"exp": 800, "stat_bonus": {"critical_chance": 0.05}},
            "icon": "💢"
        },
        {
            "id": "critical_master",
            "name": "Critical Master",
            "description": "Land 250 critical hits",
            "category": "Combat",
            "tier": 3,
            "requirement": {"critical_hits": 250},
            "reward": {"exp": 2000, "stat_bonus": {"critical_chance": 0.1}, "item": "Precision Scope"},
            "icon": "💥"
        },
        
        # Wealth Achievements
        {
            "id": "gold_collector",
            "name": "Gold Collector",
            "description": "Earn 1,000 gold",
            "category": "Wealth",
            "tier": 1,
            "requirement": {"total_gold_earned": 1000},
            "reward": {"exp": 200, "stat_bonus": {"charisma": 2}},
            "icon": "💰"
        },
        {
            "id": "wealthy",
            "name": "Wealthy",
            "description": "Earn 10,000 gold",
            "category": "Wealth",
            "tier": 2,
            "requirement": {"total_gold_earned": 10000},
            "reward": {"exp": 1000, "stat_bonus": {"charisma": 5}},
            "icon": "💎"
        },
        {
            "id": "rich",
            "name": "Rich",
            "description": "Earn 50,000 gold",
            "category": "Wealth",
            "tier": 3,
            "requirement": {"total_gold_earned": 50000},
            "reward": {"exp": 3000, "stat_bonus": {"charisma": 10}, "item": "Golden Monocle"},
            "icon": "👑"
        },
        {
            "id": "millionaire",
            "name": "Millionaire",
            "description": "Earn 100,000 gold",
            "category": "Wealth",
            "tier": 4,
            "requirement": {"total_gold_earned": 100000},
            "reward": {"exp": 10000, "stat_bonus": {"charisma": 20}, "item": "Midas Touch Gloves"},
            "icon": "🏛️"
        },
        
        # Experience Achievements
        {
            "id": "level_up",
            "name": "Level Up",
            "description": "Reach level 5",
            "category": "Experience",
            "tier": 1,
            "requirement": lambda: user_data["level"] >= 5,
            "reward": {"gold": 100, "stat_bonus": {"health": 10}},
            "icon": "📈"
        },
        {
            "id": "adventurer",
            "name": "Adventurer",
            "description": "Reach level 10",
            "category": "Experience",
            "tier": 2,
            "requirement": lambda: user_data["level"] >= 10,
            "reward": {"gold": 500, "stat_bonus": {"health": 20, "attack": 2, "defense": 2}},
            "icon": "🌄"
        },
        {
            "id": "hero",
            "name": "Hero",
            "description": "Reach level 25",
            "category": "Experience",
            "tier": 3,
            "requirement": lambda: user_data["level"] >= 25,
            "reward": {"gold": 2000, "stat_bonus": {"health": 50, "attack": 5, "defense": 5}},
            "icon": "🦸"
        },
        {
            "id": "legend",
            "name": "Legend",
            "description": "Reach level 50",
            "category": "Experience",
            "tier": 4,
            "requirement": lambda: user_data["level"] >= 50,
            "reward": {"gold": 5000, "stat_bonus": {"health": 100, "attack": 10, "defense": 10}, "item": "Legendary Cape"},
            "icon": "🌟"
        },
        
        # Exploration Achievements
        {
            "id": "explorer_novice",
            "name": "Explorer Novice",
            "description": "Visit 3 different locations",
            "category": "Exploration",
            "tier": 1,
            "requirement": lambda: len(user_data.get("visited_locations", [])) >= 3,
            "reward": {"exp": 200, "stat_bonus": {"speed": 1}},
            "icon": "🧭"
        },
        {
            "id": "traveler",
            "name": "Traveler",
            "description": "Visit 7 different locations",
            "category": "Exploration",
            "tier": 2,
            "requirement": lambda: len(user_data.get("visited_locations", [])) >= 7,
            "reward": {"exp": 500, "gold": 300, "stat_bonus": {"speed": 3}},
            "icon": "🗺️"
        },
        {
            "id": "explorer",
            "name": "Explorer",
            "description": "Visit 12 different locations",
            "category": "Exploration",
            "tier": 3,
            "requirement": lambda: len(user_data.get("visited_locations", [])) >= 12,
            "reward": {"exp": 1500, "gold": 800, "stat_bonus": {"speed": 6}, "item": "Explorer's Boots"},
            "icon": "🌍"
        },
        {
            "id": "world_traveler",
            "name": "World Traveler",
            "description": "Visit all locations in the world",
            "category": "Exploration",
            "tier": 4,
            "requirement": lambda: len(user_data.get("visited_locations", [])) >= 20,  # Assuming 20 total locations
            "reward": {"exp": 3000, "gold": 2000, "stat_bonus": {"speed": 10, "charisma": 5}, "item": "World Map"},
            "icon": "🌐"
        },
        
        # Collection Achievements
        {
            "id": "collector",
            "name": "Item Collector",
            "description": "Collect 25 different items",
            "category": "Collection",
            "tier": 1,
            "requirement": lambda: len(set(user_data.get("all_collected_items", []))) >= 25,
            "reward": {"gold": 200, "exp": 300},
            "icon": "🧰"
        },
        {
            "id": "treasure_hunter",
            "name": "Treasure Hunter",
            "description": "Open 10 treasure chests",
            "category": "Collection",
            "tier": 2,
            "requirement": {"treasure_chests_opened": 10},
            "reward": {"gold": 500, "exp": 700},
            "icon": "🗝️"
        },
        {
            "id": "hoarder",
            "name": "Hoarder",
            "description": "Collect 100 different items",
            "category": "Collection",
            "tier": 3,
            "requirement": lambda: len(set(user_data.get("all_collected_items", []))) >= 100,
            "reward": {"gold": 1500, "exp": 2000, "item": "Collector's Bag"},
            "icon": "🎒"
        },
        
        # Crafting Achievements
        {
            "id": "apprentice_crafter",
            "name": "Apprentice Crafter",
            "description": "Craft 10 items",
            "category": "Crafting",
            "tier": 1,
            "requirement": {"items_crafted": 10},
            "reward": {"exp": 200, "stat_bonus": {"crafting": 2}},
            "icon": "🔨"
        },
        {
            "id": "skilled_artisan",
            "name": "Skilled Artisan",
            "description": "Craft 25 items",
            "category": "Crafting",
            "tier": 2,
            "requirement": {"items_crafted": 25},
            "reward": {"exp": 500, "stat_bonus": {"crafting": 5}},
            "icon": "⚒️"
        },
        {
            "id": "master_crafter",
            "name": "Master Crafter",
            "description": "Craft 50 items",
            "category": "Crafting",
            "tier": 3,
            "requirement": {"items_crafted": 50},
            "reward": {"exp": 1500, "stat_bonus": {"crafting": 10}, "item": "Artisan's Tools"},
            "icon": "🛠️"
        },
        
        # Quest Achievements
        {
            "id": "quest_beginner",
            "name": "Quest Beginner",
            "description": "Complete 3 quests",
            "category": "Quests",
            "tier": 1,
            "requirement": {"quests_completed": 3},
            "reward": {"exp": 300},
            "icon": "📜"
        },
        {
            "id": "quest_taker",
            "name": "Quest Taker",
            "description": "Complete 10 quests",
            "category": "Quests",
            "tier": 2,
            "requirement": {"quests_completed": 10},
            "reward": {"exp": 800, "gold": 500},
            "icon": "📝"
        },
        {
            "id": "quest_master",
            "name": "Quest Master",
            "description": "Complete 25 quests",
            "category": "Quests",
            "tier": 3,
            "requirement": {"quests_completed": 25},
            "reward": {"exp": 2000, "gold": 1500, "item": "Quest Master's Journal"},
            "icon": "📚"
        },
        
        # Dungeon Achievements
        {
            "id": "dungeon_novice",
            "name": "Dungeon Novice",
            "description": "Complete your first dungeon",
            "category": "Dungeons",
            "tier": 1,
            "requirement": {"dungeons_completed": 1},
            "reward": {"exp": 300, "gold": 200},
            "icon": "🏰"
        },
        {
            "id": "dungeon_explorer",
            "name": "Dungeon Explorer",
            "description": "Complete 5 different dungeons",
            "category": "Dungeons",
            "tier": 2,
            "requirement": {"dungeons_completed": 5},
            "reward": {"exp": 1000, "gold": 800, "stat_bonus": {"defense": 3}},
            "icon": "🔍"
        },
        {
            "id": "dungeon_master",
            "name": "Dungeon Master",
            "description": "Complete 15 different dungeons",
            "category": "Dungeons",
            "tier": 3,
            "requirement": {"dungeons_completed": 15},
            "reward": {"exp": 3000, "gold": 2000, "stat_bonus": {"defense": 8}, "item": "Dungeon Key"},
            "icon": "🔑"
        },
        
        # Survival Achievements
        {
            "id": "survivor",
            "name": "Survivor",
            "description": "Survive 10 near-death experiences (below 10% health)",
            "category": "Survival",
            "tier": 2,
            "requirement": lambda: user_data.get("near_death_escapes", 0) >= 10,
            "reward": {"exp": 1000, "stat_bonus": {"health": 10, "defense": 3}},
            "icon": "❤️‍🩹"
        },
        {
            "id": "potion_master",
            "name": "Potion Master",
            "description": "Use 50 potions",
            "category": "Survival",
            "tier": 2,
            "requirement": {"potions_used": 50},
            "reward": {"exp": 500, "stat_bonus": {"health": 5}},
            "icon": "🧪"
        },
        {
            "id": "dodge_expert",
            "name": "Dodge Expert",
            "description": "Dodge 100 enemy attacks",
            "category": "Survival",
            "tier": 3,
            "requirement": {"enemies_dodged": 100},
            "reward": {"exp": 2000, "stat_bonus": {"speed": 8}, "item": "Shadow Step Boots"},
            "icon": "💨"
        }
    ]
    
    # Check each achievement
    newly_unlocked = []
    
    for achievement in ACHIEVEMENTS:
        achievement_id = achievement["id"]
        
        # Skip if already unlocked
        if achievement_id in user_data["achievements"]["unlocked"]:
            continue
            
        # Check if achievement is unlocked based on requirement
        requirement_met = False
        
        # Handle lambda requirements (custom conditions)
        if callable(achievement.get("requirement")):
            requirement_met = achievement["requirement"]()
        # Handle dict requirements (stat-based conditions)
        elif isinstance(achievement.get("requirement"), dict):
            requirement_met = True
            for stat, required_value in achievement["requirement"].items():
                # Handle set-type stats (like areas_visited)
                if stat == "areas_visited" and isinstance(user_data["achievements"]["progress"].get(stat), set):
                    if len(user_data["achievements"]["progress"].get(stat, set())) < required_value:
                        requirement_met = False
                        break
                # Handle regular numeric stats
                elif user_data["achievements"]["progress"].get(stat, 0) < required_value:
                    requirement_met = False
                    break
                    
        # If requirement is met, unlock achievement
        if requirement_met:
            # Unlock the achievement
            user_data["achievements"]["unlocked"].append(achievement_id)
            newly_unlocked.append(achievement)
            
            # Apply rewards
            grant_achievement_rewards(achievement)
    
    # Display newly unlocked achievements with fancy UI
    if newly_unlocked:
        print_animated(f"\n{BG_YELLOW}{BLACK} ACHIEVEMENTS UNLOCKED! {ENDC}", delay=0.05)
        for achievement in newly_unlocked:
            icon = achievement.get("icon", "🏆")
            tier = achievement.get("tier", 1)
            tier_color = [WHITE, LIGHTGREEN, LIGHTBLUE, LIGHTMAGENTA, LIGHTYELLOW][min(tier, 4)]
            
            print_animated(f"{tier_color}{icon} {achievement['name']}{ENDC} - {achievement['description']}", delay=0.03)
            
            # Show rewards
            if "reward" in achievement:
                reward_str = "Rewards: "
                reward = achievement["reward"]
                if "gold" in reward:
                    reward_str += f"{LIGHTYELLOW}{reward['gold']} Gold{ENDC}, "
                if "exp" in reward:
                    reward_str += f"{LIGHTGREEN}{reward['exp']} XP{ENDC}, "
                if "item" in reward:
                    reward_str += f"{LIGHTMAGENTA}{reward['item']}{ENDC}, "
                if "stat_bonus" in reward:
                    for stat, value in reward["stat_bonus"].items():
                        reward_str += f"{LIGHTCYAN}+{value} {stat.capitalize()}{ENDC}, "
                # Remove trailing comma and space
                reward_str = reward_str[:-2]
                print_animated(f"  {reward_str}", delay=0.02)

def update_achievement_progress():
    """Update and track progress towards achievements"""
    # Update achievement stats based on user_data
    user_stats = user_data["achievements"]["progress"]
    
    # Combat stats
    user_stats["monsters_killed"] = user_data.get("monsters_killed", 0)
    user_stats["bosses_defeated"] = user_data.get("bosses_defeated", 0)
    user_stats["critical_hits"] = user_data.get("critical_hits", 0)
    user_stats["combo_finishers"] = user_data.get("combo_finishers", 0)
    user_stats["skills_used"] = user_data.get("skills_used", 0)
    
    # Wealth stats
    user_stats["total_gold_earned"] = user_data.get("total_gold_earned", user_data.get("gold", 0))
    user_stats["gold_spent"] = user_data.get("gold_spent", 0)
    
    # Experience stats (level is directly accessed)
    
    # Exploration stats
    if "visited_locations" not in user_stats:
        user_stats["visited_locations"] = set()
    if "current_area" in user_data:
        user_stats["visited_locations"].add(user_data["current_area"])
    user_stats["distance_traveled"] = user_data.get("distance_traveled", 0)
    
    # Collection stats
    user_stats["items_collected"] = len(user_data.get("inventory", []))
    user_stats["treasure_chests_opened"] = user_data.get("treasure_chests_opened", 0)
    
    # Crafting stats
    user_stats["items_crafted"] = user_data.get("items_crafted", 0)
    
    # Quest stats
    user_stats["quests_completed"] = len(user_data.get("completed_quests", []))
    
    # Dungeon stats
    user_stats["dungeons_completed"] = len(user_data.get("completed_dungeons", []))
    
    # Other stats
    user_stats["potions_used"] = user_data.get("potions_used", 0)
    user_stats["deaths"] = user_data.get("deaths", 0)
    user_stats["enemies_dodged"] = user_data.get("enemies_dodged", 0)
    
    # Ensure all_collected_items exists for tracking unique items
    if "all_collected_items" not in user_data:
        user_data["all_collected_items"] = []
        # Initialize with current inventory
        user_data["all_collected_items"].extend(user_data.get("inventory", []))

def grant_achievement_rewards(achievement):
    """Apply rewards from unlocking an achievement"""
    global user_data
    
    if "reward" not in achievement:
        return
        
    reward = achievement["reward"]
    
    # Apply gold reward
    if "gold" in reward:
        user_data["gold"] += reward["gold"]
        print_animated(f"  {LIGHTYELLOW}+{reward['gold']} Gold{ENDC}", delay=0.02)
        
    # Apply experience reward
    if "exp" in reward:
        old_level = user_data["level"]
        user_data["exp"] += reward["exp"]
        print_animated(f"  {LIGHTGREEN}+{reward['exp']} XP{ENDC}", delay=0.02)
        # Check for level up
        check_level_up()
        # Note if level up occurred
        if user_data["level"] > old_level:
            print_animated(f"  {BG_GREEN}{BLACK} LEVEL UP! {ENDC} You are now level {user_data['level']}!", delay=0.03)
        
    # Add item reward
    if "item" in reward:
        item_name = reward["item"]
        user_data["inventory"].append(item_name)
        print_animated(f"  {LIGHTMAGENTA}Received {item_name}{ENDC}", delay=0.02)
        
        # Track item collection for achievement tracking
        if "all_collected_items" not in user_data:
            user_data["all_collected_items"] = []
        user_data["all_collected_items"].append(item_name)
        
    # Apply stat bonuses
    if "stat_bonus" in reward:
        for stat, value in reward["stat_bonus"].items():
            if stat == "critical_chance":
                # Special handling for percentage-based stats
                if "critical_chance_bonus" not in user_data:
                    user_data["critical_chance_bonus"] = 0
                user_data["critical_chance_bonus"] += value
                print_animated(f"  {LIGHTCYAN}+{value*100}% Critical Chance{ENDC}", delay=0.02)
            elif stat == "health":
                # Increase both current and max health
                user_data["max_health"] += value
                user_data["health"] += value
                print_animated(f"  {LIGHTGREEN}+{value} Max Health{ENDC}", delay=0.02)
            else:
                # Standard stat increase
                if stat not in user_data:
                    user_data[stat] = 0
                user_data[stat] += value
                print_animated(f"  {LIGHTCYAN}+{value} {stat.capitalize()}{ENDC}", delay=0.02)

def show_achievements():
    """Display achievements screen with progress tracking"""
    if "achievements" not in user_data:
        user_data["achievements"] = {
            "unlocked": [],
            "progress": {}
        }
    
    # Update achievement progress before showing
    update_achievement_progress()
    
    # Get all achievements organized by category
    all_achievements = {
        "Combat": [],
        "Wealth": [],
        "Experience": [],
        "Exploration": [],
        "Collection": [],
        "Crafting": [],
        "Quests": [],
        "Dungeons": [],
        "Survival": []
    }
    
    # Dynamically generate the achievements list based on the ACHIEVEMENTS constant
    for achievement in ACHIEVEMENTS:
        # Ensure we have proper dictionary objects for achievements
        if not isinstance(achievement, dict):
            # Skip non-dictionary achievements to prevent typing errors
            continue
            
        # Explicitly cast to proper types to avoid LSP errors
        achievement_dict = achievement  # Type hint now recognizes this as a dictionary
        
        # Get category with a safer approach using get()
        category = achievement_dict.get("category", "Other")
            
        if category in all_achievements:
            all_achievements[category].append(achievement_dict)
    
    # Count total and unlocked achievements
    total_achievements = len(ACHIEVEMENTS)
    unlocked_count = len(user_data["achievements"]["unlocked"])
    completion_pct = unlocked_count / total_achievements * 100 if total_achievements > 0 else 0
    
    # Display achievements screen
    print_header("Achievements")
    
    # Show completion summary
    print(f"{BOLD}Achievements Unlocked:{ENDC} {LIGHTCYAN}{unlocked_count}/{total_achievements}{ENDC} ({completion_pct:.1f}%)")
    
    # Show achievement progress bar
    progress_bar = create_progress_bar(completion_pct/100, 40)
    print(f"{progress_bar}\n")
    
    # Show achievement categories
    categories = list(all_achievements.keys())
    
    # Ask which category to display
    print(f"{BOLD}Categories:{ENDC}")
    for i, category in enumerate(categories, 1):
        cat_achievements = all_achievements[category]
        if not cat_achievements:
            continue
            
        cat_unlocked = len([a for a in cat_achievements if a["id"] in user_data["achievements"]["unlocked"]])
        cat_total = len(cat_achievements)
        cat_pct = cat_unlocked / cat_total * 100 if cat_total > 0 else 0
        cat_color = get_completion_color(cat_pct)
        
        print(f"{i}. {cat_color}{category}{ENDC} - {cat_unlocked}/{cat_total} ({cat_pct:.1f}%)")
    
    # Add option to show all
    all_option = len(categories) + 1
    print(f"{all_option}. {CYAN}Show All{ENDC}")
    print(f"{all_option + 1}. {YELLOW}Back{ENDC}")
    
    # Get user choice
    try:
        choice = input(f"\n{YELLOW}Choose category (1-{all_option + 1}): {ENDC}")
        choice = int(choice)
        
        if choice == all_option + 1:  # Back
            return
        elif choice == all_option:  # Show all
            show_all_achievements(all_achievements)
        elif 1 <= choice <= len(categories):
            category = categories[choice - 1]
            show_category_achievements(category, all_achievements[category])
        else:
            print(f"{RED}Invalid choice.{ENDC}")
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{ENDC}")

def show_category_achievements(category, achievements):
    """Show achievements for a specific category"""
    print_header(f"{category} Achievements")
    
    # Group by tier
    by_tier = {}
    for achievement in achievements:
        tier = achievement.get("tier", 1)
        if tier not in by_tier:
            by_tier[tier] = []
        by_tier[tier].append(achievement)
    
    # Display by tier (ascending)
    for tier in sorted(by_tier.keys()):
        tier_name = ["Beginner", "Intermediate", "Advanced", "Expert", "Master"][min(tier - 1, 4)]
        tier_color = [GREEN, CYAN, BLUE, MAGENTA, YELLOW][min(tier - 1, 4)]
        
        print(f"\n{tier_color}{BOLD}Tier {tier}: {tier_name}{ENDC}")
        
        for achievement in by_tier[tier]:
            display_achievement(achievement)
    
    input(f"\n{YELLOW}Press Enter to continue...{ENDC}")

def show_all_achievements(all_achievements):
    """Show all achievements grouped by category"""
    print_header("All Achievements")
    
    for category, achievements in all_achievements.items():
        if not achievements:
            continue
            
        cat_unlocked = len([a for a in achievements if a["id"] in user_data["achievements"]["unlocked"]])
        cat_total = len(achievements)
        
        print(f"\n{BOLD}{CYAN}{category}{ENDC} ({cat_unlocked}/{cat_total})")
        print(f"{CYAN}{'-' * (len(category) + 2)}{ENDC}")
        
        for achievement in achievements:
            display_achievement(achievement, short=True)
    
    input(f"\n{YELLOW}Press Enter to continue...{ENDC}")

def display_achievement(achievement, short=False):
    """Display a single achievement with its status and progress"""
    achievement_id = achievement["id"]
    is_unlocked = achievement_id in user_data["achievements"]["unlocked"]
    
    # Get achievement details
    name = achievement["name"]
    description = achievement["description"]
    icon = achievement.get("icon", "🏆")
    tier = achievement.get("tier", 1)
    
    # Determine colors based on tier and unlock status
    if is_unlocked:
        tier_color = [LIGHTGREEN, LIGHTCYAN, LIGHTBLUE, LIGHTMAGENTA, LIGHTYELLOW][min(tier - 1, 4)]
        status_icon = "✓"
    else:
        tier_color = GREY
        status_icon = "☐"
    
    # Display basic info
    if short:
        print(f"{tier_color}{status_icon} {icon} {name}{ENDC}")
    else:
        print(f"{tier_color}{status_icon} {icon} {name}{ENDC} - {description}")
    
    # If not unlocked, show progress (if progress tracking is available)
    if not is_unlocked and not short and isinstance(achievement.get("requirement"), dict):
        for stat, required_value in achievement["requirement"].items():
            current_value = 0
            
            # Handle set-type stats (like areas_visited)
            if stat == "areas_visited" and isinstance(user_data["achievements"]["progress"].get(stat), set):
                current_value = len(user_data["achievements"]["progress"].get(stat, set()))
            else:
                current_value = user_data["achievements"]["progress"].get(stat, 0)
                
            progress_pct = min(1.0, current_value / required_value)
            progress_bar = create_progress_bar(progress_pct, 20)
            print(f"  Progress: {current_value}/{required_value} {progress_bar}")
    
    # Show rewards if not short view
    if not short and "reward" in achievement:
        reward = achievement["reward"]
        reward_parts = []
        
        if "gold" in reward:
            reward_parts.append(f"{LIGHTYELLOW}{reward['gold']} Gold{ENDC}")
        if "exp" in reward:
            reward_parts.append(f"{LIGHTGREEN}{reward['exp']} XP{ENDC}")
        if "item" in reward:
            reward_parts.append(f"{LIGHTMAGENTA}{reward['item']}{ENDC}")
        if "stat_bonus" in reward:
            for stat, value in reward["stat_bonus"].items():
                stat_name = stat.capitalize()
                if stat == "critical_chance":
                    reward_parts.append(f"{LIGHTCYAN}+{value*100}% Crit Chance{ENDC}")
                else:
                    reward_parts.append(f"{LIGHTCYAN}+{value} {stat_name}{ENDC}")
                
        if reward_parts:
            print(f"  Rewards: {', '.join(reward_parts)}")

def create_progress_bar(percentage, length=20):
    """Create a visual progress bar with gradients"""
    filled_length = int(length * percentage)
    empty_length = length - filled_length
    
    if percentage < 0.3:
        color = RED
    elif percentage < 0.7:
        color = YELLOW
    else:
        color = GREEN
        
    bar = f"{color}{'█' * filled_length}{LIGHTGRAY}{'▒' * empty_length}{ENDC}"
    return bar

def get_completion_color(percentage):
    """Return a color based on completion percentage"""
    if percentage < 25:
        return RED
    elif percentage < 50:
        return YELLOW
    elif percentage < 75:
        return CYAN
    else:
        return GREEN

# First calculate_elemental_damage function removed (duplicate)
# Using the more complete version at line ~3038

# First apply_elemental_effects function removed (duplicate)
# Using the more complete version at line ~3090

# First update_status_effects function removed (duplicate)
# Using the more complete version below

# First get_player_element function removed (duplicate)
# Using the more complete version below with type annotations

# Elemental Combat Functions
def calculate_elemental_damage(attacker_element: str, defender_element: str, base_damage: int) -> Tuple[int, str, Dict]:
    """Calculate damage based on elemental interactions and return elemental reaction if applicable

    Args:
        attacker_element: The element of the attacker
        defender_element: The element of the defender
        base_damage: The base damage amount

    Returns:
        Tuple of (final_damage, reaction_name, reaction_effect)
    """
    damage_multiplier = 1.0
    reaction_name = ""  # Empty string instead of None
    reaction_effect = {}

    # Check for immunity (monster immune to their own element)
    if attacker_element == defender_element and defender_element != "Nullum":
        print_colored(f"The {defender_element} creature is immune to {attacker_element} damage!", WARNING)
        return 0, "", {}  # Empty string instead of None

    # Check elemental strengths and weaknesses
    if attacker_element in ELEMENTS and defender_element in ELEMENTS:
        # Defender is weak to attacker's element
        if defender_element in ELEMENTS[attacker_element].get("strength", []):
            damage_multiplier = 1.5
            print_colored(f"{attacker_element} is strong against {defender_element}!", OKGREEN)

        # Attacker's element is weak against defender's element
        elif attacker_element in ELEMENTS[defender_element].get("strength", []):
            damage_multiplier = 0.5
            print_colored(f"{attacker_element} is weak against {defender_element}!", FAIL)

    # Check for potential elemental reaction
    reaction_key = f"{attacker_element}+{defender_element}"
    if reaction_key in ELEMENTAL_REACTIONS:
        reaction = ELEMENTAL_REACTIONS[reaction_key]
        reaction_name = reaction["name"]
        reaction_effect = reaction["effect"]
        reaction_multiplier = reaction["damage_multiplier"]

        # Apply elemental reaction multiplier
        damage_multiplier *= reaction_multiplier

        print_colored(f"Elemental Reaction: {reaction_name}!", MAGENTA)
        print_colored(f"{reaction['description']}", CYAN)

    # Calculate final damage with appropriate rounding
    final_damage = int(base_damage * damage_multiplier)

    return final_damage, reaction_name, reaction_effect


def apply_elemental_effects(entity_data: Dict, reaction_effect: Dict, is_player: bool = False) -> None:
    """Apply elemental reaction effects to an entity

    Args:
        entity_data: The entity to apply effects to (player or monster)
        reaction_effect: The reaction effect data
        is_player: Whether the entity is the player
    """
    if not reaction_effect:
        return

    # Initialize status effects if not present
    if "status_effects" not in entity_data:
        entity_data["status_effects"] = {}

    duration = reaction_effect.get("duration", 3)

    # Apply each effect
    for effect_type, effect_value in reaction_effect.items():
        if effect_type == "duration":  # Skip the duration itself
            continue

        # Apply damage over time effects
        if effect_type in ["burn", "poison", "shock", "dot"]:
            entity_data["status_effects"][effect_type] = {
                "value": effect_value,
                "duration": duration,
                "description": f"Taking {effect_value} damage per turn"
            }
            entity_type = "You are" if is_player else "Enemy is"
            print_colored(f"{entity_type} suffering from {effect_type} damage for {duration} turns!", WARNING)

        # Apply stat modifications
        elif effect_type in ["attack", "defense", "evasion", "vision", "dodge", "slow", "movement"]:
            entity_data["status_effects"][effect_type] = {
                "value": effect_value,
                "duration": duration,
                "description": f"{effect_type.capitalize()} {'increased' if effect_value > 0 else 'decreased'} by {abs(effect_value)}"
            }
            stat_change = "boosted" if effect_value > 0 else "reduced"
            entity_type = "Your" if is_player else "Enemy's"
            print_colored(f"{entity_type} {effect_type} is {stat_change} by {abs(effect_value)} for {duration} turns!", CYAN if effect_value > 0 else WARNING)

        # Apply healing effects
        elif effect_type == "heal" and effect_value > 0:
            if is_player:
                user_data["health"] = min(user_data["health"] + effect_value, user_data["max_health"])
                print_colored(f"You are healed for {effect_value} HP!", OKGREEN)
            else:
                entity_data["health"] = min(entity_data["health"] + effect_value, entity_data.get("max_health", entity_data["health"]))
                print_colored(f"Enemy is healed for {effect_value} HP!", FAIL)

        # Apply control effects
        elif effect_type in ["immobilize", "stun", "confusion", "entangle"]:
            entity_data["status_effects"][effect_type] = {
                "value": True,
                "duration": duration,
                "description": f"Cannot move due to {effect_type}"
            }
            entity_type = "You are" if is_player else "Enemy is"
            print_colored(f"{entity_type} {effect_type}d for {duration} turns!", WARNING if is_player else OKGREEN)


def update_status_effects(entity_data: Dict, is_player: bool = False) -> None:
    """Update and apply the effects of status conditions

    Args:
        entity_data: The entity to update effects for
        is_player: Whether the entity is the player
    """
    if "status_effects" not in entity_data:
        return

    effects_to_remove = []

    for effect_name, effect_data in entity_data["status_effects"].items():
        # Apply damage over time effects
        if effect_name in ["burn", "poison", "shock", "dot"]:
            damage = effect_data["value"]
            if is_player:
                user_data["health"] = max(0, user_data["health"] - damage)
                print_colored(f"You take {damage} damage from {effect_name}!", FAIL)
                if user_data["health"] <= 0:
                    print_colored("You were defeated by status effects!", FAIL)
            else:
                entity_data["health"] -= damage
                print_colored(f"Enemy takes {damage} damage from {effect_name}!", OKGREEN)

        # Decrement duration and remove expired effects
        effect_data["duration"] -= 1
        if effect_data["duration"] <= 0:
            effects_to_remove.append(effect_name)
            entity_type = "Your" if is_player else "Enemy's"
            print_colored(f"{entity_type} {effect_name} effect has worn off.", CYAN)

    # Clean up expired effects
    for effect_name in effects_to_remove:
        del entity_data["status_effects"][effect_name]


def get_player_element() -> str:
    """Get the player's current element based on equipped items"""
    # Default to physical damage
    element = "Nullum"

    # Check for elemental weapon
    if user_data.get("equipped", {}).get("weapon"):
        weapon_name = user_data["equipped"]["weapon"]["name"]

        # Search through shop items or any available item collections
        # Note: Just check the weapon name for now, assuming we'll add element attributes
        # to weapons in the future
        weapon_elements = {
            "Flame Sword": "Ignis",
            "Ice Sword": "Glacies",
            "Lightning Sword": "Fulmen",
            "Nature Sword": "Viridia",
            "Earth Sword": "Gē",
            "Wind Sword": "Aer",
            "Water Sword": "Aqua",
            "Light Sword": "Lux",
            "Shadow Blade": "Tenebrae",
            "Poison Dagger": "Venēnum",
            "Steel Sword": "Ferrum",
            "Spirit Blade": "Pneuma"
        }

        # Check if the weapon has an elemental type
        if weapon_name in weapon_elements:
            element = weapon_elements[weapon_name]

    return element

# Artifact categories 
ARTIFACT_SLOTS = ["Headset", "Necklace", "Clock", "Flower", "Feather", "Ring"]

# Dimension definitions - alternate realities and planes of existence
DIMENSIONS = {
    "Overworld": {
        "name": "Overworld",
        "description": "The main world where most of your adventure takes place.",
        "access_level": 1,
        "monsters": ["Wolf", "Goblin", "Bandit", "Spider", "Skeleton"],
        "resources": ["Wood", "Stone", "Iron Ore", "Herb", "Water"],
        "special_locations": ["Ancient Ruins", "Forgotten Temple", "Sacred Grove"]
    },
    "Shadowrealm": {
        "name": "Shadowrealm",
        "description": "A dark dimension where shadows come to life and darkness reigns.",
        "access_level": 15,
        "monsters": ["Shadow Wolf", "Void Walker", "Umbral Assassin", "Darkness Elemental"],
        "resources": ["Shadow Essence", "Void Crystal", "Dark Matter", "Umbral Stone", "Night Bloom"],
        "special_locations": ["Void Nexus", "Shadow Temple", "Dark Tower"],
        "unlock_item": "Shadow Key"
    },
    "Celestial Plane": {
        "name": "Celestial Plane",
        "description": "A dimension of light and divine energy, home to celestial beings.",
        "access_level": 25,
        "monsters": ["Light Guardian", "Celestial Protector", "Divine Servant", "Radiant Phoenix"],
        "resources": ["Divine Crystal", "Celestial Dust", "Light Essence", "Holy Water", "Heavenly Ore"],
        "special_locations": ["Ivory Citadel", "Celestial Forge", "Gardens of Eternity"],
        "unlock_item": "Divine Shard"
    },
    "Elemental Chaos": {
        "name": "Elemental Chaos",
        "description": "A chaotic dimension where the fundamental elements clash in perpetual conflict.",
        "access_level": 30,
        "monsters": ["Fire Elemental", "Water Sprite", "Earth Golem", "Air Wisp", "Lightning Fiend"],
        "resources": ["Pure Fire", "Elemental Water", "Living Stone", "Wind Essence", "Lightning Crystal"],
        "special_locations": ["Core of Creation", "Primal Vortex", "The Convergence"],
        "unlock_item": "Elemental Core"
    },
    "Timeless Void": {
        "name": "Timeless Void",
        "description": "A dimension outside of time where past, present, and future exist simultaneously.",
        "access_level": 40,
        "monsters": ["Chrono Wraith", "Temporal Guardian", "Memory Eater", "Future Seer", "Past Walker"],
        "resources": ["Frozen Time", "Future Fragment", "Memory Crystal", "Temporal Sand", "Eternity Shard"],
        "special_locations": ["Clock Tower Eternal", "Hall of Ages", "Paradox Nexus"],
        "unlock_item": "Chronos Crystal"
    }
}

# Home and Camp Structure definitions
HOME_STRUCTURES = {
    "Tent": {
        "name": "Basic Tent",
        "description": "A simple tent that provides basic shelter and rest.",
        "level": 1,
        "materials": {"Cloth": 5, "Wood": 3},
        "effects": {"rest_heal": 20, "storage": 10},
        "category": "shelter"
    },
    "Campfire": {
        "name": "Campfire",
        "description": "A small fire that provides warmth and a place to cook food.",
        "level": 1,
        "materials": {"Wood": 5, "Stone": 3},
        "effects": {"cook_food": True, "light": True},
        "category": "utility"
    },
    "Storage Chest": {
        "name": "Storage Chest",
        "description": "A wooden chest that provides additional storage space.",
        "level": 1,
        "materials": {"Wood": 10, "Iron Ore": 2},
        "effects": {"storage": 20},
        "category": "storage"
    },
    "Workbench": {
        "name": "Workbench",
        "description": "A simple workbench for crafting basic items.",
        "level": 1,
        "materials": {"Wood": 15, "Iron Ore": 5},
        "effects": {"crafting_bonus": 0.1},
        "category": "crafting"
    },
    "Herb Garden": {
        "name": "Herb Garden",
        "description": "A small garden to grow healing herbs.",
        "level": 1,
        "materials": {"Wood": 5, "Herb": 3, "Water": 2},
        "effects": {"herb_production": 1},
        "category": "production"
    },
    "Training Dummy": {
        "name": "Training Dummy",
        "description": "A wooden dummy for combat practice.",
        "level": 1,
        "materials": {"Wood": 10, "Cloth": 5},
        "effects": {"combat_exp_bonus": 0.05},
        "category": "training"
    },
    "Small Hut": {
        "name": "Small Hut",
        "description": "A small wooden hut that provides better shelter than a tent.",
        "level": 2,
        "materials": {"Wood": 20, "Stone": 10, "Cloth": 5},
        "effects": {"rest_heal": 40, "storage": 20},
        "category": "shelter",
        "upgrade_from": "Tent"
    },
    "Cooking Pot": {
        "name": "Cooking Pot",
        "description": "A pot for cooking more complex meals with better effects.",
        "level": 2,
        "materials": {"Iron Ore": 10, "Stone": 5},
        "effects": {"food_quality": 0.2},
        "category": "utility",
        "requires": "Campfire"
    },
    "Reinforced Chest": {
        "name": "Reinforced Chest",
        "description": "A stronger chest with more storage capacity.",
        "level": 2,
        "materials": {"Wood": 15, "Iron Ore": 10, "Stone": 5},
        "effects": {"storage": 40},
        "category": "storage",
        "upgrade_from": "Storage Chest"
    },
    "Alchemy Station": {
        "name": "Alchemy Station",
        "description": "A station for creating potions and elixirs.",
        "level": 2,
        "materials": {"Wood": 10, "Iron Ore": 5, "Herb": 10, "Glass": 5},
        "effects": {"alchemy_bonus": 0.15},
        "category": "crafting"
    },
    "Meditation Shrine": {
        "name": "Meditation Shrine",
        "description": "A quiet place for meditation and mana regeneration.",
        "level": 2,
        "materials": {"Stone": 15, "Divine Crystal": 1},
        "effects": {"mana_regen": 0.1, "meditation_bonus": 0.2},
        "category": "spiritual"
    },
    "Forge": {
        "name": "Forge",
        "description": "A furnace for smelting ores and forging metal items.",
        "level": 3,
        "materials": {"Stone": 30, "Iron Ore": 20, "Wood": 10},
        "effects": {"smithing_bonus": 0.2, "metal_quality": 0.15},
        "category": "crafting",
        "upgrade_from": "Workbench"
    },
    "Enchanting Table": {
        "name": "Enchanting Table",
        "description": "A magical table for enchanting weapons and armor.",
        "level": 3,
        "materials": {"Wood": 20, "Divine Crystal": 5, "Shadow Essence": 3},
        "effects": {"enchant_power": 0.2, "enchant_cost": -0.1},
        "category": "magic"
    },
    "Cabin": {
        "name": "Cabin",
        "description": "A solid wooden cabin with multiple rooms.",
        "level": 3,
        "materials": {"Wood": 50, "Stone": 30, "Iron Ore": 10},
        "effects": {"rest_heal": 60, "storage": 50, "comfort": 0.3},
        "category": "shelter",
        "upgrade_from": "Small Hut"
    },
    "Portal Frame": {
        "name": "Portal Frame",
        "description": "A frame for creating portals to other dimensions.",
        "level": 4,
        "materials": {"Divine Crystal": 5, "Shadow Essence": 5, "Pure Fire": 5, "Elemental Water": 5, "Living Stone": 5},
        "effects": {"dimension_travel": True},
        "category": "magic"
    }
}

# Function for enchanting items with special effects
def enchant_item() -> None:
    """Function to enchant weapons and armor with special effects"""
    print_header("Item Enchantment")
    
    # Get list of enchantable equipment
    enchantable_items = []
    if "equipment" in user_data:
        for item in user_data["equipment"]:
            # Skip already enchanted items unless they can be re-enchanted
            if item.get("enchantment") and not item.get("can_reenchant", False):
                continue
                
            # Only weapons, armor, and accessories can be enchanted
            if item.get("type") in ["weapon", "armor", "accessory"]:
                enchantable_items.append(item)
    
    if not enchantable_items:
        print_animated(f"{YELLOW}You don't have any items that can be enchanted.{ENDC}", delay=0.03)
        return
    
    # Display enchantable items
    print_animated(f"{CYAN}Select an item to enchant:{ENDC}", delay=0.03)
    for i, item in enumerate(enchantable_items, 1):
        rarity_color = get_rarity_color(item.get("rarity", "Common"))
        enchant_text = ""
        if item.get("enchantment"):
            enchant_text = f" (Currently: {LIGHTMAGENTA}{item['enchantment']['name']}{ENDC})"
            
        print(f"{i}. {rarity_color}{item['name']}{ENDC}{enchant_text}")
    
    print(f"{len(enchantable_items) + 1}. {YELLOW}Cancel{ENDC}")
    
    # Get user selection
    try:
        choice = int(input(f"\n{YELLOW}Choose an item (1-{len(enchantable_items) + 1}): {ENDC}"))
        if choice == len(enchantable_items) + 1:
            print_animated(f"{YELLOW}Enchantment canceled.{ENDC}", delay=0.03)
            return
            
        if 1 <= choice <= len(enchantable_items):
            selected_item = enchantable_items[choice - 1]
            
            # Get available enchantments based on item type and player level
            available_enchants = get_available_enchantments(selected_item["type"], user_data["level"])
            
            if not available_enchants:
                print_animated(f"{YELLOW}No enchantments available for this item.{ENDC}", delay=0.03)
                return
            
            # Check if player has materials
            required_materials = {
                "Common": {"Magical Dust": 5},
                "Uncommon": {"Magical Dust": 10, "Enchanted Fragment": 2},
                "Rare": {"Magical Dust": 20, "Enchanted Fragment": 5, "Arcane Crystal": 1},
                "Epic": {"Magical Dust": 30, "Enchanted Fragment": 10, "Arcane Crystal": 3, "Ethereal Essence": 1},
                "Legendary": {"Magical Dust": 50, "Enchanted Fragment": 20, "Arcane Crystal": 5, "Ethereal Essence": 3}
            }
            
            item_rarity = selected_item.get("rarity", "Common")
            materials_needed = required_materials.get(item_rarity, required_materials["Common"])
            
            # Check if player has the materials
            has_materials = True
            for material, amount in materials_needed.items():
                count = user_data["inventory"].count(material)
                if count < amount:
                    has_materials = False
                    break
            
            # Display enchantment options
            print_header(f"Enchant {selected_item['name']}")
            
            # Show required materials
            print_animated(f"{CYAN}Required Materials:{ENDC}", delay=0.02)
            for material, amount in materials_needed.items():
                current = user_data["inventory"].count(material)
                color = GREEN if current >= amount else RED
                print(f"- {material}: {color}{current}/{amount}{ENDC}")
            
            if not has_materials:
                print_animated(f"\n{RED}You don't have enough materials for enchanting.{ENDC}", delay=0.03)
                return
            
            print_animated(f"\n{CYAN}Available Enchantments:{ENDC}", delay=0.03)
            for i, enchant in enumerate(available_enchants, 1):
                print(f"{i}. {LIGHTMAGENTA}{enchant['name']}{ENDC} - {enchant['description']}")
            
            print(f"{len(available_enchants) + 1}. {YELLOW}Cancel{ENDC}")
            
            # Get enchantment choice
            try:
                enchant_choice = int(input(f"\n{YELLOW}Choose an enchantment (1-{len(available_enchants) + 1}): {ENDC}"))
                if enchant_choice == len(available_enchants) + 1:
                    print_animated(f"{YELLOW}Enchantment canceled.{ENDC}", delay=0.03)
                    return
                    
                if 1 <= enchant_choice <= len(available_enchants):
                    selected_enchant = available_enchants[enchant_choice - 1]
                    
                    # Apply enchantment
                    print_animated(f"{BG_MAGENTA}{WHITE} ENCHANTING... {ENDC}", delay=0.5)
                    print_animated(f"{LIGHTMAGENTA}Mystical energies swirl around the {selected_item['name']}...{ENDC}", delay=0.05)
                    
                    # Calculate success chance based on rarity and player stats
                    success_chance = {
                        "Common": 0.95,
                        "Uncommon": 0.85,
                        "Rare": 0.75,
                        "Epic": 0.65,
                        "Legendary": 0.50
                    }.get(item_rarity, 0.95)
                    
                    # Increase chance based on player stats
                    if "crafting" in user_data:
                        success_chance += min(0.3, user_data["crafting"] * 0.01)
                    
                    # Roll for success
                    if random.random() < success_chance:
                        # Success!
                        selected_item["enchantment"] = {
                            "name": selected_enchant["name"],
                            "effect": selected_enchant["effect"],
                            "effect_value": selected_enchant["value"]
                        }
                        
                        print_animated(f"\n{BG_GREEN}{BLACK} SUCCESS! {ENDC}", delay=0.03)
                        print_animated(f"Your {selected_item['name']} is now enchanted with {LIGHTMAGENTA}{selected_enchant['name']}{ENDC}!", delay=0.03)
                        
                        # Apply the enchantment effect to the item's stats if applicable
                        if selected_enchant["effect"] == "damage":
                            if "effect" not in selected_item:
                                selected_item["effect"] = 0
                            selected_item["effect"] += selected_enchant["value"]
                        elif selected_enchant["effect"] == "defense":
                            if "effect" not in selected_item:
                                selected_item["effect"] = 0
                            selected_item["effect"] += selected_enchant["value"]
                            
                        # Add element if the enchantment adds one
                        if "element" in selected_enchant:
                            selected_item["element"] = selected_enchant["element"]
                        
                        # Update achievement stats
                        if "achievements" in user_data and "progress" in user_data["achievements"]:
                            if "items_enchanted" not in user_data["achievements"]["progress"]:
                                user_data["achievements"]["progress"]["items_enchanted"] = 0
                            user_data["achievements"]["progress"]["items_enchanted"] += 1
                            
                        # Check achievements
                        check_achievements()
                    else:
                        # Failure
                        print_animated(f"\n{BG_RED}{WHITE} FAILURE! {ENDC}", delay=0.03)
                        print_animated("The enchantment failed! The materials were consumed but the item remains unchanged.", delay=0.03)
                    
                    # Consume materials
                    for material, amount in materials_needed.items():
                        for _ in range(amount):
                            user_data["inventory"].remove(material)
                    
                else:
                    print_animated(f"{YELLOW}Invalid enchantment choice.{ENDC}", delay=0.03)
            except ValueError:
                print_animated(f"{RED}Invalid input. Please enter a number.{ENDC}", delay=0.03)
        else:
            print_animated(f"{YELLOW}Invalid item choice.{ENDC}", delay=0.03)
    except ValueError:
        print_animated(f"{RED}Invalid input. Please enter a number.{ENDC}", delay=0.03)

def get_available_enchantments(item_type, player_level):
    """Get available enchantments based on item type and player level"""
    all_enchantments = {
        # Weapon enchantments
        "weapon": [
            {
                "name": "Sharpness",
                "description": "Increases damage by 5",
                "effect": "damage",
                "value": 5,
                "min_level": 1
            },
            {
                "name": "Fire Aspect",
                "description": "Adds Fire element and deals 3 damage over time",
                "effect": "dot",
                "value": 3,
                "element": "Fire",
                "min_level": 5
            },
            {
                "name": "Frost Bite",
                "description": "Adds Ice element and has 20% chance to slow enemies",
                "effect": "slow",
                "value": 0.2,
                "element": "Ice",
                "min_level": 5
            },
            {
                "name": "Thunder Strike",
                "description": "Adds Lightning element and has 15% chance to stun",
                "effect": "stun",
                "value": 0.15,
                "element": "Lightning",
                "min_level": 10
            },
            {
                "name": "Life Steal",
                "description": "Heals for 10% of damage dealt",
                "effect": "lifesteal",
                "value": 0.1,
                "min_level": 15
            },
            {
                "name": "Critical Edge",
                "description": "Increases critical hit chance by 10%",
                "effect": "critical_chance",
                "value": 0.1,
                "min_level": 10
            },
            {
                "name": "Executioner",
                "description": "Deals 20% more damage to enemies below 30% health",
                "effect": "execute",
                "value": 0.2,
                "min_level": 20
            },
            {
                "name": "Vorpal Edge",
                "description": "Critical hits deal 50% more damage",
                "effect": "critical_damage",
                "value": 0.5,
                "min_level": 25
            }
        ],
        
        # Armor enchantments
        "armor": [
            {
                "name": "Protection",
                "description": "Increases defense by 5",
                "effect": "defense",
                "value": 5,
                "min_level": 1
            },
            {
                "name": "Flame Ward",
                "description": "Reduces Fire damage by 20%",
                "effect": "fire_resist",
                "value": 0.2,
                "min_level": 5
            },
            {
                "name": "Frost Ward",
                "description": "Reduces Ice damage by 20%",
                "effect": "ice_resist",
                "value": 0.2,
                "min_level": 5
            },
            {
                "name": "Thunder Ward",
                "description": "Reduces Lightning damage by 20%",
                "effect": "lightning_resist",
                "value": 0.2,
                "min_level": 5
            },
            {
                "name": "Vitality",
                "description": "Increases max health by 20",
                "effect": "health",
                "value": 20,
                "min_level": 10
            },
            {
                "name": "Regeneration",
                "description": "Regenerates 2 health per turn",
                "effect": "regen",
                "value": 2,
                "min_level": 15
            },
            {
                "name": "Thorns",
                "description": "Reflects 15% of damage back to attacker",
                "effect": "reflect",
                "value": 0.15,
                "min_level": 20
            },
            {
                "name": "Evasion",
                "description": "Increases dodge chance by 10%",
                "effect": "dodge",
                "value": 0.1,
                "min_level": 25
            }
        ],
        
        # Accessory enchantments
        "accessory": [
            {
                "name": "Swift",
                "description": "Increases speed by 3",
                "effect": "speed",
                "value": 3,
                "min_level": 1
            },
            {
                "name": "Wise",
                "description": "Increases intellect by 3",
                "effect": "intellect",
                "value": 3,
                "min_level": 1
            },
            {
                "name": "Lucky",
                "description": "Increases item drop chance by 15%",
                "effect": "loot_chance",
                "value": 0.15,
                "min_level": 5
            },
            {
                "name": "Wealth",
                "description": "Increases gold drops by 20%",
                "effect": "gold_bonus",
                "value": 0.2,
                "min_level": 10
            },
            {
                "name": "Experience",
                "description": "Increases XP gain by 10%",
                "effect": "exp_bonus",
                "value": 0.1,
                "min_level": 15
            },
            {
                "name": "Elemental Mastery",
                "description": "Increases elemental damage by 20%",
                "effect": "elemental_damage",
                "value": 0.2,
                "min_level": 20
            },
            {
                "name": "Charisma",
                "description": "Reduces shop prices by 15%",
                "effect": "shop_discount",
                "value": 0.15,
                "min_level": 25
            }
        ]
    }
    
    # Filter enchantments by level requirement
    available = [enchant for enchant in all_enchantments.get(item_type, []) if enchant["min_level"] <= player_level]
    
    return available

def upgrade_item() -> None:
    """Function to level up weapons and armor"""
    print_header("Item Upgrade")
    
    # Get list of upgradable equipment
    upgradable_items = []
    if "equipment" in user_data:
        for item in user_data["equipment"]:
            # Only weapons, armor, and accessories can be upgraded
            if item.get("type") in ["weapon", "armor", "accessory"]:
                upgradable_items.append(item)
    
    if not upgradable_items:
        print_animated(f"{YELLOW}You don't have any items that can be upgraded.{ENDC}", delay=0.03)
        return
    
    # Display upgradable items
    print_animated(f"{CYAN}Select an item to upgrade:{ENDC}", delay=0.03)
    for i, item in enumerate(upgradable_items, 1):
        rarity_color = get_rarity_color(item.get("rarity", "Common"))
        level_text = f" (Level {item.get('level', 1)})"
        print(f"{i}. {rarity_color}{item['name']}{ENDC}{level_text}")
    
    print(f"{len(upgradable_items) + 1}. {YELLOW}Cancel{ENDC}")
    
    # Get user selection
    try:
        choice = int(input(f"\n{YELLOW}Choose an item (1-{len(upgradable_items) + 1}): {ENDC}"))
        if choice == len(upgradable_items) + 1:
            print_animated(f"{YELLOW}Upgrade canceled.{ENDC}", delay=0.03)
            return
            
        if 1 <= choice <= len(upgradable_items):
            selected_item = upgradable_items[choice - 1]
            
            # Get current item level
            current_level = selected_item.get("level", 1)
            max_level = 10
            
            if current_level >= max_level:
                print_animated(f"{YELLOW}This item is already at maximum level.{ENDC}", delay=0.03)
                return
            
            # Calculate upgrade costs based on rarity and current level
            upgrade_costs = {
                "Common": {"base_gold": 100, "materials": {"Iron Ingot": 2, "Leather": 1}},
                "Uncommon": {"base_gold": 250, "materials": {"Iron Ingot": 3, "Leather": 2, "Silver Ingot": 1}},
                "Rare": {"base_gold": 500, "materials": {"Silver Ingot": 3, "Leather": 3, "Magical Dust": 2}},
                "Epic": {"base_gold": 1000, "materials": {"Gold Ingot": 2, "Enchanted Fragment": 3, "Magical Dust": 5}},
                "Legendary": {"base_gold": 2500, "materials": {"Gold Ingot": 4, "Enchanted Fragment": 5, "Arcane Crystal": 2}}
            }
            
            item_rarity = selected_item.get("rarity", "Common")
            base_cost = upgrade_costs.get(item_rarity, upgrade_costs["Common"])
            
            # Scale gold cost based on level
            gold_cost = base_cost["base_gold"] * current_level
            
            # Scale material costs
            materials_needed = {}
            for material, amount in base_cost["materials"].items():
                materials_needed[material] = amount * current_level
            
            # Display upgrade details
            print_header(f"Upgrade {selected_item['name']}")
            
            print(f"Current Level: {CYAN}{current_level}{ENDC}")
            print(f"New Level: {GREEN}{current_level + 1}{ENDC}")
            
            # Show stat improvements
            item_type = selected_item.get("type", "weapon")
            current_effect = selected_item.get("effect", 0)
            
            if item_type == "weapon":
                upgrade_bonus = 2 * current_level
                print(f"Damage: {CYAN}{current_effect}{ENDC} → {GREEN}{current_effect + upgrade_bonus}{ENDC} (+{upgrade_bonus})")
            elif item_type == "armor":
                upgrade_bonus = 1 * current_level
                print(f"Defense: {CYAN}{current_effect}{ENDC} → {GREEN}{current_effect + upgrade_bonus}{ENDC} (+{upgrade_bonus})")
            else:  # accessory
                upgrade_bonus = 1 * current_level
                print(f"Effect: {CYAN}{current_effect}{ENDC} → {GREEN}{current_effect + upgrade_bonus}{ENDC} (+{upgrade_bonus})")
            
            # Show costs
            print(f"\n{CYAN}Upgrade Cost:{ENDC}")
            print(f"- Gold: {LIGHTYELLOW}{gold_cost}{ENDC}")
            
            # Check if player has enough gold
            has_gold = user_data["gold"] >= gold_cost
            gold_color = GREEN if has_gold else RED
            print(f"  {gold_color}You have: {user_data['gold']}{ENDC}")
            
            print(f"{CYAN}Required Materials:{ENDC}")
            has_materials = True
            for material, amount in materials_needed.items():
                current = user_data["inventory"].count(material)
                if current < amount:
                    has_materials = False
                
                color = GREEN if current >= amount else RED
                print(f"- {material}: {color}{current}/{amount}{ENDC}")
            
            # Check if player can afford upgrade
            if not has_gold or not has_materials:
                print_animated(f"\n{RED}You don't have enough resources for this upgrade.{ENDC}", delay=0.03)
                return
            
            # Ask for confirmation
            print()
            confirm = input(f"{YELLOW}Proceed with upgrade? (y/n): {ENDC}").lower()
            if confirm != 'y':
                print_animated(f"{YELLOW}Upgrade canceled.{ENDC}", delay=0.03)
                return
            
            # Perform upgrade
            print_animated(f"{BG_CYAN}{BLACK} UPGRADING... {ENDC}", delay=0.5)
            
            # Success chance decreases with higher levels
            success_chance = 1.0 - (current_level * 0.05)
            
            # Improve chance based on crafting skill
            if "crafting" in user_data:
                success_chance += min(0.3, user_data["crafting"] * 0.01)
                
            # Cap success chance between 50% and 95%
            success_chance = max(0.5, min(0.95, success_chance))
            
            # Roll for success
            if random.random() < success_chance:
                # Success!
                # Update item level
                selected_item["level"] = current_level + 1
                
                # Update item stats based on type
                if item_type == "weapon":
                    if "effect" not in selected_item:
                        selected_item["effect"] = 0
                    selected_item["effect"] += upgrade_bonus
                elif item_type == "armor":
                    if "effect" not in selected_item:
                        selected_item["effect"] = 0
                    selected_item["effect"] += upgrade_bonus
                else:  # accessory
                    if "effect" not in selected_item:
                        selected_item["effect"] = 0
                    selected_item["effect"] += upgrade_bonus
                
                print_animated(f"\n{BG_GREEN}{BLACK} SUCCESS! {ENDC}", delay=0.03)
                print_animated(f"Your {selected_item['name']} has been upgraded to level {selected_item['level']}!", delay=0.03)
                
                # Update achievement stats
                if "achievements" in user_data and "progress" in user_data["achievements"]:
                    if "items_upgraded" not in user_data["achievements"]["progress"]:
                        user_data["achievements"]["progress"]["items_upgraded"] = 0
                    user_data["achievements"]["progress"]["items_upgraded"] += 1
                    
                # Check achievements
                check_achievements()
            else:
                # Failure - item remains the same but resources are consumed
                print_animated(f"\n{BG_RED}{WHITE} FAILURE! {ENDC}", delay=0.03)
                print_animated("The upgrade failed! The materials were consumed but the item remains unchanged.", delay=0.03)
                
                # Critical failure chance increases with level (small chance to downgrade or break)
                critical_failure_chance = 0.05 * current_level
                if random.random() < critical_failure_chance and current_level > 1:
                    # 50% chance to downgrade, 50% chance to lose enchantment
                    if random.random() < 0.5 and current_level > 1:
                        selected_item["level"] = current_level - 1
                        print_animated(f"{RED}The item was downgraded to level {selected_item['level']}!{ENDC}", delay=0.03)
                    elif "enchantment" in selected_item:
                        del selected_item["enchantment"]
                        print_animated(f"{RED}The enchantment was lost in the failed upgrade attempt!{ENDC}", delay=0.03)
            
            # Consume resources
            user_data["gold"] -= gold_cost
            for material, amount in materials_needed.items():
                for _ in range(amount):
                    user_data["inventory"].remove(material)
        else:
            print_animated(f"{YELLOW}Invalid item choice.{ENDC}", delay=0.03)
    except ValueError:
        print_animated(f"{RED}Invalid input. Please enter a number.{ENDC}", delay=0.03)

def open_chest(tier: str = "Common") -> None:
    """Open a treasure chest and get random loot

    Args:
        tier: The rarity tier of the chest (Common, Uncommon, Rare, Epic, Legendary)
    """
    print_header(f"Opening {tier} Chest")
    
    # Add visual effects based on chest rarity
    rarity_color = get_rarity_color(tier)
    print_animated(f"{BG_CYAN}{BLACK} OPENING CHEST... {ENDC}", delay=0.5)
    print_animated(f"{rarity_color}The {tier} chest creaks open, revealing its contents...{ENDC}", delay=0.05)
    
    # Define loot tables for different chest tiers
    chest_contents = {
        # Standard rarity-based chests
        "Common": {
            "gold_range": (25, 100),
            "item_count": (1, 3),
            "material_count": (2, 4),
            "equipment_chance": 0.2,
            "rare_material_chance": 0.1,
            "rarity_weights": {"Common": 80, "Uncommon": 20, "Rare": 0, "Epic": 0, "Legendary": 0},
            "artifact_chance": 0.05,
            "special_item_chance": 0.01
        },
        "Uncommon": {
            "gold_range": (100, 300),
            "item_count": (2, 4),
            "material_count": (3, 6),
            "equipment_chance": 0.4,
            "rare_material_chance": 0.25,
            "rarity_weights": {"Common": 50, "Uncommon": 40, "Rare": 10, "Epic": 0, "Legendary": 0},
            "artifact_chance": 0.1,
            "special_item_chance": 0.05
        },
        "Rare": {
            "gold_range": (300, 750),
            "item_count": (3, 5),
            "material_count": (4, 8),
            "equipment_chance": 0.6,
            "rare_material_chance": 0.5,
            "rarity_weights": {"Common": 20, "Uncommon": 50, "Rare": 25, "Epic": 5, "Legendary": 0},
            "artifact_chance": 0.2,
            "special_item_chance": 0.1
        },
        "Epic": {
            "gold_range": (750, 1500),
            "item_count": (3, 6),
            "material_count": (5, 10),
            "equipment_chance": 0.8,
            "rare_material_chance": 0.75,
            "rarity_weights": {"Common": 5, "Uncommon": 25, "Rare": 45, "Epic": 20, "Legendary": 5},
            "artifact_chance": 0.4,
            "special_item_chance": 0.2
        },
        "Legendary": {
            "gold_range": (1500, 3000),
            "item_count": (4, 8),
            "material_count": (6, 12),
            "equipment_chance": 1.0,
            "rare_material_chance": 1.0,
            "rarity_weights": {"Common": 0, "Uncommon": 10, "Rare": 40, "Epic": 35, "Legendary": 15},
            "artifact_chance": 0.75,
            "special_item_chance": 0.5
        },
        
        # Specialized chests with themed contents
        "Weather": {
            "gold_range": (200, 800),
            "item_count": (2, 4),
            "material_count": (3, 6),
            "equipment_chance": 0.5,
            "rare_material_chance": 0.6,
            "rarity_weights": {"Common": 10, "Uncommon": 40, "Rare": 35, "Epic": 10, "Legendary": 5},
            "artifact_chance": 0.5,
            "special_item_chance": 0.3,
            "weather_artifact_chance": 0.8,  # High chance for weather-themed artifacts
            "special_resources": ["Storm Crystal", "Mist Essence", "Sunlight Fragment", "Rain Drop", "Snow Flake", "Wind Whisper", "Cloud Fragment"],
            "description": "A chest that seems to change with the weather, containing items attuned to natural forces."
        },
        "Seasonal": {
            "gold_range": (300, 1000),
            "item_count": (2, 5),
            "material_count": (4, 8),
            "equipment_chance": 0.6,
            "rare_material_chance": 0.7,
            "rarity_weights": {"Common": 5, "Uncommon": 30, "Rare": 40, "Epic": 20, "Legendary": 5},
            "artifact_chance": 0.6,
            "special_item_chance": 0.4,
            "seasonal_artifact_chance": 0.8,  # High chance for season-themed artifacts
            "special_resources": ["Spring Essence", "Summer Heat", "Autumn Leaf", "Winter Frost"],
            "description": "A chest that changes with the seasons, containing seasonal items and artifacts."
        },
        "Farming": {
            "gold_range": (100, 500),
            "item_count": (3, 6),
            "material_count": (5, 10),
            "equipment_chance": 0.3,
            "rare_material_chance": 0.5,
            "rarity_weights": {"Common": 20, "Uncommon": 45, "Rare": 30, "Epic": 5, "Legendary": 0},
            "artifact_chance": 0.4,
            "special_item_chance": 0.2,
            "seed_chance": 1.0,  # Always contains seeds
            "rare_seed_chance": 0.5,  # Good chance for rare seeds
            "special_resources": ["Fertilizer", "Premium Soil", "Magic Water", "Growth Tonic", "Season Extender"],
            "description": "A chest filled with farming supplies, seeds, and agricultural artifacts."
        },
        "Artifact": {
            "gold_range": (500, 1200),
            "item_count": (1, 3),
            "material_count": (2, 5),
            "equipment_chance": 0.2,
            "rare_material_chance": 0.4,
            "rarity_weights": {"Common": 5, "Uncommon": 15, "Rare": 40, "Epic": 30, "Legendary": 10},
            "artifact_chance": 1.0,  # Always contains at least one artifact
            "multi_artifact_chance": 0.5,  # 50% chance for multiple artifacts
            "special_item_chance": 0.6,
            "special_resources": ["Artifact Fragment", "Ancient Power", "Mystic Essence", "Divine Spark"],
            "description": "A mysterious chest radiating powerful energy, containing magical artifacts."
        },
        "Void": {
            "gold_range": (1000, 3000),
            "item_count": (3, 6),
            "material_count": (4, 8),
            "equipment_chance": 0.8,
            "rare_material_chance": 0.9,
            "rarity_weights": {"Common": 0, "Uncommon": 5, "Rare": 25, "Epic": 45, "Legendary": 25},
            "artifact_chance": 0.8,
            "special_item_chance": 0.7,
            "unique_item_chance": 0.3,  # Chance for dimension-specific unique items
            "special_resources": ["Void Fragment", "Chaos Crystal", "Reality Shard", "Dimensional Essence", "Cosmic Dust"],
            "description": "A chest that seems to exist between dimensions, containing items beyond normal reality."
        }
    }
    
    # Default to Common if tier not found
    chest_config = chest_contents.get(tier, chest_contents["Common"])
    
    # Generate gold
    gold_min, gold_max = chest_config["gold_range"]
    gold_amount = random.randint(gold_min, gold_max)
    
    # Generate items
    min_items, max_items = chest_config["item_count"]
    item_count = random.randint(min_items, max_items)
    
    # Generate materials
    min_materials, max_materials = chest_config["material_count"]
    material_count = random.randint(min_materials, max_materials)
    
    # Prepare lists for different types of loot
    loot_items = []
    loot_equipment = []
    loot_materials = []
    
    # Common items pool
    common_items = [
        "Healing Potion", "Mana Potion", "Strength Potion", "Defense Potion", 
        "Speed Potion", "Antidote", "Torch", "Rope", "Bandage", "Food Ration"
    ]
    
    # Material pools
    common_materials = [
        "Wood", "Stone", "Iron Ore", "Leather", "Cloth", "Bone", "Plant Fiber",
        "Coal", "Sand", "Clay"
    ]
    
    uncommon_materials = [
        "Silver Ore", "Iron Ingot", "Silk", "Fur", "Feather", "Gem Shard", 
        "Hardwood", "Glass", "Saltpeter", "Hardened Leather"
    ]
    
    rare_materials = [
        "Gold Ore", "Silver Ingot", "Gold Ingot", "Magical Dust", "Crystal Shard",
        "Enchanted Fragment", "Rare Herb", "Monster Essence", "Mystic Oil", "Rune Fragment"
    ]
    
    epic_materials = [
        "Arcane Crystal", "Mythril Ore", "Dragon Scale", "Phoenix Feather",
        "Ethereal Essence", "Void Fragment", "Cosmic Dust", "Elemental Core",
        "Ancient Relic Piece", "Abyssal Pearl"
    ]
    
    # Weapon types
    weapon_types = ["Sword", "Axe", "Dagger", "Staff", "Bow", "Wand", "Hammer", "Spear"]
    
    # Armor types
    armor_types = ["Helmet", "Chestplate", "Leggings", "Boots", "Gauntlets", "Shield"]
    
    # Accessory types
    accessory_types = ["Ring", "Amulet", "Charm", "Bracelet", "Belt", "Earring"]
    
    # Add gold
    user_data["gold"] += gold_amount
    
    # Add common items
    for _ in range(item_count):
        loot_items.append(random.choice(common_items))
    
    # Add materials
    for _ in range(material_count):
        # Determine rarity of material
        if random.random() < chest_config["rare_material_chance"]:
            if tier == "Legendary":
                loot_materials.append(random.choice(epic_materials))
            elif tier in ["Epic", "Rare"]:
                loot_materials.append(random.choice(rare_materials))
            else:
                loot_materials.append(random.choice(uncommon_materials))
        else:
            loot_materials.append(random.choice(common_materials))
    
    # Add equipment
    if random.random() < chest_config["equipment_chance"]:
        # Determine equipment type
        equip_type = random.choice(["weapon", "armor", "accessory"])
        
        # Choose specific equipment
        if equip_type == "weapon":
            equip_name = random.choice(weapon_types)
        elif equip_type == "armor":
            equip_name = random.choice(armor_types)
        else:  # accessory
            equip_name = random.choice(accessory_types)
        
        # Determine rarity based on chest tier
        rarities = list(chest_config["rarity_weights"].keys())
        weights = list(chest_config["rarity_weights"].values())
        rarity = random.choices(rarities, weights=weights, k=1)[0]
        
        # Generate prefix based on rarity
        prefixes = {
            "Common": ["Basic", "Simple", "Standard", "Plain", "Ordinary"],
            "Uncommon": ["Fine", "Strong", "Sturdy", "Keen", "Reinforced"],
            "Rare": ["Exceptional", "Valuable", "Quality", "Refined", "Pristine"],
            "Epic": ["Magnificent", "Heroic", "Superior", "Masterful", "Elite"],
            "Legendary": ["Ancient", "Mythical", "Godly", "Supreme", "Ultimate"]
        }
        
        prefix = random.choice(prefixes[rarity])
        
        # Determine if item has an element
        elements = ["Fire", "Water", "Earth", "Air", "Lightning", "Ice", "Light", "Dark"]
        has_element = random.random() < 0.3
        element = random.choice(elements) if has_element else None
        
        # Build the full item name
        if element:
            full_name = f"{prefix} {element} {equip_name}"
        else:
            full_name = f"{prefix} {equip_name}"
        
        # Calculate effect value based on rarity
        effect_value = {
            "Common": random.randint(1, 5),
            "Uncommon": random.randint(5, 10),
            "Rare": random.randint(10, 20),
            "Epic": random.randint(20, 30),
            "Legendary": random.randint(30, 50)
        }.get(rarity, 1)
        
        # Create equipment object
        equipment = {
            "name": full_name,
            "type": equip_type,
            "rarity": rarity,
            "effect": effect_value,
            "level": 1
        }
        
        if element:
            equipment["element"] = element
        
        loot_equipment.append(equipment)
    
    # Update global tracker for achievements
    if "treasure_chests_opened" not in user_data:
        user_data["treasure_chests_opened"] = 0
    user_data["treasure_chests_opened"] += 1
    
    # Update achievement progress
    if "achievements" in user_data and "progress" in user_data["achievements"]:
        if "treasure_chests_opened" not in user_data["achievements"]["progress"]:
            user_data["achievements"]["progress"]["treasure_chests_opened"] = 0
        user_data["achievements"]["progress"]["treasure_chests_opened"] += 1
    
    # Display loot
    print_animated(f"\n{LIGHTYELLOW}You found {gold_amount} gold!{ENDC}", delay=0.03)
    
    # Show equipment (most exciting first)
    if loot_equipment:
        print_animated(f"\n{CYAN}Equipment:{ENDC}", delay=0.03)
        for equip in loot_equipment:
            rarity_color = get_rarity_color(equip["rarity"])
            print_animated(f"- {rarity_color}{equip['name']}{ENDC} ({equip['rarity']} {equip['type'].capitalize()})", delay=0.03)
            
            # Add to player's equipment
            if "equipment" not in user_data:
                user_data["equipment"] = []
            user_data["equipment"].append(equip)
    
    # Show materials
    if loot_materials:
        print_animated(f"\n{GREEN}Materials:{ENDC}", delay=0.03)
        # Count duplicates
        material_counts = {}
        for material in loot_materials:
            material_counts[material] = material_counts.get(material, 0) + 1
            
        for material, count in material_counts.items():
            print_animated(f"- {material} x{count}", delay=0.02)
            
            # Add to inventory
            for _ in range(count):
                user_data["inventory"].append(material)
    
    # Show items
    if loot_items:
        print_animated(f"\n{LIGHTBLUE}Items:{ENDC}", delay=0.03)
        # Count duplicates
        item_counts = {}
        for item in loot_items:
            item_counts[item] = item_counts.get(item, 0) + 1
            
        for item, count in item_counts.items():
            print_animated(f"- {item} x{count}", delay=0.02)
            
            # Add to inventory
            for _ in range(count):
                user_data["inventory"].append(item)
    
    # For tracking unique items for achievements
    new_items = set(loot_items + loot_materials + [equip["name"] for equip in loot_equipment])
    if "all_collected_items" not in user_data:
        user_data["all_collected_items"] = []
    user_data["all_collected_items"].extend(list(new_items))
    
    common_materials = [
        "Wood", "Stone", "Iron Ore", "Leather", "Cloth", "Bone", "Plant Fiber",
        "Coal", "Sand", "Clay"
    ]
    
    uncommon_materials = [
        "Silver Ore", "Iron Ingot", "Silk", "Fur", "Feather", "Gem Shard", 
        "Hardwood", "Glass", "Saltpeter", "Hardened Leather"
    ]
    
    rare_materials = [
        "Gold Ore", "Silver Ingot", "Gold Ingot", "Magical Dust", "Crystal Shard",
        "Enchanted Fragment", "Rare Herb", "Monster Essence", "Mystic Oil", "Rune Fragment"
    ]
    
    epic_materials = [
        "Arcane Crystal", "Mythril Ore", "Dragon Scale", "Phoenix Feather",
        "Ethereal Essence", "Void Fragment", "Cosmic Dust", "Elemental Core",
        "Ancient Relic Piece", "Abyssal Pearl"
    ]
    
    # Weapon types
    weapon_types = ["Sword", "Axe", "Dagger", "Staff", "Bow", "Wand", "Hammer", "Spear"]
    
    # Armor types
    armor_types = ["Helmet", "Chestplate", "Leggings", "Boots", "Gauntlets", "Shield"]
    
    # Accessory types
    accessory_types = ["Ring", "Amulet", "Charm", "Bracelet", "Belt", "Earring"]
    
    # Add gold
    user_data["gold"] += gold_amount
    
    # Add common items
    for _ in range(item_count):
        loot_items.append(random.choice(common_items))
    
    # Add materials
    for _ in range(material_count):
        # Determine rarity of material
        if random.random() < chest_config["rare_material_chance"]:
            if tier == "Legendary":
                loot_materials.append(random.choice(epic_materials))
            elif tier in ["Epic", "Rare"]:
                loot_materials.append(random.choice(rare_materials))
            else:
                loot_materials.append(random.choice(uncommon_materials))
        else:
            loot_materials.append(random.choice(common_materials))
    
    # Add equipment
    if random.random() < chest_config["equipment_chance"]:
        # Determine equipment type
        equip_type = random.choice(["weapon", "armor", "accessory"])
        
        # Choose specific equipment
        if equip_type == "weapon":
            equip_name = random.choice(weapon_types)
        elif equip_type == "armor":
            equip_name = random.choice(armor_types)
        else:  # accessory
            equip_name = random.choice(accessory_types)
        
        # Determine rarity based on chest tier
        rarities = list(chest_config["rarity_weights"].keys())
        weights = list(chest_config["rarity_weights"].values())
        rarity = random.choices(rarities, weights=weights, k=1)[0]
        
        # Generate prefix based on rarity
        prefixes = {
            "Common": ["Basic", "Simple", "Standard", "Plain", "Ordinary"],
            "Uncommon": ["Fine", "Strong", "Sturdy", "Keen", "Reinforced"],
            "Rare": ["Exceptional", "Valuable", "Quality", "Refined", "Pristine"],
            "Epic": ["Magnificent", "Heroic", "Superior", "Masterful", "Elite"],
            "Legendary": ["Ancient", "Mythical", "Godly", "Supreme", "Ultimate"]
        }
        
        prefix = random.choice(prefixes[rarity])
        
        # Determine if item has an element
        elements = ["Fire", "Water", "Earth", "Air", "Lightning", "Ice", "Light", "Dark"]
        has_element = random.random() < 0.3
        element = random.choice(elements) if has_element else None
        
        # Build the full item name
        if element:
            full_name = f"{prefix} {element} {equip_name}"
        else:
            full_name = f"{prefix} {equip_name}"
        
        # Calculate effect value based on rarity
        effect_value = {
            "Common": random.randint(1, 5),
            "Uncommon": random.randint(5, 10),
            "Rare": random.randint(10, 20),
            "Epic": random.randint(20, 30),
            "Legendary": random.randint(30, 50)
        }.get(rarity, 1)
        
        # Create equipment object
        equipment = {
            "name": full_name,
            "type": equip_type,
            "rarity": rarity,
            "effect": effect_value,
            "level": 1
        }
        
        if element:
            equipment["element"] = element
        
        loot_equipment.append(equipment)
    
    # Update global tracker for achievements
    if "treasure_chests_opened" not in user_data:
        user_data["treasure_chests_opened"] = 0
    user_data["treasure_chests_opened"] += 1
    
    # Update achievement progress
    if "achievements" in user_data and "progress" in user_data["achievements"]:
        if "treasure_chests_opened" not in user_data["achievements"]["progress"]:
            user_data["achievements"]["progress"]["treasure_chests_opened"] = 0
        user_data["achievements"]["progress"]["treasure_chests_opened"] += 1
    
    # Display loot
    print_animated(f"\n{LIGHTYELLOW}You found {gold_amount} gold!{ENDC}", delay=0.03)
    
    # Show equipment (most exciting first)
    if loot_equipment:
        print_animated(f"\n{CYAN}Equipment:{ENDC}", delay=0.03)
        for equip in loot_equipment:
            rarity_color = get_rarity_color(equip["rarity"])
            print_animated(f"- {rarity_color}{equip['name']}{ENDC} ({equip['rarity']} {equip['type'].capitalize()})", delay=0.03)
            
            # Add to player's equipment
            if "equipment" not in user_data:
                user_data["equipment"] = []
            user_data["equipment"].append(equip)
    
    # Show materials
    if loot_materials:
        print_animated(f"\n{GREEN}Materials:{ENDC}", delay=0.03)
        # Count duplicates
        material_counts = {}
        for material in loot_materials:
            material_counts[material] = material_counts.get(material, 0) + 1
            
        for material, count in material_counts.items():
            print_animated(f"- {material} x{count}", delay=0.02)
            
            # Add to inventory
            for _ in range(count):
                user_data["inventory"].append(material)
    
    # Show items
    if loot_items:
        print_animated(f"\n{LIGHTBLUE}Items:{ENDC}", delay=0.03)
        # Count duplicates
        item_counts = {}
        for item in loot_items:
            item_counts[item] = item_counts.get(item, 0) + 1
            
        for item, count in item_counts.items():
            print_animated(f"- {item} x{count}", delay=0.02)
            
            # Add to inventory
            for _ in range(count):
                user_data["inventory"].append(item)
    
    # For tracking unique items for achievements
    new_items = set(loot_items + loot_materials + [equip["name"] for equip in loot_equipment])
    if "all_collected_items" not in user_data:
        user_data["all_collected_items"] = []
    user_data["all_collected_items"].extend(list(new_items))
    
    # Check achievements
    check_achievements()
    
    print_animated(f"\n{GREEN}All items have been added to your inventory!{ENDC}", delay=0.03)

def check_artifact_set_bonuses() -> Dict[str, Dict[int, Dict[str, Any]]]:
    """Check for artifact set bonuses based on equipped artifacts"""
    equipped_artifacts = []

    # Get all equipped artifacts
    for slot in ARTIFACT_SLOTS:
        slot_key = f"artifact_{slot.lower()}"
        if user_data.get("equipped", {}).get(slot_key):
            equipped_artifacts.append(user_data["equipped"][slot_key]["name"])

    # Check each set for bonuses
    active_bonuses = {}
    for set_name, set_info in ARTIFACT_SETS.items():
        pieces = set_info.get("pieces", [])
        equipped_count = sum(1 for artifact in equipped_artifacts if artifact in pieces)

        # Check if any set bonuses are active
        for piece_count, bonus in set_info.get("bonuses", {}).items():
            if equipped_count >= piece_count:
                if set_name not in active_bonuses:
                    active_bonuses[set_name] = {}
                active_bonuses[set_name][piece_count] = bonus

    # Store active bonuses in user data
    user_data["active_set_bonuses"] = active_bonuses

    # Print active bonuses
    if active_bonuses:
        print_colored("\nActive Artifact Set Bonuses:", YELLOW)
        for set_name, bonuses in active_bonuses.items():
            for piece_count, bonus in bonuses.items():
                print(f"{set_name} ({piece_count}-piece): " + ", ".join([f"{stat}: {value}" for stat, value in bonus.items()]))
    
    return active_bonuses


# Function to use potions (elemental immunities, damage boosters, etc.)
def use_potion(potion_name: str) -> None:
    """Use a potion from inventory

    Args:
        potion_name: The name of the potion to use
    """
    # Check if we have the potion
    if potion_name not in user_data["inventory"]:
        print_colored(f"You don't have a {potion_name}.", FAIL)
        return

    # Check if it's a valid potion
    if potion_name not in POTION_RECIPES:
        print_colored(f"{potion_name} is not a usable potion.", FAIL)
        return

    potion_info = POTION_RECIPES[potion_name]
    effect = potion_info.get("effect", {})

    # Handle different potion effects
    if "immunity" in effect:
        element = effect["immunity"]

        # Initialize immunities if not present
        if "active_immunities" not in user_data:
            user_data["active_immunities"] = {}

        # Add immunity
        user_data["active_immunities"][element] = True
        print_colored(f"You are now immune to {element} damage for your next battle!", OKGREEN)

    elif "damage_boost" in effect:
        element = effect["damage_boost"]

        # Initialize boosters if not present
        if "element_boosters" not in user_data:
            user_data["element_boosters"] = {}

        # Add damage boost
        user_data["element_boosters"][element] = 2.0  # Double damage
        print_colored(f"Your {element} damage is doubled for your next battle!", OKGREEN)

    # Remove the potion from inventory
    user_data["inventory"].remove(potion_name)

# Artifact rarities
ARTIFACT_RARITIES = {
    "Common": {
        "color": Fore.CYAN,  # CYAN
        "stat_multiplier": 1.0,
        "drop_chance": 0.5
    },
    "Uncommon": {
        "color": Fore.GREEN,  # GREEN
        "stat_multiplier": 1.2,
        "drop_chance": 0.3
    },
    "Rare": {
        "color": Fore.BLUE,  # BLUE
        "stat_multiplier": 1.5,
        "drop_chance": 0.15
    },
    "Epic": {
        "color": Fore.MAGENTA,  # MAGENTA
        "stat_multiplier": 1.8,
        "drop_chance": 0.04
    },
    "Legendary": {
        "color": Fore.YELLOW,  # YELLOW
        "stat_multiplier": 2.0,
        "drop_chance": 0.01
    }
}

# Elemental potion recipes
POTION_RECIPES = {
    # Immunity Potions
    "Elixir of Cold": {
        "materials": {"Ice Crystal": 2, "Water Essence": 3, "Magical Herb": 1},
        "effect": {"immunity": "Ignis"},
        "description": "Grants immunity to Ignis (fire) damage for one battle",
        "type": "potion"
    },
    "Liquor Levitas": {
        "materials": {"Wind Crystal": 2, "Feather": 3, "Magical Herb": 1},
        "effect": {"immunity": "Gē"},
        "description": "Grants immunity to Gē (earth) damage for one battle",
        "type": "potion"
    },
    "Aura of Lightning": {
        "materials": {"Thunder Crystal": 2, "Metal Shard": 3, "Magical Herb": 1},
        "effect": {"immunity": "Aqua"},
        "description": "Grants immunity to Aqua (water) damage for one battle",
        "type": "potion"
    },
    "Essence of Drought": {
        "materials": {"Fire Crystal": 2, "Sand": 3, "Magical Herb": 1},
        "effect": {"immunity": "Aqua"},
        "description": "Grants immunity to Aqua (water) damage for one battle",
        "type": "potion"
    },
    "Potion of Grounding": {
        "materials": {"Earth Crystal": 2, "Iron Ore": 3, "Magical Herb": 1},
        "effect": {"immunity": "Fulmen"},
        "description": "Grants immunity to Fulmen (lightning) damage for one battle",
        "type": "potion"
    },
    "Essence of Heat": {
        "materials": {"Fire Crystal": 2, "Coal": 3, "Magical Herb": 1},
        "effect": {"immunity": "Glacies"},
        "description": "Grants immunity to Glacies (ice) damage for one battle",
        "type": "potion"
    },
    "Veil of Shadows": {
        "materials": {"Shadow Essence": 2, "Night Flower": 3, "Magical Herb": 1},
        "effect": {"immunity": "Lux"},
        "description": "Grants immunity to Lux (light) damage for one battle",
        "type": "potion"
    },
    "Radiant Elixir": {
        "materials": {"Light Crystal": 2, "Sun Petal": 3, "Magical Herb": 1},
        "effect": {"immunity": "Tenebrae"},
        "description": "Grants immunity to Tenebrae (darkness) damage for one battle",
        "type": "potion"
    },
    "Antidote Supreme": {
        "materials": {"Pure Water": 2, "Cleansing Herb": 3, "Magical Herb": 1},
        "effect": {"immunity": "Venēnum"},
        "description": "Grants immunity to Venēnum (poison) damage for one battle",
        "type": "potion"
    },
    "Rust Solution": {
        "materials": {"Acid Extract": 2, "Plant Root": 3, "Magical Herb": 1},
        "effect": {"immunity": "Ferrum"},
        "description": "Grants immunity to Ferrum (metal) damage for one battle",
        "type": "potion"
    },
    "Spirit Ward": {
        "materials": {"Soul Fragment": 2, "Holy Water": 3, "Magical Herb": 1},
        "effect": {"immunity": "Pneuma"},
        "description": "Grants immunity to Pneuma (spirit) damage for one battle",
        "type": "potion"
    },
    "Herbicide Mixture": {
        "materials": {"Toxic Extract": 2, "Mushroom Spore": 3, "Magical Herb": 1},
        "effect": {"immunity": "Viridia"},
        "description": "Grants immunity to Viridia (plant) damage for one battle",
        "type": "potion"
    },

    # Damage Booster Potions
    "Blazing Catalyst": {
        "materials": {"Fire Crystal": 3, "Dragon Scale": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Ignis"},
        "description": "Doubles your Ignis (fire) damage for one battle",
        "type": "potion"
    },
    "Tsunami Extract": {
        "materials": {"Water Essence": 3, "Sea Shell": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Aqua"},
        "description": "Doubles your Aqua (water) damage for one battle",
        "type": "potion"
    },
    "Earthen Might": {
        "materials": {"Earth Crystal": 3, "Mountain Stone": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Gē"},
        "description": "Doubles your Gē (earth) damage for one battle",
        "type": "potion"
    },
    "Tempest Brew": {
        "materials": {"Wind Crystal": 3, "Cloud Essence": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Aer"},
        "description": "Doubles your Aer (air) damage for one battle",
        "type": "potion"
    },
    "Voltaic Solution": {
        "materials": {"Thunder Crystal": 3, "Charged Core": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Fulmen"},
        "description": "Doubles your Fulmen (lightning) damage for one battle",
        "type": "potion"
    },
    "Frost Amplifier": {
        "materials": {"Ice Crystal": 3, "Frozen Heart": 1, "Magical Herb": 2},
        "effect": {"damage_boost": "Glacies"},
        "description": "Doubles your Glacies (ice) damage for one battle",
        "type": "potion"
    }
}

# Cooking recipes and their effects
COOKING_RECIPES = {
    "Hearty Stew": {
        "ingredients": {"Meat": 2, "Vegetables": 3, "Herbs": 1},
        "difficulty": "easy",
        "fail_chance": 0.1,
        "cook_time": 2,  # In game ticks
        "health_restore": 40,
        "stamina_restore": 30,
        "buffs": {"strength": 2},
        "buff_duration": 60,  # In game ticks
        "experience": 15,
        "description": "A filling meat stew that restores health and provides strength."
    },
    "Fish Soup": {
        "ingredients": {"Fish": 2, "Vegetables": 2, "Water": 1},
        "difficulty": "easy",
        "fail_chance": 0.15,
        "cook_time": 2,
        "health_restore": 30,
        "stamina_restore": 25,
        "buffs": {"agility": 2},
        "buff_duration": 50,
        "experience": 12,
        "description": "A light fish soup that increases agility."
    },
    "Forest Salad": {
        "ingredients": {"Vegetables": 3, "Mushrooms": 2, "Herbs": 1},
        "difficulty": "easy",
        "fail_chance": 0.05,
        "cook_time": 1,
        "health_restore": 20,
        "stamina_restore": 40,
        "buffs": {"perception": 3},
        "buff_duration": 70,
        "experience": 10,
        "description": "A fresh salad that sharpens your senses."
    },
    "Miner's Pie": {
        "ingredients": {"Meat": 1, "Vegetables": 3, "Wheat": 2},
        "difficulty": "medium",
        "fail_chance": 0.2,
        "cook_time": 3,
        "health_restore": 45,
        "stamina_restore": 35,
        "buffs": {"endurance": 3},
        "buff_duration": 90,
        "experience": 20,
        "description": "A hearty pie that improves endurance for mining."
    },
    "Warrior's Feast": {
        "ingredients": {"Meat": 3, "Fish": 1, "Vegetables": 2, "Herbs": 2},
        "difficulty": "medium",
        "fail_chance": 0.25,
        "cook_time": 4,
        "health_restore": 60,
        "stamina_restore": 50,
        "buffs": {"strength": 4, "endurance": 2},
        "buff_duration": 100,
        "experience": 30,
        "description": "A feast fit for warriors, providing significant combat bonuses."
    },
    "Wizard's Delight": {
        "ingredients": {"Mushrooms": 3, "Magic Herbs": 2, "Fruits": 2},
        "difficulty": "hard",
        "fail_chance": 0.3,
        "cook_time": 3,
        "health_restore": 30,
        "stamina_restore": 30,
        "mana_restore": 50,
        "buffs": {"intelligence": 5},
        "buff_duration": 120,
        "experience": 35,
        "description": "A magical dish that enhances spellcasting abilities."
    },
    "Dragon Breath Curry": {
        "ingredients": {"Meat": 2, "Dragon Fruit": 1, "Ghost Pepper": 3},
        "difficulty": "very hard",
        "fail_chance": 0.4,
        "cook_time": 5,
        "health_restore": 70,
        "stamina_restore": 60,
        "buffs": {"fire_resistance": 5, "strength": 3},
        "buff_duration": 150,
        "experience": 50,
        "description": "An extremely spicy curry that grants fire resistance."
    },
    "Frost Lotus Tea": {
        "ingredients": {"Frost Lotus": 2, "Water": 1, "Honey": 1},
        "difficulty": "medium",
        "fail_chance": 0.2,
        "cook_time": 2,
        "health_restore": 25,
        "stamina_restore": 20,
        "mana_restore": 40,
        "buffs": {"ice_resistance": 4},
        "buff_duration": 100,
        "experience": 25,
        "description": "A cooling tea that grants resistance to ice damage."
    },
    "Thunder Root Broth": {
        "ingredients": {"Thunderroot": 2, "Meat": 1, "Water": 1, "Herbs": 1},
        "difficulty": "hard",
        "fail_chance": 0.35,
        "cook_time": 4,
        "health_restore": 40,
        "stamina_restore": 35,
        "buffs": {"lightning_resistance": 4, "agility": 2},
        "buff_duration": 120,
        "experience": 40,
        "description": "A tingling broth that protects against lightning damage."
    },
    "Seasonal Harvest": {
        "ingredients": {"Spring Tulips": 1, "Summer Melon": 1, "Autumn Squash": 1, "Winter Mint": 1},
        "difficulty": "very hard",
        "fail_chance": 0.45,
        "cook_time": 6,
        "health_restore": 80,
        "stamina_restore": 80,
        "mana_restore": 80,
        "buffs": {"all_stats": 2},
        "buff_duration": 200,
        "experience": 60,
        "description": "A rare dish combining all seasons' bounty, providing resistance to all elements."
    }
}

# Failed cooking results
FAILED_COOKING = {
    "easy": {
        "name": "Burned Mess", 
        "health_restore": 5, 
        "description": "Slightly burned but still edible."
    },
    "medium": {
        "name": "Charred Disaster", 
        "health_restore": 0, 
        "description": "Completely ruined and barely edible."
    },
    "hard": {
        "name": "Inedible Catastrophe", 
        "health_restore": -5, 
        "description": "This might make you sick if you eat it."
    },
    "very hard": {
        "name": "Toxic Concoction", 
        "health_restore": -10, 
        "description": "This definitely looks dangerous to consume."
    }
}

# Enchantment types and their effects
ENCHANTMENTS = {
    # Weapon enchantments
    "Sharpness": {
        "description": "Increases weapon damage by 10% per level",
        "max_level": 5,
        "applicable_to": ["weapon"],
        "materials_per_level": {"Sharpening Stone": 2, "Magic Dust": 1}
    },
    "Elemental Fury": {
        "description": "Increases elemental damage by 10% per level", 
        "max_level": 5,
        "applicable_to": ["weapon"],
        "materials_per_level": {"Elemental Essence": 2, "Magic Crystal": 1}
    },
    "Giant Slayer": {
        "description": "Deals 15% more damage per level to large monsters",
        "max_level": 3,
        "applicable_to": ["weapon"],
        "materials_per_level": {"Giant's Tooth": 1, "Magic Dust": 2}
    },
    "Soul Stealer": {
        "description": "Has a 5% chance per level to steal health on hit",
        "max_level": 3,
        "applicable_to": ["weapon"],
        "materials_per_level": {"Spirit Essence": 2, "Blood Crystal": 1}
    },
    "Critical Eye": {
        "description": "Increases critical hit chance by a 5% per level",
        "max_level": 5,
        "applicable_to": ["weapon"],
        "materials_per_level": {"Hawk's Eye": 1, "Magic Dust": 2}
    },

    # Armor enchantments
    "Protection": {
        "description": "Reduces damage taken by 5% per level",
        "max_level": 5,
        "applicable_to": ["armor"],
        "materials_per_level": {"Steel Plate": 2, "Magic Dust": 1}
    },
    "Elemental Resist": {
        "description": "Reduces elemental damage by 10% per level",
        "max_level": 5,
        "applicable_to": ["armor"],
        "materials_per_level": {"Elemental Barrier": 2, "Magic Crystal": 1}
    },
    "Health Boost": {
        "description": "Increases maximum health by 10 per level",
        "max_level": 5,
        "applicable_to": ["armor"],
        "materials_per_level": {"Vitality Crystal": 1, "Magic Dust": 2}
    },
    "Thorns": {
        "description": "Deals 5% of damage back to attackers per level",
        "max_level": 3,
        "applicable_to": ["armor"],
        "materials_per_level": {"Thorned Vine": 2, "Magic Dust": 1}
    },
    "Evasion": {
        "description": "Increases dodge chance by 3% per level",
        "max_level": 5,
        "applicable_to": ["armor"],
        "materials_per_level": {"Swift Feather": 2, "Magic Dust": 1}
    }
}

# Random chest tiers and their potential contents
CHEST_TIERS = {
    "Common": {
        "gold_range": (10, 50),
        "item_count_range": (1, 2),
        "item_chances": {
            "material": 0.7,
            "potion": 0.2,
            "equipment": 0.1
        },
        "equipment_rarity_chances": {
            "Common": 0.8,
            "Uncommon": 0.2
        }
    },
    "Uncommon": {
        "gold_range": (30, 100),
        "item_count_range": (1, 3),
        "item_chances": {
            "material": 0.6,
            "potion": 0.3,
            "equipment": 0.1
        },
        "equipment_rarity_chances": {
            "Common": 0.6,
            "Uncommon": 0.3,
            "Rare": 0.1
        }
    },
    "Rare": {
        "gold_range": (75, 200),
        "item_count_range": (2, 4),
        "item_chances": {
            "material": 0.5,
            "potion": 0.3,
            "equipment": 0.15,
            "artifact": 0.05
        },
        "equipment_rarity_chances": {
            "Common": 0.3,
            "Uncommon": 0.5,
            "Rare": 0.2
        },
        "artifact_rarity_chances": {
            "Common": 0.6,
            "Uncommon": 0.3,
            "Rare": 0.1
        }
    },
    "Epic": {
        "gold_range": (150, 350),
        "item_count_range": (3, 5),
        "item_chances": {
            "material": 0.4,
            "potion": 0.3,
            "equipment": 0.2,
            "artifact": 0.1
        },
        "equipment_rarity_chances": {
            "Uncommon": 0.4,
            "Rare": 0.4,
            "Epic": 0.2
        },
        "artifact_rarity_chances": {
            "Uncommon": 0.5,
            "Rare": 0.3,
            "Epic": 0.2
        }
    },
    "Legendary": {
        "gold_range": (300, 800),
        "item_count_range": (4, 6),
        "item_chances": {
            "material": 0.3,
            "potion": 0.2,
            "equipment": 0.3,
            "artifact": 0.2
        },
        "equipment_rarity_chances": {
            "Rare": 0.4,
            "Epic": 0.4,
            "Legendary": 0.2
        },
        "artifact_rarity_chances": {
            "Rare": 0.5,
            "Epic": 0.3,
            "Legendary": 0.2
        }
    }
}

# Artifact set bonuses
ARTIFACT_SETS = {
    "Wisdom of the Ancients": {
        "pieces": ["Crown of Wisdom", "Timekeeper's Watch", "Band of Power"],
        "bonuses": {
            2: {"intelligence": 15, "cooldown_reduction": 0.1},
            3: {"intelligence": 30, "cooldown_reduction": 0.2, "max_mana": 50}
        }
    },
    "Eternal Flame": {
        "pieces": ["Ember Pendant", "Phoenix Plume", "Ring of Fire"],
        "bonuses": {
            2: {"fire_damage": 0.15, "fire_resistance": 0.15},
            3: {"fire_damage": 0.3, "fire_resistance": 0.3, "revival_chance": 0.5}
        }
    },
    "Nature's Embrace": {
        "pieces": ["Leaf Crown", "Eternal Bloom", "Vine Bracelet"],
        "bonuses": {
            2: {"health_regen": 10, "mana_regen": 5},
            3: {"health_regen": 20, "mana_regen": 10, "nature_control": True}
        }
    },
    
    # Weather Artifact Sets
    "Storm Chaser": {
        "pieces": ["Lightning Headpiece", "Thunder Pendant", "Cyclone Ring", "Storm Feather"],
        "bonuses": {
            2: {"lightning_damage": 0.15, "movement_speed": 0.1},
            3: {"lightning_damage": 0.25, "dodge_chance": 0.15},
            4: {"lightning_damage": 0.4, "weather_control": "Stormy", "special_ability": "Lightning Strike"}
        },
        "theme": "weather",
        "weather": "Stormy",
        "description": "Artifacts infused with the raw power of thunderstorms."
    },
    "Mist Walker": {
        "pieces": ["Ghostly Crown", "Shrouded Pendant", "Ethereal Clock", "Fog Essence"],
        "bonuses": {
            2: {"stealth": 0.2, "ghost_vision": True},
            3: {"critical_chance": 0.2, "phantom_step": True},
            4: {"stealth": 0.5, "weather_control": "Foggy", "special_ability": "Phantom Form"}
        },
        "theme": "weather",
        "weather": "Foggy",
        "description": "Artifacts that allow one to slip between the veil of mist and reality."
    },
    "Winter's Grasp": {
        "pieces": ["Frost Crown", "Blizzard Pendant", "Frozen Timepiece", "Ice Crystal"],
        "bonuses": {
            2: {"ice_damage": 0.15, "cold_resistance": 0.2},
            3: {"ice_damage": 0.3, "freeze_chance": 0.15},
            4: {"ice_damage": 0.4, "weather_control": "Snowy", "special_ability": "Freezing Aura"}
        },
        "theme": "weather",
        "weather": "Snowy",
        "description": "Artifacts that harness the biting cold of winter storms."
    },
    
    # Seasonal Artifact Sets
    "Spring Renewal": {
        "pieces": ["Blossom Crown", "Renewal Pendant", "Growth Timepiece", "Petal Essence"],
        "bonuses": {
            2: {"health_regen": 15, "nature_damage": 0.1},
            3: {"health_regen": 30, "growth_aura": True},
            4: {"health_regen": 50, "special_ability": "Rejuvenation", "season_bonus": "Spring"}
        },
        "theme": "seasonal",
        "season": "Spring",
        "description": "Artifacts that channel the rebirth and growth of springtime."
    },
    "Summer Solstice": {
        "pieces": ["Solar Crown", "Blazing Pendant", "Sundial", "Flame Feather"],
        "bonuses": {
            2: {"fire_damage": 0.15, "light_damage": 0.1},
            3: {"fire_damage": 0.25, "burn_chance": 0.2},
            4: {"fire_damage": 0.4, "special_ability": "Solar Flare", "season_bonus": "Summer"}
        },
        "theme": "seasonal",
        "season": "Summer",
        "description": "Artifacts that harness the intense heat and light of the summer sun."
    },
    "Autumn Harvest": {
        "pieces": ["Harvest Crown", "Amber Pendant", "Falling Leaf Clock", "Wheat Essence"],
        "bonuses": {
            2: {"earth_damage": 0.15, "resource_find": 0.2},
            3: {"earth_damage": 0.25, "abundance_aura": True},
            4: {"earth_damage": 0.4, "special_ability": "Cornucopia", "season_bonus": "Fall"}
        },
        "theme": "seasonal",
        "season": "Fall",
        "description": "Artifacts that embody the abundance and bounty of the harvest season."
    },
    "Winter Solstice": {
        "pieces": ["Frost Crown", "Crystal Pendant", "Frozen Clock", "Snow Essence"],
        "bonuses": {
            2: {"ice_damage": 0.15, "cold_resistance": 0.2},
            3: {"ice_damage": 0.25, "freeze_chance": 0.15},
            4: {"ice_damage": 0.4, "special_ability": "Blizzard", "season_bonus": "Winter"}
        },
        "theme": "seasonal",
        "season": "Winter",
        "description": "Artifacts that contain the quiet power and preservation of winter."
    },
    
    # Farming Artifact Sets
    "Bountiful Harvest": {
        "pieces": ["Farmer's Hat", "Soil Pendant", "Growth Clock", "Seed Pouch"],
        "bonuses": {
            2: {"farming_yield": 0.15, "growth_speed": 0.1},
            3: {"farming_yield": 0.25, "water_conservation": 0.2},
            4: {"farming_yield": 0.5, "special_ability": "Perfect Harvest"}
        },
        "theme": "farming",
        "description": "Artifacts that enhance one's connection to the soil and growing things."
    },
    "Weather Master": {
        "pieces": ["Cloud Crown", "Rain Pendant", "Sun Dial", "Wind Feather"],
        "bonuses": {
            2: {"weather_resistance": 0.2, "weather_sense": True},
            3: {"weather_resistance": 0.4, "weather_prediction": True},
            4: {"weather_resistance": 0.6, "special_ability": "Weather Shift"}
        },
        "theme": "farming",
        "description": "Artifacts that allow limited control over local weather patterns."
    }
}

# Enhanced crafting recipes with elemental weapons and artifacts
CRAFTING_RECIPES.update({
    # Weather and Season Related Items
    "Weather Amulet": {
        "materials": {"Weather Sample": 5, "Magic Crystal": 2, "Gold Ore": 3},
        "level_required": 10,
        "type": "accessory",
        "effect": 15,
        "special": "Grants a 20% chance to control weather once per day"
    },
    "Rainmaker Staff": {
        "materials": {"Weather Sample": 3, "Wood": 5, "Magic Crystal": 1, "Water Flask": 3},
        "level_required": 12,
        "type": "weapon",
        "effect": 12,
        "element": "Water",
        "special": "Can summon rain in dry areas"
    },
    "Seasonal Harvester": {
        "materials": {"Weather Sample": 2, "Steel Ingot": 3, "Magic Crystal": 1},
        "level_required": 8,
        "type": "tool",
        "special": "Increases harvest yield based on the current season"
    },
    "Farmer's Almanac": {
        "materials": {"Weather Sample": 1, "Paper": 10, "Magic Ink": 2},
        "level_required": 5,
        "type": "accessory",
        "special": "Shows optimal growing conditions for all crops"
    },
    "Weather Vane": {
        "materials": {"Iron Ore": 5, "Magic Crystal": 1},
        "level_required": 7,
        "type": "accessory",
        "special": "Predicts weather changes one day in advance"
    },
    "Storm Cloak": {
        "materials": {"Silk Thread": 10, "Magic Crystal": 2, "Weather Sample": 1},
        "level_required": 15,
        "type": "armor",
        "effect": 12,
        "element": "Lightning",
        "special": "Grants immunity to lightning damage"
    },
    "Fog Lantern": {
        "materials": {"Iron Ore": 2, "Glass": 3, "Magic Crystal": 1},
        "level_required": 10,
        "type": "accessory",
        "special": "Allows clear vision in fog and mist"
    },
    "Seasonal Boots": {
        "materials": {"Leather": 5, "Magic Crystal": 1, "Silk Thread": 3},
        "level_required": 12,
        "type": "armor",
        "effect": 8,
        "special": "Movement speed bonus changes with seasons"
    },
    "Weather Compass": {
        "materials": {"Iron Ore": 2, "Magic Crystal": 1, "Gold Ore": 1},
        "level_required": 6,
        "type": "accessory",
        "special": "Shows direction to nearest area with different weather"
    },
    "Cloudwalker Shoes": {
        "materials": {"Silk Thread": 8, "Magic Crystal": 2, "Weather Sample": 1},
        "level_required": 18,
        "type": "armor",
        "effect": 10,
        "special": "Reduces fall damage by 50%"
    },
    
    # Farming Equipment
    "Enhanced Hoe": {
        "materials": {"Iron Ore": 5, "Wood": 3, "Magic Crystal": 1},
        "level_required": 5,
        "type": "tool",
        "special": "Increases farming speed by 20%"
    },
    "Irrigation System": {
        "materials": {"Iron Ore": 8, "Clay": 5, "Glass": 2},
        "level_required": 8,
        "type": "tool",
        "special": "Automatically waters crops once per day"
    },
    "Scarecrow": {
        "materials": {"Wood": 5, "Cloth": 3, "Straw": 10},
        "level_required": 4,
        "type": "tool",
        "special": "Protects crops from birds and small pests"
    },
    "Greenhouse Glass": {
        "materials": {"Sand": 10, "Magic Crystal": 2, "Clay": 3},
        "level_required": 12,
        "type": "material",
        "special": "Used to build greenhouses for off-season farming"
    },
    "Crop Rotator": {
        "materials": {"Iron Ore": 3, "Magic Crystal": 1, "Gears": 5},
        "level_required": 15,
        "type": "tool",
        "special": "Automatically cycles crops to prevent soil depletion"
    },
    
    # Legendary Weapons
    "Void Blade": {
        "materials": {"Void Crystal": 3, "Dark Legion's Heart": 1, "Magic Crystal": 5},
        "level_required": 25,
        "type": "weapon",
        "effect": 60,
        "element": "Tenebrae"
    },
    "Dragon God Armor": {
        "materials": {"Divine Dragon Scale": 5, "Dragon God's Crown": 1, "Gold Ore": 10},
        "level_required": 30,
        "type": "armor",
        "effect": 50
    },
    "Phoenix Wings": {
        "materials": {"Eternal Flame": 3, "Phoenix Crown": 1, "Magic Crystal": 8},
        "level_required": 28,
        "type": "armor",
        "effect": 45
    },
    
    # Weather-based Equipment
    "Storm Caller": {
        "materials": {"Storm Crystal": 5, "Lightning Wyvern Scale": 2, "Magic Crystal": 3},
        "level_required": 20,
        "type": "weapon",
        "effect": 40,
        "element": "Fulmen",
        "special": "Increased damage during stormy weather",
        "weather_bonus": {"Stormy": 1.5}
    },
    "Mist Veil": {
        "materials": {"Mist Essence": 5, "Ghost Cloth": 3, "Ethereal Essence": 2},
        "level_required": 18,
        "type": "armor",
        "effect": 30,
        "element": "Pneuma",
        "special": "Partial invisibility during foggy weather",
        "weather_bonus": {"Foggy": 1.5}
    },
    "Frost Fang": {
        "materials": {"Frozen Heart": 2, "Ice Crystal": 5, "Wolf Fang": 3},
        "level_required": 22,
        "type": "weapon",
        "effect": 35,
        "element": "Glacies",
        "special": "Chance to freeze enemies during snowy weather",
        "weather_bonus": {"Snowy": 1.5}
    },
    "Solar Flare": {
        "materials": {"Radiant Core": 3, "Bright Crystal": 4, "Gold Ore": 5},
        "level_required": 21,
        "type": "weapon",
        "effect": 32,
        "element": "Lux",
        "special": "Burning effect during sunny weather",
        "weather_bonus": {"Sunny": 1.5}
    },
    "Windwalker Boots": {
        "materials": {"Razor Feather": 6, "Wind Crystal": 3, "Leather": 4},
        "level_required": 19,
        "type": "armor",
        "effect": 25,
        "element": "Aer",
        "special": "Increased movement speed during windy weather",
        "weather_bonus": {"Windy": 1.5}
    },
    "Earthen Shield": {
        "materials": {"Clay Core": 4, "Mud Stone": 3, "Iron Ore": 5},
        "level_required": 20,
        "type": "armor",
        "effect": 35,
        "element": "Gē",
        "special": "Increased defense during rainy weather",
        "weather_bonus": {"Rainy": 1.5}
    },
    "Skyweaver Staff": {
        "materials": {"Cloud Fragment": 5, "Sky Essence": 3, "Ancient Wood": 2},
        "level_required": 19,
        "type": "weapon",
        "effect": 30,
        "element": "Aer",
        "special": "Increased magic power during cloudy weather",
        "weather_bonus": {"Cloudy": 1.5}
    },
    
    # Seasonal Equipment
    "Winter's Embrace": {
        "materials": {"Frost Crown": 1, "Winter Essence": 5, "Silver Ore": 3},
        "level_required": 25,
        "type": "armor",
        "effect": 40,
        "element": "Glacies",
        "special": "Cold resistance and ice damage during winter",
        "season_bonus": {"Winter": 1.5}
    },
    "Spring Bloom Wand": {
        "materials": {"Petal Crown": 1, "Spring Essence": 5, "Living Wood": 3},
        "level_required": 24,
        "type": "weapon",
        "effect": 38,
        "element": "Viridia",
        "special": "Healing effect during spring",
        "season_bonus": {"Spring": 1.5}
    },
    "Summer Inferno": {
        "materials": {"Burning Scale": 2, "Summer Essence": 5, "Fire Crystal": 3},
        "level_required": 26,
        "type": "weapon",
        "effect": 42,
        "element": "Ignis",
        "special": "Burning aura during summer",
        "season_bonus": {"Summer": 1.5}
    },
    "Autumn Harvester": {
        "materials": {"Harvest Crown": 1, "Autumn Essence": 5, "Ancient Wood": 3},
        "level_required": 25,
        "type": "weapon",
        "effect": 40,
        "element": "Gē",
        "special": "Resource gathering bonus during fall",
        "season_bonus": {"Fall": 1.5}
    },
    
    # Farming Tools and Equipment
    "Enchanted Hoe": {
        "materials": {"Iron Ingot": 3, "Magic Crystal": 2, "Ancient Wood": 1},
        "level_required": 15,
        "type": "tool",
        "effect": 20,
        "special": "Increases farming yield by 20%"
    },
    "Seasonal Planter": {
        "materials": {"Spring Essence": 1, "Summer Essence": 1, "Autumn Essence": 1, "Winter Essence": 1, "Wood": 5},
        "level_required": 20,
        "type": "tool",
        "effect": 30,
        "special": "Allows growing crops regardless of season"
    },
    "Weather-Resistant Gloves": {
        "materials": {"Storm Crystal": 1, "Sunlight Fragment": 1, "Snow Flake": 1, "Leather": 3},
        "level_required": 18,
        "type": "armor",
        "effect": 15,
        "special": "Protects crops from adverse weather effects"
    },
    "Seed Pouch": {
        "materials": {"Leather": 5, "Cloth": 3, "Magic Crystal": 1},
        "level_required": 10,
        "type": "accessory",
        "effect": 10,
        "special": "Increases seed storage capacity"
    },
    
    # Artifact Crafting
    "Weather Attunement Crystal": {
        "materials": {"Storm Crystal": 1, "Sunlight Fragment": 1, "Ice Crystal": 1, "Wind Crystal": 1, "Rain Drop": 1},
        "level_required": 25,
        "type": "artifact_component",
        "effect": 0,
        "special": "Used to craft weather-attuned artifacts"
    },
    "Seasonal Essence Blend": {
        "materials": {"Spring Essence": 1, "Summer Essence": 1, "Autumn Essence": 1, "Winter Essence": 1},
        "level_required": 25,
        "type": "artifact_component",
        "effect": 0,
        "special": "Used to craft season-attuned artifacts"
    },
    
    # New Artifact Pieces
    "Lightning Headpiece": {
        "materials": {"Weather Attunement Crystal": 1, "Storm Crystal": 3, "Gold Ore": 5},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Storm Chaser artifact set",
        "slot": "Headset"
    },
    "Thunder Pendant": {
        "materials": {"Weather Attunement Crystal": 1, "Storm Crystal": 2, "Silver Ore": 5},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Storm Chaser artifact set",
        "slot": "Necklace"
    },
    "Cyclone Ring": {
        "materials": {"Weather Attunement Crystal": 1, "Wind Crystal": 3, "Gold Ore": 3},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Storm Chaser artifact set",
        "slot": "Ring"
    },
    "Storm Feather": {
        "materials": {"Weather Attunement Crystal": 1, "Razor Feather": 3, "Lightning Crystal": 2},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Storm Chaser artifact set",
        "slot": "Feather"
    },
    "Blossom Crown": {
        "materials": {"Seasonal Essence Blend": 1, "Spring Essence": 3, "Flower Petal": 5},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Spring Renewal artifact set",
        "slot": "Headset"
    },
    "Renewal Pendant": {
        "materials": {"Seasonal Essence Blend": 1, "Spring Essence": 2, "Silver Ore": 5},
        "level_required": 30,
        "type": "artifact",
        "effect": 25,
        "special": "Part of the Spring Renewal artifact set",
        "slot": "Necklace"
    },
    "Chaos Armor": {
        "materials": {"Chaos Crystal": 5, "Chaos Blade": 1, "Gold Ore": 15},
        "level_required": 35,
        "type": "armor",
        "effect": 55
    },
    "Legendary Sword": {
        "materials": {"Dragon Scale": 5, "Magic Crystal": 3, "Gold Ore": 2},
        "level_required": 20,
        "type": "weapon",
        "effect": 50,
        "element": "Ignis"
    },
    "Phoenix Armor": {
        "materials": {"Phoenix Feather": 3, "Magic Crystal": 2, "Gold Ore": 3},
        "level_required": 25,
        "type": "armor",
        "effect": 40
    },
    "Dragon Slayer Bow": {
        "materials": {"Dragon Scale": 3, "Magic Crystal": 2, "Wood": 4},
        "level_required": 22,
        "type": "weapon",
        "effect": 45,
        "element": "Aer"
    },

    # Elemental Weapons
    "Flame Sword": {
        "materials": {"Fire Crystal": 3, "Iron Ore": 5, "Wood": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Ignis"
    },
    "Frost Blade": {
        "materials": {"Ice Crystal": 3, "Iron Ore": 5, "Wood": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Glacies"
    },
    "Lightning Staff": {
        "materials": {"Thunder Crystal": 3, "Magic Wood": 5, "Crystal Shard": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Fulmen"
    },
    "Nature Scythe": {
        "materials": {"Plant Extract": 3, "Strong Wood": 5, "Silk": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Viridia"
    },
    "Earth Mace": {
        "materials": {"Earth Crystal": 3, "Iron Ore": 5, "Leather": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Gē"
    },
    "Wind Bow": {
        "materials": {"Wind Crystal": 3, "Flexible Wood": 5, "Silk": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Aer"
    },
    "Water Trident": {
        "materials": {"Water Essence": 3, "Iron Ore": 5, "Shell": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Aqua"
    },
    "Light Wand": {
        "materials": {"Light Crystal": 3, "Magic Wood": 5, "Gold Ore": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Lux"
    },
    "Shadow Dagger": {
        "materials": {"Shadow Essence": 3, "Dark Metal": 5, "Leather": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Tenebrae"
    },
    "Venomous Blade": {
        "materials": {"Poison Gland": 3, "Iron Ore": 5, "Leather": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Venēnum"
    },
    "Steel Hammer": {
        "materials": {"Steel Ingot": 3, "Iron Ore": 5, "Wood": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Ferrum"
    },
    "Spirit Blade": {
        "materials": {"Soul Fragment": 3, "Magic Crystal": 5, "Pure Metal": 2},
        "level_required": 15,
        "type": "weapon",
        "effect": 35,
        "element": "Pneuma"
    },

    # Artifacts
    "Crown of Wisdom": {
        "materials": {"Magic Crystal": 2, "Gold Ore": 3, "Pure Gem": 1},
        "level_required": 10,
        "type": "artifact",
        "slot": "Headset",
        "effect": {"intelligence": 10},
        "rarity": "Rare"
    },
    "Ember Pendant": {
        "materials": {"Fire Crystal": 2, "Silver Ore": 3, "Red Gem": 1},
        "level_required": 10,
        "type": "artifact",
        "slot": "Necklace",
        "effect": {"fire_resist": 0.15},
        "rarity": "Uncommon"
    },
    "Timekeeper's Watch": {
        "materials": {"Magic Gear": 2, "Gold Ore": 3, "Time Crystal": 1},
        "level_required": 15,
        "type": "artifact",
        "slot": "Clock",
        "effect": {"cooldown_reduction": 0.1},
        "rarity": "Rare"
    },
    "Eternal Bloom": {
        "materials": {"Plant Extract": 2, "Water Essence": 3, "Life Crystal": 1},
        "level_required": 15,
        "type": "artifact",
        "slot": "Flower",
        "effect": {"health_regen": 5},
        "rarity": "Uncommon"
    },
    "Phoenix Plume": {
        "materials": {"Phoenix Feather": 1, "Magic Crystal": 2, "Fire Crystal": 3},
        "level_required": 20,
        "type": "artifact",
        "slot": "Feather",
        "effect": {"revival_chance": 0.2},
        "rarity": "Epic"
    },
    "Band of Power": {
        "materials": {"Magic Metal": 2, "Strength Crystal": 3, "Blue Gem": 1},
        "level_required": 10,
        "type": "artifact",
        "slot": "Ring",
        "effect": {"attack": 8},
        "rarity": "Uncommon"
    }
})

# Add more elemental crafting recipes
CRAFTING_RECIPES.update({
    # Elemental Weapons
    "Flame Sword": {
        "materials": {"Iron Ore": 3, "Magic Crystal": 2, "Fire Essence": 1},
        "level_required": 10,
        "type": "weapon",
        "effect": 15,
        "element": "Fire",
        "special": "Has a 15% chance to inflict Burn status"
    },
    "Frost Axe": {
        "materials": {"Iron Ore": 4, "Magic Crystal": 2, "Water Flask": 2},
        "level_required": 12,
        "type": "weapon",
        "effect": 17,
        "element": "Ice",
        "special": "Has a 15% chance to inflict Freeze status"
    },
    "Thunder Bow": {
        "materials": {"Wood": 5, "Silk Thread": 3, "Magic Crystal": 2},
        "level_required": 14,
        "type": "weapon",
        "effect": 16,
        "element": "Lightning",
        "special": "Has a 15% chance to stun enemies"
    },
    "Earthen Mace": {
        "materials": {"Iron Ore": 5, "Stone": 10, "Magic Crystal": 1},
        "level_required": 10,
        "type": "weapon",
        "effect": 18,
        "element": "Earth",
        "special": "Has a 20% chance to add extra crushing damage"
    },
    "Wind Dagger": {
        "materials": {"Iron Ore": 2, "Silk Thread": 5, "Magic Crystal": 2},
        "level_required": 11,
        "type": "weapon",
        "effect": 12,
        "element": "Wind",
        "special": "Doubles critical hit chance"
    },
    
    # Elemental Armor
    "Flame-Forged Breastplate": {
        "materials": {"Iron Ore": 8, "Magic Crystal": 3, "Fire Essence": 2},
        "level_required": 15,
        "type": "armor",
        "effect": 20,
        "element": "Fire",
        "special": "Reduces Fire damage by 30%"
    },
    "Frost Mantle": {
        "materials": {"Silk Thread": 10, "Magic Crystal": 3, "Water Flask": 3},
        "level_required": 15,
        "type": "armor",
        "effect": 18,
        "element": "Ice",
        "special": "Reduces Ice damage by 30%"
    },
    "Thunder Plate": {
        "materials": {"Iron Ore": 8, "Magic Crystal": 3, "Weather Sample": 2},
        "level_required": 15,
        "type": "armor",
        "effect": 19,
        "element": "Lightning",
        "special": "Reduces Lightning damage by 30%"
    },
    "Stone Skin Armor": {
        "materials": {"Iron Ore": 6, "Stone": 12, "Magic Crystal": 3},
        "level_required": 15,
        "type": "armor",
        "effect": 22,
        "element": "Earth",
        "special": "Reduces Earth damage by 30%"
    },
    "Windrider Vest": {
        "materials": {"Leather": 8, "Silk Thread": 6, "Magic Crystal": 3},
        "level_required": 15,
        "type": "armor",
        "effect": 16,
        "element": "Wind",
        "special": "Reduces Wind damage by 30% and increases movement speed by 10%"
    },
    
    # Advanced Farming Tools
    "Weather-Sensitive Plow": {
        "materials": {"Iron Ore": 8, "Wood": 5, "Weather Sample": 2, "Magic Crystal": 1},
        "level_required": 12,
        "type": "tool",
        "special": "Adapts to current weather to optimize tilling"
    },
    "Season Cycler": {
        "materials": {"Magic Crystal": 3, "Gold Ore": 2, "Weather Sample": 1},
        "level_required": 18,
        "type": "tool",
        "special": "Can grow any seasonal crop regardless of current season"
    },
    "Crop Enhancer": {
        "materials": {"Magic Crystal": 2, "Red Herb": 5, "Blue Herb": 5, "Green Herb": 5},
        "level_required": 10,
        "type": "tool",
        "special": "Improves crop quality by one tier"
    }
})

dungeons = [
    # Greenwood Village Dungeons
    {"name": "Goblin's Hideout", "monsters": ["Goblin", "Wolf"], "loot": ["Wooden Sword", "Wolf Pelt", "Gold Coin"]},
    {"name": "Bandit Camp", "monsters": ["Bandit"], "loot": ["Leather Armor", "Gold Coin"]},
    {"name": "Forest Spider Den", "monsters": ["Forest Spider"], "loot": ["Spider Silk", "Gold Coin"]},
    {"name": "Ancient Ruins", "monsters": ["Forest Spider", "Goblin"], "loot": ["Ancient Relic", "Gold Coin"]},
    {"name": "Goblin Fortress", "monsters": ["Goblin", "Dire Wolf"], "loot": ["Goblin Staff", "Gold Coin"]},
    {"name": "Cave of Shadows", "monsters": ["Goblin Shaman"], "loot": ["Gold Coin", "Goblin Staff"]},
    {"name": "Goblin King's castle", "monsters": ["Goblin King"], "loot": ["Goblin King's Crown", "Gold Coin"]},

    # Stormhaven Dungeons
    {"name": "Haunted Crypt", "monsters": ["Skeleton", "Ghost"], "loot": ["Bone Armor", "Spirit Essence", "Gold Coin"]},
    {"name": "Pirate's Cove", "monsters": ["Pirate Scout"], "loot": ["Cutlass", "Gold Coin"]},
    {"name": "Storm Fortress", "monsters": ["Storm Elemental"], "loot": ["Storm Crystal", "Gold Coin"]},
    {"name": "Cursed Shipwreck", "monsters": ["Haunted Armor"], "loot": ["Cursed Shield", "Gold Coin"]},
    {"name": "Ghost Ship", "monsters": ["Sea Serpent"], "loot": ["Serpent Scale", "Gold Coin"]},
    {"name": "Dreadlord's Sunken Ship", "monsters": ["Dreadlord Varkhull, the Crimson Abyss Pirate Captain"], "loot": ["Crimson Cutlass", "Gold Coin"]},
    {"name": "Cursed Lighthouse", "monsters": ["Haunted Armor", "Ghost"], "loot": ["Cursed Shield", "Gold Coin"]},
    {"name": "Cursed Graveyard", "monsters": ["Skeleton", "Ghost"], "loot": ["Bone Armor", "Spirit Essence", "Gold Coin"]},

    # Dragon's Peak Dungeons
    {"name": "Fire Dragon's Lair", "monsters": ["Fire Dragon"], "loot": ["Dragon Scale", "Flame Sword", "Gold Coin"]},
    {"name": "Ice Dragon's Nest", "monsters": ["Ice Dragon"], "loot": ["Dragon Scale", "Ice Sword", "Gold Coin"]},
    {"name": "Electrical Dragon's Roost", "monsters": ["Electrical Dragon"], "loot": ["Dragon Scale", "Lightning Sword", "Gold Coin"]},
    {"name": "Plant Dragon's Grove", "monsters": ["Plant Dragon"], "loot": ["Dragon Scale", "Nature Sword", "Gold Coin"]},
    {"name": "Earth Dragon's Cavern", "monsters": ["Earth Dragon"], "loot": ["Dragon Scale", "Earth Sword", "Gold Coin"]},
    {"name": "Wind Dragon's Summit", "monsters": ["Wind Dragon"], "loot": ["Dragon Scale", "Wind Sword", "Gold Coin"]},
    {"name": "Water Dragon's Abyss", "monsters": ["Water Dragon"], "loot": ["Dragon Scale", "Water Sword", "Gold Coin"]},
    {"name": "Fire Wyvern Nest", "monsters": ["Fire Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ice Wyvern Cave", "monsters": ["Ice Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Wyvern Peak", "monsters": ["Thunder Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Earth Wyvern Den", "monsters": ["Earth Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Dragon Knight's Fortress", "monsters": ["Dragon Knight"], "loot": ["Dragon Armor", "Gold Coin"]},
    {"name": "Water Wyvern Lagoon", "monsters": ["Water Wyvern"], "loot": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Dragon Overlord's Lair", "monsters": ["Dragon Overlord"], "loot": ["Dragon Scale", "Dragonfire Sword", "Gold Coin"]},

    # Crystal Cave Dungeons
    {"name": "Crystal Depths", "monsters": ["Crystal Golem", "Cave Troll"], "loot": ["Crystal Shard", "Troll Hide", "Gold Coin"]},
    {"name": "Cave of Echoes", "monsters": ["Crystal Spider", "Rock Elemental"], "loot": ["Crystal Web", "Earth Stone", "Gold Coin"]},
    {"name": "Crystal Cavern", "monsters": ["Cave Bat", "Crystal Tarantula"], "loot": ["Bat Wing", "Crystal Fang", "Gold Coin"]},
    {"name": "Crystal Golem's Lair", "monsters": ["Crystal Giant Tarantula"], "loot": ["Crystal Eye", "Gold Coin"]},
    {"name": "Serpent's Lair", "monsters": ["Crystal Serpent"], "loot": ["Serpent Scale", "Gold Coin"]},
    {"name": "Corrupted Miner's Hideout", "monsters": ["Corrupted Miner"], "loot": ["Miner's Pickaxe", "Gold Coin"]},
    {"name": "Crystal Cavern", "monsters": ["Crystal Golem", "Cave Troll"], "loot": ["Crystal Shard", "Troll Hide", "Gold Coin"]},

    # Shadowmere Dungeons
    {"name": "Shadow Keep", "monsters": ["Shadow Beast", "Dark Knight"], "loot": ["Shadow Essence", "Dark Armor", "Gold Coin"]},
    {"name": "Wraith's Lair", "monsters": ["Wraith"], "loot": ["Soul Gem", "Gold Coin"]},
    {"name": "Night Stalker Den", "monsters": ["Night Stalker"], "loot": ["Night Blade", "Gold Coin"]},
    {"name": "Assassin's Hideout", "monsters": ["Shadow Assassin"], "loot": ["Assassin's Dagger", "Gold Coin"]},
    {"name": "Dark Fortress", "monsters": ["Dark Knight"], "loot": ["Dark Armor", "Gold Coin"]},
    {"name": "Vampire's Crypt", "monsters": ["Vampire"], "loot": ["Vampire Fang", "Gold Coin"]},
    {"name": "Undead Fortress", "monsters": ["Undead Knight"], "loot": ["Undead Blade", "Gold Coin"]},
    {"name": "Undead Army Base", "monsters": ["Undead Army General","Undead Army Commander"], "loot": ["Undead Armor", "Gold Coin"]},

    # Frostvale Dungeons
    {"name": "Frozen Halls", "monsters": ["Ice Troll", "Frost Giant"], "loot": ["Frozen Heart", "Giant's Club", "Gold Coin"]},
    {"name": "Snowy Cavern", "monsters": ["Snow Wolf", "Ice Elemental"], "loot": ["Frost Pelt", "Ice Crystal", "Gold Coin"]},
    {"name": "Frost Wraith's Lair", "monsters": ["Frost Wraith"], "loot": ["Wraith Essence", "Gold Coin"]},
    {"name": "Troll's Den", "monsters": ["Ice Troll"], "loot": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost Revenant", "monsters": ["Ice Revenant"], "loot": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frozen Eye Cave", "monsters": ["Frost vengeful eye of the snow"], "loot": ["Frost Eye", "Gold Coin"]},

    # Silent Ashes Dungeons
    {"name": "Ash Ruins", "monsters": ["Ash Revenant", "Cursed Wanderer"], "loot": ["Ancient Relic", "Cursed Gem", "Gold Coin"]},
    {"name": "Phoenix Nest", "monsters": ["Phoenix"], "loot": ["Phoenix Feather", "Gold Coin"]},
    {"name": "Ash Wraith's Den", "monsters": ["Ash Wraith"], "loot": ["Wraith Essence", "Gold Coin"]},
    {"name": "Guardian's Ash Fortress", "monsters": ["Burnt Guardian"], "loot": ["Guardian's Ash", "Gold Coin"]},
    {"name": "Magmatic Knight's Lair", "monsters": ["Magmatic Knight,The fallen knight of the ashes"], "loot": ["Knight's Ash", "Gold Coin"]},
    {"name": "Vision of the Thunder Cave", "monsters": ["Vision of the Thunder,the core of the storm"], "loot": ["Storm Eye", "Gold Coin"]},

    # Long Shui Zhen Dungeons
    {"name": "Water Palace", "monsters": ["Water Elemental", "Jade Warrior"], "loot": ["Water Essence", "Jade Sword", "Gold Coin"]},
    {"name": "Dragon Temple", "monsters": ["Dragon Spirit"], "loot": ["Spirit Pearl", "Gold Coin"]},
    {"name": "Jade General's Fortress", "monsters": ["Jade General","Jade Soldier"], "loot": ["Jade Armor", "Gold Coin"]},
    {"name": "Jade Emperor's Chamber", "monsters": ["Jade Emperor", "Jade Emperor's Guard"], "loot": ["Jade Crown", "Gold Coin"]},
    {"name": "Long Shui Zhen's well", "monsters": ["Legendary Dragon"], "loot": ["Dragon Scale", "Legendary Sword"]},

    # Jade Lotus Village Dungeons
    {"name": "Lotus Sanctuary", "monsters": ["Lotus Spirit", "Pond Serpent"], "loot": ["Lotus Petal", "Serpent Scale", "Gold Coin"]},
    {"name": "Garden of Spirits", "monsters": ["Garden Guardian"], "loot": ["Sacred Charm", "Gold Coin"]},
    {"name": "Lotus Shrine", "monsters": ["Lotus Guardian"], "loot": ["Lotus Shield", "Gold Coin"]},
    {"name": "Koi Pond", "monsters": ["Koi Empress"], "loot": ["Koi Scale", "Gold Coin"]},

    # Thundercliff Hold Dungeons
    {"name": "Storm Fortress", "monsters": ["Thunder Elemental", "Rock Wyvern"], "loot": ["Storm Crystal", "Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Mage's Tower", "monsters": ["Thunder Mage"], "loot": ["Thunder Staff", "Gold Coin"]},
    {"name": "Storm Wyvern Nest", "monsters": ["Storm Wyvern"], "loot": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Storm Guardian's Keep", "monsters": ["Storm Guardian"], "loot": ["Guardian's Storm", "Gold Coin"]},

    # Ember Hollow Dungeons
    {"name": "Lava Cavern", "monsters": ["Lava Hound", "Molten Wraith"], "loot": ["Lava Stone", "Gold Coin"]},
    {"name": "Ember Fortress", "monsters": ["Fire Elemental"], "loot": ["Ember Crystal", "Gold Coin"]},
    {"name": "Ashen Ruins", "monsters": ["Ash Elemental"], "loot": ["Ashen Gem", "Gold Coin"]},
    {"name": "Fire Wyvern Nest", "monsters": ["Fire Wyvern"], "loot": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ember Dragon's Lair", "monsters": ["Ember Dragon"], "loot": ["Dragon Scale", "Gold Coin"]},

    # Shogunate Of Shirui Dungeons
    {"name": "Shogun's Fortress", "monsters": ["The Shogun", "Shogun's Guard"], "loot": ["Samurai Armor", "Shogun's Blade", "Gold Coin"]},
    {"name": "Kitsune Shrine", "monsters": ["Kitsune Warrior"], "loot": ["Kitsune Mask", "Gold Coin"]},
    {"name": "Jade Temple", "monsters": ["Jade Samurai"], "loot": ["Jade Armor", "Gold Coin"]},
    {"name": "Tengu's Nest", "monsters": ["Tengu Warrior"], "loot": ["Tengu Feather", "Gold Coin"]},
    {"name": "Kappa's Cave", "monsters": ["Kappa Guardian"], "loot": ["Kappa Shell", "Gold Coin"]},
    {"name": "Oni's Lair", "monsters": ["Oni Berserker"], "loot": ["Oni Mask", "Gold Coin"]},
    {"name": "Corrupted Ninja's Hideout", "monsters": ["Corrupted Ninja"], "loot": ["Ninja Star", "Gold Coin"]},
    {"name": "Shadow Samurai's Fortress", "monsters": ["Shadow Samurai"], "loot": ["Shadow Blade", "Gold Coin"]},
    {"name": "Possessed Katana's Lair", "monsters": ["Possessed Katana"], "loot": ["Cursed Katana", "Gold Coin"]},

    # The Iron Caliphate of Al-Khilafah Al-Hadidiyah Dungeons
    {"name": "Caliph's Palace", "monsters": ["Az-Zālim al-Muqaddas,The Caliph of Al-Khilafah Al-Hadidiyah"], "loot": ["Iron Caliph's Crown", "Gold Coin"]},
    {"name": "Guardian's Keep", "monsters": ["Al-Hadidiyah Guardian"], "loot": ["Guardian's Blade", "Gold Coin"]},
    {"name": "Knight's Barracks", "monsters": ["Al-Hadidiyah Knight"], "loot": ["Knight's Shield", "Gold Coin"]},
    {"name": "Mercenary Camp", "monsters": ["Mercenary of the caliphate"], "loot": ["Mercenary's Dagger", "Gold Coin"]},
    {"name": "Loyalist's mosque", "monsters": ["Loyalist of the caliphate", "High Priest of the caliphate"], "loot": ["Loyalist's Blade", "High Priest's Staff", "Gold Coin"]},
    {"name": "Sorcerer's Tower", "monsters": ["Al-Hadidiyah Sorcerer"], "loot": ["Sorcerer's Tome", "Gold Coin"]},
    {"name": "Factory of golems", "monsters": ["Steel Golem"], "loot": ["Steel Core", "Gold Coin"]},
    {"name": "Janissary Barracks", "monsters": ["Royal Janissary"], "loot": ["Janissary's Blade", "Gold Coin"]},
    {"name": "General's Fortress", "monsters": ["Iron Caliphate General", "Al-Hadidiyah Knight","Mercenary of the caliphate"], "loot": ["General's Armor", "Gold Coin"]},

    # Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains Dungeons
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Palace", "monsters": ["Tēcpatl Tlamacazqui,The Emperor of the Sacred Fire and Chains", "Secret Police from The Order of the Black Sun (Yohualli Tōnatiuh)","Tlācahcāyōtl Tletl Tecpanēcatl Knight"], "loot": ["Emperor's Crown", "Black Sun Dagger", "Knight's Shield", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Guardian's Keep", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl Guardian"], "loot": ["Guardian's Blade", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Sorcerer's Tower", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl Sorcerer"], "loot": ["Sorcerer's Tome", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl High Priest's Sanctuary", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl High Priest"], "loot": ["High Priest's Staff", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Mercenary Camp", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl Mercenary"], "loot": ["Mercenary's Dagger", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Loyalist Town", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl Loyalist"], "loot": ["Loyalist's Blade", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Royal Guard's Fortress", "monsters": ["Tlācahcāyōtl Tletl Tecpanēcatl Royal Guard"], "loot": ["Royal Guard's Sword", "Gold Coin"]},

    # Crimson Abyss Dungeons
    {"name": "Crimson Abyss Fortress", "monsters": ["Crimson Abyss Demon", "Crimson Abyss Knight"], "loot": ["Demon's Heart", "Knight's Blade", "Gold Coin"]},
    {"name": "Crimson Abyss Sorcerer's Tower", "monsters": ["Crimson Abyss Sorcerer"], "loot": ["Sorcerer's Staff", "Gold Coin"]},
    {"name": "Crimson Abyss Guardian's Keep", "monsters": ["Crimson Abyss Guardian"], "loot": ["Guardian's Shield", "Gold Coin"]},
    {"name": "Abyssal Leviathan's Sunken Palace", "monsters": ["Abyssal Leviathan"], "loot": ["Leviathan Scale", "Gold Coin"]},

    # The Dark Legion Dungeons
    {"name": "Dark Legion Fortress", "monsters": ["Dark Legion Elite", "Dark Legion Warlock"], "loot": ["Dark Legion Armor", "Warlock Staff", "Gold Coin"]},
    {"name": "Dark Legion Citadel", "monsters": ["Dark Legion Elite", "Dark Legion Commander"], "loot": ["Dark Legion Armor", "Commander's Blade", "Gold Coin"]},
    {"name": "Warlock's Dark Spire", "monsters": ["Dark Legion Warlock", "Dark Legion Archpriest"], "loot": ["Warlock Staff", "Dark Tome", "Gold Coin"]},
    {"name": "Shadow Assassin's Den", "monsters": ["Dark Legion's Shadow Assassin"], "loot": ["Shadow Dagger", "Gold Coin"]},
    {"name": "The Eternal Throne", "monsters": ["Dark Legionary Supreme Lord:Noctis, the Obsidian Fallen Eternal"], "loot": ["Eternal Crown", "Obsidian Blade", "Dark Legion's Heart", "Gold Coin"]},

    # Post-game Dungeons
    {"name": "The Void Citadel", "monsters": ["Void Reaper", "Dark Legion Elite"], "loot": ["Void Scythe", "Void Crystal", "Void Armor"], "description": "A fortress suspended in the void between dimensions."},
    {"name": "Dragon God's Sanctuary", "monsters": ["Ancient Dragon God", "Dragon Elite Guard"], "loot": ["Divine Dragon Scale", "Dragon God's Crown", "Divine Armor"], "description": "The sacred realm where the first dragons originated."},
    {"name": "Eternal Phoenix Spire", "monsters": ["Eternal Phoenix", "Phoenix Guardian"], "loot": ["Eternal Flame", "Phoenix Crown", "Phoenix Wings"], "description": "A towering spire of eternal flame where the first phoenix was born."},
    {"name": "Chaos Nexus", "monsters": ["Chaos Incarnate", "Chaos Spawn"], "loot": ["Chaos Blade", "Chaos Crystal", "Chaos Armor"], "description": "The epicenter of all chaos in the universe."},
    {"name": "The Infinite Abyss", "monsters": ["Abyssal Overlord", "Abyss Dweller"], "loot": ["Abyssal Crown", "Infinity Stone", "Abyssal Armor"], "description": "An endless void where reality itself begins to break."},

    # New Elemental Lords dungeons
    {"name": "Blazing Crucible", "monsters": ["Ignis, Lord of Flames", "Phoenix Guardian"], "loot": ["Heart of Fire", "Blazing Crown", "Phoenix Feather"], "description": "A realm of perpetual fire where even the air itself burns with intense heat.", "min_level": 35, "area_type": "postgame"},
    {"name": "Frozen Eternity", "monsters": ["Glacies, Frost Sovereign", "Winter Wolf"], "loot": ["Core of Ice", "Frozen Crown", "Frost Crystal"], "description": "A magnificent ice palace where time stands still in an eternal winter.", "min_level": 35, "area_type": "postgame"},
    {"name": "Thunder Peaks", "monsters": ["Fulmen, Storm Emperor", "Lightning Elemental"], "loot": ["Lightning Heart", "Storm Crown", "Charged Crystal"], "description": "The highest mountain peaks where eternal storms rage and lightning never ceases.", "min_level": 35, "area_type": "postgame"},
    {"name": "Tectonic Depths", "monsters": ["Terra, Earth Colossus", "Stone Golem"], "loot": ["Earth Core", "Mountain Crown", "Ancient Fossil"], "description": "Deep underground caverns where the very earth shifts and breathes.", "min_level": 35, "area_type": "postgame"},
    {"name": "Abyssal Trench", "monsters": ["Aquarius, Tide Master", "Abyssal Leviathan"], "loot": ["Ocean Heart", "Coral Crown", "Leviathan Scale"], "description": "The deepest ocean trenches where pressure crushes all but the mightiest beings.", "min_level": 35, "area_type": "postgame"},
    
    # Four Horsemen challenge dungeons
    {"name": "Fields of Conquest", "monsters": ["Conquest, The White Rider", "Celestial Warrior"], "loot": ["White Bow", "Victor's Crown", "Celestial Armor"], "description": "A battlefield where victory is always just out of reach.", "min_level": 50, "area_type": "endgame"},
    {"name": "War's Domain", "monsters": ["War, The Red Rider", "Blood Knight"], "loot": ["Bloodthirsty Blade", "Warlord's Crown", "Blood-Stained Armor"], "description": "A realm where conflict never ends and peace is unknown.", "min_level": 52, "area_type": "endgame"},
    {"name": "Barren Wastelands", "monsters": ["Famine, The Black Rider", "Withered Guardian"], "loot": ["Scales of Balance", "Crown of Hunger", "Life Essence"], "description": "A desolate landscape where nothing grows and hunger is eternal.", "min_level": 54, "area_type": "endgame"},
    {"name": "Death's Dominion", "monsters": ["Death, The Pale Rider", "Reaper's Assistant"], "loot": ["Soul Scythe", "Pale Crown", "Final Judgment"], "description": "The final resting place for all mortal souls.", "min_level": 58, "area_type": "endgame"},
    
    # Special challenge dungeons
    {"name": "The Void Between Worlds", "monsters": ["Void Dragon", "Dimensional Horror"], "loot": ["Void Dragon Scale", "Void Crown", "Horror Essence"], "description": "A place that exists between realities, where the laws of physics break down.", "min_level": 45, "area_type": "dimensional"},
    {"name": "Chronos Sanctum", "monsters": ["Time Keeper", "Temporal Guardian"], "loot": ["Chronos Crystal", "Time Keeper's Staff", "Paradox Shard"], "description": "A sanctuary where past, present, and future converge into one.", "min_level": 42, "area_type": "dimensional"},
    {"name": "Astral Nexus", "monsters": ["Celestial Titan", "Astral Entity"], "loot": ["Celestial Heart", "Titan's Crown", "Star Fragment"], "description": "The convergence point of all celestial bodies and cosmic energies.", "min_level": 46, "area_type": "dimensional"}
]


# Note: All color constants are defined at the top of the file using colorama for cross-platform compatibility

def print_colored(text: str, color_code: str = "", end: str = "\n") -> None:
    print(f"{color_code}{text}{ENDC}" if color_code else text, end=end)

def print_animated(text: str, color_code: str = "", delay: Optional[float] = None) -> None:
    length = len(text)
    actual_delay = 0.01  # Default delay
    if delay is not None:
        actual_delay = delay
    else:
        actual_delay = max(0.005, min(0.03, 1.0 / (length * 10)))

    if color_code:
        sys.stdout.write(color_code)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(actual_delay)
    if color_code:
        sys.stdout.write(ENDC)
    sys.stdout.write("\n")
    sys.stdout.flush()

# Function to display headers with color
def print_header(title: str) -> None:
    print("\n" + "=" * 40)
    print(f"{BOLD}{MAGENTA}{title}{ENDC}")
    print("=" * 40)

# Show the help menu
def show_help() -> None:
    help_text = """
LEGACIES OF OUR LEGENDS - COMMANDS

PROGRESS
/start            - Starter guide
/areas             - Area guides
/dungeons          - Dungeon guides
/timetravel        - Time travel guide
/coolness          - Info about coolness
/story             - Show storyline progress

CRAFTING
/craft             - Recipes calculator
/dismantle         - Dismantling calculator
/invcalc           - Inventory calculator
/drops             - Monster drops
/enchants          - Enchantments info

ITEMS
/equip <item>      - Equip an item from inventory
/inspect <item>    - Inspect an item's special properties
/upgrade           - Upgrade weapons and armor to increase their stats
/enchant           - Apply enchantments to weapons and armor
/chest <tier>      - Open a treasure chest (Common, Uncommon, Rare, Epic, Legendary)
/use <potion>      - Use a potion from your inventory

PETS
/pet               - Pets guide

TRADING
/trading           - Trading guide

PROFESSIONS
/professions       - Professions guide
/prof_system       - Professions system

GUILD
/guild             - Guild guide

EVENTS
/events            - Event guides

MONSTERS
/mobs [area]       - Monsters in [area]
/dailymob          - Today's monster
/fight [monster]   - Fight a monster
/dungeon [name]    - Enter a dungeon
/dungeon_list      - List all dungeons
/bestiary          - List all monsters

GAMBLING
/gambling          - Gambling guide

DIMENSIONS
/dimensions        - Travel between dimensions
/dim               - Shortcut for dimensions travel
/find_key          - Search for dimension keys
/return_home       - Emergency return to Overworld

CAMP
/camp              - Manage your home camp
/camp_build        - Build or upgrade camp structures
/camp_repair       - Repair damaged structures
/camp_use          - Use a camp structure for benefits
/camp_demolish     - Remove existing structures
/camp_info         - View information about structures

WEATHER & SEASONS
/weather           - Show current weather conditions
/season            - Display current season information

MISC
/codes             - Redeemable codes
/duel              - Duel info
/farm              - Farming guide
/tip               - Random tip
/shop              - Visit the shop
/equip [item]      - Equip an item
/stats             - Show your stats
/support           - Support information
/save              - Save game
/load              - Load game
/quests            - View and accept quests
/new               - Create a new character
/inventory         - Show your inventory

SETTINGS
/settings          - Your settings
/setprogress       - Change progress
/prefix            - Show prefix
/exit              - Exit game
/gather            - Gather materials
/materials         - Show materials
/travel            - Travel to area
"""

    for line in help_text.strip().split("\n"):
        stripped = line.strip()
        if stripped.isupper() and len(stripped) > 0:
            print_colored(stripped, MAGENTA)
        elif stripped.startswith("/"):
            print_colored(stripped, CYAN)
        else:
            print(stripped)

# Function to handle commands
def show_location() -> None:
    print_header("Current Location")
    current = user_data["current_area"]
    print_animated(f"You are currently in: {current}")
    if current in LOCATIONS:
        print_animated(f"Description: {LOCATIONS[current]['description']}")

# Function to inspect items (especially legendary items)
def inspect_item(item_name: str) -> None:
    """Inspect an item to see its special properties and effects"""
    print_header("Item Inspection")

    if not item_name:
        print_colored("Please specify an item to inspect.", WARNING)
        return

    # Check if item is in inventory
    if item_name not in user_data["inventory"]:
        print_colored(f"You don't have '{item_name}' in your inventory.", FAIL)
        return

    # Check if item is a legendary item
    if item_name in LEGENDARY_ITEMS:
        item = LEGENDARY_ITEMS[item_name]
        print_colored("✧・゚: *✧・゚:* LEGENDARY ITEM *:・゚✧*:・゚✧", MAGENTA)
        print_colored(f"Name: {item_name}", CYAN)
        print(f"Type: {item['type'].capitalize()}")
        print(f"Effect: +{item['effect']} {item['type']} {'damage' if item['type'] == 'weapon' else 'defense'}")
        print_colored(f"Special Ability: {item['special_ability']}", OKGREEN)
        print(f"Description: {item['description']}")

        # Show special note based on item type
        if item['type'] == 'weapon':
            print_colored("\nThis legendary weapon can be equipped to drastically increase your attack.", YELLOW)
        elif item['type'] == 'armor':
            print_colored("\nThis legendary armor can be equipped to drastically increase your defense.", YELLOW)
        elif item['type'] == 'accessory':
            print_colored("\nThis legendary accessory grants special abilities when carried in your inventory.", YELLOW)

    # Check if item is a weapon
    elif item_name in WEAPONS:
        weapon = WEAPONS[item_name]
        print_colored("WEAPON", CYAN)
        print(f"Name: {item_name}")
        print(f"Damage: {weapon['damage']}")
        print(f"Speed: {weapon['speed']}")
        print(f"Price: {weapon['price']} gold")
        if 'effect' in weapon:
            print_colored(f"Special Effect: {weapon['effect']}", OKGREEN)

    # Otherwise it's a regular item
    else:
        print(f"Item: {item_name}")

        # Check for item types based on name patterns
        if "Potion" in item_name:
            print("Type: Consumable")
            if "Health" in item_name:
                print("Effect: Restores health when used")
            elif "Mana" in item_name:
                print("Effect: Restores mana when used")
        elif any(armor_type in item_name for armor_type in ["Armor", "Shield", "Helmet", "Boots"]):
            print("Type: Armor")
            print("Effect: Increases defense when equipped")
        else:
            print("Type: Miscellaneous item")
            print("This appears to be a regular item with no special properties.")

# Elemental System
ELEMENTS = {
    "Ignis": {
        "name": "Ignis",
        "description": "The element of fire, capable of burning and dealing damage over time.",
        "color": Fore.RED + Style.BRIGHT,  # LIGHTRED
        "weakness": ["Aqua", "Gē"],
        "strength": ["Glacies", "Aer", "Pneuma"],
        "damage_type": "elemental"
    },
    "Aqua": {
        "name": "Aqua",
        "description": "The element of water, versatile and adaptive, weakens fire.",
        "color": Fore.BLUE,  # Blue
        "weakness": ["Fulmen", "Glacies"],
        "strength": ["Ignis", "Venēnum"],
        "damage_type": "elemental"
    },
    "Gē": {
        "name": "Gē",
        "description": "The element of earth, sturdy and grounding, absorbs electricity.",
        "color": Fore.YELLOW,  # Yellow/Brown
        "weakness": ["Aer", "Ferrum"],
        "strength": ["Fulmen", "Ignis"],
        "damage_type": "elemental"
    },
    "Aer": {
        "name": "Aer",
        "description": "The element of air, swift and evasive, disperses poison.",
        "color": Fore.CYAN,  # Cyan
        "weakness": ["Ignis", "Ferrum"],
        "strength": ["Gē", "Venēnum"],
        "damage_type": "elemental"
    },
    "Fulmen": {
        "name": "Fulmen",
        "description": "The element of lightning, delivering swift, powerful strikes.",
        "color": Fore.MAGENTA,  # Magenta
        "weakness": ["Gē", "Ferrum"],
        "strength": ["Aqua", "Aer"],
        "damage_type": "elemental"
    },
    "Glacies": {
        "name": "Glacies",
        "description": "The element of ice, freezing and slowing opponents.",
        "color": Fore.CYAN + Style.BRIGHT,  # Light Cyan
        "weakness": ["Ignis", "Ferrum"],
        "strength": ["Aqua", "Aer"],
        "damage_type": "elemental"
    },
    "Lux": {
        "name": "Lux",
        "description": "The element of light, purifying and revealing the hidden.",
        "color": Fore.WHITE + Style.BRIGHT,  # White
        "weakness": ["Tenebrae"],
        "strength": ["Tenebrae", "Pneuma"],
        "damage_type": "elemental"
    },
    "Tenebrae": {
        "name": "Tenebrae",
        "description": "The element of darkness, corrupting and concealing.",
        "color": Fore.BLACK + Style.DIM,  # Dark Gray
        "weakness": ["Lux"],
        "strength": ["Lux", "Pneuma"],
        "damage_type": "elemental"
    },
    "Venēnum": {
        "name": "Venēnum",
        "description": "The element of poison, inflicting toxins and weakening foes.",
        "color": Fore.GREEN,  # Green
        "weakness": ["Aqua", "Aer"],
        "strength": ["Gē", "Ferrum"],
        "damage_type": "elemental"
    },
    "Ferrum": {
        "name": "Ferrum",
        "description": "The element of metal, resistant and conductive.",
        "color": Fore.WHITE,  # Light Gray
        "weakness": ["Venēnum", "Fulmen"],
        "strength": ["Glacies", "Aer", "Gē"],
        "damage_type": "elemental"
    },
    "Pneuma": {
        "name": "Pneuma",
        "description": "The element of spirit, affecting the soul and mind.",
        "color": Fore.MAGENTA,  # Purple
        "weakness": ["Lux", "Tenebrae"],
        "strength": ["Venēnum", "Glacies"],
        "damage_type": "elemental"
    },
    "Viridia": {
        "name": "Viridia",
        "description": "The element of plants and nature, with restorative and ensnaring abilities.",
        "color": Fore.GREEN + Style.BRIGHT,  # Bright Green
        "weakness": ["Ignis", "Venēnum"],
        "strength": ["Aqua", "Gē", "Aer"],
        "damage_type": "elemental"
    },
    "Nullum": {
        "name": "Nullum",
        "description": "Non-elemental physical damage that ignores elemental resistances.",
        "color": Style.RESET_ALL,  # Default/White
        "weakness": [],
        "strength": [],
        "damage_type": "physical"
    }
}

# Elemental Reactions
ELEMENTAL_REACTIONS = {
    # Original Reactions
    "Ignis+Aqua": {
        "name": "Fumus",
        "description": "Creates a steam cloud that reduces vision and increases evasion.",
        "effect": {"evasion": 15, "vision": -30, "duration": 5},
        "damage_multiplier": 1.2,
        "damage_type": "elemental"
    },
    "Ignis+Fulmen": {
        "name": "Tempestas",
        "description": "Creates a chain explosion with area effect burn and shock damage.",
        "effect": {"area_damage": True, "burn": 3, "shock": 2, "duration": 5},
        "damage_multiplier": 1.8,
        "damage_type": "elemental"
    },
    "Aqua+Glacies": {
        "name": "Congelatio",
        "description": "Freezes the enemy, immobilizing them for a short duration.",
        "effect": {"immobilize": 2, "duration": 5},
        "damage_multiplier": 1.3,
        "damage_type": "elemental"
    },
    "Aqua+Venēnum": {
        "name": "Dilutio",
        "description": "Creates a toxic mist that poisons all enemies in an area.",
        "effect": {"area_damage": True, "poison": 4, "duration": 5},
        "damage_multiplier": 1.5,
        "damage_type": "elemental"
    },
    "Gē+Ferrum": {
        "name": "Arma",
        "description": "Temporarily raises defense or spawns protective armor.",
        "effect": {"defense": 30, "duration": 3},
        "damage_multiplier": 1.0,
        "damage_type": "physical"
    },
    "Aer+Fulmen": {
        "name": "Tonitrus",
        "description": "Creates a thunderstorm that strikes multiple foes.",
        "effect": {"multi_target": True, "shock": 3, "duration": 5},
        "damage_multiplier": 1.6,
        "damage_type": "elemental"
    },
    "Lux+Tenebrae": {
        "name": "Umbra",
        "description": "Creates an eclipse effect causing area blindness or HP drain.",
        "effect": {"area_damage": True, "blind": 2, "drain": 5, "duration": 5},
        "damage_multiplier": 1.7,
        "damage_type": "elemental"
    },
    "Lux+Pneuma": {
        "name": "Divinum",
        "description": "Bestows a holy blessing that heals and cleanses allies.",
        "effect": {"heal": 40, "cleanse": True, "duration": 5},
        "damage_multiplier": 1.0,
        "damage_type": "elemental"
    },
    "Tenebrae+Venēnum": {
        "name": "Maleficium",
        "description": "Inflicts a curse causing damage over time and debuffs.",
        "effect": {"dot": 5, "attack": -15, "defense": -15, "duration": 5},
        "damage_multiplier": 1.4,
        "damage_type": "elemental"
    },
    "Ferrum+Fulmen": {
        "name": "Magnetismus",
        "description": "Creates a magnetic field that pulls enemies together.",
        "effect": {"pull": True, "range": 3, "duration": 5},
        "damage_multiplier": 1.2,
        "damage_type": "elemental"
    },
    "Glacies+Pneuma": {
        "name": "Frigus Animae",
        "description": "Freezes the soul, slowing enemies and lowering spirit regeneration.",
        "effect": {"slow": 30, "mana_regen": -50, "duration": 5},
        "damage_multiplier": 1.3,
        "damage_type": "elemental"
    },
    "Aer+Aqua": {
        "name": "Nebula",
        "description": "Creates a fog that increases dodge rate and conceals allies.",
        "effect": {"dodge": 25, "stealth": True, "duration": 5},
        "damage_multiplier": 1.0,
        "damage_type": "elemental"
    },
    "Gē+Venēnum": {
        "name": "Miasma",
        "description": "Creates a toxic zone on the ground that damages over time.",
        "effect": {"area_damage": True, "poison": 3, "movement": -20, "duration": 5},
        "damage_multiplier": 1.4,
        "damage_type": "elemental"
    },

    # New Reactions with Viridia
    "Viridia+Ignis": {
        "name": "Combustio",
        "description": "Plants burst into flames, creating widespread burning damage.",
        "effect": {"area_damage": True, "burn": 5, "duration": 5},
        "damage_multiplier": 1.5,
        "damage_type": "elemental"
    },
    "Viridia+Aqua": {
        "name": "Virescentia",
        "description": "Plants flourish with water, creating a healing zone and boosting attack.",
        "effect": {"healing_zone": True, "heal": 15, "attack": 15, "duration": 5},
        "damage_multiplier": 1.0,
        "damage_type": "elemental"
    },
    "Viridia+Venēnum": {
        "name": "Toxicum",
        "description": "Creates highly toxic plants that release deadly poison.",
        "effect": {"poison": 7, "area_damage": True, "duration": 5},
        "damage_multiplier": 1.7,
        "damage_type": "elemental"
    },
    "Viridia+Aer": {
        "name": "Pollinis",
        "description": "Spreads pollen that causes confusion and mild healing.",
        "effect": {"confusion": True, "heal": 10, "duration": 5},
        "damage_multiplier": 1.2,
        "damage_type": "elemental"
    },
    "Viridia+Gē": {
        "name": "Arbores",
        "description": "Creates massive roots that entangle foes and boost defense.",
        "effect": {"entangle": True, "defense": 20, "duration": 5},
        "damage_multiplier": 1.3,
        "damage_type": "elemental"
    },
    "Viridia+Lux": {
        "name": "Photosynthesis",
        "description": "Plants absorb light energy for massive healing and energy restoration.",
        "effect": {"heal": 30, "energy": 30, "duration": 5},
        "damage_multiplier": 1.0,
        "damage_type": "elemental"
    },

    # Nullum combinations
    "Nullum+Ignis": {
        "name": "Flamma Pura",
        "description": "Physical strike infused with fire, ignoring elemental resistances.",
        "effect": {"pierce_resistance": True, "burn": 2, "duration": 5},
        "damage_multiplier": 1.6,
        "damage_type": "physical"
    },
    "Nullum+Aqua": {
        "name": "Fluctus",
        "description": "Physical force with water pressure, pushing enemies back.",
        "effect": {"knockback": True, "slow": 15, "duration": 5},
        "damage_multiplier": 1.4,
        "damage_type": "physical"
    },
    "Nullum+Fulmen": {
        "name": "Percussum",
        "description": "Electrified physical strike that stuns enemies.",
        "effect": {"stun": 2, "duration": 5},
        "damage_multiplier": 1.5,
        "damage_type": "physical"
    },
    "Nullum+Ferrum": {
        "name": "Acies",
        "description": "Perfect physical strike that increases critical chance.",
        "effect": {"critical_chance": 20, "duration": 5},
        "damage_multiplier": 1.8,
        "damage_type": "physical"
    }
}

# Legendary items with special effects
LEGENDARY_ITEMS = {
    "Crown of New Dawn": {
        "type": "armor",
        "effect": 30,
        "special_ability": "Grants 10% chance to resurrect upon death",
        "description": "A legendary crown forged from otherworldly materials, rumored to be blessed by the gods themselves."
    },
    "Dimensional Compass": {
        "type": "accessory",
        "effect": 0,
        "special_ability": "Allows travel to dimensional rifts",
        "description": "A mysterious compass that points to places between worlds."
    },
    "Godforged Artifact": {
        "type": "weapon",
        "effect": 50,
        "special_ability": "Weapon damage scales with your character level",
        "description": "A weapon of divine origin, growing in power as its wielder does."
    },
    "Celestial Aegis": {
        "type": "armor",
        "effect": 40,
        "special_ability": "Reduces all damage by 20%",
        "description": "A shield forged from the scales of a celestial dragon."
    },
    "Timekeeper's Pendant": {
        "type": "accessory",
        "effect": 0,
        "special_ability": "30% chance to perform a double attack",
        "description": "A pendant containing grains of timesand, allowing its wearer to occasionally bend time."
    },
    "Phoenix Plume": {
        "type": "accessory",
        "effect": 0,
        "special_ability": "Auto-resurrect once per dungeon",
        "description": "A feather from the legendary phoenix, pulsing with the essence of rebirth."
    },
    "Worldbreaker": {
        "type": "weapon",
        "effect": 60,
        "special_ability": "10% chance to instantly defeat non-boss enemies",
        "description": "A massive hammer said to have been used to shape the very mountains."
    },
    "Voidwalker Boots": {
        "type": "armor",
        "effect": 20,
        "special_ability": "50% chance to dodge any attack",
        "description": "Boots that phase in and out of reality, making the wearer difficult to hit."
    }
}

# Post-game activity functions
def dimensional_rifts() -> None:
    """Function to handle dimensional rift exploration"""
    print_header("DIMENSIONAL RIFTS")

    if "Dimensional Compass" not in user_data["inventory"]:
        print_colored("You need the 'Dimensional Compass' to navigate the rifts!", WARNING)
        print_colored("Complete the 'Dimensional Rifts' storyline to obtain it.", YELLOW)
        return

    rifts = [
        "Mirror Dimension", 
        "Time Fracture", 
        "Shadow Realm", 
        "Elemental Plane", 
        "Dream World"
    ]

    print_colored("Available rifts:", CYAN)
    for idx, rift in enumerate(rifts, 1):
        print(f"{idx}. {rift}")

    choice = input("\nSelect a rift to explore (1-5) or 'back' to return: ")

    if choice.lower() == "back":
        return
    elif choice.isdigit() and 1 <= int(choice) <= len(rifts):
        selected_rift = rifts[int(choice)-1]
        print_colored(f"Entering the {selected_rift}...", CYAN)
        print_colored("This feature will be expanded in future updates.", YELLOW)

        # Give player a small reward for trying this feature
        reward_gold = random.randint(100, 500)
        user_data["gold"] += reward_gold
        print_colored(f"You found {reward_gold} gold in the rift!", OKGREEN)
    else:
        print_colored("Invalid choice.", FAIL)

# Function to handle dimensions system
def dimensions_menu() -> None:
    """Function to handle dimension traveling and discovery"""
    print_header("DIMENSIONAL TRAVEL")
    
    print_colored("Current Dimension: ", CYAN, end="")
    print_colored(user_data["current_dimension"], MAGENTA)
    print()
    
    print_colored("Discovered Dimensions:", CYAN)
    for dim_name in user_data["dimensions_discovered"]:
        if dim_name == user_data["current_dimension"]:
            print_colored(f"  > {dim_name} (Current)", OKGREEN)
        else:
            print_colored(f"  - {dim_name}", LIGHTGRAY)
    print()
    
    # Check for portal frame
    has_portal = "Portal Frame" in [s for s in user_data["home_structures"] if user_data["home_structures"].get(s, {}).get("built", False)]
    
    if not has_portal:
        print_colored("You need to build a Portal Frame in your camp to travel between dimensions.", WARNING)
        print_colored("Use /camp_build to construct a Portal Frame.", LIGHTGRAY)
        return
    
    # Show available dimensions based on discovered keys and level
    print_colored("Available Dimensions for Travel:", CYAN)
    available_dimensions = []
    
    for dim_name, dim_info in DIMENSIONS.items():
        if dim_name in user_data["dimensions_discovered"]:
            available_dimensions.append(dim_name)
            print_colored(f"  [{len(available_dimensions)}] {dim_name}", OKGREEN)
        elif "unlock_item" in dim_info and dim_info["unlock_item"] in user_data["dimension_keys"]:
            if user_data["level"] >= dim_info["access_level"]:
                available_dimensions.append(dim_name)
                print_colored(f"  [{len(available_dimensions)}] {dim_name}", YELLOW)
            else:
                print_colored(f"  [?] {dim_name} (Requires Level {dim_info['access_level']})", WARNING)
        elif user_data["level"] >= dim_info["access_level"]:
            print_colored(f"  [?] {dim_name} (Requires {dim_info.get('unlock_item', 'Unknown Key')})", WARNING)
    
    print_colored("  [0] Cancel", LIGHTGRAY)
    print()
    
    # Get player choice
    choice = input("Select a dimension to travel to (number): ")
    
    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            print_colored("Dimensional travel canceled.", LIGHTGRAY)
            return
            
        if 1 <= choice_idx <= len(available_dimensions):
            selected_dimension = available_dimensions[choice_idx - 1]
            
            if selected_dimension == user_data["current_dimension"]:
                print_colored("You are already in this dimension.", YELLOW)
                return
                
            # Travel to the dimension
            user_data["current_dimension"] = selected_dimension
            
            # Add to discovered if not already there
            if selected_dimension not in user_data["dimensions_discovered"]:
                user_data["dimensions_discovered"].append(selected_dimension)
                print_colored(f"You have discovered the {selected_dimension}!", OKGREEN)
                
            print_colored(f"Traveling to the {selected_dimension}...", CYAN)
            time.sleep(1)
            print_colored(f"You have arrived in the {selected_dimension}!", OKGREEN)
            
            # Describe the dimension
            if selected_dimension in DIMENSIONS:
                print_colored(DIMENSIONS[selected_dimension]["description"], LIGHTCYAN)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def find_dimension_key() -> None:
    """Find a key to unlock a new dimension"""
    current_dim = user_data["current_dimension"]
    player_level = user_data["level"]
    
    # Find potential dimensions that could have keys
    potential_keys = []
    for dim_name, dim_info in DIMENSIONS.items():
        if dim_name not in user_data["dimensions_discovered"] and "unlock_item" in dim_info:
            if dim_info["unlock_item"] not in user_data["dimension_keys"] and player_level >= dim_info["access_level"]:
                potential_keys.append((dim_name, dim_info["unlock_item"]))
    
    if not potential_keys:
        print_colored("You have found all available dimension keys for your current level.", YELLOW)
        return
        
    # Random chance to find a key based on current dimension and player level
    find_chance = min(0.05 * player_level, 0.5)  # 5% per level, max 50%
    
    # Exploring other dimensions increases chance
    if current_dim != "Overworld":
        find_chance += 0.2
        
    if random.random() < find_chance:
        # Found a key
        dim_name, key_name = random.choice(potential_keys)
        user_data["dimension_keys"].append(key_name)
        print_colored(f"You found the {key_name}!", OKGREEN)
        print_colored(f"This key will allow you to access the {dim_name} dimension.", CYAN)
        print_colored("Use /dimensions to travel to new dimensions.", LIGHTGRAY)
    else:
        print_colored("You search for dimensional anomalies but find nothing of interest.", LIGHTGRAY)

def returnToOverworld() -> None:
    """Emergency function to return to the Overworld dimension if stuck"""
    if user_data["current_dimension"] == "Overworld":
        print_colored("You are already in the Overworld.", YELLOW)
        return
        
    # Return to Overworld
    prev_dimension = user_data["current_dimension"]
    user_data["current_dimension"] = "Overworld"
    print_colored(f"You've escaped from the {prev_dimension} and returned to the Overworld!", OKGREEN)
    print_colored("You find yourself back in familiar territory.", CYAN)

# Function to handle home/camp system
def camp_menu() -> None:
    """Function to handle camp management"""
    print_header("CAMP MANAGEMENT")
    
    print_colored(f"Current Location: {user_data['home_location']}", CYAN)
    
    # Show existing structures
    print_colored("\nCurrent Structures:", CYAN)
    if not any(user_data["home_structures"].get(s, {}).get("built", False) for s in user_data["home_structures"]):
        print_colored("  No structures built yet.", LIGHTGRAY)
    else:
        for struct_name, struct_data in user_data["home_structures"].items():
            if struct_data.get("built", False):
                health_percent = struct_data.get("health", 100)
                health_color = OKGREEN if health_percent > 70 else (YELLOW if health_percent > 30 else FAIL)
                print_colored(f"  - {struct_name} ", LIGHTGRAY, end="")
                print_colored(f"[Health: {health_percent}%]", health_color)
    
    print_colored("\nOptions:", CYAN)
    print_colored("  [1] Build/Upgrade Structure", LIGHTGRAY)
    print_colored("  [2] Repair Structure", LIGHTGRAY)
    print_colored("  [3] Use Structure", LIGHTGRAY)
    print_colored("  [4] Demolish Structure", LIGHTGRAY)
    print_colored("  [5] View Structure Info", LIGHTGRAY)
    print_colored("  [0] Exit", LIGHTGRAY)
    
    choice = input("\nSelect an option: ")
    
    if choice == "1":
        build_structure()
    elif choice == "2":
        repair_structure()
    elif choice == "3":
        use_structure()
    elif choice == "4":
        demolish_structure()
    elif choice == "5":
        view_structure_info()
    elif choice == "0":
        return
    else:
        print_colored("Invalid choice.", FAIL)

def build_structure() -> None:
    """Build or upgrade a camp structure"""
    print_header("BUILD/UPGRADE STRUCTURE")
    
    # Group structures by category
    structures_by_category = {}
    for struct_name, struct_data in HOME_STRUCTURES.items():
        category = struct_data.get("category", "misc")
        if category not in structures_by_category:
            structures_by_category[category] = []
        structures_by_category[category].append((struct_name, struct_data))
    
    # Filter available structures based on player level and dependencies
    available_structures = []
    for category, structures in structures_by_category.items():
        print_colored(f"\n{category.capitalize()}:", CYAN)
        for struct_name, struct_data in structures:
            # Check if already built
            already_built = user_data["home_structures"].get(struct_name, {}).get("built", False)
            
            # Check for upgrades
            upgrade_from = struct_data.get("upgrade_from")
            if upgrade_from and not user_data["home_structures"].get(upgrade_from, {}).get("built", False):
                print_colored(f"  [?] {struct_name} (Requires {upgrade_from})", WARNING)
                continue
                
            # Check for dependencies
            requires = struct_data.get("requires")
            if requires and not user_data["home_structures"].get(requires, {}).get("built", False):
                print_colored(f"  [?] {struct_name} (Requires {requires})", WARNING)
                continue
                
            # Check level requirement (implicit in structure level)
            if struct_data.get("level", 1) * 5 > user_data["level"]:
                print_colored(f"  [?] {struct_name} (Requires Level {struct_data.get('level', 1) * 5})", WARNING)
                continue
                
            if already_built:
                if not upgrade_from:  # Can't upgrade a structure that isn't an upgrade
                    print_colored(f"  [B] {struct_name} (Already Built)", OKGREEN)
                    continue
                else:
                    print_colored(f"  [U] {struct_name} (Upgrade from {upgrade_from})", YELLOW)
            else:
                print_colored(f"  [{len(available_structures) + 1}] {struct_name}", LIGHTGRAY)
                
            # Show required materials
            for material, amount in struct_data.get("materials", {}).items():
                material_owned = user_data.get("materials", {}).get(material, 0)
                color = OKGREEN if material_owned >= amount else FAIL
                print_colored(f"      {material}: {material_owned}/{amount}", color)
                
            available_structures.append(struct_name)
    
    if not available_structures:
        print_colored("\nNo structures available to build at your current level.", WARNING)
        return
        
    print_colored("\n  [0] Cancel", LIGHTGRAY)
    
    choice = input("\nSelect a structure to build (number): ")
    
    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            return
            
        if 1 <= choice_idx <= len(available_structures):
            selected_structure = available_structures[choice_idx - 1]
            struct_data = HOME_STRUCTURES[selected_structure]
            
            # Check if we have the materials
            materials = struct_data.get("materials", {})
            can_build = True
            
            for material, amount in materials.items():
                if user_data.get("materials", {}).get(material, 0) < amount:
                    can_build = False
                    print_colored(f"Not enough {material}. Need {amount}.", FAIL)
            
            if can_build:
                # Deduct materials
                for material, amount in materials.items():
                    user_data["materials"][material] = user_data["materials"].get(material, 0) - amount
                
                # Add structure to home
                if selected_structure not in user_data["home_structures"]:
                    user_data["home_structures"][selected_structure] = {}
                    
                user_data["home_structures"][selected_structure]["built"] = True
                user_data["home_structures"][selected_structure]["health"] = 100
                user_data["home_structures"][selected_structure]["position"] = [0, 0]  # Simple position
                
                print_colored(f"Successfully built {selected_structure}!", OKGREEN)
                
                # Check if this is an upgrade
                upgrade_from = struct_data.get("upgrade_from")
                if upgrade_from:
                    # Remove the previous structure
                    if upgrade_from in user_data["home_structures"]:
                        user_data["home_structures"][upgrade_from]["built"] = False
                    print_colored(f"Upgraded from {upgrade_from} to {selected_structure}!", OKGREEN)
            else:
                print_colored("You don't have enough resources to build this structure.", FAIL)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def repair_structure() -> None:
    """Repair a damaged camp structure"""
    print_header("REPAIR STRUCTURE")
    
    # Show existing structures with health
    structures_to_repair = []
    print_colored("Structures that need repair:", CYAN)
    
    for struct_name, struct_data in user_data["home_structures"].items():
        if struct_data.get("built", False) and struct_data.get("health", 100) < 100:
            structures_to_repair.append(struct_name)
            health = struct_data.get("health", 100)
            health_color = YELLOW if health > 50 else FAIL
            print_colored(f"  [{len(structures_to_repair)}] {struct_name} ", LIGHTGRAY, end="")
            print_colored(f"[Health: {health}%]", health_color)
    
    if not structures_to_repair:
        print_colored("  No structures need repair.", LIGHTGRAY)
        return
        
    print_colored("  [0] Cancel", LIGHTGRAY)
    
    choice = input("\nSelect a structure to repair (number): ")
    
    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            return
            
        if 1 <= choice_idx <= len(structures_to_repair):
            selected_structure = structures_to_repair[choice_idx - 1]
            current_health = user_data["home_structures"][selected_structure].get("health", 100)
            
            # Calculate repair materials (25% of original for a full repair)
            original_materials = HOME_STRUCTURES[selected_structure].get("materials", {})
            repair_materials = {}
            repair_percentage = (100 - current_health) / 100
            
            for material, amount in original_materials.items():
                repair_amount = math.ceil(amount * 0.25 * repair_percentage)
                repair_materials[material] = repair_amount
            
            # Show repair cost
            print_colored(f"\nRepairing {selected_structure} will cost:", CYAN)
            can_repair = True
            
            for material, amount in repair_materials.items():
                if amount > 0:
                    material_owned = user_data.get("materials", {}).get(material, 0)
                    color = OKGREEN if material_owned >= amount else FAIL
                    print_colored(f"  {material}: {material_owned}/{amount}", color)
                    if material_owned < amount:
                        can_repair = False
            
            if can_repair:
                confirm = input("\nProceed with repair? (y/n): ").lower()
                if confirm == 'y':
                    # Deduct materials
                    for material, amount in repair_materials.items():
                        if amount > 0:
                            user_data["materials"][material] = user_data["materials"].get(material, 0) - amount
                    
                    # Repair structure
                    user_data["home_structures"][selected_structure]["health"] = 100
                    print_colored(f"Successfully repaired {selected_structure}!", OKGREEN)
            else:
                print_colored("You don't have enough resources for the repair.", FAIL)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def use_structure() -> None:
    """Use a camp structure and receive its benefits"""
    print_header("USE STRUCTURE")
    
    # Show existing usable structures
    usable_structures = []
    print_colored("Usable structures:", CYAN)
    
    for struct_name, struct_data in user_data["home_structures"].items():
        if struct_data.get("built", False) and struct_data.get("health", 0) > 0:
            # Structure must be built and have health
            struct_info = HOME_STRUCTURES.get(struct_name, {})
            if struct_info.get("effects"):
                usable_structures.append(struct_name)
                print_colored(f"  [{len(usable_structures)}] {struct_name}", LIGHTGRAY)
    
    if not usable_structures:
        print_colored("  No usable structures available.", LIGHTGRAY)
        return
        
    print_colored("  [0] Cancel", LIGHTGRAY)
    
    choice = input("\nSelect a structure to use (number): ")
    
    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            return
            
        if 1 <= choice_idx <= len(usable_structures):
            selected_structure = usable_structures[choice_idx - 1]
            struct_info = HOME_STRUCTURES.get(selected_structure, {})
            effects = struct_info.get("effects", {})
            
            # Apply effects based on structure type
            print_colored(f"Using {selected_structure}...", CYAN)
            
            # Health regeneration
            if "rest_heal" in effects:
                heal_amount = effects["rest_heal"]
                old_health = user_data["health"]
                user_data["health"] = min(user_data["max_health"], user_data["health"] + heal_amount)
                actual_heal = user_data["health"] - old_health
                print_colored(f"You rest and recover {actual_heal} health points!", OKGREEN)
            
            # Mana regeneration
            if "mana_regen" in effects:
                if "mana" in user_data and "max_mana" in user_data:
                    mana_regen = effects["mana_regen"]
                    old_mana = user_data["mana"]
                    user_data["mana"] = min(user_data["max_mana"], user_data["mana"] + int(user_data["max_mana"] * mana_regen))
                    actual_regen = user_data["mana"] - old_mana
                    print_colored(f"You meditate and recover {actual_regen} mana points!", OKGREEN)
            
            # Herb production
            if "herb_production" in effects:
                herb_amount = effects["herb_production"]
                herb_types = ["Red Herb", "Blue Herb", "Green Herb"]
                
                for _ in range(herb_amount):
                    herb = random.choice(herb_types)
                    user_data["materials"][herb] = user_data["materials"].get(herb, 0) + 1
                    print_colored(f"You harvested 1 {herb}!", OKGREEN)
            
            # Cooking food
            if "cook_food" in effects:
                if "food_quality" in effects:
                    quality_bonus = effects["food_quality"]
                    print_colored(f"Your food is {int(quality_bonus * 100)}% more effective when cooked here!", OKGREEN)
                
                # Simplified cooking system
                if "Raw Meat" in user_data.get("materials", {}):
                    meat_amount = min(3, user_data["materials"]["Raw Meat"])
                    if meat_amount > 0:
                        user_data["materials"]["Raw Meat"] -= meat_amount
                        user_data["materials"]["Cooked Meat"] = user_data["materials"].get("Cooked Meat", 0) + meat_amount
                        print_colored(f"You cooked {meat_amount} Raw Meat into Cooked Meat!", OKGREEN)
                else:
                    print_colored("You don't have any Raw Meat to cook.", YELLOW)
            
            # Combat experience bonus
            if "combat_exp_bonus" in effects:
                print_colored(f"Training here will give you {int(effects['combat_exp_bonus'] * 100)}% more combat experience!", OKGREEN)
                # Award small amount of XP
                exp_gain = int(10 * (1 + effects['combat_exp_bonus']))
                user_data["exp"] += exp_gain
                print_colored(f"You trained and gained {exp_gain} experience!", OKGREEN)
                check_level_up()
            
            # Crafting bonus
            if "crafting_bonus" in effects or "smithing_bonus" in effects or "alchemy_bonus" in effects:
                bonus_type = "crafting"
                bonus_value = effects.get("crafting_bonus", 0)
                
                if "smithing_bonus" in effects:
                    bonus_type = "smithing"
                    bonus_value = effects["smithing_bonus"]
                elif "alchemy_bonus" in effects:
                    bonus_type = "alchemy"
                    bonus_value = effects["alchemy_bonus"]
                
                print_colored(f"Using this {bonus_type} station gives you a {int(bonus_value * 100)}% bonus to {bonus_type}!", OKGREEN)
            
            # Dimension travel
            if "dimension_travel" in effects:
                print_colored("This portal allows dimensional travel!", CYAN)
                print_colored("Use /dimensions to travel between dimensions.", LIGHTGRAY)
            
            # Slightly damage structure from use
            current_health = user_data["home_structures"][selected_structure].get("health", 100)
            damage = random.randint(1, 5)  # Random damage between 1-5%
            user_data["home_structures"][selected_structure]["health"] = max(0, current_health - damage)
            
            if user_data["home_structures"][selected_structure]["health"] < 30:
                print_colored(f"Warning: {selected_structure} is in need of repair!", WARNING)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def demolish_structure() -> None:
    """Demolish a camp structure and recover some materials"""
    print_header("DEMOLISH STRUCTURE")
    
    # Show existing structures that can be demolished
    demolishable_structures = []
    print_colored("Structures that can be demolished:", CYAN)
    
    for struct_name, struct_data in user_data["home_structures"].items():
        if struct_data.get("built", False):
            # Check if any other structures depend on this one
            has_dependents = False
            for dep_name, dep_data in HOME_STRUCTURES.items():
                if dep_data.get("requires") == struct_name or dep_data.get("upgrade_from") == struct_name:
                    if dep_name in user_data["home_structures"] and user_data["home_structures"][dep_name].get("built", False):
                        has_dependents = True
                        break
            
            if has_dependents:
                print_colored(f"  [X] {struct_name} (Required by other structures)", WARNING)
            elif struct_name == "Tent" and len([s for s in user_data["home_structures"] if user_data["home_structures"].get(s, {}).get("built", False)]) == 1:
                print_colored(f"  [X] {struct_name} (Cannot demolish your only shelter)", WARNING)
            else:
                demolishable_structures.append(struct_name)
                print_colored(f"  [{len(demolishable_structures)}] {struct_name}", LIGHTGRAY)
    
    if not demolishable_structures:
        print_colored("  No structures can be demolished at this time.", LIGHTGRAY)
        return
        
    print_colored("  [0] Cancel", LIGHTGRAY)
    
    choice = input("\nSelect a structure to demolish (number): ")
    
    try:
        choice_idx = int(choice)
        if choice_idx == 0:
            return
            
        if 1 <= choice_idx <= len(demolishable_structures):
            selected_structure = demolishable_structures[choice_idx - 1]
            
            # Confirm demolition
            confirm = input(f"Are you sure you want to demolish {selected_structure}? (y/n): ").lower()
            if confirm != 'y':
                print_colored("Demolition canceled.", LIGHTGRAY)
                return
            
            # Return some materials (50% of original)
            original_materials = HOME_STRUCTURES[selected_structure].get("materials", {})
            print_colored("Recovered materials:", CYAN)
            
            for material, amount in original_materials.items():
                recovered = math.ceil(amount * 0.5)
                user_data["materials"][material] = user_data["materials"].get(material, 0) + recovered
                print_colored(f"  {material}: +{recovered}", OKGREEN)
            
            # Remove structure
            user_data["home_structures"][selected_structure]["built"] = False
            print_colored(f"Successfully demolished {selected_structure}!", OKGREEN)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def view_structure_info() -> None:
    """View detailed information about camp structures"""
    print_header("STRUCTURE INFORMATION")
    
    # Group structures by category
    structures_by_category = {}
    for struct_name, struct_data in HOME_STRUCTURES.items():
        category = struct_data.get("category", "misc")
        if category not in structures_by_category:
            structures_by_category[category] = []
        structures_by_category[category].append((struct_name, struct_data))
    
    # Display categories
    categories = list(structures_by_category.keys())
    print_colored("Structure Categories:", CYAN)
    
    for idx, category in enumerate(categories, 1):
        print_colored(f"  [{idx}] {category.capitalize()}", LIGHTGRAY)
    
    print_colored("  [0] Cancel", LIGHTGRAY)
    
    cat_choice = input("\nSelect a category (number): ")
    
    try:
        cat_idx = int(cat_choice)
        if cat_idx == 0:
            return
            
        if 1 <= cat_idx <= len(categories):
            selected_category = categories[cat_idx - 1]
            structures = structures_by_category[selected_category]
            
            print_colored(f"\n{selected_category.capitalize()} Structures:", CYAN)
            
            for idx, (struct_name, struct_data) in enumerate(structures, 1):
                print_colored(f"  [{idx}] {struct_name}", LIGHTGRAY)
            
            print_colored("  [0] Back", LIGHTGRAY)
            
            struct_choice = input("\nSelect a structure (number): ")
            
            try:
                struct_idx = int(struct_choice)
                if struct_idx == 0:
                    view_structure_info()  # Go back to category selection
                    return
                    
                if 1 <= struct_idx <= len(structures):
                    selected_structure, struct_data = structures[struct_idx - 1]
                    
                    # Display detailed information
                    print_header(selected_structure)
                    print_colored(f"Description: {struct_data.get('description', 'No description available.')}", LIGHTCYAN)
                    print_colored(f"Level: {struct_data.get('level', 1)}", LIGHTGRAY)
                    
                    if "upgrade_from" in struct_data:
                        print_colored(f"Upgrade from: {struct_data['upgrade_from']}", YELLOW)
                    
                    if "requires" in struct_data:
                        print_colored(f"Requires: {struct_data['requires']}", YELLOW)
                    
                    print_colored("\nMaterials:", CYAN)
                    for material, amount in struct_data.get("materials", {}).items():
                        print_colored(f"  {material}: {amount}", LIGHTGRAY)
                    
                    print_colored("\nEffects:", CYAN)
                    for effect, value in struct_data.get("effects", {}).items():
                        effect_name = effect.replace("_", " ").capitalize()
                        if isinstance(value, bool):
                            print_colored(f"  {effect_name}: {'Yes' if value else 'No'}", OKGREEN if value else FAIL)
                        elif isinstance(value, (int, float)):
                            if effect == "rest_heal":
                                print_colored(f"  {effect_name}: +{value} HP", OKGREEN)
                            elif effect == "storage":
                                print_colored(f"  {effect_name}: +{value} slots", OKGREEN)
                            elif effect in ("crafting_bonus", "smithing_bonus", "alchemy_bonus", "combat_exp_bonus", "mana_regen"):
                                print_colored(f"  {effect_name}: +{int(value * 100)}%", OKGREEN)
                            else:
                                print_colored(f"  {effect_name}: {value}", OKGREEN)
                    
                    # Check if player has this structure
                    built = selected_structure in user_data["home_structures"] and user_data["home_structures"][selected_structure].get("built", False)
                    
                    if built:
                        health = user_data["home_structures"][selected_structure].get("health", 100)
                        health_color = OKGREEN if health > 70 else (YELLOW if health > 30 else FAIL)
                        print_colored("\nStatus: Built", OKGREEN)
                        print_colored(f"Health: {health}%", health_color)
                    else:
                        print_colored("\nStatus: Not Built", LIGHTGRAY)
                    
                    input("\nPress Enter to return to categories...")
                    view_structure_info()  # Return to category selection
                else:
                    print_colored("Invalid choice.", FAIL)
                    time.sleep(1)
                    view_structure_info()  # Try again
            except ValueError:
                print_colored("Please enter a valid number.", FAIL)
                time.sleep(1)
                view_structure_info()  # Try again
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)

def divine_trials() -> None:
    """Function to handle divine trials"""
    print_header("DIVINE TRIALS")

    trials = [
        "Trial of Strength", 
        "Trial of Wisdom", 
        "Trial of Courage", 
        "Trial of Endurance", 
        "Trial of Balance"
    ]

    print_colored("The gods have set forth these trials:", CYAN)
    for idx, trial in enumerate(trials, 1):
        completed = f"{OKGREEN}✓{ENDC}" if f"{trial}" in user_data.get("completed_trials", []) else f"{YELLOW}◯{ENDC}"
        print(f"{idx}. {completed} {trial}")

    choice = input("\nSelect a trial to attempt (1-5) or 'back' to return: ")

    if choice.lower() == "back":
        return
    elif choice.isdigit() and 1 <= int(choice) <= len(trials):
        selected_trial = trials[int(choice)-1]
        print_colored(f"Preparing for the {selected_trial}...", CYAN)
        print_colored("This feature will be expanded in future updates.", YELLOW)

        # Mark trial as completed for testing purposes
        user_data.setdefault("completed_trials", []).append(selected_trial)

        # Give player a small reward
        if len(user_data.get("completed_trials", [])) >= 5:
            if "Godforged Artifact" not in user_data["inventory"]:
                user_data["inventory"].append("Godforged Artifact")
                print_colored("You have completed all divine trials!", OKGREEN)
                print_colored("The gods bestow upon you the GODFORGED ARTIFACT!", MAGENTA)
    else:
        print_colored("Invalid choice.", FAIL)

def legendary_hunts() -> None:
    """Function to handle legendary monster hunts"""
    print_header("LEGENDARY HUNTS")

    legendary_monsters = [
        {"name": "Ancient Dragon", "level": 35, "health": 500, "attack": 50, "drops": ["Dragon's Heart", "Dragon Scale"]},
        {"name": "Behemoth", "level": 40, "health": 700, "attack": 60, "drops": ["Behemoth Horn", "Massive Hide"]},
        {"name": "Kraken", "level": 45, "health": 800, "attack": 70, "drops": ["Kraken Ink", "Giant Tentacle"]},
        {"name": "Phoenix", "level": 50, "health": 600, "attack": 80, "drops": ["Phoenix Plume", "Eternal Flame"]},
        {"name": "World Serpent", "level": 55, "health": 1000, "attack": 90, "drops": ["Serpent Fang", "World Scale"]}
    ]

    print_colored("These legendary beasts await worthy challengers:", CYAN)
    for idx, monster in enumerate(legendary_monsters, 1):
        hunted = f"{OKGREEN}✓{ENDC}" if monster["name"] in user_data.get("legendary_hunts_completed", []) else f"{YELLOW}◯{ENDC}"
        print(f"{idx}. {hunted} {monster['name']} (Level {monster['level']})")

    choice = input("\nSelect a monster to hunt (1-5) or 'back' to return: ")

    if choice.lower() == "back":
        return
    elif choice.isdigit() and 1 <= int(choice) <= len(legendary_monsters):
        selected_monster = legendary_monsters[int(choice)-1]

        if user_data["level"] < selected_monster["level"]:
            print_colored("You are not strong enough to face this monster yet!", WARNING)
            print_colored(f"Required level: {selected_monster['level']}", YELLOW)
            return

        print_colored(f"Hunting the {selected_monster['name']}...", CYAN)

        # Simulate fight with the monster
        fight(selected_monster)

        # If player survived and monster was defeated
        if user_data["health"] > 0:
            user_data.setdefault("legendary_hunts_completed", []).append(selected_monster["name"])
    else:
        print_colored("Invalid choice.", FAIL)

def time_trials() -> None:
    """Function to handle dungeon time trials"""
    print_header("TIME TRIALS")

    # Get completed dungeons
    completed_dungeons = user_data.get("dungeons_completed", [])
    if len(completed_dungeons) < 3:
        print_colored("You need to complete at least 3 dungeons to access Time Trials!", WARNING)
        return

    print_colored("Select a dungeon to challenge in Time Trial mode:", CYAN)
    for idx, dungeon_name in enumerate(completed_dungeons, 1):
        trial_record = user_data.get("time_trial_records", {}).get(dungeon_name, "No record")
        print(f"{idx}. {dungeon_name} - Best time: {trial_record}")

    choice = input("\nSelect a dungeon (1-{}) or 'back' to return: ".format(len(completed_dungeons)))

    if choice.lower() == "back":
        return
    elif choice.isdigit() and 1 <= int(choice) <= len(completed_dungeons):
        selected_dungeon = completed_dungeons[int(choice)-1]
        print_colored(f"Preparing Time Trial for {selected_dungeon}...", CYAN)
        print_colored("This feature will be expanded in future updates.", YELLOW)

        # Simulate a trial record
        completion_time = random.randint(60, 300)  # Random time between 1-5 minutes
        minutes = completion_time // 60
        seconds = completion_time % 60
        time_str = f"{minutes}m {seconds}s"

        user_data.setdefault("time_trial_records", {})[selected_dungeon] = time_str
        print_colored(f"Trial completed in {time_str}!", OKGREEN)

        if "Timekeeper's Pendant" not in user_data["inventory"] and len(user_data.get("time_trial_records", {})) >= 5:
            user_data["inventory"].append("Timekeeper's Pendant")
            print_colored("You've mastered the flow of time!", OKGREEN)
            print_colored("You've earned the TIMEKEEPER'S PENDANT!", MAGENTA)
    else:
        print_colored("Invalid choice.", FAIL)

def new_game_plus() -> None:
    """Function to handle New Game+ mode"""
    print_header("NEW GAME+")

    if user_data["level"] < 50:
        print_colored("You need to reach level 50 to start New Game+!", WARNING)
        return

    print_colored("WARNING: Starting New Game+ will reset your story progress", FAIL)
    print_colored("but you'll keep your level, skills, and equipment.", YELLOW)

    confirm = input("\nAre you sure you want to start New Game+? (yes/no): ")

    if confirm.lower() == "yes":
        # Reset story progress but keep character stats
        user_data["active_quests"] = []
        user_data["completed_quests"] = []
        user_data["current_area"] = "Greenwood Village"
        user_data["dungeons_completed"] = []

        # Add bonus
        user_data["health"] += 50
        user_data["max_health"] += 50
        user_data["attack"] += 10
        user_data["defense"] += 10

        print_colored("You have started New Game+!", OKGREEN)
        print_colored("The world has reset, but you retain your power!", CYAN)
        print_colored("You've gained permanent stat bonuses!", MAGENTA)
    else:
        print_colored("New Game+ cancelled.", YELLOW)

def endless_tower() -> None:
    """Function to handle the Endless Tower challenge"""
    print_header("ENDLESS TOWER")

    current_floor = user_data.get("endless_tower_floor", 0)
    print_colored(f"Current highest floor: {current_floor}", CYAN)

    print_colored("The Endless Tower challenges await...", YELLOW)
    print_colored("Each floor contains stronger enemies than the last.", YELLOW)
    print_colored("How high can you climb?", CYAN)

    options = ["Climb higher", "Claim rewards", "Exit"]
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

    choice = input("\nSelect an option: ")

    if choice == "1":
        # Climb to next floor
        next_floor = current_floor + 1
        print_colored(f"Climbing to floor {next_floor}...", CYAN)

        # Generate a monster based on floor number
        monster = {
            "name": f"Tower Guardian {next_floor}",
            "level": 30 + next_floor,
            "health": 100 + (next_floor * 20),
            "attack": 20 + (next_floor * 3),
            "drops": ["Tower Fragment", "Ancient Coin", "Magic Dust"]
        }

        print_colored(f"You encounter {monster['name']}!", YELLOW)

        # Simulate fight
        fight(monster)

        # If player won, advance to next floor
        if user_data["health"] > 0:
            user_data["endless_tower_floor"] = next_floor
            print_colored(f"You've reached floor {next_floor}!", OKGREEN)

            # Special rewards for milestone floors
            if next_floor == 10:
                user_data["inventory"].append("Tower Champion's Badge")
                print_colored("You've earned the Tower Champion's Badge!", MAGENTA)
            elif next_floor == 25:
                user_data["inventory"].append("Celestial Aegis")
                print_colored("You've earned the CELESTIAL AEGIS!", MAGENTA)
            elif next_floor == 50:
                user_data["inventory"].append("Tower Master's Crown")
                print_colored("You've earned the Tower Master's Crown!", MAGENTA)
        else:
            print_colored("You were defeated! The tower has repelled you.", FAIL)
    elif choice == "2":
        # Calculate rewards based on highest floor
        if current_floor == 0:
            print_colored("You haven't climbed any floors yet!", WARNING)
            return

        gold_reward = current_floor * 100
        exp_reward = current_floor * 50

        user_data["gold"] += gold_reward
        user_data["exp"] += exp_reward

        print_colored(f"You received {gold_reward} gold and {exp_reward} experience!", OKGREEN)
    elif choice == "3":
        return
    else:
        print_colored("Invalid choice.", FAIL)

# Developer settings and commands
DEV_COMMANDS = {
    "/dev_complete": "Complete a dungeon, story, or quest",
    "/dev_give": "Give items, gold, exp, or levels", 
    "/dev_set": "Set health, location, or other stats",
    "/dev_unlock": "Unlock areas, skills, or features",
    "/dev_mode": "Toggle god mode, debug mode, etc"
}

def dev_command_handler(cmd: str) -> None:
    global user_data
    parts = cmd.split()
    base_cmd = parts[0].lower()

    if not parts:
        print("Invalid command format")
        return

    try:
        if base_cmd == "/dev_complete":
            if len(parts) < 3:
                print("Usage: /dev_complete [dungeon/story/quest] [name]")
                return

            complete_type = parts[1]
            name = " ".join(parts[2:])

            if complete_type == "dungeon":
                if name not in user_data["dungeons_completed"]:
                    user_data["dungeons_completed"].append(name)
                    print(f"Completed dungeon: {name}")
            elif complete_type == "quest":
                quest = next((q for q in QUESTS if q["name"].lower() == name.lower()), None)
                if quest:
                    user_data["completed_quests"].append(quest["id"])
                    print(f"Completed quest: {name}")

        elif base_cmd == "/dev_give":
            if len(parts) < 3:
                print("Usage: /dev_give [item/gold/exp/level] [amount/name]")
                return

            give_type = parts[1]
            value = " ".join(parts[2:])

            if give_type == "item":
                user_data["inventory"].append(value)
                print(f"Added {value} to inventory")
            elif give_type in ["gold", "exp", "level"]:
                amount = int(value)
                if give_type == "gold":
                    user_data["gold"] += amount
                elif give_type == "exp":
                    user_data["exp"] += amount
                elif give_type == "level":
                    user_data["level"] += amount
                print(f"Added {amount} {give_type}")

        elif base_cmd == "/dev_set":
            if len(parts) < 3:
                print("Usage: /dev_set [health/location/class] [value]")
                return

            set_type = parts[1]
            value = " ".join(parts[2:])

            if set_type == "health":
                hp = int(value)
                user_data["health"] = hp
                user_data["max_health"] = hp
                print(f"Set health to {hp}")
            elif set_type == "location":
                if value in LOCATIONS:
                    user_data["current_area"] = value
                    print(f"Moved to {value}")
            elif set_type == "class":
                if value in CHARACTER_CLASSES:
                    user_data["class"] = value
                    print(f"Changed class to {value}")

        elif base_cmd == "/dev_unlock":
            if len(parts) < 2:
                print("Usage: /dev_unlock [all/areas/skills]")
                return

            unlock_type = parts[1]

            if unlock_type == "all":
                for location in LOCATIONS:
                    user_data.setdefault("unlocked_areas", []).append(location)
                print("Unlocked everything")
            elif unlock_type == "areas":
                for location in LOCATIONS:
                    user_data.setdefault("unlocked_areas", []).append(location)
                print("Unlocked all areas")
            elif unlock_type == "skills":
                if user_data["class"]:
                    user_data["skills"] = SKILLS[user_data["class"]]
                    print("Unlocked all class skills")

        elif base_cmd == "/dev_mode":
            if len(parts) < 2:
                print("Usage: /dev_mode [god/debug]")
                return

            mode_type = parts[1]

            if mode_type == "god":
                user_data["god_mode"] = not user_data.get("god_mode", False)
                print(f"God mode: {'enabled' if user_data['god_mode'] else 'disabled'}")
            elif mode_type == "debug":
                user_data["debug_mode"] = not user_data.get("debug_mode", False)
                print(f"Debug mode: {'enabled' if user_data['debug_mode'] else 'disabled'}")

    except Exception as e:
        print(f"Error in dev command: {e}")
        print("Use /help_dev to see command usage")

# Weather and Seasons System
def update_weather() -> None:
    """Function to update the weather based on current game time"""
    current_day = game_state["current_day"]
    
    # Check if it's time to change the weather
    if current_day - game_state["last_weather_change"] >= game_state["weather_duration"]:
        dimension = user_data.get("current_dimension", "Overworld")
        
        # Different weather system for different dimensions
        if dimension != "Overworld" and dimension in DIMENSION_WEATHERS:
            # Special dimension-specific weather
            special_weather = random.choice(DIMENSION_WEATHERS[dimension])
            game_state["current_weather"] = special_weather["name"]
            game_state["current_weather_description"] = special_weather["description"]
            game_state["current_weather_color"] = special_weather["color"]
            game_state["current_weather_crop_modifier"] = special_weather["crop_growth_modifier"]
        else:
            # Regular weather
            weathers = []
            weights = []
            
            for weather_id, weather_data in WEATHERS.items():
                weathers.append(weather_id)
                weights.append(weather_data["rarity"])
                
            new_weather = random.choices(weathers, weights=weights, k=1)[0]
            game_state["current_weather"] = new_weather
            game_state["current_weather_description"] = WEATHERS[new_weather]["description"]
            game_state["current_weather_color"] = WEATHERS[new_weather]["color"]
            game_state["current_weather_crop_modifier"] = WEATHERS[new_weather]["crop_growth_modifier"]
            
        # Update weather duration (3-7 days)
        game_state["weather_duration"] = random.randint(3, 7)
        game_state["last_weather_change"] = current_day
        
        # Notify player
        print_colored(f"The weather has changed to: {get_weather_name()}", game_state["current_weather_color"])
        print_colored(f"{get_weather_description()}", LIGHTGRAY)

def update_season() -> None:
    """Function to update the season based on current game time"""
    current_day = game_state["current_day"]
    days_per_season = game_state["days_per_season"]
    
    # Calculate which season it should be
    season_index = (current_day // days_per_season) % len(SEASONS)
    new_season = SEASONS[season_index]
    
    # Check if season changed
    if new_season != game_state["current_season"]:
        game_state["current_season"] = new_season
        game_state["season_day"] = 1
        
        # Notify player
        print_colored(f"The season has changed to {new_season}!", YELLOW)
        
        # Different message for each season
        if new_season == "Spring":
            print_colored("The world blooms with new life and the air is filled with fresh scents.", GREEN)
        elif new_season == "Summer":
            print_colored("The days grow longer and warmer. A perfect time for certain crops.", OKGREEN)
        elif new_season == "Fall":
            print_colored("Leaves change color and the air becomes crisp. Harvest season begins.", YELLOW)
        elif new_season == "Winter":
            print_colored("A chill settles over the land. Few crops will grow in this cold.", CYAN)
    else:
        game_state["season_day"] += 1

def get_weather_name() -> str:
    """Get the current weather name with proper formatting"""
    dimension = user_data.get("current_dimension", "Overworld")
    
    if dimension != "Overworld" and dimension in DIMENSION_WEATHERS:
        # Special dimension-specific weather may already be stored as a name
        return game_state["current_weather"]
    else:
        # Regular weather is stored as an ID, get the name
        return WEATHERS[game_state["current_weather"]]["name"]

def get_weather_description() -> str:
    """Get the current weather description"""
    dimension = user_data.get("current_dimension", "Overworld")
    
    if dimension != "Overworld" and dimension in DIMENSION_WEATHERS:
        # Special dimension-specific weather description
        return game_state["current_weather_description"]
    else:
        # Regular weather description
        return WEATHERS[game_state["current_weather"]]["description"]

def show_weather() -> None:
    """Function to display current weather information"""
    print_header("Current Weather")
    
    weather_name = get_weather_name()
    weather_desc = get_weather_description()
    weather_color = game_state["current_weather_color"]
    
    print_colored(f"Current Weather: {weather_name}", weather_color)
    print_colored(f"Description: {weather_desc}", LIGHTGRAY)
    print_colored("Effect on Crops: ", CYAN, end="")
    
    modifier = game_state["current_weather_crop_modifier"]
    if modifier > 1.0:
        print_colored(f"+{int((modifier-1.0)*100)}% growth rate", OKGREEN)
    elif modifier < 1.0:
        print_colored(f"-{int((1.0-modifier)*100)}% growth rate", FAIL)
    else:
        print_colored("No effect", LIGHTGRAY)
        
    print()
    print_colored("Weather affects how quickly your crops grow and can influence", YELLOW)
    print_colored("certain activities. Each crop has optimal and unfavorable weather.", YELLOW)

def show_season() -> None:
    """Function to display current season information"""
    print_header("Current Season")
    
    season = game_state["current_season"]
    day = game_state["season_day"]
    days_total = game_state["days_per_season"]
    
    season_colors = {
        "Spring": GREEN,
        "Summer": YELLOW,
        "Fall": RED,
        "Winter": CYAN
    }
    
    print_colored(f"Current Season: {season}", season_colors.get(season, LIGHTGRAY))
    print_colored(f"Day: {day}/{days_total}", LIGHTGRAY)
    
    # Season-specific messages
    if season == "Spring":
        print_colored("Best crops: Most common vegetables, berries", OKGREEN)
        print_colored("Spring rains help crops grow quickly.", LIGHTCYAN)
    elif season == "Summer":
        print_colored("Best crops: Heat-loving fruits, peppers, grains", OKGREEN)
        print_colored("The warm weather is perfect for sun-loving plants.", LIGHTYELLOW)
    elif season == "Fall":
        print_colored("Best crops: Root vegetables, gourds, nuts", OKGREEN)
        print_colored("Harvest season brings abundance before winter.", LIGHTRED)
    elif season == "Winter":
        print_colored("Best crops: Frost berries, crystal blooms", OKGREEN)
        print_colored("Few crops grow in winter - a time for planning.", BLUE)
        
    print()
    print_colored("Some crops will only grow during certain seasons.", YELLOW)
    print_colored("Check the crop information before planting!", YELLOW)

def handle_command(cmd: str) -> None:
    allowed_commands_without_character = {"/new", "/load", "/help", "/exit", "/prefix", "/save"}

    parts = cmd.lower().split()
    base_cmd = parts[0] if parts else ""

    # Special handling for /dev command
    if base_cmd == "/dev":
        if len(parts) > 1 and " ".join(parts[1:]) == "activatedevmode":
            user_data["dev_mode"] = True
            print("Developer mode activated! Use /help_dev to see available commands.")
            return
        else:
            print("Incorrect developer command. Use '/dev ACTIVATEDEVMODE' to enable developer mode.")
            return
    elif cmd.lower() == "/help_dev" and user_data.get("dev_mode", False):
        print_header("Developer Commands")
        for command, desc in DEV_COMMANDS.items():
            print(f"{command}: {desc}")
        return

    # Handle developer commands if dev mode is active
    if cmd.split()[0].lower() in DEV_COMMANDS and user_data.get("dev_mode", False):
        dev_command_handler(cmd)
        return
    elif cmd.split()[0].lower() in DEV_COMMANDS and not user_data.get("dev_mode", False):
        print("Developer mode not activated! Use /dev with correct password.")
        return

    # Increment ticks based on command if it's not a no-tick command
    base_command = cmd.split()[0].lower()
    if base_command not in NO_TICK_COMMANDS:
        if base_command in TICK_COMMANDS:
            ticks = random.randint(*TICK_COMMANDS[base_command])
            game_state["current_tick"] += ticks
            game_state["current_day"] = game_state["current_tick"] // TICKS_PER_DAY

            # Update plant growth based on elapsed ticks, weather, and season
            if "farming" in user_data:
                # Update weather and season based on current game time
                update_weather()
                update_season()
                
                current_weather = game_state["current_weather"]
                current_season = game_state["current_season"]
                weather_modifier = game_state.get("current_weather_crop_modifier", 1.0)
                
                for plot in user_data["farming"]["growth"]:
                    crop_name = user_data["farming"]["plots"].get(plot)
                    if not crop_name:
                        continue
                        
                    # Base growth ticks
                    growth_ticks = ticks
                    crop_data = CROPS.get(crop_name, {})
                    
                    # Season modifier - check if current season is optimal for this crop
                    season_modifier = 1.0
                    crop_seasons = crop_data.get("seasons", [])
                    
                    # All-season crops (mainly dimension-specific)
                    if "All" in crop_seasons:
                        season_modifier = 1.2  # Bonus for all-season crops
                    elif current_season in crop_seasons:
                        season_modifier = 1.2  # Good season for this crop
                    else:
                        season_modifier = 0.5  # Bad season - grows slower
                    
                    # Weather modifier - check if current weather is optimal/weak for this crop
                    crop_optimal_weather = crop_data.get("optimal_weather", [])
                    crop_weak_weather = crop_data.get("weak_weather", [])
                    
                    additional_weather_modifier = 1.0
                    if current_weather in crop_optimal_weather:
                        additional_weather_modifier = 1.3  # This weather is perfect for the crop
                    elif current_weather in crop_weak_weather:
                        additional_weather_modifier = 0.7  # This weather harms the crop
                    
                    # Apply all modifiers
                    total_modifier = weather_modifier * season_modifier * additional_weather_modifier
                    
                    # Apply modified growth ticks (convert to integer)
                    modified_ticks = int(growth_ticks * total_modifier)
                    if modified_ticks < 1:
                        modified_ticks = 1  # Ensure at least some growth
                        
                    user_data["farming"]["growth"][plot] += modified_ticks

    elif cmd.startswith("/talk"):
        try:
            parts = cmd.split(" ", 1)
            npc_name = parts[1] if len(parts) > 1 else None
            talk_to_npc(npc_name)
        except Exception as e:
            print(f"{FAIL}Error talking to NPC: {e}{ENDC}")
    elif cmd == "/npcs":
        list_npcs()
    elif cmd == "/story":
        show_storyline()

    if user_data["class"] is None and cmd not in allowed_commands_without_character:
        print_animated("You need to create a character first! Use /new to start your adventure.")
        return

    commands = {
        "/sell": lambda: sell_item(cmd.split(" ", 1)[1] if len(cmd.split(" ", 1)) > 1 else ""),
        "/start": start_guide,
        "/help": show_help,
        "/h": show_help,
        "/pet": show_pets,
        "/search": search_resources,
        "/location": show_location,
        "/location_check": check_location,
        "/professions": show_professions,
        "/prof_system": professions_system,
        "/cook": cook_food,
        "/stats": show_stats,
        "/s_t": show_stats,
        "/shop": visit_shop,
        "/inventory": show_inventory,
        "/i": show_inventory,
        "/quests": show_quests,
        "/gather": lambda: gather_materials(user_data["current_area"]),
        "/craft": craft_item,
        "/materials": print_materials,
        "/travel": travel_to_area,
        "/new": create_character,
        "/save": lambda: save_prompt(),
        "/load": lambda: load_prompt(),
        "/saves": show_save_slots,
        "/delete_save": lambda: delete_save_prompt(),
        "/exit": exit_game,
        "/guild": guild_guide,
        "/guild_join": guild_join,
        "/guild_leave": guild_leave,
        "/guild_list": guild_list,
        # New item enhancement commands
        "/upgrade": upgrade_item,
        "/enchant": enchant_item,
        "/use": lambda: use_potion(cmd.split(" ", 1)[1] if len(cmd.split(" ", 1)) > 1 else ""),
        "/chest": lambda: open_chest(cmd.split(" ", 1)[1] if len(cmd.split(" ", 1)) > 1 else "Common"),
        "/areas": area_guides,
        "/dungeons": dungeon_guides,
        "/timetravel": time_travel_guide,
        "/coolness": coolness_info,
        "/dismantle": dismantle_items,
        "/invcalc": inventory_calculator,
        "/drops": show_drops,
        "/enchants": show_enchants,
        "/trading": trading_system,
        "/gambling": gambling_guide,
        "/codes": redeem_codes,
        "/duel": duel_info,
        "/farm": farming_guide,
        "/tip": random_tip,
        "/support": show_support,
        "/dungeon_list": list_dungeons,
        "/bestiary": show_bestiary,
        "/dailymob": daily_monster,
        "/weapon_info": lambda: show_weapon_info(),
        "/settings": user_settings,
        "/prefix": command_prefix,
        "/pet_adopt": adopt_pet,
        "/pet_train": train_pet,
        "/pet_list": show_pets,
        "/pet_evolve": evolve_pet,
        "/evolve_pet": evolve_pet,
        "/achievement_list": show_achievements,
        "/inventory_sort": sort_inventory,
        "/inventory_filter": filter_inventory,
        "/quest_complete": complete_quest,
        "/quest_list": list_active_quests,
        "/q": list_active_quests,
        "/l": load_prompt,
        "/x": exit_game,
        # Dimensions system commands
        "/dimensions": dimensions_menu,
        "/dim": dimensions_menu,
        "/find_key": find_dimension_key,
        "/return_home": returnToOverworld,
        # Home/camp system commands
        "/camp": camp_menu,
        "/camp_build": build_structure,
        "/camp_repair": repair_structure,
        "/camp_use": use_structure,
        "/camp_demolish": demolish_structure,
        "/camp_info": view_structure_info,
        
        # Weather and season commands
        "/weather": show_weather,
        "/season": show_season,
        "/c": create_character,
        "/g": guild_guide,
        "/d": dungeon_guides,
        "/f": fight_monster,
        "/t": travel_to_area,
        "/a": show_achievements,
        "/m": print_materials,
        "/r": redeem_codes,
        "/u": user_settings,
        "/z": show_save_slots
    }

    # Handle commands with arguments
    if cmd.startswith("/fight "):
        fight_monster(cmd.split(" ", 1)[1])
    elif cmd.startswith("/equip "):
        equip_item(cmd.split(" ", 1)[1])
    elif cmd.startswith("/dungeon "):
        enter_dungeon(cmd.split(" ", 1)[1])
    elif cmd.startswith("/guild_join "):
        guild_join(cmd.split(" ", 1)[1])
    elif cmd.startswith("/guild_leave"):
        guild_leave()
    elif cmd.startswith("/pet_adopt "):
        adopt_pet(cmd.split(" ", 1)[1])
    elif cmd.startswith("/pet_train "):
        train_pet(cmd.split(" ", 1)[1])
    elif cmd.startswith("/pet_evolve ") or cmd.startswith("/evolve_pet "):
        # Extract pet name from either command format
        pet_name = cmd.split(" ", 1)[1]
        evolve_pet(pet_name)
    elif cmd.startswith("/quest_complete "):
        complete_quest(cmd.split(" ", 1)[1])
    # Post-game commands
    elif cmd == "/postgame":
        show_postgame_content()
    elif cmd == "/rifts":
        dimensional_rifts()
    elif cmd == "/trials":
        divine_trials()
    elif cmd == "/legendary_hunts":
        legendary_hunts()
    elif cmd == "/time_trials":
        time_trials()
    elif cmd == "/newgame+":
        new_game_plus()
    elif cmd == "/tower":
        endless_tower()
    elif cmd.startswith("/inspect "):
        inspect_item(cmd.split(" ", 1)[1])
    elif cmd in commands:
        commands[cmd]()
    else:
        print_animated("Unknown command. Type '/help' for a list of commands.")

# Define functions
def start_guide() -> None:
    print_header("Starter Guide")
    print("Welcome to TextRP CLI! Type /help for help!")

def area_guides() -> None:
    print_header("Area Guides")
    print("Areas: Forest, Cave, Desert, Snowy Peaks...")

def dungeon_guides() -> None:
    print_header("Dungeon Guides")
    print("Dungeons are challenging! Bring a team and gear up.")

def coolness_info() -> None:
    print_header("Coolness")
    print("Coolness is a rare stat that boosts drop rates and XP gain.")

def random_tip() -> None:
    tips = [
        "Always carry health potions!",
        "Upgrade your gear before dungeons.",
    ]
    print_header("Random Tip")
    print(random.choice(tips))

def guild_guide() -> None:
    print_header("Adventurer's Guild")
    
    # Initialize adventurer data if it doesn't exist
    if "adventurer" not in user_data:
        user_data["adventurer"] = {
            "rank": "Novice",
            "exp": 0,
            "level": 1,
            "total_quests": 0,
            "bosses_defeated": 0,
            "reputation": 0
        }
    
    adv = user_data["adventurer"]
    exp_required = adv["level"] * 100
    
    print(f"{CYAN}Adventurer Rank:{ENDC} {adv['rank']}")
    print(f"{CYAN}Adventurer Level:{ENDC} {adv['level']}")
    print(f"{CYAN}Experience:{ENDC} {adv['exp']}/{exp_required}")
    print(f"{CYAN}Quests Completed:{ENDC} {adv['total_quests']}")
    print(f"{CYAN}Bosses Defeated:{ENDC} {adv['bosses_defeated']}")
    print(f"{CYAN}Guild Reputation:{ENDC} {adv['reputation']}")
    
    # Create progress bar for experience
    exp_percentage = min(100, (adv['exp'] / exp_required) * 100)
    progress_bar = create_progress_bar(exp_percentage)
    print(f"\n{CYAN}Progress:{ENDC} [{progress_bar}] {int(exp_percentage)}%")
    
    # Show available rank advancements
    next_rank = get_next_rank(adv["rank"])
    if next_rank:
        print(f"\n{YELLOW}Next Rank:{ENDC} {next_rank['name']}")
        print(f"{YELLOW}Requirements:{ENDC} Level {next_rank['level_req']}, {next_rank['quest_req']} Quests, {next_rank['boss_req']} Bosses")
    
    # Show rewards for current level
    print(f"\n{GREEN}Active Benefits:{ENDC}")
    for level in range(1, adv["level"] + 1):
        rewards = get_adventurer_level_rewards(level)
        if rewards:
            print(f"- Level {level}: {rewards['description']}")
    
    # Show guild facilities
    print(f"\n{PURPLE}Adventurer's Guild Facilities:{ENDC}")
    print(f"- {LIGHTBLUE}Quest Board{ENDC}: Special quests for adventurers")
    print(f"- {LIGHTBLUE}Trading Post{ENDC}: Exchange rare items with other adventurers")
    print(f"- {LIGHTBLUE}Training Ground{ENDC}: Practice combat techniques")
    print(f"- {LIGHTBLUE}Research Library{ENDC}: Learn about monsters and dungeons")
    print(f"- {LIGHTBLUE}Trophy Hall{ENDC}: Display your greatest achievements")

def user_settings() -> None:
    print_header("User Settings")
    print(f"Level: {user_data['level']}")
    print(f"Gold: {user_data['gold']}")
    print(f"Coolness: {user_data['coolness']}")
    print(f"Guild: {user_data['guild']}")
    print(f"Pets: {', '.join(user_data['pets']) if user_data['pets'] else 'No pets'}")
    print(f"Health: {user_data['health']}/{user_data['max_health']}")
    print(f"Experience: {user_data['exp']}")
    print(f"Current Area: {user_data['current_area']}")
    print_materials()

def command_prefix() -> None:
    print_header("Command Prefix")
    print("Prefix for commands is '/'. Use '/help' for all available commands.")

def exit_game() -> None:
    print_animated("Exiting game...", BLUE, 0.01)
    print_animated("Goodbye!", BLUE, 0.01)
    sys.exit()

def show_villages() -> None:
    print_header("Villages")
    for village in villages:
        print(f"Name: {village['name']}, Population: {village['population']}, Special Items: {', '.join(village['special_items'])}")

def show_biomes() -> None:
    print_header("Biomes")
    for biome in biomes:
        print(f"Name: {biome['name']}, Description: {biome['description']}")

def join_guild(guild_name: str) -> None:
    user_data["guild"] = guild_name
    print_header("Join Guild")
    print(f"Successfully joined the {guild_name} guild!")

def adopt_pet(pet_name: str) -> None:
    if pet_name in PETS:
        if pet_name in user_data["pets"]:
            print(f"You already have a pet named {pet_name}.")
        else:
            user_data["pets"].append(pet_name)
            print(f"You have adopted a pet: {pet_name}.")
    else:
        print(f"No pet named {pet_name} found.")
    print_header("Adopt Pet")
    print(f"Adopted a new pet named {pet_name}!")

def show_mobs(area: Optional[str] = None) -> None:
    print_header("Monsters")
    target_area = area if area else user_data.get("current_area", "")

    if target_area not in LOCATIONS:
        print(f"Invalid area: {target_area}")
        return

    area_monster_names = LOCATIONS[target_area].get("monsters", [])
    area_monsters = [m for m in monsters if m["name"] in area_monster_names]

    if area_monsters:
        print(f"Monsters in {target_area}:")
        for monster in area_monsters:
            print(f"- {monster['name']} (Level {monster['level']})")
            print(f"  Health: {monster['health']}, Attack: {monster['attack']}")
            if monster.get("boss", False):
                print(f"  {RED}⚠ BOSS MONSTER ⚠{ENDC}")
    else:
        print(f"No monsters found in {target_area}")

# Function to handle a fight with a monster (used in dungeons)
def fight(monster: Dict) -> None:
    """
    Enhanced combat system with combo mechanics, status effects, and visual feedback
    Includes pet integration with abilities and elemental interactions
    """
    if not user_data["class"]:
        print(f"{FAIL}You need to create a character first! Use /new{ENDC}")
        return

    if user_data["health"] <= 0:
        print(f"{FAIL}You can't fight while defeated! Use a healing potion or rest.{ENDC}")
        return

    # Initialize combat state variables
    combo_counter = 0
    max_combo = 3  # Can build up to 3-hit combos
    stunned = False
    monster_stunned = False
    combat_log = []  # Track recent actions for combo detection
    player_status_effects = []  # Track temporary buffs/debuffs
    monster_status_effects = []
    
    # Pet combat variables
    active_pet = get_active_pet()
    pet_shield_active = False
    pet_shield_duration = 0
    pet_dodge_bonus = 0
    # Track turns for pet ability cooldowns in future implementation
    
    # Extract monster data with defaults
    monster_health = monster["health"]
    monster_name = monster["name"]
    monster_level = monster["level"]
    monster_element = monster.get("element", "Normal")
    
    # Get player element
    player_element = user_data.get("element", "Normal")
    
    # Battle intro with fancy visuals
    print_header(f"⚔️ COMBAT: {monster_name} ⚔️")
    print_animated(f"{BG_RED}{WHITE} BATTLE START! {ENDC}", delay=0.05)
    print_animated(f"You encountered a {LIGHTRED}{monster_name}{ENDC} (Level {YELLOW}{monster_level}{ENDC})!", delay=0.03)
    
    if monster.get("boss", False):
        print_animated(f"{BG_MAGENTA}{WHITE}❗ BOSS BATTLE ❗{ENDC}", delay=0.05)
        print_animated(f"{monster.get('description', 'A powerful foe stands before you!')}", LIGHTMAGENTA, delay=0.03)
    
    # Display monster's element if available
    if monster_element != "Normal":
        print_animated(f"Element: {get_element_color(monster_element)}{monster_element}{ENDC}", delay=0.02)
    
    # Main combat loop
    turn_counter = 0
    while user_data["health"] > 0 and monster_health > 0:
        turn_counter += 1
        try:
            # Display health bars with visual representation
            player_health_percent = user_data["health"] / user_data["max_health"]
            monster_health_percent = monster_health / monster["health"]
            
            # Create health bars
            player_health_bar = create_health_bar(player_health_percent, 20)
            monster_health_bar = create_health_bar(monster_health_percent, 20)
            
            print(f"\n{BOLD}Turn {turn_counter}{ENDC}")
            print(f"\n{CYAN}Your Health: {user_data['health']}/{user_data['max_health']} {player_health_bar}{ENDC}")
            print(f"{LIGHTRED}Enemy Health: {monster_health}/{monster['health']} {monster_health_bar}{ENDC}")
            
            # Display active status effects
            if player_status_effects:
                effects_str = ", ".join([f"{e['name']} ({e['duration']})" for e in player_status_effects])
                print(f"{LIGHTYELLOW}Your Status: {effects_str}{ENDC}")
            if monster_status_effects:
                effects_str = ", ".join([f"{e['name']} ({e['duration']})" for e in monster_status_effects])
                print(f"{LIGHTYELLOW}Enemy Status: {effects_str}{ENDC}")
            
            # Display combo counter if active
            if combo_counter > 0:
                print(f"{LIGHTMAGENTA}Combo: x{combo_counter}{ENDC}")
                
            # Display active pet information if any
            if active_pet:
                pet_name = active_pet["name"]
                pet_level = active_pet.get("level", 1)
                pet_element = active_pet.get("element", "Nullum")
                pet_element_display = f" | {get_element_color(pet_element)}{pet_element}{ENDC}" if pet_element != "Nullum" else ""
                
                # Display pet status
                print(f"\n{CYAN}Active Pet: {pet_name} (Lvl {pet_level}){pet_element_display}{ENDC}")
                
                # Show active abilities if any
                pet_abilities = active_pet.get("abilities", [])
                if pet_abilities and pet_shield_active:
                    print(f"{YELLOW}Pet Shield: Active ({pet_shield_duration} turns){ENDC}")
            
            # Check if player is stunned
            if stunned:
                print(f"{YELLOW}You are stunned and cannot act this turn!{ENDC}")
                stunned = False  # Stun lasts one turn
            else:
                # Actions menu
                print("\n⚔️ Actions:")
                print(f"{LIGHTCYAN}1. Attack{ENDC}")
                print(f"{LIGHTGREEN}2. Use Skill{ENDC}")
                print(f"{LIGHTBLUE}3. Use Item{ENDC}")
                # Show pet command option if a pet is active
                if active_pet and active_pet.get("abilities", []):
                    print(f"{MAGENTA}4. Pet Command{ENDC}")
                    print(f"{YELLOW}5. Defend{ENDC}")
                    print(f"{LIGHTRED}6. Flee{ENDC}")
                else:
                    print(f"{YELLOW}4. Defend{ENDC}")
                    print(f"{LIGHTRED}5. Flee{ENDC}")
                
                max_choice = "6" if active_pet and active_pet.get("abilities", []) else "5"
                choice = input(f"{YELLOW}Choose action (1-{max_choice}): {ENDC}").strip()
                
                if choice == "1":  # Basic Attack
                    # Calculate damage with equipped weapon and combo bonus
                    base_damage = user_data.get("attack", 10)
                    weapon_bonus = user_data.get("equipped", {}).get("weapon", {}).get("effect", 0)
                    combo_bonus = int(combo_counter * base_damage * 0.2)  # 20% bonus damage per combo point
                    
                    # Calculate critical hit
                    is_critical = random.random() < (CRITICAL_CHANCE + combo_counter * 0.05)  # Combo increases crit chance
                    
                    # Calculate total damage
                    damage = base_damage + weapon_bonus + combo_bonus
                    
                    if is_critical:
                        crit_multiplier = 2.0
                        # Apply class-specific crit bonuses
                        if user_data["class"] == "Rogue":
                            crit_multiplier = 2.5
                        elif user_data["class"] == "Archer":
                            crit_multiplier = 2.2
                            
                        damage = int(damage * crit_multiplier)
                        print_animated(f"{BG_YELLOW}{BLACK} CRITICAL HIT! {ENDC}", delay=0.02)
                    
                    # Apply elemental damage modifiers
                    elemental_result = calculate_elemental_damage(player_element, monster_element, damage)
                    damage = elemental_result[0]
                    effect_message = elemental_result[1]
                    elemental_effects = elemental_result[2]
                    
                    # Apply damage
                    monster_health -= damage
                    
                    # Apply any elemental effects to monster
                    if elemental_effects:
                        for effect_name, effect_data in elemental_effects.items():
                            monster_status_effects.append({
                                "name": effect_name,
                                "duration": effect_data.get("duration", 2),
                                "effect": effect_data
                            })
                    
                    # Display attack results
                    print_animated(f"You {get_attack_verb(combo_counter)} the {monster_name} for {LIGHTGREEN}{damage}{ENDC} damage!", delay=0.02)
                    if effect_message:
                        print_animated(f"{LIGHTCYAN}{effect_message}{ENDC}", delay=0.02)
                    
                    # Update combo counter
                    combat_log.append("attack")
                    if len(combat_log) >= 3 and combat_log[-3:] == ["attack", "attack", "attack"]:
                        # Reset combo after 3 consecutive attacks
                        print_animated(f"{BG_MAGENTA}{WHITE} COMBO FINISHER! {ENDC}", delay=0.02)
                        combo_counter = 0
                        combat_log = []
                        # Apply stun effect on combo finisher
                        monster_stunned = True
                        print_animated(f"The {monster_name} is stunned!", LIGHTYELLOW, delay=0.02)
                    else:
                        combo_counter = min(combo_counter + 1, max_combo)
                
                elif choice == "2":  # Use Skill
                    if user_data["skills"]:
                        print("\nAvailable skills:")
                        for i, skill in enumerate(user_data["skills"], 1):
                            # Get skill details if available
                            skill_name = skill if isinstance(skill, str) else skill.get("name", "Unknown Skill")
                            skill_desc = skill.get("description", "No description") if isinstance(skill, dict) else ""
                            skill_element = skill.get("element", player_element) if isinstance(skill, dict) else player_element
                            
                            # Display with element color
                            print(f"[{i}] {get_element_color(skill_element)}{skill_name}{ENDC} - {skill_desc}")
                            
                        try:
                            skill_choice = int(input("Choose skill (0 to cancel): "))
                            if skill_choice == 0:
                                continue
                                
                            if 1 <= skill_choice <= len(user_data["skills"]):
                                skill = user_data["skills"][skill_choice - 1]
                                skill_name = skill if isinstance(skill, str) else skill.get("name", "Unknown Skill")
                                skill_element = skill.get("element", player_element) if isinstance(skill, dict) else player_element
                                
                                # Base skill damage calculation
                                intellect_bonus = user_data.get("intellect", 0) * 0.5
                                base_skill_damage = random.randint(15, 25) + int(intellect_bonus)
                                
                                # Calculate skill-specific damage
                                if isinstance(skill, dict) and "damage_multiplier" in skill:
                                    skill_multiplier = skill.get("damage_multiplier", 1.0)
                                    damage = int(base_skill_damage * skill_multiplier)
                                else:
                                    damage = base_skill_damage
                                
                                # Apply elemental damage modifiers
                                elemental_result = calculate_elemental_damage(skill_element, monster_element, damage)
                                damage = elemental_result[0]
                                effect_message = elemental_result[1]
                                elemental_effects = elemental_result[2]
                                
                                # Apply damage
                                monster_health -= damage
                                
                                # Apply any elemental effects
                                if elemental_effects:
                                    for effect_name, effect_data in elemental_effects.items():
                                        monster_status_effects.append({
                                            "name": effect_name,
                                            "duration": effect_data.get("duration", 2),
                                            "effect": effect_data
                                        })
                                
                                # Display skill results with visual effects
                                print_animated(f"{BG_CYAN}{WHITE} SKILL ACTIVATED! {ENDC}", delay=0.02)
                                print_animated(f"You cast {get_element_color(skill_element)}{skill_name}{ENDC} and deal {LIGHTGREEN}{damage}{ENDC} damage!", delay=0.02)
                                if effect_message:
                                    print_animated(f"{LIGHTCYAN}{effect_message}{ENDC}", delay=0.02)
                                
                                # Special skill effects
                                if isinstance(skill, dict) and "effects" in skill:
                                    for effect, value in skill["effects"].items():
                                        if effect == "heal":
                                            heal_amount = int(value)
                                            user_data["health"] = min(user_data["health"] + heal_amount, user_data["max_health"])
                                            print_animated(f"You recover {LIGHTGREEN}{heal_amount}{ENDC} health!", delay=0.02)
                                        elif effect == "stun":
                                            if random.random() < value:
                                                monster_stunned = True
                                                print_animated(f"The {monster_name} is stunned!", LIGHTYELLOW, delay=0.02)
                                        elif effect == "combo":
                                            combo_counter = min(combo_counter + value, max_combo)
                                            print_animated(f"Combo increased to {LIGHTMAGENTA}x{combo_counter}{ENDC}!", delay=0.02)
                                
                                # Reset combo counter after using a skill
                                combat_log = []
                            else:
                                print("Invalid skill choice.")
                                
                        except ValueError:
                            print("Invalid input.")
                    else:
                        print(f"{YELLOW}You have no skills available!{ENDC}")
                        continue
                        
                elif choice == "3":  # Use Item
                    # Get a list of usable combat items
                    combat_items = [item for item in user_data["inventory"] 
                                  if item in ["Healing Potion", "Mana Potion", "Strength Potion", 
                                             "Defense Potion", "Speed Potion", "Bomb"]]
                    
                    if combat_items:
                        print("\nUsable items:")
                        for i, item in enumerate(combat_items, 1):
                            print(f"[{i}] {item}")
                            
                        try:
                            item_choice = int(input("Choose item (0 to cancel): "))
                            if item_choice == 0:
                                continue
                                
                            if 1 <= item_choice <= len(combat_items):
                                item_name = combat_items[item_choice - 1]
                                
                                # Apply item effects
                                if item_name == "Healing Potion":
                                    heal_amount = int(user_data["max_health"] * 0.3)  # 30% of max health
                                    user_data["health"] = min(user_data["health"] + heal_amount, user_data["max_health"])
                                    print_animated(f"{BG_GREEN}{BLACK} ITEM USED! {ENDC}", delay=0.02)
                                    print_animated(f"You used a Healing Potion and recovered {LIGHTGREEN}{heal_amount}{ENDC} health!", delay=0.02)
                                    
                                elif item_name == "Strength Potion":
                                    # Add temporary strength buff
                                    player_status_effects.append({
                                        "name": "Strength Up",
                                        "duration": 3,
                                        "effect": {"attack": 10}
                                    })
                                    print_animated(f"{BG_GREEN}{BLACK} ITEM USED! {ENDC}", delay=0.02)
                                    print_animated("You used a Strength Potion! Attack increased for 3 turns.", delay=0.02)
                                    
                                elif item_name == "Defense Potion":
                                    # Add temporary defense buff
                                    player_status_effects.append({
                                        "name": "Defense Up",
                                        "duration": 3,
                                        "effect": {"defense": 10}
                                    })
                                    print_animated(f"{BG_GREEN}{BLACK} ITEM USED! {ENDC}", delay=0.02)
                                    print_animated("You used a Defense Potion! Defense increased for 3 turns.", delay=0.02)
                                    
                                elif item_name == "Speed Potion":
                                    # Add temporary speed buff
                                    player_status_effects.append({
                                        "name": "Speed Up",
                                        "duration": 3,
                                        "effect": {"speed": 5}
                                    })
                                    print_animated(f"{BG_GREEN}{BLACK} ITEM USED! {ENDC}", delay=0.02)
                                    print_animated("You used a Speed Potion! Speed increased for 3 turns.", delay=0.02)
                                    
                                elif item_name == "Bomb":
                                    # Deal direct damage to monster
                                    bomb_damage = 50  # Fixed damage
                                    monster_health -= bomb_damage
                                    print_animated(f"{BG_GREEN}{BLACK} ITEM USED! {ENDC}", delay=0.02)
                                    print_animated(f"You threw a Bomb! The {monster_name} takes {LIGHTRED}{bomb_damage}{ENDC} damage!", delay=0.02)
                                
                                # Remove the item after use
                                user_data["inventory"].remove(item_name)
                                
                            else:
                                print("Invalid item choice.")
                                
                        except ValueError:
                            print("Invalid input.")
                    else:
                        print(f"{YELLOW}You have no usable combat items!{ENDC}")
                        continue
                
                elif choice == "4" and active_pet and active_pet.get("abilities", []):  # Pet Command
                    # Get active pet abilities
                    pet_abilities = []
                    pet_stats = user_data["pet_stats"].get(active_pet["name"], {}).get("level", 1)
                    pet_loyalty = user_data["pet_stats"].get(active_pet["name"], {}).get("loyalty", 50)
                    
                    # Get abilities available at current pet level
                    for level_req, ability_name in active_pet.get("abilities", {}).items():
                        if int(level_req) <= pet_stats:
                            pet_abilities.append(ability_name)
                    
                    if not pet_abilities:
                        print_animated(f"{YELLOW}{active_pet['name']} doesn't know any abilities yet. Train your pet more!{ENDC}", delay=0.02)
                        continue
                        
                    # Display pet abilities
                    print(f"\n{CYAN}{active_pet['name']}'s Abilities:{ENDC}")
                    for i, ability in enumerate(pet_abilities, 1):
                        ability_desc = ABILITY_DESCRIPTIONS.get(ability, "No description available")
                        print(f"{i}. {MAGENTA}{ability}{ENDC} - {ability_desc}")
                    
                    print(f"0. {YELLOW}Back{ENDC}")
                    
                    try:
                        ability_choice = int(input("Choose ability (0 to cancel): "))
                        if ability_choice == 0:
                            continue
                            
                        if 1 <= ability_choice <= len(pet_abilities):
                            selected_ability = pet_abilities[ability_choice-1]
                            
                            # Check loyalty for ability success
                            loyalty_check_passed = True
                            if pet_loyalty < 30 and random.random() < 0.3:  # 30% chance to fail at low loyalty
                                print_animated(f"{RED}{active_pet['name']} ignores your command!{ENDC}", delay=0.02)
                                loyalty_check_passed = False
                            
                            if loyalty_check_passed:
                                # Process pet ability
                                if selected_ability == "Quick Attack":
                                    # Pet deals small damage
                                    pet_damage = int(user_data.get("attack", 10) * 0.1)  # 10% of player attack
                                    monster_health -= pet_damage
                                    print_animated(f"{CYAN}{active_pet['name']} dashes forward with a quick attack, dealing {LIGHTRED}{pet_damage}{ENDC} damage!", delay=0.02)
                                
                                elif selected_ability == "Protective Stance":
                                    # Pet provides damage reduction
                                    pet_shield_active = True
                                    pet_shield_duration = 3
                                    print_animated(f"{CYAN}{active_pet['name']} takes a protective stance, ready to block incoming attacks!{ENDC}", delay=0.02)
                                
                                elif selected_ability == "Flame Burst":
                                    # Pet deals fire elemental damage
                                    pet_damage = int(user_data.get("attack", 10) * 0.15)  # 15% of player attack
                                    # Apply elemental damage calculation
                                    final_damage, reaction_name, reaction_effect = calculate_elemental_damage("Fire", monster_element, pet_damage)
                                    monster_health -= final_damage
                                    
                                    print_animated(f"{CYAN}{active_pet['name']} unleashes a burst of {RED}flames{ENDC}, dealing {LIGHTRED}{final_damage}{ENDC} damage!", delay=0.02)
                                    
                                    if reaction_name:
                                        print_animated(f"{YELLOW}Elemental Reaction: {reaction_name}!{ENDC}", delay=0.02)
                                        apply_elemental_effects(monster, reaction_effect, is_player=False)
                                
                                elif selected_ability == "Healing Mist":
                                    # Pet heals player
                                    heal_amount = int(user_data.get("max_health", 100) * 0.1)  # 10% of max health
                                    user_data["health"] = min(user_data["health"] + heal_amount, user_data["max_health"])
                                    print_animated(f"{CYAN}{active_pet['name']} creates a healing mist, restoring {GREEN}{heal_amount}{ENDC} health!", delay=0.02)
                                
                                elif selected_ability == "Stone Shield":
                                    # Pet creates a stronger shield
                                    pet_shield_active = True
                                    pet_shield_duration = 3
                                    player_status_effects.append({
                                        "name": "Stone Shield",
                                        "duration": 3,
                                        "effect": {"defense": int(user_data.get("defense", 5) * 0.15)}  # 15% defense boost
                                    })
                                    print_animated(f"{CYAN}{active_pet['name']} creates a shield of stone around you!{ENDC}", delay=0.02)
                                
                                elif selected_ability == "Swift Movement":
                                    # Pet increases dodge chance
                                    pet_dodge_bonus = 0.1  # +10% dodge chance
                                    player_status_effects.append({
                                        "name": "Swift Movement",
                                        "duration": 3,
                                        "effect": {"speed": int(user_data.get("speed", 5) * 0.2)}  # 20% speed boost
                                    })
                                    print_animated(f"{CYAN}{active_pet['name']} enhances your agility, making you more difficult to hit!{ENDC}", delay=0.02)
                                
                                elif selected_ability == "Shock Strike":
                                    # Pet deals lightning damage with stun chance
                                    pet_damage = int(user_data.get("attack", 10) * 0.15)  # 15% of player attack
                                    # Apply elemental damage calculation
                                    final_damage, reaction_name, reaction_effect = calculate_elemental_damage("Lightning", monster_element, pet_damage)
                                    monster_health -= final_damage
                                    
                                    print_animated(f"{CYAN}{active_pet['name']} strikes with {YELLOW}lightning{ENDC}, dealing {LIGHTRED}{final_damage}{ENDC} damage!", delay=0.02)
                                    
                                    # Chance to stun
                                    if random.random() < 0.15:  # 15% stun chance
                                        monster_stunned = True
                                        print_animated(f"{YELLOW}The {monster_name} is stunned!{ENDC}", delay=0.02)
                                        
                                    if reaction_name:
                                        print_animated(f"{YELLOW}Elemental Reaction: {reaction_name}!{ENDC}", delay=0.02)
                                        apply_elemental_effects(monster, reaction_effect, is_player=False)
                                
                                elif selected_ability == "Energy Pulse":
                                    # Pet deals neutral damage
                                    pet_damage = int(user_data.get("attack", 10) * 0.12)  # 12% of player attack
                                    monster_health -= pet_damage
                                    print_animated(f"{CYAN}{active_pet['name']} releases a pulse of neutral energy, dealing {LIGHTRED}{pet_damage}{ENDC} damage!", delay=0.02)
                                
                                elif selected_ability == "Find Treasure":
                                    # No direct combat effect, will be checked during loot
                                    print_animated(f"{CYAN}{active_pet['name']} is keeping an eye out for extra treasures!{ENDC}", delay=0.02)
                                    # Just to not waste a turn
                                    pet_damage = int(user_data.get("attack", 10) * 0.05)  # 5% of player attack
                                    monster_health -= pet_damage
                                    print_animated(f"{CYAN}While searching, {active_pet['name']} deals {LIGHTRED}{pet_damage}{ENDC} damage!", delay=0.02)
                                
                                elif selected_ability == "Intimidate":
                                    # Chance for weaker enemies to flee
                                    if monster_level < user_data.get("level", 1) and random.random() < 0.3:  # 30% chance if monster is lower level
                                        monster_health = 0  # Force end combat
                                        print_animated(f"{CYAN}{active_pet['name']} lets out a terrifying sound! The {monster_name} flees in fear!{ENDC}", delay=0.02)
                                    else:
                                        # If intimidate fails, still deal some damage and reduce enemy attack
                                        pet_damage = int(user_data.get("attack", 10) * 0.08)  # 8% of player attack
                                        monster_health -= pet_damage
                                        monster_status_effects.append({
                                            "name": "Intimidated",
                                            "duration": 2,
                                            "effect": {"attack": -int(monster["attack"] * 0.15)}  # Reduce enemy attack by 15%
                                        })
                                        print_animated(f"{CYAN}{active_pet['name']} intimidates the {monster_name}, lowering its attack power!{ENDC}", delay=0.02)
                                
                                elif selected_ability == "Fierce Loyalty":
                                    # Only activates when player health is low, gives damage boost
                                    if user_data["health"] < user_data["max_health"] * 0.2:  # Below 20% health
                                        pet_damage = int(user_data.get("attack", 10) * 0.25)  # 25% of player attack
                                        monster_health -= pet_damage
                                        print_animated(f"{CYAN}Seeing you in danger, {active_pet['name']} attacks fiercely for {LIGHTRED}{pet_damage}{ENDC} damage!{ENDC}", delay=0.02)
                                    else:
                                        # Regular attack if health isn't low
                                        pet_damage = int(user_data.get("attack", 10) * 0.1)  # 10% of player attack
                                        monster_health -= pet_damage
                                        print_animated(f"{CYAN}{active_pet['name']} loyally attacks for {LIGHTRED}{pet_damage}{ENDC} damage!{ENDC}", delay=0.02)
                                
                                # Pet gains experience from battle
                                if "pet_stats" not in user_data:
                                    user_data["pet_stats"] = {}
                                    
                                if active_pet["name"] not in user_data["pet_stats"]:
                                    user_data["pet_stats"][active_pet["name"]] = {
                                        "level": 1,
                                        "exp": 0,
                                        "exp_next": 100,
                                        "loyalty": 50,
                                        "abilities": [],
                                        "element": active_pet.get("element", "Nullum")
                                    }
                                    
                                # Add some exp for using ability in battle
                                user_data["pet_stats"][active_pet["name"]]["exp"] += 3
                                
                        else:
                            print("Invalid ability selection.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                
                elif choice == "5" and active_pet and active_pet.get("abilities", []) or choice == "4":  # Defend
                    # Reduce incoming damage and gain a small health recovery
                    defense_buff = int(user_data.get("defense", 5) * 0.5)
                    player_status_effects.append({
                        "name": "Defending",
                        "duration": 1,
                        "effect": {"defense": defense_buff}
                    })
                    
                    # Heal a small amount
                    heal_amount = int(user_data["max_health"] * 0.05)  # 5% of max health
                    user_data["health"] = min(user_data["health"] + heal_amount, user_data["max_health"])
                    
                    # Gain a combo point
                    combo_counter = min(combo_counter + 1, max_combo)
                    
                    print_animated(f"{BG_BLUE}{WHITE} DEFENDING! {ENDC}", delay=0.02)
                    print_animated(f"You take a defensive stance! Reduced damage for 1 turn and recovered {LIGHTGREEN}{heal_amount}{ENDC} health.", delay=0.02)
                    print_animated(f"Combo increased to {LIGHTMAGENTA}x{combo_counter}{ENDC}!", delay=0.02)
                    
                    # Update combat log
                    combat_log.append("defend")
                
                elif choice == "6" and active_pet and active_pet.get("abilities", []) or choice == "5" and not (active_pet and active_pet.get("abilities", [])):  # Flee
                    # Calculate flee chance based on speed and status
                    player_speed = user_data.get("speed", 5)
                    monster_speed = monster.get("speed", 5)
                    
                    # Apply speed buffs from status effects
                    for effect in player_status_effects:
                        if "speed" in effect["effect"]:
                            player_speed += effect["effect"]["speed"]
                    
                    base_chance = 0.4  # Base flee chance
                    speed_diff = player_speed - monster_speed
                    flee_chance = base_chance + (speed_diff * 0.05)
                    
                    # Boss battles are harder to flee from
                    if monster.get("boss", False):
                        flee_chance *= 0.5
                    
                    # Clamp between 10% and 90%
                    flee_chance = max(0.1, min(flee_chance, 0.9))
                    
                    # Roll for success
                    if random.random() < flee_chance:
                        print_animated(f"{BG_GREEN}{BLACK} ESCAPED! {ENDC}", delay=0.02)
                        print_animated("You successfully fled from battle!", delay=0.02)
                        return
                    else:
                        print_animated(f"{BG_RED}{WHITE} FAILED TO ESCAPE! {ENDC}", delay=0.02)
                        print_animated("You couldn't escape!", delay=0.02)
                        # Reset combo after failed flee
                        combo_counter = 0
                        combat_log = []
                
                else:
                    print(f"{YELLOW}Invalid choice!{ENDC}")
                    continue
            
            # Update status effects
            player_status_effects = [effect for effect in player_status_effects if effect["duration"] > 0]
            for effect in player_status_effects:
                effect["duration"] -= 1
            
            monster_status_effects = [effect for effect in monster_status_effects if effect["duration"] > 0]
            for effect in monster_status_effects:
                effect["duration"] -= 1
            
            # Monster's turn if it's still alive and not stunned
            if monster_health > 0:
                if monster_stunned:
                    print_animated(f"The {monster_name} is stunned and cannot attack!", LIGHTYELLOW, delay=0.02)
                    monster_stunned = False  # Reset stun for next turn
                else:
                    print_animated(f"\n{LIGHTRED}Enemy's turn!{ENDC}", delay=0.02)
                    
                    # Calculate base monster damage
                    monster_attack = monster["attack"]
                    
                    # Calculate player defense with equipment and status effects
                    defense_bonus = user_data.get("equipped", {}).get("armor", {}).get("effect", 0)
                    for effect in player_status_effects:
                        if "defense" in effect["effect"]:
                            defense_bonus += effect["effect"]["defense"]
                    
                    # Calculate final damage
                    damage_taken = max(1, monster_attack - defense_bonus)
                    
                    # Check for pet shield effect
                    if pet_shield_active and pet_shield_duration > 0 and active_pet:
                        # Check for Protective Stance ability
                        if "Protective Stance" in active_pet.get("abilities", {}).values():
                            # 20% chance to block damage
                            if random.random() < 0.2:
                                blocked_damage = int(damage_taken * 0.3)  # Block 30% of damage
                                damage_taken -= blocked_damage
                                print_animated(f"{CYAN}{active_pet['name']} blocks {blocked_damage} damage!{ENDC}", delay=0.02)
                        
                        # Decrement pet shield duration
                        pet_shield_duration -= 1
                        if pet_shield_duration <= 0:
                            pet_shield_active = False
                            print_animated(f"{YELLOW}{active_pet['name']}'s protective stance ends.{ENDC}", delay=0.02)
                    
                    # Check for dodge
                    player_speed = user_data.get("speed", 5)
                    for effect in player_status_effects:
                        if "speed" in effect["effect"]:
                            player_speed += effect["effect"]["speed"]
                    
                    dodge_chance = DODGE_CHANCE + (player_speed * 0.01)  # Speed increases dodge chance
                    
                    # Add pet dodge bonus if active
                    if pet_dodge_bonus > 0:
                        dodge_chance += pet_dodge_bonus
                        
                    dodge_chance = min(dodge_chance, 0.5)  # Cap at 50%
                    
                    if random.random() < dodge_chance:
                        print_animated(f"{BG_CYAN}{BLACK} DODGE! {ENDC}", delay=0.02)
                        print_animated("You dodged the attack!", delay=0.02)
                    else:
                        # Apply damage to player
                        user_data["health"] -= damage_taken
                        
                        # Check for critical hit from monster
                        if random.random() < 0.1:  # 10% monster crit chance
                            damage_taken = int(damage_taken * 1.5)
                            print_animated(f"{BG_RED}{WHITE} CRITICAL HIT! {ENDC}", delay=0.02)
                        
                        print_animated(f"The {monster_name} attacks and deals {LIGHTRED}{damage_taken}{ENDC} damage!", delay=0.02)
                        
                        # Apply monster attack effects
                        if "effects" in monster:
                            for effect_name, chance in monster["effects"].items():
                                if random.random() < chance:
                                    if effect_name == "poison":
                                        player_status_effects.append({
                                            "name": "Poisoned",
                                            "duration": 3,
                                            "effect": {"poison_damage": int(user_data["max_health"] * 0.05)}
                                        })
                                        print_animated(f"{LIGHTGREEN}You have been poisoned!{ENDC}", delay=0.02)
                                    elif effect_name == "stun":
                                        stunned = True
                                        print_animated(f"{LIGHTYELLOW}You have been stunned!{ENDC}", delay=0.02)
                                    elif effect_name == "burn":
                                        player_status_effects.append({
                                            "name": "Burning",
                                            "duration": 2,
                                            "effect": {"burn_damage": int(user_data["max_health"] * 0.07)}
                                        })
                                        print_animated(f"{LIGHTRED}You are burning!{ENDC}", delay=0.02)
                    
                    # Apply damage over time effects
                    for effect in player_status_effects:
                        if "poison_damage" in effect["effect"]:
                            poison_damage = effect["effect"]["poison_damage"]
                            user_data["health"] -= poison_damage
                            print_animated(f"{LIGHTGREEN}Poison deals {poison_damage} damage!{ENDC}", delay=0.02)
                        elif "burn_damage" in effect["effect"]:
                            burn_damage = effect["effect"]["burn_damage"]
                            user_data["health"] -= burn_damage
                            print_animated(f"{LIGHTRED}Burning deals {burn_damage} damage!{ENDC}", delay=0.02)

        except Exception as e:
            print(f"{FAIL}Error during combat: {e}{ENDC}")
            continue

    # Combat conclusion
    print_animated(f"\n{BG_CYAN}{WHITE} BATTLE COMPLETED! {ENDC}", delay=0.05)
    
    if monster_health <= 0:
        print_animated(f"\n{BG_GREEN}{BLACK} VICTORY! {ENDC}", delay=0.05)
        print_animated(f"You defeated the {monster_name}!", LIGHTGREEN, delay=0.03)
        
        # Calculate experience and rewards
        exp_gain = monster["level"] * 20
        
        # Bonus exp for higher level monsters
        if monster["level"] > user_data["level"]:
            level_diff = monster["level"] - user_data["level"]
            exp_bonus = int(exp_gain * (level_diff * 0.2))  # 20% more exp per level difference
            exp_gain += exp_bonus
            print_animated(f"Bonus EXP for defeating a stronger enemy: +{exp_bonus}!", LIGHTCYAN, delay=0.02)
        
        user_data["exp"] += exp_gain
        print_animated(f"Gained {LIGHTCYAN}{exp_gain}{ENDC} experience!", delay=0.02)

        # Increment monsters killed count
        user_data["monsters_killed"] += 1
        
        # Increment specific monster type counter
        monster_type = monster.get("type", "unknown")
        if "monster_types_killed" not in user_data:
            user_data["monster_types_killed"] = {}
        user_data["monster_types_killed"][monster_type] = user_data["monster_types_killed"].get(monster_type, 0) + 1

        # Check for achievements
        check_achievements()

        # Check if monster is a boss
        if monster.get("boss", False):
            print_animated(f"{BG_MAGENTA}{WHITE} BOSS DEFEATED! {ENDC}", delay=0.05)
            print_animated(f"Congratulations! You defeated the boss {monster_name}!", LIGHTMAGENTA, delay=0.03)
            
            # Award special boss rewards
            bonus_gold = monster["level"] * 50
            user_data["gold"] += bonus_gold
            print_animated(f"Bonus reward: {LIGHTYELLOW}{bonus_gold} gold{ENDC}!", delay=0.02)
            
            # Initialize adventurer data if it doesn't exist
            if "adventurer" not in user_data:
                user_data["adventurer"] = {
                    "rank": "Novice",
                    "exp": 0,
                    "level": 1,
                    "total_quests": 0,
                    "bosses_defeated": 0,
                    "reputation": 0
                }
            
            # Increment boss counter
            user_data["adventurer"]["bosses_defeated"] += 1
            
            # Award adventurer experience (boss level * 20)
            boss_level = monster.get("level", 1)
            adv_exp = boss_level * 20
            add_adventurer_exp(adv_exp)
            
            # Display adventurer rewards
            print_animated(f"\n{CYAN}Adventurer's Guild:{ENDC} Boss defeated!", delay=0.02)
            print_animated(f"{CYAN}+{adv_exp} Adventurer EXP{ENDC}", delay=0.02)
            print_animated(f"{CYAN}Bosses Defeated:{ENDC} {user_data['adventurer']['bosses_defeated']}", delay=0.02)
            
            # Check if rank advancement is available
            check_rank_advancement()
            
            # Check for level up
            check_level_up()
        else:
            # Regular monsters also give some adventurer exp
            if "adventurer" in user_data:
                # Award small amount of adventurer experience (monster level * 2)
                monster_level = monster.get("level", 1)
                adv_exp = max(5, monster_level * 2)  # Minimum 5 exp
                add_adventurer_exp(adv_exp)
                
                # Only show message if it's at least 10 exp
                if adv_exp >= 10:
                    print_animated(f"{CYAN}+{adv_exp} Adventurer EXP{ENDC}", delay=0.02)
            
            # Check for level up
            check_level_up()

        # Handle loot
        loot(monster)
    else:
        print_animated(f"\n{BG_RED}{WHITE} DEFEAT! {ENDC}", delay=0.05)
        print_animated("You were defeated!", LIGHTRED, delay=0.03)
        user_data["health"] = 1  # Prevent death, set to 1 HP
        
        # Lose some gold on defeat
        if user_data["gold"] > 0:
            gold_loss = max(1, int(user_data["gold"] * 0.1))  # Lose 10% of gold
            user_data["gold"] -= gold_loss
            print_animated(f"You lost {LIGHTYELLOW}{gold_loss} gold{ENDC}!", delay=0.02)
        
        print_animated("Rest at an inn or use a healing potion to recover.", LIGHTCYAN, delay=0.02)

# Utility functions for the enhanced combat system
def create_health_bar(percent: float, length: int = 20) -> str:
    """Creates a visual health bar based on percentage"""
    filled_length = int(length * percent)
    empty_length = length - filled_length
    
    if percent > 0.7:
        bar_color = LIGHTGREEN
    elif percent > 0.3:
        bar_color = LIGHTYELLOW
    else:
        bar_color = LIGHTRED
    
    bar = f"{bar_color}{'█' * filled_length}{GREY}{'▒' * empty_length}{ENDC}"
    return bar

def get_attack_verb(combo: int) -> str:
    """Returns a different attack verb based on combo counter for variety"""
    if combo == 0:
        return random.choice(["strike", "hit", "attack"])
    elif combo == 1:
        return random.choice(["slash", "smash", "strike"])
    elif combo == 2:
        return random.choice(["thrash", "pummel", "devastate"])
    else:
        return random.choice(["obliterate", "annihilate", "demolish"])

def get_element_color(element: str) -> str:
    """Returns the appropriate color code for an element"""
    element_colors = {
        "Fire": LIGHTRED,
        "Water": LIGHTBLUE,
        "Earth": LIGHTGREEN,
        "Air": LIGHTCYAN,
        "Lightning": LIGHTYELLOW,
        "Ice": CYAN,
        "Light": WHITE,
        "Dark": GREY,
        "Poison": GREEN,
        "Normal": WHITE
    }
    return element_colors.get(element, WHITE)

def get_save_slots() -> List[str]:
    saves = [f for f in os.listdir() if f.startswith("save_") and f.endswith(".json")]
    return sorted(saves)

def get_save_directory() -> str:
    save_dir = os.path.join(os.getcwd(), "saves")
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def save_game(slot: int = 1, auto: bool = False) -> None:
    try:
        save_data = {
            "user_data": user_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0"
        }

        save_dir = get_save_directory()
        filename = os.path.join(save_dir, f"save_{slot}.json")

        # Create backup of existing save
        if os.path.exists(filename):
            backup_file = f"{filename}.backup"
            os.replace(filename, backup_file)

        with open(filename, "w") as f:
            json.dump(save_data, f, indent=2)
        if not auto:
            print(f"Game saved successfully in slot {slot}!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(slot: int = 1) -> bool:
    save_dir = get_save_directory()
    filename = os.path.join(save_dir, f"save_{slot}.json")

    try:
        if not os.path.exists(filename):
            print(f"No saved game found in slot {slot}.")
            return False

        with open(filename, "r", encoding='utf-8') as f:
            save_data = json.load(f)
            if save_data.get("version") != "1.0":
                print("Warning: Save file version mismatch")
            global user_data
            user_data = save_data["user_data"]
            ensure_user_data_keys(user_data)
            print(f"Game loaded successfully from slot {slot}!")
            print(f"Save timestamp: {save_data['timestamp']}")
            return True
    except Exception as e:
        print(f"Error loading game: {e}")
        # Try to load backup if it exists
        backup_file = f"{filename}.backup"
        if os.path.exists(backup_file):
            print("Attempting to load backup...")
            try:
                with open(backup_file, "r", encoding='utf-8') as f:
                    save_data = json.load(f)
                    user_data = save_data["user_data"]
                    ensure_user_data_keys(user_data)
                    print("Backup loaded successfully!")
                    return True
            except Exception:
                print("Backup load failed.")
        return False

def auto_save() -> None:
    save_game(slot=0, auto=True)

def show_save_slots() -> None:
    print_header("Save Slots")
    save_dir = get_save_directory()
    saves = [f for f in os.listdir(save_dir) if f.startswith("save_") and f.endswith(".json")]
    saves = sorted(saves)
    if not saves:
        print("No saved games found.")
        return

    for save in saves:
        try:
            save_path = os.path.join(save_dir, save)
            with open(save_path, "r") as f:
                data = json.load(f)
                slot = save.split("_")[1].split(".")[0]
                name = data['user_data'].get('name', 'Unknown')
                print(f"\nSlot {slot}:")
                print(f"Character: {name}, Level {data['user_data']['level']} {data['user_data']['class']}")
                print(f"Location: {data['user_data']['current_area']}")
                print(f"Saved: {data['timestamp']}")
        except Exception:
            continue

def delete_save(slot: int) -> None:
    filename = f"save_{slot}.json"
    try:
        os.remove(filename)
        print(f"Save in slot {slot} deleted.")
    except FileNotFoundError:
        print(f"No save found in slot {slot}.")

def _display_and_select_quests(quest_entries, has_hylit):
    """Helper function to display and select from a list of quest entries.
    
    Args:
        quest_entries: List of quest entries with availability info
        has_hylit: Boolean indicating if player has Hylit companion
        
    Returns:
        Selected quest entry or None if no selection made
    """
    if not quest_entries:
        print("No quests available.")
        return None
        
    available_quests = []
    unavailable_quests = []
    
    # Separate available and unavailable quests
    for entry in quest_entries:
        if entry["prerequisite_met"] and entry["level_met"] and entry["location_available"]:
            available_quests.append(entry)
        else:
            unavailable_quests.append(entry)
            
    # Display available quests first
    if available_quests:
        print(f"\n{GREEN}Available Quests:{ENDC}")
        for i, entry in enumerate(available_quests, 1):
            quest = entry["quest"]
            
            # Enhanced display based on quest type
            if quest.get("story", False):
                if "story_arc" in quest:
                    print(f"\n{i}. {CYAN}{quest['name']}{ENDC} [{quest['story_arc']}]")
                else:
                    print(f"\n{i}. {YELLOW}{quest['name']}{ENDC} [Chapter {quest.get('chapter', '?')}]")
            else:
                print(f"\n{i}. {quest['name']}")
                
            # Hylit narration for immersion
            if has_hylit:
                print_animated(f"Hylit whispers: '{quest['description']}'", CYAN)
            else:
                print(f"   {quest['description']}")
                
            # Quest objective
            target_type, target_count = next(iter(quest["target"].items()))
            print(f"   Objective: {target_type.capitalize()} x {target_count}")
            
            # Rewards with color coding
            print(f"   Rewards: {YELLOW}{quest['reward']['gold']}{ENDC} gold, {GREEN}{quest['reward']['exp']}{ENDC} exp")
            if "item" in quest["reward"]:
                print(f"           + {MAGENTA}{quest['reward']['item']}{ENDC}")
                
            # Special requirements
            if "requirements" in quest:
                req = quest["requirements"]
                if "season" in req:
                    season_match = req["season"] == user_data.get("current_season", "")
                    status = f"{GREEN}✓{ENDC}" if season_match else f"{RED}✗{ENDC}"
                    print(f"   Required Season: {req['season']} {status}")
                if "weather" in req:
                    weather_match = req["weather"] == user_data.get("current_weather", "")
                    status = f"{GREEN}✓{ENDC}" if weather_match else f"{RED}✗{ENDC}"
                    print(f"   Required Weather: {req['weather']} {status}")
                if "profession" in req:
                    prof_match = req["profession"] == user_data.get("profession", "")
                    status = f"{GREEN}✓{ENDC}" if prof_match else f"{RED}✗{ENDC}"
                    print(f"   Required Profession: {req['profession']} {status}")
                    
    # Display unavailable quests with reason
    if unavailable_quests:
        print(f"\n{YELLOW}Unavailable Quests:{ENDC}")
        for i, entry in enumerate(unavailable_quests, len(available_quests) + 1):
            quest = entry["quest"]
            reasons = []
            
            if not entry["prerequisite_met"]:
                reasons.append(f"{RED}Prerequisite not met{ENDC}")
            if not entry["level_met"]:
                reasons.append(f"{RED}Requires level {quest.get('level_required', '?')}{ENDC}")
            if not entry["location_available"]:
                reasons.append(f"{YELLOW}Must travel to: {', '.join(quest.get('travel_locations', []))}{ENDC}")
                
            print(f"\n{i}. {LIGHTGRAY}{quest['name']}{ENDC} ({', '.join(reasons)})")
            print(f"   {LIGHTGRAY}{quest['description']}{ENDC}")
    
    # Prompt for quest selection if any available
    if available_quests:
        choice = input("\nSelect a quest to accept (or 0 to go back): ").strip()
        try:
            choice_index = int(choice)
            if choice_index == 0:
                return None
                
            if 1 <= choice_index <= len(available_quests):
                return available_quests[choice_index - 1]
            else:
                print("Invalid choice.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
    else:
        input("\nPress Enter to continue...")
        return None

def show_quests() -> None:
    print_header("Quest Journal")

    # Check if player has Hylit companion for narration
    has_hylit = "Hylit" in user_data["pets"]
    
    # Initialize quest categories
    quest_categories = {
        "main_story": [],      # Main storyline quests
        "story_arcs": {},      # Secondary story arcs (Weather Mysteries, Void Walker, etc.)
        "location": [],        # Location-specific quests
        "profession": [],      # Profession-specific quests
        "seasonal": [],        # Season-specific quests
        "weather": [],         # Weather-specific quests
        "daily": [],           # Daily quests that reset
        "general": []          # General side quests
    }
    
    # Categorize available quests
    for quest in QUESTS:
        # Skip completed quests
        if quest["id"] in user_data["completed_quests"]:
            continue
            
        # Skip active quests for available quest display
        if quest in user_data["active_quests"]:
            continue
            
        # Check if quest is available based on prerequisites
        prerequisite_met = True
        if "prerequisite" in quest and quest["prerequisite"] not in user_data["completed_quests"]:
            prerequisite_met = False
            
        # Check level requirements
        level_met = True
        if "level_required" in quest and user_data["level"] < quest["level_required"]:
            level_met = False
            
        # Create a quest entry with availability info
        quest_entry = {
            "quest": quest,
            "prerequisite_met": prerequisite_met,
            "level_met": level_met,
            "location_available": "travel_locations" not in quest or user_data["location"] in quest["travel_locations"]
        }
        
        # Categorize based on quest attributes
        if quest.get("story", False) and not quest.get("story_arc", None):
            quest_categories["main_story"].append(quest_entry)
        elif "story_arc" in quest:
            arc_name = quest["story_arc"]
            if arc_name not in quest_categories["story_arcs"]:
                quest_categories["story_arcs"][arc_name] = []
            quest_categories["story_arcs"][arc_name].append(quest_entry)
        elif "requirements" in quest:
            if "profession" in quest["requirements"]:
                quest_categories["profession"].append(quest_entry)
            elif "season" in quest["requirements"]:
                quest_categories["seasonal"].append(quest_entry)
            elif "weather" in quest["requirements"]:
                quest_categories["weather"].append(quest_entry)
            elif "daily" in quest["requirements"] and quest["requirements"]["daily"]:
                quest_categories["daily"].append(quest_entry)
            else:
                quest_categories["general"].append(quest_entry)
        elif "travel_locations" in quest:
            quest_categories["location"].append(quest_entry)
        else:
            quest_categories["general"].append(quest_entry)
    
    # Define quest menu options
    quest_menu_options = {
        "1": "View Main Story Quests",
        "2": "View Story Arc Quests",
        "3": "View Available Side Quests",
        "4": "View Active Quests",
        "5": "View Completed Quests",
        "0": "Back"
    }
    
    while True:
        print("\nQuest Menu:")
        for key, option in quest_menu_options.items():
            print(f"{key}. {option}")
            
        choice = input("\nSelect an option: ").strip()
        
        if choice == "0":
            return
            
        elif choice == "1":  # Main story quests
            print_header("Main Story Quests")
            
            if not quest_categories["main_story"]:
                print("No main story quests available at this time.")
                input("\nPress Enter to continue...")
                continue
                
            # Sort main story quests by chapter
            quest_categories["main_story"].sort(key=lambda x: x["quest"].get("chapter", 0))
            
            # Display main story quests
            quest_selected = _display_and_select_quests(quest_categories["main_story"], has_hylit)
            if quest_selected:
                # Accept the quest
                user_data["active_quests"].append(quest_selected["quest"])
                print(f"\n{GREEN}Quest '{quest_selected['quest']['name']}' added to your journal!{ENDC}")
                
                # Special handling for storyline quests - show immersive message
                chapter = quest_selected["quest"].get("chapter", 0)
                print_animated(f"\nChapter {chapter} begins...", CYAN)
                if has_hylit:
                    print_animated("Hylit: 'This is a pivotal moment in your journey. The path ahead may be challenging, but I believe in you!'", CYAN)
                
                input("\nPress Enter to continue...")
                
        elif choice == "2":  # Story arc quests
            if not quest_categories["story_arcs"]:
                print("No story arc quests available at this time.")
                input("\nPress Enter to continue...")
                continue
                
            # Create story arc menu
            print_header("Story Arcs")
            story_arcs = list(quest_categories["story_arcs"].keys())
            
            for i, arc in enumerate(story_arcs, 1):
                available_quests = sum(1 for q in quest_categories["story_arcs"][arc] 
                                     if q["prerequisite_met"] and q["level_met"] and q["location_available"])
                total_quests = len(quest_categories["story_arcs"][arc])
                print(f"{i}. {arc} ({available_quests}/{total_quests} available)")
                
            arc_choice = input("\nSelect a story arc (or 0 to go back): ").strip()
            
            try:
                arc_index = int(arc_choice)
                if arc_index == 0:
                    continue
                    
                if 1 <= arc_index <= len(story_arcs):
                    selected_arc = story_arcs[arc_index-1]
                    print_header(f"{selected_arc} Quests")
                    
                    # Sort by quest sequence (prerequisite chain)
                    arc_quests = quest_categories["story_arcs"][selected_arc]
                    quest_selected = _display_and_select_quests(arc_quests, has_hylit)
                    
                    if quest_selected:
                        # Accept the quest
                        user_data["active_quests"].append(quest_selected["quest"])
                        print(f"\n{GREEN}Quest '{quest_selected['quest']['name']}' added to your journal!{ENDC}")
                        
                        # Special immersive message for story arcs
                        if has_hylit:
                            if selected_arc == "Weather Mysteries":
                                print_animated("Hylit: 'The weather holds many secrets. This quest may reveal forgotten knowledge about the elements themselves.'", CYAN)
                            elif selected_arc == "Void Walker":
                                print_animated("Hylit: 'These dimensional disturbances are concerning. Be cautious as you investigate further.'", CYAN)
                        
                        input("\nPress Enter to continue...")
            except ValueError:
                print("Invalid choice. Please enter a number.")
                
        elif choice == "3":  # Side quests
            print_header("Available Side Quests")
            
            # Combine all side quest categories
            all_side_quests = (
                quest_categories["location"] + 
                quest_categories["profession"] + 
                quest_categories["seasonal"] + 
                quest_categories["weather"] + 
                quest_categories["daily"] + 
                quest_categories["general"]
            )
            
            if not all_side_quests:
                print("No side quests available at this time.")
                input("\nPress Enter to continue...")
                continue
                
            # Filter options for side quests
            filter_options = {
                "1": "All Side Quests",
                "2": "Location Quests",
                "3": "Profession Quests",
                "4": "Seasonal Quests",
                "5": "Weather Quests",
                "6": "Daily Quests",
                "0": "Back"
            }
            
            print("\nFilter Options:")
            for key, option in filter_options.items():
                print(f"{key}. {option}")
                
            filter_choice = input("\nSelect a filter: ").strip()
            
            if filter_choice == "0":
                continue
                
            filtered_quests = []
            if filter_choice == "1":
                filtered_quests = all_side_quests
            elif filter_choice == "2":
                filtered_quests = quest_categories["location"]
            elif filter_choice == "3":
                filtered_quests = quest_categories["profession"]
            elif filter_choice == "4":
                filtered_quests = quest_categories["seasonal"]
            elif filter_choice == "5":
                filtered_quests = quest_categories["weather"]
            elif filter_choice == "6":
                filtered_quests = quest_categories["daily"]
            else:
                print("Invalid choice.")
                continue
                
            if not filtered_quests:
                print("No quests found with this filter.")
                input("\nPress Enter to continue...")
                continue
                
            # Sort side quests by level required
            filtered_quests.sort(key=lambda x: x["quest"].get("level_required", 0))
            
            quest_selected = _display_and_select_quests(filtered_quests, has_hylit)
            if quest_selected:
                # Accept the quest
                user_data["active_quests"].append(quest_selected["quest"])
                print(f"\n{GREEN}Quest '{quest_selected['quest']['name']}' added to your journal!{ENDC}")
                input("\nPress Enter to continue...")
                
        elif choice == "4":  # Active quests
            print_header("Active Quests")
            
            if not user_data["active_quests"]:
                print("You have no active quests.")
                input("\nPress Enter to continue...")
                continue
                
            # Display active quests with detailed progress
            active_quests = user_data["active_quests"]
            for i, quest in enumerate(active_quests, 1):
                # Determine quest type/category for display
                quest_type = "Side Quest"
                if quest.get("story", False):
                    if "story_arc" in quest:
                        quest_type = f"{quest['story_arc']} Quest"
                    else:
                        quest_type = f"Chapter {quest.get('chapter', '?')} Main Quest"
                        
                # Format quest header with color based on type
                if "Chapter" in quest_type:
                    print(f"\n{i}. {YELLOW}{quest['name']}{ENDC} ({quest_type})")
                elif "Arc" in quest_type:
                    print(f"\n{i}. {CYAN}{quest['name']}{ENDC} ({quest_type})")
                else:
                    print(f"\n{i}. {GREEN}{quest['name']}{ENDC} ({quest_type})")
                    
                print(f"   Description: {quest['description']}")
                
                # Show quest objective with progress bar
                target = next(iter(quest["target"].items()))
                target_type, target_count = target
                target_progress = user_data.get("quest_progress", {}).get(quest["name"], {}).get(target_type, 0)
                
                # Calculate progress percentage and create visual progress bar
                progress_percent = min(100, int((target_progress / target_count) * 100))
                progress_bar = create_progress_bar(progress_percent/100)
                
                print(f"   Objective: {target_type.capitalize()} x {target_count}")
                print(f"   Progress: {progress_bar} {target_progress}/{target_count} ({progress_percent}%)")
                
                # Show rewards
                print("   Rewards:")
                print(f"     - {quest['reward']['gold']} gold")
                print(f"     - {quest['reward']['exp']} experience")
                if "item" in quest["reward"]:
                    print(f"     - Item: {quest['reward']['item']}")
                    
                # Location requirement, if any
                if "travel_locations" in quest:
                    if user_data["location"] in quest["travel_locations"]:
                        print(f"   {GREEN}You are in the right location to progress this quest.{ENDC}")
                    else:
                        print(f"   {YELLOW}Travel to: {', '.join(quest['travel_locations'])}{ENDC}")
                        
            # Option to abandon a quest
            print("\nOptions:")
            print("1. Return to quest menu")
            print("2. Abandon a quest")
            
            active_choice = input("\nSelect an option: ").strip()
            
            if active_choice == "2":
                abandon_index = input("Enter the number of the quest to abandon (or 0 to cancel): ").strip()
                try:
                    abandon_index = int(abandon_index)
                    if abandon_index == 0:
                        continue
                        
                    if 1 <= abandon_index <= len(active_quests):
                        quest_to_abandon = active_quests[abandon_index-1]
                        
                        # Check if it's a main story quest
                        if quest_to_abandon.get("story", False) and not quest_to_abandon.get("story_arc", None):
                            confirm = input(f"{RED}Warning: This is a main story quest. Are you sure you want to abandon it? (y/n): {ENDC}").strip().lower()
                            if confirm != 'y':
                                continue
                                
                        # Abandon the quest
                        user_data["active_quests"].remove(quest_to_abandon)
                        print(f"{YELLOW}Quest '{quest_to_abandon['name']}' abandoned.{ENDC}")
                except ValueError:
                    print("Invalid choice. Please enter a number.")
            
        elif choice == "5":  # Completed quests
            print_header("Completed Quests")
            
            # Get all completed quests
            completed_quest_ids = user_data["completed_quests"]
            if not completed_quest_ids:
                print("You haven't completed any quests yet.")
                input("\nPress Enter to continue...")
                continue
                
            # Find quest details for each completed ID
            completed_quests = []
            for quest in QUESTS:
                if quest["id"] in completed_quest_ids:
                    completed_quests.append(quest)
                    
            # Group by chapter and story arc
            completed_by_chapter = {}
            completed_by_arc = {}
            completed_side = []
            
            for quest in completed_quests:
                if quest.get("story", False):
                    if "story_arc" in quest:
                        arc = quest["story_arc"]
                        if arc not in completed_by_arc:
                            completed_by_arc[arc] = []
                        completed_by_arc[arc].append(quest)
                    else:
                        chapter = quest.get("chapter", 0)
                        if chapter not in completed_by_chapter:
                            completed_by_chapter[chapter] = []
                        completed_by_chapter[chapter].append(quest)
                else:
                    completed_side.append(quest)
                    
            # Display completed main story quests by chapter
            if completed_by_chapter:
                print("\nCompleted Main Story Quests:")
                for chapter in sorted(completed_by_chapter.keys()):
                    print(f"\nChapter {chapter}:")
                    for quest in completed_by_chapter[chapter]:
                        print(f"  - {YELLOW}{quest['name']}{ENDC}")
                        
            # Display completed story arc quests
            if completed_by_arc:
                print("\nCompleted Story Arc Quests:")
                for arc in sorted(completed_by_arc.keys()):
                    print(f"\n{arc}:")
                    for quest in completed_by_arc[arc]:
                        print(f"  - {CYAN}{quest['name']}{ENDC}")
                        
            # Display completed side quests
            if completed_side:
                print("\nCompleted Side Quests:")
                for quest in completed_side:
                    print(f"  - {GREEN}{quest['name']}{ENDC}")
                    
            # Show completion statistics
            total_completed = len(completed_quest_ids)
            total_available = len(QUESTS)
            completion_percent = int((total_completed / total_available) * 100)
            
            print("\nQuest Completion Stats:")
            print(f"Total Quests Completed: {total_completed}/{total_available} ({completion_percent}%)")
            
            # Show milestones and achievements based on completion
            if completion_percent >= 10:
                print(f"{GREEN}Achievement: Quest Beginner{ENDC}")
            if completion_percent >= 25:
                print(f"{GREEN}Achievement: Quest Enthusiast{ENDC}")
            if completion_percent >= 50:
                print(f"{GREEN}Achievement: Quest Master{ENDC}")
            if completion_percent >= 75:
                print(f"{GREEN}Achievement: Quest Legend{ENDC}")
            if completion_percent == 100:
                print(f"{CYAN}Achievement: Completionist{ENDC}")
                
            input("\nPress Enter to continue...")
            
        else:
            print("Invalid choice. Please try again.")


# Ability descriptions for pets
ABILITY_DESCRIPTIONS = {
    # General abilities
    "Quick Attack": "Pet attacks first in combat, dealing small damage (10% of your attack)",
    "Protective Stance": "Pet has a 20% chance to block incoming attacks, reducing damage by 30%",
    "Find Treasure": "Pet has a 15% chance to find extra loot after battles",
    "Scouting": "Pet helps you find materials more efficiently (+10% gathering yield)",
    
    # Elemental abilities
    "Flame Burst": "Pet deals Fire elemental damage to enemies (15% of your attack)",
    "Healing Mist": "Pet has a 20% chance to heal you for 10% of your max health each turn",
    "Stone Shield": "Pet creates a shield that reduces damage by 15% for 3 turns",
    "Swift Movement": "Pet increases your dodge chance by 10% during combat",
    "Shock Strike": "Pet deals Lightning damage with a 15% chance to stun the enemy for 1 turn",
    "Energy Pulse": "Pet releases a burst of energy dealing 12% of your attack as neutral damage",
    
    # Special abilities
    "Scavenge": "Pet may find bonus materials when exploring",
    "Weather Sense": "Pet predicts weather changes, giving warning before severe weather",
    "Fierce Loyalty": "When your health drops below 20%, pet deals 50% more damage",
    "Intimidate": "Pet has a 10% chance to frighten weaker enemies, making them flee"
}

# Function to handle loot drops
def loot(monster: Dict) -> None:
    """
    Enhanced loot system with rarity levels, random drops, and treasure chests
    Includes pet integration for bonus loot
    """
    global user_data
    
    print_animated(f"\n{BG_YELLOW}{BLACK} LOOT DISCOVERED! {ENDC}", delay=0.05)
    
    # Basic monster drops
    base_drops = monster.get("drops", [])
    
    # Calculate additional random drops based on monster level
    monster_level = monster.get("level", 1)
    is_boss = monster.get("boss", False)
    
    # Check for active pet with Find Treasure ability
    active_pet = get_active_pet()
    has_treasure_finder = False
    pet_treasure_bonus = 0
    
    if active_pet:
        pet_name = active_pet["name"]
        pet_abilities = []
        
        # Get the pet's abilities
        if "pet_stats" in user_data and pet_name in user_data["pet_stats"]:
            pet_abilities = user_data["pet_stats"][pet_name].get("abilities", [])
            
            # Check if pet has Find Treasure ability
            if "Find Treasure" in pet_abilities:
                has_treasure_finder = True
                pet_level = user_data["pet_stats"][pet_name].get("level", 1)
                pet_loyalty = user_data["pet_stats"][pet_name].get("loyalty", 50)
                
                # Higher level and loyalty increase bonus chance
                pet_treasure_bonus = 0.15  # Base 15% chance
                pet_treasure_bonus += min(0.05, pet_level * 0.01)  # +1% per level up to 5%
                
                if pet_loyalty >= 70:
                    pet_treasure_bonus += 0.05  # +5% for high loyalty
    
    # Determine drop quantities and chances
    drop_count = random.randint(1, 3)  # Base drop count
    
    # Bosses give more loot
    if is_boss:
        drop_count += random.randint(2, 4)
    
    # Chance to find a chest
    chest_chance = 0.1 + (monster_level * 0.01)  # 10% base + 1% per monster level
    if is_boss:
        chest_chance += 0.3  # Bosses have higher chest chance
        
    # Apply pet bonuses if available
    if has_treasure_finder and active_pet and "name" in active_pet:
        extra_items = 1  # Always get at least one extra item
        drop_count += extra_items
        chest_chance += pet_treasure_bonus  # Increased chest chance
        
        # Pet found extra treasure notification
        pet_name = active_pet.get("name", "Your pet")
        print_animated(f"{CYAN}{pet_name} found {extra_items} extra treasure(s)!{ENDC}", delay=0.02)
        print_animated(f"{YELLOW}Chest discovery chance increased by {int(pet_treasure_bonus*100)}%{ENDC}", delay=0.02)
    
    # Prepare loot table
    all_drops = []
    
    # Add base drops from monster definition
    for item in base_drops:
        all_drops.append({
            "name": item,
            "type": "base",
            "rarity": "Common" if item != "Gold Coin" else "Currency"
        })
    
    # Check for chest
    found_chest = random.random() < chest_chance
    if found_chest:
        chest_tier = "Common"
        if is_boss:
            # Boss chests are better
            if monster_level > 20:
                chest_tier = random.choice(["Epic", "Legendary"])
            elif monster_level > 10:
                chest_tier = random.choice(["Rare", "Epic"])
            else:
                chest_tier = random.choice(["Common", "Uncommon", "Rare"])
        else:
            # Regular monster chests
            rarity_roll = random.random()
            if rarity_roll < 0.1 * (monster_level / 20):  # Higher level monsters have better chest chance
                chest_tier = "Legendary"
            elif rarity_roll < 0.2 * (monster_level / 15):
                chest_tier = "Epic"
            elif rarity_roll < 0.4 * (monster_level / 10):
                chest_tier = "Rare"
            elif rarity_roll < 0.6:
                chest_tier = "Uncommon"
            
        all_drops.append({
            "name": f"{chest_tier} Chest",
            "type": "chest",
            "rarity": chest_tier
        })
    
    # Add random gold based on monster level
    gold_amount = random.randint(5, 15) * max(1, monster_level // 2)
    if is_boss:
        gold_amount *= 3  # Triple gold for bosses
    
    all_drops.append({
        "name": f"{gold_amount} Gold",
        "type": "gold",
        "rarity": "Currency",
        "amount": gold_amount
    })
    
    # Add random material drops based on area and monster type
    if "type" in monster:
        monster_type = monster["type"]
        material_chance = 0.3 + (monster_level * 0.02)  # 30% base + 2% per level
        
        if random.random() < material_chance:
            if monster_type == "undead":
                material = random.choice(["Bone Dust", "Spectral Essence", "Grave Soil"])
            elif monster_type == "beast":
                material = random.choice(["Beast Hide", "Sharp Claw", "Monster Tooth"])
            elif monster_type == "elemental":
                material = random.choice(["Elemental Core", "Pure Essence", "Crystallized Magic"])
            elif monster_type == "dragon":
                material = random.choice(["Dragon Scale", "Dragon Tooth", "Dragon Blood"])
            elif monster_type == "demon":
                material = random.choice(["Demon Horn", "Infernal Ash", "Corrupted Essence"])
            else:
                material = random.choice(["Strange Dust", "Magical Residue", "Creature Part"])
                
            rarity = "Common"
            if random.random() < 0.2:
                rarity = "Uncommon"
            if random.random() < 0.1:
                rarity = "Rare"
                
            all_drops.append({
                "name": material,
                "type": "material",
                "rarity": rarity
            })
    
    # Add random equipment drop for higher level monsters or bosses
    equipment_chance = 0.05 + (monster_level * 0.01)  # 5% base + 1% per level
    if is_boss:
        equipment_chance = 0.5 + (monster_level * 0.02)  # 50% base + 2% per level for bosses
        
    if random.random() < equipment_chance:
        equip_type = random.choice(["weapon", "armor", "accessory"])
        
        if equip_type == "weapon":
            weapons = ["Sword", "Axe", "Dagger", "Staff", "Bow", "Wand", "Hammer", "Spear"]
            equip_name = random.choice(weapons)
        elif equip_type == "armor":
            armors = ["Helmet", "Chestplate", "Leggings", "Boots", "Gauntlets", "Shield"]
            equip_name = random.choice(armors)
        else:  # accessory
            accessories = ["Ring", "Amulet", "Charm", "Bracelet", "Belt", "Earring"]
            equip_name = random.choice(accessories)
        
        # Determine rarity
        rarity_roll = random.random()
        if rarity_roll < 0.05 * (monster_level / 20):  # Higher level = better chance
            rarity = "Legendary"
            prefix = random.choice(["Ancient", "Mythical", "Godly", "Supreme", "Ultimate"])
        elif rarity_roll < 0.15 * (monster_level / 15):
            rarity = "Epic"
            prefix = random.choice(["Magnificent", "Heroic", "Superior", "Masterful", "Elite"])
        elif rarity_roll < 0.3 * (monster_level / 10):
            rarity = "Rare"
            prefix = random.choice(["Exceptional", "Valuable", "Quality", "Refined", "Pristine"])
        elif rarity_roll < 0.5:
            rarity = "Uncommon"
            prefix = random.choice(["Fine", "Strong", "Sturdy", "Keen", "Reinforced"])
        else:
            rarity = "Common"
            prefix = random.choice(["Basic", "Simple", "Standard", "Plain", "Ordinary"])
        
        # Add effects based on rarity
        effect_value = 0
        if rarity == "Legendary":
            effect_value = 15 + monster_level // 2
        elif rarity == "Epic":
            effect_value = 10 + monster_level // 3
        elif rarity == "Rare":
            effect_value = 7 + monster_level // 4
        elif rarity == "Uncommon":
            effect_value = 5 + monster_level // 5
        else:
            effect_value = 3 + monster_level // 7
        
        # Sometimes add a random element
        has_element = random.random() < 0.3
        element = None
        if has_element:
            element = random.choice(["Fire", "Water", "Earth", "Air", "Lightning", "Ice", "Light", "Dark"])
            
        # Build the full item name
        if element:
            full_name = f"{prefix} {element} {equip_name}"
        else:
            full_name = f"{prefix} {equip_name}"
            
        all_drops.append({
            "name": full_name,
            "type": "equipment",
            "rarity": rarity,
            "equip_type": equip_type,
            "effect": effect_value,
            "element": element
        })
    
    # Display all drops with colors based on rarity
    print_animated("\nLoot found:", delay=0.02)
    
    # Group items by type for better display
    grouped_drops = {}
    for i, drop in enumerate(all_drops):
        drop_type = drop["type"]
        if drop_type not in grouped_drops:
            grouped_drops[drop_type] = []
        # Add the index so we can refer back to the original list
        drop["index"] = i
        grouped_drops[drop_type].append(drop)
    
    # Display loot by category with colors
    current_idx = 1
    display_drops = []
    
    # 1. Equipment (most exciting)
    if "equipment" in grouped_drops:
        print_animated(f"\n{BOLD}Equipment:{ENDC}", delay=0.01)
        for item in grouped_drops["equipment"]:
            rarity_color = get_rarity_color(item["rarity"])
            print_animated(f"{current_idx}. {rarity_color}{item['name']}{ENDC} ({item['rarity']} {item['equip_type'].capitalize()})", delay=0.02)
            item["display_index"] = current_idx
            display_drops.append(item)
            current_idx += 1
    
    # 2. Chests
    if "chest" in grouped_drops:
        print_animated(f"\n{BOLD}Treasures:{ENDC}", delay=0.01)
        for item in grouped_drops["chest"]:
            rarity_color = get_rarity_color(item["rarity"])
            print_animated(f"{current_idx}. {rarity_color}{item['name']}{ENDC}", delay=0.02)
            item["display_index"] = current_idx
            display_drops.append(item)
            current_idx += 1
    
    # 3. Materials
    if "material" in grouped_drops:
        print_animated(f"\n{BOLD}Materials:{ENDC}", delay=0.01)
        for item in grouped_drops["material"]:
            rarity_color = get_rarity_color(item["rarity"])
            print_animated(f"{current_idx}. {rarity_color}{item['name']}{ENDC} ({item['rarity']})", delay=0.02)
            item["display_index"] = current_idx
            display_drops.append(item)
            current_idx += 1
            
    # 4. Basic drops
    if "base" in grouped_drops:
        print_animated(f"\n{BOLD}Other Items:{ENDC}", delay=0.01)
        for item in grouped_drops["base"]:
            rarity_color = get_rarity_color(item["rarity"])
            print_animated(f"{current_idx}. {rarity_color}{item['name']}{ENDC}", delay=0.02)
            item["display_index"] = current_idx
            display_drops.append(item)
            current_idx += 1
    
    # 5. Gold (always shown)
    if "gold" in grouped_drops:
        print_animated(f"\n{BOLD}Currency:{ENDC}", delay=0.01)
        for item in grouped_drops["gold"]:
            print_animated(f"{current_idx}. {LIGHTYELLOW}{item['name']}{ENDC}", delay=0.02)
            item["display_index"] = current_idx
            display_drops.append(item)
            current_idx += 1
            
    # 6. Special pet-found items if pet has Find Treasure ability
    if has_treasure_finder and active_pet and "name" in active_pet and "pet_stats" in user_data and active_pet["name"] in user_data["pet_stats"]:
        # Chance for bonus rare materials scales with pet level and loyalty
        pet_level = user_data["pet_stats"][active_pet["name"]].get("level", 1)
        pet_loyalty = user_data["pet_stats"][active_pet["name"]].get("loyalty", 50)
        rare_chance = 0.15 + (pet_level * 0.02) + (pet_loyalty * 0.001)  # 15% base + bonuses
        
        if random.random() < rare_chance:
            # Select a rare bonus material
            rare_bonus_materials = [
                "Fire Essence", "Water Essence", "Earth Essence", "Air Essence", 
                "Lightning Essence", "Arcane Dust", "Mythril", "Stardust",
                "Dragon Scale", "Phoenix Feather", "Enchanted Gem"
            ]
            bonus_material = random.choice(rare_bonus_materials)
            
            # Create the item
            pet_item = {
                "name": bonus_material,
                "type": "material",
                "quantity": 1,
                "rarity": "Rare",
                "pet_bonus": True  # Mark as pet-found
            }
            
            # Add to display drops
            print_animated(f"\n{BOLD}{MAGENTA}Pet Discovery:{ENDC}", delay=0.01)
            print_animated(f"{current_idx}. {CYAN}[Pet Find] {get_rarity_color('Rare')}{bonus_material}{ENDC} ✨", delay=0.03)
            pet_item["display_index"] = current_idx
            display_drops.append(pet_item)
            current_idx += 1
    
    # Handle loot selection with improved UI
    print_animated(f"\n{BOLD}You can select one item to loot.{ENDC}", delay=0.02)
    print_animated("Type 'all' to take everything or press Enter to skip.", delay=0.02)
    
    while True:
        try:
            choice = input(f"{CYAN}Choose loot (1-{len(display_drops)}, 'all', or press Enter): {ENDC}").strip().lower()
            
            # Take all loot
            if choice == "all":
                print_animated(f"{BG_GREEN}{BLACK} LOOTING ALL ITEMS {ENDC}", delay=0.02)
                # Process each item
                for item in display_drops:
                    process_loot_item(item)
                break
                
            # Skip looting
            elif choice == "":
                print_animated(f"{YELLOW}No loot taken.{ENDC}", delay=0.02)
                break
                
            # Take specific item
            else:
                choice_int = int(choice)
                if 1 <= choice_int <= len(display_drops):
                    selected_item = next((item for item in display_drops if item["display_index"] == choice_int), None)
                    if selected_item:
                        # Process the selected item
                        process_loot_item(selected_item)
                        break
                else:
                    print(f"{YELLOW}Invalid choice, please try again.{ENDC}")
                    
        except ValueError:
            print(f"{YELLOW}Invalid input, please enter a number, 'all', or press Enter to skip.{ENDC}")

def process_loot_item(item):
    """Process a single loot item based on its type"""
    global user_data
    
    item_type = item["type"]
    item_name = item["name"]
    
    # Check if item was found by pet
    pet_bonus = item.get("pet_bonus", False)
    pet_prefix = f"{CYAN}[Pet Find] {ENDC}" if pet_bonus else ""
    
    if item_type == "gold":
        gold_amount = item["amount"]
        user_data["gold"] += gold_amount
        print_animated(f"{pet_prefix}Gained {LIGHTYELLOW}{gold_amount} gold{ENDC}!", delay=0.02)
        
    elif item_type == "chest":
        print_animated(f"{pet_prefix}{CYAN}You've found a {get_rarity_color(item['rarity'])}{item_name}{ENDC}!", delay=0.02)
        # Directly open the chest
        open_chest(item["rarity"])
        
    elif item_type == "equipment":
        # Add equipment to inventory with properties
        equip_item = {
            "name": item["name"],
            "type": item["equip_type"],
            "rarity": item["rarity"],
            "effect": item["effect"]
        }
        if "element" in item and item["element"]:
            equip_item["element"] = item["element"]
            
        # Check if inventory has equipment section
        if "equipment" not in user_data:
            user_data["equipment"] = []
            
        user_data["equipment"].append(equip_item)
        print_animated(f"{pet_prefix}Added {get_rarity_color(item['rarity'])}{item_name}{ENDC} to your equipment!", delay=0.02)
        
    else:  # base items, materials, etc.
        user_data["inventory"].append(item_name)
        print_animated(f"{pet_prefix}Added {get_rarity_color(item.get('rarity', 'Common'))}{item_name}{ENDC} to inventory!", delay=0.02)

def get_rarity_color(rarity):
    """Returns the appropriate color code for an item rarity"""
    rarity_colors = {
        "Common": WHITE,
        "Uncommon": LIGHTGREEN,
        "Rare": LIGHTBLUE,
        "Epic": LIGHTMAGENTA,
        "Legendary": LIGHTYELLOW,
        "Currency": LIGHTYELLOW
    }
    return rarity_colors.get(rarity, WHITE)

# Function to enter a dungeon
def enter_dungeon(dungeon_name: str) -> None:
    try:
        dungeon = next((d for d in dungeons if d["name"].lower() == dungeon_name.lower()), None)
        if not dungeon:
            print(f"{FAIL}Dungeon '{dungeon_name}' not found!{ENDC}")
            return

        print_header(f"Entering {dungeon['name']}...")
        print_colored("Prepare yourself for tough battles and great loot!", CYAN)

        # Check if dungeon has any boss monsters
        boss_monsters = []
        for monster_name in dungeon["monsters"]:
            monster = next((m for m in monsters if m["name"].lower() == monster_name.lower()), None)
            if monster and monster.get("boss", False):
                boss_monsters.append(monster)

        # If no boss monsters, limit number of monsters fought to random 10-15
        max_monsters = len(dungeon["monsters"])
        if not boss_monsters:
            max_monsters = random.randint(10, 15)
            max_monsters = min(max_monsters, len(dungeon["monsters"]))

        monsters_fought = 0
        all_monsters_defeated = True
        for monster_name in dungeon["monsters"]:
            if monsters_fought >= max_monsters:
                print_colored(f"Reached limit of {max_monsters} monsters for this dungeon (no boss present).", YELLOW)
                break
            try:
                monster = next(m for m in monsters if m["name"].lower() == monster_name.lower())
                if user_data["health"] <= 0:
                    print_colored("You were defeated! Dungeon run failed.", FAIL)
                    all_monsters_defeated = False
                    return
                # If monster is a boss, print special styled name
                if monster.get("boss", False):
                    boss_name = f"⋆༺ 𓆩{monster['name'].upper()}𓆪 ༻ ⋆"
                    print_colored(boss_name, FAIL)
                else:
                    print_colored(f"Encountered: {monster['name']}", CYAN)
                fight(monster)
                if user_data["health"] <= 0:
                    all_monsters_defeated = False
                    break
                monsters_fought += 1
            except StopIteration:
                print_colored(f"Warning: Monster '{monster_name}' not found in database", WARNING)
                continue

        if user_data["health"] > 0 and all_monsters_defeated:
            print_colored(f"You have completed the {dungeon['name']}!", OKGREEN)

            # Mark dungeon as completed
            if dungeon['name'] not in user_data.get("dungeons_completed", []):
                user_data.setdefault("dungeons_completed", []).append(dungeon['name'])
                print_colored(f"Dungeon {dungeon['name']} has been marked as completed!", OKGREEN)

                # Additional reward for first completion
                reward_gold = 500
                reward_exp = 1000
                user_data["gold"] += reward_gold
                user_data["exp"] += reward_exp
                print_colored(f"You received {reward_gold} gold and {reward_exp} experience as a completion reward!", MAGENTA)

            # Get loot regardless of completion status
            loot_item = random.choice(dungeon["loot"])
            print_colored(f"At the end of the dungeon, you found: {loot_item}", MAGENTA)
            user_data["inventory"].append(loot_item)
    except Exception as e:
        print_colored(f"Error in dungeon: {e}", FAIL)

# Shop functions
def visit_shop() -> None:
    print_header("Shop")
    print("Welcome to the shop! What would you like to buy?")
    for idx, item in enumerate(shop_items):
        print(f"{idx + 1}. {item['name']} - {item['price']} gold")
    print(f"{len(shop_items) + 1}. Exit shop")

    choice = int(input("Choose an item to buy (1-{}): ".format(len(shop_items) + 1)))
    if 1 <= choice <= len(shop_items):
        buy_item(choice - 1)
    elif choice == len(shop_items) + 1:
        print("Exiting shop...")
    else:
        print("Invalid choice.")

def buy_item(item_index: int) -> None:
    global user_data
    item = shop_items[item_index]
    if user_data["gold"] >= item["price"]:
        user_data["gold"] -= item["price"]
        user_data["inventory"].append(item["name"])
        print(f"You bought {item['name']} for {item['price']} gold!")
    else:
        print("You don't have enough gold!")

def equip_item(item_name: str) -> None:
    if not user_data["class"]:
        print(f"{FAIL}You need to create a character first! Use /new{ENDC}")
        return

    try:
        # Case-insensitive match for item in inventory
        item = next((i for i in user_data["inventory"] if i.lower() == item_name.lower()), None)
        if not item:
            print(f"{WARNING}You don't have {item_name} in your inventory.{ENDC}")
            return

        item_type = None
        effect = 0

        # Check if item is a weapon (case-insensitive)
        weapon_key = next((w for w in WEAPONS if w.lower() == item.lower()), None)
        if weapon_key:
            item_type = "weapon"
            effect = WEAPONS[weapon_key]["damage"]
        # Check if item is armor by keywords
        elif any(armor_type in item for armor_type in ["Armor", "Shield", "Helmet", "Boots"]):
            item_type = "armor"
            armor_tier = item.split()[0]
            effect = {
                "Bone": 5,
                "Iron": 10,
                "Steel": 15,
                "Dark": 15,
                "Dragon": 20
            }.get(armor_tier, 5)

        if item_type:
            user_data["equipped"][item_type] = {"name": item, "effect": effect}
            print_header("Equip Item")
            print(f"{OKGREEN}You equipped {item}!{ENDC}")
        else:
            print(f"{WARNING}{item} cannot be equipped.{ENDC}")
    except Exception as e:
        print(f"{FAIL}Error equipping item: {e}{ENDC}")

def show_stats() -> None:
    print_header("Your Stats")
    print(f"{BOLD}Level:{ENDC} {user_data['level']}")
    print(f"{BOLD}Health:{ENDC} {user_data['health']}/{user_data['max_health']}")
    print(f"{BOLD}Attack:{ENDC} {user_data['attack'] + (user_data['equipped']['weapon']['effect'] if user_data['equipped']['weapon'] else 0)}")
    print(f"{BOLD}Defense:{ENDC} {user_data['defense'] + (user_data['equipped']['armor']['effect'] if user_data['equipped']['armor'] else 0)}")
    print(f"{BOLD}Gold:{ENDC} {user_data['gold']}")
    print(f"{BOLD}Equipped Weapon:{ENDC} {user_data['equipped']['weapon']['name'] if user_data['equipped']['weapon'] else 'None'}")
    print(f"{BOLD}Equipped Armor:{ENDC} {user_data['equipped']['armor']['name'] if user_data['equipped']['armor'] else 'None'}")

# New functions for additional commands
def list_dungeons() -> None:
    print_header("Dungeon List")
    # Group dungeons by area
    dungeons_by_area = {}
    for dungeon in dungeons:
        area = dungeon.get('area', 'Unknown Area')
        if area not in dungeons_by_area:
            dungeons_by_area[area] = []
        dungeons_by_area[area].append(dungeon)

    # Display dungeons by area with completion status
    for area, area_dungeons in sorted(dungeons_by_area.items()):
        print(f"\n{BOLD}{CYAN}{area}:{ENDC}")
        for dungeon in sorted(area_dungeons, key=lambda x: x['name']):
            name = dungeon['name']
            completed = name in user_data.get("dungeons_completed", [])
            if completed:
                print(f"{OKGREEN}✓ {name}{ENDC}")
                # Show rewards if completed
                if "loot" in dungeon:
                    print(f"  Rewards collected: {', '.join(dungeon['loot'])}")
            else:
                # Show requirements if not completed
                reqs = []
                if "level_required" in dungeon:
                    reqs.append(f"Level {dungeon['level_required']}")
                if reqs:
                    print(f"{FAIL}✗ {name} (Required: {', '.join(reqs)}){ENDC}")
                else:
                    print(f"{FAIL}✗ {name}{ENDC}")
            # Show monsters
            if "monsters" in dungeon:
                print(f"  Monsters: {', '.join(dungeon['monsters'])}")

def show_bestiary() -> None:
    print_header("Bestiary")
    for monster in monsters:
        print(f"Name: {monster['name']}, Level: {monster['level']}, Health: {monster['health']}, Attack: {monster['attack']}, Drops: {', '.join(monster['drops'])}")

def show_support() -> None:
    print_header("Support Information")
    print_animated("For support, visit our Discord server or check the wiki.", CYAN, 0.01)

# Guild management commands
def get_next_rank(current_rank):
    ranks = [
        {"name": "Novice", "level_req": 1, "quest_req": 0, "boss_req": 0},
        {"name": "Apprentice", "level_req": 5, "quest_req": 10, "boss_req": 1},
        {"name": "Journeyman", "level_req": 10, "quest_req": 25, "boss_req": 3},
        {"name": "Adventurer", "level_req": 15, "quest_req": 50, "boss_req": 5},
        {"name": "Veteran", "level_req": 20, "quest_req": 75, "boss_req": 10},
        {"name": "Elite", "level_req": 25, "quest_req": 100, "boss_req": 15},
        {"name": "Master", "level_req": 30, "quest_req": 150, "boss_req": 20},
        {"name": "Grandmaster", "level_req": 40, "quest_req": 200, "boss_req": 30},
        {"name": "Legend", "level_req": 50, "quest_req": 300, "boss_req": 50},
        {"name": "Hero", "level_req": 60, "quest_req": 400, "boss_req": 75},
        {"name": "Champion", "level_req": 70, "quest_req": 500, "boss_req": 100}
    ]
    
    for i, rank in enumerate(ranks):
        if rank["name"] == current_rank and i < len(ranks) - 1:
            return ranks[i + 1]
    return None

def get_adventurer_level_rewards(level):
    rewards = {
        1: {"description": "Access to basic quests", "bonuses": {}},
        2: {"description": "+5% Gold from monsters", "bonuses": {"gold_bonus": 0.05}},
        3: {"description": "Access to the Guild Shop", "bonuses": {"unlock_shop": True}},
        5: {"description": "+10% XP from all sources", "bonuses": {"xp_bonus": 0.10}},
        7: {"description": "Access to uncommon materials", "bonuses": {"unlock_materials": "uncommon"}},
        10: {"description": "+15% Damage against bosses", "bonuses": {"boss_damage": 0.15}},
        12: {"description": "Access to rare materials", "bonuses": {"unlock_materials": "rare"}},
        15: {"description": "+10% Crafting success chance", "bonuses": {"craft_bonus": 0.10}},
        20: {"description": "+20% Health in dungeons", "bonuses": {"dungeon_health": 0.20}},
        25: {"description": "Access to epic materials", "bonuses": {"unlock_materials": "epic"}},
        30: {"description": "Unique weapon for your class", "bonuses": {"unique_weapon": True}},
        35: {"description": "Pet evolution unlocked", "bonuses": {"pet_evolution": True}},
        40: {"description": "+25% All stats in trials", "bonuses": {"trial_stats": 0.25}},
        50: {"description": "Legendary equipment crafting", "bonuses": {"legendary_craft": True}},
        60: {"description": "Dimensional travel discount", "bonuses": {"dimension_discount": 0.50}},
        70: {"description": "Hero's equipment set", "bonuses": {"hero_set": True}}
    }
    
    return rewards.get(level, None)

def add_adventurer_exp(amount):
    """Add experience to the adventurer and check for level up
    
    Args:
        amount: Amount of experience to add
    """
    # Initialize adventurer data if it doesn't exist
    if "adventurer" not in user_data:
        user_data["adventurer"] = {
            "rank": "Novice",
            "exp": 0,
            "level": 1,
            "total_quests": 0,
            "bosses_defeated": 0,
            "reputation": 0
        }
    
    adv = user_data["adventurer"]
    
    # Add the experience
    adv["exp"] += amount
    
    # Check for level up
    exp_required = adv["level"] * 100
    
    # While we have enough exp for next level
    while adv["exp"] >= exp_required:
        adv["exp"] -= exp_required
        adv["level"] += 1
        exp_required = adv["level"] * 100
        
        rewards = get_adventurer_level_rewards(adv["level"])
        
        print_animated(f"\n{OKGREEN}◆◆◆ ADVENTURER LEVEL UP! ◆◆◆{ENDC}", delay=0.05)
        print_animated(f"{OKGREEN}You are now level {adv['level']}!{ENDC}", delay=0.05)
        
        if rewards:
            print_animated(f"{OKGREEN}New Reward: {rewards['description']}{ENDC}", delay=0.05)
        
        # Check if new rank is available
        check_rank_advancement()

def check_rank_advancement():
    """Check if adventurer qualifies for a rank advancement"""
    adv = user_data["adventurer"]
    next_rank = get_next_rank(adv["rank"])
    
    if next_rank and adv["level"] >= next_rank["level_req"] and \
       adv["total_quests"] >= next_rank["quest_req"] and \
       adv["bosses_defeated"] >= next_rank["boss_req"]:
        
        old_rank = adv["rank"]
        adv["rank"] = next_rank["name"]
        
        print_animated(f"\n{HEADER}▓▓▓ ADVENTURER RANK ADVANCEMENT! ▓▓▓{ENDC}", delay=0.05)
        print_animated(f"{CYAN}You have been promoted from {old_rank} to {next_rank['name']}!{ENDC}", delay=0.05)
        print_animated(f"{YELLOW}Visit the Adventurer's Guild to learn about your new benefits.{ENDC}", delay=0.05)
        
        # Add some gold as a reward
        reward_gold = adv["level"] * 100
        user_data["gold"] += reward_gold
        print_animated(f"{LIGHTYELLOW}You received {reward_gold} gold for your promotion!{ENDC}", delay=0.05)

def guild_join(guild_name: str) -> None:
    print(f"{YELLOW}The adventurer system has been updated!{ENDC}")
    print("You are now automatically part of the Adventurer's Guild.")
    print("Use '/guild' to view your adventurer status and guild information.")

def guild_leave() -> None:
    print(f"{YELLOW}You cannot leave the Adventurer's Guild.{ENDC}")
    print("All players are members of the guild for quest tracking and rewards.")
    print("Use '/guild' to view your adventurer status and guild information.")

def guild_list() -> None:
    print_header("Available Factions")
    # List of factions in the game world
    factions = [
        {"name": "Empire of Aetheria", "alignment": "Order", "description": "A powerful empire ruling the central kingdoms with strict laws and military might."},
        {"name": "Northern Tribes", "alignment": "Freedom", "description": "Independent clans of the frozen north, valuing strength and personal liberty."},
        {"name": "Order of the Sacred Flame", "alignment": "Light", "description": "Devotees of celestial powers, focusing on healing, protection, and banishing darkness."},
        {"name": "Shadowveil Syndicate", "alignment": "Shadow", "description": "A secretive network of spies, assassins, and information brokers."},
        {"name": "Arcane Confluence", "alignment": "Knowledge", "description": "Scholars and mages dedicated to the pursuit of magical knowledge."},
        {"name": "Wildwalker Coalition", "alignment": "Nature", "description": "Protectors of nature who draw power from the primal forces of the world."},
        {"name": "Ironheart Mercenary Company", "alignment": "Neutral", "description": "Elite mercenaries who sell their combat services to the highest bidder."},
        {"name": "Children of the Void", "alignment": "Chaos", "description": "Cultists who worship ancient entities from beyond reality."},
        {"name": "The Eternal Vigil", "alignment": "Spirit", "description": "Those who maintain the balance between the living world and spirit realm."},
        {"name": "Techsmith's Guild", "alignment": "Progress", "description": "Inventors and engineers pushing the boundaries of what's possible without magic."}
    ]
    
    # The Old Legacy factions
    print(f"{LIGHTBLUE}Original Factions:{ENDC}")
    print(f"- {CYAN}Warriors Guild{ENDC}: Combat specialists")
    print(f"- {BLUE}Mages Guild{ENDC}: Magic practitioners")
    print(f"- {YELLOW}Rogues Guild{ENDC}: Masters of stealth")
    print(f"- {OKGREEN}Paladins Guild{ENDC}: Holy warriors")
    print(f"- {LIGHTRED}Hunters Guild{ENDC}: Beast trackers")
    
    # Print the new factions
    print(f"\n{LIGHTMAGENTA}Major World Factions:{ENDC}")
    for faction in factions:
        print(f"- {BOLD}{faction['name']}{ENDC} ({faction['alignment']}): {faction['description']}")
    
    print(f"\n{YELLOW}Note:{ENDC} Factions represent the major powers in the world.")
    print("Your reputation with these factions affects quests, prices, and dialogue options.")
    print("The Adventurer's Guild remains neutral, working with all factions as needed.")

# Trading system
def trading_system() -> None:
    print_header("Trading System")
    print("Trading system is under development. Stay tuned!")

# Professions system
def professions_system() -> None:
    print_header("Professions System")
    if user_data["has_chosen_profession"]:
        print(f"You are currently a {user_data['profession']}.")
    else:
        print("You have not chosen a profession yet.")
        print("Available professions:")
        for prof in PROFESSIONS:
            print(f"- {prof}")
        choice = input("Choose a profession: ").capitalize()
        if choice in PROFESSIONS:
            user_data["profession"] = choice
            user_data["has_chosen_profession"] = True
            print(f"You are now a {choice}.")
        else:
            print("Invalid profession choice.")

def get_active_pet() -> Optional[Dict]:
    """Returns the currently active pet or None if no pet is active"""
    active_pet_name = user_data.get("active_pet", None)
    if not active_pet_name or active_pet_name not in user_data["pets"]:
        return None
    
    pet_info = PETS.get(active_pet_name, None)
    if not pet_info:
        return None
    
    # Initialize additional pet stats if they don't exist yet
    if "pet_stats" not in user_data:
        user_data["pet_stats"] = {}
    
    if active_pet_name not in user_data["pet_stats"]:
        pet_level = 1
        user_data["pet_stats"][active_pet_name] = {
            "level": pet_level,
            "exp": 0,
            "exp_next": 100 * pet_level,
            "loyalty": 50,  # 0-100 scale
            "abilities": [],
            "element": pet_info.get("element", "Nullum")
        }
    
    # Combine base pet info with pet stats
    full_pet_info = {**pet_info, **user_data["pet_stats"][active_pet_name]}
    full_pet_info["name"] = active_pet_name
    
    return full_pet_info

def pet_level_up(pet_name: str) -> bool:
    """Level up a pet if it has enough experience
    Returns True if level up successful, False otherwise
    """
    if pet_name not in user_data["pets"] or pet_name not in user_data.get("pet_stats", {}):
        return False
    
    pet_stats = user_data["pet_stats"][pet_name]
    if pet_stats["exp"] >= pet_stats["exp_next"]:
        pet_stats["level"] += 1
        pet_stats["exp"] = pet_stats["exp"] - pet_stats["exp_next"]
        pet_stats["exp_next"] = 100 * pet_stats["level"]
        
        # Check for new abilities at certain levels
        pet_base = PETS.get(pet_name, {})
        pet_abilities = pet_base.get("abilities", {})
        
        for level, ability in pet_abilities.items():
            if str(pet_stats["level"]) == level and ability not in pet_stats["abilities"]:
                pet_stats["abilities"].append(ability)
                print(f"{CYAN}Your pet {pet_name} learned a new ability: {ability}!{ENDC}")
        
        return True
    return False

def train_pet(pet_name: str) -> None:
    """Train your pet to increase its experience and loyalty"""
    print_header("Pet Training")
    
    if pet_name not in user_data["pets"]:
        print(f"You do not own a pet named {pet_name}.")
        return
    
    # Initialize pet stats if needed
    if "pet_stats" not in user_data:
        user_data["pet_stats"] = {}
    
    if pet_name not in user_data["pet_stats"]:
        user_data["pet_stats"][pet_name] = {
            "level": 1,
            "exp": 0,
            "exp_next": 100,
            "loyalty": 50,
            "abilities": [],
            "element": PETS.get(pet_name, {}).get("element", "Nullum")
        }
    
    print(f"Training {pet_name}...")
    
    # Training options
    print("\nTraining Activities:")
    print("1. Basic Training (+10 exp, +2 loyalty)")
    print("2. Advanced Drills (+25 exp, +1 loyalty)")
    print("3. Elemental Focus (+15 exp, chance to unlock elemental ability)")
    print("4. Loyalty Building (+5 exp, +5 loyalty)")
    print("0. Cancel")
    
    choice = input("\nChoose a training activity: ").strip()
    
    if choice == "0":
        return
    
    pet_stats = user_data["pet_stats"][pet_name]
    # We'll use pet stats directly instead of base pet data
    pet_element = pet_stats.get("element", "Nullum")
    
    training_cost = 10  # Base gold cost for training
    
    if user_data["gold"] < training_cost:
        print(f"{RED}You need {training_cost} gold to train your pet.{ENDC}")
        return
    
    user_data["gold"] -= training_cost
    
    if choice == "1":  # Basic Training
        exp_gain = 10
        loyalty_gain = 2
        print(f"{GREEN}You complete basic training with {pet_name}.{ENDC}")
        
    elif choice == "2":  # Advanced Drills
        exp_gain = 25
        loyalty_gain = 1
        print(f"{GREEN}You push {pet_name} through some challenging drills.{ENDC}")
        
    elif choice == "3":  # Elemental Focus
        exp_gain = 15
        loyalty_gain = 0
        
        # If pet doesn't have an element yet, chance to develop one
        if pet_element == "Nullum":
            element_choices = ["Fire", "Water", "Earth", "Air", "Lightning"]
            if random.random() < 0.25:  # 25% chance
                new_element = random.choice(element_choices)
                pet_stats["element"] = new_element
                print(f"{CYAN}Success! {pet_name} has connected with the {new_element} element!{ENDC}")
            else:
                print(f"You train {pet_name} to focus on elemental energy, but no connection forms yet.")
        else:
            print(f"You help {pet_name} strengthen their {pet_element} elemental connection.")
            # Chance to learn an elemental ability if at appropriate level
            if pet_stats["level"] >= 3 and random.random() < 0.2:  # 20% chance if level 3+
                elemental_abilities = {
                    "Fire": "Flame Burst",
                    "Water": "Healing Mist",
                    "Earth": "Stone Shield",
                    "Air": "Swift Movement",
                    "Lightning": "Shock Strike"
                }
                
                ability = elemental_abilities.get(pet_element, "Energy Pulse")
                if ability not in pet_stats["abilities"]:
                    pet_stats["abilities"].append(ability)
                    print(f"{CYAN}{pet_name} learned {ability}!{ENDC}")
                    
    elif choice == "4":  # Loyalty Building
        exp_gain = 5
        loyalty_gain = 5
        print(f"{GREEN}You spend quality time bonding with {pet_name}.{ENDC}")
        
    else:
        print("Invalid choice.")
        return
    
    # Apply experience and loyalty gains
    pet_stats["exp"] += exp_gain
    pet_stats["loyalty"] = min(100, pet_stats["loyalty"] + loyalty_gain)
    
    print(f"Experience gained: {exp_gain}")
    print(f"Current EXP: {pet_stats['exp']}/{pet_stats['exp_next']}")
    print(f"Loyalty: {pet_stats['loyalty']}/100")
    
    # Check for level up
    if pet_level_up(pet_name):
        print(f"{YELLOW}{pet_name} leveled up to level {pet_stats['level']}!{ENDC}")
    
    # Learning chance based on loyalty
    if pet_stats["loyalty"] >= 75 and random.random() < 0.1:  # 10% chance if loyalty is high
        general_abilities = ["Quick Attack", "Protective Stance", "Find Treasure", "Scouting"]
        potential_ability = random.choice(general_abilities)
        
        if potential_ability not in pet_stats["abilities"]:
            pet_stats["abilities"].append(potential_ability)
            print(f"{CYAN}Due to your strong bond, {pet_name} learned {potential_ability}!{ENDC}")

def equip_pet(pet_name: str = "") -> None:
    """Equip or unequip a pet to accompany you in battle"""
    print_header("Equip Pet")
    
    if pet_name == "":
        # Show available pets
        if not user_data["pets"]:
            print("You have no pets to equip.")
            return
            
        current_pet = user_data.get("active_pet", None)
        if current_pet:
            print(f"Currently equipped: {current_pet}")
        else:
            print("No pet currently equipped.")
            
        print("\nAvailable pets:")
        for i, pet in enumerate(user_data["pets"], 1):
            print(f"{i}. {pet}")
            
        choice = input("\nEnter pet number to equip, or 0 to unequip current pet: ").strip()
        
        if choice == "0":
            if current_pet:
                user_data["active_pet"] = None
                print(f"Unequipped {current_pet}.")
            else:
                print("No pet is currently equipped.")
            return
            
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(user_data["pets"]):
                pet_name = user_data["pets"][choice_idx]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return
    
    # Equip the selected pet
    if pet_name in user_data["pets"]:
        user_data["active_pet"] = pet_name
        print(f"Equipped {pet_name} as your active companion.")
        
        # Initialize pet stats if this is first time equipping
        if "pet_stats" not in user_data:
            user_data["pet_stats"] = {}
            
        if pet_name not in user_data["pet_stats"]:
            user_data["pet_stats"][pet_name] = {
                "level": 1,
                "exp": 0,
                "exp_next": 100,
                "loyalty": 50,
                "abilities": [],
                "element": PETS.get(pet_name, {}).get("element", "Nullum")
            }
    else:
        print(f"You don't have a pet named {pet_name}.")

def show_pets() -> None:
    """Display a detailed view of all owned pets"""
    print_header("Your Pets")
    
    if not user_data["pets"]:
        print("You have no pets.")
        return
        
    active_pet = user_data.get("active_pet", None)
    
    for pet_name in user_data["pets"]:
        pet_info = PETS.get(pet_name, None)
        if not pet_info:
            print(f"{pet_name} - A mysterious companion.")
            continue
            
        # Check if this is the active pet
        active_marker = f" {GREEN}[ACTIVE]{ENDC}" if pet_name == active_pet else ""
        
        # Get color based on pet rarity/type
        pet_color = CYAN if pet_name == "Hylit" else YELLOW if "Dragon" in pet_name or "Phoenix" in pet_name else WHITE
        
        # Display pet name with color and active status
        print(f"\n{pet_color}{pet_name}{ENDC}{active_marker}")
        print(f"Description: {pet_info['description']}")
        
        # Get pet stats if available
        if "pet_stats" in user_data and pet_name in user_data["pet_stats"]:
            pet_stats = user_data["pet_stats"][pet_name]
            
            # Display level and exp
            level = pet_stats["level"]
            exp = pet_stats["exp"]
            exp_next = pet_stats["exp_next"]
            loyalty = pet_stats["loyalty"]
            
            # Create progress bars
            exp_percent = exp / exp_next
            exp_bar = create_progress_bar(exp_percent, 15)
            
            # Set loyalty color based on percentage (without creating unused variable)
            loyalty_color = RED if loyalty < 30 else YELLOW if loyalty < 70 else GREEN
            
            print(f"Level: {level}")
            print(f"EXP: {exp_bar} {exp}/{exp_next}")
            print(f"Loyalty: {loyalty_color}{loyalty}/100{ENDC}")
            
            # Display element if any
            element = pet_stats.get("element", "Nullum")
            if element != "Nullum":
                element_color = get_element_color(element)
                print(f"Element: {element_color}{element}{ENDC}")
            
            # Display abilities
            abilities = pet_stats.get("abilities", [])
            if abilities:
                print("Abilities:")
                for ability in abilities:
                    print(f"  - {MAGENTA}{ability}{ENDC}")
        
        # Display base stat boosts
        boost_str = ", ".join(f"+{v} {k}" for k, v in pet_info.get("boost", {}).items())
        if boost_str:
            print(f"Stat Bonuses: {boost_str}")
    
    # Display commands for pet interaction
    print("\nPet Commands:")
    print("/equip_pet - Equip a pet for battle")
    print("/train_pet <name> - Train your pet to increase its level and abilities")
    print("/pet_info <name> - View detailed information about a specific pet")
    print("/feed_pet <name> - Feed your pet to increase loyalty")

def evolve_pet(pet_name: str) -> None:
    """Evolve a pet to its next form if requirements are met
    
    Args:
        pet_name: The name of the pet to evolve
    """
    print_header("Pet Evolution")
    
    # Check if pet exists
    if pet_name not in user_data["pets"]:
        print(f"{RED}You don't have a pet named '{pet_name}'.{ENDC}")
        return
    
    # Check if adventurer level requirement is met
    if "adventurer" not in user_data or user_data["adventurer"]["level"] < 35:
        print(f"{YELLOW}Pet evolution requires Adventurer Level 35.{ENDC}")
        print(f"Your current level: {user_data.get('adventurer', {}).get('level', 0)}")
        print("Continue advancing in the Adventurer's Guild to unlock this feature.")
        return
    
    # Check if pet has an evolution
    pet_base = PETS.get(pet_name, {})
    next_evolution = pet_base.get("evolution")
    
    if not next_evolution:
        print(f"{YELLOW}{pet_name} cannot evolve further.{ENDC}")
        return
    
    # Get evolution requirements
    if pet_name not in PET_EVOLUTIONS:
        print(f"{RED}Evolution data not found for {pet_name}.{ENDC}")
        return
    
    evolution_data = PET_EVOLUTIONS[pet_name]
    level_req = evolution_data.get("level_required", 0)
    loyalty_req = evolution_data.get("loyalty_required", 0)
    materials_req = evolution_data.get("materials_required", [])
    
    # Initialize pet stats if needed
    if "pet_stats" not in user_data:
        user_data["pet_stats"] = {}
    
    if pet_name not in user_data["pet_stats"]:
        user_data["pet_stats"][pet_name] = {
            "level": 1,
            "exp": 0,
            "exp_next": 100,
            "loyalty": 50,
            "abilities": [],
            "element": pet_base.get("element", "Nullum")
        }
    
    pet_stats = user_data["pet_stats"][pet_name]
    
    # Check requirements
    print(f"{CYAN}Evolution Target:{ENDC} {next_evolution}")
    print(f"\n{CYAN}Requirements:{ENDC}")
    
    # Level check
    level_ok = pet_stats["level"] >= level_req
    level_status = f"{GREEN}✓{ENDC}" if level_ok else f"{RED}✗{ENDC}"
    print(f"{level_status} Level {pet_stats['level']}/{level_req}")
    
    # Loyalty check
    loyalty_ok = pet_stats["loyalty"] >= loyalty_req
    loyalty_status = f"{GREEN}✓{ENDC}" if loyalty_ok else f"{RED}✗{ENDC}"
    print(f"{loyalty_status} Loyalty {pet_stats['loyalty']}/{loyalty_req}")
    
    # Materials check
    print(f"\n{CYAN}Required Materials:{ENDC}")
    materials_ok = True
    for material in materials_req:
        material_count = sum(1 for item in user_data.get("materials", []) if item == material)
        material_status = f"{GREEN}✓{ENDC}" if material_count > 0 else f"{RED}✗{ENDC}"
        print(f"{material_status} {material}: {material_count}/1")
        if material_count < 1:
            materials_ok = False
    
    # Check if all requirements are met
    if not (level_ok and loyalty_ok and materials_ok):
        print(f"\n{YELLOW}Cannot evolve yet. Please meet all requirements first.{ENDC}")
        return
    
    # Confirm evolution
    print(f"\n{CYAN}Your {pet_name} is ready to evolve into {next_evolution}!{ENDC}")
    confirm = input("Proceed with evolution? This will consume the required materials. (y/n): ").lower()
    
    if confirm != 'y':
        print("Evolution cancelled.")
        return
    
    # Process evolution - consume materials
    for material in materials_req:
        # Find and remove one instance of each required material
        for i, item in enumerate(user_data.get("materials", [])):
            if item == material:
                user_data["materials"].pop(i)
                break
    
    # Replace old pet with evolved form
    user_data["pets"].remove(pet_name)
    user_data["pets"].append(next_evolution)
    
    # Transfer pet stats to evolved form
    evolved_stats = pet_stats.copy()
    evolved_stats["element"] = PETS.get(next_evolution, {}).get("element", evolved_stats["element"])
    user_data["pet_stats"][next_evolution] = evolved_stats
    
    # If pet was active, update active pet
    if user_data.get("active_pet") == pet_name:
        user_data["active_pet"] = next_evolution
    
    # Clear old pet stats
    del user_data["pet_stats"][pet_name]
    
    # Show evolution animation
    print("\n")
    print_animated(f"{HEADER}✧・゚: *✧・゚:* EVOLUTION *:・゚✧*:・゚✧{ENDC}", delay=0.05)
    print_animated(f"{YELLOW}Your {pet_name} is evolving...{ENDC}", delay=0.1)
    time.sleep(1)
    
    for _ in range(5):
        print_animated(".", delay=0.3)
    
    print("\n")
    print_animated(f"{MAGENTA}Congratulations! {pet_name} has evolved into {next_evolution}!{ENDC}", delay=0.05)
    
    # Show new pet abilities
    new_abilities = PETS.get(next_evolution, {}).get("abilities", {})
    print(f"\n{CYAN}New Abilities:{ENDC}")
    for level, ability in new_abilities.items():
        print(f"- Level {level}: {ability}")
    
    # Add achievement
    # This should be added to the achievement system
    print(f"\n{GREEN}Achievement Unlocked: First Evolution{ENDC}")
    
    # Update adventurer experience
    add_adventurer_exp(50)  # Award exp for evolving a pet

def pet_info(pet_name: str) -> None:
    """Display detailed information about a specific pet"""
    print_header("Pet Information")
    
    if pet_name not in user_data["pets"]:
        print(f"You don't have a pet named {pet_name}.")
        return
        
    pet_base = PETS.get(pet_name, {})
    if not pet_base:
        print(f"No information available for {pet_name}.")
        return
        
    # Display pet details
    print(f"{YELLOW}Name:{ENDC} {pet_name}")
    print(f"{YELLOW}Description:{ENDC} {pet_base.get('description', 'A mysterious companion')}")
    print(f"{YELLOW}Rarity:{ENDC} {pet_base.get('rarity', 'Common')}")
    print(f"{YELLOW}Element:{ENDC} {pet_base.get('element', 'Nullum')}")
    print(f"{YELLOW}Combat Style:{ENDC} {pet_base.get('combat_style', 'Balanced')}")
    
    # Display evolution information
    evolution = pet_base.get("evolution")
    if evolution:
        print(f"\n{MAGENTA}Evolution Path:{ENDC} {pet_name} → {evolution}")
        
        if pet_name in PET_EVOLUTIONS:
            evo_data = PET_EVOLUTIONS[pet_name]
            print(f"{MAGENTA}Evolution Requirements:{ENDC}")
            print(f"- Level: {evo_data.get('level_required', 'Unknown')}")
            print(f"- Loyalty: {evo_data.get('loyalty_required', 'Unknown')}")
            materials = evo_data.get('materials_required', [])
            if materials:
                print(f"- Materials: {', '.join(materials)}")
            
            # Show adventurer level requirement
            print("- Adventurer Level: 35 (Evolution Feature)")
            print(f"\n{CYAN}Use '/evolve_pet {pet_name}' to evolve this pet when requirements are met.{ENDC}")
    else:
        print(f"\n{YELLOW}Evolution:{ENDC} Max evolution reached")
    
    # Display base stats
    boosts = pet_base.get("boost", {})
    if boosts:
        print(f"\n{YELLOW}Base Stat Bonuses:{ENDC}")
        for stat, value in boosts.items():
            print(f"  {stat.capitalize()}: +{value}")
    
    # Display additional stats if available
    if "pet_stats" in user_data and pet_name in user_data["pet_stats"]:
        pet_stats = user_data["pet_stats"][pet_name]
        
        print(f"\n{YELLOW}Current Stats:{ENDC}")
        print(f"Level: {pet_stats['level']}")
        
        # Calculate actual bonuses based on level
        level_multiplier = 1 + (pet_stats['level'] - 1) * 0.1  # 10% increase per level
        print(f"Stat Multiplier: x{level_multiplier:.1f} (from level)")
        
        print(f"\n{YELLOW}Calculated Combat Bonuses:{ENDC}")
        for stat, base_value in boosts.items():
            actual_value = round(base_value * level_multiplier)
            print(f"  {stat.capitalize()}: +{actual_value}")
        
        # Display element
        element = pet_stats.get("element", "Nullum")
        if element != "Nullum":
            element_color = get_element_color(element)
            print(f"\n{YELLOW}Element:{ENDC} {element_color}{element}{ENDC}")
        
        # Display abilities
        abilities = pet_stats.get("abilities", [])
        if abilities:
            print(f"\n{YELLOW}Abilities:{ENDC}")
            for ability in abilities:
                print(f"  - {MAGENTA}{ability}{ENDC}")
                
                # Display ability descriptions
                ability_desc = ABILITY_DESCRIPTIONS.get(ability, "No description available")
                print(f"    {ability_desc}")
        
        # Display loyalty and effects
        loyalty = pet_stats.get("loyalty", 0)
        loyalty_color = RED if loyalty < 30 else YELLOW if loyalty < 70 else GREEN
        
        print(f"\n{YELLOW}Loyalty:{ENDC} {loyalty_color}{loyalty}/100{ENDC}")
        
        # Loyalty effects
        if loyalty < 30:
            print("  Low loyalty: Pet may occasionally refuse to use abilities")
        elif loyalty < 70:
            print("  Moderate loyalty: Pet performs as expected")
        else:
            print("  High loyalty: Pet may occasionally perform critical hits")

def feed_pet(pet_name: str) -> None:
    """Feed your pet to increase loyalty"""
    print_header("Feed Pet")
    
    if pet_name not in user_data["pets"]:
        print(f"You don't have a pet named {pet_name}.")
        return
    
    # Initialize pet stats if needed
    if "pet_stats" not in user_data:
        user_data["pet_stats"] = {}
    
    if pet_name not in user_data["pet_stats"]:
        user_data["pet_stats"][pet_name] = {
            "level": 1,
            "exp": 0,
            "exp_next": 100,
            "loyalty": 50,
            "abilities": [],
            "element": PETS.get(pet_name, {}).get("element", "Nullum")
        }
    
    # Get food from inventory
    food_items = [item for item in user_data["inventory"] if "Food" in item or "Treat" in item or "Fish" in item or "Meat" in item or "Fruit" in item]
    
    if not food_items:
        print("You don't have any food items to feed your pet.")
        print("You can find food by hunting, fishing, or purchasing from shops.")
        return
    
    print(f"Selected pet: {pet_name}")
    print(f"Current loyalty: {user_data['pet_stats'][pet_name]['loyalty']}/100")
    print("\nAvailable food items:")
    
    for i, food in enumerate(food_items, 1):
        print(f"{i}. {food}")
    
    print("0. Cancel")
    
    choice = input("\nSelect food to give to your pet: ").strip()
    
    if choice == "0":
        return
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(food_items):
            selected_food = food_items[choice_idx]
            
            # Remove the food from inventory
            user_data["inventory"].remove(selected_food)
            
            # Calculate loyalty and exp gain based on food type
            loyalty_gain = 5  # Base gain
            exp_gain = 2  # Base gain
            
            if "Premium" in selected_food:
                loyalty_gain += 10
                exp_gain += 5
            elif "Rare" in selected_food:
                loyalty_gain += 7
                exp_gain += 3
                
            if "Treat" in selected_food:
                loyalty_gain += 3
            elif "Meat" in selected_food:
                exp_gain += 2
                
            # Apply gains
            user_data["pet_stats"][pet_name]["loyalty"] = min(100, user_data["pet_stats"][pet_name]["loyalty"] + loyalty_gain)
            user_data["pet_stats"][pet_name]["exp"] += exp_gain
            
            print(f"\n{GREEN}You feed {selected_food} to {pet_name}.{ENDC}")
            print(f"Loyalty increased by {loyalty_gain}!")
            print(f"Experience gained: {exp_gain}")
            print(f"Current loyalty: {user_data['pet_stats'][pet_name]['loyalty']}/100")
            
            # Check for level up
            if pet_level_up(pet_name):
                print(f"{YELLOW}{pet_name} leveled up to level {user_data['pet_stats'][pet_name]['level']}!{ENDC}")
            
            # Special interactions based on pet
            if pet_name == "Hylit":
                print(f"{CYAN}Hylit: 'Thank you for the delicious food!'{ENDC}")
            elif "Dragon" in pet_name:
                print(f"{RED}Your dragon pet breathes a small flame of appreciation.{ENDC}")
            elif "Cat" in pet_name:
                print("Your cat purrs contentedly.")
            elif "Dog" in pet_name:
                print("Your dog wags its tail excitedly!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

# Achievements system
achievements = []

# Second show_achievements function removed (duplicate)
# Using the more complete version defined earlier

# Inventory management commands
def sort_inventory() -> None:
    user_data["inventory"].sort()
    print("Inventory sorted alphabetically.")

def filter_inventory() -> None:
    filter_term = input("Enter filter term: ").lower()
    filtered = [item for item in user_data["inventory"] if filter_term in item.lower()]
    print(f"Filtered inventory items containing '{filter_term}':")
    for item in filtered:
        print(f"- {item}")

# Quest management commands
def list_active_quests() -> None:
    print_header("Active Quests")
    if not user_data["active_quests"]:
        print("You have no active quests.")
        return
    for quest in user_data["active_quests"]:
        print(f"- {quest['name']}: {quest['description']}")

def complete_quest(quest_name: str) -> None:
    quest = next((q for q in user_data["active_quests"] if q["name"].lower() == quest_name.lower()), None)
    if quest:
        user_data["active_quests"].remove(quest)
        user_data["completed_quests"].append(quest["id"])
        reward = quest.get("reward", {})
        gold = reward.get("gold", 0)
        exp = reward.get("exp", 0)
        user_data["gold"] += gold
        user_data["exp"] += exp
        
        # Add adventurer experience (50% of regular exp, minimum 10)
        adv_exp = max(10, int(exp * 0.5))
        add_adventurer_exp(adv_exp)
        
        # Increment quest counter in adventurer data
        if "adventurer" in user_data:
            user_data["adventurer"]["total_quests"] += 1
            # Check if rank advancement is available
            check_rank_advancement()
        
        print(f"Quest '{quest['name']}' completed! You received {gold} gold and {exp} experience.")
        print(f"{CYAN}Adventurer Guild:{ENDC} +{adv_exp} adventurer exp")
        check_level_up()
        # Grant Hylit pet after completing quest 1
        if quest["id"] == 101 and "Hylit" not in user_data["pets"]:
            user_data["pets"].append("Hylit")
            print("Hylit has joined you as a companion!")
    else:
        print(f"No active quest named '{quest_name}' found.")

def create_character() -> None:
    if user_data["class"] is not None:
        print("You have already created a character!")
        return

    print_header("Character Creation")

    # Prompt for character name
    while True:
        name = input("Enter your character's name: ").strip()
        if name:
            user_data["name"] = name
            break
        else:
            print("Name cannot be empty. Please enter a valid name.")

    print("Choose your class:")
    for class_name in CHARACTER_CLASSES:
        print(f"[{class_name}]")
        for stat, value in CHARACTER_CLASSES[class_name].items():
            print(f"  {stat}: {value:+}")

    while True:
        choice = input("Enter class name: ").capitalize()
        if choice in CHARACTER_CLASSES:
            user_data["class"] = choice
            user_data["skills"] = SKILLS[choice]
            stats = CHARACTER_CLASSES[choice]
            user_data["max_health"] += stats["health_bonus"]
            user_data["health"] = user_data["max_health"]
            user_data["attack"] += stats["attack_bonus"]
            user_data["defense"] += stats["defense_bonus"]
            user_data["speed"] = stats.get("speed_bonus", 5)  # Default speed 5 if not set
            print(f"\nWelcome, {name} the {choice}! Your adventure begins...")
            break
        print("Invalid class. Try again.")

# Sample villages (added for completeness)
villages = [
    {"name": "Greenwood", "population": 150, "special_items": ["Herbal Potion", "Wooden Bow"]},
    {"name": "Stonehaven", "population": 200, "special_items": ["Iron Sword", "Shield"]},
    {"name": "Riverbend", "population": 120, "special_items": ["Fishing Rod", "Water Flask"]},
    {"name": "Snowpeak", "population": 80, "special_items": ["Warm Cloak", "Ice Pick"]},
    {"name": "Emberfall", "population": 100, "special_items": ["Firestarter", "Lava Stone"]},
    {"name": "Thundercliff", "population": 90, "special_items": ["Lightning Rod", "Storm Cloak"]},
    {"name": "Jade Lotus", "population": 110, "special_items": ["Lotus Blossom", "Jade Pendant"]},
    {"name": "Shogunate of Shirui", "population": 130, "special_items": ["Samurai Armor", "Katana"]},
    {"name": "Long Shui Zhen", "population": 140, "special_items": ["Dragon Scale", "Water Orb"]},
    {"name": "Dragon's Reach", "population": 95, "special_items": ["Dragon Claw", "Dragon Fang"]},
]

biomes = [
{
   "name":"Forest",
   "description":"A lush green area filled with trees and wildlife."
},
{
   "name":"Desert",
   "description":"A vast sandy area with scarce resources."
},
{
   "name":"Cave",
   "description":"A dark underground area with hidden treasures."
},
{
   "name":"Snowy Peaks",
   "description":"A cold mountainous region with snow-covered terrain."
},
{
    "name": "Lava River",
    "description": "A river of molten lava flowing through a rocky landscape."
},
{
    "name": "Plains",
    "description": "A flat, open area with grasslands and few trees."
},
{
   "name":"Swamp",
   "description":"A murky area filled with water and strange creatures."
},
{
   "name":"Ocean",
   "description":"A vast body of water with islands and sea monsters."
},
{
   "name":"Sky Islands",
   "description":"Floating islands high in the sky, accessible by air."
},
{
   "name":"Crystal Caverns",
   "description":"A cave filled with sparkling crystals and rare minerals."
},
{
    "name": "Mines",
    "description": "A network of tunnels and shafts, rich in minerals and ores."
},
{
    "name": "Temple",
    "description": "An ancient structure filled with traps and treasures."
},
{
    "name": "Desert Spring",
    "description": "A hidden refreshing big spring filled with water and strange creatures in depths of the hot desert."
},
{
    "name":"Ancient Ruins",
    "description":"Remnants of a long-lost civilization, filled with secrets and treasures."
},
{
   "name":"Jungle",
   "description":"A dense and tropical area filled with towering trees, exotic plants, and wild animals."
},
{
   "name":"Tundra",
   "description":"A cold, barren landscape with little vegetation, covered in permafrost and snow."
},
{
   "name":"Savannah",
   "description":"A vast grassy plain with scattered trees, home to many herds of animals."
},
{
   "name":"Fungal Forest",
   "description":"A damp, dark forest where giant fungi dominate the landscape instead of trees."
},
{
   "name":"Mountain Range",
   "description":"A towering series of mountains, often with dangerous cliffs and peaks, and home to hardy creatures."
},
{
   "name":"Rainforest",
   "description":"A hot, humid area with dense foliage, continuous rainfall, and diverse wildlife."
},
{
   "name":"Barren Wasteland",
   "description":"An empty, desolate region with little to no life, plagued by sandstorms and harsh winds."
},
{
   "name":"Underwater Ruins",
   "description":"Sunken cities and forgotten structures beneath the ocean, filled with ancient artifacts and dangers."
},
{
   "name":"Meadow",
   "description":"A peaceful, open field filled with colorful flowers, tall grasses, and peaceful wildlife."
},
{
   "name":"Mystic Forest",
   "description":"A magical forest filled with glowing plants, enchanted creatures, and hidden secrets."
},
{
   "name":"Twilight Grove",
   "description":"A mysterious forest where the sun never fully sets, creating a perpetual twilight with bioluminescent plants and glowing creatures."
},
{
   "name":"Corrupted Land",
   "description":"A dark and twisted environment where the very soil is tainted, giving rise to dangerous, mutated creatures and toxic flora."
},
{
   "name":"Icy Wastes",
   "description":"A barren, freezing expanse filled with endless ice fields, glaciers, and the occasional frozen lake hiding ancient secrets."
},
{
   "name":"Oasis",
   "description":"A rare, fertile area in the desert, featuring a small pool of water surrounded by palm trees and desert wildlife."
},
{
   "name":"Lush Highlands",
   "description":"A rolling green landscape with gentle hills, fertile soil, and peaceful wildlife, perfect for farming or settling."
},
{
   "name":"Boreal Forest",
   "description":"A cold and dense forest filled with evergreens and snow, inhabited by resilient wildlife adapted to the harsh conditions."
},
{
   "name":"Sunken Abyss",
   "description":"An underwater trench deep in the ocean, home to strange abyssal creatures and ancient, sunken ruins."
},
{
   "name":"Shroom Cavern",
   "description":"A vast underground network filled with towering mushrooms, glowing spores, and rare fungal lifeforms."
},
{
   "name":"Frostbitten Tundra",
   "description":"An arctic wasteland where the air is frozen, and snowstorms are a constant threat, with dangerous wildlife adapted to the extreme cold."
},
{
   "name":"Radiant Plains",
   "description":"A glowing meadow where flowers and grasses emit light, creating a serene and ethereal landscape filled with beauty and tranquility."
},
{
   "name":"Ashen Wastes",
   "description":"A scorched, desolate plain left behind by ancient fires, where the ground is cracked, and the air is thick with ash and smoke."
},
{
   "name":"Celestial Peaks",
   "description":"Towering mountain ranges that reach beyond the clouds, where the air is thin, and the environment is home to rare celestial beings."
},
{
   "name":"Mystic Marsh",
   "description":"A foggy and swampy area filled with enchanted waters, strange will-o'-the-wisps, and ancient trees with whispered secrets."
},
{
   "name":"Crystal Fields",
   "description":"Vast plains where the earth itself is covered with shimmering crystals, creating a dazzling landscape that’s both beautiful and treacherous."
},
{
   "name":"Vibrant Reef",
   "description":"A colorful underwater biome teeming with vibrant corals, exotic fish, and rare underwater plants, but also home to deadly sea predators."
},
{
   "name":"Sandstorm Flats",
   "description":"A vast desert landscape constantly ravaged by powerful sandstorms, leaving only remnants of ancient structures buried beneath the dunes."
},
{
   "name":"The Nether",
   "description":"A fiery, chaotic dimension filled with volcanic terrain, strange creatures, and hostile environments, with a constant threat of fire and lava."
},
{
   "name":"Skyward Cavern",
   "description":"A network of caves suspended in the sky, connected by floating platforms and filled with rare ores and aerial creatures."
},
{
    "name":"Volcano",
    "description":"A towering mountain with a fiery core, spewing lava and ash, home to fire elementals and rare minerals."
},
{
    "name":"Coast",
    "description":"A sandy beach area with gentle waves, palm trees, and hidden treasures along the shore."
},
{
    "name": "Cliffside",
    "description": "A steep rocky area overlooking the ocean, with hidden caves and dangerous cliffs."
},
{
    "name": "Deep Cave",
    "description": "A dark cave filled with hidden treasures and dangerous creatures."
},
{
    "name": "Dragon's Reach",
    "description": "A mountainous area rumored to once be home to the oldest original dragons,now left only with hidden caves and treasures."
},
{
    "name": "Dragon's peak",
    "description": "A high mountain peak where The great war of human rebellion occurred,where humans killed the last dragon king Frosthymir. Now said to be cursed from all the renmants of the diseased and hatred souls of the dragons who died in that war."
},
{
    "name": "Lotus Pond",
    "description": "A serene pond filled with beautiful lotus flowers, home to rare aquatic creatures and the Koi along with their empress."
},
{
    "name": "Abyssal Ravine",
    "description": "A deep underwater cavern filled with ancient ruins from people that used to inhabit here,with rare conditions met this place can create rare minerals"
},
{
    "name": "Ancient Forest Of Gradanvanka",
    "description": "A dense forest created by the Eternal Gradanvanka when the Eternals, a demigod that lives now in the sky, still walked among mortals in this world."
},
]

# Dismantle items function stub
def dismantle_items() -> None:
    print_header("Dismantling Items")
    print("Dismantling items feature is coming soon!")

# Inventory calculator function stub
def inventory_calculator() -> None:
    print_header("Inventory Calculator")
    print("Inventory calculator feature is coming soon!")

# Show drops function stub
def show_drops() -> None:
    print_header("Monster Drops")
    print("Monster drops feature is coming soon!")

# Show enchants function stub
def show_enchants() -> None:
    print_header("Enchantments")
    print("Enchantments feature is coming soon!")

# Time travel guide function
def time_travel_guide() -> None:
    print_header("Time Travel Guide")
    print("Select a location to travel back in time to:")

    locations = list(LOCATIONS.keys())
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc} - {LOCATIONS[loc]['description']}")

    choice = input("\nEnter the number of the location to time travel to (or 0 to cancel): ")
    try:
        choice = int(choice)
        if choice == 0:
            print("Time travel cancelled.")
            return
        if 1 <= choice <= len(locations):
            destination = locations[choice - 1]
            user_data["current_area"] = destination
            print(f"You have traveled back in time to {destination}!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# Show inventory function stub
def show_inventory() -> None:
    print_header("INVENTORY")
    if not user_data["inventory"]:
        print("Your inventory is empty.")
        return

    # Group items by type
    weapons = []
    armors = []
    accessories = []
    artifacts = []
    potions = []
    misc = []

    for item_name in user_data["inventory"]:
        # Check if this is an item object with details
        if isinstance(item_name, dict):
            item = item_name
            item_name = item["name"]

            if item.get("type") == "weapon":
                weapons.append(item)
            elif item.get("type") == "armor":
                armors.append(item)
            elif item.get("type") == "accessory":
                accessories.append(item)
            elif item.get("type") == "artifact":
                artifacts.append(item)
            elif item.get("type") == "potion":
                potions.append(item)
            else:
                misc.append(item_name)
        else:
            # For simple string items, check against recipes
            if item_name in CRAFTING_RECIPES:
                recipe = CRAFTING_RECIPES[item_name]
                if recipe.get("type") == "weapon":
                    weapons.append(item_name)
                elif recipe.get("type") == "armor":
                    armors.append(item_name)
                elif recipe.get("type") == "accessory":
                    accessories.append(item_name)
                elif recipe.get("type") == "artifact":
                    artifacts.append(item_name)
                else:
                    misc.append(item_name)
            elif item_name in POTION_RECIPES:
                potions.append(item_name)
            else:
                misc.append(item_name)

    # Display sections
    if weapons:
        print(f"\n{BLUE}WEAPONS:{ENDC}")
        for idx, item in enumerate(weapons, 1):
            if isinstance(item, dict):
                level_str = f" (Level {item.get('level', 1)})" if item.get('level', 1) > 1 else ""
                element_str = f" [{item.get('element', 'Nullum')}]" if 'element' in item else ""
                enchant_str = ""
                if "enchantments" in item and item["enchantments"]:
                    enchants = []
                    for name, level in item["enchantments"].items():
                        enchants.append(f"{name} {level}")
                    enchant_str = f" | {', '.join(enchants)}"
                print(f"{idx}. {item['name']}{level_str}{element_str}{enchant_str}")
            else:
                print(f"{idx}. {item}")

    if armors:
        print(f"\n{GREEN}ARMORS:{ENDC}")
        for idx, item in enumerate(armors, 1):
            if isinstance(item, dict):
                level_str = f" (Level {item.get('level', 1)})" if item.get('level', 1) > 1 else ""
                enchant_str = ""
                if "enchantments" in item and item["enchantments"]:
                    enchants = []
                    for name, level in item["enchantments"].items():
                        enchants.append(f"{name} {level}")
                    enchant_str = f" | {', '.join(enchants)}"
                print(f"{idx}. {item['name']}{level_str}{enchant_str}")
            else:
                print(f"{idx}. {item}")

    if accessories:
        print(f"\n{MAGENTA}ACCESSORIES:{ENDC}")
        for idx, item in enumerate(accessories, 1):
            if isinstance(item, dict):
                print(f"{idx}. {item['name']}")
            else:
                print(f"{idx}. {item}")

    if artifacts:
        print(f"\n{YELLOW}ARTIFACTS:{ENDC}")
        for idx, item in enumerate(artifacts, 1):
            if isinstance(item, dict):
                rarity = item.get("rarity", "Common")
                slot = item.get("slot", "")
                rarity_color = ARTIFACT_RARITIES.get(rarity, {}).get("color", "")
                print(f"{idx}. {rarity_color}{item['name']}{ENDC} ({slot})")
            else:
                # Try to get artifact info from recipes
                artifact_info = CRAFTING_RECIPES.get(item, {})
                rarity = artifact_info.get("rarity", "Common")
                slot = artifact_info.get("slot", "")
                rarity_color = ARTIFACT_RARITIES.get(rarity, {}).get("color", "")
                if slot:
                    print(f"{idx}. {rarity_color}{item}{ENDC} ({slot})")
                else:
                    print(f"{idx}. {item}")

    if potions:
        print(f"\n{CYAN}POTIONS:{ENDC}")
        for idx, item in enumerate(potions, 1):
            if isinstance(item, dict):
                print(f"{idx}. {item['name']}")
            else:
                # Try to get potion description from recipes
                potion_info = POTION_RECIPES.get(item, {})
                desc = potion_info.get("description", "")
                if desc:
                    print(f"{idx}. {item} - {desc}")
                else:
                    print(f"{idx}. {item}")

    if misc:
        print(f"\n{ENDC}OTHER ITEMS:{ENDC}")
        for idx, item in enumerate(misc, 1):
            print(f"{idx}. {item}")

    print(f"\nGold: {user_data['gold']}")

    # Display equipped items
    print("\nEquipped:")

    # Weapon
    if user_data.get("equipped", {}).get("weapon"):
        weapon = user_data["equipped"]["weapon"]
        level_str = f" (Level {weapon.get('level', 1)})" if weapon.get('level', 1) > 1 else ""
        element_str = f" [{weapon.get('element', 'Nullum')}]" if 'element' in weapon else ""
        print(f"Weapon: {weapon['name']}{level_str}{element_str}")
    else:
        print("Weapon: None")

    # Armor
    if user_data.get("equipped", {}).get("armor"):
        armor = user_data["equipped"]["armor"]
        level_str = f" (Level {armor.get('level', 1)})" if armor.get('level', 1) > 1 else ""
        print(f"Armor: {armor['name']}{level_str}")
    else:
        print("Armor: None")

    # Accessory
    if user_data.get("equipped", {}).get("accessory"):
        print(f"Accessory: {user_data['equipped']['accessory']['name']}")
    else:
        print("Accessory: None")

    # Artifacts
    print("\nArtifacts:")
    for slot in ARTIFACT_SLOTS:
        slot_key = f"artifact_{slot.lower()}"
        if user_data.get("equipped", {}).get(slot_key):
            artifact = user_data["equipped"][slot_key]
            rarity = artifact.get("rarity", "Common")
            rarity_color = ARTIFACT_RARITIES.get(rarity, {}).get("color", "")
            print(f"{slot}: {rarity_color}{artifact.get('name', 'Unknown')}{ENDC}")
        else:
            print(f"{slot}: None")

# Daily monster function stub
def daily_monster() -> None:
    print_header("Daily Monster")
    monster = random.choice(monsters)
    print(f"Today's monster is: {monster['name']} (Level {monster['level']})")
    print(f"Health: {monster['health']}, Attack: {monster['attack']}")
    print(f"Loot: {', '.join(monster['drops'])}")

# Redeem codes function
def redeem_codes() -> None:
    print_header("Redeemable Codes")
    print("Enter redeemable codes to claim rewards!")
    code = input("Enter code: ").strip()
    if code == "WELCOME2023":
        print("Code accepted! You received 100 gold and 50 experience.")
        user_data["gold"] += 100
        user_data["exp"] += 50
        check_level_up()
    else:
        print("Invalid or expired code.")

# Gambling guide function stub
def gambling_guide() -> None:
    print_header("Gambling Guide")
    print("Gambling feature is coming soon! Play responsibly ;].")

# Duel info function stub
def duel_info() -> None:
    print_header("Duel Info")
    print("Duel feature is coming soon! Challenge your friends.")

# Farming guide function stub
# Farming data structures

# Seasons for crop growing
SEASONS = ["Spring", "Summer", "Fall", "Winter"]

# Current season tracking
if "current_season" not in game_state:
    game_state["current_season"] = "Spring"
    game_state["season_day"] = 1
    game_state["days_per_season"] = 30  # Each season lasts 30 in-game days

CROPS = {
    # Basic Crops
    "Wheat": {
        "growth_time": 2, 
        "yield": "Wheat", 
        "seed_cost": 10, 
        "sell_price": 25, 
        "biome": ["Plains", "Abundant Field"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["stormy", "windy"],
        "seasons": ["Spring", "Summer", "Fall"],
        "tier": "common",
        "description": "A staple grain crop that grows quickly."
    },
    "Corn": {
        "growth_time": 3, 
        "yield": "Corn", 
        "seed_cost": 15, 
        "sell_price": 35, 
        "biome": ["Plains", "Abundant Field"],
        "optimal_weather": ["sunny", "rainy"],
        "weak_weather": ["foggy"],
        "seasons": ["Summer", "Fall"],
        "tier": "common",
        "description": "Tall stalks with yellow kernels. Loves the heat."
    },
    "Tomato": {
        "growth_time": 4, 
        "yield": "Tomato", 
        "seed_cost": 20, 
        "sell_price": 45, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["foggy", "stormy"],
        "seasons": ["Summer"],
        "tier": "common",
        "description": "Red juicy fruits that thrive in warm weather."
    },
    "Potato": {
        "growth_time": 5, 
        "yield": "Potato", 
        "seed_cost": 25, 
        "sell_price": 55, 
        "biome": ["Plains", "Abundant Field"],
        "optimal_weather": ["rainy", "cloudy"],
        "weak_weather": ["sunny"],
        "seasons": ["Spring", "Fall"],
        "tier": "common",
        "description": "Starchy tubers that grow underground."
    },
    "Rice": {
        "growth_time": 6, 
        "yield": "Rice", 
        "seed_cost": 30, 
        "sell_price": 65, 
        "biome": ["Swamp", "Plains"],
        "optimal_weather": ["rainy"],
        "weak_weather": ["sunny", "windy"],
        "seasons": ["Spring", "Summer"],
        "tier": "common",
        "description": "Grows best in waterlogged soil."
    },
    "Carrot": {
        "growth_time": 3, 
        "yield": "Carrot", 
        "seed_cost": 15, 
        "sell_price": 35, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["rainy", "cloudy"],
        "weak_weather": ["stormy"],
        "seasons": ["Spring", "Fall"],
        "tier": "common",
        "description": "Orange root vegetables that grow underground."
    },
    "Lettuce": {
        "growth_time": 2, 
        "yield": "Lettuce", 
        "seed_cost": 10, 
        "sell_price": 25, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["cloudy", "rainy"],
        "weak_weather": ["sunny", "stormy"],
        "seasons": ["Spring", "Fall"],
        "tier": "common",
        "description": "Leafy green vegetable that prefers cool weather."
    },
    "Strawberry": {
        "growth_time": 4, 
        "yield": "Strawberry", 
        "seed_cost": 25, 
        "sell_price": 55, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "rainy"],
        "weak_weather": ["stormy", "foggy"],
        "seasons": ["Spring", "Summer"],
        "tier": "common",
        "description": "Sweet red berries that grow on small plants."
    },

    # New Common Crops
    "Onion": {
        "growth_time": 3, 
        "yield": "Onion", 
        "seed_cost": 15, 
        "sell_price": 40, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["clear", "sunny"],
        "weak_weather": ["rainy", "foggy"],
        "seasons": ["Spring", "Summer"],
        "tier": "common",
        "description": "Layered bulbs with a strong aroma."
    },
    "Pumpkin": {
        "growth_time": 7, 
        "yield": "Pumpkin", 
        "seed_cost": 35, 
        "sell_price": 70, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["stormy", "foggy"],
        "seasons": ["Summer", "Fall"],
        "tier": "common",
        "description": "Large orange gourds that grow on sprawling vines."
    },
    "Cabbage": {
        "growth_time": 5, 
        "yield": "Cabbage", 
        "seed_cost": 20, 
        "sell_price": 50, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["cloudy", "rainy"],
        "weak_weather": ["sunny", "windy"],
        "seasons": ["Spring", "Fall"],
        "tier": "common",
        "description": "Dense leafy heads that prefer cooler weather."
    },
    "Eggplant": {
        "growth_time": 6, 
        "yield": "Eggplant", 
        "seed_cost": 30, 
        "sell_price": 60,
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["foggy", "windy"],
        "seasons": ["Summer"],
        "tier": "common",
        "description": "Purple fruits with a meaty texture."
    },

    # Uncommon Crops
    "Watermelon": {
        "growth_time": 8, 
        "yield": "Watermelon", 
        "seed_cost": 45, 
        "sell_price": 90, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "rainy"],
        "weak_weather": ["windy", "foggy"],
        "seasons": ["Summer"],
        "tier": "uncommon",
        "description": "Large, juicy fruits with red flesh and black seeds."
    },
    "Pineapple": {
        "growth_time": 10, 
        "yield": "Pineapple", 
        "seed_cost": 60, 
        "sell_price": 120, 
        "biome": ["Plains", "Tropical Beach"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["cloudy", "foggy"],
        "seasons": ["Summer"],
        "tier": "uncommon",
        "description": "Spiky tropical fruits with sweet yellow flesh."
    },
    "Sunflower": {
        "growth_time": 6, 
        "yield": "Sunflower Seeds", 
        "seed_cost": 40, 
        "sell_price": 85, 
        "biome": ["Plains", "Abundant Field"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["stormy", "windy"],
        "seasons": ["Summer", "Fall"],
        "tier": "uncommon",
        "description": "Tall flowers with edible seeds that follow the sun."
    },
    "Grape": {
        "growth_time": 9, 
        "yield": "Grapes", 
        "seed_cost": 55, 
        "sell_price": 110, 
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["stormy", "foggy"],
        "seasons": ["Summer", "Fall"],
        "tier": "uncommon",
        "description": "Clusters of small fruits that grow on vines."
    },

    # Special Crops
    "Golden Wheat": {
        "growth_time": 8, 
        "yield": "Golden Wheat", 
        "seed_cost": 100, 
        "sell_price": 250, 
        "biome": ["Plains", "Mystic Forest"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["stormy", "foggy"],
        "seasons": ["Summer", "Fall"],
        "tier": "rare",
        "description": "Magical grain that glows with a golden light."
    },
    "Magic Beans": {
        "growth_time": 10, 
        "yield": "Magic Beans", 
        "seed_cost": 150, 
        "sell_price": 300, 
        "biome": ["Mystic Forest"],
        "optimal_weather": ["rainy", "foggy"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Spring", "Fall"],
        "tier": "rare",
        "description": "Mystical beans that may grow into something extraordinary."
    },
    "Dragon Fruit": {
        "growth_time": 12, 
        "yield": "Dragon Fruit", 
        "seed_cost": 200, 
        "sell_price": 450, 
        "biome": ["Dragon's Peak"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["rainy", "foggy"],
        "seasons": ["Summer"],
        "tier": "epic",
        "description": "Exotic fruits with fiery properties."
    },
    "Moonflower": {
        "growth_time": 6, 
        "yield": "Moonflower", 
        "seed_cost": 80, 
        "sell_price": 200, 
        "biome": ["Moonveil Harbor"],
        "optimal_weather": ["foggy", "cloudy"],
        "weak_weather": ["sunny", "stormy"],
        "seasons": ["Spring", "Fall"],
        "tier": "rare",
        "description": "Silver flowers that bloom under moonlight."
    },
    "Frost Berries": {
        "growth_time": 5, 
        "yield": "Frost Berries", 
        "seed_cost": 90, 
        "sell_price": 220, 
        "biome": ["Frostvale"],
        "optimal_weather": ["cloudy", "foggy"],
        "weak_weather": ["sunny", "rainy"],
        "seasons": ["Winter"],
        "tier": "rare",
        "description": "Icy blue berries that remain frozen even in warm weather."
    },
    "Fire Peppers": {
        "growth_time": 7, 
        "yield": "Fire Peppers", 
        "seed_cost": 120, 
        "sell_price": 280, 
        "biome": ["Ember Hollow"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["rainy", "foggy"],
        "seasons": ["Summer"],
        "tier": "rare",
        "description": "Intensely hot peppers that occasionally emit sparks."
    },
    "Shadow Root": {
        "growth_time": 9, 
        "yield": "Shadow Root", 
        "seed_cost": 130, 
        "sell_price": 290, 
        "biome": ["Shadowmere"],
        "optimal_weather": ["foggy", "cloudy"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Fall", "Winter"],
        "tier": "rare",
        "description": "Mysterious roots that seem to absorb light."
    },
    "Crystal Bloom": {
        "growth_time": 11, 
        "yield": "Crystal Bloom", 
        "seed_cost": 180, 
        "sell_price": 400, 
        "biome": ["Crystal Cave"],
        "optimal_weather": ["clear", "foggy"],
        "weak_weather": ["stormy", "rainy"],
        "seasons": ["Winter", "Spring"],
        "tier": "epic",
        "description": "Flowers with petals that resemble translucent crystals."
    },

    # Dimension-Specific Crops
    "Cosmic Lotus": {
        "growth_time": 15, 
        "yield": "Cosmic Lotus", 
        "seed_cost": 300, 
        "sell_price": 750, 
        "biome": ["Celestial Realm"],
        "optimal_weather": ["Cosmic Rain", "Celestial Harmony"],
        "weak_weather": ["clear", "foggy"],
        "seasons": ["All"],
        "tier": "legendary",
        "description": "A mystical flower that contains the essence of stars."
    },
    "Void Mushroom": {
        "growth_time": 12, 
        "yield": "Void Mushroom", 
        "seed_cost": 250, 
        "sell_price": 600, 
        "biome": ["Shadow Realm"],
        "optimal_weather": ["Darkness Storm", "Void Mist"],
        "weak_weather": ["sunny", "rainy"],
        "seasons": ["All"],
        "tier": "epic",
        "description": "Fungus that thrives in complete darkness."
    },
    "Elemental Orchid": {
        "growth_time": 14, 
        "yield": "Elemental Essence", 
        "seed_cost": 280, 
        "sell_price": 700, 
        "biome": ["Elemental Plane"],
        "optimal_weather": ["Elemental Surge", "Primal Storm"],
        "weak_weather": ["cloudy", "foggy"],
        "seasons": ["All"],
        "tier": "epic",
        "description": "A flower that changes color based on the dominant element."
    },
    "Timeless Herb": {
        "growth_time": 10, 
        "yield": "Timeless Herb", 
        "seed_cost": 230, 
        "sell_price": 550, 
        "biome": ["Ancient Ruins"],
        "optimal_weather": ["Time Flux", "Arcane Winds"],
        "weak_weather": ["stormy", "windy"],
        "seasons": ["All"],
        "tier": "rare",
        "description": "An herb that seems to exist in multiple time periods at once."
    },
    
    # Rare Crops
    "Phoenix Flower": {
        "growth_time": 15, 
        "yield": "Phoenix Flower", 
        "seed_cost": 500, 
        "sell_price": 1200, 
        "biome": ["Silent Ashes"],
        "optimal_weather": ["clear", "sunny"],
        "weak_weather": ["rainy", "foggy"],
        "seasons": ["Summer"],
        "tier": "legendary",
        "description": "A flower that burns with eternal flame."
    },
    "Dragon's Breath Plant": {
        "growth_time": 20, 
        "yield": "Dragon's Breath", 
        "seed_cost": 800, 
        "sell_price": 2000, 
        "biome": ["Dragon's Peak"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["rainy", "foggy"],
        "seasons": ["Summer"],
        "tier": "legendary",
        "description": "A plant that exhales wisps of dragonfire."
    },
    "Celestial Herb": {
        "growth_time": 18, 
        "yield": "Celestial Herb", 
        "seed_cost": 600, 
        "sell_price": 1500, 
        "biome": ["Celestial Peaks"],
        "optimal_weather": ["clear", "Celestial Harmony"],
        "weak_weather": ["stormy", "windy"],
        "seasons": ["Spring", "Summer"],
        "tier": "legendary",
        "description": "A mythical herb that radiates celestial energy."
    },
    "Void Lotus": {
        "growth_time": 25, 
        "yield": "Void Lotus", 
        "seed_cost": 1000, 
        "sell_price": 2500, 
        "biome": ["Crimson Abyss"],
        "optimal_weather": ["foggy", "Void Mist"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Winter", "Fall"],
        "tier": "legendary",
        "description": "A lotus that blooms in the darkest void, absorbing all light around it."
    },

    # Seasonal Specialty Crops
    "Winter Mint": {
        "growth_time": 8,
        "yield": "Winter Mint",
        "seed_cost": 75,
        "sell_price": 180,
        "biome": ["Frost Plains", "Garden"],
        "optimal_weather": ["snowy", "cloudy"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Winter"],
        "tier": "uncommon",
        "description": "Frosty blue leaves with a cooling effect. Thrives in winter."
    },
    "Autumn Squash": {
        "growth_time": 7,
        "yield": "Autumn Squash",
        "seed_cost": 40,
        "sell_price": 90,
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["cloudy", "clear"],
        "weak_weather": ["stormy", "foggy"],
        "seasons": ["Fall"],
        "tier": "uncommon",
        "description": "Rich, colorful gourds that store well through winter."
    },
    "Spring Tulips": {
        "growth_time": 4,
        "yield": "Spring Tulips",
        "seed_cost": 30,
        "sell_price": 75,
        "biome": ["Garden", "Meadow"],
        "optimal_weather": ["rainy", "cloudy"],
        "weak_weather": ["stormy", "windy"],
        "seasons": ["Spring"],
        "tier": "uncommon",
        "description": "Colorful spring flowers that symbolize renewal."
    },
    "Summer Melon": {
        "growth_time": 9,
        "yield": "Summer Melon",
        "seed_cost": 50,
        "sell_price": 120,
        "biome": ["Plains", "Garden"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["foggy", "cloudy"],
        "seasons": ["Summer"],
        "tier": "uncommon",
        "description": "Sweet, juicy melons that love hot weather."
    },
    
    # Weather-Dependent Rare Crops
    "Ghost Pepper": {
        "growth_time": 12,
        "yield": "Ghost Pepper",
        "seed_cost": 100,
        "sell_price": 250,
        "biome": ["Volcanic Plains", "Desert"],
        "optimal_weather": ["sunny", "clear"],
        "weak_weather": ["rainy", "cloudy"],
        "seasons": ["Summer", "Fall"],
        "tier": "rare",
        "description": "Extremely spicy peppers that seem to glow at night."
    },
    "Frost Lotus": {
        "growth_time": 14,
        "yield": "Frost Lotus",
        "seed_cost": 120,
        "sell_price": 280,
        "biome": ["Frost Plains", "Mountain"],
        "optimal_weather": ["snowy", "foggy"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Winter"],
        "tier": "rare",
        "description": "Ice-blue flowers that only bloom in freezing conditions."
    },
    "Thunderroot": {
        "growth_time": 11,
        "yield": "Thunderroot",
        "seed_cost": 110,
        "sell_price": 260,
        "biome": ["Plains", "Storm Fields"],
        "optimal_weather": ["stormy", "rainy"],
        "weak_weather": ["sunny", "clear"],
        "seasons": ["Spring", "Fall"],
        "tier": "rare",
        "description": "Roots that absorb electrical energy during storms."
    }
}

def cook_food() -> None:
    """Function to cook food with a chance of failure"""
    print_header("Cooking Station")
    
    # Check if the player is at a suitable location or has the right equipment
    if "camp" not in user_data or "Kitchen" not in user_data.get("camp", {}).get("structures", {}):
        if user_data["current_area"] not in ["Greenwood Village", "Stormhaven", "Dragon's Peak"]:
            print_colored("You need to be in a village with a kitchen or have a Kitchen in your camp to cook!", FAIL)
            return
    
    # Display available recipes
    print_colored("Available Recipes:", HEADER)
    available_recipes = []
    
    for recipe_name, recipe_data in COOKING_RECIPES.items():
        # Check if player has the ingredients
        has_ingredients = True
        missing_ingredients = {}
        
        for ingredient, amount in recipe_data["ingredients"].items():
            if ingredient not in user_data.get("materials", {}) or user_data.get("materials", {}).get(ingredient, 0) < amount:
                has_ingredients = False
                current_amount = user_data.get("materials", {}).get(ingredient, 0)
                missing_ingredients[ingredient] = amount - current_amount
        
        # Display recipe with color based on availability
        color = GREEN if has_ingredients else RED
        print_colored(f"{recipe_name} - {recipe_data['description']}", color)
        
        if has_ingredients:
            available_recipes.append(recipe_name)
            print_colored("  Ingredients: ", YELLOW, end="")
            for ingredient, amount in recipe_data["ingredients"].items():
                print(f"{ingredient} x{amount}", end=", ")
            print()
            print_colored(f"  Difficulty: {recipe_data['difficulty']} | Fail Chance: {int(recipe_data['fail_chance'] * 100)}%", YELLOW)
            print_colored(f"  Restores: {recipe_data.get('health_restore', 0)} HP, {recipe_data.get('stamina_restore', 0)} Stamina", BLUE)
            if "buffs" in recipe_data:
                print_colored("  Buffs: ", BLUE, end="")
                for buff, value in recipe_data["buffs"].items():
                    print(f"{buff.replace('_', ' ').title()} +{value}", end=", ")
                print()
        else:
            print_colored("  Missing ingredients: ", RED, end="")
            for ingredient, amount in missing_ingredients.items():
                print(f"{ingredient} x{amount}", end=", ")
            print()
    
    if not available_recipes:
        print_colored("\nYou don't have ingredients for any recipes. Try gathering more materials!", WARNING)
        return
    
    # Recipe selection
    print()
    recipe_choice = input("What would you like to cook? (or press Enter to cancel): ")
    
    if not recipe_choice:
        return
    
    if recipe_choice not in COOKING_RECIPES:
        print_colored("That recipe doesn't exist!", FAIL)
        return
    
    if recipe_choice not in available_recipes:
        print_colored("You don't have the ingredients for that recipe!", FAIL)
        return
    
    selected_recipe = COOKING_RECIPES[recipe_choice]
    
    # Remove ingredients from inventory
    for ingredient, amount in selected_recipe["ingredients"].items():
        user_data["materials"][ingredient] -= amount
        if user_data["materials"][ingredient] <= 0:
            del user_data["materials"][ingredient]
    
    # Cooking animation
    print_colored("\nCooking in progress...", YELLOW)
    cook_time = selected_recipe.get("cook_time", 3)
    for i in range(cook_time):
        time.sleep(0.5)
        print_colored("🔥" * (i+1), YELLOW)
    
    # Determine success or failure based on difficulty
    difficulty = selected_recipe["difficulty"]
    fail_chance = selected_recipe["fail_chance"]
    
    # Profession bonus - reduce fail chance for Chefs
    if user_data.get("profession") == "Chef":
        fail_chance = max(0.01, fail_chance - 0.1)  # Minimum 1% chance to fail
        print_colored("Your Chef skills improve your chances of success!", GREEN)
    
    # Roll for success
    if random.random() < fail_chance:
        # Cooking failed
        failed_result = FAILED_COOKING[difficulty]
        print_colored(f"\nOh no! Your {recipe_choice} turned into a {failed_result['name']}!", FAIL)
        print_colored(f"{failed_result['description']}", WARNING)
        
        # Add failed result to inventory
        if failed_result["name"] not in user_data["inventory"]:
            user_data["inventory"][failed_result["name"]] = 0
        user_data["inventory"][failed_result["name"]] += 1
        
        # Small XP gain even for failure
        exp_gain = int(selected_recipe["experience"] * 0.3)
        user_data["exp"] += exp_gain
        print_colored(f"You gained {exp_gain} experience from the attempt.", BLUE)
    else:
        # Cooking succeeded
        print_colored(f"\nSuccess! You've cooked a delicious {recipe_choice}!", SUCCESS)
        
        # Add food to inventory
        if recipe_choice not in user_data["inventory"]:
            user_data["inventory"][recipe_choice] = 0
        user_data["inventory"][recipe_choice] += 1
        
        # XP gain
        exp_gain = selected_recipe["experience"]
        user_data["exp"] += exp_gain
        print_colored(f"You gained {exp_gain} experience!", BLUE)
        
        # Chance for bonus food with Chef profession
        if user_data.get("profession") == "Chef" and random.random() < 0.25:
            user_data["inventory"][recipe_choice] += 1
            print_colored("Your Chef skills allowed you to cook an extra portion!", SUCCESS)
    
    # Check for level up
    check_level_up()
    
    # Add cooking achievements
    if "cooking_stats" not in user_data:
        user_data["cooking_stats"] = {"dishes_cooked": 0, "failures": 0, "by_difficulty": {}}
    
    if random.random() < fail_chance:
        user_data["cooking_stats"]["failures"] += 1
    else:
        user_data["cooking_stats"]["dishes_cooked"] += 1
        
    if difficulty not in user_data["cooking_stats"]["by_difficulty"]:
        user_data["cooking_stats"]["by_difficulty"][difficulty] = 0
    user_data["cooking_stats"]["by_difficulty"][difficulty] += 1
    
    # Check cooking achievements
    if user_data["cooking_stats"]["dishes_cooked"] >= 10:
        achievement_name = "Amateur Chef"
        grant_achievement_rewards({"name": achievement_name, "rewards": {"exp": 100, "gold": 50}})
    
    if user_data["cooking_stats"]["dishes_cooked"] >= 50:
        achievement_name = "Experienced Cook"
        grant_achievement_rewards({"name": achievement_name, "rewards": {"exp": 300, "gold": 150}})
    
    if user_data["cooking_stats"]["by_difficulty"].get("hard", 0) >= 20:
        achievement_name = "Master Chef"
        grant_achievement_rewards({"name": achievement_name, "rewards": {"exp": 500, "gold": 300}})

def farming_guide() -> None:
    print_header("Farming")

    # Initialize farming data if not present
    if "farming" not in user_data:
        user_data["farming"] = {
            "plots": {},  # Store planted crops
            "growth": {},  # Store growth progress
            "unlocked_plots": 3  # Start with 3 plots
        }

    while True:
        # Show farm status
        print_colored("\n=== Your Farm ===", GREEN)
        print(f"Gold: {user_data['gold']}")
        print(f"Plots available: {user_data['farming']['unlocked_plots']} (Used: {len(user_data['farming']['plots'])})")

        print("\nActions:")
        print("1. View crop prices and info")
        print("2. Buy seeds")
        print("3. Plant crops")
        print("4. View farm")
        print("5. Harvest crops")
        print("6. Sell crops")
        print("7. Upgrade farm")
        print("8. Exit farming")

        choice = input("\nChoose action (1-8): ")

        if choice == "1":
            print_colored("\n=== Crop Information ===", CYAN)
            print_colored(f"Current Season: {game_state['current_season']}", YELLOW)
            print_colored(f"Current Weather: {get_weather_name()}", game_state.get("current_weather_color", CYAN))
            print()
            
            # Allow filtering by tier
            print("Filter by tier:")
            print("1. All Crops")
            print("2. Common Crops")
            print("3. Uncommon Crops")
            print("4. Rare Crops")
            print("5. Epic Crops")
            print("6. Legendary Crops")
            print("7. Seasonal Crops (current season)")
            
            tier_filter = input("\nChoose filter (1-7, default 1): ").strip()
            
            # Default to all crops
            if not tier_filter or tier_filter not in "1234567":
                tier_filter = "1"
            
            filtered_crops = {}
            current_season = game_state['current_season']
            
            for crop, info in CROPS.items():
                # Apply filters
                if tier_filter == "2" and info.get("tier") != "common":
                    continue
                elif tier_filter == "3" and info.get("tier") != "uncommon":
                    continue
                elif tier_filter == "4" and info.get("tier") != "rare":
                    continue
                elif tier_filter == "5" and info.get("tier") != "epic":
                    continue
                elif tier_filter == "6" and info.get("tier") != "legendary":
                    continue
                elif tier_filter == "7" and current_season not in info.get("seasons", []) and "All" not in info.get("seasons", []):
                    continue
                    
                filtered_crops[crop] = info
            
            # Get tiers for color coding
            tier_colors = {
                "common": WHITE,
                "uncommon": GREEN,
                "rare": BLUE,
                "epic": PURPLE,
                "legendary": YELLOW
            }
            
            # Display filtered crops
            for crop, info in filtered_crops.items():
                tier = info.get("tier", "common")
                tier_color = tier_colors.get(tier, WHITE)
                
                print_colored(f"\n{crop} ({tier.capitalize()}):", tier_color)
                print(f"  Description: {info.get('description', 'No description available')}")
                print(f"  Growth Time: {info['growth_time']} cycles")
                print(f"  Seed Cost: {info['seed_cost']} gold")
                print(f"  Market Price: {info['sell_price']} gold")
                
                # Display seasonal information
                seasons = info.get("seasons", [])
                if "All" in seasons:
                    print_colored("  Seasons: All seasons", OKGREEN)
                else:
                    season_str = ", ".join(seasons)
                    season_color = OKGREEN if current_season in seasons else FAIL
                    print_colored(f"  Seasons: {season_str}", season_color)
                
                # Display weather preferences
                optimal_weather = info.get("optimal_weather", [])
                weak_weather = info.get("weak_weather", [])
                
                current_weather = game_state["current_weather"]
                
                optimal_str = ", ".join(optimal_weather)
                weak_str = ", ".join(weak_weather)
                
                optimal_color = OKGREEN if current_weather in optimal_weather else LIGHTGRAY
                weak_color = FAIL if current_weather in weak_weather else LIGHTGRAY
                
                print_colored(f"  Optimal Weather: {optimal_str}", optimal_color)
                print_colored(f"  Weak Weather: {weak_str}", weak_color)
                
                # Show where crop can be grown
                biomes = info.get("biome", [])
                print(f"  Biomes: {', '.join(biomes)}")
                print(f"  Profit per crop: {info['sell_price'] - info['seed_cost']} gold")

        elif choice == "2":
            print_colored("\n=== Seed Shop ===", YELLOW)
            print("Available seeds:")
            for crop, info in CROPS.items():
                print(f"{crop} seeds: {info['seed_cost']} gold")

            seed = input("\nWhich seeds would you like to buy? (or Enter to cancel): ").capitalize()
            if seed in CROPS:
                amount = input("How many? ")
                try:
                    amount = int(amount)
                    total_cost = CROPS[seed]["seed_cost"] * amount
                    if total_cost <= user_data["gold"]:
                        user_data["gold"] -= total_cost
                        seed_name = f"{seed} seeds"
                        if seed_name not in user_data["materials"]:
                            user_data["materials"][seed_name] = 0
                        user_data["materials"][seed_name] += amount
                        print_colored(f"Bought {amount} {seed} seeds for {total_cost} gold!", GREEN)
                    else:
                        print_colored("Not enough gold!", RED)
                except ValueError:
                    print_colored("Please enter a valid number.", RED)

        elif choice == "3":
            print_colored("\n=== Plant Crops ===", GREEN)
            print_colored(f"Current Season: {game_state['current_season']}", YELLOW)
            print_colored(f"Current Weather: {get_weather_name()}", game_state.get("current_weather_color", CYAN))
            
            seeds = [mat for mat in user_data["materials"] if mat.endswith(" seeds")]

            if not seeds:
                print_colored("You don't have any seeds!", RED)
                continue

            # Get current season for showing compatibility
            current_season = game_state["current_season"]
            
            print("\nYour seeds:")
            for seed in seeds:
                # Get the actual crop name
                crop_name = seed.replace(" seeds", "")
                if crop_name in CROPS:
                    crop_data = CROPS[crop_name]
                    # Check if it's compatible with the current season
                    crop_seasons = crop_data.get("seasons", [])
                    if "All" in crop_seasons or current_season in crop_seasons:
                        seasons_color = OKGREEN
                        season_note = "(In season)"
                    else:
                        seasons_color = FAIL
                        season_note = "(Out of season - grows slower)"
                    
                    # Show the seed with color-coded seasonal information
                    print(f"{seed}: {user_data['materials'][seed]} ", end="")
                    print_colored(season_note, seasons_color)
                else:
                    # Legacy seed without seasonal data
                    print(f"{seed}: {user_data['materials'][seed]}")

            if len(user_data["farming"]["plots"]) >= user_data["farming"]["unlocked_plots"]:
                print_colored("All plots are occupied! Harvest some crops or upgrade your farm.", RED)
                continue

            seed = input("\nWhich seeds would you like to plant? (or Enter to cancel): ")
            if seed in seeds:
                crop_name = seed.replace(" seeds", "")
                crop_data = CROPS.get(crop_name, {})
                
                # Check season compatibility and warn player if needed
                if crop_name in CROPS:
                    crop_seasons = crop_data.get("seasons", [])
                    if "All" not in crop_seasons and current_season not in crop_seasons:
                        print_colored("WARNING: This crop is out of season and will grow much slower!", YELLOW)
                        confirm = input("Do you still want to plant it? (y/n): ").lower()
                        if confirm != 'y':
                            continue
                
                available_plots = user_data["farming"]["unlocked_plots"] - len(user_data["farming"]["plots"])
                amount = input(f"How many? (max {min(user_data['materials'][seed], available_plots)}): ")

                try:
                    amount = int(amount)
                    if amount > 0 and amount <= user_data["materials"][seed] and amount <= available_plots:
                        # Display growth estimate based on weather and season
                        if crop_name in CROPS:
                            # Calculate modifiers
                            current_weather = game_state["current_weather"]
                            general_weather_modifier = game_state.get("current_weather_crop_modifier", 1.0)
                            
                            # Get seasons for this crop
                            crop_seasons = crop_data.get("seasons", [])
                            
                            season_modifier = 1.0
                            if "All" in crop_seasons:
                                season_modifier = 1.2
                            elif current_season in crop_seasons:
                                season_modifier = 1.2  
                            else:
                                season_modifier = 0.5
                                
                            weather_bonus = 1.0
                            if current_weather in crop_data.get("optimal_weather", []):
                                weather_bonus = 1.3
                            elif current_weather in crop_data.get("weak_weather", []):
                                weather_bonus = 0.7
                                
                            total_modifier = general_weather_modifier * season_modifier * weather_bonus
                            days_estimate = int(crop_data["growth_time"] / total_modifier)
                            
                            print_colored(f"Estimated growth time: {days_estimate} days", CYAN)
                            
                            if total_modifier > 1.0:
                                print_colored("Current conditions are favorable for this crop!", OKGREEN)
                            elif total_modifier < 0.8:
                                print_colored("Current conditions are poor for this crop. Consider planting something else.", YELLOW)
                        
                        # Plant the crops
                        for _ in range(amount):
                            plot_id = str(len(user_data["farming"]["plots"]))
                            user_data["farming"]["plots"][plot_id] = crop_name
                            user_data["farming"]["growth"][plot_id] = 0
                        user_data["materials"][seed] -= amount
                        if user_data["materials"][seed] <= 0:
                            del user_data["materials"][seed]
                        print_colored(f"Planted {amount} {crop_name}!", GREEN)
                    else:
                        print_colored("Invalid amount!", RED)
                except ValueError:
                    print_colored("Please enter a valid number.", RED)

        elif choice == "4":
            print_colored("\n=== Farm Status ===", CYAN)
            print_colored(f"Current Season: {game_state['current_season']}", YELLOW)
            print_colored(f"Current Weather: {get_weather_name()}", game_state.get("current_weather_color", CYAN))
            print_colored(f"Weather Description: {get_weather_description()}", LIGHTGRAY)
            print()
            
            if not user_data["farming"]["plots"]:
                print("No crops planted!")
                continue

            # Calculate total growth modifiers for display
            current_weather = game_state["current_weather"]
            current_season = game_state["current_season"]
            general_weather_modifier = game_state.get("current_weather_crop_modifier", 1.0)
            
            for plot, crop in user_data["farming"]["plots"].items():
                crop_data = CROPS.get(crop, {})
                
                # Get growth progress
                growth = user_data["farming"]["growth"][plot]
                max_growth = crop_data["growth_time"] * TICKS_PER_DAY // 10  # Scale growth time to ticks
                
                # Calculate modifiers
                season_modifier = 1.0
                crop_seasons = crop_data.get("seasons", [])
                
                if "All" in crop_seasons:
                    season_modifier = 1.2
                elif current_season in crop_seasons:
                    season_modifier = 1.2
                else:
                    season_modifier = 0.5
                    
                weather_bonus = 1.0
                if current_weather in crop_data.get("optimal_weather", []):
                    weather_bonus = 1.3
                elif current_weather in crop_data.get("weak_weather", []):
                    weather_bonus = 0.7
                    
                total_modifier = general_weather_modifier * season_modifier * weather_bonus
                modifier_percent = int((total_modifier - 1.0) * 100)
                
                # Determine status and color
                if growth >= max_growth:
                    status = "✨ Ready to harvest!"
                    status_color = OKGREEN
                else:
                    percent_complete = min(int((growth / max_growth) * 100), 99)
                    growth_icon = "🌱" if percent_complete < 33 else "🌿" if percent_complete < 66 else "🌾"
                    status = f"{growth_icon} Growing... {percent_complete}% complete"
                    status_color = YELLOW
                
                # Show crop tier with appropriate color
                tier = crop_data.get("tier", "common").capitalize()
                tier_colors = {
                    "Common": WHITE,
                    "Uncommon": GREEN,
                    "Rare": BLUE,
                    "Epic": PURPLE,
                    "Legendary": YELLOW
                }
                tier_color = tier_colors.get(tier, WHITE)
                
                # Display the crop info
                print_colored(f"Plot {plot}: ", CYAN, end="")
                print_colored(f"{status} ", status_color, end="")
                print_colored(f"{crop} ", tier_color, end="")
                print(f"({growth}/{max_growth} ticks)")
                
                # Show growth modifiers
                modifier_color = OKGREEN if modifier_percent > 0 else (FAIL if modifier_percent < 0 else WHITE)
                modifier_sign = "+" if modifier_percent > 0 else ""
                print_colored(f"  Growth Rate: {modifier_sign}{modifier_percent}% ", modifier_color, end="")
                
                # Show weather and season effects
                if current_weather in crop_data.get("optimal_weather", []):
                    print_colored("(Optimal weather) ", OKGREEN, end="")
                elif current_weather in crop_data.get("weak_weather", []):
                    print_colored("(Unfavorable weather) ", FAIL, end="")
                    
                if current_season in crop_seasons:
                    print_colored("(Good season) ", OKGREEN)
                elif "All" in crop_seasons:
                    print_colored("(Grows in all seasons) ", OKGREEN)
                else:
                    print_colored("(Wrong season) ", FAIL)

        elif choice == "5":
            print_colored("\n=== Harvest Crops ===", YELLOW)
            harvested = False
            for plot, crop in list(user_data["farming"]["plots"].items()):
                if user_data["farming"]["growth"][plot] >= CROPS[crop]["growth_time"]:
                    harvested = True
                    yield_amount = random.randint(1, 3)
                    if crop not in user_data["materials"]:
                        user_data["materials"][crop] = 0
                    user_data["materials"][crop] += yield_amount

                    # Remove harvested crop
                    del user_data["farming"]["plots"][plot]
                    del user_data["farming"]["growth"][plot]

                    print_colored(f"Harvested {yield_amount}x {crop} from plot {plot}!", GREEN)

            if not harvested:
                print_colored("No crops ready to harvest!", RED)

        elif choice == "6":
            print_colored("\n=== Sell Crops ===", YELLOW)
            crops_to_sell = [crop for crop in user_data["materials"] if crop in CROPS]

            if not crops_to_sell:
                print_colored("You have no crops to sell!", RED)
                continue

            print("\nYour crops:")
            for crop in crops_to_sell:
                print(f"{crop}: {user_data['materials'][crop]} (Worth: {CROPS[crop]['sell_price']} gold each)")

            crop = input("\nWhat would you like to sell? (or Enter to cancel): ")
            if crop in crops_to_sell:
                amount = input(f"How many? (max {user_data['materials'][crop]}): ")
                try:
                    amount = int(amount)
                    if 0 < amount <= user_data["materials"][crop]:
                        total_price = CROPS[crop]["sell_price"] * amount
                        user_data["materials"][crop] -= amount
                        if user_data["materials"][crop] <= 0:
                            del user_data["materials"][crop]
                        user_data["gold"] += total_price
                        print_colored(f"Sold {amount}x {crop} for {total_price} gold!", GREEN)
                    else:
                        print_colored("Invalid amount!", RED)
                except ValueError:
                    print_colored("Please enter a valid number.", RED)

        elif choice == "7":
            print_colored("\n=== Farm Upgrades ===", MAGENTA)
            upgrade_cost = 1000 * (user_data["farming"]["unlocked_plots"] - 2)
            print(f"Upgrade cost for new plot: {upgrade_cost} gold")

            if input("Would you like to upgrade? (y/n): ").lower() == 'y':
                if user_data["gold"] >= upgrade_cost:
                    user_data["gold"] -= upgrade_cost
                    user_data["farming"]["unlocked_plots"] += 1
                    print_colored(f"Farm upgraded! You now have {user_data['farming']['unlocked_plots']} plots!", GREEN)
                else:
                    print_colored("Not enough gold!", RED)

        elif choice == "8":
            break

        # Progress growth for all planted crops
        for plot in user_data["farming"]["growth"]:
            user_data["farming"]["growth"][plot] += 1

# Horse festival function (added for completeness)
# Horse festival function removed as it was not useful

# New function for gathering materials
def gather_materials(area: str) -> None:
    # Fix check to see if area is in any MATERIALS areas list
    if not any(area in mat["areas"] for mat in MATERIALS.values()):
        print(f"No materials can be gathered in {area}")
        return

    available_materials = [name for name, info in MATERIALS.items() if area in info["areas"]]
    print(f"\nAvailable materials in {area}:")
    for i, mat in enumerate(available_materials, 1):
        tool_req = MATERIALS[mat]["tool_required"]
        print(f"{i}. {mat} {'(Requires: ' + tool_req + ')' if tool_req else ''}")

    choice = input("\nChoose material to gather (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(available_materials):
            material = available_materials[choice - 1]
            tool_required = MATERIALS[material]["tool_required"]

            if tool_required and tool_required not in user_data["tools"]:
                print(f"You need a {tool_required} to gather {material}")
                return

            amount = random.randint(1, 3)
            user_data["materials"][material] = user_data["materials"].get(material, 0) + amount
            print(f"Gathered {amount} {material}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def craft_item() -> None:
    print_header("Crafting")
    
    # Get player's profession for crafting bonuses
    player_profession = user_data.get("profession", None)
    crafting_bonus = 0
    profession_specializations = user_data.get("profession_specializations", {})
    
    # Apply profession bonuses if applicable
    if player_profession in ["Blacksmith", "Alchemist", "Tailor", "Artificer"]:
        crafting_bonus = 10  # Base 10% bonus for crafting professions
        
        # Apply specialization bonuses
        if player_profession == "Blacksmith" and profession_specializations.get("Master Weaponsmith", False):
            crafting_bonus += 15  # Additional 15% for weapon crafting
        elif player_profession == "Alchemist" and profession_specializations.get("Potion Master", False):
            crafting_bonus += 15  # Additional 15% for potion crafting
        elif player_profession == "Tailor" and profession_specializations.get("Master Outfitter", False):
            crafting_bonus += 15  # Additional 15% for armor crafting
        elif player_profession == "Artificer" and profession_specializations.get("Arcane Engineer", False):
            crafting_bonus += 15  # Additional 15% for magical item crafting
    
    # Filter recipes by type option
    crafting_categories = {
        "1": ("Weapons", "weapon"),
        "2": ("Armor", "armor"),
        "3": ("Tools", "tool"),
        "4": ("Accessories", "accessory"),
        "5": ("Materials", "material"),
        "6": ("All Items", None)
    }
    
    print("\nCrafting Categories:")
    for key, (name, _) in crafting_categories.items():
        print(f"{key}. {name}")
    
    category_choice = input("\nChoose a category (number) or press Enter for all: ").strip()
    if not category_choice:
        category_choice = "6"  # Default to All Items
    
    # Get the category filter
    selected_category = None
    if category_choice in crafting_categories:
        _, selected_category = crafting_categories[category_choice]
    
    # Filter recipes by player level and category if selected
    available_recipes = []
    for name, recipe in CRAFTING_RECIPES.items():
        if user_data["level"] >= recipe["level_required"]:
            if selected_category is None or recipe.get("type") == selected_category:
                available_recipes.append(name)
    
    # Sort recipes by level required
    available_recipes.sort(key=lambda x: CRAFTING_RECIPES[x]["level_required"])
    
    if not available_recipes:
        print("No recipes available at your level or in this category")
        return
    
    # Check which recipes can be crafted with current materials
    craftable_recipes = []
    for recipe_name in available_recipes:
        recipe = CRAFTING_RECIPES[recipe_name]
        can_craft = True
        for material, amount in recipe["materials"].items():
            if user_data["materials"].get(material, 0) < amount:
                can_craft = False
                break
        craftable_recipes.append((recipe_name, can_craft))
    
    print(f"\nAvailable recipes ({len(available_recipes)}):")
    for i, (recipe_name, can_craft) in enumerate(craftable_recipes, 1):
        recipe = CRAFTING_RECIPES[recipe_name]
        
        # Format based on craftability
        if can_craft:
            status = f"{GREEN}[CRAFTABLE]{ENDC}"
        else:
            status = f"{RED}[MISSING MATERIALS]{ENDC}"
        
        # Format recipe name based on its type
        item_type = recipe.get("type", "")
        if item_type == "weapon":
            type_color = RED
        elif item_type == "armor":
            type_color = BLUE
        elif item_type == "tool":
            type_color = YELLOW
        elif item_type == "accessory":
            type_color = MAGENTA
        else:
            type_color = WHITE
            
        # Show item level and effects
        effect_str = ""
        if "effect" in recipe:
            effect_str = f" - Power: {recipe['effect']}"
        if "element" in recipe:
            element_color = get_element_color(recipe["element"])
            effect_str += f" - Element: {element_color}{recipe['element']}{ENDC}"
        if "special" in recipe:
            effect_str += f" - Special: {recipe['special']}"
            
        print(f"\n{i}. {type_color}{recipe_name}{ENDC} {status}{effect_str}")
        print(f"   Type: {item_type.capitalize()}, Level Required: {recipe['level_required']}")
        
        # Show materials with color indicating if you have enough
        print("   Required materials:")
        for material, amount in recipe["materials"].items():
            have_amount = user_data["materials"].get(material, 0)
            if have_amount >= amount:
                material_status = f"{GREEN}{have_amount}/{amount}{ENDC}"
            else:
                material_status = f"{RED}{have_amount}/{amount}{ENDC}"
            print(f"    - {material}: {material_status}")
    
    # Highlight the crafting bonus if applicable
    if crafting_bonus > 0:
        print(f"\n{YELLOW}Crafting Bonus: +{crafting_bonus}% quality from {player_profession} profession{ENDC}")
    
    choice = input("\nChoose item to craft (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(craftable_recipes):
            recipe_name, can_craft = craftable_recipes[choice - 1]
            recipe = CRAFTING_RECIPES[recipe_name]

            # Check materials again to be safe
            missing_materials = []
            for material, amount in recipe["materials"].items():
                if user_data["materials"].get(material, 0) < amount:
                    missing_materials.append(f"{material} ({user_data['materials'].get(material, 0)}/{amount})")
            
            if missing_materials:
                print(f"{RED}Cannot craft - missing materials:{ENDC}")
                for mat in missing_materials:
                    print(f"  - {mat}")
                return

            # Confirm crafting
            confirm = input(f"Craft {recipe_name}? (y/n): ").strip().lower()
            if confirm != 'y':
                return
                
            # Determine if crafting results in a higher quality item based on profession
            quality_bonus = random.randint(0, 100)
            quality_result = "normal"
            
            if quality_bonus < crafting_bonus:
                # Crafting bonus triggered for better quality
                if quality_bonus < crafting_bonus * 0.3:  # 30% of bonus chance for exceptional quality
                    quality_result = "exceptional"
                else:
                    quality_result = "superior"
            
            # Consume materials
            for material, amount in recipe["materials"].items():
                user_data["materials"][material] -= amount

            # Add item to inventory with quality tag if applicable
            crafted_item = recipe_name
            if quality_result == "superior":
                crafted_item = f"Superior {recipe_name}"
                print(f"{GREEN}Your expertise as a {player_profession} helped create a superior quality item!{ENDC}")
            elif quality_result == "exceptional":
                crafted_item = f"Exceptional {recipe_name}"
                print(f"{CYAN}Your mastery as a {player_profession} resulted in an exceptional crafting result!{ENDC}")
            
            user_data["inventory"].append(crafted_item)
            
            # Update any related achievements or stats
            user_data["stats"]["items_crafted"] = user_data["stats"].get("items_crafted", 0) + 1
            
            if recipe.get("type") == "weapon":
                user_data["stats"]["weapons_crafted"] = user_data["stats"].get("weapons_crafted", 0) + 1
            elif recipe.get("type") == "armor":
                user_data["stats"]["armor_crafted"] = user_data["stats"].get("armor_crafted", 0) + 1
            
            # Special message based on item type
            item_type = recipe.get("type", "")
            if item_type == "weapon":
                print(f"{RED}Successfully crafted {crafted_item}!{ENDC} This new weapon will help you in battles.")
            elif item_type == "armor":
                print(f"{BLUE}Successfully crafted {crafted_item}!{ENDC} This armor will offer better protection.")
            elif item_type == "tool":
                print(f"{YELLOW}Successfully crafted {crafted_item}!{ENDC} This tool will help you gather resources more efficiently.")
            else:
                print(f"Successfully crafted {crafted_item}!")
                
            # Show item details
            print("\nItem details:")
            if "effect" in recipe:
                print(f"Power: {recipe['effect']}")
            if "element" in recipe:
                element_color = get_element_color(recipe["element"])
                print(f"Element: {element_color}{recipe['element']}{ENDC}")
            if "special" in recipe:
                print(f"Special ability: {recipe['special']}")
                
            # Offer to equip if it's equippable
            if item_type in ["weapon", "armor", "accessory"]:
                equip_choice = input("\nEquip this item now? (y/n): ").strip().lower()
                if equip_choice == 'y':
                    equip_item(crafted_item)
                    
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def print_materials() -> None:
    print_header("Materials")
    if not user_data["materials"]:
        print("You don't have any materials")
        return

    for material, amount in user_data["materials"].items():
        print(f"{material}: {amount}")

def travel_to_area() -> None:
    print_header("Travel")
    print("\nAvailable locations:")
    locations = list(LOCATIONS.keys())
    for i, loc in enumerate(locations, 1):
        info = LOCATIONS[loc]
        print(f"{i}. {loc} - {info['description']}")
        if info['type'] == 'town':
            print(f"   Shops: {', '.join(info['shops'])}")

    choice = input("\nChoose area to travel to (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(locations):
            user_data["current_area"] = locations[choice - 1]
            print(f"Traveled to {user_data['current_area']}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Invalid input")

def fight_monster(monster_name: str) -> None:
    try:
        monster = next((m for m in monsters if m["name"].lower() == monster_name.lower()), None)
        if not monster:
            print(f"Monster '{monster_name}' not found!")
            return

        # Check player level against monster level
        if user_data["level"] < monster["level"]:
            print(f"{FAIL}Warning: This monster is too strong for your level! (Required: Level {monster['level']}){ENDC}")
            if input("Do you still want to fight? (y/n): ").lower() != 'y':
                return

        if user_data["health"] <= 0:
            print("You can't fight while defeated! Use a healing potion or rest.")
            return

        # Check if monster is in current area (case-insensitive)
        area_monsters = LOCATIONS.get(user_data["current_area"], {}).get("monsters", [])
        if not any(monster["name"].lower() == m.lower() for m in area_monsters):
            print(f"{monster['name']} is not in this area! Travel to find it.")
            return

        print_header(f"Fighting {monster['name']}")
        monster_health = monster["health"]

        while user_data["health"] > 0 and monster_health > 0:
            try:
                print(f"\nYour Health: {user_data['health']}/{user_data['max_health']}")
                print(f"Monster Health: {monster_health}/{monster['health']}")
                print("\nActions:")
                print("1. Attack")
                print("2. Use Skill")
                print("3. Use Healing Potion")
                print("4. Flee")

                choice = input("Choose action (1-4): ").strip()

                if choice == "1":
                    # Calculate damage with equipped weapon
                    base_damage = user_data.get("attack", 10)  # Default attack value if not found
                    weapon_bonus = user_data.get("equipped", {}).get("weapon", {}).get("effect", 0)
                    damage = base_damage + weapon_bonus

                    if random.random() < CRITICAL_CHANCE:
                        damage *= 2
                        print("Critical hit!")

                    monster_health -= damage
                    print(f"You deal {damage} damage!")

                elif choice == "2":
                    if user_data["skills"]:
                        print("\nAvailable skills:")
                        for i, skill in enumerate(user_data["skills"], 1):
                            print(f"[{i}] {skill}")
                        try:
                            skill_choice = int(input("Choose skill (0 to cancel): "))
                            if skill_choice == 0:
                                continue
                            if 1 <= skill_choice <= len(user_data["skills"]):
                                skill = user_data["skills"][skill_choice - 1]
                                damage = random.randint(15, 25)  # Skills do more damage
                                monster_health -= damage
                                print(f"You used {skill} and dealt {damage} damage!")
                            else:
                                print("Invalid skill choice.")
                        except ValueError:
                            print("Invalid input.")
                    else:
                        print("You have no skills available!")
                        continue

                elif choice == "3":
                    if "Healing Potion" in user_data["inventory"]:
                        user_data["health"] = min(user_data["health"] + 30, user_data["max_health"])
                        user_data["inventory"].remove("Healing Potion")
                        print("You used a Healing Potion! Health restored.")
                        continue
                    else:
                        print("You have no Healing Potions!")
                        continue

                elif choice == "4":
                    # Calculate flee chance based on speed
                    player_speed = user_data.get("speed", 5)
                    monster_speed = monster.get("speed", 5)  # Default monster speed 5 if not set
                    base_chance = 0.4  # Base flee chance
                    speed_diff = player_speed - monster_speed
                    flee_chance = base_chance + (speed_diff * 0.05)
                    flee_chance = max(0.1, min(flee_chance, 0.9))  # Clamp between 10% and 90%

                    if random.random() < flee_chance:
                        print("You successfully fled!")
                        return
                    print("Failed to flee!")

                else:
                    print("Invalid choice!")
                    continue

                # Monster attacks if still alive
                if monster_health > 0:
                    defense_bonus = user_data.get("equipped", {}).get("armor", {}).get("effect", 0)
                    damage_taken = max(1, monster["attack"] - defense_bonus)
                    if random.random() > DODGE_CHANCE:
                        user_data["health"] -= damage_taken
                        print(f"Monster deals {damage_taken} damage!")
                    else:
                        print("You dodged the attack!")

            except Exception as e:
                print(f"Error during combat: {e}")
                continue

        if monster_health <= 0:
            if monster['name'] == "Dark Legionary Supreme Lord:Noctis, the Obsidian Fallen Eternal":
                print(f"\n{FAIL}If the sky betrays me...I will make sure it will fall...even if you defeat me...{ENDC}")
                user_data["progress"] = "endgame"
            print(f"\nYou defeated the {monster['name']}!")
            exp_gain = monster["level"] * 20
            user_data["exp"] += exp_gain
            print(f"Gained {exp_gain} experience!")
            check_achievements()

            # Increment monsters killed count
            user_data["monsters_killed"] += 1

            # Check if monster is a boss
            if monster.get("boss", False):
                print(f"Congratulations! You defeated the boss {monster['name']}!")
                # Mark dungeon as completed if in a dungeon
                for dungeon in dungeons:
                    if monster['name'] in dungeon['monsters']:
                        if dungeon['name'] not in user_data["dungeons_completed"]:
                            user_data["dungeons_completed"].append(dungeon['name'])
                            print(f"You have completed the dungeon: {dungeon['name']}!")
                            # Reward player (example: gold and exp bonus)
                            reward_gold = 500
                            reward_exp = 1000
                            user_data["gold"] += reward_gold
                            user_data["exp"] += reward_exp
                            print(f"You received {reward_gold} gold and {reward_exp} experience as a reward!")
                        break
            else:
                # Check for level up
                check_level_up()
                # Trigger boss encounter if monsters killed between 12 and 26
                if 12 <= user_data["monsters_killed"] <= 26:
                    # Find a boss in dungeons of the current area
                    bosses_in_area = []
                    for dungeon in dungeons:
                        if dungeon.get("name", "").lower() == user_data["current_area"].lower():
                            for m_name in dungeon["monsters"]:
                                m = next((mon for mon in monsters if mon["name"] == m_name and mon.get("boss", False)), None)
                                if m:
                                    bosses_in_area.append(m)
                    if bosses_in_area:
                        boss = random.choice(bosses_in_area)
                        print(f"\nA boss {boss['name']} appears!")
                        fight_monster(boss["name"])
            loot(monster)
        else:
            print("You were defeated!")

    except Exception as e:
        print(f"Error initiating combat: {e}")

def check_level_up() -> None:
    while user_data["exp"] >= EXP_TO_LEVEL * user_data["level"]:
        user_data["level"] += 1
        user_data["max_health"] += 20
        user_data["health"] = user_data["max_health"]
        user_data["attack"] += 5
        user_data["defense"] += 3
        print(f"\nLevel Up! You are now level {user_data['level']}!")
        print("Your stats have increased!")
        print(f"Health: {user_data['health']}/{user_data['max_health']}")
        print(f"Attack: {user_data['attack']}")
        print(f"Defense: {user_data['defense']}")

def show_weapon_info() -> None:
    print_header("Weapon Information")
    for weapon, stats in WEAPONS.items():
        print(f"\n{weapon}:")
        print(f"  Damage: {stats['damage']}")
        print(f"  Speed: {stats['speed']}")
        print(f"  Price: {stats['price']} gold")
        if 'effect' in stats:
            print(f"  Special Effect: {stats['effect']}")




# Enhanced pet system
# Pet evolution paths and requirements
PET_EVOLUTIONS = {
    "Cat": {
        "evolves_to": "Shadow Cat",
        "level_required": 10,
        "loyalty_required": 75,
        "materials_required": ["Shadow Essence", "Feline Spirit"]
    },
    "Dog": {
        "evolves_to": "War Hound",
        "level_required": 10,
        "loyalty_required": 80,
        "materials_required": ["Beast Fang", "Loyal Heart"]
    },
    "Dragon Hatchling": {
        "evolves_to": "Young Drake",
        "level_required": 15,
        "loyalty_required": 70,
        "materials_required": ["Dragon Scale", "Fire Essence"]
    },
    "Young Drake": {
        "evolves_to": "Adult Dragon",
        "level_required": 30,
        "loyalty_required": 90,
        "materials_required": ["Dragon Heart", "Ancient Flame", "Royal Crown"]
    },
    "Wolf Pup": {
        "evolves_to": "Dire Wolf",
        "level_required": 12,
        "loyalty_required": 75,
        "materials_required": ["Wolf Fang", "Forest Spirit"]
    },
    "Hawk": {
        "evolves_to": "Royal Eagle",
        "level_required": 10,
        "loyalty_required": 70,
        "materials_required": ["Wind Essence", "Sharp Talon"]
    },
    "Fish": {
        "evolves_to": "Koi Guardian",
        "level_required": 8,
        "loyalty_required": 65,
        "materials_required": ["Water Essence", "River Pearl"]
    },
    "Snake": {
        "evolves_to": "Venom Serpent",
        "level_required": 10,
        "loyalty_required": 60,
        "materials_required": ["Venom Sac", "Ancient Scale"]
    },
    "Phoenix Chick": {
        "evolves_to": "Adolescent Phoenix",
        "level_required": 15,
        "loyalty_required": 75,
        "materials_required": ["Eternal Flame", "Phoenix Feather"]
    },
    "Adolescent Phoenix": {
        "evolves_to": "Adult Phoenix",
        "level_required": 30,
        "loyalty_required": 85,
        "materials_required": ["Phoenix Ash", "Solar Crystal", "Rebirth Ember"]
    },
    "Battle Wolf": {
        "evolves_to": "Alpha Wolf",
        "level_required": 14,
        "loyalty_required": 80,
        "materials_required": ["Alpha Fang", "Moon Crystal"]
    },
    "Guardian Bear": {
        "evolves_to": "Ancient Bear",
        "level_required": 15,
        "loyalty_required": 75,
        "materials_required": ["Bear Essence", "Mountain Crystal"]
    },
    "Spirit Fox": {
        "evolves_to": "Nine-Tailed Fox",
        "level_required": 18,
        "loyalty_required": 85,
        "materials_required": ["Spirit Essence", "Ancient Scroll", "Fox Fire"]
    },
    "Lucky Rabbit": {
        "evolves_to": "Fortune Hare",
        "level_required": 12,
        "loyalty_required": 70,
        "materials_required": ["Fortune Clover", "Golden Carrot"]
    },
    "Mystic Owl": {
        "evolves_to": "Wisdom Owl",
        "level_required": 16,
        "loyalty_required": 75,
        "materials_required": ["Ancient Knowledge", "Moonlit Feather"]
    },
    "Shadow Panther": {
        "evolves_to": "Void Stalker",
        "level_required": 17,
        "loyalty_required": 80,
        "materials_required": ["Void Fragment", "Shadow Crystal", "Midnight Essence"]
    },
    "Thunder Eagle": {
        "evolves_to": "Storm Harbinger",
        "level_required": 20,
        "loyalty_required": 75,
        "materials_required": ["Storm Essence", "Lightning Crystal", "Royal Feather"]
    },
    "Abyssal Kraken Hatchling": {
        "evolves_to": "Kraken Juvenile",
        "level_required": 25,
        "loyalty_required": 70,
        "materials_required": ["Abyssal Ink", "Deep Sea Pearl", "Ocean Crystal"]
    },
    "Kraken Juvenile": {
        "evolves_to": "Elder Kraken",
        "level_required": 40,
        "loyalty_required": 85,
        "materials_required": ["Kraken Heart", "Abyssal Crown", "Oceanic Essence", "Legendary Sea Chart"]
    }
}

PETS = {
    "Hylit": {
        "price": 0, 
        "boost": {"intelligence": 2, "exp_gain": 5}, 
        "description": "Your fairy companion and guide",
        "element": "Nullum",
        "abilities": {"1": "Find Treasure", "3": "Weather Sense"},
        "rarity": "Unique",
        "combat_style": "Support",
        "evolution": None  # Unique companion cannot evolve
    },
    "Cat": {
        "price": 50, 
        "boost": {"attack": 2, "speed": 3}, 
        "description": "A stealthy companion that boosts attack",
        "element": "Nullum",
        "abilities": {"2": "Quick Attack", "4": "Scouting"},
        "rarity": "Common",
        "combat_style": "Agile",
        "evolution": "Shadow Cat"
    },
    
    # Evolved Pets
    "Shadow Cat": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 5, "speed": 7, "critical_chance": 5}, 
        "description": "A mystical feline born from shadows, swift and deadly",
        "element": "Tenebrae",
        "abilities": {"1": "Shadow Pounce", "3": "Night Vision", "5": "Stealth Strike", "7": "Soul Bond"},
        "rarity": "Rare",
        "combat_style": "Assassin",
        "evolution": None
    },
    "Dog": {
        "price": 50, 
        "boost": {"defense": 2, "loyalty": 5}, 
        "description": "A loyal friend that boosts defense",
        "element": "Nullum",
        "abilities": {"2": "Protective Stance", "5": "Intimidate"},
        "rarity": "Common",
        "combat_style": "Defensive",
        "evolution": "War Hound"
    },
    
    "War Hound": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"defense": 6, "loyalty": 10, "health": 15}, 
        "description": "A battle-hardened canine warrior, loyal to the death",
        "element": "Ferrum",
        "abilities": {"1": "Battle Howl", "3": "Iron Hide", "5": "Pack Tactics", "8": "Guardian's Aura"},
        "rarity": "Rare",
        "combat_style": "Tank",
        "evolution": None
    },
    "Dragon Hatchling": {
        "price": 200, 
        "boost": {"attack": 5, "health": 10}, 
        "description": "A baby dragon that boosts attack and health",
        "element": "Ignis",
        "abilities": {"1": "Flame Burst", "3": "Intimidate", "5": "Fierce Loyalty"},
        "rarity": "Epic",
        "combat_style": "Offensive",
        "evolution": "Young Drake"
    },
    
    "Young Drake": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 12, "health": 25, "fire_resistance": 50}, 
        "description": "A growing dragon with formidable power",
        "element": "Ignis",
        "abilities": {"1": "Fire Breath", "3": "Wing Slash", "5": "Dragon Roar", "7": "Heat Aura"},
        "rarity": "Epic",
        "combat_style": "Berserker",
        "evolution": "Adult Dragon"
    },
    
    "Adult Dragon": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 25, "health": 50, "fire_resistance": 100, "intimidation": 20}, 
        "description": "A mighty dragon in its prime, commanding respect and fear",
        "element": "Ignis",
        "abilities": {"1": "Inferno", "3": "Dragon Claw", "5": "Tail Sweep", "7": "Fire Storm", "10": "Dragon Soul Bond"},
        "rarity": "Legendary",
        "combat_style": "Dominator",
        "evolution": None
    },
    "Phoenix Chick": {
        "price": 200, 
        "boost": {"health": 15, "magic": 5}, 
        "description": "A magical bird that boosts health and magic",
        "element": "Fire",
        "abilities": {"1": "Healing Mist", "3": "Flame Burst", "6": "Weather Sense"},
        "rarity": "Epic",
        "combat_style": "Support",
        "evolution": "Adolescent Phoenix"
    },
    "Adolescent Phoenix": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"health": 25, "magic": 15, "fire_damage": 15}, 
        "description": "A maturing phoenix with growing flames and regenerative powers",
        "element": "Ignis",
        "abilities": {"1": "Healing Flames", "3": "Fire Shield", "5": "Phoenix Dive", "7": "Warmth Aura"},
        "rarity": "Epic",
        "combat_style": "Healer",
        "evolution": "Adult Phoenix"
    },
    "Adult Phoenix": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"health": 40, "magic": 30, "fire_damage": 25, "revival": 1}, 
        "description": "A magnificent phoenix with the power of rebirth and eternal flame",
        "element": "Ignis",
        "abilities": {"1": "Resurrection", "3": "Inferno", "5": "Cleansing Fire", "7": "Life Bond", "10": "Eternal Flame"},
        "rarity": "Legendary",
        "combat_style": "Immortal",
        "evolution": None
    },
    "Battle Wolf": {
        "price": 150, 
        "boost": {"attack": 4, "speed": 3}, 
        "description": "A fierce wolf that boosts attack and speed",
        "element": "Nullum",
        "abilities": {"1": "Quick Attack", "4": "Intimidate"},
        "rarity": "Rare",
        "combat_style": "Offensive",
        "evolution": "Alpha Wolf"
    },
    "Alpha Wolf": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 12, "speed": 8, "critical_chance": 8}, 
        "description": "A powerful pack leader with commanding presence and deadly attacks",
        "element": "Tenebrae",
        "abilities": {"1": "Savage Strike", "3": "Pack Leader", "5": "Moonlight Howl", "7": "Feral Instinct"},
        "rarity": "Epic",
        "combat_style": "Predator",
        "evolution": None
    },
    "Guardian Bear": {
        "price": 150, 
        "boost": {"defense": 4, "health": 5}, 
        "description": "A strong bear that boosts defense and health",
        "element": "Earth",
        "abilities": {"1": "Protective Stance", "3": "Stone Shield"},
        "rarity": "Rare",
        "combat_style": "Defensive",
        "evolution": "Ancient Bear"
    },
    "Ancient Bear": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"defense": 15, "health": 20, "damage_reduction": 10}, 
        "description": "A primordial bear spirit with tremendous resilience and earth power",
        "element": "Gē",
        "abilities": {"1": "Mountain's Strength", "3": "Earth Armor", "5": "Primal Roar", "7": "Nature's Guardian"},
        "rarity": "Epic",
        "combat_style": "Warden",
        "evolution": None
    },
    "Spirit Fox": {
        "price": 175, 
        "boost": {"exp_gain": 10, "magic": 3}, 
        "description": "A mystical fox that boosts experience gain and magic",
        "element": "Nullum",
        "abilities": {"2": "Find Treasure", "4": "Energy Pulse"},
        "rarity": "Rare",
        "combat_style": "Magical",
        "evolution": "Nine-Tailed Fox"
    },
    "Nine-Tailed Fox": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"exp_gain": 20, "magic": 15, "intelligence": 10}, 
        "description": "A legendary spirit fox with nine tails and immense magical power",
        "element": "Pneuma",
        "abilities": {"1": "Fox Fire", "3": "Spirit Whisper", "5": "Illusion", "7": "Soul Binding", "9": "Ancestral Wisdom"},
        "rarity": "Legendary",
        "combat_style": "Mystic",
        "evolution": None
    },
    "Lucky Rabbit": {
        "price": 100, 
        "boost": {"gold_find": 10, "luck": 5}, 
        "description": "A lucky companion that helps find more gold",
        "element": "Nullum",
        "abilities": {"1": "Find Treasure", "3": "Scavenge"},
        "rarity": "Uncommon",
        "combat_style": "Support",
        "evolution": "Fortune Hare"
    },
    "Fortune Hare": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"gold_find": 25, "luck": 15, "loot_quality": 10}, 
        "description": "A mythical hare that brings incredible fortune to its companion",
        "element": "Lux",
        "abilities": {"1": "Golden Touch", "3": "Lucky Strike", "5": "Fortune Aura", "7": "Prosperity Bond"},
        "rarity": "Epic",
        "combat_style": "Fortune",
        "evolution": None
    },
    "Mystic Owl": {
        "price": 125, 
        "boost": {"intelligence": 3, "magic": 4}, 
        "description": "An intelligent owl that boosts intelligence and magic",
        "element": "Air",
        "abilities": {"2": "Swift Movement", "5": "Energy Pulse"},
        "rarity": "Uncommon",
        "combat_style": "Magical",
        "evolution": "Wisdom Owl"
    },
    "Wisdom Owl": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"intelligence": 12, "magic": 15, "mana_regen": 10}, 
        "description": "An ancient owl with vast knowledge and powerful arcane abilities",
        "element": "Aer",
        "abilities": {"1": "Arcane Sight", "3": "Knowledge Transfer", "5": "Spell Echo", "7": "Time Dilation"},
        "rarity": "Epic",
        "combat_style": "Sage",
        "evolution": None
    },
    "Shadow Panther": {
        "price": 175, 
        "boost": {"stealth": 5, "attack": 3}, 
        "description": "A stealthy panther that boosts stealth and attack",
        "element": "Nullum",
        "abilities": {"1": "Quick Attack", "3": "Scouting"},
        "rarity": "Rare",
        "combat_style": "Agile",
        "evolution": "Void Stalker"
    },
    "Void Stalker": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"stealth": 12, "attack": 8, "critical_chance": 10}, 
        "description": "A fearsome predator that has merged with the darkness of the void",
        "element": "Tenebrae",
        "abilities": {"1": "Shadow Step", "3": "Void Strike", "5": "Dark Ambush", "7": "Dimensional Shift"},
        "rarity": "Epic",
        "combat_style": "Assassin",
        "evolution": None
    },
    "Thunder Eagle": {
        "price": 200, 
        "boost": {"speed": 5, "attack": 3}, 
        "description": "A fast eagle that boosts speed and attack",
        "element": "Lightning",
        "abilities": {"1": "Swift Movement", "3": "Shock Strike"},
        "rarity": "Rare",
        "combat_style": "Agile",
        "evolution": "Storm Harbinger"
    },
    "Storm Harbinger": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"speed": 10, "attack": 7, "lightning_damage": 15}, 
        "description": "A majestic bird of storms that controls the weather",
        "element": "Fulmen",
        "abilities": {"1": "Lightning Strike", "3": "Storm Caller", "5": "Thunder Dash", "8": "Eye of the Storm"},
        "rarity": "Epic",
        "combat_style": "Elemental",
        "evolution": None
    },
    "Abyssal Kraken Hatchling": {
        "price": 300, 
        "boost": {"attack": 10, "defense": 5}, 
        "description": "A baby kraken that boosts attack and defense",
        "element": "Water",
        "abilities": {"1": "Healing Mist", "3": "Intimidate", "5": "Energy Pulse"},
        "rarity": "Epic",
        "combat_style": "Balanced",
        "evolution": "Kraken Juvenile"
    },
    "Kraken Juvenile": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 18, "defense": 12, "water_damage": 15}, 
        "description": "A growing sea monster with mastery over ocean currents",
        "element": "Aqua",
        "abilities": {"1": "Tentacle Slam", "3": "Whirlpool", "5": "Deep Pressure", "7": "Water Manipulation"},
        "rarity": "Epic",
        "combat_style": "Controller",
        "evolution": "Elder Kraken"
    },
    "Elder Kraken": {
        "price": 0,  # Can only be obtained by evolution
        "boost": {"attack": 35, "defense": 25, "water_damage": 30, "intimidation": 20}, 
        "description": "An ancient sea titan that commands the depths of the ocean",
        "element": "Aqua",
        "abilities": {"1": "Crushing Grasp", "3": "Tsunami", "5": "Abyssal Darkness", "7": "Oceanic Fury", "10": "Leviathan's Call"},
        "rarity": "Legendary",
        "combat_style": "Destroyer",
        "evolution": None
    },
    "Small Copper Golem": {
        "price": 250, 
        "boost": {"defense": 10, "health": 5}, 
        "description": "A small golem made from copper that boosts defense",
        "element": "Earth",
        "abilities": {"1": "Protective Stance", "3": "Stone Shield"},
        "rarity": "Rare",
        "combat_style": "Defensive"
    },
    "Small Silver Golem": {
        "price": 300, 
        "boost": {"defense": 15, "health": 7}, 
        "description": "A small golem made from silver that boosts defense",
        "element": "Earth",
        "abilities": {"1": "Protective Stance", "3": "Stone Shield", "5": "Energy Pulse"},
        "rarity": "Epic",
        "combat_style": "Defensive"
    },
    "Small Titanium Golem": {
        "price": 350, 
        "boost": {"defense": 25, "health": 10}, 
        "description": "A small golem made from titanium that boosts defense",
        "element": "Earth",
        "abilities": {"1": "Protective Stance", "2": "Stone Shield", "4": "Energy Pulse", "6": "Fierce Loyalty"},
        "rarity": "Legendary",
        "combat_style": "Defensive"
    },
    # New elemental pets
    "Flame Salamander": {
        "price": 180,
        "boost": {"attack": 6, "magic": 4},
        "description": "A fiery salamander that empowers fire magic",
        "element": "Fire",
        "abilities": {"1": "Flame Burst", "3": "Energy Pulse", "5": "Fierce Loyalty"},
        "rarity": "Rare",
        "combat_style": "Magical"
    },
    "Frost Fox": {
        "price": 180,
        "boost": {"defense": 4, "magic": 6},
        "description": "A fox with fur of crystalline ice",
        "element": "Ice",
        "abilities": {"1": "Healing Mist", "3": "Swift Movement", "5": "Energy Pulse"},
        "rarity": "Rare",
        "combat_style": "Magical"
    },
    "Static Weasel": {
        "price": 180,
        "boost": {"speed": 6, "attack": 4},
        "description": "A weasel crackling with electricity",
        "element": "Lightning",
        "abilities": {"1": "Quick Attack", "3": "Shock Strike", "5": "Swift Movement"},
        "rarity": "Rare",
        "combat_style": "Agile"
    },
    "Stone Tortoise": {
        "price": 180,
        "boost": {"defense": 8, "health": 6},
        "description": "A tortoise with a shell of living stone",
        "element": "Earth",
        "abilities": {"1": "Stone Shield", "3": "Protective Stance", "5": "Energy Pulse"},
        "rarity": "Rare",
        "combat_style": "Defensive"
    },
    "Zephyr Hawk": {
        "price": 180,
        "boost": {"speed": 8, "intelligence": 4},
        "description": "A hawk that rides the wind currents",
        "element": "Air",
        "abilities": {"1": "Swift Movement", "3": "Scouting", "5": "Weather Sense"},
        "rarity": "Rare",
        "combat_style": "Agile"
    },
    "Hellstone Golem": {
        "price": 600, 
        "boost": {"defense": 90, "attack": 20}, 
        "description": "A powerful golem made from hellstone that boosts defense",
        "element": "Fire",
        "abilities": {"1": "Stone Shield", "2": "Flame Burst", "4": "Fierce Loyalty", "6": "Energy Pulse"},
        "rarity": "Legendary",
        "combat_style": "Defensive"
    },
    "Abyssal Obsidian Golem": {
        "price": 1000, 
        "boost": {"defense": 150, "health": 50}, 
        "description": "A powerful golem made from obsidian extracted from the abyss",
        "element": "Earth",
        "abilities": {"1": "Stone Shield", "2": "Protective Stance", "3": "Energy Pulse", "5": "Intimidate"},
        "rarity": "Mythic",
        "combat_style": "Defensive"
    },
    "Abyssal Diamond Golem": {
        "price": 1500, 
        "boost": {"defense": 200, "attack": 40, "health": 100}, 
        "description": "A powerful golem made from diamond extracted from the abyssal caves",
        "element": "Earth",
        "abilities": {"1": "Stone Shield", "2": "Protective Stance", "3": "Energy Pulse", "4": "Intimidate", "5": "Fierce Loyalty"},
        "rarity": "Mythic",
        "combat_style": "Balanced"
    }
}


def show_professions() -> None:
    print_header("Professions")

    if user_data["has_chosen_profession"]:
        prof = user_data["profession"]
        print(f"{CYAN}Your current profession: {BOLD}{prof}{ENDC}")
        
        if prof in PROFESSIONS:
            profession_info = PROFESSIONS[prof]
            
            # Basic information
            print(f"\n{YELLOW}Special Ability: {ENDC}{profession_info['special_ability']}")
            print(f"{LIGHTGRAY}{profession_info['ability_description']}{ENDC}")
            
            # Bonuses
            print(f"\n{YELLOW}Profession bonuses:{ENDC}")
            print(f"Gathering bonus for: {', '.join(profession_info['gather_bonus'])}")
            print(f"Crafting bonus for: {', '.join(profession_info['craft_bonus'])}")
            
            # Passive bonuses
            print(f"\n{YELLOW}Passive Bonuses:{ENDC}")
            for stat, value in profession_info['passive_bonus'].items():
                print(f"  {stat.replace('_', ' ').title()}: +{value}")
            
            # Level bonuses
            print(f"\n{YELLOW}Level Milestone Bonuses:{ENDC}")
            for level, bonus in profession_info['level_bonuses'].items():
                if user_data["level"] >= level:
                    print(f"  Level {level}: {OKGREEN}✓{ENDC} {bonus}")
                else:
                    print(f"  Level {level}: {YELLOW}⊗{ENDC} {bonus} (Locked)")
            
            # Weather bonuses if applicable
            if 'weather_bonuses' in profession_info:
                print(f"\n{YELLOW}Weather Bonuses:{ENDC}")
                current_weather = user_data.get("current_weather", "Sunny")
                for weather, bonus in profession_info['weather_bonuses'].items():
                    if weather == current_weather:
                        print(f"  {weather}: {OKGREEN}✓{ENDC} {bonus} (Active)")
                    else:
                        print(f"  {weather}: {bonus}")
            
            # Season bonuses if applicable
            if 'season_bonuses' in profession_info:
                print(f"\n{YELLOW}Seasonal Bonuses:{ENDC}")
                current_season = user_data.get("current_season", "Summer")
                for season, bonus in profession_info['season_bonuses'].items():
                    if season == current_season:
                        print(f"  {season}: {OKGREEN}✓{ENDC} {bonus} (Active)")
                    else:
                        print(f"  {season}: {bonus}")
            
            # Profession change option
            change = input("\nDo you want to change your profession? (y/n): ").lower()
            if change == 'y':
                user_data["has_chosen_profession"] = False
                print(f"You have abandoned your profession as a {prof}.")
                show_professions()  # Recursive call to show profession selection
            return
    
    # Display available professions if user hasn't chosen one or wants to change
    print(f"{YELLOW}Available Professions:{ENDC}")
    
    # Group professions by type
    traditional = []
    specialized = []
    
    for prof, info in PROFESSIONS.items():
        if prof in ["Miner", "Herbalist", "Blacksmith", "Alchemist", "Hunter", "Woodcutter", "Fisher", "Archaeologist", "Enchanter"]:
            traditional.append(prof)
        else:
            specialized.append(prof)
    
    # Display traditional professions
    print(f"\n{HEADER}Traditional Professions:{ENDC}")
    for prof in traditional:
        info = PROFESSIONS[prof]
        print(f"{CYAN}{prof}:{ENDC} {info['ability_description']}")
        print(f"  Special Ability: {info['special_ability']}")
        print(f"  Gathering: {', '.join(info['gather_bonus'][:3])}{'...' if len(info['gather_bonus']) > 3 else ''}")
    
    # Display specialized professions
    print(f"\n{HEADER}Specialized Professions:{ENDC}")
    for prof in specialized:
        info = PROFESSIONS[prof]
        print(f"{MAGENTA}{prof}:{ENDC} {info['ability_description']}")
        print(f"  Special Ability: {info['special_ability']}")
        print(f"  Gathering: {', '.join(info['gather_bonus'][:3])}{'...' if len(info['gather_bonus']) > 3 else ''}")
    
    # Let player choose a profession
    print(f"\n{YELLOW}To see detailed information about a profession, type its name.{ENDC}")
    print(f"{YELLOW}To select a profession, type 'choose <profession name>'.{ENDC}")
    print(f"{YELLOW}To exit, press Enter.{ENDC}")
    
    choice = input("\nCommand: ").strip()
    
    if not choice:
        return
    
    if choice.lower().startswith("choose "):
        prof_choice = choice[7:].strip().capitalize()
        if prof_choice in PROFESSIONS:
            user_data["profession"] = prof_choice
            user_data["has_chosen_profession"] = True
            print(f"{SUCCESS}You are now a {prof_choice}.{ENDC}")
            
            # Show special message for new profession types
            if prof_choice == "Farmer":
                print(f"{CYAN}As a Farmer, you gain special bonuses during different seasons and weather conditions.{ENDC}")
                print(f"{CYAN}You'll excel at growing crops and crafting food items.{ENDC}")
            elif prof_choice == "Weather Mage":
                print(f"{CYAN}As a Weather Mage, you can harness the power of weather for combat and resource gathering.{ENDC}")
                print(f"{CYAN}Your abilities will vary based on current weather conditions.{ENDC}")
            elif prof_choice == "Artifact Hunter":
                print(f"{CYAN}As an Artifact Hunter, you specialize in finding, restoring, and using powerful artifacts.{ENDC}")
                print(f"{CYAN}You'll gain extra power when using complete artifact sets.{ENDC}")
            elif prof_choice == "Monster Tamer":
                print(f"{CYAN}As a Monster Tamer, you can interact with monsters in unique ways.{ENDC}")
                print(f"{CYAN}At higher levels, you may even be able to tame certain monsters as companions.{ENDC}")
        else:
            print(f"{FAIL}Invalid profession choice.{ENDC}")
    else:
        # Show detailed info about a profession
        prof_choice = choice.capitalize()
        if prof_choice in PROFESSIONS:
            info = PROFESSIONS[prof_choice]
            print(f"\n{HEADER}Detailed Information: {prof_choice}{ENDC}")
            print(f"{YELLOW}Special Ability:{ENDC} {info['special_ability']}")
            print(f"{LIGHTGRAY}{info['ability_description']}{ENDC}")
            
            print(f"\n{YELLOW}Gathering Bonuses:{ENDC}")
            for resource in info['gather_bonus']:
                print(f"  • {resource}")
                
            print(f"\n{YELLOW}Crafting Bonuses:{ENDC}")
            for category in info['craft_bonus']:
                print(f"  • {category}")
                
            print(f"\n{YELLOW}Passive Bonuses:{ENDC}")
            for stat, value in info['passive_bonus'].items():
                print(f"  • {stat.replace('_', ' ').title()}: +{value}")
                
            print(f"\n{YELLOW}Level Milestone Bonuses:{ENDC}")
            for level, bonus in info['level_bonuses'].items():
                print(f"  • Level {level}: {bonus}")
                
            if 'weather_bonuses' in info:
                print(f"\n{YELLOW}Weather Bonuses:{ENDC}")
                for weather, bonus in info['weather_bonuses'].items():
                    print(f"  • {weather}: {bonus}")
                    
            if 'season_bonuses' in info:
                print(f"\n{YELLOW}Seasonal Bonuses:{ENDC}")
                for season, bonus in info['season_bonuses'].items():
                    print(f"  • {season}: {bonus}")
                    
            # Option to choose this profession
            select = input(f"\nDo you want to become a {prof_choice}? (y/n): ").lower()
            if select == 'y':
                user_data["profession"] = prof_choice
                user_data["has_chosen_profession"] = True
                print(f"{SUCCESS}You are now a {prof_choice}.{ENDC}")
            else:
                show_professions()  # Go back to profession selection
        else:
            print(f"{FAIL}Invalid profession name.{ENDC}")

def check_location() -> None:
    print_header("Location Information")
    current = user_data["current_area"]

    print("Current Location:", current)
    if current in LOCATIONS:
        loc_info = LOCATIONS[current]
        print(f"\nType: {loc_info['type']}")
        print(f"Description: {loc_info['description']}")
        if 'shops' in loc_info:
            print(f"Available Shops: {', '.join(loc_info['shops'])}")
        if 'monsters' in loc_info:
            print(f"Local Monsters: {', '.join(loc_info['monsters'])}")

    print("\nAll Available Locations:")
    for name, info in LOCATIONS.items():
        print(f"\n{name}:")
        print(f"  Type: {info['type']}")
        print(f"  Description: {info['description']}")

    print("\nAvailable Dungeons:")
    for dungeon in dungeons:
        print(f"\n{dungeon['name']}:")
        print(f"  Monsters: {', '.join(dungeon['monsters'])}")
        print(f"  Possible Loot: {', '.join(dungeon['loot'])}")

def search_resources() -> None:
    print_header("Resource Search")
    search_type = random.choice(["monster", "material"])

    if search_type == "monster":
        # Get basic area monsters
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(user_data["current_area"], {}).get("monsters", [])]
        
        # Add weather-dependent monsters based on current weather
        current_weather = user_data.get("current_weather", "Sunny")
        weather_monsters = [m for m in monsters if m.get("weather") == current_weather]
        
        # Add seasonal monsters based on current season
        current_season = user_data.get("current_season", "Summer")
        season_monsters = [m for m in monsters if m.get("season") == current_season]
        
        # Combine all possible monster types
        all_possible_monsters = area_monsters.copy()
        
        # 30% chance for weather-specific monster if available
        if weather_monsters and random.random() < 0.3:
            all_possible_monsters.extend(weather_monsters)
            
        # 20% chance for season-specific monster if available
        if season_monsters and random.random() < 0.2:
            all_possible_monsters.extend(season_monsters)
            
        if all_possible_monsters:
            monster = random.choice(all_possible_monsters)
            print(f"You found a {monster['name']}!")
            print(f"Level: {monster['level']}")
            print(f"Health: {monster['health']}")
            print(f"Attack: {monster['attack']}")
            print(f"Possible drops: {', '.join(monster['drops'])}")
            
            # Show special information about weather or seasonal monsters
            if "weather" in monster:
                print(f"{CYAN}This is a {monster['weather']} weather monster! It appears during {monster['weather']} conditions.{ENDC}")
            if "season" in monster:
                print(f"{MAGENTA}This is a {monster['season']} seasonal monster! It thrives during the {monster['season']} season.{ENDC}")
                
        else:
            print("No monsters found in this area.")
    else:
        available_materials = [name for name, info in MATERIALS.items() 
                             if user_data["current_area"] in info["areas"]]
        if available_materials:
            material = random.choice(available_materials)
            tool_required = MATERIALS[material]["tool_required"]
            print(f"You found {material}!")
            if tool_required:
                print(f"Tool required: {tool_required}")
            if tool_required in user_data["tools"]:
                print("You have the right tool to gather this!")
            elif tool_required:
                print("You need the right tool to gather this.")
        else:
            print("No materials found in this area.")

def save_prompt() -> None:
    print_header("Save Game")
    show_save_slots()
    try:
        slot = int(input("\nEnter save slot number (1-5): "))
        if 1 <= slot <= 5:
            save_game(slot)
        else:
            print("Invalid slot number. Choose between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def load_prompt() -> None:
    print_header("Load Game")
    show_save_slots()
    try:
        slot = int(input("\nEnter save slot number to load: "))
        load_game(slot)
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_save_prompt() -> None:
    print_header("Delete Save")
    show_save_slots()
    try:
        slot = int(input("\nEnter save slot number to delete: "))
        if input(f"Are you sure you want to delete save slot {slot}? (y/n): ").lower() == 'y':
            delete_save(slot)
    except ValueError:
        print("Invalid input. Please enter a number.")

def talk_to_npc(npc_name: Optional[str] = None) -> None:
    if not npc_name:
        print_header("Available NPCs")
        npcs_here = [name for name, npc in NPCS.items() if npc["location"] == user_data["current_area"]]
        if npcs_here:
            print(f"NPCs in {user_data['current_area']}:")
            for name in npcs_here:
                print(f"- {name}")
        else:
            print(f"No NPCs found in {user_data['current_area']}")
        return

    try:
        npc = next((npc for name, npc in NPCS.items() if name.lower() == npc_name.lower()), None)
        if not npc:
            print(f"{FAIL}No NPC named '{npc_name}' found.{ENDC}")
            return

        if npc["location"] != user_data["current_area"]:
            print(f"{WARNING}This NPC is in {npc['location']}. You need to travel there first!{ENDC}")
            return

        print_header(f"Talking to {npc_name}")
        print_animated(npc["dialogues"]["greeting"], CYAN)

        while True:
            print(f"\n{BOLD}Options:{ENDC}")
            options = []

            if "quests" in npc:
                options.append("1. Ask about quests")
            if "story" in npc["dialogues"]:
                options.append("2. Listen to story")
            if "shop" in npc:
                options.append("3. Trade/Shop")
            if "additional" in npc["dialogues"]:
                options.append("4. Ask for advice")
            options.append("5. End conversation")

            for option in options:
                print(option)

            choice = input(f"\n{YELLOW}What would you like to do? {ENDC}")

            if choice == "1" and "quests" in npc:
                print_animated(npc["dialogues"].get("quest", "No quests available."), YELLOW)
                available_quests = [q for q in QUESTS if q["name"] in npc["quests"] 
                                  and q["id"] not in user_data["completed_quests"]
                                  and q not in user_data["active_quests"]]

                if available_quests:
                    for quest in available_quests:
                        print(f"\n{CYAN}Quest: {quest['name']}{ENDC}")
                        print(f"Description: {quest['description']}")
                        print(f"Reward: {quest['reward']['gold']} gold, {quest['reward']['exp']} exp")
                        if quest.get('story', False):
                            print(f"{MAGENTA}[Story Quest]{ENDC}")
                        if input(f"{YELLOW}Accept quest? (y/n): {ENDC}").lower() == 'y':
                            user_data["active_quests"].append(quest)
                            print(f"{OKGREEN}Quest accepted!{ENDC}")
                else:
                    print(f"{YELLOW}No available quests at the moment.{ENDC}")

            elif choice == "2" and "story" in npc["dialogues"]:
                if isinstance(npc["dialogues"]["story"], dict):
                    for part, text in npc["dialogues"]["story"].items():
                        print_animated(f"\n{MAGENTA}{part.capitalize()}:{ENDC}", delay=0.02)
                        print_animated(text, CYAN, delay=0.03)
                        input(f"\n{YELLOW}Press Enter to continue...{ENDC}")
                else:
                    print_animated(npc["dialogues"]["story"], CYAN)

            elif choice == "3" and "shop" in npc:
                print(f"\n{BOLD}Available items:{ENDC}")
                for item in npc["shop"]:
                    price = WEAPONS[item]["price"] if item in WEAPONS else MARKET_PRICES.get(item, 0)
                    print(f"{item}: {price} gold")

                while True:
                    item = input(f"\n{YELLOW}What would you like to buy? (or press Enter to cancel): {ENDC}").strip()
                    if not item:
                        break

                    if item in npc["shop"]:
                        price = WEAPONS[item]["price"] if item in WEAPONS else MARKET_PRICES.get(item, 0)
                        if user_data["gold"] >= price:
                            user_data["gold"] -= price
                            user_data["inventory"].append(item)
                            print(f"{OKGREEN}Bought {item}!{ENDC}")
                        else:
                            print(f"{FAIL}Not enough gold!{ENDC}")
                    else:
                        print(f"{FAIL}Item not available.{ENDC}")

            elif choice == "4" and "additional" in npc["dialogues"]:
                advice = random.choice(npc["dialogues"]["additional"])
                print_animated(advice, CYAN)

            elif choice == "5" or choice.lower() == "exit":
                print_animated("Farewell!", CYAN)
                break

            else:
                print(f"{FAIL}Invalid choice.{ENDC}")

    except Exception as e:
        print(f"{FAIL}Error in conversation: {e}{ENDC}")

def list_npcs() -> None:
    print_header("NPCs in Current Area")
    current_area = user_data["current_area"]
    found = False

    for npc_name, npc in NPCS.items():
        if npc["location"] == current_area:
            found = True
            print(f"\n{npc_name}")
            print(f"Location: {npc['location']}")
            if "quests" in npc:
                print(f"Available Quests: {len(npc['quests'])}")
            if "shop" in npc:
                print("Has shop: Yes")

    if not found:
        print(f"No NPCs found in {current_area}")

def show_storyline() -> None:
    print_header("Main Storyline")
    current_chapter = None

    # Count completed main chapters and check for post-game access
    completed_main_chapters = 0
    for chapter_name, chapter in STORYLINE.items():
        # Skip post-game chapters in the count
        if chapter.get("post_game", False):
            continue

        completed_quests = all(
            any(q["name"] == quest_name and q["id"] in user_data["completed_quests"] 
                for q in QUESTS)
            for quest_name in chapter["quest_line"]
        )

        if completed_quests:
            completed_main_chapters += 1

    # Check if player has unlocked post-game content
    post_game_unlocked = completed_main_chapters >= 6  # After completing 6 main chapters
    if post_game_unlocked and not user_data.get("post_game_unlocked", False):
        user_data["post_game_unlocked"] = True
        print_colored("✧・゚: *✧・゚:* CONGRATULATIONS *:・゚✧*:・゚✧", CYAN)
        print_colored("You have completed the main storyline and unlocked post-game content!", OKGREEN)
        print_colored("New adventures and challenges await in the post-game chapters!", OKGREEN)
        print_colored("Type '/postgame' to access special post-game content.", MAGENTA)

    # Display chapters based on story progression
    for chapter_name, chapter in STORYLINE.items():
        # Skip post-game chapters if not unlocked
        if chapter.get("post_game", False) and not user_data.get("post_game_unlocked", False):
            continue

        if user_data["level"] >= chapter["required_level"]:
            completed_quests = all(
                any(q["name"] == quest_name and q["id"] in user_data["completed_quests"] 
                    for q in QUESTS)
                for quest_name in chapter["quest_line"]
            )

            if completed_quests:
                status = f"{OKGREEN}✓ Completed{ENDC}"
            elif current_chapter is None:
                status = f"{YELLOW}► In Progress{ENDC}"
            else:
                status = f"{FAIL}- Locked{ENDC}"

            # Add special formatting for post-game chapters
            if chapter.get("post_game", False):
                print(f"\n{BOLD}{MAGENTA}⚝ {chapter['title']} [{status}] ⚝{ENDC}")
            else:
                print(f"\n{BOLD}{chapter['title']} [{status}]{ENDC}")

            print(f"Required Level: {chapter['required_level']}")
            print(f"Description: {chapter['description']}")

            if not completed_quests and current_chapter is None:
                current_chapter = chapter_name
                print(f"\n{UNDERLINE}Current quest line:{ENDC}")
                for quest_name in chapter["quest_line"]:
                    quest = next((q for q in QUESTS if q["name"] == quest_name), None)
                    if quest:
                        quest_status = f"{OKGREEN}✓{ENDC}" if quest["id"] in user_data["completed_quests"] else f"{YELLOW}►{ENDC}"
                        print(f"  {quest_status} {quest_name}")

def show_postgame_content() -> None:
    """Display post-game exclusive content and challenges"""
    if not user_data.get("post_game_unlocked", False):
        print_colored("You have not yet unlocked post-game content.", FAIL)
        print_colored("Complete the main storyline first!", YELLOW)
        return

    print_header("POST-GAME CONTENT")
    print_colored("Welcome to the post-game adventures!", MAGENTA)

    # Show available post-game activities
    print("\n" + BOLD + "Available Activities:" + ENDC)

    # Dimensional Rifts
    print(f"\n{CYAN}1. Dimensional Rifts{ENDC}")
    print("  Explore alternate realities with unique challenges and rewards.")
    print("  Requirements: Level 35+")

    # Divine Trials
    print(f"\n{CYAN}2. Divine Trials{ENDC}")
    print("  Face the challenges of the gods to earn divine artifacts.")
    print("  Requirements: Level 40+")

    # Legendary Hunts
    print(f"\n{CYAN}3. Legendary Hunts{ENDC}")
    print("  Track down and defeat legendary monsters for rare loot.")
    print("  Requirements: Level 30+")

    # Time Trials
    print(f"\n{CYAN}4. Time Trials{ENDC}")
    print("  Complete dungeons against the clock for special rewards.")
    print("  Requirements: Complete any 3 dungeons")

    # New Game+
    print(f"\n{CYAN}5. New Game+{ENDC}")
    print("  Start a new journey with your current level and equipment.")
    print("  Requirements: Level 50+")

    # Endless Tower
    print(f"\n{CYAN}6. Endless Tower{ENDC}")
    print("  Climb the infinite tower with increasingly difficult challenges.")
    print("  Requirements: Level 35+")

    choice = input("\nEnter a number to learn more, or type 'back' to return: ")

    if choice == "1" and user_data["level"] >= 35:
        dimensional_rifts()
    elif choice == "2" and user_data["level"] >= 40:
        divine_trials()
    elif choice == "3" and user_data["level"] >= 30:
        legendary_hunts()
    elif choice == "4" and len(user_data.get("dungeons_completed", [])) >= 3:
        time_trials()
    elif choice == "5" and user_data["level"] >= 50:
        new_game_plus()
    elif choice == "6" and user_data["level"] >= 35:
        endless_tower()
    elif choice.lower() == "back":
        return
    else:
        print_colored("You don't meet the requirements or made an invalid choice.", WARNING)




# Main loop
if __name__ == "__main__":
    # Check for python3 command
    check_python_command()
    
    # Check if launched from the proper launcher
    launcher_env = os.environ.get("LAUNCHER_ACTIVE")
    if not launcher_env:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
        print(f"{Fore.BLUE}Made by andy64lol{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print("\n")  # Add a blank line for spacing
        print_animated(f"{BOLD}{CYAN}===================================================={ENDC}")
        print_animated(f"{BOLD}{CYAN}     Welcome to Legacies of our Legends RPG!{ENDC}")
        print_animated(f"{BOLD}{CYAN}===================================================={ENDC}")
        print_animated(f"{GREEN}--------------------------------------------------------------------{ENDC}")
        print_animated(f"{BOLD}{GREEN}Type '/help' for commands or '/new' to create a character.{ENDC}")
        print_animated(f"{GREEN}--------------------------------------------------------------------{ENDC}")
        print_animated(f"{BOLD}{BLUE}Made by andy64lol{ENDC}")

    # Auto-save interval in seconds
    AUTO_SAVE_INTERVAL = 300  # 5 minutes
    last_save = time.time()

    while True:
        try:
            # Auto-save check
            if time.time() - last_save > AUTO_SAVE_INTERVAL:
                auto_save()
                last_save = time.time()

            command = input(f"\n{YELLOW}>> {ENDC}").strip()
            # Do not convert to lowercase to preserve command arguments
            handle_command(command.lower())

            # Auto-save after important actions (check command prefix only)
            if command.lower().startswith(("/fight", "/dungeon", "/equip", "/travel")):
                auto_save()
                last_save = time.time()
        except Exception as e:
            print(f"{FAIL}Error: {e}{ENDC}")
            print_animated("Type '/help' for available commands.", YELLOW)
