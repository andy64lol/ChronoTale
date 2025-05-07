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
[21] 👑 Treasure Hunt (VIP) (5)
[22] 👑 Card Battle (VIP) (5)
[23] Back
""")
        choice = input("Select: ")
        games = [paper_scissors_rock, coin_flip_game, high_low, guess_the_number, 
                quick_math, word_shuffle, lucky_spinner, dart_throw, reaction_test, 
                melody_memory, guess_password, hangman_game, memory_match, number_racing,
                balloon_pop, ring_toss, duck_shooting]
        if choice == "22":
            break
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
    
    for round in range(6):
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

def bottle_toss():
    if not pay_to_play(3):
        return
    clear()
    print(Fore.BLUE + "🎳 Bottle Toss!")
    bottles = ["🍾"] * 6
    hits = 0
    
    for throw in range(3):
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
    if "VIP Pass 🌟" not in player["inventory"]:
        print(Fore.RED + "❌ This game requires a VIP Pass!")
        return
    if not pay_to_play(5):
        return
        
    clear()
    print(Fore.YELLOW + "💎 VIP Treasure Hunt!")
    treasures = ["💎", "👑", "💰", "⭐", "❌"]
    map_size = 5
    treasure_map = random.choices(treasures, weights=[1, 1, 2, 2, 4], k=map_size)
    attempts = 3
    score = 0
    
    while attempts > 0:
        print(f"\nAttempts left: {attempts}")
        print("Map:", " ".join("?" * map_size))
        choice = int(input(f"Choose location (1-{map_size}): ")) - 1
        
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
        else:
            print(Fore.RED + "Invalid location!")
            
        attempts -= 1
    
    tickets = score
    if tickets > 0:
        print(Fore.GREEN + f"You earned {tickets} tickets!")
        player["tickets"] += tickets
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
    "Tiny Slime": {"power": 1, "emoji": "🟢", "rarity": "common", "rank": "E"},
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
    "Novice Duelist": {"difficulty": 1, "deck_size": 30},
    "Veteran Knight": {"difficulty": 2, "deck_size": 35},
    "Dragon Master": {"difficulty": 3, "deck_size": 40},
    "Dark Wizard": {"difficulty": 4, "deck_size": 45}
}

if "card_collection" not in player:
    player["card_collection"] = []
    player["current_deck"] = []

def buy_card_pack():
    pack_cost = 10
    if player["tickets"] < pack_cost:
        print(Fore.RED + f"Not enough tickets! Need {pack_cost} tickets.")
        return
    
    player["tickets"] -= pack_cost
    cards = []
    for _ in range(5):
        rarity = random.choices(["common", "uncommon", "rare", "legendary"], 
                              weights=[60, 25, 10, 5])[0]
        possible_cards = [card for card, data in CARD_DATABASE.items() 
                         if data["rarity"] == rarity]
        card = random.choice(possible_cards)
        cards.append(card)
        player["card_collection"].append(card)
    
    print(Fore.GREEN + "\nYou got:")
    for card in cards:
        print(f"{CARD_DATABASE[card]['emoji']} {card} ({CARD_DATABASE[card]['rarity']})")

def manage_deck():
    while True:
        clear()
        print(Fore.CYAN + "📋 Deck Management")
        print(f"Current deck: {len(player['current_deck'])}/30 cards")
        print("\n[1] View collection")
        print("[2] Build new deck")
        print("[3] View current deck")
        print("[0] Back")
        
        choice = input("Choose option: ")
        if choice == "1":
            view_collection()
        elif choice == "2":
            build_deck()
        elif choice == "3":
            view_deck()
        elif choice == "0":
            break

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

def card_battle():
    if len(player["current_deck"]) < 30:
        print(Fore.RED + "⚠️ You need a deck of at least 30 cards to play ChronoSpace TCG!")
        print(Fore.YELLOW + "Would you like to see the tutorial? (y/n)")
        if input().lower() == 'y':
            show_card_tutorial()
        return

    clear()
    print(Fore.CYAN + "🌌 Welcome to ChronoSpace TCG!")
    print(Fore.YELLOW + "\nChoose your opponent:")
    
    npcs = {
        "Apprentice Time Keeper": {"difficulty": 1, "deck_size": 30, "faction": "Time Keepers"},
        "Void Walker Initiate": {"difficulty": 2, "deck_size": 35, "faction": "Void Walkers"},
        "Beast Master": {"difficulty": 3, "deck_size": 40, "faction": "Cosmic Beasts"},
        "Reality Architect": {"difficulty": 4, "deck_size": 45, "faction": "Dimensional Weavers"}
    }
    
    for i, (npc, data) in enumerate(npcs.items(), 1):
        print(f"[{i}] {npc} ({data['faction']})")
        print(Fore.YELLOW + "Type 'tutorial' to learn the rules, or press Enter to exit.")
        if input().lower() == 'tutorial':
            show_card_tutorial()
        return
        
    clear()
    print(Fore.YELLOW + "🎴 Card Battle!")
    
    print("\nChoose opponent:")
    for i, (npc, data) in enumerate(CARD_NPCS.items(), 1):
        print(f"[{i}] {npc}")
    
    try:
        choice = int(input("Select opponent: ")) - 1
        opponent = list(CARD_NPCS.keys())[choice]
    except (ValueError, IndexError):
        print("Invalid choice!")
        return
        
    print(f"\nBattling against {opponent}!")
    npc_deck = []
    for _ in range(CARD_NPCS[opponent]["deck_size"]):
        npc_deck.append(random.choice(list(CARD_DATABASE.keys())))
    
    player_hand = random.sample(list(CARD_DATABASE.keys()), 3)
    cpu_hand = random.sample(list(CARD_DATABASE.keys()), 3)
    
    player_score = 0
    cpu_score = 0
    rounds = 3
    
    for round in range(rounds):
        print(f"\nRound {round + 1}/{rounds}")
        print("\nYour cards:")
        for i, card in enumerate(player_hand, 1):
            print(f"[{i}] {CARD_DATABASE[card]['emoji']} {card} (Power: {CARD_DATABASE[card]['power']})")
            
        choice = int(input("\nChoose your card (1-3): ")) - 1
        if choice < 0 or choice >= len(player_hand):
            print(Fore.RED + "Invalid choice!")
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
        
    print(f"\nFinal Score - You: {player_score} | CPU: {cpu_score}")
    
    if player_score > cpu_score:
        tickets = 10
        print(Fore.GREEN + f"You won the battle! +{tickets} tickets!")
        player["tickets"] += tickets
        update_mission_progress("vip_games")
    elif player_score < cpu_score:
        print(Fore.RED + "You lost the battle!")
    else:
        tickets = 5
        print(Fore.YELLOW + f"It's a tie! +{tickets} tickets")
        player["tickets"] += tickets
