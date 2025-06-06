#!/usr/bin/env python3
"""

My Last Days Here

"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from colorama import init, Fore, Style
import platform

# Enhanced colorama initialization based on environment
if platform.system() == "Windows":
    init(autoreset=True, convert=True, strip=False)
else:
    # For Unix-like systems, use different settings
    init(autoreset=True, convert=False, strip=None)

# Enhanced color management system
class ColorManager:
    """Enhanced color management with automatic fallback"""
    
    @staticmethod
    def is_color_supported() -> bool:
        """Check if terminal supports color output"""
        try:
            # Check if we're in a proper terminal
            if not sys.stdout.isatty():
                return False
            
            # Check environment variables
            term = os.environ.get('TERM', '').lower()
            if 'color' in term or 'xterm' in term or 'screen' in term:
                return True
                
            # Check for common color-supporting terminals
            if any(term.startswith(prefix) for prefix in ['xterm', 'screen', 'tmux', 'rxvt']):
                return True
                
            return False
        except (OSError, AttributeError, ValueError):
            return False
    
    @staticmethod
    def apply_color(text: str, color_code: str) -> str:
        """Apply color with automatic fallback"""
        if ColorManager.is_color_supported():
            try:
                return f"{color_code}{text}{Style.RESET_ALL}"
            except (AttributeError, ValueError, TypeError):
                return text
        return text
    
    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove ANSI color codes from text"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

# Global color manager instance
color_manager = ColorManager()

# Enhanced print functions with automatic color handling
def colored_print(text: str, color_code: str = "") -> None:
    """Print text with color support and automatic fallback"""
    if color_code and color_manager.is_color_supported():
        try:
            print(f"{color_code}{text}{Style.RESET_ALL}")
        except (AttributeError, ValueError, TypeError):
            print(text)
    else:
        print(color_manager.strip_ansi(text) if not color_manager.is_color_supported() else text)

def safe_format(text: str, color_code: str = "") -> str:
    """Format text with color codes that are safely handled"""
    if color_code and color_manager.is_color_supported():
        try:
            return f"{color_code}{text}{Style.RESET_ALL}"
        except (AttributeError, ValueError, TypeError):
            return text
    return color_manager.strip_ansi(text) if not color_manager.is_color_supported() else text

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
            
            # Ensure save_name is a valid string before processing
            if save_name is None or not isinstance(save_name, str):
                return None
                
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
        """Print text with typing effect and enhanced color handling"""
        import re
        
        # If colors aren't supported, strip ANSI codes and print normally
        if not color_manager.is_color_supported():
            clean_text = color_manager.strip_ansi(text)
            for char in clean_text:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()
            return
        
        # For color-supporting terminals, handle ANSI codes properly
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
        colored_print(f"\n{'='*60}", Fore.MAGENTA)
        colored_print("Chapter 1: The Weight of Yesterday", Fore.MAGENTA)
        colored_print(f"{'='*60}", Fore.MAGENTA)
        
        character = self.game_state.selected_character
        opening = CharacterStoryAdapter.get_character_opening(character)
        
        self.slow_print(f"\n{opening}")
        
        time.sleep(2)
        
        self.slow_print("\nThe silence in your room feels heavier tonight, weighted with the accumulated emotions of three transformative years. Your school uniform hangs ready for tomorrow's ceremony, but looking at it makes your chest tight with the realization that after graduation, you'll never wear it again. The fabric holds so many memories - first day nerves, exam anxiety, celebration after achievements, comfort during difficult times.")
        
        self.slow_print("\nTomorrow, everything changes. Tomorrow marks the end of the only home you've truly known during these formative years. The hallways that witnessed your growth, the classrooms where you discovered parts of yourself, the friendships that shaped your understanding of love and loyalty - all of it becomes memory.")
        
        self.slow_print("\nYou walk to your window and look out at the familiar neighborhood, knowing that even though the buildings will remain, your relationship with this place is ending forever. The person who returns here will be fundamentally different - no longer a student, no longer protected by the structure of school life, no longer surrounded by the same community that helped you become who you are today.")
        
        time.sleep(2)
        
        self.slow_print("\nMemories flood your mind unbidden, each one carrying emotional weight that threatens to overwhelm you. Some make you smile through tears, others stop your breath with their intensity. Tonight, in the quiet space between childhood's end and adulthood's beginning, they demand to be acknowledged.")
        
        memories = CharacterStoryAdapter.get_character_memories(character)
        
        self.slow_print("\nWhich memory threatens to break your heart with its beauty and finality tonight?")
        
        chosen_memory = self.make_choice(
            "What memory overwhelms you with emotion?",
            memories,
            1
        )
        
        # React to the chosen memory with profound emotional depth
        memory_reactions = {
            "graduation_memory": "The memory crashes over you like a tidal wave of realization. You can almost hear the echo of your younger self's voice on the first day, so eager and uncertain, so unaware of how profoundly this place would reshape your soul. Tears blur your vision as you understand that tomorrow doesn't just mark the end of school - it marks the death of the version of yourself who believed the future was limitless and time was endless. The weight of all those moments - the mundane Tuesday mornings, the stressful exam periods, the spontaneous laughter in hallways - suddenly feels precious beyond measure.",
            
            "tutoring_hina": "Your breath catches as you relive those quiet afternoons when academic help transformed into something deeper - a recognition of shared humanity. You remember the exact moment when her confused expression melted into understanding, how her eyes lit up with gratitude that went far beyond the subject matter. The vulnerability in those sessions, the way you both revealed parts of yourselves through patient explanation and humble learning, created a bond that felt sacred. Your heart aches with the bittersweet knowledge that such pure connections are rare gifts, and that saying goodbye to someone who saw your capacity for kindness feels like losing a piece of your identity.",
            
            "helping_hana": "The memory wraps around your heart like golden sunlight, bringing back the exact sensation of that moment when offering help felt like extending your hand across an invisible bridge. You can still see the relief and gratitude in her expression, feel the warm satisfaction of knowing your kindness made a real difference in someone's day. But now the memory carries the sharp edge of impermanence - the understanding that these spontaneous acts of care, these unplanned moments of human grace, belong to a specific time and place that's ending. The pain comes from realizing that the ecosystem of casual kindness you've all created together will scatter to the winds.",
            
            "sports_tournament": "The roar of the crowd fills your ears as if you're back on that field, surrounded by teammates who became family through shared sweat and determination. You can feel the adrenaline coursing through your veins, taste the sweet exhaustion of giving everything you had for a common goal. The memory is so vivid you can sense the weight of your teammates' arms around your shoulders, hear their breathless laughter, feel the electric connection of being part of something bigger than yourself. But now it feels like watching a beautiful movie of someone else's life, because that specific group of people, in that exact configuration of youth and hope and shared purpose, can never exist again.",
            
            "music_performance": "Your chest constricts with the memory of standing before an audience, your heart hammering against your ribs as fear transformed into something transcendent. You remember the hush that fell over the room, the way your voice or instrument became a bridge between your inner world and theirs, how sharing your art felt like offering pieces of your soul for judgment. But what overwhelms you now is the realization that it wasn't just a performance - it was a declaration of who you were becoming, witnessed by people who helped shape that becoming. The tears come because you understand that courage like that, witnessed by this specific community, was a gift you may never receive again.",
            
            "andrew_help": "The memory floods you with warmth and profound sadness as you remember the moment when language barriers dissolved into pure human connection. You can still see the mixture of relief and gratitude in his eyes when your kindness helped him navigate an unfamiliar world, feel the satisfaction of knowing that your empathy built a bridge across cultural differences. The pain comes from understanding that some friendships transcend every boundary - language, culture, geography, even goodbye - yet still must face the reality of physical separation. What breaks your heart is knowing that the version of yourself who could offer that help so naturally, in that specific context, is also saying farewell.",
            
            "hina_manga": "Your throat tightens as you remember the exact moment when someone looked past your carefully constructed exterior to see the real person underneath. The memory of sharing something deeply personal - your love for stories, your secret dreams, your unguarded enthusiasm - and having it received with genuine interest and understanding still makes your heart race. It was perhaps the first time you realized that being truly seen, not just looked at but actually seen and accepted, was both terrifying and essential to your growth. The tears come because such moments of authentic recognition are rare treasures, and you're saying goodbye to the person who witnessed your becoming.",
            
            "haruto_music": "The melody still echoes in your heart, but now it sounds like a lullaby for the end of innocence. You remember how music became a language when words felt inadequate, how harmony created understanding deeper than any conversation could reach. Those moments of creating beauty together, of finding connection through shared rhythm and melody, revealed parts of yourself you didn't know existed. The memory hurts because you're not just losing a friend - you're losing a collaborator in creating something beautiful, someone who understood that music could express what hearts couldn't speak aloud."
        }
        
        memory_key = chosen_memory[1] if chosen_memory and isinstance(chosen_memory, (list, tuple)) and len(chosen_memory) > 1 else ""
        reaction = memory_reactions.get(memory_key, "The memory pierces through you with the exquisite pain of time that cannot be reclaimed, carrying within it the bittersweet knowledge that some experiences are so perfect in their imperfection that they feel like compressed eternities, whole lifetimes contained within single heartbeats.")
        self.slow_print(f"\n{reaction}")
        
        self.slow_print("\nYou close your eyes and let yourself feel everything without resistance - the joy that bubbles up from your chest like champagne, effervescent and golden; the pain that sits heavy in your stomach like swallowed stones; the love that flows through your veins like warm honey, sweet and sustaining; the loss that echoes in your bones like the final note of a symphony, beautiful and final.")
        
        self.slow_print("\nTomorrow you'll be strong, composed, ready to walk across that stage and into whatever comes next. Tomorrow you'll smile for the cameras and celebrate with family and accept congratulations with grace. But tonight, in this sacred space between who you were and who you're becoming, you honor the magnitude of this transition by allowing yourself to grieve.")
        
        self.slow_print("\nYou understand now that nostalgia isn't just missing the past - it's mourning for the person you were when that past was your present, acknowledging that growth requires letting go, that becoming someone new means saying goodbye to who you used to be.")
        
        self.slow_print("\nThe tears that fall are not just for what you're leaving behind, but for the recognition that you have been profoundly loved, deeply shaped, irrevocably changed by this place and these people. You carry their influence forward like invisible treasure, knowing that while the external circumstances will change, the person they helped you become will endure.")
        
        self.display_stats()
    
    def chapter_2_friendship_reflections(self):
        """Chapter 2: The Bonds We've Built"""
        colored_print(f"\n{'='*60}", Fore.MAGENTA)
        colored_print("Chapter 2: The Bonds We've Built", Fore.MAGENTA)
        colored_print(f"{'='*60}", Fore.MAGENTA)
        
        self.slow_print("Your phone screen illuminates the darkness of your room like a beacon of human connection, buzzing insistently with messages from classmates scattered across the sprawling city, each one preparing for tomorrow's life-altering ceremony in their own unique way - some surrounded by family celebrations, others sitting alone with thoughts too complex for words, all united by the shared weight of this transition. The group chat that has been your emotional lifeline through grueling tests, joyous celebrations, unexpected crises, and the mundane daily rhythms that somehow became precious has never been more active than tonight, filled with a potent mixture of excitement and melancholy that mirrors the complex storm of emotions swirling in your own heart.")
        
        self.slow_print("\nAs you scroll through the seemingly endless flood of memories being shared - candid photos from school festivals where everyone looks impossibly young and carefree, inside jokes that make you laugh through unexpected tears, heartfelt promises to stay in touch that everyone desperately hopes will prove true despite knowing how difficult maintaining connections can be, late-night conversations about dreams and fears and the infinite possibilities of the future - you're struck by the profound realization that these relationships have been the invisible foundation upon which your entire understanding of yourself has been built. Each friendship has taught you something irreplaceable about the infinite varieties of love, the complexities of loyalty when it's tested by time and distance, the terrifying beauty of vulnerability when it's met with acceptance, and the quiet strength that comes from knowing you are truly known by others.")
        
        self.slow_print("\nSome connections were immediate and intense, like lightning strikes that illuminated hidden corners of your personality and revealed parts of yourself you didn't even know existed until someone else's understanding brought them into focus. Others grew slowly and quietly, like patient seeds that took months of shared experiences to sprout but eventually became the strongest, most resilient trees in your emotional landscape, providing shade and shelter through every season of your growth. A few were beautifully seasonal - intensely meaningful for a specific period or circumstance before naturally evolving into cherished memories that taught you that not all connections are meant to last forever, but all authentic connections leave permanent marks on the soul.")
        
        self.slow_print("\nBut tonight, as you face the stark reality of scattering like dandelion seeds to different universities in distant cities, different career paths that will consume your daily energy, different life trajectories that may never intersect again despite your best intentions, you understand with crystalline clarity that these relationships have been infinitely more than just companionship or social convenience. They've been transformative mirrors that showed you not just who you are, but who you could become if you had the courage to grow; they've been unshakeable support systems that held you up during the darkest times when your own strength felt insufficient; they've been safe laboratories where you learned the intricate, mysterious chemistry of human connection - how trust is built through countless small moments, how love can be expressed through teasing and silence and shared understanding, how forgiveness can heal wounds you didn't even know you were carrying.")
        
        self.slow_print("\nEach person in your circle brought out different facets of your personality, like turning a prism to catch light at new angles. With some friends you discovered your capacity for wild laughter that made your stomach hurt and tears stream down your face. With others you found depths of empathy you never knew you possessed, the ability to sit with someone's pain without trying to fix it, to offer presence as comfort. Some friendships taught you about healthy boundaries - when to give and when to protect your own energy. Others showed you the profound intimacy that can exist in shared silence, when words become unnecessary because understanding flows between you like an invisible current.")
        
        self.slow_print("\nThe group dynamics taught you about loyalty and jealousy, inclusion and the subtle cruelties of exclusion, how easily misunderstandings can fracture relationships and how healing requires both courage and humility. You learned that real friendship means celebrating someone else's success even when you're struggling, offering support without keeping score, and sometimes loving someone enough to tell them truths they don't want to hear. You discovered that being truly known - with all your flaws and fears and secret dreams exposed - is both terrifying and essential to genuine human connection.")
        
        relationships = CharacterStoryAdapter.get_character_relationships(self.game_state.selected_character)
        
        chosen_relationship = self.make_choice(
            "Which relationship has fundamentally shaped who you've become?",
            relationships,
            2
        )
        
        # Extended reflection based on relationship choice
        relationship_reflections = {
            "study_partnership": "The countless hours spent hunched over textbooks together created a bond forged in shared struggle and mutual support. You remember the way you learned to read each other's frustration levels, how to offer encouragement without being patronizing, how to celebrate small victories as if they were major triumphs. This relationship taught you that true partnership means showing up consistently, especially when the work is hard and the progress feels slow. The thought of studying alone in university fills you with unexpected loneliness.",
            
            "creative_collaboration": "Those moments of creating something beautiful together - whether art, music, writing, or performance - revealed depths of connection that ordinary conversation could never reach. You learned to trust someone else with your creative vulnerability, to build on each other's ideas without ego, to find harmony even when your styles were different. This relationship showed you that true artistic collaboration requires both individual authenticity and willingness to be changed by another person's vision. The silence your future creative projects will lack their input feels deafening.",
            
            "sports_teamwork": "The bond forged through shared physical challenges and collective goals taught you lessons about trust that extend far beyond any playing field. You learned to rely on others completely, to subordinate individual glory for team success, to push through exhaustion because others were counting on you. This relationship demonstrated that some forms of love are expressed through sweat, determination, and the willingness to literally have someone's back. The thought of competing without their presence feels like performing with half your strength.",
            
            "quiet_understanding": "This was the friendship of comfortable silences and shared glances that communicated volumes. You learned that profound connection doesn't always require constant conversation, that some people understand your heart without needing explanations. This relationship taught you the value of simply being present with another person, of offering your authentic self without pretense or performance. The future feels slightly more frightening knowing you're losing someone who could read your moods like a familiar book.",
            
            "adventurous_exploration": "Together you pushed boundaries, tried new experiences, and encouraged each other to step outside comfort zones that would have remained unchallenged alone. This relationship taught you that some of life's most meaningful moments happen when you're slightly scared but not alone, that growth often requires a trusted companion willing to jump into uncertainty with you. The thought of facing new challenges without their enthusiastic partnership makes the unknown feel more daunting.",
            
            "intellectual_sparring": "The hours of debate, discussion, and intellectual challenge sharpened your thinking and expanded your perspective in ways that no classroom could match. This relationship taught you to defend your ideas while remaining open to being wrong, to find excitement in having your assumptions challenged by someone who respected your intelligence. The future conversations you'll have without their brilliant counterpoints already feel less vibrant, less alive with possibility."
        }
        
        relationship_key = chosen_relationship[1] if chosen_relationship and isinstance(chosen_relationship, (list, tuple)) and len(chosen_relationship) > 1 else ""
        reflection = relationship_reflections.get(relationship_key, "This relationship taught you something essential about the human capacity for connection, about how we shape each other simply by caring, simply by showing up, simply by choosing to see and be seen.")
        self.slow_print(f"\n{reflection}")
        
        self.slow_print("\nYou close your eyes and let the full weight of gratitude wash over you. These friendships haven't just entertained you or comforted you - they've fundamentally altered your understanding of what it means to be human. You've learned that love comes in countless forms, that loyalty can be quiet or fierce, that some people enter your life and leave you irrevocably changed.")
        
        self.slow_print("\nThe fear of losing these connections battles with the knowledge that what you've built together has already changed you permanently. Distance may alter the frequency of your interactions, but it cannot erase the ways these relationships have shaped your capacity for love, your understanding of friendship, your appreciation for the rare gift of being truly known by another person.")
        
        time.sleep(2)
        self.display_stats()
    
    def chapter_3_future_plans(self):
        """Chapter 3: What Comes Next"""
        colored_print(f"\n{'='*60}", Fore.MAGENTA)
        colored_print("Chapter 3: What Comes Next", Fore.MAGENTA)
        colored_print(f"{'='*60}", Fore.MAGENTA)
        
        self.slow_print("Your desk is scattered with the tangible, overwhelming manifestations of infinite possibility - crisp acceptance letters bearing prestigious university seals that represent years of academic validation, job application confirmations from companies that could launch your professional life in directions you never imagined, colorful brochures for gap year programs promising adventure and self-discovery in foreign countries, scholarship offers with dollar amounts that could fundamentally alter your family's financial trajectory and lift generational burdens from your shoulders. Each piece of paper represents not merely an opportunity or a career path, but a completely different version of who you might become, a different story you might live, a different person you might discover yourself to be when tested by new circumstances and challenges.")
        
        self.slow_print("\nTomorrow marks not just the ceremonial end of high school, but the last precious moment when all these radically different futures feel equally possible, when you can still imagine yourself succeeding in any direction, when the weight of choice hasn't yet collapsed the quantum superposition of your potential into a single reality. Once you commit to your chosen path, all the other possibilities will fade from vibrant potential into either sources of lifelong regret or profound relief that you escaped their particular challenges. The overwhelming weight of deciding not just what you want to do with your life, but fundamentally who you want to become as a human being - what values will guide you, what dreams will sustain you, what compromises you're willing to make - sits heavy on your shoulders like an invisible crown of responsibility.")
        
        self.slow_print("\nYou think about the countless conversations with parents whose love manifests as worry, who want security and stability for you because they've seen how cruel and unpredictable the world can be to dreamers; with teachers who recognized potential in you that you're still not entirely sure you possess, who spoke of futures that seemed impossible until they believed in you; with friends who are making choices that appear so much clearer and more confident than your own, though you suspect many of them are just as terrified and uncertain as you are beneath their carefully constructed facades of certainty. Everyone in your life has offered advice, opinions, and expectations, but ultimately this decision belongs to you alone in the most profound and terrifying sense - the person you become through this choice will have to live with its consequences for decades to come.")
        
        self.slow_print("\nSome paths promise the comfort of stability and predictable success but might slowly crush parts of your soul you're just beginning to discover, leaving you financially secure but spiritually hollow. Others offer the intoxicating chance to follow dreams and passions that might prove impossible to sustain in a world that often punishes artistic ambition with poverty and irrelevance. Still others represent careful compromises that could either be demonstrations of wise pragmatism and emotional maturity, or acts of devastating cowardice that you'll regret for the rest of your life - and you won't know which until years from now when it's far too late to change course.")
        
        future_choices = [
            ("Follow your creative passions despite the uncertainty", "creative_path", {"excitement": 20, "confidence": 15}),
            ("Choose security and practical career prospects", "practical_path", {"confidence": 15, "nostalgia": 10}),
            ("Stay close to home and the people you love", "local_path", {"friendship": 25, "nostalgia": 15}),
            ("Embrace adventure and the complete unknown", "adventure_path", {"excitement": 25, "confidence": 10}),
            ("Take time to explore before committing to anything", "discovery_path", {"nostalgia": 20, "confidence": 5})
        ]
        
        chosen_future = self.make_choice(
            "What path calls to your deepest, truest self?",
            future_choices,
            3
        )
        
        # Extended path reactions with deeper emotional content
        path_reactions = {
            "creative_path": "The decision crystallizes in your chest like something clicking into place. You feel a surge of terrifying, exhilarating determination to follow your artistic passions, whatever the financial risk, whatever the skepticism of others. You understand that some dreams are too important to abandon for safety, that your creative voice might be exactly what the world needs. The fear of failure feels less powerful than the fear of never trying, of wondering 'what if' for the rest of your life. You choose to bet on yourself, on your talent, on the possibility that passion can become profession if you're willing to work harder than anyone expects.",
            
            "practical_path": "There's profound comfort in choosing security, even if it means temporarily setting aside some dreams. You recognize that stability can be its own form of freedom - the freedom from financial anxiety, from uncertainty, from the pressure to constantly prove yourself. This choice doesn't feel like giving up; it feels like being responsible, like honoring the sacrifices others have made for your education. You can pursue creativity as a meaningful hobby while building a career that allows you to help others, to contribute to society, to sleep peacefully at night knowing you can take care of yourself and eventually your loved ones.",
            
            "local_path": "The thought of maintaining these precious friendships, of staying connected to the community that shaped you, fills you with warmth and certainty. You've learned that geography isn't destiny - you can find adventure and growth while remaining rooted in relationships that matter. This choice feels like honoring what you've built while trusting that the right opportunities will find you here. Distance doesn't necessarily equal growth, and staying doesn't necessarily equal stagnation. You choose love over ambition, connection over achievement, and that feels like wisdom rather than limitation.",
            
            "adventure_path": "Your heart races with excitement about discovering who you could become when stripped of everything familiar. The unknown stops feeling frightening and starts feeling like the only honest choice for someone your age. You understand that this might be your only chance to be completely selfish, to prioritize discovery over security, to say yes to experiences that will never be available again. The possibility of failure feels less important than the certainty of growth. You choose courage over comfort, trusting that you're strong enough to handle whatever comes, that the person you'll become through adventure will be worth the risks you're taking now.",
            
            "discovery_path": "Sometimes the wisest choice is admitting you need more time to grow into the person capable of making such important decisions. This isn't procrastination; it's self-awareness. You recognize that rushing into commitments when you're still figuring out your values, your interests, your capacity for different kinds of work and lifestyle, could lead to choices you'll regret for decades. Taking time to explore, to volunteer, to travel, to work different jobs, to simply exist without the pressure of five-year plans - this feels like the most honest response to the magnitude of the decision before you."
        }
        
        future_key = chosen_future[1] if chosen_future and isinstance(chosen_future, (list, tuple)) and len(chosen_future) > 1 else ""
        reaction = path_reactions.get(future_key, "The decision settles into your bones with the quiet certainty of truth. This choice feels aligned with something essential in your nature, something that transcends logic or other people's expectations. You trust yourself to make it work.")
        self.slow_print(f"\n{reaction}")
        
        self.slow_print("\nAs you make peace with your choice, you feel something shift inside you - the transition from student to adult, from someone whose path is determined by others to someone who must forge their own way. The fear remains, but it's accompanied by excitement, by pride in your courage to choose authentically rather than safely.")
        
        self.slow_print("\nYou understand that this decision doesn't lock you into a single future forever. Paths can be changed, dreams can evolve, new opportunities will arise. But choosing consciously, based on who you are right now and what matters most to you, feels like the first real act of adulthood.")
        
        self.display_stats()
    
    def chapter_4_final_preparations(self):
        """Chapter 4: The Last Evening"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 4: The Last Evening")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("Your graduation outfit hangs ready in your closet like a costume for the most important performance of your life - carefully chosen, meticulously prepared, representing the person you want to appear to be when you cross that stage. Your speech, if you're giving one, has been practiced until the words feel smooth on your tongue, though you know the emotion of the moment might make them catch in your throat anyway. Your yearbook sits heavy on your desk, filled with signatures and messages that range from silly inside jokes to profound declarations of friendship, each one a small time capsule of how others see you and want to be remembered by you.")
        
        self.slow_print("\nBut despite all the official preparations, all the ceremonial readiness, there's still something deeper calling to you - one last meaningful act before tomorrow transforms everything forever. This evening feels sacred, pregnant with the weight of transition, and you want to honor it with intention rather than letting it slip away in nervous busy-work or mindless distraction. This is your last night as a high school student, your final hours in this identity you've worn for three transformative years.")
        
        self.slow_print("\nThe apartment feels different tonight - charged with anticipation and melancholy, as if the walls themselves understand that tomorrow will mark the end of an era. Your family moves around you with unusual gentleness, sensing the magnitude of this transition even if they can't fully comprehend the emotional complexity of what you're experiencing. There's so much you want to preserve, so many feelings you want to process, so many people you want to reach out to one final time.")
        
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
        
        # Add reflection based on preparation choice
        preparation_key = chosen_preparation[1] if chosen_preparation and isinstance(chosen_preparation, (list, tuple)) and len(chosen_preparation) > 1 else ""
        preparation_reflections = {
            "letters": "Writing heartfelt letters to your closest friends feels like the most meaningful way to honor these relationships.",
            "time_capsule": "Creating a time capsule helps you preserve these precious memories for the future.",
            "family_call": "Sharing your feelings with family strengthens the bonds that will support you through this transition.",
            "school_walk": "Walking through the empty school corridors one last time feels like a sacred farewell ritual.",
            "organization": "Preparing your space for the future helps you feel ready for what comes next."
        }
        
        reflection = preparation_reflections.get(preparation_key, "This final evening activity helps you process the magnitude of tomorrow's transition.")
        self.slow_print(f"\n{reflection}")
        
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
        
        # Add reflection based on graduation moment choice
        moment_key = chosen_moment[1] if chosen_moment and isinstance(chosen_moment, (list, tuple)) and len(chosen_moment) > 1 else ""
        moment_reflections = {
            "pride_focus": "The pride swelling in your chest feels overwhelming - pride in yourself, your classmates, and everything you've accomplished together.",
            "sadness_embrace": "Tears blur your vision as the weight of this ending settles in. This sadness is beautiful because it represents how much these years have meant.",
            "future_excitement": "Your heart races with anticipation for what comes next. The future feels bright and full of infinite possibilities.",
            "mindful_presence": "You breathe deeply and let yourself fully experience this singular moment - the sounds, the emotions, the sense of completion."
        }
        
        reflection = moment_reflections.get(moment_key, "This graduation moment fills you with complex emotions that will stay with you forever.")
        self.slow_print(f"\n{reflection}")
        
        self.slow_print("\nThe principal's voice echoes through the auditorium as names are called one by one, each pronunciation carrying the weight of recognition for three years of struggle, growth, and transformation. Some names are mispronounced, drawing gentle laughter that breaks the tension; others are called with perfect clarity, as if the speaker understands the magnitude of this moment for each individual student. You watch your classmates rise from their seats and walk across the stage - some confident and beaming, others visibly nervous, a few fighting back tears, all of them forever changed by this ritual of passage.")
        
        self.slow_print("\nEach step across that stage represents not just academic achievement, but the accumulation of countless moments that shaped these young adults - late nights studying for exams that seemed impossible, friendships forged in the crucible of adolescent drama, heartbreaks that felt like the end of the world but became lessons in resilience, small victories that built confidence brick by brick, failures that taught humility and perseverance. The diploma is just paper, but what it represents is the transformation of children into adults ready to face an uncertain world with courage, compassion, and the knowledge that they are capable of more than they ever imagined.")
        
        self.slow_print("\nWhen your name is finally called, the world narrows to this single moment - the walk across the stage feeling both eternal and instantaneous, the handshake with the principal somehow containing all the pride and hope of everyone who helped you reach this point, the diploma in your hands surprisingly heavy with possibility and responsibility. The applause washes over you like a wave of love and recognition, and for just this moment, you feel held by an entire community that believes in your potential to make the world better simply by being in it.")
        
        self.display_stats()
    
    def chapter_6_farewells(self):
        """Chapter 6: Saying Goodbye"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 6: Saying Goodbye")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("After the ceremony concludes and the formal pomp and circumstance gives way to organic human connection, everyone gathers in the courtyard and hallways for the real graduation - the photos that will live in frames and hearts for decades, the hugs that try to compress three years of shared experience into a single embrace, the final conversations that attempt to capture everything you've meant to each other in words that suddenly feel inadequate. The reality of separation is setting in with the weight of approaching thunderclouds, but so is a profound appreciation for everything you've shared - not just the big moments that will make it into speeches and yearbooks, but the countless small interactions that wove your lives together into something beautiful and irreplaceable.")
        
        self.slow_print("\nThe air vibrates with a unique mixture of celebration and heartbreak that only exists at graduations - joy for what's been accomplished, excitement for what lies ahead, and grief for what's ending. You look around at faces you've seen every day for years, suddenly precious because soon they'll become memories you'll struggle to keep vivid. Every laugh feels more valuable, every shared glance carries extra weight, every moment of connection becomes something to treasure because you don't know when - or if - you'll experience this particular configuration of souls together again.")
        
        self.slow_print("\nParents and families orbit around the edges of your group, taking photos and offering congratulations, but they can't quite penetrate the invisible bubble of teenage emotion that surrounds you and your classmates. This is your moment, your goodbye, your transition - and while their love and pride mean everything, only you understand the specific texture of loss and hope that defines this experience. The ceremony was for them; this gathering is for you.")
        
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
        
        # Add reflection based on farewell choice
        farewell_key = chosen_farewell[1] if chosen_farewell and isinstance(chosen_farewell, (list, tuple)) and len(chosen_farewell) > 1 else ""
        farewell_reflections = {
            "group_photo": "The group photo becomes a sacred ritual of preservation - herding everyone together despite their scattered conversations, arranging heights and positions with the unconscious choreography of people who know each other's bodies and personalities intimately. The camera clicks multiple times because someone always blinks or looks away at the crucial moment, but that just means more attempts to capture the perfect essence of this imperfect, beautiful group. When you finally get the shot where everyone is genuinely laughing - not posing, but truly joyful - you know you've created a visual time capsule that will sit on desks and walls for decades, a tangible reminder that once upon a time, this exact configuration of souls existed in perfect harmony.",
            
            "individual_talks": "These one-on-one conversations become the most precious part of the entire day - pulling friends aside for the kinds of intimate exchanges that can only happen when the noise of group dynamics fades away. You find yourself saying things you've thought but never voiced, hearing confessions and appreciations that surprise you with their depth and vulnerability. These talks reveal the specific ways each friendship has shaped you, the particular qualities you'll miss most about each person, the promises to stay in touch that feel genuinely achievable because they're rooted in real understanding rather than generic sentiment. Each conversation feels like a small ceremony of acknowledgment - recognizing what you've meant to each other and blessing the connection to survive the test of distance and time.",
            
            "stay_connected": "The exchange of contact information becomes surprisingly emotional as you realize how much intention will be required to maintain these relationships that have been sustained by proximity and routine for so long. Creating group chats, sharing social media handles, writing down addresses that might change but represent current realities - each piece of information exchanged feels like a small act of faith in the future. The concrete planning of reunions, the promises to visit each other at universities, the scheduling of video calls - these practical arrangements become deeply meaningful because they represent the transition from passive friendship to active commitment, from relationships maintained by circumstance to connections sustained by choice.",
            
            "gift_giving": "The small gifts you prepared - handwritten letters, friendship bracelets, photos you printed and wrote messages on the back, mixtapes or playlists that capture your shared memories - become vessels for emotions too complex for words alone. Watching each person's face as they unwrap these tokens of affection, seeing them understand that you thought of them specifically, individually, while preparing for this moment, creates a circuit of love that flows both ways. These tangible reminders will outlast the graduation ceremony itself, becoming treasured artifacts that can be touched and held when memory alone feels insufficient to bridge the distance between past and future.",
            
            "natural_flow": "Simply being present in the moment without forcing structure or sentiment allows the organic beauty of these connections to shine through authentically. You move through the gathering like water, participating in conversations as they arise naturally, joining in laughter that bubbles up spontaneously, offering hugs that happen when they're genuinely needed rather than because protocol demands them. This approach creates space for the unexpected moments that often become the most treasured memories - someone's spontaneous joke that has everyone doubled over with laughter, a quiet moment of eye contact that communicates everything without words, the way the group naturally gravitates together and apart like a gentle dance of affection and independence."
        }
        
        reflection = farewell_reflections.get(farewell_key, "These final moments together feel both precious and bittersweet.")
        self.slow_print(f"\n{reflection}")
        
        self.slow_print("\nAs the day winds down and the golden afternoon light begins to fade into the soft purple of early evening, you realize with a clarity that takes your breath away that while this particular chapter is ending - this daily shared existence, this routine intimacy, this easy access to the people who have become extensions of your own heart - the story of your friendships will continue in new and unexpected ways. The relationships you've built are strong enough to survive transformation, flexible enough to adapt to distance, deep enough to transcend the superficial changes that geography and time will inevitably bring.")
        
        self.slow_print("\nYou understand now that love doesn't require proximity to survive, that true friendship is measured not in frequency of contact but in the willingness to show up when it matters, in the ability to pick up conversations as if no time has passed, in the knowledge that somewhere in the world there are people who carry pieces of your story in their hearts. The fear of losing these connections begins to transform into gratitude for having experienced them at all, into trust that what you've built together has already changed you permanently in ways that distance cannot undo.")
        
        self.slow_print("\nThe goodbye hugs feel different now - not like endings, but like seeds being planted in soil that will nurture connection across whatever distances the future creates. You're not just saying goodbye to people; you're graduating these relationships from the safe cocoon of shared daily life into the more challenging but ultimately more meaningful realm of chosen connection, where love persists because it chooses to, not because circumstance makes it convenient.")
        
        self.display_stats()
    
    def chapter_7_new_beginnings(self):
        """Chapter 7: Moving Forward"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}Chapter 7: New Beginnings")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.slow_print("A week has passed since graduation, and the world feels fundamentally different in ways both subtle and profound. Your room looks like a museum of transition - some belongings carefully packed away in boxes labeled for storage or donation, others deliberately set out for your new life like artifacts of intention and hope. The graduation cap sits on your dresser, already gathering dust but still radiating the energy of that transformative moment when you walked across the stage and into uncertainty.")
        
        self.slow_print("\nYour phone buzzes with a text from a classmate sharing their first day at their new job or college, complete with photos that show them looking simultaneously excited and terrified in unfamiliar environments. The message carries that particular mixture of bravado and vulnerability that defines this period - everyone trying to appear confident about choices that feel impossibly large, sharing updates that are equal parts celebration and plea for validation that they're doing the right thing.")
        
        self.slow_print("\nYou realize this is how it will be now - connections maintained through deliberate effort rather than daily proximity, relationships sustained by intention rather than convenience. The easy intimacy of shared hallways and lunch tables has been replaced by scheduled phone calls and carefully composed messages. It's not worse, necessarily, but it's undeniably different, requiring new skills and deeper commitment to keep the bonds you've built from gradually dissolving in the acid of distance and time.")
        
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
        
        # Add reflection based on beginning choice
        beginning_key = chosen_beginning[1] if chosen_beginning and isinstance(chosen_beginning, (list, tuple)) and len(chosen_beginning) > 1 else ""
        beginning_reflections = {
            "enthusiastic_sharing": "Your enthusiastic response reveals the genuine excitement bubbling beneath your surface uncertainty - you discover that you actually want to share your new experiences, to maintain these vital connections that have sustained you through the most formative period of your life. The act of composing your reply becomes a small celebration of growth, an acknowledgment that you're becoming someone new while honoring the relationships that helped shape that becoming. You realize that staying connected doesn't mean clinging to the past; it means carrying the best parts of your shared history forward into whatever adventures await.",
            
            "grateful_connection": "The wave of gratitude that washes over you feels almost overwhelming in its intensity - gratitude not just for these specific friends reaching out, but for the entire ecosystem of care and connection that you've all created together over these years. You understand with sudden clarity that the simple act of a classmate thinking to share their first-day experiences with you represents something precious and rare in a world that often feels disconnected and superficial. These continuing friendships remind you that love takes many forms, that some of the most meaningful relationships in your life began with shared homework struggles and evolved into bonds that transcend geography and circumstance.",
            
            "growth_realization": "Looking at your friend's photos and updates, you're struck by how much everyone has already transformed in just one week - new environments bringing out different facets of their personalities, new challenges revealing reserves of strength and adaptability none of you knew you possessed. The recognition of this collective growth fills you with a complex mixture of pride, excitement, and poignant nostalgia for who you all were just days ago. You realize that growing up doesn't mean leaving your friends behind; it means growing alongside them, celebrating the people they're becoming while cherishing the memories of who you were together.",
            
            "reunion_planning": "The impulse to plan a reunion springs from a deep understanding that some connections are too precious to leave to chance, that maintaining these friendships will require intention and effort but is worth every ounce of energy you can devote to it. As you start texting about dates and locations, you realize you're not just planning a gathering - you're committing to the ongoing work of love, to showing up for people even when it's inconvenient, to prioritizing relationships that have shaped your understanding of what it means to be human. The excitement of imagining everyone together again, sharing stories of their new adventures while reconnecting with the shared foundation of your high school years, feels like the perfect bridge between past and future."
        }
        
        reflection = beginning_reflections.get(beginning_key, "This response to your classmates shows how you're handling this transition into your new life.")
        self.slow_print(f"\n{reflection}")
        
        self.slow_print(f"\nAs {CHARACTERS[self.game_state.selected_character]['name']}, you've learned through this profound experience of transition that graduation isn't really an ending in any meaningful sense - it's a metamorphosis, a transformation as complete and necessary as a butterfly emerging from its chrysalis, forever changed by the process but carrying within its new form all the essential elements that made its previous existence meaningful. The friendships that sustained you through adolescent uncertainty, the lessons learned through both triumph and failure, the memories that feel simultaneously like yesterday and a lifetime ago - all of these have become integral parts of your identity, woven so thoroughly into the fabric of who you are that they'll continue to influence every choice, every relationship, every moment of courage or compassion in the journey ahead.")
        
        self.slow_print("\nYou understand now that growing up doesn't mean abandoning the past or betraying the person you used to be - it means integrating all your experiences into a richer, more complex understanding of what it means to be human. The shy moments and confident ones, the times you succeeded and the times you failed spectacularly, the friendships that lifted you up and the conflicts that taught you about forgiveness - all of it becomes part of your story, part of your strength, part of your capacity to face whatever challenges and opportunities await in the vast, uncertain, beautiful world beyond these familiar walls.")
        
        self.slow_print("\nThe future stretches before you like an unwritten book, its pages blank with possibility but its foundation solid with everything you've learned about love, loyalty, resilience, and hope. You're ready not because you have all the answers, but because you've learned how to ask the right questions, how to seek help when you need it, and how to trust in your own capacity to grow and adapt and become whoever you're meant to be.")
        
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
            self.slow_print(f"\n{Fore.CYAN}You're walking through the ancient, hallowed halls of Oxford University, your black student robes billowing behind you as you navigate between centuries-old stone walls that have witnessed the education of prime ministers, poets, and pioneers. The dreaming spires that pierce the English sky remind you constantly of the modest school building in Japan where you first discovered who you could become when stripped of everything familiar and forced to rebuild your identity from the ground up. Your study abroad application essay about 'Finding Home in a Foreign Land' - written with tears streaming down your face as you poured your heart onto the page - was what ultimately secured your place in this prestigious institution, but you know the real education happened in those Japanese classrooms where you learned that courage isn't the absence of fear, but the decision to grow despite it.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}Your cramped dormitory room tells the story of a young man caught between two worlds but belonging fully to both - the wall above your narrow bed is covered with photos from your Japanese graduation ceremony, each one carefully printed and arranged like a shrine to the most transformative year of your life. Rei's candid shots capture moments you didn't even know were being photographed: you laughing so hard at one of Sato's jokes that you're doubled over with tears in your eyes, the concentrated expression on your face as Hina helped you with calligraphy, the pure joy radiating from your smile during the sports festival when Kazuha's team invited you to join their victory celebration. When your British roommate asks about these photos with genuine curiosity, you find yourself smiling as you begin to tell the story of the year that didn't just change your life but fundamentally altered your understanding of what it means to be human.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As Andrew, you've learned through the profound alchemy of displacement and acceptance that home isn't determined by geography or genetics - it's discovered in the places where you're challenged to become the best version of yourself, where people see your potential even when you can't see it yourself, where love transcends language barriers and cultural differences. Oxford will provide you with the intellectual tools and international perspective to bridge cultures professionally, but your Japanese classmates already gave you something infinitely more valuable - the emotional intelligence and cross-cultural empathy that will allow you to help other displaced souls find their place in an increasingly connected but often alienating world, just as they helped you find yours in the most unexpected of places.{Style.RESET_ALL}")
        
        elif character_ending["path"] in ["university", "arts_university", "local_university", "university_athletic"]:
            self.slow_print(f"\n{Fore.CYAN}You're walking across your university campus in the crisp morning air, your backpack heavy with textbooks that smell of possibility and dreams that feel more tangible with each passing day. The familiar weight of academic responsibility feels different now - not like a burden imposed by others, but like a path you've consciously chosen, a tool you're actively using to build the future you envision for yourself. The acceptance letter that arrived months ago is still pinned to your bedroom wall at home, its creased edges and slightly faded ink serving as a daily reminder of how far you've traveled from the uncertain, anxious student who worried about not being good enough to the confident young adult who has learned that growth happens not despite your fears, but because you choose to act in spite of them.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}{character_ending['university']}{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As {character_name}, you've consciously chosen the path of continued learning and intentional growth, understanding that education isn't just about acquiring knowledge but about developing the critical thinking skills, creative problem-solving abilities, and emotional intelligence that will serve you throughout your life. The friendships forged during those intense final weeks of high school have not only remained strong despite the geographical distances and different academic pressures, but have actually deepened as you've all learned to maintain connections through deliberate effort rather than simple proximity. Your shared experiences of transition, uncertainty, and discovery continue to shape who you're becoming, providing a foundation of mutual understanding and support that makes even the most challenging university experiences feel manageable because you know you're not facing them alone.{Style.RESET_ALL}")
        
        else:  # Career/gap year paths
            self.slow_print(f"\n{Fore.CYAN}You're getting ready for another day in your new life, one that deliberately doesn't involve the familiar rhythms of textbooks, lecture halls, or academic deadlines that defined your existence for so many years. Instead, you're pursuing your passion with the raw immediacy of someone who has chosen to learn through direct experience rather than theoretical study, diving headfirst into the real world with all its unpredictable challenges and unexpected rewards. Your morning routine feels both liberating and slightly terrifying - no assignments to complete, no grades to worry about, just the vast open space of possibility where your success depends entirely on your willingness to work hard, adapt quickly, and trust in your own developing instincts about what feels right and meaningful.{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.WHITE}{character_ending.get('career', character_ending.get('university', 'You are following your own unique path that defies conventional expectations but honors your authentic desires and natural talents.'))}{Style.RESET_ALL}")
            
            self.slow_print(f"\n{Fore.GREEN}As {character_name}, you've made the courageous decision to trust your instincts and follow your heart even when that path looks different from what others expected or recommended, understanding that sometimes the most meaningful growth happens when you're willing to forge your own trail rather than following well-worn routes that others have traveled before you. The interpersonal skills, emotional resilience, and deep capacity for connection that you developed during those transformative high school years provide an unshakeable foundation that allows you to build something uniquely yours - a life and career that reflects your authentic values, natural talents, and genuine passion rather than external expectations or societal pressure to conform to traditional definitions of success.{Style.RESET_ALL}")
        
        # Common ending note about friendship
        self.slow_print(f"\n{Fore.YELLOW}Your phone buzzes insistently with a new message in the group chat you all created during those emotional final hours after graduation ceremony, and despite the fact that everyone has scattered to dramatically different paths - some immersed in rigorous university coursework, others diving headfirst into demanding career opportunities, still others taking gap years to explore and discover themselves - the bonds you formed during those intense final days of high school have not only remained unbroken but have actually grown stronger through the deliberate effort required to maintain them across distance and different life circumstances. The message thread shows photos from everyone's new adventures: dorm room setups with familiar faces grinning behind stacks of textbooks, first-day-of-work selfies with nervous but excited expressions, travel photos from gap year adventures that make everyone simultaneously envious and proud, each image accompanied by updates that feel like letters from parallel universes where your friends are becoming the people they always had the potential to be.{Style.RESET_ALL}")
        
        self.slow_print(f"\n{Fore.MAGENTA}You understand now with crystal clarity that some stories do end with graduation - the story of who you were when you were defined primarily by your role as a student, when your identity was shaped by classes and grades and the particular social ecosystem of high school life. But your story - the deeper story of who you are becoming as a conscious, intentional human being capable of love, growth, creativity, and positive impact on the world - is just beginning to unfold in ways that will surprise and challenge and inspire you for decades to come. The foundation has been laid; now comes the thrilling, terrifying, beautiful work of building a life that honors both your dreams and your values, your individual ambitions and your commitment to the people who helped shape your understanding of what it means to be truly alive.{Style.RESET_ALL}")
        
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
        
        print(f"\n{Fore.WHITE}A deeply emotional journey through the final, irreplaceable moments of")
        print("childhood's end, where every goodbye carries the accumulated weight of")
        print("three transformative years filled with shared dreams that felt infinite,")
        print("laughter that echoed through hallways and hearts, tears that taught you")
        print("the complexity of human connection, and friendships that redefined your")
        print("understanding of love, loyalty, and what it means to truly belong.")
        print(f"These last days will change everything forever.{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💫 Story Theme: Experience the profound beauty and exquisite")
        print("heartbreak of growing up in real time, saying farewell to the people")
        print("who shaped your identity and held your heart, while stepping bravely")
        print("into an uncertain future that promises both loss and limitless possibility.")
        print("This is a story about the courage required to let go of who you were")
        print(f"in order to become who you're meant to be.{Style.RESET_ALL}")
    
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
