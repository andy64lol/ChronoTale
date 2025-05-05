import sys
import random
import json
import os
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Color constants
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
CYAN = '\033[96m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[94m'
LIGHTCYAN = '\033[96m'
LIGHTYELLOW = '\033[93m'
BG_YELLOW = '\033[43m'
BG_CYAN = '\033[46m'
BG_LIGHTYELLOW = '\033[103m'
BG_LIGHTCYAN = '\033[106m'

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
    '/search': (2, 4)
}

# Commands that don't take time
NO_TICK_COMMANDS = {'/help', '/stats', '/h', '/s_t', '/inventory', '/i', '/materials', 
                   '/m', '/quests', '/q', '/save', '/load', '/prefix', '/settings',
                   '/bestiary', '/weapon_info', '/location', '/location_check',
                   '/professions', '/dungeon_list', '/mobs', '/tip', '/codes',
                   '/support', '/exit', '/x'}

# Game time tracking
game_state = {
    "current_tick": 0,
    "current_day": 0,
    "last_command_tick": 0
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
        "id": 503,
        "name": "Sabotage Supply Lines",
        "description": "Disrupt the Iron Caliphate's supply routes to weaken their forces.",
        "target": {"location": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah", "count": 1},
        "reward": {"gold": 2000, "exp": 2500, "item": "Blueprints for Resistance Gear"},
        "story": False,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 504,
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
        "id": 403,
        "name": "Assassinate a Corrupt Official",
        "description": "Eliminate a corrupt official threatening the Shogunate's peace.",
        "target": {"npc": "Corrupt Official", "count": 1},
        "reward": {"gold": 1400, "exp": 1800, "item": "Unique Samurai Weapons"},
        "story": False,
        "chapter": 4,
        "travel_locations": ["Shogunate of Shirui"]
    },
    {
        "id": 404,
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
    }
]

# Available professions with their bonuses
PROFESSIONS = {
    "Miner": {"gather_bonus": ["Iron Ore", "Gold Ore"], "craft_bonus": ["weapons"]},
    "Herbalist": {"gather_bonus": ["Red Herb"], "craft_bonus": ["potions"]},
    "Blacksmith": {"gather_bonus": ["Iron Ore"], "craft_bonus": ["armor"]},
    "Alchemist": {"gather_bonus": ["Red Herb"], "craft_bonus": ["potions"]},
    "Hunter": {"gather_bonus": ["Leather"], "craft_bonus": ["bows"]},
    "Woodcutter": {"gather_bonus": ["Wood"], "craft_bonus": ["staves"]},
    "Fisher": {"gather_bonus": ["Fish"], "craft_bonus": ["fishing gear"]},
    "Archaeologist": {"gather_bonus": ["Ancient Relic"], "craft_bonus": ["artifacts"]},
    "Enchanter": {"gather_bonus": ["Magic Crystal"], "craft_bonus": ["enchanted items"]},
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
    "dungeons_completed": []
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
        "dungeons_completed": []
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
    {"name": "Void Reaper", "level": 25, "health": 2500, "attack": 300, "drops": ["Void Scythe", "Void Crystal", "Gold Coin"], "boss": True},
    {"name": "Ancient Dragon God", "level": 30, "health": 3000, "attack": 400, "drops": ["Divine Dragon Scale", "Dragon God's Crown", "Gold Coin"], "boss": True},
    {"name": "Eternal Phoenix", "level": 28, "health": 2800, "attack": 350, "drops": ["Eternal Flame", "Phoenix Crown", "Gold Coin"], "boss": True},
    {"name": "Chaos Incarnate", "level": 35, "health": 3500, "attack": 450, "drops": ["Chaos Blade", "Chaos Crystal", "Gold Coin"], "boss": True},
    {"name": "Abyssal Overlord", "level": 40, "health": 4000, "attack": 500, "drops": ["Abyssal Crown", "Infinity Stone", "Gold Coin"], "boss": True},
    {"name": "Dragon Elite Guard", "level": 32, "health": 3200, "attack": 420, "drops": ["Elite Dragon Scale", "Dragon Guard Armor", "Gold Coin"]},
    {"name": "Phoenix Guardian", "level": 30, "health": 3000, "attack": 380, "drops": ["Phoenix Feather", "Guardian's Flame", "Gold Coin"]},
    {"name": "Chaos Spawn", "level": 33, "health": 3300, "attack": 430, "drops": ["Chaos Shard", "Spawn Crystal", "Gold Coin"]},
    {"name": "Abyss Dweller", "level": 38, "health": 3800, "attack": 480, "drops": ["Dweller's Heart", "Abyssal Fragment", "Gold Coin"]},
    {"name": "Void Dragon", "level": 45, "health": 5000, "attack": 600, "drops": ["Void Dragon Scale", "Void Crown", "Gold Coin"], "boss": True},
    {"name": "Time Keeper", "level": 42, "health": 4500, "attack": 550, "drops": ["Chronos Crystal", "Time Keeper's Staff", "Gold Coin"], "boss": True},
    {"name": "Celestial Titan", "level": 48, "health": 5500, "attack": 650, "drops": ["Celestial Heart", "Titan's Crown", "Gold Coin"], "boss": True},
    {"name": "Dimensional Horror", "level": 50, "health": 6000, "attack": 700, "drops": ["Horror Essence", "Dimensional Shard", "Gold Coin"], "boss": True}
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
    if "achievements" not in user_data:
        user_data["achievements"] = {
            "completed": set(),
            "stats": {
                "monsters_killed": 0,
                "items_crafted": 0,
                "dungeons_completed": 0,
                "crops_harvested": 0,
                "bosses_defeated": 0,
                "quests_completed": 0,
                "areas_visited": set(),
                "max_damage_dealt": 0,
                "total_gold_earned": 0,
                "rare_items_found": 0
            }
        }

    stats = user_data["achievements"]["stats"]
    completed = user_data["achievements"]["completed"]

    # Dynamic achievement checks
    achievements_conditions = {
        "First Steps": lambda: user_data["class"] is not None,
        "Monster Hunter": lambda: stats["monsters_killed"] >= 100,
        "Master Crafter": lambda: stats["items_crafted"] >= 50,
        "Dungeon Master": lambda: len(user_data.get("dungeons_completed", [])) >= 10,
        "Boss Slayer": lambda: stats["bosses_defeated"] >= 5,
        "Quest Champion": lambda: stats["quests_completed"] >= 20,
        "World Explorer": lambda: len(stats["areas_visited"]) >= 10,
        "Legendary Warrior": lambda: stats["max_damage_dealt"] >= 1000,
        "Rich Merchant": lambda: stats["total_gold_earned"] >= 10000,
        "Rare Collector": lambda: stats["rare_items_found"] >= 5,
        "Dragon Tamer": lambda: any("Dragon" in pet for pet in user_data["pets"]),
        "Master Farmer": lambda: stats["crops_harvested"] >= 100,
        "Ultimate Hero": lambda: user_data["level"] >= 50,
        "Dark Legion Nemesis": lambda: any(q["id"] == 703 and q["id"] in user_data["completed_quests"] for q in QUESTS)
    }

    # Check each achievement
    for achievement, condition in achievements_conditions.items():
        if achievement not in completed and condition():
            grant_achievement(achievement)

    # Update stats after each relevant action
    stats["areas_visited"].add(user_data["current_area"])

def grant_achievement(name):
    if name not in user_data["achievements"]["completed"]:
        user_data["achievements"]["completed"].add(name)
        reward = ACHIEVEMENTS[name]["reward"]
        for type, amount in reward.items():
            if type == "gold":
                user_data["gold"] += amount
            elif type == "exp":
                user_data["exp"] += amount
        print(f"\n🏆 Achievement Unlocked: {name}!")
        print(f"Description: {ACHIEVEMENTS[name]['desc']}")
        print(f"Reward: {reward}")

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

# Function for enhancing weapons with enchantments
def enchant_item() -> None:
    """Function to enchant weapons and armor with special effects"""
    print_header("ENCHANTMENT FORGE")

    if not user_data.get("inventory", []):
        print_colored("You don't have any items to enchant!", FAIL)
        return

    # Only show equipable items that can be enchanted
    enchantable_items = []
    for item in user_data["inventory"]:
        if isinstance(item, dict) and item.get("type") in ["weapon", "armor"]:
            enchantable_items.append(item)
        elif isinstance(item, str):
            # Check crafting recipes to see if it's a weapon or armor
            if item in CRAFTING_RECIPES:
                recipe = CRAFTING_RECIPES[item]
                if recipe.get("type") in ["weapon", "armor"]:
                    enchantable_items.append(item)

    if not enchantable_items:
        print_colored("You don't have any items that can be enchanted!", FAIL)
        return

    print_colored("Choose an item to enchant:", CYAN)
    for idx, item in enumerate(enchantable_items, 1):
        if isinstance(item, dict):
            name = item["name"]
            current_level = item.get("level", 1)
            current_enchants = item.get("enchantments", {})
            enchant_str = ", ".join([f"{ench} {lvl}" for ench, lvl in current_enchants.items()]) if current_enchants else "None"
            print(f"{idx}. {name} (Level {current_level}) - Enchantments: {enchant_str}")
        else:
            print(f"{idx}. {item}")

    try:
        choice = int(input("\nEnter item number (0 to cancel): "))
        if choice == 0:
            return
        elif 1 <= choice <= len(enchantable_items):
            selected_item = enchantable_items[choice-1]

            # If item is a string, convert to object
            if isinstance(selected_item, str):
                # Convert string item to a dictionary if it's a weapon or armor
                recipe = CRAFTING_RECIPES[selected_item]
                if recipe.get("type") == "weapon":
                    selected_item = {
                        "name": selected_item,
                        "type": "weapon",
                        "effect": recipe.get("effect", 10),
                        "level": 1,
                        "experience": 0,
                        "enchantments": {},  # Initialize enchantments here
                        "element": recipe.get("element", "Nullum")
                    }
                elif recipe.get("type") == "armor":
                    selected_item = {
                        "name": selected_item,
                        "type": "armor",
                        "effect": recipe.get("effect", 5),
                        "level": 1,
                        "experience": 0,
                        "enchantments": {}  # Initialize enchantments here
                    }

                # Remove string item from inventory
                user_data["inventory"].remove(selected_item)
                # Add structured item to inventory
                user_data["inventory"].append(selected_item)

            # Now selected_item is guaranteed to be a dictionary
            if "enchantments" not in selected_item:
                user_data["inventory"].remove(selected_item)

            # Show available enchantments for this item type
            item_type = selected_item["type"] if isinstance(selected_item, dict) and "type" in selected_item else ""
            available_enchants = []

            for enchant_name, enchant_info in ENCHANTMENTS.items():
                if item_type in enchant_info.get("applicable_to", []):
                    # Check if this enchantment is already at max level
                    current_level = 0
                    if isinstance(selected_item, dict) and "enchantments" in selected_item:
                        if enchant_name in selected_item["enchantments"]:
                            current_level = selected_item["enchantments"][enchant_name]

                    max_level = enchant_info.get("max_level", 5)

                    if current_level < max_level:
                        available_enchants.append((enchant_name, enchant_info))

            if not available_enchants:
                print_colored("This item has all possible enchantments at max level!", FAIL)
                return

            item_name = selected_item["name"] if isinstance(selected_item, dict) and "name" in selected_item else str(selected_item)
            print_colored(f"\nAvailable enchantments for {item_name}:", CYAN)
            for idx, (enchant_name, enchant_info) in enumerate(available_enchants, 1):
                if isinstance(selected_item, dict):
                    current_level = selected_item.get("enchantments", {}).get(enchant_name, 0)
                else:
                    current_level = 0
                next_level = current_level + 1
                materials = enchant_info.get("materials_per_level", {})

                print(f"{idx}. {enchant_name} {next_level} - {enchant_info['description']}")
                print("   Required materials: " + ", ".join([f"{count} {material}" for material, count in materials.items()]))

            try:
                enchant_choice = int(input("\nChoose enchantment (0 to cancel): "))
                if enchant_choice == 0:
                    return
                elif 1 <= enchant_choice <= len(available_enchants):
                    enchant_name, enchant_info = available_enchants[enchant_choice-1]

                    # Check if user has necessary materials
                    materials_needed = enchant_info.get("materials_per_level", {})
                    missing_materials = []

                    for material, count in materials_needed.items():
                        player_count = 0
                        for inv_item in user_data["inventory"]:
                            if isinstance(inv_item, str) and inv_item == material:
                                player_count += 1

                        if player_count < count:
                            missing_materials.append(f"{count - player_count} {material}")

                    if missing_materials:
                        print_colored("You don't have enough materials! Missing:", FAIL)
                        for item in missing_materials:
                            print(f"- {item}")
                        return

                    # Remove materials from inventory
                    for material, count in materials_needed.items():
                        for _ in range(count):
                            user_data["inventory"].remove(material)

                    # Apply enchantment
                    if isinstance(selected_item, dict):
                        current_level = selected_item.get("enchantments", {}).get(enchant_name, 0)
                    else:  # Handle case where selected_item is a string
                        current_level = 0
                    if "enchantments" not in selected_item:
                        if isinstance(selected_item, dict):
                            selected_item["enchantments"] = {}
                            print_colored(f"Successfully enchanted {selected_item['name']} with {enchant_name} {current_level + 1}!", OKGREEN)
                        else:
                            print_colored("This item cannot be enchanted.", FAIL)
                    if isinstance(selected_item, dict):
                        selected_item["enchantments"][enchant_name] = current_level + 1
                        print_colored(f"Successfully enchanted {selected_item['name']} with {enchant_name} {current_level + 1}!", OKGREEN)
                    else:
                        print_colored("This item cannot be enchanted.", FAIL)
                    # If equipped, update stats
                    for slot, equipped_item in user_data.get("equipped", {}).items():
                        if isinstance(equipped_item, dict) and isinstance(selected_item, dict):
                            if equipped_item.get("name") == selected_item.get("name"):
                                user_data["equipped"][slot] = selected_item
                                print_colored("Updated equipped item with new enchantment.", CYAN)
                                break
                        elif isinstance(equipped_item, str) and isinstance(selected_item, str):
                            if equipped_item == selected_item:
                                user_data["equipped"][slot] = selected_item
                                print_colored("Updated equipped item with new enchantment.", CYAN)
                                break
                else:
                    print_colored("Invalid choice.", FAIL)
            except ValueError:
                print_colored("Please enter a valid number.", FAIL)
        else:
            print_colored("Invalid choice.", FAIL)
    except ValueError:
        print_colored("Please enter a valid number.", FAIL)


# Function for upgrading weapons and armor to increase their level
def upgrade_item() -> None:
    """Function to level up weapons and armor"""
    print_header("ITEM UPGRADING")

    if not user_data.get("inventory", []):
        print_colored("You don't have any items to upgrade!", FAIL)
        return

    # Only show equipable items that can be upgraded
    upgradable_items = []
    for idx, item in enumerate(user_data["inventory"]):
        if isinstance(item, dict) and item.get("type") in ["weapon", "armor"]:
            upgradable_items.append((idx, item))
        elif isinstance(item, str) and item in CRAFTING_RECIPES:
            recipe = CRAFTING_RECIPES[item]
            if recipe.get("type") in ["weapon", "armor"]:
                upgradable_items.append((idx, item))

    if not upgradable_items:
        print_colored("You don't have any items that can be upgraded!", FAIL)
        return

    print_colored("Choose an item to upgrade:", CYAN)
    for list_idx, (_, item) in enumerate(upgradable_items, 1):
        if isinstance(item, dict):
            print(f"{list_idx}. {item['name']} (Level {item.get('level', 1)})")
        else:
            print(f"{list_idx}. {item}")

    try:
        choice = int(input("\nEnter item number (0 to cancel): "))
        if choice == 0:
            return
        if choice < 1 or choice > len(upgradable_items):
            print_colored("Invalid choice.", FAIL)
            return

        inv_idx, selected_item = upgradable_items[choice-1]

        # Convert string item to object if needed
        if isinstance(selected_item, str):
            recipe = CRAFTING_RECIPES[selected_item]
            item_type = recipe.get("type", "")
            base_stats = {
                "name": selected_item,
                "type": item_type,
                "level": 1,
                "experience": 0,
                "enchantments": {},
            }

            if item_type == "weapon":
                base_stats.update({
                    "effect": recipe.get("effect", 10),
                    "element": recipe.get("element", "Nullum")
                })
            elif item_type == "armor":
                base_stats.update({
                    "effect": recipe.get("effect", 5)
                })

            # Replace string item with object in inventory
            user_data["inventory"][inv_idx] = base_stats
            selected_item = base_stats

        # Calculate upgrade requirements
        current_level = selected_item.get("level", 1)
        base_effect = selected_item.get("effect", 10)
        item_type = selected_item.get("type", "weapon")

        # Gold cost increases with level
        gold_cost = current_level * 50

        # Material requirements
        materials_needed = {
            "Magic Crystal": current_level,
            "Iron Ore" if item_type == "weapon" else "Leather": current_level * 2
        }

        # Check resources
        if user_data.get("gold", 0) < gold_cost:
            print_colored(f"You don't have enough gold! Need {gold_cost} gold.", FAIL)
            return

        # Count materials in inventory
        material_counts = {}
        for inv_item in user_data["inventory"]:
            if isinstance(inv_item, str):
                material_counts[inv_item] = material_counts.get(inv_item, 0) + 1

        missing_materials = []
        for material, required in materials_needed.items():
            if material_counts.get(material, 0) < required:
                missing_materials.append(f"{required - material_counts.get(material, 0)} {material}")

        if missing_materials:
            print_colored("You don't have enough materials! Missing:", FAIL)
            for item in missing_materials:
                print(f"- {item}")
            return

        # Show upgrade preview
        print_colored(f"\nUpgrade {selected_item['name']} from Level {current_level} to Level {current_level + 1}:", CYAN)
        print(f"Current effect: {base_effect + (current_level - 1) * 5}")
        print(f"New effect: {base_effect + current_level * 5}")

        print("\nRequired:")
        print(f"- {gold_cost} gold")
        for material, count in materials_needed.items():
            print(f"- {count} {material}")

        if input("\nProceed with upgrade? (y/n): ").lower() != 'y':
            print_colored("Upgrade cancelled.", YELLOW)
            return

        # Deduct resources
        user_data["gold"] -= gold_cost
        for material, count in materials_needed.items():
            for _ in range(count):
                user_data["inventory"].remove(material)

        # Upgrade item
        selected_item["level"] += 1
        selected_item["effect"] = base_effect + (current_level) * 5

        # Update equipped item if needed
        for slot, equipped_item in user_data.get("equipped", {}).items():
            if isinstance(equipped_item, dict) and equipped_item.get("name") == selected_item["name"]:
                user_data["equipped"][slot] = selected_item
                print_colored("Updated equipped item with new stats.", CYAN)
                break

        print_colored(f"Successfully upgraded {selected_item['name']} to Level {selected_item['level']}!", OKGREEN)

    except ValueError:
        print_colored("Please enter a valid number.", FAIL)
    except Exception as e:
        print_colored(f"An error occurred: {str(e)}", FAIL)


# Function for opening treasure chests with random loot
def open_chest(tier: str = "Common") -> None:
    """Open a treasure chest and get random loot

    Args:
        tier: The rarity tier of the chest (Common, Uncommon, Rare, Epic, Legendary)
    """
    if tier not in CHEST_TIERS:
        print_colored(f"Invalid chest tier: {tier}", FAIL)
        return

    chest_info = CHEST_TIERS[tier]
    gold_range = chest_info.get("gold_range", (10, 50))
    item_count_range = chest_info.get("item_count_range", (1, 2))
    item_chances = chest_info.get("item_chances", {})
    equipment_rarity_chances = chest_info.get("equipment_rarity_chances", {})
    artifact_rarity_chances = chest_info.get("artifact_rarity_chances", {})

    # Get chest color based on tier
    tier_colors = {
        "Common": CYAN,
        "Uncommon": OKGREEN,
        "Rare": BLUE,
        "Epic": MAGENTA,
        "Legendary": YELLOW
    }
    chest_color = tier_colors.get(tier, CYAN)

    print_header(f"OPENING {chest_color}{tier} CHEST{ENDC}")
    print_colored(f"Opening {tier} chest...", chest_color)
    time.sleep(1)

    # Roll for gold
    gold_amount = random.randint(gold_range[0], gold_range[1])
    user_data["gold"] += gold_amount
    print_colored(f"You found {gold_amount} gold!", YELLOW)

    # Roll for items
    item_count = random.randint(item_count_range[0], item_count_range[1])

    # Common materials that could drop from chests
    common_materials = [
        "Iron Ore", "Wood", "Leather", "Magic Crystal", "Magic Dust", 
        "Fire Crystal", "Water Essence", "Earth Crystal", "Wind Crystal",
        "Ice Crystal", "Thunder Crystal", "Light Crystal", "Shadow Essence",
        "Poison Gland", "Steel Ingot", "Soul Fragment", "Plant Extract",
        "Sharpening Stone", "Steel Plate", "Swift Feather", "Spirit Essence"
    ]

    # Potions that could drop from chests
    potions = list(POTION_RECIPES.keys())

    # Equipment (weapons and armor) that could drop
    equipment = []
    for item_name, item_info in CRAFTING_RECIPES.items():
        if item_info.get("type") in ["weapon", "armor"]:
            equipment.append(item_name)

    # Artifacts that could drop
    artifacts = []
    for item_name, item_info in CRAFTING_RECIPES.items():
        if item_info.get("type") == "artifact":
            artifacts.append(item_name)

    # Roll for each item
    for i in range(item_count):
        # Determine item type
        item_roll = random.random()
        current_chance = 0

        for item_type, chance in item_chances.items():
            current_chance += chance
            if item_roll <= current_chance:
                # Found our item type!
                if item_type == "material":
                    # Roll for a material
                    material = random.choice(common_materials)
                    user_data["inventory"].append(material)
                    print_colored(f"You found {material}!", OKGREEN)

                elif item_type == "potion":
                    # Roll for a potion
                    potion = random.choice(potions)
                    user_data["inventory"].append(potion)
                    print_colored(f"You found {potion}!", CYAN)

                elif item_type == "equipment":
                    # Roll for equipment rarity
                    rarity_roll = random.random()
                    current_rarity_chance = 0
                    selected_rarity = "Common"

                    for rarity, rarity_chance in equipment_rarity_chances.items():
                        current_rarity_chance += rarity_chance
                        if rarity_roll <= current_rarity_chance:
                            selected_rarity = rarity
                            break

                    # Filter equipment by rarity (as best we can)
                    rarity_equipment = []
                    for item in equipment:
                        # For simplicity, just use some heuristics to guess rarity
                        if selected_rarity == "Legendary" and "Legendary" in item:
                            rarity_equipment.append(item)
                        elif selected_rarity == "Epic" and any(word in item for word in ["Epic", "God", "Divine"]):
                            rarity_equipment.append(item)
                        elif selected_rarity == "Rare" and not any(word in item for word in ["Common", "Basic"]):
                            rarity_equipment.append(item)
                        elif selected_rarity == "Uncommon" and not any(word in item for word in ["Common", "Basic"]):
                            rarity_equipment.append(item)
                        elif selected_rarity == "Common":
                            rarity_equipment.append(item)

                    # If no equipment matched the criteria, just use any equipment
                    if not rarity_equipment:
                        rarity_equipment = equipment

                    # Roll for a specific equipment
                    if rarity_equipment:
                        item = random.choice(rarity_equipment)
                        user_data["inventory"].append(item)

                        # Get rarity color
                        rarity_color = tier_colors.get(selected_rarity, CYAN)
                        print_colored(f"You found {rarity_color}{item}!{ENDC}", OKGREEN)

                elif item_type == "artifact":
                    # Roll for artifact rarity
                    rarity_roll = random.random()
                    current_rarity_chance = 0
                    selected_rarity = "Common"

                    for rarity, rarity_chance in artifact_rarity_chances.items():
                        current_rarity_chance += rarity_chance
                        if rarity_roll <= current_rarity_chance:
                            selected_rarity = rarity
                            break

                    # Filter artifacts by rarity
                    rarity_artifacts = []
                    for artifact_name in artifacts:
                        recipe = CRAFTING_RECIPES.get(artifact_name, {})
                        if recipe.get("rarity") == selected_rarity:
                            rarity_artifacts.append(artifact_name)

                    # If no artifacts matched the criteria, just use any artifact
                    if not rarity_artifacts:
                        rarity_artifacts = artifacts

                    # Roll for a specific artifact
                    if rarity_artifacts:
                        artifact = random.choice(rarity_artifacts)
                        user_data["inventory"].append(artifact)

                        # Get rarity color
                        artifact_info = CRAFTING_RECIPES.get(artifact, {})
                        rarity = artifact_info.get("rarity", "Common")
                        rarity_color = tier_colors.get(rarity, CYAN)

                        print_colored(f"You found {rarity_color}{artifact}!{ENDC}", YELLOW)

                break

    print_colored("\nChest looting complete!", OKGREEN)


# Function to check for artifact set bonuses based on equipped artifacts
def check_artifact_set_bonuses() -> None:
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
        "color": '\033[96m',  # CYAN
        "stat_multiplier": 1.0,
        "drop_chance": 0.5
    },
    "Uncommon": {
        "color": '\033[92m',  # OKGREEN
        "stat_multiplier": 1.2,
        "drop_chance": 0.3
    },
    "Rare": {
        "color": '\033[94m',  # BLUE
        "stat_multiplier": 1.5,
        "drop_chance": 0.15
    },
    "Epic": {
        "color": '\033[35m',  # MAGENTA
        "stat_multiplier": 1.8,
        "drop_chance": 0.04
    },
    "Legendary": {
        "color": '\033[33m',  # YELLOW
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
    }
}

# Enhanced crafting recipes with elemental weapons and artifacts
CRAFTING_RECIPES.update({
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
    {"name": "The Infinite Abyss", "monsters": ["Abyssal Overlord", "Abyss Dweller"], "loot": ["Abyssal Crown", "Infinity Stone", "Abyssal Armor"], "description": "An endless void where reality itself begins to break down."}
]


# ANSI color codes for output

# Text color (foreground)
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
CYAN = '\033[96m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
WHITE = '\033[37m'
BLACK = '\033[30m'
GREY = '\033[90m'
LIGHTRED = '\033[91m'
LIGHTGREEN = '\033[92m'
LIGHTYELLOW = '\033[93m'
LIGHTBLUE = '\033[94m'
LIGHTMAGENTA = '\033[95m'
LIGHTCYAN = '\033[96m'

# Background colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'
BG_GREY = '\033[100m'
BG_LIGHTRED = '\033[101m'
BG_LIGHTGREEN = '\033[102m'
BG_LIGHTYELLOW = '\033[103m'
BG_LIGHTBLUE = '\033[104m'
BG_LIGHTMAGENTA = '\033[105m'
BG_LIGHTCYAN = '\033[106m'
BG_BRIGHTWHITE = '\033[107m'

# Text effects
RESET = '\033[0m'
DIM = '\033[2m'
ITALIC = '\033[3m'
BLINK = '\033[5m'
REVERSE = '\033[7m'
HIDDEN = '\033[8m'
STRIKETHROUGH = '\033[9m'

def print_colored(text: str, color_code: str = "") -> None:
    print(f"{color_code}{text}{ENDC}" if color_code else text)

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
        "color": "\033[91m",  # Red
        "weakness": ["Aqua", "Gē"],
        "strength": ["Glacies", "Aer", "Pneuma"],
        "damage_type": "elemental"
    },
    "Aqua": {
        "name": "Aqua",
        "description": "The element of water, versatile and adaptive, weakens fire.",
        "color": "\033[94m",  # Blue
        "weakness": ["Fulmen", "Glacies"],
        "strength": ["Ignis", "Venēnum"],
        "damage_type": "elemental"
    },
    "Gē": {
        "name": "Gē",
        "description": "The element of earth, sturdy and grounding, absorbs electricity.",
        "color": "\033[33m",  # Yellow/Brown
        "weakness": ["Aer", "Ferrum"],
        "strength": ["Fulmen", "Ignis"],
        "damage_type": "elemental"
    },
    "Aer": {
        "name": "Aer",
        "description": "The element of air, swift and evasive, disperses poison.",
        "color": "\033[96m",  # Cyan
        "weakness": ["Ignis", "Ferrum"],
        "strength": ["Gē", "Venēnum"],
        "damage_type": "elemental"
    },
    "Fulmen": {
        "name": "Fulmen",
        "description": "The element of lightning, delivering swift, powerful strikes.",
        "color": "\033[95m",  # Magenta
        "weakness": ["Gē", "Ferrum"],
        "strength": ["Aqua", "Aer"],
        "damage_type": "elemental"
    },
    "Glacies": {
        "name": "Glacies",
        "description": "The element of ice, freezing and slowing opponents.",
        "color": "\033[96m",  # Light Cyan
        "weakness": ["Ignis", "Ferrum"],
        "strength": ["Aqua", "Aer"],
        "damage_type": "elemental"
    },
    "Lux": {
        "name": "Lux",
        "description": "The element of light, purifying and revealing the hidden.",
        "color": "\033[97m",  # White
        "weakness": ["Tenebrae"],
        "strength": ["Tenebrae", "Pneuma"],
        "damage_type": "elemental"
    },
    "Tenebrae": {
        "name": "Tenebrae",
        "description": "The element of darkness, corrupting and concealing.",
        "color": "\033[90m",  # Dark Gray
        "weakness": ["Lux"],
        "strength": ["Lux", "Pneuma"],
        "damage_type": "elemental"
    },
    "Venēnum": {
        "name": "Venēnum",
        "description": "The element of poison, inflicting toxins and weakening foes.",
        "color": "\033[92m",  # Green
        "weakness": ["Aqua", "Aer"],
        "strength": ["Gē", "Ferrum"],
        "damage_type": "elemental"
    },
    "Ferrum": {
        "name": "Ferrum",
        "description": "The element of metal, resistant and conductive.",
        "color": "\033[37m",  # Light Gray
        "weakness": ["Venēnum", "Fulmen"],
        "strength": ["Glacies", "Aer", "Gē"],
        "damage_type": "elemental"
    },
    "Pneuma": {
        "name": "Pneuma",
        "description": "The element of spirit, affecting the soul and mind.",
        "color": "\033[35m",  # Purple
        "weakness": ["Lux", "Tenebrae"],
        "strength": ["Venēnum", "Glacies"],
        "damage_type": "elemental"
    },
    "Viridia": {
        "name": "Viridia",
        "description": "The element of plants and nature, with restorative and ensnaring abilities.",
        "color": "\033[32m",  # Green
        "weakness": ["Ignis", "Venēnum"],
        "strength": ["Aqua", "Gē", "Aer"],
        "damage_type": "elemental"
    },
    "Nullum": {
        "name": "Nullum",
        "description": "Non-elemental physical damage that ignores elemental resistances.",
        "color": "\033[0m",  # Default/White
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

            # Update plant growth based on elapsed ticks
            if "farming" in user_data:
                for plot in user_data["farming"]["growth"]:
                    growth_ticks = ticks
                    user_data["farming"]["growth"][plot] += growth_ticks

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
        "/achievement_list": show_achievements,
        "/inventory_sort": sort_inventory,
        "/inventory_filter": filter_inventory,
        "/quest_complete": complete_quest,
        "/quest_list": list_active_quests,
        "/q": list_active_quests,
        "/l": load_prompt,
        "/x": exit_game,
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
    print_header("Guild Guide")
    if user_data["guild"]:
        print(f"You're part of the {user_data['guild']} guild!")
    else:
        print("You are not in a guild. Type '/join_guild [guild_name]' to join one.")

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
    if not user_data["class"]:
        print("You need to create a character first! Use /new")
        return

    if user_data["health"] <= 0:
        print("You can't fight while defeated! Use a healing potion or rest.")
        return

    print_header(f"Fighting {monster['name']}")
    monster_health = monster["health"]
    print(f"You encountered a {monster['name']} (Level {monster['level']})!")

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
        print(f"\nYou defeated the {monster['name']}!")
        exp_gain = monster["level"] * 20
        user_data["exp"] += exp_gain
        print(f"Gained {exp_gain} experience!")

        # Increment monsters killed count
        user_data["monsters_killed"] += 1

        # Check if monster is a boss
        if monster.get("boss", False):
            print(f"Congratulations! You defeated the boss {monster['name']}!")
            # Note: We no longer auto-complete dungeons here
            # Dungeon completion is now handled directly in enter_dungeon function
            # This prevents confusion between fighting bosses outside dungeons
            # and completing dungeon runs
        else:
            # Check for level up
            check_level_up()

        # Handle loot
        loot(monster)
    else:
        print("You were defeated!")
        user_data["health"] = 1  # Prevent death, set to 1 HP

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

def show_quests() -> None:
    print_header("Available Quests")

    # Check if player has Hylit companion for narration
    has_hylit = "Hylit" in user_data["pets"]

    # Show story quests first
    print("\nStory Quests:")
    story_quests = [q for q in QUESTS if q.get("story", False)
                   and q["id"] not in user_data["completed_quests"]
                   and q not in user_data["active_quests"]]

    for quest in story_quests:
        if has_hylit:
            print_animated(f"Hylit says: 'A new quest awaits you! {quest['name']}'", CYAN)
            print_animated(f"Hylit narrates: {quest['description']}", CYAN)
        else:
            print(f"\n[Chapter {quest['chapter']}] {quest['name']}")
            print(f"Description: {quest['description']}")

        print(f"Reward: {quest['reward']['gold']} gold, {quest['reward']['exp']} exp")
        if "item" in quest["reward"]:
            print(f"Special Reward: {quest['reward']['item']}")

        # Add travel requirement narration if quest has travel locations
        if "travel_locations" in quest:
            if has_hylit:
                print_animated(f"Hylit whispers: 'You must travel to these places: {', '.join(quest['travel_locations'])}'", CYAN)
            else:
                print(f"Travel to: {', '.join(quest['travel_locations'])}")

        if input("Accept story quest? (y/n): ").lower() == 'y':
            user_data["active_quests"].append(quest)
            print("Story quest accepted!")

    # Show side quests
    print("\nSide Quests:")
    side_quests = [q for q in QUESTS if not q.get("story", False)
                  and q["id"] not in user_data["completed_quests"]
                  and q not in user_data["active_quests"]]

    for quest in side_quests:
        print(f"\n{quest['name']}")
        print(f"Description: {quest['description']}")
        print(f"Reward: {quest['reward']['gold']} gold, {quest['reward']['exp']} exp")
        if input("Accept side quest? (y/n): ").lower() == 'y':
            user_data["active_quests"].append(quest)
            print("Side quest accepted!")


# Function to handle loot drops
def loot(monster: Dict) -> None:
    global user_data
    drops = monster["drops"]
    print("\nLoot found:")
    for idx, item in enumerate(drops, 1):
        print(f"{idx}. {item}")

    while True:
        try:
            choice = input(f"Choose item to take (1-{len(drops)}) or press Enter to skip: ").strip()
            if choice == "":
                print("No loot taken.")
                break
            choice_int = int(choice)
            if 1 <= choice_int <= len(drops):
                item = drops[choice_int - 1]
                if item == "Gold Coin":
                    gold_amount = random.randint(5, 15)
                    user_data["gold"] += gold_amount
                    print(f"Gained {gold_amount} gold!")
                else:
                    user_data["inventory"].append(item)
                    print(f"Added {item} to inventory!")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid input, please enter a number or press Enter to skip.")

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
def guild_join(guild_name: str) -> None:
    if user_data["guild"]:
        print(f"You are already in the guild '{user_data['guild']}'. Leave it first to join another.")
        return
    user_data["guild"] = guild_name
    print(f"You have joined the guild '{guild_name}'.")

def guild_leave() -> None:
    if not user_data["guild"]:
        print("You are not currently in any guild.")
        return
    print(f"You have left the guild '{user_data['guild']}'.")
    user_data["guild"] = None

def guild_list() -> None:
    print_header("Guild List")
    # For now, just a static list of guilds
    guilds = ["Warriors", "Mages", "Rogues", "Paladins", "Hunters"]
    for guild in guilds:
        print(f"- {guild}")

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

def train_pet(pet_name: str) -> None:
    if pet_name in user_data["pets"]:
        print(f"Training pet {pet_name}... (Feature coming soon!)")
    else:
        print(f"You do not own a pet named {pet_name}.")

def show_pets() -> None:
    print_header("Your Pets")
    if not user_data["pets"]:
        print("You have no pets.")
        return
    for pet_name in user_data["pets"]:
        if pet_name == "Hylit":
            continue
        pet_info = PETS.get(pet_name, None)
        if pet_info:
            desc = pet_info.get("description", "No description available.")
            print(f"- {pet_name}: {desc}")
        else:
            print(f"- {pet_name}: No information available.")

# Achievements system
achievements = []

def show_achievements() -> None:
    print_header("Achievements")
    if not achievements:
        print("No achievements earned yet.")
    else:
        for ach in achievements:
            print(f"- {ach}")

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
        print(f"Quest '{quest['name']}' completed! You received {gold} gold and {exp} experience.")
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
CROPS = {
    # Basic Crops
    "Wheat": {"growth_time": 2, "yield": "Wheat", "seed_cost": 10, "sell_price": 25, "biome": ["Plains", "Abundant Field"]},
    "Corn": {"growth_time": 3, "yield": "Corn", "seed_cost": 15, "sell_price": 35, "biome": ["Plains", "Abundant Field"]},
    "Tomato": {"growth_time": 4, "yield": "Tomato", "seed_cost": 20, "sell_price": 45, "biome": ["Plains", "Garden"]},
    "Potato": {"growth_time": 5, "yield": "Potato", "seed_cost": 25, "sell_price": 55, "biome": ["Plains", "Abundant Field"]},
    "Rice": {"growth_time": 6, "yield": "Rice", "seed_cost": 30, "sell_price": 65, "biome": ["Swamp", "Plains"]},
    "Carrot": {"growth_time": 3, "yield": "Carrot", "seed_cost": 15, "sell_price": 35, "biome": ["Plains", "Garden"]},
    "Lettuce": {"growth_time": 2, "yield": "Lettuce", "seed_cost": 10, "sell_price": 25, "biome": ["Plains", "Garden"]},
    "Strawberry": {"growth_time": 4, "yield": "Strawberry", "seed_cost": 25, "sell_price": 55, "biome": ["Plains", "Garden"]},

    # Special Crops
    "Golden Wheat": {"growth_time": 8, "yield": "Golden Wheat", "seed_cost": 100, "sell_price": 250, "biome": ["Plains", "Mystic Forest"]},
    "Magic Beans": {"growth_time": 10, "yield": "Magic Beans", "seed_cost": 150, "sell_price": 300, "biome": ["Mystic Forest"]},
    "Dragon Fruit": {"growth_time": 12, "yield": "Dragon Fruit", "seed_cost": 200, "sell_price": 450, "biome": ["Dragon's Peak"]},
    "Moonflower": {"growth_time": 6, "yield": "Moonflower", "seed_cost": 80, "sell_price": 200, "biome": ["Moonveil Harbor"]},
    "Frost Berries": {"growth_time": 5, "yield": "Frost Berries", "seed_cost": 90, "sell_price": 220, "biome": ["Frostvale"]},
    "Fire Peppers": {"growth_time": 7, "yield": "Fire Peppers", "seed_cost": 120, "sell_price": 280, "biome": ["Ember Hollow"]},
    "Shadow Root": {"growth_time": 9, "yield": "Shadow Root", "seed_cost": 130, "sell_price": 290, "biome": ["Shadowmere"]},
    "Crystal Bloom": {"growth_time": 11, "yield": "Crystal Bloom", "seed_cost": 180, "sell_price": 400, "biome": ["Crystal Cave"]},

    # Rare Crops
    "Phoenix Flower": {"growth_time": 15, "yield": "Phoenix Flower", "seed_cost": 500, "sell_price": 1200, "biome": ["Silent Ashes"]},
    "Dragon's Breath Plant": {"growth_time": 20, "yield": "Dragon's Breath", "seed_cost": 800, "sell_price": 2000, "biome": ["Dragon's Peak"]},
    "Celestial Herb": {"growth_time": 18, "yield": "Celestial Herb", "seed_cost": 600, "sell_price": 1500, "biome": ["Celestial Peaks"]},
    "Void Lotus": {"growth_time": 25, "yield": "Void Lotus", "seed_cost": 1000, "sell_price": 2500, "biome": ["Crimson Abyss"]}
}

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
            for crop, info in CROPS.items():
                print(f"\n{crop}:")
                print(f"  Growth Time: {info['growth_time']} cycles")
                print(f"  Seed Cost: {info['seed_cost']} gold")
                print(f"  Market Price: {info['sell_price']} gold")
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
            seeds = [mat for mat in user_data["materials"] if mat.endswith(" seeds")]

            if not seeds:
                print_colored("You don't have any seeds!", RED)
                continue

            print("\nYour seeds:")
            for seed in seeds:
                print(f"{seed}: {user_data['materials'][seed]}")

            if len(user_data["farming"]["plots"]) >= user_data["farming"]["unlocked_plots"]:
                print_colored("All plots are occupied! Harvest some crops or upgrade your farm.", RED)
                continue

            seed = input("\nWhich seeds would you like to plant? (or Enter to cancel): ")
            if seed in seeds:
                available_plots = user_data["farming"]["unlocked_plots"] - len(user_data["farming"]["plots"])
                amount = input(f"How many? (max {min(user_data['materials'][seed], available_plots)}): ")

                try:
                    amount = int(amount)
                    if amount > 0 and amount <= user_data["materials"][seed] and amount <= available_plots:
                        crop_name = seed.replace(" seeds", "")
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
            if not user_data["farming"]["plots"]:
                print("No crops planted!")
                continue

            for plot, crop in user_data["farming"]["plots"].items():
                growth = user_data["farming"]["growth"][plot]
                max_growth = CROPS[crop]["growth_time"] * TICKS_PER_DAY // 10  # Scale growth time to ticks
                status = "🌱" if growth < max_growth/3 else "🌿" if growth < max_growth*2/3 else "🌾" if growth < max_growth else "✨"
                print(f"Plot {plot}: {status} {crop} ({growth}/{max_growth} ticks) - Day {game_state['current_day']}")

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
    available_recipes = [name for name, recipe in CRAFTING_RECIPES.items()
                        if user_data["level"] >= recipe["level_required"]]

    if not available_recipes:
        print("No recipes available at your level")
        return

    print("\nAvailable recipes:")
    for i, recipe_name in enumerate(available_recipes, 1):
        recipe = CRAFTING_RECIPES[recipe_name]
        print(f"\n{i}. {recipe_name}")
        print("Required materials:")
        for material, amount in recipe["materials"].items():
            have_amount = user_data["materials"].get(material, 0)
            print(f"  - {material}: {amount} (Have: {have_amount})")
        print(f"Level required: {recipe['level_required']}")

    choice = input("\nChoose item to craft (number) or 0 to cancel: ")
    try:
        choice = int(choice)
        if choice == 0:
            return
        if 1 <= choice <= len(available_recipes):
            recipe_name = available_recipes[choice - 1]
            recipe = CRAFTING_RECIPES[recipe_name]

            # Check materials
            can_craft = True
            for material, amount in recipe["materials"].items():
                if user_data["materials"].get(material, 0) < amount:
                    print(f"Not enough {material}")
                    can_craft = False

            if can_craft:
                # Consume materials
                for material, amount in recipe["materials"].items():
                    user_data["materials"][material] -= amount

                # Add item to inventory
                user_data["inventory"].append(recipe_name)
                print(f"Successfully crafted {recipe_name}!")
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
PETS = {
    "Hylit": {"price": 0, "boost": {}, "description": "Your fairy companion and guide"},
    "Cat": {"price": 50, "boost": {"attack": 2}, "description": "A stealthy companion that boosts attack"},
    "Dog": {"price": 50, "boost": {"defense": 2}, "description": "A loyal friend that boosts defense"},
    "Dragon Hatchling": {"price": 200, "boost": {"attack": 5, "health": 10}, "description": "A baby dragon that boosts attack and health"},
    "Phoenix Chick": {"price": 200, "boost": {"health": 15}, "description": "A magical bird that boosts health"},
    "Battle Wolf": {"price": 150, "boost": {"attack": 4}, "description": "A fierce wolf that boosts attack"},
    "Guardian Bear": {"price": 150, "boost": {"defense": 4}, "description": "A strong bear that boosts defense"},
    "Spirit Fox": {"price": 175, "boost": {"exp_gain": 10}, "description": "A mystical fox that boosts experience gain"},
    "Lucky Rabbit": {"price": 100, "boost": {"gold_find": 10}, "description": "A lucky companion that helps find more gold"},
    "Mystic Owl": {"price": 125, "boost": {"intelligence": 3}, "description": "An intelligent owl that boosts intelligence"},
    "Shadow Panther": {"price": 175, "boost": {"stealth": 5}, "description": "A stealthy panther that boosts stealth"},
    "Thunder Eagle": {"price": 200, "boost": {"speed": 5}, "description": "A fast eagle that boosts speed"},
    "Abyssal Kraken Hatchling": {"price": 300, "boost": {"attack": 10, "defense": 5}, "description": "A baby kraken that boosts attack and defense"},
    "Small Copper Golem": {"price": 250, "boost": {"defense": 10}, "description": "A small golem made from copper that boosts defense"},
    "Small Silver Golem": {"price": 300, "boost": {"defense": 15}, "description": "A small golem made from silver that boosts defense"},
    "Small Titanium Golem": {"price": 350, "boost": {"defense": 25}, "description": "A small golem made from titanium that boosts defense"},
    "Hellstone Golem": {"price": 600, "boost": {"defense": 90}, "description": "A powerful golem made from hellstone that boosts defense"},
    "Abyssal Obsidian Golem": {"price": 1000, "boost": {"defense": 150}, "description": "A powerful golem made from obsidian extracted from the abyss where water and lava create contact"},
    "Abyssal Diamond Golem": {"price": 1500, "boost": {"defense": 200}, "description": "A powerful golem made from diamond extracted from the abyssal caves"}
}


def show_professions() -> None:
    print_header("Professions")

    if user_data["has_chosen_profession"]:
        print(f"Your current profession: {user_data['profession']}")
        if user_data["profession"] in PROFESSIONS:
            bonuses = PROFESSIONS[user_data["profession"]]
            print("\nProfession bonuses:")
            print(f"Gathering bonus for: {', '.join(bonuses['gather_bonus'])}")
            print(f"Crafting bonus for: {', '.join(bonuses['craft_bonus'])}")
        return

    print("Available professions:")
    for prof, bonuses in PROFESSIONS.items():
        print(f"\n{prof}:")
        print(f"  Gathering bonus: {', '.join(bonuses['gather_bonus'])}")
        print(f"  Crafting bonus: {', '.join(bonuses['craft_bonus'])}")

    choice = input("\nChoose a profession (or press Enter to skip): ").capitalize()
    if choice in PROFESSIONS:
        user_data["profession"] = choice
        user_data["has_chosen_profession"] = True
        print(f"\nYou are now a {choice}!")
    elif choice:
        print("Invalid profession choice.")

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
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(user_data["current_area"], {}).get("monsters", [])]
        if area_monsters:
            monster = random.choice(area_monsters)
            print(f"You found a {monster['name']}!")
            print(f"Level: {monster['level']}")
            print(f"Health: {monster['health']}")
            print(f"Attack: {monster['attack']}")
            print(f"Possible drops: {', '.join(monster['drops'])}")
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
