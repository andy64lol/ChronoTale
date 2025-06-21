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
        WHITE="", LIGHTRED_EX="", LIGHTGREEN_EX="", LIGHTBLUE_EX=""
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
        "districts": ["Ciudad Vieja", "Centro", "Lado Oeste", "Alturas del Noreste", "Las Colinas"],
        "danger_level": 3,
        "cartel_presence": "Los Hermanos del Desierto",
        "specialties": ["drug_labs", "money_laundering", "weapons_trafficking"]
    },
    "Santa Fe": {
        "description": "La capital con rica historia y blancos adinerados, pero vigilancia pesada",
        "english_desc": "The capital city with rich history and wealthy targets, but heavy surveillance",
        "districts": ["La Plaza", "Camino del Cañón", "Distrito Ferroviario", "Centro", "Lado Este"],
        "danger_level": 2,
        "cartel_presence": "Cartel de la Corona",
        "specialties": ["art_theft", "political_corruption", "high_society_cons"]
    },
    "Las Cruces": {
        "description": "Ciudad fronteriza con oportunidades de contrabando y fuerte presencia del cartel",
        "english_desc": "Border town with smuggling opportunities and strong cartel presence",
        "districts": ["Valle de Mesilla", "Mesa del Este", "Rancho Sonoma", "Cerros Picacho", "Centro"],
        "danger_level": 4,
        "cartel_presence": "Cártel de la Frontera Sur",
        "specialties": ["human_trafficking", "border_smuggling", "cartel_wars"]
    },
    "Roswell": {
        "description": "Pequeña ciudad del desierto con secretos militares y blancos fáciles",
        "english_desc": "Small desert town with military secrets and easy targets",
        "districts": ["Centro", "Alturas Militares", "Del Norte", "Club de Campo", "Main Sur"],
        "danger_level": 1,
        "cartel_presence": "Pandilla de los Extraterrestres",
        "specialties": ["alien_conspiracy", "military_theft", "rural_meth"]
    }
}

VEHICLES = {
    "stolen_car": {"name": "Stolen Car", "speed": 2, "reliability": 60, "value": 500},
    "motorcycle": {"name": "Motorcycle", "speed": 4, "reliability": 70, "value": 1200},
    "pickup_truck": {"name": "Pickup Truck", "speed": 1, "reliability": 90, "value": 800},
    "sports_car": {"name": "Sports Car", "speed": 5, "reliability": 80, "value": 3000},
    "suv": {"name": "SUV", "speed": 2, "reliability": 85, "value": 2200},
    "lowrider": {"name": "Lowrider", "speed": 2, "reliability": 75, "value": 1800}
}

WEAPONS = {
    "fists": {"name": "Puños / Fists", "damage": 10, "price": 0, "ammo": None, "spanish": "Puños"},
    "knife": {"name": "Navaja / Knife", "damage": 25, "price": 50, "ammo": None, "spanish": "Navaja"},
    "machete": {"name": "Machete", "damage": 35, "price": 120, "ammo": None, "spanish": "Machete"},
    "pistol": {"name": "Pistola / Pistol", "damage": 40, "price": 300, "ammo": "9mm", "spanish": "Pistola"},
    "revolver": {"name": "Revólver / Revolver", "damage": 50, "price": 450, "ammo": "357", "spanish": "Revólver"},
    "desert_eagle": {"name": "Desert Eagle", "damage": 65, "price": 800, "ammo": "50cal", "spanish": "Águila del Desierto"},
    "shotgun": {"name": "Escopeta / Shotgun", "damage": 80, "price": 600, "ammo": "shells", "spanish": "Escopeta"},
    "sawed_off": {"name": "Escopeta Recortada / Sawed-off", "damage": 90, "price": 750, "ammo": "shells", "spanish": "Recortada"},
    "rifle": {"name": "Rifle de Asalto / Assault Rifle", "damage": 60, "price": 1500, "ammo": "556", "spanish": "Rifle"},
    "ak47": {"name": "AK-47 Cuerno de Chivo", "damage": 70, "price": 2000, "ammo": "762", "spanish": "Cuerno de Chivo"},
    "smg": {"name": "Metralleta / SMG", "damage": 45, "price": 800, "ammo": "9mm", "spanish": "Metralleta"},
    "uzi": {"name": "Uzi", "damage": 50, "price": 1200, "ammo": "9mm", "spanish": "Uzi"},
    "sniper": {"name": "Rifle de Francotirador / Sniper", "damage": 120, "price": 3500, "ammo": "762", "spanish": "Francotirador"},
    "rpg": {"name": "RPG Lanzacohetes", "damage": 200, "price": 8000, "ammo": "rockets", "spanish": "Lanzacohetes"},
    "grenade": {"name": "Granada / Grenade", "damage": 150, "price": 500, "ammo": None, "spanish": "Granada"}
}

DRUGS = {
    "mota": {"name": "Mota (Marijuana)", "spanish": "Mota", "buy_price": 10, "sell_price": 15, "risk": 1, "origin": "Local farms"},
    "coca": {"name": "Coca (Cocaine)", "spanish": "Coca", "buy_price": 50, "sell_price": 80, "risk": 3, "origin": "Colombian cartels"},
    "cristal": {"name": "Cristal (Methamphetamine)", "spanish": "Cristal", "buy_price": 30, "sell_price": 50, "risk": 2, "origin": "Desert labs"},
    "chiva": {"name": "Chiva (Heroin)", "spanish": "Chiva", "buy_price": 80, "sell_price": 120, "risk": 4, "origin": "Afghan suppliers"},
    "fentanilo": {"name": "Fentanilo (Fentanyl)", "spanish": "Fentanilo", "buy_price": 100, "sell_price": 180, "risk": 5, "origin": "Chinese precursors"}
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
        self.ammo = {"9mm": 0, "shells": 0, "556": 0, "357": 0, "50cal": 0, "762": 0, "rockets": 0}
        self.drugs = {"mota": 0, "coca": 0, "cristal": 0, "chiva": 0, "fentanilo": 0}
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
        self.skills = {
            "shooting": 1,
            "driving": 1,
            "stealth": 1,
            "charisma": 1,
            "strength": 1
        }
        self.skill_points = 5  # Points to allocate to skills
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100

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
        """Display main game menu"""
        while self.running:
            # Check if player is dead
            if self.player.health <= 0:
                self.handle_death()
                continue
                
            self.display_header()
            
            print(f"{Fore.YELLOW}What do you want to do?{Style.RESET_ALL}")
            print()
            print(f"1. {Fore.GREEN}Explore the city{Style.RESET_ALL}")
            print(f"2. {Fore.RED}Criminal activities{Style.RESET_ALL}")
            print(f"3. {Fore.BLUE}Vehicle management{Style.RESET_ALL}")
            print(f"4. {Fore.MAGENTA}Visit locations{Style.RESET_ALL}")
            print(f"5. {Fore.CYAN}Character status{Style.RESET_ALL}")
            print(f"6. {Fore.YELLOW}Save game{Style.RESET_ALL}")
            print(f"7. {Fore.WHITE}Load game{Style.RESET_ALL}")
            print(f"8. {Fore.RED}Quit game{Style.RESET_ALL}")
            print()
            
            choice = input(f"{Fore.CYAN}Elige tu opción / Enter your choice (1-9): {Style.RESET_ALL}").strip()
            
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
                self.character_status()
            elif choice == "7":
                self.allocate_skill_points()
            elif choice == "8":
                self.change_language()
            elif choice == "9":
                self.save_game()
            elif choice == "10":
                self.load_game()
            elif choice == "11":
                self.quit_game()
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

    def fight_police(self):
        """Fight against police when wanted"""
        print(f"\n{Fore.RED}Lucha Contra la Policía / Fight Police{Style.RESET_ALL}")
        
        if self.player.wanted_level == 0:
            print(f"{Fore.YELLOW}No tienes nivel de búsqueda / No wanted level. Police aren't looking for you.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        # Different police responses based on wanted level
        police_forces = {
            1: {"name": "Patrulla Local / Local Patrol", "officers": 2, "armor": 20, "weapons": "pistols"},
            2: {"name": "Policía de Ciudad / City Police", "officers": 3, "armor": 40, "weapons": "shotguns"},
            3: {"name": "SWAT Ligero / Light SWAT", "officers": 4, "armor": 60, "weapons": "rifles"},
            4: {"name": "SWAT Pesado / Heavy SWAT", "officers": 6, "armor": 80, "weapons": "assault rifles"},
            5: {"name": "Federales / Federal Agents", "officers": 8, "armor": 100, "weapons": "military gear"}
        }
        
        force = police_forces[self.player.wanted_level]
        
        print(f"Enfrentando: {force['name']}")
        print(f"Oficiales: {force['officers']}")
        print(f"Armadura: {force['armor']}")
        print(f"Armamento: {force['weapons']}")
        print()
        
        # Check player weapons
        player_weapons = [weapon for weapon in self.player.inventory if weapon in WEAPONS]
        if not player_weapons or player_weapons == ["fists"]:
            print(f"{Fore.RED}¡Sin armas apropiadas para enfrentar policía! / No proper weapons to fight police!{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")
            return
        
        fight_taunts = [
            "'¡Nunca nos atraparán vivos!'",
            "'¡Las calles son nuestras!'", 
            "'¡Vengan por nosotros, cobardes!'"
        ]
        
        print(f"{Fore.YELLOW}{random.choice(fight_taunts)}{Style.RESET_ALL}")
        
        if input("\n¿Iniciar tiroteo? / Start shootout? (s/y or n): ").lower() in ['s', 'y']:
            # Calculate combat effectiveness
            player_firepower = 0
            for weapon in player_weapons:
                if weapon in WEAPONS:
                    player_firepower += WEAPONS[weapon]["damage"]
            
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

def main():
    """Main entry point"""
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    main()
