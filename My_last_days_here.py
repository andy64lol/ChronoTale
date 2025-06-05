#!/usr/bin/env python3
"""
My Last Days Here - An Enhanced Interactive Story Game
Part of the ChronoTale Collection

A deeply emotional narrative adventure about the final days of high school,
graduation, friendships, and the transition to adulthood.
Features comprehensive save/load system and extended storyline.
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from colorama import init, Fore, Style

# Initialize colorama with proper strip settings
init(autoreset=True, strip=False, convert=True)

# Color management
def safe_color(text: str, color_code: str = "") -> str:
    """Safely apply color codes, with fallback for environments that don't support ANSI"""
    try:
        if color_code and hasattr(Fore, color_code.split('.')[1] if '.' in color_code else ''):
            return f"{color_code}{text}{Style.RESET_ALL}"
        else:
            return text
    except:
        return text

# Constants
SAVE_DIR = "saves/my_last_days_here"
MAX_SAVES = 10

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Character Definitions with Interconnected Relationships
CHARACTERS = {
    "hiroyuki": {
        "name": "Hiroyuki",
        "description": "The ordinary guy who secretly helped everyone",
        "background": "A typical high school student who always blended into the background. With graduation approaching, he reflects on how he quietly helped his classmates throughout their years together - tutoring Hina in math, covering for Hana when she needed space, and being a reliable friend to everyone.",
        "initial_stats": {"excitement": 45, "nostalgia": 35, "confidence": 30, "friendship": 35},
        "unique_trait": "hidden_kindness",
        "relationships": ["hina", "hana", "miyuki", "kazuha", "haruto", "rei", "sato", "andrew"],
        "connections": {
            "hina": "secret_tutor",
            "hana": "class_helper",
            "miyuki": "homework_helper",
            "kazuha": "study_partner",
            "haruto": "understanding_friend",
            "rei": "photography_kindness",
            "sato": "unexpected_support",
            "andrew": "cultural_helper"
        }
    },
    "hina": {
        "name": "Hina",
        "description": "The manga artist who drew everyone's stories",
        "background": "An introverted artist who secretly drew manga featuring her classmates as heroes in their daily school adventures. As graduation approaches, she wonders if she should finally share her art with everyone and pursue her dream of becoming a professional manga artist.",
        "initial_stats": {"excitement": 35, "nostalgia": 45, "confidence": 25, "friendship": 30},
        "unique_trait": "observer_artist",
        "relationships": ["hiroyuki", "hana", "miyuki", "kazuha", "haruto", "yuki", "rei", "andrew"],
        "connections": {
            "hiroyuki": "secret_reader",
            "hana": "art_subject",
            "miyuki": "admired_from_afar",
            "kazuha": "sports_sketches",
            "haruto": "understanding_friend",
            "yuki": "shared_creativity",
            "rei": "artistic_kinship",
            "andrew": "cultural_fascination"
        }
    },
    "hana": {
        "name": "Hana",
        "description": "The popular girl holding everyone together",
        "background": "Outwardly cheerful and popular, she became the unofficial social coordinator of the class. As graduation looms, she's organizing farewell events while secretly worrying about whether the friendships she's helped nurture will survive after high school.",
        "initial_stats": {"excitement": 40, "nostalgia": 50, "confidence": 35, "friendship": 45},
        "unique_trait": "social_coordinator",
        "relationships": ["hiroyuki", "hina", "miyuki", "kazuha", "haruto", "yuki", "andrew"],
        "connections": {
            "hiroyuki": "grateful_friend",
            "hina": "encouraging_supporter",
            "miyuki": "study_buddy",
            "kazuha": "class_partner",
            "haruto": "twin_sister",
            "yuki": "welcoming_friend",
            "andrew": "cultural_bridge"
        }
    },
    "miyuki": {
        "name": "Miyuki",
        "description": "The perfect student facing future uncertainty",
        "background": "Student council president with excellent grades who's always had her future planned out. As graduation approaches, she's starting to question whether the path she's chosen is really what she wants, while harboring unspoken feelings for a classmate.",
        "initial_stats": {"excitement": 50, "nostalgia": 25, "confidence": 35, "friendship": 45},
        "unique_trait": "perfectionist_questioning",
        "relationships": ["hiroyuki", "hina", "hana", "kazuha", "haruto", "yuki", "andrew"],
        "connections": {
            "hiroyuki": "homework_helper",
            "hina": "secret_admirer_of_art",
            "hana": "study_partner",
            "kazuha": "friendly_rival",
            "haruto": "secret_crush",
            "yuki": "academic_competitor",
            "andrew": "language_exchange"
        }
    },
    "kazuha": {
        "name": "Kazuha",
        "description": "The athlete bringing everyone together",
        "background": "A star athlete and natural leader who became friends with everyone regardless of social groups. As graduation nears, he's organizing sports tournaments and team activities to create lasting memories with his classmates before they all go separate ways.",
        "initial_stats": {"excitement": 55, "nostalgia": 30, "confidence": 50, "friendship": 60},
        "unique_trait": "social_unifier",
        "relationships": ["hiroyuki", "hina", "hana", "miyuki", "haruto", "yuki", "andrew"],
        "connections": {
            "hiroyuki": "study_buddy",
            "hina": "encouraging_friend",
            "hana": "festival_partner",
            "miyuki": "friendly_rival",
            "haruto": "best_friend",
            "yuki": "sports_mentor",
            "andrew": "sports_teammate"
        }
    },
    "haruto": {
        "name": "Haruto",
        "description": "The quiet twin finding his voice",
        "background": "Hana's twin brother who has always been more reserved than his outgoing sister. As graduation approaches, he's finally starting to open up to his friends and considering whether to pursue his interest in music or follow a more traditional path his family expects.",
        "initial_stats": {"excitement": 35, "nostalgia": 40, "confidence": 30, "friendship": 45},
        "unique_trait": "emerging_confidence",
        "relationships": ["hiroyuki", "hina", "hana", "miyuki", "kazuha", "yuki", "rei", "sato", "andrew"],
        "connections": {
            "hiroyuki": "understanding_friend",
            "hina": "art_appreciation",
            "hana": "twin_brother",
            "miyuki": "crush_interest",
            "kazuha": "best_friend",
            "yuki": "shared_creativity",
            "rei": "music_collaboration",
            "sato": "fellow_dreamer",
            "andrew": "cultural_exchange"
        }
    },
    "yuki": {
        "name": "Yuki",
        "description": "The transfer student finding her place",
        "background": "Transferred to the school in her second year and initially struggled to fit in. Now, as graduation nears, she's grateful for the friendships she's built and is considering staying in the area for college to maintain these connections she's worked so hard to create.",
        "initial_stats": {"excitement": 40, "nostalgia": 35, "confidence": 45, "friendship": 50},
        "unique_trait": "grateful_newcomer",
        "relationships": ["hina", "andrew", "haruto", "miyuki", "kazuha"],
        "connections": {
            "hina": "creative_friendship",
            "andrew": "fellow_outsider",
            "haruto": "shared_interests",
            "miyuki": "study_partner",
            "kazuha": "sports_encouragement"
        }
    },
    "rei": {
        "name": "Rei",
        "description": "The photography club member capturing memories",
        "background": "A quiet observer who documents school life through photography. She's been creating a secret yearbook of candid moments showing the real friendships and connections between classmates. As graduation approaches, she's planning to give everyone copies as a farewell gift.",
        "initial_stats": {"excitement": 40, "nostalgia": 55, "confidence": 35, "friendship": 45},
        "unique_trait": "memory_keeper",
        "relationships": ["hina", "hiroyuki", "haruto", "andrew", "yuki", "sato"],
        "connections": {
            "hina": "artistic_friendship",
            "hiroyuki": "captured_kindness",
            "haruto": "music_collaboration",
            "andrew": "cultural_documentation",
            "yuki": "creative_partnership",
            "sato": "unexpected_friendship"
        }
    },
    "sato": {
        "name": "Sato",
        "description": "The class clown considering his future",
        "background": "Always the entertainer who keeps everyone laughing, but graduation has him thinking seriously about what comes next. He's torn between pursuing comedy and entertainment or following a more stable career path, while treasuring the friendships that have sustained him through high school.",
        "initial_stats": {"excitement": 45, "nostalgia": 40, "confidence": 35, "friendship": 55},
        "unique_trait": "entertainer_dreamer",
        "relationships": ["haruto", "rei", "andrew", "hiroyuki", "yuki"],
        "connections": {
            "haruto": "creative_collaboration",
            "rei": "unexpected_friendship",
            "andrew": "humor_exchange",
            "hiroyuki": "supportive_friendship",
            "yuki": "encouraging_friendship"
        }
    },
    "andrew": {
        "name": "Andrew",
        "description": "The exchange student embracing Japanese culture",
        "background": "An American exchange student who initially struggled with cultural differences but has grown to love Japanese school life. As his exchange program ends with graduation, he's conflicted about returning home and considering ways to stay in Japan longer.",
        "initial_stats": {"excitement": 35, "nostalgia": 50, "confidence": 45, "friendship": 60},
        "unique_trait": "cultural_bridge",
        "relationships": ["yuki", "rei", "sato", "kazuha", "miyuki", "hina"],
        "connections": {
            "yuki": "fellow_outsider",
            "rei": "photography_collaboration",
            "sato": "humor_appreciation",
            "kazuha": "sports_friendship",
            "miyuki": "language_exchange",
            "hina": "art_appreciation"
        }
    }
}

class GameState:
    """Manages the current state of the game"""
    
    def __init__(self):
        self.player_name: str = ""
        self.selected_character: str = ""
        self.character_background: Dict[str, Any] = {}
        self.current_chapter: int = 1
        self.choices_made: List[Dict[str, Any]] = []
        self.character_stats: Dict[str, int] = {
            "excitement": 50,
            "nostalgia": 30,
            "confidence": 20,
            "friendship": 40
        }
        self.inventory: List[str] = []
        self.discovered_memories: List[str] = []
        self.relationships: Dict[str, int] = {}
        self.playtime: float = 0.0
        self.save_count: int = 0
        self.achievements: List[str] = []
        self.endings_unlocked: List[str] = []
        self.start_time: float = time.time()
        
    def add_choice(self, chapter: int, choice_text: str, choice_id: str, impact: Dict[str, int]):
        """Record a choice made by the player"""
        choice_data = {
            "chapter": chapter,
            "choice_text": choice_text,
            "choice_id": choice_id,
            "impact": impact,
            "timestamp": datetime.now().isoformat()
        }
        self.choices_made.append(choice_data)
        
        # Apply stat changes
        for stat, change in impact.items():
            if stat in self.character_stats:
                self.character_stats[stat] = max(0, min(100, self.character_stats[stat] + change))
    
    def update_playtime(self):
        """Update total playtime"""
        if self.start_time:
            self.playtime = time.time() - self.start_time

class SaveManager:
    """Handles saving and loading game data"""
    
    @staticmethod
    def save_game(game_state: GameState, save_name: Optional[str] = None) -> bool:
        """Save the current game state"""
        try:
            game_state.update_playtime()
            
            if not save_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"save_{timestamp}.json"
            
            if not save_name.endswith('.json'):
                save_name += '.json'
            
            save_path = os.path.join(SAVE_DIR, save_name)
            
            save_data = {
                "player_name": game_state.player_name,
                "selected_character": game_state.selected_character,
                "character_background": game_state.character_background,
                "current_chapter": game_state.current_chapter,
                "choices_made": game_state.choices_made,
                "character_stats": game_state.character_stats,
                "inventory": game_state.inventory,
                "discovered_memories": game_state.discovered_memories,
                "relationships": game_state.relationships,
                "playtime": game_state.playtime,
                "save_count": game_state.save_count + 1,
                "achievements": game_state.achievements,
                "endings_unlocked": game_state.endings_unlocked,
                "save_timestamp": datetime.now().isoformat(),
                "game_version": "2.0.0"
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Failed to save game: {e}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def load_game(save_name: Optional[str] = None) -> Optional[GameState]:
        """Load a game state from file"""
        try:
            if not save_name:
                saves = SaveManager.list_saves()
                if not saves:
                    return None
                save_name = saves[0]['filename']
            
            if not save_name.endswith('.json'):
                save_name += '.json'
            
            save_path = os.path.join(SAVE_DIR, save_name)
            
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            game_state = GameState()
            game_state.player_name = save_data.get("player_name", "")
            game_state.selected_character = save_data.get("selected_character", "")
            game_state.character_background = save_data.get("character_background", {})
            game_state.current_chapter = save_data.get("current_chapter", 1)
            game_state.choices_made = save_data.get("choices_made", [])
            game_state.character_stats = save_data.get("character_stats", {})
            game_state.inventory = save_data.get("inventory", [])
            game_state.discovered_memories = save_data.get("discovered_memories", [])
            game_state.relationships = save_data.get("relationships", {})
            game_state.playtime = save_data.get("playtime", 0.0)
            game_state.save_count = save_data.get("save_count", 0)
            game_state.achievements = save_data.get("achievements", [])
            game_state.endings_unlocked = save_data.get("endings_unlocked", [])
            game_state.start_time = time.time() - game_state.playtime
            
            return game_state
            
        except Exception as e:
            print(f"{Fore.RED}Failed to load game: {e}{Style.RESET_ALL}")
            return None
    
    @staticmethod
    def list_saves() -> List[Dict[str, Any]]:
        """List all available save files"""
        saves = []
        try:
            if not os.path.exists(SAVE_DIR):
                return saves
            
            for filename in os.listdir(SAVE_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(SAVE_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            save_data = json.load(f)
                        
                        save_info = {
                            "filename": filename,
                            "character": save_data.get("selected_character", "Unknown"),
                            "chapter": save_data.get("current_chapter", 1),
                            "playtime": save_data.get("playtime", 0),
                            "timestamp": save_data.get("save_timestamp", "Unknown"),
                            "player_name": save_data.get("player_name", "Unknown")
                        }
                        saves.append(save_info)
                        
                    except Exception:
                        continue
            
            # Sort by timestamp (newest first)
            saves.sort(key=lambda x: x["timestamp"], reverse=True)
            
        except Exception:
            pass
        
        return saves

class CharacterStoryAdapter:
    """Adapts story content based on selected character"""
    
    @staticmethod
    def get_character_opening(character: str) -> str:
        """Get character-specific opening text"""
        openings = {
            "hiroyuki": "You stand at your bedroom window, looking out at the school you've attended for three years. Tomorrow is graduation, and you can't help but think about all the quiet moments when you helped your classmates without them ever knowing...",
            "hina": "Your desk is covered with manga pages - secret drawings of your classmates living their daily adventures. Tomorrow is graduation, and you're wondering if you should finally share these stories that captured everyone's true hearts...",
            "hana": "The graduation ceremony checklist sits before you, every detail planned perfectly. Tomorrow is the day you've been organizing for months, but tonight you're wondering if the friendships you've nurtured will survive beyond these school walls...",
            "miyuki": "Your valedictorian speech is written and rewritten, but the words feel hollow. Tomorrow you'll stand before everyone with perfect grades and a perfect future planned, yet you're questioning if this path is truly yours...",
            "kazuha": "The sports equipment room feels different tonight. Tomorrow is graduation, and you're thinking about how sports brought everyone together - the shy kids, the smart ones, the artists. Will these bonds last beyond the final whistle?",
            "haruto": "Your guitar sits in the corner, still holding the melodies you've been too afraid to share. Tomorrow is graduation, and you're finally ready to let people hear your voice - but is it too late to change who you've been?",
            "yuki": "The acceptance letter to the local college sits on your desk. Tomorrow is graduation from the school where you finally found your place. Should you stay near these hard-won friendships or follow your original dreams?",
            "rei": "Your camera is full of candid photos showing the real connections between your classmates. Tomorrow is graduation, and you've prepared a special gift - a memory book that reveals the beautiful moments they never knew you captured...",
            "sato": "The comedy club's final performance was yesterday, but tomorrow is graduation and the real world awaits. You've made everyone laugh for three years, but now you're wondering: can you turn these smiles into a future?",
            "andrew": "Your plane ticket home sits next to your Japanese textbooks. Tomorrow is graduation, ending an exchange program that became so much more than you expected. How do you say goodbye to a place that taught you who you really are?"
        }
        return openings.get(character, "Tomorrow is graduation day, and everything is about to change...")
    
    @staticmethod
    def get_character_memories(character: str) -> List[Tuple[str, str, Dict[str, int]]]:
        """Get character-specific memory choices"""
        if character == "hiroyuki":
            return [
                ("Graduation day - tears in your eyes watching everyone you secretly helped succeed, knowing they'll never truly know", "graduation_memory", {"excitement": 20, "nostalgia": 25, "friendship": 15}),
                ("The night Hina cried over math homework and you spent four hours helping her understand, seeing her first genuine smile in weeks", "tutoring_hina", {"friendship": 20, "nostalgia": 15, "confidence": 8}),
                ("Staying up until 3am with Hana to make handwritten invitations for every classmate, watching her pour her heart into each one", "helping_hana", {"nostalgia": 25, "confidence": 12, "friendship": 15}),
                ("Finding Miyuki collapsed from exhaustion in the student council room and carrying her to the nurse, promising to help shoulder her burden", "helping_miyuki", {"friendship": 20, "nostalgia": 18, "confidence": 12}),
                ("The rainy evening when Haruto broke down about feeling invisible, and you held him while he sobbed about not knowing who he was", "haruto_friendship", {"nostalgia": 30, "friendship": 25, "confidence": 10})
            ]
        elif character == "hina":
            return [
                ("Graduation day - your hands trembling as you finally show everyone the manga pages that captured their hearts, watching their tears of recognition", "graduation_memory", {"excitement": 25, "nostalgia": 30, "confidence": 20}),
                ("Three years of secretly drawing your classmates during lunch breaks, each panel a love letter to friendships you were too shy to voice", "drawing_classmates", {"nostalgia": 25, "friendship": 20, "confidence": 8}),
                ("The moment Hiroyuki found your sketchbook and whispered 'You see us all so beautifully' - the first time anyone truly understood your art", "hiroyuki_validation", {"confidence": 30, "nostalgia": 20, "friendship": 15}),
                ("Capturing Kazuha's determination during the final sports festival, tears streaming down your face as you drew his unwavering spirit", "sketching_kazuha", {"nostalgia": 25, "friendship": 15, "confidence": 10}),
                ("Working through the night to finish a 50-page manga featuring everyone's dreams and fears, your final gift to the people who gave you a voice", "graduation_manga", {"excitement": 20, "nostalgia": 30, "friendship": 25})
            ]
        elif character == "hana":
            return [
                ("Graduation day - watching three years of careful planning unfold perfectly, but knowing this is the last time you'll bring everyone together", "graduation_memory", {"excitement": 30, "nostalgia": 35, "friendship": 25}),
                ("The night you secretly planned Haruto's farewell concert, seeing your shy twin brother finally shine as the musician you always knew he was", "haruto_surprise", {"nostalgia": 30, "friendship": 25, "confidence": 15}),
                ("Sitting with each classmate individually to help them write yearbook messages, holding back tears as they shared memories you helped create", "yearbook_messages", {"nostalgia": 25, "friendship": 30, "confidence": 18}),
                ("The school festival where you watched from backstage as everyone laughed and celebrated, knowing you'd given them one last perfect memory", "festival_success", {"confidence": 20, "nostalgia": 25, "excitement": 12}),
                ("Your final dance with Kazuha under the cherry blossoms, both of you crying as you realized childhood was ending in this very moment", "graduation_dance", {"excitement": 20, "nostalgia": 30, "friendship": 20})
            ]
        elif character == "miyuki":
            return [
                ("Graduation day - abandoning your planned valedictorian speech to speak from the heart about how your classmates taught you what truly matters", "graduation_memory", {"confidence": 25, "nostalgia": 30, "excitement": 20}),
                ("The rainy afternoon when you finally found Haruto alone in the music room, both of you crying as you confessed your feelings and fears about the future", "haruto_conversation", {"confidence": 20, "nostalgia": 25, "friendship": 20}),
                ("Three sleepless nights with Hana planning every detail of graduation, watching her sacrifice her own dreams to make everyone else's memories perfect", "hana_collaboration", {"friendship": 25, "nostalgia": 20, "confidence": 15}),
                ("The moment Kazuha made you laugh so hard during finals week that you forgot about being perfect and just felt young and free for once", "kazuha_laughs", {"nostalgia": 25, "friendship": 20, "confidence": 12}),
                ("Finding Hina's manga and realizing she saw beauty in everyone you thought were just competitors - learning what real friendship looks like", "discovering_hina", {"friendship": 20, "nostalgia": 18, "excitement": 8})
            ]
        elif character == "kazuha":
            return [
                ("Graduation day - looking at the empty sports field and remembering every laugh, every victory, every moment you brought outcasts and popular kids together through sheer determination", "graduation_memory", {"nostalgia": 35, "friendship": 30, "confidence": 20}),
                ("The final sports tournament where shy Hina cheered louder than anyone, quiet Haruto played music during breaks, and even Miyuki forgot about grades - your dream of unity finally real", "sports_tournament", {"excitement": 20, "nostalgia": 30, "friendship": 25}),
                ("Countless afternoons teaching Andrew not just Japanese sports terms, but watching him find belonging in a country that felt foreign until you made it home", "teaching_andrew", {"friendship": 25, "nostalgia": 20, "confidence": 15}),
                ("The night Haruto played guitar while you taught him to throw a baseball, both of you crying as you realized you'd found a brother in each other", "helping_haruto", {"friendship": 25, "nostalgia": 20, "confidence": 12}),
                ("Standing on the podium after the championship, not caring about the trophy but seeing everyone in the crowd cheering together - shy kids, smart kids, everyone united", "victory_celebration", {"excitement": 20, "nostalgia": 30, "friendship": 20})
            ]
        elif character == "haruto":
            return [
                ("Graduation day - your hands shaking as you perform the song you wrote about saying goodbye, watching everyone cry including yourself", "graduation_memory", {"excitement": 30, "nostalgia": 35, "confidence": 25}),
                ("The moment Kazuha grabbed your shoulders and said 'Your music saved me from the loneliness of being the only one who cared' - realizing your quiet strength mattered", "kazuha_encouragement", {"confidence": 25, "nostalgia": 20, "friendship": 20}),
                ("Finding Miyuki crying in the music room after hearing your song about feeling invisible, both of you finally understanding each other's hidden pain", "miyuki_connection", {"confidence": 20, "nostalgia": 25, "friendship": 18}),
                ("Discovering that Hina drew an entire manga chapter about your music bringing light to dark places, seeing yourself as the hero you never thought you were", "hina_collaboration", {"nostalgia": 25, "friendship": 20, "confidence": 15}),
                ("Hana surprising you with a concert she planned in secret, watching your twin sister wipe away tears as you finally let everyone hear your voice", "hana_support", {"excitement": 20, "nostalgia": 30, "friendship": 25})
            ]
        elif character == "yuki":
            return [
                ("Graduation day - standing with friends who chose to love you despite your broken Japanese and awkward moments, finally belonging somewhere", "graduation_memory", {"excitement": 25, "nostalgia": 30, "friendship": 25}),
                ("Crying with Andrew as you both practiced English and Japanese together, two outsiders who found home in each other's struggle", "andrew_help", {"friendship": 25, "nostalgia": 20, "confidence": 15}),
                ("The day Hina showed you her manga where you were the brave transfer student who saved everyone - seeing yourself as others saw you", "hina_manga", {"confidence": 25, "nostalgia": 20, "friendship": 18}),
                ("Kazuha refusing to let you sit alone during lunch until you finally joined the sports festival committee, tears of gratitude streaming down your face", "kazuha_inclusion", {"friendship": 25, "nostalgia": 18, "confidence": 15}),
                ("Late night study sessions with Miyuki where you both confessed your fears about the future, finding strength in shared vulnerability", "miyuki_dreams", {"nostalgia": 20, "friendship": 18, "confidence": 12})
            ]
        elif character == "rei":
            return [
                ("Graduation day - watching everyone cry over the photo books you made, realizing your quiet observations captured the love they didn't know they shared", "graduation_memory", {"excitement": 30, "nostalgia": 35, "friendship": 25}),
                ("Hiding behind your camera while Haruto performed, tears blurring your lens as you captured his transformation from invisible to unforgettable", "haruto_music", {"nostalgia": 30, "friendship": 20, "confidence": 15}),
                ("Andrew asking you to be his photographer because 'you see the real Japan, not the tourist version' - understanding your true artistic gift", "andrew_photos", {"friendship": 22, "nostalgia": 18, "confidence": 15}),
                ("Staying up all night with Hina combining your candid photos with her manga panels, creating a masterpiece that told everyone's true story", "hina_collaboration", {"excitement": 20, "nostalgia": 25, "friendship": 18}),
                ("Your teacher displaying your secret portraits with the caption 'The Heart of Friendship' - finally being seen as the artist you always were", "exhibition_success", {"confidence": 30, "excitement": 25, "nostalgia": 18})
            ]
        elif character == "sato":
            return [
                ("Graduation day - making everyone laugh through their tears, realizing your humor was the medicine that healed three years of teenage pain", "graduation_memory", {"excitement": 25, "nostalgia": 35, "friendship": 25}),
                ("The night your comedy show made even the shyest students laugh until they cried, watching Hina actually speak up to compliment your performance", "comedy_success", {"confidence": 25, "nostalgia": 20, "friendship": 20}),
                ("Andrew learning your jokes in broken Japanese and performing them back to you, both of you crying with laughter at the beautiful disaster", "andrew_humor", {"friendship": 20, "nostalgia": 18, "confidence": 15}),
                ("Hiroyuki staying after every performance to help you clean up, never asking for credit but always being there when you needed someone", "hiroyuki_support", {"friendship": 25, "nostalgia": 20, "confidence": 12}),
                ("Rei's photo of you mid-joke - mouth wide open, arms flailing - becoming the yearbook cover because it captured pure joy", "rei_photos", {"nostalgia": 25, "friendship": 18, "confidence": 15})
            ]
        elif character == "andrew":
            return [
                ("Graduation day - wearing your cap and gown with a small American flag pin, finally understanding that home isn't where you're from but where you choose to grow", "graduation_memory", {"excitement": 30, "nostalgia": 35, "friendship": 25}),
                ("Your presentation about cultural exchange where you broke down crying talking about how Japan saved you from loneliness, receiving a standing ovation", "presentation_success", {"confidence": 25, "nostalgia": 25, "excitement": 20}),
                ("Kazuha teaching you baseball while you taught him English curse words, both of you laughing until you couldn't breathe", "kazuha_friendship", {"friendship": 25, "nostalgia": 20, "confidence": 18}),
                ("Rei's photo series documenting your first year - from confused and isolated to laughing with friends - becoming your most treasured possession", "rei_documentation", {"nostalgia": 30, "friendship": 20, "confidence": 12}),
                ("The moment you decided to apply to Oxford to study Japan officially, knowing you needed to come back to the place that taught you who you really are", "staying_decision", {"excitement": 25, "nostalgia": 25, "confidence": 15})
            ]
        else:
            return [("A quiet moment of reflection about growing up", "default_memory", {"nostalgia": 10, "friendship": 5})]
    
    @staticmethod
    def get_character_relationships(character: str) -> List[Tuple[str, str, Dict[str, int]]]:
        """Get character-specific relationship choices"""
        if character == "hiroyuki":
            return [
                ("Hina - the artist whose talent you helped nurture", "hina_connection", {"friendship": 20, "confidence": 15}),
                ("Hana - who appreciated your behind-the-scenes help", "hana_connection", {"friendship": 18, "nostalgia": 12}),
                ("Miyuki - who relied on your quiet support", "miyuki_connection", {"friendship": 15, "confidence": 10}),
                ("Haruto - your closest confidant about the future", "haruto_connection", {"nostalgia": 25, "friendship": 20})
            ]
        elif character == "hina":
            return [
                ("Hiroyuki - who believed in your art when no one else did", "hiroyuki_connection", {"confidence": 25, "friendship": 20}),
                ("Rei - your fellow artist and creative collaborator", "rei_connection", {"excitement": 20, "friendship": 18}),
                ("Andrew - fascinated by your cultural storytelling", "andrew_connection", {"friendship": 15, "confidence": 12}),
                ("Yuki - who inspired characters in your graduation manga", "yuki_connection", {"nostalgia": 18, "friendship": 15})
            ]
        elif character == "hana":
            return [
                ("Haruto - your twin brother finding his musical voice", "haruto_connection", {"nostalgia": 30, "friendship": 25}),
                ("Miyuki - your partner in planning the perfect graduation", "miyuki_connection", {"confidence": 20, "friendship": 18}),
                ("Kazuha - your dance partner and celebration coordinator", "kazuha_connection", {"excitement": 18, "friendship": 15}),
                ("Andrew - who helped you understand different perspectives", "andrew_connection", {"friendship": 15, "confidence": 12})
            ]
        elif character == "miyuki":
            return [
                ("Haruto - whose music opened your heart to new possibilities", "haruto_connection", {"excitement": 25, "confidence": 20}),
                ("Hana - your partner in creating perfect graduation memories", "hana_connection", {"friendship": 20, "confidence": 18}),
                ("Kazuha - who taught you that excellence includes joy", "kazuha_connection", {"nostalgia": 18, "friendship": 15}),
                ("Andrew - your language exchange partner and cultural bridge", "andrew_connection", {"friendship": 15, "confidence": 12})
            ]
        elif character == "kazuha":
            return [
                ("Haruto - your best friend who found courage through music", "haruto_connection", {"friendship": 25, "nostalgia": 20}),
                ("Andrew - your sports teammate and cultural exchange buddy", "andrew_connection", {"friendship": 20, "excitement": 18}),
                ("Miyuki - your friendly rival who learned to have fun", "miyuki_connection", {"friendship": 18, "nostalgia": 15}),
                ("Yuki - who you welcomed into the sports community", "yuki_connection", {"friendship": 15, "confidence": 12})
            ]
        elif character == "haruto":
            return [
                ("Hana - your twin sister who always believed in your music", "hana_connection", {"nostalgia": 30, "friendship": 25}),
                ("Kazuha - your best friend who gave you confidence", "kazuha_connection", {"friendship": 25, "confidence": 20}),
                ("Miyuki - who listened to your music with genuine appreciation", "miyuki_connection", {"excitement": 20, "friendship": 18}),
                ("Rei - who captured your musical journey through photography", "rei_connection", {"nostalgia": 18, "friendship": 15})
            ]
        elif character == "yuki":
            return [
                ("Andrew - your fellow outsider who became family", "andrew_connection", {"friendship": 25, "nostalgia": 20}),
                ("Hina - who included you in her artistic world", "hina_connection", {"friendship": 20, "confidence": 18}),
                ("Kazuha - who welcomed you into the sports community", "kazuha_connection", {"friendship": 18, "confidence": 15}),
                ("Miyuki - your study partner and dream-sharing friend", "miyuki_connection", {"friendship": 15, "confidence": 12})
            ]
        elif character == "rei":
            return [
                ("Hina - your artistic collaborator and creative inspiration", "hina_connection", {"excitement": 25, "friendship": 20}),
                ("Andrew - who you documented throughout his cultural journey", "andrew_connection", {"nostalgia": 20, "friendship": 18}),
                ("Haruto - whose musical awakening you captured beautifully", "haruto_connection", {"nostalgia": 18, "friendship": 15}),
                ("Sato - whose comedic spirit you learned to appreciate", "sato_connection", {"friendship": 15, "excitement": 12})
            ]
        elif character == "sato":
            return [
                ("Haruto - your creative collaborator in music and comedy", "haruto_connection", {"excitement": 20, "friendship": 18}),
                ("Andrew - who appreciated your humor across cultural barriers", "andrew_connection", {"friendship": 18, "confidence": 15}),
                ("Hiroyuki - who quietly supported your entertainment dreams", "hiroyuki_connection", {"friendship": 20, "confidence": 15}),
                ("Rei - who captured your best moments and genuine spirit", "rei_connection", {"nostalgia": 15, "friendship": 12})
            ]
        elif character == "andrew":
            return [
                ("Yuki - your partner in navigating outsider experiences", "yuki_connection", {"friendship": 25, "nostalgia": 20}),
                ("Kazuha - who welcomed you through sports and genuine friendship", "kazuha_connection", {"friendship": 20, "excitement": 18}),
                ("Rei - who documented your cultural discovery journey", "rei_connection", {"nostalgia": 22, "friendship": 15}),
                ("Miyuki - your language exchange partner and academic ally", "miyuki_connection", {"friendship": 18, "confidence": 12})
            ]
        else:
            return [("A significant person in your high school journey", "default_person", {"friendship": 10, "nostalgia": 5})]

    @staticmethod
    def get_optional_scenes(character: str) -> List[Dict[str, Any]]:
        """Get character-specific optional scenes with probability outcomes"""
        if character == "hiroyuki":
            return [
                {
                    "scene_id": "confess_to_hina",
                    "title": "Confess your feelings to Hina",
                    "description": "You've supported her art for so long. Do you tell her your feelings before graduation?",
                    "trigger_condition": {"confidence": 25, "friendship": 30},
                    "outcomes": {
                        "accepted": {
                            "probability": 0.35,
                            "description": "Hina smiles and admits she's always hoped you'd say something",
                            "effects": {"excitement": 40, "confidence": 30, "friendship": 25},
                            "unlocks": "romance_ending"
                        },
                        "gentle_rejection": {
                            "probability": 0.40,
                            "description": "She values your friendship too much to risk changing it",
                            "effects": {"nostalgia": 20, "friendship": 15, "confidence": -5},
                            "unlocks": "friendship_ending"
                        },
                        "grateful_friendship": {
                            "probability": 0.25,
                            "description": "She's touched but focused on her manga career dreams",
                            "effects": {"friendship": 20, "confidence": 10, "nostalgia": 15},
                            "unlocks": "supportive_friend_memory"
                        }
                    }
                },
                {
                    "scene_id": "organize_class_reunion",
                    "title": "Propose organizing future class reunions",
                    "description": "You want to keep everyone connected. Do you take responsibility for future reunions?",
                    "trigger_condition": {"friendship": 40, "confidence": 25},
                    "outcomes": {
                        "enthusiastic_support": {
                            "probability": 0.45,
                            "description": "Everyone loves the idea and asks you to be the coordinator",
                            "effects": {"confidence": 25, "friendship": 30, "excitement": 20},
                            "unlocks": "class_coordinator_ending"
                        },
                        "moderate_interest": {
                            "probability": 0.35,
                            "description": "Some are interested, others are focused on moving forward",
                            "effects": {"friendship": 15, "confidence": 10, "nostalgia": 20},
                            "unlocks": "reunion_organizer_achievement"
                        },
                        "mixed_reactions": {
                            "probability": 0.20,
                            "description": "People are uncertain about staying connected",
                            "effects": {"nostalgia": 25, "confidence": -5, "friendship": 5},
                            "unlocks": "acceptance_memory"
                        }
                    }
                }
            ]
        
        elif character == "hina":
            return [
                {
                    "scene_id": "publish_graduation_manga",
                    "title": "Submit your graduation manga to a publisher",
                    "description": "Your manga about classmates' adventures is finished. Do you submit it professionally?",
                    "trigger_condition": {"confidence": 35, "excitement": 25},
                    "outcomes": {
                        "accepted_for_publication": {
                            "probability": 0.30,
                            "description": "A publisher loves your authentic storytelling and wants to publish it",
                            "effects": {"excitement": 40, "confidence": 35, "friendship": 20},
                            "unlocks": "manga_artist_ending"
                        },
                        "positive_feedback": {
                            "probability": 0.50,
                            "description": "Publishers give encouraging feedback and ask to see future work",
                            "effects": {"confidence": 25, "excitement": 20, "nostalgia": 15},
                            "unlocks": "aspiring_artist_achievement"
                        },
                        "rejection_with_hope": {
                            "probability": 0.20,
                            "description": "Not accepted yet, but you're inspired to keep improving",
                            "effects": {"confidence": 10, "excitement": 15, "nostalgia": 20},
                            "unlocks": "determination_memory"
                        }
                    }
                },
                {
                    "scene_id": "art_exhibition_display",
                    "title": "Display your manga at the graduation art exhibition",
                    "description": "The school wants student art for the graduation exhibition. Do you share your manga?",
                    "trigger_condition": {"confidence": 25, "friendship": 30},
                    "outcomes": {
                        "overwhelming_praise": {
                            "probability": 0.35,
                            "description": "Everyone is amazed by how well you captured their true selves",
                            "effects": {"confidence": 30, "friendship": 25, "excitement": 20},
                            "unlocks": "class_historian_ending"
                        },
                        "mixed_but_positive": {
                            "probability": 0.45,
                            "description": "Most people love it, some are surprised to see themselves",
                            "effects": {"confidence": 20, "friendship": 15, "nostalgia": 18},
                            "unlocks": "artistic_recognition_achievement"
                        },
                        "overwhelming_attention": {
                            "probability": 0.20,
                            "description": "The attention makes you shy, but you're glad you shared",
                            "effects": {"nostalgia": 25, "confidence": 5, "friendship": 10},
                            "unlocks": "artistic_courage_memory"
                        }
                    }
                }
            ]
        
        # Similar patterns for other characters...
        else:
            return []

class StoryEngine:
    """Handles the narrative flow and story progression"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.current_scene = ""
        
    def play_chapter(self, chapter_num: int):
        """Play a specific chapter"""
        chapter_methods = {
            1: self.chapter_1_school_memories,
            2: self.chapter_2_friendship_reflections,
            3: self.chapter_3_future_plans,
            4: self.chapter_4_final_preparations,
            5: self.chapter_5_graduation_day,
            6: self.chapter_6_farewells,
            7: self.chapter_7_new_beginnings
        }
        
        if chapter_num in chapter_methods:
            chapter_methods[chapter_num]()
            self.game_state.current_chapter = chapter_num + 1
        else:
            self.show_ending()
    
    def display_stats(self):
        """Display current character stats"""
        print(f"\n{Fore.CYAN}=== Your Current Feelings ==={Style.RESET_ALL}")
        stats = self.game_state.character_stats
        print(f"{Fore.GREEN}Excitement: {stats.get('excitement', 0)}/100{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Nostalgia: {stats.get('nostalgia', 0)}/100{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Confidence: {stats.get('confidence', 0)}/100{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Friendship: {stats.get('friendship', 0)}/100{Style.RESET_ALL}")
    
    def make_choice(self, prompt: str, choices: List[Tuple[str, str, Dict[str, int]]], chapter: int):
        """Handle player choice with impact tracking"""
        print(f"\n{Fore.CYAN}{prompt}{Style.RESET_ALL}")
        
        for i, (choice_text, choice_id, impact) in enumerate(choices, 1):
            print(f"{i}. {choice_text}")
        
        while True:
            try:
                choice_num = int(input(f"\n{Fore.YELLOW}Choose (1-{len(choices)}): {Style.RESET_ALL}"))
                if 1 <= choice_num <= len(choices):
                    chosen = choices[choice_num - 1]
                    self.game_state.add_choice(chapter, chosen[0], chosen[1], chosen[2])
                    
                    # Show impact
                    if any(value != 0 for value in chosen[2].values()):
                        impact_text = []
                        for stat, change in chosen[2].items():
                            if change > 0:
                                impact_text.append(f"+{change} {stat}")
                            elif change < 0:
                                impact_text.append(f"{change} {stat}")
                        
                        if impact_text:
                            print(f"\n{Fore.GREEN}Impact: {', '.join(impact_text)}{Style.RESET_ALL}")
                    
                    return chosen
                else:
                    print(f"{Fore.RED}Please choose a number between 1 and {len(choices)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Game paused. Returning to menu...{Style.RESET_ALL}")
                return choices[0] if choices else None
    
    def slow_print(self, text: str, delay: float = 0.03):
        """Print text with typing effect and proper color handling"""
        # Handle ANSI color codes properly
        import re
        
        # Split text into segments with and without ANSI codes
        ansi_pattern = r'\x1b\[[0-9;]*m'
        segments = re.split(f'({ansi_pattern})', text)
        
        for segment in segments:
            if re.match(ansi_pattern, segment):
                # This is an ANSI code, print it immediately without delay
                print(segment, end='', flush=True)
            else:
                # This is regular text, print with delay
                for char in segment:
                    print(char, end='', flush=True)
                    time.sleep(delay)
        print()  # New line at the end
    
    def chapter_1_school_memories(self):
        """Chapter 1: The Weight of Yesterday"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 1: The Weight of Yesterday")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        character = self.game_state.selected_character
        opening = CharacterStoryAdapter.get_character_opening(character)
        
        self.slow_print(f"\n{opening}")
        
        time.sleep(2)
        
        self.slow_print(f"\nThe silence in your room feels heavier tonight. Tomorrow, everything changes. Tomorrow, you say goodbye to the only home you've known for three years.")
        
        time.sleep(1)
        
        memories = CharacterStoryAdapter.get_character_memories(character)
        
        self.slow_print(f"\nWhich memory threatens to break your heart tonight?")
        
        chosen_memory = self.make_choice(
            "What memory overwhelms you with emotion?",
            memories,
            1
        )
        
        # React to the chosen memory with deeper emotion
        memory_reactions = {
            "graduation_memory": "Tears blur your vision as you realize tomorrow marks the end of an era that can never return.",
            "tutoring_hina": "Your heart aches with the bittersweet knowledge that some bonds are too precious to last forever.",
            "helping_hana": "The memory wraps around your heart like a warm embrace, tinged with the pain of knowing it's ending.",
            "sports_tournament": "The echo of laughter and cheers feels like ghosts now, beautiful and heartbreaking.",
            "music_performance": "Your chest tightens as you remember the moment vulnerability became strength, connection became love.",
            "andrew_help": "The memory brings both warmth and sorrow - knowing that some friendships transcend all boundaries, even goodbye.",
            "hina_manga": "Your throat constricts as you remember being seen, truly seen, for the first time in your life.",
            "haruto_music": "The melody still plays in your heart, but now it sounds like a lullaby for childhood's end."
        }
        
        reaction = memory_reactions.get(chosen_memory[1], "The memory pierces through you with the exquisite pain of time that cannot be reclaimed.")
        self.slow_print(f"\n{reaction}")
        
        self.slow_print(f"\nYou close your eyes and let yourself feel everything - the joy, the pain, the love, the loss. Tomorrow you'll be strong. Tonight, you grieve for what you're leaving behind.")
        
        self.display_stats()
    
    def chapter_2_friendship_reflections(self):
        """Chapter 2: The Bonds We've Built"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 2: The Bonds We've Built")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("Your phone buzzes with messages from classmates, each preparing for tomorrow in their own way. As you scroll through the group chat, you think about the relationships that have shaped your high school experience...")
        
        relationships = CharacterStoryAdapter.get_character_relationships(self.game_state.selected_character)
        
        chosen_relationship = self.make_choice(
            "Which relationship has meant the most to you?",
            relationships,
            2
        )
        
        # Add deeper reflection based on choice
        self.slow_print(f"\nYou close your eyes and remember all the moments you shared. These connections have shaped who you've become...")
        
        time.sleep(1)
        self.display_stats()
    
    def chapter_3_future_plans(self):
        """Chapter 3: What Comes Next"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 3: What Comes Next")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("The acceptance letters and job applications on your desk represent different paths forward. Tomorrow marks not just an ending, but a beginning. What kind of future do you want to build?")
        
        future_choices = [
            ("Focus on pursuing your creative dreams", "creative_path", {"excitement": 20, "confidence": 15}),
            ("Choose a stable, practical career", "practical_path", {"confidence": 15, "nostalgia": 10}),
            ("Stay close to home and friends", "local_path", {"friendship": 25, "nostalgia": 15}),
            ("Adventure into the unknown", "adventure_path", {"excitement": 25, "confidence": 10}),
            ("Take time to figure things out", "discovery_path", {"nostalgia": 20, "confidence": 5})
        ]
        
        chosen_future = self.make_choice(
            "What path calls to you most strongly?",
            future_choices,
            3
        )
        
        path_reactions = {
            "creative_path": "You feel a surge of determination to follow your artistic passions, whatever the risk.",
            "practical_path": "There's comfort in choosing security, even if it means setting aside some dreams.",
            "local_path": "The thought of maintaining these precious friendships gives you strength.",
            "adventure_path": "Your heart races with excitement about discovering who you could become.",
            "discovery_path": "Sometimes the wisest choice is admitting you need more time to grow."
        }
        
        reaction = path_reactions.get(chosen_future[1], "The decision feels right in your heart.")
        self.slow_print(f"\n{reaction}")
        
        self.display_stats()
    
    def chapter_4_final_preparations(self):
        """Chapter 4: The Last Evening"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 4: The Last Evening")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("Your graduation outfit hangs ready, your speech (if you're giving one) is practiced, and your yearbook is full of signatures. But there's still one thing you want to do before tomorrow...")
        
        final_preparations = [
            ("Write heartfelt letters to your closest friends", "letters", {"friendship": 20, "nostalgia": 15}),
            ("Create a time capsule of memories", "time_capsule", {"nostalgia": 25, "excitement": 10}),
            ("Call family members to share your feelings", "family_call", {"confidence": 15, "nostalgia": 20}),
            ("Take a midnight walk around the school", "school_walk", {"nostalgia": 30, "confidence": 10}),
            ("Organize your room and prepare for the future", "organization", {"confidence": 20, "excitement": 15})
        ]
        
        chosen_preparation = self.make_choice(
            "How do you want to spend this final evening?",
            final_preparations,
            4
        )
        
        # Check for optional scenes based on stats and character
        self._check_optional_scenes()
        
        self.display_stats()
    
    def chapter_5_graduation_day(self):
        """Chapter 5: The Big Day"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 5: Graduation Day")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("The morning sun streams through your window as you wake up on graduation day. Your heart is full of anticipation, nostalgia, and excitement all at once. Today, everything changes...")
        
        time.sleep(2)
        
        self.slow_print("At the ceremony, you look around at all your classmates in their graduation caps and gowns. So many memories, so many friendships, so many dreams about to unfold...")
        
        graduation_moments = [
            ("Focus on feeling proud of how far you've all come", "pride_focus", {"excitement": 25, "confidence": 20}),
            ("Let yourself feel the sadness of this ending", "sadness_embrace", {"nostalgia": 30, "friendship": 15}),
            ("Concentrate on excitement for the future", "future_excitement", {"excitement": 35, "confidence": 15}),
            ("Appreciate being present in this moment", "mindful_presence", {"nostalgia": 20, "confidence": 10, "friendship": 10})
        ]
        
        chosen_moment = self.make_choice(
            "As you sit in the graduation ceremony, what fills your heart?",
            graduation_moments,
            5
        )
        
        self.slow_print("\nThe principal calls names one by one. Each step across the stage represents years of growth, friendship, and discovery...")
        
        self.display_stats()
    
    def chapter_6_farewells(self):
        """Chapter 6: Saying Goodbye"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 6: Saying Goodbye")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("After the ceremony, everyone gathers for photos, hugs, and final conversations. The reality of separation is setting in, but so is the appreciation for everything you've shared...")
        
        farewell_choices = [
            ("Organize a group photo with everyone", "group_photo", {"friendship": 25, "nostalgia": 20}),
            ("Have one-on-one conversations with close friends", "individual_talks", {"friendship": 30, "confidence": 15}),
            ("Share contact information and plan future meetings", "stay_connected", {"friendship": 20, "excitement": 15}),
            ("Give everyone small gifts you prepared", "gift_giving", {"friendship": 35, "nostalgia": 15}),
            ("Simply enjoy the moment without forcing anything", "natural_flow", {"confidence": 20, "nostalgia": 25})
        ]
        
        chosen_farewell = self.make_choice(
            "How do you want to handle these final moments together?",
            farewell_choices,
            6
        )
        
        self.slow_print("\nAs the day winds down, you realize that while this chapter is ending, the story of your friendships will continue in new and unexpected ways...")
        
        self.display_stats()
    
    def chapter_7_new_beginnings(self):
        """Chapter 7: Moving Forward"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 7: New Beginnings")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("A week has passed since graduation. Your room looks different now - some things packed away, others set out for your new life. You receive a text from a classmate sharing their first day at their new job or college...")
        
        new_beginning_choices = [
            ("Reply enthusiastically and share your own updates", "enthusiastic_sharing", {"excitement": 20, "friendship": 15}),
            ("Feel grateful that the connections are continuing", "grateful_connection", {"friendship": 25, "nostalgia": 15}),
            ("Realize how much you've all grown already", "growth_realization", {"confidence": 25, "excitement": 10}),
            ("Plan a reunion for later in the year", "reunion_planning", {"friendship": 30, "excitement": 20})
        ]
        
        chosen_beginning = self.make_choice(
            "How do you respond to staying connected with your classmates?",
            new_beginning_choices,
            7
        )
        
        self.slow_print(f"\nAs {CHARACTERS[self.game_state.selected_character]['name']}, you've learned that graduation isn't really an ending - it's a transformation. The friendships, lessons, and memories from high school have become part of who you are, and they'll continue to influence your journey ahead...")
        
        self.show_ending()
    
    def _check_optional_scenes(self):
        """Check for character-specific optional scenes"""
        optional_scenes = CharacterStoryAdapter.get_optional_scenes(self.game_state.selected_character)
        
        for scene in optional_scenes:
            if self._can_trigger_scene(scene):
                self._present_optional_scene(scene)
                break  # Only one optional scene per chapter
    
    def _can_trigger_scene(self, scene: Dict[str, Any]) -> bool:
        """Check if scene trigger conditions are met"""
        trigger = scene.get("trigger_condition", {})
        stats = self.game_state.character_stats
        
        for stat, required_value in trigger.items():
            if stats.get(stat, 0) < required_value:
                return False
        
        return True
    
    def _present_optional_scene(self, scene: Dict[str, Any]):
        """Present optional scene to player"""
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"{Fore.YELLOW}Optional Scene Available!")
        print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{scene['title']}{Style.RESET_ALL}")
        print(f"{scene['description']}")
        
        choice = input(f"\n{Fore.YELLOW}Do you want to pursue this opportunity? (y/n): {Style.RESET_ALL}").lower()
        
        if choice in ['y', 'yes']:
            self._execute_optional_scene(scene)
        else:
            print(f"\n{Fore.BLUE}You decide to let this moment pass...{Style.RESET_ALL}")
    
    def _execute_optional_scene(self, scene: Dict[str, Any]):
        """Execute optional scene with probability-based outcome"""
        outcomes = scene.get("outcomes", {})
        
        # Calculate outcome based on probabilities
        rand = random.random()
        cumulative_prob = 0.0
        chosen_outcome = None
        
        for outcome_id, outcome_data in outcomes.items():
            cumulative_prob += outcome_data["probability"]
            if rand <= cumulative_prob:
                chosen_outcome = outcome_data
                break
        
        if chosen_outcome:
            print(f"\n{Fore.GREEN}{chosen_outcome['description']}{Style.RESET_ALL}")
            
            # Apply effects
            for stat, change in chosen_outcome["effects"].items():
                if stat in self.game_state.character_stats:
                    self.game_state.character_stats[stat] = max(0, min(100, 
                        self.game_state.character_stats[stat] + change))
            
            # Track unlocks
            if "unlocks" in chosen_outcome:
                unlock = chosen_outcome["unlocks"]
                if "ending" in unlock:
                    self.game_state.endings_unlocked.append(unlock)
                elif "achievement" in unlock:
                    self.game_state.achievements.append(unlock)
            
            time.sleep(2)
    
    def show_ending(self):
        """Show character-specific ending based on their unique path"""
        stats = self.game_state.character_stats
        character = self.game_state.selected_character
        character_name = CHARACTERS[character]['name']
        
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}GRADUATION: A NEW CHAPTER BEGINS")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        
        # Character-specific endings with university/career paths
        character_endings = {
            "hiroyuki": {
                "university": "You've been accepted to a local university where you plan to study education. Your dream is to become a teacher who helps students the way you helped your classmates - quietly, consistently, and with genuine care.",
                "path": "university",
                "future": "Teaching and helping others discover their potential"
            },
            "hina": {
                "university": "Art school accepted your graduation manga as part of your portfolio. You'll study visual storytelling and manga creation, finally ready to share your unique perspective with the world.",
                "path": "art_school", 
                "future": "Professional manga artist and storyteller"
            },
            "hana": {
                "career": "You've decided to take a gap year to work at an event planning company while figuring out your next steps. Your talent for bringing people together has opened unexpected opportunities.",
                "path": "gap_year_career",
                "future": "Event coordination and community building"
            },
            "miyuki": {
                "university": "Despite perfect grades qualifying you for any university, you've chosen a program that combines business with social work - a path that honors both achievement and helping others.",
                "path": "university",
                "future": "Social entrepreneurship and community leadership"
            },
            "kazuha": {
                "university": "Your athletic scholarship to university comes with the opportunity to study sports psychology. You want to help others find the same confidence that sports gave you.",
                "path": "university_athletic",
                "future": "Sports psychology and youth mentorship"
            },
            "haruto": {
                "career": "You've decided to pursue music full-time, starting with local performances while building your confidence. University can wait - your voice needs to be heard now.",
                "path": "music_career",
                "future": "Musician and composer"
            },
            "yuki": {
                "university": "You've chosen to attend the local university to stay near the friendships you've worked so hard to build. Sometimes the best choice is staying where you belong.",
                "path": "local_university",
                "future": "Psychology and helping transfer students"
            },
            "rei": {
                "university": "Your photography portfolio earned you a spot at a prestigious arts university. You'll study documentary photography while continuing to capture the stories that matter.",
                "path": "arts_university",
                "future": "Documentary photographer and visual storyteller"
            },
            "sato": {
                "career": "You've chosen to pursue comedy and entertainment professionally, starting with local venues while developing your unique style. Making people laugh is your calling.",
                "path": "entertainment_career",
                "future": "Professional comedian and entertainer"
            },
            "andrew": {
                "university": "Your exchange program was so successful that Oxford University offered you a place to study International Relations. You'll return to England but carry Japan in your heart forever.",
                "path": "oxford_university",
                "future": "International diplomacy bridging cultures"
            }
        }
        
        character_ending = character_endings.get(character, {
            "university": "You're ready for whatever path lies ahead.",
            "path": "unknown",
            "future": "An exciting journey of discovery"
        })
        
        # Display character-specific ending
        self.slow_print(f"\n{Fore.YELLOW}Six months later...{Style.RESET_ALL}")
        
        if character == "andrew":
            self.slow_print(f"\n{Fore.CYAN}You're walking through the historic halls of Oxford University, wearing your student robes. The dreaming spires remind you of the school in Japan where you found yourself. Your study abroad application essay about 'Finding Home in a Foreign Land' was what secured your place here.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}Your dormitory wall is covered with photos from your Japanese graduation - Rei's candid shots of everyone laughing together. Your roommate asks about them, and you smile as you begin to tell the story of the year that changed your life.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As Andrew, you've learned that home isn't where you're from - it's where you discover who you're meant to become. Oxford will give you the tools to bridge cultures and help others find their place in the world, just as your Japanese classmates helped you find yours.{Style.RESET_ALL}")
        
        elif character_ending["path"] in ["university", "arts_university", "local_university", "university_athletic"]:
            self.slow_print(f"\n{Fore.CYAN}You're walking across your university campus, backpack full of textbooks and dreams. The acceptance letter is still pinned to your wall at home, a reminder of how far you've come since graduation day.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}{character_ending['university']}{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As {character_name}, you've chosen the path of learning and growth. The friendships from high school remain strong, and your shared experiences continue to shape who you're becoming.{Style.RESET_ALL}")
        
        else:  # Career/gap year paths
            self.slow_print(f"\n{Fore.CYAN}You're getting ready for another day in your new life, one that doesn't involve textbooks or lecture halls. Instead, you're pursuing your passion directly, learning through experience rather than classrooms.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}{character_ending.get('career', character_ending.get('university', 'You are following your own unique path.'))}{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As {character_name}, you've chosen to trust your instincts and follow your heart. The skills and friendships from high school give you the foundation to build something uniquely yours.{Style.RESET_ALL}")
        
        # Common ending note about friendship
        self.slow_print(f"\n{Fore.YELLOW}Your phone buzzes with a message in the group chat you all created after graduation. Despite everyone's different paths - university, careers, gap years - the bonds you formed during those final days of high school remain unbroken.{Style.RESET_ALL}")
        
        self.slow_print(f"\n{Fore.MAGENTA}Some stories end with graduation. Yours is just beginning.{Style.RESET_ALL}")
        
        self.show_final_stats(character_ending)
    
    def show_final_stats(self, character_ending: Dict[str, str]):
        """Display comprehensive final statistics"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}Your High School Journey")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        character = CHARACTERS[self.game_state.selected_character]
        
        print(f"\n{Fore.YELLOW}Character: {character['name']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Trait: {character['unique_trait']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Future Path: {character_ending.get('future', 'Unknown path')}{Style.RESET_ALL}")
        
        # Path type
        path_type = character_ending.get('path', 'unknown')
        path_descriptions = {
            "university": "University Student",
            "arts_university": "Arts University Student", 
            "local_university": "Local University Student",
            "university_athletic": "University Athlete",
            "oxford_university": "Oxford University Student",
            "gap_year_career": "Gap Year Professional",
            "music_career": "Professional Musician",
            "entertainment_career": "Entertainment Professional"
        }
        
        print(f"{Fore.CYAN}Path Type: {path_descriptions.get(path_type, 'Unique Journey')}{Style.RESET_ALL}")
        
        # Final stats
        print(f"\n{Fore.CYAN}Final Emotional State:{Style.RESET_ALL}")
        for stat, value in self.game_state.character_stats.items():
            print(f"{Fore.GREEN}{stat.title()}: {value}/100{Style.RESET_ALL}")
        
        # Achievements
        if self.game_state.achievements:
            print(f"\n{Fore.YELLOW}Achievements Unlocked:{Style.RESET_ALL}")
            for achievement in self.game_state.achievements:
                print(f"⭐ {achievement.replace('_', ' ').title()}")
        
        # Special endings
        if self.game_state.endings_unlocked:
            print(f"\n{Fore.MAGENTA}Special Endings Unlocked:{Style.RESET_ALL}")
            for ending in self.game_state.endings_unlocked:
                print(f"✨ {ending.replace('_', ' ').title()}")
        
        # Playtime
        playtime = self.format_playtime(self.game_state.playtime)
        print(f"\n{Fore.BLUE}Time Played: {playtime}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Choices Made: {len(self.game_state.choices_made)}{Style.RESET_ALL}")
        
        # Show university vs career path stats
        university_characters = ["hiroyuki", "hina", "miyuki", "kazuha", "yuki", "rei", "andrew"]
        career_characters = ["hana", "haruto", "sato"]
        
        if self.game_state.selected_character in university_characters:
            print(f"\n{Fore.GREEN}🎓 University Path: Ready for higher education and continued learning{Style.RESET_ALL}")
        elif self.game_state.selected_character in career_characters:
            print(f"\n{Fore.GREEN}💼 Career Path: Following passion and entering the workforce{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Thank you for experiencing this graduation journey!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Every ending is a new beginning...{Style.RESET_ALL}")
    
    def format_playtime(self, seconds: float) -> str:
        """Format playtime in readable format"""
        minutes = int(seconds // 60)
        hours = minutes // 60
        minutes = minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

def check_launcher() -> None:
    """Check if the game was launched from the main launcher"""
    
    # Check for the actual launcher environment variable
    launched_from_launcher = os.environ.get('LAUNCHED_FROM_LAUNCHER')
    
    # Check if launched directly vs from launcher
    if not launched_from_launcher:
        print(f"{Fore.YELLOW}=== LAUNCHER PROTECTION ==={Style.RESET_ALL}")
        print(f"{Fore.CYAN}This game is part of the ChronoTale collection.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}For the best experience, launch from the main ChronoTale launcher.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Starting in standalone mode with limited features...{Style.RESET_ALL}\n")
    else:
        # Launched from launcher
        print(f"{Fore.GREEN}✓ Launched from ChronoTale launcher{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Full feature set available!{Style.RESET_ALL}\n")

class GameManager:
    """Main game manager that coordinates all systems"""
    
    def __init__(self):
        self.game_state: Optional[GameState] = None
        self.story_engine: Optional[StoryEngine] = None
    
    def show_title_screen(self):
        """Display the game title and introduction"""
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.CYAN}        MY LAST DAYS HERE: FAREWELL")
        print(f"{Fore.CYAN}    An Interactive Story Experience")
        print(f"{Fore.CYAN}      Part of the ChronoTale Collection")
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}A deeply emotional journey through the final moments of")
        print("childhood, where every goodbye carries the weight of")
        print("three years of shared dreams, laughter, and tears.")
        print(f"These last days will change everything forever.{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💫 Story Theme: Experience the profound beauty and")
        print("heartbreak of growing up, saying farewell to the people")
        print(f"who shaped you, and stepping into an uncertain future.{Style.RESET_ALL}")
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}Main Menu")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        print(f"1. {Fore.GREEN}New Game{Style.RESET_ALL}")
        print(f"2. {Fore.YELLOW}Load Game{Style.RESET_ALL}")
        print(f"3. {Fore.BLUE}View Save Files{Style.RESET_ALL}")
        print(f"4. {Fore.MAGENTA}Game Information{Style.RESET_ALL}")
        print(f"5. {Fore.RED}Exit{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Select option (1-5): {Style.RESET_ALL}")
                if choice in ['1', '2', '3', '4', '5']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter 1-5.{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                return '5'
    
    def new_game(self):
        """Start a new game"""
        print(f"\n{Fore.GREEN}Starting a new graduation journey...{Style.RESET_ALL}")
        
        # Character selection
        character = self.select_character()
        if not character:
            return False
        
        # Initialize game state with character name
        self.game_state = GameState()
        self.game_state.player_name = CHARACTERS[character]['name']
        self.game_state.selected_character = character
        self.game_state.character_background = CHARACTERS[character].copy()
        
        # Set character-specific initial stats
        self.game_state.character_stats = CHARACTERS[character]["initial_stats"].copy()
        
        self.story_engine = StoryEngine(self.game_state)
        
        print(f"\n{Fore.GREEN}You are {CHARACTERS[character]['name']}.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{CHARACTERS[character]['background']}{Style.RESET_ALL}")
        time.sleep(3)
        
        return True
    
    def select_character(self):
        """Allow player to select a character"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Choose Your Character")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Each character has a unique story and perspective on graduation:{Style.RESET_ALL}")
        
        char_list = list(CHARACTERS.keys())
        for i, char_id in enumerate(char_list, 1):
            char = CHARACTERS[char_id]
            print(f"\n{i}. {Fore.YELLOW}{char['name']}{Style.RESET_ALL}")
            print(f"   {char['description']}")
            print(f"   {Fore.BLUE}{char['background'][:80]}...{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Select character (1-{len(char_list)}): {Style.RESET_ALL}")
                choice_num = int(choice)
                if 1 <= choice_num <= len(char_list):
                    selected_char = char_list[choice_num - 1]
                    
                    # Show detailed character info
                    char = CHARACTERS[selected_char]
                    print(f"\n{Fore.GREEN}You selected: {char['name']}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}{char['background']}{Style.RESET_ALL}")
                    
                    confirm = input(f"\n{Fore.YELLOW}Confirm selection? (y/n): {Style.RESET_ALL}")
                    if confirm.lower() in ['y', 'yes']:
                        return selected_char
                else:
                    print(f"{Fore.RED}Please choose a number between 1 and {len(char_list)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Character selection cancelled.{Style.RESET_ALL}")
                return None
    
    def load_game(self):
        """Load an existing game"""
        saves = SaveManager.list_saves()
        
        if not saves:
            print(f"\n{Fore.YELLOW}No save files found.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.CYAN}Available Save Files:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        for i, save in enumerate(saves, 1):
            character_name = CHARACTERS.get(save['character'], {}).get('name', 'Unknown')
            playtime = self.format_playtime(save['playtime'])
            timestamp = save['timestamp'][:16] if save['timestamp'] != 'Unknown' else 'Unknown'
            
            print(f"{i}. {Fore.YELLOW}{character_name}{Style.RESET_ALL} - Chapter {save['chapter']}")
            print(f"   Time: {playtime} | Saved: {timestamp}")
        
        print(f"{len(saves) + 1}. {Fore.RED}Cancel{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Select save file (1-{len(saves) + 1}): {Style.RESET_ALL}")
                choice_num = int(choice)
                
                if choice_num == len(saves) + 1:
                    return False
                elif 1 <= choice_num <= len(saves):
                    selected_save = saves[choice_num - 1]
                    
                    self.game_state = SaveManager.load_game(selected_save['filename'])
                    if self.game_state:
                        self.story_engine = StoryEngine(self.game_state)
                        print(f"\n{Fore.GREEN}Game loaded successfully!{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"\n{Fore.RED}Failed to load save file.{Style.RESET_ALL}")
                        return False
                else:
                    print(f"{Fore.RED}Please choose a number between 1 and {len(saves) + 1}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                return False
    
    def view_save_files(self):
        """Display information about save files"""
        saves = SaveManager.list_saves()
        
        if not saves:
            print(f"\n{Fore.YELLOW}No save files found.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}Save File Details:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            for i, save in enumerate(saves, 1):
                character = CHARACTERS.get(save['character'], {})
                character_name = character.get('name', 'Unknown Character')
                playtime = self.format_playtime(save['playtime'])
                
                print(f"\n{i}. {Fore.YELLOW}{save['filename']}{Style.RESET_ALL}")
                print(f"   Character: {character_name}")
                print(f"   Progress: Chapter {save['chapter']}")
                print(f"   Playtime: {playtime}")
                print(f"   Last Saved: {save['timestamp'][:19] if save['timestamp'] != 'Unknown' else 'Unknown'}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def show_game_info(self):
        """Display game information and credits"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}About My Last Days Here")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Version: 2.0.0{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Part of the ChronoTale Collection{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Story Features:{Style.RESET_ALL}")
        print("• 10 unique characters with interconnected storylines")
        print("• Multiple character perspectives on graduation")
        print("• Probability-based optional scenes")
        print("• Multiple endings based on your choices")
        print("• Comprehensive save/load system")
        
        print(f"\n{Fore.YELLOW}Characters:{Style.RESET_ALL}")
        for char_id, char_data in CHARACTERS.items():
            print(f"• {char_data['name']} - {char_data['description']}")
        
        print(f"\n{Fore.GREEN}This game celebrates the emotional journey of")
        print("growing up, saying goodbye, and moving forward into")
        print(f"adulthood with hope and friendship.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def format_playtime(self, seconds: float) -> str:
        """Format playtime in readable format"""
        minutes = int(seconds // 60)
        hours = minutes // 60
        minutes = minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def play_story(self):
        """Main story playback loop"""
        if not self.game_state or not self.story_engine:
            print(f"{Fore.RED}No active game. Please start a new game or load a save.{Style.RESET_ALL}")
            return
        
        while self.game_state.current_chapter <= 7:
            try:
                # Play current chapter
                self.story_engine.play_chapter(self.game_state.current_chapter)
                
                # Check if player wants to save
                save_choice = input(f"\n{Fore.YELLOW}Would you like to save your progress? (y/n): {Style.RESET_ALL}")
                if save_choice.lower() in ['y', 'yes']:
                    if SaveManager.save_game(self.game_state):
                        print(f"{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Failed to save game.{Style.RESET_ALL}")
                
                # Continue to next chapter
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Game interrupted. Progress saved.{Style.RESET_ALL}")
                SaveManager.save_game(self.game_state, "autosave_interrupt.json")
                break
        
        # Game completed
        if self.game_state.current_chapter > 7:
            SaveManager.save_game(self.game_state, "completed_game.json")
    
    def run(self):
        """Main game loop"""
        self.show_title_screen()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':  # New Game
                if self.new_game():
                    self.play_story()
            elif choice == '2':  # Load Game
                if self.load_game():
                    self.play_story()
            elif choice == '3':  # View Save Files
                self.view_save_files()
            elif choice == '4':  # Game Information
                self.show_game_info()
            elif choice == '5':  # Exit
                print(f"\n{Fore.CYAN}Thank you for playing My Last Days Here!")
                print(f"Remember: every ending is a new beginning. ✨{Style.RESET_ALL}")
                break

def main():
    """Main entry point"""
    try:
        # Check launcher protection
        check_launcher()
        
        # Initialize and run game
        game = GameManager()
        game.run()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Thank you for playing My Last Days Here.")
        print(f"Take care of yourself. ❤️{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please report this issue if it persists.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
