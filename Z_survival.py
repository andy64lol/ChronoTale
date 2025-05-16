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
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# Python3 restriction removed

# Setup save folder
SAVES_FOLDER = "saves"
MAX_SAVE_SLOTS = 5

# Ensure the saves folder exists

# Military grade weapons
# Experimental weapons found only at the research station
EXPERIMENTAL_WEAPONS = {
    "sonic_disruptor": {
        "name": "Sonic Disruptor",
        "type": "weapon",
        "damage": 40,
        "durability": 100,
        "ammo": 30,
        "max_ammo": 30,
        "damage_type": "sonic",
        "stun_chance": 0.75,  # 75% chance to stun enemies
        "location_specific": "research_station",
        "special_effect": "stun",
        "weight": 4,
        "crafting": False,
        "description": "A prototype weapon developed at the research station to study the effects of concentrated sound waves on infected tissue. Emits a focused sonic pulse that disrupts the coordination of infected subjects, temporarily stunning them and causing internal tissue damage. While not as lethal as conventional firearms, its stunning effect provides a significant tactical advantage."
    },
    "cryo_rifle": {
        "name": "Cryogenic Rifle",
        "type": "weapon",
        "damage": 35,
        "durability": 80,
        "ammo": 15,
        "max_ammo": 15,
        "damage_type": "cold",
        "location_specific": "research_station",
        "special_effect": "freeze",
        "slow_effect": 0.6,  # Reduces enemy speed by 60%
        "weight": 6,
        "crafting": False,
        "description": "An experimental weapon that fires specialized ammunition containing rapidly expanding cryo-compounds. Upon impact, these compounds flash-freeze the target, significantly reducing their mobility and causing tissue damage from rapid crystallization. Most effective against fast-moving enemies and those with regenerative capabilities."
    },
    "pulse_gauntlet": {
        "name": "Pulse Gauntlet",
        "type": "weapon",
        "damage": 60,
        "durability": 150,
        "melee": True,
        "damage_type": "electric",
        "location_specific": "research_station",
        "special_effect": "chain_lightning",
        "chain_targets": 3,  # Can hit up to 3 targets
        "weight": 3,
        "crafting": False,
        "description": "A heavy-duty gauntlet retrofitted with experimental high-voltage capacitors. Delivers devastating close-range electrical shocks that can arc between multiple targets when they're in close proximity. Especially effective against groups of infected or when cornered, as the chain lightning effect can create breathing room in tight situations."
    },
    "chemical_thrower": {
        "name": "Experimental Chemical Thrower",
        "type": "weapon",
        "damage": 20,
        "durability": 70,
        "ammo": 50,
        "max_ammo": 50,
        "damage_type": "chemical",
        "area_effect": True,
        "area_damage_radius": 5,
        "dot_damage": 5,  # Damage over time per tick
        "dot_duration": 5,  # Duration in ticks
        "location_specific": "research_station",
        "special_effect": "acid",
        "weight": 7,
        "crafting": False,
        "description": "A repurposed industrial sprayer modified to dispense experimental corrosive compounds developed to break down infected tissue. Creates a lingering chemical cloud that continues to damage anything within its area of effect. The acidic compound is particularly effective against armored infected but requires proper respiratory protection to use safely."
    }
}

MILITARY_WEAPONS = {
    "rpg_launcher": {
        "name": "RPG-7 Launcher",
        "type": "weapon",
        "damage": 150,
        "durability": 50,
        "ammo": 0,
        "max_ammo": 1,
        "area_effect": True,
        "damage_type": "explosive",
        "area_damage_radius": 10,
        "area_damage_percent": 0.8,
        "rarity": 0.02,
        "weight": 7.0,
        "noise_level": 10, # Extremely loud, attracts zombies from very far
        "military_grade": True,
        "description": "An RPG-7 rocket-propelled grenade launcher, complete with optical sight and folding grip. This devastating anti-vehicle weapon can obliterate entire zombie hordes with a single shot, though its thunderous explosion will attract every infected within miles. The rare military hardware is nearly impossible to find outside of military bases and is equally difficult to maintain in the apocalypse."
    },
    "tactical_crossbow": {
        "name": "Tactical Crossbow",
        "type": "weapon",
        "damage": 60,
        "durability": 120,
        "ammo": 1,
        "max_ammo": 1,
        "damage_type": "piercing",
        "rarity": 0.05,
        "weight": 3.5,
        "noise_level": 1, # Nearly silent
        "military_grade": True,
        "stealth_bonus": 0.3, # 30% stealth bonus when using
        "scope": True, # Has scope for better accuracy
        "description": "A modern tactical crossbow with carbon fiber limbs, integrated scope, and military-grade construction. Designed for special forces stealth operations, this weapon delivers lethal strikes with minimal noise, making it perfect for stealth kills that won't alert nearby infected. Its specialized bolts can penetrate zombie skulls with ease."
    },
    "m4_carbine": {
        "name": "M4A1 Carbine",
        "type": "weapon",
        "damage": 45,
        "durability": 200,
        "ammo": 0,
        "max_ammo": 30,
        "fire_rate": 3, # Can hit multiple times per attack
        "damage_type": "ballistic",
        "rarity": 0.03,
        "weight": 3.0,
        "noise_level": 8, # Very loud
        "military_grade": True,
        "customizable": True, # Can add attachments
        "description": "The standard-issue assault rifle of the U.S. military, featuring selective fire capability and tactical rail system for attachments. This reliable weapon offers excellent firepower in a compact package, with manageable recoil even during sustained fire. Its modularity allows for various attachments, though its loud report will draw unwanted attention."
    },
    "riot_shield": {
        "name": "Ballistic Riot Shield",
        "type": "weapon",
        "damage": 15,
        "durability": 300,
        "defensive": True,
        "damage_reduction": 0.7, # Reduces incoming damage by 70%
        "damage_type": "blunt",
        "rarity": 0.04,
        "weight": 7.5,
        "military_grade": True,
        "description": "A heavy-duty polycarbonate riot shield with ballistic protection, originally used by military police and SWAT teams. This transparent shield provides excellent protection against both zombie attacks and survivor weapons, though it limits mobility. Its edge can be used to bash attackers, and the transparent viewport allows you to see incoming threats."
    },
    "flamethrower": {
        "name": "M9 Military Flamethrower",
        "type": "weapon",
        "damage": 60,
        "durability": 100,
        "ammo": 0,
        "max_ammo": 100, # Percentage of fuel
        "area_effect": True,
        "damage_type": "fire",
        "area_damage_radius": 5,
        "area_damage_percent": 1.0,
        "continuous_damage": True, # Causes burning effect
        "rarity": 0.01,
        "weight": 9.0,
        "noise_level": 6,
        "military_grade": True,
        "description": "A military-grade incendiary weapon that projects a controlled stream of flaming fuel. Devastating against groups of infected, this weapon continues to burn enemies after the initial hit. While extremely powerful, it's also dangerous to the user, heavy, and requires specialized fuel that's difficult to source in the apocalypse."
    },
    "rpg_rocket": {
        "name": "RPG Rocket",
        "type": "ammo",
        "count": 1,
        "weight": 2.5,
        "craftable": True,
        "rarity": 0.01,
        "weapon": "rpg_launcher",
        "crafting_difficulty": "extreme",
        "crafting_requirements": {
            "metal_pipe": 1,
            "gunpowder": 3,
            "fuel": 1,
            "explosive_compound": 2,
            "precision_parts": 2,
            "tools": 1
        },
        "description": "A 40mm rocket-propelled warhead for the RPG-7 launcher. The olive-drab metal casing houses a shaped charge designed to penetrate armored vehicles, though against soft targets like zombies, it creates a devastating blast radius. The propellant and stabilizing fins ensure accurate delivery to the target. These sophisticated munitions require extensive technical knowledge to craft or maintain."
    },
    "assault_rifle": {
        "name": "AK-47 Assault Rifle",
        "type": "weapon",
        "damage": 45,
        "durability": 120,
        "ammo": 0,
        "max_ammo": 30,
        "damage_type": "ballistic",
        "fire_rate": 3, # Can hit multiple targets or same target multiple times
        "accuracy": 0.85,
        "rarity": 0.05,
        "weight": 4.5,
        "noise_level": 8,
        "military_grade": True,
        "description": "The iconic AK-47, renowned worldwide for its legendary reliability and stopping power. This particular model shows signs of heavy use—the wooden furniture is scratched and worn, while the metal components bear a patina of use rather than neglect. Even in the apocalypse, the rifle's simple, robust design continues to function with minimal maintenance. The distinctive silhouette and unmistakable sound make it both feared and coveted among survivors."
    },
    "rifle_ammo": {
        "name": "7.62mm Rifle Ammunition",
        "type": "ammo",
        "count": 30,
        "weight": 0.7,
        "craftable": True,
        "rarity": 0.1,
        "weapon": "assault_rifle",
        "crafting_difficulty": "hard",
        "crafting_requirements": {
            "bullet_casing": 30,
            "gunpowder": 2,
            "metal_scrap": 1,
            "tools": 1
        },
        "description": "A box of 7.62×39mm rifle cartridges, the standard ammunition for AK-pattern rifles. Each round consists of a brass casing, primer, powder charge, and steel-core bullet. The stopping power of these rounds makes them effective against both the living and the undead. Handloaded rounds crafted in the apocalypse lack the factory precision of pre-fall ammunition but will still reliably cycle through a properly maintained weapon."
    },
    "lmg": {
        "name": "M249 Light Machine Gun",
        "type": "weapon",
        "damage": 40,
        "durability": 100,
        "ammo": 0,
        "max_ammo": 100,
        "damage_type": "ballistic",
        "fire_rate": 5, # High rate of fire, hits multiple targets
        "accuracy": 0.7,
        "rarity": 0.01,
        "weight": 10.0,
        "noise_level": 9,
        "military_grade": True,
        "description": "A belt-fed light machine gun designed for sustained fire support. The heavy barrel allows for extended firing without overheating, though the weapon's considerable weight makes it unwieldy for extended travel. Perfect for defending fixed positions against hordes of undead, its thunderous report will both clear a path and draw more infected from miles around."
    },
    "belt_ammo": {
        "name": "5.56mm Linked Ammunition",
        "type": "ammo",
        "count": 100,
        "weight": 2.5,
        "craftable": True,
        "rarity": 0.02,
        "weapon": "lmg",
        "crafting_difficulty": "extreme",
        "crafting_requirements": {
            "bullet_casing": 100,
            "gunpowder": 5,
            "metal_scrap": 2,
            "tools": 1,
            "metal_links": 100
        },
        "description": "A belt of linked 5.56mm cartridges for machine gun use. The brass casings gleam dully, connected by metal links designed to smoothly feed through the weapon's action before being ejected. Creating a functional ammunition belt in the post-apocalypse represents the pinnacle of survivor craftsmanship, requiring both extensive technical knowledge and specialized components."
    },
    "sniper_rifle": {
        "name": "Military Sniper Rifle",
        "type": "weapon",
        "damage": 80,
        "durability": 90,
        "ammo": 0,
        "max_ammo": 5,
        "damage_type": "ballistic",
        "range": 3, # Extreme range, can target zombies from 3 locations away
        "accuracy": 0.95,
        "critical_chance": 0.4,
        "critical_multiplier": 3.0,
        "rarity": 0.02,
        "weight": 6.0,
        "noise_level": 7,
        "military_grade": True,
        "description": "A precision long-range rifle with telescopic sight and adjustable stock. Once the domain of military and law enforcement specialists, this rifle's ability to eliminate threats from extreme distances makes it invaluable in the zombie-infested landscape. The pristine optical scope offers unparalleled clarity, allowing for precise shot placement even in challenging conditions."
    }
}

# Vehicle definitions
VEHICLES = {
    "bicycle": {
        "name": "Mountain Bicycle",
        "type": "vehicle",
        "speed": 3, # 3x faster than walking
        "fuel_type": None, # Doesn't require fuel
        "durability": 50,
        "max_durability": 50,
        "capacity": 1, # Passenger capacity
        "noise_level": 1,
        "craftable": True,
        "crafting_difficulty": "medium",
        "crafting_requirements": {
            "metal_pipe": 4,
            "rubber": 2,
            "metal_scrap": 2,
            "chain": 1,
            "tools": 1
        },
        "repair_requirements": {
            "metal_scrap": 1,
            "rubber": 1,
            "tools": 1
        },
        "description": "A sturdy mountain bike with patched tires and a makeshift cargo rack. Silent and requiring no fuel, it's perfect for reconnaissance missions or quick escapes. The lack of engine noise makes it ideal for avoiding infected, though the limited cargo capacity restricts extended journeys."
    },
    "motorcycle": {
        "name": "Modified Motorcycle",
        "type": "vehicle",
        "speed": 6, # 6x faster than walking
        "fuel_type": "gasoline",
        "fuel_capacity": 10,
        "fuel_consumption": 1, # Units per travel
        "durability": 70,
        "max_durability": 70,
        "capacity": 2,
        "noise_level": 6,
        "craftable": True,
        "crafting_difficulty": "hard",
        "crafting_requirements": {
            "engine_parts": 1,
            "metal_frame": 1,
            "wheels": 2,
            "metal_pipe": 4,
            "rubber": 4,
            "metal_scrap": 6,
            "electronics": 1,
            "tools": 1
        },
        "repair_requirements": {
            "metal_scrap": 2,
            "rubber": 1,
            "engine_parts": 1,
            "tools": 1
        },
        "description": "A heavily modified dirt bike with reinforced frame and expanded fuel tank. The engine has been muffled as much as possible without sacrificing too much power, though it's still loud enough to attract infected. Excellent for rapid transit between locations, with enough cargo space for essential supplies."
    },
    "car": {
        "name": "Survivor Sedan",
        "type": "vehicle",
        "speed": 5, # 5x faster than walking but more cargo
        "fuel_type": "gasoline",
        "fuel_capacity": 40,
        "fuel_consumption": 3, # Units per travel
        "durability": 100,
        "max_durability": 100,
        "capacity": 4,
        "cargo_capacity": 10, # Can carry more items
        "noise_level": 5,
        "armor": 2, # Provides protection when inside
        "craftable": False,
        "repair_requirements": {
            "metal_scrap": 5,
            "rubber": 2,
            "engine_parts": 2,
            "electronics": 1,
            "tools": 1
        },
        "description": "A four-door sedan modified for apocalyptic conditions. The windows have been reinforced with salvaged metal grating, and the body shows signs of collision repairs with mismatched panels. The back seats have been removed to maximize storage space, and the fuel system modified to accept lower-quality gasoline. More protected than a motorcycle, but lacks the same off-road capabilities."
    },
    "truck": {
        "name": "Reinforced Pickup Truck",
        "type": "vehicle",
        "speed": 4, # 4x faster than walking
        "fuel_type": "diesel",
        "fuel_capacity": 60,
        "fuel_consumption": 5, # Units per travel
        "durability": 150,
        "max_durability": 150,
        "capacity": 5,
        "cargo_capacity": 20, # Significant cargo space
        "noise_level": 7,
        "armor": 4, # Good protection
        "craftable": False,
        "repair_requirements": {
            "metal_scrap": 8,
            "rubber": 4,
            "engine_parts": 3,
            "electronics": 2,
            "tools": 1
        },
        "description": "A heavy-duty pickup truck with extensive modifications for survival. The bed has been enclosed with a custom cage of steel pipes and mesh, while the front sports a reinforced bumper capable of clearing infected from the road. The elevated suspension and all-terrain tires allow navigation of debris-strewn streets and off-road detours. The diesel engine is louder than preferred but offers superior torque and fuel efficiency."
    },
    "armored_vehicle": {
        "name": "Military Armored Personnel Carrier",
        "type": "vehicle",
        "speed": 3, # 3x faster than walking
        "fuel_type": "diesel",
        "fuel_capacity": 150,
        "fuel_consumption": 12, # Units per travel
        "durability": 300,
        "max_durability": 300,
        "capacity": 8,
        "cargo_capacity": 40, # Massive cargo space
        "noise_level": 8,
        "armor": 10, # Extreme protection
        "military_grade": True,
        "craftable": False,
        "repair_requirements": {
            "metal_plate": 5,
            "rubber": 4,
            "engine_parts": 5,
            "electronics": 3,
            "hydraulics": 2,
            "military_parts": 3,
            "tools": 1
        },
        "description": "A decommissioned military APC with extensive armor plating and reinforced windows. The interior has been stripped of military equipment and repurposed for survival, with added storage compartments and crude living facilities. Near-impervious to infected attacks, it can plow through hordes with minimal damage. The extreme fuel consumption and noise are significant drawbacks, but nothing offers better protection on the move."
    },
    "military_humvee": {
        "name": "Military Humvee",
        "type": "vehicle",
        "speed": 5, # 5x faster than walking
        "fuel_type": "gasoline",
        "fuel_consumption": 3, # Higher consumption rate
        "durability": 120,
        "max_durability": 120,
        "capacity": 4, # Passenger capacity
        "noise_level": 3,
        "armor": 0.6, # Strong protection from zombies
        "military_origin": True,
        "craftable": False,
        "found_at": ["military_base"],
        "repair_requirements": {
            "metal_sheet": 2,
            "tools": 1,
            "rubber": 2,
            "industrial_parts": 1
        },
        "description": "A High Mobility Multipurpose Wheeled Vehicle (HMMWV) still in military colors, with reinforced frame and bulletproof windows. The overhead weapon mount has been removed, but the vehicle retains excellent all-terrain capability and defensive features. Offers substantial protection against infected attacks with room for passengers and supplies. The military-grade armor plating makes it nearly impervious to regular zombies."
    },
    "military_truck": {
        "name": "Military Transport Truck",
        "type": "vehicle",
        "speed": 3.5, # 3.5x faster than walking
        "fuel_type": "diesel",
        "fuel_consumption": 4, # Very high consumption rate
        "durability": 150,
        "max_durability": 150,
        "capacity": 8, # High passenger capacity
        "storage_capacity": 500, # Significant cargo space
        "noise_level": 4,
        "armor": 0.4, # Good protection from zombies
        "military_origin": True,
        "craftable": False,
        "found_at": ["military_base"],
        "repair_requirements": {
            "metal_sheet": 3,
            "tools": 1,
            "rubber": 2,
            "industrial_parts": 2
        },
        "description": "A 5-ton military transport truck with canvas-covered rear cargo area and six-wheel drive. Designed for troop and supply transport in combat zones, it offers exceptional carrying capacity and durability. The large profile attracts significant zombie attention, but the elevated cab and reinforced undercarriage provide good protection. Ideal for relocating groups of survivors and large quantities of supplies."
    },
    "armored_personnel_carrier": {
        "name": "Armored Personnel Carrier",
        "type": "vehicle",
        "speed": 4, # 4x faster than walking
        "fuel_type": "diesel",
        "fuel_consumption": 5, # Extremely high consumption rate
        "durability": 200,
        "max_durability": 200,
        "capacity": 6, # Good passenger capacity
        "storage_capacity": 300, # Decent cargo space
        "noise_level": 5,
        "armor": 0.8, # Excellent protection from zombies
        "military_origin": True,
        "craftable": False,
        "found_at": ["military_base"],
        "repair_requirements": {
            "metal_sheet": 4,
            "tools": 2,
            "electronics": 1,
            "industrial_parts": 3
        },
        "description": "A tracked armored fighting vehicle designed to transport infantry into battle and provide fire support. This decommissioned military APC features heavy armor plating, small vision ports with bulletproof glass, and a top hatch. The interior has been stripped of weapons systems but retains seating and storage. Extremely effective at plowing through zombie hordes and nearly impervious to attacks, its main drawbacks are the excessive fuel consumption and noise that attracts infected from considerable distances."
    }
}

# New buildings that can be constructed at camp
BUILDINGS = {
    "workshop": {
        "name": "Survivor's Workshop",
        "level": 1,
        "max_level": 3,
        "construction_requirements": {
            "wood": 20,
            "metal_scrap": 15,
            "tools": 1
        },
        "upgrade_requirements": {
            2: {"wood": 30, "metal_scrap": 25, "electronics": 1, "tools": 1},
            3: {"wood": 50, "metal_scrap": 40, "electronics": 3, "precision_parts": 1, "tools": 2}
        },
        "benefits": {
            1: {"crafting_bonus": 0.1, "repair_bonus": 0.1},
            2: {"crafting_bonus": 0.2, "repair_bonus": 0.2, "advanced_crafting": True},
            3: {"crafting_bonus": 0.3, "repair_bonus": 0.3, "advanced_crafting": True, "military_crafting": True}
        },
        "description": "A dedicated space for crafting, repairing, and modifying equipment. Higher levels unlock more advanced crafting recipes and improve success rates for complex items."
    },
    "garage": {
        "name": "Vehicle Garage",
        "level": 1,
        "max_level": 3,
        "construction_requirements": {
            "wood": 30,
            "metal_scrap": 25,
            "tools": 1
        },
        "upgrade_requirements": {
            2: {"wood": 45, "metal_scrap": 40, "engine_parts": 1, "tools": 1},
            3: {"wood": 70, "metal_scrap": 60, "engine_parts": 3, "electronics": 2, "tools": 2}
        },
        "benefits": {
            1: {"vehicle_repair_bonus": 0.1, "vehicle_storage": 1},
            2: {"vehicle_repair_bonus": 0.2, "vehicle_storage": 2, "vehicle_crafting": True},
            3: {"vehicle_repair_bonus": 0.3, "vehicle_storage": 3, "vehicle_crafting": True, "military_vehicle_repair": True}
        },
        "description": "A covered structure for storing, repairing, and eventually constructing vehicles. Higher levels allow for more complex vehicle modifications and repairs to military vehicles."
    },
    "watchtower": {
        "name": "Observation Tower",
        "level": 1,
        "max_level": 3,
        "construction_requirements": {
            "wood": 25,
            "metal_scrap": 10,
            "rope": 2
        },
        "upgrade_requirements": {
            2: {"wood": 40, "metal_scrap": 20, "tools": 1},
            3: {"wood": 60, "metal_scrap": 35, "electronics": 1, "tools": 1}
        },
        "benefits": {
            1: {"detection_range": 1, "defense_bonus": 0.1},
            2: {"detection_range": 2, "defense_bonus": 0.2, "distant_scouting": True},
            3: {"detection_range": 3, "defense_bonus": 0.3, "distant_scouting": True, "zombie_migration_tracking": True}
        },
        "description": "An elevated platform providing visibility of the surrounding area. Helps detect approaching zombie hordes and potential threats. Higher levels increase detection range and enable tracking of zombie migrations."
    },
    "armory": {
        "name": "Survivor Armory",
        "level": 1,
        "max_level": 3,
        "construction_requirements": {
            "metal_scrap": 30,
            "wood": 20,
            "tools": 1,
            "lock": 1
        },
        "upgrade_requirements": {
            2: {"metal_scrap": 50, "wood": 30, "electronics": 1, "tools": 1},
            3: {"metal_scrap": 80, "wood": 50, "electronics": 2, "precision_parts": 2, "tools": 2}
        },
        "benefits": {
            1: {"weapon_storage": 10, "ammo_crafting_bonus": 0.1},
            2: {"weapon_storage": 20, "ammo_crafting_bonus": 0.2, "weapon_repair": True},
            3: {"weapon_storage": 30, "ammo_crafting_bonus": 0.3, "weapon_repair": True, "military_maintenance": True}
        },
        "description": "A secure storage facility for weapons and ammunition. Higher levels allow for weapon maintenance, repairs, and eventually maintenance of military-grade hardware."
    }
}
if not os.path.exists(SAVES_FOLDER):
    os.makedirs(SAVES_FOLDER)

class Colors:
    # Use colorama for cross-platform compatibility
    HEADER = Fore.MAGENTA + Style.BRIGHT
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    MAGENTA = Fore.MAGENTA
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT
    UNDERLINE = Style.BRIGHT  # Closest approximation in colorama

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
        "special_items": ["pistol", "metal_scrap", "fuel", "tactical_flashlight", "office_supplies", "sonic_disruptor"],
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
        "special_items": ["kitchen_knife", "cloth", "baseball_bat", "canned_food", "family_photo", "nail_bat"],
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
        "special_items": ["wood", "fresh_fruit", "medicinal_herbs", "hunting_knife", "wild_game", "crossbow_bolt", "machete"],
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
        "special_items": ["tools", "metal_scrap", "industrial_parts", "protective_gear", "preserved_food", "flamethrower", "hazmat_piercer"],
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
        "special_items": ["textbooks", "science_equipment", "cafeteria_food", "first_aid_supplies", "sports_equipment", "battery_pack"],
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
        "special_items": ["seeds", "fertilizer", "farming_tools", "fresh_produce", "preserved_meats", "fuel_canister"],
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
        "special_items": ["riot_shield", "prison_shank", "guard_baton", "pepper_spray", "handcuffs", "taser", "prison_jumpsuit", "antibiotics", "tactical_crossbow"],
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

# Boss zombie types - special high-difficulty encounters
BOSS_ZOMBIES = {
    "behemoth": {
        "name": "Behemoth",
        "health": 300,
        "damage": 35,
        "speed": 0.7,
        "armor": 0.4,
        "special_ability": "ground_pound",
        "special_moves": ["slam", "charge", "roar"],
        "description": "A colossal infected that towers over others, with muscles grotesquely enlarged and skin hardened into natural armor plates. The Behemoth can crush enemies with devastating physical attacks and shrug off significant damage. Its thunderous roars can stun survivors temporarily."
    },
    "patient_zero": {
        "name": "Patient Zero",
        "health": 200,
        "damage": 25,
        "speed": 1.5,
        "special_ability": "mutation",
        "regeneration": True,
        "special_moves": ["toxic_spray", "call_horde", "mutate"],
        "description": "One of the first infected, exhibiting unique mutations and retaining fragments of intelligence. Patient Zero can evolve during combat, adapting to attacks and developing new offensive capabilities. It can release pheromones to call other infected and regenerate health over time."
    },
    "tank_commander": {
        "name": "Tank Commander",
        "health": 250,
        "damage": 30,
        "speed": 1.1,
        "armor": 0.6,
        "special_ability": "coordinated_attack",
        "military_origin": True,
        "special_moves": ["order_attack", "suppressive_fire", "take_cover"],
        "description": "Formerly a high-ranking military officer infected while inside an armored vehicle. Protected by military-grade body armor and tactical helmet, the Tank Commander retains advanced combat skills and can issue guttural commands that coordinate other military zombies in sophisticated attack patterns."
    },
    "behemoth_mammoth": {
        "name": "Behemoth Mammoth",
        "health": 400,
        "damage": 45,
        "speed": 0.6,
        "armor": 0.7,
        "special_ability": "trample",
        "animal_origin": True,
        "special_moves": ["charge", "tusk_sweep", "earth_shatter"],
        "location_specific": "zoo",
        "description": "A terrifying fusion of elephant and infected tissue, standing nearly fifteen feet tall with elongated, twisted tusks that can impale vehicles. Its hide, thickened from the infection, is resistant to most conventional weapons, and patches of bone armor protrude from vital areas. The creature's massive size allows it to trample through barricades and survivor defenses with ease, while its deafening roar can induce panic in even the most hardened survivors."
    },
    "living_hive": {
        "name": "The Living Hive",
        "health": 220,
        "damage": 20,
        "speed": 0.8,
        "special_ability": "spawn_infected",
        "regeneration": True,
        "special_moves": ["acid_spray", "spawn_parasites", "toxic_cloud"],
        "location_specific": "research_station",
        "description": "Once the head researcher at Polaris Station, now a horrific amalgamation of human and experimental bioweapon. The Living Hive's distended abdomen houses dozens of parasitic organisms that can be expelled during combat to overwhelm survivors. Its skin secretes a caustic fluid that damages weapons and protective gear on contact, while pulsating growth nodes across its body continuously regenerate damaged tissue when not directly attacked."
    },
    "amphibious_terror": {
        "name": "Amphibious Terror",
        "health": 280,
        "damage": 35,
        "speed": 1.7,
        "special_ability": "ambush_predator",
        "animal_origin": True,
        "water_advantage": True,
        "special_moves": ["dive_attack", "death_roll", "tail_sweep"],
        "location_specific": "zoo",
        "weakness": "fire",
        "description": "A monstrously mutated crocodilian experiment that escaped containment during the initial outbreak. Its scaled hide has fused with the infection to create armored plates capable of deflecting small arms fire, while its massively elongated jaw can snap with enough force to shear through metal. The creature is terrifyingly fast in water and can remain submerged for hours before ambushing unsuspecting survivors. Its only weakness is an aversion to fire, which can temporarily drive it back into deeper waters."
    },
    "hazmat_controller": {
        "name": "Hazmat Controller",
        "health": 180,
        "damage": 25,
        "speed": 1.3,
        "special_ability": "radiation_manipulation",
        "military_origin": True,
        "special_moves": ["radiation_pulse", "contaminate_area", "energy_shield"],
        "location_specific": "research_station",
        "description": "A former containment specialist transformed by exposure to both the infection and experimental radiation. Still clad in the tattered remains of a hazmat suit fused to its mutated flesh, the Controller can manipulate radiation fields to create defensive barriers and offensive bursts of energy. Its presence causes electronics to malfunction and creates lingering zones of contamination that slowly drain the health of anyone passing through them."
    }
}

LOCATIONS = {
    "camp": {
        "name": "Survivor Camp",
        "description": "Your fortified sanctuary surrounded by reinforced barricades and watchtowers. The only place where you can truly rest without fear of the undead. The faint glow of campfires creates an illusion of normalcy amidst the apocalypse.",
        "danger_level": 0,
        "resource_types": ["food", "medical"],
        "sleep_safety": 1.0,  # 100% safe if barricades intact
        "special_areas": ["trading_post", "medical_tent", "community_garden", "barracks", "workshop", "command_center", "kitchen", "training_area", "lookout_tower"],
        "special_items": ["medicine", "tools", "seeds", "trading_goods", "survivor_maps"],
        "special_item_chance": 0.15,  # 15% chance to find special items
        "encounter_chance": 0.2,  # 20% chance of random encounters (even in camp)
        "survivor_encounter_chance": 0.7,  # 70% chance to encounter human survivors
        "animal_types": ["dog", "cat", "chicken", "farm_animal"],  # Domesticated animals
        "friendly_animals": True,  # Animals here are generally friendly
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
        "sleep_safety": 0.3  # 30% safe for sleeping
    },
    "military_base": {
        "name": "Fort Defiance Military Base",
        "description": "A sprawling compound of concrete and steel, this former military installation was one of the last holdouts against the infection. High walls and watchtowers surround barracks, armories, and command centers now silent except for the shuffling of infected soldiers still in uniform. Military-grade weapons and supplies remain, guarded by the base's automated security systems and the dangerous remnants of elite combat units that succumbed to the virus.",
        "danger_level": 5,
        "resource_types": ["weapons", "military_gear", "food", "fuel"],
        "sleep_safety": 0.2,  # 20% safe for sleeping
        "special_areas": ["armory", "vehicle_depot", "command_center", "barracks", "research_lab", "training_grounds", "prison_block", "helipad", "communications_center", "medical_wing"],
        "special_items": ["rpg_launcher", "ak47", "sniper_rifle", "lmg", "military_helmet", "riot_shield", "body_armor", "night_vision", "tactical_crossbow", "flamethrower"],
        "special_item_chance": 0.25,  # 25% chance to find special items
        "zombie_types": ["military", "hazmat", "screamer", "behemoth"],
        "encounter_chance": 0.6,  # 60% chance of random encounters
        "survivor_encounter_chance": 0.3  # 30% chance to encounter human survivors
    },
    "zoo": {
        "name": "Oakridge Wildlife Park",
        "description": "Once a place of family entertainment and conservation, Oakridge Wildlife Park has become a twisted ecosystem of infected wildlife. Broken enclosures and torn fences have allowed the more resilient exotic animals to roam freely, creating bizarre territories within the overgrown park. The gift shops and food stands offer unusual supplies, while the veterinary facilities contain specialized medical items. But beware—the zoo's residents have been transformed by the infection into grotesque versions of their former selves.",
        "danger_level": 4,
        "resource_types": ["food", "medical", "exotic_materials"],
        "sleep_safety": 0.3,  # 30% safe for sleeping
        "special_areas": ["big_cat_enclosure", "reptile_house", "aviary", "primate_sanctuary", "aquarium", "safari_zone", "veterinary_clinic", "storage_warehouse"],
        "special_items": ["tranquilizer_gun", "animal_medicine", "exotic_meat", "leather_hides", "snake_venom", "zookeeper_keys", "feeding_charts", "animal_tracking_gear"],
        "special_item_chance": 0.3,  # 30% chance to find special items
        "zombie_types": ["crawler", "stalker", "screamer"],
        "encounter_chance": 0.7,  # 70% chance of random encounters
        "survivor_encounter_chance": 0.2,  # 20% chance to encounter human survivors
        "animal_encounter_chance": 0.6,  # 60% chance to encounter animals
        "animal_types": ["infected_lion", "infected_tiger", "infected_gorilla", "infected_wolf", "infected_bear", "infected_crocodile", "infected_snake", "infected_baboon"]
    },
    "underground_bunker": {
        "name": "Contingency Bunker X-27",
        "description": "A classified government facility built to house high-ranking officials in case of catastrophe. Buried deep beneath the earth, this self-contained bunker appears to have been breached during the early days of the outbreak. Its hardened concrete walls and reinforced blast doors now contain the infected remnants of the political and military elite who sought refuge here. Advanced technology, weapons, and supplies remain intact in many secured areas, but accessing them requires navigating maze-like corridors patrolled by the infected former occupants.",
        "danger_level": 6,
        "resource_types": ["weapons", "advanced_tech", "medical", "preserved_food", "fuel"],
        "sleep_safety": 0.4,  # 40% safe if you find a secure room
        "special_areas": ["command_center", "living_quarters", "armory", "medical_bay", "communications_hub", "research_lab", "power_plant", "water_treatment", "food_storage", "security_office"],
        "special_items": ["hazmat_suit", "government_files", "advanced_weapons", "experimental_drugs", "radiation_detector", "security_keycard", "emergency_beacon", "night_vision", "gas_mask", "survival_cache_coordinates"],
        "special_item_chance": 0.35,  # 35% chance to find special items
        "zombie_types": ["military", "hazmat", "scientist", "crawler", "screamer"],
        "encounter_chance": 0.5,  # 50% chance of random encounters
        "survivor_encounter_chance": 0.1,  # 10% chance to encounter human survivors
        "requires_special_item": "bunker_coordinates",  # Need to find this item first to access this location
        "oxygen_limited": True,  # Some areas have ventilation issues
        "radiation_zones": True  # Some areas have radiation contamination
    },
    "mall": {
        "name": "Westfield Shopping Center",
        "description": "Once a temple of consumerism, this massive shopping complex now stands as a labyrinth of looted stores and abandoned dreams. The multi-level structure creates a challenging environment of tight corridors, open atriums, and countless hiding places. Improvised barricades suggest various survivor groups attempted to make stands here in the past. Glass skylights create patches of sunlight amid the darkness, while burst water pipes have created small indoor ponds and streams. Department stores still contain valuable supplies, but navigating the complex's confusing layout presents its own dangers.",
        "danger_level": 3,
        "resource_types": ["food", "clothing", "weapons", "materials", "medical"],
        "sleep_safety": 0.5,  # 50% safe for sleeping if secured
        "special_areas": ["food_court", "department_store", "sporting_goods", "pharmacy", "electronics_store", "hardware_store", "security_office", "management_suite", "loading_dock", "parking_garage", "cinema", "rooftop"],
        "special_items": ["camping_gear", "kitchen_supplies", "electronics_parts", "tools", "designer_clothes", "sports_equipment", "luxury_items", "first_aid_supplies", "furniture", "books"],
        "special_item_chance": 0.4,  # 40% chance to find special items
        "zombie_types": ["civilian", "crawler", "child", "screamer", "bloated"],
        "encounter_chance": 0.5,  # 50% chance of random encounters
        "survivor_encounter_chance": 0.35  # 35% chance to encounter human survivors
    },
    "research_station": {
        "name": "Polaris Research Station",
        "description": "A remote scientific facility that was conducting classified experiments before the outbreak. The sprawling compound contains several buildings dedicated to different research fields, including virology, weapons development, and experimental medicine. Security measures are still partially active, and the infected within include scientists and military personnel who were stationed here. Evidence suggests some research on the infection itself was taking place here before communications went dark.",
        "danger_level": 6,
        "resource_types": ["advanced_medical", "experimental_weapons", "scientific_data", "hazardous_materials"],
        "sleep_safety": 0.3,  # 30% safe for sleeping if in a secured lab
        "special_areas": ["main_laboratory", "containment_cells", "data_center", "weapons_testing_range", "medical_wing", "dormitories", "greenhouse", "morgue", "security_checkpoint"],
        "special_items": ["experimental_vaccine", "research_notes", "prototype_weapons", "hazmat_suit", "biological_samples", "electronic_keycard", "antidote_formulas", "research_journals"],
        "special_item_chance": 0.35,  # 35% chance to find special items
        "zombie_types": ["scientist", "hazmat", "military", "specimen", "mutant", "feral"],
        "encounter_chance": 0.65,  # 65% chance of random encounters
        "survivor_encounter_chance": 0.15,  # 15% chance to encounter human survivors
        "requires_biohazard_protection": True,  # Areas with active biological contaminants
        "radiation_zones": True  # Some areas have radiation contamination
    },
    "zoo": {
        "name": "Oakridge Wildlife Park",
        "description": "Once a place of family entertainment and conservation, Oakridge Wildlife Park has become a twisted ecosystem of infected wildlife. Broken enclosures and torn fences have allowed the more resilient exotic animals to roam freely, creating bizarre territories within the overgrown park. The gift shops and food stands offer unusual supplies, while the veterinary facilities contain specialized medical items. But beware—the zoo's residents have been transformed by the infection into grotesque versions of their former selves.",
        "danger_level": 4,
        "resource_types": ["food", "medical", "exotic_materials"],
        "sleep_safety": 0.3,  # 30% safe for sleeping
        "special_areas": ["big_cat_enclosure", "reptile_house", "aviary", "primate_sanctuary", "aquarium", "safari_zone", "veterinary_clinic", "storage_warehouse"],
        "special_items": ["tranquilizer_gun", "animal_medicine", "exotic_meat", "leather_hides", "snake_venom", "zookeeper_keys", "feeding_charts", "animal_tracking_gear"],
        "special_item_chance": 0.3,  # 30% chance to find special items
        "zombie_types": ["crawler", "stalker", "screamer"],
        "encounter_chance": 0.7,  # 70% chance of random encounters
        "survivor_encounter_chance": 0.2,  # 20% chance to encounter human survivors
        "animal_encounter_chance": 0.6,  # 60% chance to encounter animals
        "animal_types": ["infected_lion", "infected_tiger", "infected_gorilla", "infected_wolf", "infected_bear", "infected_crocodile", "infected_snake", "infected_baboon"]
    },
    "bunker_complex": {
        "name": "Hawkins Underground Survival Bunker",
        "description": "A massive government-built fallout shelter buried deep beneath the earth, designed to house important officials during nuclear disaster. Several sections have been compromised by flooding or structural failure, but much of the complex remains intact. The limited-access entry points make it relatively defensible, but the confined spaces create deadly choke points when confronted with infected. The lower levels contain a treasure trove of supplies, weapons, and technology.",
        "danger_level": 4,
        "resource_types": ["food", "medical", "weapons", "materials", "fuel"],
        "sleep_safety": 0.6,  # 60% safe for sleeping - very secure
        "zombie_types": ["hazmat", "military", "screamer", "walker"],
        "special_areas": ["command_center", "living_quarters", "hydroponics_lab", "armory", "medical_bay", "communications_room", "power_plant", "flooded_section"],
        "special_items": ["hazmat_suit", "government_documents", "rare_seeds", "advanced_electronics", "military_rations", "radiation_detector"],
        "special_item_chance": 0.3,  # 30% chance to find special items
        "encounter_chance": 0.4,  # 40% chance of random encounters
        "survivor_encounter_chance": 0.5  # 50% chance to encounter human survivors (many took shelter here)
    },
    "mall": {
        "name": "Northridge Shopping Mall",
        "description": "This massive commercial complex once housed over 200 stores across three sprawling floors. Shattered display windows frame mannequins that stand in silent vigil over the chaos that claimed their shoppers. The central plaza's decorative fountain has long dried up, its basin now filled with the remnants of desperate last stands. The food court still reeks of decay, while the endless echoing halls amplify every sound—including the shuffling of undead feet searching for their next meal.",
        "danger_level": 4,
        "resource_types": ["food", "weapons", "materials", "medical"],
        "sleep_safety": 0.3,  # 30% safe for sleeping
        "special_areas": ["food_court", "department_store", "security_office", "clothing_stores", "electronics_shop", "pharmacy", "toy_store", "movie_theater"],
        "special_items": ["portable_generator", "designer_clothes", "security_card", "electronics_parts", "medicine_cache"],
        "special_item_chance": 0.25,  # 25% chance to find special items
        "encounter_chance": 0.5,  # 50% chance of random encounters
        "survivor_encounter_chance": 0.4,  # 40% chance to encounter human survivors
        "animal_types": ["dog", "infected_rat"]  # Some animals found here
    },
    "military": {
        "name": "Fort Hyperion Military Base",
        "description": "The fallen bastion of what was supposed to be humanity's last defense. Heavy-duty fences topped with razor wire failed to contain the outbreak that started within. Armored vehicles sit abandoned in perfect formation, their occupants having joined the ranks of the undead. The weapons depot and medical facility remain largely intact—if you can navigate the hordes of military-grade zombies still wearing the tattered remains of their uniforms. High risk, but potentially the most valuable supplies in the region.",
        "danger_level": 6,  # Extremely dangerous
        "resource_types": ["weapons", "materials", "medical", "food", "military_grade", "vehicle_parts", "fuel"],
        "sleep_safety": 0.15,  # 15% safe for sleeping
        "zombie_types": ["military", "hazmat", "screamer", "tank"],
        "special_areas": ["armory", "vehicle_depot", "command_center", "barracks", "firing_range"],
        "special_items": ["rpg_launcher", "assault_rifle", "military_helmet", "tank_parts", "helicopter_blades", "targeting_system", "body_armor", "night_vision", "humvee_keys", "tank_manual"],
        "special_item_chance": 0.2  # 20% chance to find special items
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
    },
    "research_lab": {
        "name": "Nexus Biomedical Research Facility",
        "description": "A sprawling complex of sterile labs and advanced research chambers where the outbreak may have originated. Pristine white walls are now stained with blood and organic matter, while sophisticated equipment sits abandoned mid-experiment. The facility's remote location and extreme containment protocols kept it operational longer than most places, but eventually succumbed. Security measures make navigation challenging, but potentially rewarding. Specialized infected wearing lab coats and protective gear roam the halls, some exhibiting unique mutations not seen elsewhere. The facility's lower levels remain in partial lockdown, containing both extreme hazards and invaluable research materials.",
        "danger_level": 5,
        "resource_types": ["medical", "chemicals", "electronics", "scientific_equipment", "documents"],
        "sleep_safety": 0.2,  # 20% safe for sleeping
        "special_feature": "may_contain_patient_zero"
    },
    "bunker": {
        "name": "Fallout Survival Bunker",
        "description": "A massive underground complex built by a doomsday prepper collective before the outbreak. Multiple reinforced levels connected by narrow stairwells contain living quarters, storage rooms, and makeshift medical facilities. The bunker's heavy blast doors were compromised early in the outbreak, allowing the infection to spread through the confined spaces with devastating efficiency. The residents' paranoia meant they were well-stocked with survival supplies, weapons, and long-term food stores, much of which remains untouched. Air filtration systems still function on emergency power, creating an eerie background hum throughout the claustrophobic corridors.",
        "danger_level": 4,
        "resource_types": ["food", "weapons", "medical", "ammo", "fuel", "survival_gear"],
        "sleep_safety": 0.4,  # 40% safe for sleeping
        "special_feature": "emergency_power"
    },
    "amusement_park": {
        "name": "Wonderland Amusement Park",
        "description": "Once filled with the sounds of laughter and excitement, this sprawling entertainment complex now stands as a twisted monument to lost joy. Colorful rides sit motionless against the skyline, while concession stands still hold stale treats. The park's mascot characters, now worn and bloodstained costumes inhabited by the infected, wander through abandoned midways in a macabre parody of entertainment. Maintenance areas contain tools and spare parts, while gift shops and restaurants might still hold usable supplies. The park's remote control systems and backup generators could potentially be salvaged for camp upgrades. At night, some rides flicker to life on failing circuits, creating an unsettling carnival atmosphere that attracts the infected from miles around.",
        "danger_level": 3,
        "resource_types": ["food", "materials", "electronics", "tools", "fuel"],
        "sleep_safety": 0.35,  # 35% safe for sleeping
        "special_feature": "working_generators"
    },
    "underground": {
        "name": "Millfield Underground System",
        "description": "A labyrinthine network of maintenance tunnels, storm drains, and abandoned subway lines running beneath the city. Perpetual darkness is broken only by your flashlight beam reflecting off stagnant water and rusted infrastructure. The damp environment has accelerated decay, both of infrastructure and of the infected that wander these passages. Some areas flood periodically, while others contain makeshift shelters established by survivors who sought refuge below ground, only to succumb to the infection or starvation. Municipal storage areas contain tools and materials, while forgotten maintenance caches might hold valuable supplies. The darkness provides excellent concealment, but limited visibility makes detecting threats nearly impossible until they're within arm's reach.",
        "danger_level": 4,
        "resource_types": ["materials", "tools", "electronics", "chemicals", "scrap"],
        "sleep_safety": 0.3,  # 30% safe for sleeping
        "special_feature": "darkness_concealment"
    },
    "military_base": {
        "name": "Fort Defiance Military Base",
        "description": "A sprawling military installation that was one of the last strongholds to fall. Surrounded by reinforced perimeter walls topped with razor wire, the base contains multiple strategic zones. High-value military equipment and supplies remain, but the base is heavily infested with military personnel who turned while still in uniform and combat gear. Defensive measures, some still active, pose additional hazards to unwary scavengers. Those who brave the dangers might find weapons, ammunition, and equipment unavailable anywhere else.",
        "danger_level": 5,
        "resource_types": ["weapons", "ammo", "medical", "electronics", "military_gear"],
        "sleep_safety": 0.1,  # Only 10% safe for sleeping
        "special_feature": "military_equipment",
        "military_zombies": True,
        "sub_locations": {
            "command_center": {
                "name": "Command Center",
                "description": "The nerve center of Fort Defiance, filled with communication equipment, computer terminals, and strategic maps. Security protocols and reinforced infrastructure make this area difficult to access but potentially rich in intelligence and electronic components.",
                "loot_quality": "high",
                "special_zombies": ["military", "tank_commander"]
            },
            "armory": {
                "name": "Armory",
                "description": "A heavily fortified weapons storage facility with reinforced doors and security systems. If you can breach it, military-grade firearms, ammunition, and equipment await. Most of the best supplies were likely evacuated, but many valuable items remain in secured lockers.",
                "loot_quality": "very_high",
                "special_zombies": ["military"]
            },
            "barracks": {
                "name": "Barracks",
                "description": "Living quarters for base personnel, featuring bunk rooms, recreational areas, and personal storage. While less secure than other areas, the barracks contain everyday items, clothing, and occasionally personal weapons or contraband hidden by soldiers.",
                "loot_quality": "medium",
                "special_zombies": ["military", "walker"]
            },
            "vehicle_depot": {
                "name": "Vehicle Depot",
                "description": "A massive garage and maintenance facility for military vehicles. While most operational vehicles were deployed in evacuation efforts, parts, tools, and fuel remain. Some damaged or abandoned vehicles might be salvageable with enough expertise and resources.",
                "loot_quality": "high",
                "special_zombies": ["military", "hazmat"]
            },
            "research_lab": {
                "name": "Research Laboratory",
                "description": "A classified facility where military scientists studied the infection, seeking vaccines or weapons applications. Hazardous materials and experimental equipment fill the space, along with valuable research data. Containment protocols mean this area may house unique infected specimens.",
                "loot_quality": "very_high",
                "special_zombies": ["hazmat", "bloater", "patient_zero"]
            }
        }
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
    },
    "tactical_crossbow": {
        "name": "Tactical Crossbow",
        "type": "weapon",
        "damage": 40,
        "durability": 75,
        "ammo": 0,
        "max_ammo": 1,
        "silent": True,
        "damage_type": "piercing_weapons",
        "retrievable_ammo": 0.7,
        "critical_chance": 0.25,
        "critical_multiplier": 2.0,
        "hazmat_bonus": 3.0,  # Triple damage against hazmat zombies
        "description": "A modern compound crossbow with tactical modifications—fiber optic sights, carbon-fiber limbs, and an integrated quiver. The draw mechanism has been carefully maintained, and the string shows recent replacement with paracord. Its near-silent operation and reusable ammunition make it ideal for stealth operations in infected territory. The high-velocity bolts can pierce protective gear, making it especially effective against hazmat zombies. Its precision allows for targeting weak points with devastating critical hits."
    },
    "crossbow_bolt": {
        "name": "Crossbow Bolt",
        "type": "ammo",
        "count": 5,
        "weight": 0.2,
        "craftable": True,
        "weapon": "tactical_crossbow",
        "crafting_requirements": {
            "metal_scrap": 1,
            "duct_tape": 1,
            "wood": 1
        },
        "description": "Hand-crafted bolts for crossbows, fashioned from straightened metal rods with improvised fletching. The heads are sharpened to brutal points, some even sporting barbs made from scrap metal. Though lacking the uniformity of manufactured arrows, their lethality against the infected is undiminished—at close range, they can penetrate a zombie's skull with ease."
    },
    "nail_bat": {
        "name": "Nail-Spiked Baseball Bat",
        "type": "weapon",
        "damage": 25,
        "durability": 40,
        "damage_type": "blunt_heavy",
        "area_attack": True,
        "special_effect": "splash_damage",
        "crawler_bonus": 2.0,  # Double damage against crawlers
        "description": "A baseball bat transformed into something far more sinister—dozens of nails driven through the barrel create a porcupine-like implement of destruction. The wood is stained with dark patches of dried blood and gore. While crude, it's brutally effective at causing traumatic injuries to the infected, though the nails occasionally catch on bone and clothing, making follow-up swings slower. Particularly effective against crawlers and can hit multiple targets with a wide swing."
    },
    "machete": {
        "name": "Machete",
        "type": "weapon",
        "damage": 22,
        "durability": 70,
        "damage_type": "slashing",
        "bloater_bonus": 2.5,  # Extra effective against bloater zombies
        "dismemberment_chance": 0.35,  # 35% chance to dismember limbs
        "decapitation_chance": 0.15,  # 15% chance for instant kills via decapitation
        "sweep_attack": True,  # Can hit multiple targets with a single swing
        "description": "A heavy-bladed cutting tool with a worn black handle wrapped in electrical tape for grip. The blade shows signs of frequent sharpening, with a serrated section near the handle for sawing. Originally designed for clearing vegetation, it has found a new purpose in the apocalypse as an efficient means of separating zombie heads from shoulders with minimal effort and noise. The blade can sweep through multiple targets and is particularly effective at puncturing bloated infected, releasing the pressure before they can explode."
    },
    "riot_shield": {
        "name": "Riot Shield",
        "type": "weapon",
        "damage": 5,
        "durability": 150,
        "defense_bonus": 15,
        "damage_type": "blunt_shield",
        "defense_type": "physical_barrier",
        "bloater_protection": True,  # Protects against bloater explosions
        "screamer_protection": True,  # Reduces impact of screamer sonic attacks
        "push_back_chance": 0.8,  # 80% chance to push zombies back
        "explosion_damage_reduction": 0.75,  # Reduces explosion damage by 75%
        "description": "A transparent polycarbonate shield looted from a police station or military checkpoint. Though scraped and dented from impacts, it remains sturdy enough to create a defensive barrier between you and the infected. The shield is particularly effective at blocking acidic spray from bloaters, deflecting sonic attacks from screamers, and creating distance with a powerful push. Most effective in narrow spaces where it can control the flow of approaching zombies."
    },
    "hazmat_piercer": {
        "name": "Hazmat Piercer",
        "type": "weapon",
        "damage": 18,
        "durability": 60,
        "hazmat_damage_bonus": 25,
        "description": "A specialized weapon designed for penetrating hazmat suits and protective gear. Essentially an ice pick with an elongated, reinforced shaft and ergonomic grip, it can punch through the reinforced fabric and plastic of hazmat suits to reach the infected inside. Particularly effective against hazmat zombies, though less impressive against standard infected."
    },
    "flamethrower": {
        "name": "Improvised Flamethrower",
        "type": "weapon",
        "damage": 35,
        "durability": 30,
        "ammo": 0,
        "max_ammo": 10,
        "area_effect": True,
        "damage_type": "fire",
        "fire_damage": 10,
        "bloater_bonus": 3.0,  # Triple damage against bloaters due to gas ignition
        "area_damage_percent": 0.7,  # 70% of primary damage applies to nearby zombies
        "continuous_damage": 5,  # Zombies continue to take damage for 2 turns after being hit
        "continuous_turns": 2,
        "horde_control": True,  # Creates a temporary barrier of flames
        "attraction_radius": 3,  # Attracts zombies from 3 zones away
        "crawler_bonus": 1.5,  # Extra effective against crawlers
        "screamer_panic": True,  # Causes screamers to panic and flee
        "description": "A jury-rigged contraption consisting of a pressurized tank, pump mechanism, and ignition system. Though dangerous to the user and limited in capacity, it creates a devastating cone of flame that can incinerate multiple infected at once. Particularly devastating against bloaters whose gas ignites explosively, and effective at creating a wall of flame that temporarily blocks zombie movements. The bright flame and distinct roar will draw every zombie for miles, but sometimes a tactical retreat requires scorching the earth behind you."
    },
    "fuel_canister": {
        "name": "Fuel Canister",
        "type": "ammo",
        "count": 2,
        "weight": 3.0,
        "craftable": True,
        "weapon": "flamethrower",
        "crafting_requirements": {
            "fuel": 3,
            "alcohol": 1,
            "duct_tape": 1
        },
        "description": "A pressurized canister filled with a volatile mixture of scavenged fuels, oils, and alcohols. The resulting concoction burns with an intense, sticky flame ideal for anti-infected operations. Each canister provides enough fuel for several bursts from an improvised flamethrower, though the inconsistent mixture sometimes leads to clogs or unexpected flare-ups."
    },
    "sonic_disruptor": {
        "name": "Sonic Disruptor",
        "type": "weapon",
        "damage": 10,
        "durability": 40,
        "ammo": 0,
        "max_ammo": 5,
        "screamer_damage_bonus": 30,
        "stun_effect": True,
        "description": "A modified audio device that generates targeted high-frequency sound waves. Originally equipment from a research facility studying zombie behavior, it has minimal effect on most infected but proves devastating against screamers and other noise-sensitive mutations. The device emits a barely audible high-pitched whine when powered, with lights indicating its charged status."
    },
    "tactical_crossbow": {
        "name": "Tactical Crossbow",
        "type": "weapon",
        "damage": 45,
        "durability": 80,
        "ammo": 0,
        "max_ammo": 1,
        "silent": True,
        "critical_hit_chance": 0.25,
        "hazmat_penetration": 0.85,
        "description": "A modern, military-grade crossbow with carbon-fiber frame and integrated sighting system. Offers exceptional penetration against armored targets like hazmat zombies, and its silent operation makes it perfect for stealth approaches. Each bolt can be retrieved from defeated enemies, making this a highly sustainable option for the resourceful survivor."
    },
    "m4_carbine": {
        "name": "M4 Carbine",
        "type": "weapon",
        "damage": 40,
        "durability": 120,
        "ammo": 0,
        "max_ammo": 30,
        "military_origin": True,
        "burst_fire": True,
        "description": "Standard issue military assault rifle with select-fire capability. This weapon features a modular design with rails for attachments, offering excellent reliability and firepower. Its lightweight design allows for quick target acquisition and handling, while the burst fire mode conserves ammunition against multiple threats. Extremely effective but the noise attracts significant zombie attention."
    },
    "riot_shield": {
        "name": "Tactical Riot Shield",
        "type": "weapon",
        "damage": 15,
        "durability": 150,
        "defense_bonus": 25,
        "block_chance": 0.35,
        "military_origin": True,
        "description": "A heavy-duty polycarbonate shield used by military and law enforcement for riot control. Provides substantial protection against zombie attacks, allowing for defensive combat strategies. The shield's transparent design gives full visibility while maintaining protection, and its reinforced edges can be used to push back or stun attackers."
    },
    "flamethrower": {
        "name": "M9 Flamethrower",
        "type": "weapon",
        "damage": 35,
        "area_damage": True,
        "durability": 40,
        "ammo": 0,
        "max_ammo": 100,
        "military_origin": True,
        "bloater_damage_bonus": 50,
        "crawler_damage_bonus": 40,
        "description": "Military-grade incendiary weapon that projects a stream of flammable liquid. Particularly effective against groups of zombies and special types like bloaters and crawlers. The intense heat can neutralize multiple threats at once, creating temporary barriers of flame. Requires fuel canisters to operate and makes stealth impossible, but few weapons match its area-denial capabilities."
    },
    "machete": {
        "name": "Military Combat Machete",
        "type": "weapon",
        "damage": 35,
        "durability": 100,
        "bloater_damage_bonus": 30,
        "dismemberment_chance": 0.3,
        "military_origin": True,
        "description": "High-carbon steel machete with tactical grip, originally designed for jungle warfare. The weighted blade provides exceptional cutting power against bloaters and can potentially dismember limbs from other zombie types. Silent, reliable, and never needs reloading, making it an excellent backup weapon or primary for stealthy approaches."
    },
    "battery_pack": {
        "name": "High-Capacity Battery Pack",
        "type": "ammo",
        "count": 1,
        "weight": 1.0,
        "craftable": True,
        "weapon": "sonic_disruptor",
        "crafting_requirements": {
            "electronics": 2,
            "metal_scrap": 1,
            "wire": 2
        },
        "description": "A cobbled-together power source for electronic devices, combining salvaged batteries with rudimentary charging circuits. The exposed wiring and jury-rigged connections look precarious, but the pack delivers a stable current when needed. The clear plastic casing reveals the mess of components inside, some still bearing labels from consumer electronics."
    },
    "carbon_fiber_bolts": {
        "name": "Carbon-Fiber Tactical Bolts",
        "type": "ammo",
        "count": 5,
        "weight": 0.5,
        "craftable": True,
        "weapon": "tactical_crossbow",
        "hazmat_penetration_bonus": 0.15,
        "crafting_requirements": {
            "metal_scrap": 1,
            "wood": 1,
            "duct_tape": 1
        },
        "description": "Military-grade crossbow bolts with carbon-fiber shafts and hardened steel tips. The streamlined design provides excellent penetration against armored targets like hazmat zombies. Each bolt is balanced for accuracy and features a retrievable design that allows them to be recovered from defeated enemies with minimal damage."
    },
    "5.56mm_rounds": {
        "name": "5.56mm NATO Rounds",
        "type": "ammo",
        "count": 30,
        "weight": 0.8,
        "weapon": "m4_carbine",
        "military_origin": True,
        "description": "Standard military-issue 5.56×45mm NATO rounds in a box. These bullets are designed for use with the M4 Carbine and similar assault rifles. Each cartridge features a full metal jacket over a lead core, providing excellent terminal ballistics against both soft and moderately armored targets. The military-grade manufacturing ensures reliable feeding and firing even in adverse conditions."
    },
    "fuel_canister_military": {
        "name": "Military-Grade Fuel Canister",
        "type": "ammo",
        "count": 100,
        "weight": 5.0,
        "weapon": "flamethrower",
        "military_origin": True,
        "area_damage_bonus": 0.2,
        "description": "A pressurized military-grade canister containing a specialized napalm-based fuel mixture. This formulation burns hotter and more consistently than civilian alternatives, with additives to increase adhesion to targets. The built-in pressure regulation system ensures constant flow rate even as the canister empties, providing reliable performance throughout combat operations."
    }
}

ZOMBIE_TYPES = {
    "screamer": {
        "name": "Screamer",
        "health": 25,
        "damage": 8,
        "speed": 1.5,
        "sound_detection": 2.5,
        "can_attract": True,
        "description": "A zombie with a grotesquely deformed jaw and throat that emits piercing screams to attract other infected. While not particularly strong, its ability to call hordes makes it a priority target. Extremely sensitive to sonic weapons."
    },
    "hazmat": {
        "name": "Hazmat Zombie",
        "health": 40,
        "damage": 12,
        "speed": 0.9,
        "armor": 0.3,
        "weakness": "piercing",
        "description": "Formerly a hazardous materials worker or military personnel, this zombie is partially protected by remnants of a hazmat suit. The degraded protective gear provides partial immunity to blunt and slashing weapons, but is vulnerable to piercing attacks like crossbow bolts."
    },
    "crawler": {
        "name": "Crawler",
        "health": 15,
        "damage": 8,
        "speed": 0.7,
        "stealth": 0.8,
        "prone_attack": True,
        "description": "A zombie with damaged or missing legs that crawls along the ground. Often overlooked until it's too late, crawlers can attack from unexpected angles and are particularly vulnerable to area-effect weapons like flamethrowers."
    },
    "bloater": {
        "name": "Bloater",
        "health": 60,
        "damage": 15,
        "speed": 0.6,
        "toxic_burst": True,
        "weakness": "blades",
        "description": "A grotesquely swollen infected filled with toxic gases and fluids. Slow-moving but dangerous in close quarters, bloaters explode when killed with ballistic weapons, releasing a cloud of toxic gas. Blade weapons like machetes can dispatch them safely by releasing pressure gradually."
    },
    "military": {
        "name": "Military Zombie",
        "health": 45,
        "damage": 14,
        "speed": 1.2,
        "armor": 0.25,
        "tactical": True,
        "description": "Formerly military personnel infected while in combat gear. Partial body armor provides protection, and residual combat training manifests in more coordinated attacks. These zombies often appear in groups and exhibit rudimentary tactical behavior."
    },
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
    "scientist": {
        "name": "Researcher Zombie",
        "health": 35,
        "damage": 10,
        "speed": 1.3,
        "intelligence": 0.7,
        "special_ability": "chemical_spray",
        "weakness": "fire",
        "location_specific": "research_station",
        "description": "Formerly a scientist at Polaris Research Station, these infected still wear tattered lab coats and occasionally carry chemical compounds that splatter when attacked. Their exposure to experimental treatments before turning has given them limited problem-solving abilities, allowing them to operate simple equipment and navigate obstacles more effectively than typical infected."
    },
    "specimen": {
        "name": "Failed Test Subject",
        "health": 60,
        "damage": 18,
        "speed": 1.4,
        "regeneration": True,
        "mutation_chance": 0.3,
        "weakness": "electricity",
        "location_specific": "research_station",
        "description": "Human test subjects who were administered experimental treatments before the outbreak. Their bodies show signs of bizarre mutations, with transparent patches of skin revealing pulsing organs and bone structures. They can rapidly regenerate tissue damage and occasionally manifest unpredictable mutations mid-combat that grant new offensive capabilities."
    },
    "feral": {
        "name": "Feral Zombie",
        "health": 40,
        "damage": 22,
        "speed": 2.0,
        "stealth": 0.5,
        "pounce_attack": True,
        "location_specific": "zoo",
        "description": "These infected have adopted animalistic behavior patterns after the outbreak, moving on all fours with unnaturally bent limbs. They emit guttural growls instead of moans and prefer to ambush prey from elevated positions or dense vegetation. Their attacks are lightning-fast and brutally savage, with preference for throat and limb targeting."
    },
    "zookeeper": {
        "name": "Infected Zookeeper",
        "health": 45,
        "damage": 14,
        "speed": 1.1,
        "animal_control": True,
        "special_ability": "summon_infected_animals",
        "location_specific": "zoo",
        "description": "Former animal handlers still wearing torn uniform fragments and carrying tools of their trade. These specialized infected can somehow influence the behavior of infected animals, directing their attacks with primitive signals. When threatened, they can emit specific calls that summon nearby infected animals to their defense."
    },
    "screamer": {
        "name": "Screamer",
        "health": 35,
        "damage": 12,
        "speed": 2,
        "special_ability": "call_horde",
        "description": "Emits ear-piercing screams that can attract more zombies. Vulnerable to sonic weapons."
    },
    "hazmat": {
        "name": "Hazmat Zombie",
        "health": 50,
        "damage": 20,
        "speed": 1,
        "special_ability": "toxic_cloud",
        "special_resistance": "toxic",
        "weakness": "penetration",
        "description": "Former CDC workers in damaged hazmat suits. Leaks toxic fumes when damaged and is immune to chemical attacks. Vulnerable to piercing weapons that breach the suit."
    },
    "crawler": {
        "name": "Crawler",
        "health": 15,
        "damage": 8,
        "speed": 2,
        "special_ability": "hard_to_hit",
        "description": "Missing lower limbs, these zombies crawl along the ground and are difficult to hit. Often attack in groups."
    },
    "bloater": {
        "name": "Bloater",
        "health": 60,
        "damage": 18,
        "speed": 1,
        "special_ability": "explode",
        "weakness": "blades",
        "description": "Swollen with gases and toxic fluids. Explodes when killed, causing splash damage. Vulnerable to bladed weapons."
    },
    "military": {
        "name": "Military Zombie",
        "health": 55,
        "damage": 20,
        "speed": 2,
        "special_ability": "armored",
        "description": "Former soldiers wearing damaged body armor. More resistant to attacks but vulnerable to armor-piercing rounds."
    },
    "stalker": {
        "name": "Forest Stalker",
        "health": 35,
        "damage": 20,
        "speed": 2,
        "stealth": 3,
        "description": "Camouflaged zombie that lurks in wooded areas. Hard to spot until it's too late."
    },
    "banshee": {
        "name": "Banshee",
        "health": 30,
        "damage": 12,
        "speed": 2,
        "special_ability": "call_horde",
        "description": "Emits piercing screams that can attract more zombies to your location. Kill it quickly!"
    },
    "screamer": {
        "name": "Screamer",
        "health": 25,
        "damage": 8,
        "speed": 3,
        "special_ability": "sonic_attack",
        "weakness": "sonic_weapons",
        "description": "A zombie with deformed vocal cords that can emit high-pitched sonic attacks capable of disorienting humans. Their heightened sensitivity to sound makes them vulnerable to sonic weapons. Often found in packs, coordinating with each other through sound."
    },
    "hazmat": {
        "name": "Hazmat Zombie",
        "health": 50,
        "damage": 15,
        "speed": 1,
        "armor": 15,
        "weakness": "piercing_weapons",
        "special_ability": "toxic_cloud",
        "description": "Former hazardous materials worker still wearing fully intact protective gear. The suit protects it from conventional attacks, but is vulnerable to piercing weapons that can breach the suit. Releases toxic gas when damaged, causing ongoing damage to survivors in the vicinity."
    },
    "crawler": {
        "name": "Crawler",
        "health": 15,
        "damage": 20,
        "speed": 1,
        "stealth": 5,
        "special_ability": "sudden_lunge",
        "description": "Missing its legs but incredibly dangerous. Their low profile makes them extremely difficult to spot in tall grass or debris. They can suddenly lunge at victims with surprising range, using their abnormally strong arms to drag survivors down before ripping into them with savage bites. Their unusual movement pattern can confuse standard combat tactics."
    },
    "bloater": {
        "name": "Bloater",
        "health": 65,
        "damage": 25,
        "speed": 1,
        "special_ability": "toxic_explosion",
        "weakness": "fire_weapons",
        "description": "Grotesquely swollen with toxic gases produced by advanced decomposition. Their distended bodies are filled with corrosive fluids and explosive gases. When severely damaged, they rupture violently, releasing a cloud of toxic gas and acidic fluids that can damage equipment and cause ongoing injuries. Their unstable biology makes them especially vulnerable to fire weapons, which can cause them to detonate prematurely."
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
    "banshee": {
        "name": "Banshee",
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
        "health": 350,
        "damage": 40,
        "speed": 1,
        "armor": 8,
        "is_boss": True,
        "special_ability": "ground_pound",
        "description": "A colossal zombie that towers over others. Its massive fists can create shockwaves when slammed into the ground."
    },
    "infected_scientist": {
        "name": "Patient Zero",
        "health": 180,
        "damage": 25,
        "speed": 2,
        "is_boss": True,
        "special_ability": "mutation",
        "description": "One of the original scientists infected by the Necroa_A virus. Can rapidly adapt during combat, changing its attack patterns."
    },
    "titan": {
        "name": "Titan",
        "health": 300,
        "damage": 40,
        "speed": 1,
        "is_boss": True,
        "special_ability": "rage",
        "description": "A colossal zombie that gets stronger as it takes damage. The final challenge for any survivor."
    },
    "behemoth": {
        "name": "Behemoth",
        "health": 350,
        "damage": 45,
        "speed": 1,
        "armor": 15,
        "is_boss": True,
        "special_ability": "charge_attack",
        "weakness": "explosives",
        "description": "A monstrous zombie of unprecedented size, standing over twelve feet tall with massively overdeveloped musculature. Its thick hide is resistant to most conventional weapons, though explosive weapons can penetrate its defenses. The Behemoth can unleash devastating charge attacks that can shatter barricades and walls. Survivors report seeing these rare mutations demolish entire survivor compounds single-handedly."
    },
    "infected_scientist": {
        "name": "Patient Zero",
        "health": 200,
        "damage": 25,
        "speed": 3,
        "is_boss": True,
        "special_ability": "mutation_cloud",
        "weakness": "fire_weapons",
        "description": "A uniquely intelligent infected wearing the tattered remains of a laboratory coat. Unlike other zombies, this one displays tactical intelligence and can coordinate attacks. It can release spores that temporarily mutate nearby zombies, enhancing their abilities. Research notes suggest this may be one of the original test subjects from the facility where the outbreak began. Its brain appears partially intact, making it significantly more dangerous than typical infected."
    }
}

# Define infected animals for the game
INFECTED_ANIMALS = {
    # Canine Variants
    "infected_wolf": {
        "name": "Infected Wolf",
        "health": 120,
        "damage": 25,
        "speed": 1.7,
        "animal": True,
        "pack_hunter": True,
        "description": "Once a proud predator, now twisted by the infection into something far more vicious. The wolf's fur has fallen out in patches, revealing lesions and exposed muscle. Its eyes glow with an unnatural yellow-green hue, and saliva constantly drips from elongated fangs. These creatures maintain their pack hunting instincts but have lost all fear, making them relentlessly aggressive."
    },
    "infected_dog": {
        "name": "Infected Guard Dog",
        "health": 100,
        "damage": 22,
        "speed": 1.8,
        "animal": True,
        "tracking": True,
        "description": "Once someone's loyal pet or guard dog, now corrupted beyond recognition. Unlike wolves, these former domesticated animals still remember their training and will actively hunt humans with terrifying focus. Their skin has split in numerous places, revealing pulsating muscle tissue beneath, and they emit a guttural growl that sounds almost mechanical."
    },
    "infected_coyote": {
        "name": "Infected Coyote Pack",
        "health": 90,
        "damage": 18,
        "speed": 2.0,
        "animal": True,
        "pack_hunter": True,
        "climber": True,
        "description": "Formerly shy and cautious creatures, infected coyotes have become bold pack hunters that coordinate attacks with disturbing intelligence. Their bones have elongated, giving them an unnatural, skeletal appearance, and their jaws have developed to bite through protective gear. They make unsettling, almost human-like vocalizations to communicate with pack members."
    },
    
    # Ursine Variants
    "infected_bear": {
        "name": "Infected Grizzly",
        "health": 200,
        "damage": 40,
        "speed": 1.1,
        "animal": True,
        "armored": True,
        "description": "A massive bear corrupted by the infection, standing nearly ten feet tall when on its hind legs. The infection has caused tumorous growths along its back and shoulders, forming natural armor plates. Its claws have grown to extraordinary length, capable of tearing through metal with frightening ease. What remains of its fur is matted with dried blood and pus from weeping sores."
    },
    "infected_black_bear": {
        "name": "Infected Black Bear",
        "health": 150,
        "damage": 35,
        "speed": 1.3,
        "animal": True,
        "climber": True,
        "description": "Smaller than its grizzly cousin but far more agile, the infected black bear can climb surfaces that should be impossible for a creature its size. The infection has caused its jaw to split vertically, creating a four-part mouth lined with razor-sharp teeth. Its heightened metabolism means it must constantly feed, making it relentlessly pursue any potential food source."
    },
    
    # Feline Variants
    "infected_lion": {
        "name": "Infected Lion",
        "health": 170,
        "damage": 35,
        "speed": 1.5,
        "animal": True,
        "ambush": True,
        "description": "This once-magnificent big cat now resembles a nightmare, with patchy fur and exposed ribs visible through necrotic flesh. The infection has enhanced its already formidable hunting abilities, allowing it to stalk prey with uncanny patience before lunging with explosive speed. Unlike normal lions, these infected cats hunt alone and target humans preferentially."
    },
    "infected_tiger": {
        "name": "Infected Tiger",
        "health": 180,
        "damage": 40,
        "speed": 1.6,
        "animal": True,
        "ambush": True,
        "swimming": True,
        "description": "Formerly a Siberian tiger, this enormous feline predator has been grotesquely transformed by the infection. Its distinctive stripes are still visible on patches of remaining fur, but much of its skin is exposed and covered in pulsating veins. The tiger retains its hunting prowess and stealth, but now displays an intelligence that borders on cunning when stalking human prey."
    },
    "infected_mountain_lion": {
        "name": "Infected Cougar",
        "health": 140,
        "damage": 30,
        "speed": 1.9,
        "animal": True,
        "ambush": True,
        "climber": True,
        "description": "The North American cougar was already a formidable predator before infection; now it's become something truly nightmarish. Its limbs have elongated unnaturally, allowing for incredible leaping distances, and its skull has partially collapsed, giving it a demonic appearance. It has developed the ability to mimic human cries for help to lure in potential prey."
    },
    "infected_bobcat": {
        "name": "Infected Bobcat",
        "health": 100,
        "damage": 25,
        "speed": 2.0,
        "animal": True,
        "stealth": True,
        "ambush": True,
        "description": "Though smaller than other big cats, the infected bobcat is possibly more dangerous due to its enhanced agility and near-perfect camouflage. The infection has caused its fur to develop chameleon-like properties, and it can remain perfectly still for days waiting for prey. Its legs have developed insect-like jointing, allowing it to move in ways that appear fundamentally wrong."
    },
    
    # Primates
    "infected_gorilla": {
        "name": "Infected Silverback",
        "health": 250,
        "damage": 45,
        "speed": 1.2,
        "animal": True,
        "armored": True,
        "climber": True,
        "description": "A nightmarish evolution of what was once a powerful silverback gorilla. The infection has increased its muscle mass to grotesque proportions, with arms capable of tearing humans apart with minimal effort. Its face is barely recognizable, with most of the skin torn away to reveal a permanent grimace of exposed teeth and gums. Unlike regular gorillas, the infected version is territorial and aggressively hunts humans."
    },
    "infected_baboon": {
        "name": "Infected Baboon Troop",
        "health": 120,
        "damage": 20,
        "speed": 1.6,
        "animal": True,
        "pack_hunter": True,
        "climber": True,
        "description": "Perhaps the most disturbing of the infected animals due to their uncanny resemblance to humans. Baboons were already aggressive and territorial; the infection has made them hyper-violent and pack-oriented. Their faces have split open to reveal rows of needle-like teeth, and they've developed a rudimentary ability to use simple tools and weapons."
    },
    
    # Reptiles
    "infected_crocodile": {
        "name": "Infected Crocodile",
        "health": 160,
        "damage": 50,
        "speed": 0.6,
        "swimming_speed": 1.8,
        "animal": True,
        "ambush": True,
        "swimming": True,
        "description": "An already prehistoric predator made even more terrifying by the infection. Its scaled hide has split in places to reveal bulging musculature and throbbing organs. The crocodile's jaw has expanded beyond normal proportions, allowing it to crush even reinforced materials with ease. Most dangerous in water, but capable of surprising bursts of speed on land when pursuing prey."
    },
    "infected_snake": {
        "name": "Infected Python",
        "health": 130,
        "damage": 30,
        "speed": 1.3,
        "animal": True,
        "stealth": True,
        "ambush": True,
        "description": "This massive constrictor has grown to unnatural proportions due to the infection. Its scales have fused into armor-like plates in some areas, while other parts of its body have split open to reveal pulsating internal organs. Most disturbing is its newfound ability to regurgitate and weaponize its highly corrosive digestive acids against threats."
    },
    
    # Small mammals
    "infected_rat": {
        "name": "Infected Rat Swarm",
        "health": 100,
        "damage": 15,
        "speed": 1.4,
        "animal": True,
        "swarm": True,
        "climber": True,
        "description": "Individually weak but overwhelming in numbers, infected rats move as a coordinated horde. Each rat's eyes glow with an unnatural green luminescence, and their bodies are covered in weeping sores. They can squeeze through incredibly small openings and are capable of stripping flesh to bone in minutes. The swarm seems to share a hive mind, reacting instantaneously to threats and opportunities."
    },
    "infected_fox": {
        "name": "Infected Fox",
        "health": 75,
        "damage": 20,
        "speed": 2.2,
        "animal": True,
        "stealth": True,
        "night_hunter": True,
        "description": "Once known for their cunning, infected foxes have become something far more sinister. The infection has caused their limbs to elongate unnaturally, and their already sharp senses have become preternaturally acute. Their distinctive calls have transformed into a sound that resembles eerie human laughter, which they use to disorient and terrify prey before attacking."
    },
    
    # Birds
    "infected_hawk": {
        "name": "Infected Hawk",
        "health": 60,
        "damage": 25,
        "speed": 2.5,
        "animal": True,
        "flying": True,
        "ambush": True,
        "description": "A once-majestic raptor transformed into an aerial nightmare. Its wingspan has nearly doubled, and its talons have developed barbed tips that make them difficult to dislodge from flesh. Most disturbing is its hunting method - it shrieks at frequencies that cause disorientation and nausea in humans before diving at incredible speeds to strike vulnerable areas like the eyes and throat."
    },
    "infected_vulture": {
        "name": "Infected Vulture Flock",
        "health": 80,
        "damage": 15,
        "speed": 2.0,
        "animal": True,
        "flying": True,
        "swarm": True,
        "description": "Once nature's clean-up crew, infected vultures have become active hunters. Their heads have become almost entirely skeletal, and their wings have developed bat-like membrane extensions. They hunt in organized flocks, using coordinated diving attacks to overwhelm prey. Most disturbing is their affinity for human eyes, which they target with surgical precision."
    },
    
    # Aquatic
    "infected_shark": {
        "name": "Infected Bull Shark",
        "health": 180,
        "damage": 45,
        "speed": 0.5,
        "swimming_speed": 2.0,
        "animal": True,
        "swimming": True,
        "ambush": True,
        "description": "The bullshark was already one of few sharks that could venture into freshwater; the infection has enhanced this ability, allowing it to survive in virtually any water source. Its skin has developed bioluminescent patches that pulse hypnotically, and its multiple rows of teeth have fused into serrated bone plates that can shear through metal. Encounters are rare but almost always fatal."
    },
    
    # Infected Hybrid Mutations
    "chimera": {
        "name": "Chimeric Predator",
        "health": 220,
        "damage": 40,
        "speed": 1.5,
        "animal": True,
        "mutation": True,
        "special_attack": "adaptive_strike",
        "description": "A horrifying fusion of multiple infected animals - possibly the result of advanced infection or deliberate experimentation. This creature displays characteristics of wolves, big cats, and reptiles simultaneously, with mismatched limbs and asymmetrical features. It can rapidly adapt its attack strategies based on its prey's weaknesses, making it unpredictably dangerous and able to counter survivor tactics."
    },
    "infected_abomination": {
        "name": "Zoological Abomination",
        "health": 300,
        "damage": 50,
        "speed": 1.0,
        "animal": True,
        "mutation": True,
        "armored": True,
        "regeneration": True,
        "description": "A monstrous entity that defies categorization - likely the result of multiple animals fused together by an advanced form of the infection. Standing nearly 12 feet tall, this nightmarish creature features multiple heads, limbs of different species, and exposed internal organs that pulsate with bioluminescent fluid. Parts of it constantly die and regenerate, making it both revolting and nearly impossible to kill permanently."
    },
    
    # Arctic Region Infected
    "infected_polar_bear": {
        "name": "Infected Polar Titan",
        "health": 280,
        "damage": 55,
        "speed": 1.2,
        "animal": True,
        "armored": True,
        "cold_resistant": True,
        "description": "Once the apex predator of the Arctic, this infected polar bear has grown to incredible proportions. Its white fur is now sparse, revealing bluish skin with protruding ice-like crystalline structures. The infection has adapted to the extreme cold, allowing parts of the bear to actually freeze solid, creating natural armor plates that can withstand significant damage. Its breath crystallizes in the air, creating a fog that obscures its movements."
    },
    "infected_walrus": {
        "name": "Infected Walrus Bull",
        "health": 240,
        "damage": 40,
        "speed": 0.7,
        "swimming_speed": 1.6,
        "animal": True,
        "swimming": True,
        "armored": True,
        "description": "This grotesque creature retains the massive blubber layer of the walrus, but the infection has caused it to harden into a natural armor. Its tusks have grown to absurd proportions, often over six feet long, and have developed serrated edges. The most disturbing feature is its ability to use these tusks to anchor itself to ice or structures, allowing it to pull its massive bulk from water with surprising speed."
    },
    
    # Desert Region Infected
    "infected_camel": {
        "name": "Infected Dromedary",
        "health": 150,
        "damage": 35,
        "speed": 1.7,
        "animal": True,
        "heat_resistant": True,
        "description": "The camel's natural ability to survive harsh desert conditions has been horrifically enhanced by the infection. Its humps have split open, revealing a network of pulsating reservoirs containing a caustic fluid it can projectile vomit at threats. Its hide has hardened into a rough exoskeleton that efficiently reflects heat, while its legs have elongated further, allowing it to cover vast distances without tiring."
    },
    "infected_scorpion": {
        "name": "Infected Emperor Scorpion",
        "health": 90,
        "damage": 40,
        "speed": 1.1,
        "animal": True,
        "venomous": True,
        "stealth": True,
        "description": "Already formidable arachnids, the infection has caused desert scorpions to grow to the size of large dogs. Their exoskeletons have developed additional layers of hardened chitin, and their stingers contain a neurotoxin that causes both extreme pain and hallucinations. These creatures often bury themselves in sand or debris, with only their sensory hairs exposed, waiting for prey to approach."
    },
    
    # Tropical Region Infected
    "infected_alligator": {
        "name": "Mutant Alligator",
        "health": 200,
        "damage": 60,
        "speed": 0.8,
        "swimming_speed": 2.0,
        "animal": True,
        "swimming": True,
        "armored": True,
        "ambush": True,
        "description": "The infection has transformed this massive reptile into a true monster of the swamps. Its hide has developed spike-like protrusions along its back and tail, while its jaw has split into three separate mandibles lined with rotating teeth. Most disturbing is its ability to partially digest and absorb the characteristics of its prey, sometimes developing traits from recent meals that make each encounter unpredictable."
    },
    "infected_anaconda": {
        "name": "Infected Anaconda",
        "health": 170,
        "damage": 45,
        "speed": 1.4,
        "swimming_speed": 1.8,
        "animal": True,
        "swimming": True,
        "constrictor": True,
        "description": "This once-enormous snake has grown to truly terrifying proportions, sometimes exceeding forty feet in length. The infection has caused segmented plates to develop along its length, and its head has split partway down its neck, creating a bifurcated jaw system that can engulf large prey. It retains its constricting ability but has developed acidic secretions that begin breaking down prey even before consumption."
    },
    "infected_jaguar": {
        "name": "Infected Jaguar",
        "health": 160,
        "damage": 40,
        "speed": 2.0,
        "animal": True,
        "ambush": True,
        "climber": True,
        "stealth": True,
        "description": "The already-formidable jungle cat has become a silent nightmare in the tropical forests. Its spotted coat has developed active camouflage abilities that make it nearly invisible when stationary. The infection has enhanced its muscles to the point where it can leap over 50 feet horizontally, and its bite can crack steel. Like other infected felines, it displays disturbing intelligence when stalking human prey."
    },
    
    # Special Mutations
    "behemoth_mammoth": {
        "name": "Behemoth Mammoth",
        "health": 400,
        "damage": 70,
        "speed": 0.9,
        "animal": True,
        "mutation": True,
        "boss": True,
        "armored": True,
        "cold_resistant": True,
        "regeneration": True,
        "description": "A truly prehistoric horror - possibly a zoo elephant transformed beyond recognition or, more disturbingly, a genuine mammoth revived through the infection's mysterious properties. Standing over 18 feet tall, this colossus features multiple tusks growing in spiral patterns and a hide covered in bone-plate protrusions. The creature exudes a freezing aura that slows nearby movements and can project its tusks as javelins that regrow within minutes."
    },
    "infected_hive": {
        "name": "Living Hive",
        "health": 250,
        "damage": 30,
        "speed": 0.5,
        "animal": True,
        "mutation": True,
        "boss": True,
        "swarm": True,
        "description": "A revolting amalgamation that may have once been a large mammal, now transformed into a mobile colony of smaller infected organisms. The central mass resembles a pulsating organ system with no clear head, from which swarm dozens of rat-sized parasitic creatures that attack in coordinated waves. When damaged, the hive releases toxic spores that cause disorientation and hallucinations."
    },
    "amphibious_terror": {
        "name": "Amphibious Terror",
        "health": 320,
        "damage": 55,
        "speed": 1.4,
        "swimming_speed": 2.2,
        "animal": True,
        "mutation": True,
        "boss": True,
        "swimming": True,
        "ambush": True,
        "description": "A nightmarish fusion of crocodilian and cephalopod characteristics that dominates both water and land. Its lower body resembles an alligator, while its upper torso has developed multiple tentacle-like appendages with barbed suckers. It can project ink-like clouds that contain hallucinogenic toxins, and can remain submerged for hours while extending sensory tendrils above water to detect prey."
    }
}
# Define friendly animal companions
FRIENDLY_ANIMALS = {
    # Dog variations
    "dog": {
        "name": "Survivor Dog",
        "health": 80,
        "damage": 20,
        "speed": 1.6,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "detection_bonus": 0.3,  # 30% bonus to detect threats
        "description": "A resilient canine that has somehow avoided infection, this German Shepherd mix shows signs of previous domestication. Though cautious, it responds positively to kind treatment and food offerings. With patience, such dogs can become loyal companions, offering protection and assistance in detecting nearby threats."
    },
    "hunting_dog": {
        "name": "Hunting Dog",
        "health": 70,
        "damage": 25,
        "speed": 1.8,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "tracking_bonus": 0.4,  # 40% bonus to tracking/finding resources
        "detection_bonus": 0.2,  # 20% bonus to detect threats
        "description": "This lean hunting breed - possibly a Lab-Hound mix - has survived by using its exceptional nose to find food. Appears to have been previously trained for hunting. While thinner than other dogs, it's exceptionally fast and possesses remarkable tracking abilities that could help locate distant resources."
    },
    "guard_dog": {
        "name": "Guard Dog",
        "health": 90,
        "damage": 30,
        "speed": 1.4,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "combat_bonus": 0.25,  # 25% damage bonus in combat
        "description": "A powerful Rottweiler or similar breed that has survived the apocalypse. Its sturdy build and protective instincts make it an excellent guardian. Though initially wary, with proper handling it could become a formidable ally in combat situations, intimidating threats and fighting ferociously when needed."
    },
    
    # Cat variations
    "cat": {
        "name": "Survivor Cat",
        "health": 40,
        "damage": 10,
        "speed": 1.5,
        "animal": True,
        "friendly": True,
        "stealth": True,
        "companion_potential": True,
        "stealth_bonus": 0.2,  # 20% bonus to stealth
        "description": "This feline has survived through stealth and cunning, avoiding infected by staying high and quiet. Though not as immediately useful as dogs, cats provide companionship and can serve as early warning systems, reacting to approaching threats before humans can detect them."
    },
    "hunter_cat": {
        "name": "Hunter Cat",
        "health": 35,
        "damage": 15,
        "speed": 1.7,
        "animal": True,
        "friendly": True,
        "stealth": True,
        "companion_potential": True,
        "stealth_bonus": 0.3,  # 30% bonus to stealth
        "scavenging_bonus": 0.2,  # 20% bonus to finding small items
        "description": "A sleek, muscular feline that has thrived by hunting rats and small prey. Its exceptional reflexes and predatory instincts make it an efficient hunter. As a companion, it can help control vermin around camp and occasionally bring back small game, while also providing stealth advantages when exploring."
    },
    
    # Bird companions
    "crow": {
        "name": "Intelligent Crow",
        "health": 20,
        "damage": 5,
        "speed": 2.0,
        "animal": True,
        "friendly": True,
        "flying": True,
        "companion_potential": True,
        "scouting_bonus": 0.4,  # 40% bonus to scouting/avoiding ambushes
        "description": "An unusually intelligent crow that seems drawn to human presence. These adaptable birds have thrived in the post-apocalyptic world due to their problem-solving abilities. As a companion, it could scout ahead, warning of dangers and occasionally leading you to overlooked resources it finds with its keen eyes."
    },
    "falcon": {
        "name": "Trained Falcon",
        "health": 30,
        "damage": 12,
        "speed": 2.5,
        "animal": True, 
        "friendly": True,
        "flying": True,
        "companion_potential": True,
        "hunting_bonus": 0.3,  # 30% bonus when hunting
        "scouting_bonus": 0.3,  # 30% bonus to scouting
        "description": "A magnificent bird of prey that appears to have once been someone's trained hunting falcon. It still responds to basic falconry commands and gestures. These birds can spot movement from incredible distances and could be retrained to hunt small game or scout wide areas for threats and resources."
    },
    
    # Horse companion
    "horse": {
        "name": "Survivor Horse",
        "health": 150,
        "damage": 25,
        "speed": 2.2,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "carrying_capacity": 20,  # Extra inventory slots
        "travel_bonus": 0.5,  # 50% faster travel on maps
        "description": "A sturdy horse that has survived by grazing in remote areas. Shows signs of previous domestication and responds well to gentle handling. As a companion, it could significantly increase your travel speed and carrying capacity, though caring for it would require secure locations with access to grass and water."
    },
    
    # Specialized Zoo Companions
    "trained_falcon": {
        "name": "Trained Falcon",
        "health": 40,
        "damage": 15,
        "speed": 3.0,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "flight": True,
        "scouting": True,
        "detection_bonus": 0.6,  # 60% bonus to detect threats
        "scouting_range": 2,     # Can scout ahead 2 areas
        "skills": ["reconnaissance", "warning"],
        "location_specific": "zoo",
        "description": "Once part of the zoo's falconry exhibit, this bird of prey has been trained to respond to basic commands. Its incredible eyesight can spot dangers from extreme distances, and it can scout ahead to identify threats or resources. The falcon requires minimal resources to maintain and can silently warn of approaching dangers before they detect you."
    },
    "trained_chimpanzee": {
        "name": "Trained Chimpanzee",
        "health": 75,
        "damage": 20,
        "speed": 1.5,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "intelligence": 0.8,
        "tool_use": True,
        "carrying_capacity": 15,
        "skills": ["item_retrieval", "distraction", "tool_mastery"],
        "location_specific": "zoo",
        "description": "A remarkably intelligent former zoo resident that has formed a bond with humans. This chimpanzee can understand dozens of commands and can be trained to retrieve items, create distractions, or even use simple tools. While not as combat-capable as dogs, its problem-solving abilities make it invaluable for complex survival situations requiring adaptability and precision."
    },
    "tactical_k9": {
        "name": "Tactical K9 Unit",
        "health": 100,
        "damage": 35,
        "speed": 1.9,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "armored": True,
        "weapon_specialized": True,
        "combat_bonus": 0.4,
        "detection_bonus": 0.3,
        "skills": ["coordinated_attack", "equipment_carrier", "breach_assistance"],
        "location_specific": "military_base",
        "description": "A former military or police dog wearing remnants of tactical gear. This highly trained canine responds to verbal commands and hand signals with precision. Its specialized training allows it to participate in coordinated attacks, carry small pieces of equipment, and assist in securing or breaching areas. The surviving tactical vest provides some protection against attacks."
    },
    "research_macaw": {
        "name": "Research Station Macaw",
        "health": 35,
        "damage": 5,
        "speed": 2.8,
        "animal": True,
        "friendly": True,
        "companion_potential": True,
        "flight": True,
        "mimicry": True,
        "distraction": True,
        "skills": ["vocal_lure", "alarm_call", "research_memory"],
        "location_specific": "research_station",
        "description": "This brilliantly colored parrot was part of communication experiments at the research station. Its exceptional vocal mimicry can be used to distract enemies or lure them away from your position. More impressively, it seems to have memorized security codes and procedures from its time in the lab, occasionally squawking combinations that unlock secured areas within research facilities."
    },
    
    # Farm animals
    "chicken": {
        "name": "Chicken",
        "health": 10,
        "damage": 1,
        "speed": 0.8,
        "animal": True,
        "friendly": True,
        "farm_animal": True,
        "food_production": True,
        "description": "A common barnyard chicken that has survived the apocalypse. Though seemingly insignificant, chickens provide a renewable food source through eggs and can be raised in secure areas of settlements."
    },
    "goat": {
        "name": "Survivor Goat",
        "health": 50,
        "damage": 8,
        "speed": 1.2,
        "animal": True,
        "friendly": True,
        "farm_animal": True,
        "food_production": True,
        "description": "A hardy goat that has adapted well to post-apocalyptic conditions. Goats are valuable for milk production and can thrive on vegetation that other livestock can't eat. They're also more manageable than larger farm animals in a survival situation."
    },
    "sheep": {
        "name": "Survivor Sheep",
        "health": 60,
        "damage": 5,
        "speed": 0.9,
        "animal": True,
        "friendly": True,
        "farm_animal": True,
        "resource_production": True,  # Wool for crafting
        "description": "A sheep that has managed to avoid predators since the collapse. While not as versatile as goats, sheep provide both wool for crafting warm clothing and meat when needed. Their quiet nature makes them less likely to attract unwanted attention."
    },
    "farm_animal": {
        "name": "Livestock",
        "health": 100,
        "damage": 5,
        "speed": 0.7,
        "animal": True,
        "friendly": True,
        "farm_animal": True,
        "food_production": True,
        "description": "Surviving domesticated animals like goats, sheep, or pigs that can provide sustainable food sources for survivor communities. These animals require protection and resources but offer significant benefits to long-term survival."
    }
}

# Define human survivors that can be encountered
SURVIVOR_TYPES = {
    "hostile_bandit": {
        "name": "Hostile Bandit",
        "health_range": [70, 120],
        "damage_range": [15, 30],
        "speed_range": [0.9, 1.3],
        "hostile": True,
        "loot_quality": "medium",
        "description": "A desperate survivor who has turned to violence and theft to survive. Heavily armed and dangerous, they view other survivors as walking supply caches rather than potential allies. Years of fighting for survival have left them paranoid and quick to attack.",
        "dialogue": {
            "greeting": ["Back off! This is my territory!", "Hand over your supplies and nobody gets hurt!", "One more step and you're dead!"],
            "aggressive": ["I'm gonna enjoy taking your stuff!", "Should've just walked away!", "Time to die, fresh meat!"],
            "retreat": ["This isn't worth it! I'm out!", "Too much heat! Falling back!", "Live to fight another day!"]
        }
    },
    "cautious_survivor": {
        "name": "Cautious Survivor",
        "health_range": [60, 90],
        "damage_range": [10, 20],
        "speed_range": [0.8, 1.1],
        "hostile": False,
        "cautious": True,
        "recruit_difficulty": "medium",
        "skill_potential": ["medical", "crafting", "scavenging"],
        "loot_quality": "low",
        "description": "A survivor who has managed to stay alive by avoiding conflict whenever possible. Though wary of strangers, they might be convinced to cooperate if approached carefully. They've developed specialized skills to compensate for avoiding direct combat.",
        "dialogue": {
            "greeting": ["Stay where you are! I'm not looking for trouble.", "Who are you? What do you want?", "I've got nothing worth taking, so please just move along."],
            "friendly": ["Maybe we can help each other out.", "I've got some medical training if you need it.", "I know where to find supplies if we work together."],
            "joining": ["Strength in numbers, I guess.", "I'll join you, but I'm watching my back.", "I can contribute to your group if you'll have me."]
        }
    },
    "friendly_trader": {
        "name": "Friendly Trader",
        "health_range": [50, 80],
        "damage_range": [8, 15],
        "speed_range": [0.7, 1.0],
        "hostile": False,
        "trader": True,
        "recruit_difficulty": "hard",
        "loot_quality": "high",
        "description": "A rare sight in the wasteland - someone who still believes in rebuilding civilization through commerce. They travel between survivor enclaves trading goods and information. While not the best in combat, they have access to rare items and valuable knowledge about the region.",
        "dialogue": {
            "greeting": ["Hello there! Looking to trade?", "Ah, another survivor! I've got goods if you've got something to barter with.", "Well met, friend! Care to see my wares?"],
            "trade": ["I've got some special items you won't find easily.", "These medical supplies will cost you, but they're worth it.", "Information has value too - I can mark locations on your map for the right price."],
            "joining": ["Travel with you? Well, having protection would be nice...", "I suppose my trading network could benefit your group.", "I'll join you, but I expect to continue my trading operations."]
        }
    },
    "skilled_hunter": {
        "name": "Skilled Hunter",
        "health_range": [80, 110],
        "damage_range": [20, 35],
        "speed_range": [1.0, 1.4],
        "hostile": False,
        "recruit_difficulty": "medium",
        "skill_potential": ["hunting", "stealth", "tracking"],
        "loot_quality": "medium",
        "description": "A survivor who has mastered living off the land. Expert at tracking, hunting, and moving silently, they prefer the wilderness to the dangerous ruins of civilization. They've learned to read the environment and can detect threats long before others.",
        "dialogue": {
            "greeting": ["Freeze. Been tracking you for half a mile.", "You're making enough noise to attract every infected in the county.", "Hmm, you're not infected. That's something at least."],
            "friendly": ["I know where all the game trails are. Never go hungry with me around.", "I can teach you to move without being heard.", "The infected can't track what they can't see or smell."],
            "joining": ["The lone hunter routine gets old. Might be nice to hunt with a pack again.", "I'll join, but when we're in the wild, you follow my lead.", "I can keep your group fed and safe in the wilderness."]
        }
    },
    "military_veteran": {
        "name": "Military Veteran",
        "health_range": [100, 150],
        "damage_range": [25, 40],
        "speed_range": [0.9, 1.2],
        "hostile": False,
        "recruit_difficulty": "hard",
        "skill_potential": ["combat", "tactics", "leadership"],
        "loot_quality": "high",
        "description": "A former soldier who survived the initial outbreak due to superior training and equipment. Disciplined and combat-hardened, they approach survival with military precision. Though the chain of command is long gone, they still maintain a strict code of conduct.",
        "dialogue": {
            "greeting": ["Identify yourself!", "State your business, civilian.", "Hands where I can see them. Standard procedure."],
            "friendly": ["My unit was overrun during the early days. Been solo ever since.", "I've got combat training that could help your group survive.", "Military discipline is what keeps people alive in this hellscape."],
            "joining": ["Your group could use some proper tactical training.", "I'll join, but we need clear protocols and chain of command.", "Roger that. Consider me your new security specialist."]
        }
    },
    "engineering_expert": {
        "name": "Engineering Expert",
        "health_range": [60, 90],
        "damage_range": [10, 20],
        "speed_range": [0.7, 1.0],
        "hostile": False,
        "recruit_difficulty": "very_hard",
        "skill_potential": ["engineering", "electronics", "vehicle_repair"],
        "loot_quality": "medium",
        "description": "A survivor with extensive technical knowledge who has repurposed their skills for the apocalypse. They can repair vehicles, improve weapons, and build sophisticated traps. Their expertise makes them highly valued among survivor groups, though they're often not the best in direct combat.",
        "dialogue": {
            "greeting": ["Don't shoot! I'm more valuable alive than dead!", "I could fix that weapon you're pointing at me. Looks misaligned.", "Engineering solution: Neither of us wants violence, so let's cooperate."],
            "friendly": ["I can modify your equipment to work 30% more efficiently.", "That vehicle of yours? I could double its fuel efficiency.", "Give me some parts and I can build defenses that will keep the infected out."],
            "joining": ["Your group needs technical expertise. I'm it.", "I'll join if I get space to set up a workshop.", "Together we can build something that lasts in this broken world."]
        }
    }
}

# List of first and last names for randomly generating survivor identities
SURVIVOR_FIRST_NAMES = [
    # Western names
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", 
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth",
    "Margaret", "Nancy", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Donna", "Emily",
    "George", "Christopher", "Ronald", "Kevin", "Jason", "Edward", "Brian", "Timothy", "Jeffrey", "Ryan",
    "Melissa", "Michelle", "Laura", "Helen", "Deborah", "Amanda", "Stephanie", "Carolyn", "Christine", "Marie",
    "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Charlotte", "Mia", "Amelia", "Harper", "Evelyn",
    "Noah", "Liam", "Jacob", "Mason", "Ethan", "Logan", "Lucas", "Oliver", "Alexander", "Elijah",
    "Benjamin", "Samuel", "Jack", "Henry", "Owen", "Sebastian", "Gabriel", "Carter", "Jayden", "Nathan",
    "Grace", "Chloe", "Lily", "Hannah", "Zoe", "Abigail", "Ella", "Victoria", "Madison", "Scarlett",
    "Jonathan", "Nicholas", "Aiden", "Dylan", "Isaac", "Christian", "Wyatt", "Patrick", "Jeremy", "Aaron",
    "Samantha", "Rachel", "Lauren", "Julia", "Rebecca", "Katherine", "Katherine", "Madeline", "Natalie", "Leah",
    "Peter", "Frank", "Brandon", "Tyler", "Gregory", "Dennis", "Raymond", "Gary", "Vincent", "Eric",
    "Catherine", "Nicole", "Angela", "Brittany", "Amy", "Pamela", "Theresa", "Judith", "Joan", "Denise",
    
    # Middle Eastern names
    "Ahmed", "Mohammed", "Ali", "Hassan", "Ibrahim", "Omar", "Mustafa", "Karim", "Samir", "Yusuf",
    "Fatima", "Aisha", "Leila", "Zahra", "Yasmin", "Amira", "Noor", "Samira", "Farah", "Zeinab",
    "Khalid", "Mahmoud", "Tariq", "Rami", "Jamal", "Bilal", "Hamza", "Ziad", "Fadi", "Nasir",
    "Layla", "Hanan", "Rana", "Maya", "Maha", "Dalia", "Rasha", "Jamila", "Salma", "Nadia",
    "Adnan", "Faisal", "Hakim", "Salim", "Abdul", "Malik", "Rashid", "Kareem", "Bassam", "Jalal",
    "Mariam", "Fathima", "Soraya", "Sahar", "Noura", "Asma", "Reem", "Farida", "Latifa", "Rabab",
    
    # East Asian names
    "Wei", "Chen", "Hiroshi", "Jin", "Xiang", "Ming", "Tao", "Hiro", "Yong", "Jian",
    "Li", "Mei", "Yuki", "Sakura", "Ying", "Jing", "Aiko", "Hikari", "Xiu", "Nari",
    "Takashi", "Kenji", "Haruki", "Ryo", "Daichi", "Kazuo", "Akira", "Takumi", "Shota", "Yuta",
    "Yumi", "Ayumi", "Haruka", "Rina", "Yuna", "Kaori", "Mei", "Akemi", "Naomi", "Saki",
    "Wei", "Feng", "Cheng", "Hong", "Jie", "Peng", "Xiao", "Jun", "Yang", "Kai", 
    "Fang", "Hui", "Jia", "Yan", "Xue", "Min", "Jiaying", "Liling", "Xiuying", "Zhen",
    "Seung", "Joon", "Min-ho", "Ji-hoon", "Tae", "Young", "Hyun", "Sung", "Dae", "Jae",
    "Ji-young", "Min-ji", "Soo-jin", "Hye-jin", "Yu-na", "Eun-ji", "Ji-hye", "So-young", "Eun-young", "Mi-sook",
    
    # Latin American names
    "Carlos", "Miguel", "Javier", "Luis", "Jorge", "Antonio", "Alejandro", "Roberto", "Diego", "Hector",
    "Sofia", "Isabella", "Valentina", "Gabriela", "Camila", "Ana", "Lucia", "Elena", "Carmen", "Mariana",
    "Francisco", "Emilio", "Eduardo", "Rafael", "Fernando", "Manuel", "Ricardo", "Salvador", "Guillermo", "Raul",
    "Paula", "Daniela", "Natalia", "Victoria", "Catalina", "Laura", "Adriana", "Alicia", "Veronica", "Fernanda",
    "Andres", "Oscar", "Alberto", "Julio", "Lorenzo", "Mauricio", "Victor", "Ignacio", "Arturo", "Gustavo",
    "Jimena", "Paola", "Alejandra", "Monica", "Claudia", "Sara", "Teresa", "Rosa", "Julieta", "Marta",
    
    # South Asian names
    "Priya", "Lakshmi", "Neha", "Divya", "Anjali", "Anika", "Meera", "Riya", "Shreya", "Tanvi",
    "Arjun", "Vikram", "Raj", "Aditya", "Amit", "Rohan", "Vijay", "Sanjay", "Ajay", "Rahul",
    "Ananya", "Kavya", "Ishita", "Deepika", "Nisha", "Pooja", "Simran", "Anita", "Sanjana", "Isha",
    "Nikhil", "Varun", "Karthik", "Ravi", "Pranav", "Akash", "Kunal", "Arun", "Gaurav", "Nitin",
    "Aarti", "Jyoti", "Shweta", "Priyanka", "Sneha", "Sunita", "Rekha", "Swati", "Sapna", "Usha",
    "Deepak", "Manish", "Rajiv", "Vinay", "Prakash", "Dinesh", "Rajesh", "Manoj", "Sunil", "Anil",
    
    # Eastern European names
    "Dmitri", "Ivan", "Alexei", "Viktor", "Nikolai", "Sergei", "Vladimir", "Mikhail", "Boris", "Oleg",
    "Olga", "Tatiana", "Anastasia", "Natalia", "Svetlana", "Irina", "Yelena", "Katya", "Polina", "Masha",
    "Andrei", "Yuri", "Pavel", "Grigori", "Pyotr", "Maxim", "Leonid", "Vitaly", "Roman", "Semyon",
    "Ekaterina", "Maria", "Daria", "Lyudmila", "Valentina", "Nadezhda", "Galina", "Vera", "Alina", "Anna",
    "Jakub", "Adam", "Tomasz", "Piotr", "Marcin", "Marek", "Lukasz", "Jan", "Michal", "Pawel",
    "Agnieszka", "Magdalena", "Katarzyna", "Anna", "Barbara", "Malgorzata", "Ewa", "Joanna", "Krystyna", "Teresa",
    "Klaus", "Heinrich", "Fritz", "Hans", "Johann", "Otto", "Ernst", "Wilhelm", "Gunter", "Horst",
    "Helga", "Ingrid", "Gertrude", "Hildegard", "Ursula", "Renate", "Christa", "Edeltraud", "Inge", "Margot",
    
    # African names
    "Kwame", "Kofi", "Tunde", "Sekou", "Mandla", "Idris", "Chiwetel", "Nnamdi", "Oluwaseun", "Abioye",
    "Amara", "Zara", "Nia", "Folami", "Ayana", "Makena", "Zuri", "Thema", "Ayo", "Imani",
    "Chidi", "Tendai", "Themba", "Sipho", "Koffi", "Jabari", "Chike", "Adebayo", "Olufemi", "Jelani",
    "Nala", "Safiya", "Zahara", "Asha", "Nuru", "Abeni", "Eshe", "Monifa", "Zalika", "Nyala",
    "Chinua", "Kwesi", "Mamadou", "Kamau", "Jamal", "Obi", "Ngozi", "Wekesa", "Kwaku", "Mutua",
    "Amina", "Chiamaka", "Femi", "Dada", "Kehinde", "Oni", "Dayo", "Oluchi", "Fumni", "Amadi"
]

SURVIVOR_LAST_NAMES = [
    # Western surnames
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
    "Anderson", "Taylor", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Moore", "Young",
    "Clark", "Lewis", "Robinson", "Walker", "Allen", "King", "Wright", "Scott", "Green", "Adams",
    "Baker", "Nelson", "Carter", "Mitchell", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans",
    "Edwards", "Collins", "Stewart", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy",
    "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Reynolds", "James",
    "Murray", "Brooks", "Watson", "Powell", "Price", "Myers", "Long", "Ross", "Foster", "Sanders",
    "Jenkins", "Perry", "Butler", "Barnes", "Fisher", "Henderson", "Coleman", "Simmons", "Patterson", "Jordan",
    "Graham", "Hughes", "Harrison", "Gibson", "McDonald", "Kennedy", "Wells", "Dixon", "Woods", "West",
    "Ferguson", "Warren", "Mills", "Nichols", "Grant", "Knight", "Ferguson", "Stone", "Hawkins", "Dunn",
    
    # East Asian surnames
    "Kim", "Zhang", "Wang", "Li", "Chen", "Liu", "Tanaka", "Suzuki", "Sato", "Yamamoto",
    "Nakamura", "Takahashi", "Kobayashi", "Watanabe", "Park", "Choi", "Lee", "Ng", "Wu", "Ho",
    "Yoshida", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Hayashi", "Kimura", "Saito", "Shimizu", "Yamazaki",
    "Mori", "Ikeda", "Hashimoto", "Ishikawa", "Yamada", "Ogawa", "Goto", "Okada", "Hasegawa", "Morita",
    "Lin", "Zhu", "Huang", "Zhou", "Yang", "Zhao", "Sun", "Luo", "Ma", "Xu",
    "Guo", "Song", "Zheng", "Cao", "Peng", "Deng", "Xie", "Liang", "Tang", "Jiang",
    "Jeong", "Kang", "Cho", "Yoon", "Shin", "Yoo", "Han", "Im", "Kwon", "Jang",
    "Baek", "Ahn", "Song", "Chung", "Bae", "Hong", "Ryu", "Lim", "Seo", "Yang",
    
    # South Asian surnames
    "Singh", "Patel", "Gupta", "Kumar", "Sharma", "Shah", "Das", "Rao", "Reddy", "Nair",
    "Devi", "Kaur", "Malhotra", "Chatterjee", "Kapoor", "Jain", "Agarwal", "Mukherjee", "Verma", "Yadav",
    "Banerjee", "Pande", "Bose", "Menon", "Desai", "Iyer", "Chowdhury", "Patil", "Sinha", "Dutta",
    "Khanna", "Chopra", "Sarkar", "Chauhan", "Malik", "Bhatnagar", "Mahajan", "Mathur", "Mittal", "Rastogi",
    "Goswami", "Chakraborty", "Bhat", "Naidu", "Pillai", "Tagore", "Chanda", "Saxena", "Varma", "Khatri",
    "Biswas", "Deshpande", "Ganguly", "Dubey", "Shukla", "Rajan", "Trivedi", "Cherian", "Mehra", "Prasad",
    
    # Latin American surnames
    "Gonzalez", "Hernandez", "Lopez", "Martinez", "Rodriguez", "Perez", "Sanchez", "Ramirez", "Flores", "Torres",
    "Diaz", "Santos", "Fernandez", "Morales", "Ortiz", "Cruz", "Reyes", "Gutierrez", "Mendoza", "Ruiz",
    "Alvarez", "Castillo", "Gomez", "Vasquez", "Ramos", "Jimenez", "Romero", "Vargas", "Acosta", "Fuentes",
    "Medina", "Herrera", "Suarez", "Aguirre", "Sosa", "Miranda", "Valencia", "Delgado", "Cortes", "Navarro",
    "Rojas", "Castro", "Aguilar", "Quintero", "Molina", "Estrada", "Pacheco", "Cardenas", "Orozco", "Contreras",
    "Valdez", "Cervantes", "Vera", "Santiago", "Guerrero", "Rivera", "Bautista", "Montoya", "Carrillo", "Mejia",
    
    # Eastern European surnames
    "Ivanov", "Kowalski", "Müller", "Novak", "Petrov", "Popov", "Smirnov", "Kovalenko", "Kozlov", "Sokolov",
    "Volkov", "Kuznetsov", "Wagner", "Bauer", "Hoffman", "Nowak", "Wójcik", "Kowalczyk", "Kaminski", "Lewandowski",
    "Fedorov", "Antonov", "Morozov", "Solovyov", "Lebedev", "Kozlowski", "Mazur", "Zielinski", "Szymanski", "Zajac",
    "Malinowski", "Jaworski", "Grabowski", "Weber", "Fischer", "Schneider", "Koch", "Wolf", "Schäfer", "Becker",
    "Kovalchuk", "Shevchenko", "Boyko", "Tkachuk", "Savchenko", "Bondarenko", "Kravchenko", "Sydorenko", "Marchenko", "Moroz",
    "Klimenko", "Lysenko", "Karpenko", "Pavlenko", "Savchuk", "Melnyk", "Koval", "Shvets", "Ostapenko", "Polishchuk",
    
    # Middle Eastern surnames
    "Ibrahim", "Mahmoud", "Abbas", "Hassan", "Mohammed", "Ahmed", "Ali", "Khalil", "Awad", "Mansour",
    "Saleh", "Rahman", "Yousef", "Amir", "Bishara", "Farah", "Hakim", "Najjar", "Wasem", "Zaher",
    "Al-Farsi", "Kazemi", "Shirazi", "Karimi", "Mousavi", "Nassar", "El-Masri", "Darwish", "Haddad", "Salim",
    "Zidane", "Rahim", "Kamal", "Sharif", "Qureshi", "Aziz", "Hamid", "Hafez", "Mahdi", "Saab",
    "Al-Aswad", "Al-Hassan", "Al-Nabulsi", "Al-Sayyid", "Bakir", "El-Sayyed", "Habibi", "Ismail", "Jaber", "Khoury",
    "Nasrallah", "Qasim", "Rabbani", "Safar", "Taha", "Yahya", "Zakaria", "Zaman", "Majid", "Naser",
    
    # African surnames
    "Okafor", "Osei", "Mensah", "Abiola", "Adebayo", "Chukwu", "Eze", "Mwangi", "Nkosi", "Okonkwo",
    "Tutu", "Mandela", "Abebe", "Kimathi", "Mbeki", "Nkrumah", "Mobutu", "Nyerere", "Sankara", "Selassie",
    "Adeyemi", "Agbaje", "Banda", "Chisanga", "Diallo", "Egwu", "Gueye", "Iwu", "Jalloh", "Kamara",
    "Kone", "Lumumba", "Makeba", "Ndlovu", "Okeke", "Patel", "Quan", "Ruto", "Senghor", "Toure",
    "Ugwu", "Vundi", "Waweru", "Xhosa", "Yakubu", "Zuma", "Achebe", "Biko", "Chikwenye", "Diop",
    "Ekwensi", "Fela", "Garvey", "Haile", "Igwe", "Jelani", "Kagame", "Luthuli", "Mutesa", "Nujoma"
]

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
            "/companions": {"func": self.cmd_companions, "help": "View and manage your companions"},
            "/dismiss": {"func": self.cmd_dismiss, "help": "Dismiss a companion from your group. Usage: /dismiss [companion_name]"},
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
                except (FileNotFoundError, json.JSONDecodeError):
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
        
        # Boss zombie dictionaries - moved here temporarily until we can properly add a BOSS_ZOMBIES constant
        BOSS_ZOMBIES = {
            "behemoth": {
                "name": "Behemoth",
                "health": 300,
                "damage": 40,
                "speed": 1,
                "armor": 20,
                "special_ability": "ground_pound",
                "special_moves": ["charge", "ground_pound", "throw_debris"],
                "description": "A massive, hulking monster standing over 8 feet tall. Former military personnel mutated by experimental treatments at Fort Defiance. Its skin has hardened into armor-like plates with military gear fused to its body. Can tear concrete barriers apart and throw debris as projectiles."
            },
            "infected_scientist": {
                "name": "Patient Zero",
                "health": 200,
                "damage": 25,
                "speed": 2,
                "special_ability": "mutation_cloud",
                "special_moves": ["call_infected", "mutation_cloud", "rapid_attack"],
                "vulnerability": "headshots",
                "description": "A uniquely intelligent infected wearing tattered remains of a laboratory coat. Unlike other zombies, it displays tactical intelligence and can coordinate attacks. Can release spores that temporarily enhance nearby zombies. Research notes suggest this may be one of the original test subjects where the outbreak began."
            },
            "tank_commander": {
                "name": "Armored Tank Commander",
                "health": 250,
                "damage": 35,
                "speed": 1,
                "armor": 30,
                "special_ability": "howitzer_arm",
                "special_moves": ["cannon_blast", "machine_gun_spray", "armor_charge"],
                "weakness": "exposed_back",
                "description": "A grotesque fusion of man and machine, this former tank commander is partially merged with tank armor plating. Its right arm has morphed into a cannon-like appendage capable of firing explosive blasts, while its left arm resembles a machine gun. Despite its heavy armor, the creature's back remains exposed where the mutation is incomplete."
            }
        }
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
            # First check if it's in our BOSS_ZOMBIES dictionary
            if specific_boss in BOSS_ZOMBIES:
                boss_data = BOSS_ZOMBIES[specific_boss]
                zombie = {
                    "name": boss_data["name"],
                    "health": boss_data["health"],
                    "max_health": boss_data["health"],
                    "damage": boss_data["damage"],
                    "speed": boss_data.get("speed", 1),
                    "is_boss": True,
                    "type": specific_boss,
                    "special_ability": boss_data.get("special_ability", None),
                    "special_moves": boss_data.get("special_moves", []),
                    "description": boss_data.get("description", "A powerful zombie boss.")
                }
                
                # Add any specific attributes
                for key in ["armor", "vulnerability", "weakness"]:
                    if key in boss_data:
                        zombie[key] = boss_data[key]
                
                # Apply level scaling
                level_factor = 1 + (self.player["level"] - 1) * 0.15
                zombie["health"] = int(zombie["health"] * level_factor)
                zombie["max_health"] = zombie["health"]
                zombie["damage"] = int(zombie["damage"] * level_factor)
                
                print(f"\n*** BOSS ENCOUNTER: {zombie['name']} ***")
                print(zombie["description"])
                print("This is no ordinary zombie. Prepare for a tough fight!")
                return zombie
                
            # Fallback to ZOMBIE_TYPES for backward compatibility
            elif specific_boss in ZOMBIE_TYPES:
                zombie = ZOMBIE_TYPES[specific_boss].copy()
                zombie["type"] = specific_boss
                zombie["max_health"] = zombie["health"]
                zombie["is_boss"] = True

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
                       
        # Adjust zombie type weights based on location
        location_id = self.player["location"]
        current_hour = self.player["hours_passed"] % 24
        is_night = 18 <= current_hour or current_hour < 6
                       
        # In the military base, add special zombie types with higher probability
        if location_id == "military_base":
            # More likely to encounter military, hazmat, and screamer zombies
            military_base_zombies = {
                "military": 8,    # Very common
                "hazmat": 5,      # Common
                "screamer": 4,    # Somewhat common
                "walker": 3,      # Less common than usual
                "runner": 3,
                "brute": 3,
                "spitter": 2,
                "crawler": 2,
                "bloater": 2
            }
            
            # Also small chance to encounter a boss
            if random.random() < 0.05:  # 5% chance for boss
                boss_type = random.choice(["behemoth", "tank_commander"])
                return self.spawn_zombie(specific_boss=boss_type)
        weights = []

        # Location-specific zombie spawning

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

                    for _, inv_item in enumerate(self.player["inventory"]):  # Index not used
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
        """Travel to a different location, optionally using a vehicle."""
        # Handle argument parsing with more options
        if not args or (len(args) >= 1 and args[0] == "help"):
            print("Usage: /go [location] (optional: using [vehicle_id])")
            print("Available locations:")
            for loc_id, loc_data in LOCATIONS.items():
                if loc_id != self.player["location"]:
                    print(f"- {loc_id} ({loc_data['name']})")
            
            # Show available vehicles if player has any
            vehicles = self.get_player_vehicles()
            if vehicles:
                print("\nAvailable vehicles:")
                for vehicle_id, vehicle_data in vehicles.items():
                    fuel_status = ""
                    if vehicle_data.get("fuel_type"):
                        current_fuel = vehicle_data.get("current_fuel", 0)
                        max_fuel = vehicle_data.get("fuel_capacity", 0)
                        fuel_status = f" - Fuel: {current_fuel}/{max_fuel}"
                    
                    print(f"- {vehicle_id} ({vehicle_data['name']}) - Speed: {vehicle_data.get('speed', 1)}x{fuel_status}")
            return

        # Parse destination
        destination = args[0].lower()
        
        # Parse vehicle if provided
        vehicle_id = None
        if len(args) >= 3 and args[1].lower() == "using":
            vehicle_id = args[2].lower()
        
        if destination in LOCATIONS:
            if destination == self.player["location"]:
                print("You are already there.")
                return

            # Check if player has enough stamina (only if not using vehicle)
            if not vehicle_id and self.player["stamina"] < 10:
                print("You're too exhausted to travel on foot. Rest, use items to restore stamina, or use a vehicle.")
                return
            
            # Check if the vehicle exists and is available
            vehicle_data = None
            travel_speed_multiplier = 1  # Default walking speed
            fuel_consumption = 0
            vehicle_protection = 0
            
            if vehicle_id:
                vehicles = self.get_player_vehicles()
                if not vehicles or vehicle_id not in vehicles:
                    print(f"You don't have access to a {vehicle_id}.")
                    return
                
                vehicle_data = vehicles[vehicle_id]
                
                # Check fuel if the vehicle requires it
                if vehicle_data.get("fuel_type"):
                    current_fuel = vehicle_data.get("current_fuel", 0)
                    fuel_consumption = vehicle_data.get("fuel_consumption", 1)
                    
                    if current_fuel < fuel_consumption:
                        # Safely get fuel type and vehicle name
                        fuel_type = "fuel" if vehicle_data is None else vehicle_data.get("fuel_type", "fuel")
                        vehicle_name = "vehicle" if vehicle_data is None else vehicle_data.get("name", "vehicle")
                        print(f"Not enough {fuel_type} in your {vehicle_name} for this journey.")
                        return
                
                # Get travel speed multiplier and protection
                travel_speed_multiplier = vehicle_data.get("speed", 1)
                vehicle_protection = vehicle_data.get("armor", 0)
                
                print(f"You're traveling using your {vehicle_data['name']}.")
            else:
                print("You're traveling on foot.")

            # Calculate encounter chance based on vehicle and danger level
            danger_level = LOCATIONS[destination]["danger_level"]
            base_encounter_chance = 0.2 * danger_level
            
            # Vehicles reduce encounter chance and provide protection
            if vehicle_data:
                # Louder vehicles attract more zombies but higher speed may avoid them
                noise_level = vehicle_data.get("noise_level", 1)
                encounter_chance = base_encounter_chance * (noise_level / 10)
                # Faster vehicles can avoid some encounters
                encounter_chance = encounter_chance / travel_speed_multiplier
            else:
                encounter_chance = base_encounter_chance
            
            # Check for random encounter while traveling
            if danger_level > 0 and random.random() < encounter_chance:
                if vehicle_data and vehicle_data.get("noise_level", 0) > 5:
                    print("\nThe noise of your vehicle has attracted zombies during your journey!")
                else:
                    print("\nWhile traveling, you encounter zombies!")
                
                # Vehicle provides protection
                if vehicle_protection > 0 and vehicle_data:
                    print(f"Your {vehicle_data.get('name', 'vehicle')} provides some protection.")
                
                self.current_zombie = self.spawn_zombie()
                self.start_combat()
                if not self.game_running:  # Player died in combat
                    return

            # Update location
            self.player["location"] = destination
            print(f"\nYou have traveled to {LOCATIONS[destination]['name']}.")
            
            # Consume resources based on travel method
            if vehicle_id:
                # Consume fuel
                if fuel_consumption > 0:
                    # Get vehicles reference again to be sure
                    vehicles = self.get_player_vehicles()
                    current_fuel = vehicles[vehicle_id].get("current_fuel", 0)
                    vehicles[vehicle_id]["current_fuel"] = current_fuel - fuel_consumption
                    # Use default fuel type if vehicle_data is None
                    fuel_type = "fuel" if vehicle_data is None else vehicle_data.get("fuel_type", "fuel")
                    print(f"Consumed {fuel_consumption} units of {fuel_type}. Remaining: {vehicles[vehicle_id]['current_fuel']}")
                
                # Small stamina cost for driving
                self.player["stamina"] = max(self.player["stamina"] - 3, 0)
            else:
                # Higher stamina cost for walking
                self.player["stamina"] = max(self.player["stamina"] - 10, 0)

            # Check mission progress
            self.check_mission_progress("location", destination)

            # Travel time adjusted by vehicle speed
            if vehicle_id:
                # Vehicle travel is still a medium_action, but takes less time due to speed
                travel_hours = random.uniform(1, 3) / travel_speed_multiplier
                self.advance_time("medium_action", travel_hours)
            else:
                # On foot travel is a heavy action that takes significant time
                self.advance_time("heavy_action")
    
    def get_player_vehicles(self):
        """Get all vehicles the player currently has access to."""
        if "vehicles" not in self.player:
            self.player["vehicles"] = {}
        return self.player["vehicles"]
    
    def has_item(self, item_id, amount=1):
        """Check if the player has a specific item in their inventory.
        
        Args:
            item_id (str): The ID of the item to check for
            amount (int): The required amount of the item
            
        Returns:
            bool: True if the player has at least the required amount, False otherwise
        """
        for item in self.player["inventory"]:
            if item["id"] == item_id:
                return item.get("count", 1) >= amount
        return False
        
    def find_item_index(self, item_id):
        """Find the index of an item in the player's inventory.
        
        Args:
            item_id (str): The ID of the item to find
            
        Returns:
            int: The index of the item in the inventory list, or -1 if not found
        """
        for i, item in enumerate(self.player["inventory"]):
            if item["id"] == item_id:
                return i
        return -1
    
    def cmd_vehicles(self, *args):
        """View, repair, or manage the player's vehicles."""
        if not args:
            print("Usage: /vehicles [list|repair|refuel|status] (vehicle_id)")
            return
        
        command = args[0].lower()
        vehicles = self.get_player_vehicles()
        
        if command == "list":
            if not vehicles:
                print("You don't have any vehicles.")
                return
            
            print("==================================================")
            print("                YOUR VEHICLES                     ")
            print("==================================================")
            
            for vehicle_id, vehicle_data in vehicles.items():
                print(f"- {vehicle_data['name']} ({vehicle_id})")
                print(f"  Condition: {vehicle_data.get('durability', 0)}/{vehicle_data.get('max_durability', 100)}")
                
                if vehicle_data.get("fuel_type"):
                    current_fuel = vehicle_data.get("current_fuel", 0)
                    max_fuel = vehicle_data.get("fuel_capacity", 0)
                    print(f"  Fuel ({vehicle_data['fuel_type']}): {current_fuel}/{max_fuel}")
                
                print(f"  Speed: {vehicle_data.get('speed', 1)}x travel speed")
                if vehicle_data.get("armor", 0) > 0:
                    print(f"  Protection: {vehicle_data.get('armor', 0)}")
                print(f"  Noise Level: {vehicle_data.get('noise_level', 1)}/10")
                print(f"  Capacity: {vehicle_data.get('capacity', 1)} passengers")
                
                if vehicle_data.get("cargo_capacity", 0) > 0:
                    print(f"  Cargo Space: {vehicle_data.get('cargo_capacity')} units")
                
                print("")
        
        elif command == "repair" and len(args) >= 2:
            vehicle_id = args[1].lower()
            if vehicle_id not in vehicles:
                print(f"You don't have a {vehicle_id}.")
                return
            
            vehicle_data = vehicles[vehicle_id]
            durability = vehicle_data.get("durability", 0)
            max_durability = vehicle_data.get("max_durability", 100)
            
            if durability >= max_durability:
                print(f"Your {vehicle_data['name']} is already in perfect condition.")
                return
            
            # Check for repair requirements
            repair_reqs = vehicle_data.get("repair_requirements", {})
            if not repair_reqs:
                print(f"You don't know how to repair this vehicle.")
                return
            
            # Check if player has the required items
            can_repair = True
            missing_items = []
            
            for item_id, amount in repair_reqs.items():
                if not self.has_item(item_id, amount):
                    can_repair = False
                    missing_items.append(f"{amount}x {item_id}")
            
            if not can_repair:
                print(f"You need the following items to repair your {vehicle_data['name']}:")
                for item in missing_items:
                    print(f"- {item}")
                return
            
            # Perform the repair
            for item_id, amount in repair_reqs.items():
                self.remove_from_inventory(self.find_item_index(item_id), amount)
            
            repair_amount = int(max_durability * 0.25)  # Repair 25% of max durability
            vehicles[vehicle_id]["durability"] = min(durability + repair_amount, max_durability)
            
            print(f"You've repaired your {vehicle_data['name']}. New condition: {vehicles[vehicle_id]['durability']}/{max_durability}")
            
            # Repairing is a medium action
            self.advance_time("medium_action")
        
        elif command == "refuel" and len(args) >= 2:
            vehicle_id = args[1].lower()
            if vehicle_id not in vehicles:
                print(f"You don't have a {vehicle_id}.")
                return
            
            vehicle_data = vehicles[vehicle_id]
            
            # Check if vehicle uses fuel
            # Safely get fuel type
            fuel_type = None if vehicle_data is None else vehicle_data.get("fuel_type")
            if not fuel_type:
                print(f"This vehicle doesn't require fuel.")
                return
            
            current_fuel = vehicle_data.get("current_fuel", 0)
            max_fuel = vehicle_data.get("fuel_capacity", 0)
            
            if current_fuel >= max_fuel:
                print(f"Your {vehicle_data['name']} is already full of {fuel_type}.")
                return
            
            # Check if player has fuel
            fuel_item = None
            if fuel_type == "gasoline":
                fuel_item = "fuel"
            elif fuel_type == "diesel":
                fuel_item = "diesel_fuel"
            else:
                fuel_item = fuel_type
            
            fuel_index = self.find_item_index(fuel_item)
            if fuel_index == -1:
                print(f"You don't have any {fuel_type}.")
                return
            
            # Calculate how much fuel to add
            fuel_item_data = self.player["inventory"][fuel_index]
            fuel_amount = fuel_item_data.get("count", 1)
            fuel_needed = max_fuel - current_fuel
            fuel_to_use = min(fuel_amount, fuel_needed)
            
            # Refuel the vehicle
            vehicles[vehicle_id]["current_fuel"] = current_fuel + fuel_to_use
            
            # Remove used fuel from inventory
            self.remove_from_inventory(fuel_index, fuel_to_use)
            
            print(f"You've added {fuel_to_use} units of {fuel_type} to your {vehicle_data['name']}.")
            print(f"Fuel level: {vehicles[vehicle_id]['current_fuel']}/{max_fuel}")
            
            # Refueling is a light action
            self.advance_time("light_action")
        
        elif command == "status" and len(args) >= 2:
            vehicle_id = args[1].lower()
            if vehicle_id not in vehicles:
                print(f"You don't have a {vehicle_id}.")
                return
            
            vehicle_data = vehicles[vehicle_id]
            
            print(f"==== {vehicle_data['name']} Status ====")
            print(f"Condition: {vehicle_data.get('durability', 0)}/{vehicle_data.get('max_durability', 100)}")
            
            if vehicle_data.get("fuel_type"):
                current_fuel = vehicle_data.get("current_fuel", 0)
                max_fuel = vehicle_data.get("fuel_capacity", 0)
                fuel_range = current_fuel / vehicle_data.get("fuel_consumption", 1)
                print(f"Fuel ({vehicle_data['fuel_type']}): {current_fuel}/{max_fuel}")
                print(f"Estimated Range: {int(fuel_range)} trips")
            
            print(f"Speed: {vehicle_data.get('speed', 1)}x travel speed")
            print(f"Protection: {vehicle_data.get('armor', 0)}")
            print(f"Description: {vehicle_data.get('description', 'No description available.')}")
        
        else:
            print("Unknown vehicle command. Use /vehicles for help.")
    
    def cmd_craft_vehicle(self, *args):
        """Craft a vehicle from materials."""
        if not args or args[0] == "help":
            print("Usage: /craft_vehicle [vehicle_id]")
            print("Craftable vehicles:")
            
            for vehicle_id, vehicle_data in VEHICLES.items():
                if vehicle_data.get("craftable", False):
                    print(f"- {vehicle_id} ({vehicle_data['name']})")
            return
        
        vehicle_id = args[0].lower()
        
        # Check if this vehicle exists and is craftable
        if vehicle_id not in VEHICLES:
            print(f"There is no vehicle called '{vehicle_id}'.")
            return
        
        vehicle_data = VEHICLES[vehicle_id]
        if not vehicle_data.get("craftable", False):
            print(f"You cannot craft a {vehicle_data['name']}. You must find one instead.")
            return
        
        # Check crafting difficulty against player skills
        difficulty = vehicle_data.get("crafting_difficulty", "medium")
        player_level = self.player.get("level", 1)
        
        if difficulty == "extreme" and player_level < 10:
            print(f"Crafting a {vehicle_data['name']} requires level 10 mechanics skill. Your level: {player_level}")
            return
        elif difficulty == "hard" and player_level < 5:
            print(f"Crafting a {vehicle_data['name']} requires level 5 mechanics skill. Your level: {player_level}")
            return
        
        # Check for crafting requirements
        crafting_reqs = vehicle_data.get("crafting_requirements", {})
        if not crafting_reqs:
            print(f"You don't know how to craft this vehicle.")
            return
        
        # Check if player has the required items
        can_craft = True
        missing_items = []
        
        for item_id, amount in crafting_reqs.items():
            if not self.has_item(item_id, amount):
                can_craft = False
                missing_items.append(f"{amount}x {item_id}")
        
        if not can_craft:
            print(f"You need the following items to craft a {vehicle_data['name']}:")
            for item in missing_items:
                print(f"- {item}")
            return
        
        # Consume resources
        for item_id, amount in crafting_reqs.items():
            self.remove_from_inventory(self.find_item_index(item_id), amount)
        
        # Initialize vehicle with default values
        new_vehicle = vehicle_data.copy()
        
        # Set initial fuel level if applicable
        if new_vehicle.get("fuel_type"):
            new_vehicle["current_fuel"] = 0
        
        # Add vehicle to player's collection
        if "vehicles" not in self.player:
            self.player["vehicles"] = {}
        
        # Use an incrementing ID if player already has this type of vehicle
        base_id = vehicle_id
        i = 1
        while vehicle_id in self.player["vehicles"]:
            vehicle_id = f"{base_id}_{i}"
            i += 1
        
        self.player["vehicles"][vehicle_id] = new_vehicle
        
        print(f"You have successfully crafted a {new_vehicle['name']}!")
        
        # Crafting a vehicle is a heavy action
        self.advance_time("heavy_action", 5)  # Takes 5 hours

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
                # For Research Station, add a chance to find experimental weapons
                if self.player["location"] == "research_station" and resource_type == "weapons" and random.random() < 0.15:
                    # Special logic for experimental weapons in research station
                    experimental_items = list(EXPERIMENTAL_WEAPONS.keys())
                    
                    # Check if any experimental weapons already in inventory
                    existing_experimental = [item_id for item_id in experimental_items 
                                             if self.find_item_index(item_id) >= 0]
                    
                    # Prefer weapons player doesn't already have
                    available_weapons = [w for w in experimental_items if w not in existing_experimental]
                    
                    if not available_weapons:  # If player has all experimental weapons
                        available_weapons = experimental_items
                    
                    found_item_id = random.choice(available_weapons)
                    found_item = EXPERIMENTAL_WEAPONS[found_item_id]
                    print(Colors.colorize("\nYou've discovered a sealed research cabinet in a secured lab area!", Colors.CYAN))
                    time.sleep(1)
                    print(Colors.colorize("After bypassing the security measures, you find an experimental prototype weapon...", Colors.CYAN))
                    time.sleep(1)
                else:
                    found_item_id = random.choice(matching_items)
                    found_item = ITEMS[found_item_id]

                # Add to inventory if there's space
                if self.add_to_inventory(found_item_id):
                    print(f"You found: {Colors.colorize(found_item['name'], Colors.GREEN)}!")
                    print(found_item["description"])

                    # Special message for experimental weapons
                    if found_item_id in EXPERIMENTAL_WEAPONS:
                        print(Colors.colorize("\nThis is a rare prototype weapon with unique combat capabilities!", Colors.YELLOW))
                        print(Colors.colorize("Handle with care - it may be the only one of its kind remaining.", Colors.YELLOW))

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
        
        # Random encounter system - determine what type of encounter happens
        encounter_happened = False
        
        # Get location-specific encounter chances
        danger_level = location["danger_level"]
        base_encounter_chance = location.get("encounter_chance", 0.3)  # Default 30% if not specified
        
        # Calculate final encounter chance (higher in dangerous areas)
        encounter_chance = base_encounter_chance * (1 + (danger_level * 0.1))
        
        if random.random() < encounter_chance:
            # Determine encounter type
            encounter_type = random.choices(
                ["zombie", "animal", "survivor"], 
                weights=[0.6, 0.25, 0.15],  # Default weights
                k=1
            )[0]
            
            # Location-specific adjustments
            if location.get("infected_animals", False):
                # More likely to encounter animals in locations with specified animal types
                encounter_type = random.choices(
                    ["zombie", "animal", "survivor"],
                    weights=[0.4, 0.5, 0.1],
                    k=1
                )[0]
            
            if location.get("survivor_encounter_chance", 0):
                # Use location's specific survivor encounter chance
                survivor_chance = location.get("survivor_encounter_chance", 0)
                if survivor_chance > 0:
                    encounter_type = random.choices(
                        ["zombie", "animal", "survivor"],
                        weights=[max(0.1, 0.7 - (survivor_chance * 0.5)), 0.3, survivor_chance],
                        k=1
                    )[0]
            
            # Handle the encounter based on type
            if encounter_type == "zombie":
                print("\nWhile exploring, you encounter a zombie!")
                self.current_zombie = self.spawn_zombie()
                self.current_enemy = self.current_zombie  # Set both references for consistency
                self.start_combat()
                encounter_happened = True
            
            elif encounter_type == "animal":
                encounter_happened = self.encounter_animal()
            
            elif encounter_type == "survivor":
                encounter_happened = self.encounter_survivor()
                
        # Special items in location's special areas (if not in combat)
        if not encounter_happened and "special_areas" in location and "special_items" in location:
            special_item_chance = location.get("special_item_chance", 0.1)  # Default 10% if not specified
            
            if random.random() < special_item_chance:
                special_area = random.choice(location["special_areas"])
                special_item_id = random.choice(location["special_items"])
                
                print(f"\nYou discover {special_area} within {location['name']}.")
                
                if self.add_to_inventory(special_item_id):
                    special_item = ITEMS[special_item_id]
                    print(f"Inside, you find: {special_item['name']}!")
                    print(special_item["description"])
                else:
                    print(f"You found a {ITEMS[special_item_id]['name']}, but your inventory is full!")

        # Mission progress for exploration-type missions
        self.check_mission_progress("explore", self.player["location"])

    def start_combat(self):
        """Initialize combat with a zombie, animal, or hostile survivor."""
        if not hasattr(self, 'current_zombie') or not self.current_zombie:
            return

        self.in_combat = True
        enemy = self.current_zombie
        # Set both current_zombie and current_enemy to maintain compatibility
        self.current_enemy = enemy  # Add a more consistently named reference

        # Initialize variables
        time_color = Colors.YELLOW
        combat_color = Colors.RED
        is_night = False
        is_dawn_dusk = False
        damage_boost = 0
        
        # Check if this is a non-zombie enemy (animal or survivor)
        enemy_type = "zombie"  # Default
        if "animal" in enemy and enemy["animal"]:
            enemy_type = "animal"
            # Set specialized display for animals
            combat_color = Colors.GREEN
            time_color = combat_color
        elif "hostile" in enemy and enemy["hostile"] is True:
            enemy_type = "survivor"
            # Set specialized display for hostile survivors
            combat_color = Colors.YELLOW
            time_color = combat_color
        else:
            # Regular zombie
            combat_color = Colors.RED
            
            # Check time of day for combat adjustments (zombies only)
            current_hour = self.player["hours_passed"] % 24
            is_night = current_hour in NIGHT_HOURS
            is_dawn_dusk = current_hour in DAWN_DUSK_HOURS

            # Day/night color coding
            time_color = Colors.YELLOW
            if is_night:
                time_color = Colors.BLUE
            elif is_dawn_dusk:
                time_color = Colors.MAGENTA

            # Apply night combat modifier to zombies
            if is_night and NIGHT_ZOMBIE_DAMAGE_MODIFIER > 1.0:
                original_damage = enemy["damage"]
                enemy["damage"] = int(enemy["damage"] * NIGHT_ZOMBIE_DAMAGE_MODIFIER)
                damage_boost = enemy["damage"] - original_damage
        
        print("\n" + Colors.colorize("="*50, time_color))
        
        # Different combat messages based on enemy type
        if enemy_type == "animal":
            print(Colors.colorize(f"COMBAT: {enemy['name']} attacks!", Colors.BOLD + combat_color))
        elif enemy_type == "survivor":
            print(Colors.colorize(f"COMBAT: {enemy['name']} attacks!", Colors.BOLD + combat_color))
        else:
            print(Colors.colorize(f"COMBAT: {enemy['name']} appears!", Colors.BOLD + combat_color))
        
        print(Colors.colorize("="*50, time_color))

        # Show health with colors
        enemy_health_color = Colors.health_color(enemy["health"], enemy["max_health"])
        player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

        enemy_health = enemy["health"]
        enemy_max_health = enemy["max_health"]
        player_health = self.player["health"]
        player_max_health = self.player["max_health"]

        # Different display based on enemy type
        if enemy_type == "animal":
            print(f"Animal Health: {Colors.colorize(f'{enemy_health}/{enemy_max_health}', enemy_health_color)}")
        elif enemy_type == "survivor":
            print(f"Survivor Health: {Colors.colorize(f'{enemy_health}/{enemy_max_health}', enemy_health_color)}")
        else:
            print(f"Zombie Health: {Colors.colorize(f'{enemy_health}/{enemy_max_health}', enemy_health_color)}")
            
        print(f"Your Health: {Colors.colorize(f'{player_health}/{player_max_health}', player_health_color)}")

        # Show day/night status effects for zombies only
        if enemy_type == "zombie":
            if is_night:
                print(Colors.colorize("\nNight Combat: Zombies deal more damage and are harder to hit!", Colors.BOLD + Colors.BLUE))
                if damage_boost > 0:
                    print(Colors.colorize(f"The darkness gives the zombie +{damage_boost} attack damage!", Colors.RED))
            elif is_dawn_dusk:
                print(Colors.colorize("\nDusk/Dawn Combat: Limited visibility affects combat.", Colors.MAGENTA))
        
        # Special messages for different enemy types
        if enemy_type == "animal":
            if "pack_hunter" in enemy and enemy.get("pack_attack", False):
                print(Colors.colorize(f"\nThe {enemy['name']} is hunting in a pack! They coordinate their attacks.", Colors.BOLD + Colors.GREEN))
            if "ambush" in enemy and enemy.get("ambush", False):
                print(Colors.colorize(f"\nThe {enemy['name']} is an ambush predator! Watch for surprise attacks.", Colors.BOLD + Colors.GREEN))
        elif enemy_type == "survivor":
            if "skills" in enemy and enemy["skills"]:
                skill_list = ", ".join(enemy["skills"])
                print(Colors.colorize(f"\nThis survivor has skills in: {skill_list}", Colors.BOLD + Colors.YELLOW))

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
        
    def get_companions_assistance(self, enemy_type):
        """Calculate and apply combat assistance from companions.
        
        Args:
            enemy_type: Type of enemy being fought (zombie, animal, survivor)
            
        Returns:
            tuple: (damage_bonus, message_list) - The damage multiplier from companions and combat messages
        """
        if not self.player.get("companions"):
            return 1.0, []
        
        damage_bonus = 1.0
        messages = []
        
        # Get the player's currently equipped weapon type
        current_weapon_id = self.player.get("equipped_weapon", "fists")
        current_weapon_type = "melee"  # Default for fists
        
        if current_weapon_id != "fists":
            current_weapon = ITEMS.get(current_weapon_id, {})
            current_weapon_type = current_weapon.get("weapon_type", "melee")
        
        # Process each companion's assistance
        companion_specializations = self.player.get("companion_weapon_specializations", {})
        for idx, companion in enumerate(self.player.get("companions", [])):
            companion_id = companion.get("id", str(idx))
            
            # Only active companions can assist (not resting/injured)
            if companion.get("status", "active") != "active":
                continue
                
            # Calculate assistance chance based on relationship and morale
            assist_chance = 0.5 + (companion.get("relationship", 50) / 200)
            
            if random.random() < assist_chance:
                # Companion will assist in combat
                base_assist_damage = random.uniform(5, 15)
                assist_multiplier = 1.0
                
                # Apply weapon specialization if available
                if companion_id in companion_specializations:
                    spec = companion_specializations[companion_id]
                    if spec.get("weapon_type") == current_weapon_type:
                        assist_multiplier = spec.get("damage_bonus", 1.2)
                
                # Apply skill bonuses if available
                if "combat" in companion.get("skills", []):
                    assist_multiplier += 0.15
                
                if "marksmanship" in companion.get("skills", []) and current_weapon_type == "ranged":
                    assist_multiplier += 0.25
                
                if "blade_master" in companion.get("skills", []) and current_weapon_type == "blade":
                    assist_multiplier += 0.25
                    
                if "explosives" in companion.get("skills", []) and current_weapon_type == "explosive":
                    assist_multiplier += 0.3
                
                # Generate a random assistance message based on companion type and weapon
                assist_messages = [
                    f"{companion['name']} fires a well-aimed shot at the {enemy_type}!",
                    f"{companion['name']} strikes the {enemy_type} from the side!",
                    f"{companion['name']} creates a distraction, allowing you to hit harder!",
                    f"{companion['name']} coordinates with you for a more effective attack!"
                ]
                
                if current_weapon_type == "ranged":
                    assist_messages.extend([
                        f"{companion['name']} calls out weak points for you to target!",
                        f"{companion['name']} provides covering fire, increasing your accuracy!"
                    ])
                elif current_weapon_type == "melee":
                    assist_messages.extend([
                        f"{companion['name']} helps you flank the {enemy_type}!",
                        f"{companion['name']} throws a rock, distracting the {enemy_type}!"
                    ])
                
                # Add the companion's assistance to overall damage bonus
                companion_bonus = (base_assist_damage * assist_multiplier) / 100.0
                damage_bonus += companion_bonus
                
                # Add a message about the companion's assistance
                messages.append(Colors.colorize(random.choice(assist_messages), Colors.CYAN))
                
                # Small chance for companion to get injured during combat
                injury_chance = 0.05  # 5% base chance
                if random.random() < injury_chance:
                    companion["status"] = "injured"
                    companion["recovery_time"] = random.randint(2, 6)  # Hours needed to recover
                    messages.append(Colors.colorize(f"{companion['name']} was injured while helping you fight!", Colors.RED))
        
        return damage_bonus, messages

    def cmd_attack(self, *args):
        """Attack the current enemy in combat."""
        if not self.in_combat or (not hasattr(self, 'current_enemy') and not hasattr(self, 'current_zombie')):
            print(Colors.colorize("You are not in combat.", Colors.YELLOW))
            return

        # Player attacks first
        enemy = self.current_zombie if hasattr(self, 'current_zombie') else self.current_enemy
        hardcore_mode = self.player.get("hardcore_mode", False)
        
        # Determine enemy type
        enemy_type = "zombie"  # Default
        if "animal" in enemy and enemy["animal"]:
            enemy_type = "animal"
        elif "hostile" in enemy and enemy["hostile"] is True:
            enemy_type = "survivor"
            
        # Get companion assistance for combat
        companion_damage_bonus, companion_messages = self.get_companions_assistance(enemy_type)
        
        # Display companion assistance messages if any
        for message in companion_messages:
            print(message)

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
            weapon_id = self.player["equipped_weapon"]  # This is the inventory key
            inventory_idx = self.player["equipped_weapon"]
            
            # Different handling based on enemy type
            weakness_bonus = 1.0
            
            if enemy_type == "zombie":
                # Check zombie type for weaknesses
                enemy_subtype = enemy.get("type", "walker")
                zombie_weakness = ZOMBIE_TYPES.get(enemy_subtype, {}).get("weakness", None)
                
                # Apply bonus damage if the weapon exploits zombie weakness
                if zombie_weakness and weapon.get("damage_type", None) == zombie_weakness:
                    weakness_bonus = 2.0  # Double damage against vulnerable zombies
                    print(Colors.colorize(f"Your {weapon['name']} is extremely effective against this type of zombie!", Colors.GREEN))
            
            elif enemy_type == "animal":
                # Check animal type for weaknesses or resistances
                animal_type = enemy.get("animal_type", "dog")
                
                # Some weapons are better against certain animals
                if animal_type in ["bear", "boar"] and weapon.get("damage_type") == "piercing":
                    weakness_bonus = 1.5  # Piercing weapons better against large animals
                    print(Colors.colorize(f"Your {weapon['name']} cuts deep into the {animal_type}!", Colors.GREEN))
                elif animal_type in ["rat", "crow"] and weapon.get("damage_type") == "blunt":
                    weakness_bonus = 0.7  # Blunt weapons less effective against small, quick animals
                    print(Colors.colorize(f"The {animal_type} is too quick for your {weapon['name']} to hit solidly!", Colors.YELLOW))
                
            elif enemy_type == "survivor":
                # Check if the survivor has armor
                if enemy.get("armor", 0) > 0:
                    if weapon.get("damage_type") == "piercing":
                        weakness_bonus = 1.3  # Piercing weapons better against armored survivors
                        print(Colors.colorize(f"Your {weapon['name']} finds a weak spot in their armor!", Colors.GREEN))
                    elif weapon.get("damage_type") == "blunt":
                        weakness_bonus = 0.8  # Blunt weapons less effective against armor
                        print(Colors.colorize(f"Their armor absorbs some of the impact from your {weapon['name']}!", Colors.YELLOW))
                
            # Check for experimental weapons
            is_experimental = False
            if weapon_id in EXPERIMENTAL_WEAPONS:
                is_experimental = True
                special_effect = EXPERIMENTAL_WEAPONS[weapon_id].get("special_effect", None)
                
                # Apply experimental weapon special effects
                if special_effect == "stun" and random.random() < EXPERIMENTAL_WEAPONS[weapon_id].get("stun_chance", 0):
                    print(Colors.colorize(f"The {weapon['name']} emits a concentrated sonic pulse that disrupts {enemy['name']}'s neurology!", Colors.CYAN))
                    if not "effects" in enemy:
                        enemy["effects"] = {}
                    enemy["effects"]["stunned"] = {"duration": 2}  # Stunned for 2 turns
                    print(Colors.colorize(f"{enemy['name']} is stunned and will miss its next attack!", Colors.GREEN))
                
                elif special_effect == "freeze":
                    slow_effect = EXPERIMENTAL_WEAPONS[weapon_id].get("slow_effect", 0.5)
                    print(Colors.colorize(f"The {weapon['name']} coats {enemy['name']} in a rapidly expanding cryo-compound!", Colors.CYAN))
                    if not "effects" in enemy:
                        enemy["effects"] = {}
                    enemy["effects"]["frozen"] = {
                        "slow_percent": slow_effect,
                        "duration": random.randint(2, 3)
                    }
                    print(Colors.colorize(f"{enemy['name']}'s movement is severely restricted by ice formation!", Colors.BLUE))
                
                elif special_effect == "chain_lightning":
                    chain_targets = EXPERIMENTAL_WEAPONS[weapon_id].get("chain_targets", 1)
                    if chain_targets > 1:
                        chain_damage = int(damage * 0.6)  # Chain damage is 60% of primary
                        print(Colors.colorize(f"Electrical current from the {weapon['name']} arcs to nearby threats!", Colors.CYAN))
                        print(Colors.colorize(f"The chain lightning causes {chain_damage} additional damage!", Colors.YELLOW))
                        # In real combat, this would hit multiple enemies, but in single-target we just add damage
                        damage += chain_damage  # Add chain damage to total
                
                elif special_effect == "acid":
                    dot_damage = EXPERIMENTAL_WEAPONS[weapon_id].get("dot_damage", 5)
                    dot_duration = EXPERIMENTAL_WEAPONS[weapon_id].get("dot_duration", 3)
                    print(Colors.colorize(f"The {weapon['name']} sprays corrosive compounds that stick to {enemy['name']}!", Colors.CYAN))
                    if not "effects" in enemy:
                        enemy["effects"] = {}
                    enemy["effects"]["acid"] = {
                        "damage": dot_damage,
                        "duration": dot_duration
                    }
                    print(Colors.colorize(f"Acid begins eating through {enemy['name']}'s defenses, causing ongoing damage!", Colors.GREEN))

            # Check for special weapon properties
            # Handle area effect weapons (Molotov, Flamethrower)
            elif weapon_id == "molotov" or weapon.get("area_effect", False):
                if weapon_id == "flamethrower":
                    print(Colors.colorize(f"You unleash a stream of fire from your {weapon['name']}!", Colors.YELLOW))
                else:
                    if enemy_type == "zombie":
                        print(Colors.colorize(f"You throw the {weapon['name']} at the zombies!", Colors.YELLOW))
                    elif enemy_type == "animal":
                        print(Colors.colorize(f"You throw the {weapon['name']} at the {enemy['name']}!", Colors.YELLOW))
                    else:
                        print(Colors.colorize(f"You throw the {weapon['name']} at the survivor!", Colors.YELLOW))
                        
                print(Colors.colorize("The area erupts in flames!", Colors.RED))

                # Deal damage to primary enemy (with possible weakness bonus)
                actual_damage = int(damage * weakness_bonus)
                enemy["health"] -= actual_damage
                print(f"The {enemy['name']} takes {Colors.colorize(str(actual_damage), Colors.RED)} damage from the flames!")

                # Different effects based on enemy type
                if enemy_type == "zombie":
                    # Extra effective against bloaters
                    enemy_subtype = enemy.get("type", "walker")
                    if enemy_subtype == "bloater" and random.random() < 0.6:
                        print(Colors.colorize("The bloater's gas ignites in a violent explosion!", Colors.RED))
                        explosion_damage = damage * 2
                        enemy["health"] -= explosion_damage
                        print(f"The bloater takes an additional {Colors.colorize(str(explosion_damage), Colors.RED)} damage!")
                    
                    # Chance to attract more zombies but also damage them
                    if random.random() < 0.5:
                        extra_damage = damage // 2
                        print(Colors.colorize("The fire spreads, damaging nearby zombies!", Colors.YELLOW))
                        print(f"All zombies in the area take an additional {Colors.colorize(str(extra_damage), Colors.RED)} damage.")
                        enemy["health"] -= extra_damage
                        
                elif enemy_type == "animal":
                    # Animals may panic when on fire
                    if random.random() < 0.7:
                        print(Colors.colorize(f"The {enemy['name']} panics in the flames!", Colors.YELLOW))
                        enemy["skip_turn"] = True
                        
                elif enemy_type == "survivor":
                    # Survivors might try to put the fire out
                    if random.random() < 0.5:
                        print(Colors.colorize("The survivor tries to extinguish the flames!", Colors.YELLOW))
                        dodge_penalty = 15  # Makes it harder for them to dodge next turn

                # Flamethrower uses fuel
                if weapon_id == "flamethrower" and "ammo" in weapon:
                    weapon["ammo"] = max(0, weapon["ammo"] - 1)
                    print(Colors.colorize(f"Fuel remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.YELLOW))
                    
                    if weapon["ammo"] <= 0:
                        print(Colors.colorize("Your flamethrower is out of fuel!", Colors.RED))
                
                # Molotov is single-use
                if weapon_id == "molotov":
                    self.remove_from_inventory(self.player["equipped_weapon"])
                    self.player["equipped_weapon"] = None
                else:
                    # Reduce durability for other weapons
                    if "durability" in weapon:
                        weapon["durability"] = max(0, weapon["durability"] - 1)

                # Skip the normal attack flow
                if enemy["health"] <= 0:
                    self.end_combat(True)
                    return

                # Skip to enemy's attack
                print(Colors.colorize("\nThe flames die down...", Colors.YELLOW))
                
            # Handle flamethrower separately (it's an area weapon but reusable)
            elif weapon_id == "flamethrower":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is out of fuel!", Colors.RED))
                    print(Colors.colorize("You'll need to find fuel canisters to use it again.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You unleash a stream of fire from your {weapon['name']}!", Colors.RED))
                    
                    # Get enemy type to check for special effects
                    enemy_type = enemy.get("type", "walker")
                    
                    # Apply additional fire damage
                    fire_damage = weapon.get("fire_damage", 0)
                    total_damage = damage + fire_damage
                    
                    # Check for enemy type bonuses
                    if enemy_type == "bloater":
                        bloater_bonus = weapon.get("bloater_bonus", 3.0)
                        print(Colors.colorize("The bloater's gas ignites in a violent explosion!", Colors.RED + Colors.BOLD))
                        explosion_damage = int(total_damage * bloater_bonus)
                        total_damage += explosion_damage
                        print(Colors.colorize(f"BONUS EXPLOSION DAMAGE: {explosion_damage}!", Colors.RED + Colors.BOLD))
                    elif enemy_type == "crawler":
                        crawler_bonus = weapon.get("crawler_bonus", 1.5)
                        print(Colors.colorize("The crawler is completely engulfed in flames!", Colors.YELLOW))
                        total_damage = int(total_damage * crawler_bonus)
                    elif enemy_type == "screamer" and weapon.get("screamer_panic", False):
                        print(Colors.colorize("The screamer panics at the sight of the flames!", Colors.GREEN))
                        # 50% chance the screamer will flee instead of attacking this turn
                        if random.random() < 0.5:
                            # Add skip_enemy_turn flag to enemy instead of combat_data
                            enemy["skip_turn"] = True
                            print(Colors.colorize("The screamer is too terrified to attack this turn!", Colors.GREEN))
                    
                    # Deal damage to primary enemy
                    enemy["health"] -= total_damage
                    print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage from the intense flames!")
                    
                    # Apply burn effect to the enemy
                    if "effects" not in enemy:
                        enemy["effects"] = {}
                    
                    # Add a burning effect that will deal damage over time
                    continuous_damage = weapon.get("continuous_damage", 5)
                    continuous_turns = weapon.get("continuous_turns", 2)
                    
                    enemy["effects"]["burning"] = {
                        "damage_per_turn": continuous_damage,
                        "turns_remaining": continuous_turns,
                        "description": "On fire! Taking damage each turn."
                    }
                    
                    print(Colors.colorize(f"The {enemy['name']} is now on fire and will take {continuous_damage} damage for {continuous_turns} more turns!", Colors.YELLOW))
                    
                    # Chance to damage nearby enemies
                    area_damage_percent = weapon.get("area_damage_percent", 0.7)
                    area_damage = int(total_damage * area_damage_percent)
                    print(Colors.colorize("The fire spreads, damaging nearby hostiles!", Colors.YELLOW))
                    print(f"All enemies in the area take an additional {Colors.colorize(str(area_damage), Colors.RED)} damage.")
                    enemy["health"] -= area_damage  # This simulates other enemies in the area also taking damage
                    
                    # Create a temporary barrier of flames if the weapon has horde control
                    if weapon.get("horde_control", False):
                        print(Colors.colorize("A wall of flames temporarily blocks the path, controlling the enemy horde!", Colors.YELLOW))
                        if "temporary_effects" not in self.player:
                            self.player["temporary_effects"] = {}
                        
                        self.player["temporary_effects"]["flame_barrier"] = {
                            "turns": 2,
                            "defense_bonus": 10,
                            "description": "A wall of flame provides temporary protection"
                        }
                    
                    # Use ammo
                    weapon["ammo"] -= 1
                    print(Colors.colorize(f"Fuel remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.CYAN))
                    
                    # Skip the normal attack flow if enemy is defeated
                    if enemy["health"] <= 0:
                        self.end_combat(True)
                        return
                    
                    # Chance to attract additional enemies based on attraction radius
                    attraction_radius = weapon.get("attraction_radius", 3)
                    attraction_chance = min(0.1 * attraction_radius, 0.7)  # Up to 70% chance based on radius
                    
                    if random.random() < attraction_chance:
                        print(Colors.colorize(f"\nThe noise and flames have attracted more hostiles from up to {attraction_radius} zones away!", Colors.RED))
                        # This could be expanded to actually spawn more enemies in future combat rounds
                    
                    # Skip to enemy's attack
                    print(Colors.colorize("\nThe flames die down...", Colors.YELLOW))
                    
            # Handle sonic disruptor (especially effective against screamers)
            elif weapon_id == "tactical_crossbow":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is not loaded!", Colors.RED))
                    print(Colors.colorize("You'll need carbon-fiber bolts to use it.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You take careful aim with your {weapon['name']} and fire!", Colors.CYAN))
                    
                    # Get enemy type and subtype for bonus damage
                    enemy_subtype = ""
                    if enemy_type == "zombie":
                        enemy_subtype = enemy.get("type", "walker")
                    
                    critical_hit = False
                    bonus_damage = 0
                    
                    # Check for critical hit - improved with marksmanship
                    base_crit_chance = weapon.get("critical_hit_chance", 0.25)
                    # Marksmanship companions improve critical chance
                    if self.player.get("marksmanship_bonus", 0) > 0:
                        marksmanship_crit_bonus = min(0.25, self.player.get("marksmanship_bonus", 0) * 0.5)  # Up to 25% additional crit chance
                        crit_chance = base_crit_chance + marksmanship_crit_bonus
                        print(Colors.colorize("Your marksmanship training improves your aim!", Colors.GREEN))
                    else:
                        crit_chance = base_crit_chance
                        
                    if random.random() < crit_chance:
                        critical_hit = True
                        crit_multiplier = 1.5  # Base 50% bonus for crits
                        
                        # Marksmanship improves critical damage further
                        if self.player.get("marksmanship_bonus", 0) > 0:
                            crit_multiplier = 1.5 + (self.player.get("marksmanship_bonus", 0) * 0.5)  # Up to +50% additional crit damage
                            
                        bonus_damage += int(damage * (crit_multiplier - 1.0))
                        print(Colors.colorize("Critical hit! The bolt strikes a vital area!", Colors.GREEN))
                    
                    # Extra effective against hazmat zombies
                    if enemy_type == "zombie" and enemy_subtype == "hazmat":
                        penetration = weapon.get("hazmat_penetration", 0.85)
                        if random.random() < penetration:
                            print(Colors.colorize("The bolt penetrates the hazmat suit's protection!", Colors.GREEN))
                            bonus_damage += int(damage * 0.75)  # 75% bonus damage
                    
                    # Calculate base damage with weapon bonuses
                    base_damage = damage + bonus_damage
                    
                    # Apply companion damage bonus - especially effective with marksmanship specialists
                    total_damage = int(base_damage * companion_damage_bonus)
                    enemy["health"] -= total_damage
                    print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage!")
                    
                    # Reduce ammo
                    weapon["ammo"] = max(0, weapon["ammo"] - 1)
                    print(Colors.colorize(f"Bolts remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.YELLOW))
                    
                    # Chance to recover the bolt - improved with marksmanship
                    base_recovery_chance = 0.7  # Base 70% chance
                    
                    # Marksmanship improves recovery chance
                    if self.player.get("marksmanship_bonus", 0) > 0:
                        # Up to 20% additional recovery chance
                        recovery_bonus = min(0.2, self.player.get("marksmanship_bonus", 0) * 0.5)
                        recovery_chance = base_recovery_chance + recovery_bonus
                        
                        if random.random() < recovery_chance:
                            print(Colors.colorize("With your precision shooting, you'll definitely be able to recover this bolt.", Colors.GREEN))
                            self.player["temp_recovered_bolts"] = self.player.get("temp_recovered_bolts", 0) + 1
                    else:
                        # Standard recovery chance
                        if random.random() < base_recovery_chance:
                            print(Colors.colorize("You'll be able to recover this bolt after combat.", Colors.GREEN))
                            self.player["temp_recovered_bolts"] = self.player.get("temp_recovered_bolts", 0) + 1
                    
            elif weapon_id == "machete":
                print(Colors.colorize(f"You swing your {weapon['name']} in a wide arc!", Colors.CYAN))
                
                # Get enemy type for bonus damage
                enemy_subtype = enemy.get("type", "walker")
                bonus_damage = 0
                
                # Extra effective against bloater zombies
                if enemy_type == "zombie" and enemy_subtype == "bloater":
                    bonus_damage = weapon.get("bloater_damage_bonus", 30)
                    print(Colors.colorize("The blade slices deeply into the bloater's distended form!", Colors.GREEN))
                
                # Check for dismemberment chance
                if random.random() < weapon.get("dismemberment_chance", 0.3):
                    print(Colors.colorize("You sever a limb with your precise strike!", Colors.GREEN))
                    bonus_damage += int(damage * 0.4)  # 40% bonus damage for dismemberment
                
                # Calculate base damage with weapon bonuses
                base_damage = damage + bonus_damage
                
                # Apply companion damage bonus for blade weapons
                # Blade masters especially effective with this weapon
                if self.player.get("blade_bonus", 0) > 0:
                    blade_bonus = 1.0 + self.player.get("blade_bonus", 0)
                    total_damage = int(base_damage * blade_bonus * companion_damage_bonus)
                    print(Colors.colorize("Your blade mastery enhances the attack!", Colors.GREEN))
                else:
                    total_damage = int(base_damage * companion_damage_bonus)
                    
                enemy["health"] -= total_damage
                print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage!")
                    
            elif weapon_id == "m4_carbine":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is out of ammunition!", Colors.RED))
                    print(Colors.colorize("You'll need 5.56mm rounds to use it again.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You fire a burst from your {weapon['name']}!", Colors.CYAN))
                    
                    # Get enemy type for potential bonuses
                    enemy_subtype = enemy.get("type", "walker")
                    bonus_damage = 0
                    
                    # Extra effective against military zombies
                    if enemy_type == "zombie" and enemy_subtype == "military":
                        bonus_damage = weapon.get("military_damage_bonus", 25)
                        print(Colors.colorize("Your military-grade weapon is highly effective against the military zombie!", Colors.GREEN))
                    
                    # Apply marksmanship bonus - marksmanship specialists are better with firearms
                    marksmanship_bonus = 1.0
                    if self.player.get("marksmanship_bonus", 0) > 0:
                        marksmanship_bonus = 1.0 + self.player.get("marksmanship_bonus", 0)
                        print(Colors.colorize("Your marksmanship training improves your aim!", Colors.GREEN))
                    
                    # Burst fire gives multiple hits with companion bonus applied
                    base_hits = random.randint(1, 3)  # 1-3 hits per burst normally
                    
                    # Marksmanship companions can increase hit count
                    if companion_damage_bonus > 1.0 and marksmanship_bonus > 1.0:
                        bonus_hits = random.randint(0, 2)  # 0-2 additional hits with marksmanship companions
                        hits = base_hits + bonus_hits
                        if bonus_hits > 0:
                            print(Colors.colorize(f"Your companion helps you place {bonus_hits} additional shots!", Colors.GREEN))
                    else:
                        hits = base_hits
                    
                    # Apply damage calculation
                    base_damage = damage + bonus_damage
                    total_damage = 0
                    
                    for i in range(hits):
                        # Apply both companion and marksmanship bonuses to each hit
                        hit_damage = int(base_damage * marksmanship_bonus * companion_damage_bonus)
                        enemy["health"] -= hit_damage
                        total_damage += hit_damage
                        
                    print(f"The {hits}-round burst hits the {enemy['name']} for {Colors.colorize(str(total_damage), Colors.RED)} total damage!")
                    
                    # Reduce ammo (3 rounds per burst)
                    ammo_used = min(3, weapon["ammo"])
                    weapon["ammo"] = max(0, weapon["ammo"] - ammo_used)
                    print(Colors.colorize(f"Ammunition remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.YELLOW))
                    
                    # Loud gunfire attracts more zombies
                    if random.random() < 0.4:  # 40% chance
                        print(Colors.colorize("The gunfire echoes in the distance, possibly attracting more zombies...", Colors.RED))
                        # Logic to potentially spawn more zombies after combat
                        self.player["attracted_zombies"] = True
                        
            elif weapon_id == "flamethrower":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is out of fuel!", Colors.RED))
                    print(Colors.colorize("You'll need military-grade fuel canisters to use it again.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You unleash a stream of fire from your {weapon['name']}!", Colors.YELLOW))
                    print(Colors.colorize("The area erupts in flames!", Colors.RED))
                    
                    # Get enemy type for bonus damage
                    enemy_subtype = enemy.get("type", "walker")
                    bonus_damage = 0
                    
                    # Extra effective against different enemy types
                    if enemy_type == "zombie":
                        if enemy_subtype == "bloater":
                            bonus_damage = weapon.get("bloater_damage_bonus", 50)
                            print(Colors.colorize("The bloater's gas ignites in a violent explosion!", Colors.RED))
                        elif enemy_subtype == "crawler":
                            bonus_damage = weapon.get("crawler_damage_bonus", 40)
                            print(Colors.colorize("The flames completely engulf the low-lying crawler!", Colors.RED))
                    elif enemy_type == "animal":
                        # Animals take extra damage from fire
                        bonus_damage = weapon.get("animal_damage_bonus", 35)
                        print(Colors.colorize(f"The {enemy['name']} panics in the flames!", Colors.RED))
                    
                    # Apply explosives bonus from companions if available
                    explosives_bonus = 1.0
                    if self.player.get("explosives_bonus", 0) > 0:
                        explosives_bonus = 1.0 + self.player.get("explosives_bonus", 0)
                        print(Colors.colorize("Your knowledge of incendiary weapons improves the effectiveness!", Colors.GREEN))
                    
                    # Apply area effect damage with companion bonus
                    base_damage = damage + bonus_damage
                    actual_damage = int(base_damage * explosives_bonus * companion_damage_bonus)
                    
                    # Area effect damage to primary target
                    enemy["health"] -= actual_damage
                    print(f"The {enemy['name']} takes {Colors.colorize(str(actual_damage), Colors.RED)} damage from the flames!")
                    
                    # Chance for area effect to hit additional targets - improved with companions
                    area_chance = 0.6  # Base 60% chance
                    if companion_damage_bonus > 1.0 and explosives_bonus > 1.0:
                        area_chance = 0.8  # Increased to 80% with explosives specialist companion
                        print(Colors.colorize("Your companion helps direct the flames for maximum area coverage!", Colors.GREEN))
                    
                    if random.random() < area_chance:
                        area_damage = int(base_damage * 0.7 * explosives_bonus * companion_damage_bonus)  # 70% damage to area
                        print(Colors.colorize(f"The fire spreads, damaging nearby {enemy_type}s!", Colors.YELLOW))
                        print(f"Surrounding enemies take {Colors.colorize(str(area_damage), Colors.RED)} damage.")
                        # Additional damage to main target to simulate multiple enemies
                        enemy["health"] -= area_damage // 2
                    
                    # Reduce fuel
                    fuel_used = random.randint(2, 5)  # Variable fuel consumption
                    weapon["ammo"] = max(0, weapon["ammo"] - fuel_used)
                    print(Colors.colorize(f"Fuel remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.YELLOW))
                    
            elif weapon_id == "riot_shield":
                print(Colors.colorize(f"You brace behind your {weapon['name']} and push forward!", Colors.CYAN))
                
                # Apply companion tactical bonus to defense if available
                # Tactical companions provide better defensive strategies
                base_defense_bonus = weapon.get("defense_bonus", 25)
                if self.player.get("tactics_bonus", 0) > 0:
                    tactics_modifier = 1.0 + self.player.get("tactics_bonus", 0)
                    defense_bonus = int(base_defense_bonus * tactics_modifier)
                    print(Colors.colorize(f"Your tactical training enhances your shield effectiveness!", Colors.GREEN))
                else:
                    defense_bonus = base_defense_bonus
                    
                self.player["temp_defense_bonus"] = defense_bonus
                print(Colors.colorize(f"Your defensive stance grants +{defense_bonus} protection against {enemy_type} attacks!", Colors.GREEN))
                
                # Stunning effect - improved with tactical training
                stun_chance = 0.4  # Base 40% chance to stun
                if self.player.get("tactics_bonus", 0) > 0:
                    stun_chance += min(0.2, self.player.get("tactics_bonus", 0) * 0.5)  # Up to 20% additional stun chance
                    
                if random.random() < stun_chance:
                    print(Colors.colorize(f"You bash the {enemy['name']} with your shield, stunning it momentarily!", Colors.GREEN))
                    self.player["temp_stun_enemy"] = True
                
                # Apply damage (less than other weapons but still effective)
                # Apply companion damage bonus
                total_damage = int(damage * companion_damage_bonus)
                enemy["health"] -= total_damage
                print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage from the shield bash!")
                    
            elif weapon_id == "sonic_disruptor":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} has no power!", Colors.RED))
                    print(Colors.colorize("You'll need to find battery packs to use it again.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You activate the {weapon['name']}, sending out high-frequency sound waves!", Colors.CYAN))
                    
                    # Check enemy type and subtype for bonus damage
                    bonus_damage = 0
                    stun_effect = weapon.get("stun_effect", False)
                    enemy_subtype = enemy.get("type", "walker")
                    
                    # Apply engineering bonus - engineering specialists are better with tech weapons
                    tech_bonus = 1.0
                    if self.player.get("engineering_bonus", 0) > 0:
                        tech_bonus = 1.0 + self.player.get("engineering_bonus", 0)
                        print(Colors.colorize("Your engineering expertise improves the weapon's effectiveness!", Colors.GREEN))
                    
                    # Different effects based on enemy type
                    if enemy_type == "zombie":
                        # Extra effective against screamer types (both normal and boss variants)
                        if enemy_subtype in ["screamer", "banshee"]:
                            bonus_damage = weapon.get("screamer_damage_bonus", 40)  # Increased bonus damage
                            print(Colors.colorize(f"The sound waves are extremely effective against this sound-sensitive zombie!", Colors.GREEN))
                            print(Colors.colorize("The screamer's own sonic abilities are disrupted!", Colors.GREEN))
                            stun_effect = True
                            
                            # Prevent the screamer from summoning reinforcements
                            if "summoned_help" in enemy:
                                enemy["summoned_help"] = True
                        # Still effective but less powerful against other zombie types
                        else:
                            stun_effect = True  # All zombies can be stunned by sonic weapons
                            
                            # More effective against crawler zombie type (sensitive to vibrations)
                            if enemy_subtype == "crawler":
                                bonus_damage = 20
                                print(Colors.colorize("The sonic waves throw off the crawler's sensory perception!", Colors.GREEN))
                    
                    elif enemy_type == "animal":
                        # Animals have sensitive hearing
                        bonus_damage = weapon.get("animal_damage_bonus", 30)
                        stun_effect = True
                        print(Colors.colorize(f"The {enemy['name']} recoils from the high-frequency sound!", Colors.GREEN))
                    
                    elif enemy_type == "survivor":
                        # Less effective against humans but causes disorientation
                        stun_effect = random.random() < 0.5  # 50% chance to stun humans
                        print(Colors.colorize(f"The {enemy['name']} covers their ears in pain!", Colors.YELLOW))
                    
                    # Calculate base damage with weapon bonuses
                    base_damage = damage + bonus_damage
                    
                    # Engineering companions improve the weapon's effectiveness
                    if companion_damage_bonus > 1.0 and tech_bonus > 1.0:
                        # Engineering companion provides frequency modulation for maximum effect
                        print(Colors.colorize("Your companion optimizes the weapon's frequency for maximum effect!", Colors.GREEN))
                        stun_chance_bonus = 0.2  # +20% stun chance with engineering companion
                    else:
                        stun_chance_bonus = 0.0
                    
                    # Apply tech and companion damage bonuses
                    total_damage = int(base_damage * tech_bonus * companion_damage_bonus)
                    enemy["health"] -= total_damage
                    print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage from the sonic attack!")
                    
                    # Apply stun effect if applicable
                    stun_chance = 0.7 + stun_chance_bonus  # Base 70% chance + possible bonus
                    if stun_effect and random.random() < stun_chance:
                        print(Colors.colorize(f"The {enemy['name']} is stunned by the sound waves!", Colors.GREEN))
                        print(Colors.colorize("It won't be able to attack this turn!", Colors.GREEN))
                        
                        # Skip the enemy's attack turn
                        if enemy["health"] <= 0:
                            self.end_combat(True)
                        return
                    
                    # Use ammo - engineering companions can reduce ammo consumption
                    ammo_cost = 1
                    if tech_bonus > 1.3 and random.random() < 0.3:  # 30% chance with high engineering skill
                        print(Colors.colorize("Your engineering efficiency prevents power drain!", Colors.GREEN))
                        ammo_cost = 0
                    
                    weapon["ammo"] -= ammo_cost
                    print(Colors.colorize(f"Power remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.CYAN))
                    
                    # Skip to enemy's attack if not stunned and not defeated
                    if enemy["health"] <= 0:
                        self.end_combat(True)
                        return
                        
            # Handle hazmat piercer (especially effective against hazmat zombies)
            elif weapon_id == "hazmat_piercer":
                print(Colors.colorize(f"You thrust the {weapon['name']} forward with precision!", Colors.CYAN))
                
                # Check target type for bonus damage
                bonus_damage = 0
                precision_bonus = 1.0
                
                # Apply precision bonus from companions with blade mastery
                if self.player.get("blade_bonus", 0) > 0:
                    precision_bonus = 1.0 + (self.player.get("blade_bonus", 0) * 0.5)  # 50% of blade bonus applies
                    print(Colors.colorize("Your precise handling improves the piercing attack!", Colors.GREEN))
                
                # Different effects based on enemy type
                if enemy_type == "zombie":
                    # Extra effective against hazmat zombies
                    if "hazmat" in enemy.get("id", "").lower() or enemy.get("type", "") == "hazmat":
                        bonus_damage = weapon.get("hazmat_damage_bonus", 25)
                        print(Colors.colorize(f"The piercer punctures through the protective suit with ease!", Colors.GREEN))
                
                elif enemy_type == "survivor":
                    # Effective against human armor
                    if enemy.get("armor", 0) > 0:
                        bonus_damage = weapon.get("armor_damage_bonus", 20)
                        print(Colors.colorize(f"The piercer finds a gap in {enemy['name']}'s armor!", Colors.GREEN))
                
                # Blade master companions improve precision
                if companion_damage_bonus > 1.0 and precision_bonus > 1.0:
                    print(Colors.colorize("Your companion helps you target a vital weak point!", Colors.GREEN))
                    critical_chance = 0.3  # 30% critical hit chance with blade master companion
                    if random.random() < critical_chance:
                        print(Colors.colorize("CRITICAL HIT! The weapon strikes a vital point!", Colors.RED + Colors.BOLD))
                        bonus_damage += int(damage * 0.5)  # +50% damage on critical
                
                # Calculate base damage with all bonuses
                base_damage = damage + bonus_damage
                
                # Apply precision and companion damage bonuses
                total_damage = int(base_damage * precision_bonus * companion_damage_bonus)
                enemy["health"] -= total_damage
                print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage!")
                
                # Skip to enemy's attack if not defeated
                if enemy["health"] <= 0:
                    self.end_combat(True)
                    return
                    
            # Handle tactical crossbow (silent weapon with retrievable ammo)
            elif weapon_id == "tactical_crossbow":
                # Check if it has ammo
                if weapon["ammo"] <= 0:
                    print(Colors.colorize(f"Your {weapon['name']} is not loaded!", Colors.RED))
                    print(Colors.colorize("You'll need to find crossbow bolts to use it again.", Colors.YELLOW))
                else:
                    print(Colors.colorize(f"You aim the {weapon['name']} carefully and fire!", Colors.CYAN))
                    
                    # Get enemy type and subtype to check for special effects
                    enemy_subtype = enemy.get("type", "walker")
                    
                    # Apply marksmanship bonus - marksmanship specialists are excellent with this weapon
                    marksmanship_bonus = 1.0
                    if self.player.get("marksmanship_bonus", 0) > 0:
                        marksmanship_bonus = 1.0 + self.player.get("marksmanship_bonus", 0) * 1.5  # 150% of marksmanship bonus
                        print(Colors.colorize("Your marksmanship training improves your accuracy!", Colors.GREEN))
                    
                    # Check for enemy weakness based on type
                    weakness_bonus = 1.0
                    
                    if enemy_type == "zombie":
                        if enemy_subtype == "hazmat" or enemy.get("weakness", "") == "piercing_weapons":
                            weakness_bonus = weapon.get("hazmat_bonus", 3.0)  # Triple damage against hazmat zombies
                            print(Colors.colorize("The bolt pierces straight through the hazmat suit's protective material!", Colors.GREEN))
                            
                            # Special effect for hazmat zombies - toxic gas leak
                            if enemy_subtype == "hazmat":
                                print(Colors.colorize("Toxic gas leaks from the punctured suit!", Colors.GREEN))
                    
                    elif enemy_type == "survivor":
                        if enemy.get("armor", 0) > 0:
                            # Armor-piercing effect against survivors with armor
                            weakness_bonus = 2.0
                            print(Colors.colorize(f"The bolt finds a gap in {enemy['name']}'s armor!", Colors.GREEN))
                    
                    # Marksmanship companions improve critical hit chance
                    base_crit_chance = weapon.get("critical_chance", 0.25)  # Base 25% chance
                    crit_chance_bonus = 0.0
                    
                    if companion_damage_bonus > 1.0 and marksmanship_bonus > 1.0:
                        crit_chance_bonus = 0.25  # +25% crit chance with marksmanship companion
                        print(Colors.colorize("Your companion helps you aim for a vital point!", Colors.GREEN))
                    
                    # Combined critical hit chance
                    crit_chance = min(base_crit_chance + crit_chance_bonus, 0.75)  # Cap at 75% max
                    crit_multiplier = weapon.get("critical_multiplier", 2.0)
                    
                    # Roll for critical hit
                    if random.random() < crit_chance:
                        print(Colors.colorize("CRITICAL HIT! The bolt strikes a vital point!", Colors.RED + Colors.BOLD))
                        # Apply all damage bonuses on critical hit
                        total_damage = int(damage * crit_multiplier * weakness_bonus * marksmanship_bonus * companion_damage_bonus)
                    else:
                        # Regular hit still benefits from marksmanship and companion bonuses
                        total_damage = int(damage * weakness_bonus * marksmanship_bonus * companion_damage_bonus)
                    
                    # Apply damage
                    enemy["health"] -= total_damage
                    print(f"The {enemy['name']} takes {Colors.colorize(str(total_damage), Colors.RED)} damage from the bolt!")
                    
                    # Improved retrievable ammo chance with marksmanship skills
                    base_retrieve_chance = weapon.get("retrievable_ammo", 0.5)
                    retrieve_bonus = 0.0
                    
                    if marksmanship_bonus > 1.0:
                        retrieve_bonus = 0.2  # +20% retrieval chance with marksmanship
                    
                    if companion_damage_bonus > 1.0 and marksmanship_bonus > 1.0:
                        retrieve_bonus += 0.1  # Additional +10% with companion
                    
                    retrieve_chance = min(base_retrieve_chance + retrieve_bonus, 0.9)  # Cap at 90%
                    
                    if enemy["health"] <= 0 and random.random() < retrieve_chance:
                        print(Colors.colorize(f"You were able to retrieve your bolt from the {enemy['name']}'s body.", Colors.GREEN))
                    else:
                        # Use ammo
                        weapon["ammo"] -= 1
                        print(Colors.colorize(f"Bolts remaining: {weapon['ammo']}/{weapon['max_ammo']}", Colors.YELLOW))
                    
                    # Silent weapon - less chance of attracting more enemies
                    if weapon.get("silent", False) and random.random() < 0.9:
                        print(Colors.colorize("The silent attack doesn't attract any additional attention.", Colors.GREEN))
                    
                    # Skip to enemy's attack if not defeated
                    if enemy["health"] <= 0:
                        self.end_combat(True)
                        return
                        
            # Handle riot shield (defensive weapon with less damage but defense bonus)
            elif weapon_id == "riot_shield":
                print(Colors.colorize(f"You bash forward with your {weapon['name']}!", Colors.CYAN))
                
                # Apply damage
                enemy["health"] -= damage
                print(f"The {enemy['name']} takes {Colors.colorize(str(damage), Colors.RED)} damage!")
                
                # Apply defense bonus for enemy's counterattack
                defense_bonus = weapon.get("defense_bonus", 15)
                print(Colors.colorize(f"You brace behind your shield, reducing incoming damage by {defense_bonus}!", Colors.GREEN))
                
                # Remember the defense bonus for the enemy's attack phase
                self.combat_defense_bonus = defense_bonus
                
                # Skip to enemy's attack if not defeated
                if enemy["health"] <= 0:
                    self.end_combat(True)
                    return

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
                            # Apply companion damage bonus to critical hits
                            total_damage = int(damage * companion_damage_bonus)
                            enemy["health"] -= total_damage
                            print(f"You hit the {enemy['name']} for {Colors.colorize(str(total_damage), Colors.RED)} damage!")

                # Weapon special effects in hardcore mode
                if hardcore_mode and weapon:
                    # Bladed weapons have chance to cause bleeding
                    if weapon.get("id", "") in ["machete", "kitchen_knife"] and random.random() < 0.3:
                        print(Colors.colorize(f"Your {weapon['name']} causes the {enemy_type} to bleed!", Colors.RED))
                        enemy["bleeding"] = True

                    # Blunt weapons have chance to stun
                    if weapon.get("id", "") in ["baseball_bat", "reinforced_bat"] and random.random() < 0.2:
                        print(Colors.colorize(f"Your {weapon['name']} stuns the {enemy_type} temporarily!", Colors.YELLOW))
                        enemy["stunned"] = True
            else:
                print(Colors.colorize(f"You miss the {enemy['name']}!", Colors.YELLOW))

            # Check if enemy is defeated
            if enemy["health"] <= 0:
                self.end_combat(True)
                return

        # Enemy attacks back (unless stunned)
        if hardcore_mode and enemy.get("stunned", False):
            print(Colors.colorize(f"The {enemy_type} is stunned and cannot attack this turn!", Colors.GREEN))
            enemy["stunned"] = False  # Stun wears off after one turn
        else:
            dodge_bonus = 0
            if weapon and weapon.get("reach", 0) > 1:
                dodge_bonus = 0.15  # Harder for enemy to hit you if you have a reach weapon

            # Check if enemy is stunned from riot shield, sonic disruptor, or other sources
            if self.player.get("temp_stun_enemy", False):
                print(Colors.colorize(f"The {enemy['name']} is stunned and cannot attack this turn!", Colors.GREEN))
                # Reset the stun flag after this turn
                self.player["temp_stun_enemy"] = False
                return
                
            # Process experimental weapon status effects
            if "effects" in enemy:
                # Check for stunned effect from sonic disruptor
                if "stunned" in enemy["effects"]:
                    print(Colors.colorize(f"{enemy['name']} is stunned from the sonic disruption and cannot attack this turn!", Colors.CYAN))
                    enemy["effects"]["stunned"]["duration"] -= 1
                    if enemy["effects"]["stunned"]["duration"] <= 0:
                        del enemy["effects"]["stunned"]
                        print(Colors.colorize(f"{enemy['name']}'s neural functions are returning to normal.", Colors.YELLOW))
                    return  # Skip attack entirely
                
                # Apply acid effect damage from chemical thrower
                if "acid" in enemy["effects"]:
                    acid_effect = enemy["effects"]["acid"]
                    acid_damage = acid_effect["damage"]
                    enemy["health"] -= acid_damage
                    print(Colors.colorize(f"The corrosive compounds continue to eat away at {enemy['name']}, causing {acid_damage} damage!", Colors.GREEN))
                    acid_effect["duration"] -= 1
                    if acid_effect["duration"] <= 0:
                        del enemy["effects"]["acid"]
                        print(Colors.colorize("The corrosive compounds have been neutralized.", Colors.YELLOW))
                    # Don't return - acid damage doesn't prevent attack
                
                # Apply frozen effect from cryo rifle (reduces enemy damage and speed)
                if "frozen" in enemy["effects"]:
                    print(Colors.colorize(f"{enemy['name']}'s movements are impaired by ice formations!", Colors.BLUE))
                    enemy["effects"]["frozen"]["duration"] -= 1
                    if enemy["effects"]["frozen"]["duration"] <= 0:
                        del enemy["effects"]["frozen"]
                        print(Colors.colorize(f"The ice encasing {enemy['name']} has melted away.", Colors.YELLOW))
                    else:
                        # Apply speed and damage penalties while frozen
                        hit_chance -= 0.25  # Much harder to hit while frozen
                        # Damage reduction will be applied later when damage is calculated
                
            # Enemy attack chance calculation
            hit_chance = 0.6 + 0.1 * enemy.get("speed", 1) - dodge_bonus

            # Get weather info again to apply to enemy attack
            current_weather = self.player.get("current_weather", "clear")
            weather_info = WEATHER_TYPES.get(current_weather, WEATHER_TYPES["clear"])

            # Weather effects on enemy attacks
            if current_weather == "rainy":
                hit_chance -= 0.07  # Enemies slower in rain
                print(Colors.colorize(f"The rain slows the {enemy['name']}'s movements.", weather_info["color"]))
            elif current_weather == "stormy":
                hit_chance -= 0.12  # Enemies much slower in heavy storm
                print(Colors.colorize(f"The storm severely hampers the {enemy['name']}'s attack.", weather_info["color"]))
            elif current_weather == "foggy":
                hit_chance += 0.1  # Easier for enemies to surprise you in fog
                print(Colors.colorize(f"The fog gives the {enemy['name']} a surprise advantage!", weather_info["color"]))
            elif current_weather == "hot":
                hit_chance += 0.08  # Enemies more aggressive in heat
                print(Colors.colorize(f"The heat makes the {enemy['name']} more aggressive.", weather_info["color"]))
            elif current_weather == "cold":
                hit_chance -= 0.1  # Enemies slower in cold
                print(Colors.colorize(f"The cold weather makes the {enemy['name']} sluggish.", weather_info["color"]))

            # Hardcore mode gives enemies a better chance to hit when player is in bad shape
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
                damage = enemy["damage"]
                
                # Apply damage reduction from frozen effect
                if "effects" in enemy and "frozen" in enemy["effects"]:
                    slow_percent = enemy["effects"]["frozen"].get("slow_percent", 0.5)
                    damage_reduction = int(damage * slow_percent)
                    damage -= damage_reduction
                    print(Colors.colorize(f"The ice formations reduce {enemy['name']}'s attack damage by {damage_reduction}!", Colors.BLUE))

                # Boss enemies in hardcore mode have special abilities
                special_attack = False
                if hardcore_mode and enemy.get("boss", False):
                    # Tank has slam attack
                    if enemy.get("id") == "tank" and random.random() < 0.2:
                        print(Colors.colorize("The Tank performs a devastating slam attack!", Colors.BOLD + Colors.RED))
                        damage = int(damage * 1.5)
                        self.player["stamina"] = max(0, self.player["stamina"] - 20)  # Drains stamina
                        special_attack = True

                        # Chance to cause broken limb
                        if random.random() < 0.3:
                            self.player["broken_limb"] = True
                            print(Colors.colorize("The impact breaks one of your limbs!", Colors.BOLD + Colors.RED))

                    # Screamer has disorienting attack
                    elif enemy.get("id") == "screamer" and random.random() < 0.25:
                        print(Colors.colorize("The Screamer lets out an ear-piercing shriek!", Colors.BOLD + Colors.RED))
                        damage = int(damage * 0.7)  # Less physical damage
                        special_attack = True

                        # Increases insanity
                        insanity_increase = random.randint(5, 15)
                        self.player["insanity"] = min(100, self.player.get("insanity", 0) + insanity_increase)
                        print(Colors.colorize(f"The shriek disturbs your mental state! (+{insanity_increase} insanity)", Colors.MAGENTA))

                    # Boomer has toxic attack
                    elif enemy.get("id") == "boomer" and random.random() < 0.3:
                        print(Colors.colorize("The Boomer vomits toxic bile on you!", Colors.BOLD + Colors.GREEN))
                        damage = int(damage * 0.5)  # Less immediate damage
                        special_attack = True

                        # High chance of infection
                        if random.random() < 0.7:
                            self.player["infected"] = True
                            print(Colors.colorize("The toxic bile infects your wounds!", Colors.RED))

                # Apply defense bonus from riot shield or other sources
                defense_bonus = self.player.get("temp_defense_bonus", 0)
                if defense_bonus > 0:
                    original_damage = damage
                    damage = max(1, damage - defense_bonus)  # Ensure at least 1 damage
                    damage_reduced = original_damage - damage
                    print(Colors.colorize(f"Your defensive equipment absorbs {damage_reduced} damage!", Colors.GREEN))
                
                # Apply military vehicle protection if in a vehicle
                if self.player.get("in_vehicle", False) and self.player.get("current_vehicle"):
                    vehicle = self.player.get("current_vehicle")
                    if vehicle.get("id") in ["humvee", "transport_truck", "apc"]:
                        vehicle_protection = vehicle.get("protection", 0)
                        if vehicle_protection > 0:
                            original_damage = damage
                            damage = max(1, damage - vehicle_protection)  # Ensure at least 1 damage
                            damage_reduced = original_damage - damage
                            print(Colors.colorize(f"Your {vehicle.get('name', 'vehicle')} absorbs {damage_reduced} damage!", Colors.GREEN))

                # Apply damage to player
                self.player["health"] -= damage

                if special_attack:
                    # Already printed special attack messages
                    pass
                else:
                    print(Colors.colorize(f"The {enemy['name']} hits you for {damage} damage!", Colors.RED))

                # Infection chance in hardcore mode (from hostile entities)
                if hardcore_mode and not special_attack and not self.player.get("infected", False):
                    if random.random() < INFECTION_CHANCE:
                        self.player["infected"] = True
                        print(Colors.colorize(f"The {enemy['name']}'s attack has infected you!", Colors.RED))

                # Bleeding chance in hardcore mode
                if hardcore_mode and not self.player.get("bleeding", False):
                    if (enemy.get("id", "") == "hunter" and random.random() < 0.4) or random.random() < 0.15:
                        self.player["bleeding"] = True
                        print(Colors.colorize(f"The {enemy['name']}'s attack has caused you to start bleeding!", Colors.RED))

                # Check if player died
                if self.player["health"] <= 0:
                    self.player["health"] = 0
                    self.end_combat(False)

                    # Record death in death log for hardcore mode
                    if self.player.get("hardcore_mode", False):
                        if self.death_log is None:
                            self.death_log = self.load_death_log()
                        # Get enemy name for death cause
                        enemy_name = enemy.get("name", "Enemy")
                        self.record_death(f"Killed by {enemy_name}")

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
                print(Colors.colorize(f"The {enemy['name']} misses you!", Colors.GREEN))

            # Special enemy effects even on miss (for bosses in hardcore mode)
            if hardcore_mode and enemy.get("boss", False) and enemy.get("id") == "hunter" and random.random() < 0.15:
                print(Colors.colorize("The Hunter's quick movements make it hard to keep your balance.", Colors.YELLOW))
                stamina_loss = random.randint(5, 10)
                self.player["stamina"] = max(0, self.player["stamina"] - stamina_loss)
                print(Colors.colorize(f"You lose {stamina_loss} stamina trying to keep up.", Colors.YELLOW))

        # Display combat status with color
        health_color = Colors.health_color(enemy["health"], enemy["max_health"])
        player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

        enemy_health_text = f"{enemy['health']}/{enemy['max_health']}"
        print(f"\n{enemy['name']} Health: {Colors.colorize(enemy_health_text, health_color)}")

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
        if not self.in_combat or (not hasattr(self, 'current_enemy') and not hasattr(self, 'current_zombie')):
            print(Colors.colorize("You are not in combat.", Colors.YELLOW))
            return

        hardcore_mode = self.player.get("hardcore_mode", False)    
        enemy = self.current_zombie if hasattr(self, 'current_zombie') else self.current_enemy
        
        # Determine enemy type
        enemy_type = "zombie"  # Default
        if "animal" in enemy and enemy["animal"]:
            enemy_type = "animal"
        elif "hostile" in enemy and enemy["hostile"] is True:
            enemy_type = "survivor"
            
        # Default flee chance initialization
        flee_chance = 0.5

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

        # Base flee chance calculation with different formulas based on enemy type
        if enemy_type == "zombie":
            flee_chance = 0.5 - 0.1 * enemy.get("speed", 1) + 0.05 * self.player["level"] - stamina_penalty
            
            # Boss zombies are harder to flee from
            if enemy.get("boss", False):
                flee_chance -= 0.2
                print(Colors.colorize("The powerful zombie makes escape difficult!", Colors.RED))
                
        elif enemy_type == "animal":
            # Animals have different flee mechanics based on type
            animal_type = enemy.get("animal_type", "dog")
            
            # Base animal flee chance
            flee_chance = 0.6 - 0.1 * enemy.get("speed", 1) + 0.05 * self.player["level"] - stamina_penalty
            
            # Adjust based on animal type
            if animal_type in ["bear", "boar"]:
                flee_chance -= 0.15  # Large animals are harder to flee from
                print(Colors.colorize(f"The large {animal_type} makes escape difficult!", Colors.RED))
            elif animal_type in ["wolf", "dog"]:
                flee_chance -= 0.1  # Canines are quick but not as intimidating
                print(Colors.colorize(f"The {animal_type} is quick and might catch you!", Colors.YELLOW))
            elif animal_type in ["rat", "crow"]:
                flee_chance += 0.2  # Small animals are easy to flee from
                print(Colors.colorize(f"The small {animal_type} shouldn't be hard to escape from.", Colors.GREEN))
                
            # Special animal traits affect flee chance
            if "pack_hunter" in enemy and enemy.get("pack_attack", False):
                flee_chance -= 0.1  # Pack animals coordinate to cut off escape
                print(Colors.colorize("The pack is trying to surround you!", Colors.RED))
            if "ambush" in enemy and enemy.get("ambush", False):
                flee_chance -= 0.05  # Ambush predators are good at pursuit
                print(Colors.colorize("The predator is agile in pursuit!", Colors.RED))
                
        elif enemy_type == "survivor": 
            # Survivors have equipment that affects flee chance
            flee_chance = 0.5 - 0.05 * enemy.get("speed", 1) + 0.05 * self.player["level"] - stamina_penalty
            
            # Armed survivors are more dangerous to flee from
            if "weapon" in enemy and enemy["weapon"]:
                weapon_type = enemy["weapon"].get("type", "melee")
                if weapon_type == "ranged":
                    flee_chance -= 0.15  # Ranged weapons make fleeing harder
                    print(Colors.colorize("The survivor has a ranged weapon and might shoot you as you flee!", Colors.RED))
                    
            # Skilled survivors are harder to escape
            if "skills" in enemy and enemy["skills"]:
                if "tracking" in enemy["skills"]:
                    flee_chance -= 0.1
                    print(Colors.colorize("The survivor has tracking skills!", Colors.RED))
                if "marksmanship" in enemy["skills"]:
                    flee_chance -= 0.05
                    print(Colors.colorize("The survivor is an excellent marksman!", Colors.RED))

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
            # Different success messages based on enemy type
            if enemy_type == "zombie":
                print(Colors.colorize("\nYou successfully escape from the zombie!", Colors.GREEN))
            elif enemy_type == "animal":
                animal_type = enemy.get("animal_type", "animal")
                print(Colors.colorize(f"\nYou successfully escape from the {animal_type}!", Colors.GREEN))
            elif enemy_type == "survivor":
                print(Colors.colorize("\nYou successfully escape from the hostile survivor!", Colors.GREEN))

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

            # Enemy gets a more powerful attack due to failed escape
            damage = enemy["damage"]
            
            # Different failure messages and effects based on enemy type
            if enemy_type == "zombie":
                # In hardcore mode, failed escapes are more dangerous
                if hardcore_mode:
                    damage_modifier = 1.25  # 25% more damage on failed escape
                    damage = int(damage * damage_modifier)
                    print(Colors.colorize("The zombie catches you from behind as you try to run!", Colors.RED))
                else:
                    print(Colors.colorize("The zombie lunges at you as you turn to run!", Colors.RED))
                
                # Apply damage to player
                self.player["health"] -= damage
                print(Colors.colorize(f"The {enemy['name']} hits you for {damage} damage!", Colors.RED))
                
                # Special effects on failed escape in hardcore mode (zombie-specific)
                if hardcore_mode:
                    # Higher infection chance when caught fleeing
                    if not self.player.get("infected", False) and random.random() < INFECTION_CHANCE * 1.5:
                        self.player["infected"] = True
                        print(Colors.colorize("The enemy's attack has infected you!", Colors.RED))
                    
                    # Higher bleeding chance when caught fleeing
                    if not self.player.get("bleeding", False) and random.random() < 0.25:
                        self.player["bleeding"] = True
                        print(Colors.colorize("The enemy's attack has caused you to start bleeding!", Colors.RED))
                        
            elif enemy_type == "animal":
                animal_type = enemy.get("animal_type", "animal")
                
                # Different attack messages based on animal type
                if animal_type in ["bear", "boar"]:
                    # Large animals hit harder when you're running
                    damage_modifier = 1.3
                    damage = int(damage * damage_modifier)
                    print(Colors.colorize(f"The {animal_type} charges at you as you try to escape!", Colors.RED))
                elif animal_type in ["wolf", "dog"]:
                    print(Colors.colorize(f"The {animal_type} leaps at your legs as you turn to run!", Colors.RED))
                else:
                    print(Colors.colorize(f"The {animal_type} catches you as you try to escape!", Colors.RED))
                
                # Apply damage to player
                self.player["health"] -= damage
                print(Colors.colorize(f"The {enemy['name']} hits you for {damage} damage!", Colors.RED))
                
                # Special effects for animals
                if hardcore_mode and animal_type in ["wolf", "bear"] and not self.player.get("bleeding", False):
                    if random.random() < 0.3:  # 30% chance of bleeding from predator attack
                        self.player["bleeding"] = True
                        print(Colors.colorize(f"The {animal_type}'s attack has caused you to start bleeding!", Colors.RED))
                        
            elif enemy_type == "survivor":
                # Survivor attack mechanics
                if "weapon" in enemy and enemy["weapon"]:
                    weapon_type = enemy["weapon"].get("type", "melee")
                    weapon_name = enemy["weapon"].get("name", "weapon")
                    
                    if weapon_type == "ranged" and random.random() < 0.4:  # 40% chance of getting shot while fleeing
                        # Ranged weapons do more damage when fleeing
                        damage_modifier = 1.5
                        damage = int(damage * damage_modifier)
                        print(Colors.colorize(f"The survivor shoots you with their {weapon_name} as you run away!", Colors.RED))
                    else:
                        print(Colors.colorize(f"The survivor strikes you with their {weapon_name} as you try to escape!", Colors.RED))
                else:
                    print(Colors.colorize("The survivor lunges at you as you try to escape!", Colors.RED))
                
                # Apply damage to player
                self.player["health"] -= damage
                print(Colors.colorize(f"The hostile survivor hits you for {damage} damage!", Colors.RED))
                
                # Special effects for survivors
                if hardcore_mode and "weapon" in enemy and enemy["weapon"]:
                    weapon_damage_type = enemy["weapon"].get("damage_type", "blunt")
                    if weapon_damage_type == "piercing" and not self.player.get("bleeding", False):
                        if random.random() < 0.2:  # 20% chance of bleeding from piercing weapons
                            self.player["bleeding"] = True
                            print(Colors.colorize("The survivor's attack has caused you to start bleeding!", Colors.RED))

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
                    
                    # Get appropriate death message based on enemy type
                    enemy_name = enemy.get("name", "enemy")
                    
                    if enemy_type == "zombie":
                        death_cause = f"Killed while fleeing from {enemy_name}"
                    elif enemy_type == "animal":
                        animal_type = enemy.get("animal_type", "animal")
                        death_cause = f"Killed while fleeing from a {animal_type}"
                    elif enemy_type == "survivor":
                        death_cause = f"Killed while fleeing from a hostile survivor ({enemy_name})"
                    else:
                        death_cause = f"Killed while fleeing from {enemy_name}"
                        
                    self.record_death(death_cause)

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

                # Different death messages based on enemy type
                if enemy_type == "zombie":
                    print(Colors.colorize("\n💀 You have died while trying to escape from the zombie... Game over.", Colors.BOLD + Colors.RED))
                elif enemy_type == "animal":
                    animal_type = enemy.get("animal_type", "animal")
                    print(Colors.colorize(f"\n💀 You have died while trying to escape from the {animal_type}... Game over.", Colors.BOLD + Colors.RED))
                elif enemy_type == "survivor":
                    print(Colors.colorize("\n💀 You have died while trying to escape from the hostile survivor... Game over.", Colors.BOLD + Colors.RED))
                else:
                    print(Colors.colorize("\n💀 You have died while trying to escape... Game over.", Colors.BOLD + Colors.RED))
                    
                self.end_combat(False)
                self.game_running = False
                return

            # Display combat status with color based on enemy type
            health_color = Colors.health_color(enemy["health"], enemy["max_health"])
            player_health_color = Colors.health_color(self.player["health"], self.player["max_health"])

            # Display appropriate enemy health information
            enemy_health_text = f"{enemy['health']}/{enemy['max_health']}"
            
            if enemy_type == "zombie":
                print(f"\nZombie Health: {Colors.colorize(enemy_health_text, health_color)}")
            elif enemy_type == "animal":
                animal_type = enemy.get("animal_type", "animal")
                print(f"\n{animal_type.capitalize()} Health: {Colors.colorize(enemy_health_text, health_color)}")
            elif enemy_type == "survivor":
                print(f"\nHostile Survivor Health: {Colors.colorize(enemy_health_text, health_color)}")
            else:
                print(f"\nEnemy Health: {Colors.colorize(enemy_health_text, health_color)}")

            # Display player health
            player_health_text = f"{self.player['health']}/{self.player['max_health']}"
            print(f"Your Health: {Colors.colorize(player_health_text, player_health_color)}")

            # Display additional info in hardcore mode
            if hardcore_mode:
                # Stamina
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
                    
                # Enemy-specific status displays
                if enemy_type == "zombie" and enemy.get("special_abilities", []):
                    abilities = ", ".join(enemy["special_abilities"])
                    print(f"Zombie Abilities: {Colors.colorize(abilities, Colors.RED)}")
                elif enemy_type == "animal" and enemy.get("pack_attack", False):
                    print(f"Animal Trait: {Colors.colorize('Pack Hunter', Colors.RED)}")
                elif enemy_type == "survivor" and "skills" in enemy:
                    skills = ", ".join(enemy["skills"])
                    print(f"Survivor Skills: {Colors.colorize(skills, Colors.YELLOW)}")

            # Fleeing takes time (medium action)
            self.advance_time("medium_action")

    def end_combat(self, victory):
        """End combat state and apply results."""
        self.in_combat = False
        
        if (not hasattr(self, 'current_zombie') and not hasattr(self, 'current_enemy')) or (hasattr(self, 'current_zombie') and not self.current_zombie) or (hasattr(self, 'current_enemy') and not self.current_enemy):
            return

        # Determine enemy type
        enemy = self.current_zombie if hasattr(self, 'current_zombie') else self.current_enemy
        enemy_type = "zombie"  # Default
        if "animal" in enemy and enemy["animal"]:
            enemy_type = "animal"
        elif "hostile" in enemy and enemy["hostile"] is True:
            enemy_type = "survivor"

        if victory:
            # Base XP gain is influenced by enemy's stats
            xp_gain = 20 + 10 * enemy.get("speed", 1)
            
            # Different victory messages and rewards based on enemy type
            if enemy_type == "zombie":
                # Special enemy types give more XP
                enemy_subtype = enemy.get("type") if enemy else None
                if enemy_subtype == "stalker":
                    xp_gain += 15  # Forest stalkers are worth more XP

                print(f"\nYou defeated the {enemy['name']}!")
                print(f"Gained {xp_gain} XP!")

                self.player["xp"] += xp_gain
                
                # Track enemy kills by type
                if "zombies_killed" not in self.player:
                    self.player["zombies_killed"] = 0
                self.player["zombies_killed"] += 1

                # Check for mission progress related to killing specific enemy types
                self.check_mission_progress("kill", enemy)

                # Chance to find items depends on enemy type
                loot_chance = 0.3  # Base 30% chance

                # Special enemy types have better loot
                if enemy.get("type") == "brute":
                    loot_chance = 0.5  # Brutes have more loot
                elif enemy.get("type") == "stalker":
                    loot_chance = 0.6  # Forest stalkers have the best loot chance

                if random.random() < loot_chance:
                    # Different enemy types tend to have different loot
                    item_types = ["food", "medical", "material"]

                    # Forest stalkers might drop crafting materials
                    if enemy.get("type") == "stalker":
                        item_types = ["material", "material", "food", "medical"]  # Weight toward materials

                    item_type = random.choice(item_types)

                    matching_items = [item_id for item_id, item in ITEMS.items() 
                                    if item["type"] == item_type]

                    if matching_items:
                        found_item_id = random.choice(matching_items)
                        found_item = ITEMS[found_item_id]

                        # Add item to inventory
                        if self.add_to_inventory(found_item_id):
                            if enemy_type == "zombie":
                                print(f"You found {found_item['name']} on the zombie!")
                            elif enemy_type == "animal":
                                print(f"You found {found_item['name']} near the defeated {enemy['name']}!")
                            elif enemy_type == "survivor":
                                print(f"You found {found_item['name']} in the survivor's belongings!")
                            else:
                                print(f"You found {found_item['name']} on the enemy!")
                
            elif enemy_type == "animal":
                # Animal victory
                xp_gain += 10  # Animals give slightly more XP than regular zombies
                
                # Bigger animals give more XP
                animal_type = enemy.get("animal_type", "dog")
                if animal_type in ["bear", "boar"]:
                    xp_gain += 20  # Dangerous large animals worth more XP
                
                print(f"\nYou defeated the {enemy['name']}!")
                print(f"Gained {xp_gain} XP!")
                
                self.player["xp"] += xp_gain
                
                # Track animal kills
                if "animals_killed" not in self.player:
                    self.player["animals_killed"] = 0
                self.player["animals_killed"] += 1
                
                # Check for mission progress
                self.check_mission_progress("kill_animal", animal_type)
                
                # Animal loot - meat, hide, etc.
                if random.random() < 0.7:  # 70% chance to get animal loot
                    animal_loot = {
                        "dog": ["raw_meat"],
                        "wolf": ["raw_meat", "wolf_pelt"],
                        "bear": ["raw_meat", "bear_pelt", "bear_claw"],
                        "deer": ["raw_meat", "deer_hide", "antlers"],
                        "boar": ["raw_meat", "boar_tusk"],
                        "rat": ["raw_meat"],
                        "crow": ["feathers"]
                    }
                    
                    if animal_type in animal_loot:
                        loot_options = animal_loot[animal_type]
                        loot = random.choice(loot_options)
                        
                        # Add to inventory
                        if self.add_to_inventory(loot):
                            print(Colors.colorize(f"You harvested: {ITEMS.get(loot, {'name': loot})['name']}", Colors.YELLOW))
                
            elif enemy_type == "survivor":
                # Survivor victory
                xp_gain += 25  # Survivors give more XP than zombies or animals
                
                # Skilled survivors give more XP
                if "skills" in enemy and enemy["skills"]:
                    xp_gain += 5 * len(enemy["skills"])
                
                print(f"\nYou defeated the hostile survivor {enemy['name']}!")
                print(f"Gained {xp_gain} XP!")
                
                self.player["xp"] += xp_gain
                
                # Track survivor kills
                if "survivors_killed" not in self.player:
                    self.player["survivors_killed"] = 0
                self.player["survivors_killed"] += 1
                
                # Check for mission progress
                self.check_mission_progress("kill_survivor", "hostile")
                
                # Survivor loot - weapons, supplies, etc.
                print(Colors.colorize("You search the survivor's belongings:", Colors.YELLOW))
                
                # Get survivor equipment and add to inventory with chances
                loot_found = False
                
                # Weapon loot
                if "weapon" in enemy and enemy["weapon"] and random.random() < 0.4:
                    weapon_id = enemy["weapon"].get("id", "knife")
                    if self.add_to_inventory(weapon_id):
                        print(Colors.colorize(f"- {ITEMS.get(weapon_id, {'name': weapon_id})['name']}", Colors.YELLOW))
                        loot_found = True
                    
                    # Ammo for ranged weapons
                    if "ammo" in enemy["weapon"] and enemy["weapon"]["ammo"] > 0 and random.random() < 0.6:
                        ammo_amount = random.randint(1, enemy["weapon"]["ammo"])
                        ammo_id = enemy["weapon"].get("ammo_type", "pistol_ammo")
                        for _ in range(ammo_amount):
                            self.add_to_inventory(ammo_id)
                        print(Colors.colorize(f"- {ammo_amount}x {ITEMS.get(ammo_id, {'name': ammo_id})['name']}", Colors.YELLOW))
                
                # Supply loot
                standard_supplies = ["bandage", "painkillers", "canned_food", "water_bottle", "lighter"]
                for _ in range(random.randint(0, 2)):
                    if random.random() < 0.5:
                        supply = random.choice(standard_supplies)
                        if self.add_to_inventory(supply):
                            print(Colors.colorize(f"- {ITEMS.get(supply, {'name': supply})['name']}", Colors.YELLOW))
                            loot_found = True
                
                if not loot_found:
                    print(Colors.colorize("Nothing useful found.", Colors.YELLOW))
            
            # Check for level up for all enemy types
            self.level_up()
                        
            # Handle recovered crossbow bolts if player was victorious
            if self.player.get("temp_recovered_bolts", 0) > 0:
                recovered_bolts = self.player.get("temp_recovered_bolts", 0)
                print(Colors.colorize(f"You recover {recovered_bolts} crossbow bolt(s) from the battlefield.", Colors.GREEN))
                
                # Find carbon-fiber bolts in inventory and add the recovered bolts
                bolt_found = False
                for item_idx, item in enumerate(self.player["inventory"]):
                    if item.get("id") == "carbon_fiber_bolts":
                        bolt_found = True
                        self.player["inventory"][item_idx]["count"] += recovered_bolts
                        break
                
                # If player doesn't have the bolts item, add it to inventory
                if not bolt_found:
                    self.add_to_inventory("carbon_fiber_bolts", recovered_bolts)
                
                # Reset the recovered bolts counter
                self.player["temp_recovered_bolts"] = 0
            
            # Handle attracted zombies from loud weapons - all enemy types can attract zombies
            if self.player.get("attracted_zombies", False):
                # Reset the flag
                self.player["attracted_zombies"] = False
                
                # 30% chance of immediate followup encounter
                if random.random() < 0.3:
                    print(Colors.colorize("\nThe sound of combat has attracted zombies!", Colors.RED))
                    print("Prepare for another encounter!")
                    
                    # Force a new encounter after a short pause
                    time.sleep(1.5)
                    self.spawn_zombie()  # Create a new zombie
                    self.start_combat()  # Start combat with the new zombie
                    return
        else:
            # Player was defeated
            print(Colors.colorize("\nYou have been defeated!", Colors.RED))
            
            # Different defeat messages based on enemy type
            if enemy_type == "zombie":
                print(Colors.colorize("You were overwhelmed by the zombie!", Colors.RED + Colors.BOLD))
            elif enemy_type == "animal":
                animal_type = enemy.get("animal_type", "animal")
                print(Colors.colorize(f"The {animal_type} was too much for you to handle!", Colors.RED + Colors.BOLD))
            elif enemy_type == "survivor":
                print(Colors.colorize("The hostile survivor got the better of you!", Colors.RED + Colors.BOLD))
                
            # Record death in hardcore mode with proper cause
            if self.player.get("hardcore_mode", False):
                if self.death_log is None:
                    self.death_log = self.load_death_log()
                enemy_name = enemy.get("name", "enemy")
                self.record_death(f"Killed by {enemy_name}")

        # Reset combat state and temporary combat attributes
        self.current_zombie = None
        if hasattr(self, 'current_enemy'):
            self.current_enemy = None
        self.player["temp_defense_bonus"] = 0
        self.player["temp_stun_enemy"] = False

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
                for _, item in enumerate(inventory_copy):  # Using _ instead of idx as it's not used
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
                self.current_zombie = self.spawn_zombie(specific_type=special_type)
                self.current_enemy = self.current_zombie  # Set both references for consistency
            else:
                # Regular zombie
                self.current_zombie = self.spawn_zombie()
                self.current_enemy = self.current_zombie  # Set both references for consistency

            self.start_combat()
            return  # Exit scavenging function while in combat

        # If no zombie encounter, find items
        found_something = False

        # Determine how many items to potentially find (1-3, more in later rounds)
        potential_items = min(3, 1 + self.current_scavenging['round'] // 2)

        # For each potential item slot
        for _ in range(potential_items):  # Using _ since the index isn't used
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
            
    def generate_random_name(self):
        """Generate a random name for survivors.
        
        Returns:
            str: A randomly generated full name with cultural consistency
        """
        # Pick a random cultural group to ensure first/last name consistency
        cultures = ["western", "middle_eastern", "east_asian", "latin_american", 
                    "south_asian", "eastern_european", "african"]
        
        selected_culture = random.choice(cultures)
        
        # Get all first names from the selected culture
        first_names_for_culture = []
        last_names_for_culture = []
        
        # Find the indices of this culture's names in the list
        # (names are organized with a comment like "# Western names" before each group)
        first_name_indices = []
        last_name_indices = []
        
        # Map cultural identifier to the comment strings in the list
        culture_comment_map = {
            "western": "# Western names",
            "middle_eastern": "# Middle Eastern names",
            "east_asian": "# East Asian names",
            "latin_american": "# Latin American names",
            "south_asian": "# South Asian names",
            "eastern_european": "# Eastern European names",
            "african": "# African names"
        }
        
        culture_surname_comment_map = {
            "western": "# Western surnames",
            "middle_eastern": "# Middle Eastern surnames",
            "east_asian": "# East Asian surnames",
            "latin_american": "# Latin American surnames",
            "south_asian": "# South Asian surnames",
            "eastern_european": "# Eastern European surnames",
            "african": "# African surnames"
        }
        
        # Find the range of first names for this culture
        found_culture = False
        for i, name in enumerate(SURVIVOR_FIRST_NAMES):
            if isinstance(name, str) and name.startswith("#") and selected_culture in name.lower():
                found_culture = True
                continue
                
            if found_culture and isinstance(name, str) and name.startswith("#"):
                # We've hit the next culture's comment
                break
                
            if found_culture:
                first_names_for_culture.append(name)
        
        # Find the range of last names for this culture
        found_culture = False
        for i, name in enumerate(SURVIVOR_LAST_NAMES):
            if isinstance(name, str) and name.startswith("#") and selected_culture in name.lower():
                found_culture = True
                continue
                
            if found_culture and isinstance(name, str) and name.startswith("#"):
                # We've hit the next culture's comment
                break
                
            if found_culture:
                last_names_for_culture.append(name)
        
        # If we couldn't find matching names for some reason (should never happen),
        # fall back to the old random method
        if not first_names_for_culture or not last_names_for_culture:
            first_name = random.choice(SURVIVOR_FIRST_NAMES)
            last_name = random.choice(SURVIVOR_LAST_NAMES)
        else:
            first_name = random.choice(first_names_for_culture)
            last_name = random.choice(last_names_for_culture)
            
        return f"{first_name} {last_name}"
        
    def spawn_survivor(self, specific_type=None):
        """Create a random survivor based on location.
        
        Args:
            specific_type: Optional specific survivor type to spawn
            
        Returns:
            dict: A survivor instance with randomized attributes
        """
        location = LOCATIONS[self.player["location"]]
        
        # Determine survivor type
        if specific_type and specific_type in SURVIVOR_TYPES:
            survivor_type = specific_type
        else:
            # Higher chance of hostile survivors in dangerous areas
            danger_level = location["danger_level"]
            hostile_chance = min(0.2 + (danger_level * 0.1), 0.7)  # 20-70% chance based on danger
            
            if random.random() < hostile_chance:
                survivor_type = "hostile_bandit"
            else:
                non_hostile_types = [s_type for s_type, data in SURVIVOR_TYPES.items() 
                                    if not data.get("hostile", False)]
                survivor_type = random.choice(non_hostile_types)
        
        # Base survivor from template
        survivor_template = SURVIVOR_TYPES[survivor_type].copy()
        survivor = {
            "id": f"survivor_{int(time.time())}_{random.randint(1000, 9999)}", # Unique ID
            "type": survivor_type,
            "name": self.generate_random_name(),
            "base_type": survivor_template["name"],
            "description": survivor_template["description"],
            "hostile": survivor_template.get("hostile", False),
            "trader": survivor_template.get("trader", False),
            "cautious": survivor_template.get("cautious", False)
        }
        
        # Randomize stats within ranges
        health_range = survivor_template.get("health_range", [70, 100])
        damage_range = survivor_template.get("damage_range", [10, 20])
        speed_range = survivor_template.get("speed_range", [0.8, 1.2])
        
        survivor["health"] = random.randint(health_range[0], health_range[1])
        survivor["max_health"] = survivor["health"]
        survivor["damage"] = random.randint(damage_range[0], damage_range[1])
        survivor["speed"] = round(random.uniform(speed_range[0], speed_range[1]), 1)
        
        # Equipment and skills
        survivor["equipped_weapon"] = None
        survivor["skills"] = []
        
        if "skill_potential" in survivor_template:
            potential_skills = survivor_template["skill_potential"]
            # Give the survivor 1-2 skills from their potential list
            num_skills = random.randint(1, min(2, len(potential_skills)))
            survivor["skills"] = random.sample(potential_skills, num_skills)
        
        # Determine loot quality
        survivor["loot_quality"] = survivor_template.get("loot_quality", "low")
        
        # Dialogue options
        survivor["dialogue"] = survivor_template.get("dialogue", {})
        
        # Recruitment difficulty
        survivor["recruit_difficulty"] = survivor_template.get("recruit_difficulty", "hard")
        
        return survivor

    def spawn_animal(self, is_friendly=None, specific_type=None):
        """Create a random animal based on location.
        
        Args:
            is_friendly: Override to spawn a friendly or hostile animal
            specific_type: Optional specific animal type to spawn
            
        Returns:
            dict: An animal instance with attributes
        """
        location = LOCATIONS[self.player["location"]]
        
        # Check if this location has specific animal types
        location_animals = location.get("animal_types", [])
        
        # Determine if friendly or infected
        if is_friendly is None:
            # Use location's default (if specified)
            if location.get("friendly_animals", False):
                is_friendly = True
            elif location.get("infected_animals", False):
                is_friendly = False
            else:
                # Default behavior: 30% chance of friendly animals
                is_friendly = random.random() < 0.3
        
        # Select animal type
        if specific_type:
            if is_friendly and specific_type in FRIENDLY_ANIMALS:
                animal_type = specific_type
            elif not is_friendly and specific_type in INFECTED_ANIMALS:
                animal_type = specific_type
            else:
                # Fallback if specified type doesn't match friendly/hostile status
                animal_type = self._select_random_animal_type(is_friendly, location_animals)
        else:
            animal_type = self._select_random_animal_type(is_friendly, location_animals)
        
        # Get the template
        if is_friendly:
            animal_template = FRIENDLY_ANIMALS[animal_type].copy()
        else:
            animal_template = INFECTED_ANIMALS[animal_type].copy()
        
        # Create the animal instance
        animal = animal_template.copy()
        animal["id"] = f"animal_{int(time.time())}_{random.randint(1000, 9999)}"  # Unique ID
        
        # Some variation in health/damage for variety
        animal["health"] = int(animal["health"] * random.uniform(0.9, 1.1))
        animal["max_health"] = animal["health"]
        animal["damage"] = int(animal["damage"] * random.uniform(0.9, 1.1))
        
        # Add any special behavior based on the animal type
        if not is_friendly and animal.get("pack_hunter", False):
            # Pack hunters have a chance to call others of their kind
            animal["calls_pack"] = True
            animal["pack_size"] = random.randint(2, 4)
        
        return animal
    
    def _select_random_animal_type(self, is_friendly, location_animals):
        """Helper function to select a random animal type.
        
        Args:
            is_friendly: Whether to select a friendly animal
            location_animals: List of animal types available in this location
            
        Returns:
            str: Animal type ID
        """
        # Filter animals based on the location's available types (if specified)
        if location_animals:
            if is_friendly:
                available_types = [animal for animal in location_animals 
                                 if animal in FRIENDLY_ANIMALS]
                if not available_types:  # Fallback if no matching friendly animals
                    available_types = list(FRIENDLY_ANIMALS.keys())
            else:
                available_types = [animal for animal in location_animals 
                                 if animal in INFECTED_ANIMALS]
                if not available_types:  # Fallback if no matching infected animals
                    available_types = list(INFECTED_ANIMALS.keys())
        else:
            # No location-specific animals, use all available
            if is_friendly:
                available_types = list(FRIENDLY_ANIMALS.keys())
            else:
                available_types = list(INFECTED_ANIMALS.keys())
        
        return random.choice(available_types)
    
    def encounter_survivor(self):
        """Handle an encounter with another survivor.
        
        Returns:
            bool: True if combat started, False otherwise
        """
        survivor = self.spawn_survivor()
        
        print("\n" + Colors.colorize("="*50, Colors.YELLOW))
        print(Colors.colorize("SURVIVOR ENCOUNTER", Colors.YELLOW + Colors.BOLD))
        print(Colors.colorize("="*50, Colors.YELLOW))
        
        # Display survivor info
        print(f"You encounter {survivor['name']}, a {survivor['base_type']}.")
        print(f"{survivor['description']}")
        
        # Randomly select a greeting dialogue
        if "greeting" in survivor["dialogue"]:
            greeting = random.choice(survivor["dialogue"]["greeting"])
            print(f"\n{survivor['name']} says: \"{greeting}\"")
        
        # Handle hostile survivors differently
        if survivor["hostile"]:
            print(Colors.colorize("\nThis survivor seems hostile and is preparing to attack!", Colors.RED))
            
            # Give player a chance to avoid combat with charisma
            if "charisma" in self.player.get("skills", []) and random.random() < 0.4:
                print(Colors.colorize("Your charisma helps you de-escalate the situation.", Colors.GREEN))
                print(f"{survivor['name']} lowers their weapon and backs away cautiously.")
                return False
            
            print("\nThe hostile survivor attacks!")
            
            # Add survivor to current combat enemy
            self.current_zombie = survivor  # Set as current enemy
            self.current_enemy = survivor   # Set both references for consistency
            self.start_combat()
            return True
        
        # For non-hostile survivors, give interaction options
        print("\nHow do you want to interact?")
        print("1. Approach peacefully")
        print("2. Offer to trade")
        print("3. Try to recruit them")
        print("4. Keep your distance and move on")
        print("5. Attack")
        
        choice = input("> ")
        
        if choice == "1":
            # Peaceful approach
            print("\nYou approach with your hands visible, showing you mean no harm.")
            if survivor["cautious"] and random.random() < 0.3:
                print(f"{survivor['name']} remains wary but shares some information with you.")
                self.peaceful_survivor_interaction(survivor)
            else:
                print(f"{survivor['name']} seems relieved to meet another friendly face.")
                if "friendly" in survivor["dialogue"]:
                    friendly_line = random.choice(survivor["dialogue"]["friendly"])
                    print(f"\n{survivor['name']} says: \"{friendly_line}\"")
                self.peaceful_survivor_interaction(survivor)
        
        elif choice == "2":
            # Trading
            if survivor["trader"] or random.random() < 0.4:
                print(f"\n{survivor['name']} agrees to trade with you.")
                self.trade_with_survivor(survivor)
            else:
                print(f"\n{survivor['name']} doesn't have anything to trade.")
                self.peaceful_survivor_interaction(survivor)
        
        elif choice == "3":
            # Recruitment attempt
            self.try_recruit_survivor(survivor)
        
        elif choice == "4":
            # Move on
            print("\nYou decide it's safer to keep your distance and continue on your way.")
            print(f"{survivor['name']} watches you leave, then disappears into the ruins.")
        
        elif choice == "5":
            # Attack (turn a non-hostile encounter hostile)
            print("\nYou decide to attack the survivor, catching them by surprise!")
            self.current_zombie = survivor  # Set the enemy to the survivor
            self.current_enemy = survivor   # Set both references for consistency
            self.start_combat()
            return True
        
        else:
            print("\nYou hesitate, unsure how to respond.")
            print(f"{survivor['name']} gives you a cautious nod and continues on their way.")
        
        return False
    
    def peaceful_survivor_interaction(self, survivor):
        """Handle peaceful interaction with a non-hostile survivor.
        
        Args:
            survivor: The survivor data
        """
        # Chance to give player useful information
        print("\nYou exchange stories about surviving in this harsh world.")
        
        info_types = [
            ("location", "tells you about a nearby location that might have supplies"),
            ("zombie", "warns you about a dangerous zombie type in the area"),
            ("safe_spot", "shares the location of a relatively safe place to rest"),
            ("crafting", "gives you a tip about crafting something useful")
        ]
        
        info_type, desc = random.choice(info_types)
        print(f"{survivor['name']} {desc}.")
        
        if info_type == "location":
            # Reveal a random location on the map
            unknown_locations = [loc for loc in LOCATIONS.keys() 
                               if loc != "camp" and loc not in self.player["discovered_locations"]]
            if unknown_locations:
                new_loc = random.choice(unknown_locations)
                self.player["discovered_locations"].append(new_loc)
                print(Colors.colorize(f"You've discovered {LOCATIONS[new_loc]['name']}!", Colors.GREEN))
        
        elif info_type == "zombie":
            zombie_types = list(ZOMBIE_TYPES.keys())
            zombie_type = random.choice(zombie_types)
            zombie_info = ZOMBIE_TYPES[zombie_type]
            print(f"They describe the {zombie_info['name']} - {zombie_info['description'][:100]}...")
            if "weakness" in zombie_info:
                print(Colors.colorize(f"Importantly, they mention it has a weakness to {zombie_info['weakness']}.", Colors.GREEN))
        
        elif info_type == "safe_spot":
            # Increase sleep safety temporarily at current location
            self.player["temporary_sleep_bonus"] = 0.2
            print(Colors.colorize("Your next rest will be 20% safer thanks to this information.", Colors.GREEN))
        
        elif info_type == "crafting":
            # Instead of revealing a recipe, just give general crafting advice
            crafting_tips = [
                "You can create improvised weapons by combining everyday items with tape and tools.",
                "Food preservation techniques can help food last longer during your journeys.",
                "Scrap electronics are useful for crafting advanced items like radios or sensors.",
                "Medical supplies can be crafted from common plants if you know what to look for.",
                "Reinforcing your armor with materials from car parts can provide extra protection.",
                "Makeshift traps can be created using scrap materials and basic mechanics."
            ]
            
            print(Colors.colorize(f"They share some crafting advice: {random.choice(crafting_tips)}", Colors.GREEN))
    
    def trade_with_survivor(self, survivor):
        """Trading interface with a survivor.
        
        Args:
            survivor: The survivor data
        """
        print("\n" + Colors.colorize("="*50, Colors.CYAN))
        print(Colors.colorize("TRADING", Colors.CYAN + Colors.BOLD))
        print(Colors.colorize("="*50, Colors.CYAN))
        
        # Generate a small selection of items based on survivor type and loot quality
        item_count = random.randint(3, 6)
        quality = survivor["loot_quality"]
        
        if quality == "low":
            item_chance = {"common": 0.7, "uncommon": 0.25, "rare": 0.05}
        elif quality == "medium":
            item_chance = {"common": 0.4, "uncommon": 0.5, "rare": 0.1}
        else:  # high
            item_chance = {"common": 0.2, "uncommon": 0.6, "rare": 0.2}
        
        # Trader specialization based on survivor type
        if survivor["type"] == "friendly_trader":
            # Broad selection
            item_types = ["weapon", "medical", "food", "materials", "tool"]
        elif survivor["type"] == "military_veteran":
            # Military focus
            item_types = ["weapon", "medical", "military_gear"]
        elif survivor["type"] == "skilled_hunter":
            # Survival focus
            item_types = ["weapon", "food", "materials", "tool"]
        elif survivor["type"] == "engineering_expert":
            # Technical focus
            item_types = ["tool", "materials", "electronics"]
        else:
            # Default mix
            item_types = ["weapon", "medical", "food", "materials"]
        
        # Generate items
        trade_items = []
        for _ in range(item_count):
            rarity = random.choices(list(item_chance.keys()), 
                                   weights=list(item_chance.values()))[0]
            
            # Get items matching type and rarity
            matching_items = [item_id for item_id, item in ITEMS.items()
                             if item.get("rarity", "common") == rarity and
                                item.get("type") in item_types]
            
            if matching_items:
                item_id = random.choice(matching_items)
                price = ITEMS[item_id].get("value", 10) * 1.5  # Markup
                trade_items.append((item_id, int(price)))
        
        # Display trade items
        print(f"{survivor['name']} offers these items for trade:")
        for i, (item_id, price) in enumerate(trade_items, 1):
            item = ITEMS[item_id]
            print(f"{i}. {item['name']} - {price} supplies")
        
        print(f"\nYou have {self.player['supplies']} supplies.")
        print("Enter the number of the item you want to buy, or 0 to exit.")
        
        while True:
            choice = input("> ")
            if choice == "0" or choice.lower() == "exit":
                print("\nYou end the trading session.")
                break
            
            try:
                choice = int(choice)
                if 1 <= choice <= len(trade_items):
                    item_id, price = trade_items[choice-1]
                    if self.player['supplies'] >= price:
                        # Purchase the item
                        self.player['supplies'] -= price
                        self.add_to_inventory(item_id)
                        print(Colors.colorize(f"You purchased {ITEMS[item_id]['name']} for {price} supplies.", Colors.GREEN))
                        print(f"You have {self.player['supplies']} supplies remaining.")
                    else:
                        print(Colors.colorize("You don't have enough supplies for that item.", Colors.RED))
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a number.")
    
    def try_recruit_survivor(self, survivor):
        """Attempt to recruit a survivor to join your group.
        
        Args:
            survivor: The survivor data
            
        Returns:
            bool: True if recruitment successful, False otherwise
        """
        # Check if already at max companions (2 active companions)
        active_companions = [c for c in self.player.get("companions", []) 
                            if c.get("status", "active") == "active"]
        if len(active_companions) >= 2:
            print(Colors.colorize("You can't recruit any more companions. You already have the maximum of 2 active companions in your group.", Colors.RED))
            print("You need to dismiss one of your current companions before recruiting someone new.")
            return False
            
        print(f"\nYou ask {survivor['name']} if they'd like to join your group.")
        
        # Determine difficulty based on survivor type
        difficulty = survivor["recruit_difficulty"]
        
        if difficulty == "easy":
            base_chance = 0.7
        elif difficulty == "medium":
            base_chance = 0.5
        elif difficulty == "hard":
            base_chance = 0.3
        else:  # very_hard
            base_chance = 0.2
        
        # Charisma bonus
        if "charisma" in self.player.get("skills", []):
            base_chance += 0.2
        
        # Location danger impact - survivors more likely to join in dangerous areas
        location = LOCATIONS[self.player["location"]]
        danger_bonus = location["danger_level"] * 0.05
        
        # Group size penalty - large groups are harder to convince to join
        companion_count = len(active_companions)
        group_penalty = companion_count * 0.05
        
        final_chance = max(0.1, min(0.9, base_chance + danger_bonus - group_penalty))
        
        if random.random() < final_chance:
            # Success
            print(Colors.colorize(f"{survivor['name']} agrees to join your group!", Colors.GREEN))
            
            if "joining" in survivor["dialogue"]:
                joining_line = random.choice(survivor["dialogue"]["joining"])
                print(f"\n{survivor['name']} says: \"{joining_line}\"")
            
            # Add to companions list
            if "companions" not in self.player:
                self.player["companions"] = []
            
            # Set some additional companion properties
            survivor["loyalty"] = 50  # Base loyalty
            survivor["days_with_group"] = 0
            survivor["status"] = "active"  # Explicitly set as active
            
            self.player["companions"].append(survivor)
            
            # Apply any skill benefits
            self.apply_companion_skills(survivor)
            
            # Inform the player about the companion limit
            if len(active_companions) == 1:  # This means we now have 2 active companions
                print(Colors.colorize("\nYou now have 2 active companions, which is the maximum.", Colors.YELLOW))
                print("If you want to recruit someone else, you'll need to dismiss one of your current companions using the /dismiss [name] command.")
            
            return True
        else:
            # Failure
            print(Colors.colorize(f"{survivor['name']} declines your offer to join.", Colors.RED))
            
            reasons = [
                "I prefer to work alone.",
                "I don't know if I can trust your group yet.",
                "I have my own mission to complete.",
                "I need to find someone I lost.",
                "Your group draws too much attention.",
                "Too many people means too many mistakes.",
                "I’ve seen what happens when groups fall apart.",
                "I move faster on my own.",
                "Your supplies won't last with another mouth to feed.",
                "I’ve already lost too many people.",
                "I don’t want to get attached again.",
                "You’re heading in the wrong direction.",
                "I’ve got a safe place of my own.",
                "Groups attract raiders, not just zombies.",
                "Someone in your group gives me a bad feeling.",
                "I have my own rules—I don’t follow others'.",
                "I don't want to become someone I hate.",
                "I've seen what desperation does to people.",
                "I trust my instincts, not strangers.",
                "I need to stay off the grid for now."
            ]

            
            print(f"\n{survivor['name']}: \"{random.choice(reasons)}\"")
            
            # Small chance they might give you something anyway
            if random.random() < 0.3:
                # Generate a small gift
                common_items = [item_id for item_id, item in ITEMS.items() 
                               if item.get("rarity", "common") == "common" and
                                  item.get("value", 10) < 15]
                
                if common_items:
                    gift_id = random.choice(common_items)
                    self.add_to_inventory(gift_id)
                    print(f"\n{survivor['name']} gives you a {ITEMS[gift_id]['name']} before leaving.")
            
            return False
    
    def cmd_companions(self, *args):
        """View and manage your companions."""
        companions = self.player.get("companions", [])
        
        if not companions:
            print(Colors.colorize("\nYou have no companions in your group.", Colors.YELLOW))
            return
        
        print(Colors.colorize("\nYour Companions:", Colors.HEADER))
        print(Colors.colorize("="*50, Colors.BLUE))
        
        active_companions = [c for c in companions if c.get("status", "active") == "active"]
        injured_companions = [c for c in companions if c.get("status") == "injured"]
        
        print(Colors.colorize(f"Active Companions: {len(active_companions)}/2", Colors.CYAN))
        
        # Display active companions first
        if active_companions:
            print(Colors.colorize("\nActive:", Colors.GREEN))
            for i, companion in enumerate(active_companions):
                name = companion.get("name", "Unknown")
                days = companion.get("days_with_group", 0)
                loyalty = companion.get("loyalty", 50)
                loyalty_str = "High" if loyalty >= 70 else "Medium" if loyalty >= 40 else "Low"
                
                # Show companion's role/type
                companion_type = companion.get("survivor_type", "cautious_survivor").replace("_", " ").title()
                
                # Display specialized skills
                skills = companion.get("skills", [])
                skill_str = ", ".join(skill.replace("_", " ").title() for skill in skills) if skills else "None"
                
                # Show weapon specialization if any
                weapon_spec = None
                if "weapon_specialization" in companion:
                    spec = companion["weapon_specialization"]
                    weapon_type = spec.get("weapon_type", "unknown")
                    bonus = spec.get("damage_bonus", 1.2)
                    bonus_percent = int((bonus - 1.0) * 100)
                    weapon_spec = f"{weapon_type.title()} Weapons Specialist (+{bonus_percent}% damage)"
                
                print(f"{i+1}. {Colors.colorize(name, Colors.CYAN)} - {companion_type}")
                print(f"   Days with group: {days} | Loyalty: {loyalty_str}")
                print(f"   Skills: {skill_str}")
                if weapon_spec:
                    print(f"   Specialization: {Colors.colorize(weapon_spec, Colors.GREEN)}")
                print("")
        
        # Display injured companions
        if injured_companions:
            print(Colors.colorize("\nInjured/Recovering:", Colors.RED))
            for i, companion in enumerate(injured_companions):
                name = companion.get("name", "Unknown")
                recovery_time = companion.get("recovery_time", 1)
                
                print(f"{i+1}. {Colors.colorize(name, Colors.RED)} - Recovering ({recovery_time} hours until ready)")
        
        print(Colors.colorize("\nCommands:", Colors.YELLOW))
        print("/dismiss [name] - Dismiss a companion from your group")
        print("/companions - Show this list again")
    
    def cmd_dismiss(self, *args):
        """Dismiss a companion from your group."""
        if not args:
            print(Colors.colorize("You need to specify which companion to dismiss.", Colors.YELLOW))
            print("Usage: /dismiss [companion_name]")
            return
        
        companion_name = " ".join(args).lower()
        companions = self.player.get("companions", [])
        
        if not companions:
            print(Colors.colorize("You don't have any companions to dismiss.", Colors.RED))
            return
        
        # Find the companion by name
        dismissed = False
        dismissed_companion = None
        for i, companion in enumerate(companions):
            if companion.get("name", "").lower() == companion_name:
                dismissed_companion = companions.pop(i)
                dismissed = True
                break
        
        if dismissed and dismissed_companion:
            name = dismissed_companion.get("name")
            print(Colors.colorize(f"\n{name} has left your group.", Colors.CYAN))
            
            # Remove any bonuses from this companion
            # We would need to track which bonuses came from which companion for proper removal
            # For simplicity, we'll just give a message about skill changes
            if "skills" in dismissed_companion and dismissed_companion["skills"]:
                print(Colors.colorize("Your group's capabilities have been adjusted due to the departure.", Colors.YELLOW))
                
            # Handle weapon specialization removal if needed
            if "companion_weapon_specializations" in self.player:
                companion_id = dismissed_companion.get("id", "unknown")
                if companion_id in self.player["companion_weapon_specializations"]:
                    del self.player["companion_weapon_specializations"][companion_id]
            
            # Random farewell message based on loyalty
            loyalty = dismissed_companion.get("loyalty", 50)
            if loyalty > 70:
                farewells = [
                    f"{name} thanks you for the time spent together and promises to remember you.",
                    f"{name} seems sad to go, but understands your decision.",
                    f"{name} gives you some supplies as a parting gift."
                ]
            elif loyalty > 40:
                farewells = [
                    f"{name} nods and wishes you good luck.",
                    f"{name} understands and hopes you both survive.",
                    f"{name} accepts your decision without argument."
                ]
            else:
                farewells = [
                    f"{name} seems relieved to be leaving.",
                    f"{name} was already thinking about leaving anyway.",
                    f"{name} leaves without saying much."
                ]
            
            print(random.choice(farewells))
            
        else:
            print(Colors.colorize(f"You don't have a companion named '{companion_name}'.", Colors.RED))
            print("Use /companions to see a list of your current companions.")
    
    def apply_companion_skills(self, companion):
        """Apply skills and bonuses from a companion.
        
        Args:
            companion: The companion data
        """
        skills = companion.get("skills", [])
        
        # If this companion has weapon specializations, store them
        if "weapon_specialization" in companion:
            if "companion_weapon_specializations" not in self.player:
                self.player["companion_weapon_specializations"] = {}
            
            companion_id = companion.get("id", str(len(self.player.get("companions", []))))
            self.player["companion_weapon_specializations"][companion_id] = companion["weapon_specialization"]
            
            # Display information about the companion's weapon specialization
            specialization = companion["weapon_specialization"]
            weapon_type = specialization.get("weapon_type", "unknown")
            bonus = specialization.get("damage_bonus", 1.2)
            bonus_percent = int((bonus - 1.0) * 100)
            
            print(Colors.colorize(f"{companion['name']} is specialized in {weapon_type} weapons (+{bonus_percent}% damage).", Colors.GREEN))
        
        for skill in skills:
            if skill == "medical":
                self.player["medical_bonus"] = self.player.get("medical_bonus", 0) + 0.2
                print(Colors.colorize("Your group's medical effectiveness has improved.", Colors.GREEN))
            
            elif skill == "crafting":
                self.player["crafting_bonus"] = self.player.get("crafting_bonus", 0) + 0.15
                print(Colors.colorize("Your group's crafting efficiency has improved.", Colors.GREEN))
            
            elif skill == "hunting":
                self.player["food_find_bonus"] = self.player.get("food_find_bonus", 0) + 0.25
                print(Colors.colorize("Your group will find more food while exploring.", Colors.GREEN))
            
            elif skill == "combat":
                self.player["combat_bonus"] = self.player.get("combat_bonus", 0) + 0.15
                print(Colors.colorize("Your group's combat effectiveness has improved.", Colors.GREEN))
            
            elif skill == "stealth":
                self.player["stealth_bonus"] = self.player.get("stealth_bonus", 0) + 0.2
                print(Colors.colorize("Your group can move more quietly now.", Colors.GREEN))
            
            elif skill == "engineering":
                self.player["repair_bonus"] = self.player.get("repair_bonus", 0) + 0.3
                print(Colors.colorize("Your group's repair and building capabilities have improved.", Colors.GREEN))
                
            elif skill == "marksmanship":
                self.player["ranged_bonus"] = self.player.get("ranged_bonus", 0) + 0.25
                print(Colors.colorize(f"{companion['name']} improves your group's accuracy with ranged weapons.", Colors.GREEN))
                
            elif skill == "explosives":
                self.player["explosive_bonus"] = self.player.get("explosive_bonus", 0) + 0.3
                print(Colors.colorize(f"{companion['name']} knows how to maximize explosive damage.", Colors.GREEN))
                
            elif skill == "blade_master":
                self.player["blade_bonus"] = self.player.get("blade_bonus", 0) + 0.25
                print(Colors.colorize(f"{companion['name']} is skilled with blade weapons.", Colors.GREEN))
                
            elif skill == "tactics":
                self.player["combat_bonus"] = self.player.get("combat_bonus", 0) + 0.1
                self.player["group_defense"] = self.player.get("group_defense", 0) + 0.2
                print(Colors.colorize(f"{companion['name']} provides tactical combat advice to the group.", Colors.GREEN))
    
    def encounter_animal(self):
        """Handle an encounter with an animal.
        
        Returns:
            bool: True if combat started, False otherwise
        """
        animal = self.spawn_animal()
        is_friendly = animal.get("friendly", False)
        
        print("\n" + Colors.colorize("="*50, Colors.GREEN))
        print(Colors.colorize("ANIMAL ENCOUNTER", Colors.GREEN + Colors.BOLD))
        print(Colors.colorize("="*50, Colors.GREEN))
        
        print(f"You encounter a {animal['name']}!")
        print(f"{animal['description']}")
        
        if is_friendly:
            # Handle friendly animal encounter
            if animal.get("companion_potential", False):
                print("\nThis animal could potentially become a companion.")
                print("1. Try to befriend it")
                print("2. Leave it alone")
                print("3. Try to hunt it for food")
                
                choice = input("> ")
                
                if choice == "1":
                    # Try to befriend
                    success_chance = 0.6
                    
                    # Bonus if player has food
                    food_items = [item_idx for item_idx, item in enumerate(self.player["inventory"]) 
                                 if ITEMS[item["id"]].get("type") == "food"]
                    
                    if food_items:
                        print("\nYou can offer food to increase your chances:")
                        for i, idx in enumerate(food_items):
                            item = ITEMS[self.player["inventory"][idx]["id"]]
                            print(f"{i+1}. {item['name']}")
                        print("0. Don't offer food")
                        
                        food_choice = input("> ")
                        try:
                            food_idx = int(food_choice) - 1
                            if food_idx >= 0 and food_idx < len(food_items):
                                item_idx = food_items[food_idx]
                                item = ITEMS[self.player["inventory"][item_idx]["id"]]
                                print(f"\nYou offer the {item['name']} to the {animal['name']}.")
                                success_chance += 0.3  # Significant bonus for food
                                self.remove_from_inventory(item_idx)
                        except ValueError:
                            pass
                    
                    if random.random() < success_chance:
                        # Success
                        print(Colors.colorize(f"The {animal['name']} cautiously approaches and accepts your friendship!", Colors.GREEN))
                        
                        # Add as companion
                        if "animal_companions" not in self.player:
                            self.player["animal_companions"] = []
                        
                        # Give the animal a random name
                        pet_names = ["Buddy", "Max", "Charlie", "Cooper", "Luna", "Bella", "Rocky", "Shadow", 
                                    "Scout", "Rusty", "Daisy", "Bear", "Duke", "Sadie", "Rosie", "Pepper"]
                        animal["given_name"] = random.choice(pet_names)
                        
                        print(f"You decide to call it {animal['given_name']}.")
                        
                        self.player["animal_companions"].append(animal)
                        
                        # Apply animal bonuses
                        if animal.get("detection_bonus"):
                            self.player["detection_bonus"] = self.player.get("detection_bonus", 0) + animal["detection_bonus"]
                            print(Colors.colorize(f"{animal['given_name']} will help detect threats before they notice you.", Colors.GREEN))
                        
                        if animal.get("stealth_bonus"):
                            self.player["stealth_bonus"] = self.player.get("stealth_bonus", 0) + animal["stealth_bonus"]
                            print(Colors.colorize(f"{animal['given_name']} will help you move more quietly.", Colors.GREEN))
                    else:
                        # Failure
                        print(Colors.colorize(f"The {animal['name']} is too cautious and backs away.", Colors.RED))
                
                elif choice == "2":
                    # Leave alone
                    print(f"\nYou decide to leave the {animal['name']} alone.")
                    print("It watches you for a moment, then disappears.")
                
                elif choice == "3":
                    # Hunt it - turn friendly encounter hostile
                    print(f"\nYou decide to hunt the {animal['name']} for food.")
                    animal["friendly"] = False
                    self.current_zombie = animal  # Set the enemy reference
                    self.current_enemy = animal   # Set both references for consistency
                    self.start_combat()
                    return True
            
            elif animal.get("farm_animal", False):
                print("\nThis animal could provide a sustainable food source if kept at your camp.")
                print("1. Try to capture it and bring it back to camp")
                print("2. Leave it alone")
                print("3. Hunt it for immediate food")
                
                choice = input("> ")
                
                if choice == "1":
                    # Try to capture for camp
                    camp_upgrade_level = self.player.get("camp_upgrades", {}).get("livestock_pen", 0)
                    
                    if camp_upgrade_level > 0:
                        # Can capture if livestock pen exists
                        print(f"\nYou manage to secure the {animal['name']} and plan to bring it back to camp.")
                        
                        if "farm_animals" not in self.player:
                            self.player["farm_animals"] = []
                        
                        self.player["farm_animals"].append(animal["name"].lower())
                        print(Colors.colorize(f"When you return to camp, the {animal['name']} will be added to your livestock pen.", Colors.GREEN))
                        
                        if animal.get("food_production", False):
                            print(Colors.colorize("This will provide a steady source of food.", Colors.GREEN))
                    else:
                        print(Colors.colorize("You don't have a livestock pen at your camp. You need to build one first.", Colors.RED))
                        print(f"The {animal['name']} wanders away.")
                
                elif choice == "2":
                    # Leave alone
                    print(f"\nYou decide to leave the {animal['name']} alone.")
                
                elif choice == "3":
                    # Hunt
                    print(f"\nYou decide to hunt the {animal['name']} for immediate food.")
                    animal["friendly"] = False
                    self.current_zombie = animal  # Set the enemy reference
                    self.current_enemy = animal   # Set both references for consistency
                    self.start_combat()
                    return True
            
            else:
                # Generic friendly animal
                print(f"\nThe {animal['name']} doesn't seem interested in you and soon moves on.")
        
        else:
            # Infected/hostile animal
            print(Colors.colorize(f"\nThe {animal['name']} appears aggressive and infected!", Colors.RED))
            
            # Special case for pack hunters
            if animal.get("pack_hunter", False) and animal.get("calls_pack", False):
                pack_size = animal.get("pack_size", 3)
                print(Colors.colorize(f"You realize this isn't just one {animal['name']} - it's a pack of {pack_size}!", Colors.RED))
                print("The infected animals begin to circle you, coordinating their attack.")
                
                # Increase difficulty for pack animals
                animal["damage"] = int(animal["damage"] * 1.2)
                animal["health"] = int(animal["health"] * pack_size * 0.7)  # Not full multiplier to keep it balanced
                animal["pack_attack"] = True
            
            # Special case for ambush predators
            if animal.get("ambush", False) and random.random() < 0.7:
                print(Colors.colorize(f"The {animal['name']} lunges at you before you can react!", Colors.RED))
                # Ambush gives them a first attack
                damage = int(animal["damage"] * 0.7)  # Reduced first strike
                self.player["health"] -= damage
                print(Colors.colorize(f"You take {damage} damage from the surprise attack!", Colors.RED))
            
            # Start combat
            self.current_zombie = animal  # Set the enemy reference
            self.current_enemy = animal   # Set both references for consistency
            self.start_combat()
            return True
        
        return False

# Start the game if run directly
if __name__ == "__main__":
    if os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1":
        game = GameState()
        game.start_game()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
