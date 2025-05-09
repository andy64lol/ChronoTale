import random
import os
import sys
import time
import pickle
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Game settings
X_MIN, X_MAX = -50, 50
Y_MIN, Y_MAX = -50, 50
Z_MIN, Z_MAX = -5, 5
SAVE_DIR = 'saves'
MAX_SLOTS = 5
SANITY_MAX = 100
MIN_HEAVEN_DOOR_DISTANCE = 10

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Directions mapping
directions = {
    '/right': (1, 0, 0),
    '/left': (-1, 0, 0),
    '/forward': (0, 1, 0),
    '/backward': (0, -1, 0),
    '/upstairs': (0, 0, 1),
    '/downstairs': (0, 0, -1)
}

doors = ['door1', 'door2', 'door3', 'door4']

class Room:
    def __init__(self, theme=None, level=1):
        self.theme = theme if theme else random.choice(['hospital', 'school', 'home', 'limbo', 'mall'])
        self.level = level
        self.generate_description()

    def generate_description(self):
        # Theme-based descriptions
        theme_descriptions = {
            'hospital': [
                (Fore.CYAN + "A sterile hospital room with medical equipment frozen in time." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.RED + "A blood-stained operating theater with flickering lights." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.LIGHTGREEN_EX + "A doctor's office with patient files scattered about." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.WHITE + "A hospital corridor stretches out before you, chairs lining the walls." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.LIGHTBLACK_EX + "A hospital reception area, the receptionist missing from her desk." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTRED_EX + "A trauma room with red-stained sheets and haunting monitors." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.YELLOW + "A pediatric ward with empty cribs and disconnected life support." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.BLUE + "An MRI room, the machine humming with no one inside it." + Style.RESET_ALL, ['door1', 'door3'])
            ],
            'school': [
                (Fore.LIGHTYELLOW_EX + "A school classroom where the blackboard writes by itself." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A gymnasium with basketballs that bounce on their own." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.BLUE + "A science lab with experiments that continue without supervision." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.CYAN + "A school cafeteria with food that moves on its plates." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.RED + "A detention room where desk graffiti shifts and changes." + Style.RESET_ALL, ['door1']),
                (Fore.MAGENTA + "A music room where instruments play themselves softly." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.WHITE + "A locker room with lockers that open and close on their own." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTBLACK_EX + "The principal's office with commendations for students who never existed." + Style.RESET_ALL, ['door2'])
            ],
            'home': [
                (Fore.MAGENTA + "A child's bedroom where toys move when you're not looking." + Style.RESET_ALL, ['door1']),
                (Fore.LIGHTBLACK_EX + "A dusty attic filled with forgotten relics." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.YELLOW + "A living room with a TV showing only static." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.BLUE + "A bathroom with a mirror that reflects a different person." + Style.RESET_ALL, ['door1']),
                (Fore.CYAN + "A kitchen where the refrigerator hums an eerie melody." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A dining room with place settings for people who aren't there." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.RED + "A basement with strange markings on the concrete walls." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.WHITE + "A study filled with books written in incomprehensible languages." + Style.RESET_ALL, ['door2', 'door3'])
            ],
            'limbo': [
                (Fore.WHITE + "A mirrored room that reflects impossible angles." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.LIGHTBLUE_EX + "A frozen cavern shimmering with ice crystals." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.LIGHTMAGENTA_EX + "A wall of photos and memories that feel like your own." + Style.RESET_ALL, ['door2']),
                (Fore.LIGHTBLACK_EX + "An endless void with floating debris of forgotten memories." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.CYAN + "A room where gravity doesn't work consistently." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A forest clearing inside an enclosed room, complete with a sky." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.YELLOW + "A room where time moves visibly backwards." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.RED + "A chamber where your thoughts materialize as whispers in the air." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'mall': [
                (Fore.BLUE + "An endless corridor with doors that seem to breathe." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.GREEN + "An overgrown indoor garden where plants whisper secrets." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.YELLOW + "A library where books write themselves." + Style.RESET_ALL, ['door1', 'door2', 'door4']),
                (Fore.LIGHTRED_EX + "A food court where meals appear and disappear on their own." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.CYAN + "A clothing store with mannequins that change position." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.MAGENTA + "A toy store where the toys observe you carefully." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.WHITE + "An electronics store with screens showing your past." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTBLACK_EX + "A cinema playing movies of your life you don't remember." + Style.RESET_ALL, ['door1', 'door2'])
            ],
            'Train_station': [
                (Fore.BLUE + "A train station with trains that never arrive." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A platform where the echoes of footsteps linger." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.YELLOW + "A waiting room with chairs that shift positions." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTRED_EX + "A ticket booth that dispenses tickets to nowhere." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.CYAN + "An empty train car that feels like a memory." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.MAGENTA + "A control room with screens showing distorted images." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.WHITE + "A maintenance area filled with tools that hum softly." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.LIGHTBLACK_EX + "An underground tunnel that seems to stretch forever." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.RED + "A undergroud railway where blood is spilled everywhere and the faces of the corpses distorts" + Style.RESET_ALL, ['door1', 'door2'])
            ],
            'Abandoned_amusement_park': [
                (Fore.BLUE + "An abandoned roller coaster with a broken track." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A funhouse with mirrors that show distorted reflections." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.YELLOW + "A carnival game booth with prizes that seem to watch you." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTRED_EX + "A Ferris wheel that creaks ominously with doors in the middle of the sky leading to nowhere." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.CYAN + "A clown's tent filled with laughter that echoes eerily." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.MAGENTA + "A food stand with food made up of human parts that seems to move on its own..." + Style.RESET_ALL, ['door2', 'door4'])
            ]
        }

        # Theme-based features
        theme_features = {
            'hospital': [
                "There's an emergency stairwell leading up.",
                "A service elevator shaft descends into darkness.",
                "Both the patient and staff stairwells are accessible.",
                "No exit signs can be seen.",
                "A worn hospital staircase winds upwards.",
                "A broken hospital gurney blocks the stairs."
            ],
            'school': [
                "There's a staircase to the upper floor classrooms.",
                "A dark stairwell leads to the basement level.",
                "Both main and emergency staircases are visible.",
                "No fire exit signs can be seen.",
                "A spiral staircase leads to the library tower.",
                "Blocked stairs with 'Do Not Enter' tape lead nowhere."
            ],
            'home': [
                "There's a carpeted staircase leading to the upper floor.",
                "A cellar door opens to stairs descending below.",
                "Both the main stairs and a ladder to the attic are visible.",
                "No way up or down from this floor.",
                "A vintage spiral staircase winds to the upper level.",
                "Half-collapsed stairs lead to nowhere safe."
            ],
            'limbo': [
                "There's a floating staircase suspended in midair.",
                "A dark pit seems to lead downward forever.",
                "Staircases spiral both upward and downward impossibly.",
                "No conventional paths up or down exist here.",
                "A spiral of light seems to lead upwards.",
                "Broken fragments of stairs hang in the air."
            ],
            'mall': [
                "There's an escalator leading to the upper level.",
                "A down escalator leads to the lower concourse.",
                "Both up and down escalators are operational.",
                "No directory signs indicate other levels.",
                "A decorative spiral staircase leads to a mezzanine.",
                "The mall map shows stairs that aren't there."
            ],
            'Train_station': [
                "There's a staircase leading to the platform above.",
                "A dark stairwell leads to the underground tracks.",
                "Both main and emergency staircases are visible.",
                "No fire exit signs can be seen.",
                "A spiral staircase leads to the observation deck.",
                "Blocked stairs with 'Do Not Enter' tape lead nowhere.",
                "A staircase in the middle of the railways",
                "A station with weird paintings of people you knew,but their faces seem very distorted..."
            ],
            'Abandoned_amusement_park': [
                "A staircase leading to the top of the fun house",
                "A dark stairwell leading to nowhere.",
                "Both main and emergency staircases are visible and they collide into one,bending at impossible angles you've never seen...",
                "No fire exit signs can be seen near an emergency door of the park,which leads to a wall...",
                "A spiral staircase leads to the pirate ship.",
                "Blocked stairs with 'Only authorised personel' tape that lead nowhere but a wall.",
                "A staircase in the middle of the seats of the circus that doesn't make sense...",
                "A mirror maze with refelections of people you knew,but their faces seem very distorted..."
            ]
        }

        # Theme-based paths
        theme_paths = {
            'hospital': [
                "Hospital corridors extend in all directions.",
                "Only the patient wing and administration area are accessible.",
                "Left leads to radiology, right to the ICU.",
                "A single hallway continues forward.",
                "A narrow service passage leads left.",
                "A wide main corridor stretches ahead."
            ],
            'school': [
                "School hallways extend in all directions.",
                "Only forward to the gym and backward to the entrance are clear.",
                "Left corridor leads to classrooms, right to administration.",
                "A single hallway continues forward.",
                "A narrow pathway leads left to the library.",
                "A wide main hall stretches ahead."
            ],
            'home': [
                "Doorways lead to other rooms in all directions.",
                "Only forward to the living room and backward to the foyer are clear.",
                "Left door leads to the kitchen, right to the bedroom.",
                "A single doorway continues forward.",
                "A narrow passage leads left to the pantry.",
                "A wide entryway opens ahead."
            ],
            'limbo': [
                "Impossible pathways extend in all directions.",
                "Only forward and backward seem to lead somewhere tangible.",
                "Left leads to darkness, right to blinding light.",
                "A single shimmering path continues forward.",
                "A narrow thread of reality twists to the left.",
                "A wide avenue of memories stretches ahead."
            ],
            'mall': [
                "Shopping concourses extend in all directions.",
                "Only the main concourse and entrance are clear.",
                "Left leads to the department store, right to boutiques.",
                "A single walkway continues forward.",
                "A hallway that bends into impossible angles",
                "A narrow service corridor twists to the left.",
                "A wide shopping promenade stretches ahead.",
                "A restaurant area with large restaurants that you feel like you've eaten here before.",
                "A food court with a strange smell that makes you feel sick.",
                "A mall with a strange clock that seems to be broken and counting randomly."
            ],
            'Train_station': [
                "Train platforms extend in all directions.",
                "Only the main platform and entrance are clear.",
                "Left leads to the ticket booth, right to the waiting area.",
                "A single walkway continues forward.",
                "A narrow service corridor twists to the left.",
                "A wide platform stretches ahead.",
                "A train floting while colisioning against the wall.",
                "A hallway that seems like a the insides of a train car.",
                "A train station with a weird clock that seems to be broken and counting randomly."
            ],
            'Abandoned_amusement_park':[
                "A deserted fun ride that seems infinite",
                "A circus with a fake clown that seems to be real",
                "A roller coaster that seems to be broken",
                "A hallway from a fun house",
                "Platforms of the park that seem to be floating forming a path",
                "Distorted bathroom hallway that seems to have infinite stalls",
                "A food court with a familiar yet decilious smell of fast food brands that never existed"
            ]
        }

        # Theme-based interactables
        theme_interactables = {
            'hospital': [
                ("A patient's chart hangs on the wall.", "The chart has your name on it..."),
                ("A medical monitor flickers with vitals.", "The heartbeat matches your own exactly..."),
                ("A wheelchair sits empty in the corner.", "It slowly begins to move on its own..."),
                ("A bottle of medication sits on the counter.", "The prescription is made out to you..."),
                ("An IV drip stands beside an empty bed.", "The fluid in the bag turns red as you watch..."),
                ("A surgical mask lies discarded on the floor.", "It smells of antiseptic and something else..."),
                ("A set of X-rays are clipped to a lightboard.", "They show a skull with something inside it..."),
                None
            ],
            'school': [
                ("An old yearbook lies open on a desk.", "Your photo is on every page, getting older..."),
                ("A chalkboard covered in equations.", "The math solves a problem about your life..."),
                ("A school trophy cabinet.", "Your name appears and disappears on the plaques..."),
                ("A student's backpack left behind.", "It contains homework with your handwriting..."),
                ("A test paper on the teacher's desk.", "Every answer is written in blood..."),
                ("A detention slip with your name on it.", "It details a crime you don't remember committing..."),
                ("A row of lockers.", "One has your name on it with scratches around the lock..."),
                ("A note pinned to the wall.", "It reads 'You will never escape from us,nerd'..."),
                ("A broken clock on the wall.", "It ticks make you remember of something urgent you needed to do..."),
                ("A row of student lockers.", "One has your name on it with scratches around the lock..."),
                None
            ],
            'home': [
                ("An old TV flickers with static.", "The TV shows glimpses of your past..."),
                ("A rusty music box sits on a table.", "The melody brings tears to your eyes..."),
                ("A dusty photo album lies open.", "The photos show memories you'd forgotten..."),
                ("A home movie plays on a projector.", "You're in the film but don't remember it being taken..."),
                ("A child's drawing is pinned to the refrigerator.", "It depicts a dark figure standing behind a family..."),
                ("A landline phone that begins to ring.", "When you answer, you hear your own voice..."),
                ("A broken clock on the wall.", "It ticks makes you remember of █████████████,and ████████████████..."),
                None
            ],
            'limbo': [
                ("A mirror reflects a different room.", "Your reflection seems wrong somehow..."),
                ("A broken clock ticks erratically.", "Time seems distorted here..."),
                ("A locked chest sits in the corner.", "It hums with mysterious energy..."),
                ("A faded painting depicts a forgotten landscape.", "The scene shifts as you watch..."),
                ("A floating orb of swirling memories.", "You see faces you've never met yet recognize..."),
                ("A door standing alone without walls.", "Through the keyhole, you see yourself sleeping..."),
                ("A strange artifact that pulses with light.", "It seems to respond to your thoughts..."),
                ("A wall of photos and memories.", "They feel like your own but are not..."),
                ("A door that leads to nowhere.", "It opens to a void that whispers your name...you better not cross it..."),
                ("A floating object that seems to be a mirror.", "It shows you a different version of yourself..."),
                ("A phone opened with distorted text you can't recognise...", "It seems to be a post in social media about you..."),
                None
            ],
            'mall': [
                ("A store mannequin in an unusual pose.", "Its head turns slightly to watch you..."),
                ("A mall directory with a 'You Are Here' marker.", "The marker moves when you look away..."),
                ("A food court tray with a half-eaten meal.", "Steam still rises from it as if just abandoned..."),
                ("A store security camera.", "It follows your movement too precisely..."),
                ("A bright sale sign flashing discounts.", "The text briefly changes to personal messages for you..."),
                ("A vending machine with strange products.", "Items inside have your face on the packaging..."),
                ("A shopping cart that rolls away on its own.", "It seems to be leading you somewhere..."),
                None
            ],
            'Train_station': [
                ("A train schedule board with your name.", "The next train is always 'now'..."),
                ("A ticket machine that dispenses blank tickets.", "The tickets show places you've never been..."),
                ("A waiting bench with a strange inscription.", "It reads 'You will never leave'..."),
                ("A train conductor's hat left behind.", "It feels warm as if someone just wore it..."),
                ("A train car filled with fog.", "You hear whispers of your name inside..."),
                ("A station clock that ticks backward.", "Time seems to unravel around it..."),
                ("A corpse with blood in the middle of the rails", "The face seems distorted but yet familiar..."),
                None
            ],
            'Abandoned_amusement_park': [
                ("A broken ride with a strange inscription.", "It reads 'You will never leave'..."),
                ("A clown's mask left behind.", "It seems to be watching you..."),
                ("A ticket booth with a strange inscription.", "It reads 'You will never leave'..."),
                ("A funhouse mirror that distorts your reflection.", "You see a version of yourself that isn't you..."),
                ("A carousel with horses that seem to move on their own.", "They look like people you know..."),
                ("A Ferris wheel that creaks ominously.", "The view from the top shows a different world..."),
                ("A toy clown with a distorted face", "It seems to be watching you..."),
            ]
        }

        # Select descriptions based on theme
        base_descriptions = theme_descriptions.get(self.theme, theme_descriptions['limbo'])
        features = theme_features.get(self.theme, theme_features['limbo'])
        paths = theme_paths.get(self.theme, theme_paths['limbo'])
        interactables = theme_interactables.get(self.theme, theme_interactables['limbo'])

        # Higher-level rooms have more complex descriptions
        if self.level > 25:
            # Add more disturbing elements for higher levels
            base_descriptions = [(desc[0] + Fore.RED + " Something feels very wrong here." + Style.RESET_ALL, desc[1]) for desc in base_descriptions]

        self.description, self.doors = random.choice(base_descriptions)
        self.stairs = random.choice(features)
        self.paths = random.choice(paths)
        self.interactable = random.choice(interactables)

        # Always make some directions available
        # This ensures the player doesn't get stuck in a room
        random_directions = []
        if random.random() < 0.8:  # 80% chance for forward/backward
            random_directions.extend(['/forward', '/backward'])
        if random.random() < 0.7:  # 70% chance for left/right
            random_directions.extend(['/left', '/right'])
        if random.random() < 0.5:  # 50% chance for stairs
            if random.random() < 0.5:
                random_directions.append('/upstairs')
            else:
                random_directions.append('/downstairs')

        # Set available directions based on descriptions + random availability
        self.available_directions = {
            '/upstairs': 'up' in self.stairs.lower() or '/upstairs' in random_directions,
            '/downstairs': ('down' in self.stairs.lower() or 'below' in self.stairs.lower()) or '/downstairs' in random_directions,
            '/forward': ('forward' in self.paths.lower() or 'all' in self.paths.lower()) or '/forward' in random_directions,
            '/backward': ('back' in self.paths.lower() or 'all' in self.paths.lower()) or '/backward' in random_directions,
            '/left': ('left' in self.paths.lower() or 'all' in self.paths.lower()) or '/left' in random_directions,
            '/right': ('right' in self.paths.lower() or 'all' in self.paths.lower()) or '/right' in random_directions
        }

# Enhanced items with effects
items = {
    'battery': 'Restores sanity slightly',
    'flashlight': 'Reveals hidden paths and increases sanity recovery',
    'mysterious key': 'May unlock special doors',
    'old map': 'Shows nearby points of interest',
    'strange coin': 'Makes unusual sounds when danger is near',
    'polaroid camera': 'Captures evidence of the impossible',
    'music box': 'Calms the mind, restoring sanity',
    'compass': 'Points to... something',
    'pills': 'Restores significant sanity',
    'sanity': 'A manifestation of your mental state'
}

class Player:
    def __init__(self, name="Unknown", x=0, y=0, z=0, inventory=None, sanity=100, level=1):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.inventory = inventory if inventory is not None else []
        self.sanity = int(sanity)  # Force sanity to be an integer
        self.has_light = False
        self.level = level

class Game:
    def __init__(self):
        self.player = None
        self.exit = None
        self.special_door = None
        self.running = True
        self.discovered_areas = set()
        self.game_mode = None
        self.entities = []
        self.high_score = self.load_high_score()
        self.current_room = None
        # Initialize game state, menu will be shown explicitly from main()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def animate_text(self, text, delay=0.03):
        """Display text with a typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def show_load_menu(self):
        while True:
            print(Fore.CYAN + "\nSave slots:" + Style.RESET_ALL)
            for slot in range(1, MAX_SLOTS + 1):
                filepath = os.path.join(SAVE_DIR, f'save_slot_{slot}.sav')
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'rb') as f:
                            data = pickle.load(f)
                        player = data['player']
                        print(f"{slot}. {player.name} - Level {player.level} - Sanity: {player.sanity}")
                    except (pickle.PickleError, EOFError) as e:
                        print(f"{slot}. [Corrupted Save] ({e})")
                else:
                    print(f"{slot}. [Empty]")

            choice = input("\nEnter slot number to load (0 to return): ").strip()
            if choice == "0":
                return False
            if not choice.isdigit() or int(choice) < 1 or int(choice) > MAX_SLOTS:
                print(Fore.RED + f"Invalid slot number. Choose 1-{MAX_SLOTS} or 0 to return." + Style.RESET_ALL)
                continue
            if self.load(choice):
                return True
            else:
                print(Fore.RED + "Failed to load save. Please try again." + Style.RESET_ALL)

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError) as e:
            print(Fore.RED + f"\nCould not load high score: {e}" + Style.RESET_ALL)
            return 0

    def save_high_score(self, score):
        try:
            if score > self.high_score:
                with open('highscore.txt', 'w') as f:
                    f.write(str(score))
                self.high_score = score
                print(Fore.GREEN + f"\nNew High Score: {score}!" + Style.RESET_ALL)


        except (FileNotFoundError, ValueError) as e:
            print(Fore.RED + f"\nCould not load high score: {e}" + Style.RESET_ALL)
            return 0

    def show_menu(self):
        self.clear_screen()
        print(Fore.CYAN + """
█░░ █ █▀▄▀█ █ █▄░█ ▄▀█ █░░
█▄▄ █ █░▀░█ █ █░▀█ █▀█ █▄▄""" + Style.RESET_ALL)

        print("\nSelect Option:")
        print(Fore.RED + "1. Nightmare Mode" + Style.RESET_ALL + " - 34 entities, one life, infinite levels")
        print(Fore.YELLOW + "2. Normal Mode" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Load Game" + Style.RESET_ALL)
        print(Fore.WHITE + "0. Quit Game" + Style.RESET_ALL)

        try:
            choice = input("\nEnter your choice (0-3): ").strip()

            if choice == "0":
                print(Fore.YELLOW + "\nThank you for playing Liminal. Goodbye!" + Style.RESET_ALL)
                sys.exit(0)
            elif choice == "1":
                self.game_mode = "nightmare"
                print(Fore.RED + f"\nCurrent High Score: {self.high_score} levels" + Style.RESET_ALL)
            elif choice == "3":
                if self.show_load_menu():
                    return
                self.show_menu()
                return
            elif choice == "2":
                print("\nSelect Normal Mode Type:")
                print(Fore.CYAN + "1. Coma Mode" + Style.RESET_ALL + " - Standard game")
                print(Fore.GREEN + "2. Dreaming Mode" + Style.RESET_ALL + " - No entities, special ending")
                try:
                    sub_choice = input("\nEnter your choice (1-2): ").strip()
                    if sub_choice == "1":
                        self.game_mode = "coma"
                    elif sub_choice == "2":
                        self.game_mode = "dreaming" 
                    else:
                        print(Fore.YELLOW + "\nInvalid choice. Defaulting to Coma Mode." + Style.RESET_ALL)
                        self.game_mode = "coma"
                except (EOFError, KeyboardInterrupt):
                    print(Fore.RED + "\nInput interrupted. Returning to main menu." + Style.RESET_ALL)
                    self.show_menu()
                    return
            else:
                print(Fore.RED + "\nInvalid choice. Please try again." + Style.RESET_ALL)
                time.sleep(1)
                self.show_menu()
                return
        except (EOFError, KeyboardInterrupt):
            print(Fore.RED + "\nInput interrupted. Exiting game." + Style.RESET_ALL)
            sys.exit(0)

        self.initialize_game()

    def check_nightmare_death(self):
        if self.game_mode == "nightmare" and self.player is not None:
            for entity in self.entities:
                if (entity['pos'] == (self.player.x, self.player.y, self.player.z) and 
                    not entity.get('friendly', False)):
                    self.animate_text(Fore.RED + f"\n{entity['name']} found you. Game Over." + Style.RESET_ALL)
                    self.save_high_score(self.player.level)
                    self.running = False
                    return True
        return False

    def move_entities(self):
        if self.game_mode == "nightmare" and self.player is not None:
            for entity in self.entities:
                if random.random() < entity['speed']:
                    dx = self.player.x - entity['pos'][0]
                    dy = self.player.y - entity['pos'][1]
                    dz = self.player.z - entity['pos'][2]

                    # Move towards player with some randomness to avoid clustering
                    x, y, z = entity['pos']
                    directions = []
                    if dx != 0:
                        directions.append(('x', 1 if dx > 0 else -1))
                    if dy != 0:
                        directions.append(('y', 1 if dy > 0 else -1))
                    if dz != 0:
                        directions.append(('z', 1 if dz > 0 else -1))

                    if directions:
                        axis, step = random.choice(directions)
                        if axis == 'x':
                            x += step
                        elif axis == 'y':
                            y += step
                        else:
                            z += step

                    entity['pos'] = (x, y, z)

    def generate_entities(self):
        if self.game_mode == "nightmare":
            self.entities = []

            # Theme-based entities
            theme_entities = {
                'hospital': [
                    {'name': 'Shadowy Doctor', 'speed': 0.5, 'friendly': False, 'theme': 'hospital'},
                    {'name': 'Ghostly Patient', 'speed': 0.3, 'friendly': True, 'theme': 'hospital'},
                    {'name': 'Blood Seeker', 'speed': 0.6, 'friendly': False, 'theme': 'hospital'},
                    {'name': 'Orderly', 'speed': 0.4, 'friendly': False, 'theme': 'hospital'},
                    {'name': 'Nurse', 'speed': 0.5, 'friendly': False, 'theme': 'hospital'},
                    {'name': 'The surgeon', 'speed': 0.4, 'friendly': False, 'theme': 'hospital'},
                    {'name': 'The girl of that toilet stall', 'speed': 0.3, 'friendly': False, 'theme': 'hospital'}
                ],
                'school': [
                    {'name': 'Phantom Teacher', 'speed': 0.4, 'friendly': False, 'theme': 'school'},
                    {'name': 'Lost Student', 'speed': 0.3, 'friendly': True, 'theme': 'school'},
                    {'name': 'The bully', 'speed': 0.5, 'friendly': False, 'theme': 'school'},
                    {'name': 'Teacher\'s Assistant', 'speed': 0.5, 'friendly': False, 'theme': 'school'},
                    {'name': 'Hall Monitor', 'speed': 0.5, 'friendly': False, 'theme': 'school'},
                    {'name': 'Cafeteria Ghost', 'speed': 0.4, 'friendly': False, 'theme': 'school'},
                    {'name': 'The Librarian', 'speed': 0.3, 'friendly': True, 'theme': 'school'},
                    {'name': 'Detention Spirit', 'speed': 0.6, 'friendly': False, 'theme': 'school'}
                ],
                'home': [
                    {'name': 'Shadow Mother', 'speed': 0.4, 'friendly': False, 'theme': 'home'},
                    {'name': 'Child Spirit', 'speed': 0.3, 'friendly': True, 'theme': 'home'},
                    {'name': 'Basement Dweller', 'speed': 0.5, 'friendly': False, 'theme': 'home'},
                    {'name': 'Attic Crawler', 'speed': 0.6, 'friendly': False, 'theme': 'home'},
                    {'name': 'Sister', 'speed': 0.4, 'friendly': False, 'theme': 'home'},
                    {'name': 'Brother', 'speed': 0.3, 'friendly': False, 'theme': 'home'},
                    {'name': 'Father', 'speed': 0.5, 'friendly': False, 'theme': 'home'},
                    {'name': 'Mother', 'speed': 0.6, 'friendly': False, 'theme': 'home'},
                    {'name': 'Grandmother', 'speed': 0.2, 'friendly': True, 'theme': 'home'},
                    {'name': 'Grandfather', 'speed': 0.2, 'friendly': True, 'theme': 'home'},
                    {'name': 'The good dog', 'speed': 0.4, 'friendly': False, 'theme': 'home'},
                    {'name': 'The stray cat', 'speed': 0.3, 'friendly': True, 'theme': 'home'},
                ],
                'limbo': [
                    {'name': 'Shadow Walker', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'Mind Eater', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'Lost Soul', 'speed': 0.3, 'friendly': True, 'theme': 'limbo'},
                    {'name': 'Void Stalker', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'The angel', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'The demon', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'The shadow', 'speed': 0.3, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'The watcher', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                    {'name': 'Your friend', 'speed': 0.4, 'friendly': True, 'theme': 'limbo'},
                ],
                'mall': [
                    {'name': 'Mannequin', 'speed': 0.4, 'friendly': False, 'theme': 'mall'},
                    {'name': 'Distorted shopping machine', 'speed': 0.5, 'friendly': False, 'theme': 'mall'},
                    {'name': 'Lost Weird Shopper', 'speed': 0.3, 'friendly': False, 'theme': 'mall'},
                    {'name': 'Security Patrol', 'speed': 0.5, 'friendly': False, 'theme': 'mall'},
                    {'name': 'Faceless Clerk', 'speed': 0.6, 'friendly': False, 'theme': 'mall'},
                    {'name': 'Faceless Security Guard', 'speed': 0.4, 'friendly': False, 'theme': 'mall'}
                ],
                'Train_station':[
                    {'name': 'Train conductor', 'speed': 0.4, 'friendly': False, 'theme': 'Train_station'},
                    {'name': 'Crawling Woman', 'speed': 0.9, 'friendly': False, 'theme': 'Train_station'},
                    {'name': 'Undead corpses', 'speed': 0.5, 'friendly': False, 'theme': 'Train_station'},
                    {'name': 'The train', 'speed': 10.5, 'friendly': False, 'theme': 'Train_station'},
                ],
                'Abandoned_amusement_park':[
                    {'name': 'The clown', 'speed': 0.4, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                    {'name': 'The clown with a knife', 'speed': 0.5, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                    {'name': 'The clown with a chainsaw', 'speed': 0.6, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                    {'name': 'The Mickey Mouse', 'speed': 0.4, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                    {'name': 'The Donald Duck', 'speed': 0.5, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                    {'name': 'The Goofy', 'speed': 0.6, 'friendly': False, 'theme': 'Abandoned_amusement_park'},
                ]
            }

            # Get the current level theme
            current_theme = self.level_theme if hasattr(self, 'level_theme') else 'limbo'

            # Default entities for mixed themes
            default_entities = [
                {'name': 'Shadow Walker', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Mind Eater', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Lost Soul', 'speed': 0.3, 'friendly': True, 'theme': 'limbo'},
                {'name': 'Void Stalker', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The angel', 'speed': 0.4, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The demon', 'speed': 0.5, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The shadow', 'speed': 0.3, 'friendly': False, 'theme': 'limbo'},
                {'name': 'The watcher', 'speed': 0.6, 'friendly': False, 'theme': 'limbo'},
                {'name': 'Your friend', 'speed': 0.4, 'friendly': True, 'theme': 'limbo'},
                {'name': 'Your worst dream','speed': 0.5, 'friendly': False, 'theme': 'limbo'},
            ]

            # Create a mix of themed and default entities
            theme_specific = theme_entities.get(current_theme, default_entities)
            all_entities = theme_specific + default_entities  # Mix theme-specific with default entities

            # Higher player level means more entities and they're faster
            if self.player:
                num_entities = min(34, 20 + (self.player.level // 5))
                level_speed_boost = min(0.2, self.player.level * 0.01)  # Max 0.2 speed boost at level 20+
            else:
                num_entities = 20
                level_speed_boost = 0

            for _ in range(num_entities):
                entity_type = random.choice(all_entities).copy()

                # Apply level-based speed boost
                entity_type['speed'] = min(0.9, entity_type['speed'] + level_speed_boost)

                # Position the entity
                entity_type['pos'] = (
                    random.randint(X_MIN, X_MAX),
                    random.randint(Y_MIN, Y_MAX),
                    random.randint(Z_MIN, Z_MAX)
                )

                # Make sure entity isn't placed directly on the player
                if self.player:
                    if entity_type['pos'] == (self.player.x, self.player.y, self.player.z):
                        # Reposition if on player
                        entity_type['pos'] = (
                            random.randint(X_MIN, X_MAX),
                            random.randint(Y_MIN, Y_MAX),
                            random.randint(Z_MIN, Z_MAX)
                        )

                self.entities.append(entity_type)

    def initialize_game(self):
        try:
            print(Fore.CYAN + "\nEnter your character's name:" + Style.RESET_ALL)
            name = input("> ").strip()
            if not name:
                name = "Unknown"
            
            start_z = random.randint(Z_MIN, Z_MAX)
            self.player = Player(name=name, x=0, y=0, z=start_z)
            self.generate_level()
            self.print_intro()
        except (EOFError, KeyboardInterrupt):
            print(Fore.RED + "\nGame initialization interrupted. Returning to menu." + Style.RESET_ALL)
            self.player = None
            time.sleep(1)
            try:
                self.show_menu()
            except Exception as e:
                print(Fore.RED + f"\nError returning to menu: {str(e)}" + Style.RESET_ALL)
                sys.exit(1)
        except Exception as e:
            print(Fore.RED + f"\nError during game initialization: {str(e)}" + Style.RESET_ALL)
            self.player = None
            time.sleep(1)
            try:
                self.show_menu()
            except Exception as e:
                print(Fore.RED + f"\nError returning to menu: {str(e)}" + Style.RESET_ALL)
                sys.exit(1)

    def generate_level(self):
        # Choose a theme for the level
        themes = ['hospital', 'school', 'home', 'limbo', 'mall', 'Train_station', 'Abandoned_amusement_park']

        # Theme progression: early levels are hospital and home, mid-levels include school and mall,
        # and higher levels tend toward limbo with higher frequency
        if self.player is None:
            # Default to a random theme if no player is set yet
            theme_weights = [1, 1, 1, 1, 1, 1, 1]  # Equal weights for all themes
            level = 1
        elif self.player.level < 10:
            theme_weights = [5, 1, 5, 1, 2, 1, 1]  # Hospital and home more common
            level = self.player.level
        elif self.player.level < 25:
            theme_weights = [3, 4, 3, 2, 4, 2, 2]  # School and mall more common
            level = self.player.level
        elif self.player.level < 40:
            theme_weights = [2, 3, 2, 5, 3, 2, 2]  # Limbo becomes more common
            level = self.player.level
        else:
            theme_weights = [1, 2, 1, 10, 1, 2, 3]  # Limbo dominant at high levels, more amusement park at very high levels
            level = self.player.level

        # Make sure the number of weights matches the number of themes
        if len(theme_weights) != len(themes):
            print(Fore.RED + "Warning: Theme weights don't match themes. Using equal weights." + Style.RESET_ALL)
            theme_weights = [1] * len(themes)
            
        self.level_theme = random.choices(themes, weights=theme_weights, k=1)[0]

        # Generate the exit far from the player
        while True:
            self.exit = (
                random.randint(X_MIN, X_MAX),
                random.randint(Y_MIN, Y_MAX),
                random.randint(Z_MIN, Z_MAX)
            )

            # Make sure exit is far enough from player
            if self.player:
                distance = abs(self.exit[0] - self.player.x) + abs(self.exit[1] - self.player.y) + abs(self.exit[2] - self.player.z)
                if distance >= 10:  # Minimum distance to make it challenging
                    break
            else:
                break

        # Generate special door for heaven/hell endings
        if self.player is not None and self.player.level >= 50:  # Special door appears after level 50
            z = 5 if random.random() < 0.5 else -5  # Top or bottom floor
            x = random.randint(X_MIN, X_MAX)
            y = random.randint(Y_MIN, Y_MAX)
            while abs(x - self.player.x) + abs(y - self.player.y) < MIN_HEAVEN_DOOR_DISTANCE:
                x = random.randint(X_MIN, X_MAX)
                y = random.randint(Y_MIN, Y_MAX)
            self.special_door = (x, y, z)
        else:
            self.special_door = None

        # Pre-generate some rooms to create consistency in the world
        # This creates a more coherent "tiled map" feeling
        self.discovered_areas = set()  # Reset discovered areas
        self.room_map = {}  # Store pre-generated rooms

        # Generate a number of predefined rooms
        num_predefined = min(50, 20 + (level // 2))  # More rooms at higher levels
        for _ in range(num_predefined):
            pos = (
                random.randint(X_MIN, X_MAX),
                random.randint(Y_MIN, Y_MAX),
                random.randint(Z_MIN, Z_MAX)
            )
            if pos not in self.room_map:
                self.room_map[pos] = Room(theme=self.level_theme, level=level)

        # Add specific room at exit location
        self.room_map[self.exit] = Room(theme='limbo', level=level)  # Exit is always limbo-themed

        # If there's a special door, make that room special too
        if self.special_door:
            special_room = Room(theme='limbo', level=level)
            # Make sure it's a special room with visible distinctions
            special_room.description = Fore.WHITE + "A room with a strange door that glows with otherworldly energy." + Style.RESET_ALL
            self.room_map[self.special_door] = special_room

    def print_intro(self):
        title = """
█░░ █ █▀▄▀█ █ █▄░█ ▄▀█ █░░
█▄▄ █ █░▀░█ █ █░▀█ █▀█ █▄▄"""

        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT + title + Style.RESET_ALL)
        if self.player is not None:
            print(Fore.MAGENTA + f"\nWelcome, {self.player.name}, to where reality bends and perception ends..." + Style.RESET_ALL)
        else:
            print(Fore.MAGENTA + "\nWelcome to where reality bends and perception ends..." + Style.RESET_ALL)
        print("\nType /help for a list of commands.\n")

    def check_endings(self):
        if self.player is None:
            return False

        current_pos = (self.player.x, self.player.y, self.player.z)

        # Wall of photos ending (Real ending)
        if (self.current_room and 
            "wall of photos" in self.current_room.description.lower() and 
            random.random() < 0.05):
            self.wake_up_ending()
            return True

        # Heaven/Hell endings
        if self.special_door and current_pos == self.special_door:
            if self.player.sanity > 70:
                self.heaven_ending()
            else:
                self.hell_ending()
            return True

        # Exit to next level
        if current_pos == self.exit:
            self.next_level()
            return False  # Not a game ending, just level progression

        return False

    def wake_up_ending(self):
        self.clear_screen()
        self.animate_text(Fore.CYAN + "\nYou stare at the wall of photos. Memories flood back...")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nA car accident. A hospital room. Machines beeping.")
        time.sleep(1)
        self.animate_text(Fore.GREEN + "\nYou've been in a coma. This was all in your mind.")
        time.sleep(1)
        self.animate_text(Fore.WHITE + "\nYou feel yourself pulled back to reality.")
        time.sleep(2)
        self.animate_text(Fore.MAGENTA + "\nYour eyes open. A doctor smiles down at you.")
        time.sleep(1)
        self.animate_text(Fore.CYAN + "\n\"Welcome back,\" she says.")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nYou see all your family members around your bed.")
        time.sleep(1)
        self.animate_text(Fore.WHITE + "\nYou start tearing along your family's faces.")
        time.sleep(1)
        self.animate_text(Fore.GREEN + "\nYOU WOKE UP - THE REAL ENDING" + Style.RESET_ALL)
        self.running = False
        return True

    def heaven_ending(self):
        self.clear_screen()
        self.animate_text(Fore.CYAN + "\nYou step through the door into blinding light...")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nYou realise your body is no longer heavy.")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nA sense of peace washes over you.")
        time.sleep(1)
        self.animate_text(Fore.WHITE + "\nYou see familiar faces. People you once knew.")
        time.sleep(1)
        self.animate_text(Fore.MAGENTA + "\nThey welcome you with open arms.")
        time.sleep(1)
        self.animate_text(Fore.CYAN + "\nYou realize you've been here before.")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nYou're finally home.")
        time.sleep(1)
        self.animate_text(Fore.WHITE + "\nHEAVEN ENDING - You found peace" + Style.RESET_ALL)
        self.running = False
        return True

    def hell_ending(self):
        self.clear_screen()
        self.animate_text(Fore.RED + "\nYou step through the door into smothering darkness...")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nThe air is hot and sulfurous.")
        time.sleep(1)
        self.animate_text(Fore.RED + "\nYou hear screams in the distance.")
        time.sleep(1)
        self.animate_text(Fore.MAGENTA + "\nShadowy figures surround you.")
        time.sleep(1)
        self.animate_text(Fore.RED + "\nYou try to run, but there's nowhere to go.")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nYou realize this is your fate.")
        time.sleep(1)
        self.animate_text(Fore.RED + "\nHELL ENDING - Your sanity was too low" + Style.RESET_ALL)
        self.running = False
        return True

    def dreaming_ending(self):
        self.clear_screen()
        self.animate_text(Fore.CYAN + "\nYou sit on your bed, looking out the window...")
        time.sleep(1)
        self.animate_text(Fore.YELLOW + "\nThe dream is ending, but you know you can return.")
        time.sleep(1)
        self.animate_text(Fore.GREEN + "\nYou close your eyes, ready to wake up.")
        time.sleep(1)
        self.animate_text(Fore.WHITE + "\nWhen you open them, you're back in your room.")
        time.sleep(1)
        self.animate_text(Fore.MAGENTA + "\nIt was all a dream, but the memories remain.")
        time.sleep(1)
        self.animate_text(Fore.CYAN + "\nYou can always return to this place.")
        time.sleep(1)
        self.animate_text(Fore.RED + "\nYou know you can ALWAYS return...")
        time.sleep(1)
        self.animate_text(Fore.CYAN + "\nAnd you know you can go back whenever you want.")
        time.sleep(1)
        self.animate_text(Fore.GREEN + "\nDREAMING ENDING - You can always return" + Style.RESET_ALL)
        self.running = False
        return True

    def next_level(self):
        if self.player is None:
            return

        self.player.level += 1
        self.player.sanity = min(self.player.sanity + 15, SANITY_MAX)  # Reward for completing a level

        print(Fore.GREEN + f"\nYou found the exit! Moving to level {self.player.level}." + Style.RESET_ALL)
        print(Fore.CYAN + f"Sanity restored to {self.player.sanity}." + Style.RESET_ALL)

        # Add a random item to inventory sometimes
        if random.random() < 0.3:
            item = random.choice(list(items.keys()))
            if item != 'sanity':  # Don't add sanity as an item
                self.player.inventory.append(item)
                print(Fore.YELLOW + f"You found a {item}!" + Style.RESET_ALL)

        self.generate_level()
        self.generate_entities()
        time.sleep(2)

    def display_room(self):
        if self.player is None:
            return

        current_pos = (self.player.x, self.player.y, self.player.z)

        # Use the room from our tiled map if it exists, otherwise create a new one
        if hasattr(self, 'room_map') and current_pos in self.room_map:
            self.current_room = self.room_map[current_pos]
        elif current_pos not in self.discovered_areas:
            # Create a new room using the level theme
            level = self.player.level if self.player else 1
            theme = self.level_theme if hasattr(self, 'level_theme') else None
            self.current_room = Room(theme=theme, level=level)

            # Add to discovered areas and room map
            self.discovered_areas.add(current_pos)
            if hasattr(self, 'room_map'):
                self.room_map[current_pos] = self.current_room

        # Make sure current_room is set
        if self.current_room is None:
            self.current_room = Room(theme=self.level_theme if hasattr(self, 'level_theme') else None, 
                                     level=self.player.level if self.player else 1)

        # Display room description with theme information
        theme_colors = {
            'hospital': Fore.CYAN,
            'school': Fore.YELLOW,
            'home': Fore.GREEN,
            'limbo': Fore.MAGENTA,
            'mall': Fore.BLUE
        }

        # Show theme info at higher levels when player has more experience
        if self.player and self.player.level > 5 and hasattr(self.current_room, 'theme') and self.current_room.theme:
            theme_color = theme_colors.get(self.current_room.theme, Fore.WHITE)
            theme_name = self.current_room.theme.upper()
            print(f"\n{theme_color}[{theme_name} ZONE - LEVEL {self.player.level}]{Style.RESET_ALL}")

        # Display room description with null checks
        if hasattr(self.current_room, 'description') and self.current_room.description:
            print(f"\n{self.current_room.description}")
        else:
            print("\nAn undefined space that feels wrong somehow.")

        if hasattr(self.current_room, 'stairs') and self.current_room.stairs:
            print(f"{self.current_room.stairs}")
        else:
            print("There are no visible stairs or elevators.")

        if hasattr(self.current_room, 'paths') and self.current_room.paths:
            print(f"{self.current_room.paths}")
        else:
            print("Paths extend in unpredictable directions.")

        # Display interactable if present with null checks
        if hasattr(self.current_room, 'interactable') and self.current_room.interactable and isinstance(self.current_room.interactable, tuple) and len(self.current_room.interactable) > 0:
            print(Fore.YELLOW + f"\n{self.current_room.interactable[0]}" + Style.RESET_ALL)

        # Display any nearby entities in nightmare mode
        if self.game_mode == "nightmare" and hasattr(self, 'entities'):
            nearby_entities = []
            for entity in self.entities:
                ex, ey, ez = entity['pos']
                distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)

                if distance <= 3:  # Close enough to sense
                    if hasattr(self.player, 'has_light') and self.player.has_light:  # Can see clearly with light
                        entity_name = entity['name']
                        entity_theme = entity.get('theme', 'unknown')
                        # Show more detail about entities when player has a light
                        nearby_entities.append(f"{entity_name} ({entity_theme}) is nearby.")
                    else:  # Can only sense
                        nearby_entities.append("Something moves in the darkness.")

            if nearby_entities:
                print(Fore.RED + "\nDanger:" + Style.RESET_ALL)
                for entity_msg in nearby_entities:
                    print(Fore.RED + f" - {entity_msg}" + Style.RESET_ALL)

        # Show if this is the exit
        if hasattr(self, 'exit') and current_pos == self.exit:
            print(Fore.GREEN + "\nThis room has a door that feels different. It might be the exit." + Style.RESET_ALL)

        # Show special door if present
        if hasattr(self, 'special_door') and self.special_door and current_pos == self.special_door:
            if self.player.sanity > 70:
                print(Fore.WHITE + "\nA radiant door pulses with warm light. It calls to you." + Style.RESET_ALL)
            else:
                print(Fore.RED + "\nA dark door emanates dread. Something waits beyond." + Style.RESET_ALL)

        # Display minimap for player with adjacency information
        if hasattr(self.player, 'has_light') and self.player.has_light and hasattr(self, 'room_map'):  # Only show minimap if player has light
            print(Fore.CYAN + "\nAdjacent Rooms:" + Style.RESET_ALL)
            for direction, (dx, dy, dz) in directions.items():
                adjacent_pos = (self.player.x + dx, self.player.y + dy, self.player.z + dz)
                if adjacent_pos in self.room_map:
                    adj_room = self.room_map[adjacent_pos]
                    if hasattr(adj_room, 'theme') and adj_room.theme:
                        print(f" - {direction}: {theme_colors.get(adj_room.theme, Fore.WHITE)}{adj_room.theme.capitalize()} area{Style.RESET_ALL}")
                    else:
                        print(f" - {direction}: Unknown area")

    def show_help(self):
        print(Fore.CYAN + "\n=== COMMANDS ===" + Style.RESET_ALL)
        print("movement: /right, /left, /forward, /backward, /upstairs, /downstairs")
        print("alternate movement: /move [direction]")
        print("interact: /examine, /use [item], /take")
        print("inventory: /inventory or /i")
        print("stats: /stats")
        print("save game: /save [slot]")
        print("load game: /load [slot]")
        print("exit: /exit or /quit")
        print("help: /help")

    def show_stats(self):
        if self.player is None:
            print(Fore.RED + "\nNo active player." + Style.RESET_ALL)
            return

        print(Fore.CYAN + "\n=== STATS ===" + Style.RESET_ALL)
        print(f"Name: {self.player.name}")
        print(f"Level: {self.player.level}")

        # Display sanity with color coding
        sanity_color = Fore.GREEN
        if self.player.sanity < 30:
            sanity_color = Fore.RED
        elif self.player.sanity < 70:
            sanity_color = Fore.YELLOW
        print(f"Sanity: {sanity_color}{self.player.sanity}{Style.RESET_ALL}")

        print(f"Position: ({self.player.x}, {self.player.y}, {self.player.z})")

        if self.game_mode == "nightmare":
            print(Fore.RED + "Game Mode: Nightmare" + Style.RESET_ALL)
        elif self.game_mode == "coma":
            print(Fore.YELLOW + "Game Mode: Coma" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Game Mode: Dreaming" + Style.RESET_ALL)

    def show_inventory(self):
        if self.player is None:
            print(Fore.RED + "\nNo active player." + Style.RESET_ALL)
            return

        if not self.player.inventory:
            print(Fore.YELLOW + "\nYour inventory is empty." + Style.RESET_ALL)
            return

        print(Fore.CYAN + "\n=== INVENTORY ===" + Style.RESET_ALL)
        for item in self.player.inventory:
            print(f"{item}: {items.get(item, 'Unknown item')}")

    def move(self, direction):
        if self.player is None:
            print(Fore.RED + "\nNo active player." + Style.RESET_ALL)
            return

        # Handle directions with slash prefix for consistency
        if direction.startswith('/'):
            direction = direction[1:]

        if direction not in directions:
            print(Fore.RED + f"Invalid direction. Use: {', '.join(directions.keys())}" + Style.RESET_ALL)
            return

        # Make sure current_room is set
        if not hasattr(self, 'current_room') or self.current_room is None:
            self.current_room = Room(theme=self.level_theme if hasattr(self, 'level_theme') else None, 
                                     level=self.player.level if self.player else 1)

        # Check if the direction is available in the current room
        if not hasattr(self.current_room, 'available_directions') or not self.current_room.available_directions.get(direction, False):
            print(Fore.RED + f"You can't go {direction} from here." + Style.RESET_ALL)
            return

        dx, dy, dz = directions[direction]
        self.player.x += dx
        self.player.y += dy
        self.player.z += dz

        # Constrain to world bounds
        self.player.x = max(X_MIN, min(X_MAX, self.player.x))
        self.player.y = max(Y_MIN, min(Y_MAX, self.player.y))
        self.player.z = max(Z_MIN, min(Z_MAX, self.player.z))

        # Sanity loss on movement
        sanity_loss = 1
        if hasattr(self.player, 'has_light') and self.player.has_light:
            sanity_loss = 0.5

        # Round down to int for sanity
        self.player.sanity = int(max(0, self.player.sanity - sanity_loss))

        print(f"Moving {direction}...")

        # If you moved, entities might move too
        if hasattr(self, 'move_entities') and callable(getattr(self, 'move_entities')):
            self.move_entities()

        # Check if player died by entity
        if hasattr(self, 'check_nightmare_death') and callable(getattr(self, 'check_nightmare_death')):
            if self.check_nightmare_death():
                return

        # Check if new position triggers an ending
        if hasattr(self, 'check_endings') and callable(getattr(self, 'check_endings')):
            if not self.check_endings():
                self.display_room()

        # Warn if sanity is low
        if hasattr(self.player, 'sanity'):
            if self.player.sanity < 20:
                print(Fore.RED + "\nYour sanity is dangerously low!" + Style.RESET_ALL)
            elif self.player.sanity < 50:
                print(Fore.YELLOW + "\nYour sanity is getting low." + Style.RESET_ALL)

    def interact(self, action):
        if self.player is None:
            print(Fore.RED + "\nNo active player." + Style.RESET_ALL)
            return

        if not self.current_room:
            print(Fore.RED + "\nNo current room to interact with." + Style.RESET_ALL)
            return

        if action == "examine":
            if (hasattr(self.current_room, 'interactable') and 
                self.current_room.interactable and 
                isinstance(self.current_room.interactable, tuple) and 
                len(self.current_room.interactable) > 1):

                print(Fore.CYAN + f"\n{self.current_room.interactable[1]}" + Style.RESET_ALL)

                # Sometimes interacting gives sanity
                if random.random() < 0.3:
                    gain = random.randint(5, 15)
                    self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
                    print(Fore.GREEN + f"You feel a bit better. +{gain} sanity." + Style.RESET_ALL)
            else:
                print("There's nothing interesting to examine here.")

        elif action == "take":
            if (hasattr(self.current_room, 'interactable') and 
                self.current_room.interactable and 
                isinstance(self.current_room.interactable, tuple)):

                # Higher chance of finding something to test inventory properly
                if random.random() < 0.9:  
                    item = random.choice(list(items.keys()))
                    if item != 'sanity':  # Don't add sanity as an item
                        self.player.inventory.append(item)
                        print(Fore.YELLOW + f"You found a {item}!" + Style.RESET_ALL)
                    else:
                        print("There's nothing useful to take.")
                else:
                    print("There's nothing useful to take.")
            else:
                print("There's nothing useful to take.")

        elif action.startswith("use "):
            item = action[4:].strip()
            if item in self.player.inventory:
                self.use_item(item)
            else:
                print(Fore.RED + f"You don't have a {item}." + Style.RESET_ALL)

        else:
            print(Fore.RED + "Unknown action. Try 'examine', 'take', or 'use [item]'." + Style.RESET_ALL)

    def use_item(self, item):
        if self.player is None:
            print(Fore.RED + "\nNo active player." + Style.RESET_ALL)
            return

        if item == 'battery':
            gain = random.randint(10, 20)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(Fore.GREEN + f"You use the battery to power your devices. +{gain} sanity." + Style.RESET_ALL)
            self.player.inventory.remove(item)

        elif item == 'flashlight':
            self.player.has_light = True
            print(Fore.YELLOW + "You turn on the flashlight. It will help you see and preserve sanity." + Style.RESET_ALL)
            if 'battery' not in self.player.inventory:
                print("The flashlight will eventually need batteries.")

        elif item == 'mysterious key':
            current_pos = (self.player.x, self.player.y, self.player.z)
            if current_pos == self.exit:
                print(Fore.GREEN + "The key fits the exit door! You can now proceed to the next level." + Style.RESET_ALL)
                self.next_level()
            elif self.special_door and current_pos == self.special_door:
                print(Fore.CYAN + "The key fits the mysterious door. You open it..." + Style.RESET_ALL)
                if self.player.sanity > 70:
                    self.heaven_ending()
                else:
                    self.hell_ending()
            else:
                print("You try the key, but there's no lock here that it fits.")

        elif item == 'old map':
            # Show nearby points of interest
            print(Fore.CYAN + "\nThe map reveals:" + Style.RESET_ALL)

            # Show exit direction
            if self.exit is not None:
                exit_x, exit_y, exit_z = self.exit
                dx = exit_x - self.player.x
                dy = exit_y - self.player.y
                dz = exit_z - self.player.z
            else:
                print("The map seems to be blank or damaged.")
                return

            if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                direction = "east" if dx > 0 else "west"
            elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                direction = "north" if dy > 0 else "south"
            else:
                direction = "up" if dz > 0 else "down"

            print(f"- The exit appears to be to the {direction}.")

            # Sometimes reveal special door
            if self.special_door and random.random() < 0.5:
                print("- A special door is marked with a strange symbol.")

            # In nightmare mode, reveal nearby entities
            if self.game_mode == "nightmare":
                nearby_count = 0
                for entity in self.entities:
                    ex, ey, ez = entity['pos']
                    distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)
                    if distance <= 5:
                        nearby_count += 1

                if nearby_count > 0:
                    print(Fore.RED + f"- {nearby_count} entities are nearby." + Style.RESET_ALL)

        elif item == 'strange coin':
            # Warns about nearby entities
            if self.game_mode == "nightmare":
                danger_level = 0
                for entity in self.entities:
                    ex, ey, ez = entity['pos']
                    distance = abs(ex - self.player.x) + abs(ey - self.player.y) + abs(ez - self.player.z)
                    if distance <= 3 and not entity.get('friendly', False):
                        danger_level += 1

                if danger_level == 0:
                    print("The coin is silent. No immediate danger.")
                elif danger_level <= 2:
                    print(Fore.YELLOW + "The coin hums softly. Danger is near." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "The coin vibrates violently! Immediate danger!" + Style.RESET_ALL)
            else:
                print("The coin seems inert in this reality.")

        elif item == 'polaroid camera':
            print("You take a photo. It develops slowly...")
            time.sleep(1)

            photo_descriptions = [
                "The photo shows this room, but with someone standing behind you who isn't there.",
                "The photo is completely black except for two glowing eyes.",
                "The photo shows you, but your face is blurred and distorted.",
                "The photo reveals hidden writing on the walls that says 'WAKE UP'.",
                "The photo shows the exit door glowing faintly.",
                "The photo is normal, but as you watch, your figure in it begins to move."
            ]

            print(Fore.CYAN + random.choice(photo_descriptions) + Style.RESET_ALL)

            # Small chance to reveal exit
            if random.random() < 0.2 and self.exit is not None:
                exit_x, exit_y, exit_z = self.exit
                print(Fore.GREEN + f"You notice coordinates in the corner: ({exit_x}, {exit_y}, {exit_z})" + Style.RESET_ALL)

        elif item == 'music box':
            gain = random.randint(15, 30)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(Fore.GREEN + f"The gentle melody soothes your mind. +{gain} sanity." + Style.RESET_ALL)

            # In nightmare mode, entities are attracted to the sound
            if self.game_mode == "nightmare":
                print(Fore.RED + "But the sound might attract unwanted attention..." + Style.RESET_ALL)
                for entity in self.entities:
                    if random.random() < 0.3:
                        ex, ey, ez = entity['pos']
                        # Move entity closer to player
                        if ex < self.player.x:
                            ex += 1
                        elif ex > self.player.x:
                            ex -= 1
                        if ey < self.player.y:
                            ey += 1
                        elif ey > self.player.y:
                            ey -= 1
                        if ez < self.player.z:
                            ez += 1
                        elif ez > self.player.z:
                            ez -= 1
                        entity['pos'] = (ex, ey, ez)

        elif item == 'compass':
            # Points to exit or special door
            if self.special_door and self.player.level >= 50 and random.random() < 0.3:
                sx, sy, sz = self.special_door
                dx = sx - self.player.x
                dy = sy - self.player.y
                dz = sz - self.player.z

                if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                    direction = "east" if dx > 0 else "west"
                elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                    direction = "north" if dy > 0 else "south"
                else:
                    direction = "up" if dz > 0 else "down"

                print(Fore.MAGENTA + f"The compass needle spins wildly, then points {direction} with a strange glow." + Style.RESET_ALL)
            else:
                if self.exit is not None:
                    ex, ey, ez = self.exit
                    dx = ex - self.player.x
                    dy = ey - self.player.y
                    dz = ez - self.player.z

                    if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                        direction = "east" if dx > 0 else "west"
                    elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
                        direction = "north" if dy > 0 else "south"
                    else:
                        direction = "up" if dz > 0 else "down"

                    print(Fore.CYAN + f"The compass needle points {direction}." + Style.RESET_ALL)
                else:
                    print(Fore.CYAN + "The compass needle spins erratically, as if confused." + Style.RESET_ALL)

        elif item == 'pills':
            gain = random.randint(30, 50)
            self.player.sanity = int(min(SANITY_MAX, self.player.sanity + gain))
            print(Fore.GREEN + f"You take the pills. Your mind clears significantly. +{gain} sanity." + Style.RESET_ALL)
            self.player.inventory.remove(item)

        else:
            print(f"You're not sure how to use the {item}.")

    def save(self, slot_number=None):
        if self.player is None:
            print(Fore.RED + "\nNo active player to save." + Style.RESET_ALL)
            return False

        if slot_number is None:
            print(Fore.CYAN + "\nSave slots:" + Style.RESET_ALL)
            for slot in range(1, MAX_SLOTS + 1):
                filepath = os.path.join(SAVE_DIR, f'save_slot_{slot}.sav')
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'rb') as f:
                            data = pickle.load(f)
                        player = data['player']
                        print(f"{slot}. {player.name} - Level {player.level} - Sanity: {player.sanity}")
                    except (pickle.PickleError, EOFError) as e:
                        print(f"{slot}. [Corrupted Save] ({e})")
                else:
                    print(f"{slot}. [Empty]")

            slot_number = input("\nEnter slot number (1-5): ").strip()
            if not slot_number.isdigit() or int(slot_number) < 1 or int(slot_number) > MAX_SLOTS:
                print(Fore.RED + f"Invalid slot number. Choose 1-{MAX_SLOTS}." + Style.RESET_ALL)
                return False

        try:
            save_data = {
                'player': self.player,
                'exit': self.exit,
                'special_door': self.special_door,
                'discovered_areas': self.discovered_areas,
                'game_mode': self.game_mode,
                'entities': self.entities,
                'current_room': self.current_room
            }

            filepath = os.path.join(SAVE_DIR, f'save_slot_{slot_number}.sav')
            with open(filepath, 'wb') as f:
                pickle.dump(save_data, f)

            print(Fore.GREEN + f"Game saved to slot {slot_number}." + Style.RESET_ALL)
            return True
        except Exception as e:
            print(Fore.RED + f"Error saving game: {e}" + Style.RESET_ALL)
            return False

    def load(self, slot_number):
        try:
            filepath = os.path.join(SAVE_DIR, f'save_slot_{slot_number}.sav')
            if not os.path.exists(filepath):
                print(Fore.RED + f"Save slot {slot_number} is empty." + Style.RESET_ALL)
                return False

            with open(filepath, 'rb') as f:
                data = pickle.load(f)

            self.player = data['player']
            self.exit = data['exit']
            self.special_door = data['special_door']
            self.discovered_areas = data['discovered_areas']
            self.game_mode = data['game_mode']
            self.entities = data['entities']
            self.current_room = data['current_room']

            print(Fore.GREEN + f"Game loaded from slot {slot_number}." + Style.RESET_ALL)
            self.display_room()
            return True
        except Exception as e:
            print(Fore.RED + f"Error loading game: {e}" + Style.RESET_ALL)
            return False

    def process_command(self, command):
        if not command:
            return

        if command in directions:
            self.move(command)

        elif command == '/help':
            self.show_help()

        elif command in ['/inventory', '/i']:
            self.show_inventory()

        elif command == '/stats':
            self.show_stats()

        elif command.startswith('/save'):
            parts = command.split()
            slot = None
            if len(parts) > 1:
                try:
                    slot = int(parts[1])
                except (ValueError, TypeError):
                    print(Fore.RED + "Invalid save slot number." + Style.RESET_ALL)
            self.save(slot)

        elif command.startswith('/load'):
            parts = command.split()
            if len(parts) > 1:
                try:
                    slot = int(parts[1])
                    self.load(slot)
                except (ValueError, TypeError):
                    print(Fore.RED + "Invalid save slot number." + Style.RESET_ALL)
            else:
                self.show_load_menu()

        elif command in ['/exit', '/quit']:
            confirm = input("Are you sure you want to quit? Progress will be lost unless saved. (y/n): ")
            if confirm and confirm.lower().startswith('y'):
                print("Thanks for playing!")
                self.running = False

        elif command in ['/examine', '/take'] or command.startswith('/use '):
            # Remove the slash for internal processing
            cmd = command[1:] if command.startswith('/') else command
            self.interact(cmd)

        # Add support for '/move direction' command
        elif command.startswith('/move '):
            direction = command[6:].strip()
            if f'/{direction}' in directions or direction in directions:
                self.move(direction)
            else:
                print(Fore.RED + f"Invalid direction. Use: {', '.join([d.replace('/', '') for d in directions.keys()])}" + Style.RESET_ALL)

        else:
            print(Fore.RED + "Unknown command. Type /help for commands." + Style.RESET_ALL)

    def game_loop(self):
        if not self.player:
            return

        self.display_room()

        while self.running:
            # Check for game over due to low sanity
            if self.player.sanity <= 0:
                print(Fore.RED + "\nYour sanity has completely eroded. You are lost in the liminal space forever." + Style.RESET_ALL)
                if self.game_mode == "nightmare":
                    self.save_high_score(self.player.level)
                self.running = False
                break

            try:
                command = input("\n> ").strip().lower()
                self.process_command(command)
            except EOFError:
                print(Fore.RED + "\nInput error occurred. Exiting game." + Style.RESET_ALL)
                self.running = False
                break
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\nGame interrupted. Goodbye!" + Style.RESET_ALL)
                self.running = False
                break

            # Dreaming mode check for special ending
            if self.game_mode == "dreaming" and self.player.level >= 10 and random.random() < 0.05:
                self.dreaming_ending()

def main():
    try:
        game = Game()
        game.show_menu()  # Show menu explicitly first
        game.game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except EOFError:
        print("\nInput error occurred. Exiting game.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
