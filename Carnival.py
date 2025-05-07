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
import time
from colorama import Fore, init
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
    "completed_missions": []  # Completed mission IDs
}

MISSIONS = {
    "rookie": {"id": "rookie", "name": "Play 5 minigames", "target": 5, "reward": 10, "type": "play_games"},
    "mathematician": {"id": "mathematician", "name": "Win Quick Math 3 times", "target": 3, "reward": 15, "type": "win_quick_math"},
    "lucky": {"id": "lucky", "name": "Win Lucky Spinner 3 times", "target": 3, "reward": 20, "type": "win_spinner"},
    "vip_games": {"id": "vip_games", "name": "Play all VIP games", "target": 3, "reward": 50, "type": "vip_games", "vip_only": True}
}

NPCS = {
    "Carnival Master 🎪": {"missions": ["rookie"]},
    "Math Wizard 🧙‍♂️": {"missions": ["mathematician"]},
    "Lucky Luke 🍀": {"missions": ["lucky"]},
    "VIP Host 👑": {"missions": ["vip_games"], "vip_only": True}
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
    "VIP Pass 🌟": {"price": 100, "discount": 0.7, "uses": 1}
}

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
    print("[0] Back")

    choice = input("Choose category: ")

    if choice == "1":
        shop_costumes()
    elif choice == "2":
        shop_consumables()
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
[18] Back
""")
        choice = input("Select: ")
        games = [paper_scissors_rock, coin_flip_game, high_low, guess_the_number, 
                quick_math, word_shuffle, lucky_spinner, dart_throw, reaction_test, 
                melody_memory, guess_password, hangman_game, memory_match, number_racing,
                balloon_pop, ring_toss, duck_shooting]
        if choice == "18":
            break
        elif choice in map(str, range(1, 15)):
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
    elif choice == "0":
        return
    else:
        print("Invalid.")

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

def main_menu():
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
        print(carnival_art)
        print(f"👤 {player['equipped_costume']} {player['name']} | 🎟️ Tickets: {player['tickets']}")
        print("🎒 Inventory:", ", ".join(player["inventory"]) or "Empty")
        print("⚡ Active Items:", ", ".join(player["equipped_items"]) or "None")
        print("🏆 Achievements:", ", ".join(player["achievements"]) or "None")
        print("📋 Active Missions:", len(player["missions"]))
        print("""
[1] Play Minigames
[2] Ticket Shop
[3] Save Game
[4] Load Game
[5] Tutorials
[6] Gambling Games
[7] Talk to NPCs
[8] Exit
""")
        choice = input("Select option: ")
        if choice == "1":
            minigame_menu()
        elif choice == "2":
            shop()
        elif choice == "3":
            save_menu()
        elif choice == "4":
            load_menu()
        elif choice == "5":
            tutorials()
        elif choice == "6":
            gambling_menu()
        elif choice == "7":
            talk_to_npcs()
        elif choice == "8":
            print("Thanks for playing!")
            break
        else:
            print("Invalid.")

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
