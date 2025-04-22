import sys
import random
import json
import os
import time
from typing import List, Dict, Optional
from datetime import datetime

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
    "Chapter 3: Shadows of the Past": {
        "title": "Shadows of the Past",
        "description": "Dark secrets emerge from the shadows of Shadowmere, threatening to unravel the peace. The hero must confront the darkness within.",
        "required_level": 10,
        "quest_line": ["The Shadow's Call", "Ancient Secrets", "The Final Shadow"],
        "reward": {"gold": 1000, "exp": 1500, "item": "Shadow Blade"}
    },
    "Chapter 4: The Shogunate's Struggle": {
        "title": "The Shogunate's Struggle",
        "description": "The Shogunate of Shirui faces tyranny and rebellion. The hero must navigate political intrigue and battle fierce warriors to restore balance.",
        "required_level": 15,
        "quest_line": ["Free the people", "Shogun's Challenge", "Kitsune's Secret"],
        "reward": {"gold": 1500, "exp": 2000, "item": "Samurai Armor"}
    },
    "Chapter 5: The Iron Caliphate": {
        "title": "The Iron Caliphate",
        "description": "The Iron Caliphate of Al-Khilafah Al-Hadidiyah rises with an iron fist. The hero must face powerful foes and uncover ancient mysteries.",
        "required_level": 20,
        "quest_line": ["Caliph's Wrath", "Guardian's Siege", "Knight's Honor"],
        "reward": {"gold": 2000, "exp": 2500, "item": "Iron Caliph's Crown"}
    },
    "Chapter 6: The Empire of Fire and Chains": {
        "title": "The Empire of Fire and Chains",
        "description": "The Tlācahcāyōtl Tletl Tecpanēcatl empire threatens to engulf the land in flames and chains. The hero must rally allies and ignite hope.",
        "required_level": 25,
        "quest_line": ["Emperor's Decree", "Order of the Black Sun", "Sacred Fire"],
        "reward": {"gold": 2500, "exp": 3000, "item": "Emperor's Crown"}
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
    "Thunder Staff": {"damage": 30, "speed": 1.0, "price": 1000, "effect": "thunder_damage"}
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
    # New story quests for extended chapters
    {
        "id": 401,
        "name": "Shogun's Challenge",
        "description": "Face the Shogun's elite guards and prove your strength.",
        "target": {"monster": "Shogun's Guard", "count": 3},
        "reward": {"gold": 1200, "exp": 1600, "item": "Shogun's Blade"},
        "story": True,
        "chapter": 4,
        "travel_locations": ["Shogunate Of Shirui"]
    },
    {
        "id": 402,
        "name": "Kitsune's Secret",
        "description": "Uncover the mysterious secrets of the Kitsune Warrior.",
        "target": {"monster": "Kitsune Warrior", "count": 1},
        "reward": {"gold": 1300, "exp": 1700, "item": "Kitsune Mask"},
        "story": True,
        "chapter": 4,
        "travel_locations": ["Shogunate Of Shirui"]
    },
    {
        "id": 501,
        "name": "Caliph's Wrath",
        "description": "Defend against the wrath of the Iron Caliphate's forces.",
        "target": {"monster": "Al-Hadidiyah Knight", "count": 5},
        "reward": {"gold": 1800, "exp": 2200, "item": "Knight's Shield"},
        "story": True,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 502,
        "name": "Guardian's Siege",
        "description": "Break the siege laid by the Iron Caliphate's guardians.",
        "target": {"monster": "Al-Hadidiyah Guardian", "count": 3},
        "reward": {"gold": 1900, "exp": 2300, "item": "Guardian's Blade"},
        "story": True,
        "chapter": 5,
        "travel_locations": ["The Iron Caliphate of Al-Khilafah Al-Hadidiyah"]
    },
    {
        "id": 601,
        "name": "Emperor's Decree",
        "description": "Carry out the Emperor's decree and face the Order of the Black Sun.",
        "target": {"monster": "Secret Police from The Order of the Black Sun (Yohualli Tōnatiuh)", "count": 4},
        "reward": {"gold": 2200, "exp": 2700, "item": "Black Sun Dagger"},
        "story": True,
        "chapter": 6,
        "travel_locations": ["Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains"]
    },
    {
        "id": 602,
        "name": "Order of the Black Sun",
        "description": "Infiltrate the Order and uncover their dark plans.",
        "target": {"monster": "Tlācahcāyōtl Tletl Tecpanēcatl Sorcerer", "count": 2},
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
        "travel_locations": ["Long Shui Zhen"]
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
        print(f"This item cannot be sold.")
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
    {"name": "Goblin", "level": 1, "health": 50, "attack": 10, "drops": ["Gold Coin", "Wooden Sword"]},
    {"name": "Wolf", "level": 2, "health": 60, "attack": 12, "drops": ["Wolf Pelt", "Gold Coin"]},
    {"name": "Forest Spider", "level": 1, "health": 45, "attack": 8, "drops": ["Spider Silk", "Gold Coin"]},
    {"name": "Bandit", "level": 2, "health": 65, "attack": 14, "drops": ["Leather Armor", "Gold Coin"]},
    {"name": "Dire Wolf", "level": 2, "health": 70, "attack": 15, "drops": ["Wolf Fang", "Gold Coin"]},
    {"name": "Goblin Shaman", "level": 2, "health": 55, "attack": 13, "drops": ["Goblin Staff", "Gold Coin"], "boss": True},
    {"name": "Goblin King", "level": 3, "health": 80, "attack": 20, "drops": ["Goblin Crown", "Gold Coin"],"boss": True},

    # Added missing monsters
    {"name": "Dragon Whelp", "level": 4, "health": 100, "attack": 25, "drops": ["Dragon Scale", "Gold Coin"]},
    {"name": "Shadow Master", "level": 10, "health": 300, "attack": 60, "drops": ["Shadow Master's Cloak", "Gold Coin"], "boss": True},
    {"name": "Blight Beast", "level": 7, "health": 180, "attack": 40, "drops": ["Blight Beast Claw", "Gold Coin"]},

    # Stormhaven Monsters (Level 2-3)
    {"name": "Skeleton", "level": 2, "health": 75, "attack": 15, "drops": ["Gold Coin", "Bone Armor"]},
    {"name": "Ghost", "level": 3, "health": 70, "attack": 18, "drops": ["Spirit Essence", "Gold Coin"]},
    {"name": "Storm Elemental", "level": 3, "health": 85, "attack": 20, "drops": ["Storm Crystal", "Gold Coin"]},
    {"name": "Pirate Scout", "level": 2, "health": 70, "attack": 16, "drops": ["Cutlass", "Gold Coin"]},
    {"name": "Haunted Armor", "level": 3, "health": 80, "attack": 22, "drops": ["Cursed Shield", "Gold Coin"]},
    {"name": "Sea Serpent", "level": 3, "health": 90, "attack": 25, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Dreadlord Varkhull, the Crimson Abyss Pirate Captain", "level": 5, "health": 150, "attack": 30, "drops": ["Crimson Cutlass", "Gold Coin"], "boss": True},

    # Dragon's Peak Monsters (Level 5-6)
    {"name": "Fire Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Flame Sword"]},
    {"name": "Ice Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Ice Sword"]},
    {"name": "Electrical Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Lightning Sword"]},
    {"name": "Plant Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Nature Sword"]},
    {"name": "Earth Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Earth Sword"]},
    {"name": "Wind Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Wind Sword"]},
    {"name": "Water Dragon", "level": 6, "health": 200, "attack": 35, "drops": ["Dragon Scale", "Gold Coin", "Water Sword"]},
    {"name": "Fire Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Ice Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Thunder Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Earth Wyvern", "level": 5, "health": 150, "attack": 28, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Dragon Knight", "level": 5, "health": 150, "attack": 28, "drops": ["Dragon Armor", "Gold Coin"]},
    {"name": "Water Wyvern", "level": 5, "health": 160, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Dragon Overlord", "level": 12, "health": 600, "attack": 90, "drops": ["Dragon Scale", "Dragonfire Sword", "Gold Coin"], "boss": True},

    # Crystal Cave Monsters (Level 3-4)
    {"name": "Crystal Golem", "level": 4, "health": 120, "attack": 25, "drops": ["Crystal Shard", "Gold Coin"]},
    {"name": "Cave Troll", "level": 4, "health": 130, "attack": 28, "drops": ["Troll Hide", "Gold Coin"]},
    {"name": "Crystal Spider", "level": 3, "health": 90, "attack": 22, "drops": ["Crystal Web", "Gold Coin"]},
    {"name": "Rock Elemental", "level": 4, "health": 140, "attack": 26, "drops": ["Earth Stone", "Gold Coin"]},
    {"name": "Cave Bat", "level": 3, "health": 80, "attack": 20, "drops": ["Bat Wing", "Gold Coin"]},
    {"name": "Crystal Tarantula", "level": 4, "health": 110, "attack": 24, "drops": ["Crystal Fang", "Gold Coin"]},
    {"name": "Crystal Giant Tarantula", "level": 7, "health": 200, "attack": 40, "drops": ["Crystal Eye", "Gold Coin"]},
    {"name": "Crystal Serpent", "level": 4, "health": 110, "attack": 24, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Corrupted Miner", "level": 4, "health": 115, "attack": 25, "drops": ["Miner's Pickaxe", "Gold Coin"]},

    # Shadowmere Monsters (Level 4-5)
    {"name": "Shadow Beast", "level": 4, "health": 110, "attack": 24, "drops": ["Shadow Essence", "Gold Coin"]},
    {"name": "Dark Knight", "level": 5, "health": 140, "attack": 28, "drops": ["Dark Armor", "Gold Coin"]},
    {"name": "Wraith", "level": 5, "health": 120, "attack": 30, "drops": ["Soul Gem", "Gold Coin"]},
    {"name": "Night Stalker", "level": 4, "health": 100, "attack": 26, "drops": ["Night Blade", "Gold Coin"]},
    {"name": "Shadow Assassin", "level": 5, "health": 130, "attack": 32, "drops": ["Assassin's Dagger", "Gold Coin"]},
    {"name": "Vampire", "level": 5, "health": 150, "attack": 35, "drops": ["Vampire Fang", "Gold Coin"]},
    {"name": "Undead Knight", "level": 5, "health": 160, "attack": 38, "drops": ["Undead Blade", "Gold Coin"]},
    {"name": "Undead Army General","level": 7, "health": 200, "attack": 40, "drops": ["Undead Armor", "Gold Coin"]},
    {"name": "Undead Army Commander","level": 8, "health": 250, "attack": 50, "drops": ["Undead's Blade", "Gold Coin"]},

    # Frostvale Monsters (Level 3-4)
    {"name": "Ice Troll", "level": 4, "health": 125, "attack": 26, "drops": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost Giant", "level": 4, "health": 140, "attack": 28, "drops": ["Giant's Club", "Gold Coin"]},
    {"name": "Snow Wolf", "level": 3, "health": 95, "attack": 20, "drops": ["Frost Pelt", "Gold Coin"]},
    {"name": "Ice Elemental", "level": 4, "health": 115, "attack": 24, "drops": ["Ice Crystal", "Gold Coin"]},
    {"name": "Frost Wraith", "level": 4, "health": 130, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"]},
    {"name": "Hatred frozen soul", "level": 5, "health": 150, "attack": 35, "drops": ["Frozen Soul", "Gold Coin"]},
    {"name": "Ice Revenant", "level": 5, "health": 160, "attack": 32, "drops": ["Frozen Heart", "Gold Coin"]},
    {"name": "Frost vengeful eye of the snow", "level": 7, "health": 200, "attack": 40, "drops": ["Frost Eye", "Gold Coin"]},

    # Long Shui Zhen Monsters (Level 4-8)
    {"name": "Dragon Spirit", "level": 5, "health": 130, "attack": 28, "drops": ["Spirit Pearl", "Gold Coin"]},
    {"name": "Water Elemental", "level": 4, "health": 110, "attack": 24, "drops": ["Water Essence", "Gold Coin"]},
    {"name": "Jade Warrior", "level": 5, "health": 140, "attack": 26, "drops": ["Jade Sword", "Gold Coin"]},
    {"name": "Jade General", "level": 5, "health": 150, "attack": 30, "drops": ["Jade Armor", "Gold Coin"]},
    {"name": "Jade soldier", "level": 4, "health": 120, "attack": 22, "drops": ["Jade Shield", "Gold Coin"]},
    {"name": "Jade Emperor's Guard", "level": 6, "health": 160, "attack": 32, "drops": ["Jade Shield", "Gold Coin"]},
    {"name": "Jade Emperor", "level": 8, "health": 390, "attack": 65, "drops": ["Jade Crown", "Gold Coin"]},

    # Jade Lotus Village Monsters (Level 2-3)
    {"name": "Lotus Spirit", "level": 3, "health": 85, "attack": 18, "drops": ["Lotus Petal", "Gold Coin"]},
    {"name": "Pond Serpent", "level": 2, "health": 70, "attack": 16, "drops": ["Serpent Scale", "Gold Coin"]},
    {"name": "Garden Guardian", "level": 3, "health": 90, "attack": 20, "drops": ["Sacred Charm", "Gold Coin"]},
    {"name": "Lotus Guardian", "level": 3, "health": 95, "attack": 22, "drops": ["Lotus Shield", "Gold Coin"]},
    {"name": "Koi Empress", "level": 3, "health": 100, "attack": 24, "drops": ["Koi Scale", "Gold Coin"]},

    # Silent Ashes Monsters (Level 5-6)
    {"name": "Ash Revenant", "level": 6, "health": 160, "attack": 32, "drops": ["Revenant Ash", "Gold Coin"]},
    {"name": "Cursed Wanderer", "level": 5, "health": 140, "attack": 28, "drops": ["Cursed Relic", "Gold Coin"]},
    {"name": "Phoenix", "level": 6, "health": 180, "attack": 34, "drops": ["Phoenix Feather", "Gold Coin"]},
    {"name": "Ash Wraith", "level": 5, "health": 150, "attack": 30, "drops": ["Wraith Essence", "Gold Coin"]},
    {"name": "Burnt Guardian", "level": 5, "health": 145, "attack": 29, "drops": ["Guardian's Ash", "Gold Coin"]},
    {"name": "Magmatic Knight,The fallen knight of the ashes", "level": 6, "health": 200, "attack": 40, "drops": ["Knight's Ash", "Gold Coin"]},

    # Thundercliff Hold Monsters (Level 4-5)
    {"name": "Thunder Elemental", "level": 5, "health": 130, "attack": 28, "drops": ["Storm Crystal", "Gold Coin"]},
    {"name": "Rock Wyvern", "level": 4, "health": 120, "attack": 26, "drops": ["Wyvern Scale", "Gold Coin"]},
    {"name": "Storm Hawk", "level": 4, "health": 110, "attack": 24, "drops": ["Hawk Feather", "Gold Coin"]},
    {"name": "Storm Wyvern", "level": 5, "health": 140, "attack": 30, "drops": ["Wyvern Wing", "Gold Coin"]},
    {"name": "Thunder Mage", "level": 5, "health": 150, "attack": 32, "drops": ["Thunder Staff", "Gold Coin"]},
    {"name": "Storm Guardian", "level": 5, "health": 160, "attack": 34, "drops": ["Guardian's Storm", "Gold Coin"]},
    {"name": "Vision of the Thunder,the core of the storm", "level": 5, "health": 150, "attack": 32, "drops": ["Storm Eye", "Gold Coin"]},

    # Shogunate Of Shirui Monsters (Level 5-12)
    {"name": "The Shogun", "level": 12, "health": 400, "attack": 70, "drops": ["Samurai Armor", "Gold Coin"]},
    {"name": "Shogun's Guard", "level": 8, "health": 350, "attack": 60, "drops": ["Shogun's Blade", "Gold Coin"]},
    {"name": "Jade Samurai", "level": 7, "health": 300, "attack": 50, "drops": ["Jade Armor", "Gold Coin"]},
    {"name": "Kitsune Warrior", "level": 6, "health": 250, "attack": 40, "drops": ["Kitsune Mask", "Gold Coin"]},
    {"name": "Tengu Warrior", "level": 6, "health": 240, "attack": 38, "drops": ["Tengu Feather", "Gold Coin"]},
    {"name": "Kappa Guardian", "level": 5, "health": 220, "attack": 35, "drops": ["Kappa Shell", "Gold Coin"]},
    {"name": "Oni Berserker", "level": 7, "health": 280, "attack": 45, "drops": ["Oni Mask", "Gold Coin"]},
    {"name": "Corrupted Ninja", "level": 5, "health": 200, "attack": 30, "drops": ["Ninja Star", "Gold Coin"]},
    {"name": "Shadow Samurai", "level": 6, "health": 260, "attack": 42, "drops": ["Shadow Blade", "Gold Coin"]},
    {"name": "Possessed Katana", "level": 5, "health": 210, "attack": 36, "drops": ["Cursed Katana", "Gold Coin"]},

    # The Iron Caliphate of Al-Khilafah Al-Hadidiyah Monsters (Level 7-12)
    {"name": "Az-Zālim al-Muqaddas,The Caliph of Al-Khilafah Al-Hadidiyah", "level": 12, "health": 500, "attack": 80, "drops": ["Iron Caliph's Crown", "Gold Coin"], "boss": True},
    {"name": "Al-Hadidiyah Guardian", "level": 11, "health": 450, "attack": 75, "drops": ["Guardian's Blade", "Gold Coin"]},
    {"name": "Al-Hadidiyah Knight", "level": 10, "health": 400, "attack": 70, "drops": ["Knight's Shield", "Gold Coin"]},
    {"name": "Mercenary of the caliphate", "level": 9, "health": 350, "attack": 65, "drops": ["Mercenary's Dagger", "Gold Coin"]},
    {"name": "Loyalist of the caliphate", "level": 8, "health": 300, "attack": 60, "drops": ["Loyalist's Blade", "Gold Coin"]},
    {"name": "High Priest of the caliphate", "level": 7, "health": 250, "attack": 55, "drops": ["High Priest's Staff", "Gold Coin"]},
    {"name": "Al-Hadidiyah Sorcerer", "level": 7, "health": 240, "attack": 50, "drops": ["Sorcerer's Tome", "Gold Coin"]},
    {"name": "Steel Golem", "level": 8, "health": 280, "attack": 60, "drops": ["Steel Core", "Gold Coin"]},
    {"name": "Royal Janissary", "level": 9, "health": 320, "attack": 65, "drops": ["Janissary's Blade", "Gold Coin"]},
    {"name": "Iron Caliphate General", "level": 10, "health": 370, "attack": 70, "drops": ["General's Armor", "Gold Coin"]},


    #  Tlācahcāyōtl Tletl Tecpanēcatl/Empire of the Sacred Fire and Chains Monsters (Level 7-12)
    {"name": "Tēcpatl Tlamacazqui,The Emperor of the Sacred Fire and Chains", "level": 12, "health": 550, "attack": 85, "drops": ["Emperor's Crown", "Gold Coin"], "boss": True},
    {"name": "Secret Police from The Order of the Black Sun (Yohualli Tōnatiuh)", "level": 10, "health": 400, "attack": 70, "drops": ["Black Sun Dagger", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Knight", "level": 11, "health": 450, "attack": 75, "drops": ["Knight's Shield", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Guardian", "level": 9, "health": 350, "attack": 65, "drops": ["Guardian's Blade", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Sorcerer", "level": 8, "health": 300, "attack": 60, "drops": ["Sorcerer's Tome", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl High Priest", "level": 7, "health": 250, "attack": 55, "drops": ["High Priest's Staff", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Mercenary", "level": 9, "health": 320, "attack": 65, "drops": ["Mercenary's Dagger", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Loyalist", "level": 8, "health": 280, "attack": 60, "drops": ["Loyalist's Blade", "Gold Coin"]},
    {"name": "Tlācahcāyōtl Tletl Tecpanēcatl Royal Guard", "level": 10, "health": 370, "attack": 70, "drops": ["Royal Guard's Sword", "Gold Coin"]},

     # Crimson Abyss Monsters (Level 9-16)
    {"name": "Crimson Abyss Demon", "level": 15, "health": 600, "attack": 100, "drops": ["Demon's Heart", "Gold Coin"]},
    {"name": "Crimson Abyss Knight", "level": 14, "health": 550, "attack": 90, "drops": ["Knight's Blade", "Gold Coin"]},
    {"name": "Crimson Abyss Sorcerer", "level": 13, "health": 500, "attack": 80, "drops": ["Sorcerer's Staff", "Gold Coin"]},
    {"name": "Crimson Abyss Guardian", "level": 12, "health": 450, "attack": 75, "drops": ["Guardian's Shield", "Gold Coin"]},
    {"name": "Abyssal Leviathan", "level": 16, "health": 700, "attack": 120, "drops": ["Leviathan Scale", "Gold Coin"], "boss": True},

    # The Dark Legion (Level 17-20)
    {"name": "Dark Legion Elite", "level": 17, "health": 800, "attack": 130, "drops": ["Dark Legion Armor", "Gold Coin"]},
    {"name": "Dark Legion Warlock", "level": 18, "health": 750, "attack": 140, "drops": ["Warlock Staff", "Gold Coin"]},
    {"name": "Dark Legion Commander", "level": 19, "health": 900, "attack": 150, "drops": ["Commander's Blade", "Gold Coin"]},
    {"name": "Dark Legion's Shadow Assassin", "level": 17, "health": 700, "attack": 160, "drops": ["Shadow Dagger", "Gold Coin"]},
    {"name": "Dark Legion Archpriest", "level": 18, "health": 850, "attack": 145, "drops": ["Dark Tome", "Gold Coin"]},
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
]



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
    {"name": "factory of golems", "monsters": ["Steel Golem"], "loot": ["Steel Core", "Gold Coin"]},
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
    {"name": "Dark Legion Citadel", "monsters": ["Dark Legion Elite", "Dark Legion Commander"], "loot": ["Dark Legion Armor", "Commander's Blade", "Gold Coin"]},
    {"name": "Warlock's Dark Spire", "monsters": ["Dark Legion Warlock", "Dark Legion Archpriest"], "loot": ["Warlock Staff", "Dark Tome", "Gold Coin"]},
    {"name": "Shadow Assassin's Den", "monsters": ["Dark Legion's Shadow Assassin"], "loot": ["Shadow Dagger", "Gold Coin"]},
    {"name": "The Eternal Throne", "monsters": ["Dark Legionary Supreme Lord:Noctis, the Obsidian Fallen Eternal"], "loot": ["Eternal Crown", "Obsidian Blade", "Dark Legion's Heart", "Gold Coin"]},
]


# ANSI color codes for output
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

import sys
import time

def print_colored(text: str, color_code: str = "") -> None:
    print(f"{color_code}{text}{ENDC}" if color_code else text)

def print_animated(text: str, color_code: str = "", delay: float = None) -> None:
    length = len(text)
    if delay is None:
        delay = max(0.005, min(0.03, 1.0 / (length * 10)))
    if color_code:
        sys.stdout.write(color_code)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
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

CRAFTING
/craft             - Recipes calculator
/dismantle         - Dismantling calculator
/invcalc           - Inventory calculator
/drops             - Monster drops
/enchants          - Enchantments info

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

def handle_command(cmd: str) -> None:
    allowed_commands_without_character = {"/new", "/load", "/help", "/exit", "/prefix", "/save"}
    
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

    if cmd.startswith("/talk"):
        npc_name = cmd.split(" ", 1)[1] if len(cmd.split(" ", 1)) > 1 else None
        talk_to_npc(npc_name)
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

def show_mobs(area: str = None) -> None:
    print_header("Monsters")
    if area:
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(area, {}).get("monsters", [])]
        if area_monsters:
            print(f"Monsters in {area}:")
            for monster in area_monsters:
                print(f"- {monster['name']} (Level {monster['level']})")
        else:
            print(f"No monsters found in {area}")
    else:
        current_area = user_data["current_area"]
        area_monsters = [m for m in monsters if m["name"] in LOCATIONS.get(current_area, {}).get("monsters", [])]
        if area_monsters:
            print(f"Monsters in {current_area}:")
            for monster in area_monsters:
                print(f"- {monster['name']} (Level {monster['level']})")
        else:
            print("No monsters in current area")

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
                base_damage = user_data["attack"]
                weapon_bonus = user_data["equipped"]["weapon"]["effect"] if user_data["equipped"]["weapon"] else 0
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
                defense_bonus = user_data["equipped"]["armor"]["effect"] if user_data["equipped"]["armor"] else 0
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
    try:
        save_dir = get_save_directory()
        filename = os.path.join(save_dir, f"save_{slot}.json")

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
        for monster_name in dungeon["monsters"]:
            if monsters_fought >= max_monsters:
                print_colored(f"Reached limit of {max_monsters} monsters for this dungeon (no boss present).", YELLOW)
                break
            try:
                monster = next(m for m in monsters if m["name"].lower() == monster_name.lower())
                if user_data["health"] <= 0:
                    print_colored("You were defeated! Dungeon run failed.", FAIL)
                    return
                # If monster is a boss, print special styled name
                if monster.get("boss", False):
                    boss_name = f"⋆༺ 𓆩{monster['name'].upper()}𓆪 ༻ ⋆"
                    print_colored(boss_name, FAIL)
                else:
                    print_colored(f"Encountered: {monster['name']}", CYAN)
                fight(monster)
                monsters_fought += 1
            except StopIteration:
                print_colored(f"Warning: Monster '{monster_name}' not found in database", WARNING)
                continue

        if user_data["health"] > 0:
            print_colored(f"You have completed the {dungeon['name']}!", OKGREEN)
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
    listed_dungeons = set()
    for dungeon in dungeons:
        if dungeon['name'] not in listed_dungeons:
            if dungeon['name'] in user_data.get("dungeons_completed", []):
                print(f"\033[92m- {dungeon['name']} (Completed!)\033[0m")
            else:
                print(f"- {dungeon['name']}")
            listed_dungeons.add(dungeon['name'])
    # Check for any dungeons referenced in monsters but not listed
    monster_dungeon_names = set()
    for dungeon in dungeons:
        monster_dungeon_names.add(dungeon['name'])
    unlisted_dungeons = monster_dungeon_names - listed_dungeons
    for dungeon_name in unlisted_dungeons:
        print(f"- {dungeon_name}: (Dungeon referenced by monsters but not listed)")

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
    print_header("Inventory")
    if not user_data["inventory"]:
        print("Your inventory is empty.")
        return
    for idx, item in enumerate(user_data["inventory"], 1):
        print(f"{idx}. {item}")

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
    print("Gambling feature is coming soon! Play responsibly.")

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
                    base_damage = user_data["attack"]
                    weapon_bonus = user_data["equipped"]["weapon"]["effect"] if user_data["equipped"]["weapon"] else 0
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
                    defense_bonus = user_data["equipped"]["armor"]["effect"] if user_data["equipped"]["armor"] else 0
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

def talk_to_npc(npc_name: str = None) -> None:
    if not npc_name:
        print("Which NPC would you like to talk to?")
        return

    npc = next((npc for name, npc in NPCS.items() if name.lower() == npc_name.lower()), None)
    if not npc:
        print(f"No NPC named '{npc_name}' found.")
        return

    if npc["location"] != user_data["current_area"]:
        print(f"This NPC is in {npc['location']}. You need to travel there first!")
        return

    print_header(f"Talking to {npc_name}")
    print_animated(npc["dialogues"]["greeting"], CYAN)

    while True:
        print("\nOptions:")
        print("1. Ask about quests")
        print("2. Listen to story")
        print("3. Trade/Shop")
        print("4. End conversation")

        choice = input("\nWhat would you like to do? ")

        if choice == "1" and "quests" in npc:
            print_animated(npc["dialogues"].get("quest", "No quests available."), YELLOW)
            for quest_name in npc["quests"]:
                quest = next((q for q in QUESTS if q["name"] == quest_name), None)
                if quest and quest["id"] not in user_data["completed_quests"]:
                    print(f"\nQuest: {quest['name']}")
                    print(f"Description: {quest['description']}")
                    if input("Accept quest? (y/n): ").lower() == 'y':
                        user_data["active_quests"].append(quest)
                        print("Quest accepted!")

        elif choice == "2":
            if "story" in npc["dialogues"]:
                for part, text in npc["dialogues"]["story"].items():
                    print_animated(f"\n{part.capitalize()}:", MAGENTA)
                    print_animated(text, CYAN)
                    input("\nPress Enter to continue...")
            else:
                print("This NPC has no story to tell.")

        elif choice == "3" and "shop" in npc:
            print("\nAvailable items:")
            for item in npc["shop"]:
                if item in WEAPONS:
                    print(f"{item}: {WEAPONS[item]['price']} gold")

            item = input("\nWhat would you like to buy? (or press Enter to cancel): ")
            if item in npc["shop"]:
                if item in WEAPONS and user_data["gold"] >= WEAPONS[item]["price"]:
                    user_data["gold"] -= WEAPONS[item]["price"]
                    user_data["inventory"].append(item)
                    print(f"Bought {item}!")
                else:
                    print("Not enough gold!")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")

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

    for chapter_name, chapter in STORYLINE.items():
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



