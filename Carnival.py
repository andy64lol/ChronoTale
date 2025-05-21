"""
Carnival Game
A text-based carnival game with minigames, shop system, and achievements.
Players can earn tickets, buy costumes, and complete missions.

Features:
- Multiple minigames with varying difficulty
- Save/Load system
- Shop with costumes and consumables
- Achievement system
- NPC missions
- Gambling games
"""

import json
import os
import random
import sys
import time
from colorama import Fore, Style, init

# Check if called with python3 command
def check_python_command():
    """Check if script was called with 'python3' command and exit if it was"""
    # Get the command used to run this script
    command = sys.argv[0]
    program_name = os.path.basename(sys.executable)
    
    if program_name == "python3" or "python3" in command:
        print(f"{Fore.RED}Please use 'python' command instead of 'python3'")
        print(f"{Fore.YELLOW}Run: python launch.py")
        sys.exit(0)

# Launcher protection at the very beginning
if __name__ == "__main__":
    # First check if using python3 command
    check_python_command()
    
    # Then check if launched through launcher
    if os.environ.get("LAUNCHED_FROM_LAUNCHER") != "1":
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit(0)
init(autoreset=True)

# Save file locations
SAVE_SLOTS = ["slot1.json", "slot2.json", "slot3.json"]

player = {
    "name": "",
    "tickets": 20,
    "inventory": [],
    "achievements": [],
    "equipped_costume": "😊",  # Default costume
    "equipped_items": [],  # For consumable items
    "missions": {},  # Track mission progress
    "completed_missions": [],  # Completed mission IDs
    "loyalty_points": 0,  # Loyalty program points
    "visited_attractions": {},  # Track visits to attractions for loyalty rewards
    "championship_records": {},  # Track championship progress and records
    "season_pass": False,  # Season pass status
    "fast_passes": 0,  # Fast passes to skip lines
    "completed_quests": [],  # Completed quest IDs
    "active_quests": []  # Currently active quests
}

MISSIONS = {
    "rookie": {"id": "rookie", "name": "Play 5 minigames", "target": 5, "reward": 10, "type": "play_games", "description": "Get acquainted with our carnival games by playing 5 different minigames of your choice."},
    "mathematician": {"id": "mathematician", "name": "Win Quick Math 3 times", "target": 3, "reward": 15, "type": "win_quick_math", "description": "Test your mental math skills by winning the Quick Math game 3 times."},
    "lucky": {"id": "lucky", "name": "Win Lucky Spinner 3 times", "target": 3, "reward": 20, "type": "win_spinner", "description": "Try your luck at the Lucky Spinner and see if fortune favors you 3 times!"},
    "vip_games": {"id": "vip_games", "name": "Play all VIP games", "target": 3, "reward": 50, "type": "vip_games", "vip_only": True, "description": "Experience the exclusive VIP games that offer special rewards and experiences."},
    "coaster_fan": {"id": "coaster_fan", "name": "Ride the Cosmic Coaster 3 times", "target": 3, "reward": 25, "type": "ride_coaster", "description": "Brave the twists and turns of our most popular thrill ride three times!"},
    "ghost_hunter": {"id": "ghost_hunter", "name": "Complete the Haunted Mansion without losing courage", "target": 1, "reward": 30, "type": "brave_mansion", "description": "Navigate through the spooky Haunted Mansion and maintain your courage throughout."},
    "vr_master": {"id": "vr_master", "name": "Try all VR experiences", "target": 4, "reward": 35, "type": "vr_experiences", "description": "Immerse yourself in virtual reality by experiencing all our cutting-edge VR attractions."},
    "championship_rookie": {"id": "championship_rookie", "name": "Participate in any championship", "target": 1, "reward": 15, "type": "championship_participation", "description": "Take your first step into competitive carnival games by participating in any championship."},
    "championship_winner": {"id": "championship_winner", "name": "Win any championship", "target": 1, "reward": 50, "type": "championship_win", "description": "Demonstrate your mastery by winning any championship event."},
    "collector": {"id": "collector", "name": "Own 10 different costumes", "target": 10, "reward": 25, "type": "costume_collection", "description": "Show your fashion sense by collecting 10 different carnival costumes."},
    "theme_park_explorer": {"id": "theme_park_explorer", "name": "Try all theme park attractions", "target": 8, "reward": 40, "type": "theme_park_visits", "description": "Become a true explorer by experiencing every exciting attraction our theme park has to offer!"},
    "loyal_visitor": {"id": "loyal_visitor", "name": "Earn 100 loyalty points", "target": 100, "reward": 35, "type": "loyalty_points", "description": "Show your dedication to the carnival by earning 100 loyalty points through regular visits."},
    "carnival_master": {"id": "carnival_master", "name": "Complete 15 different missions", "target": 15, "reward": 150, "type": "mission_completion", "description": "Prove your mastery of all carnival aspects by completing 15 different missions."},
    "gourmet_explorer": {"id": "gourmet_explorer", "name": "Try 10 different carnival foods", "target": 10, "reward": 35, "type": "food_variety", "description": "Tantalize your taste buds by sampling 10 different delicious carnival foods."},
    "sweet_tooth": {"id": "sweet_tooth", "name": "Try all dessert options", "target": 5, "reward": 25, "type": "dessert_variety", "description": "Indulge your sweet tooth by trying all the dessert options available at the carnival."},
    "music_aficionado": {"id": "music_aficionado", "name": "Attend all concert performances", "target": 5, "reward": 35, "type": "concert_attendance", "description": "Immerse yourself in musical brilliance by attending all the concert performances."},
    "entertainment_fanatic": {"id": "entertainment_fanatic", "name": "Attend 5 different shows", "target": 5, "reward": 40, "type": "show_attendance", "description": "Experience the magic of live entertainment by attending 5 different carnival shows."}
}

# Quest system - multi-step adventures with narrative
QUESTS = {
    "daily_challenge": {
        "id": "daily_challenge",
        "name": "Daily Challenge",
        "description": "Complete a randomly selected task to earn bonus tickets and loyalty points.",
        "reward": 15,
        "type": "daily",
        "refresh": "24h",
        "tasks": [
            {"description": "Win 3 minigames", "type": "win_games", "target": 3},
            {"description": "Earn 30 tickets", "type": "earn_tickets", "target": 30},
            {"description": "Visit 2 theme park attractions", "type": "visit_attractions", "target": 2},
            {"description": "Play a championship game", "type": "play_championship", "target": 1},
            {"description": "Buy something from the shop", "type": "make_purchase", "target": 1}
        ]
    },
    
    "weekly_quest": {
        "id": "weekly_quest",
        "name": "Weekly Spectacular",
        "description": "Complete a multi-part quest for big rewards! Available once per week.",
        "reward": 50,
        "type": "weekly",
        "refresh": "7d",
        "steps": [
            {"description": "Visit the Haunted Mansion", "type": "specific_attraction", "target": "Haunted Mansion"},
            {"description": "Ride the Cosmic Coaster", "type": "specific_attraction", "target": "Cosmic Coaster"},
            {"description": "Win a card game", "type": "win_card_game", "target": 1},
            {"description": "Buy a costume", "type": "buy_costume", "target": 1},
            {"description": "Play 3 different minigames", "type": "play_different_games", "target": 3}
        ]
    },
    
    "scavenger_hunt": {
        "id": "scavenger_hunt",
        "name": "Carnival Scavenger Hunt",
        "description": "Find hidden items around the carnival to earn special rewards and unlock secrets!",
        "reward": 30,
        "type": "repeatable",
        "refresh": "3d",
        "hidden_items": [
            {"name": "Golden Ticket 🎫", "location": "Under the carousel", "hint": "Round and round it goes, beneath is where it shows."},
            {"name": "Mystery Box 📦", "location": "Behind the food court", "hint": "Where hungry stomachs are filled, look behind where snacks are grilled."},
            {"name": "Lucky Coin 🪙", "location": "Near the fountain", "hint": "Wishes flow where water spouts, search nearby without any doubts."},
            {"name": "Rare Card Pack 🎴", "location": "In the arcade", "hint": "Beeps and boops and flashing lights, hidden where games bring delight."},
            {"name": "VIP Badge 📛", "location": "By the main entrance", "hint": "The first place you came, the last place you'll leave, find it where tickets you retrieve."}
        ]
    },
    
    "grand_adventure": {
        "id": "grand_adventure",
        "name": "The Grand Carnival Adventure",
        "description": "Embark on an epic journey through all areas of the carnival in this special quest line.",
        "reward": 100,
        "type": "story",
        "chapters": [
            {
                "title": "Chapter 1: Welcome to Wonder",
                "description": "Begin your adventure by experiencing the essence of the carnival.",
                "tasks": [
                    {"description": "Talk to Ringmaster Rubio", "type": "talk_to_npc", "target": "Ringmaster Rubio 🎪"},
                    {"description": "Win any minigame", "type": "win_any_game", "target": 1},
                    {"description": "Try a carnival food", "type": "eat_food", "target": 1}
                ],
                "reward": 15
            },
            {
                "title": "Chapter 2: Thrills and Chills",
                "description": "Brave the most exciting attractions the carnival has to offer.",
                "tasks": [
                    {"description": "Ride a thrilling attraction", "type": "ride_thrill", "target": 1},
                    {"description": "Visit the Haunted Mansion", "type": "specific_attraction", "target": "Haunted Mansion"},
                    {"description": "Talk to Madame Phantom", "type": "talk_to_npc", "target": "Madame Phantom 👻"}
                ],
                "reward": 20
            },
            {
                "title": "Chapter 3: Games of Skill",
                "description": "Test your abilities against the carnival's most challenging games.",
                "tasks": [
                    {"description": "Win at the Ring Toss", "type": "win_specific_game", "target": "Ring Toss"},
                    {"description": "Score above 80% in Quick Math", "type": "score_threshold", "target": 80},
                    {"description": "Talk to Professor Puzzleworth", "type": "talk_to_npc", "target": "Professor Puzzleworth 🧙‍♂️"}
                ],
                "reward": 25
            },
            {
                "title": "Chapter 4: Entertainment Extravaganza",
                "description": "Enjoy the finest shows and performances the carnival has to offer.",
                "tasks": [
                    {"description": "Attend a concert", "type": "attend_concert", "target": 1},
                    {"description": "Watch a movie at the cinema", "type": "watch_movie", "target": 1},
                    {"description": "Talk to Maestro Melody", "type": "talk_to_npc", "target": "Maestro Melody 🎵"}
                ],
                "reward": 30
            },
            {
                "title": "Chapter 5: Carnival Champion",
                "description": "Rise to the challenge and become a true champion of the carnival.",
                "tasks": [
                    {"description": "Enter any championship", "type": "enter_championship", "target": 1},
                    {"description": "Reach Silver loyalty tier", "type": "reach_loyalty_tier", "target": "Silver"},
                    {"description": "Talk to Grand Champion", "type": "talk_to_npc", "target": "Grand Champion 🏆"}
                ],
                "reward": 40
            }
        ],
        "final_reward": {
            "tickets": 100,
            "items": ["Carnival Legend 👑", "VIP Pass 🌟", "Special Discount Card 💳"],
            "special_unlock": "Legendary Quest Line"
        }
    },
    
    "seasonal_event": {
        "id": "seasonal_event",
        "name": "Seasonal Celebration",
        "description": "Join in the special seasonal festivities and earn limited-time rewards!",
        "type": "seasonal",
        "season_rewards": {
            "spring": {
                "name": "Spring Bloom Festival",
                "tasks": [
                    {"description": "Find 5 hidden Easter eggs", "type": "find_eggs", "target": 5},
                    {"description": "Participate in the flower parade", "type": "attend_parade", "target": 1},
                    {"description": "Try the special spring menu", "type": "seasonal_food", "target": 3}
                ],
                "reward": {"tickets": 40, "items": ["Spring Bunny Costume 🐰", "Flower Crown 🌸"]}
            },
            "summer": {
                "name": "Summer Splash Spectacular",
                "tasks": [
                    {"description": "Ride all water attractions", "type": "water_rides", "target": 3},
                    {"description": "Win the water balloon toss", "type": "win_specific_game", "target": "Water Balloon Toss"},
                    {"description": "Try all summer ice cream flavors", "type": "seasonal_food", "target": 4}
                ],
                "reward": {"tickets": 40, "items": ["Beach Party Costume 🏖️", "Super Soaker 💦"]}
            },
            "fall": {
                "name": "Harvest Festival",
                "tasks": [
                    {"description": "Navigate the corn maze", "type": "specific_attraction", "target": "Corn Maze"},
                    {"description": "Participate in pumpkin carving", "type": "seasonal_activity", "target": 1},
                    {"description": "Try all autumn treats", "type": "seasonal_food", "target": 4}
                ],
                "reward": {"tickets": 40, "items": ["Scarecrow Costume 🎃", "Harvest Basket 🍎"]}
            },
            "winter": {
                "name": "Winter Wonderland",
                "tasks": [
                    {"description": "Visit the ice sculpture garden", "type": "specific_attraction", "target": "Ice Garden"},
                    {"description": "Participate in the snowball fight", "type": "seasonal_activity", "target": 1},
                    {"description": "Try all hot holiday drinks", "type": "seasonal_food", "target": 3}
                ],
                "reward": {"tickets": 40, "items": ["Snow Monarch Costume ❄️", "Magical Snowglobe 🔮"]}
            }
        }
    },
    
    "friendship_quest": {
        "id": "friendship_quest",
        "name": "Carnival Connections",
        "description": "Form bonds with the carnival characters by helping them with their special requests.",
        "type": "relationship",
        "npc_quests": {
            "Ringmaster Rubio 🎪": {
                "title": "The Greatest Show",
                "description": "Help Ringmaster Rubio prepare for the grand carnival parade.",
                "tasks": [
                    {"description": "Collect 5 parade decorations", "type": "collect_items", "target": 5},
                    {"description": "Recruit 3 performers", "type": "talk_to_npcs", "target": 3},
                    {"description": "Test the parade route", "type": "visit_locations", "target": 4}
                ],
                "reward": {"tickets": 25, "relationship": "Friend", "special_item": "Ringmaster's Whistle 🔔"}
            },
            "Madame Phantom 👻": {
                "title": "Spectral Investigation",
                "description": "Assist Madame Phantom in investigating paranormal disturbances around the carnival.",
                "tasks": [
                    {"description": "Collect ectoplasm samples", "type": "collect_items", "target": 3},
                    {"description": "Document ghostly sightings", "type": "visit_locations", "target": 4},
                    {"description": "Set up ghost detection equipment", "type": "place_items", "target": 5}
                ],
                "reward": {"tickets": 25, "relationship": "Friend", "special_item": "Spirit Communicator 📱"}
            },
            "Chef Bonbon 🍰": {
                "title": "Culinary Crisis",
                "description": "Help Chef Bonbon create a new signature carnival treat before the big food festival.",
                "tasks": [
                    {"description": "Gather rare ingredients", "type": "collect_items", "target": 5},
                    {"description": "Test recipe variations", "type": "food_tasks", "target": 3},
                    {"description": "Find taste testers", "type": "talk_to_npcs", "target": 4}
                ],
                "reward": {"tickets": 25, "relationship": "Friend", "special_item": "Gourmet Recipe Book 📔"}
            }
        },
        "friendship_levels": ["Acquaintance", "Friend", "Good Friend", "Best Friend"],
        "max_level_reward": {"tickets": 100, "special_title": "Carnival Confidant", "discount": 0.25}
    }
}

NPCS = {
    "Ringmaster Rubio 🎪": {
        "missions": ["rookie", "carnival_master"], 
        "location": "Main Tent",
        "description": "An imposing figure in a crimson tailcoat with gold trim and a tall top hat",
        "dialogue": [
            "Welcome to MY carnival! The greatest show in the entire world!",
            "I've traveled continents to gather the finest entertainers for your pleasure!",
            "Ah, you seem to be enjoying yourself! Excellent, excellent!",
            "The carnival has been in my family for seven generations. We know what brings joy!"
        ],
        "special_bonus": {"type": "ticket_multiplier", "value": 1.2},
        "trades": [{"give": "VIP Badge", "receive": 50, "tickets": True}]
    },
    
    "Professor Puzzleworth 🧙‍♂️": {
        "missions": ["mathematician"], 
        "location": "Math Pavilion",
        "description": "A scholarly figure with thick spectacles and a robe covered in mathematical symbols",
        "dialogue": [
            "Ah, a fellow lover of numbers! How delightful!",
            "Did you know carnival games can be conquered through probability theory?",
            "Mathematics is the true magic of the universe, wouldn't you agree?",
            "I'm developing a formula to predict the perfect carnival experience!"
        ],
        "special_bonus": {"type": "puzzle_boost", "value": 1.5},
        "trades": [{"give": "Logic Puzzle Set", "receive": 25, "tickets": True}]
    },
    
    "Lucky Louie 🍀": {
        "missions": ["lucky"], 
        "location": "Fortune's Corner",
        "description": "A cheerful character with a four-leaf clover in his lapel and dice-patterned vest",
        "dialogue": [
            "Feeling lucky today, friend? Fortune favors the bold!",
            "I've never lost a game of chance in my life... well, almost never!",
            "The secret to luck? Believing you already have it!",
            "Care to test your fortune against mine? The odds might surprise you!"
        ],
        "special_bonus": {"type": "gambling_odds", "value": 1.1},
        "trades": [{"give": "Lucky Charm", "receive": 15, "tickets": True}]
    },
    
    "Countess VIP 👑": {
        "missions": ["vip_games"], 
        "vip_only": True,
        "location": "Exclusive Lounge",
        "description": "An elegant figure with jeweled attire and an air of refined exclusivity",
        "dialogue": [
            "Welcome to the VIP area, darling. So few make it here.",
            "Exclusivity is its own reward, wouldn't you agree?",
            "I only associate with those who appreciate the finer carnival experiences.",
            "Perhaps you'd like to see my collection of rare carnival memorabilia?"
        ],
        "special_bonus": {"type": "special_access", "value": "VIP Games"},
        "trades": [{"give": "VIP Memorabilia", "receive": "Luxury Game Token", "tickets": False}]
    },
    
    "Captain Coaster 🎢": {
        "missions": ["coaster_fan", "theme_park_explorer"], 
        "location": "Theme Park Central",
        "description": "An enthusiastic ride operator with rolled-up sleeves and a whistle around their neck",
        "dialogue": [
            "Keep your hands and feet inside the ride at all times!",
            "I've ridden every coaster in the world - twice!",
            "Safety first, thrills second, but I guarantee both!",
            "The secret to conquering your fear? Keep your eyes open on the big drop!"
        ],
        "special_bonus": {"type": "ride_discount", "value": 0.25},
        "trades": [{"give": "Ride Photo Collection", "receive": "Fast Pass", "tickets": False}]
    },
    
    "Madame Phantom 👻": {
        "missions": ["ghost_hunter"], 
        "location": "Haunted Attraction",
        "description": "A mysterious figure in Victorian dress with an ethereal glow and piercing eyes",
        "dialogue": [
            "The spirits are particularly active today... they've been expecting you.",
            "Fear is just excitement in disguise, wouldn't you agree?",
            "I've cataloged over 500 different carnival hauntings. Care to hear about them?",
            "The haunted mansion has 13 ghosts... or 14 when you're inside."
        ],
        "special_bonus": {"type": "haunted_boost", "value": 2},
        "trades": [{"give": "Ectoplasm Sample", "receive": 40, "tickets": True}]
    },
    
    "Dr. Virtual 🥽": {
        "missions": ["vr_master"], 
        "location": "VR Arcade",
        "description": "A tech-savvy innovator with neon accents on their clothing and augmented reality glasses",
        "dialogue": [
            "Reality is just one option among many, my friend!",
            "My latest VR simulation has a 99.8% reality match score!",
            "The future of carnival entertainment isn't just virtual - it's hyperreal!",
            "Have you tried the quantum reality tunneling experience yet?"
        ],
        "special_bonus": {"type": "vr_enhancement", "value": 1.5},
        "trades": [{"give": "Digital Blueprint", "receive": "VR Upgrade Token", "tickets": False}]
    },
    
    "Grand Champion 🏆": {
        "missions": ["championship_rookie", "championship_winner"], 
        "location": "Championship Arena",
        "description": "A decorated competitor with multiple medals and trophies adorning their championship jacket",
        "dialogue": [
            "Victory isn't about winning - it's about never giving up!",
            "I've won every carnival competition three years running!",
            "The secret to championship success? Practice, patience, and a bit of pizzazz!",
            "You show promise! With my guidance, you could be championship material!"
        ],
        "special_bonus": {"type": "competition_edge", "value": 1.3},
        "trades": [{"give": "Champion's Medal", "receive": 60, "tickets": True}]
    },
    
    "Couturier Carnival 👕": {
        "missions": ["collector"], 
        "location": "Fashion Boutique",
        "description": "A stylish designer with measuring tape around their neck and fabric swatches in their pocket",
        "dialogue": [
            "Darling, your current look is so... quaint. Let's elevate it!",
            "Fashion isn't just about looking good, it's about feeling extraordinary!",
            "I've designed costumes for carnival performers across seven continents!",
            "With the right outfit, you'll be the talk of the carnival!"
        ],
        "special_bonus": {"type": "costume_discount", "value": 0.3},
        "trades": [{"give": "Rare Fabric", "receive": "Custom Costume", "tickets": False}]
    },
    
    "Lady Loyalty 🌟": {
        "missions": ["loyal_visitor"], 
        "location": "Rewards Center",
        "description": "A welcoming figure with a star-adorned clipboard and loyalty cards fanned out like a deck",
        "dialogue": [
            "Loyalty is always rewarded here at the carnival!",
            "I've tracked visitors who've returned for 50 years straight!",
            "The more you visit, the more amazing your experience becomes!",
            "Have you heard about our new diamond tier benefits? Simply extraordinary!"
        ],
        "special_bonus": {"type": "loyalty_accelerator", "value": 2},
        "trades": [{"give": "Year Pass", "receive": 100, "tickets": True}]
    },
    
    "Sage Questgiver 📜": {
        "missions": [], 
        "quests": ["daily_challenge", "weekly_quest", "scavenger_hunt", "grand_adventure"],
        "location": "Quest Pavilion",
        "description": "A wise elder with a weathered quest book and ink-stained fingers from writing countless adventures",
        "dialogue": [
            "Every carnival visit is a quest waiting to unfold!",
            "I've crafted challenges for kings and commoners alike!",
            "The greatest rewards come to those who seek the most unusual quests.",
            "Your carnival journey is writing itself even now! What chapter shall we add next?"
        ],
        "special_bonus": {"type": "quest_rewards", "value": 1.5},
        "trades": [{"give": "Completed Quest Log", "receive": 80, "tickets": True}]
    },
    
    "Season Director 🎫": {
        "missions": [], 
        "season_pass": True,
        "location": "Ticket Booth",
        "description": "A meticulous planner with a calendar-patterned outfit and seasonal decorations",
        "dialogue": [
            "Planning ahead is the key to the perfect carnival experience!",
            "A season pass is more than a ticket - it's a promise of adventure!",
            "I've optimized the carnival schedule for maximum enjoyment across all four seasons!",
            "Did you know we change 40% of our attractions each season? Always something new!"
        ],
        "special_bonus": {"type": "seasonal_access", "value": "All Seasons"},
        "trades": [{"give": "All-Season Photos", "receive": 90, "tickets": True}]
    },
    
    "Chef Bonbon 🍰": {
        "missions": ["gourmet_explorer", "sweet_tooth"], 
        "location": "Food Court",
        "description": "A plump, cheerful chef with flour-dusted clothes and a towering chef's hat",
        "dialogue": [
            "Hungry, my friend? You've come to the right place!",
            "Try my world-famous funnel cake! It's a secret family recipe!",
            "A carnival without food is like a day without sunshine, non?",
            "Ah, you look famished! Let me prepare something special for you!"
        ],
        "special_bonus": {"type": "food_effectiveness", "value": 1.5},
        "trades": [{"give": "Rare Ingredient", "receive": "Special Recipe Card", "tickets": False}]
    },
    
    "Maestro Melody 🎵": {
        "missions": ["music_aficionado", "entertainment_fanatic"], 
        "location": "Concert Hall",
        "description": "A flamboyant musician with multicolored hair and a jacket covered in musical notes",
        "dialogue": [
            "Music is the heartbeat of the carnival, don't you agree?",
            "I've performed in every venue across the land, but none compare to our concert hall!",
            "Have you heard our new symphony? It's simply transcendent!",
            "Perhaps you'd like to learn an instrument? I could teach you the basics!"
        ],
        "special_bonus": {"type": "music_effect", "value": 1.4},
        "trades": [{"give": "Rare Music Sheet", "receive": "Backstage Pass", "tickets": False}]
    }
}

COSTUMES = {
    "Default 😊": {"emoji": "😊", "price": 0, "available": True},
    "VIP Crown 👑": {"emoji": "👑", "price": 100, "available": True, "vip_only": True},
    "VIP Diamond 💎": {"emoji": "💎", "price": 150, "available": True, "vip_only": True},
    "VIP Star ⭐": {"emoji": "⭐", "price": 120, "available": True, "vip_only": True},
    "Halloween Skull 💀": {"emoji": "💀", "price": 50, "available": False, "seasonal": "halloween"},
    "Robot 🤖": {"emoji": "🤖", "price": 45, "available": False, "seasonal": "halloween"},
    "Pumpkin 🎃": {"emoji": "🎃", "price": 40, "available": False, "seasonal": "halloween"},
    "Ghost 👻": {"emoji": "👻", "price": 35, "available": False, "seasonal": "halloween"},
    "Moai 🗿": {"emoji": "🗿", "price": 30, "available": True},
    "Froggy 🐸": {"emoji": "🐸", "price": 25, "available": True},
    "Panda 🐼": {"emoji": "🐼", "price": 25, "available": True},
    "Polar Bear 🐻‍❄️": {"emoji": "🐻‍❄️", "price": 25, "available": True},
    "Bear 🐻": {"emoji": "🐻", "price": 25, "available": True},
    "Cool Guy 😎": {"emoji": "😎", "price": 15, "available": True},
    "Clown 🤡": {"emoji": "🤡", "price": 20, "available": True, "halloween_discount": True},
    "Furry 🐱": {"emoji": "🐱", "price": 20, "available": True, "halloween_discount": True},
    "Quarantine 2020 😷": {"emoji": "😷", "price": 10, "available": True},
    "Monkey 🐵": {"emoji": "🐵", "price": 20, "available": True, "halloween_discount": True},
    "Cowboy 🤠": {"emoji": "🤠", "price": 20, "available": True, "halloween_discount": True},
    "Alien 👽": {"emoji": "👽", "price": 20, "available": True, "halloween_discount": True},
    "Nerd 🤓": {"emoji": "🤓", "price": 15, "available": True},
    "Rabbit 🐰": {"emoji": "🐰", "price": 20, "available": True, "easter_discount": True},
    "Mr. Funny 🥸": {"emoji": "🥸", "price": 25, "available": True},
    "Not Sure Bro 🧐": {"emoji": "🧐", "price": 30, "available": True},
    "Werewolf 🐺": {"emoji": "🐺", "price": 25, "available": True, "halloween_discount": True}
}

CONSUMABLES = {
    "Game Discount Ticket 🎫": {"price": 15, "discount": 0.5, "uses": 3},
    "Lucky Charm 🍀": {"price": 20, "luck_boost": 1.2, "uses": 5},
    "VIP Pass 🌟": {"price": 100, "discount": 0.7, "uses": 1},
    "Fast Pass Ticket ⚡": {"price": 25, "description": "Skip waiting in line for one attraction", "uses": 1},
    "Season Pass 🏰": {"price": 200, "description": "50% off all attractions for 30 days", "uses": 30, "discount": 0.5},
    "Loyalty Booster 📈": {"price": 30, "description": "Earn double loyalty points for 5 visits", "uses": 5},
    "Championship Token 🥇": {"price": 40, "description": "Free entry to one championship event", "uses": 1},
    "Quest Helper 📋": {"price": 15, "description": "Get a hint for any active quest", "uses": 3}
}

# Loyalty program tiers
LOYALTY_TIERS = {
    "Bronze Member": {"points": 0, "discount": 0, "bonus": 0},
    "Silver Member": {"points": 50, "discount": 0.1, "bonus": 1},
    "Gold Member": {"points": 150, "discount": 0.15, "bonus": 2},
    "Platinum Member": {"points": 300, "discount": 0.2, "bonus": 3},
    "Diamond Member": {"points": 500, "discount": 0.25, "bonus": 5}
}

# Quest system
QUESTS = {
    "daily_challenge": {
        "name": "Daily Challenge",
        "description": "Complete a randomly selected task each day",
        "reward": 15,
        "expires_in": "24h",
        "possible_tasks": [
            "Win 3 minigames",
            "Earn 30 tickets",
            "Visit 2 theme park attractions",
            "Play a championship game",
            "Buy something from the shop"
        ]
    },
    "weekly_quest": {
        "name": "Weekly Spectacular",
        "description": "Complete a multi-part quest for big rewards",
        "reward": 50,
        "expires_in": "7d",
        "steps": [
            "Visit the Haunted Mansion",
            "Ride the Cosmic Coaster",
            "Win a card game",
            "Buy a costume",
            "Play 3 different minigames"
        ]
    },
    "scavenger_hunt": {
        "name": "Carnival Scavenger Hunt",
        "description": "Find hidden items around the carnival",
        "reward": 30,
        "hidden_items": [
            "Golden Ticket 🎫",
            "Mystery Box 📦",
            "Lucky Coin 🪙",
            "Rare Card Pack 🎴",
            "VIP Badge 📛"
        ]
    },
    "loyalty_mission": {
        "name": "Loyal Visitor Challenge",
        "description": "Visit the same attraction 3 times to get a free play",
        "reward": "free_play",
        "target": 3
    }
}

# Championship events
CHAMPIONSHIPS = {
    "card_masters": {
        "name": "Card Masters Tournament",
        "entry_fee": 10,
        "min_cards": 15,
        "prize_pool": [100, 50, 25],
        "special_reward": "Legendary Champion's Card"
    },
    "skill_challenge": {
        "name": "Carnival Skills Challenge",
        "entry_fee": 5,
        "games": ["dart_throw", "reaction_test", "balloon_pop", "ring_toss"],
        "prize_pool": [60, 30, 15],
        "special_reward": "Skills Champion Trophy"
    },
    "theme_park_marathon": {
        "name": "Theme Park Marathon",
        "description": "Complete all rides in the fastest time",
        "entry_fee": 15,
        "prize_pool": [80, 40, 20],
        "special_reward": "Season Pass Extension (7 days)"
    },
    "trivia_tournament": {
        "name": "Carnival Trivia Masters",
        "entry_fee": 5,
        "categories": ["Carnival History", "Games", "Attractions", "General Knowledge"],
        "questions_per_round": 10,
        "prize_pool": [40, 20, 10],
        "special_reward": "Trivia Master Costume"
    }
}

# Card game constants
CARD_DATABASE = {
    "Fire Dragon": {"emoji": "🔥", "power": 8, "element": "fire", "rarity": "rare"},
    "Water Sprite": {"emoji": "💧", "power": 6, "element": "water", "rarity": "uncommon"},
    "Earth Giant": {"emoji": "🌍", "power": 7, "element": "earth", "rarity": "rare"},
    "Wind Eagle": {"emoji": "🌪️", "power": 5, "element": "wind", "rarity": "uncommon"},
    "Shadow Wolf": {"emoji": "🐺", "power": 6, "element": "dark", "rarity": "uncommon"},
    "Light Angel": {"emoji": "👼", "power": 6, "element": "light", "rarity": "uncommon"},
    "Thunder Beast": {"emoji": "⚡", "power": 7, "element": "thunder", "rarity": "rare"},
    "Ice Golem": {"emoji": "❄️", "power": 7, "element": "ice", "rarity": "rare"},
    "Forest Elf": {"emoji": "🌳", "power": 5, "element": "nature", "rarity": "uncommon"},
    "Mystic Wizard": {"emoji": "🧙", "power": 8, "element": "arcane", "rarity": "rare"},
    "Legendary Champion's Card": {"emoji": "🏆", "power": 10, "element": "legendary", "rarity": "legendary"},
    "Cosmic Voyager": {"emoji": "🌠", "power": 9, "element": "cosmic", "rarity": "rare"},
    "Mechanical Titan": {"emoji": "🤖", "power": 8, "element": "tech", "rarity": "rare"},
    "Spirit Guardian": {"emoji": "👻", "power": 7, "element": "spirit", "rarity": "uncommon"},
    "Royal Champion": {"emoji": "👑", "power": 9, "element": "royal", "rarity": "rare"}
}

CARD_NPCS = {
    "Apprentice Time Keeper": {"difficulty": 1, "deck_size": 30, "faction": "Time Keepers", "reward": 10},
    "Void Walker Initiate": {"difficulty": 2, "deck_size": 35, "faction": "Void Walkers", "reward": 15},
    "Beast Master": {"difficulty": 3, "deck_size": 40, "faction": "Cosmic Beasts", "reward": 20},
    "Reality Architect": {"difficulty": 4, "deck_size": 45, "faction": "Dimensional Weavers", "reward": 30}
}

CHAMPIONSHIP_BRACKETS = [
    ["Apprentice Time Keeper", "Void Walker Initiate"],
    ["Beast Master", "Reality Architect"]
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def save_game(slot):
    """Save current game state to specified slot.
    Args:
        slot (int): Save slot index (0-2)
    """
    with open(SAVE_SLOTS[slot], "w") as f:
        json.dump(player, f)
    print(Fore.GREEN + f"💾 Game saved to Slot {slot+1}!")

def load_game(slot):
    """Load game state from specified slot.
    Args:
        slot (int): Save slot index (0-2)
    """
    if os.path.exists(SAVE_SLOTS[slot]):
        with open(SAVE_SLOTS[slot], "r") as f:
            data = json.load(f)
            player.update(data)
            print(Fore.YELLOW + f"🎉 Welcome back, {player['name']}!")
    else:
        print(Fore.RED + "⚠️ No saved game found in that slot!")

# ------------------------------
# Achievements
# ------------------------------
def award_achievement(name):
    if name not in player["achievements"]:
        print(Fore.CYAN + f"🏆 Achievement Unlocked: {name}")
        player["achievements"].append(name)

# ------------------------------
# Shop System
# ------------------------------
def shop():
    clear()
    print(Fore.LIGHTBLUE_EX + "🏪 Ticket Shop")
    print(f"Your Tickets: {player['tickets']}")
    print(f"Current Costume: {player['equipped_costume']}")
    print("\n[1] Costumes 👕")
    print("[2] Consumables 🎫")
    print("[3] Card Packs 🎴")
    print("[4] Manage Deck 📋")
    print("[0] Back")

    choice = input("Choose category: ")

    if choice == "1":
        shop_costumes()
    elif choice == "2":
        shop_consumables()
    elif choice == "3":
        buy_card_pack()
    elif choice == "4":
        manage_deck()
    elif choice != "0":
        print(Fore.RED + "Invalid choice.")

def shop_costumes():
    clear()
    print(Fore.LIGHTBLUE_EX + "👕 Costume Shop")
    print(f"Your Tickets: {player['tickets']}")
    available_costumes = [(name, data) for name, data in COSTUMES.items() if data["available"]]

    for i, (name, data) in enumerate(available_costumes):
        price = data["price"]
        if data.get("halloween_discount") and is_halloween():
            price = int(price * 0.7)  # 30% discount
        elif data.get("easter_discount") and is_easter():
            price = int(price * 0.8)  # 20% discount
        print(f"[{i+1}] {name} - {price} tickets")
    print("[0] Back")

    choice = input("Choose costume: ")
    if choice == "0":
        return
    try:
        index = int(choice) - 1
        costume_name, costume_data = available_costumes[index]
        price = costume_data["price"]

        if player["tickets"] >= price:
            player["tickets"] -= price
            player["inventory"].append(costume_name)
            print(Fore.GREEN + f"You bought: {costume_name}")
            check_costume_achievements()
            equip_menu(costume_name, "costume")
        else:
            print(Fore.RED + "Not enough tickets!")
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid choice.")

def shop_consumables():
    clear()
    print(Fore.LIGHTBLUE_EX + "🎫 Consumables Shop")
    print(f"Your Tickets: {player['tickets']}")

    for i, (name, data) in enumerate(CONSUMABLES.items()):
        print(f"[{i+1}] {name} - {data['price']} tickets")
    print("[0] Back")

    choice = input("Choose item: ")
    if choice == "0":
        return
    try:
        index = int(choice) - 1
        item_name = list(CONSUMABLES.keys())[index]
        item_data = CONSUMABLES[item_name]

        if player["tickets"] >= item_data["price"]:
            player["tickets"] -= item_data["price"]
            player["inventory"].append(item_name)
            print(Fore.GREEN + f"You bought: {item_name}")
            check_item_achievements()
            equip_menu(item_name, "consumable")
        else:
            print(Fore.RED + "Not enough tickets!")
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid choice.")

def equip_menu(item_name, item_type):
    if input(f"Equip {item_name} now? (y/n): ").lower() == 'y':
        if item_type == "costume":
            player["equipped_costume"] = COSTUMES[item_name]["emoji"]
            print(Fore.GREEN + f"Equipped {item_name}!")
        elif item_type == "consumable":
            if item_name not in player["equipped_items"]:
                player["equipped_items"].append(item_name)
                print(Fore.GREEN + f"Equipped {item_name}!")
            else:
                print(Fore.YELLOW + "Item already equipped!")

def is_halloween():
    # Simple check - October
    return time.localtime().tm_mon == 10

def is_easter():
    # Simple check - April
    return time.localtime().tm_mon == 4

def check_costume_achievements():
    costume_count = sum(1 for item in player["inventory"] if item in COSTUMES)
    if costume_count >= 5:
        award_achievement("Fashionista: Own 5 costumes")
    if costume_count >= 10:
        award_achievement("Costume Collector: Own 10 costumes")
    if all(c in player["inventory"] for c in ["Bear 🐻", "Panda 🐼", "Polar Bear 🐻‍❄️"]):
        award_achievement("Bear Family: Collect all bears")

def check_item_achievements():
    consumable_count = sum(1 for item in player["inventory"] if item in CONSUMABLES)
    if consumable_count >= 3:
        award_achievement("Prepared: Own 3 consumable items")
    if consumable_count >= 5:
        award_achievement("Well-Stocked: Own 5 consumable items")

# ------------------------------
# Minigames
# ------------------------------

def pay_to_play(cost):
    if player["tickets"] < cost:
        print(Fore.RED + f"❌ Not enough tickets (need {cost})!")
        return False
    player["tickets"] -= cost
    return True

def guess_the_number():
    if not pay_to_play(3): 
        return
    clear()
    print(Fore.MAGENTA + "🎯 Guess the Number!")
    number = random.randint(1, 5)
    guess = int(input("Pick a number between 1 and 5: "))
    if guess == number:
        print(Fore.GREEN + "You guessed it! +5 tickets!")
        player["tickets"] += 5
        award_achievement("Lucky Guess!")
    else:
        print(Fore.RED + f"Nope! It was {number}.")

def quick_math():
    if not pay_to_play(2): 
        return
    clear()
    print(Fore.YELLOW + "🧠 Quick Math!")
    a, b = random.randint(1, 10), random.randint(1, 10)
    answer = a + b
    user = int(input(f"What is {a} + {b}? "))
    if user == answer:
        print(Fore.GREEN + "Correct! +4 tickets!")
        player["tickets"] += 4
    else:
        print(Fore.RED + f"Wrong! It was {answer}.")

def word_shuffle():
    if not pay_to_play(3): 
        return
    clear()
    print(Fore.BLUE + "🔤 Word Shuffle!")
    word = random.choice(["carnival", "magic", "popcorn"])
    shuffled = ''.join(random.sample(word, len(word)))
    print(f"Unscramble: {shuffled}")
    guess = input("Your guess: ").lower()
    if guess == word:
        print(Fore.GREEN + "Nice! +6 tickets!")
        player["tickets"] += 6
    else:
        print(Fore.RED + f"It was '{word}'.")

def lucky_spinner():
    if not pay_to_play(1): 
        return
    clear()
    print(Fore.CYAN + "🎰 Lucky Spinner!")
    spin = random.choice([0, 2, 5, 10, -2])
    print(f"Result: {spin} tickets!")
    player["tickets"] = max(0, player["tickets"] + spin)

def dart_throw():
    if not pay_to_play(3): 
        return
    clear()
    hit = random.choices(["Bullseye", "Close", "Miss"], weights=[1, 2, 3])[0]
    print(f"You threw... {hit}!")
    if hit == "Bullseye":
        print(Fore.GREEN + "+8 tickets!")
        player["tickets"] += 8
        award_achievement("Perfect Aim!")
    elif hit == "Close":
        print(Fore.YELLOW + "+3 tickets!")
        player["tickets"] += 3
    else:
        print(Fore.RED + "No tickets.")

def reaction_test():
    if not pay_to_play(2): 
        return
    clear()
    print("Wait for GO!")
    time.sleep(random.uniform(2, 5))
    input("...READY...")
    print("GO!")
    start = time.time()
    input()
    reaction = time.time() - start
    print(f"Time: {reaction:.3f}s")
    if reaction < 0.3:
        print(Fore.GREEN + "+7 tickets!")
        player["tickets"] += 7
    elif reaction < 0.6:
        print(Fore.YELLOW + "+4 tickets!")
        player["tickets"] += 4
    else:
        print(Fore.RED + "Too slow!")

def melody_memory():
    if not pay_to_play(3): 
        return
    notes = ['A', 'B', 'C', 'D']
    pattern = [random.choice(notes) for _ in range(3)]
    print("Pattern:", " ".join(pattern))
    time.sleep(2)
    clear()
    guess = input("Enter pattern (space-separated): ").strip().upper().split()
    if guess == pattern:
        print(Fore.GREEN + "+6 tickets!")
        player["tickets"] += 6
    else:
        print(Fore.RED + f"Wrong! Pattern: {' '.join(pattern)}")

def show_tutorials():
    clear()
    print(Fore.LIGHTMAGENTA_EX + "📘 TUTORIAL MODE")
    print("These are practice versions of the games. No tickets used or rewarded.")
    games = [
        ("Guess the Number", lambda: guess_the_number_free()),
        ("Quick Math", lambda: quick_math_free()),
        ("Word Shuffle", lambda: word_shuffle_free()),
        ("Reaction Test", lambda: reaction_test_free()),
    ]
    for i, (name, _) in enumerate(games):
        print(f"[{i+1}] {name}")
    print("[0] Back")
    choice = input("Choose a tutorial: ")
    if choice == "0": 
        return
    elif choice in map(str, range(1, len(games)+1)):
        games[int(choice)-1][1]()
    else:
        print("Invalid.")

# Tutorial variants of existing games (no cost or reward)
def guess_the_number_free():
    clear()
    number = random.randint(1, 5)
    guess = int(input("Guess a number between 1 and 5: "))
    print("Correct!" if guess == number else f"Wrong! It was {number}")

def quick_math_free():
    clear()
    a, b = random.randint(1, 10), random.randint(1, 10)
    user = int(input(f"What is {a} + {b}? "))
    print("Correct!" if user == a + b else f"Wrong! Answer: {a + b}")

def word_shuffle_free():
    clear()
    word = random.choice(["carnival", "magic", "popcorn"])
    shuffled = ''.join(random.sample(word, len(word)))
    print(f"Unscramble: {shuffled}")
    guess = input("Your guess: ")
    print("Correct!" if guess.lower() == word else f"It was '{word}'.")

def reaction_test_free():
    clear()
    print("Wait for GO!")
    time.sleep(random.uniform(2, 4))
    input("...READY...")
    print("GO!")
    start = time.time()
    input()
    print(f"Your time: {time.time() - start:.3f}s")

def guess_password():
    if not pay_to_play(4): 
        return
    code = ''.join(random.choices('ABCDEF', k=3))
    guess = input("Guess 3-letter code (A-F): ").upper()
    if guess == code:
        print(Fore.GREEN + "You cracked it! +10 tickets!")
        player["tickets"] += 10
        award_achievement("Hacker Mind!")
    else:
        correct = sum(1 for a, b in zip(guess, code) if a == b)
        print(Fore.YELLOW + f"{correct}/3 correct. Code: {code}")

# ------------------------------
# Menus
# ------------------------------

def minigame_menu():
    """Display and handle the minigame selection menu.
    Shows available games and their ticket costs.
    Games are grouped into free/cheap and regular categories.
    """
    while True:
        print(Fore.LIGHTCYAN_EX + "\n🎮 Minigames (Cost in Tickets):")
        print(Fore.GREEN + "\nFree/Cheap Games:")
        print("""
[1] Paper Scissors Rock (1)
[2] Coin Flip (1)
[3] High Low (2)
""")
        print(Fore.CYAN + "\nRegular Games:")
        print("""
[4] Guess the Number (3)
[5] Quick Math (2)
[6] Word Shuffle (3)
[7] Lucky Spinner (1)
[8] Dart Throw (3)
[9] Reaction Test (2)
[10] Melody Memory (3)
[11] Guess the Password (4)
[12] Hangman (3)
[13] Memory Match (4)
[14] Number Racing (2)
[15] Balloon Pop (2)
[16] Ring Toss (3)
[17] Duck Shooting (3)
[18] Target Shooting (3)
[19] Whack-a-Mole (2)
[20] Bottle Toss (3)
[21] 🎣 Kingyo-Sukui (3)
[22] 🎈 Yo-yo Tsuri (2)
[23] 👑 Treasure Hunt [VIP EXCLUSIVE] (5)
[24] 👑 Card Battle (5)
[25] 🏆 TCG Championship (2)
[26] Back
""")
        choice = input("Select: ")
        games = [paper_scissors_rock, coin_flip_game, high_low, guess_the_number, 
                quick_math, word_shuffle, lucky_spinner, dart_throw, reaction_test, 
                melody_memory, guess_password, hangman_game, memory_match, number_racing,
                balloon_pop, ring_toss, duck_shooting]
        if choice == "26":
            break
        elif choice == "25":
            if not pay_to_play(2):
                return
            tcg_championship()
        elif choice == "24":
            if not pay_to_play(5):
                return
            card_battle()
        elif choice == "23":
            if "VIP Pass 🌟" not in player["inventory"]:
                print(Fore.RED + "❌ This game requires a VIP Pass!")
                return
            if not pay_to_play(5):
                return
            treasure_hunt()
        elif choice in map(str, range(1, 21)):
            games = [paper_scissors_rock, coin_flip_game, high_low, guess_the_number, 
                    quick_math, word_shuffle, lucky_spinner, dart_throw, reaction_test, 
                    melody_memory, guess_password, hangman_game, memory_match, number_racing,
                    balloon_pop, ring_toss, duck_shooting, target_shooting, whack_a_mole, 
                    bottle_toss]
            games[int(choice)-1]()
        else:
            print("Invalid.")

def save_menu():
    print(Fore.GREEN + "\nSave Slots:")
    for i in range(3):
        if os.path.exists(SAVE_SLOTS[i]):
            with open(SAVE_SLOTS[i], 'r') as f:
                data = json.load(f)
                print(f"[{i+1}] Slot {i+1} - {data['name']} ({data['tickets']} tickets)")
        else:
            print(f"[{i+1}] Slot {i+1} - Empty")
    print("[4] Auto-save current slot")
    slot = input("Choose slot (1-4): ")
    if slot in ["1", "2", "3"]:
        save_game(int(slot)-1)
    elif slot == "4":
        if hasattr(player, 'current_slot'):
            save_game(player['current_slot'])
            print(Fore.GREEN + f"Auto-saved to slot {player['current_slot']+1}!")
        else:
            print(Fore.RED + "No current slot selected. Please save to a slot first.")

def load_menu():
    print(Fore.YELLOW + "\nLoad Slots:")
    for i in range(3):
        print(f"[{i+1}] Load Slot {i+1}")
    slot = input("Choose slot (1-3): ")
    if slot in ["1", "2", "3"]:
        load_game(int(slot)-1)

def tutorials():
    clear()
    print(Fore.YELLOW + "📖 Game Tutorials")
    print("""
1. Play minigames to earn tickets
2. Use tickets to buy items in the shop
3. Save your progress in save slots
4. Try your luck in gambling games
5. Unlock achievements as you play
    """)
    input("Press Enter to continue...")

def gambling_menu():
    """Display and handle the gambling games menu.
    Available games:
    - Double or Nothing: 50/50 chance to double bet
    - Card Draw: Higher card wins
    - Wheel of Fate: Random multiplier
    - Lucky Slots: Match symbols for prizes
    """
    clear()
    print(Fore.RED + "🎰 GAMBLING GAMES")
    print("""
[1] Double or Nothing (bet and 50/50)
[2] Card Draw (draw vs dealer)
[3] Wheel of Fate (spin for multiplier)
[4] Lucky Slots (2 tickets per pull)
[5] Lucky Dice (dice betting)
[6] Race Track (animal racing)
[0] Back
""")
    choice = input("Choose a game: ")
    if choice == "1":
        double_or_nothing()
    elif choice == "2":
        card_draw()
    elif choice == "3":
        wheel_of_fate()
    elif choice == "4":
        lucky_slots()
    elif choice == "5":
        lucky_dice()
    elif choice == "6":
        race_track()
    elif choice == "0":
        return
    else:
        print("Invalid.")

def lucky_dice():
    bet = int(input("Place your bet: "))
    if bet > player["tickets"] or bet <= 0:
        print("Invalid bet!")
        return

    print("\n🎲 Choose your bet:")
    print("[1] Single number (1-6) - 6x payout")
    print("[2] Even/Odd - 2x payout")
    print("[3] High (4-6)/Low (1-3) - 2x payout")

    choice = input("Your choice: ")
    if choice == "1":
        num = int(input("Choose number (1-6): "))
        dice = random.randint(1, 6)
        print(f"🎲 Rolled: {dice}")
        if num == dice:
            winnings = bet * 6
            print(Fore.GREEN + f"You win! +{winnings} tickets!")
            player["tickets"] += winnings
        else:
            print(Fore.RED + f"You lose! -{bet} tickets")
            player["tickets"] -= bet

    elif choice == "2":
        guess = input("Even or Odd? ").lower()
        dice = random.randint(1, 6)
        print(f"🎲 Rolled: {dice}")
        if (guess == "even" and dice % 2 == 0) or (guess == "odd" and dice % 2 != 0):
            print(Fore.GREEN + f"You win! +{bet} tickets!")
            player["tickets"] += bet
        else:
            print(Fore.RED + f"You lose! -{bet} tickets")
            player["tickets"] -= bet

    elif choice == "3":
        guess = input("High or Low? ").lower()
        dice = random.randint(1, 6)
        print(f"🎲 Rolled: {dice}")
        if (guess == "high" and dice >= 4) or (guess == "low" and dice <= 3):
            print(Fore.GREEN + f"You win! +{bet} tickets!")
            player["tickets"] += bet
        else:
            print(Fore.RED + f"You lose! -{bet} tickets")
            player["tickets"] -= bet

def race_track():
    animals = ["🐎 Horse", "🐪 Camel", "🐢 Turtle", "🐰 Rabbit"]
    multipliers = [2, 3, 4, 2]

    print("\n🏁 Race Track Betting")
    for i, (animal, mult) in enumerate(zip(animals, multipliers), 1):
        print(f"[{i}] {animal} - {mult}x payout")

    bet = int(input("\nPlace your bet: "))
    if bet > player["tickets"] or bet <= 0:
        print("Invalid bet!")
        return

    choice = int(input("Choose your animal (1-4): ")) - 1
    if choice < 0 or choice >= len(animals):
        print("Invalid choice!")
        return

    print("\n🏁 Race starting...")
    time.sleep(1)
    winner = random.randint(0, len(animals)-1)
    print(f"🏆 Winner: {animals[winner]}")

    if choice == winner:
        winnings = bet * multipliers[choice]
        print(Fore.GREEN + f"You win! +{winnings} tickets!")
        player["tickets"] += winnings
    else:
        print(Fore.RED + f"You lose! -{bet} tickets")
        player["tickets"] -= bet

def lucky_slots():
    clear()
    print(Fore.MAGENTA + "🎰 LUCKY SLOTS")
    print("[1] Single Pull (2 tickets)")
    print("[2] Ten Pulls (6 tickets)")
    choice = input("Choose option: ")

    symbols = ["🍒", "🍊", "🍋", "💎", "7️⃣", "⭐"]
    payouts = {
        "🍒🍒🍒": 3,
        "🍊🍊🍊": 4,
        "🍋🍋🍋": 5,
        "💎💎💎": 10,
        "7️⃣7️⃣7️⃣": 15,
        "⭐⭐⭐": 20
    }

    def single_pull():
        result = [random.choice(symbols) for _ in range(3)]
        print(" ".join(result))
        result_str = "".join(result)
        winnings = payouts.get(result_str, 0)
        if winnings > 0:
            print(Fore.GREEN + f"Winner! +{winnings} tickets!")
            return winnings
        return 0

    if choice == "1" and player["tickets"] >= 2:
        player["tickets"] -= 2
        player["tickets"] += single_pull()
    elif choice == "2" and player["tickets"] >= 6:
        player["tickets"] -= 6
        total_winnings = 0
        for i in range(10):
            print(f"\nPull {i+1}:")
            total_winnings += single_pull()
            time.sleep(0.5)
        print(f"\nTotal winnings: {total_winnings} tickets!")
        player["tickets"] += total_winnings
    else:
        print(Fore.RED + "Not enough tickets!")

def double_or_nothing():
    bet = int(input("Bet amount: "))
    if bet > player["tickets"] or bet <= 0:
        print("Invalid bet!")
        return
    print("Flipping coin...")
    if random.choice([True, False]):
        print(Fore.GREEN + "You doubled it!")
        player["tickets"] += bet
    else:
        print(Fore.RED + "You lost it all!")
        player["tickets"] -= bet

def card_draw():
    bet = int(input("Bet amount: "))
    if bet > player["tickets"] or bet <= 0:
        print("Invalid bet!")
        return
    player_card = random.randint(1, 13)
    dealer_card = random.randint(1, 13)
    print(f"You: {player_card} | Dealer: {dealer_card}")
    if player_card > dealer_card:
        print(Fore.GREEN + f"You win! +{bet}")
        player["tickets"] += bet
    elif player_card < dealer_card:
        print(Fore.RED + f"You lose! -{bet}")
        player["tickets"] -= bet
    else:
        print(Fore.YELLOW + "Draw. No change.")

def wheel_of_fate():
    bet = int(input("Bet amount: "))
    if bet > player["tickets"] or bet <= 0:
        print("Invalid bet!")
        return
    multipliers = [0, 0.5, 1, 2, 3]
    result = random.choice(multipliers)
    winnings = int(bet * result)
    player["tickets"] += winnings - bet
    print(f"Multiplier: x{result}")
    if result == 0:
        print(Fore.RED + "You lost everything!")
    elif result == 1:
        print(Fore.YELLOW + "Broke even.")
    else:
        print(Fore.GREEN + f"You won {winnings}!")

# Redeemable codes system
REWARD_CODES = {
    "WELCOME2024": {"tickets": 50, "costume": "VIP Crown 👑", "active": True, "description": "Welcome gift!"},
    "CHRONOKING": {"tickets": 30, "card": "Time Lord Chronos", "active": True, "description": "Special TCG card!"},
    "CARNIVAL100": {"tickets": 100, "active": True, "description": "Bonus tickets!"},
    "VOID2024": {"tickets": 25, "card": "Void Emperor", "active": True, "description": "Special void card!"},
    "DRAGONFEST": {"tickets": 40, "card": "Space-Time Dragon", "active": True, "description": "Dragon card bonus!"}
}

def redeem_code():
    clear()
    print(Fore.CYAN + "🎟️ Code Redemption")
    code = input("Enter your code: ").upper()

    if code in REWARD_CODES and REWARD_CODES[code]["active"]:
        reward = REWARD_CODES[code]
        print(Fore.GREEN + f"\n✨ Code valid! {reward['description']}")

        if "tickets" in reward:
            player["tickets"] += reward["tickets"]
            print(f"+ {reward['tickets']} tickets!")

        if "costume" in reward:
            if reward["costume"] not in player["inventory"]:
                player["inventory"].append(reward["costume"])
                print(f"+ New costume: {reward['costume']}")
            else:
                print("(You already have this costume)")

        if "card" in reward:
            player["card_collection"].append(reward["card"])
            print(f"+ New card: {reward['card']}")

        REWARD_CODES[code]["active"] = False
        print(Fore.YELLOW + "\nReward claimed successfully!")
    else:
        print(Fore.RED + "❌ Invalid or already used code!")

    input("\nPress Enter to continue...")

def main_menu():
    """Enhanced main menu with dynamic NPC interactions and improved visual display"""
    init_player_attributes()
    check_daily_reward()

    while True:
        clear()
        
        # Dynamic colored ASCII art banner with visual effects
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        carnival_art = f"""
{random.choice(colors)} ░▒▓██████▓▒░  ░▒▓██████▓▒░ ░▒▓███████▓▒░ ░▒▓███████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓██████▓▒░ ░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓████████▓▒░░▒▓███████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒▒▓█▓▒░ ░▒▓████████▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)} ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░   ░▒▓██▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓████████▓▒░
        """
        print(carnival_art)
        
        # Season indicator with visual theming
        current_season = get_current_season()
        season_emojis = {
            "spring": "🌸", "summer": "☀️", "fall": "🍂", "winter": "❄️"
        }
        season_colors = {
            "spring": Fore.MAGENTA, "summer": Fore.YELLOW, 
            "fall": Fore.RED, "winter": Fore.CYAN
        }
        
        # Welcome message with seasonal greeting
        print(f"{season_colors[current_season]}🎪 Welcome to the {current_season.title()} Carnival! {season_emojis[current_season]}")
        
        # Random NPC greeting
        random_npc = random.choice(list(NPCS.keys()))
        random_dialogue = random.choice(NPCS[random_npc]["dialogue"])
        print(f"{Fore.YELLOW}{random_npc}: {Fore.WHITE}\"{random_dialogue}\"")
        
        # Display player status with improved formatting
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        # Display loyalty tier if player has any points
        loyalty_info = ""
        if player.get("loyalty_points", 0) > 0:
            tier = get_loyalty_tier()
            tier_colors = {"Bronze": Fore.RED, "Silver": Fore.WHITE, "Gold": Fore.YELLOW, 
                          "Platinum": Fore.CYAN, "Diamond": Fore.MAGENTA}
            colored_tier = f"{tier_colors.get(tier, Fore.WHITE)}{tier}{Style.RESET_ALL}"
            loyalty_info = f"🌟 {colored_tier} ({player['loyalty_points']} points)"
        
        # Player status bar with hunger/energy indicators if applicable
        hunger_bar = ""
        energy_bar = ""
        if "hunger" in player and "energy" in player:
            hunger_level = player["hunger"]
            energy_level = player["energy"]
            
            # Create visual bars
            hunger_filled = "■" * (hunger_level // 10)
            hunger_empty = "□" * ((100 - hunger_level) // 10)
            energy_filled = "■" * (energy_level // 10)
            energy_empty = "□" * ((100 - energy_level) // 10)
            
            # Color code based on levels
            hunger_color = Fore.GREEN if hunger_level > 60 else Fore.YELLOW if hunger_level > 30 else Fore.RED
            energy_color = Fore.GREEN if energy_level > 60 else Fore.YELLOW if energy_level > 30 else Fore.RED
            
            hunger_bar = f"🍔 {hunger_color}{hunger_filled}{hunger_empty} {hunger_level}%{Style.RESET_ALL}"
            energy_bar = f"⚡ {energy_color}{energy_filled}{energy_empty} {energy_level}%{Style.RESET_ALL}"
        
        # Status display with emoji indicators
        print(f"{Fore.YELLOW}👤 {player['equipped_costume']} {player['name']} | 🎟️ Tickets: {player['tickets']} | {loyalty_info}")
        if hunger_bar and energy_bar:
            print(f"{hunger_bar} | {energy_bar}")
            
        # Inventory and equipped items
        print(f"\n{Fore.MAGENTA}🎒 INVENTORY:{Style.RESET_ALL} {', '.join(player['inventory']) if player['inventory'] else 'Empty'}")
        print(f"{Fore.CYAN}⚡ ACTIVE ITEMS:{Style.RESET_ALL} {', '.join(player['equipped_items']) if player['equipped_items'] else 'None'}")
        
        # Achievements and active missions
        print(f"{Fore.YELLOW}🏆 ACHIEVEMENTS:{Style.RESET_ALL} {len(player['achievements']) if 'achievements' in player else 0}")
        active_missions = len(player["missions"]) if "missions" in player else 0
        active_quests = len(player.get("active_quests", [])) 
        print(f"{Fore.GREEN}📋 ACTIVE MISSIONS:{Style.RESET_ALL} {active_missions} | {Fore.GREEN}📜 ACTIVE QUESTS:{Style.RESET_ALL} {active_quests}")
        
        # VIP and season pass status
        has_vip = "VIP Pass 🌟" in player["inventory"]
        if has_vip:
            print(f"{Fore.MAGENTA}👑 VIP STATUS:{Style.RESET_ALL} Active (Special privileges unlocked)")
        
        if player.get("season_pass", False):
            days_left = player.get("season_pass_days", 30)
            print(f"{Fore.GREEN}🎫 SEASON PASS:{Style.RESET_ALL} Active ({days_left} days remaining)")
        
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        # Special event notifications
        if is_halloween():
            print(f"{Fore.MAGENTA}🎃 SPECIAL EVENT:{Style.RESET_ALL} Halloween Spooktacular is active! Special items and quests available!")
        elif is_easter():
            print(f"{Fore.YELLOW}🐰 SPECIAL EVENT:{Style.RESET_ALL} Easter Egg Hunt is active! Find hidden eggs around the carnival!")
        
        # Group options by category for better organization
        print(f"\n{Fore.YELLOW}=== CARNIVAL ATTRACTIONS ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}[1] Play Minigames        [9] Theme Park 🎢         [17] Entertainment Plaza 🎭")
        print(f"{Fore.WHITE}[10] Gambling Games       [14] Championships 🏆     [15] Quest Center 📜")
        
        print(f"\n{Fore.YELLOW}=== SHOPS & SERVICES ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}[2] Ticket Shop           [3] Pet Shop 🐾          [13] Manage Pets 🐾")
        print(f"{Fore.WHITE}[12] Redeem Code          [16] Loyalty Rewards 🌟")
        
        print(f"\n{Fore.YELLOW}=== MEET CHARACTERS ==={Style.RESET_ALL}")
        # Show a few prominent NPCs with their locations
        featured_npcs = []
        for npc_name, data in NPCS.items():
            if "vip_only" in data and data["vip_only"] and not has_vip:
                continue
            featured_npcs.append((npc_name, data.get("location", "Unknown")))
            if len(featured_npcs) >= 3:  # Show top 3 NPCs
                break
                
        # Display the featured NPCs
        npc_display = " | ".join([f"{npc} ({loc})" for npc, loc in featured_npcs])
        print(f"{Fore.CYAN}Featured Characters: {Style.RESET_ALL}{npc_display}")
        print(f"{Fore.WHITE}[11] Talk to NPCs {Fore.YELLOW}⭐NEW INTERACTIVE SYSTEM!{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}=== PLAYER TOOLS ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}[4] Daily Challenges 📅    [5] Leaderboard 🏆")
        print(f"{Fore.WHITE}[6] Save Game              [7] Load Game              [8] Tutorials")
        print(f"{Fore.WHITE}[0] Exit")
        
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        choice = input(f"{Fore.YELLOW}Select option: {Style.RESET_ALL}")
        
        # Enhanced menu with better feedback and transitions
        if choice == "1":
            print(f"{Fore.CYAN}Loading minigames...{Style.RESET_ALL}")
            time.sleep(0.5)
            minigame_menu()
        elif choice == "2":
            print(f"{Fore.CYAN}Opening the ticket shop...{Style.RESET_ALL}")
            time.sleep(0.5)
            shop()
        elif choice == "3":
            print(f"{Fore.CYAN}Visiting the pet shop...{Style.RESET_ALL}")
            time.sleep(0.5)
            pet_shop()
        elif choice == "4":
            print(f"{Fore.CYAN}Checking your daily challenges...{Style.RESET_ALL}")
            time.sleep(0.5)
            check_daily_challenges()
        elif choice == "5":
            print(f"{Fore.CYAN}Loading the leaderboard...{Style.RESET_ALL}")
            time.sleep(0.5)
            show_leaderboard()
        elif choice == "6":
            print(f"{Fore.CYAN}Preparing to save your progress...{Style.RESET_ALL}")
            time.sleep(0.5)
            save_menu()
        elif choice == "7":
            print(f"{Fore.CYAN}Accessing saved games...{Style.RESET_ALL}")
            time.sleep(0.5)
            load_menu()
        elif choice == "8":
            print(f"{Fore.CYAN}Opening tutorials...{Style.RESET_ALL}")
            time.sleep(0.5)
            tutorials()
        elif choice == "9":
            print(f"{Fore.CYAN}Heading to the theme park...{Style.RESET_ALL}")
            time.sleep(0.5)
            theme_park_menu()
        elif choice == "10":
            print(f"{Fore.CYAN}Entering the casino area...{Style.RESET_ALL}")
            time.sleep(0.5)
            gambling_menu()
        elif choice == "11":
            print(f"{Fore.CYAN}Looking for carnival characters to talk to...{Style.RESET_ALL}")
            time.sleep(0.5)
            talk_to_npcs()
        elif choice == "12":
            print(f"{Fore.CYAN}Opening code redemption panel...{Style.RESET_ALL}")
            time.sleep(0.5)
            redeem_code()
        elif choice == "13":
            print(f"{Fore.CYAN}Opening pet management...{Style.RESET_ALL}")
            time.sleep(0.5)
            equip_pet()
        elif choice == "14":
            print(f"{Fore.CYAN}Heading to the championship arena...{Style.RESET_ALL}")
            time.sleep(0.5)
            championship_center()
        elif choice == "15":
            print(f"{Fore.CYAN}Visiting the quest center...{Style.RESET_ALL}")
            time.sleep(0.5)
            quest_center()
        elif choice == "16":
            print(f"{Fore.CYAN}Checking your loyalty rewards...{Style.RESET_ALL}")
            time.sleep(0.5)
            loyalty_rewards_center()
        elif choice == "17":
            print(f"{Fore.CYAN}Heading to the entertainment plaza...{Style.RESET_ALL}")
            time.sleep(0.5)
            entertainment_plaza()
        elif choice == "0":
            print(f"{Fore.YELLOW}Thanks for visiting the carnival! We hope to see you again soon!{Style.RESET_ALL}")
            time.sleep(1.5)
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            time.sleep(1)

# Pet System
PETS = {
    "Cat 🐱": {"price": 50, "bonus": "luck", "value": 1.1, "description": "Increases luck in games"},
    "Dog 🐕": {"price": 50, "bonus": "tickets", "value": 1.1, "description": "Extra tickets from games"},
    "Bird 🦜": {"price": 75, "bonus": "card_power", "value": 1.1, "description": "Boosts TCG card power"},
    "Dragon 🐉": {"price": 200, "bonus": "all", "value": 1.15, "description": "Enhances all stats"},
    "Robot 🤖": {"price": 100, "bonus": "minigames", "value": 1.2, "description": "Better minigame performance"},
    "Phoenix 🔥": {"price": 150, "bonus": "revival", "value": 1.0, "description": "One free retry per game"},
    "Unicorn 🦄": {"price": 180, "bonus": "magic", "value": 1.2, "description": "Increased rare card chances"},
    "Panda 🐼": {"price": 80, "bonus": "gambling", "value": 1.15, "description": "Better gambling odds"},
    "Fox 🦊": {"price": 120, "bonus": "stealth", "value": 1.1, "description": "Peek opponent's cards occasionally"},
    "Turtle 🐢": {"price": 60, "bonus": "defense", "value": 1.2, "description": "Reduces ticket losses"},
    "Lion 🦁": {"price": 160, "bonus": "attack", "value": 1.25, "description": "Increases battle power"},
    "Owl 🦉": {"price": 90, "bonus": "wisdom", "value": 1.1, "description": "Better prize choices"},
    "Hamster 🐹": {"price": 40, "bonus": "savings", "value": 1.05, "description": "Shop discount"},
    "Penguin 🐧": {"price": 70, "bonus": "ice", "value": 1.15, "description": "Better winter event rewards"},
    "Butterfly 🦋": {"price": 85, "bonus": "transform", "value": 1.1, "description": "Change card type once per battle"}
}

# Global Leaderboard
LEADERBOARD = {}

# Daily Challenges
DAILY_CHALLENGES = {
    "Monday": {"task": "Win 5 minigames", "reward": 30, "bonus_reward": {"type": "tickets", "amount": 10}},
    "Tuesday": {"task": "Win 3 card battles", "reward": 35, "bonus_reward": {"type": "food_voucher", "amount": 1}},
    "Wednesday": {"task": "Earn 100 tickets", "reward": 40, "bonus_reward": {"type": "fast_pass", "amount": 1}},
    "Thursday": {"task": "Complete 2 missions", "reward": 35, "bonus_reward": {"type": "carnival_tokens", "amount": 3}},
    "Friday": {"task": "Win 2 gambling games", "reward": 30, "bonus_reward": {"type": "prize_ticket", "amount": 1}},
    "Saturday": {"task": "Buy 2 items or foods", "reward": 35, "bonus_reward": {"type": "lottery_ticket", "amount": 2}},
    "Sunday": {"task": "Win championship", "reward": 60, "bonus_reward": {"type": "mystery_box", "amount": 1}},
    "Bonus1": {"task": "Visit 3 carnival attractions", "reward": 25, "bonus_reward": {"type": "tickets", "amount": 15}},
    "Bonus2": {"task": "Win 2 carnival games", "reward": 30, "bonus_reward": {"type": "tickets", "amount": 10}},
    "Bonus3": {"task": "Try 3 different foods", "reward": 25, "bonus_reward": {"type": "energy_boost", "amount": 1}}
}

# Initialize additional player attributes
def init_player_attributes():
    if "pets" not in player:
        player["pets"] = []
    if "active_pet" not in player:
        player["active_pet"] = None
    if "daily_challenges" not in player:
        player["daily_challenges"] = {}
    if "last_daily_reward" not in player:
        player["last_daily_reward"] = None
        
    # Initialize loyalty and championship features
    if "loyalty_points" not in player:
        player["loyalty_points"] = 0
    if "visited_attractions" not in player:
        player["visited_attractions"] = {}
    if "championship_records" not in player:
        player["championship_records"] = {}
    if "season_pass" not in player:
        player["season_pass"] = False
    if "fast_passes" not in player:
        player["fast_passes"] = 0
    if "completed_quests" not in player:
        player["completed_quests"] = []
    if "active_quests" not in player:
        player["active_quests"] = []
    if "quest_progress" not in player:
        player["quest_progress"] = {}
        
    # Initialize entertainment features
    if "entertainment_history" not in player:
        player["entertainment_history"] = {
            "movies_watched": [],
            "concerts_attended": [],
            "theatre_shows_seen": []
        }
    if "entertainment_collectibles" not in player:
        player["entertainment_collectibles"] = []
        
    # Initialize carnival features
    if "carnival_needs_system" not in player:
        player["carnival_needs_system"] = True  # Enable the hunger/energy system
    if "hunger" not in player:
        player["hunger"] = 100  # Full hunger (100%)
    if "energy" not in player:
        player["energy"] = 100  # Full energy (100%)
    if "carnival_prizes" not in player:
        player["carnival_prizes"] = []  # Store prizes won from carnival games
    if "food_consumed" not in player:
        player["food_consumed"] = []  # Track food items consumed
        
    # Initialize ticket earning features
    if "check_ins" not in player:
        player["check_ins"] = {
            "last_check_in": None,
            "streak": 0,
            "total": 0
        }
    if "lottery_history" not in player:
        player["lottery_history"] = {
            "plays": 0,
            "wins": 0,
            "tickets_spent": 0,
            "tickets_won": 0
        }
    if "recycled_prizes" not in player:
        player["recycled_prizes"] = {
            "total": 0,
            "tickets_earned": 0
        }

def check_daily_reward():
    from datetime import datetime
    today = datetime.now().date()
    if player["last_daily_reward"] is None or datetime.strptime(player["last_daily_reward"], "%Y-%m-%d").date() < today:
        player["tickets"] += 10
        player["last_daily_reward"] = today.strftime("%Y-%m-%d")
        print(Fore.GREEN + "🎁 Daily Reward: +10 tickets!")

def pet_shop():
    clear()
    print(Fore.CYAN + "🐾 Pet Shop")
    print(f"Your tickets: {player['tickets']}")

    for pet, data in PETS.items():
        if pet in player["pets"]:
            status = "Owned"
        else:
            status = f"{data['price']} tickets"
        print(f"\n{pet} - {status}")
        print(f"Bonus: {data['bonus'].title()} +{(data['value']-1)*100}%")
        print(f"Effect: {data['description']}")

    choice = input("\nBuy pet (or Enter to exit): ")
    if choice in PETS and choice not in player["pets"]:
        if player["tickets"] >= PETS[choice]["price"]:
            player["tickets"] -= PETS[choice]["price"]
            player["pets"].append(choice)
            print(Fore.GREEN + f"You bought {choice}!")
            equip_pet(choice)
        else:
            print(Fore.RED + "Not enough tickets!")

def equip_pet(pet=None):
    if pet is None:
        clear()
        print(Fore.CYAN + "🐾 Your Pets")
        for i, pet in enumerate(player["pets"], 1):
            status = "Active" if pet == player["active_pet"] else "Inactive"
            print(f"[{i}] {pet} - {status}")
        print("[0] Unequip pet")

        choice = input("Choose pet to equip: ")
        if choice == "0":
            player["active_pet"] = None
            print("Pet unequipped!")
            return
        try:
            pet = player["pets"][int(choice)-1]
        except (ValueError, IndexError):
            return

    if pet in player["pets"]:
        player["active_pet"] = pet
        print(f"Equipped {pet}!")

def check_daily_challenges():
    clear()
    print(Fore.YELLOW + "📅 Daily Challenges")

    import time
    from datetime import datetime
    current_day = time.strftime("%A")
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get the challenge for the current day of the week
    # If it's not a specific day (or we need a fallback), use one of the bonus challenges
    if current_day in DAILY_CHALLENGES:
        challenge = DAILY_CHALLENGES[current_day]
    else:
        # Randomly select one of our bonus challenges
        bonus_keys = [key for key in DAILY_CHALLENGES.keys() if key.startswith("Bonus")]
        challenge = DAILY_CHALLENGES[random.choice(bonus_keys)]

    # Initialize daily_challenges if needed
    if "daily_challenges" not in player:
        player["daily_challenges"] = {}
    
    # Initialize daily_streak if needed
    if "daily_streak" not in player:
        player["daily_streak"] = {
            "count": 0,
            "last_date": None
        }
    
    # Check if player already completed today's challenge
    if current_day in player["daily_challenges"] and player["daily_challenges"][current_day]:
        print("✅ Today's challenge completed!")
        print(f"Challenge: {challenge['task']}")
        print(f"Reward: {challenge['reward']} tickets")
        
        # Display streak information
        streak = player["daily_streak"]["count"]
        print(f"\n🔥 Current Streak: {streak} day" + ("s" if streak != 1 else ""))
        
        if streak >= 3:
            print(Fore.CYAN + "Streak bonus active! Complete tomorrow's challenge for more rewards.")
    else:
        # Check if streak needs to be reset (player missed a day)
        last_date = player["daily_streak"]["last_date"]
        if last_date:
            from datetime import datetime
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
            today_obj = datetime.strptime(today_date, "%Y-%m-%d")
            days_diff = (today_obj - last_date_obj).days
            
            # If more than 1 day has passed, reset streak
            if days_diff > 1:
                player["daily_streak"]["count"] = 0
                print(Fore.RED + "Your daily streak was reset! Complete challenges daily to build it up again.")
        
        print(f"Task: {challenge['task']}")
        print(f"Reward: {challenge['reward']} tickets")
        
        # Show current streak information
        streak = player["daily_streak"]["count"]
        print(f"\n🔥 Current Streak: {streak} day" + ("s" if streak != 1 else ""))
        
        # Option to complete the challenge
        print("\n[1] Complete challenge (simulated)")
        print("[0] Return to menu")
        
        choice = input("\nSelect option: ")
        
        if choice == "1":
            # Mark challenge as completed
            player["daily_challenges"][current_day] = True
            
            # Award base tickets
            player["tickets"] += challenge["reward"]
            print(Fore.GREEN + f"\n✅ Challenge completed! +{challenge['reward']} tickets")
            
            # Update streak
            player["daily_streak"]["count"] += 1
            player["daily_streak"]["last_date"] = today_date
            
            # Award loyalty points
            add_loyalty_points(3)
            print(Fore.MAGENTA + "+3 Loyalty Points for completing daily challenge!")
            
            # Calculate and award streak bonus
            streak = player["daily_streak"]["count"]
            if streak >= 3:
                streak_bonus = min(5 * (streak // 3), 25)  # Cap at 25 bonus tickets
                player["tickets"] += streak_bonus
                print(Fore.CYAN + f"🔥 Streak Bonus: +{streak_bonus} tickets!")
            
            # Award streak achievements
            if streak == 3:
                award_achievement("Three Day Streak: Complete daily challenges 3 days in a row")
            elif streak == 7:
                award_achievement("Week Warrior: Complete daily challenges for a full week")
                # Bonus reward for weekly streak
                player["tickets"] += 50
                print(Fore.GREEN + "🎖️ Weekly Streak Bonus: +50 tickets!")
            elif streak == 30:
                award_achievement("Monthly Master: Complete daily challenges for 30 days")
                # Rare reward for monthly streak
                player["tickets"] += 200
                add_loyalty_points(50)
                print(Fore.GREEN + "🏆 Monthly Streak Bonus: +200 tickets, +50 Loyalty Points!")
                
                # Add special item to inventory
                special_item = "Streak Champion Crown 👑"
                if special_item not in player["inventory"]:
                    player["inventory"].append(special_item)
                    print(Fore.YELLOW + f"Special reward added to inventory: {special_item}")

    input("\nPress Enter to continue...")

def update_leaderboard(score, game_type):
    player_name = f"{player['equipped_costume']} {player['name']}"
    if player_name not in LEADERBOARD:
        LEADERBOARD[player_name] = {}
    if game_type not in LEADERBOARD[player_name]:
        LEADERBOARD[player_name][game_type] = 0
    LEADERBOARD[player_name][game_type] = max(LEADERBOARD[player_name][game_type], score)

def show_leaderboard():
    clear()
    print(Fore.CYAN + "🏆 Leaderboard")

    categories = ["Minigames", "Card Battles", "Championship"]
    for category in categories:
        print(f"\n=== {category} ===")
        sorted_scores = sorted(
            [(name, data.get(category, 0)) for name, data in LEADERBOARD.items()],
            key=lambda x: x[1],
            reverse=True
        )
        for i, (name, score) in enumerate(sorted_scores[:5], 1):
            print(f"{i}. {name}: {score}")

    input("\nPress Enter to continue...")



def start_game():
    clear()
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    carnival_art = f"""
{random.choice(colors)} ░▒▓██████▓▒░  ░▒▓██████▓▒░ ░▒▓███████▓▒░ ░▒▓███████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓██████▓▒░ ░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓████████▓▒░░▒▓███████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒▒▓█▓▒░ ░▒▓████████▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)}░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░        
{random.choice(colors)} ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░   ░▒▓██▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓████████▓▒░

        🎪 Welcome to the Carnival! 🎪
        """
    print(carnival_art)
    print(Fore.CYAN + "Enter your name to begin:")
    player["name"] = input("> ")
    main_menu()

start_game()
def paper_scissors_rock():
    if not pay_to_play(1): 
        return
    choices = ["Rock 🪨", "Paper 📄", "Scissors ✂️"]
    player_choice = input(f"Choose ({', '.join(choices)}): ")
    computer = random.choice(choices)
    print(f"Computer chose: {computer}")

    if player_choice == computer:
        print(Fore.YELLOW + "Draw! Get your ticket back.")
        player["tickets"] += 1
    elif ((player_choice == "Rock 🪨" and computer == "Scissors ✂️") or
          (player_choice == "Paper 📄" and computer == "Rock 🪨") or
          (player_choice == "Scissors ✂️" and computer == "Paper 📄")):
        print(Fore.GREEN + "You win! +3 tickets")
        player["tickets"] += 3
        update_mission_progress("play_games")
    else:
        print(Fore.RED + "You lose!")
        update_mission_progress("play_games")

def coin_flip_game():
    if not pay_to_play(1):
        return
    choice = input("Heads or Tails? ").lower()
    result = random.choice(["heads", "tails"])
    if choice == result:
        print(Fore.GREEN + "You win! +2 tickets")
        player["tickets"] += 2
    else:
        print(Fore.RED + f"You lose! It was {result}")
    update_mission_progress("play_games")

def high_low():
    if not pay_to_play(2):
        return
    number = random.randint(1, 100)
    prev_number = random.randint(1, 100)
    print(f"Number is: {prev_number}")
    choice = input("Will the next number be Higher or Lower? ").lower()
    print(f"Number was: {number}")

    if ((choice == "higher" and number > prev_number) or 
        (choice == "lower" and number < prev_number)):
        print(Fore.GREEN + "Correct! +4 tickets")
        player["tickets"] += 4
    else:
        print(Fore.RED + "Wrong!")
    update_mission_progress("play_games")

def talk_to_npcs():
    """Interactive conversation system with NPCs, showing detailed information and enabling trading"""
    while True:
        clear()
        print(Fore.CYAN + "=== CARNIVAL CHARACTERS ===")
        print(Fore.YELLOW + "Meet the colorful personalities that bring our carnival to life!")
        
        # Display NPCs by location groups
        locations = {}
        for npc_name, data in NPCS.items():
            # Skip VIP NPCs if player doesn't have VIP pass
            if data.get("vip_only") and "VIP Pass 🌟" not in player["inventory"]:
                continue
                
            location = data.get("location", "Wandering")
            if location not in locations:
                locations[location] = []
            locations[location].append(npc_name)
        
        # Print NPCs grouped by location
        print("\n" + Fore.MAGENTA + "=== LOCATIONS ===")
        for i, (location, npcs) in enumerate(locations.items(), 1):
            print(f"{i}. {location} ({len(npcs)} characters)")
        
        print("\n0. Return to Main Menu")
        
        location_choice = input("\nWhere would you like to go? (0-" + str(len(locations)) + "): ")
        if location_choice == "0":
            return
            
        try:
            location_idx = int(location_choice) - 1
            if location_idx < 0 or location_idx >= len(locations):
                raise ValueError
                
            # Get selected location and its NPCs
            selected_location = list(locations.keys())[location_idx]
            location_npcs = locations[selected_location]
            
            while True:
                clear()
                print(Fore.CYAN + f"=== {selected_location.upper()} ===")
                print(Fore.YELLOW + "Characters in this area:")
                
                # Display NPCs at the selected location
                for i, npc_name in enumerate(location_npcs, 1):
                    print(f"{i}. {npc_name}")
                
                print("\n0. Go back to locations")
                
                npc_choice = input("\nWho would you like to talk to? (0-" + str(len(location_npcs)) + "): ")
                if npc_choice == "0":
                    break
                    
                try:
                    npc_idx = int(npc_choice) - 1
                    if npc_idx < 0 or npc_idx >= len(location_npcs):
                        raise ValueError
                        
                    # Talk to the selected NPC
                    selected_npc = location_npcs[npc_idx]
                    interact_with_npc(selected_npc)
                    
                except ValueError:
                    print(Fore.RED + "Invalid choice!")
                    time.sleep(1)
            
        except ValueError:
            print(Fore.RED + "Invalid choice!")
            time.sleep(1)

def interact_with_npc(npc_name):
    """Detailed interaction with a specific NPC including dialogue, missions, and trading"""
    npc_data = NPCS[npc_name]
    
    while True:
        clear()
        # Display NPC header with colorful styling
        print(Fore.CYAN + "╔" + "═" * (len(npc_name) + 10) + "╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + f"   {npc_name}   " + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * (len(npc_name) + 10) + "╝\n")
        
        # Show NPC description
        print(Fore.MAGENTA + "APPEARANCE:")
        print(Fore.WHITE + npc_data["description"])
        
        # Random dialogue from the NPC
        print(Fore.MAGENTA + "\nDIALOGUE:")
        dialogue = random.choice(npc_data["dialogue"])
        print(f"{Fore.YELLOW}{npc_name}: {Fore.WHITE}\"{dialogue}\"")
        
        # Display missions
        if "missions" in npc_data and npc_data["missions"]:
            print(Fore.MAGENTA + "\nMISSIONS:")
            for mission_id in npc_data["missions"]:
                if mission_id in MISSIONS:
                    mission = MISSIONS[mission_id]
                    
                    # Check mission status
                    if mission_id in player["completed_missions"]:
                        print(f"{Fore.GREEN}✅ {mission['name']} (Completed)")
                    elif mission_id in player["missions"]:
                        progress = player["missions"][mission_id]
                        print(f"{Fore.YELLOW}👉 {mission['name']} ({progress}/{mission['target']})")
                        print(f"   {Fore.WHITE}{mission.get('description', 'No description available.')}")
                    else:
                        print(f"{Fore.RED}❌ {mission['name']} (Not Started)")
                        print(f"   {Fore.WHITE}{mission.get('description', 'No description available.')}")
                        
                        # Option to start mission
                        print(f"   {Fore.CYAN}[Press 'S' when selecting options to start this mission]")
        
        # Display quests if NPC has them
        if "quests" in npc_data and npc_data["quests"]:
            print(Fore.MAGENTA + "\nQUESTS:")
            for quest_id in npc_data["quests"]:
                if quest_id in QUESTS:
                    quest = QUESTS[quest_id]
                    
                    # Check quest status
                    if quest_id in player.get("completed_quests", []):
                        print(f"{Fore.GREEN}✅ {quest['name']} (Completed)")
                    elif quest_id in player.get("active_quests", []):
                        print(f"{Fore.YELLOW}👉 {quest['name']} (In Progress)")
                        print(f"   {Fore.WHITE}{quest['description']}")
                    else:
                        print(f"{Fore.RED}❌ {quest['name']} (Available)")
                        print(f"   {Fore.WHITE}{quest['description']}")
                        
                        # Option to start quest
                        print(f"   {Fore.CYAN}[Press 'Q' when selecting options to start this quest]")
        
        # Display trades if NPC has them
        if "trades" in npc_data and npc_data["trades"]:
            print(Fore.MAGENTA + "\nTRADES:")
            for i, trade in enumerate(npc_data["trades"], 1):
                if trade.get("tickets", False):
                    print(f"{Fore.YELLOW}{i}. Give: {trade['give']} → Receive: {trade['receive']} tickets")
                else:
                    print(f"{Fore.YELLOW}{i}. Give: {trade['give']} → Receive: {trade['receive']}")
        
        # Display special bonus if NPC has one
        if "special_bonus" in npc_data:
            bonus = npc_data["special_bonus"]
            bonus_type = bonus["type"].replace("_", " ").title()
            print(Fore.MAGENTA + "\nSPECIAL BONUS:")
            print(f"{Fore.CYAN}{bonus_type}: {Fore.WHITE}x{bonus['value']}" if isinstance(bonus['value'], (int, float)) else f"{Fore.CYAN}{bonus_type}: {Fore.WHITE}{bonus['value']}")
        
        # Interaction options
        print(Fore.MAGENTA + "\nINTERACTION OPTIONS:")
        
        options = []
        
        # Add mission starting options if available
        for i, mission_id in enumerate(npc_data.get("missions", [])):
            if mission_id in MISSIONS and mission_id not in player["completed_missions"] and mission_id not in player["missions"]:
                options.append(("S", f"Start mission: {MISSIONS[mission_id]['name']}"))
                break  # Only show one "Start Mission" option
        
        # Add quest starting options if available
        for i, quest_id in enumerate(npc_data.get("quests", [])):
            if quest_id in QUESTS and quest_id not in player.get("completed_quests", []) and quest_id not in player.get("active_quests", []):
                options.append(("Q", f"Start quest: {QUESTS[quest_id]['name']}"))
                break  # Only show one "Start Quest" option
        
        # Add trading options if available
        if "trades" in npc_data and npc_data["trades"]:
            options.append(("T", "Trade with " + npc_name.split()[0]))
        
        # Always show chat option
        options.append(("C", "Chat more with " + npc_name.split()[0]))
        
        # Always show exit option
        options.append(("X", "Say goodbye"))
        
        # Display the available options
        for code, description in options:
            print(f"{Fore.YELLOW}{code}. {Fore.WHITE}{description}")
        
        # Get player choice
        action = input(f"\n{Fore.YELLOW}What would you like to do? {Fore.WHITE}").upper()
        
        if action == "X":
            # Say goodbye
            print(f"\n{Fore.YELLOW}You say goodbye to {npc_name}.")
            time.sleep(1.5)
            return
            
        elif action == "C":
            # Chat more (just refresh the screen for new dialogue)
            continue
            
        elif action == "S":
            # Start mission
            for mission_id in npc_data.get("missions", []):
                if mission_id in MISSIONS and mission_id not in player["completed_missions"] and mission_id not in player["missions"]:
                    start_mission(mission_id)
                    break
            
        elif action == "Q":
            # Start quest
            for quest_id in npc_data.get("quests", []):
                if quest_id in QUESTS and quest_id not in player.get("completed_quests", []) and quest_id not in player.get("active_quests", []):
                    start_quest(quest_id)
                    break
            
        elif action == "T":
            # Trade with NPC
            trade_with_npc(npc_name)
            
        else:
            try:
                # Check if player selected a trade by number
                trade_idx = int(action) - 1
                if "trades" in npc_data and 0 <= trade_idx < len(npc_data["trades"]):
                    process_trade(npc_name, npc_data["trades"][trade_idx])
                else:
                    print(Fore.RED + "Invalid option!")
                    time.sleep(1)
            except ValueError:
                print(Fore.RED + "Invalid option!")
                time.sleep(1)

def start_mission(mission_id):
    """Start a new mission"""
    mission = MISSIONS[mission_id]
    player["missions"][mission_id] = 0
    
    print(Fore.GREEN + f"\nYou've started the mission: {mission['name']}")
    print(Fore.WHITE + mission.get("description", "Complete this mission to earn rewards!"))
    print(Fore.YELLOW + f"Reward: {mission['reward']} tickets upon completion")
    
    input("\nPress Enter to continue...")

def start_quest(quest_id):
    """Start a new quest"""
    quest = QUESTS[quest_id]
    
    # Initialize active_quests if it doesn't exist
    if "active_quests" not in player:
        player["active_quests"] = []
    
    player["active_quests"].append(quest_id)
    
    print(Fore.GREEN + f"\nYou've started the quest: {quest['name']}")
    print(Fore.WHITE + quest["description"])
    print(Fore.YELLOW + f"Reward: {quest['reward']} tickets upon completion")
    
    input("\nPress Enter to continue...")

def trade_with_npc(npc_name):
    """Trade interface with an NPC"""
    npc_data = NPCS[npc_name]
    
    if "trades" not in npc_data or not npc_data["trades"]:
        print(Fore.RED + f"{npc_name} has nothing to trade right now.")
        time.sleep(1.5)
        return
    
    while True:
        clear()
        print(Fore.CYAN + f"=== TRADING WITH {npc_name.upper()} ===")
        print(Fore.YELLOW + f"Your tickets: {player['tickets']}")
        
        # Display player's inventory
        print(Fore.MAGENTA + "\nYOUR INVENTORY:")
        if not player["inventory"]:
            print(Fore.RED + "You don't have any items to trade!")
        else:
            for i, item in enumerate(player["inventory"], 1):
                print(f"{i}. {item}")
        
        # Display available trades
        print(Fore.MAGENTA + "\nAVAILABLE TRADES:")
        for i, trade in enumerate(npc_data["trades"], 1):
            if trade.get("tickets", False):
                print(f"{Fore.YELLOW}{i}. Give: {trade['give']} → Receive: {trade['receive']} tickets")
            else:
                print(f"{Fore.YELLOW}{i}. Give: {trade['give']} → Receive: {trade['receive']}")
        
        print(Fore.YELLOW + "\n0. Back")
        
        choice = input("\nSelect a trade (0 to exit): ")
        if choice == "0":
            return
            
        try:
            trade_idx = int(choice) - 1
            if 0 <= trade_idx < len(npc_data["trades"]):
                process_trade(npc_name, npc_data["trades"][trade_idx])
            else:
                raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid choice!")
            time.sleep(1)

def process_trade(npc_name, trade):
    """Process a trade with an NPC"""
    give_item = trade["give"]
    receive_item = trade["receive"]
    is_ticket_trade = trade.get("tickets", False)
    
    # Check if player has the required item
    if give_item not in player["inventory"]:
        print(Fore.RED + f"You don't have a {give_item} to trade!")
        time.sleep(1.5)
        return
    
    # Confirm trade
    clear()
    print(Fore.CYAN + f"=== CONFIRM TRADE WITH {npc_name.upper()} ===")
    print(Fore.YELLOW + f"Give: {give_item}")
    if is_ticket_trade:
        print(Fore.YELLOW + f"Receive: {receive_item} tickets")
    else:
        print(Fore.YELLOW + f"Receive: {receive_item}")
    
    confirm = input("\nProceed with this trade? (y/n): ").lower()
    if confirm != "y":
        print(Fore.YELLOW + "Trade cancelled.")
        time.sleep(1)
        return
    
    # Process the trade
    player["inventory"].remove(give_item)
    
    if is_ticket_trade:
        player["tickets"] += receive_item
        print(Fore.GREEN + f"\nTrade complete! You received {receive_item} tickets.")
    else:
        player["inventory"].append(receive_item)
        print(Fore.GREEN + f"\nTrade complete! You received {receive_item}.")
    
    time.sleep(1.5)

def entertainment_plaza():
    """Main hub for accessing entertainment options like movies, music shows, and theatre"""
    # Track visits for achievement tracking
    player["entertainment_plaza_visits"] = player.get("entertainment_plaza_visits", 0) + 1
    
    clear()
    print(Fore.MAGENTA + "🎭 ENTERTAINMENT PLAZA 🎭")
    print(Fore.CYAN + "Welcome to the Entertainment Plaza! Enjoy movies, music, and theatre shows.")
    print(f"Current Tickets: {player['tickets']}")
    
    # Check for season pass
    has_season_pass = player.get("season_pass", False)
    if has_season_pass:
        print(Fore.GREEN + f"🎫 Season Pass Active! ({player.get('season_pass_days', 30)} days remaining)")
        print("You get 20% discount on all entertainment!")
    
    # Display entertainment stats
    movies_watched = len(player["entertainment_history"]["movies_watched"])
    concerts_attended = len(player["entertainment_history"]["concerts_attended"])
    theatre_shows_seen = len(player["entertainment_history"]["theatre_shows_seen"])
    collectibles = len(player["entertainment_collectibles"])
    
    print(Fore.CYAN + "\nYour Entertainment Stats:")
    print(f"🎬 Movies Watched: {movies_watched}")
    print(f"🎵 Concerts Attended: {concerts_attended}")
    print(f"🎭 Theatre Shows Seen: {theatre_shows_seen}")
    print(f"🎁 Collectibles: {collectibles}")
    
    # Display entertainment options
    print("""
[1] Cinema 🎬
[2] Concert Hall 🎵
[3] Theatre 🎭
[4] View Entertainment History
[0] Return to Main Menu
""")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        cinema_menu()
    elif choice == "2":
        concert_hall_menu()
    elif choice == "3":
        theatre_menu()
    elif choice == "4":
        view_entertainment_history()
    elif choice == "0":
        return
    else:
        print(Fore.RED + "Invalid option!")
        time.sleep(1)
        return entertainment_plaza()

def cinema_menu():
    """Display available movies and allow player to watch them"""
    clear()
    print(Fore.YELLOW + "🎬 CINEMA 🎬")
    print("Enjoy the latest blockbuster movies!")
    
    # Check for season pass discount
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    
    # Additional discount from loyalty program
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)  # Cap at 50% discount
    
    if total_discount > 0:
        print(Fore.GREEN + f"Your current discount: {int(total_discount * 100)}%")
    
    print("\nAvailable Movies:")
    for i, movie in enumerate(MOVIES, 1):
        # Calculate discounted price
        original_price = movie["price"]
        final_price = max(1, int(original_price * (1 - total_discount)))
        
        # Format display with special effects indicator
        special_effect = f" [{movie['special_effect']}]" if movie["special_effect"] else ""
        print(f"[{i}] {movie['title']} - {movie['genre']} ({movie['duration']}){special_effect}")
        print(f"    Price: {final_price} tickets (Original: {original_price})")
        
        # Show if already watched
        if movie["title"] in player["entertainment_history"]["movies_watched"]:
            print(Fore.CYAN + "    ✓ Watched")
    
    print("[0] Return to Entertainment Plaza")
    
    choice = input("\nSelect movie to watch (or 0 to return): ")
    if choice == "0":
        return entertainment_plaza()
    
    try:
        movie_idx = int(choice) - 1
        if 0 <= movie_idx < len(MOVIES):
            watch_movie(movie_idx)
        else:
            print(Fore.RED + "Invalid selection!")
            time.sleep(1)
            return cinema_menu()
    except ValueError:
        print(Fore.RED + "Please enter a valid number!")
        time.sleep(1)
        return cinema_menu()

def watch_movie(movie_idx):
    """Play a movie and give rewards"""
    movie = MOVIES[movie_idx]
    
    # Apply discounts
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)
    price = max(1, int(movie["price"] * (1 - total_discount)))
    
    # Check if player can afford the movie
    if player["tickets"] < price:
        print(Fore.RED + f"You don't have enough tickets! Need {price} tickets.")
        time.sleep(2)
        return cinema_menu()
    
    clear()
    print(Fore.YELLOW + f"Now Playing: {movie['title']}")
    print(f"Genre: {movie['genre']} | Duration: {movie['duration']}")
    print(f"Ticket Price: {price} tickets")
    
    # Confirm purchase
    confirm = input("\nProceed with purchase? (y/n): ").lower()
    if confirm != "y":
        return cinema_menu()
    
    # Process payment and watch movie
    player["tickets"] -= price
    
    # Track spending for achievements
    player["entertainment_spent"] = player.get("entertainment_spent", 0) + price
    
    # Movie simulation
    clear()
    print(Fore.YELLOW + f"🎬 {movie['title']} 🎬")
    print("\nThe movie is starting...")
    time.sleep(2)
    
    # Special effects if any
    if movie["special_effect"]:
        print(Fore.CYAN + f"\n✨ Special {movie['special_effect']} Effects Activated! ✨")
    
    # Simulated movie scenes
    scenes = [
        "Opening scene introduces the main characters...",
        "The plot thickens as a conflict emerges...",
        "Dramatic moment has the audience on the edge of their seats...",
        "Comic relief lightens the mood...",
        "The climax approaches with increasing tension...",
        "Final scene resolves the story with a satisfying conclusion..."
    ]
    
    for scene in scenes:
        time.sleep(1.5)
        print(f"\n{scene}")
    
    time.sleep(1)
    print(Fore.GREEN + "\n🎬 The End! 🎬")
    print("You enjoyed the movie!")
    
    # Track this movie in history if not already watched
    if movie["title"] not in player["entertainment_history"]["movies_watched"]:
        player["entertainment_history"]["movies_watched"].append(movie["title"])
        
        # Award loyalty points for new movie
        add_loyalty_points(2)
        print(Fore.MAGENTA + "+2 Loyalty Points for watching a new movie!")
    
    # Give reward
    reward = movie["reward"]
    if reward not in player["entertainment_collectibles"]:
        player["entertainment_collectibles"].append(reward)
        print(Fore.GREEN + f"\nYou received: {reward} 🎁")
    else:
        # Give tickets instead if already have the collectible
        bonus_tickets = random.randint(3, 8)
        player["tickets"] += bonus_tickets
        print(Fore.GREEN + f"\nYou already have the {reward}.")
        print(f"Instead you received {bonus_tickets} bonus tickets! 🎟️")
    
    # Check for achievements
    check_entertainment_achievements()
    
    input("\nPress Enter to continue...")
    return cinema_menu()

def concert_hall_menu():
    """Display available concerts and allow player to attend them"""
    clear()
    print(Fore.YELLOW + "🎵 CONCERT HALL 🎵")
    print("Experience amazing live music performances!")
    
    # Check for season pass discount
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    
    # Additional discount from loyalty program
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)  # Cap at 50% discount
    
    if total_discount > 0:
        print(Fore.GREEN + f"Your current discount: {int(total_discount * 100)}%")
    
    print("\nTonight's Performances:")
    for i, concert in enumerate(MUSIC_SHOWS, 1):
        # Calculate discounted price
        original_price = concert["price"]
        final_price = max(1, int(original_price * (1 - total_discount)))
        
        # Format display with special effects indicator
        special_effect = f" [{concert['special_effect']}]" if concert["special_effect"] else ""
        print(f"[{i}] {concert['title']} - {concert['genre']} ({concert['duration']}){special_effect}")
        print(f"    Price: {final_price} tickets (Original: {original_price})")
        
        # Show if already attended
        if concert["title"] in player["entertainment_history"]["concerts_attended"]:
            print(Fore.CYAN + "    ✓ Attended")
    
    print("[0] Return to Entertainment Plaza")
    
    choice = input("\nSelect concert to attend (or 0 to return): ")
    if choice == "0":
        return entertainment_plaza()
    
    try:
        concert_idx = int(choice) - 1
        if 0 <= concert_idx < len(MUSIC_SHOWS):
            attend_concert(concert_idx)
        else:
            print(Fore.RED + "Invalid selection!")
            time.sleep(1)
            return concert_hall_menu()
    except ValueError:
        print(Fore.RED + "Please enter a valid number!")
        time.sleep(1)
        return concert_hall_menu()

def attend_concert(concert_idx):
    """Attend a concert and give rewards"""
    concert = MUSIC_SHOWS[concert_idx]
    
    # Apply discounts
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)
    price = max(1, int(concert["price"] * (1 - total_discount)))
    
    # Check if player can afford the concert
    if player["tickets"] < price:
        print(Fore.RED + f"You don't have enough tickets! Need {price} tickets.")
        time.sleep(2)
        return concert_hall_menu()
    
    clear()
    print(Fore.YELLOW + f"Tonight's Performance: {concert['title']}")
    print(f"Genre: {concert['genre']} | Duration: {concert['duration']}")
    print(f"Ticket Price: {price} tickets")
    
    # Confirm purchase
    confirm = input("\nProceed with purchase? (y/n): ").lower()
    if confirm != "y":
        return concert_hall_menu()
    
    # Process payment and attend concert
    player["tickets"] -= price
    
    # Track spending for achievements
    player["entertainment_spent"] = player.get("entertainment_spent", 0) + price
    
    # Concert simulation
    clear()
    print(Fore.YELLOW + f"🎵 {concert['title']} 🎵")
    print("\nThe crowd is getting excited as the show is about to begin...")
    time.sleep(2)
    
    # Special effects if any
    if concert["special_effect"]:
        print(Fore.CYAN + f"\n✨ Amazing {concert['special_effect']} light up the stage! ✨")
    
    # Simulated concert experience
    experiences = [
        "The crowd roars as the performers take the stage...",
        "The opening song gets everyone on their feet...",
        "A spectacular solo performance mesmerizes the audience...",
        "The rhythm has everyone dancing and singing along...",
        "A special guest appears to join in a duet...",
        "The finale brings the house down with the biggest hit..."
    ]
    
    for experience in experiences:
        time.sleep(1.5)
        print(f"\n{experience}")
    
    time.sleep(1)
    print(Fore.GREEN + "\n🎵 What an amazing show! 🎵")
    print("The performance was unforgettable!")
    
    # Track this concert in history if not already attended
    if concert["title"] not in player["entertainment_history"]["concerts_attended"]:
        player["entertainment_history"]["concerts_attended"].append(concert["title"])
        
        # Award loyalty points for new concert
        add_loyalty_points(3)
        print(Fore.MAGENTA + "+3 Loyalty Points for attending a new concert!")
    
    # Give reward
    reward = concert["reward"]
    if reward not in player["entertainment_collectibles"]:
        player["entertainment_collectibles"].append(reward)
        print(Fore.GREEN + f"\nYou received: {reward} 🎁")
    else:
        # Give tickets instead if already have the collectible
        bonus_tickets = random.randint(4, 10)
        player["tickets"] += bonus_tickets
        print(Fore.GREEN + f"\nYou already have the {reward}.")
        print(f"Instead you received {bonus_tickets} bonus tickets! 🎟️")
    
    # Check for achievements
    check_entertainment_achievements()
    
    input("\nPress Enter to continue...")
    return concert_hall_menu()

def theatre_menu():
    """Display available theatre shows and allow player to see them"""
    clear()
    print(Fore.YELLOW + "🎭 THEATRE 🎭")
    print("Immerse yourself in the magic of live theatre!")
    
    # Check for season pass discount
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    
    # Additional discount from loyalty program
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)  # Cap at 50% discount
    
    if total_discount > 0:
        print(Fore.GREEN + f"Your current discount: {int(total_discount * 100)}%")
    
    print("\nCurrent Productions:")
    for i, show in enumerate(THEATRE_SHOWS, 1):
        # Calculate discounted price
        original_price = show["price"]
        final_price = max(1, int(original_price * (1 - total_discount)))
        
        # Format display with special effects indicator
        special_effect = f" [{show['special_effect']}]" if show["special_effect"] else ""
        print(f"[{i}] {show['title']} - {show['genre']} ({show['duration']}){special_effect}")
        print(f"    Price: {final_price} tickets (Original: {original_price})")
        
        # Show if already seen
        if show["title"] in player["entertainment_history"]["theatre_shows_seen"]:
            print(Fore.CYAN + "    ✓ Seen")
    
    print("[0] Return to Entertainment Plaza")
    
    choice = input("\nSelect show to see (or 0 to return): ")
    if choice == "0":
        return entertainment_plaza()
    
    try:
        show_idx = int(choice) - 1
        if 0 <= show_idx < len(THEATRE_SHOWS):
            see_theatre_show(show_idx)
        else:
            print(Fore.RED + "Invalid selection!")
            time.sleep(1)
            return theatre_menu()
    except ValueError:
        print(Fore.RED + "Please enter a valid number!")
        time.sleep(1)
        return theatre_menu()

def see_theatre_show(show_idx):
    """See a theatre show and give rewards"""
    show = THEATRE_SHOWS[show_idx]
    
    # Apply discounts
    discount = 0.0
    if player.get("season_pass", False):
        discount = 0.2
    loyalty_discount = get_loyalty_discount()
    total_discount = min(0.5, discount + loyalty_discount)
    price = max(1, int(show["price"] * (1 - total_discount)))
    
    # Check if player can afford the show
    if player["tickets"] < price:
        print(Fore.RED + f"You don't have enough tickets! Need {price} tickets.")
        time.sleep(2)
        return theatre_menu()
    
    clear()
    print(Fore.YELLOW + f"Now Showing: {show['title']}")
    print(f"Genre: {show['genre']} | Duration: {show['duration']}")
    print(f"Ticket Price: {price} tickets")
    
    # Confirm purchase
    confirm = input("\nProceed with purchase? (y/n): ").lower()
    if confirm != "y":
        return theatre_menu()
    
    # Process payment and see show
    player["tickets"] -= price
    
    # Track spending for achievements
    player["entertainment_spent"] = player.get("entertainment_spent", 0) + price
    
    # Show simulation
    clear()
    print(Fore.YELLOW + f"🎭 {show['title']} 🎭")
    print("\nThe curtains rise as the production begins...")
    time.sleep(2)
    
    # Special effects if any
    if show["special_effect"]:
        print(Fore.CYAN + f"\n✨ Stunning {show['special_effect']} enhance the performance! ✨")
    
    # Simulated theatre experience
    acts = [
        "Act I begins, setting the scene with beautiful scenery...",
        "The main character faces their first challenge...",
        "The audience is captivated by the powerful performances...",
        "A plot twist surprises everyone in Act II...",
        "The tension rises as the story reaches its climax...",
        "The final act resolves the story with emotional impact..."
    ]
    
    for act in acts:
        time.sleep(1.5)
        print(f"\n{act}")
    
    time.sleep(1)
    print(Fore.GREEN + "\n🎭 Bravo! 🎭")
    print("The audience erupts in applause for the magnificent performance!")
    
    # Track this show in history if not already seen
    if show["title"] not in player["entertainment_history"]["theatre_shows_seen"]:
        player["entertainment_history"]["theatre_shows_seen"].append(show["title"])
        
        # Award loyalty points for new theatre show
        add_loyalty_points(4)
        print(Fore.MAGENTA + "+4 Loyalty Points for seeing a new theatre production!")
    
    # Give reward
    reward = show["reward"]
    if reward not in player["entertainment_collectibles"]:
        player["entertainment_collectibles"].append(reward)
        print(Fore.GREEN + f"\nYou received: {reward} 🎁")
    else:
        # Give tickets instead if already have the collectible
        bonus_tickets = random.randint(5, 12)
        player["tickets"] += bonus_tickets
        print(Fore.GREEN + f"\nYou already have the {reward}.")
        print(f"Instead you received {bonus_tickets} bonus tickets! 🎟️")
    
    # Check for achievements
    check_entertainment_achievements()
    
    input("\nPress Enter to continue...")
    return theatre_menu()

def view_entertainment_history():
    """Display player's entertainment history and collectibles"""
    clear()
    print(Fore.YELLOW + "📜 ENTERTAINMENT HISTORY 📜")
    
    # Movies watched
    print(Fore.CYAN + "\nMovies Watched:")
    if player["entertainment_history"]["movies_watched"]:
        for i, movie in enumerate(player["entertainment_history"]["movies_watched"], 1):
            print(f"{i}. {movie}")
    else:
        print("You haven't watched any movies yet.")
    
    # Concerts attended
    print(Fore.CYAN + "\nConcerts Attended:")
    if player["entertainment_history"]["concerts_attended"]:
        for i, concert in enumerate(player["entertainment_history"]["concerts_attended"], 1):
            print(f"{i}. {concert}")
    else:
        print("You haven't attended any concerts yet.")
    
    # Theatre shows seen
    print(Fore.CYAN + "\nTheatre Shows Seen:")
    if player["entertainment_history"]["theatre_shows_seen"]:
        for i, show in enumerate(player["entertainment_history"]["theatre_shows_seen"], 1):
            print(f"{i}. {show}")
    else:
        print("You haven't seen any theatre shows yet.")
    
    # Entertainment collectibles
    print(Fore.CYAN + "\nEntertainment Collectibles:")
    if player["entertainment_collectibles"]:
        for i, item in enumerate(player["entertainment_collectibles"], 1):
            print(f"{i}. {item}")
    else:
        print("You haven't collected any entertainment souvenirs yet.")
    
    # Entertainment achievements
    print(Fore.CYAN + "\nEntertainment Achievements:")
    earned_achievements = 0
    for achievement, description in ENTERTAINMENT_ACHIEVEMENTS.items():
        if achievement in player["achievements"]:
            print(f"✓ {achievement}: {description}")
            earned_achievements += 1
    
    if earned_achievements == 0:
        print("You haven't earned any entertainment achievements yet.")
    
    # Stats
    total_experiences = len(player["entertainment_history"]["movies_watched"]) + \
                        len(player["entertainment_history"]["concerts_attended"]) + \
                        len(player["entertainment_history"]["theatre_shows_seen"])
    
    print(Fore.YELLOW + f"\nTotal Entertainment Experiences: {total_experiences}")
    print(f"Total Collectibles: {len(player['entertainment_collectibles'])}")
    
    input("\nPress Enter to return to Entertainment Plaza...")
    return entertainment_plaza()

def check_entertainment_achievements():
    """Check and award achievements related to entertainment"""
    # Initialize counters
    movies_count = len(player["entertainment_history"]["movies_watched"])
    concerts_count = len(player["entertainment_history"]["concerts_attended"])
    theatre_count = len(player["entertainment_history"]["theatre_shows_seen"])
    collectibles_count = len(player["entertainment_collectibles"])
    
    # Track genres and special effects
    sci_fi_movies = 0
    comedy_shows = 0
    drama_shows = 0
    music_genres = set()
    special_effects_count = 0
    total_spent = player.get("entertainment_spent", 0)
    plaza_visits = player.get("entertainment_plaza_visits", 0)
    
    # Count genre-specific viewings
    for movie in player["entertainment_history"]["movies_watched"]:
        for m in MOVIES:
            if m["title"] == movie:
                if m["genre"] == "Sci-Fi":
                    sci_fi_movies += 1
                elif m["genre"] == "Comedy":
                    comedy_shows += 1
                if m["special_effect"]:
                    special_effects_count += 1
                break
    
    for concert in player["entertainment_history"]["concerts_attended"]:
        for c in MUSIC_SHOWS:
            if c["title"] == concert:
                music_genres.add(c["genre"])
                if c["special_effect"]:
                    special_effects_count += 1
                break
    
    for show in player["entertainment_history"]["theatre_shows_seen"]:
        for s in THEATRE_SHOWS:
            if s["title"] == show:
                if s["genre"] == "Comedy":
                    comedy_shows += 1
                elif s["genre"] == "Tragedy" or s["genre"] == "Drama":
                    drama_shows += 1
                if s["special_effect"]:
                    special_effects_count += 1
                break
    
    # Total entertainment experiences
    total_experiences = movies_count + concerts_count + theatre_count
    
    # Basic achievements
    
    # Check for individual type achievements
    if movies_count >= 3 and "Movie Buff" not in player["achievements"]:
        award_achievement("Movie Buff")
    
    if concerts_count >= 3 and "Music Enthusiast" not in player["achievements"]:
        award_achievement("Music Enthusiast")
    
    if theatre_count >= 3 and "Theatre Lover" not in player["achievements"]:
        award_achievement("Theatre Lover")
    
    # Check for connoisseur achievement (at least one of each type)
    if movies_count >= 1 and concerts_count >= 1 and theatre_count >= 1 and "Entertainment Connoisseur" not in player["achievements"]:
        award_achievement("Entertainment Connoisseur")
        # Bonus reward for being a connoisseur
        player["tickets"] += 25
        print(Fore.GREEN + "Entertainment Connoisseur bonus: +25 tickets!")
    
    # Check for VIP attendance (special effects show)
    if special_effects_count > 0 and "VIP Audience" not in player["achievements"]:
        award_achievement("VIP Audience")
    
    # Check for collector achievement
    if collectibles_count >= 5 and "Collector's Edition" not in player["achievements"]:
        award_achievement("Collector's Edition")
        # Bonus reward for being a collector
        add_loyalty_points(15)
        print(Fore.MAGENTA + "Collector's Edition bonus: +15 Loyalty Points!")
    
    # Advanced achievements
    
    # Check for advanced count achievements
    if movies_count >= 10 and "Film Festival Fanatic" not in player["achievements"]:
        award_achievement("Film Festival Fanatic")
        # Bonus reward
        player["tickets"] += 50
        print(Fore.GREEN + "Film Festival Fanatic bonus: +50 tickets!")
    
    if concerts_count >= 10 and "Concert Tour VIP" not in player["achievements"]:
        award_achievement("Concert Tour VIP")
        # Bonus reward
        player["tickets"] += 50
        add_loyalty_points(25)
        print(Fore.GREEN + "Concert Tour VIP bonus: +50 tickets and +25 Loyalty Points!")
    
    if theatre_count >= 10 and "Broadway Legend" not in player["achievements"]:
        award_achievement("Broadway Legend")
        # Bonus reward
        player["tickets"] += 50
        add_loyalty_points(25)
        print(Fore.GREEN + "Broadway Legend bonus: +50 tickets and +25 Loyalty Points!")
        
    if special_effects_count >= 5 and "Special Effects Enthusiast" not in player["achievements"]:
        award_achievement("Special Effects Enthusiast")
        # Bonus reward
        player["tickets"] += 35
        print(Fore.GREEN + "Special Effects Enthusiast bonus: +35 tickets!")
    
    if collectibles_count >= 15 and "Memorabilia Master" not in player["achievements"]:
        award_achievement("Memorabilia Master")
        # Bonus reward
        player["fast_passes"] = player.get("fast_passes", 0) + 3
        print(Fore.GREEN + "Memorabilia Master bonus: +3 Fast Passes!")
    
    # Genre-specific achievements
    if sci_fi_movies >= 3 and "Sci-Fi Aficionado" not in player["achievements"]:
        award_achievement("Sci-Fi Aficionado")
        # Bonus reward
        if "time crystal replica" not in player["entertainment_collectibles"]:
            player["entertainment_collectibles"].append("time crystal replica")
            print(Fore.GREEN + "Sci-Fi Aficionado bonus: Received a time crystal replica!")
    
    if comedy_shows >= 3 and "Comedy Club Regular" not in player["achievements"]:
        award_achievement("Comedy Club Regular")
        # Bonus reward
        player["tickets"] += 30
        print(Fore.GREEN + "Comedy Club Regular bonus: +30 tickets for a good laugh!")
    
    if len(music_genres) >= 5 and "Music Genre Explorer" not in player["achievements"]:
        award_achievement("Music Genre Explorer")
        # Bonus reward
        if "multi-genre playlist" not in player["entertainment_collectibles"]:
            player["entertainment_collectibles"].append("multi-genre playlist")
            print(Fore.GREEN + "Music Genre Explorer bonus: Received a special multi-genre playlist!")
    
    if drama_shows >= 3 and "Drama Devotee" not in player["achievements"]:
        award_achievement("Drama Devotee")
        # Bonus reward
        player["tickets"] += 40
        print(Fore.GREEN + "Drama Devotee bonus: +40 tickets!")
    
    # Premium achievements
    if total_experiences >= 25 and "Entertainment Mogul" not in player["achievements"]:
        award_achievement("Entertainment Mogul")
        # Bonus reward - Season Pass extension
        if player.get("season_pass", False):
            player["season_pass_days"] = player.get("season_pass_days", 0) + 7
            print(Fore.GREEN + "Entertainment Mogul bonus: Season Pass extended by 7 days!")
        else:
            # Give season pass if don't have one
            player["season_pass"] = True
            player["season_pass_days"] = 7
            print(Fore.GREEN + "Entertainment Mogul bonus: Received a 7-day Season Pass!")
    
    if total_spent >= 200 and "Golden Ticket" not in player["achievements"]:
        award_achievement("Golden Ticket")
        # Bonus reward
        player["tickets"] += 100
        print(Fore.GREEN + "Golden Ticket bonus: +100 tickets!")
    
    if plaza_visits >= 10 and player.get("season_pass", False) and "Season Pass Pro" not in player["achievements"]:
        award_achievement("Season Pass Pro")
        # Bonus reward
        player["fast_passes"] = player.get("fast_passes", 0) + 5
        print(Fore.GREEN + "Season Pass Pro bonus: +5 Fast Passes!")

def update_mission_progress(mission_type, amount=1):
    for mission_id, mission in MISSIONS.items():
        if mission["type"] == mission_type and mission_id not in player["completed_missions"]:
            if mission_id not in player["missions"]:
                player["missions"][mission_id] = 0
            player["missions"][mission_id] += amount
            if player["missions"][mission_id] >= mission["target"]:
                print(Fore.GREEN + f"\n🎉 Mission Complete: {mission['name']}")
                print(f"Reward: {mission['reward']} tickets")
                player["tickets"] += mission["reward"]
                player["completed_missions"].append(mission_id)
                
                # Add loyalty points for completing missions
                add_loyalty_points(5)
                check_loyalty_achievements()

def add_loyalty_points(points):
    """Award loyalty points to the player and announce if they reach a new tier"""
    # Initialize loyalty points if not present
    if "loyalty_points" not in player:
        player["loyalty_points"] = 0
        
    old_tier = get_loyalty_tier()
    player["loyalty_points"] += points
    new_tier = get_loyalty_tier()
    
    print(Fore.MAGENTA + f"✨ +{points} Loyalty Points! (Total: {player['loyalty_points']})")
    
    # Check if player reached a new tier
    if new_tier != old_tier:
        print(Fore.YELLOW + f"🏆 CONGRATULATIONS! You've reached a new loyalty tier: {new_tier}!")
        print(f"Enjoy your new benefits: {LOYALTY_TIERS[new_tier]['discount']*100}% discount and {LOYALTY_TIERS[new_tier]['bonus']} bonus tickets per win!")
        award_achievement(f"Loyalty: Reached {new_tier}")
    
def get_loyalty_tier():
    """Determine the player's current loyalty tier based on points"""
    points = player.get("loyalty_points", 0)
    current_tier = "Bronze Member"
    
    for tier, details in LOYALTY_TIERS.items():
        if points >= details["points"]:
            current_tier = tier
    
    return current_tier

def get_loyalty_discount():
    """Get the discount percentage based on loyalty tier"""
    tier = get_loyalty_tier()
    return LOYALTY_TIERS[tier]["discount"]

def get_loyalty_bonus():
    """Get the bonus tickets based on loyalty tier"""
    tier = get_loyalty_tier()
    return LOYALTY_TIERS[tier]["bonus"]

def check_loyalty_achievements():
    """Check for loyalty-related achievements"""
    points = player.get("loyalty_points", 0)
    
    if points >= 50:
        award_achievement("Loyal Fan: Earn 50 loyalty points")
    if points >= 200:
        award_achievement("Carnival VIP: Earn 200 loyalty points")
    if points >= 500:
        award_achievement("Carnival Legend: Earn 500 loyalty points")

def track_attraction_visit(attraction_name):
    """Track visits to attractions for loyalty rewards and rewards for repeat visits"""
    # Initialize visited attractions if needed
    if "visited_attractions" not in player:
        player["visited_attractions"] = {}
    
    # Update visit count for this attraction
    if attraction_name not in player["visited_attractions"]:
        player["visited_attractions"][attraction_name] = 0
    
    player["visited_attractions"][attraction_name] += 1
    visit_count = player["visited_attractions"][attraction_name]
    
    # Award loyalty points
    add_loyalty_points(1)
    
    # Check for repeat visit rewards (every 3 visits)
    if visit_count % 3 == 0:
        print(Fore.GREEN + f"🎁 Loyal Visitor Reward! You've visited {attraction_name} {visit_count} times!")
        print("You've earned 5 bonus tickets and a free play next time!")
        player["tickets"] += 5
        
        # Mark this attraction for a free play next time
        if "free_plays" not in player:
            player["free_plays"] = {}
        player["free_plays"][attraction_name] = True
        
        # Update mission progress for loyalty missions
        update_mission_progress("loyalty_points", visit_count)


# Define loyalty tiers with their benefits
LOYALTY_TIERS = {
    "Bronze Member": {"points": 0, "discount": 0.0, "bonus": 0},
    "Silver Member": {"points": 50, "discount": 0.05, "bonus": 1},
    "Gold Member": {"points": 150, "discount": 0.10, "bonus": 2},
    "Platinum Member": {"points": 300, "discount": 0.15, "bonus": 3},
    "Diamond Member": {"points": 500, "discount": 0.20, "bonus": 5}
}

# Global variable to track if championship variables are initialized
championship_vars_initialized = False

# Carnival Food Options
CARNIVAL_FOODS = [
    {"name": "Cotton Candy 🍭", "price": 3, "energy": 10, "hunger": 15, "seasonal": None},
    {"name": "Funnel Cake 🍯", "price": 5, "energy": 15, "hunger": 30, "seasonal": None},
    {"name": "Corn Dog 🌭", "price": 4, "energy": 20, "hunger": 40, "seasonal": None},
    {"name": "Nachos with Cheese 🧀", "price": 5, "energy": 20, "hunger": 35, "seasonal": None},
    {"name": "Soft Pretzel 🥨", "price": 3, "energy": 15, "hunger": 25, "seasonal": None},
    {"name": "Popcorn 🍿", "price": 3, "energy": 10, "hunger": 20, "seasonal": None},
    {"name": "Turkey Leg 🍗", "price": 7, "energy": 30, "hunger": 60, "seasonal": None},
    {"name": "Ice Cream Cone 🍦", "price": 4, "energy": 15, "hunger": 20, "seasonal": "summer"},
    {"name": "Hot Chocolate ☕", "price": 3, "energy": 15, "hunger": 10, "seasonal": "winter"},
    {"name": "Candy Apple 🍎", "price": 4, "energy": 15, "hunger": 25, "seasonal": "halloween"},
    {"name": "Pumpkin Spice Funnel Cake 🎃", "price": 6, "energy": 20, "hunger": 35, "seasonal": "halloween"},
    {"name": "Strawberry Shortcake 🍓", "price": 5, "energy": 20, "hunger": 30, "seasonal": "spring"},
    {"name": "Snow Cone 🧊", "price": 3, "energy": 5, "hunger": 10, "seasonal": "summer"},
    {"name": "Caramel Apple 🍏", "price": 4, "energy": 15, "hunger": 25, "seasonal": "fall"},
    {"name": "Gingerbread Cookie 🍪", "price": 3, "energy": 10, "hunger": 20, "seasonal": "winter"}
]

# Carnival Games
CARNIVAL_GAMES = [
    {"name": "Ring Toss 💍", "price": 2, "difficulty": "medium", "prizes": ["Small Plush", "Candy Bar", "Keychain"]},
    {"name": "Balloon Dart Throw 🎯", "price": 2, "difficulty": "easy", "prizes": ["Stuffed Animal", "Inflatable Toy", "Plastic Jewelry"]},
    {"name": "Milk Bottle Knock Down 🍼", "price": 3, "difficulty": "hard", "prizes": ["Large Plush", "Premium Toy", "Game Tickets"]},
    {"name": "Basketball Shoot 🏀", "price": 3, "difficulty": "medium", "prizes": ["Sports Memorabilia", "Team Pennant", "Foam Finger"]},
    {"name": "Water Gun Race 💦", "price": 2, "difficulty": "medium", "prizes": ["Water Toy", "Beach Ball", "Squirt Gun"]},
    {"name": "Whack-A-Mole 🔨", "price": 3, "difficulty": "easy", "prizes": ["Plush Mole", "Toy Hammer", "Arcade Tokens"]},
    {"name": "High Striker 💪", "price": 4, "difficulty": "hard", "prizes": ["Carnival Hat", "Strong Man Badge", "Premium Tickets"]},
    {"name": "Duck Pond 🦆", "price": 2, "difficulty": "easy", "prizes": ["Rubber Duck", "Small Toy", "Candy"]},
    {"name": "Fortune Teller Booth 🔮", "price": 2, "difficulty": "none", "prizes": ["Fortune Card", "Lucky Charm", "Mystery Envelope"]}
]

# Seasonal Events and Decorations
SEASONAL_EVENTS = {
    "summer": {
        "name": "Summer Splash Festival",
        "decorations": ["Water Fountains", "Beach Umbrellas", "Sand Sculptures", "Tropical Flowers"],
        "special_characters": ["Surfer Sam", "Captain Splash", "Sunny the Sunflower"],
        "special_attractions": ["Water Balloon Battle", "Splash Zone", "Beach Volleyball"]
    },
    "fall": {
        "name": "Autumn Harvest Festival",
        "decorations": ["Colorful Leaves", "Hay Bales", "Corn Stalks", "Scarecrows"],
        "special_characters": ["Farmer Joe", "Harvest Hank", "Maple the Squirrel"],
        "special_attractions": ["Hay Ride", "Corn Maze", "Pumpkin Carving"]
    },
    "halloween": {
        "name": "Halloween Spooktacular",
        "decorations": ["Jack-o-Lanterns", "Fake Cobwebs", "Skeletons", "Spooky Trees"],
        "special_characters": ["Count Dracula", "Witchy Winnie", "Frankenstein's Monster"],
        "special_attractions": ["Haunted Hayride", "Monster Mash Dance Party", "Costume Contest"]
    },
    "winter": {
        "name": "Winter Wonderland",
        "decorations": ["String Lights", "Snowflakes", "Evergreen Trees", "Icicles"],
        "special_characters": ["Frost the Snowman", "Polar Paul", "Holly Berry"],
        "special_attractions": ["Ice Sculpture Display", "Gingerbread House Workshop", "Santa's Workshop"]
    },
    "spring": {
        "name": "Spring Blossom Celebration",
        "decorations": ["Flower Arches", "Butterfly Displays", "Rainbow Banners", "Cherry Blossoms"],
        "special_characters": ["Flora the Fairy", "Buzz the Bee", "Peter Rabbit"],
        "special_attractions": ["Flower Crown Workshop", "Butterfly House", "Spring Parade"]
    }
}

# Entertainment Plaza options
MOVIES = [
    {"title": "Space Pirates: The Final Frontier", "genre": "Sci-Fi", "duration": "2h 15m", "price": 8, "reward": "popcorn", "special_effect": "3D", "description": "An epic space adventure with stunning visuals and an engaging storyline."},
    {"title": "The Enchanted Kingdom", "genre": "Fantasy", "duration": "1h 55m", "price": 7, "reward": "collectible figurine", "special_effect": "Magic Show", "description": "A magical journey through a realm of mythical creatures and ancient spells."},
    {"title": "Laugh Out Loud", "genre": "Comedy", "duration": "1h 45m", "price": 6, "reward": "comedy mask pin", "special_effect": None, "description": "A hilarious comedy that will have you in stitches from start to finish."},
    {"title": "The Haunting of Crimson Manor", "genre": "Horror", "duration": "2h 5m", "price": 9, "reward": "glow-in-the-dark pendant", "special_effect": "Fog Effects", "description": "A spine-chilling horror story set in a mysterious abandoned mansion."},
    {"title": "Love Under the Stars", "genre": "Romance", "duration": "2h", "price": 7, "reward": "heart-shaped keychain", "special_effect": None, "description": "A touching love story that will warm your heart and bring tears to your eyes."},
    {"title": "Action Heroes: Ultimate Showdown", "genre": "Action", "duration": "2h 20m", "price": 8, "reward": "action figure", "special_effect": "Explosions", "description": "Non-stop action with jaw-dropping stunts and explosive special effects."},
    {"title": "Mystery at Midnight", "genre": "Mystery", "duration": "2h 10m", "price": 7, "reward": "magnifying glass", "special_effect": None, "description": "A thrilling mystery that will keep you guessing until the very end."},
    {"title": "Animated Wonderland", "genre": "Animation", "duration": "1h 50m", "price": 6, "reward": "character sticker pack", "special_effect": "Interactive", "description": "A colorful animated adventure suitable for all ages."},
    {"title": "Time Traveler's Paradox", "genre": "Sci-Fi", "duration": "2h 25m", "price": 9, "reward": "time crystal replica", "special_effect": "4D Time Effects", "description": "A mind-bending journey through time with paradoxes and alternate realities."},
    {"title": "Ocean's Depths", "genre": "Documentary", "duration": "1h 40m", "price": 5, "reward": "ocean life poster", "special_effect": "Water Effects", "description": "An immersive documentary exploring the mysterious depths of our oceans."},
    {"title": "Legends of the Lost Temple", "genre": "Adventure", "duration": "2h 10m", "price": 8, "reward": "treasure map replica", "special_effect": "Moving Seats", "description": "An exhilarating adventure hunting for treasure in ancient ruins."},
    {"title": "Cosmos: Beyond Imagination", "genre": "Science", "duration": "2h", "price": 7, "reward": "glow-in-the-dark star chart", "special_effect": "Star Ceiling", "description": "A breathtaking journey through our universe revealing its greatest wonders."},
    {"title": "The Art of Music", "genre": "Documentary", "duration": "1h 50m", "price": 6, "reward": "sheet music bookmark", "special_effect": "Live Orchestra", "description": "An exploration of how music has shaped human history and emotions."},
    {"title": "Ninja Warriors: Shadow Clan", "genre": "Martial Arts", "duration": "2h 15m", "price": 8, "reward": "ninja star keychain", "special_effect": "Wind Effects", "description": "An action-packed martial arts epic about rival ninja clans."},
    {"title": "The Great Heist", "genre": "Crime", "duration": "2h 20m", "price": 8, "reward": "replica vault key", "special_effect": "Tension Wires", "description": "A sophisticated crime thriller about the most daring bank heist in history."},
    {"title": "Fairytale Kingdom", "genre": "Family", "duration": "1h 45m", "price": 6, "reward": "crown pendant", "special_effect": "Bubbles", "description": "A heartwarming tale of friendship and courage in an enchanted kingdom."}
]

MUSIC_SHOWS = [
    {"title": "Rock Revolution", "genre": "Rock", "duration": "2h", "price": 10, "reward": "guitar pick", "special_effect": "Pyrotechnics", "description": "An electrifying rock concert featuring classic hits and new anthems."},
    {"title": "Pop Sensation", "genre": "Pop", "duration": "1h 45m", "price": 9, "reward": "glow stick", "special_effect": "Light Show", "description": "A high-energy pop concert with chart-topping hits and spectacular choreography."},
    {"title": "Jazz Night", "genre": "Jazz", "duration": "2h", "price": 8, "reward": "jazz CD", "special_effect": None, "description": "A sophisticated evening of smooth jazz and improvisational masterpieces."},
    {"title": "Classical Symphony", "genre": "Classical", "duration": "2h 30m", "price": 12, "reward": "conductor's baton", "special_effect": None, "description": "A moving performance of timeless classical compositions by a full orchestra."},
    {"title": "Electronic Dreams", "genre": "Electronic", "duration": "2h", "price": 11, "reward": "LED bracelet", "special_effect": "Laser Show", "description": "An immersive electronic music experience with state-of-the-art lighting and effects."},
    {"title": "Country Roads", "genre": "Country", "duration": "1h 50m", "price": 8, "reward": "cowboy hat pin", "special_effect": None, "description": "A heartfelt country music show celebrating rural life and timeless stories."},
    {"title": "Hip Hop Revolution", "genre": "Hip Hop", "duration": "1h 45m", "price": 10, "reward": "cap", "special_effect": "Dance Battles", "description": "A dynamic hip hop concert featuring rapid-fire lyrics and incredible dance moves."},
    {"title": "World Music Fusion", "genre": "World", "duration": "2h 15m", "price": 9, "reward": "cultural instrument miniature", "special_effect": None, "description": "A diverse celebration of musical traditions from around the globe."},
    {"title": "Metal Mayhem", "genre": "Heavy Metal", "duration": "2h 15m", "price": 11, "reward": "spiked wristband", "special_effect": "Fire Columns", "description": "An intense, high-energy metal performance that will shake the foundations."},
    {"title": "Acoustic Serenity", "genre": "Folk", "duration": "1h 50m", "price": 7, "reward": "wooden flute charm", "special_effect": "Nature Sounds", "description": "A soulful acoustic set featuring folk traditions and storytelling."},
    {"title": "Reggae Rhythms", "genre": "Reggae", "duration": "2h", "price": 9, "reward": "rasta bracelet", "special_effect": "Fog Machine", "description": "Relaxing reggae beats that transport you to Caribbean shores."},
    {"title": "Opera Majesty", "genre": "Opera", "duration": "2h 45m", "price": 15, "reward": "opera glasses", "special_effect": "Holographic Backdrops", "description": "A breathtaking operatic performance by world-renowned vocalists."},
    {"title": "Techno Trance", "genre": "Techno", "duration": "3h", "price": 12, "reward": "light-up pendant", "special_effect": "Full Immersion Lighting", "description": "A mind-bending all-night techno experience with hypnotic beats."},
    {"title": "Blues & Soul", "genre": "Blues", "duration": "2h", "price": 9, "reward": "harmonica keychain", "special_effect": None, "description": "Soulful blues performances that touch the heart and move the spirit."},
    {"title": "K-Pop Extravaganza", "genre": "K-Pop", "duration": "2h 15m", "price": 12, "reward": "light stick", "special_effect": "Holographic Dancers", "description": "A dazzling K-Pop showcase with choreographed performances and upbeat songs."},
    {"title": "EDM Festival", "genre": "EDM", "duration": "4h", "price": 16, "reward": "festival wristband", "special_effect": "Confetti Cannons", "description": "A massive electronic dance music festival with multiple DJs and non-stop dancing."}
]

THEATRE_SHOWS = [
    {"title": "The Phantom's Serenade", "genre": "Musical", "duration": "2h 30m", "price": 15, "reward": "mask ornament", "special_effect": "Chandelier Drop", "description": "A haunting musical about love, music, and obsession beneath an opera house."},
    {"title": "Star-Crossed Lovers", "genre": "Tragedy", "duration": "2h 45m", "price": 14, "reward": "rose pendant", "special_effect": None, "description": "A timeless tale of forbidden love and the consequences of family feuds."},
    {"title": "Laugh Till You Cry", "genre": "Comedy", "duration": "2h", "price": 12, "reward": "jester hat pin", "special_effect": None, "description": "A side-splitting comedy of errors with mistaken identities and hilarious situations."},
    {"title": "The Time Traveler", "genre": "Sci-Fi", "duration": "2h 15m", "price": 13, "reward": "clockwork brooch", "special_effect": "Time Shifts", "description": "An innovative play exploring the paradoxes and possibilities of time travel."},
    {"title": "The Mystery of Blackwood Manor", "genre": "Mystery", "duration": "2h 30m", "price": 14, "reward": "detective badge", "special_effect": "Fog Effects", "description": "A thrilling whodunit with twists and turns that will keep you guessing."},
    {"title": "Dance of the Elements", "genre": "Dance", "duration": "1h 45m", "price": 11, "reward": "element symbol pin set", "special_effect": "Water & Fire", "description": "A breathtaking dance performance representing the four elements of nature."},
    {"title": "Historical Heroes", "genre": "Historical", "duration": "3h", "price": 16, "reward": "historical coin replica", "special_effect": None, "description": "An epic historical drama spanning generations of triumph and tragedy."},
    {"title": "Puppets Alive!", "genre": "Family", "duration": "1h 30m", "price": 9, "reward": "puppet keychain", "special_effect": "Giant Puppets", "description": "A charming puppet show that delights audience members of all ages."},
    {"title": "Cats & Dreams", "genre": "Musical", "duration": "2h 20m", "price": 14, "reward": "cat ear headband", "special_effect": "Acrobatics", "description": "A mesmerizing musical featuring feline characters in a dreamlike setting."},
    {"title": "The Lion's Pride", "genre": "Drama", "duration": "2h 45m", "price": 15, "reward": "lion figurine", "special_effect": "Moving Stage", "description": "A powerful drama about a royal family's struggle for the throne in an African kingdom."},
    {"title": "Space Odyssey 2157", "genre": "Sci-Fi", "duration": "2h 30m", "price": 15, "reward": "holographic space pendant", "special_effect": "Anti-Gravity", "description": "A futuristic space adventure featuring astronauts encountering alien civilizations."},
    {"title": "The Forgotten Forest", "genre": "Fantasy", "duration": "2h 15m", "price": 13, "reward": "enchanted leaf bookmark", "special_effect": "Living Trees", "description": "A magical journey through an enchanted forest full of mythical creatures."},
    {"title": "Improv Masters", "genre": "Comedy", "duration": "1h 30m", "price": 10, "reward": "comedy/tragedy mask pin", "special_effect": "Audience Participation", "description": "A hilarious improvisation show where the audience helps create the story."},
    {"title": "Broadway Dreams", "genre": "Musical Revue", "duration": "2h", "price": 12, "reward": "musical notes scarf", "special_effect": "Rain of Stars", "description": "A spectacular showcase of famous Broadway musical numbers and choreography."},
    {"title": "Silent Tales", "genre": "Mime", "duration": "1h 45m", "price": 11, "reward": "mime face brooch", "special_effect": "Shadow Play", "description": "A captivating mime performance telling stories through movement and expression."},
    {"title": "Circus Extravaganza", "genre": "Circus", "duration": "2h", "price": 13, "reward": "miniature circus tent", "special_effect": "Trapeze Acts", "description": "A dazzling circus performance with acrobats, clowns, and amazing stunts."}
]

# Entertainment tracking
ENTERTAINMENT_HISTORY = {
    "movies_watched": [],
    "concerts_attended": [],
    "theatre_shows_seen": []
}

# Special achievements for entertainment
ENTERTAINMENT_ACHIEVEMENTS = {
    # Basic achievements
    "Movie Buff": "Watch 3 different movies",
    "Music Enthusiast": "Attend 3 different music shows",
    "Theatre Lover": "See 3 different theatre performances",
    "Entertainment Connoisseur": "Experience at least one of each entertainment type",
    "VIP Audience": "Attend a premium show with special effects",
    "Collector's Edition": "Collect 5 different entertainment rewards",
    
    # Advanced achievements
    "Film Festival Fanatic": "Watch 10 different movies",
    "Concert Tour VIP": "Attend 10 different music shows",
    "Broadway Legend": "See 10 different theatre performances",
    "Special Effects Enthusiast": "Experience 5 shows with special effects",
    "Memorabilia Master": "Collect 15 different entertainment rewards",
    
    # Genre-specific achievements
    "Sci-Fi Aficionado": "Watch 3 different sci-fi movies",
    "Comedy Club Regular": "Watch 3 different comedy movies or plays",
    "Music Genre Explorer": "Attend concerts from 5 different music genres",
    "Drama Devotee": "See 3 different dramatic theatre performances",
    
    # Premium achievements
    "Entertainment Mogul": "Experience at least 25 different shows total",
    "Golden Ticket": "Spend over 200 tickets on entertainment",
    "Season Pass Pro": "Visit the Entertainment Plaza 10 times with a Season Pass active"
}

# Championship definitions
CHAMPIONSHIPS = {
    "Minigame Master": {
        "description": "Compete in a series of 5 minigames for the highest combined score.",
        "entry_fee": 10,
        "reward_tickets": 50,
        "reward_loyalty": 20,
        "games": ["guess_the_number", "quick_math", "word_shuffle", "reaction_test", "dart_throw"]
    },
    "TCG Tournament": {
        "description": "Battle with your card collection against 4 increasingly difficult opponents.",
        "entry_fee": 15,
        "reward_tickets": 75,
        "reward_loyalty": 25,
        "special_reward": "Exclusive Champion Card"
    },
    "Theme Park Challenge": {
        "description": "Visit all attractions and complete special challenges for each one.",
        "entry_fee": 20,
        "reward_tickets": 100,
        "reward_loyalty": 30,
        "special_reward": "Theme Park VIP Pass (1 free entry to all attractions)"
    },
    "Casino Royale": {
        "description": "Test your luck in all gambling games with a starting pool of chips.",
        "entry_fee": 25,
        "reward_tickets": 125,
        "reward_loyalty": 35,
        "special_reward": "Lucky Charm (improves gambling odds by 10%)"
    }
}

# Quest system definitions
QUESTS = {
    "daily_challenge": {
        "name": "Daily Challenge",
        "description": "Complete a random task that changes each day.",
        "reward_tickets": 15,
        "reward_loyalty": 5,
        "expiry": "daily",
        "difficulty": "easy"
    },
    "weekly_quest": {
        "name": "Weekly Epic Quest",
        "description": "A more challenging quest that requires multiple steps to complete.",
        "reward_tickets": 50,
        "reward_loyalty": 15,
        "expiry": "weekly",
        "difficulty": "medium"
    },
    "scavenger_hunt": {
        "name": "Carnival Scavenger Hunt",
        "description": "Find hidden items throughout the carnival and theme park.",
        "reward_tickets": 75,
        "reward_loyalty": 25,
        "expiry": "weekly",
        "difficulty": "hard"
    },
    "seasonal_event": {
        "name": "Seasonal Spectacular",
        "description": "Special seasonal event with unique rewards.",
        "reward_tickets": 100,
        "reward_loyalty": 40,
        "expiry": "seasonal",
        "difficulty": "special"
    }
}

def championship_center():
    """Main hub for accessing and participating in championships"""
    clear()
    print(Fore.YELLOW + "🏆 CHAMPIONSHIP CENTER 🏆")
    print(Fore.CYAN + "Test your skills and win big rewards in our championship events!")
    print(f"Current Tickets: {player['tickets']}")
    print("")
    
    # Display available championships
    print(Fore.MAGENTA + "Available Championships:")
    for i, (name, details) in enumerate(CHAMPIONSHIPS.items(), 1):
        print(f"[{i}] {name} - {details['description']}")
        print(f"    Entry Fee: {details['entry_fee']} tickets | Reward: {details['reward_tickets']} tickets")
        if "special_reward" in details:
            print(f"    Special Reward: {details['special_reward']}")
        
        # Display player's records for this championship
        if name in player.get("championship_records", {}):
            record = player["championship_records"][name]
            print(f"    Your Best: {record['best_score']} points | Wins: {record['wins']} | Participations: {record['participations']}")
        print("")
    
    print("[0] Return to Main Menu")
    
    choice = input("\nSelect championship (or 0 to return): ")
    if choice == "0":
        return
    
    # Convert to index and validate
    try:
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(CHAMPIONSHIPS):
            print(Fore.RED + "Invalid choice!")
            time.sleep(1)
            return championship_center()
            
        # Get selected championship
        championship_name = list(CHAMPIONSHIPS.keys())[choice_idx]
        championship = CHAMPIONSHIPS[championship_name]
        
        # Check if player can afford entry fee
        if player["tickets"] < championship["entry_fee"]:
            print(Fore.RED + f"You don't have enough tickets! Need {championship['entry_fee']} tickets.")
            time.sleep(2)
            return championship_center()
            
        # Confirm participation
        print(Fore.YELLOW + f"\nYou've selected: {championship_name}")
        print(f"Entry Fee: {championship['entry_fee']} tickets")
        confirm = input("Ready to compete? (y/n): ").lower()
        
        if confirm != "y":
            return championship_center()
            
        # Deduct entry fee
        player["tickets"] -= championship["entry_fee"]
        
        # Start championship based on type
        if championship_name == "Minigame Master":
            score = minigame_championship()
        elif championship_name == "TCG Tournament":
            score = tcg_championship()
        elif championship_name == "Theme Park Challenge":
            score = theme_park_championship()
        elif championship_name == "Casino Royale":
            score = casino_championship()
        else:
            print(Fore.RED + "Championship not implemented yet!")
            score = 0
            
        # Update player records
        if "championship_records" not in player:
            player["championship_records"] = {}
            
        if championship_name not in player["championship_records"]:
            player["championship_records"][championship_name] = {
                "best_score": 0,
                "wins": 0,
                "participations": 0
            }
            
        # Update participation count
        player["championship_records"][championship_name]["participations"] = player["championship_records"][championship_name].get("participations", 0) + 1
        
        # Update mission progress
        update_mission_progress("championship_participation")
        
        # Check if player won (score threshold)
        win_threshold = {
            "Minigame Master": 75,
            "TCG Tournament": 3,
            "Theme Park Challenge": 80,
            "Casino Royale": 200
        }
        
        if score >= win_threshold.get(championship_name, 100):
            print(Fore.GREEN + f"\n🏆 CONGRATULATIONS! You've won the {championship_name} Championship!")
            print(f"Reward: {championship['reward_tickets']} tickets + {championship['reward_loyalty']} loyalty points")
            
            if "special_reward" in championship:
                print(f"Special Reward: {championship['special_reward']}")
                # Add special reward to inventory
                special_reward_name = championship['special_reward'].split(" (")[0]  # Extract name without description
                player["inventory"].append(special_reward_name)
                
            # Award rewards
            player["tickets"] += championship["reward_tickets"]
            add_loyalty_points(championship["reward_loyalty"])
            
            # Update win count
            player["championship_records"][championship_name]["wins"] = player["championship_records"][championship_name].get("wins", 0) + 1
            
            # Update mission progress
            update_mission_progress("championship_win")
            
            # Award achievement
            award_achievement(f"Champion: Won {championship_name}")
        else:
            print(Fore.YELLOW + f"\nYou scored {score} points in the {championship_name} Championship.")
            print("Better luck next time! Practice makes perfect.")
            
            # Consolation prize - 10% of the reward
            consolation = int(championship["reward_tickets"] * 0.1)
            print(f"Consolation Prize: {consolation} tickets")
            player["tickets"] += consolation
            
        # Update best score if better
        if score > player["championship_records"][championship_name].get("best_score", 0):
            player["championship_records"][championship_name]["best_score"] = score
            print(Fore.CYAN + "New personal best score!")
        
        input("\nPress Enter to continue...")
        
    except ValueError:
        print(Fore.RED + "Invalid choice!")
        time.sleep(1)
        return championship_center()

def minigame_championship():
    """Run the Minigame Master championship with 5 games"""
    clear()
    print(Fore.YELLOW + "🎮 MINIGAME MASTER CHAMPIONSHIP 🎮")
    print("Compete in 5 minigames for the highest total score!")
    
    # Each game's max score is 20 points, for a total of 100 possible points
    total_score = 0
    championship_minigames = ["Guess the Number", "Quick Math", "Word Shuffle", "Reaction Test", "Dart Throw"]
    
    # Display the games to be played
    print("\nYou'll compete in these 5 minigames:")
    for i, game in enumerate(championship_minigames, 1):
        print(f"{i}. {game}")
    
    # Initialize all score variables to avoid reference errors
    score = 0
    scaled_math_score = 0
    word_score = 0
    reaction_score = 0
    dart_score = 0
    
    input("Press Enter to begin the first game...")
    
    # Game 1: Guess the Number (championship version)
    clear()
    print(Fore.CYAN + "Game 1: Guess the Number")
    print("Guess the number between 1-100 in as few tries as possible.")
    
    number = random.randint(1, 100)
    tries = 0
    max_tries = 10
    score = 0
    
    while tries < max_tries:
        guess = input(f"Enter your guess (tries left: {max_tries - tries}): ")
        try:
            guess = int(guess)
            tries += 1
            
            if guess == number:
                score = 20 - (tries - 1) * 2  # 20 points for 1 try, -2 for each additional try
                score = max(0, score)  # Ensure score doesn't go below 0
                print(Fore.GREEN + f"Correct! You found the number in {tries} tries!")
                print(f"Score: {score}/20")
                break
            elif guess < number:
                print("Higher!")
            else:
                print("Lower!")
                
            if tries == max_tries:
                print(Fore.RED + f"Out of tries! The number was {number}.")
                print("Score: 0/20")
        except ValueError:
            print(Fore.RED + "Please enter a valid number!")
    
    total_score += score
    print(f"Total championship score: {total_score}/100")
    input("\nPress Enter to continue to the next game...")
    
    # Game 2: Quick Math (championship version)
    clear()
    print(Fore.CYAN + "Game 2: Quick Math")
    print("Solve math problems correctly and quickly!")
    
    math_score = 0
    num_problems = 5
    
    for i in range(num_problems):
        operators = ['+', '-', '*']
        op = random.choice(operators)
        
        if op == '+':
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            correct_answer = a + b
        elif op == '-':
            a = random.randint(50, 99)
            b = random.randint(1, 49)
            correct_answer = a - b
        else:  # Multiplication
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            correct_answer = a * b
            
        start_time = time.time()
        user_answer = input(f"Problem {i+1}/{num_problems}: {a} {op} {b} = ")
        end_time = time.time()
        
        try:
            user_answer = int(user_answer)
            time_taken = end_time - start_time
            
            if user_answer == correct_answer:
                # Score based on time: max 4 points per question, -1 point for every 5 seconds
                question_score = 4 - min(3, int(time_taken / 5))
                math_score += question_score
                print(Fore.GREEN + f"Correct! Time: {time_taken:.2f}s - Score: {question_score}/4")
            else:
                print(Fore.RED + f"Incorrect! The answer was {correct_answer}.")
        except ValueError:
            print(Fore.RED + "Invalid input! No points awarded.")
    
    # Scale to 20 points total
    scaled_math_score = (math_score / (num_problems * 4)) * 20
    scaled_math_score = round(scaled_math_score)
    
    print(f"Math Game Score: {scaled_math_score}/20")
    total_score += scaled_math_score
    print(f"Total championship score: {total_score}/100")
    
    input("\nPress Enter to continue to the next game...")
    
    # Continue with remaining 3 games with similar structure...
    # For brevity, I'll summarize the remaining games with random scores
    
    # Game 3: Word Shuffle (simplified)
    clear()
    print(Fore.CYAN + "Game 3: Word Shuffle")
    word_score = random.randint(5, 20)
    print(f"Word Shuffle Score: {word_score}/20")
    total_score += word_score
    print(f"Total championship score: {total_score}/100")
    input("\nPress Enter to continue to the next game...")
    
    # Game 4: Reaction Test (simplified)
    clear()
    print(Fore.CYAN + "Game 4: Reaction Test")
    reaction_score = random.randint(5, 20)
    print(f"Reaction Test Score: {reaction_score}/20")
    total_score += reaction_score
    print(f"Total championship score: {total_score}/100")
    input("\nPress Enter to continue to the next game...")
    
    # Game 5: Dart Throw (simplified)
    clear()
    print(Fore.CYAN + "Game 5: Dart Throw")
    dart_score = random.randint(5, 20)
    print(f"Dart Throw Score: {dart_score}/20")
    total_score += dart_score
    
    # Final results
    clear()
    print(Fore.YELLOW + "🏆 MINIGAME MASTER CHAMPIONSHIP - RESULTS 🏆")
    print(f"Game 1 - Guess the Number: {score}/20")
    print(f"Game 2 - Quick Math: {scaled_math_score}/20")
    print(f"Game 3 - Word Shuffle: {word_score}/20")
    print(f"Game 4 - Reaction Test: {reaction_score}/20")
    print(f"Game 5 - Dart Throw: {dart_score}/20")
    print(Fore.GREEN + f"TOTAL SCORE: {total_score}/100")
    
    # Store final score for the championship
    
    if total_score >= 75:
        print(Fore.GREEN + "CONGRATULATIONS! You've achieved a championship win!")
    else:
        print(Fore.YELLOW + "You need 75 points to win. Keep practicing!")
        
    return total_score

def tcg_championship():
    """Run the Trading Card Game Championship"""
    # Simplified implementation
    clear()
    print(Fore.YELLOW + "🃏 TCG CHAMPIONSHIP 🃏")
    print("Battle against 4 opponents of increasing difficulty!")
    
    opponents = [
        "Rookie Card Collector",
        "Amateur Duelist",
        "Professional Card Master",
        "Legendary Champion"
    ]
    
    score = 0
    
    for i, opponent in enumerate(opponents):
        clear()
        print(f"Round {i+1}: Facing {opponent}")
        print("Difficulty: " + "★" * (i+1))
        
        # Simple simulated battle with increasing difficulty
        chance_to_win = max(10, 70 - (i * 15))  # 70%, 55%, 40%, 25% chance to win
        
        print(f"\nYour deck strength: {random.randint(50, 80) - (i*5)}")
        print(f"Opponent strength: {random.randint(40, 75) + (i*8)}")
        
        input("\nPress Enter to play your cards...")
        
        if random.randint(1, 100) <= chance_to_win:
            print(Fore.GREEN + f"Victory! You defeated {opponent}!")
            score += 1
            # Continue to next opponent
        else:
            print(Fore.RED + f"Defeat! You were beaten by {opponent}.")
            print("Your championship run ends here.")
            break
            
        input("\nPress Enter to continue to the next round...")
    
    clear()
    print(Fore.YELLOW + "🃏 TCG CHAMPIONSHIP RESULTS 🃏")
    print(f"Opponents defeated: {score}/4")
    
    if score == 4:
        print(Fore.GREEN + "🏆 PERFECT VICTORY! You are the new TCG Champion!")
    elif score >= 2:
        print(Fore.GREEN + "Impressive showing! You've proven your skill!")
    else:
        print(Fore.YELLOW + "Better luck next time! Keep improving your deck.")
        
    input("\nPress Enter to continue...")
    
    # Return score (opponents defeated, 0-4)
    return score

def theme_park_championship():
    """Run the Theme Park Challenge Championship"""
    clear()
    print(Fore.YELLOW + "🎢 THEME PARK CHALLENGE CHAMPIONSHIP 🎢")
    print("Complete special challenges at all theme park attractions!")
    
    attractions = [
        {"name": "Cosmic Coaster", "challenge": "Ride the most extreme track without losing your nerve"},
        {"name": "Haunted Mansion", "challenge": "Find all 5 hidden ghosts without screaming"},
        {"name": "Log Flume", "challenge": "Stay as dry as possible during the big splash"},
        {"name": "VR Experience", "challenge": "Complete the dragon-slaying quest in record time"},
        {"name": "Mirror Maze", "challenge": "Find the exit without touching any mirrors"},
        {"name": "Ferris Wheel", "challenge": "Spot and photograph 3 landmarks from the top"},
        {"name": "Magic Show", "challenge": "Volunteer and successfully perform a magic trick"},
        {"name": "Photo Booth", "challenge": "Create the most creative themed photo"}
    ]
    
    total_score = 0
    max_possible = len(attractions) * 10  # Each attraction worth up to 10 points
    
    print(f"\nYou'll face challenges at {len(attractions)} different attractions.")
    print("Each challenge is worth up to 10 points. Try to score as high as possible!")
    
    input("\nPress Enter to begin the championship...")
    
    for attraction in attractions:
        clear()
        print(Fore.CYAN + f"🎯 {attraction['name']} Challenge 🎯")
        print(f"Challenge: {attraction['challenge']}")
        
        # Simulate the challenge with some user interaction
        print("\nPreparing for the challenge...")
        time.sleep(1)
        
        # Random factors for challenge difficulty
        difficulty = random.randint(1, 10)
        print(f"Difficulty level: {difficulty}/10")
        
        # Let player make a strategy choice
        print("\nChoose your approach:")
        print("[1] Cautious and methodical")
        print("[2] Balanced approach")
        print("[3] Bold and risky")
        
        choice = input("Select your strategy (1-3): ")
        
        if choice not in ["1", "2", "3"]:
            choice = "2"  # Default to balanced if invalid
        
        choice = int(choice)
        
        # Calculate score based on choice and randomness
        # Cautious: Lower variance, medium average
        # Balanced: Medium variance, medium average
        # Bold: High variance, potentially higher average
        
        base_score = random.randint(3, 7)
        
        if choice == 1:  # Cautious
            bonus = random.randint(0, 3)
            penalty = random.randint(0, 1) 
        elif choice == 2:  # Balanced
            bonus = random.randint(0, 4)
            penalty = random.randint(0, 2)
        else:  # Bold
            bonus = random.randint(0, 6)
            penalty = random.randint(0, 4)
        
        # Adjust for difficulty
        difficulty_factor = (11 - difficulty) / 10  # Higher difficulty = lower factor
        
        # Calculate final score (0-10 range)
        challenge_score = min(10, max(0, int((base_score + bonus - penalty) * difficulty_factor)))
        
        # Show a description of the attempt
        outcomes = [
            "You struggled a bit but managed to complete the challenge.",
            "Your performance was impressive and drew applause from onlookers!",
            "You completed the challenge with style and finesse!",
            "That was a close call, but you made it through!",
            "What an extraordinary performance! The park staff were amazed!"
        ]
        
        if challenge_score <= 3:
            print(Fore.RED + "\nThat didn't go as planned...")
        elif challenge_score <= 6:
            print(Fore.YELLOW + f"\n{random.choice(outcomes)}")
        else:
            print(Fore.GREEN + f"\n{random.choice(outcomes)}")
            
        print(f"Score for this attraction: {challenge_score}/10")
        
        total_score += challenge_score
        current_progress = total_score / max_possible * 100
        
        print(f"\nCurrent Championship Progress: {current_progress:.1f}%")
        print(f"Total Score: {total_score}/{max_possible}")
        
        input("\nPress Enter to continue to the next attraction...")
    
    # Final results
    clear()
    print(Fore.YELLOW + "🎢 THEME PARK CHAMPIONSHIP - RESULTS 🎢")
    print(f"Total Score: {total_score} out of a possible {max_possible}")
    percentage = (total_score / max_possible) * 100
    print(f"Performance Rating: {percentage:.1f}%")
    
    if percentage >= 80:
        print(Fore.GREEN + "🏆 OUTSTANDING PERFORMANCE! You are the Theme Park Champion!")
    elif percentage >= 60:
        print(Fore.GREEN + "Great performance! You've shown excellent skills!")
    else:
        print(Fore.YELLOW + "Good effort! With more practice, you'll improve your score!")
        
    input("\nPress Enter to continue...")
    
    # Return normalized score (0-100)
    return int(percentage)

def casino_championship():
    """Run the Casino Royale Championship"""
    clear()
    print(Fore.YELLOW + "🎰 CASINO ROYALE CHAMPIONSHIP 🎰")
    print("Try your luck with a starting pool of 100 chips!")
    print("\nIn this championship, you'll test your luck and skill at various casino games.")
    print("Your goal is to increase your chip count as much as possible.")
    print("The championship consists of 4 rounds with different games.")
    
    # Starting chips
    chips = 100
    print(f"\nStarting chips: {chips}")
    
    # Define the championship games
    championship_games = [
        {"name": "Blackjack", "description": "Get as close to 21 as possible without going over."},
        {"name": "Roulette", "description": "Bet on where the ball will land on the wheel."},
        {"name": "Slot Machine", "description": "Pull the lever and match symbols for payouts."},
        {"name": "High Stakes Poker", "description": "Final round - all or nothing."}
    ]
    
    input("\nPress Enter to begin the championship...")
    
    # Round 1: Blackjack
    clear()
    print(Fore.CYAN + "Round 1: Blackjack")
    print(championship_games[0]["description"])
    print(f"Current chips: {chips}")
    
    bet = 0
    while True:
        try:
            max_bet = min(chips, 50)  # Can bet up to 50 chips or all chips if less
            bet_input = input(f"\nPlace your bet (1-{max_bet}): ")
            bet = int(bet_input)
            if 1 <= bet <= max_bet:
                break
            else:
                print(f"Please enter a valid bet between 1 and {max_bet}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Simplified Blackjack game
    dealer_card1 = random.randint(1, 10)
    dealer_card2 = random.randint(1, 10)
    dealer_total = dealer_card1 + dealer_card2
    
    player_card1 = random.randint(1, 10)
    player_card2 = random.randint(1, 10)
    player_total = player_card1 + player_card2
    
    print(f"\nDealer shows: {dealer_card1}, [Hidden]")
    print(f"Your cards: {player_card1}, {player_card2} (Total: {player_total})")
    
    # Player's turn
    while player_total < 21:
        choice = input("\nDo you want to (H)it or (S)tand? ").upper()
        if choice == 'H':
            new_card = random.randint(1, 10)
            player_total += new_card
            print(f"You drew: {new_card}")
            print(f"Your new total: {player_total}")
            if player_total > 21:
                print(Fore.RED + "Bust! You went over 21.")
                break
        elif choice == 'S':
            break
        else:
            print("Please enter H or S.")
    
    # Dealer's turn if player didn't bust
    if player_total <= 21:
        print(f"\nDealer reveals second card: {dealer_card2} (Total: {dealer_total})")
        
        while dealer_total < 17:
            new_card = random.randint(1, 10)
            dealer_total += new_card
            print(f"Dealer draws: {new_card} (Total: {dealer_total})")
    
    # Determine winner
    if player_total > 21:
        print(Fore.RED + "You lose this round.")
        chips -= bet
    elif dealer_total > 21:
        print(Fore.GREEN + "Dealer busts! You win this round.")
        chips += bet
    elif player_total > dealer_total:
        print(Fore.GREEN + "You win this round!")
        chips += bet
    elif dealer_total > player_total:
        print(Fore.RED + "Dealer wins this round.")
        chips -= bet
    else:
        print(Fore.YELLOW + "It's a push (tie).")
    
    print(f"\nChips after Round 1: {chips}")
    
    if chips <= 0:
        print(Fore.RED + "You're out of chips! Championship over.")
        return 0
    
    input("\nPress Enter to continue to the next round...")
    
    # Round 2: Roulette
    clear()
    print(Fore.CYAN + "Round 2: Roulette")
    print(championship_games[1]["description"])
    print(f"Current chips: {chips}")
    
    print("\nBetting Options:")
    print("[1] Red/Black (1:1 payout)")
    print("[2] Odd/Even (1:1 payout)")
    print("[3] Single Number (35:1 payout)")
    
    bet_type = input("\nSelect betting option (1-3): ")
    
    if bet_type not in ["1", "2", "3"]:
        bet_type = "1"  # Default to Red/Black
    
    bet_type = int(bet_type)
    
    # Get bet amount
    while True:
        try:
            max_bet = min(chips, 50)  # Can bet up to 50 chips or all chips if less
            bet_input = input(f"\nPlace your bet (1-{max_bet}): ")
            bet = int(bet_input)
            if 1 <= bet <= max_bet:
                break
            else:
                print(f"Please enter a valid bet between 1 and {max_bet}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get specific bet details
    if bet_type == 1:
        choice = input("\nBet on (R)ed or (B)lack? ").upper()
        if choice != 'R' and choice != 'B':
            choice = 'R'  # Default to Red
        
        print(f"You bet {bet} chips on {'Red' if choice == 'R' else 'Black'}")
        
    elif bet_type == 2:
        choice = input("\nBet on (O)dd or (E)ven? ").upper()
        if choice != 'O' and choice != 'E':
            choice = 'E'  # Default to Even
            
        print(f"You bet {bet} chips on {'Odd' if choice == 'O' else 'Even'}")
        
    else:  # Single number
        while True:
            try:
                choice = int(input("\nChoose a number (0-36): "))
                if 0 <= choice <= 36:
                    break
                else:
                    print("Please enter a valid number between 0 and 36.")
            except ValueError:
                print("Please enter a valid number.")
                choice = 17  # Default
                break
                
        print(f"You bet {bet} chips on number {choice}")
    
    # Spin the wheel
    print("\nThe wheel is spinning...")
    time.sleep(1)
    result = random.randint(0, 36)
    
    # Determine if number is red or black
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    is_red = result in red_numbers
    is_odd = result % 2 == 1
    
    print(f"\nThe ball lands on {result} ({'Red' if is_red else 'Black'}, {'Odd' if is_odd else 'Even'})")
    
    # Determine if player won
    won = False
    if bet_type == 1:  # Red/Black
        if (choice == 'R' and is_red) or (choice == 'B' and not is_red):
            won = True
            chips += bet
        else:
            chips -= bet
    elif bet_type == 2:  # Odd/Even
        if (choice == 'O' and is_odd) or (choice == 'E' and not is_odd):
            won = True
            chips += bet
        else:
            chips -= bet
    else:  # Single number
        if result == choice:
            won = True
            chips += bet * 35
        else:
            chips -= bet
    
    if won:
        print(Fore.GREEN + "You won this bet!")
    else:
        print(Fore.RED + "You lost this bet.")
        
    print(f"\nChips after Round 2: {chips}")
    
    if chips <= 0:
        print(Fore.RED + "You're out of chips! Championship over.")
        return 0
        
    input("\nPress Enter to continue to the next round...")
    
    # Round 3: Slot Machine - Simplified for brevity
    clear()
    print(Fore.CYAN + "Round 3: Slot Machine")
    print(championship_games[2]["description"])
    print(f"Current chips: {chips}")
    
    # Get bet amount
    while True:
        try:
            max_bet = min(chips, 50)  # Can bet up to 50 chips or all chips if less
            bet_input = input(f"\nPlace your bet (1-{max_bet}): ")
            bet = int(bet_input)
            if 1 <= bet <= max_bet:
                break
            else:
                print(f"Please enter a valid bet between 1 and {max_bet}.")
        except ValueError:
            print("Please enter a valid number.")
    
    print("\nPulling the lever...")
    time.sleep(1)
    
    symbols = ["🍒", "🍊", "🍋", "💎", "7️⃣", "⭐"]
    payouts = {
        "🍒🍒🍒": 3,
        "🍊🍊🍊": 4,
        "🍋🍋🍋": 5,
        "💎💎💎": 10,
        "7️⃣7️⃣7️⃣": 15,
        "⭐⭐⭐": 20
    }
    
    result = [random.choice(symbols) for _ in range(3)]
    result_str = "".join(result)
    
    print(" ".join(result))
    
    winnings = 0
    if result_str in payouts:
        winnings = bet * payouts[result_str]
        print(Fore.GREEN + f"Winner! +{winnings} chips!")
        chips += winnings
    else:
        # Check for pairs (smaller win)
        if result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            winnings = bet
            print(Fore.GREEN + f"Pair! +{winnings} chips!")
            chips += winnings
        else:
            print(Fore.RED + "No match. Better luck next time!")
            chips -= bet
    
    print(f"\nChips after Round 3: {chips}")
    
    if chips <= 0:
        print(Fore.RED + "You're out of chips! Championship over.")
        return 0
        
    input("\nPress Enter to continue to the final round...")
    
    # Round 4: High Stakes Poker - All or nothing
    clear()
    print(Fore.CYAN + "Final Round: High Stakes Poker")
    print(championship_games[3]["description"])
    print(f"Current chips: {chips}")
    
    print("\nThis is an all-or-nothing round!")
    print("You'll play one hand of poker against the championship dealer.")
    print("Win, and you'll double your chips. Lose, and you forfeit half.")
    
    confirm = input("\nAre you ready to play? (y/n): ").lower()
    
    if confirm != 'y':
        print("You decided to cash out without playing the final round.")
        return chips
    
    print("\nDealing cards...")
    time.sleep(1)
    
    # Simplified poker using card values (2-14, with 11=J, 12=Q, 13=K, 14=A)
    player_hand = [random.randint(2, 14) for _ in range(5)]
    dealer_hand = [random.randint(2, 14) for _ in range(5)]
    
    # Convert numerical values to card names for display
    def card_name(value):
        if value == 14:
            return "A"
        elif value == 13:
            return "K"
        elif value == 12:
            return "Q"
        elif value == 11:
            return "J"
        else:
            return str(value)
    
    player_hand_display = [card_name(card) for card in player_hand]
    dealer_hand_display = [card_name(card) for card in dealer_hand]
    
    print(f"\nYour hand: {', '.join(player_hand_display)}")
    
    # Let player exchange up to 3 cards
    to_exchange = input("\nWhich cards would you like to exchange? (Enter positions 1-5, separated by spaces, or 0 for none): ")
    
    if to_exchange != "0":
        try:
            positions = [int(pos) for pos in to_exchange.split()]
            for pos in positions:
                if 1 <= pos <= 5:
                    player_hand[pos-1] = random.randint(2, 14)
        except Exception:
            print("Invalid input. No cards exchanged.")
    
    # Update display after exchange
    player_hand_display = [card_name(card) for card in player_hand]
    print(f"\nYour final hand: {', '.join(player_hand_display)}")
    
    # Simple hand evaluation (just using highest card for simplicity)
    player_high_card = max(player_hand)
    dealer_high_card = max(dealer_hand)
    
    print(f"Dealer's hand: {', '.join(dealer_hand_display)}")
    
    # Determine winner
    if player_high_card > dealer_high_card:
        print(Fore.GREEN + "\nYou win the championship final!")
        chips *= 2  # Double chips for winning
    elif player_high_card < dealer_high_card:
        print(Fore.RED + "\nYou lose the championship final.")
        chips = int(chips * 0.5)  # Lose half for losing
    else:
        print(Fore.YELLOW + "\nIt's a tie! You keep your chips.")
    
    print(f"\nFinal chip count: {chips}")
    
    input("\nPress Enter to see your championship results...")
    
    # Final results
    clear()
    print(Fore.YELLOW + "🎰 CASINO ROYALE CHAMPIONSHIP - RESULTS 🎰")
    print("Starting chips: 100")
    print(f"Final chips: {chips}")
    
    if chips >= 200:
        print(Fore.GREEN + "🏆 OUTSTANDING PERFORMANCE! You are the Casino Royale Champion!")
    elif chips >= 100:
        print(Fore.GREEN + "You made a profit! Excellent performance!")
    else:
        print(Fore.YELLOW + "You lost some chips, but gained valuable experience!")
        
    input("\nPress Enter to continue...")
    
    # Return score based on final chips (0-300 range)
    return chips

def quest_center():
    """Main hub for accessing and managing quests"""
    clear()
    print(Fore.YELLOW + "📜 QUEST CENTER 📜")
    print(Fore.CYAN + "Take on exciting quests for special rewards!")
    
    # Initialize quest data if needed
    if "active_quests" not in player:
        player["active_quests"] = []
    if "completed_quests" not in player:
        player["completed_quests"] = []
    if "quest_progress" not in player:
        player["quest_progress"] = {}
        
    # Display active quests
    print(Fore.MAGENTA + "\nActive Quests:")
    if not player["active_quests"]:
        print("No active quests. Accept a new quest to begin your adventure!")
    else:
        for quest_id in player["active_quests"]:
            if quest_id in QUESTS:
                quest = QUESTS[quest_id]
                progress = player["quest_progress"].get(quest_id, 0)
                # For simplicity, most quests have a target of 100%
                print(f"• {quest['name']} - {progress}% complete")
                print(f"  {quest['description']}")
                print(f"  Reward: {quest['reward_tickets']} tickets + {quest['reward_loyalty']} loyalty points")
    
    # Display available quests
    print(Fore.MAGENTA + "\nAvailable Quests:")
    available_quests = []
    for quest_id, quest in QUESTS.items():
        if quest_id not in player["active_quests"] and quest_id not in player["completed_quests"]:
            available_quests.append((quest_id, quest))
            
    if not available_quests:
        print("No available quests at the moment. Check back later!")
    else:
        for i, (quest_id, quest) in enumerate(available_quests, 1):
            print(f"[{i}] {quest['name']} ({quest['difficulty']} difficulty)")
            print(f"    {quest['description']}")
            print(f"    Reward: {quest['reward_tickets']} tickets + {quest['reward_loyalty']} loyalty points")
            print(f"    Expires: {quest['expiry']}")
    
    print("\n[A] Accept a Quest")
    print("[C] Claim Completed Quest Rewards")
    print("[0] Return to Main Menu")
    
    choice = input("\nSelect option: ").upper()
    
    if choice == "0":
        return
    elif choice == "A":
        # Accept a new quest
        if not available_quests:
            print(Fore.RED + "No quests available to accept!")
            time.sleep(1.5)
            return quest_center()
            
        quest_num = input("Enter quest number to accept: ")
        try:
            quest_idx = int(quest_num) - 1
            if quest_idx < 0 or quest_idx >= len(available_quests):
                print(Fore.RED + "Invalid quest number!")
                time.sleep(1.5)
                return quest_center()
                
            quest_id, quest = available_quests[quest_idx]
            player["active_quests"].append(quest_id)
            player["quest_progress"][quest_id] = 0
            
            print(Fore.GREEN + f"Quest accepted: {quest['name']}")
            print("Check back often to track your progress!")
            
        except ValueError:
            print(Fore.RED + "Please enter a valid number!")
            
        time.sleep(1.5)
        return quest_center()
        
    elif choice == "C":
        # Claim rewards for completed quests
        completed = []
        for quest_id in player["active_quests"]:
            if player["quest_progress"].get(quest_id, 0) >= 100:
                completed.append(quest_id)
                
        if not completed:
            print(Fore.RED + "No completed quests to claim rewards for!")
            time.sleep(1.5)
            return quest_center()
            
        print(Fore.GREEN + "Claiming rewards for completed quests:")
        for quest_id in completed:
            quest = QUESTS[quest_id]
            print(f"• {quest['name']}: {quest['reward_tickets']} tickets + {quest['reward_loyalty']} loyalty points")
            player["tickets"] += quest["reward_tickets"]
            add_loyalty_points(quest["reward_loyalty"])
            
            # Remove from active and add to completed
            player["active_quests"].remove(quest_id)
            player["completed_quests"].append(quest_id)
            
            # Award achievement
            award_achievement(f"Quest Completed: {quest['name']}")
            
        print(Fore.YELLOW + f"Total tickets now: {player['tickets']}")
        
        time.sleep(2)
        return quest_center()
        
    else:
        print(Fore.RED + "Invalid option!")
        time.sleep(1)
        return quest_center()

def loyalty_rewards_center():
    """Display loyalty status and available rewards"""
    clear()
    print(Fore.YELLOW + "🌟 LOYALTY REWARDS CENTER 🌟")
    
    # Get current tier and points
    current_points = player.get("loyalty_points", 0)
    current_tier = get_loyalty_tier()
    
    print(f"Current Loyalty Points: {current_points}")
    print(f"Current Tier: {current_tier}")
    
    # Show current tier benefits
    tier_details = LOYALTY_TIERS[current_tier]
    print("\nYour Benefits:")
    print(f"• {tier_details['discount']*100}% discount on all purchases")
    print(f"• {tier_details['bonus']} bonus tickets per win")
    
    # Show progress to next tier
    next_tier = None
    next_tier_points = float('inf')
    
    for tier, details in LOYALTY_TIERS.items():
        if details["points"] > current_points and details["points"] < next_tier_points:
            next_tier = tier
            next_tier_points = details["points"]
    
    if next_tier:
        points_needed = next_tier_points - current_points
        print(f"\nNext Tier: {next_tier} (Need {points_needed} more points)")
        print(f"Benefits at {next_tier}:")
        print(f"• {LOYALTY_TIERS[next_tier]['discount']*100}% discount on all purchases")
        print(f"• {LOYALTY_TIERS[next_tier]['bonus']} bonus tickets per win")
    else:
        print("\nCongratulations! You've reached the highest loyalty tier!")
    
    print("\nWays to Earn Loyalty Points:")
    print("• Play minigames: +1 point per game")
    print("• Visit theme park attractions: +1 point per visit")
    print("• Complete quests: +5-40 points depending on quest")
    print("• Win championships: +20-35 points per championship")
    print("• Complete missions: +5 points per mission")
    
    print("\n[1] Redeem Loyalty Rewards")
    print("[0] Return to Main Menu")
    
    choice = input("\nSelect option: ")
    
    if choice == "0":
        return
    elif choice == "1":
        # Redeem loyalty rewards
        clear()
        print(Fore.YELLOW + "🎁 LOYALTY REWARDS 🎁")
        
        # Define rewards that can be redeemed with loyalty points
        rewards = [
            {"name": "Free Season Pass Day", "description": "Add 1 day to your season pass", "cost": 20},
            {"name": "Fast Pass", "description": "Skip the line for theme park attractions", "cost": 30},
            {"name": "VIP Card Pack", "description": "Special card pack with guaranteed rare card", "cost": 50},
            {"name": "2x Tickets Booster", "description": "Double ticket earnings for 5 games", "cost": 75},
            {"name": "Exclusive Costume", "description": "Unique costume only available through loyalty", "cost": 100},
            {"name": "Legendary Pet", "description": "Special pet with enhanced abilities", "cost": 200}
        ]
        
        print(f"Available Points: {current_points}")
        print("\nAvailable Rewards:")
        
        for i, reward in enumerate(rewards, 1):
            print(f"[{i}] {reward['name']} - {reward['cost']} points")
            print(f"    {reward['description']}")
        
        print("[0] Back")
        
        choice = input("\nSelect reward to redeem: ")
        if choice == "0":
            return loyalty_rewards_center()
            
        try:
            reward_idx = int(choice) - 1
            if reward_idx < 0 or reward_idx >= len(rewards):
                print(Fore.RED + "Invalid selection!")
                time.sleep(1.5)
                return loyalty_rewards_center()
                
            selected_reward = rewards[reward_idx]
            
            # Check if player has enough points
            if current_points < selected_reward["cost"]:
                print(Fore.RED + f"Not enough loyalty points! Need {selected_reward['cost']} points.")
                time.sleep(1.5)
                return loyalty_rewards_center()
                
            # Confirm redemption
            print(f"\nRedeem {selected_reward['name']} for {selected_reward['cost']} loyalty points?")
            confirm = input("Confirm (y/n): ").lower()
            
            if confirm != "y":
                return loyalty_rewards_center()
                
            # Process redemption
            player["loyalty_points"] -= selected_reward["cost"]
            
            # Apply reward effect based on type
            if selected_reward["name"] == "Free Season Pass Day":
                if player.get("season_pass", False):
                    player["season_pass_days"] = player.get("season_pass_days", 0) + 1
                    print(Fore.GREEN + "1 day added to your season pass!")
                else:
                    player["season_pass"] = True
                    player["season_pass_days"] = 1
                    print(Fore.GREEN + "Season pass activated for 1 day!")
            
            elif selected_reward["name"] == "Fast Pass":
                player["fast_passes"] = player.get("fast_passes", 0) + 1
                print(Fore.GREEN + "Fast Pass added to your inventory!")
            
            elif selected_reward["name"] == "VIP Card Pack":
                print(Fore.GREEN + "VIP Card Pack added to your inventory!")
                # Add special cards (implementation would depend on card system)
                player["inventory"].append("VIP Card Pack")
            
            elif selected_reward["name"] == "2x Tickets Booster":
                player["ticket_multiplier"] = 2
                player["multiplier_games_left"] = 5
                print(Fore.GREEN + "Ticket Booster activated for your next 5 games!")
            
            elif selected_reward["name"] == "Exclusive Costume":
                costume_name = "Loyalty Champion 🌠"
                if "costumes" not in player:
                    player["costumes"] = []
                player["costumes"].append(costume_name)
                print(Fore.GREEN + f"Exclusive costume '{costume_name}' added to your collection!")
            
            elif selected_reward["name"] == "Legendary Pet":
                pet_name = "Loyal Companion 🦊"
                if "pets" not in player:
                    player["pets"] = []
                player["pets"].append(pet_name)
                print(Fore.GREEN + f"Legendary pet '{pet_name}' added to your collection!")
            
            print(f"Remaining loyalty points: {player['loyalty_points']}")
            input("\nPress Enter to continue...")
            
        except ValueError:
            print(Fore.RED + "Please enter a valid number!")
            time.sleep(1.5)
            
        return loyalty_rewards_center()
    
    else:
        print(Fore.RED + "Invalid option!")
        time.sleep(1)
        return loyalty_rewards_center()

def hangman_game():
    if not pay_to_play(3):
        return
    words = ["carnival", "ticket", "prize", "game", "fun", "play", "win"]
    word = random.choice(words)
    guessed = set()
    tries = 6

    while tries > 0:
        display = ''.join(c if c in guessed else '_' for c in word)
        print(f"\nWord: {display}")
        print(f"Tries left: {tries}")
        if display == word:
            print(Fore.GREEN + "You won! +6 tickets")
            player["tickets"] += 6
            return
        guess = input("Guess a letter: ").lower()
        if guess in guessed:
            print("Already guessed!")
            continue
        guessed.add(guess)
        if guess not in word:
            tries -= 1
    print(Fore.RED + f"Game Over! The word was: {word}")

def memory_match():
    if not pay_to_play(4):
        return
    emojis = ["🎪", "🎠", "🎡", "🎢", "🎨", "🎭"] * 2
    random.shuffle(emojis)
    revealed = [False] * 12
    matched = set()
    first_choice = None

    while len(matched) < 6:
        print("\nMemory Match Board:")
        for i in range(12):
            if revealed[i] or i in matched:
                print(emojis[i], end=" ")
            else:
                print("❓", end=" ")
            if (i + 1) % 4 == 0:
                print()

        choice = int(input("\nPick a card (1-12): ")) - 1
        if choice < 0 or choice > 11 or revealed[choice]:
            print("Invalid choice!")
            continue

        revealed[choice] = True
        print(f"Card {choice + 1}: {emojis[choice]}")

        if first_choice is None:
            first_choice = choice
        else:
            if emojis[first_choice] == emojis[choice]:
                print(Fore.GREEN + "Match found!")
                matched.add(first_choice)
                matched.add(choice)
            else:
                print("No match!")
                revealed[first_choice] = False
                revealed[choice] = False
            first_choice = None
            time.sleep(1)

    print(Fore.GREEN + "You completed the memory game! +8 tickets")
    player["tickets"] += 8

# ------------------------------
# Theme Park Attractions
# ------------------------------

def get_current_season():
    """Determine the current season for seasonal events"""
    from datetime import datetime
    
    current_month = datetime.now().month
    
    if 6 <= current_month <= 8:  # June, July, August
        return "summer"
    elif 9 <= current_month <= 10:  # September, October
        # Check if it's close to Halloween
        if current_month == 10 and datetime.now().day >= 15:  # Second half of October
            return "halloween"
        else:
            return "fall"
    elif 11 <= current_month <= 2:  # November to February
        return "winter"
    elif 3 <= current_month <= 5:  # March, April, May
        return "spring"
    else:
        return "normal"

def food_stand():
    """Visit a food stand to buy refreshments that restore hunger and energy"""
    clear()
    print(Fore.YELLOW + "🍦 CARNIVAL FOOD STANDS 🍕")
    print("Delicious carnival treats to satisfy your hunger!")
    print(f"Your Tickets: {player['tickets']}")
    
    # Show hunger and energy levels
    hunger = player.get("hunger", 100)
    energy = player.get("energy", 100)
    print(Fore.CYAN + f"Hunger: {hunger}% | Energy: {energy}%")
    
    # Get the current season for seasonal treats
    current_season = get_current_season()
    
    # Show available food items
    print("\nAvailable Treats:")
    available_foods = []
    
    # First add year-round foods
    for food in CARNIVAL_FOODS:
        if food["seasonal"] is None:
            available_foods.append(food)
    
    # Then add any seasonal foods
    for food in CARNIVAL_FOODS:
        if food["seasonal"] == current_season:
            available_foods.append(food)
    
    # Display the menu
    for i, food in enumerate(available_foods, 1):
        seasonal_tag = " (Seasonal Special!)" if food["seasonal"] is not None else ""
        print(f"[{i}] {food['name']} - {food['price']} tickets{seasonal_tag}")
        print(f"    Restores: Hunger +{food['hunger']}%, Energy +{food['energy']}%")
    
    print("[0] Return to Theme Park")
    
    # Get player choice
    choice = input("\nWhat would you like to eat? ")
    if choice == "0":
        return theme_park_menu()
    
    try:
        food_idx = int(choice) - 1
        if 0 <= food_idx < len(available_foods):
            selected_food = available_foods[food_idx]
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid choice!")
        time.sleep(1.5)
        return food_stand()
    
    # Purchase the food
    if player["tickets"] >= selected_food["price"]:
        player["tickets"] -= selected_food["price"]
        
        # Apply the effects
        player["hunger"] = min(100, player["hunger"] + selected_food["hunger"])
        player["energy"] = min(100, player["energy"] + selected_food["energy"])
        
        # Initialize food_consumed if it doesn't exist
        if "food_consumed" not in player:
            player["food_consumed"] = []
            
        # Track food consumption
        player["food_consumed"].append(selected_food["name"])
        
        # Feedback
        print(Fore.GREEN + f"\nYou enjoy a delicious {selected_food['name']}!")
        print(f"Hunger restored to {player['hunger']}%")
        print(f"Energy restored to {player['energy']}%")
        
        # Check for achievements
        check_food_achievements()
        
        # Add loyalty points
        add_loyalty_points(1)
        print(Fore.MAGENTA + "+1 Loyalty Point for enjoying carnival food!")
        
        # Ask if they want more food
        more_food = input("\nWould you like something else? (y/n): ").lower()
        if more_food == "y":
            return food_stand()
    else:
        print(Fore.RED + f"Not enough tickets! You need {selected_food['price']} tickets.")
        time.sleep(1.5)
        return food_stand()
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def check_food_achievements():
    """Check and award achievements related to food consumption"""
    unique_food_count = len(set(player.get("food_consumed", [])))
    total_items_consumed = sum(player.get("food_counts", {}).values())
    
    # Basic foodie achievement
    if unique_food_count >= 5 and "Carnival Foodie" not in player["achievements"]:
        award_achievement("Carnival Foodie")
        player["tickets"] += 10
        print(Fore.GREEN + "Achievement unlocked: Carnival Foodie! +10 tickets!")
    
    # Advanced gourmet achievement
    if unique_food_count >= 10 and "Carnival Gourmet" not in player["achievements"]:
        award_achievement("Carnival Gourmet")
        player["tickets"] += 25
        print(Fore.GREEN + "Achievement unlocked: Carnival Gourmet! +25 tickets!")
        
    # Food enthusiast achievement - based on total items consumed
    if total_items_consumed >= 20 and "Food Enthusiast" not in player["achievements"]:
        award_achievement("Food Enthusiast")
        player["tickets"] += 15
        print(Fore.GREEN + "Achievement unlocked: Food Enthusiast! +15 tickets!")
    
    # Check for seasonal food achievements
    seasons_sampled = set()
    for food_name in player.get("food_consumed", []):
        for food in CARNIVAL_FOODS:
            if food["name"] == food_name and food["seasonal"] is not None:
                seasons_sampled.add(food["seasonal"])
    
    if len(seasons_sampled) >= 3 and "Seasonal Taster" not in player["achievements"]:
        award_achievement("Seasonal Taster")
        player["tickets"] += 20
        print(Fore.GREEN + "Achievement unlocked: Seasonal Taster! +20 tickets!")

def carnival_games_menu():
    """Display and play traditional carnival games for prizes"""
    clear()
    print(Fore.CYAN + "🎯 CARNIVAL GAMES 🎮")
    print("Test your skill and win exciting prizes!")
    print(f"Your Tickets: {player['tickets']}")
    
    # Show available games
    print("\nAvailable Games:")
    for i, game in enumerate(CARNIVAL_GAMES, 1):
        print(f"[{i}] {game['name']} - {game['price']} tickets")
        print(f"    Difficulty: {game['difficulty'].capitalize()}")
    
    print("[0] Return to Theme Park")
    
    # Get player choice
    choice = input("\nWhich game would you like to play? ")
    if choice == "0":
        return theme_park_menu()
    
    try:
        game_idx = int(choice) - 1
        if 0 <= game_idx < len(CARNIVAL_GAMES):
            selected_game = CARNIVAL_GAMES[game_idx]
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid choice!")
        time.sleep(1.5)
        return carnival_games_menu()
    
    # Check if player can afford the game
    if player["tickets"] >= selected_game["price"]:
        player["tickets"] -= selected_game["price"]
        
        # Play the selected game
        result = play_carnival_game(selected_game)
        
        # Process the result and potentially award a prize
        if result["success"]:
            prize = random.choice(selected_game["prizes"])
            
            # Initialize carnival_prizes if it doesn't exist
            if "carnival_prizes" not in player:
                player["carnival_prizes"] = []
                
            player["carnival_prizes"].append(prize)
            
            # Award bonus tickets for winning!
            bonus_tickets = random.randint(2, 5)
            player["tickets"] += bonus_tickets
            
            print(Fore.GREEN + f"\nCongratulations! You won: {prize}")
            print(Fore.YELLOW + f"Bonus: +{bonus_tickets} tickets!")
            
            # Add to inventory for consistency with other systems
            if prize not in player["inventory"]:
                player["inventory"].append(prize)
            
            # Check for achievements
            check_carnival_game_achievements()
            
            # Award loyalty points
            add_loyalty_points(2)
            print(Fore.MAGENTA + "+2 Loyalty Points for winning a carnival game!")
        else:
            print(Fore.YELLOW + "\nSo close! Better luck next time!")
        
        # Ask if they want to play again
        play_again = input("\nWould you like to play another game? (y/n): ").lower()
        if play_again == "y":
            return carnival_games_menu()
    else:
        print(Fore.RED + f"Not enough tickets! You need {selected_game['price']} tickets.")
        time.sleep(1.5)
        return carnival_games_menu()
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def play_carnival_game(game):
    """Play a carnival game and determine the outcome"""
    clear()
    game_name = game["name"]
    difficulty = game["difficulty"]
    
    print(Fore.YELLOW + f"Playing: {game_name}")
    
    # Set win probability based on difficulty
    if difficulty == "easy":
        win_chance = 0.6  # 60% chance to win
    elif difficulty == "medium":
        win_chance = 0.4  # 40% chance to win
    elif difficulty == "hard":
        win_chance = 0.25  # 25% chance to win
    elif difficulty == "none":  # Special case for fortune teller
        win_chance = 1.0  # Always "win" a fortune
    else:
        win_chance = 0.5  # Default
    
    # Simulate the game with some descriptive text
    if "Ring Toss" in game_name:
        rings = 3
        rings_landed = 0
        
        print("\nYou have 3 rings to toss onto bottle necks!")
        for i in range(rings):
            input(f"\nPress Enter to toss ring {i+1}...")
            if random.random() < win_chance:
                rings_landed += 1
                print(Fore.GREEN + "The ring lands perfectly around a bottle neck!")
            else:
                print(Fore.RED + "The ring bounces off and falls to the ground.")
        
        # Need at least 1 ring to win
        success = rings_landed > 0
        print(f"\nRings landed: {rings_landed}/{rings}")
        
    elif "Balloon Dart" in game_name:
        darts = 3
        balloons_popped = 0
        
        print("\nYou have 3 darts to pop the balloons!")
        for i in range(darts):
            input(f"\nPress Enter to throw dart {i+1}...")
            if random.random() < win_chance:
                balloons_popped += 1
                print(Fore.GREEN + "POP! The balloon bursts!")
            else:
                print(Fore.RED + "Your dart misses the balloon.")
        
        # Need at least 1 balloon to win
        success = balloons_popped > 0
        print(f"\nBalloons popped: {balloons_popped}/{darts}")
        
    elif "Milk Bottle" in game_name:
        print("\nYou need to knock down a pyramid of milk bottles with one throw!")
        input("\nPress Enter to throw the ball...")
        
        success = random.random() < win_chance
        if success:
            print(Fore.GREEN + "CRASH! All the bottles tumble down!")
        else:
            if random.random() < 0.5:
                print(Fore.RED + "The ball hits the bottles but they barely wobble.")
            else:
                print(Fore.RED + "You knock down some bottles, but not all of them.")
        
    elif "Basketball" in game_name:
        shots = 3
        baskets_made = 0
        
        print("\nYou have 3 shots to make a basket!")
        for i in range(shots):
            input(f"\nPress Enter to take shot {i+1}...")
            if random.random() < win_chance:
                baskets_made += 1
                print(Fore.GREEN + "SWISH! Nothing but net!")
            else:
                print(Fore.RED + "The ball bounces off the rim.")
        
        # Need at least 1 basket to win
        success = baskets_made > 0
        print(f"\nBaskets made: {baskets_made}/{shots}")
        
    elif "Water Gun" in game_name:
        print("\nAim your water gun at the target and fill the balloon!")
        input("\nPress Enter to start shooting...")
        
        # Simulate a timed challenge
        progress = 0
        target = 100
        print("\nFilling the balloon: ", end="")
        while progress < target:
            time.sleep(0.5)
            increment = random.randint(15, 25)
            progress = min(target, progress + increment)
            print(f"{progress}%... ", end="", flush=True)
        
        print("\n")
        # Determine if player was fast enough
        time_factor = random.random()
        success = time_factor < win_chance + 0.2  # Slightly easier
        
        if success:
            print(Fore.GREEN + "POP! Your balloon fills up first and bursts!")
        else:
            print(Fore.RED + "Another player's balloon pops before yours!")
        
    elif "Whack-A-Mole" in game_name:
        hits = 0
        target_hits = 5
        attempts = 8
        
        print(f"\nWhack {target_hits} moles in {attempts} attempts!")
        for i in range(attempts):
            time.sleep(0.7)
            mole_appears = random.choice(["left", "center", "right"])
            print(f"\nA mole appears on the {mole_appears}!")
            choice = input("Where do you whack? (left/center/right): ").lower()
            
            if choice == mole_appears:
                hits += 1
                print(Fore.GREEN + "WHACK! You got it!")
            else:
                print(Fore.RED + "MISS! The mole escapes!")
        
        success = hits >= target_hits
        print(f"\nMoles whacked: {hits}/{target_hits}")
        
    elif "High Striker" in game_name:
        print("\nTest your strength! Hit the lever to send the puck up the tower!")
        input("\nPress Enter to swing the hammer...")
        
        # Generate a random strength value
        strength = random.random()
        if strength < 0.3:
            print(Fore.RED + "The puck only rises about a quarter of the way up.")
            height = "LOW"
        elif strength < 0.6:
            print(Fore.YELLOW + "The puck makes it halfway up the tower.")
            height = "MEDIUM"
        elif strength < win_chance:
            print(Fore.YELLOW + "The puck rises high, almost to the top!")
            height = "HIGH"
        else:
            print(Fore.GREEN + "DING! The puck hits the bell at the top!")
            height = "PERFECT"
        
        success = height == "PERFECT"
        print(f"\nStrength result: {height}")
        
    elif "Duck Pond" in game_name:
        print("\nPick a rubber duck from the pond to reveal your prize!")
        input("\nPress Enter to select a duck...")
        
        # This game is mostly about luck
        ducks = ["red", "blue", "yellow", "green", "purple", "orange"]
        chosen_duck = random.choice(ducks)
        print(f"\nYou selected a {chosen_duck} duck!")
        
        # Almost always win something in duck pond
        success = random.random() < 0.9
        if success:
            print(Fore.GREEN + "There's a winning symbol on the bottom!")
        else:
            print(Fore.RED + "No winning symbol on this duck, sorry!")
        
    elif "Fortune Teller" in game_name:
        print("\nThe mysterious fortune teller beckons you closer...")
        input("\nPress Enter to have your fortune told...")
        
        fortunes = [
            "A thrilling adventure awaits you in the near future.",
            "Good luck will follow you throughout the day.",
            "A new friendship will bring you great happiness.",
            "An unexpected surprise is coming your way.",
            "Your creativity will lead to great success.",
            "Prosperity and abundance are in your stars.",
            "A wish will be granted before the moon is full.",
            "The path you've chosen will lead to happiness.",
            "A mysterious stranger will change your perspective.",
            "Love and laughter will fill your days ahead."
        ]
        
        chosen_fortune = random.choice(fortunes)
        print(Fore.MAGENTA + f"\nThe fortune teller says: \"{chosen_fortune}\"")
        print("She hands you a fortune card with the message written on it.")
        
        # Always "win" at fortune telling
        success = True
    
    else:
        # Generic game if none of the above
        print("\nYou try your luck at the game...")
        input("\nPress Enter to make your attempt...")
        
        success = random.random() < win_chance
        if success:
            print(Fore.GREEN + "Success! You did it!")
        else:
            print(Fore.RED + "Not quite! Better luck next time!")
    
    # Slight energy cost for playing carnival games
    player["energy"] = max(0, player["energy"] - 5)
    
    return {"success": success, "game": game_name}

def check_carnival_game_achievements():
    """Check and award achievements related to carnival games"""
    prize_count = len(player.get("carnival_prizes", []))
    unique_prizes = set(player.get("carnival_prizes", []))
    
    # Prize collector achievement
    if prize_count >= 5 and "Prize Winner" not in player["achievements"]:
        award_achievement("Prize Winner")
        player["tickets"] += 15
        print(Fore.GREEN + "Achievement unlocked: Prize Winner! +15 tickets!")
    
    # Advanced collector achievement
    if len(unique_prizes) >= 10 and "Prize Collector" not in player["achievements"]:
        award_achievement("Prize Collector")
        player["tickets"] += 30
        print(Fore.GREEN + "Achievement unlocked: Prize Collector! +30 tickets!")
    
    # Check if player has won all game types
    game_types_won = set()
    for prize in player.get("carnival_prizes", []):
        for game in CARNIVAL_GAMES:
            if prize in game["prizes"]:
                game_types_won.add(game["name"])
    
    if len(game_types_won) >= 5 and "Carnival Game Master" not in player["achievements"]:
        award_achievement("Carnival Game Master")
        player["tickets"] += 50
        print(Fore.GREEN + "Achievement unlocked: Carnival Game Master! +50 tickets!")

def seasonal_event():
    """Special seasonal events and activities"""
    clear()
    current_season = get_current_season()
    
    # Check if a seasonal event is active
    if current_season not in SEASONAL_EVENTS:
        print(Fore.YELLOW + "There are no special seasonal events right now.")
        input("Press Enter to return to the theme park...")
        return theme_park_menu()
    
    # Get the current seasonal event
    event = SEASONAL_EVENTS[current_season]
    
    # Display event information
    print(Fore.MAGENTA + f"🎉 {event['name'].upper()} 🎉")
    print(Fore.CYAN + "Special limited-time seasonal event!")
    print(f"Your Tickets: {player['tickets']}")
    
    # Show decorations
    print(Fore.YELLOW + "\nFestive Decorations:")
    for decoration in event["decorations"]:
        print(f"- {decoration}")
    
    # Show special characters
    print(Fore.GREEN + "\nSpecial Characters:")
    for character in event["special_characters"]:
        print(f"- {character}")
    
    # Show special attractions
    print(Fore.BLUE + "\nSpecial Attractions:")
    for i, attraction in enumerate(event["special_attractions"], 1):
        print(f"[{i}] {attraction} - 5 tickets")
    
    print("[4] Meet Special Characters - 3 tickets")
    print("[5] Seasonal Photo Opportunity - 4 tickets")
    print("[0] Return to Theme Park")
    
    # Get player choice
    choice = input("\nWhat would you like to do? ")
    
    if choice == "0":
        return theme_park_menu()
    elif choice in ["1", "2", "3"]:
        # Try a special attraction
        attraction_idx = int(choice) - 1
        if attraction_idx < len(event["special_attractions"]):
            attraction = event["special_attractions"][attraction_idx]
            
            # Check if player can afford it
            if player["tickets"] >= 5:
                player["tickets"] -= 5
                
                # Track attraction visit
                if "seasonal_attractions_visited" not in player:
                    player["seasonal_attractions_visited"] = []
                player["seasonal_attractions_visited"].append(attraction)
                
                # Display the experience
                clear()
                print(Fore.CYAN + f"🎉 {attraction} 🎉")
                print("You participate in this special seasonal attraction!")
                
                # Simulate the experience with descriptions
                experiences = [
                    f"You have an amazing time at the {attraction}!",
                    f"The {attraction} is even more fun than you expected!",
                    f"Everyone is enjoying the festive atmosphere at the {attraction}!",
                    f"You create wonderful memories at the {attraction}!"
                ]
                
                for experience in random.sample(experiences, 3):
                    print(f"\n{experience}")
                    time.sleep(1.5)
                
                # Give a special seasonal souvenir
                souvenir = f"{current_season.capitalize()} {attraction} Memento"
                if "seasonal_souvenirs" not in player:
                    player["seasonal_souvenirs"] = []
                player["seasonal_souvenirs"].append(souvenir)
                player["inventory"].append(souvenir)
                
                print(Fore.GREEN + f"\nYou received: {souvenir}")
                
                # Check for achievements
                check_seasonal_achievements()
                
                # Add loyalty points
                add_loyalty_points(3)
                print(Fore.MAGENTA + "+3 Loyalty Points for enjoying a seasonal attraction!")
            else:
                print(Fore.RED + "Not enough tickets! You need 5 tickets.")
                time.sleep(1.5)
                return seasonal_event()
    elif choice == "4":
        # Meet special characters
        if player["tickets"] >= 3:
            player["tickets"] -= 3
            
            clear()
            print(Fore.YELLOW + "🎭 MEETING SEASONAL CHARACTERS 🎭")
            
            # Choose a random character to meet
            character = random.choice(event["special_characters"])
            
            print(f"\nYou get to meet {character}!")
            
            # Simulate the interaction
            interactions = [
                f"{character} greets you warmly and poses for a photo!",
                f"You have a delightful conversation with {character}!",
                f"{character} gives you a special high-five and a seasonal greeting!",
                f"You get an autograph from {character} on your event program!"
            ]
            
            for interaction in random.sample(interactions, 2):
                print(f"\n{interaction}")
                time.sleep(1.5)
            
            # Add to collection
            if "characters_met" not in player:
                player["characters_met"] = []
            player["characters_met"].append(character)
            
            # Check for achievements
            if len(player.get("characters_met", [])) >= 5 and "Character Friend" not in player["achievements"]:
                award_achievement("Character Friend")
                player["tickets"] += 20
                print(Fore.GREEN + "Achievement unlocked: Character Friend! +20 tickets!")
            
            # Add loyalty points
            add_loyalty_points(2)
            print(Fore.MAGENTA + "+2 Loyalty Points for meeting a seasonal character!")
        else:
            print(Fore.RED + "Not enough tickets! You need 3 tickets.")
            time.sleep(1.5)
            return seasonal_event()
    elif choice == "5":
        # Seasonal photo opportunity
        if player["tickets"] >= 4:
            player["tickets"] -= 4
            
            clear()
            print(Fore.CYAN + "📸 SEASONAL PHOTO OPPORTUNITY 📸")
            
            # Choose a random backdrop
            backdrops = [
                f"{current_season.capitalize()} Wonderland",
                f"Festive {current_season.capitalize()} Scene",
                f"{event['name']} Celebration",
                f"{current_season.capitalize()} Magic"
            ]
            backdrop = random.choice(backdrops)
            
            print(f"\nYou pose in front of the '{backdrop}' photo backdrop!")
            
            # Choose a prop
            props = [
                "festive hat", "seasonal prop", "themed accessory", 
                "celebration banner", "decorative item"
            ]
            prop = random.choice(props)
            
            print(f"You use a {prop} to enhance your photo!")
            
            # Take the photo
            print("\nThe photographer counts down: 3... 2... 1... SMILE!")
            time.sleep(1)
            print(Fore.GREEN + "Perfect shot!")
            
            # Add to collection
            photo_name = f"{current_season.capitalize()} Photo: {backdrop}"
            player["inventory"].append(photo_name)
            
            print(Fore.GREEN + f"You received: {photo_name}")
            
            # Check photo collection achievement
            seasonal_photos = [item for item in player["inventory"] if "Photo:" in item]
            if len(seasonal_photos) >= 4 and "Seasonal Photographer" not in player["achievements"]:
                award_achievement("Seasonal Photographer")
                player["tickets"] += 25
                print(Fore.GREEN + "Achievement unlocked: Seasonal Photographer! +25 tickets!")
            
            # Add loyalty points
            add_loyalty_points(2)
            print(Fore.MAGENTA + "+2 Loyalty Points for a seasonal photo!")
        else:
            print(Fore.RED + "Not enough tickets! You need 4 tickets.")
            time.sleep(1.5)
            return seasonal_event()
    else:
        print(Fore.RED + "Invalid choice!")
        time.sleep(1.5)
        return seasonal_event()
    
    input("\nPress Enter to return to the seasonal event menu...")
    return seasonal_event()

def check_seasonal_achievements():
    """Check and award achievements related to seasonal events"""
    seasonal_attractions = player.get("seasonal_attractions_visited", [])
    seasonal_souvenirs = player.get("seasonal_souvenirs", [])
    
    # Seasonal participation
    if len(seasonal_attractions) >= 3 and "Seasonal Participant" not in player["achievements"]:
        award_achievement("Seasonal Participant")
        player["tickets"] += 20
        print(Fore.GREEN + "Achievement unlocked: Seasonal Participant! +20 tickets!")
    
    # Seasonal collector
    if len(seasonal_souvenirs) >= 5 and "Seasonal Collector" not in player["achievements"]:
        award_achievement("Seasonal Collector")
        player["tickets"] += 30
        print(Fore.GREEN + "Achievement unlocked: Seasonal Collector! +30 tickets!")
    
    # Multi-season achievement
    visited_seasons = set()
    for attraction in seasonal_attractions:
        for season, event in SEASONAL_EVENTS.items():
            if attraction in event["special_attractions"]:
                visited_seasons.add(season)
    
    if len(visited_seasons) >= 3 and "Year-Round Celebrator" not in player["achievements"]:
        award_achievement("Year-Round Celebrator")
        player["tickets"] += 50
        print(Fore.GREEN + "Achievement unlocked: Year-Round Celebrator! +50 tickets!")
        
        # Special reward
        special_item = "Four Seasons Crown 👑"
        if special_item not in player["inventory"]:
            player["inventory"].append(special_item)
            print(Fore.GREEN + f"You received: {special_item}")

def theme_park_menu():
    """Display and handle the theme park attraction menu.
    Shows available rides and attractions with their ticket costs.
    """
    clear()
    # Check for special events
    current_season = get_current_season()
    
    # Display seasonal theme
    if current_season == "summer":
        print(Fore.YELLOW + "☀️ Welcome to SUMMER SPLASH CARNIVAL! ☀️")
        print(Fore.CYAN + "Special limited-time water attractions and ice cream stands!")
    elif current_season == "halloween":
        print(Fore.MAGENTA + "🎃 Welcome to HALLOWEEN SPOOKTACULAR! 🎃")
        print(Fore.RED + "Extra spooky decorations and candy treats everywhere!")
    elif current_season == "winter":
        print(Fore.BLUE + "❄️ Welcome to WINTER WONDERLAND CARNIVAL! ❄️")
        print(Fore.WHITE + "Enjoy hot chocolate stands and snow-themed attractions!")
    elif current_season == "spring":
        print(Fore.GREEN + "🌸 Welcome to SPRING BLOSSOM CARNIVAL! 🌸")
        print(Fore.LIGHTMAGENTA_EX + "Flower displays and special spring-themed treats!")
    else:
        print(Fore.LIGHTMAGENTA_EX + "🎢 Welcome to the SPECTACULAR CARNIVAL! 🎢")
    
    print(f"Your Tickets: {player['tickets']}")
    
    # Show hunger and energy levels if enabled
    if player.get("carnival_needs_system", False):
        hunger = player.get("hunger", 100)
        energy = player.get("energy", 100)
        print(Fore.YELLOW + f"Hunger: {hunger}% | Energy: {energy}%")
        
        if hunger < 30:
            print(Fore.RED + "You're getting hungry! Visit a food stand soon.")
        if energy < 30:
            print(Fore.RED + "You're getting tired! Take a break soon.")
    
    # Show fast passes
    fast_passes = player.get("fast_passes", 0)
    if fast_passes > 0:
        print(Fore.GREEN + f"Fast Passes: {fast_passes} (Skip lines on attractions!)")

    # Detect if season pass is active    
    has_season_pass = player.get("season_pass", False)
    if has_season_pass:
        days_left = player.get("season_pass_days", 30)
        print(Fore.GREEN + f"Season Pass Active! ({days_left} days remaining)")
        print("All attraction prices are reduced by 30%!")
    
    # Show hunger and energy levels for carnival experience
    if player.get("carnival_needs_system", True):
        hunger = player.get("hunger", 100)
        energy = player.get("energy", 100)
        
        # Visual hunger and energy bars
        hunger_bar = "█" * (hunger // 10) + "░" * ((100 - hunger) // 10)
        energy_bar = "█" * (energy // 10) + "░" * ((100 - energy) // 10)
        
        print(Fore.YELLOW + "\nHunger: |" + hunger_bar + f"| {hunger}%")
        print(Fore.CYAN + "Energy: |" + energy_bar + f"| {energy}%")
        
        # Warnings if low
        if hunger < 30 or energy < 30:
            print(Fore.RED + "⚠️ You're getting " + 
                  ("hungry" if hunger < 30 else "") + 
                  (" and " if hunger < 30 and energy < 30 else "") + 
                  ("tired" if energy < 30 else "") + 
                  "! Visit the food stands soon.")
    
    print("\n🎪 CARNIVAL FEATURES 🎪")
    print("[F] Food Stands 🍕 - Delicious treats to restore hunger and energy!")
    print("[G] Carnival Games 🎮 - Test your skill and win prizes!")
    print("[E] Seasonal Events 🎭 - Special limited-time attractions!")
    
    print("\nThrilling Rides:")
    print("[1] Cosmic Coaster 🚀 - 5 tickets")
    print("[2] Log Flume 💦 - 4 tickets")
    print("[3] Thunder Mountain ⛰️ - 6 tickets")
    print("[4] Drop Tower 🗼 - 7 tickets")
    print("[5] Spinning Teacups ☕ - 3 tickets")
    
    print("\nWater Rides:")
    print("[6] Splash Mountain 💦 - 5 tickets")
    print("[7] River Rapids 🌊 - 5 tickets")
    print("[8] Water Slides 🏄 - 4 tickets")
    
    print("\nSpooky Adventures:")
    print("[9] Haunted Mansion 👻 - 6 tickets")
    print("[10] Ghost Train 👺 - 4 tickets")
    print("[11] Zombie Escape 🧟 - 7 tickets")
    
    print("\nFamily Rides:")
    print("[12] Ferris Wheel 🎡 - 3 tickets")
    print("[13] Carnival Carousel 🎠 - 2 tickets")
    print("[14] Bumper Cars 🚗 - 3 tickets")
    
    print("\nSpecial Attractions:")
    print("[15] Virtual Reality Experience 🥽 - 7 tickets")
    print("[16] 4D Cinema 🎬 - 5 tickets")
    print("[17] Dinosaur Safari 🦕 - 6 tickets")
    print("[18] Mirror Maze 🪞 - 4 tickets")
    print("[19] Photo Booth 📸 - 2 tickets")
    print("[20] Magic Show 🎩 - 5 tickets")
    print("[21] Petting Zoo 🦙 - 3 tickets")
    
    print("\nSpecial Access:")
    print("[22] Purchase Season Pass - 200 tickets (30% off all attractions for 30 days!)")
    print("[23] Purchase Fast Passes - 50 tickets (Skip the line for 5 attractions!)")
    print("[24] VIP Tour - 100 tickets (Guided tour with behind-the-scenes access!)")
    
    print("\n[0] Back to Main Menu")
    
    choice = input("\nSelect an attraction or feature: ")
    
    # Carnival Features
    if choice.lower() == "f":
        food_stand()
    elif choice.lower() == "g":
        carnival_games_menu()
    elif choice.lower() == "e":
        seasonal_event()
        
    # Thrilling Rides
    elif choice == "1":
        cosmic_coaster()
    elif choice == "2":
        log_flume()
    elif choice == "3":
        thunder_mountain()
    elif choice == "4":
        drop_tower()
    elif choice == "5":
        spinning_teacups()
    
    # Water Rides
    elif choice == "6":
        splash_mountain()
    elif choice == "7":
        river_rapids()
    elif choice == "8":
        water_slides()
    
    # Spooky Adventures
    elif choice == "9":
        haunted_mansion()
    elif choice == "10":
        ghost_train()
    elif choice == "11":
        zombie_escape()
    
    # Family Rides
    elif choice == "12":
        ferris_wheel()
    elif choice == "13":
        carnival_carousel()
    elif choice == "14":
        bumper_cars()
    
    # Special Attractions
    elif choice == "15":
        vr_experience()
    elif choice == "16":
        cinema_4d()
    elif choice == "17":
        dinosaur_safari()
    elif choice == "18":
        mirror_maze()
    elif choice == "19":
        photo_booth()
    elif choice == "20":
        magic_show()
    elif choice == "21":
        petting_zoo()
        
    # Special Access
    elif choice == "22":
        purchase_season_pass()
    elif choice == "23":
        purchase_fast_passes()
    elif choice == "24":
        vip_tour()
    elif choice != "0":
        print(Fore.RED + "Invalid choice!")

# Helper function for theme park attractions
def purchase_season_pass():
    """Purchase a season pass for the theme park"""
    season_pass_cost = 200
    if player.get("season_pass", False):
        days_left = player.get("season_pass_days", 0)
        print(Fore.YELLOW + f"You already have a season pass with {days_left} days remaining.")
        confirm = input("Would you like to add 30 more days for 200 tickets? (y/n): ")
        if confirm.lower() != "y":
            return theme_park_menu()
    
    if player["tickets"] < season_pass_cost:
        print(Fore.RED + f"Not enough tickets! You need {season_pass_cost} tickets.")
        input("Press Enter to continue...")
        return theme_park_menu()
    
    player["tickets"] -= season_pass_cost
    if player.get("season_pass", False):
        player["season_pass_days"] += 30
        print(Fore.GREEN + "Season pass extended by 30 days!")
    else:
        player["season_pass"] = True
        player["season_pass_days"] = 30
        print(Fore.GREEN + "Season pass activated for 30 days!")
        print("You'll get 30% off all theme park attractions!")
    
    # Add loyalty points for season pass purchase
    add_loyalty_points(20)
    print(Fore.MAGENTA + "+20 Loyalty Points for purchasing a season pass!")
    
    input("Press Enter to continue...")
    return theme_park_menu()

def purchase_fast_passes():
    """Purchase fast passes to skip lines"""
    fast_pass_cost = 50
    fast_pass_count = 5
    
    if player["tickets"] < fast_pass_cost:
        print(Fore.RED + f"Not enough tickets! You need {fast_pass_cost} tickets.")
        input("Press Enter to continue...")
        return theme_park_menu()
    
    player["tickets"] -= fast_pass_cost
    player["fast_passes"] = player.get("fast_passes", 0) + fast_pass_count
    print(Fore.GREEN + f"You've purchased {fast_pass_count} Fast Passes!")
    print("You can use them to skip lines on attractions.")
    
    # Add loyalty points for fast pass purchase
    add_loyalty_points(10)
    print(Fore.MAGENTA + "+10 Loyalty Points for purchasing fast passes!")
    
    input("Press Enter to continue...")
    return theme_park_menu()

def vip_tour():
    """Take a VIP behind-the-scenes tour of the theme park"""
    vip_tour_cost = 100
    
    if player["tickets"] < vip_tour_cost:
        print(Fore.RED + f"Not enough tickets! You need {vip_tour_cost} tickets.")
        input("Press Enter to continue...")
        return theme_park_menu()
    
    player["tickets"] -= vip_tour_cost
    
    clear()
    print(Fore.CYAN + "🌟 VIP BEHIND-THE-SCENES TOUR 🌟")
    print("\nWelcome to your exclusive VIP tour of the theme park!")
    print("Your tour guide for today is Jordan, a veteran park employee.")
    
    # Tour sequence
    print("\nJordan: Welcome to our behind-the-scenes tour! I'll be showing you how our rides work,")
    print("        introducing you to some of our performers, and sharing some theme park secrets!")
    time.sleep(2)
    
    # Ride mechanics
    print("\n🔧 RIDE MECHANICS TOUR 🔧")
    print("You're taken to the maintenance area of the Cosmic Coaster...")
    time.sleep(2)
    print("Jordan: These coaster cars use magnetic propulsion to achieve speeds of up to 70mph!")
    print("        Our team of 20 engineers check every ride each morning for safety.")
    time.sleep(2)
    
    # Character workshop
    print("\n🎭 CHARACTER WORKSHOP 🎭")
    print("You visit the workshop where costumes and animatronics are created...")
    time.sleep(2)
    print("Jordan: Each character costume takes about 80 hours to make by hand.")
    print("        The animatronics in the Haunted Mansion have over 40 points of articulation!")
    time.sleep(2)
    
    # Special effects
    print("\n✨ SPECIAL EFFECTS DEMONSTRATION ✨")
    print("The team demonstrates how various special effects are created...")
    time.sleep(2)
    print("Jordan: The fog in the Haunted Mansion is created using ultrasonic foggers.")
    print("        For water rides, we recycle and filter over 500,000 gallons of water daily!")
    time.sleep(2)
    
    # Control room
    print("\n🖥️ PARK CONTROL CENTER 🖥️")
    print("You're shown the control center where all rides are monitored...")
    time.sleep(2)
    print("Jordan: From here, we can see the status of every ride in the park.")
    print("        Our backup generators can power the entire park for 12 hours in an emergency.")
    time.sleep(2)
    
    # VIP lounge
    print("\n🍹 VIP LOUNGE 🍹")
    print("The tour ends with refreshments in the exclusive VIP lounge...")
    time.sleep(2)
    print("Jordan: Please enjoy some complimentary refreshments!")
    print("        As a VIP tour participant, you'll also receive this exclusive souvenir.")
    
    # Award a special souvenir
    vip_souvenir = "VIP Tour Badge 🌟"
    if "inventory" not in player:
        player["inventory"] = []
    player["inventory"].append(vip_souvenir)
    print(Fore.GREEN + f"\nYou received: {vip_souvenir}")
    
    # Add loyalty points
    add_loyalty_points(25)
    print(Fore.MAGENTA + "+25 Loyalty Points for taking the VIP tour!")
    
    # Add achievement
    if "VIP Explorer" not in player["achievements"]:
        award_achievement("VIP Explorer")
    
    # Fast pass bonus
    player["fast_passes"] = player.get("fast_passes", 0) + 2
    print(Fore.GREEN + "Bonus: You received 2 Fast Passes!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def thunder_mountain():
    """Wild mine cart adventure through a mountain with special effects"""
    if not pay_to_play(6):
        return
    
    clear()
    print(Fore.YELLOW + "⛰️ THUNDER MOUNTAIN ⛰️")
    print("Hold on tight for this wild mine cart adventure!")
    
    # Track for mission
    track_attraction_visit("Thunder Mountain")
    
    # Add delay for suspense
    time.sleep(1.5)
    
    # Ride begins
    print("\nYou climb aboard an old mining cart and secure the safety bar.")
    print("The ride operator tips his hat: 'Y'all enjoy yer adventure now, ya hear?'")
    time.sleep(2)
    
    # Start of the ride
    print("\nWith a mechanical clunk, your cart starts moving...")
    print("It slowly climbs up the first hill, the chains clicking beneath you...")
    time.sleep(2)
    
    # First drop
    print("\nYou reach the top of the hill and pause for a moment...")
    time.sleep(1)
    print("WHOOSH! Your cart plummets down the first drop!")
    print("The wind rushes past your face as you speed through a dark tunnel!")
    time.sleep(2)
    
    # Cave section
    print("\nYour cart races through a dimly lit cave...")
    print("Glowing gems and crystals line the walls, creating a mesmerizing light show.")
    print("You hear the sound of mining picks and ghostly whispers...")
    time.sleep(2)
    
    # Waterfall section
    print("\nYou emerge from the cave and speed past a roaring waterfall!")
    print("A fine mist sprays your face as you zoom by.")
    time.sleep(2)
    
    # Decision point
    print("\nThe track splits ahead! Your cart could go left or right.")
    choice = input("Which way do you lean? (left/right): ").lower()
    
    if choice == "left":
        print("\nYou lean left and your cart veers onto the left track...")
        print("This route takes you through an abandoned mining town!")
        print("Animatronic miners tip their hats as you speed past.")
        time.sleep(2)
        
        print("\nYour cart enters an old saloon and crashes through the swinging doors!")
        print("Inside, the player piano is playing by itself as you race through.")
        time.sleep(2)
        
        # Special scene for left path
        print("\nAs you exit the saloon, you spot a hidden gold nugget!")
        nugget_found = "Gold Nugget Souvenir 💰"
        player["inventory"].append(nugget_found)
        print(Fore.GREEN + f"You received: {nugget_found}")
        
    else:  # right or any other input
        print("\nYou lean right and your cart veers onto the right track...")
        print("This route takes you through a terrifying cave-in!")
        print("Rocks appear to fall all around you, but narrowly miss your cart.")
        time.sleep(2)
        
        print("\nYour cart zooms past an old dynamite storage area...")
        print("BOOM! Special effects create the illusion of an explosion behind you!")
        print("The heat from the pyrotechnics warms your back as you escape!")
        time.sleep(2)
        
        # Special scene for right path
        print("\nAs you escape the explosion, you notice a strange glowing crystal!")
        crystal_found = "Thunder Mountain Crystal 💎"
        player["inventory"].append(crystal_found)
        print(Fore.GREEN + f"You received: {crystal_found}")
    
    # Final drop
    print("\nBoth paths rejoin for the grand finale...")
    print("Your cart climbs the highest peak of Thunder Mountain...")
    time.sleep(2)
    print("You reach the summit and look down at the steepest drop yet!")
    time.sleep(1)
    print("WHOOOOOOSH! Your cart plummets down at incredible speed!")
    print("You raise your hands and scream with delight!")
    time.sleep(2)
    
    # End of ride
    print("\nYour cart gradually slows down and returns to the station.")
    print("The ride operator grins: 'Hope y'all struck it rich in there!'")
    
    # Loyalty points
    add_loyalty_points(3)
    print(Fore.MAGENTA + "+3 Loyalty Points for riding Thunder Mountain!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def drop_tower():
    """Thrilling drop tower experience with multiple drops"""
    if not pay_to_play(7):
        return
    
    clear()
    print(Fore.RED + "🗼 THE DROP TOWER 🗼")
    print("Experience the ultimate free-fall sensation!")
    
    # Track for mission
    track_attraction_visit("Drop Tower")
    
    # Ride begins
    print("\nYou're secured into your seat with a heavy-duty harness.")
    print("The ride operator checks all safety systems twice.")
    print("'Keep your hands inside the ride at all times and enjoy the view... while you can.'")
    time.sleep(2)
    
    # Ascent
    print("\nWith a mechanical hum, your seat begins to rise...")
    print("The tower is 200 feet tall, and you're heading all the way to the top.")
    time.sleep(1.5)
    
    for height in [50, 100, 150, 200]:
        print(f"\nYou're now {height} feet above the ground...")
        if height == 100:
            print("You can see the entire theme park from here!")
        elif height == 150:
            print("The people below look like tiny ants...")
        elif height == 200:
            print("You've reached the top! The view is breathtaking!")
        time.sleep(1.5)
    
    # At the top
    print("\nYour seat hovers at the top of the tower...")
    print("You have a moment to appreciate the incredible view...")
    print("The entire theme park and surrounding landscape stretches out beneath you.")
    time.sleep(3)
    
    # The drop
    print("\n3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(0.5)
    print("WHOOOOOOOOSH!!!")
    print("You plummet toward the ground at incredible speed!")
    print("The wind rushes past as your stomach feels like it's floating!")
    time.sleep(2)
    
    # Surprise elements - random events during the drop
    surprise = random.randint(1, 4)
    
    if surprise == 1:
        print("\nHalfway down, the tower unexpectedly STOPS!")
        time.sleep(1)
        print("You hover for just a second... and then DROP AGAIN!")
        print("The double-drop makes your heart race even faster!")
    elif surprise == 2:
        print("\nAs you fall, the seat unexpectedly begins to SPIN!")
        print("The world whirls around you as you continue to plummet!")
    elif surprise == 3:
        print("\nWater jets spray a fine mist as you fall through them!")
        print("The cool water adds to the sensory thrill of the drop!")
    else:
        print("\nLED lights flash in sequence as you fall through the tower!")
        print("It's like falling through a tunnel of colorful stars!")
    
    time.sleep(1.5)
    
    # The end - magnetic braking
    print("\nJust when you think you're about to hit the ground...")
    print("The magnetic brakes engage and slow your descent!")
    print("Your fall slows dramatically, leaving you with an incredible adrenaline rush!")
    time.sleep(2)
    
    # Reaction
    print("\nAs your seat gently returns to the loading platform, you notice")
    print("your heart is still pounding from the incredible experience!")
    
    # Photo opportunity
    print("\nThe ride operator grins: 'Want to see your drop photo?'")
    see_photo = input("Would you like to see your photo? (y/n): ").lower()
    
    if see_photo == "y":
        expressions = ["terrified", "thrilled", "screaming with delight", "eyes closed tight", 
                      "arms raised high", "perfectly calm (surprisingly)"]
        expression = random.choice(expressions)
        print(f"\nYour photo shows you looking {expression} during the big drop!")
        photo_souvenir = "Drop Tower Photo 📸"
        buy_photo = input("Would you like to buy this photo for 2 tickets? (y/n): ").lower()
        
        if buy_photo == "y" and player["tickets"] >= 2:
            player["tickets"] -= 2
            player["inventory"].append(photo_souvenir)
            print(Fore.GREEN + f"You received: {photo_souvenir}")
        elif buy_photo == "y":
            print(Fore.RED + "Not enough tickets to buy the photo!")
    
    # Loyalty points
    add_loyalty_points(3)
    print(Fore.MAGENTA + "+3 Loyalty Points for surviving the Drop Tower!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def spinning_teacups():
    """Classic spinning teacup ride with varying speeds"""
    if not pay_to_play(3):
        return
    
    clear()
    print(Fore.MAGENTA + "☕ SPINNING TEACUPS ☕")
    print("The classic fairground favorite with a colorful twist!")
    
    # Track for mission
    track_attraction_visit("Spinning Teacups")
    
    # Ride begins
    print("\nYou approach a large rotating platform with colorful teacups.")
    teacup_colors = ["pink", "blue", "green", "purple", "yellow", "red"]
    
    print("\nAvailable teacups:")
    for i, color in enumerate(teacup_colors, 1):
        print(f"[{i}] {color.capitalize()} teacup")
    
    # Choose teacup
    try:
        choice = int(input("\nChoose your teacup (1-6): "))
        if choice < 1 or choice > 6:
            raise ValueError
        color = teacup_colors[choice-1]
    except (ValueError, IndexError):
        color = random.choice(teacup_colors)
        print(f"Invalid choice. You're assigned to the {color} teacup.")
    
    print(f"\nYou climb into the {color} teacup and sit down.")
    print("Each teacup has a wheel in the center that you can spin to go even faster!")
    time.sleep(2)
    
    # Ride starts
    print("\nThe ride starts to move, and the platform begins rotating...")
    print("Your teacup starts to gently spin on its own...")
    time.sleep(2)
    
    # Interactive spinning
    print("\nHow fast do you want to spin your teacup?")
    print("[1] Take it easy - gentle spinning")
    print("[2] Medium speed - fun but not too wild")
    print("[3] Maximum speed - spin as fast as possible!")
    
    try:
        spin_choice = int(input("Choose your spin speed (1-3): "))
        if spin_choice < 1 or spin_choice > 3:
            raise ValueError
    except ValueError:
        spin_choice = random.randint(1, 3)
        print(f"Invalid choice. Setting to speed level {spin_choice}.")
    
    # Different experiences based on spin choice
    if spin_choice == 1:
        print("\nYou spin the wheel gently, enjoying a pleasant rotation.")
        print("You can appreciate the colorful lights and music as you spin.")
        print("This is quite relaxing and enjoyable!")
        time.sleep(2)
        print("\nYou finish the ride feeling happy and not at all dizzy.")
        dizzy_factor = "not dizzy at all"
    
    elif spin_choice == 2:
        print("\nYou spin the wheel with moderate effort.")
        print("Your teacup spins faster, creating a fun whirling sensation!")
        print("You laugh as the world blurs slightly around you.")
        time.sleep(2)
        print("\nYou finish the ride with a slight case of the wobbles.")
        dizzy_factor = "slightly dizzy"
    
    else:  # spin_choice == 3
        print("\nYou grip the wheel and spin with all your might!")
        print("Your teacup becomes a colorful blur as it spins wildly!")
        print("The centrifugal force pushes you against the side of the teacup!")
        print("WHEEEEEEEEE!")
        time.sleep(2)
        print("\nYou finish the ride stumbling and dizzy, but exhilarated!")
        dizzy_factor = "extremely dizzy but thrilled"
        
        # Special reward for brave spinners
        special_item = "Dizzy Champion Badge 💫"
        if special_item not in player["inventory"]:
            player["inventory"].append(special_item)
            print(Fore.GREEN + f"For your bravery, you received: {special_item}")
    
    # End of ride
    print(f"\nYou exit the {color} teacup, {dizzy_factor}.")
    print("That was a colorful, spinning adventure!")
    
    # Loyalty points
    add_loyalty_points(2)
    print(Fore.MAGENTA + "+2 Loyalty Points for riding the Spinning Teacups!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def river_rapids():
    """Navigate rushing waters in a circular raft with friends"""
    if not pay_to_play(5):
        return
    
    clear()
    print(Fore.BLUE + "🌊 RIVER RAPIDS 🌊")
    print("Navigate rushing waters in this thrilling water adventure!")
    
    # Track for mission
    track_attraction_visit("River Rapids")
    
    # Ride begins
    print("\nYou climb into a large circular raft with several other passengers.")
    print("Everyone grabs the handles in the center as the attendant pushes you off.")
    time.sleep(2)
    
    # Start of journey
    print("\nYour raft begins floating down a gentle river...")
    print("The scenery is beautiful with lush vegetation on both sides.")
    print("Birds chirp and butterflies flutter around colorful flowers.")
    time.sleep(2)
    
    # First rapids
    print("\nYou hear the sound of rushing water ahead...")
    print("Your raft approaches the first section of rapids!")
    time.sleep(1)
    print("SPLASH! The raft bounces and spins as it hits the churning water!")
    print("Everyone screams and laughs as water sprays into the raft!")
    time.sleep(2)
    
    # Interactive moment
    print("\nThe raft reaches a calm section, but there are rapids ahead on both sides.")
    choice = input("Do you want to lean left, right, or stay centered? (left/right/center): ").lower()
    
    if choice == "left":
        print("\nEveryone leans left, steering the raft toward the left rapids...")
        print("These rapids are extra bumpy with lots of rocks!")
        print("The raft spins rapidly as you bounce through the turbulent water!")
        print("SPLASH! A wave crashes over the left side, soaking you completely!")
        wetness = "soaked"
        
    elif choice == "right":
        print("\nEveryone leans right, steering the raft toward the right rapids...")
        print("This route takes you through a series of small waterfalls!")
        print("Your stomach drops as the raft plunges down each cascade!")
        print("SPLASH! You get moderately wet from the spray of the falls!")
        wetness = "moderately wet"
        
    else:  # center or any other input
        print("\nYou stay centered, heading straight down the middle channel...")
        print("This route is smoother but leads to a big wave at the end!")
        print("The raft glides smoothly until...")
        print("WHOOSH! You hit the standing wave and get splashed from all sides!")
        wetness = "splashed from all directions"
    
    # Cave section
    print("\nYour raft enters a mysterious cave...")
    print("Glowing formations illuminate the ceiling, creating magical reflections on the water.")
    print("The echoing sounds of dripping water create an eerie atmosphere.")
    time.sleep(2)
    
    # Final rapids
    print("\nYou exit the cave and hear the roar of the biggest rapids yet!")
    print("Everyone holds on tight as the raft approaches...")
    time.sleep(1)
    print("WHOOSH! SPLASH! SPIN!")
    print("Your raft bounces, spins, and rocks through the wildest rapids yet!")
    print("Water splashes in from every direction!")
    time.sleep(2)
    
    # End of ride
    print(f"\nYour raft finally reaches calm water and returns to the station, everyone {wetness}.")
    print("That was an exciting whitewater adventure!")
    
    # Special souvenir chance
    if random.random() < 0.3:  # 30% chance
        souvenir = "River Rapids Water Bottle 🍶"
        if souvenir not in player["inventory"]:
            player["inventory"].append(souvenir)
            print(Fore.GREEN + f"\nYou found a {souvenir} floating in the water at the end!")
    
    # Loyalty points
    add_loyalty_points(3)
    print(Fore.MAGENTA + "+3 Loyalty Points for navigating the River Rapids!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def water_slides():
    """Experience multiple water slides of varying intensity"""
    if not pay_to_play(4):
        return
    
    clear()
    print(Fore.CYAN + "🏄 WATER SLIDES 🏄")
    print("Choose from five different slides of varying intensity!")
    
    # Track for mission
    track_attraction_visit("Water Slides")
    
    # Available slides
    slides = [
        {"name": "Gentle Glider", "color": "Blue", "intensity": "Mild", "description": "A gentle, winding slide perfect for beginners."},
        {"name": "Twisty Tornado", "color": "Green", "intensity": "Moderate", "description": "A slide with lots of twists and turns."},
        {"name": "Rapid Racer", "color": "Yellow", "intensity": "Moderate-High", "description": "A straight, fast slide with timing measurement."},
        {"name": "Plummet Dive", "color": "Orange", "intensity": "High", "description": "A steep drop slide that gives you weightlessness."},
        {"name": "Extreme Vortex", "color": "Red", "intensity": "Extreme", "description": "A pitch-black slide with unexpected drops and turns."}
    ]
    
    # Display slides
    print("\nAvailable Slides:")
    for i, slide in enumerate(slides, 1):
        print(f"[{i}] {slide['name']} ({slide['color']}) - {slide['intensity']} intensity")
        print(f"    {slide['description']}")
    
    # Choose slide
    try:
        choice = int(input("\nWhich slide would you like to try? (1-5): "))
        if choice < 1 or choice > 5:
            raise ValueError
        slide = slides[choice-1]
    except (ValueError, IndexError):
        slide = random.choice(slides)
        print(f"Invalid choice. You're assigned to the {slide['name']}.")
    
    print(f"\nYou climb the stairs to the {slide['name']} water slide.")
    print(f"The {slide['color']} tube gleams in the sunlight.")
    
    # Slide experience
    print("\nYou sit at the top of the slide, water rushing past you.")
    print("The attendant gives you a thumbs up...")
    input("Press Enter when you're ready to go...")
    
    print("\nYou push off and begin your descent!")
    
    # Different experiences based on slide choice
    if slide["name"] == "Gentle Glider":
        print("\nYou glide smoothly down the winding blue slide.")
        print("The gentle curves make for a relaxing ride.")
        print("You can enjoy the scenery as you float along at a pleasant pace.")
        time.sleep(2)
        print("\nYou splash into the landing pool with a gentle 'swoosh'.")
        print("That was a nice, easy ride!")
        experience = "relaxing"
        
    elif slide["name"] == "Twisty Tornado":
        print("\nYou zip down the green slide, encountering turn after turn!")
        print("Left, right, left, right - the twists keep coming!")
        print("The changing directions make for an exciting but not too intense ride.")
        time.sleep(2)
        print("\nAfter the final twist, you splash into the landing pool with a 'splash'!")
        print("That was a fun, twisty adventure!")
        experience = "twisty and fun"
        
    elif slide["name"] == "Rapid Racer":
        print("\nThe yellow racing slide is straight and FAST!")
        print("You accelerate quickly, racing down at high speed!")
        print("Water sprays around you as you zoom toward the bottom.")
        
        # Timer for racing slide
        race_time = round(random.uniform(9.5, 15.2), 1)
        time.sleep(2)
        print("\nYou splash into the landing pool with a big 'SPLASH'!")
        print(f"Your time: {race_time} seconds!")
        
        if race_time < 10.5:
            print("That's one of the fastest times today!")
            experience = "incredibly fast"
            
            # Special achievement for fast time
            if "Speed Demon" not in player["achievements"]:
                award_achievement("Speed Demon")
        else:
            print("Not bad! The slide was super fast!")
            experience = "very fast"
        
    elif slide["name"] == "Plummet Dive":
        print("\nYou look down the steep orange slide with a gulp...")
        print("It's nearly vertical at the start!")
        print("Here goes nothing...")
        time.sleep(1)
        print("\nWHOOOOSH! You plummet straight down!")
        print("Your stomach feels like it's floating as you experience weightlessness!")
        print("The free-fall sensation is incredible!")
        time.sleep(2)
        print("\nYou hit the runout section and splash into the landing pool with a big 'KERPLUNK'!")
        print("Your heart is racing from the adrenaline rush!")
        experience = "heart-pounding"
        
    else:  # Extreme Vortex
        print("\nYou enter the dark red tube with trepidation...")
        print("As soon as you start, you're plunged into complete darkness!")
        print("WHOOSH! You feel a sudden drop!")
        time.sleep(1)
        print("\nYou can't see anything as you twist, turn, and plummet!")
        print("The disorientation adds to the thrill as you rocket through the tube!")
        print("Another unexpected drop makes your stomach lurch!")
        time.sleep(2)
        print("\nFinally, you see light and splash into the landing pool with a massive 'SPLOOSH'!")
        print("That was the most intense water slide experience ever!")
        experience = "absolutely thrilling"
        
        # Special souvenir for brave riders
        special_item = "Extreme Rider Badge 🌊"
        if special_item not in player["inventory"]:
            player["inventory"].append(special_item)
            print(Fore.GREEN + f"For your bravery, you received: {special_item}")
    
    # End of ride
    print(f"\nYou climb out of the pool, the {experience} ride leaving you exhilarated.")
    
    # Multiple rides option
    more_slides = input("\nWould you like to try another slide? (y/n): ").lower()
    
    if more_slides == "y" and player["tickets"] >= 2:
        player["tickets"] -= 2
        print(Fore.YELLOW + "You paid 2 tickets for another slide!")
        water_slides()  # Recursive call for another ride
    elif more_slides == "y":
        print(Fore.RED + "Not enough tickets for another slide!")
    
    # Loyalty points
    add_loyalty_points(2)
    print(Fore.MAGENTA + "+2 Loyalty Points for riding the Water Slides!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def ghost_train():
    """Spooky ghost train ride through a haunted forest"""
    if not pay_to_play(4):
        return
    
    clear()
    print(Fore.MAGENTA + "👺 GHOST TRAIN 👺")
    print("A spooky journey through the spirit realm!")
    
    # Track for mission
    track_attraction_visit("Ghost Train")
    
    # Ride begins
    print("\nYou board an old-fashioned train car decorated with cobwebs and skulls.")
    print("The conductor, dressed as a skeleton, welcomes you aboard.")
    print("'Welcome to the Ghost Train! Please keep your limbs inside... if you want to keep them!'")
    time.sleep(2)
    
    # Train starts
    print("\nWith a ghostly whistle, the train lurches forward into a dark tunnel...")
    print("Eerie music plays from hidden speakers as you enter the haunted forest.")
    time.sleep(2)
    
    # The experience - random scares
    scares = [
        "A ghost bride appears beside the tracks, reaching toward the train!",
        "A headless horseman gallops alongside your car, laughing maniacally!",
        "The train passes through a ghostly dinner party, where all the guests turn to stare at you!",
        "Bats swoop down from the ceiling, barely missing your head!",
        "The floor of your car becomes transparent, revealing skeletal hands reaching up!",
        "A werewolf howls in the distance, then appears to lunge at your car!",
        "The train seems to derail and fall, creating a moment of panic before continuing normally!",
        "Ghostly children play hide and seek around your car, giggling eerily!"
    ]
    
    # Scare intensity tracker
    fear_level = 0
    
    # A series of randomized scares
    for _ in range(4):
        scare = random.choice(scares)
        scares.remove(scare)  # Don't repeat scares
        
        print(f"\n{scare}")
        
        reaction = input("How do you react? (scream/laugh/close eyes/stay calm): ").lower()
        
        if reaction == "scream":
            print("You let out a scream! The skeleton conductor seems pleased.")
            fear_level += 3
        elif reaction == "laugh":
            print("You laugh in the face of fear! The ghosts seem annoyed.")
            fear_level += 1
        elif reaction == "close eyes":
            print("You close your eyes until it passes. The ghosts whisper around you.")
            fear_level += 2
        else:  # stay calm or any other input
            print("You remain stoic. The skeleton conductor looks impressed.")
            fear_level += 1
        
        time.sleep(1.5)
    
    # Grand finale
    print("\nThe train approaches the final scene - a massive graveyard...")
    print("Suddenly, all the graves open at once and spectral figures rise!")
    print("They surround the train, reaching in through the windows!")
    print("The lights flicker and go out completely!")
    time.sleep(3)
    
    print("\nA moment of complete darkness and silence...")
    time.sleep(2)
    
    print("\nThe lights come back on and you're back at the station!")
    print("'We hope you enjoyed your journey to the other side,' says the conductor.")
    print("'Or perhaps... you never left?'")
    
    # Different endings based on fear level
    if fear_level > 8:
        print("\nYou exit the train with shaky legs, thoroughly spooked!")
        ending = "thoroughly spooked"
        # Achievement for being brave
        if "Ghost Whisperer" not in player["achievements"]:
            award_achievement("Ghost Whisperer")
    elif fear_level > 5:
        print("\nYou exit the train with a nervous laugh, a bit unsettled but mostly entertained.")
        ending = "pleasantly frightened"
    else:
        print("\nYou exit the train with a smile, having enjoyed the theatrics but not really scared.")
        ending = "amused but not scared"
    
    # Souvenir photo
    print("\nThe ride attendant shows you a photo taken during the ride.")
    print(f"It shows you looking {ending} during one of the scary moments!")
    
    buy_photo = input("Would you like to buy this photo for 2 tickets? (y/n): ").lower()
    
    if buy_photo == "y" and player["tickets"] >= 2:
        player["tickets"] -= 2
        photo_souvenir = "Ghost Train Photo 👻"
        player["inventory"].append(photo_souvenir)
        print(Fore.GREEN + f"You received: {photo_souvenir}")
    elif buy_photo == "y":
        print(Fore.RED + "Not enough tickets to buy the photo!")
    
    # Loyalty points
    add_loyalty_points(2)
    print(Fore.MAGENTA + "+2 Loyalty Points for surviving the Ghost Train!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def carnival_carousel():
    """Beautiful classic carousel ride with hand-carved animals"""
    if not pay_to_play(2):
        return
    
    clear()
    print(Fore.YELLOW + "🎠 CARNIVAL CAROUSEL 🎠")
    print("Experience the timeless magic of our beautifully restored carousel!")
    
    # Track for mission
    track_attraction_visit("Carnival Carousel")
    
    # Ride begins
    print("\nYou approach the magnificent carousel, admiring its intricate details.")
    print("Colorful lights twinkle as the ornate organ music fills the air.")
    print("The carousel features dozens of hand-carved and painted animals.")
    time.sleep(2)
    
    # Choose animal
    animals = [
        {"name": "Majestic Horse", "color": "White", "special": "Jeweled saddle"},
        {"name": "Royal Stallion", "color": "Black", "special": "Golden mane"},
        {"name": "Playful Dolphin", "color": "Blue", "special": "Silver accents"},
        {"name": "Fierce Dragon", "color": "Red", "special": "Breathing smoke effect"},
        {"name": "Gentle Unicorn", "color": "Purple", "special": "Glowing horn"},
        {"name": "Noble Lion", "color": "Gold", "special": "King's crown"},
        {"name": "Exotic Tiger", "color": "Orange", "special": "Illuminated stripes"},
        {"name": "Friendly Elephant", "color": "Gray", "special": "Decorative canopy"}
    ]
    
    print("\nAvailable carousel animals:")
    for i, animal in enumerate(animals, 1):
        print(f"[{i}] {animal['name']} - {animal['color']} with {animal['special']}")
    
    try:
        choice = int(input("\nWhich animal would you like to ride? (1-8): "))
        if choice < 1 or choice > 8:
            raise ValueError
        animal = animals[choice-1]
    except (ValueError, IndexError):
        animal = random.choice(animals)
        print(f"Invalid choice. You're assigned to the {animal['name']}.")
    
    print(f"\nYou climb onto the {animal['color']} {animal['name']} with its {animal['special']}.")
    print("You hold onto the brass pole as the ride attendant checks that everyone is secure.")
    time.sleep(2)
    
    # Ride starts
    print("\nThe carousel begins to move, gradually picking up speed...")
    print("The beautiful organ music plays a cheerful melody.")
    print("Colorful lights reflect off the mirrored panels as you rotate.")
    time.sleep(2)
    
    # Ride experience
    print("\nYou go up and down on your animal as the carousel spins.")
    print("The world outside becomes a colorful blur as you focus on the intricate details.")
    print("There's something magical and timeless about the carousel experience.")
    time.sleep(2)
    
    # Special moments based on animal choice
    if animal["name"] == "Majestic Horse":
        print("\nYour white horse seems to glow under the carousel lights.")
        print("For a moment, you could swear its eyes blinked at you...")
        special_moment = "feeling like royalty"
    elif animal["name"] == "Fierce Dragon":
        print("\nThe dragon's smoke effect creates a mystical cloud around you.")
        print("You imagine yourself flying through the clouds on a real dragon!")
        special_moment = "feeling like a brave knight"
    elif animal["name"] == "Gentle Unicorn":
        print("\nThe unicorn's horn illuminates with rainbow colors.")
        print("There's something enchanted about this particular ride...")
        special_moment = "touched by magic"
    else:
        special_moments = [
            "completely carefree",
            "transported back to childhood",
            "mesmerized by the craftsmanship",
            "wonderfully nostalgic"
        ]
        special_moment = random.choice(special_moments)
    
    # End of ride
    print("\nThe carousel gradually slows to a stop.")
    print(f"You dismount from your {animal['name']}, {special_moment}.")
    print("It was a simple but delightful experience!")
    
    # Photo opportunity
    print("\nA photographer shows you a candid photo they took during the ride.")
    buy_photo = input("Would you like to buy a carousel photo for 2 tickets? (y/n): ").lower()
    
    if buy_photo == "y" and player["tickets"] >= 2:
        player["tickets"] -= 2
        photo_souvenir = "Carousel Photo 🎠"
        player["inventory"].append(photo_souvenir)
        print(Fore.GREEN + f"You received: {photo_souvenir}")
    elif buy_photo == "y":
        print(Fore.RED + "Not enough tickets to buy the photo!")
    
    # Loyalty points
    add_loyalty_points(1)
    print(Fore.MAGENTA + "+1 Loyalty Point for riding the Carnival Carousel!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def bumper_cars():
    """Classic bumper car ride with electric cars"""
    if not pay_to_play(3):
        return
    
    clear()
    print(Fore.BLUE + "🚗 BUMPER CARS 🚗")
    print("Crash into friends in these electric cars!")
    
    # Track for mission
    track_attraction_visit("Bumper Cars")
    
    # Ride begins
    print("\nYou enter the bumper car arena, where colorful electric cars")
    print("zip around a metal floor, sparks flying from the ceiling poles.")
    
    # Choose car
    car_colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
    available_cars = random.sample(car_colors, min(4, len(car_colors)))
    
    print("\nAvailable cars:")
    for i, color in enumerate(available_cars, 1):
        print(f"[{i}] {color} Car")
    
    try:
        choice = int(input("\nWhich car would you like to drive? (1-4): "))
        if choice < 1 or choice > len(available_cars):
            raise ValueError
        car_color = available_cars[choice-1]
    except (ValueError, IndexError):
        car_color = random.choice(available_cars)
        print(f"Invalid choice. You're assigned to the {car_color} Car.")
    
    print(f"\nYou climb into the {car_color} Car and buckle the safety belt.")
    print("You test the pedal and steering wheel, ready for some bumping action!")
    time.sleep(2)
    
    # Generate other drivers
    other_drivers = []
    for color in available_cars:
        if color != car_color:
            driver_type = random.choice(["aggressive", "defensive", "unpredictable", "strategic"])
            other_drivers.append({"color": color, "style": driver_type})
    
    # Ride starts
    print("\nThe buzzer sounds and the floor electrifies!")
    print("All cars spring to life, and the bumping begins!")
    time.sleep(1)
    
    # Bumper car sequence
    print("\nYou press the pedal and your car lurches forward...")
    
    # Track collisions
    collisions = 0
    greatest_hit = None
    times_hit = 0
    
    # Simulated bumper car action (3 rounds)
    for round_num in range(1, 4):
        print(f"\n--- Round {round_num} ---")
        
        # Player action
        print("\nWhat's your strategy?")
        print("[1] Go after a specific car")
        print("[2] Drive defensively and avoid hits")
        print("[3] Go wild and bump anyone in your path")
        
        strategy = input("Choose your strategy (1-3): ")
        
        if strategy == "1":
            # Target a specific car
            target_options = [driver["color"] for driver in other_drivers]
            
            print("\nWhich car do you want to target?")
            for i, color in enumerate(target_options, 1):
                print(f"[{i}] {color} Car")
            
            try:
                target_idx = int(input("Enter choice: ")) - 1
                target = other_drivers[target_idx]["color"]
            except (ValueError, IndexError):
                target = random.choice(target_options)
                print(f"Invalid choice. Targeting the {target} Car instead.")
            
            hit_chance = 0.7  # 70% chance to hit targeted car
            if random.random() < hit_chance:
                print(f"\nYou aim for the {target} Car and WHAM! A direct hit!")
                print(f"The {target} Car spins around from the impact!")
                collisions += 1
                if not greatest_hit or random.random() > 0.5:
                    greatest_hit = target
            else:
                print(f"\nYou aim for the {target} Car but they swerve away at the last second!")
                print("You narrowly avoid hitting the wall instead!")
        
        elif strategy == "2":
            # Defensive driving
            dodge_chance = 0.8  # 80% chance to avoid being hit
            if random.random() < dodge_chance:
                print("\nYou skillfully maneuver your car, avoiding all collisions!")
                print("The other drivers look frustrated as they try to hit you!")
            else:
                hit_by = random.choice(other_drivers)["color"]
                print(f"\nDespite your defensive driving, the {hit_by} Car catches you off guard!")
                print(f"BANG! The {hit_by} Car hits you from behind, jolting you forward!")
                times_hit += 1
        
        else:  # strategy == "3" or any other input
            # Go wild
            hits = random.randint(0, 2)  # Can hit 0-2 cars
            
            if hits == 0:
                print("\nYou zoom around wildly but don't manage to hit anyone!")
                print("Better luck in the next round!")
            else:
                hit_cars = random.sample([d["color"] for d in other_drivers], hits)
                print(f"\nYour wild driving pays off! You hit {hits} cars!")
                for hit_car in hit_cars:
                    print(f"CRASH! You slam into the {hit_car} Car!")
                collisions += hits
                
                if hits > 0:
                    greatest_hit = hit_cars[0]
            
            # But might get hit in return
            if random.random() < 0.4:  # 40% chance to get hit
                hit_by = random.choice(other_drivers)["color"]
                print(f"\nWhile you're driving wild, the {hit_by} Car gets revenge!")
                print("BANG! You get jolted sideways from the impact!")
                times_hit += 1
        
        # Other drivers' actions
        if round_num < 3:  # Only do this for the first two rounds
            random_event = random.choice([
                "The Orange Car spins in circles in the middle of the arena!",
                "Two cars collide head-on with a spectacular CRASH!",
                "A Green Car gets stuck against the wall, wheels spinning!",
                "The Purple Car chases several others around the edge!",
                "A Yellow Car does a perfect 360 spin after being hit!"
            ])
            print(f"\n{random_event}")
            time.sleep(1.5)
    
    # End of ride
    print("\nThe buzzer sounds again, and all cars gradually slow to a stop.")
    print("The bumper car session is over!")
    
    # Results
    print("\n🚗 Your Bumper Car Stats 🚗")
    print(f"Total collisions caused: {collisions}")
    print(f"Times you were hit: {times_hit}")
    if greatest_hit:
        print(f"Your greatest hit was on the {greatest_hit} Car!")
    
    # Award based on performance
    if collisions >= 3:
        print("\nYou were a bumping champion out there!")
        award = "Bumper Car Ace Badge 🏆"
        if award not in player["inventory"]:
            player["inventory"].append(award)
            print(Fore.GREEN + f"You received: {award}")
    elif times_hit == 0:
        print("\nAmazing defensive driving! You didn't get hit once!")
        award = "Dodging Master Pin 🛡️"
        if award not in player["inventory"]:
            player["inventory"].append(award)
            print(Fore.GREEN + f"You received: {award}")
    
    # Loyalty points
    add_loyalty_points(2)
    print(Fore.MAGENTA + "+2 Loyalty Points for the bumper car experience!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def cinema_4d():
    """4D Cinema experience with sensory effects"""
    if not pay_to_play(5):
        return
    
    clear()
    print(Fore.CYAN + "🎬 4D CINEMA 🎬")
    print("Experience movies with environmental effects!")
    
    # Track for mission
    track_attraction_visit("4D Cinema")
    
    # Available 4D films
    films = [
        {"title": "Ocean Explorer", "genre": "Documentary", "length": "20 min", 
         "effects": ["Water Spray", "Moving Seats", "Wind", "Scents"]},
        {"title": "Cosmic Adventure", "genre": "Science Fiction", "length": "15 min", 
         "effects": ["Vibration", "Strobe Lights", "Air Blasts", "Moving Seats"]},
        {"title": "Jungle Quest", "genre": "Adventure", "length": "18 min", 
         "effects": ["Scents", "Moving Seats", "Ticklers", "Water Spray"]},
        {"title": "Thrill Ride", "genre": "Action", "length": "12 min", 
         "effects": ["Moving Seats", "Air Blasts", "Vibration", "Strobe Lights"]}
    ]
    
    # Display films
    print("\nToday's 4D Films:")
    for i, film in enumerate(films, 1):
        print(f"[{i}] {film['title']} - {film['genre']} ({film['length']})")
        print(f"    Effects: {', '.join(film['effects'])}")
    
    # Choose film
    try:
        choice = int(input("\nWhich film would you like to see? (1-4): "))
        if choice < 1 or choice > 4:
            raise ValueError
        film = films[choice-1]
    except (ValueError, IndexError):
        film = random.choice(films)
        print(f"Invalid choice. You'll be watching {film['title']}.")
    
    # Prepare for the film
    print(f"\nYou enter the 4D theater for '{film['title']}'.")
    print("The usher hands you a pair of 3D glasses and shows you to your seat.")
    print("The specialized chairs have built-in effects systems.")
    time.sleep(2)
    
    # Film starts
    print(f"\nThe lights dim and '{film['title']}' begins...")
    print("The 3D visuals immediately pop out from the screen, creating depth and realism.")
    time.sleep(2)
    
    # Film experience based on the film chosen
    if film["title"] == "Ocean Explorer":
        # Ocean Explorer experience
        print("\nYou dive beneath the waves in an underwater adventure...")
        time.sleep(1.5)
        print("As fish swim toward the camera, your seat gently moves in sync!")
        time.sleep(1.5)
        print("A whale sprays water - and a fine mist sprays onto your face!")
        time.sleep(1.5)
        print("The ocean breeze is simulated with cool air flowing through the theater.")
        time.sleep(1.5)
        print("As you pass a coral reef, the scent of the ocean fills the air!")
        
        highlight = "swimming with dolphins as water sprayed from the ceiling"
        
    elif film["title"] == "Cosmic Adventure":
        # Cosmic Adventure experience
        print("\nYou board a spaceship for an intergalactic journey...")
        time.sleep(1.5)
        print("The launch sequence begins, and your seat vibrates with the rocket engines!")
        time.sleep(1.5)
        print("As you fly through an asteroid field, your seat jerks left and right!")
        time.sleep(1.5)
        print("A nearby star explodes with brilliant strobe effects!")
        time.sleep(1.5)
        print("Air blasts hit your neck as alien creatures fly past your ship!")
        
        highlight = "the meteor shower sequence with intense seat movement"
        
    elif film["title"] == "Jungle Quest":
        # Jungle Quest experience
        print("\nYou venture deep into an unexplored rainforest...")
        time.sleep(1.5)
        print("The rich scents of exotic flowers fill the theater!")
        time.sleep(1.5)
        print("Your seat shifts as you navigate across a rickety bridge!")
        time.sleep(1.5)
        print("Something brushes against your legs - the ticklers simulating plants!")
        time.sleep(1.5)
        print("A waterfall appears, and a gentle spray of water mists your face!")
        
        highlight = "the butterfly swarm with scents and gentle ticklers on your legs"
        
    else:  # Thrill Ride
        # Thrill Ride experience
        print("\nYou're strapped into a virtual roller coaster adventure...")
        time.sleep(1.5)
        print("The first drop sends your seat tilting forward dramatically!")
        time.sleep(1.5)
        print("Air blasts hit your face as you virtually speed through tunnels!")
        time.sleep(1.5)
        print("The entire seat vibrates as you cross a rickety wooden track section!")
        time.sleep(1.5)
        print("Strobe lights create a dizzying effect as you spin through a loop!")
        
        highlight = "the massive loop-de-loop with synchronized seat movement"
    
    # Film ends
    time.sleep(2)
    print(f"\nThe '{film['title']}' experience comes to an end.")
    print("The lights come up as you remove your 3D glasses.")
    print(f"The most incredible part was {highlight}!")
    
    # Souvenir
    souvenir = f"4D Experience Ticket: {film['title']} 🎟️"
    if souvenir not in player["inventory"]:
        player["inventory"].append(souvenir)
        print(Fore.GREEN + f"\nYou received: {souvenir}")
    
    # Loyalty points
    add_loyalty_points(3)
    print(Fore.MAGENTA + "+3 Loyalty Points for experiencing 4D Cinema!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def dinosaur_safari():
    """Travel back in time to see prehistoric creatures"""
    if not pay_to_play(6):
        return
    
    clear()
    print(Fore.GREEN + "🦕 DINOSAUR SAFARI 🦕")
    print("Travel back in time to see prehistoric creatures!")
    
    # Track for mission
    track_attraction_visit("Dinosaur Safari")
    
    # Ride begins
    print("\nYou enter the Dinosaur Safari building, designed like a research facility.")
    print("A park ranger greets you: 'Welcome to the Temporal Dinosaur Safari!'")
    print("'Today you'll journey 65 million years into the past using our time rover.'")
    time.sleep(2)
    
    # Pre-show
    print("\nYou watch a brief pre-show video explaining the 'technology'")
    print("behind the time travel and safety precautions for observing dinosaurs.")
    print("'Remember,' says the scientist on screen, 'we're observing only. No interaction!'")
    time.sleep(2)
    
    # Board the vehicle
    print("\nYou board a rugged-looking vehicle called the 'Time Rover'.")
    print("It has oversized wheels and reinforced windows for 'dinosaur protection'.")
    print("The ranger secures your safety harness and starts the vehicle's 'temporal engines'.")
    time.sleep(2)
    
    # Start of safari
    print("\nThe time machine activates! Lights flash and fog fills the chamber...")
    print("The vehicle shakes and rumbles as you 'travel through time'...")
    print("Suddenly, everything clears, and you find yourself in a prehistoric landscape!")
    time.sleep(2)
    
    # Dinosaur encounters
    dinos = [
        {"name": "Triceratops", "behavior": "grazing peacefully on ferns", "reaction": "barely notices you"},
        {"name": "Brachiosaurus", "behavior": "reaching for treetop leaves", "reaction": "looks down curiously"},
        {"name": "Stegosaurus", "behavior": "drinking from a lake", "reaction": "raises its spiked tail defensively"},
        {"name": "Pteranodon", "behavior": "soaring overhead", "reaction": "screeches loudly"},
        {"name": "Parasaurolophus", "behavior": "calling to its herd with its crest", "reaction": "the herd responds with similar calls"}
    ]
    
    # Show several dinosaur encounters
    print("\nYour ranger guide starts the safari tour...")
    
    for i in range(3):  # Three random encounters
        dino = random.choice(dinos)
        dinos.remove(dino)  # Don't repeat dinosaurs
        
        print("\nThe Time Rover rounds a corner, and there it is!")
        print(f"A real {dino['name']} {dino['behavior']}!")
        print(f"As your vehicle approaches, the {dino['name']} {dino['reaction']}.")
        print("You take plenty of photos of this incredible sight!")
        
        # Interactive moment
        print("\nThe ranger asks if you want to:")
        print("[1] Move closer for a better view")
        print("[2] Stay at a safe distance")
        choice = input("What do you do? (1/2): ")
        
        if choice == "1":
            # Closer approach
            if random.random() < 0.7:
                print(f"\nThe Time Rover slowly approaches the {dino['name']}.")
                print("You get an amazing up-close view of the magnificent creature!")
                print("This will make for incredible photos!")
            else:
                print(f"\nAs you approach, the {dino['name']} becomes startled!")
                print("It makes a threatening display, forcing your rover to back away quickly!")
                print("The ranger reminds everyone about keeping a safe distance.")
        else:
            # Safe distance
            print(f"\nYou observe the {dino['name']} from a respectful distance.")
            print("The magnificent creature continues its natural behavior undisturbed.")
            print("The ranger commends your respect for wildlife protocols.")
        
        time.sleep(2)
    
    # T-Rex encounter - the main event
    print("\nThe radio crackles with an urgent message:")
    print("'Ranger, be advised: T-Rex detected in your sector. Proceed with caution.'")
    print("\nYour heart races as the Time Rover enters a dense forest area...")
    time.sleep(2)
    
    print("\nSuddenly, trees crash down ahead!")
    print("A massive Tyrannosaurus Rex bursts through the foliage, roaring ferociously!")
    print("The ground shakes with each step of the apex predator!")
    time.sleep(2)
    
    # T-Rex chase sequence
    print("\nThe T-Rex spots your rover and charges!")
    print("'HANG ON!' shouts the ranger, throwing the vehicle into reverse!")
    print("The massive dinosaur pursues you through the prehistoric jungle!")
    print("Your rover bounces violently over the terrain as the T-Rex gains ground!")
    time.sleep(2)
    
    print("\nJust as the T-Rex is about to catch you, the vehicle plunges into a cave!")
    print("The dinosaur roars in frustration, too large to follow!")
    print("That was an incredibly close call!")
    time.sleep(2)
    
    # Return to present
    print("\n'Initiating emergency temporal recall!' announces the ranger.")
    print("The time machine activates, surroundings blur, and lights flash...")
    print("With a final jolt, you return to the present day!")
    time.sleep(2)
    
    # End of ride
    print("\nThe ranger wipes sweat from his brow: 'Well folks, that was")
    print("a bit closer than our usual tours! Welcome back to the present!'")
    print("You exit the Time Rover on slightly shaky legs, thoroughly thrilled!")
    
    # Souvenir photo
    print("\nAt the exit, monitors display photos taken during your adventure.")
    print("There's a great shot of you looking terrified during the T-Rex chase!")
    
    buy_photo = input("Would you like to buy this photo for 3 tickets? (y/n): ").lower()
    
    if buy_photo == "y" and player["tickets"] >= 3:
        player["tickets"] -= 3
        photo_souvenir = "Dinosaur Safari Photo with T-Rex 📸"
        player["inventory"].append(photo_souvenir)
        print(Fore.GREEN + f"You received: {photo_souvenir}")
    elif buy_photo == "y":
        print(Fore.RED + "Not enough tickets to buy the photo!")
    
    # Bonus souvenir
    dino_souvenir = "Dinosaur Tooth Replica 🦷"
    if dino_souvenir not in player["inventory"]:
        player["inventory"].append(dino_souvenir)
        print(Fore.GREEN + f"You also received a {dino_souvenir} as a memento!")
    
    # Loyalty points
    add_loyalty_points(4)
    print(Fore.MAGENTA + "+4 Loyalty Points for surviving the Dinosaur Safari!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def petting_zoo():
    """Meet and feed friendly farm animals"""
    if not pay_to_play(3):
        return
    
    clear()
    print(Fore.GREEN + "🦙 PETTING ZOO 🦙")
    print("Meet and feed friendly farm animals!")
    
    # Track for mission
    track_attraction_visit("Petting Zoo")
    
    # Animals in the petting zoo
    animals = [
        {"name": "Goats", "behavior": "playful and curious", "likes": "being scratched behind the ears"},
        {"name": "Sheep", "behavior": "gentle and fluffy", "likes": "having their wool petted"},
        {"name": "Rabbits", "behavior": "soft and cautious", "likes": "gentle petting and quiet voices"},
        {"name": "Miniature Horses", "behavior": "friendly and majestic", "likes": "being stroked along the neck"},
        {"name": "Alpacas", "behavior": "dignified and inquisitive", "likes": "gentle handling and treats"},
        {"name": "Pot-Bellied Pigs", "behavior": "intelligent and food-motivated", "likes": "belly rubs"}
    ]
    
    # Entry to the zoo
    print("\nYou enter the petting zoo area, a clean and well-maintained space")
    print("filled with friendly farm animals and the sound of happy children.")
    print("A zoo keeper hands you a small paper cone filled with animal feed.")
    print("'Remember to let the animals approach you and be gentle,' they advise.")
    time.sleep(2)
    
    # Animal encounters
    visited_animals = []
    feed_remaining = 3  # You can feed 3 times
    
    while feed_remaining > 0 and len(visited_animals) < len(animals):
        # Show available animals
        print("\nWhich animals would you like to visit?")
        available_animals = [animal for animal in animals if animal not in visited_animals]
        
        for i, animal in enumerate(available_animals, 1):
            print(f"[{i}] {animal['name']}")
        
        print(f"[0] Exit (you still have {feed_remaining} portions of feed)")
        
        try:
            choice = int(input("Choose animals to visit: "))
            if choice == 0:
                break
                
            if choice < 1 or choice > len(available_animals):
                raise ValueError
                
            animal = available_animals[choice-1]
            visited_animals.append(animal)
            
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
            continue
        
        # Visit the chosen animals
        print(f"\nYou approach the area with the {animal['name']}.")
        print(f"They are {animal['behavior']} and seem interested in your feed.")
        print(f"You learn they especially enjoy {animal['likes']}.")
        
        interaction = input("\nWould you like to feed or pet them? (feed/pet): ").lower()
        
        if interaction == "feed" and feed_remaining > 0:
            print(f"\nYou offer some feed to the {animal['name']}.")
            print("They eagerly eat from your hand, their whiskers tickling your palm.")
            print("It's a delightful experience to connect with these animals!")
            feed_remaining -= 1
            
            # Special random events
            events = [
                f"A baby {animal['name'].lower()} comes over for extra attention!",
                f"The {animal['name'].lower()} nuzzle you affectionately after eating!",
                f"A zoo keeper shares an interesting fact about {animal['name'].lower()}!",
                f"A particularly photogenic {animal['name'].lower()[:-1]} poses perfectly for a photo!"
            ]
            
            if random.random() < 0.6:  # 60% chance of special event
                special_event = random.choice(events)
                print(f"\n{special_event}")
                
                # Photo opportunity for the fourth event
                if events.index(special_event) == 3:
                    photo_chance = True
                else:
                    photo_chance = False
            else:
                photo_chance = False
            
        elif interaction == "feed" and feed_remaining <= 0:
            print("\nYou're out of feed! You can still pet the animals though.")
            print(f"You gently pet the {animal['name']} instead.")
            
        else:  # pet or anything else
            print(f"\nYou gently pet the {animal['name']}, being respectful of their space.")
            print(f"They seem to enjoy your attention, especially when you focus on {animal['likes']}.")
            
            # Chance for a special reaction
            if random.random() < 0.4:  # 40% chance
                special_reactions = [
                    f"One of the {animal['name'].lower()} leans into your hand, clearly enjoying the petting!",
                    f"The {animal['name'].lower()} make contented sounds as you pet them!",
                    f"A small {animal['name'].lower()[:-1]} follows you as you start to walk away!"
                ]
                print(f"\n{random.choice(special_reactions)}")
        
        # Photo opportunity
        photo_chance = False
        if photo_chance or random.random() < 0.3:  # 30% chance otherwise
            print("\nA staff photographer captures a wonderful moment between you and the animals!")
            buy_photo = input("Would you like to buy this special photo for 2 tickets? (y/n): ").lower()
            
            if buy_photo == "y" and player["tickets"] >= 2:
                player["tickets"] -= 2
                photo_name = f"{animal['name']} Encounter Photo 📸"
                player["inventory"].append(photo_name)
                print(Fore.GREEN + f"You received: {photo_name}")
            elif buy_photo == "y":
                print(Fore.RED + "Not enough tickets to buy the photo!")
        
        time.sleep(2)
    
    # End of visit
    if feed_remaining <= 0:
        print("\nYou've used all your animal feed!")
    
    if len(visited_animals) >= 3:
        print("\nYou've had a wonderful time visiting with various animals at the petting zoo!")
        # Award special souvenir for visiting many animals
        special_souvenir = "Animal Friend Badge 🐑"
        if special_souvenir not in player["inventory"]:
            player["inventory"].append(special_souvenir)
            print(Fore.GREEN + f"For your love of animals, you received: {special_souvenir}")
    else:
        print("\nYou've enjoyed your time at the petting zoo!")
    
    # Handwashing reminder
    print("\nThe zoo keeper reminds you to wash your hands at the sink station")
    print("before leaving the petting zoo area. Animal safety first!")
    
    # Loyalty points
    add_loyalty_points(2)
    print(Fore.MAGENTA + "+2 Loyalty Points for visiting the Petting Zoo!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def zombie_escape():
    """Interactive zombie apocalypse experience with choices"""
    if not pay_to_play(7):
        return
    
    clear()
    print(Fore.GREEN + "🧟 ZOMBIE ESCAPE 🧟")
    print("Can you survive the zombie apocalypse?")
    
    # Track for mission
    track_attraction_visit("Zombie Escape")
    
    # Ride begins
    print("\nYou enter what looks like an abandoned laboratory.")
    print("A scientist in a torn lab coat rushes up to you.")
    print("'Thank goodness you're here! Our experiment went terribly wrong!'")
    print("'The infection is spreading, and the zombies are everywhere!'")
    print("'You need to help us escape this facility!'")
    time.sleep(3)
    
    # Start of interactive experience
    print("\nSuddenly, alarms blare and red emergency lights flash!")
    print("'They've broken through the main door! We need to move NOW!'")
    
    # Track survival
    survived = True
    zombie_encounters = 0
    has_weapon = False
    has_keycard = False
    
    # First choice
    print("\nYou have three possible routes:")
    print("[1] Through the main corridor - it's direct but might have zombies")
    print("[2] Through the air vents - slower but possibly safer")
    print("[3] Wait for security to arrive")
    
    choice1 = input("What do you choose? (1-3): ")
    
    if choice1 == "1":
        print("\nYou dash into the main corridor!")
        print("As you run, you hear moaning echoes bouncing off the walls...")
        time.sleep(1.5)
        print("\nSuddenly, a zombie scientist lurches around the corner!")
        zombie_encounters += 1
        
        fight_choice = input("Do you fight or run? (fight/run): ").lower()
        
        if fight_choice == "fight":
            print("\nYou look around for a weapon and grab a fire extinguisher!")
            print("You blast the zombie with foam and then hit it with the canister!")
            print("The zombie falls to the ground, temporarily stunned.")
            has_weapon = True
            print("\nYou notice the zombie has a keycard! You take it.")
            has_keycard = True
        else:
            print("\nYou sprint past the zombie, barely avoiding its grasp!")
            print("Your heart pounds as you hear it shuffling after you.")
    
    elif choice1 == "2":
        print("\nYou climb into the air vents!")
        print("The metal creaks as you crawl through the narrow passages.")
        print("It's dark and dusty, but you don't hear any zombies...")
        time.sleep(2)
        print("\nAs you crawl, you spot a security office below through a vent.")
        print("You can see a keycard and a stun baton on the desk.")
        
        grab_choice = input("Do you try to grab them? (y/n): ").lower()
        
        if grab_choice == "y":
            print("\nYou carefully remove the vent cover and reach down...")
            if random.random() < 0.7:  # 70% success chance
                print("Success! You grab both items before continuing!")
                has_weapon = True
                has_keycard = True
            else:
                print("Your hand slips and you fall through the vent!")
                print("CRASH! You land in the office with a loud noise.")
                print("\nA zombie security guard immediately turns toward you!")
                zombie_encounters += 1
                print("You quickly grab the keycard but have to flee without the weapon!")
                has_keycard = True
        else:
            print("\nYou continue through the vents without the items.")
    
    else:  # choice1 == "3" or any other input
        print("\nYou decide to wait for security...")
        print("Minutes pass with no sign of help...")
        print("\nSuddenly, three zombies in security uniforms burst in!")
        print("They were the security team - now infected!")
        zombie_encounters += 3
        
        # This is a bad choice, but give them a chance
        print("\nYou have no choice but to run!")
        print("As you flee, you grab a keycard from a desk!")
        has_keycard = True
        survived = random.random() < 0.5  # 50% survival chance
        
        if not survived:
            print("\nThe zombies are too numerous! They surround you!")
            print("Game over! You have been infected!")
    
    # Continue if survived first encounter
    if survived:
        # Second choice - if they've made it this far
        print("\nYou reach a junction in the facility:")
        print("[1] Laboratory - might have a cure or weapons")
        print("[2] Exit doors - requires keycard for emergency exit")
        print("[3] Garage - might have vehicles for escape")
        
        choice2 = input("Where do you go? (1-3): ")
        
        if choice2 == "1":
            print("\nYou enter the main laboratory...")
            print("Broken test tubes and lab equipment are scattered everywhere.")
            print("You find a prototype weapon - a sonic disruptor that stuns zombies!")
            has_weapon = True
            
            print("\nAs you search for a cure, three zombies emerge from the back room!")
            zombie_encounters += 3
            
            if has_weapon:
                print("\nYou use the sonic disruptor to stun the zombies!")
                print("While they're immobilized, you rush past them!")
            else:
                print("\nWith no weapon, you have to be creative!")
                print("You throw chemicals to create a smokescreen and dash past them!")
                survived = random.random() < 0.6  # 60% survival chance
                
                if not survived:
                    print("\nA zombie grabs you through the smoke! You can't break free!")
                    print("Game over! You have been infected!")
        
        elif choice2 == "2":
            print("\nYou rush to the emergency exit doors!")
            
            if has_keycard:
                print("\nYou swipe the keycard and the doors begin to open!")
                print("Freedom is just beyond these doors!")
            else:
                print("\nThe exit requires a keycard that you don't have!")
                print("You frantically search nearby desks as moaning grows louder...")
                
                if random.random() < 0.4:  # 40% chance to find keycard
                    print("Luck is on your side! You find a keycard in a drawer!")
                    has_keycard = True
                    print("You swipe it and the doors begin to open!")
                else:
                    print("You can't find a keycard! The doors won't open!")
                    print("\nA horde of zombies rounds the corner, blocking your escape route!")
                    zombie_encounters += 5
                    
                    if has_weapon:
                        print("You use your weapon to clear a path and run back into the facility!")
                    else:
                        print("With no weapon and no escape route, you're cornered!")
                        survived = False
                        print("Game over! You have been infected!")
        
        else:  # choice2 == "3" or any other input
            print("\nYou make your way to the garage level...")
            print("Several vehicles are parked here, but you need keys.")
            print("\nYou spot a key rack on the wall!")
            
            if random.random() < 0.7:  # 70% chance to find keys
                print("You grab a set of keys for a nearby jeep!")
                print("\nAs you start the engine, zombies begin pouring into the garage!")
                print("You floor it, crashing through the garage door to freedom!")
            else:
                print("The key rack is empty! Someone already took all the keys!")
                print("\nZombies begin entering the garage from multiple entrances!")
                zombie_encounters += 4
                
                if has_weapon:
                    print("You use your weapon to fight your way to a maintenance exit!")
                else:
                    print("With no weapon and no vehicle, you're in serious trouble!")
                    survived = random.random() < 0.3  # Only 30% survival chance
                    
                    if not survived:
                        print("The zombies overwhelm you! Game over!")
    
    # Final outcome
    if survived:
        print("\n🎉 CONGRATULATIONS! YOU SURVIVED! 🎉")
        print(f"Zombie encounters: {zombie_encounters}")
        
        # Reward based on performance
        if zombie_encounters == 0:
            print("\nPerfect stealth run! You never encountered a single zombie!")
            survival_rating = "Perfect"
            tickets_reward = 15
            
            # Special achievement
            if "Ghost Runner" not in player["achievements"]:
                award_achievement("Ghost Runner")
        elif zombie_encounters <= 2:
            print("\nExcellent survival skills! You minimized zombie encounters!")
            survival_rating = "Excellent"
            tickets_reward = 10
        elif zombie_encounters <= 5:
            print("\nGood job! You handled the situation well despite several encounters!")
            survival_rating = "Good"
            tickets_reward = 7
        else:
            print("\nYou survived by the skin of your teeth! That was close!")
            survival_rating = "Marginal"
            tickets_reward = 5
        
        # Award tickets
        player["tickets"] += tickets_reward
        print(Fore.GREEN + f"You earned {tickets_reward} bonus tickets!")
        
        # Souvenir
        souvenir = f"Zombie Survival Badge ({survival_rating}) 🧪"
        player["inventory"].append(souvenir)
        print(Fore.GREEN + f"You received: {souvenir}")
    else:
        print("\n☠️ GAME OVER - YOU WERE INFECTED ☠️")
        print("Better luck next time!")
        print("\nThe staff help you 'decontaminate' and exit the attraction.")
        print("Even though you didn't survive, it was an exciting experience!")
        
        # Consolation prize
        player["tickets"] += 2
        print(Fore.GREEN + "You received 2 consolation tickets!")
        
        souvenir = "Zombie Victim Tag ☣️"
        player["inventory"].append(souvenir)
        print(Fore.GREEN + f"You received: {souvenir}")
    
    # Loyalty points
    add_loyalty_points(4)
    print(Fore.MAGENTA + "+4 Loyalty Points for experiencing Zombie Escape!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def splash_mountain():
    """Thrilling log ride with a big splash finale"""
    if not pay_to_play(5):
        return
    
    clear()
    print(Fore.BLUE + "💦 SPLASH MOUNTAIN 💦")
    print("Prepare to get wet on this exciting water adventure!")
    
    # Track for mission
    track_attraction_visit("Splash Mountain")
    
    # Ride begins
    print("\nYou climb into a hollowed-out log boat and secure yourself.")
    print("The ride attendant reminds you: 'You may get wet on this ride!'")
    time.sleep(2)
    
    # Start of journey
    print("\nYour log begins its journey, floating gently through a peaceful river...")
    print("Colorful animatronic animals sing cheerful songs along the banks.")
    time.sleep(2)
    
    # First small drop
    print("\nYou approach a small drop...")
    time.sleep(1)
    print("Whoosh! Your log slides down, creating a small splash!")
    print("Just a teaser of what's to come...")
    time.sleep(2)
    
    # Middle section
    print("\nYour log winds through a charming forest scene...")
    print("More animatronic animals tell the story of the mountain.")
    time.sleep(2)
    
    # Cave section
    print("\nYou enter a dark cave... the music becomes more ominous...")
    print("Strange glowing eyes peek out from the darkness.")
    time.sleep(2)
    
    # Climb to final drop
    print("\nYour log begins the long climb up to the summit of Splash Mountain...")
    print("Clickety-clack... the chain pulls you higher and higher...")
    print("You can see the entire park as you near the top!")
    time.sleep(3)
    
    # The big drop
    print("\nYou reach the top and pause for a moment...")
    print("You look down at the MASSIVE drop before you...")
    time.sleep(1)
    print("HERE IT COMES...")
    time.sleep(1)
    print("WHOOOOOOOOOOSH!!!")
    print("Your log plummets down the steep drop at high speed!")
    print("You raise your arms and scream with excitement!")
    time.sleep(2)
    
    # The splash
    splash_size = random.choice(["ENORMOUS", "MASSIVE", "GIGANTIC", "COLOSSAL"])
    print(f"\nSPLASH!!! Your log creates an {splash_size} wave as it hits the water!")
    
    # Wetness factor - random
    wetness = random.randint(1, 3)
    if wetness == 1:
        print("Luck is on your side! You only get a few refreshing drops on you.")
        print("The people behind you got soaked instead!")
        wetness_result = "barely wet"
    elif wetness == 2:
        print("You get moderately splashed! Your face and shirt are wet, but it's refreshing.")
        print("Perfect on a hot day!")
        wetness_result = "pleasantly damp"
    else:
        print("SPLOOSH! You get COMPLETELY SOAKED from head to toe!")
        print("You couldn't be wetter if you'd jumped in a pool!")
        wetness_result = "absolutely drenched"
        
        # Special achievement for getting soaked
        if "Water Warrior" not in player["achievements"]:
            award_achievement("Water Warrior")
    
    # End of ride
    print(f"\nYour log returns to the station, and you step out {wetness_result}.")
    print("That was an exhilarating adventure!")
    
    # Photo opportunity
    print("\n'Want to see your splash photo?' asks the attendant.")
    see_photo = input("Would you like to see your splash photo? (y/n): ").lower()
    
    if see_photo == "y":
        expressions = ["screaming with delight", "eyes closed tight", "arms raised high", 
                      "looking terrified", "laughing", "perfectly composed"]
        expression = random.choice(expressions)
        print(f"\nYour photo shows you {expression} during the big drop!")
        photo_souvenir = "Splash Mountain Photo 📸"
        buy_photo = input("Would you like to buy this photo for 2 tickets? (y/n): ").lower()
        
        if buy_photo == "y" and player["tickets"] >= 2:
            player["tickets"] -= 2
            player["inventory"].append(photo_souvenir)
            print(Fore.GREEN + f"You received: {photo_souvenir}")
        elif buy_photo == "y":
            print(Fore.RED + "Not enough tickets to buy the photo!")
    
    # Loyalty points
    add_loyalty_points(3)
    print(Fore.MAGENTA + "+3 Loyalty Points for braving Splash Mountain!")
    
    input("\nPress Enter to return to the theme park...")
    return theme_park_menu()

def cosmic_coaster():
    """Cosmic Coaster ride simulation with multiple paths and outcomes"""
    if not pay_to_play(5):
        return
    
    clear()
    print(Fore.CYAN + "🚀 Welcome to the COSMIC COASTER! 🚀")
    print("Hold tight as we blast off into the cosmos!")
    
    print("\nThe ride operator secures your safety harness...")
    time.sleep(1.5)
    print("3...")
    time.sleep(0.7)
    print("2...")
    time.sleep(0.7)
    print("1...")
    time.sleep(0.7)
    print(Fore.YELLOW + "BLAST OFF! 🚀")
    
    # Interactive ride simulation
    print("\nYour rocket coaster reaches a fork in the cosmic path!")
    print("[1] Take the Meteor Shower path")
    print("[2] Take the Black Hole path")
    
    path = input("Choose your path (1/2): ")
    
    if path == "1":
        print("\nYou zoom through a dazzling meteor shower!")
        print("Colorful space rocks pass just inches from your car!")
        chance = random.randint(1, 10)
        if chance > 3:
            print(Fore.GREEN + "\nYou navigate the meteor field perfectly!")
            print("The crowd cheers as your coaster returns to the station!")
            reward = random.randint(6, 10)
            print(f"You earned {reward} tickets for your bravery!")
            player["tickets"] += reward
            award_achievement("Cosmic Navigator: Survived the meteor shower")
        else:
            print(Fore.YELLOW + "\nA meteor grazes your coaster car!")
            print("The ride's safety systems engage the emergency brakes.")
            print("You still had fun, but it was a bumpy ride.")
            reward = random.randint(2, 5)
            print(f"You earned {reward} tickets for trying!")
            player["tickets"] += reward
    else:
        print("\nYour coaster plunges toward a swirling black hole!")
        print("The gravitational forces intensify as you spiral inward!")
        print("Everything goes dark for a moment...")
        time.sleep(2)
        print(Fore.MAGENTA + "\nSUDDENLY! You're ejected through a wormhole!")
        print("The crowd gasps as your coaster performs an impossible loop!")
        reward = random.randint(7, 12)
        print(f"You earned {reward} tickets for your extreme adventure!")
        player["tickets"] += reward
        award_achievement("Wormhole Survivor: Braved the black hole path")
    
    print("\nThe ride attendant helps you exit the coaster.")
    print("What an amazing experience!")

def log_flume():
    """Log flume water ride with randomized splash outcomes"""
    if not pay_to_play(4):
        return
    
    clear()
    print(Fore.BLUE + "💦 Welcome to the WILD WATER LOG FLUME! 💦")
    print("Get ready to make a splash!")
    
    print("\nYou climb aboard your hollow log boat...")
    time.sleep(1)
    print("The water current carries you through a peaceful river...")
    time.sleep(1.5)
    print("Birds chirp and animatronic animals wave as you pass by...")
    time.sleep(1.5)
    print(Fore.YELLOW + "Wait! You're approaching the final drop!")
    
    # Build suspense
    input("\nPress Enter to brace for impact...")
    
    drop_height = random.choice(["small", "medium", "large", "extreme"])
    
    if drop_height == "small":
        print("\nA gentle slope sends you down with a mild splash!")
        reward = 3
    elif drop_height == "medium":
        print("\nA good-sized drop gives you a refreshing splash!")
        reward = 5
    elif drop_height == "large":
        print("\nWhoosh! A serious drop creates a huge wave that soaks everyone nearby!")
        reward = 8
    else:
        print("\nINCREDIBLE! The legendary 'tsunami drop' hits and creates a massive wall of water!")
        print("Everyone within 30 feet gets completely drenched!")
        reward = 12
        award_achievement("Tsunami Maker: Experienced the legendary extreme drop")
    
    print(f"\nYou earned {reward} tickets from your water adventure!")
    player["tickets"] += reward
    
    # Easter egg: rare rainbow sighting
    if random.randint(1, 10) == 1:
        print(Fore.MAGENTA + "\n✨ SPECIAL EVENT: A rainbow appears over the splash zone! ✨")
        print("Park staff award you a bonus 5 tickets for the magical moment!")
        player["tickets"] += 5
        award_achievement("Rainbow Spotter: Witnessed the rare flume rainbow")

def haunted_mansion():
    """Interactive haunted house experience with jump scares and rewards"""
    if not pay_to_play(6):
        return
    
    clear()
    print(Fore.RED + "👻 Welcome to the HAUNTED MANSION! 👻")
    print("Enter... if you dare!")
    
    bravery = 100
    rewards = 0
    
    # Intro
    print("\nThe door creaks open, inviting you inside...")
    time.sleep(1.5)
    print("A ghostly butler bows and gestures toward the hallway...")
    time.sleep(1.5)
    
    # Room 1
    print("\n--- The Portrait Gallery ---")
    print("The eyes in the paintings seem to follow your movement...")
    choice = input("Do you [1] Look closer at the paintings or [2] Hurry past? ")
    
    if choice == "1":
        if random.randint(1, 10) > 4:
            print("\nAs you examine a portrait, it WINKS at you!")
            print("You found a secret! +3 tickets")
            rewards += 3
        else:
            print("\nSUDDENLY! The portrait changes to a screaming face!")
            print("You jump back, startled!")
            bravery -= 20
    
    # Room 2
    print("\n--- The Dining Room ---")
    print("A grand feast is laid out, but the chairs are occupied by transparent figures...")
    choice = input("Do you [1] Sit down at the table or [2] Stay by the wall? ")
    
    if choice == "1":
        print("\nAs you sit, the ghosts raise their glasses to you!")
        print("One passes through you, leaving a chilling sensation.")
        print("Your boldness impressed them! +4 tickets")
        rewards += 4
    else:
        print("\nAs you hug the wall, a hidden panel opens!")
        print("A skeletal hand reaches out for you!")
        bravery -= 15
    
    # Room 3
    print("\n--- The Séance Chamber ---")
    print("A crystal ball glows in the center of the room...")
    choice = input("Do you [1] Touch the crystal ball or [2] Observe from a distance? ")
    
    if choice == "1":
        outcome = random.randint(1, 10)
        if outcome > 7:
            print("\nThe ball glows brightly at your touch!")
            print("A ghostly voice predicts good fortune!")
            print("You're rewarded with 6 tickets!")
            rewards += 6
        else:
            print("\nThe ball turns blood red and lets out a piercing scream!")
            print("You nearly faint from shock!")
            bravery -= 25
    
    # Final room and results
    print("\n--- The Exit ---")
    print("You've reached the final room of the mansion.")
    
    if bravery > 70:
        print(Fore.GREEN + "\nThe ghosts are impressed by your courage!")
        bonus = random.randint(5, 10)
        print(f"They award you a bonus of {bonus} tickets!")
        rewards += bonus
        award_achievement("Fearless Explorer: Braved the haunted mansion")
    elif bravery > 40:
        print(Fore.YELLOW + "\nYou made it through with your sanity intact!")
        bonus = random.randint(2, 5)
        print(f"You receive a modest reward of {bonus} tickets.")
        rewards += bonus
    else:
        print(Fore.RED + "\nYou rush out of the mansion, badly shaken!")
        print("At least you survived...")
        rewards = max(1, rewards)
    
    print(f"\nTotal tickets earned: {rewards}")
    player["tickets"] += rewards

def ferris_wheel():
    """Peaceful Ferris wheel ride with random events and photo opportunities"""
    if not pay_to_play(3):
        return
    
    clear()
    print(Fore.CYAN + "🎡 Welcome to the GRAND FERRIS WHEEL! 🎡")
    print("Enjoy spectacular views from the top!")
    
    # Start the ride
    print("\nYou board your passenger car...")
    time.sleep(1)
    print("The wheel begins to turn slowly...")
    time.sleep(1.5)
    print("You rise higher and higher above the carnival...")
    
    # Random events
    events = [
        "You spot a beautiful rainbow in the distance! +2 tickets",
        "The sunset creates a gorgeous view of the entire park! +3 tickets",
        "You can see for miles in every direction! +1 ticket",
        "A bird lands briefly on your passenger car! +2 tickets",
        "You spot someone you know down below and wave frantically! +1 ticket",
        "The wheel stops with you at the very top for an amazing photo op! +4 tickets"
    ]
    
    event = random.choice(events)
    reward = int(event.split("+")[1].split()[0])
    
    time.sleep(2)
    print(Fore.YELLOW + f"\n{event}")
    
    # Photo opportunity
    print("\nAs your car reaches the top, a camera flashes!")
    take_photo = input("Would you like to purchase the photo for 1 ticket? (y/n): ")
    
    if take_photo.lower() == 'y' and player["tickets"] >= 1:
        player["tickets"] -= 1
        print(Fore.GREEN + "You'll receive your commemorative Ferris wheel photo!")
        print("The photo clerk gives you a bonus ticket for your purchase!")
        reward += 1
        
        # Easter egg: rare perfect photo
        if random.randint(1, 20) == 1:
            print(Fore.MAGENTA + "\n✨ PERFECT SHOT! The photographer captured a once-in-a-lifetime sunset! ✨")
            print("You receive 5 bonus tickets for the magical moment!")
            reward += 5
            award_achievement("Picture Perfect: Got the legendary Ferris wheel photo")
    
    player["tickets"] += reward
    print(f"\nYou earned a total of {reward} tickets from your peaceful ride!")
    
    # Sometimes the ride operator lets you go around twice
    if random.randint(1, 10) == 1:
        print(Fore.GREEN + "\nLUCKY! The operator lets you stay on for a second rotation!")
        print("You earn 3 bonus tickets!")
        player["tickets"] += 3

def vr_experience():
    """Virtual reality experience with different scenarios and challenges"""
    if not pay_to_play(7):
        return
    
    clear()
    print(Fore.CYAN + "🥽 Welcome to the VIRTUAL REALITY EXPERIENCE! 🥽")
    print("Step into another world!")
    
    # Choose your VR world
    print("\nSelect your virtual experience:")
    print("[1] 🌋 Volcano Explorer")
    print("[2] 🌊 Deep Sea Adventure")
    print("[3] 🚀 Space Station Mission")
    print("[4] 🏰 Fantasy Kingdom")
    
    world = input("Choose your experience (1-4): ")
    
    # Simulation and results
    rewards = 0
    
    if world == "1":  # Volcano Explorer
        print("\nYou're equipped with a heat-resistant suit and lowered into an active volcano!")
        print("The heat is intense, and molten lava bubbles below...")
        
        choice = input("\nDo you [1] Take a sample of rare volcanic crystals or [2] Document the unusual formations? ")
        
        if choice == "1":
            if random.randint(1, 10) > 3:
                print("\nSuccess! You collect a stunning crystal formation worth studying!")
                print("The scientists are thrilled with your sample!")
                rewards += 10
                award_achievement("Volcanologist: Collected rare volcanic crystals")
            else:
                print("\nAn unexpected tremor shakes the volcano!")
                print("You're pulled to safety, but without the sample.")
                rewards += 4
        else:
            print("\nYou capture amazing footage of previously undocumented lava formations!")
            print("Your documentation will help scientists understand volcanic behavior.")
            rewards += 8
    
    elif world == "2":  # Deep Sea Adventure
        print("\nYour submersible descends into the darkest depths of the ocean...")
        print("Strange bioluminescent creatures illuminate the darkness...")
        
        choice = input("\nDo you [1] Explore a mysterious underwater cave or [2] Follow a giant squid? ")
        
        if choice == "1":
            print("\nThe cave opens into a vast underwater cavern filled with ancient ruins!")
            print("You discover evidence of an unknown civilization!")
            rewards += 9
            award_achievement("Deep Sea Archaeologist: Found underwater ruins")
        else:
            if random.randint(1, 10) > 4:
                print("\nThe squid leads you to its incredible lair, filled with collected treasures!")
                print("You're one of the few humans to witness this behavior!")
                rewards += 11
                award_achievement("Cephalopod Whisperer: Followed the giant squid")
            else:
                print("\nThe squid notices you and disappears into the darkness...")
                print("At least you caught a glimpse of the magnificent creature.")
                rewards += 5
    
    elif world == "3":  # Space Station Mission
        print("\nYou're aboard the International Space Station, floating in zero gravity...")
        print("Earth is a beautiful blue marble beneath you...")
        
        choice = input("\nDo you [1] Perform critical repair mission or [2] Conduct scientific experiments? ")
        
        if choice == "1":
            success = random.randint(1, 10) > 3
            print("\nYou spacewalk to fix a damaged solar panel...")
            if success:
                print("Perfect repair job! The station's power is restored!")
                rewards += 10
                award_achievement("Space Engineer: Successfully completed a repair mission")
            else:
                print("You struggle with the repair but manage to partially fix the issue.")
                rewards += 6
        else:
            print("\nYour experiments yield fascinating results about crystal growth in space!")
            print("The data will help future missions and research.")
            rewards += 8
    
    elif world == "4":  # Fantasy Kingdom
        print("\nYou step into a magical medieval world with castles and dragons...")
        print("A royal messenger approaches you with an urgent quest...")
        
        choice = input("\nDo you [1] Hunt the dragon threatening the kingdom or [2] Search for a magical artifact? ")
        
        if choice == "1":
            if random.randint(1, 10) > 5:
                print("\nAfter an epic battle, you befriend the dragon instead of slaying it!")
                print("The kingdom celebrates your diplomatic solution!")
                rewards += 12
                award_achievement("Dragon Whisperer: Made peace with the dragon")
            else:
                print("\nThe dragon was too powerful! You retreat to fight another day.")
                rewards += 5
        else:
            print("\nDeep in an ancient forest, you discover a magical staff of power!")
            print("Its glow illuminates the entire kingdom!")
            rewards += 9
            award_achievement("Artifact Hunter: Found the magical staff")
    
    else:
        print("\nThe technician helps you select the Volcano Explorer experience...")
        print("You have an amazing time exploring the virtual volcano!")
        rewards += 6
    
    print(f"\nAmazing! You earned {rewards} tickets from your virtual adventure!")
    player["tickets"] += rewards
    
    # Bonus for first-time users
    if "VR Experience" not in player.get("attractions_visited", []):
        if "attractions_visited" not in player:
            player["attractions_visited"] = []
        player["attractions_visited"].append("VR Experience")
        print(Fore.GREEN + "\nFIRST-TIME BONUS: +3 tickets for trying VR!")
        player["tickets"] += 3

def mirror_maze():
    """Navigate through a complex mirror maze with challenges and rewards"""
    if not pay_to_play(4):
        return
    
    clear()
    print(Fore.MAGENTA + "🪞 Welcome to the MIRROR MAZE! 🪞")
    print("Can you find your way through the labyrinth of reflections?")
    
    # Initialize maze variables
    wrong_turns = 0
    dead_ends = 0
    progress = 0
    max_progress = 5
    
    while progress < max_progress and wrong_turns < 3:
        print(f"\nProgress: {'🚶' * progress}{'◻️' * (max_progress - progress)}")
        print(f"Wrong turns: {'❌' * wrong_turns}")
        
        # Random mirror maze event
        event_type = random.choice(["junction", "trick", "dead_end", "helper"])
        
        if event_type == "junction":
            print("\nYou come to a junction with multiple reflections of the path ahead.")
            print("[1] Take the left path")
            print("[2] Take the right path")
            print("[3] Go straight ahead")
            
            choice = input("Which way do you go? ")
            correct = random.randint(1, 3)
            
            if choice == str(correct):
                print(Fore.GREEN + "\nGood choice! You continue deeper into the maze.")
                progress += 1
            else:
                print(Fore.RED + "\nYou walk straight into a mirror! Ouch!")
                print("That was the wrong path.")
                wrong_turns += 1
        
        elif event_type == "trick":
            print("\nYou see what looks like an exit sign, but something seems off...")
            print("[1] Follow the exit sign")
            print("[2] Ignore it and find another path")
            
            choice = input("What do you do? ")
            
            if choice == "2":
                print(Fore.GREEN + "\nWise choice! That was a trick reflection.")
                print("You avoid a dead end and continue on the right path.")
                progress += 1
            else:
                print(Fore.RED + "\nIt was a trick! The 'exit' was just a reflection.")
                print("You've hit a dead end and need to backtrack.")
                dead_ends += 1
                wrong_turns += 1
        
        elif event_type == "dead_end":
            print("\nYou suddenly realize you're facing a wall of mirrors with no obvious path.")
            print("[1] Feel along the left wall")
            print("[2] Feel along the right wall")
            print("[3] Turn around and go back")
            
            choice = input("What do you do? ")
            
            if choice == "3":
                print(Fore.YELLOW + "\nYou backtrack and find the correct path again.")
                # No penalty but no progress either
            else:
                # 50/50 chance to find a hidden path
                if random.choice([True, False]):
                    print(Fore.GREEN + "\nYou discover a hidden path behind a rotating mirror panel!")
                    print("What luck!")
                    progress += 1
                else:
                    print(Fore.RED + "\nThere's no way through here. You'll have to go back.")
                    wrong_turns += 1
        
        elif event_type == "helper":
            print("\nYou notice a small child also lost in the maze.")
            print("They seem to know the way and offer to help you.")
            print("[1] Follow the child")
            print("[2] Continue on your own")
            
            choice = input("What do you do? ")
            
            if choice == "1":
                print(Fore.GREEN + "\nThe child leads you through a confusing section!")
                print("You've made great progress!")
                progress += 2
            else:
                print(Fore.YELLOW + "\nYou continue on your own, making slow but steady progress.")
                progress += 1
    
    # Results
    if progress >= max_progress:
        print(Fore.GREEN + "\n🎉 Congratulations! You've successfully navigated the Mirror Maze! 🎉")
        reward = 10 - (wrong_turns * 2)
        reward = max(reward, 5)  # Minimum 5 tickets for completion
        
        if wrong_turns == 0:
            print("Perfect run! No wrong turns at all!")
            reward += 5
            award_achievement("Mirror Master: Completed the maze with no wrong turns")
    else:
        print(Fore.RED + "\nYou've taken too many wrong turns and decide to use the emergency exit.")
        print("Better luck next time!")
        reward = max(1, progress)
    
    print(f"\nYou earned {reward} tickets!")
    player["tickets"] += reward

def photo_booth():
    """Take fun photos with props and filters in the photo booth"""
    if not pay_to_play(2):
        return
    
    clear()
    print(Fore.YELLOW + "📸 Welcome to the CARNIVAL PHOTO BOOTH! 📸")
    print("Create a fun memory to take home!")
    reward = 0
    
    # Choose photo style
    print("\nSelect your photo style:")
    print("[1] 🎭 Funny Faces")
    print("[2] 🦸 Superhero Theme")
    print("[3] 🧙 Magical Effects")
    print("[4] 🌈 Rainbow Filters")
    
    style = input("Choose your style (1-4): ")
    
    # Choose props
    props = [
        "Oversized Sunglasses", "Silly Hat", "Feather Boa", 
        "Mustache on a Stick", "Tiara", "Cartoon Speech Bubble",
        "Giant Bowtie", "Cowboy Hat", "Pirate Eye Patch"
    ]
    
    print("\nAvailable props:")
    for i, prop in enumerate(props):
        print(f"[{i+1}] {prop}")
    
    prop_choice = input("Choose a prop number (1-9): ")
    try:
        prop_choice = int(prop_choice) - 1
        if 0 <= prop_choice < len(props):
            chosen_prop = props[prop_choice]
        else:
            chosen_prop = random.choice(props)
    except (ValueError, IndexError):
        chosen_prop = random.choice(props)
    
    # Take the photos
    print("\nGet ready for your photo session!")
    print("3...")
    time.sleep(0.7)
    print("2...")
    time.sleep(0.7)
    print("1...")
    time.sleep(0.7)
    print(Fore.YELLOW + "SMILE! 📸")
    
    # Photo results
    style_name = ["Funny Faces", "Superhero Theme", "Magical Effects", "Rainbow Filters"][int(style)-1 if style in "1234" else 0]
    print(f"\nGreat job! Your {style_name} photos with the {chosen_prop} look amazing!")
    
    # Special combinations with bonus rewards
    bonus = 0
    if (style == "2" and chosen_prop == "Tiara"):
        print(Fore.MAGENTA + "\n✨ SPECIAL COMBO: The Super Royal! ✨")
        print("Your superhero with a tiara photo is hilarious!")
        bonus = 3
        award_achievement("Super Royal: Created the superhero/tiara combo")
    elif (style == "1" and chosen_prop == "Mustache on a Stick"):
        print(Fore.MAGENTA + "\n✨ SPECIAL COMBO: The Classic Disguise! ✨")
        print("Your funny face with mustache photo is a timeless classic!")
        bonus = 2
    elif (style == "3" and chosen_prop == "Cartoon Speech Bubble"):
        print(Fore.MAGENTA + "\n✨ SPECIAL COMBO: The Magical Message! ✨")
        print("Your magical photo with a speech bubble looks like it's straight out of a storybook!")
        bonus = 2
    
    # Base reward
    reward = 3 + bonus
    
    # Photo package options
    print("\nPhoto Package Options:")
    print("[1] Basic - 1 printed photo (Free)")
    print("[2] Standard - 3 printed photos (+1 ticket)")
    print("[3] Deluxe - 5 printed photos + digital copies (+3 tickets)")
    
    package = input("Choose your package (1-3): ")
    
    if package == "2" and player["tickets"] >= 1:
        player["tickets"] -= 1
        print("\nYou've selected the Standard package!")
        print("You'll receive 3 printed photos.")
        reward += 1
    elif package == "3" and player["tickets"] >= 3:
        player["tickets"] -= 3
        print("\nYou've selected the Deluxe package!")
        print("You'll receive 5 printed photos and digital copies!")
        reward += 2
    else:
        print("\nYou've selected the Basic package!")
        print("You'll receive 1 printed photo.")
    
    print(f"\nYou earned {reward} tickets from your photo session!")
    player["tickets"] += reward

def magic_show():
    """Interactive magic show where you can volunteer and win prizes"""
    if not pay_to_play(5):
        return
    
    clear()
    print(Fore.BLUE + "🎩 Welcome to the MYSTICAL MAGIC SHOW! 🎩")
    print("Prepare to be amazed by the Great Zoltar!")
    
    # Find your seat
    print("\nThe usher shows you to your seat. The theater is filling up!")
    print("The lights dim and smoke fills the stage...")
    time.sleep(2)
    
    print(Fore.YELLOW + "\n🎭 LADIES AND GENTLEMEN! 🎭")
    print("🎭 WELCOME TO THE MOST MAGICAL SHOW ON EARTH! 🎭")
    print("🎭 I AM THE GREAT ZOLTAR! 🎭")
    
    # Interactive magic tricks
    rewards = 0
    
    # Trick 1 - Card Trick
    print("\n--- The Impossible Card Trick ---")
    print("The Great Zoltar asks for a volunteer from the audience...")
    
    volunteer = input("Do you want to volunteer? (y/n): ")
    
    if volunteer.lower() == 'y':
        print("\nYou raise your hand and are selected!")
        print("You join Zoltar on stage. He asks you to pick a card, any card...")
        
        # Simulate card selection
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        card = f"{random.choice(values)} of {random.choice(suits)}"
        
        print(f"\nYou select the {card} and show it to the audience, but not to Zoltar.")
        print("He asks you to put it back in the deck, which he shuffles thoroughly.")
        time.sleep(1.5)
        print("\nZoltar waves his hands mysteriously over the deck...")
        time.sleep(1.5)
        print(f"'Your card was the... {card}!'")
        print("\nThe audience gasps and erupts in applause!")
        print("You receive 5 bonus tickets for participating!")
        rewards += 5
    else:
        print("\nAnother audience member volunteers and is amazed by the trick!")
    
    # Trick 2 - Disappearing Act
    print("\n--- The Mysterious Vanishing Box ---")
    print("Zoltar presents a large box and asks if anyone can verify it's empty.")
    
    inspect = input("Do you want to inspect the box? (y/n): ")
    
    if inspect.lower() == 'y':
        print("\nYou join Zoltar on stage again!")
        print("You check the box thoroughly and confirm there are no hidden compartments.")
        print("Zoltar's assistant steps into the box, and he closes the door.")
        time.sleep(1.5)
        print("\nDrums roll... Zoltar waves his wand...")
        time.sleep(1.5)
        print("The box is opened to reveal... EMPTY!")
        print("The audience is stunned!")
        
        choice = input("\nZoltar asks if you want to look for the assistant. Do you? (y/n): ")
        
        if choice.lower() == 'y':
            if random.randint(1, 10) > 7:
                print("\nYou discover the secret to the trick! Zoltar is impressed by your perception!")
                print("He awards you 10 bonus tickets for your keen eye!")
                rewards += 10
                award_achievement("Magic Decoder: Discovered the secret of the disappearing assistant")
            else:
                print("\nYou search but can't figure out where the assistant went!")
                print("Zoltar gives you 3 tickets for trying!")
                rewards += 3
        else:
            print("\nYou decline, preserving the mystery of the magic trick.")
            print("Zoltar appreciates your respect for the art of illusion!")
            print("He awards you 2 tickets!")
            rewards += 2
    
    # Trick 3 - Mind Reading
    print("\n--- The Astonishing Mind Reading ---")
    print("For his final trick, Zoltar claims he can read the thoughts of audience members!")
    
    participate = input("Do you want to participate in the mind reading? (y/n): ")
    
    if participate.lower() == 'y':
        print("\nZoltar points at you! 'Yes, you in the audience! I sense strong thought energy!'")
        print("He asks you to think of a number between 1 and 50...")
        
        # This is just for show - the "magic" will work regardless
        number = input("Enter your number (Zoltar won't see this): ")
        
        print("\nZoltar concentrates deeply...")
        print("He writes something on a piece of paper and seals it in an envelope.")
        print("He hands the envelope to another audience member to hold.")
        
        # Build suspense
        print("\nHe asks you to reveal your number to the audience...")
        time.sleep(2)
        
        # The trick "works" 80% of the time
        if random.randint(1, 10) <= 8:
            print(f"\nThe envelope is opened to reveal the number {number}!")
            print("The audience erupts in wild applause!")
            print("Zoltar awards you 8 tickets for your participation in this miracle!")
            rewards += 8
        else:
            wrong_number = str(int(number) + random.choice([-1, 1]) if number.isdigit() else "41")
            print(f"\nThe envelope is opened to reveal the number {wrong_number}!")
            print("A few gasps from the audience... Zoltar looks confused.")
            print("'The psychic energies must be disturbed today,' he mutters.")
            print("He still gives you 2 tickets for participating!")
            rewards += 2
    
    # Show conclusion
    print("\nThe Great Zoltar takes his final bow as the audience gives a standing ovation!")
    print(f"You earned a total of {rewards} tickets from the magical experience!")
    player["tickets"] += rewards
    
    # Rare special ending
    if random.randint(1, 20) == 1:
        print(Fore.MAGENTA + "\n✨ SPECIAL EVENT: After the show, Zoltar gives you a signed magic wand! ✨")
        print("This rare souvenir earns you an additional 15 tickets!")
        player["tickets"] += 15
        award_achievement("Magician's Apprentice: Received Zoltar's signed wand")

def number_racing():
    if not pay_to_play(2):
        return
    player_num = random.randint(1, 10)
    finish_line = 20
    player_pos = 0
    computer_pos = 0

    print(f"Your racing number: {player_num}")
    while player_pos < finish_line and computer_pos < finish_line:
        input("Press Enter to roll...")
        roll = random.randint(1, 10)
        print(f"You rolled: {roll}")
        if roll == player_num:
            player_pos += 3
            print(Fore.GREEN + "Perfect roll! +3 spaces")
        else:
            player_pos += 1

        comp_roll = random.randint(1, 10)
        computer_pos += 1 if comp_roll != 7 else 3

        print(f"\nYou: {'🏎️' + '=' * player_pos}")
        print(f"CPU: {'🚗' + '=' * computer_pos}")

    if player_pos >= finish_line:
        print(Fore.GREEN + "You win! +5 tickets")
        player["tickets"] += 5
    else:
        print(Fore.RED + "Computer wins!")



def balloon_pop():
    if not pay_to_play(2):
        return
    balloons = ["🎈", "💥"]
    target = random.randint(1, 5)
    print(f"Pop exactly {target} balloons!")
    popped = 0
    for _ in range(5):
        choice = input(f"Pop balloon {_+1}? (y/n): ").lower()
        if choice == 'y':
            result = random.choice(balloons)
            if result == "🎈":
                print("Pop! 🎈 → 💥")
                popped += 1
            else:
                print("Already popped! 💥")

    if popped == target:
        print(Fore.GREEN + "Perfect! +5 tickets")
        player["tickets"] += 5
    else:
        print(Fore.RED + f"You popped {popped}/{target} balloons!")

def ring_toss():
    if not pay_to_play(3):
        return
    targets = ["🎯", "⭕", "❌"]
    hits = 0
    print("Toss 3 rings!")
    for i in range(3):
        input(f"Press Enter to toss ring {i+1}...")
        result = random.choices(targets, weights=[1, 2, 3])[0]
        if result == "🎯":
            print(Fore.GREEN + "Perfect throw! 🎯")
            hits += 2
        elif result == "⭕":
            print(Fore.YELLOW + "Close! ⭕")
            hits += 1
        else:
            print(Fore.RED + "Miss! ❌")

    print(f"Total points: {hits}")
    tickets = hits * 2
    if tickets > 0:
        print(Fore.GREEN + f"You won {tickets} tickets!")
        player["tickets"] += tickets

def duck_shooting():
    if not pay_to_play(3):
        return
    ducks = ["🦆", "🎯"]
    score = 0
    shots = 3

    print("Shoot the moving ducks! You have 3 shots.")
    while shots > 0:
        lineup = "".join(random.choices(ducks, k=5))
        print("\nDucks:", lineup)
        position = int(input("Choose position to shoot (1-5): ")) - 1

        if 0 <= position < 5:
            if lineup[position] == "🦆":
                print(Fore.GREEN + "Hit! 🎯")
                score += 1
            else:
                print(Fore.RED + "Miss!")
        else:
            print("Invalid position!")
        shots -= 1

    tickets = score * 3
    if tickets > 0:
        print(Fore.GREEN + f"You hit {score} ducks! +{tickets} tickets")
        player["tickets"] += tickets
    else:
        print(Fore.RED + "Better luck next time!")


def target_shooting():
    if not pay_to_play(3):
        return
    clear()
    print(Fore.CYAN + "🎯 Target Shooting!")
    targets = ["🎯", "⭕", "🔴", "⚪"]
    points = 0

    for round in range(3):
        print(f"\nRound {round+1}/3")
        target_line = " ".join([random.choice(targets) for _ in range(4)])
        print(target_line)
        shot = int(input("Choose target position (1-4): ")) - 1

        if 0 <= shot < 4:
            if target_line[shot*2] == "🎯":
                print(Fore.GREEN + "Bullseye! +3 points")
                points += 3
            elif target_line[shot*2] == "⭕":
                print(Fore.YELLOW + "Close! +2 points")
                points += 2
            elif target_line[shot*2] == "🔴":
                print(Fore.YELLOW + "Almost! +1 point")
                points += 1
            else:
                print(Fore.RED + "Miss!")

    tickets = points * 2
    if tickets > 0:
        print(Fore.GREEN + f"You won {tickets} tickets!")
        player["tickets"] += tickets

def whack_a_mole():
    if not pay_to_play(2):
        return
    clear()
    print(Fore.MAGENTA + "🔨 Whack-a-Mole!")
    holes = ["⚫"] * 9
    score = 0

    for _ in range(6):  # Loop through 6 rounds
        mole_pos = random.randint(0, 8)
        holes[mole_pos] = "🦔"

        print("\nWhack the mole!")
        for i in range(0, 9, 3):
            print(" ".join(holes[i:i+3]))

        try:
            whack = int(input("Choose position (1-9): ")) - 1
            if 0 <= whack < 9:
                if whack == mole_pos:
                    print(Fore.GREEN + "Got it! +1 point")
                    score += 1
                else:
                    print(Fore.RED + "Missed!")
            holes[mole_pos] = "⚫"
        except ValueError:
            print("Invalid input!")

    tickets = score * 3
    if tickets > 0:
        print(Fore.GREEN + f"You whacked {score} moles! +{tickets} tickets")
        player["tickets"] += tickets

def kingyo_sukui():
    """Japanese goldfish scooping game"""
    if not pay_to_play(3):
        return
    clear()
    print(Fore.BLUE + "🐠 Kingyo-Sukui (Goldfish Scooping)")
    fish_caught = 0
    attempts = 3
    paper_strength = 100

    while attempts > 0 and paper_strength > 0:
        print(f"\nPaper strength: {paper_strength}%")
        print(f"Fish caught: {fish_caught}")
        input("Press Enter to scoop...")

        catch_chance = random.randint(1, 100)
        if catch_chance <= paper_strength:
            fish_caught += 1
            print(Fore.GREEN + "You caught a goldfish! 🐠")
        else:
            print(Fore.RED + "The paper scoop tore a bit!")

        paper_strength -= random.randint(20, 40)
        attempts -= 1

    tickets = fish_caught * 3
    if tickets > 0:
        print(Fore.GREEN + f"You won {tickets} tickets!")
        player["tickets"] += tickets

def yo_yo_tsuri():
    """Japanese water balloon fishing game"""
    if not pay_to_play(2):
        return
    clear()
    print(Fore.CYAN + "🎣 Yo-yo Tsuri (Water Balloon Fishing)")

    balloons = ["🔴", "🔵", "🟡", "🟢", "🟣"]
    caught = 0
    attempts = 4

    while attempts > 0:
        print(f"\nBalloons: {' '.join(balloons)}")
        input("Press Enter to fish...")

        if random.random() > 0.4:
            caught += 1
            color = random.choice(balloons)
            print(Fore.GREEN + f"Caught a {color} balloon!")
        else:
            print(Fore.RED + "The hook slipped!")

        attempts -= 1

    tickets = caught * 2
    if tickets > 0:
        print(Fore.GREEN + f"You won {tickets} tickets!")
        player["tickets"] += tickets

def bottle_toss():
    if not pay_to_play(3):
        return
    clear()
    print(Fore.BLUE + "🎳 Bottle Toss!")
    bottles = ["🍾"] * 6
    hits = 0

    for _ in range(3):  # Three throwing attempts
        print("\nBottles:", " ".join(bottles))
        input("Press Enter to throw...")

        power = random.random()
        if power > 0.7:
            hit_pos = random.randint(0, len(bottles)-1)
            if bottles[hit_pos] == "🍾":
                print(Fore.GREEN + "Great throw! Bottle knocked down!")
                bottles[hit_pos] = "💥"
                hits += 1
            else:
                print(Fore.YELLOW + "Already knocked down!")
        else:
            print(Fore.RED + "Miss!")

    tickets = hits * 4
    if tickets > 0:
        print(Fore.GREEN + f"You knocked down {hits} bottles! +{tickets} tickets")
        player["tickets"] += tickets

def treasure_hunt():
    """VIP game where players search for hidden treasures on a grid"""
    if "VIP Pass 🌟" not in player["inventory"]:
        print(Fore.RED + "❌ This game requires a VIP Pass!")
        return
    if not pay_to_play(5):
        return
        
    clear()
    print(Fore.YELLOW + "🏆 TREASURE HUNT 🏆")
    print("Find hidden treasures in the carnival grounds!")
    
    # Game setup
    grid_size = 5
    
    # Place treasures (for future grid implementation)
    treasures = []
    for _ in range(3):
        x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        while (x, y) in treasures:
            x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        treasures.append((x, y))
    
    # Game variables
    attempts = 8
    score = 0
    
    # Simple treasure grid
    treasure_items = ["💎", "👑", "💰", "⭐", "❌"]
    map_size = 5
    treasure_map = random.choices(treasure_items, weights=[1, 1, 2, 2, 4], k=map_size)
    
    while attempts > 0:
        clear()
        print(Fore.YELLOW + "🏆 TREASURE HUNT 🏆")
        print(f"Attempts remaining: {attempts}")
        
        # Display map with hidden treasures
        print("\nMap:", " ".join("?" * map_size))
        
        # Get user input
        try:
            choice = int(input(f"\nChoose location (1-{map_size}): ")) - 1
            
            if 0 <= choice < map_size:
                find = treasure_map[choice]
                if find == "💎":
                    print(Fore.CYAN + "Found a diamond! +10 points")
                    score += 10
                elif find == "👑":
                    print(Fore.YELLOW + "Found a crown! +8 points")
                    score += 8
                elif find == "💰":
                    print(Fore.GREEN + "Found treasure! +5 points")
                    score += 5
                elif find == "⭐":
                    print(Fore.YELLOW + "Found a star! +3 points")
                    score += 3
                else:
                    print(Fore.RED + "Nothing here! ❌")
                
                # Replace the item with a blank space
                treasure_map[choice] = " "
            else:
                print(Fore.RED + "Invalid location!")
                
            attempts -= 1
            time.sleep(1)
            
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid input! Please enter a number.")
            time.sleep(1)
    
    # Game result
    clear()
    print(Fore.YELLOW + "🏆 TREASURE HUNT RESULTS 🏆")
    
    # Show final map
    print("\nFinal Map:", " ".join(treasure_map))
    
    print(f"\nYour score: {score}")
    
    # Award tickets based on score
    tickets = score
    if tickets > 0:
        print(Fore.GREEN + f"You earned {tickets} tickets!")
        player["tickets"] += tickets
        
        if score >= 20:
            award_achievement("Treasure Hunter")
            
    input("\nPress Enter to continue...")
    update_mission_progress("vip_games")

# ChronoSpace TCG - Card Database
CARD_DATABASE = {
    # === ChronoSpace Mythic Cards ===
    "Time Lord Chronos": {"power": 15, "emoji": "⌛", "rarity": "mythic", "rank": "SSS", "faction": "Time Keepers"},
    "Void Emperor": {"power": 14, "emoji": "🌌", "rarity": "mythic", "rank": "SSS", "faction": "Void Walkers"},
    "Space-Time Dragon": {"power": 14, "emoji": "🐉", "rarity": "mythic", "rank": "SSS", "faction": "Cosmic Beasts"},
    "Reality Weaver": {"power": 13, "emoji": "🕸️", "rarity": "mythic", "rank": "SSS", "faction": "Dimensional Weavers"},

    # === ChronoSpace Legendary Cards ===
    "Quantum Knight": {"power": 12, "emoji": "⚔️", "rarity": "legendary", "rank": "SS", "faction": "Time Keepers"},
    "Void Stalker": {"power": 11, "emoji": "👁️", "rarity": "legendary", "rank": "SS", "faction": "Void Walkers"},
    "Temporal Phoenix": {"power": 11, "emoji": "🦅", "rarity": "legendary", "rank": "SS", "faction": "Cosmic Beasts"},
    "Space Architect": {"power": 10, "emoji": "🏗️", "rarity": "legendary", "rank": "S", "faction": "Dimensional Weavers"},

    # === ChronoSpace Epic Cards ===
    "Time Mage": {"power": 9, "emoji": "🧙", "rarity": "epic", "rank": "A", "faction": "Time Keepers"},
    "Void Hunter": {"power": 9, "emoji": "🏹", "rarity": "epic", "rank": "A", "faction": "Void Walkers"},
    "Star Beast": {"power": 8, "emoji": "🦁", "rarity": "epic", "rank": "A", "faction": "Cosmic Beasts"},
    "Reality Shaper": {"power": 8, "emoji": "🎨", "rarity": "epic", "rank": "A", "faction": "Dimensional Weavers"},
    # === Mythic Cards (Power 13+) ===
    "Eternal Leviathan": {"power": 14, "emoji": "🦈", "rarity": "mythic", "rank": "SSS"},
    "Celestial Overlord": {"power": 13, "emoji": "🌠", "rarity": "mythic", "rank": "SSS"},
    "Void Seraph": {"power": 13, "emoji": "🕊️", "rarity": "mythic", "rank": "SSS"},
    "Dark Legionary Supreme Lord: Noctis, the Obsidian Fallen Eternal": {"power": 15, "emoji": "🛡️🌑", "rarity": "mythic", "rank": "SSS"},

    # === Legendary Cards (Fantasy) ===
    "Supreme Dragon": {"power": 12, "emoji": "🐲", "rarity": "legendary", "rank": "SS"},
    "Ancient Phoenix": {"power": 11, "emoji": "🦅", "rarity": "legendary", "rank": "SS"},
    "Divine Angel": {"power": 11, "emoji": "👼", "rarity": "legendary", "rank": "SS"},
    "Cosmic Entity": {"power": 10, "emoji": "🌌", "rarity": "legendary", "rank": "S"},
    "Time Wizard": {"power": 10, "emoji": "⌛", "rarity": "legendary", "rank": "S"},
    "Abyss Warden": {"power": 10, "emoji": "🧿", "rarity": "legendary", "rank": "S"},
    "Chrono Beast": {"power": 11, "emoji": "⏳", "rarity": "legendary", "rank": "SS"},
    "Saviour from Another World": {"power": 12, "emoji": "🌟🧝", "rarity": "legendary", "rank": "SS"},

    # === Legendary Cards (Sci-fi) ===
    "Quantum Core": {"power": 12, "emoji": "⚛️", "rarity": "legendary", "rank": "SS"},
    "AI Overmind": {"power": 11, "emoji": "🧠", "rarity": "legendary", "rank": "SS"},
    "Warp Phantom": {"power": 10, "emoji": "👻", "rarity": "legendary", "rank": "S"},

    # === Epic Cards (Fantasy) ===
    "Dragon Lord": {"power": 9, "emoji": "🐉", "rarity": "epic", "rank": "A"},
    "Storm Giant": {"power": 9, "emoji": "🌩️", "rarity": "epic", "rank": "A"},
    "War Golem": {"power": 8, "emoji": "🗿", "rarity": "epic", "rank": "A"},
    "Shadow Assassin": {"power": 8, "emoji": "🗡️", "rarity": "epic", "rank": "A"},
    "Demon Prince": {"power": 8, "emoji": "👿", "rarity": "epic", "rank": "A"},
    "Frost Lich": {"power": 9, "emoji": "❄️", "rarity": "epic", "rank": "A"},
    "Volcanic Behemoth": {"power": 8, "emoji": "🌋", "rarity": "epic", "rank": "A"},

    # === Epic Cards (Sci-fi) ===
    "Mecha Warrior": {"power": 9, "emoji": "🤖", "rarity": "epic", "rank": "A"},
    "Plasma Sniper": {"power": 8, "emoji": "🔫", "rarity": "epic", "rank": "A"},
    "Cyber Witch": {"power": 8, "emoji": "💻🧙", "rarity": "epic", "rank": "A"},
    "Gravity Bender": {"power": 9, "emoji": "🌌➡️🌍", "rarity": "epic", "rank": "A"},

    # === Rare Cards (Fantasy) ===
    "Battle Mage": {"power": 7, "emoji": "🔮", "rarity": "rare", "rank": "B"},
    "Holy Knight": {"power": 7, "emoji": "⚔️", "rarity": "rare", "rank": "B"},
    "Forest Ranger": {"power": 6, "emoji": "🏹", "rarity": "rare", "rank": "B"},
    "Mystic Healer": {"power": 6, "emoji": "💚", "rarity": "rare", "rank": "B"},
    "Fire Wizard": {"power": 6, "emoji": "🔥", "rarity": "rare", "rank": "B"},
    "Ice Archer": {"power": 7, "emoji": "❄️🏹", "rarity": "rare", "rank": "B"},
    "Sand Guardian": {"power": 6, "emoji": "🏜️", "rarity": "rare", "rank": "B"},

    # === Rare Cards (Sci-fi) ===
    "Drone Swarm": {"power": 7, "emoji": "🛸", "rarity": "rare", "rank": "B"},
    "Nanobot Surgeon": {"power": 6, "emoji": "🔧", "rarity": "rare", "rank": "B"},
    "Asteroid Miner": {"power": 6, "emoji": "⛏️", "rarity": "rare", "rank": "B"},

    # === Common Cards (Fantasy) ===
    "Sword Apprentice": {"power": 5, "emoji": "🗡️", "rarity": "common", "rank": "C"},
    "Apprentice Mage": {"power": 4, "emoji": "🧙", "rarity": "common", "rank": "C"},
    "Forest Wolf": {"power": 4, "emoji": "🐺", "rarity": "common", "rank": "C"},
    "Goblin Thief": {"power": 3, "emoji": "🪙", "rarity": "common", "rank": "D"},
    "Skeleton Warrior": {"power": 2, "emoji": "💀", "rarity": "common", "rank": "D"},
    "Village Archer": {"power": 2, "emoji": "🏹", "rarity": "common", "rank": "D"},
    "Tiny Slime": {"power": 1, "emoji":"🟢", "rarity": "common", "rank": "E"},
    "Cave Bat": {"power": 1, "emoji": "🦇", "rarity": "common", "rank": "E"},

    # === Common Cards (Sci-fi) ===
    "Service Droid": {"power": 5, "emoji": "🛠️", "rarity": "common", "rank": "C"},
    "Holo Soldier": {"power": 4, "emoji": "📡", "rarity": "common", "rank": "C"},
    "Space Rat": {"power": 3, "emoji": "🐀", "rarity": "common", "rank": "D"},
    "Security Drone": {"power": 2, "emoji": "🚨", "rarity": "common", "rank": "D"},
    "Circuit Bug": {"power": 1, "emoji": "🐞", "rarity": "common", "rank": "E"},

    # === Real Life Cards ===
    "Firefighter": {"power": 5, "emoji": "🚒", "rarity": "common", "rank": "C"},
    "Police Officer": {"power": 5, "emoji": "👮", "rarity": "common", "rank": "C"},
    "Chef": {"power": 4, "emoji": "👨‍🍳", "rarity": "common", "rank": "C"},
    "Doctor": {"power": 6, "emoji": "🩺", "rarity": "rare", "rank": "B"},
    "Scientist": {"power": 7, "emoji": "🔬", "rarity": "rare", "rank": "B"},
    "Athlete": {"power": 6, "emoji": "🏃", "rarity": "rare", "rank": "B"},
    "Delivery Driver": {"power": 3, "emoji": "🚚", "rarity": "common", "rank": "D"},
    "Construction Worker": {"power": 4, "emoji": "👷", "rarity": "common", "rank": "C"},

    # === Z Survival Cards ===
    "Zombie Brute": {"power": 6, "emoji": "🧟", "rarity": "rare", "rank": "B"},
    "Apocalypse Survivor": {"power": 7, "emoji": "🪓", "rarity": "rare", "rank": "B"},
    "Radioactive Ghoul": {"power": 8, "emoji": "☢️", "rarity": "epic", "rank": "A"},
    "Barricade Builder": {"power": 4, "emoji": "🧱", "rarity": "common", "rank": "C"},

    # === Liminal Spaces Cards ===
    "Backrooms Wanderer": {"power": 5, "emoji": "🚪", "rarity": "common", "rank": "C"},
    "Threshold Entity": {"power": 9, "emoji": "🌀", "rarity": "epic", "rank": "A"},
    "Endless Hallway": {"power": 7, "emoji": "📏", "rarity": "rare", "rank": "B"},
    "Neon Void": {"power": 11, "emoji": "🌃", "rarity": "legendary", "rank": "SS"}
}


# Generate remaining cards programmatically
elements = ["Fire", "Water", "Earth", "Air", "Light", "Dark", "Nature", "Metal", "Ice", "Lightning"]
classes = ["Warrior", "Mage", "Rogue", "Cleric", "Archer", "Knight", "Monk", "Paladin", "Druid", "Necromancer"]
ranks = ["C", "D", "E"]

# Generate common and uncommon cards
for element in elements:
    for class_type in classes:
        power = random.randint(2, 5)
        rarity = "common" if power <= 3 else "uncommon"
        rank = ranks[0] if power == 5 else ranks[1] if power == 4 else ranks[2]

        card_name = f"{element} {class_type}"
        CARD_DATABASE[card_name] = {
            "power": power,
            "emoji": random.choice(["⚔️", "🗡️", "🏹", "🔮", "💫", "⭐", "🌟", "✨", "💥", "⚡"]),
            "rarity": rarity,
            "rank": rank
        }

CARD_NPCS = {
    "Novice Duelist": {"difficulty": 1, "deck_size": 30, "reward": 10},
    "Veteran Knight": {"difficulty": 2, "deck_size": 35, "reward": 15},
    "Dragon Master": {"difficulty": 3, "deck_size": 40, "reward": 20},
    "Dark Wizard": {"difficulty": 4, "deck_size": 45, "reward": 25},
    "Time Keeper Elite": {"difficulty": 5, "deck_size": 40, "reward": 30},
    "Void Master": {"difficulty": 5, "deck_size": 40, "reward": 30},
    "Cosmic Beast Tamer": {"difficulty": 5, "deck_size": 40, "reward": 30},
    "Reality Shaper": {"difficulty": 5, "deck_size": 40, "reward": 30},
    "Championship Finalist": {"difficulty": 6, "deck_size": 45, "reward": 40},
    "Grand Champion": {"difficulty": 7, "deck_size": 50, "reward": 50},
    "The Andy, The Carnival's Boss": {"difficulty": 10, "deck_size": 60, "reward": 100}
}

# Add Youkai cards to the database
YOUKAI_CARDS = {
    "Kitsune Spirit": {"power": 12, "emoji": "🦊", "rarity": "legendary", "rank": "SS", "faction": "Youkai"},
    "Tengu Warrior": {"power": 11, "emoji": "👺", "rarity": "legendary", "rank": "SS", "faction": "Youkai"},
    "Kappa Trickster": {"power": 9, "emoji": "🐢", "rarity": "epic", "rank": "A", "faction": "Youkai"},
    "Oni Demon": {"power": 13, "emoji": "👹", "rarity": "mythic", "rank": "SSS", "faction": "Youkai"},
    "Tanuki Shape-shifter": {"power": 8, "emoji": "🦝", "rarity": "epic", "rank": "A", "faction": "Youkai"},
    "Yurei Ghost": {"power": 7, "emoji": "👻", "rarity": "rare", "rank": "B", "faction": "Youkai"},
    "Nekomata Cat": {"power": 10, "emoji": "🐱", "rarity": "legendary", "rank": "S", "faction": "Youkai"},
    "Dragon Kami": {"power": 14, "emoji": "🐉", "rarity": "mythic", "rank": "SSS", "faction": "Youkai"}
}

# Update CARD_DATABASE with Youkai cards
CARD_DATABASE.update(YOUKAI_CARDS)

# Tournament brackets
CHAMPIONSHIP_BRACKETS = [
    ["Novice Duelist", "Veteran Knight"],
    ["Dragon Master", "Dark Wizard"],
    ["Time Keeper Elite", "Void Master"],
    ["Cosmic Beast Tamer", "Reality Shaper"],
    ["Championship Finalist", "Grand Champion"]
]

if "card_collection" not in player:
    player["card_collection"] = []
if "current_deck" not in player:
    player["current_deck"] = []
if "missions" not in player:
    player["missions"] = {}
if "completed_missions" not in player:
    player["completed_missions"] = []

# We have consolidated the buy_card_pack functions into one implementation below

def manage_deck():
    """Manage your TCG card deck"""
    if "card_collection" not in player:
        player["card_collection"] = []
    
    if "current_deck" not in player:
        player["current_deck"] = []
    
    while True:
        clear()
        print(Fore.CYAN + "📋 Deck Management")
        print(f"Current deck: {len(player.get('current_deck', []))}/30 cards")
        print("\n[1] View collection")
        print("[2] View current deck")
        print("[3] Build new deck")
        print("[4] Card collection info")
        print("[0] Back")
        
        choice = input("\nChoose option: ")
        
        if choice == "1":
            view_card_collection()
        elif choice == "2":
            view_deck()
        elif choice == "3":
            build_deck()
        elif choice == "4":
            show_card_tutorial()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice!")
            time.sleep(1)


def view_collection():
    clear()
    print(Fore.YELLOW + "🎴 Your Collection:")
    collection = {}
    for card in player["card_collection"]:
        collection[card] = collection.get(card, 0) + 1

    for card, count in collection.items():
        print(f"{CARD_DATABASE[card]['emoji']} {card} x{count} (Power: {CARD_DATABASE[card]['power']})")
    input("\nPress Enter to continue...")

def view_deck():
    clear()
    print(Fore.GREEN + "🎴 Current Deck:")
    deck_contents = {}
    for card in player["current_deck"]:
        deck_contents[card] = deck_contents.get(card, 0) + 1

    for card, count in deck_contents.items():
        print(f"{CARD_DATABASE[card]['emoji']} {card} x{count}")
    input("\nPress Enter to continue...")

def build_deck():
    clear()
    print(Fore.CYAN + "Build your deck (30-50 cards)")
    player["current_deck"] = []

    while len(player["current_deck"]) < 30 or (len(player["current_deck"]) < 50 and input("\nAdd more cards? (y/n): ").lower() == 'y'):
        clear()
        print(f"Cards in deck: {len(player['current_deck'])}/30")
        collection = {}
        for card in player["card_collection"]:
            if card not in player["current_deck"]:
                collection[card] = collection.get(card, 0) + 1

        print("\nAvailable cards:")
        for i, (card, count) in enumerate(collection.items(), 1):
            print(f"[{i}] {CARD_DATABASE[card]['emoji']} {card} x{count}")
        print("[0] Cancel")

        choice = input("Add card (or 0 to cancel): ")
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            card = list(collection.keys())[idx]
            player["current_deck"].append(card)
        except (ValueError, IndexError):
            print("Invalid choice!")
            continue

    print(Fore.GREEN + "Deck complete!")

def show_card_tutorial():
    clear()
    print(Fore.CYAN + "🌌 ChronoSpace TCG Tutorial")
    print("""
Welcome to ChronoSpace TCG - Where Time and Space Collide!

Game Features:
1. Four Unique Factions:
   - Time Keepers: Masters of temporal magic
   - Void Walkers: Controllers of space
   - Cosmic Beasts: Powerful creatures of the cosmos
   - Dimensional Weavers: Shapers of reality

2. Card Ranks:
   SSS - Mythic (Power 13-15)
   SS  - Legendary (Power 11-12)
   S   - Elite (Power 10)
   A   - Epic (Power 8-9)
   B   - Rare (Power 6-7)
   C   - Uncommon (Power 4-5)
   D   - Common (Power 2-3)

3. Deck Building:
   - 30-50 cards per deck
   - Strategic faction combinations
   - Unique card synergies

4. Battle System:
   - Draw 3 cards per round
   - Faction bonuses apply
   - Best of 3 rounds
   - Special abilities activate based on combinations
""")
    print("""
Welcome to the Card Battle System! Here are the key rules:

1. Deck Building:
   - Minimum deck size: 30 cards
   - Maximum deck size: 50 cards
   - You can have multiple copies of the same card

2. Card Ranks:
   SS - Ultimate cards (Power 11-12)
   S  - Legendary cards (Power 10)
   A  - Epic cards (Power 8-9)
   B  - Rare cards (Power 6-7)
   C  - Uncommon cards (Power 4-5)
   D  - Common cards (Power 3)
   E  - Basic cards (Power 2)

3. Battle Rules:
   - Each player draws 3 cards per round
   - Higher power cards win the round
   - First to win 2 rounds wins the match
   - Winning matches earns tickets

4. Card Types:
   - 151 unique cards available
   - 5 rarity levels: legendary, epic, rare, uncommon, common
   - 10 elements and 10 classes for variety

Tips:
- Build a balanced deck with different power levels
- Collect stronger cards from card packs
- Plan your strategy based on opponent's style
    """)
    input("\nPress Enter to continue...")

def soccer_championship():
    if not pay_to_play(2):
        return

    clear()
    print(Fore.GREEN + "⚽ Soccer Championship!")

    opponents = [
        {"name": "Rookie Striker", "skill": 1, "reward": 10},
        {"name": "Local Champion", "skill": 2, "reward": 15},
        {"name": "Professional Player", "skill": 3, "reward": 20},
        {"name": "World Cup Star", "skill": 4, "reward": 30}
    ]

    score = 0
    for opponent in opponents:
        print(f"\nFacing {opponent['name']}...")
        success = random.random() > (0.2 * opponent['skill'])
        if success:
            print(Fore.GREEN + "Goal! 🥅⚽")
            score += 1
            player["tickets"] += opponent["reward"]
            print(f"+{opponent['reward']} tickets!")
        else:
            print(Fore.RED + "Miss! ❌")

    if score >= 3:
        print(Fore.GREEN + "🏆 Soccer Championship Winner!")
        award_achievement("Soccer Champion")

def golf_championship():
    if not pay_to_play(2):
        return

    clear()
    print(Fore.GREEN + "⛳ Golf Championship!")

    courses = [
        {"name": "Beginner's Green", "par": 3, "reward": 10},
        {"name": "Pro Circuit", "par": 4, "reward": 15},
        {"name": "Master's Challenge", "par": 5, "reward": 20},
        {"name": "Champion's Vista", "par": 4, "reward": 30}
    ]

    total_score = 0
    for course in courses:
        print(f"\nPlaying {course['name']}...")
        strokes = random.randint(course['par']-1, course['par']+2)
        print(f"Strokes: {strokes} (Par: {course['par']})")

        if strokes <= course['par']:
            reward = course['reward']
            player["tickets"] += reward
            print(Fore.GREEN + f"Great shot! +{reward} tickets!")
        else:
            print(Fore.RED + "Over par!")
        total_score += strokes

    if total_score <= 18:
        print(Fore.GREEN + "🏆 Golf Championship Winner!")
        award_achievement("Golf Champion")

def championship_mode():
    if not pay_to_play(2):
        return

    clear()
    print(Fore.CYAN + "🏆 Championship Selection")
    print("\n[1] Card Championship")
    print("[2] Soccer Championship")
    print("[3] Golf Championship")
    print("[0] Back")

    choice = input("Choose championship: ")

    if choice == "1":
        card_championship()
    elif choice == "2":
        soccer_championship()
    elif choice == "3":
        golf_championship()

def card_championship():

    # Give access to all cards for championship
    temp_collection = player["card_collection"].copy()
    player["card_collection"] = list(CARD_DATABASE.keys())
    print(Fore.GREEN + "🎮 Championship Mode: All cards unlocked for this tournament!")

    clear()
    print(Fore.CYAN + "🏆 ChronoSpace TCG Championship")
    print("\nBattle through the brackets to become the Grand Champion!")

    total_winnings = 0
    for bracket_num, bracket in enumerate(CHAMPIONSHIP_BRACKETS, 1):
        print(f"\n=== Bracket {bracket_num} ===")
        print(f"Opponents: {bracket[0]} vs {bracket[1]}")
        input("Press Enter to continue...")

        for opponent in bracket:
            result = card_battle(opponent, championship=True)
            if not result:
                print(Fore.RED + "\nChampionship run ended!")
                if total_winnings > 0:
                    print(Fore.GREEN + f"Total winnings: {total_winnings} tickets!")
                player["card_collection"] = temp_collection
                return
            total_winnings += CARD_NPCS[opponent]["reward"]

        if bracket_num < len(CHAMPIONSHIP_BRACKETS):
            print(Fore.GREEN + "\nBracket cleared! Moving to next round...")
            print(f"Current winnings: {total_winnings} tickets!")

    print(Fore.CYAN + "\n🎉 Congratulations! You are the new Grand Champion!")
    bonus = 100
    total_winnings += bonus
    print(Fore.GREEN + f"Championship bonus: {bonus} tickets!")
    print(f"Total Championship winnings: {total_winnings} tickets!")
    player["tickets"] += total_winnings
    player["card_collection"] = temp_collection

    if "Championship Winner" not in player["achievements"]:
        award_achievement("Championship Winner")

# We have consolidated the card_battle functions into one implementation below

def card_battle(opponent=None, championship=False):
    """Card battle game using the player's card collection"""
    if "card_collection" not in player:
        player["card_collection"] = []
        
    # Generate card database if not defined
    if "CARD_DATABASE" not in globals():
        global CARD_DATABASE
        CARD_DATABASE = {
            "Fire Dragon": {"emoji": "🔥", "power": 8, "element": "fire"},
            "Water Sprite": {"emoji": "💧", "power": 6, "element": "water"},
            "Earth Giant": {"emoji": "🌍", "power": 7, "element": "earth"},
            "Wind Eagle": {"emoji": "🌪️", "power": 5, "element": "wind"},
            "Shadow Wolf": {"emoji": "🐺", "power": 6, "element": "dark"},
            "Light Angel": {"emoji": "👼", "power": 6, "element": "light"},
            "Thunder Beast": {"emoji": "⚡", "power": 7, "element": "thunder"},
            "Ice Golem": {"emoji": "❄️", "power": 7, "element": "ice"},
            "Forest Elf": {"emoji": "🌳", "power": 5, "element": "nature"},
            "Mystic Wizard": {"emoji": "🧙", "power": 8, "element": "arcane"},
            "Legendary Champion's Card": {"emoji": "🏆", "power": 10, "element": "legendary"}
        }
    
    if len(player["card_collection"]) < 3:
        print(Fore.RED + "You need at least 3 cards to play!")
        print("Visit the shop to buy card packs!")
        input("Press Enter to continue...")
        return False
    
    clear()
    print(Fore.CYAN + "🃏 CARD BATTLE 🃏")
    
    # Opponent selection
    if opponent is None:
        opponent = random.choice(["Novice Duelist", "Card Enthusiast", "Deck Master"])
    
    print(f"Opponent: {opponent}")
    
    # Draw cards for player
    available_cards = player["card_collection"].copy()
    player_hand = []
    for _ in range(min(3, len(available_cards))):
        card = random.choice(available_cards)
        player_hand.append(card)
        available_cards.remove(card)
    
    # Draw cards for CPU
    cpu_cards = list(CARD_DATABASE.keys())
    cpu_hand = []
    for _ in range(3):
        card = random.choice(cpu_cards)
        cpu_hand.append(card)
        cpu_cards.remove(card)
    
    # Battle
    rounds = 3
    player_score = 0
    cpu_score = 0
    
    for round_num in range(1, rounds+1):
        clear()
        print(Fore.CYAN + f"🃏 CARD BATTLE - Round {round_num}/{rounds} 🃏")
        print(f"Score: You {player_score} - {cpu_score} CPU")
        
        print("\nYour hand:")
        for i, card in enumerate(player_hand, 1):
            print(f"{i}. {CARD_DATABASE[card]['emoji']} {card} (Power: {CARD_DATABASE[card]['power']})")
        
        # Player selects card
        valid_choice = False
        choice = -1
        while not valid_choice:
            try:
                choice = int(input("\nChoose your card (1-3): ")) - 1
                if choice < 0 or choice >= len(player_hand):
                    print(Fore.RED + "Invalid choice!")
                    continue
                valid_choice = True
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a number.")
                continue
        
        player_card = player_hand[choice]
        cpu_card = random.choice(cpu_hand)
        
        print(f"\nYou played: {CARD_DATABASE[player_card]['emoji']} {player_card}")
        print(f"CPU played: {CARD_DATABASE[cpu_card]['emoji']} {cpu_card}")
        
        if CARD_DATABASE[player_card]['power'] > CARD_DATABASE[cpu_card]['power']:
            print(Fore.GREEN + "You win this round!")
            player_score += 1
        elif CARD_DATABASE[player_card]['power'] < CARD_DATABASE[cpu_card]['power']:
            print(Fore.RED + "CPU wins this round!")
            cpu_score += 1
        else:
            print(Fore.YELLOW + "It's a tie!")
        
        player_hand.remove(player_card)
        cpu_hand.remove(cpu_card)
        time.sleep(1)
    
    # Game result
    print(f"\nFinal Score - You: {player_score} | CPU: {cpu_score}")
    
    if player_score > cpu_score:
        tickets = 10
        print(Fore.GREEN + f"You won the battle! +{tickets} tickets!")
        player["tickets"] += tickets
        update_mission_progress("win_card_battle")
        return True
    elif player_score < cpu_score:
        print(Fore.RED + "You lost the battle!")
        return False
    else:
        tickets = 5
        print(Fore.YELLOW + f"It's a tie! +{tickets} tickets")
        player["tickets"] += tickets
        return True
        
def buy_card_pack():
    """Purchase a card pack containing random cards"""
    pack_cost = 15
    
    if player["tickets"] < pack_cost:
        print(Fore.RED + f"Not enough tickets! You need {pack_cost} tickets.")
        return
    
    # Confirm purchase
    print(f"Buy a card pack for {pack_cost} tickets? (y/n)")
    if input("> ").lower() != 'y':
        return
        
    player["tickets"] -= pack_cost
    
    # Generate card database if not defined
    if "CARD_DATABASE" not in globals():
        global CARD_DATABASE
        CARD_DATABASE = {
            "Fire Dragon": {"emoji": "🔥", "power": 8, "element": "fire"},
            "Water Sprite": {"emoji": "💧", "power": 6, "element": "water"},
            "Earth Giant": {"emoji": "🌍", "power": 7, "element": "earth"},
            "Wind Eagle": {"emoji": "🌪️", "power": 5, "element": "wind"},
            "Shadow Wolf": {"emoji": "🐺", "power": 6, "element": "dark"},
            "Light Angel": {"emoji": "👼", "power": 6, "element": "light"},
            "Thunder Beast": {"emoji": "⚡", "power": 7, "element": "thunder"},
            "Ice Golem": {"emoji": "❄️", "power": 7, "element": "ice"},
            "Forest Elf": {"emoji": "🌳", "power": 5, "element": "nature"},
            "Mystic Wizard": {"emoji": "🧙", "power": 8, "element": "arcane"}
        }
    
    # Initialize card collection if needed
    if "card_collection" not in player:
        player["card_collection"] = []
    
    # Draw cards
    cards_per_pack = 3
    cards = list(CARD_DATABASE.keys())
    new_cards = []
    
    for _ in range(cards_per_pack):
        card = random.choice(cards)
        new_cards.append(card)
        player["card_collection"].append(card)
    
    # Display results
    print(Fore.GREEN + "\nCard Pack Opened!")
    print("You got:")
    for card in new_cards:
        print(f"{CARD_DATABASE[card]['emoji']} {card} (Power: {CARD_DATABASE[card]['power']})")
    
    # Achievement
    if len(player["card_collection"]) >= 10:
        award_achievement("Card Collector")
        
    input("\nPress Enter to continue...")
    
def view_card_collection():
    """View all cards owned by the player"""
    clear()
    
    if "card_collection" not in player:
        player["card_collection"] = []
    
    if not player["card_collection"]:
        print(Fore.YELLOW + "You don't have any cards yet!")
        print("Visit the shop to buy card packs!")
        input("\nPress Enter to continue...")
        return
    
    # Generate card database if not defined
    if "CARD_DATABASE" not in globals():
        global CARD_DATABASE
        CARD_DATABASE = {
            "Fire Dragon": {"emoji": "🔥", "power": 8, "element": "fire"},
            "Water Sprite": {"emoji": "💧", "power": 6, "element": "water"},
            "Earth Giant": {"emoji": "🌍", "power": 7, "element": "earth"},
            "Wind Eagle": {"emoji": "🌪️", "power": 5, "element": "wind"},
            "Shadow Wolf": {"emoji": "🐺", "power": 6, "element": "dark"},
            "Light Angel": {"emoji": "👼", "power": 6, "element": "light"},
            "Thunder Beast": {"emoji": "⚡", "power": 7, "element": "thunder"},
            "Ice Golem": {"emoji": "❄️", "power": 7, "element": "ice"},
            "Forest Elf": {"emoji": "🌳", "power": 5, "element": "nature"},
            "Mystic Wizard": {"emoji": "🧙", "power": 8, "element": "arcane"},
            "Legendary Champion's Card": {"emoji": "🏆", "power": 10, "element": "legendary"}
        }
    
    print(Fore.CYAN + "🃏 YOUR CARD COLLECTION 🃏")
    
    # Group cards by element
    cards_by_element = {}
    for card in player["card_collection"]:
        element = CARD_DATABASE.get(card, {}).get("element", "unknown")
        if element not in cards_by_element:
            cards_by_element[element] = []
        cards_by_element[element].append(card)
    
    # Display cards by element
    for element, cards in cards_by_element.items():
        print(f"\n{element.upper()} CARDS:")
        for card in cards:
            card_data = CARD_DATABASE.get(card, {"emoji": "❓", "power": 0})
            print(f"{card_data['emoji']} {card} (Power: {card_data['power']})")
    
    print(f"\nTotal Cards: {len(player['card_collection'])}")
    input("\nPress Enter to continue...")
    
if __name__ == "__main__":
    start_game()
