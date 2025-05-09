"""
Z_survival...
This game takes part in 2057, a new zombie virus, denominated as Necroa_A, has been spreading on Earth...
Governments did all, but they failed...
Now the world is on the edge of extinction...
You are one of the few remaining survivors...
...
Use /help to see available commands.
"""

import random
import time
import os
import json
import math
import sys
from datetime import datetime
from typing import Dict, List, Optional, Union

# Setup save folder
SAVES_FOLDER = "saves"
MAX_SAVE_SLOTS = 5

# Ensure the saves folder exists
if not os.path.exists(SAVES_FOLDER):
    os.makedirs(SAVES_FOLDER)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colorize(text, color):
        """Apply color to text."""
        return f"{color}{text}{Colors.ENDC}"

    @staticmethod
    def health_color(value, max_value):
        """Return appropriate color based on health percentage."""
        percent = value / max_value * 100
        if percent > 70:
            return Colors.GREEN
        elif percent > 30:
            return Colors.YELLOW
        else:
            return Colors.RED

# Animation utilities
class Animations:
    @staticmethod
    def type_text(text, delay=0.03):
        """Type text with a delay for animation effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def loading_bar(length=20, delay=0.05, message="Loading"):
        """Show a loading bar animation."""
        print(f"{message} ", end="")
        for i in range(length + 1):
            bar = "[" + "=" * i + " " * (length - i) + "]"
            sys.stdout.write(f"\r{message} {bar} {i * 100 // length}%")
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def zombie_animation():
        """Display a simple ASCII zombie animation."""
        frames = [
            r"""
      .-.
     (o.o)
      |=|
     __|__
   //.=|=.\\
  // .=|=. \\
  \\ .=|=. //
   \\(_=_)//
    (:| |:)
     || ||
     () ()
     || ||
     || ||
    ==' '==
            """,
            r"""
      .-.
     (-.-)
      |=|
     __|__
   //.=|=.\\
  // .=|=. \\
  \\ .=|=. //
   \\(_=_)//
    (:| |:)
     || ||
     () ()
     || ||
     || ||
    ==' '==
            """
        ]
        for _ in range(3):
            for frame in frames:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Colors.GREEN + frame + Colors.ENDC)
                time.sleep(0.3)

# Game constants
# Save file paths
SAVES_FOLDER = "saves"
SAVE_FILE = os.path.join(SAVES_FOLDER, "save.json")
DEATH_LOG_FILE = os.path.join(SAVES_FOLDER, "hardcore_death_log.json")

MAX_HEALTH = 75  # Reduced for hardcore mode
MAX_STAMINA = 80
MAX_HUNGER = 80
MAX_THIRST = 80
MAX_INVENTORY_SLOTS = 10  # Limited inventory for hardcore mode
TIME_FACTOR = 0.4  # Faster time passing in hardcore mode
HARDCORE_MODE = False  # Enable hardcore features
PERMADEATH = True  # No save loading after death
INFECTION_CHANCE = 0.15  # Chance to get infected after zombie hit
BLEED_DAMAGE = 2  # Damage per hour when bleeding
INSANITY_FACTOR = 0.02  # Insanity increases when tired, hungry, or thirsty

# Day/Night cycle constants
DAYTIME_HOURS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # 6:00 - 18:59
DAWN_DUSK_HOURS = [5, 19]  # 5:00-5:59, 19:00-19:59
NIGHT_HOURS = [20, 21, 22, 23, 0, 1, 2, 3, 4]  # 20:00 - 4:59
NIGHT_ZOMBIE_CHANCE_MODIFIER = 0.25  # Zombies more common at night
NIGHT_ZOMBIE_DAMAGE_MODIFIER = 1.2  # Zombies deal more damage at night
NIGHT_STAMINA_DRAIN_MODIFIER = 1.3  # Stamina drains faster at night
NIGHT_VISION_PENALTY = True  # Harder to see/fight at night

# Weather system constants
WEATHER_TYPES = {
    "clear": {
        "name": "Clear Sky",
        "description": "The sky is clear, offering good visibility and travel conditions.",
        "effects": "Improved rest quality, better stamina recovery, and normal zombie activity.",
        "stamina_modifier": 1.0,  # Normal stamina consumption
        "visibility_modifier": 1.0,  # Normal visibility
        "zombie_speed_modifier": 1.0,  # Normal zombie speed
        "color": Colors.CYAN,
        "symbol": "☀️",
    },
    "cloudy": {
        "name": "Cloudy",
        "description": "Gray clouds cover the sky, creating a gloomy atmosphere.",
        "effects": "Slightly reduced visibility and minor impact on resource discovery.",
        "stamina_modifier": 1.05,  # Slightly increased stamina consumption
        "visibility_modifier": 0.9,  # Slightly reduced visibility
        "zombie_speed_modifier": 1.0,  # Normal zombie speed
        "color": Colors.BLUE,
        "symbol": "☁️",
    },
    "rainy": {
        "name": "Rainy",
        "description": "Rain falls steadily, making travel more difficult and reducing visibility.",
        "effects": "Higher stamina drain, reduced visibility, but zombies move 10% slower.",
        "stamina_modifier": 1.2,  # Increased stamina consumption
        "visibility_modifier": 0.7,  # Reduced visibility
        "zombie_speed_modifier": 0.9,  # Zombies slightly slower in rain
        "color": Colors.BLUE,
        "symbol": "🌧️",
    },
    "stormy": {
        "name": "Thunderstorm",
        "description": "Lightning flashes and thunder booms as heavy rain pours down.",
        "effects": "Severe stamina drain, poor visibility, rain noise increases zombie spawns, but zombies move 20% slower.",
        "stamina_modifier": 1.3,  # Significantly increased stamina consumption
        "visibility_modifier": 0.5,  # Severely reduced visibility 
        "zombie_speed_modifier": 0.8,  # Zombies slower in heavy rain
        "color": Colors.BOLD + Colors.BLUE,
        "symbol": "⛈️",
    },
    "foggy": {
        "name": "Foggy",
        "description": "A thick fog limits visibility and conceals potential dangers.",
        "effects": "Severely reduced visibility, greatly increased zombie ambush chance, 20% higher miss chance in combat.",
        "stamina_modifier": 1.1,  # Slightly increased stamina consumption
        "visibility_modifier": 0.4,  # Severely reduced visibility
        "zombie_speed_modifier": 0.95,  # Zombies slightly slower in fog
        "color": Colors.BOLD + Colors.CYAN,
        "symbol": "🌫️",
    },
    "windy": {
        "name": "Windy",
        "description": "Strong winds blow, carrying sounds farther and making ranged attacks difficult.",
        "effects": "Reduced accuracy with ranged weapons, sounds travel further attracting more zombies, moderately reduced visibility.",
        "stamina_modifier": 1.15,  # Moderately increased stamina consumption
        "visibility_modifier": 0.8,  # Moderately reduced visibility
        "zombie_speed_modifier": 1.0,  # Normal zombie speed
        "color": Colors.YELLOW,
        "symbol": "🌬️",
    },
    "hot": {
        "name": "Heat Wave",
        "description": "Oppressive heat makes movement exhausting and accelerates dehydration.",
        "effects": "30% faster thirst depletion, higher stamina consumption, zombies move 10% faster and are more aggressive.",
        "stamina_modifier": 1.25,  # Significantly increased stamina consumption
        "visibility_modifier": 0.9,  # Slightly reduced visibility due to heat haze
        "zombie_speed_modifier": 1.1,  # Zombies more active in heat
        "thirst_modifier": 1.3,  # Increased thirst
        "color": Colors.RED,
        "symbol": "🔥",
    },
    "cold": {
        "name": "Cold Snap",
        "description": "Bitter cold makes survival harder and increases hunger.",
        "effects": "20% faster hunger depletion, higher stamina consumption, zombies are 10% slower but resources are harder to find.",
        "stamina_modifier": 1.2,  # Increased stamina consumption
        "visibility_modifier": 0.85,  # Slightly reduced visibility
        "zombie_speed_modifier": 0.9,  # Zombies slower in cold
        "hunger_modifier": 1.2,  # Increased hunger
        "color": Colors.BOLD + Colors.BLUE,
        "symbol": "❄️",
    }
}

# Scavenging areas with loot tables and risk factors
SCAVENGE_AREAS = {
    "urban": {
        "name": "Urban Center",
        "description": "The towering skyscrapers of downtown Millfield cast long shadows over streets littered with abandoned luxury cars and shattered glass. The financial district's marble-floored buildings offer hiding places for both valuable items and the walking dead. Every sound echoes between the concrete canyons, potentially drawing unwanted attention. The risk is extreme, but the rewards could be life-changing—if you survive long enough to use them.",
        "risk_level": 4,
        "zombie_chance": 0.65,
        "resource_types": {
            "food": 0.25,
            "material": 0.4,
            "weapon": 0.15,
            "medical": 0.2,
        },
        "special_items": ["pistol", "metal_scrap", "fuel", "tactical_flashlight", "office_supplies"],
        "special_item_chance": 0.15,
    },
    "residential": {
        "name": "Residential Area",
        "description": "The suburbs tell the most human stories of the apocalypse. Family photos still hang on walls, kitchen tables remain set for meals never eaten, and children's toys lie scattered across overgrown lawns. Each home is a time capsule of interrupted lives, preserving both mundane household items and the occasional well-hidden valuables. Infected former residents often remain in their homes, wandering from room to room in a grotesque parody of their previous routines. The familiar layout of these houses makes navigation easier, but complacency can be deadly.",
        "risk_level": 3,
        "zombie_chance": 0.45,
        "resource_types": {
            "food": 0.4,
            "material": 0.25,
            "weapon": 0.1,
            "medical": 0.25,
        },
        "special_items": ["kitchen_knife", "cloth", "baseball_bat", "canned_food", "family_photo"],
        "special_item_chance": 0.2,
    },
    "commercial": {
        "name": "Commercial District",
        "description": "The once-bustling heart of consumer culture now stands as a monument to humanity's former excess. Small boutiques and family-owned businesses line the cracked sidewalks, their broken windows like gaping mouths frozen in eternal screams. Cash registers sit open and empty—money being worthless now—but the stockrooms and shelves still contain overlooked treasures. Fast food restaurants and convenience stores offer the possibility of preserved food, while hardware stores might yield tools and materials. The buildings' close proximity to each other allows for quick movement between potential scavenging sites, but also limits escape routes when danger appears.",
        "risk_level": 3,
        "zombie_chance": 0.5,
        "resource_types": {
            "food": 0.35,
            "material": 0.3,
            "weapon": 0.15,
            "medical": 0.2,
        },
        "special_items": ["energy_bar", "soda", "metal_scrap", "cash_register", "store_supplies"],
        "special_item_chance": 0.25,
    },
    "medical": {
        "name": "Medical Facility",
        "description": "The antiseptic smell has long since been replaced by the unmistakable odor of decay, but hospitals and clinics remain treasure troves of life-saving supplies. Overturned gurneys block hallways, and dried bloodstains map the desperate final moments of patients and staff alike. Pharmacies may still contain medicine cabinets with untouched prescription drugs, while supply closets might hold bandages and surgical tools. These facilities saw the highest concentration of infected as the outbreak spread, meaning the halls are often crowded with medical staff and patients who succumbed to the virus. The bright fluorescent lighting that still flickers in some sections creates disorienting strobe effects that can mask approaching danger.",
        "risk_level": 4,
        "zombie_chance": 0.7,
        "resource_types": {
            "food": 0.1,
            "material": 0.15,
            "weapon": 0.05,
            "medical": 0.7,
        },
        "special_items": ["first_aid_kit", "bandage", "pain_killers", "surgical_tools", "antibiotics"],
        "special_item_chance": 0.4,
    },
    "woods": {
        "name": "Wooded Area",
        "description": "The dense forest stands as nature's sanctuary, largely unclaimed by the chaos that consumed civilization. Sunlight filters through the leafy canopy, creating dappled patterns on the undergrowth below. Wild berries and edible mushrooms grow in abundance for those who know what to look for, while fallen branches provide ready materials for tools and fire. The infected here are often solitary wanderers who stumbled in from nearby areas, their decomposing forms now moving sluggishly through the underbrush. Their limited numbers are offset by the difficulty in spotting them among the trees and shadows. The sound of birds and small animals provides a constant audio gauge—when the forest falls silent, danger is near.",
        "risk_level": 2,
        "zombie_chance": 0.3,
        "resource_types": {
            "food": 0.5,
            "material": 0.4,
            "weapon": 0.05,
            "medical": 0.05,
        },
        "special_items": ["wood", "fresh_fruit", "medicinal_herbs", "hunting_knife", "wild_game"],
        "special_item_chance": 0.3,
    },
    "highway": {
        "name": "Highway",
        "description": "The six-lane expanse of asphalt stretches to the horizon, a graveyard of vehicles caught in the ultimate traffic jam. Cars and trucks sit in eternal gridlock, many still containing the personal effects—and sometimes remains—of those who thought escape was possible. Suitcases full of now-worthless possessions litter the roadway, occasionally yielding useful items among the discarded keepsakes. Some vehicles still contain fuel in their tanks, a precious resource in the new world. The exposed nature of the highway offers good visibility but little cover when threats appear. The infected here often roam in groups that followed the sounds and lights of the last evacuation attempts.",
        "risk_level": 3,
        "zombie_chance": 0.4,
        "resource_types": {
            "food": 0.3,
            "material": 0.3,
            "weapon": 0.2,
            "medical": 0.2,
        },
        "special_items": ["fuel", "metal_scrap", "pistol_ammo", "car_battery", "roadside_flare"],
        "special_item_chance": 0.2,
    },
    "warehouse": {
        "name": "Industrial Warehouse",
        "description": "Massive steel structures housing the engines of commerce that once kept society functioning. Towering shelves filled with pallets of goods create a maze-like interior where sight lines are limited and danger can lurk around any corner. The loading docks' mechanized doors hang partially open, allowing entry for both scavengers and the infected. Forklifts and pallet jacks sit abandoned mid-task, while inventory manifests blown by the wind create ghostly paper trails across concrete floors. The most valuable resources often remain locked in shipping containers or secured storage areas, requiring both time and tools to access.",
        "risk_level": 3,
        "zombie_chance": 0.5,
        "resource_types": {
            "food": 0.2,
            "material": 0.5,
            "weapon": 0.15,
            "medical": 0.15,
        },
        "special_items": ["tools", "metal_scrap", "industrial_parts", "protective_gear", "preserved_food"],
        "special_item_chance": 0.25,
    },
    "school": {
        "name": "Educational Facility",
        "description": "The hallways that once echoed with children's voices now resonate with haunting silence, punctuated only by the occasional distant moan. Classrooms contain educational supplies that can be repurposed, while cafeterias might hold overlooked food stores. Science labs potentially contain valuable chemicals and equipment, while administrative offices might have first aid supplies and communication devices. The infected here include former students and faculty, creating a particularly disturbing atmosphere as you navigate past colorful bulletin boards and school spirit banners that celebrate achievements that will never occur.",
        "risk_level": 3,
        "zombie_chance": 0.45,
        "resource_types": {
            "food": 0.25,
            "material": 0.3,
            "weapon": 0.1,
            "medical": 0.35,
        },
        "special_items": ["textbooks", "science_equipment", "cafeteria_food", "first_aid_supplies", "sports_equipment"],
        "special_item_chance": 0.35,
    },
    "farm": {
        "name": "Agricultural Area",
        "description": "Rolling fields that once produced food for thousands now grow wild and untended. Farmhouses and barns stand as isolated islands in seas of overgrown crops, their isolation providing both safety and vulnerability. Silos might contain preserved grain, while equipment sheds hold tools and fuel for machinery. The infected here are often former farmhands and rural families, their weathered forms moving slowly across the open terrain. The wide sight lines allow you to spot danger from a distance, but also mean you can be spotted just as easily. Seasonal weather patterns dramatically affect both the available resources and the difficulty of traversing these open spaces.",
        "risk_level": 2,
        "zombie_chance": 0.3,
        "resource_types": {
            "food": 0.6,
            "material": 0.25,
            "weapon": 0.05,
            "medical": 0.1,
        },
        "special_items": ["seeds", "fertilizer", "farming_tools", "fresh_produce", "preserved_meats"],
        "special_item_chance": 0.4,
    },
    "underground": {
        "name": "Sewer System",
        "description": "The labyrinthine network beneath the city streets offers a dangerous but potentially rewarding exploration opportunity. Dripping water echoes through concrete tunnels, while the dim emergency lighting creates disorienting shadows that play tricks on the eyes. The complex system of maintenance tunnels, treatment facilities, and drainage pipes provides numerous hiding places for both valuable caches and deadly threats. The infected here move slowly in the darkness, often only revealing themselves when it's too late to retreat. The limited access points mean safety is distant, but the underground network also connects many parts of the city without the need to traverse zombie-infested streets above.",
        "risk_level": 4,
        "zombie_chance": 0.6,
        "resource_types": {
            "food": 0.1,
            "material": 0.5,
            "weapon": 0.2,
            "medical": 0.2,
        },
        "special_items": ["water_purifier", "industrial_chemicals", "maintenance_tools", "emergency_supplies", "worker_equipment"],
        "special_item_chance": 0.2,
    },
    "prison": {
        "name": "Maximum Security Cell Blocks",
        "description": "The claustrophobic corridors and cell blocks of Irongate Prison form a maze of barred doors and narrow chokepoints. Infected inmates in tattered orange jumpsuits and guards in uniform fragments roam the facility, some still chained or cuffed. The prison's isolation and security measures have kept many areas untouched since the fall, but navigating the heavily infested corridors comes with extreme risk. Armories, infirmaries, and storage areas offer unique supplies not found elsewhere.",
        "risk_level": 5,
        "zombie_chance": 0.75,
        "resource_types": {
            "food": 0.1,
            "material": 0.2,
            "weapon": 0.4,
            "medical": 0.2,
            "ammo": 0.1
        },
        "special_items": ["riot_shield", "prison_shank", "guard_baton", "pepper_spray", "handcuffs", "taser", "prison_jumpsuit", "antibiotics"],
        "special_item_chance": 0.35,
    }
}
# Define the camp upgrade system
CAMP_UPGRADES = {
    "shelter": {
        "name": "Survivor Shelter",
        "level": 1,
        "max_level": 5,
        "description": "Your home within the apocalypse, built from scavenged materials and desperate innovation. Each upgrade reinforces walls, improves insulation, and creates more secure sleeping areas. At higher levels, dedicated medical and cooking spaces enhance daily life quality.",
        "benefits": "Improves sleep quality (faster health/stamina recovery), reduces illness chance, and provides better protection from weather effects.",
        "upgrade_materials": {
            2: {"wood": 15, "metal_scrap": 5, "cloth": 10},
            3: {"wood": 25, "metal_scrap": 15, "cloth": 15, "tools": 1},
            4: {"wood": 40, "metal_scrap": 30, "cloth": 20, "tools": 2},
            5: {"wood": 60, "metal_scrap": 45, "cloth": 30, "industrial_parts": 5, "tools": 3}
        }
    },
    "barricades": {
        "name": "Defensive Barricades",
        "level": 1,
        "max_level": 5,
        "description": "The primary line of defense between you and the infected hordes. Starting as simple timber walls reinforced with scrap metal, they evolve into sophisticated defensive structures with observation points and alarm systems. Higher levels incorporate concrete elements and metal spikes that damage zombies attempting to breach the perimeter.",
        "benefits": "Increases camp security, reduces zombie attack frequency, adds damage to attacking zombies, and improves overall sleep safety.",
        "hp": 100,  # Current HP of barricades
        "max_hp": 100,  # Max HP at current level
        "upgrade_materials": {
            2: {"wood": 20, "metal_scrap": 10},
            3: {"wood": 30, "metal_scrap": 25, "tools": 1},
            4: {"wood": 40, "metal_scrap": 40, "concrete": 10, "tools": 2},
            5: {"wood": 50, "metal_scrap": 60, "concrete": 25, "industrial_parts": 3, "tools": 3}
        }
    },
    "camp_entrance": {
        "name": "Fortified Gateway",
        "level": 1,
        "max_level": 3,
        "description": "The carefully controlled access point to your sanctuary. Level 1 features a reinforced door with simple locking mechanisms. Higher levels add a security checkpoint with double-gate system creating a decontamination zone, observation platforms, and quick-deploy emergency barriers for crisis situations.",
        "benefits": "Provides faster safe entry/exit, reduces chance of zombies slipping in during your return, adds emergency lockdown options.",
        "upgrade_materials": {
            2: {"wood": 15, "metal_scrap": 20, "tools": 1},
            3: {"metal_scrap": 35, "industrial_parts": 5, "tools": 2, "electronics": 3}
        }
    },
    "machine_guns": {
        "name": "Automated Defense Turrets",
        "level": 0,
        "max_level": 3,
        "description": "Salvaged firearms mounted on swivel platforms, connected to primitive motion sensors and triggering mechanisms. At Level 1, they're manually armed systems that require regular maintenance. By Level 3, they become sophisticated automated sentries with targeting AI and adjustable sensitivity to preserve ammunition.",
        "benefits": "Automatically damages zombies during attacks, reduces barricade damage, creates safe zones around the camp perimeter.",
        "upgrade_materials": {
            1: {"metal_scrap": 15, "weapons": 2, "tools": 2, "electronics": 2},
            2: {"metal_scrap": 25, "weapons": 3, "tools": 3, "electronics": 5, "industrial_parts": 2},
            3: {"metal_scrap": 40, "weapons": 5, "tools": 4, "electronics": 10, "industrial_parts": 5}
        }
    },
    "trenches": {
        "name": "Defensive Earthworks",
        "level": 0,
        "max_level": 3,
        "description": "Strategic excavations surrounding the camp that impede zombie movement. Beginning as simple ditches, they evolve into sophisticated defensive systems with sharpened stakes, covered fighting positions, and channeling barriers that force the infected into killzones. Higher levels incorporate concrete reinforcements and primitive but effective alarm triggers.",
        "benefits": "Slows zombie approach, creates defensive positions for fighting, channels zombies away from vulnerable areas, provides early warning of attacks.",
        "upgrade_materials": {
            1: {"wood": 10, "tools": 1},
            2: {"wood": 25, "metal_scrap": 10, "tools": 2},
            3: {"wood": 40, "metal_scrap": 20, "concrete": 10, "tools": 3}
        }
    },
    "garden": {
        "name": "Sustainable Food Production",
        "level": 1,
        "max_level": 4,
        "description": "Your attempt at food independence in the apocalypse. Starting with simple vegetable plots in reclaimed soil, the system evolves to include rainwater collection, composting systems, and even primitive greenhouses for year-round growing. Higher levels incorporate aquaponics systems that combine fish farming with plant cultivation, maximizing food output from minimal resources.",
        "benefits": "Provides regular food supplies, reduces hunger decay rate, occasional surplus for crafting medical items.",
        "upgrade_materials": {
            2: {"wood": 10, "seeds": 3, "tools": 1, "fertilizer": 2},
            3: {"wood": 20, "metal_scrap": 10, "seeds": 8, "tools": 2, "fertilizer": 5, "water_purifier": 1},
            4: {"wood": 30, "metal_scrap": 25, "seeds": 15, "tools": 3, "fertilizer": 10, "water_purifier": 2, "electronics": 3}
        }
    },
    "tunnel": {
        "name": "Emergency Escape Network",
        "level": 0,
        "max_level": 2,
        "description": "A concealed underground passage that provides a last-resort escape option when the camp is overrun. Level 1 consists of a rough tunnel leading to a concealed exit beyond the barricades. Level 2 expands this into a small network with multiple exit points and emergency supply caches, potentially allowing you to circle behind attackers or reach different areas of the city without surface travel.",
        "benefits": "Provides emergency escape route, enables safer travel between certain locations, may reveal new scavenging areas.",
        "upgrade_materials": {
            1: {"wood": 15, "metal_scrap": 10, "tools": 3},
            2: {"wood": 30, "metal_scrap": 25, "concrete": 5, "tools": 5, "industrial_parts": 3}
        }
    },
    "radio": {
        "name": "Communications Center",
        "level": 0,
        "max_level": 3,
        "description": "A collection of salvaged communication equipment that keeps you informed about the outside world. Starting with a basic receiver capable of picking up emergency broadcasts, it evolves into a sophisticated setup capable of monitoring zombie movements, tracking weather patterns, and potentially communicating with other survivor enclaves. The highest level can detect military transmissions and scan for signs of organized evacuation or rescue efforts.",
        "benefits": "Provides advance warning of zombie hordes, reveals resource-rich locations, occasionally discovers special missions or survivor stories.",
        "upgrade_materials": {
            1: {"metal_scrap": 5, "electronics": 3, "batteries": 2},
            2: {"metal_scrap": 15, "electronics": 8, "batteries": 5, "tools": 2},
            3: {"metal_scrap": 25, "electronics": 15, "batteries": 10, "tools": 3, "industrial_parts": 2}
        }
    },
    "drones": {
        "name": "Aerial Reconnaissance",
        "level": 0,
        "max_level": 2,
        "description": "Salvaged or handcrafted unmanned aerial vehicles equipped with cameras and sensors. Level 1 consists of a basic model with limited range and battery life, capable of scouting the immediate surroundings. Level 2 features improved models with longer range, better cameras, and the ability to operate at night, providing crucial intelligence on zombie movements and potential resources without risking human scouts.",
        "benefits": "Scouts new locations without risk, identifies resource-rich areas, provides advance warning of threats, occasionally finds rare resources or survivors.",
        "upgrade_materials": {
            1: {"metal_scrap": 8, "electronics": 5, "batteries": 3, "tools": 2},
            2: {"metal_scrap": 20, "electronics": 15, "batteries": 8, "tools": 4, "industrial_parts": 3}
        }
    },
    "workshop": {
        "name": "Engineering Bay",
        "level": 1,
        "max_level": 5,
        "description": "The creative heart of your survival efforts, where raw materials become life-saving tools and weapons. Beginning as a simple collection of salvaged tools, it grows into a comprehensive fabrication space with specialized stations for metalworking, electronics repair, and even ammunition reloading. The highest levels incorporate power tools, precision instruments, and testing areas that allow for the creation of sophisticated weapons, traps, and survival gear previously only available through scavenging.",
        "benefits": "Enables more complex crafting recipes, improves crafted item quality, allows weapon modifications and repairs.",
        "upgrade_materials": {
            2: {"wood": 10, "metal_scrap": 15, "tools": 2},
            3: {"wood": 20, "metal_scrap": 30, "tools": 4, "industrial_parts": 3},
            4: {"wood": 30, "metal_scrap": 45, "tools": 6, "industrial_parts": 8, "electronics": 5},
            5: {"wood": 40, "metal_scrap": 60, "tools": 10, "industrial_parts": 15, "electronics": 10}
        }
    },
    "medical_bay": {
        "name": "Infirmary",
        "level": 0,
        "max_level": 3,
        "description": "A dedicated space for treating injuries and illness, crucial for long-term survival. Level 1 provides basic first aid capabilities with clean surfaces and organized supplies. Higher levels incorporate specialized equipment like IV stands, sterilization tools, and a growing pharmacy of salvaged medications. The highest level allows for minor surgical procedures, proper quarantine protocols, and the cultivation of medicinal plants to supplement dwindling pharmaceutical supplies.",
        "benefits": "Improves effectiveness of medical items, reduces illness duration, allows crafting of advanced medical supplies.",
        "upgrade_materials": {
            1: {"wood": 10, "cloth": 15, "medical": 5},
            2: {"wood": 20, "metal_scrap": 10, "cloth": 25, "medical": 10, "tools": 2},
            3: {"wood": 30, "metal_scrap": 25, "cloth": 40, "medical": 20, "tools": 4, "electronics": 5}
        }
    },
    "watchtower": {
        "name": "Observation Post",
        "level": 0,
        "max_level": 3,
        "description": "Elevated structures providing visibility over the surrounding area. Level 1 is a simple platform with basic optics for daytime observation. Higher levels add multiple towers with overlapping fields of view, nightvision capabilities, and sophisticated alarm systems that can distinguish between zombie threats and potential human allies or wildlife. The highest level incorporates weather protection, comfortable observation positions for extended watches, and communication links to the main compound.",
        "benefits": "Provides advance warning of zombie approach, reduces surprise attacks, helps identify distant resources.",
        "upgrade_materials": {
            1: {"wood": 20, "metal_scrap": 5, "tools": 1},
            2: {"wood": 35, "metal_scrap": 15, "tools": 2, "electronics": 2},
            3: {"wood": 50, "metal_scrap": 30, "tools": 3, "electronics": 5, "industrial_parts": 2}
        }
    }
}

LOCATIONS = {
    "camp": {
        "name": "Survivor Camp",
        "description": "Your fortified sanctuary surrounded by reinforced barricades and watchtowers. The only place where you can truly rest without fear of the undead. The faint glow of campfires creates an illusion of normalcy amidst the apocalypse.",
        "danger_level": 0,
        "resource_types": ["food", "medical"],
        "sleep_safety": 1.0,  # 100% safe if barricades intact
        "barricades_intact": True  # If False, safety drops to 40%
    },
    "town": {
        "name": "Abandoned Town",
        "description": "Once a bustling community filled with life and laughter, Millfield now lies in eerie silence. Abandoned vehicles rust on cracked streets, while empty homes contain the forgotten possessions of those who fled—or worse, didn't escape in time. The wind carries whispers of what once was, along with the distant moans of the infected.",
        "danger_level": 2,
        "resource_types": ["food", "weapons", "medical", "materials"],
        "sleep_safety": 0.6  # 60% safe for sleeping
    },
    "hospital": {
        "name": "St. Mary's Hospital",
        "description": "The faded red cross still hangs above the entrance to this once-sacred place of healing, now a labyrinth of dark corridors and blood-stained examination rooms. Medical supplies are abundant, but so are the infected medical staff and patients who never made it out. The emergency generators occasionally flicker to life, creating moments of surreal illumination in this temple of death.",
        "danger_level": 3,
        "resource_types": ["medical", "food"],
        "sleep_safety": 0.4  # 40% safe for sleeping
    },
    "mall": {
        "name": "Northridge Shopping Mall",
        "description": "This massive commercial complex once housed over 200 stores across three sprawling floors. Shattered display windows frame mannequins that stand in silent vigil over the chaos that claimed their shoppers. The central plaza's decorative fountain has long dried up, its basin now filled with the remnants of desperate last stands. The food court still reeks of decay, while the endless echoing halls amplify every sound—including the shuffling of undead feet searching for their next meal.",
        "danger_level": 4,
        "resource_types": ["food", "weapons", "materials", "medical"],
        "sleep_safety": 0.3  # 30% safe for sleeping
    },
    "military": {
        "name": "Fort Hyperion Military Base",
        "description": "The fallen bastion of what was supposed to be humanity's last defense. Heavy-duty fences topped with razor wire failed to contain the outbreak that started within. Armored vehicles sit abandoned in perfect formation, their occupants having joined the ranks of the undead. The weapons depot and medical facility remain largely intact—if you can navigate the hordes of military-grade zombies still wearing the tattered remains of their uniforms. High risk, but potentially the most valuable supplies in the region.",
        "danger_level": 5,
        "resource_types": ["weapons", "materials", "medical", "food"],
        "sleep_safety": 0.2  # 20% safe for sleeping
    },
    "forest": {
        "name": "Whispering Pines Forest",
        "description": "Ancient evergreens tower overhead, creating a dense canopy that filters the sunlight into ghostly beams. The undergrowth conceals both natural resources and feral infected that hunt by sound. Mushrooms and edible plants grow in abundance here, free from human interference. The gentle rustling of leaves provides a false sense of security, only to be shattered by the occasional distant howl or snap of branches underfoot. Nature reclaims what was once hers, caring little for humanity's plight.",
        "danger_level": 3,
        "resource_types": ["food", "materials", "herbs"],
        "sleep_safety": 0.5  # 50% safe for sleeping
    },
    "gas_station": {
        "name": "Last Stop Service Station",
        "description": "The neon sign hanging above this roadside establishment flickers periodically as the solar backup batteries struggle to maintain power. Rusted pumps stand like monuments to a lost civilization that once worshipped speed and convenience. The attached mini-mart has been picked over, but thorough searching might reveal overlooked treasures. Abandoned vehicles in various states of disrepair litter the cracked concrete lot, some still containing the personal effects—and occasionally remains—of their former owners.",
        "danger_level": 2,
        "resource_types": ["food", "materials", "fuel"],
        "sleep_safety": 0.6  # 60% safe for sleeping
    },
    "farm": {
        "name": "Clearwater Farm",
        "description": "This once-productive family farm lies on the outskirts of town, its fields now untended and overgrown. The weathered farmhouse and massive red barn still stand as testament to sturdy pre-apocalypse construction. Some crops continue to grow wild in the fields, offering a renewable food source if you can harvest them safely. Farm equipment sits rusting but might be salvageable for parts. Occasional infected farmhands wander aimlessly, perpetually performing their old duties in a macabre parody of life.",
        "danger_level": 2,
        "resource_types": ["food", "materials", "seeds", "tools"],
        "sleep_safety": 0.65  # 65% safe for sleeping
    },
    "school": {
        "name": "Westridge High School",
        "description": "Colorful banners announcing the spring dance still hang in the main hallway, frozen in time like everything else. Classrooms contain school supplies that can be repurposed, while the cafeteria might hold overlooked food. The gymnasium offers a large, defensible space with few entrances, making it a potential temporary shelter. Many of the infected here are teenagers, faster than most but less durable. Haunting messages scrawled on lockers and walls tell the story of the panic that ensued when the infection reached these halls of learning.",
        "danger_level": 3,
        "resource_types": ["food", "materials", "medical", "books"],
        "sleep_safety": 0.45  # 45% safe for sleeping
    },
    "police_station": {
        "name": "Millfield Police Department",
        "description": "The local law enforcement headquarters stands as a fortified island amidst the chaos. Heavy security doors and barred windows made it one of the last places to fall. The armory may still contain weapons and ammunition if it hasn't been completely looted. Cells in the holding area create natural choke points for defense, while the dispatch center might hold valuable information about evacuation efforts. Many officers turned within these walls, still wearing their tactical gear, making them some of the most dangerous infected you'll encounter.",
        "danger_level": 4,
        "resource_types": ["weapons", "ammo", "materials", "medical"],
        "sleep_safety": 0.35  # 35% safe for sleeping
    },
    "power_plant": {
        "name": "Riverside Power Plant",
        "description": "This massive industrial complex once supplied electricity to the entire region. Enormous turbines sit silent, and control rooms filled with blinking panels stand abandoned. The plant's remote location meant fewer people were present when the outbreak hit, but those who were have become particularly dangerous infected that lurk in the shadows of massive machinery. The facility's maintenance areas contain valuable tools and materials, while the employee break rooms might hold overlooked food supplies. The plant's backup generators could potentially be salvaged to power your camp.",
        "danger_level": 4,
        "resource_types": ["materials", "tools", "fuel", "electronics"],
        "sleep_safety": 0.3  # 30% safe for sleeping
    },
    "prison": {
        "name": "Irongate Correctional Facility",
        "description": "This maximum-security prison once housed the region's most dangerous criminals, now it contains something far worse. Three-story cell blocks with barred doors form a labyrinth filled with infected inmates and guards still wearing tattered uniforms. The facility's isolated location and reinforced structures make it both a treasure trove of untouched supplies and one of the most dangerous locations in the region. The armory, if accessible, would contain riot gear and weapons, while the infirmary might still have valuable medical supplies. Prisoner common areas and guard quarters could yield other resources, but the density of infected makes any exploration extremely hazardous.",
        "danger_level": 5,
        "resource_types": ["weapons", "medical", "food", "materials", "ammo"],
        "sleep_safety": 0.25,  # 25% safe for sleeping
        "scavenge_area": "prison"
    }
}

ITEMS = {
    # Weapons
    "baseball_bat": {
        "name": "Baseball Bat",
        "type": "weapon",
        "damage": 15,
        "durability": 50,
        "description": "A Louisville Slugger with 'Wildcats' painted on the barrel, likely taken from a sporting goods store or someone's garage. The grip is wrapped in duct tape for better handling, and dried bloodstains tell the story of its new purpose in the apocalypse. Excellent for delivering powerful blows while maintaining distance from the infected."
    },
    "kitchen_knife": {
        "name": "Kitchen Knife",
        "type": "weapon",
        "damage": 10,
        "durability": 30,
        "description": "A once-ordinary 8-inch chef's knife from someone's kitchen drawer, now repurposed as a last line of defense. The handle is wrapped with cloth to improve grip when slick with sweat or blood. Requires dangerous close-quarters combat, but its silent efficiency makes it ideal for stealth situations. The blade dulls quickly when used against bone."
    },
    "kitchen_fork": {
        "name": "Kitchen Fork",
        "type": "weapon",
        "damage": 6,
        "durability": 25,
        "description": "A large two-pronged fork from a kitchen set, its tines sharpened to wicked points. While not designed as a weapon, its length provides slight reach advantage in desperate situations. The metal prongs can pierce zombie flesh effectively but are prone to bending when striking bone or harder surfaces. A last-resort weapon that's better than bare hands."
    },
    "pistol": {
        "name": "9mm Handgun",
        "type": "weapon",
        "damage": 30,
        "durability": 100,
        "ammo": 0,
        "max_ammo": 10,
        "description": "A standard semi-automatic pistol, likely scavenged from a police officer or civilian gun owner. The slide shows scratch marks from desperate handling, and the grip is worn smooth from use. Provides substantial stopping power but the noise attracts every infected within hearing distance—use only when absolutely necessary or when escape is guaranteed."
    },
    "shotgun": {
        "name": "Pump-Action Shotgun",
        "type": "weapon",
        "damage": 50,
        "durability": 80,
        "ammo": 0,
        "max_ammo": 6,
        "description": "A devastating close-range weapon that can stop multiple infected with a single blast. The synthetic stock has been reinforced with metal plating, and a shoulder strap made of seat belts has been added for ease of carrying. The thunderous report will alert every zombie for hundreds of yards—but sometimes making a statement is exactly what you need."
    },
    "axe": {
        "name": "Fire Axe",
        "type": "weapon",
        "damage": 25,
        "durability": 40,
        "description": "Salvaged from a fire station or emergency box, this axe features a bright red fiberglass handle and a weathered steel head. The edge has been sharpened beyond safety regulations, transforming a rescue tool into an efficient zombie dispatcher. Its weight requires strength to wield effectively but delivers devastating results. Equally useful for breaking through doors and barricades when escape becomes necessary."
    },
    "machete": {
        "name": "Machete",
        "type": "weapon",
        "damage": 20,
        "durability": 60,
        "description": "A 24-inch agricultural tool with a single-edged blade, now serving a grimmer purpose. The black handle has been wrapped with paracord for improved grip, and a wrist loop added to prevent disarming. Its sweeping blade can strike multiple targets in a single arc, making it ideal for crowd control. The relatively thin blade retains its edge well with minimal maintenance."
    },
    "police_baton": {
        "name": "Police Tactical Baton",
        "type": "weapon",
        "damage": 18,
        "durability": 70,
        "dismantle_yield": {
            "metal_bar": 1,
            "cloth": 1
        },
        "description": "A collapsible steel baton once carried by law enforcement officers. The weighted steel tip delivers focused impact, and the rubber grip provides excellent control during strikes. Its telescoping design allows for easy concealment and rapid deployment with a flick of the wrist. While not lethal against the living, it's highly effective for temporarily stunning zombies or creating space in tight situations."
    },
    "taser": {
        "name": "Police Taser",
        "type": "weapon",
        "damage": 12,
        "durability": 15,
        "dismantle_yield": {
            "electronics": 1,
            "metal_scrap": 1,
            "small_iron_piece": 1
        },
        "description": "A law enforcement-grade electroshock weapon with limited remaining charges. The bright yellow body design contrasts with its serious purpose - to deliver temporarily paralyzing electrical current. While no longer capable of completely incapacitating the dead, it can still cause muscle spasms that momentarily interrupt a zombie's attacks. The limited battery life makes this a resource to use strategically rather than as a primary weapon."
    },
    "riot_shield": {
        "name": "Tactical Riot Shield",
        "type": "weapon",
        "damage": 8,
        "durability": 120,
        "block_chance": 40,
        "dismantle_yield": {
            "metal_scrap": 3,
            "cloth": 1
        },
        "description": "A transparent polycarbonate shield with 'POLICE' emblazoned across the front, designed to control crowds in the old world. Now it serves as mobile protection against the grasping hands and snapping teeth of the infected. The shield's curved surface can deflect attacks and create space to maneuver. While primarily defensive, the reinforced edge can be used as a blunt weapon in emergencies."
    },
    "prison_shank": {
        "name": "Improvised Prison Shank",
        "type": "weapon",
        "damage": 15,
        "durability": 20,
        "craft_recipe": {
            "metal_scrap": 1,
            "cloth": 1
        },
        "dismantle_yield": {
            "metal_scrap": 1
        },
        "description": "A crude but lethally effective weapon crafted by inmates long before the apocalypse. A toothbrush or similar handle has been melted and embedded with a sharpened piece of metal—possibly from a food tray, door hinge, or maintenance tool. The blade is wrapped with cloth and tape to form a crude grip. While fragile compared to manufactured weapons, its penetrating design makes it deadly in close quarters."
    },

    # Ammunition
    "pistol_ammo": {
        "name": "Pistol Ammunition",
        "type": "ammo",
        "weapon": "pistol",
        "count": 10,
        "description": "Rounds for pistol. Essential for ranged combat."
    },
    "shotgun_ammo": {
        "name": "Shotgun Shells",
        "type": "ammo",
        "weapon": "shotgun",
        "count": 6,
        "description": "Shells for shotgun. Powerful but rare."
    },

    # Food
    "canned_food": {
        "name": "Canned Food Assortment",
        "type": "food",
        "health": 5,
        "hunger": 40,
        "description": "A random selection of dented cans with faded labels—could be beans, soup, fruit, or something else entirely. The expiration dates are long past, but the contents remain safe, if unappetizing. Metal cans have become precious artifacts of the old world, providing essential calories in any survival situation. The distinctive 'pop' of opening one has become both a comfort and a danger, as the sound can carry in the quiet of the apocalypse."
    },
    "energy_bar": {
        "name": "Protein Energy Bar",
        "type": "food",
        "stamina": 20,
        "hunger": 15,
        "description": "A foil-wrapped rectangle of compressed nutrients, salvaged from a gym bag or abandoned convenience store. The chocolate coating has developed a white film, and the texture is more like clay than food, but these concentrated calories provide a quick energy boost when you need it most. The wrapper crinkles loudly—a luxury sound from a forgotten world."
    },
    "water_bottle": {
        "name": "Plastic Water Bottle",
        "type": "food",
        "health": 5,
        "thirst": 40,
        "description": "A half-liter bottle, slightly cloudy with age but containing the most precious resource in the apocalypse—clean water. The label has worn away, leaving only the vague outline of a mountain spring that no longer exists. The cap's seal remains unbroken, promising safe hydration amidst a world of contamination. Best consumed slowly to avoid waste."
    },
    "fresh_fruit": {
        "name": "Wild Fruit Harvest",
        "type": "food",
        "health": 10,
        "hunger": 20,
        "thirst": 15,
        "description": "A handful of nature's bounty—wild berries, small apples, or whatever happens to be in season. The vibrant colors seem almost obscene compared to the muted tones of the apocalyptic landscape. The tart, sweet flavors explode on your tongue, providing vitamins long absent from your diet of preserved foods. Each bite carries the taste of a world that continues despite humanity's fall."
    },
    "jerky": {
        "name": "Homemade Jerky Strips",
        "type": "food",
        "hunger": 30,
        "stamina": 10,
        "description": "Tough strips of dark, dried meat made by survivors who knew the old ways. Could be beef, venison, or something less identifiable—questions are luxury in the apocalypse. The heavy salt preservation and smoky flavor mask any gaminess, while providing essential protein for rebuilding muscles after exertion. The act of chewing itself requires effort, a reminder that nothing comes easy anymore."
    },
    "soda": {
        "name": "Warm Soda Can",
        "type": "food",
        "thirst": 25,
        "stamina": 15,
        "description": "An aluminum can of sugary carbonated beverage, warm and possibly decades old. The once-bright label has faded to ghostly pastels, but the contents remain mysteriously preserved. The sugar and caffeine provide a momentary energy surge, while the excessive sweetness briefly transports you to times long past. The carbonation has weakened but still provides a comforting fizz against your tongue."
    },
    "clean_water_jug": {
        "name": "Purified Water Container",
        "type": "food",
        "thirst": 80,
        "health": 5,
        "description": "A repurposed one-gallon plastic container filled with clear water that's been carefully boiled or filtered. Condensation beads on the inside, promising blessed relief from constant thirst. In the new economy, this would trade for valuable supplies or even weapons. The slight aftertaste of purification tablets is a small price to pay for avoiding the waterborne illnesses that have claimed so many since the fall."
    },
    "mre": {
        "name": "Military MRE Package",
        "type": "food",
        "hunger": 70,
        "health": 10,
        "stamina": 15,
        "description": "A vacuum-sealed miracle of pre-apocalypse engineering, designed to sustain soldiers in combat conditions. The brown plastic package contains a complete meal, heating element, utensils, and even a dessert. The contents are nearly indestructible, with a shelf-life measured in decades. The included flameless ration heater provides the luxury of a hot meal without fire—a technological marvel from a civilization that no longer exists."
    },

    # Medical
    "bandage": {
        "name": "Sterile Bandage",
        "type": "medical",
        "health": 25,
        "description": "A vacuum-sealed package containing a white cotton compress and adhesive wrap, likely scavenged from a first aid kit or pharmacy. The packaging has yellowed slightly with age, but the contents remain sterile—a critical consideration in a world where infection often means death. The familiar image of a red cross on the wrapper serves as a bittersweet reminder of organized healthcare that no longer exists."
    },
    "first_aid_kit": {
        "name": "Emergency Medical Kit",
        "type": "medical",
        "health": 60,
        "description": "A red plastic case containing a curated selection of life-saving supplies: antiseptic wipes, butterfly closures, gauze pads, medical tape, tweezers, and basic medications. The compartmentalized interior speaks to a world that once had the luxury of organization and preparation. The latches have been reinforced with duct tape, preserving the precious contents through countless relocations. In the apocalypse, this represents the difference between life and death."
    },
    "pain_killers": {
        "name": "Expired Analgesics",
        "type": "medical",
        "health": 20,
        "stamina": 10,
        "description": "A blister pack or bottle of pharmaceutical pain relievers, the label faded and the expiration date long past. The white tablets have developed a slight discoloration but retain most of their efficacy. In a world without comfort, these pills offer temporary reprieve from the constant aches of survival. The recommended dosage printed on the packaging seems quaint now—luxury instructions from a time when moderation mattered."
    },
    "antibiotics": {
        "name": "Salvaged Antibiotics",
        "type": "medical",
        "health": 40,
        "infection_cure": True,
        "description": "A partial course of broad-spectrum antibiotics in a childproof bottle with a pharmacy label too faded to read. These miracle pills represent one of the most valuable finds in the apocalypse—the power to fight bacterial infections that would otherwise be fatal. The remaining count is never enough for a full course, requiring careful rationing and calculated risk. Their existence is a reminder of medical science that can no longer be reproduced."
    },
    "prison_meds": {
        "name": "Prison Infirmary Supplies",
        "type": "medical",
        "health": 35,
        "stamina": 10,
        "description": "A small cache of institutional medical supplies from the prison infirmary - basic antiseptics, cotton swabs, adhesive bandages, and a few tablets of unknown medication. The generic packaging bears correctional facility stamps and inventory codes. Despite being basic, these items were heavily controlled in the prison environment and represent life-saving resources in the apocalypse."
    },

    # Materials
    "wood": {
        "name": "Reclaimed Lumber",
        "type": "material",
        "count": 1,
        "description": "An assortment of wooden pieces salvaged from abandoned structures—fence posts, furniture fragments, broken pallets, and splintered decorative moldings. Some pieces still bear traces of their previous purpose: faded paint, mounting holes, or decorative carvings. Each represent countless hours of pre-apocalypse craftsmanship, now reduced to raw material. The dry pieces make good kindling, while the sturdier sections can reinforce barricades."
    },
    "metal_scrap": {
        "name": "Salvaged Metal Fragments",
        "type": "material",
        "count": 1,
        "description": "A collection of rust-spotted metal pieces harvested from the skeleton of civilization—car panels, signposts, kitchen appliances, and structural components. Each piece bears witness to its origin: bent nail holes, manufacturer stamps, or oxidation patterns unique to its exposure. Sharp edges make handling dangerous without gloves, but the versatility of metal makes these scraps invaluable for reinforcement, tool-making, and weaponry."
    },
    "metal_bar": {
        "name": "Metal Bar",
        "type": "material",
        "count": 1,
        "rarity": 0.3,
        "description": "A solid bar of metal, roughly foot-long and relatively free of corrosion. Unlike the more common scraps, these intact pieces retain their structural integrity, making them invaluable for crafting items that require strength and precision. Originally part of building frameworks, vehicle chassis, or industrial equipment, these standardized components represent the exact specifications of the old world—dimensions that are increasingly difficult to reproduce without factory machinery."
    },
    "cloth": {
        "name": "Fabric Remnants",
        "type": "material",
        "count": 1,
        "description": "Assorted textile pieces recovered from abandoned homes and businesses—curtains, clothing, bedding, and upholstery. Some retain patterns or logos that spark memories of the world before. The varied textures range from soft cotton to durable canvas, each with different applications in survival. Beyond practical uses for bandages and repairs, these familiar materials provide rare moments of comfort and color in a world defined by harshness."
    },
    "metal_pipe": {
        "name": "Metal Pipe",
        "type": "material",
        "count": 1,
        "description": "A length of hollow metal tubing salvaged from plumbing systems, fence posts, or industrial structures. The sturdy cylinder shows minor rust spots but retains its structural integrity. With its excellent reach and solid weight, a metal pipe serves as both a valuable crafting component and a potential improvised weapon. Its versatility in construction makes it a prized find for any survivor looking to build or reinforce their shelter."
    },
    "glass_bottle": {
        "name": "Glass Bottle",
        "type": "material",
        "count": 1,
        "description": "An intact glass container salvaged from abandoned stores, homes, or restaurants. The transparent vessel might have once contained soda, alcohol, or condiments, but its original contents are long gone. In the new world, these fragile objects serve multiple purposes - from storing purified water to crafting incendiary weapons. The hard, breakable material can also be crushed to create sharp improvised tools in desperate situations."
    },
    "fuel": {
        "name": "Hydrocarbon Fuel",
        "type": "material",
        "count": 1,
        "description": "A container of precious liquid energy—gasoline, diesel, or kerosene—siphoned from abandoned vehicles or storage tanks. The volatile liquid sloshes in its container, emitting the once-common but now exotic aroma of refined petroleum. The amber fluid represents concentrated power in the apocalypse: the ability to run generators, power tools, create explosives, or fuel the rare working vehicle. Its flammability makes it both valuable and dangerous."
    },
    "tools": {
        "name": "Mechanical Tools",
        "type": "material",
        "count": 1,
        "description": "A collection of hand tools representing human ingenuity—hammers, screwdrivers, pliers, wrenches, or saws. Some bear the worn grips and scratched surfaces of frequent use before the fall. These implements, once commonplace, are now precious aids that multiply human capability. Beyond their practical applications for building and repair, they represent the pinnacle of pre-collapse technology: simple machines that require no power source besides human effort."
    },
    "electronics": {
        "name": "Electronic Components",
        "type": "material",
        "count": 1,
        "description": "A collection of circuit boards, wiring, batteries, switches, and other electronic parts salvaged from consumer devices. These fragments of advanced technology represent humanity's peak achievement before the fall. The intricate patterns of copper traces and silicon chips contain knowledge that is already being lost to time. While many survivors see only scrap value, those with the right skills can transform these components into communications equipment, sensors, or other devices that bridge the old world and new."
    },
    "gunpowder": {
        "name": "Recovered Gunpowder",
        "type": "material",
        "count": 1,
        "rarity": 0.1,
        "description": "A small container of the dark, granular mixture that transforms firearms from metal tubes to lethal weapons. Harvested from disassembled ammunition or carefully salvaged from abandoned reloading workshops, each grain is a precious resource in the post-apocalyptic economy. The volatile black powder requires careful handling and dry storage, as moisture renders it useless. With proper knowledge, it can be crafted into new ammunition—a skill that grows more valuable as manufactured rounds become increasingly rare."
    },
    "primer": {
        "name": "Bullet Primers",
        "type": "material",
        "count": 1,
        "rarity": 0.05,
        "description": "Tiny metal cups containing the pressure-sensitive compound that initiates the firing sequence in ammunition. These small, seemingly insignificant components are among the most difficult pieces to scavenge or reproduce in the post-apocalyptic world. Each primer represents the complex industrial chemistry of the old world—precise mixtures of compounds that remain stable until struck, then create the spark that ignites gunpowder. Their rarity makes functional ammunition an increasingly precious commodity."
    },
    "copper": {
        "name": "Copper Components",
        "type": "material",
        "count": 1,
        "rarity": 0.2,
        "description": "Various forms of the distinctive reddish-brown metal, harvested from electrical wiring, plumbing fixtures, or decorative items. Softer than steel but more malleable, copper's unique properties make it essential for certain specialized applications. In ammunition manufacturing, it's used for bullet jackets and casings due to its ductility and corrosion resistance. The metal's excellent electrical conductivity also makes it valuable for maintaining or repairing remaining technological systems."
    },
    "trigger_assembly": {
        "name": "Firearm Trigger Assembly",
        "type": "material",
        "count": 1,
        "rarity": 0.07,
        "description": "A complex arrangement of springs, sears, and levers that form the firing mechanism of a firearm. These precision-engineered components require manufacturing capabilities that no longer exist in the post-apocalyptic world. Salvaged from broken or disassembled weapons, each mechanism represents irreplaceable pre-fall technology. The compact assembly translates the simple pull of a finger into the precisely timed sequence that releases the firing pin—the mechanical heart of any functioning firearm."
    },
    "small_iron_piece": {
        "name": "Precision Iron Component",
        "type": "material",
        "count": 1,
        "rarity": 0.15,
        "description": "A small but precisely formed iron part, likely salvaged from machinery, tools, or firearms. Unlike crude scrap metal, these components retain the exact dimensions and specifications needed for complex assemblies. The material shows evidence of machine tooling—perfect edges, drilled holes, or threaded sections that would be nearly impossible to reproduce without industrial equipment. These standardized pieces bridge the gap between raw materials and functioning technology."
    },
    "machine_gun_parts": {
        "name": "Automatic Weapon Components",
        "type": "material",
        "count": 1,
        "rarity": 0.03,
        "description": "Specialized mechanisms designed specifically for automatic or semi-automatic firearms—gas blocks, bolt carriers, recoil springs, and feed mechanisms. These components represent the pinnacle of pre-fall weapons engineering, embodying solutions to the complex problems of rapid, reliable fire. Each part shows signs of precision manufacturing with tolerances measured in thousandths of an inch. In the new world, these irreplaceable components are worth more than gold to those who understand their value."
    },
    "broken_firearm": {
        "name": "Damaged Firearm",
        "type": "material",
        "count": 1,
        "rarity": 0.08,
        "description": "The remains of what was once a functional weapon, now compromised by rust, impact damage, or missing components. The barrel might be bent, the chamber cracked, or the action seized by corrosion. While no longer capable of firing safely, these ruined weapons contain valuable parts that can be salvaged—springs, pins, metal stock, and occasionally intact mechanisms. To the knowledgeable survivor, these are not useless relics but treasure troves of components for repairs or crafting."
    },
    "rifle_barrel": {
        "name": "Rifle Barrel",
        "type": "material",
        "count": 1,
        "rarity": 0.06,
        "description": "A long, cylindrical tube of precision-machined steel, designed to contain explosive pressure while accurately guiding a projectile. The spiraled rifling grooves inside the bore represent manufacturing capabilities that no longer exist in the post-apocalyptic world. The metal shows varying degrees of wear—some with pristine bores that will deliver accuracy for thousands more rounds, others with visible corrosion that compromises performance. A critical component for crafting functional firearms."
    },

    # Craftable items
    "molotov": {
        "name": "Molotov Cocktail",
        "type": "weapon",
        "damage": 35,
        "durability": 1,
        "aoe": True,
        "craft_recipe": {
            "glass_bottle": 1,
            "fuel": 1,
            "cloth": 1
        },
        "dismantle_yield": {
            "glass_bottle": 1,
            "fuel": 0.5
        },
        "description": "A glass bottle filled with scavenged fuel and topped with a fuel-soaked rag wick. This improvised incendiary weapon creates a pool of burning liquid when it shatters on impact, effective against groups of zombies or for creating temporary barriers of fire. The volatile nature of this weapon makes safe carrying a challenge, and the limited throwing range means you must get uncomfortably close to your targets. The distinctive whoosh of flames and screech of burning infected often draws more danger."
    },
    "spear": {
        "name": "Makeshift Spear",
        "type": "weapon",
        "damage": 22,
        "durability": 45,
        "reach": 2,
        "craft_recipe": {
            "wood": 1,
            "metal_pipe": 1,
            "kitchen_knife": 1,
            "cloth": 2
        },
        "dismantle_yield": {
            "wood": 1,
            "metal_pipe": 1,
            "metal_scrap": 1,
            "cloth": 1
        },
        "description": "A length of metal pipe or wooden shaft with a sharpened blade—often a kitchen knife, machete fragment, or sharpened metal—securely lashed to one end. This improvised weapon provides crucial distance when engaging the infected, allowing strikes without entering their grasp. The extended reach comes at the cost of reduced power and slow recovery between thrusts. Despite its relatively simple construction, a well-crafted spear is often a survivor's first true zombie-specific weapon."
    },
    "reinforced_bat": {
        "name": "Reinforced Baseball Bat",
        "type": "weapon",
        "damage": 30,
        "durability": 70,
        "craft_recipe": {
            "baseball_bat": 1,
            "nails": 15,
            "metal_scrap": 3,
            "cloth": 2
        },
        "dismantle_yield": {
            "baseball_bat": 1,
            "nails": 8,
            "metal_scrap": 2
        },
        "description": "A standard baseball bat that has been methodically upgraded with metal reinforcements—nails, screws, metal plates, and wrapped wire. These modifications transform a sporting good into a dedicated skull-crusher, adding both weight and durability. The additional mass requires more strength to wield effectively but delivers devastating impacts. The metal additions occasionally catch on bone or clothing, requiring a forceful tug to free the weapon after a solid hit."
    },

    # Craftable Firearms and Ammunition
    "makeshift_revolver": {
        "name": "Improvised Revolver",
        "type": "weapon",
        "damage": 25,
        "durability": 20,
        "ammo": 0,
        "max_ammo": 6,
        "ammo_type": "revolver_round",
        "craft_recipe": {
            "trigger_assembly": 1,
            "metal_bar": 3,
            "small_iron_piece": 1,
            "tools": 1
        },
        "dismantle_yield": {
            "trigger_assembly": 1,
            "metal_bar": 2,
            "small_iron_piece": 1,
            "metal_scrap": 2
        },
        "description": "A crude but functional single-action revolver laboriously handcrafted from scavenged parts. The cylinder alignment is imprecise, the rifling minimal, and the trigger pull inconsistent—but it fires when needed, usually. The heavy, unwieldy frame lacks the refinement of manufactured firearms, and occasional misfires are expected. Despite these flaws, the ability to deliver lethal force at range makes this weapon invaluable. Handle with extreme caution, as catastrophic failures are possible."
    },
    "pipe_shotgun": {
        "name": "Pipe Shotgun",
        "type": "weapon",
        "damage": 40,
        "durability": 15,
        "ammo": 0,
        "max_ammo": 1,
        "ammo_type": "shotgun_shell",
        "craft_recipe": {
            "metal_bar": 2,
            "metal_scrap": 5,
            "small_iron_piece": 2,
            "wood": 2,
            "tools": 1
        },
        "dismantle_yield": {
            "metal_bar": 1,
            "metal_scrap": 4,
            "small_iron_piece": 1,
            "wood": 1
        },
        "description": "A primitive but devastatingly effective single-shot firearm crafted from thick metal pipe fittings. This improvised shotgun must be manually reloaded after each shot, but delivers massive stopping power at close range. The simple break-action design minimizes mechanical failures, though the crude construction makes each shot a gamble. The concussive blast affects everything in a narrow cone, ideal for tight confines when surrounded. The perfect weapon for when you'll only get one shot."
    },
    "makeshift_smg": {
        "name": "Improvised SMG",
        "type": "weapon",
        "damage": 15,
        "durability": 25,
        "ammo": 0,
        "max_ammo": 20,
        "ammo_type": "pistol_round",
        "fire_rate": 3,
        "craft_recipe": {
            "trigger_assembly": 1,
            "metal_bar": 5,
            "small_iron_piece": 2,
            "machine_gun_parts": 1,
            "rifle_barrel": 1,
            "tools": 2,
            "metal_scrap": 6
        },
        "dismantle_yield": {
            "trigger_assembly": 1,
            "metal_bar": 3,
            "small_iron_piece": 1,
            "machine_gun_parts": 1,
            "metal_scrap": 4
        },
        "description": "A cobbled-together automatic weapon resembling pre-fall submachine guns, created by someone with exceptional metalworking skills. The stamped metal frame houses recovered firing mechanisms and a modified barrel—evidence of both ingenuity and desperation. It delivers a rapid, somewhat inaccurate hail of pistol ammunition, effective at clearing groups of infected at close range. The high rate of fire means ammunition depletes quickly, and the crude action jams frequently. Cooling issues limit sustained fire."
    },
    "scrap_rifle": {
        "name": "Scrap Rifle",
        "type": "weapon",
        "damage": 35,
        "durability": 30,
        "ammo": 0,
        "max_ammo": 5,
        "ammo_type": "rifle_round",
        "craft_recipe": {
            "trigger_assembly": 1,
            "metal_bar": 4,
            "rifle_barrel": 1,
            "wood": 3,
            "metal_scrap": 4,
            "small_iron_piece": 2,
            "tools": 2
        },
        "dismantle_yield": {
            "trigger_assembly": 1,
            "metal_bar": 3,
            "rifle_barrel": 1,
            "wood": 2,
            "metal_scrap": 3,
            "small_iron_piece": 1
        },
        "description": "A long-barreled firearm assembled from a salvaged rifle receiver, repurposed metal, and hand-carved wooden furniture. The bolt action requires manual cycling between shots but offers good reliability with proper maintenance. While lacking the precision of pre-fall manufacturing, a skilled craftsman has ensured reasonable accuracy at medium range. The weapon's considerable length makes it awkward in confined spaces but provides superior reach for keeping infected at a safer distance."
    },
    "revolver_round": {
        "name": "Handcrafted Revolver Ammunition",
        "type": "ammo",
        "weapon": "makeshift_revolver",
        "count": 10,
        "craft_recipe": {
            "gunpowder": 5,
            "copper": 5,
            "metal_scrap": 4,
            "primer": 2,
            "tools": 1
        },
        "description": "Hand-loaded revolver cartridges crafted from scavenged materials—recovered brass casings, lead scraps melted into crude bullets, and carefully measured gunpowder. Each round varies slightly in powder load and bullet seating, making performance inconsistent. The ammunition lacks the uniform pressure control of factory rounds, occasionally leading to squibs or excessive recoil. Despite these flaws, these handmade rounds transform a revolver from an expensive club into a functional firearm."
    },
    "pistol_round": {
        "name": "Handcrafted Pistol Ammunition",
        "type": "ammo",
        "weapon": ["pistol", "makeshift_smg"],
        "count": 15,
        "craft_recipe": {
            "gunpowder": 6,
            "copper": 7,
            "metal_scrap": 3,
            "primer": 3,
            "tools": 1
        },
        "description": "Semi-automatic pistol ammunition meticulously assembled using salvaged components. The lighter bullets and measured powder charges are designed for the higher cycling rate of semi-auto actions. Slight variations in quality are visible—some casings show tarnish, while others have minor dents. The projectiles may tumble in flight rather than maintaining perfect stability, reducing long-range accuracy but often creating more devastating wound channels at moderate distances."
    },
    "rifle_round": {
        "name": "Handcrafted Rifle Ammunition",
        "type": "ammo",
        "weapon": "scrap_rifle",
        "count": 8,
        "craft_recipe": {
            "gunpowder": 8,
            "copper": 6,
            "metal_scrap": 5,
            "primer": 2,
            "tools": 1
        },
        "description": "Long cartridges containing larger powder charges behind aerodynamic bullets, hand-loaded for use in rifles. The heavier projectiles and increased propellant deliver superior range, accuracy, and penetration compared to pistol ammunition. Creating these rounds requires significant expertise—powder must be carefully measured, bullets precisely seated, and casings inspected for stress fractures. The quality varies, but well-crafted examples rival pre-fall factory ammunition in performance."
    },
    "shotgun_shell": {
        "name": "Refilled Shotgun Shell",
        "type": "ammo",
        "weapon": ["shotgun", "pipe_shotgun"],
        "count": 6,
        "craft_recipe": {
            "gunpowder": 6,
            "metal_scrap": 8,
            "primer": 1,
            "tools": 1
        },
        "description": "Shotgun cartridges reloaded with scavenged materials—recovered plastic hulls filled with measured powder charges and improvised projectiles. Instead of uniform lead shot, these shells might contain metal scraps, ball bearings, cut nails, or whatever small, dense objects were available. The stopgap wads might be cloth, paper, or plastic. This ammunition delivers devastating close-range effectiveness despite its inconsistent pattern and occasional failure to cycle in semi-automatic shotguns."
    },
    "machine_gun_ammo": {
        "name": "Linked Machine Gun Ammunition",
        "type": "ammo",
        "weapon": "machine_gun",
        "count": 30,
        "craft_recipe": {
            "gunpowder": 15,
            "copper": 12,
            "metal_scrap": 10,
            "primer": 6,
            "tools": 2,
            "metal_bar": 1
        },
        "description": "A belt of linked cartridges designed for high-volume automatic fire in machine guns. Creating these rounds represents the pinnacle of post-apocalyptic ammunition crafting—each cartridge must meet exact specifications to avoid jamming the delicate feeding mechanisms. The metal links connecting each round are often salvaged from pre-fall belts and carefully cleaned and inspected. The substantial resources required to produce this ammunition make it among the most valuable currencies in survivor enclaves."
    }
}

ZOMBIE_TYPES = {
    "walker": {
        "name": "Walker",
        "health": 30,
        "damage": 10,
        "speed": 1,
        "description": "Slow but persistent. The most common type of zombie."
    },
    "runner": {
        "name": "Runner",
        "health": 20,
        "damage": 15,
        "speed": 3,
        "description": "Fast and aggressive. Can catch you off guard."
    },
    "brute": {
        "name": "Brute",
        "health": 80,
        "damage": 25,
        "speed": 1,
        "description": "Very tough but slow. A real threat in close quarters."
    },
    "spitter": {
        "name": "Spitter",
        "health": 25,
        "damage": 15,
        "range": 2,
        "speed": 2,
        "description": "Can attack from a distance with acidic projectiles."
    },
    "stalker": {
        "name": "Forest Stalker",
        "health": 35,
        "damage": 20,
        "speed": 2,
        "stealth": 3,
        "description": "Camouflaged zombie that lurks in wooded areas. Hard to spot until it's too late."
    },

    # Boss zombies
    "tank": {
        "name": "Tank",
        "health": 200,
        "damage": 30,
        "speed": 1,
        "armor": 5,
        "is_boss": True,
        "special_ability": "armor",
        "description": "A massive zombie covered in hardened skin. Takes reduced damage from all attacks."
    },
    "screamer": {
        "name": "Screamer",
        "health": 120,
        "damage": 20,
        "speed": 2,
        "is_boss": True,
        "special_ability": "summon",
        "description": "A terrifying zombie that can emit ear-piercing screams to call other zombies to its aid."
    },
    "hunter": {
        "name": "Hunter",
        "health": 150,
        "damage": 25,
        "speed": 4,
        "dodge": 3,
        "is_boss": True,
        "special_ability": "leap",
        "description": "An agile zombie that can leap great distances and is hard to hit due to its acrobatic movements."
    },
    "necromancer": {
        "name": "Necromancer",
        "health": 140,
        "damage": 15,
        "speed": 1,
        "is_boss": True,
        "special_ability": "revive",
        "description": "A mysterious zombie that seems to have the ability to reanimate the dead. Can heal itself during combat."
    },
    "behemoth": {
        "name": "Behemoth",
        "health": 300,
        "damage": 40,
        "speed": 1,
        "is_boss": True,
        "special_ability": "rage",
        "description": "A colossal zombie that gets stronger as it takes damage. The final challenge for any survivor."
    }
}

MISSIONS = {
    "tutorial": {
        "name": "Learning the Ropes",
        "description": "Learn basic survival skills at the camp.",
        "objective": "Complete basic training",
        "location": "camp",
        "reward": {"xp": 50, "item": "bandage", "count": 2},
        "completion_text": "You've learned the basics of survival. Take these bandages, you'll need them."
    },
    "food_run": {
        "name": "Food Run",
        "description": "The camp is running low on food. Gather supplies from the abandoned town.",
        "objective": "Collect 3 food items",
        "location": "town",
        "reward": {"xp": 100, "item": "energy_bar", "count": 1},
        "completion_text": "Thank you! These supplies will help everyone at the camp."
    },
    "medical_emergency": {
        "name": "Medical Emergency",
        "description": "A survivor is badly injured. Find medical supplies at the hospital.",
        "objective": "Find a first aid kit",
        "location": "hospital",
        "reward": {"xp": 150, "item": "pistol_ammo", "count": 5},
        "completion_text": "You saved a life today. Take this ammunition as thanks."
    },
    "secure_perimeter": {
        "name": "Secure the Perimeter",
        "description": "The camp's defenses are weakening. Collect materials to reinforce them.",
        "objective": "Collect 5 material items",
        "location": "town",
        "reward": {"xp": 120, "item": "kitchen_knife", "count": 1},
        "completion_text": "The camp is safer now thanks to you. This knife might come in handy."
    },
    "weapon_cache": {
        "name": "Weapon Cache",
        "description": "Rumors of a hidden weapon cache in the military outpost.",
        "objective": "Find the weapon cache",
        "location": "military",
        "reward": {"xp": 200, "item": "shotgun", "count": 1},
        "completion_text": "You found the cache! This shotgun will be extremely useful."
    },
    "forest_hunt": {
        "name": "Forest Hunt",
        "description": "A strange new type of zombie has been spotted in the forest. Investigate the area.",
        "objective": "Kill a Forest Stalker zombie",
        "location": "forest",
        "reward": {"xp": 180, "item": "machete", "count": 1},
        "completion_text": "You've eliminated the forest stalker! This machete will be useful for future expeditions."
    },
    "fuel_gathering": {
        "name": "Fuel Run",
        "description": "The camp needs fuel to run the generator. Check the abandoned gas station.",
        "objective": "Collect 3 fuel containers",
        "location": "gas_station",
        "reward": {"xp": 130, "item": "first_aid_kit", "count": 1},
        "completion_text": "With this fuel, we can keep the lights on for a while. Take this first aid kit as thanks."
    },

    # Boss missions
    "hospital_nightmare": {
        "name": "Hospital Nightmare",
        "description": "Frightening screams have been heard from the hospital. Investigate and eliminate whatever's causing them.",
        "objective": "Defeat the Screamer boss",
        "location": "hospital",
        "boss_type": "screamer",
        "min_level": 5,
        "reward": {"xp": 300, "item": "rifle", "count": 1},
        "completion_text": "You've defeated the horrifying Screamer! The hospital is safer now, and this rifle will help you face future threats."
    },
    "tank_buster": {
        "name": "Tank Buster",
        "description": "A massive zombie has been spotted at the military outpost. It seems impervious to normal weapons.",
        "objective": "Defeat the Tank boss",
        "location": "military",
        "boss_type": "tank",
        "min_level": 6,
        "reward": {"xp": 350, "item": "molotov", "count": 3},
        "completion_text": "The Tank has fallen! Its armor was tough, but you prevailed. These Molotov cocktails should help with other tough enemies."
    },
    "forest_predator": {
        "name": "Forest Predator",
        "description": "Survivors report being stalked by an unusually fast and agile zombie in the forest.",
        "objective": "Defeat the Hunter boss",
        "location": "forest",
        "boss_type": "hunter",
        "min_level": 7,
        "reward": {"xp": 400, "item": "rifle_ammo", "count": 20},
        "completion_text": "The Hunter has been hunted! Its speed made it a formidable foe, but you were faster. This ammunition will help keep your distance in future fights."
    },
    "gas_station_horror": {
        "name": "Gas Station Horror",
        "description": "Strange activity reported at the gas station. Dead zombies seem to be rising again.",
        "objective": "Defeat the Necromancer boss",
        "location": "gas_station",
        "boss_type": "necromancer",
        "min_level": 8,
        "reward": {"xp": 450, "item": "medkit", "count": 2},
        "completion_text": "The Necromancer is no more! Its ability to heal was troublesome, but you persevered. These medkits might come in handy soon."
    },
    "town_terror": {
        "name": "Town Terror",
        "description": "A colossal zombie is rampaging through the town. It must be stopped before it destroys everything.",
        "objective": "Defeat the Behemoth boss",
        "location": "town",
        "boss_type": "behemoth",
        "min_level": 10,
        "reward": {"xp": 600, "item": "shotgun_ammo", "count": 20},
        "completion_text": "The Behemoth has fallen! Its immense strength and rage were terrifying, but you've saved what remains of the town. Take this ammunition for your next challenge."
    }
}

class GameState:
    """Main class to handle game state and save/load functionality."""

    def __init__(self):
        # Ensure saves directory exists
        if not os.path.exists(SAVES_FOLDER):
            os.makedirs(SAVES_FOLDER)

        # Initialize death log for hardcore mode tracking
        self.death_log = {
            "total_deaths": 0,
            "deaths": []
        }
        self.death_log.update(self.load_death_log() or {})

        # Initialize crafting skill
        self.crafting_skill = 0

        # Initialize combat state
        self.in_combat = False
        self.current_zombie = None

        self.player = {
            "name": "",
            "health": MAX_HEALTH,
            "max_health": MAX_HEALTH,
            "stamina": MAX_STAMINA,
            "max_stamina": MAX_STAMINA,
            "hunger": MAX_HUNGER,
            "max_hunger": MAX_HUNGER,
            "thirst": MAX_THIRST,
            "max_thirst": MAX_THIRST,
            "sleep": 100,
            "max_sleep": 100,
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 100,
            "location": "camp",
            "inventory": [],
            "equipped_weapon": None,
            "days_survived": 1,
            "hours_passed": 0,
            "zombies_killed": 0,
            "active_missions": ["tutorial"],
            "completed_missions": [],
            # New stats tracking
            "bosses_defeated": [],
            "locations_visited": ["camp"],
            "items_crafted": 0,
            "distance_traveled": 0,
            "resources_gathered": 0,
            "damage_dealt": 0,
            "damage_taken": 0,
            "death_counter": 0,  # Track how many times this player has died (hardcore mode)
            "current_weather": "clear",  # Default weather
            "weather_duration": 8,  # Hours until weather changes

            # Hardcore mode status effects
            "bleeding": False,
            "infected": False,
            "insanity": 0,  # 0-100 scale, affects perception and decision-making
            "broken_limb": False,
            "exhaustion": 0,  # 0-100 scale, affects stamina regeneration
            "hardcore_mode": HARDCORE_MODE
        }
        self.game_running = True
        self.in_combat = False
        self.current_zombie = None
        self.commands = {
            "/help": {"func": self.cmd_help, "help": "Show available commands"},
            "/status": {"func": self.cmd_status, "help": "Show your current status"},
            "/inventory": {"func": self.cmd_inventory, "help": "Show your inventory"},
            "/equip": {"func": self.cmd_equip, "help": "Equip a weapon. Usage: /equip [item_id]"},
            "/use": {"func": self.cmd_use, "help": "Use an item. Usage: /use [item_id]"},
            "/look": {"func": self.cmd_look, "help": "Look around your current location"},
            "/go": {"func": self.cmd_go, "help": "Travel to a location. Usage: /go [location]"},
            "/explore": {"func": self.cmd_explore, "help": "Explore the area for resources"},
            "/rest": {"func": self.cmd_rest, "help": "Rest to recover stamina. Usage: /rest [hours]"},
            "/attack": {"func": self.cmd_attack, "help": "Attack a zombie (in combat)"},
            "/flee": {"func": self.cmd_flee, "help": "Try to escape from combat"},
            "/craft": {"func": self.cmd_craft, "help": "Craft items from materials. Usage: /craft"},
            "/drop": {"func": self.cmd_drop, "help": "Drop an item from inventory. Usage: /drop [item_id]"},
            "/scavenge": {"func": self.cmd_scavenge_area, "help": "Scavenge your current location for resources. Usage: /scavenge"},
            "/sleep": {"func": self.cmd_sleep, "help": "Sleep to recover energy until dawn (default) or for specific hours. Usage: /sleep [hours|dawn]"},
            "/eat": {"func": self.cmd_eat, "help": "Eat food to reduce hunger. Usage: /eat [item_id]"},
            "/missions": {"func": self.cmd_missions, "help": "Show active and available missions"},
            "/map": {"func": self.cmd_map, "help": "Display a map of available locations"},
            "/stats": {"func": self.cmd_stats, "help": "Show detailed player statistics"},
            "/time": {"func": self.cmd_time, "help": "Display current game time and date"},
            "/boss": {"func": self.cmd_boss, "help": "Information about boss zombies you've encountered"},
            "/weather": {"func": self.cmd_weather, "help": "Check the current weather conditions"},
            "/deathlog": {"func": self.cmd_deathlog, "help": "View the death log (hardcore mode)"},
            "/upgrade_camp": {"func": self.cmd_upgrade_camp, "help": "View or upgrade camp facilities"},
            "/repair_barricades": {"func": self.cmd_repair_barricades, "help": "Repair damaged camp barricades"},
            "/dismantle": {"func": self.cmd_dismantle, "help": "Break down an item into its components. Usage: /dismantle [item_id]"},
            "/save": {"func": self.cmd_save, "help": "Save your game progress to a slot (1-5). Usage: /save [slot]"},
            "/load": {"func": self.cmd_load, "help": "Load a saved game from a slot (1-5). Usage: /load [slot]"},
            "/saves_list": {"func": self.cmd_saves_list, "help": "Show all available save slots"},
            "/quit": {"func": self.cmd_quit, "help": "Quit the game"}
        }

    def cmd_deathlog(self, *args):
        """View the death log (hardcore mode)."""
        # Initialize death log if needed
        if self.death_log is None:
            self.death_log = self.load_death_log()

        # Display death log
        print(Colors.colorize("\n=== HARDCORE MODE DEATH LOG ===", Colors.BOLD + Colors.RED))

        # No deaths recorded yet
        if self.death_log["total_deaths"] == 0:
            print(Colors.colorize("\nNo deaths have been recorded yet.", Colors.YELLOW))
            print(Colors.colorize("The log awaits its first entries...", Colors.CYAN))
            return

        # Display death statistics
        print(Colors.colorize(f"\nTotal Deaths Recorded: {self.death_log['total_deaths']}", Colors.BOLD + Colors.RED))

        # Sort deaths by days survived (descending)
        sorted_deaths = sorted(self.death_log["deaths"], key=lambda x: x.get("days_survived", 0), reverse=True)

        # Show top survivors
        print(Colors.colorize("\n== NOTABLE SURVIVORS ==", Colors.BOLD + Colors.YELLOW))
        for i, death in enumerate(sorted_deaths[:5]):  # Show top 5
            print(f"{i+1}. {Colors.colorize(death['name'], Colors.GREEN)} - "
                  f"Survived {Colors.colorize(str(death['days_survived']), Colors.YELLOW)} days, "
                  f"Killed {Colors.colorize(str(death['zombies_killed']), Colors.RED)} zombies")

        # Show recent deaths
        print(Colors.colorize("\n== RECENT DEATHS ==", Colors.BOLD + Colors.RED))
        for i, death in enumerate(reversed(sorted_deaths[-5:])):  # Show latest 5
            print(f"{i+1}. {Colors.colorize(death['name'], Colors.YELLOW)} - "
                  f"{Colors.colorize(death['cause'], Colors.RED)} at "
                  f"{Colors.colorize(death['location'], Colors.CYAN)}")

        # Some flavor text
        print(Colors.colorize("\nEvery death is a story in the apocalypse. What will yours be?", Colors.MAGENTA))

    def start_game(self):
        """Initialize and start the game."""
        # Clear screen and load death log at game start
        self.clear_screen()
        self.death_log = self.load_death_log()

        self.clear_screen()

        # Display zombie animation as intro
        Animations.zombie_animation()

        # Print game title with colors
        title = Colors.colorize("\n" + "="*70, Colors.RED)
        title += "\n" + Colors.colorize("ZOMBIE SURVIVAL RPG".center(70), Colors.BOLD + Colors.RED)
        title += "\n" + Colors.colorize("="*70, Colors.RED)
        print(title + "\n")

        # Type out introduction for effect
        intro_text = "Welcome to the post-apocalyptic world overrun by zombies. "
        intro_text += "Your goal is to survive as long as possible, complete missions, "
        intro_text += "and perhaps find a way to escape this nightmare."
        Animations.type_text(Colors.colorize(intro_text, Colors.YELLOW))

        print(Colors.colorize("\nType commands prefixed with / to play (e.g., /help, /status).\n", Colors.CYAN))

        # Always show save slots at startup
        save_slots = self.get_save_slots()

        # Display stylish save slots header
        divider = "=" * 50
        print(Colors.colorize(f"\n{divider}", Colors.RED))
        print(Colors.colorize("LOAD GAME".center(50), Colors.BOLD + Colors.YELLOW))
        print(Colors.colorize(f"{divider}", Colors.RED))

        print(Colors.colorize(f"\n{divider}", Colors.CYAN))
        print(Colors.colorize("SAVE SLOTS".center(50), Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"{divider}", Colors.CYAN))

        # Display save slots in a more stylish format
        if save_slots:
            print()  # Add space before slots
            for save in save_slots:
                slot_header = f"Slot {save['slot']}:"
                print(Colors.colorize(slot_header, Colors.BOLD + Colors.GREEN))

                # Display character info with colors
                character_info = f"Survivor: {Colors.colorize(save['name'], Colors.YELLOW)}, "
                character_info += f"Level {Colors.colorize(str(save['level']), Colors.YELLOW)} "
                character_info += f"({Colors.colorize(str(save['days_survived']), Colors.RED)} days survived)"
                print(character_info)

                # Display location with cyan color
                location_info = f"Location: {Colors.colorize(LOCATIONS[save['location']]['name'], Colors.CYAN)}"
                print(location_info)

                # Display save date with purple color
                date_str = datetime.fromtimestamp(save['saved_date']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Saved: {Colors.colorize(date_str, Colors.MAGENTA)}")
                print()  # Add space after each slot
        else:
            print(Colors.colorize("\nNo saved games found.", Colors.YELLOW))
            print(Colors.colorize("Start a new game and use /save [slot] to create your first save.", Colors.CYAN))

        # Calculate empty slots
        used_slots = [save['slot'] for save in save_slots]
        empty_slots = [i for i in range(1, MAX_SAVE_SLOTS + 1) if i not in used_slots]

        # Show empty slots in a more attractive format
        if empty_slots:
            print(Colors.colorize("\nEmpty slots:", Colors.BOLD))
            empty_slots_str = ", ".join([str(slot) for slot in empty_slots])
            print(Colors.colorize(f"[{empty_slots_str}]", Colors.BLUE))

        # Always ask to load a save file at the start
        print(Colors.colorize(f"\n{divider}", Colors.RED))
        # This is the key prompt that needs to appear for every player at startup
        load_option = input(Colors.colorize("Load a saving file? (y/n): ", Colors.BOLD + Colors.GREEN))

        if load_option.lower() == 'y' and save_slots:
            # Prompt for slot
            while True:
                try:
                    slot_prompt = Colors.colorize("\nEnter save slot number to load: ", Colors.YELLOW)
                    slot = int(input(slot_prompt))
                    if slot == 0:
                        break
                    if any(save['slot'] == slot for save in save_slots):
                        # Show loading animation with custom message
                        Animations.loading_bar(length=20, message=f"Loading save from slot {slot}")
                        self.load_game(slot)
                        return  # Return after loading to avoid character creation
                    else:
                        print(Colors.colorize(f"Save slot {slot} does not exist. Please choose from the available slots.", Colors.RED))
                except ValueError:
                    print(Colors.colorize("Please enter a valid number.", Colors.RED))
        elif load_option.lower() == 'y' and not save_slots:
            print(Colors.colorize("\nNo save files found. Starting a new game.", Colors.YELLOW))
            time.sleep(1.5)

        # Character creation for new game
        while not self.player["name"]:
            name = input(Colors.colorize("\nEnter your survivor's name: ", Colors.GREEN))
            if name:
                self.player["name"] = name

            # Hardcore mode selection
            hardcore_warning = "\n" + Colors.colorize("=== HARDCORE MODE ===", Colors.BOLD + Colors.RED)
            hardcore_warning += "\n" + Colors.colorize("Features:", Colors.YELLOW)
            hardcore_warning += "\n- " + Colors.colorize("PERMADEATH", Colors.RED) + ": Save file deleted on death"
            hardcore_warning += "\n- " + Colors.colorize("Status Effects", Colors.RED) + ": Bleeding, Infection, Broken Limbs"
            hardcore_warning += "\n- " + Colors.colorize("Mental Health System", Colors.MAGENTA) + ": Insanity affects gameplay"
            hardcore_warning += "\n- " + Colors.colorize("Limited Resources", Colors.YELLOW) + ": Reduced health/stat caps"
            hardcore_warning += "\n- " + Colors.colorize("Faster Deterioration", Colors.YELLOW) + ": Stats decrease faster"
            hardcore_warning += "\n- " + Colors.colorize("Advanced Combat", Colors.RED) + ": Weapon effects, critical hits"
            print(hardcore_warning)

            hardcore_option = input(Colors.colorize("\nEnable Hardcore Mode? (y/n): ", Colors.BOLD + Colors.RED))

            # Set hardcore mode flag
            self.player["hardcore_mode"] = hardcore_option.lower() == 'y'

            # Apply hardcore mode settings
            if self.player["hardcore_mode"]:
                print(Colors.colorize("\nHardcore Mode Enabled!", Colors.BOLD + Colors.RED))

                # Initialize status effect trackers
                self.player["bleeding"] = False
                self.player["infected"] = False
                self.player["broken_limb"] = False
                self.player["exhaustion"] = 0
                self.player["insanity"] = 0

                # Reduced stat caps for hardcore mode
                self.player["max_health"] = int(MAX_HEALTH * 0.85)  # 15% health reduction
                self.player["max_stamina"] = int(MAX_STAMINA * 0.85)
                self.player["max_hunger"] = int(MAX_HUNGER * 0.85)
                self.player["max_thirst"] = int(MAX_THIRST * 0.85)

                # Apply limits
                self.player["health"] = self.player["max_health"]
                self.player["stamina"] = self.player["max_stamina"]
                self.player["hunger"] = self.player["max_hunger"]
                self.player["thirst"] = self.player["max_thirst"]

                Animations.loading_bar(length=15, message="Initializing hardcore survival parameters")
                print(Colors.colorize("\nYou've chosen the path of greater challenge and immersion.", Colors.YELLOW))
                print(Colors.colorize("Every decision you make will have more significant consequences.", Colors.YELLOW))
            else:
                print(Colors.colorize("\nStandard Mode Enabled", Colors.GREEN))
                print(Colors.colorize("You'll face challenges, but without the more punishing mechanics.", Colors.YELLOW))

            welcome_msg = f"\nWelcome, {Colors.colorize(self.player['name'], Colors.BOLD + Colors.GREEN)}. Your journey begins..."
            Animations.type_text(welcome_msg)
            print(Colors.colorize("Type /help to see available commands.", Colors.CYAN))

        # Add time display
        self.update_game_time()

        # Main game loop
        while self.game_running:
            try:
                prompt = Colors.colorize("\n> ", Colors.BOLD + Colors.BLUE)
                command = input(prompt).strip()
                if not command:
                    continue

                if not command.startswith("/"):
                    print(Colors.colorize("Commands must start with / (e.g., /help)", Colors.YELLOW))
                    continue

                # Parse command and arguments
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                # Handle command execution with visual feedback
                if cmd in self.commands:
                    # Flash command recognition
                    print(Colors.colorize(f"Executing: {cmd}", Colors.CYAN))
                    time.sleep(0.2)  # Brief pause for effect
                    self.commands[cmd]["func"](*args)
                else:
                    error_msg = f"Unknown command: {Colors.colorize(cmd, Colors.RED)}. "
                    error_msg += f"Type {Colors.colorize('/help', Colors.GREEN)} to see available commands."
                    print(error_msg)
            except Exception as e:
                print(Colors.colorize(f"Error executing command: {e}", Colors.RED))

    def advance_time(self, command_type, hours=None):
        """
        Advance game time based on the type of command executed.
        Returns the number of hours that passed.

        Command types:
        - "look" - Quick observation (0.5-1 hour)
        - "light_action" - Simple actions like equip, inventory, craft (0.5-1.5 hours)
        - "medium_action" - Medium actions like standard exploration, scavenging (1-3 hours)
        - "heavy_action" - Heavy actions like combat, long travel (2-5 hours)
        - "rest" - Rest or sleep (special case, handled separately with hours parameter)
        - "zero" - Commands that don't consume time (help, save, stats, etc.)

        Parameters:
        - command_type: The type of action being performed
        - hours: Optional specific number of hours to pass (used for rest/sleep)
        """
        if command_type == "zero":
            return 0

        if command_type == "rest" and hours is not None:
            # Use the specific hours provided for rest/sleep
            hours_passed = hours

        # Random time advancement based on command type
        if command_type == "look":
            hours_passed = round(random.uniform(0.5, 1.0), 1)
        elif command_type == "light_action":
            hours_passed = round(random.uniform(0.5, 1.5), 1)
        elif command_type == "medium_action":
            hours_passed = round(random.uniform(1.0, 3.0), 1)
        elif command_type == "heavy_action":
            hours_passed = round(random.uniform(2.0, 5.0), 1)
        else:
            # Default is 1 hour if unspecified
            hours_passed = 1.0

        # Weather can affect time passage (e.g., harder to travel in storms)
        current_weather = self.player.get("current_weather", "clear")
        if current_weather == "stormy" and command_type in ["medium_action", "heavy_action"]:
            # Storms slow you down
            hours_passed *= 1.5
            print(Colors.colorize("The storm slows your progress significantly.", Colors.BLUE))
        elif current_weather == "rainy" and command_type in ["medium_action", "heavy_action"]:
            # Rain slightly slows you down
            hours_passed *= 1.2
            print(Colors.colorize("The rain makes your task take longer than usual.", Colors.BLUE))

        # Update the time counter and display time passage message
        hours_passed = round(hours_passed, 1)  # Round to one decimal place

        # Only show time passage for non-zero advancement
        if hours_passed > 0:
            # Different messages based on amount of time passed
            if hours_passed < 1:
                minutes = int(hours_passed * 60)
                print(Colors.colorize(f"\nTime passes... ({minutes} minutes)", Colors.CYAN))
            else:
                hour_text = "hour" if hours_passed == 1 else "hours"
                print(Colors.colorize(f"\nTime passes... ({hours_passed} {hour_text})", Colors.CYAN))

            # Update game time
            self.player["hours_passed"] += hours_passed

            # Check if a day has passed
            if self.player["hours_passed"] >= 24:
                days = int(self.player["hours_passed"] // 24)
                self.player["days_survived"] += days
                self.player["hours_passed"] %= 24

                # Alert player about day change
                if days == 1:
                    print(Colors.colorize(f"A new day dawns... Day {self.player['days_survived']}", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"{days} days pass... Now on Day {self.player['days_survived']}", Colors.YELLOW))

            # Update weather after significant time passage
            if hours_passed >= 1:
                self.update_weather()

            # Display current time
            current_hour = int(self.player["hours_passed"])
            is_night = current_hour in NIGHT_HOURS
            is_dawn_dusk = current_hour in DAWN_DUSK_HOURS

            time_period = "night" if is_night else "dawn/dusk" if is_dawn_dusk else "daytime"
            time_color = Colors.BLUE if is_night else Colors.MAGENTA if is_dawn_dusk else Colors.YELLOW

            # Warning about night dangers
            if is_night:
                print(Colors.colorize(f"It's now {current_hour}:00 - {time_period.upper()}. Zombies are more dangerous!", time_color))
            else:
                print(Colors.colorize(f"It's now {current_hour}:00 - {time_period}.", time_color))

            # Call update_survival_stats to handle hunger, thirst, etc.
            self.update_survival_stats(int(hours_passed))

        return hours_passed

    def update_weather(self):
        """Update the weather conditions based on time."""
        # Decrease weather duration counter
        self.player["weather_duration"] = max(0, self.player.get("weather_duration", 0) - 1)

        # If weather duration is 0, change the weather
        if self.player["weather_duration"] <= 0:
            old_weather = self.player.get("current_weather", "clear")

            # Weather transition probabilities (simplified)
            weather_options = ["clear", "cloudy", "rainy", "foggy", "windy", "stormy"]

            # Different weights based on current weather to make transitions more realistic
            if old_weather == "clear":
                weights = [0.4, 0.3, 0.1, 0.1, 0.08, 0.02]
            elif old_weather == "cloudy":
                weights = [0.2, 0.3, 0.25, 0.1, 0.1, 0.05]
            elif old_weather == "rainy" or old_weather == "foggy":
                weights = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
            elif old_weather == "stormy":
                weights = [0.1, 0.2, 0.3, 0.2, 0.2, 0.0]  # Storm usually transitions to rain
            else:
                weights = [0.2, 0.2, 0.2, 0.2, 0.15, 0.05]

            # Add seasonal weathers with low chance
            day_number = self.player["days_survived"]
            # Heat waves in "summer" (every 30 days or so)
            if day_number % 30 < 10 and random.random() < 0.1:  
                weather_options.append("hot")
                weights.append(0.15)
                # Adjust other weights
                weights = [w * 0.85 for w in weights]  
            # Cold snaps in "winter"
            elif day_number % 30 >= 20 and random.random() < 0.1:  
                weather_options.append("cold")
                weights.append(0.15)
                # Adjust other weights
                weights = [w * 0.85 for w in weights]

            # Select new weather
            new_weather = random.choices(weather_options, weights=weights, k=1)[0]

            # Set new weather
            self.player["current_weather"] = new_weather

            # Set duration based on weather type
            if new_weather in ["stormy", "hot", "cold"]:
                duration = random.randint(3, 6)  # Extreme weather doesn't last as long
            elif new_weather in ["rainy", "foggy"]:
                duration = random.randint(5, 10)
            else:
                duration = random.randint(8, 16)

            self.player["weather_duration"] = duration

            # Notify player of weather change
            if old_weather != new_weather:
                weather_info = WEATHER_TYPES[new_weather]
                symbol = weather_info.get("symbol", "")
                color = weather_info.get("color", Colors.CYAN)

                print(Colors.colorize(f"\nThe weather has changed to {symbol} {weather_info['name']}!", color))
                print(Colors.colorize(weather_info["description"], Colors.CYAN))

                # Warnings for severe weather
                if new_weather == "stormy":
                    print(Colors.colorize("Warning: The thunderstorm will make travel dangerous!", Colors.RED))
                elif new_weather == "hot":
                    print(Colors.colorize("Warning: The heat wave will increase your thirst!", Colors.RED))
                elif new_weather == "cold":
                    print(Colors.colorize("Warning: The cold snap will increase your hunger!", Colors.RED))

    def update_game_time(self):
        """Update and display the in-game date and time."""
        days = self.player["days_survived"]
        hours = int(self.player["hours_passed"] % 24)  # Convert to integer to ensure formatting works

        # Calculate date based on days survived (starting from today)
        from datetime import timedelta
        start_date = datetime.now()
        current_date = start_date + timedelta(days=days)
        date_str = current_date.strftime("%B %d, %Y")

        time_str = f"{hours:02d}:00"

        # Display formatted time
        time_display = f"\n{Colors.BOLD}{Colors.BLUE}Day {days}{Colors.ENDC} | "
        time_display += f"{Colors.YELLOW}{date_str}{Colors.ENDC} | "
        time_display += f"{Colors.CYAN}Time: {time_str}{Colors.ENDC}"

        # Add weather information to time display
        current_weather = self.player.get("current_weather", "clear")
        if current_weather in WEATHER_TYPES:
            weather_info = WEATHER_TYPES[current_weather]
            symbol = weather_info.get("symbol", "")
            weather_name = weather_info["name"]
            weather_color = weather_info["color"] 
            time_display += f" | {Colors.colorize(f'{symbol} {weather_name}', weather_color)}"

        print(time_display)

        # Check if weather should change
        self.update_weather()

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_save_slots(self):
        """Get a list of available save slots."""
        save_slots = []
        for i in range(1, MAX_SAVE_SLOTS + 1):
            slot_file = os.path.join(SAVES_FOLDER, f"save_slot_{i}.json")
            if os.path.exists(slot_file):
                try:
                    with open(slot_file, 'r') as f:
                        save_data = json.load(f)
                        save_slots.append({
                            'slot': i,
                            'name': save_data.get('name', 'Unknown'),
                            'level': save_data.get('level', 1),
                            'days_survived': save_data.get('days_survived', 0),
                            'location': save_data.get('location', 'Unknown'),
                            'saved_date': os.path.getmtime(slot_file)
                        })
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    # If there's an error reading the save file, just skip it
                    pass
        return save_slots

    def save_game(self, slot=None):
        """Save game state to file.

        Args:
            slot: Optional save slot number (1-5). If None, prompt for slot.
        """
        # Get existing save slots
        save_slots = self.get_save_slots()

        # Display save slots if no slot is provided
        if slot is None:
            self.clear_screen()
            print(Colors.colorize("\n=== SAVE GAME ===", Colors.BOLD + Colors.CYAN))

            # Show existing save slots
            if save_slots:
                print("\nExisting save slots:")
                for save in save_slots:
                    date_str = datetime.fromtimestamp(save['saved_date']).strftime('%Y-%m-%d %H:%M')
                    print(f"  {save['slot']}. {save['name']} (Level {save['level']}, {save['days_survived']} days, {save['location']}) - {date_str}")

            # Calculate available slots
            used_slots = [save['slot'] for save in save_slots]
            available_slots = [i for i in range(1, MAX_SAVE_SLOTS + 1) if i not in used_slots]

            # Show available empty slots
            if available_slots:
                print("\nEmpty save slots:", end=" ")
                for slot_num in available_slots:
                    print(f"{slot_num}", end=" ")
                print()

            # Prompt for slot
            while True:
                try:
                    slot = int(input("\nEnter save slot (1-5) or 0 to cancel: "))
                    if slot == 0:
                        print("Save cancelled.")
                        return False
                    if 1 <= slot <= MAX_SAVE_SLOTS:
                        break
                    else:
                        print(f"Please enter a number between 1 and {MAX_SAVE_SLOTS}.")
                except ValueError:
                    print("Please enter a valid number.")

        # Confirm overwrite if slot is occupied
        slot_file = os.path.join(SAVES_FOLDER, f"save_slot_{slot}.json")
        if os.path.exists(slot_file):
            confirmation = input(f"Save slot {slot} already exists. Overwrite? (y/n): ").lower()
            if confirmation != 'y':
                print("Save cancelled.")
                return False

        # Save the game
        try:
            # Ensure saves directory exists
            if not os.path.exists(SAVES_FOLDER):
                os.makedirs(SAVES_FOLDER)

            with open(slot_file, 'w') as f:
                json.dump(self.player, f, indent=4)
            print(f"Game saved successfully to slot {slot}.")
            return True
        except PermissionError:
            print("Error: No permission to write save file.")
            return False
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot=None):
        """Load game state from file.

        Args:
            slot: Optional save slot number (1-5). If None, prompt for slot.
        """
        # Get available save slots
        save_slots = self.get_save_slots()

        # Check if there are any save slots
        if not save_slots:
            print("No saved games found.")
            return False

        # Display save slots if no slot is provided
        if slot is None:
            self.clear_screen()
            print(Colors.colorize("\n=== LOAD GAME ===", Colors.BOLD + Colors.CYAN))

            # Show existing save slots
            print("\nAvailable save slots:")
            for save in save_slots:
                date_str = datetime.fromtimestamp(save['saved_date']).strftime('%Y-%m-%d %H:%M')
                print(f"  {save['slot']}. {save['name']} (Level {save['level']}, {save['days_survived']} days, {save['location']}) - {date_str}")

            # Prompt for slot
            while True:
                try:
                    slot = int(input("\nEnter save slot to load (1-5) or 0 to cancel: "))
                    if slot == 0:
                        print("Load cancelled.")
                        return False
                    if any(save['slot'] == slot for save in save_slots):
                        break
                    else:
                        print(f"Save slot {slot} does not exist. Please choose from the available slots.")
                except ValueError:
                    print("Please enter a valid number.")

        # Load the game
        slot_file = os.path.join(SAVES_FOLDER, f"save_slot_{slot}.json")
        try:
            if os.path.exists(slot_file):
                try:
                    with open(slot_file, 'r') as f:
                        loaded_data = json.load(f)
                        # Validate loaded data has required fields
                        required_fields = ["name", "health", "max_health", "stamina", "location"]
                        if all(field in loaded_data for field in required_fields):
                            self.player = loaded_data
                            print(f"Game loaded successfully from slot {slot}.")
                            return True
                        else:
                            print("Error: Save file appears to be corrupted.")
                            return False
                except json.JSONDecodeError:
                    print("Error: Save file is corrupted.")
                    return False
            print(f"Save slot {slot} does not exist.")
            return False
        except PermissionError:
            print("Error: No permission to read save file.")
            return False
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def load_death_log(self):
        """Load the hardcore mode death log from file."""
        death_log = {
            "total_deaths": 0,
            "deaths": []
        }
        try:
            if os.path.exists(DEATH_LOG_FILE):
                with open(DEATH_LOG_FILE, 'r') as f:
                    death_log = json.load(f)
            return death_log
        except Exception as e:
            print(Colors.colorize(f"Error loading death log: {e}", Colors.RED))
            return death_log

    def save_death_log(self):
        """Save the hardcore mode death log to file."""
        try:
            with open(DEATH_LOG_FILE, 'w') as f:
                json.dump(self.death_log, f)
            return True
        except Exception as e:
            print(Colors.colorize(f"Error saving death log: {e}", Colors.RED))
            return False

    def record_death(self, cause):
        """Record a death in hardcore mode."""
        if not self.player.get("hardcore_mode", False):
            return

        # Update player death counter
        self.player["death_counter"] += 1

        # Prepare death record
        death_record = {
            "name": self.player["name"],
            "cause": cause,
            "days_survived": self.player["days_survived"],
            "level": self.player["level"],
            "zombies_killed": self.player["zombies_killed"],
            "bosses_defeated": len(self.player.get("bosses_defeated", [])),
            "location": LOCATIONS[self.player["location"]]["name"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Initialize death_log if None
        if self.death_log is None:
            self.death_log = {"total_deaths": 0, "deaths": []}

        # Add death to log
        self.death_log["total_deaths"] += 1
        self.death_log["deaths"].append(death_record)

        # Save death log
        self.save_death_log()

        # Display the death record
        print(Colors.colorize("\n=== DEATH RECORDED IN THE HARDCORE LOG ===", Colors.BOLD + Colors.RED))
        print(Colors.colorize(f"Name: {death_record['name']}", Colors.YELLOW))
        print(Colors.colorize(f"Cause of Death: {death_record['cause']}", Colors.RED))
        print(Colors.colorize(f"Days Survived: {death_record['days_survived']}", Colors.YELLOW))
        print(Colors.colorize(f"Level Reached: {death_record['level']}", Colors.YELLOW))
        print(Colors.colorize(f"Zombies Killed: {death_record['zombies_killed']}", Colors.YELLOW))
        print(Colors.colorize(f"Final Resting Place: {death_record['location']}", Colors.MAGENTA))
        print(Colors.colorize("\nYour story will be remembered in the annals of the apocalypse.", Colors.BOLD + Colors.CYAN))

    # Helper functions
    def level_up(self):
        """Check and perform level up if enough XP."""
        if self.player["xp"] >= self.player["xp_to_next_level"]:
            self.player["level"] += 1
            self.player["xp"] -= self.player["xp_to_next_level"]
            self.player["xp_to_next_level"] = int(self.player["xp_to_next_level"] * 1.5)
            self.player["max_health"] += 10
            self.player["max_stamina"] += 5
            self.player["max_hunger"] += 5
            self.player["max_thirst"] += 5
            self.player["health"] = self.player["max_health"]
            self.player["stamina"] = self.player["max_stamina"]
            self.player["hunger"] = self.player["max_hunger"]
            self.player["thirst"] = self.player["max_thirst"]

            print("\n*** LEVEL UP! ***")
            print(f"You are now level {self.player['level']}!")
            print(f"Max Health increased to {self.player['max_health']}")
            print(f"Max Stamina increased to {self.player['max_stamina']}")
            print(f"Max Hunger increased to {self.player['max_hunger']}")
            print(f"Max Thirst increased to {self.player['max_thirst']}")
            print("You've been fully restored.")
            return True
        return False

    def add_to_inventory(self, item_id, count=1):
        """Add an item to player's inventory."""
        if len(self.player["inventory"]) >= MAX_INVENTORY_SLOTS:
            print("Your inventory is full! Drop something first.")
            return False

        # If item is stackable, check if we already have it
        base_item = ITEMS.get(item_id, {})
        if base_item.get("type") in ["ammo", "material", "food"] and count > 0:
            for inv_item in self.player["inventory"]:
              if inv_item["id"] == item_id and len(self.player["inventory"]) < MAX_INVENTORY_SLOTS:
                inv_item["count"] += count
                return True

        # Create a copy of the item to add to inventory
        if item_id in ITEMS:
            item = ITEMS[item_id].copy()
            item["id"] = item_id
            if "count" in item:
                item["count"] = count
            self.player["inventory"].append(item)
            return True
        return False

    def remove_from_inventory(self, item_idx, count=1):
        """Remove an item from player's inventory."""
        if 0 <= item_idx < len(self.player["inventory"]):
            item = self.player["inventory"][item_idx]

            # If item is stackable and we're not removing all
            if "count" in item and item["count"] > count:
                item["count"] -= count
                return True
            else:
                # If equipped weapon is being removed, unequip it
                if self.player["equipped_weapon"] == item_idx:
                    self.player["equipped_weapon"] = None

                self.player["inventory"].pop(item_idx)
                return True
        return False

    def spawn_zombie(self, specific_boss=None, specific_type=None):
        """Create a random zombie based on location danger level or spawn a specific boss/type."""
        location = LOCATIONS[self.player["location"]]
        danger = location["danger_level"]

        # Check if we need to spawn a specific zombie type (for scavenging)
        if specific_type and specific_type in ZOMBIE_TYPES:
            zombie = ZOMBIE_TYPES[specific_type].copy()
            zombie["type"] = specific_type
            zombie["max_health"] = zombie["health"]

            # Adjust stats based on player level
            level_factor = 1 + (self.player["level"] - 1) * 0.1
            zombie["health"] = int(zombie["health"] * level_factor)
            zombie["max_health"] = zombie["health"]
            zombie["damage"] = int(zombie["damage"] * level_factor)

            return zombie

        # Check if we need to spawn a specific boss for a mission
        elif specific_boss:
            if specific_boss in ZOMBIE_TYPES:
                zombie = ZOMBIE_TYPES[specific_boss].copy()
                zombie["type"] = specific_boss
                zombie["max_health"] = zombie["health"]

                # Enhanced boss stats based on player level
                level_factor = 1 + (self.player["level"] - 1) * 0.15
                zombie["health"] = int(zombie["health"] * level_factor)
                zombie["max_health"] = zombie["health"]
                zombie["damage"] = int(zombie["damage"] * level_factor)

                print(f"\n*** BOSS ENCOUNTER: {zombie['name']} ***")
                print(zombie["description"])
                print("This is no ordinary zombie. Prepare for a tough fight!")
                return zombie

        # Regular zombie spawning logic
        # Higher danger levels have more dangerous zombies
        zombie_types = [z_type for z_type in ZOMBIE_TYPES.keys() 
                       if not ZOMBIE_TYPES[z_type].get("is_boss", False)]  # Filter out boss zombies
        weights = []

        # Location-specific zombie spawning
        location_id = self.player["location"]

        # Check if it's night time for difficulty adjustment
        current_hour = self.player["hours_passed"] % 24
        is_night = current_hour in NIGHT_HOURS
        is_dawn_dusk = current_hour in DAWN_DUSK_HOURS

        # Night time danger modifier
        night_modifier = 1.0
        if is_night:
            night_modifier = 1.75  # Much more dangerous at night
        elif is_dawn_dusk:
            night_modifier = 1.25  # More dangerous at dawn/dusk

        for z_type in zombie_types:
            # Basic weights by zombie type
            base_weight = 0

            if z_type == "walker":
                base_weight = max(5 - danger, 1)  # Walkers are common in safe areas
                if is_night:
                    base_weight += 1  # More walkers at night
            elif z_type == "runner":
                base_weight = min(danger + 1, 5)  # Runners more common in dangerous areas
                if is_night:
                    base_weight += 2  # Runners very active at night
            elif z_type == "brute":
                base_weight = min(danger - 1, 4) if danger > 2 else 0  # Brutes only in dangerous areas
            elif z_type == "spitter":
                base_weight = min(danger - 2, 3) if danger > 3 else 0  # Spitters only in very dangerous areas
                if is_night:
                    base_weight += 1  # More active at night
            elif z_type == "stalker":
                # Forest stalkers appear mostly in the forest
                if location_id == "forest":
                    base_weight = 7  # Very common in the forest
                    if is_night:
                        base_weight += 3  # Forest stalkers hunt at night
                elif danger >= 3:
                    base_weight = 2  # Rare but possible in other dangerous areas
                    if is_night and location_id in ["town", "camp"]:
                        base_weight += 1  # Can stalk into populated areas at night
                else:
                    base_weight = 0  # Not present in safe areas

            # Apply the night modifier to the final weight
            weights.append(int(base_weight * night_modifier))

        # Ensure we have at least one valid zombie type
        if sum(weights) == 0:
            weights[0] = 1  # Default to walker

        z_type = random.choices(zombie_types, weights=weights, k=1)[0]
        zombie = ZOMBIE_TYPES[z_type].copy()

        # Scale zombie health based on player level
        level_factor = 1 + (self.player["level"] - 1) * 0.2
        zombie["health"] = int(zombie["health"] * level_factor)
        zombie["max_health"] = zombie["health"]
        zombie["type"] = z_type

        # Add special behaviors for different zombie types
        if z_type == "stalker":
            # Forest stalkers have a chance to ambush, increasing their first hit damage
            zombie["ambush"] = random.random() < 0.7  # 70% chance to ambush

        return zombie

    def check_mission_progress(self, event_type, data=None):
        """Check if any active missions have progressed."""
        for mission_id in self.player["active_missions"]:
            if mission_id in MISSIONS:
                mission = MISSIONS[mission_id]

                # Check if mission is completed
                if event_type == "location" and data == mission["location"]:
                    if mission["objective"].startswith("Find"):
                        # For "find" objectives, we check through exploration
                        pass
                elif event_type == "collect" and "Collect" in mission["objective"]:
                    # Check collection objectives
                    required_type = None
                    if "food items" in mission["objective"]:
                        required_type = "food"
                    elif "medical items" in mission["objective"]:
                        required_type = "medical"
                    elif "material items" in mission["objective"]:
                        required_type = "material"
                    elif "weapon" in mission["objective"]:
                        required_type = "weapon"
                    elif "fuel containers" in mission["objective"]:
                        required_type = "fuel"

                    if required_type and data and data.get("type") == required_type:
                        # Count how many items of required type we have
                        count = 0
                        for item in self.player["inventory"]:
                            if item.get("type") == required_type:
                                count += item.get("count", 1)

                        # Parse required number from objective
                        required_count = int(mission["objective"].split()[1])
                        if count >= required_count:
                            self.complete_mission(mission_id)
                elif event_type == "explore" and "Find" in mission["objective"]:
                    # For "find" type missions in the right location
                    if data == mission["location"]:
                        # 25% chance to find the objective
                        if random.random() < 0.25:
                            self.complete_mission(mission_id)
                elif event_type == "kill" and "Kill" in mission["objective"]:
                    # Check kill specific zombie type objectives
                    zombie_type = data.get("type", "") if data else ""
                    if "Forest Stalker" in mission["objective"] and zombie_type == "stalker":
                        self.complete_mission(mission_id)

    def complete_mission(self, mission_id):
        """Complete a mission and give rewards."""
        if mission_id in MISSIONS and mission_id in self.player["active_missions"]:
            mission = MISSIONS[mission_id]

            print(f"\n*** MISSION COMPLETED: {mission['name']} ***")
            print(mission["completion_text"])

            # Give rewards
            reward = mission["reward"]
            self.player["xp"] += reward["xp"]
            print(f"Gained {reward['xp']} XP!")

            if "item" in reward:
                if self.add_to_inventory(reward["item"], reward.get("count", 1)):
                    item_name = ITEMS[reward["item"]]["name"]
                    count = reward.get("count", 1)
                    print(f"Received {count}x {item_name}")
                else:
                    print("Inventory full! Couldn't receive item reward.")

            # Update mission lists
            self.player["active_missions"].remove(mission_id)
            self.player["completed_missions"].append(mission_id)

            # Check for level up
            self.level_up()

            # Add new missions as appropriate
            self.check_new_missions()

    def check_new_missions(self):
        """Add new missions based on player progress."""
        level = self.player["level"]
        active_and_completed = self.player["active_missions"] + self.player["completed_missions"]

        # Regular missions
        if level >= 2 and "food_run" not in active_and_completed:
            self.player["active_missions"].append("food_run")
            print("\n*** NEW MISSION AVAILABLE: Food Run ***")
            print(MISSIONS["food_run"]["description"])

        if level >= 3 and "secure_perimeter" not in active_and_completed:
            self.player["active_missions"].append("secure_perimeter")
            print("\n*** NEW MISSION AVAILABLE: Secure the Perimeter ***")
            print(MISSIONS["secure_perimeter"]["description"])

        if level >= 4 and "medical_emergency" not in active_and_completed:
            self.player["active_missions"].append("medical_emergency")
            print("\n*** NEW MISSION AVAILABLE: Medical Emergency ***")
            print(MISSIONS["medical_emergency"]["description"])

        if level >= 5 and "weapon_cache" not in active_and_completed:
            self.player["active_missions"].append("weapon_cache")
            print("\n*** NEW MISSION AVAILABLE: Weapon Cache ***")
            print(MISSIONS["weapon_cache"]["description"])

        if level >= 3 and "forest_hunt" not in active_and_completed:
            self.player["active_missions"].append("forest_hunt")
            print("\n*** NEW MISSION AVAILABLE: Forest Hunt ***")
            print(MISSIONS["forest_hunt"]["description"])

        if level >= 4 and "fuel_gathering" not in active_and_completed:
            self.player["active_missions"].append("fuel_gathering")
            print("\n*** NEW MISSION AVAILABLE: Fuel Run ***")
            print(MISSIONS["fuel_gathering"]["description"])

        # Boss missions - these unlock at higher levels
        if level >= 5 and "hospital_nightmare" not in active_and_completed:
            self.player["active_missions"].append("hospital_nightmare")
            print("\n*** NEW MISSION AVAILABLE: Hospital Nightmare ***")
            print(MISSIONS["hospital_nightmare"]["description"])
            print("WARNING: This mission involves a powerful boss zombie!")

        if level >= 6 and "tank_buster" not in active_and_completed:
            self.player["active_missions"].append("tank_buster")
            print("\n*** NEW MISSION AVAILABLE: Tank Buster ***")
            print(MISSIONS["tank_buster"]["description"])
            print("WARNING: This mission involves a powerful boss zombie!")

        if level >= 7 and "forest_predator" not in active_and_completed:
            self.player["active_missions"].append("forest_predator")
            print("\n*** NEW MISSION AVAILABLE: Forest Predator ***")
            print(MISSIONS["forest_predator"]["description"])
            print("WARNING: This mission involves a powerful boss zombie!")

        if level >= 8 and "gas_station_horror" not in active_and_completed:
            self.player["active_missions"].append("gas_station_horror")
            print("\n*** NEW MISSION AVAILABLE: Gas Station Horror ***")
            print(MISSIONS["gas_station_horror"]["description"])
            print("WARNING: This mission involves a powerful boss zombie!")

        if level >= 10 and "town_terror" not in active_and_completed:
            self.player["active_missions"].append("town_terror")
            print("\n*** NEW MISSION AVAILABLE: Town Terror ***")
            print(MISSIONS["town_terror"]["description"])
            print("WARNING: This mission involves a powerful boss zombie!")

    # Command functions
    def cmd_help(self, *args):
        """Show available commands."""
        print("\nAvailable Commands:")
        print("=" * 50)
        for cmd, info in sorted(self.commands.items()):
            print(f"{cmd:<15} - {info['help']}")

    def cmd_status(self, *args):
        """Show player status."""
        p = self.player

        # Hardcore mode indicator
        if p.get("hardcore_mode", False):
            hardcore_indicator = Colors.colorize(" [HARDCORE MODE] ", Colors.BOLD + Colors.RED)
            print(f"\nSurvivor Status: {hardcore_indicator}")
        else:
            print("\nSurvivor Status:")

        print(Colors.colorize("=" * 50, Colors.YELLOW))

        name_display = f"Name: {Colors.colorize(p['name'], Colors.BOLD + Colors.CYAN)}"
        level_display = f"Level: {Colors.colorize(str(p['level']), Colors.GREEN)}"
        days_display = f"Days Survived: {Colors.colorize(str(p['days_survived']), Colors.YELLOW)}"
        print(f"{name_display}   {level_display}   {days_display}")

        xp_display = f"XP: {p['xp']}/{p['xp_to_next_level']}"
        print(Colors.colorize(xp_display, Colors.CYAN))

        # Health status with color indicators
        health_percent = p['health'] / p['max_health'] * 100
        health_color = Colors.health_color(p['health'], p['max_health'])
        health_status = "Good" if health_percent > 70 else "Injured" if health_percent > 30 else "Critical"
        health_display = f"Health: {p['health']}/{p['max_health']} ({health_status})"
        print(Colors.colorize(health_display, health_color))

        # Stamina status
        stamina_percent = p['stamina'] / p['max_stamina'] * 100
        stamina_color = Colors.health_color(p['stamina'], p['max_stamina'])
        stamina_status = "Energized" if stamina_percent > 70 else "Tired" if stamina_percent > 30 else "Exhausted"
        stamina_display = f"Stamina: {p['stamina']}/{p['max_stamina']} ({stamina_status})"
        print(Colors.colorize(stamina_display, stamina_color))

        # Hunger status
        hunger_percent = p['hunger'] / p['max_hunger'] * 100
        hunger_color = Colors.health_color(p['hunger'], p['max_hunger'])
        hunger_status = "Well Fed" if hunger_percent > 70 else "Hungry" if hunger_percent > 30 else "Starving"
        hunger_display = f"Hunger: {p['hunger']}/{p['max_hunger']} ({hunger_status})"
        print(Colors.colorize(hunger_display, hunger_color))

        # Sleep status
        if "sleep" not in p:
            p["sleep"] = 100

        if "max_sleep" not in p:
            p["max_sleep"] = 100

        sleep_percent = p['sleep'] / p['max_sleep'] * 100
        sleep_color = Colors.health_color(p['sleep'], p['max_sleep'])
        sleep_status = "Well Rested" if sleep_percent > 70 else "Tired" if sleep_percent > 30 else "Exhausted"
        sleep_display = f"Sleep: {p['sleep']}/{p['max_sleep']} ({sleep_status})"
        print(Colors.colorize(sleep_display, sleep_color))

        # Thirst status
        thirst_percent = p['thirst'] / p['max_thirst'] * 100
        thirst_color = Colors.health_color(p['thirst'], p['max_thirst'])
        thirst_status = "Hydrated" if thirst_percent > 70 else "Thirsty" if thirst_percent > 30 else "Dehydrated"
        thirst_display = f"Thirst: {p['thirst']}/{p['max_thirst']} ({thirst_status})"
        print(Colors.colorize(thirst_display, thirst_color))

        # Location info
        location_name = LOCATIONS[p['location']]['name']
        danger_level = LOCATIONS[p['location']]['danger_level']
        danger_display = "⚠️" * danger_level if danger_level > 0 else "✓ Safe"
        print(f"Location: {Colors.colorize(location_name, Colors.CYAN)} (Danger: {danger_display})")
        print(f"Zombies Killed: {Colors.colorize(str(p['zombies_killed']), Colors.RED)}")

        # Hardcore mode status effects
        if p.get("hardcore_mode", False):
            print(Colors.colorize("\nStatus Effects:", Colors.BOLD + Colors.YELLOW))

            if p.get("bleeding", False):
                print(Colors.colorize("  ✗ Bleeding", Colors.RED) + 
                      ": Losing health over time. Use bandages to stop.")

            if p.get("infected", False):
                print(Colors.colorize("  ✗ Infected", Colors.RED) + 
                      ": Health deteriorating. Find antibiotics or medical supplies.")

            if p.get("broken_limb", False):
                print(Colors.colorize("  ✗ Broken Limb", Colors.YELLOW) + 
                      ": Reduced movement speed and stamina recovery.")

            if p.get("exhaustion", 0) > 50:
                print(Colors.colorize(f"  ✗ Exhaustion ({p['exhaustion']}%)", Colors.YELLOW) + 
                      ": Stamina recovery reduced.")

            if p.get("insanity", 0) > 30:
                print(Colors.colorize(f"  ✗ Mental Stress ({p['insanity']}%)", Colors.MAGENTA) + 
                      ": Perception and decisions affected.")

            if not any([p.get("bleeding", False), p.get("infected", False), 
                       p.get("broken_limb", False), p.get("exhaustion", 0) > 50,
                       p.get("insanity", 0) > 30]):
                print(Colors.colorize("  ✓ Healthy", Colors.GREEN) + 
                      ": No negative status effects.")

        # Weapon info
        print(Colors.colorize("\nEquipment:", Colors.BOLD + Colors.YELLOW))
        if p["equipped_weapon"] is not None:
            weapon = p["inventory"][p["equipped_weapon"]]
            weapon_display = f"Equipped Weapon: {weapon['name']}"
            print(Colors.colorize(weapon_display, Colors.CYAN))

            # Durability with color
            durability_percent = weapon['durability'] / 100
            durability_color = Colors.health_color(weapon['durability'], 100)
            print(f"  Durability: {durability_percent:.0f}%", durability_color)

            if "ammo" in weapon:
                ammo_color = Colors.GREEN if weapon['ammo'] > 0 else Colors.RED
                print(Colors.colorize(f"  Ammo: {weapon['ammo']}/{weapon['max_ammo']}", ammo_color))

            # Display special weapon properties for hardcore mode
            special_props = []
            if weapon.get("reach", 0) > 1:
                special_props.append(f"Reach: {weapon['reach']}")
            if weapon.get("aoe", False):
                special_props.append("Area Effect")

            if special_props:
                props_str = ", ".join(special_props)
                print(Colors.colorize(f"  Special: {props_str}", Colors.YELLOW))
        else:
            print(Colors.colorize("Equipped Weapon: None (Unarmed)", Colors.RED))

    def cmd_inventory(self, *args):
        """Show player inventory."""
        if not self.player["inventory"]:
            print("\nYour inventory is empty.")
            # No time passes when checking an empty inventory
            return

        print(f"\nInventory ({len(self.player['inventory'])}/{MAX_INVENTORY_SLOTS} slots):")
        print("=" * 50)
        for i, item in enumerate(self.player["inventory"]):
            equipped = " (Equipped)" if self.player["equipped_weapon"] == i else ""
            count = f" x{item['count']}" if "count" in item else ""
            print(f"{i+1}. {item['name']}{count}{equipped}")
            print(f"   {item['description']}")

            if item["type"] == "weapon":
                print(f"   Damage: {item['damage']}  Durability: {item['durability']}/100")
                if "ammo" in item:
                    print(f"   Ammo: {item['ammo']}/{item['max_ammo']}")
            elif item["type"] in ["food", "medical"]:
                effects = []
                if "health" in item:
                    effects.append(f"+{item['health']} Health")
                if "stamina" in item:
                    effects.append(f"+{item['stamina']} Stamina")
                if "hunger" in item:
                    effects.append(f"+{item['hunger']} Hunger")
                if "thirst" in item:
                    effects.append(f"+{item['thirst']} Thirst")
                print(f"   Effects: {', '.join(effects)}")
            elif item["type"] == "material":
                print("   Materials for crafting items.")

        # Checking inventory takes a small amount of time
        self.advance_time("light_action")

    def cmd_equip(self, *args):
        """Equip a weapon."""
        if not args:
            print("Usage: /equip [item_number]")
            return

        try:
            item_idx = int(args[0]) - 1
            if 0 <= item_idx < len(self.player["inventory"]):
                item = self.player["inventory"][item_idx]
                if item["type"] == "weapon":
                    self.player["equipped_weapon"] = item_idx
                    print(f"Equipped {item['name']}.")
                    # Equipping a weapon takes a small amount of time
                    self.advance_time("light_action")
                else:
                    print("You can only equip weapons.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid item number.")

    def cmd_use(self, *args):
        """Use an item from inventory."""
        if not args:
            print("Usage: /use [item_number]")
            return

        try:
            item_idx = int(args[0]) - 1
            if 0 <= item_idx < len(self.player["inventory"]):
                item = self.player["inventory"][item_idx]

                if item["type"] == "food" or item["type"] == "medical":
                    used_item = False
                    # Apply healing effects
                    if "health" in item:
                        old_health = self.player["health"]
                        self.player["health"] = min(self.player["health"] + item["health"], self.player["max_health"])
                        health_gained = self.player["health"] - old_health
                        if health_gained > 0:
                            print(f"Restored {health_gained} health.")
                            used_item = True

                    # Apply stamina effects
                    if "stamina" in item:
                        old_stamina = self.player["stamina"]
                        self.player["stamina"] = min(self.player["stamina"] + item["stamina"], self.player["max_stamina"])
                        stamina_gained = self.player["stamina"] - old_stamina
                        if stamina_gained > 0:
                            print(f"Restored {stamina_gained} stamina.")
                            used_item = True

                    # Apply hunger effects
                    if "hunger" in item:
                        old_hunger = self.player["hunger"]
                        self.player["hunger"] = min(self.player["hunger"] + item["hunger"], self.player["max_hunger"])
                        hunger_gained = self.player["hunger"] - old_hunger
                        if hunger_gained > 0:
                            print(f"Satisfied {hunger_gained} hunger.")
                            used_item = True

                    # Apply thirst effects
                    if "thirst" in item:
                        old_thirst = self.player["thirst"]
                        self.player["thirst"] = min(self.player["thirst"] + item["thirst"], self.player["max_thirst"])
                        thirst_gained = self.player["thirst"] - old_thirst
                        if thirst_gained > 0:
                            print(f"Quenched {thirst_gained} thirst.")
                            used_item = True

                    if used_item:
                        if "count" in item and item["count"] > 1:
                            item["count"] -= 1
                            print(f"Used 1 {item['name']}. {item['count']} remaining.")
                        else:
                            self.remove_from_inventory(item_idx)
                            print(f"Used {item['name']}.")

                        # Using an item takes a small amount of time
                        self.advance_time("light_action")
                    else:
                        print(f"You don't need to use {item['name']} right now.")

                elif item["type"] == "ammo":
                    # Find matching weapon
                    weapon_type = item["weapon"]
                    weapon_found = False

                    for i, inv_item in enumerate(self.player["inventory"]):
                        if inv_item.get("id") == weapon_type:
                            # Load ammo into the weapon
                            space_available = inv_item["max_ammo"] - inv_item["ammo"]
                            ammo_to_add = min(space_available, item["count"])

                            if ammo_to_add > 0:
                                inv_item["ammo"] += ammo_to_add
                                print(f"Loaded {ammo_to_add} rounds into {inv_item['name']}.")

                                # Reduce or remove ammo item
                                if ammo_to_add >= item["count"]:
                                    self.remove_from_inventory(item_idx)
                                else:
                                    item["count"] -= ammo_to_add
                                    print(f"{item['count']} rounds remaining in inventory.")

                                # Loading ammo takes a small amount of time
                                self.advance_time("light_action")
                                weapon_found = True
                                break
                            else:
                                print(f"The {inv_item['name']} is already fully loaded.")
                                weapon_found = True
                                break

                    if not weapon_found:
                        print(f"You don't have a {weapon_type.replace('_', ' ')} to use this ammunition with.")

                else:
                    print(f"You can't use {item['name']} directly.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid item number.")

    def cmd_look(self, *args):
        """Look around the current location."""
        location = LOCATIONS[self.player["location"]]
        print(f"\n{location['name']}")
        print("=" * 50)
        print(location["description"])
        print(f"Danger Level: {location['danger_level']} {'🧟' * location['danger_level']}")

        # Show available resources
        print("\nPotential Resources:")
        for resource in location["resource_types"]:
            print(f"- {resource.capitalize()}")

        # Show available exits
        print("\nAvailable Locations:")
        for loc_id, loc_data in LOCATIONS.items():
            if loc_id != self.player["location"]:
                print(f"- {loc_data['name']} (/go {loc_id})")

        # Looking around consumes time
        self.advance_time("look")

    def update_survival_stats(self, hours=1):
        """Update hunger, thirst, sleep and other stats as time passes."""
        # Convert hours to int if it's a float
        hours = int(hours) if isinstance(hours, float) else hours
        # Convert hours to float if it's not already (for handling decimal hours)
        hours = float(hours)
        hardcore_mode = self.player.get("hardcore_mode", False)

        # Get current weather for modifiers
        current_weather = self.player.get("current_weather", "clear")
        weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

        # Apply weather modifiers to survival stats
        hunger_modifier = weather_info.get("hunger_modifier", 1.0)
        thirst_modifier = weather_info.get("thirst_modifier", 1.0)
        stamina_modifier = weather_info.get("stamina_modifier", 1.0)

        # Ensure sleep stat exists
        if "sleep" not in self.player:
            self.player["sleep"] = 100
            self.player["max_sleep"] = 100

        if self.player["hunger"] > 20 and self.player["thirst"] > 20:
            stamina_gain = min(int(hours * 3 * TIME_FACTOR * stamina_modifier), # use stamina_modifier here
                              self.player["max_stamina"] - self.player["stamina"])
            if stamina_gain > 0:
                self.player["stamina"] += stamina_gain

        # Weather-specific descriptions
        if hunger_modifier > 1.0 or thirst_modifier > 1.0:
            if current_weather == "hot":
                print(Colors.colorize("The heat is making you dehydrate faster.", Colors.RED))
            elif current_weather == "cold":
                print(Colors.colorize("The cold makes you burn calories faster to stay warm.", Colors.BLUE))

        # Decrease hunger and thirst based on time and weather (faster in hardcore mode)
        hunger_loss = int(hours * 5 * TIME_FACTOR * hunger_modifier)
        thirst_loss = int(hours * 8 * TIME_FACTOR * thirst_modifier)

        # Decrease sleep (only when not in a sleeping command)
        sleeping = getattr(self, '_sleeping', False)
        if not sleeping:
            sleep_loss = int(hours * 3 * TIME_FACTOR)
            # Adjust sleep loss based on hardcore mode
            if hardcore_mode:
                sleep_loss = int(sleep_loss * 1.25)
        else:
            sleep_loss = 0

        # In hardcore mode, stats decrease faster
        if hardcore_mode:
            hunger_loss = int(hunger_loss * 1.25)
            thirst_loss = int(thirst_loss * 1.25)

        old_hunger = self.player["hunger"]
        old_thirst = self.player["thirst"]
        old_sleep = self.player.get("sleep", 100)

        self.player["hunger"] = max(0, self.player["hunger"] - hunger_loss)
        self.player["thirst"] = max(0, self.player["thirst"] - thirst_loss)
        self.player["sleep"] = max(0, self.player.get("sleep", 100) - sleep_loss)

        # Show warning messages if stats get low
        if old_hunger > 30 and self.player["hunger"] <= 30:
            print(Colors.colorize("\n⚠️ You are getting hungry. Find food soon.", Colors.YELLOW))
        if old_thirst > 30 and self.player["thirst"] <= 30:
            print(Colors.colorize("\n⚠️ You are getting thirsty. Find water soon.", Colors.YELLOW))
        if old_sleep > 30 and self.player["sleep"] <= 30:
            print(Colors.colorize("\n⚠️ You're starting to feel tired. Get some sleep soon.", Colors.YELLOW))

        # Critical hunger and thirst effects (more severe in hardcore mode)
        if self.player["hunger"] <= 0:
            health_loss = int(hours * 5 * TIME_FACTOR)
            if hardcore_mode:
                health_loss = int(health_loss * 1.5)
            self.player["health"] = max(1, self.player["health"] - health_loss)
            print(Colors.colorize("\n❗ You are starving! Your health is decreasing.", Colors.RED))

            # In hardcore mode, starvation increases insanity
            if hardcore_mode:
                insanity_gain = int(hours * 5 * INSANITY_FACTOR)
                self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_gain)
                if insanity_gain > 0:
                    print(Colors.colorize("  Your mental state is deteriorating from starvation...", Colors.MAGENTA))

        if self.player["thirst"] <= 0:
            health_loss = int(hours * 8 * TIME_FACTOR)
            if hardcore_mode:
                health_loss = int(health_loss * 1.5)
            self.player["health"] = max(1, self.player["health"] - health_loss)
            print(Colors.colorize("\n❗ You are dehydrated! Your health is decreasing rapidly.", Colors.RED))

            # In hardcore mode, dehydration increases insanity even faster
            if hardcore_mode:
                insanity_gain = int(hours * 8 * INSANITY_FACTOR)
                self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_gain)
                if insanity_gain > 0:
                    print(Colors.colorize("  Your mind is clouding from severe dehydration...", Colors.MAGENTA))

        # Handle hardcore mode status effects
        if hardcore_mode:
            # Bleeding damage
            if self.player.get("bleeding", False):
                bleed_damage = BLEED_DAMAGE * hours
                self.player["health"] = max(1, self.player["health"] - bleed_damage)
                print(Colors.colorize(f"\n❗ You're losing blood! (-{bleed_damage} health)", Colors.RED))

                # 10% chance to stop bleeding naturally each hour
                if random.random() < 0.1 * hours:
                    self.player["bleeding"] = False
                    print(Colors.colorize("  The bleeding has stopped naturally.", Colors.GREEN))

            # Infection damage
            if self.player.get("infected", False):
                infection_damage = int(hours * 3 * TIME_FACTOR)
                self.player["health"] = max(1, self.player["health"] - infection_damage)
                print(Colors.colorize(f"\n❗ Your infection is worsening! (-{infection_damage} health)", Colors.RED))

                # Infection increases insanity
                insanity_gain = int(hours * 3 * INSANITY_FACTOR)
                self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_gain)

                # 5% chance to recover from infection naturally each hour
                if random.random() < 0.05 * hours:
                    self.player["infected"] = False
                    print(Colors.colorize("  Your immune system has fought off the infection.", Colors.GREEN))

            # Broken limb reduces stamina recovery
            if self.player.get("broken_limb", False):
                # 2% chance to heal naturally each hour
                if random.random() < 0.02 * hours:
                    self.player["broken_limb"] = False
                    print(Colors.colorize("\n  Your broken limb has healed enough for normal movement.", Colors.GREEN))

            # Exhaustion gradually decreases when resting
            if self.player.get("exhaustion", 0) > 0:
                exhaustion_recovery = int(hours * 2)
                self.player["exhaustion"] = max(0, self.player.get("exhaustion", 0) - exhaustion_recovery)
                if self.player["exhaustion"] == 0:
                    print(Colors.colorize("\n  You're no longer exhausted.", Colors.GREEN))

            # Insanity gradually decreases when well-fed and hydrated
            if self.player.get("insanity", 0) > 0 and self.player["hunger"] > 60 and self.player["thirst"] > 60:
                insanity_recovery = int(hours * 1)
                self.player["insanity"] = max(0, self.player.get("insanity", 0) - insanity_recovery)
                if self.player["insanity"] == 0 and insanity_recovery > 0:
                    print(Colors.colorize("\n  Your mind is clearer now.", Colors.GREEN))

            # High insanity can cause hallucinations
            if self.player.get("insanity", 0) > 70 and random.random() < 0.2 * hours:
                hallucinations = [
                    "You hear whispers coming from the shadows...",
                    "Something moved in the corner of your eye, but nothing's there.",
                    "The walls seem to be breathing...",
                    "You feel like you're being watched.",
                    "Did that zombie just call your name?",
                    "The ground seems to shift beneath your feet."
                ]
                print(Colors.colorize(f"\n  {random.choice(hallucinations)}", Colors.MAGENTA))

        # Time advancement is now handled by advance_time method

        # Stamina regeneration (affected by hardcore mode, status effects, and weather)
        regen_modifier = 1.0
        # Apply weather effects to stamina regeneration
        if current_weather == "stormy":
            regen_modifier *= 0.5  # Stormy weather halves stamina recovery
            if random.random() < 0.3:
                print(Colors.colorize("The storm is making rest difficult and slowing your recovery.", Colors.BOLD + Colors.BLUE))
        elif current_weather == "hot":
            regen_modifier *= 0.7  # Hot weather reduces stamina recovery
            if random.random() < 0.3:
                print(Colors.colorize("The oppressive heat makes it hard to recover your energy.", Colors.RED))
        elif current_weather == "cold":
            regen_modifier *= 0.75  # Cold weather reduces stamina recovery
            if random.random() < 0.3:
                print(Colors.colorize("The cold is sapping your energy, making recovery slower.", Colors.BLUE))

        # Hardcore mode effects
        if hardcore_mode:
            regen_modifier *= 0.75  # Reduced recovery in hardcore mode

            if self.player.get("broken_limb", False):
                regen_modifier *= 0.5  # Broken limb halves stamina recovery

            if self.player.get("exhaustion", 0) > 50:
                regen_modifier *= 0.5  # High exhaustion halves stamina recovery

            if self.player.get("insanity", 0) > 50:
                regen_modifier *= 0.75  # High insanity reduces stamina recovery

        # Slowly regenerate stamina if not starving or dehydrated
        if self.player["hunger"] > 20 and self.player["thirst"] > 20:
            stamina_gain = min(int(hours * 3 * TIME_FACTOR * regen_modifier), 
                              self.player["max_stamina"] - self.player["stamina"])
            if stamina_gain > 0:
                self.player["stamina"] += stamina_gain
                # If weather is good, add a small bonus
                if current_weather == "clear" and random.random() < 0.2:
                    bonus = min(2, self.player["max_stamina"] - self.player["stamina"])
                    if bonus > 0:
                        self.player["stamina"] += bonus
                        print(Colors.colorize("The pleasant weather gives you a small energy boost.", Colors.GREEN))

        # Check for death
        if self.player["health"] <= 0:
            death_message = "\n💀 You have died from your injuries..."
            death_cause = "Injuries"

            if hardcore_mode:
                # Different death messages based on status effects
                if self.player.get("bleeding", False):
                    death_message = "\n💀 You have bled out and died..."
                    death_cause = "Blood loss"
                elif self.player.get("infected", False):
                    death_message = "\n💀 The infection has claimed your life..."
                    death_cause = "Infection"
                elif self.player["hunger"] <= 0:
                    death_message = "\n💀 You have starved to death..."
                    death_cause = "Starvation"
                elif self.player["thirst"] <= 0:
                    death_message = "\n💀 You have died from dehydration..."
                    death_cause = "Dehydration"

                # Record death in hardcore mode
                if self.death_log is None:
                    self.death_log = self.load_death_log()
                self.record_death(death_cause)

                # In hardcore mode with permadeath, we'll delete the save file
                if PERMADEATH and os.path.exists(SAVE_FILE):
                    try:
                        os.remove(SAVE_FILE)
                        death_message += "\nYour save file has been deleted. (PERMADEATH)"
                    except (ValueError, TypeError):
                        pass

            print(Colors.colorize(death_message, Colors.BOLD + Colors.RED))
            self.game_running = False

    def cmd_sleep(self, *args):
        """Sleep to recover energy and reduce fatigue, with location-based risk."""
        if self.in_combat:
            print(Colors.colorize("You can't sleep while in combat!", Colors.RED))
            return

        # Get current hour of day
        current_hour = self.player.get("hours_passed", 0) % 24

        # Calculate hours until dawn (6 AM)
        if current_hour < 6:
            hours_until_dawn = 6 - current_hour
        else:
            hours_until_dawn = (24 - current_hour) + 6

        # Get sleep duration - default to sleeping until dawn
        sleep_until_dawn = True
        hours = hours_until_dawn

        if args:
            try:
                specified_hours = max(1, min(24, int(args[0])))
                hours = specified_hours
                sleep_until_dawn = False
            except ValueError:
                if args[0].lower() == "dawn" or args[0].lower() == "day":
                    # Explicitly sleeping until dawn
                    hours = hours_until_dawn
                    sleep_until_dawn = True
                else:
                    print("Please specify a valid number of hours between 1 and 24 or 'dawn'.")
                    return

        # Get current location and its safety level
        current_location = self.player["location"]
        location_info = LOCATIONS[current_location]

        # Check if at camp with damaged barricades
        if current_location == "camp" and location_info.get("barricades_intact") is False:
            sleep_safety = 0.4  # 40% safe if barricades are broken
            print(Colors.colorize("Warning: The camp barricades are damaged, making sleep riskier.", Colors.YELLOW))
        else:
            sleep_safety = location_info.get("sleep_safety", 0.5)  # Default 50% if not specified

        # Get current weather and its effects
        current_weather = self.player.get("current_weather", "clear")
        weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

        # Weather affects sleep quality and zombie activity
        weather_effect = ""
        rest_quality_modifier = 1.0
        danger_modifier = 1.0

        if current_weather == "stormy":
            rest_quality_modifier = 0.7  # 30% less effective rest
            danger_modifier = 1.3  # 30% more dangerous
            weather_effect = "The thunderstorm makes it difficult to sleep soundly."
        elif current_weather == "rainy":
            rest_quality_modifier = 0.8  # 20% less effective rest
            danger_modifier = 1.2  # 20% more dangerous
            weather_effect = "The rain patters on the roof as you try to sleep."
        elif current_weather == "foggy":
            rest_quality_modifier = 0.9  # 10% less effective rest
            danger_modifier = 1.1  # 10% more dangerous
            weather_effect = "The fog makes it hard to sleep soundly."
        elif current_weather == "windy":
            rest_quality_modifier = 0.9  # 10% less effective rest
            danger_modifier = 1.1  # 10% more dangerous
            weather_effect = "The howling wind makes it harder to sleep soundly."
        elif current_weather == "clear":
            rest_quality_modifier = 1.2  # 20% more effective rest
            danger_modifier = 0.9  # 10% less dangerous
            weather_effect = "The clear night provides restful conditions."
        elif current_weather == "hot":
            rest_quality_modifier = 0.8  # 20% less effective rest
            danger_modifier = 1.1  # 10% more dangerous
            weather_effect = "The oppressive heat makes it hard to sleep."
        elif current_weather == "cold":
            rest_quality_modifier = 0.9  # 10% less effective rest
            danger_modifier = 0.9  # 10% less dangerous
            weather_effect = "The cold makes you shiver while you try to sleep."

        if weather_effect:
            print(Colors.colorize(f"\n{weather_effect}", weather_info["color"]))

        # Calculate death risk based on location safety and weather
        death_risk = (1.0 - sleep_safety) * danger_modifier

        print(f"Sleeping for {hours} hours...")
        Animations.loading_bar(length=10, delay=0.05, message="Sleeping")

        # Roll for death risk
        if random.random() < death_risk:
            death_message = "You were killed in your sleep by zombies!"
            print(Colors.colorize(f"\n☠️ {death_message}", Colors.BOLD + Colors.RED))
            if self.player.get("hardcore_mode", False):
                self.record_death(death_message)
            self.game_running = False
            return

        # Successful sleep - recover stats
        stamina_recovery = min(hours * 10 * rest_quality_modifier, self.player["max_stamina"] - self.player["stamina"])
        self.player["stamina"] += stamina_recovery

        # Hunger and thirst still deplete while sleeping, but at a slower rate
        self.player["hunger"] = max(0, self.player["hunger"] - (hours * 2))
        self.player["thirst"] = max(0, self.player["thirst"] - (hours * 3))

        # Set sleeping flag so sleep doesn't decrease during sleep
        self._sleeping = True

        # Ensure sleep stat exists
        if "sleep" not in self.player:
            self.player["sleep"] = 100
            self.player["max_sleep"] = 100

        # Calculate how long you actually sleep based on sleep bar
        actual_hours = hours

        # Higher sleep means you're less tired and more likely to wake up early
        current_sleep_percent = (self.player["sleep"] / self.player["max_sleep"]) * 100

        # Calculate probability of sleeping the full duration vs waking up early
        # At 0% sleep, you'll sleep the full time because you're exhausted
        # At 100% sleep, you have a 70% chance of waking up early
        wake_early_chance = (current_sleep_percent * 0.7) / 100

        # If sleeping until dawn and sleep meter is somewhat high, might wake up early
        if sleep_until_dawn and random.random() < wake_early_chance:
            # Wake up 1-3 hours before dawn
            early_wake = random.randint(1, min(3, hours-1))
            if early_wake < hours:
                actual_hours = hours - early_wake
                print(Colors.colorize(f"\nYou wake up naturally {early_wake} hour(s) before dawn.", Colors.CYAN))

        # Advance game time by actual sleep duration
        self.advance_time("rest", hours=actual_hours)

        # Sleep recovery based on time, conditions, and sleep quality
        sleep_recovery = min(
            hours * 8 * rest_quality_modifier,  # Base recovery
            self.player["max_sleep"] - self.player["sleep"]  # Cap at max_sleep
        )

        # Apply sleep recovery
        old_sleep = self.player["sleep"]
        self.player["sleep"] = min(self.player["max_sleep"], old_sleep + sleep_recovery)

        # Reset sleeping flag
        self._sleeping = False

        # Display results
        print(Colors.colorize(f"\nYou slept for {actual_hours} hours and recovered {stamina_recovery:.0f} stamina.", Colors.GREEN))

        # Display sleep recovery if significant
        if sleep_recovery > 0:
            sleep_gain = self.player["sleep"] - old_sleep
            print(Colors.colorize(f"Your sleep meter improved by {sleep_gain:.0f} points.", Colors.GREEN))

        # Check for health recovery if in camp or with improved shelter
        if current_location == "camp" and CAMP_UPGRADES["shelter"]["level"] > 1:
            health_recovery = min(hours * CAMP_UPGRADES["shelter"]["level"], self.player["max_health"] - self.player["health"])
            self.player["health"] += health_recovery
            print(Colors.colorize(f"Your comfortable shelter helped you heal. Recovered {health_recovery:.0f} health.", Colors.GREEN))

        # Show warning if hunger or thirst are low after sleeping
        if self.player["hunger"] < 20:
            print(Colors.colorize("You wake up feeling very hungry.", Colors.YELLOW))
        if self.player["thirst"] < 20:
            print(Colors.colorize("Your mouth is dry from thirst.", Colors.YELLOW))

        # "Insane" effect if sleep is too low
        if self.player.get("sleep", 0) < 30:
            if not self.player.get("insane", False):
                self.player["insane"] = True
                print(Colors.colorize("You haven't been sleeping enough. You're starting to hallucinate...", Colors.RED))
                print(Colors.colorize("50% chance of action failure until you get proper rest.", Colors.RED))
        elif self.player.get("sleep", 0) > 70:
            if self.player.get("insane", False):
                self.player["insane"] = False
                print(Colors.colorize("You feel clear-headed and alert again after a good rest.", Colors.GREEN))

    def cmd_rest(self, *args):
        """Rest to recover stamina at the cost of hunger and thirst."""
        if self.in_combat:
            print(Colors.colorize("You can't rest while in combat!", Colors.RED))
            return

        # Get rest duration
        hours = 8  # Default rest time
        if args:
            try:
                hours = max(1, min(24, int(args[0])))
            except ValueError:
                print("Please specify a valid number of hours between 1 and 24.")
                return

        # Get current weather and location info
        current_weather = self.player.get("current_weather", "clear")
        weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])
        danger_level = LOCATIONS[self.player["location"]]["danger_level"]

        # Weather affects rest quality and zombie encounter chance
        rest_quality_modifier = 1.0
        danger_modifier = 1.0

        # Weather-specific rest modifiers
        if current_weather == "stormy":
            rest_quality_modifier = 0.6  # Storms make rest less effective
            danger_modifier = 1.2  # But thunder can mask your presence from zombies
            print(Colors.colorize("\nThe storm makes rest difficult, with thunder and lightning disturbing your sleep.", weather_info["color"]))
        elif current_weather == "rainy":
            rest_quality_modifier = 0.8  # Rain makes rest somewhat less effective
            danger_modifier = 0.9  # Rain masks sounds, making zombie encounters less likely
            print(Colors.colorize("\nThe rain patters on the roof as you try to rest.", weather_info["color"]))
        elif current_weather == "foggy":
            rest_quality_modifier = 0.9  # Fog has minimal impact on rest
            danger_modifier = 1.3  # But makes zombie ambushes more likely
            print(Colors.colorize("\nThe thick fog creates an eerie atmosphere as you try to rest.", weather_info["color"]))
        elif current_weather == "hot":
            rest_quality_modifier = 0.7  # Heat makes rest less effective
            danger_modifier = 1.1  # Heat makes zombies more active
            print(Colors.colorize("\nThe oppressive heat makes it difficult to sleep comfortably.", weather_info["color"]))
        elif current_weather == "cold":
            rest_quality_modifier = 0.8  # Cold makes rest less effective
            danger_modifier = 0.8  # Cold makes zombies more sluggish
            print(Colors.colorize("\nYou huddle for warmth as you try to rest in the cold.", weather_info["color"]))
        elif current_weather == "clear":
            rest_quality_modifier = 1.2  # Clear weather improves rest quality
            print(Colors.colorize("\nThe peaceful clear weather provides ideal conditions for rest.", weather_info["color"]))
        elif current_weather == "windy":
            rest_quality_modifier = 0.85  # Wind makes rest somewhat less effective
            danger_modifier = 1.1  # Wind can mask zombie sounds, increasing surprise encounters
            print(Colors.colorize("\nThe howling wind makes it harder to sleep soundly.", weather_info["color"]))

        print(f"Resting for {hours} hours...")
        Animations.loading_bar(length=10, delay=0.02, message="Resting")

        # Chance of being interrupted by zombies in dangerous areas
        # Modified by weather and location danger
        encounter_chance = 0.1 * danger_level * hours / 8 * danger_modifier

        if danger_level > 0 and random.random() < encounter_chance:
            # Calculate how long player rested before interruption
            actual_hours = max(1, int(hours * random.random()))
            print(Colors.colorize(f"After {actual_hours} hours, your rest is interrupted by zombies!", Colors.BOLD + Colors.RED))

            # Still apply partial rest effects, modified by weather
            base_stamina_recovery = actual_hours * 10
            modified_recovery = int(base_stamina_recovery * rest_quality_modifier)
            stamina_recovery = min(modified_recovery, self.player["max_stamina"] - self.player["stamina"])
            self.player["stamina"] += stamina_recovery

            # Apply time effects
            self.update_survival_stats(actual_hours)

            # Start combat
            self.current_zombie = self.spawn_zombie()
            self.start_combat()
        else:
            # Full rest, modified by weather
            base_stamina_recovery = hours * 10
            modified_recovery = int(base_stamina_recovery * rest_quality_modifier)
            stamina_recovery = min(modified_recovery, self.player["max_stamina"] - self.player["stamina"])
            self.player["stamina"] += stamina_recovery

            # For rest, we'll use the actual hours directly instead of the standard categories
            # since rest is a special case where player explicitly chooses the duration

            # First update the in-game time
            self.player["hours_passed"] += hours

            # Then update day count
            new_days = self.player["hours_passed"] // 24
            if new_days > self.player["days_survived"]:
                self.player["days_survived"] = new_days
                days = self.player["days_survived"]
                print(Colors.colorize(f"You have survived for {days} days!", Colors.GREEN))

            # Update survival stats based on time passed
            self.update_survival_stats(hours)

            # Rest quality message based on weather
            if rest_quality_modifier >= 1.1:
                print(Colors.colorize(f"You feel well-rested. Recovered {stamina_recovery} stamina.", Colors.GREEN))
            elif rest_quality_modifier >= 0.9:
                print(f"You feel rested. Recovered {stamina_recovery} stamina.")
            elif rest_quality_modifier >= 0.7:
                print(Colors.colorize(f"Your rest was disturbed by the weather. Recovered {stamina_recovery} stamina.", Colors.YELLOW))
            else:
                print(Colors.colorize(f"You had a poor rest due to the harsh weather. Recovered only {stamina_recovery} stamina.", Colors.RED))

            # Weather affects healing while resting
            healing_modifier = rest_quality_modifier
            if self.player["hunger"] > 30 and self.player["thirst"] > 30:
                base_health_recovery = hours * 2
                modified_health_recovery = int(base_health_recovery * healing_modifier)
                health_recovery = min(modified_health_recovery, self.player["max_health"] - self.player["health"])

                if health_recovery > 0:
                    self.player["health"] += health_recovery
                    print(Colors.colorize(f"Your wounds have healed. Recovered {health_recovery} health.", Colors.GREEN))

                    # Chance to cure status effects in good weather
                    if current_weather == "clear" and self.player.get("hardcore_mode", False):
                        # Chance to heal bleeding
                        if self.player.get("bleeding", False) and random.random() < 0.2:
                            self.player["bleeding"] = False
                            print(Colors.colorize("The restful conditions have helped stop your bleeding.", Colors.GREEN))

                        # Reduced chance to heal infection
                        if self.player.get("infected", False) and random.random() < 0.1:
                            self.player["infected"] = False
                            print(Colors.colorize("Your body has fought off the infection while resting.", Colors.GREEN))

    def cmd_drop(self, *args):
        """Drop an item from inventory."""
        if not args:
            print("Usage: /drop [item_number]")
            return

        try:
            item_idx = int(args[0]) - 1
            if 0 <= item_idx < len(self.player["inventory"]):
                item = self.player["inventory"][item_idx]
                item_name = item["name"]

                # Get count if specified
                count = 1
                if len(args) > 1:
                    try:
                        count = min(int(args[1]), item.get("count", 1))
                    except ValueError:
                        print("Please specify a valid count.")
                        return

                if self.remove_from_inventory(item_idx, count):
                    count_str = f" x{count}" if count > 1 else ""
                    print(f"Dropped {item_name}{count_str}.")

                    # Dropping items takes a small amount of time
                    self.advance_time("light_action")
                else:
                    print("Failed to drop item.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid item number.")

    def cmd_craft(self, *args):
        """Craft items from materials."""
        # Define craftable recipes
        RECIPES = {
            "bandage": {
                "name": "Bandage",
                "materials": {"cloth": 2},
                "result": "bandage",
                "count": 1,
                "description": "Craft a bandage to heal wounds."
            },
            "molotov": {
                "name": "Molotov Cocktail",
                "materials": {"cloth": 1, "fuel": 1},
                "result": "molotov",
                "count": 1,
                "description": "A makeshift incendiary weapon effective against groups of zombies."
            },
            "spear": {
                "name": "Makeshift Spear",
                "materials": {"wood": 2, "kitchen_knife": 1},
                "result": "spear",
                "count": 1,
                "description": "A simple but effective melee weapon with good reach."
            },
            "water_filter": {
                "name": "Water Filter",
                "materials": {"cloth": 2, "metal_scrap": 1},
                "result": "clean_water_jug",
                "count": 1,
                "description": "Filter contaminated water to make it drinkable."
            },
            "reinforced_bat": {
                "name": "Reinforced Baseball Bat",
                "materials": {"baseball_bat": 1, "metal_scrap": 2},
                "result": "reinforced_bat",
                "count": 1,
                "description": "A baseball bat reinforced with metal for increased damage and durability."
            }
        }

        # If no arguments provided, show available recipes
        if not args:
            print("\nAvailable Crafting Recipes:")
            print("=" * 50)
            for recipe_id, recipe in RECIPES.items():
                print(f"{recipe_id} - {recipe['name']}")
                print(f"  Description: {recipe['description']}")
                print("  Materials needed:")
                for material, count in recipe['materials'].items():
                    material_name = ITEMS.get(material, {}).get('name', material)
                    print(f"    - {material_name} x{count}")
                print()
            print("Usage: /craft [recipe_name]")
            return

        # Get recipe to craft
        recipe_id = args[0].lower()
        if recipe_id not in RECIPES:
            print(f"Unknown recipe: {recipe_id}")
            print("Use /craft to see available recipes.")
            return

        recipe = RECIPES[recipe_id]

        # Check if player has the required materials
        materials_found = {}
        for material, count_needed in recipe["materials"].items():
            # Find material in inventory
            found = False
            for i, item in enumerate(self.player["inventory"]):
                if item.get("id") == material:
                    if "count" in item:
                        if item["count"] >= count_needed:
                            materials_found[material] = {"idx": i, "count": count_needed}
                            found = True
                            break
                    else:
                        materials_found[material] = {"idx": i, "count": 1}
                        found = True
                        break

            if not found:
                material_name = ITEMS.get(material, {}).get('name', material)
                print(f"You don't have enough {material_name} to craft this item.")
                return

        # Remove materials from inventory
        for material, data in materials_found.items():
            self.remove_from_inventory(data["idx"], data["count"])

        # Add crafted item to inventory
        result_id = recipe["result"]
        result_count = recipe.get("count", 1)

        if self.add_to_inventory(result_id, result_count):
            print(f"You crafted: {ITEMS[result_id]['name']}!")
            print(ITEMS[result_id]["description"])

            # Crafting takes a moderate amount of time
            self.advance_time("medium_action")
        else:
            print("Inventory full! Couldn't add crafted item.")

    def cmd_go(self, *args):
        """Travel to a different location."""
        if not args:
            print("Usage: /go [location]")
            print("Available locations:")
            for loc_id, loc_data in LOCATIONS.items():
                if loc_id != self.player["location"]:
                    print(f"- {loc_id} ({loc_data['name']})")
            return

        destination = args[0].lower()
        if destination in LOCATIONS:
            if destination == self.player["location"]:
                print("You are already there.")
                return

            # Check if player has enough stamina
            if self.player["stamina"] < 10:
                print("You're too exhausted to travel. Rest or use items to restore stamina.")
                return

            # Check for random encounter while traveling
            danger_level = LOCATIONS[destination]["danger_level"]
            if danger_level > 0 and random.random() < (0.2 * danger_level):
                print("\nWhile traveling, you encounter a zombie!")
                self.current_zombie = self.spawn_zombie()
                self.start_combat()
                if not self.game_running:  # Player died in combat
                    return

            self.player["location"] = destination
            print(f"\nYou have traveled to {LOCATIONS[destination]['name']}.")
            self.player["stamina"] = max(self.player["stamina"] - 10, 0)  # Traveling costs stamina

            # Check mission progress
            self.check_mission_progress("location", destination)

            # Travel is a heavy action that takes significant time
            self.advance_time("heavy_action")

            self.cmd_look()
        else:
            print(f"Unknown location: {destination}")

    def cmd_explore(self, *args):
        """Explore the area for resources."""
        # Check if player has enough stamina
        if self.player["stamina"] < 15:
            print("You're too exhausted to explore. Rest or use items to restore stamina.")
            return

        location = LOCATIONS[self.player["location"]]
        print(f"\nExploring {location['name']}...")
        time.sleep(1)  # Brief delay for tension

        # Chance of finding items based on location danger
        chance = 0.5 + (location["danger_level"] * 0.1)
        if random.random() < chance:
            # Determine what type of item was found
            resource_types = location["resource_types"]
            resource_type = random.choice(resource_types)

            # Get items of that type
            matching_items = [item_id for item_id, item in ITEMS.items() 
                             if item["type"] == resource_type or 
                                (resource_type == "weapons" and item["type"] == "weapon") or
                                (resource_type == "medical" and item["type"] == "medical")]

            if matching_items:
                found_item_id = random.choice(matching_items)
                found_item = ITEMS[found_item_id]

                # Add to inventory if there's space
                if self.add_to_inventory(found_item_id):
                    print(f"You found: {found_item['name']}!")
                    print(found_item["description"])

                    # Check mission progress
                    self.check_mission_progress("collect", found_item)
                else:
                    print(f"You found {found_item['name']}, but your inventory is full!")
            else:
                print("You searched the area but found nothing useful.")
        else:
            print("You searched the area but found nothing useful.")

        # Cost of exploring
        self.player["stamina"] -= 15

        # Exploration is a medium action that takes a fair amount of time
        self.advance_time("medium_action")

        # Chance of zombie encounter
        danger_level = location["danger_level"]
        if danger_level > 0 and random.random() < (0.15 * danger_level):
            print("\nWhile exploring, you encounter a zombie!")
            self.current_zombie = self.spawn_zombie()
            self.start_combat()

        # Mission progress for exploration-type missions
        self.check_mission_progress("explore", self.player["location"])

    def start_combat(self):
        """Initialize combat with a zombie."""
        if not self.current_zombie:
            return

        self.in_combat = True
        zombie = self.current_zombie

        # Check time of day for combat adjustments
        current_hour = self.player["hours_passed"] % 24
        is_night = current_hour in NIGHT_HOURS
        is_dawn_dusk = current_hour in DAWN_DUSK_HOURS

        # Day/night color coding
        time_color = Colors.YELLOW
        if is_night:
            time_color = Colors.BLUE
        elif is_dawn_dusk:
            time_color = Colors.MAGENTA

        # Apply night combat modifier
        damage_boost = 0  # Initialize variable to prevent unbound error
        if is_night and NIGHT_ZOMBIE_DAMAGE_MODIFIER > 1.0:
            original_damage = zombie["damage"]
            zombie["damage"] = int(zombie["damage"] * NIGHT_ZOMBIE_DAMAGE_MODIFIER)
            damage_boost = zombie["damage"] - original_damage

        print("\n" + Colors.colorize("="*50, time_color))
        print(Colors.colorize(f"COMBAT: {zombie['name']} appears!", Colors.BOLD + Colors.RED))
        print(Colors.colorize("="*50, time_color))

        # Show health with colors
        zombie_health_color = Colors.health_color(zombie["health"], zombie["max_health"])
        player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

        zombie_health = zombie["health"]
        zombie_max_health = zombie["max_health"]
        player_health = self.player["health"]
        player_max_health = self.player["max_health"]

        print(f"Zombie Health: {Colors.colorize(f'{zombie_health}/{zombie_max_health}', zombie_health_color)}")
        print(f"Your Health: {Colors.colorize(f'{player_health}/{player_max_health}', player_health_color)}")

        # Show day/night status effects
        if is_night:
            print(Colors.colorize("\nNight Combat: Zombies deal more damage and are harder to hit!", Colors.BOLD + Colors.BLUE))
            if 'damage_boost' in locals():
                print(Colors.colorize(f"The darkness gives the zombie +{damage_boost} attack damage!", Colors.RED))
        elif is_dawn_dusk:
            print(Colors.colorize("\nDusk/Dawn Combat: Limited visibility affects combat.", Colors.MAGENTA))

        # Apply weather effects to combat
        current_weather = self.player.get("current_weather", "clear")
        if current_weather in WEATHER_TYPES and current_weather != "clear":
            weather_info = WEATHER_TYPES[current_weather]

            # Display weather combat effects
            if current_weather == "rainy":
                print(Colors.colorize("\nRain Effect: Zombies move slower but visibility is reduced.", weather_info["color"]))
            elif current_weather == "foggy":
                print(Colors.colorize("\nFog Effect: Severely reduced visibility - increased miss chance!", weather_info["color"]))
            elif current_weather == "stormy":
                print(Colors.colorize("\nStorm Effect: Zombies are slower but visibility is poor.", weather_info["color"]))
            elif current_weather == "windy":
                print(Colors.colorize("\nWind Effect: Ranged weapons less accurate.", weather_info["color"]))
            elif current_weather == "hot":
                print(Colors.colorize("\nHeat Effect: Zombies are more aggressive.", Colors.RED))
            elif current_weather == "cold":
                print(Colors.colorize("\nCold Effect: You move slower in the cold.", Colors.BLUE))

        print("\nCommands: /attack, /flee, /inventory, /use, /equip")

        # Combat loop handled by the main game loop and combat commands

    def cmd_attack(self, *args):
        """Attack the current zombie in combat."""
        if not self.in_combat or not self.current_zombie:
            print(Colors.colorize("You are not in combat.", Colors.YELLOW))
            return

        # Player attacks first
        zombie = self.current_zombie
        hardcore_mode = self.player.get("hardcore_mode", False)

        # Check if player has equipped weapon
        weapon = None
        damage = 5  # Base unarmed damage

        # In hardcore mode, player stamina affects combat performance
        stamina_percent = self.player["stamina"] / self.player["max_stamina"]
        stamina_penalty = 0
        damage_reduction = 0  # Initialize here to avoid unbound variable

        if weapon and weapon["durability"] <= 0:
                print(Colors.colorize(f"Your {weapon['name']} breaks from extensive use!", Colors.RED))
                self.remove_from_inventory(self.player["equipped_weapon"])
                self.player["equipped_weapon"] = None
                return  # Add this to prevent further attack processing

        if hardcore_mode and stamina_percent < 0.3:
            stamina_penalty = 0.2  # 20% penalty to hit chance when exhausted
            damage_reduction = 0.3  # 30% reduction to damage when exhausted
            damage = int(damage * (1 - damage_reduction))
            print(Colors.colorize("\n⚠️ You're exhausted! Your attacks are less effective.", Colors.YELLOW))

            # Each attack costs stamina
            stamina_cost = 2
            self.player["stamina"] = max(0, self.player["stamina"] - stamina_cost)

            # Update exhaustion level in hardcore mode
            self.player["exhaustion"] = min(100, self.player.get("exhaustion", 0) + 5)

        # Mental stress effects in hardcore mode
        insanity_penalty = 0
        if hardcore_mode and self.player.get("insanity", 0) > 50:
            insanity_penalty = 0.1  # 10% additional penalty when mentally stressed
            print(Colors.colorize("Your mental state is affecting your combat performance...", Colors.MAGENTA))

            # Chance of hallucination during combat
            if random.random() < 0.1:
                hallucinations = [
                    "The zombie's face morphs into someone you once knew...",
                    "The walls seem to close in around you during combat...",
                    "You hear whispers telling you to give up...",
                    "Your vision blurs momentarily...",
                    "For a moment, you see dozens of zombies instead of one..."
                ]
                print(Colors.colorize(f"\n  {random.choice(hallucinations)}", Colors.MAGENTA))

        if self.player["equipped_weapon"] is not None:
            weapon = self.player["inventory"][self.player["equipped_weapon"]]
            damage = weapon["damage"]

            # In hardcore mode, apply stamina penalty to damage
            if hardcore_mode and stamina_percent < 0.3:
                damage = int(damage * (1 - damage_reduction))

            # Special weapon effects
            weapon_id = weapon.get("id", "")

            # Handle Molotov Cocktail (area effect weapon)
            if weapon_id == "molotov" or weapon.get("aoe", False):
                print(Colors.colorize(f"You throw the {weapon['name']} at the zombies!", Colors.YELLOW))
                print(Colors.colorize("The area erupts in flames!", Colors.RED))

                # Deal damage to primary zombie
                zombie["health"] -= damage
                print(f"The {zombie['name']} takes {Colors.colorize(str(damage), Colors.RED)} damage from the flames!")

                # Chance to attract more zombies but also damage them
                if random.random() < 0.5:
                    extra_damage = damage // 2
                    print(Colors.colorize("The fire spreads, damaging nearby zombies!", Colors.YELLOW))
                    print(f"All zombies in the area take an additional {Colors.colorize(str(extra_damage), Colors.RED)} damage.")
                    zombie["health"] -= extra_damage

                # Molotov is single-use
                self.remove_from_inventory(self.player["equipped_weapon"])
                self.player["equipped_weapon"] = None

                # Skip the normal attack flow
                if zombie["health"] <= 0:
                    self.end_combat(True)
                    return

                # Skip to zombie's attack
                print(Colors.colorize("\nThe flames die down...", Colors.YELLOW))

            # Check if weapon uses ammo
            elif "ammo" in weapon:
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is out of ammo!", Colors.RED))
                    damage = damage // 3  # Use as melee weapon, much less effective
                else:
                    weapon["ammo"] -= 1
                    print(Colors.colorize(f"You fire your {weapon['name']}! ({weapon['ammo']} ammo left)", Colors.CYAN))

                    # Gunshots have a chance to attract more zombies in hardcore mode
                    if hardcore_mode and random.random() < 0.2:
                        print(Colors.colorize("\n⚠️ The sound of gunfire may attract more zombies to this area!", Colors.YELLOW))

            # Check if weapon has reach advantage (like spear)
            elif weapon.get("reach", 0) > 1:
                hit_chance = 0.8 + min(0.05 * (self.player["level"] - 1), 0.15) # Initialize hit_chance
                # Weapons with reach have better hit chance and reduce chance of being hit back
                hit_chance_bonus = 0.1
                hit_chance += hit_chance_bonus  # Add the bonus to the hit chance
                print(Colors.colorize(f"You attack with your {weapon['name']}, keeping the zombie at a distance.", Colors.CYAN))

            # Reduce weapon durability (unless already handled, like with the molotov)
            if weapon_id != "molotov" and not weapon.get("aoe", False):
                # In hardcore mode, weapons degrade faster
                durability_loss = 2
                if hardcore_mode:
                    durability_loss = 3

                weapon["durability"] = max(0, weapon["durability"] - durability_loss)

                # Warn about low durability
                if weapon["durability"] <= 20 and weapon["durability"] > 0:
                    print(Colors.colorize(f"⚠️ Your {weapon['name']} is severely damaged and might break soon!", Colors.YELLOW))

                if weapon["durability"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} breaks from extensive use!", Colors.RED))
                    self.remove_from_inventory(self.player["equipped_weapon"])
                    self.player["equipped_weapon"] = None
                    return  # Add return to prevent further processing

        else:
            print(Colors.colorize("You attack with your bare hands!", Colors.YELLOW))

        # If not a special weapon that skips normal attack flow
        if self.player["equipped_weapon"] is not None or weapon is None:
            # Calculate hit chance (80% base + player level advantage + weapon bonuses)
            hit_chance = 0.8 + min(0.05 * (self.player["level"] - 1), 0.15)

            # Apply hardcore mode penalties
            hit_chance -= stamina_penalty
            hit_chance -= insanity_penalty

            # Get current weather for combat modifiers
            current_weather = self.player.get("current_weather", "clear")
            weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

            # Apply weather effects to combat
            if current_weather == "foggy":
                hit_chance -= 0.2  # Severely reduced accuracy in fog
                print(Colors.colorize("The thick fog makes it difficult to aim accurately.", weather_info["color"]))
            elif current_weather == "rainy":
                hit_chance -= 0.1  # Reduced accuracy in rain
                print(Colors.colorize("The rain affects your grip and visibility.", weather_info["color"]))
            elif current_weather == "stormy":
                hit_chance -= 0.15  # Significantly reduced accuracy in storms
                print(Colors.colorize("The howling storm hampers your movements.", weather_info["color"]))
            elif current_weather == "windy":
                # Wind affects ranged weapons more
                if weapon and "ammo" in weapon:
                    hit_chance -= 0.15  # Ranged weapons severely affected by wind
                    print(Colors.colorize("The strong winds make it difficult to aim!", weather_info["color"]))
                else:
                    hit_chance -= 0.05  # Melee weapons less affected
            elif current_weather == "hot":
                hit_chance -= 0.07  # Reduced accuracy due to heat exhaustion
                print(Colors.colorize("The oppressive heat slows your reactions.", weather_info["color"]))
            elif current_weather == "cold":
                hit_chance += 0.05  # Easier to hit slower zombies in cold
                print(Colors.colorize("The cold slows the zombie, making it easier to hit.", weather_info["color"]))

            # Broken limb effect in hardcore mode
            if hardcore_mode and self.player.get("broken_limb", False):
                hit_chance -= 0.15
                damage = int(damage * 0.7)  # 30% damage reduction
                print(Colors.colorize("Your broken limb makes it difficult to fight effectively.", Colors.YELLOW))

            # Add weapon-specific bonuses
            if weapon and weapon.get("reach", 0) > 1:
                hit_chance += 0.1

            # Ensure hit chance has reasonable bounds regardless of modifiers
            hit_chance = max(0.2, min(hit_chance, 0.95))

            if random.random() < hit_chance:
                # Critical hit system with weather effects
                critical_hit = False
                crit_chance = 0.1  # Base 10% critical hit chance for hardcore mode

                # Weather affects critical hit chance
                if current_weather == "stormy":
                    crit_chance += 0.05  # Dramatic lightning enhances critical moments
                elif current_weather == "hot":
                    crit_chance -= 0.03  # Heat makes precise strikes harder
                elif current_weather == "cold":
                    crit_chance += 0.02  # Cold weather allows for more deliberate strikes

                if hardcore_mode and random.random() < crit_chance:
                    critical_hit = False
                    crit_chance = 0.1  # Base 10% critical hit chance for hardcore mode

                    # Weather affects critical hit chance
                    if current_weather == "stormy":
                        crit_chance += 0.05  # Dramatic lightning enhances critical moments
                    elif current_weather == "hot":
                        crit_chance -= 0.03  # Heat makes precise strikes harder
                    elif current_weather == "cold":
                        crit_chance += 0.02  # Cold weather allows for more deliberate strikes

                    if hardcore_mode and random.random() < crit_chance:
                        critical_hit = True
                        damage = int(damage * 1.5)  # 50% more damage on critical
                        print(Colors.colorize("⚡ CRITICAL HIT!", Colors.BOLD + Colors.YELLOW))

                        # **Use the `critical_hit` variable here**
                        if critical_hit:
                            zombie["health"] -= damage
                            print(f"You hit the {zombie['name']} for {Colors.colorize(str(damage), Colors.RED)} damage!")

                # Weapon special effects in hardcore mode
                if hardcore_mode and weapon:
                    # Bladed weapons have chance to cause bleeding
                    if weapon.get("id", "") in ["machete", "kitchen_knife"] and random.random() < 0.3:
                        print(Colors.colorize(f"Your {weapon['name']} causes the zombie to bleed!", Colors.RED))
                        zombie["bleeding"] = True

                    # Blunt weapons have chance to stun
                    if weapon.get("id", "") in ["baseball_bat", "reinforced_bat"] and random.random() < 0.2:
                        print(Colors.colorize(f"Your {weapon['name']} stuns the zombie temporarily!", Colors.YELLOW))
                        zombie["stunned"] = True
            else:
                print(Colors.colorize(f"You miss the {zombie['name']}!", Colors.YELLOW))

            # Check if zombie is defeated
            if zombie["health"] <= 0:
                self.end_combat(True)
                return

        # Zombie attacks back (unless stunned)
        if hardcore_mode and zombie.get("stunned", False):
            print(Colors.colorize("The zombie is stunned and cannot attack this turn!", Colors.GREEN))
            zombie["stunned"] = False  # Stun wears off after one turn
        else:
            dodge_bonus = 0
            if weapon and weapon.get("reach", 0) > 1:
                dodge_bonus = 0.15  # Harder for zombie to hit you if you have a reach weapon

            # Zombie attack chance calculation
            hit_chance = 0.6 + 0.1 * zombie.get("speed", 1) - dodge_bonus

            # Get weather info again to apply to zombie attack
            current_weather = self.player.get("current_weather", "clear")
            weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

            # Weather effects on zombie attacks
            if current_weather == "rainy":
                hit_chance -= 0.07  # Zombies slower in rain
                print(Colors.colorize("The rain slows the zombie's movements.", weather_info["color"]))
            elif current_weather == "stormy":
                hit_chance -= 0.12  # Zombies much slower in heavy storm
                print(Colors.colorize("The storm severely hampers the zombie's attack.", weather_info["color"]))
            elif current_weather == "foggy":
                hit_chance += 0.1  # Easier for zombies to surprise you in fog
                print(Colors.colorize("The fog gives the zombie a surprise advantage!", weather_info["color"]))
            elif current_weather == "hot":
                hit_chance += 0.08  # Zombies more aggressive in heat
                print(Colors.colorize("The heat makes the zombie more aggressive.", weather_info["color"]))
            elif current_weather == "cold":
                hit_chance -= 0.1  # Zombies slower in cold
                print(Colors.colorize("The cold weather makes the zombie sluggish.", weather_info["color"]))

            # Hardcore mode gives zombies a better chance to hit when player is in bad shape
            if hardcore_mode:
                if stamina_percent < 0.3:
                    hit_chance += 0.1  # Harder to dodge when tired
                if self.player.get("broken_limb", False):
                    hit_chance += 0.15  # Much harder to dodge with a broken limb
                if self.player.get("insanity", 0) > 50:
                    hit_chance += 0.1  # Mental stress affects reactions

            # Ensure reasonable bounds for hit chance
            hit_chance = max(0.2, min(hit_chance, 0.95))

            if random.random() < hit_chance:
                damage = zombie["damage"]

                # Boss zombies in hardcore mode have special abilities
                special_attack = False
                if hardcore_mode and zombie.get("boss", False):
                    # Tank has slam attack
                    if zombie.get("id") == "tank" and random.random() < 0.2:
                        print(Colors.colorize("The Tank performs a devastating slam attack!", Colors.BOLD + Colors.RED))
                        damage = int(damage * 1.5)
                        self.player["stamina"] = max(0, self.player["stamina"] - 20)  # Drains stamina
                        special_attack = True

                        # Chance to cause broken limb
                        if random.random() < 0.3:
                            self.player["broken_limb"] = True
                            print(Colors.colorize("The impact breaks one of your limbs!", Colors.BOLD + Colors.RED))

                    # Screamer has disorienting attack
                    elif zombie.get("id") == "screamer" and random.random() < 0.25:
                        print(Colors.colorize("The Screamer lets out an ear-piercing shriek!", Colors.BOLD + Colors.RED))
                        damage = int(damage * 0.7)  # Less physical damage
                        special_attack = True

                        # Increases insanity
                        insanity_increase = random.randint(5, 15)
                        self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_increase)
                        print(Colors.colorize(f"The shriek disturbs your mental state! (+{insanity_increase} insanity)", Colors.MAGENTA))

                    # Boomer has toxic attack
                    elif zombie.get("id") == "boomer" and random.random() < 0.3:
                        print(Colors.colorize("The Boomer vomits toxic bile on you!", Colors.BOLD + Colors.GREEN))
                        damage = int(damage * 0.5)  # Less immediate damage
                        special_attack = True

                        # High chance of infection
                        if random.random() < 0.7:
                            self.player["infected"] = True
                            print(Colors.colorize("The toxic bile infects your wounds!", Colors.RED))

                # Apply damage to player
                self.player["health"] -= damage

                if special_attack:
                    # Already printed special attack messages
                    pass
                else:
                    print(Colors.colorize(f"The {zombie['name']} hits you for {damage} damage!", Colors.RED))

                # Infection chance in hardcore mode (regular zombies)
                if hardcore_mode and not special_attack and not self.player.get("infected", False):
                    if random.random() < INFECTION_CHANCE:
                        self.player["infected"] = True
                        print(Colors.colorize("The zombie's attack has infected you!", Colors.RED))

                # Bleeding chance in hardcore mode
                if hardcore_mode and not self.player.get("bleeding", False):
                    if (zombie.get("id", "") == "hunter" and random.random() < 0.4) or random.random() < 0.15:
                        self.player["bleeding"] = True
                        print(Colors.colorize("The zombie's attack has caused you to start bleeding!", Colors.RED))

                # Check if player died
                if self.player["health"] <= 0:
                    self.player["health"] = 0
                    self.end_combat(False)

                    # Record death in death log for hardcore mode
                    if self.player.get("hardcore_mode", False):
                        if self.death_log is None:
                            self.death_log = self.load_death_log()
                        # Get zombie name for death cause
                        zombie_name = zombie.get("name", "Zombie")
                        self.record_death(f"Killed by {zombie_name}")

                        # Delete save file in permadeath mode
                        if PERMADEATH and os.path.exists(SAVE_FILE):
                            try:
                                os.remove(SAVE_FILE)
                                print(Colors.colorize("\nHARDCORE MODE: Your save file has been deleted.", Colors.BOLD + Colors.RED))
                            except Exception as e:
                                print(f"Error removing save file: {e}")
                                pass

                    print(Colors.colorize("\n💀 You have died... Game over.", Colors.BOLD + Colors.RED))
                    self.game_running = False
                    return
            else:
                print(Colors.colorize(f"The {zombie['name']} misses you!", Colors.GREEN))

            # Special zombie effects even on miss (for bosses in hardcore mode)
            if hardcore_mode and zombie.get("boss", False) and zombie.get("id") == "hunter" and random.random() < 0.15:
                print(Colors.colorize("The Hunter's quick movements make it hard to keep your balance.", Colors.YELLOW))
                stamina_loss = random.randint(5, 10)
                self.player["stamina"] = max(0, self.player["stamina"] - stamina_loss)
                print(Colors.colorize(f"You lose {stamina_loss} stamina trying to keep up.", Colors.YELLOW))

        # Display combat status with color
        health_color = Colors.health_color(zombie["health"], zombie["max_health"])
        player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

        zombie_health_text = f"{zombie['health']}/{zombie['max_health']}"
        print(f"\nZombie Health: {Colors.colorize(zombie_health_text, health_color)}")

        player_health_text = f"{self.player['health']}/{self.player['max_health']}"
        print(f"Your Health: {Colors.colorize(player_health_text, player_health_color)}")

        # Display additional info in hardcore mode
        if hardcore_mode:
            stamina_color = Colors.health_color(self.player["stamina"], self.player["max_stamina"])
            stamina_text = f"{self.player['stamina']}/{self.player['max_stamina']}"
            print(f"Stamina: {Colors.colorize(stamina_text, stamina_color)}")

            # Status effects
            status_effects = []
            if self.player.get("bleeding", False):
                status_effects.append(Colors.colorize("Bleeding", Colors.RED))
            if self.player.get("infected", False):
                status_effects.append(Colors.colorize("Infected", Colors.RED))
            if self.player.get("broken_limb", False):
                status_effects.append(Colors.colorize("Broken Limb", Colors.YELLOW))
            if self.player.get("insanity", 0) > 50:
                status_effects.append(Colors.colorize("Mental Stress", Colors.MAGENTA))

            if status_effects:
                print(f"Status: {', '.join(status_effects)}")

        # Combat takes time (medium action)
        self.advance_time("medium_action")

    def cmd_flee(self, *args):
        """Attempt to flee from combat."""
        if not self.in_combat or not self.current_zombie:
            print(Colors.colorize("You are not in combat.", Colors.YELLOW))
            return

        hardcore_mode = self.player.get("hardcore_mode", False)    
        zombie = self.current_zombie

        # Stamina affects escape chance in hardcore mode
        stamina_penalty = 0

        if hardcore_mode:
            # Fleeing costs stamina
            stamina_cost = 15  # Significant stamina cost to flee

            if self.player["stamina"] < stamina_cost:
                print(Colors.colorize("You're too exhausted to run away!", Colors.RED))
                stamina_penalty = 0.2  # Severe penalty when too tired
                # Still allow attempt but with penalty
            else:
                self.player["stamina"] -= stamina_cost

            # Update exhaustion in hardcore mode
            self.player["exhaustion"] = min(100, self.player.get("exhaustion", 0) + 10)

            if self.player.get("broken_limb", False):
                stamina_penalty += 0.25  # Very hard to flee with broken limb
                print(Colors.colorize("Your broken limb makes running difficult!", Colors.RED))

            if self.player.get("insanity", 0) > 70:
                stamina_penalty += 0.15  # Mental stress affects decision making
                print(Colors.colorize("Your panicked mind can't focus on escape routes!", Colors.MAGENTA))

        # Base flee chance calculation
        flee_chance = 0.5 - 0.1 * zombie.get("speed", 1) + 0.05 * self.player["level"] - stamina_penalty

        # Boss zombies are harder to flee from
        if zombie.get("boss", False):
            flee_chance -= 0.2
            print(Colors.colorize("The powerful zombie makes escape difficult!", Colors.RED))

        # Apply weather effects to flee chance
        current_weather = self.player.get("current_weather", "clear")
        weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

        if current_weather == "rainy":
            flee_chance -= 0.05  # Rain makes terrain slippery
            print(Colors.colorize("The rain makes the ground slippery as you try to escape.", weather_info["color"]))
        elif current_weather == "stormy":
            flee_chance -= 0.1  # Storm severely impedes movement
            print(Colors.colorize("The violent storm makes running difficult!", weather_info["color"]))
        elif current_weather == "foggy":
            flee_chance += 0.1  # Fog helps concealment for escape
            print(Colors.colorize("The fog provides cover for your escape attempt.", weather_info["color"]))
        elif current_weather == "hot":
            flee_chance -= 0.07  # Heat makes prolonged running harder
            print(Colors.colorize("The heat saps your energy as you try to flee.", weather_info["color"]))
        elif current_weather == "cold":
            flee_chance -= 0.05  # Cold makes quick movements harder
            print(Colors.colorize("The cold makes your muscles stiffer as you attempt to run.", weather_info["color"]))

        # Display flee attempt animation
        print(Colors.colorize("\nAttempting to escape...", Colors.YELLOW))

        # In hardcore mode, display current chances
        if hardcore_mode:
            chance_display = int(flee_chance * 100)
            chance_color = Colors.GREEN if chance_display > 50 else Colors.YELLOW if chance_display > 25 else Colors.RED
            chance_text = f"{chance_display}%"
            print(f"Escape chance: {Colors.colorize(chance_text, chance_color)}")

            # Warning for low chance
            if chance_display < 30:
                print(Colors.colorize("⚠️ The odds don't look good!", Colors.RED))

        # Process flee attempt
        if random.random() < flee_chance:
            print(Colors.colorize("\nYou successfully escape from the zombie!", Colors.GREEN))

            # In hardcore mode, there's still a risk when fleeing
            if hardcore_mode:
                # Chance of losing items when fleeing
                if random.random() < 0.15:
                    # Determine which item might be dropped
                    if len(self.player["inventory"]) > 0:
                        dropped_idx = random.randint(0, len(self.player["inventory"]) - 1)
                        dropped_item = self.player["inventory"][dropped_idx]

                        print(Colors.colorize(f"In your haste, you drop your {dropped_item['name']}!", Colors.RED))

                        # Drop the item
                        self.remove_from_inventory(dropped_idx)

                        # If it was the equipped weapon, remove that reference
                        if self.player["equipped_weapon"] == dropped_idx:
                            self.player["equipped_weapon"] = None
                        # Adjust equipped weapon index if necessary
                        elif self.player["equipped_weapon"] is not None and self.player["equipped_weapon"] > dropped_idx:
                            self.player["equipped_weapon"] -= 1

                # Chance of injury when fleeing
                if random.random() < 0.1:
                    injury_damage = random.randint(5, 10)
                    self.player["health"] -= injury_damage
                    print(Colors.colorize(f"You stumble while escaping and take {injury_damage} damage!", Colors.RED))

                    # Chance of broken limb from fall
                    if random.random() < 0.2 and not self.player.get("broken_limb", False):
                        self.player["broken_limb"] = True
                        print(Colors.colorize("You twist your ankle badly in the escape!", Colors.RED))

            self.end_combat(False)
        else:
            print(Colors.colorize("\nYou fail to escape!", Colors.RED))

            # Zombie gets a more powerful attack due to failed escape
            damage = zombie["damage"]

            # In hardcore mode, failed escapes are more dangerous
            if hardcore_mode:
                damage_modifier = 1.25  # 25% more damage on failed escape
                damage = int(damage * damage_modifier)

                print(Colors.colorize("The zombie catches you from behind as you try to run!", Colors.RED))

            # Apply damage to player
            self.player["health"] -= damage
            print(Colors.colorize(f"The {zombie['name']} hits you for {damage} damage!", Colors.RED))

            # Special effects on failed escape in hardcore mode
            if hardcore_mode:
                # Higher infection chance when caught fleeing
                if not self.player.get("infected", False) and random.random() < INFECTION_CHANCE * 1.5:
                    self.player["infected"] = True
                    print(Colors.colorize("The zombie's attack has infected you!", Colors.RED))

                # Higher bleeding chance when caught fleeing
                if not self.player.get("bleeding", False) and random.random() < 0.25:
                    self.player["bleeding"] = True
                    print(Colors.colorize("The zombie's attack has caused you to start bleeding!", Colors.RED))

                # Mental trauma from failed escape
                insanity_increase = random.randint(3, 8)
                self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_increase)

                if insanity_increase > 5:
                    print(Colors.colorize("The failed escape attempt increases your sense of hopelessness.", Colors.MAGENTA))

            # Check if player died
            if self.player["health"] <= 0:
                self.player["health"] = 0

                # Record death in death log for hardcore mode
                if self.player.get("hardcore_mode", False):
                    if self.death_log is None:
                        self.death_log = self.load_death_log()
                    # Get zombie name for death cause
                    zombie_name = zombie.get("name", "Zombie")
                    self.record_death(f"Killed while fleeing from {zombie_name}")

                    # Delete save file in permadeath mode
                    if PERMADEATH:
                        save_slots = self.get_save_slots()
                        for save in save_slots:
                            slot_file = os.path.join(SAVES_FOLDER, f"save_slot_{save['slot']}.json")
                            try:
                                os.remove(slot_file)
                                print(Colors.colorize("\nHARDCORE MODE: Your save file has been deleted.", Colors.BOLD + Colors.RED))
                            except Exception as e:
                                print(f"Error removing save file: {e}")
                                pass

                print(Colors.colorize("\n💀 You have died while trying to escape... Game over.", Colors.BOLD + Colors.RED))
                self.end_combat(False)
                self.game_running = False
                return

            # Display combat status with color
            health_color = Colors.health_color(zombie["health"], zombie["max_health"])
            player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

            zombie_health_text = f"{zombie['health']}/{zombie['max_health']}"
            print(f"\nZombie Health: {Colors.colorize(zombie_health_text, health_color)}")

            player_health_text = f"{self.player['health']}/{self.player['max_health']}"
            print(f"Your Health: {Colors.colorize(player_health_text, player_health_color)}")

            # Display additional info in hardcore mode
            if hardcore_mode:
                stamina_color = Colors.health_color(self.player["stamina"], self.player["max_stamina"])
                stamina_text = f"{self.player['stamina']}/{self.player['max_stamina']}"
                print(f"Stamina: {Colors.colorize(stamina_text, stamina_color)}")

                # Status effects
                status_effects = []
                if self.player.get("bleeding", False):
                    status_effects.append(Colors.colorize("Bleeding", Colors.RED))
                if self.player.get("infected", False):
                    status_effects.append(Colors.colorize("Infected", Colors.RED))
                if self.player.get("broken_limb", False):
                    status_effects.append(Colors.colorize("Broken Limb", Colors.YELLOW))
                if self.player.get("insanity", 0) > 50:
                    status_effects.append(Colors.colorize("Mental Stress", Colors.MAGENTA))

                if status_effects:
                    print(f"Status: {', '.join(status_effects)}")

            # Fleeing takes time (medium action)
            self.advance_time("medium_action")

    def end_combat(self, victory):
        """End combat state and apply results."""
        self.in_combat = False

        if victory and self.current_zombie is not None:
            # Base XP gain is influenced by zombie speed
            xp_gain = 20 + 10 * self.current_zombie.get("speed", 1)

            # Special zombie types give more XP
            zombie_type = self.current_zombie.get("type") if self.current_zombie else None
            if zombie_type == "stalker":
                xp_gain += 15  # Forest stalkers are worth more XP

            print(f"\nYou defeated the {self.current_zombie['name']}!")
            print(f"Gained {xp_gain} XP!")

            self.player["xp"] += xp_gain
            self.player["zombies_killed"] += 1

            # Check for mission progress related to killing specific zombie types
            self.check_mission_progress("kill", self.current_zombie)

            # Check for level up
            self.level_up()

            # Chance to find items depends on zombie type
            loot_chance = 0.3  # Base 30% chance

            # Special zombie types have better loot
            if self.current_zombie and self.current_zombie.get("type") == "brute":
                loot_chance = 0.5  # Brutes have more loot
            elif self.current_zombie and self.current_zombie.get("type") == "stalker":
                loot_chance = 0.6  # Forest stalkers have the best loot chance

            if random.random() < loot_chance:
                # Different zombie types tend to have different loot
                item_types = ["food", "medical", "material"]

                # Forest stalkers might drop crafting materials
                if self.current_zombie and self.current_zombie.get("type") == "stalker":
                    item_types = ["material", "material", "food", "medical"]  # Weight toward materials

                item_type = random.choice(item_types)

                matching_items = [item_id for item_id, item in ITEMS.items() 
                                 if item["type"] == item_type]

                if matching_items:
                    found_item_id = random.choice(matching_items)
                    found_item = ITEMS[found_item_id]

                    # Add item to inventory
                    if self.add_to_inventory(found_item_id):
                        print(f"You found {found_item['name']} on the zombie!")

        # Reset combat state
        self.current_zombie = None

    def cmd_missions(self, *args):
        """Show active and available missions."""
        if not self.player["active_missions"]:
            print("\nYou have no active missions.")
        else:
            print("\nActive Missions:")
            print("=" * 50)
            for mission_id in self.player["active_missions"]:
                mission = MISSIONS[mission_id]
                print(f"- {mission['name']}")
                print(f"  {mission['description']}")
                print(f"  Objective: {mission['objective']}")
                print(f"  Location: {LOCATIONS[mission['location']]['name']}")
                print(f"  Reward: {mission['reward']['xp']} XP")
                if "item" in mission["reward"]:
                    item_name = ITEMS[mission["reward"]["item"]]["name"]
                    count = mission["reward"].get("count", 1)
                    print(f"          {count}x {item_name}")
                print()

        if self.player["completed_missions"]:
            print("\nCompleted Missions:")
            print("=" * 50)
            for mission_id in self.player["completed_missions"]:
                mission = MISSIONS[mission_id]
                print(f"- {mission['name']}")

    def cmd_save(self, *args):
        """Save the current game state using the slot system."""
        # Check if a slot number was provided as an argument
        slot = None
        if args and len(args) > 0:
            try:
                slot_arg = int(args[0])
                if 1 <= slot_arg <= MAX_SAVE_SLOTS:
                    slot = slot_arg
                else:
                    print(f"Invalid save slot. Please use a number between 1 and {MAX_SAVE_SLOTS}.")
                    return
            except ValueError:
                print("Invalid save slot. Please use a number.")
                return

        # Save the game
        self.save_game(slot)

    def cmd_saves_list(self, *args):
        """Display a list of all available save slots."""
        save_slots = self.get_save_slots()

        # Display stylish save slots header
        divider = "=" * 50
        print(Colors.colorize(f"\n{divider}", Colors.RED))
        print(Colors.colorize("SAVE SLOT MANAGEMENT".center(50), Colors.BOLD + Colors.YELLOW))
        print(Colors.colorize(f"{divider}", Colors.RED))

        print(Colors.colorize(f"\n{divider}", Colors.CYAN))
        print(Colors.colorize("AVAILABLE SAVE SLOTS".center(50), Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"{divider}", Colors.CYAN))

        # Display save slots in a more stylish format
        if save_slots:
            print()  # Add space before slots
            for save in save_slots:
                slot_header = f"Slot {save['slot']}:"
                print(Colors.colorize(slot_header, Colors.BOLD + Colors.GREEN))

                # Display character info with colors
                character_info = f"Survivor: {Colors.colorize(save['name'], Colors.YELLOW)}, "
                character_info += f"Level {Colors.colorize(str(save['level']), Colors.YELLOW)} "
                character_info += f"({Colors.colorize(str(save['days_survived']), Colors.RED)} days survived)"
                print(character_info)

                # Display location with cyan color
                location_info = f"Location: {Colors.colorize(LOCATIONS[save['location']]['name'], Colors.CYAN)}"
                print(location_info)

                # Display zombie kills and resources gathered
                stats = f"Zombies Killed: {Colors.colorize(str(save.get('zombies_killed', 0)), Colors.RED)}, "
                stats += f"Resources: {Colors.colorize(str(save.get('resources_gathered', 0)), Colors.GREEN)}"
                print(stats)

                # Display save date with purple color
                date_str = datetime.fromtimestamp(save['saved_date']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Saved: {Colors.colorize(date_str, Colors.MAGENTA)}")
                print()  # Add space after each slot
        else:
            print(Colors.colorize("\nNo saved games found.", Colors.YELLOW))
            print(Colors.colorize("Start a new game and use /save [slot] to create your first save.", Colors.CYAN))

        # Calculate empty slots
        used_slots = [save['slot'] for save in save_slots]
        empty_slots = [i for i in range(1, MAX_SAVE_SLOTS + 1) if i not in used_slots]

        # Show empty slots in a more attractive format
        if empty_slots:
            print(Colors.colorize("Empty slots:", Colors.BOLD))
            empty_slots_str = ", ".join([str(slot) for slot in empty_slots])
            print(Colors.colorize(f"[{empty_slots_str}]", Colors.BLUE))

        # Usage tips with styled box
        print(Colors.colorize(f"\n{divider}", Colors.GREEN))
        print(Colors.colorize("SAVE COMMANDS".center(50), Colors.BOLD + Colors.GREEN))
        print(Colors.colorize(f"{divider}", Colors.GREEN))

        print(f"\n  {Colors.colorize('/save [slot]', Colors.YELLOW)} - Save to a slot (1-5)")
        print(f"  {Colors.colorize('/load [slot]', Colors.YELLOW)} - Load from a slot (1-5)")
        print(f"  {Colors.colorize('/saves_list', Colors.YELLOW)} - Show this list of save slots")

        # Some flavor text
        print(Colors.colorize(f"\n{divider}", Colors.RED))
        print(Colors.colorize("Every save is a story waiting to be continued...".center(50), Colors.MAGENTA))

    def cmd_load(self, *args):
        """Load a saved game using the slot system."""
        # Check if a slot number was provided as an argument
        slot = None
        if args and len(args) > 0:
            try:
                slot_arg = int(args[0])
                if 1 <= slot_arg <= MAX_SAVE_SLOTS:
                    slot = slot_arg
                else:
                    print(f"Invalid save slot. Please use a number between 1 and {MAX_SAVE_SLOTS}.")
                    return
            except ValueError:
                print("Invalid save slot. Please use a number.")
                return

        # Load the game
        if self.load_game(slot):
            self.cmd_status()
        # Note: Error messages are handled within the load_game method

    def cmd_map(self, *args):
        """Display a map of available locations."""
        print(Colors.colorize("\n=== AVAILABLE LOCATIONS ===", Colors.BOLD + Colors.CYAN))

        # Create a simple ASCII map
        map_art = """
        .-----------.-----------.-----------.-----------.-----------. 
        |           |           |           |           |           |
        |   CAMP    |   TOWN    |  HOSPITAL |   MALL    |  MILITARY |
        |   (Safe)  |  Danger 2 |  Danger 3 | Danger 4  |  Danger 5 |
        |           |           |           |           |           |
        '-----------'-----------'-----------'-----------'-----------'
        |           |           |
        |  FOREST   |    GAS    |
        | Danger 3  | STATION 2 |
        |           |           |
        '-----------'-----------'
        """

        print(Colors.colorize(map_art, Colors.GREEN))

        # Current location marker
        current_loc = self.player["location"]
        print(f"Current location: {Colors.colorize(LOCATIONS[current_loc]['name'], Colors.BOLD + Colors.RED)}")

        # Print location details
        print(Colors.colorize("\nLocation Details:", Colors.BOLD + Colors.YELLOW))
        for loc_id, loc in LOCATIONS.items():
            location_name = loc["name"]
            danger = "⚠️" * loc["danger_level"] if loc["danger_level"] > 0 else "✓ Safe"

            if loc_id == current_loc:
                location_name = Colors.colorize(f"► {location_name} ◄", Colors.BOLD + Colors.RED)

            visited = "✓" if loc_id in self.player["locations_visited"] else "?"

            print(f"{location_name} - Danger: {danger} - Visited: {visited}")
            if loc_id in self.player["locations_visited"]:
                resource_types = ", ".join(loc["resource_types"])
                print(f"  Resources: {resource_types}")
            print()

    def cmd_stats(self, *args):
        """Show detailed player statistics."""
        p = self.player

        # Title
        header = "\n===== SURVIVOR STATISTICS ====="
        print(Colors.colorize(header, Colors.BOLD + Colors.CYAN))

        # Basic stats
        print(Colors.colorize("\nSURVIVAL RECORD:", Colors.BOLD + Colors.YELLOW))

        days_text = f"Days Survived: {p['days_survived']}"
        print(f"{Colors.colorize(days_text, Colors.GREEN)}")

        zombies_text = f"Zombies Killed: {p['zombies_killed']}"
        print(f"{Colors.colorize(zombies_text, Colors.RED)}")

        bosses_text = f"Bosses Defeated: {len(p['bosses_defeated'])}"
        print(f"{Colors.colorize(bosses_text, Colors.RED)}")

        locations_text = f"Locations Discovered: {len(p['locations_visited'])}/{len(LOCATIONS)}"
        print(f"{Colors.colorize(locations_text, Colors.BLUE)}")

        # Combat stats
        print(Colors.colorize("\nCOMBAT STATS:", Colors.BOLD + Colors.YELLOW))

        damage_dealt_text = f"Total Damage Dealt: {p['damage_dealt']}"
        print(f"{Colors.colorize(damage_dealt_text, Colors.RED)}")

        damage_taken_text = f"Total Damage Taken: {p['damage_taken']}"
        print(f"{Colors.colorize(damage_taken_text, Colors.RED)}")

        # Survival stats
        print(Colors.colorize("\nSURVIVAL ACTIVITY:", Colors.BOLD + Colors.YELLOW))

        crafted_text = f"Items Crafted: {p['items_crafted']}"
        print(f"{Colors.colorize(crafted_text, Colors.GREEN)}")

        distance_text = f"Distance Traveled: {p['distance_traveled']} km"
        print(f"{Colors.colorize(distance_text, Colors.BLUE)}")

        resources_text = f"Resources Gathered: {p['resources_gathered']}"
        print(f"{Colors.colorize(resources_text, Colors.GREEN)}")

        # Missions
        print(Colors.colorize("\nMISSION STATUS:", Colors.BOLD + Colors.YELLOW))

        active_text = f"Active Missions: {len(p['active_missions'])}"
        print(f"{Colors.colorize(active_text, Colors.CYAN)}")

        completed_text = f"Completed Missions: {len(p['completed_missions'])}"
        print(f"{Colors.colorize(completed_text, Colors.GREEN)}")

        # Calculate completion rate
        completion_rate = 0
        if len(MISSIONS) > 0:
            completion_rate = len(p['completed_missions']) / len(MISSIONS) * 100

        rate_text = f"Completion Rate: {completion_rate:.1f}%"
        print(f"{Colors.colorize(rate_text, Colors.GREEN)}")

    def cmd_time(self, *args):
        """Display current game time and date."""
        # Call the existing update_game_time method
        self.update_game_time()

        # Additional time-based info
        hours = self.player["hours_passed"] % 24
        time_of_day = ""
        if 5 <= hours < 8:
            time_of_day = "Early Morning"
        elif 8 <= hours < 12:
            time_of_day = "Morning"
        elif 12 <= hours < 15:
            time_of_day = "Afternoon"
        elif 15 <= hours < 18:
            time_of_day = "Late Afternoon"
        elif 18 <= hours < 21:
            time_of_day = "Evening"
        elif 21 <= hours < 24:
            time_of_day = "Night"
        else:  # 0 <= hours < 5
            time_of_day = "Late Night"

        print(f"Time of day: {Colors.colorize(time_of_day, Colors.YELLOW)}")
        print(f"Weather: {Colors.colorize(self.player['current_weather'], Colors.CYAN)}")

        # Survival tip based on time
        tips = [
            "The night is dangerous. Consider resting until morning.",
            "Daytime is best for exploration and gathering resources.",
            "Keep an eye on your hunger and thirst levels.",
            "Always be prepared for combat, especially in dangerous areas.",
            "Conserve ammunition for special zombies and emergencies."
        ]
        print(f"\nSurvival Tip: {Colors.colorize(random.choice(tips), Colors.GREEN)}")

    def cmd_boss(self, *args):
        """Information about boss zombies encountered."""
        bosses = self.player["bosses_defeated"]

        if not bosses:
            print(Colors.colorize("\nYou haven't encountered any boss zombies yet.", Colors.YELLOW))
            print("Complete missions and explore dangerous areas to find them.")
            return

        print(Colors.colorize("\n===== BOSS ZOMBIES ENCOUNTERED =====", Colors.BOLD + Colors.RED))

        for boss_type in bosses:
            if boss_type in ZOMBIE_TYPES:
                boss = ZOMBIE_TYPES[boss_type]
                name = Colors.colorize(boss["name"], Colors.BOLD + Colors.RED)
                print(f"\n{name}")
                print(f"Type: {boss_type}")
                print(f"Health: {boss['health']}")
                print(f"Damage: {boss['damage']}")
                print(f"Special Ability: {boss.get('special_ability', 'None')}")
                print(f"Description: {boss['description']}")

        if len(bosses) < 5:
            remaining = 5 - len(bosses)
            print(f"\nThere are {Colors.colorize(str(remaining), Colors.YELLOW)} more boss zombies to discover!")

    def cmd_weather(self, *args):
        """Check the current weather conditions."""
        # Get the current weather
        current_weather = self.player.get("current_weather", "clear")

        print(Colors.colorize("\n=== CURRENT WEATHER CONDITIONS ===", Colors.BOLD + Colors.CYAN))

        if current_weather in WEATHER_TYPES:
            weather_info = WEATHER_TYPES[current_weather]
            weather_name = weather_info["name"]
            weather_color = weather_info["color"]
            weather_symbol = weather_info.get("symbol", "")
            weather_description = weather_info["description"]
            weather_effects = weather_info["effects"]

            # Display current weather information with color
            print(Colors.colorize(f"{weather_symbol} {weather_name}", weather_color))
            print(f"\n{weather_description}")
            print(f"\nGameplay Effects: {Colors.colorize(weather_effects, Colors.YELLOW)}")

            # Display specific mechanical effects based on weather
            print(Colors.colorize("\nDetailed Effects:", Colors.BOLD))

            if current_weather == "clear":
                print("- Normal exploration and combat conditions")
                print("- Standard stamina usage for all activities")
            elif current_weather == "cloudy":
                print("- Slightly reduced chance to find resources")
                print("- Minor visibility reduction")
            elif current_weather == "rainy":
                print("- Stamina drains 20% faster during travel")
                print("- Zombies move 10% slower")
                print("- Visibility reduced in combat (slightly higher miss chance)")
            elif current_weather == "foggy":
                print("- Greatly increased zombie ambush chance during exploration")
                print("- 20% higher miss chance in combat")
                print("- Significantly reduced visibility for all activities")
            elif current_weather == "stormy":
                print("- Stamina recovery reduced by 50%")
                print("- Zombies move 15% slower")
                print("- 40% increase in zombie spawns (thunder attracts them)")
                print("- Visibility severely impacted")
            elif current_weather == "windy":
                print("- 25% reduced accuracy with ranged weapons")
                print("- 15% faster stamina drain during exploration")
                print("- Reduces ability to hear zombies approaching")
            elif current_weather == "hot":
                print("- Stamina drains 30% faster during all activities")
                print("- Thirst depletes 40% faster")
                print("- Zombies are 20% more aggressive and deal more damage")
            elif current_weather == "cold":
                print("- Player moves 20% slower")
                print("- Hunger depletes 30% faster")
                print("- Stamina recovery reduced by 25%")
        else:
            print("Unknown weather conditions.")

        # Weather forecast for next few hours
        print(Colors.colorize("\nForecast:", Colors.BOLD))
        # Generate a more realistic forecast by giving current weather a higher chance
        weather_keys = list(WEATHER_TYPES.keys())
        weights = [3 if w == current_weather else 1 for w in weather_keys]
        forecast = random.choices(weather_keys, weights=weights, k=3)

        for i, weather in enumerate(forecast):
            hours = (self.player["hours_passed"] + (i+1)*6) % 24
            time_str = f"{hours:02d}:00"

            # Display forecast with appropriate day/night period
            if hours in NIGHT_HOURS:
                time_period = "(Night)"
                time_color = Colors.BLUE
            elif hours in DAWN_DUSK_HOURS:
                time_period = "(Dawn/Dusk)"
                time_color = Colors.MAGENTA
            else:
                time_period = "(Day)"
                time_color = Colors.YELLOW

            # Get weather symbol and name
            weather_info = WEATHER_TYPES[weather]
            weather_symbol = weather_info.get("symbol", "")
            weather_name = weather_info["name"]
            weather_color = weather_info["color"]

            # Format the forecast entry
            forecast_time = Colors.colorize(f"In {(i+1)*6} hours ({time_str}) {time_period}: ", time_color)
            forecast_weather = Colors.colorize(f"{weather_symbol} {weather_name}", weather_color)
            print(f"{forecast_time}{forecast_weather}")

    def cmd_upgrade_camp(self, *args):
        """View or upgrade camp facilities."""
        if self.player["location"] != "camp":
            print(Colors.colorize("You must be at the camp to upgrade facilities!", Colors.RED))
            return

        if args and args[0].lower() in CAMP_UPGRADES:
            # Upgrade a specific facility
            upgrade_id = args[0].lower()
            self.upgrade_facility(upgrade_id)
            return

        # Display available upgrades
        print(Colors.colorize("\n=== CAMP FACILITIES ===", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize("Your camp can be upgraded to improve safety and survival odds.", Colors.YELLOW))
        print(Colors.colorize("Materials are required for each upgrade.", Colors.YELLOW))

        # List all current upgrades and their levels
        print(Colors.colorize("\nCURRENT FACILITIES:", Colors.BOLD + Colors.GREEN))

        for upgrade_id, upgrade in CAMP_UPGRADES.items():
            level = upgrade["level"]
            max_level = upgrade["max_level"]

            if level == 0:
                status = Colors.colorize("Not Built", Colors.RED)
            else:
                if level == max_level:
                    status = Colors.colorize(f"Level {level} (MAX)", Colors.GREEN)
                else:
                    status = Colors.colorize(f"Level {level}/{max_level}", Colors.YELLOW)

            # Draw a progress bar for visual representation
            bar_length = 10
            filled = int((level / max_level) * bar_length)
            bar = "[" + "=" * filled + " " * (bar_length - filled) + "]"

            print(f"{Colors.colorize(upgrade['name'], Colors.BOLD + Colors.CYAN)}: {status} {bar}")
            print(f"  {Colors.colorize(upgrade['description'], Colors.BLUE)}")
            print(f"  {Colors.colorize('Benefit:', Colors.GREEN)} {upgrade['benefits']}")

            # Show barricade HP if this is the barricades
            if upgrade_id == "barricades" and level > 0:
                current_hp = upgrade.get("hp", 0)
                max_hp = upgrade.get("max_hp", 100)
                hp_percent = (current_hp / max_hp) * 100
                hp_color = Colors.health_color(current_hp, max_hp)

                print(f"  {Colors.colorize('Barricade HP:', Colors.YELLOW)} {Colors.colorize(f'{current_hp}/{max_hp} ({hp_percent:.1f}%)', hp_color)}")

                if current_hp < max_hp * 0.25:
                    print(f"  {Colors.colorize('⚠️ CRITICAL DAMAGE! Barricades need immediate repairs!', Colors.RED)}")
                elif current_hp < max_hp * 0.5:
                    print(f"  {Colors.colorize('⚠️ WARNING: Barricades are significantly damaged!', Colors.YELLOW)}")

            print("")

        # Show upgrade instructions
        print(Colors.colorize("\nHOW TO UPGRADE:", Colors.BOLD + Colors.CYAN))
        print(f"Use {Colors.colorize('/upgrade_camp [facility_name]', Colors.GREEN)} to upgrade a specific facility.")
        print(f"Example: {Colors.colorize('/upgrade_camp shelter', Colors.GREEN)} to upgrade your shelter.")
        print(f"Repair barricades with {Colors.colorize('/repair_barricades', Colors.GREEN)}.")

        # Explain how facility levels affect gameplay
        print(Colors.colorize("\nFACILITY BENEFITS:", Colors.BOLD + Colors.CYAN))
        print("- Shelter: Improves sleep safety and recovery")
        print("- Barricades: Protects camp from zombie attacks")
        print("- Workshop: Enables more advanced crafting")
        print("- Garden: Provides food over time")
        print("- Radio: Gives information about nearby resources")

        # Advancing time for checking camp facilities
        self.advance_time("light_action")

    def upgrade_facility(self, facility_id):
        """Upgrade a specific camp facility."""
        if facility_id not in CAMP_UPGRADES:
            print(Colors.colorize(f"Unknown facility: {facility_id}", Colors.RED))
            return

        facility = CAMP_UPGRADES[facility_id]
        current_level = facility["level"]
        max_level = facility["max_level"]

        if current_level >= max_level:
            print(Colors.colorize(f"Your {facility['name']} is already at maximum level!", Colors.YELLOW))
            return

        # Calculate materials needed for upgrade
        materials_needed = {
            "wood": (current_level + 1) * 2,
            "metal_scrap": current_level + 1,
            "cloth": current_level
        }

        # Special requirements for advanced facilities
        if facility_id in ["machine_guns", "radio", "drones"]:
            materials_needed["metal_scrap"] *= 2
            materials_needed["cloth"] *= 2

        if facility_id == "workshop" and current_level >= 2:
            materials_needed["metal_scrap"] *= 2

        # Check if player has enough materials
        can_upgrade = True
        missing_materials = {}

        for material, amount in materials_needed.items():
            available = 0
            for idx, item in enumerate(self.player["inventory"]):
                if item.get("id") == material:
                    available += item.get("count", 1)

            if available < amount:
                can_upgrade = False
                missing_materials[material] = amount - available

        # Display upgrade information
        print(Colors.colorize(f"\n=== UPGRADE {facility['name'].upper()} ===", Colors.BOLD + Colors.CYAN))
        print(f"Current level: {Colors.colorize(str(current_level), Colors.YELLOW)}/{Colors.colorize(str(max_level), Colors.GREEN)}")
        print(f"Benefits: {Colors.colorize(facility['benefits'], Colors.BLUE)}")

        # Display materials required
        print(Colors.colorize("\nMaterials required:", Colors.BOLD))
        for material, amount in materials_needed.items():
            material_name = ITEMS.get(material, {}).get("name", material)

            if material in missing_materials:
                status = Colors.colorize(f"MISSING {missing_materials[material]}", Colors.RED)
            else:
                status = Colors.colorize("Available", Colors.GREEN)

            print(f"- {material_name}: {amount} ({status})")

        # Perform upgrade if possible
        if can_upgrade:
            confirm = input(Colors.colorize("\nConfirm upgrade? (y/n): ", Colors.GREEN))
            if confirm.lower() != "y":
                print("Upgrade cancelled.")
                return

            # Remove materials from inventory
            for material, amount in materials_needed.items():
                remaining = amount
                for idx, item in enumerate(self.player["inventory"]):
                    if item.get("id") == material:
                        to_use = min(remaining, item.get("count", 1))
                        remaining -= to_use

                        if item.get("count", 1) <= to_use:
                            # Remove item completely
                            self.player["inventory"].pop(idx)
                        else:
                            # Reduce count
                            self.player["inventory"][idx]["count"] -= to_use

                        if remaining <= 0:
                            break

            # Apply upgrade
            facility["level"] += 1

            # Update effects based on facility
            if facility_id == "barricades":
                # Barricades get more HP with level
                facility["max_hp"] = 100 * facility["level"]
                facility["hp"] = facility["max_hp"]  # Fully repaired after upgrade
                LOCATIONS["camp"]["barricades_intact"] = True

            elif facility_id == "shelter":
                # Better shelter improves sleep quality
                pass  # Already checked in sleep command

            print(Colors.colorize(f"\nUpgrade successful! {facility['name']} is now level {facility['level']}!", Colors.BOLD + Colors.GREEN))

            # Show specific benefits from upgrade
            if facility_id == "workshop":
                print(Colors.colorize("You can now craft more advanced items!", Colors.YELLOW))
            elif facility_id == "barricades":
                print(Colors.colorize("Your camp is now better protected against zombie attacks!", Colors.YELLOW))
            elif facility_id == "garden":
                print(Colors.colorize("Your garden will now produce more food over time!", Colors.YELLOW))

            # Upgrading takes time
            self.advance_time("medium_action")
        else:
            print(Colors.colorize("\nYou don't have enough materials for this upgrade.", Colors.RED))
            print("Go scavenging to find more resources.")

    def cmd_eat(self, *args):
        """Eat food to reduce hunger and possibly gain health."""
        if self.in_combat:
            print(Colors.colorize("You can't eat during combat!", Colors.RED))
            return

        if not args:
            print(Colors.colorize("You need to specify what to eat. Usage: /eat [item_id]", Colors.YELLOW))
            print("Use /inventory to see what food items you have.")
            return

        item_id = args[0].lower()

        # Check if the player has this item
        item_index = None
        for idx, item in enumerate(self.player["inventory"]):
            if item["id"] == item_id:
                item_index = idx
                break

        if item_index is None:
            print(Colors.colorize(f"You don't have {item_id} in your inventory.", Colors.RED))
            return

        # Check if the item is food
        item_data = ITEMS.get(item_id, {})
        if not item_data or item_data.get("type") != "food":
            print(Colors.colorize(f"{item_data.get('name', item_id)} is not edible!", Colors.RED))
            return

        # Process eating the food
        food_name = item_data.get("name", item_id)
        hunger_value = item_data.get("hunger_value", 10)
        health_value = item_data.get("health_value", 0)

        # Calculate safety probability (percentage chance of food being safe)
        safety_prob = item_data.get("safety", 79)  # Default 79% safe like an apple

        # Pills can increase safety probability if the player has them
        has_pills = False
        for inv_item in self.player["inventory"]:
            if inv_item.get("id") == "antibiotics" or inv_item.get("id") == "med_pills":
                has_pills = True
                break

        if has_pills:
            safety_prob += 15  # Pills increase safety by 15%
            safety_prob = min(safety_prob, 99)  # Cap at 99% safety (never 100% safe)
            print(Colors.colorize("You take some medicine before eating to prevent illness.", Colors.CYAN))

        # Check for thirst reduction from the food (some foods like fruits help with thirst)
        thirst_value = item_data.get("thirst_value", 0)

        # Apply effects
        print(Colors.colorize(f"\nYou eat the {food_name}.", Colors.CYAN))

        # Hunger reduction
        old_hunger = self.player["hunger"]
        self.player["hunger"] = min(self.player["max_hunger"], old_hunger + hunger_value)
        hunger_gain = self.player["hunger"] - old_hunger

        hunger_message = f"Hunger: {old_hunger} → {self.player['hunger']} (+{hunger_gain})"
        print(Colors.colorize(hunger_message, Colors.GREEN))

        # Health restoration if applicable
        if health_value > 0:
            old_health = self.player["health"]
            self.player["health"] = min(self.player["max_health"], old_health + health_value)
            health_gain = self.player["health"] - old_health

            health_message = f"Health: {old_health} → {self.player['health']} (+{health_gain})"
            print(Colors.colorize(health_message, Colors.GREEN))

        # Thirst effect if applicable
        if thirst_value > 0:
            old_thirst = self.player["thirst"]
            self.player["thirst"] = min(self.player["max_thirst"], old_thirst + thirst_value)
            thirst_gain = self.player["thirst"] - old_thirst

            thirst_message = f"Thirst: {old_thirst} → {self.player['thirst']} (+{thirst_gain})"
            print(Colors.colorize(thirst_message, Colors.GREEN))

        # Check for food illness based on safety probability
        if random.randint(1, 100) > safety_prob:
            print(Colors.colorize("\nYou don't feel so good after eating that...", Colors.RED))
            Animations.loading_bar(length=10, message="Feeling ill")

            # Determine severity of illness
            recovery_chance = item_data.get("recovery_chance", 80)  # 80% chance of recovery by default

            if has_pills:
                recovery_chance += 15  # Pills increase recovery chance
                recovery_chance = min(recovery_chance, 99)  # Cap at 99%

            # Check if player recovers or gets severely ill
            if random.randint(1, 100) <= recovery_chance:
                # Mild illness
                health_loss = random.randint(5, 15)
                self.player["health"] = max(1, self.player["health"] - health_loss)

                print(Colors.colorize(f"You feel sick for a while, losing {health_loss} health.", Colors.YELLOW))
                print(Colors.colorize("Fortunately, you recover after a few hours of discomfort.", Colors.GREEN))

                # Add sickness effect for hardcore mode
                if self.player.get("hardcore_mode", False):
                    self.player["stamina"] = max(0, self.player["stamina"] - 20)
                    print(Colors.colorize("The illness has left you fatigued.", Colors.YELLOW))
            else:
                # Severe illness - potentially fatal
                print(Colors.colorize("\n⚠️ You've contracted SEVERE FOOD POISONING!", Colors.BOLD + Colors.RED))
                health_loss = random.randint(40, 60)
                self.player["health"] = max(0, self.player["health"] - health_loss)

                print(Colors.colorize(f"You lose {health_loss} health from the poisoning!", Colors.RED))

                # Check if player died
                if self.player["health"] <= 0:
                    death_message = "You died from severe food poisoning."
                    print(Colors.colorize(f"\n☠️ {death_message}", Colors.BOLD + Colors.RED))
                    if self.player.get("hardcore_mode", False):
                        self.record_death(death_message)
                    self.game_running = False
                    return
                else:
                    # Survived but severely weakened
                    print(Colors.colorize("You barely survive the ordeal, but are severely weakened.", Colors.YELLOW))

                    # Add illness effects for hardcore mode
                    if self.player.get("hardcore_mode", False):
                        self.player["infected"] = True
                        self.player["stamina"] = max(0, self.player["stamina"] - 50)
                        print(Colors.colorize("You've developed an infection that will continue to weaken you.", Colors.RED))

        # Remove the item from inventory after eating
        item = self.player["inventory"][item_index]
        if item.get("count", 1) > 1:
            item["count"] -= 1
        else:
            self.player["inventory"].pop(item_index)

        # Eating takes a small amount of time
        self.advance_time("light_action")

    def cmd_dismantle(self, *args):
        """Break down an item into its components."""
        if self.in_combat:
            print(Colors.colorize("You can't dismantle items during combat!", Colors.RED))
            return

        if not args:
            print(Colors.colorize("\nUsage: /dismantle [item_id]", Colors.YELLOW))
            print(Colors.colorize("This command breaks down weapons and items into their component parts.\n", Colors.CYAN))

            # Display items that can be dismantled
            dismantlable_items = []
            for idx, item in enumerate(self.player["inventory"]):
                item_id = item["id"]
                item_data = ITEMS.get(item_id, {})

                # Check if item has craft_recipe or dismantle_yield
                if "craft_recipe" in item_data or "dismantle_yield" in item_data:
                    dismantlable_items.append((idx, item))

            if dismantlable_items:
                print(Colors.colorize("Items you can dismantle:", Colors.GREEN))
                for idx, item in dismantlable_items:
                    print(f"{idx}. {Colors.colorize(ITEMS[item['id']]['name'], Colors.YELLOW)} " +
                          f"(x{item['count']})")
            else:
                print(Colors.colorize("You don't have any items that can be dismantled.", Colors.RED))
            return

        try:
            item_idx = int(args[0])
            if item_idx < 0 or item_idx >= len(self.player["inventory"]):
                print(Colors.colorize("Invalid item index!", Colors.RED))
                return

            item = self.player["inventory"][item_idx]
            item_id = item["id"]
            item_data = ITEMS.get(item_id, {})

            # Check if item is currently equipped
            if self.player.get("equipped") == item_id:
                print(Colors.colorize("You can't dismantle your equipped weapon!", Colors.RED))
                return

            # Determine what components the item breaks down into
            components = {}
            if "dismantle_yield" in item_data:
                # Use defined dismantle yield if available
                components = item_data["dismantle_yield"]
            elif "craft_recipe" in item_data:
                # Otherwise use 60-90% of craft recipe (randomized per component)
                for component, amount in item_data["craft_recipe"].items():
                    # Return 60-90% of each component, minimum 1
                    recovery_rate = random.uniform(0.6, 0.9)
                    recovered_amount = max(1, int(amount * recovery_rate))
                    components[component] = recovered_amount
            else:
                print(Colors.colorize(f"The {ITEMS[item_id]['name']} cannot be dismantled.", Colors.RED))
                return

            # Now perform the dismantling
            print(Colors.colorize(f"\nDismantling {ITEMS[item_id]['name']}...", Colors.CYAN))
            Animations.loading_bar(length=10, message="Breaking down components")

            # Remove the item from inventory
            self.remove_from_inventory(item_idx)

            # Add the components to inventory
            print(Colors.colorize("\nYou recovered:", Colors.GREEN))
            for component, amount in components.items():
                self.add_to_inventory(component, amount)
                if component in ITEMS:
                    component_name = ITEMS[component]['name']
                else:
                    component_name = component.replace('_', ' ').title()
                print(f"- {Colors.colorize(component_name, Colors.YELLOW)} x{amount}")

            # Time advancement for dismantling (light action)
            self.advance_time("light_action")

            # Check for skill improvement chance (crafting-related)
            if random.random() < 0.1:  # 10% chance
                self.player["crafting_skill"] = min(10, self.player.get("crafting_skill", 0) + 1)
                print(Colors.colorize("\nYou've gained insight into how things are assembled. Crafting skill improved!", Colors.MAGENTA))

        except ValueError:
            print(Colors.colorize("Please specify a valid item number.", Colors.RED))
        except Exception as e:
            print(Colors.colorize(f"Error dismantling item: {e}", Colors.RED))

    def cmd_repair_barricades(self, *args):
        """Repair damaged camp barricades."""
        if self.player["location"] != "camp":
            print(Colors.colorize("You must be at the camp to repair barricades!", Colors.RED))
            return

        # Check if barricades exist
        if CAMP_UPGRADES["barricades"]["level"] == 0:
            print(Colors.colorize("You haven't built any barricades yet!", Colors.RED))
            print(f"Use {Colors.colorize('/upgrade_camp barricades', Colors.GREEN)} to build them first.")
            return

        # Check if barricades are already at max HP
        barricades = CAMP_UPGRADES["barricades"]
        if barricades["hp"] >= barricades["max_hp"]:
            print(Colors.colorize("The barricades are already in perfect condition!", Colors.GREEN))
            return

        # Calculate repair needs
        max_hp = barricades["max_hp"]
        current_hp = barricades["hp"]
        missing_hp = max_hp - current_hp
        repair_percentage = (missing_hp / max_hp) * 100

        # Materials needed based on damage
        materials_needed = {
            "wood": math.ceil(missing_hp / 50),  # 1 wood per 50 HP
            "metal_scrap": math.ceil(missing_hp / 100)  # 1 metal per 100 HP
        }

        # Check if player has enough materials
        can_repair = True
        missing_materials = {}

        for material, amount in materials_needed.items():
            available = 0
            for item in self.player["inventory"]:
                if item.get("id") == material:
                    available += item.get("count", 1)

            if available < amount:
                can_repair = False
                missing_materials[material] = amount - available

        # Display repair information
        print(Colors.colorize("\n=== REPAIR BARRICADES ===", Colors.BOLD + Colors.CYAN))

        # Show current HP status
        hp_color = Colors.health_color(current_hp, max_hp)
        hp_percentage = (current_hp / max_hp) * 100
        print(f"Current status: {Colors.colorize(f'{current_hp}/{max_hp} HP ({hp_percentage:.1f}%)', hp_color)}")

        # Visual representation
        bar_length = 20
        filled = int((current_hp / max_hp) * bar_length)
        bar = "[" + "=" * filled + " " * (bar_length - filled) + "]"
        print(f"Integrity: {Colors.colorize(bar, hp_color)}")

        # Repair assessment
        if repair_percentage < 25:
            assessment = "Minor repairs needed"
        elif repair_percentage < 50:
            assessment = "Moderate repairs needed"
        else:
            assessment = "Major repairs needed"

        print(Colors.colorize(f"\n{assessment}", Colors.YELLOW))

        # Materials required
        print(Colors.colorize("\nMaterials required:", Colors.BOLD))
        for material, amount in materials_needed.items():
            material_name = ITEMS.get(material, {}).get("name", material)

            if material in missing_materials:
                status = Colors.colorize(f"MISSING {missing_materials[material]}", Colors.RED)
            else:
                status = Colors.colorize("Available", Colors.GREEN)

            print(f"- {material_name}: {amount} ({status})")

        # Perform repair if possible
        if can_repair:
            confirm = input(Colors.colorize("\nConfirm repair? (y/n): ", Colors.GREEN))
            if confirm.lower() != "y":
                print("Repair cancelled.")
                return

            # Remove materials from inventory
            for material, amount in materials_needed.items():
                remaining = amount
                inventory_copy = self.player["inventory"].copy()
                for idx, item in enumerate(inventory_copy):
                    if item.get("id") == material:
                        to_use = min(remaining, item.get("count", 1))
                        remaining -= to_use

                        if item.get("count", 1) <= to_use:
                            # Remove item completely
                            self.player["inventory"].remove(item)
                        else:
                            # Reduce count
                            item["count"] -= to_use

                        if remaining <= 0:
                            break

            # Apply repair
            barricades["hp"] = max_hp
            LOCATIONS["camp"]["barricades_intact"] = True

            print(Colors.colorize("\nRepairs successful! The barricades are now fully restored!", Colors.BOLD + Colors.GREEN))
            print(Colors.colorize("Your camp is secure once again.", Colors.YELLOW))

            # Repairing takes time
            self.advance_time("medium_action")
        else:
            print(Colors.colorize("\nYou don't have enough materials for repairs.", Colors.RED))
            print("Go scavenging to find more resources.")

    def cmd_scavenge_area(self, *args):
        """Scavenge your current location for resources."""
        if self.in_combat:
            print(Colors.colorize("You can't scavenge while in combat!", Colors.RED))
            return

        # Get current location type
        current_location = self.player["location"]
        location_info = LOCATIONS[current_location]
        location_type = location_info.get("type", "urban")  # Default to urban if not specified

        # Determine scavenge area based on location type
        area_id = location_type

        # If the location has a specific scavenge area defined, use that instead
        if "scavenge_area" in location_info:
            area_id = location_info["scavenge_area"]

        # Check if this is a valid scavenge area
        if area_id not in SCAVENGE_AREAS:
            print(Colors.colorize(f"Unknown area: {area_id}", Colors.RED))
            print("Available areas: " + ", ".join(SCAVENGE_AREAS.keys()))
            return

        # Initialize scavenging session if this is a new area
        if not hasattr(self, 'current_scavenging') or self.current_scavenging['area'] != area_id:
            area = SCAVENGE_AREAS[area_id]
            self.current_scavenging = {
                'area': area_id,
                'area_name': area['name'],
                'round': 1,
                'items_found': [],
                'zombies_killed': 0,
                'risk_modifier': 1.0,
                'loot_modifier': 1.0
            }
            print(Colors.colorize(f"\n=== SCAVENGING: {area['name']} ===", Colors.BOLD + Colors.CYAN))
            print(Colors.colorize(area['description'], Colors.YELLOW))
            print(Colors.colorize(f"Risk Level: {'🔴' * area['risk_level']}", Colors.RED))
        else:
            # Continuing an existing scavenging session
            area = SCAVENGE_AREAS[self.current_scavenging['area']]
            self.current_scavenging['round'] += 1

            # Increase risk and reward with each round
            self.current_scavenging['risk_modifier'] += 0.25
            self.current_scavenging['loot_modifier'] += 0.15

            print(Colors.colorize(f"\n=== CONTINUED SCAVENGING: Round {self.current_scavenging['round']} ===", Colors.BOLD + Colors.CYAN))
            print(Colors.colorize(f"Risk Level: {'🔴' * math.ceil(area['risk_level'] * self.current_scavenging['risk_modifier'])}", Colors.RED))
            print(Colors.colorize(f"Loot Quality: {'⭐' * math.ceil(self.current_scavenging['loot_modifier'])}", Colors.YELLOW))

        # Stamina cost for scavenging
        stamina_cost = 10 * self.current_scavenging['round']
        if self.player["stamina"] < stamina_cost:
            print(Colors.colorize("You're too exhausted to continue scavenging!", Colors.RED))
            print("Take time to rest and try again later.")
            # End scavenging session
            delattr(self, 'current_scavenging')
            return

        # Reduce stamina
        self.player["stamina"] -= stamina_cost
        print(Colors.colorize(f"Searching consumes {stamina_cost} stamina...", Colors.CYAN))

        # Animation for scavenging
        print(Colors.colorize("\nSearching the area carefully...", Colors.CYAN))
        Animations.loading_bar(length=15, message="Scavenging")

        # Determine if a zombie appears
        zombie_chance = area['zombie_chance'] * self.current_scavenging['risk_modifier']

        # In hardcore mode, zombie encounters are more likely
        if self.player.get("hardcore_mode", False):
            zombie_chance += 0.1

        # Check for zombie encounter
        if random.random() < zombie_chance:
            print(Colors.colorize("\n❗ You've encountered a zombie while scavenging!", Colors.BOLD + Colors.RED))

            # Special zombies more likely in later rounds
            special_zombie_chance = 0.1 * self.current_scavenging['round']
            special_zombie_chance = min(special_zombie_chance, 0.5)  # Cap at 50%

            # Spawn zombie and start combat
            if random.random() < special_zombie_chance:
                # Determine which special zombie based on area
                if area_id == "medical":
                    special_type = "spitter"  # Medical zombies often have toxic abilities
                elif area_id == "urban":
                    special_type = "hunter"  # Urban zombies are more aggressive
                elif area_id == "woods":
                    special_type = "stalker"  # Forest zombies are stealthy
                else:
                    special_type = random.choice(["runner", "brute"])

                print(Colors.colorize(f"It's a {ZOMBIE_TYPES[special_type]['name']}!", Colors.BOLD + Colors.RED))
                self.spawn_zombie(specific_type=special_type)
            else:
                # Regular zombie
                self.spawn_zombie()

            self.start_combat()
            return  # Exit scavenging function while in combat

        # If no zombie encounter, find items
        found_something = False

        # Determine how many items to potentially find (1-3, more in later rounds)
        potential_items = min(3, 1 + self.current_scavenging['round'] // 2)

        # For each potential item slot
        for i in range(potential_items):
            # Base chance to find something (60-85%)
            find_chance = 0.6 + (0.05 * self.current_scavenging['loot_modifier'])
            find_chance = min(find_chance, 0.85)  # Cap at 85%

            if random.random() < find_chance:
                # First determine if it's a special item
                special_item_chance = area['special_item_chance'] * self.current_scavenging['loot_modifier']

                if random.random() < special_item_chance and area['special_items']:
                    # Find a special item for this area
                    item_id = random.choice(area['special_items'])
                    found_something = True
                else:
                    # Choose a regular item based on area resource distribution
                    item_type = random.choices(
                        list(area['resource_types'].keys()),
                        weights=list(area['resource_types'].values())
                    )[0]

                    # Find an item of the chosen type
                    matching_items = [item_id for item_id, item in ITEMS.items() 
                                     if item['type'] == item_type]

                    if matching_items:
                        item_id = random.choice(matching_items)
                        found_something = True
                    else:
                        continue

                # Add the item to inventory
                if self.add_to_inventory(item_id):
                    self.current_scavenging['items_found'].append(item_id)
                    item_name = ITEMS[item_id]['name']
                    print(Colors.colorize(f"You found: {item_name}!", Colors.GREEN))
                else:
                    print(Colors.colorize("You found something, but your inventory is full!", Colors.YELLOW))
                    break

        # Update game stats
        if hasattr(self, 'current_scavenging') and self.current_scavenging['items_found']:
            self.player["resources_gathered"] += len(self.current_scavenging['items_found'])

        # Determine time spent based on scavenging round
        estimated_time = 0
        if self.current_scavenging['round'] <= 2:
            # Early rounds are medium actions
            self.advance_time("medium_action")
            estimated_time = 1.5  # Approximately 1.5 hours for medium actions
        else:
            # Later rounds with higher risk are heavy actions
            self.advance_time("heavy_action")
            estimated_time = 3  # Approximately 3 hours for heavy actions

        # No need to call update_survival_stats as advance_time handles that

        if not found_something:
            print(Colors.colorize("You searched thoroughly but didn't find anything useful.", Colors.YELLOW))

        # Ask if player wants to continue scavenging with increasing risk/reward
        print(Colors.colorize("\n--- SCAVENGING RESULTS ---", Colors.BOLD + Colors.CYAN))
        print(f"Items found this session: {len(self.current_scavenging['items_found'])}")
        print(f"Time spent: {estimated_time} hour(s)")

        # Current status
        player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])
        stamina_color = Colors.health_color(self.player["stamina"], self.player["max_stamina"])

        print(Colors.colorize("\n--- YOUR STATUS ---", Colors.BOLD + Colors.YELLOW))
        health_text = f"{self.player['health']}/{self.player['max_health']}"
        print(f"Health: {Colors.colorize(health_text, player_health_color)}")

        stamina_text = f"{self.player['stamina']}/{self.player['max_stamina']}"
        print(f"Stamina: {Colors.colorize(stamina_text, stamina_color)}")

        if self.player.get("hardcore_mode", False):
            # Display status effects in hardcore mode
            status_effects = []
            if self.player.get("bleeding", False):
                status_effects.append(Colors.colorize("Bleeding", Colors.RED))
            if self.player.get("infected", False):
                status_effects.append(Colors.colorize("Infected", Colors.RED))
            if self.player.get("broken_limb", False):
                status_effects.append(Colors.colorize("Broken Limb", Colors.YELLOW))

            if status_effects:
                print(f"Status: {', '.join(status_effects)}")

        # Risk assessment for next round
        next_risk = area['risk_level'] * (self.current_scavenging['risk_modifier'] + 0.25)
        next_reward = self.current_scavenging['loot_modifier'] + 0.15

        print(Colors.colorize("\n--- CONTINUE SCAVENGING? ---", Colors.BOLD + Colors.MAGENTA))
        print(f"Next round risk level: {'🔴' * math.ceil(next_risk)}")
        print(f"Next round loot quality: {'⭐' * math.ceil(next_reward)}")

        # For hardcore mode, give more detailed warnings
        if self.player.get("hardcore_mode", False) and next_risk > 4:
            print(Colors.colorize("⚠️ WARNING: The risk of deadly encounters is extremely high!", Colors.BOLD + Colors.RED))

        # Ask player if they want to continue
        continue_option = input(Colors.colorize("\nContinue scavenging this area? (y/n): ", Colors.GREEN))
        if continue_option.lower() != 'y':
            print(Colors.colorize("\nYou decide to leave with your findings.", Colors.CYAN))
            # End scavenging session
            delattr(self, 'current_scavenging')

        # Update game time display
        self.update_game_time()

    def cmd_quit(self, *args):
        """Quit the game."""
        confirm = input(Colors.colorize("Are you sure you want to quit? Unsaved progress will be lost (y/n): ", Colors.YELLOW))
        if confirm.lower() == 'y':
            farewell = "Thanks for playing Zombie Survival RPG!"
            Animations.type_text(Colors.colorize(farewell, Colors.BOLD + Colors.GREEN))
            self.game_running = False

# Start the game if run directly
if __name__ == "__main__":
    # Check if game was launched from the launcher
    if os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1":
        game = GameState()
        game.start_game()
    else:
        print("This game should be launched through the launch.py launcher.")
        print("Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
