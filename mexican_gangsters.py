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
        "description": "Base militar con acceso a armas y tecnología avanzada",
        "english_desc": "Military base with access to weapons and advanced technology",
        "districts": ["Centro", "North Plains", "Curry County", "Airport District", "Military Base", "Tech Park"],
        "danger_level": 4,
        "cartel_presence": "Comandos del Aire",
        "specialties": ["military_weapons_theft", "air_force_corruption", "tech_smuggling"],
        "police_stations": 2,
        "hospitals": 1,
        "airports": 1,
        "major_highways": ["US-60", "US-84"],
        "population": 39000
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
        
        # Additional attributes for new features
        self.heat_level = 0
        self.prison_time = 0
        self.prison_contacts = []
        self.story_progress = 0

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
            print(f"15. {Fore.RED}Salir del juego / Quit game{Style.RESET_ALL}")
            print()
            
            choice = input(f"{Fore.CYAN}Elige tu opción / Enter your choice (1-15): {Style.RESET_ALL}").strip()
            
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
                self.story_missions()
            elif choice == "11":
                self.multiple_save_system()
            elif choice == "12":
                self.gang_hierarchy_system()
            elif choice == "13":
                self.character_status()
            elif choice == "14":
                self.allocate_skill_points()
            elif choice == "15":
                self.change_language()
            elif choice == "16":
                self.quit_game()
            
            # Auto police encounter check for 3+ wanted level after any action
            if self.player.wanted_level >= 3 and choice not in ["13", "14", "15", "16"]:
                self.police_encounter()
            else:
                print(f"{Fore.RED}{self.get_text('Opción inválida', 'Invalid choice')}. {self.get_text('Presiona Enter para continuar', 'Press Enter to continue')}...{Style.RESET_ALL}")
                input()

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
            self.nothing_happens
        ]
        
        # Weight the encounters based on wanted level and location danger
        weights = [20, 15, self.player.wanted_level * 10, 25, 20, 30]
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
            if self.player.vehicle:
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
            vehicle_info = VEHICLES[self.player.vehicle]
            print(f"Current Vehicle: {vehicle_info['name']}")
            print(f"Speed: {'★' * vehicle_info['speed']}")
            print(f"Reliability: {vehicle_info['reliability']}%")
            print(f"Value: ${vehicle_info['value']:,}")
            print()
            
            print(f"1. {Fore.GREEN}Sell vehicle{Style.RESET_ALL}")
            print(f"2. {Fore.YELLOW}Abandon vehicle{Style.RESET_ALL}")
            print(f"3. {Fore.CYAN}Back{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}Enter choice: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                sell_price = vehicle_info['value'] // 2
                self.player.add_money(sell_price)
                vehicle_name = vehicle_info['name']
                self.player.vehicle = None
                print(f"{Fore.GREEN}Sold {vehicle_name} for ${sell_price}.{Style.RESET_ALL}")
            elif choice == "2":
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
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Money: ${self.player.money:,}")
        print(f"Respect: {self.player.respect}")
        print(f"Wanted Level: {'★' * self.player.wanted_level}{'☆' * (5 - self.player.wanted_level)}")
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
        if self.player.vehicle:
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
                vehicle_speed = VEHICLES[self.player.vehicle]["speed"]
                escape_chance = 30 + (vehicle_speed * 15) + (self.player.skills["driving"] * 5)
                
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
                    "skills": self.player.skills
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

    def allocate_skill_points(self):
        """Allocate skill points to improve character abilities"""
        self.display_header()
        print(f"{Fore.LIGHTBLUE_EX}Asignación de Puntos de Habilidad / Skill Point Allocation{Style.RESET_ALL}")
        print()
        
        if self.player.skill_points <= 0:
            print(f"{Fore.YELLOW}No tienes puntos de habilidad disponibles / No skill points available.{Style.RESET_ALL}")
            print("Gana experiencia completando misiones para obtener más puntos.")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"Puntos disponibles / Available points: {Fore.GREEN}{self.player.skill_points}{Style.RESET_ALL}")
        print(f"Nivel actual / Current level: {self.player.level}")
        print(f"Experiencia / Experience: {self.player.experience}/{self.player.experience_to_next}")
        print()
        
        print(f"{Fore.CYAN}Habilidades actuales / Current skills:{Style.RESET_ALL}")
        skills_spanish = {
            "shooting": "Tiro / Shooting",
            "driving": "Conducción / Driving", 
            "stealth": "Sigilo / Stealth",
            "charisma": "Carisma / Charisma",
            "strength": "Fuerza / Strength"
        }
        
        for i, (skill, level) in enumerate(self.player.skills.items(), 1):
            stars = "★" * level + "☆" * (10 - level)
            print(f"{i}. {skills_spanish[skill]}: {stars} ({level}/10)")
        
        print(f"6. {Fore.CYAN}Volver / Back{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.CYAN}¿Qué habilidad mejorar? / Which skill to improve?: {Style.RESET_ALL}").strip()
        
        try:
            choice_num = int(choice)
            skill_names = list(self.player.skills.keys())
            
            if 1 <= choice_num <= 5:
                skill_name = skill_names[choice_num - 1]
                if self.player.skills[skill_name] >= 10:
                    print(f"{Fore.RED}Esta habilidad ya está al máximo / This skill is already maxed out.{Style.RESET_ALL}")
                else:
                    self.player.skills[skill_name] += 1
                    self.player.skill_points -= 1
                    
                    improvement_messages = [
                        f"¡Habilidad de {skills_spanish[skill_name].split(' / ')[0]} mejorada!",
                        f"Te sientes más hábil en {skills_spanish[skill_name].split(' / ')[0]}.",
                        f"Tu entrenamiento en {skills_spanish[skill_name].split(' / ')[0]} da frutos."
                    ]
                    
                    print(f"{Fore.GREEN}{random.choice(improvement_messages)}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{skills_spanish[skill_name]} improved to {self.player.skills[skill_name]}/10!{Style.RESET_ALL}")
                    
                    if self.player.skill_points > 0:
                        if input("\n¿Mejorar otra habilidad? / Improve another skill? (s/y or n): ").lower() in ['s', 'y']:
                            self.allocate_skill_points()
            elif choice_num == 6:
                return
        except ValueError:
            print(f"{Fore.RED}Opción inválida / Invalid choice.{Style.RESET_ALL}")
        
        input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

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
        
        if self.player.vehicle:
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
