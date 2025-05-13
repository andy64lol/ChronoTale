# Import standard libraries
import os
import sys
import time
import random
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Check if the script is being run directly or through the launcher
def check_launcher():
    if 'LAUNCHED_FROM_MENU' not in os.environ:
        print("This game should be launched through the launch.py launcher.")
        print("Please run 'python3 launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit()

# Game data
day = 1
money = 1000
reputation = 3.0
restaurant_level = 1
restaurant_name = "4ndyBurguer"

# Time management
current_time_period = "morning"  # current time of day period
hour = 8  # 24-hour format (8 AM game start)
minute = 0
day_of_week = 1  # 1 = Monday, 7 = Sunday
week = 1
time_speed = 1.0  # Time modifier for game speed

# Marketing and business variables
active_marketing = 0  # Current marketing level (0-10)
active_collaborations = []  # List of active business collaborations

# Location management
owned_locations = []  # Store dictionaries with location type and customizations
current_location_index = 0  # Index of currently active location

# Initialize with a small starting restaurant in Downtown
starting_location = {
    "id": "downtown_location", 
    "type": "small_restaurant", 
    "name": "Downtown Restaurant",
    "area": "Downtown",
    "floors": 1,
    "staff_assigned": [],
    "custom_name": "Burger Boss Downtown",
    "upgrades": [],
    "decor_level": 1,
    "kitchen_level": 1,
    "seating_capacity": 30,
    "daily_customers": 0,
    "total_customers": 0,
    "is_open": False
}
owned_locations.append(starting_location)

# For backward compatibility
locations = ["Downtown"]
# Define initial location
initial_location = "Downtown"

# Customer-related variables
customer_base = 20
max_daily_customers = 40
customer_patience = 5
customer_satisfaction = 3.0
satisfaction_history = [3.0]
daily_served = 0
total_served = 0
regular_customers = 0

# Staff-related variables
staff = []
active_collaborations = []

# Inventory
inventory = {
    # Burger ingredients
    "buns": 20,
    "patties": 20, 
    "lettuce": 10,
    "tomato": 10,
    "cheese": 10,
    "pickles": 10,
    "onions": 10,
    "ketchup": 30,
    "mustard": 30,
    "mayo": 30,
    "bacon": 0,
    "premium_buns": 0,
    "angus_beef": 0,
    "avocado": 0,
    "gourmet_cheese": 0,
    
    # Side ingredients
    "potatoes": 20,
    "onion_bulbs": 0,
    "batter": 0,
    "seasoning": 10,
    "cooking_oil": 10,
    "poutine_cheese": 0,
    "gravy_mix": 0,
    
    # Beverage ingredients
    "4ndycola_syrup": 0,
    "root_beer_syrup": 0,
    "orange_soda_syrup": 0,
    "lemon_lime_syrup": 0,
    "coffee_beans": 0,
    "milk": 0,
    "water": 0,
    "ice_cream_mix": 0,
    
    # Dessert ingredients
    "cookie_dough": 0,
    "brownie_mix": 0,
    "apple_pie_filling": 0,
    "sugar": 10,
    "chocolate_sauce": 0
}

# Costs
costs = {
    # Burger ingredients
    "buns": 0.5,
    "patties": 1.2,
    "lettuce": 0.3,
    "tomato": 0.4,
    "cheese": 0.6,
    "pickles": 0.3,
    "onions": 0.2,
    "ketchup": 0.1,
    "mustard": 0.1,
    "mayo": 0.1,
    "bacon": 0.8,
    "premium_buns": 1.0,
    "angus_beef": 2.0,
    "avocado": 0.7,
    "gourmet_cheese": 1.2,
    
    # Side ingredients
    "potatoes": 0.5,
    "onion_bulbs": 0.3,
    "batter": 0.5,
    "seasoning": 0.2,
    "cooking_oil": 0.8,
    "poutine_cheese": 1.0,
    "gravy_mix": 0.6,
    
    # Beverage ingredients
    "4ndycola_syrup": 1.0,
    "root_beer_syrup": 1.0,
    "orange_soda_syrup": 1.0,
    "lemon_lime_syrup": 1.0,
    "coffee_beans": 1.2,
    "milk": 0.5,
    "water": 0.2,
    "ice_cream_mix": 0.8,
    
    # Dessert ingredients
    "cookie_dough": 0.6,
    "brownie_mix": 0.7,
    "apple_pie_filling": 0.8,
    "sugar": 0.2,
    "chocolate_sauce": 0.5
}

# Prices for menu items (default prices)
prices = {
    # Burgers
    "basic_burger": 5.99,
    "cheeseburger": 6.99,
    "deluxe_burger": 7.99,
    "bacon_burger": 8.99,
    "veggie_burger": 7.49,
    "double_burger": 9.99,
    "premium_burger": 11.99,
    "gourmet_burger": 14.99,
    "signature_burger": 12.99,
    "spicy_burger": 8.49,
    "mushroom_burger": 8.99,
    "bbq_burger": 9.49,
    "breakfast_burger": 8.99,
    "fish_burger": 9.99,
    "kawaii_burger": 13.99,
    
    # Sides
    "fries": 2.99,
    "large_fries": 3.99,
    "onion_rings": 4.49,
    "poutine": 5.99,
    
    # Beverages
    "4ndycola": 1.99,
    "root_beer": 1.99,
    "orange_soda": 1.99,
    "lemon_lime_soda": 1.99,
    "coffee": 2.49,
    "milkshake": 4.99,
    
    # Desserts
    "chocolate_chip_cookie": 1.99,
    "brownie": 2.99,
    "apple_pie": 3.49,
    "ice_cream_cone": 2.49,
    "sundae": 3.99,
    
    # Combo Meals
    "basic_combo": 8.99,
    "deluxe_combo": 11.99,
    "premium_combo": 14.99,
    "family_meal": 24.99,
    "kids_meal": 6.99
}

# Customer types with their characteristics
customer_types = [
    "regular",          # Average spending, average patience
    "student",          # Low spending, low patience
    "family",           # High spending, low patience (kids are impatient)
    "business_person",  # High spending, low patience (in a hurry)
    "food_critic",      # Medium spending, high patience, affects reputation more
    "elderly",          # Low spending, high patience
    "tourist",          # Medium spending, high patience
    "health_nut",       # Medium spending, medium patience, prefers healthy options
    "vip"               # Very important, impacts reputation significantly
]

# Staff roles and attributes
staff_roles = {
    "cook": {
        "base_salary": 50,
        "speed_bonus": 0.5,  # Affects burger preparation time
        "error_rate": 0.1,   # Chance of making mistakes
        "max_level": 5,      # Maximum experience level
        "specialties": ["Burgers", "Sides", "Desserts"]  # Possible specialties
    },
    "cashier": {
        "base_salary": 40,
        "charm_bonus": 0.3,  # Affects customer satisfaction
        "error_rate": 0.15,  # Chance of making mistakes with orders/change
        "max_level": 5,
        "specialties": ["Upselling", "Speed", "Customer Service"]
    },
    "manager": {
        "base_salary": 75,
        "efficiency_bonus": 0.2,  # Reduces overall operating costs
        "morale_bonus": 0.2,      # Improves staff performance
        "max_level": 5,
        "specialties": ["Efficiency", "Marketing", "Training"]
    },
    "cleaner": {
        "base_salary": 35,
        "hygiene_bonus": 0.4,  # Affects restaurant rating
        "speed_bonus": 0.1,    # Affects table turnover rate
        "max_level": 5,
        "specialties": ["Restaurant", "Kitchen", "Bathrooms"]
    },
    "automation_specialist": {
        "base_salary": 85,
        "automation_bonus": 0.5,  # Affects automation level
        "maintenance_skill": 0.3, # Reduces maintenance costs
        "max_level": 5,
        "specialties": ["Kitchen", "Service", "Inventory"],
        "unlock_requirement": {"collaboration": "MechaMeat"}  # Requires MechaMeat collaboration
    }
}

# Celebrity endorsement data
celebrity_endorsements = {
    # Movie Stars & Action Heroes
    "MaximusSteelheart": {
        "name": "Maximus Steelheart",
        "type": "Action Movie Star",
        "cost": 50000,
        "duration": 30,  # Days
        "benefits": {
            "customer_boost": 1.4,
            "reputation_gain": 0.3,
            "special_item": "Steelheart Explosion Burger"
        },
        "description": "A tough action movie star known for his explosive roles and love for high-energy foods."
    },
    "RileyCrimson": {
        "name": "Riley Crimson",
        "type": "Drama Star",
        "cost": 45000,
        "duration": 30,  # Days
        "benefits": {
            "customer_boost": 1.3,
            "reputation_gain": 0.4,
            "special_item": "Crimson Space Opera Combo"
        },
        "description": "A former action hero turned drama queen, famous for her roles in epic space operas."
    },
    "SapphireLuna": {
        "name": "Sapphire Luna",
        "type": "Indie Film Star",
        "cost": 30000,
        "duration": 25,  # Days
        "benefits": {
            "customer_boost": 1.25,
            "social_media_boost": 1.5,
            "special_item": "Sapphire Sci-Fi Slider"
        },
        "description": "A rising star in indie films, known for her roles in sci-fi thrillers."
    },
    "TylerVortex": {
        "name": "Tyler Vortex",
        "type": "Action Hero",
        "cost": 40000,
        "duration": 28,  # Days
        "benefits": {
            "customer_boost": 1.35,
            "male_customer_boost": 1.5,
            "special_item": "Vortex Speed Burger"
        },
        "description": "A popular action hero known for his fast-paced car chase scenes, always craving a good burger after filming."
    },
    
    # Musicians & Singers
    "JadeStorm": {
        "name": "Jade Storm",
        "type": "Rock Musician",
        "cost": 55000,
        "duration": 35,  # Days
        "benefits": {
            "customer_boost": 1.5,
            "younger_customer_boost": 1.6,
            "special_item": "Storm Rock Energy Meal"
        },
        "description": "A rock musician whose electric energy brings crowds wherever she performs."
    },
    "JaxsonBlaze": {
        "name": "Jaxson Blaze",
        "type": "Pop Sensation",
        "cost": 65000,
        "duration": 40,  # Days
        "benefits": {
            "customer_boost": 1.6,
            "teenage_customer_boost": 2.0,
            "special_item": "Blazing Pop Star Combo"
        },
        "description": "A pop sensation with millions of fans. He's often seen in glamorous settings but loves the comfort of a 4ndyBurgers meal."
    },
    "CassidyRayne": {
        "name": "Cassidy Rayne",
        "type": "Country Singer",
        "cost": 35000,
        "duration": 28,  # Days
        "benefits": {
            "customer_boost": 1.3,
            "rural_location_boost": 1.7,
            "special_item": "Country Comfort Burger"
        },
        "description": "A country singer who enjoys simple, hearty meals after a long day of songwriting."
    },
    
    # TV Personalities
    "VinceTheViper": {
        "name": "Vince 'The Viper' Harker",
        "type": "Talk Show Host",
        "cost": 40000,
        "duration": 30,  # Days
        "benefits": {
            "customer_boost": 1.35,
            "older_customer_boost": 1.5,
            "special_item": "Viper Talk Show Special"
        },
        "description": "A charismatic talk show host with an infectious laugh who loves to share his burger cravings with the audience."
    },
    "LolaShine": {
        "name": "Lola Shine",
        "type": "Reality TV Star",
        "cost": 30000,
        "duration": 25,  # Days
        "benefits": {
            "customer_boost": 1.25,
            "female_customer_boost": 1.6,
            "special_item": "Shine Glamour Burger"
        },
        "description": "A famous reality TV star who loves showing off her extravagant lifestyle. She's also a known burger connoisseur."
    },
    
    # Video Game & Social Media Stars
    "XanderByte": {
        "name": "Xander Byte",
        "type": "Game Streamer",
        "cost": 25000,
        "duration": 20,  # Days
        "benefits": {
            "customer_boost": 1.3,
            "teenage_customer_boost": 1.8,
            "special_item": "Gamer Fuel Combo"
        },
        "description": "A viral video game streamer with millions of followers, always sharing his latest 4ndyBurgers experience with his fans."
    },
    "SkylarNova": {
        "name": "Skylar Nova",
        "type": "Social Media Influencer",
        "cost": 28000,
        "duration": 25,  # Days
        "benefits": {
            "customer_boost": 1.25,
            "social_media_boost": 2.0,
            "special_item": "Influencer's Choice Meal"
        },
        "description": "A rising star in the social media world, famous for posting influencer-style content with an occasional 4ndyBurgers cameo."
    },
    
    # Athletes & Olympians
    "CarlosTheBull": {
        "name": "Carlos 'The Bull' Barron",
        "type": "Football Star",
        "cost": 60000,
        "duration": 35,  # Days
        "benefits": {
            "customer_boost": 1.45,
            "male_customer_boost": 1.7,
            "special_item": "The Bull's Power Burger"
        },
        "description": "A legendary football player and sports commentator, known for his muscle-building routine and his love for 4ndyBurgers' premium options."
    },
    "AriaSwift": {
        "name": "Aria Swift",
        "type": "Olympic Gold Medalist",
        "cost": 50000,
        "duration": 30,  # Days
        "benefits": {
            "customer_boost": 1.4,
            "health_conscious_boost": 1.6,
            "special_item": "Gold Medal Fitness Burger"
        },
        "description": "An Olympic gold medalist in track and field, who loves rewarding herself with a delicious meal after training."
    }
}

# Active celebrity endorsements
active_endorsements = []

# Marketing campaign tracking
active_campaigns = []
campaign_effects = {}

# Business collaborations available
collaboration_options = {
    # Supply & Ingredient Collaborations
    "SodaStorm": {
        "name": "SodaStorm Inc.",
        "cost": 15000,
        "description": "Premium beverage supplier offering exclusive drinks and discounts",
        "requirements": {"level": 6, "reputation": 3.5},
        "benefits": {
            "discounts": {"4ndycola_syrup": 0.25, "root_beer_syrup": 0.25, "orange_soda_syrup": 0.25, "lemon_lime_syrup": 0.25},
            "new_items": ["energy_drink_syrup", "fruit_punch_syrup", "sparkling_water"],
            "special_effects": {"beverage_satisfaction": 1.2}
        },
        "active": False,
        "category": "supplier"
    },
    "MechaMeat": {
        "name": "MechaMeat Industries",
        "cost": 25000,
        "description": "Advanced automated cooking systems and premium meat supplier",
        "requirements": {"level": 8, "reputation": 4.0},
        "benefits": {
            "discounts": {"patties": 0.2, "angus_beef": 0.3, "bacon": 0.2},
            "new_items": ["wagyu_beef", "automated_grill_system"],
            "special_effects": {"cooking_automation": 2, "meat_quality": 1.3}
        },
        "active": False,
        "category": "supplier"
    },
    "KawaiiKitchen": {
        "name": "KawaiiKitchen Co.",
        "cost": 12000,
        "description": "Japanese-inspired food designs and kawaii presentation styles",
        "requirements": {"level": 5, "reputation": 3.0},
        "benefits": {
            "discounts": {},
            "new_items": ["kawaii_burger", "bento_box", "dessert_platter"],
            "special_effects": {"satisfaction_bonus": 1.15, "instagram_exposure": 1.5}
        },
        "active": False,
        "category": "supplier"
    },
    "TurboTyres": {
        "name": "TurboTyres Delivery",
        "cost": 20000,
        "description": "Fast delivery service to expand your business reach",
        "requirements": {"level": 7, "reputation": 3.8},
        "benefits": {
            "discounts": {},
            "new_items": [],
            "special_effects": {"enable_delivery": True, "customer_volume": 1.25}
        },
        "active": False,
        "category": "delivery"
    },
    
    # Location Expansion Collaborations
    "QuickZoom": {
        "name": "QuickZoom Drive-Thru™",
        "cost": 35000,
        "description": "Drive-thru franchising specialists for rapid-service locations",
        "requirements": {"level": 10, "reputation": 4.0},
        "benefits": {
            "discounts": {},
            "new_items": [],
            "special_effects": {"enable_drive_thru": True},
            "new_locations": ["small_drive_thru", "medium_drive_thru"]
        },
        "active": False,
        "category": "expansion"
    },
    "NightBite": {
        "name": "NightBite Express™",
        "cost": 30000,
        "description": "Late-night food service specialists for 24-hour operations",
        "requirements": {"level": 9, "reputation": 3.8},
        "benefits": {
            "discounts": {},
            "new_items": ["midnight_special_burger", "night_owl_combo"],
            "special_effects": {"enable_night_shift": True, "night_customer_boost": 1.5}
        },
        "active": False,
        "category": "expansion"
    },
    "FunZone": {
        "name": "FunZone Amusement Parks",
        "cost": 50000,
        "description": "Partner with major amusement parks for prime food locations",
        "requirements": {"level": 15, "reputation": 4.5},
        "benefits": {
            "discounts": {},
            "new_items": ["roller_coaster_meal", "thrill_seeker_combo"],
            "special_effects": {"amusement_park_income": 2.0},
            "new_locations": ["amusement_park_stand"]
        },
        "active": False,
        "category": "expansion"
    },
    "MegaMall": {
        "name": "MegaMall Enterprises",
        "cost": 45000,
        "description": "Premium shopping mall food court locations and management",
        "requirements": {"level": 12, "reputation": 4.2},
        "benefits": {
            "discounts": {},
            "new_items": ["shopper_special", "food_court_feast"],
            "special_effects": {"mall_customer_volume": 1.8},
            "new_locations": ["mall_food_court"]
        },
        "active": False,
        "category": "expansion"
    },
    "SkyBites": {
        "name": "SkyBites Airport Services",
        "cost": 60000,
        "description": "Airport terminal restaurant management and concessions",
        "requirements": {"level": 18, "reputation": 4.7},
        "benefits": {
            "discounts": {},
            "new_items": ["jet_lag_jumbo_meal", "first_class_burger"],
            "special_effects": {"airport_premium_prices": 1.5, "international_exposure": 2.0},
            "new_locations": ["airport_small_stand", "airport_large_stand"]
        },
        "active": False,
        "category": "expansion"
    },
    "SportServe": {
        "name": "SportServe Stadium Solutions",
        "cost": 40000, 
        "description": "Stadium and sporting venue food service specialists",
        "requirements": {"level": 14, "reputation": 4.3},
        "benefits": {
            "discounts": {},
            "new_items": ["home_run_burger", "victory_meal"],
            "special_effects": {"event_day_boost": 3.0},
            "new_locations": ["stadium_vendor"]
        },
        "active": False,
        "category": "expansion"
    },
    
    # Advertising Collaborations
    "AdCrunch": {
        "name": "AdCrunch Media™",
        "cost": 18000,
        "description": "Traditional advertising specialists for print, radio and TV",
        "requirements": {"level": 7, "reputation": 3.6},
        "benefits": {
            "discounts": {},
            "new_items": [],
            "special_effects": {"marketing_effectiveness": 1.4, "traditional_advertising_boost": 1.3}
        },
        "active": False,
        "category": "advertising"
    },
    "ViralTuna": {
        "name": "ViralTuna Agency™",
        "cost": 22000,
        "description": "Social media marketing and viral campaign specialists",
        "requirements": {"level": 8, "reputation": 3.7},
        "benefits": {
            "discounts": {},
            "new_items": ["viral_challenge_meal", "influencer_special"],
            "special_effects": {"social_media_reach": 2.0, "younger_customer_boost": 1.5}
        },
        "active": False,
        "category": "advertising"
    }
}

# Track active distributor discounts (populated when collaborations are activated)
distributor_discounts = {}

# Restaurant upgrades
available_upgrades = {
    "equipment": {
        "basic_grill": {
            "cost": 500,
            "description": "10% faster cooking time",
            "effect": {"cooking_speed": 1.1},
            "owned": False
        },
        "deluxe_grill": {
            "cost": 2000,
            "description": "25% faster cooking time",
            "effect": {"cooking_speed": 1.25},
            "owned": False,
            "requires": "basic_grill"
        },
        "industrial_fryer": {
            "cost": 1500,
            "description": "Unlock onion rings and other fried items",
            "effect": {"side_items": True, "unlock_items": ["onion_rings"]},
            "owned": False
        },
        "double_fryer": {
            "cost": 3000,
            "description": "30% faster frying and reduces oil usage by 20%",
            "effect": {"frying_speed": 1.3, "oil_efficiency": 0.8},
            "owned": False,
            "requires": "industrial_fryer"
        },
        "automatic_drink_dispenser": {
            "cost": 1200,
            "description": "Unlock 4ndyCola and soda drinks",
            "effect": {"drink_items": True},
            "owned": False
        },
        "premium_drink_machine": {
            "cost": 2500,
            "description": "Add root beer, orange soda and lemon-lime soda to menu",
            "effect": {"unlock_items": ["root_beer", "orange_soda", "lemon_lime_soda"]},
            "owned": False,
            "requires": "automatic_drink_dispenser"
        },
        "coffee_machine": {
            "cost": 2000,
            "description": "Unlock coffee beverages",
            "effect": {"unlock_items": ["coffee"]},
            "owned": False
        },
        "ice_cream_machine": {
            "cost": 4000,
            "description": "Unlock milkshakes, ice cream cones and sundaes",
            "effect": {"unlock_items": ["milkshake", "ice_cream_cone", "sundae"]},
            "owned": False
        },
        "dessert_station": {
            "cost": 3000,
            "description": "Unlock cookies, brownies and apple pies",
            "effect": {"unlock_items": ["chocolate_chip_cookie", "brownie", "apple_pie"]},
            "owned": False
        },
        "combo_meal_register": {
            "cost": 1500,
            "description": "15% discount when making combo meals (saves ingredients)",
            "effect": {"combo_efficiency": 0.85},
            "owned": False
        },
        "automated_patty_flipper": {
            "cost": 3500,
            "description": "Automates burger cooking, reducing errors by 40%",
            "effect": {"error_reduction": 0.4, "staff_efficiency": 1.15},
            "owned": False
        },
        "self-service_kiosk": {
            "cost": 5000,
            "description": "Reduces need for cashiers and improves order accuracy",
            "effect": {"order_accuracy": 1.2, "cashier_reduction": 1},
            "owned": False
        },
        "smart_inventory_system": {
            "cost": 4000,
            "description": "Tracks inventory and suggests purchases automatically",
            "effect": {"inventory_management": True, "waste_reduction": 0.15},
            "owned": False
        }
    },
    "furniture": {
        "basic_tables": {
            "cost": 800,
            "description": "Add seating for 10 more customers",
            "effect": {"seating_capacity": 10},
            "owned": False
        },
        "comfortable_chairs": {
            "cost": 1500,
            "description": "Customers stay 20% longer, improving chance of additional orders",
            "effect": {"customer_stay_time": 1.2},
            "owned": False
        },
        "theme_decoration": {
            "cost": 3000, 
            "description": "Themed decor improves restaurant atmosphere and satisfaction",
            "effect": {"customer_satisfaction": 0.3},
            "owned": False
        },
        "outdoor_seating": {
            "cost": 4000,
            "description": "Add outdoor seating for 15 more customers",
            "effect": {"seating_capacity": 15, "special_effect": "weather_dependent"},
            "owned": False
        },
        "play_area": {
            "cost": 5000,
            "description": "Attracts families and keeps kids entertained",
            "effect": {"family_attraction": 0.5, "customer_satisfaction": 0.2},
            "owned": False
        }
    },
    "restaurant": {
        "expanded_kitchen": {
            "cost": 8000,
            "description": "Larger kitchen allows for more staff and efficiency",
            "effect": {"max_cooks": 2, "cooking_efficiency": 1.2},
            "owned": False
        },
        "dining_expansion": {
            "cost": 10000, 
            "description": "Doubles dining space and customer capacity",
            "effect": {"customer_capacity": 2.0},
            "owned": False
        },
        "drive_thru": {
            "cost": 15000,
            "description": "Add drive-thru service for 30% more customers",
            "effect": {"customer_volume": 1.3, "takeout_efficiency": 1.5},
            "owned": False
        },
        "restroom_upgrade": {
            "cost": 3000,
            "description": "Improved restrooms increase customer satisfaction",
            "effect": {"customer_satisfaction": 0.2, "hygiene_rating": 0.5},
            "owned": False
        },
        "entertainment_system": {
            "cost": 5000,
            "description": "TV, music and games keeps customers entertained while waiting",
            "effect": {"customer_patience": 1.3, "customer_satisfaction": 0.1},
            "owned": False
        },
        "security_system": {
            "cost": 4000,
            "description": "Reduces chance of robbery and improves safety",
            "effect": {"robbery_chance": 0.2, "insurance_cost": 0.8},
            "owned": False
        }
    },
    "research": {
        "recipe_development": {
            "cost": 3000,
            "description": "Unlocks premium burger recipes",
            "effect": {"unlock_recipes": ["gourmet_burger", "signature_burger"]},
            "owned": False
        },
        "quality_ingredients": {
            "cost": 5000,
            "description": "Access to higher quality ingredients for better reputation",
            "effect": {"food_quality": 1.2, "unlock_items": ["premium_buns", "angus_beef", "gourmet_cheese"]},
            "owned": False
        },
        "efficient_cooking": {
            "cost": 4000,
            "description": "Improved cooking techniques reduce ingredient waste by 15%",
            "effect": {"ingredient_efficiency": 0.85},
            "owned": False
        },
        "menu_optimization": {
            "cost": 2000,
            "description": "Scientific menu design increases sales of high-margin items by 20%",
            "effect": {"premium_sale_chance": 1.2},
            "owned": False
        },
        "staff_training_program": {
            "cost": 6000,
            "description": "Comprehensive training improves staff performance by 15%",
            "effect": {"staff_efficiency": 1.15, "staff_error_rate": 0.85},
            "owned": False
        },
        "customer_loyalty_program": {
            "cost": 4000,
            "description": "Loyalty cards and rewards increase regular customers by 25%",
            "effect": {"regular_customers": 1.25, "customer_retention": 1.2},
            "owned": False
        },
        "supply_chain_optimization": {
            "cost": 7000,
            "description": "Optimized supply chain reduces ingredient costs by 15%",
            "effect": {"ingredient_cost": 0.85},
            "owned": False
        },
        "health_menu_options": {
            "cost": 5000,
            "description": "Healthy menu alternatives attract new customer demographics",
            "effect": {"health_customer_attraction": 1.3, "unlock_recipes": ["veggie_burger", "grilled_chicken_burger"]},
            "owned": False
        }
    }
}

# Recipe requirements (ingredients needed to make each item)
recipes = {
    # Burgers
    "basic_burger": {
        "buns": 1,
        "patties": 1,
        "lettuce": 1,
        "tomato": 1,
        "ketchup": 1,
        "mustard": 1,
        "preparation_time": 60  # seconds
    },
    "cheeseburger": {
        "buns": 1,
        "patties": 1,
        "cheese": 1,
        "lettuce": 1,
        "tomato": 1,
        "ketchup": 1,
        "mustard": 1,
        "preparation_time": 70  # seconds
    },
    "deluxe_burger": {
        "buns": 1,
        "patties": 1,
        "cheese": 1,
        "lettuce": 1,
        "tomato": 1,
        "pickles": 1,
        "onions": 1,
        "ketchup": 1,
        "mustard": 1,
        "mayo": 1,
        "preparation_time": 90  # seconds
    },
    "bacon_burger": {
        "buns": 1,
        "patties": 1,
        "cheese": 1,
        "bacon": 2,
        "lettuce": 1,
        "tomato": 1,
        "ketchup": 1,
        "mayo": 1,
        "preparation_time": 100  # seconds
    },
    "double_burger": {
        "buns": 1,
        "patties": 2,
        "cheese": 2,
        "lettuce": 1,
        "tomato": 1,
        "onions": 1,
        "ketchup": 1,
        "mayo": 1,
        "preparation_time": 120  # seconds
    },
    "premium_burger": {
        "premium_buns": 1,
        "angus_beef": 1,
        "gourmet_cheese": 1,
        "lettuce": 1,
        "tomato": 1,
        "onions": 1,
        "mayo": 1,
        "preparation_time": 150  # seconds
    },
    "kawaii_burger": {
        "premium_buns": 1,
        "patties": 1,
        "cheese": 1,
        "lettuce": 1,
        "tomato": 1,
        "preparation_time": 180  # seconds
    },
    
    # Sides
    "fries": {
        "potatoes": 2,
        "cooking_oil": 1,
        "seasoning": 1,
        "preparation_time": 180  # seconds
    },
    "large_fries": {
        "potatoes": 4,
        "cooking_oil": 2,
        "seasoning": 2,
        "preparation_time": 240  # seconds
    },
    "onion_rings": {
        "onion_bulbs": 2,
        "batter": 1,
        "cooking_oil": 1,
        "preparation_time": 210  # seconds
    },
    "poutine": {
        "potatoes": 3,
        "cooking_oil": 1,
        "poutine_cheese": 1,
        "gravy_mix": 1,
        "preparation_time": 300  # seconds
    },
    
    # Beverages
    "4ndycola": {
        "4ndycola_syrup": 1,
        "preparation_time": 20  # seconds
    },
    "root_beer": {
        "root_beer_syrup": 1,
        "preparation_time": 20  # seconds
    },
    "orange_soda": {
        "orange_soda_syrup": 1,
        "preparation_time": 20  # seconds
    },
    "lemon_lime_soda": {
        "lemon_lime_syrup": 1,
        "preparation_time": 20  # seconds
    },
    "coffee": {
        "coffee_beans": 1,
        "preparation_time": 60  # seconds
    },
    "milkshake": {
        "ice_cream_mix": 1,
        "milk": 1,
        "preparation_time": 90  # seconds
    },
    
    # Desserts
    "chocolate_chip_cookie": {
        "cookie_dough": 1,
        "sugar": 1,
        "preparation_time": 120  # seconds
    },
    "brownie": {
        "brownie_mix": 1,
        "sugar": 1,
        "chocolate_sauce": 1,
        "preparation_time": 150  # seconds
    },
    "apple_pie": {
        "apple_pie_filling": 1,
        "sugar": 1,
        "preparation_time": 180  # seconds
    },
    "ice_cream_cone": {
        "ice_cream_mix": 1,
        "sugar": 1,
        "preparation_time": 60  # seconds
    },
    "sundae": {
        "ice_cream_mix": 2,
        "chocolate_sauce": 1,
        "preparation_time": 90  # seconds
    },
    
    # Combo Meals
    "basic_combo": {
        "basic_burger": 1,
        "fries": 1,
        "4ndycola": 1,
        "preparation_time": 30  # seconds (assembly time only)
    },
    "deluxe_combo": {
        "deluxe_burger": 1,
        "large_fries": 1,
        "4ndycola": 1,
        "preparation_time": 30  # seconds (assembly time only)
    },
    "premium_combo": {
        "premium_burger": 1,
        "large_fries": 1,
        "4ndycola": 1,
        "chocolate_chip_cookie": 1,
        "preparation_time": 30  # seconds (assembly time only)
    },
    "family_meal": {
        "cheeseburger": 2,
        "bacon_burger": 2,
        "large_fries": 2,
        "4ndycola": 4,
        "preparation_time": 60  # seconds (assembly time only)
    },
    "kids_meal": {
        "basic_burger": 1,
        "fries": 1,
        "4ndycola": 1,
        "chocolate_chip_cookie": 1,
        "preparation_time": 30  # seconds (assembly time only)
    }
}

# Marketing campaigns
marketing_campaigns = {
    "flyers": {
        "cost": 500,
        "duration": 5,  # days
        "customer_boost": 0.15,  # 15% more customers
        "description": "Distribute flyers in the neighborhood"
    },
    "social_media": {
        "cost": 1000,
        "duration": 7,
        "customer_boost": 0.2,
        "reputation_boost": 0.1,
        "description": "Launch a social media campaign"
    },
    "newspaper_ad": {
        "cost": 1500,
        "duration": 10,
        "customer_boost": 0.25,
        "description": "Place an ad in the local newspaper"
    },
    "radio_spot": {
        "cost": 3000,
        "duration": 14,
        "customer_boost": 0.3,
        "reputation_boost": 0.2,
        "description": "Air a radio commercial"
    },
    "tv_commercial": {
        "cost": 8000,
        "duration": 30,
        "customer_boost": 0.5,
        "reputation_boost": 0.3,
        "description": "Produce and air a TV commercial"
    },
    "influencer": {
        "cost": 5000,
        "duration": 20,
        "customer_boost": 0.4,
        "reputation_boost": 0.25,
        "description": "Partner with a local food influencer"
    },
    "promo_event": {
        "cost": 4000,
        "duration": 3,
        "customer_boost": 1.0,  # Double customers
        "description": "Host a special promotional event"
    },
    "loyalty_cards": {
        "cost": 2000,
        "duration": 60,
        "regular_customer_boost": 0.3,
        "description": "Introduce loyalty cards with rewards"
    }
}

# Active marketing campaigns
active_campaigns = []

# Research queue
research_queue = []

# Print header
def clear():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear()
    print(f"{Fore.GREEN}======================================================")
    print(f"{Fore.YELLOW}{restaurant_name} - Day {day}")
    print(f"{Fore.GREEN}======================================================")

# Main menu
def main_menu():
    global restaurant_name
    
    while True:
        print_header()
        print(f"{Fore.MAGENTA}BURGER BOSS TYCOON")
        print(f"{Fore.CYAN}Welcome to your fast food empire!")
        
        print(f"\n{Fore.YELLOW}1. New Game")
        print(f"{Fore.YELLOW}2. Load Game")
        print(f"{Fore.YELLOW}3. How to Play")
        print(f"{Fore.YELLOW}4. Quit")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == "1":
            start_new_game()
        elif choice == "2":
            load_game()
        elif choice == "3":
            how_to_play()
        elif choice == "4":
            return
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)

# Define restaurant_upgrades variable to store upgrade status
restaurant_upgrades = {}

# Location types with their attributes
location_types = {
    # Regular Restaurant Locations
    "small_restaurant": {
        "name": "Small Restaurant",
        "cost": 10000,
        "max_floors": 1,
        "max_staff": {"cook": 2, "cashier": 2, "manager": 1, "cleaner": 1, "automation_specialist": 0},
        "base_customers": 50,
        "maintenance_cost": 100,
        "description": "A small restaurant with basic facilities in a decent location.",
        "upgrade_cost": 15000,
        "upgrades_to": "medium_restaurant"
    },
    "medium_restaurant": {
        "name": "Medium Restaurant",
        "cost": 25000,
        "max_floors": 2,
        "max_staff": {"cook": 4, "cashier": 3, "manager": 2, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 100,
        "maintenance_cost": 250,
        "description": "A medium-sized restaurant with good visibility and customer flow.",
        "upgrade_cost": 35000,
        "upgrades_to": "large_restaurant"
    },
    "large_restaurant": {
        "name": "Large Restaurant",
        "cost": 60000,
        "max_floors": 3,
        "max_staff": {"cook": 6, "cashier": 5, "manager": 3, "cleaner": 4, "automation_specialist": 2},
        "base_customers": 200,
        "maintenance_cost": 500,
        "description": "A large restaurant in a prime location with excellent visibility.",
        "upgrade_cost": None
    },
    
    # Drive-Thru Locations (requires QuickZoom collaboration)
    "small_drive_thru": {
        "name": "Small Drive-Thru",
        "cost": 30000,
        "max_floors": 1,
        "max_staff": {"cook": 3, "cashier": 3, "manager": 1, "cleaner": 1, "automation_specialist": 1},
        "base_customers": 80,
        "maintenance_cost": 200,
        "description": "A small drive-thru location focused on quick service and takeout.",
        "special_attributes": {"drive_thru_enabled": True, "takeout_boost": 1.5},
        "upgrade_cost": 30000,
        "upgrades_to": "medium_drive_thru",
        "requires_collaboration": "QuickZoom"
    },
    "medium_drive_thru": {
        "name": "Medium Drive-Thru",
        "cost": 60000,
        "max_floors": 2,
        "max_staff": {"cook": 5, "cashier": 4, "manager": 2, "cleaner": 2, "automation_specialist": 2},
        "base_customers": 150,
        "maintenance_cost": 350,
        "description": "A medium drive-thru with dual lanes and an efficient kitchen layout.",
        "special_attributes": {"drive_thru_enabled": True, "takeout_boost": 2.0, "dual_lanes": True},
        "upgrade_cost": None,
        "requires_collaboration": "QuickZoom"
    },
    
    # Special Locations (each requires its own collaboration)
    "mall_food_court": {
        "name": "Mall Food Court Location",
        "cost": 40000,
        "max_floors": 3,
        "max_staff": {"cook": 4, "cashier": 4, "manager": 2, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 180,
        "maintenance_cost": 450,
        "description": "A premium location in a busy shopping mall food court.",
        "special_attributes": {"shopping_rush_boost": 2.0, "weekend_boost": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "MegaMall"
    },
    "amusement_park_stand": {
        "name": "Amusement Park Food Stand",
        "cost": 50000,
        "max_floors": 4,
        "max_staff": {"cook": 5, "cashier": 5, "manager": 2, "cleaner": 3, "automation_specialist": 2},
        "base_customers": 250,
        "maintenance_cost": 600,
        "description": "A large food stand inside a popular amusement park with high traffic.",
        "special_attributes": {"seasonal_boost": 3.0, "family_customer_boost": 2.0, "premium_pricing": 1.3},
        "upgrade_cost": None,
        "requires_collaboration": "FunZone"
    },
    "stadium_vendor": {
        "name": "Stadium Vendor Stand",
        "cost": 35000,
        "max_floors": 1,
        "max_staff": {"cook": 3, "cashier": 4, "manager": 1, "cleaner": 1, "automation_specialist": 1},
        "base_customers": 400,
        "maintenance_cost": 300,
        "description": "A compact vendor stand inside a sports stadium with event-based traffic.",
        "special_attributes": {"event_day_only": True, "high_volume": True, "captive_audience": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "SportServe"
    },
    "airport_small_stand": {
        "name": "Airport Terminal Stand",
        "cost": 45000,
        "max_floors": 2,
        "max_staff": {"cook": 3, "cashier": 4, "manager": 1, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 200,
        "maintenance_cost": 400,
        "description": "A food stand in an airport terminal with international customers.",
        "special_attributes": {"international_customers": True, "24h_operation": True, "premium_pricing": 1.4},
        "upgrade_cost": 50000,
        "upgrades_to": "airport_large_stand",
        "requires_collaboration": "SkyBites"
    },
    "airport_large_stand": {
        "name": "Large Airport Terminal Restaurant",
        "cost": 95000,
        "max_floors": 3,
        "max_staff": {"cook": 6, "cashier": 6, "manager": 2, "cleaner": 4, "automation_specialist": 2},
        "base_customers": 300,
        "maintenance_cost": 800,
        "description": "A large restaurant in a major airport terminal hub with premium services.",
        "special_attributes": {"international_customers": True, "24h_operation": True, "premium_pricing": 1.6, "business_class_service": True},
        "upgrade_cost": None,
        "requires_collaboration": "SkyBites"
    },
    
    # Additional Premium Locations
    "luxury_hotel_lobby": {
        "name": "Luxury Hotel Lobby Restaurant",
        "cost": 70000,
        "max_floors": 1,
        "max_staff": {"cook": 5, "cashier": 3, "manager": 2, "cleaner": 3, "automation_specialist": 1},
        "base_customers": 120,
        "maintenance_cost": 700,
        "description": "An upscale restaurant in the lobby of a 5-star hotel with affluent clientele.",
        "special_attributes": {"premium_pricing": 2.0, "high_tip_rate": 1.8, "prestige_boost": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "LuxuryStay"
    },
    "gaming_arcade": {
        "name": "Gaming Arcade Restaurant",
        "cost": 45000,
        "max_floors": 1,
        "max_staff": {"cook": 4, "cashier": 3, "manager": 1, "cleaner": 2, "automation_specialist": 2},
        "base_customers": 180,
        "maintenance_cost": 350,
        "description": "A vibrant eatery inside a popular gaming arcade, catering to gamers of all ages.",
        "special_attributes": {"late_night_boost": 2.0, "younger_customers": True, "continuous_traffic": 1.4},
        "upgrade_cost": None,
        "requires_collaboration": "GameZone"
    },
    "cruise_ship_food_court": {
        "name": "Cruise Ship Food Court",
        "cost": 85000,
        "max_floors": 2,
        "max_staff": {"cook": 5, "cashier": 5, "manager": 2, "cleaner": 3, "automation_specialist": 2},
        "base_customers": 220,
        "maintenance_cost": 750,
        "description": "A restaurant on a luxury cruise ship serving vacationers on the high seas.",
        "special_attributes": {"captive_audience": 2.0, "premium_pricing": 1.7, "vacation_mode": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "OceanLine"
    },
    "train_station_kiosk": {
        "name": "Train Station Kiosk",
        "cost": 30000,
        "max_floors": 2,
        "max_staff": {"cook": 3, "cashier": 4, "manager": 1, "cleaner": 1, "automation_specialist": 1},
        "base_customers": 300,
        "maintenance_cost": 250,
        "description": "A convenient food kiosk in a busy train station catering to commuters and travelers.",
        "special_attributes": {"rush_hour_boost": 2.5, "take_away_focus": True, "quick_service": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "RailRoute"
    },
    "tropical_resort": {
        "name": "Tropical Island Resort",
        "cost": 100000,
        "max_floors": 3,
        "max_staff": {"cook": 6, "cashier": 5, "manager": 2, "cleaner": 4, "automation_specialist": 2},
        "base_customers": 150,
        "maintenance_cost": 900,
        "description": "An exclusive restaurant at a tropical island resort with breathtaking ocean views.",
        "special_attributes": {"premium_pricing": 2.5, "exotic_location": True, "vacation_dining": 1.8},
        "upgrade_cost": None,
        "requires_collaboration": "TropicalGetaway"
    },
    "volcano_lookout": {
        "name": "Active Volcano Tourist Spot",
        "cost": 65000,
        "max_floors": 1,
        "max_staff": {"cook": 3, "cashier": 3, "manager": 1, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 100,
        "maintenance_cost": 600,
        "description": "A unique dining spot near an active volcano, offering thrilling views with your meal.",
        "special_attributes": {"tourism_boost": 2.0, "premium_pricing": 1.8, "exotic_experience": True},
        "upgrade_cost": None,
        "requires_collaboration": "ExtremeTourism"
    },
    "desert_oasis": {
        "name": "Desert Oasis Tour Stand",
        "cost": 40000,
        "max_floors": 1,
        "max_staff": {"cook": 2, "cashier": 2, "manager": 1, "cleaner": 1, "automation_specialist": 1},
        "base_customers": 80,
        "maintenance_cost": 400,
        "description": "A refreshing pit stop in the middle of desert tours, catering to adventurous travelers.",
        "special_attributes": {"tourism_dependent": True, "seasonal_boost": 1.7, "premium_pricing": 1.4},
        "upgrade_cost": None,
        "requires_collaboration": "WildernessExpeditions"
    },
    "ancient_ruins": {
        "name": "Ancient Ruins Site",
        "cost": 55000,
        "max_floors": 2,
        "max_staff": {"cook": 4, "cashier": 3, "manager": 1, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 120,
        "maintenance_cost": 500,
        "description": "A themed restaurant adjacent to famous ancient ruins, popular with history enthusiasts and tourists.",
        "special_attributes": {"tourism_dependent": True, "group_tours": 1.8, "historical_appeal": 1.5},
        "upgrade_cost": None,
        "requires_collaboration": "HistoricTourism"
    },
    "safari_park": {
        "name": "Safari Adventure Park",
        "cost": 75000,
        "max_floors": 2,
        "max_staff": {"cook": 5, "cashier": 4, "manager": 2, "cleaner": 3, "automation_specialist": 1},
        "base_customers": 200,
        "maintenance_cost": 650,
        "description": "An exotic-themed restaurant in a safari park, offering views of wildlife during your meal.",
        "special_attributes": {"family_destination": True, "seasonal_boost": 2.0, "themed_experience": 1.6},
        "upgrade_cost": None,
        "requires_collaboration": "WildlifePartnership"
    },
    "great_wall": {
        "name": "Great Wall of China Restaurant",
        "cost": 90000,
        "max_floors": 1,
        "max_staff": {"cook": 4, "cashier": 4, "manager": 1, "cleaner": 3, "automation_specialist": 1},
        "base_customers": 150,
        "maintenance_cost": 800,
        "description": "A unique dining experience near one of the world's most famous landmarks.",
        "special_attributes": {"international_tourism": 2.5, "premium_pricing": 2.0, "landmark_prestige": True},
        "upgrade_cost": None,
        "requires_collaboration": "GlobalLandmarks"
    },
    "cruise_stopover": {
        "name": "Cruise Ship Stopover",
        "cost": 60000,
        "max_floors": 2,
        "max_staff": {"cook": 6, "cashier": 5, "manager": 2, "cleaner": 3, "automation_specialist": 2},
        "base_customers": 280,
        "maintenance_cost": 550,
        "description": "A port restaurant serving passengers during cruise ship stopovers, creating intense busy periods.",
        "special_attributes": {"seasonal_boost": 2.2, "cruise_dependent": True, "port_business": 1.8},
        "upgrade_cost": None,
        "requires_collaboration": "HarborDining"
    },
    "national_park": {
        "name": "National Park Eatery",
        "cost": 45000,
        "max_floors": 1,
        "max_staff": {"cook": 3, "cashier": 3, "manager": 1, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 170,
        "maintenance_cost": 400,
        "description": "A rustic restaurant inside a national park, popular with hikers and nature enthusiasts.",
        "special_attributes": {"seasonal_boost": 2.5, "outdoor_enthusiasts": 1.4, "weekend_boost": 1.6},
        "upgrade_cost": None,
        "requires_collaboration": "NatureParks"
    },
    "arts_center": {
        "name": "Cultural Arts Center",
        "cost": 50000,
        "max_floors": 1,
        "max_staff": {"cook": 4, "cashier": 3, "manager": 1, "cleaner": 2, "automation_specialist": 1},
        "base_customers": 130,
        "maintenance_cost": 450,
        "description": "A sophisticated cafe inside a cultural arts center, catering to art enthusiasts and performers.",
        "special_attributes": {"event_dependent": True, "cultural_prestige": 1.5, "evening_boost": 1.7},
        "upgrade_cost": None,
        "requires_collaboration": "ArtsAlliance"
    }
}

# Time of day effects on customer behavior
time_of_day = {
    "morning": {
        "hours": "6:00 AM - 11:00 AM",
        "customer_modifier": 0.8,
        "popular_items": ["coffee", "breakfast_burger"],
        "special_effects": {
            "breakfast_items_boost": 2.0,
            "coffee_sales_boost": 2.5
        }
    },
    "lunch": {
        "hours": "11:00 AM - 2:00 PM",
        "customer_modifier": 1.5,
        "popular_items": ["basic_combo", "deluxe_combo"],
        "special_effects": {
            "combo_meal_boost": 2.0,
            "business_lunch_rush": 1.8
        }
    },
    "afternoon": {
        "hours": "2:00 PM - 5:00 PM",
        "customer_modifier": 0.6,
        "popular_items": ["ice_cream_cone", "milkshake", "fries"],
        "special_effects": {
            "dessert_boost": 1.5,
            "side_items_boost": 1.3
        }
    },
    "dinner": {
        "hours": "5:00 PM - 9:00 PM",
        "customer_modifier": 1.4,
        "popular_items": ["premium_combo", "family_meal"],
        "special_effects": {
            "family_meal_boost": 2.0,
            "premium_burger_boost": 1.7
        }
    },
    "late_night": {
        "hours": "9:00 PM - 2:00 AM",
        "customer_modifier": 0.7,
        "popular_items": ["double_burger", "midnight_special_burger"],
        "special_effects": {
            "large_meal_boost": 1.5,
            "younger_customers": True
        },
        "requires_collaboration": "NightBite"
    },
    "overnight": {
        "hours": "2:00 AM - 6:00 AM",
        "customer_modifier": 0.3,
        "popular_items": ["coffee", "basic_burger"],
        "special_effects": {
            "reduced_menu": True,
            "night_shift_penalty": 0.8
        },
        "requires_collaboration": "NightBite"
    }
}

# Business Collaborations menu
def business_collaborations_menu():
    global money, active_collaborations, distributor_discounts, restaurant_level, reputation, restaurant_upgrades
    
    while True:
        print_header()
        print(f"{Fore.GREEN}=== BUSINESS COLLABORATIONS ===")
        print(f"{Fore.CYAN}Level: {restaurant_level} | Reputation: {reputation:.1f}/5.0")
        print(f"{Fore.YELLOW}Available Funds: ${money:.2f}")
        
        # Show active collaborations
        if active_collaborations:
            print(f"\n{Fore.GREEN}Active Collaborations:")
            
            # Group collaborations by category
            active_by_category = {"supplier": [], "expansion": [], "advertising": [], "delivery": []}
            
            for collab_id in active_collaborations:
                collab = collaboration_options[collab_id]
                if "category" in collab:
                    category = collab["category"]
                    if category in active_by_category:
                        active_by_category[category].append(collab)
                else:
                    # For backward compatibility
                    active_by_category["supplier"].append(collab)
            
            # Display by category
            for category, title in [
                ("supplier", "Supply & Ingredient Partners"), 
                ("expansion", "Location & Expansion Partners"),
                ("advertising", "Marketing & Advertising Partners"),
                ("delivery", "Delivery & Logistics Partners")
            ]:
                if active_by_category[category]:
                    print(f"\n{Fore.YELLOW}{title}:")
                    for collab in active_by_category[category]:
                        print(f"• {Fore.CYAN}{collab['name']} - {collab['description']}")
        else:
            print(f"\n{Fore.RED}No active business collaborations.")
        
        # Main collaboration menu options
        print(f"\n{Fore.GREEN}Partnership Categories:")
        print("1. Supply & Ingredient Partnerships")
        print("2. Location & Expansion Partnerships")
        print("3. Marketing & Advertising Partnerships")
        print("4. Delivery & Logistics Partnerships")
        print("5. Return to Daily Menu")
        
        # Get category choice
        category_choice = input("\nSelect a category to explore (1-5): ")
        
        if category_choice == "5":
            break
            
        # Map choices to categories
        category_map = {
            "1": "supplier",
            "2": "expansion",
            "3": "advertising",
            "4": "delivery"
        }
        
        if category_choice not in category_map:
            print(f"{Fore.RED}Invalid choice.")
            time.sleep(1)
            continue
            
        selected_category = category_map[category_choice]
        
        # Show collaborations for the selected category
        while True:
            print_header()
            print(f"{Fore.GREEN}=== {selected_category.upper()} PARTNERSHIPS ===")
            print(f"{Fore.CYAN}Level: {restaurant_level} | Reputation: {reputation:.1f}/5.0")
            print(f"{Fore.YELLOW}Available Funds: ${money:.2f}")
            
            # List available collaborations in this category
            available_collabs = []
            
            i = 1
            for collab_id, collab in collaboration_options.items():
                # Skip if not in selected category or already active
                if collab.get("category", "supplier") != selected_category or collab["active"]:
                    continue
                    
                # Check if requirements are met
                meets_requirements = True
                req_text = ""
                
                if "level" in collab["requirements"] and restaurant_level < collab["requirements"]["level"]:
                    meets_requirements = False
                    req_text += f" Restaurant Level {collab['requirements']['level']},"
                
                if "reputation" in collab["requirements"] and reputation < collab["requirements"]["reputation"]:
                    meets_requirements = False
                    req_text += f" Reputation {collab['requirements']['reputation']:.1f},"
                
                # Display with appropriate color based on whether requirements are met
                if meets_requirements:
                    print(f"{i}. {Fore.CYAN}{collab['name']} - ${collab['cost']:.2f}")
                    print(f"   {collab['description']}")
                    
                    # Show benefits
                    if "discounts" in collab["benefits"] and collab["benefits"]["discounts"]:
                        discount_text = ", ".join([f"{k.replace('_', ' ')} ({int(v*100)}% off)" for k, v in collab["benefits"]["discounts"].items()])
                        print(f"   {Fore.GREEN}Discounts: {discount_text}")
                    
                    if "new_items" in collab["benefits"] and collab["benefits"]["new_items"]:
                        items_text = ", ".join([item.replace('_', ' ').title() for item in collab["benefits"]["new_items"]])
                        print(f"   {Fore.GREEN}New Items: {items_text}")
                    
                    # Show new locations for expansion partnerships
                    if "new_locations" in collab["benefits"] and collab["benefits"]["new_locations"]:
                        locations_text = []
                        for loc_type in collab["benefits"]["new_locations"]:
                            if loc_type in location_types:
                                locations_text.append(location_types[loc_type]["name"])
                        if locations_text:
                            print(f"   {Fore.GREEN}New Locations: {', '.join(locations_text)}")
                    
                    if "special_effects" in collab["benefits"]:
                        effects = []
                        for effect, value in collab["benefits"]["special_effects"].items():
                            if isinstance(value, bool):
                                effects.append(effect.replace('_', ' ').title())
                            elif isinstance(value, (int, float)) and value > 1:
                                effects.append(f"{effect.replace('_', ' ').title()} +{int((value-1)*100)}%")
                        if effects:
                            print(f"   {Fore.GREEN}Special Effects: {', '.join(effects)}")
                    
                    available_collabs.append(collab_id)
                    i += 1
                else:
                    print(f"{Fore.LIGHTBLACK_EX}{collab['name']} - ${collab['cost']:.2f} (Locked)")
                    print(f"   {Fore.RED}Requirements not met:{req_text[:-1]}")
            
            if not available_collabs:
                print(f"\n{Fore.RED}No available partnerships in this category.")
                input("Press Enter to return to categories...")
                break
                
            print(f"\n{i}. Return to Categories")
            
            # Get collaboration choice
            choice = input(f"\nSelect a collaboration to establish (1-{i}): ")
            
            if choice == str(i):
                break
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num < i:
                    selected_collab_id = available_collabs[choice_num - 1]
                    selected_collab = collaboration_options[selected_collab_id]
                    
                    # Confirm partnership
                    print(f"\n{Fore.YELLOW}Establish partnership with {selected_collab['name']} for ${selected_collab['cost']:.2f}?")
                    confirm = input("Confirm (y/n): ")
                    
                    if confirm.lower() == 'y':
                        # Check if can afford
                        if money >= selected_collab['cost']:
                            # Establish partnership
                            money -= selected_collab['cost']
                            collaboration_options[selected_collab_id]["active"] = True
                            active_collaborations.append(selected_collab_id)
                            
                            # Apply benefits
                            
                            # 1. Add ingredient discounts to the distributor_discounts dictionary
                            if "discounts" in selected_collab["benefits"]:
                                for item, discount in selected_collab["benefits"]["discounts"].items():
                                    distributor_discounts[item] = discount
                            
                            # 2. Add new inventory items if needed
                            if "new_items" in selected_collab["benefits"]:
                                for item in selected_collab["benefits"]["new_items"]:
                                    if item not in inventory:
                                        inventory[item] = 0
                                        
                                    # Set costs for new items if they don't have costs yet
                                    if item not in costs:
                                        # Set a reasonable default cost
                                        costs[item] = 1.5
                                        
                                    # Add recipes for new menu items if they don't exist
                                    if item.endswith("_burger") and item not in recipes:
                                        # Default burger recipe
                                        recipes[item] = {
                                            "buns": 1,
                                            "patties": 1,
                                            "lettuce": 1,
                                            "cheese": 1,
                                            "special_sauce": 1,
                                            "preparation_time": 90
                                        }
                                        # Set a default price if not already set
                                        if item not in prices:
                                            prices[item] = 9.99
                            
                            # 3. Unlock new locations if provided
                            if "new_locations" in selected_collab["benefits"]:
                                for loc_type in selected_collab["benefits"]["new_locations"]:
                                    print(f"{Fore.GREEN}You can now purchase {location_types[loc_type]['name']} locations!")
                            
                            # Autosave after establishing collaboration
                            auto_save(reason="Business Collaboration")
                            
                            print(f"\n{Fore.GREEN}Partnership established with {selected_collab['name']}!")
                            print("The benefits of this collaboration are now available to your restaurant.")
                            input("Press Enter to continue...")
                        else:
                            print(f"\n{Fore.RED}You don't have enough money for this partnership.")
                            input("Press Enter to continue...")
                else:
                    print(f"{Fore.RED}Invalid choice.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.")
                time.sleep(1)

# Start new game
def start_new_game():
    global restaurant_name, money, day, reputation, restaurant_level
    global staff, inventory, active_collaborations, active_campaigns
    
    print_header()
    print(f"{Fore.GREEN}=== NEW GAME ===")
    print(f"{Fore.CYAN}Welcome to Burger Boss Tycoon!")
    print(f"{Fore.CYAN}As a new restaurant owner, your goal is to build a successful fast food empire.")
    
    # Get restaurant name
    default_name = "Burger Boss"
    custom_name = input(f"\nEnter your restaurant name (default: {default_name}): ")
    restaurant_name = custom_name if custom_name else default_name
    
    # Reset game variables
    money = 1000
    day = 1
    reputation = 3.0
    restaurant_level = 1
    staff = []
    active_collaborations = []
    active_campaigns = []
    
    # Reset inventory to starting values
    inventory = {
        # Burger ingredients
        "buns": 20,
        "patties": 20, 
        "lettuce": 10,
        "tomato": 10,
        "cheese": 10,
        "pickles": 10,
        "onions": 10,
        "ketchup": 30,
        "mustard": 30,
        "mayo": 30,
        "bacon": 0,
        "premium_buns": 0,
        "angus_beef": 0,
        "avocado": 0,
        "gourmet_cheese": 0,
        
        # Side ingredients
        "potatoes": 20,
        "onion_bulbs": 0,
        "batter": 0,
        "seasoning": 10,
        "cooking_oil": 10,
        "poutine_cheese": 0,
        "gravy_mix": 0,
        
        # Beverage ingredients
        "4ndycola_syrup": 0,
        "root_beer_syrup": 0,
        "orange_soda_syrup": 0,
        "lemon_lime_syrup": 0,
        "coffee_beans": 0,
        "milk": 0,
        "ice_cream_mix": 0,
        
        # Dessert ingredients
        "cookie_dough": 0,
        "brownie_mix": 0,
        "apple_pie_filling": 0,
        "sugar": 10,
        "chocolate_sauce": 0
    }
    
    # Reset all upgrades to not owned
    for category in available_upgrades:
        for upgrade in available_upgrades[category]:
            available_upgrades[category][upgrade]["owned"] = False
    
    # Reset all business collaborations to inactive
    for collab_id in collaboration_options:
        collaboration_options[collab_id]["active"] = False
    
    print(f"\n{Fore.GREEN}Welcome to {restaurant_name}!")
    print(f"{Fore.CYAN}You have ${money:.2f} to start your business.")
    print(f"{Fore.CYAN}Hire staff, buy ingredients, and serve customers to grow your restaurant.")
    input("\nPress Enter to begin...")
    
    daily_menu()

# Functions for game save/load system
def get_save_directory():
    """Get the save directory, creating it if it doesn't exist"""
    # Create saves directory if it doesn't exist
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'burger_saves')
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def get_save_slots():
    """Get list of save slots with information"""
    save_dir = get_save_directory()
    save_slots = []
    
    # Check for autosave (slot 0)
    autosave_path = os.path.join(save_dir, "burger_save_0.json")
    if os.path.exists(autosave_path):
        try:
            with open(autosave_path, 'r') as f:
                save_data = json.load(f)
                save_slots.append({
                    "slot": 0,
                    "exists": True,
                    "name": save_data.get("restaurant_name", "Unknown"),
                    "day": save_data.get("day", 0),
                    "money": save_data.get("money", 0),
                    "level": save_data.get("restaurant_level", 1),
                    "location_count": len(save_data.get("owned_locations", [])),
                    "timestamp": save_data.get("timestamp", "Unknown"),
                    "autosave": True
                })
        except Exception as e:
            # If there's an error loading the autosave, treat it as non-existent
            save_slots.append({
                "slot": 0,
                "exists": False,
                "error": str(e),
                "autosave": True
            })
    else:
        save_slots.append({
            "slot": 0,
            "exists": False,
            "autosave": True
        })
    
    # Check for save files (slots 1-5)
    for slot in range(1, 6):
        save_path = os.path.join(save_dir, f"burger_save_{slot}.json")
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r') as f:
                    save_data = json.load(f)
                    save_slots.append({
                        "slot": slot,
                        "exists": True,
                        "name": save_data.get("restaurant_name", "Unknown"),
                        "day": save_data.get("day", 0),
                        "money": save_data.get("money", 0),
                        "level": save_data.get("restaurant_level", 1),
                        "location_count": len(save_data.get("owned_locations", [])),
                        "timestamp": save_data.get("timestamp", "Unknown")
                    })
            except Exception as e:
                # If there's an error loading the save, treat it as non-existent
                save_slots.append({
                    "slot": slot,
                    "exists": False,
                    "error": str(e)
                })
        else:
            save_slots.append({
                "slot": slot,
                "exists": False
            })
    
    return save_slots

def save_game(slot=None, auto=False, auto_reason=""):
    """Save the game to a specified slot
    
    Args:
        slot: Save slot (1-5) or None to show selection menu
        auto: If True, perform autosave without user interaction
        auto_reason: Reason for the autosave (e.g., "day change", "level up")
    """
    global money, day, reputation, restaurant_level, restaurant_name
    global staff, inventory, active_collaborations, active_campaigns
    global prices, owned_locations, current_location_index, daily_sales
    global hour, minute, day_of_week, active_celebrity_endorsements
    
    # If auto save, use slot 0 (autosave slot)
    if auto:
        slot = 0  # Use slot 0 for autosaves
    # If no slot specified, show slot selection menu
    elif slot is None:
        show_save_slots()
        print(f"\n{Fore.YELLOW}Select a slot to save your game (1-5), or 0 to cancel: ")
        try:
            choice = int(input("> "))
            if choice == 0:
                print(f"{Fore.YELLOW}Save cancelled.")
                return False
            elif 1 <= choice <= 5:
                slot = choice
            else:
                print(f"{Fore.RED}Invalid choice.")
                return False
        except ValueError:
            print(f"{Fore.RED}Invalid input.")
            return False
    
    # Create save data
    save_data = {
        "restaurant_name": restaurant_name,
        "money": money,
        "day": day,
        "hour": hour,
        "minute": minute,
        "day_of_week": day_of_week,
        "reputation": reputation,
        "restaurant_level": restaurant_level,
        "staff": staff,
        "inventory": inventory,
        "active_collaborations": active_collaborations,
        "active_campaigns": active_campaigns,
        "prices": prices,
        "owned_locations": owned_locations,
        "current_location_index": current_location_index,
        "daily_sales": daily_sales,
        "active_celebrity_endorsements": active_celebrity_endorsements,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "autosave_reason": auto_reason if auto else ""
    }
    
    # Save to file
    save_dir = get_save_directory()
    save_path = os.path.join(save_dir, f"burger_save_{slot}.json")
    try:
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        if not auto:
            if slot == 0:
                print(f"\n{Fore.GREEN}Game autosaved successfully!")
            else:
                print(f"\n{Fore.GREEN}Game saved successfully to slot {slot}!")
        return True
    except Exception as e:
        if not auto:
            print(f"\n{Fore.RED}Error saving game: {str(e)}")
        return False

def auto_save(reason=""):
    """Perform an automatic save without user interaction
    
    Args:
        reason (str): Optional reason for the autosave (e.g., "day change", "level up")
    """
    return save_game(auto=True, auto_reason=reason)

def show_save_slots():
    """Display all save slots with their information"""
    print_header()
    print(f"{Fore.GREEN}=== SAVE SLOTS ===\n")
    
    save_slots = get_save_slots()
    
    for slot_info in save_slots:
        slot_num = slot_info["slot"]
        is_autosave = "autosave" in slot_info and slot_info["autosave"]
        
        # Skip showing autosave if it doesn't exist
        if is_autosave and not slot_info["exists"]:
            continue
            
        slot_label = "Autosave" if is_autosave else f"Slot {slot_num}"
        
        if slot_info["exists"]:
            print(f"{Fore.CYAN}{slot_label}: {slot_info['name']} - Day {slot_info['day']}")
            print(f"  Money: ${slot_info['money']:,.2f} | Level: {slot_info['level']} | Locations: {slot_info['location_count']}")
            print(f"  Saved: {slot_info['timestamp']}")
        else:
            if "error" in slot_info:
                print(f"{Fore.RED}{slot_label}: ERROR - {slot_info['error']}")
            else:
                print(f"{Fore.YELLOW}{slot_label}: [Empty]")

def load_game(slot=None):
    """Load a game from a specified slot
    
    Args:
        slot: Save slot (1-5) or None to show selection menu
        
    Returns:
        bool: True if successful, False otherwise
    """
    global money, day, reputation, restaurant_level, restaurant_name
    global staff, inventory, active_collaborations, active_campaigns
    global prices, owned_locations, current_location_index, daily_sales
    global hour, minute, day_of_week, active_celebrity_endorsements
    
    # If no slot specified, show slot selection menu
    if slot is None:
        show_save_slots()
        print(f"\n{Fore.YELLOW}Select a slot to load (0-5), or 9 to cancel: ")
        print(f"{Fore.YELLOW}Note: 0 = Autosave, 1-5 = Regular save slots")
        try:
            choice = int(input("> "))
            if choice == 9:
                print(f"{Fore.YELLOW}Load cancelled.")
                return False
            elif 0 <= choice <= 5:
                slot = choice
            else:
                print(f"{Fore.RED}Invalid choice.")
                return False
        except ValueError:
            print(f"{Fore.RED}Invalid input.")
            return False
    
    # Load from file
    save_dir = get_save_directory()
    save_path = os.path.join(save_dir, f"burger_save_{slot}.json")
    
    if not os.path.exists(save_path):
        print(f"\n{Fore.RED}No save file found in slot {slot}.")
        input("Press Enter to continue...")
        return False
    
    try:
        with open(save_path, 'r') as f:
            save_data = json.load(f)
        
        # Load game data
        restaurant_name = save_data.get("restaurant_name", "4ndyBurguer")
        money = save_data.get("money", 1000)
        day = save_data.get("day", 1)
        hour = save_data.get("hour", 8)
        minute = save_data.get("minute", 0)
        day_of_week = save_data.get("day_of_week", 1)
        reputation = save_data.get("reputation", 3.0)
        restaurant_level = save_data.get("restaurant_level", 1)
        staff = save_data.get("staff", [])
        inventory = save_data.get("inventory", {})
        active_collaborations = save_data.get("active_collaborations", [])
        active_campaigns = save_data.get("active_campaigns", [])
        prices = save_data.get("prices", {})
        owned_locations = save_data.get("owned_locations", [])
        current_location_index = save_data.get("current_location_index", 0)
        daily_sales = save_data.get("daily_sales", {})
        active_celebrity_endorsements = save_data.get("active_celebrity_endorsements", [])
        
        print(f"\n{Fore.GREEN}Game loaded successfully from slot {slot}!")
        input("Press Enter to continue...")
        
        # Go to daily menu
        daily_menu()
        
        return True
    except Exception as e:
        print(f"\n{Fore.RED}Error loading game: {str(e)}")
        input("Press Enter to continue...")
        return False

# How to play
def how_to_play():
    print_header()
    print(f"{Fore.GREEN}=== HOW TO PLAY ===")
    print(f"{Fore.CYAN}Welcome to Burger Boss Tycoon, a fast food restaurant management simulation!")
    
    print(f"\n{Fore.YELLOW}Game Objective:")
    print("Build a successful fast food empire by managing your restaurant, serving customers,")
    print("upgrading your facilities, and expanding to new locations.")
    
    print(f"\n{Fore.YELLOW}Daily Operations:")
    print("1. Buy ingredients to stock your inventory")
    print("2. Hire and manage staff to improve service")
    print("3. Open your restaurant to serve customers")
    print("4. Upgrade equipment and facilities")
    print("5. Launch marketing campaigns")
    print("6. Research new recipes and technologies")
    
    print(f"\n{Fore.YELLOW}Key Metrics:")
    print("- Money: Your available funds")
    print("- Reputation: How customers view your restaurant (1-5 stars)")
    print("- Restaurant Level: Represents your business growth")
    
    print(f"\n{Fore.YELLOW}Tips:")
    print("- Balance your menu prices for profit while keeping customers happy")
    print("- Keep your inventory stocked to avoid lost sales")
    print("- Invest in marketing to attract more customers")
    print("- Upgrade equipment to improve efficiency and unlock new menu items")
    print("- Hire and train staff to provide better service")
    
    input("\nPress Enter to return to the main menu...")

# Daily menu
def daily_menu():
    global day, money, current_time_period, hour, minute, day_of_week, active_collaborations
    
    while True:
        print_header()
        print(f"{Fore.YELLOW}Day {day} ({get_day_name(day_of_week)}) - {get_formatted_time()} ({current_time_period.replace('_', ' ').title()})")
        print(f"{Fore.CYAN}Money: ${money:.2f} | Reputation: {reputation:.1f}/5.0 | Level: {restaurant_level}")
        
        # Show current location information
        if owned_locations:
            current_location = owned_locations[current_location_index]
            location_name = current_location.get("custom_name", "Unknown Location")
            location_type = location_types.get(current_location["type"], {"name": "Unknown Type"})["name"]
            location_status = f"{Fore.GREEN}Open" if current_location.get("is_open", False) else f"{Fore.RED}Closed"
            print(f"{Fore.CYAN}Current Location: {location_name} ({location_type}) - {location_status}")
        
        # Show time period status
        time_period_info = time_of_day[current_time_period]
        if "requires_collaboration" in time_period_info:
            collab_name = time_period_info["requires_collaboration"]
            required_active = collab_name in active_collaborations
            period_status = f"{Fore.GREEN}Available" if required_active else f"{Fore.RED}Requires {collab_name} Collaboration"
            print(f"{Fore.CYAN}Time Period Status: {period_status}")
            
        # Show important stats like inventory levels
        low_ingredients = [item for item, qty in inventory.items() if qty < 10 and item in ["patties", "buns"]]
        if low_ingredients:
            print(f"\n{Fore.RED}Low Ingredients Warning: {', '.join(low_ingredients)}")
        
        # Business Operations
        print(f"\n{Fore.GREEN}=== BUSINESS OPERATIONS ===")
        print(f"{Fore.CYAN}1. Open Restaurant (Serve Customers)")
        print(f"{Fore.CYAN}2. View Financial Report")
        
        # Inventory Management
        print(f"\n{Fore.GREEN}=== INVENTORY MANAGEMENT ===")
        print(f"{Fore.CYAN}3. Go Shopping (Buy Ingredients)")
        print(f"{Fore.CYAN}4. Check Inventory")
        print(f"{Fore.CYAN}5. View Recipes")
        
        # Restaurant Management
        print(f"\n{Fore.GREEN}=== RESTAURANT MANAGEMENT ===")
        print(f"{Fore.CYAN}6. Upgrade Restaurant")
        print(f"{Fore.CYAN}7. Manage Staff")
        print(f"{Fore.CYAN}8. Marketing Campaigns")
        
        # Research and Development
        print(f"\n{Fore.GREEN}=== RESEARCH & DEVELOPMENT ===")
        print(f"{Fore.CYAN}9. Research New Recipes")
        print(f"{Fore.CYAN}10. Price Management")
        
        # Expansion
        print(f"\n{Fore.GREEN}=== EXPANSION ===")
        print(f"{Fore.CYAN}11. Manage Locations")
        print(f"{Fore.CYAN}12. Business Collaborations")
        print(f"{Fore.CYAN}13. Time Management")
        
        # System Options
        print(f"\n{Fore.GREEN}=== SYSTEM ===")
        print(f"{Fore.CYAN}14. Save Game")
        print(f"{Fore.CYAN}15. Return to Main Menu")
        
        choice = input("\nSelect an option (1-15): ")
        
        if choice == "1":
            open_restaurant()
        elif choice == "2":
            financial_report()
        elif choice == "3":
            go_shopping()
        elif choice == "4":
            check_inventory()
        elif choice == "5":
            view_recipes()
        elif choice == "6":
            upgrade_restaurant()
        elif choice == "7":
            manage_staff()
        elif choice == "8":
            marketing_menu()
        elif choice == "9":
            research_recipes()
        elif choice == "10":
            manage_prices()
        elif choice == "11":
            manage_locations()
        elif choice == "12":
            business_collaborations_menu()
        elif choice == "13":
            advance_time_dialog()
        elif choice == "14":
            save_game()
            input("Press Enter to continue...")
        elif choice == "15":
            if input(f"{Fore.YELLOW}Return to main menu? Progress since last save will be lost. (y/n): ").lower() == 'y':
                main_menu()
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)

# Financial report
def financial_report():
    pass

# Upgrade restaurant
def upgrade_restaurant():
    pass

# View category upgrades
def view_category_upgrades(category):
    pass

# Purchase upgrade
def purchase_upgrade(category, upgrade_name):
    pass

# Apply upgrade effects
def apply_upgrade_effects(category, upgrade_name):
    pass

# Manage staff
def manage_staff():
    global staff, money
    
    while True:
        print_header()
        print(f"{Fore.GREEN}=== STAFF MANAGEMENT ===")
        print(f"{Fore.YELLOW}Available funds: ${money:.2f}")
        
        # Display current staff
        print(f"\n{Fore.CYAN}Current Staff:")
        if staff:
            for i, employee in enumerate(staff):
                # Basic employee info
                print(f"{i+1}. {employee['name']} - {employee['role'].title()} (Level {employee['level']})")
                
                # Performance info
                perf_color = Fore.RED if employee['performance'] < 0.9 else Fore.GREEN if employee['performance'] > 1.1 else Fore.CYAN
                print(f"   Performance: {perf_color}{employee['performance']:.2f}")
                
                # Salary info
                print(f"   Salary: ${employee['salary']}/day, Days worked: {employee['days_worked']}")
                
                # Show specialty if present
                if "specialty" in employee:
                    print(f"   Specialty: {Fore.YELLOW}{employee['specialty']}")
                
                # Show automation level if present
                if "automation_level" in employee:
                    print(f"   Automation: {Fore.MAGENTA}Level {employee['automation_level']}")
        else:
            print("No staff hired yet.")
        
        # Staff management options
        print(f"\n{Fore.YELLOW}Options:")
        print("1. Hire Staff")
        print("2. Train Staff")
        print("3. Fire Staff")
        print("4. Return to Daily Menu")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == "1":
            hire_staff()
        elif choice == "2":
            train_staff()
        elif choice == "3":
            fire_staff()
        elif choice == "4":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)

# Hire staff function
def hire_staff():
    global staff, money, staff_roles, active_collaborations
    
    print_header()
    print(f"{Fore.GREEN}=== HIRE STAFF ===")
    print(f"{Fore.YELLOW}Available funds: ${money:.2f}")
    
    # List available staff roles
    print("\nAvailable Positions:")
    roles = list(staff_roles.keys())
    
    # Filter roles based on unlocked collaborations
    available_roles = []
    for role in roles:
        role_data = staff_roles[role]
        # Check if role has unlock requirements
        if "unlock_requirement" in role_data:
            # Check if MechaMeat collaboration is required and active
            if "collaboration" in role_data["unlock_requirement"]:
                required_collab = role_data["unlock_requirement"]["collaboration"]
                if required_collab in collaboration_options and collaboration_options[required_collab]["active"]:
                    available_roles.append(role)
        else:
            available_roles.append(role)
    
    # Display available roles
    for i, role in enumerate(available_roles):
        role_data = staff_roles[role]
        print(f"{i+1}. {role.title()} - ${role_data['base_salary']}/day")
        if role == "cook":
            print(f"   {Fore.CYAN}Cooks prepare food faster and with fewer mistakes")
        elif role == "cashier":
            print(f"   {Fore.CYAN}Cashiers improve customer satisfaction and order accuracy")
        elif role == "manager":
            print(f"   {Fore.CYAN}Managers improve overall efficiency and staff morale")
        elif role == "cleaner":
            print(f"   {Fore.CYAN}Cleaners maintain hygiene ratings and improve turnover time")
        elif role == "automation_specialist":
            print(f"   {Fore.MAGENTA}Automation specialists program equipment and reduce staff workload")
            print(f"   {Fore.YELLOW}Unlocked through MechaMeat collaboration")
    
    print(f"{len(available_roles)+1}. Cancel")
    
    # Choose role to hire
    choice = input(f"\nSelect a position to hire (1-{len(available_roles)+1}): ")
    
    try:
        choice_num = int(choice)
        if choice_num == len(available_roles) + 1:
            return
        
        if 1 <= choice_num <= len(available_roles):
            selected_role = available_roles[choice_num - 1]
            role_data = staff_roles[selected_role]
            
            # Generate potential candidates
            candidates = []
            for i in range(3):
                # Base candidate attributes
                candidate = {
                    "name": generate_name(),
                    "role": selected_role,
                    "level": 1,
                    "experience": 0,
                    "salary": role_data["base_salary"],
                    "days_worked": 0,
                    "performance": random.uniform(0.8, 1.2)  # Performance multiplier
                }
                
                # Add specialties for some candidates
                if "specialties" in role_data and random.random() < 0.7:  # 70% chance to have a specialty
                    candidate["specialty"] = random.choice(role_data["specialties"])
                
                # Add automation abilities for some candidates if MechaMeat collaboration is active
                if "MechaMeat" in collaboration_options and collaboration_options["MechaMeat"]["active"]:
                    # Higher chance for automation specialists to have automation abilities
                    auto_chance = 0.8 if selected_role == "automation_specialist" else 0.3
                    if random.random() < auto_chance:
                        candidate["automation_level"] = random.randint(1, 3)  # 1-3 automation level
                
                # Add slight modifier to salary based on special traits
                salary_modifier = 1.0
                if "specialty" in candidate:
                    salary_modifier += 0.1  # 10% increase for specialty
                if "automation_level" in candidate:
                    salary_modifier += 0.1 * candidate["automation_level"]  # 10-30% increase for automation
                
                candidate["salary"] = round(candidate["salary"] * salary_modifier)
                candidates.append(candidate)
            
            # Display candidates
            print(f"\n{Fore.GREEN}Available Candidates:")
            for i, candidate in enumerate(candidates):
                performance_desc = "Average"
                if candidate["performance"] > 1.1:
                    performance_desc = f"{Fore.GREEN}Excellent"
                elif candidate["performance"] > 1.0:
                    performance_desc = f"{Fore.CYAN}Good"
                elif candidate["performance"] < 0.9:
                    performance_desc = f"{Fore.RED}Poor"
                
                # Base display info
                display_info = f"{i+1}. {candidate['name']} - ${candidate['salary']}/day - Performance: {performance_desc}"
                
                # Add specialty info if present
                if "specialty" in candidate:
                    display_info += f" - Specialty: {Fore.YELLOW}{candidate['specialty']}"
                
                # Add automation info if present
                if "automation_level" in candidate:
                    auto_level = candidate["automation_level"]
                    auto_desc = f"{Fore.MAGENTA}Level {auto_level}"
                    display_info += f" - Automation: {auto_desc}"
                
                print(display_info)
            
            print(f"{len(candidates)+1}. Don't hire anyone")
            
            # Choose candidate
            hire_choice = input(f"\nSelect a candidate to hire (1-{len(candidates)+1}): ")
            
            try:
                hire_num = int(hire_choice)
                if hire_num == len(candidates) + 1:
                    return
                
                if 1 <= hire_num <= len(candidates):
                    selected_candidate = candidates[hire_num - 1]
                    
                    # Confirm hire
                    print(f"\n{Fore.YELLOW}Hire {selected_candidate['name']} as a {selected_role.title()} for ${selected_candidate['salary']}/day?")
                    if input("Confirm (y/n): ").lower() != 'y':
                        return
                    
                    # Check if can afford salary for at least 7 days
                    salary_cost = selected_candidate['salary'] * 7
                    if money < salary_cost:
                        print(f"{Fore.RED}Warning: You may not be able to afford this employee's salary for the next week.")
                        if input("Hire anyway? (y/n): ").lower() != 'y':
                            return
                    
                    # Add to staff
                    staff.append(selected_candidate)
                    
                    # Autosave after hiring staff
                    auto_save(reason="Staff Hired")
                    
                    print(f"{Fore.GREEN}Successfully hired {selected_candidate['name']} as a {selected_role.title()}!")
                    input("Press Enter to continue...")
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.")
                time.sleep(1)
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.")
        time.sleep(1)

# Generate a random name for staff
def generate_name():
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                  "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                  "Alex", "Casey", "Jordan", "Taylor", "Morgan", "Avery", "Riley", "Quinn", "Peyton", "Cameron"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                 "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                 "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright"]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Train staff
def train_staff():
    pass

# Fire staff
def fire_staff():
    pass

# Marketing menu
def marketing_menu():
    global money
    
    while True:
        clear()
        print_header()
        print(f"\n{Fore.CYAN}===== MARKETING MENU ====={Style.RESET_ALL}")
        print(f"Money: ${money:.2f}")
        
        print("\n1. Traditional Marketing Campaigns")
        print("2. Celebrity Endorsements")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            traditional_marketing_menu()
        elif choice == "2":
            celebrity_endorsement_menu()
        elif choice == "3":
            return
        else:
            print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

def traditional_marketing_menu():
    global money
    
    while True:
        clear()
        print_header()
        print(f"\n{Fore.CYAN}===== TRADITIONAL MARKETING CAMPAIGNS ====={Style.RESET_ALL}")
        print(f"Money: ${money:.2f}")
        
        print(f"\n{Fore.YELLOW}Active Marketing Campaigns:{Style.RESET_ALL}")
        
        # TODO: Display active marketing campaigns
        print("None")
        
        print(f"\n{Fore.GREEN}Available Marketing Campaigns:{Style.RESET_ALL}")
        print("1. Local Flyers - $500")
        print("2. Newspaper Ad - $1,000")
        print("3. Radio Spot - $2,500")
        print("4. Social Media Campaign - $3,500")
        print("5. TV Commercial - $10,000")
        print("6. Loyalty Program - $5,000")
        
        print("\n7. Back to Marketing Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "7":
            return
        
        campaign_costs = {
            "1": 500,
            "2": 1000,
            "3": 2500, 
            "4": 3500,
            "5": 10000,
            "6": 5000
        }
        
        campaign_names = {
            "1": "Local Flyers",
            "2": "Newspaper Ad",
            "3": "Radio Spot",
            "4": "Social Media Campaign",
            "5": "TV Commercial",
            "6": "Loyalty Program"
        }
        
        if choice in campaign_costs:
            cost = campaign_costs[choice]
            name = campaign_names[choice]
            
            if money >= cost:
                confirm = input(f"Launch {name} campaign for ${cost}? (y/n): ")
                if confirm.lower() == 'y':
                    money -= cost
                    launch_marketing_campaign(name)
                    print(f"\n{Fore.GREEN}Marketing campaign launched successfully!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
            else:
                print(f"\n{Fore.RED}Not enough money to launch this campaign.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
        else:
            print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            
def celebrity_endorsement_menu():
    global money, active_endorsements, day
    
    while True:
        clear()
        print_header()
        print(f"\n{Fore.CYAN}===== CELEBRITY ENDORSEMENTS ====={Style.RESET_ALL}")
        print(f"Money: ${money:.2f}")
        print(f"Current Day: {day}")
        
        # Display active endorsements
        print(f"\n{Fore.YELLOW}Active Endorsements:{Style.RESET_ALL}")
        if not active_endorsements:
            print("None")
        else:
            for endorsement in active_endorsements:
                celeb_id = endorsement["id"]
                celeb_data = celebrity_endorsements[celeb_id]
                days_remaining = endorsement["active_until_day"] - day
                status_color = Fore.GREEN if days_remaining > 10 else Fore.YELLOW if days_remaining > 3 else Fore.RED
                
                print(f"• {celeb_data['name']} ({celeb_data['type']})")
                print(f"  {status_color}Days Remaining: {days_remaining}{Style.RESET_ALL}")
                
                # Show benefits
                if "benefits" in celeb_data:
                    print("  Benefits:")
                    for benefit, value in celeb_data["benefits"].items():
                        if benefit == "customer_boost":
                            print(f"    - Customer Traffic: +{(value-1)*100:.0f}%")
                        elif benefit == "reputation_gain":
                            print(f"    - Daily Reputation Gain: +{value}")
                        elif benefit == "special_item":
                            print(f"    - Special Menu Item: {value}")
                        elif "boost" in benefit:
                            print(f"    - {benefit.replace('_', ' ').title()}: +{(value-1)*100:.0f}%")
        
        # Group celebrities by category
        celeb_categories = {
            "Movie Stars & Action Heroes": [],
            "Musicians & Singers": [],
            "TV Personalities": [],
            "Video Game & Social Media Stars": [],
            "Athletes & Olympians": []
        }
        
        # Filter available celebrities
        available_celebs = []
        for celeb_id, celeb_data in celebrity_endorsements.items():
            # Check if this celebrity is already active
            if any(e["id"] == celeb_id for e in active_endorsements):
                continue
                
            # Check if we can afford them
            if money >= celeb_data["cost"]:
                available_celebs.append(celeb_id)
                
                # Categorize them
                if "Action" in celeb_data["type"] or "Movie" in celeb_data["type"] or "Film" in celeb_data["type"]:
                    celeb_categories["Movie Stars & Action Heroes"].append(celeb_id)
                elif "Singer" in celeb_data["type"] or "Musician" in celeb_data["type"] or "Pop" in celeb_data["type"]:
                    celeb_categories["Musicians & Singers"].append(celeb_id)
                elif "TV" in celeb_data["type"] or "Show" in celeb_data["type"] or "Reality" in celeb_data["type"]:
                    celeb_categories["TV Personalities"].append(celeb_id)
                elif "Game" in celeb_data["type"] or "Social" in celeb_data["type"] or "Media" in celeb_data["type"]:
                    celeb_categories["Video Game & Social Media Stars"].append(celeb_id)
                elif "Athlete" in celeb_data["type"] or "Olympic" in celeb_data["type"] or "Sport" in celeb_data["type"]:
                    celeb_categories["Athletes & Olympians"].append(celeb_id)
        
        # Display available endorsements by category
        print(f"\n{Fore.GREEN}Available Celebrity Endorsements:{Style.RESET_ALL}")
        
        # Track displayed items and their indices for selection
        display_items = []
        item_counter = 1
        
        if not available_celebs:
            print(f"{Fore.RED}No celebrities available to endorse your restaurant.{Style.RESET_ALL}")
            print("You may need more money or wait for current endorsements to end.")
        else:
            for category, celebs in celeb_categories.items():
                if celebs:
                    print(f"\n{Fore.CYAN}{category}:{Style.RESET_ALL}")
                    for celeb_id in celebs:
                        celeb_data = celebrity_endorsements[celeb_id]
                        print(f"{item_counter}. {celeb_data['name']} - ${celeb_data['cost']:,} for {celeb_data['duration']} days")
                        print(f"   {celeb_data['description']}")
                        
                        if "benefits" in celeb_data:
                            benefits_text = []
                            for benefit, value in celeb_data["benefits"].items():
                                if benefit == "customer_boost":
                                    benefits_text.append(f"Customer Traffic: +{(value-1)*100:.0f}%")
                                elif benefit == "special_item":
                                    benefits_text.append(f"Special Menu Item: {value}")
                                elif "boost" in benefit:
                                    benefits_text.append(f"{benefit.replace('_', ' ').title()}: +{(value-1)*100:.0f}%")
                            
                            if benefits_text:
                                print(f"   {Fore.YELLOW}Benefits: {', '.join(benefits_text)}{Style.RESET_ALL}")
                                
                        display_items.append(celeb_id)
                        item_counter += 1
        
        print(f"\n{item_counter}. Back to Marketing Menu")
        
        choice = input("\nEnter your choice: ")
        
        if choice == str(item_counter):
            return
            
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(display_items):
                celeb_id = display_items[choice_idx]
                celeb_data = celebrity_endorsements[celeb_id]
                cost = celeb_data["cost"]
                
                if money >= cost:
                    confirm = input(f"Hire {celeb_data['name']} for ${cost:,} for {celeb_data['duration']} days? (y/n): ")
                    if confirm.lower() == 'y':
                        money -= cost
                        
                        # Add to active endorsements
                        active_endorsements.append({
                            "id": celeb_id,
                            "started_day": day,
                            "active_until_day": day + celeb_data["duration"]
                        })
                        
                        # Handle special menu item addition if there is one
                        if "benefits" in celeb_data and "special_item" in celeb_data["benefits"]:
                            special_item = celeb_data["benefits"]["special_item"]
                            print(f"\n{Fore.GREEN}New menu item added: {special_item}!{Style.RESET_ALL}")
                            
                        print(f"\n{Fore.GREEN}You have successfully partnered with {celeb_data['name']}!{Style.RESET_ALL}")
                        print(f"The endorsement will last for {celeb_data['duration']} days.")
                        
                        input("\nPress Enter to continue...")
                    else:
                        print("Endorsement canceled.")
                else:
                    print(f"\n{Fore.RED}You don't have enough money for this endorsement.{Style.RESET_ALL}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
        
        input("\nPress Enter to continue...")

# Launch marketing campaign
def launch_marketing_campaign(campaign_name):
    global active_campaigns, day
    
    # Create a new campaign effects dictionary
    new_campaign = {}
    
    # Each campaign should have different effects
    if campaign_name == "Local Flyers":
        new_campaign["customer_boost"] = 1.1  # 10% more customers
        new_campaign["duration"] = 3  # lasts 3 days
    elif campaign_name == "Newspaper Ad":
        new_campaign["customer_boost"] = 1.15  # 15% more customers
        new_campaign["duration"] = 5  # lasts 5 days
    elif campaign_name == "Radio Spot":
        new_campaign["customer_boost"] = 1.2  # 20% more customers
        new_campaign["duration"] = 7  # lasts 7 days
    elif campaign_name == "Social Media Campaign":
        new_campaign["customer_boost"] = 1.25  # 25% more customers
        new_campaign["younger_customer_boost"] = 1.4  # 40% more young customers
        new_campaign["duration"] = 10  # lasts 10 days
    elif campaign_name == "TV Commercial":
        new_campaign["customer_boost"] = 1.35  # 35% more customers
        new_campaign["reputation_boost"] = 0.2  # small reputation boost
        new_campaign["duration"] = 14  # lasts 14 days
    elif campaign_name == "Loyalty Program":
        new_campaign["customer_return_rate"] = 1.25  # 25% more return customers
        new_campaign["repeat_customer_spend"] = 1.15  # 15% more spending from repeat customers
        new_campaign["duration"] = 30  # lasts 30 days
    
    # Add campaign to active campaigns list with start and end dates
    new_campaign["start_day"] = day
    new_campaign["end_day"] = day + new_campaign["duration"]
    new_campaign["name"] = campaign_name
    
    active_campaigns.append(new_campaign)
    
    # Autosave after launching a marketing campaign
    auto_save(reason="Marketing Campaign")

# Research recipes
def research_recipes():
    pass

# Get recipe research cost
def get_recipe_research_cost(recipe_name):
    pass

# Manage prices
def manage_prices():
    pass

# Modify price
def modify_price(recipe_name):
    pass

# Calculate recipe cost
def calculate_recipe_cost(recipe_name):
    pass

# Manage locations
def manage_locations():
    global money, owned_locations, current_location_index, active_collaborations
    
    while True:
        print_header()
        print(f"{Fore.GREEN}=== RESTAURANT LOCATIONS ===")
        print(f"{Fore.CYAN}Available Funds: ${money:.2f}\n")
        
        # Show current locations
        if owned_locations:
            print(f"{Fore.YELLOW}Your Restaurant Locations:")
            for i, location in enumerate(owned_locations):
                # Highlight current active location
                prefix = f"{Fore.GREEN}▶ " if i == current_location_index else "  "
                
                # Get location type info
                loc_type = location["type"]
                type_info = location_types.get(loc_type, {"name": "Unknown Type"})
                
                # Format location details
                location_name = location["custom_name"] if "custom_name" in location else f"{location['area']} {type_info['name']}"
                
                # Add status indicators
                status = []
                if location.get("is_open", False):
                    status.append(f"{Fore.GREEN}Open")
                else:
                    status.append(f"{Fore.RED}Closed")
                
                # Show any special attributes for this location
                special = ""
                if "special_attributes" in type_info:
                    special_attrs = []
                    for attr, value in type_info["special_attributes"].items():
                        if isinstance(value, bool) and value:
                            special_attrs.append(attr.replace("_", " ").title())
                    if special_attrs:
                        special = f"{Fore.CYAN} - " + ", ".join(special_attrs)
                
                print(f"{prefix}{i+1}. {location_name} ({type_info['name']}) - {', '.join(status)}{special}")
                print(f"   {Fore.YELLOW}Floors: {location['floors']}/{type_info['max_floors']}, Staff: {len(location.get('staff_assigned', []))}")
        else:
            print(f"{Fore.RED}You don't own any restaurant locations yet.")
        
        print(f"\n{Fore.CYAN}Location Management Options:")
        print("1. Purchase New Location")
        print("2. Upgrade Existing Location")
        print("3. Rename Location")
        print("4. Set Active Location")
        print("5. Sell Location")
        print("6. Return to Daily Menu")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == "1":
            purchase_new_location()
        elif choice == "2":
            upgrade_location()
        elif choice == "3":
            rename_location()
        elif choice == "4":
            set_active_location()
        elif choice == "5":
            sell_location()
        elif choice == "6":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)

def purchase_new_location():
    global money, owned_locations, active_collaborations
    
    print_header()
    print(f"{Fore.GREEN}=== PURCHASE NEW LOCATION ===")
    print(f"{Fore.CYAN}Available Funds: ${money:.2f}\n")
    
    # Get available location types based on owned collaborations
    available_types = []
    
    # Regular restaurant locations are always available
    for loc_type in ["small_restaurant", "medium_restaurant", "large_restaurant"]:
        available_types.append(loc_type)
    
    # Special locations require collaborations
    for loc_type, type_info in location_types.items():
        if "requires_collaboration" in type_info:
            required_collab = type_info["requires_collaboration"]
            # Check if the required collaboration is active
            if required_collab in active_collaborations:
                available_types.append(loc_type)
    
    # Display available location types
    print(f"{Fore.YELLOW}Available Location Types:")
    i = 1
    loc_type_map = {}
    
    for loc_type in available_types:
        type_info = location_types[loc_type]
        loc_type_map[str(i)] = loc_type
        
        cost = type_info["cost"]
        cost_color = Fore.GREEN if money >= cost else Fore.RED
        
        print(f"{i}. {type_info['name']} - {cost_color}${cost:,}")
        print(f"   {type_info['description']}")
        
        # Show special attributes if any
        if "special_attributes" in type_info:
            special_attrs = []
            for attr, value in type_info["special_attributes"].items():
                if isinstance(value, bool) and value:
                    special_attrs.append(attr.replace("_", " ").title())
                elif isinstance(value, (int, float)) and value > 1:
                    special_attrs.append(f"{attr.replace('_', ' ').title()} +{int((value-1)*100)}%")
            if special_attrs:
                print(f"   {Fore.CYAN}Special Features: " + ", ".join(special_attrs))
        
        i += 1
    
    print(f"\n{i}. Return to Location Management")
    
    # Get location type choice
    choice = input(f"\nSelect a location type to purchase (1-{i}): ")
    
    if choice == str(i):
        return
    
    if choice in loc_type_map:
        selected_type = loc_type_map[choice]
        type_info = location_types[selected_type]
        
        # Check if can afford
        if money < type_info["cost"]:
            print(f"\n{Fore.RED}You don't have enough money to purchase this location.")
            input("Press Enter to continue...")
            return
        
        # Select area
        print_header()
        print(f"{Fore.GREEN}=== SELECT LOCATION AREA ===")
        print(f"{Fore.YELLOW}Select an area for your new {type_info['name']}:")
        
        # Different areas have different effects on customer traffic
        areas = [
            {"name": "Downtown", "customer_mod": 1.2, "rent_mod": 1.3, "description": "High foot traffic with premium rent"},
            {"name": "Uptown", "customer_mod": 1.1, "rent_mod": 1.2, "description": "Good traffic with upscale customers"},
            {"name": "Suburbs", "customer_mod": 0.8, "rent_mod": 0.7, "description": "Steady traffic with lower rent"},
            {"name": "Business District", "customer_mod": 1.4, "rent_mod": 1.4, "description": "High lunch rush with premium rent"},
            {"name": "University Campus", "customer_mod": 1.0, "rent_mod": 0.9, "description": "Student traffic with moderate rent"}
        ]
        
        # Add special areas for special location types
        if selected_type == "mall_food_court":
            areas.append({"name": "Luxury Mall", "customer_mod": 1.3, "rent_mod": 1.5, "description": "Premium customers with high rent"})
            areas.append({"name": "Outlet Mall", "customer_mod": 1.6, "rent_mod": 1.1, "description": "Very high traffic with moderate rent"})
        elif selected_type in ["small_drive_thru", "medium_drive_thru"]:
            areas.append({"name": "Highway Exit", "customer_mod": 1.5, "rent_mod": 0.8, "description": "High drive-by traffic with lower rent"})
            areas.append({"name": "Interstate Junction", "customer_mod": 1.7, "rent_mod": 1.0, "description": "Very high drive-by traffic with moderate rent"})
        elif selected_type == "stadium_vendor":
            areas.append({"name": "Main Concourse", "customer_mod": 1.8, "rent_mod": 1.7, "description": "Premium location with very high event traffic"})
            areas.append({"name": "Upper Level", "customer_mod": 1.3, "rent_mod": 0.9, "description": "Less crowded with lower rent"})
        elif selected_type in ["airport_small_stand", "airport_large_stand"]:
            areas.append({"name": "Main Terminal", "customer_mod": 1.6, "rent_mod": 1.6, "description": "Very high traffic with premium rent"})
            areas.append({"name": "Concourse B", "customer_mod": 1.4, "rent_mod": 1.3, "description": "Good traffic with high rent"})
        elif selected_type == "amusement_park_stand":
            areas.append({"name": "Main Entrance", "customer_mod": 1.7, "rent_mod": 1.7, "description": "Prime location with very high traffic"})
            areas.append({"name": "Thrill Ride Area", "customer_mod": 1.5, "rent_mod": 1.2, "description": "Good location near popular rides"})
        
        # Display area options
        for i, area in enumerate(areas):
            traffic_str = "Low"
            if area["customer_mod"] > 1.5:
                traffic_str = "Very High"
            elif area["customer_mod"] > 1.2:
                traffic_str = "High"
            elif area["customer_mod"] > 0.9:
                traffic_str = "Medium"
            
            rent_str = "Low"
            if area["rent_mod"] > 1.5:
                rent_str = "Very High"
            elif area["rent_mod"] > 1.2:
                rent_str = "High"
            elif area["rent_mod"] > 0.9:
                rent_str = "Medium"
            
            print(f"{i+1}. {area['name']} - Customer Traffic: {traffic_str}, Rent: {rent_str}")
            print(f"   {area['description']}")
        
        print(f"\n{len(areas)+1}. Cancel Purchase")
        
        # Get area choice
        area_choice = input(f"\nSelect an area (1-{len(areas)+1}): ")
        
        if area_choice == str(len(areas)+1):
            return
        
        try:
            area_index = int(area_choice) - 1
            if 0 <= area_index < len(areas):
                selected_area = areas[area_index]
                
                # Calculate final cost with area modifier
                final_cost = type_info["cost"] * selected_area["rent_mod"]
                
                # Confirm purchase
                print(f"\n{Fore.YELLOW}Purchase a {type_info['name']} in {selected_area['name']} for ${final_cost:,.2f}?")
                print(f"{Fore.CYAN}This will be your restaurant's {len(owned_locations)+1} location.")
                confirm = input("\nConfirm purchase (y/n): ")
                
                if confirm.lower() == 'y':
                    # Create new location
                    location_id = f"{selected_area['name'].lower().replace(' ', '_')}_{len(owned_locations)}"
                    new_location = {
                        "id": location_id,
                        "type": selected_type,
                        "name": type_info["name"],
                        "area": selected_area["name"],
                        "area_modifiers": {
                            "customer_mod": selected_area["customer_mod"],
                            "rent_mod": selected_area["rent_mod"]
                        },
                        "floors": 1,
                        "staff_assigned": [],
                        "custom_name": f"{restaurant_name} {selected_area['name']}",
                        "upgrades": [],
                        "decor_level": 1,
                        "kitchen_level": 1,
                        "seating_capacity": 30 if "seating_capacity" not in type_info else type_info["seating_capacity"],
                        "daily_customers": 0,
                        "total_customers": 0,
                        "is_open": False,
                        "maintenance_cost": type_info["maintenance_cost"]
                    }
                    
                    # Add special attributes if present in location type
                    if "special_attributes" in type_info:
                        new_location["special_attributes"] = dict(type_info["special_attributes"])
                    
                    # Purchase location
                    money -= final_cost
                    owned_locations.append(new_location)
                    
                    # Autosave after purchasing a location
                    auto_save(reason="Location Purchase")
                    
                    print(f"\n{Fore.GREEN}Successfully purchased new location!")
                    print(f"Your new {type_info['name']} in {selected_area['name']} is ready for business.")
                    print("Use 'Set Active Location' to start managing this location.")
                    input("Press Enter to continue...")
            else:
                print(f"{Fore.RED}Invalid choice.")
                time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")
            time.sleep(1)
    else:
        print(f"{Fore.RED}Invalid choice.")
        time.sleep(1)

def upgrade_location():
    global money, owned_locations
    
    if not owned_locations:
        print(f"{Fore.RED}You don't own any locations to upgrade.")
        input("Press Enter to continue...")
        return
    
    print_header()
    print(f"{Fore.GREEN}=== UPGRADE LOCATION ===")
    print(f"{Fore.CYAN}Available Funds: ${money:.2f}\n")
    
    # Display owned locations
    print(f"{Fore.YELLOW}Select a location to upgrade:")
    for i, location in enumerate(owned_locations):
        loc_type = location["type"]
        type_info = location_types.get(loc_type, {"name": "Unknown Type"})
        location_name = location["custom_name"] if "custom_name" in location else f"{location['area']} {type_info['name']}"
        print(f"{i+1}. {location_name}")
    
    print(f"\n{len(owned_locations)+1}. Cancel")
    
    # Get location choice
    choice = input(f"\nSelect a location (1-{len(owned_locations)+1}): ")
    
    if choice == str(len(owned_locations)+1):
        return
    
    try:
        loc_index = int(choice) - 1
        if 0 <= loc_index < len(owned_locations):
            location = owned_locations[loc_index]
            loc_type = location["type"]
            type_info = location_types.get(loc_type, {})
            
            # Display upgrade options
            print_header()
            print(f"{Fore.GREEN}=== UPGRADE OPTIONS FOR {location['custom_name'].upper()} ===")
            print(f"{Fore.CYAN}Available Funds: ${money:.2f}\n")
            
            upgrades = []
            
            # 1. Floor expansion if allowed
            if "max_floors" in type_info and location["floors"] < type_info["max_floors"]:
                floor_cost = type_info["cost"] * 0.4 * location["floors"]  # 40% of base cost times current floors
                upgrades.append({"name": "Add Floor", "cost": floor_cost, "type": "floor"})
            
            # 2. Upgrade to next location type if available
            if "upgrades_to" in type_info:
                next_type = type_info["upgrades_to"]
                if next_type in location_types:
                    upgrade_cost = type_info.get("upgrade_cost", location_types[next_type]["cost"] * 0.7)
                    upgrades.append({"name": f"Upgrade to {location_types[next_type]['name']}", 
                                    "cost": upgrade_cost, 
                                    "type": "location_type",
                                    "new_type": next_type})
            
            # 3. Kitchen upgrade
            kitchen_cost = 2000 * location["kitchen_level"]
            upgrades.append({"name": f"Upgrade Kitchen (Level {location['kitchen_level']} → {location['kitchen_level']+1})", 
                           "cost": kitchen_cost, 
                           "type": "kitchen"})
            
            # 4. Decor upgrade
            decor_cost = 1000 * location["decor_level"]
            upgrades.append({"name": f"Upgrade Decor (Level {location['decor_level']} → {location['decor_level']+1})", 
                           "cost": decor_cost, 
                           "type": "decor"})
            
            # 5. Seating capacity
            seating_cost = (location["seating_capacity"] // 10) * 500
            upgrades.append({"name": f"Expand Seating (Capacity {location['seating_capacity']} → {location['seating_capacity']+10})", 
                           "cost": seating_cost, 
                           "type": "seating"})
            
            # Display upgrades
            for i, upgrade in enumerate(upgrades):
                cost_color = Fore.GREEN if money >= upgrade["cost"] else Fore.RED
                print(f"{i+1}. {upgrade['name']} - {cost_color}${upgrade['cost']:,.2f}")
            
            print(f"\n{len(upgrades)+1}. Cancel")
            
            # Get upgrade choice
            upgrade_choice = input(f"\nSelect an upgrade (1-{len(upgrades)+1}): ")
            
            if upgrade_choice == str(len(upgrades)+1):
                return
            
            try:
                upgrade_index = int(upgrade_choice) - 1
                if 0 <= upgrade_index < len(upgrades):
                    selected_upgrade = upgrades[upgrade_index]
                    
                    # Check if can afford
                    if money < selected_upgrade["cost"]:
                        print(f"\n{Fore.RED}You don't have enough money for this upgrade.")
                        input("Press Enter to continue...")
                        return
                    
                    # Confirm upgrade
                    print(f"\n{Fore.YELLOW}Purchase {selected_upgrade['name']} for ${selected_upgrade['cost']:,.2f}?")
                    confirm = input("\nConfirm purchase (y/n): ")
                    
                    if confirm.lower() == 'y':
                        # Apply upgrade
                        money -= selected_upgrade["cost"]
                        
                        if selected_upgrade["type"] == "floor":
                            location["floors"] += 1
                            print(f"\n{Fore.GREEN}Added a new floor to {location['custom_name']}!")
                            print(f"The location now has {location['floors']} floors.")
                        
                        elif selected_upgrade["type"] == "location_type":
                            new_type = selected_upgrade["new_type"]
                            location["type"] = new_type
                            location["name"] = location_types[new_type]["name"]
                            
                            # Update max floors if the new type has more
                            if "max_floors" in location_types[new_type] and location_types[new_type]["max_floors"] > location["floors"]:
                                print(f"\n{Fore.GREEN}Upgraded {location['custom_name']} to a {location_types[new_type]['name']}!")
                                print(f"This location can now have up to {location_types[new_type]['max_floors']} floors.")
                            
                            # Apply special attributes if any
                            if "special_attributes" in location_types[new_type]:
                                location["special_attributes"] = dict(location_types[new_type]["special_attributes"])
                                special_attrs = []
                                for attr in location["special_attributes"]:
                                    special_attrs.append(attr.replace("_", " ").title())
                                print(f"Special features: {', '.join(special_attrs)}")
                        
                        elif selected_upgrade["type"] == "kitchen":
                            location["kitchen_level"] += 1
                            print(f"\n{Fore.GREEN}Upgraded the kitchen at {location['custom_name']} to level {location['kitchen_level']}!")
                            print("Food preparation is now more efficient.")
                        
                        elif selected_upgrade["type"] == "decor":
                            location["decor_level"] += 1
                            print(f"\n{Fore.GREEN}Upgraded the decor at {location['custom_name']} to level {location['decor_level']}!")
                            print("Customer satisfaction will improve.")
                        
                        elif selected_upgrade["type"] == "seating":
                            location["seating_capacity"] += 10
                            print(f"\n{Fore.GREEN}Expanded seating at {location['custom_name']} to {location['seating_capacity']} seats!")
                            print("You can now serve more customers simultaneously.")
                        
                        location["upgrades"].append({
                            "type": selected_upgrade["type"],
                            "name": selected_upgrade["name"],
                            "day_purchased": day
                        })
                        
                        input("Press Enter to continue...")
                else:
                    print(f"{Fore.RED}Invalid choice.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.")
                time.sleep(1)
        else:
            print(f"{Fore.RED}Invalid location selection.")
            time.sleep(1)
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.")
        time.sleep(1)

def rename_location():
    global owned_locations
    
    if not owned_locations:
        print(f"{Fore.RED}You don't own any locations to rename.")
        input("Press Enter to continue...")
        return
    
    print_header()
    print(f"{Fore.GREEN}=== RENAME LOCATION ===\n")
    
    # Display owned locations
    print(f"{Fore.YELLOW}Select a location to rename:")
    for i, location in enumerate(owned_locations):
        location_name = location["custom_name"] if "custom_name" in location else f"{location['area']} {location['name']}"
        print(f"{i+1}. {location_name}")
    
    print(f"\n{len(owned_locations)+1}. Cancel")
    
    # Get location choice
    choice = input(f"\nSelect a location (1-{len(owned_locations)+1}): ")
    
    if choice == str(len(owned_locations)+1):
        return
    
    try:
        loc_index = int(choice) - 1
        if 0 <= loc_index < len(owned_locations):
            location = owned_locations[loc_index]
            
            # Get new name
            print(f"\n{Fore.YELLOW}Current name: {location['custom_name']}")
            new_name = input("Enter new name (or leave blank to cancel): ")
            
            if new_name:
                location["custom_name"] = new_name
                print(f"\n{Fore.GREEN}Location renamed to '{new_name}'!")
                input("Press Enter to continue...")
        else:
            print(f"{Fore.RED}Invalid location selection.")
            time.sleep(1)
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.")
        time.sleep(1)

def set_active_location():
    global owned_locations, current_location_index
    
    if not owned_locations:
        print(f"{Fore.RED}You don't own any locations to set as active.")
        input("Press Enter to continue...")
        return
    
    print_header()
    print(f"{Fore.GREEN}=== SET ACTIVE LOCATION ===\n")
    
    # Display owned locations
    print(f"{Fore.YELLOW}Select a location to make active:")
    for i, location in enumerate(owned_locations):
        prefix = f"{Fore.GREEN}▶ " if i == current_location_index else "  "
        location_name = location["custom_name"] if "custom_name" in location else f"{location['area']} {location['name']}"
        print(f"{prefix}{i+1}. {location_name}")
    
    print(f"\n{len(owned_locations)+1}. Cancel")
    
    # Get location choice
    choice = input(f"\nSelect a location (1-{len(owned_locations)+1}): ")
    
    if choice == str(len(owned_locations)+1):
        return
    
    try:
        loc_index = int(choice) - 1
        if 0 <= loc_index < len(owned_locations):
            current_location_index = loc_index
            
            print(f"\n{Fore.GREEN}Active location set to '{owned_locations[current_location_index]['custom_name']}'!")
            input("Press Enter to continue...")
        else:
            print(f"{Fore.RED}Invalid location selection.")
            time.sleep(1)
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.")
        time.sleep(1)

def sell_location():
    global money, owned_locations, current_location_index
    
    if not owned_locations:
        print(f"{Fore.RED}You don't own any locations to sell.")
        input("Press Enter to continue...")
        return
    
    # Can't sell your only location
    if len(owned_locations) <= 1:
        print(f"{Fore.RED}You cannot sell your only location.")
        input("Press Enter to continue...")
        return
    
    print_header()
    print(f"{Fore.GREEN}=== SELL LOCATION ===\n")
    
    # Display owned locations
    print(f"{Fore.YELLOW}Select a location to sell:")
    for i, location in enumerate(owned_locations):
        # Can't sell active location
        if i == current_location_index:
            print(f"{Fore.RED}▶ {i+1}. {location['custom_name']} (Active - Cannot Sell)")
            continue
        
        location_name = location["custom_name"] if "custom_name" in location else f"{location['area']} {location['name']}"
        
        # Calculate sell value (50% of total investment)
        loc_type = location["type"]
        type_info = location_types.get(loc_type, {"cost": 10000})
        base_value = type_info["cost"]
        
        # Add value for upgrades
        upgrade_value = 0
        for upgrade in location.get("upgrades", []):
            if upgrade["type"] == "floor":
                upgrade_value += base_value * 0.2  # 20% of base cost per floor
            elif upgrade["type"] == "kitchen":
                upgrade_value += 1000 * location["kitchen_level"]
            elif upgrade["type"] == "decor":
                upgrade_value += 500 * location["decor_level"]
            elif upgrade["type"] == "seating":
                upgrade_value += (location["seating_capacity"] - 30) * 250
        
        total_value = (base_value + upgrade_value) * 0.5  # 50% of total value
        
        print(f"  {i+1}. {location_name} - Sell Value: ${total_value:,.2f}")
    
    print(f"\n{len(owned_locations)+1}. Cancel")
    
    # Get location choice
    choice = input(f"\nSelect a location to sell (1-{len(owned_locations)+1}): ")
    
    if choice == str(len(owned_locations)+1):
        return
    
    try:
        loc_index = int(choice) - 1
        if 0 <= loc_index < len(owned_locations):
            # Can't sell active location
            if loc_index == current_location_index:
                print(f"{Fore.RED}You cannot sell your active location.")
                print("Please set another location as active first.")
                input("Press Enter to continue...")
                return
                
            location = owned_locations[loc_index]
            
            # Calculate sell value (same as above)
            loc_type = location["type"]
            type_info = location_types.get(loc_type, {"cost": 10000})
            base_value = type_info["cost"]
            
            upgrade_value = 0
            for upgrade in location.get("upgrades", []):
                if upgrade["type"] == "floor":
                    upgrade_value += base_value * 0.2
                elif upgrade["type"] == "kitchen":
                    upgrade_value += 1000 * location["kitchen_level"]
                elif upgrade["type"] == "decor":
                    upgrade_value += 500 * location["decor_level"]
                elif upgrade["type"] == "seating":
                    upgrade_value += (location["seating_capacity"] - 30) * 250
            
            sell_value = round((base_value + upgrade_value) * 0.5)
            
            # Confirm sale
            print(f"\n{Fore.YELLOW}Sell {location['custom_name']} for ${sell_value:,.2f}?")
            print(f"{Fore.RED}Warning: All staff assigned to this location will be fired.")
            print("This action cannot be undone.")
            confirm = input("\nConfirm sale (y/n): ")
            
            if confirm.lower() == 'y':
                # Remove staff assigned to this location
                for staff_member in location.get("staff_assigned", []):
                    if staff_member in staff:
                        staff.remove(staff_member)
                
                # Sell location
                money += sell_value
                owned_locations.pop(loc_index)
                
                # Adjust current_location_index if needed
                if loc_index < current_location_index:
                    current_location_index -= 1
                elif current_location_index >= len(owned_locations):
                    current_location_index = len(owned_locations) - 1
                
                print(f"\n{Fore.GREEN}Location sold for ${sell_value:,.2f}!")
                input("Press Enter to continue...")
        else:
            print(f"{Fore.RED}Invalid location selection.")
            time.sleep(1)
    except ValueError:
        print(f"{Fore.RED}Please enter a valid number.")
        time.sleep(1)

# View location performance
def view_location_performance():
    pass

# Update game time
def update_game_time(minutes_passed=30):
    global hour, minute, day, day_of_week, week, current_time_period
    
    minute += minutes_passed
    
    # Handle minute overflow
    if minute >= 60:
        hour += minute // 60
        minute = minute % 60
    
    # Handle hour overflow
    if hour >= 24:
        hour = hour % 24
        day += 1
        day_of_week += 1
        
        # Autosave at the start of a new day
        auto_save(reason="Day Change")
        
        # Handle day_of_week overflow
        if day_of_week > 7:
            day_of_week = 1
            week += 1
    
    # Update time period
    new_time_period = get_current_time_period()
    if new_time_period != current_time_period:
        current_time_period = new_time_period
        return True  # Time period changed
    
    return False  # Time period didn't change

def get_current_time_period():
    """Determine current time period based on hour"""
    if 6 <= hour < 11:
        return "morning"
    elif 11 <= hour < 14:
        return "lunch"
    elif 14 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "dinner"
    elif 21 <= hour < 2 or (hour == 2 and minute == 0):
        return "late_night"
    else:  # 2 AM - 6 AM
        return "overnight"

def get_day_name(day_num):
    """Return the name of the day given the day number (1-7)"""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day_num - 1]

def get_formatted_time():
    """Return a formatted time string (12-hour format)"""
    period = "AM" if hour < 12 else "PM"
    hour_12 = hour % 12
    if hour_12 == 0:
        hour_12 = 12
    return f"{hour_12}:{minute:02d} {period}"

def advance_time_dialog():
    """Show a dialog for advancing time"""
    global hour, minute, current_time_period, active_collaborations
    
    while True:
        print_header()
        print(f"{Fore.GREEN}=== TIME MANAGEMENT ===")
        print(f"{Fore.YELLOW}Current Time: {get_formatted_time()} ({get_day_name(day_of_week)})")
        print(f"Current Period: {current_time_period.replace('_', ' ').title()}")
        
        current_period_info = time_of_day[current_time_period]
        print(f"Hours: {current_period_info['hours']}")
        
        if "requires_collaboration" in current_period_info:
            collab_name = current_period_info["requires_collaboration"]
            required_active = collab_name in active_collaborations
            status = f"{Fore.GREEN}Available" if required_active else f"{Fore.RED}Requires {collab_name} Collaboration"
            print(f"Status: {status}")
        
        print(f"\n{Fore.CYAN}What would you like to do?")
        print("1. Advance to next time period")
        print("2. Advance to specific time period")
        print("3. Return to daily menu")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            # Find the next time period
            periods = list(time_of_day.keys())
            current_index = periods.index(current_time_period)
            next_index = (current_index + 1) % len(periods)
            next_period = periods[next_index]
            
            # Check if next period is available
            if "requires_collaboration" in time_of_day[next_period]:
                required_collab = time_of_day[next_period]["requires_collaboration"]
                if required_collab not in active_collaborations:
                    print(f"\n{Fore.RED}You can't advance to {next_period.replace('_', ' ').title()} period.")
                    print(f"You need the {required_collab} collaboration to operate during this time.")
                    input("Press Enter to continue...")
                    continue
            
            # Calculate time difference to next period
            target_hour = 0
            
            if next_period == "morning":
                target_hour = 6
            elif next_period == "lunch":
                target_hour = 11
            elif next_period == "afternoon":
                target_hour = 14
            elif next_period == "dinner":
                target_hour = 17
            elif next_period == "late_night":
                target_hour = 21
            elif next_period == "overnight":
                target_hour = 2
            
            # Calculate minutes to advance
            minutes_to_advance = 0
            
            # Handle day boundary
            if target_hour < hour:
                minutes_to_advance = (24 - hour + target_hour) * 60 - minute
            else:
                minutes_to_advance = (target_hour - hour) * 60 - minute
            
            if minutes_to_advance <= 0:
                minutes_to_advance += 24 * 60  # Add a full day
            
            # Confirm time advance
            hours_to_advance = minutes_to_advance // 60
            mins_remaining = minutes_to_advance % 60
            
            time_str = ""
            if hours_to_advance > 0:
                time_str += f"{hours_to_advance} hour{'s' if hours_to_advance != 1 else ''}"
            if mins_remaining > 0:
                if time_str:
                    time_str += " and "
                time_str += f"{mins_remaining} minute{'s' if mins_remaining != 1 else ''}"
            
            print(f"\n{Fore.YELLOW}Advance time by {time_str} to reach {next_period.replace('_', ' ').title()} period?")
            confirm = input("Confirm (y/n): ")
            
            if confirm.lower() == 'y':
                update_game_time(minutes_to_advance)
                print(f"\n{Fore.GREEN}Time advanced to {get_formatted_time()} ({get_day_name(day_of_week)})")
                print(f"You are now in the {current_time_period.replace('_', ' ').title()} period.")
                input("Press Enter to continue...")
                break
            
        elif choice == "2":
            print_header()
            print(f"{Fore.GREEN}=== SELECT TIME PERIOD ===")
            print(f"{Fore.YELLOW}Current Time: {get_formatted_time()} ({get_day_name(day_of_week)})")
            
            # List available time periods
            available_periods = []
            for i, (period_name, period_info) in enumerate(time_of_day.items(), 1):
                is_available = True
                status = ""
                
                if "requires_collaboration" in period_info:
                    required_collab = period_info["requires_collaboration"]
                    if required_collab not in active_collaborations:
                        is_available = False
                        status = f" {Fore.RED}(Requires {required_collab} Collaboration)"
                
                period_display = period_name.replace('_', ' ').title()
                if is_available:
                    available_periods.append(period_name)
                    print(f"{i}. {period_display} - {period_info['hours']}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}{i}. {period_display} - {period_info['hours']}{status}")
            
            print(f"\n{len(time_of_day) + 1}. Cancel")
            
            # Get period choice
            choice = input(f"\nSelect a time period to advance to (1-{len(time_of_day) + 1}): ")
            
            if choice == str(len(time_of_day) + 1):
                continue
                
            try:
                period_index = int(choice) - 1
                if 0 <= period_index < len(time_of_day):
                    selected_period = list(time_of_day.keys())[period_index]
                    
                    # Check if period is available
                    if selected_period not in available_periods:
                        print(f"\n{Fore.RED}This time period is not available.")
                        input("Press Enter to continue...")
                        continue
                    
                    # Calculate target hour for selected period
                    target_hour = 0
                    
                    if selected_period == "morning":
                        target_hour = 8  # Middle of morning period
                    elif selected_period == "lunch":
                        target_hour = 12  # Middle of lunch period
                    elif selected_period == "afternoon":
                        target_hour = 15  # Middle of afternoon period
                    elif selected_period == "dinner":
                        target_hour = 19  # Middle of dinner period
                    elif selected_period == "late_night":
                        target_hour = 23  # Middle of late night period
                    elif selected_period == "overnight":
                        target_hour = 4   # Middle of overnight period
                    
                    # Calculate minutes to advance
                    minutes_to_advance = 0
                    
                    # Handle day boundary
                    if target_hour < hour or (target_hour == hour and minute > 30):
                        minutes_to_advance = (24 - hour + target_hour) * 60 - minute
                    else:
                        minutes_to_advance = (target_hour - hour) * 60 - minute
                    
                    if minutes_to_advance <= 0:
                        minutes_to_advance += 24 * 60  # Add a full day
                    
                    # Confirm time advance
                    hours_to_advance = minutes_to_advance // 60
                    mins_remaining = minutes_to_advance % 60
                    
                    time_str = ""
                    if hours_to_advance > 0:
                        time_str += f"{hours_to_advance} hour{'s' if hours_to_advance != 1 else ''}"
                    if mins_remaining > 0:
                        if time_str:
                            time_str += " and "
                        time_str += f"{mins_remaining} minute{'s' if mins_remaining != 1 else ''}"
                    
                    print(f"\n{Fore.YELLOW}Advance time by {time_str} to reach {selected_period.replace('_', ' ').title()} period?")
                    confirm = input("Confirm (y/n): ")
                    
                    if confirm.lower() == 'y':
                        update_game_time(minutes_to_advance)
                        print(f"\n{Fore.GREEN}Time advanced to {get_formatted_time()} ({get_day_name(day_of_week)})")
                        print(f"You are now in the {current_time_period.replace('_', ' ').title()} period.")
                        input("Press Enter to continue...")
                        break
                else:
                    print(f"{Fore.RED}Invalid choice.")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.")
                time.sleep(1)
                
        elif choice == "3":
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(1)

# Open restaurant for business
def open_restaurant():
    global money, day, inventory, daily_sales, reputation, hour, minute, current_time_period
    global owned_locations, current_location_index, active_collaborations
    
    # Get the current active location
    current_location = owned_locations[current_location_index]
    location_name = current_location["custom_name"]
    
    # Check if the location is already open
    if current_location.get("is_open", False):
        print(f"{Fore.RED}{location_name} is already open for business!")
        input("Press Enter to continue...")
        return
    
    # Check which time period we're in and if it's available
    if "requires_collaboration" in time_of_day[current_time_period]:
        required_collab = time_of_day[current_time_period]["requires_collaboration"]
        if required_collab not in active_collaborations:
            print(f"{Fore.RED}You can't open during {current_time_period.replace('_', ' ').title()} period!")
            print(f"You need the {required_collab} collaboration to operate during this time.")
            input("Press Enter to continue...")
            return
    
    # Check if location has special time restrictions
    if "special_attributes" in current_location:
        if "event_day_only" in current_location["special_attributes"] and current_location["special_attributes"]["event_day_only"]:
            # For stadium vendors - check if there's an event today
            is_event_day = (day_of_week == 3 or day_of_week == 6)  # Events on Wednesdays and Saturdays
            if not is_event_day:
                print(f"{Fore.RED}There's no event at the stadium today!")
                print("Stadium vendors can only open on event days (Wednesdays and Saturdays).")
                input("Press Enter to continue...")
                return
    
    # Check if enough ingredients
    if inventory["patties"] < 10 or inventory["buns"] < 10:
        print(f"{Fore.RED}You don't have enough basic ingredients to open!")
        print("Make sure you have at least 10 patties and 10 buns.")
        input("Press Enter to continue...")
        return
    
    # Check if enough staff assigned to this location
    staff_at_location = len(current_location.get("staff_assigned", []))
    min_staff_needed = 2  # At least need 1 cook and 1 cashier
    
    if staff_at_location < min_staff_needed:
        print(f"{Fore.RED}You don't have enough staff to open this location!")
        print(f"You need at least {min_staff_needed} staff members (at least 1 cook and 1 cashier).")
        
        # Check if the player has staff but hasn't assigned them
        if len(staff) >= min_staff_needed:
            print(f"{Fore.YELLOW}You have {len(staff)} staff members, but they need to be assigned to this location.")
            print("Use 'Manage Staff' to assign staff to this location.")
        else:
            print(f"{Fore.YELLOW}You only have {len(staff)} staff members. Use 'Hire Staff' to hire more staff.")
        
        input("Press Enter to continue...")
        return
    
    # Get the location type and its base customers
    loc_type = current_location["type"]
    type_info = location_types.get(loc_type, {"base_customers": 50})
    
    # Base customers from location type
    base_customers = type_info.get("base_customers", 50)
    
    # Apply area modifier
    if "area_modifiers" in current_location and "customer_mod" in current_location["area_modifiers"]:
        base_customers *= current_location["area_modifiers"]["customer_mod"]
    
    # Apply time period modifier
    time_period_info = time_of_day[current_time_period]
    time_customer_mod = time_period_info.get("customer_modifier", 1.0)
    expected_customers = base_customers * time_customer_mod
    
    # Apply day of week modifications
    day_modifier = 1.0
    if day_of_week == 6 or day_of_week == 7:  # Weekend
        day_modifier = 1.3  # 30% more customers on weekends
    expected_customers *= day_modifier
    
    # Factor in reputation
    reputation_modifier = 1.0 + (reputation - 3.0) * 0.1
    expected_customers *= reputation_modifier
    
    # Factor in staff quality
    staff_modifier = 1.0
    staff_at_location = current_location.get("staff_assigned", [])
    if staff_at_location:
        # Find these staff members in the staff list
        location_staff = [s for s in staff if s["id"] in staff_at_location]
        if location_staff:
            total_skill = sum(s["skill_level"] for s in location_staff)
            avg_skill = total_skill / len(location_staff)
            staff_modifier = 0.8 + (avg_skill * 0.1)  # 0.8 to 1.3 based on skill 0-5
            expected_customers *= staff_modifier
    
    # Factor in marketing if any
    marketing_modifier = 1.0 + (active_marketing * 0.05)
    expected_customers *= marketing_modifier
    
    # Factor in special location attributes
    if "special_attributes" in current_location:
        for attr, value in current_location["special_attributes"].items():
            if attr == "premium_pricing" and isinstance(value, (int, float)):
                # Premium pricing increases revenue but slightly decreases customers
                expected_customers *= 0.9
            elif attr == "captive_audience" and isinstance(value, (int, float)):
                expected_customers *= value
            elif attr == "high_volume" and value:
                expected_customers *= 1.5
    
    # Factor in special time period effects
    if "special_effects" in time_period_info:
        if "business_lunch_rush" in time_period_info["special_effects"] and current_time_period == "lunch":
            if "downtown" in current_location["area"].lower() or "business district" in current_location["area"].lower():
                expected_customers *= time_period_info["special_effects"]["business_lunch_rush"]
    
    # Calculate opening duration based on time period
    period_durations = {
        "morning": 5,  # 5 hours (6am-11am)
        "lunch": 3,    # 3 hours (11am-2pm)
        "afternoon": 3, # 3 hours (2pm-5pm)
        "dinner": 4,    # 4 hours (5pm-9pm)
        "late_night": 5, # 5 hours (9pm-2am)
        "overnight": 4  # 4 hours (2am-6am)
    }
    
    duration_hours = period_durations.get(current_time_period, 4)
    
    # Round to a good integer value
    expected_customers = int(expected_customers)
    
    # Add some variability
    expected_customers = random.randint(int(expected_customers * 0.9), int(expected_customers * 1.1))
    
    print(f"{Fore.GREEN}Opening {location_name} for business during {current_time_period.replace('_', ' ')}!")
    print(f"Current time: {get_formatted_time()} on {get_day_name(day_of_week)}, Day {day}")
    print(f"Expecting approximately {expected_customers} customers over the next {duration_hours} hours.")
    input("Press Enter to start serving...")
    
    # Initialize daily sales
    daily_sales = {recipe: 0 for recipe in recipes}
    total_money_earned = 0
    total_reputation_change = 0
    
    # Initialize customer tracking
    customers_seen = 0
    
    # Set location as open
    current_location["is_open"] = True
    
    # Serve customers over time
    for i in range(expected_customers):
        # Every few customers, time passes
        if i > 0 and i % 5 == 0:
            time_increment = (duration_hours * 60) // (expected_customers // 5)
            time_changed = update_game_time(time_increment)
            
            # If time period changes during service, break early
            if time_changed:
                remaining = expected_customers - i
                print(f"\n{Fore.YELLOW}Time has advanced to {current_time_period.replace('_', ' ').title()} period.")
                print(f"Approximately {remaining} potential customers were lost due to the time change.")
                break
        
        customer_result = serve_customer(i+1, expected_customers)
        if customer_result:
            money_earned, reputation_change = customer_result
            total_money_earned += money_earned
            total_reputation_change += reputation_change
            customers_seen = i  # Update customers seen counter
    
    # End of service summary
    clear()
    print_header()
    print(f"{Fore.GREEN}=== END OF SERVICE SUMMARY ===")
    print(f"{Fore.YELLOW}Location: {location_name}")
    print(f"Time Period: {current_time_period.replace('_', ' ').title()}")
    print(f"Current Time: {get_formatted_time()} on {get_day_name(day_of_week)}, Day {day}")
    
    print(f"\n{Fore.YELLOW}Financial Results:")
    print(f"Total Revenue: ${total_money_earned:.2f}")
    
    # Calculate expenses for this service period
    staff_at_location = current_location.get("staff_assigned", [])
    location_staff = [s for s in staff if s["id"] in staff_at_location]
    staff_wages = sum(s.get("salary", 0) for s in location_staff) * (duration_hours / 24)  # Prorated for time period
    
    # Calculate rent and utilities based on location
    rent = current_location.get("maintenance_cost", 100) * (duration_hours / 24)  # Prorated for time period
    utilities = (25 + (len(location_staff) * 5)) * (duration_hours / 24)  # Prorated for time period
    
    print(f"Staff Wages: ${staff_wages:.2f}")
    print(f"Rent/Maintenance: ${rent:.2f}")
    print(f"Utilities: ${utilities:.2f}")
    
    period_profit = total_money_earned - staff_wages - rent - utilities
    profit_color = Fore.GREEN if period_profit >= 0 else Fore.RED
    print(f"Period Profit: {profit_color}${period_profit:.2f}")
    
    # Update money
    money += period_profit
    
    # Update customer counters for the location
    customers_served = min(customers_seen + 1, expected_customers)
    current_location["daily_customers"] = customers_served
    current_location["total_customers"] = current_location.get("total_customers", 0) + customers_served
    
    # Set location as closed
    current_location["is_open"] = False
    
    # Reputation change
    if customers_served > 0:
        reputation += total_reputation_change / customers_served
        reputation = max(1.0, min(5.0, reputation))  # Clamp between 1-5
        
        rep_change_str = f"+{total_reputation_change/customers_served:.2f}" if total_reputation_change >= 0 else f"{total_reputation_change/customers_served:.2f}"
        rep_color = Fore.GREEN if total_reputation_change >= 0 else Fore.RED
        print(f"\nReputation Change: {rep_color}{rep_change_str}")
        print(f"Current Reputation: {Fore.YELLOW}{reputation:.1f}/5.0")
    
    # Sales breakdown
    print(f"\n{Fore.CYAN}Sales Breakdown:")
    for recipe, count in daily_sales.items():
        if count > 0:
            revenue = count * prices.get(recipe, 0)
            print(f"{recipe.replace('_', ' ').title()}: {count} sold (${revenue:.2f})")
    
    # Check for level up
    if check_level_up():
        print(f"\n{Fore.GREEN}Congratulations! Your restaurant has leveled up!")
        print(f"You are now level {restaurant_level}.")
    
    # Autosave after completing a business day
    auto_save(reason="Business Day Completed")
    
    input("\nPress Enter to continue...")

# Check for level up 
def check_level_up():
    global restaurant_level, reputation, day
    
    # Define level thresholds based on a combination of factors
    level_requirements = {
        2: {"days": 3, "reputation": 3.2, "locations": 1},
        3: {"days": 7, "reputation": 3.5, "locations": 1},
        4: {"days": 14, "reputation": 3.7, "locations": 1},
        5: {"days": 21, "reputation": 4.0, "locations": 1},
        6: {"days": 30, "reputation": 4.1, "locations": 2},
        7: {"days": 45, "reputation": 4.2, "locations": 2},
        8: {"days": 60, "reputation": 4.3, "locations": 2},
        9: {"days": 75, "reputation": 4.4, "locations": 3},
        10: {"days": 90, "reputation": 4.5, "locations": 3},
        # Additional levels with higher requirements
        11: {"days": 105, "reputation": 4.6, "locations": 3},
        12: {"days": 120, "reputation": 4.6, "locations": 4},
        13: {"days": 135, "reputation": 4.7, "locations": 4},
        14: {"days": 150, "reputation": 4.7, "locations": 4},
        15: {"days": 180, "reputation": 4.8, "locations": 5},
        # End-game levels with very high requirements
        16: {"days": 210, "reputation": 4.8, "locations": 5},
        17: {"days": 240, "reputation": 4.8, "locations": 6},
        18: {"days": 270, "reputation": 4.9, "locations": 6},
        19: {"days": 300, "reputation": 4.9, "locations": 7},
        20: {"days": 365, "reputation": 5.0, "locations": 7}
    }
    
    # Check if the restaurant qualifies for the next level
    next_level = restaurant_level + 1
    if next_level in level_requirements:
        req = level_requirements[next_level]
        
        # Check all criteria
        days_met = day >= req["days"]
        reputation_met = reputation >= req["reputation"]
        locations_met = len(owned_locations) >= req["locations"]
        
        if days_met and reputation_met and locations_met:
            restaurant_level = next_level
            
            # Autosave when leveling up
            auto_save(reason="Level Up")
            
            return True
    
    return False

# Calculate daily costs
def calculate_daily_costs():
    pass

# Serve customer
def serve_customer(customer_num=1, total_customers=1):
    global inventory, daily_sales, current_location_index, current_time_period
    
    # Calculate staff efficiency based on customer number and total customers
    efficiency = calculate_staff_efficiency(customer_num, total_customers)
    
    # Print customer info
    if customer_num % 10 == 0:  # Only show every 10th customer to avoid spam
        print(f"\nCustomer #{customer_num}/{total_customers} arrives...")
    
    # Determine customer preferences based on time period
    time_period_info = time_of_day[current_time_period]
    popular_items = time_period_info.get("popular_items", [])
    
    # Determine what the customer wants to order
    available_items = [recipe for recipe in recipes.keys() if all(inventory.get(ingredient, 0) >= quantity for ingredient, quantity in recipes[recipe].items() if ingredient != "preparation_time")]
    
    if not available_items:
        if customer_num % 5 == 0:  # Only show occasionally
            print(f"{Fore.RED}No items available to serve! Customer leaves disappointed.")
        return None
    
    # Bias toward popular items for this time period
    weighted_items = available_items.copy()
    for popular in popular_items:
        if popular in available_items:
            # Add popular items multiple times to increase their probability
            weighted_items.extend([popular] * 3)
    
    # Customer selects an item
    selected_item = random.choice(weighted_items)
    
    # Check if we have all ingredients for this item
    can_make = True
    for ingredient, quantity in recipes[selected_item].items():
        if ingredient == "preparation_time":
            continue
        if inventory.get(ingredient, 0) < quantity:
            can_make = False
            break
    
    if not can_make:
        if customer_num % 5 == 0:  # Only show occasionally
            print(f"{Fore.YELLOW}Cannot make {selected_item.replace('_', ' ').title()} - out of ingredients!")
        return None
    
    # Make the food item
    preparation_time = recipes[selected_item].get("preparation_time", 60)  # Default 60 seconds if not specified
    
    # Apply staff efficiency to preparation time - we'll use this value
    effective_prep_time = preparation_time / efficiency
    
    # Only show detailed preparation occasionally
    if customer_num % 10 == 0:
        print(f"{Fore.CYAN}Preparing {selected_item.replace('_', ' ').title()}... (Est. Time: {effective_prep_time:.1f}s)")
        
        # Apply special time period effects to food quality
        quality_modifier = 1.0
        if "special_effects" in time_period_info:
            if "breakfast_items_boost" in time_period_info["special_effects"] and "breakfast" in selected_item:
                quality_modifier *= time_period_info["special_effects"]["breakfast_items_boost"]
            elif "dessert_boost" in time_period_info["special_effects"] and selected_item in ["ice_cream_cone", "milkshake", "sundae"]:
                quality_modifier *= time_period_info["special_effects"]["dessert_boost"]
        
        quality = random.uniform(0.7, 1.0) * efficiency * quality_modifier
        quality_str = "Excellent" if quality > 0.9 else "Good" if quality > 0.7 else "Average"
        print(f"Quality: {quality_str} ({quality:.2f})")
    
    # Use ingredients
    for ingredient, quantity in recipes[selected_item].items():
        if ingredient == "preparation_time":
            continue
        inventory[ingredient] -= quantity
    
    # Calculate money earned
    item_price = prices.get(selected_item, 5.0)  # Default $5 if price not set
    
    # Apply special modifiers based on location attributes
    active_location = owned_locations[current_location_index]
    if "special_attributes" in active_location:
        if "premium_pricing" in active_location["special_attributes"]:
            premium_factor = active_location["special_attributes"]["premium_pricing"]
            item_price *= premium_factor
    
    # Apply time period effects on pricing
    if "special_effects" in time_period_info:
        if "premium_pricing" in time_period_info["special_effects"]:
            item_price *= time_period_info["special_effects"]["premium_pricing"]
    
    # Apply celebrity endorsement effects if any are active
    for endorsement in active_endorsements:
        if "active_until_day" in endorsement and day <= endorsement["active_until_day"]:
            celeb_data = celebrity_endorsements[endorsement["id"]]
            if "benefits" in celeb_data:
                # Apply price boost for their special item if this is it
                if "special_item" in celeb_data["benefits"] and celeb_data["benefits"]["special_item"] == selected_item:
                    item_price *= 1.5  # 50% premium on celebrity endorsed items
    
    # Record the sale
    daily_sales[selected_item] = daily_sales.get(selected_item, 0) + 1
    
    # Calculate reputation impact
    # Factors: food quality, price-value perception, staff efficiency
    reputation_impact = random.uniform(-0.1, 0.3) * efficiency
    if efficiency > 1.1:  # Great service
        reputation_impact += 0.1
    
    if customer_num % 10 == 0:  # Only show occasionally
        print(f"{Fore.GREEN}Customer purchased {selected_item.replace('_', ' ').title()} for ${item_price:.2f}")
    
    return item_price, reputation_impact

# Calculate staff efficiency
def calculate_staff_efficiency(current_customer, total_customers):
    # Base efficiency is 1.0
    base_efficiency = 1.0
    
    # Adjust based on how many customers we've served today (fatigue factor)
    fatigue_factor = 1.0 - (current_customer / total_customers * 0.3)  # Up to 30% efficiency loss due to fatigue
    
    # Consider staff skills, specialties, and automation
    staff_bonus = 0
    for employee in staff:
        if employee["role"] == "cook":
            # Cooks directly affect food preparation efficiency
            bonus = 0.05 * employee["level"]  # 5% bonus per level
            
            # Add specialty bonus
            if "specialty" in employee and employee["specialty"] == "Burgers":
                bonus += 0.1  # 10% bonus for burger specialists
            
            # Add automation bonus
            if "automation_level" in employee:
                bonus += 0.1 * employee["automation_level"]  # 10-30% automation bonus
                
            staff_bonus += bonus * employee["performance"]  # Scale by performance
            
    # Apply fatigue factor to base efficiency
    final_efficiency = base_efficiency * fatigue_factor + staff_bonus
    
    # Ensure efficiency is within reasonable bounds
    return max(0.5, min(1.5, final_efficiency))

# Go shopping
def go_shopping():
    global money
    
    # Organize ingredients by category
    categories = {
        "Burger Ingredients": [
            "buns", "patties", "lettuce", "tomato", "cheese", "pickles", 
            "onions", "ketchup", "mustard", "mayo", "bacon", "premium_buns", 
            "angus_beef", "avocado", "gourmet_cheese"
        ],
        "Side Ingredients": [
            "potatoes", "onion_bulbs", "batter", "seasoning", "cooking_oil", 
            "poutine_cheese", "gravy_mix"
        ],
        "Beverage Ingredients": [
            "4ndycola_syrup", "root_beer_syrup", "orange_soda_syrup", 
            "lemon_lime_syrup", "coffee_beans", "milk", "ice_cream_mix"
        ],
        "Dessert Ingredients": [
            "cookie_dough", "brownie_mix", "apple_pie_filling", "sugar", 
            "chocolate_sauce"
        ]
    }
    
    while True:
        print_header()
        print(f"{Fore.GREEN}=== SHOPPING ===")
        print(f"{Fore.CYAN}Money: ${money:.2f}\n")
        
        print(f"{Fore.YELLOW}Select a category:")
        print("1. Burger Ingredients")
        print("2. Side Ingredients")
        print("3. Beverage Ingredients")
        print("4. Dessert Ingredients")
        print("5. Return to Daily Menu")
        
        category_choice = input("\nEnter your choice (1-5): ")
        
        if category_choice == "5":
            break
        
        category_map = {
            "1": "Burger Ingredients",
            "2": "Side Ingredients",
            "3": "Beverage Ingredients",
            "4": "Dessert Ingredients"
        }
        
        if category_choice not in category_map:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)
            continue
        
        selected_category = category_map[category_choice]
        
        while True:
            print_header()
            print(f"{Fore.GREEN}=== SHOPPING: {selected_category} ===")
            print(f"{Fore.CYAN}Money: ${money:.2f}\n")
            
            # Display ingredient costs and current inventory for selected category
            print(f"{Fore.YELLOW}Available Ingredients:")
            
            i = 1
            items = {}
            
            for item in categories[selected_category]:
                if item in costs:
                    items[str(i)] = item
                    display_name = item.replace('_', ' ').capitalize()
                    print(f"{i}. {display_name} - ${costs[item]:.2f} each (Current: {inventory[item]})")
                    i += 1
            
            print(f"\n{Fore.CYAN}{i}. Return to category selection")
            
            # Get item to purchase
            choice = input("\nSelect an item to buy (1-" + str(i) + "): ")
            
            if choice == str(i):
                break
            
            if choice in items:
                item = items[choice]
                display_name = item.replace('_', ' ')
                
                # Apply supply chain optimization if researched
                item_cost = costs[item]
                if "supply_chain_optimization" in restaurant_upgrades.get("research", []):
                    item_cost *= 0.85
                    discount_active = True
                else:
                    discount_active = False
                    
                # Apply distributor discounts if applicable
                if item in distributor_discounts:
                    item_cost *= (1 - distributor_discounts[item])
                    distributor_discount_active = True 
                else:
                    distributor_discount_active = False
                
                max_buy = int(money / item_cost)
                
                if max_buy <= 0:
                    print(f"\n{Fore.RED}You don't have enough money to buy any {display_name}!")
                    input("Press Enter to continue...")
                    continue
                
                if discount_active:
                    print(f"{Fore.GREEN}Supply chain optimization: 15% discount applied!")
                    
                if distributor_discount_active:
                    discount_percent = distributor_discounts[item] * 100
                    print(f"{Fore.GREEN}Distributor discount: {discount_percent:.0f}% off!")
                
                print(f"\nHow many {display_name}s do you want to buy? (max: {max_buy})")
                try:
                    amount = int(input())
                    if amount <= 0:
                        print(f"{Fore.RED}Please enter a positive number.")
                        time.sleep(1)
                        continue
                    
                    if amount > max_buy:
                        print(f"{Fore.RED}You can only afford {max_buy}.")
                        time.sleep(1)
                        continue
                    
                    cost = amount * item_cost
                    
                    money -= cost
                    inventory[item] += amount
                    
                    print(f"\n{Fore.GREEN}Purchased {amount} {display_name}s for ${cost:.2f}")
                    input("Press Enter to continue...")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.")
                    time.sleep(1)
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")
                time.sleep(1)

# Check inventory
def check_inventory():
    pass

# View recipes
def view_recipes():
    pass

# View burger recipes
def view_burger_recipes():
    pass

# View side recipes
def view_side_recipes():
    pass

# View beverage recipes
def view_beverage_recipes():
    pass

# View dessert recipes
def view_dessert_recipes():
    pass

# View combo meals
def view_combo_meals():
    pass

# Main game function
def main_game():
    # Check if run directly
    if __name__ == "__main__":
        check_launcher()
        
    # Initialize colorama
    init(autoreset=True)
    
    # Display main menu
    main_menu()

# Run the game
main_game()
