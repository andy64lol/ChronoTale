#!/usr/bin/env python3
"""
Mexican Gangsters - A Text-based RPG Game
Set in New Mexico with GTA-style gameplay mechanics

Features:
- Open-world exploration across New Mexico cities
- Criminal activities and missions
- Gang reputation system
- Vehicle system with stealing and driving
- Police wanted level system
- Weapon and money management
- Drug dealing and territory control
- Character customization and stats
"""

import random
import json
import os
import time
from typing import Optional
from datetime import datetime
import sys

# Import colorama with proper fallback
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORS_AVAILABLE = True
except ImportError:
    # Create simple fallback objects
    from types import SimpleNamespace
    Fore = SimpleNamespace(
        RED="", YELLOW="", GREEN="", CYAN="", BLUE="", MAGENTA="", 
        WHITE="", LIGHTRED_EX="", LIGHTGREEN_EX="", LIGHTBLUE_EX="", 
        LIGHTMAGENTA_EX="", LIGHTCYAN_EX=""
    )
    Back = SimpleNamespace(
        RED="", YELLOW="", GREEN="", CYAN="", BLUE="", MAGENTA="", 
        WHITE="", BLACK=""
    )
    Style = SimpleNamespace(RESET_ALL="", BRIGHT="", DIM="")
    COLORS_AVAILABLE = False

# Game configuration
SAVE_FILE = "mexican_gangsters_save.json"

# New enhanced systems
SPECIAL_EVENTS = {
    "cartel_meeting": {
        "name": "Reunión del Cartel / Cartel Meeting",
        "description": "Un alto jefe del cartel quiere reunirse contigo / A high-ranking cartel boss wants to meet you",
        "requirements": {"respect": 75, "criminal_level": 3},
        "rewards": {"money": 15000, "respect": 20, "special_mission": True},
        "consequences": {"police_attention": 15}
    },
    "police_raid": {
        "name": "Redada Policial / Police Raid", 
        "description": "La policía está haciendo redadas en la ciudad / Police are conducting raids in the city",
        "requirements": {"wanted_level": 3},
        "effects": {"all_activities_dangerous": True, "escape_chance": 0.6},
        "duration": 3  # days
    },
    "gang_war": {
        "name": "Guerra de Pandillas / Gang War",
        "description": "Las pandillas rivales están en guerra / Rival gangs are at war",
        "requirements": {"gang_affiliation": True, "respect": 50},
        "rewards": {"territory_control": True, "money": 25000},
        "risks": {"death_chance": 0.3, "injury_chance": 0.6}
    },
    "corrupt_official": {
        "name": "Oficial Corrupto / Corrupt Official",
        "description": "Un oficial de policía corrupto ofrece sus servicios / A corrupt police officer offers services",
        "requirements": {"money": 10000, "criminal_level": 2},
        "benefits": {"reduced_wanted": True, "inside_info": True},
        "cost": 5000
    }
}

BUSINESS_VENTURES = {
    "drug_lab": {
        "name": "Laboratorio de Drogas / Drug Lab",
        "spanish_name": "Laboratorio de Metanfetaminas",
        "cost": 50000,
        "daily_income": 3000,
        "risk_level": 4,
        "requirements": {"criminal_level": 3, "chemistry_skill": 5},
        "upkeep": 1000,
        "police_attention": 20
    },
    "chop_shop": {
        "name": "Desguace / Chop Shop", 
        "spanish_name": "Taller de Desguace",
        "cost": 30000,
        "daily_income": 1500,
        "risk_level": 2,
        "requirements": {"criminal_level": 2, "mechanics_skill": 4},
        "upkeep": 500,
        "police_attention": 10
    },
    "smuggling_route": {
        "name": "Ruta de Contrabando / Smuggling Route",
        "spanish_name": "Ruta de Contrabando Fronterizo", 
        "cost": 75000,
        "daily_income": 5000,
        "risk_level": 5,
        "requirements": {"criminal_level": 4, "connections": 3},
        "upkeep": 2000,
        "police_attention": 30
    },
    "money_laundering": {
        "name": "Lavado de Dinero / Money Laundering",
        "spanish_name": "Operación de Lavado",
        "cost": 100000,
        "daily_income": 2000,
        "risk_level": 3,
        "requirements": {"criminal_level": 4, "intelligence": 7},
        "upkeep": 3000,
        "police_attention": 25,
        "special_ability": "clean_dirty_money"
    }
}

REPUTATION_SYSTEM = {
    "street_thug": {"min_respect": 0, "max_respect": 24, "title": "Matón Callejero / Street Thug"},
    "small_time": {"min_respect": 25, "max_respect": 49, "title": "Delincuente Menor / Small-time Criminal"},
    "enforcer": {"min_respect": 50, "max_respect": 74, "title": "Sicario / Enforcer"},
    "lieutenant": {"min_respect": 75, "max_respect": 99, "title": "Lugarteniente / Lieutenant"},
    "boss": {"min_respect": 100, "max_respect": 149, "title": "Jefe / Boss"},
    "kingpin": {"min_respect": 150, "max_respect": 999, "title": "Capo / Kingpin"}
}
CITIES = {
    "Albuquerque": {
        "description": "La ciudad más grande de Nuevo México, perfecta para grandes golpes y tratos peligrosos",
        "english_desc": "The largest city in New Mexico, perfect for big scores and dangerous deals",
        "districts": ["Ciudad Vieja", "Centro", "Lado Oeste", "Alturas del Noreste", "Las Colinas", "Valle del Río", "Westside", "Foothills"],
        "danger_level": 3,
        "cartel_presence": "Los Hermanos del Desierto",
        "specialties": ["drug_labs", "money_laundering", "weapons_trafficking"],
        "police_stations": 4,
        "hospitals": 3,
        "airports": 1,
        "major_highways": ["I-25", "I-40"],
        "population": 560000
    },
    "Santa Fe": {
        "description": "La capital con rica historia y blancos adinerados, pero vigilancia pesada",
        "english_desc": "The capital city with rich history and wealthy targets, but heavy surveillance",
        "districts": ["La Plaza", "Camino del Cañón", "Distrito Ferroviario", "Centro", "Lado Este", "Midtown", "Eastside", "Southside"],
        "danger_level": 2,
        "cartel_presence": "Cartel de la Corona",
        "specialties": ["art_theft", "political_corruption", "high_society_cons"],
        "police_stations": 3,
        "hospitals": 2,
        "airports": 1,
        "major_highways": ["I-25", "US-285"],
        "population": 85000
    },
    "Las Cruces": {
        "description": "Ciudad fronteriza con oportunidades de contrabando y fuerte presencia del cartel",
        "english_desc": "Border town with smuggling opportunities and strong cartel presence",
        "districts": ["Valle de Mesilla", "Mesa del Este", "Rancho Sonoma", "Cerros Picacho", "Centro", "Universidad", "West Mesa", "East Mesa"],
        "danger_level": 4,
        "cartel_presence": "Cártel de la Frontera Sur",
        "specialties": ["human_trafficking", "border_smuggling", "cartel_wars"],
        "police_stations": 2,
        "hospitals": 2,
        "airports": 1,
        "major_highways": ["I-25", "I-10"],
        "population": 215000
    },
    "Roswell": {
        "description": "Pequeña ciudad del desierto con secretos militares y blancos fáciles",
        "english_desc": "Small desert town with military secrets and easy targets",
        "districts": ["Centro", "Alturas Militares", "Del Norte", "Club de Campo", "Main Sur", "Industrial", "Airport District"],
        "danger_level": 1,
        "cartel_presence": "Pandilla de los Extraterrestres",
        "specialties": ["alien_conspiracy", "military_theft", "rural_meth"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-285", "US-70"],
        "population": 48000
    },
    "Taos": {
        "description": "Pueblo artístico en las montañas con turistas ricos y contrabando de lujo",
        "english_desc": "Artistic mountain town with wealthy tourists and luxury smuggling",
        "districts": ["Plaza Histórica", "Ranchos de Taos", "Pueblo", "Ski Valley", "Arroyo Seco", "El Prado"],
        "danger_level": 2,
        "cartel_presence": "Los Artistas del Norte",
        "specialties": ["art_forgery", "luxury_theft", "mountain_smuggling"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-64", "NM-68"],
        "population": 6000
    },
    "Farmington": {
        "description": "Centro de energía con trabajadores petroleros y dinero fácil",
        "english_desc": "Energy hub with oil workers and easy money",
        "districts": ["Centro", "Animas Valley", "La Plata", "Crouch Mesa", "Northside", "Industrial Park"],
        "danger_level": 3,
        "cartel_presence": "Cartel del Petróleo Negro",
        "specialties": ["oil_theft", "worker_extortion", "energy_smuggling"],
        "police_stations": 2,
        "hospitals": 2,
        "airports": 1,
        "major_highways": ["US-64", "US-550"],
        "population": 46000
    },
    "Gallup": {
        "description": "Pueblo fronterizo con comercio nativo y contrabando tribal",
        "english_desc": "Border town with native trade and tribal smuggling",
        "districts": ["Centro Histórico", "Red Rock", "Miyamura", "Gamerco", "Church Rock", "Twin Lakes"],
        "danger_level": 3,
        "cartel_presence": "Hermandad de la Roca Roja",
        "specialties": ["casino_robbery", "artifact_theft", "reservation_smuggling"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["I-40", "US-491"],
        "population": 22000
    },
    "Silver City": {
        "description": "Antiguo pueblo minero con túneles secretos y operaciones subterráneas",
        "english_desc": "Old mining town with secret tunnels and underground operations",
        "districts": ["Centro Histórico", "College District", "Chihuahua Hill", "Swan Street", "Little Walnut", "Boston Hill"],
        "danger_level": 2,
        "cartel_presence": "Los Mineros Oscuros",
        "specialties": ["underground_labs", "precious_metal_theft", "tunnel_smuggling"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-180", "NM-90"],
        "population": 10000
    },
    "Carlsbad": {
        "description": "Ciudad de cuevas con turismo y oportunidades de secuestro",
        "english_desc": "Cave city with tourism and kidnapping opportunities",
        "districts": ["Centro", "Riverside", "La Huerta", "Country Club", "North Carlsbad", "Industrial"],
        "danger_level": 2,
        "cartel_presence": "Señores de las Cavernas",
        "specialties": ["tourist_kidnapping", "cave_smuggling", "potash_theft"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-62", "US-285"],
        "population": 32000
    },
    "Clovis": {
        "description": "Ciudad agrícola con rutas de contrabando rural y laboratorios escondidos",
        "english_desc": "Agricultural city with rural smuggling routes and hidden labs",
        "districts": ["Centro", "Tierra Blanca", "West Seventh", "North Prince", "Colonial Park", "Curry Station"],
        "danger_level": 3,
        "cartel_presence": "Los Agricultores Violentos",
        "specialties": ["rural_meth_labs", "cattle_rustling", "grain_smuggling"],
        "police_stations": 2,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-60", "US-70"],
        "population": 39000
    },
    "Hobbs": {
        "description": "Boom town petrolero con dinero rápido y crimen organizado",
        "english_desc": "Oil boom town with fast money and organized crime",
        "districts": ["Centro", "North Park", "Wilson Park", "Broadmoor", "Taylor Ranch", "Industrial Zone"],
        "danger_level": 4,
        "cartel_presence": "Cartel del Oro Negro",
        "specialties": ["oil_field_heists", "worker_exploitation", "pipeline_sabotage"],
        "police_stations": 2,
        "hospitals": 2,
        "airports": 1,
        "major_highways": ["US-62", "NM-18"],
        "population": 40000
    },
    "Española": {
        "description": "Valle histórico con cultura rica y contrabando tradicional",
        "english_desc": "Historic valley with rich culture and traditional smuggling",
        "districts": ["Centro", "Sombrillo", "Santa Cruz", "Alcalde", "Velarde", "Rio Arriba"],
        "danger_level": 3,
        "cartel_presence": "Hermanos del Valle Sagrado",
        "specialties": ["cultural_artifact_theft", "family_vendettas", "mountain_hideouts"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 0,
        "major_highways": ["US-84", "NM-68"],
        "population": 10000
    },
    "Portales": {
        "description": "Universidad y agricultura con tráfico de drogas estudiantil",
        "english_desc": "University and agriculture with student drug trafficking",
        "districts": ["Universidad", "Centro", "Roosevelt Park", "West Side", "Farm District", "Country Club"],
        "danger_level": 2,
        "cartel_presence": "Pandilla Universitaria",
        "specialties": ["campus_dealing", "agricultural_chemicals", "student_recruitment"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-70", "NM-467"],
        "population": 12000
    },
    "Raton": {
        "description": "Paso de montaña fronterizo con Colorado y contrabando internacional",
        "english_desc": "Mountain pass border with Colorado and international smuggling",
        "districts": ["Centro Histórico", "Raton Pass", "Tiger Drive", "Second Street", "Mountain View", "Railroad District"],
        "danger_level": 3,
        "cartel_presence": "Los Vigilantes del Paso",
        "specialties": ["mountain_smuggling", "train_robbery", "colorado_connection"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["I-25", "US-64"],
        "population": 6000
    },
    "Truth or Consequences": {
        "description": "Pueblo extraño con aguas termales y actividades paranormales",
        "english_desc": "Strange town with hot springs and paranormal activities",
        "districts": ["Centro", "Hot Springs", "Elephant Butte", "Williamsburg", "Palomas", "Desert Hills"],
        "danger_level": 2,
        "cartel_presence": "Los Curanderos del Desierto",
        "specialties": ["tourist_scams", "spiritual_fraud", "desert_burial"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["I-25", "US-195"],
        "population": 6000
    },
    "Aztec": {
        "description": "Ruinas antiguas con turismo arqueológico y robo de artefactos",
        "english_desc": "Ancient ruins with archaeological tourism and artifact theft",
        "districts": ["Centro", "Aztec Ruins", "Hart Canyon", "Flora Vista", "Crouch Mesa", "Archaeological Zone"],
        "danger_level": 2,
        "cartel_presence": "Guardianes de los Ancestros",
        "specialties": ["artifact_smuggling", "archaeological_theft", "tourist_robbery"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 0,
        "major_highways": ["US-550", "NM-173"],
        "population": 6500
    },
    "Alamogordo": {
        "description": "Centro de investigación espacial con tecnología clasificada",
        "english_desc": "Space research center with classified technology",
        "districts": ["Centro", "Desert Aire", "Chaparral", "North End", "Alameda Park", "Research District"],
        "danger_level": 3,
        "cartel_presence": "Cartel del Espacio",
        "specialties": ["space_tech_theft", "research_espionage", "military_secrets"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-54", "US-70"],
        "population": 31000
    },
    "Hobbs": {
        "description": "Boomtown petrolero con trabajadores ricos y poca vigilancia",
        "english_desc": "Oil boomtown with wealthy workers and little surveillance",
        "districts": ["Centro", "North Hobbs", "East Hobbs", "Del Norte", "Industrial", "Oilfield District"],
        "danger_level": 3,
        "cartel_presence": "Barones del Petróleo",
        "specialties": ["oil_worker_robbery", "equipment_theft", "pipeline_sabotage"],
        "police_stations": 1,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-62", "NM-18"],
        "population": 38000
    }
}

VEHICLES = {
    "stolen_car": {"name": "Carro Robado / Stolen Car", "speed": 2, "reliability": 60, "value": 500, "spanish": "Carro Robado"},
    "motorcycle": {"name": "Motocicleta / Motorcycle", "speed": 4, "reliability": 70, "value": 1200, "spanish": "Motocicleta"},
    "pickup_truck": {"name": "Camioneta / Pickup Truck", "speed": 1, "reliability": 90, "value": 800, "spanish": "Camioneta"},
    "sports_car": {"name": "Carro Deportivo / Sports Car", "speed": 5, "reliability": 80, "value": 3000, "spanish": "Carro Deportivo"},
    "suv": {"name": "SUV", "speed": 2, "reliability": 85, "value": 2200, "spanish": "SUV"},
    "lowrider": {"name": "Lowrider", "speed": 2, "reliability": 75, "value": 1800, "spanish": "Lowrider"},
    "muscle_car": {"name": "Muscle Car", "speed": 4, "reliability": 75, "value": 2500, "spanish": "Carro Músculo"},
    "chopper": {"name": "Chopper Motorcycle", "speed": 3, "reliability": 65, "value": 2000, "spanish": "Chopper"},
    "armored_car": {"name": "Carro Blindado / Armored Car", "speed": 1, "reliability": 95, "value": 5000, "spanish": "Carro Blindado"},
    "police_car": {"name": "Patrulla / Police Car", "speed": 3, "reliability": 85, "value": 1500, "spanish": "Patrulla"},
    "ambulance": {"name": "Ambulancia / Ambulance", "speed": 2, "reliability": 90, "value": 1800, "spanish": "Ambulancia"},
    "fire_truck": {"name": "Camión de Bomberos / Fire Truck", "speed": 1, "reliability": 95, "value": 3000, "spanish": "Camión de Bomberos"},
    "semi_truck": {"name": "Tráiler / Semi Truck", "speed": 1, "reliability": 95, "value": 4000, "spanish": "Tráiler"},
    "luxury_sedan": {"name": "Sedán de Lujo / Luxury Sedan", "speed": 3, "reliability": 90, "value": 4500, "spanish": "Sedán de Lujo"},
    "convertible": {"name": "Convertible", "speed": 4, "reliability": 70, "value": 3500, "spanish": "Convertible"},
    "van": {"name": "Camioneta / Van", "speed": 2, "reliability": 80, "value": 1500, "spanish": "Camioneta"},
    "atv": {"name": "Cuatrimoto / ATV", "speed": 3, "reliability": 75, "value": 900, "spanish": "Cuatrimoto"},
    "dirt_bike": {"name": "Moto de Cross / Dirt Bike", "speed": 5, "reliability": 60, "value": 800, "spanish": "Moto de Cross"},
    "limousine": {"name": "Limusina / Limousine", "speed": 2, "reliability": 85, "value": 6000, "spanish": "Limusina"},
    "monster_truck": {"name": "Monster Truck", "speed": 2, "reliability": 80, "value": 3500, "spanish": "Monster Truck"}
}

# Street Racing Circuits
RACING_CIRCUITS = {
    "desert_highway": {
        "name": "Desert Highway Circuit",
        "spanish": "Circuito Carretera del Desierto",
        "location": "Albuquerque",
        "distance": "15 miles",
        "difficulty": 3,
        "entry_fee": 2000,
        "max_prize": 10000,
        "hazards": ["sand_storms", "police_checkpoints", "rival_racers"]
    },
    "mountain_pass": {
        "name": "Mountain Pass Challenge",
        "spanish": "Desafío del Paso de Montaña",
        "location": "Santa Fe",
        "distance": "12 miles",
        "difficulty": 4,
        "entry_fee": 3500,
        "max_prize": 15000,
        "hazards": ["sharp_turns", "cliff_edges", "weather_conditions"]
    },
    "border_run": {
        "name": "Border Run",
        "spanish": "Carrera Fronteriza",
        "location": "Las Cruces",
        "distance": "20 miles",
        "difficulty": 5,
        "entry_fee": 5000,
        "max_prize": 25000,
        "hazards": ["border_patrol", "cartel_interference", "smuggler_routes"]
    },
    "alien_highway": {
        "name": "Alien Highway Sprint",
        "spanish": "Sprint Carretera Alienígena",
        "location": "Roswell",
        "distance": "8 miles",
        "difficulty": 2,
        "entry_fee": 1000,
        "max_prize": 6000,
        "hazards": ["ufo_sightings", "military_presence", "desert_mirages"]
    }
}

# Underground Fighting Tournaments
FIGHTING_TOURNAMENTS = {
    "warehouse_brawl": {
        "name": "Warehouse Brawl",
        "spanish": "Pelea de Almacén",
        "location": "Albuquerque",
        "entry_fee": 1500,
        "rounds": 3,
        "max_prize": 8000,
        "opponents": ["street_fighter", "ex_boxer", "gang_enforcer"]
    },
    "cartel_championship": {
        "name": "Cartel Championship",
        "spanish": "Campeonato del Cartel",
        "location": "Las Cruces",
        "entry_fee": 4000,
        "rounds": 5,
        "max_prize": 20000,
        "opponents": ["cartel_hitman", "prison_champion", "underground_legend"]
    },
    "desert_death_match": {
        "name": "Desert Death Match",
        "spanish": "Combate a Muerte del Desierto",
        "location": "Santa Fe",
        "entry_fee": 2500,
        "rounds": 4,
        "max_prize": 12000,
        "opponents": ["desert_warrior", "mma_fighter", "bounty_hunter"]
    }
}

# Property Investment System
PROPERTIES = {
    "safe_house": {
        "name": "Safe House",
        "spanish": "Casa de Seguridad",
        "cost": 25000,
        "monthly_upkeep": 500,
        "benefits": {"heat_reduction": 10, "storage_space": 20},
        "description": "A secure location to lay low and store items"
    },
    "warehouse": {
        "name": "Criminal Warehouse",
        "spanish": "Almacén Criminal",
        "cost": 75000,
        "monthly_upkeep": 1200,
        "benefits": {"storage_space": 100, "smuggling_bonus": 15},
        "description": "Large storage facility for contraband operations"
    },
    "nightclub": {
        "name": "Nightclub",
        "spanish": "Club Nocturno",
        "cost": 150000,
        "monthly_upkeep": 3000,
        "benefits": {"daily_income": 2000, "reputation_boost": 5},
        "description": "Legitimate front business with good income"
    },
    "luxury_mansion": {
        "name": "Luxury Mansion",
        "spanish": "Mansión de Lujo",
        "cost": 500000,
        "monthly_upkeep": 8000,
        "benefits": {"prestige": 50, "gang_capacity": 15, "daily_income": 1000},
        "description": "Ultimate status symbol and gang headquarters"
    }
}

# Advanced NPC System
NPCS = {
    "informant": {
        "name": "El Soplón / The Snitch",
        "location": "Albuquerque",
        "services": ["police_intel", "gang_info", "job_tips"],
        "relationship": 0,
        "trust_level": "neutral",
        "dialogue": {
            "greeting": "¿Qué necesitas saber? / What do you need to know?",
            "friendly": "Siempre tengo información para mis amigos / I always have info for my friends",
            "hostile": "No hablo con enemigos / I don't talk to enemies"
        }
    },
    "mechanic": {
        "name": "Miguel el Mecánico / Miguel the Mechanic",
        "location": "Santa Fe",
        "services": ["vehicle_upgrades", "custom_parts", "stolen_car_cleanup"],
        "relationship": 0,
        "trust_level": "neutral",
        "dialogue": {
            "greeting": "Necesitas arreglos? / Need repairs?",
            "friendly": "Para ti, precios especiales / Special prices for you",
            "hostile": "No trabajo con ratas / I don't work with rats"
        }
    },
    "arms_dealer": {
        "name": "Doña Carmen / Lady Carmen",
        "location": "Las Cruces",
        "services": ["rare_weapons", "ammunition", "explosives"],
        "relationship": 0,
        "trust_level": "neutral",
        "dialogue": {
            "greeting": "¿Qué armamento buscas? / What weapons are you looking for?",
            "friendly": "Tengo las mejores armas para mis clientes leales / I have the best weapons for loyal customers",
            "hostile": "Fuera de aquí / Get out of here"
        }
    }
}

# Random Events System
RANDOM_EVENTS = [
    {
        "name": "police_checkpoint",
        "spanish": "Control Policial",
        "description": "Police checkpoint ahead",
        "probability": 15,
        "consequences": ["wanted_increase", "bribe_opportunity", "arrest_risk"]
    },
    {
        "name": "rival_gang_encounter",
        "spanish": "Encuentro con Pandilla Rival",
        "description": "Rival gang members spotted",
        "probability": 12,
        "consequences": ["gang_war", "territory_dispute", "respect_challenge"]
    },
    {
        "name": "drug_deal_gone_wrong",
        "spanish": "Trato de Drogas Salió Mal",
        "description": "A drug deal has gone sideways",
        "probability": 8,
        "consequences": ["money_loss", "heat_increase", "opportunity"]
    },
    {
        "name": "federal_investigation",
        "spanish": "Investigación Federal",
        "description": "Federal agents are investigating your operations",
        "probability": 5,
        "consequences": ["major_heat", "asset_seizure", "informant_risk"]
    },
    {
        "name": "cartel_invitation",
        "spanish": "Invitación del Cartel",
        "description": "A major cartel wants to meet",
        "probability": 3,
        "consequences": ["alliance_opportunity", "territory_expansion", "dangerous_mission"]
    }
]

# Police Career System
POLICE_RANKS = {
    "cadet": {
        "name": "Police Cadet / Cadete de Policía",
        "spanish": "Cadete de Policía",
        "salary": 500,
        "requirements": {"corruption": 0, "arrests": 0},
        "abilities": ["patrol", "traffic_stops"]
    },
    "officer": {
        "name": "Police Officer / Oficial de Policía",
        "spanish": "Oficial de Policía", 
        "salary": 800,
        "requirements": {"corruption": 0, "arrests": 5},
        "abilities": ["patrol", "traffic_stops", "investigations", "drug_busts"]
    },
    "detective": {
        "name": "Detective / Detective",
        "spanish": "Detective",
        "salary": 1200,
        "requirements": {"corruption": 0, "arrests": 15},
        "abilities": ["investigations", "undercover", "gang_raids", "interrogations"]
    },
    "sergeant": {
        "name": "Sergeant / Sargento",
        "spanish": "Sargento",
        "salary": 1500,
        "requirements": {"corruption": 0, "arrests": 30},
        "abilities": ["team_leadership", "major_operations", "swat_coordination"]
    },
    "lieutenant": {
        "name": "Lieutenant / Teniente",
        "spanish": "Teniente",
        "salary": 2000,
        "requirements": {"corruption": 0, "arrests": 50},
        "abilities": ["department_oversight", "federal_cooperation", "anti_cartel"]
    },
    "captain": {
        "name": "Captain / Capitán",
        "spanish": "Capitán",
        "salary": 2500,
        "requirements": {"corruption": 0, "arrests": 75},
        "abilities": ["city_coordination", "budget_control", "political_liaison"]
    }
}

POLICE_OPERATIONS = {
    "patrol": {
        "name": "Street Patrol / Patrulla Callejera",
        "spanish": "Patrulla Callejera",
        "time": 2,
        "salary_bonus": 50,
        "arrest_chance": 15,
        "corruption_risk": 5
    },
    "traffic_stops": {
        "name": "Traffic Enforcement / Control de Tráfico",
        "spanish": "Control de Tráfico",
        "time": 1,
        "salary_bonus": 30,
        "arrest_chance": 8,
        "corruption_risk": 10
    },
    "drug_bust": {
        "name": "Drug Bust / Operativo Antidrogas",
        "spanish": "Operativo Antidrogas",
        "time": 4,
        "salary_bonus": 200,
        "arrest_chance": 40,
        "corruption_risk": 15
    },
    "gang_raid": {
        "name": "Gang Raid / Redada de Pandillas",
        "spanish": "Redada de Pandillas",
        "time": 6,
        "salary_bonus": 300,
        "arrest_chance": 60,
        "corruption_risk": 20
    },
    "undercover": {
        "name": "Undercover Operation / Operación Encubierta",
        "spanish": "Operación Encubierta",
        "time": 8,
        "salary_bonus": 500,
        "arrest_chance": 80,
        "corruption_risk": 25
    }
}

WEAPONS = {
    "fists": {"name": "Puños / Fists", "damage": 10, "price": 0, "ammo": None, "spanish": "Puños", "type": "melee"},
    "knife": {"name": "Navaja / Knife", "damage": 25, "price": 50, "ammo": None, "spanish": "Navaja", "type": "melee"},
    "machete": {"name": "Machete", "damage": 35, "price": 120, "ammo": None, "spanish": "Machete", "type": "melee"},
    "bat": {"name": "Bate de Béisbol / Baseball Bat", "damage": 30, "price": 75, "ammo": None, "spanish": "Bate", "type": "melee"},
    "crowbar": {"name": "Palanca / Crowbar", "damage": 32, "price": 80, "ammo": None, "spanish": "Palanca", "type": "melee"},
    "katana": {"name": "Katana", "damage": 60, "price": 400, "ammo": None, "spanish": "Katana", "type": "melee"},
    "chainsaw": {"name": "Motosierra / Chainsaw", "damage": 85, "price": 600, "ammo": "gas", "spanish": "Motosierra", "type": "melee"},
    
    "pistol": {"name": "Pistola / Pistol", "damage": 40, "price": 300, "ammo": "9mm", "spanish": "Pistola", "type": "handgun"},
    "revolver": {"name": "Revólver / Revolver", "damage": 50, "price": 450, "ammo": "357", "spanish": "Revólver", "type": "handgun"},
    "desert_eagle": {"name": "Desert Eagle", "damage": 65, "price": 800, "ammo": "50cal", "spanish": "Águila del Desierto", "type": "handgun"},
    "glock": {"name": "Glock", "damage": 42, "price": 350, "ammo": "9mm", "spanish": "Glock", "type": "handgun"},
    "beretta": {"name": "Beretta", "damage": 38, "price": 320, "ammo": "9mm", "spanish": "Beretta", "type": "handgun"},
    "colt45": {"name": "Colt .45", "damage": 55, "price": 500, "ammo": "45acp", "spanish": "Colt .45", "type": "handgun"},
    
    "shotgun": {"name": "Escopeta / Shotgun", "damage": 80, "price": 600, "ammo": "shells", "spanish": "Escopeta", "type": "shotgun"},
    "sawed_off": {"name": "Escopeta Recortada / Sawed-off", "damage": 90, "price": 750, "ammo": "shells", "spanish": "Recortada", "type": "shotgun"},
    "combat_shotgun": {"name": "Escopeta de Combate / Combat Shotgun", "damage": 95, "price": 900, "ammo": "shells", "spanish": "Escopeta de Combate", "type": "shotgun"},
    "automatic_shotgun": {"name": "Escopeta Automática / Auto Shotgun", "damage": 85, "price": 1200, "ammo": "shells", "spanish": "Escopeta Automática", "type": "shotgun"},
    
    "rifle": {"name": "Rifle de Asalto / Assault Rifle", "damage": 60, "price": 1500, "ammo": "556", "spanish": "Rifle", "type": "rifle"},
    "ak47": {"name": "AK-47 Cuerno de Chivo", "damage": 70, "price": 2000, "ammo": "762", "spanish": "Cuerno de Chivo", "type": "rifle"},
    "m16": {"name": "M-16", "damage": 65, "price": 1800, "ammo": "556", "spanish": "M-16", "type": "rifle"},
    "scar": {"name": "SCAR-H", "damage": 75, "price": 2500, "ammo": "762", "spanish": "SCAR-H", "type": "rifle"},
    "g36": {"name": "G36", "damage": 62, "price": 1700, "ammo": "556", "spanish": "G36", "type": "rifle"},
    
    "smg": {"name": "Metralleta / SMG", "damage": 45, "price": 800, "ammo": "9mm", "spanish": "Metralleta", "type": "smg"},
    "uzi": {"name": "Uzi", "damage": 50, "price": 1200, "ammo": "9mm", "spanish": "Uzi", "type": "smg"},
    "mp5": {"name": "MP5", "damage": 48, "price": 1000, "ammo": "9mm", "spanish": "MP5", "type": "smg"},
    "skorpion": {"name": "Skorpion", "damage": 35, "price": 600, "ammo": "9mm", "spanish": "Skorpion", "type": "smg"},
    "tec9": {"name": "TEC-9", "damage": 40, "price": 700, "ammo": "9mm", "spanish": "TEC-9", "type": "smg"},
    
    "sniper": {"name": "Rifle de Francotirador / Sniper", "damage": 120, "price": 3500, "ammo": "762", "spanish": "Francotirador", "type": "sniper"},
    "barrett": {"name": "Barrett .50 Cal", "damage": 150, "price": 5000, "ammo": "50cal", "spanish": "Barrett", "type": "sniper"},
    "dragunov": {"name": "Dragunov", "damage": 125, "price": 3800, "ammo": "762", "spanish": "Dragunov", "type": "sniper"},
    
    "rpg": {"name": "RPG Lanzacohetes", "damage": 200, "price": 8000, "ammo": "rockets", "spanish": "Lanzacohetes", "type": "explosive"},
    "grenade": {"name": "Granada / Grenade", "damage": 150, "price": 500, "ammo": None, "spanish": "Granada", "type": "explosive"},
    "molotov": {"name": "Molotov", "damage": 120, "price": 50, "ammo": None, "spanish": "Molotov", "type": "explosive"},
    "c4": {"name": "C4 Explosive", "damage": 250, "price": 1000, "ammo": None, "spanish": "C4", "type": "explosive"},
    "sticky_bomb": {"name": "Bomba Pegajosa / Sticky Bomb", "damage": 180, "price": 800, "ammo": None, "spanish": "Bomba Pegajosa", "type": "explosive"},
    
    "taser": {"name": "Taser", "damage": 5, "price": 200, "ammo": "battery", "spanish": "Taser", "type": "special"},
    "pepper_spray": {"name": "Gas Pimienta / Pepper Spray", "damage": 10, "price": 25, "ammo": None, "spanish": "Gas Pimienta", "type": "special"},
    "flamethrower": {"name": "Lanzallamas / Flamethrower", "damage": 100, "price": 2000, "ammo": "fuel", "spanish": "Lanzallamas", "type": "special"}
}

DRUGS = {
    "mota": {"name": "Mota (Marijuana)", "spanish": "Mota", "buy_price": 10, "sell_price": 15, "risk": 1, "origin": "Local farms", "weight": 1},
    "coca": {"name": "Coca (Cocaine)", "spanish": "Coca", "buy_price": 50, "sell_price": 80, "risk": 3, "origin": "Colombian cartels", "weight": 0.5},
    "cristal": {"name": "Cristal (Methamphetamine)", "spanish": "Cristal", "buy_price": 30, "sell_price": 50, "risk": 2, "origin": "Desert labs", "weight": 0.3},
    "chiva": {"name": "Chiva (Heroin)", "spanish": "Chiva", "buy_price": 80, "sell_price": 120, "risk": 4, "origin": "Afghan suppliers", "weight": 0.2},
    "fentanilo": {"name": "Fentanilo (Fentanyl)", "spanish": "Fentanilo", "buy_price": 100, "sell_price": 180, "risk": 5, "origin": "Chinese precursors", "weight": 0.1},
    "extasis": {"name": "Éxtasis (Ecstasy)", "spanish": "Éxtasis", "buy_price": 25, "sell_price": 40, "risk": 2, "origin": "European labs", "weight": 0.1},
    "lsd": {"name": "LSD", "spanish": "LSD", "buy_price": 15, "sell_price": 25, "risk": 2, "origin": "Underground chemists", "weight": 0.01},
    "hongos": {"name": "Hongos (Mushrooms)", "spanish": "Hongos", "buy_price": 20, "sell_price": 35, "risk": 1, "origin": "Local growers", "weight": 0.5},
    "ketamina": {"name": "Ketamina (Ketamine)", "spanish": "Ketamina", "buy_price": 40, "sell_price": 65, "risk": 3, "origin": "Veterinary theft", "weight": 0.3},
    "pcp": {"name": "PCP", "spanish": "PCP", "buy_price": 35, "sell_price": 55, "risk": 3, "origin": "Street labs", "weight": 0.2},
    "crack": {"name": "Crack", "spanish": "Crack", "buy_price": 20, "sell_price": 35, "risk": 3, "origin": "Local cooks", "weight": 0.2},
    "spice": {"name": "Spice (K2)", "spanish": "Spice", "buy_price": 8, "sell_price": 15, "risk": 1, "origin": "Chemical suppliers", "weight": 0.3},
    "oxi": {"name": "Oxi (Oxidado)", "spanish": "Oxi", "buy_price": 5, "sell_price": 12, "risk": 2, "origin": "Brazilian suppliers", "weight": 0.3},
    "flakka": {"name": "Flakka", "spanish": "Flakka", "buy_price": 12, "sell_price": 22, "risk": 2, "origin": "Chinese labs", "weight": 0.2}
}

# Business types for passive income
BUSINESSES = {
    "car_wash": {"name": "Car Wash / Lavado de Carros", "spanish": "Lavado de Carros", "cost": 5000, "daily_income": 200, "heat_generation": 1},
    "restaurant": {"name": "Restaurant / Restaurante", "spanish": "Restaurante", "cost": 15000, "daily_income": 500, "heat_generation": 1},
    "nightclub": {"name": "Nightclub / Club Nocturno", "spanish": "Club Nocturno", "cost": 50000, "daily_income": 1500, "heat_generation": 3},
    "gas_station": {"name": "Gas Station / Gasolinera", "spanish": "Gasolinera", "cost": 25000, "daily_income": 800, "heat_generation": 2},
    "pawn_shop": {"name": "Pawn Shop / Casa de Empeño", "spanish": "Casa de Empeño", "cost": 10000, "daily_income": 400, "heat_generation": 2},
    "strip_club": {"name": "Strip Club / Club de Striptease", "spanish": "Club de Striptease", "cost": 75000, "daily_income": 2000, "heat_generation": 4},
    "casino": {"name": "Casino", "spanish": "Casino", "cost": 200000, "daily_income": 5000, "heat_generation": 5},
    "auto_shop": {"name": "Auto Shop / Taller Mecánico", "spanish": "Taller Mecánico", "cost": 30000, "daily_income": 1000, "heat_generation": 3},
    "pharmacy": {"name": "Pharmacy / Farmacia", "spanish": "Farmacia", "cost": 40000, "daily_income": 1200, "heat_generation": 3},
    "construction": {"name": "Construction Company / Constructora", "spanish": "Constructora", "cost": 100000, "daily_income": 3000, "heat_generation": 2}
}

# Advanced criminal activities
CRIMINAL_ACTIVITIES = {
    "bank_heist": {
        "name": "Bank Heist / Atraco Bancario",
        "spanish": "Atraco Bancario",
        "min_reward": 50000,
        "max_reward": 200000,
        "risk": 5,
        "required_members": 3,
        "required_skills": {"shooting": 3, "stealth": 2},
        "heat_increase": 15,
        "time_hours": 4
    },
    "armored_truck": {
        "name": "Armored Truck / Camión Blindado",
        "spanish": "Camión Blindado",
        "min_reward": 20000,
        "max_reward": 80000,
        "risk": 4,
        "required_members": 2,
        "required_skills": {"shooting": 2, "driving": 3},
        "heat_increase": 10,
        "time_hours": 2
    },
    "jewelry_store": {
        "name": "Jewelry Store / Joyería",
        "spanish": "Joyería",
        "min_reward": 10000,
        "max_reward": 50000,
        "risk": 3,
        "required_members": 1,
        "required_skills": {"stealth": 2},
        "heat_increase": 8,
        "time_hours": 1
    },
    "drug_lab_raid": {
        "name": "Drug Lab Raid / Asalto a Laboratorio",
        "spanish": "Asalto a Laboratorio",
        "min_reward": 30000,
        "max_reward": 100000,
        "risk": 4,
        "required_members": 3,
        "required_skills": {"shooting": 3, "intimidation": 2},
        "heat_increase": 12,
        "time_hours": 3
    },
    "kidnapping": {
        "name": "Kidnapping / Secuestro",
        "spanish": "Secuestro",
        "min_reward": 25000,
        "max_reward": 150000,
        "risk": 5,
        "required_members": 2,
        "required_skills": {"intimidation": 3, "charisma": 2},
        "heat_increase": 20,
        "time_hours": 24
    },
    "cybercrime": {
        "name": "Cybercrime / Cibercrimen",
        "spanish": "Cibercrimen",
        "min_reward": 5000,
        "max_reward": 75000,
        "risk": 2,
        "required_members": 0,
        "required_skills": {"hacking": 3},
        "heat_increase": 5,
        "time_hours": 2
    },
    "extortion": {
        "name": "Business Extortion / Extorsión",
        "spanish": "Extorsión",
        "min_reward": 1000,
        "max_reward": 15000,
        "risk": 2,
        "required_members": 1,
        "required_skills": {"intimidation": 2, "charisma": 1},
        "heat_increase": 3,
        "time_hours": 1
    },
    "smuggling_run": {
        "name": "Smuggling Run / Contrabando",
        "spanish": "Contrabando",
        "min_reward": 15000,
        "max_reward": 60000,
        "risk": 3,
        "required_members": 1,
        "required_skills": {"driving": 3, "stealth": 2},
        "heat_increase": 7,
        "time_hours": 6
    }
}

# Gang territories that can be controlled
TERRITORIES = {
    "downtown_albuquerque": {
        "name": "Downtown Albuquerque",
        "spanish": "Centro de Albuquerque",
        "city": "Albuquerque",
        "income_per_day": 500,
        "control_cost": 10000,
        "current_controller": "Los Hermanos del Desierto"
    },
    "westside_albuquerque": {
        "name": "Westside Albuquerque", 
        "spanish": "Lado Oeste Albuquerque",
        "city": "Albuquerque",
        "income_per_day": 300,
        "control_cost": 6000,
        "current_controller": "Independent"
    },
    "old_town_santa_fe": {
        "name": "Old Town Santa Fe",
        "spanish": "Ciudad Vieja Santa Fe", 
        "city": "Santa Fe",
        "income_per_day": 400,
        "control_cost": 8000,
        "current_controller": "Cartel de la Corona"
    },
    "border_las_cruces": {
        "name": "Border District Las Cruces",
        "spanish": "Distrito Fronterizo Las Cruces",
        "city": "Las Cruces", 
        "income_per_day": 800,
        "control_cost": 15000,
        "current_controller": "Cártel de la Frontera Sur"
    },
    "military_roswell": {
        "name": "Military District Roswell",
        "spanish": "Distrito Militar Roswell",
        "city": "Roswell",
        "income_per_day": 200,
        "control_cost": 4000,
        "current_controller": "Pandilla de los Extraterrestres"
    },
    "tourist_taos": {
        "name": "Tourist District Taos",
        "spanish": "Distrito Turístico Taos",
        "city": "Taos",
        "income_per_day": 350,
        "control_cost": 7000,
        "current_controller": "Los Artistas del Norte"
    },
    "oil_fields_farmington": {
        "name": "Oil Fields Farmington",
        "spanish": "Campos Petroleros Farmington",
        "city": "Farmington",
        "income_per_day": 600,
        "control_cost": 12000,
        "current_controller": "Cartel del Petróleo Negro"
    }
}

class Player:
    def __init__(self):
        self.name = ""
        self.gender = "unknown"  # Will be set during character creation
        self.age = 25
        self.health = 100
        self.max_health = 100
        self.money = 1000
        self.respect = 0
        self.wanted_level = 0
        self.location = "Albuquerque"
        self.district = "Downtown"
        self.inventory = {"fists": 1}
        self.ammo = {
            "9mm": 0, "shells": 0, "556": 0, "357": 0, "50cal": 0, "762": 0, "rockets": 0,
            "45acp": 0, "gas": 0, "battery": 0, "fuel": 0
        }
        self.drugs = {
            "mota": 0, "coca": 0, "cristal": 0, "chiva": 0, "fentanilo": 0, "extasis": 0,
            "lsd": 0, "hongos": 0, "ketamina": 0, "pcp": 0, "crack": 0, "spice": 0, "oxi": 0, "flakka": 0
        }
        self.vehicle: Optional[str] = None
        self.gang_affiliation: Optional[str] = None
        self.stats = {
            "missions_completed": 0,
            "people_killed": 0,
            "cars_stolen": 0,
            "money_earned": 0,
            "drugs_sold": 0,
            "times_arrested": 0,
            "territory_controlled": 0,
            "gang_members_recruited": 0,
            "rival_gangs_eliminated": 0,
            "heists_completed": 0
        }
        # Gang leadership attributes
        self.gang_name: Optional[str] = None
        self.gang_members = []
        self.territory = []
        self.gang_reputation = 0
        self.businesses = []  # Owned businesses for passive income
        self.safe_houses = []  # Safe houses in different cities
        self.contacts = {}  # Corrupt officials, suppliers, etc.
        self.heat_level = 0  # How much attention you're attracting
        self.prison_time = 0  # Days left in prison
        
        self.skills = {
            "shooting": 1,
            "driving": 1,
            "stealth": 1,
            "charisma": 1,
            "strength": 1,
            "hacking": 1,  # New skill for tech crimes
            "business": 1,  # New skill for managing operations
            "intimidation": 1  # New skill for extortion
        }
        self.skill_points = 5  # Points to allocate to skills
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100
        
        # Language preference system
        self.language_mode = "bilingual"  # "spanish", "english", or "bilingual"
        
        # New extended attributes
        self.properties = []  # Owned properties
        self.racing_wins = 0
        self.fighting_wins = 0
        self.npc_relationships = {}  # NPC relationship tracking
        self.special_items = []  # Rare/special items
        self.achievements = []  # Achievement system
        self.daily_activities_count = 0  # Track daily activity limits
        self.last_activity_date = None  # Date tracking
        self.prestige = 0  # Social standing in criminal world
        
        # Police Career System attributes
        self.is_police = False
        self.police_rank: Optional[str] = None
        self.police_corruption = 0  # 0-100, higher = more corrupt
        self.total_arrests = 0
        self.police_salary = 0
        self.police_operations_completed = 0
        self.undercover_identity = None
        self.good_deeds = 0  # Track helpful actions for police recruitment
        self.criminals_stopped = 0  # Track criminals stopped by player
        
        # Additional attributes for new features
        self.heat_level = 0
        self.prison_time = 0
        self.prison_contacts = []
        self.story_progress = 0
        
        # New business ventures
        self.business_ventures = []
        self.daily_income = 0
        self.criminal_level = 1  # Progression through criminal ranks
        
        # Empire building system
        self.empire = {
            "territories": [],
            "lieutenants": [],
            "operations": [],
            "influence": 0,
            "daily_income": 0
        }
        self.current_special_event = None
        
        # Enhanced relationship system
        for npc_id in NPCS.keys():
            self.npc_relationships[npc_id] = 0

    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if player dies"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True
        return False

    def heal(self, amount: int):
        """Heal player up to max health"""
        self.health = min(self.max_health, self.health + amount)

    def add_money(self, amount: int):
        """Add money and track earnings"""
        self.money += amount
        if amount > 0:
            self.stats["money_earned"] += amount

    def remove_money(self, amount: int) -> bool:
        """Remove money, return False if insufficient funds"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def add_respect(self, amount: int):
        """Add respect points"""
        self.respect += amount
    
    def add_experience(self, amount: int):
        """Add experience and handle level ups"""
        self.experience += amount
        while self.experience >= self.experience_to_next:
            self.experience -= self.experience_to_next
            self.level += 1
            self.skill_points += 3
            self.experience_to_next = int(self.experience_to_next * 1.5)
            return True  # Leveled up
        return False  # No level up

    def increase_wanted_level(self, amount: int = 1):
        """Increase wanted level (max 5 stars)"""
        self.wanted_level = min(5, self.wanted_level + amount)

    def decrease_wanted_level(self, amount: int = 1):
        """Decrease wanted level"""
        self.wanted_level = max(0, self.wanted_level - amount)
    
    def get_reputation_title(self) -> str:
        """Get current reputation title"""
        for level, data in REPUTATION_SYSTEM.items():
            if data["min_respect"] <= self.respect <= data["max_respect"]:
                return data["title"]
        return "Unknown Criminal"
    
    def get_criminal_level(self) -> int:
        """Calculate criminal level based on various factors"""
        base_level = self.respect // 25
        business_bonus = len(self.business_ventures)
        territory_bonus = len(self.territory) * 2
        return min(5, base_level + business_bonus + territory_bonus)
    
    def can_afford_business(self, business_id: str) -> bool:
        """Check if player can afford a business venture"""
        if business_id not in BUSINESS_VENTURES:
            return False
        business = BUSINESS_VENTURES[business_id]
        return (self.money >= business["cost"] and 
                self.criminal_level >= business["requirements"].get("criminal_level", 1))
    
    def add_business_venture(self, business_id: str) -> bool:
        """Add a new business venture"""
        if business_id in self.business_ventures:
            return False
        
        business = BUSINESS_VENTURES[business_id]
        if self.remove_money(business["cost"]):
            self.business_ventures.append(business_id)
            self.daily_income += business["daily_income"]
            self.heat_level += business["police_attention"]
            return True
        return False
    
    def trigger_special_event(self) -> Optional[str]:
        """Check for and trigger special events"""
        if self.current_special_event:
            return None  # Already in an event
        
        for event_id, event in SPECIAL_EVENTS.items():
            # Check requirements
            meets_requirements = True
            for req, value in event["requirements"].items():
                if req == "respect" and self.respect < value:
                    meets_requirements = False
                elif req == "criminal_level" and self.get_criminal_level() < value:
                    meets_requirements = False
                elif req == "wanted_level" and self.wanted_level < value:
                    meets_requirements = False
                elif req == "gang_affiliation" and not self.gang_affiliation:
                    meets_requirements = False
                elif req == "money" and self.money < value:
                    meets_requirements = False
            
            if meets_requirements and random.random() < 0.15:  # 15% chance
                self.current_special_event = event_id
                return event_id
        
        return None
    
    def improve_npc_relationship(self, npc_id: str, amount: int):
        """Improve relationship with an NPC"""
        if npc_id in self.npc_relationships:
            self.npc_relationships[npc_id] = min(100, self.npc_relationships[npc_id] + amount)
    
    def get_npc_trust_level(self, npc_id: str) -> str:
        """Get trust level with NPC"""
        if npc_id not in self.npc_relationships:
            return "unknown"
        
        relationship = self.npc_relationships[npc_id]
        if relationship >= 80:
            return "trusted_ally"
        elif relationship >= 60:
            return "good_friend"
        elif relationship >= 40:
            return "friendly"
        elif relationship >= 20:
            return "neutral"
        elif relationship >= 0:
            return "suspicious"
        else:
            return "hostile"

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.game_time = 0
        self.running = True
        self.current_mission = None
        self.language = "bilingual"  # Options: "spanish", "english", "bilingual"

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def slow_print(self, text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def display_header(self):
        """Display game header with player info"""
        self.clear_screen()
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   MEXICAN GANGSTERS - NEW MEXICO CRIME EMPIRE{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print()
        
        # Player status bar
        health_color = Fore.GREEN if self.player.health > 60 else Fore.YELLOW if self.player.health > 30 else Fore.RED
        wanted_stars = "★" * self.player.wanted_level + "☆" * (5 - self.player.wanted_level)
        
        print(f"{Fore.CYAN}Player: {self.player.name}{Style.RESET_ALL} | " +
              f"{health_color}Health: {self.player.health}/100{Style.RESET_ALL} | " +
              f"{Fore.GREEN}Money: ${self.player.money:,}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Respect: {self.player.respect}{Style.RESET_ALL} | " +
              f"{Fore.RED}Wanted: {wanted_stars}{Style.RESET_ALL} | " +
              f"{Fore.YELLOW}Location: {self.player.location}, {self.player.district}{Style.RESET_ALL}")
        
        if self.player.vehicle:
            vehicle_name = VEHICLES[self.player.vehicle]["name"]
            print(f"{Fore.BLUE}Vehicle: {vehicle_name}{Style.RESET_ALL}")
        
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print()

    def character_creation(self):
        """Create player character"""
        self.clear_screen()
        print(f"{Fore.RED}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}      WELCOME TO MEXICAN GANGSTERS{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*50}{Style.RESET_ALL}")
        print()
        
        self.slow_print(f"{Fore.WHITE}Bienvenido a Nuevo México, donde el crimen paga y la lealtad lo es todo.{Style.RESET_ALL}")
        self.slow_print(f"{Fore.WHITE}Welcome to New Mexico, where crime pays and loyalty is everything.{Style.RESET_ALL}")
        self.slow_print(f"{Fore.WHITE}Eres un criminal de poca monta buscando hacerte grande en el hampa.{Style.RESET_ALL}")
        self.slow_print(f"{Fore.WHITE}You're a small-time criminal looking to make it big in the underworld.{Style.RESET_ALL}")
        print()
        
        # Get player name
        while True:
            name = input(f"{Fore.CYAN}Ingresa el nombre de tu personaje / Enter your character's name: {Style.RESET_ALL}").strip()
            if name:
                self.player.name = name
                break
            print(f"{Fore.RED}Por favor ingresa un nombre válido / Please enter a valid name.{Style.RESET_ALL}")
        
        # Gender selection
        print(f"\n{Fore.YELLOW}Selecciona el género de tu personaje / Select your character's gender:{Style.RESET_ALL}")
        print(f"1. {Fore.BLUE}Hombre / Male{Style.RESET_ALL}")
        print(f"2. {Fore.MAGENTA}Mujer / Female{Style.RESET_ALL}")
        print(f"3. {Fore.CYAN}No binario / Non-binary{Style.RESET_ALL}")
        print(f"4. {Fore.WHITE}Prefiero no decir / Prefer not to say{Style.RESET_ALL}")
        
        while True:
            gender_choice = input(f"{Fore.CYAN}Elige una opción (1-4) / Choose an option (1-4): {Style.RESET_ALL}").strip()
            if gender_choice == "1":
                self.player.gender = "male"
                print(f"{Fore.GREEN}Género seleccionado: Hombre / Gender selected: Male{Style.RESET_ALL}")
                break
            elif gender_choice == "2":
                self.player.gender = "female"
                print(f"{Fore.GREEN}Género seleccionado: Mujer / Gender selected: Female{Style.RESET_ALL}")
                break
            elif gender_choice == "3":
                self.player.gender = "non-binary"
                print(f"{Fore.GREEN}Género seleccionado: No binario / Gender selected: Non-binary{Style.RESET_ALL}")
                break
            elif gender_choice == "4":
                self.player.gender = "undisclosed"
                print(f"{Fore.GREEN}Género: Prefiero no decir / Gender: Prefer not to say{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Opción inválida / Invalid option. Elige 1-4 / Choose 1-4.{Style.RESET_ALL}")
        
        # Age selection
        print(f"\n{Fore.YELLOW}Selecciona la edad de tu personaje / Select your character's age:{Style.RESET_ALL}")
        while True:
            try:
                age_input = input(f"{Fore.CYAN}Edad (18-60) / Age (18-60): {Style.RESET_ALL}").strip()
                age = int(age_input)
                if 18 <= age <= 60:
                    self.player.age = age
                    print(f"{Fore.GREEN}Edad seleccionada: {age} años / Age selected: {age} years{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}La edad debe estar entre 18 y 60 años / Age must be between 18 and 60 years{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor ingresa una edad válida / Please enter a valid age{Style.RESET_ALL}")
        
        # Choose starting city
        print(f"\n{Fore.YELLOW}Elige tu ciudad de inicio / Choose your starting city:{Style.RESET_ALL}")
        cities = list(CITIES.keys())
        for i, city in enumerate(cities, 1):
            danger = "★" * CITIES[city]["danger_level"]
            cartel = CITIES[city]["cartel_presence"]
            print(f"{i}. {city} - {CITIES[city]['description']}")
            print(f"   {CITIES[city]['english_desc']}")
            print(f"   Peligro/Danger: {danger} | Cartel: {cartel}")
            print()
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Ingresa tu elección / Enter choice (1-{len(cities)}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(cities):
                    self.player.location = cities[choice - 1]
                    self.player.district = CITIES[self.player.location]["districts"][0]
                    break
                else:
                    print(f"{Fore.RED}Elección inválida. Ingresa 1-{len(cities)} / Invalid choice. Please enter 1-{len(cities)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor ingresa un número / Please enter a number.{Style.RESET_ALL}")

        # Starting attributes with lore
        print(f"\n{Fore.GREEN}¡Personaje creado exitosamente! / Character created successfully!{Style.RESET_ALL}")
        
        # City-specific intro lore
        city_intros = {
            "Albuquerque": "Las calles de Albuquerque te llaman, hermano. Los Hermanos del Desierto controlan aquí, pero siempre hay espacio para uno más con agallas.",
            "Santa Fe": "Santa Fe, la capital elegante donde el dinero viejo se encuentra con el crimen nuevo. El Cartel de la Corona no tolera aficionados.",
            "Las Cruces": "La frontera es salvaje, amigo. Aquí el Cártel de la Frontera Sur hace las reglas, y las balas hablan más fuerte que las palabras.",
            "Roswell": "Roswell... donde los extraterrestres no son el único misterio. La Pandilla de los Extraterrestres controla lo que los militares no ven."
        }
        
        self.slow_print(f"Bienvenido a {self.player.location}, {self.player.name}.")
        self.slow_print(f"Welcome to {self.player.location}, {self.player.name}.")
        self.slow_print(city_intros[self.player.location])
        input(f"\n{Fore.CYAN}Presiona Enter para comenzar tu carrera criminal / Press Enter to begin your criminal career...{Style.RESET_ALL}")

    def main_menu(self):
        """Enhanced main game menu with all new features"""
        while self.running:
            # Check if player is dead
            if self.player.health <= 0:
                self.handle_death()
                continue
                
            self.display_header()
            
            # Display heat level and prison time warnings
            if self.player.heat_level > 75:
                print(f"{Fore.RED}⚠️  ALERTA DE CALOR / HEAT WARNING: {self.player.heat_level}/100{Style.RESET_ALL}")
            if self.player.prison_time > 0:
                print(f"{Fore.YELLOW}🔒 Tiempo en prisión / Prison time: {self.player.prison_time} días{Style.RESET_ALL}")
            
            # Show daily income from businesses and territories
            daily_income = 0
            for business in self.player.businesses:
                daily_income += business["daily_income"]
            for territory in self.player.territory:
                daily_income += TERRITORIES[territory]["income_per_day"]
            
            if daily_income > 0:
                print(f"{Fore.GREEN}💰 Ingresos diarios / Daily income: ${daily_income:,}{Style.RESET_ALL}")
            
            print(f"\n{Fore.YELLOW}¿Qué quieres hacer? / What do you want to do?{Style.RESET_ALL}")
            print()
            
            # Core Activities
            print(f"{Fore.CYAN}=== ACTIVIDADES PRINCIPALES / CORE ACTIVITIES ==={Style.RESET_ALL}")
            print(f"1. {Fore.GREEN}Explorar la ciudad / Explore the city{Style.RESET_ALL}")
            print(f"2. {Fore.RED}Actividades criminales / Criminal activities{Style.RESET_ALL}")
            print(f"3. {Fore.BLUE}Manejo de vehículos / Vehicle management{Style.RESET_ALL}")
            print(f"4. {Fore.MAGENTA}Visitar lugares / Visit locations{Style.RESET_ALL}")
            
            # Gang and Business Empire
            print(f"\n{Fore.CYAN}=== IMPERIO CRIMINAL / CRIMINAL EMPIRE ==={Style.RESET_ALL}")
            print(f"5. {Fore.LIGHTRED_EX}Gestión de pandilla / Gang management{Style.RESET_ALL}")
            print(f"6. {Fore.LIGHTGREEN_EX}Gestión de negocios / Business management{Style.RESET_ALL}")
            print(f"7. {Fore.LIGHTBLUE_EX}Control territorial / Territory control{Style.RESET_ALL}")
            
            # Advanced Criminal Operations
            print(f"\n{Fore.CYAN}=== OPERACIONES AVANZADAS / ADVANCED OPERATIONS ==={Style.RESET_ALL}")
            print(f"8. {Fore.LIGHTMAGENTA_EX}Atracos avanzados / Advanced heists{Style.RESET_ALL}")
            print(f"9. {Fore.LIGHTCYAN_EX}Cibercrimen / Cybercrime operations{Style.RESET_ALL}")
            
            # Character Management
            print(f"\n{Fore.CYAN}=== GESTIÓN DE PERSONAJE / CHARACTER MANAGEMENT ==={Style.RESET_ALL}")
            print(f"10. {Fore.YELLOW}Estado del personaje / Character status{Style.RESET_ALL}")
            print(f"11. {Fore.WHITE}Asignar puntos de habilidad / Allocate skill points{Style.RESET_ALL}")
            print(f"12. {Fore.LIGHTBLUE_EX}Cambiar idioma / Change language{Style.RESET_ALL}")
            
            # Game Management
            print(f"\n{Fore.CYAN}=== GESTIÓN DEL JUEGO / GAME MANAGEMENT ==={Style.RESET_ALL}")
            print(f"13. {Fore.GREEN}Guardar juego / Save game{Style.RESET_ALL}")
            print(f"14. {Fore.BLUE}Cargar juego / Load game{Style.RESET_ALL}")
            print(f"15. {Fore.LIGHTMAGENTA_EX}Carreras callejeras / Street racing{Style.RESET_ALL}")
            print(f"16. {Fore.LIGHTRED_EX}Torneos de pelea / Fighting tournaments{Style.RESET_ALL}")
            print(f"17. {Fore.LIGHTGREEN_EX}Inversiones inmobiliarias / Property investments{Style.RESET_ALL}")
            print(f"18. {Fore.LIGHTBLUE_EX}Relaciones con NPCs / NPC relationships{Style.RESET_ALL}")
            print(f"19. {Fore.LIGHTYELLOW_EX}Centro de logros / Achievement center{Style.RESET_ALL}")
            print(f"20. {Fore.LIGHTCYAN_EX}Carrera policial / Police career{Style.RESET_ALL}")
            
            # New Expansion Features
            print(f"\n{Fore.CYAN}=== NUEVAS CARACTERÍSTICAS / NEW FEATURES ==={Style.RESET_ALL}")
            print(f"22. {Fore.LIGHTMAGENTA_EX}Casino y apuestas / Casino & gambling{Style.RESET_ALL}")
            print(f"23. {Fore.LIGHTYELLOW_EX}Mercado negro / Black market{Style.RESET_ALL}")
            print(f"24. {Fore.LIGHTRED_EX}Misiones especiales / Special missions{Style.RESET_ALL}")
            print(f"25. {Fore.LIGHTGREEN_EX}Construcción de imperio / Empire building{Style.RESET_ALL}")
            print(f"26. {Fore.LIGHTBLUE_EX}Investigación privada / Private investigation{Style.RESET_ALL}")
            print(f"27. {Fore.LIGHTCYAN_EX}Contrabando internacional / International smuggling{Style.RESET_ALL}")
            print(f"28. {Fore.WHITE}Academia criminal / Criminal academy{Style.RESET_ALL}")
            print(f"21. {Fore.RED}Salir del juego / Quit game{Style.RESET_ALL}")
            print()
            
            choice = input(f"{Fore.CYAN}Elige tu opción / Enter your choice (1-28): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.explore_city()
            elif choice == "2":
                self.criminal_activities()
            elif choice == "3":
                self.vehicle_management()
            elif choice == "4":
                self.visit_locations()
            elif choice == "5":
                self.gang_management()
            elif choice == "6":
                self.business_management()
            elif choice == "7":
                self.territory_control()
            elif choice == "8":
                self.advanced_heist()
            elif choice == "9":
                self.cybercrime_operations()
            elif choice == "10":
                self.character_status()
            elif choice == "11":
                self.allocate_skill_points()
            elif choice == "12":
                self.language_menu()
            elif choice == "13":
                self.save_game()
            elif choice == "14":
                self.load_game()
            elif choice == "15":
                self.street_racing_menu()
            elif choice == "16":
                self.fighting_tournament_menu()
            elif choice == "17":
                self.enhanced_business_ventures_menu()
            elif choice == "18":
                self.special_events_system()
            elif choice == "19":
                self.enhanced_reputation_system()
            elif choice == "20":
                self.police_career_menu()
            elif choice == "21":
                return False
            elif choice == "22":
                self.casino_gambling_menu()
            elif choice == "23":
                self.black_market_menu()
            elif choice == "24":
                self.special_missions_menu()
            elif choice == "25":
                self.empire_building_menu()
            elif choice == "26":
                self.private_investigation_menu()
            elif choice == "27":
                self.international_smuggling_menu()
            elif choice == "28":
                self.criminal_academy_menu()
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice. Presiona Enter para continuar...{Style.RESET_ALL}")
                input()
            
            # Auto police encounter check for 3+ wanted level after any action (unless player is police)
            if self.player.wanted_level >= 3 and choice not in ["13", "14", "19", "20", "21"] and not self.player.is_police:
                self.police_encounter()

    def explore_city(self):
        """Explore the current city"""
        self.display_header()
        print(f"{Fore.YELLOW}Exploring {self.player.location}...{Style.RESET_ALL}")
        print()
        
        # Random encounters while exploring
        encounters = [
            self.random_mugger,
            self.find_money,
            self.police_patrol,
            self.drug_dealer,
            self.gang_member,
            self.witness_crime,
            self.help_citizen,
            self.report_suspicious_activity,
            self.nothing_happens
        ]
        
        # Weight the encounters based on wanted level and location danger
        weights = [20, 15, self.player.wanted_level * 10, 25, 20, 15, 15, 10, 30]
        encounter = random.choices(encounters, weights=weights)[0]
        encounter()
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def criminal_activities(self):
        """Show criminal activity options"""
        self.display_header()
        print(f"{Fore.RED}Criminal Activities{Style.RESET_ALL}")
        print()
        print(f"1. {Fore.YELLOW}Robar tienda / Rob a store{Style.RESET_ALL}")
        print(f"2. {Fore.GREEN}Vender drogas / Deal drugs{Style.RESET_ALL}")
        print(f"3. {Fore.BLUE}Robar auto / Steal a car{Style.RESET_ALL}")
        print(f"4. {Fore.MAGENTA}Misión de pandilla / Gang mission{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Atraco a banco / Bank heist{Style.RESET_ALL}")
        print(f"6. {Fore.LIGHTBLUE_EX}Secuestro / Kidnapping{Style.RESET_ALL}")
        print(f"7. {Fore.LIGHTGREEN_EX}Extorsión / Extortion{Style.RESET_ALL}")
        print(f"8. {Fore.LIGHTRED_EX}Guerra de territorios / Turf war{Style.RESET_ALL}")
        print(f"9. {Fore.WHITE}Robo a mano armada / Armed robbery{Style.RESET_ALL}")
        print(f"10. {Fore.YELLOW}Asalto a casa / Home invasion{Style.RESET_ALL}")
        print(f"11. {Fore.RED}Luchar contra policía / Fight police{Style.RESET_ALL}")
        print(f"12. {Fore.CYAN}Volver al menú / Back to main menu{Style.RESET_ALL}")
        print()
        
        choice = input(f"{Fore.CYAN}Elige actividad / Enter your choice (1-12): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.rob_store()
        elif choice == "2":
            self.deal_drugs()
        elif choice == "3":
            self.steal_car()
        elif choice == "4":
            self.gang_mission()
        elif choice == "5":
            self.bank_heist()
        elif choice == "6":
            self.kidnapping()
        elif choice == "7":
            self.extortion()
        elif choice == "8":
            self.turf_war()
        elif choice == "9":
            self.armed_robbery()
        elif choice == "10":
            self.home_invasion()
        elif choice == "11":
            self.fight_police()
        elif choice == "12":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter / Press Enter to continue...{Style.RESET_ALL}")

    def kidnapping(self):
        """Kidnapping mission for high-value targets"""
        print(f"\n{Fore.LIGHTBLUE_EX}Secuestro / Kidnapping{Style.RESET_ALL}")
        
        if self.player.respect < 40:
            print(f"{Fore.RED}Necesitas más respeto para secuestros / Need more respect for kidnapping operations.{Style.RESET_ALL}")
            return
        
        targets = [
            {"name": "Empresario Rico / Rich Businessman", "ransom": 50000, "risk": 3, "guards": 2},
            {"name": "Hijo de Político / Politician's Son", "ransom": 75000, "risk": 4, "guards": 3},
            {"name": "Esposa de Narco / Drug Lord's Wife", "ransom": 100000, "risk": 5, "guards": 4},
            {"name": "Turista Americano / American Tourist", "ransom": 25000, "risk": 2, "guards": 1}
        ]
        
        target = random.choice(targets)
        print(f"Objetivo identificado: {target['name']}")
        print(f"Rescate esperado: ${target['ransom']:,}")
        print(f"Riesgo: {'★' * target['risk']}")
        print(f"Guardaespaldas: {target['guards']}")
        
        if input("\n¿Proceder con el secuestro? / Proceed with kidnapping? (s/y or n): ").lower() in ['s', 'y']:
            success_chance = 50 - (target['risk'] * 10) + (self.player.skills['stealth'] * 5)
            
            if random.randint(1, 100) <= success_chance:
                ransom = target['ransom'] + random.randint(-5000, 10000)
                self.player.add_money(ransom)
                self.player.add_respect(target['risk'] * 3)
                self.player.stats["missions_completed"] += 1
                
                success_messages = [
                    f"'¡Secuestro exitoso! El rescate de ${ransom:,} está en camino.'",
                    f"'La familia pagó rápido. ${ransom:,} en efectivo.'",
                    f"'Operación limpia, hermano. ${ransom:,} sin problemas.'"
                ]
                print(f"{Fore.GREEN}{random.choice(success_messages)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Kidnapping successful! Ransom: ${ransom:,}{Style.RESET_ALL}")
            else:
                damage = random.randint(30, 60)
                self.player.take_damage(damage)
                self.player.increase_wanted_level(3)
                
                failure_messages = [
                    "'¡Los guardias nos vieron! ¡Vámonos!'",
                    "'¡La policía viene! ¡Aborten la misión!'",
                    "'¡Algo salió mal! ¡Retirada!'"
                ]
                print(f"{Fore.RED}{random.choice(failure_messages)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Kidnapping failed! Lost {damage} health and gained heat.{Style.RESET_ALL}")

    def extortion(self):
        """Extortion racket for protection money"""
        print(f"\n{Fore.LIGHTGREEN_EX}Extorsión / Extortion{Style.RESET_ALL}")
        
        businesses = [
            {"name": "Restaurante Local / Local Restaurant", "payment": 500, "risk": 1},
            {"name": "Tienda de Conveniencia / Convenience Store", "payment": 300, "risk": 1},
            {"name": "Discoteca / Nightclub", "payment": 1500, "risk": 2},
            {"name": "Casino Pequeño / Small Casino", "payment": 2500, "risk": 3},
            {"name": "Banco Local / Local Bank", "payment": 5000, "risk": 4}
        ]
        
        business = random.choice(businesses)
        print(f"Objetivo: {business['name']}")
        print(f"Pago semanal esperado: ${business['payment']}")
        print(f"Riesgo: {'★' * business['risk']}")
        
        extortion_lines = [
            "'Bonito negocio... sería una pena que algo le pasara.'",
            "'Necesitan protección en este barrio peligroso.'",
            "'Paguen y no tendrán problemas con nosotros.'"
        ]
        
        print(f"{Fore.YELLOW}{random.choice(extortion_lines)}{Style.RESET_ALL}")
        
        if input("\n¿Proceder con la extorsión? / Proceed with extortion? (s/y or n): ").lower() in ['s', 'y']:
            success_chance = 70 - (business['risk'] * 5) + (self.player.skills['charisma'] * 3)
            
            if random.randint(1, 100) <= success_chance:
                payment = business['payment'] + random.randint(-50, 100)
                self.player.add_money(payment)
                self.player.add_respect(2)
                
                success_responses = [
                    "'Está bien, está bien, pagaremos.'",
                    "'No queremos problemas, aquí tienen.'",
                    "'Entendemos el mensaje, tomen el dinero.'"
                ]
                print(f"{Fore.GREEN}{random.choice(success_responses)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Extortion successful! Weekly payment: ${payment}{Style.RESET_ALL}")
            else:
                self.player.increase_wanted_level(business['risk'])
                failure_responses = [
                    "'¡No les pagaremos nada! ¡Llamaremos a la policía!'",
                    "'¡Largo de aquí antes de que llamen a los federales!'",
                    "'¡Este negocio está protegido por otros!'"
                ]
                print(f"{Fore.RED}{random.choice(failure_responses)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Extortion failed! Business refused and called police.{Style.RESET_ALL}")

    def turf_war(self):
        """Territory war against rival gangs"""
        print(f"\n{Fore.LIGHTRED_EX}Guerra de Territorios / Turf War{Style.RESET_ALL}")
        
        if not self.player.gang_affiliation and not self.player.gang_name:
            print(f"{Fore.RED}Necesitas estar en una pandilla para guerras territoriales / Need gang affiliation for turf wars.{Style.RESET_ALL}")
            return
        
        rival_gangs = [gang for gang in [
            "Los Hermanos del Desierto", "Cartel de la Corona", 
            "Cártel de la Frontera Sur", "Pandilla de los Extraterrestres"
        ] if gang != self.player.gang_affiliation]
        
        rival = random.choice(rival_gangs)
        territories = ["El Centro", "Las Esquinas", "El Mercado", "La Zona Industrial", "Los Muelles"]
        territory = random.choice(territories)
        
        print(f"Guerra contra: {rival}")
        print(f"Territorio en disputa: {territory}")
        print("Recompensa: Control territorial y respeto")
        
        war_preparations = [
            "'¡Vamos a enseñarles quién manda aquí!'",
            "'Es hora de reclamar nuestro territorio.'",
            "'¡Esta guerra decidirá el futuro de la ciudad!'"
        ]
        
        print(f"{Fore.YELLOW}{random.choice(war_preparations)}{Style.RESET_ALL}")
        
        if input("\n¿Comenzar guerra territorial? / Start turf war? (s/y or n): ").lower() in ['s', 'y']:
            # Check if player has good weapons
            has_heavy_weapons = any(weapon in self.player.inventory for weapon in ["ak47", "rifle", "shotgun"])
            
            success_chance = 40 + (self.player.respect // 5)
            if has_heavy_weapons:
                success_chance += 20
            if len(self.player.gang_members) > 0:
                success_chance += len(self.player.gang_members) * 5
            
            if random.randint(1, 100) <= success_chance:
                respect_gain = random.randint(15, 25)
                money_gain = random.randint(2000, 5000)
                
                self.player.add_respect(respect_gain)
                self.player.add_money(money_gain)
                self.player.territory.append(territory)
                self.player.stats["territory_controlled"] += 1
                self.player.stats["rival_gangs_eliminated"] += 1
                
                victory_messages = [
                    f"'¡Victoria! {territory} ahora es nuestro territorio!'",
                    f"'¡{rival} huyó como cobardes! ¡{territory} es nuestro!'",
                    f"'¡Dominamos las calles! {territory} bajo nuestro control!'"
                ]
                print(f"{Fore.GREEN}{random.choice(victory_messages)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Territory conquered! +{respect_gain} respect, +${money_gain:,}{Style.RESET_ALL}")
            else:
                damage = random.randint(40, 70)
                money_lost = min(self.player.money // 4, 3000)
                
                self.player.take_damage(damage)
                self.player.remove_money(money_lost)
                self.player.increase_wanted_level(3)
                
                defeat_messages = [
                    f"'¡{rival} nos superó en número! ¡Retirada!'",
                    f"'¡Perdimos {territory}! ¡Reagrupémonos!'",
                    "'¡La guerra no terminó, volveremos más fuertes!'"
                ]
                print(f"{Fore.RED}{random.choice(defeat_messages)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Territory lost! -{damage} health, -${money_lost:,}, +3 heat{Style.RESET_ALL}")

    def gang_management(self):
        """Gang management system"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}Manejo de Pandilla / Gang Management{Style.RESET_ALL}")
        print()
        
        if not self.player.gang_affiliation and not self.player.gang_name:
            print(f"{Fore.YELLOW}No tienes afiliación de pandilla / No gang affiliation{Style.RESET_ALL}")
            print(f"1. {Fore.GREEN}Crear tu propia pandilla / Create your own gang{Style.RESET_ALL}")
            print(f"2. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
            if choice == "1":
                self.create_gang()
            return
        
        gang_name = self.player.gang_name or self.player.gang_affiliation
        print(f"Pandilla: {gang_name}")
        print(f"Miembros: {len(self.player.gang_members)}")
        print(f"Territorios: {len(self.player.territory)}")
        print(f"Reputación de pandilla: {self.player.gang_reputation}")
        print()
        
        print(f"1. {Fore.GREEN}Reclutar miembro / Recruit member{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Ver miembros / View members{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Misión de pandilla / Gang mission{Style.RESET_ALL}")
        print(f"4. {Fore.MAGENTA}Ver territorios / View territories{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Expandir pandilla / Expand gang{Style.RESET_ALL}")
        print(f"6. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.recruit_member()
        elif choice == "2":
            self.view_gang_members()
        elif choice == "3":
            self.gang_mission()
        elif choice == "4":
            self.view_territories()
        elif choice == "5":
            self.expand_gang()
        elif choice == "6":
            return

    def create_gang(self):
        """Create your own gang"""
        if self.player.respect < 50:
            print(f"{Fore.RED}Necesitas al menos 50 de respeto para crear una pandilla / Need at least 50 respect to create a gang.{Style.RESET_ALL}")
            return
        
        if self.player.money < 5000:
            print(f"{Fore.RED}Necesitas $5,000 para establecer una pandilla / Need $5,000 to establish a gang.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}Crear Tu Propia Pandilla / Create Your Own Gang{Style.RESET_ALL}")
        gang_name = input(f"{Fore.CYAN}Nombre de la pandilla / Gang name: {Style.RESET_ALL}").strip()
        
        if gang_name:
            self.player.gang_name = gang_name
            self.player.remove_money(5000)
            self.player.gang_reputation = 10
            
            creation_messages = [
                f"'¡{gang_name} ha nacido en las calles!'",
                f"'¡La pandilla {gang_name} ahora controla este territorio!'",
                f"'¡{gang_name} está lista para dominar la ciudad!'"
            ]
            
            print(f"{Fore.GREEN}{random.choice(creation_messages)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Gang '{gang_name}' created successfully!{Style.RESET_ALL}")
            print("Tu pandilla ahora puede reclutar miembros y controlar territorio.")

    def recruit_member(self):
        """Recruit new gang members"""
        if len(self.player.gang_members) >= 10:
            print(f"{Fore.RED}Tu pandilla está llena / Your gang is full (max 10 members).{Style.RESET_ALL}")
            return
        
        recruitment_cost = (len(self.player.gang_members) + 1) * 500
        
        if self.player.money < recruitment_cost:
            print(f"{Fore.RED}Necesitas ${recruitment_cost} para reclutar / Need ${recruitment_cost} to recruit.{Style.RESET_ALL}")
            return
        
        mexican_names = [
            "Carlos 'El Lobo'", "Miguel 'Cicatriz'", "José 'La Sombra'", "Roberto 'El Martillo'",
            "Diego 'Serpiente'", "Alejandro 'El Rayo'", "Fernando 'Huesos'", "Ricardo 'El Fantasma'",
            "Antonio 'Bala'", "Raúl 'El Tiburón'", "Emilio 'Navaja'", "Héctor 'El Viento'"
        ]
        
        specialties = ["Sicario", "Conductor", "Hacker", "Explosivos", "Francotirador", "Muscle"]
        
        recruit_name = random.choice(mexican_names)
        specialty = random.choice(specialties)
        loyalty = random.randint(60, 90)
        
        print(f"Recluta disponible: {recruit_name}")
        print(f"Especialidad: {specialty}")
        print(f"Lealtad inicial: {loyalty}%")
        print(f"Costo: ${recruitment_cost}")
        
        if input(f"\n¿Reclutar a {recruit_name}? / Recruit {recruit_name}? (s/y or n): ").lower() in ['s', 'y']:
            self.player.remove_money(recruitment_cost)
            
            new_member = {
                "name": recruit_name,
                "specialty": specialty,
                "loyalty": loyalty,
                "missions_completed": 0
            }
            
            self.player.gang_members.append(new_member)
            self.player.stats["gang_members_recruited"] += 1
            
            recruitment_lines = [
                f"'{recruit_name} se une a la familia!'",
                f"'Bienvenido a la pandilla, {recruit_name}!'",
                f"'{recruit_name} juró lealtad a la causa!'"
            ]
            
            print(f"{Fore.GREEN}{random.choice(recruitment_lines)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Successfully recruited {recruit_name}!{Style.RESET_ALL}")

    def view_gang_members(self):
        """View gang member details"""
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros en tu pandilla / No gang members yet.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Miembros de la Pandilla / Gang Members:{Style.RESET_ALL}")
        print()
        
        for i, member in enumerate(self.player.gang_members, 1):
            loyalty_color = Fore.GREEN if member["loyalty"] > 70 else Fore.YELLOW if member["loyalty"] > 40 else Fore.RED
            print(f"{i}. {member['name']}")
            print(f"   Especialidad: {member['specialty']}")
            print(f"   Lealtad: {loyalty_color}{member['loyalty']}%{Style.RESET_ALL}")
            print(f"   Misiones: {member['missions_completed']}")
            print()

    def view_territories(self):
        """View controlled territories"""
        if not self.player.territory:
            print(f"{Fore.YELLOW}No controlas territorios / No territories controlled yet.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Territorios Controlados / Controlled Territories:{Style.RESET_ALL}")
        for i, territory in enumerate(self.player.territory, 1):
            print(f"{i}. {territory}")

    def expand_gang(self):
        """Expand gang operations"""
        expansion_cost = len(self.player.gang_members) * 1000 + len(self.player.territory) * 2000
        
        print(f"{Fore.YELLOW}Expansión de Pandilla / Gang Expansion{Style.RESET_ALL}")
        print(f"Costo: ${expansion_cost:,}")
        print("Beneficios: Más respeto, mejor reputación, nuevas oportunidades")
        
        if self.player.money < expansion_cost:
            print(f"{Fore.RED}Dinero insuficiente / Insufficient funds.{Style.RESET_ALL}")
            return
        
        if input("\n¿Expandir operaciones? / Expand operations? (s/y or n): ").lower() in ['s', 'y']:
            self.player.remove_money(expansion_cost)
            self.player.add_respect(10)
            self.player.gang_reputation += 15
            
            expansion_results = [
                "¡La pandilla ahora controla más territorio!",
                "¡Nuevas conexiones criminales establecidas!",
                "¡Reputación en las calles mejorada!",
                "¡Más oportunidades de negocio disponibles!"
            ]
            
            print(f"{Fore.GREEN}{random.choice(expansion_results)}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Gang expansion successful! +10 respect, +15 gang reputation{Style.RESET_ALL}")

    def rob_store(self):
        """Rob a convenience store"""
        print(f"\n{Fore.YELLOW}You approach a convenience store...{Style.RESET_ALL}")
        
        # Check if player has weapon
        if "fists" in self.player.inventory and len(self.player.inventory) == 1:
            print(f"{Fore.RED}You only have your fists. This might not go well...{Style.RESET_ALL}")
        
        success_chance = 60 + (self.player.skills["stealth"] * 5)
        if random.randint(1, 100) <= success_chance:
            money_stolen = random.randint(200, 800)
            self.player.add_money(money_stolen)
            self.player.add_respect(5)
            self.player.increase_wanted_level(1)
            print(f"{Fore.GREEN}Robbery successful! You stole ${money_stolen}.{Style.RESET_ALL}")
            
            # Chance to find drugs
            if random.randint(1, 100) <= 30:
                drug = random.choice(list(DRUGS.keys()))
                amount = random.randint(1, 3)
                self.player.drugs[drug] += amount
                print(f"{Fore.MAGENTA}You also found {amount} units of {DRUGS[drug]['name']}!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}The robbery went wrong!{Style.RESET_ALL}")
            if random.randint(1, 100) <= 50:
                damage = random.randint(10, 30)
                self.player.take_damage(damage)
                print(f"{Fore.RED}You were shot and lost {damage} health!{Style.RESET_ALL}")
            
            self.player.increase_wanted_level(2)
            print(f"{Fore.RED}Police are now looking for you!{Style.RESET_ALL}")

    def deal_drugs(self):
        """Deal drugs to make money"""
        print(f"\n{Fore.GREEN}Drug dealing menu{Style.RESET_ALL}")
        print()
        
        # Show current drug inventory
        has_drugs = False
        print(f"{Fore.YELLOW}Your current stash:{Style.RESET_ALL}")
        for drug_key, amount in self.player.drugs.items():
            if amount > 0:
                drug_name = DRUGS[drug_key]["name"]
                sell_price = DRUGS[drug_key]["sell_price"]
                print(f"- {drug_name}: {amount} units (${sell_price} each)")
                has_drugs = True
        
        if not has_drugs:
            print(f"{Fore.RED}You don't have any drugs to sell.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}You need to find drugs through exploration or other criminal activities.{Style.RESET_ALL}")
            return
        
        print()
        print(f"1. {Fore.GREEN}Sell all drugs{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Sell specific drug{Style.RESET_ALL}")
        print(f"3. {Fore.CYAN}Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Enter choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            total_money = 0
            total_risk = 0
            for drug_key, amount in self.player.drugs.items():
                if amount > 0:
                    money = amount * DRUGS[drug_key]["sell_price"]
                    total_money += money
                    total_risk += DRUGS[drug_key]["risk"] * amount
                    self.player.drugs[drug_key] = 0
            
            # Risk of getting caught
            if random.randint(1, 100) <= total_risk:
                print(f"{Fore.RED}You were caught dealing drugs!{Style.RESET_ALL}")
                self.player.increase_wanted_level(2)
                total_money //= 2  # Lose half the money
                print(f"{Fore.RED}You had to dump half your stash!{Style.RESET_ALL}")
            
            self.player.add_money(total_money)
            self.player.add_respect(total_money // 50)
            self.player.stats["drugs_sold"] += 1
            print(f"{Fore.GREEN}You made ${total_money} from drug sales!{Style.RESET_ALL}")

    def steal_car(self):
        """Steal a random car"""
        print(f"\n{Fore.BLUE}Looking for a car to steal...{Style.RESET_ALL}")
        
        # Different success rates based on car type
        available_cars = list(VEHICLES.keys())
        car_weights = [30, 20, 25, 10, 15, 12]  # Easier cars have higher weights
        
        target_car = random.choices(available_cars, weights=car_weights)[0]
        car_info = VEHICLES[target_car]
        
        print(f"You spot a {car_info['name']}...")
        
        # Success chance based on player's driving skill and car reliability
        success_chance = 50 + (self.player.skills["driving"] * 10) - (car_info["reliability"] // 10)
        
        if random.randint(1, 100) <= success_chance:
            # Abandon current vehicle if any
            if self.player.vehicle and self.player.vehicle in VEHICLES:
                old_vehicle = VEHICLES[self.player.vehicle]["name"]
                print(f"You abandon your {old_vehicle}.")
            
            self.player.vehicle = target_car
            self.player.add_respect(3)
            self.player.stats["cars_stolen"] += 1
            self.player.skills["driving"] = min(10, self.player.skills["driving"] + 1)
            
            print(f"{Fore.GREEN}Successfully stole the {car_info['name']}!{Style.RESET_ALL}")
            
            # Chance of being spotted
            if random.randint(1, 100) <= 30:
                self.player.increase_wanted_level(1)
                print(f"{Fore.YELLOW}Someone saw you steal the car!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Car theft failed!{Style.RESET_ALL}")
            if random.randint(1, 100) <= 40:
                print(f"{Fore.RED}The car alarm attracted police attention!{Style.RESET_ALL}")
                self.player.increase_wanted_level(2)

    def gang_mission(self):
        """Gang-related missions"""
        print(f"\n{Fore.MAGENTA}Gang Missions{Style.RESET_ALL}")
        
        if not self.player.gang_affiliation:
            print(f"{Fore.YELLOW}You're not affiliated with any gang yet.{Style.RESET_ALL}")
            print("Complete more criminal activities to attract gang attention.")
            return
        
        # Generate random gang mission
        missions = [
            {"name": "Turf War", "reward": 500, "risk": 3},
            {"name": "Drug Delivery", "reward": 300, "risk": 2},
            {"name": "Rival Gang Hit", "reward": 800, "risk": 4},
            {"name": "Protection Racket", "reward": 400, "risk": 2}
        ]
        
        mission = random.choice(missions)
        print(f"Mission: {mission['name']}")
        print(f"Reward: ${mission['reward']}")
        print(f"Risk Level: {'★' * mission['risk']}")
        
        if input("\nAccept mission? (y/n): ").lower() == 'y':
            success_chance = 70 - (mission['risk'] * 10) + (self.player.respect // 10)
            
            if random.randint(1, 100) <= success_chance:
                self.player.add_money(mission['reward'])
                self.player.add_respect(mission['risk'] * 5)
                self.player.stats["missions_completed"] += 1
                print(f"{Fore.GREEN}Mission successful! You earned ${mission['reward']}.{Style.RESET_ALL}")
            else:
                damage = random.randint(20, 50)
                self.player.take_damage(damage)
                self.player.increase_wanted_level(mission['risk'])
                print(f"{Fore.RED}Mission failed! You lost {damage} health and gained heat.{Style.RESET_ALL}")

    def bank_heist(self):
        """High-risk, high-reward bank robbery"""
        print(f"\n{Fore.RED}Planning a bank heist...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This is extremely dangerous but potentially very profitable.{Style.RESET_ALL}")
        
        if self.player.respect < 50:
            print(f"{Fore.RED}You need more street cred for a job this big. (Need 50+ respect){Style.RESET_ALL}")
            return
        
        # Check for good weapons
        has_good_weapon = any(weapon in self.player.inventory for weapon in ["rifle", "shotgun", "smg"])
        if not has_good_weapon:
            print(f"{Fore.RED}You need better weapons for a bank job.{Style.RESET_ALL}")
            return
        
        if input("\nProceed with bank heist? (y/n): ").lower() == 'y':
            # Very low success chance but huge reward
            success_chance = 25 + (self.player.skills["shooting"] * 5)
            
            if random.randint(1, 100) <= success_chance:
                money_stolen = random.randint(10000, 50000)
                self.player.add_money(money_stolen)
                self.player.add_respect(50)
                self.player.stats["missions_completed"] += 1
                print(f"{Fore.GREEN}BANK HEIST SUCCESSFUL!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}You stole ${money_stolen:,}!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}You're now a legend in the criminal underworld!{Style.RESET_ALL}")
            else:
                damage = random.randint(40, 80)
                self.player.take_damage(damage)
                self.player.increase_wanted_level(5)  # Maximum heat
                money_lost = min(self.player.money // 2, 5000)
                self.player.remove_money(money_lost)
                print(f"{Fore.RED}BANK HEIST FAILED!{Style.RESET_ALL}")
                print(f"{Fore.RED}You lost {damage} health, ${money_lost}, and now have maximum heat!{Style.RESET_ALL}")

    def vehicle_management(self):
        """Manage player's vehicle"""
        self.display_header()
        print(f"{Fore.BLUE}Vehicle Management{Style.RESET_ALL}")
        print()
        
        if not self.player.vehicle:
            print(f"{Fore.YELLOW}You don't have a vehicle.{Style.RESET_ALL}")
            print("Steal a car or buy one to get around faster.")
        else:
            if self.player.vehicle in VEHICLES:
                vehicle_info = VEHICLES[self.player.vehicle]
                print(f"Current Vehicle: {vehicle_info['name']}")
                print(f"Speed: {'★' * vehicle_info['speed']}")
                print(f"Reliability: {vehicle_info['reliability']}%")
                print(f"Value: ${vehicle_info['value']:,}")
                print()
            else:
                print(f"{Fore.RED}Invalid vehicle data{Style.RESET_ALL}")
                self.player.vehicle = None
            
            print(f"1. {Fore.GREEN}Sell vehicle{Style.RESET_ALL}")
            print(f"2. {Fore.YELLOW}Abandon vehicle{Style.RESET_ALL}")
            print(f"3. {Fore.CYAN}Back{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Enter choice: {Style.RESET_ALL}").strip()
            
            if choice == "1" and self.player.vehicle and self.player.vehicle in VEHICLES:
                vehicle_info = VEHICLES[self.player.vehicle]
                sell_price = vehicle_info['value'] // 2
                self.player.add_money(sell_price)
                vehicle_name = vehicle_info['name']
                self.player.vehicle = None
                print(f"{Fore.GREEN}Sold {vehicle_name} for ${sell_price}.{Style.RESET_ALL}")
            elif choice == "2" and self.player.vehicle and self.player.vehicle in VEHICLES:
                vehicle_info = VEHICLES[self.player.vehicle]
                vehicle_name = vehicle_info['name']
                self.player.vehicle = None
                print(f"{Fore.YELLOW}Abandoned {vehicle_name}.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def visit_locations(self):
        """Visit different locations in the city"""
        self.display_header()
        print(f"{Fore.MAGENTA}Available Locations{Style.RESET_ALL}")
        print()
        
        locations = [
            ("Gun Shop", self.gun_shop),
            ("Hospital", self.hospital),
            ("Black Market", self.black_market),
            ("Police Station", self.police_station),
            ("Travel to Another City", self.travel_city)
        ]
        
        for i, (name, _) in enumerate(locations, 1):
            print(f"{i}. {name}")
        
        print(f"{len(locations) + 1}. Back to main menu")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}Enter choice: {Style.RESET_ALL}"))
            if 1 <= choice <= len(locations):
                locations[choice - 1][1]()
            elif choice == len(locations) + 1:
                return
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def gun_shop(self):
        """Visit the gun shop"""
        print(f"\n{Fore.YELLOW}Welcome to the Gun Shop{Style.RESET_ALL}")
        
        if self.player.wanted_level >= 3:
            print(f"{Fore.RED}The shop owner recognizes you and refuses service!{Style.RESET_ALL}")
            return
        
        print("\nAvailable weapons:")
        available_weapons = ["knife", "pistol", "shotgun", "rifle", "smg"]
        
        for weapon in available_weapons:
            weapon_info = WEAPONS[weapon]
            owned = " (OWNED)" if weapon in self.player.inventory else ""
            print(f"- {weapon_info['name']}: ${weapon_info['price']} (Damage: {weapon_info['damage']}){owned}")
        
        weapon_choice = input("\nEnter weapon name to buy (or 'back'): ").lower().strip()
        
        if weapon_choice == "back":
            return
        
        if weapon_choice in available_weapons:
            weapon_info = WEAPONS[weapon_choice]
            if weapon_choice in self.player.inventory:
                print(f"{Fore.YELLOW}You already own this weapon.{Style.RESET_ALL}")
            elif self.player.remove_money(weapon_info['price']):
                self.player.inventory[weapon_choice] = 1
                print(f"{Fore.GREEN}Purchased {weapon_info['name']}!{Style.RESET_ALL}")
                
                # Add some ammo if applicable
                if weapon_info['ammo']:
                    self.player.ammo[weapon_info['ammo']] += 50
                    print(f"Received 50 rounds of {weapon_info['ammo']} ammo.")
            else:
                print(f"{Fore.RED}Not enough money.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Weapon not available.{Style.RESET_ALL}")

    def hospital(self):
        """Visit the hospital to heal"""
        print(f"\n{Fore.GREEN}City Hospital{Style.RESET_ALL}")
        
        if self.player.health == self.player.max_health:
            print("You're already at full health.")
            return
        
        heal_cost = (self.player.max_health - self.player.health) * 10
        print(f"Healing cost: ${heal_cost}")
        print(f"Current health: {self.player.health}/{self.player.max_health}")
        
        if input("Pay for treatment? (y/n): ").lower() == 'y':
            if self.player.remove_money(heal_cost):
                self.player.heal(self.player.max_health)
                print(f"{Fore.GREEN}Fully healed!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Not enough money.{Style.RESET_ALL}")

    def black_market(self):
        """Visit the black market"""
        print(f"\n{Fore.MAGENTA}Black Market{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Shady deals and illegal goods...{Style.RESET_ALL}")
        
        if self.player.respect < 20:
            print(f"{Fore.RED}You don't have enough street cred to access the black market.{Style.RESET_ALL}")
            return
        
        print("\n1. Buy drugs")
        print("2. Sell stolen goods")
        print("3. Hire mercenary")
        print("4. Back")
        
        choice = input(f"\n{Fore.CYAN}Enter choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Buy drugs
            print("\nAvailable drugs:")
            for drug_key, drug_info in DRUGS.items():
                print(f"- {drug_info['name']}: ${drug_info['buy_price']} per unit")
            
            drug_choice = input("Enter drug name to buy: ").lower().strip()
            if drug_choice in DRUGS:
                try:
                    amount = int(input("How many units? "))
                    total_cost = DRUGS[drug_choice]['buy_price'] * amount
                    
                    if self.player.remove_money(total_cost):
                        self.player.drugs[drug_choice] += amount
                        print(f"{Fore.GREEN}Bought {amount} units of {DRUGS[drug_choice]['name']}.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Not enough money.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid amount.{Style.RESET_ALL}")

    def police_station(self):
        """Visit police station (risky!)"""
        print(f"\n{Fore.BLUE}Police Station{Style.RESET_ALL}")
        
        if self.player.wanted_level == 0:
            print("The police don't seem interested in you.")
            return
        
        print(f"{Fore.RED}This is very risky with your current wanted level!{Style.RESET_ALL}")
        
        if self.player.wanted_level >= 3:
            print(f"{Fore.RED}You are immediately arrested!{Style.RESET_ALL}")
            self.get_arrested()
            return
        
        if random.randint(1, 100) <= self.player.wanted_level * 20:
            print(f"{Fore.RED}Police recognize you and arrest you!{Style.RESET_ALL}")
            self.get_arrested()

    def travel_city(self):
        """Travel to another city"""
        print(f"\n{Fore.YELLOW}Travel to Another City{Style.RESET_ALL}")
        
        if not self.player.vehicle:
            print(f"{Fore.RED}You need a vehicle to travel between cities.{Style.RESET_ALL}")
            return
        
        current_city = self.player.location
        available_cities = [city for city in CITIES.keys() if city != current_city]
        
        print("\nAvailable destinations:")
        for i, city in enumerate(available_cities, 1):
            danger = "★" * CITIES[city]["danger_level"]
            print(f"{i}. {city} - {CITIES[city]['description']} (Danger: {danger})")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}Enter choice (0 to cancel): {Style.RESET_ALL}"))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_cities):
                destination = available_cities[choice - 1]
                
                # Travel time and risk
                travel_cost = 50
                if self.player.remove_money(travel_cost):
                    print(f"Traveling to {destination}...")
                    time.sleep(2)
                    
                    self.player.location = destination
                    self.player.district = CITIES[destination]["districts"][0]
                    
                    # Random encounter during travel
                    if random.randint(1, 100) <= 20:
                        self.travel_encounter()
                    
                    print(f"{Fore.GREEN}Arrived in {destination}!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Not enough money for travel (${travel_cost} needed).{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")

    def travel_encounter(self):
        """Random encounter during travel"""
        encounters = [
            "You encounter a police roadblock but manage to avoid it.",
            "Your vehicle breaks down but you fix it quickly.",
            "You help a stranded motorist and gain respect.",
            "Rival gang members spot you but you escape.",
            "You find abandoned cargo with valuable items."
        ]
        
        encounter = random.choice(encounters)
        print(f"{Fore.YELLOW}{encounter}{Style.RESET_ALL}")
        
        # Apply encounter effects
        if "respect" in encounter:
            self.player.add_respect(5)
        elif "cargo" in encounter:
            money_found = random.randint(100, 500)
            self.player.add_money(money_found)
            print(f"Found ${money_found}!")

    def character_status(self):
        """Display detailed character information"""
        self.display_header()
        print(f"{Fore.CYAN}Character Status{Style.RESET_ALL}")
        print()
        
        # Basic stats
        print(f"{Fore.YELLOW}Basic Information:{Style.RESET_ALL}")
        print(f"Name: {self.player.name}")
        
        # Display gender with appropriate translation
        gender_display = {
            "male": "Hombre / Male",
            "female": "Mujer / Female", 
            "non-binary": "No binario / Non-binary",
            "undisclosed": "Prefiero no decir / Prefer not to say",
            "unknown": "No especificado / Not specified"
        }
        print(f"Gender: {gender_display.get(self.player.gender, 'No especificado / Not specified')}")
        print(f"Age: {self.player.age} años / years")
        
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Money: ${self.player.money:,}")
        print(f"Respect: {self.player.respect}")
        print(f"Wanted Level: {'★' * self.player.wanted_level}{'☆' * (5 - self.player.wanted_level)}")
        
        # Police career status
        if self.player.is_police:
            print(f"Police Career: {self.player.police_rank}")
            print(f"Good Deeds: {self.player.good_deeds}")
            print(f"Criminals Stopped: {self.player.criminals_stopped}")
            print(f"Total Arrests: {self.player.total_arrests}")
            if self.player.police_corruption > 0:
                print(f"Corruption: {self.player.police_corruption}%")
        
        print()
        
        # Skills
        print(f"{Fore.GREEN}Skills:{Style.RESET_ALL}")
        for skill, level in self.player.skills.items():
            stars = "★" * level + "☆" * (10 - level)
            print(f"{skill.capitalize()}: {stars} ({level}/10)")
        print()
        
        # Inventory
        print(f"{Fore.BLUE}Weapons:{Style.RESET_ALL}")
        for weapon in self.player.inventory:
            weapon_info = WEAPONS[weapon]
            print(f"- {weapon_info['name']} (Damage: {weapon_info['damage']})")
        print()
        
        # Ammo
        print(f"{Fore.MAGENTA}Ammunition:{Style.RESET_ALL}")
        for ammo_type, amount in self.player.ammo.items():
            if amount > 0:
                print(f"- {ammo_type}: {amount} rounds")
        print()
        
        # Drugs
        print(f"{Fore.RED}Drugs:{Style.RESET_ALL}")
        for drug_key, amount in self.player.drugs.items():
            if amount > 0:
                drug_name = DRUGS[drug_key]["name"]
                print(f"- {drug_name}: {amount} units")
        print()
        
        # Vehicle
        if self.player.vehicle and self.player.vehicle in VEHICLES:
            vehicle_info = VEHICLES[self.player.vehicle]
            print(f"{Fore.YELLOW}Vehicle: {vehicle_info['name']}{Style.RESET_ALL}")
            print(f"Speed: {'★' * vehicle_info['speed']}")
            print(f"Reliability: {vehicle_info['reliability']}%")
            print()
        
        # Statistics
        print(f"{Fore.CYAN}Statistics:{Style.RESET_ALL}")
        for stat, value in self.player.stats.items():
            stat_name = stat.replace('_', ' ').title()
            print(f"{stat_name}: {value}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    # Random encounter methods
    def random_mugger(self):
        """Random mugger encounter"""
        print(f"{Fore.RED}A mugger approaches you with a knife!{Style.RESET_ALL}")
        
        print("\n1. Fight back")
        print("2. Run away")
        print("3. Give money")
        
        choice = input(f"\n{Fore.CYAN}What do you do? {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Fight
            if random.randint(1, 100) <= 60 + self.player.skills["strength"] * 5:
                money_gained = random.randint(50, 200)
                self.player.add_money(money_gained)
                self.player.add_respect(3)
                print(f"{Fore.GREEN}You defeated the mugger and took ${money_gained}!{Style.RESET_ALL}")
                self.player.stats["people_killed"] += 1
            else:
                damage = random.randint(15, 35)
                money_lost = min(self.player.money // 4, 300)
                self.player.take_damage(damage)
                self.player.remove_money(money_lost)
                print(f"{Fore.RED}The mugger hurt you and took ${money_lost}!{Style.RESET_ALL}")
                
        elif choice == "2":
            # Run
            if self.player.vehicle or random.randint(1, 100) <= 70:
                print(f"{Fore.YELLOW}You successfully escaped!{Style.RESET_ALL}")
            else:
                damage = random.randint(5, 15)
                self.player.take_damage(damage)
                print(f"{Fore.RED}The mugger caught you and hurt you!{Style.RESET_ALL}")
                
        elif choice == "3":
            # Give money
            money_lost = min(self.player.money // 3, 200)
            self.player.remove_money(money_lost)
            print(f"{Fore.YELLOW}You gave the mugger ${money_lost} and they left.{Style.RESET_ALL}")

    def find_money(self):
        """Find random money"""
        money_found = random.randint(20, 150)
        self.player.add_money(money_found)
        locations = ["abandoned wallet", "dropped envelope", "old stash", "lottery ticket"]
        location = random.choice(locations)
        print(f"{Fore.GREEN}You found ${money_found} in an {location}!{Style.RESET_ALL}")

    def police_patrol(self):
        """Police patrol encounter"""
        if self.player.wanted_level == 0:
            print(f"{Fore.BLUE}A police car drives by, but they don't notice you.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.RED}Police patrol spotted you!{Style.RESET_ALL}")
        
        if self.player.vehicle:
            print("\n1. Try to outrun them")
            print("2. Surrender")
            
            choice = input(f"\n{Fore.CYAN}What do you do? {Style.RESET_ALL}").strip()
            
            if choice == "1":
                # Chase scene
                if self.player.vehicle and self.player.vehicle in VEHICLES:
                    vehicle_speed = VEHICLES[self.player.vehicle]["speed"]
                    escape_chance = 30 + (vehicle_speed * 15) + (self.player.skills["driving"] * 5)
                else:
                    escape_chance = 20  # No vehicle or invalid vehicle
                
                if random.randint(1, 100) <= escape_chance:
                    print(f"{Fore.GREEN}You successfully outran the police!{Style.RESET_ALL}")
                    self.player.skills["driving"] = min(10, self.player.skills["driving"] + 1)
                else:
                    print(f"{Fore.RED}The police caught you after a chase!{Style.RESET_ALL}")
                    self.get_arrested()
            else:
                print(f"{Fore.YELLOW}You surrender to the police.{Style.RESET_ALL}")
                self.get_arrested()
        else:
            # On foot - harder to escape
            if random.randint(1, 100) <= 20:
                print(f"{Fore.GREEN}You managed to hide and avoid the police!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}The police caught you!{Style.RESET_ALL}")
                self.get_arrested()

    def drug_dealer(self):
        """Meet a drug dealer with Mexican street culture"""
        dealer_introductions = [
            "Un narcomenudista se acerca sigilosamente...",
            "Un dealer te hace señas desde una esquina...",
            "Un vendedor susurra tu nombre..."
        ]
        
        print(f"{Fore.MAGENTA}{random.choice(dealer_introductions)}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}A drug dealer approaches you...{Style.RESET_ALL}")
        
        drug = random.choice(list(DRUGS.keys()))
        drug_info = DRUGS[drug]
        amount = random.randint(1, 5)
        price = drug_info["buy_price"] * amount
        
        # Spanish drug slang
        dealer_offers = [
            f"'Oye carnal, tengo {drug_info['spanish']} de calidad. {amount} piezas por ${price}.'",
            f"'¿Buscas {drug_info['spanish']}? Tengo {amount} gramos frescos por ${price}.'",
            f"'Mercancía buena, hermano. {drug_info['spanish']} directo de {drug_info['origin']}. ${price} por {amount} piezas.'"
        ]
        
        print(f"{Fore.YELLOW}{random.choice(dealer_offers)}{Style.RESET_ALL}")
        print(f"They offer {amount} units of {drug_info['name']} for ${price}.")
        
        if input("¿Comprar la mercancía? / Buy the drugs? (s/y or n): ").lower() in ['s', 'y']:
            if self.player.remove_money(price):
                self.player.drugs[drug] += amount
                success_phrases = [
                    "'Buen negocio, carnal. Nos vemos por aquí.'",
                    "'Placer hacer negocios contigo, hermano.'",
                    "'Que disfrutes la mercancía, y recomiéndanos.'"
                ]
                print(f"{Fore.GREEN}{random.choice(success_phrases)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Transaction complete! / ¡Transacción completa!{Style.RESET_ALL}")
                
                # Small chance of police sting
                if random.randint(1, 100) <= 10:
                    sting_reveals = [
                        "'¡Policía! ¡Al suelo!'",
                        "'¡Quedas arrestado por posesión!'",
                        "'¡Era una trampa, cabrón!'"
                    ]
                    print(f"{Fore.RED}{random.choice(sting_reveals)}{Style.RESET_ALL}")
                    print(f"{Fore.RED}It was a police sting! You're in trouble! / ¡Era una trampa policial!{Style.RESET_ALL}")
                    self.player.increase_wanted_level(2)
            else:
                poor_responses = [
                    "'No tienes suficiente varo, hermano.'",
                    "'Vuelve cuando tengas la lana completa.'",
                    "'Sin dinero no hay trato, carnal.'"
                ]
                print(f"{Fore.RED}{random.choice(poor_responses)}{Style.RESET_ALL}")
                print(f"{Fore.RED}You don't have enough money. / No tienes suficiente dinero.{Style.RESET_ALL}")

    def gang_member(self):
        """Meet a gang member"""
        gangs = ["Los Hermanos", "Desert Vipers", "Albuquerque Cartel", "Santa Fe Syndicate"]
        gang = random.choice(gangs)
        
        print(f"{Fore.MAGENTA}A member of {gang} approaches you...{Style.RESET_ALL}")
        
        if self.player.respect >= 30 and not self.player.gang_affiliation:
            print(f"They offer you membership in {gang}!")
            if input(f"Join {gang}? (y/n): ").lower() == 'y':
                self.player.gang_affiliation = gang
                self.player.add_respect(20)
                print(f"{Fore.GREEN}You are now a member of {gang}!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Gang missions are now available.{Style.RESET_ALL}")
        elif self.player.gang_affiliation == gang:
            print(f"They nod respectfully at a fellow {gang} member.")
            self.player.add_respect(2)
        elif self.player.gang_affiliation and self.player.gang_affiliation != gang:
            print(f"{Fore.RED}They recognize you as a rival gang member!{Style.RESET_ALL}")
            if random.randint(1, 100) <= 40:
                print(f"{Fore.RED}A fight breaks out!{Style.RESET_ALL}")
                damage = random.randint(20, 40)
                self.player.take_damage(damage)
                print(f"{Fore.RED}You lost {damage} health!{Style.RESET_ALL}")
        else:
            print("They size you up but don't seem impressed.")
            print("(Need more respect to join a gang)")

    def nothing_happens(self):
        """Nothing interesting happens"""
        events = [
            "You walk around but nothing interesting happens.",
            "The streets are quiet today.",
            "You observe the city life around you.",
            "A peaceful moment in your chaotic life.",
            "You take time to plan your next move."
        ]
        event = random.choice(events)
        print(f"{Fore.WHITE}{event}{Style.RESET_ALL}")

    def get_arrested(self):
        """Handle getting arrested"""
        print(f"\n{Fore.RED}You have been arrested!{Style.RESET_ALL}")
        
        # Consequences of arrest
        bail_amount = self.player.wanted_level * 1000
        time_served = self.player.wanted_level
        
        # Lose some money and items
        money_lost = min(self.player.money // 3, bail_amount)
        self.player.remove_money(money_lost)
        
        # Lose all drugs (confiscated)
        drugs_lost = sum(self.player.drugs.values()) > 0
        if drugs_lost:
            for drug in self.player.drugs:
                self.player.drugs[drug] = 0
            print(f"{Fore.RED}All your drugs were confiscated!{Style.RESET_ALL}")
        
        # Lose vehicle if stolen
        if self.player.vehicle:
            self.player.vehicle = None
            print(f"{Fore.RED}Your vehicle was impounded!{Style.RESET_ALL}")
        
        # Reset wanted level but increase arrest count
        self.player.wanted_level = 0
        self.player.stats["times_arrested"] += 1
        
        print(f"Bail paid: ${money_lost}")
        print(f"Time served: {time_served} days")
        print(f"{Fore.YELLOW}You are released but your reputation took a hit.{Style.RESET_ALL}")
        
        self.player.respect = max(0, self.player.respect - 10)

    def save_game(self):
        """Save the current game state"""
        try:
            game_data = {
                "player": {
                    "name": self.player.name,
                    "gender": self.player.gender,
                    "age": self.player.age,
                    "health": self.player.health,
                    "max_health": self.player.max_health,
                    "money": self.player.money,
                    "respect": self.player.respect,
                    "wanted_level": self.player.wanted_level,
                    "location": self.player.location,
                    "district": self.player.district,
                    "inventory": self.player.inventory,
                    "ammo": self.player.ammo,
                    "drugs": self.player.drugs,
                    "vehicle": self.player.vehicle,
                    "gang_affiliation": self.player.gang_affiliation,
                    "stats": self.player.stats,
                    "skills": self.player.skills,
                    # Police career attributes
                    "is_police": self.player.is_police,
                    "police_rank": self.player.police_rank,
                    "police_corruption": self.player.police_corruption,
                    "total_arrests": self.player.total_arrests,
                    "police_operations_completed": self.player.police_operations_completed,
                    "good_deeds": self.player.good_deeds,
                    "criminals_stopped": self.player.criminals_stopped
                },
                "game_time": self.game_time,
                "save_timestamp": datetime.now().isoformat()
            }
            
            with open(SAVE_FILE, 'w') as f:
                json.dump(game_data, f, indent=2)
            
            print(f"{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Error saving game: {e}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def load_game(self):
        """Load a saved game state"""
        try:
            if not os.path.exists(SAVE_FILE):
                print(f"{Fore.RED}No save file found.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                return
            
            with open(SAVE_FILE, 'r') as f:
                game_data = json.load(f)
            
            # Restore player data
            player_data = game_data["player"]
            self.player.name = player_data["name"]
            self.player.gender = player_data.get("gender", "unknown")
            self.player.age = player_data.get("age", 25)
            self.player.health = player_data["health"]
            self.player.max_health = player_data["max_health"]
            self.player.money = player_data["money"]
            self.player.respect = player_data["respect"]
            self.player.wanted_level = player_data["wanted_level"]
            self.player.location = player_data["location"]
            self.player.district = player_data["district"]
            self.player.inventory = player_data["inventory"]
            self.player.ammo = player_data["ammo"]
            self.player.drugs = player_data["drugs"]
            self.player.vehicle = player_data["vehicle"]
            self.player.gang_affiliation = player_data["gang_affiliation"]
            self.player.stats = player_data["stats"]
            self.player.skills = player_data["skills"]
            
            # Restore police career attributes
            self.player.is_police = player_data.get("is_police", False)
            self.player.police_rank = player_data.get("police_rank", None)
            self.player.police_corruption = player_data.get("police_corruption", 0)
            self.player.total_arrests = player_data.get("total_arrests", 0)
            self.player.police_operations_completed = player_data.get("police_operations_completed", 0)
            self.player.good_deeds = player_data.get("good_deeds", 0)
            self.player.criminals_stopped = player_data.get("criminals_stopped", 0)
            
            self.game_time = game_data["game_time"]
            self.language = game_data.get("language", "bilingual")
            
            save_time = game_data.get("save_timestamp", "Unknown")
            print(f"{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
            print(f"Save date: {save_time}")
            
        except Exception as e:
            print(f"{Fore.RED}Error loading game: {e}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def quit_game(self):
        """Quit the game"""
        print(f"\n{Fore.YELLOW}¡Gracias por jugar Mexican Gangsters!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Thanks for playing Mexican Gangsters!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Tu imperio criminal en Nuevo México te espera...{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Your criminal empire in New Mexico awaits your return...{Style.RESET_ALL}")
        
        if input("\nSave before quitting? (y/n): ").lower() == 'y':
            self.save_game()
        
        self.running = False

    def handle_death(self):
        """Handle player death"""
        self.clear_screen()
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.RED}           WASTED / HAS MUERTO{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print()
        
        death_messages = [
            "Las calles de Nuevo México cobraron otra víctima...",
            "Tu imperio criminal ha llegado a su fin...",
            "La vida del crimen finalmente te alcanzó...",
            "Otro gangster caído en las guerras del hampa..."
        ]
        
        print(f"{Fore.YELLOW}{random.choice(death_messages)}{Style.RESET_ALL}")
        print("The streets of New Mexico claimed another victim...")
        print()
        
        # Show final stats
        print("Estadísticas Finales / Final Stats:")
        print(f"Dinero total ganado: ${self.player.stats['money_earned']:,}")
        print(f"Misiones completadas: {self.player.stats['missions_completed']}")
        print(f"Respeto máximo: {self.player.respect}")
        print(f"Nivel alcanzado: {self.player.level}")
        
        if self.player.gang_name:
            print(f"Lideró la pandilla: {self.player.gang_name}")
        if self.player.territory:
            print(f"Territorios controlados: {len(self.player.territory)}")
        
        print()
        respawn_choice = input(f"{Fore.CYAN}¿Renacer en el hospital? / Respawn at hospital? (s/y or n): {Style.RESET_ALL}").lower()
        
        if respawn_choice in ['s', 'y']:
            # Respawn with penalties
            self.player.health = 50  # Half health
            self.player.money = max(100, self.player.money // 2)  # Lose half money
            self.player.wanted_level = 0  # Clear wanted level
            
            # Lose some weapons
            weapons_to_lose = ["rpg", "sniper", "ak47"]
            for weapon in weapons_to_lose:
                if weapon in self.player.inventory:
                    del self.player.inventory[weapon]
            
            # Reset ammo
            for ammo_type in self.player.ammo:
                self.player.ammo[ammo_type] = max(0, self.player.ammo[ammo_type] // 2)
            
            print(f"{Fore.GREEN}Has renacido en el hospital con penalizaciones...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}You respawned at the hospital with penalties...{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
        else:
            self.running = False

    def armed_robbery(self):
        """Armed robbery of various targets"""
        print(f"\n{Fore.WHITE}Robo a Mano Armada / Armed Robbery{Style.RESET_ALL}")
        
        targets = [
            {"name": "Camión de Valores / Armored Truck", "reward": 25000, "risk": 5, "guards": 4},
            {"name": "Joyería / Jewelry Store", "reward": 15000, "risk": 3, "guards": 2},
            {"name": "Farmacia / Pharmacy", "reward": 5000, "risk": 2, "guards": 1},
            {"name": "Gasolinera / Gas Station", "reward": 2000, "risk": 1, "guards": 1},
            {"name": "Restaurante Caro / Expensive Restaurant", "reward": 8000, "risk": 2, "guards": 1}
        ]
        
        target = random.choice(targets)
        print(f"Objetivo: {target['name']}")
        print(f"Recompensa estimada: ${target['reward']:,}")
        print(f"Riesgo: {'★' * target['risk']}")
        print(f"Seguridad: {target['guards']} guardias")
        
        # Check if player has weapon
        has_weapon = any(weapon in self.player.inventory for weapon in ["pistol", "shotgun", "rifle", "ak47"])
        if not has_weapon:
            print(f"{Fore.RED}¡Necesitas un arma para robos a mano armada! / Need a weapon for armed robbery!{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        robbery_lines_spanish = [
            "'¡Todo el mundo al suelo! ¡Esto es un asalto!'",
            "'¡Manos arriba! ¡Den todo el dinero!'",
            "'¡Nadie se mueva y nadie sale lastimado!'"
        ]
        
        robbery_lines_english = [
            "'Everyone on the ground! This is a robbery!'",
            "'Hands up! Give me all the money!'",
            "'Nobody move and nobody gets hurt!'"
        ]
        
        if self.language == "spanish":
            print(f"{Fore.YELLOW}{random.choice(robbery_lines_spanish)}{Style.RESET_ALL}")
        elif self.language == "english":
            print(f"{Fore.YELLOW}{random.choice(robbery_lines_english)}{Style.RESET_ALL}")
        else:  # bilingual
            print(f"{Fore.YELLOW}{random.choice(robbery_lines_spanish)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{random.choice(robbery_lines_english)}{Style.RESET_ALL}")
        
        if input("\n¿Proceder con el robo? / Proceed with robbery? (s/y or n): ").lower() in ['s', 'y']:
            success_chance = 60 - (target['risk'] * 8) + (self.player.skills['shooting'] * 4)
            
            if random.randint(1, 100) <= success_chance:
                money_stolen = target['reward'] + random.randint(-2000, 5000)
                self.player.add_money(money_stolen)
                self.player.add_respect(target['risk'] * 2)
                self.player.add_experience(target['risk'] * 15)
                self.player.increase_wanted_level(target['risk'])
                
                success_messages = [
                    f"'¡Robo exitoso! ${money_stolen:,} en nuestras manos!'",
                    f"'¡Fácil dinero! ${money_stolen:,} sin complicaciones!'",
                    f"'¡Como quitarle dulces a un niño! ${money_stolen:,}!'"
                ]
                
                print(f"{Fore.GREEN}{random.choice(success_messages)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Armed robbery successful! Stolen: ${money_stolen:,}{Style.RESET_ALL}")
                
                if self.player.add_experience(target['risk'] * 15):
                    print(f"{Fore.CYAN}¡Has subido de nivel! / You leveled up!{Style.RESET_ALL}")
            else:
                damage = random.randint(20, 50)
                self.player.take_damage(damage)
                self.player.increase_wanted_level(target['risk'] + 1)
                
                failure_messages = [
                    "'¡Los guardias respondieron! ¡Vámonos!'",
                    "'¡Alarma silenciosa! ¡La policía viene!'",
                    "'¡Algo salió mal! ¡Aborten la misión!'"
                ]
                
                print(f"{Fore.RED}{random.choice(failure_messages)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Armed robbery failed! Lost {damage} health and gained heat.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def home_invasion(self):
        """Home invasion for valuable loot"""
        print(f"\n{Fore.YELLOW}Asalto a Casa / Home Invasion{Style.RESET_ALL}")
        
        houses = [
            {"name": "Mansión Rica / Rich Mansion", "loot": 20000, "risk": 4, "alarm": True},
            {"name": "Casa Suburbana / Suburban House", "loot": 8000, "risk": 2, "alarm": False},
            {"name": "Apartamento de Lujo / Luxury Apartment", "loot": 12000, "risk": 3, "alarm": True},
            {"name": "Casa de Playa / Beach House", "loot": 15000, "risk": 3, "alarm": False}
        ]
        
        house = random.choice(houses)
        print(f"Objetivo: {house['name']}")
        print(f"Botín estimado: ${house['loot']:,}")
        print(f"Riesgo: {'★' * house['risk']}")
        print(f"Sistema de alarma: {'Sí' if house['alarm'] else 'No'}")
        
        invasion_preparations = [
            "'Casa vacía, es nuestra oportunidad.'",
            "'Entramos rápido, tomamos todo y nos vamos.'",
            "'Silencio total, no queremos despertar a nadie.'"
        ]
        
        print(f"{Fore.YELLOW}{random.choice(invasion_preparations)}{Style.RESET_ALL}")
        
        if input("\n¿Proceder con el asalto? / Proceed with invasion? (s/y or n): ").lower() in ['s', 'y']:
            success_chance = 70 - (house['risk'] * 10) + (self.player.skills['stealth'] * 6)
            if house['alarm']:
                success_chance -= 15
            
            if random.randint(1, 100) <= success_chance:
                loot_value = house['loot'] + random.randint(-3000, 8000)
                items_found = random.choice([
                    "joyas y electrónicos / jewelry and electronics",
                    "efectivo y drogas / cash and drugs", 
                    "armas y dinero / weapons and money",
                    "objetos de valor / valuable items"
                ])
                
                self.player.add_money(loot_value)
                self.player.add_respect(house['risk'])
                self.player.add_experience(house['risk'] * 12)
                
                # Chance to find drugs
                if random.randint(1, 100) <= 30:
                    drug = random.choice(list(DRUGS.keys()))
                    amount = random.randint(1, 3)
                    self.player.drugs[drug] += amount
                    print(f"{Fore.MAGENTA}También encontraste {amount} unidades de {DRUGS[drug]['spanish']}!{Style.RESET_ALL}")
                
                success_messages = [
                    f"'¡Asalto perfecto! Encontramos {items_found} por ${loot_value:,}!'",
                    f"'¡Casa llena de tesoros! ${loot_value:,} en botín!'",
                    f"'¡Fácil trabajo! ${loot_value:,} sin problemas!'"
                ]
                
                print(f"{Fore.GREEN}{random.choice(success_messages)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Home invasion successful! Loot: ${loot_value:,}{Style.RESET_ALL}")
            else:
                damage = random.randint(15, 40)
                self.player.take_damage(damage)
                self.player.increase_wanted_level(house['risk'])
                
                failure_messages = [
                    "'¡Los dueños llegaron temprano! ¡Corremos!'",
                    "'¡Alarma activada! ¡Policía en camino!'",
                    "'¡Vecinos curiosos! ¡Mejor nos vamos!'"
                ]
                
                print(f"{Fore.RED}{random.choice(failure_messages)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Home invasion failed! Lost {damage} health and gained heat.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    # Missing business functions
    def view_available_businesses(self):
        """Show available businesses for purchase"""
        print(f"\n{Fore.CYAN}Negocios Disponibles / Available Businesses:{Style.RESET_ALL}")
        for biz_id, business in BUSINESSES.items():
            print(f"• {business['name']} - ${business['cost']:,}")
            print(f"  Ingresos diarios: ${business['daily_income']:,}")
            print(f"  Descripción: {business['description']}")
            print()

    def upgrade_business(self):
        """Upgrade existing businesses"""
        if not self.player.businesses:
            print(f"{Fore.YELLOW}No tienes negocios para mejorar{Style.RESET_ALL}")
            return
        
        for i, business in enumerate(self.player.businesses, 1):
            print(f"{i}. {BUSINESSES[business['type']]['name']} - Nivel {business.get('level', 1)}")
        
        try:
            choice = int(input("Selecciona negocio para mejorar: "))
            if 1 <= choice <= len(self.player.businesses):
                business = self.player.businesses[choice - 1]
                upgrade_cost = 10000 * business.get('level', 1)
                if self.player.money >= upgrade_cost:
                    self.player.remove_money(upgrade_cost)
                    business['level'] = business.get('level', 1) + 1
                    business['daily_income'] = int(business['daily_income'] * 1.5)
                    print(f"{Fore.GREEN}Negocio mejorado!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Dinero insuficiente{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def sell_business(self):
        """Sell existing businesses"""
        if not self.player.businesses:
            print(f"{Fore.YELLOW}No tienes negocios para vender{Style.RESET_ALL}")
            return
        
        for i, business in enumerate(self.player.businesses, 1):
            print(f"{i}. {BUSINESSES[business['type']]['name']}")
        
        try:
            choice = int(input("Selecciona negocio para vender: "))
            if 1 <= choice <= len(self.player.businesses):
                business = self.player.businesses.pop(choice - 1)
                sell_price = BUSINESSES[business['type']]['cost'] // 2
                self.player.add_money(sell_price)
                print(f"{Fore.GREEN}Negocio vendido por ${sell_price:,}!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def collect_business_earnings(self):
        """Collect daily earnings from businesses"""
        if not self.player.businesses:
            print(f"{Fore.YELLOW}No tienes negocios{Style.RESET_ALL}")
            return
        
        total_earnings = 0
        for business in self.player.businesses:
            earnings = business['daily_income']
            total_earnings += earnings
        
        self.player.add_money(total_earnings)
        print(f"{Fore.GREEN}Cobraste ${total_earnings:,} de tus negocios!{Style.RESET_ALL}")

    # Missing territory functions
    def take_territory(self, available_territories):
        """Take control of available territories"""
        if not available_territories:
            print(f"{Fore.YELLOW}No hay territorios disponibles{Style.RESET_ALL}")
            return
        
        for i, (territory_id, territory) in enumerate(available_territories, 1):
            name = territory["spanish"] if self.player.language_mode == "spanish" else territory["name"]
            print(f"{i}. {name} - Cost: ${territory['control_cost']:,}")
        
        try:
            choice = int(input("Selecciona territorio (0 para cancelar): "))
            if choice == 0:
                return
            if 1 <= choice <= len(available_territories):
                territory_id, territory = available_territories[choice - 1]
                if self.player.money >= territory["control_cost"]:
                    self.player.remove_money(territory["control_cost"])
                    self.player.territory.append(territory_id)
                    print(f"{Fore.GREEN}¡Territorio adquirido!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Dinero insuficiente{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def territory_war(self):
        """Initiate territory wars"""
        print(f"{Fore.RED}Guerra Territorial iniciada{Style.RESET_ALL}")
        if len(self.player.gang_members) < 3:
            print(f"{Fore.YELLOW}Necesitas al menos 3 miembros para guerra territorial{Style.RESET_ALL}")
            return
        
        war_cost = 15000
        if self.player.money >= war_cost:
            self.player.remove_money(war_cost)
            if random.randint(1, 100) <= 60:
                new_territory = f"Zona de Guerra {len(self.player.territory) + 1}"
                self.player.territory.append(new_territory)
                self.player.add_respect(25)
                print(f"{Fore.GREEN}¡Victoria! Conquistaste {new_territory}!{Style.RESET_ALL}")
            else:
                casualties = random.randint(1, 2)
                for _ in range(casualties):
                    if self.player.gang_members:
                        lost = self.player.gang_members.pop()
                        print(f"Perdiste a {lost['name']} en la guerra")
                print(f"{Fore.RED}Guerra perdida{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Necesitas ${war_cost:,} para iniciar guerra{Style.RESET_ALL}")

    def defend_territories(self):
        """Defend owned territories"""
        if not self.player.territory:
            print(f"{Fore.YELLOW}No tienes territorios que defender{Style.RESET_ALL}")
            return
        
        print(f"{Fore.BLUE}Defendiendo territorios...{Style.RESET_ALL}")
        for territory in self.player.territory[:]:  # Copy list to avoid modification issues
            if random.randint(1, 100) <= 20:  # 20% chance of attack per territory
                print(f"{Fore.RED}¡{territory} está bajo ataque!{Style.RESET_ALL}")
                defense_cost = 3000
                if self.player.money >= defense_cost and len(self.player.gang_members) >= 2:
                    self.player.remove_money(defense_cost)
                    if random.randint(1, 100) <= 70:
                        print(f"{Fore.GREEN}Defensa exitosa de {territory}!{Style.RESET_ALL}")
                        self.player.add_respect(10)
                    else:
                        self.player.territory.remove(territory)
                        print(f"{Fore.RED}Perdiste {territory}!{Style.RESET_ALL}")
                else:
                    self.player.territory.remove(territory)
                    print(f"{Fore.RED}No pudiste defender {territory}!{Style.RESET_ALL}")

    # Missing gang management functions
    def promote_gang_member(self):
        """Promote gang members"""
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros para promover{Style.RESET_ALL}")
            return
        
        for i, member in enumerate(self.player.gang_members, 1):
            current_rank = member.get('rank', 'Soldado')
            print(f"{i}. {member['name']} - {current_rank}")
        
        try:
            choice = int(input("Selecciona miembro para promover: "))
            if 1 <= choice <= len(self.player.gang_members):
                member = self.player.gang_members[choice - 1]
                ranks = ['Soldado', 'Teniente', 'Capitán', 'Subjefe']
                current_rank = member.get('rank', 'Soldado')
                if current_rank in ranks and ranks.index(current_rank) < len(ranks) - 1:
                    new_rank_index = ranks.index(current_rank) + 1
                    member['rank'] = ranks[new_rank_index]
                    member['loyalty'] = min(100, member['loyalty'] + 15)
                    print(f"{Fore.GREEN}{member['name']} promovido a {member['rank']}!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}{member['name']} ya tiene el rango máximo{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def assign_gang_mission(self):
        """Assign missions to gang members"""
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros disponibles{Style.RESET_ALL}")
            return
        
        missions = [
            {"name": "Recolección de Deudas", "cost": 2000, "reward": 5000, "risk": 30},
            {"name": "Vigilancia de Territorio", "cost": 1000, "reward": 3000, "risk": 20},
            {"name": "Contrabando", "cost": 5000, "reward": 12000, "risk": 50}
        ]
        
        print("Misiones disponibles:")
        for i, mission in enumerate(missions, 1):
            print(f"{i}. {mission['name']} - Costo: ${mission['cost']:,} - Recompensa: ${mission['reward']:,}")
        
        try:
            choice = int(input("Selecciona misión: "))
            if 1 <= choice <= len(missions):
                mission = missions[choice - 1]
                if self.player.money >= mission['cost']:
                    self.player.remove_money(mission['cost'])
                    if random.randint(1, 100) > mission['risk']:
                        self.player.add_money(mission['reward'])
                        self.player.add_respect(5)
                        print(f"{Fore.GREEN}¡Misión exitosa! Ganaste ${mission['reward']:,}!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Misión fallida{Style.RESET_ALL}")
                        if self.player.gang_members and random.randint(1, 100) <= 25:
                            injured = random.choice(self.player.gang_members)
                            injured['loyalty'] = max(0, injured['loyalty'] - 20)
                            print(f"{injured['name']} resultó herido, lealtad reducida")
                else:
                    print(f"{Fore.RED}Dinero insuficiente{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def kick_gang_member(self):
        """Remove gang members"""
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros que expulsar{Style.RESET_ALL}")
            return
        
        for i, member in enumerate(self.player.gang_members, 1):
            print(f"{i}. {member['name']} - Lealtad: {member['loyalty']}%")
        
        try:
            choice = int(input("Selecciona miembro para expulsar: "))
            if 1 <= choice <= len(self.player.gang_members):
                removed = self.player.gang_members.pop(choice - 1)
                print(f"{Fore.RED}{removed['name']} expulsado de la pandilla{Style.RESET_ALL}")
                
                # Low loyalty members might seek revenge
                if removed['loyalty'] < 50 and random.randint(1, 100) <= 30:
                    print(f"{Fore.RED}¡{removed['name']} busca venganza!{Style.RESET_ALL}")
                    damage = random.randint(15, 35)
                    self.player.take_damage(damage)
                    print(f"Sufriste {damage} de daño")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")

    def train_gang_member(self):
        """Train gang members to improve skills"""
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros para entrenar{Style.RESET_ALL}")
            return
        
        training_cost = 3000
        if self.player.money < training_cost:
            print(f"{Fore.RED}Necesitas ${training_cost:,} para entrenamiento{Style.RESET_ALL}")
            return
        
        for i, member in enumerate(self.player.gang_members, 1):
            print(f"{i}. {member['name']} - Especialidad: {member['specialty']}")
        
        try:
            choice = int(input("Selecciona miembro para entrenar: "))
            if 1 <= choice <= len(self.player.gang_members):
                member = self.player.gang_members[choice - 1]
                self.player.remove_money(training_cost)
                member['loyalty'] = min(100, member['loyalty'] + 10)
                
                # Improve specialty skill
                skill_improvements = {
                    "Tirador": "shooting",
                    "Conductor": "driving", 
                    "Hacker": "hacking",
                    "Músculo": "strength",
                    "Espía": "stealth"
                }
                
                skill = skill_improvements.get(member['specialty'], "shooting")
                if skill in self.player.skills:
                    self.player.skills[skill] = min(10, self.player.skills[skill] + 1)
                    print(f"{Fore.GREEN}{member['name']} entrenado! Tu habilidad {skill} mejoró!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}{member['name']} entrenado! Lealtad aumentada!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
    
    def street_police_combat(self):
        """Street police combat functionality"""
        print(f"\n{Fore.RED}¡COMBATE POLICIAL CALLEJERO! / STREET POLICE COMBAT!{Style.RESET_ALL}")
        
        # Calculate player combat effectiveness
        player_firepower = 0
        for weapon in self.player.inventory:
            if weapon in WEAPONS:
                player_firepower += WEAPONS[weapon]["damage"]
        
        # Define police force based on wanted level
        police_forces = {
            1: {"name": "Patrulla Local", "officers": 2, "armor": 20},
            2: {"name": "Policía de Ciudad", "officers": 3, "armor": 40},
            3: {"name": "SWAT Ligero", "officers": 4, "armor": 60},
            4: {"name": "SWAT Pesado", "officers": 6, "armor": 80},
            5: {"name": "Federales", "officers": 8, "armor": 100}
        }
        
        force = police_forces.get(self.player.wanted_level, police_forces[1])
        
        print(f"Enfrentando: {force['name']}")
        print(f"Oficiales: {force['officers']}")
        print(f"Armadura: {force['armor']}")
        
        if input("\n¿Iniciar combate? / Start combat? (s/y or n): ").lower() in ['s', 'y']:
            player_effectiveness = player_firepower + (self.player.skills["shooting"] * 10)
            police_effectiveness = force["armor"] + (force["officers"] * 15)
            
            # Combat resolution
            if player_effectiveness > police_effectiveness:
                # Player wins
                money_found = random.randint(500, 2000)
                respect_gain = self.player.wanted_level * 5
                
                self.player.add_money(money_found)
                self.player.add_respect(respect_gain)
                self.player.add_experience(self.player.wanted_level * 20)
                self.player.wanted_level = min(5, self.player.wanted_level + 1)  # Heat increases
                
                victory_messages = [
                    f"'¡Les dimos una lección! ${money_found} de sus bolsillos!'",
                    f"'¡Victoria en las calles! ${money_found} de botín policial!'",
                    f"'¡Mostramos quién manda aquí! ${money_found} ganados!'"
                ]
                
                print(f"{Fore.GREEN}{random.choice(victory_messages)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Police fight won! +${money_found}, +{respect_gain} respect{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Tu nivel de búsqueda aumentó / Your wanted level increased!{Style.RESET_ALL}")
                
                if self.player.add_experience(self.player.wanted_level * 20):
                    print(f"{Fore.CYAN}¡Has subido de nivel! / You leveled up!{Style.RESET_ALL}")
            else:
                # Player loses
                damage = random.randint(30, 70)
                money_lost = min(self.player.money // 3, 5000)
                
                self.player.take_damage(damage)
                self.player.remove_money(money_lost)
                
                defeat_messages = [
                    "'¡Nos superaron! ¡Retirada urgente!'",
                    "'¡Demasiados policías! ¡Escapemos!'",
                    "'¡Esta vez ganaron ellos! ¡Volveremos!'"
                ]
                
                print(f"{Fore.RED}{random.choice(defeat_messages)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Police fight lost! -{damage} health, -${money_lost:,}{Style.RESET_ALL}")
                
                # Check if player died
                if self.player.health <= 0:
                    print(f"{Fore.RED}¡Has caído en el tiroteo! / You fell in the shootout!{Style.RESET_ALL}")
                    input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
                    return
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def get_text(self, spanish_text: str, english_text: str) -> str:
        """Get text based on current language setting"""
        if self.language == "spanish":
            return spanish_text
        elif self.language == "english":
            return english_text
        else:  # bilingual
            return f"{spanish_text} / {english_text}"

    def change_language(self):
        """Change game language settings"""
        self.display_header()
        print(f"{Fore.MAGENTA}Configuración de Idioma / Language Settings{Style.RESET_ALL}")
        print()
        
        current_lang = {
            "spanish": "Español solamente",
            "english": "English only", 
            "bilingual": "Bilingüe / Bilingual"
        }
        
        print(f"Idioma actual / Current language: {Fore.GREEN}{current_lang[self.language]}{Style.RESET_ALL}")
        print()
        print("Opciones / Options:")
        print(f"1. {Fore.YELLOW}Español solamente{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}English only{Style.RESET_ALL}")
        print(f"3. {Fore.GREEN}Bilingüe / Bilingual{Style.RESET_ALL}")
        print(f"4. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Seleccionar / Select (1-4): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.language = "spanish"
            print(f"{Fore.GREEN}Idioma cambiado a español solamente.{Style.RESET_ALL}")
        elif choice == "2":
            self.language = "english"
            print(f"{Fore.GREEN}Language changed to English only.{Style.RESET_ALL}")
        elif choice == "3":
            self.language = "bilingual"
            print(f"{Fore.GREEN}Idioma cambiado a bilingüe / Language changed to bilingual.{Style.RESET_ALL}")
        elif choice == "4":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar / Press Enter to continue...{Style.RESET_ALL}")

    def run(self):
        """Main game loop"""
        try:
            # Check if save file exists
            if os.path.exists(SAVE_FILE):
                print(f"{Fore.YELLOW}Save file detected.{Style.RESET_ALL}")
                if input("Load existing game? (y/n): ").lower() == 'y':
                    self.load_game()
                else:
                    self.character_creation()
            else:
                self.character_creation()
            
            # Main game loop
            while self.running:
                # Check if player died
                if self.player.health <= 0:
                    print(f"\n{Fore.RED}{'='*50}{Style.RESET_ALL}")
                    print(f"{Fore.RED}    GAME OVER - YOU DIED    {Style.RESET_ALL}")
                    print(f"{Fore.RED}{'='*50}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}Your criminal career has come to an end...{Style.RESET_ALL}")
                    print("\nFinal Stats:")
                    print(f"Money: ${self.player.money:,}")
                    print(f"Respect: {self.player.respect}")
                    print(f"Missions completed: {self.player.stats['missions_completed']}")
                    
                    if input("\nStart new game? (y/n): ").lower() == 'y':
                        if os.path.exists(SAVE_FILE):
                            os.remove(SAVE_FILE)
                        self.player = Player()
                        self.character_creation()
                        continue
                    else:
                        break
                
                # Reduce wanted level over time
                if self.player.wanted_level > 0 and random.randint(1, 100) <= 5:
                    self.player.decrease_wanted_level(1)
                
                self.main_menu()
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Game interrupted. Thanks for playing!{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            print("Game data has been preserved.")

    def buy_business(self):
        """Purchase a new business for money laundering and income"""
        print(f"\n{Fore.GREEN}Comprar Negocio / Buy Business{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.CYAN}Negocios Disponibles / Available Businesses:{Style.RESET_ALL}")
        available = []
        for biz_type, info in BUSINESSES.items():
            owned = any(b["type"] == biz_type for b in self.player.businesses)
            if not owned:
                available.append((biz_type, info))
        
        if not available:
            print(f"{Fore.YELLOW}Ya posees todos los tipos de negocios / You already own all business types{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        for i, (biz_type, info) in enumerate(available, 1):
            text = info["spanish"] if self.player.language_mode == "spanish" else info["name"]
            print(f"{i}. {text}")
            print(f"   Costo: ${info['cost']:,}")
            print(f"   Ingresos diarios: ${info['daily_income']:,}")
            print(f"   Generación de calor: {info['heat_generation']}")
            print()
        
        try:
            choice = int(input(f"{Fore.CYAN}Selecciona negocio (0 para cancelar): {Style.RESET_ALL}"))
            if choice == 0:
                return
            if 1 <= choice <= len(available):
                biz_type, info = available[choice - 1]
                
                if self.player.money >= info["cost"]:
                    self.player.remove_money(info["cost"])
                    
                    new_business = {
                        "type": biz_type,
                        "daily_income": info["daily_income"],
                        "upgrade_level": 1,
                        "location": self.player.location,
                        "days_owned": 0
                    }
                    
                    self.player.businesses.append(new_business)
                    self.player.heat_level += info["heat_generation"]
                    
                    text = info["spanish"] if self.player.language_mode == "spanish" else info["name"]
                    print(f"{Fore.GREEN}¡Compraste {text}! / Purchased {text}!{Style.RESET_ALL}")
                    print(f"Genera ${info['daily_income']:,} por día")
                else:
                    print(f"{Fore.RED}Dinero insuficiente / Insufficient funds{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def advanced_heist(self):
        """Plan and execute complex heists with crew"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}Atraco Avanzado / Advanced Heist{Style.RESET_ALL}")
        print()
        
        if len(self.player.gang_members) < 2:
            print(f"{Fore.RED}Necesitas al menos 2 miembros para atracos complejos{Style.RESET_ALL}")
            print(f"{Fore.RED}Need at least 2 gang members for complex heists{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Atracos Disponibles / Available Heists:{Style.RESET_ALL}")
        
        available_heists = []
        for heist_id, heist in CRIMINAL_ACTIVITIES.items():
            if len(self.player.gang_members) >= heist["required_members"]:
                # Check skill requirements
                can_do = True
                for skill, min_level in heist["required_skills"].items():
                    if self.player.skills.get(skill, 0) < min_level:
                        can_do = False
                        break
                
                if can_do:
                    available_heists.append((heist_id, heist))
        
        if not available_heists:
            print(f"{Fore.YELLOW}No cumples los requisitos para ningún atraco{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}You don't meet requirements for any heists{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        for i, (heist_id, heist) in enumerate(available_heists, 1):
            text = heist["spanish"] if self.player.language_mode == "spanish" else heist["name"]
            print(f"{i}. {text}")
            print(f"   Recompensa: ${heist['min_reward']:,} - ${heist['max_reward']:,}")
            print(f"   Riesgo: {'★' * heist['risk']}")
            print(f"   Duración: {heist['time_hours']} horas")
            print(f"   Miembros requeridos: {heist['required_members']}")
            print()
        
        try:
            choice = int(input(f"{Fore.CYAN}Selecciona atraco (0 para cancelar): {Style.RESET_ALL}"))
            if choice == 0:
                return
            if 1 <= choice <= len(available_heists):
                heist_id, heist = available_heists[choice - 1]
                self.execute_heist(heist_id, heist)
        except ValueError:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")

    def execute_heist(self, heist_id, heist):
        """Execute a complex heist operation"""
        print(f"\n{Fore.YELLOW}Preparando {heist['spanish']}...{Style.RESET_ALL}")
        print(f"Preparing {heist['name']}...")
        
        # Calculate success chance
        base_chance = 50
        skill_bonus = 0
        for skill, min_level in heist["required_skills"].items():
            skill_bonus += (self.player.skills.get(skill, 0) - min_level) * 5
        
        member_bonus = len(self.player.gang_members) * 3
        respect_bonus = min(self.player.respect // 100, 20)
        
        success_chance = min(95, base_chance + skill_bonus + member_bonus + respect_bonus)
        
        print(f"\nProbabilidad de éxito: {success_chance}%")
        print(f"Success probability: {success_chance}%")
        
        if input("\n¿Proceder con el atraco? / Proceed with heist? (s/y or n): ").lower() not in ['s', 'y']:
            return
        
        # Simulate heist execution
        print(f"\n{Fore.YELLOW}Ejecutando atraco...{Style.RESET_ALL}")
        time.sleep(2)
        
        if random.randint(1, 100) <= success_chance:
            # Successful heist
            reward = random.randint(heist["min_reward"], heist["max_reward"])
            
            # Bonus for high-skilled crew
            if skill_bonus > 20:
                reward = int(reward * 1.2)
            
            self.player.add_money(reward)
            self.player.add_respect(heist["risk"] * 10)
            self.player.add_experience(heist["risk"] * 20)
            self.player.heat_level += heist["heat_increase"]
            self.player.stats["heists_completed"] += 1
            
            print(f"{Fore.GREEN}¡Atraco exitoso! / Heist successful!{Style.RESET_ALL}")
            print(f"Ganaste ${reward:,}")
            print(f"Gained ${reward:,}")
            print(f"+{heist['risk'] * 10} respeto")
            print(f"+{heist['risk'] * 10} respect")
            
            # Crew gets experience
            for member in self.player.gang_members:
                member["missions_completed"] += 1
                member["loyalty"] = min(100, member["loyalty"] + 5)
        
        else:
            # Failed heist
            print(f"{Fore.RED}¡Atraco fallido! / Heist failed!{Style.RESET_ALL}")
            
            # Consequences
            if random.randint(1, 100) <= 30:
                # Gang member caught
                if self.player.gang_members:
                    caught_member = random.choice(self.player.gang_members)
                    self.player.gang_members.remove(caught_member)
                    print(f"{Fore.RED}{caught_member['name']} fue capturado por la policía{Style.RESET_ALL}")
                    print(f"{caught_member['name']} was caught by police")
            
            # Increased heat and wanted level
            self.player.heat_level += heist["heat_increase"] * 2
            self.player.increase_wanted_level(2)
            
            # Possible injury
            if random.randint(1, 100) <= 40:
                damage = random.randint(20, 40)
                self.player.take_damage(damage)
                print(f"{Fore.RED}Resultaste herido en el escape / You were injured in the escape{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def cybercrime_operations(self):
        """Advanced cybercrime and hacking operations"""
        self.display_header()
        print(f"{Fore.LIGHTBLUE_EX}Operaciones Cibercriminales / Cybercrime Operations{Style.RESET_ALL}")
        print()
        
        if self.player.skills.get("hacking", 0) < 2:
            print(f"{Fore.RED}Necesitas habilidad de hacking nivel 2+ / Need hacking skill level 2+{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        cyber_activities = {
            "atm_hack": {
                "name": "ATM Hacking / Hackeo de ATM",
                "spanish": "Hackeo de ATM",
                "reward": (500, 2000),
                "risk": 2,
                "required_hacking": 2,
                "time": 1
            },
            "credit_fraud": {
                "name": "Credit Card Fraud / Fraude de Tarjetas",
                "spanish": "Fraude de Tarjetas",
                "reward": (2000, 8000),
                "risk": 3,
                "required_hacking": 3,
                "time": 2
            },
            "bank_transfer": {
                "name": "Bank Transfer Hack / Hackeo de Transferencias",
                "spanish": "Hackeo de Transferencias",
                "reward": (10000, 50000),
                "risk": 4,
                "required_hacking": 4,
                "time": 4
            },
            "crypto_theft": {
                "name": "Cryptocurrency Theft / Robo de Criptomonedas",
                "spanish": "Robo de Criptomonedas",
                "reward": (5000, 100000),
                "risk": 5,
                "required_hacking": 5,
                "time": 6
            }
        }
        
        print(f"{Fore.CYAN}Operaciones Disponibles / Available Operations:{Style.RESET_ALL}")
        available = []
        for activity_id, activity in cyber_activities.items():
            if self.player.skills.get("hacking", 0) >= activity["required_hacking"]:
                available.append((activity_id, activity))
        
        for i, (activity_id, activity) in enumerate(available, 1):
            text = activity["spanish"] if self.player.language_mode == "spanish" else activity["name"]
            print(f"{i}. {text}")
            print(f"   Recompensa: ${activity['reward'][0]:,} - ${activity['reward'][1]:,}")
            print(f"   Riesgo: {'★' * activity['risk']}")
            print(f"   Tiempo: {activity['time']} hora(s)")
            print()
        
        try:
            choice = int(input(f"{Fore.CYAN}Selecciona operación (0 para cancelar): {Style.RESET_ALL}"))
            if choice == 0:
                return
            if 1 <= choice <= len(available):
                activity_id, activity = available[choice - 1]
                self.execute_cybercrime(activity_id, activity)
        except ValueError:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")

    def execute_cybercrime(self, activity_id, activity):
        """Execute cybercrime operation"""
        print(f"\n{Fore.YELLOW}Iniciando operación cibercriminal...{Style.RESET_ALL}")
        print("Starting cybercrime operation...")
        
        # Calculate success chance based on hacking skill
        hacking_skill = self.player.skills.get("hacking", 0)
        base_chance = 40 + (hacking_skill * 10)
        success_chance = min(90, base_chance)
        
        print(f"Probabilidad de éxito: {success_chance}%")
        
        if input("\n¿Proceder? / Proceed? (s/y or n): ").lower() not in ['s', 'y']:
            return
        
        print(f"\n{Fore.CYAN}Ejecutando...{Style.RESET_ALL}")
        time.sleep(activity["time"])
        
        if random.randint(1, 100) <= success_chance:
            reward = random.randint(activity["reward"][0], activity["reward"][1])
            
            # Skill bonus
            if hacking_skill >= 5:
                reward = int(reward * 1.3)
            
            self.player.add_money(reward)
            self.player.add_experience(activity["risk"] * 15)
            self.player.heat_level += activity["risk"]
            
            print(f"{Fore.GREEN}¡Operación exitosa! / Operation successful!{Style.RESET_ALL}")
            print(f"Ganaste ${reward:,}")
        else:
            print(f"{Fore.RED}¡Operación fallida! / Operation failed!{Style.RESET_ALL}")
            
            # Consequences
            if random.randint(1, 100) <= 25:
                self.player.increase_wanted_level(1)
                print(f"{Fore.RED}Las autoridades detectaron actividad sospechosa{Style.RESET_ALL}")
            
            self.player.heat_level += activity["risk"] * 2
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def business_management(self):
        """Manage criminal business empire"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}Gestión de Negocios / Business Management{Style.RESET_ALL}")
        print()
        
        if not self.player.businesses:
            print(f"{Fore.YELLOW}No posees negocios / You don't own any businesses yet{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Tus Negocios / Your Businesses:{Style.RESET_ALL}")
            daily_total = 0
            for i, business in enumerate(self.player.businesses, 1):
                biz_info = BUSINESSES[business["type"]]
                income = business["daily_income"]
                daily_total += income
                print(f"{i}. {biz_info['name']} - ${income:,}/día")
            print(f"\n{Fore.GREEN}Ingresos diarios totales: ${daily_total:,}{Style.RESET_ALL}")
        
        print(f"\n1. {Fore.GREEN}Comprar negocio / Buy business{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Ver negocios disponibles / View available businesses{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Mejorar negocio / Upgrade business{Style.RESET_ALL}")
        print(f"4. {Fore.RED}Vender negocio / Sell business{Style.RESET_ALL}")
        print(f"5. {Fore.MAGENTA}Cobrar ganancias / Collect earnings{Style.RESET_ALL}")
        print(f"6. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.buy_business()
        elif choice == "2":
            self.view_available_businesses()
        elif choice == "3":
            self.upgrade_business()
        elif choice == "4":
            self.sell_business()
        elif choice == "5":
            self.collect_business_earnings()
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def territory_control(self):
        """Manage and expand territorial control"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}Control Territorial / Territory Control{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.CYAN}Territorios Controlados / Controlled Territories:{Style.RESET_ALL}")
        if not self.player.territory:
            print(f"{Fore.YELLOW}No controlas territorios / You don't control any territories{Style.RESET_ALL}")
        else:
            daily_income = 0
            for territory in self.player.territory:
                territory_info = TERRITORIES[territory]
                income = territory_info["income_per_day"]
                daily_income += income
                text = territory_info["spanish"] if self.player.language_mode == "spanish" else territory_info["name"]
                print(f"• {text} - ${income:,}/día")
            print(f"\n{Fore.GREEN}Ingresos territoriales diarios: ${daily_income:,}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Territorios Disponibles / Available Territories:{Style.RESET_ALL}")
        available_territories = []
        for territory_id, territory in TERRITORIES.items():
            if territory_id not in self.player.territory:
                available_territories.append((territory_id, territory))
        
        if not available_territories:
            print(f"{Fore.YELLOW}Controlas todos los territorios / You control all territories{Style.RESET_ALL}")
        else:
            for i, (territory_id, territory) in enumerate(available_territories, 1):
                text = territory["spanish"] if self.player.language_mode == "spanish" else territory["name"]
                print(f"{i}. {text}")
                print(f"   Ciudad: {territory['city']}")
                print(f"   Ingresos diarios: ${territory['income_per_day']:,}")
                print(f"   Costo de control: ${territory['control_cost']:,}")
                print(f"   Controlado por: {territory['current_controller']}")
                print()
        
        print(f"1. {Fore.GREEN}Tomar territorio / Take territory{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Guerra territorial / Territory war{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Defender territorios / Defend territories{Style.RESET_ALL}")
        print(f"4. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.take_territory(available_territories)
        elif choice == "2":
            self.territory_war()
        elif choice == "3":
            self.defend_territories()
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def police_encounter(self):
        """Handle police encounters with 3+ wanted level"""
        if self.player.wanted_level >= 3:
            encounter_chance = min(80, self.player.wanted_level * 15)
            if random.randint(1, 100) <= encounter_chance:
                print(f"\n{Fore.RED}🚔 ¡ENCUENTRO POLICIAL! / POLICE ENCOUNTER!{Style.RESET_ALL}")
                print("Los policías te han reconocido en la calle")
                print("Police have recognized you on the street")
                
                print(f"\n1. {Fore.GREEN}Huir / Run away{Style.RESET_ALL}")
                print(f"2. {Fore.RED}Luchar / Fight{Style.RESET_ALL}")
                print(f"3. {Fore.YELLOW}Intentar sobornar / Try to bribe{Style.RESET_ALL}")
                print(f"4. {Fore.BLUE}Rendirse / Surrender{Style.RESET_ALL}")
                
                choice = input(f"\n{Fore.CYAN}¿Qué haces? / What do you do?: {Style.RESET_ALL}").strip()
                
                if choice == "1":
                    self.flee_from_police()
                elif choice == "2":
                    self.fight_police()
                elif choice == "3":
                    self.bribe_police()
                elif choice == "4":
                    self.surrender_to_police()
                else:
                    print(f"{Fore.RED}Te quedas paralizado y los policías te arrestan{Style.RESET_ALL}")
                    self.arrest_player()

    def flee_from_police(self):
        """Attempt to flee from police"""
        driving_skill = self.player.skills.get("driving", 0)
        stealth_skill = self.player.skills.get("stealth", 0)
        
        if self.player.vehicle and self.player.vehicle in VEHICLES:
            vehicle_info = VEHICLES[self.player.vehicle]
            flee_chance = 40 + (driving_skill * 8) + (vehicle_info["speed"] * 5)
        else:
            flee_chance = 30 + (stealth_skill * 10)
        
        flee_chance = min(85, flee_chance)
        
        if random.randint(1, 100) <= flee_chance:
            print(f"{Fore.GREEN}¡Escapaste exitosamente! / Successfully escaped!{Style.RESET_ALL}")
            if self.player.vehicle:
                print("Tu vehículo te ayudó a escapar")
            else:
                print("Lograste perderte entre las calles")
            
            # Slight wanted level increase for fleeing
            self.player.increase_wanted_level(1)
        else:
            print(f"{Fore.RED}¡No pudiste escapar! / Couldn't escape!{Style.RESET_ALL}")
            print("Los policías te alcanzaron")
            self.arrest_player()

    def fight_police(self):
        """Fight the police"""
        print(f"\n{Fore.RED}¡COMBATE POLICIAL! / POLICE COMBAT!{Style.RESET_ALL}")
        
        # Player combat strength
        shooting_skill = self.player.skills.get("shooting", 0)
        strength_skill = self.player.skills.get("strength", 0)
        weapon_bonus = 0
        
        # Check for weapons
        for weapon in self.player.inventory:
            if weapon in WEAPONS:
                weapon_bonus += WEAPONS[weapon]["damage"]
        
        player_strength = shooting_skill * 10 + strength_skill * 5 + weapon_bonus
        
        # Police strength based on wanted level
        police_strength = self.player.wanted_level * 25 + random.randint(50, 100)
        
        print(f"Tu fuerza de combate: {player_strength}")
        print(f"Fuerza policial: {police_strength}")
        
        if player_strength > police_strength:
            # Victory
            print(f"\n{Fore.GREEN}¡Derrotaste a los policías! / Defeated the police!{Style.RESET_ALL}")
            money_found = random.randint(500, 2000)
            self.player.add_money(money_found)
            self.player.add_respect(15)
            self.player.add_experience(25)
            
            print(f"Encontraste ${money_found:,} en efectivo")
            print("Ganaste respeto en las calles")
            
            # Major wanted level increase
            self.player.increase_wanted_level(2)
            self.player.heat_level += 20
            
        else:
            # Defeat
            print(f"\n{Fore.RED}¡Los policías te derrotaron! / Police defeated you!{Style.RESET_ALL}")
            damage = random.randint(30, 60)
            self.player.take_damage(damage)
            
            if self.player.health <= 0:
                print("Moriste en el enfrentamiento")
                return
            
            print(f"Sufriste {damage} de daño")
            self.arrest_player()

    def bribe_police(self):
        """Attempt to bribe police officers"""
        bribe_amount = self.player.wanted_level * 1000
        
        print(f"Los policías quieren ${bribe_amount:,} para dejarte ir")
        print(f"Police want ${bribe_amount:,} to let you go")
        
        if self.player.money >= bribe_amount:
            if input("\n¿Pagar soborno? / Pay bribe? (s/y or n): ").lower() in ['s', 'y']:
                self.player.remove_money(bribe_amount)
                self.player.decrease_wanted_level(1)
                
                print(f"{Fore.GREEN}¡Soborno exitoso! / Successful bribe!{Style.RESET_ALL}")
                print("Los policías te dejan ir")
                print("Tu nivel de búsqueda disminuyó")
            else:
                print("Te niegas a pagar y huyes")
                self.flee_from_police()
        else:
            print(f"{Fore.RED}No tienes suficiente dinero para el soborno{Style.RESET_ALL}")
            print("Los policías proceden con el arresto")
            self.arrest_player()

    def surrender_to_police(self):
        """Surrender to police voluntarily"""
        print(f"{Fore.YELLOW}Te rindes voluntariamente{Style.RESET_ALL}")
        print("Voluntary surrender")
        
        # Reduced prison time for voluntary surrender
        base_time = self.player.wanted_level * 2
        self.player.prison_time = max(1, base_time - 2)
        
        print(f"Tiempo en prisión reducido por entregarte: {self.player.prison_time} días")
        self.send_to_prison()

    def arrest_player(self):
        """Player gets arrested"""
        print(f"\n{Fore.RED}¡HAS SIDO ARRESTADO! / YOU'VE BEEN ARRESTED!{Style.RESET_ALL}")
        
        # Prison time based on wanted level
        self.player.prison_time = self.player.wanted_level * 3
        
        # Lose money (lawyer fees, fines)
        fine = min(self.player.money // 3, self.player.wanted_level * 2000)
        self.player.remove_money(fine)
        
        print(f"Multa pagada: ${fine:,}")
        print(f"Tiempo en prisión: {self.player.prison_time} días")
        
        self.send_to_prison()

    def send_to_prison(self):
        """Send player to prison"""
        print(f"\n{Fore.YELLOW}Enviado a la Penitenciaría de Nuevo México{Style.RESET_ALL}")
        print("Sent to New Mexico State Penitentiary")
        
        # Reset wanted level
        self.player.wanted_level = 0
        self.player.heat_level = max(0, self.player.heat_level - 30)
        
        # Prison activities while serving time
        if self.player.prison_time > 0:
            self.prison_activities()

    def prison_activities(self):
        """Activities available while in prison"""
        print(f"\n{Fore.CYAN}Actividades en Prisión / Prison Activities{Style.RESET_ALL}")
        print(f"Días restantes / Days remaining: {self.player.prison_time}")
        print()
        
        print(f"1. {Fore.GREEN}Entrenar fuerza / Train strength{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Hacer contactos / Make contacts{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Planear escape / Plan escape{Style.RESET_ALL}")
        print(f"4. {Fore.WHITE}Servir tiempo / Serve time{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué haces en prisión? / What do you do in prison?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Train strength
            if self.player.skills["strength"] < 10:
                self.player.skills["strength"] += 1
                print(f"{Fore.GREEN}Tu fuerza aumentó a {self.player.skills['strength']}{Style.RESET_ALL}")
            else:
                print("Tu fuerza ya está al máximo")
            
        elif choice == "2":
            # Make contacts for future gang recruitment
            if random.randint(1, 100) <= 60:
                contact_name = random.choice([
                    "Carlos 'El Veterano'", "Miguel 'Cicatrices'", "José 'El Silencioso'",
                    "Roberto 'Puños de Hierro'", "Diego 'El Susurro'"
                ])
                print(f"{Fore.GREEN}Hiciste contacto con {contact_name}{Style.RESET_ALL}")
                print("Podrás reclutarlo cuando salgas")
                
                # Add to contacts for later recruitment
                if "prison_contacts" not in self.player.__dict__:
                    self.player.prison_contacts = []
                self.player.prison_contacts.append(contact_name)
            else:
                print("No lograste hacer contactos útiles")
                
        elif choice == "3":
            # Plan escape
            self.prison_escape()
            return
            
        elif choice == "4":
            # Serve time quietly
            print("Sirves tu tiempo tranquilamente")
            print("You serve your time quietly")
        
        # Reduce prison time
        self.player.prison_time = max(0, self.player.prison_time - 1)
        
        if self.player.prison_time > 0:
            time.sleep(1)
            self.prison_activities()
        else:
            print(f"\n{Fore.GREEN}¡LIBERADO! / RELEASED!{Style.RESET_ALL}")
            print("Has cumplido tu sentencia")
            print("You've served your sentence")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def prison_escape(self):
        """Attempt to escape from prison"""
        print(f"\n{Fore.RED}Intento de Fuga / Escape Attempt{Style.RESET_ALL}")
        
        stealth_skill = self.player.skills.get("stealth", 0)
        charisma_skill = self.player.skills.get("charisma", 0)
        
        escape_chance = 25 + (stealth_skill * 8) + (charisma_skill * 5)
        escape_chance = min(75, escape_chance)
        
        print(f"Probabilidad de escape: {escape_chance}%")
        
        if input("¿Intentar escapar? / Attempt escape? (s/y or n): ").lower() in ['s', 'y']:
            if random.randint(1, 100) <= escape_chance:
                print(f"{Fore.GREEN}¡ESCAPE EXITOSO! / SUCCESSFUL ESCAPE!{Style.RESET_ALL}")
                print("Lograste escapar de la prisión")
                print("You managed to escape from prison")
                
                # Reset prison time but increase wanted level significantly
                self.player.prison_time = 0
                self.player.increase_wanted_level(3)
                self.player.heat_level += 40
                
                print("Tu nivel de búsqueda aumentó drasticamente")
                print("Your wanted level increased drastically")
                
            else:
                print(f"{Fore.RED}¡ESCAPE FALLIDO! / ESCAPE FAILED!{Style.RESET_ALL}")
                print("Te atraparon intentando escapar")
                
                # Double remaining prison time
                self.player.prison_time *= 2
                damage = random.randint(20, 40)
                self.player.take_damage(damage)
                
                print(f"Tu sentencia se duplicó: {self.player.prison_time} días")
                print(f"Sufriste {damage} de daño en el intento")
                
                if self.player.prison_time > 0:
                    time.sleep(2)
                    self.prison_activities()

    def gang_hierarchy_system(self):
        """Advanced gang hierarchy management"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}Jerarquía de Pandilla / Gang Hierarchy{Style.RESET_ALL}")
        print()
        
        if not self.player.gang_affiliation and not self.player.gang_name:
            print(f"{Fore.YELLOW}No tienes afiliación de pandilla / No gang affiliation{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        # Gang hierarchy levels
        hierarchy_levels = {
            0: {"name": "Novato / Rookie", "spanish": "Novato", "respect_needed": 0},
            1: {"name": "Soldado / Soldier", "spanish": "Soldado", "respect_needed": 50},
            2: {"name": "Teniente / Lieutenant", "spanish": "Teniente", "respect_needed": 150},
            3: {"name": "Capitán / Captain", "spanish": "Capitán", "respect_needed": 300},
            4: {"name": "Jefe / Boss", "spanish": "Jefe", "respect_needed": 500},
            5: {"name": "Don / Godfather", "spanish": "Don", "respect_needed": 1000}
        }
        
        # Determine current rank
        current_rank = 0
        for level, info in hierarchy_levels.items():
            if self.player.respect >= info["respect_needed"]:
                current_rank = level
        
        current_info = hierarchy_levels[current_rank]
        rank_name = current_info["spanish"] if self.player.language_mode == "spanish" else current_info["name"]
        
        print(f"Rango actual / Current rank: {Fore.YELLOW}{rank_name}{Style.RESET_ALL}")
        print(f"Respeto: {self.player.respect}")
        print()
        
        # Show next rank requirements
        if current_rank < 5:
            next_rank = hierarchy_levels[current_rank + 1]
            next_name = next_rank["spanish"] if self.player.language_mode == "spanish" else next_rank["name"]
            needed = next_rank["respect_needed"] - self.player.respect
            print(f"Próximo rango / Next rank: {next_name}")
            print(f"Respeto necesario / Respect needed: {needed}")
        else:
            print(f"{Fore.YELLOW}¡Has alcanzado el rango máximo! / You've reached maximum rank!{Style.RESET_ALL}")
        
        print()
        print(f"1. {Fore.GREEN}Ver beneficios de rango / View rank benefits{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Gestionar pandilla / Manage gang{Style.RESET_ALL}")
        print(f"3. {Fore.RED}Dejar pandilla / Leave gang{Style.RESET_ALL}")
        print(f"4. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.show_rank_benefits(hierarchy_levels, current_rank)
        elif choice == "2":
            self.advanced_gang_management()
        elif choice == "3":
            self.leave_gang()

    def show_rank_benefits(self, hierarchy_levels, current_rank):
        """Show benefits for each gang rank"""
        print(f"\n{Fore.CYAN}Beneficios por Rango / Rank Benefits:{Style.RESET_ALL}")
        print()
        
        benefits = {
            0: ["Acceso básico a misiones / Basic mission access"],
            1: ["10% descuento en armas / 10% weapon discount", "Acceso a robos menores / Access to minor heists"],
            2: ["Comando de hasta 3 miembros / Command up to 3 members", "Acceso a territorios / Territory access"],
            3: ["15% más ingresos de territorio / 15% more territory income", "Misiones de alto valor / High-value missions"],
            4: ["Crear tu propia pandilla / Create your own gang", "Comando de hasta 10 miembros / Command up to 10 members"],
            5: ["Respeto máximo en las calles / Maximum street respect", "Acceso a todos los contenidos / Access to all content"]
        }
        
        for level, info in hierarchy_levels.items():
            rank_name = info["spanish"] if self.player.language_mode == "spanish" else info["name"]
            status = f"{Fore.GREEN}ACTUAL{Style.RESET_ALL}" if level == current_rank else f"{Fore.YELLOW}DISPONIBLE{Style.RESET_ALL}" if level < current_rank else f"{Fore.RED}BLOQUEADO{Style.RESET_ALL}"
            
            print(f"{level}. {rank_name} - {status}")
            print(f"   Respeto requerido: {info['respect_needed']}")
            for benefit in benefits.get(level, []):
                print(f"   • {benefit}")
            print()
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def advanced_gang_management(self):
        """Advanced gang management with hierarchy"""
        print(f"\n{Fore.LIGHTRED_EX}Gestión Avanzada de Pandilla / Advanced Gang Management{Style.RESET_ALL}")
        
        if not self.player.gang_members:
            print(f"{Fore.YELLOW}No tienes miembros en tu pandilla / No gang members{Style.RESET_ALL}")
            print("Recluta miembros primero / Recruit members first")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Miembros de la Pandilla / Gang Members:{Style.RESET_ALL}")
        for i, member in enumerate(self.player.gang_members, 1):
            loyalty_color = Fore.GREEN if member["loyalty"] > 70 else Fore.YELLOW if member["loyalty"] > 40 else Fore.RED
            print(f"{i}. {member['name']}")
            print(f"   Especialidad: {member['specialty']}")
            print(f"   Lealtad: {loyalty_color}{member['loyalty']}%{Style.RESET_ALL}")
            print(f"   Rango: {member.get('rank', 'Soldado')}")
            print()
        
        print(f"1. {Fore.GREEN}Promover miembro / Promote member{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Asignar misión / Assign mission{Style.RESET_ALL}")
        print(f"3. {Fore.RED}Expulsar miembro / Kick member{Style.RESET_ALL}")
        print(f"4. {Fore.BLUE}Entrenar miembro / Train member{Style.RESET_ALL}")
        print(f"5. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.promote_gang_member()
        elif choice == "2":
            self.assign_gang_mission()
        elif choice == "3":
            self.kick_gang_member()
        elif choice == "4":
            self.train_gang_member()

    def leave_gang(self):
        """Leave current gang affiliation"""
        print(f"\n{Fore.RED}Dejar Pandilla / Leave Gang{Style.RESET_ALL}")
        
        if self.player.gang_name:
            print(f"Eres el líder de {self.player.gang_name}")
            print("Dejar tu propia pandilla la disolverá")
        else:
            print(f"Estás afiliado a {self.player.gang_affiliation}")
            print("Dejar la pandilla puede tener consecuencias")
        
        print(f"\n{Fore.YELLOW}Consecuencias de dejar la pandilla:{Style.RESET_ALL}")
        print("• Perderás todos los miembros")
        print("• Perderás todos los territorios")
        print("• Perderás respeto en las calles")
        print("• Posibles represalias de ex-miembros")
        
        if input("\n¿Estás seguro? / Are you sure? (s/y or n): ").lower() in ['s', 'y']:
            # Consequences of leaving
            self.player.gang_affiliation = None
            self.player.gang_name = None
            self.player.gang_members = []
            self.player.territory = []
            self.player.respect = max(0, self.player.respect - 100)
            self.player.gang_reputation = 0
            
            print(f"{Fore.RED}Has dejado la pandilla / You've left the gang{Style.RESET_ALL}")
            print("Perdiste 100 puntos de respeto")
            
            # Chance of revenge attack
            if random.randint(1, 100) <= 30:
                print(f"\n{Fore.RED}¡ATAQUE DE VENGANZA! / REVENGE ATTACK!{Style.RESET_ALL}")
                print("Ex-miembros de tu pandilla te atacan")
                damage = random.randint(20, 50)
                self.player.take_damage(damage)
                print(f"Sufriste {damage} de daño")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def multiple_save_system(self):
        """Enhanced save system with 3 slots"""
        self.display_header()
        print(f"{Fore.LIGHTBLUE_EX}Sistema de Guardado / Save System{Style.RESET_ALL}")
        print()
        
        print(f"1. {Fore.GREEN}Guardar en Slot 1 / Save to Slot 1{Style.RESET_ALL}")
        print(f"2. {Fore.GREEN}Guardar en Slot 2 / Save to Slot 2{Style.RESET_ALL}")
        print(f"3. {Fore.GREEN}Guardar en Slot 3 / Save to Slot 3{Style.RESET_ALL}")
        print(f"4. {Fore.BLUE}Cargar desde Slot 1 / Load from Slot 1{Style.RESET_ALL}")
        print(f"5. {Fore.BLUE}Cargar desde Slot 2 / Load from Slot 2{Style.RESET_ALL}")
        print(f"6. {Fore.BLUE}Cargar desde Slot 3 / Load from Slot 3{Style.RESET_ALL}")
        print(f"7. {Fore.YELLOW}Ver información de slots / View slot info{Style.RESET_ALL}")
        print(f"8. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elección / Choice: {Style.RESET_ALL}").strip()
        
        if choice in ["1", "2", "3"]:
            slot = int(choice)
            self.save_to_slot(slot)
        elif choice in ["4", "5", "6"]:
            slot = int(choice) - 3
            self.load_from_slot(slot)
        elif choice == "7":
            self.show_slot_info()

    def save_to_slot(self, slot):
        """Save game to specific slot"""
        try:
            save_data = {
                "player_name": self.player.name,
                "health": self.player.health,
                "money": self.player.money,
                "respect": self.player.respect,
                "wanted_level": self.player.wanted_level,
                "location": self.player.location,
                "inventory": self.player.inventory,
                "drugs": self.player.drugs,
                "ammo": self.player.ammo,
                "vehicle": self.player.vehicle,
                "gang_affiliation": self.player.gang_affiliation,
                "gang_name": self.player.gang_name,
                "gang_members": self.player.gang_members,
                "territory": self.player.territory,
                "businesses": self.player.businesses,
                "skills": self.player.skills,
                "level": self.player.level,
                "experience": self.player.experience,
                "stats": self.player.stats,
                "language_mode": self.player.language_mode,
                "heat_level": self.player.heat_level,
                "prison_time": self.player.prison_time,
                "save_timestamp": datetime.now().isoformat(),
                "game_version": "2.0"
            }
            
            filename = f"mexican_gangsters_slot_{slot}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}¡Juego guardado en Slot {slot}! / Game saved to Slot {slot}!{Style.RESET_ALL}")
            print(f"Archivo: {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}Error al guardar: {e}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def load_from_slot(self, slot):
        """Load game from specific slot"""
        filename = f"mexican_gangsters_slot_{slot}.json"
        
        if not os.path.exists(filename):
            print(f"{Fore.RED}No hay partida guardada en Slot {slot} / No saved game in Slot {slot}{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            # Load player data
            self.player.name = save_data.get("player_name", "Unknown")
            self.player.health = save_data.get("health", 100)
            self.player.money = save_data.get("money", 1000)
            self.player.respect = save_data.get("respect", 0)
            self.player.wanted_level = save_data.get("wanted_level", 0)
            self.player.location = save_data.get("location", "Albuquerque")
            self.player.inventory = save_data.get("inventory", {"fists": 1})
            self.player.drugs = save_data.get("drugs", {})
            self.player.ammo = save_data.get("ammo", {})
            self.player.vehicle = save_data.get("vehicle")
            self.player.gang_affiliation = save_data.get("gang_affiliation")
            self.player.gang_name = save_data.get("gang_name")
            self.player.gang_members = save_data.get("gang_members", [])
            self.player.territory = save_data.get("territory", [])
            self.player.businesses = save_data.get("businesses", [])
            self.player.skills = save_data.get("skills", {})
            self.player.level = save_data.get("level", 1)
            self.player.experience = save_data.get("experience", 0)
            self.player.stats = save_data.get("stats", {})
            self.player.language_mode = save_data.get("language_mode", "bilingual")
            self.player.heat_level = save_data.get("heat_level", 0)
            self.player.prison_time = save_data.get("prison_time", 0)
            
            print(f"{Fore.GREEN}¡Juego cargado desde Slot {slot}! / Game loaded from Slot {slot}!{Style.RESET_ALL}")
            timestamp = save_data.get("save_timestamp", "Unknown")
            print(f"Última guardado: {timestamp}")
            
        except Exception as e:
            print(f"{Fore.RED}Error al cargar: {e}{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def show_slot_info(self):
        """Show information about all save slots"""
        print(f"\n{Fore.CYAN}Información de Slots / Slot Information:{Style.RESET_ALL}")
        print()
        
        for slot in range(1, 4):
            filename = f"mexican_gangsters_slot_{slot}.json"
            print(f"Slot {slot}:")
            
            if os.path.exists(filename):
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        save_data = json.load(f)
                    
                    print(f"  Nombre: {save_data.get('player_name', 'Unknown')}")
                    print(f"  Nivel: {save_data.get('level', 1)}")
                    print(f"  Dinero: ${save_data.get('money', 0):,}")
                    print(f"  Respeto: {save_data.get('respect', 0)}")
                    print(f"  Ubicación: {save_data.get('location', 'Unknown')}")
                    print(f"  Guardado: {save_data.get('save_timestamp', 'Unknown')}")
                    
                except Exception:
                    print(f"  {Fore.RED}Archivo corrupto{Style.RESET_ALL}")
            else:
                print(f"  {Fore.YELLOW}Vacío{Style.RESET_ALL}")
            print()
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def story_missions(self):
        """Main story missions with lore"""
        self.display_header()
        print(f"{Fore.LIGHTMAGENTA_EX}Misiones de Historia / Story Missions{Style.RESET_ALL}")
        print()
        
        # Track story progress
        if not hasattr(self.player, 'story_progress'):
            self.player.story_progress = 0
        
        story_missions = [
            {
                "id": 0,
                "name": "El Principio / The Beginning",
                "spanish": "El Principio",
                "description": "Establece tu presencia en las calles de Nuevo México",
                "english_desc": "Establish your presence on the streets of New Mexico",
                "requirements": {"money": 0, "respect": 0},
                "rewards": {"money": 1000, "respect": 10}
            },
            {
                "id": 1,
                "name": "Primer Contacto / First Contact",
                "spanish": "Primer Contacto",
                "description": "Conecta con los carteles locales",
                "english_desc": "Connect with local cartels",
                "requirements": {"money": 5000, "respect": 25},
                "rewards": {"money": 3000, "respect": 20}
            },
            {
                "id": 2,
                "name": "Territorio en Disputa / Disputed Territory",
                "spanish": "Territorio en Disputa", 
                "description": "Controla tu primer territorio",
                "english_desc": "Control your first territory",
                "requirements": {"money": 10000, "respect": 75, "territories": 1},
                "rewards": {"money": 5000, "respect": 30}
            },
            {
                "id": 3,
                "name": "El Imperio Crece / The Empire Grows",
                "spanish": "El Imperio Crece",
                "description": "Expande tu imperio criminal",
                "english_desc": "Expand your criminal empire",
                "requirements": {"money": 25000, "respect": 150, "businesses": 2},
                "rewards": {"money": 10000, "respect": 50}
            },
            {
                "id": 4,
                "name": "Guerra de Carteles / Cartel War",
                "spanish": "Guerra de Carteles",
                "description": "Enfréntate a los grandes carteles",
                "english_desc": "Face the major cartels",
                "requirements": {"money": 50000, "respect": 300, "gang_members": 5},
                "rewards": {"money": 20000, "respect": 75}
            },
            {
                "id": 5,
                "name": "El Rey de Nuevo México / King of New Mexico",
                "spanish": "El Rey de Nuevo México",
                "description": "Domina todo el estado",
                "english_desc": "Dominate the entire state",
                "requirements": {"money": 100000, "respect": 500, "territories": 5},
                "rewards": {"money": 50000, "respect": 100}
            }
        ]
        
        current_mission = story_missions[min(self.player.story_progress, len(story_missions) - 1)]
        
        print(f"{Fore.YELLOW}Misión Actual / Current Mission:{Style.RESET_ALL}")
        mission_name = current_mission["spanish"] if self.player.language_mode == "spanish" else current_mission["name"]
        description = current_mission["description"] if self.player.language_mode == "spanish" else current_mission["english_desc"]
        
        print(f"• {mission_name}")
        print(f"• {description}")
        print()
        
        # Check requirements
        can_complete = True
        print(f"{Fore.CYAN}Requisitos / Requirements:{Style.RESET_ALL}")
        
        for req, value in current_mission["requirements"].items():
            if req == "money":
                status = "✓" if self.player.money >= value else "✗"
                print(f"{status} Dinero: ${self.player.money:,} / ${value:,}")
                if self.player.money < value:
                    can_complete = False
            elif req == "respect":
                status = "✓" if self.player.respect >= value else "✗"
                print(f"{status} Respeto: {self.player.respect} / {value}")
                if self.player.respect < value:
                    can_complete = False
            elif req == "territories":
                territories = len(self.player.territory)
                status = "✓" if territories >= value else "✗"
                print(f"{status} Territorios: {territories} / {value}")
                if territories < value:
                    can_complete = False
            elif req == "businesses":
                businesses = len(self.player.businesses)
                status = "✓" if businesses >= value else "✗"
                print(f"{status} Negocios: {businesses} / {value}")
                if businesses < value:
                    can_complete = False
            elif req == "gang_members":
                members = len(self.player.gang_members)
                status = "✓" if members >= value else "✗"
                print(f"{status} Miembros: {members} / {value}")
                if members < value:
                    can_complete = False
        
        print()
        
        if can_complete:
            print(f"{Fore.GREEN}¡Puedes completar esta misión! / You can complete this mission!{Style.RESET_ALL}")
            if input("¿Completar misión? / Complete mission? (s/y or n): ").lower() in ['s', 'y']:
                self.complete_story_mission(current_mission)
        else:
            print(f"{Fore.RED}No cumples todos los requisitos / You don't meet all requirements{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def complete_story_mission(self, mission):
        """Complete a story mission"""
        print(f"\n{Fore.GREEN}¡MISIÓN COMPLETADA! / MISSION COMPLETED!{Style.RESET_ALL}")
        
        # Give rewards
        for reward, amount in mission["rewards"].items():
            if reward == "money":
                self.player.add_money(amount)
                print(f"Ganaste ${amount:,}")
            elif reward == "respect":
                self.player.add_respect(amount)
                print(f"Ganaste {amount} puntos de respeto")
        
        # Advance story progress
        self.player.story_progress += 1
        
        # Check if this is the final mission (ending)
        if self.player.story_progress >= 6:
            self.show_ending()
        else:
            print(f"\nProgreso de historia: {self.player.story_progress}/6")

    def show_ending(self):
        """Show the game ending"""
        self.display_header()
        print(f"{Fore.YELLOW}¡FELICITACIONES! / CONGRATULATIONS!{Style.RESET_ALL}")
        print()
        
        ending_text_spanish = """
        Has completado tu ascenso al poder en Nuevo México.
        Desde las humildes calles de Albuquerque hasta controlar todo el estado,
        tu imperio criminal se extiende por cada ciudad y territorio.
        
        Los carteles te respetan, la policía te teme, y tu nombre
        es leyenda en las calles del suroeste.
        
        Pero recuerda: en este mundo, el poder siempre está
        en disputa. Mantén tu imperio fuerte, porque otros
        buscan lo que tú has construido.
        
        Tu legado como el Rey de Nuevo México comienza ahora.
        """
        
        ending_text_english = """
        You have completed your rise to power in New Mexico.
        From the humble streets of Albuquerque to controlling the entire state,
        your criminal empire spans every city and territory.
        
        The cartels respect you, police fear you, and your name
        is legend on the streets of the Southwest.
        
        But remember: in this world, power is always
        contested. Keep your empire strong, because others
        seek what you have built.
        
        Your legacy as the King of New Mexico begins now.
        """
        
        text = ending_text_spanish if self.player.language_mode == "spanish" else ending_text_english
        
        for line in text.strip().split('\n'):
            print(f"{Fore.YELLOW}{line.strip()}{Style.RESET_ALL}")
            time.sleep(0.5)
        
        print(f"\n{Fore.YELLOW}ESTADÍSTICAS FINALES / FINAL STATISTICS:{Style.RESET_ALL}")
        print(f"Dinero total: ${self.player.money:,}")
        print(f"Respeto: {self.player.respect}")
        print(f"Territorios controlados: {len(self.player.territory)}")
        print(f"Negocios: {len(self.player.businesses)}")
        print(f"Miembros de pandilla: {len(self.player.gang_members)}")
        print(f"Misiones completadas: {self.player.stats.get('missions_completed', 0)}")
        print(f"Atracos exitosos: {self.player.stats.get('heists_completed', 0)}")
        
        print(f"\n{Fore.LIGHTBLUE_EX}Puedes continuar jugando en modo libre{Style.RESET_ALL}")
        print("You can continue playing in free mode")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def street_racing_menu(self):
        """Street racing circuit menu"""
        self.display_header()
        print(f"{Fore.LIGHTMAGENTA_EX}CARRERAS CALLEJERAS / STREET RACING{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Victorias en carreras / Racing wins: {self.player.racing_wins}{Style.RESET_ALL}")
        print()
        
        if not self.player.vehicle:
            print(f"{Fore.RED}Necesitas un vehículo para participar en carreras / You need a vehicle to participate in races{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Circuitos Disponibles / Available Circuits:{Style.RESET_ALL}")
        available_circuits = []
        
        for circuit_id, circuit in RACING_CIRCUITS.items():
            if circuit["location"] == self.player.location or self.player.racing_wins >= 5:
                available_circuits.append((circuit_id, circuit))
        
        if not available_circuits:
            print(f"{Fore.YELLOW}No hay circuitos disponibles en esta ciudad / No circuits available in this city{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        for i, (circuit_id, circuit) in enumerate(available_circuits, 1):
            name = circuit["spanish"] if self.player.language_mode == "spanish" else circuit["name"]
            print(f"{i}. {name}")
            print(f"   Ubicación: {circuit['location']}")
            print(f"   Distancia: {circuit['distance']}")
            print(f"   Dificultad: {'★' * circuit['difficulty']}")
            print(f"   Entrada: ${circuit['entry_fee']:,}")
            print(f"   Premio máximo: ${circuit['max_prize']:,}")
            print()
        
        print(f"{len(available_circuits) + 1}. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige un circuito / Choose a circuit: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_circuits):
                circuit_id, circuit = available_circuits[choice_num - 1]
                self.participate_in_race(circuit_id, circuit)
        except ValueError:
            pass
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def participate_in_race(self, circuit_id, circuit):
        """Participate in a street race"""
        if self.player.money < circuit["entry_fee"]:
            print(f"{Fore.RED}No tienes suficiente dinero para la entrada / Not enough money for entry fee{Style.RESET_ALL}")
            return
        
        self.player.remove_money(circuit["entry_fee"])
        
        print(f"\n{Fore.YELLOW}Preparándose para la carrera / Preparing for the race...{Style.RESET_ALL}")
        
        # Calculate racing performance
        if not self.player.vehicle or self.player.vehicle not in VEHICLES:
            print(f"{Fore.RED}Error: Vehículo no válido / Invalid vehicle{Style.RESET_ALL}")
            return
        
        vehicle_info = VEHICLES[self.player.vehicle]
        driving_skill = self.player.skills.get("driving", 0)
        
        performance = (vehicle_info["speed"] * 15) + (driving_skill * 10) + random.randint(1, 30)
        
        # Handle hazards
        hazard_penalties = 0
        for hazard in circuit["hazards"]:
            if random.randint(1, 100) <= 25:
                hazard_penalties += random.randint(5, 15)
                if hazard == "police_checkpoints":
                    print(f"{Fore.RED}¡Control policial! / Police checkpoint!{Style.RESET_ALL}")
                    self.player.increase_wanted_level(1)
                elif hazard == "sand_storms":
                    print(f"{Fore.YELLOW}¡Tormenta de arena! / Sand storm!{Style.RESET_ALL}")
                elif hazard == "sharp_turns":
                    print(f"{Fore.YELLOW}¡Curvas peligrosas! / Dangerous turns!{Style.RESET_ALL}")
        
        final_performance = max(10, performance - hazard_penalties)
        
        # Determine race result
        if final_performance >= 80:
            # Victory
            prize = circuit["max_prize"]
            print(f"\n{Fore.GREEN}¡VICTORIA! / VICTORY!{Style.RESET_ALL}")
            print("¡Ganaste la carrera! / You won the race!")
            print(f"Premio: ${prize:,}")
            
            self.player.add_money(prize)
            self.player.racing_wins += 1
            self.player.add_respect(10)
            self.player.add_experience(25)
            
            # Check for achievements
            if self.player.racing_wins == 1:
                self.unlock_achievement("Primer Piloto / First Racer")
            elif self.player.racing_wins == 10:
                self.unlock_achievement("Rey de la Carretera / King of the Road")
            
        elif final_performance >= 60:
            # Second place
            prize = circuit["max_prize"] // 2
            print(f"\n{Fore.YELLOW}¡SEGUNDO LUGAR! / SECOND PLACE!{Style.RESET_ALL}")
            print("Buen trabajo, pero no fue suficiente / Good job, but not enough")
            print(f"Premio: ${prize:,}")
            
            self.player.add_money(prize)
            self.player.add_respect(5)
            self.player.add_experience(15)
            
        else:
            # Loss
            print(f"\n{Fore.RED}¡DERROTA! / DEFEAT!{Style.RESET_ALL}")
            print("No lograste terminar entre los primeros / You didn't finish in the top positions")
            
            # Small consolation prize
            consolation = circuit["entry_fee"] // 4
            if consolation > 0:
                print(f"Premio de consolación: ${consolation:,}")
                self.player.add_money(consolation)
            
            self.player.add_experience(5)

    def fighting_tournament_menu(self):
        """Fighting tournament menu"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}TORNEOS DE PELEA / FIGHTING TOURNAMENTS{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Victorias en torneos / Tournament wins: {self.player.fighting_wins}{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.CYAN}Torneos Disponibles / Available Tournaments:{Style.RESET_ALL}")
        available_tournaments = []
        
        for tournament_id, tournament in FIGHTING_TOURNAMENTS.items():
            if tournament["location"] == self.player.location or self.player.fighting_wins >= 3:
                available_tournaments.append((tournament_id, tournament))
        
        if not available_tournaments:
            print(f"{Fore.YELLOW}No hay torneos disponibles en esta ciudad / No tournaments available in this city{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        for i, (tournament_id, tournament) in enumerate(available_tournaments, 1):
            name = tournament["spanish"] if self.player.language_mode == "spanish" else tournament["name"]
            print(f"{i}. {name}")
            print(f"   Ubicación: {tournament['location']}")
            print(f"   Rondas: {tournament['rounds']}")
            print(f"   Entrada: ${tournament['entry_fee']:,}")
            print(f"   Premio máximo: ${tournament['max_prize']:,}")
            print()
        
        print(f"{len(available_tournaments) + 1}. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige un torneo / Choose a tournament: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_tournaments):
                tournament_id, tournament = available_tournaments[choice_num - 1]
                self.participate_in_tournament(tournament_id, tournament)
        except ValueError:
            pass
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def participate_in_tournament(self, tournament_id, tournament):
        """Participate in a fighting tournament"""
        if self.player.money < tournament["entry_fee"]:
            print(f"{Fore.RED}No tienes suficiente dinero para la entrada / Not enough money for entry fee{Style.RESET_ALL}")
            return
        
        self.player.remove_money(tournament["entry_fee"])
        
        print(f"\n{Fore.YELLOW}Entrando al torneo / Entering tournament...{Style.RESET_ALL}")
        
        # Tournament progression
        strength_skill = self.player.skills.get("strength", 0)
        current_health = self.player.health
        rounds_won = 0
        
        for round_num in range(1, tournament["rounds"] + 1):
            print(f"\n{Fore.CYAN}Ronda {round_num} / Round {round_num}{Style.RESET_ALL}")
            
            # Opponent strength increases each round
            opponent_strength = 50 + (round_num * 15) + random.randint(1, 20)
            player_strength = (strength_skill * 12) + (current_health * 0.5) + random.randint(1, 25)
            
            # Weapon bonus
            weapon_bonus = 0
            for weapon in self.player.inventory:
                if weapon in WEAPONS and WEAPONS[weapon]["type"] == "melee":
                    weapon_bonus += WEAPONS[weapon]["damage"] // 2
            
            player_strength += weapon_bonus
            
            print(f"Tu fuerza: {int(player_strength)}")
            print(f"Fuerza del oponente: {int(opponent_strength)}")
            
            if player_strength > opponent_strength:
                print(f"{Fore.GREEN}¡Ganaste la ronda! / You won the round!{Style.RESET_ALL}")
                rounds_won += 1
                damage_taken = random.randint(5, 15)
            else:
                print(f"{Fore.RED}Perdiste la ronda / You lost the round{Style.RESET_ALL}")
                damage_taken = random.randint(20, 35)
                break
            
            current_health -= damage_taken
            print(f"Daño recibido: {damage_taken}")
            
            if current_health <= 20:
                print(f"{Fore.RED}Estás muy herido para continuar / Too injured to continue{Style.RESET_ALL}")
                break
        
        # Tournament results
        if rounds_won == tournament["rounds"]:
            # Victory
            prize = tournament["max_prize"]
            print(f"\n{Fore.GREEN}¡CAMPEÓN DEL TORNEO! / TOURNAMENT CHAMPION!{Style.RESET_ALL}")
            print("¡Ganaste el torneo completo! / You won the entire tournament!")
            print(f"Premio: ${prize:,}")
            
            self.player.add_money(prize)
            self.player.fighting_wins += 1
            self.player.add_respect(15)
            self.player.add_experience(35)
            
            # Check for achievements
            if self.player.fighting_wins == 1:
                self.unlock_achievement("Primer Luchador / First Fighter")
            elif self.player.fighting_wins == 5:
                self.unlock_achievement("Campeón Invencible / Undefeated Champion")
            
        elif rounds_won >= tournament["rounds"] // 2:
            # Partial victory
            prize = tournament["max_prize"] // 3
            print(f"\n{Fore.YELLOW}¡BUEN DESEMPEÑO! / GOOD PERFORMANCE!{Style.RESET_ALL}")
            print("Llegaste lejos en el torneo / You made it far in the tournament")
            print(f"Premio: ${prize:,}")
            
            self.player.add_money(prize)
            self.player.add_respect(8)
            self.player.add_experience(20)
        else:
            # Early elimination
            print(f"\n{Fore.RED}ELIMINADO TEMPRANO / EARLY ELIMINATION{Style.RESET_ALL}")
            print("Necesitas entrenar más / You need more training")
            self.player.add_experience(10)
        
        # Apply health damage
        health_loss = (tournament["rounds"] - rounds_won) * 8
        self.player.take_damage(health_loss)

    def property_investment_menu(self):
        """Property investment and management menu"""
        self.display_header()
        print(f"{Fore.LIGHTGREEN_EX}INVERSIONES INMOBILIARIAS / PROPERTY INVESTMENTS{Style.RESET_ALL}")
        print()
        
        # Show owned properties
        if self.player.properties:
            print(f"{Fore.CYAN}Propiedades Poseídas / Owned Properties:{Style.RESET_ALL}")
            total_upkeep = 0
            total_income = 0
            
            for prop_id in self.player.properties:
                prop_info = PROPERTIES[prop_id]
                name = prop_info["spanish"] if self.player.language_mode == "spanish" else prop_info["name"]
                print(f"• {name}")
                print(f"  Mantenimiento mensual: ${prop_info['monthly_upkeep']:,}")
                total_upkeep += prop_info["monthly_upkeep"]
                
                if "daily_income" in prop_info["benefits"]:
                    daily_income = prop_info["benefits"]["daily_income"]
                    total_income += daily_income
                    print(f"  Ingresos diarios: ${daily_income:,}")
                
                print()
            
            print(f"{Fore.GREEN}Ingresos diarios totales: ${total_income:,}{Style.RESET_ALL}")
            print(f"{Fore.RED}Mantenimiento mensual total: ${total_upkeep:,}{Style.RESET_ALL}")
            print()
        
        # Show available properties
        print(f"{Fore.CYAN}Propiedades Disponibles / Available Properties:{Style.RESET_ALL}")
        available_properties = []
        
        for prop_id, prop_info in PROPERTIES.items():
            if prop_id not in self.player.properties:
                available_properties.append((prop_id, prop_info))
        
        if not available_properties:
            print(f"{Fore.YELLOW}Posees todas las propiedades disponibles / You own all available properties{Style.RESET_ALL}")
        else:
            for i, (prop_id, prop_info) in enumerate(available_properties, 1):
                name = prop_info["spanish"] if self.player.language_mode == "spanish" else prop_info["name"]
                print(f"{i}. {name}")
                print(f"   Costo: ${prop_info['cost']:,}")
                print(f"   Mantenimiento mensual: ${prop_info['monthly_upkeep']:,}")
                print(f"   Descripción: {prop_info['description']}")
                
                # Show benefits
                benefits = []
                for benefit, value in prop_info["benefits"].items():
                    if benefit == "heat_reduction":
                        benefits.append(f"Reducción de calor: {value}")
                    elif benefit == "storage_space":
                        benefits.append(f"Espacio de almacenamiento: {value}")
                    elif benefit == "daily_income":
                        benefits.append(f"Ingresos diarios: ${value:,}")
                    elif benefit == "reputation_boost":
                        benefits.append(f"Aumento de reputación: {value}")
                    elif benefit == "prestige":
                        benefits.append(f"Prestigio: {value}")
                    elif benefit == "gang_capacity":
                        benefits.append(f"Capacidad de pandilla: {value}")
                
                print(f"   Beneficios: {', '.join(benefits)}")
                print()
        
        print(f"{len(available_properties) + 1}. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué propiedad quieres comprar? / Which property do you want to buy?: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_properties):
                prop_id, prop_info = available_properties[choice_num - 1]
                self.buy_property(prop_id, prop_info)
        except ValueError:
            pass
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def buy_property(self, prop_id, prop_info):
        """Buy a property"""
        if self.player.money < prop_info["cost"]:
            print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
            return
        
        name = prop_info["spanish"] if self.player.language_mode == "spanish" else prop_info["name"]
        
        print(f"\n¿Comprar {name} por ${prop_info['cost']:,}?")
        if input("Confirmar compra (s/y or n): ").lower() in ['s', 'y']:
            self.player.remove_money(prop_info["cost"])
            self.player.properties.append(prop_id)
            
            # Apply benefits
            for benefit, value in prop_info["benefits"].items():
                if benefit == "prestige":
                    self.player.prestige += value
                elif benefit == "reputation_boost":
                    self.player.add_respect(value)
            
            print(f"{Fore.GREEN}¡Propiedad comprada! / Property purchased!{Style.RESET_ALL}")
            print(f"Ahora posees: {name}")
            
            # Check for achievements
            if len(self.player.properties) == 1:
                self.unlock_achievement("Primer Propietario / First Property Owner")
            elif len(self.player.properties) == len(PROPERTIES):
                self.unlock_achievement("Magnate Inmobiliario / Real Estate Magnate")

    def npc_relationship_menu(self):
        """NPC relationship management menu"""
        self.display_header()
        print(f"{Fore.LIGHTBLUE_EX}RELACIONES CON NPCs / NPC RELATIONSHIPS{Style.RESET_ALL}")
        print()
        
        # Show current relationships
        print(f"{Fore.CYAN}Relaciones Actuales / Current Relationships:{Style.RESET_ALL}")
        
        for npc_id, npc_info in NPCS.items():
            relationship_level = self.player.npc_relationships.get(npc_id, 0)
            
            if relationship_level >= 75:
                status = f"{Fore.GREEN}Aliado / Ally"
            elif relationship_level >= 50:
                status = f"{Fore.YELLOW}Amigo / Friend"
            elif relationship_level >= 25:
                status = f"{Fore.BLUE}Conocido / Acquaintance"
            elif relationship_level <= -25:
                status = f"{Fore.RED}Enemigo / Enemy"
            else:
                status = f"{Fore.WHITE}Neutral"
            
            print(f"• {npc_info['name']} ({npc_info['location']})")
            print(f"  Estado: {status}{Style.RESET_ALL} ({relationship_level}/100)")
            print()
        
        # NPC interaction options
        print(f"{Fore.CYAN}NPCs Disponibles / Available NPCs:{Style.RESET_ALL}")
        
        # Filter NPCs by current location
        available_npcs = []
        for npc_id, npc_info in NPCS.items():
            if npc_info["location"] == self.player.location:
                available_npcs.append((npc_id, npc_info))
        
        if not available_npcs:
            print(f"{Fore.YELLOW}No hay NPCs disponibles en esta ciudad / No NPCs available in this city{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        for i, (npc_id, npc_info) in enumerate(available_npcs, 1):
            relationship_level = self.player.npc_relationships.get(npc_id, 0)
            print(f"{i}. {npc_info['name']}")
            print(f"   Servicios: {', '.join(npc_info['services'])}")
            print(f"   Relación: {relationship_level}/100")
            print()
        
        print(f"{len(available_npcs) + 1}. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Con quién quieres interactuar? / Who do you want to interact with?: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_npcs):
                npc_id, npc_info = available_npcs[choice_num - 1]
                self.interact_with_npc(npc_id, npc_info)
        except ValueError:
            pass
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def interact_with_npc(self, npc_id, npc_info):
        """Interact with an NPC"""
        relationship_level = self.player.npc_relationships.get(npc_id, 0)
        
        print(f"\n{Fore.YELLOW}Interactuando con {npc_info['name']}{Style.RESET_ALL}")
        
        # Choose appropriate dialogue
        if relationship_level >= 50:
            dialogue = npc_info["dialogue"]["friendly"]
        elif relationship_level <= -25:
            dialogue = npc_info["dialogue"]["hostile"]
        else:
            dialogue = npc_info["dialogue"]["greeting"]
        
        print(f'"{dialogue}"')
        print()
        
        # Interaction options
        print(f"1. {Fore.GREEN}Conversar / Chat{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Solicitar servicios / Request services{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Hacer regalo / Give gift{Style.RESET_ALL}")
        print(f"4. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué quieres hacer? / What do you want to do?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.chat_with_npc(npc_id, npc_info)
        elif choice == "2" and relationship_level >= 0:
            self.request_npc_services(npc_id, npc_info)
        elif choice == "2":
            print(f"{Fore.RED}Esta persona no confía en ti lo suficiente / This person doesn't trust you enough{Style.RESET_ALL}")
        elif choice == "3":
            self.give_gift_to_npc(npc_id, npc_info)

    def chat_with_npc(self, npc_id, npc_info):
        """Chat with an NPC to improve relationship"""
        relationship_improvement = random.randint(2, 8)
        
        if npc_id not in self.player.npc_relationships:
            self.player.npc_relationships[npc_id] = 0
        
        self.player.npc_relationships[npc_id] = min(100, self.player.npc_relationships[npc_id] + relationship_improvement)
        
        print(f"{Fore.GREEN}Tuviste una buena conversación / You had a good conversation{Style.RESET_ALL}")
        print(f"Relación mejorada en {relationship_improvement} puntos")

    def request_npc_services(self, npc_id, npc_info):
        """Request services from an NPC"""
        relationship_level = self.player.npc_relationships.get(npc_id, 0)
        
        print(f"{Fore.CYAN}Servicios Disponibles / Available Services:{Style.RESET_ALL}")
        
        for i, service in enumerate(npc_info["services"], 1):
            cost = 500 + (i * 200)  # Variable cost based on service
            
            if relationship_level >= 50:
                cost = int(cost * 0.7)  # Friend discount
            
            print(f"{i}. {service.replace('_', ' ').title()} - ${cost:,}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué servicio necesitas? / What service do you need?: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(npc_info["services"]):
                service = npc_info["services"][choice_num - 1]
                cost = 500 + (choice_num * 200)
                
                if relationship_level >= 50:
                    cost = int(cost * 0.7)
                
                if self.player.money >= cost:
                    self.player.remove_money(cost)
                    self.provide_npc_service(service, npc_info)
                else:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
        except ValueError:
            pass

    def provide_npc_service(self, service, npc_info):
        """Provide the requested NPC service"""
        if service == "police_intel":
            if self.player.wanted_level > 0:
                self.player.decrease_wanted_level(1)
                print(f"{Fore.GREEN}Información policial obtenida - Nivel de búsqueda reducido{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No hay actividad policial que reportar{Style.RESET_ALL}")
        
        elif service == "gang_info":
            print(f"{Fore.BLUE}Información valiosa sobre pandillas rivales obtenida{Style.RESET_ALL}")
            self.player.add_respect(5)
        
        elif service == "job_tips":
            bonus_money = random.randint(200, 800)
            self.player.add_money(bonus_money)
            print(f"{Fore.GREEN}Consejo de trabajo útil - Ganaste ${bonus_money:,} extra{Style.RESET_ALL}")
        
        elif service == "vehicle_upgrades":
            if self.player.vehicle:
                print(f"{Fore.GREEN}Vehículo mejorado - Mejor rendimiento en carreras{Style.RESET_ALL}")
                # Could add vehicle upgrade system here
            else:
                print(f"{Fore.YELLOW}No tienes vehículo para mejorar{Style.RESET_ALL}")
        
        elif service == "rare_weapons":
            rare_weapon = random.choice(["katana", "desert_eagle", "combat_shotgun"])
            if rare_weapon not in self.player.inventory:
                self.player.inventory[rare_weapon] = 1
                print(f"{Fore.GREEN}Arma rara obtenida: {WEAPONS[rare_weapon]['name']}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Ya posees esa arma{Style.RESET_ALL}")

    def give_gift_to_npc(self, npc_id, npc_info):
        """Give a gift to an NPC"""
        if not self.player.inventory or len(self.player.inventory) == 0:
            print(f"{Fore.YELLOW}No tienes objetos para regalar / You have no items to give{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Objetos Disponibles / Available Items:{Style.RESET_ALL}")
        
        # Convert inventory dict to list for display
        inventory_items = list(self.player.inventory.keys())
        for i, item in enumerate(inventory_items, 1):
            quantity = self.player.inventory[item]
            print(f"{i}. {item} (x{quantity})")
        
        choice = input(f"\n{Fore.CYAN}¿Qué quieres regalar? / What do you want to give?: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(inventory_items):
                item = inventory_items[choice_num - 1]
                
                # Calculate gift value
                gift_value = random.randint(5, 20)
                
                if npc_id not in self.player.npc_relationships:
                    self.player.npc_relationships[npc_id] = 0
                
                self.player.npc_relationships[npc_id] = min(100, self.player.npc_relationships[npc_id] + gift_value)
                
                # Remove one unit of the item or delete if only one left
                if self.player.inventory[item] > 1:
                    self.player.inventory[item] -= 1
                else:
                    del self.player.inventory[item]
                
                print(f"{Fore.GREEN}Regalo entregado / Gift given{Style.RESET_ALL}")
                print(f"Relación mejorada en {gift_value} puntos")
        except ValueError:
            pass

    def achievement_center(self):
        """Achievement center to view unlocked achievements"""
        self.display_header()
        print(f"{Fore.LIGHTYELLOW_EX}CENTRO DE LOGROS / ACHIEVEMENT CENTER{Style.RESET_ALL}")
        print()
        
        if not self.player.achievements:
            print(f"{Fore.YELLOW}No has desbloqueado logros aún / You haven't unlocked any achievements yet{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Logros Desbloqueados / Unlocked Achievements:{Style.RESET_ALL}")
            for i, achievement in enumerate(self.player.achievements, 1):
                print(f"{i}. {achievement}")
        
        print(f"\n{Fore.CYAN}Logros Disponibles / Available Achievements:{Style.RESET_ALL}")
        
        # List potential achievements
        potential_achievements = [
            "Primer Piloto / First Racer - Gana tu primera carrera",
            "Rey de la Carretera / King of the Road - Gana 10 carreras",
            "Primer Luchador / First Fighter - Gana tu primer torneo",
            "Campeón Invencible / Undefeated Champion - Gana 5 torneos",
            "Primer Propietario / First Property Owner - Compra tu primera propiedad",
            "Magnate Inmobiliario / Real Estate Magnate - Posee todas las propiedades",
            "Diplomático / Diplomat - Alcanza nivel 75 con un NPC",
            "Rey del Crimen / Crime King - Completa la historia principal",
            "Agente de la Ley / Law Enforcement Officer - Únete a la policía",
            "Policía Veterano / Veteran Officer - Realiza 10 arrestos",
            "Azote del Crimen / Scourge of Crime - Realiza 50 arrestos",
            "Capitán de Policía / Police Captain - Alcanza el rango de Capitán"
        ]
        
        for achievement in potential_achievements:
            status = "✓" if any(ach in achievement for ach in self.player.achievements) else "✗"
            print(f"{status} {achievement}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def unlock_achievement(self, achievement):
        """Unlock an achievement"""
        if achievement not in self.player.achievements:
            self.player.achievements.append(achievement)
            print(f"\n{Fore.YELLOW}🏆 ¡LOGRO DESBLOQUEADO! / ACHIEVEMENT UNLOCKED!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{achievement}{Style.RESET_ALL}")
            
            # Achievement rewards
            self.player.add_money(1000)
            self.player.add_respect(10)
            print("Recompensa: $1,000 y 10 puntos de respeto")

    def police_career_menu(self):
        """Police career system menu"""
        self.display_header()
        print(f"{Fore.LIGHTCYAN_EX}CARRERA POLICIAL / POLICE CAREER{Style.RESET_ALL}")
        print()
        
        if not self.player.is_police:
            print(f"{Fore.YELLOW}No eres miembro de la policía / You are not a police officer{Style.RESET_ALL}")
            print()
            print(f"1. {Fore.GREEN}Unirse a la policía / Join the police force{Style.RESET_ALL}")
            print(f"2. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}¿Qué quieres hacer? / What do you want to do?: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.join_police_force()
        else:
            # Display police status
            if not self.player.police_rank or self.player.police_rank not in POLICE_RANKS:
                print(f"{Fore.RED}Error: Rango policial inválido / Invalid police rank{Style.RESET_ALL}")
                self.player.is_police = False
                self.player.police_rank = None
                return
            
            rank_info = POLICE_RANKS[self.player.police_rank]
            rank_name = rank_info["spanish"] if self.player.language_mode == "spanish" else rank_info["name"]
            
            print(f"{Fore.CYAN}Estado Policial / Police Status:{Style.RESET_ALL}")
            print(f"Rango: {rank_name}")
            print(f"Arrestos totales: {self.player.total_arrests}")
            print(f"Salario base: ${rank_info['salary']:,}")
            print(f"Nivel de corrupción: {self.player.police_corruption}/100")
            print(f"Operaciones completadas: {self.player.police_operations_completed}")
            print()
            
            print(f"1. {Fore.GREEN}Realizar operación policial / Conduct police operation{Style.RESET_ALL}")
            print(f"2. {Fore.BLUE}Investigar crimen / Investigate crime{Style.RESET_ALL}")
            print(f"3. {Fore.YELLOW}Solicitar ascenso / Request promotion{Style.RESET_ALL}")
            print(f"4. {Fore.RED}Actividades corruptas / Corrupt activities{Style.RESET_ALL}")
            print(f"5. {Fore.MAGENTA}Renunciar a la policía / Resign from police{Style.RESET_ALL}")
            print(f"6. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}¿Qué quieres hacer? / What do you want to do?: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.conduct_police_operation()
            elif choice == "2":
                self.investigate_crime()
            elif choice == "3":
                self.request_promotion()
            elif choice == "4":
                self.corrupt_activities()
            elif choice == "5":
                self.resign_from_police()
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def join_police_force(self):
        """Join the police force by demonstrating good citizenship"""
        print(f"\n{Fore.YELLOW}RECLUTAMIENTO POLICIAL / POLICE RECRUITMENT{Style.RESET_ALL}")
        print()
        
        # Check eligibility
        if self.player.wanted_level > 0:
            print(f"{Fore.RED}No puedes unirte a la policía con antecedentes criminales{Style.RESET_ALL}")
            print("Wanted level must be 0 to join the police force")
            return
        
        if self.player.gang_affiliation or self.player.gang_name:
            print(f"{Fore.RED}Debes abandonar tu pandilla primero{Style.RESET_ALL}")
            print("You must leave your gang first")
            return
        
        print("Requisitos para unirse a la policía:")
        print("Requirements to join the police:")
        print("- Sin antecedentes criminales / No criminal record")
        print("- Sin afiliación a pandillas / No gang affiliation")
        print("- Demostrar servicio a la comunidad / Demonstrate community service")
        print("- Ayudar a detener criminales / Help stop criminals")
        print()
        
        print("Tu progreso hacia el reclutamiento:")
        print("Your progress toward recruitment:")
        print(f"Buenas acciones realizadas: {self.player.good_deeds}/10")
        print(f"Criminales detenidos: {self.player.criminals_stopped}/5")
        print()
        
        # Check if player meets requirements
        if self.player.good_deeds >= 10 and self.player.criminals_stopped >= 5:
            print(f"{Fore.GREEN}¡Cumples todos los requisitos! / You meet all requirements!{Style.RESET_ALL}")
            print()
            
            if input("¿Aceptar invitación para unirte a la policía? / Accept invitation to join police? (s/y or n): ").lower() in ['s', 'y']:
                self.player.is_police = True
                self.player.police_rank = "cadet"
                self.player.police_corruption = 0
                self.player.total_arrests = 0
                self.player.police_operations_completed = 0
                
                # Clear criminal attributes and lose gang reputation
                if self.player.gang_affiliation or self.player.gang_name:
                    print(f"\n{Fore.YELLOW}CONSECUENCIAS DE UNIRSE A LA POLICÍA / CONSEQUENCES OF JOINING POLICE{Style.RESET_ALL}")
                    print("Tu decisión de unirte a la policía tiene consecuencias:")
                    print("Your decision to join the police has consequences:")
                    print("- Pierdes toda reputación con pandillas / Lost all gang reputation")
                    print("- Los criminales te consideran traidor / Criminals consider you a traitor")
                    print("- Tus antiguos contactos te evitarán / Your old contacts will avoid you")
                    
                self.player.gang_affiliation = None
                self.player.gang_name = None
                self.player.gang_members = []
                self.player.territory = []
                self.player.businesses = []
                self.player.heat_level = 0
                
                # Lose respect from criminal underworld
                original_respect = self.player.respect
                self.player.respect = max(0, self.player.respect - 50)
                respect_lost = original_respect - self.player.respect
                
                # Reward for good citizenship
                self.player.add_money(2000)  # Signing bonus
                
                print(f"\n{Fore.GREEN}¡Felicitaciones! Te has unido a la policía{Style.RESET_ALL}")
                print("Congratulations! You have joined the police force")
                print("Rango inicial: Cadete de Policía / Police Cadet")
                print("Bono de firma: $2,000")
                
                if respect_lost > 0:
                    print(f"{Fore.RED}Respeto perdido en el submundo: -{respect_lost}{Style.RESET_ALL}")
                    print("Underworld respect lost due to joining law enforcement")
                
                self.unlock_achievement("Agente de la Ley / Law Enforcement Officer")
        else:
            print(f"{Fore.YELLOW}Necesitas hacer más buenas acciones para calificar{Style.RESET_ALL}")
            print("You need to do more good deeds to qualify")
            print()
            print("Formas de conseguir buenas acciones:")
            print("Ways to earn good deeds:")
            print("- Ayudar ciudadanos durante la exploración / Help citizens while exploring")
            print("- Detener crímenes en progreso / Stop crimes in progress")
            print("- Reportar actividad criminal / Report criminal activity")
            print("- Rechazar participar en actividades criminales / Refuse criminal activities")

    def conduct_police_operation(self):
        """Conduct various police operations"""
        self.display_header()
        print(f"{Fore.LIGHTCYAN_EX}OPERACIONES POLICIALES / POLICE OPERATIONS{Style.RESET_ALL}")
        print()
        
        if not self.player.police_rank or self.player.police_rank not in POLICE_RANKS:
            print(f"{Fore.RED}Error: Rango policial inválido / Invalid police rank{Style.RESET_ALL}")
            return
        
        rank_abilities = POLICE_RANKS[self.player.police_rank]["abilities"]
        available_operations = []
        
        for op_id, operation in POLICE_OPERATIONS.items():
            if any(ability in rank_abilities for ability in [op_id, op_id.replace("_", "")]):
                available_operations.append((op_id, operation))
        
        if not available_operations:
            print(f"{Fore.YELLOW}No hay operaciones disponibles para tu rango{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Operaciones Disponibles / Available Operations:{Style.RESET_ALL}")
        
        for i, (op_id, operation) in enumerate(available_operations, 1):
            name = operation["spanish"] if self.player.language_mode == "spanish" else operation["name"]
            print(f"{i}. {name}")
            print(f"   Duración: {operation['time']} horas")
            print(f"   Bono salarial: ${operation['salary_bonus']:,}")
            print(f"   Probabilidad de arresto: {operation['arrest_chance']}%")
            print(f"   Riesgo de corrupción: {operation['corruption_risk']}%")
            print()
        
        print(f"{len(available_operations) + 1}. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige una operación / Choose an operation: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_operations):
                op_id, operation = available_operations[choice_num - 1]
                self.execute_police_operation(op_id, operation)
        except ValueError:
            pass

    def execute_police_operation(self, op_id, operation):
        """Execute a specific police operation"""
        print(f"\n{Fore.YELLOW}Ejecutando operación / Executing operation...{Style.RESET_ALL}")
        
        # Calculate success based on skills and rank
        base_success = 60
        skill_bonus = (self.player.skills.get("shooting", 0) + self.player.skills.get("stealth", 0)) * 3
        if not self.player.police_rank:
            rank_bonus = 0
        else:
            rank_bonus = list(POLICE_RANKS.keys()).index(self.player.police_rank) * 5
        
        success_chance = min(95, base_success + skill_bonus + rank_bonus)
        
        if random.randint(1, 100) <= success_chance:
            # Successful operation
            print(f"{Fore.GREEN}¡Operación exitosa! / Operation successful!{Style.RESET_ALL}")
            
            # Salary bonus
            salary_bonus = operation["salary_bonus"]
            self.player.add_money(salary_bonus)
            print(f"Bono salarial: ${salary_bonus:,}")
            
            # Arrest chance
            if random.randint(1, 100) <= operation["arrest_chance"]:
                arrests_made = random.randint(1, 3)
                self.player.total_arrests += arrests_made
                print(f"Arrestos realizados: {arrests_made}")
                
                # Check for achievements
                if self.player.total_arrests >= 10:
                    self.unlock_achievement("Policía Veterano / Veteran Officer")
                if self.player.total_arrests >= 50:
                    self.unlock_achievement("Azote del Crimen / Scourge of Crime")
            
            # Experience and respect
            self.player.add_experience(operation["time"] * 5)
            self.player.add_respect(3)
            self.player.police_operations_completed += 1
            
        else:
            # Failed operation
            print(f"{Fore.RED}Operación fallida / Operation failed{Style.RESET_ALL}")
            
            # Potential consequences
            if random.randint(1, 100) <= 30:
                damage = random.randint(10, 25)
                self.player.take_damage(damage)
                print(f"Herido en el servicio: -{damage} salud")
        
        # Corruption risk
        if random.randint(1, 100) <= operation["corruption_risk"]:
            corruption_increase = random.randint(1, 5)
            self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
            print(f"{Fore.YELLOW}Exposición a la corrupción: +{corruption_increase}{Style.RESET_ALL}")

    def investigate_crime(self):
        """Investigate ongoing crimes"""
        print(f"\n{Fore.BLUE}INVESTIGACIÓN CRIMINAL / CRIME INVESTIGATION{Style.RESET_ALL}")
        print()
        
        # Generate random case
        cases = [
            {
                "name": "Robo a mano armada / Armed robbery",
                "difficulty": 2,
                "reward": 300,
                "arrests": 1
            },
            {
                "name": "Tráfico de drogas / Drug trafficking", 
                "difficulty": 3,
                "reward": 500,
                "arrests": 2
            },
            {
                "name": "Actividad de pandillas / Gang activity",
                "difficulty": 4,
                "reward": 800,
                "arrests": 3
            },
            {
                "name": "Operación del cartel / Cartel operation",
                "difficulty": 5,
                "reward": 1200,
                "arrests": 4
            }
        ]
        
        case = random.choice(cases)
        
        print(f"Caso asignado: {case['name']}")
        print(f"Dificultad: {'★' * case['difficulty']}")
        print(f"Recompensa: ${case['reward']:,}")
        print()
        
        # Investigation choices
        print(f"1. {Fore.GREEN}Investigación directa / Direct investigation{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Trabajo encubierto / Undercover work{Style.RESET_ALL}")
        print(f"3. {Fore.BLUE}Cooperar con informantes / Work with informants{Style.RESET_ALL}")
        print(f"4. {Fore.CYAN}Cancelar / Cancel{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Método de investigación / Investigation method: {Style.RESET_ALL}").strip()
        
        success_chance = 50
        corruption_risk = 0
        
        if choice == "1":
            # Direct investigation
            success_chance = 60 + (self.player.skills.get("charisma", 0) * 5)
            corruption_risk = 5
        elif choice == "2":
            # Undercover work
            success_chance = 70 + (self.player.skills.get("stealth", 0) * 5)
            corruption_risk = 15
        elif choice == "3":
            # Work with informants
            success_chance = 80 + (self.player.skills.get("charisma", 0) * 3)
            corruption_risk = 25
        else:
            return
        
        # Account for case difficulty
        success_chance -= case["difficulty"] * 10
        success_chance = max(20, min(90, success_chance))
        
        if random.randint(1, 100) <= success_chance:
            print(f"\n{Fore.GREEN}¡Investigación exitosa! / Investigation successful!{Style.RESET_ALL}")
            self.player.add_money(case["reward"])
            self.player.total_arrests += case["arrests"]
            self.player.add_experience(case["difficulty"] * 10)
            print(f"Recompensa: ${case['reward']:,}")
            print(f"Arrestos: {case['arrests']}")
        else:
            print(f"\n{Fore.RED}Investigación fallida / Investigation failed{Style.RESET_ALL}")
            print("El caso permanece sin resolver")
        
        # Corruption check
        if corruption_risk > 0 and random.randint(1, 100) <= corruption_risk:
            corruption_increase = random.randint(2, 8)
            self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
            print(f"{Fore.YELLOW}Corrupción aumentada: +{corruption_increase}{Style.RESET_ALL}")

    def request_promotion(self):
        """Request a promotion to higher rank"""
        print(f"\n{Fore.YELLOW}SOLICITUD DE ASCENSO / PROMOTION REQUEST{Style.RESET_ALL}")
        print()
        
        if not self.player.police_rank:
            print(f"{Fore.RED}Error: No tienes rango policial / No police rank{Style.RESET_ALL}")
            return
        
        current_rank_index = list(POLICE_RANKS.keys()).index(self.player.police_rank)
        
        if current_rank_index >= len(POLICE_RANKS) - 1:
            print(f"{Fore.YELLOW}Ya tienes el rango más alto / You already have the highest rank{Style.RESET_ALL}")
            return
        
        next_rank_key = list(POLICE_RANKS.keys())[current_rank_index + 1]
        next_rank = POLICE_RANKS[next_rank_key]
        
        rank_name = next_rank["spanish"] if self.player.language_mode == "spanish" else next_rank["name"]
        
        print(f"Rango objetivo: {rank_name}")
        print(f"Salario: ${next_rank['salary']:,}")
        print()
        
        print("Requisitos:")
        can_promote = True
        
        for requirement, value in next_rank["requirements"].items():
            if requirement == "corruption":
                status = "✓" if self.player.police_corruption <= value else "✗"
                print(f"{status} Corrupción máxima: {self.player.police_corruption} / {value}")
                if self.player.police_corruption > value:
                    can_promote = False
            elif requirement == "arrests":
                status = "✓" if self.player.total_arrests >= value else "✗"
                print(f"{status} Arrestos mínimos: {self.player.total_arrests} / {value}")
                if self.player.total_arrests < value:
                    can_promote = False
        
        if can_promote:
            print(f"\n{Fore.GREEN}¡Ascenso aprobado! / Promotion approved!{Style.RESET_ALL}")
            self.player.police_rank = next_rank_key
            print(f"Nuevo rango: {rank_name}")
            print(f"Nuevo salario: ${next_rank['salary']:,}")
            
            # Achievement check
            if next_rank_key == "captain":
                self.unlock_achievement("Capitán de Policía / Police Captain")
        else:
            print(f"\n{Fore.RED}Ascenso denegado / Promotion denied{Style.RESET_ALL}")
            print("No cumples todos los requisitos")

    def corrupt_activities(self):
        """Engage in corrupt police activities"""
        print(f"\n{Fore.RED}ACTIVIDADES CORRUPTAS / CORRUPT ACTIVITIES{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  Advertencia: Estas actividades aumentan tu corrupción{Style.RESET_ALL}")
        print()
        
        print(f"1. {Fore.RED}Aceptar soborno / Accept bribe{Style.RESET_ALL}")
        print(f"2. {Fore.RED}Vender evidencia / Sell evidence{Style.RESET_ALL}")
        print(f"3. {Fore.RED}Proteger criminales / Protect criminals{Style.RESET_ALL}")
        print(f"4. {Fore.RED}Robar del depósito / Steal from evidence{Style.RESET_ALL}")
        print(f"5. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué actividad corrupta? / What corrupt activity?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Accept bribe
            bribe_amount = random.randint(500, 2000)
            corruption_increase = random.randint(10, 20)
            
            print(f"Oferta de soborno: ${bribe_amount:,}")
            print(f"Aumento de corrupción: +{corruption_increase}")
            
            if input("¿Aceptar soborno? / Accept bribe? (s/y or n): ").lower() in ['s', 'y']:
                self.player.add_money(bribe_amount)
                self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
                print(f"{Fore.GREEN}Soborno aceptado / Bribe accepted{Style.RESET_ALL}")
        
        elif choice == "2":
            # Sell evidence
            evidence_value = random.randint(800, 1500)
            corruption_increase = random.randint(15, 25)
            
            print(f"Valor de la evidencia: ${evidence_value:,}")
            print(f"Aumento de corrupción: +{corruption_increase}")
            
            if input("¿Vender evidencia? / Sell evidence? (s/y or n): ").lower() in ['s', 'y']:
                self.player.add_money(evidence_value)
                self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
                print(f"{Fore.GREEN}Evidencia vendida / Evidence sold{Style.RESET_ALL}")
        
        elif choice == "3":
            # Protect criminals
            protection_fee = random.randint(1000, 3000)
            corruption_increase = random.randint(20, 30)
            
            print(f"Pago por protección: ${protection_fee:,}")
            print(f"Aumento de corrupción: +{corruption_increase}")
            
            if input("¿Ofrecer protección? / Offer protection? (s/y or n): ").lower() in ['s', 'y']:
                self.player.add_money(protection_fee)
                self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
                print(f"{Fore.GREEN}Protección ofrecida / Protection offered{Style.RESET_ALL}")
        
        elif choice == "4":
            # Steal from evidence
            stolen_value = random.randint(300, 1000)
            corruption_increase = random.randint(25, 35)
            
            print(f"Valor robado: ${stolen_value:,}")
            print(f"Aumento de corrupción: +{corruption_increase}")
            
            if input("¿Robar del depósito? / Steal from evidence? (s/y or n): ").lower() in ['s', 'y']:
                self.player.add_money(stolen_value)
                self.player.police_corruption = min(100, self.player.police_corruption + corruption_increase)
                print(f"{Fore.GREEN}Robo completado / Theft completed{Style.RESET_ALL}")
        
        # Check for corruption consequences
        if self.player.police_corruption >= 80:
            print(f"\n{Fore.RED}⚠️  ADVERTENCIA: Tu nivel de corrupción es muy alto{Style.RESET_ALL}")
            print("Riesgo de investigación interna")

    def resign_from_police(self):
        """Resign from the police force"""
        print(f"\n{Fore.YELLOW}RENUNCIA POLICIAL / POLICE RESIGNATION{Style.RESET_ALL}")
        print()
        
        print("¿Estás seguro de que quieres renunciar a la policía?")
        print("Are you sure you want to resign from the police?")
        print()
        print("Perderás:")
        print("You will lose:")
        print("- Rango policial / Police rank")
        print("- Salario policial / Police salary")
        print("- Acceso a operaciones / Access to operations")
        print()
        
        if input("¿Confirmar renuncia? / Confirm resignation? (s/y or n): ").lower() in ['s', 'y']:
            # Calculate severance pay based on rank and service
            if not self.player.police_rank:
                print(f"{Fore.RED}Error: No tienes rango policial / No police rank{Style.RESET_ALL}")
                return
            
            rank_index = list(POLICE_RANKS.keys()).index(self.player.police_rank)
            severance = (rank_index + 1) * 500 + (self.player.police_operations_completed * 50)
            
            self.player.add_money(severance)
            
            # Reset police attributes
            self.player.is_police = False
            self.player.police_rank = None
            self.player.police_corruption = 0
            
            print(f"\n{Fore.GREEN}Renuncia procesada / Resignation processed{Style.RESET_ALL}")
            print(f"Pago de liquidación: ${severance:,}")
            print("Ahora eres un civil / You are now a civilian")

    def witness_crime(self):
        """Witness a crime in progress and choose how to respond"""
        crimes = [
            "Ves a alguien robando un auto / You see someone stealing a car",
            "Presencias un atraco a mano armada / You witness an armed robbery", 
            "Observas tráfico de drogas / You observe drug trafficking",
            "Ves vandalismo en progreso / You see vandalism in progress"
        ]
        
        crime = random.choice(crimes)
        print(f"\n{Fore.YELLOW}CRIMEN EN PROGRESO / CRIME IN PROGRESS{Style.RESET_ALL}")
        print(crime)
        print()
        
        print(f"1. {Fore.GREEN}Intervenir y detener el crimen / Intervene and stop the crime{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Llamar a la policía / Call the police{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Ignorar y alejarse / Ignore and walk away{Style.RESET_ALL}")
        print(f"4. {Fore.RED}Unirse a los criminales / Join the criminals{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué haces? / What do you do?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            success_chance = 40 + (self.player.skills.get("strength", 0) * 8)
            
            if random.randint(1, 100) <= success_chance:
                print(f"{Fore.GREEN}¡Detuviste el crimen! / You stopped the crime!{Style.RESET_ALL}")
                print()
                
                # If player is police, show police options
                if self.player.is_police:
                    print("Como oficial de policía, ¿qué haces con el criminal?")
                    print("As a police officer, what do you do with the criminal?")
                    print()
                    print(f"1. {Fore.GREEN}Detener al criminal / Detain the criminal{Style.RESET_ALL}")
                    print(f"2. {Fore.YELLOW}Dejarlo ir / Let the criminal go{Style.RESET_ALL}")
                    print(f"3. {Fore.RED}Pedir soborno para dejarlo ir / Ask for bribe to let them go{Style.RESET_ALL}")
                    
                    police_choice = input(f"\n{Fore.CYAN}¿Qué decides? / What do you decide?: {Style.RESET_ALL}").strip()
                    
                    if police_choice == "1":
                        # Official arrest - good police work
                        print(f"{Fore.GREEN}Arrestaste al criminal oficialmente / You officially arrested the criminal{Style.RESET_ALL}")
                        self.player.good_deeds += 3
                        self.player.criminals_stopped += 1
                        self.player.total_arrests += 1
                        reward = random.randint(300, 600)
                        self.player.add_money(reward)
                        print("Buenas acciones: +3, Arrestos: +1")
                        print(f"Bono policial: ${reward:,}")
                        
                    elif police_choice == "2":
                        # Let go - minimal good deed
                        print(f"{Fore.YELLOW}Dejaste ir al criminal con una advertencia / You let the criminal go with a warning{Style.RESET_ALL}")
                        self.player.good_deeds += 1
                        print("Buenas acciones: +1")
                        
                    elif police_choice == "3":
                        # Corruption attempt
                        bribe_success = random.randint(1, 100)
                        if bribe_success <= 60:  # 60% chance of success
                            bribe_amount = random.randint(500, 1500)
                            print(f"{Fore.YELLOW}El criminal aceptó pagar soborno / The criminal agreed to pay bribe{Style.RESET_ALL}")
                            self.player.add_money(bribe_amount)
                            self.player.police_corruption += 10
                            print(f"Soborno recibido: ${bribe_amount:,}")
                            print("Corrupción aumentada: +10")
                            
                            # Lose reputation with law enforcement community
                            self.player.respect = max(0, self.player.respect - 5)
                            print("Respeto perdido por corrupción: -5")
                        else:
                            # Criminal fights back
                            print(f"{Fore.RED}¡El criminal se resistió y atacó! / The criminal resisted and attacked!{Style.RESET_ALL}")
                            damage = random.randint(20, 35)
                            self.player.take_damage(damage)
                            self.player.police_corruption += 5
                            print(f"Daño recibido: {damage}")
                            print("Corrupción aumentada: +5")
                else:
                    # Civilian intervention
                    self.player.good_deeds += 2
                    self.player.criminals_stopped += 1
                    self.player.add_respect(5)
                    reward = random.randint(200, 500)
                    self.player.add_money(reward)
                    print("Buenas acciones: +2, Criminales detenidos: +1")
                    print(f"Recompensa de la víctima: ${reward:,}")
            else:
                print(f"{Fore.RED}Los criminales te atacaron / The criminals attacked you{Style.RESET_ALL}")
                damage = random.randint(15, 30)
                self.player.take_damage(damage)
                print(f"Daño recibido: {damage}")
                
        elif choice == "2":
            print(f"{Fore.GREEN}Llamaste a la policía / You called the police{Style.RESET_ALL}")
            self.player.good_deeds += 1
            print("Buenas acciones: +1")
            
            if random.randint(1, 100) <= 60:
                print("La policía llegó a tiempo y arrestó a los criminales")
                self.player.criminals_stopped += 1
                print("Criminales detenidos: +1")
                
                # If player is police, they get credit for the call
                if self.player.is_police:
                    print("Como oficial fuera de servicio, recibes reconocimiento")
                    print("As an off-duty officer, you receive recognition")
                    self.player.total_arrests += 1
                    bonus = random.randint(100, 200)
                    self.player.add_money(bonus)
                    print(f"Bono policial: ${bonus:,}")
                
        elif choice == "3":
            print(f"{Fore.YELLOW}Te alejaste sin hacer nada / You walked away without doing anything{Style.RESET_ALL}")
            
        elif choice == "4":
            # Check if player is police - major consequences
            if self.player.is_police:
                print(f"{Fore.RED}¡GRAVE ERROR! Participaste en actividad criminal siendo policía{Style.RESET_ALL}")
                print("SERIOUS MISCONDUCT! You participated in criminal activity as a police officer")
                print()
                
                money_gained = random.randint(300, 800)
                self.player.add_money(money_gained)
                self.player.increase_wanted_level(2)  # Higher wanted level for corrupt cop
                self.player.police_corruption += 25
                self.player.heat_level += 20
                
                print(f"Dinero ganado: ${money_gained:,}")
                print("Nivel de búsqueda aumentado: +2")
                print("Corrupción policial aumentada: +25")
                
                # Chance of being discovered and fired
                if random.randint(1, 100) <= 30:
                    print(f"\n{Fore.RED}¡TU PARTICIPACIÓN FUE DESCUBIERTA!{Style.RESET_ALL}")
                    print("YOUR PARTICIPATION WAS DISCOVERED!")
                    print("Has sido expulsado de la fuerza policial")
                    print("You have been expelled from the police force")
                    
                    self.player.is_police = False
                    self.player.police_rank = None
                    self.player.police_corruption = 0
                    
            else:
                print(f"{Fore.RED}Te uniste a los criminales / You joined the criminals{Style.RESET_ALL}")
                money_gained = random.randint(300, 800)
                self.player.add_money(money_gained)
                self.player.increase_wanted_level(1)
                self.player.heat_level += 10
                print(f"Dinero ganado: ${money_gained:,}")
                print("Nivel de búsqueda aumentado")

    def help_citizen(self):
        """Help a citizen in need"""
        situations = [
            "Una persona mayor necesita ayuda con sus compras / An elderly person needs help with groceries",
            "Alguien perdió su billetera / Someone lost their wallet",
            "Un turista está perdido / A tourist is lost", 
            "Un automóvil se averió en la carretera / A car broke down on the road"
        ]
        
        situation = random.choice(situations)
        print(f"\n{Fore.CYAN}CIUDADANO NECESITA AYUDA / CITIZEN NEEDS HELP{Style.RESET_ALL}")
        print(situation)
        print()
        
        print(f"1. {Fore.GREEN}Ayudar sin esperar nada / Help without expecting anything{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Ayudar por dinero / Help for money{Style.RESET_ALL}")
        print(f"3. {Fore.RED}Ignorar / Ignore{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué haces? / What do you do?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            print(f"{Fore.GREEN}Ayudaste desinteresadamente / You helped selflessly{Style.RESET_ALL}")
            self.player.good_deeds += 2
            self.player.add_respect(3)
            print("Buenas acciones: +2")
            
            if random.randint(1, 100) <= 30:
                reward = random.randint(100, 300)
                self.player.add_money(reward)
                print(f"La persona te dio una propina: ${reward:,}")
                
        elif choice == "2":
            print(f"{Fore.YELLOW}Ayudaste por una tarifa / You helped for a fee{Style.RESET_ALL}")
            self.player.good_deeds += 1
            payment = random.randint(50, 150)
            self.player.add_money(payment)
            print(f"Buenas acciones: +1, Pago: ${payment:,}")
            
        elif choice == "3":
            print(f"{Fore.RED}Ignoraste a la persona / You ignored the person{Style.RESET_ALL}")

    def report_suspicious_activity(self):
        """Report suspicious activity to authorities"""
        activities = [
            "Ves personas sospechosas merodeando / You see suspicious people lurking",
            "Notas actividad extraña en un edificio / You notice strange activity in a building",
            "Observas un vehículo abandonado / You observe an abandoned vehicle",
            "Escuchas ruidos sospechosos / You hear suspicious noises"
        ]
        
        activity = random.choice(activities)
        print(f"\n{Fore.YELLOW}ACTIVIDAD SOSPECHOSA / SUSPICIOUS ACTIVITY{Style.RESET_ALL}")
        print(activity)
        print()
        
        print(f"1. {Fore.GREEN}Reportar a las autoridades / Report to authorities{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}Investigar por tu cuenta / Investigate yourself{Style.RESET_ALL}")
        print(f"3. {Fore.YELLOW}Ignorar / Ignore{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué haces? / What do you do?: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            print(f"{Fore.GREEN}Reportaste la actividad sospechosa / You reported the suspicious activity{Style.RESET_ALL}")
            self.player.good_deeds += 1
            print("Buenas acciones: +1")
            
            if random.randint(1, 100) <= 40:
                print("Tu reporte llevó a arrestos importantes")
                self.player.criminals_stopped += 1
                reward = random.randint(200, 400)
                self.player.add_money(reward)
                print(f"Criminales detenidos: +1, Recompensa: ${reward:,}")
                
                # Police get additional credit
                if self.player.is_police:
                    self.player.total_arrests += 1
                    bonus = random.randint(150, 300)
                    self.player.add_money(bonus)
                    print(f"Bono policial adicional: ${bonus:,}")
                
        elif choice == "2":
            print(f"{Fore.BLUE}Decidiste investigar por tu cuenta / You decided to investigate yourself{Style.RESET_ALL}")
            
            investigation_success = 30 + (self.player.skills.get("stealth", 0) * 10)
            
            if random.randint(1, 100) <= investigation_success:
                print(f"{Fore.GREEN}Descubriste una operación criminal / You discovered a criminal operation{Style.RESET_ALL}")
                self.player.good_deeds += 2
                self.player.criminals_stopped += 2
                reward = random.randint(500, 1000)
                self.player.add_money(reward)
                print("Buenas acciones: +2, Criminales detenidos: +2")
                print(f"Recompensa policial: ${reward:,}")
            else:
                print(f"{Fore.RED}Te descubrieron investigando / You were caught investigating{Style.RESET_ALL}")
                damage = random.randint(10, 25)
                self.player.take_damage(damage)
                print(f"Daño recibido: {damage}")
                
        elif choice == "3":
            print(f"{Fore.YELLOW}Decidiste ignorar la situación / You decided to ignore the situation{Style.RESET_ALL}")

    def enhanced_business_ventures_menu(self):
        """Enhanced business ventures system with advanced criminal enterprises"""
        self.display_header()
        print(f"{Fore.LIGHTGREEN_EX}EMPRESAS CRIMINALES AVANZADAS / ADVANCED CRIMINAL ENTERPRISES{Style.RESET_ALL}")
        print()
        
        # Show current ventures
        if self.player.business_ventures:
            print(f"{Fore.CYAN}Tus Empresas Actuales / Your Current Ventures:{Style.RESET_ALL}")
            total_daily = 0
            total_upkeep = 0
            for venture_id in self.player.business_ventures:
                venture = BUSINESS_VENTURES[venture_id]
                name = venture["spanish_name"] if self.player.language_mode == "spanish" else venture["name"]
                print(f"• {name}")
                print(f"  Ingresos diarios: ${venture['daily_income']:,}")
                print(f"  Mantenimiento: ${venture['upkeep']:,}")
                print(f"  Nivel de riesgo: {'★' * venture['risk_level']}")
                total_daily += venture["daily_income"]
                total_upkeep += venture["upkeep"]
                print()
            
            print(f"{Fore.GREEN}Ingresos diarios totales: ${total_daily:,}{Style.RESET_ALL}")
            print(f"{Fore.RED}Gastos diarios totales: ${total_upkeep:,}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Beneficio neto: ${total_daily - total_upkeep:,}{Style.RESET_ALL}")
            print()
        
        # Show available ventures
        print(f"{Fore.CYAN}Empresas Disponibles / Available Ventures:{Style.RESET_ALL}")
        available_ventures = []
        
        for venture_id, venture in BUSINESS_VENTURES.items():
            if venture_id not in self.player.business_ventures:
                name = venture["spanish_name"] if self.player.language_mode == "spanish" else venture["name"]
                
                can_afford = self.player.money >= venture["cost"]
                meets_level = self.player.get_criminal_level() >= venture["requirements"]["criminal_level"]
                
                color = Fore.GREEN if can_afford and meets_level else Fore.RED
                
                print(f"{color}{len(available_ventures) + 1}. {name}{Style.RESET_ALL}")
                print(f"   Costo: ${venture['cost']:,}")
                print(f"   Ingresos diarios: ${venture['daily_income']:,}")
                print(f"   Mantenimiento: ${venture['upkeep']:,}")
                print(f"   Nivel criminal requerido: {venture['requirements']['criminal_level']}")
                print(f"   Nivel de riesgo: {'★' * venture['risk_level']}")
                print()
                
                available_ventures.append(venture_id)
        
        if not available_ventures:
            print(f"{Fore.YELLOW}Ya posees todas las empresas disponibles / You own all available ventures{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"0. {Fore.YELLOW}Volver al menú principal / Back to main menu{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}Elige una empresa para comprar / Choose a venture to purchase: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(available_ventures):
                venture_id = available_ventures[choice - 1]
                venture = BUSINESS_VENTURES[venture_id]
                
                if self.player.money < venture["cost"]:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                elif self.player.get_criminal_level() < venture["requirements"]["criminal_level"]:
                    print(f"{Fore.RED}Nivel criminal insuficiente / Criminal level too low{Style.RESET_ALL}")
                else:
                    name = venture["spanish_name"] if self.player.language_mode == "spanish" else venture["name"]
                    
                    print(f"\n{Fore.YELLOW}¿Confirmas la compra de {name} por ${venture['cost']:,}?{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Confirm purchase of {name} for ${venture['cost']:,}?{Style.RESET_ALL}")
                    
                    confirm = input("(y/n): ").lower().strip()
                    if confirm == 'y':
                        if self.player.add_business_venture(venture_id):
                            print(f"{Fore.GREEN}¡Empresa adquirida exitosamente! / Enterprise acquired successfully!{Style.RESET_ALL}")
                            print(f"Atención policial aumentada en: +{venture['police_attention']}")
                            
                            if venture_id == "money_laundering":
                                self.unlock_achievement("El Blanqueador / The Launderer")
                            elif venture_id == "drug_lab":
                                self.unlock_achievement("Químico Maestro / Master Chemist")
                        else:
                            print(f"{Fore.RED}Error al adquirir la empresa / Error acquiring enterprise{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid option{Style.RESET_ALL}")
        
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def special_events_system(self):
        """Handle special dynamic events"""
        self.display_header()
        print(f"{Fore.LIGHTMAGENTA_EX}EVENTOS ESPECIALES / SPECIAL EVENTS{Style.RESET_ALL}")
        print()
        
        # Check for active event
        if self.player.current_special_event:
            event_id = self.player.current_special_event
            event = SPECIAL_EVENTS[event_id]
            
            print(f"{Fore.YELLOW}{event['name']}{Style.RESET_ALL}")
            print(event['description'])
            print()
            
            if event_id == "cartel_meeting":
                print(f"{Fore.GREEN}Evento del cartel en progreso / Cartel event in progress{Style.RESET_ALL}")
            elif event_id == "police_raid":
                print(f"{Fore.RED}Redada policial activa / Police raid active{Style.RESET_ALL}")
            elif event_id == "gang_war":
                print(f"{Fore.YELLOW}Guerra de pandillas / Gang war{Style.RESET_ALL}")
            elif event_id == "corrupt_official":
                print(f"{Fore.BLUE}Oficial corrupto disponible / Corrupt official available{Style.RESET_ALL}")
            
            return
        
        # Try to trigger new event
        triggered_event = self.player.trigger_special_event()
        
        if triggered_event:
            event = SPECIAL_EVENTS[triggered_event]
            print(f"{Fore.YELLOW}EVENTO ACTIVADO / EVENT TRIGGERED{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{event['name']}{Style.RESET_ALL}")
            print(event['description'])
            print()
            
            print(f"1. {Fore.GREEN}Participar / Participate{Style.RESET_ALL}")
            print(f"2. {Fore.YELLOW}Ignorar / Ignore{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Tu decisión / Your choice: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                print(f"{Fore.GREEN}Decidiste participar en el evento / You decided to participate{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Decidiste ignorar el evento / You decided to ignore the event{Style.RESET_ALL}")
                self.player.current_special_event = None
        else:
            print(f"{Fore.CYAN}No hay eventos especiales disponibles en este momento{Style.RESET_ALL}")
            print(f"{Fore.CYAN}No special events available at this time{Style.RESET_ALL}")
            print()
            print(f"{Fore.YELLOW}Los eventos se activan basados en:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Events are triggered based on:{Style.RESET_ALL}")
            print("• Tu nivel de respeto / Your respect level")
            print("• Tu nivel criminal / Your criminal level")
            print("• Tu afiliación a pandillas / Your gang affiliation")
            print("• Tu nivel de búsqueda / Your wanted level")
            print("• Tu dinero disponible / Your available money")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def enhanced_reputation_system(self):
        """Display enhanced reputation and standing"""
        self.display_header()
        print(f"{Fore.LIGHTCYAN_EX}SISTEMA DE REPUTACIÓN / REPUTATION SYSTEM{Style.RESET_ALL}")
        print()
        
        # Current reputation
        title = self.player.get_reputation_title()
        criminal_level = self.player.get_criminal_level()
        
        print(f"{Fore.YELLOW}Tu Reputación Actual / Your Current Reputation:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Título: {title}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Nivel Criminal: {criminal_level}/5{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Respeto: {self.player.respect}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Prestigio: {self.player.prestige}{Style.RESET_ALL}")
        print()
        
        # Show reputation levels
        print(f"{Fore.CYAN}Niveles de Reputación / Reputation Levels:{Style.RESET_ALL}")
        for level, data in REPUTATION_SYSTEM.items():
            current = "👑" if data["min_respect"] <= self.player.respect <= data["max_respect"] else "  "
            color = Fore.YELLOW if current == "👑" else Fore.WHITE
            print(f"{current} {color}{data['title']} ({data['min_respect']}-{data['max_respect']} respeto){Style.RESET_ALL}")
        
        print()
        
        # Factors affecting reputation
        print(f"{Fore.CYAN}Factores que Afectan la Reputación / Factors Affecting Reputation:{Style.RESET_ALL}")
        print(f"• Misiones completadas: {self.player.stats['missions_completed']}")
        print(f"• Personas eliminadas: {self.player.stats['people_killed']}")
        print(f"• Atracos completados: {self.player.stats['heists_completed']}")
        print(f"• Territorio controlado: {len(self.player.territory)}")
        print(f"• Miembros de pandilla: {len(self.player.gang_members)}")
        print(f"• Empresas criminales: {len(self.player.business_ventures)}")
        
        # Benefits of current level
        print(f"\n{Fore.CYAN}Beneficios del Nivel Actual / Current Level Benefits:{Style.RESET_ALL}")
        if criminal_level >= 2:
            print("• Acceso a trabajos criminales de nivel medio")
        if criminal_level >= 3:
            print("• Puede liderar una pandilla")
            print("• Acceso a laboratorios de drogas")
        if criminal_level >= 4:
            print("• Puede controlar territorio")
            print("• Acceso a operaciones de contrabando")
        if criminal_level >= 5:
            print("• Acceso a todos los negocios criminales")
            print("• Puede iniciar guerras de pandillas")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def language_menu(self):
        """Language selection menu"""
        self.display_header()
        print(f"{Fore.LIGHTCYAN_EX}CONFIGURACIÓN DE IDIOMA / LANGUAGE SETTINGS{Style.RESET_ALL}")
        print()
        
        current_mode = self.player.language_mode
        print(f"{Fore.YELLOW}Modo actual / Current mode: {current_mode.title()}{Style.RESET_ALL}")
        print()
        
        print(f"1. {Fore.GREEN}Español solamente / Spanish only{Style.RESET_ALL}")
        print(f"2. {Fore.BLUE}English only{Style.RESET_ALL}")
        print(f"3. {Fore.MAGENTA}Bilingüe / Bilingual{Style.RESET_ALL}")
        print(f"4. {Fore.YELLOW}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Selecciona idioma / Select language (1-4): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.player.language_mode = "spanish"
            print(f"{Fore.GREEN}Idioma cambiado a español{Style.RESET_ALL}")
        elif choice == "2":
            self.player.language_mode = "english"
            print(f"{Fore.GREEN}Language changed to English{Style.RESET_ALL}")
        elif choice == "3":
            self.player.language_mode = "bilingual"
            print(f"{Fore.GREEN}Modo bilingüe activado / Bilingual mode activated{Style.RESET_ALL}")
        elif choice == "4":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid option{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def allocate_skill_points(self):
        """Skill point allocation menu"""
        self.display_header()
        print(f"{Fore.LIGHTGREEN_EX}ASIGNACIÓN DE PUNTOS DE HABILIDAD / SKILL POINT ALLOCATION{Style.RESET_ALL}")
        print()
        
        if self.player.skill_points <= 0:
            print(f"{Fore.YELLOW}No tienes puntos de habilidad disponibles / No skill points available{Style.RESET_ALL}")
            print("Gana experiencia para obtener más puntos / Gain experience to earn more points")
            input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Puntos disponibles / Available points: {self.player.skill_points}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Nivel actual / Current level: {self.player.level}{Style.RESET_ALL}")
        print()
        
        # Display current skills
        print(f"{Fore.YELLOW}Habilidades actuales / Current skills:{Style.RESET_ALL}")
        skill_list = []
        for i, (skill, level) in enumerate(self.player.skills.items(), 1):
            stars = "★" * level + "☆" * (10 - level)
            print(f"{i}. {skill.capitalize()}: {stars} ({level}/10)")
            skill_list.append(skill)
        
        print(f"\n0. {Fore.YELLOW}Volver / Back{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}Elige habilidad para mejorar / Choose skill to improve: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(skill_list):
                skill = skill_list[choice - 1]
                current_level = self.player.skills[skill]
                
                if current_level >= 10:
                    print(f"{Fore.RED}Esta habilidad ya está al máximo / This skill is already at maximum{Style.RESET_ALL}")
                else:
                    self.player.skills[skill] += 1
                    self.player.skill_points -= 1
                    print(f"{Fore.GREEN}¡{skill.capitalize()} mejorado! / {skill.capitalize()} improved!{Style.RESET_ALL}")
                    print(f"Nuevo nivel / New level: {self.player.skills[skill]}/10")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid option{Style.RESET_ALL}")
        
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def casino_gambling_menu(self):
        """Advanced casino and gambling system"""
        self.display_header()
        print(f"{Fore.LIGHTMAGENTA_EX}🎰 CASINO EL DORADO 🎰{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}¡Bienvenido al casino más exclusivo de Nuevo México! / Welcome to New Mexico's most exclusive casino!{Style.RESET_ALL}")
        print()
        
        # Check if player has enough money
        if self.player.money < 100:
            print(f"{Fore.RED}Necesitas al menos $100 para jugar / You need at least $100 to play{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"💰 Dinero disponible / Available money: ${self.player.money:,}")
        print()
        
        print(f"1. {Fore.RED}Póker Texas Hold'em (Apuesta mínima: $500){Style.RESET_ALL}")
        print(f"2. {Fore.BLACK}Blackjack (Apuesta mínima: $200){Style.RESET_ALL}")  
        print(f"3. {Fore.GREEN}Ruleta (Apuesta mínima: $100){Style.RESET_ALL}")
        print(f"4. {Fore.YELLOW}Máquinas tragamonedas / Slot machines ($50-$1000){Style.RESET_ALL}")
        print(f"5. {Fore.BLUE}Carreras de caballos / Horse racing{Style.RESET_ALL}")
        print(f"6. {Fore.MAGENTA}Pelea de gallos / Cockfighting{Style.RESET_ALL}")
        print(f"7. {Fore.CYAN}Apuestas deportivas / Sports betting{Style.RESET_ALL}")
        print(f"0. {Fore.WHITE}Salir / Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige tu juego / Choose your game: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.play_poker()
        elif choice == "2":
            self.play_blackjack()
        elif choice == "3":
            self.play_roulette()
        elif choice == "4":
            self.play_slots()
        elif choice == "5":
            self.horse_racing()
        elif choice == "6":
            self.cockfighting()
        elif choice == "7":
            self.sports_betting()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def play_poker(self):
        """Texas Hold'em poker game"""
        min_bet = 500
        if self.player.money < min_bet:
            print(f"{Fore.RED}No tienes suficiente dinero / Not enough money (Minimum: ${min_bet}){Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.RED}♠️ TEXAS HOLD'EM POKER ♠️{Style.RESET_ALL}")
        print("Mesa VIP - Competición de alto nivel / VIP Table - High stakes competition")
        
        bet = min(min_bet * random.randint(1, 3), self.player.money // 2)
        print(f"Tu apuesta / Your bet: ${bet:,}")
        
        # Simulate poker hand strength (1-10)
        player_hand = random.randint(1, 10) + (self.player.skills.get("charisma", 1) // 2)
        dealer_hand = random.randint(1, 10)
        
        hand_names = ["Par bajo", "Par medio", "Par alto", "Doble par", "Trío", 
                     "Escalera", "Color", "Full house", "Póker", "Escalera real"]
        
        print(f"\nTu mano: {hand_names[min(player_hand-1, 9)]}")
        print("Evaluando manos...")
        
        if player_hand > dealer_hand:
            winnings = bet * random.randint(2, 4)
            self.player.money += winnings
            print(f"{Fore.GREEN}¡Ganaste! / You won! +${winnings:,}{Style.RESET_ALL}")
            self.player.add_experience(50)
        else:
            self.player.money -= bet
            print(f"{Fore.RED}Perdiste / You lost: -${bet:,}{Style.RESET_ALL}")

    def play_blackjack(self):
        """Blackjack card game"""
        min_bet = 200
        if self.player.money < min_bet:
            print(f"{Fore.RED}No tienes suficiente dinero / Not enough money (Minimum: ${min_bet}){Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.BLACK}♣️ BLACKJACK 21 ♣️{Style.RESET_ALL}")
        
        bet = min(min_bet * random.randint(1, 2), self.player.money // 3)
        print(f"Tu apuesta / Your bet: ${bet:,}")
        
        # Simple blackjack simulation
        player_cards = random.randint(15, 21)  # Player gets decent cards
        dealer_cards = random.randint(17, 22)   # Dealer might bust
        
        print(f"Tus cartas suman: {player_cards}")
        print(f"Cartas del dealer: {dealer_cards}")
        
        if player_cards == 21:
            winnings = bet * 2
            self.player.money += winnings
            print(f"{Fore.GREEN}¡BLACKJACK! ¡Ganaste! / BLACKJACK! You won! +${winnings:,}{Style.RESET_ALL}")
        elif player_cards > 21:
            self.player.money -= bet
            print(f"{Fore.RED}Te pasaste / Bust! -${bet:,}{Style.RESET_ALL}")
        elif dealer_cards > 21 or player_cards > dealer_cards:
            winnings = bet
            self.player.money += winnings
            print(f"{Fore.GREEN}¡Ganaste! / You won! +${winnings:,}{Style.RESET_ALL}")
        else:
            self.player.money -= bet
            print(f"{Fore.RED}Perdiste / You lost: -${bet:,}{Style.RESET_ALL}")

    def play_roulette(self):
        """Roulette game"""
        min_bet = 100
        if self.player.money < min_bet:
            print(f"{Fore.RED}No tienes suficiente dinero / Not enough money (Minimum: ${min_bet}){Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🎯 RULETA EUROPEA 🎯{Style.RESET_ALL}")
        print("1. Rojo/Negro (Paga 2:1)")
        print("2. Par/Impar (Paga 2:1)")  
        print("3. Número específico (Paga 35:1)")
        
        bet_type = input("Tipo de apuesta / Bet type (1-3): ").strip()
        bet_amount = min(min_bet * random.randint(1, 5), self.player.money // 4)
        
        winning_number = random.randint(0, 36)
        print(f"\n¡La bola cayó en: {winning_number}!")
        
        won = False
        multiplier = 1
        
        if bet_type == "1":  # Color
            color_choice = input("Rojo (r) o Negro (n)? / Red (r) or Black (n)?: ").lower()
            is_red = winning_number in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
            if (color_choice == "r" and is_red) or (color_choice == "n" and not is_red and winning_number != 0):
                won = True
                multiplier = 2
        elif bet_type == "2":  # Even/Odd
            parity = input("Par (p) o Impar (i)? / Even (e) or Odd (o)?: ").lower()
            if (parity in ["p", "e"] and winning_number % 2 == 0 and winning_number != 0) or \
               (parity in ["i", "o"] and winning_number % 2 == 1):
                won = True
                multiplier = 2
        elif bet_type == "3":  # Specific number
            try:
                chosen_number = int(input("Número (0-36) / Number (0-36): "))
                if chosen_number == winning_number:
                    won = True
                    multiplier = 35
            except ValueError:
                print("Número inválido / Invalid number")
                return
        
        if won:
            winnings = bet_amount * multiplier
            self.player.money += winnings
            print(f"{Fore.GREEN}¡Ganaste! / You won! +${winnings:,}{Style.RESET_ALL}")
            self.player.add_experience(30)
        else:
            self.player.money -= bet_amount
            print(f"{Fore.RED}Perdiste / You lost: -${bet_amount:,}{Style.RESET_ALL}")

    def play_slots(self):
        """Slot machine game"""
        print(f"\n{Fore.YELLOW}🎰 MÁQUINAS TRAGAMONEDAS 🎰{Style.RESET_ALL}")
        print("Elige tu máquina / Choose your machine:")
        print("1. Clásica ($50-$200)")
        print("2. Video Poker ($100-$500)")
        print("3. Jackpot Progresivo ($500-$2000)")
        
        machine_choice = input("Máquina / Machine (1-3): ").strip()
        
        if machine_choice == "1":
            bet_range = (50, 200)
            jackpot_chance = 0.05
        elif machine_choice == "2":
            bet_range = (100, 500)
            jackpot_chance = 0.03
        elif machine_choice == "3":
            bet_range = (500, 2000)
            jackpot_chance = 0.01
        else:
            print("Opción inválida / Invalid choice")
            return
        
        bet = min(random.randint(bet_range[0], bet_range[1]), self.player.money // 3)
        if self.player.money < bet:
            print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
            return
        
        print(f"\nApuesta: ${bet:,}")
        print("🎰 Girando... / Spinning...")
        print("🍒 🍋 🍊")
        
        luck = random.random()
        if luck < jackpot_chance:
            # Jackpot!
            winnings = bet * random.randint(50, 100)
            self.player.money += winnings
            print(f"{Fore.YELLOW}🎉 ¡¡¡JACKPOT!!! 🎉 +${winnings:,}{Style.RESET_ALL}")
            self.player.add_experience(100)
        elif luck < 0.2:
            # Small win
            winnings = bet * random.randint(2, 5)
            self.player.money += winnings
            print(f"{Fore.GREEN}¡Ganaste! / You won! +${winnings:,}{Style.RESET_ALL}")
        else:
            # Loss
            self.player.money -= bet
            print(f"{Fore.RED}Perdiste / You lost: -${bet:,}{Style.RESET_ALL}")

    def horse_racing(self):
        """Horse racing betting"""
        print(f"\n{Fore.BLUE}🐎 HIPÓDROMO SANTA FE 🐎{Style.RESET_ALL}")
        
        horses = [
            {"name": "Rayo Plateado", "odds": "3:1", "chance": 0.25},
            {"name": "Viento del Norte", "odds": "5:1", "chance": 0.15},
            {"name": "Estrella Fugaz", "odds": "2:1", "chance": 0.30},
            {"name": "Trueno Negro", "odds": "8:1", "chance": 0.10},
            {"name": "Corazón Valiente", "odds": "4:1", "chance": 0.20}
        ]
        
        print("Caballos en carrera / Horses racing:")
        for i, horse in enumerate(horses, 1):
            print(f"{i}. {horse['name']} - Cuotas: {horse['odds']}")
        
        try:
            horse_choice = int(input("\nElige caballo / Choose horse (1-5): ")) - 1
            bet = min(random.randint(200, 1000), self.player.money // 3)
            
            if horse_choice < 0 or horse_choice >= len(horses):
                print("Caballo inválido / Invalid horse")
                return
            
            if self.player.money < bet:
                print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                return
            
            chosen_horse = horses[horse_choice]
            print(f"\nApuesta: ${bet:,} en {chosen_horse['name']}")
            print("🏁 ¡La carrera comienza! / The race begins!")
            
            # Race simulation
            winner = random.choices(horses, weights=[h['chance'] for h in horses])[0]
            
            print(f"🏆 ¡Ganador: {winner['name']}!")
            
            if winner == chosen_horse:
                multiplier = int(chosen_horse['odds'].split(':')[0])
                winnings = bet * multiplier
                self.player.money += winnings
                print(f"{Fore.GREEN}¡Tu caballo ganó! / Your horse won! +${winnings:,}{Style.RESET_ALL}")
                self.player.add_experience(40)
            else:
                self.player.money -= bet
                print(f"{Fore.RED}Perdiste / You lost: -${bet:,}{Style.RESET_ALL}")
                
        except ValueError:
            print("Entrada inválida / Invalid input")

    def cockfighting(self):
        """Cockfighting betting (cultural context)"""
        print(f"\n{Fore.MAGENTA}🐓 PALENQUE TRADICIONAL 🐓{Style.RESET_ALL}")
        print("Apuestas en peleas de gallos tradicionales / Traditional cockfighting bets")
        
        roosters = [
            {"name": "El Guerrero", "strength": random.randint(70, 90)},
            {"name": "Pluma de Oro", "strength": random.randint(60, 85)},
            {"name": "Espolón de Acero", "strength": random.randint(75, 95)},
            {"name": "Rey del Palenque", "strength": random.randint(65, 80)}
        ]
        
        print("Gallos peleadores / Fighting roosters:")
        for i, rooster in enumerate(roosters, 1):
            print(f"{i}. {rooster['name']} - Fuerza estimada: {rooster['strength']}/100")
        
        try:
            rooster_choice = int(input("\nElige gallo / Choose rooster (1-4): ")) - 1
            bet = min(random.randint(300, 800), self.player.money // 4)
            
            if rooster_choice < 0 or rooster_choice >= len(roosters):
                print("Gallo inválido / Invalid rooster")
                return
            
            if self.player.money < bet:
                print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                return
            
            chosen_rooster = roosters[rooster_choice]
            opponent = random.choice([r for r in roosters if r != chosen_rooster])
            
            print(f"\n🥊 Pelea: {chosen_rooster['name']} vs {opponent['name']}")
            print("¡La pelea comienza! / The fight begins!")
            
            # Fight simulation based on strength + luck
            player_score = chosen_rooster['strength'] + random.randint(1, 30)
            opponent_score = opponent['strength'] + random.randint(1, 30)
            
            if player_score > opponent_score:
                winnings = bet * random.randint(2, 4)
                self.player.money += winnings
                print(f"{Fore.GREEN}¡{chosen_rooster['name']} ganó! / {chosen_rooster['name']} won! +${winnings:,}{Style.RESET_ALL}")
                self.player.add_experience(30)
            else:
                self.player.money -= bet
                print(f"{Fore.RED}¡{opponent['name']} ganó! Perdiste -${bet:,}{Style.RESET_ALL}")
                
        except ValueError:
            print("Entrada inválida / Invalid input")

    def sports_betting(self):
        """Sports betting system"""
        print(f"\n{Fore.CYAN}⚽ APUESTAS DEPORTIVAS ⚽{Style.RESET_ALL}")
        
        sports_events = [
            {"sport": "Fútbol", "teams": "Chivas vs América", "odds": "2.5:1"},
            {"sport": "Boxeo", "teams": "Canelo vs Golovkin", "odds": "1.8:1"},
            {"sport": "Baseball", "teams": "Yankees vs Red Sox", "odds": "3:1"},
            {"sport": "UFC", "teams": "Jones vs Cormier", "odds": "2:1"},
            {"sport": "NBA", "teams": "Lakers vs Warriors", "odds": "2.2:1"}
        ]
        
        print("Eventos disponibles / Available events:")
        for i, event in enumerate(sports_events, 1):
            print(f"{i}. {event['sport']}: {event['teams']} - Cuotas: {event['odds']}")
        
        try:
            event_choice = int(input("\nElige evento / Choose event (1-5): ")) - 1
            bet = min(random.randint(100, 600), self.player.money // 3)
            
            if event_choice < 0 or event_choice >= len(sports_events):
                print("Evento inválido / Invalid event")
                return
            
            if self.player.money < bet:
                print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                return
            
            chosen_event = sports_events[event_choice]
            print(f"\nApuesta: ${bet:,} en {chosen_event['teams']}")
            
            # Sports betting outcome
            if random.random() < 0.4:  # 40% win chance
                multiplier = float(chosen_event['odds'].split(':')[0])
                winnings = int(bet * multiplier)
                self.player.money += winnings
                print(f"{Fore.GREEN}¡Ganaste la apuesta! / You won the bet! +${winnings:,}{Style.RESET_ALL}")
                self.player.add_experience(25)
            else:
                self.player.money -= bet
                print(f"{Fore.RED}Perdiste la apuesta / You lost the bet: -${bet:,}{Style.RESET_ALL}")
                
        except ValueError:
            print("Entrada inválida / Invalid input")

    def black_market_menu(self):
        """Black market trading system"""
        self.display_header()
        print(f"{Fore.LIGHTYELLOW_EX}🏴‍☠️ MERCADO NEGRO DE ALBUQUERQUE 🏴‍☠️{Style.RESET_ALL}")
        print(f"{Fore.RED}¡Cuidado! Operaciones ilegales de alto riesgo / Warning! High-risk illegal operations{Style.RESET_ALL}")
        print()
        
        black_market_items = [
            {"name": "Información clasificada del gobierno", "price": 50000, "risk": 4, "exp": 200},
            {"name": "Drogas sintéticas experimentales", "price": 25000, "risk": 3, "exp": 150},
            {"name": "Armas militares", "price": 75000, "risk": 5, "exp": 300},
            {"name": "Documentos falsos premium", "price": 15000, "risk": 2, "exp": 100},
            {"name": "Órganos humanos", "price": 100000, "risk": 5, "exp": 400},
            {"name": "Plutonio enriquecido", "price": 200000, "risk": 5, "exp": 500},
            {"name": "Secretos industriales", "price": 30000, "risk": 3, "exp": 120}
        ]
        
        print(f"💰 Tu dinero: ${self.player.money:,}")
        print(f"⭐ Nivel de respeto: {self.player.respect}")
        print()
        
        print("Artículos disponibles / Available items:")
        for i, item in enumerate(black_market_items, 1):
            risk_stars = "💀" * item['risk']
            print(f"{i}. {item['name']}")
            print(f"   Precio: ${item['price']:,} | Riesgo: {risk_stars} | EXP: +{item['exp']}")
        
        print(f"\n0. {Fore.WHITE}Salir del mercado negro / Exit black market{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿Qué quieres comprar? / What do you want to buy?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(black_market_items):
                item = black_market_items[choice - 1]
                
                if self.player.money < item['price']:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                if self.player.respect < item['risk'] * 500:
                    print(f"{Fore.RED}Tu reputación no es suficiente para esta transacción / Your reputation isn't high enough{Style.RESET_ALL}")
                    return
                
                print(f"\n{Fore.YELLOW}Realizando transacción peligrosa... / Conducting dangerous transaction...{Style.RESET_ALL}")
                
                # Risk calculation
                success_chance = 0.6 + (self.player.skills.get("stealth", 1) * 0.05)
                
                if random.random() < success_chance:
                    self.player.money -= item['price']
                    self.player.add_experience(item['exp'])
                    self.player.respect += item['risk'] * 100
                    
                    # Add to inventory (using quantity system)
                    item_key = item['name'].lower().replace(' ', '_')
                    if item_key not in self.player.inventory:
                        self.player.inventory[item_key] = 1
                    else:
                        self.player.inventory[item_key] += 1
                    
                    print(f"{Fore.GREEN}¡Transacción exitosa! / Successful transaction!{Style.RESET_ALL}")
                    print(f"Adquiriste: {item['name']}")
                    print(f"Experiencia ganada: +{item['exp']}")
                    print(f"Respeto ganado: +{item['risk'] * 100}")
                else:
                    # Failed transaction - police attention
                    self.player.wanted_level = min(5, self.player.wanted_level + item['risk'])
                    print(f"{Fore.RED}¡Transacción fallida! ¡La policía está en alerta! / Transaction failed! Police are alerted!{Style.RESET_ALL}")
                    print(f"Nivel de búsqueda aumentó a: {self.player.wanted_level}")
                    
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def special_missions_menu(self):
        """Special high-stakes missions system"""
        self.display_header()
        print(f"{Fore.LIGHTRED_EX}🎯 MISIONES ESPECIALES DE ALTO RIESGO 🎯{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Misiones únicas con grandes recompensas / Unique missions with high rewards{Style.RESET_ALL}")
        print()
        
        special_missions = [
            {
                "name": "Infiltración en la DEA",
                "description": "Obtén información clasificada del gobierno",
                "reward": 100000,
                "exp": 500,
                "risk": 5,
                "requirements": {"respect": 5000, "stealth": 8}
            },
            {
                "name": "Rescate del Jefe del Cartel",
                "description": "Libera al líder capturado de prisión federal",
                "reward": 200000,
                "exp": 800,
                "risk": 5,
                "requirements": {"respect": 8000, "strength": 7, "shooting": 8}
            },
            {
                "name": "Sabotaje Industrial",
                "description": "Destruye instalaciones de la competencia",
                "reward": 75000,
                "exp": 400,
                "risk": 4,
                "requirements": {"respect": 3000, "hacking": 6}
            },
            {
                "name": "Secuestro VIP",
                "description": "Secuestra a un político importante",
                "reward": 150000,
                "exp": 600,
                "risk": 5,
                "requirements": {"respect": 6000, "charisma": 7, "stealth": 6}
            }
        ]
        
        print(f"💰 Tu dinero: ${self.player.money:,}")
        print(f"⭐ Tu respeto: {self.player.respect}")
        print()
        
        for i, mission in enumerate(special_missions, 1):
            print(f"{i}. {Fore.LIGHTCYAN_EX}{mission['name']}{Style.RESET_ALL}")
            print(f"   {mission['description']}")
            print(f"   Recompensa: ${mission['reward']:,} | EXP: +{mission['exp']} | Riesgo: {'💀' * mission['risk']}")
            
            # Check requirements
            can_do = True
            req_text = "Requisitos: "
            for req, value in mission['requirements'].items():
                if req == "respect":
                    if self.player.respect < value:
                        can_do = False
                        req_text += f"{req}: {value} (Tienes: {self.player.respect}) "
                    else:
                        req_text += f"{req}: {value} ✓ "
                else:
                    if self.player.skills.get(req, 1) < value:
                        can_do = False
                        req_text += f"{req}: {value} (Tienes: {self.player.skills.get(req, 1)}) "
                    else:
                        req_text += f"{req}: {value} ✓ "
            
            color = Fore.GREEN if can_do else Fore.RED
            print(f"   {color}{req_text}{Style.RESET_ALL}")
            print()
        
        print(f"0. {Fore.WHITE}Volver / Back{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿Qué misión aceptas? / Which mission do you accept?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(special_missions):
                mission = special_missions[choice - 1]
                
                # Check if player meets requirements
                can_do = True
                for req, value in mission['requirements'].items():
                    if req == "respect":
                        if self.player.respect < value:
                            can_do = False
                    else:
                        if self.player.skills.get(req, 1) < value:
                            can_do = False
                
                if not can_do:
                    print(f"{Fore.RED}No cumples con los requisitos para esta misión / You don't meet the requirements{Style.RESET_ALL}")
                    return
                
                print(f"\n{Fore.YELLOW}Ejecutando: {mission['name']}...{Style.RESET_ALL}")
                print(mission['description'])
                
                # Mission success calculation
                success_chance = 0.4  # Base 40% chance
                for req, value in mission['requirements'].items():
                    if req == "respect":
                        if self.player.respect > value * 1.5:
                            success_chance += 0.1
                    else:
                        if self.player.skills.get(req, 1) > value:
                            success_chance += 0.1
                
                success_chance = min(0.8, success_chance)  # Max 80% success
                
                if random.random() < success_chance:
                    # Success
                    self.player.money += mission['reward']
                    self.player.add_experience(mission['exp'])
                    self.player.respect += mission['risk'] * 200
                    
                    print(f"{Fore.GREEN}🎉 ¡MISIÓN COMPLETADA! / MISSION COMPLETED! 🎉{Style.RESET_ALL}")
                    print(f"Recompensa: +${mission['reward']:,}")
                    print(f"Experiencia: +{mission['exp']}")
                    print(f"Respeto: +{mission['risk'] * 200}")
                else:
                    # Failure
                    self.player.wanted_level = min(5, self.player.wanted_level + mission['risk'])
                    self.player.respect -= mission['risk'] * 100
                    
                    print(f"{Fore.RED}💥 MISIÓN FALLIDA / MISSION FAILED 💥{Style.RESET_ALL}")
                    print(f"Nivel de búsqueda: +{mission['risk']}")
                    print(f"Respeto perdido: -{mission['risk'] * 100}")
                    
                    # Chance of injury
                    if random.random() < 0.3:
                        health_loss = random.randint(20, 50)
                        self.player.health = max(10, self.player.health - health_loss)
                        print(f"Salud perdida: -{health_loss}")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def empire_building_menu(self):
        """Advanced empire building and management system"""
        self.display_header()
        print(f"{Fore.LIGHTGREEN_EX}🏛️ CONSTRUCCIÓN DE IMPERIO CRIMINAL 🏛️{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Expande tu imperio a través de todo el suroeste / Expand your empire across the Southwest{Style.RESET_ALL}")
        print()
        
        # Initialize empire data if not exists
        if not hasattr(self.player, 'empire'):
            self.player.empire = {
                "territories": [],
                "lieutenants": [],
                "operations": [],
                "influence": 0,
                "daily_income": 0
            }
        
        empire = self.player.empire
        
        print(f"💰 Dinero disponible: ${self.player.money:,}")
        print(f"👑 Influencia total: {empire['influence']}")
        print(f"💵 Ingresos diarios: ${empire['daily_income']:,}")
        print(f"🗺️ Territorios controlados: {len(empire['territories'])}")
        print(f"👥 Lugartenientes: {len(empire['lieutenants'])}")
        print()
        
        print(f"1. {Fore.CYAN}Expandir territorio / Expand territory{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Reclutar lugartenientes / Recruit lieutenants{Style.RESET_ALL}")  
        print(f"3. {Fore.MAGENTA}Establecer operaciones / Establish operations{Style.RESET_ALL}")
        print(f"4. {Fore.GREEN}Recolectar ingresos / Collect income{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Guerra territorial / Territorial war{Style.RESET_ALL}")
        print(f"6. {Fore.BLUE}Ver estado del imperio / View empire status{Style.RESET_ALL}")
        print(f"0. {Fore.WHITE}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige opción / Choose option: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.expand_territory()
        elif choice == "2":
            self.recruit_lieutenants()
        elif choice == "3":
            self.establish_operations()
        elif choice == "4":
            self.collect_empire_income()
        elif choice == "5":
            self.territorial_war()
        elif choice == "6":
            self.view_empire_status()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def expand_territory(self):
        """Expand criminal empire to new territories"""
        print(f"\n{Fore.CYAN}🗺️ EXPANSIÓN TERRITORIAL 🗺️{Style.RESET_ALL}")
        
        available_territories = [
            {"name": "El Paso, Texas", "cost": 50000, "income": 5000, "difficulty": 3},
            {"name": "Phoenix, Arizona", "cost": 75000, "income": 8000, "difficulty": 4},
            {"name": "Denver, Colorado", "cost": 100000, "income": 12000, "difficulty": 5},
            {"name": "Las Vegas, Nevada", "cost": 150000, "income": 20000, "difficulty": 5},
            {"name": "Tijuana, México", "cost": 80000, "income": 15000, "difficulty": 4}
        ]
        
        # Remove already controlled territories
        controlled = [t["name"] for t in self.player.empire["territories"]]
        available = [t for t in available_territories if t["name"] not in controlled]
        
        if not available:
            print(f"{Fore.YELLOW}Ya controlas todos los territorios disponibles / You already control all available territories{Style.RESET_ALL}")
            return
        
        print("Territorios disponibles para expansión / Available territories for expansion:")
        for i, territory in enumerate(available, 1):
            print(f"{i}. {territory['name']}")
            print(f"   Costo: ${territory['cost']:,} | Ingresos: ${territory['income']:,}/día | Dificultad: {'⭐' * territory['difficulty']}")
        
        print("\n0. Cancelar / Cancel")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿Qué territorio quieres conquistar? / Which territory to conquer?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(available):
                territory = available[choice - 1]
                
                if self.player.money < territory['cost']:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                print(f"\n{Fore.YELLOW}Conquistando {territory['name']}...{Style.RESET_ALL}")
                
                # Success based on difficulty and player stats
                success_chance = 0.7 - (territory['difficulty'] * 0.1)
                success_chance += (self.player.skills.get("shooting", 1) * 0.02)
                success_chance += (self.player.skills.get("charisma", 1) * 0.02)
                
                if random.random() < success_chance:
                    self.player.money -= territory['cost']
                    self.player.empire["territories"].append(territory)
                    self.player.empire["daily_income"] += territory['income']
                    self.player.empire["influence"] += territory['difficulty'] * 100
                    
                    print(f"{Fore.GREEN}¡Territorio conquistado! / Territory conquered!{Style.RESET_ALL}")
                    print(f"Nuevos ingresos diarios: +${territory['income']:,}")
                    self.player.add_experience(territory['difficulty'] * 50)
                else:
                    # Failed expansion
                    loss = territory['cost'] // 2
                    self.player.money -= loss
                    self.player.wanted_level = min(5, self.player.wanted_level + 1)
                    
                    print(f"{Fore.RED}¡Conquista fallida! / Conquest failed!{Style.RESET_ALL}")
                    print(f"Perdiste: ${loss:,}")
                    print("Nivel de búsqueda aumentó")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def recruit_lieutenants(self):
        """Recruit and manage criminal lieutenants"""
        print(f"\n{Fore.YELLOW}👥 RECLUTAMIENTO DE LUGARTENIENTES 👥{Style.RESET_ALL}")
        
        available_lieutenants = [
            {"name": "Miguel 'El Sombra'", "specialty": "Stealth", "cost": 25000, "bonus": 10},
            {"name": "Carlos 'Manos de Hierro'", "specialty": "Strength", "cost": 20000, "bonus": 8},
            {"name": "Ana 'La Computadora'", "specialty": "Hacking", "cost": 35000, "bonus": 15},
            {"name": "Roberto 'El Tirador'", "specialty": "Shooting", "cost": 30000, "bonus": 12},
            {"name": "Elena 'La Negociadora'", "specialty": "Charisma", "cost": 28000, "bonus": 11}
        ]
        
        # Remove already recruited
        recruited = [lt["name"] for lt in self.player.empire["lieutenants"]]
        available = [lt for lt in available_lieutenants if lt["name"] not in recruited]
        
        if not available:
            print(f"{Fore.YELLOW}Ya tienes todos los lugartenientes disponibles / You already have all available lieutenants{Style.RESET_ALL}")
            return
        
        print("Lugartenientes disponibles / Available lieutenants:")
        for i, lt in enumerate(available, 1):
            print(f"{i}. {lt['name']} - Especialidad: {lt['specialty']}")
            print(f"   Costo: ${lt['cost']:,} | Bonus de habilidad: +{lt['bonus']}%")
        
        print("\n0. Cancelar / Cancel")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿A quién quieres reclutar? / Who do you want to recruit?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(available):
                lieutenant = available[choice - 1]
                
                if self.player.money < lieutenant['cost']:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                self.player.money -= lieutenant['cost']
                self.player.empire["lieutenants"].append(lieutenant)
                
                print(f"{Fore.GREEN}¡{lieutenant['name']} se ha unido a tu organización!{Style.RESET_ALL}")
                print(f"Bonus en {lieutenant['specialty']}: +{lieutenant['bonus']}%")
                
                self.player.add_experience(100)
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def establish_operations(self):
        """Establish criminal operations in controlled territories"""
        print(f"\n{Fore.MAGENTA}🏭 ESTABLECER OPERACIONES CRIMINALES 🏭{Style.RESET_ALL}")
        
        if not self.player.empire["territories"]:
            print(f"{Fore.RED}Necesitas controlar territorios primero / You need to control territories first{Style.RESET_ALL}")
            return
        
        operation_types = [
            {"name": "Laboratorio de Drogas", "cost": 40000, "daily_income": 3000, "risk": 3},
            {"name": "Red de Contrabando", "cost": 60000, "daily_income": 5000, "risk": 4},
            {"name": "Casino Clandestino", "cost": 80000, "daily_income": 8000, "risk": 2},
            {"name": "Taller de Falsificación", "cost": 35000, "daily_income": 2500, "risk": 2},
            {"name": "Red de Trata", "cost": 100000, "daily_income": 12000, "risk": 5}
        ]
        
        print("Tipos de operaciones / Operation types:")
        for i, op in enumerate(operation_types, 1):
            print(f"{i}. {op['name']}")
            print(f"   Costo: ${op['cost']:,} | Ingresos: ${op['daily_income']:,}/día | Riesgo: {'⚠️' * op['risk']}")
        
        print("\n0. Cancelar / Cancel")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿Qué operación quieres establecer? / Which operation to establish?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(operation_types):
                operation = operation_types[choice - 1].copy()
                
                if self.player.money < operation['cost']:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                # Choose territory
                print("\nTeritorios disponibles / Available territories:")
                for i, territory in enumerate(self.player.empire["territories"], 1):
                    print(f"{i}. {territory['name']}")
                
                territory_choice = int(input("¿En qué territorio? / In which territory?: ")) - 1
                
                if 0 <= territory_choice < len(self.player.empire["territories"]):
                    territory = self.player.empire["territories"][territory_choice]
                    operation["territory"] = territory["name"]
                    
                    self.player.money -= operation['cost']
                    self.player.empire["operations"].append(operation)
                    self.player.empire["daily_income"] += operation['daily_income']
                    
                    print(f"{Fore.GREEN}¡Operación establecida en {territory['name']}!{Style.RESET_ALL}")
                    print(f"Nuevos ingresos diarios: +${operation['daily_income']:,}")
                    
                    self.player.add_experience(operation['cost'] // 1000)
                else:
                    print(f"{Fore.RED}Territorio inválido / Invalid territory{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def collect_empire_income(self):
        """Collect daily income from empire operations"""
        print(f"\n{Fore.GREEN}💰 RECOLECCIÓN DE INGRESOS 💰{Style.RESET_ALL}")
        
        if self.player.empire["daily_income"] <= 0:
            print(f"{Fore.YELLOW}No tienes ingresos diarios configurados / No daily income set up{Style.RESET_ALL}")
            return
        
        # Calculate actual income (can be affected by various factors)
        base_income = self.player.empire["daily_income"]
        
        # Lieutenant bonuses
        business_bonus = 0
        for lt in self.player.empire["lieutenants"]:
            if lt["specialty"] == "Business":
                business_bonus += lt["bonus"]
        
        # Wanted level penalty
        wanted_penalty = self.player.wanted_level * 0.1
        
        final_income = int(base_income * (1 + business_bonus/100) * (1 - wanted_penalty))
        
        print(f"Ingresos base: ${base_income:,}")
        if business_bonus > 0:
            print(f"Bonus de lugartenientes: +{business_bonus}%")
        if wanted_penalty > 0:
            print(f"Penalización por búsqueda: -{wanted_penalty*100}%")
        
        print(f"\n{Fore.GREEN}Ingresos totales recolectados: ${final_income:,}{Style.RESET_ALL}")
        
        self.player.money += final_income
        
        # Random events during collection
        if random.random() < 0.1:
            event_type = random.choice(["raid", "bonus", "competitor"])
            
            if event_type == "raid":
                loss = final_income // 3
                self.player.money -= loss
                print(f"\n{Fore.RED}¡Redada policial! Perdiste ${loss:,}{Style.RESET_ALL}")
                self.player.wanted_level = min(5, self.player.wanted_level + 1)
            elif event_type == "bonus":
                bonus = final_income // 2
                self.player.money += bonus
                print(f"\n{Fore.YELLOW}¡Operación especial exitosa! Bonus: +${bonus:,}{Style.RESET_ALL}")
            elif event_type == "competitor":
                print(f"\n{Fore.CYAN}Un competidor quiere hacer un trato...{Style.RESET_ALL}")
                if input("¿Aceptas negociar? (s/n): ").lower() == 's':
                    if random.random() < 0.6:
                        bonus = random.randint(10000, 50000)
                        self.player.money += bonus
                        print(f"{Fore.GREEN}¡Negociación exitosa! +${bonus:,}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}¡Era una trampa! Te atacan...{Style.RESET_ALL}")
                        self.player.health -= random.randint(10, 30)

    def territorial_war(self):
        """Engage in territorial warfare"""
        print(f"\n{Fore.RED}⚔️ GUERRA TERRITORIAL ⚔️{Style.RESET_ALL}")
        print("Declara la guerra a organizaciones rivales para expandir tu dominio")
        
        rival_organizations = [
            {"name": "Cartel de Sinaloa", "strength": 80, "territories": 3, "reward": 100000},
            {"name": "Los Zetas", "strength": 90, "territories": 4, "reward": 150000},
            {"name": "Cartel del Golfo", "strength": 75, "territories": 2, "reward": 80000},
            {"name": "Familia Michoacana", "strength": 70, "territories": 3, "reward": 120000}
        ]
        
        print("Organizaciones rivales / Rival organizations:")
        for i, org in enumerate(rival_organizations, 1):
            print(f"{i}. {org['name']}")
            print(f"   Fuerza: {org['strength']}/100 | Territorios: {org['territories']} | Recompensa: ${org['reward']:,}")
        
        print("\n0. Cancelar / Cancel")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿A quién quieres atacar? / Who do you want to attack?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(rival_organizations):
                rival = rival_organizations[choice - 1]
                
                print(f"\n{Fore.RED}🔥 INICIANDO GUERRA CONTRA {rival['name'].upper()} 🔥{Style.RESET_ALL}")
                
                # Calculate player strength
                player_strength = 50  # Base strength
                player_strength += self.player.skills.get("shooting", 1) * 3
                player_strength += self.player.skills.get("strength", 1) * 2
                player_strength += len(self.player.empire["lieutenants"]) * 5
                player_strength += len(self.player.empire["territories"]) * 3
                
                print(f"Tu fuerza: {player_strength}/100")
                print(f"Fuerza rival: {rival['strength']}/100")
                
                # War simulation
                if player_strength > rival['strength']:
                    win_chance = 0.7
                elif player_strength == rival['strength']:
                    win_chance = 0.5
                else:
                    win_chance = 0.3
                
                print(f"\n{Fore.YELLOW}¡La guerra comienza!{Style.RESET_ALL}")
                print("Desplegando fuerzas...")
                print("Combate en progreso...")
                
                if random.random() < win_chance:
                    # Victory
                    self.player.money += rival['reward']
                    self.player.empire["influence"] += rival['territories'] * 200
                    self.player.respect += rival['strength'] * 10
                    
                    print(f"\n{Fore.GREEN}🏆 ¡VICTORIA! 🏆{Style.RESET_ALL}")
                    print(f"Has derrotado a {rival['name']}")
                    print(f"Recompensa: +${rival['reward']:,}")
                    print(f"Influencia: +{rival['territories'] * 200}")
                    print(f"Respeto: +{rival['strength'] * 10}")
                    
                    self.player.add_experience(rival['strength'] * 5)
                else:
                    # Defeat
                    loss = min(self.player.money // 3, rival['reward'] // 2)
                    self.player.money -= loss
                    self.player.health -= random.randint(20, 40)
                    self.player.respect -= rival['strength'] * 5
                    
                    print(f"\n{Fore.RED}💀 DERROTA 💀{Style.RESET_ALL}")  
                    print(f"Has sido derrotado por {rival['name']}")
                    print(f"Pérdidas: -${loss:,}")
                    print(f"Salud perdida: -{40}")
                    print(f"Respeto perdido: -{rival['strength'] * 5}")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def view_empire_status(self):
        """View detailed empire status and statistics"""
        print(f"\n{Fore.BLUE}📊 ESTADO DEL IMPERIO 📊{Style.RESET_ALL}")
        empire = self.player.empire
        
        print(f"👑 {Fore.YELLOW}INFORMACIÓN GENERAL{Style.RESET_ALL}")
        print(f"Influencia total: {empire['influence']}")
        print(f"Ingresos diarios: ${empire['daily_income']:,}")
        print(f"Territorios controlados: {len(empire['territories'])}")
        print(f"Lugartenientes reclutados: {len(empire['lieutenants'])}")
        print(f"Operaciones activas: {len(empire['operations'])}")
        
        if empire['territories']:
            print(f"\n🗺️ {Fore.CYAN}TERRITORIOS CONTROLADOS{Style.RESET_ALL}")
            for territory in empire['territories']:
                print(f"• {territory['name']} - Ingresos: ${territory['income']:,}/día")
        
        if empire['lieutenants']:
            print(f"\n👥 {Fore.YELLOW}LUGARTENIENTES{Style.RESET_ALL}")
            for lt in empire['lieutenants']:
                print(f"• {lt['name']} - {lt['specialty']} (+{lt['bonus']}%)")
        
        if empire['operations']:
            print(f"\n🏭 {Fore.MAGENTA}OPERACIONES ACTIVAS{Style.RESET_ALL}")
            for op in empire['operations']:
                print(f"• {op['name']} en {op['territory']} - ${op['daily_income']:,}/día")

    def private_investigation_menu(self):
        """Private investigation and intelligence gathering"""
        self.display_header()
        print(f"{Fore.LIGHTBLUE_EX}🔍 INVESTIGACIÓN PRIVADA 🔍{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Servicios de espionaje e inteligencia / Espionage and intelligence services{Style.RESET_ALL}")
        print()
        
        print(f"1. {Fore.CYAN}Investigar rivales / Investigate rivals{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Espionaje industrial / Industrial espionage{Style.RESET_ALL}")
        print(f"3. {Fore.MAGENTA}Chantaje y extorsión / Blackmail and extortion{Style.RESET_ALL}")
        print(f"4. {Fore.GREEN}Información del mercado / Market intelligence{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Eliminar evidencia / Eliminate evidence{Style.RESET_ALL}")
        print(f"0. {Fore.WHITE}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige servicio / Choose service: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.investigate_rivals()
        elif choice == "2":
            self.industrial_espionage()
        elif choice == "3":
            self.blackmail_extortion()
        elif choice == "4":
            self.market_intelligence()
        elif choice == "5":
            self.eliminate_evidence()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def investigate_rivals(self):
        """Investigate rival criminal organizations"""
        print(f"\n{Fore.CYAN}🎯 INVESTIGACIÓN DE RIVALES 🎯{Style.RESET_ALL}")
        
        investigation_targets = [
            {"name": "Los Hermanos García", "cost": 5000, "info_value": 2000, "risk": 2},
            {"name": "Cartel del Norte", "cost": 15000, "info_value": 8000, "risk": 4},
            {"name": "Organización Phantom", "cost": 25000, "info_value": 15000, "risk": 5},
            {"name": "Red de Corrupción Política", "cost": 40000, "info_value": 30000, "risk": 5}
        ]
        
        print("Objetivos de investigación / Investigation targets:")
        for i, target in enumerate(investigation_targets, 1):
            print(f"{i}. {target['name']}")
            print(f"   Costo: ${target['cost']:,} | Valor de información: ${target['info_value']:,} | Riesgo: {'⚠️' * target['risk']}")
        
        print("\n0. Cancelar / Cancel")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿A quién investigar? / Who to investigate?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(investigation_targets):
                target = investigation_targets[choice - 1]
                
                if self.player.money < target['cost']:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                print(f"\n{Fore.YELLOW}Investigando {target['name']}...{Style.RESET_ALL}")
                
                # Success chance based on stealth and hacking skills
                success_chance = 0.6 + (self.player.skills.get("stealth", 1) * 0.03) + (self.player.skills.get("hacking", 1) * 0.02)
                success_chance = min(0.9, success_chance)
                
                self.player.money -= target['cost']
                
                if random.random() < success_chance:
                    # Successful investigation
                    self.player.money += target['info_value']
                    self.player.add_experience(target['risk'] * 20)
                    
                    print(f"{Fore.GREEN}¡Investigación exitosa! / Successful investigation!{Style.RESET_ALL}")
                    print(f"Información valiosa obtenida: +${target['info_value']:,}")
                    
                    # Additional benefits
                    info_types = ["Rutas de contrabando", "Contactos corruptos", "Planes futuros", "Puntos débiles", "Ubicaciones secretas"]
                    discovered_info = random.choice(info_types)
                    print(f"Información descubierta: {discovered_info}")
                    
                    if discovered_info in ["Contactos corruptos", "Puntos débiles"]:
                        self.player.respect += target['risk'] * 50
                        print(f"Respeto ganado: +{target['risk'] * 50}")
                        
                else:
                    # Failed investigation
                    print(f"{Fore.RED}¡Investigación detectada! / Investigation detected!{Style.RESET_ALL}")
                    self.player.wanted_level = min(5, self.player.wanted_level + target['risk'] - 1)
                    print("Nivel de búsqueda aumentó")
                    
                    # Chance of retaliation
                    if random.random() < 0.3:
                        damage = random.randint(10, 30)
                        self.player.health -= damage
                        print(f"Represalias enemigas: -{damage} salud")
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def international_smuggling_menu(self):
        """International smuggling operations"""
        self.display_header()
        print(f"{Fore.LIGHTCYAN_EX}🌍 CONTRABANDO INTERNACIONAL 🌍{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Operaciones de contrabando a gran escala / Large-scale smuggling operations{Style.RESET_ALL}")
        print()
        
        print(f"1. {Fore.CYAN}Contrabando México-USA / Mexico-USA smuggling{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Tráfico de armas / Arms trafficking{Style.RESET_ALL}")
        print(f"3. {Fore.MAGENTA}Contrabando de personas / Human trafficking{Style.RESET_ALL}")
        print(f"4. {Fore.GREEN}Lavado de dinero offshore / Offshore money laundering{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Contrabando de órganos / Organ trafficking{Style.RESET_ALL}")
        print(f"0. {Fore.WHITE}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}Elige operación / Choose operation: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            self.mexico_usa_smuggling()
        elif choice == "2":
            self.arms_trafficking()
        elif choice == "3":
            self.human_trafficking()
        elif choice == "4":
            self.offshore_laundering()
        elif choice == "5":
            self.organ_trafficking()
        elif choice == "0":
            return
        else:
            print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

    def criminal_academy_menu(self):
        """Criminal training academy system"""
        self.display_header()
        print(f"{Fore.WHITE}🎓 ACADEMIA CRIMINAL DE NUEVO MÉXICO 🎓{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Entrena y mejora tus habilidades criminales / Train and improve your criminal skills{Style.RESET_ALL}")
        print()
        
        print(f"💰 Tu dinero: ${self.player.money:,}")
        print(f"📊 Puntos de habilidad disponibles: {self.player.skill_points}")
        print()
        
        training_courses = [
            {"name": "Curso de Tiro Avanzado", "skill": "shooting", "cost": 10000, "improvement": 2, "duration": "3 días"},
            {"name": "Entrenamiento de Sigilo", "skill": "stealth", "cost": 8000, "improvement": 2, "duration": "2 días"},
            {"name": "Academia de Hacking", "skill": "hacking", "cost": 15000, "improvement": 3, "duration": "5 días"},
            {"name": "Escuela de Negocios Criminales", "skill": "business", "cost": 12000, "improvement": 2, "duration": "4 días"},
            {"name": "Gimnasio de Combate", "skill": "strength", "cost": 6000, "improvement": 1, "duration": "1 día"},
            {"name": "Curso de Liderazgo Criminal", "skill": "charisma", "cost": 20000, "improvement": 3, "duration": "1 semana"},
            {"name": "Entrenamiento de Conducción Extrema", "skill": "driving", "cost": 9000, "improvement": 2, "duration": "2 días"},
            {"name": "Seminario de Intimidación", "skill": "intimidation", "cost": 7000, "improvement": 1, "duration": "1 día"}
        ]
        
        print("Cursos disponibles / Available courses:")
        for i, course in enumerate(training_courses, 1):
            current_level = self.player.skills.get(course["skill"], 1)
            max_level = 10
            
            if current_level >= max_level:
                status = f"{Fore.RED}(Máximo alcanzado){Style.RESET_ALL}"
            elif self.player.money >= course["cost"]:
                status = f"{Fore.GREEN}(Disponible){Style.RESET_ALL}"
            else:
                status = f"{Fore.YELLOW}(Sin dinero suficiente){Style.RESET_ALL}"
            
            print(f"{i}. {course['name']} {status}")
            print(f"   Habilidad: {course['skill'].capitalize()} (Actual: {current_level}/10)")
            print(f"   Costo: ${course['cost']:,} | Mejora: +{course['improvement']} | Duración: {course['duration']}")
            print()
        
        print(f"0. {Fore.WHITE}Salir de la academia / Exit academy{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.CYAN}¿Qué curso quieres tomar? / Which course do you want to take?: {Style.RESET_ALL}"))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(training_courses):
                course = training_courses[choice - 1]
                skill = course["skill"]
                current_level = self.player.skills.get(skill, 1)
                
                if current_level >= 10:
                    print(f"{Fore.RED}Ya tienes el nivel máximo en {skill} / You already have maximum level in {skill}{Style.RESET_ALL}")
                    return
                
                if self.player.money < course["cost"]:
                    print(f"{Fore.RED}No tienes suficiente dinero / Not enough money{Style.RESET_ALL}")
                    return
                
                print(f"\n{Fore.YELLOW}Inscribiéndote en: {course['name']}...{Style.RESET_ALL}")
                print(f"Duración del curso: {course['duration']}")
                print("Entrenando...")
                
                # Training simulation
                self.player.money -= course["cost"]
                
                # Success chance based on current level (harder to improve at higher levels)
                success_chance = 0.9 - (current_level * 0.05)
                
                if random.random() < success_chance:
                    # Successful training
                    improvement = min(course["improvement"], 10 - current_level)
                    self.player.skills[skill] = current_level + improvement
                    
                    print(f"\n{Fore.GREEN}¡Entrenamiento completado exitosamente!{Style.RESET_ALL}")
                    print(f"{skill.capitalize()} mejorado: {current_level} → {self.player.skills[skill]}")
                    
                    # Bonus experience
                    exp_gain = course["cost"] // 100
                    self.player.add_experience(exp_gain)
                    print(f"Experiencia ganada: +{exp_gain}")
                    
                    # Special bonuses for certain skills
                    if skill == "shooting" and self.player.skills[skill] >= 8:
                        print(f"{Fore.CYAN}¡Desbloqueaste nuevas armas en el mercado negro!{Style.RESET_ALL}")
                    elif skill == "hacking" and self.player.skills[skill] >= 7:
                        print(f"{Fore.CYAN}¡Ahora puedes hackear sistemas gubernamentales!{Style.RESET_ALL}")
                    elif skill == "charisma" and self.player.skills[skill] >= 9:
                        print(f"{Fore.CYAN}¡Puedes sobornar a oficiales de alto rango!{Style.RESET_ALL}")
                        
                else:
                    # Failed training
                    refund = course["cost"] // 2
                    self.player.money += refund
                    
                    print(f"\n{Fore.RED}El entrenamiento no fue exitoso / Training was not successful{Style.RESET_ALL}")
                    print(f"Reembolso parcial: ${refund:,}")
                    
                    # Still gain some experience
                    exp_gain = course["cost"] // 200
                    self.player.add_experience(exp_gain)
            else:
                print(f"{Fore.RED}Opción inválida / Invalid choice{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Entrada inválida / Invalid input{Style.RESET_ALL}")

    def industrial_espionage(self):
        """Industrial espionage operations"""
        print(f"\n{Fore.YELLOW}🏭 ESPIONAJE INDUSTRIAL 🏭{Style.RESET_ALL}")
        targets = [
            {"name": "Petrolera Estatal", "reward": 25000, "risk": 3},
            {"name": "Empresa Tecnológica", "reward": 40000, "risk": 4}
        ]
        
        for i, target in enumerate(targets, 1):
            print(f"{i}. {target['name']} - ${target['reward']:,}")
        
        try:
            choice = int(input("\nObjetivo: ")) - 1
            if 0 <= choice < len(targets):
                target = targets[choice]
                if random.random() < 0.6:
                    self.player.money += target['reward']
                    print(f"{Fore.GREEN}Éxito: +${target['reward']:,}{Style.RESET_ALL}")
        except ValueError:
            pass

    def blackmail_extortion(self):
        """Blackmail operations"""
        print(f"\n{Fore.RED}💰 CHANTAJE 💰{Style.RESET_ALL}")
        targets = [{"name": "Político corrupto", "payment": 15000}]
        
        for i, target in enumerate(targets, 1):
            print(f"{i}. {target['name']} - ${target['payment']:,}")
        
        try:
            choice = int(input("\nVíctima: ")) - 1
            if 0 <= choice < len(targets):
                self.player.money += targets[choice]['payment']
                print(f"{Fore.GREEN}Cobrado{Style.RESET_ALL}")
        except ValueError:
            pass

    def market_intelligence(self):
        """Market intelligence"""
        print(f"\n{Fore.BLUE}📊 INTELIGENCIA DE MERCADO 📊{Style.RESET_ALL}")
        self.player.money += 10000
        print(f"{Fore.GREEN}Información vendida: +$10,000{Style.RESET_ALL}")

    def eliminate_evidence(self):
        """Evidence elimination"""
        print(f"\n{Fore.RED}🔥 ELIMINACIÓN DE EVIDENCIA 🔥{Style.RESET_ALL}")
        if self.player.wanted_level > 0:
            cost = self.player.wanted_level * 10000
            if self.player.money >= cost:
                self.player.money -= cost
                self.player.wanted_level = max(0, self.player.wanted_level - 1)
                print(f"{Fore.GREEN}Evidencia eliminada{Style.RESET_ALL}")

    def mexico_usa_smuggling(self):
        """Mexico-USA smuggling"""
        print(f"\n{Fore.CYAN}🌎 CONTRABANDO MÉXICO-USA 🌎{Style.RESET_ALL}")
        if random.random() < 0.7:
            profit = random.randint(50000, 150000)
            self.player.money += profit
            print(f"{Fore.GREEN}Éxito: +${profit:,}{Style.RESET_ALL}")
        else:
            self.player.wanted_level += 2
            print(f"{Fore.RED}Interceptado{Style.RESET_ALL}")

    def arms_trafficking(self):
        """Arms trafficking"""
        print(f"\n{Fore.RED}🔫 TRÁFICO DE ARMAS 🔫{Style.RESET_ALL}")
        if random.random() < 0.6:
            profit = random.randint(30000, 80000)
            self.player.money += profit
            print(f"{Fore.GREEN}Venta exitosa: +${profit:,}{Style.RESET_ALL}")

    def human_trafficking(self):
        """Human trafficking (dark content)"""
        print(f"\n{Fore.RED}⚠️ OPERACIÓN DE ALTO RIESGO ⚠️{Style.RESET_ALL}")
        if random.random() < 0.4:
            self.player.money += 75000
            print(f"{Fore.GREEN}Operación completada{Style.RESET_ALL}")
        else:
            self.player.wanted_level = 5
            print(f"{Fore.RED}Operación descubierta{Style.RESET_ALL}")

    def offshore_laundering(self):
        """Offshore money laundering"""
        print(f"\n{Fore.GREEN}🏦 LAVADO OFFSHORE 🏦{Style.RESET_ALL}")
        if self.player.money >= 50000:
            amount = min(100000, self.player.money // 2)
            fee = int(amount * 0.15)
            self.player.money -= fee
            print(f"{Fore.GREEN}Dinero lavado (Comisión: ${fee:,}){Style.RESET_ALL}")

    def organ_trafficking(self):
        """Organ trafficking (extreme content)"""
        print(f"\n{Fore.RED}💀 OPERACIÓN EXTREMA 💀{Style.RESET_ALL}")
        if random.random() < 0.3:
            self.player.money += 100000
            print(f"{Fore.GREEN}Operación completada{Style.RESET_ALL}")
        else:
            self.player.wanted_level = 5
            self.player.health -= 20
            print(f"{Fore.RED}Operación fallida{Style.RESET_ALL}")

def main():
    """Main entry point"""
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    if os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1":
        main()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit(0)
