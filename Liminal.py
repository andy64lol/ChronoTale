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
        self.level = level
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
        self.temporal_awareness = 100
        self.has_light = False
        self.level = level
        self.entity_encounters = 0
        self.anomaly_exposures = 0
        self.deepest_level = 0
        self.psychological_state = "stable"
        self.last_entity_encounter = None
        self.active_effects = []

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

if __name__ == "__main__":

    if os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1":
        main()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python3 launch.py' to access all games.")
        input("Press Enter to exit...")
        sys.exit(0)
