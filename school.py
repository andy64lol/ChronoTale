import random
import time
import json
import os
import platform
import re
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

# Enhanced setup for colorama to ensure colors work in various environments
os.environ["FORCE_COLOR"] = "1"  # Force colors in environments like Replit
os.environ["TERM"] = os.environ.get("TERM", "xterm-256color")  # Set terminal type if not defined

# Check if we're running in Replit environment
if "REPL_ID" in os.environ or "REPLIT_ENVIRONMENT" in os.environ:
    os.environ["REPLIT_ENVIRONMENT"] = "true"
    # For Replit, don't do character-by-character printing
    init(autoreset=False, strip=False)
# Optimized colorama configuration based on platform
elif platform.system() == "Windows":
    init(autoreset=True, convert=True)
else:
    init(autoreset=False, strip=False)  # Don't auto-reset for better color control

# Game Settings
game_settings = {
    "allow_nsfw": False,  # Controls mature/explicit content
    "allow_bullying": False,  # Controls bullying events and interactions
    "allow_cuss_words": False,  # Controls language filter
    "allow_cross_family_love": False,  # Controls romantic options with step-siblings/family
    "nsfw_level": "low",  # none, low, medium, high - Controls the detail level of NSFW content
    "cross_family_romance_type": "none",  # none, step, all - Controls which family relationships can be romantic
    "difficulty": "normal",  # easy, normal, hard
    "text_speed": "normal",  # slow, normal, fast
    "enable_cheats": False,  # Enable cheat commands
    "show_tutorial": True,  # Show tutorial hints
}

# Character Name Lists
male_first_names = [
    "Haruki", "Kenji", "Akira", "Daichi", "Ryo", "Kenta", "Sora", "Yuki", "Takeshi", "Hiroshi", 
    "Kazuki", "Haru", "Takumi", "Hayato", "Tsubasa", "Kaito", "Haruto", "Minato", "Ren", "Sota", 
    "Yuto", "Yusei", "Shota", "Jin", "Tatsuya", "Kosei", "Ryota", "Eiji", "Yuji", "Naoki", 
    "Kazuya", "Shinichi", "Taro", "Takuya", "Shota", "Kohei", "Shun", "Daisuke", "Yuma", "Kosuke"
]

female_first_names = [
    "Emi", "Mika", "Yuna", "Kaori", "Hana", "Sakura", "Rei", "Yuki", "Aiko", "Midori", 
    "Yui", "Hinata", "Haruka", "Aoi", "Akane", "Misaki", "Nao", "Ayaka", "Nanami", "Rin", 
    "Mio", "Saki", "Karin", "Ai", "Yuna", "Kokoro", "Miyu", "Hina", "Sora", "Ichika", 
    "Mai", "Kotone", "Risa", "Ayane", "Kana", "Yuka", "Reina", "Maya", "Momoka", "Yuzuki"
]

last_names = [
    "Takahashi", "Yamamoto", "Kobayashi", "Tanaka", "Sasaki", "Fujimoto", "Hoshino", "Shimizu", 
    "Nakamura", "Suzuki", "Sato", "Kato", "Ito", "Watanabe", "Yamada", "Matsumoto", "Inoue", 
    "Kimura", "Hayashi", "Saito", "Yamaguchi", "Nakajima", "Matsui", "Ikeda", "Yoshida", 
    "Yamashita", "Sasaki", "Yamazaki", "Ogawa", "Ishikawa", "Maeda", "Hasegawa", "Murata", 
    "Kobayashi", "Kojima", "Kondo", "Ishii", "Abe", "Harada", "Fujita", "Aoki", "Hashimoto", 
    "Okada", "Sakamoto", "Mori", "Endo", "Fukuda", "Goto", "Nishimura", "Takagi"
]

# More diverse international student names
international_first_names = [
    "Li", "Wei", "Chen", "Ming", "Jing",  # Chinese
    "Kim", "Park", "Lee", "Choi", "Jung",  # Korean
    "John", "Emma", "Michael", "Olivia", "William",  # Western
    "Raj", "Priya", "Arun", "Divya", "Vikram",  # Indian
    "Maria", "Carlos", "Ana", "Miguel", "Sofia",  # Latino
    "Ahmed", "Fatima", "Mohammad", "Aisha", "Omar"  # Middle Eastern
]

international_last_names = [
    "Wang", "Zhang", "Liu", "Chen", "Yang",  # Chinese
    "Kim", "Lee", "Park", "Choi", "Kang",  # Korean
    "Smith", "Johnson", "Brown", "Williams", "Jones",  # Western
    "Patel", "Sharma", "Singh", "Kumar", "Shah",  # Indian
    "Rodriguez", "Garcia", "Martinez", "Gonzalez", "Lopez",  # Latino
    "Ali", "Hassan", "Khan", "Ahmed", "Mahmoud"  # Middle Eastern
]

# School Staff and Special NPCs
school_staff = [
    {"name": "Mr. Tanaka", "role": "Janitor", "personality": "kind"},
    {"name": "Ms. Yamamoto", "role": "School Nurse", "personality": "strict"},
    {"name": "Mr. Sato", "role": "Principal", "personality": "serious"},
    {"name": "Ms. Suzuki", "role": "Librarian", "personality": "kind"},
]

club_presidents = [
    {"name": "Yuki Kato", "club": "Student Council", "personality": "strict"},
    {"name": "Hana Ito", "club": "Drama Club", "personality": "serious"},
    {"name": "Ryo Fujimoto", "club": "Science Club", "personality": "serious"},
    {"name": "Sakura Tanaka", "club": "Art Club", "personality": "kind"},
]

# Function to manage game settings
def settings_menu():
    # No need for global statement since we're only reading game_settings
    while True:
        print("\n{0}===== GAME SETTINGS ====={1}".format(Fore.CYAN, Style.RESET_ALL))
        print("{0}1. Content Settings{1}".format(Fore.YELLOW, Style.RESET_ALL))
        print(
            "{0}2. Game Difficulty:{1} {2}".format(
                Fore.GREEN, Style.RESET_ALL, game_settings["difficulty"].capitalize()
            )
        )
        print(
            "{0}3. Text Speed:{1} {2}".format(
                Fore.BLUE, Style.RESET_ALL, game_settings["text_speed"].capitalize()
            )
        )
        print(
            "{0}4. Enable Cheats:{1} {2}".format(
                Fore.MAGENTA,
                Style.RESET_ALL,
                "Yes" if game_settings["enable_cheats"] else "No",
            )
        )
        print(
            "{0}5. Show Tutorial:{1} {2}".format(
                Fore.CYAN,
                Style.RESET_ALL,
                "Yes" if game_settings.get("show_tutorial", True) else "No",
            )
        )
        print("{0}6. Save Settings{1}".format(Fore.GREEN, Style.RESET_ALL))
        print("{0}7. Reset Settings to Default{1}".format(Fore.RED, Style.RESET_ALL))
        print("{0}8. Return to Main Menu{1}".format(Fore.YELLOW, Style.RESET_ALL))

        choice = input("\nSelect an option (1-8): ")

        if choice == "1":
            content_settings_menu()
        elif choice == "2":
            toggle_setting("difficulty", ["easy", "normal", "hard"])
        elif choice == "3":
            toggle_setting("text_speed", ["slow", "normal", "fast"])
        elif choice == "4":
            game_settings["enable_cheats"] = not game_settings["enable_cheats"]
            print(
                "Cheats {0}.".format(
                    "enabled" if game_settings["enable_cheats"] else "disabled"
                )
            )
        elif choice == "5":
            game_settings["show_tutorial"] = not game_settings.get(
                "show_tutorial", True
            )
            print(
                "Tutorial hints {0}.".format(
                    "enabled" if game_settings["show_tutorial"] else "disabled"
                )
            )
        elif choice == "6":
            save_settings()
            print("Settings saved successfully!")
        elif choice == "7":
            reset_settings()
            print("Settings reset to default values.")
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


def content_settings_menu():
    # No need for global statement since we're only modifying dictionary contents
    # not reassigning game_settings itself
    while True:
        print("\n{0}===== CONTENT SETTINGS ====={1}".format(Fore.CYAN, Style.RESET_ALL))
        print(
            "1. Allow Bullying Events: {0}".format(
                "Yes" if game_settings["allow_bullying"] else "No"
            )
        )
        print(
            "2. Allow Cuss Words: {0}".format(
                "Yes" if game_settings["allow_cuss_words"] else "No"
            )
        )
        print(
            "3. {0}Allow Anime-Style Family Relationships:{1} {2}".format(
                Fore.MAGENTA,
                Style.RESET_ALL,
                f"{Fore.GREEN}Yes{Style.RESET_ALL}"
                if game_settings["allow_cross_family_love"]
                else f"{Fore.RED}No{Style.RESET_ALL}",
            )
        )
        print(
            "4. Family Romance Type: {0}{1}{2}".format(
                Fore.MAGENTA,
                game_settings["cross_family_romance_type"].capitalize(),
                Style.RESET_ALL
            )
        )
        print(
            "5. NSFW Content Level: {0}{1}{2}".format(
                Fore.RED,
                game_settings["nsfw_level"].capitalize(),
                Style.RESET_ALL
            )
        )
        print("6. Return to Settings Menu")

        choice = input("\nSelect an option (1-6): ")

        if choice == "1":
            game_settings["allow_bullying"] = not game_settings["allow_bullying"]
            print(
                "Bullying events {0}.".format(
                    "enabled" if game_settings["allow_bullying"] else "disabled"
                )
            )
        elif choice == "2":
            game_settings["allow_cuss_words"] = not game_settings["allow_cuss_words"]
            print(
                "Cuss words {0}.".format(
                    "enabled" if game_settings["allow_cuss_words"] else "disabled"
                )
            )
        elif choice == "3":
            game_settings["allow_cross_family_love"] = not game_settings[
                "allow_cross_family_love"
            ]
            if game_settings["allow_cross_family_love"]:
                print(
                    "{0}Anime-style family relationships enabled!{1}".format(
                        Fore.MAGENTA, Style.RESET_ALL
                    )
                )
                print(
                    "This allows special relationships with siblings similar to anime storylines."
                )
            else:
                print("Anime-style family relationships disabled.")
                # Reset the cross-family romance type if disabled
                game_settings["cross_family_romance_type"] = "none"
        elif choice == "4":
            # Only configurable if cross-family love is enabled
            if not game_settings["allow_cross_family_love"]:
                print(f"{Fore.YELLOW}You need to enable anime-style family relationships first.{Style.RESET_ALL}")
            else:
                # Toggle through the options
                romance_types = ["none", "step", "all"]
                current_index = romance_types.index(game_settings["cross_family_romance_type"])
                next_index = (current_index + 1) % len(romance_types)
                game_settings["cross_family_romance_type"] = romance_types[next_index]
                
                if game_settings["cross_family_romance_type"] == "none":
                    print("No romantic relationships with family members allowed.")
                elif game_settings["cross_family_romance_type"] == "step":
                    print(f"{Fore.MAGENTA}Romantic relationships with step-siblings/step-family members allowed.{Style.RESET_ALL}")
                    print("This is a common anime trope where characters are not blood-related.")
                elif game_settings["cross_family_romance_type"] == "all":
                    print(f"{Fore.RED}All family romance options enabled.{Style.RESET_ALL}")
                    print("This enables all anime-style family relationship tropes.")
        elif choice == "5":
            # Toggle NSFW content level
            nsfw_levels = ["none", "low", "medium", "high"]
            current_index = nsfw_levels.index(game_settings["nsfw_level"])
            next_index = (current_index + 1) % len(nsfw_levels)
            game_settings["nsfw_level"] = nsfw_levels[next_index]
            
            # Update the allow_nsfw value based on the level
            game_settings["allow_nsfw"] = game_settings["nsfw_level"] != "none"
            
            if game_settings["nsfw_level"] == "none":
                print("All NSFW content disabled. The game will be completely family-friendly.")
            elif game_settings["nsfw_level"] == "low":
                print(f"{Fore.YELLOW}Low NSFW content enabled. This includes mild romantic scenes and suggestions.{Style.RESET_ALL}")
            elif game_settings["nsfw_level"] == "medium":
                print(f"{Fore.YELLOW}Medium NSFW content enabled. This includes more detailed romantic scenes.{Style.RESET_ALL}")
            elif game_settings["nsfw_level"] == "high":
                print(f"{Fore.RED}High NSFW content enabled. This includes detailed romantic encounters with anime-style descriptions.{Style.RESET_ALL}")
            
            print(f"NSFW content level set to: {game_settings['nsfw_level'].capitalize()}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def toggle_setting(setting_name, options):
    # No need for global statement since we're only modifying dictionary values
    current_index = options.index(game_settings[setting_name])
    next_index = (current_index + 1) % len(options)
    game_settings[setting_name] = options[next_index]
    print(
        "{0} set to {1}".format(
            setting_name.capitalize(), game_settings[setting_name].capitalize()
        )
    )


def save_settings():
    try:
        with open("game_settings.json", "w") as file:
            json.dump(game_settings, file)
    except Exception as e:
        print("Error saving settings: {0}".format(e))


def load_settings():
    # Need global here because we're updating the game_settings dictionary object
    try:
        if os.path.exists("game_settings.json"):
            with open("game_settings.json", "r") as file:
                loaded_settings = json.load(file)
                game_settings.update(loaded_settings)
    except Exception as e:
        print("Error loading settings: {0}".format(e))


def reset_settings():
    # Need global because we're reassigning the game_settings variable
    global game_settings
    game_settings = {
        "allow_nsfw": True,  # Set based on nsfw_level (anything above "none")
        "allow_bullying": False,
        "allow_cuss_words": False,
        "allow_cross_family_love": True,  # Changed default to True for anime-style relationships
        "nsfw_level": "low",  # Added nsfw level control (none, low, medium, high)
        "cross_family_romance_type": "step",  # Default to step-siblings only (none, step, all)
        "difficulty": "normal",
        "text_speed": "normal",
        "enable_cheats": False,
        "show_tutorial": True,
    }


# Try to load settings at startup
load_settings()

# Tutorial system
def show_tutorial(topic, force=False):
    """
    Display tutorial messages to help new players
    Only shows if tutorial setting is enabled

    Arguments:
    topic -- the tutorial topic to show
    force -- if True, shows tutorial regardless of settings
    """
    if not game_settings.get("show_tutorial", True) and not force:
        return

    tutorials = {
        "new_game": f"{Fore.YELLOW}TUTORIAL: Welcome to Campus Life! Use commands like '/help' to see available actions. Try '/go classroom' to navigate to different locations.{Style.RESET_ALL}",
        "first_day": f"{Fore.YELLOW}TUTORIAL: It's your first day! Make sure to attend classes and introduce yourself to other students to build relationships.{Style.RESET_ALL}",
        "study": f"{Fore.YELLOW}TUTORIAL: Use '/study [subject]' to improve your grades. Studying consumes energy but improves your academic standing.{Style.RESET_ALL}",
        "sleep": f"{Fore.YELLOW}TUTORIAL: Use '/sleep' in your bedroom or dorm to rest and restore energy. Remember to change into pajamas first!{Style.RESET_ALL}",
        "relationships": f"{Fore.YELLOW}TUTORIAL: Build relationships with other students and teachers using '/interact [name]'. Higher relationships unlock new interaction options.{Style.RESET_ALL}",
        "clothing": f"{Fore.YELLOW}TUTORIAL: Use '/change_clothes [outfit]' to change your outfit. Different locations require appropriate clothing.{Style.RESET_ALL}",
        "clubs": f"{Fore.YELLOW}TUTORIAL: Join clubs with '/join_club [club name]' to gain benefits and meet like-minded students.{Style.RESET_ALL}",
        "romance": f"{Fore.YELLOW}TUTORIAL: Romantic relationships develop through repeated positive interactions. Use '/romance' to view your current romantic status.{Style.RESET_ALL}",
        "quests": f"{Fore.YELLOW}TUTORIAL: Complete quests to earn rewards and advance the story. Use '/quests' to see your current objectives.{Style.RESET_ALL}",
        "health": f"{Fore.YELLOW}TUTORIAL: Monitor your health, energy, hunger, and stress. Use '/status' to check your current condition.{Style.RESET_ALL}",
        "exams": f"{Fore.YELLOW}TUTORIAL: Prepare for exams by studying regularly. Exams occur at the end of each term and affect your overall grades.{Style.RESET_ALL}",
        "weekend": f"{Fore.YELLOW}TUTORIAL: Weekends are free time! Visit different locations like the mall or arcade to enjoy various activities.{Style.RESET_ALL}",
        "part_time": f"{Fore.YELLOW}TUTORIAL: Get a part-time job to earn extra money. Use '/work [job]' to work at your job during appropriate hours.{Style.RESET_ALL}",
        "festivals": f"{Fore.YELLOW}TUTORIAL: School festivals offer special activities and minigames. Participate to earn unique rewards and achievements.{Style.RESET_ALL}",
        "money": f"{Fore.YELLOW}TUTORIAL: Money can be spent on clothing, food, and activities. Earn money through part-time jobs or completing certain quests.{Style.RESET_ALL}",
        "holidays": f"{Fore.YELLOW}TUTORIAL: During holidays, you'll return to your family home. Use this time to strengthen family relationships and relax.{Style.RESET_ALL}",
        "dating": f"{Fore.YELLOW}TUTORIAL: Once in a dating relationship, you can go on special dates and engage in romantic activities. Keep your partner happy with regular interactions!{Style.RESET_ALL}",
        "graduation": f"{Fore.YELLOW}TUTORIAL: Your performance throughout your academic years will determine your graduation outcome and future career options.{Style.RESET_ALL}",
    }

    if topic in tutorials:
        slow_print(tutorials[topic])
        print("")  # Empty line for better readability


# Helper functions for content filtering
def is_content_allowed(content_type):
    """
    Check if specific content type is allowed in the game settings
    """
    # Default: content not allowed
    allowed = False
    
    # Check each content type
    if content_type == "nsfw":
        # NSFW is allowed if nsfw_level is not "none"
        allowed = game_settings["nsfw_level"] != "none"
    
    elif content_type == "bullying":
        allowed = game_settings["allow_bullying"]
    
    elif content_type == "cuss_words":
        allowed = game_settings["allow_cuss_words"]
    
    elif content_type == "cross_family_love":
        # Initial check on if it's enabled
        allowed = game_settings.get("allow_cross_family_love", True)
        
        # If it's enabled, also check that the romance type isn't "none"
        if allowed:
            allowed = game_settings.get("cross_family_romance_type", "none") != "none"
    
    return allowed


def filter_text(text, content_types=None):
    """
    Filter text based on game settings
    If any content type in the list is not allowed, a censored version is returned

    Arguments:
    text -- the original text to potentially filter
    content_types -- list of content types in the text (nsfw, bullying, cuss_words, cross_family_love)

    Returns:
    Original text if all content types are allowed, or censored version
    """
    if not content_types:
        return text

    # Remove cross_family_love from content types - handled by cross_family_romance_type setting
    if "cross_family_love" in content_types:
        content_types.remove("cross_family_love")

    # If no content types left to check, return original text
    if not content_types:
        return text

    for content_type in content_types:
        if content_type == "cuss_words" and not is_content_allowed("cuss_words"):
            # Replace cuss words with asterisks if not allowed
            cuss_words = ["damn", "hell", "crap", "shit", "fuck", "ass", "bitch"]
            censored_text = text
            for word in cuss_words:
                # Use word boundaries to only replace whole words, not parts of words
                # This prevents "class" or "classic" from being censored because they contain "ass"
                pattern = r'\b' + re.escape(word) + r'\b'
                censored_text = re.sub(pattern, "*" * len(word), censored_text, flags=re.IGNORECASE)
            text = censored_text
            
        elif content_type == "bullying" and not is_content_allowed("bullying"):
            # Replace bullying content with a milder version
            text = "Someone was unkind to you in class."
            continue
            
        elif content_type == "nsfw":
            # Handle NSFW content based on nsfw_level setting
            nsfw_level = game_settings["nsfw_level"]
            
            # If NSFW is completely disabled
            if nsfw_level == "none":
                text = "[Content not available with current settings]"
                continue
            
            # For different NSFW levels, we provide different content
            content_modified = False
            
            if "explicit" in text.lower() or "intimate" in text.lower():
                # High level explicit content
                if nsfw_level == "low":
                    text = "You spend some private time together."
                    content_modified = True
                elif nsfw_level == "medium":
                    # Medium level keeps some suggestive content but avoids explicit details
                    # Remove the most explicit parts while keeping the romantic elements
                    explicit_words = ["naked", "nude", "moan", "touch", "climax", "orgasm", "aroused"]
                    censored_text = text
                    for word in explicit_words:
                        pattern = r'\b' + re.escape(word) + r'\b'
                        replacement = "..." if word in ["climax", "orgasm"] else "*" * len(word)
                        censored_text = re.sub(pattern, replacement, censored_text, flags=re.IGNORECASE)
                    text = censored_text
                    content_modified = True
                # For high level, we keep the original content
            
            # Moderately suggestive content (only process if not already modified)
            elif not content_modified and ("kiss" in text.lower() or "embrace" in text.lower() or "cuddle" in text.lower()):
                # Allow all levels to show this content since it's mild
                # No changes needed, continue with original text
                pass

    # If we reach here, all content filtering has been applied
    return text


def check_relationship_compatibility(person1, person2):
    """
    Check if a relationship is allowed based on settings
    
    Arguments:
    person1 -- Player data dictionary
    person2 -- NPC data dictionary
    
    Returns:
    bool -- Whether the relationship is compatible
    """
    # Check if they are family members
    is_family_member = False
    relation_type = "none"  # Default relation (none, step, blood)
    relation_description = "sibling"  # Default description
    
    if "family" in person1:
        # Check if they are siblings
        if "siblings" in person1["family"] and person2["name"] in [
            member["name"] for member in person1["family"]["siblings"]
        ]:
            is_family_member = True
            
            # Get the specific relation (older/younger brother/sister and whether they're step or twin)
            for member in person1["family"]["siblings"]:
                if member["name"] == person2["name"]:
                    relation_description = member["relation"]  # e.g., "older sister", "twin brother"
                    
                    # Determine relation type (step or blood)
                    if "step" in relation_description:
                        relation_type = "step"
                    elif "adopted" in relation_description:
                        relation_type = "step"  # Treat adopted as step for romance purposes
                    else:
                        relation_type = "blood"  # Blood relation (includes twins)
                    break
        
        # Check if they are parents (future implementation)
        if "parents" in person1["family"] and person2["name"] in [
            parent["name"] for parent in person1["family"]["parents"]
        ]:
            is_family_member = True
            relation_type = "blood"  # Default to blood for parents
            
            # Get the specific relation (father/mother and whether they're step)
            for parent in person1["family"]["parents"]:
                if parent["name"] == person2["name"]:
                    relation_description = parent["relation"]  # e.g., "father", "step-mother"
                    if "step" in relation_description:
                        relation_type = "step"
                    break
    
    # If they're family members, check if the relationship is allowed based on settings
    if is_family_member:
        # Check if cross-family love is enabled
        if not game_settings["allow_cross_family_love"]:
            slow_print(f"{Fore.RED}You cannot pursue a romantic relationship with family members.{Style.RESET_ALL}")
            return False
        
        # Check specific type of cross-family relationship allowed
        romance_type = game_settings["cross_family_romance_type"]
        
        if romance_type == "none":
            slow_print(f"{Fore.RED}You cannot pursue a romantic relationship with family members.{Style.RESET_ALL}")
            return False
        elif romance_type == "step" and relation_type == "blood":
            slow_print(f"{Fore.RED}You can only pursue romantic relationships with step-family members, not blood relatives.{Style.RESET_ALL}")
            return False
        
        # If we reach here, the relationship is allowed based on settings
        
        # Get more descriptive messages based on NSFW level
        nsfw_level = game_settings["nsfw_level"]
        
        # Low NSFW level messages (mild suggestions)
        low_nsfw_messages = [
            '{0}"It\'s not like I think of you as just a {1} or anything..."{2}',
            '{0}"W-what if someone finds out about us? Not that I care!"{2}',
            '{0}"We may be related, but my heart wants what it wants..."{2}',
            '{0}"I\'ve always felt this special connection with you..."{2}',
            '{0}"Maybe this was destined to happen all along..."{2}',
        ]
        
        # Medium NSFW level messages (more romantic)
        medium_nsfw_messages = [
            '{0}"When we\'re alone like this, I forget we\'re supposed to be {1}s..."{2}',
            '{0}"My heart races whenever you\'re close to me, despite our family ties..."{2}',
            '{0}"I know it\'s taboo, but I can\'t help feeling this way about you..."{2}',
            '{0}"Let\'s keep this between us... our special secret relationship..."{2}',
            '{0}"I\'ve always watched you from afar, wishing we weren\'t related..."{2}',
        ]
        
        # High NSFW level messages (more direct)
        high_nsfw_messages = [
            '{0}"Being your {1} makes this even more exciting somehow..."{2}',
            '{0}"When we\'re behind closed doors, family titles don\'t matter..."{2}',
            '{0}"No one understands our bond - it goes beyond normal family relations..."{2}',
            '{0}"I\'ve dreamed of you holding me like this, even though we\'re family..."{2}',
            '{0}"The forbidden nature of our feelings makes them stronger, don\'t you think?"{2}',
        ]
        
        # Choose appropriate message set based on NSFW level
        if nsfw_level == "medium":
            special_messages = medium_nsfw_messages
        elif nsfw_level == "high":
            special_messages = high_nsfw_messages
        else:  # "none" or "low"
            special_messages = low_nsfw_messages
        
        relation_term = relation_description.split()[-1]  # Get just "sister", "brother" etc.
        
        # Show the special romance message
        slow_print(
            "{0}A special bond forms between you and your {1}...{2}".format(
                Fore.MAGENTA, relation_description, Style.RESET_ALL
            ),
            delay=0.04,
        )
        
        # Random anime-style line
        slow_print(
            random.choice(special_messages).format(Fore.MAGENTA, relation_term, Style.RESET_ALL),
            delay=0.05,
        )
        
        # Add special achievement for family romance
        achievement_name = "Forbidden Love"
        if relation_type == "step":
            achievement_name = "Not Blood Related"
        
        if achievement_name not in player["achievements"]:
            player["achievements"].append(achievement_name)
            slow_print(
                "{0}Achievement unlocked: {1}{2}".format(
                    Fore.YELLOW, achievement_name, Style.RESET_ALL
                )
            )
            
            # Bonus charisma for being daring
            player["charisma"]["social"] += 3
            slow_print(
                "Your social charisma has increased due to your unique relationship!"
            )
        
        return True
    
    # All other relationships are allowed
    return True


# Game Title
TITLE = "My First Day Here: Campus Life Edition"
# Define ASCII art with line-by-line strings for better readability
ASCII_ART = f"""    {Fore.MAGENTA}____________________________
   |{Fore.CYAN}                            {Fore.MAGENTA}|
   |{Fore.WHITE}    My First Day Here:      {Fore.MAGENTA}|
   |{Fore.WHITE}    Campus Life Edition     {Fore.MAGENTA}|
   |____________________________| {Style.RESET_ALL}"""

# Weather system variables
WEATHER_TYPES = ["sunny", "cloudy", "rainy", "stormy", "foggy", "snowy", "windy"]

WEATHER_EFFECTS = {
    "sunny": {
        "mood": 5,  # Positive effect on mood (stress reduction)
        "energy": 5,  # Energy bonus
        "description": "The sun is shining brightly today, lifting everyone's spirits.",
        "activities": ["outdoor sports", "picnic", "gardening"],
    },
    "cloudy": {
        "mood": 0,  # Neutral effect
        "energy": 0,
        "description": "The sky is covered with clouds, making for a mild day.",
        "activities": ["reading", "studying", "indoor activities"],
    },
    "rainy": {
        "mood": -5,  # Slightly negative effect (increases stress)
        "energy": -5,  # Slightly draining
        "description": "Rain pours down steadily, creating a melancholic atmosphere.",
        "activities": ["studying", "reading", "sleeping"],
    },
    "stormy": {
        "mood": -10,  # More negative effect
        "energy": -10,  # More draining
        "description": "A storm rages outside with thunder and lightning. Better stay indoors!",
        "activities": ["studying", "sleeping", "watching movies"],
    },
    "foggy": {
        "mood": -3,
        "energy": -3,
        "description": "A thick fog has settled, creating a mysterious atmosphere.",
        "activities": ["reading", "writing", "meditation"],
    },
    "snowy": {
        "mood": 3,  # Slightly positive (pretty snow)
        "energy": -7,  # But cold and requires more energy
        "description": "Snowflakes fall gently, covering everything in white.",
        "activities": ["skiing", "snowball fights", "hot cocoa by the fire"],
    },
    "windy": {
        "mood": -2,
        "energy": -5,
        "description": "Strong winds blow through the campus, rustling the trees.",
        "activities": ["kite flying", "indoor games", "crafting"],
    },
}

# Season-appropriate weather
SEASONAL_WEATHER = {
    "spring": ["sunny", "cloudy", "rainy", "windy"],
    "summer": ["sunny", "cloudy", "rainy", "stormy"],
    "fall": ["cloudy", "rainy", "foggy", "windy"],
    "winter": ["cloudy", "foggy", "snowy", "windy"],
}

# Current weather
current_weather = "sunny"

# Global Variables
player = {
    "name": "",
    "gender": "",
    "money": 1000,
    "grades": {},
    "reputation": {"students": 0, "teachers": 0},
    "charisma": {"social": 0, "academic": 0},
    "rank": {"students": "Nobody", "teachers": "Unknown"},
    "part_time_job": None,
    "energy": 100,
    "hunger": 100,
    "stress": 20,  # For health/stress system (0-100)
    "health": 100,  # Overall health (affected by stress, hunger, sleep)
    "current_location": "",
    "electives": [],
    "clubs": [],
    "club_positions": {},  # Positions/roles in clubs
    "romantic_interest": None,  # For romance system
    "romance_stage": 0,  # Romance progression (0-5)
    "romance_points": 0,  # Points toward next romance stage
    "ex_partners": [],  # List of ex romantic partners with status info
    "achievements": [],  # For achievement system
    "quests": [],  # For quest tracking
    "completed_quests": [],  # IDs of completed quests
    "festival_points": 0,  # Points earned during festivals
    "festival_achievements": [],  # Special achievements from festivals
    "school_year": 1,  # Current school year (1-4)
    "year_progress": 0,  # Progress within current year (0-100%)
    "completed_years": [],  # Years successfully completed
    "internships": [],  # Career building internships for upper years
    "gpa": 0.0,  # Grade Point Average across all subjects
    "clothing": {
        "owned": [],  # List of owned clothing items
        "wearing": None,  # Currently worn outfit
    },
    "pe_stats": {  # Physical Education stats
        "strength": 1,
        "agility": 1,
        "endurance": 1,
        "technique": 1,
    },
    # Accommodation System
    "accommodation_type": "",  # "dorm" or "home"
    "dorm_number": 0,  # Random dorm number if in dorm
    "home_location": "",  # Location of home if not in dorm
    # Daily Life System
    "has_had_dinner": False,  # Track if player has had dinner
    "has_slept": False,  # Track if player has slept
    # Family System
    "family": {
        "parents": [],  # Will contain parent info
        "siblings": [],  # Will contain sibling info if any
    },
    "family_relationship": {},  # Track relationship with family members
    "relationships": {},  # Track relationships with other characters
    # Mental Health System
    "mental_health": {
        "happiness": 80,  # 0-100 scale (0: severely depressed, 100: extremely happy)
        "depression": 0,  # 0-100 scale (0: none, 100: severe)
        "anxiety": 0,  # 0-100 scale (0: none, 100: severe)
        "self_esteem": 70,  # 0-100 scale (0: very low, 100: very high)
        "bullying_incidents": 0,  # Count of bullying incidents experienced
        "breakup_count": 0,  # Number of romantic breakups experienced
        "therapy_sessions": 0,  # Number of therapy sessions attended
        "last_therapy_date": None,  # Date of last therapy session
        "support_network": 50,  # 0-100 scale (friends/family support strength)
        "coping_skills": 30,  # Developed coping mechanisms (0-100)
    },
    # Neurodiversity traits
    "neurodiversity": {
        "trait": None,  # Main trait if any (dyslexia, adhd, autism)
        "severity": 0,  # Severity level (1-5)
        "accommodations": [],  # List of accommodations received
        "diagnosis_date": None,  # When diagnosed (if at all)
        "managed": False,  # Whether the condition is being properly managed
        "strengths": [],  # Special strengths due to neurodiversity
    },
}

# ----- CLUB SYSTEM -----
clubs = {
    "Student Council": {
        "description": "The prestigious student government organization. Members develop leadership skills and organize school events.",
        "meeting_day": "Friday",
        "location": "Student Council Room",
        "benefits": {
            "reputation": {"teachers": 2, "students": 1},
            "charisma": {"social": 1},
            "stress_reduction": 5,
        },
        "activities": [
            "Organize school festivals",
            "Hold meetings",
            "Vote on school policies",
        ],
        "requirements": {
            "charisma": {"social": 5, "academic": 6},
            "reputation": {"teachers": 20},
        },
        "members": [],
        "president": "Yuki Kato",
    },
    "Drama Club": {
        "description": "For those interested in acting and theater. Members perform plays and develop public speaking skills.",
        "meeting_day": "Thursday",
        "location": "Auditorium",
        "benefits": {"charisma": {"social": 2}, "stress_reduction": 10},
        "activities": ["Rehearse for plays", "Study scripts", "Perform for the school"],
        "requirements": {"charisma": {"social": 7}},
        "members": [],
        "president": "Hana Ito",
    },
    "Science Club": {
        "description": "A club for science enthusiasts. Members conduct experiments and participate in science competitions.",
        "meeting_day": "Tuesday",
        "location": "Science Lab",
        "benefits": {"charisma": {"academic": 2}, "grades_boost": ["Science"]},
        "activities": [
            "Conduct experiments",
            "Prepare for science fair",
            "Discuss scientific topics",
        ],
        "requirements": {"charisma": {"academic": 6}, "grades": {"Science": "C"}},
        "members": [],
        "president": "Ryo Fujimoto",
    },
    "Art Club": {
        "description": "For creative students interested in visual arts. Members create and display artwork around the school.",
        "meeting_day": "Wednesday",
        "location": "Art Room",
        "benefits": {
            "charisma": {"social": 1},
            "stress_reduction": 15,
            "grades_boost": ["Art"],
        },
        "activities": ["Paint", "Sculpt", "Exhibit artwork"],
        "requirements": {"grades": {"Art": "C"}},
        "members": [],
        "president": "Sakura Tanaka",
    },
    "Sports Club": {
        "description": "For athletic students. Members practice various sports and compete against other schools.",
        "meeting_day": "Monday",
        "location": "Gym",
        "benefits": {
            "charisma": {"social": 2},
            "stress_reduction": 20,
            "energy_boost": 10,
        },
        "activities": ["Practice sports", "Compete in tournaments", "Fitness training"],
        "requirements": {"energy": 50},
        "members": [],
        "president": "Takeshi Yamamoto",
    },
    "Music Club": {
        "description": "For music lovers. Members practice instruments and perform concerts.",
        "meeting_day": "Tuesday",
        "location": "Music Room",
        "benefits": {
            "charisma": {"social": 1},
            "stress_reduction": 15,
            "grades_boost": ["Music"],
        },
        "activities": ["Practice instruments", "Compose music", "Perform concerts"],
        "requirements": {},
        "members": [],
        "president": "Haruka Suzuki",
    },
    "Literature Club": {
        "description": "For book enthusiasts. Members read and discuss literature, and sometimes write their own stories.",
        "meeting_day": "Wednesday",
        "location": "Library",
        "benefits": {
            "charisma": {"academic": 2},
            "grades_boost": ["Literature", "English"],
        },
        "activities": ["Read books", "Discuss literature", "Write stories"],
        "requirements": {"grades": {"Literature": "C"}},
        "members": [],
        "president": "Yuna Tanaka",
    },
    "Gaming Club": {
        "description": "For video game enthusiasts. Members play games together and sometimes organize tournaments.",
        "meeting_day": "Thursday",
        "location": "Computer Lab",
        "benefits": {"charisma": {"social": 1}, "stress_reduction": 25},
        "activities": [
            "Play video games",
            "Organize tournaments",
            "Discuss game development",
        ],
        "requirements": {},
        "members": [],
        "president": "Kenta Nakamura",
    },
}

# ----- ROMANCE SYSTEM -----
# Romance stages and requirements
ROMANCE_STAGES = {
    0: {"name": "Not interested", "req": 0},
    1: {"name": "Acquainted", "req": 30},
    2: {"name": "Friends", "req": 60},
    3: {"name": "Close Friends", "req": 100},
    4: {"name": "Crush", "req": 150},
    5: {"name": "Dating", "req": 200},
}

# Romantic interaction options by stage
ROMANCE_INTERACTIONS = {
    0: ["Small talk", "Study together"],
    1: ["Chat", "Hang out", "Compliment"],
    2: ["Deep conversation", "Fun activity", "Share interests"],
    3: ["Personal discussion", "Gift giving", "Plan outing"],
    4: ["Express feelings", "Romantic gesture", "Special date"],
    5: ["Kiss", "Hold hands", "Special date", "Love confession"],
}

# ----- CLOTHING SYSTEM -----
# Clothing items available in the game
CLOTHING_ITEMS = {
    # Basic starter items
    "School Uniform": {
        "description": "Standard school uniform required for attending classes",
        "price": 3000,
        "type": "uniform",
        "appropriate_for": ["school", "classes", "library", "cafeteria"],
        "charisma": 0,  # No bonus, but required
    },
    "Casual Black T-shirt": {
        "description": "A simple black t-shirt for casual wear",
        "price": 1000,
        "type": "casual",
        "appropriate_for": ["free time", "weekend", "shopping", "restaurant"],
        "charisma": 1,
    },
    "Casual Black Pants": {
        "description": "Simple black pants/trousers for casual wear",
        "price": 1500,
        "type": "casual",
        "appropriate_for": ["free time", "weekend", "shopping", "restaurant"],
        "charisma": 1,
    },
    "Pajamas": {
        "description": "Comfortable sleeping clothes, required for sleeping",
        "price": 1200,
        "type": "sleep",
        "appropriate_for": ["sleep", "dorm"],
        "charisma": -10 if "outside" else 0,  # Penalty for wearing outside
    },
    # Additional purchasable items
    "Formal Attire": {
        "description": "Elegant formal wear for special occasions",
        "price": 7000,
        "type": "formal",
        "appropriate_for": ["formal event", "date", "ceremony"],
        "charisma": 10,
    },
    "Sporty Outfit": {
        "description": "Athletic wear ideal for sports and exercise",
        "price": 3500,
        "type": "sports",
        "appropriate_for": ["gym", "sports", "exercise"],
        "charisma": 3,
        "energy_boost": 5,
    },
    "Trendy Outfit": {
        "description": "Fashionable clothes following the latest trends",
        "price": 5000,
        "type": "casual",
        "appropriate_for": ["free time", "weekend", "shopping", "date", "party"],
        "charisma": 8,
    },
    "Winter Coat": {
        "description": "Warm coat for the cold winter months",
        "price": 4500,
        "type": "outerwear",
        "appropriate_for": ["winter", "cold weather"],
        "charisma": 4,
        "health_boost": 5 if "winter" else 0,  # Health bonus in winter
    },
    "Swimwear": {
        "description": "Proper attire for swimming or beach activities",
        "price": 2500,
        "type": "swim",
        "appropriate_for": ["beach", "pool"],
        "charisma": 5 if "beach" or "pool" else -15,  # Penalty for inappropriate wear
    },
    "Designer Clothes": {
        "description": "High-end designer outfit that attracts attention",
        "price": 12000,
        "type": "casual",
        "appropriate_for": ["free time", "shopping", "party", "date"],
        "charisma": 15,
        "reputation_boost": 5,
    },
}

# Locations where clothing can be changed
CHANGING_LOCATIONS = [
    "Student Room 364",  # Dorm room
    "Your Bedroom",  # Home bedroom
    "Changing Room",  # Sports facility
]

# Change clothing function
def change_clothing(new_clothing_name):
    """
    Change the player's current clothing

    Arguments:
    new_clothing_name -- Name of the clothing to change into

    Returns:
    bool -- Whether the change was successful
    """
    # No need for global declaration since we're only accessing/modifying dictionary entries

    # Check if player owns this clothing
    if new_clothing_name not in player["clothing"]["owned"]:
        slow_print(f"You don't own {new_clothing_name}.")
        return False

    # Check if player is in an appropriate location for changing
    if player["current_location"] not in CHANGING_LOCATIONS:
        slow_print("You can only change clothes in your room or a changing room.")
        return False

    # Remove effects of current clothing if any
    if player["clothing"]["wearing"]:
        apply_clothing_effects(player["clothing"]["wearing"], apply=False)

    # Change to new clothing
    player["clothing"]["wearing"] = new_clothing_name

    # Apply effects of new clothing
    apply_clothing_effects(new_clothing_name, apply=True)

    slow_print(f"You changed into {new_clothing_name}.")

    # Check if wearing appropriate clothing
    is_appropriate, reason = is_clothing_appropriate(
        new_clothing_name,
        player["current_location"],
        is_school_day=current_date.weekday() < 5,
        is_festival=check_for_special_events(),
    )

    if not is_appropriate:
        slow_print(f"Warning: {reason}")

    return True


# Function to check if clothing is appropriate for the current location/situation
def is_clothing_appropriate(
    clothing_name, location, is_school_day=True, is_festival=False
):
    """
    Check if the current clothing is appropriate for the location and time

    Arguments:
    clothing_name -- Name of the clothing item
    location -- Current location
    is_school_day -- Whether it's a school day (weekday)
    is_festival -- Whether there's a festival happening

    Returns:
    (bool, str) -- Whether the clothing is appropriate and reason if not
    """
    # No clothing selected
    if not clothing_name or clothing_name not in CLOTHING_ITEMS:
        return False, "You need to wear something!"

    clothing = CLOTHING_ITEMS[clothing_name]

    # School rules
    school_locations = [
        "Classroom",
        "School Hallway",
        "Library",
        "Cafeteria",
        "Science Lab",
        "Gym",
    ]
    if location in school_locations and is_school_day and not is_festival:
        if clothing["type"] != "uniform":
            return False, "School uniform is required during school days!"

    # Sleeping requires pajamas
    if location in ["Student Room 364", "Your Bedroom"] and player.get(
        "sleeping", False
    ):
        if clothing["type"] != "sleep":
            return False, "You need to wear pajamas to sleep properly!"

    # Pajamas restrictions
    if clothing["type"] == "sleep" and location not in [
        "Student Room 364",
        "Your Bedroom",
    ]:
        return False, "You shouldn't wear pajamas outside your room!"

    # Special occasion clothing
    if location == "Gym" and clothing["type"] not in ["sports", "uniform"]:
        return False, "Athletic wear or uniform is required in the gym!"

    if location == "Beach" and clothing["type"] != "swim":
        return False, "You need proper swimwear at the beach!"

    # All other cases are fine
    return True, ""


# Apply clothing effects (charisma, other stats)
def apply_clothing_effects(clothing_name, apply=True):
    """
    Apply or remove effects from clothing

    Arguments:
    clothing_name -- Name of the clothing item
    apply -- Whether to apply (True) or remove (False) effects
    """
    if not clothing_name or clothing_name not in CLOTHING_ITEMS:
        return

    clothing = CLOTHING_ITEMS[clothing_name]

    # Apply/remove charisma effect
    if "charisma" in clothing:
        modifier = 1 if apply else -1
        charisma_boost = clothing["charisma"] * modifier

        # Special case for pajamas outside
        if clothing["type"] == "sleep" and player["current_location"] not in [
            "Student Room 364",
            "Your Bedroom",
        ]:
            charisma_boost = -10 * modifier

        player["charisma"]["social"] = max(
            0, min(100, player["charisma"]["social"] + charisma_boost)
        )

    # Other potential effects
    if "energy_boost" in clothing:
        modifier = 1 if apply else -1
        energy_boost = clothing["energy_boost"] * modifier
        player["energy"] = max(0, min(100, player["energy"] + energy_boost))

    if "health_boost" in clothing:
        modifier = 1 if apply else -1
        health_boost = clothing["health_boost"] * modifier
        player["health"] = max(0, min(100, player["health"] + health_boost))

    if "reputation_boost" in clothing:
        modifier = 1 if apply else -1
        rep_boost = clothing["reputation_boost"] * modifier
        player["reputation"]["students"] = max(
            0, min(100, player["reputation"]["students"] + rep_boost)
        )


# ----- FESTIVAL SYSTEM -----
FESTIVALS = {
    "Spring Cherry Blossom Festival": {
        "date": (4, 15),  # April 15
        "description": "Celebrate the blooming of cherry blossoms with various activities and food stalls.",
        "activities": [
            "Cherry blossom viewing",
            "Traditional dance",
            "Food stalls",
            "Poetry contest",
        ],
        "special_rewards": {
            "Cherry Blossom Enthusiast": "Stress reduction effect increased by 10%"
        },
        "minigame": "poetry_contest",  # Poetry writing contest minigame
    },
    "Summer Cultural Festival": {
        "date": (7, 20),  # July 20
        "description": "A vibrant festival with performances, games, and food celebrating the summer season.",
        "activities": [
            "Firework display",
            "Stage performances",
            "Game booths",
            "Food competition",
        ],
        "special_rewards": {"Cultural Festival Star": "Charisma (social) +2"},
        "minigame": "goldfish_scooping",  # Traditional Japanese goldfish scooping game
    },
    "Autumn Sports Festival": {
        "date": (10, 10),  # October 10
        "description": "A day of competitive sports activities between different classes and clubs.",
        "activities": ["Relay race", "Tug of war", "Ball games", "Team competitions"],
        "special_rewards": {
            "Sports Festival Champion": "PE stats +1 in all categories"
        },
        "minigame": "relay_race",  # Relay race minigame
    },
    "Winter Holiday Festival": {
        "date": (12, 20),  # December 20
        "description": "A cozy celebration with decorations, gifts, and warm food before the winter break.",
        "activities": [
            "Gift exchange",
            "Holiday decorating",
            "Hot food stalls",
            "Caroling",
        ],
        "special_rewards": {"Winter Festival Enthusiast": "Money +1000"},
        "minigame": "gift_exchange",  # Gift exchange minigame
    },
    # Traditional Japanese Festivals
    "Tanabata Festival": {
        "date": (7, 7),  # July 7
        "description": "The Star Festival celebrating the meeting of the deities Orihime and Hikoboshi.",
        "activities": [
            "Writing wishes on tanzaku papers",
            "Decorating bamboo with ornaments",
            "Star gazing",
            "Traditional storytelling",
        ],
        "special_rewards": {
            "Star-Crossed Scholar": "Academic charisma +2 and a special wish granted"
        },
        "minigame": "tanzaku_wish",  # Wish writing minigame
    },
    "Obon Festival": {
        "date": (8, 15),  # August 15
        "description": "A Japanese Buddhist custom to honor the spirits of ancestors with lanterns and traditional dance.",
        "activities": [
            "Bon Odori dance",
            "Floating lanterns",
            "Ancestor offerings",
            "Traditional food",
        ],
        "special_rewards": {
            "Spirit Dancer": "Energy +20 and special spiritual insight"
        },
        "minigame": "bon_odori",  # Rhythm-based dance minigame
    },
    "Setsubun Festival": {
        "date": (2, 3),  # February 3
        "description": "A bean-throwing festival to chase away evil spirits and welcome good fortune.",
        "activities": [
            "Bean throwing",
            "Demon mask making",
            "Fortune direction rituals",
            "Special sushi rolls",
        ],
        "special_rewards": {"Fortune Bearer": "Luck +20% for the next month"},
        "minigame": "bean_throwing",  # Target-based bean throwing minigame
    },
    "Hinamatsuri": {
        "date": (3, 3),  # March 3
        "description": "Girls' Day or Doll Festival celebrating female children and praying for their health and happiness.",
        "activities": [
            "Displaying ornamental dolls",
            "Making peach blossom decorations",
            "Traditional tea ceremony",
            "Special rice cakes",
        ],
        "special_rewards": {
            "Doll Festival Celebrant": "Relationship points +15 with female students"
        },
        "minigame": "doll_arrangement",  # Doll arrangement puzzle minigame
    },
    "Kodomo no Hi": {
        "date": (5, 5),  # May 5
        "description": "Children's Day celebrating the happiness of children and praying for their health and success.",
        "activities": [
            "Koinobori (carp streamers) decoration",
            "Kabuto (samurai helmet) crafting",
            "Traditional sweets",
            "Martial arts demonstrations",
        ],
        "special_rewards": {"Youthful Warrior": "PE stats +2 and energy +15"},
        "minigame": "koinobori_race",  # Carp race minigame
    },
    "Gion Matsuri": {
        "date": (7, 17),  # July 17
        "description": "One of Japan's most famous festivals with a month-long celebration featuring massive floats and street food.",
        "activities": [
            "Float procession viewing",
            "Traditional music performances",
            "Yukata wearing",
            "Street food tasting",
        ],
        "special_rewards": {
            "Festival Connoisseur": "Charisma (social) +3 and stress -25"
        },
        "minigame": "yukata_design",  # Yukata design minigame
    },
    "Awa Odori": {
        "date": (8, 12),  # August 12-15, but we'll use the start date
        "description": "A famous dance festival where large groups of dancers perform traditional dances in colorful costumes.",
        "activities": [
            "Group dancing",
            "Costume wearing",
            "Traditional music",
            "Dance competitions",
        ],
        "special_rewards": {"Dance Master": "Charisma (social) +2 and PE stats +1"},
        "minigame": "rhythm_dance",  # Rhythm-based dance minigame
    },
    "Shichi-Go-San": {
        "date": (11, 15),  # November 15
        "description": "A day to celebrate children's growth and well-being at the ages of 3, 5, and 7.",
        "activities": [
            "Traditional photo session",
            "Shrine visit",
            "Chitose candy distribution",
            "Special kimono wearing",
        ],
        "special_rewards": {"Child at Heart": "Stress -30 and energy +20"},
        "minigame": "candy_collecting",  # Candy collecting minigame
    },
    "Momijigari": {
        "date": (11, 10),  # Mid-November (approximate)
        "description": "The tradition of viewing autumn leaves, particularly Japanese maple trees.",
        "activities": [
            "Leaf viewing hikes",
            "Nature photography",
            "Outdoor tea ceremony",
            "Leaf crafts",
        ],
        "special_rewards": {"Nature Enthusiast": "Stress -25 and creativity +15"},
        "minigame": "leaf_collection",  # Leaf collection minigame
    },
}

# ----- ACHIEVEMENT SYSTEM -----
achievements = {
    "Academic Excellence": {
        "description": "Get an A in every subject",
        "reward": {"charisma": {"academic": 3}},
        "condition": lambda: all(grade == "A" for grade in player["grades"].values()),
    },
    "Social Butterfly": {
        "description": "Reach 'Popular' rank among students",
        "reward": {"charisma": {"social": 3}},
        "condition": lambda: player["rank"]["students"] == "Popular",
    },
    "Teacher's Pet": {
        "description": "Reach 'Respected' rank among teachers",
        "reward": {"reputation": {"teachers": 10}},
        "condition": lambda: player["rank"]["teachers"] == "Respected",
    },
    "Club Leader": {
        "description": "Become president of any club",
        "reward": {"charisma": {"social": 2, "academic": 2}},
        "condition": lambda: any(
            club_info["president"] == player["name"]
            for club_name, club_info in clubs.items()
        ),
    },
    "Romance Expert": {
        "description": "Reach 'Dating' stage in a romantic relationship",
        "reward": {"charisma": {"social": 4}},
        "condition": lambda: player["romance_stage"] >= 5,
    },
    "Perfect Attendance": {
        "description": "Never miss a class for 30 days",
        "reward": {"reputation": {"teachers": 15}},
        "hidden": True,
    },
    "Money Maker": {
        "description": "Earn over ¥10,000 from part-time jobs",
        "reward": {"money": 5000},
        "hidden": True,
    },
    "Festival Enthusiast": {
        "description": "Participate in all 4 seasonal festivals",
        "reward": {"stress_reduction_boost": 20},
        "hidden": True,
    },
    "Quest Champion": {
        "description": "Complete 10 quests",
        "reward": {"money": 3000, "reputation": {"students": 10, "teachers": 10}},
        "condition": lambda: len(player["completed_quests"]) >= 10,
    },
    "Athletic Prodigy": {
        "description": "Reach level 5 in all PE stats",
        "reward": {"health_boost": 10, "energy_boost": 15},
        "condition": lambda: all(stat >= 5 for stat in player["pe_stats"].values()),
    },
    "Campus Explorer": {
        "description": "Visit every location on campus",
        "reward": {"charisma": {"social": 2}, "stress_reduction": 15},
        "condition": lambda: len(player.get("visited_locations", [])) >= len(locations),
    },
    "Festival King/Queen": {
        "description": "Win a minigame at every seasonal festival",
        "reward": {"money": 3000, "reputation": {"students": 15}},
        "hidden": True,
    },
    "Master Networker": {
        "description": "Have at least 10 friends with relationship level of 'Good Friend' or higher",
        "reward": {"charisma": {"social": 5}},
        "condition": lambda: len(
            [name for name, points in relationship.items() if points >= 60]
        )
        >= 10,
    },
    "Career Focused": {
        "description": "Complete 3 internships in your chosen field",
        "reward": {"future_job_prospects": "+20%"},
        "condition": lambda: len(player["internships"]) >= 3,
    },
    "Balance Master": {
        "description": "Maintain high grades, social life, and health simultaneously for 2 weeks",
        "reward": {"stress_reduction_boost": 25, "energy_conservation": 15},
        "hidden": True,
    },
    "Culinary Explorer": {
        "description": "Try every food item in the cafeteria and at least 5 restaurants",
        "reward": {"hunger_reduction": "-15%", "health_boost": 5},
        "hidden": True,
    },
    "Cultural Connoisseur": {
        "description": "Participate in at least 8 different Japanese festivals",
        "reward": {
            "charisma": {"social": 3, "academic": 2},
            "reputation": {"students": 10, "teachers": 5},
        },
        "condition": lambda: len(player.get("attended_festivals", [])) >= 8,
    },
    "Relationship Guru": {
        "description": "Help 5 friends with their romantic problems",
        "reward": {"charisma": {"social": 4}, "love_advice_ability": True},
        "hidden": True,
    },
    "Class Representative": {
        "description": "Be elected as class representative",
        "reward": {"reputation": {"students": 15, "teachers": 15}},
        "hidden": True,
    },
    "Graduate with Honors": {
        "description": "Complete all 4 academic years with a GPA of 3.5 or higher",
        "reward": {"career_success_rate": "+30%"},
        "condition": lambda: player["school_year"] > 4 and player["gpa"] >= 3.5,
    },
}

# ----- QUEST SYSTEM -----
# Quest structure defined in setup_game(), here are just templates for different quest types
QUEST_TEMPLATES = {
    "academic": {
        "description": "Study for {subject} exam",
        "objective": "Study {subject} for 3 hours",
        "reward": 30,
        "subject_reward": True,
    },
    "social": {
        "description": "Help {student} with a problem",
        "objective": "Talk to {student} at {location}",
        "reward": 20,
        "reputation_reward": {"students": 5},
    },
    "club": {
        "description": "Help the {club} with their activity",
        "objective": "Go to {location} for club activity",
        "reward": 25,
        "club_reputation": True,
    },
    "exploration": {
        "description": "Find something at the {location}",
        "objective": "Go to {location} and search around",
        "reward": 15,
        "item_reward": True,
    },
}

# ----- PE CHALLENGE SYSTEM -----
PE_CHALLENGES = {
    "Running Track": {
        "description": "Test your speed and endurance on the track",
        "difficulty": 1,
        "stat_affected": "endurance",
        "rewards": {"pe_stats": {"endurance": 1}},
    },
    "Basketball": {
        "description": "Practice shooting baskets and team play",
        "difficulty": 2,
        "stat_affected": "technique",
        "rewards": {"pe_stats": {"technique": 1}},
    },
    "Swimming": {
        "description": "Improve your swimming technique and stamina",
        "difficulty": 3,
        "stat_affected": "endurance",
        "rewards": {"pe_stats": {"endurance": 1, "strength": 1}},
    },
    "Martial Arts": {
        "description": "Learn discipline and self-defense techniques",
        "difficulty": 3,
        "stat_affected": "technique",
        "rewards": {"pe_stats": {"technique": 2}},
    },
    "Weight Training": {
        "description": "Build strength and muscle definition",
        "difficulty": 2,
        "stat_affected": "strength",
        "rewards": {"pe_stats": {"strength": 2}},
    },
    "Gymnastics": {
        "description": "Develop flexibility and balance",
        "difficulty": 4,
        "stat_affected": "agility",
        "rewards": {"pe_stats": {"agility": 2}},
    },
    "Team Sports": {
        "description": "Practice teamwork and coordination",
        "difficulty": 2,
        "stat_affected": "social",
        "rewards": {"charisma": {"social": 1}},
    },
}

# Cafeteria menu
cafeteria_menu = {
    "Rice Bowl": {
        "price": 300,
        "energy_gain": 20,
        "hunger_gain": 30,
        "stress_reduction": 5,
    },
    "Curry": {
        "price": 500,
        "energy_gain": 35,
        "hunger_gain": 50,
        "stress_reduction": 10,
    },
    "Sandwich": {
        "price": 250,
        "energy_gain": 15,
        "hunger_gain": 20,
        "stress_reduction": 3,
    },
    "Salad": {
        "price": 200,
        "energy_gain": 10,
        "hunger_gain": 15,
        "stress_reduction": 2,
    },
    "Soda": {"price": 150, "energy_gain": 5, "hunger_gain": 5, "stress_reduction": 8},
    # New food items
    "Bento Box": {
        "price": 650,
        "energy_gain": 40,
        "hunger_gain": 60,
        "stress_reduction": 15,
    },
    "Ramen": {
        "price": 450,
        "energy_gain": 30,
        "hunger_gain": 45,
        "stress_reduction": 12,
    },
    "Onigiri": {
        "price": 200,
        "energy_gain": 15,
        "hunger_gain": 25,
        "stress_reduction": 5,
    },
    "Udon": {
        "price": 400,
        "energy_gain": 25,
        "hunger_gain": 40,
        "stress_reduction": 8,
    },
    "Yakisoba": {
        "price": 550,
        "energy_gain": 35,
        "hunger_gain": 50,
        "stress_reduction": 10,
    },
    "Tempura Set": {
        "price": 600,
        "energy_gain": 35,
        "hunger_gain": 55,
        "stress_reduction": 12,
    },
    "Sushi Set": {
        "price": 700,
        "energy_gain": 30,
        "hunger_gain": 50,
        "stress_reduction": 18,
    },
    "Green Tea": {
        "price": 120,
        "energy_gain": 10,
        "hunger_gain": 5,
        "stress_reduction": 15,
    },
    "Coffee": {
        "price": 180,
        "energy_gain": 25,
        "hunger_gain": 5,
        "stress_reduction": 10,
    },
    "Fruit Juice": {
        "price": 200,
        "energy_gain": 15,
        "hunger_gain": 10,
        "stress_reduction": 8,
    },
}

# Health/Stress System - Visual indicators
def get_health_indicator():
    """Get a visual indicator of player's health"""
    health = player["health"]
    if health >= 90:
        return f"{Fore.LIGHTGREEN_EX}Excellent{Style.RESET_ALL}"
    elif health >= 70:
        return f"{Fore.GREEN}Good{Style.RESET_ALL}"
    elif health >= 50:
        return f"{Fore.YELLOW}Average{Style.RESET_ALL}"
    elif health >= 30:
        return f"{Fore.LIGHTRED_EX}Poor{Style.RESET_ALL}"
    else:
        return f"{Back.RED}{Fore.WHITE}Critical{Style.RESET_ALL}"


def get_stress_indicator():
    """Get a visual indicator of player's stress level"""
    stress = player["stress"]
    if stress < 20:
        return f"{Fore.LIGHTGREEN_EX}Relaxed{Style.RESET_ALL}"
    elif stress < 40:
        return f"{Fore.GREEN}Normal{Style.RESET_ALL}"
    elif stress < 60:
        return f"{Fore.YELLOW}Stressed{Style.RESET_ALL}"
    elif stress < 80:
        return f"{Fore.LIGHTRED_EX}Very Stressed{Style.RESET_ALL}"
    else:
        return f"{Back.RED}{Fore.WHITE}Burnout Risk{Style.RESET_ALL}"


def handle_rumor_interaction(
    choice, name, personality, relationship_gain_mult=1.0, relationship_loss_mult=1.0
):
    """
    Handle rumor-related interaction options

    Arguments:
    choice -- The interaction choice (12=share gossip, 13=ask about rumors, 14=start rumor)
    name -- Name of the student being interacted with
    personality -- Personality of the student
    relationship_gain_mult -- Relationship gain multiplier
    relationship_loss_mult -- Relationship loss multiplier

    Returns:
    int -- Points gained/lost from the interaction
    """
    points_gain = 0

    if choice == "12":  # Share gossip
        if "rumors" not in player or not player["rumors"]:
            slow_print(
                f"{name}: I haven't heard any interesting gossip lately. Do you know something I don't?"
            )
            return 0

        # Show the rumors you know
        slow_print(f"\n{Fore.MAGENTA}=== Gossip to Share ==={Style.RESET_ALL}")

        # Sort rumors by spread level (least known first)
        sorted_rumors = sorted(player["rumors"], key=lambda r: r.get("spread_level", 0))

        for i, rumor in enumerate(sorted_rumors, 1):
            # Determine rumor status based on spread level
            spread_level = rumor.get("spread_level", 1)

            if spread_level <= 2:
                status = f"{Fore.CYAN}(Secret - few people know this){Style.RESET_ALL}"
            elif spread_level <= 5:
                status = f"{Fore.YELLOW}(Some people are talking about this){Style.RESET_ALL}"
            else:
                status = f"{Fore.RED}(Widely known){Style.RESET_ALL}"

            # Show the rumor with its status
            print(f"{i}. {rumor['content']} {status}")

        print("0. Never mind, I don't want to share anything")

        # Let player choose which rumor to share
        rumor_choice = input(
            f"\nWhich rumor would you like to share? (0-{len(sorted_rumors)}): "
        )
        try:
            choice_num = int(rumor_choice)
            if choice_num == 0:
                slow_print("You decide not to share any gossip.")
                return 0

            if 1 <= choice_num <= len(sorted_rumors):
                selected_rumor = sorted_rumors[choice_num - 1]

                # Different reactions based on personality
                if personality == "gossip":
                    slow_print(
                        f"{name}: Ohhh, that's juicy! I'm definitely telling everyone about this!"
                    )
                    points_gain = int(random.randint(5, 8) * relationship_gain_mult)
                    # Gossip personalities spread rumors faster
                    selected_rumor["spread_level"] = min(
                        10, selected_rumor["spread_level"] + 2
                    )
                elif personality == "serious" or personality == "kuudere":
                    slow_print(
                        f"{name}: I see. That's not particularly interesting to me, but I appreciate you sharing."
                    )
                    points_gain = int(random.randint(1, 3) * relationship_gain_mult)
                    # Serious personalities rarely spread gossip
                    if random.random() < 0.3:
                        selected_rumor["spread_level"] = min(
                            10, selected_rumor["spread_level"] + 1
                        )
                else:
                    slow_print(
                        f"{name}: Oh wow, I hadn't heard that! Thanks for telling me."
                    )
                    points_gain = int(random.randint(3, 6) * relationship_gain_mult)
                    # Normal spread increase
                    selected_rumor["spread_level"] = min(
                        10, selected_rumor["spread_level"] + 1
                    )

                # Chance for relationship benefit/penalty based on rumor type
                if "target" in selected_rumor:
                    target = selected_rumor["target"]
                    if name == target:
                        # Shared a rumor about this person - big relationship penalty!
                        slow_print(
                            f"{Fore.RED}{name} suddenly looks upset.{Style.RESET_ALL}"
                        )
                        slow_print(
                            f"{name}: Wait... people are saying that about ME? And you're spreading it?"
                        )
                        points_gain = -int(
                            random.randint(10, 20) * relationship_loss_mult
                        )
                    elif target in relationship:
                        # Target is someone this person knows
                        if relationship.get(target, 0) > 50:  # They like the target
                            slow_print(
                                f'{name} frowns. "That\'s not very nice to say about {target}."'
                            )
                            points_gain = -int(
                                random.randint(3, 8) * relationship_loss_mult
                            )

            else:
                slow_print("Invalid choice.")
        except ValueError:
            slow_print("Please enter a number.")

    elif choice == "13":  # Ask about rumors
        # Personality affects how likely they are to share rumors
        gossip_chance = 0.7  # Base chance

        if personality == "gossip":
            gossip_chance = 0.9  # Gossip personalities almost always share rumors
        elif personality in ["serious", "kuudere"]:
            gossip_chance = 0.4  # Serious personalities are less likely to gossip
        elif personality == "shy" or personality == "dandere":
            gossip_chance = 0.5  # Shy personalities are somewhat reluctant

        if random.random() < gossip_chance:
            # They share a rumor
            slow_print(f"{name} leans in and whispers:")

            # Either share an existing rumor or create a new one
            if "rumors" in player and player["rumors"] and random.random() < 0.7:
                # Share an existing rumor but increase its spread
                rumor = random.choice(player["rumors"])
                slow_print(f"\"{rumor['content']}\"")
                rumor["spread_level"] = min(10, rumor["spread_level"] + 1)
            else:
                # Generate a new rumor
                generate_random_rumor()
                if "rumors" in player and player["rumors"]:
                    new_rumor = player["rumors"][-1]  # Get the last added rumor
                    slow_print(f"\"{new_rumor['content']}\"")

            # Relationship gain
            slow_print(f"(You appreciate {name} sharing this rumor with you)")
            points_gain = int(random.randint(3, 6) * relationship_gain_mult)
        else:
            # They refuse to gossip
            if personality in ["serious", "kuudere"]:
                slow_print(
                    f"{name}: I don't participate in idle gossip. It's beneath me."
                )
            elif personality == "shy" or personality == "dandere":
                slow_print(f"{name}: I... um... don't really know any rumors. Sorry...")
            else:
                slow_print(
                    f"{name}: I don't have any interesting gossip right now. Maybe ask me later?"
                )
            points_gain = int(
                random.randint(1, 2) * relationship_gain_mult
            )  # Small gain for interaction

    elif choice == "14":  # Start a rumor
        # Show rumor type options
        print("\nWhat kind of rumor do you want to start?")
        rumor_types = {
            1: "Romantic rumor (about relationships)",
            2: "Academic rumor (about classes/grades)",
            3: "Social rumor (about student behaviors)",
            4: "Scandal rumor (juicy campus secrets)",
        }

        for num, desc in rumor_types.items():
            print(f"{num}. {desc}")

        type_choice = input("Select rumor type (1-4): ")
        try:
            type_num = int(type_choice)
            if 1 <= type_num <= 4:
                # Map selection to rumor type
                rumor_type_map = {
                    1: "romantic",
                    2: "academic",
                    3: "social",
                    4: "scandal",
                }
                selected_type = rumor_type_map[type_num]

                # Ask if the rumor targets someone specific
                print("\nDo you want this rumor to be about a specific person?")
                print("1. Yes, target someone")
                print("2. No, just a general rumor")

                target_choice = input("Choice (1-2): ")
                target_name = None

                if target_choice == "1":
                    # Show available students to target
                    print("\nWho do you want to start a rumor about?")
                    for i, student in enumerate(students, 1):
                        print(f"{i}. {student['name']}")

                    student_choice = input(f"Select a student (1-{len(students)}): ")
                    try:
                        student_num = int(student_choice)
                        if 1 <= student_num <= len(students):
                            target_name = students[student_num - 1]["name"]
                        else:
                            slow_print(
                                "Invalid choice. Starting a general rumor instead."
                            )
                    except ValueError:
                        slow_print("Invalid input. Starting a general rumor instead.")

                # Now create the rumor content
                print("\nWhat rumor do you want to start?")

                # Generate some suggestions based on type and target
                suggestions = []
                if selected_type == "romantic":
                    if target_name:
                        suggestions = [
                            f"{target_name} has a secret crush on someone in the school.",
                            f"{target_name} was caught writing love letters in class.",
                            f"{target_name} has been secretly dating someone from a rival school.",
                        ]
                    else:
                        suggestions = [
                            "Two teachers might be having a secret relationship.",
                            "There's going to be a new dating app just for our school.",
                            "The upcoming dance might be cancelled due to 'inappropriate behavior' last year.",
                        ]
                elif selected_type == "academic":
                    if target_name:
                        suggestions = [
                            f"{target_name} somehow got access to test answers before the exam.",
                            f"{target_name} is actually failing most classes despite acting smart.",
                            f"The teachers grade {target_name} more easily than other students.",
                        ]
                    else:
                        suggestions = [
                            "Next week's exams will have surprise trick questions.",
                            "The grading curve is going to be removed next semester.",
                            "A famous college scout is coming to look for potential students.",
                        ]
                elif selected_type == "social":
                    if target_name:
                        suggestions = [
                            f"{target_name} is secretly part of an underground gaming group.",
                            f"{target_name} got into a fight at a party last weekend.",
                            f"{target_name} has a secret talent no one knows about.",
                        ]
                    else:
                        suggestions = [
                            "The cafeteria is going to start serving international cuisine.",
                            "There's a secret underground club in the school basement.",
                            "A famous celebrity might be visiting the school soon.",
                        ]
                elif selected_type == "scandal":
                    if target_name:
                        suggestions = [
                            f"{target_name} got caught sneaking into the teachers' lounge.",
                            f"{target_name} is planning to drop out of school.",
                            f"{target_name} got into huge trouble for something off-campus.",
                        ]
                    else:
                        suggestions = [
                            "School funds for the festival were misused by someone in administration.",
                            "Several students are creating a petition against a strict teacher.",
                            "Someone hacked the school's computer system last week.",
                        ]

                # Display suggestions
                print("\nSuggestions (or type your own):")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")

                custom_rumor = input("\nEnter rumor (or number from suggestions): ")

                # Check if user selected a suggestion
                rumor_content = custom_rumor
                try:
                    suggestion_num = int(custom_rumor)
                    if 1 <= suggestion_num <= len(suggestions):
                        rumor_content = suggestions[suggestion_num - 1]
                except ValueError:
                    # They typed their own rumor, use that
                    pass

                # Create the rumor
                created_rumor = create_custom_rumor(
                    rumor_content, rumor_type=selected_type, target=target_name
                )

                # Relationship effects of starting a rumor
                if personality == "gossip":
                    slow_print(
                        f"{name}: Ohhh, that's spicy! I'll definitely help spread that around!"
                    )
                    created_rumor["spread_level"] += 1  # They help spread it
                    points_gain = int(random.randint(4, 8) * relationship_gain_mult)
                elif personality in ["serious", "kuudere"]:
                    slow_print(
                        f"{name}: I don't think it's appropriate to spread unverified information."
                    )
                    slow_print(f"{name} gives you a disapproving look.")
                    points_gain = -int(random.randint(3, 7) * relationship_loss_mult)
                else:
                    slow_print(f"{name}: Really? Wow, I hadn't heard that before.")
                    slow_print(f"{name} seems interested but a bit skeptical.")
                    created_rumor["spread_level"] += random.choice(
                        [0, 1]
                    )  # May or may not help spread
                    points_gain = int(random.randint(1, 4) * relationship_gain_mult)

                # Warning about potential consequences
                slow_print(
                    f"\n{Fore.YELLOW}You've started a rumor. This might have social consequences later.{Style.RESET_ALL}"
                )

            else:
                slow_print("Invalid rumor type selection.")
        except ValueError:
            slow_print("Please enter a number.")
            
    # Flirting options
    elif choice == "15":  # Basic flirting
        if personality == "tsundere":
            slow_print(f"{Fore.MAGENTA}{name}: W-What? Why are you looking at me like that? I-It's not like I care!{Style.RESET_ALL}")
            slow_print(f"{Fore.CYAN}(Despite their protests, you notice a slight blush on their face){Style.RESET_ALL}")
            points_gain = int(random.randint(5, 8) * relationship_gain_mult)
        elif personality == "kuudere":
            slow_print(f"{Fore.MAGENTA}{name}: Your attempts at flirtation are... noted.{Style.RESET_ALL}")
            points_gain = int(random.randint(3, 6) * relationship_gain_mult)
        elif personality == "dandere":
            slow_print(f"{Fore.MAGENTA}{name}: *blushes deeply and looks away* ... *smiles shyly*{Style.RESET_ALL}")
            points_gain = int(random.randint(6, 10) * relationship_gain_mult)
        elif personality == "deredere":
            slow_print(f"{Fore.MAGENTA}{name}: *giggles* You're so cute when you flirt with me!{Style.RESET_ALL}")
            points_gain = int(random.randint(7, 12) * relationship_gain_mult)
        elif personality == "yandere":
            slow_print(f"{Fore.MAGENTA}{name}: *intense stare* Are you flirting with me? Only me? It better be only me...{Style.RESET_ALL}")
            points_gain = int(random.randint(8, 15) * relationship_gain_mult)
        elif personality == "genki":
            slow_print(f"{Fore.MAGENTA}{name}: Oh! *bounces excitedly* Are we flirting now? This is fun!{Style.RESET_ALL}")
            points_gain = int(random.randint(6, 10) * relationship_gain_mult)
        elif personality == "himedere":
            slow_print(f"{Fore.MAGENTA}{name}: How bold of you to flirt with someone of my status. I'll allow it... this time.{Style.RESET_ALL}")
            points_gain = int(random.randint(4, 8) * relationship_gain_mult)
        else:
            slow_print(f"{Fore.MAGENTA}{name}: *smiles* That's sweet of you to say.{Style.RESET_ALL}")
            points_gain = int(random.randint(5, 9) * relationship_gain_mult)
        
        # Increase charisma slightly
        player["charisma"]["romantic"] += 1
        
    elif choice == "16":  # Compliment appearance
        if personality == "tsundere":
            slow_print(f"{Fore.MAGENTA}{name}: You think I look n-nice? Well, I didn't dress up for you or anything!{Style.RESET_ALL}")
            points_gain = int(random.randint(7, 12) * relationship_gain_mult)
        elif personality == "kuudere":
            slow_print(f"{Fore.MAGENTA}{name}: I appreciate the aesthetic evaluation. Your appearance is... also pleasing.{Style.RESET_ALL}")
            points_gain = int(random.randint(6, 10) * relationship_gain_mult)
        elif personality == "dandere":
            slow_print(f"{Fore.MAGENTA}{name}: *blushes deeply* T-thank you... you look nice too...{Style.RESET_ALL}")
            points_gain = int(random.randint(8, 14) * relationship_gain_mult)
        elif personality == "deredere":
            slow_print(f"{Fore.MAGENTA}{name}: Aww, thank you! I was hoping you'd notice! You always look amazing too!{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 15) * relationship_gain_mult)
        elif personality == "yandere":
            slow_print(f"{Fore.MAGENTA}{name}: You like how I look? Good. I put a lot of effort into looking perfect for you. Only for you.{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 18) * relationship_gain_mult)
        elif personality == "genki":
            slow_print(f"{Fore.MAGENTA}{name}: Really?! Thanks! I think you look great too! We'd make such a cute couple, don't you think?{Style.RESET_ALL}")
            points_gain = int(random.randint(8, 13) * relationship_gain_mult)
        elif personality == "himedere":
            slow_print(f"{Fore.MAGENTA}{name}: Of course I look good. It's expected of someone of my standing. But... thank you for noticing.{Style.RESET_ALL}")
            points_gain = int(random.randint(7, 11) * relationship_gain_mult)
        else:
            slow_print(f"{Fore.MAGENTA}{name}: *blushes* Thank you so much. That's really sweet of you to say.{Style.RESET_ALL}")
            points_gain = int(random.randint(8, 12) * relationship_gain_mult)
            
        # Increase charisma
        player["charisma"]["romantic"] += 2
        
    elif choice == "17":  # Playful teasing
        if personality == "tsundere":
            slow_print(f"{Fore.MAGENTA}{name}: Hey! Who said you could tease me?! *playfully pushes your shoulder* Two can play at that game!{Style.RESET_ALL}")
            points_gain = int(random.randint(9, 15) * relationship_gain_mult)
        elif personality == "kuudere":
            slow_print(f"{Fore.MAGENTA}{name}: Your attempt at humor is... not entirely unwelcome. *gives the smallest hint of a smile*{Style.RESET_ALL}")
            points_gain = int(random.randint(7, 12) * relationship_gain_mult)
        elif personality == "dandere":
            slow_print(f"{Fore.MAGENTA}{name}: *looks surprised, then giggles softly* I... I didn't know you could be so playful...{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 16) * relationship_gain_mult)
        elif personality == "deredere":
            slow_print(f"{Fore.MAGENTA}{name}: *laughs brightly* Oh you! *playfully teases you back* We're so cute together!{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 18) * relationship_gain_mult)
        elif personality == "yandere":
            slow_print(f"{Fore.MAGENTA}{name}: *grins* Oh? You're being playful with me? *moves closer* I can play too... but my games are a bit... different.{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 20) * relationship_gain_mult)
        elif personality == "genki":
            slow_print(f"{Fore.MAGENTA}{name}: *giggles and bounces* Hey! *playfully pokes you back* This is so much fun!{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 15) * relationship_gain_mult)
        elif personality == "himedere":
            slow_print(f"{Fore.MAGENTA}{name}: How bold! *raises eyebrow but smiles* Not many would dare tease royalty. You're... different.{Style.RESET_ALL}")
            points_gain = int(random.randint(9, 14) * relationship_gain_mult)
        else:
            slow_print(f"{Fore.MAGENTA}{name}: *laughs* You're so funny! I like this side of you.{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 15) * relationship_gain_mult)
            
        # Increase charisma
        player["charisma"]["romantic"] += 2
        player["charisma"]["social"] += 1
        
    elif choice == "18":  # Hold hands
        if personality == "tsundere":
            slow_print(f"{Fore.MAGENTA}{name}: *blushes deeply* W-what are you doing? *doesn't pull away* F-fine, if you insist...{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 18) * relationship_gain_mult)
        elif personality == "kuudere":
            slow_print(f"{Fore.MAGENTA}{name}: *looks at your hand, then slowly takes it* This physical contact is... acceptable.{Style.RESET_ALL}")
            points_gain = int(random.randint(10, 16) * relationship_gain_mult)
        elif personality == "dandere":
            slow_print(f"{Fore.MAGENTA}{name}: *looks shocked but then smiles warmly and gently holds your hand* ...thank you.{Style.RESET_ALL}")
            points_gain = int(random.randint(14, 20) * relationship_gain_mult)
        elif personality == "deredere":
            slow_print(f"{Fore.MAGENTA}{name}: *beams and intertwines fingers with yours* I've been hoping you'd do this!{Style.RESET_ALL}")
            points_gain = int(random.randint(15, 22) * relationship_gain_mult)
        elif personality == "yandere":
            slow_print(f"{Fore.MAGENTA}{name}: *grabs your hand tightly* Yes. Perfect. Now everyone can see that you're mine.{Style.RESET_ALL}")
            points_gain = int(random.randint(15, 25) * relationship_gain_mult)
        elif personality == "genki":
            slow_print(f"{Fore.MAGENTA}{name}: *gasps excitedly and swings your hand* Yay! Let's go for a walk like this!{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 18) * relationship_gain_mult)
        elif personality == "himedere":
            slow_print(f"{Fore.MAGENTA}{name}: *appears shocked* Such a public display... *softens and takes your hand* Well, I suppose it's fitting for someone at my side.{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 18) * relationship_gain_mult)
        else:
            slow_print(f"{Fore.MAGENTA}{name}: *smiles warmly and holds your hand gently* This feels nice.{Style.RESET_ALL}")
            points_gain = int(random.randint(12, 18) * relationship_gain_mult)
            
        # Increase relationship faster and boost romantic charisma
        player["charisma"]["romantic"] += 3
            
    return points_gain


def update_mental_health():
    """Update mental health stats based on various factors"""
    mental_health = player["mental_health"]

    # Depression increases with bullying incidents and decreases with therapy/support
    if mental_health["bullying_incidents"] > 5:
        mental_health["depression"] = min(
            100,
            mental_health["depression"] + (mental_health["bullying_incidents"] // 5),
        )
        mental_health["self_esteem"] = max(
            0, mental_health["self_esteem"] - (mental_health["bullying_incidents"] // 7)
        )

    # Breakups affect depression and self-esteem
    if mental_health["breakup_count"] > 0:
        mental_health["depression"] = min(
            100, mental_health["depression"] + (mental_health["breakup_count"] * 5)
        )
        mental_health["self_esteem"] = max(
            0, mental_health["self_esteem"] - (mental_health["breakup_count"] * 7)
        )

    # Support network helps reduce depression
    support_factor = mental_health["support_network"] / 100  # 0 to 1 scale
    depression_reduction = support_factor * 10  # Up to 10 points reduction
    mental_health["depression"] = max(
        0, mental_health["depression"] - depression_reduction
    )

    # Happiness is affected by various factors
    mental_health["happiness"] = max(
        0,
        min(
            100,
            80
            - mental_health["depression"] // 2
            - mental_health["anxiety"] // 3
            + mental_health["self_esteem"] // 4,
        ),
    )

    # Apply mental health effects to gameplay
    if mental_health["depression"] > 70:
        slow_print(
            f"{Fore.RED}You're feeling very depressed. Consider seeking therapy.{Style.RESET_ALL}"
        )
        decrease_energy(15)  # Severe depression drains energy
    elif mental_health["depression"] > 40:
        slow_print(f"{Fore.YELLOW}You're feeling down today.{Style.RESET_ALL}")
        decrease_energy(7)  # Moderate depression affects energy

    if mental_health["anxiety"] > 60:
        slow_print(
            f"{Fore.RED}Your anxiety is severe today, making it hard to focus.{Style.RESET_ALL}"
        )
        increase_stress(10)  # Severe anxiety increases stress
    elif mental_health["anxiety"] > 30:
        slow_print(f"{Fore.YELLOW}You're feeling anxious today.{Style.RESET_ALL}")
        increase_stress(5)  # Moderate anxiety affects stress


def attend_therapy():
    """Attend therapy session to improve mental health"""
    mental_health = player["mental_health"]

    # Check if player has enough money for therapy
    therapy_cost = 5000
    if player["money"] < therapy_cost:
        slow_print(
            f"{Fore.RED}You don't have enough money for therapy (costs {therapy_cost} yen).{Style.RESET_ALL}"
        )
        return False

    # Pay for therapy
    player["money"] -= therapy_cost
    mental_health["therapy_sessions"] += 1
    mental_health["last_therapy_date"] = current_date

    # Therapy effects
    mental_health["depression"] = max(0, mental_health["depression"] - 15)
    mental_health["anxiety"] = max(0, mental_health["anxiety"] - 10)
    mental_health["self_esteem"] = min(100, mental_health["self_esteem"] + 5)

    slow_print(
        f"{Fore.GREEN}Your therapy session was helpful. You feel a bit better.{Style.RESET_ALL}"
    )
    slow_print(f"Depression: {mental_health['depression']}/100")
    slow_print(f"Anxiety: {mental_health['anxiety']}/100")
    slow_print(f"Self-esteem: {mental_health['self_esteem']}/100")

    # Additional benefits from multiple sessions
    if mental_health["therapy_sessions"] >= 5:
        slow_print(
            f"{Fore.CYAN}You've developed better coping mechanisms from regular therapy.{Style.RESET_ALL}"
        )
        mental_health["support_network"] = min(
            100, mental_health["support_network"] + 10
        )

    return True


def build_support_network():
    """Strengthen your support network through social connections"""
    mental_health = player["mental_health"]

    # Count close relationships (over 70 points)
    close_friends = 0
    for name, points in player["relationships"].items():
        if points >= 70:
            close_friends += 1

    # Family support - check average family relationship
    family_support = 0
    if player["family_relationship"]:
        family_support = sum(player["family_relationship"].values()) / len(
            player["family_relationship"]
        )
        family_support = family_support / 20  # Convert to 0-5 scale

    # Club membership provides additional support
    club_support = min(5, len(player["clubs"]))

    # Calculate overall support network
    mental_health["support_network"] = min(
        100, 10 + (close_friends * 10) + (family_support * 5) + (club_support * 5)
    )

    return mental_health["support_network"]


def process_bullying_event(severity):
    """Process a bullying event and its effects on mental health"""
    mental_health = player["mental_health"]
    mental_health["bullying_incidents"] += 1

    # Immediate effects
    increase_stress(5 + severity * 3)

    # Mental health effects
    depression_increase = severity * 2
    anxiety_increase = severity * 3
    self_esteem_decrease = severity * 1

    mental_health["depression"] = min(
        100, mental_health["depression"] + depression_increase
    )
    mental_health["anxiety"] = min(100, mental_health["anxiety"] + anxiety_increase)
    mental_health["self_esteem"] = max(
        0, mental_health["self_esteem"] - self_esteem_decrease
    )

    # Compound effect for repeated bullying
    if mental_health["bullying_incidents"] > 3:
        slow_print(
            f"{Fore.RED}The repeated bullying is starting to affect your mental health.{Style.RESET_ALL}"
        )

        # After multiple incidents, suggest coping mechanisms
        if mental_health["bullying_incidents"] == 5:
            coping_options = [
                "Talk to a teacher or counselor about what's happening",
                "Confide in a friend or family member for support",
                "Join a club or group with supportive peers",
                "Consider therapy sessions",
            ]
            slow_print(
                f"\n{Fore.YELLOW}Coping strategies you might consider:{Style.RESET_ALL}"
            )
            for option in coping_options:
                slow_print(f"- {option}")

    # Provide mental health status update
    update_mental_health()


def update_health():
    """Update overall health based on stress, hunger, energy and mental health"""
    global ticks
    stress_factor = (100 - player["stress"]) * 0.4  # Higher stress means lower health
    hunger_factor = player["hunger"] * 0.3  # Higher hunger means better health
    energy_factor = player["energy"] * 0.3  # Higher energy means better health

    # Mental health now affects physical health
    mental_health_factor = 0
    if player["mental_health"]["depression"] > 50:
        mental_health_factor = -10  # Severe depression reduces health
    elif player["mental_health"]["anxiety"] > 60:
        mental_health_factor = -5  # Severe anxiety reduces health

    player["health"] = min(
        100,
        max(
            0, int(stress_factor + hunger_factor + energy_factor + mental_health_factor)
        ),
    )

    # Give player feedback if health is critically low
    if player["health"] < 30 and player["health"] > 0:
        slow_print(
            f"{Fore.RED}Warning: Your health is getting very low. Try to eat, rest, and reduce stress.{Style.RESET_ALL}"
        )
    elif player["health"] <= 0:
        slow_print(
            f"{Fore.RED}Your health has reached a critical level. You've been taken to the school nurse.{Style.RESET_ALL}"
        )
        player["health"] = 20  # Emergency treatment
        player["stress"] = 70
        player["energy"] = 30
        player["hunger"] = 30
        player["current_location"] = "Nurse's Office"
        ticks += 20  # Time passes while recovering

        # Nurse may notice mental health issues
        if (
            player["mental_health"]["depression"] > 50
            or player["mental_health"]["anxiety"] > 50
        ):
            slow_print(
                f"\n{Fore.YELLOW}The school nurse seems concerned about your mental state.{Style.RESET_ALL}"
            )
            slow_print(
                '"I\'m noticing some signs of distress. Have you considered talking to someone about it?"'
            )
            slow_print(
                "She gives you some information about the school's counseling services."
            )

            # Slight reduction in mental health symptoms from nurse intervention
            player["mental_health"]["depression"] = max(
                0, player["mental_health"]["depression"] - 5
            )
            player["mental_health"]["anxiety"] = max(
                0, player["mental_health"]["anxiety"] - 5
            )
            player["mental_health"][
                "support_network"
            ] += 2  # Small boost from knowing help is available


# Relationship Levels
RELATIONSHIP_LEVELS = {
    0: "Stranger",
    20: "Acquaintance",
    40: "Friend",
    60: "Good Friend",
    80: "Best Friend",
    90: "Close Friend",
}

# Ex-partner status definitions and behaviors
EX_PARTNER_STATUSES = {
    "moved_on": {
        "description": "Has moved on emotionally",
        "reconciliation_chance": 0.2,  # 20% chance
        "stalking_chance": 0.0,
        "dangerous_chance": 0.0,
        "events": [
            "greets you politely in the hallway.",
            "asks about your classes in a friendly way.",
            "mentions they hope you're doing well.",
            "introduces you to their new friend group.",
        ],
    },
    "still_interested": {
        "description": "Still has feelings for you",
        "reconciliation_chance": 0.5,  # 50% chance
        "stalking_chance": 0.1,
        "dangerous_chance": 0.0,
        "events": [
            "looks at you longingly from across the room.",
            "asks a mutual friend how you're doing.",
            "seems to 'accidentally' bump into you often.",
            "gets quiet when you talk about other people.",
        ],
    },
    "angry": {
        "description": "Upset about the breakup",
        "reconciliation_chance": 0.1,  # 10% chance
        "stalking_chance": 0.2,
        "dangerous_chance": 0.05,
        "events": [
            "glares at you when you pass each other.",
            "spreads negative rumors about you.",
            "makes a scene when you're in the same room.",
            "blocks you on all social media.",
            "argues with you over who gets to keep mutual friends.",
        ],
    },
    "yandere": {
        "description": "Obsessively attached",
        "reconciliation_chance": 0.7,  # 70% chance (they desperately want you back)
        "stalking_chance": 0.8,
        "dangerous_chance": 0.4,
        "events": [
            "appears unexpectedly wherever you go.",
            "watches you from a distance with an unsettling smile.",
            "sends you dozens of messages every day.",
            "somehow has detailed knowledge of your daily schedule.",
            "confronts anyone who gets close to you.",
            "leaves concerning 'gifts' in places only you would find them.",
        ],
    },
}

# Romance Stages
ROMANCE_STAGES = {
    0: {"name": "Stranger", "req": 0},
    1: {"name": "Acquainted", "req": 20},
    2: {"name": "Friends", "req": 40},
    3: {"name": "Close Friends", "req": 60},
    4: {"name": "Crushing", "req": 75},
    5: {"name": "Dating", "req": 90},
}

# Romance Interactions by Stage
ROMANCE_INTERACTIONS = {
    1: ["Small Talk", "Wave Hello"],
    2: ["Chat", "Study Together", "Walk Together"],
    3: ["Deep Conversation", "Have Lunch Together", "Share Secrets"],
    4: ["Hold Hands", "Special Gift", "Private Meeting"],
    5: ["Kiss", "Go on Date", "Plan Future", "Intimate Talk"],
}

# Date types with requirements and effects
DATE_TYPES = {
    "Coffee Shop": {
        "description": "A casual date at a cozy coffee shop",
        "cost": 1000,
        "min_stage": 2,
        "energy_cost": 10,
        "romance_gain": 10,
        "stress_change": -15,
        "locations": ["Restaurant District", "Shopping Mall"],
        "special_attribute": None,
    },
    "Movie": {
        "description": "Watch a film together at the cinema",
        "cost": 2000,
        "min_stage": 3,
        "energy_cost": 15,
        "romance_gain": 15,
        "stress_change": -20,
        "locations": ["Movie Theater"],
        "special_attribute": None,
    },
    "Dinner": {
        "description": "A romantic dinner at a nice restaurant",
        "cost": 3000,
        "min_stage": 3,
        "energy_cost": 20,
        "romance_gain": 20,
        "stress_change": -15,
        "locations": ["Restaurant District"],
        "special_attribute": None,
    },
    "Picnic": {
        "description": "A lovely picnic in the park",
        "cost": 1500,
        "min_stage": 3,
        "energy_cost": 25,
        "romance_gain": 20,
        "stress_change": -25,
        "locations": ["City Park"],
        "special_attribute": None,
    },
    "Amusement Park": {
        "description": "An exciting day at the amusement park",
        "cost": 4000,
        "min_stage": 4,
        "energy_cost": 40,
        "romance_gain": 25,
        "stress_change": -20,
        "locations": ["Amusement Park"],
        "special_attribute": "fun",
    },
    "Beach Day": {
        "description": "A relaxing day by the ocean",
        "cost": 2000,
        "min_stage": 4,
        "energy_cost": 35,
        "romance_gain": 25,
        "stress_change": -30,
        "locations": ["Beach"],
        "special_attribute": "relax",
    },
    "Shopping": {
        "description": "Go shopping together at the mall",
        "cost": 3000,
        "min_stage": 3,
        "energy_cost": 30,
        "romance_gain": 15,
        "stress_change": -10,
        "locations": ["Shopping Mall"],
        "special_attribute": "charisma",
    },
    "Karaoke": {
        "description": "Sing your hearts out at a karaoke bar",
        "cost": 2500,
        "min_stage": 3,
        "energy_cost": 25,
        "romance_gain": 20,
        "stress_change": -25,
        "locations": ["Karaoke Bar"],
        "special_attribute": "fun",
    },
    "Arcade": {
        "description": "Have fun playing games at the arcade",
        "cost": 2000,
        "min_stage": 2,
        "energy_cost": 20,
        "romance_gain": 15,
        "stress_change": -20,
        "locations": ["Arcade Center"],
        "special_attribute": "fun",
    },
    "Fancy Date": {
        "description": "A special high-end romantic evening",
        "cost": 5000,
        "min_stage": 5,
        "energy_cost": 35,
        "romance_gain": 35,
        "stress_change": -30,
        "locations": ["Restaurant District"],
        "special_attribute": "milestone",
    },
    "Stargazing": {
        "description": "A peaceful night watching the stars together",
        "cost": 500,
        "min_stage": 4,
        "energy_cost": 15,
        "romance_gain": 30,
        "stress_change": -35,
        "locations": ["City Park"],
        "special_attribute": "milestone",
    },
}

# Roommate NPC setup
roommate = None
roommate_seen = False

# Curfew time setup
CURFEW_HOUR = 22  # 10:00 PM
curfew_violations = 0


def assign_random_roommate():
    global roommate
    
    # Check if player has a twin sibling who can be their roommate
    has_twin_roommate = False
    if "family" in player and "siblings" in player["family"]:
        for sibling in player["family"]["siblings"]:
            if "relation" in sibling and "twin" in sibling.get("relation", ""):
                # 75% chance that twin will be your roommate if you have one
                if random.random() < 0.75:
                    has_twin_roommate = True
                    roommate = {
                        "name": sibling["name"],
                        "personality": sibling["personality"],
                        "is_twin": True,
                        "relation": sibling["relation"]
                    }
                    
                    # Higher starting relationship with twin roommate
                    roommate["relationship"] = str(player["family_relationship"].get(sibling["name"], 50))
                    
                    slow_print(f"{Fore.MAGENTA}By coincidence, your {sibling['relation']}, {sibling['name']}, is your roommate!{Style.RESET_ALL}")
                    break
    
    # If no twin or twin not selected to be roommate, choose a random roommate
    if not has_twin_roommate:
        possible_roommates = [
            {"name": "Aiko Watanabe", "personality": "kind"},
            {"name": "Kenji Takahashi", "personality": "serious"},
            {"name": "Mika Suzuki", "personality": "lazy"},
            {"name": "Daichi Yamamoto", "personality": "strict"},
        ]
        roommate = random.choice(possible_roommates)
        roommate["relationship"] = "20"  # Starting relationship points


assign_random_roommate()
player["current_location"] = "Student Room 364"


def improve_relationship(name, points):
    # No need for global since we're just modifying a dictionary, not reassigning it
    if name not in relationship:
        relationship[name] = 0

    # Roommate relationship improves faster
    if roommate and name == roommate["name"]:
        points = int(points * 1.5)

    relationship[name] += points

    # Check for romantic relationship progression
    if player["romantic_interest"] and player["romantic_interest"] == name:
        player["romance_points"] += points

        # Check if we can advance to next romance stage
        current_stage = player["romance_stage"]
        next_stage = current_stage + 1

        if (
            next_stage in ROMANCE_STAGES
            and player["romance_points"] >= ROMANCE_STAGES[next_stage]["req"]
        ):
            player["romance_stage"] = next_stage
            stage_name = ROMANCE_STAGES[next_stage]["name"]
            slow_print(
                f"\n{Fore.MAGENTA}♥ Your relationship with {name} has advanced to '{stage_name}'! ♥{Style.RESET_ALL}"
            )

            # Unlock romance achievement if reached Dating stage
            if next_stage == 5 and "Romance Expert" not in player["achievements"]:
                player["achievements"].append("Romance Expert")
                slow_print(
                    f"{Fore.YELLOW}Achievement unlocked: Romance Expert{Style.RESET_ALL}"
                )
                slow_print("Your social charisma has increased!")
                player["charisma"]["social"] += 4


# Modify random_friendship_event to improve roommate relationship faster
def random_friendship_event():
    student = random.choice(students)
    name = student["name"]
    if (
        name not in relationship or relationship[name] < 20
    ):  # Only for students you don't know well
        chance = min(
            (player["charisma"]["social"] + player["charisma"]["academic"]) / 100, 0.8
        )
        if random.random() < chance:
            slow_print(
                f"\n{Fore.CYAN}Event: {name} wants to be friends with you!{Style.RESET_ALL}"
            )
            choice = input("Accept? (y/n): ").lower()
            if choice == "y":
                relationship[name] = max(
                    relationship.get(name, 0) + random.randint(15, 25), 40
                )
                student_status[name] = "Friend"
                slow_print(
                    f"{Fore.GREEN}You are now friends with {name}!{Style.RESET_ALL}"
                )
                player["charisma"]["social"] += 2


def eat_food(food_name):
    if food_name not in cafeteria_menu:
        print("That food is not available.")
        return
    food = cafeteria_menu[food_name]
    if player["money"] < food["price"]:
        print("You don't have enough money to buy that.")
        return
    player["money"] -= food["price"]
    player["energy"] = min(player["energy"] + food["energy_gain"], 100)
    player["hunger"] = min(player["hunger"] + food["hunger_gain"], 100)
    player["stress"] = max(0, player["stress"] - food["stress_reduction"])

    update_health()  # Update overall health after eating

    slow_print(
        f"You ate {food_name}. Energy +{food['energy_gain']}, Hunger +{food['hunger_gain']}, Stress -{food['stress_reduction']}."
    )
    slow_print(f"Health: {get_health_indicator()}, Stress: {get_stress_indicator()}")


# Add /eat command handler
def eat_command(args):
    if not args:
        print("Usage: /eat [food item]")
        print("Available food items:")
        for item in cafeteria_menu:
            print(f"- {item} (¥{cafeteria_menu[item]['price']})")
        return
    food_name = " ".join(args)
    eat_food(food_name)


# Game time and ticks
current_date = datetime(2024, 4, 1)  # Start of school year
SCHOOL_YEAR_END = datetime(2025, 3, 31)
ticks = 0  # 10 ticks = 1 hour, 240 ticks = 1 day (24 hours * 10)
MAX_TICKS_PER_DAY = 240

# Player dorm room and roommate
player["current_location"] = "Student Room 364"
roommate = {
    "name": "Aiko Watanabe",
    "personality": "kind",
    "relationship": 20,  # Starting relationship points
}

# Subjects by Year (1-4) with Difficulty Level
all_subjects = {
    # First Year Subjects
    "Math I": {"difficulty": 3, "homework_freq": 0.7, "year": 1, "core": True},
    "English I": {"difficulty": 3, "homework_freq": 0.6, "year": 1, "core": True},
    "Science I": {"difficulty": 4, "homework_freq": 0.8, "year": 1, "core": True},
    "History I": {"difficulty": 3, "homework_freq": 0.6, "year": 1, "core": True},
    "Literature I": {"difficulty": 3, "homework_freq": 0.5, "year": 1, "core": True},
    "PE I": {"difficulty": 2, "homework_freq": 0.3, "year": 1, "core": True},
    "Art": {"difficulty": 2, "homework_freq": 0.4, "year": 1, "core": False},
    "Music": {"difficulty": 2, "homework_freq": 0.4, "year": 1, "core": False},
    "Computer Basics": {
        "difficulty": 2,
        "homework_freq": 0.5,
        "year": 1,
        "core": False,
    },
    "Economics Basics": {
        "difficulty": 3,
        "homework_freq": 0.6,
        "year": 1,
        "core": False,
    },
    "Psychology Intro": {
        "difficulty": 3,
        "homework_freq": 0.5,
        "year": 1,
        "core": False,
    },
    # Second Year Subjects
    "Math II": {"difficulty": 4, "homework_freq": 0.8, "year": 2, "core": True},
    "English II": {"difficulty": 3, "homework_freq": 0.7, "year": 2, "core": True},
    "Physics": {"difficulty": 5, "homework_freq": 0.9, "year": 2, "core": False},
    "Chemistry": {"difficulty": 5, "homework_freq": 0.9, "year": 2, "core": False},
    "Biology": {"difficulty": 4, "homework_freq": 0.8, "year": 2, "core": False},
    "World History": {"difficulty": 4, "homework_freq": 0.7, "year": 2, "core": True},
    "Literature II": {"difficulty": 3, "homework_freq": 0.6, "year": 2, "core": True},
    "PE II": {"difficulty": 2, "homework_freq": 0.3, "year": 2, "core": True},
    "Computer Science": {
        "difficulty": 4,
        "homework_freq": 0.7,
        "year": 2,
        "core": False,
    },
    "Business Studies": {
        "difficulty": 3,
        "homework_freq": 0.6,
        "year": 2,
        "core": False,
    },
    "Sociology": {"difficulty": 3, "homework_freq": 0.5, "year": 2, "core": False},
    # Third Year Subjects
    "Math III": {"difficulty": 5, "homework_freq": 0.9, "year": 3, "core": True},
    "English III": {"difficulty": 4, "homework_freq": 0.8, "year": 3, "core": True},
    "Advanced Physics": {
        "difficulty": 6,
        "homework_freq": 0.9,
        "year": 3,
        "core": False,
    },
    "Advanced Chemistry": {
        "difficulty": 6,
        "homework_freq": 0.9,
        "year": 3,
        "core": False,
    },
    "Advanced Biology": {
        "difficulty": 5,
        "homework_freq": 0.8,
        "year": 3,
        "core": False,
    },
    "Political Science": {
        "difficulty": 4,
        "homework_freq": 0.7,
        "year": 3,
        "core": False,
    },
    "Literature III": {"difficulty": 4, "homework_freq": 0.7, "year": 3, "core": True},
    "PE III": {"difficulty": 2, "homework_freq": 0.3, "year": 3, "core": True},
    "Programming": {"difficulty": 5, "homework_freq": 0.8, "year": 3, "core": False},
    "Economics": {"difficulty": 4, "homework_freq": 0.7, "year": 3, "core": False},
    "Philosophy": {"difficulty": 4, "homework_freq": 0.6, "year": 3, "core": False},
    # Fourth Year Subjects
    "Math IV": {"difficulty": 6, "homework_freq": 0.9, "year": 4, "core": True},
    "English IV": {"difficulty": 5, "homework_freq": 0.8, "year": 4, "core": True},
    "Thesis Research": {"difficulty": 7, "homework_freq": 1.0, "year": 4, "core": True},
    "Career Planning": {"difficulty": 3, "homework_freq": 0.5, "year": 4, "core": True},
    "Advanced Research": {
        "difficulty": 6,
        "homework_freq": 0.9,
        "year": 4,
        "core": False,
    },
    "International Relations": {
        "difficulty": 5,
        "homework_freq": 0.7,
        "year": 4,
        "core": False,
    },
    "Literature IV": {"difficulty": 5, "homework_freq": 0.7, "year": 4, "core": True},
    "PE IV": {"difficulty": 2, "homework_freq": 0.3, "year": 4, "core": False},
    "Software Development": {
        "difficulty": 6,
        "homework_freq": 0.8,
        "year": 4,
        "core": False,
    },
    "Business Management": {
        "difficulty": 5,
        "homework_freq": 0.7,
        "year": 4,
        "core": False,
    },
    "Ethics": {"difficulty": 4, "homework_freq": 0.6, "year": 4, "core": False},
}

# Current active subjects based on player's year
def get_subjects_for_year(year):
    """Get a dictionary of subjects with properties for a specific school year"""
    year_subjects = {}
    for subject_name, subject_data in all_subjects.items():
        if subject_data["year"] == year:
            year_subjects[subject_name] = subject_data
    return year_subjects


def get_current_subjects():
    """Get subjects relevant to player's current school year"""
    # Get the relevant subject data for the current school year
    subjects_data = get_subjects_for_year(player["school_year"])

    # Return just the list of subject names
    return list(subjects_data.keys())


# Update subjects when starting game or advancing year
subjects = {}  # Will be filled during setup_game or year progression

# Elective Subjects (subset of subjects for clarity)
elective_subjects = ["Music", "Computer Science", "Economics", "PE"]

homework = {}
teachers = []
students = []
relationship = {}
student_status = {}  # Stores relationship status with students

# Time system
game_time = {
    "hour": 8,    # Start the day at 8:00 AM
    "minute": 0
}
RELATIONSHIP_LEVELS = {
    0: "Stranger",
    20: "Acquaintance",
    40: "Friend",
    70: "Close Friend",
    90: "Best Friend/Dating",
}
quests = []


# Student Council
student_council = [
    {
        "name": "Yuki Tanaka",
        "role": "President",
        "gender": "F",
        "personality": "strict",
    },
    {
        "name": "Akira Suzuki",
        "role": "Vice President",
        "gender": "M",
        "personality": "serious",
    },
    {
        "name": "Sakura Yamamoto",
        "role": "Secretary",
        "gender": "F",
        "personality": "kind",
    },
    {
        "name": "Ryo Nakamura",
        "role": "Treasurer",
        "gender": "M",
        "personality": "serious",
    },
]

# Club System
clubs = {
    "Soccer Club": {
        "description": "Compete in local tournaments and train your body.",
        "members": ["Daiki Yamamoto", "Kenta Suzuki", "Ryo Tanaka"],
        "president": "Daiki Yamamoto",
        "benefits": {
            "PE": 5,  # Subject bonus
            "charisma": {"social": 2, "academic": 0},
            "stress_reduction": 5,
            "energy_cost": 15,
        },
        "meeting_days": [1, 3, 5],  # Monday, Wednesday, Friday
        "location": "Gym",
    },
    "Science Club": {
        "description": "Explore physics, chemistry, and biology through experiments.",
        "members": ["Hikari Watanabe", "Yuto Nakamura", "Mika Ito"],
        "president": "Hikari Watanabe",
        "benefits": {
            "Science": 5,
            "charisma": {"social": 1, "academic": 3},
            "stress_reduction": 2,
            "energy_cost": 10,
        },
        "meeting_days": [2, 4],  # Tuesday, Thursday
        "location": "Science Lab",
    },
    "Art Club": {
        "description": "Express yourself through painting, drawing, and sculpture.",
        "members": ["Haruka Sato", "Mei Kobayashi", "Sota Yamamoto"],
        "president": "Haruka Sato",
        "benefits": {
            "Art": 5,
            "charisma": {"social": 2, "academic": 1},
            "stress_reduction": 8,
            "energy_cost": 8,
        },
        "meeting_days": [2, 5],  # Tuesday, Friday
        "location": "Art Studio",
    },
    "Music Club": {
        "description": "Practice instruments and perform in school concerts.",
        "members": ["Yuna Kato", "Haruto Ito", "Nanami Takahashi"],
        "president": "Yuna Kato",
        "benefits": {
            "Music": 5,
            "charisma": {"social": 3, "academic": 1},
            "stress_reduction": 6,
            "energy_cost": 12,
        },
        "meeting_days": [1, 4],  # Monday, Thursday
        "location": "Music Room",
    },
    "Computer Club": {
        "description": "Learn programming, game development, and computer science.",
        "members": ["Yamato Suzuki", "Akari Watanabe", "Kaito Nakamura"],
        "president": "Yamato Suzuki",
        "benefits": {
            "Computer Science": 5,
            "charisma": {"social": 1, "academic": 3},
            "stress_reduction": 3,
            "energy_cost": 10,
        },
        "meeting_days": [3, 5],  # Wednesday, Friday
        "location": "Computer Lab",
    },
    "Economics Club": {
        "description": "Discuss market trends and investment strategies.",
        "members": ["Taro Ito", "Saki Watanabe", "Ryota Takahashi"],
        "president": "Taro Ito",
        "benefits": {
            "Economics": 5,
            "charisma": {"social": 2, "academic": 2},
            "stress_reduction": 2,
            "energy_cost": 8,
        },
        "meeting_days": [2, 4],  # Tuesday, Thursday
        "location": "Classroom",
    },
    "Literature Club": {
        "description": "Read and discuss classic and modern literature.",
        "members": ["Misaki Sato", "Ryota Kobayashi", "Hikari Tanaka"],
        "president": "Misaki Sato",
        "benefits": {
            "Literature": 5,
            "charisma": {"social": 1, "academic": 3},
            "stress_reduction": 4,
            "energy_cost": 6,
        },
        "meeting_days": [1, 3],  # Monday, Wednesday
        "location": "Library",
    },
    "Debate Club": {
        "description": "Improve your critical thinking and public speaking.",
        "members": ["Kazuki Yamamoto", "Akari Suzuki", "Yuki Watanabe"],
        "president": "Kazuki Yamamoto",
        "benefits": {
            "English": 3,
            "charisma": {"social": 3, "academic": 2},
            "stress_reduction": 2,
            "energy_cost": 12,
        },
        "meeting_days": [2, 5],  # Tuesday, Friday
        "location": "Classroom",
    },
}

# Festivals and Special Events
special_events = {
    "Spring Festival": {
        "month": 5,
        "day": 15,
        "duration": 3,
        "description": "A celebration of spring with outdoor activities and performances.",
        "activities": [
            "Food Stalls",
            "Student Performances",
            "Sports Tournament",
            "Art Exhibition",
        ],
        "rewards": {"reputation": 10, "money": 1000, "stress_reduction": 20},
    },
    "Cultural Festival": {
        "month": 10,
        "day": 20,
        "duration": 2,
        "description": "Showcase of club activities, class projects, and student talents.",
        "activities": [
            "Class Exhibitions",
            "Club Performances",
            "Cosplay Contest",
            "Food Court",
        ],
        "rewards": {"reputation": 15, "money": 1500, "stress_reduction": 15},
    },
    "Winter Celebration": {
        "month": 12,
        "day": 20,
        "duration": 1,
        "description": "End-of-year party with gift exchanges and special performances.",
        "activities": [
            "Gift Exchange",
            "Winter Concert",
            "Special Dinner",
            "Year-in-Review",
        ],
        "rewards": {"reputation": 5, "money": 500, "stress_reduction": 25},
    },
    "Sports Day": {
        "month": 9,
        "day": 10,
        "duration": 1,
        "description": "Competitive sports events between classes and clubs.",
        "activities": [
            "Relay Race",
            "Tug of War",
            "Ball Games",
            "Swimming Competition",
        ],
        "rewards": {"reputation": 8, "money": 800, "stress_reduction": 10},
    },
}

# Festival System - Calendar of special events throughout the school year
FESTIVALS = {
    "Cherry Blossom Festival": {
        "date": (4, 10),  # April 10
        "description": "Celebrate the blooming cherry blossoms with picnics and outdoor activities.",
        "activities": [
            "Hanami Picnic",
            "Poetry Reading",
            "Photography Contest",
            "Outdoor Tea Ceremony",
        ],
        "special_rewards": {
            "Cherry Blossom Memories": "Stress reduction and increased social charisma"
        },
    },
    "Summer Beach Day": {
        "date": (7, 15),  # July 15
        "description": "A school trip to the beach for sun, sand, and fun.",
        "activities": [
            "Swimming",
            "Beach Volleyball",
            "Sand Castle Contest",
            "Barbecue Party",
        ],
        "special_rewards": {"Beach MVP": "Improved PE stats and social reputation"},
    },
    "Cultural Exchange Week": {
        "date": (11, 5),  # November 5
        "description": "A week dedicated to international cultural exchange and performances.",
        "activities": [
            "International Food Fair",
            "Language Exchange",
            "Cultural Performances",
            "Traditional Costume Display",
        ],
        "special_rewards": {
            "Global Citizen": "Academic charisma boost and language skill improvement"
        },
    },
    "Winter Formal Dance": {
        "date": (12, 15),  # December 15
        "description": "The annual formal dance before winter break.",
        "activities": [
            "Ballroom Dancing",
            "Photo Booth",
            "Formal Dinner",
            "Awards Ceremony",
        ],
        "special_rewards": {
            "Dance King/Queen": "Major social reputation boost and romance opportunity"
        },
    },
    "New Year Festival": {
        "date": (1, 5),  # January 5
        "description": "Ring in the new year with traditional activities and resolutions.",
        "activities": [
            "Bell Ringing Ceremony",
            "Fortune Telling",
            "New Year's Games",
            "Resolution Board",
        ],
        "special_rewards": {"Fresh Start": "Reset stress levels and gain bonus money"},
    },
    "Spring Sports Tournament": {
        "date": (5, 20),  # May 20
        "description": "Inter-school sports competition showcasing athletic talents.",
        "activities": [
            "Soccer Match",
            "Basketball Tournament",
            "Track and Field Events",
            "Swimming Competition",
        ],
        "special_rewards": {
            "Sports Champion": "Major PE grade boost and physical stat improvements"
        },
    },
}

# Achievement System
achievements = {
    "First Day": {
        "description": "Started your school life",
        "unlocked": False,
        "reward": {"money": 100},
    },
    "Social Butterfly": {
        "description": "Make friends with 5 different students",
        "unlocked": False,
        "condition": lambda: len([s for s, v in relationship.items() if v >= 40]) >= 5,
        "reward": {"charisma": {"social": 5}},
    },
    "Academic Excellence": {
        "description": "Get an A in all subjects",
        "unlocked": False,
        "condition": lambda: all(grade == "A" for grade in player["grades"].values()),
        "reward": {"charisma": {"academic": 10}},
    },
    "Perfect Attendance": {
        "description": "Don't miss school for a month",
        "unlocked": False,
        "reward": {"reputation": {"teachers": 10}},
    },
    "Club Leader": {
        "description": "Become president of a club",
        "unlocked": False,
        "reward": {"reputation": {"students": 15, "teachers": 5}},
    },
    "Festival Champion": {
        "description": "Win a competition during a school festival",
        "unlocked": False,
        "reward": {"money": 1000, "reputation": {"students": 10}},
    },
    "Romance Blooms": {
        "description": "Enter a romantic relationship",
        "unlocked": False,
        "reward": {"charisma": {"social": 5}},
    },
    "Work Ethic": {
        "description": "Work at a part-time job for 10 days",
        "unlocked": False,
        "reward": {"money": 2000},
    },
    "Stress Manager": {
        "description": "Keep your stress below 30 for a week",
        "unlocked": False,
        "reward": {"energy": 20},
    },
}

# Locations
school_locations = [
    "Classroom",
    "Courtyard",
    "Library",
    "Cafeteria",
    "Club Room",
    "Gym",
    "School Garden",
    "Rooftop",
    "Student Council Room",
    "Music Room",
    "Science Lab",
    "Art Studio",
    "Teachers' Office",
]

# Accommodation Locations
dorm_locations = ["Dorm Lobby", "Dorm Room"]
home_locations = ["Living Room", "Bedroom", "Kitchen", "Backyard", "Study Room"]

# Part-time Job Locations
job_locations = [
    "Convenience Store",
    "Library (Work)",
    "Cafe",
    "Bookstore",
    "Restaurant",
]

# Dating & Recreation Locations
dating_locations = [
    "Restaurant District",
    "Movie Theater",
    "Shopping Mall",
    "City Park",
    "Beach",
    "Amusement Park",
    "Karaoke Bar",
    "Arcade Center",
]

# Combined Locations
locations = (
    school_locations
    + dorm_locations
    + home_locations
    + job_locations
    + dating_locations
)

# Daily Life System
mealtime_hours = {
    "breakfast": (6, 9),  # 6:00 AM to 9:00 AM
    "lunch": (11, 14),  # 11:00 AM to 2:00 PM
    "dinner": (17, 21),  # 5:00 PM to 9:00 PM
}

bedtime_hours = (21, 6)  # 9:00 PM to 6:00 AM is appropriate sleep time

# Commute times (in minutes)
commute_times = {
    "dorm": 5,  # 5 minutes from dorm to school
    "home": 30,  # 30 minutes from home to school
}

# Anime-inspired personalities (now with more variety and relationship effects)
personalities = {
    # Original personalities
    "strict": {
        "homework_mult": 1.2,
        "grade_mult": 0.9,
        "romance_compatibility": 0.6,
        "relationship_gain": 2,
        "relationship_loss": 4,
    },
    "kind": {
        "homework_mult": 0.8,
        "grade_mult": 1.1,
        "romance_compatibility": 0.9,
        "relationship_gain": 4,
        "relationship_loss": 2,
    },
    "serious": {
        "homework_mult": 1.1,
        "grade_mult": 1.0,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 3,
    },
    "lazy": {
        "homework_mult": 0.7,
        "grade_mult": 1.2,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 2,
    },
    # New additional personalities
    "sarcastic": {
        "homework_mult": 0.9,
        "grade_mult": 1.1,
        "romance_compatibility": 0.7,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Uses humor and wit to deflect emotional situations. Can be charming but sometimes hurtful."
    },
    "energetic": {
        "homework_mult": 0.8,
        "grade_mult": 1.0,
        "romance_compatibility": 0.8,
        "relationship_gain": 4,
        "relationship_loss": 3,
        "special_trait": "Always on the go and enthusiastic about activities. Can be overwhelming but never boring."
    },
    "pessimistic": {
        "homework_mult": 1.0,
        "grade_mult": 0.9,
        "romance_compatibility": 0.5,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Expects the worst in most situations. Can be realistic but sometimes a downer."
    },
    "optimistic": {
        "homework_mult": 0.9,
        "grade_mult": 1.1,
        "romance_compatibility": 0.9,
        "relationship_gain": 4,
        "relationship_loss": 2,
        "special_trait": "Always looking on the bright side. Their positivity is contagious but can seem naive."
    },
    "competitive": {
        "homework_mult": 1.2,
        "grade_mult": 1.0,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 4,
        "special_trait": "Turns everything into a competition. Can be motivating but sometimes exhausting."
    },
    "intellectual": {
        "homework_mult": 1.3,
        "grade_mult": 0.8,
        "romance_compatibility": 0.7,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Values knowledge and deep conversations. Can be fascinating but sometimes condescending."
    },
    "artistic": {
        "homework_mult": 0.8,
        "grade_mult": 1.1,
        "romance_compatibility": 0.8,
        "relationship_gain": 3,
        "relationship_loss": 2,
        "special_trait": "Creative and expressive. Sees beauty in everything but can be emotionally volatile."
    },
    "athletic": {
        "homework_mult": 0.9,
        "grade_mult": 1.0,
        "romance_compatibility": 0.8,
        "relationship_gain": 3,
        "relationship_loss": 3,
        "special_trait": "Focused on physical activities and sports. Energetic and health-conscious."
    },
    "mischievous": {
        "homework_mult": 0.7,
        "grade_mult": 1.0,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 4,
        "special_trait": "Enjoys pranks and breaking minor rules. Fun to be around but can cause trouble."
    },
    "shy": {
        "homework_mult": 1.0,
        "grade_mult": 1.0,
        "romance_compatibility": 0.6,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Reserved and quiet. Takes time to open up but can be deeply loyal."
    },
    "adventurous": {
        "homework_mult": 0.7,
        "grade_mult": 1.0,
        "romance_compatibility": 0.8,
        "relationship_gain": 3,
        "relationship_loss": 2,
        "special_trait": "Always seeking new experiences. Exciting to be around but can be unpredictable."
    },
    "traditional": {
        "homework_mult": 1.1,
        "grade_mult": 0.9,
        "romance_compatibility": 0.7,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Values customs and established ways. Respectful but can be rigid."
    },
    "rebellious": {
        "homework_mult": 0.6,
        "grade_mult": 1.0,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 4,
        "special_trait": "Questions authority and pushes boundaries. Exciting but can be troublesome."
    },
    # Anime-inspired personality types
    "tsundere": {
        "homework_mult": 1.0,
        "grade_mult": 1.0,
        "romance_compatibility": 0.8,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Acts cold but actually cares deeply. Relationship grows slower at first, then faster with persistence.",
    },
    "kuudere": {
        "homework_mult": 1.3,
        "grade_mult": 0.8,
        "romance_compatibility": 0.6,
        "relationship_gain": 1,
        "relationship_loss": 4,
        "special_trait": "Emotionally distant but highly intelligent. Harder to build relationship, but very loyal once close.",
    },
    "dandere": {
        "homework_mult": 0.9,
        "grade_mult": 1.1,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 5,
        "special_trait": "Shy and quiet, but opens up when comfortable. Sensitive to negative interactions.",
    },
    "deredere": {
        "homework_mult": 0.7,
        "grade_mult": 1.2,
        "romance_compatibility": 1.0,
        "relationship_gain": 5,
        "relationship_loss": 3,
        "special_trait": "Always cheerful and affectionate. Relationships grow very quickly.",
    },
    "yandere": {
        "homework_mult": 1.1,
        "grade_mult": 1.0,
        "romance_compatibility": 0.4,
        "relationship_gain": 4,
        "relationship_loss": 8,
        "special_trait": "Obsessively devoted but potentially dangerous. Relationship points decrease when interacting with others.",
    },
    "genki": {
        "homework_mult": 0.8,
        "grade_mult": 1.1,
        "romance_compatibility": 0.9,
        "relationship_gain": 4,
        "relationship_loss": 2,
        "special_trait": "Energetic and optimistic. Great at social activities and clubs.",
    },
    "himedere": {
        "homework_mult": 1.2,
        "grade_mult": 0.9,
        "romance_compatibility": 0.5,
        "relationship_gain": 2,
        "relationship_loss": 5,
        "special_trait": "Acts like royalty and expects to be treated as such. Harder to please but loyal to those they respect.",
    },
    # Additional anime-inspired personalities
    "bokukko": {
        "homework_mult": 0.9,
        "grade_mult": 1.0,
        "romance_compatibility": 0.8,
        "relationship_gain": 3,
        "relationship_loss": 3,
        "special_trait": "Tomboyish personality who uses masculine speech. Excels in sports and physical activities.",
    },
    "chunibyo": {
        "homework_mult": 0.7,
        "grade_mult": 0.8,
        "romance_compatibility": 0.7,
        "relationship_gain": 2,
        "relationship_loss": 4,
        "special_trait": "Lives in a fantasy world and believes in special powers. Eccentric but endearing to those who understand them.",
    },
    "megane": {
        "homework_mult": 1.4,
        "grade_mult": 1.3,
        "romance_compatibility": 0.7,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Intellectual with glasses. Exceptional at studying and academic pursuits, but can be socially awkward.",
    },
    "ojou-sama": {
        "homework_mult": 1.0,
        "grade_mult": 1.0,
        "romance_compatibility": 0.6,
        "relationship_gain": 2,
        "relationship_loss": 4,
        "special_trait": "High class and elegant. Has refined tastes and expectations, but can be surprisingly down-to-earth.",
    },
    "otaku": {
        "homework_mult": 1.1,
        "grade_mult": 1.0,
        "romance_compatibility": 0.5,
        "relationship_gain": 2,
        "relationship_loss": 3,
        "special_trait": "Obsessed with anime, games, or other specific interests. Social relationship depends on shared interests.",
    },
    "sporty": {
        "homework_mult": 0.8,
        "grade_mult": 0.9,
        "romance_compatibility": 0.8,
        "relationship_gain": 3,
        "relationship_loss": 2,
        "special_trait": "Athletic and competitive. Excels in physical activities and has strong determination.",
    },
    "wise": {
        "homework_mult": 1.2,
        "grade_mult": 1.2,
        "romance_compatibility": 0.7,
        "relationship_gain": 3,
        "relationship_loss": 3,
        "special_trait": "Mature beyond their years, offering sage advice. Thoughtful and observant.",
    },
    "fashionista": {
        "homework_mult": 0.8,
        "grade_mult": 0.9,
        "romance_compatibility": 0.8,
        "relationship_gain": 4,
        "relationship_loss": 3,
        "special_trait": "Trend-conscious and socially savvy. Excels in style and social situations.",
    },
    "class-clown": {
        "homework_mult": 0.6,
        "grade_mult": 0.8,
        "romance_compatibility": 0.9,
        "relationship_gain": 5,
        "relationship_loss": 2,
        "special_trait": "Always joking and making others laugh. Very popular but sometimes not taken seriously.",
    },
    "edgy": {
        "homework_mult": 0.9,
        "grade_mult": 0.9,
        "romance_compatibility": 0.5,
        "relationship_gain": 2,
        "relationship_loss": 4,
        "special_trait": "Dark, brooding personality. Hard to get close to but has a strong sense of justice.",
    },
}

# Part-time jobs
jobs = {
    "Convenience Store": {"pay": 1500, "time": 4, "charisma_gain": 2},
    "Library Assistant": {"pay": 1200, "time": 3, "academic_gain": 3},
    "Cafe Worker": {"pay": 1800, "time": 5, "social_gain": 3},
    "Bookstore Clerk": {"pay": 1300, "time": 4, "academic_gain": 2, "charisma_gain": 1},
    "Delivery Assistant": {"pay": 1600, "time": 5, "charisma_gain": 2},
}

# Ranks based on points
ranks = {
    "students": {0: "Nobody", 30: "Known Face", 60: "Popular", 100: "School Star"},
    "teachers": {0: "Unknown", 30: "Recognized", 60: "Favorite", 100: "Star Student"},
}


def slow_print(text, delay=None, color=Fore.WHITE, style=None, highlight=None):
    """
    Print text with a typing effect and customizable colors using colorama

    Arguments:
    text -- the text to print
    delay -- the delay between characters (overrides text_speed setting)
    color -- text color (from colorama.Fore)
    style -- text style (from colorama.Style)
    highlight -- background color (from colorama.Back)
    """
    # Apply text speed setting
    if delay is None:
        if game_settings["text_speed"] == "slow":
            delay = 0.04
        elif game_settings["text_speed"] == "normal":
            delay = 0.02
        else:  # fast
            delay = 0.005

    # Apply content filtering
    filtered_text = text
    if (
        "shit" in text.lower()
        or "fuck" in text.lower()
        or "ass" in text.lower()
        or "bitch" in text.lower()
    ):
        filtered_text = filter_text(text, ["cuss_words"])

    # Construct the style prefix - careful not to insert style codes within the text
    style_prefix = ""
    if highlight:
        style_prefix += highlight
    if style:
        style_prefix += style
    style_prefix += color
    
    # Print with delay (with style before and reset after)
    if delay > 0.01 and not os.environ.get("REPLIT_ENVIRONMENT", False):  
        # Character-by-character for slower speeds, but only outside Replit
        print(style_prefix, end="", flush=True)
        for char in filtered_text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)
    else:
        # Fast print - use this always in Replit for better color support
        print(f"{style_prefix}{filtered_text}{Style.RESET_ALL}")
        # Brief delay to simulate the typing effect
        if delay > 0:
            time.sleep(min(len(filtered_text) * delay * 0.2, 0.5))


def update_ranks():
    for category in ["students", "teachers"]:
        points = player["reputation"][category]
        current_rank = "Nobody" if category == "students" else "Unknown"
        for threshold, rank in sorted(ranks[category].items()):
            if points >= threshold:
                current_rank = rank
        player["rank"][category] = current_rank


def is_weekend():
    return current_date.weekday() >= 5


def check_weekend_activities():
    """Check for special weekend activities"""
    if not is_weekend():
        return

    # Weekend activities based on location
    current_location = player["current_location"]

    # Special locations available only on weekends
    weekend_locations = [
        "Movie Theater",
        "Shopping Mall",
        "City Park",
        "Beach",
        "Amusement Park",
        "Restaurant District",
        "Karaoke Bar",
        "Arcade Center",
    ]

    # Add weekend locations temporarily
    if current_date.weekday() == 5:  # Saturday
        slow_print(
            f"{Fore.YELLOW}It's Saturday! Special weekend locations are available.{Style.RESET_ALL}"
        )
    elif current_date.weekday() == 6:  # Sunday
        slow_print(
            f"{Fore.YELLOW}It's Sunday! Last chance for weekend activities.{Style.RESET_ALL}"
        )

    # Random weekend events
    if current_location in weekend_locations:
        handle_weekend_location(current_location)
    elif current_location == "Dorm Room" or current_location == "Bedroom":
        weekend_rest_options()
    elif current_location == "Library":
        weekend_study_session()


def handle_weekend_location(location):
    """Handle special weekend locations"""
    global ticks
    if location == "Movie Theater":
        slow_print(f"\n{Fore.CYAN}=== Movie Theater ==={Style.RESET_ALL}")

        movies = [
            {"title": "Action Blockbuster", "price": 1500, "stress": -20, "fun": 25},
            {"title": "Romantic Comedy", "price": 1200, "stress": -25, "fun": 20},
            {"title": "Sci-Fi Epic", "price": 1800, "stress": -15, "fun": 30},
            {"title": "Horror Thriller", "price": 1300, "stress": -10, "fun": 25},
            {"title": "Animated Family Film", "price": 1100, "stress": -30, "fun": 20},
        ]

        slow_print("Current movies showing:")
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} - ¥{movie['price']}")

        print(f"{len(movies) + 1}. Never mind")

        choice = input(f"Which movie would you like to see? (1-{len(movies) + 1}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(movies):
                selected_movie = movies[choice_num - 1]

                # Check if player has enough money
                if player["money"] < selected_movie["price"]:
                    slow_print(
                        f"You don't have enough money for that. You need ¥{selected_movie['price']}."
                    )
                    return

                # Watch movie
                player["money"] -= selected_movie["price"]
                player["stress"] = max(
                    0, player["stress"] + selected_movie["stress"]
                )  # Reduce stress

                slow_print(
                    f"You watch {selected_movie['title']} and enjoy the experience."
                )
                slow_print(f"Stress {selected_movie['stress']}")
                slow_print(
                    f"You spent ¥{selected_movie['price']}. Remaining money: ¥{player['money']}"
                )

                # Random chance for date opportunity if player has a romantic interest
                if (
                    player.get("romantic_interest")
                    and player["romance_stage"] >= 3
                    and random.random() < 0.4
                ):
                    romantic_date_event()

                # Advance time significantly
                global ticks
                ticks += 15  # Movie takes about 1.5 hours
            else:
                slow_print("You decide not to watch a movie.")
        except ValueError:
            slow_print("Invalid choice.")

    elif location == "Shopping Mall":
        slow_print(f"\n{Fore.CYAN}=== Shopping Mall ==={Style.RESET_ALL}")

        activities = [
            "Browse clothing stores",
            "Check out the bookstore",
            "Visit the electronics shop",
            "Get something from the food court",
            "Just window shop",
        ]

        for i, activity in enumerate(activities, 1):
            print(f"{i}. {activity}")

        choice = input(f"What would you like to do? (1-{len(activities)}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(activities):
                selected_activity = activities[choice_num - 1]

                if choice_num == 1:  # Clothing stores
                    clothes_shopping()
                elif choice_num == 2:  # Bookstore
                    bookstore_shopping()
                elif choice_num == 3:  # Electronics
                    electronics_shopping()
                elif choice_num == 4:  # Food court
                    food_court_meal()
                else:  # Window shopping
                    slow_print(
                        "You spend some time window shopping and enjoying the atmosphere."
                    )
                    player["stress"] = max(0, player["stress"] - 10)
                    slow_print("Stress -10")
                    ticks += 5  # 30 minutes

                # Random friend encounter
                if random.random() < 0.3:  # 30% chance
                    random_friend_encounter()
            else:
                slow_print("You decide to leave the mall.")
        except ValueError:
            slow_print("Invalid choice.")

    elif location == "City Park":
        slow_print(f"\n{Fore.CYAN}=== City Park ==={Style.RESET_ALL}")

        activities = [
            "Go for a jog",
            "Have a picnic",
            "Read a book under a tree",
            "Feed the ducks at the pond",
            "Play frisbee",
        ]

        for i, activity in enumerate(activities, 1):
            print(f"{i}. {activity}")

        choice = input(f"What would you like to do? (1-{len(activities)}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(activities):
                selected_activity = activities[choice_num - 1]
                slow_print(f"You chose to do {selected_activity}.")

                # Each activity has unique effects
                if choice_num == 1:  # Jogging
                    slow_print("You go for a refreshing jog around the park.")
                    player["health"] = min(100, player["health"] + 10)
                    player["energy"] = max(30, player["energy"] - 20)
                    player["stress"] = max(0, player["stress"] - 15)
                    slow_print("Health +10, Energy -20, Stress -15")

                elif choice_num == 2:  # Picnic
                    if player["money"] < 800:
                        slow_print(
                            "You don't have enough money for picnic supplies (¥800)."
                        )
                        return

                    player["money"] -= 800
                    player["hunger"] = min(100, player["hunger"] + 60)
                    player["stress"] = max(0, player["stress"] - 25)
                    slow_print("You enjoy a peaceful picnic in the park.")
                    slow_print("Hunger +60, Stress -25")
                    slow_print(
                        f"You spent ¥800 on supplies. Remaining money: ¥{player['money']}"
                    )

                elif choice_num == 3:  # Reading
                    slow_print(
                        "You find a quiet spot under a tree and read for a while."
                    )
                    player["intelligence"] = min(100, player["intelligence"] + 5)
                    player["stress"] = max(0, player["stress"] - 20)
                    slow_print("Intelligence +5, Stress -20")

                elif choice_num == 4:  # Feeding ducks
                    if player["money"] < 300:
                        slow_print("You don't have enough money for duck feed (¥300).")
                        return

                    player["money"] -= 300
                    player["stress"] = max(0, player["stress"] - 30)
                    slow_print(
                        "You spend a relaxing time feeding the ducks at the pond."
                    )
                    slow_print("Stress -30")
                    slow_print(
                        f"You spent ¥300 on duck feed. Remaining money: ¥{player['money']}"
                    )

                else:  # Frisbee
                    slow_print("You play frisbee in the open field.")
                    player["energy"] = max(20, player["energy"] - 15)
                    player["stress"] = max(0, player["stress"] - 25)
                    slow_print("Energy -15, Stress -25")

                    # Chance to meet new people
                    if random.random() < 0.4:  # 40% chance
                        random_friend_encounter()

                # Advance time
                ticks += 8  # About 45-50 minutes
            else:
                slow_print("You decide to leave the park.")
        except ValueError:
            slow_print("Invalid choice.")

    elif location == "Beach":
        slow_print(f"\n{Fore.CYAN}=== Beach ==={Style.RESET_ALL}")

        activities = [
            "Swim in the ocean",
            "Sunbathe on the sand",
            "Build a sandcastle",
            "Play beach volleyball",
            "Collect seashells",
        ]

        for i, activity in enumerate(activities, 1):
            print(f"{i}. {activity}")

        choice = input(f"What would you like to do? (1-{len(activities)}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(activities):
                # Beach activities
                if choice_num == 1:  # Swimming
                    slow_print("You go for a refreshing swim in the ocean.")
                    player["health"] = min(100, player["health"] + 15)
                    player["energy"] = max(30, player["energy"] - 25)
                    player["stress"] = max(0, player["stress"] - 20)
                    slow_print("Health +15, Energy -25, Stress -20")

                elif choice_num == 2:  # Sunbathing
                    slow_print("You relax on the sand, soaking up the sun.")
                    player["energy"] = min(100, player["energy"] + 10)
                    player["stress"] = max(0, player["stress"] - 30)
                    slow_print("Energy +10, Stress -30")

                elif choice_num == 3:  # Sandcastle
                    slow_print("You build an impressive sandcastle.")
                    player["creativity"] = min(100, player["creativity"] + 10)
                    player["stress"] = max(0, player["stress"] - 15)
                    slow_print("Creativity +10, Stress -15")

                elif choice_num == 4:  # Volleyball
                    slow_print("You join a beach volleyball game.")
                    player["charm"] = min(100, player["charm"] + 5)
                    player["energy"] = max(20, player["energy"] - 30)
                    player["stress"] = max(0, player["stress"] - 25)
                    slow_print("Charm +5, Energy -30, Stress -25")

                    # Chance to meet new people
                    if random.random() < 0.6:  # 60% chance
                        random_friend_encounter()

                else:  # Seashell collecting
                    slow_print("You spend time collecting beautiful seashells.")
                    player["stress"] = max(0, player["stress"] - 20)

                    # Random chance to find something valuable
                    if random.random() < 0.2:  # 20% chance
                        found_money = random.randint(500, 2000)
                        player["money"] += found_money
                        slow_print(
                            f"You found a rare shell that a collector buys from you for ¥{found_money}!"
                        )
                        slow_print(f"Money +{found_money}")

                    slow_print("Stress -20")

                # Advance time
                ticks += 12  # About 1-1.5 hours
            else:
                slow_print("You decide to leave the beach.")
        except ValueError:
            slow_print("Invalid choice.")

    elif location == "Restaurant District":
        slow_print(f"\n{Fore.CYAN}=== Restaurant District ==={Style.RESET_ALL}")

        restaurants = [
            {
                "name": "Sushi Bar",
                "price": 1800,
                "hunger": 70,
                "stress": -15,
                "charm": 3,
                "description": "A traditional Japanese sushi restaurant with fresh fish and authentic atmosphere.",
            },
            {
                "name": "Italian Bistro",
                "price": 2200,
                "hunger": 80,
                "stress": -20,
                "charm": 5,
                "description": "A cozy Italian restaurant with homemade pasta and wood-fired pizzas.",
            },
            {
                "name": "Campus Diner",
                "price": 1200,
                "hunger": 75,
                "stress": -10,
                "energy": 10,
                "description": "A popular student hangout with affordable comfort food.",
            },
            {
                "name": "Fine Dining",
                "price": 3500,
                "hunger": 65,
                "stress": -25,
                "charm": 8,
                "reputation": 5,
                "description": "An upscale restaurant perfect for special occasions or impressing someone.",
            },
            {
                "name": "Ramen Shop",
                "price": 900,
                "hunger": 85,
                "stress": -15,
                "energy": 15,
                "description": "A small but authentic ramen shop with steaming bowls of noodles.",
            },
            {
                "name": "Okonomiyaki House",
                "price": 1100,
                "hunger": 80,
                "stress": -18,
                "energy": 12,
                "description": "A restaurant specializing in savory Japanese pancakes cooked on a hot plate.",
            },
            {
                "name": "Korean BBQ",
                "price": 2500,
                "hunger": 90,
                "stress": -20,
                "energy": 10,
                "description": "A place where you grill your own meat at the table in Korean style.",
            },
            {
                "name": "Curry House",
                "price": 1300,
                "hunger": 85,
                "stress": -15,
                "energy": 18,
                "description": "A restaurant serving Japanese-style curry dishes that are popular with students.",
            },
            {
                "name": "Healthy Cafe",
                "price": 1600,
                "hunger": 60,
                "stress": -25,
                "health": 10,
                "description": "A modern cafe focusing on nutritious, healthy meals and smoothies.",
            },
            {
                "name": "Dessert Parlor",
                "price": 800,
                "hunger": 40,
                "stress": -30,
                "happiness": 15,
                "description": "A sweet shop specializing in various desserts and crepes.",
            },
        ]

        # Choose display style based on settings
        if game_settings["text_speed"] == "fast":
            # Quick list for fast text speed
            slow_print("The Restaurant District features several dining options:")
            for i, restaurant in enumerate(restaurants, 1):
                print(f"{i}. {restaurant['name']} - ¥{restaurant['price']}")
        else:
            # Detailed descriptions for normal/slow text speed
            slow_print(
                "You walk down the vibrant Restaurant District, with various eateries lining the street:"
            )
            for i, restaurant in enumerate(restaurants, 1):
                print(f"{i}. {restaurant['name']} - ¥{restaurant['price']}")
                print(f"   {restaurant['description']}")

        print(f"{len(restaurants) + 1}. Just window shop and leave")

        # Special event if it's dinner time or weekend
        current_hour = (ticks // 10) % 24
        dinner_start, dinner_end = 18, 22  # 6pm-10pm

        if (
            dinner_start <= current_hour <= dinner_end or is_weekend()
        ) and random.random() < 0.3:
            student = random.choice(students)
            if (
                relationship.get(student["name"], 0) >= 30
            ):  # Only for students you know somewhat
                slow_print(
                    f"\n{Fore.CYAN}You spot {student['name']} looking for a place to eat too!{Style.RESET_ALL}"
                )
                invite = input(
                    "Would you like to invite them to join you for dinner? (y/n): "
                ).lower()

                if invite == "y":
                    player["dining_companion"] = student["name"]
                    slow_print(f"{student['name']} agrees to join you!")
                    # They'll pay for their own meal but relationship will improve

        choice = input(f"Where would you like to eat? (1-{len(restaurants) + 1}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(restaurants):
                restaurant = restaurants[choice_num - 1]

                # Display restaurant description
                slow_print(f"\n{restaurant['description']}")

                # Ask if eating alone or inviting someone
                print("\nHow would you like to dine?")
                print("1. Dine alone")
                print("2. Invite a friend")
                print("3. Make it a date (if you have a romantic interest)")

                dining_choice = input("Choose an option (1-3): ")

                # Check if player has enough money
                if player["money"] < restaurant["price"]:
                    slow_print(
                        f"You realize this place is too expensive for your budget. You need ¥{restaurant['price']}."
                    )
                    return

                # Apply base effects
                player["money"] -= restaurant["price"]
                player["hunger"] = min(100, player["hunger"] + restaurant["hunger"])
                player["stress"] = max(
                    0, player["stress"] + restaurant.get("stress", 0)
                )
                if "energy" in restaurant:
                    player["energy"] = min(100, player["energy"] + restaurant["energy"])
                if "charm" in restaurant:
                    player["charm"] = min(100, player["charm"] + restaurant["charm"])
                if "reputation" in restaurant:
                    player["reputation"]["social"] = min(
                        100, player["reputation"]["social"] + restaurant["reputation"]
                    )

                if dining_choice == "1":  # Alone
                    slow_print(
                        f"You enjoy a nice meal by yourself at {restaurant['name']}."
                    )
                    slow_print("The food is delicious and gives you time to reflect.")
                    slow_print(
                        f"Hunger +{restaurant['hunger']}, Stress {restaurant['stress']}"
                    )
                    slow_print(
                        f"You spent ¥{restaurant['price']}. Remaining money: ¥{player['money'] - restaurant['price']}"
                    )

                    # Small chance of random encounter
                    if random.random() < 0.2:
                        random_friend_encounter()

                elif dining_choice == "2":  # With friend
                    # Select friend to invite
                    friends = [
                        name
                        for name, level in player["relationships"].items()
                        if level >= 30
                    ]
                    if not friends:
                        slow_print(
                            "You realize you don't have any close enough friends to invite to dinner."
                        )
                        slow_print("You decide to eat alone instead.")
                        slow_print(
                            f"Hunger +{restaurant['hunger']}, Stress {restaurant['stress']}"
                        )
                    else:
                        print("\nWho would you like to invite?")
                        for i, friend in enumerate(friends, 1):
                            print(f"{i}. {friend}")

                        friend_choice = input(f"Choose a friend (1-{len(friends)}): ")
                        try:
                            friend_idx = int(friend_choice) - 1
                            if 0 <= friend_idx < len(friends):
                                friend_name = friends[friend_idx]

                                # Extra cost for friend's meal
                                additional_cost = restaurant["price"]
                                if player["money"] < additional_cost:
                                    slow_print(
                                        f"You realize you can't afford to pay for your friend as well (¥{additional_cost})."
                                    )
                                    slow_print(
                                        "You text them to cancel and eat alone instead."
                                    )
                                else:
                                    player["money"] -= additional_cost

                                    # Friend dialogue
                                    slow_print(
                                        f"You invite {friend_name} to join you for dinner at {restaurant['name']}."
                                    )
                                    slow_print(
                                        "You have a wonderful time catching up and enjoying the food together."
                                    )

                                    # Improve relationship
                                    relationship_boost = random.randint(5, 15)
                                    player["relationships"][friend_name] = min(
                                        100,
                                        player["relationships"][friend_name]
                                        + relationship_boost,
                                    )

                                    slow_print(
                                        f"Your friendship with {friend_name} has grown stronger!"
                                    )
                                    slow_print(
                                        f"Hunger +{restaurant['hunger']}, Stress {restaurant['stress'] - 5}"
                                    )  # Extra stress reduction
                                    slow_print(
                                        f"You spent ¥{restaurant['price'] * 2} total. Remaining money: ¥{player['money']}"
                                    )

                                    # Friend might introduce you to someone new
                                    if random.random() < 0.3:
                                        slow_print(
                                            f"\n{friend_name} introduces you to one of their friends who happens to be at the restaurant."
                                        )
                                        random_friend_encounter()
                        except (ValueError, IndexError):
                            slow_print("You decide not to invite anyone after all.")

                elif dining_choice == "3" and player.get("romantic_interest"):  # Date
                    interest_name = player["romantic_interest"]

                    # Extra cost for date's meal
                    date_cost = restaurant["price"]
                    if player["money"] < date_cost:
                        slow_print(
                            f"You realize you can't afford to pay for a date (¥{date_cost})."
                        )
                        slow_print("You decide to eat alone instead.")
                    else:
                        player["money"] -= date_cost

                        slow_print(
                            f"You invite {interest_name} for a dinner date at {restaurant['name']}."
                        )

                        # Different date experience based on restaurant and romance stage
                        stage = player["romance_stage"]

                        if restaurant["name"] == "Fine Dining":
                            # Fancy restaurant bonus
                            romance_boost = random.randint(10, 20)
                            slow_print(
                                "The elegant atmosphere and exquisite food create a perfect romantic setting."
                            )
                            slow_print(
                                f"{interest_name} seems very impressed by your choice of restaurant."
                            )
                        else:
                            romance_boost = random.randint(5, 15)
                            slow_print(
                                "You enjoy a lovely meal together, talking and laughing as you eat."
                            )

                        # Advance romance stage potentially
                        if stage < 5 and random.random() < 0.4:
                            player["romance_stage"] += 1
                            slow_print(
                                f"Your relationship with {interest_name} has advanced to the next level!"
                            )

                        slow_print(
                            f"Hunger +{restaurant['hunger']}, Stress {restaurant['stress'] - 10}"
                        )  # Extra stress reduction
                        slow_print(
                            f"You spent ¥{restaurant['price'] * 2} total. Remaining money: ¥{player['money']}"
                        )
                else:
                    slow_print("You decide to eat alone.")
                    slow_print(
                        f"Hunger +{restaurant['hunger']}, Stress {restaurant['stress']}"
                    )
                    slow_print(
                        f"You spent ¥{restaurant['price']}. Remaining money: ¥{player['money']}"
                    )

                # Advance time
                ticks += 12  # About 1-1.5 hours
            else:
                slow_print(
                    "You decide to just walk around the Restaurant District without eating."
                )
        except ValueError:
            slow_print(
                "You wander around the Restaurant District, enjoying the sights and smells."
            )

    elif location == "Karaoke Bar":
        slow_print(f"\n{Fore.CYAN}=== Karaoke Bar ==={Style.RESET_ALL}")

        # Cost options
        options = [
            {"name": "One hour session", "price": 1500, "time": 6},  # 30-40 minutes
            {"name": "Two hour session", "price": 2500, "time": 12},  # ~1 hour
            {"name": "All-night session", "price": 4000, "time": 20},  # ~2 hours
        ]

        slow_print("The karaoke bar offers private rooms with all the latest songs.")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option['name']} - ¥{option['price']}")

        print(f"{len(options) + 1}. Just look around and leave")

        choice = input(f"What would you like to do? (1-{len(options) + 1}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                option = options[choice_num - 1]

                # Check if player has enough money
                if player["money"] < option["price"]:
                    slow_print(
                        f"You don't have enough money for that. You need ¥{option['price']}."
                    )
                    return

                # Ask about group
                print("\nWho will you be singing with?")
                print("1. Go solo (practice your singing)")
                print("2. Invite friends")
                print("3. Make it a date (if you have a romantic interest)")

                group_choice = input("Choose an option (1-3): ")

                # Apply base effects
                player["money"] -= option["price"]
                stress_reduction = min(
                    25, option["time"] * 2
                )  # More time = more stress reduction
                player["stress"] = max(0, player["stress"] - stress_reduction)

                if group_choice == "1":  # Solo
                    slow_print("You decide to practice your singing skills in private.")
                    player["creativity"] = min(
                        100, player["creativity"] + random.randint(5, 10)
                    )
                    slow_print(
                        f"You belt out your favorite songs for {option['name'].lower()}."
                    )
                    slow_print(f"Creativity +5-10, Stress -{stress_reduction}")
                    slow_print(
                        f"You spent ¥{option['price']}. Remaining money: ¥{player['money']}"
                    )

                elif group_choice == "2":  # With friends
                    # Select friends to invite
                    friends = [
                        name
                        for name, level in player["relationships"].items()
                        if level >= 20
                    ]
                    if not friends:
                        slow_print(
                            "You realize you don't have any friends to invite to karaoke."
                        )
                        slow_print("You decide to sing alone instead.")
                    else:
                        # Choose how many friends to invite (1-3)
                        max_friends = min(3, len(friends))
                        print(
                            f"\nHow many friends do you want to invite? (1-{max_friends})"
                        )
                        num_choice = input(f"Enter a number (1-{max_friends}): ")

                        try:
                            num_friends = min(max_friends, max(1, int(num_choice)))

                            # Select which friends
                            invited_friends = []
                            for i in range(num_friends):
                                print(f"\nSelect friend #{i+1}:")
                                for j, friend in enumerate(friends, 1):
                                    if friend not in invited_friends:
                                        print(f"{j}. {friend}")

                                choice = input("Choose a friend: ")
                                try:
                                    idx = int(choice) - 1
                                    if (
                                        0 <= idx < len(friends)
                                        and friends[idx] not in invited_friends
                                    ):
                                        invited_friends.append(friends[idx])
                                except (ValueError, IndexError):
                                    pass

                            if invited_friends:
                                # Group karaoke session
                                slow_print(
                                    f"You and {', '.join(invited_friends)} have an amazing time singing together!"
                                )

                                # Additional cost for drinks/snacks
                                additional_cost = 500 * len(invited_friends)
                                if player["money"] < additional_cost:
                                    slow_print(
                                        f"You don't have enough money for drinks and snacks (¥{additional_cost})."
                                    )
                                    slow_print(
                                        "Your friends chip in to cover the difference."
                                    )
                                else:
                                    player["money"] -= additional_cost
                                    slow_print(
                                        f"You treat everyone to drinks and snacks for ¥{additional_cost}."
                                    )

                                # Improve relationships
                                for friend in invited_friends:
                                    relationship_boost = random.randint(5, 15)
                                    player["relationships"][friend] = min(
                                        100,
                                        player["relationships"].get(friend, 0)
                                        + relationship_boost,
                                    )

                                # Extra stress reduction for social fun
                                extra_stress = min(20, 5 * len(invited_friends))
                                player["stress"] = max(
                                    0, player["stress"] - extra_stress
                                )

                                # Charm increase from social activity
                                player["charm"] = min(
                                    100, player["charm"] + random.randint(3, 8)
                                )

                                slow_print(
                                    f"Stress -{stress_reduction + extra_stress}, Charm +3-8"
                                )
                                total_cost = option["price"] + additional_cost
                                slow_print(
                                    f"You spent ¥{total_cost} total. Remaining money: ¥{player['money']}"
                                )
                            else:
                                slow_print(
                                    "You couldn't decide who to invite and end up singing alone."
                                )
                        except ValueError:
                            slow_print("You decide to sing alone after all.")

                elif group_choice == "3" and player.get("romantic_interest"):  # Date
                    interest_name = player["romantic_interest"]

                    # Additional cost for date
                    date_cost = 1500  # Cost for drinks/snacks
                    if player["money"] < date_cost:
                        slow_print(
                            f"You don't have enough money for a proper date (¥{date_cost})."
                        )
                        slow_print("You decide to sing alone instead.")
                    else:
                        player["money"] -= date_cost

                        slow_print(f"You invite {interest_name} for a karaoke date.")
                        slow_print(
                            "You take turns singing your favorite songs, sometimes doing duets together."
                        )

                        # Romance boost
                        romance_boost = random.randint(8, 15)

                        # Special romantic moment
                        if random.random() < 0.5:
                            slow_print(
                                f"During a slow song, {interest_name} sits very close to you and your eyes meet..."
                            )

                            # Chance to advance romance stage
                            if player["romance_stage"] < 5 and random.random() < 0.4:
                                player["romance_stage"] += 1
                                slow_print(
                                    f"Your relationship with {interest_name} has advanced to the next level!"
                                )

                        # Extra bonuses for date
                        player["charm"] = min(
                            100, player["charm"] + random.randint(5, 10)
                        )

                        slow_print(f"Stress -{stress_reduction + 15}, Charm +5-10")
                        total_cost = option["price"] + date_cost
                        slow_print(
                            f"You spent ¥{total_cost} total. Remaining money: ¥{player['money']}"
                        )
                else:
                    slow_print("You decide to enjoy some solo karaoke time.")

                # Advance time based on session length
                ticks += option["time"]
            else:
                slow_print("You decide to not sing karaoke today.")
        except ValueError:
            slow_print("You decide to leave the karaoke bar without singing.")

    elif location == "Arcade Center":
        slow_print(f"\n{Fore.CYAN}=== Arcade Center ==={Style.RESET_ALL}")

        # Different games with different prices and effects
        arcade_games = [
            {
                "name": "Dancing Stage",
                "price": 300,
                "rounds": 1,
                "energy": -10,
                "stress": -12,
                "social": 2,
                "skill": "rhythm",
                "description": "A dance game with arrows to step on in time with music.",
            },
            {
                "name": "Racing Simulator",
                "price": 500,
                "rounds": 1,
                "energy": -8,
                "stress": -10,
                "skill": "reflexes",
                "description": "A realistic racing game with full motion controls.",
            },
            {
                "name": "Fighting Arena",
                "price": 400,
                "rounds": 1,
                "energy": -12,
                "stress": -15,
                "skill": "technique",
                "description": "A competitive fighting game requiring skill and timing.",
            },
            {
                "name": "Rhythm Game",
                "price": 300,
                "rounds": 1,
                "energy": -8,
                "stress": -15,
                "skill": "rhythm",
                "description": "Tap buttons in time with falling notes and music.",
            },
            {
                "name": "Crane Game",
                "price": 200,
                "rounds": 1,
                "luck": True,
                "stress": -5,
                "description": "Try to grab a prize with the mechanical claw.",
            },
            {
                "name": "Photo Booth",
                "price": 600,
                "rounds": 1,
                "social": 5,
                "stress": -10,
                "description": "Take fun decorated photos with friends.",
            },
            {
                "name": "Virtual Reality",
                "price": 1000,
                "rounds": 3,
                "energy": -20,
                "stress": -25,
                "description": "An immersive VR experience with various game options.",
            },
            {
                "name": "Ticket Games",
                "price": 1500,
                "rounds": 5,
                "energy": -15,
                "stress": -20,
                "tickets": True,
                "description": "Various games that award tickets for prizes.",
            },
        ]

        slow_print(
            "Welcome to the Arcade Center! With flashing lights and exciting sounds, this is a great place to have fun."
        )

        if game_settings["text_speed"] != "fast":
            slow_print(
                "Students gather here to play games, compete, and hang out with friends."
            )
            slow_print("You notice various types of arcade machines and attractions.")

        print("\nGames Available:")
        for i, game in enumerate(arcade_games, 1):
            print(f"{i}. {game['name']} - ¥{game['price']} per play")
            if game_settings["text_speed"] != "fast":
                print(f"   {game['description']}")

        print(f"{len(arcade_games) + 1}. Just watch others play")
        print(f"{len(arcade_games) + 2}. Leave")

        # Social component - random friend encounter
        if random.random() < 0.4:
            friend_options = []
            for name, level in relationship.items():
                if level >= 20:  # Acquaintance or better
                    friend_options.append(name)

            if friend_options:
                friend = random.choice(friend_options)
                slow_print(
                    f"\n{Fore.CYAN}You spot {friend} playing at one of the arcade machines!{Style.RESET_ALL}"
                )
                interact = input(f"Would you like to join {friend}? (y/n): ").lower()

                if interact == "y":
                    # Determine which game they're playing
                    friend_game = random.choice(arcade_games)
                    slow_print(f"{friend} is playing {friend_game['name']}!")
                    slow_print("You offer to play together for the next round.")

                    # Check if player can afford it
                    if player["money"] < friend_game["price"]:
                        slow_print(
                            f"Unfortunately, you don't have enough money. You need ¥{friend_game['price']}."
                        )
                        slow_print(f"You watch {friend} play instead.")
                    else:
                        player["money"] -= friend_game["price"]

                        # Play together
                        slow_print(
                            f"You and {friend} have a great time playing {friend_game['name']} together!"
                        )

                        # Game effects
                        if "energy" in friend_game:
                            player["energy"] = max(
                                0, player["energy"] + friend_game["energy"]
                            )
                        if "stress" in friend_game:
                            player["stress"] = max(
                                0, player["stress"] + friend_game["stress"] - 5
                            )  # Extra stress reduction with friend

                        # Relationship boost
                        relationship_boost = random.randint(3, 8)
                        relationship[friend] = min(
                            100, relationship[friend] + relationship_boost
                        )

                        slow_print(f"Your friendship with {friend} has grown stronger!")
                        slow_print(
                            f"You spent ¥{friend_game['price']}. Remaining money: ¥{player['money']}"
                        )

                        # Special wins/moments
                        if random.random() < 0.3:
                            special_moments = [
                                f"You beat {friend}'s high score!",
                                f"You and {friend} achieve a new co-op record!",
                                f"You win a small prize and give it to {friend}.",
                                f"{friend} teaches you a special technique for the game.",
                            ]
                            slow_print(random.choice(special_moments))
                            relationship[friend] = min(
                                100, relationship[friend] + 5
                            )  # Extra boost

                        # Advance time
                        ticks += 3  # About 20 minutes

        choice = input(f"\nWhat would you like to do? (1-{len(arcade_games) + 2}): ")

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(arcade_games):
                selected_game = arcade_games[choice_num - 1]

                # Check money
                total_cost = selected_game["price"] * selected_game["rounds"]
                if player["money"] < total_cost:
                    slow_print(f"You don't have enough money. You need ¥{total_cost}.")
                    return

                player["money"] -= total_cost

                # Play alone or with someone?
                if (
                    selected_game["name"] != "Crane Game"
                    and selected_game["name"] != "Photo Booth"
                ):
                    print("\nHow would you like to play?")
                    print("1. Play alone")
                    print("2. Invite a friend to play")
                    print("3. Challenge a stranger")

                    play_style = input("Choose an option (1-3): ")

                    # Initialize invited_friend to avoid "possibly unbound" errors
                    invited_friend = None

                    if play_style == "2":  # With friend
                        friends = [
                            name for name, level in relationship.items() if level >= 30
                        ]
                        if not friends:
                            slow_print(
                                "You realize you don't have any close enough friends to invite."
                            )
                            slow_print("You decide to play alone instead.")
                            play_style = "1"
                        else:
                            print("\nWho would you like to invite?")
                            for i, friend in enumerate(friends, 1):
                                print(f"{i}. {friend}")

                            friend_choice = input(
                                f"Choose a friend (1-{len(friends)}): "
                            )
                            try:
                                friend_idx = int(friend_choice) - 1
                                if 0 <= friend_idx < len(friends):
                                    play_style = "2.1"  # With specific friend
                                    invited_friend = friends[friend_idx]
                                else:
                                    play_style = "1"  # Fallback to alone
                            except ValueError:
                                play_style = "1"  # Fallback to alone

                    # Play game with selected style
                    if play_style == "1":  # Alone
                        slow_print(f"You play {selected_game['name']} by yourself.")

                        # Basic game effects
                        if "energy" in selected_game:
                            player["energy"] = max(
                                0, player["energy"] + selected_game["energy"]
                            )
                        if "stress" in selected_game:
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"]
                            )

                        # Skill-based outcome
                        if "skill" in selected_game:
                            skill_roll = random.random()
                            if skill_roll < 0.7:  # 70% chance of normal success
                                slow_print("You do pretty well and have fun playing.")
                            elif skill_roll < 0.95:  # 25% chance of great success
                                slow_print(
                                    "You're on fire! You set a new personal record!"
                                )
                                player["stress"] = max(
                                    0, player["stress"] - 5
                                )  # Extra stress reduction
                            else:  # 5% chance of amazing success
                                slow_print(
                                    "INCREDIBLE! You achieved the highest score ever seen on this machine!"
                                )
                                player["stress"] = max(
                                    0, player["stress"] - 10
                                )  # Major stress reduction

                                # Other players gather around
                                slow_print(
                                    "Other arcade-goers gather around to watch your amazing performance!"
                                )
                                if "social" in selected_game:
                                    player["charisma"]["social"] = min(
                                        100,
                                        player["charisma"]["social"]
                                        + selected_game["social"] * 2,
                                    )

                        # Ticket prizes
                        if "tickets" in selected_game:
                            tickets = random.randint(20, 100)
                            slow_print(f"You win {tickets} tickets!")

                            print("\nWhat would you like to exchange your tickets for?")
                            print("1. Small toy (50 tickets)")
                            print("2. Candy (30 tickets)")
                            print("3. Keychain (80 tickets)")
                            print("4. Save tickets for later")

                            prize_choice = input("Choose an option (1-4): ")
                            if prize_choice == "1" and tickets >= 50:
                                slow_print(
                                    "You exchange your tickets for a cute small toy!"
                                )
                                player["items"].append("Arcade Toy")
                            elif prize_choice == "2" and tickets >= 30:
                                slow_print("You exchange your tickets for some candy!")
                                player["hunger"] = min(100, player["hunger"] + 10)
                                player["energy"] = min(100, player["energy"] + 5)
                            elif prize_choice == "3" and tickets >= 80:
                                slow_print(
                                    "You exchange your tickets for a cool keychain!"
                                )
                                player["items"].append("Arcade Keychain")
                            else:
                                slow_print(
                                    "You decide to save your tickets for another time."
                                )

                    elif play_style == "2.1" and invited_friend:  # With specific friend
                        slow_print(
                            f"You invite {invited_friend} to play {selected_game['name']} with you."
                        )
                        slow_print("You both have a great time playing together!")

                        # Game effects with friend bonus
                        if "energy" in selected_game:
                            player["energy"] = max(
                                0, player["energy"] + selected_game["energy"]
                            )
                        if "stress" in selected_game:
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"] - 5
                            )  # Extra stress reduction with friend

                        # Relationship boost
                        if invited_friend in relationship:
                            relationship_boost = random.randint(5, 10)
                            relationship[invited_friend] = min(
                                100, relationship[invited_friend] + relationship_boost
                            )
                            slow_print(
                                f"Your friendship with {invited_friend} has grown stronger!"
                            )
                        else:
                            # Add friend to relationships if not already there
                            relationship_boost = random.randint(5, 10)
                            relationship[invited_friend] = relationship_boost
                            slow_print(
                                f"You've started a new friendship with {invited_friend}!"
                            )

                    elif play_style == "3":  # Challenge stranger
                        slow_print(
                            f"You look around for someone to challenge at {selected_game['name']}."
                        )

                        # Meet a new potential friend or rival
                        stranger_names = [
                            "Yusuke",
                            "Keiko",
                            "Takeshi",
                            "Hana",
                            "Ryota",
                            "Sakura",
                        ]
                        stranger = random.choice(stranger_names)

                        if stranger not in relationship:
                            relationship[stranger] = 0

                        slow_print(f"You challenge {stranger} who's waiting to play.")

                        # Game outcome
                        outcome = random.random()
                        if outcome < 0.4:  # You win
                            slow_print(
                                f"You win against {stranger}! They seem impressed by your skills."
                            )
                            relationship[stranger] = min(
                                100, relationship[stranger] + random.randint(5, 15)
                            )
                            slow_print(
                                f"{stranger} asks for a rematch sometime. You've made a new friend!"
                            )
                        elif outcome < 0.8:  # Close match
                            slow_print(
                                f"It's a close match with {stranger}! You both had fun competing."
                            )
                            relationship[stranger] = min(
                                100, relationship[stranger] + random.randint(3, 8)
                            )
                            slow_print(
                                f"You and {stranger} exchange contact info to play again sometime."
                            )
                        else:  # You lose
                            slow_print(
                                f"You lose to {stranger}, who's clearly an expert at this game."
                            )
                            slow_print(
                                f"{stranger} gives you some tips on how to improve."
                            )
                            relationship[stranger] = min(
                                100, relationship[stranger] + random.randint(1, 5)
                            )

                        if "stress" in selected_game:
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"]
                            )
                        if "energy" in selected_game:
                            player["energy"] = max(
                                0, player["energy"] + selected_game["energy"] - 5
                            )  # Extra energy used in competition

                else:  # Special games with different mechanics
                    if selected_game["name"] == "Crane Game":
                        slow_print(
                            "You try your luck at the crane machine, aiming for a prize..."
                        )

                        # Crane game outcome based on luck
                        crane_luck = random.random()
                        if crane_luck < 0.15:  # 15% chance to win
                            prizes = [
                                "Cute Plushie",
                                "Character Keychain",
                                "Small Figurine",
                                "Lucky Charm",
                            ]
                            won_prize = random.choice(prizes)
                            slow_print(f"Success! You managed to grab a {won_prize}!")
                            player["items"].append(won_prize)
                            player["stress"] = max(
                                0, player["stress"] - 15
                            )  # Extra stress reduction from winning
                        elif crane_luck < 0.3:  # Almost wins
                            slow_print(
                                "So close! The prize slips out of the claw at the last moment."
                            )
                            slow_print(
                                "A staff member notices and gives you a small consolation prize."
                            )
                            player["items"].append("Consolation Prize")
                            player["stress"] = max(0, player["stress"] - 8)
                        else:
                            slow_print(
                                "The claw weakly grabs at the prize but can't pick it up."
                            )
                            slow_print("Maybe next time...")
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"]
                            )

                    elif selected_game["name"] == "Photo Booth":
                        print("\nWho would you like to take photos with?")
                        print("1. Take solo photos")
                        print("2. With friends")
                        print("3. With romantic interest (if you have one)")

                        photo_choice = input("Choose an option (1-3): ")

                        if photo_choice == "1":  # Solo
                            slow_print(
                                "You take some fun solo photos with different filters and backgrounds."
                            )
                            slow_print(
                                "The photos turn out great! You keep them as a memento."
                            )
                            player["items"].append("Photo Booth Pictures")
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"]
                            )

                        elif photo_choice == "2":  # With friends
                            friends = [
                                name
                                for name, level in relationship.items()
                                if level >= 30
                            ]
                            if not friends:
                                slow_print(
                                    "You realize you don't have any close enough friends to invite."
                                )
                                slow_print("You take solo photos instead.")
                                player["items"].append("Solo Photo Booth Pictures")
                            else:
                                # Let player select up to 3 friends
                                print(
                                    "\nSelect up to 3 friends to take photos with (enter numbers separated by spaces):"
                                )
                                for i, friend in enumerate(friends, 1):
                                    print(f"{i}. {friend}")

                                friend_choices = input("Choose friends (e.g., '1 3'): ")
                                photo_friends = []

                                try:
                                    indices = [
                                        int(idx) - 1 for idx in friend_choices.split()
                                    ]
                                    for idx in indices[:3]:
                                        if 0 <= idx < len(friends):
                                            photo_friends.append(friends[idx])
                                except ValueError:
                                    slow_print(
                                        "Invalid selection. You'll take solo photos."
                                    )

                                if photo_friends:
                                    friend_str = ", ".join(photo_friends)
                                    slow_print(
                                        f"You and {friend_str} squeeze into the photo booth together."
                                    )
                                    slow_print(
                                        "You all make silly poses and try different backgrounds."
                                    )
                                    slow_print(
                                        "The photos turn out hilarious and memorable!"
                                    )

                                    player["items"].append("Friend Group Photos")
                                    player["stress"] = max(
                                        0,
                                        player["stress"] + selected_game["stress"] - 5,
                                    )

                                    # Friendship boost
                                    for friend in photo_friends:
                                        relationship_boost = random.randint(3, 8)
                                        relationship[friend] = min(
                                            100,
                                            relationship[friend] + relationship_boost,
                                        )

                                    slow_print(
                                        "Your friendships have grown stronger through this shared memory!"
                                    )
                                else:
                                    slow_print("You take solo photos instead.")
                                    player["items"].append("Solo Photo Booth Pictures")

                        elif photo_choice == "3" and player.get(
                            "romantic_interest"
                        ):  # With date
                            interest_name = player["romantic_interest"]

                            slow_print(
                                f"You invite {interest_name} to take cute photos together."
                            )
                            slow_print(
                                "You both pose close together with various romantic backgrounds."
                            )

                            player["items"].append("Couple Photo Booth Pictures")
                            player["stress"] = max(
                                0, player["stress"] + selected_game["stress"] - 10
                            )

                            # Romance boost
                            romance_boost = random.randint(5, 15)
                            player["romance_points"] = min(
                                100, player["romance_points"] + romance_boost
                            )

                            slow_print(
                                f"The photo session brings you and {interest_name} closer together!"
                            )

                            # Special romantic moment
                            if random.random() < 0.3 and player["romance_stage"] >= 3:
                                slow_print(
                                    f"\n{Fore.MAGENTA}As you look at the photos, {interest_name} gives you a special look that makes your heart flutter.{Style.RESET_ALL}"
                                )
                                player["romance_points"] = min(
                                    100, player["romance_points"] + 5
                                )
                        else:
                            slow_print("You take solo photos instead.")
                            player["items"].append("Solo Photo Booth Pictures")

                # Common end for all arcade games
                slow_print(
                    f"You spent ¥{total_cost}. Remaining money: ¥{player['money']}"
                )

                # Advance time
                ticks += (
                    selected_game["rounds"] * 2
                )  # Each round is about 10-15 minutes

            elif choice_num == len(arcade_games) + 1:  # Just watch
                slow_print(
                    "You wander around the arcade, watching other people play games."
                )
                slow_print(
                    "It's entertaining and relaxing just to observe the excitement around you."
                )
                player["stress"] = max(0, player["stress"] - 5)
                ticks += 3  # About 20 minutes
            else:
                slow_print("You decide to leave the arcade center.")
        except ValueError:
            slow_print("You wander around the arcade for a bit then leave.")

    elif location == "Amusement Park":
        slow_print(f"\n{Fore.CYAN}=== Amusement Park ==={Style.RESET_ALL}")

        # Check if player has enough money for entrance
        entrance_fee = 3000
        if player["money"] < entrance_fee:
            slow_print(
                f"The entrance fee is ¥{entrance_fee}, but you only have ¥{player['money']}."
            )
            slow_print(
                "You decide to come back another time when you have enough money."
            )
            return

        slow_print(f"You pay the entrance fee of ¥{entrance_fee}.")
        player["money"] -= entrance_fee

        rides = [
            {"name": "Roller Coaster", "thrill": 30, "energy": -20},
            {"name": "Ferris Wheel", "thrill": 10, "energy": -5},
            {"name": "Water Ride", "thrill": 25, "energy": -15},
            {"name": "Haunted House", "thrill": 20, "energy": -10},
            {"name": "Carousel", "thrill": 5, "energy": -5},
        ]

        # How many rides to go on (energy dependent)
        max_rides = min(5, player["energy"] // 10)
        if max_rides == 0:
            slow_print(
                "You're too tired to go on any rides. Maybe come back another time."
            )
            # Refund entrance fee
            player["money"] += entrance_fee
            slow_print(f"You get a refund of ¥{entrance_fee}.")
            return

        ride_count = 0
        while ride_count < max_rides:
            print(
                f"\nYou can go on {max_rides - ride_count} more rides. Choose wisely!"
            )

            for i, ride in enumerate(rides, 1):
                print(f"{i}. {ride['name']}")
            print(f"{len(rides) + 1}. Exit the park")

            choice = input(
                f"Which ride would you like to go on? (1-{len(rides) + 1}): "
            )

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(rides):
                    selected_ride = rides[choice_num - 1]

                    slow_print(f"You go on the {selected_ride['name']}!")
                    player["stress"] = max(
                        0, player["stress"] - selected_ride["thrill"]
                    )
                    player["energy"] = max(
                        0, player["energy"] + selected_ride["energy"]
                    )

                    slow_print(
                        f"Stress -{selected_ride['thrill']}, Energy {selected_ride['energy']}"
                    )

                    # Chance for special event on rides
                    if random.random() < 0.3:  # 30% chance
                        if (
                            player.get("romantic_interest")
                            and player["romance_stage"] >= 2
                        ):
                            romantic_date_event()
                        else:
                            random_friend_encounter()

                    ride_count += 1

                    # Check if out of energy
                    if player["energy"] < 10:
                        slow_print("You're feeling too tired to go on more rides.")
                        break

                elif choice_num == len(rides) + 1:
                    slow_print("You decide to leave the amusement park.")
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid choice.")

        slow_print("You had a fun day at the amusement park!")

        # Advance time significantly
        ticks += 20  # About 2 hours


def weekend_rest_options():
    """Special rest options for weekends when in bedroom/dorm"""
    global ticks
    slow_print(f"\n{Fore.YELLOW}=== Weekend Relaxation ==={Style.RESET_ALL}")

    options = [
        {"name": "Sleep in late", "energy": 40, "stress": -15},
        {"name": "Binge watch shows", "energy": -10, "stress": -30},
        {"name": "Video games", "energy": -15, "stress": -25},
        {"name": "Call family", "energy": -5, "stress": -20},
        {"name": "Catch up on homework", "energy": -20, "intelligence": 15},
    ]

    print("How would you like to spend your free time?")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option['name']}")

    choice = input(f"Choose an activity (1-{len(options)}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(options):
            selected = options[choice_num - 1]

            slow_print(f"You decide to {selected['name'].lower()}.")

            # Apply effects
            for stat, change in selected.items():
                if stat != "name":
                    if stat == "energy":
                        player[stat] = min(100, max(0, player[stat] + change))
                    else:
                        player[stat] = min(100, player[stat] + change)

                    if change > 0:
                        slow_print(f"{stat.capitalize()} +{change}")
                    else:
                        slow_print(f"{stat.capitalize()} {change}")

            # Special case for calling family
            if choice_num == 4:
                improve_family_relationships()

            # Special case for homework
            if choice_num == 5:
                complete_random_homework()

            # Advance time
            ticks += 10  # About 1 hour
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")


def weekend_study_session():
    """Special weekend study options in the library"""
    global ticks
    slow_print(f"\n{Fore.YELLOW}=== Weekend Study Session ==={Style.RESET_ALL}")

    # Get current subjects
    current_subjects = get_current_subjects()

    if not current_subjects:
        slow_print("You don't have any subjects to study right now.")
        return

    print("The library is quieter on weekends, making it ideal for focused study.")
    print("Which subject would you like to focus on?")

    for i, subject_name in enumerate(current_subjects, 1):
        grade = player["grades"].get(subject_name, "N/A")
        print(f"{i}. {subject_name} (Current Grade: {grade})")

    print(f"{len(current_subjects) + 1}. Study all subjects briefly")

    choice = input(f"Choose an option (1-{len(current_subjects) + 1}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(current_subjects):
            # Study one subject intensively
            subject = current_subjects[choice_num - 1]

            slow_print(f"You spend several hours deeply focused on {subject}.")

            # Better results from weekend study
            grade_boost = random.uniform(0.3, 0.7)
            current_grade = player["grades"].get(subject, 60.0)
            new_grade = min(100.0, current_grade + grade_boost)
            player["grades"][subject] = new_grade

            # Complete homework for this subject
            homework[subject] = True

            # Increase academic charisma instead of intelligence
            player["charisma"]["academic"] = min(
                100, player["charisma"]["academic"] + random.randint(5, 10)
            )
            player["energy"] = max(0, player["energy"] - 25)
            player["stress"] = max(
                0, player["stress"] - 5
            )  # Slight stress reduction from accomplishment

            slow_print(f"Your understanding of {subject} has improved significantly!")
            slow_print(f"Grade in {subject}: {current_grade:.1f} → {new_grade:.1f}")
            slow_print("Academic Charisma +5-10, Energy -25")
            slow_print(f"You've completed your {subject} homework.")

            # Random chance to meet a study partner
            if random.random() < 0.4:  # 40% chance
                find_study_partner()

        elif choice_num == len(current_subjects) + 1:
            # Study all subjects briefly
            slow_print(
                "You spread your time across all subjects, making moderate progress in each."
            )

            for subject in current_subjects:
                grade_boost = random.uniform(0.1, 0.3)
                current_grade = player["grades"].get(subject, 60.0)
                new_grade = min(100.0, current_grade + grade_boost)
                player["grades"][subject] = new_grade

            player["charisma"]["academic"] = min(
                100, player["charisma"]["academic"] + random.randint(3, 7)
            )
            player["energy"] = max(0, player["energy"] - 30)

            slow_print("You've made progress in all your subjects.")
            slow_print("Academic Charisma +3-7, Energy -30")

            # Small chance to complete homework for random subject
            if random.random() < 0.3:  # 30% chance
                random_subject = random.choice(current_subjects)
                homework[random_subject] = True
                slow_print(f"You managed to complete your {random_subject} homework!")

        else:
            print("Invalid choice.")
            return

        # Advance time significantly
        ticks += 15  # About 1.5 hours

    except ValueError:
        print("Invalid choice.")


def improve_family_relationships():
    """Improve relationships with family members through a call"""
    if not player["family"]["parents"] and not player["family"]["siblings"]:
        slow_print("You have no family members to call.")
        return

    family_members = player["family"]["parents"] + player["family"]["siblings"]

    for member in family_members:
        name = member["name"]
        relation = member.get("relation", "family member")

        # Improve relationship
        current_relationship = player["family_relationship"].get(name, 50)
        improvement = random.randint(3, 8)
        player["family_relationship"][name] = min(
            100, current_relationship + improvement
        )

        slow_print(f"You had a nice conversation with your {relation}, {name}.")
        slow_print(f"Your relationship with {name} improved.")


def complete_random_homework():
    """Complete homework for random subjects during weekend study"""
    current_subjects = get_current_subjects()

    if not current_subjects:
        return

    # Complete 1-3 random homework assignments
    num_to_complete = min(len(current_subjects), random.randint(1, 3))
    subjects_to_complete = random.sample(list(current_subjects), num_to_complete)

    for subject in subjects_to_complete:
        homework[subject] = True
        slow_print(f"You completed your {subject} homework!")


def romantic_date_event():
    """Special romantic event during weekend activities"""
    if not player.get("romantic_interest"):
        return

    interest_name = player["romantic_interest"]

    # Find the student object
    interest = None
    for student in students:
        if student["name"] == interest_name:
            interest = student
            break

    if not interest:
        return

    slow_print(f"\n{Fore.MAGENTA}=== Romantic Encounter ==={Style.RESET_ALL}")
    slow_print(f"You run into {interest_name} during your weekend activity!")

    personality = interest.get("personality", "kind")

    # Different dialogue based on personality and romance stage
    stage = player["romance_stage"]

    if stage <= 2:
        slow_print(f"{interest_name} seems pleasantly surprised to see you.")
        slow_print("They suggest joining you for a while.")

        print("\nHow do you respond?")
        print("1. Enthusiastically welcome them to join you")
        print("2. Act cool but accept")
        print("3. Make an excuse about being busy")

        choice = input("Choose your response (1-3): ")

        if choice == "1":
            slow_print(f"You happily invite {interest_name} to join you.")
            slow_print(
                "You spend a fun time together and get to know each other better."
            )
            player["romance_stage"] = min(5, stage + 1)
            slow_print(f"Your relationship with {interest_name} has advanced!")
        elif choice == "2":
            slow_print("You act casual but agree to hang out together.")
            slow_print("You have a pleasant time, though you maintain some distance.")
            if random.random() < 0.5:  # 50% chance to advance
                player["romance_stage"] = min(5, stage + 1)
                slow_print(f"Your relationship with {interest_name} has advanced!")
        else:
            slow_print("You make an excuse about being busy.")
            slow_print(f"{interest_name} looks disappointed as they leave.")
            if stage > 0:
                player["romance_stage"] = max(0, stage - 1)
                slow_print(f"Your relationship with {interest_name} has regressed.")

    else:  # Stage 3+
        slow_print(f"{interest_name}'s face lights up when they see you.")
        slow_print('"I was hoping I might run into you today!" they say.')

        print("\nWhat would you like to do?")
        print("1. Suggest turning this into a proper date")
        print("2. Casually spend time together")
        print("3. Keep it brief, say you need to go soon")

        choice = input("Choose your response (1-3): ")

        if choice == "1":
            slow_print(
                f"You suggest making this an official date with {interest_name}."
            )
            slow_print(f"{interest_name} blushes happily and agrees.")
            slow_print("You have a wonderful time together, creating special memories.")
            player["romance_stage"] = min(5, stage + 1)
            slow_print(f"Your relationship with {interest_name} has grown stronger!")

            # Special romantic moment based on personality
            if personality == "tsundere":
                slow_print(
                    f'At the end of the date, {interest_name} hesitantly says, "I... I guess this wasn\'t terrible. We could... maybe do it again sometime."'
                )
            elif personality == "kuudere":
                slow_print(
                    f'{interest_name} looks at you with a slight softening in their usually stoic expression. "This was... pleasant. I would not be opposed to repeating it."'
                )
            elif personality == "dandere":
                slow_print(
                    f'{interest_name} shyly takes your hand for a moment. "Th-thank you for today. It was really special."'
                )
            elif personality == "deredere":
                slow_print(
                    f'{interest_name} hugs you enthusiastically. "This was the BEST day ever! Let\'s do this again soon, okay?"'
                )
            elif personality == "yandere":
                slow_print(
                    f'{interest_name} looks intensely into your eyes. "No one else gets to see you like this. Only me. Remember that."'
                )
            elif personality == "genki":
                slow_print(
                    f'{interest_name} jumps excitedly. "That was super fun! We make an awesome team! Same time next weekend?"'
                )
            elif personality == "himedere":
                slow_print(
                    f'{interest_name} gives you a regal nod. "I suppose I can pencil you in for another outing. Consider yourself fortunate."'
                )
            else:
                slow_print(
                    f'{interest_name} smiles warmly at you. "Thank you for today. I really enjoyed spending time with you."'
                )

        elif choice == "2":
            slow_print(
                "You casually spend time together, enjoying each other's company."
            )
            slow_print("It's comfortable and enjoyable, if not particularly romantic.")
            if random.random() < 0.3:  # 30% chance to advance
                player["romance_stage"] = min(5, stage + 1)
                slow_print(f"Your relationship with {interest_name} has advanced!")

        else:
            slow_print("You tell them you can only stay for a little while.")
            slow_print(f"{interest_name} tries to hide their disappointment.")
            slow_print("You chat briefly before parting ways.")
            # No regression but no advancement either


def random_friend_encounter():
    """Random encounter with a friend or potential friend during weekend activities"""
    # Select a random student who isn't a romantic interest
    available_students = [
        s for s in students if s["name"] != player.get("romantic_interest")
    ]

    if not available_students:
        return

    student = random.choice(available_students)
    name = student["name"]
    personality = student.get("personality", "kind")

    slow_print(f"\n{Fore.GREEN}=== Chance Encounter ==={Style.RESET_ALL}")
    slow_print(f"You run into {name} during your weekend activity!")

    # Check existing relationship
    relationship = player["relationships"].get(name, 0)

    if relationship < 20:
        slow_print(f"You don't know {name} very well, but they greet you politely.")
    elif relationship < 50:
        slow_print(f"{name} seems happy to see a familiar face.")
    else:
        slow_print(f"{name} greets you enthusiastically like an old friend!")

    print("\nHow do you respond?")
    print("1. Chat enthusiastically and spend time together")
    print("2. Have a brief, friendly conversation")
    print("3. Just give a quick greeting and continue your activity")

    choice = input("Choose your response (1-3): ")

    if choice == "1":
        slow_print(
            f"You have a great conversation with {name} and spend some time together."
        )
        relationship_boost = random.randint(10, 20)
        current = player["relationships"].get(name, 0)
        player["relationships"][name] = min(100, current + relationship_boost)
        slow_print(f"Your friendship with {name} has improved significantly!")

        # Special interaction based on personality
        if personality == "tsundere":
            slow_print(
                f"{name} tries to act indifferent but clearly enjoys your company."
            )
        elif personality == "kuudere":
            slow_print(
                f"{name} remains calm, but you notice them relaxing slightly as you talk."
            )
        elif personality == "dandere":
            slow_print(
                f"{name} gradually becomes more talkative as they get comfortable with you."
            )
        elif personality == "deredere":
            slow_print(
                f"{name} enthusiastically shares stories and laughs at all your jokes."
            )
        elif personality == "yandere":
            slow_print(
                f"{name} seems very interested in your personal life and other friendships."
            )
        elif personality == "genki":
            slow_print(
                f"{name} bubbles with energy, making your time together action-packed and fun."
            )
        elif personality == "himedere":
            slow_print(f"{name} acts superior but clearly values your attention.")
        else:
            slow_print(f"You and {name} discover you have several common interests.")

    elif choice == "2":
        slow_print(
            f"You have a pleasant chat with {name} before continuing your activities."
        )
        relationship_boost = random.randint(5, 10)
        current = player["relationships"].get(name, 0)
        player["relationships"][name] = min(100, current + relationship_boost)
        slow_print(f"Your friendship with {name} has improved!")

    else:
        slow_print(
            f"You exchange brief pleasantries with {name} and continue on your way."
        )
        relationship_boost = random.randint(0, 3)
        current = player["relationships"].get(name, 0)
        player["relationships"][name] = min(100, current + relationship_boost)

    # Potential study benefit if they're studious
    if student.get("personality") in ["serious", "kuudere"] and choice in ["1", "2"]:
        current_subjects = get_current_subjects()
        if current_subjects:
            subject = random.choice(current_subjects)
            grade_boost = random.uniform(0.1, 0.3)
            current_grade = player["grades"].get(subject, 60.0)
            new_grade = min(100.0, current_grade + grade_boost)
            player["grades"][subject] = new_grade
            slow_print(
                f"{name} mentions something helpful about {subject} that improves your understanding!"
            )
            slow_print(f"Your grade in {subject} slightly improved.")


def find_study_partner():
    """Find a study partner during weekend library session"""
    # Select a random student with "serious" or "kuudere" personality
    studious_students = [
        s for s in students if s.get("personality") in ["serious", "kuudere", "strict"]
    ]

    if not studious_students:
        # Fall back to any student
        available_students = [s for s in students]
        if not available_students:
            return
        student = random.choice(available_students)
    else:
        student = random.choice(studious_students)

    name = student["name"]
    personality = student.get("personality", "serious")

    slow_print(f"\n{Fore.CYAN}=== Study Partner ==={Style.RESET_ALL}")
    slow_print(f"You notice {name} is also studying in the library today.")

    print("\nWould you like to approach them to study together?")
    print("1. Yes, suggest studying together")
    print("2. No, continue studying alone")

    choice = input("Choose an option (1-2): ")

    if choice == "1":
        slow_print(f"You approach {name} and suggest studying together.")

        # Personality-based response
        if personality in ["serious", "strict", "kuudere"]:
            slow_print(f"{name} nods approvingly at your studious attitude.")
            acceptance = 0.9  # 90% chance they'll accept
        else:
            slow_print(f"{name} seems surprised at your suggestion.")
            acceptance = 0.6  # 60% chance they'll accept

        if random.random() < acceptance:
            slow_print(f"{name} agrees to study with you.")

            # Academic benefit
            current_subjects = get_current_subjects()
            subject = None
            if current_subjects:
                subject = random.choice(current_subjects)
                grade_boost = random.uniform(0.3, 0.8)
                current_grade = player["grades"].get(subject, 60.0)
                new_grade = min(100.0, current_grade + grade_boost)
                player["grades"][subject] = new_grade

                # Complete homework for this subject
                homework[subject] = True
                slow_print(
                    f"You made progress on your {subject} homework with a grade boost from {current_grade:.1f} to {new_grade:.1f}."
                )

            # Relationship improvement
            relationship_boost = random.randint(5, 15)
            current = player["relationships"].get(name, 0)
            player["relationships"][name] = min(100, current + relationship_boost)

            # Show different message based on whether a subject was chosen
            if subject:
                slow_print(
                    f"Studying with {name} helps you understand {subject} much better!"
                )
            else:
                slow_print(
                    f"Studying with {name} helps you understand your coursework better!"
                )
            slow_print(f"Your friendship with {name} has improved!")

            # Intelligence boost
            player["intelligence"] = min(
                100, player["intelligence"] + random.randint(3, 8)
            )
            slow_print("Intelligence +3-8")
        else:
            slow_print(f"{name} politely declines, saying they prefer to study alone.")

            # Small relationship improvement for trying
            relationship_boost = random.randint(1, 3)
            current = player["relationships"].get(name, 0)
            player["relationships"][name] = min(100, current + relationship_boost)
    else:
        slow_print("You decide to continue studying on your own.")


def clothes_shopping():
    """Shopping for clothes at the mall"""
    slow_print(f"\n{Fore.CYAN}=== Clothing Store ==={Style.RESET_ALL}")

    # Filter out clothing the player already owns
    available_clothing = {}
    for name, details in CLOTHING_ITEMS.items():
        if name not in player["clothing"]["owned"]:
            available_clothing[name] = details

    if not available_clothing:
        slow_print("You already own all available clothing items!")
        return

    # Display available clothing
    print(f"\n{Fore.YELLOW}Available Clothing Items:{Style.RESET_ALL}")
    clothing_list = []
    for i, (name, details) in enumerate(available_clothing.items(), 1):
        clothing_list.append(name)
        price_text = f"¥{details['price']}"

        # Build stat bonuses text
        stat_bonuses = []
        if "charisma" in details:
            stat_bonuses.append(
                f"Charisma {'+'if details['charisma'] >= 0 else ''}{details['charisma']}"
            )
        if "energy_boost" in details:
            stat_bonuses.append(f"Energy +{details['energy_boost']}")
        if "health_boost" in details:
            stat_bonuses.append(f"Health +{details['health_boost']}")
        if "reputation_boost" in details:
            stat_bonuses.append(f"Reputation +{details['reputation_boost']}")

        stat_text = ", ".join(stat_bonuses) if stat_bonuses else "No stat bonuses"

        print(f"{i}. {name} - {price_text}")
        print(f"   {Fore.CYAN}Type:{Style.RESET_ALL} {details['type'].capitalize()}")
        print(f"   {Fore.CYAN}Description:{Style.RESET_ALL} {details['description']}")
        print(f"   {Fore.CYAN}Effects:{Style.RESET_ALL} {stat_text}")
        print()

    print(f"{len(clothing_list) + 1}. Just browse (no purchase)")

    if len(clothing_list) == 0:
        slow_print("There are no new clothing items available for purchase.")
        slow_print("You browse the clothing stores without buying anything.")
        player["stress"] = max(0, player["stress"] - 5)
        slow_print("Window shopping is relaxing. Stress -5")

        # Advance time
        global ticks
        ticks += 5  # About 30 minutes
        return

    choice = input(f"What would you like to buy? (1-{len(clothing_list) + 1}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(clothing_list):
            clothing_name = clothing_list[choice_num - 1]
            clothing_details = available_clothing[clothing_name]

            # Check if player has enough money
            if player["money"] < clothing_details["price"]:
                slow_print(
                    f"You don't have enough money for that. You need ¥{clothing_details['price']}."
                )
                return

            # Purchase item
            player["money"] -= clothing_details["price"]
            player["clothing"]["owned"].append(clothing_name)

            slow_print(f"{Fore.GREEN}You purchased {clothing_name}!{Style.RESET_ALL}")
            slow_print(
                f"You spent ¥{clothing_details['price']}. Remaining money: ¥{player['money']}"
            )

            # Ask if player wants to wear the new clothing right away
            wear_now = input(
                "Would you like to wear your new clothing now? (y/n): "
            ).lower()
            if wear_now == "y":
                # Check if in appropriate location for changing
                if player["current_location"] in CHANGING_LOCATIONS:
                    # Remove effects of current clothing
                    if player["clothing"]["wearing"]:
                        apply_clothing_effects(
                            player["clothing"]["wearing"], apply=False
                        )

                    # Change to new clothing
                    player["clothing"]["wearing"] = clothing_name
                    apply_clothing_effects(clothing_name, apply=True)

                    slow_print(f"You changed into your new {clothing_name}.")

                    # Check appropriateness for current location
                    is_weekday = current_date.weekday() < 5
                    is_festival_day = check_for_special_events()
                    clothing_appropriate, reason = is_clothing_appropriate(
                        clothing_name,
                        player["current_location"],
                        is_school_day=is_weekday,
                        is_festival=is_festival_day,
                    )

                    if not clothing_appropriate:
                        slow_print(f"Warning: {reason}")
                else:
                    slow_print(
                        "You can't change clothes here. You need to be in your room or a changing room."
                    )

            # Random compliment chance for stylish clothing
            if (
                "charisma" in clothing_details
                and clothing_details["charisma"] > 5
                and random.random() < 0.4
            ):
                slow_print("A stranger compliments your purchase!")
                player["stress"] = max(0, player["stress"] - 5)
                slow_print("The compliment boosts your confidence. Stress -5")

        elif choice_num == len(clothing_list) + 1:
            slow_print("You browse the clothing stores without buying anything.")
            player["stress"] = max(0, player["stress"] - 5)
            slow_print("Window shopping is relaxing. Stress -5")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Invalid choice.")

    # Advance time
    ticks += 5  # About 30 minutes


def bookstore_shopping():
    """Shopping at the bookstore"""
    slow_print(f"\n{Fore.CYAN}=== Bookstore ==={Style.RESET_ALL}")

    books = [
        {"name": "Academic Study Guide", "price": 2500, "intelligence": 8},
        {"name": "Popular Novel", "price": 1200, "stress": -15},
        {"name": "Self-Improvement Book", "price": 1800, "intelligence": 3, "charm": 3},
        {"name": "Manga Collection", "price": 1000, "stress": -10, "creativity": 5},
        {"name": "Historical Biography", "price": 2000, "intelligence": 5, "wisdom": 5},
    ]

    print("Available books:")
    for i, book in enumerate(books, 1):
        price_text = f"¥{book['price']}"
        stat_text = ""

        for stat, value in book.items():
            if stat not in ["name", "price"]:
                if stat == "stress":
                    stat_text += f"Stress {value}, "
                else:
                    stat_text += f"{stat.capitalize()} +{value}, "

        stat_text = stat_text.rstrip(", ")

        print(f"{i}. {book['name']} - {price_text} ({stat_text})")

    print(f"{len(books) + 1}. Just browse (no purchase)")

    choice = input(f"What would you like to buy? (1-{len(books) + 1}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(books):
            book = books[choice_num - 1]

            # Check if player has enough money
            if player["money"] < book["price"]:
                slow_print(
                    f"You don't have enough money for that. You need ¥{book['price']}."
                )
                return

            # Purchase book
            player["money"] -= book["price"]

            slow_print(f"You purchase '{book['name']}'!")

            for stat, value in book.items():
                if stat not in ["name", "price"]:
                    if stat == "stress":
                        player[stat] = max(0, player[stat] + value)
                        slow_print(f"Stress {value}")
                    else:
                        player[stat] = min(100, player[stat] + value)
                        slow_print(f"{stat.capitalize()} +{value}")

            slow_print(
                f"You spent ¥{book['price']}. Remaining money: ¥{player['money']}"
            )

            # Subject boost for academic books
            if book["name"] == "Academic Study Guide":
                current_subjects = get_current_subjects()
                if current_subjects:
                    subject = random.choice(current_subjects)
                    grade_boost = random.uniform(0.2, 0.5)
                    current_grade = player["grades"].get(subject, 60.0)
                    new_grade = min(100.0, current_grade + grade_boost)
                    player["grades"][subject] = new_grade
                    slow_print(f"The study guide helps with your {subject} class!")
                    slow_print(f"Your grade in {subject} improved!")

        elif choice_num == len(books) + 1:
            slow_print("You browse the bookstore without buying anything.")

            # Chance to learn something anyway
            if random.random() < 0.3:
                player["intelligence"] = min(100, player["intelligence"] + 2)
                slow_print(
                    "You learn something interesting from browsing books. Intelligence +2"
                )

            player["stress"] = max(0, player["stress"] - 5)
            slow_print("Browsing books is relaxing. Stress -5")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Invalid choice.")

    # Advance time
    global ticks
    ticks += 4  # About 25 minutes


def electronics_shopping():
    """Shopping at the electronics store"""
    slow_print(f"\n{Fore.CYAN}=== Electronics Store ==={Style.RESET_ALL}")

    items = [
        {"name": "Study Tablet", "price": 15000, "intelligence": 5, "productivity": 10},
        {"name": "Gaming Console", "price": 25000, "stress": -20, "creativity": 5},
        {
            "name": "Noise-Canceling Headphones",
            "price": 8000,
            "stress": -10,
            "productivity": 5,
        },
        {"name": "E-reader", "price": 10000, "intelligence": 8},
        {"name": "Smart Watch", "price": 12000, "health": 5, "productivity": 5},
    ]

    print("Available electronics:")
    for i, item in enumerate(items, 1):
        price_text = f"¥{item['price']}"
        stat_text = ""

        for stat, value in item.items():
            if stat not in ["name", "price"]:
                if stat == "stress":
                    stat_text += f"Stress {value}, "
                else:
                    stat_text += f"{stat.capitalize()} +{value}, "

        stat_text = stat_text.rstrip(", ")

        print(f"{i}. {item['name']} - {price_text} ({stat_text})")

    print(f"{len(items) + 1}. Just browse (no purchase)")

    choice = input(f"What would you like to buy? (1-{len(items) + 1}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(items):
            item = items[choice_num - 1]

            # Check if player has enough money
            if player["money"] < item["price"]:
                slow_print(
                    f"You don't have enough money for that. You need ¥{item['price']}."
                )
                return

            # Purchase item
            player["money"] -= item["price"]

            slow_print(f"You purchase a {item['name']}!")

            for stat, value in item.items():
                if stat not in ["name", "price"]:
                    if stat == "stress":
                        player[stat] = max(0, player[stat] + value)
                        slow_print(f"Stress {value}")
                    elif stat == "productivity":
                        # Add productivity bonus to player inventory instead of direct stat
                        player["items"] = player.get("items", [])
                        player["items"].append(item["name"])
                        slow_print(f"Productivity +{value} (Item added to inventory)")
                    else:
                        player[stat] = min(100, player[stat] + value)
                        slow_print(f"{stat.capitalize()} +{value}")

            slow_print(
                f"You spent ¥{item['price']}. Remaining money: ¥{player['money']}"
            )

        elif choice_num == len(items) + 1:
            slow_print("You browse the electronics store without buying anything.")
            player["stress"] = max(0, player["stress"] - 3)
            slow_print("Looking at the latest tech is entertaining. Stress -3")

        else:
            print("Invalid choice.")

    except ValueError:
        print("Invalid choice.")

    # Advance time
    global ticks
    ticks += 6  # About 35-40 minutes


def food_court_meal():
    """Having a meal at the food court"""
    slow_print(f"\n{Fore.CYAN}=== Food Court ==={Style.RESET_ALL}")

    food_options = [
        {
            "name": "Fast Food Combo",
            "price": 800,
            "hunger": 70,
            "energy": 10,
            "health": -5,
        },
        {"name": "Healthy Salad", "price": 900, "hunger": 50, "health": 10},
        {"name": "Gourmet Burger", "price": 1200, "hunger": 80, "energy": 15},
        {
            "name": "International Cuisine",
            "price": 1500,
            "hunger": 75,
            "energy": 10,
            "stress": -10,
        },
        {
            "name": "Sweet Dessert",
            "price": 600,
            "hunger": 30,
            "stress": -15,
            "health": -3,
        },
    ]

    print("Available food options:")
    for i, food in enumerate(food_options, 1):
        price_text = f"¥{food['price']}"
        stat_text = f"Hunger +{food['hunger']}"

        for stat, value in food.items():
            if stat not in ["name", "price", "hunger"]:
                if value > 0:
                    stat_text += f", {stat.capitalize()} +{value}"
                else:
                    stat_text += f", {stat.capitalize()} {value}"

        print(f"{i}. {food['name']} - {price_text} ({stat_text})")

    print(f"{len(food_options) + 1}. Just look around (don't eat)")

    choice = input(f"What would you like to eat? (1-{len(food_options) + 1}): ")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(food_options):
            food = food_options[choice_num - 1]

            # Check if player has enough money
            if player["money"] < food["price"]:
                slow_print(
                    f"You don't have enough money for that. You need ¥{food['price']}."
                )
                return

            # Purchase food
            player["money"] -= food["price"]
            player["hunger"] = min(100, player["hunger"] + food["hunger"])

            slow_print(f"You enjoy a delicious {food['name']}!")
            slow_print(f"Hunger +{food['hunger']}")

            for stat, value in food.items():
                if stat not in ["name", "price", "hunger"]:
                    player[stat] = min(100, max(0, player[stat] + value))
                    if value > 0:
                        slow_print(f"{stat.capitalize()} +{value}")
                    else:
                        slow_print(f"{stat.capitalize()} {value}")

            slow_print(
                f"You spent ¥{food['price']}. Remaining money: ¥{player['money']}"
            )

            # Random chance to meet someone
            if random.random() < 0.3:  # 30% chance
                random_friend_encounter()

        elif choice_num == len(food_options) + 1:
            slow_print(
                "You decide not to eat anything and just look around the food court."
            )

        else:
            print("Invalid choice.")

    except ValueError:
        print("Invalid choice.")


# Track holiday events that have been shown
holiday_events_shown = {
    "lunar_new_year": False,
    "summer_holiday": False,
    "winter_holiday": False,
    "spring_break": False,
}


def is_holiday():
    # Regular holidays
    holidays = [
        (1, 1),  # New Year's Day
        (1, 15),  # Coming of Age Day (second Monday of January)
        (2, 11),  # National Foundation Day
        (2, 23),  # Emperor's Birthday
        (3, 20),  # Spring Equinox
        (4, 29),  # Showa Day
        (5, 3),  # Constitution Memorial Day
        (5, 4),  # Greenery Day
        (5, 5),  # Children's Day
        (7, 17),  # Marine Day (third Monday of July)
        (8, 11),  # Mountain Day
        (9, 18),  # Respect for the Aged Day (third Monday of September)
        (9, 23),  # Autumn Equinox
        (10, 9),  # Sports Day (second Monday of October)
        (11, 3),  # Culture Day
        (11, 23),  # Labor Thanksgiving Day
        (12, 25),  # Christmas
    ]

    # Check for Lunar New Year (approximate dates for multiple years)
    lunar_new_year_dates = [
        (1, 22),  # 2023
        (2, 10),  # 2024
        (1, 29),  # 2025
        (2, 17),  # 2026
    ]

    # Check if it's a holiday
    is_regular_holiday = (current_date.month, current_date.day) in holidays
    is_lunar_new_year = (current_date.month, current_date.day) in lunar_new_year_dates

    # Summer holiday period (July 20 to August 31)
    is_summer_holiday = (current_date.month == 7 and current_date.day >= 20) or (
        current_date.month == 8
    )

    # Winter holiday period (December 24 to January 7)
    is_winter_holiday = (current_date.month == 12 and current_date.day >= 24) or (
        current_date.month == 1 and current_date.day <= 7
    )

    # Spring break (March 15 to April 5)
    is_spring_break = (current_date.month == 3 and current_date.day >= 15) or (
        current_date.month == 4 and current_date.day <= 5
    )

    # Special holiday messages and events
    # No need for global as we're only modifying dictionary entries, not reassigning the variable

    # Lunar New Year Celebration
    if is_lunar_new_year and not holiday_events_shown["lunar_new_year"]:
        slow_print(
            f"\n{Fore.RED}======= LUNAR NEW YEAR FESTIVAL ======={Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.RED}Happy Lunar New Year! The campus is decorated with red lanterns and traditional decorations.{Style.RESET_ALL}"
        )
        slow_print(
            "Many students have returned to their families, but special activities are available for those who stayed."
        )

        # Give player a red envelope (bonus money)
        lucky_money = random.choice([88, 188, 288, 388, 588, 888])
        player["money"] += lucky_money
        slow_print(
            f"\n{Fore.RED}You received a red envelope with ¥{lucky_money} as a New Year's gift!{Style.RESET_ALL}"
        )

        # Special reputation boost
        reputation_boost = random.randint(3, 8)
        player["reputation"]["students"] += reputation_boost
        player["reputation"]["teachers"] += reputation_boost
        slow_print(
            "Your participation in New Year festivities increased your reputation!"
        )

        # Lunar New Year activities
        print(f"\n{Fore.YELLOW}Lunar New Year Activities:{Style.RESET_ALL}")
        print("1. Attend the lion dance performance")
        print("2. Help decorate the campus")
        print("3. Learn calligraphy")
        print("4. Cook traditional food with other students")

        choice = input("\nHow would you like to celebrate? (1-4): ")
        if choice == "1":
            slow_print(
                "You enjoyed the exciting lion dance performance with drums and cymbals!"
            )
            slow_print("The performers were impressed by your enthusiasm.")
            player["stress"] = max(0, player["stress"] - 15)
            player["charisma"]["social"] += 1
        elif choice == "2":
            slow_print(
                "You spent time hanging red lanterns and spring couplets around campus."
            )
            slow_print(
                "The teachers appreciated your help and the campus looks beautiful!"
            )
            player["reputation"]["teachers"] += 5
            player["charisma"]["social"] += 1
        elif choice == "3":
            slow_print(
                "You learned how to write New Year blessings in beautiful calligraphy."
            )
            player["charisma"]["academic"] += 2
            player["stress"] = max(0, player["stress"] - 10)
        elif choice == "4":
            slow_print(
                "You spent time making dumplings and other traditional foods with fellow students."
            )
            slow_print(
                "Everyone enjoyed the delicious meal and appreciated your cooking skills!"
            )
            player["hunger"] = 100
            player["reputation"]["students"] += 5
            player["charisma"]["social"] += 1

        # Remember that we've shown this event
        holiday_events_shown["lunar_new_year"] = True

    # Summer holiday special events
    if (
        is_summer_holiday
        and current_date.day == 20
        and current_date.month == 7
        and not holiday_events_shown["summer_holiday"]
    ):
        slow_print(
            f"\n{Fore.YELLOW}======= SUMMER VACATION BEGINS ======={Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.YELLOW}Summer vacation has started! You have free time until the end of August.{Style.RESET_ALL}"
        )
        slow_print(
            "The campus is much quieter now, with most students gone for the break."
        )

        # Summer holiday activities menu
        print(f"\n{Fore.CYAN}How will you spend your summer?{Style.RESET_ALL}")
        print("1. Work full-time (earn more money)")
        print("2. Summer studies (improve academics)")
        print("3. Travel (increase social skills and reduce stress)")
        print("4. Relax at home (recover energy and reduce stress)")
        print("5. Summer school internship (academic reputation and experience)")

        choice = input("\nWhat would you like to do this summer? (1-5): ")
        if choice == "1":
            # Work full-time
            earnings = 5000 + (player["charisma"]["social"] * 200)
            player["money"] += earnings
            player["energy"] -= 30
            player["stress"] += 15
            slow_print(
                f"You worked hard all summer at a resort and earned ¥{earnings}!"
            )
            slow_print(
                "Your experience dealing with customers improved your social skills."
            )
            player["charisma"]["social"] += 2

            # Add achievement if this is first summer job
            if "Summer Worker" not in player["achievements"]:
                player["achievements"].append("Summer Worker")
                slow_print(
                    f"{Fore.GREEN}Achievement Unlocked: Summer Worker{Style.RESET_ALL}"
                )

        elif choice == "2":
            # Summer studies
            player["charisma"]["academic"] += 3
            player["stress"] += 10

            # Improve grades
            improved = 0
            for subject in list(player["grades"].keys()):
                if (
                    player["grades"][subject] != "A"
                    and player["grades"][subject] != "A+"
                ):
                    if player["grades"][subject] == "B":
                        player["grades"][subject] = "A"
                        improved += 1
                    elif player["grades"][subject] == "C":
                        player["grades"][subject] = "B"
                        improved += 1
                    elif player["grades"][subject] == "D":
                        player["grades"][subject] = "C"
                        improved += 1
                    elif player["grades"][subject] == "F":
                        player["grades"][subject] = "D"
                        improved += 1

            slow_print(
                f"You studied hard over the summer and improved in {improved} subjects!"
            )
            slow_print(
                "Your focus on academics has made you better prepared for the coming year."
            )
            player["reputation"]["teachers"] += 5

            # Add achievement if grades significantly improved
            if improved >= 3 and "Summer Scholar" not in player["achievements"]:
                player["achievements"].append("Summer Scholar")
                slow_print(
                    f"{Fore.GREEN}Achievement Unlocked: Summer Scholar{Style.RESET_ALL}"
                )

        elif choice == "3":
            # Travel
            player["charisma"]["social"] += 3
            player["money"] -= 3000
            player["stress"] = max(0, player["stress"] - 30)

            destinations = [
                "the beach",
                "the mountains",
                "a historic city",
                "a foreign country",
            ]
            destination = random.choice(destinations)

            slow_print(f"You traveled to {destination} and had an amazing adventure!")
            slow_print(
                "You met many interesting people and learned about different cultures."
            )
            slow_print(
                "The experience broadened your horizons and reduced your stress."
            )

            # Add achievement for first travel experience
            if "World Traveler" not in player["achievements"]:
                player["achievements"].append("World Traveler")
                slow_print(
                    f"{Fore.GREEN}Achievement Unlocked: World Traveler{Style.RESET_ALL}"
                )

        elif choice == "4":
            # Relax at home
            player["energy"] = 100
            player["stress"] = 0
            player["health"] = 100

            slow_print(
                "You had a relaxing summer at home, catching up on sleep and hobbies."
            )
            slow_print("You feel completely refreshed and ready for the new term!")

            # Small money bonus from family
            allowance = random.randint(500, 1500)
            player["money"] += allowance
            slow_print(f"Your family gave you a summer allowance of ¥{allowance}.")

        elif choice == "5":
            # Summer internship
            player["charisma"]["academic"] += 4
            player["reputation"]["teachers"] += 15
            player["money"] += 2000
            player["stress"] += 20

            internship_types = [
                "research assistant",
                "teaching assistant",
                "laboratory technician",
            ]
            internship = random.choice(internship_types)

            slow_print(f"You spent your summer as a {internship} at the university.")
            slow_print("The experience was challenging but very rewarding.")
            slow_print(
                "You made valuable connections with faculty and gained practical experience."
            )

            # Add internship to player's record
            if "internships" not in player:
                player["internships"] = []
            player["internships"].append(f"Summer {internship.title()}")

            # Add achievement
            if "Summer Intern" not in player["achievements"]:
                player["achievements"].append("Summer Intern")
                slow_print(
                    f"{Fore.GREEN}Achievement Unlocked: Summer Intern{Style.RESET_ALL}"
                )

        # Time skip for summer (advance date to August 31)
        summer_end = datetime(current_date.year, 8, 31)
        days_passed = (summer_end - current_date).days + 1

        # Fast forward through summer
        for _ in range(days_passed):
            advance_day()

        slow_print(
            f"\n{Fore.YELLOW}Summer vacation has ended. Classes will resume tomorrow.{Style.RESET_ALL}"
        )
        slow_print("You hope this will be a great semester!")

        # Remember that we've shown this event
        holiday_events_shown["summer_holiday"] = True

    # Winter holiday events
    if (
        is_winter_holiday
        and current_date.day == 24
        and current_date.month == 12
        and not holiday_events_shown["winter_holiday"]
    ):
        slow_print(
            f"\n{Fore.CYAN}======= WINTER HOLIDAY BEGINS ======={Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.CYAN}Winter break has started! The campus is decorated for the holidays.{Style.RESET_ALL}"
        )
        slow_print("Many students have gone home to celebrate with family.")

        # Small gift and money from family
        player["money"] += 1000
        slow_print(
            "Your family sent you ¥1000 and a small care package for the holidays!"
        )
        player["hunger"] = 100
        player["energy"] += 20

        # Remember that we've shown this event
        holiday_events_shown["winter_holiday"] = True

    # Spring break events
    if (
        is_spring_break
        and current_date.day == 15
        and current_date.month == 3
        and not holiday_events_shown["spring_break"]
    ):
        slow_print(
            f"\n{Fore.GREEN}======= SPRING BREAK BEGINS ======={Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.GREEN}Spring break has begun! A short rest before the end of the academic year.{Style.RESET_ALL}"
        )
        slow_print(
            "Many students are studying for final exams or enjoying a brief vacation."
        )

        # Give a small energy boost
        player["energy"] += 30
        player["stress"] = max(0, player["stress"] - 20)

        # Remember that we've shown this event
        holiday_events_shown["spring_break"] = True

    return (
        is_regular_holiday
        or is_lunar_new_year
        or is_summer_holiday
        or is_winter_holiday
        or is_spring_break
    )


def check_curfew():
    """Check if player is violating curfew and handle consequences"""
    global curfew_violations
    
    # Only applies to players living at home
    if player["accommodation_type"] != "home":
        return
    
    # Get current time
    current_hour = (ticks // 10) % 24
    
    # Check if it's past curfew
    if current_hour >= CURFEW_HOUR or current_hour < 6:  # Between 10 PM and 6 AM
        # Define home locations
        home_locations = ["Your Bedroom", "Living Room", "Kitchen", "Home Study"]
        
        # Check if player is not at home
        if player["current_location"] not in home_locations:
            slow_print(f"\n{Fore.RED}=== CURFEW VIOLATION ==={Style.RESET_ALL}")
            slow_print(f"It's {current_hour}:00, past your curfew of {CURFEW_HOUR}:00!")
            
            # Player will be teleported home after this check
            
            # Determine which parent will scold the player
            if "family" in player and "parents" in player["family"] and player["family"]["parents"]:
                scolding_parent = random.choice(player["family"]["parents"])
                parent_name = scolding_parent["name"]
                parent_personality = scolding_parent["personality"]
                
                if parent_personality in ["strict", "protective", "traditional"]:
                    # Stricter parents have harsher reactions
                    penalty = random.randint(10, 20)
                    stress_increase = random.randint(15, 25)
                    
                    slow_print(f"{Fore.RED}{parent_name} is furious that you've stayed out past curfew!{Style.RESET_ALL}")
                    slow_print(f"\"Where have you been? Do you know what time it is?\" {parent_name} demands.")
                    
                    # Apply a relationship penalty with this parent
                    if parent_name in player["family_relationship"]:
                        player["family_relationship"][parent_name] = max(0, player["family_relationship"][parent_name] - penalty)
                        slow_print(f"Relationship with {parent_name} decreased by {penalty} points.")
                    
                    # Possible grounding
                    if curfew_violations >= 2:
                        slow_print(f"{Fore.RED}You've been grounded for the next 3 days! Your movements will be restricted.{Style.RESET_ALL}")
                        player["grounded"] = 3  # Grounded for 3 days
                    
                else:
                    # More lenient parents have milder reactions
                    penalty = random.randint(5, 10)
                    stress_increase = random.randint(5, 15)
                    
                    slow_print(f"{Fore.YELLOW}{parent_name} is concerned that you've stayed out past curfew.{Style.RESET_ALL}")
                    slow_print(f"\"I was worried about you. Please try to be home on time,\" {parent_name} says.")
                    
                    # Apply a smaller relationship penalty with this parent
                    if parent_name in player["family_relationship"]:
                        player["family_relationship"][parent_name] = max(0, player["family_relationship"][parent_name] - penalty)
                        slow_print(f"Relationship with {parent_name} decreased by {penalty} points.")
                
                # Increase stress regardless of parent type
                player["stress"] = min(100, player["stress"] + stress_increase)
                slow_print(f"Your stress level increased by {stress_increase} points.")
                
                # Increase violation count
                curfew_violations += 1
            
            # Teleport player home
            player["current_location"] = "Your Bedroom"
            slow_print("You've been sent to your bedroom.")
            
            return True  # Return True to indicate a curfew violation was handled
    
    return False  # No curfew violation

def update_year_progress():
    """Update the player's progress through the current school year"""
    # No need for global current_date as we're only reading its value, not modifying it

    # School year starts in April and ends in March
    start_month = 4  # April
    end_month = 3  # March of next year

    current_month = current_date.month
    current_day = current_date.day

    # Calculate year progress as a percentage
    if current_month >= start_month:
        # We're in Apr-Dec of the current year
        months_passed = current_month - start_month
    else:
        # We're in Jan-Mar of the next year
        months_passed = (12 - start_month) + current_month

    # Add fraction of current month (assume 30 days per month for simplicity)
    month_fraction = current_day / 30.0

    # Calculate total progress (12 months = 100%)
    total_progress = ((months_passed + month_fraction) / 12.0) * 100

    # Update player's year progress
    player["year_progress"] = round(total_progress, 1)

    # Check if the school year has completed (around March 20th)
    if current_month == end_month and current_day >= 20:
        handle_year_end()


def handle_year_end():
    """Handle the end of a school year and transition to the next"""
    global subjects, homework

    # Only proceed if we haven't already completed this year
    if player["school_year"] not in player["completed_years"]:
        slow_print(
            f"\n{Fore.CYAN}======================================{Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.YELLOW}CONGRATULATIONS! School Year {player['school_year']} has been completed!{Style.RESET_ALL}"
        )
        slow_print(
            f"{Fore.CYAN}======================================{Style.RESET_ALL}"
        )

        # Calculate final grades and GPA
        calculate_final_grades()

        # Show year-end summary
        show_year_end_summary()

        # Add current year to completed years
        player["completed_years"].append(player["school_year"])

        # Check if player has graduated (completed year 4)
        if player["school_year"] == 4:
            handle_graduation()
            return

        # Advance to next year
        player["school_year"] += 1
        player["year_progress"] = 0

        # Update subjects for the new year
        subjects = get_current_subjects()

        # Reset homework for new subjects
        homework = {}
        for subject_name in subjects:
            homework[subject_name] = False

        # Update electives for new year
        if player["school_year"] > 1:
            choose_new_electives()

        # Special bonuses for upper years
        if player["school_year"] == 3:
            # Third year special opportunities
            offer_internship_opportunities()

        if player["school_year"] == 4:
            # Fourth year career planning
            begin_career_planning()

        slow_print(
            f"\n{Fore.GREEN}Welcome to Year {player['school_year']}!{Style.RESET_ALL}"
        )
        slow_print("Your new courses have been set up. Good luck with your studies!")


def calculate_final_grades():
    """Calculate final grades and GPA for the current school year"""
    # Convert letter grades to GPA points
    grade_points = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "D-": 0.7,
        "F": 0.0,
    }

    # Get the subjects for the current year
    subjects = get_current_subjects()

    total_points = 0
    total_subjects = 0

    for subject_name, grade in player["grades"].items():
        # Only count subjects for the current year
        if subject_name in subjects:
            # Handle both numerical and letter grades
            if isinstance(grade, (int, float)):
                # Convert numerical grade to letter grade
                if grade >= 90:
                    letter_grade = "A"
                elif grade >= 80:
                    letter_grade = "B"
                elif grade >= 70:
                    letter_grade = "C"
                elif grade >= 60:
                    letter_grade = "D"
                else:
                    letter_grade = "F"
                points = grade_points.get(letter_grade, 0)
            else:
                # It's already a letter grade
                # First try the full grade (e.g., "A+")
                # Then fallback to just the letter (e.g., "A")
                points = grade_points.get(grade, grade_points.get(grade[0] if grade else "F", 0))

            total_points += points
            total_subjects += 1

    if total_subjects > 0:
        player["gpa"] = round(total_points / total_subjects, 2)
    else:
        player["gpa"] = 0.0


def show_year_end_summary():
    """Display a summary of the player's achievements for the current school year"""
    slow_print(
        f"\n{Fore.YELLOW}=== Year {player['school_year']} Summary ==={Style.RESET_ALL}"
    )
    slow_print(f"Final GPA: {player['gpa']}")

    # Get the current subjects
    subjects = get_current_subjects()

    # Show final grades
    slow_print("\nFinal Grades:")
    current_year_subjects = [s for s in player["grades"].keys() if s in subjects]
    for subject in current_year_subjects:
        slow_print(f"  {subject}: {player['grades'][subject]}")

    # Show relationship progress
    slow_print("\nRelationships Developed:")
    if relationship:
        for name, points in sorted(
            relationship.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            status = get_relationship_status(points)
            slow_print(f"  {name}: {status} ({points} points)")
    else:
        slow_print("  No significant relationships developed.")

    # Show achievements unlocked this year
    slow_print("\nAchievements Unlocked:")
    if player["achievements"]:
        for achievement in player["achievements"]:
            slow_print(f"  ✓ {achievement}")
    else:
        slow_print("  No achievements unlocked.")

    # Show club positions
    if player["clubs"]:
        slow_print("\nClub Memberships:")
        for club in player["clubs"]:
            position = player["club_positions"].get(club, "Member")
            slow_print(f"  {club}: {position}")

    # Show statistics
    slow_print("\nStatistics:")
    slow_print(f"  Money Earned: ¥{player['money']}")
    slow_print(f"  Reputation with Students: {player['reputation']['students']}")
    slow_print(f"  Reputation with Teachers: {player['reputation']['teachers']}")
    slow_print(f"  Charisma (Social): {player['charisma']['social']}")
    slow_print(f"  Charisma (Academic): {player['charisma']['academic']}")

    # Ask player if they want to continue to the next year
    slow_print(
        f"\n{Fore.GREEN}Ready to advance to Year {player['school_year'] + 1}?{Style.RESET_ALL}"
    )
    try:
        input(
            f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}"
        )  # No need to store the input
    except EOFError:
        print(f"{Fore.RED}Input error encountered. Continuing...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}. Continuing...{Style.RESET_ALL}")


def choose_new_electives():
    """Allow player to choose new electives for the new school year"""
    # Get available electives for the current year
    available_electives = []
    # Get the subjects for the current school year
    all_subjects = get_subjects_for_year(player["school_year"])

    for subject_name, subject_data in all_subjects.items():
        if not subject_data["core"]:
            available_electives.append(subject_name)

    if not available_electives:
        return

    slow_print(
        f"\n{Fore.YELLOW}=== Choose Your Electives for Year {player['school_year']} ==={Style.RESET_ALL}"
    )
    slow_print(
        "As you advance to a new school year, you can choose new elective subjects."
    )

    # Display available electives
    for i, elective in enumerate(available_electives, 1):
        slow_print(f"{i}. {elective}")

    # Let player choose electives
    chosen_electives = []
    num_to_choose = min(2, len(available_electives))

    while len(chosen_electives) < num_to_choose:
        try:
            choice = int(
                input(
                    f"{Fore.CYAN}Select elective {len(chosen_electives)+1}/{num_to_choose} (enter number): {Style.RESET_ALL}"
                )
            )
            if 1 <= choice <= len(available_electives):
                elective = available_electives[choice - 1]
                if elective not in chosen_electives:
                    chosen_electives.append(elective)
                    slow_print(f"You selected {elective}")
                else:
                    slow_print("You've already selected that elective.")
            else:
                slow_print("Invalid choice. Please enter a valid number.")
        except ValueError:
            slow_print("Please enter a number.")
        except EOFError:
            slow_print(
                f"{Fore.RED}Input error encountered. Skipping selection.{Style.RESET_ALL}"
            )
            # Add a random elective if none selected due to error
            if not chosen_electives and available_electives:
                random_elective = random.choice(available_electives)
                chosen_electives.append(random_elective)
                slow_print(
                    f"Automatically selected {random_elective} due to input error."
                )
            break
        except Exception as e:
            slow_print(
                f"{Fore.RED}Error: {str(e)}. Skipping selection.{Style.RESET_ALL}"
            )
            break

    player["electives"] = chosen_electives
    slow_print(
        f"\n{Fore.GREEN}Your electives for Year {player['school_year']} are: {', '.join(chosen_electives)}{Style.RESET_ALL}"
    )


def offer_internship_opportunities():
    """Offer internship opportunities for third-year students"""
    slow_print(f"\n{Fore.YELLOW}=== Internship Opportunities ==={Style.RESET_ALL}")
    slow_print(
        "As a third-year student, you now have access to internship opportunities."
    )
    slow_print(
        "Internships can provide valuable experience, connections, and future job prospects."
    )

    internships = [
        {
            "name": "Tech Company Internship",
            "requirements": {
                "charisma": {"academic": 8},
                "grades": {"Computer Science": "B"},
            },
            "benefits": {"money": 5000, "reputation": 15, "skill": "Programming"},
        },
        {
            "name": "Hospital Volunteer",
            "requirements": {"charisma": {"social": 7}},
            "benefits": {"reputation": 20, "skill": "Medical Knowledge"},
        },
        {
            "name": "Research Assistant",
            "requirements": {"charisma": {"academic": 10}},
            "benefits": {"reputation": 15, "skill": "Research Methodology"},
        },
        {
            "name": "Teaching Assistant",
            "requirements": {"grades": {"average": "B"}},
            "benefits": {"money": 3000, "reputation": 10, "skill": "Teaching"},
        },
        {
            "name": "Business Intern",
            "requirements": {"charisma": {"social": 8, "academic": 5}},
            "benefits": {"money": 8000, "skill": "Business Acumen"},
        },
    ]

    # Show available internships based on player qualifications
    available = []
    for i, internship in enumerate(internships):
        # Check if player meets requirements (simplified check)
        meets_requirements = True
        if "grades" in internship["requirements"]:
            for subject, min_grade in internship["requirements"]["grades"].items():
                if subject == "average":
                    meets_requirements = player["gpa"] >= 3.0  # B average or better
                elif subject in player["grades"]:
                    # For letter grades (A is better than B)
                    if isinstance(player["grades"][subject], str) and isinstance(min_grade, str):
                        meets_requirements = player["grades"][subject][0] <= min_grade[0]
                    # For numerical grades (higher is better)
                    elif isinstance(player["grades"][subject], (int, float)):
                        # Convert min_grade letter to threshold
                        grade_thresholds = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
                        threshold = grade_thresholds.get(min_grade[0], 0)
                        meets_requirements = player["grades"][subject] >= threshold

        if meets_requirements:
            available.append(internship)
            slow_print(f"\n{i+1}. {internship['name']}")
            slow_print(
                f"   Benefits: ¥{internship['benefits'].get('money', 0)}, Reputation +{internship['benefits'].get('reputation', 0)}"
            )
            slow_print(f"   Skill gained: {internship['benefits']['skill']}")

    if not available:
        slow_print(
            "\nUnfortunately, you don't qualify for any internships at this time."
        )
        slow_print(
            "Focus on improving your grades and skills to qualify next semester."
        )
        return

    try:
        choice = int(
            input(
                f"\n{Fore.CYAN}Select an internship to apply for (0 to skip): {Style.RESET_ALL}"
            )
        )
        if 1 <= choice <= len(available):
            selected = available[choice - 1]
            player["internships"].append(selected["name"])

            # Apply benefits
            if "money" in selected["benefits"]:
                player["money"] += selected["benefits"]["money"]
            if "reputation" in selected["benefits"]:
                player["reputation"]["teachers"] += selected["benefits"]["reputation"]

            slow_print(
                f"\n{Fore.GREEN}Congratulations! You've been accepted to the {selected['name']}.{Style.RESET_ALL}"
            )
            slow_print(
                "This will provide valuable experience throughout your third year."
            )
        elif choice == 0:
            slow_print("\nYou decided not to apply for any internships at this time.")
        else:
            slow_print(
                "\nInvalid choice. You can apply for internships later through the career office."
            )
    except ValueError:
        slow_print(
            "\nInvalid input. You can apply for internships later through the career office."
        )
    except EOFError:
        slow_print(
            f"{Fore.RED}Input error encountered. Skipping internship selection.{Style.RESET_ALL}"
        )
    except Exception as e:
        slow_print(
            f"{Fore.RED}Error: {str(e)}. Skipping internship selection.{Style.RESET_ALL}"
        )


def begin_career_planning():
    """Start career planning for fourth-year students"""
    slow_print(f"\n{Fore.YELLOW}=== Career Planning ==={Style.RESET_ALL}")
    slow_print(
        "As a fourth-year student, it's time to start thinking about your future after graduation."
    )
    slow_print(
        "Your academic performance, relationships, and experiences will influence your career options."
    )

    # Career paths based on player's strengths
    careers = [
        {
            "path": "Graduate School",
            "description": "Continue your academic journey with advanced studies",
            "min_gpa": 3.5,
        },
        {
            "path": "Corporate Career",
            "description": "Join a company in your field of study",
            "min_charisma": {"social": 7},
        },
        {
            "path": "Entrepreneurship",
            "description": "Start your own business venture",
            "min_charisma": {"social": 8, "academic": 6},
        },
        {
            "path": "Teaching",
            "description": "Share your knowledge with the next generation",
            "min_reputation": {"teachers": 60},
        },
        {
            "path": "Creative Industry",
            "description": "Pursue a career in arts, design, or media",
            "requirements": {"clubs": ["Art Club", "Music Club", "Drama Club"]},
        },
        {
            "path": "Public Service",
            "description": "Work for the government or non-profit organizations",
            "min_reputation": {"students": 50, "teachers": 50},
        },
    ]

    slow_print(
        "\nBased on your current progress, these career paths could be suitable for you:"
    )

    available_careers = []
    for career in careers:
        eligible = True

        if "min_gpa" in career and player["gpa"] < career["min_gpa"]:
            eligible = False

        if "min_charisma" in career:
            for charisma_type, min_value in career["min_charisma"].items():
                if player["charisma"][charisma_type] < min_value:
                    eligible = False

        if "min_reputation" in career:
            for rep_type, min_value in career["min_reputation"].items():
                if player["reputation"][rep_type] < min_value:
                    eligible = False

        if "requirements" in career and "clubs" in career["requirements"]:
            if not any(
                club in player["clubs"] for club in career["requirements"]["clubs"]
            ):
                eligible = False

        if eligible:
            available_careers.append(career)
            slow_print(f"\n- {career['path']}: {career['description']}")

    if not available_careers:
        slow_print(
            "\nYou should work on improving your skills and relationships to open up more career options."
        )
    else:
        slow_print(
            "\nYour final year will help you prepare for these potential careers."
        )
        slow_print("Work hard to maintain your GPA and build relevant skills!")


def handle_graduation():
    """Handle the player's graduation from school with career paths and epilogue"""
    slow_print(
        f"\n{Fore.CYAN}================================================{Style.RESET_ALL}"
    )
    slow_print(f"{Fore.YELLOW}CONGRATULATIONS ON YOUR GRADUATION!{Style.RESET_ALL}")
    slow_print(
        f"{Fore.CYAN}================================================{Style.RESET_ALL}"
    )

    # Calculate career success based on overall performance
    academic_score = player["gpa"] * 25  # Max 100
    social_score = min(
        100, player["reputation"]["students"] + player["charisma"]["social"] * 5
    )
    teacher_score = min(
        100, player["reputation"]["teachers"] + player["charisma"]["academic"] * 5
    )
    achievement_score = min(100, len(player["achievements"]) * 10)

    # Calculate overall success score (0-100)
    overall_score = (
        academic_score + social_score + teacher_score + achievement_score
    ) / 4

    # Determine graduation honors
    honors = "None"
    if player["gpa"] >= 3.9:
        honors = f"{Fore.MAGENTA}Summa Cum Laude{Style.RESET_ALL}"
    elif player["gpa"] >= 3.7:
        honors = f"{Fore.CYAN}Magna Cum Laude{Style.RESET_ALL}"
    elif player["gpa"] >= 3.5:
        honors = f"{Fore.GREEN}Cum Laude{Style.RESET_ALL}"

    # Determine post-graduation outcome
    if overall_score >= 90:
        outcome = "Outstanding Success"
        description = "You graduated with top honors and immediately received multiple prestigious job offers."
    elif overall_score >= 75:
        outcome = "Great Success"
        description = "Your hard work paid off with excellent job prospects and a bright future ahead."
    elif overall_score >= 60:
        outcome = "Successful"
        description = (
            "You've done well and have good career opportunities available to you."
        )
    elif overall_score >= 45:
        outcome = "Satisfactory"
        description = "You graduated with decent prospects and should find a good job with some effort."
    elif overall_score >= 30:
        outcome = "Mixed Results"
        description = "Your school experience had ups and downs, but you made it through graduation."
    else:
        outcome = "Challenging Start"
        description = (
            "You graduated, but may need to work extra hard to establish your career."
        )

    # Show graduation summary
    slow_print(f"\n{Fore.YELLOW}=== Graduation Summary ==={Style.RESET_ALL}")
    slow_print(f"Final GPA: {player['gpa']}")
    slow_print(f"Graduation Honors: {honors}")
    slow_print(f"Social Reputation: {player['reputation']['students']}")
    slow_print(f"Teacher Reputation: {player['reputation']['teachers']}")
    slow_print(f"Final Balance: ¥{player['money']}")
    slow_print(
        f"Achievements Unlocked: {len(player['achievements'])}/{len(achievements)}"
    )

    # Show graduation outcome
    slow_print(f"\n{Fore.GREEN}Your Graduation Outcome: {outcome}{Style.RESET_ALL}")
    slow_print(description)

    # Show relationships at graduation
    if relationship:
        slow_print("\nLifelong Connections:")
        for name, points in sorted(
            relationship.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            status = get_relationship_status(points)
            slow_print(f"  {name}: {status} ({points} points)")

    # Create list of potential career paths based on player's stats and choices
    career_paths = []

    # Add different career paths based on player's stats
    if player["gpa"] >= 3.7:
        career_paths.append(
            {
                "name": "Graduate School Scholarship",
                "description": "Your exceptional academic performance has earned you a full scholarship to a prestigious graduate program.",
                "outcome": "You'll continue your education and become a respected expert in your field.",
            }
        )

    if player["charisma"]["social"] >= 8:
        career_paths.append(
            {
                "name": "Corporate Management Trainee",
                "description": "A major corporation has offered you a place in their exclusive management training program.",
                "outcome": "You'll rise quickly through the corporate ranks with your excellent people skills.",
            }
        )

    if player["charisma"]["academic"] >= 8:
        career_paths.append(
            {
                "name": "Research Fellowship",
                "description": "Your deep subject knowledge has impressed a research institution, which has offered you a fellowship.",
                "outcome": "You'll contribute to groundbreaking research and academic advancement.",
            }
        )

    if player["reputation"]["teachers"] >= 75:
        career_paths.append(
            {
                "name": "Teaching Position",
                "description": "Your former professors have recommended you for a teaching position at a respected school.",
                "outcome": "You'll inspire the next generation of students with your knowledge and passion.",
            }
        )

    if player["reputation"]["students"] >= 75:
        career_paths.append(
            {
                "name": "Community Leadership",
                "description": "Your popularity and leadership skills have opened doors to community organizing and political opportunities.",
                "outcome": "You'll make a significant impact on your community through leadership and advocacy.",
            }
        )

    if "internships" in player and len(player["internships"]) > 0:
        career_paths.append(
            {
                "name": "Direct Job Offer",
                "description": f"Your internship at {player['internships'][-1]} impressed your supervisors, who have offered you a full-time position.",
                "outcome": "You'll start your career with valuable experience and connections already in place.",
            }
        )

    if player["money"] >= 10000:
        career_paths.append(
            {
                "name": "Entrepreneurship",
                "description": "With your savings and business acumen, you're well-positioned to start your own business.",
                "outcome": "You'll build your own company and create opportunities for yourself and others (and don't ask me how the hell you're going to start that, idk lol).",
            }
        )

    # If romantic relationship is serious, add this path
    if player["romantic_interest"] and player["romance_stage"] >= 4:
        career_paths.append(
            {
                "name": "Family Focus",
                "description": f"Your relationship with {player['romantic_interest']} has become the center of your life plans.",
                "outcome": "You'll build a fulfilling life together, supporting each other's dreams and goals.",
            }
        )

    # If no special paths are available, add these default options
    if not career_paths:
        career_paths = [
            {
                "name": "Entry-Level Position",
                "description": "You've secured a solid entry-level position in your field of study.",
                "outcome": "You'll gain valuable experience and have room to grow in your career.",
            },
            {
                "name": "Freelance Work",
                "description": "You've decided to take on freelance projects and build your portfolio.",
                "outcome": "You'll enjoy the flexibility of freelance work while developing your skills and client base.",
            },
            {
                "name": "Travel Year",
                "description": "You've decided to take a year off to travel and explore before settling into a career.",
                "outcome": "You'll gain valuable life experience and perspective that will shape your future choices.",
            },
        ]

    # Present career choices
    slow_print(f"\n{Fore.CYAN}====== YOUR FUTURE AWAITS ======{Style.RESET_ALL}")
    slow_print(
        "Based on your accomplishments, these career paths are available to you:"
    )

    for i, path in enumerate(career_paths, 1):
        slow_print(f"\n{i}. {Fore.GREEN}{path['name']}{Style.RESET_ALL}")
        slow_print(f"   {path['description']}")

    # Make sure there's at least one career path available
    if not career_paths:
        # If somehow no career paths are available, create a default one
        default_path = {
            "name": "Entry-Level Position",
            "description": "You've secured a solid entry-level position in your field of study.",
            "outcome": "You'll gain valuable experience and have room to grow in your career.",
        }
        career_paths.append(default_path)

    # Default chosen path (used if any error occurs)
    chosen_path = career_paths[0]

    # Let player choose their future
    attempt_count = 0
    max_attempts = 3
    while attempt_count < max_attempts:
        try:
            choice = input(
                f"\n{Fore.YELLOW}Which path will you choose for your future? (1-{len(career_paths)}): {Style.RESET_ALL}"
            )
            choice_num = int(choice)
            if 1 <= choice_num <= len(career_paths):
                chosen_path = career_paths[choice_num - 1]
                break
            else:
                slow_print("Please enter a valid choice.")
            attempt_count += 1
        except ValueError:
            slow_print("Please enter a number.")
            attempt_count += 1
        except EOFError:
            slow_print(
                f"{Fore.RED}Input error encountered. Selecting a random career path.{Style.RESET_ALL}"
            )
            chosen_path = random.choice(career_paths)
            break
        except Exception as e:
            slow_print(
                f"{Fore.RED}Error: {str(e)}. Selecting a random career path.{Style.RESET_ALL}"
            )
            chosen_path = random.choice(career_paths)
            break

    # If all attempts failed, choose a random path
    if attempt_count >= max_attempts:
        slow_print(
            f"{Fore.RED}Too many invalid choices. Selecting a random career path.{Style.RESET_ALL}"
        )
        chosen_path = random.choice(career_paths)

    # Show epilogue
    slow_print(f"\n{Fore.MAGENTA}====== EPILOGUE ======{Style.RESET_ALL}")
    slow_print(f"You chose: {Fore.GREEN}{chosen_path['name']}{Style.RESET_ALL}")
    slow_print(f"\n{chosen_path['outcome']}")

    # Generate a personalized future story based on player's choices and stats
    slow_print("\nFive years after graduation...")

    # Different epilogue scenarios based on career path
    if "Graduate School" in chosen_path["name"]:
        slow_print(
            "You completed your advanced degree with distinction. Your research has been published in prestigious journals, and you've received offers from multiple institutions."
        )
        if player["charisma"]["social"] >= 5:
            slow_print(
                "You've also maintained your social connections from college, creating a supportive network of fellow academics."
            )

    elif "Corporate" in chosen_path["name"]:
        slow_print(
            "You've been promoted twice in five years, managing your own team and impressing executives with your leadership skills."
        )
        if player["gpa"] >= 3.0:
            slow_print(
                "Your solid academic foundation has helped you master complex business challenges with ease."
            )

    elif "Research" in chosen_path["name"]:
        slow_print(
            "Your research has contributed to important advancements in your field. Colleagues respect your innovative approach and dedication."
        )
        if "internships" in player:
            slow_print(
                "The connections you made during your internships have opened doors to collaborative projects with industry leaders."
            )

    elif "Teaching" in chosen_path["name"]:
        slow_print(
            "Your students consistently rate you as one of their favorite teachers. Your unique teaching style has made complex subjects accessible to many."
        )
        if player["reputation"]["students"] >= 50:
            slow_print(
                "The social skills you developed in college have made you particularly effective at connecting with and motivating your students."
            )

    elif "Community" in chosen_path["name"]:
        slow_print(
            "You've become a respected voice in your community, advocating for important changes and bringing people together around common goals."
        )
        if player["money"] >= 5000:
            slow_print(
                "Your financial stability has allowed you to dedicate more time to volunteer work and community projects."
            )

    elif "Job Offer" in chosen_path["name"]:
        slow_print(
            "You've thrived in your role, earning the respect of colleagues and superiors alike. Your prior internship experience gave you a valuable head start."
        )
        if player["charisma"]["academic"] >= 6:
            slow_print(
                "Your strong academic foundation has helped you approach problems with depth and nuance that impresses everyone around you."
            )

    elif "Entrepreneurship" in chosen_path["name"]:
        slow_print(
            "Your business has grown steadily under your leadership. The skills you developed in college have served you well as an entrepreneur."
        )
        if player["reputation"]["teachers"] >= 60:
            slow_print(
                "You've maintained relationships with your former professors, who have provided valuable advice and connections for your business."
            )

    elif "Family" in chosen_path["name"]:
        slow_print(
            f"Your relationship with {player['romantic_interest']} has flourished. You've created a supportive partnership that brings out the best in both of you."
        )
        if player["charisma"]["social"] >= 7:
            slow_print(
                "Your social skills have helped you build a wonderful community of friends around your family."
            )

    else:
        slow_print(
            "The past five years have been full of growth and learning. Your college experience provided a strong foundation for navigating adult life."
        )
        slow_print(
            "While there have been challenges along the way, you've faced them with the resilience and skills you developed during your campus years."
        )

    # Connect epilogue to college relationships
    if relationship:
        top_relationship = max(relationship.items(), key=lambda x: x[1])
        if top_relationship[1] >= 75:
            slow_print(
                f"\nYou've remained close with {top_relationship[0]} all these years. Your friendship has been one of the most valuable things you took from college."
            )

    # Final message
    slow_print(
        f"\n{Fore.YELLOW}As you reflect on your college years, you realize how those experiences shaped who you've become.{Style.RESET_ALL}"
    )
    slow_print(
        f"{Fore.YELLOW}The lessons learned, friendships formed, and challenges overcome during your campus life continue to influence your journey.{Style.RESET_ALL}"
    )

    # Unlock achievement for completing the game
    if "Graduate" not in player["achievements"]:
        player["achievements"].append("Graduate")
        slow_print(f"\n{Fore.YELLOW}Achievement Unlocked: Graduate{Style.RESET_ALL}")

    # Specialized achievement based on outcome
    if overall_score >= 90 and "Valedictorian" not in player["achievements"]:
        player["achievements"].append("Valedictorian")
        slow_print(
            f"\n{Fore.YELLOW}Achievement Unlocked: Valedictorian{Style.RESET_ALL}"
        )

    if "Family" in chosen_path["name"] and "Soul Mate" not in player["achievements"]:
        player["achievements"].append("Soul Mate")
        slow_print(f"\n{Fore.YELLOW}Achievement Unlocked: Soul Mate{Style.RESET_ALL}")

    if (
        "Entrepreneurship" in chosen_path["name"]
        and "Business Mogul" not in player["achievements"]
    ):
        player["achievements"].append("Business Mogul")
        slow_print(
            f"\n{Fore.YELLOW}Achievement Unlocked: Business Mogul{Style.RESET_ALL}"
        )

    # Unlock template password after completing a full game
    slow_print(
        f"\n{Fore.MAGENTA}Special unlocked: You can now access advanced Student Templates!{Style.RESET_ALL}"
    )
    slow_print(f"{Fore.YELLOW}Secret password: GRADUATE{Style.RESET_ALL}")
    slow_print(
        "Use this password in the main menu for special options in your next game!"
    )

    # Final thank you message
    slow_print(f"\n{Fore.CYAN}Thank you for playing Campus Life RPG!{Style.RESET_ALL}")
    slow_print(
        "Your journey through school has concluded, but your life's adventure is just beginning."
    )

    # Return to main menu
    try:
        input(
            f"\n{Fore.CYAN}Press Enter to return to the main menu...{Style.RESET_ALL}"
        )
    except EOFError:
        print(f"{Fore.RED}Input error encountered. Continuing...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}. Continuing...{Style.RESET_ALL}")
    show_main_menu()


def advance_day():
    global current_date, ticks
    # Need globals for current_date and ticks as we're reassigning them
    # No need for homework global as we're not reassigning it
    current_date += timedelta(days=1)
    ticks = 0

    # If player is grounded, reduce grounding days
    if player.get("grounded", 0) > 0:
        player["grounded"] -= 1
        if player["grounded"] == 0:
            slow_print(f"{Fore.GREEN}You are no longer grounded! You can leave home now.{Style.RESET_ALL}")
        else:
            slow_print(f"{Fore.YELLOW}You are still grounded for {player['grounded']} more days.{Style.RESET_ALL}")

    # Restore some energy after sleep
    player["energy"] = min(player["energy"] + 50, 100)
    player["hunger"] = max(player["hunger"] - 20, 0)

    # Check for special events and festivals
    check_for_special_events()

    # Reduce stress naturally
    player["stress"] = max(0, player["stress"] - 5)

    # Update mental health
    update_mental_health()

    # Update rumors - spread and potentially create new ones
    update_rumors()

    # Random chance for ex-partner events
    if player["ex_partners"] and random.random() < 0.1:  # 10% daily chance
        process_ex_partner_event()

    # Update year progress
    update_year_progress()

    # Handle holiday accommodation switching (dorm to home and back)
    handle_holiday_accommodation()

    if not is_weekend() and not is_holiday():
        # Check for monthly exam
        check_monthly_exam()

        # Check for missed homework sanctions
        for subject, done in list(homework.items()):
            if not done:
                apply_sanction("missed_homework")
                break  # Apply sanction once per day if any homework missed

        # Randomly assign homework for subjects
        for subject in player["electives"]:
            if (
                subject in subjects
                and random.random() < subjects[subject]["homework_freq"]
            ):
                homework[subject] = False

        # Random events
        if random.random() < 0.2:  # 20% chance
            random_school_event()

        # Random friendship events
        if random.random() < 0.15:  # 15% chance
            random_friendship_event()

        # Check for club meetings
        check_club_meetings()

    # Status message for the new day
    day_type = (
        "Weekend" if is_weekend() else "Holiday" if is_holiday() else "School Day"
    )
    slow_print(
        f"\n{Fore.CYAN}=== {current_date.strftime('%A, %B %d, %Y')} | {day_type} ==={Style.RESET_ALL}"
    )
    slow_print(f"Year {player['school_year']} Progress: {player['year_progress']}%")

    # Check for achievements
    check_achievements()

    # Hunger and energy warnings
    if player["hunger"] < 30:
        slow_print(
            f"{Fore.RED}You're very hungry! Find something to eat soon.{Style.RESET_ALL}"
        )
    if player["energy"] < 30:
        slow_print(
            f"{Fore.RED}You're exhausted! You should rest soon.{Style.RESET_ALL}"
        )
    if player["stress"] > 70:
        slow_print(
            f"{Fore.RED}You're feeling very stressed! Take some time to relax.{Style.RESET_ALL}"
        )


def random_school_event():
    # Regular school events
    regular_events = [
        "You forgot your homework!",
        "Someone shared their lunch with you",
        "Pop quiz surprise!",
        "School festival preparation",
        "Club recruitment day",
        "A teacher gives an inspiring lecture",
        "You find a quiet spot to read during lunch",
        "Your friend tells you a funny joke",
        "You overhear some interesting gossip",
    ]

    # Bullying events with severity levels (1-5)
    bullying_events = [
        {
            "text": "Someone threw a paper airplane with a rude message at you.",
            "severity": 1,
        },
        {"text": "A classmate kept kicking the back of your chair.", "severity": 1},
        {
            "text": "Someone put an eraser on your chair when you stood up.",
            "severity": 1,
        },
        {
            "text": "A group of students was whispering and laughing when you walked past.",
            "severity": 2,
        },
        {"text": "Someone hid your textbook as a prank.", "severity": 2},
        {
            "text": "You found mean comments about you written in the bathroom.",
            "severity": 3,
        },
        {"text": "Someone spread a false rumor about you.", "severity": 4},
        {"text": "Your personal belongings were damaged.", "severity": 4},
        {
            "text": "A group of students cornered you and mocked you relentlessly.",
            "severity": 5,
        },
    ]

    # Mental health support events
    support_events = [
        "A teacher notices you seem down and checks in with you.",
        "A friendly student invites you to join their study group.",
        "The school counselor is offering free mental health check-ins.",
        "You discover a support group for students with similar challenges.",
        "A kind note of encouragement was left on your desk.",
    ]

    # Determine if a bullying event should occur (15% chance if enabled)
    if game_settings["allow_bullying"] and random.random() < 0.15:
        bullying_event = random.choice(bullying_events)
        event_text = bullying_event["text"]
        severity = bullying_event["severity"]

        slow_print(
            "\n{0}Event:{1} {2}".format(
                Fore.YELLOW, Style.RESET_ALL, filter_text(event_text, ["bullying"])
            )
        )

        # Process the bullying event with its severity
        process_bullying_event(severity)

        # Small chance (20%) of a support event following bullying
        if random.random() < 0.20:
            support_event = random.choice(support_events)
            slow_print(
                "\n{0}Later:{1} {2}".format(Fore.CYAN, Style.RESET_ALL, support_event)
            )

            # Support events reduce the negative impact
            mental_health = player["mental_health"]
            mental_health["depression"] = max(0, mental_health["depression"] - 5)
            mental_health["anxiety"] = max(0, mental_health["anxiety"] - 5)
            mental_health["self_esteem"] = min(100, mental_health["self_esteem"] + 3)
            mental_health["support_network"] = min(
                100, mental_health["support_network"] + 5
            )
    else:
        # Regular event
        event = random.choice(regular_events)
        slow_print("\n{0}Event:{1} {2}".format(Fore.YELLOW, Style.RESET_ALL, event))

        if event == "You forgot your homework!":
            # Get current subjects - this already returns a list
            subject_list = get_current_subjects()
            if subject_list:
                # Choose a random subject
                subject = random.choice(subject_list)
                if subject in homework and homework[subject]:
                    slow_print(
                        "But wait! You actually did complete your homework for {}!".format(
                            subject
                        )
                    )
                    slow_print("The teacher is impressed by your responsibility.")
                    increase_reputation("teachers", 2)
                else:
                    slow_print("Your teacher in {} is disappointed.".format(subject))
                    increase_stress(3)
                    # Use increase_reputation with negative value instead of decrease_reputation
                    increase_reputation("teachers", -1)
        elif event == "Someone shared their lunch with you":
            slow_print("You feel less hungry and happier!")
            decrease_hunger(20)
            decrease_stress(5)

            # Small chance to build relationship with a random student
            if random.random() < 0.3:
                # Get random student
                student = random.choice(students)
                name = student["name"]
                improve_relationship(name, 5)
                slow_print(
                    "It was {} who shared with you. Your relationship improved!".format(
                        name
                    )
                )
        elif event == "Pop quiz surprise!":
            subject_list = get_current_subjects()
            if subject_list:
                subject = random.choice(subject_list)
                slow_print("The quiz is in {}!".format(subject))

                # Check homework status to determine outcome
                if subject in homework and homework[subject]:
                    slow_print("Thanks to your completed homework, you feel prepared!")
                    improve_grade = (
                        random.random() < 0.7
                    )  # 70% chance of grade improvement
                    if improve_grade and subject in player["grades"]:
                        current_grade = player["grades"][subject]
                        if current_grade != "A":  # Can't improve beyond A
                            # Calculate new improved grade
                            grade_values = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}
                            rev_grade_values = {0: "A", 1: "B", 2: "C", 3: "D", 4: "F"}
                            current_value = grade_values[current_grade]
                            new_value = max(
                                0, current_value - 1
                            )  # Improve by one level
                            new_grade = rev_grade_values[new_value]
                            player["grades"][subject] = new_grade
                            slow_print(
                                "Your grade in {} improved to {}!".format(
                                    subject, new_grade
                                )
                            )
                else:
                    slow_print("You feel unprepared for this quiz...")
                    increase_stress(8)
                    worsen_grade = random.random() < 0.5  # 50% chance of grade decrease
                    if worsen_grade and subject in player["grades"]:
                        current_grade = player["grades"][subject]
                        if current_grade != "F":  # Can't get worse than F
                            # Calculate new worsened grade
                            grade_values = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}
                            rev_grade_values = {0: "A", 1: "B", 2: "C", 3: "D", 4: "F"}
                            current_value = grade_values[current_grade]
                            new_value = min(4, current_value + 1)  # Worsen by one level
                            new_grade = rev_grade_values[new_value]
                            player["grades"][subject] = new_grade
                            slow_print(
                                "Your grade in {} dropped to {}!".format(
                                    subject, new_grade
                                )
                            )
        elif event == "School festival preparation":
            slow_print("You help set up decorations for the upcoming festival.")
            increase_reputation("students", 2)
            decrease_energy(10)
            player["festival_points"] += 5
            slow_print("Festival preparation points earned!")
        elif event == "Club recruitment day":
            slow_print("You receive flyers from various clubs.")
            show_clubs()
        elif event == "A teacher gives an inspiring lecture":
            slow_print("You feel motivated and your academic charisma increases!")
            player["charisma"]["academic"] += 1
            decrease_stress(5)
        elif event == "You find a quiet spot to read during lunch":
            slow_print("The peaceful moment helps you relax and focus.")
            decrease_stress(7)
            player["mental_health"]["anxiety"] = max(
                0, player["mental_health"]["anxiety"] - 3
            )
        elif event == "Your friend tells you a funny joke":
            slow_print("You laugh and feel your mood improving.")
            decrease_stress(5)
            player["mental_health"]["happiness"] = min(
                100, player["mental_health"]["happiness"] + 5
            )

        elif event == "You overhear some interesting gossip":
            # Initialize rumors system if it doesn't exist
            if "rumors" not in player:
                player["rumors"] = []

            # Generate a new rumor
            generate_random_rumor()

            if player["rumors"]:
                # Get the most recent rumor
                latest_rumor = player["rumors"][-1]
                slow_print(f"You overhear that {latest_rumor['content']}")

                # Option to spread the rumor
                spread_choice = input("Spread this rumor? (y/n): ").lower()

                if spread_choice == "y":
                    # Spreading increases the rumor's reach
                    latest_rumor["spread_level"] += 2

                    # Possible consequences of spreading rumors
                    if random.random() < 0.2:  # 20% chance of negative consequence
                        slow_print(
                            f"{Fore.RED}Someone overheard you spreading the rumor and seems upset.{Style.RESET_ALL}"
                        )
                        increase_reputation("students", -3)
                        increase_stress(5)
                    else:
                        slow_print("Others seemed interested in the gossip you shared.")
                        player["charisma"]["social"] += 1

    update_ranks()


def show_me():
    print(f"\n{Fore.CYAN}=== {player['name']}'s Profile ==={Style.RESET_ALL}")
    print(
        f"Current Date: {current_date.strftime('%Y-%m-%d')} ({'Weekend' if is_weekend() else 'Holiday' if is_holiday() else 'Weekday'})"
    )

    # School Year Information
    year_names = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
    year_name = year_names.get(player["school_year"], f"Year {player['school_year']}")
    print(
        f"{Fore.MAGENTA}School Year: {year_name} (Year {player['school_year']}){Style.RESET_ALL}"
    )
    print(f"Year Progress: {player['year_progress']}%")
    print(f"GPA: {player['gpa']}")

    # Basic Stats
    print(f"Money: ¥{player['money']}")
    print(f"Energy: {player['energy']}/100")
    print(f"Hunger: {player['hunger']}/100")
    print(f"Stress: {player['stress']}/100")
    print(f"Health: {player['health']}/100 ({get_health_indicator()})")

    # Clothing information
    current_clothing = player["clothing"]["wearing"]
    if current_clothing:
        clothing_type = CLOTHING_ITEMS[current_clothing]["type"].capitalize()
        print(
            f"\n{Fore.CYAN}Currently Wearing:{Style.RESET_ALL} {current_clothing} ({clothing_type})"
        )
    else:
        print(f"\n{Fore.RED}Warning: You aren't wearing any clothes!{Style.RESET_ALL}")

    # Show owned clothing items
    if player["clothing"]["owned"]:
        print(f"\n{Fore.CYAN}Owned Clothing:{Style.RESET_ALL}")
        for i, clothing in enumerate(player["clothing"]["owned"], 1):
            clothing_type = CLOTHING_ITEMS[clothing]["type"].capitalize()
            print(f"  {i}. {clothing} ({clothing_type})")
    else:
        print("\nYou don't own any clothing. (This shouldn't happen!)")

    # Academic Information
    print(f"\n{Fore.YELLOW}Current Subjects:{Style.RESET_ALL}")

    # Get subject data and filter for current year
    subjects_data = get_subjects_for_year(player["school_year"])
    current_subjects = get_current_subjects()

    # Core subjects
    core_subjects = []
    elective_subjects = []

    # Process each subject
    for subject in current_subjects:
        if subject in subjects_data:
            subject_data = subjects_data[subject]
            if subject_data.get("core", False):
                core_subjects.append(subject)
            elif subject in player.get("electives", []):
                elective_subjects.append(subject)

    print(f"{Fore.CYAN}Core Subjects:{Style.RESET_ALL}")
    for subject in core_subjects:
        grade = player["grades"].get(subject, "N/A")
        print(f"  {subject}: {grade}")

    print(f"\n{Fore.CYAN}Elective Subjects:{Style.RESET_ALL}")
    for subject in elective_subjects:
        grade = player["grades"].get(subject, "N/A")
        print(f"  {subject}: {grade}")

    # Completed years
    if player.get("completed_years", []):
        completed_years = ", ".join(str(year) for year in player.get("completed_years", []))
        print(f"\n{Fore.YELLOW}Completed Years: {completed_years}{Style.RESET_ALL}")

    # Reputation and Social Stats
    print(f"\n{Fore.YELLOW}Reputation:{Style.RESET_ALL}")
    # Safely access rank with default value if key doesn't exist
    student_rank = player.get('rank', {}).get('students', 'Unknown')
    teacher_rank = player.get('rank', {}).get('teachers', 'Unknown')
    
    print(
        f"  Among Students: {player['reputation']['students']} ({student_rank})"
    )
    print(
        f"  Among Teachers: {player['reputation']['teachers']} ({teacher_rank})"
    )

    print(f"\n{Fore.YELLOW}Charisma:{Style.RESET_ALL}")
    print(f"  Social: {player['charisma']['social']}")
    print(f"  Academic: {player['charisma']['academic']}")

    # PE Stats
    print(f"\n{Fore.YELLOW}Physical Education Stats:{Style.RESET_ALL}")
    # Safely access pe_stats with a default empty dictionary if missing
    pe_stats = player.get("pe_stats", {})
    if pe_stats:
        for stat, value in pe_stats.items():
            print(f"  {stat.capitalize()}: {value}")
    else:
        print("  No PE stats available yet.")

    # Clubs
    if player["clubs"]:
        print(f"\n{Fore.YELLOW}Clubs:{Style.RESET_ALL}")
        for club in player["clubs"]:
            position = player["club_positions"].get(club, "Member")
            print(f"  {club} - {position}")

    # Internships
    if player.get("internships", []):
        print(f"\n{Fore.YELLOW}Internships:{Style.RESET_ALL}")
        for internship in player.get("internships", []):
            print(f"  • {internship}")

    # Romance
    if player["romantic_interest"]:
        print(
            f"\n{Fore.MAGENTA}Romantic Interest: {player['romantic_interest']}{Style.RESET_ALL}"
        )
        if player["romantic_interest"] in relationship:
            stage = player["romance_stage"]
            stage_name = ROMANCE_STAGES[stage]["name"]
            print(f"  Relationship Stage: {stage_name} (Stage {stage})")
            print(
                f"  Romance Points: {player['romance_points']}/{ROMANCE_STAGES[min(stage+1, max(ROMANCE_STAGES.keys()))]['req']}"
            )

    # Achievements
    if player["achievements"]:
        print(
            f"\n{Fore.YELLOW}Achievements Unlocked ({len(player['achievements'])}/{len(achievements)}){Style.RESET_ALL}"
        )
        for achievement in player["achievements"]:
            print(f"  ✓ {achievement}")

    # Jobs
    if player.get("part_time_job"):
        print(
            f"\n{Fore.YELLOW}Part-time Job:{Style.RESET_ALL} {player.get('part_time_job')}"
        )

    # Quests
    if player["quests"]:
        print(f"\n{Fore.YELLOW}Active Quests:{Style.RESET_ALL}")
        for quest_id in player["quests"]:
            for quest in quests:
                if quest["id"] == quest_id and not quest["completed"]:
                    print(f"  • {quest['description']}")
                    print(f"    Objective: {quest['objective']}")
                    print(f"    Reward: ¥{quest['reward']}")

    # Homework
    if homework:
        print(f"\n{Fore.YELLOW}Pending Homework:{Style.RESET_ALL}")
        for subject, done in homework.items():
            status = (
                f"{Fore.GREEN}✓ Done{Style.RESET_ALL}"
                if done
                else f"{Fore.RED}✗ Not Done{Style.RESET_ALL}"
            )
            print(f"  {subject}: {status}")


def work_part_time(job_name):
    global ticks
    if job_name in jobs:
        job = jobs[job_name]
        player["money"] += job["pay"]
        if "charisma_gain" in job:
            player["charisma"]["social"] += job["charisma_gain"]
        if "academic_gain" in job:
            player["charisma"]["academic"] += job["academic_gain"]
        slow_print(f"You worked at {job_name} and earned ¥{job['pay']}!")
        ticks += job["time"] * 10  # Each hour is 10 ticks
        if ticks >= MAX_TICKS_PER_DAY:
            slow_print("You are very tired and need to sleep.")
        else:
            slow_print(f"Time passed: {ticks} ticks.")
    else:
        print("That job is not available.")


# Family member generation
def generate_family_members():
    """Generate randomized family members for the player"""
    family = {"parents": [], "siblings": []}

    family_relationship = {}

    # Generate 1-2 parents
    num_parents = random.randint(1, 2)

    last_names = [
        "Tanaka",
        "Yamamoto",
        "Sato",
        "Suzuki",
        "Watanabe",
        "Ito",
        "Nakamura",
        "Kobayashi",
        "Takahashi",
        "Kato",
        "Yoshida",
        "Sasaki",
        "Yamaguchi",
        "Matsumoto",
        "Inoue",
    ]

    # Use player's last name if available, or randomly select one
    player_name_parts = player["name"].split()
    if len(player_name_parts) > 1:
        family_last_name = player_name_parts[-1]
    else:
        family_last_name = random.choice(last_names)

    parent_personalities = [
        "caring",
        "strict",
        "relaxed",
        "ambitious",
        "traditional",
        "modern",
        "protective",
        "wise",
    ]
    parent_occupations = [
        "teacher",
        "doctor",
        "office worker",
        "business owner",
        "chef",
        "artist",
        "engineer",
        "lawyer",
        "police officer",
        "writer",
        "scientist",
        "store manager",
    ]

    mother_first_names = [
        "Akiko",
        "Haruka",
        "Yui",
        "Emi",
        "Sakura",
        "Misaki",
        "Hana",
        "Aiko",
        "Yumiko",
        "Naomi",
    ]
    father_first_names = [
        "Kenji",
        "Hiroshi",
        "Takashi",
        "Akira",
        "Yuki",
        "Daichi",
        "Kazuki",
        "Satoshi",
        "Ryo",
        "Taro",
    ]

    # Generate mother (if needed)
    if num_parents > 0:
        mom_name = f"{random.choice(mother_first_names)} {family_last_name}"
        mom_personality = random.choice(parent_personalities)
        mom_occupation = random.choice(parent_occupations)

        family["parents"].append(
            {
                "name": mom_name,
                "relation": "Mother",
                "personality": mom_personality,
                "occupation": mom_occupation,
            }
        )

        # Initial relationship value with mother
        family_relationship[mom_name] = random.randint(50, 80)

    # Generate father (if two parents)
    if num_parents > 1:
        dad_name = f"{random.choice(father_first_names)} {family_last_name}"
        dad_personality = random.choice(parent_personalities)
        dad_occupation = random.choice(parent_occupations)

        family["parents"].append(
            {
                "name": dad_name,
                "relation": "Father",
                "personality": dad_personality,
                "occupation": dad_occupation,
            }
        )

        # Initial relationship value with father
        family_relationship[dad_name] = random.randint(40, 75)

    # Decide if player has siblings (0-2)
    num_siblings = random.randint(0, 2)

    sibling_first_names_male = [
        "Sota",
        "Hayato",
        "Ryota",
        "Haruto",
        "Yuto",
        "Kota",
        "Sora",
        "Minato",
        "Ren",
        "Kaito",
    ]
    sibling_first_names_female = [
        "Yuna",
        "Hinata",
        "Hina",
        "Koharu",
        "Mei",
        "Rin",
        "Miyu",
        "Aoi",
        "Ichika",
        "Sana",
    ]

    sibling_personalities = [
        "friendly",
        "competitive",
        "nerdy",
        "athletic",
        "artistic",
        "shy",
        "outgoing",
        "rebellious",
        "studious",
    ]

    # Generate siblings
    for _ in range(num_siblings):
        # Determine gender
        sibling_gender = random.choice(["M", "F"])

        # Determine age (younger, older, or twin)
        has_twin = random.random() < 0.15  # 15% chance for a twin
        
        if has_twin:
            age_diff = 0  # Same age = twin
        else:
            age_diff = random.randint(-5, 5)
            if age_diff == 0:  # Avoid same age unless it's a twin
                age_diff = random.choice([-1, 1])

        if age_diff == 0:
            age_status = "twin"
        else:
            age_status = "older" if age_diff < 0 else "younger"

        # Choose name based on gender
        if sibling_gender == "M":
            sibling_name = (
                f"{random.choice(sibling_first_names_male)} {family_last_name}"
            )
            relation = f"{age_status} brother"
        else:
            sibling_name = (
                f"{random.choice(sibling_first_names_female)} {family_last_name}"
            )
            relation = f"{age_status} sister"

        # Determine personality
        sibling_personality = random.choice(sibling_personalities)

        family["siblings"].append(
            {
                "name": sibling_name,
                "relation": relation,
                "personality": sibling_personality,
                "age_difference": abs(age_diff),
            }
        )

        # Initial relationship value with sibling
        family_relationship[sibling_name] = random.randint(30, 70)

    return family, family_relationship


# Neurodiversity info dictionary with traits and their properties
NEURODIVERSITY_TRAITS = {
    "dyslexia": {
        "description": "A learning disorder that involves difficulty reading",
        "academic_impact": -10,  # Negative impact on academic performance
        "strengths": ["creativity", "visual thinking", "problem-solving"],
        "accommodations": ["extended test time", "audio textbooks"],
    },
    "adhd": {
        "description": "Attention-deficit/hyperactivity disorder affecting focus and behavior",
        "academic_impact": -5,  # Slight negative impact on academic performance
        "energy_impact": 10,  # Higher energy levels
        "strengths": ["hyperfocus", "creativity", "energetic", "spontaneity"],
        "accommodations": [
            "structured environment",
            "frequent breaks",
            "note-taking assistance",
        ],
    },
    "autism": {
        "description": "A developmental disorder characterized by difficulties with social interaction and communication",
        "academic_impact": 5,  # Can have positive impact on specific subjects
        "social_impact": -10,  # Negative impact on social interactions
        "strengths": [
            "pattern recognition",
            "detailed memory",
            "specialized knowledge",
            "honesty",
        ],
        "accommodations": [
            "sensory accommodations",
            "clear instructions",
            "social skills support",
        ],
    },
    "anxiety_disorder": {
        "description": "Excessive worry that affects daily activities",
        "stress_impact": 15,  # Higher baseline stress
        "social_impact": -5,  # Slight negative impact on social interactions
        "strengths": ["empathy", "conscientiousness", "preparation"],
        "accommodations": [
            "quiet test environment",
            "alternative presentations",
            "counseling support",
        ],
    },
    "depression": {
        "description": "A mood disorder causing persistent feelings of sadness and loss of interest",
        "energy_impact": -10,  # Lower energy levels
        "happiness_impact": -15,  # Lower baseline happiness
        "strengths": ["empathy", "creative insights", "resilience development"],
        "accommodations": [
            "flexible deadlines",
            "counseling support",
            "absence accommodations",
        ],
    },
}

# Ex-partner status types
EX_PARTNER_STATUSES = {
    "moved_on": {
        "description": "Has moved on and is in a new relationship",
        "reconciliation_chance": 0.02,  # 2% chance of wanting to reconcile
        "yandere_chance": 0.01,  # 1% chance of becoming yandere
        "friendship_chance": 0.40,  # 40% chance of remaining friends
        "events": [
            "is now dating someone else but smiles at you in the hallway.",
            "mentions your name to mutual friends in a positive way.",
            "invites you to a group social event.",
        ],
    },
    "still_interested": {
        "description": "Still has feelings for you",
        "reconciliation_chance": 0.12,  # 12% chance of wanting to reconcile
        "yandere_chance": 0.03,  # 3% chance of becoming yandere
        "friendship_chance": 0.35,  # 35% chance of remaining friends
        "events": [
            "sends you a text asking how you've been.",
            "tries to sit near you in class.",
            "asks mutual friends about what you've been up to.",
            "gives you a meaningful look across the cafeteria.",
        ],
    },
    "angry": {
        "description": "Holds a grudge against you",
        "reconciliation_chance": 0.04,  # 4% chance of wanting to reconcile
        "yandere_chance": 0.06,  # 6% chance of becoming yandere
        "friendship_chance": 0.15,  # 15% chance of remaining friends
        "events": [
            "walks the other way when they see you coming.",
            "tells unflattering stories about you to others.",
            "posts cryptic social media messages that might be about you.",
            "gives you an icy stare when you make eye contact.",
        ],
    },
    "yandere": {
        "description": "Has developed an unhealthy obsession with you",
        "reconciliation_chance": 0.20,  # 20% "chance" of wanting to reconcile (obsession)
        "stalking_chance": 0.65,  # 65% chance of stalking behaviors
        "dangerous_chance": 0.25,  # 25% chance of dangerous behaviors
        "events": [
            "somehow appears wherever you go.",
            "has been asking everyone about your daily schedule.",
            "leaves gifts in unexpected places for you to find.",
            "watches you from a distance with an intense stare.",
            "has created a shrine dedicated to you in their room.",
        ],
    },
}

# Modified setup_game function
def setup_game(non_interactive=False):
    # Only need global for _non_interactive as we're reassigning it
    # No need for player, subjects, homework, birthdays globals as we're only modifying their contents
    global _non_interactive
    _non_interactive = non_interactive

    slow_print(f"{Fore.CYAN}Welcome to {Fore.WHITE}{TITLE}{Fore.CYAN}!{Style.RESET_ALL}")
    
    # Check if we're in non-interactive mode
    if non_interactive:
        # Default values for non-interactive environments (like Replit)
        player["name"] = "Student"
        player["gender"] = "M"
        print(f"\n{Fore.YELLOW}Using default values for non-interactive environment.{Style.RESET_ALL}")
    else:
        try:
            player["name"] = input(f"{Fore.YELLOW}Enter your name: {Style.RESET_ALL}")
            while True:
                gender = input(f"{Fore.YELLOW}Choose your gender (M/F): {Style.RESET_ALL}").upper()
                if gender in ["M", "F"]:
                    player["gender"] = gender
                    break
                print(f"{Fore.RED}Please enter M or F.{Style.RESET_ALL}")
        except EOFError:
            # Fall back to default values if we hit an EOF error
            player["name"] = "Student"
            player["gender"] = "M"
            print(f"\n{Fore.YELLOW}Using default values due to input limitations.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Error during setup: {e}{Style.RESET_ALL}")
            player["name"] = "Student"
            player["gender"] = "M"

    # List of available player traits
PLAYER_TRAITS = {
    # Physical traits
    "strong": {
        "description": "You have above-average physical strength",
        "effects": {"pe_stats_strength": 20, "pe_grade_bonus": 10},
        "category": "physical"
    },
    "athletic": {
        "description": "You excel at physical activities and sports",
        "effects": {"pe_stats_all": 15, "pe_grade_bonus": 15, "stamina_regen": 10},
        "category": "physical"
    },
    "weak": {
        "description": "You have below-average physical strength",
        "effects": {"pe_stats_strength": -15, "pe_grade_penalty": 10},
        "category": "physical"
    },
    "fast": {
        "description": "You can run very quickly",
        "effects": {"pe_stats_agility": 25, "pe_grade_bonus": 5},
        "category": "physical"
    },
    "clumsy": {
        "description": "You're somewhat uncoordinated",
        "effects": {"pe_stats_coordination": -20, "accident_chance": 10},
        "category": "physical"
    },
    "heat_sensitive": {
        "description": "You struggle in hot weather",
        "effects": {"summer_energy_penalty": 15, "summer_pe_penalty": 20},
        "category": "physical"
    },
    "cold_sensitive": {
        "description": "You struggle in cold weather",
        "effects": {"winter_energy_penalty": 15, "winter_pe_penalty": 20},
        "category": "physical"
    },
    
    # Mental traits
    "studious": {
        "description": "You learn academic subjects more easily",
        "effects": {"study_efficiency": 20, "academic_charisma": 10},
        "category": "mental"
    },
    "forgetful": {
        "description": "You often forget things",
        "effects": {"homework_forgotten_chance": 15, "study_efficiency": -10},
        "category": "mental"
    },
    "creative": {
        "description": "You have a strong creative streak",
        "effects": {"art_bonus": 25, "music_bonus": 15, "creativity_activities_bonus": 20},
        "category": "mental"
    },
    "analytical": {
        "description": "You excel at logical thinking",
        "effects": {"math_bonus": 20, "science_bonus": 15, "problem_solving_bonus": 20},
        "category": "mental"
    },
    "night_owl": {
        "description": "You function better at night",
        "effects": {"night_energy_bonus": 20, "morning_energy_penalty": 15},
        "category": "mental"
    },
    "early_bird": {
        "description": "You function better in the morning",
        "effects": {"morning_energy_bonus": 20, "night_energy_penalty": 15},
        "category": "mental"
    },
    
    # Social traits
    "charismatic": {
        "description": "People naturally like you",
        "effects": {"relationship_gain_bonus": 20, "social_charisma": 15},
        "category": "social"
    },
    "shy": {
        "description": "You find social interactions challenging",
        "effects": {"relationship_gain_penalty": 15, "social_stress": 10},
        "category": "social"
    },
    "funny": {
        "description": "You have a great sense of humor",
        "effects": {"joke_success": 25, "stress_reduction_bonus": 15},
        "category": "social"
    },
    "empathetic": {
        "description": "You understand others' feelings well",
        "effects": {"relationship_gain_bonus": 15, "therapy_effectiveness": 20},
        "category": "social"
    },
    "blunt": {
        "description": "You speak your mind without filter",
        "effects": {"honesty_bonus": 20, "relationship_random_penalty": 10},
        "category": "social"
    },
    
    # Circumstantial traits
    "wealthy_family": {
        "description": "Your family has significant wealth",
        "effects": {"starting_money": 2000, "monthly_allowance": 500},
        "category": "circumstantial"
    },
    "scholarship": {
        "description": "You're attending on scholarship",
        "effects": {"grades_importance": 20, "reputation_teachers_gain_bonus": 15},
        "category": "circumstantial"
    },
    "part_timer": {
        "description": "You're experienced with part-time work",
        "effects": {"job_income_bonus": 25, "job_fatigue_reduction": 15},
        "category": "circumstantial"
    },
    "local": {
        "description": "You grew up in this town",
        "effects": {"town_knowledge": 20, "starting_reputation_students": 10},
        "category": "circumstantial"
    },
    "foreigner": {
        "description": "You're from another country",
        "effects": {"cultural_misunderstanding_chance": 20, "language_bonus": 25},
        "category": "circumstantial"
    },
    
    # Personality traits
    "ambitious": {
        "description": "You aim high in everything you do",
        "effects": {"achievement_bonus": 20, "stress_gain": 15},
        "category": "personality"
    },
    "laid_back": {
        "description": "You take life as it comes",
        "effects": {"stress_resistance": 25, "achievement_penalty": 10},
        "category": "personality"
    },
    "perfectionist": {
        "description": "You strive for perfection in your work",
        "effects": {"quality_bonus": 20, "stress_from_failure": 25},
        "category": "personality"
    },
    "adventurous": {
        "description": "You love trying new things",
        "effects": {"new_experience_bonus": 20, "boredom_resistance": 25},
        "category": "personality"
    },
    "cautious": {
        "description": "You carefully consider risks",
        "effects": {"accident_prevention": 25, "spontaneity_penalty": 15},
        "category": "personality"
    }
}

# Function to randomly assign starting traits to the player
def assign_random_traits(count=3):
    """
    Assign random traits to the player
    
    Arguments:
    count -- Number of traits to assign (default: 3)
    
    Returns:
    List of assigned trait names
    """
    # Get all trait categories
    categories = set(trait_data["category"] for trait_data in PLAYER_TRAITS.values())
    
    # Try to select one trait from each category for balance
    selected_traits = []
    remaining_categories = list(categories)
    
    # First, try to take one from each category
    while len(selected_traits) < count and remaining_categories:
        category = random.choice(remaining_categories)
        remaining_categories.remove(category)
        
        # Get traits in this category
        category_traits = [name for name, data in PLAYER_TRAITS.items() 
                          if data["category"] == category and name not in selected_traits]
        
        if category_traits:
            selected_trait = random.choice(category_traits)
            selected_traits.append(selected_trait)
    
    # If we still need more traits, pick from any category
    while len(selected_traits) < count:
        # Get all traits not yet selected
        available_traits = [name for name in PLAYER_TRAITS.keys() 
                           if name not in selected_traits]
        
        if not available_traits:
            break  # No more traits available
        else: 
            selected_trait = random.choice(available_traits)
            selected_traits.append(selected_trait)
    
    return selected_traits

# Reset player to starting state
    player["school_year"] = 1
    player["year_progress"] = 0
    player["money"] = 1000
    player["grades"] = {}
    player["reputation"] = {"students": 0, "teachers": 0}
    player["charisma"] = {"social": 0, "academic": 0}
    player["energy"] = 100
    player["hunger"] = 100
    player["stress"] = 20
    player["health"] = 100
    player["completed_years"] = []
    player["gpa"] = 0.0
    player["achievements"] = []
    player["romantic_interest"] = None
    player["traits"] = []  # Initialize empty traits list
    player["romance_stage"] = 0
    player["romance_points"] = 0
    player["has_had_dinner"] = False
    player["has_slept"] = False
    player["relationships"] = {}  # Initialize empty relationships dictionary

    # Reset mental health to starting values
    player["mental_health"] = {
        "happiness": 80,
        "depression": 0,
        "anxiety": 0,
        "self_esteem": 70,
        "bullying_incidents": 0,
        "breakup_count": 0,
        "therapy_sessions": 0,
        "last_therapy_date": None,
        "support_network": 50,  # Start with moderate social support
    }

    # Reset neurodiversity traits
    player["neurodiversity"] = {
        "traits": [],
        "severity": {},
        "accommodations": [],
        "strengths": [],
    }

    # Reset ex partners
    player["ex_partners"] = []
    
    # Assign random starting traits
    player["traits"] = assign_random_traits(3)
    
    # Display traits to player
    if player["traits"]:
        slow_print(f"\n{Fore.YELLOW}=== Your Character Traits ==={Style.RESET_ALL}")
        for trait in player["traits"]:
            trait_info = PLAYER_TRAITS[trait]
            slow_print(f"{Fore.CYAN}{trait.title()}{Style.RESET_ALL}: {trait_info['description']}")
            
            # Apply trait effects
            if trait == "wealthy_family":
                player["money"] += 2000  # Apply starting money bonus
                slow_print(f"{Fore.GREEN}Your starting money has been increased to ¥{player['money']}{Style.RESET_ALL}")
            elif trait == "strong":
                player["pe_stats"]["strength"] += 20
                slow_print(f"{Fore.GREEN}Your strength has been increased to {player['pe_stats']['strength']}{Style.RESET_ALL}")
            elif trait == "athletic":
                # Apply to all PE stats
                for stat in player["pe_stats"]:
                    player["pe_stats"][stat] += 15
                slow_print(f"{Fore.GREEN}All your physical stats have been improved{Style.RESET_ALL}")
            elif trait == "charismatic":
                player["charisma"]["social"] += 15
                slow_print(f"{Fore.GREEN}Your social charisma has been increased to {player['charisma']['social']}{Style.RESET_ALL}")
            elif trait == "studious":
                player["charisma"]["academic"] += 10
                slow_print(f"{Fore.GREEN}Your academic charisma has been increased to {player['charisma']['academic']}{Style.RESET_ALL}")
            elif trait == "local":
                player["reputation"]["students"] += 10
                slow_print(f"{Fore.GREEN}Your student reputation has been increased to {player['reputation']['students']}{Style.RESET_ALL}")
    
    # 2% chance of having a neurodivergent trait
    if random.random() < 0.02:
        # Select a random trait
        trait = random.choice(list(NEURODIVERSITY_TRAITS.keys()))
        severity = random.randint(3, 8)  # Scale 1-10, moderate severity

        player["neurodiversity"]["traits"].append(trait)
        player["neurodiversity"]["severity"][trait] = severity

        # Select a few strengths associated with this trait
        player["neurodiversity"]["strengths"] = random.sample(
            NEURODIVERSITY_TRAITS[trait]["strengths"],
            min(2, len(NEURODIVERSITY_TRAITS[trait]["strengths"])),
        )

        # Apply trait effects
        if trait == "dyslexia":
            player["charisma"]["academic"] -= 2
        elif trait == "adhd":
            player["energy"] += 10
            player["stress"] += 5
        elif trait == "autism":
            player["charisma"]["social"] -= 3
            player["charisma"]["academic"] += 2
        elif trait == "anxiety_disorder":
            player["stress"] += 10
            player["mental_health"]["anxiety"] = 30
        elif trait == "depression":
            player["energy"] -= 10
            player["mental_health"]["depression"] = 30
            player["mental_health"]["happiness"] -= 20

        # Notify the player about their trait
        slow_print(
            f"\n{Fore.CYAN}You have {trait.replace('_', ' ')} (Severity: {severity}/10){Style.RESET_ALL}"
        )
        slow_print(
            f"This gives you strengths in: {', '.join(player['neurodiversity']['strengths'])}"
        )
        slow_print("However, you may face some challenges in certain situations.")

        # Ask about accommodations
        slow_print(
            f"\nWould you like to request academic accommodations for your {trait.replace('_', ' ')}?"
        )
        accommodations_choice = input("(Y/N): ").upper()
        if accommodations_choice == "Y":
            player["neurodiversity"]["accommodations"] = random.sample(
                NEURODIVERSITY_TRAITS[trait]["accommodations"],
                min(2, len(NEURODIVERSITY_TRAITS[trait]["accommodations"])),
            )
            slow_print(
                f"You have been granted: {', '.join(player['neurodiversity']['accommodations'])}"
            )
            # Mitigate some negative impacts of the trait
            if trait in ["dyslexia", "adhd"]:
                player["charisma"]["academic"] += 1

    # Initialize clothing
    player["clothing"] = {
        "owned": [
            "School Uniform",
            "Casual Black T-shirt",
            "Casual Black Pants",
            "Pajamas",
        ],
        "wearing": "School Uniform",
    }

    # Apply initial clothing effects
    apply_clothing_effects("School Uniform", apply=True)

    # Accommodation selection
    slow_print(f"\n{Fore.YELLOW}=== Choose Your Accommodation ==={Style.RESET_ALL}")
    slow_print("You can either live in a student dormitory or commute from home.")
    slow_print(
        f"{Fore.CYAN}Dormitory{Style.RESET_ALL}: Close to campus, less commute time, more freedom. No family interaction."
    )
    slow_print(
        f"{Fore.CYAN}Home{Style.RESET_ALL}: Further from campus, more commute time, family interactions, less freedom."
    )

    # Check if we're in non-interactive mode
    if _non_interactive:
        # Default to dorm in non-interactive mode
        choice = "1"
        print(f"\n{Fore.YELLOW}Auto-selecting dormitory accommodation for non-interactive mode.{Style.RESET_ALL}")
    else:
        print("\nWill you stay in student accommodation?")
        print("1. Yes (Dormitory)")
        print("2. No (Live at home)")
        
        while True:
            try:
                choice = input("Select an option (1-2): ")
                if choice in ["1", "2"]:
                    break
                print("Please select a valid option (1-2).")
            except EOFError:
                # Default to option 1 (dorm) if we get an EOF error
                choice = "1"
                print(f"\n{Fore.YELLOW}Auto-selecting dormitory due to input limitations.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error during selection: {e}. Defaulting to dormitory.{Style.RESET_ALL}")
                choice = "1"
                break
    
    if choice == "1":
        player["accommodation_type"] = "dorm"
        # Assign random dorm number
        player["dorm_number"] = random.randint(100, 999)
        slow_print(
            f"You'll be staying in the student dormitory, room {player['dorm_number']}."
        )
        player["current_location"] = "Dorm Room"

        # No need for detailed family if living in dorm
        # But still generate family for holiday visits
        family, family_relationship = generate_family_members()
        player["family"] = family
        player["family_relationship"] = family_relationship

        # Brief family description
        slow_print(
            "\nYour family lives far from the school, so you'll only see them during holidays."
        )
        for parent in family["parents"]:
            slow_print(
                f"Your {parent['relation']}, {parent['name']}, is a {parent['personality']} {parent['occupation']}."
            )

        if family["siblings"]:
            for sibling in family["siblings"]:
                slow_print(
                    f"You have a {sibling['personality']} {sibling['relation']}, {sibling['name']}."
                )

        # Show dormitory-specific tutorials
        show_tutorial("new_game")
        show_tutorial("sleep")
        show_tutorial("clothing")

    elif choice == "2":
        player["accommodation_type"] = "home"
        player["home_location"] = "Living Room"  # Start at home's living room
        player["current_location"] = "Living Room"

        # Generate detailed family for daily interactions
        family, family_relationship = generate_family_members()
        player["family"] = family
        player["family_relationship"] = family_relationship

        slow_print(f"\n{Fore.YELLOW}=== Your Family ==={Style.RESET_ALL}")
        for parent in family["parents"]:
            slow_print(
                f"Your {parent['relation']}, {parent['name']}, is a {parent['personality']} {parent['occupation']}."
            )
            slow_print(
                f"Initial relationship: {family_relationship[parent['name']]}/100"
            )

        if family["siblings"]:
            slow_print("\nYour siblings:")
            for sibling in family["siblings"]:
                slow_print(
                    f"- {sibling['name']}, your {sibling['personality']} {sibling['relation']}."
                )
                slow_print(
                    f"  Initial relationship: {family_relationship[sibling['name']]}/100"
                )
        else:
            slow_print("You're an only child.")

        # Show home-specific tutorials
        show_tutorial("new_game")
        show_tutorial("relationships")
        show_tutorial("sleep")
        show_tutorial("clothing")

    # Get subject data for the first year
    subjects_data = get_subjects_for_year(player["school_year"])

    # Get available electives for first year
    available_electives = []
    for subject_name in subjects_data:
        if not subjects_data[subject_name].get("core", True):
            available_electives.append(subject_name)

    # Elective subject selection
    slow_print(
        f"\n{Fore.YELLOW}=== Choose Your Elective Subjects for Year 1 ==={Style.RESET_ALL}"
    )
    slow_print(
        "You can choose two elective subjects to study alongside your core subjects."
    )

    for i, elective in enumerate(available_electives, 1):
        print(f"{i}. {elective}")

    chosen_electives = []
    
    # Handle non-interactive mode
    if _non_interactive:
        # Auto-select first two electives in non-interactive mode
        chosen_electives = available_electives[:2]
        print(f"\n{Fore.YELLOW}Auto-selecting first two electives for non-interactive mode.{Style.RESET_ALL}")
        for elective in chosen_electives:
            slow_print(f"You selected {elective}")
    else:
        # Interactive elective selection
        while len(chosen_electives) < 2:
            try:
                choice = input(f"Select elective {len(chosen_electives)+1} by number: ")
                if choice.isdigit() and 1 <= int(choice) <= len(available_electives):
                    elective_choice = available_electives[int(choice) - 1]
                    if elective_choice not in chosen_electives:
                        chosen_electives.append(elective_choice)
                        slow_print(f"You selected {elective_choice}")
                    else:
                        print("You already selected that elective.")
                else:
                    print("Invalid choice. Please enter a valid number.")
            except EOFError:
                # Handle EOF error by selecting defaults
                if len(chosen_electives) == 0:
                    chosen_electives = available_electives[:2]
                    print(f"\n{Fore.YELLOW}Auto-selecting first two electives due to input limitations.{Style.RESET_ALL}")
                    for elective in chosen_electives:
                        slow_print(f"You selected {elective}")
                    break
                else:
                    # Add next available elective
                    for elective in available_electives:
                        if elective not in chosen_electives:
                            chosen_electives.append(elective)
                            slow_print(f"You selected {elective}")
                            break
                    break
            except Exception as e:
                print(f"\n{Fore.RED}Error during selection: {e}. Selecting defaults.{Style.RESET_ALL}")
                chosen_electives = available_electives[:2]
                for elective in chosen_electives:
                    slow_print(f"You selected {elective}")
                break

    player["electives"] = chosen_electives

    # Show the chosen electives
    slow_print(
        f"\n{Fore.GREEN}Your electives for Year 1 are: {', '.join(chosen_electives)}{Style.RESET_ALL}"
    )

    # Create list of core subjects
    core_subjects = []

    # Get subject data for the first year
    subjects_data = get_subjects_for_year(player["school_year"])

    # Identify core subjects
    for subject_name, subject_data in subjects_data.items():
        if subject_data.get("core", False):
            core_subjects.append(subject_name)

    slow_print(f"\nYour core subjects are: {', '.join(core_subjects)}")

    # Initialize teachers for all subjects
    for subject_name, subject_data in subjects_data.items():
        gender = random.choice(["M", "F"])
        first_name = random.choice(
            male_first_names if gender == "M" else female_first_names
        )
        name = f"{first_name} {random.choice(last_names)}"
        personality = random.choice(list(personalities.keys()))
        teachers.append(
            {
                "name": name,
                "subject": subject_name,
                "personality": personality,
                "difficulty": subject_data["difficulty"],
                "gender": gender,
            }
        )
        player["grades"][subject_name] = "C"  # Starting grade

    # Create international student names lists
    international_first_names_male = [
        "John", "Michael", "William", "David", "James", "Robert", "Daniel", "Thomas", "Alex", "Richard",
        "Carlos", "Juan", "Miguel", "Luis", "Pedro", "Antonio", "Jose", "Francisco", "Javier", "Alejandro",
        "Li", "Wei", "Chen", "Zhang", "Wang", "Liu", "Yang", "Huang", "Zhou", "Wu",
        "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Han"
    ]
    
    international_first_names_female = [
        "Mary", "Jennifer", "Sarah", "Elizabeth", "Emily", "Emma", "Olivia", "Sophia", "Isabella", "Charlotte",
        "Maria", "Sofia", "Valentina", "Camila", "Lucia", "Isabella", "Gabriela", "Victoria", "Ana", "Elena",
        "Li", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Wu", "Zhou", "Zhao",
        "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Ha", "Yoon", "Seo", "Jang"
    ]
    
    international_last_names = [
        "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Garcia", "Rodriguez", "Martinez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres",
        "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou",
        "Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"
    ]

    # Create random students for the player's year
    for _ in range(15):
        # Determine if this student is international (15% chance)
        is_international = random.random() < 0.15
        
        gender = random.choice(["M", "F"])
        
        if is_international:
            # Choose a random nationality
            nationality = random.choice(["American", "Chinese", "Korean", "Mexican", "Spanish", "British", "French", "German", "Brazilian", "Indian"])
            
            # Select name based on nationality and gender
            if gender == "M":
                first_name = random.choice(international_first_names_male)
            else:
                first_name = random.choice(international_first_names_female)
                
            last_name = random.choice(international_last_names)
        else:
            # Japanese student
            first_name = random.choice(
                male_first_names if gender == "M" else female_first_names
            )
            last_name = random.choice(last_names)
            nationality = "Japanese"
            
        name = first_name + " " + last_name
        personality = random.choice(list(personalities.keys()))
        year = random.randint(1, 4)  # Students can be from any year
        
        students.append({
            "name": name, 
            "personality": personality, 
            "gender": gender, 
            "year": year,
            "nationality": nationality,
            "is_international": is_international
        })
    
    # Add club presidents to the students list
    for president in club_presidents:
        # Check if the president is already in the students list
        if not any(student.get("name") == president["name"] for student in students):
            # Assume club presidents are in their 3rd or 4th year
            year = random.randint(3, 4)
            # Assume gender based on name (simple approach)
            gender = "M" if president["name"].split()[0] in male_first_names else "F"
            
            # 10% chance for club president to be international
            is_international = random.random() < 0.10
            if is_international:
                nationality = random.choice(["American", "Chinese", "Korean", "Mexican", "Spanish", "British", "French", "German", "Brazilian", "Indian"])
            else:
                nationality = "Japanese"
                
            # Add to students list
            students.append({
                "name": president["name"],
                "personality": president["personality"],
                "gender": gender,
                "year": year,
                "is_club_president": True,
                "club": president["club"],
                "nationality": nationality,
                "is_international": is_international
            })
    
    # Initialize at least 10 student relationships with random relationship points
    classmates = []
    classmate_count = 0
    
    # First check if we have a twin sibling who should be in our class
    # We'll check each sibling to see if they're a twin
    if "family" in player and "siblings" in player["family"]:
        for sibling in player["family"]["siblings"]:
            if "relation" in sibling and "twin" in sibling.get("relation", ""):
                # 100% chance that twin will be in your class if you have one
                twin_name = sibling["name"]
                twin_personality = sibling["personality"]
                
                # Add twin to students list as a year 1 student
                twin_gender = "M" if "brother" in sibling["relation"] else "F"
                
                # Check if twin is already in students list
                twin_exists = False
                for student in students:
                    if student.get("name") == twin_name:
                        twin_exists = True
                        # Update student to be year 1 and have is_twin flag
                        student["year"] = 1
                        student["is_twin"] = True
                        student["personality"] = twin_personality
                        break
                
                # Add twin to students list if not already there
                if not twin_exists:
                    students.append({
                        "name": twin_name,
                        "personality": twin_personality,
                        "gender": twin_gender,
                        "year": 1,
                        "nationality": "Japanese",  # Same as player
                        "is_international": False,
                        "is_twin": True
                    })
                
                # Add twin to classmates with higher starting relationship
                relationship[twin_name] = player["family_relationship"].get(twin_name, 65)
                student_status[twin_name] = get_relationship_status(relationship[twin_name])
                classmates.append(twin_name)
                classmate_count += 1
                
                slow_print(f"{Fore.MAGENTA}Your {sibling['relation']}, {twin_name}, is in your class!{Style.RESET_ALL}")
                break
    
    # First identify students in the player's year to be classmates
    player_year_students = [s for s in students if s.get("year", 1) == 1]
    
    # Number of additional classmates to add (10 - any twins we already added)
    remaining_classmates = 10 - classmate_count
    
    # If we don't have enough year 1 students, we'll just use any student
    if len(player_year_students) < remaining_classmates:
        random_students = random.sample(students, min(remaining_classmates, len(students)))
        for student in random_students:
            if classmate_count < 10:
                name = student["name"]
                # Generate a random relationship level between 5 and 30
                relationship_points = random.randint(5, 30)
                relationship[name] = relationship_points
                student_status[name] = get_relationship_status(relationship_points)
                classmates.append(name)
                classmate_count += 1
    else:
        # We have enough year 1 students to pick from
        random_classmates = random.sample(player_year_students, min(remaining_classmates, len(player_year_students)))
        for student in random_classmates:
            name = student["name"]
            # Generate a random relationship level between 5 and 30
            relationship_points = random.randint(5, 30)
            relationship[name] = relationship_points
            student_status[name] = get_relationship_status(relationship_points)
            classmates.append(name)
            classmate_count += 1
    
    # Also establish a relationship with at least one teacher
    if teachers:
        teacher = random.choice(teachers)
        teacher_name = teacher["name"]
        # Generate a random relationship level between 5 and 25
        teacher_relationship_points = random.randint(5, 25)
        player["relationships"][teacher_name] = teacher_relationship_points
        slow_print(f"\n{Fore.CYAN}You already know {teacher_name}, who teaches {teacher['subject']}.{Style.RESET_ALL}")
    
    if classmates:
        slow_print(f"\n{Fore.CYAN}You already know some of your classmates:{Style.RESET_ALL}")
        for i, classmate in enumerate(classmates, 1):
            if i <= 3:  # Only show the first 3 to avoid overwhelming the player
                slow_print(f"  - {classmate} (Relationship: {relationship[classmate]} points)")
        if len(classmates) > 3:
            slow_print(f"  - And {len(classmates) - 3} others...")

    # Initialize empty homework for all subjects (core + electives)
    homework = {}
    for subject_name in subjects:
        if subject_name in core_subjects or subject_name in player["electives"]:
            homework[subject_name] = False

    # Initialize quest log
    # We need 'global quests' because we're reassigning the variable, not just modifying its contents
    global quests
    quests = []

    # Add core quests
    quests.extend(
        [
            {
                "id": 1,
                "description": "Find your way around campus",
                "objective": "Visit 5 different locations",
                "status": "active",
                "reward": 10,
                "completed": False,
            },
            {
                "id": 2,
                "description": "Meet your roommate",
                "objective": "Go to Student Room 364",
                "status": "active",
                "reward": 5,
                "completed": False,
            },
            {
                "id": 3,
                "description": "Attend orientation",
                "objective": "Go to Classroom",
                "status": "active",
                "reward": 15,
                "completed": False,
            },
        ]
    )

    # Add subject-specific quests
    quest_id = 4
    for subject_name in core_subjects:
        if quest_id <= 10:  # Limit initial quests
            quests.append(
                {
                    "id": quest_id,
                    "description": f"Complete {subject_name} assignment",
                    "objective": f"Study {subject_name}",
                    "status": "active",
                    "reward": 20,
                    "completed": False,
                }
            )
            quest_id += 1

    # Add elective-specific quests
    for elective in chosen_electives:
        quests.append(
            {
                "id": quest_id,
                "description": f"Excel in {elective} class",
                "objective": f"Study {elective} for 3 hours",
                "status": "active",
                "reward": 25,
                "completed": False,
            }
        )
        quest_id += 1

    # Initialize birthdays for the game
    generate_birthdays()  # This sets the global birthdays variable
    
    # Welcome message
    slow_print(
        f"\n{Fore.CYAN}Welcome to your first year of college, {player['name']}!{Style.RESET_ALL}"
    )
    slow_print(
        "Your journey begins now. Good luck with your studies and new life on campus!"
    )
    slow_print("Type /help to see all available commands.")

    # Show more tutorials
    show_tutorial("quests")
    show_tutorial("study")
    show_tutorial("health")


# Handle holiday accommodation switching
def handle_holiday_accommodation():
    """
    Handle accommodation changes during holidays
    Temporarily switch dorm students to home during holidays
    """
    # No need for global player as we're only modifying its contents, not reassigning it

    # Only handle if player is normally in dorm
    if player["accommodation_type"] == "dorm" and is_holiday():
        # Store current status
        if not player.get("holiday_mode", False):
            # Switch to holiday mode (going home)
            player["holiday_mode"] = True
            player["original_location"] = player["current_location"]
            player["temp_accommodation_type"] = player["accommodation_type"]

            # Switch to home
            player["accommodation_type"] = "home"
            player["current_location"] = "Living Room"

            # Show tutorial and notification
            show_tutorial("holidays")
            slow_print(f"\n{Fore.MAGENTA}=== Holiday Break ==={Style.RESET_ALL}")
            slow_print("You've returned to your family home for the holiday break.")
            slow_print(
                "This is a great time to strengthen your family relationships and relax!"
            )
            slow_print("You'll return to your dorm when school resumes.")

            # Family welcomes you home
            slow_print("\nYour family is happy to see you!")
            for parent in player["family"]["parents"]:
                slow_print(f"{parent['name']} greets you warmly.")

                # Improve family relationship
                current_relationship = player["family_relationship"].get(
                    parent["name"], 50
                )
                improvement = random.randint(5, 10)
                player["family_relationship"][parent["name"]] = min(
                    100, current_relationship + improvement
                )

            # Siblings also welcome you if any
            if player["family"]["siblings"]:
                for sibling in player["family"]["siblings"]:
                    slow_print(
                        f"{sibling['name']} seems {random.choice(['happy', 'excited', 'pleased'])} to see you."
                    )

                    # Improve sibling relationship
                    current_relationship = player["family_relationship"].get(
                        sibling["name"], 50
                    )
                    improvement = random.randint(3, 8)
                    player["family_relationship"][sibling["name"]] = min(
                        100, current_relationship + improvement
                    )

    # Handle returning to dorm after holiday
    elif player.get("holiday_mode", False) and not is_holiday():
        # Switch back to dorm
        player["holiday_mode"] = False
        player["accommodation_type"] = player.get("temp_accommodation_type", "dorm")
        player["current_location"] = player.get("original_location", "Dorm Room")

        slow_print(
            f"\n{Fore.CYAN}The holiday break is over. You've returned to your dormitory.{Style.RESET_ALL}"
        )
        slow_print("Your time with family has left you feeling refreshed.")

        # Stress reduction from holiday
        stress_decrease = random.randint(15, 30)
        player["stress"] = max(0, player["stress"] - stress_decrease)
        slow_print(f"Your stress has decreased by {stress_decrease} points.")


# Commands
def show_academic_year():
    """Display information about the current academic year"""
    year_names = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
    year_name = year_names.get(player["school_year"], f"Year {player['school_year']}")

    print(f"\n{Fore.CYAN}=== Academic Year Information ==={Style.RESET_ALL}")
    print(
        f"{Fore.MAGENTA}Current Year: {year_name} (Year {player['school_year']}){Style.RESET_ALL}"
    )
    print(f"Year Progress: {player['year_progress']}%")
    print(f"GPA: {player['gpa']}")

    if player["completed_years"]:
        completed_years = ", ".join(
            str(year) for year in sorted(player["completed_years"])
        )
        print(f"Years Completed: {completed_years}")

    # Get subject data
    subjects_data = get_subjects_for_year(player["school_year"])

    # Core subjects
    core_subjects = []
    elective_subjects = []

    # Process each subject
    for subject_name, subject_data in subjects_data.items():
        if subject_data.get("core", False):
            core_subjects.append(subject_name)
        elif subject_name in player.get("electives", []):
            elective_subjects.append(subject_name)

    print(f"\n{Fore.YELLOW}Current Core Subjects:{Style.RESET_ALL}")
    for subject in sorted(core_subjects):
        grade = player["grades"].get(subject, "N/A")
        print(f"  {subject}: {grade}")

    print(f"\n{Fore.YELLOW}Current Elective Subjects:{Style.RESET_ALL}")
    for subject in sorted(elective_subjects):
        grade = player["grades"].get(subject, "N/A")
        print(f"  {subject}: {grade}")

    if player["school_year"] >= 3 and player["internships"]:
        print(f"\n{Fore.YELLOW}Current Internships:{Style.RESET_ALL}")
        for internship in player["internships"]:
            print(f"  • {internship}")

    # Show when the school year ends
    current_month = current_date.month
    end_month = 3  # March

    if current_month >= 4:  # After April
        months_remaining = (12 - current_month) + end_month
    else:  # January-March
        months_remaining = end_month - current_month

    print(
        f"\n{Fore.CYAN}The school year will end in approximately {months_remaining} months.{Style.RESET_ALL}"
    )

    if player["school_year"] == 4:
        print(
            f"{Fore.MAGENTA}This is your final year! Prepare for graduation.{Style.RESET_ALL}"
        )


def generate_full_student_list():
    """Generate a large list of students for the school (500-600 students)"""
    full_student_list = []
    
    # Generate a random number between 500 and 600
    total_students = random.randint(500, 600)
    
    # Create international student names lists
    international_first_names_male = [
        "John", "Michael", "William", "David", "James", "Robert", "Daniel", "Thomas", "Alex", "Richard",
        "Carlos", "Juan", "Miguel", "Luis", "Pedro", "Antonio", "Jose", "Francisco", "Javier", "Alejandro",
        "Li", "Wei", "Chen", "Zhang", "Wang", "Liu", "Yang", "Huang", "Zhou", "Wu",
        "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Han"
    ]
    
    international_first_names_female = [
        "Mary", "Jennifer", "Sarah", "Elizabeth", "Emily", "Emma", "Olivia", "Sophia", "Isabella", "Charlotte",
        "Maria", "Sofia", "Valentina", "Camila", "Lucia", "Isabella", "Gabriela", "Victoria", "Ana", "Elena",
        "Li", "Wang", "Zhang", "Liu", "Chen", "Yang", "Huang", "Wu", "Zhou", "Zhao",
        "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Ha", "Yoon", "Seo", "Jang"
    ]
    
    international_last_names = [
        "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Garcia", "Rodriguez", "Martinez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres",
        "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou",
        "Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"
    ]
    
    # Tags that can be assigned to students
    tags = [
        "athlete", "honors", "exchange", "scholarship", "commuter", "resident", 
        "club_member", "volunteer", "part_time_worker", "mentor", "tutor",
        "student_council", "newspaper", "theater", "music", "art", "stem", "social",
        "introverted", "extroverted", "night_owl", "early_bird", "studious", "party_goer"
    ]
    
    # Generate students
    for _ in range(total_students):
        # Determine if this student is international (15% chance)
        is_international = random.random() < 0.15
        
        gender = random.choice(["M", "F"])
        
        if is_international:
            # Choose a random nationality
            nationality = random.choice(["American", "Chinese", "Korean", "Mexican", "Spanish", "British", "French", "German", "Brazilian", "Indian"])
            
            # Select name based on nationality and gender
            if gender == "M":
                first_name = random.choice(international_first_names_male)
            else:
                first_name = random.choice(international_first_names_female)
                
            last_name = random.choice(international_last_names)
        else:
            # Japanese student
            first_name = random.choice(
                male_first_names if gender == "M" else female_first_names
            )
            last_name = random.choice(last_names)
            nationality = "Japanese"
            
        name = first_name + " " + last_name
        personality = random.choice(list(personalities.keys()))
        year = random.randint(1, 4)  # Students can be from any year
        
        # Assign 1-3 random tags
        student_tags = random.sample(tags, random.randint(1, 3))
        
        student = {
            "name": name, 
            "personality": personality, 
            "gender": gender, 
            "year": year,
            "nationality": nationality,
            "is_international": is_international,
            "tags": student_tags
        }
        
        # Special chance for club membership
        if random.random() < 0.2:  # 20% chance
            all_club_names = []
            for club_name in clubs:
                all_club_names.append(club_name)
            
            if all_club_names:
                student["club_member"] = random.choice(all_club_names)
                if "club_member" not in student_tags:
                    student_tags.append("club_member")
        
        full_student_list.append(student)
    
    return full_student_list

def show_help():
    print(
        f"""
{Fore.CYAN}=== AVAILABLE COMMANDS ==={Style.RESET_ALL}

{Fore.YELLOW}Basic Commands:{Style.RESET_ALL}
/help               - Show this help message
/exit               - Quit the game
/save [slot_name]   - Save your progress
/load [slot_name]   - Load a saved game
/save_list          - List all save slots
/current_date       - Show current date
/time               - Show current time
/schedule           - Show the school schedule
/settings           - Modify game settings (content filters, difficulty, text speed)

{Fore.YELLOW}Status Commands:{Style.RESET_ALL}
/me                 - Show your complete profile with all stats
/status             - View your current status
/homework           - Check your homework
/quests             - Show current quests
/achievements       - Show your achievements
/relationship       - View your relationships
/year               - Show academic year information
/rumors             - Check campus gossip and rumors
/change_clothes     - Change into different clothing
/student list       - Show all students in the school (500-600 NPCs)
/npc list [tag]     - Show NPCs filtered by tag category

{Fore.YELLOW}Location Commands:{Style.RESET_ALL}
/go [location]      - Move to a location
/sleep              - Sleep in your room or bedroom to advance to the next day
/dinner             - Have dinner at Kitchen or Cafeteria during dinner hours
/look               - Inspect your current location in detail
/who_is_here        - See who is currently in the same location as you

{Fore.YELLOW}Academic Commands:{Style.RESET_ALL}
/study [subject]    - Study a subject
/teachers           - See a list of your teachers
/students           - See a list of your classmates
/complete_quest [id]- Complete a quest

{Fore.YELLOW}Social Commands:{Style.RESET_ALL}
/interact [student] - Interact with a student
/clubs              - See available clubs
/join_club [name]   - Join a club
/leave_club [name]  - Leave a club
/romance            - Check your romantic relationship
/date [date_type]    - Go on a date with your romantic interest (at valid locations)

{Fore.YELLOW}Activities Commands:{Style.RESET_ALL}
/work [job_name]    - Work at a part-time job
/jobs               - List available jobs
/eat [food_name]    - Eat food at the cafeteria
/relax              - Reduce stress by relaxing
"""
    )


def go_location(args):
    if not args:
        print(f"\n{Fore.CYAN}Available Locations:{Style.RESET_ALL}")
        for loc in locations:
            print(f"- {loc}")
        return

    # Check if player is grounded
    if player.get("grounded", 0) > 0 and player["accommodation_type"] == "home":
        home_locations = ["Your Bedroom", "Living Room", "Kitchen", "Home Study"]
        if " ".join(args).capitalize() not in home_locations:
            slow_print(f"\n{Fore.RED}You are grounded for {player['grounded']} more days. You cannot leave home.{Style.RESET_ALL}")
            return

    destination = " ".join(args).capitalize()
    destination_match = next(
        (loc for loc in locations if loc.lower() == destination.lower()), None
    )

    if destination_match:
        # Check if the player's clothing is appropriate for this location
        is_weekday = current_date.weekday() < 5
        is_festival_day = check_for_special_events()
        clothing_appropriate, reason = is_clothing_appropriate(
            player["clothing"]["wearing"],
            destination_match,
            is_school_day=is_weekday,
            is_festival=is_festival_day,
        )

        # Handle inappropriate clothing
        school_locations = [
            "Classroom",
            "School Hallway",
            "Library",
            "Cafeteria",
            "Science Lab",
            "Gym",
        ]

        if not clothing_appropriate:
            if (
                destination_match in school_locations
                and is_weekday
                and player["clothing"]["wearing"] != "School Uniform"
            ):
                # School uniform violation
                response = input(f"Warning: {reason} Continue anyway? (y/n): ").lower()
                if response != "y":
                    slow_print("You decide to change clothes first.")
                    return
                else:
                    # Apply uniform violation sanctions if going to school without uniform
                    apply_sanction("uniform_violation")
            elif player["clothing"][
                "wearing"
            ] == "Pajamas" and destination_match not in [
                "Student Room 364",
                "Your Bedroom",
            ]:
                # Pajamas in public warning
                response = input(f"Warning: {reason} Continue anyway? (y/n): ").lower()
                if response != "y":
                    slow_print("You decide to change clothes first.")
                    return
                else:
                    slow_print(
                        f"{Fore.RED}People are staring at you in your pajamas! Your reputation decreases.{Style.RESET_ALL}"
                    )
                    player["reputation"]["students"] = max(
                        0, player["reputation"]["students"] - 5
                    )
                    player["stress"] += 10
            elif (
                destination_match == "Beach"
                and player["clothing"]["wearing"] != "Swimwear"
            ):
                # Beach without swimwear
                slow_print(
                    f"Warning: {reason} You'll need proper swimwear to enjoy the beach activities."
                )
            elif destination_match == "Gym" and player["clothing"]["wearing"] not in [
                "Sporty Outfit",
                "School Uniform",
            ]:
                # Gym without proper attire
                response = input(f"Warning: {reason} Continue anyway? (y/n): ").lower()
                if response != "y":
                    slow_print("You decide to change clothes first.")
                    return
                else:
                    slow_print("The PE teacher gives you a disapproving look.")
                    player["reputation"]["teachers"] = max(
                        0, player["reputation"]["teachers"] - 2
                    )

        # Move to the location
        slow_print(f"You walk to the {destination_match}.")

        # Update player location
        player["current_location"] = destination_match

        # Energy cost for movement
        player["energy"] = max(0, player["energy"] - 2)
        player["hunger"] = max(0, player["hunger"] - 1)

        # Handle club interactions if the location is a club room
        for club_name, club_info in clubs.items():
            if club_info["location"] == destination_match:
                handle_club_location(club_name)

        # Check for PE class challenges
        if destination_match == "Gym" and random.random() < 0.3:
            pe_class_challenge()

        # Check for romance opportunities
        if random.random() < 0.2:
            romance_opportunity()

        # Apply quest logic
        check_quest_objectives(destination_match)

        # Random events based on location
        random_location_event(destination_match)
    else:
        print("Unknown location.")


def sleep_command(args=None):
    global ticks
    # Only need global for ticks as it's being reassigned on line 9586
    # No need for current_date, homework, player globals as we're only modifying their contents

    # Initialize sleep options
    skip_ticks = 0
    sleep_overnight = False
    stress_decrease = 0

    # Parse arguments for advanced sleep options
    if args:
        try:
            # Check if there's a number argument for skipping ticks
            skip_ticks = int(args[0])
            if skip_ticks < 0 or skip_ticks > 24:
                print("Invalid sleep time. Please enter a value between 1-24 hours.")
                return
        except ValueError:
            # If the argument isn't a number, check if it's a special command
            if args[0].lower() == "overnight":
                sleep_overnight = True
            else:
                print(
                    "Invalid sleep command. Use '/sleep [hours]' or '/sleep overnight'."
                )
                return
    else:
        # Default to sleeping overnight if no arguments
        sleep_overnight = True

    # Check if player is in a valid location to sleep
    valid_sleep_locations = ["Student Room 364", "Your Bedroom"]
    current_location = player["current_location"]

    if current_location not in valid_sleep_locations:
        print(
            f"You can't sleep here. Go to your {'Student Room 364' if player['accommodation_type'] == 'dorm' else 'Your Bedroom'} first."
        )
        return

    # Check if player is wearing pajamas for overnight sleep
    if sleep_overnight and player["clothing"]["wearing"] != "Pajamas":
        # Offer to change into pajamas if they have them
        if "Pajamas" in player["clothing"]["owned"]:
            change_prompt = input(
                "You need to wear pajamas to sleep properly overnight. Change into pajamas? (y/n): "
            ).lower()
            if change_prompt == "y":
                # Change into pajamas
                if player["clothing"]["wearing"]:
                    apply_clothing_effects(player["clothing"]["wearing"], apply=False)

                player["clothing"]["wearing"] = "Pajamas"
                apply_clothing_effects("Pajamas", apply=True)
                slow_print("You changed into your pajamas.")
            else:
                slow_print("You decide not to change clothes.")
                return
        else:
            slow_print(
                "You don't own any pajamas. You need to buy them from the Shopping Mall first."
            )
            return

    # Current time info
    current_hour = (ticks // 10) % 24
    bedtime_start, bedtime_end = bedtime_hours

    # Handle nap (skip ticks)
    if skip_ticks > 0:
        show_tutorial("sleep")
        slow_print(f"{Fore.CYAN}You take a {skip_ticks} hour nap...{Style.RESET_ALL}")

        # Skip the specified number of ticks (10 ticks = 1 hour)
        ticks += skip_ticks * 10

        # Apply nap effects
        energy_gain = min(5 * skip_ticks, 40)  # Cap at 40 energy for naps
        player["energy"] = min(100, player["energy"] + energy_gain)

        stress_decrease = min(2 * skip_ticks, 20)  # Cap at 20 stress reduction
        player["stress"] = max(0, player["stress"] - stress_decrease)

        # Increase hunger due to nap
        player["hunger"] = max(0, player["hunger"] - (skip_ticks * 2))

        slow_print(f"You wake up after {skip_ticks} hours feeling somewhat refreshed.")
        slow_print(f"Energy +{energy_gain}, Stress -{stress_decrease}")

        # Show warnings if hungry
        if player["hunger"] < 30:
            slow_print(f"{Fore.RED}You wake up feeling quite hungry.{Style.RESET_ALL}")

        return

    # Handle overnight sleep
    elif sleep_overnight:
        # Check if it's appropriate bedtime
        if (
            current_hour >= bedtime_start
            or current_hour < bedtime_end
            or player["energy"] <= 30
        ):  # Allow sleeping at night or when tired
            # Set sleeping flag for pajama effects
            player["sleeping"] = True

            # Day is over, advance to next day
            advance_day()
            player["has_slept"] = True

            # Reset sleeping flag after waking up
            player["sleeping"] = False
            player["has_had_dinner"] = False  # Reset dinner flag for the new day

            slow_print(
                f"{Fore.CYAN}You sleep soundly through the night and wake up refreshed.{Style.RESET_ALL}"
            )
            slow_print(f"It's now {current_date.strftime('%A, %B %d')}.")

            # Apply sleep quality modifiers
            sleep_quality = 1.0  # Base sleep quality

            # Better sleep if had dinner
            if player.get("has_had_dinner", False):
                sleep_quality += 0.2
                slow_print("Having had dinner helped you sleep better.")

            # Better sleep if stress is low
            if player["stress"] < 30:
                sleep_quality += 0.1
                slow_print(
                    "Your low stress levels contributed to a good night's sleep."
                )

            # Worse sleep if stress is high
            if player["stress"] > 70:
                sleep_quality -= 0.2
                slow_print("Your high stress made it difficult to sleep well.")

            # Restore energy based on sleep quality
            energy_gain = int(100 * sleep_quality)
            player["energy"] = min(100, energy_gain)

            # Reset homework completion for new day
            for subject in homework:
                homework[subject] = False

            # Decrease stress overnight
            stress_decrease = min(15, int(player["stress"] * 0.2))
            player["stress"] = max(0, player["stress"] - stress_decrease)
        else:
            slow_print(
                "It's too early to sleep for the night. You can take a nap instead using '/sleep [hours]'."
            )
            show_tutorial("sleep")
            return

        # Report stress decrease
        slow_print(f"Your stress decreased by {stress_decrease}.")

        # Check for weekend or holiday
        if is_weekend():
            slow_print(f"{Fore.YELLOW}It's the weekend!{Style.RESET_ALL}")
        elif is_holiday():
            slow_print(f"{Fore.YELLOW}It's a holiday!{Style.RESET_ALL}")

        # Random morning event with family if living at home
        if (
            player["accommodation_type"] == "home" and random.random() < 0.7
        ):  # 70% chance
            have_family_breakfast()
    else:
        print(
            f"It's only {current_hour}:00. It's too early to sleep. Do something else until night time (after {bedtime_start}:00)."
        )


def dinner_command():
    """Have dinner at appropriate locations (Kitchen at home or Cafeteria at school)"""
    have_dinner()


def have_dinner():
    """Have dinner at home or at cafeteria"""
    global ticks

    # Check if in valid location
    valid_dinner_locations = ["Cafeteria", "Kitchen"]
    current_location = player["current_location"]

    if current_location not in valid_dinner_locations:
        print(
            f"You can't have dinner here. Go to the {'Cafeteria' if player['accommodation_type'] == 'dorm' else 'Kitchen'} first."
        )
        return

    # Check if it's dinner time
    current_hour = (ticks // 10) % 24
    dinner_start, dinner_end = mealtime_hours["dinner"]

    if not (dinner_start <= current_hour < dinner_end):
        print(
            f"It's not dinner time yet. Dinner is served between {dinner_start}:00 and {dinner_end}:00."
        )
        return

    # Check if already had dinner
    if player.get("has_had_dinner", False):
        print("You already had dinner today.")
        return

    # Different dinner experience based on location
    if current_location == "Cafeteria":
        # Cafeteria dinner (costs money)
        slow_print(f"\n{Fore.YELLOW}=== Campus Cafeteria Dinner ==={Style.RESET_ALL}")

        # Show menu
        print("Available dinner options:")
        dinner_options = {
            "1": {
                "name": "Standard Meal Set",
                "price": 500,
                "hunger": 60,
                "energy": 20,
                "stress": -10,
            },
            "2": {
                "name": "Deluxe Curry",
                "price": 800,
                "hunger": 80,
                "energy": 30,
                "stress": -15,
            },
            "3": {
                "name": "Healthy Salad Bowl",
                "price": 600,
                "hunger": 50,
                "energy": 25,
                "stress": -20,
            },
            "4": {
                "name": "Ramen Special",
                "price": 700,
                "hunger": 75,
                "energy": 25,
                "stress": -12,
            },
        }

        for key, meal in dinner_options.items():
            print(f"{key}. {meal['name']} - ¥{meal['price']}")

        print("5. Never mind (cancel)")

        choice = input("Choose a meal (1-5): ")

        if choice in dinner_options:
            meal = dinner_options[choice]

            # Check if enough money
            if player["money"] < meal["price"]:
                print(
                    f"You don't have enough money for that. You need ¥{meal['price']}."
                )
                return

            # Purchase meal
            player["money"] -= meal["price"]
            player["hunger"] = min(100, player["hunger"] + meal["hunger"])
            player["energy"] = min(100, player["energy"] + meal["energy"])
            player["stress"] = max(0, player["stress"] + meal["stress"])
            player["has_had_dinner"] = True

            slow_print(f"You enjoy a delicious {meal['name']} for dinner.")
            slow_print(
                f"Hunger +{meal['hunger']}, Energy +{meal['energy']}, Stress {meal['stress']}"
            )
            slow_print(
                f"You spent ¥{meal['price']}. Remaining money: ¥{player['money']}"
            )

            # Advance time
            ticks += 5  # Half an hour
        elif choice == "5":
            print("You decide not to eat dinner at the cafeteria.")
        else:
            print("Invalid choice.")

    else:  # Kitchen (home dinner)
        slow_print(f"\n{Fore.YELLOW}=== Family Dinner ==={Style.RESET_ALL}")

        # Family dinner (free but involves family interaction)
        # Check if any family members are available
        family_members = player["family"]["parents"] + player["family"]["siblings"]
        if not family_members:
            slow_print("You make a simple dinner for yourself at home.")
            player["hunger"] = min(100, player["hunger"] + 50)
            player["energy"] = min(100, player["energy"] + 15)
            player["stress"] = max(0, player["stress"] - 10)
            player["has_had_dinner"] = True
            ticks += 5  # Half an hour
            return

        # Family dinner with interactions
        present_members = random.sample(
            family_members,
            min(len(family_members), random.randint(1, len(family_members))),
        )

        slow_print(
            f"You join your family for dinner. Present: {', '.join([m['name'] for m in present_members])}"
        )

        # Random dinner conversation topics
        topics = [
            "your school progress",
            "current events",
            "family matters",
            "weekend plans",
            "a TV show everyone is watching",
            "future goals",
            "funny childhood memories",
        ]

        topic = random.choice(topics)
        slow_print(f"The conversation revolves around {topic}.")

        # Response options
        print("\nHow do you participate in the conversation?")
        print("1. Actively engage and share your thoughts")
        print("2. Listen mostly and make occasional comments")
        print("3. Stay quiet and focus on your food")

        choice = input("Choose your approach (1-3): ")

        # Effects based on participation
        if choice == "1":
            slow_print("You actively participate in the family conversation.")
            player["stress"] = max(0, player["stress"] - 15)

            # Improve relationship with all present family members
            for member in present_members:
                name = member["name"]
                current_relationship = player["family_relationship"].get(name, 50)
                improvement = random.randint(3, 7)
                player["family_relationship"][name] = min(
                    100, current_relationship + improvement
                )
                slow_print(f"Your relationship with {name} improved.")

        elif choice == "2":
            slow_print("You listen to the conversation and make occasional comments.")
            player["stress"] = max(0, player["stress"] - 10)

            # Slight improvement with family members
            for member in present_members:
                name = member["name"]
                current_relationship = player["family_relationship"].get(name, 50)
                improvement = random.randint(1, 3)
                player["family_relationship"][name] = min(
                    100, current_relationship + improvement
                )

            slow_print("Your family appreciates your attention.")

        else:  # choice == "3"
            slow_print("You stay quiet and focus on your meal.")
            player["stress"] = max(0, player["stress"] - 5)

            # Potential slight negative effect on relationships
            for member in present_members:
                name = member["name"]
                current_relationship = player["family_relationship"].get(name, 50)
                change = random.randint(-2, 1)
                player["family_relationship"][name] = max(
                    0, min(100, current_relationship + change)
                )

            if random.random() < 0.3:  # 30% chance of comment
                commenter = random.choice(present_members)
                slow_print(
                    f"{commenter['name']} asks if you're feeling alright since you're so quiet."
                )

        # Dinner effects
        player["hunger"] = min(100, player["hunger"] + 70)
        player["energy"] = min(100, player["energy"] + 20)
        player["has_had_dinner"] = True

        slow_print("The home-cooked meal was delicious and filling.")
        slow_print("Hunger +70, Energy +20")

        # Advance time
        ticks += 7  # 40 minutes for family dinner


def have_family_breakfast():
    """Have breakfast with family members (only when living at home)"""
    if player["accommodation_type"] != "home" or not player["family"]["parents"]:
        return

    slow_print(f"\n{Fore.YELLOW}=== Family Breakfast ==={Style.RESET_ALL}")

    # Choose a random family member to interact with
    family_members = player["family"]["parents"] + player["family"]["siblings"]
    if not family_members:
        return

    family_member = random.choice(family_members)
    name = family_member["name"]
    relation = family_member.get("relation", "family member")
    personality = family_member.get("personality", "kind")

    slow_print(f"You join your {relation}, {name}, for breakfast.")

    # Generate conversation based on relationship and personality
    if "Mother" in relation or "Father" in relation:
        if personality == "strict":
            conversations = [
                f'"How are your grades? You need to maintain a good GPA," says your {relation} firmly.',
                f'"Did you finish all your homework? Education comes first," your {relation} reminds you.',
                f'"I expect you to excel this semester," says your {relation} with a serious expression.',
                f'"Have you decided what career path you\'re taking?" asks your {relation}.',
                f"Your {relation} gives you a lecture about responsibility and hard work.",
            ]
        elif personality == "caring":
            conversations = [
                f'"Did you sleep well? You seem a bit tired," your {relation} says with concern.',
                f'"I made your favorite breakfast today," says your {relation} with a warm smile.',
                f'"Are you eating properly at school? Don\'t skip meals," your {relation} worries.',
                f'"Is everything okay? You know you can always talk to me," offers your {relation}.',
                f"Your {relation} asks if you need anything for school.",
            ]
        else:  # default/other personalities
            conversations = [
                f'"How are your studies going? Make sure to focus on school," says your {relation}.',
                f"\"Don't forget to call if you're going to be late today,\" reminds your {relation}.",
                f"Your {relation} asks about your friends at school.",
                f'"The weather looks nice today, doesn\'t it?" comments your {relation}.',
                f"Your {relation} discusses family plans for the upcoming weekend.",
            ]
    else:  # Sibling
        if personality == "mischievous":
            conversations = [
                f'"Did you use my stuff without asking again?" your {relation} asks accusingly.',
                f"Your {relation} teases you about your school friends.",
                f'"Want to prank our parents later?" whispers your {relation} with a grin.',
                f"Your {relation} is hiding something under the table and gives you a wink.",
                f'"Cover for me tonight, I\'m sneaking out," your {relation} says quietly.',
            ]
        else:  # default/other personalities
            conversations = [
                f"Your {relation} talks about a new video game they're playing.",
                f'"Can you help me with homework later?" asks your {relation}.',
                f"Your {relation} tells you about drama with their friends.",
                f"Your {relation} is rushing to finish breakfast before heading out.",
                f'"Did you hear what happened at school yesterday?" your {relation} asks excitedly.',
            ]

    conversation = random.choice(conversations)
    slow_print(conversation)

    # Response options
    print("\nHow do you respond?")
    print("1. Engage in conversation")
    print("2. Give brief response")
    print("3. Ignore/change subject")

    choice = input("Choose an option (1-3): ")

    # Relationship impact based on choice
    relationship_change = 0

    if choice == "1":  # Positive interaction
        slow_print("You have a good conversation with your family member.")
        relationship_change = random.randint(2, 5)
        player["stress"] = max(0, player["stress"] - 5)
        slow_print("The pleasant family interaction reduces your stress a bit.")
    elif choice == "2":  # Neutral interaction
        slow_print("You give a brief response and continue eating.")
        relationship_change = random.randint(0, 2)
    else:  # Negative interaction
        slow_print("You try to avoid the conversation and quickly finish your meal.")
        relationship_change = random.randint(-5, -1)

    # Update relationship
    current_relationship = player["family_relationship"].get(name, 50)
    player["family_relationship"][name] = max(
        0, min(100, current_relationship + relationship_change)
    )

    if relationship_change > 0:
        slow_print(f"Your relationship with {name} improved slightly.")
    elif relationship_change < 0:
        slow_print(f"Your relationship with {name} suffered slightly.")

    # Breakfast effect
    player["hunger"] = min(100, player["hunger"] + 30)
    slow_print("Having breakfast satisfies your hunger for now.")


def analyze_student_response(student, target=None):
    personality = student.get("personality", "kind")
    response_types = {
        # Original personality types
        "strict": [
            "I only talk to serious students.",
            "Studies come first!",
            "What's your grade in Math?",
        ],
        "kind": ["Nice to meet you!", "How are you doing?", "Want to study together?"],
        "serious": [
            "Have you done your homework?",
            "The exams are coming up...",
            "Let's focus on studies.",
            "Do you need help with anything?",
        ],
        "lazy": [
            "Hey, what's up?",
            "Want to skip class?",
            "This is boring...",
            "Heya, let's chill",
        ],
        # Anime-inspired personality types
        "tsundere": [
            "Don't get me wrong, I'm not talking to you because I like you or anything!",
            "I-it's not like I wanted to see you!",
            "Hmph! I guess I could help you with homework... if you really need it.",
            "Don't misunderstand! I just happened to be here.",
        ],
        "kuudere": [
            "Hello.",
            "I see you are here again.",
            "Your academic performance is satisfactory.",
            "I have noticed your efforts.",
        ],
        "dandere": [
            "Oh... h-hello there...",
            "I was just... um... reading this book...",
            "You want to t-talk to me...?",
            "*nods silently with a small smile*",
        ],
        "deredere": [
            "Hi there! I'm so happy to see you!",
            "Wow, you look great today! Want to hang out?",
            "I was just thinking about you! What a coincidence!",
            "You're amazing! Let's spend time together!",
        ],
        "yandere": [
            "I've been watching you...",
            "Who were you talking to earlier?",
            "You belong with me, don't you agree?",
            "I'll always be there for you... always...",
        ],
        "genki": [
            "Hey hey! What's up?",
            "Let's do something fun together!",
            "I've got so much energy today! Wanna join me?",
            "There's a new activity I want to try! Come with me!",
        ],
        "himedere": [
            "You may approach me.",
            "I suppose I could grace you with my presence.",
            "Consider yourself fortunate that I'm speaking with you.",
            "A commoner like you should be honored by my attention.",
        ],
    }

    # Check if this is a romantic interest interaction
    if target == "romance" and player["romantic_interest"] == student["name"]:
        stage = player["romance_stage"]

        # Default romantic responses for each stage
        default_romantic_responses = {
            0: [
                "I don't really know you that well...",
                "Oh, hi there.",
                "Did you need something?",
            ],
            1: [
                "Nice to see you again!",
                "I was hoping to run into you.",
                "What's up?",
            ],
            2: [
                "Hey, I was just thinking about you!",
                "I'm glad you came to talk to me.",
                "What have you been up to?",
            ],
            3: [
                "I've been looking forward to seeing you!",
                "You always brighten my day.",
                "I was hoping we could spend some time together.",
            ],
            4: [
                "You know, I really enjoy spending time with you...",
                "There's something I've been wanting to tell you...",
                "Do you want to go somewhere together after school?",
            ],
            5: [
                "Hey there, sweetie!",
                "I've missed you!",
                "Want to go on a date this weekend?",
            ],
        }

        # Personality-specific romantic responses
        personality_romantic_responses = {
            "tsundere": {
                0: [
                    "Why are you talking to me? I-it's not like I care!",
                    "Don't think you're special or anything!",
                    "I just happened to be here, okay?",
                ],
                1: [
                    "I noticed you around... not that I was looking!",
                    "I guess talking to you isn't the worst...",
                    "Don't get any weird ideas about us!",
                ],
                2: [
                    "I didn't save a seat for you or anything... it was just empty!",
                    "I made extra lunch... you can have it if you want...",
                    "You're... not completely terrible to be around.",
                ],
                3: [
                    "I wasn't waiting for you! I just got here early!",
                    "It's not like I made this specially for you... I just had extra!",
                    "You're... kind of important to me... maybe.",
                ],
                4: [
                    "Don't get me wrong, I don't like-like you or anything!",
                    "I just happened to have two tickets... it would be a waste not to invite you.",
                    "I... fine! I like spending time with you! Happy now?",
                ],
                5: [
                    "B-baka! Of course I like you! Why else would I be here?",
                    "It's not like I love you or anything... I just... okay maybe I do.",
                    "Don't make me say embarrassing things!",
                ],
            },
            "kuudere": {
                0: [
                    "Hello.",
                    "I acknowledge your presence.",
                    "You wish to speak with me?",
                ],
                1: [
                    "Your company is acceptable.",
                    "I find your conversation... adequate.",
                    "I would not object to further interaction.",
                ],
                2: [
                    "I anticipated our meeting today.",
                    "Your academic performance is impressive.",
                    "I have prepared notes for our shared class.",
                ],
                3: [
                    "Your absence was... noticeable.",
                    "I have calculated a 73% compatibility between us.",
                    "Your presence causes an unusual physiological response in me.",
                ],
                4: [
                    "I have analyzed my feelings. The conclusion is... affection.",
                    "My efficiency decreases by 23% when thinking of you. This is... troubling.",
                    "I would like to establish a formal relationship.",
                ],
                5: [
                    "I experience happiness in your presence.",
                    "I have strong emotional attachments to you.",
                    "My feelings for you are... significant.",
                ],
            },
            "dandere": {
                0: ["Oh... um... h-hi...", "*looks down shyly*", "*smiles nervously*"],
                1: [
                    "I... um... it's nice to see you...",
                    "*quietly offers you a small gift*",
                    "*whispers* Thank you for talking to me...",
                ],
                2: [
                    "I was... hoping you might come by today...",
                    "*writes you a note instead of speaking*",
                    "*finally makes eye contact and smiles*",
                ],
                3: [
                    "I've been... thinking about you...",
                    "*speaks more than usual when you're alone together*",
                    "I... made something for you...",
                ],
                4: [
                    "Being with you makes me... happy...",
                    "*manages a full conversation without looking away*",
                    "I... really care about you...",
                ],
                5: [
                    "You make me feel safe enough to be myself...",
                    "*initiates holding hands*",
                    "*whispers* I love you...",
                ],
            },
            "deredere": {
                0: [
                    "Hi there! Nice to meet you!",
                    "Wow, I'm so happy you came to talk to me!",
                    "You seem really interesting!",
                ],
                1: [
                    "I was just thinking about you! How's your day?",
                    "You always have the best energy! I love that!",
                    "I've been hoping to run into you!",
                ],
                2: [
                    "You're amazing! I love spending time with you!",
                    "Every day is better when I get to see you!",
                    "You always make me smile so much!",
                ],
                3: [
                    "I've been thinking about you all day!",
                    "You're the best thing in my life right now!",
                    "I get so excited whenever I see you!",
                ],
                4: [
                    "My heart beats faster whenever you're near!",
                    "I've never felt this way about anyone before!",
                    "You mean everything to me!",
                ],
                5: [
                    "I love you so much! You're my everything!",
                    "Every moment with you is magical!",
                    "You make me the happiest person in the world!",
                ],
            },
            "yandere": {
                0: [
                    "Oh, you noticed me...",
                    "I've been watching you for a while...",
                    "You're talking to me? How wonderful...",
                ],
                1: [
                    "I saw you yesterday... you looked nice.",
                    "I know your schedule by heart already.",
                    "You don't need other friends, you know...",
                ],
                2: [
                    "I don't like when you talk to others...",
                    "You belong with me, don't you think?",
                    "I've been keeping track of everywhere you go...",
                ],
                3: [
                    "I made sure no one else will bother us today...",
                    "I've cleared my schedule - and yours - so we can be together.",
                    "No one will ever love you like I do. No one.",
                ],
                4: [
                    "I've eliminated all distractions from your life.",
                    "We're meant to be together forever.",
                    "I can't live without you. And I won't let you live without me.",
                ],
                5: [
                    "You're mine. Forever and ever and ever...",
                    "I've made sure we'll never be apart again.",
                    "I love you so much it hurts... Do you understand?",
                ],
            },
            "genki": {
                0: [
                    "Hey hey! Nice to meet you!",
                    "Wow, this is exciting! Let's be friends!",
                    "I love meeting new people! Especially ones as cool as you!",
                ],
                1: [
                    "Hey there! Ready for another awesome day?",
                    "I have so much energy today! Let's do something fun!",
                    "Life is an adventure, right? Let's enjoy it together!",
                ],
                2: [
                    "I was just about to go do something fun! Wanna come?",
                    "You make every day more exciting!",
                    "We make such a great team, don't we?",
                ],
                3: [
                    "I can't stop thinking about all the fun things we could do together!",
                    "You're the highlight of my day, every day!",
                    "Being with you makes everything twice as fun!",
                ],
                4: [
                    "My heart does a little dance whenever I see you!",
                    "I've never met anyone who gets me like you do!",
                    "Let's make every moment count together!",
                ],
                5: [
                    "You're my favorite person in the whole world!",
                    "Life with you is like one big exciting adventure!",
                    "I want to share all my happiness with you forever!",
                ],
            },
            "himedere": {
                0: [
                    "You may address me if you wish.",
                    "I suppose I could spare you a moment of my time.",
                    "Oh? You're approaching me?",
                ],
                1: [
                    "I acknowledge your persistent attempts to gain my favor.",
                    "Your dedication to earning my attention is... noted.",
                    "I shall permit you to accompany me occasionally.",
                ],
                2: [
                    "You have shown yourself worthy of my continued acknowledgment.",
                    "I find your company less tiresome than most.",
                    "I have decided to include you in my inner circle.",
                ],
                3: [
                    "Your absence is... noticeable to me.",
                    "I have come to expect your presence.",
                    "I shall allow you the honor of escorting me.",
                ],
                4: [
                    "I find myself... thinking of you in your absence.",
                    "You have somehow become important to me. How curious.",
                    "I shall grant you the exclusive privilege of my affection.",
                ],
                5: [
                    "You alone are worthy of my love.",
                    "I have chosen you above all others.",
                    "Consider yourself honored - you have captured the heart of royalty.",
                ],
            },
        }

        # Use personality-specific responses if available, otherwise default
        if (
            personality in personality_romantic_responses
            and stage in personality_romantic_responses[personality]
        ):
            return random.choice(personality_romantic_responses[personality][stage])
        else:
            return random.choice(default_romantic_responses[stage])

    # Standard personality-based response
    base_response = random.choice(response_types[personality])

    # Add context based on player's stats
    if target == "player":
        if player["grades"].get("Math", "C") == "A":
            base_response += "\nWow, you're really good at Math!"
        if player["reputation"]["students"] > 50:
            base_response += "\nEveryone talks about you!"
        if player["charisma"]["social"] > 5:
            base_response += "\nYou're really easy to talk to!"
        if player["charisma"]["academic"] > 5:
            base_response += "\nYou seem really smart!"
        if player["money"] > 100000:
            base_response += "\nYou seem to have a lot of money!"
        if player["charisma"]["social"] < 5:
            base_response += "\nYou seem a bit shy."
        if player["charisma"]["academic"] < 5:
            base_response += "\nHave you even studied lately?"

    # Add special responses based on relationship level
    if student["name"] in relationship:
        points = relationship[student["name"]]
        if points >= 90:
            base_response += (
                f"\n{Fore.MAGENTA}We've become such close friends!{Style.RESET_ALL}"
            )
        elif points >= 70:
            base_response += (
                f"\n{Fore.GREEN}I'm glad we're good friends!{Style.RESET_ALL}"
            )
        elif points >= 40:
            base_response += "\nIt's nice having you as a friend."

    return base_response


def get_relationship_status(points):
    for threshold, status in sorted(RELATIONSHIP_LEVELS.items(), reverse=True):
        if points >= threshold:
            return status
    return "Stranger"


def interact_student(args):
    if not args:
        print("Usage: /interact [student name]")
        return
    name = " ".join(args)

    # Check if it's an ex-partner
    ex_partner = next(
        (ex for ex in player["ex_partners"] if ex["name"].lower() == name.lower()), None
    )
    if ex_partner:
        interact_ex_partner(ex_partner)
        return

    found = next((s for s in students if s["name"].lower() == name.lower()), None)
    if found:
        if name not in relationship:
            relationship[name] = 0
            student_status[name] = "Stranger"

        current_status = get_relationship_status(relationship[name])
        print(f"\n{Fore.CYAN}================================{Style.RESET_ALL}")
        print(f"           {found['name']}")
        
        # Show special status for club presidents
        if found.get("is_club_president", False):
            print(f"{Fore.YELLOW}Club President: {found['club']}{Style.RESET_ALL}")
            
        print(f"Status: {current_status}")
        print(f"Points: {relationship[name]}")
        print("================================")
        print("1. Chat")
        print("2. Study together")
        print("3. Ask about others")
        print("4. Give gift")
        if relationship.get(name, 0) >= 40:  # Friend level required
            print("5. Ask to hang out")
            print("7. Ask for friendship")
        if relationship.get(name, 0) >= 50:
            print("8. Ask for money")
        if relationship.get(name, 0) >= 70 and not student_status.get(name, "").startswith(
            ("Best Friend", "Dating")
        ):
            print("6. Confess feelings")
        if relationship.get(name, 0) >= 60:
            print("9. Ask for help with homework")
        if relationship.get(name, 0) >= 80:
            print("10. Request a favor")

        # If they're your partner and NSFW is allowed, show intimate options
        if student_status.get(name, "") == "Dating" and game_settings.get(
            "allow_nsfw", False
        ):
            print(f"{Fore.MAGENTA}11. Suggest private time{Style.RESET_ALL}")

        # Flirting options based on relationship level
        if relationship.get(name, 0) >= 30 and found["gender"] != player["gender"]:
            print(f"{Fore.MAGENTA}15. Flirt{Style.RESET_ALL}")
            if relationship.get(name, 0) >= 50:
                print(f"{Fore.MAGENTA}16. Compliment appearance{Style.RESET_ALL}")
            if relationship.get(name, 0) >= 70:
                print(f"{Fore.MAGENTA}17. Playful teasing{Style.RESET_ALL}")
            if relationship.get(name, 0) >= 85:
                print(f"{Fore.MAGENTA}18. Hold hands{Style.RESET_ALL}")
        
        # Gossip and rumor options
        if relationship.get(name, 0) >= 50:
            print("12. Share gossip")
            print("13. Ask about rumors")
            print("14. Start a rumor")
        print(f"================================{Style.RESET_ALL}")

        choice = input(f"\n{Fore.GREEN}Choose an option:{Style.RESET_ALL} ")
        points_gain = 0
        personality = found.get("personality", "kind")

        print(f"\n{Fore.YELLOW}{found['name']}:{Style.RESET_ALL}")

        # Declare variables that might be used in later conditions
        subject = (
            "General Studies"  # Default value in case there are no current subjects
        )
        current_grade = 60.0
        new_grade = 60.0

        # Get personality-specific relationship modifiers
        relationship_gain_mult = (
            personalities[personality].get("relationship_gain", 3) / 3.0
        )
        relationship_loss_mult = (
            personalities[personality].get("relationship_loss", 3) / 3.0
        )

        # Personality-specific responses for different interaction types
        if choice == "1":  # Chat
            response = analyze_student_response(found, "player")
            slow_print(response)

            # Personality affects chat points
            base_points = random.randint(2, 5)

            # Special personality handling
            if personality == "tsundere" and relationship.get(name, 0) < 30:
                # Tsundere initially gives fewer points but more later
                points_gain = int(base_points * 0.7)
                slow_print(
                    f"{Fore.CYAN}(They seem reluctant to chat, but you sense they actually enjoy talking to you){Style.RESET_ALL}"
                )
            elif personality == "dandere" and relationship.get(name, 0) < 20:
                # Dandere takes time to open up
                points_gain = int(base_points * 0.6)
                slow_print(
                    f"{Fore.CYAN}(They seem very shy, but appreciate your patience){Style.RESET_ALL}"
                )
            elif personality == "yandere" and relationship.get(name, 0) > 50:
                # Yandere becomes more intense at higher relationship levels
                points_gain = int(base_points * 1.5)
                slow_print(
                    f"{Fore.RED}(They seem intensely focused on you...){Style.RESET_ALL}"
                )
            else:
                points_gain = int(base_points * relationship_gain_mult)

        elif choice == "2":  # Study together
            # Academic-focused personalities prefer studying
            academic_focused = personality in ["strict", "serious", "kuudere"]
            if academic_focused:
                messages = [
                    "Great idea! Let's study together!",
                    "I was hoping you'd suggest that.",
                    "Excellent. I have prepared some notes.",
                    "Your academic focus is commendable.",
                ]
                slow_print(random.choice(messages))
                points_gain = int(random.randint(3, 7) * relationship_gain_mult)
                player["charisma"]["academic"] += 1
            else:
                if personality == "lazy":
                    slow_print("Study? Do we have to? *sighs* Fine...")
                    points_gain = int(random.randint(1, 2) * relationship_gain_mult)
                elif personality == "tsundere":
                    slow_print(
                        "I-it's not like I'm helping you because I care! I just don't want you to fail..."
                    )
                    points_gain = int(random.randint(2, 4) * relationship_gain_mult)
                elif personality == "deredere" or personality == "genki":
                    slow_print("Sure! Studying is more fun with you around!")
                    points_gain = int(random.randint(2, 5) * relationship_gain_mult)
                else:
                    slow_print("Study? Maybe later...")
                    points_gain = int(random.randint(1, 3) * relationship_gain_mult)

        elif choice == "3":  # Ask about others
            other_student = random.choice(students)
            while other_student["name"] == found["name"]:
                other_student = random.choice(students)

            # Yandere doesn't like talking about others
            if personality == "yandere":
                slow_print(
                    f"Why do you care about {other_student['name']}? You should only be interested in me..."
                )
                points_gain = -int(random.randint(3, 6) * relationship_loss_mult)
            # Himedere is dismissive of others
            elif personality == "himedere":
                slow_print(
                    f"{other_student['name']}? A commoner not worth my time. Unlike you, who has better taste."
                )
                points_gain = int(random.randint(1, 3) * relationship_gain_mult)
            else:
                response = analyze_student_response(other_student)
                slow_print(f"Oh, {other_student['name']}? {response}")
                points_gain = int(random.randint(2, 4) * relationship_gain_mult)

        elif choice == "4":  # Give gift
            if player["money"] >= 500:
                player["money"] -= 500

                if personality == "tsundere":
                    slow_print(
                        "W-why would you give me this? It's not like I wanted a gift... but... thank you."
                    )
                    points_gain = int(random.randint(6, 12) * relationship_gain_mult)
                elif personality == "kuudere":
                    slow_print("A gift. This is... unexpected. I will treasure it.")
                    points_gain = int(random.randint(5, 10) * relationship_gain_mult)
                elif personality == "dandere":
                    slow_print(
                        "*looks surprised and blushes* F-for me? Thank you so much..."
                    )
                    points_gain = int(random.randint(7, 12) * relationship_gain_mult)
                elif personality == "deredere":
                    slow_print(
                        "Oh my gosh! A gift! I love it! You're the sweetest person ever!"
                    )
                    points_gain = int(random.randint(8, 15) * relationship_gain_mult)
                elif personality == "yandere":
                    slow_print(
                        "A gift from you? I'll keep it forever. I'll never let it go. Never."
                    )
                    points_gain = int(random.randint(10, 20) * relationship_gain_mult)
                elif personality == "genki":
                    slow_print(
                        "Wow! This is so exciting! Thank you, thank you, thank you!"
                    )
                    points_gain = int(random.randint(7, 12) * relationship_gain_mult)
                elif personality == "himedere":
                    slow_print(
                        "Hmm, acceptable. I shall add it to my collection of tributes from admirers."
                    )
                    points_gain = int(random.randint(5, 8) * relationship_gain_mult)
                else:
                    slow_print("They really appreciated your gift!")
                    points_gain = int(random.randint(5, 10) * relationship_gain_mult)
            else:
                slow_print("You don't have enough money for a gift...")

        elif choice == "5" and relationship.get(name, 0) >= 40:  # Hang out
            if personality == "dandere":
                slow_print("*nods shyly* I'd... like that...")
                points_gain = int(random.randint(6, 10) * relationship_gain_mult)
            elif personality == "kuudere":
                slow_print(
                    "I find the prospect of spending time with you... satisfactory."
                )
                points_gain = int(random.randint(4, 7) * relationship_gain_mult)
            elif personality == "deredere" or personality == "genki":
                slow_print(
                    "Yes! I'd love to hang out with you! I know the perfect place!"
                )
                points_gain = int(random.randint(8, 12) * relationship_gain_mult)
            elif personality == "yandere":
                slow_print("Just the two of us? Alone? Yes. That's perfect.")
                points_gain = int(random.randint(10, 15) * relationship_gain_mult)
            else:
                slow_print("You had a great time hanging out!")
                points_gain = int(random.randint(5, 8) * relationship_gain_mult)

            player["charisma"]["social"] += 1

        elif choice == "6" and relationship.get(name, 0) >= 70:  # Confess feelings
            # Romance compatibility affects success chance
            romance_compatibility = personalities[personality].get(
                "romance_compatibility", 0.7
            )
            success_chance = (
                player["charisma"]["social"] / 100
            ) * romance_compatibility

            if random.random() < success_chance:
                student_status[name] = "Dating"

                if personality == "tsundere":
                    slow_print(
                        f"{Fore.GREEN}I... fine! I like you too! Are you happy now? Don't make me say it again!{Style.RESET_ALL}"
                    )
                elif personality == "kuudere":
                    slow_print(
                        f"{Fore.GREEN}I have also developed romantic feelings for you. This is acceptable.{Style.RESET_ALL}"
                    )
                elif personality == "dandere":
                    slow_print(
                        f"{Fore.GREEN}*blushes deeply* I... I've liked you for a long time... *smiles*{Style.RESET_ALL}"
                    )
                elif personality == "deredere":
                    slow_print(
                        f"{Fore.GREEN}Yes! Yes! I love you too! I'm so happy right now!{Style.RESET_ALL}"
                    )
                elif personality == "yandere":
                    slow_print(
                        f"{Fore.GREEN}Finally. You're mine now. Forever and ever...{Style.RESET_ALL}"
                    )
                elif personality == "genki":
                    slow_print(
                        f"{Fore.GREEN}Wow! This is the best day ever! Of course I feel the same way!{Style.RESET_ALL}"
                    )
                elif personality == "himedere":
                    slow_print(
                        f"{Fore.GREEN}I suppose I shall accept your feelings. Consider yourself fortunate.{Style.RESET_ALL}"
                    )
                else:
                    slow_print(
                        f"{Fore.GREEN}They accepted your feelings!{Style.RESET_ALL}"
                    )

                points_gain = int(random.randint(10, 15) * relationship_gain_mult)

                # Set player's romantic interest
                player["romantic_interest"] = name
                player["romance_stage"] = 5  # Start at dating stage

            else:
                if personality == "tsundere":
                    slow_print(
                        f"{Fore.RED}W-what? Don't say such embarrassing things! I don't... I'm not ready...{Style.RESET_ALL}"
                    )
                elif personality == "kuudere":
                    slow_print(
                        f"{Fore.RED}Your feelings are noted, but I cannot reciprocate at this time.{Style.RESET_ALL}"
                    )
                elif personality == "dandere":
                    slow_print(
                        f"{Fore.RED}*looks down* I'm sorry... I'm not... I can't...{Style.RESET_ALL}"
                    )
                elif personality == "deredere":
                    slow_print(
                        f"{Fore.RED}Oh! I'm so flattered, but I think we should stay friends for now.{Style.RESET_ALL}"
                    )
                elif personality == "yandere":
                    slow_print(
                        f"{Fore.RED}Not yet. You need to prove yourself to me first. Show me how much you care...{Style.RESET_ALL}"
                    )
                elif personality == "himedere":
                    slow_print(
                        f"{Fore.RED}You presume too much. One does not simply confess to royalty.{Style.RESET_ALL}"
                    )
                else:
                    slow_print(
                        f"{Fore.RED}They want to remain friends...{Style.RESET_ALL}"
                    )

                points_gain = -int(random.randint(5, 10) * relationship_loss_mult)

        elif choice == "7" and relationship.get(name, 0) >= 40:  # Ask for friendship
            current_level = get_relationship_status(relationship.get(name, 0))
            next_level = None

            # Determine next level
            if current_level == "Acquaintance":
                next_level = "Friend"
            elif current_level == "Friend":
                next_level = "Close Friend"
            elif current_level == "Close Friend":
                next_level = "Best Friend"

            if next_level:
                # Success chance based on personality and current relationship
                success_chance = min(0.85, relationship.get(name, 0) / 100)

                # Personality adjustments
                if personality == "deredere" or personality == "genki":
                    success_chance += 0.15  # More open to friendship
                elif personality == "kuudere" or personality == "himedere":
                    success_chance -= 0.1  # More reserved
                elif personality == "yandere":
                    success_chance += (
                        0.2 if player.get("romantic_interest") == name else -0.2
                    )

                if random.random() < success_chance:
                    if personality == "tsundere":
                        slow_print(
                            f"{Fore.GREEN}Friends? I guess... if it's that important to you... Not that I care!{Style.RESET_ALL}"
                        )
                    elif personality == "kuudere":
                        slow_print(
                            f"{Fore.GREEN}I acknowledge our bond has grown. Your friendship is acceptable.{Style.RESET_ALL}"
                        )
                    elif personality == "dandere":
                        slow_print(
                            f"{Fore.GREEN}*smiles softly* I'd... really like that...{Style.RESET_ALL}"
                        )
                    elif personality == "deredere" or personality == "genki":
                        slow_print(
                            f"{Fore.GREEN}Yes! We're totally {next_level.lower()}s now! This is amazing!{Style.RESET_ALL}"
                        )
                    elif personality == "yandere":
                        slow_print(
                            f"{Fore.GREEN}Closer friends? Good. I want to be the closest person to you...{Style.RESET_ALL}"
                        )
                    elif personality == "himedere":
                        slow_print(
                            f"{Fore.GREEN}I shall grant you the status of royal {next_level.lower()}. Consider it an honor.{Style.RESET_ALL}"
                        )
                    else:
                        slow_print(
                            f"{Fore.GREEN}Of course! I'd love to be {next_level.lower()}s with you!{Style.RESET_ALL}"
                        )

                    if next_level == "Best Friend":
                        student_status[name] = "Best Friend"
                        player["best_friend"] = name
                        slow_print(f"You are now best friends with {name}!")
                    else:
                        slow_print(
                            f"Your relationship with {name} has advanced to {next_level}!"
                        )

                    # Significant relationship boost
                    points_gain = int(random.randint(10, 20) * relationship_gain_mult)
                else:
                    slow_print(
                        f"{Fore.RED}I don't think we're quite there yet. Let's spend more time together first.{Style.RESET_ALL}"
                    )
                    points_gain = -int(random.randint(3, 8) * relationship_loss_mult)
            else:
                if current_level.startswith("Best Friend"):
                    slow_print(f"You're already best friends with {name}!")
                elif current_level.startswith("Dating"):
                    slow_print(f"You're already dating {name}!")
                else:
                    slow_print(f"Your relationship is already at {current_level}.")
                points_gain = 0

        elif choice == "8" and relationship.get(name, 0) >= 50:  # Ask for money
            # Base chance depends on relationship and personality
            base_chance = min(0.6, relationship.get(name, 0) / 120)

            # Personality adjustments
            if personality == "deredere" or personality == "genki":
                base_chance += 0.1  # More generous
            elif personality == "kuudere" or personality == "himedere":
                base_chance -= 0.15  # Less likely to give money
            elif personality == "tsundere":
                base_chance -= 0.05  # Reluctant

            # Chance decreases if player has asked before
            if player.get("money_requests", {}).get(name, 0) > 0:
                base_chance -= 0.2 * player["money_requests"].get(name, 0)

            # Initialize money_requests tracking if not exists
            if "money_requests" not in player:
                player["money_requests"] = {}

            # Amount depends on relationship
            min_amount = 500
            max_amount = int(min(5000, relationship.get(name, 0) * 50))

            if random.random() < base_chance:
                amount = random.randint(min_amount, max_amount)
                player["money"] += amount

                # Track this request
                player["money_requests"][name] = (
                    player["money_requests"].get(name, 0) + 1
                )

                if personality == "tsundere":
                    slow_print(
                        f"{Fore.GREEN}Fine, take it! But don't think I'm doing this because I like you or anything!{Style.RESET_ALL}"
                    )
                elif personality == "kuudere":
                    slow_print(
                        f"{Fore.GREEN}I see. Your financial situation is suboptimal. I can provide assistance this once.{Style.RESET_ALL}"
                    )
                elif personality == "dandere":
                    slow_print(
                        f"{Fore.GREEN}*quietly hands over money* H-here... please use it well...{Style.RESET_ALL}"
                    )
                elif personality == "deredere":
                    slow_print(
                        f"{Fore.GREEN}Of course I'll help you! What are friends for?{Style.RESET_ALL}"
                    )
                elif personality == "yandere":
                    slow_print(
                        f"{Fore.GREEN}You need money? I'll give you whatever you need. Just stay with me.{Style.RESET_ALL}"
                    )
                elif personality == "himedere":
                    slow_print(
                        f"{Fore.GREEN}A royal donation to help one of my subjects. Use it wisely.{Style.RESET_ALL}"
                    )
                else:
                    slow_print(
                        f"{Fore.GREEN}Sure, I can help you out this time.{Style.RESET_ALL}"
                    )

                slow_print(f"You received ¥{amount}!")
                points_gain = int(random.randint(2, 5) * relationship_gain_mult)
            else:
                if player.get("money_requests", {}).get(name, 0) > 0:
                    slow_print(
                        f"{Fore.RED}You've already asked me for money before... I can't keep giving you money.{Style.RESET_ALL}"
                    )
                else:
                    slow_print(
                        f"{Fore.RED}I'm sorry, I can't spare any money right now.{Style.RESET_ALL}"
                    )
                points_gain = -int(random.randint(5, 10) * relationship_loss_mult)

        elif choice == "9" and relationship.get(name, 0) >= 60:  # Ask for help with homework
            # Get current subjects and homework
            current_subjects = get_current_subjects()
            incomplete_homework = [
                subject
                for subject in current_subjects
                if not homework.get(subject, False)
            ]

            if not incomplete_homework:
                slow_print("You don't have any incomplete homework right now.")
                points_gain = 0
            else:
                # Pick a random subject
                subject = random.choice(incomplete_homework)

                # Chance to help depends on relationship and personality
                help_chance = min(0.9, relationship.get(name, 0) / 100)

                # Personality and intelligence adjustments
                student_intelligence = found.get("intelligence", 60)
                if student_intelligence > 70:
                    help_chance += 0.15
                elif student_intelligence < 40:
                    help_chance -= 0.15

                if personality in ["serious", "kuudere"]:
                    help_chance += 0.2  # More likely to help with academic matters
                elif personality == "lazy":
                    help_chance -= 0.3  # Less likely to help

                if random.random() < help_chance:
                    # Complete the homework
                    homework[subject] = True

                    # Grade boost
                    grade_boost = random.uniform(
                        1.0, 3.0
                    )  # Bigger boost than studying alone
                    current_grade = player["grades"].get(subject, 60.0)
                    new_grade = min(100.0, current_grade + grade_boost)
                    player["grades"][subject] = new_grade

                    if personality == "tsundere":
                        slow_print(
                            f"{Fore.GREEN}Fine, I'll help you. But only because you'd obviously fail without me!{Style.RESET_ALL}"
                        )
                    elif personality == "kuudere":
                        slow_print(
                            f"{Fore.GREEN}Your academic progress is important. I will assist you with this assignment.{Style.RESET_ALL}"
                        )
                    elif personality == "dandere":
                        slow_print(
                            f"{Fore.GREEN}I'd be happy to help... I actually really enjoy {subject}...{Style.RESET_ALL}"
                        )
                    elif personality == "deredere":
                        slow_print(
                            f"{Fore.GREEN}Homework together? That's so fun! Let's make it a study date!{Style.RESET_ALL}"
                        )
                    elif personality == "yandere":
                        slow_print(
                            f"{Fore.GREEN}I'll help you with anything you need. Anything at all...{Style.RESET_ALL}"
                        )
                    elif personality == "genki":
                        slow_print(
                            f"{Fore.GREEN}Let's tackle this homework together! We'll finish it in no time!{Style.RESET_ALL}"
                        )
                    else:
                        slow_print(
                            f"{Fore.GREEN}Sure, I can help you with your {subject} homework.{Style.RESET_ALL}"
                        )

                    slow_print(
                        f"With {name}'s help, you completed your {subject} homework!"
                    )
                    slow_print(
                        f"Your grade in {subject} has improved from {current_grade:.1f} to {new_grade:.1f}!"
                    )
                    points_gain = int(random.randint(5, 10) * relationship_gain_mult)
                else:
                    if personality == "kuudere" or personality == "serious":
                        slow_print(
                            f"{Fore.RED}I believe in self-sufficiency. You should attempt this assignment on your own.{Style.RESET_ALL}"
                        )
                    elif personality == "lazy":
                        slow_print(
                            f"{Fore.RED}Ugh, homework? I haven't even done mine. Sorry, can't help.{Style.RESET_ALL}"
                        )
                    else:
                        slow_print(
                            f"{Fore.RED}I'd like to help, but I'm not very good at {subject} myself.{Style.RESET_ALL}"
                        )
                    points_gain = -int(random.randint(2, 5) * relationship_loss_mult)

        elif choice == "10" and relationship.get(name, 0) >= 80:  # Request a favor
            # Different favor options
            print("\nWhat kind of favor do you want to ask?")
            print("1. Help boost your reputation")
            print("2. Introduce you to someone")
            print("3. Help with a school project")
            print("4. Stand up for you against someone")
            print("5. Never mind")

            favor_choice = input("Choose a favor (1-5): ")

            if favor_choice == "5":
                slow_print("You decide not to ask for a favor after all.")
                points_gain = 0

            else:
                # Base chance depends on relationship and favor difficulty
                base_chance = min(0.8, relationship.get(name, 0) / 100)

                # Track favors if not already tracked
                if "favors_asked" not in player:
                    player["favors_asked"] = {}

                # Reduce chance if favors have been asked before
                if player["favors_asked"].get(name, 0) > 0:
                    base_chance -= 0.15 * player["favors_asked"].get(name, 0)

                # Process each favor type
                if favor_choice == "1":  # Reputation boost
                    if random.random() < base_chance:
                        rep_increase = random.randint(10, 25)
                        player["reputation"]["students"] += rep_increase

                        slow_print(
                            f"{Fore.GREEN}{name} speaks highly of you to other students, boosting your reputation!{Style.RESET_ALL}"
                        )
                        slow_print(f"Student Reputation +{rep_increase}")

                        # Track favor
                        player["favors_asked"][name] = (
                            player["favors_asked"].get(name, 0) + 1
                        )
                        points_gain = int(random.randint(3, 7) * relationship_gain_mult)
                    else:
                        slow_print(
                            f"{Fore.RED}I'm not sure I have that kind of influence with other students...{Style.RESET_ALL}"
                        )
                        points_gain = -int(
                            random.randint(3, 6) * relationship_loss_mult
                        )

                elif favor_choice == "2":  # Introduce to someone
                    # Find a student they know that you don't
                    potential_introductions = []
                    for student in students:
                        other_name = student["name"]
                        if other_name != name and other_name != player["name"]:
                            if (
                                other_name not in player["relationships"]
                                or player["relationships"][other_name] < 20
                            ):
                                potential_introductions.append(student)

                    if not potential_introductions or random.random() >= base_chance:
                        slow_print(
                            f"{Fore.RED}I don't really know anyone you haven't met already...{Style.RESET_ALL}"
                        )
                        points_gain = -int(
                            random.randint(2, 5) * relationship_loss_mult
                        )
                    else:
                        # Select a random student to introduce
                        intro_student = random.choice(potential_introductions)
                        intro_name = intro_student["name"]

                        slow_print(
                            f"{Fore.GREEN}{name} introduces you to {intro_name}!{Style.RESET_ALL}"
                        )
                        slow_print(
                            f"You have a pleasant first conversation with {intro_name}."
                        )

                        # Add relationship points with the new student
                        start_points = random.randint(15, 30)
                        player["relationships"][intro_name] = start_points

                        # Track favor
                        player["favors_asked"][name] = (
                            player["favors_asked"].get(name, 0) + 1
                        )
                        points_gain = int(
                            random.randint(5, 10) * relationship_gain_mult
                        )

                elif favor_choice == "3":  # School project help
                    if random.random() < base_chance:
                        # Intelligence boost
                        int_boost = random.randint(5, 15)
                        player["intelligence"] = min(
                            100, player["intelligence"] + int_boost
                        )

                        # Random subject grade boost
                        current_subjects = get_current_subjects()
                        if current_subjects:
                            subject = random.choice(current_subjects)
                            grade_boost = random.uniform(2.0, 5.0)
                            current_grade = player["grades"].get(subject, 60.0)
                            new_grade = min(100.0, current_grade + grade_boost)
                            player["grades"][subject] = new_grade

                            slow_print(
                                f"{Fore.GREEN}{name} agrees to help with your project! Their assistance is invaluable.{Style.RESET_ALL}"
                            )
                            slow_print(f"Intelligence +{int_boost}")
                            slow_print(
                                f"Your grade in {subject} improved from {current_grade:.1f} to {new_grade:.1f}!"
                            )
                        else:
                            slow_print(
                                f"{Fore.GREEN}{name} agrees to help with your project! Their assistance is invaluable.{Style.RESET_ALL}"
                            )
                            slow_print(f"Intelligence +{int_boost}")

                        # Teacher reputation boost
                        teacher_rep_boost = random.randint(5, 10)
                        player["reputation"]["teachers"] += teacher_rep_boost
                        slow_print(f"Teacher Reputation +{teacher_rep_boost}")

                        # Track favor
                        player["favors_asked"][name] = (
                            player["favors_asked"].get(name, 0) + 1
                        )
                        points_gain = int(
                            random.randint(6, 12) * relationship_gain_mult
                        )
                    else:
                        slow_print(
                            f"{Fore.RED}I'm really swamped with my own projects right now. Maybe next time?{Style.RESET_ALL}"
                        )
                        points_gain = -int(
                            random.randint(3, 7) * relationship_loss_mult
                        )

                elif favor_choice == "4":  # Stand up for you
                    if "bully_encounter" not in player:
                        player["bully_encounter"] = False

                    if not player["bully_encounter"]:
                        slow_print(
                            "There isn't currently anyone you need protection from."
                        )
                        points_gain = 0
                    elif random.random() < base_chance:
                        slow_print(
                            f"{Fore.GREEN}{name} agrees to stand up for you the next time someone gives you trouble!{Style.RESET_ALL}"
                        )
                        slow_print(
                            "You feel more confident knowing you have their support."
                        )

                        # Stress reduction from having backup
                        stress_reduction = random.randint(10, 20)
                        player["stress"] = max(0, player["stress"] - stress_reduction)
                        slow_print(f"Stress -{stress_reduction}")

                        # Reset bully encounter
                        player["bully_encounter"] = False

                        # Track favor
                        player["favors_asked"][name] = (
                            player["favors_asked"].get(name, 0) + 1
                        )
                        points_gain = int(
                            random.randint(8, 15) * relationship_gain_mult
                        )
                    else:
                        slow_print(
                            f"{Fore.RED}I... I'm not sure I can help with that. Confrontation isn't really my thing...{Style.RESET_ALL}"
                        )
                        points_gain = -int(
                            random.randint(4, 8) * relationship_loss_mult
                        )

        # Rumor/gossip interaction options
        elif (
            choice == "11"
            and student_status.get(name, "") == "Dating"
            and game_settings.get("allow_nsfw", False)
        ):
            # Process NSFW content based on relationship stage
            if relationship.get(name, 0) >= 90:  # Close bond required
                slow_print(
                    f"{Fore.MAGENTA}You and {name} spend some private time together...{Style.RESET_ALL}"
                )

                if personality == "shy" or personality == "dandere":
                    slow_print(
                        f"{name} blushes deeply but doesn't resist as you move closer..."
                    )
                elif personality == "genki" or personality == "deredere":
                    slow_print(
                        f"{name} enthusiastically embraces you, pulling you closer..."
                    )
                elif personality == "yandere":
                    slow_print(
                        f"{name}'s eyes gleam with intense passion as they pull you into their arms..."
                    )
                else:
                    slow_print("You both spend an intimate moment together...")

                slow_print(f"{Fore.MAGENTA}[Intimate content omitted]{Style.RESET_ALL}")
                points_gain = int(random.randint(8, 15) * relationship_gain_mult)
                decrease_stress(20)
                player["energy"] -= 15
            else:
                slow_print(f"{name} doesn't seem ready for that level of intimacy yet.")
                slow_print("You should work on building a stronger bond first.")
                points_gain = -int(random.randint(5, 10) * relationship_loss_mult)
                increase_stress(10)

        elif choice in ["12", "13", "14"] and relationship.get(name, 0) >= 50:
            # Handle rumor interactions (share gossip, ask about rumors, start rumor)
            # Call the specialized function that handles all rumor interaction types
            points_gain = handle_rumor_interaction(
                choice,
                name,
                personality,
                relationship_gain_mult,
                relationship_loss_mult,
            )

        # Make sure the relationship entry exists
        if name not in relationship:
            relationship[name] = 0
            
        # Apply personality-based relationship changes
        relationship[name] += points_gain

        # Ensure relationship doesn't go below 0
        if relationship[name] < 0:
            relationship[name] = 0

        new_status = get_relationship_status(relationship[name])
        if points_gain > 0 and new_status != current_status:
            slow_print(
                f"\n{Fore.CYAN}Your relationship has improved to: {new_status}!{Style.RESET_ALL}"
            )
        elif points_gain < 0 and new_status != current_status:
            slow_print(
                f"\n{Fore.RED}Your relationship has decreased to: {new_status}.{Style.RESET_ALL}"
            )

        # Ensure the student_status entry exists and is properly updated
        if name not in student_status:
            student_status[name] = new_status
        else:
            current_status_str = student_status.get(name, "")
            student_status[name] = (
                new_status
                if not current_status_str.startswith("Dating")
                else current_status_str
            )
        player["reputation"]["students"] += random.randint(1, 3)
        update_ranks()
    else:
        print("No student with that name.")


def show_relationship():
    print("\n--- Relationships ---")
    if not relationship:
        print("No relationships established yet.")
        return

    print("\nStudent Council:")
    for member in student_council:
        points = relationship.get(member["name"], 0)
        print(f"{member['name']} ({member['role']}) - Points: {points}")

    print("\nOther Students:")
    for student in students:
        if student["name"] in relationship:
            points = relationship.get(student["name"], 0)
            print(f"{student['name']} ({student['gender']}) - Points: {points}")


def study_subject(args):
    if not args:
        print("Usage: /study [subject]")
        return
    subject = " ".join(args).capitalize()
    if subject in subjects:
        homework[subject] = True
        slow_print(f"You studied {subject} and finished the homework!")
        player["charisma"]["academic"] += 1
    else:
        print("Unknown subject.")


def show_status():
    print(f"\n--- {player['name']}'s Status ---")
    print("Homework Completed:")
    for subj, done in homework.items():
        status = "✅" if done else "❌"
        print(f"{subj}: {status}")
    print("\nRelationships:")
    if relationship:
        for name, points in relationship.items():
            print(f"{name}: {points} points")
    else:
        print("No relationships yet.")
    show_me()


def show_homework():
    print("\n--- Homework ---")
    for subj, done in homework.items():
        status = "Done" if done else "Not Done"
        print(f"{subj}: {status}")


def show_teachers():
    print("\n--- Teachers ---")
    for teacher in teachers:
        print(f"{teacher['name']} - {teacher['subject']} ({teacher['personality']})")


def show_full_student_list():
    """Display the full list of 500-600 students in the school"""
    # Check if we have already generated the full student list
    if "full_student_list" not in player:
        # Generate the full student list
        player["full_student_list"] = generate_full_student_list()
        
    full_student_list = player["full_student_list"]
    total_students = len(full_student_list)
    
    print(f"\n{Fore.CYAN}=== FULL STUDENT DIRECTORY ({total_students} STUDENTS) ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Year 1: {len([s for s in full_student_list if s.get('year') == 1])} students{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Year 2: {len([s for s in full_student_list if s.get('year') == 2])} students{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Year 3: {len([s for s in full_student_list if s.get('year') == 3])} students{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Year 4: {len([s for s in full_student_list if s.get('year') == 4])} students{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}International: {len([s for s in full_student_list if s.get('is_international', False)])} students{Style.RESET_ALL}")
    
    # Count students by nationality
    nationality_counts = {}
    for student in full_student_list:
        nationality = student.get("nationality", "Unknown")
        if nationality in nationality_counts:
            nationality_counts[nationality] += 1
        else:
            nationality_counts[nationality] = 1
    
    print(f"\n{Fore.CYAN}=== NATIONALITIES ==={Style.RESET_ALL}")
    for nationality, count in sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{nationality}: {count} students")
    
    # Ask if the user wants to see the full list or filter
    while True:
        print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
        print("1. Show all students (warning: very long list)")
        print("2. Show students of a specific year")
        print("3. Show students of a specific nationality")
        print("4. Show students with a specific tag")
        print("5. Back to game")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            # Show all students in pages of 20
            print(f"\n{Fore.CYAN}=== ALL STUDENTS ({total_students}) ==={Style.RESET_ALL}")
            for i, student in enumerate(full_student_list, 1):
                name = student.get("name", "Unknown")
                year = student.get("year", 1)
                nationality = student.get("nationality", "Unknown")
                tags = ", ".join(student.get("tags", []))
                
                nationality_info = ""
                if student.get("is_international", False):
                    nationality_info = f" ({Fore.BLUE}{nationality}{Style.RESET_ALL})"
                    
                print(f"{i}. {name}{nationality_info} - Year {year} - Tags: {tags}")
                
                # Pause after every 20 students
                if i % 20 == 0 and i < total_students:
                    input("Press Enter to see more students...")
        
        elif choice == "2":
            year_choice = input("Enter year (1-4): ")
            try:
                year = int(year_choice)
                if 1 <= year <= 4:
                    year_students = [s for s in full_student_list if s.get("year") == year]
                    print(f"\n{Fore.CYAN}=== YEAR {year} STUDENTS ({len(year_students)}) ==={Style.RESET_ALL}")
                    
                    for i, student in enumerate(year_students, 1):
                        name = student.get("name", "Unknown")
                        nationality = student.get("nationality", "Unknown")
                        tags = ", ".join(student.get("tags", []))
                        
                        nationality_info = ""
                        if student.get("is_international", False):
                            nationality_info = f" ({Fore.BLUE}{nationality}{Style.RESET_ALL})"
                            
                        print(f"{i}. {name}{nationality_info} - Tags: {tags}")
                        
                        # Pause after every 20 students
                        if i % 20 == 0 and i < len(year_students):
                            input("Press Enter to see more students...")
                else:
                    print("Invalid year number. Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == "3":
            print(f"\n{Fore.CYAN}Available nationalities:{Style.RESET_ALL}")
            for nationality in sorted(nationality_counts.keys()):
                print(f"- {nationality} ({nationality_counts[nationality]} students)")
                
            nationality_choice = input("Enter nationality: ")
            if nationality_choice in nationality_counts:
                nationality_students = [s for s in full_student_list if s.get("nationality") == nationality_choice]
                print(f"\n{Fore.CYAN}=== {nationality_choice.upper()} STUDENTS ({len(nationality_students)}) ==={Style.RESET_ALL}")
                
                for i, student in enumerate(nationality_students, 1):
                    name = student.get("name", "Unknown")
                    year = student.get("year", 1)
                    tags = ", ".join(student.get("tags", []))
                    
                    print(f"{i}. {name} - Year {year} - Tags: {tags}")
                    
                    # Pause after every 20 students
                    if i % 20 == 0 and i < len(nationality_students):
                        input("Press Enter to see more students...")
            else:
                print("Invalid nationality.")
        
        elif choice == "4":
            # Gather all possible tags
            all_tags = set()
            for student in full_student_list:
                for tag in student.get("tags", []):
                    all_tags.add(tag)
            
            print(f"\n{Fore.CYAN}Available tags:{Style.RESET_ALL}")
            for tag in sorted(all_tags):
                tag_count = len([s for s in full_student_list if tag in s.get("tags", [])])
                print(f"- {tag} ({tag_count} students)")
                
            tag_choice = input("Enter tag: ")
            if tag_choice in all_tags:
                tagged_students = [s for s in full_student_list if tag_choice in s.get("tags", [])]
                print(f"\n{Fore.CYAN}=== STUDENTS WITH TAG '{tag_choice}' ({len(tagged_students)}) ==={Style.RESET_ALL}")
                
                for i, student in enumerate(tagged_students, 1):
                    name = student.get("name", "Unknown")
                    year = student.get("year", 1)
                    nationality = student.get("nationality", "Unknown")
                    tags = ", ".join(student.get("tags", []))
                    
                    nationality_info = ""
                    if student.get("is_international", False):
                        nationality_info = f" ({Fore.BLUE}{nationality}{Style.RESET_ALL})"
                        
                    print(f"{i}. {name}{nationality_info} - Year {year} - Tags: {tags}")
                    
                    # Pause after every 20 students
                    if i % 20 == 0 and i < len(tagged_students):
                        input("Press Enter to see more students...")
            else:
                print("Invalid tag.")
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def show_npc_list(args):
    """Display NPCs filtered by tag"""
    # Check if we have already generated the full student list
    if "full_student_list" not in player:
        # Generate the full student list
        player["full_student_list"] = generate_full_student_list()
        
    full_student_list = player["full_student_list"]
    
    # Include teachers and other NPCs in the full NPC list
    npcs = full_student_list.copy()
    
    # Add teachers to NPCs list with appropriate tags
    for teacher in teachers:
        teacher_name = teacher.get("name", "Unknown")
        subject = teacher.get("subject", "Unknown")
        
        # Create tags for teachers
        teacher_tags = ["teacher", "faculty"]
        if subject:
            teacher_tags.append(f"{subject.lower().replace(' ', '_')}_teacher")
            
        teacher_info = {
            "name": teacher_name,
            "role": "Teacher",
            "subject": subject,
            "tags": teacher_tags,
            "nationality": "Japanese"  # Default, could be changed if teacher data includes nationality
        }
        
        npcs.append(teacher_info)
    
    # Add club presidents with the "club_president" tag if not already there
    for president in club_presidents:
        # Check if already in the list
        president_in_list = False
        for npc in npcs:
            if npc.get("name") == president.get("name"):
                # Add club_president tag if not already there
                if "club_president" not in npc.get("tags", []):
                    npc.setdefault("tags", []).append("club_president")
                president_in_list = True
                break
                
        if not president_in_list:
            president_info = {
                "name": president.get("name", "Unknown"),
                "role": "Club President",
                "club": president.get("club", "Unknown"),
                "tags": ["student", "club_president"],
                "nationality": "Japanese"  # Default
            }
            npcs.append(president_info)
    
    # Gather all possible NPC tags
    all_tags = set()
    for npc in npcs:
        for tag in npc.get("tags", []):
            all_tags.add(tag)
    
    # Handle command arguments
    if args:
        tag_filter = args[0].lower()
        
        if tag_filter in all_tags:
            # Filter NPCs by the specified tag
            filtered_npcs = [npc for npc in npcs if tag_filter in npc.get("tags", [])]
            
            print(f"\n{Fore.CYAN}=== NPCs WITH TAG '{tag_filter}' ({len(filtered_npcs)}) ==={Style.RESET_ALL}")
            
            for i, npc in enumerate(filtered_npcs, 1):
                name = npc.get("name", "Unknown")
                role = npc.get("role", "Student")
                nationality = npc.get("nationality", "Unknown")
                
                # Add special info based on role
                extra_info = ""
                if role == "Teacher":
                    extra_info = f" - Subject: {npc.get('subject', 'Unknown')}"
                elif role == "Club President":
                    extra_info = f" - Club: {npc.get('club', 'Unknown')}"
                elif "year" in npc:
                    extra_info = f" - Year {npc.get('year', 1)}"
                
                # Show nationality for international NPCs
                nationality_info = ""
                if npc.get("is_international", False):
                    nationality_info = f" ({Fore.BLUE}{nationality}{Style.RESET_ALL})"
                
                # Show relationship if exists
                relationship_info = ""
                if name in relationship:
                    rel_points = relationship.get(name, 0)
                    rel_status = student_status.get(name, "Unknown")
                    relationship_info = f" - {rel_status} ({rel_points} points)"
                
                print(f"{i}. {name}{nationality_info} - {role}{extra_info}{relationship_info}")
                
                # Pause after every 20 NPCs
                if i % 20 == 0 and i < len(filtered_npcs):
                    input("Press Enter to see more NPCs...")
        else:
            print(f"No NPCs found with tag '{tag_filter}'.")
            print(f"\n{Fore.CYAN}Available tags:{Style.RESET_ALL}")
            for tag in sorted(all_tags):
                tag_count = len([npc for npc in npcs if tag in npc.get("tags", [])])
                print(f"- {tag} ({tag_count} NPCs)")
    else:
        # No tag specified, show available tags
        print(f"\n{Fore.CYAN}=== NPC TAGS ==={Style.RESET_ALL}")
        print("Please specify a tag to filter NPCs.")
        print("Usage: /npc list [tag]")
        print(f"\n{Fore.CYAN}Available tags:{Style.RESET_ALL}")
        
        for tag in sorted(all_tags):
            tag_count = len([npc for npc in npcs if tag in npc.get("tags", [])])
            print(f"- {tag} ({tag_count} NPCs)")

def show_students():
    print(f"\n{Fore.CYAN}=== YOUR CLASSMATES ==={Style.RESET_ALL}")
    
    # Filter students for player's year
    classmates = [s for s in students if s.get("year", 1) == player["school_year"]]
    
    if not classmates:
        print("You don't have any classmates yet.")
        return
    
    for student in classmates:
        name = student.get("name", "Unknown")
        rel_points = relationship.get(name, 0)
        rel_status = student_status.get(name, "Unknown")
        
        # Check if they're a club president
        club_info = ""
        if student.get("is_club_president", False):
            club_info = f" ({Fore.MAGENTA}President of {student['club']}{Style.RESET_ALL})"
            
        # Display nationality for international students
        nationality_info = ""
        if student.get("is_international", False):
            nationality_info = f" ({Fore.BLUE}{student.get('nationality', 'International')}{Style.RESET_ALL})"
            
        print(f"{name}{nationality_info} - {rel_status} ({rel_points} points){club_info}")
        
        # If high enough relationship, show more details
        if rel_points >= 50:
            personality = student.get("personality", "unknown")
            print(f"  Personality: {personality}")
            
            # Show compatibility if available
            if "compatibility" in student:
                compatibility = student["compatibility"]
                print(f"  Compatibility: {compatibility}%")


def show_quests():
    print("\n--- Quests ---")
    if not quests:
        print("No active quests.")
        return
    for quest in quests:
        status = "Completed" if quest["completed"] else "Active"
        print(f"{quest['description']} - {quest['objective']} ({status})")


def complete_quest(args):
    if not args:
        print("Usage: /complete_quest [quest_id]")
        return
    quest_id = int(args[0])
    quest = next((q for q in quests if q["id"] == quest_id), None)
    if quest and not quest["completed"]:
        quest["completed"] = True
        slow_print(
            f"Quest '{quest['description']}' completed! You earned {quest['reward']} relationship points."
        )
        for student in students:
            if student["name"] == quest["description"].split()[1]:  # E.g., Haruki
                relationship[student["name"]] = relationship.get(student["name"], 0) + quest["reward"]
                player["reputation"]["students"] += quest["reward"]
                update_ranks()
    else:
        print("Quest not found or already completed.")


# Function to handle club mechanics
def handle_club_location(club_name):
    """Handle interactions when visiting a club location"""
    if club_name in player["clubs"]:
        # Already a member
        position = player["club_positions"].get(club_name, "Member")
        president = clubs[club_name]["president"]

        slow_print(f"{Fore.CYAN}Welcome back to the {club_name}!{Style.RESET_ALL}")

        # Get club benefits
        benefits = clubs[club_name]["benefits"]

        # Apply subject bonus if applicable
        for subject, bonus in benefits.items():
            if subject in subjects:
                if not homework.get(subject, False):
                    homework[subject] = True
                    slow_print(
                        f"You worked on your {subject} homework with club members!"
                    )

        # Apply charisma and reputation benefits
        if "charisma" in benefits:
            for skill, value in benefits["charisma"].items():
                player["charisma"][skill] += value
                slow_print(
                    f"Your {skill} skills improved by being at the club! (+{value})"
                )

        # Reduce stress
        if "stress_reduction" in benefits:
            reduction = benefits["stress_reduction"]
            player["stress"] = max(0, player["stress"] - reduction)
            slow_print(
                f"Spending time at the club helped you relax! (-{reduction} stress)"
            )

        # Consume energy
        if "energy_cost" in benefits:
            player["energy"] = max(0, player["energy"] - benefits["energy_cost"])
            slow_print(
                f"Club activities made you tired. (-{benefits['energy_cost']} energy)"
            )

        # Chance to become president if not already and relationship with current president is high
        if (
            position != "President"
            and relationship.get(president, 0) >= 80
        ):
            if random.random() < 0.1:  # 10% chance
                clubs[club_name]["president"] = player["name"]
                player["club_positions"][club_name] = "President"
                slow_print(
                    f"{Fore.GREEN}Congratulations! You've been elected as the new President of {club_name}!{Style.RESET_ALL}"
                )

                # Unlock achievement
                if "Club Leader" not in player["achievements"]:
                    player["achievements"].append("Club Leader")
                    slow_print(
                        f"{Fore.YELLOW}Achievement unlocked: Club Leader{Style.RESET_ALL}"
                    )
    else:
        # Not a member yet
        slow_print(f"{Fore.CYAN}You visit the {club_name}.{Style.RESET_ALL}")
        slow_print(
            f"The club is currently in session. {clubs[club_name]['president']} is leading the activities."
        )
        slow_print(f"Club description: {clubs[club_name]['description']}")

        join = input(f"Would you like to join the {club_name}? (y/n): ").lower()
        if join == "y":
            if len(player["clubs"]) < 2:  # Limit to 2 clubs
                player["clubs"].append(club_name)
                player["club_positions"][club_name] = "Member"
                clubs[club_name]["members"].append(player["name"])
                slow_print(
                    f"{Fore.GREEN}You are now a member of the {club_name}!{Style.RESET_ALL}"
                )
                player["reputation"]["students"] += 5
                update_ranks()

                # Unlock achievement for joining first club
                if (
                    len(player["clubs"]) == 1
                    and "Club Member" not in player["achievements"]
                ):
                    player["achievements"].append("Club Member")
                    slow_print(
                        f"{Fore.YELLOW}Achievement unlocked: Club Member{Style.RESET_ALL}"
                    )
            else:
                slow_print(
                    f"{Fore.RED}You can only join a maximum of 2 clubs.{Style.RESET_ALL}"
                )
                leave_club = input(
                    "Would you like to leave one of your current clubs? (y/n): "
                ).lower()
                if leave_club == "y":
                    print("Your current clubs:")
                    for i, club in enumerate(player["clubs"], 1):
                        print(f"{i}. {club}")
                    choice = input(
                        "Enter the number of the club you want to leave (or 0 to cancel): "
                    )
                    if choice.isdigit() and 1 <= int(choice) <= len(player["clubs"]):
                        old_club = player["clubs"][int(choice) - 1]
                        player["clubs"].remove(old_club)
                        clubs[old_club]["members"].remove(player["name"])
                        slow_print(f"You left the {old_club}.")

                        # Now join the new club
                        player["clubs"].append(club_name)
                        player["club_positions"][club_name] = "Member"
                        clubs[club_name]["members"].append(player["name"])
                        slow_print(
                            f"{Fore.GREEN}You are now a member of the {club_name}!{Style.RESET_ALL}"
                        )
                        player["reputation"]["students"] += 5
                        update_ranks()


# Function for PE class challenges
def pe_class_challenge():
    """Handle PE class challenges in the gym with enhanced narrative"""
    if "PE" not in player["electives"] and random.random() < 0.7:
        # Less likely to have PE challenges if not taking PE as elective
        return

    slow_print(
        "\n{0}=== PE Class Challenge ==={1}".format(Fore.YELLOW, Style.RESET_ALL)
    )
    
    # Check the current season to apply seasonal effects
    season = get_current_season()
    
    # Inform about seasonal conditions
    if season == "summer":
        slow_print(f"{Fore.YELLOW}It's a hot summer day. The gym feels particularly warm today.{Style.RESET_ALL}")
        
        # Check if player has the "strong" trait
        if "strong" in player.get("traits", []):
            slow_print(f"{Fore.GREEN}Your strength helps you handle the summer heat better.{Style.RESET_ALL}")
        elif "heat_sensitive" in player.get("traits", []):
            slow_print(f"{Fore.RED}You find the heat particularly difficult to deal with.{Style.RESET_ALL}")
        else:
            slow_print(f"{Fore.YELLOW}The heat makes physical activities more challenging.{Style.RESET_ALL}")
    
    elif season == "winter":
        slow_print(f"{Fore.CYAN}It's cold outside, but the gym is adequately heated.{Style.RESET_ALL}")
        
        # Check if player has the "cold_sensitive" trait
        if "cold_sensitive" in player.get("traits", []):
            slow_print(f"{Fore.RED}Even in the heated gym, you find it hard to warm up properly.{Style.RESET_ALL}")
    
    # Apply special energy costs based on season and traits
    seasonal_energy_cost = 0
    if season == "summer":
        if "heat_sensitive" in player.get("traits", []):
            seasonal_energy_cost = 10
            player["energy"] = max(0, player["energy"] - seasonal_energy_cost)
            slow_print(f"{Fore.RED}The heat is draining your energy faster. (-{seasonal_energy_cost} Energy){Style.RESET_ALL}")
        elif "strong" not in player.get("traits", []):
            seasonal_energy_cost = 5
            player["energy"] = max(0, player["energy"] - seasonal_energy_cost)
            slow_print(f"{Fore.YELLOW}The summer heat is making you tired more quickly. (-{seasonal_energy_cost} Energy){Style.RESET_ALL}")
    
    elif season == "winter" and "cold_sensitive" in player.get("traits", []):
        seasonal_energy_cost = 7
        player["energy"] = max(0, player["energy"] - seasonal_energy_cost)
        slow_print(f"{Fore.RED}You're spending extra energy just trying to stay warm. (-{seasonal_energy_cost} Energy){Style.RESET_ALL}")

    # Expanded challenges with more detailed narratives
    challenges = [
        {
            "name": "Sprint Race",
            "difficulty": 3,
            "description": "Race against your classmates in a 100-meter sprint.",
            "prep_narrative": [
                "The class lines up at the starting line, a mix of excitement and nervousness in the air.",
                "You stretch your legs and take deep breaths, focusing on the track ahead.",
                "The PE teacher holds the whistle to her lips, waiting for everyone to get ready.",
            ],
            "success_narrative": [
                "You explode off the starting line with perfect form, your legs pumping rhythmically.",
                "The wind rushes past your face as you maintain your speed through the middle section.",
                "With a final burst of energy, you cross the finish line ahead of most of your classmates.",
            ],
            "great_success_narrative": [
                "Your start is impeccable, pushing off with explosive power that surprises even yourself.",
                "You find yourself in 'the zone', every movement fluid and efficient as you pull ahead.",
                "As you cross the finish line well ahead of the others, even the PE teacher looks impressed.",
                "A few classmates come over to ask about your training routine.",
            ],
            "failure_narrative": [
                "Your reaction time at the start is a fraction too slow, putting you behind immediately.",
                "You try to make up ground but find your energy draining faster than expected.",
                "By the time you cross the finish line, most of your classmates are already catching their breath.",
            ],
        },
        {
            "name": "Basketball Game",
            "difficulty": 4,
            "description": "Play a quick basketball game with your classmates.",
            "prep_narrative": [
                "The class divides into two teams, with you joining the blue team.",
                "Everyone takes their positions on the court as the teacher explains the rules for today's game.",
                "You wipe your palms on your gym clothes, ready to give it your best effort.",
            ],
            "success_narrative": [
                "You find yourself in good positions throughout the game, making several accurate passes.",
                "When the ball comes your way, you manage to score a clean basket that earns approving nods.",
                "Your defensive moves prevent the opposing team from scoring several times.",
            ],
            "great_success_narrative": [
                "You play with unexpected confidence, calling for passes and making strategic moves.",
                "A perfectly executed three-pointer from your hand draws cheers from your teammates.",
                "In the final moments, you intercept a pass and drive to the basket for a game-winning shot.",
                "Even students from other classes who were watching applaud your performance.",
            ],
            "failure_narrative": [
                "The ball seems to slip from your grasp more often than not today.",
                "You misjudge a pass and send the ball out of bounds, leading to groans from teammates.",
                "Despite your efforts, you can't seem to find your rhythm during the game.",
            ],
        },
        {
            "name": "Swimming Relay",
            "difficulty": 5,
            "description": "Compete in a swimming relay race against other teams.",
            "prep_narrative": [
                "In the echoing school pool area, the class divides into relay teams of four.",
                "You adjust your swimming goggles and cap, mentally preparing for your leg of the relay.",
                "The chlorine scent fills your nostrils as you watch the first swimmers take their positions.",
            ],
            "success_narrative": [
                "When your turn comes, you dive cleanly into the water with minimal splash.",
                "Your strokes are strong and even, propelling you through the water efficiently.",
                "You touch the wall with good timing, allowing your teammate to start with a slight advantage.",
            ],
            "great_success_narrative": [
                "Your dive is perfectly executed, giving you a fraction of a second advantage immediately.",
                "Your swimming technique is flawless today - each stroke powerful yet controlled.",
                "You finish your leg of the relay significantly ahead of the competing teams.",
                "Your teammates cheer wildly as you climb out, some patting you on the back for your contribution.",
            ],
            "failure_narrative": [
                "Your dive is slightly off-angle, causing you to go deeper than intended.",
                "You struggle to find your rhythm in the water, your breathing becoming uneven.",
                "By the time you reach the wall, your team has fallen behind, and you can sense the disappointment.",
            ],
        },
        {
            "name": "Volleyball Match",
            "difficulty": 3,
            "description": "Play a volleyball match against another class.",
            "prep_narrative": [
                "Your class lines up against students from Class 2-B for today's volleyball match.",
                "The teacher reviews proper serving and receiving techniques before the game begins.",
                "You take your position on the court, watching the server from the opposing team carefully.",
            ],
            "success_narrative": [
                "You manage several good returns, your positioning on the court consistently solid.",
                "A well-timed spike from your hand earns a point and high-fives from your teammates.",
                "Throughout the game, you communicate well with your team, calling out incoming balls.",
            ],
            "great_success_narrative": [
                "You play as if volleyball has always been your favorite sport, every move precise.",
                "An incredible diving save from you keeps a critical point alive, leading to your team scoring.",
                "Your serves are particularly powerful today, causing the opposing team obvious difficulty.",
                "After the match, even the opposing team compliments your play.",
            ],
            "failure_narrative": [
                "The volleyball seems to always come toward you at awkward angles today.",
                "Your serve hits the net twice in a row, causing you to flush with embarrassment.",
                "Despite your best efforts, you miss a crucial easy return that costs your team a point.",
            ],
        },
        {
            "name": "Fitness Test",
            "difficulty": 2,
            "description": "Complete a series of fitness exercises to test your overall condition.",
            "prep_narrative": [
                "The PE teacher explains today's fitness assessment: push-ups, sit-ups, flexibility, and the beep test.",
                "Students around you look either confident or nervous as they prepare for the challenge.",
                "You do some quick warm-up stretches, mentally preparing for each element of the test.",
            ],
            "success_narrative": [
                "You perform each exercise with good form, completing a respectable number of repetitions.",
                "Your flexibility test goes particularly well, showing above-average results.",
                "During the beep test, you maintain a steady pace that gets you through most levels.",
            ],
            "great_success_narrative": [
                "Your push-up and sit-up counts exceed even your own expectations today.",
                "In the flexibility test, you reach further than almost anyone else in the class.",
                "During the beep test, you're among the last few students still running, showing exceptional endurance.",
                "The PE teacher makes notes on your performance, clearly impressed by your fitness level.",
            ],
            "failure_narrative": [
                "Your push-ups lack proper form, with the teacher correcting you several times.",
                "The sit-ups leave you winded far earlier than you expected.",
                "During the beep test, you drop out earlier than most, your stamina failing you today.",
            ],
        },
    ]

    # Select a random challenge
    challenge = random.choice(challenges)

    # Display challenge info with enhanced formatting
    slow_print(
        "\n{0}Today's Challenge: {1}{2}".format(
            Fore.CYAN, challenge["name"], Style.RESET_ALL
        )
    )
    slow_print(
        "{0}Description: {1}{2}".format(
            Fore.CYAN, challenge["description"], Style.RESET_ALL
        )
    )
    slow_print("")

    # Display preparation narrative
    slow_print("{0}=== Setting the Scene ==={1}".format(Fore.MAGENTA, Style.RESET_ALL))
    for line in challenge["prep_narrative"]:
        slow_print(line)
        time.sleep(0.3)  # Brief pause between narrative lines

    slow_print("")  # Empty line for spacing

    # Print a prompt to build anticipation
    slow_print("{0}The challenge begins...{1}".format(Fore.YELLOW, Style.RESET_ALL))
    time.sleep(1)  # Dramatic pause

    # Challenge success is based on player's energy, PE stats, traits, season, social charisma, and some randomness
    pe_skill_factor = (player["pe_stats"]["technique"] / 10) * 0.2 + (
        player["pe_stats"]["stamina"] / 10
    ) * 0.2
    
    # Base success chance
    base_success_chance = (
        (player["energy"] / 100) * 0.4
        + pe_skill_factor
        + (player["charisma"]["social"] / 10) * 0.1
        + random.random() * 0.1
    )
    
    # Apply trait bonuses/penalties
    trait_modifier = 0
    for trait in player.get("traits", []):
        if trait == "athletic":
            trait_modifier += 0.15  # Athletic trait gives 15% bonus
            slow_print(f"{Fore.GREEN}Your athletic trait gives you a natural advantage. (+15% success chance){Style.RESET_ALL}")
        elif trait == "strong" and season == "summer":
            trait_modifier += 0.1  # Strong trait helps in summer heat
            slow_print(f"{Fore.GREEN}Your strength helps you overcome the summer heat. (+10% success chance){Style.RESET_ALL}")
        elif trait == "fast" and challenge["name"] == "Sprint Race":
            trait_modifier += 0.2  # Fast trait helps in sprints
            slow_print(f"{Fore.GREEN}Your natural speed gives you an edge in the sprint. (+20% success chance){Style.RESET_ALL}")
        elif trait == "clumsy":
            trait_modifier -= 0.1  # Clumsy trait is a penalty
            slow_print(f"{Fore.RED}Your clumsiness makes this more challenging. (-10% success chance){Style.RESET_ALL}")
        elif trait == "weak":
            trait_modifier -= 0.05  # Weak trait is a small penalty
            slow_print(f"{Fore.RED}Your lower strength is a slight disadvantage. (-5% success chance){Style.RESET_ALL}")
            
    # Apply seasonal penalties if applicable
    if season == "summer" and "strong" not in player.get("traits", []):
        if "heat_sensitive" in player.get("traits", []):
            trait_modifier -= 0.2  # Heat sensitive in summer is a big penalty
            slow_print(f"{Fore.RED}The summer heat severely impacts your performance. (-20% success chance){Style.RESET_ALL}")
        else:
            trait_modifier -= 0.1  # Regular summer penalty without strong trait
            slow_print(f"{Fore.RED}The heat is making this more difficult. (-10% success chance){Style.RESET_ALL}")
    
    elif season == "winter" and "cold_sensitive" in player.get("traits", []):
        trait_modifier -= 0.15  # Cold sensitive in winter is a penalty
        slow_print(f"{Fore.RED}The cold weather makes it hard for you to perform well. (-15% success chance){Style.RESET_ALL}")
    
    # Apply trait modifier to success chance
    success_chance = base_success_chance + trait_modifier
    
    # Show trait impact if significant
    if abs(trait_modifier) > 0.05:
        if trait_modifier > 0:
            slow_print(f"{Fore.GREEN}Your traits are helping your performance significantly!{Style.RESET_ALL}")
        else:
            slow_print(f"{Fore.RED}Your traits are making this challenge more difficult.{Style.RESET_ALL}")
    
    difficulty_factor = challenge["difficulty"] / 5  # Normalize difficulty to 0-1 range

    if success_chance > difficulty_factor:
        result = "success"

        # Greater success if significantly above difficulty
        if success_chance > difficulty_factor + 0.3:
            result = "great_success"
    else:
        result = "failure"

    # Display narrative based on result
    slow_print("\n{0}=== Challenge Results ==={1}".format(Fore.YELLOW, Style.RESET_ALL))

    # Display result and apply effects
    if result == "great_success":
        # Show great success narrative
        for line in challenge["great_success_narrative"]:
            slow_print("{0}{1}{2}".format(Fore.GREEN, line, Style.RESET_ALL))
            time.sleep(0.3)

        # Apply great success effects
        reputation_gain_students = random.randint(3, 6)
        reputation_gain_teachers = random.randint(2, 4)
        charisma_gain = 2

        player["reputation"]["students"] += reputation_gain_students
        player["reputation"]["teachers"] += reputation_gain_teachers
        player["grades"]["PE"] = "A"  # Set PE grade to A
        player["charisma"]["social"] += charisma_gain
        player["pe_stats"]["technique"] += 1  # Improve technique with great success
        player["pe_stats"]["stamina"] += 1  # Improve stamina with great success

        # Show rewards summary
        slow_print(
            "\n{0}=== Challenge Rewards ==={1}".format(Fore.YELLOW, Style.RESET_ALL)
        )
        slow_print("• Student Reputation: +{0}".format(reputation_gain_students))
        slow_print("• Teacher Reputation: +{0}".format(reputation_gain_teachers))
        slow_print("• Social Charisma: +{0}".format(charisma_gain))
        slow_print("• PE Grade: A")
        slow_print("• PE Technique: +1")
        slow_print("• PE Stamina: +1")

        # Chance to unlock achievement
        if "PE Champion" not in player["achievements"]:
            player["achievements"].append("PE Champion")
            slow_print(
                "\n{0}Achievement unlocked: PE Champion{1}".format(
                    Fore.YELLOW, Style.RESET_ALL
                )
            )

    elif result == "success":
        # Show success narrative
        for line in challenge["success_narrative"]:
            slow_print("{0}{1}{2}".format(Fore.CYAN, line, Style.RESET_ALL))
            time.sleep(0.3)

        # Apply success effects
        reputation_gain_students = random.randint(1, 3)
        reputation_gain_teachers = 1
        charisma_gain = 1

        player["reputation"]["students"] += reputation_gain_students
        player["reputation"]["teachers"] += reputation_gain_teachers
        player["charisma"]["social"] += charisma_gain

        # Show rewards summary
        slow_print(
            "\n{0}=== Challenge Rewards ==={1}".format(Fore.YELLOW, Style.RESET_ALL)
        )
        slow_print("• Student Reputation: +{0}".format(reputation_gain_students))
        slow_print("• Teacher Reputation: +{0}".format(reputation_gain_teachers))
        slow_print("• Social Charisma: +{0}".format(charisma_gain))

        # Random chance to improve a PE stat
        if random.random() < 0.5:
            player["pe_stats"]["technique"] += 1
            slow_print("• PE Technique: +1")
        else:
            player["pe_stats"]["stamina"] += 1
            slow_print("• PE Stamina: +1")

        # Improve PE grade if not already A
        if player["grades"].get("PE", "C") != "A":
            current_grade = player["grades"].get("PE", "C")
            new_grade = chr(max(ord(current_grade) - 1, ord("A")))
            player["grades"]["PE"] = new_grade
            slow_print("• PE Grade improved to {0}".format(new_grade))

    else:  # failure
        # Show failure narrative
        for line in challenge["failure_narrative"]:
            slow_print("{0}{1}{2}".format(Fore.RED, line, Style.RESET_ALL))
            time.sleep(0.3)

        # Apply failure effects
        reputation_loss = random.randint(0, 2)
        player["reputation"]["students"] -= reputation_loss

        # Show effects summary
        slow_print(
            "\n{0}=== Challenge Effects ==={1}".format(Fore.YELLOW, Style.RESET_ALL)
        )
        if reputation_loss > 0:
            slow_print("• Student Reputation: -{0}".format(reputation_loss))

        # PE grade might decrease if not already F
        if player["grades"].get("PE", "C") != "F":
            current_grade = player["grades"].get("PE", "C")
            new_grade = chr(min(ord(current_grade) + 1, ord("F")))
            player["grades"]["PE"] = new_grade
            slow_print("• PE Grade dropped to {0}".format(new_grade))

        # Small chance to still improve stamina from the effort
        if random.random() < 0.3:
            player["pe_stats"]["stamina"] += 1
            slow_print("• Despite the struggle, your stamina improved: +1")

    # Regardless of outcome, PE challenges use energy
    energy_cost = 10 + (challenge["difficulty"] * 3)
    hunger_cost = 5 + challenge["difficulty"]
    stress_change = random.randint(3, 8)  # Physical activities add some stress

    player["energy"] = max(0, player["energy"] - energy_cost)
    player["hunger"] = max(0, player["hunger"] - hunger_cost)
    player["stress"] = min(100, player["stress"] + stress_change)

    slow_print(
        "\n{0}The challenge was physically demanding:{1}".format(
            Fore.CYAN, Style.RESET_ALL
        )
    )
    slow_print("• Energy: -{0}".format(energy_cost))
    slow_print("• Hunger: -{0}".format(hunger_cost))
    slow_print("• Stress: +{0}".format(stress_change))

    # Chance for a special interaction with another student
    if random.random() < 0.3:  # 30% chance
        slow_print(
            "\n{0}=== After the Challenge ==={1}".format(Fore.MAGENTA, Style.RESET_ALL)
        )

        random_student = random.choice(students)
        student_name = random_student["name"]

        if result == "great_success":
            slow_print("{0} approaches you after class.".format(student_name))
            slow_print(
                '"That was amazing! Do you play {0} outside of school too?"'.format(
                    challenge["name"].lower()
                )
            )
            player["reputation"]["students"] += 2

            # Add or improve relationship
            if student_name not in relationship:
                relationship[student_name] = 10
            else:
                relationship[student_name] = min(100, relationship[student_name] + 10)

            slow_print("You've made a good impression on {0}!".format(student_name))

        elif result == "success":
            slow_print(
                "You notice {0} giving you an approving nod after the challenge.".format(
                    student_name
                )
            )

            # Add or improve relationship slightly
            if student_name not in relationship:
                relationship[student_name] = 5
            else:
                relationship[student_name] = min(100, relationship[student_name] + 5)

        else:  # failure
            slow_print("{0} comes over and pats you on the back.".format(student_name))
            slow_print(
                "\"Don't worry about it. We all have off days. You'll do better next time!\""
            )

            # Add or improve relationship for their kindness
            if student_name not in relationship:
                relationship[student_name] = 8
            else:
                relationship[student_name] = min(100, relationship[student_name] + 8)

            slow_print("You appreciate {0}'s encouragement.".format(student_name))

    update_ranks()


# Function for romance opportunities
def romance_opportunity():
    """Create opportunities for romantic interactions"""
    # Skip if player already has a romantic interest and relationship is strong
    if (
        player["romantic_interest"]
        and player["romantic_interest"] in relationship
        and relationship.get(player["romantic_interest"], 0) > 75
    ):
        if random.random() < 0.8:  # 80% chance to skip
            return

    # Find eligible students for romance
    eligible_students = []
    for student in students:
        # Only consider students of the gender the player might be interested in
        # For simplicity, assuming opposite gender attraction, but this could be expanded
        if student["gender"] != player["gender"]:
            # Add students with high relationship points or interesting personality
            if student["name"] in relationship and relationship.get(student["name"], 0) >= 30:
                eligible_students.append(student)
            elif (
                student["personality"] in ["kind", "serious"] and random.random() < 0.3
            ):
                eligible_students.append(student)

    if not eligible_students:
        return  # No eligible students found

    # Select a student for the romantic event
    romantic_interest = random.choice(eligible_students)
    name = romantic_interest["name"]

    # Initialize relationship if not exists
    if name not in relationship:
        relationship[name] = 20  # Start with some interest

    # Different scenarios based on current relationship level
    rel_points = relationship.get(name, 0)

    if rel_points < 40:  # Early stage - initial interest
        slow_print(
            f"\n{Fore.MAGENTA}You notice {name} glancing at you from across the room.{Style.RESET_ALL}"
        )

        options = ["Smile back", "Wave hello", "Look away", "Approach them"]

        print("How do you respond?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Choose an option (1-4): ")
        if choice == "1":
            slow_print(f"You smile back at {name}. They smile too.")
            relationship[name] += random.randint(3, 5)
        elif choice == "2":
            slow_print(f"You wave hello to {name}. They wave back, looking pleased.")
            relationship[name] += random.randint(4, 6)
        elif choice == "3":
            slow_print(
                f"You look away. When you glance back, {name} seems disappointed."
            )
            relationship[name] -= random.randint(1, 3)
        elif choice == "4":
            slow_print(f"You approach {name} and start a conversation.")
            dialogue = analyze_student_response(romantic_interest, "player")
            slow_print(f'{name}: "{dialogue}"')
            relationship[name] += random.randint(5, 8)
            player["charisma"]["social"] += 1

    elif rel_points < 70:  # Middle stage - growing interest
        scenario = random.choice(
            [
                f"{name} asks if you'd like to study together after school.",
                f"You run into {name} at the cafeteria, and they invite you to sit together.",
                f"{name} compliments something about you.",
            ]
        )

        slow_print(f"\n{Fore.MAGENTA}{scenario}{Style.RESET_ALL}")

        options = [
            "Accept enthusiastically",
            "Accept casually",
            "Politely decline",
            "Flirt back",
        ]

        print("How do you respond?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Choose an option (1-4): ")
        if choice == "1":
            slow_print(
                f"You enthusiastically accept {name}'s gesture. They seem very happy."
            )
            relationship[name] += random.randint(6, 9)
        elif choice == "2":
            slow_print(f"You casually accept. {name} seems pleased.")
            relationship[name] += random.randint(4, 7)
        elif choice == "3":
            slow_print(
                f"You politely decline. {name} tries to hide their disappointment."
            )
            relationship[name] -= random.randint(3, 6)
        elif choice == "4":
            slow_print(f"You flirt back. {name} blushes and seems very interested.")
            relationship[name] += random.randint(7, 10)
            player["charisma"]["social"] += 1

    elif rel_points < 90:  # Advanced stage - possible relationship
        if not player["romantic_interest"]:
            slow_print(
                f"\n{Fore.MAGENTA}{name} has been spending a lot of time with you lately.{Style.RESET_ALL}"
            )
            slow_print(f"You sense that {name} might have feelings for you.")

            options = [
                "Ask them on a date",
                "Wait for them to make a move",
                "Keep things friendly",
                "Confess your feelings",
            ]

            print("What will you do?")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            choice = input("Choose an option (1-4): ")
            if choice == "1":
                slow_print(f"You ask {name} on a date. They happily accept!")
                relationship[name] += random.randint(8, 12)
                player["romantic_interest"] = name

                # Unlock achievement
                if "Romance Blooms" not in player["achievements"]:
                    player["achievements"].append("Romance Blooms")
                    slow_print(
                        f"{Fore.YELLOW}Achievement unlocked: Romance Blooms{Style.RESET_ALL}"
                    )

            elif choice == "2":
                slow_print(
                    f"You decide to wait. {name} seems a bit uncertain about your feelings."
                )
                relationship[name] += random.randint(2, 5)

            elif choice == "3":
                slow_print(
                    f"You keep things friendly. {name} seems slightly disappointed."
                )
                relationship[name] -= random.randint(4, 8)

            elif choice == "4":
                slow_print(f"You confess your feelings to {name}.")

                # Success chance based on charisma and some randomness
                success_chance = (
                    player["charisma"]["social"] / 50
                ) + random.random() * 0.5

                if success_chance > 0.6:
                    slow_print(
                        f"{Fore.GREEN}{name} feels the same way! You're now dating!{Style.RESET_ALL}"
                    )
                    relationship[name] += random.randint(15, 20)
                    player["romantic_interest"] = name
                    student_status[name] = "Dating"

                    # Unlock achievement
                    if "Romance Blooms" not in player["achievements"]:
                        player["achievements"].append("Romance Blooms")
                        slow_print(
                            f"{Fore.YELLOW}Achievement unlocked: Romance Blooms{Style.RESET_ALL}"
                        )
                else:
                    slow_print(
                        f"{Fore.RED}{name} appreciates your feelings but wants to remain friends for now.{Style.RESET_ALL}"
                    )
                    relationship[name] -= random.randint(5, 10)

    elif player["romantic_interest"] == name:  # In a relationship
        scenario = random.choice(
            [
                f"{name} brings you a small gift.",
                f"{name} asks if you want to go somewhere together on the weekend.",
                f"You and {name} have a quiet moment together between classes.",
            ]
        )

        slow_print(f"\n{Fore.MAGENTA}{scenario}{Style.RESET_ALL}")

        options = [
            "Share your feelings",
            "Suggest a date location",
            "Ask about their day",
            "Give a small gift",
        ]

        print("How do you respond?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Choose an option (1-4): ")

        relationship[name] += random.randint(
            5, 10
        )  # Always gain points when in a relationship
        player["stress"] = max(
            0, player["stress"] - random.randint(5, 10)
        )  # Reduce stress

        slow_print(f"You and {name} grow closer. Your stress level decreases.")


# Function to check for special events and festivals
# Festival minigames function
def play_festival_minigame(minigame_type):
    """Play a festival-specific minigame"""
    slow_print(
        "\n{0}=== Festival Minigame: {1} ==={2}".format(
            Fore.CYAN, minigame_type.replace("_", " ").title(), Style.RESET_ALL
        )
    )

    # Poetry Contest Minigame (Cherry Blossom Festival)
    if minigame_type == "poetry_contest":
        slow_print("Welcome to the Cherry Blossom Poetry Contest!")
        slow_print(
            "Create a poem by selecting words that fit the theme of spring and cherry blossoms."
        )

        themes = ["beauty", "nature", "transience", "renewal", "pink petals"]
        theme = random.choice(themes)
        slow_print(f"Your theme is: {theme}")

        word_sets = {
            "nouns": [
                "blossoms",
                "spring",
                "breeze",
                "petals",
                "sunlight",
                "branches",
                "dawn",
                "dreams",
                "path",
                "garden",
            ],
            "verbs": [
                "floating",
                "dancing",
                "falling",
                "blooming",
                "whispering",
                "awakening",
                "drifting",
                "embracing",
                "shimmering",
            ],
            "adjectives": [
                "gentle",
                "pink",
                "delicate",
                "fleeting",
                "serene",
                "peaceful",
                "radiant",
                "ephemeral",
                "tender",
            ],
        }

        # Player selects words
        poem_words = []
        for category in ["nouns", "verbs", "adjectives"]:
            print(f"\nChoose two {category}:")
            options = word_sets[category]
            for i, word in enumerate(options, 1):
                print(f"{i}. {word}")

            for _ in range(2):
                choice = input(f"Select a {category[:-1]} (1-{len(options)}): ")
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(options):
                        poem_words.append(options[index])
                    else:
                        poem_words.append(random.choice(options))
                except ValueError:
                    poem_words.append(random.choice(options))

        # Generate poem using selected words
        poem_structures = [
            "{adj1} {noun1}, {verb1} in the {adj2} {noun2}, {verb2} with the wind.",
            "The {adj1} {noun1} {verb1}, as {adj2} {noun2} {verb2} in harmony.",
            "{verb1} {adj1} {noun1}, {verb2} like {adj2} {noun2} in spring.",
            "{adj1} are the {noun1} that {verb1}, {adj2} are the {noun2} that {verb2}.",
        ]

        poem_template = random.choice(poem_structures)
        final_poem = poem_template.format(
            adj1=poem_words[4],
            adj2=poem_words[5],
            noun1=poem_words[0],
            noun2=poem_words[1],
            verb1=poem_words[2],
            verb2=poem_words[3],
        )

        slow_print("\n{0}Your poem:{1}".format(Fore.YELLOW, Style.RESET_ALL))
        slow_print("{0}{1}{2}".format(Fore.CYAN, final_poem, Style.RESET_ALL))

        # Judge poem based on theme
        theme_words = {
            "beauty": [
                "delicate",
                "radiant",
                "pink",
                "gentle",
                "petals",
                "blossoms",
                "shimmering",
            ],
            "nature": [
                "garden",
                "branches",
                "breeze",
                "spring",
                "blooming",
                "petals",
                "sunlight",
            ],
            "transience": [
                "fleeting",
                "ephemeral",
                "falling",
                "drifting",
                "dreams",
                "tender",
            ],
            "renewal": [
                "awakening",
                "blooming",
                "dawn",
                "spring",
                "path",
                "embracing",
                "new",
            ],
            "pink petals": [
                "pink",
                "petals",
                "blossoms",
                "floating",
                "falling",
                "delicate",
                "dancing",
            ],
        }

        score = 0
        for word in poem_words:
            if word in theme_words[theme]:
                score += 10

        # Bonus points for creativity
        score += random.randint(0, 30)

        slow_print(f"\nThe judges have scored your poem: {score} points!")

        if score >= 70:
            slow_print(
                f"{Fore.GREEN}Congratulations! Your poem won first place!{Style.RESET_ALL}"
            )
            reward_money = 1000
            stress_reduction = 20
            charisma_gain = 2
        elif score >= 50:
            slow_print(
                f"{Fore.CYAN}Well done! Your poem won second place!{Style.RESET_ALL}"
            )
            reward_money = 500
            stress_reduction = 15
            charisma_gain = 1
        else:
            slow_print("Thank you for participating in the poetry contest!")
            reward_money = 200
            stress_reduction = 10
            charisma_gain = 0

        player["money"] += reward_money
        player["stress"] = max(0, player["stress"] - stress_reduction)
        player["charisma"]["academic"] += charisma_gain

        slow_print(
            f"You earned ¥{reward_money}, reduced stress by {stress_reduction}, and gained {charisma_gain} academic charisma!"
        )

    # Goldfish Scooping Minigame (Summer Cultural Festival)
    elif minigame_type == "goldfish_scooping":
        slow_print("Welcome to Kingyo-sukui (Goldfish Scooping)!")
        slow_print(
            "You have a paper scoop (poi) to catch as many goldfish as you can before it breaks."
        )

        # Game parameters
        scoop_health = 100  # Paper scoop durability
        caught_fish = 0
        total_attempts = 0
        max_attempts = 10

        slow_print(
            f"Your paper scoop has {scoop_health}% durability. Catch as many goldfish as you can!"
        )

        while scoop_health > 0 and total_attempts < max_attempts:
            total_attempts += 1

            print(
                f"\nAttempt {total_attempts}/{max_attempts} - Scoop durability: {scoop_health}%"
            )
            print("1. Quick scoop (Low risk, 5-20% damage)")
            print("2. Medium scoop (Medium risk, 10-30% damage)")
            print("3. Big scoop (High risk, 20-50% damage)")

            choice = input("Choose your scooping technique (1-3): ")

            # Determine damage and success chance based on technique
            if choice == "1":
                success_chance = 0.7
                damage = random.randint(5, 20)
                fish_caught = 1
            elif choice == "2":
                success_chance = 0.5
                damage = random.randint(10, 30)
                fish_caught = 2
            elif choice == "3":
                success_chance = 0.3
                damage = random.randint(20, 50)
                fish_caught = 3
            else:
                success_chance = 0.5
                damage = random.randint(10, 30)
                fish_caught = 1

            # Determine success
            if random.random() < success_chance:
                caught_fish += fish_caught
                slow_print(
                    f"{Fore.GREEN}Success! You caught {fish_caught} goldfish!{Style.RESET_ALL}"
                )
            else:
                slow_print(f"{Fore.RED}The fish got away!{Style.RESET_ALL}")
                damage += 5  # Extra damage for failed attempt

            # Apply damage to scoop
            scoop_health -= damage
            slow_print(f"Your scoop took {damage}% damage.")

            if scoop_health <= 0:
                slow_print(f"{Fore.RED}Your paper scoop broke!{Style.RESET_ALL}")

        slow_print(
            f"\n{Fore.CYAN}Game Over! You caught {caught_fish} goldfish in total!{Style.RESET_ALL}"
        )

        # Determine rewards based on performance
        reward_money = caught_fish * 50
        stress_reduction = min(30, caught_fish * 3)
        social_charisma = min(3, caught_fish // 3)

        player["money"] += reward_money
        player["stress"] = max(0, player["stress"] - stress_reduction)
        player["charisma"]["social"] += social_charisma

        slow_print(
            f"You earned ¥{reward_money}, reduced stress by {stress_reduction}, and gained {social_charisma} social charisma!"
        )

        # Special prize for high performance
        if caught_fish >= 8:
            slow_print(
                f"{Fore.YELLOW}The stall owner gives you a special prize for your excellent performance!{Style.RESET_ALL}"
            )
            player["festival_achievements"].append("Goldfish Master")
            player["charisma"]["social"] += 2

    # Tanzaku Wish Minigame (Tanabata Festival)
    elif minigame_type == "tanzaku_wish":
        slow_print("Welcome to Tanzaku Wish Writing!")
        slow_print("Write your wish on colorful paper and hang it on the bamboo tree.")

        wish_categories = [
            "Academic Success",
            "Romantic Love",
            "Friendship",
            "Health",
            "Wealth",
            "Personal Growth",
        ]

        print("\nChoose a category for your wish:")
        for i, category in enumerate(wish_categories, 1):
            print(f"{i}. {category}")

        choice = input("Select a category (1-6): ")
        try:
            category_index = int(choice) - 1
            if 0 <= category_index < len(wish_categories):
                chosen_category = wish_categories[category_index]
            else:
                chosen_category = random.choice(wish_categories)
        except ValueError:
            chosen_category = random.choice(wish_categories)

        slow_print(f"\nYou have chosen to make a wish for: {chosen_category}")

        wish_elements = {
            "Academic Success": [
                "studying",
                "learning",
                "tests",
                "homework",
                "grades",
                "knowledge",
                "wisdom",
            ],
            "Romantic Love": [
                "romance",
                "love",
                "dating",
                "partner",
                "relationship",
                "heart",
                "feelings",
            ],
            "Friendship": [
                "friends",
                "bonds",
                "trust",
                "memories",
                "support",
                "fun",
                "laughter",
            ],
            "Health": [
                "body",
                "mind",
                "spirit",
                "strength",
                "energy",
                "healing",
                "balance",
            ],
            "Wealth": [
                "money",
                "fortune",
                "abundance",
                "success",
                "prosperity",
                "career",
                "opportunity",
            ],
            "Personal Growth": [
                "growth",
                "skills",
                "talent",
                "confidence",
                "courage",
                "creativity",
                "passion",
            ],
        }

        print("\nCreate your wish by selecting keywords:")
        options = wish_elements[chosen_category]
        for i, word in enumerate(options, 1):
            print(f"{i}. {word}")

        wish_keywords = []
        for i in range(3):
            keyword_choice = input(f"Select keyword {i+1} (1-{len(options)}): ")
            try:
                index = int(keyword_choice) - 1
                if 0 <= index < len(options):
                    wish_keywords.append(options[index])
                else:
                    wish_keywords.append(random.choice(options))
            except ValueError:
                wish_keywords.append(random.choice(options))

        # Create wish based on selected keywords
        wish_templates = [
            "I wish for {kw1}, {kw2}, and {kw3} in my life.",
            "May I be blessed with {kw1}, filled with {kw2}, and surrounded by {kw3}.",
            "I hope to achieve {kw1}, discover {kw2}, and embrace {kw3}.",
            "Let the stars grant me {kw1}, guide me to {kw2}, and inspire {kw3}.",
        ]

        final_wish = random.choice(wish_templates).format(
            kw1=wish_keywords[0], kw2=wish_keywords[1], kw3=wish_keywords[2]
        )

        slow_print(f"\n{Fore.CYAN}Your Tanzaku wish:{Style.RESET_ALL}")
        slow_print(f"{Fore.YELLOW}{final_wish}{Style.RESET_ALL}")

        # Hanging the wish on the bamboo
        slow_print("\nYou carefully hang your colorful wish on the bamboo tree...")
        slow_print(
            f"{Fore.MAGENTA}The night sky seems to twinkle in response to your wish!{Style.RESET_ALL}"
        )

        # Category-specific rewards
        if chosen_category == "Academic Success":
            player["charisma"]["academic"] += 2
            slow_print("You feel inspired to study harder! (+2 Academic Charisma)")
        elif chosen_category == "Romantic Love":
            # Boost romance chances
            for student in students:
                if student["name"] in relationship:
                    relationship[student["name"]] += 5
            slow_print(
                "Your heart feels lighter! (+5 points with all romantic interests)"
            )
        elif chosen_category == "Friendship":
            player["charisma"]["social"] += 2
            player["reputation"]["students"] += 10
            slow_print(
                "You feel more connected to your friends! (+2 Social Charisma, +10 Student Reputation)"
            )
        elif chosen_category == "Health":
            player["health"] += 15
            player["energy"] += 20
            slow_print("You feel refreshed and healthy! (+15 Health, +20 Energy)")
        elif chosen_category == "Wealth":
            bonus = random.randint(500, 1500)
            player["money"] += bonus
            slow_print(f"You found ¥{bonus} on your way home! What luck!")
        elif chosen_category == "Personal Growth":
            player["charisma"]["academic"] += 1
            player["charisma"]["social"] += 1
            player["pe_stats"]["technique"] += 1
            slow_print(
                "You feel a surge of personal growth! (+1 to Academic, Social, and Technique)"
            )

        # Universal rewards
        player["stress"] = max(0, player["stress"] - 15)
        slow_print("Writing your wish was therapeutic! (-15 Stress)")

        # Special achievement
        player["festival_achievements"].append("Star-Wisher")
        slow_print(f"{Fore.YELLOW}Achievement Unlocked: Star-Wisher{Style.RESET_ALL}")

    # Bean Throwing Minigame (Setsubun Festival)
    elif minigame_type == "bean_throwing":
        slow_print("Welcome to Setsubun Bean Throwing!")
        slow_print("Throw beans to chase away the oni (demons) and bring good fortune!")

        # Game parameters
        beans_left = 10
        oni_defeated = 0
        demon_types = ["Red Oni", "Blue Oni", "Yellow Oni", "Purple Oni", "Black Oni"]

        slow_print(f"You have {beans_left} beans. Aim carefully to hit the demons!")

        while beans_left > 0:
            # Spawn a random demon
            current_demon = random.choice(demon_types)
            demon_difficulty = demon_types.index(current_demon) + 1
            demon_health = demon_difficulty * 2

            slow_print(
                f"\n{Fore.RED}A {current_demon} appears! (Difficulty: {demon_difficulty}/5){Style.RESET_ALL}"
            )

            while demon_health > 0 and beans_left > 0:
                print(f"Beans left: {beans_left} | Demon health: {demon_health}")
                print("1. Throw carefully (Higher accuracy, uses 1 bean)")
                print("2. Throw handful (Lower accuracy, uses 3 beans)")
                print("3. Shout 'Oni wa soto, fuku wa uchi!' (Bonus damage if you hit)")

                choice = input("Choose your action (1-3): ")

                # Determine action results
                if choice == "1":
                    beans_used = 1
                    hit_chance = 0.8 - (demon_difficulty * 0.1)
                    damage = 1
                elif choice == "2":
                    beans_used = min(3, beans_left)
                    hit_chance = 0.6 - (demon_difficulty * 0.05)
                    damage = random.randint(1, beans_used)
                else:  # choice == "3"
                    beans_used = 1
                    hit_chance = 0.7 - (demon_difficulty * 0.1)
                    damage = 2  # Bonus damage when shouting the traditional phrase

                beans_left -= beans_used

                # Determine if hit was successful
                if random.random() < hit_chance:
                    demon_health -= damage
                    if choice == "3":
                        slow_print(
                            f"{Fore.YELLOW}'Oni wa soto, fuku wa uchi!' (Demons out, luck in!){Style.RESET_ALL}"
                        )
                    slow_print(
                        f"{Fore.GREEN}Hit! You dealt {damage} damage to the {current_demon}!{Style.RESET_ALL}"
                    )
                else:
                    slow_print(
                        f"{Fore.RED}Miss! The {current_demon} dodged your beans!{Style.RESET_ALL}"
                    )

                if demon_health <= 0:
                    slow_print(
                        f"{Fore.GREEN}You defeated the {current_demon}!{Style.RESET_ALL}"
                    )
                    oni_defeated += 1
                    break

                if beans_left <= 0:
                    slow_print(
                        f"{Fore.RED}You're out of beans! The {current_demon} escapes!{Style.RESET_ALL}"
                    )
                    break

            # Check if game should continue
            if beans_left <= 0:
                break

            # Ask if player wants to continue
            if beans_left > 0:
                continue_choice = input(
                    f"You have {beans_left} beans left. Continue throwing? (y/n): "
                )
                if continue_choice.lower() != "y":
                    break

        slow_print(
            f"\n{Fore.CYAN}Game Over! You defeated {oni_defeated} oni!{Style.RESET_ALL}"
        )

        # Determine rewards based on performance
        fortune_bonus = oni_defeated * 100
        stress_reduction = oni_defeated * 5

        # Apply rewards
        player["money"] += fortune_bonus
        player["stress"] = max(0, player["stress"] - stress_reduction)

        slow_print(f"Your good fortune brought you ¥{fortune_bonus}!")
        slow_print(f"Defeating the oni reduced your stress by {stress_reduction}!")

        # Special achievement for high performance
        if oni_defeated >= 5:
            slow_print(
                f"{Fore.YELLOW}Achievement Unlocked: Oni Vanquisher{Style.RESET_ALL}"
            )
            player["festival_achievements"].append("Oni Vanquisher")
            player["reputation"]["students"] += 10
            slow_print(
                "Your victory against the oni has impressed your fellow students! (+10 Student Reputation)"
            )

    # Bon Odori Dance Minigame (Obon Festival)
    elif minigame_type == "bon_odori":
        slow_print("Welcome to the Bon Odori Dance Circle!")
        slow_print(
            "Follow the rhythm and dance patterns to honor the spirits of ancestors."
        )

        # Game parameters
        dance_moves = [
            "Step Right",
            "Step Left",
            "Turn",
            "Clap",
            "Bow",
            "Raise Arms",
            "Wave Fan",
        ]
        dance_sequence = []
        player_sequence = []
        sequence_length = 3
        max_rounds = 5
        current_round = 1
        score = 0

        slow_print("\nWatch the dance sequence and then repeat it!")

        while current_round <= max_rounds:
            # Generate dance sequence
            dance_sequence = [
                random.choice(dance_moves) for _ in range(sequence_length)
            ]

            # Show sequence
            slow_print(
                f"\n{Fore.YELLOW}Round {current_round}: Watch the sequence...{Style.RESET_ALL}"
            )
            for move in dance_sequence:
                slow_print(f"{move}...")
                time.sleep(0.7)

            # Clear screen equivalent
            print("\n" * 5)

            # Ask player to repeat
            slow_print(f"{Fore.CYAN}Now repeat the sequence!{Style.RESET_ALL}")
            player_sequence = []

            for i in range(sequence_length):
                print("\nAvailable moves:")
                for j, move in enumerate(dance_moves, 1):
                    print(f"{j}. {move}")

                choice = input(f"Move {i+1}/{sequence_length}: ")
                try:
                    move_index = int(choice) - 1
                    if 0 <= move_index < len(dance_moves):
                        player_sequence.append(dance_moves[move_index])
                    else:
                        player_sequence.append(random.choice(dance_moves))
                except ValueError:
                    player_sequence.append(random.choice(dance_moves))

            # Check accuracy
            correct_moves = sum(
                1 for p, d in zip(player_sequence, dance_sequence) if p == d
            )
            round_score = (correct_moves / sequence_length) * 100
            score += round_score

            # Feedback
            slow_print(
                f"\n{Fore.YELLOW}Original sequence: {', '.join(dance_sequence)}{Style.RESET_ALL}"
            )
            slow_print(
                f"{Fore.CYAN}Your sequence: {', '.join(player_sequence)}{Style.RESET_ALL}"
            )
            slow_print(
                f"You got {correct_moves}/{sequence_length} moves correct ({round_score:.0f}% accuracy)!"
            )

            if correct_moves == sequence_length:
                slow_print(
                    f"{Fore.GREEN}Perfect! The spirits are pleased with your dance!{Style.RESET_ALL}"
                )
            elif correct_moves >= sequence_length / 2:
                slow_print(
                    f"{Fore.YELLOW}Good effort! The spirits appreciate your dance.{Style.RESET_ALL}"
                )
            else:
                slow_print(
                    f"{Fore.RED}The spirits seem a bit confused by your dance...{Style.RESET_ALL}"
                )

            # Increase difficulty
            if current_round < max_rounds:
                sequence_length += 1

            current_round += 1

        # Calculate final score
        final_score = score / max_rounds
        slow_print(
            f"\n{Fore.CYAN}Dance complete! Your average accuracy was {final_score:.0f}%!{Style.RESET_ALL}"
        )

        # Determine rewards based on performance
        if final_score >= 80:
            energy_bonus = 30
            stress_reduction = 25
            social_charisma = 3
            slow_print(
                f"{Fore.GREEN}The spirits were deeply moved by your dance!{Style.RESET_ALL}"
            )
        elif final_score >= 60:
            energy_bonus = 20
            stress_reduction = 15
            social_charisma = 2
            slow_print(
                f"{Fore.YELLOW}Your dance honored the ancestors well.{Style.RESET_ALL}"
            )
        else:
            energy_bonus = 10
            stress_reduction = 10
            social_charisma = 1
            slow_print("Your participation in the dance was appreciated.")

        # Apply rewards
        player["energy"] += energy_bonus
        player["stress"] = max(0, player["stress"] - stress_reduction)
        player["charisma"]["social"] += social_charisma

        slow_print(
            f"Dancing gave you energy (+{energy_bonus}) and reduced your stress (-{stress_reduction})!"
        )
        slow_print(f"Your dancing improved your social charisma (+{social_charisma})!")

        # Special achievement for high performance
        if final_score >= 90:
            slow_print(
                f"{Fore.YELLOW}Achievement Unlocked: Spirit Dancer{Style.RESET_ALL}"
            )
            player["festival_achievements"].append("Spirit Dancer")

    # Implement other minigames as needed
    else:
        slow_print(
            f"The {minigame_type.replace('_', ' ').title()} minigame is still being prepared for the festival!"
        )

    return True


def interact_ex_partner(ex_partner):
    """
    Handle interactions with ex-partners, including yandere therapy

    Arguments:
    ex_partner -- Dictionary containing ex-partner information
    """
    name = ex_partner["name"]
    status = ex_partner["status"]

    # Display ex-partner info
    print(f"\n{Fore.CYAN}================================{Style.RESET_ALL}")
    print(f"           {name}")
    print(f"Status: Ex-Partner ({EX_PARTNER_STATUSES[status]['description']})")
    print(f"Breakup Date: {ex_partner.get('breakup_date', 'Unknown')}")
    print("================================")

    # Display general options
    print("1. Chat about feelings")
    print("2. Apologize for past")
    print("3. Suggest friendship")

    # Reconciliation option
    if status in ["moved_on", "still_interested"]:
        print("4. Suggest getting back together")

    # Special therapy option for yandere
    if status == "yandere":
        print(f"{Fore.MAGENTA}5. Suggest therapy/counseling{Style.RESET_ALL}")

    print(f"================================{Style.RESET_ALL}")

    choice = input(f"\n{Fore.GREEN}Choose an option:{Style.RESET_ALL} ")

    if choice == "1":  # Chat about feelings
        slow_print(f"You engage {name} in a conversation about your past relationship.")

        if status == "moved_on":
            slow_print(
                f"{name}: I appreciate your maturity in talking about this. I've moved on, and I hope you're doing well too."
            )
            # Small chance of status change
            if random.random() < 0.1:
                ex_partner["status"] = "still_interested"
                slow_print(
                    f"{Fore.CYAN}(You notice a hint of lingering feelings in their eyes){Style.RESET_ALL}"
                )

        elif status == "still_interested":
            slow_print(
                f"{name}: It's... nice to talk about what we had. I still think about us sometimes."
            )

            # Chance they might make a move
            if random.random() < 0.3:
                slow_print(
                    f"{name} moves closer to you, hesitating as if wanting to say more."
                )
                respond = input("Encourage them to speak? (Y/N): ").upper()

                if respond == "Y":
                    slow_print(
                        f"{name}: I still have feelings for you. I've been hoping we might try again someday."
                    )
                    reconcile = input("Suggest reconciliation? (Y/N): ").upper()

                    if reconcile == "Y":
                        # Similar logic to reconciliation option
                        if player["romantic_interest"]:
                            slow_print(
                                f"You're currently in a relationship with {player['romantic_interest']}."
                            )
                            break_up = input(
                                f"End your relationship with {player['romantic_interest']}? (Y/N): "
                            ).upper()

                            if break_up == "Y":
                                # Handle breakup and reconciliation
                                current = player["romantic_interest"]

                                # Add current partner to ex-partners
                                new_ex = {
                                    "name": current,
                                    "status": "angry",
                                    "breakup_date": current_date.strftime("%Y-%m-%d"),
                                }
                                player["ex_partners"].append(new_ex)

                                # Update player's romantic status
                                player["romantic_interest"] = name
                                player["romance_stage"] = 4
                                player["romance_points"] = ROMANCE_STAGES[4]["req"]

                                # Remove this person from ex-partners
                                player["ex_partners"].remove(ex_partner)

                                slow_print(
                                    f"{Fore.GREEN}You and {name} decide to give your relationship another chance.{Style.RESET_ALL}"
                                )
                                slow_print(
                                    f"You've broken up with {current} to be with {name} again."
                                )
                            else:
                                slow_print(
                                    f"You tell {name} that you're committed to your current relationship."
                                )
                                slow_print(
                                    f"{name} looks disappointed but nods in understanding."
                                )

                                # Worsen status
                                ex_partner["status"] = "angry"
                        else:
                            # Not currently dating anyone
                            player["romantic_interest"] = name
                            player["romance_stage"] = 4
                            player["romance_points"] = ROMANCE_STAGES[4]["req"]

                            # Remove from ex-partners
                            player["ex_partners"].remove(ex_partner)

                            slow_print(
                                f"{Fore.GREEN}You and {name} are back together!{Style.RESET_ALL}"
                            )
                    else:
                        slow_print(
                            f"You gently tell {name} that you value them but aren't looking to get back together."
                        )
                        slow_print(f"{name} looks disappointed but tries to hide it.")

                        # May change status
                        if random.random() < 0.4:
                            ex_partner["status"] = "angry"
                else:
                    slow_print(
                        f"You keep the conversation casual. {name} seems slightly disappointed."
                    )

        elif status == "angry":
            slow_print(
                f"{name}: *coldly* I don't really want to talk about our past. It's better left behind us."
            )

            # Chance of status improvement
            if random.random() < 0.2:
                ex_partner["status"] = "moved_on"
                slow_print(
                    f"{Fore.CYAN}(Despite their words, they seem less angry than before){Style.RESET_ALL}"
                )

        elif status == "yandere":
            slow_print(
                f"{name}: *intense stare* Our relationship isn't in the past. It's just on pause. We'll be together again... one way or another."
            )
            slow_print(
                f"{Fore.RED}Their intensity makes you uncomfortable.{Style.RESET_ALL}"
            )

            # Increase mental health stress
            player["mental_health"]["anxiety"] = min(
                100, player["mental_health"]["anxiety"] + 5
            )
            increase_stress(5)

    elif choice == "2":  # Apologize
        slow_print(
            f"You sincerely apologize to {name} for any hurt you caused in your relationship."
        )

        if status == "moved_on":
            slow_print(
                f"{name}: I appreciate that, thank you. It's all water under the bridge now."
            )
            # Improve status and potentially add to friends
            if random.random() < 0.7:
                if name not in player["relationships"]:
                    player["relationships"][name] = 30  # Start as acquaintance
                slow_print(f"{name} seems glad to be on better terms with you.")

        elif status == "still_interested":
            slow_print(
                f"{name}: Your apology means a lot to me. I've never stopped caring about you."
            )

            # Chance of reconciliation suggestion
            if random.random() < 0.4:
                slow_print(f"{name}: Do you think... we could try again?")
                respond = input("Consider getting back together? (Y/N): ").upper()

                if respond == "Y":
                    # Similar reconciliation logic
                    if player["romantic_interest"]:
                        slow_print(
                            f"You're currently in a relationship with {player['romantic_interest']}."
                        )
                        break_up = input(
                            f"End your relationship with {player['romantic_interest']}? (Y/N): "
                        ).upper()

                        if break_up == "Y":
                            # Handle breakup and reconciliation (similar to chat option)
                            current = player["romantic_interest"]

                            # Add current partner to ex-partners
                            new_ex = {
                                "name": current,
                                "status": "angry",
                                "breakup_date": current_date.strftime("%Y-%m-%d"),
                            }
                            player["ex_partners"].append(new_ex)

                            # Update player's romantic status
                            player["romantic_interest"] = name
                            player["romance_stage"] = 4
                            player["romance_points"] = ROMANCE_STAGES[4]["req"]

                            # Remove this person from ex-partners
                            player["ex_partners"].remove(ex_partner)

                            slow_print(
                                f"{Fore.GREEN}You and {name} decide to give your relationship another chance.{Style.RESET_ALL}"
                            )
                            slow_print(
                                f"You've broken up with {current} to be with {name} again."
                            )
                        else:
                            slow_print(
                                f"You tell {name} that while you care about them, you're committed to your current relationship."
                            )
                            slow_print(
                                f"{name} looks heartbroken but nods in understanding."
                            )

                            # Worsen status potentially
                            if random.random() < 0.5:
                                ex_partner["status"] = "angry"
                    else:
                        # Not currently dating anyone
                        player["romantic_interest"] = name
                        player["romance_stage"] = 4
                        player["romance_points"] = ROMANCE_STAGES[4]["req"]

                        # Remove from ex-partners
                        player["ex_partners"].remove(ex_partner)

                        slow_print(
                            f"{Fore.GREEN}You and {name} decide to give your relationship another chance!{Style.RESET_ALL}"
                        )
                else:
                    slow_print(
                        f"You tell {name} that you value their forgiveness but think it's best to move forward separately."
                    )

                    # May change status
                    if random.random() < 0.5:
                        ex_partner["status"] = "angry"
                        slow_print(f"{name} looks hurt by your rejection.")
                    else:
                        ex_partner["status"] = "moved_on"
                        slow_print(f"{name} accepts your decision with grace.")

        elif status == "angry":
            # Chance of accepting apology
            if random.random() < 0.6:
                slow_print(
                    f"{name}: *sighs* I guess I appreciate the apology. It's been a while anyway."
                )
                ex_partner["status"] = "moved_on"
                slow_print(
                    f"{Fore.GREEN}{name} seems to have let go of some anger toward you.{Style.RESET_ALL}"
                )
            else:
                slow_print(
                    f"{name}: An apology doesn't change what happened. I need more time."
                )
                slow_print(
                    f"{Fore.YELLOW}{name} is still upset, but your apology didn't make things worse.{Style.RESET_ALL}"
                )

        elif status == "yandere":
            slow_print(
                f"{name}: *smiles unsettlingly* There's nothing to apologize for. We'll be together again soon anyway."
            )
            slow_print(
                f"{Fore.RED}Their response makes you deeply uncomfortable.{Style.RESET_ALL}"
            )
            player["mental_health"]["anxiety"] = min(
                100, player["mental_health"]["anxiety"] + 7
            )
            increase_stress(8)

    elif choice == "3":  # Suggest friendship
        slow_print(
            f"You suggest to {name} that you could try to be friends despite your history."
        )

        if status == "moved_on":
            slow_print(f"{name}: I think that sounds healthy. I'd like that.")

            # Add to relationships if not already there
            if name not in player["relationships"]:
                player["relationships"][name] = 40  # Start as friend
            else:
                player["relationships"][name] = max(40, player["relationships"][name])

            slow_print(
                f"{Fore.GREEN}You and {name} have established a friendship.{Style.RESET_ALL}"
            )

        elif status == "still_interested":
            slow_print(
                f"{name}: *hesitates* I can try, but it might be difficult for me to see you just as a friend."
            )

            # Add to relationships but with a lower starting value
            if name not in player["relationships"]:
                player["relationships"][name] = 30  # Start as acquaintance
            else:
                player["relationships"][name] = max(30, player["relationships"][name])

            slow_print(
                f"{Fore.YELLOW}You and {name} are working on building a friendship, though it may be complicated.{Style.RESET_ALL}"
            )

        elif status == "angry":
            # Chance of accepting friendship
            if random.random() < 0.4:
                slow_print(
                    f"{name}: *considers* I suppose we could try being civil. Baby steps."
                )

                ex_partner["status"] = "moved_on"

                if name not in player["relationships"]:
                    player["relationships"][name] = 20  # Start at a low level

                slow_print(
                    f"{Fore.YELLOW}{name} is cautiously open to rebuilding a connection.{Style.RESET_ALL}"
                )
            else:
                slow_print(
                    f"{name}: I don't think that's a good idea right now. I need more space."
                )
                slow_print(
                    f"{Fore.RED}{name} isn't ready for friendship yet.{Style.RESET_ALL}"
                )

        elif status == "yandere":
            slow_print(
                f"{name}: *laughs inappropriately* Friends? No, no. We're meant to be so much more than friends."
            )
            slow_print(
                f"{Fore.RED}They step uncomfortably close to you.{Style.RESET_ALL}"
            )
            slow_print('"Friends is such a weak word for what we are to each other."')

            player["mental_health"]["anxiety"] = min(
                100, player["mental_health"]["anxiety"] + 10
            )
            increase_stress(10)

    elif choice == "4" and status in ["moved_on", "still_interested"]:  # Reconciliation
        slow_print(
            f"You suggest to {name} that you might want to try your relationship again."
        )

        # Reconciliation chance varies by status
        reconcile_chance = EX_PARTNER_STATUSES[status]["reconciliation_chance"]

        # Bonus chance based on time passed and past relationship level
        days_since_breakup = 0
        if "breakup_date" in ex_partner:
            breakup_date = datetime.strptime(ex_partner["breakup_date"], "%Y-%m-%d")
            days_since_breakup = (current_date - breakup_date).days

        # More likely to reconcile if some time has passed (but not too much)
        if 7 <= days_since_breakup <= 90:
            reconcile_chance += 0.1

        if random.random() < reconcile_chance:
            # They want to reconcile
            if status == "moved_on":
                slow_print(
                    f"{name}: *surprised* Really? I... I've thought about it too, actually."
                )
            else:  # still_interested
                slow_print(f"{name}: *eyes light up* I've been hoping you'd say that!")

            # Check if player is currently in a relationship
            if player["romantic_interest"]:
                slow_print(
                    f"You're currently in a relationship with {player['romantic_interest']}."
                )
                break_up = input(
                    f"End your relationship with {player['romantic_interest']}? (Y/N): "
                ).upper()

                if break_up == "Y":
                    # Handle breakup and reconciliation
                    current = player["romantic_interest"]

                    # Add current partner to ex-partners
                    new_ex = {
                        "name": current,
                        "status": "angry",
                        "breakup_date": current_date.strftime("%Y-%m-%d"),
                    }
                    player["ex_partners"].append(new_ex)

                    # Update player's romantic status
                    player["romantic_interest"] = name
                    player["romance_stage"] = 4
                    player["romance_points"] = ROMANCE_STAGES[4]["req"]

                    # Remove this person from ex-partners
                    player["ex_partners"].remove(ex_partner)

                    slow_print(
                        f"{Fore.GREEN}You and {name} decide to give your relationship another chance.{Style.RESET_ALL}"
                    )
                    slow_print(
                        f"You've broken up with {current} to be with {name} again."
                    )
                else:
                    slow_print(
                        f"You tell {name} that you can't end your current relationship."
                    )
                    slow_print(
                        f'{name} looks deeply hurt. "So why did you bring this up?"'
                    )

                    # Worsen status
                    ex_partner["status"] = "angry"
            else:
                # Not currently dating anyone
                player["romantic_interest"] = name
                player["romance_stage"] = 4
                player["romance_points"] = ROMANCE_STAGES[4]["req"]

                # Remove from ex-partners
                player["ex_partners"].remove(ex_partner)

                slow_print(
                    f"{Fore.GREEN}You and {name} are back together!{Style.RESET_ALL}"
                )
                decrease_stress(15)
                player["mental_health"]["happiness"] = min(
                    100, player["mental_health"]["happiness"] + 15
                )
        else:
            # They reject reconciliation
            if status == "moved_on":
                slow_print(
                    f"{name}: I'm sorry, but I've moved on. I think it's best if we both keep moving forward separately."
                )
            else:  # still_interested
                slow_print(
                    f"{name}: I still care about you, but I'm not sure going back is the right choice. I need more time."
                )

            # Chance to change status
            if random.random() < 0.5:
                if status == "still_interested":
                    ex_partner["status"] = "moved_on"
                elif status == "moved_on" and random.random() < 0.3:
                    ex_partner["status"] = "angry"

            slow_print(
                f"{Fore.RED}Your reconciliation attempt was unsuccessful.{Style.RESET_ALL}"
            )
            increase_stress(10)
            player["mental_health"]["self_esteem"] = max(
                0, player["mental_health"]["self_esteem"] - 5
            )

    elif choice == "5" and status == "yandere":  # Therapy option for yandere
        slow_print(
            f"{Fore.CYAN}You carefully suggest to {name} that their feelings seem very intense, and that talking to someone might help.{Style.RESET_ALL}"
        )

        # Success chance starts low and improves with repeated attempts
        therapy_attempts = ex_partner.get("therapy_attempts", 0)
        base_success = 0.1 + (
            therapy_attempts * 0.1
        )  # Each attempt improves chance by 10%
        success_chance = min(0.5, base_success)  # Cap at 50%

        # Record attempt
        ex_partner["therapy_attempts"] = therapy_attempts + 1

        if random.random() < success_chance:
            # They agree to therapy
            slow_print(
                f"{Fore.GREEN}{name} appears vulnerable for a moment. \"Maybe you're right. I haven't been feeling like myself.\""
            )
            slow_print(
                f"They agree to speak with the campus counselor.{Style.RESET_ALL}"
            )

            # Set therapy status
            ex_partner["in_therapy"] = True
            ex_partner["therapy_sessions"] = 1
            ex_partner["therapy_start_date"] = current_date.strftime("%Y-%m-%d")

            # After first session, status may improve
            if random.random() < 0.7:
                ex_partner["status"] = "angry"  # First step down from yandere
                slow_print(
                    f"{Fore.YELLOW}After their first session, {name} seems slightly less obsessive.{Style.RESET_ALL}"
                )

            # Reduce player anxiety
            player["mental_health"]["anxiety"] = max(
                0, player["mental_health"]["anxiety"] - 10
            )
            decrease_stress(15)

        else:
            # They reject therapy
            if therapy_attempts == 0:
                # First rejection
                slow_print(
                    f'{Fore.RED}{name} becomes defensive. "There\'s nothing wrong with me! I just love you too much!"{Style.RESET_ALL}'
                )
                slow_print("They storm off, clearly upset by your suggestion.")
            elif therapy_attempts < 3:
                # Subsequent rejections
                slow_print(
                    f"{Fore.RED}{name}: \"You're trying to change me, aren't you? Don't you see how perfect we are together?\"{Style.RESET_ALL}"
                )
                slow_print(
                    "They refuse again, but seem slightly less defensive than before."
                )
            else:
                # After multiple attempts
                slow_print(
                    f'{Fore.YELLOW}{name} pauses. "You keep bringing this up... do you really think I need help?"{Style.RESET_ALL}'
                )
                slow_print(
                    "They don't agree, but they're starting to question their behavior."
                )

                # Slightly improved chance for next time
                ex_partner["therapy_reconsideration"] = True

            # Slight stress increase from difficult conversation
            increase_stress(5)

    # Update and check for continued therapy progress
    if ex_partner.get("in_therapy", False):
        therapy_sessions = ex_partner.get("therapy_sessions", 1)

        # Every third interaction, therapy progresses if they're still in it
        if therapy_sessions % 3 == 0:
            slow_print(
                f"\n{Fore.CYAN}Update: {name} has been attending therapy regularly.{Style.RESET_ALL}"
            )

            # Chance to improve status based on sessions
            improvement_chance = min(0.8, 0.3 + (therapy_sessions * 0.1))

            if random.random() < improvement_chance:
                if status == "yandere":
                    ex_partner["status"] = "angry"
                    slow_print(
                        f"{Fore.GREEN}Their obsessive behaviors have decreased significantly.{Style.RESET_ALL}"
                    )
                elif status == "angry":
                    ex_partner["status"] = "moved_on"
                    slow_print(
                        f"{Fore.GREEN}They seem much more at peace with the past now.{Style.RESET_ALL}"
                    )

                    # Chance to become friends
                    if random.random() < 0.6:
                        if name not in player["relationships"]:
                            player["relationships"][name] = 35
                        slow_print(
                            f"{name} mentions they'd like to try being friends again."
                        )

            # Increment sessions
            ex_partner["therapy_sessions"] = therapy_sessions + 1

    # Update player's mental health after the interaction
    update_mental_health()


def create_custom_rumor(content, rumor_type="social", target=None):
    """
    Create a custom rumor initiated by the player

    Arguments:
    content -- The rumor text content
    rumor_type -- Type of rumor (romantic, academic, social, scandal)
    target -- Optional target student of the rumor

    Returns:
    The created rumor object
    """
    if "rumors" not in player:
        player["rumors"] = []

    # Create the rumor
    new_rumor = {
        "content": content,
        "type": rumor_type,
        "spread_level": 1,  # Starts with few people knowing
        "date_created": current_date.strftime("%Y-%m-%d"),
        "originator": player["name"],  # Track who started it
    }

    # Add target if provided
    if target:
        new_rumor["target"] = target

    player["rumors"].append(new_rumor)
    return new_rumor


def generate_random_rumor():
    """Generate a random rumor to add to the rumor mill"""
    if "rumors" not in player:
        player["rumors"] = []

    # Decide on rumor type
    rumor_type = random.choice(["romantic", "academic", "social", "scandal"])

    # Generate content based on type
    content = ""

    if rumor_type == "romantic":
        # Pick two random students
        if len(students) >= 2:
            student1, student2 = random.sample(students, 2)
            content = f"{student1['name']} and {student2['name']} were seen holding hands behind the gym."
        else:
            content = (
                "There's a new couple on campus, but no one knows who they are yet."
            )

    elif rumor_type == "academic":
        subjects_data = get_subjects_for_year(player["school_year"])
        if subjects_data and students:
            subject = random.choice(list(subjects_data.keys()))
            student = random.choice(students)
            content = f"{student['name']} somehow got a perfect score on the {subject} exam that everyone else failed."
        else:
            content = "The final exams are going to be twice as difficult this year."

    elif rumor_type == "social":
        if students:
            student = random.choice(students)
            social_events = [
                f"{student['name']} had a major wardrobe malfunction during class.",
                f"{student['name']} fell asleep during an important lecture and started snoring loudly.",
                f"{student['name']} accidentally called the teacher 'mom' in front of everyone.",
            ]
            content = random.choice(social_events)
        else:
            content = "Someone set off the fire alarm as a prank last week."

    elif rumor_type == "scandal":
        if teachers and students:
            teacher = random.choice(teachers)
            scandal_types = [
                f"Someone copied all the exam answers from {teacher['name']}'s desk.",
                "The school might cancel the upcoming festival due to budget issues.",
                "Someone hacked into the school system and changed their grades.",
            ]
            content = random.choice(scandal_types)
        else:
            content = "The cafeteria is going to stop serving the popular curry dish next month."

    # Create the rumor
    if content:
        new_rumor = {
            "content": content,
            "type": rumor_type,
            "spread_level": 1,  # Starts with few people knowing
            "date_created": current_date.strftime("%Y-%m-%d"),
        }

        player["rumors"].append(new_rumor)

    return len(player["rumors"]) > 0


def update_rumors():
    """Update rumors: spread them and potentially create consequences"""
    if "rumors" not in player or not player["rumors"]:
        return

    # Chance to generate a new rumor
    if random.random() < 0.2:  # 20% daily chance
        generate_random_rumor()

    # Process each rumor
    for rumor in player["rumors"]:
        # Rumors spread over time
        if random.random() < 0.3:  # 30% chance per day per rumor
            rumor["spread_level"] = min(10, rumor["spread_level"] + 1)

        # If rumor is about player and widespread, may affect reputation
        if (
            "target" in rumor
            and rumor["target"] == player["name"]
            and rumor["spread_level"] >= 7
        ):
            rumor_type = rumor.get("type", "")

            if rumor_type == "romantic":
                # Romance rumors are mild
                if random.random() < 0.1:  # Small chance
                    increase_reputation(
                        "students", random.randint(-3, 5)
                    )  # Could be positive or negative

            elif rumor_type == "academic":
                # Academic cheating rumors hurt teacher reputation
                if random.random() < 0.3:
                    increase_reputation("teachers", -random.randint(5, 10))

            elif rumor_type == "scandal":
                # Scandal rumors hurt overall reputation
                if random.random() < 0.5:
                    increase_reputation("students", -random.randint(5, 15))
                    increase_reputation("teachers", -random.randint(3, 8))

            # Mark rumor as having had consequences
            rumor["had_consequences"] = True

        # Rumors fade over time
        days_old = (
            current_date - datetime.strptime(rumor["date_created"], "%Y-%m-%d")
        ).days
        if (
            days_old > 14 and random.random() < 0.2
        ):  # After 2 weeks, 20% daily chance to fade
            rumor["spread_level"] = max(1, rumor["spread_level"] - 1)

        # Very old rumors may be forgotten
        if (
            days_old > 30 and random.random() < 0.1
        ):  # After a month, 10% chance to be forgotten
            rumor["to_remove"] = True

    # Clean up rumors marked for removal
    player["rumors"] = [r for r in player["rumors"] if "to_remove" not in r]


def process_ex_partner_event():
    """Process a random event with an ex partner"""
    if not player["ex_partners"]:
        return  # No ex partners to have events with

    # Randomly select an ex partner to have an event with
    ex_partner_data = random.choice(player["ex_partners"])
    ex_name = ex_partner_data["name"]
    status = ex_partner_data["status"]

    # Get appropriate events for this status
    if status in EX_PARTNER_STATUSES and "events" in EX_PARTNER_STATUSES[status]:
        possible_events = EX_PARTNER_STATUSES[status]["events"]
        event_text = random.choice(possible_events)

        # Display the event
        slow_print(f"\n{Fore.YELLOW}Ex-Partner Event:{Style.RESET_ALL}")
        slow_print(f"Your ex, {ex_name}, {event_text}")

        # Process status-specific chances
        if status == "yandere":
            # Check for stalking behaviors
            if random.random() < EX_PARTNER_STATUSES[status]["stalking_chance"]:
                slow_print(
                    f"{Fore.RED}You notice {ex_name} has been following you around campus.{Style.RESET_ALL}"
                )
                increase_stress(10)
                player["mental_health"]["anxiety"] = min(
                    100, player["mental_health"]["anxiety"] + 8
                )

                # Check for dangerous escalation
                if random.random() < EX_PARTNER_STATUSES[status]["dangerous_chance"]:
                    slow_print(
                        f"{Fore.RED}They've been leaving increasingly concerning messages and gifts.{Style.RESET_ALL}"
                    )
                    slow_print(
                        "You should consider reporting this behavior to campus security."
                    )
                    increase_stress(15)
                    player["mental_health"]["anxiety"] = min(
                        100, player["mental_health"]["anxiety"] + 15
                    )

                    # Option to report
                    if random.random() < 0.7:  # 70% chance to offer reporting option
                        report_choice = input(
                            "Report this behavior to campus security? (Y/N): "
                        ).upper()
                        if report_choice == "Y":
                            slow_print(
                                f"You report {ex_name}'s behavior to campus security."
                            )
                            slow_print(
                                "They tell you they'll investigate and keep an eye out."
                            )
                            slow_print(
                                f"{Fore.GREEN}You feel safer knowing authorities are aware of the situation.{Style.RESET_ALL}"
                            )
                            decrease_stress(10)
                            player["mental_health"]["anxiety"] = max(
                                0, player["mental_health"]["anxiety"] - 12
                            )

                            # Chance to affect ex's status
                            if (
                                random.random() < 0.6
                            ):  # 60% chance of intervention working
                                ex_partner_data[
                                    "status"
                                ] = "angry"  # Change from yandere to angry
                                slow_print(
                                    f"Campus security has spoken to {ex_name}. They seem to be keeping their distance now."
                                )

        # Chance of reconciliation based on status
        reconciliation_chance = EX_PARTNER_STATUSES[status]["reconciliation_chance"]
        if random.random() < reconciliation_chance:
            slow_print(
                f"\n{ex_name} approaches you after class and asks if you could talk in private."
            )
            slow_print('"I\'ve been thinking about us... I miss what we had."')

            # Player decision
            reconcile_choice = input(
                f"Try to reconcile with {ex_name}? (Y/N): "
            ).upper()
            if reconcile_choice == "Y":
                # Reconciliation effects
                slow_print(
                    f"You agree to give your relationship with {ex_name} another chance."
                )

                # Handle harem option if enabled
                if "harem_enabled" in player and player["harem_enabled"]:
                    if "romantic_partners" not in player:
                        player["romantic_partners"] = []

                    if ex_name not in player["romantic_partners"]:
                        player["romantic_partners"].append(ex_name)

                    slow_print(
                        f"{ex_name} is now part of your romantic partners again!"
                    )
                    # Remove from ex-partners list
                    player["ex_partners"] = [
                        ex for ex in player["ex_partners"] if ex["name"] != ex_name
                    ]
                else:
                    # Standard relationship - check if we're already in another relationship
                    if (
                        player["romantic_interest"]
                        and player["romantic_interest"] != ex_name
                    ):
                        current_partner = player["romantic_interest"]
                        choice = input(
                            f"You're currently dating {current_partner}. End that relationship to be with {ex_name}? (Y/N): "
                        ).upper()

                        if choice == "Y":
                            # Break up with current partner
                            slow_print(
                                f"You break things off with {current_partner} to get back with {ex_name}."
                            )

                            # Add current partner to ex-partners with appropriate status
                            new_ex = {
                                "name": current_partner,
                                "status": "angry",  # Most likely to be angry after being dumped for an ex
                                "breakup_date": current_date.strftime("%Y-%m-%d"),
                            }
                            player["ex_partners"].append(new_ex)

                            # Update mental health from breakup
                            player["mental_health"]["breakup_count"] += 1

                            # Set ex as current romantic interest
                            player["romantic_interest"] = ex_name
                            player["romance_stage"] = 4  # Start at "Crushing" stage
                            player["romance_points"] = ROMANCE_STAGES[4][
                                "req"
                            ]  # Min req for Crushing

                            # Remove from ex-partners list
                            player["ex_partners"] = [
                                ex
                                for ex in player["ex_partners"]
                                if ex["name"] != ex_name
                            ]
                        else:
                            slow_print(
                                f"You decide to stay with {current_partner} and turn down {ex_name}'s offer."
                            )
                            # Ex becomes more angry
                            ex_partner_data["status"] = "angry"
                    else:
                        # Not currently dating anyone - get back with ex
                        player["romantic_interest"] = ex_name
                        player["romance_stage"] = 4  # Start at "Crushing" stage
                        player["romance_points"] = ROMANCE_STAGES[4][
                            "req"
                        ]  # Min req for Crushing

                        # Remove from ex-partners list
                        player["ex_partners"] = [
                            ex for ex in player["ex_partners"] if ex["name"] != ex_name
                        ]

                        slow_print(f"You and {ex_name} are back together.")
            else:
                # Rejected reconciliation - potential status change
                slow_print(
                    f"You tell {ex_name} that you don't think getting back together is a good idea."
                )

                # Random reaction to rejection
                reactions = [
                    {
                        "text": "seems to take it well, nodding sadly.",
                        "new_status": "moved_on",
                    },
                    {
                        "text": "looks disappointed but tries to smile.",
                        "new_status": "still_interested",
                    },
                    {
                        "text": "gets upset and walks away quickly.",
                        "new_status": "angry",
                    },
                    {
                        "text": "stares at you intensely before leaving without a word.",
                        "new_status": "yandere",
                    },
                ]

                # Weighted reaction based on current status
                weights = {
                    "moved_on": [0.7, 0.2, 0.09, 0.01],
                    "still_interested": [0.3, 0.4, 0.25, 0.05],
                    "angry": [0.1, 0.2, 0.6, 0.1],
                    "yandere": [0.05, 0.1, 0.25, 0.6],
                }

                reaction_probabilities = weights.get(status, [0.25, 0.25, 0.25, 0.25])
                chosen_reaction = random.choices(
                    reactions, weights=reaction_probabilities, k=1
                )[0]

                slow_print(f"{ex_name} {chosen_reaction['text']}")
                ex_partner_data["status"] = chosen_reaction["new_status"]

        # Friendship chance (only if not reconciling)
        friendship_chance = EX_PARTNER_STATUSES[status].get("friendship_chance", 0)
        if random.random() < friendship_chance and status != "yandere":
            slow_print(
                f"\n{ex_name} suggests that you both try to remain friends despite your past."
            )

            choice = input(
                f"Try to maintain a friendship with {ex_name}? (Y/N): "
            ).upper()
            if choice == "Y":
                slow_print(
                    f"You agree to work on having a friendly relationship with {ex_name}."
                )

                # Add to regular relationships if not already there
                if ex_name not in player["relationships"]:
                    player["relationships"][ex_name] = 40  # Start at "Friend" level
                else:
                    player["relationships"][ex_name] = max(
                        40, player["relationships"][ex_name]
                    )

                # If they were "angry" status, improve that
                if ex_partner_data["status"] == "angry":
                    ex_partner_data["status"] = "moved_on"
                    slow_print(
                        f"{ex_name} seems relieved that you can still be friends."
                    )
            else:
                slow_print(
                    f"You tell {ex_name} that you'd prefer to keep your distance."
                )
                # Slight chance to worsen status
                if random.random() < 0.3:
                    if ex_partner_data["status"] == "moved_on":
                        ex_partner_data["status"] = "still_interested"
                    elif ex_partner_data["status"] == "still_interested":
                        ex_partner_data["status"] = "angry"

    # Final mental health update from the interaction
    update_mental_health()


# Global birthday tracking
birthdays = {}

# Generate birthdays for NPCs
def generate_birthdays():
    """Generate random birthdays for all students and family members"""
    # No need for global declarations as we're only modifying the contents of these variables, not reassigning them
    
    # Dictionary to store birthdays (key: name, value: (month, day))
    birthday_dict = {}
    
    # Generate player's birthday (default to start of school year if not set)
    if "birthday" not in player:
        # Random birthday, avoiding the first week of school
        month = random.randint(1, 12)
        # Avoid day 0
        max_days = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
        day = random.randint(1, max_days)
        player["birthday"] = (month, day)
        
        # Add birthday to dictionary
        birthday_dict[player["name"]] = player["birthday"]
    
    # Generate birthdays for family members
    if "family" in player:
        # Parents
        if "parents" in player["family"]:
            for parent in player["family"]["parents"]:
                month = random.randint(1, 12)
                max_days = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
                day = random.randint(1, max_days)
                parent["birthday"] = (month, day)
                birthday_dict[parent["name"]] = parent["birthday"]
        
        # Siblings
        if "siblings" in player["family"]:
            for sibling in player["family"]["siblings"]:
                # If twin, same birthday as player
                if "relation" in sibling and "twin" in sibling.get("relation", ""):
                    sibling["birthday"] = player["birthday"]
                else:
                    month = random.randint(1, 12)
                    max_days = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
                    day = random.randint(1, max_days)
                    sibling["birthday"] = (month, day)
                birthday_dict[sibling["name"]] = sibling["birthday"]
    
    # Generate birthdays for students
    for student in students:
        month = random.randint(1, 12)
        max_days = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
        day = random.randint(1, max_days)
        student["birthday"] = (month, day)
        birthday_dict[student["name"]] = student["birthday"]
    
    # Generate birthdays for teachers
    for teacher in teachers:
        month = random.randint(1, 12)
        max_days = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
        day = random.randint(1, max_days)
        teacher["birthday"] = (month, day)
        birthday_dict[teacher["name"]] = teacher["birthday"]
    
    return birthday_dict

def generate_weekly_quests():
    """Generate new quests at the beginning of each week"""
    # Only need global for quests if we're assigning new quests via add_random_quests
    # No need for player and current_date as we're only reading their values
    
    # Only generate new quests at the beginning of the week (Monday)
    if current_date.weekday() != 0:  # 0 = Monday
        return
    
    # Only run once per Monday - check if we've already generated quests this week
    if player.get("last_quest_generation_date") == current_date.isoformat():
        return
    
    # Number of quests based on player's year and reputation
    base_quests = player["school_year"]
    reputation_bonus = sum(player["reputation"].values()) // 100
    total_quests = base_quests + reputation_bonus
    
    # Cap at reasonable maximum
    total_quests = min(total_quests, 5)
    
    # Generate the quests
    new_quests = add_random_quests(count=total_quests)
    
    # Mark that we've generated quests today
    player["last_quest_generation_date"] = current_date.isoformat()
    
    # Notify player of new quests if any were generated
    if new_quests:
        slow_print(f"\n{Fore.YELLOW}You have {len(new_quests)} new quests available!{Style.RESET_ALL}")
        slow_print("Type /quests to view them.")

def check_for_special_events():
    """Check if today is a special event, festival day or birthday"""
    global birthdays
    # Only need global birthdays because we're reassigning it on line 14252
    # No need for quests, player, relationship globals as we're only modifying their contents
    
    current_month = current_date.month
    current_day = current_date.day
    today_date = (current_month, current_day)
    
    # Initialize birthdays dictionary if not done yet
    if not birthdays:
        birthdays = generate_birthdays()
    
    # Track if any special event is happening
    is_special_day = False
    
    # Check for birthdays
    # Player's birthday
    if "birthday" in player and player["birthday"] == today_date:
        slow_print(f"\n{Fore.MAGENTA}🎂 Today is your birthday! 🎂{Style.RESET_ALL}")
        slow_print("Friends and family will want to celebrate with you!")
        
        # Add special quest for player's birthday party
        birthday_quest = {
            "id": 9000,  # Special high ID for birthday quests
            "description": "Celebrate your birthday",
            "objective": "Attend your birthday party at 18:00 in the Cafeteria",
            "status": "active",
            "reward": 50,
            "completed": False,
            "mandatory": True,
            "time": "18:00",
            "location": "Cafeteria",
            "type": "birthday",
            "whose_birthday": player["name"]
        }
        
        # Add to quests if not already there
        if not any(q.get("id") == 9000 for q in quests):
            quests.append(birthday_quest)
        
        is_special_day = True
    
    # Check family birthdays
    today_family_birthdays = []
    if "family" in player:
        # Check parents' birthdays
        if "parents" in player["family"]:
            for parent in player["family"]["parents"]:
                if "birthday" in parent and parent["birthday"] == today_date:
                    today_family_birthdays.append(parent["name"])
                    
                    # Add special quest for parent's birthday
                    parent_birthday_quest = {
                        "id": 9001 + len(today_family_birthdays),  # Special high ID for birthday quests
                        "description": f"Celebrate {parent['name']}'s birthday",
                        "objective": f"Visit home and give a gift to {parent['name']}",
                        "status": "active",
                        "reward": 30,
                        "completed": False,
                        "mandatory": True,
                        "location": "Living Room",
                        "type": "birthday",
                        "whose_birthday": parent["name"]
                    }
                    
                    # Add to quests if not already there
                    if not any(q.get("whose_birthday") == parent["name"] for q in quests):
                        quests.append(parent_birthday_quest)
        
        # Check siblings' birthdays
        if "siblings" in player["family"]:
            for sibling in player["family"]["siblings"]:
                if "birthday" in sibling and sibling["birthday"] == today_date:
                    today_family_birthdays.append(sibling["name"])
                    
                    # Add special quest for sibling's birthday
                    sibling_birthday_quest = {
                        "id": 9001 + len(today_family_birthdays),  # Special high ID for birthday quests
                        "description": f"Celebrate {sibling['name']}'s birthday",
                        "objective": f"Visit home and give a gift to {sibling['name']}",
                        "status": "active",
                        "reward": 25,
                        "completed": False,
                        "mandatory": True,
                        "location": "Living Room",
                        "type": "birthday",
                        "whose_birthday": sibling["name"]
                    }
                    
                    # Add to quests if not already there
                    if not any(q.get("whose_birthday") == sibling["name"] for q in quests):
                        quests.append(sibling_birthday_quest)
    
    # Display family birthday messages
    if today_family_birthdays:
        slow_print(f"\n{Fore.YELLOW}Today is the birthday of: {', '.join(today_family_birthdays)}{Style.RESET_ALL}")
        slow_print("You should visit them and bring a gift!")
        is_special_day = True
    
    # Check for classmates/friends birthdays (only people you know)
    today_birthdays = []
    for student in students:
        if "birthday" in student and student["birthday"] == today_date:
            name = student["name"]
            # Only count as birthday if you know this person (relationship > 0)
            if name in relationship and relationship[name] > 0:
                today_birthdays.append(name)
                
                # 50% chance of getting a party invitation if relationship > 40
                if relationship[name] > 40 and random.random() < 0.5:
                    # Add birthday party invitation quest
                    party_time = f"{random.randint(16, 19)}:00"  # Random time between 4-7 PM
                    party_location = random.choice(["Cafeteria", "Student Lounge", "Mall"])
                    
                    birthday_invite_quest = {
                        "id": 9100 + len(today_birthdays),  # Special high ID for birthday invites
                        "description": f"Attend {name}'s birthday party",
                        "objective": f"Go to {party_location} at {party_time}",
                        "status": "active",
                        "reward": 15,
                        "completed": False,
                        "mandatory": False,
                        "time": party_time,
                        "location": party_location,
                        "type": "birthday_invite",
                        "whose_birthday": name
                    }
                    
                    # Add to quests if not already there
                    if not any(q.get("whose_birthday") == name for q in quests):
                        quests.append(birthday_invite_quest)
                        slow_print(f"\n{Fore.CYAN}You've been invited to {name}'s birthday party at {party_time} in the {party_location}!{Style.RESET_ALL}")
    
    # Display messages about other birthdays
    if today_birthdays and not any(name == player["name"] for name in today_birthdays):
        slow_print(f"\n{Fore.CYAN}Today is the birthday of: {', '.join(today_birthdays)}{Style.RESET_ALL}")
        slow_print("You should wish them a happy birthday if you see them!")
        is_special_day = True

    # Check for special events
    for event_name, event_data in special_events.items():
        if event_data["month"] == current_month and event_data["day"] == current_day:
            slow_print(
                f"\n{Fore.YELLOW}=== Special Event: {event_name} ==={Style.RESET_ALL}"
            )
            slow_print(f"Description: {event_data['description']}")
            slow_print(f"Duration: {event_data['duration']} day(s)")
            slow_print("Activities:")
            for activity in event_data["activities"]:
                slow_print(f"- {activity}")

            # Apply event rewards
            rewards = event_data["rewards"]

            if "reputation" in rewards:
                player["reputation"]["students"] += rewards["reputation"]
                slow_print(
                    f"Your reputation among students increased by {rewards['reputation']}!"
                )

            if "money" in rewards:
                player["money"] += rewards["money"]
                slow_print(f"You earned ¥{rewards['money']} from festival activities!")

            if "stress_reduction" in rewards:
                player["stress"] = max(
                    0, player["stress"] - rewards["stress_reduction"]
                )
                slow_print(
                    f"The festival helped you relax! (Stress -{ rewards['stress_reduction']})"
                )

            # Add festival points
            player["festival_points"] += random.randint(5, 15)

            # Unlock achievement if this is the first festival

    # Check for festivals in FESTIVALS dictionary
    for festival_name, festival_data in FESTIVALS.items():
        festival_month, festival_day = festival_data["date"]

        if current_month == festival_month and current_day == festival_day:
            slow_print(
                f"\n{Fore.MAGENTA}======================================{Style.RESET_ALL}"
            )
            slow_print(f"      {festival_name}")
            slow_print(
                f"{Fore.MAGENTA}======================================{Style.RESET_ALL}"
            )
            slow_print(festival_data["description"])

            slow_print("\nFestival Activities:")
            for activity in festival_data["activities"]:
                slow_print(f"- {activity}")

            # Offer to participate in festival
            print(
                f"\n{Fore.CYAN}Would you like to participate in the festival?{Style.RESET_ALL}"
            )
            print("1. Yes, join the festivities!")
            print("2. No, maybe later.")

            choice = input("Choose an option (1-2): ")

            if choice == "1":
                slow_print(
                    f"\n{Fore.GREEN}You decide to join the {festival_name}!{Style.RESET_ALL}"
                )

                # Check if there's a minigame for this festival
                if "minigame" in festival_data and festival_data["minigame"]:
                    minigame_choice = input(
                        "Would you like to participate in the special festival minigame? (y/n): "
                    )
                    if minigame_choice.lower() == "y":
                        play_festival_minigame(festival_data["minigame"])
                    else:
                        slow_print(
                            "You enjoy the festival without participating in the special game."
                        )

                # General festival rewards
                stress_reduction = random.randint(10, 20)
                money_reward = random.randint(300, 800)
                reputation_gain = random.randint(5, 10)

                player["stress"] = max(0, player["stress"] - stress_reduction)
                player["money"] += money_reward
                player["reputation"]["students"] += reputation_gain

                slow_print(
                    f"You enjoyed the festival and reduced your stress by {stress_reduction}!"
                )
                slow_print(
                    f"You earned ¥{money_reward} and gained {reputation_gain} student reputation!"
                )

                # Chance for special rewards
                if random.random() < 0.3:  # 30% chance
                    for achievement, reward_desc in festival_data[
                        "special_rewards"
                    ].items():
                        if achievement not in player["festival_achievements"]:
                            player["festival_achievements"].append(achievement)
                            slow_print(
                                f"\n{Fore.YELLOW}Festival Achievement Unlocked: {achievement}{Style.RESET_ALL}"
                            )
                            slow_print(f"Reward: {reward_desc}")

                            # Apply special rewards
                            if "Stress reduction" in reward_desc:
                                player["stress"] = max(0, player["stress"] - 10)
                            elif "Charisma (social)" in reward_desc:
                                player["charisma"]["social"] += 2
                            elif "PE stats" in reward_desc:
                                for stat in player["pe_stats"]:
                                    player["pe_stats"][stat] += 1
                            elif "Money" in reward_desc:
                                player["money"] += 1000
            else:
                slow_print("You decide to skip the festival for now.")
            if "Festival Participant" not in player["achievements"]:
                player["achievements"].append("Festival Participant")
                slow_print(
                    f"{Fore.YELLOW}Achievement unlocked: Festival Participant{Style.RESET_ALL}"
                )

            update_ranks()
            return True
    
    # Check for holiday based dates
    is_holiday = False
    
    # Check major holidays
    if (current_month == 1 and current_day == 1) or (
        current_month == 12 and current_day >= 24 and current_day <= 26
    ):
        is_holiday = True  # New Year's Day or Christmas
    
    # Check for Golden Week (early May)
    if current_month == 5 and current_day >= 1 and current_day <= 7:
        is_holiday = True
    
    # Check for Obon (mid-August)
    if current_month == 8 and current_day >= 13 and current_day <= 16:
        is_holiday = True
    
    # School breaks
    # Spring break (late March to early April)
    if (current_month == 3 and current_day >= 20) or (
        current_month == 4 and current_day <= 7
    ):
        is_holiday = True
    
    # Summer break (late July to late August)
    if (current_month == 7 and current_day >= 20) or (
        current_month == 8 and current_day <= 31
    ):
        is_holiday = True
    
    # Winter break (late December to early January)
    if (current_month == 12 and current_day >= 20) or (
        current_month == 1 and current_day <= 7
    ):
        is_holiday = True
    
    return is_special_day or is_holiday


# Function to check for club meetings
def check_club_meetings():
    """Check if there are club meetings today"""
    if not player["clubs"]:
        return  # Not a member of any club

    current_weekday = current_date.weekday()  # 0 = Monday, 6 = Sunday

    for club_name in player["clubs"]:
        if club_name in clubs and current_weekday in clubs[club_name]["meeting_days"]:
            slow_print(
                f"\n{Fore.CYAN}=== Club Meeting: {club_name} ==={Style.RESET_ALL}"
            )
            slow_print(f"There's a {club_name} meeting today!")

            # Apply base benefits
            benefits = clubs[club_name]["benefits"]

            # Apply charisma benefits
            if "charisma" in benefits:
                for skill, value in benefits["charisma"].items():
                    player["charisma"][skill] += (
                        value // 2
                    )  # Half benefit for automated meetings

            # Reduce stress
            if "stress_reduction" in benefits:
                reduction = benefits["stress_reduction"] // 2
                player["stress"] = max(0, player["stress"] - reduction)
                slow_print(f"The club meeting helped you relax. (Stress -{reduction})")

            # Reputation gain
            player["reputation"]["students"] += random.randint(1, 3)

            # Energy cost
            if "energy_cost" in benefits:
                energy_cost = benefits["energy_cost"] // 2
                player["energy"] = max(0, player["energy"] - energy_cost)
                player["hunger"] = max(0, player["hunger"] - 3)
                slow_print(
                    f"The club activities made you a bit tired. (Energy -{energy_cost})"
                )

            update_ranks()


# Function to check and award achievements
def check_achievements():
    """Check if any achievements should be unlocked"""
    # First day achievement
    if "First Day" not in player["achievements"]:
        player["achievements"].append("First Day")
        slow_print(f"{Fore.YELLOW}Achievement unlocked: First Day{Style.RESET_ALL}")
        player["money"] += achievements["First Day"]["reward"]["money"]

    # Social Butterfly (5+ friends)
    if (
        "Social Butterfly" not in player["achievements"]
        and achievements["Social Butterfly"]["condition"]()
    ):
        player["achievements"].append("Social Butterfly")
        slow_print(
            f"{Fore.YELLOW}Achievement unlocked: Social Butterfly{Style.RESET_ALL}"
        )
        player["charisma"]["social"] += achievements["Social Butterfly"]["reward"][
            "charisma"
        ]["social"]

    # Academic Excellence (All A's)
    if (
        "Academic Excellence" not in player["achievements"]
        and achievements["Academic Excellence"]["condition"]()
    ):
        player["achievements"].append("Academic Excellence")
        slow_print(
            f"{Fore.YELLOW}Achievement unlocked: Academic Excellence{Style.RESET_ALL}"
        )
        player["charisma"]["academic"] += achievements["Academic Excellence"]["reward"][
            "charisma"
        ]["academic"]

    # Other achievements are handled in their specific contexts
    # (like Club Leader, Romance Blooms, etc.)


# Function to check quest objectives
# Global variable for tracking quest IDs
quest_counter = 1000

# Quest generation functions
def generate_new_quest(quest_type=None, difficulty=None):
    """
    Generate a new random quest based on type and difficulty
    
    Arguments:
    quest_type -- Type of quest (academic, social, adventure, job, romance)
    difficulty -- Quest difficulty (easy, medium, hard) affecting rewards
    
    Returns:
    A quest dictionary object
    """
    global quest_counter
    # Only need global for quest_counter as we're reassigning it on line 14657
    # No need for player, students, teachers, clubs, special_events globals as we're only reading their values
    
    # Increment quest counter for unique IDs
    quest_counter += 1
    
    # Set default difficulty if none provided
    if not difficulty:
        difficulty = random.choice(["easy", "medium", "hard"])
    
    # Rewards based on difficulty
    rewards = {
        "easy": {"money": random.randint(10, 30), "reputation": random.randint(2, 5)},
        "medium": {"money": random.randint(25, 50), "reputation": random.randint(4, 8)},
        "hard": {"money": random.randint(45, 100), "reputation": random.randint(7, 15)}
    }
    
    # Default to random quest type if none specified
    if not quest_type:
        quest_type = random.choice(["academic", "social", "adventure", "job", "romance"])
    
    quest = {
        "id": quest_counter,
        "type": quest_type,
        "difficulty": difficulty,
        "status": "active",
        "reward": rewards[difficulty]["money"],
        "reputation_reward": rewards[difficulty]["reputation"],
        "completed": False,
        "mandatory": False
    }
    
    # Generate quest details based on type
    if quest_type == "academic":
        # Academic quests related to studying and school activities
        academic_quests = [
            {
                "description": "Complete a challenging assignment",
                "objective": f"Study {random.choice(list(player['grades'].keys()))} for 2 hours"
            },
            {
                "description": "Earn top marks on an exam",
                "objective": f"Get an A on your next {random.choice(list(player['grades'].keys()))} exam"
            },
            {
                "description": "Help tutor a struggling student",
                "objective": "Talk to a student in the Library"
            },
            {
                "description": "Research project",
                "objective": "Spend 3 hours in the Library"
            },
            {
                "description": "Take notes for a sick classmate",
                "objective": "Attend class and take detailed notes"
            },
            {
                "description": "Join a study group",
                "objective": "Form a study group with 3 students"
            },
            {
                "description": "Submit an essay early",
                "objective": "Complete your homework 2 days before deadline"
            },
            {
                "description": "Participate in class discussion",
                "objective": "Answer 5 questions in class correctly"
            }
        ]
        selected_quest = random.choice(academic_quests)
        quest["description"] = selected_quest["description"]
        quest["objective"] = selected_quest["objective"]
    
    elif quest_type == "social":
        # Social quests involving making friends and social activities
        if not students:
            # Default if no students available
            quest["description"] = "Make a new friend"
            quest["objective"] = "Talk to 3 different students"
        else:
            student_names = [s["name"] for s in students if s["name"] in relationship and relationship[s["name"]] > 0]
            if student_names:
                student_name = random.choice(student_names)
                social_quests = [
                    {
                        "description": f"Deepen your friendship with {student_name}",
                        "objective": f"Increase relationship with {student_name} to {min(100, relationship[student_name] + 15)}"
                    },
                    {
                        "description": "Organize a small gathering",
                        "objective": "Invite 3 friends to the Student Lounge"
                    },
                    {
                        "description": "Help resolve a conflict",
                        "objective": f"Talk to {student_name} about their problem"
                    },
                    {
                        "description": "Introduce two friends to each other",
                        "objective": "Bring two classmates together at lunch"
                    },
                    {
                        "description": "Attend a social event",
                        "objective": "Go to the next campus event"
                    },
                    {
                        "description": "Share class notes",
                        "objective": f"Give your notes to {student_name}"
                    },
                    {
                        "description": "Have a heart-to-heart conversation",
                        "objective": f"Spend time with {student_name} at the Cafeteria"
                    }
                ]
                selected_quest = random.choice(social_quests)
                quest["description"] = selected_quest["description"]
                quest["objective"] = selected_quest["objective"]
            else:
                quest["description"] = "Make a new friend"
                quest["objective"] = "Talk to 3 different students"
    
    elif quest_type == "adventure":
        # Exploration and adventure quests
        adventure_quests = [
            {
                "description": "Explore the campus grounds",
                "objective": "Visit 8 different locations in one day"
            },
            {
                "description": "Find a hidden spot on campus",
                "objective": "Discover the secret garden behind the Science Building"
            },
            {
                "description": "Night adventure",
                "objective": "Visit the campus at night (after 9 PM)"
            },
            {
                "description": "Weekend expedition",
                "objective": "Visit the local town on a weekend"
            },
            {
                "description": "Geocaching challenge",
                "objective": "Find 3 hidden objects around campus"
            },
            {
                "description": "Campus mystery",
                "objective": "Investigate strange noises in the old building"
            },
            {
                "description": "Urban exploration",
                "objective": "Map out all the shortcuts between buildings"
            },
            {
                "description": "Nature walk",
                "objective": "Identify 5 different plant species on campus"
            }
        ]
        selected_quest = random.choice(adventure_quests)
        quest["description"] = selected_quest["description"]
        quest["objective"] = selected_quest["objective"]
    
    elif quest_type == "job":
        # Part-time job and career-related quests
        job_quests = [
            {
                "description": "Apply for a part-time job",
                "objective": "Submit application at the Student Affairs Office"
            },
            {
                "description": "Volunteer work",
                "objective": "Volunteer for 3 hours at a local event"
            },
            {
                "description": "Campus employment",
                "objective": "Work a shift in the Library"
            },
            {
                "description": "Internship research",
                "objective": "Research internship opportunities at 3 companies"
            },
            {
                "description": "Career fair",
                "objective": "Attend the career fair and collect 5 business cards"
            },
            {
                "description": "Resume building",
                "objective": "Create a professional resume at the Career Center"
            },
            {
                "description": "Networking event",
                "objective": "Attend an industry networking event"
            },
            {
                "description": "Job shadowing",
                "objective": "Shadow a professional for a day"
            }
        ]
        selected_quest = random.choice(job_quests)
        quest["description"] = selected_quest["description"]
        quest["objective"] = selected_quest["objective"]
    
    elif quest_type == "romance":
        # Romance-related quests (only if romance content is allowed)
        if is_content_allowed("romance"):
            if player["romantic_interest"]:
                # Quests for existing relationship
                partner_name = player["romantic_interest"]
                romance_quests = [
                    {
                        "description": f"Plan a special date with {partner_name}",
                        "objective": f"Take {partner_name} on a romantic date"
                    },
                    {
                        "description": "Anniversary surprise",
                        "objective": f"Buy a gift for {partner_name}"
                    },
                    {
                        "description": "Romantic evening",
                        "objective": f"Have dinner with {partner_name} at a nice restaurant"
                    },
                    {
                        "description": "Relationship milestone",
                        "objective": f"Progress your relationship with {partner_name} to the next stage"
                    },
                    {
                        "description": "Meet the family",
                        "objective": f"Introduce {partner_name} to your family"
                    }
                ]
                selected_quest = random.choice(romance_quests)
                quest["description"] = selected_quest["description"]
                quest["objective"] = selected_quest["objective"]
            else:
                # Quests for finding romance
                crush_candidates = []
                for student in students:
                    name = student["name"]
                    # Find students with good relationship who could be romantic interests
                    if name in relationship and relationship[name] > 30:
                        # Check compatibility based on settings
                        if check_relationship_compatibility(player, student):
                            crush_candidates.append(name)
                
                if crush_candidates:
                    crush_name = random.choice(crush_candidates)
                    romance_quests = [
                        {
                            "description": f"Express your feelings to {crush_name}",
                            "objective": f"Confess your feelings to {crush_name}"
                        },
                        {
                            "description": "Ask for a first date",
                            "objective": f"Ask {crush_name} to go on a date with you"
                        },
                        {
                            "description": "Love letter",
                            "objective": f"Write a love letter to {crush_name}"
                        },
                        {
                            "description": "Secret admirer",
                            "objective": f"Send an anonymous gift to {crush_name}"
                        },
                        {
                            "description": "Romantic gesture",
                            "objective": f"Plan a special surprise for {crush_name}"
                        }
                    ]
                    selected_quest = random.choice(romance_quests)
                    quest["description"] = selected_quest["description"]
                    quest["objective"] = selected_quest["objective"]
                else:
                    # Default if no candidates
                    quest["description"] = "Develop a romantic interest"
                    quest["objective"] = "Improve relationship with a classmate to level 50"
        else:
            # If romance content not allowed, default to a social quest
            return generate_new_quest(quest_type="social", difficulty=difficulty)
    
    return quest

# Get time of day based on game ticks
def get_time_of_day():
    """
    Get the current time of day based on game ticks
    
    Returns:
    string -- "morning", "afternoon", "evening", or "night"
    """
    # No need for global ticks as we're only reading its value, not modifying it
    
    # Default to afternoon if ticks not initialized
    if 'ticks' not in globals() or ticks is None:
        return "afternoon"
    
    # Time of day is based on ticks (each tick is 10 minutes)
    hour = (ticks // 6) % 24  # Convert ticks to hours (24-hour format)
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:  # 22-5
        return "night"

# Get the current season based on date
def get_current_season():
    """
    Determine the current season based on date
    
    Returns:
    string -- "spring", "summer", "fall", or "winter"
    """
    # No need for global current_date as we're only reading its value, not modifying it
    
    # Default to spring if current_date is not initialized
    if 'current_date' not in globals() or current_date is None:
        return "spring"
        
    month = current_date.month
    
    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "fall"
    else:  # month == 12 or month <= 2
        return "winter"

# Apply trait effects to exam performance
def apply_trait_effects_to_exam(subject, base_score):
    """
    Apply trait effects to exam performance
    
    Arguments:
    subject -- The subject being tested
    base_score -- The base score before trait modifications
    
    Returns:
    float -- Modified score after trait effects
    """
    modified_score = base_score
    season = get_current_season()
    
    # Check if player has traits that affect this subject
    for trait in player.get("traits", []):
        trait_info = PLAYER_TRAITS.get(trait, {})
        effects = trait_info.get("effects", {})
        
        # Apply general academic bonuses/penalties
        if "study_efficiency" in effects:
            modified_score += effects["study_efficiency"] * 0.1  # 10% of the efficiency bonus
        
        # Apply subject-specific bonuses
        if subject == "Math I" and "math_bonus" in effects:
            modified_score += effects["math_bonus"] * 0.2
        elif subject == "Science I" and "science_bonus" in effects:
            modified_score += effects["science_bonus"] * 0.2
        elif subject == "Art" and "art_bonus" in effects:
            modified_score += effects["art_bonus"] * 0.2
        elif subject == "Music" and "music_bonus" in effects:
            modified_score += effects["music_bonus"] * 0.2
        
        # PE subject specific modifications based on season and traits
        if subject.startswith("PE"):
            # Apply general PE bonuses
            if "pe_grade_bonus" in effects:
                modified_score += effects["pe_grade_bonus"]
            if "pe_grade_penalty" in effects:
                modified_score -= effects["pe_grade_penalty"]
            
            # Apply season specific PE modifiers for heat/cold sensitive traits
            if season == "summer" and "summer_pe_penalty" in effects:
                modified_score -= effects["summer_pe_penalty"]
                slow_print(f"{Fore.RED}The summer heat makes PE more challenging for you. (Score -{effects['summer_pe_penalty']}){Style.RESET_ALL}")
            elif season == "winter" and "winter_pe_penalty" in effects:
                modified_score -= effects["winter_pe_penalty"]
                slow_print(f"{Fore.RED}The winter cold makes PE more challenging for you. (Score -{effects['winter_pe_penalty']}){Style.RESET_ALL}")
    
    # Apply season-specific PE difficulty based on request
    if subject.startswith("PE") and season == "summer" and "strong" not in player.get("traits", []):
        # Summer PE is harder if you don't have the "strong" trait
        summer_penalty = 10
        modified_score -= summer_penalty
        slow_print(f"{Fore.RED}The summer heat makes PE class more challenging. (Score -{summer_penalty}){Style.RESET_ALL}")
    
    return max(0, min(100, modified_score))  # Clamp between 0-100

def add_random_quests(count=1, types=None):
    """
    Add random quests to the quest log
    
    Arguments:
    count -- Number of quests to add
    types -- List of quest types to choose from (academic, social, adventure, job, romance)
    
    Returns:
    List of newly added quests
    """
    # No need for 'global quests' as we're only modifying the contents of the quests list (by appending),
    # not reassigning the quests variable itself
    
    # Default quest types if none specified
    if not types:
        types = ["academic", "social", "adventure", "job"]
        # Only add romance as option if content is allowed
        if is_content_allowed("romance"):
            types.append("romance")
    
    new_quests = []
    for _ in range(count):
        quest_type = random.choice(types)
        difficulty = random.choice(["easy", "medium", "hard"])
        new_quest = generate_new_quest(quest_type, difficulty)
        quests.append(new_quest)
        new_quests.append(new_quest)
    
    return new_quests

def check_quest_objectives(location):
    """Check if being at this location completes any quest objectives"""
    # No need for global declarations here since we're only modifying contents of
    # player, quests, and relationship dictionaries/lists, not reassigning them
    # - modifying player (money, reputation, achievements) on lines 15097-15098, etc.
    # - modifying quests (marking as completed) on line 15096, etc.
    # - modifying relationship values on lines 15141-15142, etc.
    
    # Get current time safely
    current_time = get_time_of_day() if 'get_time_of_day' in globals() else "afternoon"
    
    for quest in quests:
        # Skip completed quests
        if quest["completed"]:
            continue
            
        # Regular location-based objectives
        if quest["objective"].startswith("Go to") and location in quest["objective"]:
            slow_print(
                f"{Fore.GREEN}You completed the objective for quest: {quest['description']}{Style.RESET_ALL}"
            )
            quest["completed"] = True
            player["money"] += quest["reward"]
            player["reputation"]["students"] += quest["reward"] // 5

            # Unlock achievement if this is the first quest completed
            if "Quest Completer" not in player["achievements"]:
                player["achievements"].append("Quest Completer")
                slow_print(
                    f"{Fore.YELLOW}Achievement unlocked: Quest Completer{Style.RESET_ALL}"
                )
            
            update_ranks()
        
        # Birthday quest objectives (if at right place and time)
        elif quest.get("type") == "birthday" and not quest["completed"]:
            quest_location = quest.get("location", "")
            quest_time = quest.get("time", "")
            whose_birthday = quest.get("whose_birthday", "")
            
            # Check if at right location and time matches (if specified)
            if location == quest_location:
                # If time is specified, check if current time matches
                if not quest_time or current_time == quest_time:
                    slow_print(
                        f"{Fore.MAGENTA}=== Birthday Celebration ==={Style.RESET_ALL}"
                    )
                    
                    if whose_birthday == player["name"]:
                        # Player's own birthday
                        slow_print("Everyone has gathered to celebrate your birthday!")
                        slow_print("You received gifts and had a wonderful time with your friends.")
                        
                        # Special birthday rewards
                        money_gift = random.randint(1000, 2000)
                        player["money"] += money_gift
                        slow_print(f"Birthday gift money: +¥{money_gift}")
                        
                        # Stress reduction
                        stress_reduction = random.randint(15, 30)
                        player["stress"] = max(0, player["stress"] - stress_reduction)
                        slow_print(f"The celebration helped you relax! (Stress -{stress_reduction})")
                        
                        # Relationship boost with all friends
                        for name, points in relationship.items():
                            if points > 0:  # Only improve relationships with people you know
                                relationship[name] += random.randint(2, 5)
                        slow_print("Your relationship with all friends has improved!")
                        
                        # Achievement
                        if "Birthday Celebration" not in player["achievements"]:
                            player["achievements"].append("Birthday Celebration")
                            slow_print(f"{Fore.YELLOW}Achievement unlocked: Birthday Celebration{Style.RESET_ALL}")
                    
                    elif any(parent.get("name") == whose_birthday for parent in player["family"]["parents"]):
                        # Parent's birthday
                        slow_print(f"You celebrated {whose_birthday}'s birthday!")
                        slow_print("You gave a thoughtful gift and spent quality time together.")
                        
                        # Improve family relationship
                        if "family_relationship" in player and whose_birthday in player["family_relationship"]:
                            current_rel = player["family_relationship"][whose_birthday]
                            increase = random.randint(10, 20)
                            player["family_relationship"][whose_birthday] = min(100, current_rel + increase)
                            slow_print(f"Your relationship with {whose_birthday} has improved significantly! (+{increase})")
                        
                        # Stress reduction
                        stress_reduction = random.randint(5, 15)
                        player["stress"] = max(0, player["stress"] - stress_reduction)
                        slow_print(f"The family celebration was relaxing. (Stress -{stress_reduction})")
                    
                    elif "siblings" in player["family"] and any(sibling.get("name") == whose_birthday for sibling in player["family"]["siblings"]):
                        # Sibling's birthday
                        slow_print(f"You celebrated your sibling {whose_birthday}'s birthday!")
                        slow_print("You shared some good memories and had fun together.")
                        
                        # Improve family relationship
                        if "family_relationship" in player and whose_birthday in player["family_relationship"]:
                            current_rel = player["family_relationship"][whose_birthday]
                            increase = random.randint(8, 15)
                            player["family_relationship"][whose_birthday] = min(100, current_rel + increase)
                            slow_print(f"Your relationship with {whose_birthday} has improved! (+{increase})")
                        
                        # Stress reduction
                        stress_reduction = random.randint(5, 10)
                        player["stress"] = max(0, player["stress"] - stress_reduction)
                        slow_print(f"The sibling celebration was fun. (Stress -{stress_reduction})")
                    
                    else:
                        # Friend's birthday
                        slow_print(f"You attended {whose_birthday}'s birthday party!")
                        slow_print(f"Everyone had a great time and {whose_birthday} appreciated your presence.")
                        
                        # Improve relationship
                        if whose_birthday in relationship:
                            current_rel = relationship[whose_birthday]
                            increase = random.randint(10, 15)
                            relationship[whose_birthday] = min(100, current_rel + increase)
                            slow_print(f"Your relationship with {whose_birthday} has improved! (+{increase})")
                        
                        # Small relationships boosts with other attendees
                        for student in students:
                            if student["name"] != whose_birthday and student["name"] in relationship and relationship[student["name"]] > 0:
                                # 30% chance for each known person to be at the party
                                if random.random() < 0.3:
                                    relationship[student["name"]] += random.randint(1, 3)
                                    slow_print(f"You also got to know {student['name']} better at the party.")
                        
                        # Stress reduction
                        stress_reduction = random.randint(5, 15)
                        player["stress"] = max(0, player["stress"] - stress_reduction)
                        slow_print(f"The party was fun and relaxing. (Stress -{stress_reduction})")
                    
                    # Mark quest as completed
                    quest["completed"] = True
                    player["money"] += quest["reward"]
                    player["reputation"]["students"] += quest["reward"] // 5
                    
                    update_ranks()


# Function for showing available clubs
def show_clubs():
    print(f"\n{Fore.CYAN}=== Available Clubs ==={Style.RESET_ALL}")
    for club_name, club_info in clubs.items():
        president = club_info["president"]
        location = club_info["location"]
        status = (
            f"{Fore.GREEN}Member"
            if club_name in player["clubs"]
            else f"{Fore.RED}Not a member"
        )
        position = player["club_positions"].get(club_name, "")

        print(
            f"\n{Fore.YELLOW}{club_name}{Style.RESET_ALL} - {status}{Style.RESET_ALL}"
        )
        if position:
            print(f"Your position: {position}")
        print(f"Description: {club_info['description']}")
        print(f"President: {president}")
        print(f"Location: {location}")
        print(
            f"Meeting days: {', '.join(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][day] for day in club_info['meeting_days'])}"
        )
        print("Benefits:")
        for benefit, value in club_info["benefits"].items():
            if benefit == "charisma":
                print(f"  - Social: +{value['social']}, Academic: +{value['academic']}")
            elif benefit == "stress_reduction":
                print(f"  - Stress reduction: -{value}")
            elif benefit == "energy_cost":
                print(f"  - Energy cost: -{value}")
            elif benefit in subjects:
                print(f"  - {benefit} bonus: +{value}")


# Function for joining a club
def join_club(args):
    if not args:
        print("Usage: /join_club [club name]")
        return

    club_name = " ".join(args)
    club_names = [name for name in clubs.keys()]
    club_match = next(
        (name for name in club_names if name.lower() == club_name.lower()), None
    )

    if not club_match:
        print(f"Club not found. Available clubs: {', '.join(club_names)}")
        return

    # Check if already a member
    if club_match in player["clubs"]:
        print(f"You are already a member of {club_match}.")
        return

    # Check club limit
    if len(player["clubs"]) >= 2:
        print(
            f"{Fore.RED}You can only join up to 2 clubs. Leave a club first.{Style.RESET_ALL}"
        )
        print("Your current clubs:")
        for i, club in enumerate(player["clubs"], 1):
            print(f"{i}. {club}")
        return

    # Join the club
    player["clubs"].append(club_match)
    player["club_positions"][club_match] = "Member"
    clubs[club_match]["members"].append(player["name"])

    print(
        f"{Fore.GREEN}You have successfully joined the {club_match}!{Style.RESET_ALL}"
    )
    print(
        f"Visit the {clubs[club_match]['location']} during club hours to participate in club activities."
    )

    # Achievement unlocking
    if len(player["clubs"]) == 1 and "Club Member" not in player["achievements"]:
        player["achievements"].append("Club Member")
        print(f"{Fore.YELLOW}Achievement unlocked: Club Member{Style.RESET_ALL}")


# Function for leaving a club
def leave_club(args):
    if not args:
        print("Usage: /leave_club [club name]")
        return

    club_name = " ".join(args)
    if club_name not in player["clubs"]:
        print(f"You are not a member of {club_name}.")
        return

    player["clubs"].remove(club_name)
    if club_name in player["club_positions"]:
        del player["club_positions"][club_name]

    if player["name"] in clubs[club_name]["members"]:
        clubs[club_name]["members"].remove(player["name"])

    # If player was president, assign a new random president
    if clubs[club_name]["president"] == player["name"]:
        if clubs[club_name]["members"]:
            new_president = random.choice(clubs[club_name]["members"])
            clubs[club_name]["president"] = new_president
        else:
            # Default president if no members left
            clubs[club_name]["president"] = "Faculty Advisor"

    print(f"{Fore.YELLOW}You have left the {club_name}.{Style.RESET_ALL}")


# Function to check romance status
def switch_active_partner(args):
    """Switch your active romantic partner in a harem playthrough

    Arguments:
    args -- The name of the partner to switch to
    """
    if "harem_enabled" not in player or not player["harem_enabled"]:
        slow_print(
            "{0}You don't have multiple romantic partners in this playthrough.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        return

    if "romantic_partners" not in player or not player["romantic_partners"]:
        slow_print(
            "{0}You don't have any romantic partners yet.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        return

    if not args:
        # Display list of current partners
        slow_print(f"\n{Fore.MAGENTA}=== Your Romantic Partners ==={Style.RESET_ALL}")
        for i, partner_name in enumerate(player["romantic_partners"], 1):
            active = (
                " (Active)" if player.get("romantic_interest") == partner_name else ""
            )
            slow_print(f"{i}. {partner_name}{active}")

        try:
            choice = int(
                input(
                    f"\nSelect a partner to make active (1-{len(player['romantic_partners'])}): "
                )
            )
            if 1 <= choice <= len(player["romantic_partners"]):
                new_partner = player["romantic_partners"][choice - 1]
                player["romantic_interest"] = new_partner
                slow_print(
                    f"\n{Fore.GREEN}You've switched your focus to {new_partner}.{Style.RESET_ALL}"
                )
            else:
                slow_print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
        except ValueError:
            slow_print(f"{Fore.RED}Please enter a number.{Style.RESET_ALL}")
        return

    # Try to find the partner by name
    partner_name = " ".join(args)
    if partner_name in player["romantic_partners"]:
        player["romantic_interest"] = partner_name
        slow_print(
            f"\n{Fore.GREEN}You've switched your focus to {partner_name}.{Style.RESET_ALL}"
        )
    else:
        slow_print(
            f"{Fore.RED}{partner_name} is not one of your romantic partners.{Style.RESET_ALL}"
        )
        # Show list of valid partners
        slow_print("\nYour partners are:")
        for partner in player["romantic_partners"]:
            slow_print(f"- {partner}")


def show_romance():
    """Display your romantic relationship status and options"""
    print(f"\n{Fore.MAGENTA}=== Your Romance Status ==={Style.RESET_ALL}")

    # Check if player has harem option enabled
    if (
        "harem_enabled" in player
        and player["harem_enabled"]
        and "romantic_partners" in player
        and player["romantic_partners"]
    ):
        print(f"{Fore.MAGENTA}✦ Harem Playthrough Active ✦{Style.RESET_ALL}")
        print(f"Romantic partners: {len(player['romantic_partners'])}")

        # Display each partner
        for i, partner_name in enumerate(player["romantic_partners"], 1):
            print(f"\n{Fore.CYAN}== Partner {i}: {partner_name} =={Style.RESET_ALL}")

            if partner_name in relationship:
                rel_points = relationship[partner_name]
                print(f"Relationship points: {rel_points}")

                # For simplicity, use same stage for all partners
                stage = player["romance_stage"]
                stage_name = ROMANCE_STAGES[stage]["name"]

                print(f"Current stage: {stage_name} (Stage {stage})")

                # Show who is currently active partner (for dates, etc.)
                if player.get("romantic_interest") == partner_name:
                    print(f"{Fore.YELLOW}(Currently active partner){Style.RESET_ALL}")

        # Option to switch active partner
        if len(player["romantic_partners"]) > 1:
            print(f"\n{Fore.CYAN}=== Active Partner ==={Style.RESET_ALL}")
            print(f"Current active partner: {player.get('romantic_interest', 'None')}")
            print("You can switch your active partner using '/partner [name]'")

        # Show romance points toward next stage
        stage = player["romance_stage"]
        next_stage_req = ROMANCE_STAGES[min(stage + 1, max(ROMANCE_STAGES.keys()))][
            "req"
        ]
        print(f"\nRomance points: {player['romance_points']}/{next_stage_req}")

        # Show available romantic interactions based on stage
        if stage in ROMANCE_INTERACTIONS:
            print(f"\n{Fore.CYAN}Possible interactions:{Style.RESET_ALL}")
            for interaction in ROMANCE_INTERACTIONS[stage]:
                print(f"- {interaction}")

        # Dating information
        if stage >= 2:
            print(f"\n{Fore.CYAN}Dating Options:{Style.RESET_ALL}")
            print(
                "You can go on dates using the '/date' command when in appropriate locations:"
            )

            available_date_types = []
            for date_name, date_info in DATE_TYPES.items():
                if date_info["min_stage"] <= stage:
                    available_date_types.append(
                        f"{date_name} (Stage {date_info['min_stage']}+)"
                    )

            # Group by 3 for better display
            for i in range(0, len(available_date_types), 3):
                print(", ".join(available_date_types[i : i + 3]))

            print(
                "\nAvailable date locations: Restaurant District, Movie Theater, Shopping Mall,"
            )
            print("City Park, Beach, Amusement Park, Karaoke Bar, Arcade Center")

    # Standard single relationship
    elif player.get("romantic_interest"):
        interest_name = player["romantic_interest"]
        print(f"Romantic interest: {interest_name}")

        if interest_name in relationship:
            rel_points = relationship[interest_name]
            print(f"Relationship points: {rel_points}")

            stage = player["romance_stage"]
            stage_name = ROMANCE_STAGES[stage]["name"]

            print(f"Current stage: {stage_name} (Stage {stage})")
            print(
                f"Romance points: {player['romance_points']}/{ROMANCE_STAGES[min(stage+1, max(ROMANCE_STAGES.keys()))]['req']}"
            )

            # Show available romantic interactions based on stage
            if stage in ROMANCE_INTERACTIONS:
                print(f"\n{Fore.CYAN}Possible interactions:{Style.RESET_ALL}")
                for interaction in ROMANCE_INTERACTIONS[stage]:
                    print(f"- {interaction}")

            # Dating information
            if stage >= 2:
                print(f"\n{Fore.CYAN}Dating Options:{Style.RESET_ALL}")
                print(
                    "You can go on dates using the '/date' command when in appropriate locations:"
                )

                available_date_types = []
                for date_name, date_info in DATE_TYPES.items():
                    if date_info["min_stage"] <= stage:
                        available_date_types.append(
                            f"{date_name} (Stage {date_info['min_stage']}+)"
                        )

                # Group by 3 for better display
                for i in range(0, len(available_date_types), 3):
                    print(", ".join(available_date_types[i : i + 3]))

                print(
                    "\nAvailable date locations: Restaurant District, Movie Theater, Shopping Mall,"
                )
                print("City Park, Beach, Amusement Park, Karaoke Bar, Arcade Center")
    else:
        print("You don't have a romantic interest at the moment.")
        print(f"\n{Fore.CYAN}How to start a romance:{Style.RESET_ALL}")
        print("1. Build friendship with students using '/interact [name]'")
        print("2. Once friendship is high enough, romance opportunities may occur")
        print(
            "3. You can also encounter potential romantic interests during special events"
        )


# Dating System Functions
def go_on_date(args):
    """
    Take your romantic partner on a date

    Arguments:
    args -- Command arguments (date type)
    """
    # No need for global declarations as we're only reading/modifying content, not reassigning variables

    # Check if player has a romantic interest
    if not player.get("romantic_interest"):
        slow_print(
            f"{Fore.RED}You don't have a romantic partner to go on a date with.{Style.RESET_ALL}"
        )
        return

    # Check romance stage
    if player["romance_stage"] < 2:
        slow_print(
            f"{Fore.RED}Your relationship with {player['romantic_interest']} isn't close enough for dating yet.{Style.RESET_ALL}"
        )
        slow_print("You need to reach at least 'Friends' stage to go on dates.")
        return

    # Current location
    current_location = player["current_location"]

    # Check if in a valid date location
    valid_date_locations = [
        "Restaurant District",
        "Movie Theater",
        "Shopping Mall",
        "City Park",
        "Beach",
        "Amusement Park",
        "Karaoke Bar",
        "Arcade Center",
    ]

    if current_location not in valid_date_locations:
        slow_print(
            f"{Fore.RED}You need to be in a suitable location for a date.{Style.RESET_ALL}"
        )
        slow_print(f"Valid date locations: {', '.join(valid_date_locations)}")
        return

    # Partner name
    partner_name = player["romantic_interest"]

    # List available date types for this location
    available_dates = []
    for date_name, date_info in DATE_TYPES.items():
        if (
            current_location in date_info["locations"]
            and player["romance_stage"] >= date_info["min_stage"]
        ):
            available_dates.append((date_name, date_info))

    if not available_dates:
        slow_print(
            f"{Fore.RED}There are no suitable date activities for your relationship stage at this location.{Style.RESET_ALL}"
        )
        return

    # If no specific date type provided, show options
    if not args:
        slow_print(
            f"\n{Fore.MAGENTA}=== Dating Options at {current_location} ==={Style.RESET_ALL}"
        )
        slow_print(f"You're here with {partner_name}. What would you like to do?")

        for i, (date_name, date_info) in enumerate(available_dates, 1):
            stage_req = f"(Stage {date_info['min_stage']}+)"
            slow_print(
                f"{i}. {date_name}: {date_info['description']} - ¥{date_info['cost']} {stage_req}"
            )

        print(f"{len(available_dates) + 1}. Cancel date")

        try:
            choice = int(input(f"Choose an option (1-{len(available_dates) + 1}): "))
            if 1 <= choice <= len(available_dates):
                selected_date, date_info = available_dates[choice - 1]
                # Process the selected date
                process_date(selected_date, date_info, partner_name)
            else:
                slow_print("You decide to do something else instead.")
        except ValueError:
            slow_print("Invalid choice.")
        return

    # If specific date type provided, find it
    date_type = " ".join(args).title()
    date_match = None

    for date_name, date_info in available_dates:
        if date_name.lower() == date_type.lower():
            date_match = (date_name, date_info)
            break

    if date_match:
        selected_date, date_info = date_match
        process_date(selected_date, date_info, partner_name)
    else:
        slow_print(
            f"{Fore.RED}'{date_type}' is not an available date option at this location.{Style.RESET_ALL}"
        )
        slow_print("Use '/date' without arguments to see available options.")


def process_date(date_name, date_info, partner_name):
    """
    Process a date with romantic partner

    Arguments:
    date_name -- Name of the date type
    date_info -- Date type information
    partner_name -- Name of romantic partner
    """
    global ticks, player, relationship, students  # Need global declarations for modified variables

    # Check if player has enough money
    if player["money"] < date_info["cost"]:
        slow_print(
            f"{Fore.RED}You don't have enough money for this date. You need ¥{date_info['cost']}.{Style.RESET_ALL}"
        )
        return

    # Check if player has enough energy
    if player["energy"] < date_info["energy_cost"]:
        slow_print(
            f"{Fore.RED}You don't have enough energy for this date. You need at least {date_info['energy_cost']} energy.{Style.RESET_ALL}"
        )
        return

    # Spend money and energy
    player["money"] -= date_info["cost"]
    player["energy"] = max(0, player["energy"] - date_info["energy_cost"])

    # Add romance points
    player["romance_points"] += date_info["romance_gain"]

    # Change stress
    player["stress"] = max(0, min(100, player["stress"] + date_info["stress_change"]))

    # Update relationship
    if partner_name not in relationship:
        relationship[partner_name] = ROMANCE_STAGES[player["romance_stage"]]["req"] - 5
    relationship[partner_name] += date_info["romance_gain"] // 2

    # Date narration
    slow_print(
        f"\n{Fore.MAGENTA}=== {date_name} Date with {partner_name} ==={Style.RESET_ALL}"
    )

    # Find partner personality
    partner_personality = "kind"  # Default
    for student in students:
        if student["name"] == partner_name:
            partner_personality = student.get("personality", "kind")
            break

    # Date narrative based on date type and personality
    date_narratives(date_name, partner_name, partner_personality)

    # Special attribute effects
    if date_info["special_attribute"] == "fun":
        bonus = 5
        slow_print(
            f"Having fun together increases your bond significantly! (+{bonus} romance points)"
        )
        player["romance_points"] += bonus
    elif date_info["special_attribute"] == "relax":
        reduction = 10
        slow_print(
            f"The relaxing atmosphere improves your mood and reduces stress. (-{reduction} stress)"
        )
        player["stress"] = max(0, player["stress"] - reduction)
    elif date_info["special_attribute"] == "charisma":
        bonus = 1
        slow_print(
            f"This social activity enhances your charisma! (+{bonus} social charisma)"
        )
        player["charisma"]["social"] += bonus
    elif date_info["special_attribute"] == "milestone":
        bonus = 10
        slow_print(
            f"{Fore.MAGENTA}This special date marks an important milestone in your relationship! (+{bonus} romance points){Style.RESET_ALL}"
        )
        player["romance_points"] += bonus

        # Chance for romance stage advancement
        check_romance_stage_advancement(partner_name)

    # Results summary
    slow_print(f"\n{Fore.CYAN}Date Results:{Style.RESET_ALL}")
    slow_print(f"Money spent: ¥{date_info['cost']}")
    slow_print(f"Energy used: {date_info['energy_cost']}")
    slow_print(f"Romance points gained: {date_info['romance_gain']}")
    slow_print(f"Stress change: {date_info['stress_change']}")

    # Check for stage advancement again
    check_romance_stage_advancement(partner_name)

    # Advance time (2-5 hours depending on date type)
    hours_spent = 2 + date_info["energy_cost"] // 10
    ticks += hours_spent * 10
    slow_print(f"Time passed: {hours_spent} hours")

    # Achievement for going on 5+ dates
    if "dates_completed" not in player:
        player["dates_completed"] = 0
    player["dates_completed"] += 1

    if player["dates_completed"] >= 5 and "Dating Expert" not in player["achievements"]:
        player["achievements"].append("Dating Expert")
        slow_print(
            f"\n{Fore.YELLOW}Achievement unlocked: Dating Expert{Style.RESET_ALL}"
        )
        player["charisma"]["social"] += 3


def date_narratives(date_type, partner_name, personality):
    """Generate narrative for a date based on date type and partner personality"""

    # Common narratives by date type with extended story elements
    narratives = {
        "Coffee Shop": [
            "You arrive at the café early and choose a cozy corner with comfortable seating.",
            "As {0} walks in, they spot you and their face brightens with a warm smile.",
            "The coffee shop has a gentle ambience - soft music plays while the aroma of freshly ground beans fills the air.",
            "You and {0} order your favorite drinks and find yourselves lost in conversation about dreams and aspirations.",
            "Time seems to flow differently here, each moment stretched into a perfect blend of comfort and connection.",
            "The barista occasionally glances your way, perhaps noticing the chemistry between you two.",
        ],
        "Movie": [
            "You meet {0} outside the cinema, both excited about the film you've chosen together.",
            "While waiting in line for tickets, you discuss your favorite movies and discover shared tastes.",
            "Inside the darkened theater, you find perfect seats - not too close, not too far from the screen.",
            "As the film begins, you're aware of {0}'s presence beside you, the occasional brush of arms on the shared armrest.",
            "During intense or emotional scenes, you exchange glances, forming a silent connection through your reactions.",
            "After the movie ends, you linger in the lobby, animatedly discussing your favorite moments from the film.",
        ],
        "Dinner": [
            "The restaurant has a lovely ambiance with soft lighting and elegant decor that creates an intimate setting.",
            "The host leads you to a secluded table where you pull out a chair for {0}, earning an appreciative smile.",
            "Candlelight dances across {0}'s features as you browse the menu together, suggesting favorites to each other.",
            "Your conversation flows effortlessly between light-hearted stories and deeper topics that reveal new sides of each other.",
            "The delicious food becomes a backdrop to the connection forming between you, each shared dish bringing you closer.",
            "As the evening progresses, you notice how {0}'s laugh makes the surrounding conversations fade into the background.",
        ],
        "Picnic": [
            "You've carefully prepared a picnic basket with an assortment of treats, hoping to impress {0}.",
            "Together you find the perfect spot in the park - under a blossoming tree with dappled sunlight filtering through.",
            "As you spread the blanket and arrange the food, {0} helps with genuine enthusiasm for your thoughtful preparation.",
            "Birds sing overhead while you share stories and enjoy the simple pleasure of eating outdoors together.",
            "The gentle breeze carries the scent of flowers, adding to the romantic atmosphere of your carefully planned date.",
            "Time seems to stand still in this peaceful bubble you've created together, away from the bustle of campus life.",
        ],
        "Amusement Park": [
            "The colorful entrance of the amusement park welcomes you and {0} with promises of excitement and joy.",
            "You map out a strategy together for which rides to try first, your hands occasionally brushing as you point at the park map.",
            "On the roller coaster, {0} grips your hand tightly during the drops, screaming and laughing with uninhibited excitement.",
            "Between thrilling rides, you win a small prize at a game booth and present it to {0}, who accepts it with delighted surprise.",
            "Cotton candy and other treats are shared between you, the sweetness matching the lightness in your hearts.",
            "As evening falls, the park transforms with twinkling lights, creating a magical atmosphere for the end of your date.",
        ],
        "Beach Day": [
            "The beach stretches before you like a canvas of possibilities as you and {0} find the perfect spot to set up.",
            "Waves create a rhythmic soundtrack to your date while seagulls circle overhead in the clear blue sky.",
            "You wade into the water together, splashing playfully and feeling the connection that comes from shared joy.",
            "Later, you walk along the shoreline collecting interesting shells, your footprints forming parallel paths in the wet sand.",
            "The setting sun paints the sky in magnificent colors, silhouetting your figures as you sit close on the beach towel.",
            "There's something about the vastness of the ocean that makes your growing feelings for {0} seem both significant and natural.",
        ],
        "Shopping": [
            "The bustling shopping district offers countless possibilities as you and {0} decide where to explore first.",
            "In a stylish boutique, {0} encourages you to try something you wouldn't normally wear, their eyes appreciative when you emerge.",
            "You find yourself enjoying giving honest opinions about {0}'s choices, creating a playful back-and-forth of fashion advice.",
            "A street performer catches your attention, and you pause to watch together, standing closer than strictly necessary.",
            "Over bubble tea at a small café, you compare your purchases and the stories behind why you chose each item.",
            "Shopping becomes less about the items bought and more about the shared experience of discovering each other's tastes.",
        ],
        "Karaoke": [
            "The private karaoke room becomes your own world as you scroll through song options with {0}, shoulders touching.",
            "When {0} first starts singing, you're captivated by this new side of them - confident, expressive, and completely in the moment.",
            "You join in for a duet, your voices finding harmony not just in the music but in the shared experience of vulnerability.",
            "Between songs, you share stories of music that defined important moments in your lives, building connections through melodies.",
            "The dimly lit room with its colorful flashing lights creates an atmosphere where inhibitions fade and authentic selves emerge.",
            "By the end of your session, your playlist has become a soundtrack to new memories, each song now carrying the echo of this date.",
        ],
        "Arcade": [
            "Flashing lights and electronic sounds create an energetic backdrop as you enter the arcade with {0}.",
            "You discover {0}'s competitive side at the racing games, their determination showing in their focused expression.",
            "At the claw machine, you work together strategically to win a small plush toy, celebrating with high-fives when you succeed.",
            "The dance game draws a small crowd as you both show off your moves, laughing at missteps and cheering each other's combos.",
            "You find yourself noticing the way {0}'s eyes light up with each victory, and how losing doesn't diminish their enjoyment.",
            "In this playground of games, you're really playing a different game altogether - discovering the person behind the player.",
        ],
        "Fancy Date": [
            "The maître d' leads you to a table draped in crisp linen in one of the city's most prestigious restaurants.",
            "You notice how particularly stunning {0} looks tonight, dressed elegantly for the occasion, their eyes reflecting the candlelight.",
            "The sommelier suggests a wine pairing that complements your carefully selected courses, adding sophistication to your dining experience.",
            "Between exquisite dishes, your conversation deepens beyond campus life to hopes, dreams, and philosophies.",
            "There's a moment when time seems suspended - just you, {0}, and the invisible thread of connection strengthening between you.",
            "As you leave the restaurant, the night air feels charged with possibility, the evening elevated beyond a simple dinner into something momentous.",
        ],
        "Stargazing": [
            "You've researched the perfect spot, away from city lights, where the stars would be most visible for your date with {0}.",
            "Wrapped in blankets against the night chill, you lie side by side on a grassy hilltop, faces turned toward the infinite sky.",
            "Using a stargazing app, you take turns identifying constellations, your hushed voices enhancing the intimacy of the moment.",
            "A shooting star streaks across the darkness, and you both make silent wishes, exchanging knowing smiles afterward.",
            "The conversation turns philosophical under the vast canopy of stars, creating a deeper connection through shared wonder.",
            "In this moment, the universe seems to have conspired to bring you and {0} together under its celestial watch.",
        ],
    }

    # Extended personality-specific reactions for deeper characterization
    personality_reactions = {
        "tsundere": [
            "{0} pretends to be unimpressed by your date planning, but you catch them hiding a smile when they think you're not looking.",
            "When you mention having a good time, {0} quickly looks away and mutters 'It's not like I planned my whole day around this or anything.'",
            "As the date progresses, {0}'s prickly exterior softens noticeably, revealing glimpses of genuine warmth underneath.",
        ],
        "kuudere": [
            "{0} maintains a calm, composed exterior throughout the date, but their eyes betray interest when you share personal stories.",
            "You notice subtle changes in {0}'s expression - the barely perceptible smile, the attentive posture - signs they're enjoying themselves.",
            "Near the end of your time together, {0} makes a quiet comment that shows they've been paying careful attention to everything you've said.",
        ],
        "dandere": [
            "At first, {0} seems nearly silent, responding with nods and short phrases, eyes often directed downward.",
            "Gradually, when the conversation turns to topics they're passionate about, {0} begins to speak more, their voice growing animated.",
            "By the end of the date, you're surprised at how much {0} has opened up, as if a different person emerged from behind their shyness.",
        ],
        "deredere": [
            "{0} approaches your date with unbridled enthusiasm, their affection and excitement evident in every gesture and smile.",
            "Throughout your time together, {0} finds small ways to express their fondness - a touch on your arm, a compliment, a warm laugh at your jokes.",
            "Their authentic joy in spending time with you is contagious, making even ordinary moments feel special and cherished.",
        ],
        "yandere": [
            "{0} watches you with an intensity that's both flattering and slightly unnerving, their attention never wavering.",
            "When someone else briefly interrupts your date, you notice a flash of something possessive in {0}'s eyes before their smile returns.",
            "Every detail you mention about yourself, {0} seems to memorize instantly, referencing them later with perfect recall.",
        ],
        "kind": [
            "{0} shows thoughtfulness in small ways throughout your date - ensuring you're comfortable, listening attentively, remembering details from past conversations.",
            "When a small mishap occurs, {0}'s response is so understanding and gentle that it turns an awkward moment into a pleasant memory.",
            "You notice how {0} treats everyone around you with the same warmth they show you, revealing a genuinely compassionate nature.",
        ],
        "serious": [
            "{0} approaches your date with the same thoughtfulness they bring to their studies, asking meaningful questions and considering their responses carefully.",
            "Though {0} rarely laughs loudly, you learn to spot the subtle crinkle around their eyes that signals genuine amusement.",
            "When the conversation turns serious, you appreciate how {0} engages with complex topics, showing depth of character and thought.",
        ],
        "playful": [
            "{0} transforms even ordinary moments into opportunities for fun, turning a walk into a game or finding humor in unexpected places.",
            "Their spontaneity is refreshing - suggesting an unplanned detour during your date that leads to one of the most memorable experiences.",
            "You find yourself laughing more with {0} than you have in months, their playful nature bringing out a lighter side of yourself.",
        ],
        "ambitious": [
            "When {0} speaks about their goals, their entire demeanor changes - eyes bright with purpose, voice confident and clear.",
            "You're impressed by how {0} connects your casual date activities to their larger aspirations, showing how they integrate passion into daily life.",
            "By the end of your time together, {0} has not only shared their dreams but expressed genuine interest in supporting yours.",
        ],
        "mysterious": [
            "{0} reveals information about themselves in carefully measured doses, each disclosure feeling like a specially granted privilege.",
            "Just when you think you understand {0}, they share something surprising that reshapes your perception of them.",
            "Their enigmatic smile when avoiding direct questions about their past makes you even more curious about the layers beneath their carefully maintained surface.",
        ],
        "shy": [
            "{0} blushes noticeably when you offer a sincere compliment, their fingers fidgeting with the edge of their sleeve.",
            "You notice how {0} becomes more animated when talking about subjects they love, briefly forgetting their self-consciousness.",
            "By creating a comfortable space between you, you're rewarded with glimpses of the vibrant personality {0} usually keeps hidden.",
        ],
        "energetic": [
            "{0} approaches your date with boundless enthusiasm, suggesting multiple activities and barely pausing to catch their breath between topics.",
            "Their expressive gestures and animated storytelling style draw attention from others nearby, but {0} seems focused entirely on your reaction.",
            "Despite the whirlwind of energy {0} brings, you notice how they still manage to listen attentively when you speak, their excitement never overshadowing connection.",
        ],
    }

    # Display the narrative with enhanced formatting
    if date_type in narratives:
        slow_print(
            "\n{0}=== Your Date with {1} ===\n{2}".format(
                Fore.CYAN, partner_name, Style.RESET_ALL
            )
        )

        # Add a short pause for dramatic effect
        time.sleep(0.5)

        # Display setting introduction with special color
        date_location = date_type
        if isinstance(date_type, str) and "_" in date_type:
            date_location = date_type.replace("_", " ")
        slow_print(
            "{0}Location: {1}{2}".format(Fore.YELLOW, date_location, Style.RESET_ALL)
        )
        slow_print("")

        # Display the narrative with pauses between paragraphs for better pacing
        for line in narratives[date_type]:
            slow_print(
                "{0}{1}{2}".format(
                    Fore.WHITE, line.format(partner_name), Style.RESET_ALL
                )
            )
            time.sleep(0.3)  # Short pause between narrative lines

        slow_print("")  # Empty line for separation

    # Add personality-specific reaction with special formatting
    if personality in personality_reactions:
        slow_print(
            "{0}● {1}'s Reactions:{2}".format(
                Fore.MAGENTA, partner_name, Style.RESET_ALL
            )
        )

        # Get random reaction or show all for more complex narrative
        if isinstance(personality_reactions[personality], list):
            # Show all reactions in the list for extended narrative
            for reaction in personality_reactions[personality]:
                if isinstance(reaction, str):
                    slow_print("  {0}".format(reaction.format(partner_name)))
                else:
                    slow_print("  {0}".format(str(reaction)))
                time.sleep(0.2)  # Brief pause between reactions
        else:
            # If it's a single string, just show that
            reaction_text = personality_reactions[personality]
            if isinstance(reaction_text, str):
                slow_print("  {0}".format(reaction_text.format(partner_name)))
            else:
                slow_print("  {0}".format(str(reaction_text)))
    else:
        slow_print("{0} seems to be enjoying the date with you.".format(partner_name))

    slow_print("")  # Empty line for separation

    # Add a special moment based on date type with enhanced formatting
    if date_type in ["Fancy Date", "Stargazing"]:
        slow_print(
            "\n{0}✧ A special moment occurs between you and {1}... ✧{2}".format(
                Fore.MAGENTA, partner_name, Style.RESET_ALL
            )
        )

        if date_type == "Fancy Date":
            slow_print(
                "{0}As the evening comes to a close, you and {1} share a meaningful glance across the table.{2}".format(
                    Fore.YELLOW, partner_name, Style.RESET_ALL
                )
            )
            slow_print(
                "{0}The connection between you feels stronger than ever.{1}".format(
                    Fore.YELLOW, Style.RESET_ALL
                )
            )
        else:  # Stargazing
            slow_print(
                "{0}A shooting star streaks across the sky, and you both make silent wishes.{1}".format(
                    Fore.YELLOW, Style.RESET_ALL
                )
            )
            slow_print(
                "{0}In that perfect moment, you feel truly connected to {1}.{2}".format(
                    Fore.YELLOW, partner_name, Style.RESET_ALL
                )
            )

        # Extra impact for memorable date
        slow_print(
            "\n{0}This date will remain in your memories for a long time...{1}".format(
                Fore.CYAN, Style.RESET_ALL
            )
        )


def check_romance_stage_advancement(partner_name):
    """Check and process romance stage advancement"""
    global player  # Need global declaration to modify player dictionary
    # Check if we can advance to next romance stage
    current_stage = player["romance_stage"]
    next_stage = current_stage + 1

    if (
        next_stage in ROMANCE_STAGES
        and player["romance_points"] >= ROMANCE_STAGES[next_stage]["req"]
    ):
        player["romance_stage"] = next_stage
        stage_name = ROMANCE_STAGES[next_stage]["name"]
        slow_print(
            "\n{0}♥ Your relationship with {1} has advanced to '{2}'! ♥{3}".format(
                Fore.MAGENTA, partner_name, stage_name, Style.RESET_ALL
            )
        )

        # Special message based on new stage
        if next_stage == 3:
            slow_print(
                "You and {0} have become close friends. You can feel a special connection developing.".format(
                    partner_name
                )
            )
        elif next_stage == 4:
            slow_print(
                "You realize you have deeper feelings for {0}. The way they look at you has changed too.".format(
                    partner_name
                )
            )
        elif next_stage == 5:
            # Check for harem option (15% chance)
            if "harem_enabled" not in player and random.random() < 0.15:
                player["harem_enabled"] = True
                player["romantic_partners"] = [
                    partner_name
                ]  # Initialize with first partner
                slow_print(
                    "Your relationship with {0} is now official!".format(partner_name)
                )
                slow_print(
                    "{0}You sense that you might be able to maintain multiple romantic relationships in this playthrough...{1}".format(
                        Fore.YELLOW, Style.RESET_ALL
                    )
                )
            elif "harem_enabled" in player and player["harem_enabled"]:
                # Add this partner to the harem if not already there
                if "romantic_partners" not in player:
                    player["romantic_partners"] = []

                if partner_name not in player["romantic_partners"]:
                    player["romantic_partners"].append(partner_name)

                slow_print(
                    "Your relationship with {0} is now official!".format(partner_name)
                )
                slow_print(
                    "{0}You now have {1} romantic partners.{2}".format(
                        Fore.MAGENTA, len(player["romantic_partners"]), Style.RESET_ALL
                    )
                )
            else:
                # Standard exclusive relationship
                if (
                    player["romantic_interest"]
                    and player["romantic_interest"] != partner_name
                ):
                    slow_print(
                        "{0}You've ended your relationship with {1} to be with {2}.{3}".format(
                            Fore.RED,
                            player["romantic_interest"],
                            partner_name,
                            Style.RESET_ALL,
                        )
                    )

                player["romantic_interest"] = partner_name
                slow_print(
                    "Your relationship with {0} is now official! You're dating exclusively.".format(
                        partner_name
                    )
                )

            # Unlock romance achievement if reached Dating stage
            if "Romance Expert" not in player["achievements"]:
                player["achievements"].append("Romance Expert")
                slow_print(
                    "{0}Achievement unlocked: Romance Expert{1}".format(
                        Fore.YELLOW, Style.RESET_ALL
                    )
                )
                slow_print("Your social charisma has increased!")
                player["charisma"]["social"] += 4

            # Special harem achievement
            if (
                "harem_enabled" in player
                and player["harem_enabled"]
                and "romantic_partners" in player
                and len(player["romantic_partners"]) >= 3
            ):
                if "Harem Master" not in player["achievements"]:
                    player["achievements"].append("Harem Master")
                    slow_print(
                        "{0}Achievement unlocked: Harem Master{1}".format(
                            Fore.YELLOW, Style.RESET_ALL
                        )
                    )
                    slow_print("Your social charisma has increased significantly!")
                    player["charisma"]["social"] += 8


# Function to relax and reduce stress
def relax_command():
    global ticks, player, relationship
    current_location = player.get("current_location", "")

    # Different relaxation activities based on location
    relaxation_options = {
        "Student Room 364": ["Take a nap", "Listen to music", "Read for pleasure"],
        "Library": [
            "Read a novel",
            "Watch educational videos",
            "Study at your own pace",
        ],
        "Courtyard": ["Sit under a tree", "People watch", "Exercise lightly"],
        "Rooftop": ["Enjoy the view", "Feel the breeze", "Have a quiet moment"],
        "School Garden": [
            "Smell the flowers",
            "Practice meditation",
            "Sketch the scenery",
        ],
    }

    # Default options if location not in the dictionary
    if current_location not in relaxation_options:
        relaxation_options[current_location] = [
            "Take a moment to breathe",
            "Close your eyes and rest",
            "Stretch your muscles",
        ]

    options = relaxation_options[current_location]

    print(
        f"\n{Fore.CYAN}=== Relaxation Options at {current_location} ==={Style.RESET_ALL}"
    )
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    choice = input("Choose an activity (or 0 to cancel): ")

    if not choice.isdigit() or int(choice) == 0 or int(choice) > len(options):
        print("Relaxation canceled.")
        return

    selected = options[int(choice) - 1]
    stress_reduction = random.randint(10, 20)
    energy_cost = random.randint(5, 10)

    player["stress"] = max(0, player["stress"] - stress_reduction)
    player["energy"] = max(0, player["energy"] - energy_cost)
    ticks += 5  # Relaxing takes time

    print(
        f"\n{Fore.GREEN}You {selected.lower()} and felt much better.{Style.RESET_ALL}"
    )
    print(f"Stress reduced by {stress_reduction} points.")
    print(f"Current stress level: {player['stress']}/100")

    # Chance for special event during relaxation
    if random.random() < 0.2:  # 20% chance
        if (
            current_location in ["Courtyard", "Rooftop", "School Garden"]
            and player["romantic_interest"]
        ):
            # Romantic encounter if you have a romantic interest
            print(
                f"\n{Fore.MAGENTA}While relaxing, you run into {player['romantic_interest']}.{Style.RESET_ALL}"
            )
            print("You spend some quality time together.")
            relationship[player["romantic_interest"]] += random.randint(3, 7)
            player["stress"] = max(
                0, player["stress"] - random.randint(5, 10)
            )  # Additional stress reduction
        else:
            # Random student encounter
            random_student = random.choice(students)
            print(
                f"\n{Fore.CYAN}While relaxing, you run into {random_student['name']}.{Style.RESET_ALL}"
            )
            print("You have a nice chat and feel more connected to school life.")
            if random_student["name"] not in relationship:
                relationship[random_student["name"]] = 0
            relationship[random_student["name"]] += random.randint(1, 3)
            player["charisma"]["social"] += 1


# Function to show achievements
def show_achievements():
    print(f"\n{Fore.YELLOW}=== Achievements ==={Style.RESET_ALL}")

    if not player["achievements"]:
        print("You haven't unlocked any achievements yet.")
        print("Keep playing to discover and unlock achievements!")
        return

    print(f"Unlocked achievements ({len(player['achievements'])}/{len(achievements)}):")

    for achievement_name in player["achievements"]:
        if achievement_name in achievements:
            achievement = achievements[achievement_name]
            print(f"\n{Fore.GREEN}✓ {achievement_name}{Style.RESET_ALL}")
            print(f"  {achievement['description']}")

            # Show reward if present
            if "reward" in achievement:
                print("  Rewards:")
                for reward_type, reward_value in achievement["reward"].items():
                    if isinstance(reward_value, dict):
                        for sub_type, sub_value in reward_value.items():
                            print(f"    - {sub_type.capitalize()}: +{sub_value}")
                    else:
                        print(f"    - {reward_type.capitalize()}: +{reward_value}")

    # Show locked achievements with hints but not conditions
    print(f"\n{Fore.RED}Locked achievements:{Style.RESET_ALL}")
    for name, details in achievements.items():
        if name not in player["achievements"]:
            print(f"? {details['description']}")


def show_rumors():
    """Display current rumors in the game"""
    if "rumors" not in player or not player["rumors"]:
        print(
            f"\n{Fore.YELLOW}You haven't heard any interesting gossip lately.{Style.RESET_ALL}"
        )
        return

    print(f"\n{Fore.MAGENTA}=== Campus Gossip ==={Style.RESET_ALL}")

    # Sort rumors by spread level (most widespread first)
    sorted_rumors = sorted(
        player["rumors"], key=lambda r: r.get("spread_level", 0), reverse=True
    )

    for i, rumor in enumerate(sorted_rumors, 1):
        # Determine rumor status based on spread level
        spread_level = rumor.get("spread_level", 1)

        if spread_level <= 2:
            status = f"{Fore.CYAN}(Secret - only a few people know){Style.RESET_ALL}"
        elif spread_level <= 5:
            status = (
                f"{Fore.YELLOW}(Spreading - becoming common knowledge){Style.RESET_ALL}"
            )
        else:
            status = f"{Fore.RED}(Widespread - everyone is talking about it){Style.RESET_ALL}"

        # Show the rumor with its status
        print(f"{i}. {rumor['content']} {status}")

        # Show additional info if available
        if "date_created" in rumor:
            creation_date = datetime.strptime(rumor["date_created"], "%Y-%m-%d")
            days_old = (current_date - creation_date).days
            age_text = f"{days_old} days ago" if days_old > 0 else "today"
            print(f"   First heard: {age_text}")

        if "originator" in rumor and rumor["originator"] == player["name"]:
            print(f"   {Fore.YELLOW}(You started this rumor){Style.RESET_ALL}")

        if "target" in rumor and rumor["target"] == player["name"]:
            print(f"   {Fore.RED}(This rumor is about you!){Style.RESET_ALL}")

        print()  # Empty line between rumors

    if any(r.get("target") == player["name"] for r in player["rumors"]):
        print(
            f"{Fore.YELLOW}Tip: Rumors about you can affect your reputation. You might want to address them.{Style.RESET_ALL}"
        )

    if any(r.get("originator") == player["name"] for r in player["rumors"]):
        print(
            f"{Fore.YELLOW}Tip: Starting rumors may have consequences if discovered.{Style.RESET_ALL}"
        )


def change_clothes_command(args=None):
    """
    Command to change the player's clothes

    Arguments:
    args -- Optional arguments (not used in this command)
    """
    global ticks, player

    # Show owned clothing
    slow_print(f"\n{Fore.CYAN}=== Change Clothes ==={Style.RESET_ALL}")

    # Check if we're in an appropriate location to change clothes
    current_location = player["current_location"]

    if current_location not in CHANGING_LOCATIONS:
        slow_print(f"{Fore.RED}You can't change clothes here.{Style.RESET_ALL}")
        slow_print("You need to be in your room or a changing room.")
        return

    # Show current clothing
    current_clothing = player["clothing"]["wearing"]
    if current_clothing:
        clothing_type = CLOTHING_ITEMS[current_clothing]["type"].capitalize()
        slow_print(
            f"{Fore.CYAN}Currently Wearing:{Style.RESET_ALL} {current_clothing} ({clothing_type})"
        )
    else:
        slow_print(
            f"{Fore.RED}Warning: You aren't wearing any clothes!{Style.RESET_ALL}"
        )

    # Display owned clothing items
    if player["clothing"]["owned"]:
        print(f"\n{Fore.CYAN}Your Clothing:{Style.RESET_ALL}")
        for i, clothing in enumerate(player["clothing"]["owned"], 1):
            clothing_type = CLOTHING_ITEMS[clothing]["type"].capitalize()
            currently_wearing = (
                " (Currently wearing)" if clothing == current_clothing else ""
            )
            print(f"{i}. {clothing} ({clothing_type}){currently_wearing}")
    else:
        print("\nYou don't own any clothing. (This shouldn't happen!)")

    # Ask player to select clothing
    choice = input(
        f"\nSelect clothing to wear (1-{len(player['clothing']['owned'])}) or 0 to cancel: "
    )
    try:
        choice_num = int(choice)
        if choice_num == 0:
            slow_print("You decide not to change clothes.")
            return

        if 1 <= choice_num <= len(player["clothing"]["owned"]):
            new_clothing_name = player["clothing"]["owned"][choice_num - 1]

            # Skip if already wearing this clothing
            if new_clothing_name == current_clothing:
                slow_print(f"You're already wearing {new_clothing_name}.")
                return

            # Change clothing
            if change_clothing(new_clothing_name):
                # Advance time slightly
                ticks += 2  # Changing clothes takes a little time
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")


# Function for random events based on location
def random_location_event(location):
    """Trigger random events specific to the current location"""
    # 30% chance of a location-specific event
    if random.random() > 0.3:
        return

    # Generic events for all locations
    generic_events = [
        {
            "description": "You find a small amount of money on the ground!",
            "effect": lambda: increase_money(random.randint(50, 200)),
        },
        {
            "description": "You feel a bit tired from walking around.",
            "effect": lambda: decrease_energy(random.randint(3, 7)),
        },
        {
            "description": "A cool breeze makes you feel refreshed.",
            "effect": lambda: decrease_stress(random.randint(3, 7)),
        },
    ]

    # Location-specific events
    location_events = {
        "Classroom": [
            {
                "description": "The teacher asks you a question and you answer correctly!",
                "effect": lambda: increase_reputation("teachers", random.randint(1, 3)),
            },
            {
                "description": "You help a classmate understand a difficult concept.",
                "effect": lambda: increase_reputation("students", random.randint(2, 4)),
            },
            {
                "description": "A pop quiz is announced! You feel stressed.",
                "effect": lambda: increase_stress(random.randint(5, 10)),
            },
        ],
        "Library": [
            {
                "description": "You find a helpful book that makes studying easier.",
                "effect": lambda: player["charisma"].update(
                    {"academic": player["charisma"]["academic"] + 1}
                ),
            },
            {
                "description": "The quiet atmosphere helps you concentrate.",
                "effect": lambda: decrease_stress(random.randint(5, 10)),
            },
        ],
        "Cafeteria": [
            {
                "description": "Someone shares their food with you.",
                "effect": lambda: increase_hunger(random.randint(10, 20)),
            },
            {
                "description": "You join a lively table conversation.",
                "effect": lambda: player["charisma"].update(
                    {"social": player["charisma"]["social"] + 1}
                ),
            },
        ],
        "Gym": [
            {
                "description": "An impromptu sports game starts and you join in.",
                "effect": lambda: decrease_energy(random.randint(10, 15)),
            },
            {
                "description": "Watching others exercise motivates you.",
                "effect": lambda: player["charisma"].update(
                    {"social": player["charisma"]["social"] + 1}
                ),
            },
        ],
        "Student Room 364": [
            {
                "description": "Your roommate left a snack for you.",
                "effect": lambda: increase_hunger(random.randint(5, 15)),
            },
            {
                "description": "The comfort of your room helps you relax.",
                "effect": lambda: decrease_stress(random.randint(8, 15)),
            },
        ],
    }

    # Choose and apply an event
    if location in location_events:
        all_events = generic_events + location_events[location]
    else:
        all_events = generic_events

    event = random.choice(all_events)
    slow_print(f"\n{Fore.CYAN}Event: {event['description']}{Style.RESET_ALL}")
    event["effect"]()


# Helper functions for player stats
def increase_money(amount):
    """Helper function to increase player money"""
    player["money"] += amount


def decrease_energy(amount):
    """Helper function to decrease player energy"""
    player["energy"] = max(0, player["energy"] - amount)


def decrease_stress(amount):
    """Helper function to decrease player stress"""
    player["stress"] = max(0, player["stress"] - amount)


def increase_stress(amount):
    """Helper function to increase player stress"""
    player["stress"] = min(100, player["stress"] + amount)


def increase_hunger(amount):
    """Helper function to increase player hunger"""
    player["hunger"] = min(100, player["hunger"] + amount)


def decrease_hunger(amount):
    """Helper function to decrease player hunger"""
    player["hunger"] = max(0, player["hunger"] - amount)


# Helper function to increase reputation
def increase_reputation(category, amount):
    """Helper function to increase reputation in a category"""
    player["reputation"][category] += amount
    update_ranks()


# Core subjects definition
core_subjects = ["Math", "Literature", "English", "Science", "History"]


def random_event(location):
    event_chance = random.randint(
        1, 6
    )  # Increased possibilities with ex-partner events

    # Special chance for ex-partner event (10% if player has ex-partners)
    if player["ex_partners"] and random.random() < 0.10:
        process_ex_partner_event()
        advance_day()
        return

    # Neurodiversity-specific events (if player has traits)
    if player["neurodiversity"]["traits"] and random.random() < 0.15:
        trait = player["neurodiversity"]["traits"][0]
        severity = player["neurodiversity"]["severity"].get(trait, 5)

        if trait == "dyslexia":
            slow_print(
                f"\n{Fore.YELLOW}You struggle with reading a complex text in class.{Style.RESET_ALL}"
            )

            if "extended_time" in player["neurodiversity"]["accommodations"]:
                slow_print(
                    "Your extended time accommodation helps you work through it at your own pace."
                )
                slow_print("You feel relieved that the pressure is reduced.")
                decrease_stress(5)
            else:
                slow_print(
                    "The pressure makes you feel anxious about finishing on time."
                )
                increase_stress(severity)

        elif trait == "adhd":
            slow_print(
                f"\n{Fore.YELLOW}You find it hard to focus during a long lecture.{Style.RESET_ALL}"
            )

            if "movement_breaks" in player["neurodiversity"]["accommodations"]:
                slow_print("You take a brief movement break as per your accommodation.")
                slow_print("This helps you return to class more focused.")
                decrease_stress(7)
            else:
                slow_print("You struggle to sit still and concentrate.")
                increase_stress(severity)

        elif trait == "autism":
            slow_print(
                f"\n{Fore.YELLOW}The cafeteria is particularly noisy and overwhelming today.{Style.RESET_ALL}"
            )

            if "sensory_accommodations" in player["neurodiversity"]["accommodations"]:
                slow_print(
                    "You use your noise-cancelling headphones from your accommodation plan."
                )
                slow_print("The sensory overload is significantly reduced.")
                decrease_stress(8)
            else:
                slow_print("The sensory overload is quite distressing.")
                increase_stress(severity + 2)

        elif trait == "anxiety_disorder":
            slow_print(
                f"\n{Fore.YELLOW}You feel anxious about an upcoming class presentation.{Style.RESET_ALL}"
            )

            if "alternative_assessments" in player["neurodiversity"]["accommodations"]:
                slow_print(
                    "You remember you can use your alternative assessment accommodation."
                )
                slow_print("Knowing you have options helps you feel calmer.")
                decrease_stress(10)
            else:
                slow_print("The anxiety builds throughout the day.")
                increase_stress(severity + 3)
                player["mental_health"]["anxiety"] = min(
                    100, player["mental_health"]["anxiety"] + 5
                )

        # Update mental health after neurodiversity event
        update_mental_health()
        advance_day()
        return

    if event_chance == 1:
        event = random.choice(
            [
                "pop quiz",
                "sports event",
                "surprise inspection",
                "cafeteria food fight",
                "club meeting",
                "mental health workshop",
                "campus health fair",
                "therapy dog visit",
            ]
        )

        if event == "pop quiz":
            # Get current subject list
            current_subjects = get_current_subjects()
            if current_subjects:
                subject = random.choice(current_subjects)
                slow_print(f"\nA surprise pop quiz in {subject}!")
            else:
                subject = "Basic Studies"
                slow_print(f"\nA surprise pop quiz in {subject}!")
            if homework.get(subject, False):
                slow_print("You feel prepared and ace the quiz!")
                grade = player["grades"][subject]
                if grade != "A":  # Only improve if not already at A
                    player["grades"][subject] = chr(max(ord(grade) - 1, ord("A")))
                slow_print(f"Your grade improved to {player['grades'][subject]}!")
            else:
                slow_print("You struggle because you didn't study...")
                grade = player["grades"][subject]
                if grade != "F":  # Only decrease if not already at F
                    player["grades"][subject] = chr(min(ord(grade) + 1, ord("F")))
                slow_print(f"Your grade dropped to {player['grades'][subject]}!")

        elif event == "sports event":
            slow_print(
                "\nThere's a sudden sports competition at the gym! Everyone's cheering!"
            )

        elif event == "surprise inspection":
            slow_print("\nA strict teacher inspects your homework...")
            missing = [subj for subj, done in homework.items() if not done]
            if missing:
                slow_print("You get scolded for missing homework!")
                increase_reputation("teachers", -5)
            else:
                slow_print("You pass the inspection with flying colors!")
                increase_reputation("teachers", 5)
            update_ranks()

        elif event == "cafeteria food fight":
            slow_print("\nFood fight! You get hit with a flying sandwich!")

        elif event == "club meeting":
            slow_print(
                "\nThe anime club is recruiting new members. Will you join them?"
            )

        elif event == "mental health workshop":
            slow_print(
                f"\n{Fore.CYAN}The university is hosting a mental health awareness workshop.{Style.RESET_ALL}"
            )
            attend = input("Would you like to attend? (Y/N): ").upper()

            if attend == "Y":
                slow_print(
                    "You attend the workshop and learn valuable coping strategies."
                )
                player["mental_health"]["coping_skills"] = min(
                    100, player["mental_health"]["coping_skills"] + 15
                )

                # Reduce anxiety and depression slightly
                player["mental_health"]["anxiety"] = max(
                    0, player["mental_health"]["anxiety"] - 10
                )
                player["mental_health"]["depression"] = max(
                    0, player["mental_health"]["depression"] - 8
                )

                slow_print(
                    f"{Fore.GREEN}Your mental well-being has improved from what you learned!{Style.RESET_ALL}"
                )
                decrease_stress(12)
            else:
                slow_print("You decide to skip the workshop.")

        elif event == "campus health fair":
            slow_print(
                f"\n{Fore.CYAN}There's a health fair happening on campus today.{Style.RESET_ALL}"
            )
            attend = input("Would you like to check it out? (Y/N): ").upper()

            if attend == "Y":
                slow_print("You visit various booths about physical and mental health.")
                slow_print("You learn about campus resources available to students.")

                # Improve mental health support network
                player["mental_health"]["support_network"] = min(
                    100, player["mental_health"]["support_network"] + 5
                )
                decrease_stress(8)

                # Chance to discover you have a neurodiversity trait if not already identified
                if not player["neurodiversity"]["traits"] and random.random() < 0.05:
                    slow_print(
                        f"\n{Fore.YELLOW}While talking to specialists at the fair, they suggest you might have traits of a neurodevelopmental condition.{Style.RESET_ALL}"
                    )
                    slow_print(
                        "They recommend you get assessed at the student health center."
                    )

                    choice = input("Would you like to get assessed? (Y/N): ").upper()
                    if choice == "Y":
                        # Select a random trait
                        trait = random.choice(list(NEURODIVERSITY_TRAITS.keys()))
                        severity = random.randint(3, 8)  # Scale 1-10, moderate severity

                        slow_print(
                            f"After assessment, you learn that you have {trait.replace('_', ' ')}."
                        )
                        player["neurodiversity"]["traits"].append(trait)
                        player["neurodiversity"]["severity"][trait] = severity
                        player["neurodiversity"][
                            "diagnosis_date"
                        ] = current_date.strftime("%Y-%m-%d")

                        # Ask about accommodations
                        slow_print(
                            f"The health center discusses possible accommodations for your {trait.replace('_', ' ')}."
                        )
                        accommodations_choice = input(
                            "Request academic accommodations? (Y/N): "
                        ).upper()
                        if accommodations_choice == "Y":
                            player["neurodiversity"]["accommodations"] = random.sample(
                                NEURODIVERSITY_TRAITS[trait]["accommodations"],
                                min(
                                    2,
                                    len(NEURODIVERSITY_TRAITS[trait]["accommodations"]),
                                ),
                            )
                            slow_print(
                                f"You are granted: {', '.join(player['neurodiversity']['accommodations'])}"
                            )
            else:
                slow_print("You decide to skip the health fair.")

        elif event == "therapy dog visit":
            slow_print(
                f"\n{Fore.CYAN}Therapy dogs are visiting campus today!{Style.RESET_ALL}"
            )
            slow_print(
                "You spend some time petting the dogs and chatting with their handlers."
            )

            # Mental health benefits
            decrease_stress(15)
            player["mental_health"]["happiness"] = min(
                100, player["mental_health"]["happiness"] + 10
            )
            player["mental_health"]["anxiety"] = max(
                0, player["mental_health"]["anxiety"] - 8
            )

            slow_print(
                f"{Fore.GREEN}The friendly animals really brightened your day!{Style.RESET_ALL}"
            )

    elif (
        event_chance == 2
        and player["romance_stage"] >= 3
        and player["romantic_interest"]
    ):
        # Romantic surprise event
        partner_name = player["romantic_interest"]
        slow_print(
            f"\n{Fore.MAGENTA}Surprise! {partner_name} was waiting for you outside class.{Style.RESET_ALL}"
        )
        slow_print("They brought you a small gift and wanted to see you.")

        # Improve relationship
        player["romance_points"] += random.randint(3, 8)
        decrease_stress(10)
        player["mental_health"]["happiness"] = min(
            100, player["mental_health"]["happiness"] + 8
        )

        slow_print(f"Your relationship with {partner_name} has grown stronger!")
        check_romance_stage_advancement(partner_name)

    else:
        slow_print(f"It's peaceful at the {location}.")

    advance_day()


def save_game(slot_name):
    """
    Save the current game state to a file
    
    Arguments:
    slot_name -- name of the save slot (without extension)
    """
    # Make sure the slot name doesn't already include .json
    clean_slot_name = slot_name.replace(".json", "")
    
    # Ensure relationship dictionary exists
    if not isinstance(relationship, dict):
        relationship_dict = {}
    else:
        relationship_dict = relationship
    
    game_data = {
        "player": player,
        "homework": homework,
        "teachers": teachers,
        "students": students,
        "relationship": relationship_dict,
        "quests": quests,
        "current_date": current_date.isoformat(),
    }
    
    # Always append .json extension
    filename = f"save_{clean_slot_name}.json"
    try:
        with open(filename, "w") as file:
            json.dump(game_data, file)
        slow_print(f"{Fore.GREEN}Game saved to {filename}.{Style.RESET_ALL}")
    except Exception as e:
        slow_print(f"{Fore.RED}Error saving game: {str(e)}{Style.RESET_ALL}")


def load_game(slot_name):
    """
    Load a saved game from a file
    
    Arguments:
    slot_name -- name of the save slot (without extension)
    """
    global player, homework, teachers, students, relationship, quests, current_date
    
    # Make sure the slot name doesn't already include .json
    clean_slot_name = slot_name.replace(".json", "")
    filename = f"save_{clean_slot_name}.json"
    
    # Check if the file exists
    if not os.path.exists(filename):
        # Check if they provided just "save_name" instead of "name"
        if slot_name.startswith("save_"):
            alt_filename = slot_name  # They already included save_ prefix
            if not os.path.exists(alt_filename) and not alt_filename.endswith(".json"):
                alt_filename += ".json"
        else:
            alt_filename = filename
            
        # If the alternative filename exists, use it
        if os.path.exists(alt_filename):
            filename = alt_filename
        else:
            slow_print(f"{Fore.RED}No save file found for {slot_name}.{Style.RESET_ALL}")
            return
    
    # Try to load the file
    try:
        with open(filename, "r") as file:
            game_data = json.load(file)
            
        # Update game state with loaded data
        player = game_data["player"]
        homework = game_data["homework"]
        teachers = game_data["teachers"]
        students = game_data["students"]
        
        # Safely load relationship data
        if "relationship" in game_data and isinstance(game_data["relationship"], dict):
            relationship = game_data["relationship"]
        else:
            relationship = {}
            slow_print(f"{Fore.YELLOW}Warning: Relationship data was missing or invalid. Initializing empty relationships.{Style.RESET_ALL}")
        
        quests = game_data["quests"]
        current_date = datetime.fromisoformat(game_data["current_date"])
        slow_print(f"{Fore.GREEN}Game loaded from {filename}.{Style.RESET_ALL}")
    except Exception as e:
        slow_print(f"{Fore.RED}Error loading game: {str(e)}{Style.RESET_ALL}")


def list_saves():
    files = [f for f in os.listdir() if f.endswith(".json")]
    if not files:
        print("No save files found.")
        return
    print("Available save slots:")
    for file in files:
        print(file)


# Main Loop
def display_save_slots():
    """Display and manage save slots for the game"""
    # Get only save game files (those starting with save_ and ending with .json)
    saves = [f for f in os.listdir() if f.startswith("save_") and f.endswith(".json")]
    
    print(f"\n{Fore.CYAN}================================{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}          SAVING SLOTS          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}================================{Style.RESET_ALL}")

    for i in range(5):  # Show 5 save slots
        if i < len(saves):
            save_file = saves[i]
            try:
                with open(save_file, "r") as f:
                    data = json.load(f)
                    player_name = data["player"]["name"]
                    save_time = os.path.getmtime(save_file)
                    timestamp = datetime.fromtimestamp(save_time).strftime("%d/%m/%Y %H:%M")
                print(f"{Fore.YELLOW}Saving slot {i+1}{Style.RESET_ALL}")
                print(f"File: {save_file}")
                print(f"Character: {player_name}")
                print(f"Saved on: {timestamp}")
            except Exception as e:
                print(f"{Fore.RED}Saving slot {i+1} (Error: {str(e)}){Style.RESET_ALL}")
                print(f"File: {save_file}")
                print("Status: corrupted save")
                print("Saved on: unknown")
        else:
            print(f"{Fore.WHITE}Saving slot {i+1}{Style.RESET_ALL}")
            print("File: empty")
            print("Character: none")
            print("Saved on: none")
        print(f"{Fore.CYAN}================================{Style.RESET_ALL}")

    try:
        slot_num = input(
            f"\n{Fore.GREEN}Select a slot number (1-5) or 0 to go back:{Style.RESET_ALL} "
        )
        if slot_num.isdigit():
            slot_num = int(slot_num)
            if 1 <= slot_num <= 5 and slot_num <= len(saves):
                # Extract the slot name from the save file name (remove save_ prefix and .json suffix)
                slot_name = saves[slot_num - 1][5:-5]  # Remove 'save_' and '.json'
                load_game(slot_name)
                return True
    except EOFError:
        print(f"\n{Fore.YELLOW}Returning to main menu due to input limitations.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        
    return False


# Student Templates
student_templates = {
    # First Year Templates
    "Nerdy Freshman": {
        "description": "A studious first-year student with high academic skills but low social skills.",
        "stats": {
            "charisma": {"social": 2, "academic": 8},
            "money": 1200,
            "school_year": 1,
            "electives": ["Computer Basics", "Economics Basics"],
            "grades": {
                "Math I": "A",
                "English I": "B",
                "Science I": "A",
                "History I": "B",
                "Literature I": "B",
                "PE I": "C",
                "Computer Basics": "A",
                "Economics Basics": "B",
            },
            "reputation": {"students": 10, "teachers": 30},
            "gpa": 3.5,
        },
    },
    "Sports Star": {
        "description": "An athletic first-year student who excels in physical activities but struggles with academics.",
        "stats": {
            "charisma": {"social": 8, "academic": 3},
            "money": 1500,
            "school_year": 1,
            "electives": ["PE I", "Music"],
            "grades": {
                "Math I": "C",
                "English I": "C",
                "Science I": "C",
                "History I": "C",
                "Literature I": "C",
                "PE I": "A",
                "Music": "B",
            },
            "reputation": {"students": 35, "teachers": 15},
            "gpa": 2.5,
            "pe_stats": {"strength": 3, "agility": 4, "endurance": 3, "technique": 2},
        },
    },
    "Social Butterfly": {
        "description": "A popular first-year student who knows everyone but doesn't focus much on studies.",
        "stats": {
            "charisma": {"social": 10, "academic": 2},
            "money": 2000,
            "school_year": 1,
            "electives": ["Music", "Art"],
            "grades": {
                "Math I": "D",
                "English I": "C",
                "Science I": "D",
                "History I": "C",
                "Literature I": "C",
                "PE I": "B",
                "Music": "B",
                "Art": "A",
            },
            "reputation": {"students": 45, "teachers": 10},
            "gpa": 2.0,
            "relationships": {
                "Haruki Takahashi": 25,
                "Emi Yamamoto": 30,
                "Ryo Tanaka": 20,
            },
        },
    },
    # Second Year Templates
    "Sophomore Scholar": {
        "description": "A second-year student focused on academic excellence with growing social confidence.",
        "stats": {
            "charisma": {"social": 4, "academic": 9},
            "money": 2500,
            "school_year": 2,
            "year_progress": 10,
            "electives": ["Computer Science", "Physics"],
            "grades": {
                "Math II": "A",
                "English II": "A",
                "World History": "A",
                "Literature II": "B",
                "PE II": "C",
                "Computer Science": "A",
                "Physics": "A",
            },
            "reputation": {"students": 25, "teachers": 50},
            "gpa": 3.8,
            "completed_years": [1],
            "clubs": ["Science Club"],
            "achievements": ["Academic Excellence"],
        },
    },
    "Campus Artist": {
        "description": "A creative second-year student who has made a name for themselves through their artistic talents.",
        "stats": {
            "charisma": {"social": 7, "academic": 5},
            "money": 3000,
            "school_year": 2,
            "year_progress": 15,
            "electives": ["Sociology", "Literature II"],
            "grades": {
                "Math II": "C",
                "English II": "B",
                "World History": "B",
                "Literature II": "A",
                "PE II": "C",
                "Sociology": "B",
            },
            "reputation": {"students": 40, "teachers": 30},
            "gpa": 3.0,
            "completed_years": [1],
            "clubs": ["Art Club"],
            "club_positions": {"Art Club": "Event Coordinator"},
            "romantic_interest": "Haruka Sato",
            "romance_stage": 2,
        },
    },
    # Third Year Templates
    "Junior Entrepreneur": {
        "description": "A third-year business-minded student with multiple part-time jobs and networking skills.",
        "stats": {
            "charisma": {"social": 8, "academic": 7},
            "money": 8000,
            "school_year": 3,
            "year_progress": 20,
            "electives": ["Economics", "Programming"],
            "grades": {
                "Math III": "B",
                "English III": "B",
                "Literature III": "B",
                "PE III": "B",
                "Economics": "A",
                "Programming": "B",
            },
            "reputation": {"students": 50, "teachers": 45},
            "gpa": 3.3,
            "completed_years": [1, 2],
            "clubs": ["Economics Club"],
            "club_positions": {"Economics Club": "Treasurer"},
            "internships": ["Business Intern"],
            "achievements": ["Money Maker", "Social Butterfly"],
        },
    },
    "Research Assistant": {
        "description": "A dedicated third-year student working closely with professors on advanced research.",
        "stats": {
            "charisma": {"social": 5, "academic": 10},
            "money": 4000,
            "school_year": 3,
            "year_progress": 25,
            "electives": ["Advanced Physics", "Advanced Chemistry"],
            "grades": {
                "Math III": "A",
                "English III": "B",
                "Literature III": "B",
                "PE III": "C",
                "Advanced Physics": "A",
                "Advanced Chemistry": "A",
            },
            "reputation": {"students": 20, "teachers": 65},
            "gpa": 3.7,
            "completed_years": [1, 2],
            "clubs": ["Science Club"],
            "club_positions": {"Science Club": "President"},
            "internships": ["Research Assistant"],
            "achievements": ["Teacher's Pet", "Academic Excellence"],
        },
    },
    # Fourth Year Templates
    "Senior Class President": {
        "description": "A well-respected fourth-year student who leads the student council and has excellent connections.",
        "stats": {
            "charisma": {"social": 10, "academic": 8},
            "money": 10000,
            "school_year": 4,
            "year_progress": 30,
            "electives": ["Business Management", "Ethics"],
            "grades": {
                "Math IV": "B",
                "English IV": "A",
                "Thesis Research": "A",
                "Career Planning": "A",
                "Literature IV": "B",
                "Business Management": "A",
                "Ethics": "A",
            },
            "reputation": {"students": 75, "teachers": 70},
            "gpa": 3.8,
            "completed_years": [1, 2, 3],
            "clubs": ["Student Council", "Debate Club"],
            "club_positions": {"Student Council": "President", "Debate Club": "Member"},
            "achievements": [
                "Club Leader",
                "Social Butterfly",
                "Teacher's Pet",
                "Perfect Attendance",
            ],
            "romantic_interest": "Sakura Yamamoto",
            "romance_stage": 5,
        },
    },
    "Future Scientist": {
        "description": "A brilliant fourth-year student with multiple research papers and graduate school offers.",
        "stats": {
            "charisma": {"social": 6, "academic": 10},
            "money": 6000,
            "school_year": 4,
            "year_progress": 35,
            "electives": ["Advanced Research", "Software Development"],
            "grades": {
                "Math IV": "A",
                "English IV": "A",
                "Thesis Research": "A+",
                "Career Planning": "A",
                "Literature IV": "B",
                "Advanced Research": "A+",
                "Software Development": "A",
            },
            "reputation": {"students": 30, "teachers": 90},
            "gpa": 4.0,
            "completed_years": [1, 2, 3],
            "clubs": ["Science Club", "Computer Club"],
            "club_positions": {"Science Club": "President", "Computer Club": "Member"},
            "internships": ["Research Assistant", "Tech Company Internship"],
            "achievements": ["Academic Excellence", "Teacher's Pet", "Quest Champion"],
        },
    },
    # Special Templates
    "Transfer Student": {
        "description": "A mysterious transfer student with an interesting background who can join at any year level.",
        "stats": {
            "charisma": {"social": 4, "academic": 4},
            "money": 5000,
            "school_year": 2,
            "electives": ["Art", "Sociology"],
            "grades": {
                "Math II": "B",
                "English II": "B",
                "World History": "B",
                "Literature II": "B",
                "PE II": "B",
                "Art": "A",
                "Sociology": "B",
            },
            "reputation": {"students": 15, "teachers": 15},
            "gpa": 3.2,
        },
    },
    "Exchange Student": {
        "description": "An international student with unique perspectives and cultural experience.",
        "stats": {
            "charisma": {"social": 6, "academic": 7},
            "money": 7000,
            "school_year": 3,
            "electives": ["Philosophy", "English III"],
            "grades": {
                "Math III": "B",
                "English III": "A+",
                "Literature III": "A",
                "PE III": "B",
                "Philosophy": "A",
                "Political Science": "A",
            },
            "reputation": {"students": 30, "teachers": 35},
            "gpa": 3.7,
            "completed_years": [1, 2],
            "relationships": {
                "Yuki Tanaka": 20,
                "Akira Suzuki": 15,
                "Haruki Takahashi": 25,
            },
        },
    },
}


def apply_template(template_name):
    """Apply selected template to the player"""
    global homework

    if template_name not in student_templates:
        print(f"Template {template_name} not found.")
        return False

    template = student_templates[template_name]

    # Apply stats from template
    stats = template["stats"]

    # Override basic player stats
    player["charisma"] = stats["charisma"]
    player["money"] = stats["money"]

    # Set school year (default to 1 if not specified)
    player["school_year"] = stats.get("school_year", 1)
    player["year_progress"] = stats.get("year_progress", 0)

    # Get subject data for the current year
    subjects_data = get_subjects_for_year(player["school_year"])

    # Get list of current subject names
    current_subjects = get_current_subjects()

    # Set electives based on available subjects for that year
    available_electives = []
    for subject_name, subject_data in subjects_data.items():
        if not subject_data.get("core", True):
            available_electives.append(subject_name)

    # If template specifies electives, use them, otherwise pick the first two available
    if "electives" in stats and all(
        elective in available_electives for elective in stats["electives"]
    ):
        player["electives"] = stats["electives"]
    else:
        player["electives"] = available_electives[: min(2, len(available_electives))]

    player["reputation"] = stats["reputation"]

    # Initialize homework for all subjects (core + electives)
    homework = {}
    for subject_name, subject_data in subjects_data.items():
        if subject_data.get("core", False) or subject_name in player.get(
            "electives", []
        ):
            homework[subject_name] = False

    # Apply grades, but only for current subjects
    player["grades"] = {}
    for subject_name in current_subjects:
        # If template has a grade for this subject, use it. Otherwise, default to C
        if "grades" in stats and subject_name in stats["grades"]:
            player["grades"][subject_name] = stats["grades"][subject_name]
        else:
            player["grades"][subject_name] = "C"

    # Apply GPA if specified
    if "gpa" in stats:
        player["gpa"] = stats["gpa"]
    else:
        # Calculate GPA based on grades
        calculate_final_grades()

    # Apply completed years if specified
    if "completed_years" in stats:
        player["completed_years"] = stats["completed_years"]

    # Apply relationships if present
    if "relationships" in stats:
        global relationship
        for student_name, points in stats["relationships"].items():
            relationship[student_name] = points

    # Apply romantic interest if present
    if "romantic_interest" in stats:
        player["romantic_interest"] = stats["romantic_interest"]
        player["romance_stage"] = stats.get("romance_stage", 0)
        player["romance_points"] = stats.get("romance_points", 0)

    # Apply clubs if present
    if "clubs" in stats:
        player["clubs"] = stats["clubs"]

    # Apply achievements if present
    if "achievements" in stats:
        player["achievements"] = stats["achievements"]

    # Update ranks based on new reputation
    update_ranks()

    print(
        f"\n{Fore.GREEN}Template '{template_name}' applied successfully!{Style.RESET_ALL}"
    )
    print(template["description"])

    # Show template status summary
    slow_print(f"\n{Fore.YELLOW}=== Template Status Summary ==={Style.RESET_ALL}")
    slow_print(f"School Year: {player['school_year']}")
    slow_print(f"GPA: {player['gpa']}")
    slow_print(f"Electives: {', '.join(player['electives'])}")
    slow_print(f"Money: ¥{player['money']}")
    slow_print(f"Social Charisma: {player['charisma']['social']}")
    slow_print(f"Academic Charisma: {player['charisma']['academic']}")

    if player["clubs"]:
        slow_print(f"Clubs: {', '.join(player['clubs'])}")

    if player["romantic_interest"]:
        stage_name = ROMANCE_STAGES[player["romance_stage"]]["name"]
        slow_print(f"Romance: {player['romantic_interest']} ({stage_name})")

    return True


def show_templates():
    """Display available student templates"""
    print(f"\n{Fore.CYAN}=== Student Templates ==={Style.RESET_ALL}")
    for name, template in student_templates.items():
        print(f"\n{Fore.YELLOW}{name}{Style.RESET_ALL}")
        print(f"Description: {template['description']}")
        print("Stats:")
        stats = template["stats"]
        print(
            f"  Social: {stats['charisma']['social']}, Academic: {stats['charisma']['academic']}"
        )
        print(f"  Starting Money: ¥{stats['money']}")
        print(f"  Electives: {', '.join(stats['electives'])}")
        print(
            f"  Reputation: Students {stats['reputation']['students']}, Teachers {stats['reputation']['teachers']}"
        )

    # Let user select a template
    print(f"\n{Fore.GREEN}Select a template (or 0 to go back):{Style.RESET_ALL}")
    template_names = list(student_templates.keys())
    for i, name in enumerate(template_names, 1):
        print(f"{i}. {name}")

    choice = input("Enter number: ")
    if choice == "0" or not choice.isdigit():
        return False

    choice_num = int(choice)
    if 1 <= choice_num <= len(template_names):
        template_name = template_names[choice_num - 1]
        return apply_template(template_name)
    else:
        print("Invalid selection.")
        return False


# Function to test colors
def test_color_display():
    """Test function to check if colors are displaying correctly"""
    print("\n=== COLOR TEST MODE ===")
    print("This is normal text (no color)")

    # Basic color tests
    print("{}This should be RED text{}".format(Fore.RED, Style.RESET_ALL))
    print("{}This should be GREEN text{}".format(Fore.GREEN, Style.RESET_ALL))
    print("{}This should be YELLOW text{}".format(Fore.YELLOW, Style.RESET_ALL))
    print("{}This should be BLUE text{}".format(Fore.BLUE, Style.RESET_ALL))
    print("{}This should be MAGENTA text{}".format(Fore.MAGENTA, Style.RESET_ALL))
    print("{}This should be CYAN text{}".format(Fore.CYAN, Style.RESET_ALL))
    print("{}This should be WHITE text{}".format(Fore.WHITE, Style.RESET_ALL))

    # Mixed color test
    print("\nMixed color test:")
    print(
        "Normal {}Red{} Normal {}Green{} Normal".format(
            Fore.RED, Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL
        )
    )

    # Background color test
    print("\nBackground color test:")
    print(
        "{}{}White text on red background{}".format(
            Back.RED, Fore.WHITE, Style.RESET_ALL
        )
    )
    print(
        "{}{}White text on blue background{}".format(
            Back.BLUE, Fore.WHITE, Style.RESET_ALL
        )
    )
    print(
        "{}{}Black text on green background{}".format(
            Back.GREEN, Fore.BLACK, Style.RESET_ALL
        )
    )

    # Style test
    print("\nStyle test:")
    print(
        "{}{}This should be BRIGHT yellow text{}".format(
            Style.BRIGHT, Fore.YELLOW, Style.RESET_ALL
        )
    )
    print(
        "{}{}This should be DIM blue text{}".format(
            Style.DIM, Fore.BLUE, Style.RESET_ALL
        )
    )

    # Test slow_print function with colors
    print("\nslow_print function test:")
    slow_print("This uses default slow_print (white text)", delay=0.01)
    slow_print("This should be cyan text with slow_print", color=Fore.CYAN, delay=0.01)
    slow_print(
        "This should be yellow bright text",
        color=Fore.YELLOW,
        style=Style.BRIGHT,
        delay=0.01,
    )
    slow_print(
        "{}This has embedded red{} in the text".format(Fore.RED, Style.RESET_ALL),
        delay=0.01,
    )

    # Color code embedding tests
    print("\nColor code embedding tests:")
    slow_print(
        "{0}Red text with {1}embedded cyan{0} and back to red{2}".format(
            Fore.RED, Fore.CYAN, Style.RESET_ALL
        ),
        delay=0.01,
    )
    slow_print(
        "{0}{1}Bright{2} and {3}Dim{2} in the same line{4}".format(
            Fore.YELLOW, Style.BRIGHT, Style.NORMAL, Style.DIM, Style.RESET_ALL
        ),
        delay=0.01,
    )

    print(
        "\nNote: If you don't see colors above, there may be compatibility issues with your terminal."
    )
    input("\nPress Enter to return to the main menu...")
    return show_main_menu()


def show_main_menu():
    print("\n{0}1. New game{1}".format(Fore.YELLOW, Style.RESET_ALL))
    print("{0}2. Continue game{1}".format(Fore.GREEN, Style.RESET_ALL))
    print("{0}3. Settings{1}".format(Fore.CYAN, Style.RESET_ALL))
    print(
        "{0}4. Student Templates (Password Required){1}".format(
            Fore.MAGENTA, Style.RESET_ALL
        )
    )
    print("{0}5. Test Colors (Debug){1}".format(Fore.BLUE, Style.RESET_ALL))

    try:
        choice = input(
            "\n{0}Select an option (1-5):{1} ".format(Fore.GREEN, Style.RESET_ALL)
        )
        if choice == "1":
            return False
        elif choice == "2":
            return display_save_slots()
        elif choice == "3":
            settings_menu()
            return show_main_menu()
        elif choice == "4":
            password = input(
                "{0}Enter password (hint: complete a school year or graduate):{1} ".format(
                    Fore.YELLOW, Style.RESET_ALL
                )
            )
            if password.upper() == "SCHOOLYEAREND":
                if show_templates():
                    return False  # Applied template, start new game
                else:
                    return show_main_menu()  # Return to main menu
            elif password.upper() == "GRADUATE":
                if show_graduate_templates():
                    return False  # Applied graduate template, start new game
                else:
                    return show_main_menu()  # Return to main menu
            else:
                print(
                    "{0}Incorrect password. Access denied.{1}".format(
                        Fore.RED, Style.RESET_ALL
                    )
                )
                print(
                    "Hint: Complete a school year or graduate to obtain special passwords."
                )
                return show_main_menu()
        elif choice == "5":
            return test_color_display()
        else:
            print(
                "{0}Invalid choice. Please select an option between 1 and 5.{1}".format(
                    Fore.RED, Style.RESET_ALL
                )
            )
            return show_main_menu()
    except EOFError:
        print(
            "{0}Input error encountered. Please try again.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        return False
    except Exception as e:
        print("{0}Error: {1}{2}".format(Fore.RED, str(e), Style.RESET_ALL))
        return False


def show_schedule():
    print("\n--- School Schedule ---")
    for day, events in school_events.items():
        print("{0}: {1}".format(day, ", ".join(events)))


def main(non_interactive=False):
    """Main game function that initializes and runs the game
    
    Arguments:
    non_interactive -- If True, skips interactive prompts and uses defaults
    """
    global ticks, player, relationship, current_date, students
    
    # Force color codes to work in environments like Replit
    os.environ["FORCE_COLOR"] = "1"
    
    # Re-initialize colorama to ensure it's working correctly
    if platform.system() == "Windows":
        init(autoreset=True, convert=True)
    else:
        init(autoreset=True, strip=False)
    
    # Print ASCII art with proper colors
    print(ASCII_ART)
    # Use f-strings for clearer color code formatting
    print(f"\n{Fore.MAGENTA}Welcome to a new school year!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Your journey through campus life begins...{Style.RESET_ALL}\n")

    # If in non-interactive mode, skip the menu and go directly to setup
    if non_interactive:
        print(f"{Fore.YELLOW}Running in non-interactive mode with default choices.{Style.RESET_ALL}")
        # Setup the game with defaults
        setup_game(non_interactive=True)
        
        # Display welcome message with instructions for non-interactive mode
        print(f"\n{Fore.GREEN}Hello {player['name']}!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Welcome to Campus Life! Type {Fore.YELLOW}/help{Fore.CYAN} to see available commands.{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}You're currently in {player['current_location']}.{Style.RESET_ALL}")
        # Skip the menu and continue directly to main game loop
        
    # Otherwise, show the menu as usual
    try:
        if not show_main_menu():
            setup_game()
    except EOFError:
        # If we get an EOF error, switch to non-interactive mode
        print(f"{Fore.YELLOW}Switching to non-interactive mode due to input limitations.{Style.RESET_ALL}")
        setup_game(non_interactive=True)
        
        # Display welcome message with consistent formatting using f-strings
        print(f"\n{Fore.GREEN}Hello {player['name']}!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Welcome to Campus Life! Type {Fore.YELLOW}/help{Fore.CYAN} to see available commands.{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}You're currently in {player['current_location']}.{Style.RESET_ALL}")

    # Main game loop
    while True:
        if current_date >= SCHOOL_YEAR_END:
            slow_print(
                "{0}The school year has ended! Thanks for playing!{1}".format(
                    Fore.YELLOW, Style.RESET_ALL
                )
            )
            print(
                "\n{0}Congratulations on completing a full school year!{1}".format(
                    Fore.CYAN, Style.RESET_ALL
                )
            )
            print(
                "{0}You've unlocked the Student Templates feature.{1}".format(
                    Fore.GREEN, Style.RESET_ALL
                )
            )
            print(
                "{0}Secret password: SCHOOLYEAREND{1}".format(Fore.YELLOW, Style.RESET_ALL)
            )
            print(
                "Use this password in the main menu to access special student templates for your next playthrough!"
            )
            break

        # Command processing
        command = ""
        
        # In non-interactive mode, auto-select help command first
        if non_interactive:
            print(f"\n{Fore.CYAN}Simulating a help command in non-interactive mode{Style.RESET_ALL}")
            command = "/help"
            # After displaying help, use /exit to end the game cleanly
            non_interactive = False  # Only do this automatic command once
        else:
            # In interactive mode, get command input from player
            try:
                command = input("\n{0}>>{1} ".format(Fore.GREEN, Style.RESET_ALL)).strip()
            except EOFError:
                print(f"{Fore.RED}Input error encountered. Please try again.{Style.RESET_ALL}")
                continue
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                continue
        
        # Process the command
        if not command.startswith("/"):
            print("Commands must start with '/'. Type /help for list of commands.")
            continue
            
        parts = command[1:].split()
        if not parts:
            continue
            
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        # Basic commands
        if cmd == "help":
            show_help()
        elif cmd == "exit":
            slow_print("\nThanks for playing! See you next time!")
            break
        elif cmd == "save":
            if args:
                save_game(args[0])
            else:
                print("Usage: /save [slot_name]")
        elif cmd == "load":
            if args:
                load_game(args[0])
            else:
                print("Usage: /load [slot_name]")
        elif cmd == "save_list":
            list_saves()
        elif cmd == "current_date":
            print(f"{Fore.CYAN}Current date: {current_date.strftime('%A, %B %d, %Y')}{Style.RESET_ALL}")
            if is_weekend():
                print(f"{Fore.YELLOW}It's the weekend!{Style.RESET_ALL}")
            elif is_holiday():
                print(f"{Fore.YELLOW}It's a holiday!{Style.RESET_ALL}")
        elif cmd == "time":
            # Show current time in the game
            current_hour = game_time.get("hour", 8)
            current_minute = game_time.get("minute", 0)
            am_pm = "AM" if current_hour < 12 else "PM"
            display_hour = current_hour if current_hour <= 12 else current_hour - 12
            if display_hour == 0:
                display_hour = 12
            print(f"{Fore.CYAN}Current Time: {display_hour}:{current_minute:02d} {am_pm}{Style.RESET_ALL}")
            
            # Show time period information
            period_name = "Morning" if current_hour < 12 else "Afternoon" if current_hour < 18 else "Evening"
            print(f"It's currently {period_name}.")
            
            # Check for specific time periods
            if 8 <= current_hour < 9:
                print(f"{Fore.YELLOW}It's breakfast time!{Style.RESET_ALL}")
            elif 12 <= current_hour < 13:
                print(f"{Fore.YELLOW}It's lunch time!{Style.RESET_ALL}")
            elif 18 <= current_hour < 19:
                print(f"{Fore.YELLOW}It's dinner time!{Style.RESET_ALL}")
            elif current_hour >= 22 or current_hour < 6:
                print(f"{Fore.BLUE}It's night time. Most students are sleeping.{Style.RESET_ALL}")
        elif cmd == "date":
            go_on_date(args)
        elif cmd == "schedule":
            show_schedule()
        elif cmd == "settings":
            settings_menu()

        # Status commands
        elif cmd == "me":
            show_me()
        elif cmd == "status":
            show_status()
        elif cmd == "homework":
            show_homework()
        elif cmd == "quests":
            show_quests()
        elif cmd == "achievements":
            show_achievements()
        elif cmd == "rumors":
            show_rumors()
        elif cmd == "relationship":
            show_relationship()
        elif cmd == "year":
            show_academic_year()

        # Location commands
        elif cmd == "go":
            go_location(args)
        elif cmd == "sleep":
            sleep_command(args)

        # Academic commands
        elif cmd == "study":
            study_subject(args)
        elif cmd == "teachers":
            show_teachers()
        elif cmd == "students":
            show_students()
        elif cmd == "student" and args and args[0] == "list":
            show_full_student_list()
        elif cmd == "npc" and args and args[0] == "list":
            show_npc_list(args[1:] if len(args) > 1 else None)
        elif cmd == "complete_quest":
            complete_quest(args)

        # Social commands
        elif cmd == "interact":
            interact_student(args)
        elif cmd == "clubs":
            show_clubs()
        elif cmd == "join_club":
            join_club(args)
        elif cmd == "leave_club":
            leave_club(args)
        elif cmd == "romance":
            show_romance()
        elif cmd == "partner":
            switch_active_partner(args)

        # Activities commands
        elif cmd == "work":
            if args:
                work_part_time(" ".join(args))
            else:
                print("Usage: /work [job_name]")
        elif cmd == "jobs":
            print("\nAvailable Jobs:")
            for job, details in jobs.items():
                print("{0}: ¥{1} per day".format(job, details["pay"]))
        elif cmd == "eat":
            eat_command(args)
        elif cmd == "relax":
            relax_command()

        # Change clothes command
        elif cmd == "change_clothes":
            change_clothes_command(args)

        # Unknown command
        else:
            print("Unknown command. Type /help for available commands.")

# Exam Questions by Subject
exam_questions = {
    "Math": [
        {
            "question": "What is the derivative of x²?",
            "answer": "2x",
            "options": ["x", "2x", "x²", "2"],
        },
        {
            "question": "What is the integral of 1/x?",
            "answer": "ln|x|",
            "options": ["x", "ln|x| + C", "1/x", "e^x"],
        },
        {
            "question": "Solve for x: 2x + 5 = 13",
            "answer": "4",
            "options": ["3", "4", "5", "6"],
        },
        {
            "question": "What is 15% of 200?",
            "answer": "30",
            "options": ["25", "30", "35", "40"],
        },
        {
            "question": "If a triangle has angles 30° and 60°, what is the third angle?",
            "answer": "90",
            "options": ["60", "75", "90", "120"],
        },
        {
            "question": "What is the square root of 144?",
            "answer": "12",
            "options": ["10", "11", "12", "14"],
        },
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for Gold?",
            "answer": "Au",
            "options": ["Ag", "Au", "Fe", "Cu"],
        },
        {
            "question": "What is the nearest planet to the Sun?",
            "answer": "Mercury",
            "options": ["Venus", "Mars", "Mercury", "Earth"],
        },
        {
            "question": "What is the human body's largest organ?",
            "answer": "Skin",
            "options": ["Heart", "Liver", "Brain", "Skin"],
        },
        {
            "question": "What is the speed of light?",
            "answer": "300,000 km/s",
            "options": ["200,000 km/s", "250,000 km/s", "300,000 km/s", "350,000 km/s"],
        },
        {
            "question": "What is the process of plants making food called?",
            "answer": "Photosynthesis",
            "options": ["Respiration", "Photosynthesis", "Digestion", "Absorption"],
        },
    ],
    "Literature": [
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "answer": "Shakespeare",
            "options": ["Dickens", "Shakespeare", "Hemingway", "Twain"],
        },
        {
            "question": "What is the main theme of 'The Great Gatsby'?",
            "answer": "American Dream",
            "options": ["Love", "War", "American Dream", "Family"],
        },
        {
            "question": "What is a metaphor?",
            "answer": "Comparison without like/as",
            "options": [
                "Direct comparison",
                "Comparison without like/as",
                "Sound repetition",
                "Word play",
            ],
        },
        {
            "question": "What is an autobiography?",
            "answer": "Self-written life story",
            "options": ["Fiction", "Biography", "Self-written life story", "Poetry"],
        },
        {
            "question": "What is alliteration?",
            "answer": "Same sound at start",
            "options": ["Rhyming", "Same sound at start", "Opposites", "Comparison"],
        },
    ],
    "History": [
        {
            "question": "When did World War II end?",
            "answer": "1945",
            "options": ["1943", "1944", "1945", "1946"],
        },
        {
            "question": "Who was the first President of the United States?",
            "answer": "George Washington",
            "options": [
                "John Adams",
                "Thomas Jefferson",
                "George Washington",
                "Benjamin Franklin",
            ],
        },
        {
            "question": "What ancient civilization built the pyramids?",
            "answer": "Egyptians",
            "options": ["Romans", "Greeks", "Egyptians", "Mayans"],
        },
        {
            "question": "In what year did the Berlin Wall fall?",
            "answer": "1989",
            "options": ["1985", "1987", "1989", "1991"],
        },
        {
            "question": "Who was the first Emperor of Japan?",
            "answer": "Emperor Jimmu",
            "options": [
                "Emperor Jimmu",
                "Emperor Meiji",
                "Emperor Hirohito",
                "Emperor Akihito",
            ],
        },
    ],
    "Art": [
        {
            "question": "Who painted the Mona Lisa?",
            "answer": "Leonardo da Vinci",
            "options": ["Van Gogh", "Leonardo da Vinci", "Picasso", "Monet"],
        },
        {
            "question": "What are the primary colors?",
            "answer": "Red, Blue, Yellow",
            "options": [
                "Red, Green, Blue",
                "Red, Blue, Yellow",
                "Red, Orange, Yellow",
                "Blue, Green, Yellow",
            ],
        },
        {
            "question": "What style is 'The Starry Night'?",
            "answer": "Post-Impressionism",
            "options": ["Realism", "Cubism", "Post-Impressionism", "Abstract"],
        },
        {
            "question": "What is chiaroscuro?",
            "answer": "Light and shadow contrast",
            "options": [
                "Color theory",
                "Brush technique",
                "Light and shadow contrast",
                "Perspective",
            ],
        },
        {
            "question": "What medium is used in fresco painting?",
            "answer": "Wet plaster",
            "options": ["Canvas", "Wood", "Wet plaster", "Paper"],
        },
    ],
}

# School Events Schedule
school_events = {
    "Monday": ["Morning Assembly", "Club Activities"],
    "Tuesday": ["Science Lab Day", "Sports Practice"],
    "Wednesday": ["Library Day", "Art Exhibition"],
    "Thursday": ["Math Competition", "Drama Club Performance"],
    "Friday": ["School Council Meeting", "Cultural Festival Planning"],
    "End of Month": ["Monthly Exams"],
}

# Class schedule and time tracking
class_schedule = {
    "morning_start": 9 * 10,  # 09:00 in ticks (10 ticks = 1 hour)
    "morning_end": 12 * 10,  # 12:00 in ticks
    "afternoon_start": 13 * 10,  # 13:00 in ticks
    "afternoon_end": 14 * 10,  # 14:00 in ticks
}

wake_up_time = 8 * 10  # 08:00 in ticks


def random_after_class_event():
    """Generate a random event that happens after class"""
    
    events = [
        {
            "type": "social",
            "description": "A group of students invite you to join them for a study session in the library.",
            "effect": lambda: {"energy": -5, "stress": -5, "charisma": {"academic": 1}}
        },
        {
            "type": "social",
            "description": "You overhear some students discussing the latest campus gossip.",
            "effect": lambda: {"stress": -3, "reputation": {"students": 2}}
        },
        {
            "type": "academic",
            "description": "Your teacher asks you to stay after class to discuss your recent homework.",
            "effect": lambda: {"stress": 8, "reputation": {"teachers": 3}, "charisma": {"academic": 1}}
        },
        {
            "type": "random",
            "description": "You find a 500 yen coin on the floor near your desk!",
            "effect": lambda: {"money": 500, "stress": -2}
        },
        {
            "type": "romance",
            "description": "A classmate shyly passes you a note with their phone number.",
            "effect": lambda: {"stress": -5, "charisma": {"social": 1}}
        },
        {
            "type": "academic",
            "description": "The teacher announces a pop quiz for tomorrow.",
            "effect": lambda: {"stress": 10}
        },
        {
            "type": "club",
            "description": "You notice a poster for a new club that's recruiting members.",
            "effect": lambda: {"stress": -2, "charisma": {"social": 1}}
        },
        {
            "type": "social",
            "description": "Some students are organizing a small party this weekend.",
            "effect": lambda: {"stress": -4, "reputation": {"students": 1}}
        },
        {
            "type": "health",
            "description": "You accidentally bump into someone and spill their drink.",
            "effect": lambda: {"stress": 5, "reputation": {"students": -1}}
        }
    ]
    
    # Only run event with 40% chance
    if random.random() < 0.4:
        event = random.choice(events)
        
        slow_print(f"\n{Fore.CYAN}AFTER CLASS EVENT:{Style.RESET_ALL}")
        slow_print(event["description"])
        
        # Apply event effects
        effects = event["effect"]()
        for key, value in effects.items():
            if key == "energy":
                player["energy"] = max(0, min(100, player["energy"] + value))
                slow_print(f"Energy {'increased' if value > 0 else 'decreased'} by {abs(value)}")
            elif key == "stress":
                player["stress"] = max(0, min(100, player["stress"] + value))
                slow_print(f"Stress {'increased' if value > 0 else 'decreased'} by {abs(value)}")
            elif key == "money":
                player["money"] += value
                slow_print(f"You gained {value} yen")
            elif key == "reputation":
                for rep_type, rep_value in value.items():
                    player["reputation"][rep_type] = max(0, player["reputation"][rep_type] + rep_value)
                    slow_print(f"{rep_type.capitalize()} reputation {'increased' if rep_value > 0 else 'decreased'} by {abs(rep_value)}")
            elif key == "charisma":
                for cha_type, cha_value in value.items():
                    player["charisma"][cha_type] += cha_value
                    slow_print(f"{cha_type.capitalize()} charisma increased by {cha_value}")
        
        # Check for romance event and add a special interaction opportunity
        if event["type"] == "romance" and random.random() < 0.5:
            # Pick a random suitable student
            potential_students = [s for s in students if s["gender"] != player["gender"]]
            if potential_students:
                student = random.choice(potential_students)
                student_name = student["name"]
                
                # Add some relationship points with this student
                if student_name not in relationship:
                    relationship[student_name] = 0
                    student_status[student_name] = "Stranger"
                
                relationship[student_name] += 10
                slow_print(f"{Fore.MAGENTA}The note was from {student_name}! Your relationship improved.{Style.RESET_ALL}")

def check_class_time():
    global ticks
    if ticks < wake_up_time:
        slow_print("You are sleeping. Wake up at 08:00.")
        return False
    elif wake_up_time <= ticks < class_schedule["morning_start"]:
        slow_print("You have some free time before class starts at 09:00.")
        return True
    elif class_schedule["morning_start"] <= ticks < class_schedule["morning_end"]:
        slow_print("You are in morning classes.")
        return True
    elif class_schedule["morning_end"] <= ticks < class_schedule["afternoon_start"]:
        slow_print("It's lunch break and free time.")
        return True
    elif class_schedule["afternoon_start"] <= ticks < class_schedule["afternoon_end"]:
        slow_print("You are in afternoon classes.")
        return True
    elif ticks == class_schedule["afternoon_end"]:
        slow_print("Classes just ended for the day.")
        # Trigger random after-class event
        random_after_class_event()
        return True
    else:
        slow_print("You have free time now.")
        return True


# Sanctions for missing classes or other infractions
def apply_sanction(reason):
    if reason == "missed_class":
        slow_print(
            "{0}You missed a class! Your teacher is disappointed.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        player["reputation"]["teachers"] -= 10
        player["charisma"]["academic"] = max(player["charisma"]["academic"] - 1, 0)
    elif reason == "late_to_class":
        slow_print(
            "{0}You were late to class! You lose some reputation.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        player["reputation"]["teachers"] -= 5
    elif reason == "missed_homework":
        slow_print(
            "{0}You didn't complete your homework! Your grade might suffer.{1}".format(
                Fore.RED, Style.RESET_ALL
            )
        )
        player["reputation"]["teachers"] -= 7
    elif reason == "uniform_violation":
        # First uniform violation is a warning
        if player.get("uniform_violations", 0) == 0:
            slow_print(
                "{0}The teacher scolds you for not wearing the proper school uniform!{1}".format(
                    Fore.RED, Style.RESET_ALL
                )
            )
            slow_print("You receive a warning. Next time there will be consequences.")
            player["uniform_violations"] = 1
            player["reputation"]["teachers"] -= 5
            player["stress"] += 10
        # Second violation is detention
        elif player.get("uniform_violations", 0) == 1:
            slow_print(
                "{0}This is your second uniform violation!{1}".format(
                    Fore.RED, Style.RESET_ALL
                )
            )
            slow_print(
                "You're given detention after school, which takes up your free time."
            )
            player["uniform_violations"] = 2
            player["reputation"]["teachers"] -= 10
            player["energy"] -= 15  # Detention is tiring
            player["stress"] += 15
            # Skip ahead in time
            global ticks
            ticks += 10  # Add an hour for detention
        # Third violation is a meeting with parents/principal
        else:
            slow_print(
                "{0}This is your third uniform violation! The principal is very disappointed.{1}".format(
                    Fore.RED, Style.RESET_ALL
                )
            )
            slow_print(
                "You're scheduled for a disciplinary meeting with the principal."
            )
            slow_print("Your reputation with teachers suffers significantly.")
            player["reputation"]["teachers"] = max(
                0, player["reputation"]["teachers"] - 20
            )
            player["stress"] += 25
            # Reset counter for next set of violations
            player["uniform_violations"] = 0
    else:
        slow_print(
            "{0}You received a sanction: {1}{2}".format(
                Fore.RED, reason, Style.RESET_ALL
            )
        )

    update_ranks()


# Modify main loop or relevant command handlers to call check_class_time and enforce class attendance


def take_exam(subject):
    print("\n{0}=== {1} Exam ==={2}".format(Fore.YELLOW, subject, Style.RESET_ALL))
    
    # Check if this is a PE exam to apply seasonal effects
    if subject.startswith("PE"):
        season = get_current_season()
        if season == "summer":
            if "strong" in player.get("traits", []):
                slow_print(f"{Fore.GREEN}Your strength helps you handle the summer heat during the PE exam.{Style.RESET_ALL}")
            elif "heat_sensitive" in player.get("traits", []):
                slow_print(f"{Fore.RED}The summer heat makes this PE exam especially challenging for you.{Style.RESET_ALL}")
            else:
                slow_print(f"{Fore.YELLOW}The summer heat makes this PE exam more challenging.{Style.RESET_ALL}")
        elif season == "winter" and "cold_sensitive" in player.get("traits", []):
            slow_print(f"{Fore.RED}The cold weather makes this PE exam more difficult for you.{Style.RESET_ALL}")

    # Apply trait effects for academic subjects
    trait_bonuses = []
    for trait in player.get("traits", []):
        trait_info = PLAYER_TRAITS.get(trait, {})
        effects = trait_info.get("effects", {})
        
        # Academic trait bonuses
        if subject.startswith("Math") and "math_bonus" in effects:
            trait_bonuses.append(f"{trait.title()} gives you a math advantage")
        elif subject.startswith("Science") and "science_bonus" in effects:
            trait_bonuses.append(f"{trait.title()} gives you a science advantage")
        elif subject == "Art" and "art_bonus" in effects:
            trait_bonuses.append(f"{trait.title()} gives you an artistic advantage")
        elif subject == "Music" and "music_bonus" in effects:
            trait_bonuses.append(f"{trait.title()} gives you a musical advantage")
        elif "study_efficiency" in effects and effects["study_efficiency"] > 0:
            trait_bonuses.append(f"{trait.title()} helps with studying efficiency")
        
    # Display trait advantages if any
    if trait_bonuses:
        advantages_text = ", ".join(trait_bonuses)
        slow_print(f"{Fore.GREEN}Trait advantage: {advantages_text}{Style.RESET_ALL}")
    
    total_questions = random.randint(
        6, 10
    )  # Random number of questions between 6 and 10
    questions = random.sample(
        exam_questions[subject], min(total_questions, len(exam_questions[subject]))
    )
    base_score = 0

    for i, q in enumerate(questions, 1):
        print(
            "\n{0}Question {1}:{2} {3}".format(
                Fore.CYAN, i, Style.RESET_ALL, q["question"]
            )
        )
        for j, option in enumerate(q["options"], 1):
            print("{0}. {1}".format(j, option))

        answer = input(
            "\n{0}Your answer (1-{1}):{2} ".format(
                Fore.GREEN, len(q["options"]), Style.RESET_ALL
            )
        )
        if answer.isdigit() and 1 <= int(answer) <= len(q["options"]):
            if q["options"][int(answer) - 1] == q["answer"]:
                base_score += 10 / total_questions  # Score scaled by number of questions
                print("{0}Correct!{1}".format(Fore.GREEN, Style.RESET_ALL))
            else:
                print(
                    "{0}Incorrect! The answer was: {1}{2}".format(
                        Fore.RED, q["answer"], Style.RESET_ALL
                    )
                )
        else:
            print("{0}Invalid answer! Skipping...{1}".format(Fore.RED, Style.RESET_ALL))

    # Apply trait effects to the base score
    modified_score = apply_trait_effects_to_exam(subject, base_score)
    
    # If score was modified, show the difference
    if modified_score != base_score:
        if modified_score > base_score:
            slow_print(f"{Fore.GREEN}Your traits helped improve your score from {base_score:.1f} to {modified_score:.1f}!{Style.RESET_ALL}")
        else:
            slow_print(f"{Fore.RED}Your score was reduced from {base_score:.1f} to {modified_score:.1f} due to trait/seasonal effects.{Style.RESET_ALL}")
    
    return modified_score


def check_monthly_exam():
    global current_date
    if current_date.day == 28:  # End of month exam
        print("\n{0}=== Monthly Exams ==={1}".format(Fore.YELLOW, Style.RESET_ALL))
        for subject in subjects:
            score = take_exam(subject)
            # Calculate grade based on score with A+, A++, no E, and D, F grades
            if score >= 9.5:
                new_grade = "A++"
            elif score >= 9:
                new_grade = "A+"
            elif score >= 8:
                new_grade = "A"
            elif score >= 7:
                new_grade = "B"
            elif score >= 5:
                new_grade = "C"
            elif score >= 3:
                new_grade = "D"
            else:
                new_grade = "F"

            player["grades"][subject] = new_grade
            print(
                "\n{0} exam score: {1}/10 (Grade: {2})".format(
                    subject, score, new_grade
                )
            )

        # Update teacher reputation based on grades and homework
        completed_homework = sum(1 for done in homework.values() if done)
        good_grades = sum(
            1 for grade in player["grades"].values() if grade in ["A++", "A+", "A", "B"]
        )

        reputation_gain = completed_homework * 2 + good_grades * 3
        player["reputation"]["teachers"] += reputation_gain
        print(
            "\n{0}Teacher reputation increased by {1} points!{2}".format(
                Fore.CYAN, reputation_gain, Style.RESET_ALL
            )
        )
        update_ranks()


# Random Events
random_events = [
    {
        "type": "positive",
        "description": "Found some money in the courtyard! (+500 yen)",
        "effect": {"money": 500},
    },
    {
        "type": "negative",
        "description": "Lost your textbook! (-1000 yen)",
        "effect": {"money": -1000},
    },
    {
        "type": "positive",
        "description": "Teacher praised your work! (+5 teacher reputation)",
        "effect": {"teacher_rep": 5},
    },
    {
        "type": "negative",
        "description": "Arrived late to class! (-3 teacher reputation)",
        "effect": {"teacher_rep": -3},
    },
    {
        "type": "positive",
        "description": "Helped a classmate! (+5 student reputation)",
        "effect": {"student_rep": 5},
    },
    {
        "type": "neutral",
        "description": "Someone left a note in your locker...",
        "effect": {"quest": True},
    },
    {
        "type": "neutral",
        "description": "Saw a cute cat on the way to school.",
        "effect": {},
    },
    {
        "type": "positive",
        "description": "Won a small prize in the school lottery! (+100 yen)",
        "effect": {"money": 100},
    },
    {
        "type": "negative",
        "description": "Got caught in a rainstorm without an umbrella! (-50 energy)",
        "effect": {"energy": -50},
    },
    {
        "type": "positive",
        "description": "Helped a classmate with homework! (+5 student reputation)",
        "effect": {"student_rep": 5},
    },
    {
        "type": "negative",
        "description": "Had a disagreement with a classmate. (-5 student reputation)",
        "effect": {"student_rep": -5},
    },
    {
        "type": "neutral",
        "description": "Saw a beautiful sunset on the way home.",
        "effect": {},
    },
    {
        "type": "positive",
        "description": "Helped a teacher with a project! (+10 teacher reputation)",
        "effect": {"teacher_rep": 10},
    },
    {
        "type": "negative",
        "description": "Forgot your lunch at home! (-20 energy)",
        "effect": {"energy": -20},
    },
]

# Special templates unlocked with the GRADUATE password
graduate_templates = {
    "Academic Prodigy": {
        "description": "A gifted student with exceptional academic abilities, awarded a prestigious scholarship.",
        "stats": {
            "charisma": {"social": 5, "academic": 10},
            "money": 3000,
            "school_year": 1,
            "year_progress": 0,
            "electives": ["Advanced Math", "Physics"],
            "grades": {
                "Math I": "A+",
                "English I": "A",
                "Science I": "A+",
                "History I": "A",
                "PE I": "B",
                "Advanced Math": "A+",
                "Physics": "A",
            },
            "reputation": {"students": 40, "teachers": 90},
            "gpa": 3.9,
            "completed_years": [],
            "clubs": ["Science Club", "Math Club"],
            "club_positions": {"Science Club": "Member", "Math Club": "Member"},
            "achievements": [
                "Academic Excellence",
                "Scholarship Recipient",
                "Science Olympiad",
            ],
        },
    },
    "Social Influencer": {
        "description": "A charismatic student who already has a large social media following and campus popularity.",
        "stats": {
            "charisma": {"social": 10, "academic": 5},
            "money": 5000,
            "school_year": 1,
            "year_progress": 0,
            "electives": ["Media Studies", "Psychology"],
            "grades": {
                "Math I": "C",
                "English I": "B+",
                "Science I": "C+",
                "History I": "B",
                "PE I": "A",
                "Media Studies": "A+",
                "Psychology": "A",
            },
            "reputation": {"students": 95, "teachers": 50},
            "gpa": 3.2,
            "completed_years": [],
            "clubs": ["Drama Club", "Student Council"],
            "club_positions": {
                "Drama Club": "Member",
                "Student Council": "Public Relations",
            },
            "achievements": ["Social Butterfly", "Campus Celebrity", "Trend Setter"],
        },
    },
    "Exchange Student": {
        "description": "An international student with diverse experiences and a unique global perspective.",
        "stats": {
            "charisma": {"social": 7, "academic": 7},
            "money": 4000,
            "school_year": 2,
            "year_progress": 0,
            "electives": ["International Relations", "Cultural Studies"],
            "grades": {
                "Math II": "B+",
                "English II": "A",
                "Science II": "B",
                "History II": "A+",
                "PE II": "B",
                "International Relations": "A",
                "Cultural Studies": "A+",
            },
            "reputation": {"students": 60, "teachers": 70},
            "gpa": 3.7,
            "completed_years": [1],
            "clubs": ["International Club", "Language Exchange"],
            "club_positions": {
                "International Club": "Vice President",
                "Language Exchange": "Coordinator",
            },
            "achievements": ["Multilingual", "Cultural Ambassador", "Global Citizen"],
        },
    },
    "Campus Entrepreneur": {
        "description": "A business-minded student who already runs a successful campus startup.",
        "stats": {
            "charisma": {"social": 9, "academic": 7},
            "money": 10000,
            "school_year": 3,
            "year_progress": 0,
            "electives": ["Business Management", "Marketing"],
            "grades": {
                "Math III": "B",
                "English III": "B+",
                "Science III": "B",
                "History III": "B+",
                "PE III": "B",
                "Business Management": "A+",
                "Marketing": "A",
            },
            "reputation": {"students": 80, "teachers": 75},
            "gpa": 3.5,
            "completed_years": [1, 2],
            "clubs": ["Business Club", "Entrepreneurship Society"],
            "club_positions": {
                "Business Club": "President",
                "Entrepreneurship Society": "Founder",
            },
            "internships": ["Marketing Intern", "Startup Accelerator"],
            "achievements": ["Business Leader", "Investor", "Innovation Award"],
        },
    },
    "Double Major": {
        "description": "An ambitious student pursuing two full degree programs simultaneously.",
        "stats": {
            "charisma": {"social": 4, "academic": 9},
            "money": 2000,
            "school_year": 2,
            "year_progress": 0,
            "electives": ["Advanced Literature", "Philosophy"],
            "grades": {
                "Math II": "A",
                "English II": "A+",
                "Science II": "A",
                "History II": "A+",
                "PE II": "C",
                "Advanced Literature": "A+",
                "Philosophy": "A",
            },
            "reputation": {"students": 30, "teachers": 85},
            "gpa": 3.8,
            "completed_years": [1],
            "clubs": ["Literature Club", "Philosophy Club"],
            "club_positions": {
                "Literature Club": "Member",
                "Philosophy Club": "Member",
            },
            "achievements": ["Bookworm", "Academic Excellence", "All-Nighter"],
        },
    },
}


def show_graduate_templates():
    """Display special graduate templates unlocked after completing the game"""
    print(
        "\n{0}=== Graduate Templates (Special) ==={1}".format(
            Fore.MAGENTA, Style.RESET_ALL
        )
    )
    print(
        "{0}These enhanced templates are unlocked by completing the game.{1}".format(
            Fore.CYAN, Style.RESET_ALL
        )
    )

    for idx, (name, template) in enumerate(graduate_templates.items(), 1):
        year_names = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
        year_name = year_names.get(
            template["stats"]["school_year"],
            "Year {0}".format(template["stats"]["school_year"]),
        )

        print("\n{0}. {1}{2}{3}".format(idx, Fore.GREEN, name, Style.RESET_ALL))
        print("   Description: {0}".format(template["description"]))
        print(
            "   Year: {0} (Year {1})".format(
                year_name, template["stats"]["school_year"]
            )
        )
        print(
            "   Academic Charisma: {0}".format(
                template["stats"]["charisma"]["academic"]
            )
        )
        print("   Social Charisma: {0}".format(template["stats"]["charisma"]["social"]))
        print("   Starting Money: ¥{0}".format(template["stats"]["money"]))
        print("   Starting GPA: {0}".format(template["stats"]["gpa"]))
        if "achievements" in template["stats"]:
            print(
                "   Starting Achievements: {0}".format(
                    ", ".join(template["stats"]["achievements"])
                )
            )
        if "clubs" in template["stats"]:
            print(
                "   Starting Clubs: {0}".format(", ".join(template["stats"]["clubs"]))
            )

    print(
        "\n{0}Choose a template (1-{1}) or press Enter to go back:{2}".format(
            Fore.YELLOW, len(graduate_templates), Style.RESET_ALL
        )
    )
    choice = input()

    if not choice:
        return False

    try:
        idx = int(choice)
        if 1 <= idx <= len(graduate_templates):
            template_name = list(graduate_templates.keys())[idx - 1]
            apply_graduate_template(template_name)
            return True
        else:
            print("Invalid selection.")
            return False
    except ValueError:
        print("Please enter a number.")
        return False


def apply_graduate_template(template_name):
    """Apply selected graduate template to the player with special bonuses"""
    global homework

    if template_name not in graduate_templates:
        print("Template {0} not found.".format(template_name))
        return False

    template = graduate_templates[template_name]

    # Apply stats from template
    stats = template["stats"]

    # Override basic player stats
    player["charisma"] = stats["charisma"]
    player["money"] = stats["money"]

    # Set school year
    player["school_year"] = stats.get("school_year", 1)
    player["year_progress"] = stats.get("year_progress", 0)

    # Get subject data for the current year
    subjects_data = get_subjects_for_year(player["school_year"])

    # Get list of current subject names
    current_subjects = get_current_subjects()

    # Set electives based on available subjects for that year
    available_electives = []
    for subject_name, subject_data in subjects_data.items():
        if not subject_data.get("core", True):
            available_electives.append(subject_name)

    # If template specifies electives, use them, otherwise pick the first two available
    if "electives" in stats and all(
        elective in available_electives for elective in stats["electives"]
    ):
        player["electives"] = stats["electives"]
    else:
        player["electives"] = available_electives[: min(2, len(available_electives))]

    player["reputation"] = stats["reputation"]

    # Initialize homework for all subjects (core + electives)
    homework = {}
    for subject_name, subject_data in subjects_data.items():
        if subject_data.get("core", False) or subject_name in player.get(
            "electives", []
        ):
            homework[subject_name] = False

    # Apply grades, but only for current subjects
    player["grades"] = {}
    for subject_name in current_subjects:
        # If template has a grade for this subject, use it. Otherwise, default to B
        if "grades" in stats and subject_name in stats["grades"]:
            player["grades"][subject_name] = stats["grades"][subject_name]
        else:
            player["grades"][
                subject_name
            ] = "B"  # Start with better grades in graduate templates

    # Apply GPA if specified
    if "gpa" in stats:
        player["gpa"] = stats["gpa"]
    else:
        # Calculate GPA based on grades
        calculate_final_grades()

    # Apply completed years if specified
    if "completed_years" in stats:
        player["completed_years"] = stats["completed_years"]

    # Apply relationships if present
    if "relationships" in stats:
        global relationship
        for student_name, points in stats["relationships"].items():
            relationship[student_name] = points

    # Apply romantic interest if present
    if "romantic_interest" in stats:
        player["romantic_interest"] = stats["romantic_interest"]
        player["romance_stage"] = stats.get("romance_stage", 0)
        player["romance_points"] = stats.get("romance_points", 0)

    # Apply clubs if present
    if "clubs" in stats:
        player["clubs"] = stats["clubs"]
        player["club_positions"] = stats.get("club_positions", {})
    else:
        player["clubs"] = []
        player["club_positions"] = {}

    # Apply achievements if present
    if "achievements" in stats:
        player["achievements"] = stats["achievements"]
    else:
        player["achievements"] = []

    # Apply internships if present (for year 3+)
    if "internships" in stats:
        player["internships"] = stats["internships"]

    # Graduate template bonus: better health and energy
    player["health"] = 100
    player["energy"] = 100
    player["stress"] = 0
    player["hunger"] = 100

    # Update ranks based on new reputation
    update_ranks()

    print(
        "\n{0}Graduate Template '{1}' applied successfully!{2}".format(
            Fore.MAGENTA, template_name, Style.RESET_ALL
        )
    )
    print(template["description"])

    # Show template status summary
    slow_print(
        "\n{0}=== Graduate Template Status Summary ==={1}".format(
            Fore.YELLOW, Style.RESET_ALL
        )
    )
    slow_print("School Year: {0}".format(player["school_year"]))
    slow_print("GPA: {0}".format(player["gpa"]))
    slow_print("Electives: {0}".format(", ".join(player["electives"])))
    slow_print("Money: ¥{0}".format(player["money"]))
    slow_print("Social Charisma: {0}".format(player["charisma"]["social"]))
    slow_print("Academic Charisma: {0}".format(player["charisma"]["academic"]))

    if player["clubs"]:
        club_info = []
        for club in player["clubs"]:
            position = player["club_positions"].get(club, "Member")
            club_info.append("{0} ({1})".format(club, position))
        slow_print("Clubs: {0}".format(", ".join(club_info)))

    if "achievements" in stats and stats["achievements"]:
        slow_print("Achievements: {0}".format(", ".join(stats["achievements"])))

    if "internships" in stats and stats["internships"]:
        slow_print("Internships: {0}".format(", ".join(stats["internships"])))

    if player["romantic_interest"]:
        stage_name = ROMANCE_STAGES[player["romance_stage"]]["name"]
        slow_print("Romance: {0} ({1})".format(player["romantic_interest"], stage_name))

    # Special message for graduate templates
    slow_print(
        "\n{0}As a special graduate template, you start with enhanced abilities and opportunities!{1}".format(
            Fore.CYAN, Style.RESET_ALL
        )
    )
    slow_print(
        "{0}Make the most of your campus life experience!{1}".format(
            Fore.CYAN, Style.RESET_ALL
        )
    )

    return True


# No longer auto-execute main() when imported
# This allows the runner scripts to explicitly call main() instead
if __name__ == "__main__":
    main()
