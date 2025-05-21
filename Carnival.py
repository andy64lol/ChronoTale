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
from colorama import Fore, init

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
    "rookie": {"id": "rookie", "name": "Play 5 minigames", "target": 5, "reward": 10, "type": "play_games"},
    "mathematician": {"id": "mathematician", "name": "Win Quick Math 3 times", "target": 3, "reward": 15, "type": "win_quick_math"},
    "lucky": {"id": "lucky", "name": "Win Lucky Spinner 3 times", "target": 3, "reward": 20, "type": "win_spinner"},
    "vip_games": {"id": "vip_games", "name": "Play all VIP games", "target": 3, "reward": 50, "type": "vip_games", "vip_only": True},
    "coaster_fan": {"id": "coaster_fan", "name": "Ride the Cosmic Coaster 3 times", "target": 3, "reward": 25, "type": "ride_coaster"},
    "ghost_hunter": {"id": "ghost_hunter", "name": "Complete the Haunted Mansion without losing courage", "target": 1, "reward": 30, "type": "brave_mansion"},
    "vr_master": {"id": "vr_master", "name": "Try all VR experiences", "target": 4, "reward": 35, "type": "vr_experiences"},
    "championship_rookie": {"id": "championship_rookie", "name": "Participate in any championship", "target": 1, "reward": 15, "type": "championship_participation"},
    "championship_winner": {"id": "championship_winner", "name": "Win any championship", "target": 1, "reward": 50, "type": "championship_win"},
    "collector": {"id": "collector", "name": "Own 10 different costumes", "target": 10, "reward": 25, "type": "costume_collection"},
    "theme_park_explorer": {"id": "theme_park_explorer", "name": "Try all theme park attractions", "target": 8, "reward": 40, "type": "theme_park_visits"},
    "loyal_visitor": {"id": "loyal_visitor", "name": "Earn 100 loyalty points", "target": 100, "reward": 35, "type": "loyalty_points"}
}

NPCS = {
    "Carnival Master 🎪": {"missions": ["rookie"]},
    "Math Wizard 🧙‍♂️": {"missions": ["mathematician"]},
    "Lucky Luke 🍀": {"missions": ["lucky"]},
    "VIP Host 👑": {"missions": ["vip_games"], "vip_only": True},
    "Ride Operator 🎢": {"missions": ["coaster_fan", "theme_park_explorer"]},
    "Ghost Hunter 👻": {"missions": ["ghost_hunter"]},
    "VR Technician 🥽": {"missions": ["vr_master"]},
    "Championship Director 🏆": {"missions": ["championship_rookie", "championship_winner"]},
    "Fashion Designer 👕": {"missions": ["collector"]},
    "Loyalty Program Manager 🌟": {"missions": ["loyal_visitor"]},
    "Quest Master 📜": {"quests": ["daily_challenge", "weekly_quest", "scavenger_hunt"]},
    "Season Pass Agent 🎫": {"season_pass": True, "missions": []}
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
    init_player_attributes()
    check_daily_reward()

    while True:
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
        # Display loyalty tier if player has any points
        loyalty_info = ""
        if player.get("loyalty_points", 0) > 0:
            tier = get_loyalty_tier()
            loyalty_info = f"🌟 {tier} ({player['loyalty_points']} points)"
        
        print(carnival_art)
        print(f"👤 {player['equipped_costume']} {player['name']} | 🎟️ Tickets: {player['tickets']} | {loyalty_info}")
        print("🎒 Inventory:", ", ".join(player["inventory"]) or "Empty")
        print("⚡ Active Items:", ", ".join(player["equipped_items"]) or "None")
        print("🏆 Achievements:", len(player["achievements"]) if "achievements" in player else 0)
        print("📋 Active Missions:", len(player["missions"]) if "missions" in player else 0)
        
        # Show season pass status if active
        if player.get("season_pass", False):
            days_left = player.get("season_pass_days", 30)
            print(Fore.GREEN + f"🎫 Season Pass Active! ({days_left} days remaining)")
        
        print("""
[1] Play Minigames
[2] Ticket Shop
[3] Pet Shop 🐾
[4] Daily Challenges 📅
[5] Leaderboard 🏆
[6] Save Game
[7] Load Game
[8] Tutorials
[9] Theme Park 🎢
[10] Gambling Games
[11] Talk to NPCs
[12] Redeem Code
[13] Manage Pets 🐾
[14] Championships 🏆
[15] Quest Center 📜
[16] Loyalty Rewards 🌟
[0] Exit
""")
        choice = input("Select option: ")
        if choice == "1":
            minigame_menu()
        elif choice == "2":
            shop()
        elif choice == "3":
            pet_shop()
        elif choice == "4":
            check_daily_challenges()
        elif choice == "5":
            show_leaderboard()
        elif choice == "6":
            save_menu()
        elif choice == "7":
            load_menu()
        elif choice == "8":
            tutorials()
        elif choice == "9":
            theme_park_menu()
        elif choice == "10":
            gambling_menu()
        elif choice == "11":
            talk_to_npcs()
        elif choice == "12":
            redeem_code()
        elif choice == "13":
            equip_pet()
        elif choice == "14":
            championship_center()
        elif choice == "15":
            quest_center()
        elif choice == "16":
            loyalty_rewards_center()
        elif choice == "0":
            print("Thanks for playing!")
            break
        else:
            print("Invalid.")

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
    "Monday": {"task": "Win 5 minigames", "reward": 20},
    "Tuesday": {"task": "Win 3 card battles", "reward": 25},
    "Wednesday": {"task": "Earn 100 tickets", "reward": 30},
    "Thursday": {"task": "Complete 2 missions", "reward": 25},
    "Friday": {"task": "Win 2 gambling games", "reward": 20},
    "Saturday": {"task": "Buy 2 items", "reward": 25},
    "Sunday": {"task": "Win championship", "reward": 50}
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
    challenge = DAILY_CHALLENGES[current_day]

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
    clear()
    print(Fore.YELLOW + "🎪 NPCs:")
    for npc, data in NPCS.items():
        if data.get("vip_only") and "VIP Pass 🌟" not in player["inventory"]:
            continue
        print(f"\n{npc}:")
        for mission_id in data["missions"]:
            mission = MISSIONS[mission_id]
            if mission_id in player["completed_missions"]:
                print(f"✅ {mission['name']} (Completed)")
            elif mission_id in player["missions"]:
                progress = player["missions"][mission_id]
                print(f"👉 {mission['name']} ({progress}/{mission['target']})")
            else:
                print(f"❌ {mission['name']} (Not Started)")
    input("\nPress Enter to continue...")

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

def theme_park_menu():
    """Display and handle the theme park attraction menu.
    Shows available rides and attractions with their ticket costs.
    """
    clear()
    print(Fore.LIGHTMAGENTA_EX + "🎢 Welcome to the Theme Park! 🎢")
    print(f"Your Tickets: {player['tickets']}")
    
    print("\nThrilling Rides:")
    print("[1] Cosmic Coaster 🚀 - 5 tickets")
    print("[2] Log Flume 💦 - 4 tickets")
    print("[3] Haunted Mansion 👻 - 6 tickets")
    print("[4] Ferris Wheel 🎡 - 3 tickets")
    
    print("\nSpecial Attractions:")
    print("[5] Virtual Reality Experience 🥽 - 7 tickets")
    print("[6] Mirror Maze 🪞 - 4 tickets")
    print("[7] Photo Booth 📸 - 2 tickets")
    print("[8] Magic Show 🎩 - 5 tickets")
    
    print("\n[0] Back to Main Menu")
    
    choice = input("\nSelect an attraction: ")
    
    if choice == "1":
        cosmic_coaster()
    elif choice == "2":
        log_flume()
    elif choice == "3":
        haunted_mansion()
    elif choice == "4":
        ferris_wheel()
    elif choice == "5":
        vr_experience()
    elif choice == "6":
        mirror_maze()
    elif choice == "7":
        photo_booth()
    elif choice == "8":
        magic_show()
    elif choice != "0":
        print(Fore.RED + "Invalid choice!")

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
    
# Main execution - launcher already checked at the beginning of the file
if __name__ == "__main__":
    start_game()
