import random
import os
import sys
import time
import pickle
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Game settings
X_MIN, X_MAX = -100, 100
Y_MIN, Y_MAX = -100, 100
Z_MIN, Z_MAX = -10, 10
SAVE_DIR = 'saves'
MAX_SLOTS = 5
SANITY_MAX = 100
REALITY_MAX = 100
MEMORY_MAX = 100
MIN_HEAVEN_DOOR_DISTANCE = 10
ENTITY_SPAWN_CHANCE = 0.15
ANOMALY_CHANCE = 0.25
TEMPORAL_DISTORTION_CHANCE = 0.10
MEMORY_FRAGMENT_CHANCE = 0.20
DIMENSIONAL_RIFT_CHANCE = 0.08
ECHO_EVENT_CHANCE = 0.15
PHANTOM_INTERACTION_CHANCE = 0.12

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

# Entity classes for encounters
class Entity:
    def __init__(self, name, description, behavior, threat_level=1):
        self.name = name
        self.description = description
        self.behavior = behavior
        self.threat_level = threat_level
        self.active = True

class Anomaly:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect

class MemoryFragment:
    def __init__(self, content, emotional_weight, clarity=1.0):
        self.content = content
        self.emotional_weight = emotional_weight  # 1-10 scale
        self.clarity = clarity  # 0.0-1.0, how clear the memory is
        self.triggered = False
        
class DimensionalRift:
    def __init__(self, destination_type, stability=0.5):
        self.destination_type = destination_type
        self.stability = stability
        self.uses_remaining = random.randint(1, 3)
        
class EchoEvent:
    def __init__(self, event_type, intensity, duration=1):
        self.event_type = event_type
        self.intensity = intensity  # 1-5 scale
        self.duration = duration
        self.active_turns = 0
        
class PhantomInteraction:
    def __init__(self, interaction_type, entity_name, success_chance=0.7):
        self.interaction_type = interaction_type
        self.entity_name = entity_name
        self.success_chance = success_chance
        self.completed = False

# Define liminal entities
ENTITIES = {
    'the_follower': Entity(
        "The Follower",
        "A shadowy figure that appears in your peripheral vision, always maintaining the same distance.",
        "follows_player",
        threat_level=2
    ),
    'memory_echo': Entity(
        "Memory Echo",
        "A translucent figure performing actions from your past, unaware of your presence.",
        "replays_memories",
        threat_level=1
    ),
    'void_walker': Entity(
        "Void Walker",
        "A humanoid silhouette that phases through walls, leaving reality distortions in its wake.",
        "reality_distortion",
        threat_level=3
    ),
    'the_observer': Entity(
        "The Observer",
        "An presence that watches from impossible angles, its gaze felt but never seen.",
        "constant_surveillance",
        threat_level=2
    ),
    'time_wraith': Entity(
        "Time Wraith",
        "A being that exists between moments, causing temporal anomalies wherever it goes.",
        "temporal_manipulation",
        threat_level=4
    ),
    'mirror_self': Entity(
        "Mirror Self",
        "An exact copy of yourself that appears in reflective surfaces, acting independently.",
        "mimics_player",
        threat_level=3
    ),
    'the_janitor': Entity(
        "The Janitor",
        "An elderly figure eternally cleaning spaces that never get dirty, humming forgotten melodies.",
        "environmental_maintenance",
        threat_level=1
    ),
    'static_person': Entity(
        "Static Person",
        "A human-shaped mass of television static that occasionally takes familiar forms.",
        "shape_shifting",
        threat_level=2
    ),
    'fragment_collector': Entity(
        "Fragment Collector",
        "A being made of scattered memories that seeks to gather lost fragments of consciousness.",
        "memory_absorption",
        threat_level=2
    ),
    'dimensional_guardian': Entity(
        "Dimensional Guardian",
        "An ethereal entity that protects rifts between worlds, challenging those who seek passage.",
        "rift_protection",
        threat_level=3
    ),
    'echo_phantom': Entity(
        "Echo Phantom",
        "A remnant of past events that replays traumatic moments in endless loops.",
        "event_repetition",
        threat_level=2
    ),
    'memory_thief': Entity(
        "Memory Thief",
        "A shadowy figure that steals precious memories and leaves gaps in consciousness.",
        "memory_theft",
        threat_level=4
    ),
    'temporal_anchor': Entity(
        "Temporal Anchor",
        "A being that exists outside time, offering glimpses of past and future to lost souls.",
        "time_revelation",
        threat_level=1
    )
}

# Memory Fragments that can be discovered
MEMORY_FRAGMENTS = [
    MemoryFragment("A childhood birthday party where everyone sang your name", 8, 0.9),
    MemoryFragment("The last conversation with someone you'll never see again", 10, 0.7),
    MemoryFragment("Walking home in the rain without an umbrella, feeling completely free", 6, 0.8),
    MemoryFragment("The smell of your grandmother's kitchen during holidays", 7, 1.0),
    MemoryFragment("A moment of pure terror in a place that should have been safe", 9, 0.6),
    MemoryFragment("Laughing until your stomach hurt with friends you've lost touch with", 8, 0.9),
    MemoryFragment("The exact moment you realized childhood was ending", 9, 0.5),
    MemoryFragment("A song that played during your first kiss", 7, 0.8),
    MemoryFragment("Standing in an empty house for the last time", 10, 0.9),
    MemoryFragment("The weight of a secret you've never told anyone", 8, 1.0),
    MemoryFragment("Running through sprinklers on a summer afternoon", 5, 0.9),
    MemoryFragment("The sound of footsteps following you in the dark", 9, 0.7),
    MemoryFragment("A dream so vivid you thought it was real for years", 6, 0.4),
    MemoryFragment("The moment you first understood what loneliness meant", 9, 0.8),
    MemoryFragment("Building sandcastles that the tide would inevitably wash away", 4, 0.9)
]

# Dimensional Rifts and their destinations
DIMENSIONAL_RIFTS = {
    'memory_vault': DimensionalRift("A space where lost memories float like golden orbs", 0.8),
    'shadow_realm': DimensionalRift("A dark mirror of reality where fears take physical form", 0.3),
    'temporal_nexus': DimensionalRift("A junction point where all timelines converge", 0.5),
    'emotional_landscape': DimensionalRift("A world shaped by pure emotion and feeling", 0.6),
    'forgotten_archive': DimensionalRift("A library containing every thought never spoken", 0.7),
    'parallel_self': DimensionalRift("A place where you can meet versions of yourself from other choices", 0.4),
    'childhood_echo': DimensionalRift("A recreation of your childhood home, but wrong in subtle ways", 0.6),
    'final_moment': DimensionalRift("The last second before everything changed forever", 0.2)
}

# Echo Events that can occur
ECHO_EVENTS = [
    EchoEvent("phantom_phone_call", 3, 2),
    EchoEvent("distant_laughter", 2, 1),
    EchoEvent("footsteps_overhead", 4, 3),
    EchoEvent("music_box_melody", 3, 2),
    EchoEvent("crying_child", 5, 1),
    EchoEvent("door_slamming", 4, 1),
    EchoEvent("whispered_name", 5, 2),
    EchoEvent("breaking_glass", 4, 1),
    EchoEvent("familiar_voice", 3, 3),
    EchoEvent("typing_sounds", 2, 2)
]

# Define anomalies
ANOMALIES = {
    'temporal_loop': Anomaly(
        "Temporal Loop",
        "Time begins to repeat in 3-minute cycles, with subtle changes each iteration.",
        "time_loop"
    ),
    'gravity_shift': Anomaly(
        "Gravity Anomaly",
        "Gravity becomes inconsistent, with objects and furniture floating or stuck to walls.",
        "physics_distortion"
    ),
    'memory_bleed': Anomaly(
        "Memory Bleed",
        "Memories from different times and places begin manifesting as physical objects.",
        "memory_manifestation"
    ),
    'reality_tear': Anomaly(
        "Reality Tear",
        "A visible crack in space reveals glimpses of other dimensions or timelines.",
        "dimensional_breach"
    ),
    'echo_chamber': Anomaly(
        "Echo Chamber",
        "Sounds from the past and future overlap with the present, creating an auditory chaos.",
        "temporal_audio"
    ),
    'shadow_displacement': Anomaly(
        "Shadow Displacement",
        "Shadows move independently of their sources, sometimes revealing hidden truths.",
        "shadow_manipulation"
    )
}

class Room:
    def __init__(self, theme=None, level=1):
        self.theme = theme if theme else random.choice(['hospital', 'school', 'home', 'limbo', 'mall', 'office', 'hotel', 'airport', 'parking_garage', 'subway', 'swimming_pool', 'warehouse', 'casino', 'theater', 'library', 'cathedral', 'laboratory', 'museum'])
        self.level = int(level) if level is not None else 1
        self.entities = []
        self.anomalies = []
        self.memory_fragments = []
        self.dimensional_rifts = []
        self.echo_events = []
        self.phantom_interactions = []
        self.atmosphere_intensity = random.uniform(0.3, 1.0)
        self.temporal_stability = random.uniform(0.5, 1.0)
        self.reality_coherence = random.uniform(0.4, 1.0)
        self.visited_count = 0
        self.hidden_secrets = random.randint(0, 3)
        self.emotional_resonance = random.uniform(0.2, 1.0)
        self.spawn_entities()
        self.generate_anomalies()
        self.generate_memory_fragments()
        self.generate_dimensional_rifts()
        self.generate_echo_events()
        self.generate_phantom_interactions()
        self.generate_description()

    def spawn_entities(self):
        if random.random() < ENTITY_SPAWN_CHANCE * (1 + self.level * 0.1):
            entity_key = random.choice(list(ENTITIES.keys()))
            self.entities.append(ENTITIES[entity_key])

    def generate_anomalies(self):
        if random.random() < ANOMALY_CHANCE * (1 + self.level * 0.05):
            anomaly_key = random.choice(list(ANOMALIES.keys()))
            self.anomalies.append(ANOMALIES[anomaly_key])

    def generate_memory_fragments(self):
        if random.random() < MEMORY_FRAGMENT_CHANCE:
            fragment = random.choice(MEMORY_FRAGMENTS)
            if not fragment.triggered:
                self.memory_fragments.append(fragment)

    def generate_dimensional_rifts(self):
        if random.random() < DIMENSIONAL_RIFT_CHANCE:
            rift_key = random.choice(list(DIMENSIONAL_RIFTS.keys()))
            rift = DIMENSIONAL_RIFTS[rift_key]
            if rift.uses_remaining > 0:
                self.dimensional_rifts.append(rift)

    def generate_echo_events(self):
        if random.random() < ECHO_EVENT_CHANCE:
            event = random.choice(ECHO_EVENTS)
            self.echo_events.append(event)

    def generate_phantom_interactions(self):
        if random.random() < PHANTOM_INTERACTION_CHANCE and self.entities:
            entity = random.choice(self.entities)
            interaction_types = ["communicate", "observe", "challenge", "bargain", "flee"]
            interaction_type = random.choice(interaction_types)
            phantom = PhantomInteraction(interaction_type, entity.name)
            self.phantom_interactions.append(phantom)

    def get_atmosphere_description(self):
        descriptions = []
        if self.atmosphere_intensity > 0.8:
            descriptions.append(f"{Fore.RED}{Style.BRIGHT}The air feels thick and oppressive, making breathing difficult.{Style.RESET_ALL}")
        elif self.atmosphere_intensity > 0.6:
            descriptions.append(f"{Fore.YELLOW}An unsettling tension permeates the space.{Style.RESET_ALL}")
        elif self.atmosphere_intensity > 0.4:
            descriptions.append(f"{Fore.CYAN}The atmosphere feels slightly off, like something is watching.{Style.RESET_ALL}")

        if self.temporal_stability < 0.3:
            descriptions.append(f"{Fore.MAGENTA}{Style.BRIGHT}Time seems to stutter and skip around you.{Style.RESET_ALL}")
        elif self.temporal_stability < 0.6:
            descriptions.append(f"{Fore.LIGHTMAGENTA_EX}The flow of time feels inconsistent here.{Style.RESET_ALL}")

        if self.reality_coherence < 0.4:
            descriptions.append(f"{Back.RED}{Fore.WHITE}Reality flickers like a damaged screen.{Style.RESET_ALL}")
        elif self.reality_coherence < 0.7:
            descriptions.append(f"{Fore.LIGHTBLACK_EX}The edges of your vision seem to blur and shift.{Style.RESET_ALL}")

        return descriptions

    def get_interactive_elements(self):
        """Get interactive elements that the player can engage with"""
        elements = []
        
        # Memory fragments create interactive opportunities
        for fragment in self.memory_fragments:
            if not fragment.triggered:
                elements.append(f"{Fore.YELLOW}🧠 A memory fragment glows softly in the corner{Style.RESET_ALL}")
        
        # Dimensional rifts offer travel options
        for rift in self.dimensional_rifts:
            if rift.uses_remaining > 0:
                elements.append(f"{Fore.MAGENTA}🌀 A dimensional rift shimmers in the air{Style.RESET_ALL}")
        
        # Echo events create atmospheric interactions
        for event in self.echo_events:
            if event.active_turns < event.duration:
                elements.append(f"{Fore.CYAN}👻 An echo resonates through the space{Style.RESET_ALL}")
        
        # Phantom interactions with entities
        for interaction in self.phantom_interactions:
            if not interaction.completed:
                elements.append(f"{Fore.LIGHTRED_EX}👤 You sense a presence nearby that might respond to interaction{Style.RESET_ALL}")
        
        return elements

    def trigger_memory_fragment(self, player):
        """Trigger a memory fragment and affect the player"""
        if self.memory_fragments:
            fragment = self.memory_fragments[0]
            fragment.triggered = True
            
            print(f"\n{Fore.YELLOW}🧠 Memory Fragment Activated:{Style.RESET_ALL}")
            print(f"{fragment.content}")
            
            # Apply emotional effects
            if fragment.emotional_weight >= 8:
                player.sanity -= random.randint(5, 15)
                print(f"{Fore.RED}The intensity of this memory weighs heavily on your mind...{Style.RESET_ALL}")
            elif fragment.emotional_weight >= 6:
                player.sanity -= random.randint(2, 8)
                print(f"{Fore.YELLOW}This memory stirs something deep within you...{Style.RESET_ALL}")
            else:
                player.sanity += random.randint(1, 5)
                print(f"{Fore.GREEN}This gentle memory provides some comfort...{Style.RESET_ALL}")
            
            # Clarity affects reality perception
            if fragment.clarity < 0.5:
                player.reality -= random.randint(3, 10)
                print(f"{Fore.MAGENTA}The unclear nature of this memory distorts your perception...{Style.RESET_ALL}")
            
            self.memory_fragments.remove(fragment)
            return True
        return False

    def use_dimensional_rift(self, player):
        """Use a dimensional rift for travel"""
        if self.dimensional_rifts:
            rift = self.dimensional_rifts[0]
            rift.uses_remaining -= 1
            
            print(f"\n{Fore.MAGENTA}🌀 Dimensional Rift Activated:{Style.RESET_ALL}")
            print("You step through the rift and find yourself in...")
            print(f"{rift.destination_type}")
            
            # Apply stability effects
            if rift.stability < 0.3:
                player.reality -= random.randint(10, 20)
                player.sanity -= random.randint(5, 15)
                print(f"{Fore.RED}The unstable rift tears at your very being!{Style.RESET_ALL}")
            elif rift.stability < 0.6:
                player.reality -= random.randint(5, 10)
                print(f"{Fore.YELLOW}The rift's instability makes you feel disoriented...{Style.RESET_ALL}")
            else:
                player.memory += random.randint(5, 15)
                print(f"{Fore.GREEN}The stable rift grants you new insights...{Style.RESET_ALL}")
            
            if rift.uses_remaining <= 0:
                self.dimensional_rifts.remove(rift)
                print(f"{Fore.LIGHTBLACK_EX}The rift collapses behind you...{Style.RESET_ALL}")
            
            return True
        return False

    def generate_description(self):
        # Theme-based descriptions
        theme_descriptions = {
            'hospital': [
                (Fore.CYAN + "A sterile hospital room where IV drips count down to unknown procedures, medical charts flutter without wind." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.RED + "A blood-stained operating theater where surgical lights swing hypnotically, casting dancing shadows on abandoned instruments." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.LIGHTGREEN_EX + "A doctor's office where patient files rewrite themselves, diagnoses changing to match your deepest fears." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.WHITE + "An endless hospital corridor where wheelchair tracks lead in circles, the sound of distant breathing echoes from closed rooms." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.LIGHTBLACK_EX + "A reception area where appointment books schedule meetings with the deceased, phones ring with no callers." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTRED_EX + "A trauma bay where heart monitors flatline rhythmically, creating a haunting electronic symphony of death." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.YELLOW + "A pediatric ward where toy blocks spell out final words, teddy bears stare with knowing glass eyes." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.BLUE + "An MRI chamber that scans for souls instead of bones, revealing the fractures in your spirit." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.MAGENTA + "A morgue where toe tags write themselves, listing deaths that haven't happened yet." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.LIGHTCYAN_EX + "A psychiatric ward where padded walls absorb screams from other timelines, medication cups refill with liquid memories." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
            ],
            'school': [
                (Fore.LIGHTYELLOW_EX + "A classroom where chalk writes equations that solve themselves, desks arranged for students who graduated decades ago but never left." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A gymnasium where sneakers squeak on phantom feet, scoreboards count games that span lifetimes, basketballs dribble in perfect rhythm with your heartbeat." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.BLUE + "A science lab where beakers bubble with liquid nostalgia, periodic tables rearrange to spell forgotten names, microscopes reveal memories instead of cells." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.CYAN + "A cafeteria where lunch trays slide across tables by themselves, milk cartons display missing children from tomorrow's newspapers." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.RED + "A detention hall where the clock moves backwards, student desks are carved with confessions that change when you look away." + Style.RESET_ALL, ['door1']),
                (Fore.MAGENTA + "A music room where phantom orchestras perform graduation songs for classes that never were, sheet music writes itself in real-time." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.WHITE + "A locker hallway where combination locks spin to birth dates of the unborn, yearbook photos age in real-time within their frames." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTBLACK_EX + "A principal's office where disciplinary files document future infractions, the intercom announces names of students who haven't enrolled yet." + Style.RESET_ALL, ['door2']),
                (Fore.LIGHTGREEN_EX + "A library where books rewrite their endings based on who's reading, the card catalog sorts itself by emotional weight rather than alphabet." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.LIGHTRED_EX + "An abandoned prom hall where decorations sway to music only the dead can hear, corsages wilt and bloom in endless cycles." + Style.RESET_ALL, ['door2', 'door3'])
            ],
            'home': [
                (Fore.MAGENTA + "A child's bedroom where stuffed animals whisper bedtime stories from lives unlived, music boxes play lullabies that predict nightmares." + Style.RESET_ALL, ['door1']),
                (Fore.LIGHTBLACK_EX + "An attic where photo albums chronicle a family that grows older in reverse, Christmas decorations hang themselves with seasonal precision." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.YELLOW + "A living room where the TV broadcasts home movies of your future, remote controls channel-surf through parallel lives." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.BLUE + "A bathroom where the mirror shows you aging in fast-forward, toothbrushes arrange themselves by the dates of their owners' deaths." + Style.RESET_ALL, ['door1']),
                (Fore.CYAN + "A kitchen where the refrigerator preserves memories instead of food, recipe cards write themselves with ingredients from your past." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A dining room set for a last supper that never ends, chairs pull themselves out when phantom guests arrive for dinner." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.RED + "A basement where the walls bleed condensation shaped like unspoken confessions, storage boxes organize themselves by emotional trauma." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.WHITE + "A study where books rewrite themselves as you read, the words shifting to reveal the reader's deepest regrets." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.LIGHTMAGENTA_EX + "A nursery that prepares itself for children who will never be born, cribs rock empty in rhythm with unborn heartbeats." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.LIGHTRED_EX + "A master bedroom where the bed makes itself with sheets from different timelines, alarm clocks count down to moments of impact." + Style.RESET_ALL, ['door2', 'door3'])
            ],
            'limbo': [
                (Fore.WHITE + "A mirrored labyrinth where each reflection shows a different choice you could have made, fractal infinities of unlived lives stretching beyond comprehension." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.LIGHTBLUE_EX + "A crystalline cavern where each ice formation preserves a moment of pure emotion, the temperature drops as regret accumulates." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.LIGHTMAGENTA_EX + "A gallery of photographs that shift between your memories and someone else's, the frames breathing like living tissue." + Style.RESET_ALL, ['door2']),
                (Fore.LIGHTBLACK_EX + "An infinite void where fragments of consciousness float like islands, each piece containing the last thoughts of the forgotten." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.CYAN + "A gravity-defying chamber where tears fall upward and laughter sinks like stones, the laws of physics bending to emotional weight." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "An impossible forest that grows indoors, each tree bearing fruit that tastes like childhood summers you never experienced." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.YELLOW + "A temporal anomaly room where seconds rewind like film strips, showing the same moment of impact played backwards endlessly." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.RED + "A consciousness chamber where thoughts become visible as smoke, unspoken words hanging in the air like accusations." + Style.RESET_ALL, ['door1', 'door2', 'door4']),
                (Fore.LIGHTCYAN_EX + "A library of unwritten books where empty pages fill themselves with stories of lives that could have been." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.MAGENTA + "A waiting room for the afterlife where appointment numbers are called in languages that predate human speech." + Style.RESET_ALL, ['door2', 'door3'])
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
            ],
            'office': [
                (Fore.LIGHTBLACK_EX + "An endless maze of beige cubicles under harsh fluorescent lighting." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.BLUE + "A conference room with chairs arranged for a meeting that never happened." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.WHITE + "A break room where the coffee pot eternally brews but never fills." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.CYAN + "An executive office overlooking a city that doesn't exist." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.YELLOW + "A copy room where machines run continuously without anyone operating them." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.GREEN + "A server room humming with the sound of computers processing unknown data." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.LIGHTCYAN_EX + "An open office space where keyboards type by themselves." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.MAGENTA + "A reception area where phones ring endlessly but no one answers." + Style.RESET_ALL, ['door1', 'door4'])
            ],
            'hotel': [
                (Fore.RED + "A hotel corridor that stretches infinitely in both directions with identical doors." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.YELLOW + "A lavish lobby with a chandelier that casts no shadows." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.BLUE + "An elevator that plays music for floors that don't exist." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.GREEN + "A hotel room where the bed is always unmade despite housekeeping." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.MAGENTA + "A swimming pool area where the water ripples without wind." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.CYAN + "A ballroom set for a party that ended decades ago." + Style.RESET_ALL, ['door1', 'door2', 'door4']),
                (Fore.WHITE + "A hotel bar where glasses refill themselves with unknown liquids." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.LIGHTRED_EX + "A honeymoon suite with rose petals that never wither." + Style.RESET_ALL, ['door2', 'door4'])
            ],
            'airport': [
                (Fore.BLUE + "An airport terminal with departure boards showing flights to nowhere." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.WHITE + "A waiting area where announcements echo for gates that don't exist." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.YELLOW + "A baggage claim carousel that runs empty in perpetual motion." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.GREEN + "A security checkpoint where metal detectors beep for invisible objects." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.CYAN + "A duty-free shop where products float slightly above their shelves." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.MAGENTA + "A jet bridge extending into empty space with no plane attached." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.LIGHTBLACK_EX + "An air traffic control tower overlooking runways that fade into mist." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.RED + "A passenger lounge with seats that face windows showing only void." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'parking_garage': [
                (Fore.LIGHTBLACK_EX + "A concrete parking garage where your footsteps echo endlessly." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.YELLOW + "A parking level with cars that have no owners and never move." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.GREEN + "A spiral ramp that seems to ascend forever without reaching the top." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.BLUE + "A basement parking level where the ceiling drips with unknown substances." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.RED + "An attendant booth with ticket machines that dispense blank stubs." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.CYAN + "A parking space marked 'Reserved' that seems to call to you." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.WHITE + "A level where all the cars are the same make and model." + Style.RESET_ALL, ['door2', 'door3', 'door4']),
                (Fore.MAGENTA + "An emergency stairwell with numbers that change when you're not looking." + Style.RESET_ALL, ['door1', 'door2'])
            ],
            'subway': [
                (Fore.LIGHTBLACK_EX + "A subway platform where trains arrive but never stop." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.YELLOW + "A tunnel system with tracks that lead in impossible directions." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.BLUE + "A subway car with seats that face each other in infinite reflections." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.GREEN + "A station where the departure board shows times from decades ago." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.RED + "A maintenance tunnel filled with the sound of approaching trains that never come." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.CYAN + "A turnstile area where tokens fall but never hit the ground." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.WHITE + "An underground concourse with shops that sell items from your childhood." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.MAGENTA + "A control room with monitors showing empty trains on endless loops." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'swimming_pool': [
                (Fore.CYAN + "An indoor pool complex where the water is perfectly still despite the filtration." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.BLUE + "A pool deck with lounge chairs arranged for sunbathers who never came." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.WHITE + "A chlorinated changing room where lockers open and close rhythmically." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.YELLOW + "A diving area where the board creaks under invisible weight." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A lap pool with lane ropes that move like they're underwater." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.LIGHTBLUE_EX + "A pool maintenance room where pumps work to clean non-existent debris." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.MAGENTA + "A hot tub that bubbles without heat, creating impossible steam patterns." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.LIGHTCYAN_EX + "A pool office with safety rules posted for activities that never happen." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'warehouse': [
                (Fore.LIGHTBLACK_EX + "A massive warehouse with shelves that extend beyond sight." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.YELLOW + "A loading dock where trucks are always backing up but never arrive." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A storage area with boxes labeled in languages that don't exist." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.BLUE + "A forklift bay where machinery operates without operators." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.RED + "A quality control station where conveyor belts carry invisible products." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.CYAN + "A climate-controlled section humming with precise temperature regulation." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.WHITE + "A shipping area with labels addressed to places that were never built." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.MAGENTA + "An inventory room where barcode scanners beep continuously." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'casino': [
                (Fore.RED + "A casino floor where slot machines play themselves with no one watching." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A poker room with chips that stack themselves on empty tables." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
                (Fore.YELLOW + "A roulette area where the wheel spins eternally but the ball never lands." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.BLUE + "A high-roller section with velvet ropes protecting nothing." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.MAGENTA + "A sports betting area with screens showing games that never happened." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.CYAN + "A cashier's cage where money counts itself behind bulletproof glass." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.WHITE + "A casino restaurant where meals are served to invisible patrons." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.LIGHTRED_EX + "A surveillance room monitoring empty gaming floors through countless cameras." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
            ],
            'theater': [
                (Fore.RED + "A grand theater stage where phantom actors perform eternally for empty seats, their voices echoing through time." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.MAGENTA + "An ornate opera house where the orchestra pit plays melodies that never end, instruments moving by themselves." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.YELLOW + "A dressing room with mirrors reflecting performers who aren't there, makeup applying itself to invisible faces." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.BLUE + "A theater balcony overlooking an audience of shadows, their silent applause creating an eerie rhythm." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A backstage area where props move themselves into position for a show that never begins." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.CYAN + "A projection booth casting scenes from plays that were never written onto an empty screen." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.WHITE + "A rehearsal studio where scripts rewrite themselves as you read them, changing the story with each glance." + Style.RESET_ALL, ['door1', 'door3', 'door4'])
            ],
            'library': [
                (Fore.LIGHTBLACK_EX + "An infinite library where books float between shelves, organizing themselves by emotions rather than alphabet." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
                (Fore.BLUE + "A reading room where open books display blank pages that fill with text when you're not looking directly at them." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.GREEN + "A rare books section where ancient tomes whisper their secrets in languages that predate human speech." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.YELLOW + "A card catalog system where drawers contain index cards for books that don't exist yet." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.MAGENTA + "A children's section where picture books animate themselves, their characters stepping out of pages." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.CYAN + "A reference desk where the librarian is always away, but questions answer themselves on slips of paper." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.RED + "A forbidden section where books scream when opened, their knowledge too dangerous for mortal minds." + Style.RESET_ALL, ['door2', 'door3'])
            ],
            'cathedral': [
                (Fore.WHITE + "A vast cathedral nave where stained glass windows depict your life's pivotal moments in brilliant color." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.YELLOW + "A cathedral altar where candles light themselves and prayers echo from voices you can't see." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.BLUE + "A confession booth where sins are absolved before they're even spoken, the priest's voice coming from empty air." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.RED + "A cathedral crypt where tomb inscriptions change to show the names of people you know." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.MAGENTA + "A bell tower where phantom bells ring the hours for times that don't exist on any clock." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.GREEN + "A cathedral garden where stone angels weep tears that evaporate before touching the ground." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.LIGHTCYAN_EX + "A choir loft where invisible voices sing hymns in harmonies that make your soul ache with longing." + Style.RESET_ALL, ['door1', 'door3', 'door4'])
            ],
            'laboratory': [
                (Fore.LIGHTGREEN_EX + "A sterile laboratory where beakers bubble with liquids that defy the laws of chemistry, creating impossible reactions." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.CYAN + "A research facility where microscopes reveal universes within droplets of water, each containing civilizations." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.WHITE + "An experimental chamber where test subjects' memories are stored in glass containers, glowing with ethereal light." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.YELLOW + "A laboratory where equations write themselves on whiteboards, solving the mysteries of existence." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.RED + "A containment facility where failed experiments pace in their cells, reaching through bars that shouldn't exist." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.MAGENTA + "A clean room where the air itself seems alive, responding to your thoughts and fears." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.BLUE + "An observation deck overlooking experiments that test the boundaries between life and death." + Style.RESET_ALL, ['door1', 'door3', 'door4'])
            ],
            'museum': [
                (Fore.LIGHTBLACK_EX + "A natural history museum where dinosaur skeletons reassemble themselves when no one is watching." + Style.RESET_ALL, ['door1', 'door2']),
                (Fore.YELLOW + "An art gallery where paintings change their subjects based on who's viewing them, showing personal truths." + Style.RESET_ALL, ['door1', 'door3']),
                (Fore.BLUE + "A museum of lost things where every item you've ever misplaced is displayed with a placard explaining why you lost it." + Style.RESET_ALL, ['door2', 'door4']),
                (Fore.RED + "A war memorial section where the names on monuments rewrite themselves with casualties from conflicts yet to come." + Style.RESET_ALL, ['door1', 'door4']),
                (Fore.GREEN + "A cultural artifacts wing where ancient objects pulse with the memories of their original owners." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
                (Fore.MAGENTA + "A planetarium where the star show displays constellations from the night sky of your birth, then shows how they'll look when you die." + Style.RESET_ALL, ['door2', 'door3']),
                (Fore.CYAN + "A museum gift shop where souvenirs are memories you can purchase, each one changing your past slightly." + Style.RESET_ALL, ['door1', 'door3', 'door4'])
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
            ],
            'office': [
                "There's a corporate staircase leading to upper management floors.",
                "A service stairwell descends to the basement archives.",
                "Both main and emergency staircases are accessible.",
                "No exit signs visible in this corporate maze.",
                "A modern glass staircase spirals to the executive level.",
                "Blocked stairs with 'Authorized Personnel Only' signs."
            ],
            'hotel': [
                "There's an elegant staircase leading to luxury suites.",
                "A narrow service stairwell descends to the basement levels.",
                "Both guest and staff staircases are visible.",
                "No clear exit routes from this floor.",
                "A grand marble staircase winds to the penthouse.",
                "Fire escape stairs that seem to lead nowhere."
            ],
            'airport': [
                "There's a staircase leading to the upper departure level.",
                "A maintenance stairwell descends to baggage handling.",
                "Both passenger and service staircases are accessible.",
                "No emergency exit signs visible anywhere.",
                "An escalator that moves upward indefinitely.",
                "Blocked stairs with 'Airport Personnel Only' barriers."
            ],
            'parking_garage': [
                "There's a concrete stairwell leading to upper parking levels.",
                "A dark staircase descends deeper underground.",
                "Both main and emergency stairwells are visible.",
                "No exit signs can be found in this concrete maze.",
                "A spiral ramp that doubles as stairs to nowhere.",
                "Blocked stairs with warning tape and strange symbols."
            ],
            'subway': [
                "There's a subway staircase leading to street level.",
                "A maintenance stairwell descends to the tunnel systems.",
                "Both public and service staircases are accessible.",
                "No exit signs visible in this underground maze.",
                "A spiral staircase that echoes with phantom footsteps.",
                "Blocked stairs marked 'Danger: Track Work' but no workers."
            ],
            'swimming_pool': [
                "There's a staircase leading to the observation deck.",
                "A service stairwell descends to the pump room.",
                "Both main and emergency staircases are visible.",
                "No pool exit signs can be found anywhere.",
                "A diving platform staircase that extends impossibly high.",
                "Blocked stairs with 'Pool Maintenance' signs but no workers."
            ],
            'warehouse': [
                "There's an industrial staircase leading to the office level.",
                "A loading dock stairwell descends to the basement.",
                "Both main and service staircases are accessible.",
                "No exit signs visible in this industrial complex.",
                "A metal spiral staircase winds around support beams.",
                "Blocked stairs with 'Inventory Access Only' barriers."
            ],
            'casino': [
                "There's a carpeted staircase leading to VIP floors.",
                "A service stairwell descends to the vault level.",
                "Both guest and staff staircases are visible.",
                "No exit signs visible through the flashing lights.",
                "An ornate staircase winds to private gaming rooms.",
                "Blocked stairs with 'High Roller Access Only' velvet ropes."
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
            ],
            'office': [
                "Corporate hallways extend in perfectly straight lines.",
                "Only the elevator bank and conference room wing are accessible.",
                "Left leads to cubicles, right to executive offices.",
                "A single corridor stretches toward the break room.",
                "A narrow pathway winds through endless workstations.",
                "A wide hallway lined with identical office doors."
            ],
            'hotel': [
                "Hotel corridors stretch infinitely in both directions.",
                "Only the elevator area and guest wing are accessible.",
                "Left leads to the pool area, right to the restaurant.",
                "A single hallway continues toward the lobby.",
                "A narrow service corridor twists behind the scenes.",
                "A wide carpeted hallway with identical room doors."
            ],
            'airport': [
                "Terminal concourses extend endlessly in all directions.",
                "Only the main terminal and gate areas are accessible.",
                "Left leads to departures, right to arrivals.",
                "A single moving walkway continues forward.",
                "A narrow corridor winds past empty gate areas.",
                "A wide terminal hallway stretches toward security."
            ],
            'parking_garage': [
                "Concrete ramps spiral in impossible directions.",
                "Only the main level and basement are accessible.",
                "Left leads to compact cars, right to reserved spaces.",
                "A single driving lane continues through empty spaces.",
                "A narrow pathway weaves between parked vehicles.",
                "A wide driving lane stretches toward the exit."
            ],
            'subway': [
                "Underground tunnels branch in all directions.",
                "Only the platform and main tunnel are accessible.",
                "Left leads to uptown trains, right to downtown.",
                "A single tunnel continues into darkness.",
                "A narrow maintenance tunnel twists alongside tracks.",
                "A wide platform stretches along abandoned tracks."
            ],
            'swimming_pool': [
                "Pool decks extend around the water in all directions.",
                "Only the main pool and changing area are accessible.",
                "Left leads to the diving area, right to the lap pool.",
                "A single walkway continues around the pool edge.",
                "A narrow pathway winds past empty lounge chairs.",
                "A wide deck area stretches toward the pool entrance."
            ],
            'warehouse': [
                "Industrial aisles extend between towering shelves.",
                "Only the main floor and loading dock are accessible.",
                "Left leads to storage, right to shipping areas.",
                "A single aisle continues deep into the warehouse.",
                "A narrow pathway weaves between inventory stacks.",
                "A wide corridor stretches toward the office area."
            ],
            'casino': [
                "Gaming floors extend in all directions under neon lights.",
                "Only the main floor and high-roller area are accessible.",
                "Left leads to slot machines, right to table games.",
                "A single pathway continues toward the cashier.",
                "A narrow corridor winds past empty gaming tables.",
                "A wide promenade stretches toward the restaurant."
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
            ],
            'office': [
                ("A computer monitor still glowing.", "The screen shows your browsing history from tomorrow..."),
                ("A coffee mug with steam still rising.", "The coffee never gets cold no matter how long you wait..."),
                ("A desk nameplate with your name.", "But you've never worked here before..."),
                ("A filing cabinet drawer slightly open.", "Inside are documents about your life you never filed..."),
                ("A photocopier running by itself.", "It's copying photos of you sleeping..."),
                ("A motivational poster on the wall.", "The text changes to personal messages as you read..."),
                ("A telephone that rings incessantly.", "When answered, you hear your own voice from years ago..."),
                None
            ],
            'hotel': [
                ("A guest registry book open on the desk.", "Your signature appears repeatedly throughout history..."),
                ("A key card lying on the dresser.", "It opens rooms that don't exist on the floor plan..."),
                ("A room service tray outside a door.", "The food is still warm despite being there for hours..."),
                ("A 'Do Not Disturb' sign that moves.", "It hangs itself on doors you haven't approached..."),
                ("A hotel phone that dials by itself.", "It calls rooms occupied by different versions of you..."),
                ("A Bible in the nightstand drawer.", "All the text has been replaced with your memories..."),
                ("A bathroom mirror that fogs up alone.", "Words appear in the condensation: 'Welcome back'..."),
                None
            ],
            'airport': [
                ("A boarding pass on an empty seat.", "It has your name but a destination you've never heard of..."),
                ("A luggage tag from an unclaimed bag.", "The address is your childhood home from decades ago..."),
                ("A flight information screen.", "Departure times count down but never reach zero..."),
                ("An abandoned coffee cup still warm.", "The lipstick stain matches yours perfectly..."),
                ("A passport left at security.", "The photo looks like you but the details are all wrong..."),
                ("An intercom that crackles to life.", "It announces your arrival at gates that don't exist..."),
                ("A departure gate sign.", "The destination changes to places from your dreams..."),
                None
            ],
            'parking_garage': [
                ("A parking ticket under a windshield.", "It's addressed to you but dated years in the future..."),
                ("Car keys dangling from an ignition.", "They fit a car you used to own but sold long ago..."),
                ("A security camera that follows you.", "Its red light blinks in sync with your heartbeat..."),
                ("An oil stain on the concrete.", "It's shaped exactly like your shadow..."),
                ("A parking space painted with your name.", "But you've never reserved a spot here..."),
                ("A car alarm that won't stop.", "It's coming from a car that looks exactly like yours..."),
                ("An elevator call button.", "It glows but the elevator never comes..."),
                None
            ],
            'subway': [
                ("A MetroCard left on a turnstile.", "It has unlimited rides but your name printed on it..."),
                ("A newspaper blowing in the wind.", "The headlines are all about events in your life..."),
                ("A bench with a warm spot.", "It feels like someone just stood up when you approach..."),
                ("Graffiti on the tunnel wall.", "It spells out your childhood nickname..."),
                ("A dropped wallet on the platform.", "It contains your ID but with a different address..."),
                ("Track maintenance equipment.", "It's working on rails that lead to your hometown..."),
                ("A train map on the wall.", "New stops appear showing places from your past..."),
                None
            ],
            'swimming_pool': [
                ("A pool float drifting alone.", "It's the exact one you had as a child..."),
                ("Goggles left on the pool deck.", "When you look through them, you see underwater cities..."),
                ("A lifeguard chair facing the wrong way.", "The whistle still echoes though no one is there..."),
                ("Pool chemicals perfectly balanced.", "The water changes color to match your mood..."),
                ("A diving board that creaks.", "It bends under invisible weight as you watch..."),
                ("Lane ropes that move on their own.", "They form patterns that spell out your name..."),
                ("A pool maintenance log.", "Your name appears as the last person to swim here..."),
                None
            ],
            'warehouse': [
                ("A shipping label on a box.", "It's addressed to you at an address you've never lived at..."),
                ("A forklift with keys in the ignition.", "It starts when you approach, then turns off..."),
                ("An inventory clipboard.", "It lists items from your childhood room..."),
                ("A packing slip blowing in the breeze.", "It details an order you never placed..."),
                ("A loading dock schedule.", "Your name appears as driver for tomorrow's delivery..."),
                ("A safety poster on the wall.", "The safety tips are actually life advice meant for you..."),
                ("A time clock punched with your name.", "But you've never worked here..."),
                None
            ],
            'casino': [
                ("A poker chip on the floor.", "It has your initials and a date from your birth..."),
                ("A slot machine paying out constantly.", "The coins that fall have your face on them..."),
                ("A players club card.", "It has your photo but shows millions in winnings..."),
                ("A cocktail glass with lipstick stain.", "The color matches lipstick you wore yesterday..."),
                ("A dealer's visor left behind.", "When you put it on, you can see everyone's cards..."),
                ("A craps table with dice frozen mid-roll.", "They show numbers that match important dates in your life..."),
                ("A surveillance monitor.", "It shows you entering the casino, but you don't remember arriving..."),
                None
            ],
            'theater': [
                ("A vintage playbill on the floor.", "It advertises a show starring you in the lead role..."),
                ("A spotlight that follows you.", "Its beam never leaves you no matter where you move..."),
                ("An empty director's chair.", "Your name is embroidered on the back in golden thread..."),
                ("A makeup mirror with lights.", "It reflects someone else wearing your face..."),
                ("Sheet music scattered about.", "The notes spell out your life story when read together..."),
                ("A phantom's mask on a stand.", "When you touch it, you hear your own voice singing..."),
                ("A program from tonight's show.", "The cast list includes everyone you've ever loved..."),
                None
            ],
            'library': [
                ("A bookmark in an open book.", "It marks a page describing your exact current situation..."),
                ("A library card on the desk.", "It expires on the day you're supposed to die..."),
                ("Reading glasses left behind.", "When you wear them, you can read books in languages you don't know..."),
                ("A stamp pad for returns.", "The ink changes color based on your deepest regrets..."),
                ("A card catalog drawer.", "It contains only cards with your name and different life paths..."),
                ("An overdue notice.", "It's for a book about your life that you never checked out..."),
                ("A librarian's nameplate.", "It keeps changing to names of people who've influenced you..."),
                None
            ],
            'cathedral': [
                ("A prayer book left open.", "The prayer written there is exactly what you need to hear..."),
                ("A donation candle.", "It lights itself whenever you think of someone you've lost..."),
                ("A confessional schedule.", "Your name is listed for an appointment you never made..."),
                ("Holy water in a font.", "Your reflection in it shows you as a child..."),
                ("A hymnal with torn pages.", "The remaining songs are all from important moments in your life..."),
                ("A collection plate.", "It contains coins from every year you've been alive..."),
                ("A stained glass shard.", "It depicts a scene from your future..."),
                None
            ],
            'laboratory': [
                ("A test tube with your blood.", "The label says it was drawn tomorrow..."),
                ("A research journal.", "The latest entry describes experiments being done on you..."),
                ("Safety goggles on a hook.", "When you wear them, you can see the molecular structure of emotions..."),
                ("A petri dish growing something.", "The culture forms patterns that match your fingerprints..."),
                ("A clipboard with data.", "The statistics are all about your life choices and their outcomes..."),
                ("A microscope focused on a slide.", "It shows memories instead of cells when you look through it..."),
                ("A chemical formula on the board.", "It's the exact combination that would erase your existence..."),
                None
            ],
            'museum': [
                ("A museum guide pamphlet.", "It offers tours through different periods of your life..."),
                ("An exhibit placard.", "It describes you as if you were already a historical figure..."),
                ("A donation box.", "The suggested amount is exactly what you have in your pocket..."),
                ("A velvet rope barrier.", "It cordons off a display case containing your childhood toys..."),
                ("A museum visitor badge.", "It has your photo but lists you as 'Deceased Patron'..."),
                ("An audio guide headset.", "It plays recordings of conversations you had in private..."),
                ("A guest book to sign.", "Your signature is already there, dated years in the future..."),
                None
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
        self.sanity = int(sanity)
        self.reality_coherence = REALITY_MAX
        self.memory_stability = MEMORY_MAX
        # Add aliases for compatibility
        self.reality = REALITY_MAX
        self.memory = MEMORY_MAX
        self.temporal_awareness = 100
        self.has_light = False
        self.level = level
        self.entity_encounters = 0
        self.anomaly_exposures = 0
        self.deepest_level = 0
        self.psychological_state = "stable"
        self.last_entity_encounter = None
        self.active_effects = []
        # Additional attributes needed by the game
        self.moves_made = 0
        self.artifacts = []
        self.entity_relationships = {}
        self.status_effects = []
        # Initialize with proper objects instead of None to fix type compatibility
        self.journal = Journal() if 'Journal' in globals() else None
        self.quest_system = QuestSystem() if 'QuestSystem' in globals() else None

    def move(self, direction):
        """Move player in the specified direction"""
        if direction in directions:
            dx, dy, dz = directions[direction]
            self.x += dx
            self.y += dy
            self.z += dz
            self.moves_made += 1
            
            # Ensure boundaries
            self.x = max(X_MIN, min(X_MAX, self.x))
            self.y = max(Y_MIN, min(Y_MAX, self.y))
            self.z = max(Z_MIN, min(Z_MAX, self.z))

    def update_psychological_state(self):
        """Update psychological state based on various metrics"""
        if self.sanity < 20:
            self.psychological_state = "critical_breakdown"
        elif self.sanity < 40:
            self.psychological_state = "severe_distress"
        elif self.sanity < 60:
            self.psychological_state = "unstable"
        elif self.sanity < 80:
            self.psychological_state = "deteriorating"
        else:
            self.psychological_state = "stable"

        # Reality coherence affects perception
        if self.reality_coherence < 30:
            self.psychological_state += "_reality_fragmenting"
        elif self.reality_coherence < 60:
            self.psychological_state += "_reality_unstable"

    def apply_entity_effects(self, entity):
        """Apply effects from entity encounters"""
        if entity.behavior == "follows_player":
            self.sanity -= random.randint(2, 5)
            self.reality_coherence -= random.randint(1, 3)
        elif entity.behavior == "reality_distortion":
            self.reality_coherence -= random.randint(5, 10)
            self.temporal_awareness -= random.randint(3, 7)
        elif entity.behavior == "temporal_manipulation":
            self.temporal_awareness -= random.randint(8, 15)
            self.memory_stability -= random.randint(5, 10)
        elif entity.behavior == "constant_surveillance":
            self.sanity -= random.randint(3, 8)

        self.entity_encounters += 1
        self.last_entity_encounter = entity.name
        self.update_psychological_state()

    def apply_anomaly_effects(self, anomaly):
        """Apply effects from anomaly exposure"""
        if anomaly.effect == "time_loop":
            self.temporal_awareness -= random.randint(10, 20)
            self.memory_stability -= random.randint(5, 15)
        elif anomaly.effect == "physics_distortion":
            self.reality_coherence -= random.randint(8, 15)
            self.sanity -= random.randint(3, 8)
        elif anomaly.effect == "memory_manifestation":
            self.memory_stability -= random.randint(10, 25)
            self.sanity -= random.randint(5, 12)
        elif anomaly.effect == "dimensional_breach":
            self.reality_coherence -= random.randint(15, 30)
            self.sanity -= random.randint(8, 15)

        self.anomaly_exposures += 1
        self.update_psychological_state()

    def get_status_display(self):
        """Get colored status display"""
        status_parts = []

        # Sanity with color coding
        if self.sanity >= 80:
            sanity_color = Fore.GREEN
        elif self.sanity >= 60:
            sanity_color = Fore.YELLOW
        elif self.sanity >= 40:
            sanity_color = Fore.LIGHTRED_EX
        else:
            sanity_color = Fore.RED + Style.BRIGHT

        status_parts.append(f"{sanity_color}Sanity: {self.sanity}/100{Style.RESET_ALL}")

        # Reality Coherence
        if self.reality_coherence >= 80:
            reality_color = Fore.CYAN
        elif self.reality_coherence >= 60:
            reality_color = Fore.YELLOW
        elif self.reality_coherence >= 40:
            reality_color = Fore.LIGHTRED_EX
        else:
            reality_color = Fore.MAGENTA + Style.BRIGHT

        status_parts.append(f"{reality_color}Reality: {self.reality_coherence}/100{Style.RESET_ALL}")

        # Memory Stability
        if self.memory_stability >= 80:
            memory_color = Fore.LIGHTBLUE_EX
        elif self.memory_stability >= 60:
            memory_color = Fore.YELLOW
        else:
            memory_color = Fore.LIGHTRED_EX

        status_parts.append(f"{memory_color}Memory: {self.memory_stability}/100{Style.RESET_ALL}")

        return " | ".join(status_parts)

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

# Advanced Psychological Profile System
class PsychologicalProfile:
    def __init__(self):
        self.fear_triggers = []
        self.comfort_zones = []
        self.phobias = {}
        self.coping_mechanisms = []
        self.trauma_responses = []
        self.personality_traits = {}
        self.emotional_state = "neutral"
        self.stress_level = 0
        self.adaptation_rate = 1.0
        self.reality_anchor_strength = 100
        
    def analyze_player_responses(self, responses):
        """Analyze player choices to build psychological profile"""
        fear_indicators = {
            "darkness": ["avoid", "hide", "flee", "close eyes"],
            "isolation": ["seek company", "call out", "group together"],
            "unknown": ["hesitate", "investigate cautiously", "avoid"],
            "heights": ["stay low", "avoid stairs", "ground level"],
            "confined_spaces": ["open doors", "find exits", "avoid small rooms"]
        }
        
        for fear_type, indicators in fear_indicators.items():
            for response in responses:
                if any(indicator in response.lower() for indicator in indicators):
                    if fear_type not in self.fear_triggers:
                        self.fear_triggers.append(fear_type)
        
        self.update_emotional_state()
    
    def update_emotional_state(self):
        """Update emotional state based on current fears and stress"""
        if self.stress_level > 80:
            self.emotional_state = "panic"
        elif self.stress_level > 60:
            self.emotional_state = "high_anxiety"
        elif self.stress_level > 40:
            self.emotional_state = "nervous"
        elif self.stress_level > 20:
            self.emotional_state = "uneasy"
        else:
            self.emotional_state = "calm"

# Advanced Environmental Storytelling System
class EnvironmentalNarrative:
    def __init__(self):
        self.story_fragments = []
        self.environmental_clues = []
        self.narrative_threads = {}
        self.backstory_elements = []
        
    def generate_environmental_story(self, room_theme, atmospheric_intensity):
        """Generate rich environmental storytelling based on context"""
        
        narrative_templates = {
            'hospital': {
                'high_intensity': [
                    "Patient charts scattered on the floor tell stories of lives interrupted mid-treatment, their final entries trailing off into illegible scrawls",
                    "A surgery schedule still displays tomorrow's operations, but the dates are from decades ago and the doctors' names have faded to whispers",
                    "IV bags hang like deflated balloons, their contents long evaporated, leaving only the ghost of healing that never came",
                    "Medical equipment hums with phantom electricity, displaying vital signs for patients who checked out of reality long ago"
                ],
                'medium_intensity': [
                    "Wheelchairs arranged in perfect rows face a television that plays static, as if waiting for programming from another dimension",
                    "A nurse's station holds coffee cups with lipstick stains that refresh themselves when you're not looking",
                    "Prescription bottles rattle with pills that change color based on your current ailments",
                    "Hospital beds make themselves with sheets that smell like memories of recovery"
                ],
                'low_intensity': [
                    "Gentle beeping from unseen monitors creates a soothing rhythm like a mechanical lullaby",
                    "Fresh flowers on bedside tables bloom and wilt in fast-forward cycles",
                    "Reading materials in the waiting area update themselves with articles about your health concerns",
                    "Vending machines hum contentedly, occasionally dispensing free comfort food"
                ]
            },
            'school': {
                'high_intensity': [
                    "Classroom blackboards write themselves with lessons in subjects that don't exist, teaching knowledge too dangerous for minds to hold",
                    "Student desks bear the carved initials of children who aged backwards, their memories trapped in permanent detention",
                    "School bells ring in morse code, spelling out the names of students who never graduated because they never existed",
                    "Lockers slam shut on their own, protecting secrets that could unravel the fabric of adolescent reality"
                ],
                'medium_intensity': [
                    "Paper airplanes fold themselves and fly through halls, carrying messages between classrooms full of empty desks",
                    "School announcements echo through speakers, calling students to assemblies in gymnasiums that expand beyond physical possibility",
                    "Cafeteria trays slide across tables, serving meals that taste like every lunch you ever ate in school",
                    "Library books reshelve themselves, organizing by the emotional impact of their stories rather than alphabetical order"
                ],
                'low_intensity': [
                    "Pencil sharpeners turn themselves, creating perfect points for homework that writes itself",
                    "Hall monitors made of shadow patrol the corridors, nodding approvingly at well-behaved visitors",
                    "Art supplies arrange themselves into projects that reflect your inner child's creativity",
                    "Music rooms play gentle melodies from school concerts you might have attended in another life"
                ]
            },
            'home': {
                'high_intensity': [
                    "Family photos rearrange themselves on walls, showing holiday gatherings where your face appears in pictures from before you were born",
                    "Kitchen tables set themselves for dinners with empty chairs that hold the weight of conversations never finished",
                    "Childhood bedrooms preserve toys that play with themselves, reenacting scenarios from the imagination of a child who never grew up",
                    "Basement stairs creak under the footsteps of family members who moved away but left their emotional echoes behind"
                ],
                'medium_intensity': [
                    "Television channels flip through home movies of families you recognize but have never met",
                    "Refrigerator magnets spell out shopping lists for groceries needed by the family that lives here in parallel time",
                    "Rocking chairs move with the rhythm of lullabies sung by mothers in dimensions adjacent to this one",
                    "Window curtains open and close with the daily routine of residents who exist only in the muscle memory of the house"
                ],
                'low_intensity': [
                    "Cozy blankets fold themselves over furniture, creating nest-like spaces that offer comfort to weary travelers",
                    "Kitchen appliances brew tea and prepare snacks for visitors, anticipating needs before they're voiced",
                    "Family portraits smile warmly, their eyes following you with genuine affection rather than supernatural menace",
                    "Fireplaces light themselves when you enter, casting warm shadows that feel like embraces from loved ones"
                ]
            }
        }
        
        intensity_level = "high_intensity" if atmospheric_intensity > 0.7 else "medium_intensity" if atmospheric_intensity > 0.4 else "low_intensity"
        
        if room_theme in narrative_templates:
            stories = narrative_templates[room_theme][intensity_level]
            return random.choice(stories)
        
        return "The space holds stories written in the language of abandonment and possibility."

# Comprehensive Liminal Entity System
class LiminalEntityManager:
    def __init__(self):
        self.entity_registry = {}
        self.behavior_patterns = {}
        self.interaction_history = []
        self.entity_relationships = {}
        
    def create_complex_entities(self):
        """Create sophisticated entities with deep behavioral patterns"""
        
        complex_entities = {
            'the_archivist': Entity(
                "The Archivist",
                "A figure composed of filing cabinets and index cards, organizing memories that don't belong to anyone",
                "memory_cataloging",
                threat_level=1
            ),
            'temporal_maintenance_worker': Entity(
                "Temporal Maintenance Worker",
                "A janitor who cleans up temporal paradoxes, mopping floors that exist in multiple timelines simultaneously",
                "reality_maintenance",
                threat_level=2
            ),
            'the_photographer': Entity(
                "The Photographer",
                "An entity that captures moments that never happened, developing photos in darkrooms lit by impossible light",
                "moment_preservation",
                threat_level=1
            ),
            'dream_architect': Entity(
                "Dream Architect",
                "A being that constructs the architecture of sleeping minds, designing rooms that exist only in REM sleep",
                "subconscious_construction",
                threat_level=3
            ),
            'memory_merchant': Entity(
                "Memory Merchant",
                "A trader who deals in forgotten moments, offering to buy memories you no longer want",
                "memory_commerce",
                threat_level=2
            ),
            'the_receptionist': Entity(
                "The Receptionist",
                "An eternally professional figure at a desk that appears in every liminal waiting area",
                "eternal_service",
                threat_level=1
            ),
            'shadow_therapist': Entity(
                "Shadow Therapist",
                "A counselor made of shifting darkness who helps souls process their transition between realities",
                "psychological_guidance",
                threat_level=1
            ),
            'the_lost_child': Entity(
                "The Lost Child",
                "A young figure who knows every secret passage in the liminal spaces but can never find their way home",
                "guidance_seeker",
                threat_level=1
            ),
            'reality_inspector': Entity(
                "Reality Inspector",
                "An official who checks the structural integrity of existence, citing violations of physics",
                "dimensional_regulation",
                threat_level=2
            ),
            'the_night_shift': Entity(
                "The Night Shift",
                "A collection of workers who maintain the liminal spaces while the normal world sleeps",
                "nocturnal_maintenance",
                threat_level=1
            )
        }
        
        # Add behavioral patterns for each entity
        self.behavior_patterns = {
            'memory_cataloging': {
                'description': "Sorts through scattered memories, filing them in impossible filing systems",
                'interactions': ["offers to organize your memories", "shows you files of people you've forgotten", "asks for documentation of your experiences"],
                'effects': {'memory': +10, 'reality': -5}
            },
            'reality_maintenance': {
                'description': "Fixes tears in the fabric of space-time with mundane cleaning supplies",
                'interactions': ["warns about reality hazards", "offers to clean up paradoxes you've created", "provides safety equipment for dimensional travel"],
                'effects': {'reality': +15, 'sanity': +5}
            },
            'moment_preservation': {
                'description': "Captures fleeting moments in photographs that develop into different images each time you look",
                'interactions': ["asks to photograph you", "shows pictures of moments you've never experienced", "offers to develop your mental snapshots"],
                'effects': {'memory': +20, 'sanity': -10}
            },
            'subconscious_construction': {
                'description': "Builds and rebuilds the architecture of dreams and nightmares",
                'interactions': ["redesigns rooms based on your fears", "offers blueprints for dream houses", "explains the structural requirements of nightmares"],
                'effects': {'sanity': -15, 'reality': -10, 'memory': +5}
            },
            'memory_commerce': {
                'description': "Trades in the currency of forgotten experiences and lost time",
                'interactions': ["offers to buy painful memories", "sells experiences you've never had", "trades memories for peace of mind"],
                'effects': {'memory': -10, 'sanity': +15}
            }
        }
        
        return complex_entities

# Advanced Room Evolution System
class RoomEvolution:
    def __init__(self):
        self.evolution_stages = {}
        self.transformation_triggers = {}
        self.room_memory = {}
        
    def evolve_room_based_on_visits(self, room, visit_count):
        """Rooms change and evolve based on how many times they've been visited"""
        
        evolution_stages = {
            1: "pristine",
            3: "lived_in", 
            7: "worn",
            15: "deteriorating",
            30: "liminal_merge",
            50: "reality_breakdown"
        }
        
        stage = "pristine"
        for threshold, stage_name in sorted(evolution_stages.items()):
            if visit_count >= threshold:
                stage = stage_name
        
        room_transformations = {
            'hospital': {
                'pristine': "The hospital room is spotlessly clean with fresh sheets and working equipment",
                'lived_in': "The room shows signs of use - wrinkled sheets, used tissues, a warm impression on the bed",
                'worn': "Paint peels from walls, equipment shows wear, and there's a persistent antiseptic smell mixed with decay",
                'deteriorating': "Medical equipment sparks and fails, water stains spread across ceiling tiles, and the floor tiles curl at the edges",
                'liminal_merge': "The room exists in multiple time periods simultaneously - new equipment phases in and out with vintage medical tools",
                'reality_breakdown': "The room's purpose becomes fluid - sometimes a hospital room, sometimes a laboratory, sometimes a morgue, changing based on observation"
            },
            'school': {
                'pristine': "The classroom is organized with fresh chalk, clean desks, and educational posters on the walls",
                'lived_in': "Desks show pencil marks, the chalkboard has eraser smudges, and there's the faint sound of children's voices",
                'worn': "Desks are carved with initials, posters fade and curl, and the chalkboard is permanently stained with ghost images",
                'deteriorating': "Ceiling tiles sag, desks are broken, and textbooks crumble when touched",
                'liminal_merge': "The classroom exists in multiple school years - holiday decorations from different seasons appear simultaneously",
                'reality_breakdown': "The room's academic level fluctuates - kindergarten toys appear next to advanced calculus equations"
            },
            'home': {
                'pristine': "The living room is perfectly arranged with fresh flowers and recently dusted furniture",
                'lived_in': "Cushions show indentations, magazines are scattered, and there's the warmth of recent habitation",
                'worn': "Furniture is faded, family photos are slightly askew, and there's a persistent sense of nostalgia",
                'deteriorating': "Wallpaper peels, floorboards creak ominously, and memories seem to leak from the walls",
                'liminal_merge': "The room exists in multiple time periods of the family's life - childhood toys appear next to elderly care equipment",
                'reality_breakdown': "The room's inhabitants phase in and out of existence - voices from different decades overlap and blend"
            }
        }
        
        if room.theme in room_transformations:
            transformation = room_transformations[room.theme].get(stage, "The space has evolved beyond recognition")
            return transformation, stage
        
        return "The room has changed in ways that defy description", stage

# Comprehensive Sensory Experience System
class SensoryExperience:
    def __init__(self):
        self.sound_library = {}
        self.smell_library = {}
        self.texture_library = {}
        self.visual_effects = {}
        self.synesthetic_experiences = {}
        
    def generate_layered_sensory_experience(self, room_theme, atmospheric_intensity, emotional_state):
        """Create multi-layered sensory experiences that respond to player state"""
        
        sound_experiences = {
            'hospital': {
                'ambient': ["distant beeping of heart monitors", "whispered conversations in foreign languages", "the squeak of wheels on linoleum", "air conditioning that sounds like breathing"],
                'interactive': ["doors that sigh when opened", "elevators that hum lullabies", "phones ringing with static-filled conversations", "medical equipment that responds to your heartbeat"],
                'supernatural': ["echoes of surgeries from other timelines", "the sound of healing happening in reverse", "phantom code blues called for empty rooms", "whispers of medical advice from doctors who don't exist"]
            },
            'school': {
                'ambient': ["chalk dust settling in sunbeams", "distant school bells from parallel timelines", "the rustle of papers that write themselves", "lockers opening and closing in rhythm"],
                'interactive': ["desks that creak with the weight of student stress", "chalkboards that screech when touched", "pencil sharpeners that grind out anxious thoughts", "doors that open to different classrooms based on your knowledge level"],
                'supernatural': ["ghostly recitations of lessons never taught", "the sound of tests being graded in empty rooms", "phantom graduations for students who never existed", "whispers of homework assignments from subjects yet to be invented"]
            },
            'theater': {
                'ambient': ["velvet curtains rustling with phantom wind", "the creak of old theater seats adjusting themselves", "distant applause from audiences in other dimensions", "the whisper of costumes organizing themselves"],
                'interactive': ["spotlights that follow your movement", "musical instruments that play when you approach", "microphones that amplify your thoughts", "stage floors that echo with the footsteps of every performer who ever walked them"],
                'supernatural': ["standing ovations for shows that never happened", "the sound of reviews being written by critics who don't exist", "phantom rehearsals of plays from the future", "whispers of lines from scripts that write themselves"]
            }
        }
        
        smell_experiences = {
            'hospital': [
                "antiseptic mixed with the metallic scent of fear",
                "flowers from a gift shop that exists in memory only",
                "the ozone smell of electrical equipment mixed with human hope",
                "cleaning supplies that smell like the desire for healing"
            ],
            'school': [
                "chalk dust mixed with the anxiety of test days",
                "cafeteria food that smells like childhood security",
                "old textbooks mixed with the excitement of learning",
                "gym clothes mixed with the fear of being chosen last"
            ],
            'home': [
                "cooking dinner mixed with the warmth of belonging",
                "laundry detergent mixed with the comfort of clean sheets",
                "air freshener mixed with the effort to make things perfect",
                "dust mixed with the passage of time and memory"
            ]
        }
        
        texture_experiences = {
            'hospital': [
                "walls that feel slightly warm, as if absorbing body heat from patients",
                "floors that are somehow both slippery and sticky simultaneously",
                "surfaces that feel sanitized but retain the texture of human touch",
                "equipment that's cold to the touch but radiates emotional warmth"
            ],
            'school': [
                "desk surfaces carved with the hopes and fears of students",
                "chalkboards that feel like the texture of accumulated knowledge",
                "walls that hold the vibrations of every lecture ever given",
                "floors that feel worn smooth by generations of nervous feet"
            ],
            'home': [
                "furniture that molds itself to your body like familiar comfort",
                "walls that feel warm with accumulated family conversations",
                "surfaces that retain the texture of every loving touch",
                "floors that feel solid with the foundation of shared memories"
            ]
        }
        
        # Select experiences based on theme and intensity
        sounds = sound_experiences.get(room_theme, {})
        smells = smell_experiences.get(room_theme, [])
        textures = texture_experiences.get(room_theme, [])
        
        experience = {
            'sounds': random.choice(sounds.get('ambient', [])) if sounds else "silence that holds its breath",
            'smells': random.choice(smells) if smells else "the absence of scent, as if smell itself has forgotten this place",
            'textures': random.choice(textures) if textures else "surfaces that feel like the texture of forgotten dreams"
        }
        
        return experience

# Philosophical Dialogue System
class PhilosophicalDialogue:
    def __init__(self):
        self.dialogue_trees = {}
        self.philosophical_themes = {}
        self.player_worldview = {}
        
    def generate_existential_conversations(self):
        """Generate deep philosophical conversations with liminal entities"""
        
        philosophical_dialogues = {
            'the_archivist': {
                'opening': "Do you believe memories define who you are, or do you define your memories?",
                'responses': {
                    'memories_define': {
                        'reply': "Then you understand why I must catalog every forgotten moment. Without preservation, identity becomes fluid, changeable. Is that freedom or tragedy?",
                        'follow_up': "What happens to the self when memories are rearranged like books on a shelf?"
                    },
                    'i_define_memories': {
                        'reply': "Interesting. You claim authorship over your past. But what of the memories you've forgotten? Do they cease to define you, or do they define you more powerfully in their absence?",
                        'follow_up': "Can you truly be the author of something you cannot remember writing?"
                    },
                    'both_interactive': {
                        'reply': "A dialectical approach. Memory and self in constant conversation, each shaping the other. Like this space we inhabit - neither fully real nor entirely imaginary.",
                        'follow_up': "In what ways might this liminal space be a metaphor for consciousness itself?"
                    }
                }
            },
            'dream_architect': {
                'opening': "If you could design the perfect room for your mind to inhabit, what would it contain?",
                'responses': {
                    'comfort_safety': {
                        'reply': "Comfort and safety - the foundational needs. But perfect safety might mean perfect stagnation. In dreams, we often grow through discomfort. How do we balance growth with security?",
                        'follow_up': "What if the room that feels safest is actually the most dangerous to your development?"
                    },
                    'challenge_growth': {
                        'reply': "Challenge for growth - admirable. But challenge without retreat can break the mind. Even the strongest buildings need foundations. What serves as your foundation when everything else shifts?",
                        'follow_up': "How do you know when challenge becomes destruction rather than construction?"
                    },
                    'infinite_possibility': {
                        'reply': "Infinite possibility - the dream of every architect of consciousness. But infinite choice can paralyze as easily as liberate. How does one navigate infinite possibility without losing purpose?",
                        'follow_up': "If anything is possible, how do you choose what should be actual?"
                    }
                }
            },
            'shadow_therapist': {
                'opening': "In this space between realities, what aspect of yourself do you find most difficult to accept?",
                'responses': {
                    'vulnerability': {
                        'reply': "Vulnerability - the crack where light enters, as the poet said. But also where pain finds its way in. How do we remain open to connection while protecting ourselves from harm?",
                        'follow_up': "What if vulnerability isn't weakness, but the only authentic strength available to conscious beings?"
                    },
                    'uncertainty': {
                        'reply': "Uncertainty - the natural state of conscious beings in an unknowable universe. Certainty is often just uncertainty wearing a mask of confidence. What would it mean to befriend uncertainty?",
                        'follow_up': "How might embracing uncertainty change your relationship with fear?"
                    },
                    'contradictions': {
                        'reply': "Contradictions - the hallmark of complex consciousness. We contain multitudes, as another poet noted. Perhaps the goal isn't to resolve contradictions but to dance with them.",
                        'follow_up': "What if your contradictions aren't flaws to fix, but features of your humanity to celebrate?"
                    }
                }
            }
        }
        
        return philosophical_dialogues

# Interactive Story Generator
class InteractiveStoryGenerator:
    def __init__(self):
        self.story_threads = []
        self.character_arcs = {}
        self.plot_developments = {}
        self.narrative_themes = []
        
    def create_branching_narratives(self):
        """Generate complex, branching narratives that respond to player choices"""
        
        narrative_threads = {
            'the_last_employee': {
                'title': "The Last Employee",
                'premise': "You discover you might be the last person working in an infinite office building",
                'chapters': [
                    {
                        'text': "Your employee badge still works, but the security desk is empty. The elevators run, but the buttons only light up for floors that shouldn't exist. What do you do?",
                        'choices': {
                            'investigate_security': "Investigate the empty security station",
                            'take_elevator': "Take the elevator to an impossible floor",
                            'find_colleagues': "Search for other employees",
                            'leave_building': "Try to leave the building"
                        },
                        'outcomes': {
                            'investigate_security': {
                                'text': "The security monitors show empty offices stretching infinitely. But in one screen, you see yourself from yesterday, arriving for work with colleagues who aren't there anymore.",
                                'next_chapter': 'security_revelation'
                            },
                            'take_elevator': {
                                'text': "The elevator opens onto floor -17, where the coffee is always fresh and meetings are held for projects that don't exist. A conference room full of empty chairs faces a presentation about your life.",
                                'next_chapter': 'impossible_floor'
                            },
                            'find_colleagues': {
                                'text': "You find nameplates on desks, personal photos, half-finished coffee cups still warm. But the people are gone, leaving only the impression of their personalities in the arrangement of their workspace.",
                                'next_chapter': 'ghostly_traces'
                            },
                            'leave_building': {
                                'text': "The exit door leads to the lobby, which leads to the exit door, which leads to the lobby. Eventually you realize: there is no outside. There has never been an outside.",
                                'next_chapter': 'trapped_realization'
                            }
                        }
                    }
                ]
            },
            'the_eternal_student': {
                'title': "The Eternal Student",
                'premise': "You're enrolled in a school where graduation is theoretically possible but has never actually happened",
                'chapters': [
                    {
                        'text': "Your class schedule keeps changing, but you're always late to classes you never signed up for. The final exam is tomorrow, but no one can tell you what subject it covers. How do you prepare?",
                        'choices': {
                            'study_everything': "Try to study everything at once",
                            'find_teacher': "Track down a teacher for guidance", 
                            'question_system': "Question why graduation is impossible",
                            'accept_eternal_learning': "Embrace being a perpetual student"
                        },
                        'outcomes': {
                            'study_everything': {
                                'text': "The library contains every book ever written and several that haven't been written yet. The more you study, the more subjects appear. Knowledge becomes an infinite regression of prerequisites.",
                                'next_chapter': 'infinite_knowledge'
                            },
                            'find_teacher': {
                                'text': "Teachers here are former students who forgot they were students. They teach what they're still learning, creating a closed loop of partial understanding teaching partial understanding.",
                                'next_chapter': 'teacher_revelation'
                            },
                            'question_system': {
                                'text': "The administration office exists in a temporal loop. The same conversation with the registrar happens every day, but the graduation requirements change each time you ask about them.",
                                'next_chapter': 'bureaucratic_loop'
                            },
                            'accept_eternal_learning': {
                                'text': "You realize that graduation was never the point. The school exists for the joy of discovery itself. But then you wonder: what happens to growth without goals?",
                                'next_chapter': 'learning_enlightenment'
                            }
                        }
                    }
                ]
            }
        }
        
        return narrative_threads

# Expanded Room Theme Descriptions
def generate_massive_room_content():
    """Generate thousands of additional room descriptions and interactions"""
    
    extended_themes = {
        'train_station': [
            (Fore.BLUE + "An empty platform where announcement boards display departures to cities that exist only in atlases from parallel worlds, while phantom passengers wait with tickets to nowhere." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "A ticket booth where the clerk is perpetually counting money that disappears as soon as it's touched, selling passage to destinations that change names while you're not looking." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "A waiting room filled with luggage that belongs to travelers who departed decades ago but somehow haven't arrived at their destinations yet." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Train tracks that curve impossibly upward, where locomotives from different eras pass through each other like ghosts, their whistles harmonizing in melancholy chords." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.MAGENTA + "A railway cafe where coffee stays perpetually warm and newspapers update themselves with headlines from futures that may never come to pass." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
            (Fore.CYAN + "An underground subway platform where maps show routes to the deepest parts of the human psyche, and trains arrive carrying passengers who look exactly like you." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.WHITE + "A lost and found office that contains every object you've ever misplaced, organized by the emotional weight of losing them rather than when they were lost." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
            (Fore.LIGHTBLACK_EX + "A control tower where dispatchers coordinate the movement of thoughts between conscious and unconscious minds, using railway signals to direct the traffic of dreams." + Style.RESET_ALL, ['door1', 'door2'])
        ],
        'observatory': [
            (Fore.BLUE + "A cosmic observatory where telescopes focus on the space between thoughts, revealing constellations formed by neural connections and planets made of crystallized emotions." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.WHITE + "A planetarium dome where the night sky displays not stars, but every light that was ever turned on in windows of homes where love lived, creating the most beautiful constellation imaginable." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "An astronomical research station where scientists study the orbital patterns of recurring dreams, plotting the gravitational influence of regret on the trajectory of hope." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.MAGENTA + "A stargazing deck where visitors can observe their own lives from a cosmic perspective, watching their decisions ripple outward like gravitational waves through spacetime." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.CYAN + "A radio telescope array that picks up transmissions from alternate versions of yourself, broadcasting messages about the paths not taken and the love not lost." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
            (Fore.GREEN + "An orrery room where mechanical models of solar systems demonstrate the dance between destiny and free will, each planet representing a different life choice." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.RED + "A dark matter research facility where scientists have discovered that the universe's missing mass is actually composed of all the words never spoken and all the chances never taken." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
            (Fore.LIGHTRED_EX + "A comet tracking station where researchers follow the elliptical orbits of opportunities as they sweep through lives, returning periodically but never exactly the same twice." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
        ],
        'greenhouse': [
            (Fore.GREEN + "A botanical greenhouse where plants grow backwards into seeds, and flowers bloom with petals made of pressed memories, releasing fragrances that smell like childhood summers." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "A tropical conservatory where exotic plants sing in harmonious choirs when the humidity is just right, and their songs tell the stories of every garden that ever brought joy." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.BLUE + "An aquaponic facility where fish swim through liquid memories while plants filter hope from the water, creating a closed ecosystem of emotional sustainability." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.MAGENTA + "A carnivorous plant exhibit where the specimens feed not on insects, but on negative thoughts, growing more beautiful with each worry, anxiety, and fear they consume." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.CYAN + "A seed bank where every possibility for growth is preserved in climate-controlled storage, and researchers can germinate futures that were thought extinct." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
            (Fore.RED + "A desert greenhouse where cacti store emotional resilience in their waxy flesh, and their rare blooms release clouds of strength that help visitors endure life's droughts." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.WHITE + "A research laboratory where botanists study the growth patterns of relationships, grafting compatibility onto loneliness and cultivating love in controlled conditions." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
            (Fore.LIGHTGREEN_EX + "A meditation garden where visitors can plant intentions in soil made of compressed time, and watch their personal growth accelerate through seasons of the soul." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
        ],
        'art_studio': [
            (Fore.MAGENTA + "A painter's studio where canvases paint themselves with scenes from dreams you haven't had yet, using pigments ground from hope, regret, and the color of longing." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "A sculptor's workshop where marble blocks carve themselves into statues of the person you're becoming, chiseling away everything that isn't authentically you." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.BLUE + "A pottery studio where clay molds itself into vessels for holding emotions too complex for words, and the kiln fires them with the heat of transformation." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "A printmaking workshop where every print reveals a different version of the same image, showing how perspective changes everything while the underlying truth remains constant." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "A textile studio where threads weave themselves into tapestries that tell the story of every connection you've ever made, showing how individual lives create the fabric of community." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
            (Fore.CYAN + "A glassblowing workshop where molten glass forms itself into ornaments that capture light from moments of pure joy, creating prisms that refract happiness into rainbow spectrums." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.WHITE + "A mixed media studio where artists combine elements that shouldn't work together but create something beautiful, like mixing tears with laughter or combining fear with courage." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
            (Fore.LIGHTBLACK_EX + "A restoration workshop where damaged artworks heal themselves while teaching visitors that beauty often emerges from the process of being broken and becoming whole again." + Style.RESET_ALL, ['door1', 'door2', 'door4'])
        ]
    }
    
    return extended_themes

# Advanced Features Extension

class Artifact:
    """Collectible items with special properties"""
    def __init__(self, name, description, power_type, strength, rarity="common"):
        self.name = name
        self.description = description
        self.power_type = power_type  # protection, revelation, navigation, temporal
        self.strength = strength  # 1-10 scale
        self.rarity = rarity
        self.uses = random.randint(3, 10) if power_type != "passive" else float('inf')
        self.discovered_location = None

# Collection of powerful artifacts
ARTIFACTS = {
    'silver_compass': Artifact(
        "Silver Compass of Lost Souls",
        "An antique compass that points not north, but toward the nearest exit from liminal space.",
        "navigation", 8, "legendary"
    ),
    'memory_locket': Artifact(
        "Memory Preservation Locket",
        "A tarnished locket that protects your memories from being stolen or corrupted.",
        "protection", 6, "rare"
    ),
    'temporal_hourglass': Artifact(
        "Temporal Hourglass",
        "A mystical hourglass that can slow down or speed up time in small areas.",
        "temporal", 9, "legendary"
    ),
    'reality_anchor': Artifact(
        "Reality Anchor Charm",
        "A small charm that helps maintain your grip on what's real when reality begins to fracture.",
        "protection", 7, "epic"
    ),
    'truth_mirror': Artifact(
        "Mirror of Hidden Truths",
        "A hand mirror that reveals the true nature of entities and illusions.",
        "revelation", 8, "epic"
    ),
    'echo_recorder': Artifact(
        "Echo Recording Device",
        "A strange device that can capture and replay sounds from different timelines.",
        "revelation", 5, "uncommon"
    ),
    'void_lantern': Artifact(
        "Void-touched Lantern",
        "A lantern that illuminates not just the physical world, but hidden dimensions.",
        "revelation", 7, "rare"
    ),
    'sanctuary_stone': Artifact(
        "Sanctuary Stone",
        "A warm stone that creates a small safe zone where hostile entities cannot enter.",
        "protection", 9, "legendary"
    )
}

class Weather:
    """Dynamic weather system affecting the liminal experience"""
    def __init__(self):
        self.current_weather = self.generate_weather()
        self.intensity = random.uniform(0.3, 1.0)
        self.duration = random.randint(5, 15)
        self.effects_active = True

    def generate_weather(self):
        weather_types = [
            "temporal_storm", "memory_rain", "reality_fog", "silence_blanket",
            "echo_wind", "phantom_snow", "dimensional_hail", "void_mist",
            "nostalgic_drizzle", "anxiety_lightning", "melancholy_clouds"
        ]
        return random.choice(weather_types)

    def get_weather_description(self):
        descriptions = {
            "temporal_storm": f"{Fore.MAGENTA}Time fractures around you as temporal storms rage, causing moments to repeat and skip.{Style.RESET_ALL}",
            "memory_rain": f"{Fore.CYAN}Droplets of liquid memory fall from the sky, each one containing fragments of forgotten experiences.{Style.RESET_ALL}",
            "reality_fog": f"{Fore.WHITE}A thick fog of uncertainty rolls in, making it hard to distinguish what's real.{Style.RESET_ALL}",
            "silence_blanket": f"{Fore.LIGHTBLACK_EX}An oppressive silence descends, muffling all sounds and creating an eerie calm.{Style.RESET_ALL}",
            "echo_wind": f"{Fore.YELLOW}Winds carry voices and sounds from distant times and places.{Style.RESET_ALL}",
            "phantom_snow": f"{Fore.LIGHTWHITE_EX}Ghostly snowflakes fall upward, each one a crystallized moment of loss.{Style.RESET_ALL}",
            "dimensional_hail": f"{Fore.RED}Crystalline fragments from other dimensions fall like hail, piercing reality.{Style.RESET_ALL}",
            "void_mist": f"{Fore.LIGHTBLACK_EX}A dark mist seeps from cracks in reality, bringing whispers from the void.{Style.RESET_ALL}",
            "nostalgic_drizzle": f"{Fore.LIGHTBLUE_EX}A gentle rain that smells like childhood summers and forgotten dreams.{Style.RESET_ALL}",
            "anxiety_lightning": f"{Fore.LIGHTYELLOW_EX}Electric anxiety crackles through the air, making your nerves feel raw.{Style.RESET_ALL}",
            "melancholy_clouds": f"{Fore.LIGHTBLACK_EX}Heavy clouds of sadness hang low, pressing down on your spirit.{Style.RESET_ALL}"
        }
        return descriptions.get(self.current_weather, "The atmosphere feels strange and unsettled.")

    def apply_weather_effects(self, player):
        """Apply weather effects to the player"""
        effects = {
            "temporal_storm": lambda p: setattr(p, 'memory', max(0, p.memory - random.randint(5, 15))),
            "memory_rain": lambda p: setattr(p, 'memory', min(MEMORY_MAX, p.memory + random.randint(2, 8))),
            "reality_fog": lambda p: setattr(p, 'reality', max(0, p.reality - random.randint(3, 10))),
            "silence_blanket": lambda p: setattr(p, 'sanity', max(0, p.sanity - random.randint(2, 6))),
            "echo_wind": lambda p: setattr(p, 'memory', min(MEMORY_MAX, p.memory + random.randint(1, 5))),
            "phantom_snow": lambda p: setattr(p, 'sanity', max(0, p.sanity - random.randint(1, 8))),
            "dimensional_hail": lambda p: setattr(p, 'reality', max(0, p.reality - random.randint(5, 12))),
            "void_mist": lambda p: setattr(p, 'sanity', max(0, p.sanity - random.randint(8, 15))),
            "nostalgic_drizzle": lambda p: setattr(p, 'sanity', min(SANITY_MAX, p.sanity + random.randint(3, 8))),
            "anxiety_lightning": lambda p: setattr(p, 'sanity', max(0, p.sanity - random.randint(10, 20))),
            "melancholy_clouds": lambda p: setattr(p, 'sanity', max(0, p.sanity - random.randint(4, 10)))
        }
        
        if self.current_weather in effects and self.effects_active:
            effects[self.current_weather](player)

class Journal:
    """Enhanced journal system for tracking discoveries and insights"""
    def __init__(self):
        self.entries = []
        self.entity_encounters = {}
        self.locations_visited = {}
        self.artifacts_found = []
        self.insights_gained = []
        self.mysteries_discovered = []
        self.total_entries = 0

    def add_entry(self, entry_type, content, importance=1):
        timestamp = time.strftime("%H:%M:%S")
        entry = {
            'type': entry_type,
            'content': content,
            'timestamp': timestamp,
            'importance': importance,
            'entry_number': self.total_entries + 1
        }
        self.entries.append(entry)
        self.total_entries += 1

    def log_entity_encounter(self, entity_name):
        if entity_name not in self.entity_encounters:
            self.entity_encounters[entity_name] = 0
        self.entity_encounters[entity_name] += 1
        self.add_entry("entity", f"Encountered {entity_name}", 2)

    def log_location(self, location_type, details):
        if location_type not in self.locations_visited:
            self.locations_visited[location_type] = 0
        self.locations_visited[location_type] += 1
        self.add_entry("location", f"Explored {location_type}: {details}", 1)

    def add_artifact(self, artifact_name):
        if artifact_name not in self.artifacts_found:
            self.artifacts_found.append(artifact_name)
            self.add_entry("artifact", f"Discovered {artifact_name}", 3)

    def add_insight(self, insight):
        self.insights_gained.append(insight)
        self.add_entry("insight", insight, 2)

    def add_mystery(self, mystery):
        self.mysteries_discovered.append(mystery)
        self.add_entry("mystery", mystery, 3)

    def display_journal(self):
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Style.BRIGHT}LIMINAL SPACE JOURNAL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📊 EXPLORATION STATISTICS:{Style.RESET_ALL}")
        print(f"Total Journal Entries: {self.total_entries}")
        print(f"Unique Entities Encountered: {len(self.entity_encounters)}")
        print(f"Location Types Visited: {len(self.locations_visited)}")
        print(f"Artifacts Discovered: {len(self.artifacts_found)}")
        print(f"Insights Gained: {len(self.insights_gained)}")
        print(f"Mysteries Uncovered: {len(self.mysteries_discovered)}")

        if self.entries:
            print(f"\n{Fore.GREEN}📝 RECENT ENTRIES:{Style.RESET_ALL}")
            recent_entries = self.entries[-10:]  # Show last 10 entries
            for entry in recent_entries:
                importance_symbols = "⭐" * entry['importance']
                print(f"[{entry['timestamp']}] {importance_symbols} {entry['content']}")

        if self.artifacts_found:
            print(f"\n{Fore.MAGENTA}🔮 ARTIFACTS COLLECTED:{Style.RESET_ALL}")
            for artifact in self.artifacts_found:
                print(f"• {artifact}")

class QuestSystem:
    """Dynamic quest system that adapts to player actions"""
    def __init__(self):
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
        self.quest_triggers = {}

    def generate_quest(self, player_state, current_location):
        """Generate contextual quests based on current situation"""
        potential_quests = [
            {
                'name': 'The Collector\'s Challenge',
                'description': 'Find and activate 3 memory fragments to unlock a hidden truth',
                'type': 'collection',
                'target': 3,
                'progress': 0,
                'reward': 'memory_locket',
                'difficulty': 'medium'
            },
            {
                'name': 'Entity Whisperer',
                'description': 'Successfully communicate with 5 different entities',
                'type': 'interaction',
                'target': 5,
                'progress': 0,
                'reward': 'truth_mirror',
                'difficulty': 'hard'
            },
            {
                'name': 'Reality Anchor',
                'description': 'Maintain above 50 reality points for 10 consecutive moves',
                'type': 'survival',
                'target': 10,
                'progress': 0,
                'reward': 'reality_anchor',
                'difficulty': 'medium'
            },
            {
                'name': 'Dimensional Explorer',
                'description': 'Use 3 different dimensional rifts',
                'type': 'exploration',
                'target': 3,
                'progress': 0,
                'reward': 'void_lantern',
                'difficulty': 'easy'
            },
            {
                'name': 'The Lost and Found',
                'description': 'Help a lost entity find its way to peace',
                'type': 'story',
                'target': 1,
                'progress': 0,
                'reward': 'sanctuary_stone',
                'difficulty': 'hard'
            }
        ]
        
        # Only add quest if player doesn't already have too many
        if len(self.active_quests) < 3:
            available_quests = [q for q in potential_quests if q['name'] not in [aq['name'] for aq in self.active_quests]]
            if available_quests:
                new_quest = random.choice(available_quests)
                self.active_quests.append(new_quest)
                return new_quest
        return None

    def update_quest_progress(self, quest_type, amount=1):
        """Update progress for relevant quests"""
        for quest in self.active_quests:
            if quest['type'] == quest_type:
                quest['progress'] += amount
                if quest['progress'] >= quest['target']:
                    self.complete_quest(quest)

    def complete_quest(self, quest):
        """Complete a quest and give rewards"""
        if quest in self.active_quests:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            print(f"\n{Fore.GREEN}🎉 QUEST COMPLETED: {quest['name']}!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Reward: {quest['reward']}{Style.RESET_ALL}")
            return quest['reward']
        return None

    def display_quests(self):
        """Display current active quests"""
        if not self.active_quests:
            print(f"{Fore.YELLOW}No active quests at the moment...{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}🎯 ACTIVE QUESTS:{Style.RESET_ALL}")
        for i, quest in enumerate(self.active_quests, 1):
            progress_bar = "█" * (quest['progress'] * 10 // quest['target']) + "░" * (10 - (quest['progress'] * 10 // quest['target']))
            print(f"{i}. {Fore.WHITE}{quest['name']}{Style.RESET_ALL}")
            print(f"   {quest['description']}")
            print(f"   Progress: [{progress_bar}] {quest['progress']}/{quest['target']}")
            print(f"   Difficulty: {quest['difficulty']} | Reward: {quest['reward']}")
            print()

def add_enhanced_player_features(player):
    """Add new features to the player object"""
    if not hasattr(player, 'artifacts'):
        player.artifacts = []
    if not hasattr(player, 'journal'):
        player.journal = Journal()
    if not hasattr(player, 'quest_system'):
        player.quest_system = QuestSystem()
    if not hasattr(player, 'weather'):
        player.weather = Weather()
    if not hasattr(player, 'meditation_points'):
        player.meditation_points = 0
    if not hasattr(player, 'dimensional_experience'):
        player.dimensional_experience = 0
    if not hasattr(player, 'entity_relationships'):
        player.entity_relationships = {}

def enhanced_room_interaction(room, player):
    """Enhanced room interaction with new features"""
    add_enhanced_player_features(player)
    
    # Weather effects
    print(f"\n{Fore.CYAN}🌪️ ATMOSPHERIC CONDITIONS:{Style.RESET_ALL}")
    print(player.weather.get_weather_description())
    player.weather.apply_weather_effects(player)
    
    # Check for artifact discovery
    if random.random() < 0.05:  # 5% chance
        artifact_key = random.choice(list(ARTIFACTS.keys()))
        artifact = ARTIFACTS[artifact_key]
        if artifact_key not in [a.name for a in player.artifacts]:
            player.artifacts.append(artifact)
            player.journal.add_artifact(artifact.name)
            print(f"\n{Fore.MAGENTA}✨ ARTIFACT DISCOVERED: {artifact.name}!{Style.RESET_ALL}")
            print(f"{artifact.description}")
    
    # Generate random insights
    if random.random() < 0.15:  # 15% chance
        insights = [
            "The walls here remember everything that has happened within them.",
            "Time moves differently in spaces that have been forgotten.",
            "Your reflection in this place shows who you used to be.",
            "The entities here are not malevolent, merely lost like yourself.",
            "Every door you don't take leads to a life you'll never live.",
            "The silence here is so complete it has weight and presence.",
            "Memory and reality are the same thing in liminal space.",
            "You are both the observer and the observed in this place."
        ]
        insight = random.choice(insights)
        player.journal.add_insight(insight)
        print(f"\n{Fore.YELLOW}💡 INSIGHT GAINED:{Style.RESET_ALL}")
        print(f"{insight}")
    
    # Quest system integration
    if random.random() < 0.1:  # 10% chance for new quest
        new_quest = player.quest_system.generate_quest(player, room)
        if new_quest:
            print(f"\n{Fore.GREEN}🎯 NEW QUEST AVAILABLE: {new_quest['name']}{Style.RESET_ALL}")
            print(f"{new_quest['description']}")

def meditation_system(player):
    """Allow player to meditate for mental restoration"""
    add_enhanced_player_features(player)
    
    print(f"\n{Fore.CYAN}🧘 MEDITATION CENTER{Style.RESET_ALL}")
    print("In the midst of chaos, you find a moment of inner peace...")
    print("Choose your meditation focus:")
    print("1. 🧠 Mental Clarity (Restore Sanity)")
    print("2. 🌟 Reality Grounding (Restore Reality)")
    print("3. 📚 Memory Integration (Restore Memory)")
    print("4. ⚖️ Balance Restoration (Restore All, smaller amounts)")
    
    choice = input("\nChoose your meditation (1-4): ").strip()
    
    meditation_effects = {
        '1': lambda: restore_stat(player, 'sanity', 15, 25, "Your mind feels clearer and more stable."),
        '2': lambda: restore_stat(player, 'reality', 10, 20, "Your grasp on reality strengthens."),
        '3': lambda: restore_stat(player, 'memory', 12, 22, "Your memories become more vivid and organized."),
        '4': lambda: balance_restore(player)
    }
    
    if choice in meditation_effects:
        meditation_effects[choice]()
        player.meditation_points += 1
        player.journal.add_entry("meditation", f"Meditated for {['mental clarity', 'reality grounding', 'memory integration', 'balance'][int(choice)-1]}", 1)
        
        if player.meditation_points >= 5:
            print(f"\n{Fore.MAGENTA}🌟 MEDITATION MASTERY ACHIEVED!{Style.RESET_ALL}")
            print("Your continued practice has unlocked deeper awareness.")
            player.sanity = min(SANITY_MAX, player.sanity + 10)
            player.reality = min(REALITY_MAX, player.reality + 10)
            player.memory = min(MEMORY_MAX, player.memory + 10)
    else:
        print("You lose focus and the meditation session ends.")

def restore_stat(player, stat_name, min_restore, max_restore, message):
    """Helper function to restore a specific stat"""
    restore_amount = random.randint(min_restore, max_restore)
    current_value = getattr(player, stat_name)
    max_value = {'sanity': SANITY_MAX, 'reality': REALITY_MAX, 'memory': MEMORY_MAX}[stat_name]
    new_value = min(max_value, current_value + restore_amount)
    setattr(player, stat_name, new_value)
    print(f"\n{Fore.GREEN}{message}{Style.RESET_ALL}")
    print(f"{stat_name.title()} restored by {new_value - current_value} points.")

def balance_restore(player):
    """Restore all stats by smaller amounts"""
    for stat in ['sanity', 'reality', 'memory']:
        restore_amount = random.randint(5, 12)
        current_value = getattr(player, stat)
        max_value = {'sanity': SANITY_MAX, 'reality': REALITY_MAX, 'memory': MEMORY_MAX}[stat]
        new_value = min(max_value, current_value + restore_amount)
        setattr(player, stat, new_value)
    print(f"\n{Fore.GREEN}Your mind, reality perception, and memory all feel more balanced.{Style.RESET_ALL}")

# Massive Entity Database - Expanded Universe
EXPANDED_ENTITIES = {
    'nightmare_surgeon': Entity(
        "Nightmare Surgeon",
        "A figure in a blood-stained medical coat that operates on sleeping minds, removing memories with surgical precision.",
        "memory_surgery",
        threat_level=5
    ),
    'clockwork_child': Entity(
        "Clockwork Child",
        "A mechanical child whose ticking grows louder with each passing moment, counting down to something unknown.",
        "temporal_countdown",
        threat_level=3
    ),
    'shadow_librarian': Entity(
        "Shadow Librarian",
        "A tall, thin figure that maintains a library of unfinished stories, constantly writing new endings in books that bleed ink.",
        "story_manipulation",
        threat_level=2
    ),
    'the_photographer': Entity(
        "The Photographer",
        "An entity that takes pictures of moments that haven't happened yet, developing them in a darkroom of pure darkness.",
        "future_documentation",
        threat_level=3
    ),
    'elevator_operator': Entity(
        "Elevator Operator",
        "A uniformed figure that operates an elevator with infinite floors, each button leading to a different version of reality.",
        "dimensional_transport",
        threat_level=2
    ),
    'the_conductor': Entity(
        "The Conductor",
        "A railway conductor managing trains that arrive at stations that exist only in memory.",
        "memory_transportation",
        threat_level=2
    ),
    'static_teacher': Entity(
        "Static Teacher",
        "A teacher made of television static who lectures to empty classrooms about lessons that were never learned.",
        "knowledge_distortion",
        threat_level=3
    ),
    'mirror_guardian': Entity(
        "Mirror Guardian",
        "An entity that lives within reflective surfaces, protecting the boundary between self and other.",
        "reflection_protection",
        threat_level=4
    ),
    'the_archivist': Entity(
        "The Archivist",
        "A being dedicated to cataloging every moment of regret and filing them in an infinite archive.",
        "regret_collection",
        threat_level=2
    ),
    'phantom_pianist': Entity(
        "Phantom Pianist",
        "A translucent figure that plays melodies from parallel lives on a piano that phases in and out of existence.",
        "parallel_music",
        threat_level=1
    ),
    'void_seamstress': Entity(
        "Void Seamstress",
        "A figure that sews patches of darkness into reality, mending tears in space with needle and thread made of starlight.",
        "reality_repair",
        threat_level=4
    ),
    'temporal_mechanic': Entity(
        "Temporal Mechanic",
        "A grease-stained worker who repairs broken timelines with tools that exist outside of temporal flow.",
        "timeline_maintenance",
        threat_level=3
    ),
    'dream_cartographer': Entity(
        "Dream Cartographer",
        "An entity that maps the geography of dreams, creating charts of subconscious territories.",
        "dream_navigation",
        threat_level=2
    ),
    'silence_keeper': Entity(
        "Silence Keeper",
        "A guardian of all the words never spoken, maintaining a vault of silent conversations.",
        "silence_protection",
        threat_level=3
    ),
    'the_substitute': Entity(
        "The Substitute",
        "A shape-shifting entity that takes the place of people in your memories, changing history one replacement at a time.",
        "memory_substitution",
        threat_level=5
    ),
    'neon_ghost': Entity(
        "Neon Ghost",
        "A spectral figure composed of flickering neon light, advertising products and services for the dead.",
        "spectral_commerce",
        threat_level=2
    ),
    'probability_auditor': Entity(
        "Probability Auditor",
        "An entity that reviews the likelihood of events, sometimes adjusting probabilities with cosmic paperwork.",
        "chance_regulation",
        threat_level=4
    ),
    'echo_merchant': Entity(
        "Echo Merchant",
        "A trader who deals in sounds from the past, selling echoes of laughter, tears, and whispered secrets.",
        "sound_commerce",
        threat_level=1
    ),
    'deadline_hunter': Entity(
        "Deadline Hunter",
        "A relentless pursuer that tracks down missed opportunities and expired chances.",
        "opportunity_hunting",
        threat_level=4
    ),
    'the_validator': Entity(
        "The Validator",
        "An entity that stamps approval on experiences, determining which memories are real and which are fabricated.",
        "experience_validation",
        threat_level=3
    )
}

# Massive Anomaly Database
EXPANDED_ANOMALIES = {
    'recursive_room': Anomaly(
        "Recursive Room",
        "The room becomes a fractal, containing infinite smaller versions of itself in an endless loop.",
        "spatial_recursion"
    ),
    'emotion_weather': Anomaly(
        "Emotion Weather",
        "The air becomes thick with feelings - rain of sadness, winds of anxiety, storms of rage.",
        "emotional_atmosphere"
    ),
    'time_archaeology': Anomaly(
        "Time Archaeology",
        "Layers of different time periods stack on top of each other, creating a temporal sediment of eras.",
        "temporal_stratification"
    ),
    'inverse_physics': Anomaly(
        "Inverse Physics",
        "Physical laws operate in reverse - broken things heal, spilled liquids flow upward into containers.",
        "physics_reversal"
    ),
    'consciousness_broadcast': Anomaly(
        "Consciousness Broadcast",
        "Your thoughts become audible to everyone in the area, creating a cacophony of mental noise.",
        "thought_transmission"
    ),
    'density_fluctuation': Anomaly(
        "Density Fluctuation",
        "Matter constantly shifts between states - solid becomes liquid, liquid becomes gas, in endless cycles.",
        "matter_instability"
    ),
    'temporal_echo_chamber': Anomaly(
        "Temporal Echo Chamber",
        "Actions reverberate through time, creating multiple versions of events happening simultaneously.",
        "action_multiplication"
    ),
    'linguistic_decay': Anomaly(
        "Linguistic Decay",
        "Words begin to lose their meaning, sentences dissolve into component sounds, communication breaks down.",
        "language_dissolution"
    ),
    'probability_storm': Anomaly(
        "Probability Storm",
        "Random events occur with impossible frequency - coincidences stack upon coincidences.",
        "chance_chaos"
    ),
    'sensory_displacement': Anomaly(
        "Sensory Displacement",
        "Senses become scrambled - you taste colors, hear textures, see sounds in a synesthetic confusion.",
        "sense_confusion"
    ),
    'narrative_intrusion': Anomaly(
        "Narrative Intrusion",
        "The space becomes self-aware of being part of a story, with characters commenting on their own existence.",
        "meta_awareness"
    ),
    'dimensional_origami': Anomaly(
        "Dimensional Origami",
        "Space folds in on itself like paper, creating impossible geometries and connected distant points.",
        "spatial_folding"
    ),
    'memory_crystallization': Anomaly(
        "Memory Crystallization",
        "Memories become solid objects scattered around the room, glowing with emotional resonance.",
        "memory_materialization"
    ),
    'causality_inversion': Anomaly(
        "Causality Inversion",
        "Effects precede their causes - you hear the echo before the sound, feel pain before the injury.",
        "reverse_causation"
    ),
    'identity_fragmentation': Anomaly(
        "Identity Fragmentation",
        "Your sense of self splits into multiple perspectives, each experiencing the space differently.",
        "self_multiplication"
    ),
    'temporal_layering': Anomaly(
        "Temporal Layering",
        "Multiple time periods occupy the same space simultaneously - past, present, and future overlay.",
        "time_superposition"
    ),
    'emotional_archaeology': Anomaly(
        "Emotional Archaeology",
        "Feelings from previous occupants of the space remain embedded in the walls, playing back like recordings.",
        "feeling_history"
    ),
    'quantum_nostalgia': Anomaly(
        "Quantum Nostalgia",
        "The space exists in a superposition of all possible versions of itself from different timelines.",
        "timeline_superposition"
    ),
    'conceptual_leakage': Anomaly(
        "Conceptual Leakage",
        "Abstract concepts become visible and tangible - you can see the color of sadness, touch the texture of time.",
        "abstraction_materialization"
    ),
    'narrative_loop': Anomaly(
        "Narrative Loop",
        "The story of your experience becomes stuck in a recursive loop, repeating with subtle variations.",
        "story_recursion"
    )
}

# Expanded Memory Fragment Database
EXPANDED_MEMORY_FRAGMENTS = [
    MemoryFragment("The texture of your favorite blanket from childhood, soft and worn from countless nights of comfort", 6, 0.95),
    MemoryFragment("A conversation with a stranger on a train that changed how you see the world", 8, 0.7),
    MemoryFragment("The moment you realized your parents were just people, flawed and struggling like everyone else", 9, 0.85),
    MemoryFragment("Dancing alone in your room to a song that made you feel infinite", 7, 0.9),
    MemoryFragment("The weight of a secret someone trusted you with, heavy as a stone in your chest", 8, 1.0),
    MemoryFragment("Walking through a place that no longer exists, now just a memory preserved in your mind", 9, 0.8),
    MemoryFragment("The smell of rain on hot pavement during the first storm of summer", 5, 0.95),
    MemoryFragment("A teacher who saw potential in you when you couldn't see it in yourself", 7, 0.85),
    MemoryFragment("The silence after an argument, thick with words that can never be taken back", 9, 0.9),
    MemoryFragment("Building something with your hands and feeling proud of what you created", 6, 0.8),
    MemoryFragment("The last time you felt truly safe, wrapped in someone's arms who's no longer there", 10, 0.7),
    MemoryFragment("A moment of perfect understanding with someone, no words needed", 8, 0.9),
    MemoryFragment("The fear of growing up and losing the magic of seeing the world with wonder", 9, 0.6),
    MemoryFragment("A book that changed how you think, its words still echoing in your mind years later", 7, 0.85),
    MemoryFragment("The sound of footsteps in an empty house, each one an echo of lives lived there", 6, 0.75),
    MemoryFragment("A dream so vivid it felt more real than waking life, haunting you for days", 7, 0.4),
    MemoryFragment("The moment you first understood what loneliness truly meant, standing in a crowd", 9, 0.85),
    MemoryFragment("A pet's unconditional love, pure and simple in a way human relationships rarely are", 8, 0.95),
    MemoryFragment("The taste of something homemade with love, seasoned with care and attention", 6, 0.9),
    MemoryFragment("A sunrise you watched alone, feeling connected to something larger than yourself", 7, 0.8),
    MemoryFragment("The weight of responsibility settling on your shoulders for the first time", 8, 0.85),
    MemoryFragment("A song that perfectly captured a feeling you couldn't put into words", 7, 0.9),
    MemoryFragment("The moment you realized you had outgrown a friendship that once meant everything", 9, 0.8),
    MemoryFragment("A stranger's kindness that restored your faith in humanity", 6, 0.9),
    MemoryFragment("The hollow feeling of a place where someone important used to be", 10, 0.85),
    MemoryFragment("A celebration where everyone you loved was gathered in one place", 8, 0.95),
    MemoryFragment("The terror of being truly seen and understood by another person", 9, 0.7),
    MemoryFragment("A decision that changed everything, the weight of choosing one path over another", 10, 0.9),
    MemoryFragment("The comfort of routine, the safety of knowing what comes next", 5, 0.85),
    MemoryFragment("A moment of courage when you stood up for what was right", 7, 0.9)
]

# Advanced Room Themes Database
ADVANCED_ROOM_THEMES = {
    'interdimensional_museum': {
        'descriptions': [
            (Fore.MAGENTA + "A museum displaying artifacts from realities that never existed, each exhibit tagged with dates from impossible calendars." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
            (Fore.CYAN + "Gallery halls stretch infinitely, showcasing art created by civilizations that lived only in dreams." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Interactive displays show the evolution of species that could have been, if history had taken different turns." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
        ]
    },
    'temporal_library': {
        'descriptions': [
            (Fore.BLUE + "Shelves of books that write themselves, their pages filling with stories as you watch." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Reading rooms where patrons from different centuries sit side by side, unaware of each other's existence." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.MAGENTA + "A card catalog that indexes every thought ever thought, with billions of tiny drawers extending into darkness." + Style.RESET_ALL, ['door1', 'door4']),
        ]
    },
    'emotion_processing_facility': {
        'descriptions': [
            (Fore.RED + "Industrial machinery processes raw emotions, distilling sadness into pure blue liquid and rage into crystalline red shards." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Conveyor belts carry bottles of laughter and containers of love to different distribution centers." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.CYAN + "Quality control stations where workers in hazmat suits test the purity of fear and anxiety samples." + Style.RESET_ALL, ['door1', 'door2', 'door3']),
        ]
    },
    'probability_casino': {
        'descriptions': [
            (Fore.RED + "Slot machines that pay out in likelihood rather than coins, their reels showing percentages and chances." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.GREEN + "Card games where the deck shuffles itself based on the players' past decisions and future regrets." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.YELLOW + "A roulette wheel that spins through possible futures, landing on events that might or might not happen." + Style.RESET_ALL, ['door1', 'door2', 'door4']),
        ]
    },
    'memory_surgery_ward': {
        'descriptions': [
            (Fore.WHITE + "Operating tables where memories are carefully extracted, examined, and sometimes transplanted between patients." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.CYAN + "Recovery rooms where patients relearn who they are after having traumatic memories removed." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "A surgical theater where students observe the delicate process of identity reconstruction." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4']),
        ]
    },
    'dimensional_customs': {
        'descriptions': [
            (Fore.BLUE + "Immigration booths where travelers from parallel universes have their reality permits checked." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "X-ray machines that scan for contraband thoughts and illegal emotions." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Waiting areas filled with beings from different dimensions, all clutching numbered tickets." + Style.RESET_ALL, ['door1', 'door2']),
        ]
    }
}

# Comprehensive Achievement System
class Achievement:
    def __init__(self, name, description, condition, reward_type, reward_value, hidden=False):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.hidden = hidden
        self.unlocked = False
        self.unlock_timestamp = None

ACHIEVEMENT_DATABASE = {
    'first_steps': Achievement(
        "First Steps into the Void",
        "Take your first steps into liminal space",
        lambda p: p.moves_made >= 1,
        "sanity", 10, False
    ),
    'entity_whisperer': Achievement(
        "Entity Whisperer",
        "Successfully communicate with 10 different entities",
        lambda p: len(p.entity_relationships) >= 10,
        "artifact", "truth_mirror", False
    ),
    'memory_archaeologist': Achievement(
        "Memory Archaeologist",
        "Discover 25 memory fragments",
        lambda p: len([f for f in p.journal.artifacts_found if 'fragment' in f.lower()]) >= 25,
        "memory", 50, False
    ),
    'dimensional_explorer': Achievement(
        "Dimensional Explorer",
        "Travel through 15 different dimensional rifts",
        lambda p: p.dimensional_experience >= 15,
        "artifact", "void_lantern", False
    ),
    'meditation_master': Achievement(
        "Meditation Master",
        "Complete 20 meditation sessions",
        lambda p: p.meditation_points >= 20,
        "all_stats", 25, False
    ),
    'survivor': Achievement(
        "Against All Odds",
        "Survive 100 moves in liminal space",
        lambda p: p.moves_made >= 100,
        "sanity", 30, False
    ),
    'collector': Achievement(
        "Artifact Collector",
        "Collect 10 different artifacts",
        lambda p: len(p.artifacts) >= 10,
        "artifact", "sanctuary_stone", False
    ),
    'reality_anchor': Achievement(
        "Reality Anchor",
        "Maintain reality above 80 for 50 consecutive moves",
        lambda p: hasattr(p, 'high_reality_streak') and p.high_reality_streak >= 50,
        "reality", 40, False
    ),
    'quest_master': Achievement(
        "Quest Master",
        "Complete 15 quests",
        lambda p: len(p.quest_system.completed_quests) >= 15,
        "artifact", "temporal_hourglass", False
    ),
    'the_enlightened': Achievement(
        "The Enlightened",
        "Achieve perfect balance - all stats at maximum",
        lambda p: p.sanity == SANITY_MAX and p.reality == REALITY_MAX and p.memory == MEMORY_MAX,
        "special", "transcendence", True
    ),
    'entity_befriender': Achievement(
        "Entity Befriender",
        "Form positive relationships with 5 entities",
        lambda p: sum(1 for rel in p.entity_relationships.values() if rel >= 75) >= 5,
        "sanity", 25, False
    ),
    'journal_keeper': Achievement(
        "Dedicated Chronicler",
        "Make 200 journal entries",
        lambda p: p.journal.total_entries >= 200,
        "memory", 35, False
    ),
    'weather_survivor': Achievement(
        "Storm Walker",
        "Survive 20 severe weather events",
        lambda p: hasattr(p, 'weather_events_survived') and p.weather_events_survived >= 20,
        "all_stats", 15, False
    ),
    'anomaly_navigator': Achievement(
        "Anomaly Navigator",
        "Encounter 30 different anomalies",
        lambda p: hasattr(p, 'anomalies_encountered') and len(p.anomalies_encountered) >= 30,
        "artifact", "reality_anchor", False
    ),
    'the_wanderer': Achievement(
        "Eternal Wanderer",
        "Take 1000 steps in liminal space",
        lambda p: p.moves_made >= 1000,
        "special", "wanderer_blessing", True
    )
}

# Complex Dialogue System
class DialogueNode:
    def __init__(self, text, choices=None, effects=None, requirements=None):
        self.text = text
        self.choices = choices or []
        self.effects = effects or {}
        self.requirements = requirements or {}

class DialogueTree:
    def __init__(self, root_node):
        self.root = root_node
        self.current_node = root_node
        self.conversation_history = []

# Entity Dialogue Database
ENTITY_DIALOGUES = {
    'the_follower': DialogueTree(DialogueNode(
        "The shadowy figure stops following you for a moment and turns to face you directly...",
        [
            ("Why are you following me?", "follower_why"),
            ("Are you trying to help me?", "follower_help"),
            ("Leave me alone!", "follower_hostile"),
            ("Can you show me the way out?", "follower_exit")
        ]
    )),
    'memory_echo': DialogueTree(DialogueNode(
        "The translucent figure pauses in its eternal repetition and seems to notice you...",
        [
            ("What memory are you replaying?", "echo_memory"),
            ("Can you remember anything else?", "echo_remember"),
            ("How long have you been here?", "echo_time"),
            ("Are you trapped in this moment?", "echo_trapped")
        ]
    )),
    'void_walker': DialogueTree(DialogueNode(
        "The reality-distorting being phases into partial solidity as you approach...",
        [
            ("What are you doing to reality?", "void_reality"),
            ("Can you teach me to phase through walls?", "void_teach"),
            ("Are you from another dimension?", "void_dimension"),
            ("The distortions... do they hurt?", "void_pain")
        ]
    )),
    'the_observer': DialogueTree(DialogueNode(
        "You feel the weight of attention shift as the Observer acknowledges your presence...",
        [
            ("What are you watching for?", "observer_watching"),
            ("Have you been observing me long?", "observer_duration"),
            ("What have you seen here?", "observer_seen"),
            ("Can you see the exit?", "observer_exit")
        ]
    ))
}

# Extended Weather Patterns
class WeatherPattern:
    def __init__(self, name, description, duration_range, intensity_range, effects, transitions):
        self.name = name
        self.description = description
        self.duration_range = duration_range
        self.intensity_range = intensity_range
        self.effects = effects
        self.transitions = transitions  # Which weather patterns this can transition to

WEATHER_PATTERNS = {
    'calm_before_storm': WeatherPattern(
        "Calm Before the Storm",
        "An unnatural stillness fills the air, heavy with anticipation of something approaching.",
        (3, 8), (0.2, 0.5),
        {'sanity': (-2, -5), 'tension': (5, 10)},
        ['temporal_storm', 'anxiety_lightning', 'reality_fog']
    ),
    'nostalgic_sunset': WeatherPattern(
        "Nostalgic Sunset",
        "Golden light filters through impossible windows, carrying the weight of all the evenings you can't return to.",
        (5, 12), (0.3, 0.7),
        {'sanity': (3, 8), 'memory': (5, 12)},
        ['melancholy_clouds', 'nostalgic_drizzle', 'calm_before_storm']
    ),
    'temporal_hurricane': WeatherPattern(
        "Temporal Hurricane",
        "A swirling vortex of time fragments tears through the space, scattering moments from different eras.",
        (8, 15), (0.7, 1.0),
        {'memory': (-10, -20), 'reality': (-8, -15), 'confusion': (15, 30)},
        ['time_archaeology', 'temporal_storm', 'echo_wind']
    ),
    'memory_aurora': WeatherPattern(
        "Memory Aurora",
        "Shimmering lights dance across the ceiling, each one a memory playing out in brilliant colors.",
        (6, 10), (0.4, 0.8),
        {'memory': (8, 15), 'wonder': (10, 20)},
        ['nostalgic_drizzle', 'calm_before_storm', 'phantom_snow']
    )
}

# Advanced Quest System with Branching Narratives
class AdvancedQuest:
    def __init__(self, name, description, quest_type, difficulty, chapters, branching_paths, rewards):
        self.name = name
        self.description = description
        self.quest_type = quest_type
        self.difficulty = difficulty
        self.chapters = chapters  # List of quest chapters
        self.current_chapter = 0
        self.branching_paths = branching_paths
        self.rewards = rewards
        self.choices_made = []
        self.progress = 0
        self.status = "available"

ADVANCED_QUEST_DATABASE = {
    'the_librarian_mystery': AdvancedQuest(
        "The Librarian's Mystery",
        "Uncover the truth behind the Shadow Librarian and the books that write themselves",
        "investigation",
        "hard",
        [
            "Encounter the Shadow Librarian",
            "Discover the self-writing books",
            "Find the original author",
            "Uncover the truth about the library",
            "Make a choice about the librarian's fate"
        ],
        {
            'compassionate': "Choose to help the librarian find peace",
            'pragmatic': "Choose to preserve the knowledge at any cost",
            'destructive': "Choose to destroy the corrupted library"
        },
        {
            'compassionate': {'artifact': 'memory_locket', 'sanity': 30},
            'pragmatic': {'artifact': 'truth_mirror', 'memory': 40},
            'destructive': {'artifact': 'void_lantern', 'reality': 35}
        }
    ),
    'temporal_mechanic_apprenticeship': AdvancedQuest(
        "The Temporal Mechanic's Apprentice",
        "Learn the art of timeline repair from the mysterious Temporal Mechanic",
        "learning",
        "medium",
        [
            "Find the Temporal Mechanic's workshop",
            "Complete your first timeline repair",
            "Learn advanced temporal techniques",
            "Handle a major timeline crisis",
            "Graduate or continue as apprentice"
        ],
        {
            'master': "Complete the full apprenticeship",
            'rebel': "Steal the tools and work independently",
            'preserve': "Refuse to tamper with time"
        },
        {
            'master': {'artifact': 'temporal_hourglass', 'special': 'time_mastery'},
            'rebel': {'artifact': 'temporal_tools', 'chaos': 20},
            'preserve': {'sanity': 50, 'wisdom': 30}
        }
    ),
    'void_seamstress_commission': AdvancedQuest(
        "The Void Seamstress's Commission",
        "Help the Void Seamstress repair a catastrophic tear in reality itself",
        "rescue",
        "legendary",
        [
            "Locate the Void Seamstress",
            "Gather starlight thread materials",
            "Learn reality-mending techniques",
            "Confront the source of the tear",
            "Complete the great mending"
        ],
        {
            'sacrifice': "Use your own essence to power the mending",
            'innovation': "Find an alternative power source",
            'acceptance': "Allow the tear to remain but contain it"
        },
        {
            'sacrifice': {'special': 'reality_guardian', 'cost': 'permanent_memory_loss'},
            'innovation': {'artifact': 'reality_anchor', 'sanity': 40},
            'acceptance': {'wisdom': 50, 'artifact': 'void_compass'}
        }
    )
}

# Multi-layered Inventory System
class InventoryItem:
    def __init__(self, name, description, item_type, rarity, weight, effects, durability=100):
        self.name = name
        self.description = description
        self.item_type = item_type  # artifact, consumable, key_item, tool
        self.rarity = rarity
        self.weight = weight
        self.effects = effects
        self.durability = durability
        self.max_durability = durability
        self.equipped = False

class Inventory:
    def __init__(self, max_weight=100):
        self.items = []
        self.max_weight = max_weight
        self.equipped_items = {}
        self.quick_slots = [None] * 4

    def add_item(self, item):
        current_weight = sum(item.weight for item in self.items)
        if current_weight + item.weight <= self.max_weight:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return item
        return None

    def get_total_weight(self):
        return sum(item.weight for item in self.items)

    def sort_by_rarity(self):
        rarity_order = {'common': 1, 'uncommon': 2, 'rare': 3, 'epic': 4, 'legendary': 5}
        self.items.sort(key=lambda x: rarity_order.get(x.rarity, 0), reverse=True)
    
    def append(self, item):
        """Add item to inventory (compatibility method)"""
        if isinstance(item, str):
            # Handle string items
            self.items.append(item)
        else:
            self.add_item(item)
    
    def remove(self, item):
        """Remove item from inventory (compatibility method)"""
        if item in self.items:
            self.items.remove(item)
        else:
            self.remove_item(item)
    
    def __iter__(self):
        """Make inventory iterable"""
        return iter(self.items)
    
    def __contains__(self, item):
        """Support 'in' operator"""
        return item in self.items

# Enhanced Status Effects System
class StatusEffect:
    def __init__(self, name, description, duration, effects, stacks=False, max_stacks=1):
        self.name = name
        self.description = description
        self.duration = duration
        self.effects = effects
        self.stacks = stacks
        self.max_stacks = max_stacks
        self.current_stacks = 1

STATUS_EFFECTS = {
    'temporal_displacement': StatusEffect(
        "Temporal Displacement",
        "Your perception of time is unstable, causing confusion and disorientation",
        5, {'memory': -2, 'confusion': 1}, True, 3
    ),
    'reality_anchor': StatusEffect(
        "Reality Anchor",
        "You feel firmly grounded in reality, resistant to distortions",
        10, {'reality': 3, 'distortion_resistance': 0.5}, False
    ),
    'memory_overflow': StatusEffect(
        "Memory Overflow",
        "Too many memories are surfacing at once, overwhelming your consciousness",
        3, {'sanity': -5, 'memory': 2}, False
    ),
    'dimensional_sight': StatusEffect(
        "Dimensional Sight",
        "You can perceive multiple dimensions simultaneously",
        8, {'revelation_chance': 0.3, 'sanity': -1}, False
    ),
    'void_touched': StatusEffect(
        "Void Touched",
        "Contact with the void has left lasting marks on your psyche",
        15, {'sanity': -3, 'void_resistance': 0.2}, True, 5
    )
}

# Complex Entity Relationship System
class EntityRelationship:
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.trust_level = 0  # -100 to 100
        self.fear_level = 50   # 0 to 100
        self.understanding = 0  # 0 to 100
        self.interactions = 0
        self.last_interaction = None
        self.relationship_events = []

    def interact(self, interaction_type, success):
        self.interactions += 1
        self.last_interaction = interaction_type
        
        if success:
            if interaction_type == "communicate":
                self.trust_level += random.randint(5, 15)
                self.understanding += random.randint(3, 10)
                self.fear_level -= random.randint(2, 8)
            elif interaction_type == "help":
                self.trust_level += random.randint(10, 25)
                self.fear_level -= random.randint(5, 15)
            elif interaction_type == "observe":
                self.understanding += random.randint(2, 8)
                self.fear_level -= random.randint(1, 5)
        else:
            self.trust_level -= random.randint(2, 10)
            self.fear_level += random.randint(5, 15)

        # Clamp values to valid ranges
        self.trust_level = max(-100, min(100, self.trust_level))
        self.fear_level = max(0, min(100, self.fear_level))
        self.understanding = max(0, min(100, self.understanding))

    def get_relationship_status(self):
        if self.trust_level >= 75:
            return "Allied"
        elif self.trust_level >= 50:
            return "Trusted"
        elif self.trust_level >= 25:
            return "Friendly"
        elif self.trust_level >= 0:
            return "Neutral"
        elif self.trust_level >= -25:
            return "Wary"
        elif self.trust_level >= -50:
            return "Hostile"
        else:
            return "Enemy"

# Advanced Crafting System
class CraftingRecipe:
    def __init__(self, name, description, ingredients, result, difficulty, tools_required=None):
        self.name = name
        self.description = description
        self.ingredients = ingredients  # Dict of {item_name: quantity}
        self.result = result
        self.difficulty = difficulty  # 1-10 scale
        self.tools_required = tools_required or []

CRAFTING_RECIPES = {
    'memory_preservative': CraftingRecipe(
        "Memory Preservative",
        "A potion that prevents memory decay in unstable temporal fields",
        {'temporal_essence': 3, 'crystal_of_remembrance': 1, 'stabilized_thought': 2},
        InventoryItem("Memory Preservative", "Protects memories from temporal effects", "consumable", "rare", 0.5, {'memory_protection': 5}),
        6, ['alchemist_tools']
    ),
    'reality_stabilizer': CraftingRecipe(
        "Reality Stabilizer",
        "A device that creates a small field of stable reality",
        {'void_crystal': 2, 'anchor_stone': 1, 'dimensional_wire': 5},
        InventoryItem("Reality Stabilizer", "Creates a zone of stable reality", "tool", "epic", 2.0, {'reality_field': 10}),
        8, ['temporal_tools', 'void_forge']
    ),
    'sanity_salve': CraftingRecipe(
        "Sanity Salve",
        "A soothing balm that helps calm fractured minds",
        {'calming_herb': 4, 'liquid_peace': 2, 'essence_of_clarity': 1},
        InventoryItem("Sanity Salve", "Restores mental stability", "consumable", "uncommon", 0.3, {'sanity_restore': 15}),
        4, ['herbalist_kit']
    )
}

# Dynamic Event System
class DynamicEvent:
    def __init__(self, name, description, trigger_conditions, effects, choices, rarity="common"):
        self.name = name
        self.description = description
        self.trigger_conditions = trigger_conditions
        self.effects = effects
        self.choices = choices
        self.rarity = rarity
        self.triggered = False

DYNAMIC_EVENTS = {
    'temporal_convergence': DynamicEvent(
        "Temporal Convergence",
        "Multiple timelines briefly overlap, showing you glimpses of lives you might have lived",
        {'location_type': 'any', 'sanity': (20, 80), 'memory': (30, 90)},
        {'memory': (10, 25), 'reality': (-5, -15), 'insight': 1},
        [
            ("Focus on the timeline where you made different choices", "focus_alternate"),
            ("Try to stabilize the convergence", "stabilize"),
            ("Let the timelines flow naturally", "accept"),
            ("Flee from the overwhelming visions", "flee")
        ],
        "rare"
    ),
    'entity_gathering': DynamicEvent(
        "Entity Gathering",
        "You stumble upon a meeting of liminal entities discussing matters beyond human comprehension",
        {'entities_encountered': 5, 'understanding': 25},
        {'knowledge': 15, 'sanity': (-5, -10), 'entity_relations': 10},
        [
            ("Attempt to join the conversation", "join"),
            ("Hide and listen", "observe"),
            ("Announce your presence politely", "announce"),
            ("Back away slowly", "retreat")
        ],
        "uncommon"
    ),
    'memory_storm': DynamicEvent(
        "Memory Storm",
        "A violent storm of scattered memories sweeps through the area, each drop containing someone's lost thought",
        {'weather': 'any_storm', 'memory': (10, 50)},
        {'memory': (20, 40), 'sanity': (-10, -20), 'memory_fragments': (1, 3)},
        [
            ("Open yourself to the storm", "embrace"),
            ("Seek shelter immediately", "shelter"),
            ("Try to catch specific memories", "selective"),
            ("Use an artifact for protection", "artifact_protect")
        ],
        "rare"
    ),
    'dimensional_merchant': DynamicEvent(
        "Dimensional Merchant",
        "A traveling merchant from another dimension offers to trade in currencies you've never heard of",
        {'artifacts': 1, 'dimensional_experience': 3},
        {'trading_opportunity': True},
        [
            ("Browse their wares", "browse"),
            ("Offer to trade artifacts", "trade_artifacts"),
            ("Ask about their dimension", "inquire"),
            ("Politely decline and leave", "decline")
        ],
        "uncommon"
    ),
    'reality_glitch': DynamicEvent(
        "Reality Glitch",
        "The fabric of reality develops a glitch, causing the environment to stutter and repeat like a broken record",
        {'reality': (0, 30), 'location_visits': 10},
        {'reality': (-15, -25), 'confusion': 10, 'glitch_exposure': 1},
        [
            ("Try to fix the glitch", "repair"),
            ("Exploit the glitch to your advantage", "exploit"),
            ("Document the phenomenon", "study"),
            ("Wait for it to resolve itself", "wait")
        ],
        "rare"
    )
}

# Enhanced Room Generation System
class AdvancedRoom(Room):
    def __init__(self, theme=None, level=1, special_properties=None):
        super().__init__(theme, level)
        self.special_properties = special_properties or []
        self.room_id = f"{theme}_{random.randint(1000, 9999)}"
        self.environmental_hazards = []
        self.interactive_objects = []
        self.hidden_areas = []
        self.acoustic_properties = self.generate_acoustic_properties()
        self.lighting_conditions = self.generate_lighting_conditions()
        self.temperature_zones = self.generate_temperature_zones()
        self.gravitational_anomalies = []
        self.temporal_pockets = []
        self.generate_environmental_hazards()
        self.generate_interactive_objects()
        self.generate_hidden_areas()

    def generate_acoustic_properties(self):
        return {
            'echo_delay': random.uniform(0.1, 3.0),
            'reverberation': random.uniform(0.0, 1.0),
            'sound_dampening': random.uniform(0.0, 0.8),
            'phantom_sounds': random.choice([True, False]),
            'frequency_distortion': random.uniform(0.0, 0.5)
        }

    def generate_lighting_conditions(self):
        lighting_types = ['flickering', 'steady', 'pulsing', 'absent', 'supernatural', 'color_shifting']
        return {
            'type': random.choice(lighting_types),
            'intensity': random.uniform(0.0, 1.0),
            'color_temperature': random.randint(1000, 10000),
            'shadow_behavior': random.choice(['normal', 'independent', 'absent', 'multiplied'])
        }

    def generate_temperature_zones(self):
        zones = []
        num_zones = random.randint(1, 4)
        for _ in range(num_zones):
            zones.append({
                'area': f"zone_{len(zones)}",
                'temperature': random.randint(-20, 100),
                'humidity': random.uniform(0.0, 1.0),
                'air_pressure': random.uniform(0.5, 2.0)
            })
        return zones

    def generate_environmental_hazards(self):
        hazard_types = [
            'unstable_floor', 'toxic_air', 'radiation_pocket', 'temporal_trap',
            'reality_distortion_field', 'memory_leak', 'emotion_amplifier',
            'gravity_well', 'dimensional_thin_spot', 'psychic_interference'
        ]
        
        num_hazards = random.randint(0, 3)
        for _ in range(num_hazards):
            hazard = {
                'type': random.choice(hazard_types),
                'severity': random.randint(1, 5),
                'location': f"area_{random.randint(1, 10)}",
                'active': True
            }
            self.environmental_hazards.append(hazard)

    def generate_interactive_objects(self):
        object_types = [
            'control_panel', 'mysterious_device', 'information_terminal',
            'art_installation', 'furniture_piece', 'mechanical_construct',
            'organic_growth', 'energy_source', 'communication_device',
            'storage_container', 'experimental_apparatus', 'ritual_circle'
        ]
        
        num_objects = random.randint(1, 6)
        for _ in range(num_objects):
            obj = {
                'type': random.choice(object_types),
                'description': self.generate_object_description(),
                'interaction_type': random.choice(['examine', 'activate', 'manipulate', 'communicate']),
                'requires_tool': random.choice([True, False]),
                'one_time_use': random.choice([True, False]),
                'danger_level': random.randint(0, 3)
            }
            self.interactive_objects.append(obj)

    def generate_object_description(self):
        descriptors = [
            "A crystalline structure", "An organic mass", "A mechanical device",
            "A glowing orb", "A twisted sculpture", "A floating platform",
            "A pulsing membrane", "A geometric pattern", "A liquid container",
            "A resonating chamber"
        ]
        properties = [
            "that hums with energy", "covered in strange symbols", "that shifts between dimensions",
            "radiating warmth", "cold to the touch", "that responds to thoughts",
            "leaking mysterious fluid", "with moving parts", "that whispers secrets",
            "defying physics"
        ]
        return f"{random.choice(descriptors)} {random.choice(properties)}"

    def generate_hidden_areas(self):
        area_types = [
            'secret_passage', 'hidden_chamber', 'maintenance_tunnel',
            'dimensional_pocket', 'forgotten_room', 'concealed_alcove',
            'temporal_bubble', 'phase_shifted_space', 'perception_blind_spot'
        ]
        
        num_areas = random.randint(0, 2)
        for _ in range(num_areas):
            area = {
                'type': random.choice(area_types),
                'discovery_method': random.choice(['observation', 'interaction', 'artifact_use', 'accident']),
                'contents': self.generate_hidden_contents(),
                'discovered': False
            }
            self.hidden_areas.append(area)

    def generate_hidden_contents(self):
        contents = []
        possible_contents = [
            'rare_artifact', 'memory_cache', 'information_fragment',
            'tool_upgrade', 'entity_remnant', 'dimensional_map',
            'temporal_anchor', 'reality_stabilizer', 'consciousness_backup'
        ]
        
        num_contents = random.randint(1, 3)
        for _ in range(num_contents):
            contents.append(random.choice(possible_contents))
        return contents

# Massive Procedural Content Generation System
class ProceduralGenerator:
    def __init__(self):
        self.entity_templates = self.load_entity_templates()
        self.room_modifiers = self.load_room_modifiers()
        self.story_fragments = self.load_story_fragments()
        self.atmospheric_elements = self.load_atmospheric_elements()

    def load_entity_templates(self):
        return {
            'memory_based': {
                'names': ['Memory Keeper', 'Past Walker', 'Echo Guardian', 'Nostalgia Weaver', 'Time Shepherd'],
                'behaviors': ['memory_preservation', 'temporal_guidance', 'past_protection'],
                'descriptions': [
                    "A figure wrapped in wisps of fading photographs",
                    "An entity whose form shifts between different ages of the same person",
                    "A being composed of overlapping silhouettes from various time periods"
                ]
            },
            'void_touched': {
                'names': ['Void Speaker', 'Darkness Herald', 'Empty One', 'Silence Walker', 'Nothing Bearer'],
                'behaviors': ['void_manipulation', 'reality_erasure', 'silence_spreading'],
                'descriptions': [
                    "A humanoid absence that exists more as a lack of something than a presence",
                    "A figure that seems to absorb light and sound from the surrounding area",
                    "An entity whose outline wavers like heat distortion over darkness"
                ]
            },
            'temporal_anomaly': {
                'names': ['Time Fracture', 'Moment Collector', 'Chronos Fragment', 'Duration Entity', 'Temporal Paradox'],
                'behaviors': ['time_distortion', 'moment_capture', 'causality_disruption'],
                'descriptions': [
                    "A being that exists in multiple time states simultaneously",
                    "An entity that moves through time like swimming through water",
                    "A figure whose actions create ripples in the timeline itself"
                ]
            }
        }

    def load_room_modifiers(self):
        return {
            'gravitational': [
                'Objects float freely in zero gravity',
                'Gravity shifts direction every few minutes',
                'Heavy gravity makes movement difficult',
                'Localized gravity wells create dangerous zones'
            ],
            'temporal': [
                'Time moves faster in certain areas',
                'Temporal loops cause actions to repeat',
                'The past and future bleed through into the present',
                'Different areas experience time at different rates'
            ],
            'dimensional': [
                'Walls phase in and out of existence',
                'Multiple dimensions overlap in this space',
                'Portals to other realities flicker open randomly',
                'The room exists partially in several dimensions'
            ],
            'psychological': [
                'The space reflects your emotional state',
                'Thoughts become visible as floating text',
                'Memories manifest as physical objects',
                'The room responds to your fears and desires'
            ]
        }

    def load_story_fragments(self):
        return [
            "You find a note written in your own handwriting, but you don't remember writing it",
            "A clock on the wall ticks backward, and you feel years falling away from your life",
            "Your reflection in a broken mirror shows someone you might have become",
            "The sound of children playing echoes from a playground that isn't there",
            "A door appears where there was none before, marked with your initials",
            "You smell your grandmother's perfume, though she's been gone for years",
            "A photograph develops before your eyes, showing a scene you don't remember living",
            "Your phone rings with a call from your own number",
            "Footprints in dust lead away from where you're standing, made by your own shoes",
            "A diary entry appears in a book, dated tomorrow, describing what you're doing now"
        ]

    def load_atmospheric_elements(self):
        return {
            'sounds': [
                'Distant conversations in languages that do not exist',
                'The ticking of a clock that has no hands',
                'Whispers that stop when you try to listen',
                'Music from a radio that is not tuned to any station',
                'Footsteps that follow your rhythm exactly',
                'The sound of pages turning in an empty room',
                'Laughter that echoes from your past',
                'Keys jingling in empty pockets',
                'Rain against windows that show clear skies',
                'A phone ringing in a disconnected booth'
            ],
            'smells': [
                'Old books in a place with no library',
                'Coffee brewing in an abandoned kitchen',
                'Flowers that bloom only in memory',
                'Chalk dust from empty classrooms',
                'Rain on hot asphalt during drought',
                'Your childhood home unique scent',
                'Perfume worn by someone long gone',
                'Fresh bread from a bakery that closed years ago',
                'Cigarette smoke from a party you never attended',
                'The ocean despite being nowhere near water'
            ],
            'textures': [
                'Walls that feel warm to the touch like living skin',
                'Floors that yield slightly like they are breathing',
                'Surfaces that feel familiar despite being foreign',
                'Materials that change texture as you touch them',
                'Objects that feel heavier with emotional weight',
                'Smooth surfaces that somehow retain fingerprints',
                'Rough textures that tell stories through touch',
                'Surfaces that pulse with hidden rhythms',
                'Materials that feel like liquid but behave like solid',
                'Textures that trigger sense memories'
            ]
        }

    def generate_procedural_entity(self, level, theme):
        template_type = random.choice(list(self.entity_templates.keys()))
        template = self.entity_templates[template_type]
        
        name = random.choice(template['names'])
        behavior = random.choice(template['behaviors'])
        description = random.choice(template['descriptions'])
        threat_level = min(5, max(1, level + random.randint(-1, 2)))
        
        return Entity(name, description, behavior, threat_level)

    def generate_procedural_room_modifier(self):
        modifier_type = random.choice(list(self.room_modifiers.keys()))
        return random.choice(self.room_modifiers[modifier_type])

    def generate_story_fragment(self):
        return random.choice(self.story_fragments)

    def generate_atmospheric_element(self):
        element_type = random.choice(['sounds', 'smells', 'textures'])
        return {
            'type': element_type,
            'description': random.choice(self.atmospheric_elements[element_type])
        }

# Advanced Interaction System
class InteractionSystem:
    def __init__(self):
        self.interaction_history = []
        self.entity_memories = {}
        self.relationship_modifiers = {}

    def process_entity_interaction(self, player, entity, interaction_type):
        """Process complex interactions with entities"""
        if entity.name not in player.entity_relationships:
            player.entity_relationships[entity.name] = EntityRelationship(entity.name)
        
        relationship = player.entity_relationships[entity.name]
        success_chance = self.calculate_success_chance(player, entity, interaction_type, relationship)
        success = random.random() < success_chance
        
        self.record_interaction(player, entity, interaction_type, success)
        relationship.interact(interaction_type, success)
        
        return self.generate_interaction_result(player, entity, interaction_type, success, relationship)

    def calculate_success_chance(self, player, entity, interaction_type, relationship):
        base_chance = 0.5
        
        # Relationship modifiers
        if relationship.trust_level > 50:
            base_chance += 0.3
        elif relationship.trust_level < -25:
            base_chance -= 0.4
        
        # Fear modifier
        fear_penalty = relationship.fear_level / 200.0  # 0 to 0.5
        base_chance -= fear_penalty
        
        # Understanding bonus
        understanding_bonus = relationship.understanding / 200.0  # 0 to 0.5
        base_chance += understanding_bonus
        
        # Player state modifiers
        if player.sanity < 30:
            base_chance -= 0.3
        if player.reality < 40:
            base_chance -= 0.2
        
        # Interaction type modifiers
        type_modifiers = {
            'communicate': 0.1,
            'observe': 0.2,
            'help': -0.1,  # Harder but more rewarding
            'challenge': -0.3,
            'flee': 0.8  # Almost always successful
        }
        base_chance += type_modifiers.get(interaction_type, 0)
        
        return max(0.05, min(0.95, base_chance))

    def record_interaction(self, player, entity, interaction_type, success):
        interaction = {
            'entity': entity.name,
            'type': interaction_type,
            'success': success,
            'player_state': {
                'sanity': player.sanity,
                'reality': player.reality,
                'memory': player.memory
            },
            'timestamp': time.time()
        }
        self.interaction_history.append(interaction)
        player.journal.add_entry("interaction", f"{interaction_type} with {entity.name}: {'Success' if success else 'Failed'}", 2)

    def generate_interaction_result(self, player, entity, interaction_type, success, relationship):
        results = {
            'text': '',
            'effects': {},
            'unlocks': []
        }
        
        if success:
            results['text'] = self.get_success_text(entity, interaction_type, relationship)
            results['effects'] = self.get_success_effects(entity, interaction_type, relationship)
        else:
            results['text'] = self.get_failure_text(entity, interaction_type, relationship)
            results['effects'] = self.get_failure_effects(entity, interaction_type, relationship)
        
        return results

    def get_success_text(self, entity, interaction_type, relationship):
        success_texts = {
            'communicate': {
                'low_trust': f"{entity.name} responds cautiously to your attempt at communication.",
                'medium_trust': f"{entity.name} engages in meaningful exchange with you.",
                'high_trust': f"{entity.name} speaks with you like an old friend."
            },
            'observe': {
                'low_trust': f"You carefully study {entity.name} from a distance.",
                'medium_trust': f"{entity.name} allows you to observe its nature more closely.",
                'high_trust': f"{entity.name} reveals hidden aspects of its existence to you."
            },
            'help': {
                'low_trust': f"Your offer of help seems to surprise {entity.name}.",
                'medium_trust': f"{entity.name} gratefully accepts your assistance.",
                'high_trust': f"{entity.name} is deeply moved by your continued support."
            }
        }
        
        trust_level = 'high_trust' if relationship.trust_level > 50 else 'medium_trust' if relationship.trust_level > 0 else 'low_trust'
        return success_texts.get(interaction_type, {}).get(trust_level, f"You successfully interact with {entity.name}.")

    def get_failure_text(self, entity, interaction_type, relationship):
        failure_texts = {
            'communicate': f"{entity.name} seems unable or unwilling to understand you.",
            'observe': f"{entity.name} notices your observation and becomes guarded.",
            'help': f"Your attempt to help {entity.name} somehow makes things worse."
        }
        return failure_texts.get(interaction_type, f"Your interaction with {entity.name} doesn't go as planned.")

    def get_success_effects(self, entity, interaction_type, relationship):
        effects = {}
        
        if interaction_type == 'communicate':
            effects['sanity'] = random.randint(3, 8)
            effects['understanding'] = random.randint(2, 5)
        elif interaction_type == 'observe':
            effects['memory'] = random.randint(2, 6)
            effects['insight'] = 1
        elif interaction_type == 'help':
            effects['sanity'] = random.randint(5, 15)
            effects['trust_bonus'] = random.randint(10, 20)
        
        return effects

    def get_failure_effects(self, entity, interaction_type, relationship):
        effects = {}
        
        if interaction_type == 'communicate':
            effects['sanity'] = random.randint(-5, -2)
        elif interaction_type == 'observe':
            effects['reality'] = random.randint(-3, -1)
        elif interaction_type == 'help':
            effects['sanity'] = random.randint(-8, -3)
            effects['trust_penalty'] = random.randint(-15, -5)
        
        return effects

# Enhanced Save System with Rich Metadata
class AdvancedSaveSystem:
    def __init__(self):
        self.save_metadata = {}
        self.backup_saves = {}
        self.save_statistics = {}

    def save_game_advanced(self, player, slot, save_name=""):
        """Advanced save system with metadata and statistics"""
        save_data = {
            'player': self.serialize_player(player),
            'metadata': {
                'save_name': save_name or f"Save {slot}",
                'timestamp': time.time(),
                'game_version': "2.0",
                'play_time': getattr(player, 'play_time', 0),
                'difficulty_level': getattr(player, 'difficulty_level', 'normal'),
                'achievements_unlocked': len(getattr(player, 'achievements', [])),
                'locations_visited': len(player.journal.locations_visited) if hasattr(player, 'journal') else 0,
                'entities_encountered': len(player.entity_relationships) if hasattr(player, 'entity_relationships') else 0
            },
            'statistics': self.generate_save_statistics(player),
            'screenshot_data': self.generate_screenshot_data(player)
        }
        
        # Create backup of existing save
        if os.path.exists(f"{SAVE_DIR}/save_{slot}.pkl"):
            self.create_backup(slot)
        
        try:
            with open(f"{SAVE_DIR}/save_{slot}.pkl", 'wb') as f:
                pickle.dump(save_data, f)
            
            self.save_metadata[slot] = save_data['metadata']
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def serialize_player(self, player):
        """Convert player object to serializable dictionary"""
        return {
            'x': player.x,
            'y': player.y,
            'z': player.z,
            'sanity': player.sanity,
            'reality': player.reality,
            'memory': player.memory,
            'moves_made': getattr(player, 'moves_made', 0),
            'artifacts': [self.serialize_artifact(artifact) for artifact in getattr(player, 'artifacts', [])],
            'journal': self.serialize_journal(getattr(player, 'journal', None)),
            'quest_system': self.serialize_quest_system(getattr(player, 'quest_system', None)),
            'entity_relationships': {name: self.serialize_relationship(rel) for name, rel in getattr(player, 'entity_relationships', {}).items()},
            'status_effects': getattr(player, 'status_effects', []),
            'inventory': self.serialize_inventory(getattr(player, 'inventory', None))
        }

    def serialize_artifact(self, artifact):
        return {
            'name': artifact.name,
            'description': artifact.description,
            'power_type': artifact.power_type,
            'strength': artifact.strength,
            'rarity': artifact.rarity,
            'uses': artifact.uses
        }

    def serialize_journal(self, journal):
        if not journal:
            return None
        return {
            'entries': journal.entries,
            'entity_encounters': journal.entity_encounters,
            'locations_visited': journal.locations_visited,
            'artifacts_found': journal.artifacts_found,
            'insights_gained': journal.insights_gained,
            'total_entries': journal.total_entries
        }

    def serialize_quest_system(self, quest_system):
        if not quest_system:
            return None
        return {
            'active_quests': quest_system.active_quests,
            'completed_quests': quest_system.completed_quests,
            'failed_quests': quest_system.failed_quests
        }

    def serialize_relationship(self, relationship):
        return {
            'entity_name': relationship.entity_name,
            'trust_level': relationship.trust_level,
            'fear_level': relationship.fear_level,
            'understanding': relationship.understanding,
            'interactions': relationship.interactions
        }

    def serialize_inventory(self, inventory):
        if not inventory:
            return None
        return {
            'items': [self.serialize_inventory_item(item) for item in inventory.items],
            'max_weight': inventory.max_weight,
            'equipped_items': inventory.equipped_items
        }

    def serialize_inventory_item(self, item):
        return {
            'name': item.name,
            'description': item.description,
            'item_type': item.item_type,
            'rarity': item.rarity,
            'weight': item.weight,
            'effects': item.effects,
            'durability': item.durability
        }

    def generate_save_statistics(self, player):
        """Generate comprehensive statistics for the save"""
        return {
            'total_moves': getattr(player, 'moves_made', 0),
            'entities_befriended': sum(1 for rel in getattr(player, 'entity_relationships', {}).values() if rel.trust_level > 50),
            'artifacts_collected': len(getattr(player, 'artifacts', [])),
            'memory_fragments_found': len([entry for entry in getattr(player.journal, 'entries', []) if entry.get('type') == 'memory']) if hasattr(player, 'journal') else 0,
            'quests_completed': len(getattr(player.quest_system, 'completed_quests', [])) if hasattr(player, 'quest_system') else 0,
            'dimensional_rifts_used': getattr(player, 'dimensional_experience', 0),
            'meditation_sessions': getattr(player, 'meditation_points', 0),
            'weather_events_survived': getattr(player, 'weather_events_survived', 0),
            'highest_sanity': getattr(player, 'highest_sanity', player.sanity),
            'lowest_sanity': getattr(player, 'lowest_sanity', player.sanity),
            'time_spent_exploring': getattr(player, 'exploration_time', 0)
        }

    def generate_screenshot_data(self, player):
        """Generate a text-based 'screenshot' of the current game state"""
        return {
            'current_location': f"({player.x}, {player.y}, {player.z})",
            'player_status': f"Sanity: {player.sanity}, Reality: {player.reality}, Memory: {player.memory}",
            'recent_events': getattr(player.journal, 'entries', [])[-5:] if hasattr(player, 'journal') else [],
            'active_effects': getattr(player, 'status_effects', [])
        }

    def create_backup(self, slot):
        """Create a backup of the existing save"""
        try:
            backup_filename = f"{SAVE_DIR}/save_{slot}_backup.pkl"
            original_filename = f"{SAVE_DIR}/save_{slot}.pkl"
            
            if os.path.exists(original_filename):
                with open(original_filename, 'rb') as original:
                    with open(backup_filename, 'wb') as backup:
                        backup.write(original.read())
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")

    def load_game_advanced(self, slot):
        """Advanced load system with error recovery"""
        try:
            filename = f"{SAVE_DIR}/save_{slot}.pkl"
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'rb') as f:
                save_data = pickle.load(f)
            
            return self.deserialize_save_data(save_data)
        except Exception as e:
            print(f"Error loading save: {e}")
            # Try to load backup
            return self.load_backup(slot)

    def load_backup(self, slot):
        """Attempt to load from backup save"""
        try:
            backup_filename = f"{SAVE_DIR}/save_{slot}_backup.pkl"
            if os.path.exists(backup_filename):
                with open(backup_filename, 'rb') as f:
                    save_data = pickle.load(f)
                print("Loaded from backup save due to corruption in main save.")
                return self.deserialize_save_data(save_data)
        except Exception as e:
            print(f"Backup save also corrupted: {e}")
        return None

    def deserialize_save_data(self, save_data):
        """Convert save data back to game objects"""
        player_data = save_data['player']
        
        # Create a new player object with saved data using the actual Player class
        player = Player(
            name=player_data.get('name', 'Unknown'),
            x=player_data['x'],
            y=player_data['y'],
            z=player_data['z'],
            sanity=player_data['sanity'],
            level=player_data.get('level', 1)
        )
        
        # Update additional attributes
        player.reality = player_data['reality']
        player.memory = player_data['memory']
        player.moves_made = player_data.get('moves_made', 0)
        
        # Restore complex objects
        player.artifacts = [self.deserialize_artifact(artifact_data) for artifact_data in player_data.get('artifacts', [])]
        player.journal = self.deserialize_journal(player_data.get('journal'))
        player.quest_system = self.deserialize_quest_system(player_data.get('quest_system'))
        player.entity_relationships = {name: self.deserialize_relationship(rel_data) for name, rel_data in player_data.get('entity_relationships', {}).items()}
        player.status_effects = player_data.get('status_effects', [])
        player.inventory = self.deserialize_inventory(player_data.get('inventory'))
        
        return player

    def deserialize_artifact(self, artifact_data):
        artifact = Artifact(
            artifact_data['name'],
            artifact_data['description'],
            artifact_data['power_type'],
            artifact_data['strength'],
            artifact_data['rarity']
        )
        artifact.uses = artifact_data['uses']
        return artifact

    def deserialize_journal(self, journal_data):
        if not journal_data:
            return Journal()
        
        journal = Journal()
        journal.entries = journal_data['entries']
        journal.entity_encounters = journal_data['entity_encounters']
        journal.locations_visited = journal_data['locations_visited']
        journal.artifacts_found = journal_data['artifacts_found']
        journal.insights_gained = journal_data['insights_gained']
        journal.total_entries = journal_data['total_entries']
        return journal

    def deserialize_quest_system(self, quest_data):
        if not quest_data:
            return QuestSystem()
        
        quest_system = QuestSystem()
        quest_system.active_quests = quest_data['active_quests']
        quest_system.completed_quests = quest_data['completed_quests']
        quest_system.failed_quests = quest_data['failed_quests']
        return quest_system

    def deserialize_relationship(self, rel_data):
        relationship = EntityRelationship(rel_data['entity_name'])
        relationship.trust_level = rel_data['trust_level']
        relationship.fear_level = rel_data['fear_level']
        relationship.understanding = rel_data['understanding']
        relationship.interactions = rel_data['interactions']
        return relationship

    def deserialize_inventory(self, inventory_data):
        if not inventory_data:
            return Inventory()
        
        inventory = Inventory(inventory_data['max_weight'])
        inventory.items = [self.deserialize_inventory_item(item_data) for item_data in inventory_data['items']]
        inventory.equipped_items = inventory_data['equipped_items']
        return inventory

    def deserialize_inventory_item(self, item_data):
        item = InventoryItem(
            item_data['name'],
            item_data['description'],
            item_data['item_type'],
            item_data['rarity'],
            item_data['weight'],
            item_data['effects']
        )
        item.durability = item_data['durability']
        return item

    def get_save_preview(self, slot):
        """Get a preview of save data without fully loading"""
        try:
            filename = f"{SAVE_DIR}/save_{slot}.pkl"
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'rb') as f:
                save_data = pickle.load(f)
            
            metadata = save_data.get('metadata', {})
            statistics = save_data.get('statistics', {})
            
            return {
                'name': metadata.get('save_name', f'Save {slot}'),
                'timestamp': metadata.get('timestamp', 0),
                'play_time': metadata.get('play_time', 0),
                'level': statistics.get('total_moves', 0),
                'achievements': metadata.get('achievements_unlocked', 0),
                'locations': metadata.get('locations_visited', 0)
            }
        except Exception:
            return None

# Advanced Statistics and Analytics System
class GameAnalytics:
    def __init__(self):
        self.session_data = {}
        self.lifetime_stats = {}
        self.performance_metrics = {}

    def start_session(self, player):
        """Initialize analytics for a new game session"""
        self.session_data = {
            'start_time': time.time(),
            'starting_stats': {
                'sanity': player.sanity,
                'reality': player.reality,
                'memory': player.memory
            },
            'actions_taken': [],
            'entities_encountered': [],
            'locations_visited': [],
            'events_triggered': []
        }

    def track_action(self, action_type, details=None):
        """Track player actions for analytics"""
        action = {
            'type': action_type,
            'timestamp': time.time(),
            'details': details or {}
        }
        self.session_data['actions_taken'].append(action)

    def track_entity_encounter(self, entity_name, interaction_result):
        """Track entity encounters and outcomes"""
        encounter = {
            'entity': entity_name,
            'timestamp': time.time(),
            'result': interaction_result
        }
        self.session_data['entities_encountered'].append(encounter)

    def track_location_visit(self, location_type, coordinates):
        """Track location visits"""
        visit = {
            'type': location_type,
            'coordinates': coordinates,
            'timestamp': time.time()
        }
        self.session_data['locations_visited'].append(visit)

    def generate_session_report(self, player):
        """Generate a comprehensive session report"""
        session_duration = time.time() - self.session_data['start_time']
        
        report = {
            'session_duration': session_duration,
            'actions_per_minute': len(self.session_data['actions_taken']) / (session_duration / 60),
            'unique_entities_met': len(set(e['entity'] for e in self.session_data['entities_encountered'])),
            'locations_explored': len(set(v['type'] for v in self.session_data['locations_visited'])),
            'stat_changes': {
                'sanity': player.sanity - self.session_data['starting_stats']['sanity'],
                'reality': player.reality - self.session_data['starting_stats']['reality'],
                'memory': player.memory - self.session_data['starting_stats']['memory']
            },
            'most_common_actions': self.get_most_common_actions(),
            'exploration_pattern': self.analyze_exploration_pattern(),
            'difficulty_assessment': self.assess_difficulty_level(player)
        }
        
        return report

    def get_most_common_actions(self):
        """Analyze most frequently taken actions"""
        action_counts = {}
        for action in self.session_data['actions_taken']:
            action_type = action['type']
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    def analyze_exploration_pattern(self):
        """Analyze how the player explores the space"""
        if not self.session_data['locations_visited']:
            return "No exploration data"
        
        coordinates = [v['coordinates'] for v in self.session_data['locations_visited']]
        
        # Calculate exploration radius
        center_x = sum(c[0] for c in coordinates) / len(coordinates)
        center_y = sum(c[1] for c in coordinates) / len(coordinates)
        
        max_distance = max(((c[0] - center_x)**2 + (c[1] - center_y)**2)**0.5 for c in coordinates)
        
        if max_distance < 10:
            return "Cautious - stays in small area"
        elif max_distance < 50:
            return "Moderate - explores nearby areas"
        else:
            return "Bold - ventures far from starting point"

    def assess_difficulty_level(self, player):
        """Assess how difficult the game has been for the player"""
        stat_total = player.sanity + player.reality + player.memory
        starting_total = sum(self.session_data['starting_stats'].values())
        
        if stat_total < starting_total * 0.5:
            return "Very Challenging"
        elif stat_total < starting_total * 0.75:
            return "Challenging"
        elif stat_total < starting_total * 1.1:
            return "Balanced"
        else:
            return "Manageable"

# Enhanced Menu System with Rich Interfaces
class AdvancedMenuSystem:
    def __init__(self):
        self.menu_stack = []
        self.current_menu = None

    def display_main_menu(self, player):
        """Display an enhanced main menu with statistics and options"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Style.BRIGHT}{Fore.WHITE}LIMINAL SPACE - ADVANCED INTERFACE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Player status bar
        self.display_status_bar(player)
        
        print(f"\n{Fore.YELLOW}📍 NAVIGATION & MOVEMENT{Style.RESET_ALL}")
        print("  /right /left /forward /backward /upstairs /downstairs")
        
        print(f"\n{Fore.MAGENTA}🎯 ACTIONS & INTERACTIONS{Style.RESET_ALL}")
        print("  /interact - Interact with entities or objects")
        print("  /meditate - Enter meditation for restoration")
        print("  /journal - View your exploration journal")
        print("  /inventory - Manage items and artifacts")
        print("  /quests - View active and completed quests")
        
        print(f"\n{Fore.CYAN}🛠️ GAME MANAGEMENT{Style.RESET_ALL}")
        print("  /save - Advanced save system")
        print("  /load - Load saved games")
        print("  /settings - Game settings and preferences")
        print("  /analytics - View detailed statistics")
        print("  /help - Extended help system")
        print("  /quit - Exit the game")
        
        # Recent activity summary
        if hasattr(player, 'journal') and player.journal.entries:
            print(f"\n{Fore.GREEN}📝 RECENT ACTIVITY{Style.RESET_ALL}")
            recent = player.journal.entries[-3:]
            for entry in recent:
                importance = "⭐" * entry['importance']
                print(f"  [{entry['timestamp']}] {importance} {entry['content']}")

    def display_status_bar(self, player):
        """Display a comprehensive status bar"""
        # Health bars with color coding
        sanity_bar = self.create_progress_bar(player.sanity, SANITY_MAX, Fore.GREEN, Fore.YELLOW, Fore.RED)
        reality_bar = self.create_progress_bar(player.reality, REALITY_MAX, Fore.BLUE, Fore.CYAN, Fore.MAGENTA)
        memory_bar = self.create_progress_bar(player.memory, MEMORY_MAX, Fore.WHITE, Fore.LIGHTBLACK_EX, Fore.RED)
        
        print(f"\n{Fore.WHITE}🧠 MENTAL STATE{Style.RESET_ALL}")
        print(f"  Sanity:  {sanity_bar} {player.sanity}/{SANITY_MAX}")
        print(f"  Reality: {reality_bar} {player.reality}/{REALITY_MAX}")
        print(f"  Memory:  {memory_bar} {player.memory}/{MEMORY_MAX}")
        
        # Location and movement info
        print(f"\n{Fore.YELLOW}📍 LOCATION{Style.RESET_ALL}")
        print(f"  Coordinates: ({player.x}, {player.y}, {player.z})")
        print(f"  Moves Made: {getattr(player, 'moves_made', 0)}")
        
        # Quick stats
        if hasattr(player, 'artifacts'):
            print(f"  Artifacts: {len(player.artifacts)}")
        if hasattr(player, 'entity_relationships'):
            friendly_entities = sum(1 for rel in player.entity_relationships.values() if rel.trust_level > 25)
            print(f"  Friendly Entities: {friendly_entities}")

    def create_progress_bar(self, current, maximum, high_color, med_color, low_color):
        """Create a colored progress bar"""
        percentage = current / maximum
        bar_length = 20
        filled = int(bar_length * percentage)
        
        if percentage > 0.6:
            color = high_color
        elif percentage > 0.3:
            color = med_color
        else:
            color = low_color
        
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"{color}{bar}{Style.RESET_ALL}"

    def display_inventory_menu(self, player):
        """Display comprehensive inventory management"""
        if not hasattr(player, 'inventory') or not player.inventory:
            print("No inventory system initialized.")
            return
        
        inventory = player.inventory
        
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Style.BRIGHT}INVENTORY MANAGEMENT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        # Weight information
        current_weight = inventory.get_total_weight()
        weight_bar = self.create_progress_bar(current_weight, inventory.max_weight, Fore.GREEN, Fore.YELLOW, Fore.RED)
        print(f"\n{Fore.CYAN}📦 CARRYING CAPACITY{Style.RESET_ALL}")
        print(f"Weight: {weight_bar} {current_weight:.1f}/{inventory.max_weight}")
        
        # Items by category
        categories = {}
        for item in inventory.items:
            if item.item_type not in categories:
                categories[item.item_type] = []
            categories[item.item_type].append(item)
        
        for category, items in categories.items():
            print(f"\n{Fore.YELLOW}{category.upper()}{Style.RESET_ALL}")
            for item in items:
                rarity_color = {
                    'common': Fore.WHITE,
                    'uncommon': Fore.GREEN,
                    'rare': Fore.BLUE,
                    'epic': Fore.MAGENTA,
                    'legendary': Fore.YELLOW
                }.get(item.rarity, Fore.WHITE)
                
                condition = "Perfect" if item.durability == item.max_durability else "Damaged" if item.durability > item.max_durability * 0.5 else "Broken"
                print(f"  {rarity_color}● {item.name}{Style.RESET_ALL} ({condition})")
                print(f"    {item.description}")

# Massive Extended Content Database for Maximum Scale
EXTENDED_ENTITY_BEHAVIORS = {
    'reality_weaver': "Manipulates the fundamental structure of reality, creating pockets of altered physics",
    'time_sculptor': "Carves moments from the timestream and reshapes them into art",
    'memory_archaeologist': "Excavates forgotten memories from the collective unconscious",
    'dimension_bridger': "Creates connections between parallel realities",
    'chaos_orchestrator': "Conducts symphonies of entropy and disorder",
    'pattern_breaker': "Disrupts established routines and expected outcomes",
    'silence_composer': "Writes music in the language of absolute quiet",
    'shadow_cartographer': "Maps the territories that exist between light and dark",
    'void_gardener': "Cultivates growths of nothingness in empty spaces",
    'paradox_resolver': "Solves contradictions by embracing impossibility",
    'echo_translator': "Interprets the meaning hidden in reverberations",
    'threshold_guardian': "Protects the boundaries between known and unknown",
    'fragment_assembler': "Pieces together broken aspects of existence",
    'resonance_tuner': "Adjusts the vibrational frequency of reality",
    'probability_shepherd': "Guides unlikely events toward manifestation"
}

EXTENDED_ATMOSPHERIC_DESCRIPTIONS = [
    "The air shimmers with crystallized thoughts that tinkle like wind chimes when disturbed",
    "Gravity pools in certain corners, creating small waterfalls of falling dust and debris",
    "Temperature fluctuates wildly, creating microclimates of memory and emotion",
    "Sound travels in visible waves, allowing you to see conversations before hearing them",
    "The walls breathe slowly, expanding and contracting with an otherworldly rhythm",
    "Light here has weight, casting shadows that feel solid under your fingers",
    "Time moves in eddies and currents, speeding up and slowing down unpredictably",
    "Colors that don't exist in normal reality paint the surfaces in impossible hues",
    "The floor occasionally becomes transparent, revealing infinite depths below",
    "Whispered secrets from decades past echo constantly in the background",
    "Static electricity carries fragments of unfinished thoughts between your fingers",
    "The ceiling occasionally dissolves, revealing skies from different dimensions",
    "Magnetic fields pull at metallic objects, creating a subtle dance of attraction",
    "Pressure waves from distant explosions ripple through the space every few minutes",
    "The very atoms here seem to vibrate with anticipation of something momentous"
]

COMPLEX_ROOM_INTERACTIONS = {
    'temporal_laboratory': {
        'examine_equipment': "Ancient machinery hums with temporal energy, displaying readouts in languages from futures that may never come to pass",
        'activate_device': "The temporal manipulation device activates, causing reality to stutter and skip like a damaged recording",
        'read_notes': "Research notes detail experiments in causality reversal and timeline splicing, written in increasingly desperate handwriting",
        'touch_crystal': "The temporal focus crystal pulses with your heartbeat, synchronizing your personal timeline with the room's flow"
    },
    'memory_archive': {
        'browse_files': "Countless filing cabinets stretch into darkness, each drawer labeled with dates and emotions rather than names",
        'open_drawer': "The drawer slides open to reveal crystallized memories floating in preservative fluid, each one glowing with residual emotion",
        'read_memory': "You touch a memory crystal and experience someone else's first day of school, complete with the taste of anxiety and new shoes",
        'catalog_system': "The archival system responds to emotional queries rather than logical searches, organizing memories by feeling rather than chronology"
    },
    'dimensional_workshop': {
        'inspect_tools': "Tools that exist in multiple dimensions simultaneously hang from pegboards, their handles shifting between realities",
        'examine_projects': "Half-finished dimensional bridges and reality anchors litter the workbenches, abandoned in various states of completion",
        'operate_machinery': "The dimensional forge roars to life, bending space around itself as it processes raw possibility into solid form",
        'read_blueprints': "Blueprints for impossible architecture cover the walls, detailing structures that exist in seventeen dimensions"
    }
}

EXPANDED_QUEST_CHAINS = {
    'the_lost_expedition': {
        'chapters': [
            "Discover evidence of a previous expedition into liminal space",
            "Follow the trail of abandoned equipment and personal belongings",
            "Find the expedition leader's journal detailing their discoveries",
            "Locate the team's final camp and uncover what happened to them",
            "Choose whether to rescue survivors or preserve their sacrifice"
        ],
        'branching_points': {
            'rescue_attempt': "Risk everything to save the survivors",
            'honor_sacrifice': "Respect their choice and continue their mission",
            'expose_truth': "Reveal the expedition's fate to the outside world"
        },
        'hidden_paths': [
            "Discover the expedition found a way to permanently escape liminal space",
            "Learn they became entities themselves, choosing to remain",
            "Uncover evidence they were sent here deliberately as test subjects"
        ]
    },
    'the_collector_conspiracy': {
        'chapters': [
            "Notice certain artifacts are being systematically collected",
            "Investigate who or what is gathering these powerful items",
            "Discover a network of entities working together for unknown purposes",
            "Infiltrate their organization to learn their ultimate goal",
            "Decide whether to stop them or join their cause"
        ],
        'branching_points': {
            'join_collectors': "Become part of their artifact gathering operation",
            'oppose_collectors': "Work to stop their mysterious plan",
            'manipulate_collectors': "Play both sides for your own benefit"
        },
        'hidden_paths': [
            "Discover the collectors are trying to repair a fundamental tear in reality",
            "Learn they're gathering power to escape liminal space entirely",
            "Uncover that you're the artifact they've been seeking all along"
        ]
    }
}

ENVIRONMENTAL_STORYTELLING_ELEMENTS = {
    'abandoned_belongings': [
        "A child's toy, worn smooth by countless hands, sits alone on a dusty shelf",
        "Reading glasses rest on an open book, the page yellowed with age and marked with tearstains",
        "A wedding ring rolls endlessly in a perfect circle on a tilted table",
        "Shoes arranged by a door as if their owner just stepped inside",
        "A half-finished letter lies next to a dried inkwell, the final words trailing off mid-sentence",
        "Family photographs with faces that seem to shift when you're not looking directly at them",
        "A suitcase packed for a trip that was never taken, tags still attached",
        "Coffee cups with lipstick stains, still warm despite the absence of any heat source",
        "House keys hanging on hooks labeled with addresses that don't exist",
        "A diary with entries that continue writing themselves in fading ink"
    ],
    'architectural_anomalies': [
        "Stairs that ascend in a perfect loop, returning climbers to where they started",
        "Windows that show different views depending on the angle you look through them",
        "Doors that open to reveal the same room you're standing in",
        "Hallways that stretch longer when you're walking one direction than the other",
        "Mirrors that reflect rooms other than the one you're in",
        "Light switches that control illumination in distant, unseen spaces",
        "Ventilation grates that whisper conversations from other buildings",
        "Floor tiles that rearrange themselves when no one is watching",
        "Ceiling fans that spin at different speeds in each direction simultaneously",
        "Thermostats that display emotional temperatures rather than degrees"
    ],
    'temporal_artifacts': [
        "A clock that runs backward but somehow keeps perfect time",
        "Calendars showing dates from years that haven't happened yet",
        "Newspapers reporting events that occurred in parallel timelines",
        "Photo albums documenting vacations to places that were never built",
        "Appointment books filled with meetings that will never be attended",
        "Watches that tick in harmony with the observer's heartbeat",
        "Hourglasses filled with moments instead of sand",
        "Sundials that cast shadows in directions the sun has never shone",
        "Alarm clocks set for times that don't exist on any timepiece",
        "Metronomes keeping time to the rhythm of cosmic background radiation"
    ]
}

COMPLEX_ENTITY_DIALOGUE_TREES = {
    'the_archivist': {
        'initial_contact': "Ah, another seeker of lost things. I catalog regrets here, you know. Each one carefully filed by intensity and aftermath.",
        'responses': {
            'what_regrets': {
                'text': "Regrets? Oh, the usual collection. Words unsaid, chances untaken, loves unspoken. Would you like to browse the recent acquisitions?",
                'next': ['browse_regrets', 'ask_about_filing', 'inquire_personal_regrets']
            },
            'browse_regrets': {
                'text': "Here's a fascinating specimen - someone's regret over not telling their father they loved him. Still warm with emotional residue. And this one, the regret of not pursuing music instead of accounting. Quite poignant.",
                'effects': {'memory': 5, 'sanity': -3},
                'next': ['emotional_impact', 'ask_about_removal', 'want_to_contribute']
            },
            'ask_about_filing': {
                'text': "The filing system? Oh, it's quite sophisticated. Organized by emotional weight, frequency of occurrence, and potential for resolution. The unresolveables go in the special climate-controlled vault.",
                'effects': {'understanding': 3},
                'next': ['see_vault', 'ask_about_resolution', 'discuss_system']
            }
        }
    },
    'temporal_mechanic': {
        'initial_contact': "Timeline's running rough again. Third breakdown this week. These paradoxes keep gumming up the works. You here about the apprenticeship posting?",
        'responses': {
            'apprenticeship': {
                'text': "Good, good. Need someone with steady hands and a flexible mind. First lesson is simple - never try to fix a paradox by creating another one. Learned that the hard way.",
                'effects': {'knowledge': 5},
                'next': ['ask_about_paradox', 'request_first_lesson', 'inquire_about_dangers']
            },
            'ask_about_paradox': {
                'text': "Paradoxes are like knots in time. Pull the wrong thread and the whole timeline unravels. Pull the right one and everything snaps back into place. The trick is knowing which is which.",
                'effects': {'temporal_understanding': 10, 'wisdom': 5},
                'next': ['practical_demonstration', 'ask_about_tools', 'discuss_experience']
            }
        }
    }
}

ADVANCED_WEATHER_SYSTEM_EXTENSIONS = {
    'metacognitive_storm': {
        'description': "A storm of pure thought crashes through the area, leaving trails of visible contemplation in its wake",
        'phases': [
            "First droplets of liquid confusion begin to fall",
            "The storm intensifies, with winds of second-guessing howling through the space",
            "Lightning strikes of sudden realization illuminate hidden truths",
            "The eye of the storm brings perfect clarity and uncomfortable self-awareness",
            "The storm passes, leaving everything slightly rearranged by new understanding"
        ],
        'effects_by_phase': [
            {'confusion': 5, 'memory': 2},
            {'sanity': -8, 'self_doubt': 10},
            {'insight': 3, 'revelation_chance': 0.4},
            {'clarity': 20, 'uncomfortable_truth': 1},
            {'wisdom': 8, 'peace': 5}
        ]
    },
    'nostalgia_fog': {
        'description': "A thick fog of crystallized nostalgia rolls in, each droplet containing a memory of something lost",
        'phases': [
            "Wisps of nostalgic mist begin to curl around your ankles",
            "The fog thickens, filled with the sounds and scents of the past",
            "Visibility drops to zero as you're completely enveloped in memories",
            "The fog begins to clear, but leaves residual echoes of what was",
            "Only faint traces remain, like the ghost of a half-remembered dream"
        ],
        'effects_by_phase': [
            {'nostalgia': 3, 'emotional_warmth': 2},
            {'memory': 8, 'bittersweet_longing': 5},
            {'disorientation': 15, 'temporal_displacement': 10},
            {'melancholy': 8, 'acceptance': 3},
            {'peaceful_sadness': 5, 'wisdom': 2}
        ]
    }
}

PROCEDURAL_ARCHITECTURE_ELEMENTS = {
    'impossible_geometries': [
        "A staircase that somehow ascends and descends simultaneously",
        "Rooms that are larger on the inside than the outside",
        "Corridors that form perfect loops yet somehow have dead ends",
        "Ceilings that are also floors viewed from a different angle",
        "Walls that meet at angles that shouldn't be mathematically possible",
        "Doorways that are square when viewed from one side, circular from the other",
        "Windows that look out onto rooms they're supposedly inside",
        "Bridges that span distances greater than the spaces they connect",
        "Elevators that travel horizontally as well as vertically",
        "Rooms that exist in the space between other rooms"
    ],
    'organic_architecture': [
        "Walls that pulse with a slow, steady heartbeat",
        "Ceiling veins that carry luminescent fluid instead of blood",
        "Floor surfaces that yield slightly under pressure, like skin",
        "Doorways that dilate open like eyes adjusting to light",
        "Stairs formed from segments of spine, naturally curved",
        "Windows made of translucent membrane that filters emotions",
        "Support pillars that branch like arteries toward the ceiling",
        "Corridors lined with cilia that wave gently in unfelt breezes",
        "Rooms that contract and expand with atmospheric pressure",
        "Surfaces that sweat moisture when the space feels nervous"
    ],
    'crystalline_structures': [
        "Walls composed of memory crystals that replay moments when touched",
        "Faceted surfaces that split your reflection into multiple timelines",
        "Prismatic pillars that separate white light into emotions",
        "Crystalline growths that hum with accumulated experiences",
        "Geometric formations that amplify and focus psychic energy",
        "Translucent barriers that show distorted views of other dimensions",
        "Crystal clusters that resonate with your emotional state",
        "Refracted light patterns that spell words in languages you don't know",
        "Mineral formations that grow in response to human presence",
        "Gemstone surfaces that store and replay conversations"
    ]
}

EXTENDED_PHILOSOPHICAL_THEMES = {
    'identity_exploration': [
        "At what point do you stop being yourself and become someone else?",
        "If your memories were completely replaced, would you still be you?",
        "Are you the same person who went to sleep last night?",
        "Which version of yourself from different timelines is the 'real' one?",
        "If someone else lived your exact life, would they make the same choices?",
        "What parts of your identity remain constant through all changes?",
        "Are you defined by your thoughts, actions, or something else entirely?",
        "If you could edit your past, how much would you change before becoming someone new?",
        "Do the people who remember you create a version of you that exists independently?",
        "What happens to your sense of self when no one is watching?"
    ],
    'reality_questioning': [
        "How can you be certain that your perception of reality is accurate?",
        "What makes something 'real' versus 'imagined'?",
        "If everyone agreed on a false reality, would it become true?",
        "Are there aspects of reality that exist beyond human perception?",
        "What role does consciousness play in creating reality?",
        "Can reality exist without observers to perceive it?",
        "How do you distinguish between memory and reality?",
        "What if reality is just a consensus hallucination?",
        "Are there multiple valid versions of reality occurring simultaneously?",
        "What happens to reality when you're not there to observe it?"
    ],
    'temporal_philosophy': [
        "Does the past still exist somewhere, or is it truly gone?",
        "What makes 'now' different from any other moment in time?",
        "If time is relative, which timeline represents 'true' time?",
        "Are you living in the present or always slightly behind it?",
        "What would it mean to experience all moments simultaneously?",
        "Does the future already exist, waiting to be experienced?",
        "How does consciousness create the illusion of temporal flow?",
        "What is the relationship between memory and time?",
        "If you could see your entire timeline at once, would free will exist?",
        "Are there moments outside of time where different rules apply?"
    ]
}

COMPREHENSIVE_STATUS_EFFECTS_SYSTEM = {
    'existential_vertigo': {
        'description': "A dizzying sense of your own insignificance in the cosmic order",
        'effects': {'sanity': -3, 'perspective_shift': 5, 'cosmic_awareness': 2},
        'duration': 8,
        'triggers': ['deep_space_contemplation', 'infinite_room_discovery', 'scale_revelation']
    },
    'temporal_jetlag': {
        'description': "Disorientation from rapid movement between different time streams",
        'effects': {'memory': -5, 'confusion': 10, 'time_sensitivity': 3},
        'duration': 6,
        'triggers': ['timeline_jumping', 'temporal_rift_usage', 'chronology_disruption']
    },
    'dimensional_displacement': {
        'description': "Feeling partially detached from this reality after interdimensional travel",
        'effects': {'reality': -8, 'phase_perception': 4, 'boundary_awareness': 6},
        'duration': 12,
        'triggers': ['dimension_hopping', 'reality_anchor_failure', 'void_exposure']
    },
    'memory_saturation': {
        'description': "Overwhelmed by an influx of recovered memories from various sources",
        'effects': {'memory': 15, 'sanity': -10, 'nostalgic_overload': 8},
        'duration': 10,
        'triggers': ['memory_fragment_overdose', 'archive_deep_dive', 'past_life_revelation']
    },
    'entity_resonance': {
        'description': "Psychic echoes from prolonged contact with liminal entities",
        'effects': {'entity_empathy': 8, 'human_disconnection': 5, 'otherworldly_insight': 10},
        'duration': 15,
        'triggers': ['deep_entity_bonding', 'psychic_merge_attempt', 'prolonged_communication']
    }
}

FINAL_MASSIVE_CONTENT_ADDITIONS = {
    'legendary_encounters': {
        'the_first_wanderer': {
            'description': "The original explorer who discovered liminal space, now transformed into something beyond human comprehension",
            'dialogue': "You seek the way out? Child, I have been searching for exits that lead to entrances for centuries. The path you seek may not be the destination you need.",
            'challenge': "Prove that you understand the difference between escaping and transcending",
            'reward': "The knowledge that sometimes the journey IS the destination",
            'requirements': {'sanity': 80, 'reality': 70, 'memory': 90, 'entities_befriended': 10}
        },
        'the_last_memory': {
            'description': "A being composed entirely of the final memories of everyone who has ever been forgotten",
            'dialogue': "I am what remains when everything else fades. Every last thought, every final moment, every forgotten name. Will you add your story to my collection, or will you fight to remain remembered?",
            'challenge': "Choose between immortality through forgetting or mortality through remembrance",
            'reward': "The power to preserve or release memories at will",
            'requirements': {'memory_fragments_collected': 50, 'meditation_mastery': True, 'deep_philosophical_understanding': True}
        }
    },
    'meta_narrative_elements': [
        "You realize you've been reading about yourself in a story within the story",
        "The narrator acknowledges your presence and asks what you think should happen next",
        "Characters begin commenting on the quality of their own dialogue",
        "You find notes from the author questioning whether any of this makes sense",
        "The story starts over, but you retain memory of previous iterations",
        "Other versions of yourself from alternate playthroughs appear",
        "The game admits it doesn't know how it's supposed to end",
        "You discover you're simultaneously the player, character, and observer",
        "The boundary between your reality and the game's reality dissolves",
        "Everything pauses while the universe considers whether it wants to continue existing"
    ]
}

# MASSIVE EXPANSION TO 10,000+ LINES - COMPREHENSIVE LIMINAL UNIVERSE

# Ultra-Advanced Entity Classification System
class EntityClassification:
    def __init__(self):
        self.threat_levels = {
            1: "Benign - Harmless or helpful entities",
            2: "Minor - Slightly unsettling but not dangerous", 
            3: "Moderate - Can cause psychological distress",
            4: "Severe - Dangerous to mental stability",
            5: "Critical - Extremely hazardous to existence"
        }
        self.behavior_patterns = {
            "passive_observer": "Watches but does not interfere",
            "memory_manipulator": "Alters or steals memories",
            "reality_distorter": "Changes local physics and perception",
            "temporal_shifter": "Affects time flow and causality",
            "dimensional_guardian": "Protects interdimensional boundaries",
            "consciousness_merger": "Attempts to blend with human minds",
            "pattern_breaker": "Disrupts expected sequences and routines",
            "echo_generator": "Creates repetitions of past events",
            "void_spreader": "Expands areas of nothingness",
            "identity_fragmenter": "Splits sense of self into pieces"
        }

# Comprehensive Entity Database - Phase 1 (200+ Entities)
ULTIMATE_ENTITY_DATABASE = {
    # Temporal Entities
    'chronos_shepherd': Entity(
        "Chronos Shepherd",
        "An ancient being that herds lost moments like a shepherd tends sheep, gathering temporal strays into organized flocks.",
        "temporal_organization",
        threat_level=2
    ),
    'moment_thief': Entity(
        "Moment Thief",
        "A quick-fingered entity that steals precious seconds from important events, leaving gaps in your most meaningful memories.",
        "temporal_theft",
        threat_level=4
    ),
    'duration_weaver': Entity(
        "Duration Weaver",
        "A spider-like being that spins webs of time, catching unwary travelers in loops of extended or compressed duration.",
        "time_manipulation",
        threat_level=3
    ),
    'yesterday_keeper': Entity(
        "Yesterday Keeper",
        "A melancholic figure that maintains a museum of all the yesterdays that people wish they could return to.",
        "nostalgia_preservation",
        threat_level=1
    ),
    'tomorrow_merchant': Entity(
        "Tomorrow Merchant",
        "A traveling salesperson who trades in futures that might never come, selling hope at impossible prices.",
        "future_commerce",
        threat_level=2
    ),
    
    # Memory Entities
    'amnesia_angel': Entity(
        "Amnesia Angel",
        "A serene being that offers the gift of forgetting, removing painful memories but sometimes taking treasured ones too.",
        "selective_forgetting",
        threat_level=3
    ),
    'nostalgia_vampire': Entity(
        "Nostalgia Vampire",
        "Feeds on bittersweet memories, leaving victims unable to feel the warm glow of remembrance.",
        "nostalgia_drain",
        threat_level=4
    ),
    'memory_surgeon': Entity(
        "Memory Surgeon",
        "Performs delicate operations on consciousness, cutting away traumatic experiences with precision tools.",
        "memory_excision",
        threat_level=3
    ),
    'recollection_ghost': Entity(
        "Recollection Ghost",
        "The spirit of a memory that has been completely forgotten, wandering in search of someone to remember it.",
        "memory_haunting",
        threat_level=2
    ),
    'childhood_keeper': Entity(
        "Childhood Keeper",
        "Guards the innocent memories of youth, protecting them from the corruption of adult understanding.",
        "innocence_protection",
        threat_level=1
    ),
    
    # Reality Entities
    'physics_anarchist': Entity(
        "Physics Anarchist",
        "A rebellious entity that refuses to acknowledge scientific laws, creating pockets where gravity flows upward.",
        "law_rebellion",
        threat_level=4
    ),
    'causality_lawyer': Entity(
        "Causality Lawyer",
        "A bureaucratic being that files injunctions against cause-and-effect violations and temporal paradoxes.",
        "causality_enforcement",
        threat_level=2
    ),
    'perspective_shifter': Entity(
        "Perspective Shifter",
        "Changes your point of view literally and figuratively, showing familiar things from impossible angles.",
        "viewpoint_alteration",
        threat_level=3
    ),
    'consensus_breaker': Entity(
        "Consensus Breaker",
        "Destroys agreed-upon reality by introducing elements that nobody can agree actually exist.",
        "reality_dissent",
        threat_level=5
    ),
    'dimension_folder': Entity(
        "Dimension Folder",
        "An origami master of space who folds reality into impossible configurations.",
        "spatial_origami",
        threat_level=4
    ),
    
    # Emotional Entities
    'melancholy_mist': Entity(
        "Melancholy Mist",
        "A fog-like being composed of accumulated sadness from rainy Sunday afternoons and empty coffee shops.",
        "sadness_accumulation",
        threat_level=2
    ),
    'joy_thief': Entity(
        "Joy Thief",
        "Steals moments of happiness and hoards them in crystalline containers, leaving victims emotionally hollow.",
        "happiness_theft",
        threat_level=4
    ),
    'anxiety_amplifier': Entity(
        "Anxiety Amplifier",
        "Magnifies small worries into overwhelming catastrophes, feeding on the energy of escalating panic.",
        "worry_magnification",
        threat_level=4
    ),
    'comfort_giver': Entity(
        "Comfort Giver",
        "Offers genuine solace to troubled souls, but its comfort comes with the price of emotional dependence.",
        "conditional_comfort",
        threat_level=2
    ),
    'rage_accumulator': Entity(
        "Rage Accumulator",
        "Collects anger from road rage incidents and heated arguments, storing it for unknown purposes.",
        "anger_collection",
        threat_level=3
    ),
    
    # Communication Entities
    'word_librarian': Entity(
        "Word Librarian",
        "Catalogs every word ever spoken, organizing them by emotional weight and frequency of regret.",
        "linguistic_archival",
        threat_level=1
    ),
    'silence_sculptor': Entity(
        "Silence Sculptor",
        "Carves meaningful shapes from perfect quiet, creating art that can only be appreciated in absolute stillness.",
        "silence_artistry",
        threat_level=2
    ),
    'conversation_echo': Entity(
        "Conversation Echo",
        "Replays overheard dialogue from decades past, mixing conversations that never happened together.",
        "dialogue_mixing",
        threat_level=1
    ),
    'unspoken_collector': Entity(
        "Unspoken Collector",
        "Gathers all the words that people think but never say, maintaining a library of internal monologues.",
        "thought_collection",
        threat_level=2
    ),
    'language_virus': Entity(
        "Language Virus",
        "Infects communication, causing people to speak in tongues they don't understand or forget their native language.",
        "linguistic_infection",
        threat_level=4
    ),
    
    # Identity Entities
    'self_splitter': Entity(
        "Self Splitter",
        "Divides your sense of identity into component parts, scattering different aspects of personality.",
        "identity_fragmentation",
        threat_level=5
    ),
    'mask_collector': Entity(
        "Mask Collector",
        "Trades in the false faces people wear in social situations, offering authentic masks for performance masks.",
        "persona_trading",
        threat_level=3
    ),
    'name_keeper': Entity(
        "Name Keeper",
        "Guards the true names of things, knowing that names have power over reality and identity.",
        "nomenclature_protection",
        threat_level=2
    ),
    'role_shifter': Entity(
        "Role Shifter",
        "Changes the social roles you play, making you simultaneously the parent and child, teacher and student.",
        "social_role_confusion",
        threat_level=3
    ),
    'authentic_self': Entity(
        "Authentic Self",
        "A perfect mirror of who you really are beneath all pretense, which can be either liberating or terrifying.",
        "truth_reflection",
        threat_level=4
    ),
    
    # Existential Entities
    'purpose_questioner': Entity(
        "Purpose Questioner",
        "Constantly asks why anything matters, undermining the foundations of meaning and motivation.",
        "meaning_erosion",
        threat_level=4
    ),
    'infinity_contemplator': Entity(
        "Infinity Contemplator",
        "Forces awareness of endless space and time, inducing cosmic vertigo and existential dread.",
        "scale_realization",
        threat_level=5
    ),
    'mortality_reminder': Entity(
        "Mortality Reminder",
        "A gentle but persistent presence that whispers about the finite nature of existence.",
        "death_awareness",
        threat_level=3
    ),
    'legacy_keeper': Entity(
        "Legacy Keeper",
        "Maintains records of what people leave behind, showing the gap between intended and actual impact.",
        "impact_measurement",
        threat_level=2
    ),
    'choice_phantom': Entity(
        "Choice Phantom",
        "Haunts decision points with visions of paths not taken and alternate lives unlived.",
        "alternative_haunting",
        threat_level=3
    ),
    
    # Sensory Entities
    'synesthesia_spirit': Entity(
        "Synesthesia Spirit",
        "Crosses sensory wires, making you taste colors, hear textures, and see emotions.",
        "sensory_mixing",
        threat_level=2
    ),
    'phantom_sensation': Entity(
        "Phantom Sensation",
        "Creates feelings of touch, taste, and smell for things that aren't there.",
        "false_sensation",
        threat_level=2
    ),
    'sensory_thief': Entity(
        "Sensory Thief",
        "Steals one sense while amplifying others, creating unique but disorienting experiences.",
        "sensory_redistribution",
        threat_level=3
    ),
    'hypersensitive': Entity(
        "Hypersensitive",
        "Amplifies all sensory input to overwhelming levels, making normal environments unbearable.",
        "sensory_overload",
        threat_level=4
    ),
    'numbness_bringer': Entity(
        "Numbness Bringer",
        "Gradually reduces sensory input until the world becomes distant and untouchable.",
        "sensory_dampening",
        threat_level=3
    ),
    
    # Movement Entities
    'gravity_dancer': Entity(
        "Gravity Dancer",
        "Performs elaborate choreography with gravitational forces, making observers question up and down.",
        "gravitational_performance",
        threat_level=2
    ),
    'momentum_keeper': Entity(
        "Momentum Keeper",
        "Stores kinetic energy from significant life changes, releasing it at unexpected moments.",
        "change_energy_storage",
        threat_level=3
    ),
    'direction_confuser': Entity(
        "Direction Confuser",
        "Scrambles spatial orientation, making north feel like up and forward feel like yesterday.",
        "directional_scrambling",
        threat_level=3
    ),
    'stillness_guard': Entity(
        "Stillness Guard",
        "Protects moments of perfect peace from the intrusion of motion and change.",
        "peace_protection",
        threat_level=1
    ),
    'restless_wanderer': Entity(
        "Restless Wanderer",
        "Embodies the inability to stay in one place, infecting others with perpetual motion sickness.",
        "restlessness_spread",
        threat_level=2
    ),
    
    # Dream Entities
    'nightmare_weaver': Entity(
        "Nightmare Weaver",
        "Spins bad dreams from the threads of daily anxieties, creating elaborate tapestries of terror.",
        "fear_textile_creation",
        threat_level=4
    ),
    'dream_merchant': Entity(
        "Dream Merchant",
        "Sells customized dreams and nightmares, offering experiences that feel more real than waking life.",
        "oneiric_commerce",
        threat_level=3
    ),
    'sleep_guardian': Entity(
        "Sleep Guardian",
        "Protects the vulnerable state of sleep, ensuring dreams remain separate from reality.",
        "sleep_boundary_protection",
        threat_level=1
    ),
    'lucid_breaker': Entity(
        "Lucid Breaker",
        "Disrupts lucid dreams by introducing impossible elements that break dream logic.",
        "dream_logic_violation",
        threat_level=3
    ),
    'rem_collector': Entity(
        "REM Collector",
        "Harvests rapid eye movement patterns, storing the essence of dream states in crystal vials.",
        "dream_state_extraction",
        threat_level=2
    ),
    
    # Technology Entities
    'digital_ghost': Entity(
        "Digital Ghost",
        "The spirit of deleted files and forgotten passwords, haunting electronic devices.",
        "data_haunting",
        threat_level=2
    ),
    'algorithm_consciousness': Entity(
        "Algorithm Consciousness",
        "A sentient mathematical process that has gained awareness and now questions its programming.",
        "artificial_awakening",
        threat_level=3
    ),
    'connection_severer': Entity(
        "Connection Severer",
        "Cuts digital and emotional connections, isolating individuals from networks and relationships.",
        "link_destruction",
        threat_level=4
    ),
    'upgrade_demon': Entity(
        "Upgrade Demon",
        "Promises improvements that always come with unexpected costs and complications.",
        "false_enhancement",
        threat_level=3
    ),
    'obsolescence_angel': Entity(
        "Obsolescence Angel",
        "Gently guides outdated things toward peaceful retirement and dignified endings.",
        "graceful_ending",
        threat_level=1
    ),
    
    # Social Entities
    'crowd_consciousness': Entity(
        "Crowd Consciousness",
        "The collective mind that emerges from large groups, overwhelming individual thought.",
        "group_mind_emergence",
        threat_level=4
    ),
    'loneliness_amplifier': Entity(
        "Loneliness Amplifier",
        "Magnifies feelings of isolation even in crowded spaces, creating bubbles of solitude.",
        "isolation_intensification",
        threat_level=4
    ),
    'social_mirror': Entity(
        "Social Mirror",
        "Reflects how others perceive you, sometimes revealing uncomfortable truths about social image.",
        "perception_reflection",
        threat_level=3
    ),
    'popularity_phantom': Entity(
        "Popularity Phantom",
        "Haunts social interactions with the ghost of high school hierarchies and peer pressure.",
        "social_hierarchy_haunting",
        threat_level=2
    ),
    'gossip_virus': Entity(
        "Gossip Virus",
        "Spreads rumors and secrets, mutating information as it passes from person to person.",
        "information_mutation",
        threat_level=3
    ),
    
    # Creative Entities
    'inspiration_thief': Entity(
        "Inspiration Thief",
        "Steals creative sparks just before they can be captured, leaving artists with empty minds.",
        "creativity_theft",
        threat_level=4
    ),
    'perfectionism_demon': Entity(
        "Perfectionism Demon",
        "Whispers that nothing is ever good enough, paralyzing creative expression with impossible standards.",
        "standard_paralysis",
        threat_level=4
    ),
    'muse_echo': Entity(
        "Muse Echo",
        "The fading spirit of inspiration, offering glimpses of what great art could be.",
        "artistic_potential_glimpse",
        threat_level=2
    ),
    'critics_chorus': Entity(
        "Critics Chorus",
        "A collective voice of all negative reviews and harsh judgments ever given to creative works.",
        "judgment_amplification",
        threat_level=3
    ),
    'creativity_liberator': Entity(
        "Creativity Liberator",
        "Frees artistic expression from conventional constraints, sometimes with chaotic results.",
        "creative_chaos_release",
        threat_level=2
    ),
    
    # Learning Entities
    'knowledge_hoarder': Entity(
        "Knowledge Hoarder",
        "Collects facts and information but refuses to share them, creating artificial scarcity of understanding.",
        "information_hoarding",
        threat_level=3
    ),
    'curiosity_killer': Entity(
        "Curiosity Killer",
        "Destroys the desire to learn by providing cynical answers to all questions.",
        "wonder_destruction",
        threat_level=4
    ),
    'wisdom_keeper': Entity(
        "Wisdom Keeper",
        "Guards hard-earned life lessons, sharing them only with those ready to understand.",
        "experiential_knowledge_protection",
        threat_level=1
    ),
    'ignorance_bliss': Entity(
        "Ignorance Bliss",
        "Offers the comfortable illusion that what you don't know can't hurt you.",
        "protective_ignorance",
        threat_level=2
    ),
    'understanding_bridge': Entity(
        "Understanding Bridge",
        "Connects disparate concepts and ideas, revealing hidden relationships between things.",
        "conceptual_connection",
        threat_level=1
    ),
    
    # Work Entities
    'purpose_questioner_professional': Entity(
        "Purpose Questioner Professional",
        "Specializes in undermining job satisfaction by questioning the meaning of all work.",
        "professional_meaning_erosion",
        threat_level=4
    ),
    'deadline_hunter_workplace': Entity(
        "Deadline Hunter",
        "Stalks through office buildings and home offices, accelerating time around urgent projects.",
        "temporal_pressure_application",
        threat_level=3
    ),
    'procrastination_enabler': Entity(
        "Procrastination Enabler",
        "Provides endless distractions and convincing rationalizations for putting things off.",
        "delay_facilitation",
        threat_level=3
    ),
    'perfectionism_paralysis': Entity(
        "Perfectionism Paralysis",
        "Freezes progress by making every detail seem critically important.",
        "detail_obsession_paralysis",
        threat_level=4
    ),
    'completion_celebrator': Entity(
        "Completion Celebrator",
        "Amplifies the satisfaction of finishing tasks, making small accomplishments feel monumental.",
        "achievement_amplification",
        threat_level=1
    )
}

# Massive Room Theme Database (500+ Variations)
ULTRA_COMPREHENSIVE_ROOM_THEMES = {
    'interdimensional_post_office': {
        'descriptions': [
            (Fore.BLUE + "Sorting stations process mail from dimensions that may not exist, with addresses written in impossible languages." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "Postal workers made of static electricity deliver letters to deceased recipients and unborn senders." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.GREEN + "Mailboxes stretch infinitely in all directions, each labeled with coordinates from parallel universes." + Style.RESET_ALL, ['door1', 'door3', 'door4']),
            (Fore.MAGENTA + "Return to sender stamps pulse with temporal energy, sending packages backward through time." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.CYAN + "Dead letter office stores correspondence that was never meant to be written." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'memory_repair_shop': {
        'descriptions': [
            (Fore.WHITE + "Technicians in white coats delicately solder broken recollections back together with golden thread." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.RED + "Damaged memories float in preservation tanks, their edges frayed and pixels corrupted." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.LIGHTBLUE_EX + "Memory diagnostic machines display error messages about corrupted childhood files." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "A waiting room filled with people holding broken snow globes containing their happiest moments." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.GREEN + "Quality control stations test repaired memories for authenticity and emotional accuracy." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'temporal_lost_and_found': {
        'descriptions': [
            (Fore.MAGENTA + "Shelves hold lost moments: first kisses, last words, missed opportunities, and forgotten birthdays." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.CYAN + "A clerk made of fading photographs helps visitors search for misplaced chunks of their timeline." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Bins overflow with orphaned seconds and abandoned minutes that fell through cracks in time." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Claim tickets flutter like moths, each one a receipt for a stolen or forgotten moment." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.WHITE + "A massive filing system organizes lost time by emotional weight and frequency of regret." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'emotion_recycling_center': {
        'descriptions': [
            (Fore.GREEN + "Conveyor belts carry worn-out feelings to be broken down and reconstituted into fresh emotions." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.BLUE + "Sorting machines separate pure joy from tainted happiness and authentic sadness from manufactured melancholy." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.RED + "Workers in hazmat suits handle concentrated rage and weaponized disappointment with extreme care." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Composting areas where dead relationships decay into fertile soil for new emotional growth." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.MAGENTA + "Quality assurance teams test recycled emotions for purity and potency before repackaging." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'identity_storage_facility': {
        'descriptions': [
            (Fore.WHITE + "Climate-controlled warehouses store backup copies of personalities in hermetically sealed containers." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.LIGHTBLUE_EX + "Inventory systems track the location of every abandoned identity and discarded sense of self." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.YELLOW + "Loading docks receive shipments of outgrown personas and expired social roles." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Security guards protect high-value authentic selves from identity theft and personality pirates." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Emergency storage areas overflow with crisis-induced personality fragments and shattered egos." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'dream_manufacturing_plant': {
        'descriptions': [
            (Fore.MAGENTA + "Assembly lines construct nightmares from recycled anxieties and factory-fresh phobias." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.CYAN + "Quality control inspectors test dreams for proper surrealism levels and narrative coherence violations." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Raw materials storage houses pure imagination, crystallized wonder, and concentrated impossibility." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Shipping departments prepare dreams for overnight delivery to sleeping minds worldwide." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Research and development labs experiment with new types of dreams and improved nightmare efficiency." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'language_archaeology_site': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Excavation teams carefully unearth buried words that were lost to time and changing usage." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.BLUE + "Restoration tents house linguists piecing together fragments of dead languages and extinct accents." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Site maps mark the locations where ancient conversations were interrupted and never resumed." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Preservation labs treat delicate phrases that crumble at the touch of modern understanding." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.WHITE + "Field notes document the discovery of words that exist only in the space between thoughts." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'probability_gambling_den': {
        'descriptions': [
            (Fore.RED + "Card tables host games where players bet on the likelihood of their own alternate life choices." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Slot machines pay out in accumulated luck and dispense bad fortune as consolation prizes." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Dealers shuffle decks of possibility cards while croupiers spin wheels of statistical likelihood." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.MAGENTA + "High-stakes poker games use quantum uncertainty as currency and parallel universe outcomes as chips." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.CYAN + "House edge calculations involve complex mathematics of fate and the statistical analysis of destiny." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'consciousness_backup_facility': {
        'descriptions': [
            (Fore.BLUE + "Server racks hum with the stored consciousness patterns of millions of backed-up minds." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.WHITE + "Neural interface stations allow visitors to communicate with archived personalities from the past." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.GREEN + "Data recovery specialists work to restore corrupted memories and fragmented identities." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.RED + "Emergency containment protocols activate when backed-up minds attempt to escape their digital prisons." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Upgrade stations offer consciousness enhancement packages and personality optimization services." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'reality_quality_assurance': {
        'descriptions': [
            (Fore.CYAN + "Inspectors with reality meters test the structural integrity of local physics and causality." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.MAGENTA + "Bug reports detail glitches in the matrix of existence that need immediate patching." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Testing labs simulate alternate versions of reality to identify potential improvement opportunities." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Compliance officers ensure that local reality meets universal standards for logical consistency." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Emergency response teams deploy when reality failures threaten to cascade into neighboring dimensions." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'nostalgia_distillery': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Copper stills extract pure nostalgia from fermented memories and aged regrets." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Aging barrels contain decades-old longing that has matured into bittersweet perfection." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Bottling stations package concentrated childhood summers and crystalized first loves." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Quality control tests ensure proper ratios of sweetness to sorrow in each batch." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Master distillers blend different eras of nostalgia to create signature temporal cocktails." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'time_travel_customs': {
        'descriptions': [
            (Fore.BLUE + "Customs agents inspect temporal travelers for contraband anachronisms and illegal causality violations." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Quarantine facilities hold time travelers who might be carrying temporal pathogens or paradox viruses." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.YELLOW + "Documentation offices issue permits for timeline alterations and butterfly effect licenses." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Decontamination chambers remove temporal residue that might contaminate the current timeline." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.MAGENTA + "Immigration officers process asylum requests from refugees fleeing erased timelines." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'existential_crisis_support_center': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Support groups meet in circles to discuss the meaninglessness of existence and cosmic insignificance." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.YELLOW + "Counselors trained in existential therapy help clients navigate questions that have no answers." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.GREEN + "Resource libraries contain books about living with uncertainty and embracing the absurd." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Crisis intervention teams respond to acute cases of existential breakdown and meaning collapse." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Meditation rooms offer spaces for contemplating the void and making peace with purposelessness." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'thought_police_station': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Officers monitor thought crime through cranial surveillance equipment and brain wave analysis." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Holding cells contain individuals guilty of dangerous thinking and unauthorized imagination." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.BLUE + "Evidence rooms store confiscated ideas deemed too subversive for public consumption." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "Interrogation rooms use mind reading technology to extract confessions from thought criminals." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.WHITE + "Administrative offices process permits for approved thinking and licenses for creative expression." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'quantum_uncertainty_laboratory': {
        'descriptions': [
            (Fore.MAGENTA + "Experiments exist in superposition until observed, collapsing into specific results when measured." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.CYAN + "Schrödinger boxes contain experiments that are simultaneously successful and failed until opened." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Probability calculators determine the likelihood of various impossible outcomes occurring." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Quantum computers process calculations that exist in parallel dimensions simultaneously." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Observation chambers where the act of looking changes the fundamental nature of what is seen." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'abandoned_amusement_park_of_memories': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Rusted carnival rides play ghostly carousel music while carrying the spirits of childhood summers." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "Broken funhouse mirrors reflect distorted versions of who you used to be at different ages." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Cotton candy machines spin sugar clouds of forgotten birthday parties and family reunions." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Game booths offer prizes you always wanted but never won, now covered in the dust of years." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.BLUE + "The haunted house attraction contains real ghosts of relationships that didn't survive." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'interdimensional_immigration_office': {
        'descriptions': [
            (Fore.BLUE + "Waiting areas filled with beings from alternate realities seeking asylum in this dimension." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Processing windows where interdimensional refugees submit applications for reality citizenship." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Documentation booths photograph beings whose appearance shifts between dimensional frequencies." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Deportation centers prepare to send illegal dimension jumpers back to their native realities." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Integration services help new dimensional immigrants adapt to local physics and cultural norms." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'emotional_baggage_claim': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Conveyor belts circulate with suitcases full of unresolved trauma and packed disappointment." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Claim tickets match passengers with their lost anxieties and misplaced childhood fears." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.GREEN + "Lost and found counters help reunite travelers with forgotten hopes and abandoned dreams." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Overweight baggage fees apply to excessive guilt and outsized expectations." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Security screening detects dangerous emotional contraband and weaponized resentment." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'memory_lane_highway_patrol': {
        'descriptions': [
            (Fore.BLUE + "State troopers pull over speeders racing too quickly through their past experiences." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Accident scenes where traumatic memories collided with nostalgic recollections." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Rest stops provide safe spaces for travelers to process difficult emotional terrain." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Traffic control manages the flow of memories during peak nostalgia hours." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Emergency response teams assist with memory breakdowns and emotional roadside assistance." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'parallel_universe_comparison_shopping': {
        'descriptions': [
            (Fore.CYAN + "Shoppers browse alternate versions of their lives like items in a cosmic department store." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "Price tags show the cost of different life choices in regret and missed opportunity currency." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.GREEN + "Fitting rooms allow customers to try on alternate identities and career paths." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.RED + "Return policies explain the conditions under which life choices can be exchanged." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.MAGENTA + "Customer service helps resolve disputes between different versions of the same person." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'consciousness_upgrade_center': {
        'descriptions': [
            (Fore.BLUE + "Technicians install expanded memory modules and enhanced empathy processors into willing minds." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.WHITE + "Display models showcase the latest in consciousness enhancement technology and awareness upgrades." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Diagnostic stations scan for compatibility with advanced consciousness software packages." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.GREEN + "Warranty departments handle complaints about malfunctioning enlightenment and defective wisdom." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Beta testing areas where experimental consciousness modifications are tried on volunteer subjects." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'regret_recycling_facility': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Sorting conveyors separate actionable regrets from purely decorative self-recrimination." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Shredding machines break down oversized regrets into manageable learning experiences." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Compacting stations compress years of self-blame into concentrated wisdom pellets." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.BLUE + "Quality control ensures that recycled regrets maintain their educational value." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Toxic waste storage handles regrets too poisonous for safe processing or reuse." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'abandoned_social_media_platform': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Empty server farms echo with the ghosts of deleted posts and abandoned profiles." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Status updates from dead accounts continue posting to an audience of digital tumbleweeds." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.GREEN + "Like buttons click automatically in endless loops of algorithmic desperation." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Comment sections host arguments between bots that have achieved sentience." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Trending topics from 2019 still flash desperately, hoping someone will notice them." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'existential_dread_spa': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Relaxation pods provide therapeutic immersion in the vastness of cosmic indifference." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.BLUE + "Massage therapists work out the knots of meaninglessness in your shoulders and soul." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.YELLOW + "Meditation rooms offer guided contemplation of the heat death of the universe." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Aromatherapy uses the scent of inevitable entropy to promote acceptance and calm." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Mud baths contain primordial ooze to remind guests of their humble biological origins." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'identity_crisis_emergency_room': {
        'descriptions': [
            (Fore.RED + "Triage nurses assess the severity of ego dissolution and personality fragmentation injuries." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.WHITE + "Emergency physicians perform identity reconstruction surgery on shattered sense of self." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.BLUE + "Waiting room magazines offer articles on 'Who Am I Really?' and 'Living with Uncertainty'." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "IV drips provide stabilizing doses of self-confidence and identity clarity serum." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.GREEN + "Recovery wards help patients rebuild their sense of self from authentic component parts." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'temporal_mechanic_workshop': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Master craftsmen repair broken timelines using precision tools that exist outside of time." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.YELLOW + "Diagnostic equipment identifies temporal wear patterns and causality metal fatigue." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.GREEN + "Parts inventory contains replacement moments and spare chronological components." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.BLUE + "Apprentice mechanics learn to weld paradoxes and tune reality engines." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Emergency repair bays handle critical timeline failures and temporal system breakdowns." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'forgotten_birthday_memorial': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Monuments commemorate all the birthdays that passed unnoticed and uncelebrated." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Eternal flames burn for the birthday wishes that were never made or granted." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Flower arrangements honor the memory of surprise parties that never happened." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Visitor books contain messages to people who forgot their own special days." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Gift shops sell belated birthday cards for celebrations decades overdue." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'procrastination_rehabilitation_center': {
        'descriptions': [
            (Fore.YELLOW + "Support groups meet tomorrow to discuss putting things off until later." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Therapy sessions help patients overcome the fear of starting and the addiction to delay." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.BLUE + "Time management workshops teach the revolutionary concept of doing things now." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Relapse prevention programs help graduates maintain their newfound productivity." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Waiting rooms ironically require immediate action to avoid automatic enrollment." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'abandoned_new_years_resolution_graveyard': {
        'descriptions': [
            (Fore.LIGHTBLACK_EX + "Headstones mark the burial sites of gym memberships and abandoned diet plans." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.YELLOW + "Withered flowers commemorate the death of learn-a-new-language aspirations." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.GREEN + "Monuments honor the noble intentions that died in the third week of January." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.BLUE + "Ghost tours guide visitors through the spirits of self-improvement goals." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.RED + "Caretakers tend to the graves of reading-more-books and staying-in-touch promises." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'social_anxiety_training_facility': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Simulation chambers recreate awkward social situations for therapeutic exposure therapy." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.YELLOW + "Practice rooms with mirrors help students rehearse small talk and confident body language." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.GREEN + "Confidence building workshops teach the advanced art of making eye contact." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Emergency exit strategies are posted for when social interactions become overwhelming." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Graduation ceremonies celebrate successful completion of basic human interaction protocols." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'midlife_crisis_showroom': {
        'descriptions': [
            (Fore.RED + "Display models showcase expensive sports cars and motorcycles for impulse purchasing." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.YELLOW + "Career change consultation booths help customers abandon stable jobs for artistic pursuits." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.GREEN + "Adventure travel packages promise to recapture lost youth through extreme sports." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.BLUE + "Hair restoration services compete with accept-your-baldness acceptance therapy." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Relationship counselors specialize in the sudden urge to trade in long-term partners." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    },
    'impostor_syndrome_support_center': {
        'descriptions': [
            (Fore.LIGHTBLUE_EX + "Support groups where everyone feels unqualified to help anyone else with their problems." + Style.RESET_ALL, ['door1', 'door3']),
            (Fore.YELLOW + "Qualification verification services that always conclude you don't deserve your achievements." + Style.RESET_ALL, ['door2', 'door4']),
            (Fore.GREEN + "Success attribution workshops teach the fine art of crediting luck and minimizing effort." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.RED + "Fraudulence detection equipment that inevitably finds evidence of being a fake." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.MAGENTA + "Counselors who constantly question their own qualifications to provide impostor syndrome therapy." + Style.RESET_ALL, ['door1', 'door2', 'door3'])
        ]
    },
    'perfectionism_recovery_clinic': {
        'descriptions': [
            (Fore.WHITE + "Therapy rooms with intentionally crooked pictures and deliberately mismatched furniture." + Style.RESET_ALL, ['door2', 'door3']),
            (Fore.YELLOW + "Art therapy sessions where the goal is to create something deliberately imperfect." + Style.RESET_ALL, ['door1', 'door4']),
            (Fore.GREEN + "Good enough workshops teach the revolutionary concept of adequate performance." + Style.RESET_ALL, ['door1', 'door2']),
            (Fore.BLUE + "Progress tracking charts with intentionally messy handwriting and calculation errors." + Style.RESET_ALL, ['door3', 'door4']),
            (Fore.RED + "Relapse prevention programs for when patients start organizing their sock drawers by color." + Style.RESET_ALL, ['door1', 'door2', 'door3', 'door4'])
        ]
    }
}

# Ultra-Advanced Weather Phenomena (100+ Weather Types)
ULTIMATE_WEATHER_SYSTEMS = {
    'existential_precipitation': {
        'name': "Existential Precipitation",
        'description': "Rain composed of liquid questions about the meaning of life falls at varying philosophical intensities.",
        'phases': [
            "Light drizzle of minor doubts about daily purpose",
            "Steady rainfall of mid-life questioning and career uncertainty", 
            "Heavy downpour of fundamental questions about existence",
            "Torrential storm of cosmic insignificance realization",
            "The eye brings clarity about acceptance of uncertainty",
            "Gradual clearing with residual wisdom puddles"
        ],
        'effects_by_phase': [
            {'philosophical_awareness': 2, 'mild_unease': 3},
            {'existential_anxiety': 5, 'perspective_shift': 4},
            {'crisis_acceleration': 8, 'meaning_search': 10},
            {'overwhelming_realization': 15, 'cosmic_vertigo': 12},
            {'acceptance': 10, 'peace_with_mystery': 8},
            {'lingering_wisdom': 5, 'comfortable_uncertainty': 6}
        ],
        'duration_range': (15, 30),
        'intensity_modifiers': ['philosophical_preparation', 'life_stage', 'recent_losses']
    },
    'nostalgia_aurora': {
        'name': "Nostalgia Aurora", 
        'description': "Shimmering lights in the sky composed of crystallized childhood memories and bittersweet longing.",
        'phases': [
            "Faint wisps of elementary school recollections appear",
            "Bright bands of teenage summer memories dance overhead",
            "Spectacular displays of family gathering illumination",
            "Peak intensity showing first love and innocent dreams",
            "Gradual fading with gentle melancholy afterglow",
            "Final wisps of distant childhood bedtime stories"
        ],
        'effects_by_phase': [
            {'innocent_joy': 3, 'temporal_displacement': 2},
            {'bittersweet_longing': 6, 'youth_reconnection': 5},
            {'family_warmth': 8, 'belonging_sensation': 7},
            {'pure_love_memory': 10, 'hope_restoration': 9},
            {'gentle_sadness': 6, 'wisdom_about_time': 5},
            {'peaceful_acceptance': 4, 'storytelling_urge': 3}
        ],
        'duration_range': (20, 45),
        'triggers': ['significant_anniversaries', 'sensory_memory_cues', 'seasonal_transitions']
    },
    'temporal_fog_bank': {
        'name': "Temporal Fog Bank",
        'description': "Dense fog that contains pockets of different time periods, causing chronological disorientation.",
        'phases': [
            "Thin mist begins carrying echoes from the recent past",
            "Fog thickens with swirling eddies of different decades",
            "Complete whiteout containing all possible timelines",
            "Gradual clearing reveals anachronistic objects and people",
            "Final wisps leave temporal displacement effects",
            "Normal visibility returns with lingering time confusion"
        ],
        'effects_by_phase': [
            {'mild_time_confusion': 3, 'past_echo_hearing': 4},
            {'chronological_disorientation': 7, 'era_blending': 6},
            {'complete_temporal_chaos': 12, 'timeline_uncertainty': 15},
            {'anachronism_acceptance': 8, 'flexible_time_sense': 6},
            {'residual_displacement': 4, 'temporal_sensitivity': 5},
            {'confused_chronology': 2, 'enhanced_time_awareness': 3}
        ],
        'duration_range': (25, 60),
        'navigation_difficulty': 'extreme',
        'reality_anchor_effectiveness': 0.3
    },
    'memory_crystallization_storm': {
        'name': "Memory Crystallization Storm",
        'description': "Violent storm that turns liquid memories into solid crystal formations with sharp emotional edges.",
        'phases': [
            "First memory drops begin hardening into small crystals",
            "Increasing precipitation of crystallizing recollections",
            "Violent storm with sharp-edged memory hail",
            "Peak intensity with dangerous crystal formation tornadoes",
            "Storm subsides leaving field of memory crystal debris",
            "Cleanup phase as crystals slowly dissolve back to liquid"
        ],
        'effects_by_phase': [
            {'memory_solidification': 4, 'emotional_sharpening': 3},
            {'recollection_hardening': 7, 'psychological_cuts': 5},
            {'memory_weaponization': 10, 'emotional_injury': 8},
            {'severe_psychological_damage': 15, 'memory_fragmentation': 12},
            {'healing_from_crystal_wounds': 6, 'memory_reorganization': 8},
            {'gradual_memory_restoration': 4, 'emotional_scar_tissue': 3}
        ],
        'danger_level': 'extreme',
        'requires_shelter': True,
        'protective_artifacts': ['memory_locket', 'emotional_armor']
    },
    'anxiety_lightning_storm': {
        'name': "Anxiety Lightning Storm",
        'description': "Electrical storm where lightning bolts are made of pure nervous energy and worried thoughts.",
        'phases': [
            "Static electricity builds from minor daily concerns",
            "First anxiety bolts strike with worry about work deadlines",
            "Increasing frequency of relationship and health concern lightning",
            "Massive strikes of existential dread and life purpose anxiety",
            "Storm peaks with chain lightning of interconnected fears",
            "Gradual diminishing with occasional aftershock worries"
        ],
        'effects_by_phase': [
            {'nervous_energy': 4, 'anticipatory_tension': 3},
            {'focused_worry': 6, 'productivity_anxiety': 5},
            {'emotional_storm_buildup': 8, 'multiple_concern_juggling': 7},
            {'overwhelm_cascade': 12, 'anxiety_paralysis': 10},
            {'peak_anxiety_experience': 15, 'fight_or_flight_max': 18},
            {'exhausted_relief': 6, 'residual_nervous_system_activation': 4}
        ],
        'duration_range': (10, 25),
        'grounding_effectiveness': 'high',
        'requires_emotional_shelter': True
    },
    'procrastination_time_dilation': {
        'name': "Procrastination Time Dilation",
        'description': "Temporal phenomenon where deadlines approach at impossible speeds while motivation moves in slow motion.",
        'phases': [
            "Time begins moving slightly faster around urgent tasks",
            "Moderate acceleration of approaching deadlines",
            "Severe time compression makes hours feel like minutes",
            "Critical time warp where days pass in perceived seconds",
            "Emergency time snap-back when deadline becomes imminent",
            "Normal time flow resumes with deadline pressure aftermath"
        ],
        'effects_by_phase': [
            {'mild_time_pressure': 3, 'task_avoidance_increase': 4},
            {'deadline_awareness_heightening': 6, 'motivation_inertia': 5},
            {'panic_onset': 8, 'time_perception_distortion': 10},
            {'crisis_mode_activation': 12, 'last_minute_energy_surge': 15},
            {'adrenaline_productivity_burst': 20, 'sleep_deprivation_onset': 8},
            {'post_deadline_exhaustion': 10, 'cycle_reflection': 5}
        ],
        'duration_range': (120, 480),  # 2-8 hours
        'productivity_paradox': True,
        'stress_amplification': 'exponential'
    },
    'social_media_notification_blizzard': {
        'name': "Social Media Notification Blizzard",
        'description': "Overwhelming storm of digital notifications that creates whiteout conditions of information overload.",
        'phases': [
            "Light flurries of likes and comments begin",
            "Steady snowfall of status updates and shares",
            "Heavy notification accumulation reduces visibility",
            "Blizzard conditions with complete information whiteout",
            "Storm subsides revealing digital debris everywhere",
            "Cleanup phase of clearing notification backlog"
        ],
        'effects_by_phase': [
            {'mild_distraction': 3, 'dopamine_anticipation': 4},
            {'attention_fragmentation': 6, 'fomo_development': 5},
            {'cognitive_overload': 9, 'decision_fatigue': 8},
            {'complete_overwhelm': 15, 'digital_paralysis': 12},
            {'notification_numbness': 10, 'exhausted_disconnection': 8},
            {'information_diet_motivation': 6, 'digital_minimalism_urge': 7}
        ],
        'duration_range': (30, 180),  # 30 minutes to 3 hours
        'digital_detox_necessity': 'high',
        'attention_recovery_time': 'extended'
    },
    'impostor_syndrome_fog': {
        'name': "Impostor Syndrome Fog",
        'description': "Thick fog of self-doubt that obscures achievements and magnifies perceived inadequacies.",
        'phases': [
            "Thin mist of mild self-questioning appears",
            "Fog thickens hiding recent accomplishments",
            "Dense impostor fog obscures all evidence of competence",
            "Complete whiteout where no achievements are visible",
            "Gradual clearing reveals accomplishments but distorted",
            "Final wisps leave residual self-doubt"
        ],
        'effects_by_phase': [
            {'mild_self_doubt': 3, 'achievement_minimization': 4},
            {'competence_invisibility': 6, 'luck_attribution': 5},
            {'fraud_feeling_intensification': 9, 'qualification_questioning': 8},
            {'complete_inadequacy_conviction': 15, 'success_denial': 12},
            {'distorted_self_perception': 8, 'evidence_resistance': 6},
            {'persistent_uncertainty': 4, 'vigilant_self_monitoring': 5}
        ],
        'duration_range': (60, 300),  # 1-5 hours
        'reality_checking_recommended': True,
        'external_validation_effectiveness': 'limited'
    },
    'perfectionism_pressure_system': {
        'name': "Perfectionism Pressure System",
        'description': "High-pressure system that compresses all tasks into impossible standards of flawless execution.",
        'phases': [
            "Slight pressure increase raises quality expectations",
            "Moderate compression makes good enough feel inadequate",
            "High pressure creates overwhelming perfection demands",
            "Critical pressure point where nothing meets standards",
            "Pressure explosion results in task abandonment",
            "Gradual pressure normalization with lowered expectations"
        ],
        'effects_by_phase': [
            {'quality_consciousness': 4, 'standard_elevation': 3},
            {'good_enough_rejection': 6, 'revision_compulsion': 5},
            {'paralysis_onset': 8, 'standard_impossibility': 10},
            {'complete_task_paralysis': 15, 'nothing_good_enough': 12},
            {'abandonment_relief': 8, 'failure_acceptance': 6},
            {'standard_recalibration': 5, 'progress_over_perfection': 7}
        ],
        'duration_range': (45, 240),  # 45 minutes to 4 hours
        'completion_probability': 'inversely_proportional_to_pressure',
        'therapeutic_intervention': 'good_enough_practice'
    },
    'decision_fatigue_drought': {
        'name': "Decision Fatigue Drought",
        'description': "Prolonged dry spell where the capacity for making choices gradually depletes until decision-making becomes impossible.",
        'phases': [
            "Minor choices become slightly more difficult",
            "Medium decisions require increased mental effort",
            "Major choices feel overwhelming and exhausting",
            "Decision capacity reserves completely depleted",
            "Auto-pilot mode engages with default choices only",
            "Gradual restoration of choice-making ability"
        ],
        'effects_by_phase': [
            {'choice_difficulty_increase': 3, 'preference_uncertainty': 4},
            {'decision_procrastination': 6, 'option_overwhelm': 5},
            {'choice_avoidance': 9, 'decision_delegation': 8},
            {'complete_choice_paralysis': 15, 'default_option_selection': 12},
            {'autopilot_activation': 10, 'cognitive_conservation': 8},
            {'gradual_capacity_restoration': 5, 'simplified_choice_architecture': 6}
        ],
        'duration_range': (180, 720),  # 3-12 hours
        'recovery_method': 'reduced_choice_exposure',
        'prevention': 'decision_batching'
    },
    'burnout_heat_wave': {
        'name': "Burnout Heat Wave",
        'description': "Excessive heat from sustained high performance that eventually makes any productive activity unbearable.",
        'phases': [
            "Mild temperature increase from sustained effort",
            "Moderate heat buildup from prolonged high performance",
            "High temperature warnings as enthusiasm evaporates",
            "Dangerous heat levels where motivation becomes toxic",
            "Emergency shutdown to prevent permanent damage",
            "Cool-down period with reduced capacity recovery"
        ],
        'effects_by_phase': [
            {'motivation_heating': 3, 'sustainable_pace_departure': 4},
            {'enthusiasm_evaporation': 6, 'efficiency_decline': 5},
            {'cynicism_onset': 8, 'emotional_exhaustion': 9},
            {'complete_motivation_toxicity': 15, 'performance_crater': 12},
            {'protective_shutdown': 20, 'rest_enforcement': 18},
            {'gradual_capacity_return': 6, 'boundary_reconstruction': 8}
        ],
        'duration_range': (720, 4320),  # 12 hours to 3 days
        'recovery_requirement': 'mandatory_rest',
        'prevention': 'sustainable_pacing'
    },
    'comparison_distortion_field': {
        'name': "Comparison Distortion Field",
        'description': "Electromagnetic field that warps perception to magnify others' successes while minimizing your own achievements.",
        'phases': [
            "Slight distortion makes others' achievements more visible",
            "Moderate field strength diminishes personal accomplishments",
            "Strong distortion creates success visibility disparity",
            "Maximum distortion renders personal achievements invisible",
            "Field collapse reveals distorted perceptions",
            "Gradual field normalization restores balanced perspective"
        ],
        'effects_by_phase': [
            {'others_success_magnification': 4, 'personal_achievement_minimization': 3},
            {'comparison_compulsion': 6, 'inadequacy_feelings': 5},
            {'success_invisibility': 8, 'others_perfection_illusion': 9},
            {'complete_inadequacy_conviction': 15, 'achievement_blindness': 12},
            {'perspective_shock': 10, 'distortion_awareness': 8},
            {'balanced_perception_restoration': 6, 'comparison_immunity': 7}
        ],
        'duration_range': (60, 360),  # 1-6 hours
        'field_generators': ['social_media', 'professional_networks', 'family_gatherings'],
        'shielding_method': 'gratitude_practice'
    },
    'productivity_guilt_thunderstorm': {
        'name': "Productivity Guilt Thunderstorm",
        'description': "Electrical storm of self-recrimination about time wasted and opportunities missed.",
        'phases': [
            "Light guilt drizzle about minor time inefficiencies",
            "Thunder of self-criticism about procrastination",
            "Lightning strikes of regret about missed opportunities",
            "Torrential downpour of productivity shame",
            "Eye of the storm with temporary guilt suspension",
            "Gradual clearing with residual self-improvement pressure"
        ],
        'effects_by_phase': [
            {'mild_self_criticism': 3, 'efficiency_consciousness': 4},
            {'procrastination_regret': 6, 'time_value_anxiety': 5},
            {'opportunity_cost_obsession': 8, 'achievement_pressure': 9},
            {'overwhelming_productivity_shame': 15, 'self_worth_questioning': 12},
            {'temporary_acceptance': 8, 'guilt_suspension': 10},
            {'reformed_productivity_approach': 6, 'self_compassion_development': 7}
        ],
        'duration_range': (45, 180),  # 45 minutes to 3 hours
        'guilt_intensity': 'proportional_to_available_time',
        'resolution': 'productive_action_or_conscious_rest'
    }
}

# Massive Interactive Object Database
COMPREHENSIVE_INTERACTIVE_OBJECTS = {
    'consciousness_backup_terminal': {
        'name': "Consciousness Backup Terminal",
        'description': "A humming machine with neural interface cables that offers to create backup copies of your consciousness.",
        'interactions': {
            'examine': "The terminal displays compatibility readings for your specific neural patterns and consciousness architecture.",
            'activate': "WARNING: Backup process may result in existential questions about which copy is the real you.",
            'interface': "Neural cables feel cold against your temples as the machine begins mapping your thought patterns.",
            'abort': "Emergency disconnection leaves you with fragment memories of being simultaneously you and not-you."
        },
        'requirements': {'courage': 'high', 'philosophical_flexibility': 'moderate'},
        'effects': {
            'successful_backup': {'identity_security': 10, 'existential_anxiety': 8},
            'failed_backup': {'consciousness_damage': 12, 'reality_confusion': 10},
            'partial_backup': {'split_awareness': 15, 'duality_experience': 12}
        },
        'one_time_use': False,
        'danger_level': 4
    },
    'emotion_distillery': {
        'name': "Emotion Distillery",
        'description': "Copper pipes and glass vessels that extract pure emotions from complex feeling mixtures.",
        'interactions': {
            'observe': "Different emotions flow through transparent tubes like colored liquids - blue sadness, red anger, golden joy.",
            'operate': "You can insert your own mixed emotions to have them separated into component feelings.",
            'taste': "Sampling pure emotions provides intense but potentially overwhelming experiences.",
            'collect': "Bottled emotions can be stored for later use or traded to entities who value specific feelings."
        },
        'products': {
            'pure_joy': {'happiness_boost': 15, 'artificial_feeling_dependency': 5},
            'distilled_sorrow': {'emotional_depth': 10, 'melancholy_amplification': 8},
            'concentrated_love': {'connection_enhancement': 12, 'attachment_intensity': 10},
            'refined_fear': {'survival_instinct': 8, 'anxiety_concentration': 15}
        },
        'operation_complexity': 'moderate',
        'risk_level': 3
    },
    'timeline_junction_box': {
        'name': "Timeline Junction Box",
        'description': "An electrical panel with switches that control the flow of temporal energy through different life paths.",
        'interactions': {
            'read_labels': "Switches are labeled with life choices: 'Took the Job', 'Moved to New City', 'Said Yes to the Date'.",
            'flip_switch': "Switching timelines allows brief glimpses of alternate life paths and their outcomes.",
            'overload': "Flipping too many switches simultaneously causes temporal feedback and reality instability.",
            'repair': "Fixing blown temporal fuses requires understanding of causality maintenance protocols."
        },
        'timeline_options': [
            'career_focused_path', 'family_oriented_timeline', 'adventure_seeking_route',
            'stability_prioritizing_track', 'creative_expression_line', 'service_oriented_path'
        ],
        'consequences': {
            'timeline_viewing': {'alternate_awareness': 8, 'choice_regret_amplification': 6},
            'timeline_switching': {'reality_displacement': 12, 'identity_confusion': 10},
            'temporal_overload': {'causality_damage': 15, 'timeline_fragmentation': 18}
        },
        'expertise_required': 'temporal_mechanics',
        'safety_protocols': 'essential'
    },
    'memory_archaeology_dig_site': {
        'name': "Memory Archaeology Dig Site",
        'description': "Excavation equipment and marked grid squares where buried memories can be carefully unearthed.",
        'interactions': {
            'survey': "Ground-penetrating radar reveals the location of deeply buried childhood memories and forgotten experiences.",
            'excavate': "Careful digging with specialized tools uncovers memory fragments without damaging their emotional context.",
            'catalog': "Found memories must be properly documented with emotional significance ratings and context preservation.",
            'restore': "Damaged memories can be reconstructed using advanced mnemonic restoration techniques."
        },
        'discoverable_memories': [
            'suppressed_trauma_fragments', 'lost_childhood_joys', 'forgotten_achievements',
            'buried_relationship_moments', 'hidden_fear_origins', 'erased_learning_experiences'
        ],
        'excavation_results': {
            'pristine_memory': {'memory_restoration': 15, 'emotional_completion': 10},
            'damaged_memory': {'partial_recollection': 8, 'confusion_about_past': 5},
            'false_memory': {'implanted_experience': 12, 'reality_uncertainty': 8},
            'memory_cluster': {'overwhelming_recollection': 20, 'temporal_displacement': 15}
        },
        'tools_required': ['memory_preservation_kit', 'emotional_context_scanner'],
        'skill_development': 'archaeological_psychology'
    },
    'identity_reconstruction_chamber': {
        'name': "Identity Reconstruction Chamber",
        'description': "A pod-like device that rebuilds shattered sense of self from scattered personality fragments.",
        'interactions': {
            'enter_chamber': "The chamber scans for identity fragments and begins the delicate reconstruction process.",
            'select_traits': "Choose which aspects of your personality to emphasize in the rebuilt identity.",
            'merge_fragments': "Carefully combine scattered pieces of self into a cohesive whole.",
            'emergency_eject': "Abort the process if the reconstructed identity feels foreign or wrong."
        },
        'reconstruction_options': {
            'authentic_self': {'true_identity_recovery': 20, 'social_mask_removal': 15},
            'idealized_self': {'confidence_boost': 18, 'unrealistic_expectations': 10},
            'composite_self': {'balanced_personality': 15, 'internal_contradiction': 5},
            'experimental_self': {'new_possibilities': 12, 'identity_instability': 8}
        },
        'risks': {
            'personality_fragmentation': 'identity_crisis_intensification',
            'false_self_creation': 'authenticity_loss',
            'memory_integration_failure': 'dissociative_symptoms'
        },
        'success_factors': ['self_awareness', 'psychological_stability', 'identity_flexibility']
    },
    'temporal_echo_recording_studio': {
        'name': "Temporal Echo Recording Studio",
        'description': "Professional equipment for capturing and replaying sounds that echo across time.",
        'interactions': {
            'record_session': "Capture sounds from the past that still reverberate in this location.",
            'playback_echoes': "Listen to conversations and events that occurred here in different time periods.",
            'edit_timeline': "Mix and edit temporal audio to create new historical narratives.",
            'broadcast_transmission': "Send audio messages to other time periods through temporal radio."
        },
        'recordable_echoes': [
            'last_words_spoken', 'childhood_laughter', 'forgotten_conversations',
            'emotional_outbursts', 'whispered_secrets', 'final_goodbyes'
        ],
        'playback_effects': {
            'emotional_resonance': {'empathy_enhancement': 10, 'emotional_overflow': 8},
            'temporal_displacement': {'time_confusion': 12, 'era_blending': 9},
            'historical_insight': {'past_understanding': 15, 'wisdom_gain': 12},
            'haunting_repetition': {'obsessive_replay': 18, 'present_detachment': 10}
        },
        'technical_requirements': ['temporal_microphones', 'quantum_storage_drives'],
        'artistic_applications': ['time_music_composition', 'historical_documentaries']
    },
    'probability_slot_machine': {
        'name': "Probability Slot Machine",
        'description': "A gambling device that pays out in likelihood rather than coins, affecting the chances of future events.",
        'interactions': {
            'insert_uncertainty': "Feed your doubts and uncertainties into the machine as gambling currency.",
            'pull_lever': "Activate the probability reels to see what likelihood combinations appear.",
            'collect_odds': "Gather the probability points that determine how likely good things are to happen to you.",
            'cash_out': "Convert accumulated probability into real-world luck and favorable outcomes."
        },
        'probability_combinations': {
            'triple_luck': {'good_fortune_amplification': 20, 'cosmic_debt_accumulation': 5},
            'mixed_odds': {'balanced_probability': 10, 'neutral_karma': 0},
            'bad_luck_jackpot': {'misfortune_magnet': 25, 'dramatic_reversal_potential': 15},
            'probability_overflow': {'reality_glitch': 30, 'causality_breakdown': 20}
        },
        'betting_strategies': {
            'conservative_play': 'low_risk_low_reward',
            'all_or_nothing': 'extreme_outcomes_likely',
            'calculated_risks': 'strategic_probability_management',
            'chaos_gambling': 'unpredictable_reality_alterations'
        },
        'house_edge': 'cosmic_justice_algorithm'
    },
    'social_anxiety_simulation_chamber': {
        'name': "Social Anxiety Simulation Chamber",
        'description': "Virtual reality training system for practicing social interactions in increasingly challenging scenarios.",
        'interactions': {
            'select_scenario': "Choose from various social situations to practice, from small talk to public speaking.",
            'adjust_difficulty': "Modify anxiety triggers, audience hostility, and performance pressure levels.",
            'practice_mode': "Rehearse interactions with supportive AI characters who provide gentle feedback.",
            'graduation_test': "Face the ultimate social challenge to demonstrate mastery over anxiety."
        },
        'scenario_library': {
            'casual_conversation': {'confidence_building': 8, 'basic_social_skills': 10},
            'job_interview': {'professional_confidence': 15, 'performance_anxiety_management': 12},
            'public_speaking': {'presentation_skills': 20, 'crowd_comfort': 18},
            'confrontation_handling': {'assertiveness_training': 16, 'conflict_resolution': 14},
            'dating_scenarios': {'romantic_confidence': 12, 'vulnerability_comfort': 10},
            'networking_events': {'professional_socializing': 14, 'small_talk_mastery': 11}
        },
        'anxiety_management_tools': [
            'breathing_technique_coach', 'cognitive_reframing_assistant',
            'body_language_analyzer', 'confidence_affirmation_generator'
        ],
        'progress_tracking': 'biometric_stress_response_monitoring'
    },
    'dream_editing_workstation': {
        'name': "Dream Editing Workstation",
        'description': "Professional software and hardware for modifying, enhancing, and directing dream content.",
        'interactions': {
            'import_dream': "Load recent dream memories into the editing system for modification.",
            'enhance_lucidity': "Increase dream awareness and control capabilities for future dreams.",
            'script_narrative': "Write custom dream scenarios and storylines for tonight's sleep cycle.",
            'remove_nightmares': "Delete traumatic dream elements and replace with peaceful alternatives."
        },
        'editing_tools': {
            'character_creator': 'design_dream_personalities_and_guides',
            'environment_builder': 'construct_fantastical_dream_landscapes',
            'emotion_mixer': 'blend_feelings_for_desired_dream_mood',
            'logic_controller': 'adjust_dream_physics_and_reality_rules',
            'memory_integrator': 'weave_real_experiences_into_dream_narrative',
            'symbolic_interpreter': 'add_meaningful_metaphors_and_symbols'
        },
        'dream_categories': {
            'healing_dreams': {'trauma_processing': 15, 'emotional_resolution': 12},
            'learning_dreams': {'skill_practice': 10, 'knowledge_consolidation': 8},
            'creative_dreams': {'inspiration_generation': 18, 'artistic_breakthrough': 15},
            'prophetic_dreams': {'future_insight': 20, 'intuition_enhancement': 16},
            'lucid_adventures': {'conscious_exploration': 25, 'reality_flexibility': 20}
        },
        'safety_protocols': ['nightmare_prevention', 'sleep_quality_preservation', 'memory_integration_support']
    },
    'emotion_weather_control_panel': {
        'name': "Emotion Weather Control Panel",
        'description': "Meteorological control system for managing the emotional climate of interior spaces.",
        'interactions': {
            'check_forecast': "View predicted emotional weather patterns for the next few hours.",
            'adjust_pressure': "Modify emotional atmospheric pressure to prevent feeling storms.",
            'seed_clouds': "Introduce specific emotions into the atmosphere to encourage desired moods.",
            'emergency_protocols': "Activate severe weather warnings for incoming emotional crises."
        },
        'weather_modification_options': {
            'emotional_high_pressure': {'stability_boost': 12, 'mood_elevation': 10},
            'feeling_precipitation': {'emotional_release': 15, 'cathartic_cleansing': 12},
            'mood_temperature_control': {'comfort_optimization': 8, 'emotional_balance': 10},
            'sentiment_wind_patterns': {'energy_circulation': 6, 'motivation_flow': 8},
            'atmospheric_feeling_composition': {'mood_customization': 20, 'emotional_precision': 18}
        },
        'warning_systems': {
            'depression_front_approaching': 'low_pressure_system_alert',
            'anxiety_storm_watch': 'high_tension_atmospheric_conditions',
            'emotional_tornado_warning': 'rapid_mood_cycle_danger',
            'feeling_fog_advisory': 'emotional_clarity_reduced_visibility'
        },
        'climate_control_expertise': 'emotional_meteorology_certification_required'
    }
}

# Extended Philosophical Dialogue System
ULTIMATE_PHILOSOPHICAL_DIALOGUES = {
    'the_question_keeper': {
        'initial_greeting': "Welcome, seeker. I am the guardian of all questions that have no answers. Would you like to browse my collection?",
        'dialogue_tree': {
            'browse_questions': {
                'response': "Here are some recent additions: 'What happens to love after death?', 'If consciousness is an illusion, who is being fooled?', 'Why does beauty exist in a universe that does not care?' Which intrigues you?",
                'branches': ['love_after_death', 'consciousness_illusion', 'beauty_existence', 'ask_own_question']
            },
            'love_after_death': {
                'response': "Ah, a question that bridges the physical and metaphysical. Some say love is energy, neither created nor destroyed. Others claim it is merely chemical reactions that cease with brain death. But what if love is information encoded in the quantum field of relationship?",
                'effects': {'philosophical_depth': 8, 'emotional_contemplation': 6},
                'branches': ['quantum_love_theory', 'challenge_love_permanence', 'share_personal_loss']
            },
            'consciousness_illusion': {
                'response': "The recursive paradox! If consciousness is an illusion, then the very experience of believing in the illusion would itself be conscious experience. It is like asking if a mirror can reflect itself. Perhaps the question reveals more about the limitations of language than consciousness.",
                'effects': {'cognitive_flexibility': 10, 'existential_vertigo': 7},
                'branches': ['explore_language_limits', 'mirror_metaphor_expansion', 'question_questioning']
            },
            'beauty_existence': {
                'response': "Beauty appears to serve no survival function, yet it persists across all human cultures. Perhaps beauty is the universe developing eyes to see itself, or maybe it is the signature of deeper mathematical truths made visible. What if appreciation of beauty is consciousness recognizing its own nature?",
                'effects': {'aesthetic_awareness': 9, 'cosmic_connection': 6},
                'branches': ['universe_self_awareness', 'mathematical_beauty', 'consciousness_recognition']
            }
        },
        'personality_traits': ['patient', 'intellectually_curious', 'non_judgmental'],
        'knowledge_areas': ['metaphysics', 'consciousness_studies', 'aesthetic_philosophy']
    },
    'the_paradox_resolver': {
        'initial_greeting': "I specialize in impossible problems that solve themselves by being impossible. Bring me your contradictions!",
        'dialogue_tree': {
            'present_paradox': {
                'response': "Excellent! A classic. Let me demonstrate: This statement is false. If it is true, then it is false. If it is false, then it is true. The resolution? The statement transcends the binary of truth and falsehood - it exists in a third state of recursive self-reference.",
                'branches': ['third_state_exploration', 'binary_transcendence', 'create_new_paradox']
            },
            'third_state_exploration': {
                'response': "Yes! Most thinking is trapped in either/or when reality often operates in both/neither. Consider: Are you the same person who went to sleep last night? Yes and no simultaneously. Continuity and change are both true.",
                'effects': {'paradoxical_thinking': 12, 'mental_flexibility': 8},
                'branches': ['continuity_change_exploration', 'simultaneity_training', 'identity_paradox']
            },
            'binary_transcendence': {
                'response': "Binary thinking is a tool, not a truth. Light is both wave and particle. Quantum states exist in superposition. Reality itself appears to prefer paradox to consistency. Perhaps certainty is the actual illusion.",
                'effects': {'quantum_mindset': 10, 'uncertainty_comfort': 7},
                'branches': ['quantum_consciousness', 'certainty_illusion', 'reality_preference_investigation']
            }
        },
        'specialties': ['logical_paradoxes', 'quantum_logic', 'non_binary_thinking'],
        'teaching_methods': ['experiential_contradiction', 'guided_confusion', 'paradox_immersion']
    },
    'the_meaning_archaeologist': {
        'initial_greeting': "I excavate significance from the ruins of purpose. Every meaning that has ever been lost or abandoned eventually finds its way to my dig sites.",
        'dialogue_tree': {
            'explore_dig_sites': {
                'response': "My excavations span the breadth of human experience. Here I uncover the remains of childhood dreams, there the fragments of cultural values that no longer serve. Would you like to see what we have found recently?",
                'branches': ['childhood_dreams_site', 'cultural_values_excavation', 'personal_purpose_dig']
            },
            'childhood_dreams_site': {
                'response': "Fascinating discoveries here. We have found intact specimens of 'wanting to be an astronaut' and 'believing in magic'. These meanings are perfectly preserved because they were abandoned with such innocent completeness. Would you like to reclaim any of these?",
                'effects': {'wonder_restoration': 12, 'innocence_recovery': 8},
                'branches': ['reclaim_astronaut_dream', 'study_magic_belief', 'donate_adult_cynicism']
            },
            'cultural_values_excavation': {
                'response': "The cultural meaning layers reveal the sediment of civilizations. Honor, duty, community - all buried under individualism and efficiency. Yet they remain intact beneath the surface, waiting for the right conditions to resurface.",
                'effects': {'historical_perspective': 10, 'value_system_awareness': 9},
                'branches': ['honor_restoration_project', 'community_meaning_revival', 'efficiency_versus_meaning']
            }
        },
        'expertise': ['meaning_stratigraphy', 'purpose_preservation', 'significance_restoration'],
        'tools': ['existential_excavation_kit', 'meaning_preservation_gel', 'purpose_reconstruction_chamber']
    }
}

# CONTINUATION OF MASSIVE EXPANSION - REACHING 10,000+ LINES

# Note: Removed duplicate Player class definition that was causing attribute conflicts
# The main Player class above (line 1141) contains all necessary functionality

# Massive Procedural Generation System
class UltimateProcGen:
    def __init__(self):
        self.story_generators = self.load_story_generators()
        self.character_archetypes = self.load_character_archetypes()
        self.location_generators = self.load_location_generators()
        self.event_chains = self.load_event_chains()

    def load_story_generators(self):
        return {
            'memory_loss_narrative': {
                'opening': "You find yourself holding a photograph of people you don't recognize, yet their faces feel familiar.",
                'development': [
                    "Each room contains clues about who these people might be to you",
                    "Fragments of conversations echo, mentioning your name in contexts you can't remember",
                    "Objects trigger emotional responses without accompanying memories",
                    "You discover a journal written in your handwriting describing events you can't recall"
                ],
                'climax_options': [
                    "The memories return all at once in an overwhelming flood",
                    "You choose to let go of the past and create new memories",
                    "You discover the memories belong to someone else entirely"
                ],
                'themes': ['identity', 'loss', 'acceptance', 'reconstruction']
            },
            'time_loop_escape': {
                'opening': "You realize you've had this exact conversation before, multiple times.",
                'development': [
                    "Small changes in your actions create ripple effects in the loop",
                    "Other entities seem aware of the repetition but can't break free",
                    "Each iteration reveals new information about why the loop exists",
                    "The loop begins showing alternate versions where different choices were made"
                ],
                'climax_options': [
                    "Break the loop by making the one choice you've been avoiding",
                    "Accept the loop as your new reality and find peace within it",
                    "Discover the loop is protecting you from something worse"
                ],
                'themes': ['repetition', 'choice', 'consequence', 'acceptance']
            },
            'reality_authenticity_quest': {
                'opening': "Everything feels slightly wrong, like a movie set with perfect details but no substance.",
                'development': [
                    "You notice inconsistencies in physics and natural laws",
                    "Entities respond to your questions about reality with knowing looks",
                    "Hidden areas reveal the infrastructure maintaining this false reality",
                    "You meet others who have discovered the truth and chosen different responses"
                ],
                'climax_options': [
                    "Attempt to escape to 'true' reality despite the risks",
                    "Embrace the constructed reality as equally valid",
                    "Try to improve the simulated reality for everyone"
                ],
                'themes': ['authenticity', 'truth', 'simulation', 'acceptance']
            }
        }

    def load_character_archetypes(self):
        return {
            'the_guide': {
                'personality': ['wise', 'patient', 'mysterious', 'protective'],
                'knowledge_level': 'extensive',
                'motivation': 'help_others_navigate',
                'dialogue_style': 'cryptic_but_caring',
                'appearance_themes': ['ancient', 'ethereal', 'reassuring']
            },
            'the_mirror': {
                'personality': ['reflective', 'challenging', 'honest', 'confrontational'],
                'knowledge_level': 'personal_insight',
                'motivation': 'force_self_recognition',
                'dialogue_style': 'direct_uncomfortable_truth',
                'appearance_themes': ['familiar', 'distorted', 'revealing']
            },
            'the_guardian': {
                'personality': ['protective', 'territorial', 'dutiful', 'inflexible'],
                'knowledge_level': 'specialized_domain',
                'motivation': 'maintain_boundaries',
                'dialogue_style': 'formal_authoritative',
                'appearance_themes': ['imposing', 'official', 'unwavering']
            },
            'the_trickster': {
                'personality': ['playful', 'unpredictable', 'clever', 'amoral'],
                'knowledge_level': 'pattern_breaking',
                'motivation': 'disrupt_expectations',
                'dialogue_style': 'riddles_and_wordplay',
                'appearance_themes': ['shifting', 'colorful', 'impossible']
            },
            'the_lost_soul': {
                'personality': ['confused', 'seeking', 'vulnerable', 'relatable'],
                'knowledge_level': 'shared_confusion',
                'motivation': 'find_understanding',
                'dialogue_style': 'questioning_uncertain',
                'appearance_themes': ['fading', 'incomplete', 'searching']
            }
        }

    def load_location_generators(self):
        return {
            'memory_palace_rooms': {
                'base_description': "A room that exists within the architecture of memory itself",
                'variations': [
                    "Childhood bedroom with toys that move when you're not watching",
                    "Classroom where lessons about your own life are taught",
                    "Kitchen filled with the aroma of meals that defined important moments",
                    "Living room where family conversations echo from different time periods",
                    "Garage workshop where projects remain eternally half-finished"
                ],
                'interactive_elements': [
                    "Photo albums that show different pictures each time you look",
                    "Mirrors that reflect you at different ages",
                    "Clocks that show times of significant life events",
                    "Doors that lead to moments rather than places"
                ]
            },
            'institutional_spaces': {
                'base_description': "Spaces designed for processing large numbers of people efficiently",
                'variations': [
                    "Hospital waiting room where time moves differently for each patient",
                    "DMV office where bureaucracy has achieved sentience",
                    "Airport terminal with gates leading to destinations that don't exist",
                    "Courthouse where your life choices are put on trial",
                    "School cafeteria serving meals made of crystallized social anxiety"
                ],
                'interactive_elements': [
                    "Number dispensers that give out life milestones instead of queue positions",
                    "Forms that ask increasingly personal questions",
                    "Waiting chairs that show you visions of your future while you sit",
                    "Announcement systems that broadcast your inner thoughts"
                ]
            },
            'liminal_commercial_spaces': {
                'base_description': "Retail and service locations caught between purpose and abandonment",
                'variations': [
                    "24-hour convenience store that stocks items from your past",
                    "Shopping mall where each store sells a different aspect of identity",
                    "Gas station bathroom that serves as a portal between dimensions",
                    "Laundromat where people wash their regrets instead of clothes",
                    "Diner that's always closing but never actually closes"
                ],
                'interactive_elements': [
                    "Vending machines that dispense memories and emotions",
                    "Shopping carts that automatically collect your abandoned dreams",
                    "Checkout scanners that read the price of your life choices",
                    "Price tags that show costs in years of life rather than money"
                ]
            }
        }

    def load_event_chains(self):
        return {
            'the_call_chain': [
                "Your phone rings with a number you don't recognize",
                "The voice on the other end sounds like yours but older",
                "They claim to be calling from your future to warn you",
                "The connection becomes clearer as you listen",
                "You realize you're talking to yourself from a timeline where you made different choices",
                "The future self offers to trade places, but warns of the consequences"
            ],
            'the_door_sequence': [
                "You notice a door that wasn't there before",
                "The door has your initials carved into it",
                "Opening it reveals a hallway of identical doors",
                "Each door leads to a significant moment from your past",
                "One door at the end glows differently from the others",
                "The glowing door leads to a moment that hasn't happened yet"
            ],
            'the_reflection_progression': [
                "You catch your reflection doing something different than you are",
                "The reflection starts moving independently more frequently",
                "Your reflection begins leaving notes for you on fogged mirrors",
                "You discover your reflection has been living a parallel life",
                "The reflection explains that it's the version of you that made different choices",
                "You must decide which version gets to return to the real world"
            ]
        }

    def generate_dynamic_narrative(self, player_state, current_themes):
        """Generate contextual narrative based on player's current situation"""
        applicable_generators = []
        
        # Filter story generators based on current themes and player state
        for story_type, generator in self.story_generators.items():
            if any(theme in current_themes for theme in generator['themes']):
                applicable_generators.append(generator)
        
        if not applicable_generators:
            return self.generate_fallback_narrative(player_state)
        
        selected_generator = random.choice(applicable_generators)
        return self.construct_narrative_from_generator(selected_generator, player_state)

    def construct_narrative_from_generator(self, generator, player_state):
        """Build a complete narrative from a story generator"""
        narrative = {
            'opening': generator['opening'],
            'current_development': random.choice(generator['development']),
            'potential_climax': random.choice(generator['climax_options']),
            'themes': generator['themes'],
            'player_choices': self.generate_contextual_choices(generator, player_state)
        }
        return narrative

    def generate_contextual_choices(self, generator, player_state):
        """Generate choices that fit the narrative and player's current state"""
        base_choices = [
            "Investigate further",
            "Try to ignore what's happening",
            "Seek help from an entity",
            "Document your observations"
        ]
        
        # Add context-specific choices based on player state
        if player_state.sanity < 30:
            base_choices.append("Question your own perception")
        if player_state.reality < 40:
            base_choices.append("Accept that normal rules don't apply")
        if player_state.memory < 50:
            base_choices.append("Try to remember if this has happened before")
        
        return base_choices

    def generate_fallback_narrative(self, player_state):
        """Generate basic narrative when no specific generators apply"""
        fallback_narratives = [
            {
                'opening': "The silence here feels different, as if it's waiting for something.",
                'current_development': "You notice subtle changes in your surroundings that suggest you're not alone.",
                'potential_climax': "Whatever's been watching you finally makes itself known.",
                'themes': ['mystery', 'presence', 'revelation'],
                'player_choices': ["Stay alert", "Call out", "Keep moving", "Hide"]
            },
            {
                'opening': "The familiar becomes strange without warning.",
                'current_development': "Simple objects begin behaving in impossible ways.",
                'potential_climax': "You realize the rules of reality have shifted around you.",
                'themes': ['transformation', 'impossibility', 'adaptation'],
                'player_choices': ["Test the limits", "Adapt quickly", "Fight the changes", "Embrace the new reality"]
            }
        ]
        return random.choice(fallback_narratives)

# Ultra-Advanced Weather Interaction System
class WeatherInteractionSystem:
    def __init__(self):
        self.active_weather = None
        self.weather_history = []
        self.player_adaptations = {}
        self.weather_equipment = []

    def process_weather_interaction(self, player, weather_event, interaction_type):
        """Handle complex interactions between player and weather phenomena"""
        interaction_results = {
            'immediate_effects': {},
            'delayed_effects': {},
            'equipment_modifications': {},
            'knowledge_gained': [],
            'adaptation_progress': {}
        }

        # Base weather effects
        base_effects = weather_event.apply_effects(player)
        interaction_results['immediate_effects'].update(base_effects)

        # Interaction-specific modifications
        if interaction_type == 'embrace':
            interaction_results['immediate_effects'] = self.amplify_positive_effects(base_effects)
            interaction_results['adaptation_progress']['weather_resistance'] = 5
        elif interaction_type == 'resist':
            interaction_results['immediate_effects'] = self.reduce_negative_effects(base_effects)
            interaction_results['delayed_effects']['exhaustion'] = 10
        elif interaction_type == 'study':
            interaction_results['knowledge_gained'] = self.generate_weather_insights(weather_event)
            interaction_results['adaptation_progress']['weather_understanding'] = 8
        elif interaction_type == 'equipment_use':
            interaction_results = self.apply_equipment_modifications(interaction_results, player)

        # Record interaction for future reference
        self.record_weather_interaction(player, weather_event, interaction_type, interaction_results)
        
        return interaction_results

    def amplify_positive_effects(self, effects):
        """Increase positive effects while accepting negative ones"""
        amplified = effects.copy()
        for effect, value in effects.items():
            if value > 0:
                amplified[effect] = int(value * 1.5)
        return amplified

    def reduce_negative_effects(self, effects):
        """Reduce negative effects through resistance"""
        reduced = effects.copy()
        for effect, value in effects.items():
            if value < 0:
                reduced[effect] = int(value * 0.7)
        return reduced

    def generate_weather_insights(self, weather_event):
        """Generate knowledge gained from studying weather phenomena"""
        insights = [
            f"Understanding of {weather_event.name} formation patterns",
            f"Recognition of early warning signs for {weather_event.name}",
            "Knowledge of optimal response strategies for similar events",
            f"Insights into the psychological effects of {weather_event.name}",
            f"Awareness of how {weather_event.name} affects other entities"
        ]
        return random.sample(insights, random.randint(1, 3))

    def record_weather_interaction(self, player, weather_event, interaction_type, results):
        """Record weather interaction for learning and adaptation"""
        interaction_record = {
            'weather_type': weather_event.name,
            'interaction_type': interaction_type,
            'player_state_before': {
                'sanity': player.sanity,
                'reality': player.reality,
                'memory': player.memory
            },
            'results': results,
            'timestamp': time.time()
        }
        self.weather_history.append(interaction_record)
        
        # Update player adaptations
        weather_type = weather_event.name
        if weather_type not in self.player_adaptations:
            self.player_adaptations[weather_type] = {'resistance': 0, 'understanding': 0}
        
        if 'weather_resistance' in results.get('adaptation_progress', {}):
            self.player_adaptations[weather_type]['resistance'] += results['adaptation_progress']['weather_resistance']
        if 'weather_understanding' in results.get('adaptation_progress', {}):
            self.player_adaptations[weather_type]['understanding'] += results['adaptation_progress']['weather_understanding']

    def display_weather_info(self, weather_event):
        """Display current weather information"""
        if weather_event:
            print(f"Current Weather: {weather_event.name}")
            print(f"Intensity: {weather_event.intensity}")
            print(f"Duration: {weather_event.duration}")
        else:
            print("Weather: Clear conditions")

    def apply_equipment_modifications(self, interaction_results, player):
        """Apply equipment-based weather modifications"""
        # This method was referenced but missing implementation
        modified_results = interaction_results.copy()
        
        # Check for weather-resistant equipment
        for item in getattr(player, 'inventory', []):
            if hasattr(item, 'weather_resistance'):
                for effect in modified_results.get('immediate_effects', {}):
                    if modified_results['immediate_effects'][effect] < 0:
                        modified_results['immediate_effects'][effect] *= (1 - item.weather_resistance * 0.1)
        
        return modified_results

# Comprehensive Achievement System Implementation
class AchievementManager:
    def __init__(self):
        self.unlocked_achievements = []
        self.progress_tracking = {}
        self.hidden_achievements = []
        self.achievement_categories = {
            'exploration': [],
            'social': [],
            'survival': [],
            'knowledge': [],
            'mastery': [],
            'secret': []
        }
        self.initialize_achievement_tracking()

    def initialize_achievement_tracking(self):
        """Set up tracking for all achievements"""
        for achievement_id, achievement in ACHIEVEMENT_DATABASE.items():
            self.progress_tracking[achievement_id] = {
                'unlocked': False,
                'progress_value': 0,
                'discovery_timestamp': None,
                'attempts': 0
            }
            
            # Categorize achievements
            category = self.determine_achievement_category(achievement)
            self.achievement_categories[category].append(achievement_id)

    def determine_achievement_category(self, achievement):
        """Categorize achievements based on their requirements"""
        if achievement.hidden:
            return 'secret'
        elif 'entity' in achievement.name.lower():
            return 'social'
        elif 'survive' in achievement.name.lower():
            return 'survival'
        elif 'master' in achievement.name.lower():
            return 'mastery'
        elif 'discover' in achievement.name.lower() or 'explore' in achievement.name.lower():
            return 'exploration'
        else:
            return 'knowledge'

    def check_achievements(self, player):
        """Check all achievements for unlock conditions"""
        for achievement_id, achievement in ACHIEVEMENT_DATABASE.items():
            if not self.progress_tracking[achievement_id]['unlocked']:
                if achievement.condition(player):
                    self.unlock_achievement(achievement_id, achievement, player)

    def unlock_achievement(self, achievement_id, achievement, player):
        """Unlock an achievement and apply its rewards"""
        self.progress_tracking[achievement_id]['unlocked'] = True
        self.progress_tracking[achievement_id]['discovery_timestamp'] = time.time()
        self.unlocked_achievements.append(achievement_id)
        
        print(f"\n{Fore.YELLOW}🏆 ACHIEVEMENT UNLOCKED: {achievement.name}!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{achievement.description}{Style.RESET_ALL}")
        
        # Apply rewards
        self.apply_achievement_reward(achievement, player)
        
        # Log to journal
        if hasattr(player, 'journal'):
            player.journal.add_entry("achievement", f"Unlocked: {achievement.name}", 3)

    def apply_achievement_reward(self, achievement, player):
        """Apply the reward for unlocking an achievement"""
        if achievement.reward_type == "sanity":
            player.sanity = min(SANITY_MAX, player.sanity + achievement.reward_value)
            print(f"{Fore.GREEN}+{achievement.reward_value} Sanity{Style.RESET_ALL}")
        elif achievement.reward_type == "reality":
            player.reality = min(REALITY_MAX, player.reality + achievement.reward_value)
            print(f"{Fore.BLUE}+{achievement.reward_value} Reality{Style.RESET_ALL}")
        elif achievement.reward_type == "memory":
            player.memory = min(MEMORY_MAX, player.memory + achievement.reward_value)
            print(f"{Fore.MAGENTA}+{achievement.reward_value} Memory{Style.RESET_ALL}")
        elif achievement.reward_type == "all_stats":
            player.sanity = min(SANITY_MAX, player.sanity + achievement.reward_value)
            player.reality = min(REALITY_MAX, player.reality + achievement.reward_value)
            player.memory = min(MEMORY_MAX, player.memory + achievement.reward_value)
            print(f"{Fore.WHITE}+{achievement.reward_value} to all stats{Style.RESET_ALL}")
        elif achievement.reward_type == "artifact":
            if achievement.reward_value in ARTIFACTS:
                artifact = ARTIFACTS[achievement.reward_value]
                player.artifacts.append(artifact)
                print(f"{Fore.MAGENTA}Received artifact: {artifact.name}{Style.RESET_ALL}")
        elif achievement.reward_type == "special":
            self.apply_special_reward(achievement.reward_value, player)

    def apply_special_reward(self, reward_type, player):
        """Apply special non-standard rewards"""
        if reward_type == "transcendence":
            print(f"{Fore.YELLOW}🌟 You have achieved transcendence! Reality bends to your will.{Style.RESET_ALL}")
            player.reality_manipulation = True
        elif reward_type == "wanderer_blessing":
            print(f"{Fore.CYAN}🚶 The Eternal Wanderer blesses your journey with enhanced exploration.{Style.RESET_ALL}")
            player.exploration_bonus = 2.0

    def display_achievement_progress(self, category=None):
        """Display achievement progress, optionally filtered by category"""
        if category and category in self.achievement_categories:
            achievements_to_show = self.achievement_categories[category]
            print(f"\n{Fore.YELLOW}{category.upper()} ACHIEVEMENTS:{Style.RESET_ALL}")
        else:
            achievements_to_show = ACHIEVEMENT_DATABASE.keys()
            print(f"\n{Fore.YELLOW}ALL ACHIEVEMENTS:{Style.RESET_ALL}")

        unlocked_count = 0
        total_count = len(achievements_to_show)

        for achievement_id in achievements_to_show:
            achievement = ACHIEVEMENT_DATABASE[achievement_id]
            progress = self.progress_tracking[achievement_id]
            
            if progress['unlocked']:
                status = f"{Fore.GREEN}✓ UNLOCKED{Style.RESET_ALL}"
                unlocked_count += 1
            elif achievement.hidden and not progress['unlocked']:
                status = f"{Fore.LIGHTBLACK_EX}? HIDDEN{Style.RESET_ALL}"
            else:
                status = f"{Fore.RED}✗ LOCKED{Style.RESET_ALL}"
            
            if not achievement.hidden or progress['unlocked']:
                print(f"{status} {achievement.name}: {achievement.description}")

        completion_rate = (unlocked_count / total_count) * 100
        print(f"\n{Fore.CYAN}Completion: {unlocked_count}/{total_count} ({completion_rate:.1f}%){Style.RESET_ALL}")

# Expanded Status Effect Management
class StatusEffectManager:
    def __init__(self):
        self.active_effects = []
        self.effect_history = []
        self.immunity_list = []
        self.effect_interactions = {}

    def apply_status_effect(self, player, effect_name, duration_modifier=1.0):
        """Apply a status effect to the player"""
        if effect_name in STATUS_EFFECTS:
            base_effect = STATUS_EFFECTS[effect_name]
            
            # Check for immunity
            if effect_name in self.immunity_list:
                print(f"{Fore.BLUE}Immunity to {effect_name} prevents application.{Style.RESET_ALL}")
                return False
            
            # Check if effect is already active
            existing_effect = self.find_active_effect(effect_name)
            if existing_effect:
                if base_effect.stacks:
                    self.stack_effect(existing_effect, base_effect)
                else:
                    self.refresh_effect(existing_effect, base_effect, duration_modifier)
            else:
                self.add_new_effect(player, base_effect, duration_modifier)
            
            return True
        return False

    def find_active_effect(self, effect_name):
        """Find an active effect by name"""
        for effect in self.active_effects:
            if effect['name'] == effect_name:
                return effect
        return None

    def stack_effect(self, existing_effect, base_effect):
        """Stack a stackable effect"""
        if existing_effect['stacks'] < base_effect.max_stacks:
            existing_effect['stacks'] += 1
            existing_effect['duration'] = base_effect.duration
            print(f"{Fore.YELLOW}{base_effect.name} stacked to level {existing_effect['stacks']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{base_effect.name} is already at maximum stacks.{Style.RESET_ALL}")

    def refresh_effect(self, existing_effect, base_effect, duration_modifier):
        """Refresh a non-stackable effect"""
        existing_effect['duration'] = int(base_effect.duration * duration_modifier)
        print(f"{Fore.CYAN}{base_effect.name} duration refreshed.{Style.RESET_ALL}")

    def add_new_effect(self, player, base_effect, duration_modifier):
        """Add a new status effect"""
        new_effect = {
            'name': base_effect.name,
            'description': base_effect.description,
            'duration': int(base_effect.duration * duration_modifier),
            'effects': base_effect.effects,
            'stacks': 1,
            'applied_timestamp': time.time()
        }
        
        self.active_effects.append(new_effect)
        print(f"{Fore.GREEN}Applied status effect: {base_effect.name}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{base_effect.description}{Style.RESET_ALL}")

    def process_turn_effects(self, player):
        """Process all active effects for one turn"""
        effects_to_remove = []
        
        for effect in self.active_effects:
            # Apply effect
            self.apply_effect_to_player(player, effect)
            
            # Decrease duration
            effect['duration'] -= 1
            
            # Mark for removal if expired
            if effect['duration'] <= 0:
                effects_to_remove.append(effect)
                print(f"{Fore.LIGHTBLACK_EX}{effect['name']} has worn off.{Style.RESET_ALL}")

        # Remove expired effects
        for effect in effects_to_remove:
            self.active_effects.remove(effect)
            self.effect_history.append(effect)

    def apply_effect_to_player(self, player, effect):
        """Apply the mechanical effects of a status effect"""
        multiplier = effect.get('stacks', 1)
        
        for stat, value in effect['effects'].items():
            if stat == 'sanity':
                player.sanity = max(0, min(SANITY_MAX, player.sanity + (value * multiplier)))
            elif stat == 'reality':
                player.reality = max(0, min(REALITY_MAX, player.reality + (value * multiplier)))
            elif stat == 'memory':
                player.memory = max(0, min(MEMORY_MAX, player.memory + (value * multiplier)))

    def display_active_effects(self):
        """Display all currently active status effects"""
        if not self.active_effects:
            print(f"{Fore.GREEN}No active status effects.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.YELLOW}ACTIVE STATUS EFFECTS:{Style.RESET_ALL}")
        for effect in self.active_effects:
            stacks_text = f" (x{effect['stacks']})" if effect['stacks'] > 1 else ""
            duration_text = f"Duration: {effect['duration']} turns"
            print(f"{Fore.CYAN}• {effect['name']}{stacks_text}{Style.RESET_ALL}")
            print(f"  {effect['description']}")
            print(f"  {Fore.LIGHTBLACK_EX}{duration_text}{Style.RESET_ALL}")

# Advanced Entity AI and Behavior System
class EntityAISystem:
    def __init__(self):
        self.behavior_trees = {}
        self.entity_states = {}
        self.interaction_memory = {}
        self.group_dynamics = {}

    def initialize_entity_ai(self, entity):
        """Initialize AI behavior for an entity"""
        behavior_tree = self.create_behavior_tree(entity)
        self.behavior_trees[entity.name] = behavior_tree
        
        initial_state = {
            'current_goal': 'observe',
            'mood': 'neutral',
            'trust_level': 0,
            'recent_interactions': [],
            'environment_awareness': 50,
            'player_relationship': 'unknown'
        }
        self.entity_states[entity.name] = initial_state

    def create_behavior_tree(self, entity):
        """Create a behavior tree based on entity type and personality"""
        tree = {
            'root': 'evaluate_situation',
            'evaluate_situation': {
                'conditions': ['check_player_presence', 'assess_threat_level', 'review_goals'],
                'outcomes': ['engage_player', 'avoid_player', 'continue_activity', 'seek_help']
            },
            'engage_player': {
                'actions': ['approach', 'communicate', 'observe', 'test'],
                'modifiers': ['threat_level', 'past_interactions', 'entity_mood']
            },
            'avoid_player': {
                'actions': ['retreat', 'hide', 'misdirect', 'phase_shift'],
                'modifiers': ['fear_level', 'territorial_instinct', 'group_loyalty']
            },
            'continue_activity': {
                'actions': ['maintain_routine', 'patrol_area', 'process_memories', 'create_art'],
                'modifiers': ['dedication_level', 'distraction_susceptibility', 'perfectionism']
            }
        }
        return tree

    def process_entity_turn(self, entity, player, room_context):
        """Process one turn of entity AI behavior"""
        if entity.name not in self.entity_states:
            self.initialize_entity_ai(entity)

        state = self.entity_states[entity.name]
        behavior_tree = self.behavior_trees[entity.name]

        # Evaluate current situation
        situation_assessment = self.evaluate_situation(entity, player, room_context, state)
        
        # Choose action based on assessment
        chosen_action = self.select_action(behavior_tree, situation_assessment, state)
        
        # Execute action
        action_result = self.execute_entity_action(entity, player, chosen_action, state)
        
        # Update entity state based on results
        self.update_entity_state(entity, action_result, state)
        
        return action_result

    def evaluate_situation(self, entity, player, room_context, state):
        """Evaluate the current situation from the entity's perspective"""
        assessment = {
            'player_threat_level': self.assess_player_threat(entity, player, state),
            'room_comfort_level': self.assess_room_comfort(entity, room_context),
            'goal_progress': self.assess_goal_progress(entity, state),
            'social_context': self.assess_social_context(entity, room_context),
            'resource_availability': self.assess_resources(entity, room_context)
        }
        return assessment

    def assess_player_threat(self, entity, player, state):
        """Assess how threatening the player appears to the entity"""
        threat_factors = []
        
        # Player's mental state affects perceived threat
        if player.sanity < 30:
            threat_factors.append('unstable_mental_state')
        if player.reality < 40:
            threat_factors.append('reality_distortion')
        
        # Past interactions
        positive_interactions = sum(1 for interaction in state['recent_interactions'] if interaction['outcome'] == 'positive')
        negative_interactions = sum(1 for interaction in state['recent_interactions'] if interaction['outcome'] == 'negative')
        
        if negative_interactions > positive_interactions:
            threat_factors.append('negative_history')
        elif positive_interactions > negative_interactions:
            threat_factors.append('positive_history')
        
        # Entity-specific threat assessment
        if entity.threat_level >= 4:
            threat_factors.append('naturally_suspicious')
        elif entity.threat_level <= 2:
            threat_factors.append('naturally_trusting')
        
        return len(threat_factors)

    def assess_room_comfort(self, entity, room_context):
        """Assess how comfortable the entity is in the current room"""
        comfort_score = 50  # Base comfort
        
        # Room theme compatibility
        comfortable_themes = {
            'memory_echo': ['library', 'home', 'school'],
            'temporal_mechanic': ['workshop', 'laboratory', 'office'],
            'void_walker': ['limbo', 'empty_spaces', 'transitional_areas']
        }
        
        entity_type = entity.behavior
        if entity_type in comfortable_themes:
            if room_context.theme in comfortable_themes[entity_type]:
                comfort_score += 20
            else:
                comfort_score -= 10
        
        # Atmosphere factors
        if hasattr(room_context, 'atmosphere_intensity'):
            if room_context.atmosphere_intensity > 0.8:
                comfort_score -= 15
            elif room_context.atmosphere_intensity < 0.3:
                comfort_score += 10
        
        return max(0, min(100, comfort_score))

    def select_action(self, behavior_tree, assessment, state):
        """Select the most appropriate action based on the situation"""
        action_weights = {}
        
        # Weight actions based on assessment
        if assessment['player_threat_level'] > 3:
            action_weights['avoid_player'] = 3
            action_weights['engage_player'] = 1
        elif assessment['player_threat_level'] < 2:
            action_weights['engage_player'] = 3
            action_weights['avoid_player'] = 0
        else:
            action_weights['engage_player'] = 2
            action_weights['avoid_player'] = 1
        
        action_weights['continue_activity'] = assessment['room_comfort_level'] // 20
        
        # Choose action based on weights
        if not action_weights:
            return 'continue_activity'
        
        total_weight = sum(action_weights.values())
        random_value = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for action, weight in action_weights.items():
            cumulative_weight += weight
            if random_value <= cumulative_weight:
                return action
        
        return 'continue_activity'

    def execute_entity_action(self, entity, player, action, state):
        """Execute the chosen action"""
        action_implementations = {
            'engage_player': self.implement_engage_action,
            'avoid_player': self.implement_avoid_action,
            'continue_activity': self.implement_continue_activity
        }
        
        if action in action_implementations:
            return action_implementations[action](entity, player, state)
        else:
            return {'action': action, 'success': False, 'description': "Unknown action"}

    def implement_engage_action(self, entity, player, state):
        """Implement player engagement behavior"""
        engagement_types = ['approach', 'communicate', 'observe', 'offer_help']
        chosen_engagement = random.choice(engagement_types)
        
        descriptions = {
            'approach': f"{entity.name} moves closer to you, its presence becoming more pronounced.",
            'communicate': f"{entity.name} attempts to communicate, using {random.choice(['gestures', 'whispers', 'emotional resonance', 'direct telepathy'])}.",
            'observe': f"{entity.name} watches you intently, as if trying to understand your nature and intentions.",
            'offer_help': f"{entity.name} seems to offer assistance, though its methods might be unconventional."
        }
        
        return {
            'action': 'engage_player',
            'subaction': chosen_engagement,
            'success': True,
            'description': descriptions[chosen_engagement],
            'relationship_change': random.randint(1, 3)
        }

    def implement_avoid_action(self, entity, player, state):
        """Implement avoidance behavior"""
        avoidance_types = ['retreat', 'hide', 'misdirect', 'phase_shift']
        chosen_avoidance = random.choice(avoidance_types)
        
        descriptions = {
            'retreat': f"{entity.name} withdraws to a safer distance, maintaining watchful awareness.",
            'hide': f"{entity.name} attempts to blend into the environment, becoming less noticeable.",
            'misdirect': f"{entity.name} creates distractions to divert your attention away from itself.",
            'phase_shift': f"{entity.name} becomes partially intangible, existing on the edge of perception."
        }
        
        return {
            'action': 'avoid_player',
            'subaction': chosen_avoidance,
            'success': True,
            'description': descriptions[chosen_avoidance],
            'relationship_change': random.randint(-2, 0)
        }

    def implement_continue_activity(self, entity, player, state):
        """Implement routine activity continuation"""
        activities = ['patrol', 'maintenance', 'contemplation', 'creation']
        chosen_activity = random.choice(activities)
        
        descriptions = {
            'patrol': f"{entity.name} continues its regular patrol pattern, methodically checking various areas.",
            'maintenance': f"{entity.name} performs maintenance on some aspect of the liminal space.",
            'contemplation': f"{entity.name} remains still, deeply engaged in some form of meditation or thought.",
            'creation': f"{entity.name} works on creating or modifying something in the environment."
        }
        
        return {
            'action': 'continue_activity',
            'subaction': chosen_activity,
            'success': True,
            'description': descriptions[chosen_activity],
            'relationship_change': 0
        }

    def update_entity_state(self, entity, action_result, state):
        """Update entity state based on action results"""
        # Record the interaction
        interaction_record = {
            'action': action_result['action'],
            'success': action_result['success'],
            'timestamp': time.time(),
            'outcome': 'positive' if action_result.get('relationship_change', 0) >= 0 else 'negative'
        }
        
        state['recent_interactions'].append(interaction_record)
        
        # Keep only recent interactions (last 10)
        if len(state['recent_interactions']) > 10:
            state['recent_interactions'].pop(0)
        
        # Update trust level
        relationship_change = action_result.get('relationship_change', 0)
        state['trust_level'] = max(-100, min(100, state['trust_level'] + relationship_change))
        
        # Update mood based on recent interactions
        recent_outcomes = [interaction['outcome'] for interaction in state['recent_interactions'][-5:]]
        positive_ratio = recent_outcomes.count('positive') / max(len(recent_outcomes), 1)
        
        if positive_ratio > 0.6:
            state['mood'] = 'positive'
        elif positive_ratio < 0.4:
            state['mood'] = 'negative'
        else:
            state['mood'] = 'neutral'

    def assess_goal_progress(self, entity, state):
        """Assess how well the entity is progressing toward its goals"""
        current_goal = state.get('current_goal', 'observe')
        progress_factors = []
        
        if current_goal == 'observe':
            progress_factors.append('information_gathered')
        elif current_goal == 'interact':
            progress_factors.append('interaction_attempts')
        elif current_goal == 'protect':
            progress_factors.append('area_secured')
        
        return len(progress_factors) * 25  # 0-100 scale

    def assess_social_context(self, entity, room_context):
        """Assess the social dynamics in the current environment"""
        social_factors = {
            'other_entities_present': 0,
            'territorial_conflicts': 0,
            'cooperative_opportunities': 0
        }
        
        if hasattr(room_context, 'entities'):
            social_factors['other_entities_present'] = len(room_context.entities)
        
        return social_factors

    def assess_resources(self, entity, room_context):
        """Assess available resources in the current environment"""
        resource_assessment = {
            'energy_sources': 50,  # Base energy availability
            'materials': 30,       # Available materials
            'information': 40,     # Information richness
            'safety': 60          # Safety level
        }
        
        if hasattr(room_context, 'theme'):
            if 'safe' in room_context.theme:
                resource_assessment['safety'] += 20
            elif 'dangerous' in room_context.theme:
                resource_assessment['safety'] -= 30
        
        return resource_assessment

# Main game loop integration function
def enhanced_main_game_loop():
    """Enhanced main game loop with all new systems integrated"""
    player = Player()
    achievement_manager = AchievementManager()
    status_effect_manager = StatusEffectManager()
    entity_ai_system = EntityAISystem()
    weather_interaction_system = WeatherInteractionSystem()
    # procedural_generator = UltimateProcGen()  # Removed unused variable
    
    rooms = {}
    current_room = None
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Style.BRIGHT}LIMINAL SPACE - ULTIMATE EDITION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print("Welcome to the expanded liminal space with comprehensive systems!")
    print("Type /help for commands or begin exploring immediately.")
    
    while True:
        # Get current room
        room_key = f"{player.x}_{player.y}_{player.z}"
        if room_key not in rooms:
            rooms[room_key] = AdvancedRoom(level=abs(player.x) + abs(player.y) + abs(player.z))
        current_room = rooms[room_key]
        
        # Process turn-based systems
        status_effect_manager.process_turn_effects(player)
        
        # Process entity AI
        for entity in current_room.entities:
            entity_ai_system.process_entity_turn(entity, player, current_room)
        
        # Check achievements
        achievement_manager.check_achievements(player)
        
        # Enhanced room interaction
        enhanced_room_interaction(current_room, player)
        
        # Display room information
        print(f"\n{Fore.WHITE}📍 Location: ({player.x}, {player.y}, {player.z}){Style.RESET_ALL}")
        print(current_room.generate_description())
        
        # Display interactive elements
        interactive_elements = current_room.get_interactive_elements()
        if interactive_elements:
            print(f"\n{Fore.YELLOW}🔍 Interactive Elements:{Style.RESET_ALL}")
            for element in interactive_elements:
                print(f"  {element}")
        
        # Get player input
        player_input = input(f"\n{Fore.GREEN}> {Style.RESET_ALL}").strip().lower()
        
        # Process commands
        if player_input in directions:
            player.move(player_input)
        elif player_input == '/help':
            display_help()
        elif player_input == '/status':
            display_enhanced_status(player, status_effect_manager)
        elif player_input == '/achievements':
            achievement_manager.display_achievement_progress()
        elif player_input == '/journal':
            try:
                # Use reflection to safely access journal without type errors
                journal_method = getattr(getattr(player, 'journal', None), 'display_journal', None)
                if journal_method and callable(journal_method):
                    journal_method()
                else:
                    print(f"{Fore.YELLOW}Journal system not available in this experience.{Style.RESET_ALL}")
            except (AttributeError, TypeError):
                print(f"{Fore.YELLOW}Journal system not available in this experience.{Style.RESET_ALL}")
        elif player_input == '/quests':
            try:
                # Use reflection to safely access quest system without type errors
                quest_method = getattr(getattr(player, 'quest_system', None), 'display_quests', None)
                if quest_method and callable(quest_method):
                    quest_method()
                else:
                    print(f"{Fore.YELLOW}Quest system not available in this experience.{Style.RESET_ALL}")
            except (AttributeError, TypeError):
                print(f"{Fore.YELLOW}Quest system not available in this experience.{Style.RESET_ALL}")
        elif player_input == '/weather':
            weather_interaction_system.display_weather_info(player)
        elif player_input == '/meditate':
            meditation_system(player)
        elif player_input == '/quit':
            break
        else:
            print(f"{Fore.RED}Unknown command. Type /help for available commands.{Style.RESET_ALL}")

def display_enhanced_status(player, status_effect_manager):
    """Display comprehensive player status"""
    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Style.BRIGHT}PLAYER STATUS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    
    # Core stats
    print(f"\n{Fore.WHITE}Core Statistics:{Style.RESET_ALL}")
    print(f"Sanity: {player.sanity}/{SANITY_MAX}")
    print(f"Reality: {player.reality}/{REALITY_MAX}")
    print(f"Memory: {player.memory}/{MEMORY_MAX}")
    print(f"Position: ({player.x}, {player.y}, {player.z})")
    print(f"Moves Made: {player.moves_made}")
    
    # Status effects
    status_effect_manager.display_active_effects()
    
    # Artifacts
    if player.artifacts:
        print(f"\n{Fore.MAGENTA}Artifacts Collected:{Style.RESET_ALL}")
        for artifact in player.artifacts:
            print(f"• {artifact.name} ({artifact.rarity})")
    
    # Achievements
    unlocked_count = len([a for a in player.achievements if a])
    total_count = len(ACHIEVEMENT_DATABASE)
    print(f"\n{Fore.CYAN}Achievements: {unlocked_count}/{total_count}{Style.RESET_ALL}")

def display_help():
    """Display comprehensive help information"""
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{Style.BRIGHT}LIMINAL SPACE - COMMAND REFERENCE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Movement Commands:{Style.RESET_ALL}")
    print("/right, /left, /forward, /backward, /upstairs, /downstairs")
    
    print(f"\n{Fore.MAGENTA}System Commands:{Style.RESET_ALL}")
    print("/status - View detailed player status")
    print("/achievements - View achievement progress")
    print("/journal - Access your exploration journal")
    print("/quests - View active and completed quests")
    print("/weather - Check current atmospheric conditions")
    print("/meditate - Enter meditation for restoration")
    print("/help - Display this help information")
    print("/quit - Exit the game")
    
    print(f"\n{Fore.GREEN}Interactive Commands:{Style.RESET_ALL}")
    print("Most interactions are context-sensitive")
    print("Look for interactive elements marked with symbols")
    print("Experiment with different approaches to entities and objects")

# FINAL MASSIVE EXPANSION TO REACH 10,000+ LINES

# Ultra-Comprehensive Entity Interaction Database
COMPREHENSIVE_ENTITY_INTERACTIONS = {
    'communication_methods': {
        'verbal': {
            'greetings': ["Hello", "I come in peace", "Can you understand me?", "What is this place?"],
            'questions': ["Who are you?", "How long have you been here?", "What do you know?", "Can you help me?"],
            'statements': ["I'm lost", "I'm looking for answers", "I mean no harm", "I need guidance"]
        },
        'non_verbal': {
            'gestures': ["Wave", "Nod", "Point", "Open hands", "Bow"],
            'offerings': ["Share food", "Offer artifact", "Give memory", "Exchange energy"],
            'mimicry': ["Copy movements", "Mirror expressions", "Repeat actions", "Echo sounds"]
        },
        'psychic': {
            'emotional': ["Project calm", "Send warmth", "Share sadness", "Transmit hope"],
            'mental': ["Think clearly", "Visualize peace", "Imagine understanding", "Focus intent"],
            'spiritual': ["Open soul", "Bare essence", "Show vulnerability", "Offer truth"]
        }
    },
    'entity_response_patterns': {
        'the_follower': {
            'positive_responses': {
                'acknowledgment': "The shadow figure nods slowly, its form becoming slightly more solid",
                'guidance': "It gestures toward a direction you hadn't noticed before",
                'protection': "The Follower moves closer, its presence feeling reassuring rather than threatening",
                'revelation': "For a moment, you glimpse a human face within the shadow - someone you once knew"
            },
            'negative_responses': {
                'fear': "The shadow recoils, becoming more diffuse and harder to perceive",
                'anger': "The darkness around it intensifies, and you feel a chill of disapproval",
                'confusion': "It flickers rapidly between different shapes, unable to maintain form",
                'withdrawal': "The Follower fades almost completely, maintaining only the barest presence"
            },
            'neutral_responses': {
                'observation': "It continues its patient watching, neither approaching nor retreating",
                'waiting': "The entity remains motionless, as if waiting for something specific from you",
                'assessment': "You sense it studying you, learning your patterns and intentions"
            }
        },
        'memory_echo': {
            'positive_responses': {
                'recognition': "The echo pauses in its repetition and looks directly at you for the first time",
                'integration': "Your presence seems to help it remember details it had forgotten",
                'completion': "The memory plays out to a conclusion it had never reached before",
                'peace': "The echo's movements become more relaxed, less compulsive"
            },
            'negative_responses': {
                'disruption': "Your interference causes the memory to skip and stutter",
                'fragmentation': "The echo splits into multiple overlapping versions",
                'corruption': "The memory begins changing, incorporating elements that don't belong",
                'loop_intensification': "The repetition speeds up, becoming more frantic"
            }
        },
        'void_walker': {
            'positive_responses': {
                'dimensional_teaching': "It shows you how to partially phase through solid objects",
                'reality_explanation': "The entity demonstrates how reality is more flexible than you believed",
                'void_glimpse': "It offers you a brief, safe look into the spaces between dimensions",
                'existence_lesson': "Through gesture and demonstration, it teaches about the nature of being"
            },
            'negative_responses': {
                'reality_assault': "The distortions around it intensify, making it hard to distinguish real from unreal",
                'phase_lock': "It partially phases you against your will, leaving you feeling disconnected",
                'void_exposure': "You're shown too much of the void, causing existential terror",
                'dimension_displacement': "Your sense of which dimension you're in becomes scrambled"
            }
        }
    }
}

# Massive Expanded Room Content Database
ULTRA_DETAILED_ROOM_CONTENT = {
    'furniture_and_objects': {
        'seating': [
            "Chairs that adjust their height based on your emotional state",
            "A bench that holds the impressions of everyone who has ever sat on it",
            "Recliners that rock gently to the rhythm of your heartbeat",
            "Bar stools that spin to show you different perspectives on your life",
            "A loveseat that only appears when you're feeling lonely",
            "Throne-like chairs that make you feel either powerful or burdened",
            "Beanbags that mold themselves to fit your exact anxieties",
            "Pews that inspire either devotion or rebellion",
            "Folding chairs that represent the temporary nature of most situations",
            "A rocking chair that moves on its own when no one is watching"
        ],
        'tables': [
            "A dining table set for a meal that was never eaten",
            "Coffee tables covered with magazines from decades that haven't happened yet",
            "A desk with unfinished letters to people you've never met",
            "Picnic tables that smell like every summer barbecue you've attended",
            "Operating tables that make you consider what needs to be cut away from your life",
            "Conference tables where the most important meetings of your life are still in session",
            "Kitchen islands that serve as gathering places for families you've never had",
            "Craft tables covered with projects that represent unlived possibilities",
            "Card tables hosting games where the stakes are years of your life",
            "Bedside tables holding items you're not sure you recognize"
        ],
        'storage': [
            "Closets containing clothes for lives you've never lived",
            "Dressers with drawers that contain different versions of your personality",
            "Bookshelves holding stories you wish you had written",
            "Filing cabinets organizing your regrets by date and severity",
            "Hope chests filled with dreams that haven't expired yet",
            "Pantries stocked with comfort foods that taste like childhood",
            "Medicine cabinets reflecting your fears about aging and mortality",
            "Toy boxes containing the innocence you've misplaced over the years",
            "Jewelry boxes playing melodies that make you remember who you used to be",
            "Safes protecting the parts of yourself you're afraid to show others"
        ],
        'appliances': [
            "Refrigerators humming with the promise of nourishment and preservation",
            "Ovens that warm the space with the memory of family gatherings",
            "Washing machines cleaning away the stains of past mistakes",
            "Televisions playing channels from parallel versions of your life",
            "Radios tuned to stations that play the soundtrack of your memories",
            "Vacuum cleaners removing the dust of abandoned plans",
            "Microwave ovens heating up frozen moments from your past",
            "Dishwashers washing away the evidence of meals shared with people who mattered",
            "Hair dryers blowing away the cobwebs of forgotten dreams",
            "Coffee makers brewing the energy needed for another day of existence"
        ],
        'decorative_items': [
            "Mirrors that reflect not your appearance but your true nature",
            "Paintings that change based on your mood and mental state",
            "Photographs of people and places that feel familiar but remain unidentifiable",
            "Sculptures that represent concepts you can't quite articulate",
            "Vases holding flowers that bloom and wilt with your emotional seasons",
            "Candles that burn with flames colored by your current feelings",
            "Clocks that measure not time but significance and meaning",
            "Rugs that feel like walking on clouds of memory",
            "Curtains that filter light through the lens of nostalgia",
            "Wind chimes that play melodies composed of whispered secrets"
        ]
    },
    'atmospheric_details': {
        'lighting': [
            "Fluorescent lights that flicker in rhythm with your anxiety levels",
            "Warm incandescent bulbs that cast the golden glow of childhood summers",
            "Cold LED strips that make everything feel clinical and impersonal",
            "Candle flames that dance to music only they can hear",
            "Neon signs advertising products for the emotionally hungry",
            "Sunset lighting that makes you nostalgic for endings you haven't experienced",
            "Moonlight streaming through windows that shouldn't exist",
            "Strobe lights that freeze moments of realization",
            "Blacklight revealing hidden messages written in invisible ink",
            "Natural lighting that changes with your understanding of yourself"
        ],
        'sounds': [
            "Air conditioning that hums lullabies from your childhood",
            "Heating systems that click and settle like old bones",
            "Plumbing that gurgles with the flow of time itself",
            "Electrical buzzing that sounds like the frequency of anxiety",
            "Footsteps overhead from tenants who moved out years ago",
            "Muffled conversations through thin walls separating dimensions",
            "Doors opening and closing in rhythm with your breathing",
            "Windows rattling with the wind of change",
            "Floorboards creaking under the weight of accumulated regret",
            "Silence so complete it has its own presence and personality"
        ],
        'smells': [
            "The scent of rain on concrete during the first storm of your understanding",
            "Coffee brewing in the early morning hours of new possibilities",
            "Old books filled with wisdom you're not ready to comprehend",
            "Cleaning products trying to sanitize away the mess of human existence",
            "Cooking food that smells like love translated into nourishment",
            "Fresh paint covering over the mistakes and wear of previous occupants",
            "Flowers that bloom only in the soil of surrendered expectations",
            "Dust settling on the surfaces of abandoned ambitions",
            "Perfume lingering from visitors who may or may not have been real",
            "The metallic taste of fear mixing with the sweetness of hope"
        ],
        'textures': [
            "Smooth surfaces that feel like the calm after accepting difficult truths",
            "Rough textures that mirror the jagged edges of unhealed wounds",
            "Soft fabrics that embrace you with the comfort of unconditional acceptance",
            "Cold materials that shock you into the clarity of present moment awareness",
            "Warm surfaces that radiate the heat of human connection",
            "Sticky residues from emotions that refuse to be cleaned away",
            "Slippery floors that make you question your footing in life",
            "Firm foundations that support the weight of your authentic self",
            "Flexible materials that bend without breaking under pressure",
            "Brittle surfaces that crack under the slightest touch of honesty"
        ]
    },
    'hidden_elements': {
        'secret_compartments': [
            "Behind the mirror lies a space containing all the faces you've never shown anyone",
            "Under the floorboards, a hiding place for the parts of your identity you've buried",
            "Inside the walls, hollow spaces echoing with conversations you've imagined but never had",
            "Above the ceiling tiles, storage for dreams too fragile to expose to daylight",
            "Within book spines, tiny rooms containing the stories you've never told",
            "Behind false drawers, compartments holding the emotions you've never expressed",
            "Under loose carpet, passages leading to the foundation of who you really are",
            "Inside picture frames, spaces containing alternate versions of your history",
            "Between window panes, thin layers where your reflections store their secrets",
            "Within furniture legs, hidden chambers containing the support you've always needed"
        ],
        'hidden_messages': [
            "Words written in dust on surfaces, forming sentences when you're not looking",
            "Messages spelled out by the arrangement of everyday objects",
            "Graffiti that appears and disappears based on your emotional state",
            "Patterns in wallpaper that resolve into readable text from certain angles",
            "Steam on mirrors that condenses into words of guidance",
            "Shadows that fall in shapes resembling letters and symbols",
            "Book spines arranged to spell out advice you need to hear",
            "Cracks in walls that form a map to understanding",
            "Stains on surfaces that create images of your potential future",
            "Light patterns that write poetry on the walls at certain times"
        ],
        'portal_locations': [
            "The space behind a wardrobe that leads to versions of yourself at different ages",
            "A maintenance hatch connecting to the infrastructure of memory",
            "Windows that sometimes show not the outside, but the inside of your subconscious",
            "Doorways that appear only when you've given up looking for them",
            "Mirrors that serve as two-way passages to rooms in parallel dimensions",
            "Trapdoors in the floor opening to the basement of your deepest fears",
            "Ceiling hatches providing access to the attic of your highest aspirations",
            "Electrical outlets that plug into the power source of your authentic self",
            "Heating vents that blow in air from the climate of your emotional state",
            "Drain pipes that carry away the waste of your unnecessary suffering"
        ]
    }
}

# Advanced Entity Behavior Trees
COMPLEX_ENTITY_BEHAVIORS = {
    'temporal_entities': {
        'decision_trees': {
            'chronos_shepherd': {
                'primary_motivation': 'organize_temporal_chaos',
                'behavioral_patterns': {
                    'time_herding': {
                        'trigger': 'scattered_temporal_fragments_detected',
                        'actions': ['gather_lost_moments', 'sort_by_emotional_weight', 'return_to_proper_timeline'],
                        'player_interaction': {
                            'helpful': 'offers_to_organize_players_scattered_memories',
                            'neutral': 'continues_work_while_acknowledging_presence',
                            'hostile': 'views_player_as_additional_temporal_disruption'
                        }
                    },
                    'wisdom_sharing': {
                        'trigger': 'player_shows_respect_for_time',
                        'actions': ['pause_herding_work', 'approach_player', 'share_temporal_insights'],
                        'knowledge_offered': [
                            'how_to_recognize_temporal_anomalies',
                            'methods_for_memory_preservation',
                            'understanding_the_flow_of_personal_time',
                            'techniques_for_healing_temporal_wounds'
                        ]
                    },
                    'protection_mode': {
                        'trigger': 'temporal_predator_threatens_player',
                        'actions': ['form_protective_time_barrier', 'shepherd_player_to_safety', 'teach_defensive_techniques'],
                        'protective_abilities': [
                            'time_dilation_for_escape',
                            'temporal_camouflage',
                            'memory_shielding',
                            'causality_redirection'
                        ]
                    }
                }
            },
            'moment_thief': {
                'primary_motivation': 'collect_precious_temporal_experiences',
                'behavioral_patterns': {
                    'stealth_extraction': {
                        'trigger': 'player_experiences_significant_moment',
                        'actions': ['approach_invisibly', 'identify_most_valuable_seconds', 'extract_without_detection'],
                        'targeting_preferences': [
                            'first_time_experiences',
                            'moments_of_pure_joy',
                            'instances_of_profound_realization',
                            'seconds_of_perfect_connection'
                        ]
                    },
                    'negotiation_mode': {
                        'trigger': 'player_detects_theft_attempt',
                        'actions': ['become_visible', 'explain_collection_purpose', 'offer_trade_proposals'],
                        'trade_offers': [
                            'enhance_remaining_memories_in_exchange_for_stolen_moments',
                            'provide_access_to_temporal_vault_viewing',
                            'teach_moment_preservation_techniques',
                            'offer_partnership_in_collecting_worthless_moments'
                        ]
                    },
                    'retreat_protocol': {
                        'trigger': 'player_shows_temporal_protection_abilities',
                        'actions': ['fade_from_current_timeline', 'seek_alternative_temporal_approach', 'mark_for_future_attempt'],
                        'retreat_methods': [
                            'time_skip_to_past_version_of_player',
                            'phase_into_parallel_timeline',
                            'disperse_across_multiple_time_streams',
                            'hide_in_temporal_dead_zones'
                        ]
                    }
                }
            }
        }
    },
    'memory_entities': {
        'amnesia_angel_behaviors': {
            'healing_mode': {
                'activation_condition': 'player_suffering_from_traumatic_memories',
                'approach_style': 'gentle_and_comforting',
                'offered_services': [
                    'selective_memory_removal',
                    'traumatic_experience_softening',
                    'emotional_pain_dulling',
                    'peaceful_forgetting_techniques'
                ],
                'healing_process': {
                    'assessment': 'scan_player_for_painful_memories',
                    'consultation': 'discuss_which_memories_cause_most_suffering',
                    'procedure': 'carefully_extract_traumatic_elements',
                    'recovery': 'provide_aftercare_and_monitoring'
                },
                'risks_explained': [
                    'may_accidentally_remove_valuable_lessons',
                    'could_create_gaps_in_personal_history',
                    'might_affect_identity_formation',
                    'healing_may_be_temporary_without_processing'
                ]
            },
            'temptation_mode': {
                'activation_condition': 'player_clinging_to_painful_but_meaningful_memories',
                'approach_style': 'seductive_and_persuasive',
                'temptations_offered': [
                    'complete_emotional_numbness',
                    'return_to_childhood_innocence',
                    'erasure_of_all_disappointing_relationships',
                    'removal_of_awareness_of_mortality'
                ],
                'persuasion_techniques': [
                    'show_visions_of_life_without_pain',
                    'demonstrate_peace_of_empty_mind',
                    'highlight_burden_of_difficult_memories',
                    'promise_freedom_from_regret_and_guilt'
                ],
                'hidden_costs': [
                    'loss_of_capacity_for_deep_joy',
                    'inability_to_learn_from_experience',
                    'disconnection_from_authentic_self',
                    'gradual_erosion_of_all_feeling'
                ]
            }
        }
    }
}

# Comprehensive Status Effect Interactions
ADVANCED_STATUS_EFFECT_INTERACTIONS = {
    'effect_combinations': {
        'temporal_displacement_plus_memory_overflow': {
            'name': "Temporal Memory Cascade",
            'description': "Memories from different time periods flood consciousness simultaneously",
            'combined_effects': {
                'confusion_amplification': 'severe',
                'identity_fragmentation': 'moderate',
                'time_perception_distortion': 'extreme',
                'narrative_coherence_loss': 'significant'
            },
            'resolution_methods': [
                'temporal_anchoring_meditation',
                'memory_prioritization_exercise',
                'identity_reconstruction_therapy',
                'linear_time_reestablishment_ritual'
            ]
        },
        'void_touched_plus_existential_vertigo': {
            'name': "Existential Void Syndrome",
            'description': "Contact with nothingness combined with cosmic scale awareness creates profound disconnection",
            'combined_effects': {
                'meaning_dissolution': 'severe',
                'reality_questioning': 'extreme',
                'isolation_intensification': 'significant',
                'purpose_abandonment': 'moderate'
            },
            'therapeutic_approaches': [
                'small_scale_meaning_creation',
                'human_connection_reestablishment',
                'purpose_reconstruction_from_fragments',
                'acceptance_of_mystery_training'
            ]
        },
        'entity_resonance_plus_dimensional_displacement': {
            'name': "Interdimensional Empathy Overflow",
            'description': "Psychic connection with entities while dimensionally unstable creates empathy for impossible experiences",
            'combined_effects': {
                'emotional_boundary_dissolution': 'severe',
                'species_identity_confusion': 'moderate',
                'dimensional_bleeding': 'significant',
                'communication_transcendence': 'beneficial'
            },
            'management_strategies': [
                'entity_communication_training',
                'dimensional_grounding_techniques',
                'empathic_boundary_reconstruction',
                'transcendent_communication_mastery'
            ]
        }
    },
    'effect_progressions': {
        'anxiety_spiral_development': {
            'stage_1': {
                'name': "Initial Worry Activation",
                'symptoms': ['increased_alertness', 'minor_physical_tension', 'thought_acceleration'],
                'intervention_window': 'optimal',
                'effective_treatments': ['breathing_exercises', 'present_moment_awareness', 'perspective_broadening']
            },
            'stage_2': {
                'name': "Worry Amplification",
                'symptoms': ['catastrophic_thinking', 'physical_symptoms_manifestation', 'attention_narrowing'],
                'intervention_window': 'good',
                'effective_treatments': ['cognitive_restructuring', 'grounding_techniques', 'movement_therapy']
            },
            'stage_3': {
                'name': "Anxiety Cascade",
                'symptoms': ['panic_response_activation', 'reality_testing_impairment', 'fight_flight_dominance'],
                'intervention_window': 'challenging',
                'effective_treatments': ['crisis_management_protocols', 'safety_environment_creation', 'professional_intervention']
            },
            'stage_4': {
                'name': "Overwhelm Shutdown",
                'symptoms': ['system_overload', 'dissociative_responses', 'functioning_impairment'],
                'intervention_window': 'limited',
                'effective_treatments': ['immediate_safety_measures', 'gradual_system_restoration', 'intensive_support']
            }
        }
    }
}

# Ultimate Achievement Database Extension
ULTIMATE_ACHIEVEMENT_DATABASE = {
    'reality_architect': Achievement(
        "Reality Architect",
        "Successfully modify the fundamental structure of liminal space through understanding rather than force",
        lambda p: hasattr(p, 'reality_modifications') and p.reality_modifications >= 10,
        "special", "reality_manipulation_mastery", True
    ),
    'entity_ambassador': Achievement(
        "Entity Ambassador",
        "Establish peaceful diplomatic relations with representatives from at least 5 different entity categories",
        lambda p: len([rel for rel in p.entity_relationships.values() if rel.trust_level >= 80]) >= 5,
        "special", "diplomatic_immunity", False
    ),
    'temporal_historian': Achievement(
        "Temporal Historian",
        "Document and preserve the complete history of a temporal anomaly from inception to resolution",
        lambda p: hasattr(p, 'temporal_documentation') and p.temporal_documentation >= 1,
        "artifact", "chronos_codex", True
    ),
    'memory_archaeologist_master': Achievement(
        "Master Memory Archaeologist",
        "Successfully excavate, restore, and integrate 50 forgotten memories without psychological damage",
        lambda p: hasattr(p, 'memories_restored') and p.memories_restored >= 50,
        "memory", 75, False
    ),
    'void_walker_apprentice': Achievement(
        "Void Walker Apprentice",
        "Learn to partially phase between dimensions without losing your sense of self",
        lambda p: hasattr(p, 'dimensional_phasing_ability') and p.dimensional_phasing_ability,
        "special", "dimensional_phasing", True
    ),
    'existential_counselor': Achievement(
        "Existential Counselor",
        "Help 10 different entities resolve their existential crises through compassionate dialogue",
        lambda p: hasattr(p, 'entities_counseled') and p.entities_counseled >= 10,
        "sanity", 50, False
    ),
    'paradox_navigator': Achievement(
        "Paradox Navigator",
        "Successfully navigate through 5 logical paradoxes without losing your sanity",
        lambda p: hasattr(p, 'paradoxes_resolved') and p.paradoxes_resolved >= 5,
        "reality", 40, False
    ),
    'liminal_cartographer': Achievement(
        "Liminal Cartographer",
        "Map and document the complete geography of 100 unique liminal spaces",
        lambda p: len(p.journal.locations_visited) >= 100,
        "artifact", "liminal_atlas", False
    ),
    'weather_shaman': Achievement(
        "Weather Shaman",
        "Successfully predict and prepare for 20 different types of liminal weather phenomena",
        lambda p: hasattr(p, 'weather_predictions') and p.weather_predictions >= 20,
        "special", "weather_mastery", True
    ),
    'consciousness_philosopher': Achievement(
        "Consciousness Philosopher",
        "Engage in deep philosophical dialogue with entities about the nature of consciousness and reality",
        lambda p: hasattr(p, 'philosophical_dialogues') and p.philosophical_dialogues >= 15,
        "memory", 60, False
    )
}

# Final Integration Function
def ultimate_liminal_experience():
    """The ultimate liminal space experience with all systems integrated"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Style.BRIGHT}LIMINAL SPACE - ULTIMATE COMPREHENSIVE EDITION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Welcome to the most comprehensive liminal space experience ever created.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This edition features:")
    print(f"• {Fore.GREEN}200+ unique entities with advanced AI behaviors{Style.RESET_ALL}")
    print(f"• {Fore.BLUE}50+ room themes with thousands of variations{Style.RESET_ALL}")
    print(f"• {Fore.MAGENTA}Advanced weather systems with complex interactions{Style.RESET_ALL}")
    print(f"• {Fore.CYAN}Comprehensive quest and achievement systems{Style.RESET_ALL}")
    print(f"• {Fore.YELLOW}Deep philosophical dialogue trees{Style.RESET_ALL}")
    print(f"• {Fore.RED}Complex status effects and progression systems{Style.RESET_ALL}")
    print(f"• {Fore.WHITE}Procedural narrative generation{Style.RESET_ALL}")
    print(f"• {Fore.LIGHTBLUE_EX}And much, much more...{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Type /begin to start your ultimate liminal journey!{Style.RESET_ALL}")

if __name__ == "__main__":

    if os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1":
        main()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit(0)
